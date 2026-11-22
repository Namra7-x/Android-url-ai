# Hunt Report — https://aistudio.google.com

Generated: 2026-11-22T20:28:07Z &nbsp;|&nbsp; Duration: 123m 36s

> **Nothing is filtered during collection. This report is only a grouping.**

## Summary

| What | Count | Meaning |
|---|---:|---|
| Routes collected | 18554 | Every URL found, nothing removed |
| Distinct routes verified | 9469 | One row per URL (method probes excluded) |
| HTTP responses | 10429 | Includes method probes — kept in `method_responses.jsonl` |
| **Accessible (200)** | **3523** | Confirmed live — the wins |
| Exists but different status | 4518 | 301/302/401/403/405 — real route, blocked |
| Other responses | 1428 | 404/500/etc — kept, not discarded |
| Subdomains (resolved) | 1 | DNS-verified |
| Virtual hosts (real) | 1 | Cloudflare 403/530/0 excluded |
| Parameters | 6155 | URLs with query params |
| JS endpoints (AST) | 0 | anastasis evidence-backed |
| First-party URLs | 9007 | aistudio.google.com and subdomains |
| Third-party URLs | 9547 | kept in `third_party_routes.jsonl` |
| Method responses | 1120 | kept in `method_responses.jsonl` |
| Blocked vhost checks | 0 | kept in `vhost_blocked.jsonl` |
| Secret candidates | 17 | verify manually |

> Collection keeps third-party URLs by design (9547). See `third_party_routes.jsonl`. Method-probe responses are in `method_responses.jsonl`.

## 1. SUCCESS — HTTP 200

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 200 | GET | `https://accounts.google.com/a/tesserent.com/acs` | text/html | 0 |  |
| 200 | GET | `https://accounts.google.com/gsi/client` | application/javascript | 279616 |  |
| 200 | GET | `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Faistudio.google.com%2Flibrary&dsh=S118289191%3A1795376600318879&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Faistudio.google.com%2Flibrary&ltmpl=aistudio&TL=AAxq8nt8geehhf0PGF__d_yQG8fiPQ3hG9-sZfehMxJ2QHVPYXxxJJwn0hGztivm` | text/html | 1029030 |  |
| 200 | GET | `https://accounts.google.com/o/oauth2/iframe` | text/html | 578 |  |
| 200 | GET | `https://accounts.google.com/o/oauth2/postmessageRelay` | text/html | 566 |  |
| 200 | GET | `https://accounts.google.com/signin/v2/usernamerecovery?continue=https%3A%2F%2Faistudio.google.com%2Flibrary&dsh=S118289191%3A1795376600318879&flowEntry=ServiceLogin&flowName=GlifWebSignIn&followup=https%3A%2F%2Faistudio.google.com%2Flibrary&ltmpl=aistudio` | text/html | 3754647 |  |
| 200 | GET | `https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Faistudio.google.com%2Flogs&followup=https%3A%2F%2Faistudio.google.com%2Flogs&ltmpl=aistudio&passive=1209600&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-1508547457%3A1795376600314480` | text/html | 1250472 |  |
| 200 | GET | `https://adservice.google.com/ddm/fls/z/dc_pre=CJGtxLq355cDFcu4Wggd0dMmOg` | image/gif | 42 |  |
| 200 | GET | `https://aistudio.google.com/_/MakerSuite/manifest.json` | application/manifest+json | 1195 |  |
| 200 | GET | `https://aistudio.google.com/api-reference.md` | text/markdown | 11449 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/agents` | text/html | 77583 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/agents/list-agents` | text/html | 79910 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/all-` | text/html | 66635 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/all-methods?hl=es-419` | text/html | 92174 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/api-versions` | text/html | 77384 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/batch-api/async-batch-embed-content` | text/html | 141660 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/batch-api/batch-generate-content` | text/html | 315685 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/batch-api/cancel-batch` | text/html | 68732 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/batch-api/delete-batch` | text/html | 36658 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/batch-api/get-batch` | text/html | 71287 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/batch-api/list-batches` | text/html | 71994 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/batch-api/update-embed-content-batch` | text/html | 100012 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/batch-api/update-generate-content-batch` | text/html | 330968 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/caching` | text/html | 137664 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/caching/create-cached-content` | text/html | 152559 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/caching/get-cached-content` | text/html | 72829 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/caching/update-cached-content` | text/html | 143184 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/credentials/create-credential` | text/html | 74625 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/credentials/delete-credential` | text/html | 68821 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/credentials/get-credential` | text/html | 71264 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/credentials/list-credentials` | text/html | 38667 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/credentials/update-credential` | text/html | 73136 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/embeddings` | text/html | 104529 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/embeddings/batch-embed-contents` | text/html | 69245 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/embeddings/embed-content` | text/html | 67864 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/environments/delete-environment` | text/html | 70184 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/environments/get-environment-files` | text/html | 78090 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/environments/list-environments` | text/html | 77271 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/environments/start-environment-file-upload` | text/html | 70057 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/file-search/documents/delete-document` | text/html | 37148 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/file-search/documents/get-document` | text/html | 72518 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/file-search/documents/list-documents` | text/html | 42713 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/file-search/file-search-stores/delete-file-search-store` | text/html | 68755 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/files` | text/html | 41579 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/files/create-file` | text/html | 94756 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/files/delete-file` | text/html | 70204 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/ge` | text/html | 68021 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/generate-content` | text/html | 171561 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/generate-content.md` | text/markdown | 103146 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/generate-content.openapi.json` | application/json | 279253 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/generate-content/generate-content?generate-content=true` | text/html | 192999 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/generate-content/stream-generate-content` | text/html | 183697 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/interactions-api` | text/html | 288489 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/interactions-api/cancel-interaction-by-id` | text/html | 204742 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/interactions-api/create-interaction` | text/html | 426871 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/interactions.openapi.json.` | text/html | 67267 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/live` | text/html | 72074 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/live-music` | text/html | 78798 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/live-music/bidi-generate-music` | text/html | 71475 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/models` | text/html | 71511 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/models/list-models` | text/html | 73790 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/triggers/delete-trigger` | text/html | 68644 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/triggers/run-trigger` | text/html | 70212 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/triggers/update-trigger` | text/html | 67382 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/voices` | text/html | 48485 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/voices/create-voice` | text/html | 94133 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/voices/delete-voice` | text/html | 69533 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/voices/get-voice` | text/html | 79534 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/webhooks/create-webhook` | text/html | 73069 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/webhooks/delete-webhook` | text/html | 68160 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/webhooks/ping-webhook` | text/html | 68721 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/webhooks/rotate-signing-secret` | text/html | 68717 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/webhooks/update-webhook` | text/html | 72087 |  |
| 200 | GET | `https://aistudio.google.com/api-reference?e=0` | text/html | 47864 |  |
| 200 | GET | `https://aistudio.google.com/api-reference?hl=en` | text/html | 79432 |  |
| … | … | _3448 more in JSONL_ | … | … | … |

## 2. EXISTS BUT DIFFERENT STATUS (301/302/401/403/405)

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 302 | GET | `https://access.workspace.google.com` | text/html | 226 |  |
| 302 | GET | `https://accounts.google.com` | text/html | 365 |  |
| 302 | GET | `https://accounts.google.com/AccountChooser?continue=https%3A%2F%2Faistudio.google.com%2Fapp%2Fgtm.js&followup=https%3A%2F%2Faistudio.google.com%2Fapp%2Fgtm.js&ltmpl=aistudio` | text/html | 448 |  |
| 302 | GET | `https://accounts.google.com/AccountChooser?continue=https%3A%2F%2Fsites.google.com%2Fsite%2Funwanted86%2Fjavascript%2Fbubblecursor.js&followup=https%3A%2F%2Fsites.google.com%2Fsite%2Funwanted86%2Fjavascript%2Fbubblecursor.js&osid=1&service=wise` | text/html | 523 |  |
| 302 | GET | `https://accounts.google.com/Logout?continue=https%3A%2F%2Faccounts.google.com%2Frestart%3Fcontinue%3Dhttps%3A%2F%2Fsites.google.com%2Fsite%2Funwanted86%2Fjavascript%2Fbubblecursor.js%26dsh%3DS118289191%3A1795376609153479%26flowEntry%3DServiceLogin%26flowName%3DGlifWebSignIn%26followup%3Dhttps%3A%2F%2Fsites.google.com%2Fsite%2Funwanted86%2Fjavascript%2Fbubblecursor.js%26osid%3D1%26service%3Dwise` | text/html | 0 |  |
| 302 | GET | `https://accounts.google.com/o/oauth2/auth` | text/html | 534 |  |
| 302 | GET | `https://accounts.google.com/signin/recovery?flowName=GlifWebSignIn&continue=https%3A%2F%2Faistudio.google.com%2Fapp%2Fgtm.js&followup=https%3A%2F%2Faistudio.google.com%2Fapp%2Fgtm.js&ltmpl=aistudio` | text/html | 470 |  |
| 302 | GET | `https://accounts.google.com/signin/recovery?flowName=GlifWebSignIn&continue=https%3A%2F%2Fsites.google.com%2Fsite%2Funwanted86%2Fjavascript%2Fbubblecursor.js&followup=https%3A%2F%2Fsites.google.com%2Fsite%2Funwanted86%2Fjavascript%2Fbubblecursor.js&osid=1&service=wise` | text/html | 546 |  |
| 302 | GET | `https://accounts.google.com/signin/v2/challenge/ippenter` | text/html | 249 |  |
| 302 | GET | `https://accounts.google.com/v3/signin/interstitial/doritos/forward/success?continue=https%3A%2F%2Fsites.google.com%2Fsite%2Funwanted86%2Fjavascript%2Fbubblecursor.js&timeStmp=1795376609237` | application/binary | 0 |  |
| 302 | GET | `https://accounts.google.com/v3/signin/interstitial/doritos/forward/timeout?continue=https%3A%2F%2Fsites.google.com%2Fsite%2Funwanted86%2Fjavascript%2Fbubblecursor.js&timeStmp=1795376609237` | application/binary | 0 |  |
| 302 | GET | `https://ads.google.com/aw/billing/summary` | application/binary | 0 |  |
| 302 | GET | `https://ads.google.com/aw/campaigns` | application/binary | 0 |  |
| 302 | GET | `https://ads.google.com/aw/identity/verification` | application/binary | 0 |  |
| 302 | GET | `https://ads.google.com/aw/identity/verification0s` | application/binary | 0 |  |
| 302 | GET | `https://ads.google.com/aw/overview` | application/binary | 0 |  |
| 302 | GET | `https://ads.google.com/aw/settings/account` | application/binary | 0 |  |
| 301 | GET | `https://ads.google.com/intl/en_au/home/tools/keyword` | application/binary | 0 |  |
| 302 | GET | `https://ads.google.com/nav/selectaccount` | application/binary | 0 |  |
| 302 | GET | `https://ai.google.com` | text/html | 312 |  |
| 302 | GET | `https://ai.google.com/25366l0s68779/theme/public/app.json` | text/html | 250 |  |
| 302 | GET | `https://ai.google.com/48e236h4442687/styles.json` | text/html | 241 |  |
| 302 | GET | `https://ai.google.com/build/2397867y08405` | text/html | 234 |  |
| 302 | GET | `https://aistudio.google.com` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/ ` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/  ` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/ - Ai acces la cele mai noi modele de la Google (inainte sa fie disponibile pe Gemini App). E my go to in 9 cazuri din zece. Ca modele` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/ Google AI Studio's New Conversational Audio Generation (Powered by Gemini AI) Google AI Studio now offers powerful text-to-audio generation directly from your text prompts. Key Features: Conversational Dialogue: Easily create natural-sounding conversations with multiple distinct speakers from your written dialogue. Customizable Voices: Control each speaker's voice` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/ May use vpn` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/ has 1.048.576 (1mill) token length - try that.` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/ https://chatgpt.com/g/g-Nofz6BD8Q-drawing` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/ https://chatgpt.com/g/g-V9jy1iKh4-xgg https://chatgpt.com/g/g-Ldyfxu6ve-guxg` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/ https://chatgpt.com/g/g-V9jy1iKh4-xgg https://chatgpt.com/g/g-Nofz6BD8Q-drawing` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/ is free and has a very good context window and a very good understanding of the context window but you have to save your stuff` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/ might be useful if you are not using some ai code editor like cursor` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/ new google experimental model` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/&` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/&amp` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/&lt` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/&quot` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/(2025` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/))\n\n` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/))\n\n3.` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/).\n\n2.` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/)\n![Google` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/)\n*` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/)\n-` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/)\n3.` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/)で、金輪際「免責事項」がでなくなります。` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/*` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/*/prompts/*` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/*\` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/*prompts/*` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/*star*` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/*watermark*` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/-` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/---Google` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/.*` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/.../1KBzflN1fRZwggPTfBDHLQL87...` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/.36` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/.Huang` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/.No` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com//search` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/29323a26250f1f02010032677c6e163c363c12181907150c72735b68Grok` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/2https://cloud.google.com/vertex-ai` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/2https://cloud.google.com/vertex-ai19` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/6https://www.alibabacloud.com/en/product` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/6https://www.alibabacloud.com/en/product/modelstudio` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/6https://www.alibabacloud.com/en/product/modelstudioIn` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/6https://www.langchain.com` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/6https://www.langchain.com/(a` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/823511539352-ojaretejk1s95sdvkic0te923pt7knpu.apps.googleusercontent.com` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/8https://chatgpt.com` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/8https://chatgpt.com9https://deepinfra.com` | application/binary | 0 |  |
| 302 | GET | `https://aistudio.google.com/8https://chatgpt.com9https://deepinfra.com/18` | application/binary | 0 |  |
| … | … | _4443 more in JSONL_ | … | … | … |

## 3. OTHER RESPONSES — kept, never discarded

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 404 | GET | `http://cariad.corp-partner.google.com` | text/html | 1561 |  |
| 404 | GET | `http://fii-na.corp-partner.google.com` | text/html | 1561 |  |
| 404 | GET | `https://accounts.google.com/&amp` | text/html | 1652 |  |
| 404 | GET | `https://accounts.google.com/&followup=https:/accounts.google.com` | text/html | 1652 |  |
| 404 | GET | `https://accounts.google.com/RotateCookiesgemini` | text/html | 1652 |  |
| 404 | GET | `https://accounts.google.com/accountmanagerPER_ACCOUNT_CONCURRENCY` | text/html | 1652 |  |
| 404 | GET | `https://accounts.google.com/can` | text/html | 1652 |  |
| 404 | GET | `https://accounts.google.com/o/oauth2/authconsider` | text/html | 1652 |  |
| 404 | GET | `https://accounts.google.com/o/oauth2/authmldsa` | text/html | 1652 |  |
| 404 | GET | `https://accounts.google.com/o/oauth2/v2/authGoogle` | text/html | 1652 |  |
| 404 | GET | `https://accounts.google.com/o/oauth2/v2/authMicrosoft` | text/html | 1652 |  |
| 404 | GET | `https://accounts.google.com/o/oauth2/v2/authSOFTWARE` | text/html | 1652 |  |
| 404 | GET | `https://accounts.google.com/o/oauth2/v2/authToken` | text/html | 1652 |  |
| 404 | GET | `https://accounts.google.com/o/oauth2/v2/auth_attention1n5kayakingetReactNativeStartupTimingAnimation1n77qdiffClampImpluralRulesCacheaderLargeTitleShadowVisible1n7guseAnimatedKeyboard` | text/html | 1652 |  |
| 404 | GET | `https://accounts.google.com/o/oauth2/v2/authencoding` | text/html | 1652 |  |
| 404 | GET | `https://accounts.google.com/o/oauth2/v2/authensure` | text/html | 1652 |  |
| 404 | GET | `https://accounts.google.com/o/oauth2/v2/autherro` | text/html | 1652 |  |
| 404 | GET | `https://accounts.google.com/o/oauth2/v2/authnginx` | text/html | 1652 |  |
| 404 | GET | `https://accounts.google.com/o/oauth2/v2/authsrc` | text/html | 1652 |  |
| 404 | GET | `https://accounts.google.com/o/oauth2/v2/authunauthorized_clientinvalid_clientgcp` | text/html | 1652 |  |
| 404 | GET | `https://accounts.google.com/o/oauth2/v2/authunauthorized_clientinvalid_clientgcpvertex` | text/html | 1652 |  |
| 404 | GET | `https://accounts.google.com/o/oauth2/v2client` | text/html | 1652 |  |
| 404 | GET | `https://accounts.google.com/o/oauth2/x` | text/html | 1652 |  |
| 404 | GET | `https://accounts.google.com/o/oauth2/xassertion` | text/html | 1652 |  |
| 404 | GET | `https://accounts.google.com/o/oauth2assertion` | text/html | 1652 |  |
| 404 | GET | `https://accounts.google.com/object` | text/html | 1652 |  |
| 400 | GET | `https://accounts.google.com/restart?continue%3Dhttps%3A%2F%2Faistudio.google.com%2Fapp%2Fgtm.js%26dsh%3DS118289191%3A1795376609138403%26flowEntry%3DServiceLogin%26flowName%3DGlifWebSignIn%26followup%3Dhttps%3A%2F%2Faistudio.google.com%2Fapp%2Fgtm.js%26ltmpl%3Daistudio=` | text/html | 1695 |  |
| 400 | GET | `https://accounts.google.com/restart?continue%3Dhttps%3A%2F%2Faistudio.google.com%2Fgtm.js%26dsh%3DS-1508547457%3A1795376609131717%26flowEntry%3DServiceLogin%26flowName%3DGlifWebSignIn%26followup%3Dhttps%3A%2F%2Faistudio.google.com%2Fgtm.js%26ltmpl%3Daistudio=` | text/html | 1695 |  |
| 400 | GET | `https://accounts.google.com/restart?continue%3Dhttps%3A%2F%2Faistudio.google.com%2Fhost-https-apis.google.com%2Fjs%2Fapi.js%26dsh%3DS-1508547457%3A1795376609133224%26flowEntry%3DServiceLogin%26flowName%3DGlifWebSignIn%26followup%3Dhttps%3A%2F%2Faistudio.google.com%2Fhost-https-apis.google.com%2Fjs%2Fapi.js%26ltmpl%3Daistudio=` | text/html | 1695 |  |
| 400 | GET | `https://accounts.google.com/restart?continue%3Dhttps%3A%2F%2Faistudio.google.com%2Fhost-https-www.gstatic.com%2Fglue%2Fcookienotificationbar%2Fcookienotificationbar.min.js%26dsh%3DS1228695011%3A1795376609561535%26flowEntry%3DServiceLogin%26flowName%3DGlifWebSignIn%26followup%3Dhttps%3A%2F%2Faistudio.google.com%2Fhost-https-www.gstatic.com%2Fglue%2Fcookienotificationbar%2Fcookienotificationbar.min.js%26ltmpl%3Daistudio=` | text/html | 1695 |  |
| 400 | GET | `https://accounts.google.com/restart?continue%3Dhttps%3A%2F%2Fsites.google.com%2Fsite%2Fefeitojs%2Fhome%2Fefeito%2Fefeito.js%26dsh%3DS-1508547457%3A1795376609159801%26flowEntry%3DServiceLogin%26flowName%3DGlifWebSignIn%26followup%3Dhttps%3A%2F%2Fsites.google.com%2Fsite%2Fefeitojs%2Fhome%2Fefeito%2Fefeito.js%26osid%3D1%26service%3Dwise=` | text/html | 1695 |  |
| 400 | GET | `https://accounts.google.com/restart?continue%3Dhttps%3A%2F%2Fsites.google.com%2Fsite%2Funwanted86%2Fjavascript%2Fanimatedrecentpost.js%26dsh%3DS-736926615%3A1795376609175834%26flowEntry%3DServiceLogin%26flowName%3DGlifWebSignIn%26followup%3Dhttps%3A%2F%2Fsites.google.com%2Fsite%2Funwanted86%2Fjavascript%2Fanimatedrecentpost.js%26osid%3D1%26service%3Dwise=` | text/html | 1695 |  |
| 400 | GET | `https://accounts.google.com/restart?continue%3Dhttps%3A%2F%2Fsites.google.com%2Fsite%2Funwanted86%2Fjavascript%2Fbubblecursor.js%26dsh%3DS118289191%3A1795376609153479%26flowEntry%3DServiceLogin%26flowName%3DGlifWebSignIn%26followup%3Dhttps%3A%2F%2Fsites.google.com%2Fsite%2Funwanted86%2Fjavascript%2Fbubblecursor.js%26osid%3D1%26service%3Dwise=` | text/html | 1695 |  |
| 400 | GET | `https://accounts.google.com/restart?continue%3Dhttps%3A%2F%2Fsites.google.com%2Fsite%2Fwordlisting%2Fjumpa%2Fcadang.js%26dsh%3DS118289191%3A1795376609166067%26flowEntry%3DServiceLogin%26flowName%3DGlifWebSignIn%26followup%3Dhttps%3A%2F%2Fsites.google.com%2Fsite%2Fwordlisting%2Fjumpa%2Fcadang.js%26osid%3D1%26service%3Dwise=` | text/html | 1695 |  |
| 404 | GET | `https://accounts.google.com/signincheck` | text/html | 1652 |  |
| 404 | GET | `https://accounts.google.com/v3/signin` | text/html | 1652 |  |
| 404 | GET | `https://accounts.google.com/v3/signin/challeng` | text/html | 1652 |  |
| 400 | GET | `https://accounts.youtube.com/accounts/CheckConnection?pmpo=https%3A%2F%2Faccounts.google.com&v=1180429694` | text/html | 1695 |  |
| 404 | GET | `https://adservice.google.com/ddm/clk/445204615` | text/html | 0 |  |
| 404 | GET | `https://adssettings.google.com/partne=` | text/html | 1652 |  |
| 204 | GET | `https://aistudio.google.com/_/MakerSuite/jserror?script=https%3A%2F%2Faistudio.google.com%2Fwelcome%3Fhl%3Dvi%26_gl%3D1%2A1ne7mz7%2A_ga%2ANTMyMDA4NTg0LjE3MzEyMzM3NTA.%2A_ga_P1DBVKWT6V%2AMTczMTI1MTUzNi4yLjAuMTczMTI1MTUzNi42MC4wLjU0NzIzNzMxMA..&error=Cannot+read+properties+of+undefined+%28reading+%27status%27` | text/html | 0 |  |
| 400 | GET | `https://aistudio.google.com/_/upload` | text/html | 26 |  |
| 204 | GET | `https://aistudio.google.com/app/_/MakerSuite/jserror?script=https%3A%2F%2Faistudio.google.com%2Fapp%2Fwelcome&error=Cannot+read+properties+of+undefined+%28reading+%27status%27` | text/html | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?-7huxQ=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?-AIWEA=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?-Fqumg=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?-MGT3A=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?-Te0mQ=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?044ztQ=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?0CvSVg=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?0aK3hQ=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?0kD-Pg=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?0qSQrw=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?1JbJQA=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?1K0ULw=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?1PL8Xg=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?1uY_4w=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?22OPOA=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?29AxRQ=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?2VvThA=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?2YNtNQ=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?2iP0nw=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?2xmiRQ=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?3Ed_sw=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?3WSA0Q=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?3cedTA=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?3g95tw=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?4995Hg=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?49pKNQ=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?4Bfdjw=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?4GfjXQ=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?4aOcRA=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?4vyHbQ=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?51F2GA=` |  | 0 |  |
| 204 | GET | `https://aistudio.google.com/generate_204?52Nq-w=` |  | 0 |  |
| … | … | _1353 more in JSONL_ | … | … | … |

## 4. DATA FILES (accessible)

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 200 | GET | `https://aistudio.google.com/_/MakerSuite/manifest.json` | application/manifest+json | 1195 |  |
| 200 | GET | `https://aistudio.google.com/api-reference/generate-content.openapi.json` | application/json | 279253 |  |
| 200 | GET | `https://aistudio.google.com/app/_/MakerSuite/manifest.json` | application/manifest+json | 1195 |  |
| 200 | GET | `https://aistudio.google.com/sitemap/index.xml` | text/xml | 210 |  |
| 200 | GET | `https://aistudio.google.com/welcome/_/MakerSuite/manifest.json` | text/html | 68478 |  |
| 200 | GET | `https://developers.google.com/_pwa/developers/manifest.json` | application/json | 1067 |  |
| 200 | GET | `https://dl.google.com/android/maven2/androidx/xr/compose/compose/maven-metadata.xml` | application/xml | 1087 |  |
| 200 | GET | `https://dl.google.com/android/maven2/androidx/xr/compose/material3/material3/maven-metadata.xml` | application/xml | 993 |  |
| 200 | GET | `https://dl.google.com/android/maven2/androidx/xr/runtime/runtime/maven-metadata.xml` | application/xml | 1199 |  |
| 200 | GET | `https://dl.google.com/android/maven2/androidx/xr/scenecore/scenecore/maven-metadata.xml` | application/xml | 1203 |  |
| 200 | GET | `https://dl.google.com/android/maven2/master-index.xml` | application/xml | 10422 |  |
| 200 | GET | `https://dl.google.com/dl/edgedl/chrome/gpu/software_rendering_list.json` | application/json | 11432 |  |
| 200 | GET | `https://toolbar.google.com/buttons/defs/topbuttons.xml` | text/xml | 15229 |  |

## 5. SUBDOMAINS (detailed)

Found **1**, DNS-resolved **1**.

| Host | Resolved | Source |
|---|---|---|
| `www.aistudio.google.com` | yes | passive |

## 6. VIRTUAL HOSTS (real statuses only)

| Host | Status |
|---|---|
| `www.aistudio.google.com` | 301 |
Blocked/noisy vhost checks (403/530/0) are kept in `vhost_blocked.jsonl` (0).

## 7. JS ENDPOINTS (AST, evidence-backed)

_None extracted._

## 8. PARAMETERS

| URL | Params |
|---|---|
| `http://aistudio.google.com/?linkId=13177569` | linkId |
| `http://aistudio.google.com/?linkId=13408349` | linkId |
| `http://aistudio.google.com/?linkId=16076269` | linkId |
| `http://aistudio.google.com/?linkId=9841896` | linkId |
| `http://aistudio.google.com/?model=gemini-2.0-flash-lite` | model |
| `http://aistudio.google.com/?model=gemini-2.5-flash-lite` | model |
| `http://aistudio.google.com/?trk=news_storyline_guest-text` | trk |
| `http://aistudio.google.com/?trk=organization_guest_main-feed-card-text` | trk |
| `http://aistudio.google.com/?trk=public_post-text` | trk |
| `http://aistudio.google.com/?trk=public_post_main-feed-card-text` | trk |
| `http://aistudio.google.com/api-keys?projectFilter=gen-lang-client-0032926246` | projectFilter |
| `http://aistudio.google.com/app/?linkId=9841896` | linkId |
| `http://aistudio.google.com/app/?trk=organization_guest_main-feed-card-text` | trk |
| `http://aistudio.google.com/app/?trk=public_post-text` | trk |
| `http://aistudio.google.com/app/?trk=public_post_main-feed-card-text` | trk |
| `http://aistudio.google.com/app/apikey?hl=` | hl |
| `http://aistudio.google.com/app/apps/bundled/synergy_intro?hl=ja` | hl |
| `http://aistudio.google.com/app/apps/bundled/synergy_intro?hl=pl` | hl |
| `http://aistudio.google.com/app/apps/bundled/synergy_intro?hl=ru` | hl |
| `http://aistudio.google.com/app/apps/bundled/synergy_intro?hl=vi` | hl |
| `http://aistudio.google.com/app/apps/bundled/synergy_intro?hl=zh-cn` | hl |
| `http://aistudio.google.com/app/prompts/new_chat?model=gemini` | model |
| `http://aistudio.google.com/app/prompts/new_chat?model=gemini-2` | model |
| `http://aistudio.google.com/app/prompts/new_chat?model=gemini-2.5-flash%5C` | model |
| `http://aistudio.google.com/app/prompts/new_chat?model=gemini-2.5-flash-image-preview` | model |
| `http://aistudio.google.com/app/prompts/new_chat?model=gemini-2.5-flash-lite-preview-06-17%5C` | model |
| `http://aistudio.google.com/app/prompts/new_chat?model=gemini-2.5-flash-preview-05-20` | model |
| `http://aistudio.google.com/app/prompts/new_chat?model=gemini-2.5-pro%5C` | model |
| `http://aistudio.google.com/app/prompts/new_chat?model=gemini-2.5-pro-exp-03-25` | model |
| `http://aistudio.google.com/app/prompts/new_chat?model=gemini-2.5-pro-exp-03-25%5C%5C%5C` | model |
| `http://aistudio.google.com/app/prompts/new_chat?model=gemini-2.5-pro-preview-05-06` | model |
| `http://aistudio.google.com/app/prompts/new_chat?model=gemini-2.5-pro-preview-06-05` | model |
| `http://aistudio.google.com/app/prompts/new_chat?model=gemini-3-pro-preview%5C` | model |
| `http://aistudio.google.com/app/prompts/new_chat?model=gemma-2-27b-it` | model |
| `http://aistudio.google.com/app/prompts/new_chat?model=gemma-3-12b-it` | model |
| `http://aistudio.google.com/app/prompts/new_chat?model=gemma-3-12b-it%5C` | model |
| `http://aistudio.google.com/app/prompts/new_chat?model=gemma-3-27b-it` | model |
| `http://aistudio.google.com/app/prompts/new_chat?model=gemma-3-27b-it%5C` | model |
| `http://aistudio.google.com/app/prompts/new_chat?model=gemma-3-4b-it` | model |
| `http://aistudio.google.com/app/prompts/new_chat?model=gemma-3-4b-it%5C` | model |
| `http://aistudio.google.com/app/prompts/new_chat?model=gemma-3n-e4b-it` | model |
| `http://aistudio.google.com/app/prompts/new_chat?model=gemma-3n-e4b-it%5C` | model |
| `http://aistudio.google.com/app/prompts?st=` | st |
| `http://aistudio.google.com/app/prompts?state=%7B%22ids%22%3A%5B%2210QmAKKUs4XWjeAz74OvMTbqxq0-Y1KN7%22%5D` | state |
| `http://aistudio.google.com/app/prompts?state=%7B%22ids%22%3A%5B%2212PVpaDfXQx0Pgombr_s8oP-ALKT8Lgko%22%5D` | state |
| `http://aistudio.google.com/app/prompts?state=%7B%22ids%22%3A%5B%2218qzkqPvnFK78Jr5Gr2Ljs0-7EuDUm5Q_%22%5D` | state |
| `http://aistudio.google.com/app/prompts?state=%7B%22ids%22%3A%5B%221AN7aSU4dUmGxN0` | state |
| `http://aistudio.google.com/app/prompts?state=%7B%22ids%22%3A%5B%221AN7aSU4dUmGxN0HXyhy9sCAOkBXEUO-c%22%5D` | state |
| `http://aistudio.google.com/app/prompts?state=%7B%22ids%22%3A%5B%221B1rcQ7Rfk2X9jO6zAsEKTuQCKbJl0V57%22%5D` | state |
| `http://aistudio.google.com/app/prompts?state=%7B%22ids%22%3A%5B%221GE7SJaOlZDOW1TmJFth0bihVRcnBhdC0%22%5D` | state |
| `http://aistudio.google.com/app/prompts?state=%7B%22ids%22%3A%5B%221K8Zb4DgqSB67Bv3yaZOiee1cJzqFVH-o%22%5D` | state |
| `http://aistudio.google.com/app/prompts?state=%7B%22ids%22%3A%5B%221O5rgVUqd1H7vEDVMnq07zx349SUe3Aif%22%5D` | state |
| `http://aistudio.google.com/app/prompts?state=%7B%22ids%22%3A%5B%221P-NdOBfi32DgvlLbFQNjWDh6bRpU8Cox%22%5D` | state |
| `http://aistudio.google.com/app/prompts?state=%7B%22ids%22%3A%5B%221TSAM5WahQl9MABND5y_w0DbdsFfPMlJG%22%5D` | state |
| `http://aistudio.google.com/app/prompts?state=%7B%22ids%22%3A%5B%221XSFJhnCXqzPf6KaEjRN2fJqR315I9OZT%22%5D` | state |
| `http://aistudio.google.com/app/prompts?state=%7B%22ids%22%3A%5B%221Z0RwQJ50xKbiDJsdQ8xUO6fyswjs7WWR%22%5D%2C%22action%22%3A%22open%22%2C%22userId%22%3A%22118197120810729680720%22%2C%22resourceKeys%22%3A%7B%7D%7D&usp=drive_link` | state, usp |
| `http://aistudio.google.com/app/prompts?state=%7B%22ids%22%3A%5B%221mWszGUQlXfBtatYx` | state |
| `http://aistudio.google.com/app/prompts?state=%7B%22ids%22%3A%5B%221mWszGUQlXfBtatYx__ahdghv-8IySovA%22%5D` | state |
| `http://aistudio.google.com/app/prompts?state=%7B%22ids%22%3A%5B%221xTCH4fFvMDNqWFme3KZgWVkyYd5eW5pO%22%5D` | state |
| `http://aistudio.google.com/app/usage?tab=rate-limit&timeRange=last-7-days` | tab, timeRange |

## 9. SECRET CANDIDATES

17 candidate(s) in `secrets.jsonl`. Verify manually.

## 10. TOOL RUN STATUS (no silent skips)

| Tool | Result | Detail |
|---|---|---|
| `anastasis` | exit 254 | no output produced — see logs/ |
| `dnsx` | OK | completed |
| `ffuf` | OK | off by choice — wordlist prepared |
| `gau` | OK | completed |
| `gospider` | OK | completed |
| `httpx` | OK | completed |
| `js-download` | OK | 12 chunks saved over 3 round(s) |
| `jscope` | OK | completed |
| `jsluice` | OK | 12 files parsed |
| `katana` | exit 124 | see logs/ |
| `methods` | OK | 1120 method responses |
| `subfinder` | OK | completed |
| `trufflehog` | OK | completed |
| `uncover` | OK | no API key configured — no external data |
| `urlfinder` | OK | completed |
| `uro` | OK | completed |
| `vhost` | OK | 1 real of 1 tested |
| `x8` | OK | parameter scan complete |

## 11. INTENTIONALLY NOT RUN

- **ffuf path brute** — off by default; `wordlist.txt` is ready. Set `enable_brute: true` later.
- **kiterunner** — off by default alongside ffuf.

## 12. OUTPUT FILES

| File | Meaning |
|---|---|
| [`all_routes.jsonl`](all_routes.jsonl) | every route, unfiltered (2,796,185 B) |
| [`accessible_200.jsonl`](accessible_200.jsonl) | HTTP 200 wins (3,600,494 B) |
| [`exists_blocked.jsonl`](exists_blocked.jsonl) | exists but blocked (4,769,850 B) |
| [`other_status.jsonl`](other_status.jsonl) | all other statuses (1,321,061 B) |
| [`data_files.jsonl`](data_files.jsonl) | JSON/CSV/XML among 200s (11,582 B) |
| [`params.jsonl`](params.jsonl) | parameters (939,762 B) |
| [`subdomains.jsonl`](subdomains.jsonl) | subdomains + resolution (85 B) |
| [`third_party_routes.jsonl`](third_party_routes.jsonl) | third-party URLs — kept, not deleted (1,397,295 B) |
| [`method_responses.jsonl`](method_responses.jsonl) | all method-probe responses — kept (172,994 B) |
| [`vhost_real.jsonl`](vhost_real.jsonl) | non-blocked virtual hosts (56 B) |
| [`vhost_blocked.jsonl`](vhost_blocked.jsonl) | blocked vhost checks — kept (0 B) |
| [`js_endpoints.jsonl`](js_endpoints.jsonl) | AST endpoints (0 B) |
| [`vhost.jsonl`](vhost.jsonl) | all vhost checks (56 B) |
| [`jsluice.jsonl`](jsluice.jsonl) | JS-derived URLs (75,208 B) |
| [`gospider.txt`](gospider.txt) | second crawler URLs (9,806 B) |
| [`jscope.txt`](jscope.txt) | evidence-ranked JS analysis (4,298 B) |
| [`secrets.jsonl`](secrets.jsonl) | secret candidates (12,375 B) |
| [`wordlist.txt`](wordlist.txt) | target-specific fuzz list (246,335 B) |
| [`params.txt`](params.txt) | parameter wordlist (4,064 B) |
| [`js_urls.txt`](js_urls.txt) | JS chunk URLs (729 B) |
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