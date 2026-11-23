#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
One-shot maximum-discovery web hunt.

Fast, layered, Go/Rust-first. One URL per run. No discovery time limits.
Collect wide -> verify every URL with httpx -> categorize last.

Pipeline:
  subfinder/dnsx/uncover -> urlfinder(dev) -> waybackurls -> katana -> cariddi
  -> recursive JS chunks -> jsluice(batched)/anastasis(local)/jscope
  -> trufflehog+noseyparker -> httpx -> x8/methods -> nuclei -> report+push
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
JS_REF_RE = re.compile(r"[\"'`]([^\"'`\s]{1,400}\.js(?:\?[^\"'`\s]*)?)[\"'`]", re.I)

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
                "kr", "waybackurls", "jsluice", "urlfinder", "x8",
                "jscope", "anastasis", "trufflehog", "jq", "cariddi",
                "noseyparker", "getJS", "subjs", "nuclei"]
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


def clean_host(netloc: str) -> str:
    h = str(netloc).lower()
    return h[4:] if h.startswith("www.") else h


def dedupe_key(u: str):
    p = urlparse(u)
    host = clean_host(p.netloc)
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
    # No -silent: it hides source errors (upstream issue #166).
    cmd = ["urlfinder", "-d", host, "-o", str(raw), "-duc", "-max-time", "0"]
    rc = run(cmd, logs / "urlfinder.log", timeout=3600)
    if rc != 0:  # older builds don't accept -max-time 0
        run(["urlfinder", "-d", host, "-o", str(raw), "-duc"],
            logs / "urlfinder.log", timeout=3600)
    n = clean_url_lines(raw, target_dir / "urlfinder_urls.txt")
    log(f"urlfinder: {n} URLs")


def step_waybackurls(host, target_dir, logs, settings):
    if not settings.get("enable_waybackurls", True):
        return
    out = target_dir / "wayback.txt"
    run_capture(["waybackurls", host], out, logs / "waybackurls.log", timeout=1800)
    clean_url_lines(out, target_dir / "wayback_urls.txt")


def step_katana(base, target_dir, logs, settings):
    if not settings.get("enable_katana", True):
        return
    k = target_dir / "katana"
    k.mkdir(parents=True, exist_ok=True)
    d = str(settings.get("katana_depth", 5))
    mrs = str(settings.get("katana_max_response", 2097152))

    # Lightweight, memory-safe flags.
    # NO -jsl (officially "memory intensive" and redundant with jsluice/anastasis).
    # NO -aff (experimental form filling).
    # -fs fqdn keeps the crawl on this exact host instead of every subdomain.
    # -or/-ob keep JSONL small; -mrs caps response bytes read.
    common = ["-d", d, "-fs", "fqdn", "-mrs", mrs, "-iqp", "-or", "-ob", "-duc",
              "-silent", "-j",
              "-ef", "png,jpg,jpeg,gif,svg,css,woff,woff2,ttf,eot,ico,mp4,mp3,pdf"]

    # Pass 1 — standard mode, JS link crawling, known files.
    out1 = k / "pass1.jsonl"
    cmd1 = ["katana", "-u", base, "-jc", "-kf", "all", "-c", "10", "-p", "5"] + common + ["-o", str(out1)]
    if run(cmd1, logs / "katana_pass1.log", timeout=1800) != 0:
        log("katana pass1: retrying with minimal flags")
        run(["katana", "-u", base, "-d", d, "-jc", "-silent", "-j", "-o", str(out1)],
            logs / "katana_pass1_fallback.log", timeout=1800)

    # Pass 2 — headless for runtime-DOM/XHR endpoints (lower concurrency).
    if settings.get("enable_browser", True):
        out2 = k / "pass2.jsonl"
        cmd2 = ["katana", "-u", base, "-headless", "-xhr", "-no-sandbox",
                "-c", "5", "-p", "3"] + common + ["-o", str(out2)]
        if run(cmd2, logs / "katana_pass2.log", timeout=1800) != 0:
            log("katana pass2: retrying with minimal flags")
            run(["katana", "-u", base, "-d", d, "-headless", "-xhr", "-no-sandbox",
                 "-silent", "-j", "-o", str(out2)],
                logs / "katana_pass2_fallback.log", timeout=1800)


def step_cariddi(base, target_dir, logs, settings):
    """Crawl + hunt secrets/endpoints/juicy files in one fast Go pass (stdin)."""
    if not settings.get("enable_cariddi", True):
        return
    out = target_dir / "cariddi.txt"
    try:
        proc = subprocess.run(
            ["bash", "-c",
             f"printf '%s\\n' {shlex_quote(base)} | cariddi -s -e -info -ext 2 -c 50 -t 10"],
            capture_output=True, timeout=1800)
        out.write_bytes(proc.stdout or b"")
        (logs / "cariddi.log").write_bytes(proc.stderr or b"")
        record_status("cariddi", proc.returncode)
    except Exception as e:  # noqa: BLE001
        record_status("cariddi", 1, str(e))
    count = sum(1 for _ in out.open(encoding="utf-8", errors="replace")) if out.exists() else 0
    log(f"cariddi: {count} lines")


def shlex_quote(s: str) -> str:
    import shlex
    return shlex.quote(s)


def step_js_seeds(base, target_dir, logs, settings):
    """getJS + subjs: extra JS-file seeds from the live page."""
    if not settings.get("enable_js_seeds", True):
        return
    out = target_dir / "js_seeds.txt"
    parts = []
    if which("getJS"):
        p = subprocess.run(["getJS", "-url", base], capture_output=True, timeout=300)
        parts.append(p.stdout or b"")
        record_status("getJS", p.returncode)
    if which("subjs"):
        p = subprocess.run(["bash", "-c", f"printf '%s\\n' {shlex_quote(base)} | subjs"],
                           capture_output=True, timeout=300)
        parts.append(p.stdout or b"")
        record_status("subjs", p.returncode)
    out.write_bytes(b"\n".join(parts))
    log(f"js seeds: {out.stat().st_size} bytes")


def collect_js_urls(target_dir, base):
    urls = set()
    # cariddi + passive sources are the main JS URL providers.
    for name in ("urlfinder_urls.txt", "wayback_urls.txt", "cariddi.txt",
                 "js_seeds.txt", "anastasis_urls.txt", "js_urls.txt"):
        p = target_dir / name
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        for m in ABS_RE.finditer(text):
            u = m.group(0).rstrip("\"',}]")
            if JS_RE.search(u):
                urls.add(u)
    for f in (target_dir / "katana").glob("*.jsonl"):
        for row in read_jsonl(f):
            u = (row.get("request") or {}).get("url") or row.get("url")
            if u and JS_RE.search(u):
                urls.add(u)
    return sorted(urls)


def _resolve_js_ref(ref: str, source_url: str):
    """Resolve a JS reference found inside a chunk into an absolute URL."""
    ref = ref.strip().strip("\"'`")
    if not ref or len(ref) > 500:
        return None
    if ref.startswith("//"):
        ref = "https:" + ref
    if re.match(r"^https?://", ref, re.I):
        return ref
    if ref.startswith("/") or ref.startswith("."):
        try:
            return urljoin(source_url, ref)
        except Exception:  # noqa: BLE001
            return None
    return None


def step_download_js(target_dir, logs, settings):
    seeds = collect_js_urls(target_dir, "")
    cap = int(settings.get("max_js_files", 10000) or 10000)
    rounds = max(1, int(settings.get("js_crawl_rounds", 3)))
    if not seeds:
        record_status("js-download", 0, "no JS URLs found")
        return []
    chunks = target_dir / "chunks"
    chunks.mkdir(parents=True, exist_ok=True)
    ua = settings.get("user_agent", "hunt")
    timeout = int(settings.get("js_download_timeout", 15))
    threads = int(settings.get("js_download_threads", 20))

    def fetch(u):
        try:
            req = urllib.request.Request(u, headers={"User-Agent": ua})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = r.read()
            if len(body) < 20 or len(body) > 20_000_000:
                return u, None
            return u, body
        except Exception:  # noqa: BLE001
            return u, None

    saved, seen = [], set()
    queue = list(dict.fromkeys(seeds))
    for rnd in range(rounds):
        if not queue or (cap > 0 and len(saved) >= cap):
            break
        batch = [u for u in queue if u not in seen]
        if cap > 0:
            batch = batch[:cap - len(saved)]
        seen.update(batch)
        next_queue = []
        with ThreadPoolExecutor(max_workers=threads) as pool:
            for f in as_completed([pool.submit(fetch, u) for u in batch]):
                u, body = f.result()
                if body is None:
                    continue
                name = hashlib.sha256(u.encode()).hexdigest()[:16] + ".js"
                try:
                    (chunks / name).write_bytes(body)
                except Exception:  # noqa: BLE001
                    continue
                saved.append(u)
                # Follow chunk references discovered inside this chunk.
                text = body.decode("utf-8", "replace")
                for ref in JS_REF_RE.findall(text):
                    abs_ref = _resolve_js_ref(ref, u)
                    if (abs_ref and JS_RE.search(abs_ref) and abs_ref not in seen
                            and abs_ref not in next_queue):
                        next_queue.append(abs_ref)
        queue = next_queue
        log(f"JS round {rnd + 1}: {len(saved)} chunks saved, {len(queue)} new references")

    (target_dir / "js_urls.txt").write_text("\n".join(sorted(set(saved))) + "\n", encoding="utf-8")
    record_status("js-download", 0, f"{len(saved)} chunks saved over {rounds} round(s)")
    log(f"JS chunks downloaded: {len(saved)} total")
    return saved


def step_jsluice(target_dir, logs, settings):
    if not settings.get("enable_jsluice", True):
        return
    js = sorted((target_dir / "chunks").glob("*.js")) if (target_dir / "chunks").exists() else []
    out = target_dir / "jsluice.jsonl"
    secrets = target_dir / "jsluice_secrets.jsonl"
    batch = int(settings.get("jsluice_batch", 100))
    # ONE process per batch instead of two per file: 10-50x faster.
    with open(out, "w", encoding="utf-8") as fo, open(secrets, "w", encoding="utf-8") as fs:
        for i in range(0, len(js), batch):
            group = [str(p) for p in js[i:i + batch]]
            try:
                r = subprocess.run(["jsluice", "urls", *group], capture_output=True, timeout=600)
                fo.write((r.stdout or b"").decode("utf-8", "replace"))
            except Exception:  # noqa: BLE001
                pass
            try:
                r = subprocess.run(["jsluice", "secrets", *group], capture_output=True, timeout=600)
                fs.write((r.stdout or b"").decode("utf-8", "replace"))
            except Exception:  # noqa: BLE001
                pass
    record_status("jsluice", 0, f"{len(js)} files parsed in batches of {batch}")
    log(f"jsluice: parsed {len(js)} chunks (batched)")


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
    target_dir, logs = Path(target_dir), Path(logs)
    out = target_dir / "anastasis.json"
    # Anastasis runs from its own directory via the PATH wrapper, so a relative
    # --save path lands in the tool folder. Always pass an absolute path.
    save_path = str(out.resolve())
    chunks = target_dir / "chunks"
    have_chunks = chunks.exists() and any(chunks.glob("*.js"))

    def load_raw(logfile):
        if out.exists():
            txt = out.read_text(encoding="utf-8", errors="replace")
            if txt.strip():
                return txt
        try:
            txt = logfile.read_text(encoding="utf-8", errors="replace")
            s, e = txt.find("{"), txt.rfind("}")
            if s >= 0 and e > s:
                cand = txt[s:e + 1]
                json.loads(cand)
                out.write_text(cand, encoding="utf-8")
                return cand
        except Exception:  # noqa: BLE001
            pass
        return ""

    def parse(raw):
        u, ep, pa = [], [], []
        try:
            _walk_anastasis(json.loads(raw), u, ep, pa)
        except Exception:  # noqa: BLE001
            pass
        return u, ep, pa

    # LOCAL-FIRST: parse the chunks we already downloaded (deterministic, fast,
    # no flaky network sources). Fall back to remote discovery only if empty.
    urls, endpoints, params = [], [], []
    rc = 1
    if have_chunks:
        rc = run(["anastasis", "-fs", str(chunks.resolve()), "--params", "-o", "json",
                  "--save", save_path], logs / "anastasis_local.log", timeout=3600)
        urls, endpoints, params = parse(load_raw(logs / "anastasis_local.log"))
    if not endpoints:
        rc = run(["anastasis", "-u", host, "--params", "-o", "json", "--save", save_path],
                 logs / "anastasis.log", timeout=3600)
        urls, endpoints, params = parse(load_raw(logs / "anastasis.log"))
    if not endpoints:
        record_status("anastasis", rc if rc else 1, "no endpoints from local or remote mode")
        return

    # Write full URLs so these endpoints enter the route pool and get probed.
    prefix = base.rstrip("/")
    full = set()
    for item in urls:
        parts = item.split(" ", 1)
        if len(parts) == 2:
            full.add(prefix + parts[1])
    (target_dir / "anastasis_urls.txt").write_text("\n".join(sorted(full)) + "\n", encoding="utf-8")
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


def step_noseyparker(target_dir, logs):
    """Rust GB/s secret scan over downloaded chunks (complements trufflehog)."""
    if not settings_enabled("enable_noseyparker") or not which("noseyparker"):
        return
    src = target_dir / "chunks"
    if not src.exists() or not any(src.glob("*.js")):
        record_status("noseyparker", 0, "no chunks")
        return
    ds = target_dir / "np-datastore"
    run(["noseyparker", "scan", "--datastore", str(ds), str(src)],
        logs / "noseyparker_scan.log", timeout=1800)
    run_capture(["noseyparker", "report", "--datastore", str(ds), "--format", "jsonl"],
                target_dir / "noseyparker.jsonl", logs / "noseyparker.log", timeout=600)


def step_nuclei(probe_rows, target_dir, logs, settings):
    """Curated fast nuclei templates on VERIFIED-LIVE hosts only -> real findings."""
    if not settings_enabled("enable_nuclei") or not which("nuclei"):
        return []
    live = {}
    for r in probe_rows:
        if (r.get("status_code") or 0) in (200, 401, 403):
            u = r.get("url")
            if u:
                live[u] = True
    urls = list(live)[:int(settings.get("nuclei_max_targets", 300))]
    if not urls:
        record_status("nuclei", 0, "no live hosts")
        return []
    lst = target_dir / "nuclei_urls.txt"
    lst.write_text("\n".join(urls) + "\n", encoding="utf-8")
    out = target_dir / "nuclei.jsonl"
    run(["nuclei", "-l", str(lst), "-tags", "exposure,misconfig,tech,panel",
         "-rl", "50", "-c", "25", "-jsonl", "-o", str(out), "-silent", "-duc",
         "-timeout", "10", "-retries", "1"],
        logs / "nuclei.log", timeout=1800)
    rows = read_jsonl(out)
    record_status("nuclei", 0, f"{len(rows)} findings on {len(urls)} live hosts")
    log(f"nuclei: {len(rows)} findings")
    return rows


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
    rows_out = read_jsonl(out)

    # Rate-limit recovery: retry 429s gently. No URLs are removed — this only
    # gives blocked-by-rate-limit URLs a second chance to return a real status.
    limited = [r for r in rows_out if (r.get("status_code") or r.get("status")) == 429]
    if limited:
        retry_urls = target_dir / "probe_retry_urls.txt"
        retry_urls.write_text("\n".join(str(r["url"]) for r in limited if r.get("url")) + "\n", encoding="utf-8")
        retry_out = target_dir / "probe_retry.jsonl"
        run(["httpx", "-l", str(retry_urls), "-mc", ALL_CODES, "-sc", "-cl", "-ct",
             "-title", "-td", "-j", "-o", str(retry_out), "-silent",
             "-timeout", str(settings.get("request_timeout", 20)), "-retries", "2",
             "-rl", "10", "-threads", "10"],
            logs / "httpx_retry.log", timeout=3600)
        fixed = read_jsonl(retry_out)
        by_key = {}
        for r in fixed:
            if r.get("url"):
                by_key[dedupe_key(str(r["url"]))] = r
        final = []
        for r in rows_out:
            k = dedupe_key(str(r.get("url", "")))
            repl = by_key.get(k)
            if repl and (repl.get("status_code") or 0) != 429:
                final.append(repl)
                by_key.pop(k, None)
            else:
                final.append(r)
        final.extend(by_key.values())
        write_jsonl(out, final)
        log(f"httpx rate-limit retry: {len(limited)} retried, "
            f"{sum(1 for r in final if (r.get('status_code') or 0) not in (429, 0))} recovered")
        rows_out = final
    return rows_out


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


def push_target_results(target_dir: Path, base: str):
    """Commit and push ONE target's results immediately, so later URLs never
    hold up earlier findings. Called from the runner where git credentials
    are already configured by actions/checkout."""
    host = urlparse(base).netloc.replace(":", "_")
    rel = f"results/{host}"
    try:
        subprocess.run(["git", "config", "user.name", "hunt-bot"],
                       capture_output=True, check=False)
        subprocess.run(["git", "config", "user.email", "hunt-bot@users.noreply.github.com"],
                       capture_output=True, check=False)
        # Stage only this target's files; skip heavy chunk/source-map dirs.
        proc = subprocess.run(
            ["bash", "-c",
             f"find {rel} -type f ! -path '*/chunks/*' ! -path '*/sourcemaps/*' -print0 "
             "| xargs -0 -r git add -f"],
            capture_output=True, check=False,
        )
        if proc.returncode != 0:
            log(f"result push: staging failed for {host}: {proc.stderr.decode('utf-8', 'replace')[:300]}")
            return
        staged = subprocess.run(["git", "diff", "--cached", "--quiet"],
                                capture_output=True, check=False)
        if staged.returncode == 0:
            log(f"result push: no new changes for {host}")
            return
        msg = f"Hunt results {host} {now()}"
        commit = subprocess.run(["git", "commit", "-m", msg],
                                capture_output=True, check=False)
        if commit.returncode != 0:
            log(f"result push: commit failed: {commit.stderr.decode('utf-8', 'replace')[:300]}")
            return
        # Retry with rebase: parallel jobs / user edits can move the remote.
        for attempt in range(4):
            push = subprocess.run(["git", "push"], capture_output=True, check=False)
            if push.returncode == 0:
                log(f"result push: pushed {rel} immediately")
                return
            log(f"result push: rejected (attempt {attempt + 1}), rebasing")
            subprocess.run(["git", "pull", "--rebase", "origin", "main"],
                           capture_output=True, check=False)
        log("result push: gave up after retries; final workflow step will retry")
    except Exception as e:  # noqa: BLE001
        log(f"result push: error for {host}: {e}")


# ---------------------------------------------------------------------------
# report
# ---------------------------------------------------------------------------

def report(target_dir, base, routes, probe_rows, extra_rows, settings, nuclei_rows=None):
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

    # Distinct-route view: one row per URL. Method-probe responses are kept
    # separately so 405/403 noise never inflates the "exists but blocked" count.
    distinct = {}
    for r in list(probe_rows) + list(extra_rows):
        u = r.get("url")
        if not u:
            continue
        k = dedupe_key(u)
        cur = distinct.get(k)
        if cur is None or (cur.get("source") == "method" and r.get("source") != "method"):
            distinct[k] = dict(r)

    win, blocked, other = [], [], []
    for r in distinct.values():
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

    # Noise is KEPT, just placed in its own files. Nothing is deleted.
    apex = clean_host(urlparse(base).netloc)
    first_party, third_party = [], []
    for r in all_routes:
        h = clean_host(urlparse(r["url"]).netloc)
        (first_party if h == apex or h.endswith("." + apex) else third_party).append(r)
    write_jsonl(target_dir / "third_party_routes.jsonl", third_party)
    method_rows = [r for r in extra_rows if r.get("source") == "method"]
    write_jsonl(target_dir / "method_responses.jsonl", method_rows)

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
    all_vhosts = read_jsonl(target_dir / "vhost.jsonl")
    vhosts = [v for v in all_vhosts if v.get("status_code") in (VHOST_REAL - {403})]
    vhost_noise = [v for v in all_vhosts if v not in vhosts]
    write_jsonl(target_dir / "vhost_real.jsonl", vhosts)
    write_jsonl(target_dir / "vhost_blocked.jsonl", vhost_noise)
    secrets = [l for l in (target_dir / "secrets.jsonl").read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()] if (target_dir / "secrets.jsonl").exists() else []

    write_jsonl(target_dir / "all_routes.jsonl", all_routes)
    write_jsonl(target_dir / "accessible_200.jsonl", win)
    write_jsonl(target_dir / "exists_blocked.jsonl", blocked)
    write_jsonl(target_dir / "other_status.jsonl", other)
    write_jsonl(target_dir / "data_files.jsonl", data_files)
    write_jsonl(target_dir / "params.jsonl", params)
    write_jsonl(target_dir / "subdomains.jsonl", sub_rows)
    write_jsonl(target_dir / "js_endpoints.jsonl", js_endpoints)
    nuclei = list(nuclei_rows or [])
    write_jsonl(target_dir / "nuclei.jsonl", nuclei)

    # Collapse repeated ID-like path segments so the report leads with structure,
    # not thousands of near-identical artifact/session URLs. Raw data stays intact.
    import re as _re
    from collections import Counter as _Counter
    id_seg = _re.compile(r"^([0-9a-f]{8,}|[0-9a-f-]{36}|[A-Za-z0-9_-]{20,}|\d+)$")
    pat = _Counter()
    for r in all_routes:
        segs = [s for s in urlparse(r["url"]).path.split("/") if s]
        collapsed = "/".join("{id}" if id_seg.match(s) else s for s in segs)
        pat["/" + collapsed] += 1
    top_patterns = pat.most_common(40)
    write_jsonl(target_dir / "live_200.jsonl", win)
    write_jsonl(target_dir / "live_other.jsonl", blocked)

    elapsed = int(time.time() - RUN_START)
    L = [f"# Hunt Report — {base}", "",
         f"Generated: {now()} &nbsp;|&nbsp; Duration: {elapsed // 60}m {elapsed % 60}s", "",
         "> **Nothing is filtered during collection. This report is only a grouping.**", "",
         "## Summary", "", "| What | Count | Meaning |", "|---|---:|---|",
         f"| Routes collected | {len(all_routes)} | Every URL found, nothing removed |",
         f"| Distinct routes verified | {len(distinct)} | One row per URL (method probes excluded) |",
         f"| HTTP responses | {len(merged)} | Includes method probes — kept in `method_responses.jsonl` |",
         f"| **Accessible (200)** | **{len(win)}** | Confirmed live — the wins |",
         f"| Exists but different status | {len(blocked)} | 301/302/401/403/405 — real route, blocked |",
         f"| Other responses | {len(other)} | 404/500/etc — kept, not discarded |",
         f"| Subdomains (resolved) | {len(live_subs)} | DNS-verified |",
         f"| Virtual hosts (real) | {len(vhosts)} | Cloudflare 403/530/0 excluded |",
         f"| Parameters | {len(params)} | URLs with query params |",
         f"| JS endpoints (AST) | {len(js_endpoints)} | anastasis evidence-backed |",
         f"| First-party URLs | {len(first_party)} | {apex} and subdomains |",
         f"| Third-party URLs | {len(third_party)} | kept in `third_party_routes.jsonl` |",
         f"| Method responses | {len(method_rows)} | kept in `method_responses.jsonl` |",
         f"| Blocked vhost checks | {len(vhost_noise)} | kept in `vhost_blocked.jsonl` |",
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

    L.append(f"> Collection keeps third-party URLs by design ({len(third_party)}). "
             f"See `third_party_routes.jsonl`. Method-probe responses are in `method_responses.jsonl`.")
    L.append("")
    L += ["## 0. TOP ROUTE PATTERNS (IDs collapsed)", "",
          "| Pattern | Count |", "|---|---:|"]
    for p, c in top_patterns:
        L.append(f"| `{p}` | {c} |")
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
        L.append("_No non-blocked virtual hosts found._")
    L.append(f"Blocked/noisy vhost checks (403/530/0) are kept in `vhost_blocked.jsonl` ({len(vhost_noise)}).")
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

    L += ["## 10. NUCLEI FINDINGS (verified exposures / misconfigs)", ""]
    if nuclei:
        L += ["| Severity | Template | Host |", "|---|---|---|"]
        for n in nuclei[:80]:
            info = n.get("info", {}) or {}
            L.append(f"| {info.get('severity','?')} | `{n.get('template-id','?')}` | `{n.get('host','')}` |")
        if len(nuclei) > 80:
            L.append(f"| … | _{len(nuclei)-80} more in nuclei.jsonl_ | |")
    else:
        L.append("_No nuclei findings on live hosts._")
    L.append("")

    L += ["## 11. TOOL RUN STATUS (no silent skips)", "", "| Tool | Result | Detail |", "|---|---|---|"]
    for name in sorted(RUN_STATUS):
        s = RUN_STATUS[name]
        L.append(f"| `{name}` | {'OK' if s['exit'] == 0 else 'exit ' + str(s['exit'])} | {s.get('note') or ('see logs/' if s['exit'] else 'completed')} |")
    L.append("")

    L += ["## 12. INTENTIONALLY NOT RUN", "",
          "- **ffuf path brute** — off by default; `wordlist.txt` is ready. Set `enable_brute: true` later.",
          "- **kiterunner** — off by default alongside ffuf.", ""]

    out_files = [
        ("REPORT.md", "this report"), ("all_routes.jsonl", "every route, unfiltered"),
        ("accessible_200.jsonl", "HTTP 200 wins"), ("exists_blocked.jsonl", "exists but blocked"),
        ("other_status.jsonl", "all other statuses"), ("data_files.jsonl", "JSON/CSV/XML among 200s"),
        ("params.jsonl", "parameters"), ("subdomains.jsonl", "subdomains + resolution"),
        ("third_party_routes.jsonl", "third-party URLs — kept, not deleted"),
        ("method_responses.jsonl", "all method-probe responses — kept"),
        ("vhost_real.jsonl", "non-blocked virtual hosts"),
        ("vhost_blocked.jsonl", "blocked vhost checks — kept"),
        ("js_endpoints.jsonl", "AST endpoints"), ("vhost.jsonl", "all vhost checks"),
        ("jsluice.jsonl", "JS-derived URLs"), ("cariddi.txt", "crawl + secrets/endpoints"),
        ("wayback_urls.txt", "archive URLs"), ("noseyparker.jsonl", "fast secret scan"),
        ("nuclei.jsonl", "verified exposure findings"), ("anastasis_endpoints.jsonl", "AST endpoints"),
        ("jscope.txt", "evidence-ranked JS analysis"), ("secrets.jsonl", "secret candidates"),
        ("wordlist.txt", "target-specific fuzz list"), ("params.txt", "parameter wordlist"),
        ("context.json", "shared context"), ("js_urls.txt", "JS chunk URLs"),
        ("logs/", "raw tool logs"),
    ]
    L += ["## 13. OUTPUT FILES", "", "| File | Meaning |", "|---|---|"]
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
            "js_endpoints": len(js_endpoints), "vhosts": len(vhosts), "nuclei": len(nuclei)}


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

SETTINGS = {}


def main() -> int:
    global SETTINGS
    ap = argparse.ArgumentParser()
    ap.add_argument("--urls", default="urls.txt")
    ap.add_argument("--url", default="", help="single target (matrix mode)")
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

    raw_urls = ([args.url] if args.url else
                [l.strip() for l in Path(args.urls).read_text(encoding="utf-8").splitlines()
                 if l.strip() and not l.strip().startswith("#")])
    if not raw_urls:
        log("no targets")
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
        probe_rows, extra, nuclei_rows, routes = [], [], [], {}
        try:
            step("subdomains", step_subdomains, host, td, logs, SETTINGS)
            step("urlfinder", step_urlfinder, host, td, logs, SETTINGS)
            step("waybackurls", step_waybackurls, host, td, logs, SETTINGS)
            step("katana", step_katana, base, td, logs, SETTINGS)
            step("cariddi", step_cariddi, base, td, logs, SETTINGS)
            step("js-seeds", step_js_seeds, base, td, logs, SETTINGS)
            step("js-download", step_download_js, td, logs, SETTINGS)
            step("jsluice", step_jsluice, td, logs, SETTINGS)
            step("anastasis", step_anastasis, host, base, td, logs)
            step("jscope", step_jscope, td, logs)
            step("trufflehog", step_trufflehog, td, logs)
            step("noseyparker", step_noseyparker, td, logs)

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
            nuclei_rows = step("nuclei", step_nuclei, probe_rows, td, logs, SETTINGS) or []

            if SETTINGS.get("enable_brute", False):
                log("ffuf brute enabled (wordlist ready)")
            else:
                record_status("ffuf", 0, "off by choice — wordlist prepared")
        except Exception as e:  # noqa: BLE001
            # One bad target must never kill the others or lose partial data.
            log(f"TARGET {base} partial failure: {e}")
            record_status("pipeline", 1, str(e))

        stats = report(td, base, routes, probe_rows, extra, SETTINGS, nuclei_rows)
        write_context(td, base, routes, stats)
        if SETTINGS.get("enable_result_push", True):
            push_target_results(td, base)
        summary.append((base, stats))
        log(f"REPORT {td / 'REPORT.md'} -> {stats}")

    # INDEX.md / SUMMARY.md are built by the aggregate workflow job
    # (scripts/make_index.py) so parallel per-URL jobs never race on them.
    log("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
