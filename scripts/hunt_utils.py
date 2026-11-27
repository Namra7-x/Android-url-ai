#!/usr/bin/env python3
"""
Shared helpers for hunt.py:
- Wall-clock BudgetTimer
- Apex root domain & first-party boundary resolution
- URL normalization, deduplication, and route pattern collapsing
- JSONL I/O and safe subprocess runners
- ai_feed.json and REPORT.md generation
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import threading
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urljoin, urlparse, urlunparse

ALL_CODES = ",".join(str(i) for i in range(100, 600))
STATUS_WIN = {200, 201, 202, 204, 206}
STATUS_EXISTS = {301, 302, 303, 307, 308, 401, 403, 405}
VHOST_REAL = {200, 201, 202, 204, 206, 301, 302, 303, 307, 308, 401, 403, 405}

SHARED_APEX_DOMAINS = {
    "google.com", "azure.com", "microsoft.com", "amazonaws.com",
    "alibabacloud.com", "aliyun.com", "cloudfront.net", "github.io",
    "gitlab.io", "vercel.app", "netlify.app", "herokuapp.com",
    "workers.dev", "pages.dev", "appspot.com", "web.app",
    "firebaseapp.com", "azurewebsites.net", "cloud.google.com",
    "console.alibabacloud.com", "console.aws.amazon.com", "amazon.com",
}

MULTI_LABEL_TLDS = {
    "co.uk", "org.uk", "ac.uk", "gov.uk",
    "com.au", "net.au", "org.au",
    "co.jp", "ne.jp", "or.jp",
    "com.br", "com.sg", "co.in", "co.kr",
}

ASSET_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".webp", ".avif",
    ".css", ".woff", ".woff2", ".ttf", ".eot", ".otf",
    ".mp4", ".webm", ".mp3", ".wav", ".ogg", ".pdf", ".zip", ".gz",
}

JS_OR_DATA_EXT = (".js", ".mjs", ".cjs", ".json", ".map")

DATA_FILE_EXT = (
    ".json", ".jsonl", ".ndjson", ".yaml", ".yml", ".xml", ".csv",
    ".txt", ".env", ".toml", ".ini", ".conf", ".map",
)

AI_ROUTE_RE = re.compile(
    r"(?:v1alpha|v1beta|/api/|graphql|graphiql|llms(?:-full)?\.txt|openapi|"
    r"swagger|\$discovery|ai-plugin|models|capabilities|feature[-_]?flags?|"
    r"experiments|internal|admin|debug|config|manifest|trpc|/rpc)",
    re.I,
)

LOCALE_SEG_RE = re.compile(r"^[a-z]{2}(?:-[A-Z]{2}|-[a-z]{2})?$")
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)
HEX_ID_RE = re.compile(r"^[0-9a-f]{16,}$", re.I)
NUM_ID_RE = re.compile(r"^\d+$")
SLUG_ID_RE = re.compile(r"^[A-Za-z0-9_-]{24,}$")

WELLKNOWN_AI_PATHS = [
    "/llms.txt",
    "/llms-full.txt",
    "/robots.txt",
    "/sitemap.xml",
    "/sitemap_index.xml",
    "/openapi.json",
    "/openapi.yaml",
    "/swagger.json",
    "/v1/models",
    "/api/models",
    "/api/config",
    "/config.json",
    "/manifest.json",
    "/build-manifest.json",
    "/.well-known/ai-plugin.json",
    "/.well-known/security.txt",
    "/.well-known/openid-configuration",
    "/$discovery/rest?version=v1alpha",
    "/$discovery/rest?version=v1beta",
]


class BudgetTimer:
    """Thread-safe wall-clock budget tracker keeping runs inside <=12m."""

    def __init__(self, total_seconds: int) -> None:
        self.total_seconds = max(60, int(total_seconds))
        self.start = time.monotonic()
        self.deadline = self.start + self.total_seconds

    def elapsed(self) -> float:
        return time.monotonic() - self.start

    def remaining(self) -> float:
        return max(0.0, self.deadline - time.monotonic())

    def expired(self) -> bool:
        return time.monotonic() >= self.deadline

    def wave_deadline(self, wave_seconds: float) -> float:
        return min(self.deadline, time.monotonic() + max(5.0, float(wave_seconds)))

    def cap(self, wanted: float, wave_deadline: float | None = None, min_sec: int = 5) -> int:
        limit = self.deadline if wave_deadline is None else min(self.deadline, wave_deadline)
        rem = max(0.0, limit - time.monotonic())
        if rem <= 1.0:
            return 1
        return max(min_sec if rem >= min_sec else int(rem), int(min(float(wanted), rem)))


_LOG_LOCK = threading.Lock()


def log(msg: str) -> None:
    ts = time.strftime("%H:%M:%S", time.gmtime())
    with _LOG_LOCK:
        print(f"[{ts}] {msg}", flush=True)


def which(cmd: str) -> str | None:
    return shutil.which(cmd)


def extract_apex_domain(host: str) -> tuple[str, str, str]:
    """Return (exact_host, subfinder_domain, scope_apex).

    For shared cloud/multi-tenant parents (google.com, azure.com, alibabacloud.com),
    keep the service subdomain rather than enumerating the entire parent company.
    For independent brands (www.perplexity.ai), strip to perplexity.ai.
    """
    clean = host.strip().lower().split(":")[0]
    parts = [p for p in clean.split(".") if p]
    if len(parts) < 2:
        return clean, clean, clean

    for shared in SHARED_APEX_DOMAINS:
        if clean == shared or clean.endswith("." + shared):
            sub_target = clean[4:] if clean.startswith("www.") and clean.count(".") >= 2 else clean
            return clean, sub_target, sub_target

    last_two = ".".join(parts[-2:])
    if last_two in MULTI_LABEL_TLDS and len(parts) >= 3:
        apex = ".".join(parts[-3:])
    else:
        apex = last_two

    return clean, apex, apex


def is_first_party(url_or_host: str, exact_host: str, scope_apex: str) -> bool:
    try:
        host = urlparse(url_or_host).netloc.lower().split(":")[0] if "://" in url_or_host else url_or_host.lower().split(":")[0]
    except ValueError:
        return False
    if not host:
        return False
    return (
        host == exact_host
        or host.endswith("." + exact_host)
        or host == scope_apex
        or host.endswith("." + scope_apex)
    )


def normalize_url(raw: str, base: str | None = None) -> str | None:
    if not raw:
        return None
    s = raw.strip().strip("\"'`<>")
    if not s or s.startswith(("data:", "javascript:", "mailto:", "tel:", "blob:", "#")):
        return None
    if any(bad in s for bad in ("\n", "\r", "\t", " ", "\\u003c", "%5Cu003c", "<", ">")):
        return None
    if s.startswith("//"):
        s = "https:" + s
    elif s.startswith("/") and base:
        s = urljoin(base, s)
    elif not s.startswith(("http://", "https://")):
        if base and not s.startswith("http"):
            s = urljoin(base, s)
        else:
            return None
    try:
        p = urlparse(s)
    except ValueError:
        return None
    if p.scheme not in ("http", "https") or not p.netloc:
        return None
    host = p.hostname or ""
    if not host or "." not in host:
        return None
    netloc = host.lower()
    if p.port and not ((p.scheme == "http" and p.port == 80) or (p.scheme == "https" and p.port == 443)):
        netloc = f"{netloc}:{p.port}"
    path = re.sub(r"/{2,}", "/", p.path or "/")
    query = urlencode(sorted(parse_qsl(p.query, keep_blank_values=True))) if p.query else ""
    return urlunparse((p.scheme.lower(), netloc, path, "", query, ""))


def dedupe_key(url: str) -> str:
    try:
        p = urlparse(url)
        return f"{p.scheme}://{p.netloc}{p.path}?{p.query}" if p.query else f"{p.scheme}://{p.netloc}{p.path}"
    except ValueError:
        return url


def is_asset(url: str) -> bool:
    try:
        path = urlparse(url).path.lower()
    except ValueError:
        return False
    return any(path.endswith(ext) for ext in ASSET_EXT)


def is_js_or_map_url(url: str) -> bool:
    try:
        path = urlparse(url).path.lower()
    except ValueError:
        return False
    return path.endswith(JS_OR_DATA_EXT)


def is_data_file_url(url: str) -> bool:
    try:
        path = urlparse(url).path.lower()
    except ValueError:
        return False
    return path.endswith(DATA_FILE_EXT)


def collapse_route_pattern(url: str) -> str:
    try:
        p = urlparse(url)
    except ValueError:
        return url
    segs = [s for s in (p.path or "/").split("/") if s]
    norm_segs: list[str] = []
    for idx, seg in enumerate(segs):
        if idx == 0 and LOCALE_SEG_RE.match(seg) and seg not in {"v1", "v2", "v3", "ai", "js", "ui"}:
            norm_segs.append("{locale}")
        elif UUID_RE.match(seg):
            norm_segs.append("{uuid}")
        elif NUM_ID_RE.match(seg):
            norm_segs.append("{id}")
        elif HEX_ID_RE.match(seg):
            norm_segs.append("{hex}")
        elif SLUG_ID_RE.match(seg):
            norm_segs.append("{slug}")
        else:
            norm_segs.append(seg)
    path = "/" + "/".join(norm_segs) if norm_segs else "/"
    return f"{p.netloc}{path}"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.is_file():
        return rows
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.strip()
        if not s:
            continue
        try:
            obj = json.loads(s)
            if isinstance(obj, dict):
                rows.append(obj)
        except json.JSONDecodeError:
            continue
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def run_cmd(
    cmd: list[str],
    log_path: Path,
    timeout: int = 120,
    stdout_path: Path | None = None,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
) -> tuple[int, str]:
    """Run subprocess safely, capturing logs and enforcing timeout."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    run_env = os.environ.copy()
    if env:
        run_env.update(env)
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            timeout=max(1, int(timeout)),
            cwd=str(cwd) if cwd else None,
            env=run_env,
        )
        out_text = (proc.stdout or b"").decode("utf-8", "replace")
        err_text = (proc.stderr or b"").decode("utf-8", "replace")
        if stdout_path is not None:
            stdout_path.parent.mkdir(parents=True, exist_ok=True)
            stdout_path.write_text(out_text, encoding="utf-8")
        with log_path.open("a", encoding="utf-8") as lf:
            lf.write(f"$ {' '.join(cmd)}\nexit={proc.returncode}\n")
            if err_text:
                lf.write(err_text[-8000:] + "\n")
            if stdout_path is None and out_text:
                lf.write(out_text[-4000:] + "\n")
        return proc.returncode, out_text
    except subprocess.TimeoutExpired as exc:
        out_text = (exc.stdout or b"").decode("utf-8", "replace") if isinstance(exc.stdout, (bytes, bytearray)) else (exc.stdout or "")
        if stdout_path is not None and out_text:
            stdout_path.parent.mkdir(parents=True, exist_ok=True)
            stdout_path.write_text(out_text, encoding="utf-8")
        with log_path.open("a", encoding="utf-8") as lf:
            lf.write(f"$ {' '.join(cmd)}\nTIMEOUT after {timeout}s\n")
        return 124, out_text
    except Exception as exc:  # noqa: BLE001
        with log_path.open("a", encoding="utf-8") as lf:
            lf.write(f"$ {' '.join(cmd)}\nERROR: {exc}\n")
        return 1, ""


def is_cloudflare_response(row: dict[str, Any]) -> bool:
    code = int(row.get("status_code") or 0)
    title = str(row.get("title") or "").lower()
    tech = " ".join(str(t) for t in (row.get("tech") or [])).lower()
    if code in (403, 503, 530) and (
        "just a moment" in title
        or "attention required" in title
        or "cloudflare" in title
        or "cloudflare" in tech
    ):
        return True
    return "/cdn-cgi/challenge-platform" in str(row.get("url") or "")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_filename(name: str, fallback: str = "chunk.js") -> str:
    base = re.sub(r"[^A-Za-z0-9._-]", "_", name or fallback)
    return base[:80] or fallback


def redact_secret(val: str) -> str:
    s = str(val or "").strip()
    if len(s) <= 10:
        return s[:2] + "***"
    return f"{s[:6]}...{s[-4:]}"


def build_ai_feed(
    target_dir: Path,
    base_url: str,
    exact_host: str,
    duration_sec: float,
    secrets: list[dict[str, Any]],
    jscope_findings: list[dict[str, Any]],
    all_routes: list[dict[str, Any]],
    win_rows: list[dict[str, Any]],
    blocked_rows: list[dict[str, Any]],
    data_files: list[dict[str, Any]],
    live_subs: list[str],
    vhosts_real: list[dict[str, Any]],
    sourcemap_files: list[str],
    nuclei_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    """Assemble compact, ranked intelligence JSON (ai_feed.json) for LLM analysis."""
    ai_candidates: list[dict[str, Any]] = []
    seen_ai: set[str] = set()

    def rank_score(url: str, code: int) -> int:
        score = 0
        if code in STATUS_WIN:
            score += 50
        elif code in STATUS_EXISTS:
            score += 25
        low = url.lower()
        if any(k in low for k in ("v1alpha", "v1beta", "$discovery", "llms", "openapi", "swagger", "ai-plugin")):
            score += 40
        if any(k in low for k in ("graphql", "models", "capabilities", "feature", "flag", "experiment", "internal", "admin", "config")):
            score += 25
        return score

    for r in win_rows + blocked_rows + all_routes:
        u = str(r.get("url") or "")
        if not u or u in seen_ai:
            continue
        if AI_ROUTE_RE.search(u):
            seen_ai.add(u)
            code = int(r.get("status_code") or 0)
            ai_candidates.append({
                "url": u,
                "status_code": code,
                "title": r.get("title", ""),
                "sources": r.get("sources", []),
                "score": rank_score(u, code),
            })

    ai_candidates.sort(key=lambda item: (-item["score"], item["url"]))

    pattern_counts: Counter[str] = Counter()
    pattern_samples: dict[str, str] = {}
    for r in all_routes:
        u = str(r.get("url") or "")
        if not u:
            continue
        pat = collapse_route_pattern(u)
        pattern_counts[pat] += 1
        pattern_samples.setdefault(pat, u)

    collapsed_patterns = [
        {"pattern": pat, "count": cnt, "sample": pattern_samples[pat]}
        for pat, cnt in pattern_counts.most_common(120)
    ]

    compact_secrets: list[dict[str, Any]] = []
    seen_sec: set[str] = set()
    for s in secrets:
        det = str(s.get("detector") or s.get("rule") or "unknown")
        raw = str(s.get("raw") or s.get("match") or "")
        key = f"{det}:{raw[:32]}"
        if key in seen_sec:
            continue
        seen_sec.add(key)
        compact_secrets.append({
            "source": s.get("source", ""),
            "detector": det,
            "verified": bool(s.get("verified", False)),
            "redacted": redact_secret(raw),
            "file": s.get("file", ""),
        })

    feed = {
        "target": base_url,
        "host": exact_host,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "duration_seconds": round(duration_sec, 1),
        "summary": {
            "secrets": len(compact_secrets),
            "flags_and_guards": len(jscope_findings),
            "ai_and_api_candidates": len(ai_candidates),
            "unpacked_sourcemaps": len(sourcemap_files),
            "data_files": len(data_files),
            "live_subdomains": len(live_subs),
            "real_vhosts": len(vhosts_real),
            "accessible_200": len(win_rows),
            "exists_blocked": len(blocked_rows),
            "nuclei_findings": len(nuclei_rows),
            "collapsed_patterns": len(collapsed_patterns),
        },
        "secrets": compact_secrets[:100],
        "feature_flags_and_guards": jscope_findings[:200],
        "ai_and_api_candidates": ai_candidates[:200],
        "unpacked_sourcemaps_and_configs": {
            "sourcemap_files": sourcemap_files[:150],
            "data_files": [
                {"url": d.get("url"), "status_code": d.get("status_code", 0)}
                for d in data_files[:150]
            ],
        },
        "live_subdomains_and_vhosts": {
            "subdomains": live_subs[:150],
            "vhosts_real": vhosts_real[:100],
        },
        "route_patterns": collapsed_patterns,
        "nuclei_findings": [
            {
                "severity": (n.get("info") or {}).get("severity", "?"),
                "template_id": n.get("template-id", "?"),
                "host": n.get("host", ""),
                "matched_at": n.get("matched-at", ""),
            }
            for n in nuclei_rows[:100]
        ],
    }
    (target_dir / "ai_feed.json").write_text(json.dumps(feed, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return feed


def write_report_and_context(
    target_dir: Path,
    base_url: str,
    exact_host: str,
    scope_apex: str,
    duration_sec: float,
    wave_timings: dict[str, float],
    tool_statuses: list[dict[str, Any]],
    feed: dict[str, Any],
    stats: dict[str, int],
    other_rows: list[dict[str, Any]],
    third_party_rows: list[dict[str, Any]],
    method_rows: list[dict[str, Any]],
    vhost_blocked: list[dict[str, Any]],
    js_endpoints: list[dict[str, Any]],
) -> None:
    """Write human-readable REPORT.md and machine-readable context.json."""
    mins, secs = divmod(int(round(duration_sec)), 60)
    lines = [
        f"# Web Hunt Report: `{exact_host}`",
        "",
        f"- **Target:** {base_url}",
        f"- **Scope Apex:** `{scope_apex}`",
        f"- **Duration:** `{mins}:{secs:02d}` ({duration_sec:.1f}s)",
        f"- **Generated:** {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}",
        "",
        "## Wave Timings",
        "",
        "| Wave | Elapsed (s) |",
        "|---|---:|",
    ]
    for wave_name, w_sec in wave_timings.items():
        lines.append(f"| {wave_name} | {w_sec:.1f} |")

    lines += [
        "",
        "## Headline Counts",
        "",
        "| Metric | Count | Artifact |",
        "|---|---:|---|",
        f"| Total collected routes | {stats.get('collected', 0)} | `all_routes.jsonl` |",
        f"| Accessible 200 | {stats.get('live200', 0)} | `accessible_200.jsonl` |",
        f"| Exists / blocked (30x/401/403/405) | {stats.get('liveother', 0)} | `exists_blocked.jsonl` |",
        f"| Other status (404/500/etc) | {len(other_rows)} | `other_status.jsonl` |",
        f"| Live subdomains | {stats.get('subdomains', 0)} | `subdomains.jsonl` |",
        f"| Real virtual hosts | {stats.get('vhosts', 0)} | `vhost_real.jsonl` |",
        f"| Blocked vhost checks | {len(vhost_blocked)} | `vhost_blocked.jsonl` |",
        f"| JS endpoints | {len(js_endpoints)} | `js_endpoints.jsonl` |",
        f"| Feature flags / role guards | {stats.get('flags', 0)} | `jscope_findings.json` |",
        f"| AI & API candidates | {stats.get('ai_endpoints', 0)} | `ai_feed.json` |",
        f"| Secret candidates | {stats.get('secrets', 0)} | `secrets.jsonl` |",
        f"| Unpacked sourcemap files | {stats.get('sourcemaps', 0)} | `sourcemap_files.txt` |",
        f"| Nuclei findings | {stats.get('nuclei', 0)} | `nuclei.jsonl` |",
        f"| Third-party URLs | {len(third_party_rows)} | `third_party_routes.jsonl` |",
        f"| Method probe rows | {len(method_rows)} | `method_responses.jsonl` |",
        "",
        "## High-Signal AI & API Candidates",
        "",
    ]

    ai_cands = feed.get("ai_and_api_candidates", [])
    if ai_cands:
        lines += ["| Status | Score | URL |", "|---:|---:|---|"]
        for item in ai_cands[:40]:
            lines.append(f"| {item.get('status_code', 0)} | {item.get('score', 0)} | `{item.get('url', '')}` |")
    else:
        lines.append("_No high-signal AI/API candidates surfaced._")

    lines += ["", "## Feature Flags & Role Guards", ""]
    flags = feed.get("feature_flags_and_guards", [])
    if flags:
        lines += ["| Type | Identifier | Source |", "|---|---|---|"]
        for fg in flags[:50]:
            lines.append(f"| `{fg.get('kind', '')}` | `{fg.get('name', '')}` | `{fg.get('file', '')}` |")
    else:
        lines.append("_None found._")

    lines += ["", "## Secret Candidates (Redacted)", ""]
    secs_list = feed.get("secrets", [])
    if secs_list:
        lines += ["| Tool | Detector | Verified | Redacted | File |", "|---|---|---|---|---|"]
        for sc in secs_list[:40]:
            lines.append(
                f"| `{sc.get('source', '')}` | `{sc.get('detector', '')}` | {sc.get('verified', False)} | `{sc.get('redacted', '')}` | `{sc.get('file', '')}` |"
            )
    else:
        lines.append("_None found._")

    lines += ["", "## Collapsed Route Patterns", ""]
    pats = feed.get("route_patterns", [])
    if pats:
        lines += ["| Pattern | Count | Sample |", "|---|---:|---|"]
        for pt in pats[:40]:
            lines.append(f"| `{pt.get('pattern', '')}` | {pt.get('count', 0)} | `{pt.get('sample', '')}` |")
    else:
        lines.append("_None._")

    lines += ["", "## Nuclei Findings", ""]
    nuc = feed.get("nuclei_findings", [])
    if nuc:
        lines += ["| Severity | Template | Host |", "|---|---|---|"]
        for nf in nuc[:40]:
            lines.append(f"| {nf.get('severity', '?')} | `{nf.get('template_id', '?')}` | `{nf.get('host', '')}` |")
    else:
        lines.append("_None found._")

    lines += ["", "## Tool Status", "", "| Tool | Exit | Duration (s) | Detail |", "|---|---:|---:|---|"]
    for ts in tool_statuses:
        lines.append(f"| `{ts.get('tool')}` | {ts.get('exit_code')} | {ts.get('duration_s', 0.0):.1f} | {ts.get('detail', '')} |")
    lines.append("")

    (target_dir / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")

    ctx = {
        "target": base_url,
        "host": exact_host,
        "scope_apex": scope_apex,
        "duration_seconds": round(duration_sec, 1),
        "wave_timings": wave_timings,
        "stats": stats,
        "tools": tool_statuses,
    }
    (target_dir / "context.json").write_text(json.dumps(ctx, indent=2) + "\n", encoding="utf-8")
