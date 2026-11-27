#!/usr/bin/env python3
"""
Target-specific wordlist and parameter foundry.

Mines paths, segments, and query/body parameters from downloaded JS/JSON chunks,
unpacked sourcemaps, jsluice/xnLinkFinder/katana/scrapling/archive outputs, and
merges them with AI-discovery seed terms while filtering HTML escape junk.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import parse_qsl, urlparse

INTERESTING_TERMS = {
    "api", "apis", "admin", "administrator", "internal", "private", "hidden",
    "config", "configuration", "settings", "data", "dataset", "datasets",
    "models", "model", "capabilities", "features", "flags", "feature-flags",
    "experiments", "export", "exports", "download", "downloads", "upload",
    "uploads", "auth", "oauth", "token", "tokens", "user", "users", "account",
    "accounts", "org", "orgs", "team", "teams", "workspace", "workspaces",
    "project", "projects", "dashboard", "console", "portal", "app", "apps",
    "v1", "v1alpha", "v1beta", "v2", "v3", "v4", "graphql", "graphiql",
    "rest", "rpc", "trpc", "debug", "dev", "staging", "test", "beta", "alpha",
    "preview", "canary", "sandbox", "demo", "status", "health", "healthz",
    "readyz", "metrics", "version", "info", "docs", "swagger", "openapi",
    "redoc", "manifest", "build-manifest.json", "llms.txt", "llms-full.txt",
    "public", "static", "assets", "files", "file", "media", "cdn", "_next",
    "data.json", "$discovery",
}

SEG_RE = re.compile(r"^[A-Za-z0-9$._~-]{1,48}$")
PARAM_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_.-]{0,40}$")
QUOTED_PATH_RE = re.compile(
    r"[\"'`](/[A-Za-z0-9_\-./?=&%{}:;,@+~#\[\]$]{2,220})[\"'`]"
)
ABS_URL_RE = re.compile(r"https?://[^\s\"'<>\\\)\]\},;]+", re.I)
PARAM_KEY_RE = re.compile(
    r"(?:[?&]|[\"'`])([A-Za-z_][A-Za-z0-9_]{1,35})(?:=|[\"']\s*:)"
)

HTML_JUNK_MARKERS = (
    "<", ">", "\\u003c", "\\u003e", "%5cu003c", "%5cu003e", "%5cu003",
    "%3c", "%3e", "&lt;", "&gt;", "\\x3c", "\\x3e", "\\", "\"", "'", "`",
)

STATIC_EXT_SKIP = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".webp", ".avif",
    ".woff", ".woff2", ".ttf", ".eot", ".otf", ".mp4", ".webm", ".mp3",
    ".css", ".map",
}


def is_clean_token(token: str) -> bool:
    """Reject HTML-escaped markup, control chars, hex blobs, and empty tokens."""
    if not token or len(token) > 64:
        return False
    low = token.lower()
    if any(marker in low for marker in HTML_JUNK_MARKERS):
        return False
    if any(ch.isspace() or ord(ch) < 32 or ord(ch) > 126 for ch in token):
        return False
    if len(token) >= 24 and re.fullmatch(r"[0-9a-fA-F_-]+", token):
        return False
    return True


def _read_text(path: Path, limit: int = 4_000_000) -> str:
    try:
        if not path.is_file() or path.stat().st_size > limit:
            return ""
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _add_url_parts(url_or_path: str, segs: Counter[str], paths: Counter[str], params: Counter[str]) -> None:
    if not url_or_path or not is_clean_token(url_or_path.split("?", 1)[0][:180]):
        return
    try:
        parsed = urlparse(url_or_path)
    except ValueError:
        return
    path = parsed.path or ""
    if not is_clean_token(path) or any(path.lower().endswith(ext) for ext in STATIC_EXT_SKIP):
        return

    clean_path = path.strip("/")
    if clean_path and len(clean_path) <= 100 and clean_path.count("/") <= 4:
        if not any(part.startswith("{") or "$" in part for part in clean_path.split("/")):
            paths[clean_path] += 1

    for part in clean_path.split("/"):
        if part and SEG_RE.match(part) and is_clean_token(part):
            segs[part] += 1

    for key, _ in parse_qsl(parsed.query, keep_blank_values=True):
        if PARAM_RE.match(key) and is_clean_token(key):
            params[key] += 1


def _collect_from_files(target_dir: Path, segs: Counter[str], paths: Counter[str], params: Counter[str]) -> None:
    chunk_dirs = [target_dir / "chunks_unique", target_dir / "chunks", target_dir / "sourcemaps"]
    for cdir in chunk_dirs:
        if not cdir.exists():
            continue
        for p in sorted(cdir.rglob("*")):
            if p.suffix.lower() not in {".js", ".mjs", ".ts", ".tsx", ".jsx", ".json", ".map"}:
                continue
            text = _read_text(p)
            if not text:
                continue
            for m in QUOTED_PATH_RE.findall(text):
                _add_url_parts(m, segs, paths, params)
            for m in ABS_URL_RE.findall(text):
                _add_url_parts(m, segs, paths, params)
            for m in PARAM_KEY_RE.findall(text):
                if PARAM_RE.match(m) and is_clean_token(m):
                    params[m] += 1

    for jf in list(target_dir.glob("*.jsonl")) + list((target_dir / "katana").glob("*.jsonl") if (target_dir / "katana").exists() else []):
        text = _read_text(jf)
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            for key in ("url", "endpoint", "input"):
                val = obj.get(key)
                if isinstance(val, str):
                    _add_url_parts(val, segs, paths, params)
            req = obj.get("request")
            if isinstance(req, dict) and isinstance(req.get("endpoint"), str):
                _add_url_parts(req["endpoint"], segs, paths, params)

    for tf_name in ("waymore_urls.txt", "urlfinder_raw.txt", "scrapling_urls.txt", "xnlinkfinder_endpoints.txt"):
        text = _read_text(target_dir / tf_name)
        for line in text.splitlines():
            _add_url_parts(line.strip(), segs, paths, params)

    xn_params = _read_text(target_dir / "xn_params.txt")
    for line in xn_params.splitlines():
        tok = line.strip()
        if PARAM_RE.match(tok) and is_clean_token(tok):
            params[tok] += 3


def build(
    target_dir: str | Path,
    base_url: str,
    base_wordlist: str | Path,
    out_wordlist: str | Path,
    max_words: int = 6000,
    out_params: str | Path | None = None,
) -> dict[str, int]:
    """Generate clean target-specific wordlist.txt and params.txt."""
    tdir = Path(target_dir)
    segs: Counter[str] = Counter()
    paths: Counter[str] = Counter()
    params: Counter[str] = Counter()

    _add_url_parts(base_url, segs, paths, params)
    _collect_from_files(tdir, segs, paths, params)

    seeds: list[str] = []
    wl_path = Path(base_wordlist)
    if wl_path.is_file():
        for line in wl_path.read_text(encoding="utf-8", errors="replace").splitlines():
            w = line.strip().lstrip("/")
            if w and not w.startswith("#") and is_clean_token(w):
                seeds.append(w)

    scored: dict[str, float] = {}
    for w in seeds:
        scored[w] = max(scored.get(w, 0.0), 50.0 if w.lower() in INTERESTING_TERMS else 20.0)
    for p, cnt in paths.items():
        bonus = 30.0 if any(t in p.lower() for t in INTERESTING_TERMS) else 0.0
        scored[p] = max(scored.get(p, 0.0), cnt * 3.0 + bonus)
    for s, cnt in segs.items():
        bonus = 25.0 if s.lower() in INTERESTING_TERMS else 0.0
        scored[s] = max(scored.get(s, 0.0), cnt * 1.5 + bonus)

    ordered = [
        word for word, _ in sorted(scored.items(), key=lambda kv: (-kv[1], len(kv[0]), kv[0]))
    ][:max_words]

    out_wl = Path(out_wordlist)
    out_wl.parent.mkdir(parents=True, exist_ok=True)
    out_wl.write_text("\n".join(ordered) + ("\n" if ordered else ""), encoding="utf-8")

    param_list = [p for p, _ in params.most_common(500)]
    if out_params is not None:
        out_p = Path(out_params)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text("\n".join(param_list) + ("\n" if param_list else ""), encoding="utf-8")

    return {"words": len(ordered), "params": len(param_list)}
