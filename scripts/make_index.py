#!/usr/bin/env python3
"""Build results/INDEX.md and results/SUMMARY.md from every target's context.json."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path


def _fmt_duration(seconds: object) -> str:
    try:
        total = max(0, int(round(float(seconds))))
    except (TypeError, ValueError):
        return "-"
    mins, secs = divmod(total, 60)
    return f"{mins}:{secs:02d}"


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "results")
    root.mkdir(parents=True, exist_ok=True)
    rows = []

    for ctx_file in sorted(root.glob("*/context.json")):
        host = ctx_file.parent.name
        try:
            ctx = json.loads(ctx_file.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        stats = ctx.get("stats", {}) or {}
        duration = ctx.get("duration_seconds", stats.get("duration_seconds"))
        rows.append((host, ctx.get("target", host), stats, duration))

    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    idx = [
        "# Hunt Results",
        "",
        f"Generated: {now}",
        "",
        "Open a target's **REPORT.md** for the human summary or **ai_feed.json** for compact LLM-ready leads.",
        "",
        "| Target | Duration | Report | AI Feed | Accessible 200 | Exists/Blocked | Subdomains | JS Endpoints | Secrets/Flags | AI Leads | Nuclei | Routes |",
        "|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for host, _target, s, duration in rows:
        secrets_flags = f"{s.get('secrets', 0)}/{s.get('flags', 0)}"
        feed_link = f"[ai_feed.json]({host}/ai_feed.json)" if (root / host / "ai_feed.json").exists() else "-"
        idx.append(
            f"| `{host}` | {_fmt_duration(duration)} | [REPORT.md]({host}/REPORT.md) | {feed_link} | "
            f"{s.get('live200', 0)} | {s.get('liveother', 0)} | {s.get('subdomains', 0)} | "
            f"{s.get('js_endpoints', 0)} | {secrets_flags} | {s.get('ai_endpoints', 0)} | "
            f"{s.get('nuclei', 0)} | {s.get('collected', 0)} |"
        )

    idx += [
        "",
        "- **Duration** = wall-clock time (`min:sec`, capped at `<= 12:00`).",
        "- **AI Feed** = deduplicated, ranked intelligence JSON (`ai_feed.json`) for LLM analysis.",
        "- **Secrets/Flags** = secret candidates (`titus` + `trufflehog` + `jsluice` + `xnLinkFinder`) / feature flags & role guards (`Jscope`).",
        "- **AI Leads** = `/v1alpha`, `/v1beta`, `/api/`, `graphql`, `llms.txt`, `openapi`, `$discovery`, model/config routes.",
        "- **Accessible 200** = confirmed live routes; **Exists/Blocked** = `301/302/401/403/405`.",
        "",
    ]

    (root / "INDEX.md").write_text("\n".join(idx), encoding="utf-8")
    summary_lines = ["# Summary", ""]
    for host, target, s, duration in rows:
        payload = {"duration": _fmt_duration(duration), **s}
        summary_lines.append(f"- `{host}` ({target}): {json.dumps(payload, sort_keys=True)}")
    (root / "SUMMARY.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
    print(f"index: {len(rows)} targets")
    return 0


if __name__ == "__main__":
    sys.exit(main())
