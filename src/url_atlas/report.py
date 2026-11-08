from __future__ import annotations

import csv
import json
from pathlib import Path

FIELDS = [
    "app", "version", "url", "domain", "category", "source_file",
    "evidence_type", "extraction_method", "encoding", "confidence",
]


def write_reports(out: Path, app: str, version: str, rows: list[dict],
                  new: list[dict], removed: list[dict]):
    out.mkdir(parents=True, exist_ok=True)

    def lines(name, values):
        (out / name).write_text("".join(value + "\n" for value in values), encoding="utf-8")

    # Preserve every evidence row and its source, while making the plain URL
    # inventory free of bare-domain references and other non-URL strings.
    with (out / "all-urls.jsonl").open("w", encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    with (out / "all-urls.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    by_url = {}
    for row in rows:
        by_url.setdefault(row["url"], row.get("category", ""))
    urls = sorted(url for url, category in by_url.items() if category != "domain-reference")
    domains = sorted({row["domain"] for row in rows if row.get("domain")})
    domain_references = sorted({
        row["url"] for row in rows if row.get("category") == "domain-reference"
    })
    api = sorted({row["url"] for row in rows if row.get("category") == "api"})
    websocket = sorted({row["url"] for row in rows if row.get("category") == "websocket"})
    deep_links = sorted({row["url"] for row in rows if row.get("category") == "custom-uri"})
    platform = sorted({row["url"] for row in rows if row.get("category") == "platform-uri"})
    new_urls = sorted({row["url"] for row in new if row.get("category") != "domain-reference"})

    lines("all-urls.txt", urls)
    lines("domains.txt", domains)
    lines("domain-references.txt", domain_references)
    lines("api-endpoints.txt", api)
    lines("websocket-endpoints.txt", websocket)
    lines("deep-links.txt", deep_links)
    lines("platform-uris.txt", platform)
    lines("new-urls.txt", new_urls)
    lines("removed-urls.txt", sorted({row["url"] for row in removed}))

    counts = {}
    for row in rows:
        category = row.get("category", "unknown")
        counts[category] = counts.get(category, 0) + 1

    report = [
        f"# URL Atlas: {app}", "",
        f"- Version: {version}",
        f"- Evidence rows: {len(rows)}",
        f"- Unique URL candidates (excluding bare domains): {len(urls)}",
        f"- Unique domain references: {len(domain_references)}",
        f"- Unique hostnames: {len(domains)}",
        f"- First-seen URLs: {len(new_urls)}",
        f"- Previously known URLs not observed now: {len(removed)}",
        "", "## Evidence by category", "",
    ]
    report.extend(f"- {category}: {count}" for category, count in sorted(counts.items()))
    report.extend([
        "", "## Coverage limitation", "",
        "These are static URL candidates found in acquired and scanned package files. "
        "Static analysis cannot guarantee discovery of URLs assembled at runtime, "
        "returned by remote configuration, encrypted, or enabled only for particular "
        "accounts, regions, experiments, or server responses. A missing URL means "
        "not observed in this artifact, not proof that the service no longer uses it.",
        "",
    ])
    (out / "report.md").write_text("\n".join(report), encoding="utf-8")
