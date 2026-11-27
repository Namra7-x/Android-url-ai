#!/usr/bin/env python3
"""
High-Speed 4-Wave Concurrent Web & Early-Signal Hunt Pipeline.

Wave 1 (Parallel Discovery): subfinder+dnsx+wellknown | Scrapling | katana | waymore+urlfinder
Wave 2 (Chunk Download):     3-hop parallel fetcher with Scrapling cookie fallback + SHA-256 dedup
Wave 3 (Offline Analysis):   jsluice | xnLinkFinder | sourcemapper | Jscope | trufflehog+titus
Wave 4 (Verify & Feed):      uro -> httpx -> vhost -> wordlist -> ferox/ffuf -> x8 -> nuclei -> ai_feed.json
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import signal
import ssl
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError, as_completed, wait
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import hunt_utils as hu  # noqa: E402
import wordlist  # noqa: E402

SCRIPT_SRC_RE = re.compile(r"<script[^>]+src=[\"'`]([^\"'`]+)[\"'`]", re.I)
LINK_MODULE_RE = re.compile(r"<link[^>]+href=[\"'`]([^\"'`]+\.(?:js|mjs|json))[\"'`]", re.I)
SOURCEMAP_COMMENT_RE = re.compile(r"//#\s*sourceMappingURL=([^\s]+)")
JS_REF_RE = re.compile(r"[\"'`]((?:https?://[^\"'`\s]+|/[A-Za-z0-9_./-]+\.(?:js|mjs|json|map)(?:\?[^\"'`\s]*)?))[\"'`]")
FEATURE_FLAG_RE = re.compile(
    r"(?:feature[-_]?[fF]lag[s]?|experiment[s]?|role|isAdmin|enable[A-Z][A-Za-z0-9_]+|use[A-Z][A-Za-z0-9_]*Flag)\s*[:=]\s*[\"'`]?([A-Za-z0-9_.:-]{2,64})",
)
MODEL_CANDIDATE_RE = re.compile(
    r"[\"'`]((?:claude|gemini|gpt|o[134]|devin|deepseek|qwen|llama|grok|sonar|veo|imagen|chirp|hydrogen|sonnet|opus|haiku)[-_a-z0-9.]{1,48})[\"'`]",
    re.I,
)


class HuntRunner:
    def __init__(self, target_url: str, out_root: Path, settings: dict[str, Any], budget_min: float | None) -> None:
        self.base_url = hu.normalize_url(target_url) or target_url.strip()
        if not self.base_url.startswith(("http://", "https://")):
            self.base_url = "https://" + self.base_url
        parsed = urlparse(self.base_url)
        self.exact_host, self.subfinder_domain, self.scope_apex = hu.extract_apex_domain(parsed.netloc)
        self.target_dir = out_root / self.exact_host
        self.logs_dir = self.target_dir / "logs"
        self.target_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        self.settings = settings
        budget_sec = int(budget_min * 60) if budget_min else int(settings.get("target_budget_seconds", 660))
        reserve_sec = int(settings.get("save_reserve_seconds", 45))
        self.timer = hu.BudgetTimer(budget_sec, reserve_seconds=reserve_sec)

        self._lock = threading.Lock()
        self.routes: dict[str, dict[str, Any]] = {}
        self.third_party: dict[str, dict[str, Any]] = {}
        self.js_urls: set[str] = set()
        self.tool_statuses: list[dict[str, Any]] = []
        self.scrapling_cookies: dict[str, str] = {}
        self.scrapling_ua: str = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

    def _run_cmd(
        self,
        cmd: list[str],
        log_path: Path,
        timeout: int = 120,
        stdout_path: Path | None = None,
        read_stdout: bool = True,
    ) -> tuple[int, str]:
        return hu.run_cmd(
            cmd,
            log_path,
            timeout=timeout,
            stdout_path=stdout_path,
            stop_event=self.timer.stop_event,
            read_stdout=read_stdout,
        )

    def enabled(self, key: str) -> bool:
        return bool(self.settings.get(key, True))

    def record_status(self, tool: str, exit_code: int, duration_s: float, detail: str) -> None:
        with self._lock:
            self.tool_statuses.append({
                "tool": tool,
                "exit_code": exit_code,
                "duration_s": round(duration_s, 1),
                "detail": detail,
            })

    def add_url(self, raw: str, source: str, method: str = "GET") -> None:
        norm = hu.normalize_url(raw, self.base_url)
        if not norm:
            return
        if hu.is_js_or_map_url(norm):
            with self._lock:
                if hu.is_first_party(norm, self.exact_host, self.scope_apex):
                    self.js_urls.add(norm)
        bucket = self.routes if hu.is_first_party(norm, self.exact_host, self.scope_apex) else self.third_party
        key = hu.dedupe_key(norm)
        with self._lock:
            entry = bucket.get(key)
            if entry is None:
                bucket[key] = {"url": norm, "method": method.upper(), "sources": [source]}
            elif source not in entry["sources"]:
                entry["sources"].append(source)

    def _http_get(self, url: str, timeout: int = 8, headers: dict[str, str] | None = None) -> tuple[int, dict[str, str], bytes]:
        hdrs = {"User-Agent": self.scrapling_ua, "Accept": "*/*"}
        if self.scrapling_cookies:
            hdrs["Cookie"] = "; ".join(f"{k}={v}" for k, v in self.scrapling_cookies.items())
        if headers:
            hdrs.update(headers)
        req = urllib.request.Request(url, headers=hdrs, method="GET")
        ctx = ssl.create_default_context()
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
                return resp.status, dict(resp.headers), resp.read(5 * 1024 * 1024)
        except urllib.error.HTTPError as err:
            body = b""
            try:
                body = err.read(256 * 1024)
            except Exception:  # noqa: BLE001
                pass
            return err.code, dict(err.headers or {}), body
        except Exception:  # noqa: BLE001
            return 0, {}, b""

    # ------------------------------------------------------------------
    # WAVE 1: Parallel Discovery
    # ------------------------------------------------------------------
    def _step_subdomains_and_wellknown(self, wave_deadline: float) -> list[str]:
        t0 = time.monotonic()
        live_subs: list[str] = []

        if self.enabled("enable_subdomains") and hu.which("subfinder") and not self.timer.stopped():
            sf_out = self.target_dir / "subfinder.txt"
            cap = self.timer.cap(self.settings.get("subfinder_timeout", 60), wave_deadline)
            rc, _ = self._run_cmd(
                ["subfinder", "-d", self.subfinder_domain, "-silent", "-all", "-o", str(sf_out)],
                self.logs_dir / "subfinder.log",
                timeout=cap,
                read_stdout=False,
            )
            max_subs = int(self.settings.get("max_subdomains", 2000))
            subs_set: set[str] = set()
            if sf_out.is_file():
                with sf_out.open("r", encoding="utf-8", errors="replace") as fh:
                    for line in fh:
                        s = line.strip().lower()
                        if s:
                            subs_set.add(s)
                            if len(subs_set) >= max_subs:
                                break
            subs = sorted(subs_set)
            (self.target_dir / "subdomains_all.txt").write_text("\n".join(subs) + ("\n" if subs else ""), encoding="utf-8")

            if subs and hu.which("dnsx") and not self.timer.stopped():
                dns_out = self.target_dir / "dnsx.jsonl"
                rc2, _ = self._run_cmd(
                    ["dnsx", "-l", str(self.target_dir / "subdomains_all.txt"), "-silent", "-a", "-cname", "-resp", "-json", "-o", str(dns_out)],
                    self.logs_dir / "dnsx.log",
                    timeout=self.timer.cap(25, wave_deadline),
                    read_stdout=False,
                )
                for row in hu.read_jsonl(dns_out):
                    h = str(row.get("host") or "").strip().lower()
                    if h:
                        live_subs.append(h)
                        self.add_url(f"https://{h}/", "dnsx")
                _ = rc2
            else:
                live_subs = subs[:100]
            live_subs = sorted(set(live_subs))
            (self.target_dir / "subdomains_live.txt").write_text("\n".join(live_subs) + ("\n" if live_subs else ""), encoding="utf-8")
            (self.target_dir / "subdomains_urls.txt").write_text(
                "\n".join(f"https://{h}/" for h in live_subs) + ("\n" if live_subs else ""),
                encoding="utf-8",
            )
            self.record_status("subfinder+dnsx", rc, time.monotonic() - t0, f"{len(subs)} subs, {len(live_subs)} live")

        if self.enabled("enable_wellknown_ai_probes") and not self.timer.stopped():
            wt0 = time.monotonic()
            probe_rows: list[dict[str, Any]] = []
            origin = f"{urlparse(self.base_url).scheme}://{urlparse(self.base_url).netloc}"
            for path in hu.WELLKNOWN_AI_PATHS:
                if time.monotonic() >= wave_deadline or self.timer.stopped():
                    break
                url = origin + path
                code, _hdrs, body = self._http_get(url, timeout=6)
                text = body.decode("utf-8", "replace") if body else ""
                probe_rows.append({"url": url, "status_code": code, "bytes": len(body)})
                if code == 200 and text:
                    self.add_url(url, "wellknown_200")
                    if "robots.txt" in path:
                        for line in text.splitlines():
                            m = re.match(r"^(?:Allow|Disallow|Sitemap):\s*(\S+)", line.strip(), re.I)
                            if m:
                                self.add_url(m.group(1), "robots_txt")
                    elif "sitemap" in path:
                        for loc in re.findall(r"<loc>([^<]+)</loc>", text, re.I):
                            self.add_url(loc.strip(), "sitemap")
                    elif path.endswith(".json") or "discovery" in path:
                        for m in re.findall(r"\"(/[A-Za-z0-9_./-]{2,140})\"", text):
                            self.add_url(m, "wellknown_json")
                        for m in re.findall(r"https?://[^\s\"'<>]+", text):
                            self.add_url(m, "wellknown_json")
                elif code in hu.STATUS_EXISTS:
                    self.add_url(url, f"wellknown_{code}")
            hu.write_jsonl(self.target_dir / "wellknown_probes.jsonl", probe_rows)
            self.record_status("wellknown_ai", 0, time.monotonic() - wt0, f"{len(probe_rows)} paths checked")

        return live_subs

    def _step_scrapling(self, wave_deadline: float) -> None:
        if not self.enabled("enable_scrapling"):
            self.record_status("scrapling", 0, 0.0, "disabled")
            return
        t0 = time.monotonic()
        cap = self.timer.cap(self.settings.get("scrapling_timeout", 120), wave_deadline)
        max_pages = int(self.settings.get("scrapling_max_pages", 25))
        xhr_out = self.target_dir / "scrapling_xhr.jsonl"
        urls_out = self.target_dir / "scrapling_urls.txt"
        js_out = self.target_dir / "scrapling_js.txt"
        cookies_out = self.target_dir / "scrapling_cookies.json"

        helper_code = r'''
import json, re, sys, time
from urllib.parse import urljoin, urlparse

target = sys.argv[1]
max_pages = int(sys.argv[2])
deadline = time.monotonic() + max(15, int(sys.argv[3]) - 5)
xhr_path, urls_path, js_path, cookies_path = sys.argv[4:8]

discovered_urls = set()
discovered_js = set()
xhr_events = []
cookies_dict = {}
ua_str = ""

try:
    from scrapling.fetchers import StealthyFetcher, Fetcher
except Exception as exc:
    print(f"scrapling import failed: {exc}", file=sys.stderr)
    sys.exit(2)

origin = f"{urlparse(target).scheme}://{urlparse(target).netloc}"
visited = set()
queue = [target]

def record_link(raw, src):
    if not raw or raw.startswith(("data:", "javascript:", "mailto:")):
        return
    u = urljoin(target, raw.strip())
    if not u.startswith(("http://", "https://")):
        return
    discovered_urls.add(u)
    p = urlparse(u).path.lower()
    if p.endswith((".js", ".mjs", ".cjs", ".json", ".map")):
        discovered_js.add(u)
    elif urlparse(u).netloc == urlparse(target).netloc and u not in visited and len(visited) + len(queue) < max_pages * 3:
        if not any(p.endswith(ext) for ext in (".png", ".jpg", ".jpeg", ".svg", ".css", ".woff2", ".ico")):
            queue.append(u)

def extract_html(html_text):
    if not html_text:
        return
    for pat in (
        r'<script[^>]+src=["\']([^"\']+)["\']',
        r'<link[^>]+href=["\']([^"\']+)["\']',
        r'<a[^>]+href=["\']([^"\']+)["\']',
        r'["\'](/_next/static/[^"\']+)["\']',
        r'["\'](/assets/[^"\']+\.(?:js|mjs|json))["\']',
    ):
        for m in re.findall(pat, html_text, re.I):
            record_link(m, "html")

def setup_page(page):
    def on_req(req):
        try:
            rtype = getattr(req, "resource_type", "") or ""
            rurl = req.url
            if rtype in ("xhr", "fetch", "websocket", "script") or any(k in rurl.lower() for k in ("/api/", "graphql", ".js", ".json", ".map")):
                xhr_events.append({"method": req.method, "url": rurl, "resource_type": rtype})
            record_link(rurl, f"net_{rtype}")
        except Exception:
            pass
    def on_ws(ws):
        try:
            xhr_events.append({"method": "WS", "url": ws.url, "resource_type": "websocket"})
            discovered_urls.add(ws.url)
        except Exception:
            pass
    try:
        page.on("request", on_req)
        page.on("websocket", on_ws)
    except Exception:
        pass

while queue and len(visited) < max_pages and time.monotonic() < deadline:
    url = queue.pop(0)
    if url in visited:
        continue
    visited.add(url)
    page_resp = None
    try:
        if len(visited) == 1:
            page_resp = StealthyFetcher.fetch(
                url,
                headless=True,
                solve_cloudflare=True,
                network_idle=True,
                page_setup=setup_page,
                timeout=30000,
            )
        else:
            page_resp = Fetcher.get(url, timeout=12, stealthy_headers=True)
            if getattr(page_resp, "status", 0) in (403, 503):
                page_resp = StealthyFetcher.fetch(
                    url,
                    headless=True,
                    solve_cloudflare=True,
                    network_idle=True,
                    page_setup=setup_page,
                    timeout=25000,
                )
    except Exception as exc:
        print(f"fetch error {url}: {exc}", file=sys.stderr)
        continue

    if page_resp is None:
        continue
    try:
        c = getattr(page_resp, "cookies", None)
        if isinstance(c, dict):
            cookies_dict.update({str(k): str(v) for k, v in c.items()})
    except Exception:
        pass
    try:
        body = getattr(page_resp, "body", b"")
        text = body.decode("utf-8", "replace") if isinstance(body, (bytes, bytearray)) else str(getattr(page_resp, "text", "") or "")
        extract_html(text)
    except Exception:
        pass

with open(urls_path, "w", encoding="utf-8") as f:
    f.write("\n".join(sorted(discovered_urls)) + ("\n" if discovered_urls else ""))
with open(js_path, "w", encoding="utf-8") as f:
    f.write("\n".join(sorted(discovered_js)) + ("\n" if discovered_js else ""))
with open(xhr_path, "w", encoding="utf-8") as f:
    for ev in xhr_events:
        f.write(json.dumps(ev) + "\n")
with open(cookies_path, "w", encoding="utf-8") as f:
    json.dump({"cookies": cookies_dict, "user_agent": ua_str}, f)
'''
        rc, _ = self._run_cmd(
            [sys.executable, "-c", helper_code, self.base_url, str(max_pages), str(cap),
             str(xhr_out), str(urls_out), str(js_out), str(cookies_out)],
            self.logs_dir / "scrapling.log",
            timeout=cap,
            read_stdout=False,
        )

        if cookies_out.is_file():
            try:
                cdata = json.loads(cookies_out.read_text(encoding="utf-8"))
                self.scrapling_cookies = cdata.get("cookies") or {}
                if cdata.get("user_agent"):
                    self.scrapling_ua = cdata["user_agent"]
            except Exception:  # noqa: BLE001
                pass

        cnt_u = 0
        for fpath, src_name in ((urls_out, "scrapling"), (js_out, "scrapling_js")):
            if fpath.is_file():
                for line in fpath.read_text(encoding="utf-8", errors="replace").splitlines():
                    if line.strip():
                        self.add_url(line.strip(), src_name)
                        cnt_u += 1
        for row in hu.read_jsonl(xhr_out):
            if row.get("url"):
                self.add_url(str(row["url"]), "scrapling_xhr", str(row.get("method") or "GET"))
        self.record_status("scrapling", rc, time.monotonic() - t0, f"{cnt_u} URLs/JS captured")

    def _find_headless_shell(self) -> str | None:
        if hu.which("chrome-headless-shell"):
            return hu.which("chrome-headless-shell")
        cache_dir = Path.home() / ".cache" / "chrome-headless-shell"
        if cache_dir.exists():
            for p in cache_dir.rglob("chrome-headless-shell"):
                if p.is_file() and os.access(p, os.X_OK):
                    return str(p)
        return None

    def _ingest_katana_jsonl(self, path: Path, source: str) -> int:
        cnt = 0
        for row in hu.read_jsonl(path):
            req = row.get("request") or {}
            u = req.get("endpoint") or row.get("url")
            m = req.get("method") or "GET"
            if isinstance(u, str) and u:
                self.add_url(u, source, str(m))
                cnt += 1
        return cnt

    def _step_katana(self, wave_deadline: float) -> None:
        if not self.enabled("enable_katana") or not hu.which("katana") or self.timer.stopped():
            self.record_status("katana", 0, 0.0, "disabled or missing")
            return
        t0 = time.monotonic()
        kat_dir = self.target_dir / "katana"
        kat_dir.mkdir(parents=True, exist_ok=True)
        total_cap = self.timer.cap(self.settings.get("katana_timeout", 180), wave_deadline)
        pass1_deadline = min(wave_deadline, time.monotonic() + max(30, total_cap * 0.55))

        depth = str(self.settings.get("katana_depth", 3))
        mrs = str(self.settings.get("katana_max_response", 2097152))
        conc = str(self.settings.get("katana_concurrency", 12))
        par = str(self.settings.get("katana_parallelism", 6))
        p1_out = kat_dir / "pass1.jsonl"
        p1_cmd = [
            "katana", "-u", self.base_url, "-d", depth, "-kf", "all",
            "-c", conc, "-p", par, "-fs", "fqdn", "-mrs", mrs,
            "-filter-similar", "-fst", "8", "-j", "-o", str(p1_out), "-silent",
        ]
        if self.settings.get("katana_use_jsl", True):
            p1_cmd.append("-jsl")

        rc1, _ = self._run_cmd(
            p1_cmd,
            self.logs_dir / "katana_pass1.log",
            timeout=self.timer.cap(95, pass1_deadline),
            read_stdout=False,
        )
        if rc1 != 0 and not p1_out.is_file() and not self.timer.stopped():
            fallback = [x for x in p1_cmd if x not in ("-filter-similar", "-fst", "8")]
            rc1, _ = self._run_cmd(
                fallback,
                self.logs_dir / "katana_pass1.log",
                timeout=self.timer.cap(75, pass1_deadline),
                read_stdout=False,
            )
        cnt1 = self._ingest_katana_jsonl(p1_out, "katana_p1")

        cnt2 = 0
        rc2 = 0
        rem = self.timer.cap(85, wave_deadline)
        if rem >= 15 and self.settings.get("katana_use_headless_shell", True) and not self.timer.stopped():
            p2_out = kat_dir / "pass2.jsonl"
            shell_path = self._find_headless_shell()
            p2_cmd = [
                "katana", "-u", self.base_url, "-d", "2", "-headless",
                "-ho", "--no-sandbox,--disable-gpu", "-xhr", "-kf", "all",
                "-c", "6", "-p", "3", "-fs", "fqdn", "-mrs", mrs,
                "-filter-similar", "-fst", "8", "-j", "-o", str(p2_out), "-silent",
            ]
            if shell_path:
                p2_cmd.append("-sc")
            if self.settings.get("katana_use_jsl", True):
                p2_cmd.append("-jsl")
            rc2, _ = self._run_cmd(
                p2_cmd,
                self.logs_dir / "katana_pass2.log",
                timeout=rem,
                read_stdout=False,
            )
            if rc2 != 0 and not p2_out.is_file() and not self.timer.stopped():
                fallback2 = [x for x in p2_cmd if x not in ("-filter-similar", "-fst", "8", "-sc")]
                rc2, _ = self._run_cmd(
                    fallback2,
                    self.logs_dir / "katana_pass2.log",
                    timeout=self.timer.cap(55, wave_deadline),
                    read_stdout=False,
                )
            cnt2 = self._ingest_katana_jsonl(p2_out, "katana_p2")

        self.record_status("katana", rc1 or rc2, time.monotonic() - t0, f"p1={cnt1}, p2={cnt2}")

    def _ingest_url_file_stream(self, path: Path, source: str, limit: int) -> int:
        if not path.is_file():
            return 0
        cnt = 0
        with path.open("r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                s = line.strip()
                if not s:
                    continue
                if hu.is_asset(s) and not hu.is_js_or_map_url(s):
                    continue
                self.add_url(s, source)
                cnt += 1
                if cnt >= limit:
                    break
        return cnt

    def _step_archive(self, wave_deadline: float) -> None:
        max_archive = int(self.settings.get("max_archive_urls", 50000))
        if self.enabled("enable_waymore") and hu.which("waymore") and not self.timer.stopped():
            t0 = time.monotonic()
            wm_out = self.target_dir / "waymore_urls.txt"
            cap_u = self.timer.cap(min(85, int(self.settings.get("waymore_timeout", 140) * 0.65)), wave_deadline)
            rc, _ = self._run_cmd(
                ["waymore", "-i", self.subfinder_domain, "-mode", "U", "-oU", str(wm_out), "-nlf"],
                self.logs_dir / "waymore.log",
                timeout=cap_u,
                read_stdout=False,
            )
            cnt = self._ingest_url_file_stream(wm_out, "waymore", max_archive)

            rem = self.timer.cap(45, wave_deadline)
            if rem >= 15 and not self.timer.stopped():
                resp_dir = self.target_dir / "waymore_responses"
                resp_dir.mkdir(parents=True, exist_ok=True)
                self._run_cmd(
                    ["waymore", "-i", self.subfinder_domain, "-mode", "R", "-oR", str(resp_dir),
                     "-ko", r"\.(js|mjs|json|map)(\?|$)", "-l", "60"],
                    self.logs_dir / "waymore_resp.log",
                    timeout=rem,
                    read_stdout=False,
                )
            self.record_status("waymore", rc, time.monotonic() - t0, f"{cnt} archive URLs")

        if self.enabled("enable_urlfinder") and hu.which("urlfinder") and not self.timer.stopped():
            t0 = time.monotonic()
            uf_out = self.target_dir / "urlfinder_raw.txt"
            max_min = max(1, int(self.settings.get("urlfinder_max_time_min", 2)))
            cap = self.timer.cap(max_min * 60 + 15, wave_deadline)
            rc, _ = self._run_cmd(
                ["urlfinder", "-d", self.subfinder_domain, "-all", "-max-time", str(max_min), "-v", "-o", str(uf_out)],
                self.logs_dir / "urlfinder.log",
                timeout=cap,
                read_stdout=False,
            )
            cnt = self._ingest_url_file_stream(uf_out, "urlfinder", max_archive)
            self.record_status("urlfinder", rc, time.monotonic() - t0, f"{cnt} URLs")

    # ------------------------------------------------------------------
    # WAVE 2: Chunk Download & SHA-256 Dedup
    # ------------------------------------------------------------------
    def step_download_js(self, wave_deadline: float) -> list[Path]:
        t0 = time.monotonic()
        chunks_dir = self.target_dir / "chunks_unique"
        chunks_dir.mkdir(parents=True, exist_ok=True)
        manifest_rows: list[dict[str, Any]] = []
        seen_hashes: dict[str, Path] = {}
        downloaded_urls: set[str] = set()

        # Seed HTML script/modulepreload tags from base URL
        code, _hdrs, body = self._http_get(self.base_url, timeout=8)
        if code == 200 and body:
            html = body.decode("utf-8", "replace")
            for pat in (SCRIPT_SRC_RE, LINK_MODULE_RE):
                for m in pat.findall(html):
                    self.add_url(m, "base_html")

        # Ingest any archived JS/JSON snapshots from waymore -mode R
        wm_resp = self.target_dir / "waymore_responses"
        if wm_resp.exists():
            for p in wm_resp.rglob("*"):
                if p.is_file() and p.suffix.lower() in (".js", ".mjs", ".json", ".map"):
                    data = p.read_bytes()
                    if data:
                        digest = hu.sha256_bytes(data)
                        if digest not in seen_hashes:
                            dst = chunks_dir / f"{digest[:16]}_{hu.safe_filename(p.name)}"
                            dst.write_bytes(data)
                            seen_hashes[digest] = dst
                        manifest_rows.append({"url": f"waymore://{p.name}", "sha256": digest, "file": seen_hashes[digest].name, "bytes": len(data)})

        max_files = int(self.settings.get("max_js_files", 2500))
        rounds = int(self.settings.get("js_crawl_rounds", 3))
        threads = int(self.settings.get("js_download_threads", 32))
        dl_timeout = int(self.settings.get("js_download_timeout", 8))
        fallback_state = {"fails": 0}

        def fetch_one(u: str) -> tuple[str, int, bytes]:
            if time.monotonic() >= wave_deadline or self.timer.stopped():
                return u, 0, b""
            c, _h, b = self._http_get(u, timeout=dl_timeout)
            if c in (403, 503) and fallback_state["fails"] < 5 and not self.timer.stopped():
                try:
                    from scrapling.fetchers import Fetcher  # type: ignore[import-not-found]
                    resp = Fetcher.get(u, timeout=dl_timeout, stealthy_headers=True)
                    sc = int(getattr(resp, "status", 0) or 0)
                    body = getattr(resp, "body", b"")
                    if sc == 200 and body:
                        return u, sc, body if isinstance(body, (bytes, bytearray)) else str(body).encode("utf-8", "replace")
                    fallback_state["fails"] += 1
                except Exception:  # noqa: BLE001
                    fallback_state["fails"] += 1
            return u, c, b

        for rnd in range(rounds):
            if time.monotonic() >= wave_deadline or self.timer.stopped() or len(downloaded_urls) >= max_files:
                break
            with self._lock:
                pending = [u for u in sorted(self.js_urls) if u not in downloaded_urls][:max_files - len(downloaded_urls)]
            if not pending:
                break
            newly_found: set[str] = set()
            pool = ThreadPoolExecutor(max_workers=threads)
            try:
                futs = [pool.submit(fetch_one, u) for u in pending]
                rem_wait = max(1.0, wave_deadline - time.monotonic())
                try:
                    for fut in as_completed(futs, timeout=rem_wait):
                        if time.monotonic() >= wave_deadline or self.timer.stopped():
                            break
                        u, c, b = fut.result()
                        downloaded_urls.add(u)
                        if c != 200 or not b:
                            continue
                        digest = hu.sha256_bytes(b)
                        name_part = Path(urlparse(u).path).name or f"chunk_{rnd}.js"
                        if not any(name_part.lower().endswith(e) for e in hu.JS_OR_DATA_EXT):
                            name_part += ".js"
                        if digest not in seen_hashes:
                            dst = chunks_dir / f"{digest[:16]}_{hu.safe_filename(name_part)}"
                            dst.write_bytes(b)
                            seen_hashes[digest] = dst
                        manifest_rows.append({"url": u, "sha256": digest, "file": seen_hashes[digest].name, "bytes": len(b), "round": rnd + 1})

                        text = b.decode("utf-8", "replace")
                        for m in SOURCEMAP_COMMENT_RE.findall(text):
                            if not m.startswith("data:"):
                                map_u = hu.normalize_url(urljoin(u, m), u)
                                if map_u:
                                    newly_found.add(map_u)
                        for m in JS_REF_RE.findall(text):
                            ref_u = hu.normalize_url(m, u)
                            if ref_u and hu.is_first_party(ref_u, self.exact_host, self.scope_apex) and hu.is_js_or_map_url(ref_u):
                                newly_found.add(ref_u)
                except (TimeoutError, FuturesTimeoutError):
                    pass
            finally:
                try:
                    pool.shutdown(wait=False, cancel_futures=True)
                except TypeError:
                    pool.shutdown(wait=False)
            for nu in newly_found:
                self.add_url(nu, f"chunk_round{rnd + 1}")

        (self.target_dir / "js_urls.txt").write_text("\n".join(sorted(self.js_urls)) + ("\n" if self.js_urls else ""), encoding="utf-8")
        hu.write_jsonl(self.target_dir / "chunk_manifest.jsonl", manifest_rows)
        unique_files = sorted(chunks_dir.iterdir())
        self.record_status("chunk_download", 0, time.monotonic() - t0, f"{len(downloaded_urls)} fetched -> {len(unique_files)} unique SHA-256 chunks")
        return unique_files

    # ------------------------------------------------------------------
    # WAVE 3: Offline Parallel Analysis
    # ------------------------------------------------------------------
    def _step_jsluice(self, js_files: list[Path], wave_deadline: float) -> None:
        if not self.enabled("enable_jsluice") or not hu.which("jsluice") or not js_files or self.timer.stopped():
            return
        t0 = time.monotonic()
        batch = int(self.settings.get("jsluice_batch", 100))
        out_urls = self.target_dir / "jsluice.jsonl"
        out_secs = self.target_dir / "jsluice_secrets.jsonl"
        url_buf: list[str] = []
        sec_buf: list[str] = []

        for i in range(0, len(js_files), batch):
            if time.monotonic() >= wave_deadline or self.timer.stopped():
                break
            group = [str(p) for p in js_files[i:i + batch]]
            cap = self.timer.cap(40, wave_deadline)
            _, u_stdout = self._run_cmd(["jsluice", "urls", *group], self.logs_dir / "jsluice.log", timeout=cap)
            if u_stdout:
                url_buf.append(u_stdout)
            if time.monotonic() >= wave_deadline or self.timer.stopped():
                break
            cap = self.timer.cap(40, wave_deadline)
            _, s_stdout = self._run_cmd(["jsluice", "secrets", *group], self.logs_dir / "jsluice.log", timeout=cap)
            if s_stdout:
                sec_buf.append(s_stdout)

        out_urls.write_text("".join(url_buf), encoding="utf-8")
        out_secs.write_text("".join(sec_buf), encoding="utf-8")
        cnt = 0
        for row in hu.read_jsonl(out_urls):
            if row.get("url"):
                self.add_url(str(row["url"]), "jsluice", str(row.get("method") or "GET"))
                cnt += 1
        self.record_status("jsluice", 0, time.monotonic() - t0, f"{len(js_files)} chunks -> {cnt} URLs")

    def _step_xnlinkfinder(self, chunks_dir: Path, wave_deadline: float) -> None:
        if not self.enabled("enable_xnlinkfinder") or not hu.which("xnLinkFinder") or self.timer.stopped():
            return
        if not any(chunks_dir.iterdir()):
            return
        t0 = time.monotonic()
        ep_out = self.target_dir / "xnlinkfinder_endpoints.txt"
        params_out = self.target_dir / "xn_params.txt"
        sec_out = self.target_dir / "xn_secrets.json"
        cap = self.timer.cap(80, wave_deadline)
        rc, stdout = self._run_cmd(
            ["xnLinkFinder", "-i", str(chunks_dir), "-sf", self.scope_apex,
             "-o", "cli", "-op", str(params_out), "-os", str(sec_out)],
            self.logs_dir / "xnlinkfinder.log",
            timeout=cap,
        )
        ep_lines = [l.strip() for l in stdout.splitlines() if l.strip() and not l.startswith("[")]
        ep_out.write_text("\n".join(sorted(set(ep_lines))) + ("\n" if ep_lines else ""), encoding="utf-8")
        for ep in ep_lines:
            self.add_url(ep, "xnLinkFinder")
        self.record_status("xnLinkFinder", rc, time.monotonic() - t0, f"{len(ep_lines)} endpoints")

    def _step_sourcemapper(self, chunks_dir: Path, wave_deadline: float) -> list[str]:
        if not self.enabled("enable_sourcemapper") or self.timer.stopped():
            return []
        t0 = time.monotonic()
        smap_dir = self.target_dir / "sourcemaps"
        smap_dir.mkdir(parents=True, exist_ok=True)

        # 1. Decode inline base64 sourceMappingURL comments directly
        for js_file in chunks_dir.glob("*.js"):
            if time.monotonic() >= wave_deadline or self.timer.stopped():
                break
            try:
                text = js_file.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for idx, m in enumerate(re.findall(r"//#\s*sourceMappingURL=data:application/json[^,]*,([^\s]+)", text)):
                try:
                    raw_map = json.loads(base64.b64decode(m).decode("utf-8", "replace"))
                    sources = raw_map.get("sources") or []
                    contents = raw_map.get("sourcesContent") or []
                    for s_idx, src_name in enumerate(sources):
                        if s_idx < len(contents) and isinstance(contents[s_idx], str):
                            rel = re.sub(r"^(\.\./)+|^/+", "", str(src_name)).replace("..", "_")
                            dst = smap_dir / f"inline_{js_file.stem}_{idx}" / rel
                            dst.parent.mkdir(parents=True, exist_ok=True)
                            dst.write_text(contents[s_idx], encoding="utf-8")
                except Exception:  # noqa: BLE001
                    continue

        # 2. Unpack downloaded .map files with sourcemapper CLI
        map_files = list(chunks_dir.glob("*.map"))
        if map_files and hu.which("sourcemapper"):
            for mf in map_files[:40]:
                if time.monotonic() >= wave_deadline or self.timer.stopped():
                    break
                out_sub = smap_dir / mf.stem
                self._run_cmd(
                    ["sourcemapper", "-url", str(mf), "-output", str(out_sub)],
                    self.logs_dir / "sourcemapper.log",
                    timeout=self.timer.cap(20, wave_deadline),
                    read_stdout=False,
                )

        unpacked = sorted(str(p.relative_to(smap_dir)) for p in smap_dir.rglob("*") if p.is_file())
        (self.target_dir / "sourcemap_files.txt").write_text("\n".join(unpacked) + ("\n" if unpacked else ""), encoding="utf-8")
        self.record_status("sourcemapper", 0, time.monotonic() - t0, f"{len(map_files)} maps -> {len(unpacked)} unpacked sources")
        return unpacked

    def _step_jscope(self, js_files: list[Path], wave_deadline: float) -> list[dict[str, Any]]:
        t0 = time.monotonic()
        max_bytes = int(self.settings.get("jscope_max_file_bytes", 3145728))
        rec_limit = int(self.settings.get("jscope_recursion_limit", 10000))
        findings: list[dict[str, Any]] = []
        seen_fg: set[tuple[str, str]] = set()

        def add_finding(kind: str, name: str, file_name: str) -> None:
            key = (kind, name)
            if key not in seen_fg:
                seen_fg.add(key)
                findings.append({"kind": kind, "name": name, "file": file_name})

        # Stage JS files <= 3MB using symlinks so Jscope skips oversized vendor bundles without copying
        stage_dir = self.target_dir / "jscope_stage"
        stage_dir.mkdir(parents=True, exist_ok=True)
        staged: list[Path] = []
        for p in js_files:
            try:
                if p.stat().st_size <= max_bytes:
                    link = stage_dir / p.name
                    if not link.exists():
                        try:
                            os.symlink(p.resolve(), link)
                        except OSError:
                            link.write_bytes(p.read_bytes())
                    staged.append(link)
            except OSError:
                continue

        jscope_raw = self.target_dir / "jscope.txt"
        rc = 0
        jscope_bin = hu.which("jscope")
        if self.enabled("enable_jscope") and jscope_bin and staged and not self.timer.stopped():
            wrapper = (
                "import runpy, sys\n"
                f"sys.setrecursionlimit({rec_limit})\n"
                "target_bin, target_dir = sys.argv[1], sys.argv[2]\n"
                "sys.argv = [target_bin, 'analyze', target_dir, '--verbose']\n"
                "runpy.run_path(target_bin, run_name='__main__')\n"
            )
            cap = self.timer.cap(55, wave_deadline)
            rc, stdout = self._run_cmd(
                [sys.executable, "-c", wrapper, jscope_bin, str(stage_dir)],
                self.logs_dir / "jscope.log",
                timeout=cap,
                stdout_path=jscope_raw,
            )
            for line in stdout.splitlines():
                for kind in ("feature_flag", "role", "route_guard"):
                    m = re.search(rf"{kind}:([A-Za-z0-9_.:-]+)", line)
                    if m:
                        add_finding(kind, m.group(1), "jscope")

        # Fast deterministic backup scan over chunks + unpacked sourcemaps (deadline-guarded)
        scan_dirs = [self.target_dir / "chunks_unique", self.target_dir / "sourcemaps"]
        for sdir in scan_dirs:
            if not sdir.exists() or time.monotonic() >= wave_deadline or self.timer.stopped():
                continue
            for p in sdir.rglob("*"):
                if time.monotonic() >= wave_deadline or self.timer.stopped():
                    break
                if not p.is_file() or p.suffix.lower() not in (".js", ".mjs", ".ts", ".tsx", ".jsx", ".json"):
                    continue
                if p.stat().st_size > max_bytes:
                    continue
                txt = p.read_text(encoding="utf-8", errors="replace")
                for m in FEATURE_FLAG_RE.findall(txt):
                    add_finding("flag_or_role", m, p.name)
                for m in MODEL_CANDIDATE_RE.findall(txt):
                    add_finding("model_candidate", m, p.name)

        (self.target_dir / "jscope_findings.json").write_text(json.dumps(findings, indent=2) + "\n", encoding="utf-8")
        self.record_status("jscope", rc, time.monotonic() - t0, f"{len(staged)} files -> {len(findings)} flags/models")
        return findings

    def _step_secrets_offline(self, wave_deadline: float) -> list[dict[str, Any]]:
        t0 = time.monotonic()
        scan_targets = [p for p in (self.target_dir / "chunks_unique", self.target_dir / "sourcemaps") if p.exists() and any(p.rglob("*"))]
        normalized: list[dict[str, Any]] = []
        if not scan_targets or self.timer.stopped():
            hu.write_jsonl(self.target_dir / "secrets.jsonl", [])
            return normalized

        if self.enabled("enable_trufflehog") and hu.which("trufflehog") and not self.timer.stopped():
            th_out = self.target_dir / "trufflehog.jsonl"
            all_th: list[str] = []
            for st in scan_targets:
                if time.monotonic() >= wave_deadline or self.timer.stopped():
                    break
                _, out = self._run_cmd(
                    ["trufflehog", "filesystem", str(st), "--json", "--no-update"],
                    self.logs_dir / "trufflehog.log",
                    timeout=self.timer.cap(55, wave_deadline),
                )
                if out:
                    all_th.append(out)
            th_out.write_text("".join(all_th), encoding="utf-8")
            for row in hu.read_jsonl(th_out):
                normalized.append({
                    "source": "trufflehog",
                    "detector": row.get("DetectorName", "unknown"),
                    "verified": bool(row.get("Verified", False)),
                    "raw": row.get("Raw", ""),
                    "file": ((row.get("SourceMetadata") or {}).get("Data") or {}).get("Filesystem", {}).get("file", ""),
                })

        if self.enabled("enable_titus") and hu.which("titus") and not self.timer.stopped():
            ti_out = self.target_dir / "titus.json"
            for idx, st in enumerate(scan_targets):
                if time.monotonic() >= wave_deadline or self.timer.stopped():
                    break
                sub_out = self.target_dir / f"titus_{idx}.json"
                self._run_cmd(
                    ["titus", "scan", str(st), "--format", "json", "--output", str(sub_out)],
                    self.logs_dir / "titus.log",
                    timeout=self.timer.cap(55, wave_deadline),
                    read_stdout=False,
                )
                if sub_out.is_file():
                    try:
                        data = json.loads(sub_out.read_text(encoding="utf-8", errors="replace"))
                        items = data if isinstance(data, list) else data.get("findings", data.get("matches", []))
                        for item in items or []:
                            if isinstance(item, dict):
                                normalized.append({
                                    "source": "titus",
                                    "detector": item.get("rule_name") or item.get("rule") or "titus",
                                    "verified": bool(item.get("verified", False)),
                                    "raw": item.get("match") or item.get("secret") or "",
                                    "file": item.get("path") or item.get("file") or "",
                                })
                    except json.JSONDecodeError:
                        for row in hu.read_jsonl(sub_out):
                            normalized.append({
                                "source": "titus",
                                "detector": row.get("rule_name") or row.get("rule") or "titus",
                                "verified": bool(row.get("verified", False)),
                                "raw": row.get("match") or row.get("secret") or "",
                                "file": row.get("path") or row.get("file") or "",
                            })
            if (self.target_dir / "titus_0.json").is_file() and not ti_out.is_file():
                ti_out.write_text((self.target_dir / "titus_0.json").read_text(encoding="utf-8", errors="replace"), encoding="utf-8")

        for row in hu.read_jsonl(self.target_dir / "jsluice_secrets.jsonl"):
            normalized.append({
                "source": "jsluice",
                "detector": row.get("kind", "jsluice"),
                "verified": False,
                "raw": str(row.get("data") or ""),
                "file": row.get("filename", ""),
            })

        xn_sec = self.target_dir / "xn_secrets.json"
        if xn_sec.is_file():
            try:
                xdata = json.loads(xn_sec.read_text(encoding="utf-8", errors="replace"))
                if isinstance(xdata, dict):
                    for det, vals in xdata.items():
                        if isinstance(vals, dict):
                            for secret_val, locs in vals.items():
                                normalized.append({
                                    "source": "xnLinkFinder",
                                    "detector": det,
                                    "verified": False,
                                    "raw": str(secret_val),
                                    "file": str((locs or [""])[0]) if isinstance(locs, list) else "",
                                })
            except Exception:  # noqa: BLE001
                pass

        hu.write_jsonl(self.target_dir / "secrets.jsonl", normalized)
        self.record_status("secrets_offline", 0, time.monotonic() - t0, f"{len(normalized)} candidates")
        return normalized

    # ------------------------------------------------------------------
    # WAVE 4: Live Probe, Targeted Fuzz & AI Feed
    # ------------------------------------------------------------------
    def _step_probe(self, wave_deadline: float) -> list[dict[str, Any]]:
        raw_urls = sorted(self.routes.keys())
        (self.target_dir / "raw_collected.txt").write_text("\n".join(raw_urls) + ("\n" if raw_urls else ""), encoding="utf-8")
        if self.timer.stopped():
            return []

        probe_candidates = [u for u in raw_urls if self.settings.get("probe_assets") or not hu.is_asset(u)]
        cap_max = int(self.settings.get("max_urls", 0) or 0)
        if cap_max > 0:
            probe_candidates = hu.prioritize_probe_urls(self.routes, probe_candidates, cap_max)
        elif len(probe_candidates) > 15000:
            probe_candidates = hu.prioritize_probe_urls(self.routes, probe_candidates, 15000)

        to_probe = self.target_dir / "urls_to_probe.txt"
        to_probe.write_text("\n".join(probe_candidates) + ("\n" if probe_candidates else ""), encoding="utf-8")

        deduped = probe_candidates
        if self.enabled("enable_uro") and hu.which("uro") and probe_candidates and not self.timer.stopped():
            uro_out = self.target_dir / "urls_to_probe_uro.txt"
            rc, _ = self._run_cmd(
                ["uro", "-i", str(to_probe)],
                self.logs_dir / "uro.log",
                timeout=self.timer.cap(25, wave_deadline),
                stdout_path=uro_out,
                read_stdout=False,
            )
            if rc == 0 and uro_out.is_file() and uro_out.stat().st_size > 0:
                deduped = [l.strip() for l in uro_out.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()]

        max_probe = int(self.settings.get("max_probe_urls", 3000) or 3000)
        prioritized = hu.prioritize_probe_urls(self.routes, deduped, max_probe)
        final_list = self.target_dir / "urls_to_probe_prioritized.txt"
        final_list.write_text("\n".join(prioritized) + ("\n" if prioritized else ""), encoding="utf-8")

        probe_out = self.target_dir / "probe.jsonl"
        if not self.enabled("enable_httpx") or not hu.which("httpx") or not prioritized or self.timer.stopped():
            return []

        t0 = time.monotonic()
        cap = self.timer.cap(self.settings.get("httpx_timeout", 75), wave_deadline)
        rc, _ = self._run_cmd(
            [
                "httpx", "-l", str(final_list), "-mc", hu.ALL_CODES,
                "-sc", "-cl", "-ct", "-title", "-td", "-j",
                "-o", str(probe_out), "-silent",
                "-timeout", str(self.settings.get("request_timeout", 8)), "-retries", "1",
                "-rl", str(self.settings.get("httpx_rate", 150)),
                "-threads", str(self.settings.get("httpx_threads", 80)),
            ],
            self.logs_dir / "httpx.log",
            timeout=cap,
            read_stdout=False,
        )
        rows = hu.read_jsonl(probe_out)
        self.record_status("httpx", rc, time.monotonic() - t0, f"{len(rows)}/{len(prioritized)} probed")
        return rows

    def _step_vhost(self, live_subs: list[str], wave_deadline: float) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        if not self.enabled("enable_vhost") or not live_subs or self.timer.stopped():
            return [], []
        t0 = time.monotonic()
        all_rows: list[dict[str, Any]] = []
        origin = f"{urlparse(self.base_url).scheme}://{urlparse(self.base_url).netloc}"
        for sub in live_subs[:30]:
            if time.monotonic() >= wave_deadline or self.timer.stopped():
                break
            code, _h, body = self._http_get(origin, timeout=4, headers={"Host": sub})
            title = ""
            if body:
                m = re.search(r"<title[^>]*>(.*?)</title>", body.decode("utf-8", "replace"), re.I | re.S)
                title = m.group(1).strip()[:80] if m else ""
            all_rows.append({"host": sub, "status_code": code, "title": title})

        hu.write_jsonl(self.target_dir / "vhost.jsonl", all_rows)
        real = [r for r in all_rows if r.get("status_code") in (hu.VHOST_REAL - {403})]
        blocked = [r for r in all_rows if r not in real]
        hu.write_jsonl(self.target_dir / "vhost_real.jsonl", real)
        hu.write_jsonl(self.target_dir / "vhost_blocked.jsonl", blocked)
        self.record_status("vhost", 0, time.monotonic() - t0, f"{len(real)} real / {len(all_rows)} tested")
        return real, blocked

    def _step_targeted_fuzz(self, win_rows: list[dict[str, Any]], wordlist_path: Path, cf_blocked: bool, wave_deadline: float) -> list[dict[str, Any]]:
        if not self.enabled("enable_targeted_fuzz") or cf_blocked or not wordlist_path.is_file() or self.timer.stopped():
            return []
        t0 = time.monotonic()
        prefixes: list[str] = []
        seen_p: set[str] = set()
        max_p = int(self.settings.get("fuzz_prefixes_max", 8))

        for r in win_rows:
            u = str(r.get("url") or "")
            p = urlparse(u)
            if any(seg in p.path.lower() for seg in ("/api", "/v1", "/v2", "/internal", "/data", "/admin")):
                prefix = f"{p.scheme}://{p.netloc}/" + "/".join([s for s in p.path.split("/") if s][:2])
                if prefix not in seen_p:
                    seen_p.add(prefix)
                    prefixes.append(prefix)
        if not prefixes:
            prefixes = [self.base_url.rstrip("/")]
        prefixes = prefixes[:max_p]

        fuzz_rows: list[dict[str, Any]] = []
        fuzz_out = self.target_dir / "fuzz.jsonl"
        total_cap = self.timer.cap(self.settings.get("fuzz_timeout", 65), wave_deadline)
        per_target = max(8, total_cap // max(1, len(prefixes)))

        if self.settings.get("fuzz_tool", "feroxbuster") == "feroxbuster" and hu.which("feroxbuster"):
            for idx, pref in enumerate(prefixes):
                if time.monotonic() >= wave_deadline or self.timer.stopped():
                    break
                tmp_out = self.target_dir / f"ferox_{idx}.json"
                self._run_cmd(
                    ["feroxbuster", "-u", pref, "-w", str(wordlist_path), "--silent", "--no-state",
                     "--depth", "1", "--time-limit", f"{per_target}s", "--json", "-o", str(tmp_out)],
                    self.logs_dir / "feroxbuster.log",
                    timeout=self.timer.cap(per_target + 5, wave_deadline),
                    read_stdout=False,
                )
                for row in hu.read_jsonl(tmp_out):
                    if row.get("type") == "response" and row.get("url"):
                        fuzz_rows.append({"url": row["url"], "status_code": row.get("status", 0), "sources": ["feroxbuster"]})
                        self.add_url(str(row["url"]), "feroxbuster")
        elif hu.which("ffuf"):
            for idx, pref in enumerate(prefixes):
                if time.monotonic() >= wave_deadline or self.timer.stopped():
                    break
                tmp_out = self.target_dir / f"ffuf_{idx}.json"
                self._run_cmd(
                    ["ffuf", "-u", pref.rstrip("/") + "/FUZZ", "-w", str(wordlist_path),
                     "-mc", "200,201,204,301,302,307,401,403,405", "-maxtime", str(per_target),
                     "-of", "json", "-o", str(tmp_out), "-s"],
                    self.logs_dir / "ffuf.log",
                    timeout=self.timer.cap(per_target + 5, wave_deadline),
                    read_stdout=False,
                )
                if tmp_out.is_file():
                    try:
                        data = json.loads(tmp_out.read_text(encoding="utf-8", errors="replace"))
                        for res in data.get("results", []):
                            if res.get("url"):
                                fuzz_rows.append({"url": res["url"], "status_code": res.get("status", 0), "sources": ["ffuf"]})
                                self.add_url(str(res["url"]), "ffuf")
                    except json.JSONDecodeError:
                        pass

        hu.write_jsonl(fuzz_out, fuzz_rows)
        self.record_status("targeted_fuzz", 0, time.monotonic() - t0, f"{len(prefixes)} prefixes -> {len(fuzz_rows)} hits")
        return fuzz_rows

    def _step_x8(self, win_rows: list[dict[str, Any]], param_file: Path, cf_blocked: bool, wave_deadline: float) -> None:
        if not self.enabled("enable_x8") or not hu.which("x8") or cf_blocked or self.timer.stopped():
            self.record_status("x8", 0, 0.0, "skipped (cf_blocked, stopped, or disabled)")
            return
        if not param_file.is_file() or param_file.stat().st_size == 0:
            self.record_status("x8", 0, 0.0, "no params")
            return
        t0 = time.monotonic()
        max_targets = int(self.settings.get("x8_max_api_targets", 8))
        api_urls = [
            str(r["url"]) for r in win_rows
            if r.get("url") and ("/api" in str(r["url"]).lower() or "json" in str(r.get("content_type") or "").lower())
        ][:max_targets]
        if not api_urls:
            self.record_status("x8", 0, 0.0, "no live /api/ targets")
            return
        cap = self.timer.cap(self.settings.get("x8_timeout", 45), wave_deadline)
        per_cap = max(8, cap // len(api_urls))
        out_buf: list[str] = []
        for u in api_urls:
            if time.monotonic() >= wave_deadline or self.timer.stopped():
                break
            _, out = self._run_cmd(
                ["x8", "-u", u, "-w", str(param_file)],
                self.logs_dir / "x8.log",
                timeout=self.timer.cap(per_cap, wave_deadline),
            )
            if out:
                out_buf.append(f"=== {u} ===\n{out}")
        (self.target_dir / "x8.txt").write_text("\n".join(out_buf), encoding="utf-8")
        self.record_status("x8", 0, time.monotonic() - t0, f"{len(api_urls)} API routes scanned")

    def _step_methods(self, candidate_rows: list[dict[str, Any]], cf_blocked: bool, wave_deadline: float) -> list[dict[str, Any]]:
        if not self.enabled("enable_methods") or cf_blocked or self.timer.stopped():
            return []
        t0 = time.monotonic()
        targets = [
            str(r["url"]) for r in candidate_rows
            if r.get("url") and (int(r.get("status_code") or 0) == 405 or "/api" in str(r["url"]).lower())
        ][:12]
        if not targets:
            return []
        rows: list[dict[str, Any]] = []
        ctx = ssl.create_default_context()
        for u in targets:
            if time.monotonic() >= wave_deadline or self.timer.stopped():
                break
            for meth in ("OPTIONS", "POST"):
                if time.monotonic() >= wave_deadline or self.timer.stopped():
                    break
                req = urllib.request.Request(u, headers={"User-Agent": self.scrapling_ua}, method=meth)
                try:
                    with urllib.request.urlopen(req, timeout=4, context=ctx) as resp:
                        rows.append({"url": u, "method": meth, "status_code": resp.status, "allow": resp.headers.get("Allow", "")})
                except urllib.error.HTTPError as err:
                    rows.append({"url": u, "method": meth, "status_code": err.code, "allow": err.headers.get("Allow", "") if err.headers else ""})
                except Exception:  # noqa: BLE001
                    continue
        self.record_status("methods", 0, time.monotonic() - t0, f"{len(rows)} probes")
        return rows

    def _find_nuclei_templates(self) -> Path | None:
        candidates = [
            Path.home() / "nuclei-templates",
            Path.home() / ".local" / "nuclei-templates",
            Path.home() / ".config" / "nuclei" / "nuclei-templates",
        ]
        for c in candidates:
            if c.is_dir() and any(c.iterdir()):
                return c
        return None

    def _step_nuclei(self, live_rows: list[dict[str, Any]], wave_deadline: float) -> list[dict[str, Any]]:
        if not self.enabled("enable_nuclei") or not hu.which("nuclei") or self.timer.stopped():
            return []
        t0 = time.monotonic()
        max_targets = int(self.settings.get("nuclei_max_targets", 150))
        urls = list({str(r["url"]): True for r in live_rows if r.get("url")})[:max_targets]
        if not urls:
            return []
        tpl_dir = self._find_nuclei_templates()
        if tpl_dir is None:
            self._run_cmd(
                ["nuclei", "-update-templates", "-silent"],
                self.logs_dir / "nuclei.log",
                timeout=self.timer.cap(30, wave_deadline),
                read_stdout=False,
            )
            tpl_dir = self._find_nuclei_templates()
        if tpl_dir is None:
            self.record_status("nuclei", 1, time.monotonic() - t0, "no templates found")
            return []

        nuc_list = self.target_dir / "nuclei_urls.txt"
        nuc_list.write_text("\n".join(urls) + "\n", encoding="utf-8")
        nuc_out = self.target_dir / "nuclei.jsonl"
        cap = self.timer.cap(self.settings.get("nuclei_timeout", 80), wave_deadline)
        rc, _ = self._run_cmd(
            [
                "nuclei", "-l", str(nuc_list), "-t", str(tpl_dir),
                "-tags", "exposure,misconfig,tech,panel",
                "-rl", "50", "-c", "25", "-jsonl", "-o", str(nuc_out),
                "-silent", "-duc", "-timeout", "8", "-retries", "1",
            ],
            self.logs_dir / "nuclei.log",
            timeout=cap,
            read_stdout=False,
        )
        rows = hu.read_jsonl(nuc_out)
        self.record_status("nuclei", rc, time.monotonic() - t0, f"{len(rows)} findings across {len(urls)} URLs")
        return rows

    def _run_pool_bounded(self, tasks: list[tuple[Any, tuple[Any, ...]]], deadline: float) -> list[Any]:
        pool = ThreadPoolExecutor(max_workers=len(tasks))
        results: list[Any] = [None] * len(tasks)
        try:
            futs = [pool.submit(fn, *args) for fn, args in tasks]
            rem = max(1.0, deadline - time.monotonic() + 3.0)
            wait(futs, timeout=rem)
            for idx, fut in enumerate(futs):
                if fut.done() and not fut.cancelled():
                    try:
                        results[idx] = fut.result(timeout=0)
                    except Exception as exc:  # noqa: BLE001
                        hu.log(f"worker error: {exc}")
        finally:
            try:
                pool.shutdown(wait=False, cancel_futures=True)
            except TypeError:
                pool.shutdown(wait=False)
        return results

    def _start_watchdog(self) -> threading.Event:
        done_ev = threading.Event()

        def watchdog() -> None:
            wait_sec = max(1.0, self.timer.work_deadline - time.monotonic())
            if not done_ev.wait(timeout=wait_sec):
                hu.log(f"Budget work_deadline reached ({self.timer.elapsed():.1f}s); stopping active tools to save results")
                self.timer.request_stop()
                hu.kill_all_active_procs()

        t = threading.Thread(target=watchdog, name="hunt-watchdog", daemon=True)
        t.start()
        return done_ev

    def run(self) -> int:
        wave_timings: dict[str, float] = {}
        done_ev = self._start_watchdog()

        live_subs: list[str] = []
        sourcemap_files: list[str] = []
        jscope_findings: list[dict[str, Any]] = []
        secrets: list[dict[str, Any]] = []
        probe_rows: list[dict[str, Any]] = []
        vhosts_real: list[dict[str, Any]] = []
        vhost_blocked: list[dict[str, Any]] = []
        win_rows: list[dict[str, Any]] = []
        blocked_rows: list[dict[str, Any]] = []
        other_rows: list[dict[str, Any]] = []
        probed_by_key: dict[str, dict[str, Any]] = {}
        method_rows: list[dict[str, Any]] = []
        nuclei_rows: list[dict[str, Any]] = []

        try:
            # WAVE 1: Parallel Discovery
            if not self.timer.stopped():
                w1_start = time.monotonic()
                w1_deadline = self.timer.wave_deadline(self.settings.get("wave1_budget_seconds", 200))
                hu.log(f"WAVE 1 starting for {self.base_url} (subfinder_domain={self.subfinder_domain})")
                w1_res = self._run_pool_bounded(
                    [
                        (self._step_subdomains_and_wellknown, (w1_deadline,)),
                        (self._step_scrapling, (w1_deadline,)),
                        (self._step_katana, (w1_deadline,)),
                        (self._step_archive, (w1_deadline,)),
                    ],
                    w1_deadline,
                )
                if isinstance(w1_res[0], list):
                    live_subs = w1_res[0]
                wave_timings["Wave 1 (Discovery)"] = time.monotonic() - w1_start

            # WAVE 2: Chunk Download & SHA-256 Dedup
            js_files: list[Path] = []
            if not self.timer.stopped():
                w2_start = time.monotonic()
                w2_deadline = self.timer.wave_deadline(self.settings.get("wave2_budget_seconds", 110))
                hu.log(f"WAVE 2 chunk download ({len(self.js_urls)} JS/JSON/map URLs)")
                unique_chunks = self.step_download_js(w2_deadline)
                js_files = [p for p in unique_chunks if p.suffix.lower() in (".js", ".mjs")]
                wave_timings["Wave 2 (Chunks)"] = time.monotonic() - w2_start
            else:
                chunks_dir_existing = self.target_dir / "chunks_unique"
                if chunks_dir_existing.exists():
                    unique_chunks = sorted(chunks_dir_existing.iterdir())
                    js_files = [p for p in unique_chunks if p.suffix.lower() in (".js", ".mjs")]
                else:
                    unique_chunks = []

            # WAVE 3: Offline Parallel Analysis
            if not self.timer.stopped() and unique_chunks:
                w3_start = time.monotonic()
                w3_deadline = self.timer.wave_deadline(self.settings.get("wave3_budget_seconds", 130))
                hu.log(f"WAVE 3 offline analysis on {len(unique_chunks)} unique chunks")
                chunks_dir = self.target_dir / "chunks_unique"
                w3_res = self._run_pool_bounded(
                    [
                        (self._step_jsluice, (js_files, w3_deadline)),
                        (self._step_xnlinkfinder, (chunks_dir, w3_deadline)),
                        (self._step_sourcemapper, (chunks_dir, w3_deadline)),
                        (self._step_jscope, (js_files, w3_deadline)),
                        (self._step_secrets_offline, (w3_deadline,)),
                    ],
                    w3_deadline,
                )
                if isinstance(w3_res[2], list):
                    sourcemap_files = w3_res[2]
                if isinstance(w3_res[3], list):
                    jscope_findings = w3_res[3]
                if isinstance(w3_res[4], list):
                    secrets = w3_res[4]
                wave_timings["Wave 3 (Offline AST/Secrets)"] = time.monotonic() - w3_start

            # WAVE 4: Live Verification, Targeted Fuzz, Exposure Check & AI Feed
            if not self.timer.stopped():
                w4_start = time.monotonic()
                w4_deadline = self.timer.wave_deadline(self.settings.get("wave4_budget_seconds", 175))
                hu.log(f"WAVE 4 live probe & AI feed ({len(self.routes)} first-party routes)")

                probe_rows = self._step_probe(w4_deadline)
                vhosts_real, vhost_blocked = self._step_vhost(live_subs, w4_deadline)

                wl_path = self.target_dir / "wordlist.txt"
                pf_path = self.target_dir / "params.txt"
                if not self.timer.stopped():
                    wordlist.build(
                        self.target_dir,
                        self.base_url,
                        self.settings.get("wordlist", "wordlists/common.txt"),
                        wl_path,
                        int(self.settings.get("wordlist_max", 6000)),
                        pf_path,
                    )

                probed_by_key = {hu.dedupe_key(str(r.get("url") or "")): r for r in probe_rows if r.get("url")}
                for r in probe_rows:
                    code = int(r.get("status_code") or 0)
                    if code in hu.STATUS_WIN:
                        win_rows.append(r)
                    elif code in hu.STATUS_EXISTS:
                        blocked_rows.append(r)
                    else:
                        other_rows.append(r)

                cf_count = sum(1 for r in probe_rows if hu.is_cloudflare_response(r))
                cf_blocked = bool(probe_rows) and len(win_rows) == 0 and cf_count >= max(1, len(probe_rows) // 2)

                fuzz_rows = self._step_targeted_fuzz(win_rows, wl_path, cf_blocked, w4_deadline)
                for fr in fuzz_rows:
                    if fr.get("status_code") in hu.STATUS_WIN:
                        win_rows.append(fr)
                    elif fr.get("status_code") in hu.STATUS_EXISTS:
                        blocked_rows.append(fr)

                self._step_x8(win_rows, pf_path, cf_blocked, w4_deadline)
                method_rows = self._step_methods(win_rows + blocked_rows, cf_blocked, w4_deadline)
                nuclei_rows = self._step_nuclei(win_rows + blocked_rows, w4_deadline)
                wave_timings["Wave 4 (Verify/Fuzz/Feed)"] = time.monotonic() - w4_start
        finally:
            done_ev.set()
            hu.kill_all_active_procs()

        # Always save all raw preserved artifacts + compact feed even if budget/SIGTERM hit
        all_routes = []
        with self._lock:
            routes_snapshot = sorted(self.routes.items())
            third_party_rows = sorted(self.third_party.values(), key=lambda x: x["url"])
        for k, entry in routes_snapshot:
            merged = dict(entry)
            if k in probed_by_key:
                merged["status_code"] = probed_by_key[k].get("status_code", 0)
                merged["title"] = probed_by_key[k].get("title", "")
            all_routes.append(merged)

        data_files = [r for r in all_routes if hu.is_data_file_url(r["url"])]
        params_rows = [r for r in all_routes if "?" in r["url"]]
        js_endpoints = [r for r in all_routes if any(s in ("jsluice", "xnLinkFinder", "scrapling_xhr") for s in r.get("sources", []))]
        sub_rows = [{"host": h} for h in live_subs]

        hu.write_jsonl(self.target_dir / "all_routes.jsonl", all_routes)
        hu.write_jsonl(self.target_dir / "accessible_200.jsonl", win_rows)
        hu.write_jsonl(self.target_dir / "exists_blocked.jsonl", blocked_rows)
        hu.write_jsonl(self.target_dir / "other_status.jsonl", other_rows)
        hu.write_jsonl(self.target_dir / "data_files.jsonl", data_files)
        hu.write_jsonl(self.target_dir / "params.jsonl", params_rows)
        hu.write_jsonl(self.target_dir / "subdomains.jsonl", sub_rows)
        hu.write_jsonl(self.target_dir / "js_endpoints.jsonl", js_endpoints)
        hu.write_jsonl(self.target_dir / "third_party_routes.jsonl", third_party_rows)
        hu.write_jsonl(self.target_dir / "method_responses.jsonl", method_rows)

        total_duration = self.timer.elapsed()
        feed = hu.build_ai_feed(
            self.target_dir, self.base_url, self.exact_host, total_duration,
            secrets, jscope_findings, all_routes, win_rows, blocked_rows,
            data_files, live_subs, vhosts_real, sourcemap_files, nuclei_rows,
        )

        stats = {
            "collected": len(all_routes),
            "probed": len(probe_rows),
            "live200": len(win_rows),
            "liveother": len(blocked_rows),
            "data": len(data_files),
            "subdomains": len(live_subs),
            "vhosts": len(vhosts_real),
            "js_endpoints": len(js_endpoints),
            "secrets": len(feed.get("secrets", [])),
            "flags": len(jscope_findings),
            "ai_endpoints": len(feed.get("ai_and_api_candidates", [])),
            "sourcemaps": len(sourcemap_files),
            "nuclei": len(nuclei_rows),
            "duration_seconds": round(total_duration, 1),
        }

        hu.write_report_and_context(
            self.target_dir, self.base_url, self.exact_host, self.scope_apex,
            total_duration, wave_timings, self.tool_statuses, feed, stats,
            other_rows, third_party_rows, method_rows, vhost_blocked, js_endpoints,
        )
        hu.log(f"DONE {self.exact_host} in {total_duration:.1f}s -> 200={len(win_rows)} blocked={len(blocked_rows)} ai_leads={stats['ai_endpoints']} secrets={stats['secrets']}")
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="High-speed 4-wave web & early-signal hunt runner")
    parser.add_argument("--url", required=True, help="Target URL")
    parser.add_argument("--out", default="results", help="Results output directory")
    parser.add_argument("--settings", default="config/settings.json", help="Settings JSON path")
    parser.add_argument("--budget-min", type=float, default=None, help="Hard wall-clock budget in minutes")
    args = parser.parse_args()

    settings: dict[str, Any] = {}
    s_path = Path(args.settings)
    if s_path.is_file():
        settings = json.loads(s_path.read_text(encoding="utf-8"))

    runner = HuntRunner(args.url, Path(args.out), settings, args.budget_min)

    def _handle_signal(signum: int, _frame: Any) -> None:
        hu.log(f"Received signal {signum}; stopping active workers and flushing results")
        runner.timer.request_stop()
        hu.kill_all_active_procs()

    for sig_name in ("SIGTERM", "SIGINT"):
        sig = getattr(signal, sig_name, None)
        if sig is not None:
            try:
                signal.signal(sig, _handle_signal)
            except (ValueError, OSError):
                pass

    return runner.run()


if __name__ == "__main__":
    sys.exit(main())
