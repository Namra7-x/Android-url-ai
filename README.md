# web-hunt — High-Speed Concurrent Web & Early-Signal Hunt Pipeline

A fast, 4-wave parallel reconnaissance and client-side intelligence pipeline built for GitHub Actions (`<= 10-12 min` hard cap per target URL).

## Architecture Overview

1. **Wave 1 — Parallel Discovery (`<= 210s`)**
   - `subfinder` (apex-aware) + `dnsx` + direct well-known AI/discovery probes (`/llms.txt`, `/openapi.json`, `/.well-known/ai-plugin.json`, `/$discovery/rest?version=v1alpha`, etc.)
   - `Scrapling` (`StealthyFetcher` + `AsyncFetcher`) for Cloudflare Turnstile bypass, live `XHR`/`fetch`/WebSocket capture, `<script>` tags, import maps, and framework manifests
   - `katana` (`chrome-headless-shell`, `-jsl`, similarity dedup)
   - `waymore` (`-mode U` + filtered JS/JSON/map `-mode R`) + fixed `urlfinder` (`-max-time 2 -v`)
2. **Wave 2 — Chunk Download & SHA-256 Deduplication (`<= 120s`)**
   - Up to 3 manifest/import hops via a 32-thread HTTP pool with automatic Scrapling cookie/session fallback on `403`/`503`
   - Deduplicates identical JS/JSON/map payloads into `chunks_unique/` via SHA-256 and tracks provenance in `chunk_manifest.jsonl`
3. **Wave 3 — Offline Parallel Analysis (`<= 150s`)**
   - `jsluice` (`urls` + `secrets`, batched)
   - `xnLinkFinder` (endpoints + params + `-os` secrets)
   - `sourcemapper` + inline base64 `sourceMappingURL` unpacker -> `sourcemaps/`
   - `Jscope` (with `sys.setrecursionlimit(10000)` + per-file size/timeout safety) -> feature flags, role guards, dataflows
   - `trufflehog` + `titus` scanning both `chunks_unique/` and `sourcemaps/`
4. **Wave 4 — Live Verification, Targeted Fuzz & `ai_feed.json` (`<= 180s`)**
   - `uro` deduplication + `httpx` full status verification (`200`, `301/302/401/403/405`, `other`)
   - Adaptive `wordlist.py` (HTML-escape junk filtered + AI discovery seeds) -> targeted `feroxbuster`/`ffuf` + targeted `x8` on live `/api/` routes + curated `nuclei` (`exposure,misconfig,tech,panel`)
   - Preserves 100% of raw discoveries on disk while emitting a compact, ranked `ai_feed.json` and `REPORT.md`

## Concurrency & Caching

- **Per-run concurrency group** (`web-hunt-${{ github.run_id }}`): trigger multiple workflow dispatches back-to-back without queuing.
- **Matrix parallelism** (`max_parallel: 10` default): every URL in `urls.txt` (or ad-hoc `urls_inline` input) runs simultaneously with race-safe `git push` retries.
- **Runtime-only cache** (`hunt-tools-v3`): Go compile caches (`~/go/pkg/mod`, `~/.cache/go-build`) stay isolated in the `tools` builder job so `hunt` runners restore only ready binaries & browsers in ~15-20s.

## Outputs (`results/<host>/`)

- `ai_feed.json` — compact, prioritized intelligence feed for LLM analysis (secrets, feature flags, AI/API routes, unpacked sourcemaps, live subdomains/vhosts, collapsed route patterns)
- `REPORT.md` — structured human/AI summary with wave timings, tool status, and counts
- `context.json` — summary metadata consumed by `scripts/make_index.py`
- Raw `.jsonl` / `.txt` artifacts (`accessible_200.jsonl`, `exists_blocked.jsonl`, `other_status.jsonl`, `data_files.jsonl`, `subdomains.jsonl`, `vhost_real.jsonl`, `vhost_blocked.jsonl`, `js_endpoints.jsonl`, `params.jsonl`, `secrets.jsonl`, `nuclei.jsonl`, `third_party_routes.jsonl`, `method_responses.jsonl`, `chunk_manifest.jsonl`, `logs/`)
