#!/usr/bin/env python3
"""Build results/INDEX.md + SUMMARY.md from every target's context.json."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "results")
    rows = []
    for ctx_file in sorted(root.glob("*/context.json")):
        host = ctx_file.parent.name
        try:
            ctx = json.loads(ctx_file.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        s = ctx.get("stats", {})
        rows.append((host, ctx.get("target", host), s))

    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    idx = ["# Hunt results", "", f"Generated: {now}", "",
           "Open a target's **REPORT.md** for full findings.", "",
           "| Target | Report | Accessible 200 | Exists/blocked | Subdomains | JS endpoints | Nuclei | Routes |",
           "|---|---|---:|---:|---:|---:|---:|---:|"]
    for host, target, s in rows:
        idx.append(
            f"| `{host}` | [REPORT.md]({host}/REPORT.md) | {s.get('live200', 0)} | "
            f"{s.get('liveother', 0)} | {s.get('subdomains', 0)} | {s.get('js_endpoints', 0)} | "
            f"{s.get('nuclei', 0)} | {s.get('collected', 0)} |")
    idx += ["",
            "- **Accessible 200** = confirmed live.",
            "- **Exists/blocked** = real routes returning 301/302/401/403/405.",
            "- **Nuclei** = verified exposure/misconfig findings.",
            "- Each target is pushed the moment it finishes; artifacts are per-target backups.",
            ""]
    (root / "INDEX.md").write_text("\n".join(idx), encoding="utf-8")
    (root / "SUMMARY.md").write_text(
        "\n".join(["# Summary", ""] + [f"- {t}: {json.dumps(s)}" for _, t, s in rows]) + "\n",
        encoding="utf-8")
    print(f"index: {len(rows)} targets")
    return 0


if __name__ == "__main__":
    sys.exit(main())
