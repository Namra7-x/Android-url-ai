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

1. **Subdomains** — subfinder + dnsx *(off by default)*
2. **Chunks** — Chakra: all JS chunks, lazy chunks, routes, env vars, subdomains (`-d 10`)
3. **Framework** — js-recon: lazyload + strings + endpoints (`--max-pages 1000`, `--max-iterations 20`, `--strings`, `--subsequent-requests`)
4. **Crawl** — katana `-jc -jsl -kf all -aff` + headless `-xhr` (`-d 10`)
5. **History** — waymore (+ urlscan.io if `URLSCAN_API_KEY` secret is set)
6. **Extract** — jsluice, xnLinkFinder `-owl`, trufflehog
7. **Normalize** — dedupe only, nothing filtered
8. **Wordlist** — build `wordlist.txt` + `params.txt` from everything above
9. **Probe** — httpx, all status codes
10. **Brute** — ffuf with the generated wordlist (2 rounds)
11. **API** — kiterunner with the generated wordlist
12. **Params** — arjun with the generated parameter list
13. **Feedback** — merge hits → rebuild wordlist → round 2
14. **Report** — grouped `REPORT.md` + `context.json`

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
| `enable_subdomains` | Expand subdomains (default `false`) |
| `enable_brute` | Run ffuf (default `true`) |
| `enable_browser` | Headless browser passes (default `true`) |
| `enable_kiterunner` | API brute with `kr` (default `true`) |
| `enable_arjun` | Hidden parameter discovery (default `true`) |
| `probe_assets` | Probe images/css/fonts too (default `false`) |
| `max_urls` | Probe cap (default `20000`) |
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

The same three toggles are also available as workflow inputs.

---

## Optional secret

Add repository secret `URLSCAN_API_KEY` to include urlscan.io historical requests.
Without it, that step is skipped silently.

---

## Notes

- Uses a **private repo** is recommended — artifacts and logs contain findings.
- GitHub runner IPs are datacenter IPs; Cloudflare/WAF may return 403.
  If that happens, use a self-hosted runner (`runs-on: self-hosted`).
- Only run against targets you are authorised to analyse.
- The previous project in this repo is preserved in git history.
