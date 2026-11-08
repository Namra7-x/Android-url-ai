from __future__ import annotations
import csv, json
from pathlib import Path
FIELDS=["app","version","url","domain","category","source_file","evidence_type","extraction_method","encoding","confidence"]

def write_reports(out: Path, app: str, version: str, rows: list[dict], new: list[dict], removed: list[dict]):
    out.mkdir(parents=True,exist_ok=True)
    def lines(name, values):
        (out/name).write_text("".join(v+"\n" for v in values),encoding="utf-8")
    with (out/"all-urls.jsonl").open("w",encoding="utf-8") as f:
        for r in rows: f.write(json.dumps(r,ensure_ascii=False,sort_keys=True)+"\n")
    with (out/"all-urls.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,extrasaction="ignore"); w.writeheader(); w.writerows(rows)
    urls=sorted({r["url"] for r in rows})
    domains=sorted({r["domain"] for r in rows if r.get("domain")})
    lines("all-urls.txt",urls); lines("domains.txt",domains)
    lines("api-endpoints.txt",sorted({r["url"] for r in rows if r["category"]=="api"}))
    lines("websocket-endpoints.txt",sorted({r["url"] for r in rows if r["category"]=="websocket"}))
    lines("deep-links.txt",sorted({r["url"] for r in rows if r["category"]=="custom-uri"}))
    lines("new-urls.txt",sorted({r["url"] for r in new}))
    lines("removed-urls.txt",sorted({r["url"] for r in removed}))
    report=[f"# URL Atlas: {app}","",f"- Version: {version}",f"- Evidence rows: {len(rows)}",
      f"- Unique URL candidates: {len(urls)}",f"- Unique domains: {len(domains)}",
      f"- First-seen URLs: {len({r['url'] for r in new})}",
      f"- Previously known URLs not observed now: {len(removed)}","",
      "## Coverage limitation","",
      "These are URL candidates found in scanned files. Static and dynamic inspection cannot prove that every possible endpoint is known. Remote configuration, account/region conditions, runtime construction and untested server responses may expose additional URLs.",""]
    (out/"report.md").write_text("\n".join(report),encoding="utf-8")
