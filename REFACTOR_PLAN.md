# Android-url-ai — Complete High-Speed Concurrent Refactor Plan

> **Status:** Research-verified architecture & refactor blueprint (2026-11-27).  
> **Scope:** Full overhaul of `.github/workflows/hunt.yml`, `scripts/install_tools.sh`, `scripts/hunt.py`, `scripts/wordlist.py`, `scripts/make_index.py`, and `config/settings.json` in `D:\vibee\Android-url-ai`.  
> **Core Guarantees:**
> 1. **10–12 minutes MAX per target URL** (down from 100–148 minutes).
> 2. **Full concurrency** across every URL in `urls.txt` AND across multiple simultaneous GitHub Actions triggers (`N` URLs finishes in ~the time of `1` URL).
> 3. **Install once, reuse everywhere** via a compact, fast `actions/cache@v4` binary + browser toolchain cache.
> 4. **Zero missed findings / nothing deleted** — 100% of raw discoveries stay on disk, while a clean deduplicated `ai_feed.json` + `REPORT.md` surfaces unreleased AI models, feature flags, `/v1alpha/` endpoints, and secrets for AI analysis.

---

## 1. Root-Cause Audit of the Current Pipeline (Verified from Logs & GitHub Issues)

Real run logs inside `results/*/` and upstream GitHub issue/release checks exposed **9 concrete failures** causing 2-hour runtimes and missed endpoints:

| Tool / Component | Observed Failure in Current Runs | Upstream GitHub / Root Cause | Action in New Plan |
|---|---|---|---|
| **`urlfinder`** | Returned **`Found 0 urls in 218–273 microseconds`** (`1B` output) on all 5 targets (`www.perplexity.ai`, `aistudio.google.com`, `devin.ai`, `claude.ai`, `gemini.google.com`). | `scripts/hunt.py` passes `-max-time 0`. In `projectdiscovery/urlfinder` (`dev/internal/runner/enumerate.go`), `MaxEnumerationTime * time.Minute = 0ns`, triggering an instant deadline timeout and exiting with `exit 0` so fallback never runs. Also tagged release is still `v0.0.3` (Mar 2025) and Issue `#182` hides warnings unless `-v` is set. | **Fix flags** (`-max-time 2`, root domain, `-v`) **+ pair with `waymore v8.9`** as primary historical engine. |
| **`waybackurls`** | Returned **`1B` or `MISSING`** across all 5 tested targets. | `tomnomnom/waybackurls` last released `v0.1.0` in **April 2022**; has multiple 2026 issues (`#69`, `#65`, `#66`, `#53`, `#59`) reporting `"No Output"` / `"not working at all"` due to un-retried Wayback CDX throttling. | **Drop** and replace with **`xnl-h4ck3r/waymore` (`v8.9`)**. |
| **`noseyparker`** | `MISSING` on 4 targets; `1B` (0 hits) on `devin.ai`. | `praetorian-inc/noseyparker` was **officially retired & archived on April 24, 2026**, succeeded by **`praetorian-inc/titus`**. | **Replace with `praetorian-inc/titus`** (487 rules + live validation + archive unpacking). |
| **`anastasis`** | Crashed with `npm error enoent [exit 254]` on `aistudio.google.com` & `gemini.google.com`; crashed with `ENOENT ... anastasis.json.tmp` on `claude.ai`; dumped `28,157` localized `/ar-SA/hub/blog/{id}` HTML garbage rows on `www.perplexity.ai`. | Wrapper `cd`s into `$HOME/tools/Anastasis` (breaking relative paths) and crashes on modern/large bundles. | **Drop** and replace with **`xnLinkFinder v8.2`** + **`jsluice`** + **`Jscope`**. |
| **`katana`** | Burned **`123m 36s`** on `aistudio.google.com` and **`148m 31s`** on `gemini.google.com`; blocked on `/cdn-cgi/challenge-platform` on `claude.ai` & `www.perplexity.ai`. | Sequential Pass 1 + Pass 2 at `-d 5` with no time cap, no similarity dedup, no `chrome-headless-shell`, and no Cloudflare Turnstile solver. | **Upgrade to `v1.8.0` flags** (`chrome-headless-shell`, `-d 3`, `-jsl`, similarity dedup, `180s` hard timeout) **+ pair with `Scrapling v0.5.1`**. |
| **`cariddi`** | `MISSING` on `aistudio`, `claude`, `gemini`; `263B` (7 lines) on `perplexity.ai`. | Go HTTP client immediately 403/challenged by Cloudflare/Google WAFs; only worked on unprotected `devin.ai`. | **Drop** in favor of **`Scrapling v0.5.1` + `katana v1.8.0`**. |
| **`subfinder`** | Found **`0` subdomains** on `www.perplexity.ai` and only `www.aistudio.google.com` on `aistudio`. | `hunt.py` ran `subfinder -d <host>` without stripping to the **apex root domain** (`perplexity.ai`), and didn't use `v2.17.0` filters. | **Extract apex root domain** before `subfinder v2.17.0` (`crtname`, `subdomaincenter`, regex filters). |
| **`x8`** | Returned `69B–81B` (5-line banner, **0 parameters**) across all 5 targets. | Aimed only at homepage `/` (`-u https://target/`) instead of live `/api/...` routes. | **Run `x8` only against top discovered live API/POST/JSON endpoints** (with strict time cap). |
| **`jscope`** | Extracted real early-leak leads on `devin.ai` (`role:admin`, `feature_flag:toolbarDebugMode`, `feature_flag:distributedTracing`), **but all 8 analyzers crashed** with `RecursionError` on `aistudio.google.com`. | Deeply nested minified JS AST exceeded Python's default `1000`-frame recursion depth. | **Keep `Jscope v1.0.0`** with a wrapper setting `sys.setrecursionlimit(10000)` + chunk size/timeout guards. |
| **`kiterunner` (`kr`)** | Installed & cached even though `enable_kiterunner: false` in `config/settings.json`. | Last formal release `v1.0.2` in **April 2021** (`51` open issues). | **Drop**; replace brute-forcing with time-capped **`feroxbuster v2.14.0` / `ffuf v2.3.0`**. |

---

## 2. Final Curated Tool Stack & Newly Introduced 2025–2026 Features

### A. Active Toolchain (Every Tool Has One Clear Job)

| Stage | Tool & Version | Key Role in Hunt | New 2025–2026 Features Used | Hard Timeout Cap |
|---|---|---|---|---|
| **1. Subdomains & DNS** | **`subfinder v2.17.0`** + **`dnsx`** + optional `uncover` | Finds hidden staging/beta/dev/canary subdomains on the **apex domain** and resolves live IPs/CNAMEs. | `subfinder v2.17.0`: `crtname` & `subdomaincenter` sources, `-match-regex`/`-filter-regex`, ZoomEye v2. | **60s** |
| **2. WAF Bypass & Live XHR** | **`D4Vinci/Scrapling v0.5.1`** | Bypasses Cloudflare Turnstile (`claude.ai`, `perplexity.ai`), captures live `XHR`/`fetch`/GraphQL/WebSocket URLs, harvests `<script>` chunks, and fetches direct AI discovery paths (`/llms.txt`, `openapi.json`, `$discovery`). | `v0.5.0–v0.5.1`: streamlined `StealthyFetcher` & `AsyncFetcher`, faster Turnstile solver, `RemoteSession` / `new_context=False` cookie reuse, BFS/DFS spider. *(Note: avoid calling `.relocate()` on `Response` per open Issue `#600`.)* | **120s** |
| **3. Deep SPA & AST Crawl** | **`katana v1.8.0`** | Hybrid crawler (`chrome-headless-shell`) for deep SPA routes, forms, XHRs, known files (`robots`, `sitemap`), and inline JS. | `v1.6–v1.8`: **`chrome-headless-shell`** (lighter/faster than full Chrome), pure-Go **CGO-free `jsluice`** (`-jsl`), `secrets`+`endpoints` extractors, **content-similarity dedup** (stops scanning 189 identical localized pages!). | **180s** |
| **4. Historical URLs & Old JS** | **`waymore v8.9`** + fixed **`urlfinder`** | Pulls historical URLs & archived JS snapshots from Wayback, CommonCrawl, OTX, URLScan, VT, and GhostArchive. | `waymore v8.x`: **GhostArchive** source, `v8.8` outbound HTTP timeouts (stops hanging), `v8.9` long-filename crash fix, `-mode R` archived JS downloads. `urlfinder`: fixed `-max-time 2` on root domain + `-v`. | **150s** |
| **5. Local JS Chunk Parsing** | **`jsluice`** + **`xnLinkFinder v8.2`** | Runs offline over all downloaded `.js`/`.mjs`/`.json` chunks (0 WAF risk!) to extract `/v1alpha/`, `/api/`, GraphQL ops, params, `.map` refs. | `xnLinkFinder v8.0–v8.2`: `-os` / `--output-secrets` (AWS, JWT, Google `AIza`, GitHub tokens, Stripe, DB URIs), `-rp` proxy, auto-config fix. | **90s** (offline) |
| **6. Sourcemap Unpacker** | **`sourcemapper`** (+ inline `data:` Python fallback) | If any `.js.map` file is accessible, unpacks the **original unminified TypeScript/React source tree** to expose unreleased models & routes. | Lightweight Go CLI (`denandz/sourcemapper`) + inline base64 `sourceMappingURL` decoder. | **60s** (offline) |
| **7. Feature Flags & Roles** | **`Jscope v1.0.0`** | Reconstructs client-side route guards, `feature_flag:*` toggles, `role:admin` gates, and DOM dataflows. | Runs offline in Python with **`sys.setrecursionlimit(10000)`** + per-file size/timeout safety so minified bundles don't crash. | **90s** (offline) |
| **8. Secret & Key Detection** | **`trufflehog v3.99+`** + **`praetorian-inc/titus`** | High-speed local scan across chunks + unpacked sourcemaps for unreleased internal API keys, GCP/Firebase configs, and internal staging tokens. | `titus`: replaces archived `noseyparker` with **487 combined rules** (NoseyParker + Kingfisher), archive/binary inspection, optional `--validate`. | **90s** (offline) |
| **9. Live Verification & Targeted AI Fuzz** | **`httpx v1.12.0`** + **`uro`** + **`feroxbuster v2.14.0`** / **`ffuf v2.3.0`** + **`x8 v4.3.0`** | Probing & status bucketing (`200`, `301/302/401/403/405`, `other`), URL/param deduplication (`uro`), plus **90s targeted fuzzing** on live non-CF API prefixes using mined JS words + AI seeds. | `httpx v1.12`: Markdown/DB/JSONL output. `feroxbuster v2.14`: `--scope` + per-dir `--time-limit`. `ffuf v2.3`: `-preflight` / `-postflight` token capture. | **150s total** (`httpx` 75s + `ferox`/`ffuf`/`x8` 75s) |
| **10. Exposure Check** | **`nuclei v3.7+`** | Scans verified live hosts for exposed `.env`, `.git`, Swagger/OpenAPI, debug panels, misconfigs. | Strict `-tags exposure,misconfig,tech,panel` + curated target cap + `chrome-headless-shell`/JS hardening. | **90s** |

### B. Tools Removed (Clean Cleanup)
- `waybackurls` -> replaced by `waymore v8.9`
- `anastasis` (+ Puppeteer Chrome npm build) -> replaced by `xnLinkFinder v8.2` + `jsluice` + `Jscope`
- `noseyparker` -> retired upstream; replaced by `praetorian-inc/titus`
- `kiterunner` (`kr`) -> dead since 2021; replaced by `feroxbuster v2.14.0` / `ffuf v2.3.0`
- `cariddi` -> WAF-blocked duplicate crawl; replaced by `Scrapling v0.5.1` + `katana v1.8.0`
- `getJS` + `subjs` -> redundant with Wave 1 (`Scrapling` + `katana` + regex/DOM `<script>` harvester); keep optional only if desired, not required

---

## 3. Fast Parallel Execution Design (`<= 10–12 min` MAX per URL)

Instead of running tools one after another for 2+ hours, `scripts/hunt.py` executes in **4 timed parallel waves**:

```text
[Target URL from urls.txt] ──► Normalize base + derive apex root domain (e.g. perplexity.ai)

WAVE 1 — Parallel Discovery (Wall time: max 3.5 min)
  ├── Thread A (60s cap) : subfinder (apex domain) -> dnsx live check -> well-known AI endpoint probes
  │                        (/llms.txt, /llms-full.txt, /robots.txt, /sitemap*.xml,
  │                         /openapi.json, /swagger.json, /.well-known/*, /$discovery/rest?version=v1alpha)
  ├── Thread B (120s cap): Scrapling StealthyFetcher + AsyncFetcher
  │                        - Bypasses Cloudflare / bot gates
  │                        - Records live XHR / fetch / GraphQL / WebSocket URLs
  │                        - Extracts all <script src>, importmaps, and _next/static / Vite manifests
  ├── Thread C (180s cap): Katana v1.8.0 (chrome-headless-shell, -d 3, -jsl, -xhr, similarity dedup)
  └── Thread D (150s cap): Waymore v8.9 (-mode U + archived JS URLs) + fixed urlfinder (-max-time 2 -v)

WAVE 2 — Chunk Download & Dedup (Wall time: max 2.0 min)
  ├── Collect all .js / .mjs / .json / .map URLs from Wave 1 (up to 3 manifest/import hops, time-guarded)
  ├── Fast HTTP pool (30 threads); auto-fallback to Scrapling session for Cloudflare-protected hosts
  └── Save 100% raw URLs -> SHA-256 hash chunks so identical bundles are parsed ONLY once

WAVE 3 — Offline Parallel Analysis on Local Chunks (Wall time: max 2.5 min — zero network/WAF blocks!)
  ├── Thread A: jsluice (urls + secrets, batched)
  ├── Thread B: xnLinkFinder v8.2 (endpoints + params + -os secrets)
  ├── Thread C: sourcemapper / inline .map unpacker (on any discovered .map URLs/refs)
  ├── Thread D: Jscope v1.0.0 (feature flags + role guards + dataflows, recursion limit 10000)
  └── Thread E: trufflehog + titus (487 secret rules across chunks + unpacked sourcemaps)

WAVE 4 — Live Probe, Targeted Fuzz & AI Feed (Wall time: max 3.0 min)
  ├── uro deduplicates parameter noise -> httpx probes unique routes (captures 200, 301/302, 401, 403, 405, 404/500)
  ├── Adaptive wordlist.py (JS-mined segments + AI paths) -> feroxbuster/ffuf (75s cap on non-CF live hosts)
  ├── x8 parameter fuzz ONLY on top 10 live /api/ or JSON routes (45s cap, skipped if host is 100% CF-blocked)
  ├── nuclei curated exposure/misconfig/panel check on verified live hosts (90s cap)
  └── Write:
       ├── results/<host>/...          (100% raw preservation — nothing deleted!)
       ├── results/<host>/ai_feed.json (compact ranked intelligence feed for AI analysis)
       └── results/<host>/REPORT.md    (clean human/AI summary with timings & status)

Total Worst-Case Wall Time Per URL: ~11.0 minutes (Hard failsafe ceiling: 12.0 minutes)
```

### Why Nothing Is Missed Under the 10–12 Min Limit
1. **No repeated identical pages:** Katana similarity deduplication stops wasting 90 minutes crawling `/ar-SA/hub/blog/{id}` across 50 locales while keeping every distinct route template.
2. **Parallel waves instead of serial waits:** Subdomains, Scrapling, Katana, and Waymore all run at the exact same time in Wave 1; all 5 JS/secret engines run simultaneously on local disk in Wave 3.
3. **SHA-256 chunk deduplication:** Shared vendor/framework JS chunks seen across multiple routes are downloaded and analyzed once instead of dozens of times.
4. **Raw kept separate from AI feed:** Every discovered URL, 403, 404, method response, third-party URL, and chunk is preserved; `ai_feed.json` filters noise *only at presentation time* so your AI prompt gets high-signal leads immediately.

---

## 4. Concurrent Multiple-URL & Multiple-Workflow Execution (`hunt.yml`)

To let you store as many targets as you want in `urls.txt` **AND** trigger multiple manual workflow runs concurrently without waiting or colliding:

### 1. Concurrent Multiple Targets from `urls.txt`
- `prepare` reads all non-comment lines from `inputs.urls_file` (default `urls.txt`, or optionally a comma/newline `urls_inline` input in `workflow_dispatch` for quick ad-hoc runs without editing git).
- `hunt` uses GitHub Actions `strategy.matrix` with:
  - `fail-fast: false` (one slow/blocked site never cancels the others).
  - `max-parallel: ${{ fromJSON(inputs.max_parallel) }}` with default raised from `"3"` to **`"10"`** (GitHub Free accounts support up to 20 concurrent Linux runners across a workflow; Pro/Team supports more). Running 10 URLs concurrently finishes all 10 in **~12 minutes total**.
  - `timeout-minutes: 20` per matrix job (down from `150`, giving 12 min hunt + ~2 min setup/cache + push buffer).

### 2. Concurrent Multiple Workflow Runs (No Queuing)
Currently `.github/workflows/hunt.yml` has:
```yaml
concurrency:
  group: web-hunt
  cancel-in-progress: false
```
Because every trigger shares the single group `web-hunt`, triggering Action #2 while Action #1 is running forces Action #2 to wait in queue.  
Change this to a **per-run concurrency group**:
```yaml
concurrency:
  group: web-hunt-${{ github.run_id }}
  cancel-in-progress: false
```
Now you can trigger multiple workflow dispatches back-to-back (e.g., `urls.txt` + a second dispatch for another list) and **both execute concurrently** without blocking or cancelling each other.

### 3. Race-Safe Concurrent `git push` Across 10+ Matrix Jobs
When 10 matrix jobs finish around minute 11, they all push to `main`:
- Each matrix job writes **only inside `results/<host>/`** (never touching global `INDEX.md` or `SUMMARY.md`).
- Push retry loop uses **random sleep jitter (`0–6s`) + up to 8 `git pull --rebase --autostash origin main` retries** so parallel commits land cleanly without losing a single target's results.
- The final `index` job (`needs: hunt`, `if: always()`) pulls latest `main` and rebuilds `results/INDEX.md` and `results/SUMMARY.md` once after all concurrent jobs finish.

---

## 5. "Install Once, Reuse Fast" Cache Design (`install_tools.sh` + `actions/cache@v4`)

Previously, `hunt.yml` cached `~/.cache/go-build` and `~/go/pkg/mod` alongside `~/go/bin`, inflating the cache archive and slowing restore on every parallel runner, plus downloading full Puppeteer Chrome for `anastasis` AND Chrome for Katana.

### Optimized Split-Cache Strategy
1. **Run `tools` job only if primary cache missed (or lightweight verify):**
   - `tools` job caches **runtime-ready artifacts only** (no multi-GB `pkg/mod` / `go-build` intermediate object files inside the matrix runtime cache!):
     - `~/go/bin` (`subfinder`, `dnsx`, `uncover`, `katana`, `httpx`, `ffuf`, `urlfinder`, `jsluice`, `sourcemapper`, `nuclei`)
     - `~/.local/bin` & `~/.local/lib/python3.12` (`scrapling`, `waymore`, `xnLinkFinder`, `jscope`, `uro`)
     - `~/tools/bin` (`feroxbuster`, `x8`, `trufflehog`, `titus`)
     - `~/.cache/ms-playwright` / `~/.cache/patchright` + `~/.cache/camoufox` (Scrapling StealthyFetcher browser engines, installed once via `scrapling install`)
     - `~/.cache/chrome-headless-shell` (lightweight Katana v1.8.0 browser binary)
     - `~/nuclei-templates`
     - `~/.cache/hunt-tools-ready-v3` (versioned readiness marker)
   - **Cache Key:**
     ```yaml
     key: hunt-tools-v3-${{ runner.os }}-${{ hashFiles('scripts/install_tools.sh') }}
     restore-keys: |
       hunt-tools-v3-${{ runner.os }}-
     ```
2. **Optional Separate Build Cache ONLY Inside `tools` Job:**
   - Only the `tools` builder job caches `~/go/pkg/mod` and `~/.cache/go-build` under a builder-only key (`go-build-cache-${{ runner.os }}`). Matrix `hunt` jobs never waste time downloading/extracting Go compile caches — they restore **only ready-to-run binaries** in ~15–20 seconds!
3. **Zero-Reinstall Fast Path in `tools` and `hunt`:**
   - `install_tools.sh` checks `if [ -f "$MARKER" ] && all_present; then exit 0; fi` (runs in `<1s`).
   - If you update one tool later, `restore-keys` restores all other cached tools and `install_tools.sh` (`have <tool> || install`) installs **only the newly added/updated binary**.

---

## 6. File-by-File Exact Refactor Specification

### File 1: `.github/workflows/hunt.yml`
- **Inputs (`workflow_dispatch`):**
  - `urls_file` (default `"urls.txt"`)
  - `urls_inline` (optional space/comma-separated URLs so you can test single/multiple ad-hoc targets right from the GitHub Actions UI without editing `urls.txt`)
  - `max_parallel` (default `"10"`)
  - `time_budget_minutes` (default `"11"`, hard safety ceiling passed to `hunt.py`)
- **Concurrency:** `group: web-hunt-${{ github.run_id }}`, `cancel-in-progress: false`.
- **Jobs:**
  1. `prepare`: builds JSON matrix from `urls_inline` (if non-empty) or `urls_file`, deduplicates URLs preserving order.
  2. `tools`: checks `actions/cache@v4` with `id: cache`; skips heavy `setup-go` compilation unless `cache-hit != 'true'` or `all_present` fails, warming `hunt-tools-v3` once.
  3. `hunt` (`needs: [prepare, tools]`, `timeout-minutes: 20`, `max-parallel: ${{ fromJSON(inputs.max_parallel) }}`):
     - Does **not** even need Node.js setup once `anastasis` is removed (unless using Node sourcemap fallback, or keep `python` + `node-version: "22"` only if needed; `sourcemapper` in Go removes Node dependency completely!).
     - Restores `hunt-tools-v3` cache in ~15s.
     - Runs `bash scripts/install_tools.sh` (`<1s` no-op when cached).
     - Runs `python3 scripts/hunt.py --url "${{ matrix.target }}" --out results --settings config/settings.json --budget-min "${{ inputs.time_budget_minutes }}"`.
     - Pushes `results/<host>/` (excluding `chunks/` and `sourcemaps/` raw directories if oversized, keeping all `.jsonl`/`.txt`/`.json`/`REPORT.md`) using random jitter + 8 rebase retries.
     - Uploads `hunt-<host>` artifact backup (30 days retention).
  4. `index` (`needs: hunt`, `if: always()`): checks out latest `main`, runs `python3 scripts/make_index.py results`, commits & pushes `INDEX.md` and `SUMMARY.md`.

---

### File 2: `scripts/install_tools.sh`
- **Keep & verify:**
  - Go binaries: `katana@latest` (`v1.8+`), `httpx@latest` (`v1.12+`), `ffuf/v2@latest` (`v2.3+`), `subfinder/v2@latest` (`v2.17+`), `dnsx@latest`, `uncover@latest`, `jsluice@latest`, `urlfinder@dev`, `nuclei/v3@latest`, **`github.com/denandz/sourcemapper@latest`**.
  - Prebuilt Linux amd64 binaries (fast `curl`, no compile wait): `feroxbuster` (`v2.14.0`), `x8` (`v4.3.0`), `trufflehog` (`v3.99+`), **`praetorian-inc/titus`** (prebuilt release binary).
  - Python (`pip install --user`): `scrapling[all]` (`v0.5.1`) + `scrapling install` (downloads Turnstile/Stealth browser once into cached browser dir), `waymore` (`v8.9`), `xnLinkFinder` (`v8.2`), `jscope` (`v1.0.0`), `uro`.
  - Katana browser: install **`chrome-headless-shell`** (instead of heavy full Puppeteer Chrome) + `nuclei -update-templates -silent`.
- **Remove from `REQUIRED` and installer:** `waybackurls`, `anastasis`, `noseyparker`, `kr` (`kiterunner`), `cariddi`, `getJS`, `subjs`, `puppeteer` Chrome npm install.

---

### File 3: `config/settings.json`
```json
{
  "target_budget_seconds": 660,
  "wave1_budget_seconds": 210,
  "wave2_budget_seconds": 120,
  "wave3_budget_seconds": 150,
  "wave4_budget_seconds": 180,

  "enable_subdomains": true,
  "enable_wellknown_ai_probes": true,
  "enable_scrapling": true,
  "enable_katana": true,
  "enable_waymore": true,
  "enable_urlfinder": true,
  "enable_sourcemapper": true,
  "enable_jsluice": true,
  "enable_xnlinkfinder": true,
  "enable_jscope": true,
  "enable_trufflehog": true,
  "enable_titus": true,
  "enable_httpx": true,
  "enable_uro": true,
  "enable_targeted_fuzz": true,
  "enable_x8": true,
  "enable_nuclei": true,
  "enable_vhost": true,
  "enable_result_push": true,

  "subfinder_timeout": 60,
  "scrapling_timeout": 120,
  "scrapling_max_pages": 25,
  "katana_timeout": 180,
  "katana_depth": 3,
  "katana_max_response": 2097152,
  "katana_use_jsl": true,
  "katana_use_headless_shell": true,
  "waymore_timeout": 140,
  "urlfinder_max_time_min": 2,

  "max_js_files": 2500,
  "js_crawl_rounds": 3,
  "js_download_threads": 32,
  "js_download_timeout": 8,
  "jsluice_batch": 100,
  "jscope_max_file_bytes": 3145728,
  "jscope_recursion_limit": 10000,

  "httpx_rate": 120,
  "httpx_threads": 60,
  "httpx_timeout": 75,
  "fuzz_tool": "feroxbuster",
  "fuzz_timeout": 75,
  "fuzz_prefixes_max": 8,
  "x8_max_api_targets": 8,
  "x8_timeout": 45,
  "nuclei_max_targets": 150,
  "nuclei_timeout": 90,
  "wordlist": "wordlists/common.txt",
  "wordlist_max": 6000
}
```

---

### File 4: `scripts/hunt.py` (Core Architecture Changes)
1. **Apex Root Domain Helper (`extract_apex_domain(host)`):**
   - Turns `www.perplexity.ai` -> `perplexity.ai`, `aistudio.google.com` -> keep both `aistudio.google.com` & inspect apex cautiously (note: for giant shared domains like `google.com`, run `subfinder` on the exact target domain + `*.gemini.google.com`/`*.aistudio.google.com`; for independent brands like `www.perplexity.ai`, `www.claude.ai`, strip `www.` so `subfinder` and `urlfinder` don't return `0`).
2. **Global Wall-Clock Budget Manager (`BudgetTimer`):**
   - Tracks `deadline = RUN_START + target_budget_seconds`. Every wave/tool receives `min(tool_timeout, remaining_budget)` so no single tool can push the run over 12 minutes.
3. **Wave 1 Parallel Executor (`ThreadPoolExecutor`):**
   - Runs `step_subdomains_and_wellknown`, `step_scrapling`, `step_katana`, and `step_waymore_urlfinder` **concurrently**.
   - **Well-known AI paths directly checked** (with Scrapling fallback if WAF 403s):
     - `/llms.txt`, `/llms-full.txt`, `/robots.txt`, `/sitemap.xml`, `/sitemap_index.xml`
     - `/openapi.json`, `/swagger.json`, `/v1/models`, `/api/models`, `/api/config`, `/config.json`, `/manifest.json`
     - `/.well-known/ai-plugin.json`, `/.well-known/security.txt`, `/$discovery/rest?version=v1alpha`, `/$discovery/rest?version=v1beta`
   - **Scrapling helper (`step_scrapling`):**
     - Uses `StealthyFetcher` on entry URL + top discovered key pages (`solve_cloudflare=True`, headless browser network listener capturing `XHR`/`fetch`/WebSocket requests and `.js`/`.json`/`.map` URLs), falling back cleanly to `AsyncFetcher` when no WAF challenge is present.
     - Saves `scrapling_urls.txt`, `scrapling_xhr.jsonl`, `scrapling_js.txt`, plus WAF cookie header JSON (for Wave 2 chunk downloads if needed!).
   - **Katana v1.8 (`step_katana`):**
     - Uses `-d 3`, `-jsl` (built-in pure-Go `jsluice`), `-kf all`, `-c 20 -p 10`, similarity dedup flags, and `chrome-headless-shell` for Pass 2 `-headless -xhr -no-sandbox` capped strictly inside `katana_timeout` (`180s`).
   - **Waymore + fixed urlfinder (`step_archive`):**
     - `waymore -i <domain> -mode U -oU waymore_urls.txt -nlf` (plus `-mode R` filtered strictly to `.js` / `.json` / `.map` up to a 60s download cap so you get historical JS bundles too!).
     - `urlfinder -d <domain> -all -max-time 2 -v -o urlfinder_raw.txt` (NO `-max-time 0`).
4. **Wave 2 SHA-256 Chunk Downloader (`step_download_js`):**
   - Deduplicates `.js`/`.mjs`/`.json`/`.map` URLs, downloads up to 3 hops concurrently (`32` threads), uses Scrapling cookies/session automatically on any `403`/`503` Cloudflare challenge, computes `sha256` per file so `chunks_unique/` holds zero duplicate payloads while `chunk_manifest.jsonl` maps every URL -> SHA-256 hash.
5. **Wave 3 Offline Parallel Analysis (`ThreadPoolExecutor` over `chunks_unique/`):**
   - **`jsluice`** (`urls` + `secrets` batched by 100)
   - **`xnLinkFinder`** (`-i chunks_unique/ -sf <host> -o cli -op xn_params.txt -os xn_secrets.jsonl`)
   - **`sourcemapper`** on any `.map` URLs or `//# sourceMappingURL=` references found inside chunks -> unpacks into `sourcemaps/` (which Wave 3 secret scanners also scan!)
   - **`Jscope`** invoked via small Python wrapper raising `sys.setrecursionlimit(10000)` and skipping >3MB minified blobs cleanly so individual crashes never silence other files (`jscope_findings.json` + `jscope.txt`)
   - **`trufflehog filesystem`** + **`titus scan`** running concurrently over `chunks_unique/` + `sourcemaps/`
6. **Wave 4 Verification, Targeted Fuzz & `ai_feed.json`:**
   - Deduplicate all URLs through `uro` -> verify with `httpx` (`-rl 120 -threads 60`, `75s` cap; skip obvious CF-tarpit flood retries or cap retries strictly).
   - Build `wordlist.txt` + `params.txt` using `wordlist.py`.
   - Run **targeted 75s `feroxbuster` (or `ffuf`)** on up to 8 live non-CF `/api`, `/v1`, `/internal`, `/data` prefixes.
   - Run **targeted 45s `x8`** against up to 8 live `/api/` JSON routes (not homepage `/`).
   - Run **curated 90s `nuclei`** (`-tags exposure,misconfig,tech,panel`) on live verified hosts only (`nuclei_max_targets: 150`).
   - Emit **`ai_feed.json`** + **`REPORT.md`**:
     - `ai_feed.json` groups & ranks **only high-signal intelligence** for direct LLM consumption:
       1. Verified/active secrets (`titus` + `trufflehog` + `xnLinkFinder -os`)
       2. Feature flags, admin guards & role checks (`Jscope`)
       3. AI & API endpoint candidates (`/v1alpha`, `/v1beta`, `/api/`, `graphql`, `llms.txt`, `openapi`, `$discovery`, unreleased model/product slugs)
       4. Unpacked sourcemap paths & hidden config/JSON files (`data_files.jsonl`)
       5. Live subdomains & real non-CF virtual hosts
       6. Collapsed route patterns (deduplicated across locales/IDs so 189 blog locales appear as `1` pattern, not `28,157` lines)
     - Every raw URL and blocked status (`raw_collected.txt`, `exists_blocked.jsonl`, `other_status.jsonl`, `third_party_routes.jsonl`, `method_responses.jsonl`) remains saved on disk untouched.

---

### File 5: `scripts/wordlist.py` & `wordlists/common.txt`
- Keep existing frequency-based path & parameter mining from downloaded JS/JSON chunks.
- Expand `wordlists/common.txt` with high-value AI leak & API discovery terms:
  - `llms.txt`, `llms-full.txt`, `openapi.json`, `swagger.json`, `api-docs`, `graphql`, `graphiql`
  - `v1alpha`, `v1beta`, `v1`, `v2`, `internal`, `admin`, `debug`, `feature-flags`, `flags`, `experiments`, `models`, `capabilities`, `config`, `env`, `healthz`, `metrics`, `build-manifest.json`
- Filter out HTML escape junk during mining (fix the `%5Cu003e%5Cu003c/div...` pollution seen in `devin.ai/REPORT.md`) by rejecting tokens containing `<`, `>`, `\u003c`, `\u003e`, `%5cu003` before scoring into `wordlist.txt`.

---

### File 6: `scripts/make_index.py`
- Keep rebuilding `results/INDEX.md` and `results/SUMMARY.md` from all `results/*/context.json` files.
- Add columns for **Duration (`min:sec`)**, **Secrets/Flags**, and **AI Feed Link (`ai_feed.json`)** so you can immediately open the richest results first after a concurrent multi-URL batch completes.

---

## 7. Expected Performance & Output Comparison

| Metric | Old Pipeline (`Android-url-ai`) | Refactored Pipeline (This Plan) |
|---|---|---|
| **Time per URL** | `100m – 148m` (up to 2.5 hrs) | **`8m – 12m` HARD CAP** |
| **10 URLs in `urls.txt`** | Slow queue (`max_parallel: 3`, 5+ hrs total) | **All 10 concurrent -> ~12 min total** |
| **Multiple Actions** | Queued by shared `web-hunt` group | **Concurrent per-run group (`web-hunt-<run_id>`)** |
| **Repeat Setup Time** | Restores heavy Go compile caches | **~15–20s binary+browser cache restore, 0 installs** |
| **Cloudflare Sites (`claude.ai`, `perplexity.ai`)** | Blocked (`0` JS endpoints / `2` 200s) | **Bypassed via `Scrapling v0.5.1` Turnstile + XHR capture** |
| **Passive Archives** | `urlfinder` `0` URLs + `waybackurls` `0` URLs | **Working `waymore v8.9` + fixed `urlfinder` (`-max-time 2`)** |
| **Secret & Flag Mining** | Retired `noseyparker` + crashing `Jscope`/`anastasis` | **`titus` (487 rules) + `trufflehog` + fixed `Jscope` + `xnLinkFinder v8.2` + `sourcemapper`** |
| **AI Input Readiness** | Flooded with 28k locale/HTML strings | **100% raw preserved + clean compact `ai_feed.json`** |

---

## 8. Implementation Order (When Ready to Build)

1. Update `.github/workflows/hunt.yml` (concurrent `run_id` group, `max_parallel: 10`, split runtime cache `hunt-tools-v3`, race-safe push loop, `20m` job timeout).
2. Update `scripts/install_tools.sh` (add `Scrapling`, `waymore`, `xnLinkFinder`, `titus`, `feroxbuster`, `sourcemapper`, `chrome-headless-shell`; drop `waybackurls`, `anastasis`, `noseyparker`, `kiterunner`, `cariddi`).
3. Update `config/settings.json` & `wordlists/common.txt` (wave budgets + AI discovery seeds).
4. Refactor `scripts/hunt.py` & `scripts/wordlist.py` (4 parallel waves, apex domain fix, `urlfinder` fix, SHA-256 chunk dedup, `Jscope` recursion fix, HTML-tag junk filter, `ai_feed.json` writer).
5. Update `scripts/make_index.py` (show duration & AI lead counts).
6. Run one manual `workflow_dispatch` test on 2–3 contrasting targets (`devin.ai` + Cloudflare-protected `claude.ai` + `aistudio.google.com`) to verify `< 12 min` runtime, cache hit on second run, and rich `ai_feed.json` output.
