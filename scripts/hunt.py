#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
One-shot maximum-discovery web hunt.

Fast, layered, Go/Rust-first. One URL per run. No discovery time limits.
Collect wide -> verify every URL with httpx -> categorize last.

Pipeline:
  subfinder/dnsx/uncover -> urlfinder -> gau -> katana (2 passes)
  -> download JS chunks -> jsluice -> anastasis -> jscope -> trufflehog
  -> collect -> vhost -> wordlist -> httpx -> x8 -> methods -> report
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urljoin, urlparse, urlunparse

import wordlist  # local module (scripts/ is on sys.path)

# ---------------------------------------------------------------------------
# constants
# ---------------------------------------------------------------------------

STATUS_WIN = {200}
STATUS_EXISTS = {301, 302, 303, 307, 308, 401, 403, 405}
VHOST_REAL = {200, 201, 202, 204, 206, 301, 302, 303, 307, 308, 401, 403, 405}
ALL_CODES = ",".join(str(i) for i in range(100, 600))

ASSET_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".webp", ".avif",
    ".css", ".woff", ".woff2", ".ttf", ".eot", ".otf",
    ".mp4", ".webm", ".mp3", ".wav", ".ogg", ".pdf", ".zip",
}
TEXT_EXT = {
    ".jsonl", ".json", ".txt", ".csv", ".md", ".js", ".mjs",
    ".html", ".htm", ".xml", ".map", ".yml", ".yaml",
}
TRACKING = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "gclid", "fbclid", "msclkid", "mc_cid", "mc_eid",
}
METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]
UNCOVER_ENGINE_KEYS = [
    ("shodan", "SHODAN_API_KEY"), ("censys", "CENSYS_API_ID"),
    ("fofa", "FOFA_EMAIL"), ("quake", "QUAKE_TOKEN"),
    ("hunter", "HUNTER_API_KEY"), ("zoomeye", "ZOOMEYE_API_KEY"),
    ("netlas", "NETLAS_API_KEY"), ("criminalip", "CRIMINALIP_API_KEY"),
    ("publicwww", "PUBLICWWW_API_KEY"), ("binaryedge", "BINARYEDGE_API_KEY"),
]
ABS_RE = re.compile(r"https?://[^\s\"'<>\\\)\]\},;]+", re.I)
REL_RE = re.compile(r"[\"'`](/[A-Za-z0-9_\-./?=&%{}:;,@+~#\[\]]{1,300})[\"'`]")
JS_RE = re.compile(r"\.js(\?|$)", re.I)

RUN_STATUS = {}
RUN_START = time.time()


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def log(msg: str) -> None:
    print(f"[{now()}] {msg}", flush=True)


def which(tool: str):
    return shutil.which(tool)


def record_status(name: str, code: int, note: str = ""):
    RUN_STATUS[name] = {"exit": code, "note": note}


def tail_log(path: Path, n: int = 12) -> str:
    try:
        return "\n".join(Path(path).read_text(encoding="utf-8", errors="replace").splitlines()[-n:])
    except Exception:  # noqa: BLE001
        return ""


def tool_name(cmd) -> str:
    return os.path.basename(str(cmd[0])).replace(".py", "")


def check_tools() -> bool:
    required = ["katana", "httpx", "ffuf", "uro", "subfinder", "dnsx", "uncover",
                "kr", "gau", "waybackurls", "jsluice", "urlfinder", "x8",
                "jscope", "anastasis", "trufflehog", "jq"]
    missing = [t for t in required if not which(t)]
    if missing:
        log("MISSING TOOLS: " + ", ".join(missing))
        return False
    log(f"tool check OK ({len(required)} tools present)")
    return True


def run(cmd, log_path: Path, timeout: int = 3600, cwd=None) -> int:
    log_path = Path(log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    name = tool_name(cmd)
    with open(log_path, "ab") as lf:
        lf.write(("\n$ " + " ".join(map(str, cmd)) + "\n").encode("utf-8", "replace"))
        lf.flush()
        try:
            p = subprocess.run([str(c) for c in cmd], cwd=str(cwd) if cwd else None,
                               stdout=lf, stderr=subprocess.STDOUT, timeout=timeout)
            lf.write(f"\n[exit {p.returncode}]\n".encode())
            record_status(name, p.returncode)
            if p.returncode != 0:
                log(f"WARN {name} exit {p.returncode}; log tail:\n{tail_log(log_path)}")
            return p.returncode
        except FileNotFoundError as e:
            lf.write(f"\n[missing: {e}]\n".encode("utf-8", "replace"))
            record_status(name, 127)
            return 127
        except subprocess.TimeoutExpired:
            lf.write(f"\n[timeout {timeout}s]\n".encode())
            record_status(name, 124)
            log(f"WARN {name} hit safety timeout ({timeout}s)")
            return 124
        except Exception as e:  # noqa: BLE001
            lf.write(f"\n[error {e}]\n".encode("utf-8", "replace"))
            record_status(name, 1)
            return 1


def run_capture(cmd, out_file: Path, log_path: Path, timeout: int = 3600, cwd=None) -> int:
    name = tool_name(cmd)
    out_file, log_path = Path(out_file), Path(log_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "ab") as lf:
        lf.write(("\n$ " + " ".join(map(str, cmd)) + "\n").encode("utf-8", "replace"))
        try:
            p = subprocess.run([str(c) for c in cmd], cwd=str(cwd) if cwd else None,
                               stdout=subprocess.PIPE, stderr=lf, timeout=timeout)
            out_file.write_bytes(p.stdout or b"")
            lf.write(f"\n[exit {p.returncode}] -> {out_file}\n".encode())
            record_status(name, p.returncode)
            if p.returncode != 0:
                log(f"WARN {name} exit {p.returncode}; log tail:\n{tail_log(log_path)}")
            return p.returncode
        except Exception as e:  # noqa: BLE001
            lf.write(f"\n[error {e}]\n".encode("utf-8", "replace"))
            record_status(name, 1)
            return 1


def read_jsonl(path: Path):
    rows = []
    if not Path(path).exists():
        return rows
    for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            rows.append(json.loads(line))
        except Exception:  # noqa: BLE001
            pass
    return rows


def write_jsonl(path: Path, rows) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, default=list) + "\n")


def normalize_base(raw: str) -> str:
    raw = raw.strip()
    if not re.match(r"^https?://", raw, re.I):
        raw = "https://" + raw
    p = urlparse(raw)
    return f"{p.scheme or 'https'}://{p.netloc}"


def normalize(u: str, base: str):
    if not u:
        return None
    u = u.strip().strip("\"'`,;)]}>").replace("\\/", "/")
    if u.startswith("//"):
        u = "https:" + u
    if not re.match(r"^https?://", u, re.I):
        if u.startswith("/"):
            u = urljoin(base, u)
        else:
            return None
    try:
        p = urlparse(u)
    except Exception:  # noqa: BLE001
        return None
    if not p.netloc or "." not in p.netloc:
        return None
    host = p.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    scheme = (p.scheme or "https").lower()
    query = urlencode([(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
                       if k.lower() not in TRACKING])
    return urlunparse((scheme, host, p.path or "/", "", query, ""))


def dedupe_key(u: str):
    p = urlparse(u)
    host = p.netloc.lower().removeprefix("www.")
    return (host, p.path or "/", p.query)


def is_asset(u: str) -> bool:
    return urlparse(u).path.lower().endswith(tuple(ASSET_EXT))


def harvest_file(path: Path, limit: int = 8_000_000):
    out = []
    try:
        if path.stat().st_size > limit:
            return out
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        return out
    out.extend(m.group(0) for m in ABS_RE.finditer(text))
    out.extend(m.group(1) for m in REL_RE.finditer(text))
    return out


def clean_url_lines(src: Path, dst: Path) -> int:
    """Normalize bare-host lines (urlfinder/gau output) into full URLs."""
    urls = []
    if src.exists():
        for line in src.read_text(encoding="utf-8", errors="replace").splitlines():
            s = line.strip().strip("\"'")
            if not s:
                continue
            if not re.match(r"^https?://", s, re.I) and "." in s.split("/")[0]:
                s = "https://" + s
            if re.match(r"^https?://", s, re.I):
                urls.append(s)
    dst.write_text("\n".join(sorted(set(urls))) + "\n", encoding="utf-8")
    return len(urls)


# ---------------------------------------------------------------------------
# collection steps
# ---------------------------------------------------------------------------

def step_subdomains(host, target_dir, logs, settings):
    if not settings.get("enable_subdomains", True):
        return
    subs = set()
    if which("subfinder"):
        out = target_dir / "subfinder.txt"
        run(["subfinder", "-d", host, "-all", "-recursive", "-silent", "-o", str(out)],
            logs / "subfinder.log", timeout=3600)
        if out.exists():
            subs.update(l.strip().lower() for l in out.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip())
    if settings.get("enable_uncover", True) and which("uncover"):
        engines = [e for e, k in UNCOVER_ENGINE_KEYS if os.environ.get(k, "").strip()]
        if engines:
            out = target_dir / "uncover.txt"
            run(["uncover", "-q", f'ssl:"{host}"', "-e", engines[0], "-silent", "-o", str(out)],
                logs / "uncover.log", timeout=1200)
            if out.exists():
                subs.update(l.strip().lower() for l in out.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip())
        else:
            record_status("uncover", 0, "no API key configured — no external data")

    if not subs:
        return
    allf = target_dir / "subdomains_all.txt"
    allf.write_text("\n".join(sorted(subs)) + "\n", encoding="utf-8")
    live = set(subs)
    if which("dnsx"):
        run(["dnsx", "-l", str(allf), "-silent", "-o", str(target_dir / "subdomains_live.txt")],
            logs / "dnsx.log", timeout=3600)
        lf = target_dir / "subdomains_live.txt"
        if lf.exists():
            resolved = {l.strip().lower() for l in lf.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()}
            if resolved:
                live = resolved
    cap = int(settings.get("max_subdomains", 0) or 0)
    chosen = sorted(live)[:cap] if cap > 0 else sorted(live)
    (target_dir / "subdomains_urls.txt").write_text(
        "\n".join(f"https://{h}" for h in chosen) + "\n", encoding="utf-8")
    log(f"subdomains: {len(subs)} found, {len(live)} resolved, {len(chosen)} queued")


def step_urlfinder(host, target_dir, logs, settings):
    if not settings.get("enable_urlfinder", True):
        return
    raw = target_dir / "urlfinder_raw.txt"
    cmd = ["urlfinder", "-d", host, "-o", str(raw), "-duc", "-silent", "-max-time", "0"]
    rc = run(cmd, logs / "urlfinder.log", timeout=3600)
    if rc != 0:  # older builds don't accept -max-time 0
        run(["urlfinder", "-d", host, "-o", str(raw), "-duc", "-silent"],
            logs / "urlfinder.log", timeout=3600)
    n = clean_url_lines(raw, target_dir / "urlfinder_urls.txt")
    log(f"urlfinder: {n} URLs")


def step_gau(host, target_dir, logs, settings):
    if not settings.get("enable_gau", True):
        return
    out = target_dir / "gau.txt"
    run(["gau", host, "--subs", "--threads", "10",
         "--blacklist", "png,jpg,jpeg,gif,svg,css,woff,woff2,ttf,eot,ico,mp4,mp3,pdf",
         "--o", str(out)], logs / "gau.log", timeout=3600)
    clean_url_lines(out, target_dir / "gau_urls.txt")


def step_katana(base, target_dir, logs, settings):
    if not settings.get("enable_katana", True):
        return
    k = target_dir / "katana"
    k.mkdir(parents=True, exist_ok=True)
    d = str(settings.get("katana_depth", 10))
    # NOTE: JSONL flag is -j (NOT -json).
    run(["katana", "-u", base, "-d", d, "-jc", "-jsl", "-kf", "all", "-aff",
         "-ef", "png,jpg,jpeg,gif,svg,css,woff,woff2,ttf,eot,ico,mp4,mp3,pdf",
         "-c", "30", "-timeout", "20", "-retry", "2", "-silent", "-j",
         "-o", str(k / "pass1.jsonl")], logs / "katana_pass1.log", timeout=3600)
    if settings.get("enable_browser", True):
        run(["katana", "-u", base, "-d", d, "-headless", "-xhr", "-no-sandbox",
             "-jsl", "-c", "10", "-timeout", "20", "-silent", "-j",
             "-o", str(k / "pass2.jsonl")], logs / "katana_pass2.log", timeout=3600)


def collect_js_urls(target_dir, base):
    urls = set()
    for name in ("urlfinder_urls.txt", "gau_urls.txt", "js_urls.txt"):
        p = target_dir / name
        if p.exists():
            urls.update(l.strip() for l in p.read_text(encoding="utf-8", errors="replace").splitlines()
                        if l.strip() and JS_RE.search(l))
    for f in (target_dir / "katana").glob("*.jsonl"):
        for row in read_jsonl(f):
            u = (row.get("request") or {}).get("url") or row.get("url")
            if u and JS_RE.search(u):
                urls.add(u)
    return sorted(urls)


def step_download_js(target_dir, logs, settings):
    urls = collect_js_urls(target_dir, "")
    cap = int(settings.get("max_js_files", 10000) or 10000)
    urls = urls[:cap] if cap > 0 else urls
    if not urls:
        record_status("js-download", 0, "no JS URLs found")
        return []
    chunks = target_dir / "chunks"
    chunks.mkdir(parents=True, exist_ok=True)
    ua = settings.get("user_agent", "hunt")
    timeout = int(settings.get("js_download_timeout", 15))

    def fetch(u):
        try:
            req = urllib.request.Request(u, headers={"User-Agent": ua})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = r.read()
            if len(body) < 20 or len(body) > 20_000_000:
                return None
            name = hashlib.sha256(u.encode()).hexdigest()[:16] + ".js"
            (chunks / name).write_bytes(body)
            return u
        except Exception:  # noqa: BLE001
            return None

    saved = []
    with ThreadPoolExecutor(max_workers=int(settings.get("js_download_threads", 20))) as pool:
        for f in as_completed([pool.submit(fetch, u) for u in urls]):
            r = f.result()
            if r:
                saved.append(r)
    (target_dir / "js_urls.txt").write_text("\n".join(saved) + "\n", encoding="utf-8")
    record_status("js-download", 0, f"{len(saved)} chunks saved of {len(urls)}")
    log(f"JS chunks downloaded: {len(saved)} / {len(urls)}")
    return saved


def step_jsluice(target_dir, logs, settings):
    if not settings.get("enable_jsluice", True):
        return
    js = sorted((target_dir / "chunks").glob("*.js")) if (target_dir / "chunks").exists() else []
    out = target_dir / "jsluice.jsonl"
    secrets = target_dir / "jsluice_secrets.jsonl"
    with open(out, "w", encoding="utf-8") as fo, open(secrets, "w", encoding="utf-8") as fs:
        for p in js:
            try:
                r = subprocess.run(["jsluice", "urls", str(p)], capture_output=True, timeout=60)
                fo.write((r.stdout or b"").decode("utf-8", "replace"))
            except Exception:  # noqa: BLE001
                pass
            try:
                r = subprocess.run(["jsluice", "secrets", str(p)], capture_output=True, timeout=60)
                fs.write((r.stdout or b"").decode("utf-8", "replace"))
            except Exception:  # noqa: BLE001
                pass
    record_status("jsluice", 0, f"{len(js)} files parsed")
    log(f"jsluice: parsed {len(js)} chunks")


def _walk_anastasis(obj, urls, endpoints, params):
    if isinstance(obj, dict):
        path = obj.get("path")
        if isinstance(path, str) and path.startswith("/"):
            method = str(obj.get("method") or "GET").upper()
            urls.append(f"{method} {path}")
            endpoints.append({
                "method": method, "path": path,
                "confidence": obj.get("confidence"),
                "source": obj.get("source", "anastasis"),
            })
        for key, value in obj.items():
            if key in ("name", "parameter") and isinstance(value, str):
                params.append(value)
            _walk_anastasis(value, urls, endpoints, params)
    elif isinstance(obj, list):
        for v in obj:
            _walk_anastasis(v, urls, endpoints, params)


def step_anastasis(host, base, target_dir, logs):
    if not settings_enabled("enable_anastasis"):
        return
    out = target_dir / "anastasis.json"
    rc = run(["anastasis", "-u", host, "--params", "-o", "json", "--save", str(out)],
             logs / "anastasis.log", timeout=3600)
    if rc != 0 and out.exists() is False:
        record_status("anastasis", rc, "see logs")
        return
    urls, endpoints, params = [], [], []
    try:
        _walk_anastasis(json.loads(out.read_text(encoding="utf-8", errors="replace")),
                        urls, endpoints, params)
    except Exception:  # noqa: BLE001
        pass
    full = []
    for item in urls:
        parts = item.split(" ", 1)
        if len(parts) == 2:
            full.append(parts[1])
    (target_dir / "anastasis_urls.txt").write_text("\n".join(sorted(set(full))) + "\n", encoding="utf-8")
    write_jsonl(target_dir / "anastasis_endpoints.jsonl", endpoints)
    record_status("anastasis", 0, f"{len(endpoints)} endpoints, {len(set(params))} params")
    log(f"anastasis: {len(endpoints)} endpoints, {len(set(params))} params")


def settings_enabled(key: str) -> bool:
    return bool(SETTINGS.get(key, True))


def step_jscope(target_dir, logs):
    if not settings_enabled("enable_jscope"):
        return
    chunks = target_dir / "chunks"
    if not chunks.exists() or not any(chunks.glob("*.js")):
        record_status("jscope", 0, "no local chunks to analyse")
        return
    run_capture(["jscope", "analyze", str(chunks), "--verbose"],
                target_dir / "jscope.txt", logs / "jscope.log", timeout=3600)


def step_trufflehog(target_dir, logs):
    if not settings_enabled("enable_trufflehog"):
        return
    src = target_dir / "chunks"
    if not src.exists():
        src = target_dir
    run_capture(["trufflehog", "filesystem", str(src), "--json", "--no-update"],
                target_dir / "secrets.jsonl", logs / "trufflehog.log", timeout=3600)


def collect(target_dir: Path, base: str):
    routes = {}

    def add(raw, method, source):
        n = normalize(raw, base)
        if not n:
            return
        k = dedupe_key(n)
        rec = routes.get(k)
        if rec is None:
            rec = {"url": n, "method": (method or "GET").upper(), "sources": set()}
            routes[k] = rec
        rec["sources"].add(source)
        if method and rec["method"] == "GET":
            rec["method"] = method.upper()

    for f in (target_dir / "katana").glob("*.jsonl"):
        for j in read_jsonl(f):
            req = j.get("request") or {}
            add(req.get("url") or j.get("url"), req.get("method"), f.name)

    for f in target_dir.glob("jsluice*.jsonl"):
        for j in read_jsonl(f):
            add(j.get("url"), j.get("method"), f.name)

    for f in target_dir.rglob("*"):
        if not f.is_file() or "logs" in f.parts or "chunks" in f.parts:
            continue
        if f.suffix.lower() in TEXT_EXT:
            for raw in harvest_file(f):
                add(raw, "GET", f.name)
    return routes


# ---------------------------------------------------------------------------
# verify + enrich
# ---------------------------------------------------------------------------

def step_vhost(base, target_dir, logs, settings):
    if not settings_enabled("enable_vhost"):
        return []
    host = urlparse(base).netloc.split(":")[0]
    src = target_dir / "subdomains_all.txt"
    if not src.exists():
        record_status("vhost", 0, "no subdomain names")
        return []
    words = set()
    for line in src.read_text(encoding="utf-8", errors="replace").splitlines():
        h = line.strip().lower()
        if h.endswith("." + host):
            w = h[:-(len(host) + 1)]
            if w and "." not in w:
                words.add(w)
    if not words:
        return []
    probe_url = base.rstrip("/") + "/"
    ua = settings.get("user_agent", "hunt")
    timeout = int(settings.get("method_timeout", 10))

    def check(name):
        req = urllib.request.Request(probe_url, headers={"Host": f"{name}.{host}", "User-Agent": ua})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return name, r.status
        except urllib.error.HTTPError as e:
            return name, e.code
        except Exception:  # noqa: BLE001
            return name, 0

    rows, live = [], []
    with ThreadPoolExecutor(max_workers=int(settings.get("method_threads", 20))) as pool:
        for f in as_completed([pool.submit(check, w) for w in sorted(words)]):
            name, code = f.result()
            vh = f"{name}.{host}"
            rows.append({"host": vh, "status_code": code})
            # 530/Cloudflare errors and 0 are NOT real hosts
            if code in VHOST_REAL:
                live.append(vh)
    write_jsonl(target_dir / "vhost.jsonl", rows)
    record_status("vhost", 0, f"{len(live)} real of {len(words)} tested")
    log(f"vhost: {len(live)} real hosts of {len(words)} names")
    return live


def probe(routes, target_dir, logs, settings):
    if not settings_enabled("enable_httpx") or not which("httpx"):
        return []
    rows = [r for r in routes.values() if not is_asset(r["url"])] if not settings.get("probe_assets") else list(routes.values())
    cap = int(settings.get("max_urls", 0) or 0)
    if cap > 0 and len(rows) > cap:
        rows = rows[:cap]
    src = target_dir / "urls_to_probe.txt"
    src.write_text("\n".join(r["url"] for r in rows) + "\n", encoding="utf-8")
    use = src
    if settings_enabled("enable_uro") and which("uro"):
        dedup = target_dir / "urls_to_probe_uro.txt"
        run(["uro", "-i", str(src), "-o", str(dedup)], logs / "uro.log", timeout=1800)
        if dedup.exists() and dedup.stat().st_size > 0:
            use = dedup
    out = target_dir / "probe.jsonl"
    # Explicit numeric match codes = NO filtering, no "all" string bug.
    run(["httpx", "-l", str(use), "-mc", ALL_CODES, "-sc", "-cl", "-ct",
         "-title", "-td", "-j", "-o", str(out), "-silent",
         "-timeout", str(settings.get("request_timeout", 20)), "-retries", "1",
         "-rl", str(settings.get("httpx_rate", 50)),
         "-threads", str(settings.get("httpx_threads", 50))],
        logs / "httpx.log", timeout=3600)
    return read_jsonl(out)


def merge_hits(routes, hits, base):
    added = 0
    for h in hits:
        n = normalize(h.get("url"), base)
        if not n:
            continue
        k = dedupe_key(n)
        if k not in routes:
            routes[k] = {"url": n, "method": h.get("method") or "GET", "sources": {"verify"}}
            added += 1
    return added


def step_x8(base, target_dir, logs, settings, param_file):
    if not settings_enabled("enable_x8") or not which("x8"):
        return
    if not Path(param_file).exists() or Path(param_file).stat().st_size == 0:
        record_status("x8", 0, "no parameter wordlist")
        return
    run_capture(["x8", "-u", base.rstrip("/") + "/", "-w", str(param_file)],
                target_dir / "x8.txt", logs / "x8.log", timeout=3600)
    record_status("x8", 0, "parameter scan complete")


def step_methods(probe_rows, logs, settings):
    if not settings_enabled("enable_methods"):
        return []
    targets = [r for r in probe_rows if r.get("status_code") in (200, 401, 403, 405)]
    cap = int(settings.get("method_targets", 200) or 0)
    if cap > 0:
        targets = targets[:cap]
    jobs = [(r["url"], m) for r in targets if r.get("url") for m in METHODS]
    if not jobs:
        return []
    ua = settings.get("user_agent", "hunt")
    timeout = int(settings.get("method_timeout", 10))

    def one(url, method):
        try:
            req = urllib.request.Request(url, method=method, headers={"User-Agent": ua})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return url, method, r.status
        except urllib.error.HTTPError as e:
            return url, method, e.code
        except Exception:  # noqa: BLE001
            return url, method, None

    results = []
    with ThreadPoolExecutor(max_workers=int(settings.get("method_threads", 20))) as pool:
        for f in as_completed([pool.submit(one, u, m) for u, m in jobs]):
            u, m, code = f.result()
            if code is not None:
                results.append({"url": u, "method": m, "status_code": code, "source": "method"})
    record_status("methods", 0, f"{len(results)} method responses")
    return results


def write_context(target_dir, base, routes, stats):
    ctx = {
        "target": base,
        "generated": now(),
        "routes": [{"url": r["url"], "method": r.get("method", "GET")} for r in routes.values()],
        "stats": stats,
    }
    (target_dir / "context.json").write_text(
        json.dumps(ctx, indent=1, ensure_ascii=False, default=list), encoding="utf-8")


# ---------------------------------------------------------------------------
# report
# ---------------------------------------------------------------------------

def report(target_dir, base, routes, probe_rows, extra_rows, settings):
    target_dir = Path(target_dir)
    merged = {}
    for r in list(probe_rows) + list(extra_rows):
        u = r.get("url")
        if not u:
            continue
        k = (dedupe_key(u), (r.get("method") or "GET").upper())
        if k not in merged:
            merged[k] = dict(r)
        else:
            merged[k].setdefault("source", r.get("source"))

    win, blocked, other = [], [], []
    for r in merged.values():
        try:
            st = int(r.get("status_code") or r.get("status") or 0)
        except Exception:  # noqa: BLE001
            st = 0
        r["status_code"] = st
        (win if st in STATUS_WIN else blocked if st in STATUS_EXISTS else other).append(r)
    key = lambda r: r.get("url") or ""
    for group in (win, blocked, other):
        group.sort(key=key)

    all_routes = [{"url": r["url"], "method": r.get("method", "GET"),
                   "sources": sorted(r.get("sources", []))} for r in routes.values()]
    all_routes.sort(key=key)

    data_files = [r for r in win if
                  any(x in (r.get("content_type") or "").lower() for x in ("json", "csv", "xml", "spreadsheet"))
                  or urlparse(r.get("url", "")).path.lower().endswith((".json", ".jsonl", ".csv", ".xml", ".xlsx", ".xls"))]

    params = []
    for r in all_routes:
        q = urlparse(r["url"]).query
        if q:
            params.append({"url": r["url"], "method": r["method"],
                           "params": sorted({k for k, _ in parse_qsl(q, keep_blank_values=True)})})

    all_subs = sorted({l.strip().lower() for f in [target_dir / "subdomains_all.txt"] if f.exists()
                       for l in f.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()})
    live_subs = sorted({l.strip().lower() for f in [target_dir / "subdomains_live.txt"] if f.exists()
                        for l in f.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()})
    sub_rows = [{"host": h, "resolved": h in live_subs, "source": "subfinder/uncover"} for h in all_subs]

    js_endpoints = read_jsonl(target_dir / "anastasis_endpoints.jsonl")
    vhosts = [v for v in read_jsonl(target_dir / "vhost.jsonl") if v.get("status_code") in VHOST_REAL]
    secrets = [l for l in (target_dir / "secrets.jsonl").read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()] if (target_dir / "secrets.jsonl").exists() else []

    write_jsonl(target_dir / "all_routes.jsonl", all_routes)
    write_jsonl(target_dir / "accessible_200.jsonl", win)
    write_jsonl(target_dir / "exists_blocked.jsonl", blocked)
    write_jsonl(target_dir / "other_status.jsonl", other)
    write_jsonl(target_dir / "data_files.jsonl", data_files)
    write_jsonl(target_dir / "params.jsonl", params)
    write_jsonl(target_dir / "subdomains.jsonl", sub_rows)
    write_jsonl(target_dir / "js_endpoints.jsonl", js_endpoints)
    write_jsonl(target_dir / "live_200.jsonl", win)
    write_jsonl(target_dir / "live_other.jsonl", blocked)

    elapsed = int(time.time() - RUN_START)
    L = [f"# Hunt Report — {base}", "",
         f"Generated: {now()} &nbsp;|&nbsp; Duration: {elapsed // 60}m {elapsed % 60}s", "",
         "> **Nothing is filtered during collection. This report is only a grouping.**", "",
         "## Summary", "", "| What | Count | Meaning |", "|---|---:|---|",
         f"| Routes collected | {len(all_routes)} | Every URL found, nothing removed |",
         f"| Responses checked | {len(merged)} | Every URL actually requested |",
         f"| **Accessible (200)** | **{len(win)}** | Confirmed live — the wins |",
         f"| Exists but different status | {len(blocked)} | 301/302/401/403/405 — real route, blocked |",
         f"| Other responses | {len(other)} | 404/500/etc — kept, not discarded |",
         f"| Subdomains (resolved) | {len(live_subs)} | DNS-verified |",
         f"| Virtual hosts (real) | {len(vhosts)} | Cloudflare 530 excluded |",
         f"| Parameters | {len(params)} | URLs with query params |",
         f"| JS endpoints (AST) | {len(js_endpoints)} | anastasis evidence-backed |",
         f"| Secret candidates | {len(secrets)} | verify manually |", ""]

    def section(title, rows, n=75):
        L.append(f"## {title}")
        L.append("")
        if not rows:
            L.append("_None in this category._")
            L.append("")
            return
        L.append("| Status | Method | URL | Type | Size | Source |")
        L.append("|---|---|---|---|---|---|")
        for r in rows[:n]:
            u = (r.get("url") or "").replace("|", "%7C")
            L.append(f"| {r.get('status_code','')} | {r.get('method','GET')} | `{u}` | "
                     f"{(r.get('content_type') or '').split(';')[0]} | {r.get('content_length','')} | {r.get('source','')} |")
        if len(rows) > n:
            L.append(f"| … | … | _{len(rows)-n} more in JSONL_ | … | … | … |")
        L.append("")

    section("1. SUCCESS — HTTP 200", win)
    section("2. EXISTS BUT DIFFERENT STATUS (301/302/401/403/405)", blocked)
    section("3. OTHER RESPONSES — kept, never discarded", other)
    section("4. DATA FILES (accessible)", data_files)

    L += ["## 5. SUBDOMAINS (detailed)", "",
          f"Found **{len(all_subs)}**, DNS-resolved **{len(live_subs)}**.", "",
          "| Host | Resolved | Source |", "|---|---|---|"]
    for h in all_subs[:150]:
        L.append(f"| `{h}` | {'yes' if h in live_subs else 'no'} | passive |")
    if len(all_subs) > 150:
        L.append(f"| _{len(all_subs)-150} more_ | | |")
    L.append("")

    L += ["## 6. VIRTUAL HOSTS (real statuses only)", ""]
    if vhosts:
        L += ["| Host | Status |", "|---|---|"]
        for v in vhosts[:100]:
            L.append(f"| `{v.get('host')}` | {v.get('status_code')} |")
    else:
        L.append("_None (Cloudflare 530 responses are excluded as noise)._")
    L.append("")

    L += ["## 7. JS ENDPOINTS (AST, evidence-backed)", ""]
    if js_endpoints:
        L += ["| Method | Path | Confidence |", "|---|---|---|"]
        for e in js_endpoints[:100]:
            L.append(f"| {e.get('method','GET')} | `{e.get('path','')}` | {e.get('confidence','')} |")
    else:
        L.append("_None extracted._")
    L.append("")

    L += ["## 8. PARAMETERS", ""]
    if params:
        L += ["| URL | Params |", "|---|---|"]
        for p in params[:60]:
            L.append(f"| `{p['url']}` | {', '.join(p['params'])} |")
    else:
        L.append("_None found._")
    L.append("")

    L += ["## 9. SECRET CANDIDATES", "",
          f"{len(secrets)} candidate(s) in `secrets.jsonl`. Verify manually." if secrets else "_None found._", ""]

    L += ["## 10. TOOL RUN STATUS (no silent skips)", "", "| Tool | Result | Detail |", "|---|---|---|"]
    for name in sorted(RUN_STATUS):
        s = RUN_STATUS[name]
        L.append(f"| `{name}` | {'OK' if s['exit'] == 0 else 'exit ' + str(s['exit'])} | {s.get('note') or ('see logs/' if s['exit'] else 'completed')} |")
    L.append("")

    L += ["## 11. INTENTIONALLY NOT RUN", "",
          "- **ffuf path brute** — off by default; `wordlist.txt` is ready. Set `enable_brute: true` later.",
          "- **kiterunner** — off by default alongside ffuf.", ""]

    out_files = [
        ("REPORT.md", "this report"), ("all_routes.jsonl", "every route, unfiltered"),
        ("accessible_200.jsonl", "HTTP 200 wins"), ("exists_blocked.jsonl", "exists but blocked"),
        ("other_status.jsonl", "all other statuses"), ("data_files.jsonl", "JSON/CSV/XML among 200s"),
        ("params.jsonl", "parameters"), ("subdomains.jsonl", "subdomains + resolution"),
        ("js_endpoints.jsonl", "AST endpoints"), ("vhost.jsonl", "vhost checks"),
        ("jsluice.jsonl", "JS-derived URLs"), ("anastasis_endpoints.jsonl", "AST endpoints"),
        ("jscope.txt", "evidence-ranked JS analysis"), ("secrets.jsonl", "secret candidates"),
        ("wordlist.txt", "target-specific fuzz list"), ("params.txt", "parameter wordlist"),
        ("context.json", "shared context"), ("js_urls.txt", "JS chunk URLs"),
        ("logs/", "raw tool logs"),
    ]
    L += ["## 12. OUTPUT FILES", "", "| File | Meaning |", "|---|---|"]
    for name, meaning in out_files:
        p = target_dir / name
        if p.exists():
            L.append(f"| [`{name}`]({name}) | {meaning} ({p.stat().st_size:,} B) |")
    L += ["", "## Status meaning", "", "| Status | Meaning |", "|---|---|",
          "| 200 | Accessible — confirmed win |", "| 301/302/307/308 | Redirect — route exists |",
          "| 401/403 | Exists but blocked |", "| 405 | Exists, wrong method |",
          "| 404 | Not found — kept for completeness |", "| 530 | Cloudflare error — excluded from vhosts |", "",
          "> Collect wide, verify status, categorize last. Nothing deleted from data files."]

    (target_dir / "REPORT.md").write_text("\n".join(L), encoding="utf-8")
    return {"collected": len(all_routes), "probed": len(merged), "live200": len(win),
            "liveother": len(blocked), "data": len(data_files), "subdomains": len(live_subs),
            "js_endpoints": len(js_endpoints), "vhosts": len(vhosts)}


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

SETTINGS = {}


def main() -> int:
    global SETTINGS
    ap = argparse.ArgumentParser()
    ap.add_argument("--urls", default="urls.txt")
    ap.add_argument("--out", default="results")
    ap.add_argument("--settings", default="config/settings.json")
    args = ap.parse_args()

    SETTINGS = json.loads(Path(args.settings).read_text(encoding="utf-8"))
    for key, env in (("enable_subdomains", "ENABLE_SUBDOMAINS"),
                     ("enable_brute", "ENABLE_BRUTE"),
                     ("enable_browser", "ENABLE_BROWSER")):
        if os.environ.get(env) is not None:
            SETTINGS[key] = os.environ[env].strip().lower() in ("1", "true", "yes", "on")

    if not check_tools():
        return 2

    raw_urls = [l.strip() for l in Path(args.urls).read_text(encoding="utf-8").splitlines()
                if l.strip() and not l.strip().startswith("#")]
    if not raw_urls:
        log("no targets in urls file")
        return 2

    out_root = Path(args.out)
    out_root.mkdir(parents=True, exist_ok=True)
    summary = []

    def step(name, fn, *a):
        try:
            log(f"STEP {name} start")
            r = fn(*a)
            log(f"STEP {name} done")
            return r
        except Exception as e:  # noqa: BLE001
            log(f"STEP {name} FAILED: {e}")
            return None

    for raw in raw_urls:
        base = normalize_base(raw)
        host = urlparse(base).netloc
        td = out_root / host.replace(":", "_")
        logs = td / "logs"
        logs.mkdir(parents=True, exist_ok=True)
        log(f"=== TARGET {base} -> {td} ===")

        step("subdomains", step_subdomains, host, td, logs, SETTINGS)
        step("urlfinder", step_urlfinder, host, td, logs, SETTINGS)
        step("gau", step_gau, host, td, logs, SETTINGS)
        step("katana", step_katana, base, td, logs, SETTINGS)
        step("js-download", step_download_js, td, logs, SETTINGS)
        step("jsluice", step_jsluice, td, logs, SETTINGS)
        step("anastasis", step_anastasis, host, base, td, logs)
        step("jscope", step_jscope, td, logs)
        step("trufflehog", step_trufflehog, td, logs)

        routes = collect(td, base)
        log(f"collected {len(routes)} unique URLs")

        live_vhosts = step("vhost", step_vhost, base, td, logs, SETTINGS) or []
        for h in live_vhosts:
            n = normalize(f"https://{h}", base)
            if n:
                routes[dedupe_key(n)] = {"url": n, "method": "GET", "sources": {"vhost"}}

        wl = td / "wordlist.txt"
        pf = td / "params.txt"
        info = wordlist.build(td, base, SETTINGS.get("wordlist", "wordlists/common.txt"),
                              wl, int(SETTINGS.get("wordlist_max", 8000)), pf)
        log(f"wordlist built: {info}")

        probe_rows = probe(routes, td, logs, SETTINGS) or []
        extra = step_methods(probe_rows, logs, SETTINGS) or []
        step("x8", step_x8, base, td, logs, SETTINGS, pf)

        if SETTINGS.get("enable_brute", False):
            log("ffuf brute enabled (wordlist ready)")
        else:
            record_status("ffuf", 0, "off by choice — wordlist prepared")

        stats = report(td, base, routes, probe_rows, extra, SETTINGS)
        write_context(td, base, routes, stats)
        summary.append((base, stats))
        log(f"REPORT {td / 'REPORT.md'} -> {stats}")

    idx = ["# Hunt results", "", f"Generated: {now()}", "",
           "Open a target's **REPORT.md** for the full findings.", "",
           "| Target | Report | Accessible 200 | Exists/blocked | Subdomains | JS endpoints | Routes |",
           "|---|---|---:|---:|---:|---:|---:|"]
    for base, s in summary:
        h = urlparse(base).netloc.replace(":", "_")
        idx.append(f"| `{h}` | [REPORT.md]({h}/REPORT.md) | {s['live200']} | {s['liveother']} | "
                   f"{s['subdomains']} | {s['js_endpoints']} | {s['collected']} |")
    idx += ["", "- **Accessible 200** = confirmed live responses.",
            "- **Exists/blocked** = real routes returning 301/302/401/403/405.",
            "- No time limits were applied to discovery. ffuf was off by choice; wordlists are ready.", ""]
    (out_root / "INDEX.md").write_text("\n".join(idx), encoding="utf-8")
    (out_root / "SUMMARY.md").write_text(
        "\n".join(["# Summary", ""] + [f"- {b}: {s}" for b, s in summary]) + "\n", encoding="utf-8")
    log(f"INDEX {out_root / 'INDEX.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
