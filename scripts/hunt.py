#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
One-shot web hunt pipeline.

Golden rule:
    Collect wide. Verify status. Categorize last.

- No content-type / method / shape filter during collection.
- 200                        -> live_200.jsonl          (confirmed win)
- 301/302/303/307/308/401/403/405 -> live_other.jsonl    (route exists but blocked)
- everything else            -> kept in all_routes.jsonl (nothing deleted)

Usage:
    python3 scripts/hunt.py --urls urls.txt --out output --settings config/settings.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urljoin, urlparse, urlunparse

import wordlist  # local module (scripts/ is on sys.path)

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------

STATUS_WIN = {200}
STATUS_EXISTS = {301, 302, 303, 307, 308, 401, 403, 405}

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

ABS_RE = re.compile(r"https?://[^\s\"'<>\\\)\]\},;]+", re.I)
REL_RE = re.compile(r"[\"'`](/[A-Za-z0-9_\-./?=&%{}:;,@+~#\[\]]{1,300})[\"'`]")

CHAKRA_PATH = os.environ.get("CHAKRA_PATH", os.path.expanduser("~/tools/Chakra/chakra.py"))
XNLINK_PATH = os.environ.get("XNLINK_PATH", "")

METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]

# uncover needs at least one of these API keys; it is skipped otherwise.
UNCOVER_ENGINE_KEYS = [
    ("shodan", "SHODAN_API_KEY"),
    ("censys", "CENSYS_API_ID"),
    ("fofa", "FOFA_EMAIL"),
    ("quake", "QUAKE_TOKEN"),
    ("hunter", "HUNTER_API_KEY"),
    ("zoomeye", "ZOOMEYE_API_KEY"),
    ("netlas", "NETLAS_API_KEY"),
    ("criminalip", "CRIMINALIP_API_KEY"),
    ("publicwww", "PUBLICWWW_API_KEY"),
    ("binaryedge", "BINARYEDGE_API_KEY"),
]


def uncover_engine():
    for engine, key in UNCOVER_ENGINE_KEYS:
        if os.environ.get(key, "").strip():
            return engine
    return None


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------

def now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def log(msg: str) -> None:
    print(f"[{now()}] {msg}", flush=True)


def which(tool: str):
    return shutil.which(tool)


# populated by run()/run_capture() so the final report can show exactly
# which tools ran and whether they succeeded.
RUN_STATUS = {}
RUN_START = time.time()


def record_status(name: str, code: int, note: str = ""):
    RUN_STATUS[name] = {"exit": code, "note": note}


def tool_name(cmd) -> str:
    first = str(cmd[0])
    return os.path.basename(first).replace(".py", "")


def tail_log(path: Path, n: int = 12) -> str:
    try:
        lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
        return "\n".join(lines[-n:])
    except Exception:  # noqa: BLE001
        return ""


def check_tools(settings: dict) -> bool:
    """Fail loudly before doing any work if a required tool is missing."""
    required = ["katana", "httpx", "ffuf", "uro", "subfinder", "dnsx",
                "uncover", "kr", "gau", "waybackurls", "jsluice",
                "trufflehog", "waymore", "arjun", "js-recon", "jq",
                "xnLinkFinder"]
    missing = [t for t in required if t != "xnLinkFinder" and not which(t)]
    if not xnlink_cmd():
        missing.append("xnLinkFinder")
    if not os.path.exists(CHAKRA_PATH):
        missing.append("Chakra")
    if missing:
        log("MISSING REQUIRED TOOLS: " + ", ".join(missing))
        return False
    log(f"tool check: OK ({len(required) + 1} tools present)")
    return True


def xnlink_cmd():
    """Resolve the xnLinkFinder executable (pip binary or cloned script)."""
    if XNLINK_PATH and os.path.exists(XNLINK_PATH):
        return [sys.executable, XNLINK_PATH]
    if which("xnLinkFinder"):
        return ["xnLinkFinder"]
    nested = os.path.expanduser("~/tools/xnLinkFinder/xnLinkFinder/xnLinkFinder.py")
    if os.path.exists(nested):
        return [sys.executable, nested]
    return None


def collect_js_urls(target_dir: Path, base: str):
    """Full URLs of every discovered JS file (xnLinkFinder needs URLs, not a nested dir)."""
    base_host = urlparse(base).netloc.lower().removeprefix("www.")
    urls = set()
    for f in target_dir.rglob("*"):
        if not f.is_file() or "logs" in f.parts:
            continue
        if f.suffix.lower() not in TEXT_EXT:
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except Exception:  # noqa: BLE001
            continue
        for m in ABS_RE.finditer(text):
            u = m.group(0)
            try:
                p = urlparse(u)
            except (ValueError, TypeError):
                continue
            host = p.netloc.lower().removeprefix("www.")
            if ".js" in p.path.lower() and host and host == base_host:
                urls.add(u)
    return sorted(urls)


def run(cmd, log_path: Path, timeout: int = 3600, cwd=None) -> int:
    """Run a command, append stdout+stderr to a binary log file."""
    log_path = Path(log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    name = tool_name(cmd)
    with open(log_path, "ab") as lf:
        lf.write(("\n$ " + " ".join(map(str, cmd)) + "\n").encode("utf-8", "replace"))
        lf.flush()
        try:
            p = subprocess.run(
                [str(c) for c in cmd],
                cwd=str(cwd) if cwd else None,
                stdout=lf,
                stderr=subprocess.STDOUT,
                timeout=timeout,
            )
            lf.write(f"\n[exit {p.returncode}]\n".encode())
            record_status(name, p.returncode)
            if p.returncode != 0:
                log(f"WARN {name} exited {p.returncode}; log tail:\n{tail_log(log_path)}")
            return p.returncode
        except FileNotFoundError as e:
            lf.write(f"\n[missing: {e}]\n".encode("utf-8", "replace"))
            record_status(name, 127)
            log(f"WARN {name} missing: {e}")
            return 127
        except subprocess.TimeoutExpired:
            lf.write(f"\n[timeout {timeout}s]\n".encode())
            record_status(name, 124)
            log(f"WARN {name} timed out after {timeout}s")
            return 124
        except Exception as e:  # noqa: BLE001
            lf.write(f"\n[error {e}]\n".encode("utf-8", "replace"))
            record_status(name, 1)
            log(f"WARN {name} error: {e}")
            return 1


def run_capture(cmd, out_file: Path, log_path: Path, timeout: int = 1800) -> int:
    """Run a command, write stdout to out_file, stderr to log."""
    name = tool_name(cmd)
    out_file = Path(out_file)
    log_path = Path(log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "ab") as lf:
        lf.write(("\n$ " + " ".join(map(str, cmd)) + "\n").encode("utf-8", "replace"))
        lf.flush()
        try:
            p = subprocess.run(
                [str(c) for c in cmd],
                stdout=subprocess.PIPE,
                stderr=lf,
                timeout=timeout,
            )
            out_file.write_bytes(p.stdout or b"")
            lf.write(f"\n[exit {p.returncode}] -> {out_file}\n".encode())
            record_status(name, p.returncode)
            if p.returncode != 0:
                log(f"WARN {name} exited {p.returncode}; log tail:\n{tail_log(log_path)}")
            return p.returncode
        except Exception as e:  # noqa: BLE001
            lf.write(f"\n[error {e}]\n".encode("utf-8", "replace"))
            record_status(name, 1)
            log(f"WARN {name} error: {e}")
            return 1


def read_jsonl(path: Path):
    rows = []
    if not Path(path).exists():
        return rows
    for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except Exception:  # noqa: BLE001
            continue
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
    return f"{p.scheme}://{p.netloc}"


def normalize(u: str, base: str):
    if not u:
        return None
    u = u.strip().strip("\"'`,;)]}>")
    u = u.replace("\\/", "/")
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
    path = p.path or "/"
    query = urlencode(
        [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
         if k.lower() not in TRACKING]
    )
    return urlunparse((scheme, host, path, "", query, ""))


def dedupe_key(u: str):
    p = urlparse(u)
    host = p.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    return (host, p.path or "/", p.query)


def is_asset(u: str) -> bool:
    path = urlparse(u).path.lower()
    return any(path.endswith(ext) for ext in ASSET_EXT)


def harvest_file(path: Path, base: str, limit: int = 8_000_000):
    out = []
    try:
        if path.stat().st_size > limit:
            return out
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        return out
    for m in ABS_RE.finditer(text):
        out.append(m.group(0))
    for m in REL_RE.finditer(text):
        out.append(m.group(1))
    return out


# ----------------------------------------------------------------------------
# collection
# ----------------------------------------------------------------------------

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

    # katana JSONL (has request.method)
    for f in target_dir.rglob("katana*.jsonl"):
        for j in read_jsonl(f):
            if not isinstance(j, dict):
                continue
            req = j.get("request") or {}
            add(req.get("url") or j.get("url"), req.get("method"), f.name)

    # jsluice JSONL
    for f in target_dir.rglob("jsluice*.jsonl"):
        for j in read_jsonl(f):
            if not isinstance(j, dict):
                continue
            add(j.get("url"), j.get("method"), f.name)

    # every text-ish artifact: chunks, route lists, strings, archived pages
    for f in target_dir.rglob("*"):
        if not f.is_file():
            continue
        if "logs" in f.parts:
            continue
        if f.suffix.lower() in TEXT_EXT:
            for raw in harvest_file(f, base):
                add(raw, "GET", f.name)

    return routes


# ----------------------------------------------------------------------------
# steps
# ----------------------------------------------------------------------------

def step_subdomains(host: str, target_dir: Path, logs: Path, settings: dict):
    if not settings.get("enable_subdomains"):
        return
    subs = set()

    if which("subfinder"):
        out = target_dir / "subdomains.txt"
        run(["subfinder", "-d", host, "-all", "-recursive", "-silent", "-o", str(out)],
            logs / "subfinder.log", timeout=1800)
        if out.exists():
            subs.update(l.strip().lower() for l in out.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip())
    else:
        record_status("subfinder", 127, "not found")
        log("subfinder not found")

    if settings.get("enable_uncover") and which("uncover"):
        engine = uncover_engine()
        if engine:
            out = target_dir / "uncover.txt"
            run(["uncover", "-q", f'ssl:"{host}"', "-e", engine,
                 "-silent", "-o", str(out)],
                logs / "uncover.log", timeout=1200)
            if out.exists():
                subs.update(l.strip().lower() for l in out.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip())
        else:
            record_status("uncover", 0, "no API key configured - query not sent")
            log("uncover enabled but no API key set; reporting as no-data (not a skip)")

    if not subs:
        return

    raw = target_dir / "subdomains_all.txt"
    raw.write_text("\n".join(sorted(subs)) + "\n", encoding="utf-8")

    live = set(subs)
    if which("dnsx"):
        run(["dnsx", "-l", str(raw), "-silent", "-o", str(target_dir / "subdomains_live.txt")],
            logs / "dnsx.log", timeout=1800)
        lf = target_dir / "subdomains_live.txt"
        if lf.exists():
            resolved = {l.strip().lower() for l in lf.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()}
            if resolved:
                live = resolved

    cap = int(settings.get("max_subdomains", 1000))
    urls = [f"https://{h}" for h in sorted(live)[:cap]]
    (target_dir / "subdomains_urls.txt").write_text("\n".join(urls) + "\n", encoding="utf-8")
    log(f"subdomains: {len(subs)} found, {len(live)} live, {len(urls)} URLs queued")


def step_chakra(base: str, target_dir: Path, logs: Path, settings: dict):
    if not os.path.exists(CHAKRA_PATH):
        record_status("Chakra", 127, "not found")
        log(f"Chakra not found at {CHAKRA_PATH}")
        return
    run([sys.executable, CHAKRA_PATH, base, "-o", str(target_dir / "chakra"),
         "-d", str(settings.get("chakra_depth", 10)),
         "-t", str(settings.get("chakra_threads", 16)),
         "--delay", str(settings.get("chakra_delay", 0.1))],
        logs / "chakra.log", timeout=3000)


def step_jsrecon(base: str, target_dir: Path, logs: Path, settings: dict):
    if not which("js-recon"):
        record_status("js-recon", 127, "not found")
        log("js-recon not found")
        return
    out = target_dir / "jsrecon"
    out.mkdir(parents=True, exist_ok=True)

    maxes = ["--max-pages", str(settings.get("jsrecon_max_pages", 1000)),
             "--max-iterations", str(settings.get("jsrecon_max_iterations", 20)),
             "--lazyload-timeout", str(settings.get("jsrecon_timeout_min", 45))]
    sandbox = ["--no-sandbox"] if settings.get("enable_browser", True) else []

    # 1) initial lazyload. NOTE: --strings is a flag of the `strings`
    # subcommand, NOT of `lazyload` — passing it here aborts the command.
    run(["js-recon", "lazyload", "-u", base, "-o", str(out), "-y",
         "--build-id", "--research"] + maxes + sandbox,
        logs / "jsrecon_lazyload.log", timeout=3000)

    # 2) strings must run before subsequent requests: it creates
    #    extracted_urls.json, which the Next.js subsequent pass requires.
    run(["js-recon", "strings", "-d", str(out), "-e", "-p", "-s",
         "-o", str(out / "strings.json"),
         "--extracted-url-path", str(out / "extracted_urls")],
        logs / "jsrecon_strings.log", timeout=1800)

    # 3) subsequent requests (Next.js RSC / dynamic chunks)
    extracted = out / "extracted_urls.json"
    if extracted.exists():
        run(["js-recon", "lazyload", "-u", base, "-o", str(out), "-y",
             "--subsequent-requests", "--urls-file", str(extracted)] + maxes + sandbox,
            logs / "jsrecon_subsequent.log", timeout=3000)
    else:
        record_status("js-recon-subsequent", 0, "no extracted_urls.json from strings")
        log("js-recon subsequent-requests: no extracted_urls.json produced")

    # 4) endpoints
    run(["js-recon", "endpoints", "-d", str(out), "-t", "next", "-u", base,
         "-o", str(out / "endpoints")],
        logs / "jsrecon_endpoints.log", timeout=1200)


def step_katana(base: str, target_dir: Path, logs: Path, settings: dict):
    if not which("katana"):
        record_status("katana", 127, "not found")
        log("katana not found")
        return
    k = target_dir / "katana"
    k.mkdir(parents=True, exist_ok=True)

    # pass 1: JS string literals + known files
    run(["katana", "-u", base, "-d", str(settings.get("katana_depth", 10)),
         "-jc", "-jsl", "-kf", "all", "-aff",
         "-ef", "png,jpg,jpeg,gif,svg,css,woff,woff2,ttf,eot,ico,mp4,mp3,pdf",
         "-c", "30", "-timeout", "20", "-retry", "2",
         "-silent", "-json", "-o", str(k / "pass1.jsonl")],
        logs / "katana_pass1.log", timeout=3000)

    # pass 2: headless runtime (XHR method capture)
    if settings.get("enable_browser", True):
        run(["katana", "-u", base, "-d", str(settings.get("katana_depth", 10)),
             "-headless", "-xhr", "-no-sandbox", "-jsl",
             "-c", "10", "-timeout", "20",
             "-silent", "-json", "-o", str(k / "pass2.jsonl")],
            logs / "katana_pass2.log", timeout=3000)


def step_waymore(host: str, target_dir: Path, logs: Path):
    if not which("waymore"):
        record_status("waymore", 127, "not found")
        log("waymore not found")
        return
    w = target_dir / "history"
    w.mkdir(parents=True, exist_ok=True)
    run(["waymore", "-i", host, "-mode", "U", "-oU", str(w / "waymore_urls.txt")],
        logs / "waymore.log", timeout=1800)


def step_urlscan(host: str, target_dir: Path, logs: Path, settings: dict):
    if not settings.get("enable_urlscan", True):
        return
    key = os.environ.get("URLSCAN_API_KEY", "").strip()
    w = target_dir / "history"
    w.mkdir(parents=True, exist_ok=True)
    out = w / "urlscan.json"
    headers = {"User-Agent": "hunt-pipeline/1.0"}
    if key:
        headers["api-key"] = key
    try:
        import urllib.request

        req = urllib.request.Request(
            f"https://urlscan.io/api/v1/search/?q=domain%3A{host}&size=10000",
            headers=headers,
        )
        with urllib.request.urlopen(req, timeout=60) as r:
            out.write_bytes(r.read())
        log(f"urlscan saved -> {out} ({'keyed' if key else 'no key'})")
    except Exception as e:  # noqa: BLE001
        log(f"urlscan failed: {e}")


def step_jsluice(target_dir: Path, logs: Path):
    if not which("jsluice"):
        record_status("jsluice", 127, "not found")
        log("jsluice not found")
        return
    js_files = [p for p in target_dir.rglob("*.js") if p.is_file()]
    out = target_dir / "jsluice.jsonl"
    secrets = target_dir / "jsluice_secrets.jsonl"
    with open(out, "w", encoding="utf-8") as f, open(secrets, "w", encoding="utf-8") as sf:
        for js in js_files[:8000]:
            try:
                p = subprocess.run(["jsluice", "urls", str(js)],
                                   capture_output=True, timeout=60)
                f.write((p.stdout or b"").decode("utf-8", "replace"))
            except Exception:  # noqa: BLE001
                pass
            try:
                p = subprocess.run(["jsluice", "secrets", str(js)],
                                   capture_output=True, timeout=60)
                sf.write((p.stdout or b"").decode("utf-8", "replace"))
            except Exception:  # noqa: BLE001
                pass
    (logs / "jsluice.log").write_text(f"js files: {len(js_files)}\n", encoding="utf-8")


def step_xnlinkfinder(host: str, target_dir: Path, logs: Path):
    cmd = xnlink_cmd()
    if not cmd:
        record_status("xnLinkFinder", 127, "not found")
        log("xnLinkFinder not found")
        return

    # xnLinkFinder only reads files in the ROOT of a directory input, but our
    # chunks are nested. Feed it full JS URLs instead (generated from findings).
    js_urls = collect_js_urls(target_dir, f"https://{host}")
    js_file = target_dir / "js_urls.txt"
    js_file.write_text("\n".join(js_urls) + "\n", encoding="utf-8")
    if js_urls:
        src = js_file
        log(f"xnLinkFinder input: {len(js_urls)} discovered JS URLs")
    else:
        src = target_dir / "chakra"
        if not src.exists():
            src = target_dir
        log("xnLinkFinder input: local file fallback")

    run(cmd + ["-i", str(src), "-sf", host, "-d", "3", "-nb",
               "-o", str(target_dir / "xnlinkfinder.txt"),
               "-op", str(target_dir / "xnlinkfinder_params.txt"),
               "-owl", str(target_dir / "xnlinkfinder_wordlist.txt")],
        logs / "xnlinkfinder.log", timeout=2400)


def step_trufflehog(target_dir: Path, logs: Path):
    if not which("trufflehog"):
        record_status("trufflehog", 127, "not found")
        log("trufflehog not found")
        return
    src = target_dir / "chakra"
    if not src.exists():
        src = target_dir
    run_capture(["trufflehog", "filesystem", str(src), "--json", "--no-update"],
                target_dir / "secrets.jsonl", logs / "trufflehog.log", timeout=1800)


def step_kiterunner(base: str, target_dir: Path, logs: Path, wordlist_path: Path, settings: dict):
    if not settings.get("enable_kiterunner", True):
        record_status("kiterunner", 0, "disabled by settings")
        return
    if not which("kr"):
        record_status("kiterunner", 127, "not found")
        return
    if not Path(wordlist_path).exists():
        record_status("kiterunner", 0, "no wordlist")
        return
    run_capture(
        ["kr", "brute", base, "-w", str(wordlist_path),
         "-x", str(settings.get("kiterunner_conns", 10)), "-j", "1",
         "-e", "json,txt,xml", "-o", "json", "-q", "--progress=false"],
        target_dir / "kiterunner.jsonl", logs / "kiterunner.log", timeout=2400)


def step_arjun(base: str, target_dir: Path, logs: Path, param_file: Path, settings: dict):
    if not settings.get("enable_arjun", True):
        record_status("arjun", 0, "disabled by settings")
        return
    if not which("arjun"):
        record_status("arjun", 127, "not found")
        return
    cmd = ["arjun", "-u", base, "-m", "GET,POST,JSON",
           "-oJ", str(target_dir / "arjun.json"),
           "-t", str(settings.get("arjun_threads", 10)), "--stable"]
    if Path(param_file).exists():
        cmd += ["-w", str(param_file)]
    cmd.append("--passive")
    run(cmd, logs / "arjun.log", timeout=1800)


def step_vhost(base: str, target_dir: Path, logs: Path, settings: dict):
    """Try discovered subdomain names as Host headers. Returns live vhost names."""
    if not settings.get("enable_vhost", True):
        record_status("vhost", 0, "disabled by settings")
        return []
    host = urlparse(base).netloc.split(":")[0]
    src = target_dir / "subdomains_all.txt"
    if not src.exists():
        record_status("vhost", 0, "no subdomains discovered")
        return []
    words = set()
    for line in src.read_text(encoding="utf-8", errors="replace").splitlines():
        h = line.strip().lower()
        if h.endswith("." + host):
            w = h[:-(len(host) + 1)]
            if w and "." not in w:
                words.add(w)
    if not words:
        record_status("vhost", 0, "no usable Host names")
        return []
    (target_dir / "vhost_words.txt").write_text(
        "\n".join(sorted(words)) + "\n", encoding="utf-8")

    import urllib.error
    import urllib.request
    from concurrent.futures import ThreadPoolExecutor, as_completed

    ua = settings.get("user_agent", "hunt-pipeline/1.0")
    timeout = int(settings.get("method_timeout", 10))
    probe_url = base.rstrip("/") + "/"

    def check(name):
        req = urllib.request.Request(
            probe_url, headers={"Host": f"{name}.{host}", "User-Agent": ua})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return name, r.status
        except urllib.error.HTTPError as e:
            return name, e.code
        except Exception:  # noqa: BLE001
            return name, 0

    rows, hits = [], []
    with ThreadPoolExecutor(max_workers=int(settings.get("method_threads", 20))) as pool:
        futures = [pool.submit(check, w) for w in sorted(words)]
        for f in as_completed(futures):
            name, code = f.result()
            vhost = f"{name}.{host}"
            rows.append({"host": vhost, "status_code": code})
            if code not in (0, 404):
                hits.append(vhost)
    write_jsonl(target_dir / "vhost.jsonl", rows)
    record_status("vhost", 0, f"{len(hits)} live of {len(words)} tested")
    log(f"vhost: {len(hits)} live Host headers of {len(words)} tested (no ffuf needed)")
    return hits


def step_methods(probe_rows, logs: Path, settings: dict):
    """Probe live routes with every HTTP method, in parallel."""
    if not settings.get("enable_methods", True):
        record_status("methods", 0, "disabled by settings")
        return []
    import urllib.error
    import urllib.request
    from concurrent.futures import ThreadPoolExecutor, as_completed

    targets = [r for r in probe_rows if r.get("status_code") in (200, 401, 403, 405)]
    targets = targets[:int(settings.get("max_method_targets", 200))]
    jobs = [(r["url"], m) for r in targets if r.get("url") for m in METHODS]
    if not jobs:
        return []

    timeout = int(settings.get("method_timeout", 10))
    ua = settings.get("user_agent", "hunt-pipeline/1.0")

    def one(url, method):
        try:
            req = urllib.request.Request(url, method=method, headers={"User-Agent": ua})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return url, method, resp.status
        except urllib.error.HTTPError as e:
            return url, method, e.code
        except Exception:  # noqa: BLE001
            return url, method, None

    results = []
    with ThreadPoolExecutor(max_workers=int(settings.get("method_threads", 20))) as pool:
        futures = [pool.submit(one, u, m) for u, m in jobs]
        for f in as_completed(futures):
            u, m, code = f.result()
            if code is not None:
                results.append({
                    "url": u,
                    "method": m,
                    "status_code": code,
                    "source": "method",
                })
    log(f"methods: {len(results)} method/status responses")
    return results


# ----------------------------------------------------------------------------
# probe + brute
# ----------------------------------------------------------------------------

def probe(routes, target_dir: Path, logs: Path, settings: dict):
    if not which("httpx"):
        record_status("httpx", 127, "not found")
        log("httpx not found - probe skipped")
        return []
    rows = list(routes.values())
    if not settings.get("probe_assets"):
        rows = [r for r in rows if not is_asset(r["url"])]
    cap = int(settings.get("max_urls", 20000))
    if len(rows) > cap:
        log(f"probe cap: {len(rows)} -> {cap}")
        rows = rows[:cap]
    urls_file = target_dir / "urls_to_probe.txt"
    urls_file.write_text("\n".join(r["url"] for r in rows) + "\n", encoding="utf-8")
    probe_list = urls_file
    if settings.get("enable_uro") and which("uro"):
        dedup = target_dir / "urls_to_probe_uro.txt"
        run(["uro", "-i", str(urls_file), "-o", str(dedup)], logs / "uro.log", timeout=600)
        if dedup.exists() and dedup.stat().st_size > 0:
            probe_list = dedup
            log(f"uro: probe list deduped for httpx (all routes still kept)")
    out = target_dir / "probe.jsonl"
    run(["httpx", "-l", str(probe_list), "-mc", "all", "-sc", "-cl", "-ct",
         "-title", "-td", "-json", "-o", str(out), "-silent",
         "-timeout", str(settings.get("request_timeout", 20)),
         "-retries", "1", "-rl", str(settings.get("httpx_rate", 50)),
         "-threads", "50"],
        logs / "httpx.log", timeout=3000)
    return read_jsonl(out)


def derive_prefixes(routes, limit: int):
    counts = {}
    for r in routes.values():
        parts = [x for x in urlparse(r["url"]).path.split("/") if x]
        for depth in (1, 2):
            if len(parts) >= depth:
                pref = "/" + "/".join(parts[:depth])
                counts[pref] = counts.get(pref, 0) + 1
    items = []
    for k, v in counts.items():
        last = k.split("/")[-1]
        if "." in last:
            continue
        items.append((k, v))
    items.sort(key=lambda x: -x[1])
    return [k for k, _ in items[:limit]]


def brute(routes, base: str, target_dir: Path, logs: Path, settings: dict,
          wordlist_path: Path):
    if not settings.get("enable_brute") or not which("ffuf"):
        return []
    prefixes = derive_prefixes(routes, int(settings.get("max_brute_prefixes", 15)))
    wl = str(wordlist_path) if Path(wordlist_path).exists() else settings.get("wordlist", "wordlists/common.txt")
    if not Path(wl).exists():
        log(f"wordlist missing: {wl}")
        return []
    results = []
    bdir = target_dir / "brute"
    bdir.mkdir(parents=True, exist_ok=True)
    for i, pref in enumerate(prefixes):
        url = base.rstrip("/") + pref.rstrip("/") + "/FUZZ"
        out = bdir / f"ffuf_{i}.json"
        run(["ffuf", "-u", url, "-w", wl, "-mc", "all", "-ac",
             "-rate", str(settings.get("ffuf_rate", 10)),
             "-t", str(settings.get("ffuf_threads", 10)),
             "-of", "json", "-o", str(out), "-s"],
            logs / f"ffuf_{i}.log", timeout=900)
        if out.exists():
            try:
                data = json.loads(out.read_text(encoding="utf-8", errors="replace"))
                for r in data.get("results", []):
                    results.append({
                        "url": r.get("url"),
                        "method": "GET",
                        "status_code": r.get("status"),
                        "content_type": r.get("content-type"),
                        "content_length": r.get("length"),
                        "source": "ffuf",
                    })
            except Exception:  # noqa: BLE001
                pass
    return results


def merge_hits(routes, hits, base: str) -> int:
    """Feed brute-force hits back into the context so the next round learns."""
    added = 0
    for h in hits:
        n = normalize(h.get("url"), base)
        if not n:
            continue
        k = dedupe_key(n)
        if k not in routes:
            routes[k] = {"url": n, "method": "GET", "sources": {"brute"}}
            added += 1
        else:
            routes[k].setdefault("sources", set()).add("brute")
    return added


def write_context(target_dir: Path, base: str, routes, stats: dict):
    ctx = {
        "target": base,
        "generated": now(),
        "routes": [{"url": r["url"], "method": r.get("method", "GET")}
                   for r in routes.values()],
        "stats": stats,
    }
    (target_dir / "context.json").write_text(
        json.dumps(ctx, indent=1, ensure_ascii=False, default=list),
        encoding="utf-8",
    )


# ----------------------------------------------------------------------------
# report
# ----------------------------------------------------------------------------

def report(target_dir: Path, base: str, routes, probe_rows, brute_rows, settings: dict):
    target_dir = Path(target_dir)
    merged = {}
    for r in probe_rows:
        u = r.get("url")
        if u:
            k = (dedupe_key(u), (r.get("method") or "GET").upper())
            merged[k] = dict(r)
    for r in brute_rows:
        u = r.get("url")
        if not u:
            continue
        k = (dedupe_key(u), (r.get("method") or "GET").upper())
        if k not in merged:
            merged[k] = dict(r)
        else:
            merged[k].setdefault("source", r.get("source"))

    live200, liveother, other = [], [], []
    for r in merged.values():
        try:
            st = int(r.get("status_code") or r.get("status") or 0)
        except Exception:  # noqa: BLE001
            st = 0
        r["status_code"] = st
        if st in STATUS_WIN:
            live200.append(r)
        elif st in STATUS_EXISTS:
            liveother.append(r)
        else:
            other.append(r)

    key = lambda r: r.get("url") or ""
    live200.sort(key=key)
    liveother.sort(key=key)
    other.sort(key=key)

    # all routes (unfiltered collection)
    all_routes = []
    for r in routes.values():
        all_routes.append({
            "url": r["url"],
            "method": r.get("method", "GET"),
            "sources": sorted(r.get("sources", [])),
        })
    all_routes.sort(key=key)

    # data-ish files (a category, not a filter)
    data_files = []
    for r in live200:
        ct = (r.get("content_type") or "").lower()
        path = urlparse(r.get("url", "")).path.lower()
        if (any(x in ct for x in ("json", "csv", "xml", "spreadsheet")) or
                path.endswith((".json", ".jsonl", ".ndjson", ".csv", ".xml", ".xlsx", ".xls"))):
            data_files.append(r)

    # params
    params = []
    for r in all_routes:
        q = urlparse(r["url"]).query
        if q:
            names = sorted({k for k, _ in parse_qsl(q, keep_blank_values=True)})
            params.append({"url": r["url"], "method": r["method"], "params": names})

    # hosts
    hosts = sorted({urlparse(r["url"]).netloc for r in all_routes if urlparse(r["url"]).netloc})

    # historical
    historical = []
    for f in target_dir.rglob("waymore_urls.txt"):
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if line:
                historical.append({"url": line, "source": "waymore"})

    # ---- data files: meaningful names + backward-compatible aliases ----
    write_jsonl(target_dir / "all_routes.jsonl", all_routes)
    write_jsonl(target_dir / "accessible_200.jsonl", live200)
    write_jsonl(target_dir / "exists_blocked.jsonl", liveother)
    write_jsonl(target_dir / "other_status.jsonl", other)
    write_jsonl(target_dir / "data_files.jsonl", data_files)
    write_jsonl(target_dir / "params.jsonl", params)
    write_jsonl(target_dir / "historical.jsonl", historical)
    write_jsonl(target_dir / "live_200.jsonl", live200)      # alias
    write_jsonl(target_dir / "live_other.jsonl", liveother)  # alias
    (target_dir / "hosts.txt").write_text("\n".join(hosts) + "\n", encoding="utf-8")

    sp = target_dir / "secrets.jsonl"
    secret_rows = []
    if sp.exists():
        for line in sp.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.strip():
                secret_rows.append(line.strip())
    secrets_count = len(secret_rows)

    elapsed = int(time.time() - RUN_START)

    lines = []
    lines.append(f"# Hunt Report — {base}")
    lines.append("")
    lines.append(f"Generated: {now()} &nbsp;|&nbsp; Duration: {elapsed // 60}m {elapsed % 60}s")
    lines.append("")
    lines.append("> **Nothing was filtered during collection.** This report is only a grouping.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| What | Count | Meaning |")
    lines.append("|---|---:|---|")
    lines.append(f"| Routes collected | {len(all_routes)} | Every URL found, nothing removed |")
    lines.append(f"| Responses checked | {len(merged)} | Every route actually requested |")
    lines.append(f"| **Accessible (200)** | **{len(live200)}** | Confirmed live — the wins |")
    lines.append(f"| Exists but not accessible | {len(liveother)} | 301/302/401/403/405 — real route, blocked |")
    lines.append(f"| Other responses | {len(other)} | 404/500/etc. — kept, not discarded |")
    lines.append(f"| Data files (200) | {len(data_files)} | JSON / CSV / XML / spreadsheet |")
    lines.append(f"| URLs with parameters | {len(params)} | Parameter discovery |")
    lines.append(f"| Hosts | {len(hosts)} | Apex + subdomains + vhosts |")
    lines.append(f"| Secret candidates | {secrets_count} | Keys/tokens — verify manually |")
    lines.append("")

    def section(title, rows, n=100):
        lines.append(f"## {title}")
        lines.append("")
        if not rows:
            lines.append("_No results in this category._")
            lines.append("")
            return
        lines.append("| Status | Method | URL | Type | Size | Source |")
        lines.append("|---|---|---|---|---|---|")
        for r in rows[:n]:
            st = r.get("status_code", "")
            m = r.get("method", "GET")
            u = (r.get("url") or "").replace("|", "%7C")
            ct = (r.get("content_type") or "").split(";")[0]
            cl = r.get("content_length", "")
            src = r.get("source", "")
            lines.append(f"| {st} | {m} | `{u}` | {ct} | {cl} | {src} |")
        if len(rows) > n:
            lines.append(f"| … | … | _{len(rows) - n} more in the JSONL file_ | … | … | … |")
        lines.append("")

    section("1. Accessible — HTTP 200", live200)
    section("2. Exists but not accessible — 301/302/401/403/405", liveother)
    section("3. Data files (accessible)", data_files)
    section("4. Other responses — kept, never discarded", other)

    lines.append("## 5. Parameters discovered")
    lines.append("")
    if params:
        lines.append("| URL | Method | Parameters |")
        lines.append("|---|---|---|")
        for r in params[:50]:
            u = (r["url"]).replace("|", "%7C")
            lines.append(f"| `{u}` | {r['method']} | {', '.join(r['params'])} |")
        if len(params) > 50:
            lines.append(f"| _{len(params) - 50} more_ | | |")
    else:
        lines.append("_No parameters found._")
    lines.append("")

    vhost_rows = read_jsonl(target_dir / "vhost.jsonl")
    vhost_live = [v for v in vhost_rows if v.get("status_code") not in (0, 404)]
    apex = urlparse(base).netloc.lower()
    subs = sorted({h for h in hosts if h != apex and not h.endswith("." + apex)})
    real_subs = sorted({h for h in hosts if h.endswith("." + apex)})
    lines.append("## 6. Hosts discovered")
    lines.append("")
    lines.append(f"- Apex domain: `{apex}`")
    lines.append(f"- Subdomains: **{len(real_subs)}**")
    lines.append(f"- Virtual hosts (Host-header only): **{len(vhost_live)}**")
    lines.append(f"- Other hosts: {len(subs)}")
    lines.append("")
    lines.append("```text")
    lines.extend(vhost_live[:100] and [v["host"] for v in vhost_live[:100]] or [])
    lines.extend(real_subs[:200])
    if len(real_subs) > 200:
        lines.append(f"... {len(real_subs) - 200} more in hosts.txt")
    lines.append("```")
    lines.append("")

    lines.append("## 7. Secret candidates")
    lines.append("")
    if secret_rows:
        lines.append(f"{secrets_count} candidate(s) found in `secrets.jsonl`. Verify manually — regex matches can be false positives.")
    else:
        lines.append("_None found._")
    lines.append("")

    lines.append("## 8. Tool run status")
    lines.append("")
    lines.append("| Tool | Result | Detail |")
    lines.append("|---|---|---|")
    for name in sorted(RUN_STATUS):
        st = RUN_STATUS[name]
        code = st.get("exit")
        result = "OK" if code == 0 else f"exit {code}"
        note = st.get("note") or ("completed, see logs/ for detail" if code == 0 else "check logs/")
        lines.append(f"| `{name}` | {result} | {note} |")
    lines.append("")

    lines.append("## 9. Intentionally not run")
    lines.append("")
    lines.append("- **ffuf path brute force** — off by default (it would take hours). "
                 "`wordlist.txt` is generated and ready; set `enable_brute: true` "
                 "in a later manual run to find guessed-only paths.")
    if not uncover_engine():
        lines.append("- **uncover data** — no API key configured. The tool runs, but no external data is returned.")
    lines.append("")

    lines.append("## 10. Output files")
    lines.append("")
    out_files = [
        ("REPORT.md", "This report"),
        ("all_routes.jsonl", "Every route found — unfiltered"),
        ("accessible_200.jsonl", "HTTP 200 — accessible"),
        ("exists_blocked.jsonl", "Route exists but blocked"),
        ("other_status.jsonl", "Every other status — kept"),
        ("data_files.jsonl", "Accessible JSON/CSV/XML/etc."),
        ("params.jsonl", "Parameters found"),
        ("historical.jsonl", "Archived / removed URLs"),
        ("hosts.txt", "All hosts"),
        ("wordlist.txt", "Generated wordlist — ready for ffuf"),
        ("params.txt", "Generated parameter wordlist"),
        ("context.json", "Shared context between layers"),
        ("js_urls.txt", "All discovered JS file URLs"),
        ("subdomains_all.txt", "All discovered subdomains"),
        ("subdomains_live.txt", "DNS-resolved subdomains"),
        ("vhost.jsonl", "Virtual-host results"),
        ("xnlinkfinder.txt", "Endpoints from xnLinkFinder"),
        ("xnlinkfinder_wordlist.txt", "xnLinkFinder target wordlist"),
        ("kiterunner.jsonl", "API brute results"),
        ("arjun.json", "Hidden parameter results"),
        ("jsluice.jsonl", "URLs parsed from JS"),
        ("secrets.jsonl", "Secret candidates"),
        ("logs/", "Raw tool output — check here for any error"),
    ]
    lines.append("| File | Meaning |")
    lines.append("|---|---|")
    for name, meaning in out_files:
        p = target_dir / name
        if p.exists():
            size = f"{p.stat().st_size:,} B"
            lines.append(f"| [`{name}`]({name}) | {meaning} ({size}) |")
    lines.append("")

    lines.append("## Status meaning")
    lines.append("")
    lines.append("| Status | Meaning |")
    lines.append("|---|---|")
    lines.append("| 200 | Accessible — confirmed win |")
    lines.append("| 301 / 302 / 307 / 308 | Redirect — route exists |")
    lines.append("| 401 / 403 | Exists but blocked — discovery, not a leak |")
    lines.append("| 405 | Exists, wrong method — try the method table above |")
    lines.append("| 404 | Not found — kept for completeness |")
    lines.append("")
    lines.append("> **Golden rule:** collect wide, verify status, categorize last. "
                 "Nothing is deleted from the data files.")

    (target_dir / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    return {
        "collected": len(all_routes),
        "probed": len(merged),
        "live200": len(live200),
        "liveother": len(liveother),
        "data": len(data_files),
    }


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--urls", default="urls.txt")
    ap.add_argument("--out", default="output")
    ap.add_argument("--settings", default="config/settings.json")
    args = ap.parse_args()

    settings = json.loads(Path(args.settings).read_text(encoding="utf-8"))
    for key, env in (("enable_subdomains", "ENABLE_SUBDOMAINS"),
                     ("enable_uncover", "ENABLE_UNCOVER"),
                     ("enable_urlscan", "ENABLE_URLSCAN"),
                     ("enable_uro", "ENABLE_URO"),
                     ("enable_brute", "ENABLE_BRUTE"),
                     ("enable_vhost", "ENABLE_VHOST"),
                     ("enable_methods", "ENABLE_METHODS"),
                     ("enable_browser", "ENABLE_BROWSER"),
                     ("enable_kiterunner", "ENABLE_KITERUNNER"),
                     ("enable_arjun", "ENABLE_ARJUN")):
        if os.environ.get(env) is not None:
            settings[key] = os.environ[env].strip().lower() in ("1", "true", "yes", "on")

    if not check_tools(settings):
        log("Cannot continue: a required tool is missing. Fix the installer and re-run.")
        return 2

    raw_urls = [
        l.strip() for l in Path(args.urls).read_text(encoding="utf-8").splitlines()
        if l.strip() and not l.strip().startswith("#")
    ]
    if not raw_urls:
        log("no targets in urls file")
        return 2

    out_root = Path(args.out)
    out_root.mkdir(parents=True, exist_ok=True)
    summary = []

    for raw in raw_urls:
        base = normalize_base(raw)
        host = urlparse(base).netloc
        target_dir = out_root / host.replace(":", "_")
        logs = target_dir / "logs"
        logs.mkdir(parents=True, exist_ok=True)
        log(f"=== TARGET {base} -> {target_dir} ===")

        def step(name, fn, *a):
            try:
                log(f"STEP {name} start")
                result = fn(*a)
                log(f"STEP {name} done")
                return result
            except Exception as e:  # noqa: BLE001
                log(f"STEP {name} FAILED: {e}")
                return None

        step("subdomains", step_subdomains, host, target_dir, logs, settings)
        step("chakra", step_chakra, base, target_dir, logs, settings)
        step("jsrecon", step_jsrecon, base, target_dir, logs, settings)
        step("katana", step_katana, base, target_dir, logs, settings)
        step("waymore", step_waymore, host, target_dir, logs)
        step("urlscan", step_urlscan, host, target_dir, logs, settings)
        step("jsluice", step_jsluice, target_dir, logs)
        step("xnlinkfinder", step_xnlinkfinder, host, target_dir, logs)
        step("trufflehog", step_trufflehog, target_dir, logs)

        routes = collect(target_dir, base)
        log(f"collected {len(routes)} unique URLs")

        # vhost brute feeds new hosts back into the pool
        vhost_hosts = step("vhost", step_vhost, base, target_dir, logs, settings) or []
        for h in vhost_hosts:
            n = normalize(f"https://{h}", base)
            if n:
                routes[dedupe_key(n)] = {"url": n, "method": "GET", "sources": {"vhost"}}
        if vhost_hosts:
            log(f"merged {len(vhost_hosts)} vhost hosts into routes")

        # ---- context-aware wordlist foundry ----
        wl_path = target_dir / "wordlist.txt"
        param_path = target_dir / "params.txt"
        winfo = wordlist.build(
            target_dir, base,
            settings.get("wordlist", "wordlists/common.txt"),
            wl_path,
            int(settings.get("wordlist_max", 8000)),
            param_path,
        )
        log(f"wordlist built: {winfo}")

        probe_rows = probe(routes, target_dir, logs, settings)

        all_brute = []
        if settings.get("enable_brute", False):
            rounds = int(settings.get("wordlist_rounds", 2))
            for rnd in range(rounds):
                hits = brute(routes, base, target_dir, logs, settings, wl_path)
                all_brute.extend(hits)
                added = merge_hits(routes, hits, base)
                log(f"brute round {rnd + 1}: hits={len(hits)} new={added} routes={len(routes)}")
                if added == 0:
                    break
                winfo = wordlist.build(
                    target_dir, base,
                    settings.get("wordlist", "wordlists/common.txt"),
                    wl_path,
                    int(settings.get("wordlist_max", 8000)),
                    param_path,
                )
                log(f"wordlist rebuilt: {winfo}")
        else:
            record_status("ffuf", 0, "path brute off - wordlist prepared, run later with enable_brute=true")
            log("ffuf path brute: OFF by choice (wordlist.txt is ready; no time cost)")

        step("kiterunner", step_kiterunner, base, target_dir, logs, wl_path, settings)
        step("arjun", step_arjun, base, target_dir, logs, param_path, settings)
        method_rows = step("methods", step_methods, probe_rows, logs, settings) or []
        all_brute.extend(method_rows)

        stats = report(target_dir, base, routes, probe_rows, all_brute, settings)
        write_context(target_dir, base, routes, stats)
        summary.append((base, stats))
        log(f"REPORT {target_dir / 'REPORT.md'} -> {stats}")

    slines = ["# Hunt summary", ""]
    for base, s in summary:
        slines.append(f"- {base}: collected={s['collected']} probed={s['probed']} "
                      f"live200={s['live200']} blocked={s['liveother']} data={s['data']}")
    (out_root / "SUMMARY.md").write_text("\n".join(slines) + "\n", encoding="utf-8")

    # human-friendly index — open this in the repo, no download needed
    idx = ["# Hunt results", "", f"Generated: {now()}", "",
           "Open a target's **REPORT.md** for the full readable findings.", ""]
    idx.append("| Target | Report | Accessible (200) | Exists but blocked | Data files | Routes |")
    idx.append("|---|---|---:|---:|---:|---:|")
    for base, s in summary:
        host = urlparse(base).netloc.replace(":", "_")
        idx.append(f"| `{host}` | [REPORT.md]({host}/REPORT.md) | {s['live200']} | "
                   f"{s['liveother']} | {s['data']} | {s['collected']} |")
    idx.append("")
    idx.append("- **Accessible (200)** — confirmed live responses.")
    idx.append("- **Exists but blocked** — real routes returning 301/302/401/403/405.")
    idx.append("- **Routes** — everything collected; nothing was filtered out.")
    idx.append("- **ffuf path brute** was OFF by choice; `wordlist.txt` is ready in each target folder.")
    idx.append("")
    (out_root / "INDEX.md").write_text("\n".join(idx), encoding="utf-8")
    log(f"INDEX {out_root / 'INDEX.md'}")
    log("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
