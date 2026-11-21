# Web Hunt Pipeline

One-shot deep web hunt. Point it at 1–20 URLs, run it **once**, and browse every finding directly in this repo.

**No schedule. No cron.** It only starts when you click **Run workflow**.

---

## Golden rule

> **Collect wide. Verify status. Categorize last.**

- No content-type filter — JSON, HTML, XML, binary, all kept.
- No method filter — GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD.
- **Nothing is deleted during collection.** The report is only a grouping.

### Status handling

| Status | Meaning | How the report labels it |
|---|---|---|
| **200** | Confirmed live | **Accessible — confirmed win** |
| 301 / 302 / 303 / 307 / 308 | Redirect — route exists | Exists but not accessible |
| 401 / 403 | Auth wall — route exists | Exists but not accessible |
| 405 | Method not allowed — route exists | Exists but not accessible |
| 404 / 500 / timeout | Not found / error | Other responses — kept, never discarded |

> "Exists but not accessible" is **discovery**, not a leak. More coverage, not less.

---

## First run (one click)

1. Open this repo on GitHub.
2. **Actions** → **Web Hunt Pipeline** → **Run workflow**.
3. Leave the defaults (`urls_file=urls.txt`, everything else on).
4. Click **Run workflow**.

When it finishes, **open the `results/` folder in this repo**:

- **`results/INDEX.md`** — one row per target, with a link to its report.
- **`results/openai.com/REPORT.md`** — the full human-readable report.

The workflow commits results back to the repo, so **you do not need to download anything**. An artifact is also uploaded as a backup.

---

## Add more targets later

Edit `urls.txt`, one per line:

```
https://openai.com
https://example.com
example.org
```

Commit and push, then run the workflow again. Each target gets its own `results/<host>/` folder.

---

## Mega system — context-aware wordlist foundry

Tools do not work alone. Every layer writes findings, and the next layer reads them.

```
collect routes / params / chunks
        ↓
build target-specific wordlist   ← from what was actually found
        ↓
kiterunner / arjun use it now; ffuf can use it later
        ↓
new routes / params found
        ↓
merge into context → rebuild wordlist → run again
```

The wordlist is generated **per target** from:

- Chakra `_routes.txt` + all chunk strings
- js-recon `extracted_urls.json` + `strings.json`
- katana URLs (both passes)
- jsluice URLs
- xnLinkFinder `-owl` wordlist
- waymore historical URLs
- every parameter name found
- base `wordlists/common.txt`

Scored by frequency + interesting words (`api`, `admin`, `internal`, `data`, `models`, `export`), merged, deduped and capped. **ffuf path brute is OFF by default** (it would take hours) — but `wordlist.txt` is always generated, so you can turn it on in a later run with no extra setup.

---

## What it runs (one shot, in order)

Every tool is installed and verified **before** the hunt starts. A missing tool fails the job loudly — no silent skips.

1. **Verify tools** — all 17 binaries checked; job fails if any are missing.
2. **Subdomains** — subfinder `-all -recursive` + dnsx + uncover *(uncover needs an API key for data)*
3. **Chunks** — Chakra: all JS chunks, lazy chunks, routes, env vars, subdomains (`-d 10`)
4. **Framework** — js-recon: lazyload → strings → subsequent requests → endpoints (`--max-pages 1000`, `--max-iterations 20`)
5. **Crawl** — katana `-jc -jsl -kf all -aff` + headless `-xhr` (`-d 10`)
6. **History** — waymore + urlscan.io *(works with or without `URLSCAN_API_KEY`)*
7. **Extract** — jsluice, xnLinkFinder (`-d 3`, `-owl`), trufflehog
8. **Normalize** — dedupe only, nothing filtered
9. **Vhosts** — pure-Python `Host:` header discovery using discovered subdomains (**no ffuf needed**)
10. **Wordlist** — build `wordlist.txt` + `params.txt` from everything above
11. **Probe** — httpx on a uro-deduped list, all status codes
12. **API brute** — kiterunner with the generated wordlist
13. **Params** — arjun with the generated parameter list
14. **Methods** — GET/POST/PUT/PATCH/DELETE/OPTIONS/HEAD on live routes
15. **Report** — grouped `REPORT.md` + `context.json`, then committed to the repo

> ffuf path brute is intentionally off — see [What is not run](#what-is-not-run).

---

## Results in the repo

```
results/
  INDEX.md                  ← start here (links to every target)
  SUMMARY.md
  openai.com/
    REPORT.md               ← the readable report
    all_routes.jsonl        every route, unfiltered
    accessible_200.jsonl    HTTP 200 — confirmed accessible
    exists_blocked.jsonl    301/302/401/403/405 — exists, blocked
    other_status.jsonl      404/500/etc. — kept, not discarded
    data_files.jsonl        JSON/CSV/XML/spreadsheet among the 200s
    params.jsonl            parameters found
    historical.jsonl        old/removed paths
    hosts.txt               every host
    secrets.jsonl           secret candidates
    wordlist.txt            generated wordlist — ready for ffuf
    params.txt              generated parameter wordlist
    context.json            shared context between layers
    js_urls.txt             all discovered JS file URLs
    subdomains_all.txt      all discovered subdomains
    subdomains_live.txt     DNS-resolved subdomains
    vhost.jsonl             virtual-host results
    xnlinkfinder.txt        endpoints from xnLinkFinder
    kiterunner.jsonl        API brute results
    arjun.json              hidden parameter results
    logs/                   raw tool output — check here for any error
```

Old names `live_200.jsonl` / `live_other.jsonl` are also written as aliases.

Heavy `chunks/` and `sourcemaps/` folders are kept in the artifact only, not committed, to keep the repo small.

---

## Reading the report

`REPORT.md` has 10 clear sections:

1. Accessible — HTTP 200
2. Exists but not accessible — 301/302/401/403/405
3. Data files (accessible)
4. Other responses — kept, never discarded
5. Parameters discovered
6. Hosts discovered (apex / subdomains / virtual hosts)
7. Secret candidates
8. **Tool run status** — exactly which tools ran, their exit codes, and why a tool returned no data
9. Intentionally not run
10. Output files (with sizes and links)

Section 8 is the "no silent skips" check: if a tool had a problem, it is visible there and its error tail is printed in the workflow console.

---

## What is not run

- **ffuf path brute force** — off by default because 15 folders × 8,000 words × 2 rounds would take hours. `wordlist.txt` is generated and ready. To run it, set `enable_brute: true` in the **Run workflow** inputs (or in `config/settings.json`).
- **uncover data** — no API key means the tool runs but returns no hosts. This is reported in section 8, not hidden.

---

## Settings

`config/settings.json`:

| Key | Meaning |
|---|---|
| `enable_subdomains` | subfinder + dnsx (default `true`) |
| `enable_uncover` | Shodan/Censys/etc via uncover (default `true`; needs API key) |
| `enable_urlscan` | urlscan.io history (default `true`; key optional) |
| `enable_uro` | Deduplicate the httpx probe list (default `true`) |
| `enable_brute` | ffuf path brute (default **`false`**) |
| `enable_vhost` | Virtual-host discovery, no ffuf (default `true`) |
| `enable_methods` | Test all HTTP methods on live routes (default `true`) |
| `enable_browser` | Headless browser passes (default `true`) |
| `enable_kiterunner` | API brute with `kr` (default `true`) |
| `enable_arjun` | Hidden parameter discovery (default `true`) |
| `probe_assets` | Probe images/css/fonts too (default `false`) |
| `max_urls` | Probe cap (default `20000`) |
| `max_subdomains` | Max subdomain URLs queued (default `1000`) |
| `max_method_targets` | Live routes to method-fuzz (default `200`) |
| `method_threads` | Parallel requests for vhost + methods (default `20`) |
| `ffuf_rate` | Requests/sec **when ffuf is enabled later** (default `50`) |
| `wordlist_max` | Max generated words (default `8000`) |
| `wordlist_rounds` | Feedback rounds when ffuf is on (default `2`) |
| `chakra_depth` | Chakra BFS depth (default `10`) |
| `jsrecon_max_pages` | js-recon page cap (default `1000`) |
| `jsrecon_max_iterations` | js-recon crawl iterations (default `20`) |
| `katana_depth` | katana crawl depth (default `10`) |

Every toggle is also a workflow input under **Run workflow**.

> `probe_assets=false` only skips probing static assets to save time — collection still keeps every URL in `all_routes.jsonl`.
> `uro` only dedupes the httpx input — no finding is deleted from the data files.

---

## Optional secrets

Nothing is required to run — everything works out of the box.

- `URLSCAN_API_KEY` — raises urlscan.io rate limits. Works without it (public API).
- `SHODAN_API_KEY` / `CENSYS_API_ID` + `CENSYS_API_SECRET` / `FOFA_EMAIL` + `FOFA_KEY` / `QUAKE_TOKEN` / `HUNTER_API_KEY` / `ZOOMEYE_API_KEY` / etc. — needed by `uncover` to return data. Without them it still runs and reports "no API key".

---

## Runtime

With ffuf off, a full run takes roughly **1–2 hours** (tool install + all discovery layers). The job limit is **350 minutes (5h50m)**, so there is comfortable headroom. Enabling ffuf adds about 40 minutes per round.

---

## Notes

- This is a **private repo** — results, artifacts and logs contain findings.
- GitHub runner IPs are datacenter IPs; Cloudflare/WAF may return 403. Those are recorded as "exists but not accessible", never hidden.
- Only run against targets you are authorised to analyse.
- The previous project in this repo is preserved in git history.
