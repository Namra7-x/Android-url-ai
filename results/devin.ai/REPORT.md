# Hunt Report — https://devin.ai

Generated: 2026-11-23T16:23:42Z &nbsp;|&nbsp; Duration: 100m 28s

> **Nothing is filtered during collection. This report is only a grouping.**

## Summary

| What | Count | Meaning |
|---|---:|---|
| Routes collected | 5934 | Every URL found, nothing removed |
| Distinct routes verified | 892 | One row per URL (method probes excluded) |
| HTTP responses | 2092 | Includes method probes — kept in `method_responses.jsonl` |
| **Accessible (200)** | **284** | Confirmed live — the wins |
| Exists but different status | 55 | 301/302/401/403/405 — real route, blocked |
| Other responses | 553 | 404/500/etc — kept, not discarded |
| Subdomains (resolved) | 24 | DNS-verified |
| Virtual hosts (real) | 4 | Cloudflare 403/530/0 excluded |
| Parameters | 4139 | URLs with query params |
| JS endpoints (AST) | 246 | anastasis evidence-backed |
| First-party URLs | 5779 | devin.ai and subdomains |
| Third-party URLs | 155 | kept in `third_party_routes.jsonl` |
| Method responses | 1400 | kept in `method_responses.jsonl` |
| Blocked vhost checks | 32 | kept in `vhost_blocked.jsonl` |
| Secret candidates | 3 | verify manually |

> Collection keeps third-party URLs by design (155). See `third_party_routes.jsonl`. Method-probe responses are in `method_responses.jsonl`.

## 0. TOP ROUTE PATTERNS (IDs collapsed)

| Pattern | Count |
|---|---:|
| `/_next/image` | 3919 |
| `/blog/{id}` | 128 |
| `/` | 52 |
| `/blog/page/{id}` | 19 |
| `/blog/category/product/page/{id}` | 14 |
| `/ja/blog/{id}` | 14 |
| `/download/confirmation` | 11 |
| `/legal/{id}` | 6 |
| `/api/www/avatar` | 6 |
| `/images/blog/{id}/cover.jpg` | 6 |
| `/.../pull/{id}` | 4 |
| `/blog/category/company/page/{id}` | 4 |
| `/blog/category/enterprise/page/{id}` | 4 |
| `/chat` | 4 |
| `/config` | 4 |
| `/images/blog/{id}/cover.png` | 4 |
| `/tr` | 4 |
| `/{id}/httpapi` | 3 |
| `/batch` | 3 |
| `/contact` | 3 |
| `/%5C%5Cn%5C%5Ct%5C%5Ct%5C%5Ct` | 3 |
| `/%5Cu003e%5Cu003c/a%5Cn%5Ct` | 3 |
| `/%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/a%5Cn%5Ct` | 3 |
| `/%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/a%5Cn%5Ct` | 3 |
| `/%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/once%5Cn%5Ct` | 3 |
| `/%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/static/immutable/chunks/a%5Cn%5Ct` | 3 |
| `/%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/static/immutable/chunks/once%5Cn%5Ct` | 3 |
| `/%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/static/immutable/chunks/static/immutable/chunks/a%5Cn%5Ct` | 3 |
| `/%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/static/immutable/chunks/static/immutable/chunks/once%5Cn%5Ct` | 3 |
| `/%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/static/immutable/chunks/static/immutable/chunks/the%5Cn%5Ct` | 3 |
| `/%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/static/immutable/chunks/static/immutable/chunks/visitor%5Cn%5Ct` | 3 |
| `/%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/static/immutable/chunks/the%5Cn%5Ct` | 3 |
| `/%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/static/immutable/chunks/visitor%5Cn%5Ct` | 3 |
| `/%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/the%5Cn%5Ct` | 3 |
| `/%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/visitor%5Cn%5Ct` | 3 |
| `/%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/once%5Cn%5Ct` | 3 |
| `/%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/static/immutable/chunks/a%5Cn%5Ct` | 3 |
| `/%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/static/immutable/chunks/once%5Cn%5Ct` | 3 |
| `/%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/static/immutable/chunks/static/immutable/chunks/a%5Cn%5Ct` | 3 |
| `/%5Cu003e%5Cu003c/div%5Cu003e%5Cu003c/static/immutable/chunks/static/immutable/chunks/once%5Cn%5Ct` | 3 |

## 1. SUCCESS — HTTP 200

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 200 | GET | `https://ad.doubleclick.net/activity` | image/gif | 42 |  |
| 200 | GET | `https://addons.mozilla.org/en-US/firefox/addon/vercel` | text/html | 3038 |  |
| 200 | GET | `https://app.beta.devin.ai` | text/html | 24779 |  |
| 200 | GET | `https://app.devin.ai` | text/html | 24779 |  |
| 200 | GET | `https://app.devin.ai/auth/signup` | text/html | 24779 |  |
| 200 | GET | `https://app.devin.ai/login` | text/html | 24779 |  |
| 200 | GET | `https://app.devin.ai/review` | text/html | 24779 |  |
| 200 | GET | `https://app.devin.ai/sessions/8c41f0e2` | text/html | 24779 |  |
| 200 | GET | `https://app.devin.ai/signup` | text/html | 24779 |  |
| 200 | GET | `https://app.devin.ai/signup\` | text/html | 24779 |  |
| 200 | GET | `https://app.devinenterprise.com` | text/html | 24779 |  |
| 200 | GET | `https://arxiv.org/abs/2602.07549` | text/html | 41722 |  |
| 200 | GET | `https://arxiv.org/abs/2602.07962` | text/html | 41346 |  |
| 200 | GET | `https://arxiv.org/abs/2606.14066` | text/html | 43230 |  |
| 200 | GET | `https://base-ui.com/production-error` | text/html | 44792 |  |
| 200 | GET | `https://bat.bing.com/bat.js` | application/javascript | 58485 |  |
| 200 | GET | `https://capi-automation.s3.us-east-2.amazonaws.com/public/client_js/capiParamBuilder/clientParamBuilder.bundle.js` | binary/octet-stream | 56482 |  |
| 200 | GET | `https://cognition.com` | text/html | 553228 |  |
| 200 | GET | `https://cognition.com/about` | text/html | 110408 |  |
| 200 | GET | `https://cognition.com/about\` | text/html | 110408 |  |
| 200 | GET | `https://cognition.com/careers` | text/html | 1686222 |  |
| 200 | GET | `https://cognition.com/careers\` | text/html | 1686222 |  |
| 200 | GET | `https://cognition.com/frontiercode` | text/html | 201887 |  |
| 200 | GET | `https://cognition.com/legal/acceptable-use-policy` | text/html | 141541 |  |
| 200 | GET | `https://cognition.com/legal/acceptable-use-policy\` | text/html | 141541 |  |
| 200 | GET | `https://cognition.com/legal/data-processing-statement` | text/html | 203766 |  |
| 200 | GET | `https://cognition.com/legal/data-processing-statement\` | text/html | 203766 |  |
| 200 | GET | `https://cognition.com/legal/platform-terms-of-service` | text/html | 203635 |  |
| 200 | GET | `https://cognition.com/legal/platform-terms-of-service\` | text/html | 203635 |  |
| 200 | GET | `https://cognition.com/legal/privacy-policy` | text/html | 172613 |  |
| 200 | GET | `https://cognition.com/legal/privacy-policy\` | text/html | 172613 |  |
| 200 | GET | `https://connect.facebook.net/en_US/fbevents.js` | application/x-javascript | 433362 |  |
| 200 | GET | `https://devin.ai` | text/html | 1749295 |  |
| 200 | GET | `https://devin.ai/DevinOGJapan.png\` | image/png | 515858 |  |
| 200 | GET | `https://devin.ai/_next/image?url=%2Fimages%2Fblog%2Fkimi-k2.7-glm-5.2-devin-desktop%2Fcover.png&w=2048&q=75&dpl=dpl_EZwTNMbSjDH2WjPMyXPmqDZB7GNU` | image/png | 1114945 |  |
| 200 | GET | `https://devin.ai/_next/image?url=https%3A%2F%2Fexafunction.github.io%2Fpublic%2Fhero%2Fseries_b.png&w=2048&q=75` | image/png | 48835 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/0-fep2q7sg7j6.js` | application/javascript | 260098 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/000xnk0cmrfov.js` | application/javascript | 52825 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/01jqsubr5jruv.js` | application/javascript | 31227 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/01mn8-z2tsn89.js` | application/javascript | 765 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/04y69_ozieh1_.js` | application/javascript | 52508 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/05dzak1c3ikdc.js` | application/javascript | 227 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/06l85nex44cdh.js` | application/javascript | 55645 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/0c0hxoamwjsbw.js` | application/javascript | 112594 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/0c8suttw-kd-f.js` | application/javascript | 29663 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/0e6gx0_e77dr-.js` | application/javascript | 66230 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/0h2iz7zm_52lq.js` | application/javascript | 235339 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/0m099b1rg-hr0.js` | application/javascript | 64900 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/0m6jeginm9a56.js` | application/javascript | 30423 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/0o9a0-pl15j7r.js` | application/javascript | 130356 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/0on1b1gpofy6i.js` | application/javascript | 15482 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/0pbah0ont1sch.js` | application/javascript | 229288 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/0pmrvd8_c_31g.js` | application/javascript | 47076 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/0z28ub9zygeee.js` | application/javascript | 1449 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/0zawknluu-4-v.js` | application/javascript | 4901 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/1-njn26b52310.js` | application/javascript | 13828 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/11p4dh62sa4f1.js` | application/javascript | 125820 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/13m-jxlh1q1-g.js` | application/javascript | 29653 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/15x971wfnkldk.js` | application/javascript | 31511 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/17ib25v5v0m1f.js` | application/javascript | 4611 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/19knir31_jgaw.js` | application/javascript | 38906 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/1_mmbrsewio32.js` | application/javascript | 8920 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/1a41eh5-9af0j.js` | application/javascript | 50414 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/1ai_9k5x_fc2s.js` | application/javascript | 36731 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/1czxb-w33de-y.js` | application/javascript | 886082 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/1hugnwkba432r.js` | application/javascript | 137489 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/1j0pci6a0utv-.js` | application/javascript | 18617 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/1jik6z8h85yl7.js` | application/javascript | 47522 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/1o5r4ib5_zpdf.js` | application/javascript | 42510 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/1ofl_5fayc92o.js` | application/javascript | 43207 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/1qn5jwnql3x8z.js` | application/javascript | 22540 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/1y65v6kwnsoxm.js` | application/javascript | 14487 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/2-nltif-rilsd.js` | application/javascript | 31431 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/2-vdw5iq_rr_y.js` | application/javascript | 48521 |  |
| 200 | GET | `https://devin.ai/_next/static/immutable/chunks/201s5ghhh5s6e.js` | application/javascript | 35233 |  |
| … | … | _209 more in JSONL_ | … | … | … |

## 2. EXISTS BUT DIFFERENT STATUS (301/302/401/403/405)

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 302 | GET | `https://adservice.google.com/pagead/regclk` | text/html | 0 |  |
| 405 | GET | `https://api.hsforms.com/submissions/v3/integration/submit/46599998/${k` | text/html | 229 |  |
| 302 | GET | `https://app.amplitude.com` |  | 0 |  |
| 307 | GET | `https://app.datadoghq.com/apm/trace` |  | 0 |  |
| 302 | GET | `https://app.eu.amplitude.com` |  | 0 |  |
| 302 | GET | `https://apps.stag2.amplitude.com` |  | 0 |  |
| 301 | GET | `https://assets.vercel.com/image/upload` |  | 0 |  |
| 307 | GET | `https://capture.navattic.com` | text/plain | 11 |  |
| 301 | GET | `https://chrome.google.com/webstore/detail/vercel/lahhiofdgnbcgmemekkmjnpifojdaelb` | text/html | 277 |  |
| 301 | GET | `https://cli.devin.ai` |  | 0 |  |
| 308 | GET | `https://cognition.com/contact` | text/plain | 15 |  |
| 308 | GET | `https://cognition.com/get-started` | text/plain | 15 |  |
| 302 | GET | `https://connect.facebook.net` | text/html | 0 |  |
| 307 | GET | `https://cursor.com/codebase` | text/plain | 15 |  |
| 307 | GET | `https://devin.ai/.well-known/vercel-auth-redirect` | text/plain | 15 |  |
| 401 | GET | `https://devin.ai/.well-known/vercel/flags` | application/json | 4 |  |
| 302 | GET | `https://devin.ai/.well-known/vercel/microfrontends/routing` | text/plain | 263 |  |
| 308 | GET | `https://devin.ai/api/www/avatar/?u=` | text/plain | 15 |  |
| 403 | GET | `https://devin.ai/bots/static/immutable/chunks/static/immutable/chunks/static/immutable/chunks/static/immutable/chunks/static/immutable/chunks/0pbah0ont1sch.js` | text/plain | 59 |  |
| 403 | GET | `https://devin.ai/build/lib/static/immutable/chunks/static/immutable/chunks/static/immutable/chunks/static/immutable/chunks/0pbah0ont1sch.js` | text/plain | 59 |  |
| 308 | GET | `https://devin.ai/cascade` | text/plain | 15 |  |
| 308 | GET | `https://devin.ai/changelog` | text/plain | 15 |  |
| 308 | GET | `https://devin.ai/chat?q=` | text/plain | 15 |  |
| 308 | GET | `https://devin.ai/get-started` | text/plain | 15 |  |
| 307 | GET | `https://devin.ai/review` | text/plain | 15 |  |
| 308 | GET | `https://devin.ai/university` | text/plain | 15 |  |
| 308 | GET | `https://docs.devin.ai` | text/plain | 0 |  |
| 308 | GET | `https://docs.windsurf.com/windsurf/models` | text/plain | 0 |  |
| 301 | GET | `https://facebook.com/privacy_sandbox/topics/registration` | text/html | 0 |  |
| 301 | GET | `https://google.com` | text/html | 220 |  |
| 403 | GET | `https://gw.conversionsapigateway.com` | text/html | 134 |  |
| 301 | GET | `https://hmc.conventionhall.jp/access` | text/html | 162 |  |
| 302 | GET | `https://m.youtube.com` | application/binary | 0 |  |
| 302 | GET | `https://player.vimeo.com` |  | 0 |  |
| 301 | GET | `https://reddit.com/r/CognitionLabs` |  | 0 |  |
| 301 | GET | `https://reddit.com/r/CognitionLabs/\` |  | 0 |  |
| 403 | GET | `https://sr-client-cfg.amplitude.com/config` | text/plain | 32 |  |
| 403 | GET | `https://sr-client-cfg.eu.amplitude.com/config` | text/plain | 32 |  |
| 403 | GET | `https://sr-client-cfg.stag2.amplitude.com/config` | text/plain | 32 |  |
| 302 | GET | `https://staging.itsdev.in` |  | 0 |  |
| 403 | GET | `https://static.devin.ai` | application/xml | 263 |  |
| 302 | GET | `https://status.devin.ai` | text/html | 0 |  |
| 302 | GET | `https://support.devin.ai` | text/html | 0 |  |
| 302 | GET | `https://ui.ads.microsoft.com` | text/html | 149 |  |
| 308 | GET | `https://unicorn.studio` | text/plain | 15 |  |
| 308 | GET | `https://unicorn.studio/embed/S9qZz1Wdl6bkGZci3QvX` | text/plain | 15 |  |
| 307 | GET | `https://v0.app/chat/api/open` |  | 0 |  |
| 307 | GET | `https://v0.app/chat?q=` | text/plain | 15 |  |
| 307 | GET | `https://vercel.com/account` | text/plain | 15 |  |
| 307 | GET | `https://vercel.com/teams` | text/plain | 15 |  |
| 302 | GET | `https://vercel.sentry.io/discover/homepage` | text/html | 0 |  |
| 302 | GET | `https://wa.me` | text/html | 0 |  |
| 403 | GET | `https://x.com/cognition\` | application/json | 95 |  |
| 301 | GET | `https://youtube.com` | application/binary | 0 |  |
| 301 | GET | `https://youtube.com/@cognition-labs` | application/binary | 0 |  |

## 3. OTHER RESPONSES — kept, never discarded

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 404 | GET | `https://ade.googlesyndication.com` | text/html | 1561 |  |
| 404 | GET | `https://api.devin.ai` | application/json | 22 |  |
| 404 | GET | `https://api.devinenterprise.com` | application/json | 22 |  |
| 400 | GET | `https://api.eu.amplitude.com/batch` | application/json | 43 |  |
| 404 | GET | `https://api.unifyintent.com/analytics/v1` | application/json | 84 |  |
| 404 | GET | `https://api.unifyintent.com/analytics/v1/_internal/logs` | application/json | 99 |  |
| 400 | GET | `https://api2.amplitude.com/2/httpapi` | application/json | 43 |  |
| 400 | GET | `https://api2.amplitude.com/batch` | application/json | 43 |  |
| 404 | GET | `https://auth.beta.devin.ai` |  | 0 |  |
| 404 | GET | `https://auth.devin.ai` |  | 0 |  |
| 404 | GET | `https://auth.devin.ai/login/callback` |  | 0 |  |
| 503 | GET | `https://clarity.microsoft.com/js` | text/html | 983 |  |
| 503 | GET | `https://clarity.microsoft.com/js/EXPR` | text/html | 983 |  |
| 404 | GET | `https://connect.facebook.net/log/fbevents_telemetry` | text/html | 72 |  |
| 429 | GET | `https://deepwiki.com` | text/html | 25091 |  |
| 404 | GET | `https://devin.ai/${d` | text/html | 62213 |  |
| 404 | GET | `https://devin.ai/${n.M` | text/html | 62219 |  |
| 404 | GET | `https://devin.ai/${u` | text/html | 62213 |  |
| 204 | GET | `https://devin.ai/.well-known/vercel/jwe` |  | 0 |  |
| 404 | GET | `https://devin.ai/@cognition-labs` | text/html | 62242 |  |
| 404 | GET | `https://devin.ai/API_URL=http:/localhost:8080` | text/html | 62293 |  |
| 404 | GET | `https://devin.ai/CognitionAI/devin-marketplace` | text/html | 62284 |  |
| 404 | GET | `https://devin.ai/LIVE-MODE-DEV` | text/html | 62232 |  |
| 404 | GET | `https://devin.ai/MEMORY.md` | text/markdown | 1083 |  |
| 404 | GET | `https://devin.ai/Next.js` | text/html | 62214 |  |
| 404 | GET | `https://devin.ai/Node.js` | text/html | 62214 |  |
| 404 | GET | `https://devin.ai/ROOT/node_modules/next/dist/compiled/process` | text/html | 62345 |  |
| 404 | GET | `https://devin.ai/[...not_found` | text/html | 62236 |  |
| 404 | GET | `https://devin.ai/\\n\\t\\t\\t` | text/html | 62277 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/a\n\t` | text/html | 62275 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e` | text/html | 62281 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/a\n\t` | text/html | 62339 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e` | text/html | 62345 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/a\n\t` | text/html | 62467 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/once\n\t` | text/html | 62476 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/section\u003e` | text/html | 62485 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/static/immutable/chunks/0pbah0ont1sch.js` | text/html | 62572 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/static/immutable/chunks/1y65v6kwnsoxm.js` | text/html | 62572 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/static/immutable/chunks/2-nltif-rilsd.js` | text/html | 62572 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/static/immutable/chunks/2d_yqrbc3re3g.js` | text/html | 62572 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/static/immutable/chunks/a\n\t` | text/html | 62551 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/static/immutable/chunks/once\n\t` | text/html | 62560 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/static/immutable/chunks/static/immutable/chunks/0pbah0ont1sch.js` | text/html | 62656 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/static/immutable/chunks/static/immutable/chunks/1y65v6kwnsoxm.js` | text/html | 62656 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/static/immutable/chunks/static/immutable/chunks/2-nltif-rilsd.js` | text/html | 62656 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/static/immutable/chunks/static/immutable/chunks/2d_yqrbc3re3g.js` | text/html | 62656 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/static/immutable/chunks/static/immutable/chunks/a\n\t` | text/html | 62635 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/static/immutable/chunks/static/immutable/chunks/once\n\t` | text/html | 62644 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/static/immutable/chunks/static/immutable/chunks/static/immutable/chunks/0pbah0ont1sch.js` | text/html | 62740 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/static/immutable/chunks/static/immutable/chunks/static/immutable/chunks/1y65v6kwnsoxm.js` | text/html | 62740 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/static/immutable/chunks/static/immutable/chunks/static/immutable/chunks/2-nltif-rilsd.js` | text/html | 62740 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/static/immutable/chunks/static/immutable/chunks/static/immutable/chunks/2d_yqrbc3re3g.js` | text/html | 62740 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/static/immutable/chunks/static/immutable/chunks/static/immutable/chunks/a\n\t` | text/html | 62719 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/static/immutable/chunks/static/immutable/chunks/static/immutable/chunks/once\n\t` | text/html | 62728 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/static/immutable/chunks/static/immutable/chunks/static/immutable/chunks/static/immutable/chunks/0pbah0ont1sch.js` | text/html | 62824 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/static/immutable/chunks/static/immutable/chunks/static/immutable/chunks/static/immutable/chunks/1y65v6kwnsoxm.js` | text/html | 62824 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/static/immutable/chunks/static/immutable/chunks/static/immutable/chunks/static/immutable/chunks/2-nltif-rilsd.js` | text/html | 62824 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/static/immutable/chunks/static/immutable/chunks/static/immutable/chunks/static/immutable/chunks/2d_yqrbc3re3g.js` | text/html | 62824 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/static/immutable/chunks/static/immutable/chunks/static/immutable/chunks/the\n\t` | text/html | 62725 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/static/immutable/chunks/static/immutable/chunks/static/immutable/chunks/visitor\n\t` | text/html | 62737 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/static/immutable/chunks/static/immutable/chunks/the\n\t` | text/html | 62641 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/static/immutable/chunks/static/immutable/chunks/visitor\n\t` | text/html | 62653 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/static/immutable/chunks/the\n\t` | text/html | 62557 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/static/immutable/chunks/visitor\n\t` | text/html | 62569 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/the\n\t` | text/html | 62473 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003c/visitor\n\t` | text/html | 62485 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/once\n\t` | text/html | 62348 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/static/immutable/chunks/0pbah0ont1sch.js` | text/html | 62444 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/static/immutable/chunks/1y65v6kwnsoxm.js` | text/html | 62444 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/static/immutable/chunks/2-nltif-rilsd.js` | text/html | 62444 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/static/immutable/chunks/2d_yqrbc3re3g.js` | text/html | 62444 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/static/immutable/chunks/a\n\t` | text/html | 62423 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/static/immutable/chunks/once\n\t` | text/html | 62432 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/static/immutable/chunks/static/immutable/chunks/0pbah0ont1sch.js` | text/html | 62528 |  |
| 404 | GET | `https://devin.ai/\u003e\u003c/div\u003e\u003c/static/immutable/chunks/static/immutable/chunks/1y65v6kwnsoxm.js` | text/html | 62528 |  |
| … | … | _478 more in JSONL_ | … | … | … |

## 4. DATA FILES (accessible)

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 200 | GET | `https://devin.ai/data/frontier-code-1.1/current-models.json` | application/json | 11609 |  |
| 200 | GET | `https://devin.ai/data/frontier-code-2.0/data.json` | application/json | 34194 |  |
| 200 | GET | `https://devin.ai/data/frontier-code-2.0/fable-5.2-launch.json` | application/json | 7649 |  |
| 200 | GET | `https://devin.ai/data/frontier-code-2.0/gemini-4-carbon-launch.json` | application/json | 7228 |  |
| 200 | GET | `https://devin.ai/data/frontier-code-2.0/gemini-4-hydrogen-launch.json` | application/json | 7962 |  |
| 200 | GET | `https://devin.ai/data/frontier-code-2.0/gemini-4-neon-launch.json` | application/json | 8921 |  |
| 200 | GET | `https://devin.ai/ja/rss.xml` | application/xml | 19519 |  |
| 200 | GET | `https://devin.ai/rss.xml` | application/xml | 104687 |  |
| 200 | GET | `https://devin.ai/rss.xml\` | application/xml | 104687 |  |
| 200 | GET | `https://devin.ai/sitemap.xml` | application/xml | 50382 |  |
| 200 | GET | `https://google.com/ccm/geo` | application/json | 75 |  |
| 200 | GET | `https://vercel.com/api/www/avatar/?u=` | image/svg+xml | 2114 |  |
| 200 | GET | `https://vercel.com/api/www/avatar?u=` | image/svg+xml | 2114 |  |

## 5. SUBDOMAINS (detailed)

Found **54**, DNS-resolved **24**.

| Host | Resolved | Source |
|---|---|---|
| `3ai.devin.krkr.devin.ai` | no | passive |
| `accounts.devin.ai` | no | passive |
| `api-staging.devin.ai` | no | passive |
| `api.devin.ai` | yes | passive |
| `app.beta.devin.ai` | yes | passive |
| `app.devin.ai` | yes | passive |
| `auth.beta.devin.ai` | yes | passive |
| `auth.devin.ai` | yes | passive |
| `autht.devin.ai` | no | passive |
| `beta.devin.ai` | no | passive |
| `blog.devin.ai` | no | passive |
| `cf.devin.ai` | no | passive |
| `clerk.devin.ai` | no | passive |
| `cli.devin.ai` | yes | passive |
| `content.app.devin.ai` | no | passive |
| `content.preview.devin.ai` | no | passive |
| `content7.app.devin.ai` | no | passive |
| `devin.krkr.devin.ai` | no | passive |
| `docs.devin.ai` | yes | passive |
| `docst.devin.ai` | no | passive |
| `fieldkit.devin.ai` | yes | passive |
| `frp-server-0.devin.ai` | yes | passive |
| `frp-server-1.devin.ai` | yes | passive |
| `frp-server-2.devin.ai` | no | passive |
| `frp-server-3.devin.ai` | no | passive |
| `frp-server-4.devin.ai` | no | passive |
| `git-manager.beta.devin.ai` | yes | passive |
| `git-manager.devin.ai` | yes | passive |
| `ibrowser.frp-server-0.devin.ai` | no | passive |
| `ibrowser.frp-server-1.devin.ai` | no | passive |
| `ibrowser.frp-server-2.devin.ai` | no | passive |
| `ibrowser.frp-server-3.devin.ai` | no | passive |
| `ibrowser.frp-server-4.devin.ai` | no | passive |
| `krkr.devin.ai` | no | passive |
| `legacy.devin.ai` | no | passive |
| `mail.devin.ai` | no | passive |
| `mail.p4proxy.beta.devin.ai` | yes | passive |
| `mail.p4proxy.devin.ai` | yes | passive |
| `marketplace.devin.ai` | yes | passive |
| `p4proxy.beta.devin.ai` | yes | passive |
| `p4proxy.devin.ai` | yes | passive |
| `preview.devin.ai` | no | passive |
| `saml.devin.ai` | no | passive |
| `sites.devin.ai` | yes | passive |
| `staging.devin.ai` | no | passive |
| `static.devin.ai` | yes | passive |
| `status.devin.ai` | yes | passive |
| `storybook.devin.ai` | no | passive |
| `storybook1.devin.ai` | no | passive |
| `support.devin.ai` | yes | passive |
| `t.devin.ai` | no | passive |
| `www.devin.ai` | yes | passive |
| `www.p4proxy.beta.devin.ai` | yes | passive |
| `www.p4proxy.devin.ai` | yes | passive |

## 6. VIRTUAL HOSTS (real statuses only)

| Host | Status |
|---|---|
| `fieldkit.devin.ai` | 200 |
| `www.devin.ai` | 308 |
| `docs.devin.ai` | 200 |
| `cli.devin.ai` | 302 |
Blocked/noisy vhost checks (403/530/0) are kept in `vhost_blocked.jsonl` (32).

## 7. JS ENDPOINTS (AST, evidence-backed)

| Method | Path | Confidence |
|---|---|---|
| GET | `/cli` | 0.5 |
| GET | `/cloud` | 0.5 |
| GET | `/community` | 0.5 |
| GET | `/customers` | 0.5 |
| GET | `/desktop` | 0.5 |
| GET | `/government` | 0.5 |
| GET | `/guarantee` | 0.5 |
| GET | `/partners` | 0.5 |
| GET | `/plugins` | 0.5 |
| GET | `/pricing` | 0.5 |
| GET | `/security` | 0.5 |
| GET | `/university` | 0.5 |
| GET | `/windows` | 0.5 |
| GET | `/demo` | 0.5 |
| GET | `/download` | 0.5 |
| GET | `/jetbrains` | 0.5 |
| UNKNOWN | `/signup` | 0.7 |
| UNKNOWN | `/desktop/devin-desktop-faq` | 0.7 |
| UNKNOWN | `/CognitionAI/devin-marketplace` | 0.7 |
| GET | `/customers/angellist-oncall` | 0.5 |
| GET | `/customers/crosby` | 0.5 |
| GET | `/customers/modal` | 0.5 |
| GET | `/customers/reducto` | 0.5 |
| GET | `/.well-known/vercel/jwe` | 0.78 |
| GET | `/assets/brand/motion` | 0.5 |
| UNKNOWN | `/${d}.eps` | 0.6 |
| UNKNOWN | `/${u}/${m}.mov` | 0.6 |
| UNKNOWN | `/${u}/DEVIN_SYMBOL-WORDMARK.aep` | 0.6 |
| UNKNOWN | `/assets/brand/logos/${f}` | 0.6 |
| GET | `/action-err/` | 0.5 |
| GET | `/action/` | 0.5 |
| GET | `/actionp/` | 0.5 |
| GET | `/p/action/` | 0.5 |
| UNKNOWN | `/action-err` | 0.7 |
| UNKNOWN | `/js` | 0.7 |
| UNKNOWN | `/p/action` | 0.7 |
| GET | `/wa/` | 0.5 |
| UNKNOWN | `/collect` | 0.7 |
| UNKNOWN | `/gtag/js?id=G-L4DZSL59Y4` | 0.7 |
| UNKNOWN | `/ads/pixel.js?pixel_id=a2_h6pgq02q3ehg` | 0.7 |
| UNKNOWN | `/gtm.js?id=GTM-KH5W49RR` | 0.7 |
| UNKNOWN | `/pixel/conv/ppt=27178;g=sitewide;gid=71752;ord=` | 0.7 |
| UNKNOWN | `/review` | 0.7 |
| GET | `/assets/images/new-home/frontier-models` | 0.5 |
| GET | `/api/[inferred]` | 0.7 |
| UNKNOWN | `/API_URL=http:/localhost:8080` | 0.7 |
| GET | `/brand` | 0.5 |
| GET | `/ja` | 0.5 |
| GET | `/privacy-choices` | 0.5 |
| UNKNOWN | `/login` | 0.7 |
| UNKNOWN | `/@cognition-labs` | 0.7 |
| UNKNOWN | `/company/cognition-ai-labs` | 0.7 |
| UNKNOWN | `/legal/acceptable-use-policy` | 0.7 |
| UNKNOWN | `/legal/data-processing-statement` | 0.7 |
| UNKNOWN | `/legal/platform-terms-of-service` | 0.7 |
| UNKNOWN | `/legal/privacy-policy` | 0.7 |
| UNKNOWN | `/r/CognitionLabs` | 0.7 |
| UNKNOWN | `/cognition` | 0.7 |
| UNKNOWN | `/analytics/v1/_internal/logs` | 0.7 |
| UNKNOWN | `/analytics/v1` | 0.7 |
| GET | `/api/ordersでのIDOR` | 0.55 |
| GET | `/data/frontier-code-1.1/current-models.json` | 0.5 |
| GET | `/data/frontier-code-2.0/data.json` | 0.5 |
| GET | `/data/frontier-code-2.0/fable-5.2-launch.json` | 0.5 |
| GET | `/data/frontier-code-2.0/gemini-4-carbon-launch.json` | 0.5 |
| GET | `/data/frontier-code-2.0/gemini-4-hydrogen-launch.json` | 0.5 |
| GET | `/data/frontier-code-2.0/gemini-4-neon-launch.json` | 0.5 |
| GET | `/loginでのオープンリダイレクト` | 0.5 |
| UNKNOWN | `/abs/2602.07549` | 0.7 |
| UNKNOWN | `/abs/2602.07962` | 0.7 |
| UNKNOWN | `/abs/2606.14066` | 0.7 |
| UNKNOWN | `/api/errors` | 0.7 |
| UNKNOWN | `/app.devin.ai` | 0.7 |
| UNKNOWN | `/app.devin.ai/org/northstar/settings/authentication` | 0.7 |
| UNKNOWN | `/backend/` | 0.7 |
| UNKNOWN | `/integrations/slack` | 0.7 |
| UNKNOWN | `/MEMORY.md` | 0.7 |
| UNKNOWN | `/posthog/api/posthog.api` | 0.7 |
| UNKNOWN | `/posthog/src/main/java/com/posthog/internal/PostHogLegacyQueue.kt` | 0.7 |
| UNKNOWN | `/posthog/src/main/java/com/posthog/internal/PostHogQueue.kt` | 0.7 |
| UNKNOWN | `/posthog/src/main/java/com/posthog/internal/PostHogSendCachedEventsIntegration.kt` | 0.7 |
| UNKNOWN | `/posthog/src/main/java/com/posthog/PostHog.kt` | 0.7 |
| UNKNOWN | `/tooling/` | 0.7 |
| UNKNOWN | `/login/callback` | 0.7 |
| UNKNOWN | `/app/tools/GSEA_Linux_4.4.0/gsea-cli.sh GSEA` | 0.7 |
| UNKNOWN | `/get-started` | 0.7 |
| GET | `/review` | 0.5 |
| UNKNOWN | `/${n.M}/login` | 0.6 |
| GET | `/ccm/geo` | 0.7 |
| GET | `/a?` | 0.5 |
| GET | `/a?v=3&t=l` | 0.56 |
| GET | `/ag/g/c` | 0.5 |
| GET | `/as` | 0.5 |
| GET | `/as/d` | 0.5 |
| GET | `/as/d/ccm/conversion` | 0.5 |
| GET | `/as/p/c` | 0.5 |
| GET | `/ccm/collect` | 0.5 |
| GET | `/ccm/conversion` | 0.5 |
| GET | `/ccm/form-data` | 0.5 |
| GET | `/ccm/s/collect` | 0.5 |

## 8. PARAMETERS

| URL | Params |
|---|---|
| `https://devin.ai/_next-live/feedback/feedback.html?dpl=dpl_9HT5zTaF2xzcEyHWtKmgxrGf9qpH` | dpl |
| `https://devin.ai/_next-live/feedback/instrument.d676b2a5ce5b14aa6dd7.js?dpl=dpl_9HT5zTaF2xzcEyHWtKmgxrGf9qpH%3Fdpl%3Ddpl_9HT5zTaF2xzcEyHWtKmgxrGf9qpH` | dpl |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.08kenlo3vfwcy.webp&w=1080&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.08kenlo3vfwcy.webp&w=1200&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.08kenlo3vfwcy.webp&w=1920&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.08kenlo3vfwcy.webp&w=2048&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.08kenlo3vfwcy.webp&w=384&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.08kenlo3vfwcy.webp&w=3840&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.08kenlo3vfwcy.webp&w=640&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.08kenlo3vfwcy.webp&w=750&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.08kenlo3vfwcy.webp&w=828&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0eknz0lxesg3y.webp&w=1080&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0eknz0lxesg3y.webp&w=1200&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0eknz0lxesg3y.webp&w=1920&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0eknz0lxesg3y.webp&w=2048&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0eknz0lxesg3y.webp&w=384&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0eknz0lxesg3y.webp&w=3840&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0eknz0lxesg3y.webp&w=640&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0eknz0lxesg3y.webp&w=750&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0eknz0lxesg3y.webp&w=828&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0lhpg6z57_2xq.webp&w=1080&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0lhpg6z57_2xq.webp&w=1200&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0lhpg6z57_2xq.webp&w=1920&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0lhpg6z57_2xq.webp&w=2048&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0lhpg6z57_2xq.webp&w=384&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0lhpg6z57_2xq.webp&w=3840&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0lhpg6z57_2xq.webp&w=640&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0lhpg6z57_2xq.webp&w=750&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0lhpg6z57_2xq.webp&w=828&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0mg2au9n00bxt.webp&w=1080&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0mg2au9n00bxt.webp&w=1200&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0mg2au9n00bxt.webp&w=1920&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0mg2au9n00bxt.webp&w=2048&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0mg2au9n00bxt.webp&w=384&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0mg2au9n00bxt.webp&w=3840&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0mg2au9n00bxt.webp&w=640&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0mg2au9n00bxt.webp&w=750&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0mg2au9n00bxt.webp&w=828&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0tq4w41y2cyz5.webp&w=1080&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0tq4w41y2cyz5.webp&w=1200&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0tq4w41y2cyz5.webp&w=1920&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0tq4w41y2cyz5.webp&w=2048&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0tq4w41y2cyz5.webp&w=384&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0tq4w41y2cyz5.webp&w=3840&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0tq4w41y2cyz5.webp&w=640&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0tq4w41y2cyz5.webp&w=750&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0tq4w41y2cyz5.webp&w=828&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0tsmod7d14bmw.webp&w=1080&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0tsmod7d14bmw.webp&w=1200&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0tsmod7d14bmw.webp&w=1920&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0tsmod7d14bmw.webp&w=2048&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0tsmod7d14bmw.webp&w=384&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0tsmod7d14bmw.webp&w=3840&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0tsmod7d14bmw.webp&w=640&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0tsmod7d14bmw.webp&w=750&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0tsmod7d14bmw.webp&w=828&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0xzo93vtmkjqn.jpg&w=1080&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0xzo93vtmkjqn.jpg&w=1200&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0xzo93vtmkjqn.jpg&w=1920&q=75` | q, url, w |
| `https://devin.ai/_next/image?url=%2F_next%2Fstatic%2Fimmutable%2Fmedia%2Fcover.0xzo93vtmkjqn.jpg&w=2048&q=75` | q, url, w |

## 9. SECRET CANDIDATES

3 candidate(s) in `secrets.jsonl`. Verify manually.

## 10. NUCLEI FINDINGS (verified exposures / misconfigs)

| Severity | Template | Host |
|---|---|---|
| info | `dns-waf-detect` | `luma.com` |
| info | `dns-waf-detect` | `react.dev` |
| info | `dns-waf-detect` | `tally.so` |
| info | `dns-waf-detect` | `tally.so` |
| info | `dns-waf-detect` | `tally.so` |
| info | `dns-waf-detect` | `tally.so` |

## 11. TOOL RUN STATUS (no silent skips)

| Tool | Result | Detail |
|---|---|---|
| `anastasis` | OK | 246 endpoints, 39 params |
| `cariddi` | OK | completed |
| `dnsx` | OK | completed |
| `ffuf` | OK | off by choice — wordlist prepared |
| `getJS` | exit 2 | see logs/ |
| `httpx` | OK | completed |
| `js-download` | OK | 86 chunks saved over 3 round(s) |
| `jscope` | OK | completed |
| `jsluice` | OK | 86 files parsed in batches of 100 |
| `katana` | exit 124 | see logs/ |
| `methods` | OK | 1400 method responses |
| `noseyparker` | OK | completed |
| `nuclei` | OK | 6 findings on 293 live hosts |
| `subfinder` | OK | completed |
| `subjs` | OK | completed |
| `trufflehog` | OK | completed |
| `uncover` | OK | no API key configured — no external data |
| `urlfinder` | OK | completed |
| `uro` | OK | completed |
| `vhost` | OK | 4 real of 36 tested |
| `waybackurls` | OK | completed |
| `x8` | OK | parameter scan complete |

## 12. INTENTIONALLY NOT RUN

- **ffuf path brute** — off by default; `wordlist.txt` is ready. Set `enable_brute: true` later.
- **kiterunner** — off by default alongside ffuf.

## 13. OUTPUT FILES

| File | Meaning |
|---|---|
| [`all_routes.jsonl`](all_routes.jsonl) | every route, unfiltered (1,008,421 B) |
| [`accessible_200.jsonl`](accessible_200.jsonl) | HTTP 200 wins (230,511 B) |
| [`exists_blocked.jsonl`](exists_blocked.jsonl) | exists but blocked (37,867 B) |
| [`other_status.jsonl`](other_status.jsonl) | all other statuses (481,269 B) |
| [`data_files.jsonl`](data_files.jsonl) | JSON/CSV/XML among 200s (8,488 B) |
| [`params.jsonl`](params.jsonl) | parameters (793,046 B) |
| [`subdomains.jsonl`](subdomains.jsonl) | subdomains + resolution (4,369 B) |
| [`third_party_routes.jsonl`](third_party_routes.jsonl) | third-party URLs — kept, not deleted (16,787 B) |
| [`method_responses.jsonl`](method_responses.jsonl) | all method-probe responses — kept (168,338 B) |
| [`vhost_real.jsonl`](vhost_real.jsonl) | non-blocked virtual hosts (186 B) |
| [`vhost_blocked.jsonl`](vhost_blocked.jsonl) | blocked vhost checks — kept (1,563 B) |
| [`js_endpoints.jsonl`](js_endpoints.jsonl) | AST endpoints (23,034 B) |
| [`vhost.jsonl`](vhost.jsonl) | all vhost checks (1,749 B) |
| [`jsluice.jsonl`](jsluice.jsonl) | JS-derived URLs (135,334 B) |
| [`cariddi.txt`](cariddi.txt) | crawl + secrets/endpoints (1,820,287 B) |
| [`wayback_urls.txt`](wayback_urls.txt) | archive URLs (1 B) |
| [`noseyparker.jsonl`](noseyparker.jsonl) | fast secret scan (1 B) |
| [`nuclei.jsonl`](nuclei.jsonl) | verified exposure findings (7,454 B) |
| [`anastasis_endpoints.jsonl`](anastasis_endpoints.jsonl) | AST endpoints (23,034 B) |
| [`jscope.txt`](jscope.txt) | evidence-ranked JS analysis (22,777 B) |
| [`secrets.jsonl`](secrets.jsonl) | secret candidates (1,986 B) |
| [`wordlist.txt`](wordlist.txt) | target-specific fuzz list (162,930 B) |
| [`params.txt`](params.txt) | parameter wordlist (180 B) |
| [`js_urls.txt`](js_urls.txt) | JS chunk URLs (5,491 B) |
| [`logs/`](logs/) | raw tool logs (4,096 B) |

## Status meaning

| Status | Meaning |
|---|---|
| 200 | Accessible — confirmed win |
| 301/302/307/308 | Redirect — route exists |
| 401/403 | Exists but blocked |
| 405 | Exists, wrong method |
| 404 | Not found — kept for completeness |
| 530 | Cloudflare error — excluded from vhosts |

> Collect wide, verify status, categorize last. Nothing deleted from data files.