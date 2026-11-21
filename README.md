# Web Hunt Pipeline

One-shot, maximum-discovery web hunt. One URL per run. Results are **committed into this repo** and uploaded as an artifact — no download needed.

**No schedule. No cron.** It only starts when you click **Run workflow**.

---

## Golden rule

> **Collect wide. Verify status. Categorize last.**

- No content-type / method / shape filter during collection.
- **200** = confirmed win. **301/302/401/403/405** = route exists but blocked. Everything else kept.
- Nothing is deleted from the data files. The report is only a grouping.

---

## First run

1. **Actions** → **Web Hunt Pipeline** → **Run workflow**.
2. Leave `urls_file=urls.txt`. Add one URL per line (one URL per run is recommended).
3. Click **Run workflow**.

When it finishes, open **`results/INDEX.md`** in this repo, then the target's `REPORT.md`.

**Tool caching:** tools install once; every later run restores them from the Actions cache, so installs are skipped.

---

## Pipeline (one URL, fast, no discovery time limits)

| Order | Tool | Language | Job |
|---|---|---|---|
| 1 | subfinder + dnsx + uncover | Go | subdomains, DNS-resolved only |
| 2 | **urlfinder** | Go | 200k passive URLs in minutes, no API key needed |
| 3 | gau | Go | extra archive sources (Wayback/CommonCrawl/OTX) |
| 4 | katana (2 passes) | Go | active crawl: standard `-jc -jsl` + headless `-xhr` |
| 5 | JS downloader | Python | downloads discovered JS chunks in parallel |
| 6 | jsluice | Go | AST endpoints + secrets from JS |
| 7 | **anastasis** | Node/AST | deeper endpoints, typed params, sourcemaps |
| 8 | **jscope** | Python | evidence-backed JS findings — kills noise |
| 9 | trufflehog | Go | verified secrets (1s per 27 MB) |
| 10 | Collect + vhost | Python | dedupe everything; real Host-header hosts only |
| 11 | Wordlist foundry | Python | target-specific 8,000-word list |
| 12 | httpx | Go | probes **every** URL — this decides 200 vs blocked |
| 13 | **x8** | Rust | hidden parameter discovery |
| 14 | methods | Python | GET/POST/PUT/PATCH/DELETE/OPTIONS/HEAD |
| 15 | Report | Python | 12-section readable report |

**Not run by default:** ffuf and kiterunner (wordlist is generated and ready — flip `enable_brute` in a later run).

**Removed because they were slow or broken:** js-recon (82 min + OOM), Chakra (timeout), waymore (slow), urlscan (429), arjun (network error), xnLinkFinder (0 bytes).

---

## Noise control

- Subdomains: only DNS-resolved hosts are counted.
- Vhosts: `530` (Cloudflare) and `0` are excluded — only real statuses count.
- Params: from collected URLs + anastasis AST + x8 confirmation.
- JS findings: jscope shows only evidence-backed candidates.
- Every URL is verified by httpx; 404s are kept in `other_status.jsonl`, not shown as wins.

---

## Report sections

```
results/<host>/REPORT.md
  1. SUCCESS — HTTP 200
  2. EXISTS BUT DIFFERENT STATUS (301/302/401/403/405)
  3. OTHER RESPONSES — kept, never discarded
  4. DATA FILES (accessible)
  5. SUBDOMAINS (detailed, resolved)
  6. VIRTUAL HOSTS (real statuses only)
  7. JS ENDPOINTS (AST, evidence-backed)
  8. PARAMETERS
  9. SECRET CANDIDATES
 10. TOOL RUN STATUS (no silent skips)
 11. INTENTIONALLY NOT RUN
 12. OUTPUT FILES (sizes + links)
```

Also written: `all_routes.jsonl`, `accessible_200.jsonl`, `exists_blocked.jsonl`, `other_status.jsonl`, `data_files.jsonl`, `params.jsonl`, `subdomains.jsonl`, `js_endpoints.jsonl`, `vhost.jsonl`, `jsluice.jsonl`, `secrets.jsonl`, `wordlist.txt`, `params.txt`, `context.json`, `js_urls.txt`, `logs/`.

Old aliases `live_200.jsonl` / `live_other.jsonl` are still written.

---

## Settings

`config/settings.json` — all toggles on. `max_urls=0` and `max_subdomains=0` mean **no cap**. Safety timeouts only log and continue; they are not discovery limits.

---

## Runtime

One URL typically finishes in ~20–30 minutes including install. Cached runs are faster. The GitHub job cap is 350 minutes, which we never approach.

---

## Notes

- Private repo recommended — results contain findings.
- Cloudflare/WAF may return 403/530 from datacenter IPs; these are recorded honestly, never hidden.
- Only run against targets you are authorised to analyse.
- The previous project in this repo is preserved in git history.
