# Web Hunt Report: `claude.ai`

- **Target:** https://claude.ai/
- **Scope Apex:** `claude.ai`
- **Duration:** `5:37` (337.0s)
- **Generated:** 2026-11-27T15:07:34Z

## Wave Timings

| Wave | Elapsed (s) |
|---|---:|
| Wave 1 (Discovery) | 199.2 |
| Wave 2 (Chunks) | 0.8 |
| Wave 3 (Offline AST/Secrets) | 18.1 |
| Wave 4 (Verify/Fuzz/Feed) | 118.9 |

## Headline Counts

| Metric | Count | Artifact |
|---|---:|---|
| Total collected routes | 686 | `all_routes.jsonl` |
| Accessible 200 | 259 | `accessible_200.jsonl` |
| Exists / blocked (30x/401/403/405) | 276 | `exists_blocked.jsonl` |
| Other status (404/500/etc) | 70 | `other_status.jsonl` |
| Live subdomains | 15 | `subdomains.jsonl` |
| Real virtual hosts | 1 | `vhost_real.jsonl` |
| Blocked vhost checks | 14 | `vhost_blocked.jsonl` |
| JS endpoints | 77 | `js_endpoints.jsonl` |
| Feature flags / role guards | 15 | `jscope_findings.json` |
| AI & API candidates | 39 | `ai_feed.json` |
| Secret candidates | 0 | `secrets.jsonl` |
| Unpacked sourcemap files | 0 | `sourcemap_files.txt` |
| Nuclei findings | 75 | `nuclei.jsonl` |
| Third-party URLs | 344 | `third_party_routes.jsonl` |
| Method probe rows | 24 | `method_responses.jsonl` |

## High-Signal AI & API Candidates

| Status | Score | URL |
|---:|---:|---|
| 200 | 90 | `https://claude.ai/assets/v1/llms-full.txt` |
| 200 | 90 | `https://claude.ai/assets/v1/llms.txt` |
| 200 | 90 | `https://claude.ai/llms-full.txt` |
| 200 | 90 | `https://claude.ai/llms.txt` |
| 403 | 65 | `https://claude.ai/$discovery/rest?version=v1alpha` |
| 403 | 65 | `https://claude.ai/openapi.json` |
| 403 | 65 | `https://claude.ai/openapi.yaml` |
| 403 | 65 | `https://claude.ai/swagger.json` |
| 403 | 50 | `https://claude.ai/api/config` |
| 403 | 50 | `https://claude.ai/api/event_logging/v2/batch?for=experiment-exposure` |
| 403 | 50 | `https://claude.ai/api/models` |
| 403 | 50 | `https://claude.ai/config.json` |
| 403 | 50 | `https://claude.ai/v1/models` |
| 0 | 40 | `https://claude.ai/$discovery/rest?version=v1beta` |
| 403 | 25 | `https://claude.ai/api/*` |
| 403 | 25 | `https://claude.ai/api/desktop` |
| 403 | 25 | `https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect` |
| 403 | 25 | `https://claude.ai/api/desktop/win32/arm64/setup/latest/redirect` |
| 403 | 25 | `https://claude.ai/api/desktop/win32/x64/setup/latest/redirect` |
| 403 | 25 | `https://claude.ai/api/organizations` |
| 403 | 25 | `https://claude.ai/api/v2/rum?_dd.api=fetch&batch_time=1795791719441&build_ts=1795787081&dd-api-key=pub71869dceb5b70dba6123af9ca357d1f9&dd-evp-encoding=deflate&dd-evp-origin=browser&dd-evp-origin-version=7.6.0&dd-request-id=f25e327a-cacf-45bb-9069-9c2f545713cc&ddsource=browser` |
| 403 | 25 | `https://claude.ai/assets/api/*` |
| 403 | 25 | `https://claude.ai/assets/api/desktop` |
| 403 | 25 | `https://claude.ai/build-manifest.json` |
| 403 | 25 | `https://claude.ai/cdn-cgi/api/*` |
| 403 | 25 | `https://claude.ai/cdn-cgi/api/desktop` |
| 403 | 25 | `https://claude.ai/manifest.json` |
| 0 | 0 | `https://claude.ai/api/desktop/` |
| 0 | 0 | `https://claude.ai/api/event_logging/v2/batch?for=product-analytics` |
| 0 | 0 | `https://claude.ai/api/organizations/` |
| 0 | 0 | `https://claude.ai/api/v2/rum?_dd.api=fetch&batch_time=1795791719588&build_ts=1795787081&dd-api-key=pub71869dceb5b70dba6123af9ca357d1f9&dd-evp-encoding=deflate&dd-evp-origin=browser&dd-evp-origin-version=7.6.0&dd-request-id=4dc5e0ad-f092-476c-bcd9-6a1ad85f214e&ddsource=browser` |
| 0 | 0 | `https://claude.ai/api/v2/rum?_dd.api=fetch&batch_time=1795791727790&build_ts=1795787081&dd-api-key=pub71869dceb5b70dba6123af9ca357d1f9&dd-evp-encoding=deflate&dd-evp-origin=browser&dd-evp-origin-version=7.6.0&dd-request-id=7190e8c5-aea3-4eda-a648-d86ddd167160&ddsource=browser` |
| 0 | 0 | `https://claude.ai/api/v2/rum?_dd.api=fetch&batch_time=1795791727911&build_ts=1795787081&dd-api-key=pub71869dceb5b70dba6123af9ca357d1f9&dd-evp-encoding=deflate&dd-evp-origin=browser&dd-evp-origin-version=7.6.0&dd-request-id=3e2a2acd-f481-4994-b679-273db176dd37&ddsource=browser` |
| 0 | 0 | `https://claude.ai/api/v2/rum?_dd.api=fetch&batch_time=1795791737489&build_ts=1795787081&dd-api-key=pub71869dceb5b70dba6123af9ca357d1f9&dd-evp-encoding=deflate&dd-evp-origin=browser&dd-evp-origin-version=7.6.0&dd-request-id=3d407df6-8bd1-40fa-8cdb-164a1b9b7fb0&ddsource=browser` |
| 0 | 0 | `https://claude.ai/api/v2/rum?_dd.api=fetch&batch_time=1795791737543&build_ts=1795787081&dd-api-key=pub71869dceb5b70dba6123af9ca357d1f9&dd-evp-encoding=deflate&dd-evp-origin=browser&dd-evp-origin-version=7.6.0&dd-request-id=af91f3a3-1833-4c2f-a6ba-024d58983b89&ddsource=browser` |
| 0 | 0 | `https://claude.ai/api/v2/rum?_dd.api=fetch&batch_time=1795791745967&build_ts=1795787081&dd-api-key=pub71869dceb5b70dba6123af9ca357d1f9&dd-evp-encoding=deflate&dd-evp-origin=browser&dd-evp-origin-version=7.6.0&dd-request-id=85c8ffd3-14ec-46e7-b725-8427d4a745b9&ddsource=browser` |
| 0 | 0 | `https://claude.ai/api/v2/rum?_dd.api=fetch&batch_time=1795791746078&build_ts=1795787081&dd-api-key=pub71869dceb5b70dba6123af9ca357d1f9&dd-evp-encoding=deflate&dd-evp-origin=browser&dd-evp-origin-version=7.6.0&dd-request-id=8a6a5e01-3f7f-4e98-b8f8-88727791bd6f&ddsource=browser` |
| 0 | 0 | `https://claude.ai/api/v2/rum?_dd.api=fetch&batch_time=1795791754821&build_ts=1795787081&dd-api-key=pub71869dceb5b70dba6123af9ca357d1f9&dd-evp-encoding=deflate&dd-evp-origin=browser&dd-evp-origin-version=7.6.0&dd-request-id=92f760ef-2268-4a1f-924c-278314499897&ddsource=browser` |
| 0 | 0 | `https://claude.ai/api/v2/rum?_dd.api=fetch&batch_time=1795791754888&build_ts=1795787081&dd-api-key=pub71869dceb5b70dba6123af9ca357d1f9&dd-evp-encoding=deflate&dd-evp-origin=browser&dd-evp-origin-version=7.6.0&dd-request-id=3bcb863c-5a92-4d2d-a264-3e37cd67c8b6&ddsource=browser` |

## Feature Flags & Role Guards

| Type | Identifier | Source |
|---|---|---|
| `flag_or_role` | `initial` | `2317cd7e5fc4136c_shared-903-CiPWzGcA.js` |
| `flag_or_role` | `menuitem` | `2317cd7e5fc4136c_shared-903-CiPWzGcA.js` |
| `flag_or_role` | `button` | `2317cd7e5fc4136c_shared-903-CiPWzGcA.js` |
| `flag_or_role` | `checkbox` | `2317cd7e5fc4136c_shared-903-CiPWzGcA.js` |
| `flag_or_role` | `radio` | `2317cd7e5fc4136c_shared-903-CiPWzGcA.js` |
| `flag_or_role` | `switch` | `2317cd7e5fc4136c_shared-903-CiPWzGcA.js` |
| `flag_or_role` | `tab` | `2317cd7e5fc4136c_shared-903-CiPWzGcA.js` |
| `flag_or_role` | `status` | `2317cd7e5fc4136c_shared-903-CiPWzGcA.js` |
| `model_candidate` | `claude-conversation-store` | `2317cd7e5fc4136c_shared-903-CiPWzGcA.js` |
| `model_candidate` | `claudeai.v1.` | `2317cd7e5fc4136c_shared-903-CiPWzGcA.js` |
| `model_candidate` | `claudeai.gatedHeld.v1` | `2317cd7e5fc4136c_shared-903-CiPWzGcA.js` |
| `model_candidate` | `claudeAppBindings` | `2317cd7e5fc4136c_shared-903-CiPWzGcA.js` |
| `model_candidate` | `claudeai.lastChatHost.v1` | `2317cd7e5fc4136c_shared-903-CiPWzGcA.js` |
| `model_candidate` | `claudeai.lastChatLook.v1` | `2317cd7e5fc4136c_shared-903-CiPWzGcA.js` |
| `model_candidate` | `Claude.ai` | `2317cd7e5fc4136c_shared-903-CiPWzGcA.js` |

## Secret Candidates (Redacted)

_None found._

## Collapsed Route Patterns

| Pattern | Count | Sample |
|---|---:|---|
| `claude.ai/api/v2/rum` | 10 | `https://claude.ai/api/v2/rum?_dd.api=fetch&batch_time=1795791719441&build_ts=1795787081&dd-api-key=pub71869dceb5b70dba6123af9ca357d1f9&dd-evp-encoding=deflate&dd-evp-origin=browser&dd-evp-origin-version=7.6.0&dd-request-id=f25e327a-cacf-45bb-9069-9c2f545713cc&ddsource=browser` |
| `claude.ai/cdn-cgi/challenge-platform/scripts/jsd/main.js` | 9 | `https://claude.ai/cdn-cgi/challenge-platform/scripts/jsd/main.js?ray=a61202dfed101776` |
| `claude.ai/` | 8 | `https://claude.ai/` |
| `claude.ai/cdn-cgi/challenge-platform/h/g/jsd/oneshot/b9d4778be3d9/0.6088777056110393:1795785923:J6YFUfQ-sLovHDFsyDrFTS4JX4GGqBU-htqdBrA6ADo/{hex}` | 5 | `https://claude.ai/cdn-cgi/challenge-platform/h/g/jsd/oneshot/b9d4778be3d9/0.6088777056110393:1795785923:J6YFUfQ-sLovHDFsyDrFTS4JX4GGqBU-htqdBrA6ADo/a61202dfed101776` |
| `claude.ai/cdn-cgi/challenge-platform/h/g/scripts/jsd/b9d4778be3d9/main.js` | 5 | `https://claude.ai/cdn-cgi/challenge-platform/h/g/scripts/jsd/b9d4778be3d9/main.js?ray=a61202dfed101776` |
| `claude.ai/edge-api/client-health/check` | 3 | `https://claude.ai/edge-api/client-health/check` |
| `claude.ai/$discovery/rest` | 2 | `https://claude.ai/$discovery/rest?version=v1alpha` |
| `claude.ai/.json` | 2 | `https://claude.ai/.json` |
| `claude.ai/api/event_logging/v2/batch` | 2 | `https://claude.ai/api/event_logging/v2/batch?for=experiment-exposure` |
| `claude.ai/bootstrap` | 2 | `https://claude.ai/bootstrap` |
| `claude.ai/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1` | 2 | `https://claude.ai/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=a61202dbca86609d` |
| `claude.ai/{slug}` | 2 | `https://claude.ai/claude-for-google-workspace` |
| `claude.ai/customers` | 2 | `https://claude.ai/customers` |
| `claude.ai/health/unavailable` | 2 | `https://claude.ai/health/unavailable?returnTo=` |
| `claude.ai/health/update-required` | 2 | `https://claude.ai/health/update-required?returnTo=` |
| `claude.ai/login` | 2 | `https://claude.ai/login` |
| `claude.ai/new` | 2 | `https://claude.ai/new` |
| `a.claude.ai/` | 1 | `https://a.claude.ai/` |
| `a.preview.claude.ai/` | 1 | `https://a.preview.claude.ai/` |
| `assets.claude.ai/` | 1 | `https://assets.claude.ai/` |
| `assets.claude.ai/videos/login-hero-kt3-932d39be.mp4` | 1 | `https://assets.claude.ai/videos/login-hero-kt3-932d39be.mp4` |
| `assets.claude.ai/videos/login-hero-kt3-still-005fec8b.webp` | 1 | `https://assets.claude.ai/videos/login-hero-kt3-still-005fec8b.webp` |
| `assets.claude.ai/videos/login-hero-kt3-still-1d2e63a3.webp` | 1 | `https://assets.claude.ai/videos/login-hero-kt3-still-1d2e63a3.webp` |
| `cadence.claude.ai/` | 1 | `https://cadence.claude.ai/` |
| `claude.ai/$` | 1 | `https://claude.ai/$` |
| `claude.ai/.well-known/security.txt` | 1 | `https://claude.ai/.well-known/security.txt` |
| `claude.ai/_next/static/chunks/0088q-6-qloh3.js` | 1 | `https://claude.ai/_next/static/chunks/0088q-6-qloh3.js` |
| `claude.ai/_next/static/chunks/0088q-6-qloh3.js\` | 1 | `https://claude.ai/_next/static/chunks/0088q-6-qloh3.js\` |
| `claude.ai/_next/static/chunks/00928170b0199602.css` | 1 | `https://claude.ai/_next/static/chunks/00928170b0199602.css` |
| `claude.ai/_next/static/chunks/00928170b0199602.css\` | 1 | `https://claude.ai/_next/static/chunks/00928170b0199602.css\` |
| `claude.ai/_next/static/chunks/00h04bxmkpw-h.css` | 1 | `https://claude.ai/_next/static/chunks/00h04bxmkpw-h.css` |
| `claude.ai/_next/static/chunks/00h04bxmkpw-h.css\` | 1 | `https://claude.ai/_next/static/chunks/00h04bxmkpw-h.css\` |
| `claude.ai/_next/static/chunks/034c0d400ac5dcdc.css` | 1 | `https://claude.ai/_next/static/chunks/034c0d400ac5dcdc.css` |
| `claude.ai/_next/static/chunks/034c0d400ac5dcdc.css\` | 1 | `https://claude.ai/_next/static/chunks/034c0d400ac5dcdc.css\` |
| `claude.ai/_next/static/chunks/066nce1cmpoak.js` | 1 | `https://claude.ai/_next/static/chunks/066nce1cmpoak.js` |
| `claude.ai/_next/static/chunks/066nce1cmpoak.js\` | 1 | `https://claude.ai/_next/static/chunks/066nce1cmpoak.js\` |
| `claude.ai/_next/static/chunks/06a7eb658fac9763.css` | 1 | `https://claude.ai/_next/static/chunks/06a7eb658fac9763.css` |
| `claude.ai/_next/static/chunks/06a7eb658fac9763.css\` | 1 | `https://claude.ai/_next/static/chunks/06a7eb658fac9763.css\` |
| `claude.ai/_next/static/chunks/06b57b36168654bd.js` | 1 | `https://claude.ai/_next/static/chunks/06b57b36168654bd.js` |
| `claude.ai/_next/static/chunks/06b57b36168654bd.js\` | 1 | `https://claude.ai/_next/static/chunks/06b57b36168654bd.js\` |

## Nuclei Findings

| Severity | Template | Host |
|---|---|---|
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |
| info | `dns-waf-detect` | `claude.ai` |

## Tool Status

| Tool | Exit | Duration (s) | Detail |
|---|---:|---:|---|
| `katana` | 0 | 20.0 | p1=5, p2=3 |
| `subfinder+dnsx` | 0 | 32.0 | 99 subs, 15 live |
| `wellknown_ai` | 0 | 0.9 | 19 paths checked |
| `scrapling` | 0 | 44.9 | 936 URLs/JS captured |
| `waymore` | 124 | 130.1 | 0 archive URLs |
| `urlfinder` | 124 | 69.1 | 0 URLs |
| `chunk_download` | 0 | 0.8 | 97 fetched -> 30 unique SHA-256 chunks |
| `sourcemapper` | 0 | 0.0 | 0 maps -> 0 unpacked sources |
| `xnLinkFinder` | 0 | 0.4 | 0 endpoints |
| `jsluice` | 0 | 2.4 | 25 chunks -> 913 URLs |
| `secrets_offline` | 0 | 7.6 | 0 candidates |
| `jscope` | 0 | 18.1 | 25 files -> 15 flags/models |
| `httpx` | 0 | 7.2 | 339/344 probed |
| `vhost` | 0 | 0.6 | 1 real / 15 tested |
| `targeted_fuzz` | 0 | 9.3 | 2 prefixes -> 266 hits |
| `x8` | 0 | 20.0 | 5 API routes scanned |
| `methods` | 0 | 1.0 | 24 probes |
| `nuclei` | 124 | 80.1 | 75 findings across 150 URLs |
