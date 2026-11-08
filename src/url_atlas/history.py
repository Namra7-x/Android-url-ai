from __future__ import annotations
import json
from pathlib import Path

def read_jsonl(path: Path):
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            if line.strip():
                rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows

def append_history(path: Path, records: list[dict]):
    previous = read_jsonl(path)
    old_urls = {r.get("url") for r in previous}
    current_urls = {r.get("url") for r in records}
    known = {(r.get("version"),r.get("url"),r.get("source_file"),r.get("extraction_method")) for r in previous}
    new = [r for r in records if r.get("url") not in old_urls]
    removed = [{"url":u,"status":"not-observed-in-current-scan"} for u in sorted(old_urls-current_urls) if u]
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("a",encoding="utf-8") as f:
        for r in records:
            key = (r.get("version"),r.get("url"),r.get("source_file"),r.get("extraction_method"))
            if key not in known:
                f.write(json.dumps(r,ensure_ascii=False,sort_keys=True)+"\n")
                known.add(key)
    return new, removed
