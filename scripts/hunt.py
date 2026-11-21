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
XNLINK_PATH = os.environ.get("XNLINK_PATH", os.path.expanduser("~/tools/xnLinkFinder/xnLinkFinder.py"))


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------

def now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def log(msg: str) -> None:
    print(f"[{now()}] {msg}", flush=True)


def which(tool: str):
    return shutil.which(tool)


def run(cmd, log_path: Path, timeout: int = 3600, cwd=None) -> int:
    """Run a command, append stdout+stderr to a binary log file."""
    log_path = Path(log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
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
            return p.returncode
        except FileNotFoundError as e:
            lf.write(f"\n[missing: {e}]\n".encode("utf-8", "replace"))
            return 127
        except subprocess.TimeoutExpired:
            lf.write(f"\n[timeout {timeout}s]\n".encode())
            return 124
        except Exception as e:  # noqa: BLE001
            lf.write(f"\n[error {e}]\n".encode("utf-8", "replace"))
            return 1


def run_capture(cmd, out_file: Path, log_path: Path, timeout: int = 1800) -> int:
    """Run a command, write stdout to out_file, stderr to log."""
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
            return p.returncode
        except Exception as e:  # noqa: BLE001
            lf.write(f"\n[error {e}]\n".encode("utf-8", "replace"))
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
    if not which("subfinder"):
        log("subfinder not found, skipping")
        return
    out = target_dir / "subdomains.txt"
    run(["subfinder", "-d", host, "-silent", "-o", str(out)], logs / "subfinder.log", timeout=1200)
    if which("dnsx") and out.exists():
        run(["dnsx", "-l", str(out), "-silent", "-o", str(target_dir / "subdomains_live.txt")],
            logs / "dnsx.log", timeout=1200)


def step_chakra(base: str, target_dir: Path, logs: Path):
    if not os.path.exists(CHAKRA_PATH):
        log(f"Chakra not found at {CHAKRA_PATH}, skipping")
        return
    run([sys.executable, CHAKRA_PATH, base, "-o", str(target_dir / "chakra"),
         "-t", "8", "--delay", "0.2"],
        logs / "chakra.log", timeout=2400)


def step_jsrecon(base: str, target_dir: Path, logs: Path, settings: dict):
    if not which("js-recon"):
        log("js-recon not found, skipping")
        return
    out = target_dir / "jsrecon"
    out.mkdir(parents=True, exist_ok=True)

    cmd = ["js-recon", "lazyload", "-u", base, "-o", str(out), "-y",
           "--build-id", "--subsequent-requests", "--max-pages", "200",
           "--lazyload-timeout", "30"]
    if settings.get("enable_browser", True):
        cmd.append("--no-sandbox")
    run(cmd, logs / "jsrecon_lazyload.log", timeout=2400)

    # strings: URLs + paths + secrets
    run(["js-recon", "strings", "-d", str(out), "-e", "-p", "-s",
         "-o", str(out / "strings.json"),
         "--extracted-url-path", str(out / "extracted_urls")],
        logs / "jsrecon_strings.log", timeout=1800)

    # endpoints: best-effort (tech flag required by the tool)
    run(["js-recon", "endpoints", "-d", str(out), "-t", "next", "-u", base,
         "-o", str(out / "endpoints")],
        logs / "jsrecon_endpoints.log", timeout=1200)


def step_katana(base: str, target_dir: Path, logs: Path, settings: dict):
    if not which("katana"):
        log("katana not found, skipping")
        return
    k = target_dir / "katana"
    k.mkdir(parents=True, exist_ok=True)

    # pass 1: JS string literals + known files
    run(["katana", "-u", base, "-d", "5", "-jc", "-kf", "all",
         "-ef", "png,jpg,jpeg,gif,svg,css,woff,woff2,ttf,eot,ico,mp4,mp3,pdf",
         "-c", "20", "-silent", "-json", "-o", str(k / "pass1.jsonl")],
        logs / "katana_pass1.log", timeout=2400)

    # pass 2: headless runtime (XHR method capture)
    if settings.get("enable_browser", True):
        run(["katana", "-u", base, "-d", "5", "-headless", "-xhr", "-no-sandbox",
             "-c", "10", "-silent", "-json", "-o", str(k / "pass2.jsonl")],
            logs / "katana_pass2.log", timeout=2400)


def step_waymore(host: str, target_dir: Path, logs: Path):
    if not which("waymore"):
        log("waymore not found, skipping")
        return
    w = target_dir / "history"
    w.mkdir(parents=True, exist_ok=True)
    run(["waymore", "-i", host, "-mode", "U", "-oU", str(w / "waymore_urls.txt")],
        logs / "waymore.log", timeout=1800)


def step_urlscan(host: str, target_dir: Path, logs: Path):
    key = os.environ.get("URLSCAN_API_KEY", "").strip()
    if not key:
        return
    w = target_dir / "history"
    w.mkdir(parents=True, exist_ok=True)
    out = w / "urlscan.json"
    try:
        import urllib.request

        req = urllib.request.Request(
            f"https://urlscan.io/api/v1/search/?q=domain%3A{host}&size=1000",
            headers={"api-key": key, "User-Agent": "hunt-pipeline/1.0"},
        )
        with urllib.request.urlopen(req, timeout=60) as r:
            out.write_bytes(r.read())
        log(f"urlscan saved -> {out}")
    except Exception as e:  # noqa: BLE001
        log(f"urlscan failed: {e}")


def step_jsluice(target_dir: Path, logs: Path):
    if not which("jsluice"):
        log("jsluice not found, skipping")
        return
    js_files = [p for p in target_dir.rglob("*.js") if p.is_file()]
    out = target_dir / "jsluice.jsonl"
    secrets = target_dir / "jsluice_secrets.jsonl"
    with open(out, "w", encoding="utf-8") as f, open(secrets, "w", encoding="utf-8") as sf:
        for js in js_files[:4000]:
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
    if not os.path.exists(XNLINK_PATH):
        log(f"xnLinkFinder not found at {XNLINK_PATH}, skipping")
        return
    src = target_dir / "chakra"
    if not src.exists():
        src = target_dir
    run([sys.executable, XNLINK_PATH, "-i", str(src), "-sf", host,
         "-o", str(target_dir / "xnlinkfinder.txt"),
         "-op", str(target_dir / "xnlinkfinder_params.txt"),
         "-owl", str(target_dir / "xnlinkfinder_wordlist.txt")],
        logs / "xnlinkfinder.log", timeout=1800)


def step_trufflehog(target_dir: Path, logs: Path):
    if not which("trufflehog"):
        log("trufflehog not found, skipping")
        return
    src = target_dir / "chakra"
    if not src.exists():
        src = target_dir
    run_capture(["trufflehog", "filesystem", str(src), "--json", "--no-update"],
                target_dir / "secrets.jsonl", logs / "trufflehog.log", timeout=1800)


# ----------------------------------------------------------------------------
# probe + brute
# ----------------------------------------------------------------------------

def probe(routes, target_dir: Path, logs: Path, settings: dict):
    if not which("httpx"):
        log("httpx not found, skipping probe")
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
    out = target_dir / "probe.jsonl"
    run(["httpx", "-l", str(urls_file), "-mc", "all", "-sc", "-cl", "-ct",
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


def brute(routes, base: str, target_dir: Path, logs: Path, settings: dict):
    if not settings.get("enable_brute") or not which("ffuf"):
        return []
    prefixes = derive_prefixes(routes, int(settings.get("max_brute_prefixes", 15)))
    wl = settings.get("wordlist", "wordlists/common.txt")
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
                        "status_code": r.get("status"),
                        "content_type": r.get("content-type"),
                        "content_length": r.get("length"),
                        "source": "ffuf",
                    })
            except Exception:  # noqa: BLE001
                pass
    return results


# ----------------------------------------------------------------------------
# report
# ----------------------------------------------------------------------------

def report(target_dir: Path, base: str, routes, probe_rows, brute_rows, settings: dict):
    merged = {}
    for r in probe_rows:
        u = r.get("url")
        if u:
            merged[dedupe_key(u)] = dict(r)
    for r in brute_rows:
        u = r.get("url")
        if not u:
            continue
        k = dedupe_key(u)
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

    write_jsonl(target_dir / "all_routes.jsonl", all_routes)
    write_jsonl(target_dir / "live_200.jsonl", live200)
    write_jsonl(target_dir / "live_other.jsonl", liveother)
    write_jsonl(target_dir / "data_files.jsonl", data_files)
    write_jsonl(target_dir / "params.jsonl", params)
    write_jsonl(target_dir / "historical.jsonl", historical)
    (target_dir / "hosts.txt").write_text("\n".join(hosts) + "\n", encoding="utf-8")

    secrets_count = 0
    sp = target_dir / "secrets.jsonl"
    if sp.exists():
        secrets_count = sum(1 for l in sp.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip())

    lines = []
    lines.append(f"# Hunt Report — {base}")
    lines.append("")
    lines.append(f"Generated: {now()}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Metric | Count |")
    lines.append("|---|---|")
    lines.append(f"| URLs collected (all) | {len(all_routes)} |")
    lines.append(f"| Probed | {len(merged)} |")
    lines.append(f"| **Live 200** | **{len(live200)}** |")
    lines.append(f"| Route exists but blocked (301/302/401/403/405) | {len(liveother)} |")
    lines.append(f"| Other status | {len(other)} |")
    lines.append(f"| Data-ish files (200) | {len(data_files)} |")
    lines.append(f"| URLs with params | {len(params)} |")
    lines.append(f"| Hosts | {len(hosts)} |")
    lines.append(f"| Historical URLs | {len(historical)} |")
    lines.append(f"| Secret candidates | {secrets_count} |")
    lines.append("")

    def section(title, rows, n=100):
        lines.append(f"## {title}")
        lines.append("")
        if not rows:
            lines.append("_none_")
            lines.append("")
            return
        lines.append("| Status | Method | URL | Type | Size |")
        lines.append("|---|---|---|---|---|")
        for r in rows[:n]:
            st = r.get("status_code", "")
            m = r.get("method", "GET")
            u = (r.get("url") or "").replace("|", "%7C")
            ct = (r.get("content_type") or "").split(";")[0]
            cl = r.get("content_length", "")
            lines.append(f"| {st} | {m} | {u} | {ct} | {cl} |")
        if len(rows) > n:
            lines.append(f"| ... | ... | _{len(rows) - n} more_ | ... | ... |")
        lines.append("")

    section("Live 200 (confirmed)", live200)
    section("Route exists but blocked", liveother)
    section("Data files (200)", data_files)

    lines.append("## Hosts")
    lines.append("")
    lines.append("```")
    lines.extend(hosts[:500])
    if len(hosts) > 500:
        lines.append(f"... {len(hosts) - 500} more")
    lines.append("```")
    lines.append("")

    lines.append("## Output files")
    lines.append("")
    for name in ("all_routes.jsonl", "live_200.jsonl", "live_other.jsonl",
                 "data_files.jsonl", "params.jsonl", "historical.jsonl",
                 "hosts.txt", "secrets.jsonl"):
        p = target_dir / name
        if p.exists():
            lines.append(f"- `{name}` ({p.stat().st_size} bytes)")
    lines.append("")
    lines.append("> 200 = confirmed win. 301/302/401/403/405 = route exists but blocked (discovery, not a leak).")
    lines.append("> Nothing was filtered during collection. This report is only a grouping.")

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
                     ("enable_brute", "ENABLE_BRUTE"),
                     ("enable_browser", "ENABLE_BROWSER")):
        if os.environ.get(env) is not None:
            settings[key] = os.environ[env].strip().lower() in ("1", "true", "yes", "on")

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
                fn(*a)
                log(f"STEP {name} done")
            except Exception as e:  # noqa: BLE001
                log(f"STEP {name} FAILED: {e}")

        step("subdomains", step_subdomains, host, target_dir, logs, settings)
        step("chakra", step_chakra, base, target_dir, logs)
        step("jsrecon", step_jsrecon, base, target_dir, logs, settings)
        step("katana", step_katana, base, target_dir, logs, settings)
        step("waymore", step_waymore, host, target_dir, logs)
        step("urlscan", step_urlscan, host, target_dir, logs)
        step("jsluice", step_jsluice, target_dir, logs)
        step("xnlinkfinder", step_xnlinkfinder, host, target_dir, logs)
        step("trufflehog", step_trufflehog, target_dir, logs)

        routes = collect(target_dir, base)
        log(f"collected {len(routes)} unique URLs")

        probe_rows = probe(routes, target_dir, logs, settings)
        brute_rows = brute(routes, base, target_dir, logs, settings)

        stats = report(target_dir, base, routes, probe_rows, brute_rows, settings)
        summary.append((base, stats))
        log(f"REPORT {target_dir / 'REPORT.md'} -> {stats}")

    lines = ["# Hunt summary", ""]
    for base, s in summary:
        lines.append(f"- {base}: collected={s['collected']} probed={s['probed']} "
                     f"live200={s['live200']} blocked={s['liveother']} data={s['data']}")
    (out_root / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    log("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
