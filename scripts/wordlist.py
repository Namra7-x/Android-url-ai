#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Target-specific wordlist foundry.

Builds a wordlist from what the pipeline ACTUALLY discovered:
chunk strings, routes, params, historical URLs, static base words.

This is the "context hand-off" layer: every tool writes findings,
this module turns those findings into words for the next tool.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import parse_qsl, urlparse

INTERESTING = {
    "api", "apis", "admin", "internal", "private", "config", "configuration",
    "settings", "data", "dataset", "datasets", "models", "model", "export",
    "exports", "download", "downloads", "upload", "uploads", "auth", "oauth",
    "token", "tokens", "user", "users", "account", "accounts", "org", "orgs",
    "team", "teams", "workspace", "workspaces", "project", "projects",
    "dashboard", "console", "portal", "app", "apps", "v1", "v2", "v3", "v4",
    "graphql", "rest", "rpc", "trpc", "debug", "dev", "staging", "test",
    "beta", "alpha", "preview", "sandbox", "demo", "status", "health",
    "metrics", "version", "info", "docs", "swagger", "openapi", "redoc",
    "manifest", "public", "static", "assets", "files", "file", "media",
    "cdn", "_next", "next", "data.json",
}

EXT_PRIORITY = [
    "json", "jsonl", "ndjson", "xml", "csv", "xlsx",
    "txt", "html", "php", "aspx", "js",
]

SEG_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,39}$")
EXT_RE = re.compile(r"\.([A-Za-z]{1,8})$")
QUOTED_PATH_RE = re.compile(
    r"[\"'`](/[A-Za-z0-9_\-./?=&%{}:;,@+~#\[\]]{2,250})[\"'`]"
)
ABS_RE = re.compile(r"https?://[^\s\"'<>\\\)\]\},;]+", re.I)


def _read(path, limit: int = 8_000_000) -> str:
    try:
        p = Path(path)
        if p.stat().st_size > limit:
            return ""
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        return ""


def _json_strings(obj, out):
    if isinstance(obj, str):
        out.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            _json_strings(v, out)
    elif isinstance(obj, list):
        for v in obj:
            _json_strings(v, out)


def _raw_strings(target_dir: Path):
    out = []
    for p in target_dir.rglob("*"):
        if not p.is_file():
            continue
        if "logs" in p.parts:
            continue
        name = p.name.lower()
        if name in ("wordlist.txt", "params.txt", "urls_to_probe.txt"):
            continue
        suffix = p.suffix.lower()

        if suffix == ".js":
            t = _read(p)
            if not t:
                continue
            out.extend(m.group(1) for m in QUOTED_PATH_RE.finditer(t))
            out.extend(m.group(0) for m in ABS_RE.finditer(t))
        elif suffix == ".json":
            t = _read(p)
            if not t:
                continue
            try:
                _json_strings(json.loads(t), out)
            except Exception:  # noqa: BLE001
                pass
        elif suffix == ".jsonl":
            for line in _read(p).splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    _json_strings(json.loads(line), out)
                except Exception:  # noqa: BLE001
                    pass
        elif suffix in (".txt", ".csv", ".md"):
            out.extend(_read(p).splitlines())

    return out


def build(target_dir, base: str, static_file: str, out_file: str,
          max_words: int = 8000, param_file: str | None = None) -> dict:
    target_dir = Path(target_dir)
    base_host = urlparse(base).netloc.lower()
    if base_host.startswith("www."):
        base_host = base_host[4:]

    seg = Counter()
    multi = Counter()
    exts = Counter()
    params = Counter()

    def feed(raw):
        raw = (raw or "").strip().strip("\"'`,;)]}>")
        if not raw:
            return
        if raw.startswith("//"):
            raw = "https:" + raw

        if re.match(r"^https?://", raw, re.I):
            try:
                p = urlparse(raw)
            except (ValueError, TypeError):
                # Broken bracketed hosts (e.g. "http://[abc") are junk from
                # minified JS. Skip only this string, never the whole run.
                return
            host = p.netloc.lower()
            if host.startswith("www."):
                host = host[4:]
            if not host or host != base_host:
                return
            path = p.path or "/"
            for k, _ in parse_qsl(p.query, keep_blank_values=True):
                if k and len(k) <= 40:
                    params[k.lower()] += 1
        elif raw.startswith("/"):
            path = raw.split("?")[0]
        else:
            return

        parts = [x for x in path.split("/") if x]
        clean = []
        for part in parts:
            part = part.split(";")[0]
            m = EXT_RE.search(part)
            if m:
                e = m.group(1).lower()
                if 1 <= len(e) <= 8:
                    exts[e] += 1
                part = part[:m.start()]
            if SEG_RE.match(part) and len(part) >= 2:
                clean.append(part.lower())

        for c in clean:
            seg[c] += 1

        # multi-segment words (api/v2/users)
        for i in range(len(clean)):
            for depth in (2, 3):
                if i + depth <= len(clean):
                    multi["/".join(clean[i:i + depth])] += 1
        if 2 <= len(clean) <= 4:
            multi["/".join(clean)] += 1

    for s in _raw_strings(target_dir):
        feed(s)

    base_words = set()
    for line in _read(static_file).splitlines():
        line = line.strip().lower()
        if line and not line.startswith("#"):
            base_words.add(line)

    words: dict[str, int] = {}

    def add(w: str, score: int):
        w = (w or "").strip().lower().strip("/")
        if not w or len(w) < 2 or len(w) > 120:
            return
        if any(ch in w for ch in " \t\"'<>\\"):
            return
        if w not in words or score > words[w]:
            words[w] = score

    for w in base_words:
        add(w, 1)

    for w, c in seg.items():
        add(w, c + (8 if w in INTERESTING else 0))

    for w, c in multi.items():
        boost = 5
        if w.split("/")[0] in INTERESTING:
            boost += 5
        add(w, c + boost)

    # segment + observed extension
    for w, c in seg.items():
        for e in EXT_PRIORITY:
            if exts.get(e):
                add(f"{w}.{e}", c + 2)

    ordered = sorted(words.items(), key=lambda kv: (-kv[1], kv[0]))
    final = [w for w, _ in ordered[:max_words]]

    out_path = Path(out_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(final) + "\n", encoding="utf-8")

    if param_file:
        pf = Path(param_file)
        pf.parent.mkdir(parents=True, exist_ok=True)
        pf.write_text("\n".join(sorted(params)) + "\n", encoding="utf-8")

    return {
        "wordlist": str(out_path),
        "count": len(final),
        "segments": len(seg),
        "multi": len(multi),
        "params": len(params),
        "extensions": dict(exts.most_common(20)),
    }
