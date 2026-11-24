# Hunt Report — https://flowith.io

Generated: 2026-11-24T20:07:13Z &nbsp;|&nbsp; Duration: 67m 28s

> **Nothing is filtered during collection. This report is only a grouping.**

## Summary

| What | Count | Meaning |
|---|---:|---|
| Routes collected | 9837 | Every URL found, nothing removed |
| Distinct routes verified | 3229 | One row per URL (method probes excluded) |
| HTTP responses | 4429 | Includes method probes — kept in `method_responses.jsonl` |
| **Accessible (200)** | **1042** | Confirmed live — the wins |
| Exists but different status | 874 | 301/302/401/403/405 — real route, blocked |
| Other responses | 1313 | 404/500/etc — kept, not discarded |
| Subdomains (resolved) | 59 | DNS-verified |
| Virtual hosts (real) | 63 | Cloudflare 403/530/0 excluded |
| Parameters | 5348 | URLs with query params |
| JS endpoints (AST) | 417 | anastasis evidence-backed |
| First-party URLs | 9163 | flowith.io and subdomains |
| Third-party URLs | 674 | kept in `third_party_routes.jsonl` |
| Method responses | 1400 | kept in `method_responses.jsonl` |
| Blocked vhost checks | 0 | kept in `vhost_blocked.jsonl` |
| Secret candidates | 0 | verify manually |

> Collection keeps third-party URLs by design (674). See `third_party_routes.jsonl`. Method-probe responses are in `method_responses.jsonl`.

## 0. TOP ROUTE PATTERNS (IDs collapsed)

| Pattern | Count |
|---|---:|
| `/report/v4` | 592 |
| `/tools/{id}` | 406 |
| `/tools/{id}/quality=75/static-site/v/{id}/home-v3/fox-snow.webp` | 164 |
| `/tools/{id}/quality=75/static-site/v/{id}/home-v3/k-board6.webp` | 164 |
| `/tools/{id}/quality=75/static-site/v/{id}/home-v3/img-cmp-gpt.webp` | 164 |
| `/tools/{id}/quality=75/static-site/v/{id}/home-v3/img-room.webp` | 164 |
| `/tools/{id}/quality=75/static-site/v/{id}/home-v3/k-board4.webp` | 164 |
| `/tools/{id}/quality=75/static-site/v/{id}/home-v3/img-product.webp` | 164 |
| `/tools/{id}/quality=75/static-site/v/{id}/home-v3/img-pavilion.webp` | 164 |
| `/tools/{id}/quality=75/static-site/v/{id}/home-v3/img-poster.webp` | 164 |
| `/tools/{id}/quality=75/static-site/v/{id}/home-v3/img-cmp-seedream.webp` | 164 |
| `/tools/{id}/quality=75/static-site/v/{id}/home-v3/k-board2.webp` | 164 |
| `/tools/{id}/width=1024` | 164 |
| `/tools/{id}/width=384` | 164 |
| `/tools/{id}/width=768` | 164 |
| `/blog/{id}` | 163 |
| `/` | 89 |
| `/blank` | 42 |
| `/blog/{id}/width=320` | 16 |
| `/blog/{id}/width=640` | 16 |
| `/de/tools/{id}` | 14 |
| `/es/tools/{id}` | 14 |
| `/fr/tools/{id}` | 14 |
| `/id/tools/{id}` | 14 |
| `/ja/tools/{id}` | 14 |
| `/ko/tools/{id}` | 14 |
| `/pt/tools/{id}` | 14 |
| `/ru/tools/{id}` | 14 |
| `/th/tools/{id}` | 14 |
| `/tr/tools/{id}` | 14 |
| `/vi/tools/{id}` | 14 |
| `/zh-tw/tools/{id}` | 14 |
| `/zh/tools/{id}` | 14 |
| `/blog/{id}/quality=75/static-site/v/{id}/blog/creator-tests/code-agents-mobile-comparison.webp` | 10 |
| `/ai-models/{id}` | 9 |
| `/help/articles/{id}` | 9 |
| `/blog/{id}/quality=75/static-site/v/{id}/blog/cat-garden/cover.webp` | 8 |
| `/blog/{id}/width=1020` | 7 |
| `/blog/{id}/width=340` | 7 |
| `/blog/{id}/width=680` | 7 |

## 1. SUCCESS — HTTP 200

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 200 | GET | `https://admin.flowith.io` | text/html | 1171 |  |
| 200 | GET | `https://agent.flowith.io` | text/html | 4762 |  |
| 200 | GET | `https://ai-proxy.flowith.io` | text/plain | 965 |  |
| 200 | GET | `https://api.dicebear.com/9.x/glass/svg?seed=EXPR` | image/svg+xml | 2317 |  |
| 200 | GET | `https://api.flowith.io` | text/plain | 97 |  |
| 200 | GET | `https://api.liblib.tv/api/community/project/template/detail?projectTemplateUuid=EXPR` | application/json | 141 |  |
| 200 | GET | `https://arvin.chat` | text/html | 3636 |  |
| 200 | GET | `https://bedrock.flowith.io` | text/plain | 13 |  |
| 200 | GET | `https://beszel.flowith.io` | text/html | 1462 |  |
| 200 | GET | `https://brandnew.flowith.io` | text/html | 15135 |  |
| 200 | GET | `https://cakegrowth.cn` | text/html | 103291 |  |
| 200 | GET | `https://cakegrowth.cn/static/cg.min.js` | application/javascript | 15473 |  |
| 200 | GET | `https://cakegrowth.cn/static/crypto-js.min.js` | application/javascript | 60819 |  |
| 200 | GET | `https://cdn.adjust.com/adjust-latest.min.js` | application/javascript | 52677 |  |
| 200 | GET | `https://cdn.jsdelivr.net/gh/gitbrent/PptxGenJS@3.12.0/dist/pptxgen.bundle.js` | application/javascript | 477529 |  |
| 200 | GET | `https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js` | application/javascript | 364463 |  |
| 200 | GET | `https://cdnjs.cloudflare.com/ajax/libs/pdfobject/2.1.1/pdfobject.min.js` | application/javascript | 5541 |  |
| 200 | GET | `https://challenges.cloudflare-cn.com` | text/html | 5397 |  |
| 200 | GET | `https://challenges.cloudflare.com` | text/html | 5397 |  |
| 200 | GET | `https://challenges.fed.cloudflare.com` | text/html | 5397 |  |
| 200 | GET | `https://chromewebstore.google.com` | text/html | 1811955 |  |
| 200 | GET | `https://classic.flowith.io` | text/html | 16549 |  |
| 200 | GET | `https://composer.flowith.io` | text/html | 1119 |  |
| 200 | GET | `https://count-tokens.flowith.io` | text/plain | 11 |  |
| 200 | GET | `https://d1.flowith.io` | text/plain | 4 |  |
| 200 | GET | `https://dev-edge.flowith.io` | text/plain | 97 |  |
| 200 | GET | `https://dev-events.flowith.io` | application/json | 126 |  |
| 200 | GET | `https://dev-test.flowith.io` | text/html | 8735 |  |
| 200 | GET | `https://discord.com/invite/g95B77xbpD` | text/html | 28954 |  |
| 200 | GET | `https://doc-parser.flowith.io` | application/json | 27 |  |
| 200 | GET | `https://docs.n8n.io` | text/html | 486035 |  |
| 200 | GET | `https://docs.openclaw.ai/install` | text/html | 290723 |  |
| 200 | GET | `https://docs.openclaw.ai/start/onboarding-overview` | text/html | 258335 |  |
| 200 | GET | `https://docs.x.ai/build/features/skills-plugins-marketplaces` | text/html | 231877 |  |
| 200 | GET | `https://docs.x.ai/build/overview` | text/html | 264835 |  |
| 200 | GET | `https://edge.flowith.io` | text/plain | 97 |  |
| 200 | GET | `https://editor.flowith.io` | text/html | 2316 |  |
| 200 | GET | `https://firefly.adobe.com` | text/html | 21136 |  |
| 200 | GET | `https://flowith.io` | text/html | 472570 |  |
| 200 | GET | `https://flowith.io/${w` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/([^` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/*` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/7.x/lorelei/svg?seed=%24%7Be.author_id` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/9.x/glass/svg?seed=` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/?key=%24%7Bt.value` | text/html | 472570 |  |
| 200 | GET | `https://flowith.io/?preset=%24%7Be` | text/html | 472570 |  |
| 200 | GET | `https://flowith.io/ASCII85Decode` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/ASCII85Encode` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/ASCIIHexDecode` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/ASCIIHexEncode` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/Annot` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/Annots` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/ArtBox` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/BleedBox` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/Border` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/Btn` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/CIDSystemInfo` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/CIDToGIDMap` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/Ch` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/ColorSpace` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/Contents` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/Coords` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/CreationDate` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/CropBox` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/DW` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/DescendantFonts` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/Extend` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/F1` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/Filter` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/FirstChar` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/Flags` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/FlateDecode` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/FlateEncode` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/Form` | text/html | 75866 |  |
| 200 | GET | `https://flowith.io/I` | text/html | 75866 |  |
| … | … | _967 more in JSONL_ | … | … | … |

## 2. EXISTS BUT DIFFERENT STATUS (301/302/401/403/405)

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 405 | GET | `https://a.nel.cloudflare.com/report/v4?s=qdYPHfu5NMXNKGWI%2BQJXubJJaKxbcpDfa%2BOLz%2F3YrE7v9TayxvC%2B81wP%2BQY2xOhcM%2FCZQuBjAfIHLuujd3IL02093xj3hT418WJJYSeDRgVLcFOM5uuDKswEtmKui0p50LmHZjVOaW%2BjDeeX52XqN6lo` |  | 0 |  |
| 301 | GET | `https://adobe.com/products/firefly.html` |  | 0 |  |
| 403 | GET | `https://aff.flowith.io` | text/plain | 17 |  |
| 302 | GET | `https://beta.flowith.io` |  | 0 |  |
| 301 | GET | `https://blackforestlabs.ai` | text/plain | 15 |  |
| 403 | GET | `https://challenges-staging.cloudflare.com` | text/plain | 1 |  |
| 302 | GET | `https://challenges.cloudflare.com/turnstile/v0/api.js?onload=flowithTurnstileOnLoad&render=explicit` |  | 0 |  |
| 301 | GET | `https://chromewebstore.google.com/detail/flowith-web-clipper/jkcpodicdboheakkkoblnflccfihcblb` | application/binary | 0 |  |
| 301 | GET | `https://deepl.com` | text/html | 167 |  |
| 301 | GET | `https://deepl.com/pro` | text/html | 167 |  |
| 301 | GET | `https://deepl.com/write` | text/html | 167 |  |
| 307 | GET | `https://doc.flowith.io` | text/plain | 15 |  |
| 301 | GET | `https://docs.anthropic.com/en/docs/agents-and-tools/computer-use` | text/html | 167 |  |
| 308 | GET | `https://docs.browserbase.com` | text/plain | 0 |  |
| 301 | GET | `https://docs.flowith.io` | text/html | 290 |  |
| 308 | GET | `https://docs.perplexity.ai` | text/plain | 0 |  |
| 308 | GET | `https://docs.perplexity.ai/getting-started/pricing` | text/plain | 0 |  |
| 307 | GET | `https://flowith.io/affiliate-program` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/claude-fable-5` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/claude-fable-5-1` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/claude-mythos-5` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/claude-mythos-5-1` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/claude-opus-5` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/claude-sonnet-5` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/deepseek` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/deepseek-r1` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/deepseek-v3.2` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/deepseek-v4` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/diffusiongemma` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/flux-2` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/gemini-3-1` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/gemini-3-6-flash` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/gemini-3-7-flash` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/gemini-omni-flash` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/gemini-robotics-er-2` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/gemma-4` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/gemma-4-12b` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/gpt-5-6` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/gpt-5.2` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/gpt-image-1.5` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/gpt-image-2` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/gpt-image-2-6` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/gpt-live-1` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/grok-4` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/grok-4-5` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/grok-4-6` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/kimi-k2.5` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/kling-3-0` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/kling-4-0` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/leanstral-1-5` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/lfm2-5-2-6b` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/lyria-3-5` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/macaron-v1-tall` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/macaron-v1-venti` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/meta-muse-image` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/meta-muse-video` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/midjourney` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/nano-banana-2-1` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/nano-banana-free-online` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/nano-banana-pro` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/qwen-image-3-0` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/recraft-v3` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/reve-ai` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/robostral-navigate` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/runway-aleph-2` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/seedance-2-0` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/seedance-2-5` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/seedream-4.5` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/seedream-5-0` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/seedream-5-5` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/sora-2` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/veo-3.1` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/wan-2.5-image` |  | 0 |  |
| 307 | GET | `https://flowith.io/ai-models/wan-2.6-video` |  | 0 |  |
| … | … | _799 more in JSONL_ | … | … | … |

## 3. OTHER RESPONSES — kept, never discarded

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 404 | GET | `https://admin-agent.flowith.io` | text/plain | 13 |  |
| 404 | GET | `https://api.cakegrowth.cn/v1` | application/json | 45 |  |
| 404 | GET | `https://cg-api-cn-test.ai-rich.cn/v1` | text/html | 153 |  |
| 404 | GET | `https://cg-www-cn-test.ai-rich.cn` | text/html | 153 |  |
| 404 | GET | `https://content.flo.host/download/EXPR` | application/json | 42 |  |
| 404 | GET | `https://content.flo.host/download/{EXPR` | application/json | 42 |  |
| 525 | GET | `https://dev.flowith.io` | text/plain | 16 |  |
| 404 | GET | `https://email.email.flowith.io` |  | 0 |  |
| 404 | GET | `https://flowith.io/_astro/${e.url}` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/claude-fable-5-1/width=1024` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/claude-fable-5-1/width=384` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/claude-fable-5-1/width=768` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/claude-fable-5/width=1024` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/claude-fable-5/width=384` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/claude-fable-5/width=768` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/claude-mythos-5-1/width=1024` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/claude-mythos-5-1/width=384` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/claude-mythos-5-1/width=768` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/claude-opus-5/width=1024` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/claude-opus-5/width=384` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/claude-opus-5/width=768` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/deepseek-r1/width=1024` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/deepseek-r1/width=384` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/deepseek-r1/width=768` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/deepseek/width=1024` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/deepseek/width=384` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/deepseek/width=768` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/gemini-3-1/width=1024` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/gemini-3-1/width=384` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/gemini-3-1/width=768` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/gemini-3-6-flash/width=1024` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/gemini-3-6-flash/width=384` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/gemini-3-6-flash/width=768` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/gemini-omni-flash/width=1024` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/gemini-omni-flash/width=384` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/gemini-omni-flash/width=768` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/gemma-4/width=1024` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/gemma-4/width=384` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/gemma-4/width=768` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/gpt-5.2/width=1024` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/gpt-5.2/width=384` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/gpt-5.2/width=768` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/gpt-image-2-6/width=1024` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/gpt-image-2-6/width=384` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/gpt-image-2-6/width=768` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/gpt-image-2/width=1024` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/gpt-image-2/width=1200` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/gpt-image-2/width=384` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/gpt-image-2/width=768` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/kling-4-0/width=1024` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/kling-4-0/width=384` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/kling-4-0/width=768` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/macaron-v1-venti/width=1024` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/macaron-v1-venti/width=384` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/macaron-v1-venti/width=768` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/midjourney/width=1024` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/midjourney/width=1200` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/midjourney/width=384` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/midjourney/width=768` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/nano-banana-2-1/width=1024` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/nano-banana-2-1/width=384` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/nano-banana-2-1/width=768` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/nano-banana-pro/width=1024` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/nano-banana-pro/width=1200` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/nano-banana-pro/width=384` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/nano-banana-pro/width=768` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/qwen-image-3-0/width=1024` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/qwen-image-3-0/width=384` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/qwen-image-3-0/width=768` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/recraft-v3/width=1024` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/recraft-v3/width=1200` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/recraft-v3/width=384` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/recraft-v3/width=768` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/reve-ai/width=1024` |  | 0 |  |
| 404 | GET | `https://flowith.io/ai-models/reve-ai/width=1200` |  | 0 |  |
| … | … | _1238 more in JSONL_ | … | … | … |

## 4. DATA FILES (accessible)

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 200 | GET | `https://api.dicebear.com/9.x/glass/svg?seed=EXPR` | image/svg+xml | 2317 |  |
| 200 | GET | `https://api.liblib.tv/api/community/project/template/detail?projectTemplateUuid=EXPR` | application/json | 141 |  |
| 200 | GET | `https://dev-events.flowith.io` | application/json | 126 |  |
| 200 | GET | `https://doc-parser.flowith.io` | application/json | 27 |  |
| 200 | GET | `https://flowith.io/deploy-meta.json?t=EXPR` | application/json | 257 |  |
| 200 | GET | `https://flowith.io/sitemap.xml` | application/xml | 104007 |  |
| 200 | GET | `https://ladders.flowith.io` | application/json | 43 |  |
| 200 | GET | `https://r2.flowith.io` | application/json | 157 |  |
| 200 | GET | `https://s2s.adjust.com/event` | application/json | 2 |  |

## 5. SUBDOMAINS (detailed)

Found **101**, DNS-resolved **59**.

| Host | Resolved | Source |
|---|---|---|
| `ably.flowith.io` | no | passive |
| `admin-agent.flowith.io` | yes | passive |
| `admin.flowith.io` | yes | passive |
| `adming.flowith.io` | no | passive |
| `aff.flowith.io` | yes | passive |
| `agent.flowith.io` | yes | passive |
| `ai-proxy.flowith.io` | yes | passive |
| `api-proxy.flowith.io` | no | passive |
| `api.flowith.io` | yes | passive |
| `bedrock.flowith.io` | yes | passive |
| `beszel.flowith.io` | yes | passive |
| `beta.flowith.io` | yes | passive |
| `brandnew.flowith.io` | yes | passive |
| `classic.flowith.io` | yes | passive |
| `composer.flowith.io` | yes | passive |
| `count-tokens.flowith.io` | yes | passive |
| `d1.flowith.io` | yes | passive |
| `dev-edge.flowith.io` | yes | passive |
| `dev-events.flowith.io` | yes | passive |
| `dev-test.flowith.io` | yes | passive |
| `dev.flowith.io` | yes | passive |
| `doc-parser.flowith.io` | yes | passive |
| `doc.flowith.io` | yes | passive |
| `docs.flowith.io` | yes | passive |
| `edge.flowith.io` | yes | passive |
| `editor.flowith.io` | yes | passive |
| `email.email.flowith.io` | yes | passive |
| `gpt-lc-api.flowith.io` | yes | passive |
| `gpt-lc-apic.flowith.io` | no | passive |
| `help.flowith.io` | yes | passive |
| `image-size.flowith.io` | yes | passive |
| `kuma.flowith.io` | yes | passive |
| `kv.flowith.io` | yes | passive |
| `ladders.flowith.io` | yes | passive |
| `layer-editor.flowith.io` | yes | passive |
| `libsql.flowith.io` | yes | passive |
| `link.email.flowith.io` | yes | passive |
| `mail-templates.flowith.io` | yes | passive |
| `mkt.flowith.io` | yes | passive |
| `next-gen.flowith.io` | yes | passive |
| `nsfw.flowith.io` | yes | passive |
| `og.flowith.io` | yes | passive |
| `pb-01.flowith.io` | yes | passive |
| `postgres-connector.flowith.io` | yes | passive |
| `pubkey-verify.flowith.io` | yes | passive |
| `pubsub-01.flowith.io` | yes | passive |
| `pubsub.flowith.io` | yes | passive |
| `r2.flowith.io` | yes | passive |
| `rt.flowith.io` | yes | passive |
| `secret-store.flowith.io` | yes | passive |
| `service.flowith.io` | yes | passive |
| `squad-api.flowith.io` | yes | passive |
| `ss.flowith.io` | yes | passive |
| `static-content.flowith.io` | yes | passive |
| `status.flowith.io` | yes | passive |
| `supabase.flowith.io` | no | passive |
| `try.flowith.io` | yes | passive |
| `u.flowith.io` | yes | passive |
| `umami.flowith.io` | yes | passive |
| `v2.flowith.io` | yes | passive |
| `v3.flowith.io` | yes | passive |
| `vibe.flowith.io` | yes | passive |
| `video-process.flowith.io` | yes | passive |
| `web-inspector.flowith.io` | no | passive |
| `www.admin.flowith.io` | no | passive |
| `www.aff.flowith.io` | no | passive |
| `www.ai-proxy.flowith.io` | no | passive |
| `www.bedrock.flowith.io` | no | passive |
| `www.beszel.flowith.io` | no | passive |
| `www.beta.flowith.io` | no | passive |
| `www.composer.flowith.io` | no | passive |
| `www.count-tokens.flowith.io` | no | passive |
| `www.d1.flowith.io` | no | passive |
| `www.dev.flowith.io` | no | passive |
| `www.doc-parser.flowith.io` | no | passive |
| `www.doc.flowith.io` | no | passive |
| `www.docs.flowith.io` | no | passive |
| `www.edge.flowith.io` | no | passive |
| `www.flowith.io` | yes | passive |
| `www.gpt-lc-api.flowith.io` | no | passive |
| `www.image-size.flowith.io` | no | passive |
| `www.kuma.flowith.io` | no | passive |
| `www.kv.flowith.io` | no | passive |
| `www.libsql.flowith.io` | no | passive |
| `www.mail-templates.flowith.io` | no | passive |
| `www.mkt.flowith.io` | no | passive |
| `www.og.flowith.io` | no | passive |
| `www.pb-01.flowith.io` | no | passive |
| `www.pubsub.flowith.io` | no | passive |
| `www.r2.flowith.io` | no | passive |
| `www.rt.flowith.io` | no | passive |
| `www.secret-store.flowith.io` | no | passive |
| `www.service.flowith.io` | no | passive |
| `www.squad-api.flowith.io` | no | passive |
| `www.ss.flowith.io` | no | passive |
| `www.static-content.flowith.io` | no | passive |
| `www.supabase.flowith.io` | no | passive |
| `www.try.flowith.io` | no | passive |
| `www.u.flowith.io` | no | passive |
| `www.umami.flowith.io` | no | passive |
| `www.video-process.flowith.io` | no | passive |

## 6. VIRTUAL HOSTS (real statuses only)

| Host | Status |
|---|---|
| `ai-proxy.flowith.io` | 200 |
| `classic.flowith.io` | 200 |
| `admin-agent.flowith.io` | 200 |
| `api.flowith.io` | 200 |
| `beszel.flowith.io` | 200 |
| `dev-events.flowith.io` | 200 |
| `dev.flowith.io` | 200 |
| `count-tokens.flowith.io` | 200 |
| `beta.flowith.io` | 200 |
| `agent.flowith.io` | 200 |
| `dev-edge.flowith.io` | 200 |
| `adming.flowith.io` | 200 |
| `api-proxy.flowith.io` | 200 |
| `aff.flowith.io` | 200 |
| `composer.flowith.io` | 200 |
| `ably.flowith.io` | 200 |
| `brandnew.flowith.io` | 200 |
| `bedrock.flowith.io` | 200 |
| `admin.flowith.io` | 200 |
| `d1.flowith.io` | 200 |
| `dev-test.flowith.io` | 200 |
| `doc.flowith.io` | 200 |
| `edge.flowith.io` | 200 |
| `doc-parser.flowith.io` | 200 |
| `docs.flowith.io` | 200 |
| `editor.flowith.io` | 200 |
| `ladders.flowith.io` | 200 |
| `mail-templates.flowith.io` | 200 |
| `gpt-lc-api.flowith.io` | 200 |
| `kv.flowith.io` | 200 |
| `help.flowith.io` | 200 |
| `layer-editor.flowith.io` | 200 |
| `image-size.flowith.io` | 200 |
| `libsql.flowith.io` | 200 |
| `og.flowith.io` | 200 |
| `kuma.flowith.io` | 200 |
| `nsfw.flowith.io` | 200 |
| `mkt.flowith.io` | 200 |
| `next-gen.flowith.io` | 200 |
| `gpt-lc-apic.flowith.io` | 200 |
| `postgres-connector.flowith.io` | 200 |
| `pb-01.flowith.io` | 200 |
| `pubkey-verify.flowith.io` | 200 |
| `pubsub-01.flowith.io` | 200 |
| `r2.flowith.io` | 200 |
| `pubsub.flowith.io` | 200 |
| `service.flowith.io` | 200 |
| `rt.flowith.io` | 200 |
| `u.flowith.io` | 200 |
| `secret-store.flowith.io` | 200 |
| `ss.flowith.io` | 200 |
| `status.flowith.io` | 200 |
| `supabase.flowith.io` | 200 |
| `umami.flowith.io` | 200 |
| `try.flowith.io` | 200 |
| `v2.flowith.io` | 200 |
| `squad-api.flowith.io` | 200 |
| `static-content.flowith.io` | 200 |
| `v3.flowith.io` | 200 |
| `vibe.flowith.io` | 200 |
| `web-inspector.flowith.io` | 200 |
| `video-process.flowith.io` | 200 |
| `www.flowith.io` | 301 |
Blocked/noisy vhost checks (403/530/0) are kept in `vhost_blocked.jsonl` (0).

## 7. JS ENDPOINTS (AST, evidence-backed)

| Method | Path | Confidence |
|---|---|---|
| UNKNOWN | `/knowledge-garden` | 0.7 |
| UNKNOWN | `/apps/adult-character?entry=adult-tools` | 0.7 |
| UNKNOWN | `/apps/adult-comic?entry=adult-tools` | 0.7 |
| UNKNOWN | `/apps/adult-makeover?entry=adult-tools` | 0.7 |
| UNKNOWN | `/apps/adult-story-studio?entry=adult-tools` | 0.7 |
| UNKNOWN | `/apps/adult-video-continuation?entry=adult-tools` | 0.7 |
| UNKNOWN | `/apps/adult-video?entry=adult-tools` | 0.7 |
| UNKNOWN | `/apps/nsfw-image-editor?entry=adult-tools` | 0.7 |
| UNKNOWN | `/apps/nsfw-video-editor?entry=adult-tools` | 0.7 |
| UNKNOWN | `/tools/adult-ai-video-generator` | 0.7 |
| UNKNOWN | `/tools/adult-character-generator` | 0.7 |
| UNKNOWN | `/tools/adult-comic-generator` | 0.7 |
| UNKNOWN | `/tools/adult-makeover` | 0.7 |
| UNKNOWN | `/tools/adult-story-prompt-generator` | 0.7 |
| UNKNOWN | `/tools/adult-video-continuation` | 0.7 |
| UNKNOWN | `/tools/nsfw-ai-image-editor` | 0.7 |
| UNKNOWN | `/tools/nsfw-ai-video-editor` | 0.7 |
| UNKNOWN | `/conv/${e}` | 0.6 |
| UNKNOWN | `/api/knowledge-garden/${W}` | 0.6 |
| UNKNOWN | `/api/knowledge-garden/${W}/payment` | 0.6 |
| UNKNOWN | `/7.x/lorelei/svg?seed=${e.author_id}` | 0.75 |
| UNKNOWN | `/ajax/libs/emojione/2.2.7/assets` | 0.7 |
| UNKNOWN | `/ajax/libs/twemoji/12.0.4/2` | 0.7 |
| UNKNOWN | `/cdn.jsdelivr.net/emojione/assets/4.0` | 0.7 |
| UNKNOWN | `/cdnjs.cloudflare.com/ajax/libs/emojione/2.2.7/assets` | 0.7 |
| UNKNOWN | `/cdnjs.cloudflare.com/ajax/libs/twemoji/12.0.4/2` | 0.7 |
| UNKNOWN | `/emojione/assets/4.0` | 0.7 |
| UNKNOWN | `/api-dashboard/api-keys` | 0.7 |
| UNKNOWN | `/conv-guide` | 0.7 |
| UNKNOWN | `/9.x/glass/svg?seed=` | 0.7 |
| UNKNOWN | `/repo-detail/${e.id}` | 0.6 |
| UNKNOWN | `/npm/emoji-datasource-apple/img/apple/64` | 0.7 |
| UNKNOWN | `/npm/emoji-datasource-facebook/img/facebook/64` | 0.7 |
| UNKNOWN | `/npm/emoji-datasource-google/img/google/64` | 0.7 |
| UNKNOWN | `/npm/emoji-datasource-twitter/img/twitter/64` | 0.7 |
| GET | `/image_edit/submit` | 0.5 |
| GET | `/video_edit/lipsync/submit` | 0.5 |
| GET | `/video_edit/motion-transfer/submit` | 0.5 |
| GET | `/video_edit/remove-background/submit` | 0.5 |
| GET | `/video_edit/submit` | 0.5 |
| UNKNOWN | `/M ${dP(e)} L ${dP(t)}` | 0.6 |
| UNKNOWN | `/?key=${t.value}` | 0.6 |
| UNKNOWN | `/embed?url={url}` | 0.8 |
| UNKNOWN | `/video-studio/model-logos/v1` | 0.7 |
| UNKNOWN | `/creator-elements/official` | 0.7 |
| GET | `/blank?{EXPR}` | 0.6399999999999999 |
| UNKNOWN | `/user/bug-report` | 0.7 |
| UNKNOWN | `/user/error-report` | 0.7 |
| UNKNOWN | `/miniapps/nsfw/access` | 0.7 |
| UNKNOWN | `/apps/${t}` | 0.6 |
| UNKNOWN | `/apps/${e.targetAppSlug}` | 0.6 |
| UNKNOWN | `/apps/${i.targetAppSlug}` | 0.6 |
| UNKNOWN | `/conv/${t.conversationId}` | 0.75 |
| UNKNOWN | `/conv/${t}` | 0.6 |
| UNKNOWN | `/miniapps/nsfw/assets` | 0.7 |
| UNKNOWN | `/home` | 0.7 |
| GET | `/ASCII85Decode` | 0.5 |
| GET | `/ASCII85Encode` | 0.5 |
| GET | `/ASCIIHexDecode` | 0.5 |
| GET | `/ASCIIHexEncode` | 0.5 |
| GET | `/FlateDecode` | 0.5 |
| GET | `/Annot` | 0.5 |
| GET | `/Btn` | 0.5 |
| GET | `/Ch` | 0.5 |
| GET | `/CIDSystemInfo` | 0.5 |
| GET | `/FlateEncode` | 0.5 |
| GET | `/Form` | 0.5 |
| GET | `/Image` | 0.5 |
| GET | `/Outlines` | 0.5 |
| GET | `/Pattern` | 0.5 |
| GET | `/Sig` | 0.5 |
| GET | `/Tx` | 0.5 |
| GET | `/Widget` | 0.5 |
| GET | `/XObject` | 0.5 |
| UNKNOWN | `/Annots [` | 0.7 |
| UNKNOWN | `/ArtBox [` | 0.7 |
| UNKNOWN | `/BleedBox [` | 0.7 |
| UNKNOWN | `/Border [0 0 0] /Dest [` | 0.7 |
| UNKNOWN | `/CIDToGIDMap /Identity` | 0.7 |
| UNKNOWN | `/ColorSpace /DeviceRGB` | 0.7 |
| UNKNOWN | `/Contents (` | 0.7 |
| UNKNOWN | `/Coords [` | 0.7 |
| UNKNOWN | `/CreationDate (` | 0.7 |
| UNKNOWN | `/CropBox [` | 0.7 |
| UNKNOWN | `/DescendantFonts [` | 0.7 |
| UNKNOWN | `/DW 1000` | 0.7 |
| UNKNOWN | `/Extend [true true]` | 0.7 |
| UNKNOWN | `/F1 0 Tf 0 g` | 0.7 |
| UNKNOWN | `/Filter /Standard` | 0.7 |
| UNKNOWN | `/FirstChar 32` | 0.7 |
| UNKNOWN | `/Flags 96` | 0.7 |
| UNKNOWN | `/Kids [` | 0.7 |
| UNKNOWN | `/LastChar 255` | 0.7 |
| UNKNOWN | `/Matrix [` | 0.7 |
| UNKNOWN | `/MediaBox [` | 0.7 |
| UNKNOWN | `/N /Print` | 0.7 |
| UNKNOWN | `/OpenAction [3 0 R /Fit]` | 0.7 |
| UNKNOWN | `/OpenAction [3 0 R /FitH null]` | 0.7 |
| UNKNOWN | `/OpenAction [3 0 R /FitV null]` | 0.7 |
| UNKNOWN | `/OpenAction [3 0 R /XYZ null null 1]` | 0.7 |

## 8. PARAMETERS

| URL | Params |
|---|---|
| `https://a.nel.cloudflare.com/report/v4?s=%2B11sJdt4BGy87NSe8YaCpNvhHj1Yxv1L0doRGr83R4bm0zELwmXNBZA3eFh2diUZ4ENZtMnh0kE7TQ1o1J4mY0uzMBgU5EIOPCd4F%2FemS2bT7XY2NILRYLJm1kTkF5mOIgUl%2FngV9Cp2TnSRYWyI0lEF` | s |
| `https://a.nel.cloudflare.com/report/v4?s=%2BHacCx2woKEHRhtVNK3OUvgmWv7fTEYPRBBwnCYV%2BYXemZ%2BgwfSLx0clUNJH8EH54DLXbUjffaUL28wFcZdm3%2F3RCPsFBIwNgpiNBta217ann3S6s5dJ12kYxMv%2B8ZsnwY7T76jp5LDkTPJXM0l0HD2D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=%2BbCmoLP26Q9azljNnO3e2LVNjRCcsOA9KQKrtOrFCj%2FrbrtvzEHFKJZmexytxGhJZ7oBoXsMPoEk%2FtFT1bSO7hNzgB8UUiubJANXj%2BxGjRRsvt2dHVV63VNOwf0fwLKfQukG%2Bv0oJReGN6KufozMT6vo` | s |
| `https://a.nel.cloudflare.com/report/v4?s=%2BeACqW0I8CT%2BSjAdI2buE3h9FExDV1WxlAG0on%2BekHlobi25m68B%2BUzkrVXZNfW0sP4yaQobT%2F5J06dWERtK%2FQCoZ4hvLlX1vPt0jeWRd56Z1EvnAsW8o9uc4VUcimo4N0nLZGrI4rJgp9hC4POxa6R%2F` | s |
| `https://a.nel.cloudflare.com/report/v4?s=%2Bj3NWUTPJ1yp%2FKkH1fgehcon8s6u0DSGxPUnLsk088A9%2FcMgwYwK5iRYesMkxHYiS1Hjb6tkHbUAYsfhP8bgtjijoYnDZ3b8Ck5YuNWyp6%2BtCrw4sFGYx0ZLfwKsnyaOg42qBYwz7pMfi7GKqmyA56UW` | s |
| `https://a.nel.cloudflare.com/report/v4?s=%2FD%2FEoulbcuhzfl765jAVa0zWCyOybuI71fzkr0vsdjp2G7AXyXVrZFfY%2BG9LF9fyyN8AU9s6wc6%2FjF%2Bvz7K9Sa9ZUyF8jTxowsYhVMNQE4lU3qdqzHSi%2FGvfUyJA%2F6yq42p1qcKo1sEVEBUIbYsiZ6y8` | s |
| `https://a.nel.cloudflare.com/report/v4?s=%2FSaspEtLlPQdWyE%2BEhjvJOZm1Puu2q5YQV%2FnLYNJSse46%2FP3DMPhLwyMSV3nxh%2B2ITu2HefKHloIV9Y8GRPKGuwxL7q0matVznggBOTVuHyIZtYyTVA8KPL1CeTUbhJSp%2Bf6MGQfXLJBJvE4IZc0zafg` | s |
| `https://a.nel.cloudflare.com/report/v4?s=%2FZ4B3nGT5FsBqGRaRkv7LYd5rG9Olz1yJs7wwdQfv94v3MIaGClmCJxwRVxj9V7nJuQa8b9LABqwvFi8fngl%2BpFsFjNNSKyzS15jyHWOgMhcUiNAL0ocVC9WFT6zeAJJuD588fo9SjeVA5GRjZhsnLTy` | s |
| `https://a.nel.cloudflare.com/report/v4?s=%2FZfEmJpLvJ3B8b0nxVxO7Q0QL9g3669xQdL0%2Fq8594%2FS4tPTj8nKof9gQauISiWRjwIaaPNWm3CytkdFUS7qKPakcjvPCXWP37evfu6i4O6hRcAMK66t5lu%2BUiVOqQygKnSB%2BZuADMPIc1aRtB0Eyo5J` | s |
| `https://a.nel.cloudflare.com/report/v4?s=%2Ftbm9PkdxcFRW2v0M7gJseb5LSmth%2B%2Fk7BrBaHfiDNfWHIPSEcTDBKzykwBc34Bh9rDC8%2FztghGX4ZvedHGSyDEwf%2FlXvDD15BlapnwOlSpbJmUzmompIFCndySdBAq9JG9nGhosusRL5DKzXwHxkJMg` | s |
| `https://a.nel.cloudflare.com/report/v4?s=%2FzmoLQPvrI5rE%2BCT28Brd%2F7D8hUZ2rqlQ7MV4jY%2F%2BbBE0nW5iBK2CAoKLBZFp6ar5syqyIl45uzI%2F3NxFH4TqkOLeSFY4u2B4WY4jaGV%2FzeZ3R8r8bxSAeiO9BcIJj%2BXNJ3dZ5UXhepHNs%2BpQCI%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=0NEgdqPVBp6VwETRgye1lIppkz985Q%2FNhizrSc0Pl%2FeyCvpe8aIN3FsPoBcpZpXgztZSZtHViHcWdE%2BHu0M0IXutgjnE1ZxIR1c%2FFj5OeN5BZ1y%2FSgaHuYuAl6TFpNsfOYVLlIQUVkzmZRGuMWg3DK5w` | s |
| `https://a.nel.cloudflare.com/report/v4?s=0UiaCs2bOmCadVwAXIURmcOR%2B3gEG4W2EKk0o80h%2F5HPea6lxSFTk%2BkW2IboWktyyfvvzEUQpbhL1rmZp74AY8Hq3wLWqxnDoI1qvb7KLfbWFqu3mqGcMRrICZ%2B%2Bbku%2FU7H73LWov7ANegb6qT20pppj` | s |
| `https://a.nel.cloudflare.com/report/v4?s=0XX%2FsP95t11cPHp9SE7AuICmsKw%2Fe2B87niVwhXpxB%2B8qu9utd7s6GsUFKwgBvqHs5UaTHE2Gi3v%2F4FKRDs%2FkGF9nQ0z2htz2Py%2BppVtwOrbScGFg%2BQvkojsho6mpcI0YasB2dKRcvd4OiB7Btyp8wQ0` | s |
| `https://a.nel.cloudflare.com/report/v4?s=0gEpagPvd8XdLyfq2jAUtDi%2FnE9fdR7hfn9d5V1HBFJ0xUES5A4nHzVaJL%2BIW86hjGmCPfrAylvGbnRRx%2Bfk3NG%2BaHSpDFJkqMM9VwlJiBpbj%2BqNzHHoRynZ2hnWsdY7fAK7LWb0mVWOFWUs1kk%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=0hShqeMLPyHVt1erhEIKj32S8LbFkqaYgA8ngCmXjgRpcL12hycwIpv5miaL4IxHiCL24mw%2Fpo4b%2BZNJ46Y78XnzQ0DGYiTjaALbkgUebL6mmp5zBkC4LLPsqVh8jI0w9IUGrBACD7ukgnm0duA%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=0hzKl2oMjO5VAuZNpuqQPw3qDg04ILxTqgKHJECYCUc9GsDDHnZBrIZEb2t4YY4Jg0GSIG%2BwYuVY%2F1aroNp%2BB64bXx9zWOtfKJYDOSMDXIgFvbEZ4wyl3W30GY5ZqYOJyIFnU9kQ2ADSrRXdDTQ%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=0m%2BKj2unj%2BE6EYghlK3bnM99RZrOauuGpysncfZ%2B%2BJQhNzsiD1DtES8E2gcNC2paeyL5I1I2XVc%2BGuEMFPpSBmcGpVOxpddEhjO6NYsje8YnUmGvogygCKBxlGtGciXuVGFGsE%2Bag2XUB%2FrOA7aTXJs9` | s |
| `https://a.nel.cloudflare.com/report/v4?s=0tplEaKfX57nCed3IvOfWDDqW6I7KOA338TwuKk4rWCVsu95Rk%2B4FlEemIeDbFPtzwr0eD9hz2uFrWJq7hmSUMbWZQ5GjeYIti1UMHoIcFtDuKo8UZqc%2BexWf3lsys9vyAMq1j9iL7OWNO2%2FiJg%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=1%2FVZzDZ1WCKtiioIoPouDzmaqoah%2B90Qf6skfD5qLd2eOLHaojbRhkiLGRaOwDwPuA7O0gtKOXmEWMPHRne1%2FasMc5tedAw5uHGKKdVsCChtt%2FYHZej61%2FPI7gN1L3HM2lCskw5TzKZqq%2Bse4Di4BOQF` | s |
| `https://a.nel.cloudflare.com/report/v4?s=11lLNEnKmycWNMoJSD2jVIfpbOV%2FgEdQZopeFiG2eQQnBTbzxYLjYvYFs5DXHkhKjzIYpbzWSO7zsWyjLRdcC4xEaHz1cfnBD5S%2FzinrUBfW3IQHC5TmlWvwjgmwSxUdpPg5wVi8fEN2o9%2BZq0w%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=13%2FEBkOqE7aEFMttOo88%2F%2FDNbHVy1UWettcYv%2FRECD2I%2BbKUlatslOpT7ihT7vgpx4wVN%2Bz%2F%2FKOWEtGlx%2BS%2BLKGeH4%2FGKs2iMPS%2FQasC7oUWrYRSkJ9D1QvsCBWCuQCsxmbEHvLcUPHa%2FeCtWXg%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=14ELHr6zHih6EHw3nELcOws5QOHJqgNJGy1DLogA5cUPv%2FEc2y7gUIWXNfYhobohVVaSKkxhmW1pZIIMf1mhdSf43VHxvxAVHMjR2dooQeUFpXCuykaxFdxg7LxLYJGUWqNtcm905aUMPpOmKTE%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=1BL17D358oTyYXSkI0oC5rKsNmIHau9StzM2TNrnIYxjSdswSHSHuqvoUd%2FliYFG4Zths4Wg7MjjO%2B8%2FJHXWjshAy4xjcQ7agtu1D9FIcz%2B0c52zFcgzZXWJ25mdd6VpFCQrItpURJmIxSxZ6X%2FUulyZ` | s |
| `https://a.nel.cloudflare.com/report/v4?s=1LL6wIm6qOVMTYN%2B8rZHNRN3S1zxnzxwA0fCBG0WZwkiEDgrMHmLfl%2BQ8tLoM8tziPcbiuI%2FWdUYInrohrgkbD58U3H%2B35SFRlI4oEyL28ALNnXkoZY8g1xh6hMvd%2FEuEQOe4VGwRNz6ZSGmfu%2FRzr8O` | s |
| `https://a.nel.cloudflare.com/report/v4?s=1UW2B6%2FDGhEVVVTW1nAd20EJL50JjH0SgOiSFV1PRLnsFrbFiVn6SUnRA5ndAZ%2B4D5lX8MrCZq8j2%2FvcRtIAXyjs770zxYQqlV%2BMiCpsmr2DcNc60HXM5G%2BJj8kdGCAzn8zTlgybIDo9a%2FKsZp8%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=1aXFoTigPJP0deJ%2BLhTz%2BydbsIdNlr1IWxIsECZxEDYm2UvwjzqdSjsGS1PuTeboigttEMzZy9D1nR8IPrtC6ABh0Llo4p5ArMz9lt0fZh8RhQcq2Lzau8vxsdsRDcXwsNcejqP5qmg6ChfqnhMUBcl6` | s |
| `https://a.nel.cloudflare.com/report/v4?s=1cMpiD0bY%2F8xIYuPMIje06yhbv3BHqx1PyzMlNlF94KZwKzGHZaVCIIVtInDrqKwUYTBcJv3FSS9iaZZ03eyIUkhyT2tbhkeASd%2FO3QtPNvX%2F05dkDOw0ahfvyRBNeznzw6Xh9rgJUjI6ubJd3bXk6h3` | s |
| `https://a.nel.cloudflare.com/report/v4?s=1hkmL16uXJkZUnnUv7Mi8Sy4dw4oHu2DjCxMoc%2BLKdU%2FsX2X9%2FBLqQo2r2LyNo%2FLwcKTxtoglDjf8jFVNHg7v%2FF4yFgjI%2BOie7KMXKjsBcfZiSYUluAE4CF9qfzYfBqT%2FMV5DjI83Cs2iVc5cDs%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=1w1K2dpE49HsLjsUFVlwkF0YeIpiij7sf1L4y1cXN%2BA95vuXmOH%2FXpq8BpevzonGwT75SV4sD6%2FXERXuzzNXcwayb%2FWEF7pyth0%2B%2BzWZcrjgKTkO44bb4YsOczFs3IHhUjDlx4dCqcBpwUMBja8%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=21eLxn3O%2BvjhrGZSNgedyzJApX89JhWDF9wJJ3xFqF7tbWhzm%2FI2D6V9ctMV4IJapfchxXoNr%2FuvS4jgTVTtAmQ%2BEeBUJAfLR7rFiIAsFyujwY5gBsW8bw1J%2Fs0VTcDU3TmHCXt8CwIN6cOipRDke1qz` | s |
| `https://a.nel.cloudflare.com/report/v4?s=23D6NnndFtsqWT5g0t%2F2yY93WQXTo%2BO6DcmgaAllL3Ogn5adTYngtKKlBYVB%2F4YpHvloRg6rHpK6KdoGQMOAhbdRWrmNqfx9xorDXXsbYrt7DmtLsErHxz%2BWnmKHJtzvIZJHEi9HVtyEnYrbuP1GfyZz` | s |
| `https://a.nel.cloudflare.com/report/v4?s=24GeqdAoEaJSPdAdq00t3x7sMh2g9xVjwY%2FzapNedzXxsyErkJ8pBfc32ZP8JQWtJ%2FDxdbpAHm9gx7BwmmiTElutq966Y3VN3pf5o81J00WWV%2BVnZDzuRKJqVeZ1YB1SWPNCdodoa2Ejj4G4%2FkLj9eS9` | s |
| `https://a.nel.cloudflare.com/report/v4?s=25KW7ZOP3qMw1XlaSAKH8PAGheWQg0%2Bg5PSwSmuqf4RukG1sWnx%2BWhd5wfkGmuao9%2FPokR2X1zM%2BnYzjX%2FyK%2Bc4pp4W64qvSvwngfuB9LXIi51vuYA3zPPwEHYq9Z0DGBwF1yFEg3sUj69dVr10EDoLr` | s |
| `https://a.nel.cloudflare.com/report/v4?s=29%2BX47fCRjF%2Burj59Gkxx%2BX5woDrwCwV1J%2FjLPknr%2FJ%2F5Q7P7gHnVSFeRkP215xG7UIQgBChBefgbp2PeuGi%2BZB9o0VfwPAFbiiL6lvZ%2Fs%2BTRsw2ZGVdVEJZLdXYQytsToJ4q%2BnpAtzxPJAMIte08RAh` | s |
| `https://a.nel.cloudflare.com/report/v4?s=2FL9tXS5M5YlMRl4AdhYSyJJhFqsxg0rDCkUSjmYL90gV%2F6e4mZeohhBt2WzcicvRs5%2FJt3twJB53NnOPOiCIBUBnYQCTrb0EpUa9zi5VP7cwMNt8XMQFwqsVgaF7Yb17NgMagFrZ0FCgDcpKdU%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=2TRWtD2VYvvlDtUDM2WvVhzkz1VjP%2BgCo9JdTrB4reVS1roDowGII6Oc%2F%2BRSaZrrTuA%2Bpm9jWhdgnqZGY792s3Oq5MbBSTGaWlAayIx67uJ9fd9dzgmxSrMTz3HQvYfoazH3xmXchZl%2BmCrVh9A%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=2ttatYgxGDN2xklL1JbsugkyRAx%2FfrGvFCywUtgFXwF9mz1EVjtJ6x7900gUBcf3wFgZNwCkqW%2B6CjxcK5kDpd7wY0GHbQGTXju81DpkCBdqH0mv5kNvgr3MzeOXPj%2BdqE1qJcLaIwi6E1hyiWUagcre` | s |
| `https://a.nel.cloudflare.com/report/v4?s=34E76tD75TKzOObNj3LB0A18qM25Y1fexREpfdZWY6u4FlEFFa6apBAOw8cpf%2F0xaKBc88MKlxTO%2Fu90z%2Fvh4nyQjWYsieIXQF2O6YSbzAW3PWnIIdaDtJnwaKMKGaetEvzjJa2vWE%2BzUu6Nz6o%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=3FlJgbz1PsBnwe5LnPm8CYiKZRh5S2tNCG3UqdQLkHx%2BO%2BKCARu%2BVBfvhL8zqAyYU%2FjfwlIPSfLw%2FyUAfYbxLZ82bLCU5BHqJkHr0XmiAuCeQ%2FfElzGMl6xz7yVnolNid01xKtYz1nVViBYGRnP2YGT2` | s |
| `https://a.nel.cloudflare.com/report/v4?s=3P5Kgtkhi%2FnxqkQzGGd%2FSvC%2F3mFcTLK02vyxcGrLtF4IK9CGl6qNpz1y00GX6H1nc9PPUCdBPXeG3hgkKOyBj1S%2FW90EHjJQPIbqwp8QJvSMsNBA8fGCkmUXJkPFCXZdPE0d76wcm%2BHH%2BKJj3Nw%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=3UUc2PqPs4KcLfs%2FKUuZDP39njkxdVsF02KhuhR7ROY4Hs5cRMgyi%2FqudYP8iMgXIFEXdIW6Lzqq4V3ED0Vs0GDNVEQl8QRq8p2t%2B%2BXlAI2aowJq6n1kI1PcPa0oU8bIKTwVAsYmcHmmyuyu%2BhQ%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=3YqYcsUm9zk%2FWpr6k9WkjOHLJaNnZOkeuY4kx%2FPjS42HyhtwYgC3%2Bcz2blV2o9ejUjPXPQjDcHyVxvduLovEwlKy%2FbQoufR6wgW8Y5%2BXOIOBkgAm3yKV9YbiGD9Cq25Fj821ECDzWTxVafjX3CU%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=3bdZNf6iw8W6esuHaxHJD%2FFRcOzCzTx4OdpjLQl2V21Hejzt0WiUNfU1TsRWzfQ4avPXKNz9C5V0ktEfgRIynZRHZvAW2614JbdsYVKoK09RwOHKjBi%2F%2Bj7rWQs4j87UcSEQ0JQJY4fP0Fy9EBn1teIK` | s |
| `https://a.nel.cloudflare.com/report/v4?s=3cAQpnQ8fOZCqSDJiI9LnurT4gly0stjwduET8uYm8SJgv5Q8ex7RbqaKxU8IaBmED%2B29vrtA9g4wsDmafFZdNOvqWIpkzJSaWhV98BXAv0hS%2FUKK5k28BKvIoJSoI9mq3y%2FdOTFp7m2GJMJ4zDOP%2BwC` | s |
| `https://a.nel.cloudflare.com/report/v4?s=3cLydfR4BPbuYOzAugpKL6YtoULjK8PPrx%2FjCZ9omfExMulQ%2FFc%2BBeZYi2C9ZwECcswooC94vuqwvKp4KBIQALCndFOH363VZIOxYE7ZkPqAESERPJk81KLwBI6dtfIZCZ81FFqVvAgN4oziZig%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=3ll5QKtMMrautE5EqSOUhBOJwuI7kEnm5XQHqVPZO57FFIaQ%2B7I0NbEequn96rCUOpsITsbOn0Awh6xYOlLWM8Dg2c%2FiwE6V13sBTFjVeUCYBfsdAwXl5Dvvwqap2hixAMw1biEWeLBZvERFXmATkOgm` | s |
| `https://a.nel.cloudflare.com/report/v4?s=3sZZJZDzip%2BxXcrVwog9A%2Be3Z%2BmJqBarZXC8fxEOPCEOWAHbx%2BQGI74mhyCHBWzHt4f%2FXgV24LDX8qTe1lxESVKuNe50myaw6sIg0ZjxpTjUJa5TusTqXp3MPWpKGhca75pYP2VFfOWFNFVTMKFwj%2B0b` | s |
| `https://a.nel.cloudflare.com/report/v4?s=3tevHuPMKiwm78kna%2FNhi%2BK2%2FSPjpPFi%2B3LLZFde%2BVKa%2F8QwE5JpqrOVjqU96eMowy%2F9tSh0SG%2BQ1qnTSVJssEajI74uZ9mpiBqdEsuLChBAiWd2NDKssXBar68EU1DTK3FcA2r8GwUU3Bvql7bYmj9d` | s |
| `https://a.nel.cloudflare.com/report/v4?s=3zakIknc2aDDaq4gwtcWX0u2lgcGOFhX87GtXx5b0Q635khQodgfLzTG5IZ5qAFXhELBXvd6dR0pKkWwX8yz8SCLaJHpijIinp%2FNGifw7%2BeABtoxgcocmdfsLlCzM3eRlNRwILOzFaDoOfRi9z4%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=49SRldYWx5cwHRliovvAf1RoSOj1acbTegSOVvO5V1EI8XGs22f51%2FKtXt2lXv9%2BHT%2FH7xRbm5Kt20sjTzB2VNihTU2tUJv2%2BSLv1qBA0HIw3xwEn1gNeG1YESq%2BT3qMUBQ4yQftJ1c2cdnOSrI%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=4Am4tp4Ohl82bCG8Okl4%2FxgtEr78sVU1XSNqcbTNaWq36oJsul1PFhujuGLKvVQxFUllIsI2ViwpJiIwPth3qFhRl3es4jsifSbV0JouglkRYYvBg2nITgz%2FSZlRC7AOhkbkKi5gNr%2BVPQFeGsMeg7mT` | s |
| `https://a.nel.cloudflare.com/report/v4?s=4CFz%2B3kYCww2czSgzHv6kcdsQnWyJCSlyLJGqt%2BqSwRG16q5uvUGELdFUgJO2LYTzdsf%2BXeVw0Zcd3BgCt4PIzBl4w45D4Xbcb7pvPGexnW2Yn4eea7sXPza7lAQPksUlT1FAaYJCUojkxA55wM%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=4IvqeSwb%2B1FElPB%2BGsjlXbxYdHJmLbXkUgnE5JhnH7ONxzBXhs0XpEYM2WsBzrDqh%2FMTZGWlfNE84dkACOAWTglwiHe5iKc5GbMybz63n221uHEV%2Bc7MwdJDgDrM8KnadcssEQEQ8bost4lzb6vMxeRa` | s |
| `https://a.nel.cloudflare.com/report/v4?s=4P6wpiV2Bz4VqblhnOaeZIvfjVEpR3nROuEGVsbcOMIpMESqvtVM6DrOrQ5y0hH5NPFtCTTHRg4yIcB9gJR1lVpcBocCHhzY%2Ff2rTSpk8rfL9b971Y74bCEHlNzDIdkko61n7vgmYML6XdGbp4r7Y%2FSb` | s |
| `https://a.nel.cloudflare.com/report/v4?s=4PnBzDnAAcnvqDTleQ7e8SFqL8ddPxA32UwTFGvIrohJlMp%2BZ2ZZYS7ZRyDuTXwmWDXMUuVIGBSF0IUpUSQ9Rcu%2BWo%2BHQhBOeojlao5%2F5ZBjuiq%2BUUdcEmjsQbJAfs0CdieHiPpCxFuBIKIn6aM%2Fh5E5` | s |
| `https://a.nel.cloudflare.com/report/v4?s=4UtkeslDjxNVXB5g3byou%2FvbFAAHjNtRvaP6tjL1uQhVZMrdKSpbGI2BB24nN8R7LfNnrzi16TDP8cjEdHdW5LkKPFau%2BpM7qTKlxHk4iS4%2BlJ91Sn8MtnMSe57Nx%2FA34ol%2BGWryldKN3yeme4QBa3ZL` | s |
| `https://a.nel.cloudflare.com/report/v4?s=4Z5jD8uJpzryBomLqozdGcWb43tBZ4OyccDvTS6L0VLgp%2BWL3d11rQKx%2BVEsQIPHvoOxfVG3IXpiR3HnTYKwg3Ro%2BuuIxDDa0KoxQUNYxFtIOSzlP1LGy%2FKWYO5cZRNXL2sIEH60eDaYQ%2FWdJxxm22CC` | s |
| `https://a.nel.cloudflare.com/report/v4?s=4bNMOX4DCbuG3wZVvTo90317ukX4b%2FxulCMHozrhb1pO2YXDf%2BVcET50BDLHBnX5%2BWwNMIvP5YUkzyxpkoApsGOGUKO3LNTJQFmOSP1tsGwhqkqAuZV6%2FJQP5KPKp1K6%2B%2BM29Fg4wdplHwptYP1Ui3yO` | s |
| `https://a.nel.cloudflare.com/report/v4?s=4bjTp7Vt1S%2BjQpdKQxh%2Fm5c5AyjXVp9BCLyAXbWlCxsvI3vPdtq1HtaFWWEZWXwwqnBXPoczJTlMTjeyzYFFAqK040BoK97TMGHct%2By4ckoCCl6MQ0J7UKKbVN8AQcz7bSew7rXoLp1z0AIMMkx3ifrD` | s |

## 9. SECRET CANDIDATES

_None found._

## 10. NUCLEI FINDINGS (verified exposures / misconfigs)

| Severity | Template | Host |
|---|---|---|
| info | `dns-waf-detect` | `cdnjs.cloudflare.com` |
| info | `dns-waf-detect` | `challenges.cloudflare.com` |
| info | `dns-waf-detect` | `aff.flowith.io` |
| info | `dns-waf-detect` | `challenges-staging.cloudflare.com` |
| info | `dns-waf-detect` | `cdnjs.cloudflare.com` |
| info | `dns-waf-detect` | `challenges.cloudflare-cn.com` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `discord.com` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| info | `dns-waf-detect` | `flowith.io` |
| … | _188 more in nuclei.jsonl_ | |

## 11. TOOL RUN STATUS (no silent skips)

| Tool | Result | Detail |
|---|---|---|
| `anastasis` | OK | 417 endpoints, 87 params |
| `cariddi` | OK | completed |
| `dnsx` | OK | completed |
| `ffuf` | OK | off by choice — wordlist prepared |
| `getJS` | exit 2 | see logs/ |
| `httpx` | OK | completed |
| `js-download` | OK | 673 chunks saved over 3 round(s) |
| `jscope` | OK | completed |
| `jsluice` | OK | 673 files parsed in batches of 100 |
| `katana` | OK | completed |
| `methods` | OK | 1400 method responses |
| `noseyparker` | OK | completed |
| `nuclei` | OK | 268 findings on 300 live hosts |
| `subfinder` | OK | completed |
| `subjs` | OK | completed |
| `trufflehog` | OK | completed |
| `uncover` | OK | no API key configured — no external data |
| `urlfinder` | OK | completed |
| `uro` | OK | completed |
| `vhost` | OK | 63 real of 63 tested |
| `waybackurls` | OK | completed |
| `x8` | OK | parameter scan complete |

## 12. INTENTIONALLY NOT RUN

- **ffuf path brute** — off by default; `wordlist.txt` is ready. Set `enable_brute: true` later.
- **kiterunner** — off by default alongside ffuf.

## 13. OUTPUT FILES

| File | Meaning |
|---|---|
| [`all_routes.jsonl`](all_routes.jsonl) | every route, unfiltered (1,562,758 B) |
| [`accessible_200.jsonl`](accessible_200.jsonl) | HTTP 200 wins (743,640 B) |
| [`exists_blocked.jsonl`](exists_blocked.jsonl) | exists but blocked (591,363 B) |
| [`other_status.jsonl`](other_status.jsonl) | all other statuses (867,490 B) |
| [`data_files.jsonl`](data_files.jsonl) | JSON/CSV/XML among 200s (6,284 B) |
| [`params.jsonl`](params.jsonl) | parameters (994,333 B) |
| [`subdomains.jsonl`](subdomains.jsonl) | subdomains + resolution (8,219 B) |
| [`third_party_routes.jsonl`](third_party_routes.jsonl) | third-party URLs — kept, not deleted (161,636 B) |
| [`method_responses.jsonl`](method_responses.jsonl) | all method-probe responses — kept (163,494 B) |
| [`vhost_real.jsonl`](vhost_real.jsonl) | non-blocked virtual hosts (3,192 B) |
| [`vhost_blocked.jsonl`](vhost_blocked.jsonl) | blocked vhost checks — kept (0 B) |
| [`js_endpoints.jsonl`](js_endpoints.jsonl) | AST endpoints (39,761 B) |
| [`vhost.jsonl`](vhost.jsonl) | all vhost checks (3,192 B) |
| [`jsluice.jsonl`](jsluice.jsonl) | JS-derived URLs (1,404,861 B) |
| [`cariddi.txt`](cariddi.txt) | crawl + secrets/endpoints (844,498 B) |
| [`wayback_urls.txt`](wayback_urls.txt) | archive URLs (1 B) |
| [`noseyparker.jsonl`](noseyparker.jsonl) | fast secret scan (1 B) |
| [`nuclei.jsonl`](nuclei.jsonl) | verified exposure findings (336,603 B) |
| [`anastasis_endpoints.jsonl`](anastasis_endpoints.jsonl) | AST endpoints (39,761 B) |
| [`jscope.txt`](jscope.txt) | evidence-ranked JS analysis (101,219 B) |
| [`secrets.jsonl`](secrets.jsonl) | secret candidates (0 B) |
| [`wordlist.txt`](wordlist.txt) | target-specific fuzz list (230,203 B) |
| [`params.txt`](params.txt) | parameter wordlist (181 B) |
| [`js_urls.txt`](js_urls.txt) | JS chunk URLs (33,986 B) |
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