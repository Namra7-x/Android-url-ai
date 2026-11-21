# Web Hunt Pipeline

One-shot deep web hunt. Point it at 1–20 URLs, run it **once**, download everything it found, then pick the routes/sources you want.

**No schedule. No cron. No repeat runs.** It only starts when you click **Run workflow**.

---

## Golden rule

> **Collect wide. Verify status. Categorize last.**

- No content-type filter — JSON, HTML, XML, binary, all kept.
- No method filter — GET, POST, PUT, PATCH, DELETE, OPTIONS.
- Nothing is deleted during collection. The report is only a grouping.

### Status handling

| Status | Meaning | Label |
|---|---|---|
| **200** | Confirmed live | ✅ **WIN** |
| 301 / 302 / 303 / 307 / 308 | Redirect — route exists | 🔒 route exists but blocked |
| 401 / 403 | Auth wall — route exists | 🔒 route exists but blocked |
| 405 | Method not allowed — route exists | 🔒 route exists but blocked |
| 404 | Not found | ❌ discard |

> 301/302/401/403/405 are **logged as discovery**, not reported as leaks.
> More coverage, not less.

---

## First run (one click)

1. Open the repo on GitHub.
2. Go to **Actions** → **Web Hunt Pipeline**.
3. Click **Run workflow**.
4. Leave `urls_file` = `urls.txt` (already contains `https://openai.com`).
5. Click **Run workflow**.

When it finishes:

- Open the run → **Artifacts** → download **hunt-results**.
- Or scroll the run summary to read `REPORT.md`.

---

## Add more targets later

Edit `urls.txt`, one per line:

```
https://openai.com
https://example.com
example.org
```

Commit and push, then run the workflow again. That is the only change needed.

---

## Mega system — context-aware wordlist foundry

Tools do not work alone. Every layer writes findings, and the next layer reads them.

```
collect routes / params / chunks
        ↓
build target-specific wordlist   ← from what was actually found
        ↓
ffuf / kiterunner / arjun use it
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

Then it is scored (frequency + interesting words like `api`, `admin`, `internal`, `data`, `models`, `export`), merged, deduped and capped. A static wordlist guesses once — this one **learns the target** and guesses again.

---

## What it runs (one shot, in order)

1. **Subdomains** — subfinder `-all -recursive` + dnsx + uncover *(on; uncover needs an API key)*
2. **Chunks** — Chakra: all JS chunks, lazy chunks, routes, env vars, subdomains (`-d 10`)
3. **Framework** — js-recon: lazyload + strings + endpoints (`--max-pages 1000`, `--max-iterations 20`, `--strings`, `--subsequent-requests`)
4. **Crawl** — katana `-jc -jsl -kf all -aff` + headless `-xhr` (`-d 10`)
5. **History** — waymore + urlscan.io *(works with or without `URLSCAN_API_KEY`)*
6. **Extract** — jsluice, xnLinkFinder `-owl`, trufflehog
7. **Normalize** — dedupe only, nothing filtered
8. **Vhosts** — ffuf `Host:` brute using discovered subdomains
9. **Wordlist** — build `wordlist.txt` + `params.txt` from everything above
10. **Probe** — httpx on a uro-deduped list, all status codes
11. **Brute** — ffuf with the generated wordlist (2 rounds)
12. **API** — kiterunner with the generated wordlist
13. **Params** — arjun with the generated parameter list
14. **Methods** — GET/POST/PUT/PATCH/DELETE/OPTIONS/HEAD on live routes
15. **Feedback** — merge hits → rebuild wordlist → round 2
16. **Report** — grouped `REPORT.md` + `context.json`

---

## Output (artifact)

```
output/
  SUMMARY.md
  <host>/
    all_routes.jsonl     every route, every method
    live_200.jsonl       everything that returned 200 (any type)
    live_other.jsonl     301/302/401/403/405 = exists, blocked
    data_files.jsonl     JSON/CSV/XML/XLSX among the 200s
    params.jsonl         every parameter found
    historical.jsonl     old/removed paths
    hosts.txt            unique hosts
    secrets.jsonl        secret candidates
    subdomains.txt       raw subfinder output
    subdomains_live.txt  dnsx-resolved hosts
    subdomains_urls.txt  full URLs queued for probing
    uncover.txt          uncover results (if API key)
    vhost.json           ffuf Host-header results
    wordlist.txt         generated from THIS target's findings
    params.txt           parameter names for arjun
    context.json         shared context between layers
    kiterunner.jsonl     API brute results
    arjun.json           hidden parameter results
    brute/               raw ffuf results
    chunks/              every JS file + lazy chunks
    REPORT.md            grouped report
    logs/                raw tool logs
```

---

## Settings

`config/settings.json`:

| Key | Meaning |
|---|---|
| `enable_subdomains` | subfinder + dnsx (default `true`) |
| `enable_uncover` | Shodan/Censys/etc via uncover (default `true`; needs API key) |
| `enable_urlscan` | urlscan.io history (default `true`; key optional) |
| `enable_uro` | Deduplicate the httpx probe list (default `true`) |
| `enable_brute` | Run ffuf (default `true`) |
| `enable_vhost` | ffuf Host-header brute (default `true`) |
| `enable_methods` | Test all HTTP methods on live routes (default `true`) |
| `enable_browser` | Headless browser passes (default `true`) |
| `enable_kiterunner` | API brute with `kr` (default `true`) |
| `enable_arjun` | Hidden parameter discovery (default `true`) |
| `probe_assets` | Probe images/css/fonts too (default `false`) |
| `max_urls` | Probe cap (default `20000`) |
| `max_subdomains` | Max subdomain URLs queued (default `1000`) |
| `max_method_targets` | Live routes to method-fuzz (default `200`) |
| `method_threads` | Parallel method requests (default `20`) |
| `ffuf_rate` | Requests/sec for ffuf (default `10`) |
| `max_brute_prefixes` | How many folders to fuzz per round (default `15`) |
| `wordlist` | Base path list |
| `wordlist_max` | Max generated words (default `8000`) |
| `wordlist_rounds` | Feedback rounds (default `2`) |
| `chakra_depth` | Chakra BFS depth (default `10`) |
| `jsrecon_max_pages` | js-recon page cap (default `1000`) |
| `jsrecon_max_iterations` | js-recon crawl iterations (default `20`) |
| `katana_depth` | katana crawl depth (default `10`) |

> `probe_assets=false` only skips probing static assets to save time.
> Collection still keeps **every** URL in `all_routes.jsonl`.
> `uro` only dedupes the httpx input — no finding is deleted from the data files.

Every toggle above is also a workflow input under **Run workflow** (all default to `true`).

---

## Optional secrets

Nothing is required to run — everything works out of the box.

- `URLSCAN_API_KEY` — raises urlscan.io rate limits. The step works without it (public API).
- `SHODAN_API_KEY` / `CENSYS_API_ID` + `CENSYS_API_SECRET` / `FOFA_EMAIL` + `FOFA_KEY` / `QUAKE_TOKEN` / `HUNTER_API_KEY` / `ZOOMEYE_API_KEY` / etc. — needed by `uncover`. If none are set, uncover logs "no API key" and skips; everything else still runs.

---

## Notes

- Uses a **private repo** is recommended — artifacts and logs contain findings.
- GitHub runner IPs are datacenter IPs; Cloudflare/WAF may return 403.
  If that happens, use a self-hosted runner (`runs-on: self-hosted`).
- Only run against targets you are authorised to analyse.
- The previous project in this repo is preserved in git history.
