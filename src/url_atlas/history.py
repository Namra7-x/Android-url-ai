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
    """Append new evidence forever; compare removals with only the immediately prior scan."""
    previous_history = read_jsonl(path)
    known_urls = {r.get("url") for r in previous_history if r.get("url")}
    snapshot_path = path.with_name("latest-snapshot.json")
    if snapshot_path.exists():
        try:
            previous_snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
            old_urls = set(previous_snapshot.get("urls", []))
        except (json.JSONDecodeError, OSError):
            old_urls = set()
    else:
        # On migration from the first release, use historical URLs as the best
        # available baseline; subsequent scans use a true immediately-prior snapshot.
        old_urls = known_urls
    current_urls = {r.get("url") for r in records if r.get("url")}
    new = [r for r in records if r.get("url") not in known_urls]
    removed = [{"url":u,"status":"not-observed-in-current-scan"}
               for u in sorted(old_urls-current_urls)]
    known_records = {(r.get("version"),r.get("url"),r.get("source_file"),r.get("extraction_method"))
                     for r in previous_history}
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("a",encoding="utf-8") as stream:
        for record in records:
            key = (record.get("version"),record.get("url"),record.get("source_file"),
                   record.get("extraction_method"))
            if key not in known_records:
                stream.write(json.dumps(record,ensure_ascii=False,sort_keys=True)+"\n")
                known_records.add(key)
    snapshot = {"version": records[0].get("version") if records else None,
                "urls": sorted(current_urls)}
    snapshot_path.write_text(json.dumps(snapshot,indent=2),encoding="utf-8")
    return new, removed
