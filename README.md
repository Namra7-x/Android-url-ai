# Web Hunt Pipeline

One-shot, maximum-discovery web hunt. **Multiple URLs supported** — one parallel
job per URL. Each job pushes its results to `results/<host>/` the moment it
finishes and uploads its own artifact, so a slow/failing/cancelled URL never
blocks or loses the others.

**No schedule.** Manual trigger only: **Actions → Web Hunt Pipeline → Run workflow**.

---

## Golden rule

> Collect wide. Verify status. Categorize last. Nothing is deleted.

- **200** = confirmed win. **301/302/401/403/405** = exists but blocked.
- Everything else kept in `other_status.jsonl`.
- Noise (third-party, method probes, blocked vhosts) is **kept in separate files**, never mixed into the headline counts.

---

## Speed architecture

- **Zero installs on repeat runs.** A dedicated `tools` job warms a full cache
  (Go bins + build cache, pip `--user`, Anastasis folder, Chrome, nuclei templates,
  prebuilt binaries). Hunt jobs restore it and install nothing.
- **Installer only installs what's missing** (`have <tool> || install`), and
  `restore-keys` means even after installer edits the previous cache is reused.
- **One job per URL** (`max-parallel` input, default 3) → N URLs ≈ time of one.
- **jsluice batched** (100 files/process) instead of 2 processes/file.
- **Recursive JS chunk download** (3 rounds) feeds jsluice/anastasis/jscope.
- **anastasis local-first** (`-fs chunks`) — no flaky network dependency.

---

## Tool stack (latest, verified)

| Layer | Tool | Note |
|---|---|---|
| Subdomains | subfinder + dnsx + uncover | Go |
| Passive URLs | **urlfinder @dev** + waybackurls | dev has the source fixes missing from v0.0.3; gau dropped (open no-output bug) |
| Crawl | katana v1.8 (2 passes) + **cariddi** | cariddi = crawl + secrets + endpoints + juicy files, one pass |
| JS seeds | getJS + subjs | |
| JS parse | jsluice (batched) + anastasis (local) + jscope | |
| Secrets | trufflehog (verify) + **noseyparker** (GB/s bulk) | |
| Probe | httpx (all statuses) + uro dedupe | |
| Params | x8 (Rust) + methods | |
| Findings | **nuclei** (exposure/misconfig/tech/panel on live hosts) | real verified findings |
| Vhosts | pure-Python Host-header check | Cloudflare 403/530 excluded from "real" |
| Fuzz (off) | ffuf + kiterunner | wordlist always generated |

---

## Results

```
results/
  INDEX.md            rebuilt by aggregate job from every target
  SUMMARY.md
  <host>/
    REPORT.md         13 sections incl. route-patterns + nuclei findings
    accessible_200.jsonl / exists_blocked.jsonl / other_status.jsonl
    data_files.jsonl / params.jsonl / subdomains.jsonl
    js_endpoints.jsonl / jsluice.jsonl / noseyparker.jsonl / nuclei.jsonl
    third_party_routes.jsonl / method_responses.jsonl / vhost_*.jsonl
    wordlist.txt / params.txt / context.json / js_urls.txt / logs/
```

Per-target **artifact** (`hunt-<host>`) uploaded as backup.

---

## Report sections

0 Top route patterns (IDs collapsed) · 1 Accessible 200 · 2 Exists/blocked ·
3 Other · 4 Data files · 5 Subdomains · 6 Vhosts · 7 JS endpoints · 8 Params ·
9 Secrets · 10 Nuclei findings · 11 Tool run status · 12 Not run · 13 Output files.

---

## Settings

`config/settings.json` — all discovery on; `enable_brute:false`;
`enable_result_push:true`; `max_urls:0` (no cap). `nuclei_max_targets`,
`jsluice_batch`, `js_crawl_rounds` tune speed/depth.

---

## Notes

- Private repo recommended (results contain findings).
- Runner IPs are datacenter; WAF 403/530 recorded honestly, never hidden.
- Only test targets you are authorised to analyse.
