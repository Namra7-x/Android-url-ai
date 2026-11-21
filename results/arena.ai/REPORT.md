# Hunt Report — https://arena.ai

Generated: 2026-11-21T17:31:33Z &nbsp;|&nbsp; Duration: 6m 54s

> **Nothing is filtered during collection. This report is only a grouping.**

## Summary

| What | Count | Meaning |
|---|---:|---|
| Routes collected | 917 | Every URL found, nothing removed |
| Responses checked | 1810 | Every URL actually requested |
| **Accessible (200)** | **42** | Confirmed live — the wins |
| Exists but different status | 1418 | 301/302/401/403/405 — real route, blocked |
| Other responses | 350 | 404/500/etc — kept, not discarded |
| Subdomains (resolved) | 27 | DNS-verified |
| Virtual hosts (real) | 33 | Cloudflare 530 excluded |
| Parameters | 63 | URLs with query params |
| JS endpoints (AST) | 0 | anastasis evidence-backed |
| Secret candidates | 1 | verify manually |

## 1. SUCCESS — HTTP 200

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 200 | GET | `https://accounts.google.com/gsi/fedcm/config/active.json` | application/json | 1386 | method |
| 200 | OPTIONS | `https://accounts.google.com/gsi/fedcm/config/active.json` |  |  | method |
| 200 | HEAD | `https://accounts.google.com/gsi/fedcm/config/active.json` |  |  | method |
| 200 | GET | `https://ah-cdn-develop.merge.dev/initialize.js` | application/javascript | 9588 | method |
| 200 | HEAD | `https://ah-cdn-develop.merge.dev/initialize.js` |  |  | method |
| 200 | GET | `https://ah-cdn.factorymerge.com/initialize.js` | application/javascript | 9572 | method |
| 200 | HEAD | `https://ah-cdn.factorymerge.com/initialize.js` |  |  | method |
| 200 | GET | `https://ah-cdn.merge.dev` | text/html | 805 | method |
| 200 | HEAD | `https://ah-cdn.merge.dev` |  |  | method |
| 200 | GET | `https://ah-cdn.merge.dev/initialize.js` | application/javascript | 9572 | method |
| 200 | HEAD | `https://ah-cdn.merge.dev/initialize.js` |  |  | method |
| 200 | GET | `https://arena.ai/blog/agent-mode` | text/html | 271500 | method |
| 200 | HEAD | `https://arena.ai/blog/agent-mode` |  |  | method |
| 200 | POST | `https://arena.ai/blog/agent-mode` |  |  | method |
| 200 | POST | `https://arena.ai/cdn-cgi/challenge-platform/h/b/jsd/oneshot/f8df4d4a0cd6/0.05371998817457235:1795278317:We4SxB5i3AqQ8i8WZKvngakEzsY2Y2iUSVm8MMjrkq4/a5e16ba11a39a215` |  |  | method |
| 200 | GET | `https://arena.ai/cdn-cgi/challenge-platform/h/b/scripts/jsd/f8df4d4a0cd6/main.js?ray=a5e16b3acddcaccf` | application/javascript | 43340 | method |
| 200 | HEAD | `https://arena.ai/cdn-cgi/challenge-platform/h/b/scripts/jsd/f8df4d4a0cd6/main.js?ray=a5e16b3acddcaccf` |  |  | method |
| 200 | GET | `https://arena.ai/cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js` | application/javascript | 1239 | method |
| 200 | GET | `https://cdn.jsdelivr.net/npm/chart.js` | application/javascript | 210082 |  |
| 200 | GET | `https://cdn.plot.ly/plotly-2.35.2.js` | application/javascript | 10809095 |  |
| 200 | GET | `https://cdn.plot.ly/plotly-2.35.2.min.js` | application/javascript | 4558696 |  |
| 200 | GET | `https://cdnjs.cloudflare.com` | text/html | 8891 |  |
| 200 | GET | `https://challenges.cloudflare.com` | text/html | 5397 |  |
| 200 | GET | `https://challenges.cloudflare.com/turnstile/v0/b/f8df4d4a0cd6/api.js` | application/javascript | 86968 |  |
| 200 | GET | `https://google.com/recaptcha/enterprise.js?render=6LeTGMcsAAAAALuIlkVwIxaAuZA8VledA6d3Nnb0` | text/javascript | 1155 |  |
| 200 | GET | `https://googletagmanager.com/gtag/js?id=G-L5C4D55WJJ` | application/javascript | 550003 |  |
| 200 | GET | `https://help.arena.ai` | text/html | 26194 |  |
| 200 | GET | `https://help.arena.ai/articles/1820405001-lmarena-cookie-policy` | text/html | 51190 |  |
| 200 | GET | `https://help.arena.ai/articles/3765052346-privacy-policy` | text/html | 386074 |  |
| 200 | GET | `https://help.arena.ai/articles/5629909088-terms-of-use` | text/html | 283271 |  |
| 200 | GET | `https://help.arena.ai/islands/f7c72ed704b1b6d4e60711acb651c4a97dc380a2/kb-islands.js` | application/javascript | 419425 |  |
| 200 | GET | `https://huggingface.co` | text/html | 176724 |  |
| 200 | GET | `https://login.arena.ai/?client_id=client_01KRH0N7FK2QY4YZRY638GH6PV&redirect_uri=https%3A%2F%2Fplatform.arena.ai%2Fauth%2Fcallback&state=Fe26.2%2A1%2A67decd22f2cd74608931005b6590ad7d0945474017cf7b2a97a7c4b7d743a24c%2A8fDJs4-oAXHynb0vGZvkFA%2APnFujZOJvyIa6ZuZbIjFAdwJ6jZiuA0hYVFQAM0dOjmAWfnPeQy4jQ9CXmdBHQYWmKJO6lcZOMpdJ862wHZPELoG_qj7YVyNvq3b8amm5n8C2A-Mbkq0NBSlr94N_FJ-v0O6rMl-h-PnA8g-cbKX3knIoW0JOprJBZrX9p7fVe5zvcGbkDSAvnRH4vI4a7DD%2A1793285104886%2Af6276ab490c23ef241288642f1477fe15e881c6a991dfe57b20a800df142d69a%2ARiUYah1QlEQYPa0cXOI4mnt7QjKl2yiP8hGtGMzIdWU~2&authorization_session_id=01M641BZHADPS78GQ1ERYEWSMM` | text/html | 98761 |  |
| 200 | GET | `https://mail.arena.ai/deliveries/dgT41gwLAIyAzwWLgM8FAaE29Wh0by5HftohAaAJ4g==` | text/html | 24095 |  |
| 200 | GET | `https://mail.arena.ai/manage_subscription_preferences/dgT41gwLAIyAzwWLgM8FAaE29Wh0by5HftohAaAJ4g==` | text/html | 25153 |  |
| 200 | GET | `https://mail.arena.ai/unsubscribe/dgT41gwLAIyAzwWLgM8FAaE29Wh0by5HftohAaAJ4g==` | text/html | 22141 |  |
| 200 | GET | `https://okta.arena.ai/app/UserHome?iss=https%3A%2F%2Fokta.arena.ai&session_hint=AUTHENTICATED` | text/html | 6199 |  |
| 200 | GET | `https://posthog.com` | text/html | 1841556 |  |
| 200 | GET | `https://static.cloudflareinsights.com/beacon.min.js/vce701823e78c4301a35b7e07294d87301792088814092` | text/javascript | 31853 |  |
| 200 | GET | `https://status.arena.ai` | text/html | 462972 |  |
| 200 | GET | `https://vercel.com` | text/html | 601363 |  |
| 200 | GET | `https://vercel.live/_next-live/feedback/feedback.js` | application/javascript | 76110 |  |

## 2. EXISTS BUT DIFFERENT STATUS (301/302/401/403/405)

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 401 | GET | `https://*.static.hf.space` | text/plain | 29 |  |
| 405 | PUT | `https://accounts.google.com/gsi/fedcm/config/active.json` |  |  | method |
| 405 | PATCH | `https://accounts.google.com/gsi/fedcm/config/active.json` |  |  | method |
| 405 | POST | `https://accounts.google.com/gsi/fedcm/config/active.json` |  |  | method |
| 405 | DELETE | `https://accounts.google.com/gsi/fedcm/config/active.json` |  |  | method |
| 301 | GET | `https://agent.arena.ai` | text/html | 167 |  |
| 405 | PATCH | `https://ah-cdn-develop.merge.dev/initialize.js` |  |  | method |
| 405 | PUT | `https://ah-cdn-develop.merge.dev/initialize.js` |  |  | method |
| 405 | POST | `https://ah-cdn-develop.merge.dev/initialize.js` |  |  | method |
| 405 | DELETE | `https://ah-cdn-develop.merge.dev/initialize.js` |  |  | method |
| 405 | OPTIONS | `https://ah-cdn-develop.merge.dev/initialize.js` |  |  | method |
| 405 | OPTIONS | `https://ah-cdn.factorymerge.com/initialize.js` |  |  | method |
| 405 | PUT | `https://ah-cdn.factorymerge.com/initialize.js` |  |  | method |
| 405 | DELETE | `https://ah-cdn.factorymerge.com/initialize.js` |  |  | method |
| 405 | POST | `https://ah-cdn.factorymerge.com/initialize.js` |  |  | method |
| 405 | PATCH | `https://ah-cdn.factorymerge.com/initialize.js` |  |  | method |
| 405 | POST | `https://ah-cdn.merge.dev` |  |  | method |
| 405 | PUT | `https://ah-cdn.merge.dev` |  |  | method |
| 405 | PATCH | `https://ah-cdn.merge.dev` |  |  | method |
| 405 | DELETE | `https://ah-cdn.merge.dev` |  |  | method |
| 405 | OPTIONS | `https://ah-cdn.merge.dev` |  |  | method |
| 405 | PUT | `https://ah-cdn.merge.dev/initialize.js` |  |  | method |
| 405 | PATCH | `https://ah-cdn.merge.dev/initialize.js` |  |  | method |
| 405 | POST | `https://ah-cdn.merge.dev/initialize.js` |  |  | method |
| 405 | DELETE | `https://ah-cdn.merge.dev/initialize.js` |  |  | method |
| 405 | OPTIONS | `https://ah-cdn.merge.dev/initialize.js` |  |  | method |
| 302 | GET | `https://api.arena.ai` | text/html | 49 |  |
| 302 | GET | `https://api.preview.arena.ai` | text/html | 49 |  |
| 405 | DELETE | `https://arena.ai/blog/agent-mode` |  |  | method |
| 405 | PUT | `https://arena.ai/blog/agent-mode` |  |  | method |
| 405 | PATCH | `https://arena.ai/blog/agent-mode` |  |  | method |
| 405 | GET | `https://arena.ai/cdn-cgi/challenge-platform/h/b/jsd/oneshot/f8df4d4a0cd6/0.05371998817457235:1795278317:We4SxB5i3AqQ8i8WZKvngakEzsY2Y2iUSVm8MMjrkq4/a5e16ba11a39a215` |  | 0 | method |
| 405 | PUT | `https://arena.ai/cdn-cgi/challenge-platform/h/b/jsd/oneshot/f8df4d4a0cd6/0.05371998817457235:1795278317:We4SxB5i3AqQ8i8WZKvngakEzsY2Y2iUSVm8MMjrkq4/a5e16ba11a39a215` |  |  | method |
| 405 | HEAD | `https://arena.ai/cdn-cgi/challenge-platform/h/b/jsd/oneshot/f8df4d4a0cd6/0.05371998817457235:1795278317:We4SxB5i3AqQ8i8WZKvngakEzsY2Y2iUSVm8MMjrkq4/a5e16ba11a39a215` |  |  | method |
| 405 | DELETE | `https://arena.ai/cdn-cgi/challenge-platform/h/b/jsd/oneshot/f8df4d4a0cd6/0.05371998817457235:1795278317:We4SxB5i3AqQ8i8WZKvngakEzsY2Y2iUSVm8MMjrkq4/a5e16ba11a39a215` |  |  | method |
| 405 | OPTIONS | `https://arena.ai/cdn-cgi/challenge-platform/h/b/jsd/oneshot/f8df4d4a0cd6/0.05371998817457235:1795278317:We4SxB5i3AqQ8i8WZKvngakEzsY2Y2iUSVm8MMjrkq4/a5e16ba11a39a215` |  |  | method |
| 405 | PATCH | `https://arena.ai/cdn-cgi/challenge-platform/h/b/jsd/oneshot/f8df4d4a0cd6/0.05371998817457235:1795278317:We4SxB5i3AqQ8i8WZKvngakEzsY2Y2iUSVm8MMjrkq4/a5e16ba11a39a215` |  |  | method |
| 405 | POST | `https://arena.ai/cdn-cgi/challenge-platform/h/b/scripts/jsd/f8df4d4a0cd6/main.js?ray=a5e16b3acddcaccf` |  |  | method |
| 405 | PUT | `https://arena.ai/cdn-cgi/challenge-platform/h/b/scripts/jsd/f8df4d4a0cd6/main.js?ray=a5e16b3acddcaccf` |  |  | method |
| 405 | DELETE | `https://arena.ai/cdn-cgi/challenge-platform/h/b/scripts/jsd/f8df4d4a0cd6/main.js?ray=a5e16b3acddcaccf` |  |  | method |
| 405 | PATCH | `https://arena.ai/cdn-cgi/challenge-platform/h/b/scripts/jsd/f8df4d4a0cd6/main.js?ray=a5e16b3acddcaccf` |  |  | method |
| 405 | OPTIONS | `https://arena.ai/cdn-cgi/challenge-platform/h/b/scripts/jsd/f8df4d4a0cd6/main.js?ray=a5e16b3acddcaccf` |  |  | method |
| 302 | GET | `https://arena.ai/cdn-cgi/challenge-platform/scripts/jsd/main.js?ray=a5e16b3acddcaccf` |  | 0 |  |
| 403 | GET | `https://arena.ai/de/leaderboard` | text/html | 5685 | method |
| 403 | POST | `https://arena.ai/de/leaderboard` |  |  | method |
| 403 | PATCH | `https://arena.ai/de/leaderboard` |  |  | method |
| 403 | DELETE | `https://arena.ai/de/leaderboard` |  |  | method |
| 403 | PUT | `https://arena.ai/de/leaderboard` |  |  | method |
| 403 | OPTIONS | `https://arena.ai/de/leaderboard` |  |  | method |
| 403 | HEAD | `https://arena.ai/de/leaderboard` |  |  | method |
| 403 | GET | `https://arena.ai/es/leaderboard/text` | text/html | 5679 | method |
| 403 | POST | `https://arena.ai/es/leaderboard/text` |  |  | method |
| 403 | PATCH | `https://arena.ai/es/leaderboard/text` |  |  | method |
| 403 | OPTIONS | `https://arena.ai/es/leaderboard/text` |  |  | method |
| 403 | DELETE | `https://arena.ai/es/leaderboard/text` |  |  | method |
| 403 | HEAD | `https://arena.ai/es/leaderboard/text` |  |  | method |
| 403 | PUT | `https://arena.ai/es/leaderboard/text` |  |  | method |
| 403 | GET | `https://arena.ai/he/leaderboard` | text/html | 5685 | method |
| 403 | PUT | `https://arena.ai/he/leaderboard` |  |  | method |
| 403 | POST | `https://arena.ai/he/leaderboard` |  |  | method |
| 403 | OPTIONS | `https://arena.ai/he/leaderboard` |  |  | method |
| 403 | PATCH | `https://arena.ai/he/leaderboard` |  |  | method |
| 403 | HEAD | `https://arena.ai/he/leaderboard` |  |  | method |
| 403 | DELETE | `https://arena.ai/he/leaderboard` |  |  | method |
| 403 | GET | `https://arena.ai/ko/leaderboard` | text/html | 5707 | method |
| 403 | POST | `https://arena.ai/ko/leaderboard` |  |  | method |
| 403 | PUT | `https://arena.ai/ko/leaderboard` |  |  | method |
| 403 | DELETE | `https://arena.ai/ko/leaderboard` |  |  | method |
| 403 | PATCH | `https://arena.ai/ko/leaderboard` |  |  | method |
| 403 | OPTIONS | `https://arena.ai/ko/leaderboard` |  |  | method |
| 403 | HEAD | `https://arena.ai/ko/leaderboard` |  |  | method |
| 403 | GET | `https://arena.ai/leaderboard/agent.` | text/html | 5676 | method |
| 403 | PUT | `https://arena.ai/leaderboard/agent.` |  |  | method |
| 403 | PATCH | `https://arena.ai/leaderboard/agent.` |  |  | method |
| 403 | OPTIONS | `https://arena.ai/leaderboard/agent.` |  |  | method |
| … | … | _1343 more in JSONL_ | … | … | … |

## 3. OTHER RESPONSES — kept, never discarded

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 400 | GET | `https://*.27c852f3500f38c1e7786e2c9ff9e48f.r2.cloudflarestorage.com` | text/html | 155 |  |
| 400 | GET | `https://*.arena.site` | text/html | 155 |  |
| 400 | GET | `https://*.staging.arena.site` | text/html | 155 |  |
| 404 | GET | `https://accounts.google.com/gsi` | text/html | 1652 |  |
| 429 | GET | `https://arena.ai` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/...` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/240/112` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/360` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/:$1` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/:xatebat904` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/Cost/task` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/OBJECT_TYPE/LICENSE_PLATE` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/Time/task` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/Tokens/task` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_head` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_index` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/image` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/${e}` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/0-_ubvabx48tu.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/0-cq6hvlwvlks.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/005bbm0tn8g1j.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/03j5mppd_og9f.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/061kqs79vrm8p.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/07f3c_puwbvq2.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/08ak2-rh0sgpw.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/0929u1b8ez7do.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/093-t93wqbnc3.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/0a8wj--9yy0a7.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/0bk1d6v-h03ej.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/0br91nzz7ltmr.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/0c0hxoamwjsbw.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/0c11p-gj29peh.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/0c99ncz16pkrk.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/0dew-b447dl1r.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/0g9lg5h-p0vqg.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/0hdpx0p3_ol_n.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/0hqjpbpyidd81.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/0j31dchtnmwrl.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/0lq6bk9dcvwg9.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/0ol-z_st5xwdu.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/0rfvmwnyuugnz.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/0srd8zb_7aa1v.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/0u3g3do4utk27.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/0zo-2qizay3_w.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/0ztb00qdwr8xe.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/10efcubsvxoxy.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/10tzhw4tqf040.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/147eees7ngsdy.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/14l8hnfn692xl.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/15sbgm38d4x7o.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/193_zk4a3xwn-.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/1ctikdfzfe1z_.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/1e2yy810rj6sm.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/1g-f61scvexz2.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/1h82wkhd8ojue.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/1inimb4h0jv0q.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/1n79sps_9wp-k.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/1nfry24yjor98.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/1njlxczxc-v1d.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/1nu7ocq9ow0_a.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/1p-cm8kx5pwzz.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/1q-zxaum_yo05.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/1rdvsvkvrstgr.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/1xq65hsit5wqr.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/1zi5d-ncga-v6.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/2--ilmdqh8nfv.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/20g1ey3p8k1f6.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/20uhfdw4q8fp0.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/21mqd_d02un4i.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/22d72uq_gizvj.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/239ilxz0bw00q.js` | text/plain | 17 |  |
| 429 | GET | `https://arena.ai/_next/static/immutable/chunks/24w23oh83zsrj.js` | text/plain | 17 |  |
| … | … | _275 more in JSONL_ | … | … | … |

## 4. DATA FILES (accessible)

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 200 | GET | `https://accounts.google.com/gsi/fedcm/config/active.json` | application/json | 1386 | method |
| 200 | OPTIONS | `https://accounts.google.com/gsi/fedcm/config/active.json` |  |  | method |
| 200 | HEAD | `https://accounts.google.com/gsi/fedcm/config/active.json` |  |  | method |

## 5. SUBDOMAINS (detailed)

Found **64**, DNS-resolved **27**.

| Host | Resolved | Source |
|---|---|---|
| `agent.arena.ai` | yes | passive |
| `api-gateway-bill.dev.ent.arena.ai` | no | passive |
| `api-gateway-derry.dev.ent.arena.ai` | no | passive |
| `api-gateway-jisoo.dev.ent.arena.ai` | no | passive |
| `api-gateway-kunaal.dev.ent.arena.ai` | no | passive |
| `api-gateway.staging.ent.arena.ai` | no | passive |
| `api-k8s.preview.arena.ai` | no | passive |
| `api-preview.arena.ai` | no | passive |
| `api.arena.ai` | yes | passive |
| `api.preview.arena.ai` | yes | passive |
| `api2.preview.arena.ai` | no | passive |
| `auth.arena.ai` | yes | passive |
| `autodiscover.arena.ai` | no | passive |
| `blog.arena.ai` | yes | passive |
| `canary.arena.ai` | yes | passive |
| `cdn.arena.ai` | yes | passive |
| `cn.arena.ai` | yes | passive |
| `code.arena.ai` | yes | passive |
| `console.arena.ai` | yes | passive |
| `cpanel.arena.ai` | no | passive |
| `cpcalendars.arena.ai` | no | passive |
| `cpcontacts.arena.ai` | no | passive |
| `download.arena.ai` | yes | passive |
| `email.arena.ai` | no | passive |
| `gateway-bill.dev.ent.arena.ai` | no | passive |
| `gateway-derry.dev.ent.arena.ai` | no | passive |
| `gateway-jisoo.dev.ent.arena.ai` | no | passive |
| `gateway-kunaal.dev.ent.arena.ai` | no | passive |
| `gateway.bill.dev.ent.arena.ai` | no | passive |
| `gateway.staging.ent.arena.ai` | no | passive |
| `grafana.dev.ent.arena.ai` | no | passive |
| `grafana.kunaal.dev.ent.arena.ai` | no | passive |
| `grafana.ops.dev.ent.arena.ai` | no | passive |
| `grafana.ops.preview.arena.ai` | no | passive |
| `grafana.ops.staging.ent.arena.ai` | no | passive |
| `hello-world.jisoo.dev.ent.arena.ai` | no | passive |
| `help.arena.ai` | yes | passive |
| `indexable.arena.ai` | yes | passive |
| `jisoo.dev.ent.arena.ai` | no | passive |
| `load-test-results.ops.dev.ent.arena.ai` | no | passive |
| `login.arena.ai` | yes | passive |
| `mail.arena.ai` | yes | passive |
| `mta-sts.arena.ai` | yes | passive |
| `mta-sts.everify.arena.ai` | yes | passive |
| `news.arena.ai` | yes | passive |
| `okta.arena.ai` | yes | passive |
| `oldblog.arena.ai` | yes | passive |
| `openpgpkey.arena.ai` | yes | passive |
| `ops.preview.arena.ai` | no | passive |
| `platform.arena.ai` | yes | passive |
| `portal-k8s.api.preview.arena.ai` | no | passive |
| `portal.api-preview.arena.ai` | yes | passive |
| `portal.api.preview.arena.ai` | yes | passive |
| `portal2.api.preview.arena.ai` | no | passive |
| `preview.arena.ai` | no | passive |
| `pricing-analysis.kunaal.dev.ent.arena.ai` | no | passive |
| `pricing-analysis.ops.dev.ent.arena.ai` | no | passive |
| `salesforce-pitch.ops.dev.ent.arena.ai` | no | passive |
| `status.arena.ai` | yes | passive |
| `statuspage.arena.ai` | no | passive |
| `trust.arena.ai` | yes | passive |
| `webdisk.arena.ai` | no | passive |
| `webmail.arena.ai` | no | passive |
| `www.arena.ai` | yes | passive |

## 6. VIRTUAL HOSTS (real statuses only)

| Host | Status |
|---|---|
| `code.arena.ai` | 403 |
| `console.arena.ai` | 403 |
| `api.arena.ai` | 403 |
| `cdn.arena.ai` | 403 |
| `cpanel.arena.ai` | 403 |
| `cpcontacts.arena.ai` | 403 |
| `cpcalendars.arena.ai` | 403 |
| `api-preview.arena.ai` | 403 |
| `agent.arena.ai` | 403 |
| `mail.arena.ai` | 403 |
| `blog.arena.ai` | 403 |
| `auth.arena.ai` | 403 |
| `canary.arena.ai` | 403 |
| `cn.arena.ai` | 403 |
| `help.arena.ai` | 403 |
| `autodiscover.arena.ai` | 403 |
| `login.arena.ai` | 403 |
| `download.arena.ai` | 403 |
| `email.arena.ai` | 403 |
| `mta-sts.arena.ai` | 403 |
| `oldblog.arena.ai` | 403 |
| `openpgpkey.arena.ai` | 403 |
| `status.arena.ai` | 403 |
| `okta.arena.ai` | 403 |
| `platform.arena.ai` | 403 |
| `webdisk.arena.ai` | 403 |
| `webmail.arena.ai` | 403 |
| `statuspage.arena.ai` | 403 |
| `news.arena.ai` | 403 |
| `preview.arena.ai` | 403 |
| `trust.arena.ai` | 403 |
| `www.arena.ai` | 403 |
| `indexable.arena.ai` | 403 |

## 7. JS ENDPOINTS (AST, evidence-backed)

_None extracted._

## 8. PARAMETERS

| URL | Params |
|---|---|
| `https://arena.ai/api/early_access_features/?token=` | token |
| `https://arena.ai/api/product_tours/?token=` | token |
| `https://arena.ai/api/surveys/?token=` | token |
| `https://arena.ai/api/web_experiments/?token=` | token |
| `https://arena.ai/cdn-cgi/challenge-platform/h/b/scripts/jsd/f8df4d4a0cd6/main.js?ray=a5e16b3acddcaccf` | ray |
| `https://arena.ai/cdn-cgi/challenge-platform/h/b/scripts/jsd/f8df4d4a0cd6/main.js?ray=a5e16ba11a39a215` | ray |
| `https://arena.ai/cdn-cgi/challenge-platform/scripts/jsd/main.js?ray=a5e16b3acddcaccf` | ray |
| `https://arena.ai/chat?_rsc=ry-B8umWgNEV4JR9` | _rsc |
| `https://arena.ai/cms/_next/static/chunks/05c4bb8c607b7ae3.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/0731399314762457.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/13445023d82eae1b.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/27ff602b8fc239e3.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/284ec3d0f2bfdc7e.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/291867d0316ebc27.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/307bb90312dfe0e9.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/376d23f3eccecb96.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/3a3f6b15d2958488.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/403ad5d70ac93670.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/47d03c022ccaed41.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/537418f77e124a8a.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/61e3f489fadba75d.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/643bc4436fe73c22.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/737e2963a2553154.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/7666b7b6b72fb234.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/77a5c6c9d4947acd.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/7dabb3c7c86dff64.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/8d92f502884be1b0.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/932c997673ffca02.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/94087be75c2e5547.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/974dec2dbb503c16.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/a6dad97d9634a72d.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/af4977488df03dbc.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/be48166f4b055d9b.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/c87e9b817de427e9.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/c99335402c8c703c.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/ca330e6c1f0f0588.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/cfb469ec79de724c.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/d651274a1d983081.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/e47fb5589d53a989.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/ea5ceebb0b0db6d1.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/fc9b5206e8bfa22c.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/cms/_next/static/chunks/turbopack-2e0e151a233ce8f5.js?dpl=dpl_7DBkgiawVfo9iwvAuYjayMVpc8s9` | dpl |
| `https://arena.ai/code?_rsc=ry-B8umWgNEV4JR9` | _rsc |
| `https://arena.ai/flags/?v=2` | v |
| `https://arena.ai/history/search?_rsc=ry-B8umWgNEV4JR9` | _rsc |
| `https://arena.ai/image?_rsc=ry-B8umWgNEV4JR9` | _rsc |
| `https://arena.ai/issues/?project=` | project |
| `https://arena.ai/leaderboard/agent?ref=arena.ai` | ref |
| `https://arena.ai/leaderboard/image-edit?model_a=max` | model_a |
| `https://arena.ai/leaderboard?_rsc=ry-B8umWgNEV4JR9` | _rsc |
| `https://arena.ai/rpc/api/surveys/?token=phc_LG7IJbVJqBsk584rbcKca0D5lV2vHguiijDrVji7yDM` | token |
| `https://arena.ai/rpc/flags/?v=2` | v |
| `https://arena.ai/rpc/static/dead-clicks-autocapture.js?v=1.360.0` | v |
| `https://arena.ai/rpc/static/exception-autocapture.js?v=1.360.0` | v |
| `https://arena.ai/rpc/static/surveys.js?v=1.360.0` | v |
| `https://arena.ai/rpc/static/web-vitals.js?v=1.360.0` | v |
| `https://arena.ai/search?_rsc=ry-B8umWgNEV4JR9` | _rsc |
| `https://arena.ai/text?_rsc=ry-B8umWgNEV4JR9` | _rsc |
| `https://arena.ai/video?_rsc=ry-B8umWgNEV4JR9` | _rsc |
| `https://google.com/recaptcha/enterprise.js?render=6LeTGMcsAAAAALuIlkVwIxaAuZA8VledA6d3Nnb0` | render |

## 9. SECRET CANDIDATES

1 candidate(s) in `secrets.jsonl`. Verify manually.

## 10. TOOL RUN STATUS (no silent skips)

| Tool | Result | Detail |
|---|---|---|
| `anastasis` | exit 1 | see logs |
| `dnsx` | OK | completed |
| `ffuf` | OK | off by choice — wordlist prepared |
| `gau` | OK | completed |
| `gospider` | OK | completed |
| `httpx` | OK | completed |
| `js-download` | OK | no JS URLs found |
| `jscope` | OK | no local chunks to analyse |
| `jsluice` | OK | 0 files parsed |
| `katana` | OK | completed |
| `methods` | OK | 1393 method responses |
| `subfinder` | OK | completed |
| `trufflehog` | OK | completed |
| `uncover` | OK | no API key configured — no external data |
| `urlfinder` | OK | completed |
| `uro` | OK | completed |
| `vhost` | OK | 33 real of 33 tested |
| `x8` | OK | parameter scan complete |

## 11. INTENTIONALLY NOT RUN

- **ffuf path brute** — off by default; `wordlist.txt` is ready. Set `enable_brute: true` later.
- **kiterunner** — off by default alongside ffuf.

## 12. OUTPUT FILES

| File | Meaning |
|---|---|
| [`all_routes.jsonl`](all_routes.jsonl) | every route, unfiltered (107,996 B) |
| [`accessible_200.jsonl`](accessible_200.jsonl) | HTTP 200 wins (33,499 B) |
| [`exists_blocked.jsonl`](exists_blocked.jsonl) | exists but blocked (347,070 B) |
| [`other_status.jsonl`](other_status.jsonl) | all other statuses (260,537 B) |
| [`data_files.jsonl`](data_files.jsonl) | JSON/CSV/XML among 200s (973 B) |
| [`params.jsonl`](params.jsonl) | parameters (8,599 B) |
| [`subdomains.jsonl`](subdomains.jsonl) | subdomains + resolution (5,428 B) |
| [`js_endpoints.jsonl`](js_endpoints.jsonl) | AST endpoints (0 B) |
| [`vhost.jsonl`](vhost.jsonl) | vhost checks (1,594 B) |
| [`jsluice.jsonl`](jsluice.jsonl) | JS-derived URLs (0 B) |
| [`gospider.txt`](gospider.txt) | second crawler URLs (44,546 B) |
| [`secrets.jsonl`](secrets.jsonl) | secret candidates (653 B) |
| [`wordlist.txt`](wordlist.txt) | target-specific fuzz list (82,795 B) |
| [`params.txt`](params.txt) | parameter wordlist (97 B) |
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