# Hunt Report — https://antigravity.google

Generated: 2026-11-22T18:37:37Z &nbsp;|&nbsp; Duration: 13m 6s

> **Nothing is filtered during collection. This report is only a grouping.**

## Summary

| What | Count | Meaning |
|---|---:|---|
| Routes collected | 5197 | Every URL found, nothing removed |
| Distinct routes verified | 1454 | One row per URL (method probes excluded) |
| HTTP responses | 2654 | Includes method probes — kept in `method_responses.jsonl` |
| **Accessible (200)** | **302** | Confirmed live — the wins |
| Exists but different status | 9 | 301/302/401/403/405 — real route, blocked |
| Other responses | 1143 | 404/500/etc — kept, not discarded |
| Subdomains (resolved) | 1 | DNS-verified |
| Virtual hosts (real) | 0 | Cloudflare 403/530/0 excluded |
| Parameters | 2133 | URLs with query params |
| JS endpoints (AST) | 0 | anastasis evidence-backed |
| First-party URLs | 5149 | antigravity.google and subdomains |
| Third-party URLs | 48 | kept in `third_party_routes.jsonl` |
| Method responses | 1400 | kept in `method_responses.jsonl` |
| Blocked vhost checks | 1 | kept in `vhost_blocked.jsonl` |
| Secret candidates | 1 | verify manually |

> Collection keeps third-party URLs by design (48). See `third_party_routes.jsonl`. Method-probe responses are in `method_responses.jsonl`.

## 1. SUCCESS — HTTP 200

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 200 | GET | `https://about.google` | text/html | 133480 |  |
| 200 | GET | `https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fantigravity.google.com%2F&ec=GAZAgQY&followup=https%3A%2F%2Fantigravity.google.com%2F&passive=1209600&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-349897383%3A1795372128128426` | text/html | 1259592 |  |
| 200 | GET | `https://antigravity-hub-auto-updater-974169037036.us-central1.run.app/releases` | application/json | 2847 |  |
| 200 | GET | `https://antigravity-ide-auto-updater-974169037036.us-central1.run.app/releases` | application/json | 541 |  |
| 200 | GET | `https://antigravity.google.com` | text/html | 86285 |  |
| 200 | GET | `https://antigravity.google.com/assets/manifest.json` | application/json | 429 |  |
| 200 | GET | `https://antigravity.google/` | text/html | 217210 |  |
| 200 | GET | `https://antigravity.google/?_gl=1%2A1954lpy%2A_up%2AMQ..%2A_ga%2ANzYzNjM2MDI0LjE3ODc4NzE3Njk.%2A_ga_47V54ZJ3EV%2AczE3ODc4NzE3NjgkbzEkZzAkdDE3ODc4NzE3NjkkajU5JGwwJGgw` | text/html | 217210 |  |
| 200 | GET | `https://antigravity.google/?_hsenc=p2ANqtz-8Tkmw9I0UeqoSjr86NGmBAeCO2T354wd9Qx4OaF7BX3fU778pY-magiSg6zmuCQYRaDRi4` | text/html | 217210 |  |
| 200 | GET | `https://antigravity.google/?amp=` | text/html | 217210 |  |
| 200 | GET | `https://antigravity.google/?app=antigravity` | text/html | 217210 |  |
| 200 | GET | `https://antigravity.google/?authuser=1&%3Bhl=bn&hl=bn` | text/html | 217210 |  |
| 200 | GET | `https://antigravity.google/?gad_source=0&gad_campaignid=24417978225&eps=AHas8cAQGWSLatypRfsHnrcRc-9u5TeP48kDr8D-MVOKRj6MtF_rGFHfFwEa9dHLZqXaZmLzY9fYTIpSCLogpgWOY-XgOzeAqYloBpHo3NWQ6pw-bNIC9nTvC6cVRw&gclsrc=aw.ds` | text/html | 217210 |  |
| 200 | GET | `https://antigravity.google/?gclsrc=aw.ds&gad_source=1&gad_campaignid=24305882099&gbraid=0AAAABE0JD34jh62e4cyL8Nq9Yr8Md-Pa3` | text/html | 217210 |  |
| 200 | GET | `https://antigravity.google/?linkId=57432659` | text/html | 217210 |  |
| 200 | GET | `https://antigravity.google/?linkId=61956604` | text/html | 217210 |  |
| 200 | GET | `https://antigravity.google/?prompt=consent&state=6P030c4NQcsrNP59uchDcw&iss=https%3A%2F%2Faccounts.google.com&code=4%2F0AdkVLPwyLFXz6E8OdhwkEFQ0c32vofyTKQAFCqbZLhiOgyB81hHVcKicl92sOupbQ_93Ew&scope=email+profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcloud-platform+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcclog+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fexperimentsandconfigs+openid&authuser=0` | text/html | 217210 |  |
| 200 | GET | `https://antigravity.google/?ref=aiforpro.ai` | text/html | 217210 |  |
| 200 | GET | `https://antigravity.google/?referrer=AISTUDIO` | text/html | 217210 |  |
| 200 | GET | `https://antigravity.google/?s=09` | text/html | 217210 |  |
| 200 | GET | `https://antigravity.google/?t=1wPnVB1rj1BXtoP4erejIQ&s=35` | text/html | 217210 |  |
| 200 | GET | `https://antigravity.google/?trk=article-ssr-frontend-pulse_little-text-block` | text/html | 217210 |  |
| 200 | GET | `https://antigravity.google/?trk=public_profile__posts-text` | text/html | 217210 |  |
| 200 | GET | `https://antigravity.google/?utm=googlecloudlivefeb24` | text/html | 217210 |  |
| 200 | GET | `https://antigravity.google/?utm_sourc...%5Cn%F0%9F%A4%96=` | text/html | 217210 |  |
| 200 | GET | `https://antigravity.google/?via=bahriddin.uz` | text/html | 217210 |  |
| 200 | GET | `https://antigravity.google/_astro/AgentFirst.astro_astro_type_script_index_0_lang.pgLwEYDv.js` | application/javascript | 1427 |  |
| 200 | GET | `https://antigravity.google/_astro/AgyVcsReview.astro_astro_type_script_index_0_lang.BV47Wads.js` | application/javascript | 46303 |  |
| 200 | GET | `https://antigravity.google/_astro/AnalyticsBootstrap.astro_astro_type_script_index_0_lang.DY7s9GDE.js` | application/javascript | 29978 |  |
| 200 | GET | `https://antigravity.google/_astro/AnnouncementPill.astro_astro_type_script_index_0_lang.BT7DGgwN.js` | application/javascript | 4482 |  |
| 200 | GET | `https://antigravity.google/_astro/AntigravityFooter.astro_astro_type_script_index_0_lang.CMhm0RTX.js` | application/javascript | 1969 |  |
| 200 | GET | `https://antigravity.google/_astro/BuildWithGoogleExplorer.astro_astro_type_script_index_0_lang.CmO2G-bH.js` | application/javascript | 2323 |  |
| 200 | GET | `https://antigravity.google/_astro/Button.astro_astro_type_script_index_0_lang.C_rx8ulw.js` | application/javascript | 1134 |  |
| 200 | GET | `https://antigravity.google/_astro/Changelog.astro_astro_type_script_index_0_lang.D5cGTFF8.js` | application/javascript | 7175 |  |
| 200 | GET | `https://antigravity.google/_astro/CliPluginManager.astro_astro_type_script_index_0_lang.BDA0l01W.js` | application/javascript | 17773 |  |
| 200 | GET | `https://antigravity.google/_astro/CodeSnippet.astro_astro_type_script_index_0_lang.ChVfYBTX.js` | application/javascript | 1069 |  |
| 200 | GET | `https://antigravity.google/_astro/CustomCursor.astro_astro_type_script_index_0_lang.BAxLuM9C.js` | application/javascript | 1586 |  |
| 200 | GET | `https://antigravity.google/_astro/DownloadSection.astro_astro_type_script_index_0_lang.EpoT9f7y.js` | application/javascript | 3708 |  |
| 200 | GET | `https://antigravity.google/_astro/DownloadSurvey.astro_astro_type_script_index_0_lang.CYKMW25G.js` | application/javascript | 5125 |  |
| 200 | GET | `https://antigravity.google/_astro/Draggable.G44Hfzvd.js` | application/javascript | 34427 |  |
| 200 | GET | `https://antigravity.google/_astro/FeatureExplorerNew.astro_astro_type_script_index_0_lang.DjCGJN0r.js` | application/javascript | 1440 |  |
| 200 | GET | `https://antigravity.google/_astro/Header.astro_astro_type_script_index_0_lang.DlRh6qOZ.js` | application/javascript | 14162 |  |
| 200 | GET | `https://antigravity.google/_astro/LandingLatestBlogs.astro_astro_type_script_index_0_lang.C0pOmJid.js` | application/javascript | 1569 |  |
| 200 | GET | `https://antigravity.google/_astro/LanguageSelector.astro_astro_type_script_index_0_lang.CSkw2n2e.js` | application/javascript | 30 |  |
| 200 | GET | `https://antigravity.google/_astro/MainParticlesComponent.astro_astro_type_script_index_0_lang.Cr9vcqqS.js` | application/javascript | 23341 |  |
| 200 | GET | `https://antigravity.google/_astro/MobileDesktopJourney.astro_astro_type_script_index_0_lang.xqTBvT9D.js` | application/javascript | 1488 |  |
| 200 | GET | `https://antigravity.google/_astro/MobileTableOfContentsOverride.astro_astro_type_script_index_0_lang.CnjS8CqJ.js` | application/javascript | 5644 |  |
| 200 | GET | `https://antigravity.google/_astro/ModalYoutube.astro_astro_type_script_index_0_lang.CStNYwFh.js` | application/javascript | 17054 |  |
| 200 | GET | `https://antigravity.google/_astro/ModelSelector.astro_astro_type_script_index_0_lang.CQI7_Pfi.js` | application/javascript | 12819 |  |
| 200 | GET | `https://antigravity.google/_astro/ModelsListAsset.astro_astro_type_script_index_0_lang.Cj5ApgQu.js` | application/javascript | 9326 |  |
| 200 | GET | `https://antigravity.google/_astro/MorphingParticlesComponent.astro_astro_type_script_index_0_lang.Cbj7bMvF.js` | application/javascript | 45005 |  |
| 200 | GET | `https://antigravity.google/_astro/Mp4Viewer.astro_astro_type_script_index_0_lang.QVKW1e9Z.js` | application/javascript | 9452 |  |
| 200 | GET | `https://antigravity.google/_astro/NewsletterCard.astro_astro_type_script_index_0_lang.DAYEvei1.js` | application/javascript | 8937 |  |
| 200 | GET | `https://antigravity.google/_astro/ProductUseCases.astro_astro_type_script_index_0_lang.D-NhmDef.js` | application/javascript | 3218 |  |
| 200 | GET | `https://antigravity.google/_astro/ScrollTrigger.BTGKJApg.js` | application/javascript | 42729 |  |
| 200 | GET | `https://antigravity.google/_astro/SearchOverride.astro_astro_type_script_index_0_lang.DIt0y6kt.js` | application/javascript | 119527 |  |
| 200 | GET | `https://antigravity.google/_astro/ShareButtons.astro_astro_type_script_index_0_lang.D4JXL-LY.js` | application/javascript | 3535 |  |
| 200 | GET | `https://antigravity.google/_astro/SharedHeadBootstrap.astro_astro_type_script_index_0_lang.BTURgnEv.js` | application/javascript | 26466 |  |
| 200 | GET | `https://antigravity.google/_astro/SimGenMedia.astro_astro_type_script_index_0_lang.C33GqWR9.js` | application/javascript | 65486 |  |
| 200 | GET | `https://antigravity.google/_astro/Slider.astro_astro_type_script_index_0_lang.N98p6MdE.js` | application/javascript | 1826 |  |
| 200 | GET | `https://antigravity.google/_astro/SmoothScrollLayout.astro_astro_type_script_index_0_lang.CAeerymP.js` | application/javascript | 2879 |  |
| 200 | GET | `https://antigravity.google/_astro/SplitText.Bj_bHxnY.js` | application/javascript | 7042 |  |
| 200 | GET | `https://antigravity.google/_astro/StarlightPageTitleOverride.astro_astro_type_script_index_0_lang.C7kjScF9.js` | application/javascript | 32598 |  |
| 200 | GET | `https://antigravity.google/_astro/SurfaceAccordion.astro_astro_type_script_index_0_lang.CSzxpaKB.js` | application/javascript | 2815 |  |
| 200 | GET | `https://antigravity.google/_astro/TableOfContentsOverride.astro_astro_type_script_index_0_lang.Dgl9wpyF.js` | application/javascript | 5097 |  |
| 200 | GET | `https://antigravity.google/_astro/TypedHeader.astro_astro_type_script_index_0_lang.5QS0FIL1.js` | application/javascript | 3797 |  |
| 200 | GET | `https://antigravity.google/_astro/UseCaseFeatureCards.astro_astro_type_script_index_0_lang.CGInNRxq.js` | application/javascript | 19380 |  |
| 200 | GET | `https://antigravity.google/_astro/UseCaseQuotesGallery.astro_astro_type_script_index_0_lang.o7P1y021.js` | application/javascript | 668 |  |
| 200 | GET | `https://antigravity.google/_astro/UseCases.astro_astro_type_script_index_0_lang.BqTJDAhz.js` | application/javascript | 3550 |  |
| 200 | GET | `https://antigravity.google/_astro/YoutubeVideoSection.astro_astro_type_script_index_0_lang.BJuyTwew.js` | application/javascript | 3145 |  |
| 200 | GET | `https://antigravity.google/_astro/analytics.D0A6E30p.js` | application/javascript | 9148 |  |
| 200 | GET | `https://antigravity.google/_astro/broadcastSync.Shj6kWpU.js` | application/javascript | 828 |  |
| 200 | GET | `https://antigravity.google/_astro/cache.CxDVmDkH.js` | application/javascript | 2809 |  |
| 200 | GET | `https://antigravity.google/_astro/customHighlight.C-LW2AVZ.js` | application/javascript | 1350 |  |
| 200 | GET | `https://antigravity.google/_astro/deviceInfo.DvRRrq36.js` | application/javascript | 4672 |  |
| … | … | _227 more in JSONL_ | … | … | … |

## 2. EXISTS BUT DIFFERENT STATUS (301/302/401/403/405)

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 301 | GET | `https://about.google/products` | text/html | 227 |  |
| 301 | GET | `https://google.com` | text/html | 220 |  |
| 301 | GET | `https://gstatic.com` | text/html | 221 |  |
| 301 | GET | `https://gstatic.com/glue/cookienotificationbar/cookienotificationbar.min.js` | text/html | 276 |  |
| 308 | GET | `https://modelcontextprotocol.io` | text/plain | 0 |  |
| 405 | GET | `https://services.google.com/fb/submissions/antigravity_interest_form` | text/html | 0 |  |
| 403 | GET | `https://x.com/antigravity` | text/html | 5614 |  |
| 307 | GET | `https://x.com/intent/tweet?text=Google+Antigravity+SDK` |  | 0 |  |
| 301 | GET | `https://youtube.com/@GoogleAntigravity` | application/binary | 0 |  |

## 3. OTHER RESPONSES — kept, never discarded

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 400 | GET | `https://*.appspot.com` | text/html | 1555 |  |
| 400 | GET | `https://*.run.app` | text/html | 1555 |  |
| 400 | GET | `https://*.uc.r.appspot.com` | text/html | 1555 |  |
| 429 | GET | `https://antigravity.google/ ` | text/html | 142 |  |
| 404 | GET | `https://antigravity.google/ Antigravity 1.0 2025年11月に公開 VS code 派生のAIエディタだったらしい AIエージェント Antigravity 2.0 2026年05月に公開 Antigravity 1.0から大幅な変更が入った と言われても使っていないからわからん suto3 エージェント管理アプリ Antigravity CLI An` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/ Welcome ... Gemini 3 Pro in November 2025` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/ 에이전트 개발 플랫폼인 구글 안티그래비티를 소개합니다. 핵심은 구글의 최고 모델을 갖춘 친숙한 AI 기반 IDE 경험이지만` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/&` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/&lt` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/&quot` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/)**世界。這是Google` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/)\n-` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/)%7C[1.11.9](https://github.com/LaelLuo/scoop/blob/master/bucket/google-antigravity.json)%7CAutonomous` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/)—describe` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/)をご確認ください。\n:::\n\n[![AI` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/-21.9253` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/.well-known/ai-plugin.json` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/.well-known/assetlinks.json` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/.well-known/dnt-policy.txt` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/.well-known/gpc.json` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/.well-known/nodeinfo` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/.well-known/openid-configuration` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/.well-known/security.txt` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/.well-known/trust.txt` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/:` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/:Нажмите` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/Google` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/Google에서 코딩 에이전트 IDE라면서 Gemini 3랑 같이 발표했는데 또 vscode 포크 버전임사용 가능한 모델은Gemini 3 Pro High/LowClaud` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/Google에서 코딩 에이전트 IDE라면서 Gemini 3랑 같이 발표했는데 또 vscode 포크 버전임사용 가능한 모델은Gemini 3 Pro High/LowClaude Sonnet 4.5GPT-OSS 120B` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/Mcp.Connect.Steps.Paste` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/P` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/Requested` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/\` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/\\\` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/\n-` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/\n2.` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/\nClaude` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/\nGemini` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/\nWordPress:` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/\nX:` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/\n\nAntigravity` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/\n\n[` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/\n\n[Related` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/\n\n▼` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/\nНаш` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/\u003c/a\u003e\n\u003c/li\u003e\n\u003cli` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/\u003c/a\u003e\u003c/p\u003e\n\u003ch2` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/_astro/${e(o)}` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/_astro/${r}` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/_astro/AgentFirst.astro_astro_type_script_index_0_lang.DHglPJ15.js` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/_astro/AgentFirst.astro_astro_type_script_index_0_lang.UoJ_qKTy.js` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/_astro/AgyVcsReview.astro_astro_type_script_index_0_lang.D0rEHiEB.js` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/_astro/AnalyticsBootstrap.astro_astro_type_script_index_0_lang.BDH2WotZ.js` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/_astro/AnalyticsBootstrap.astro_astro_type_script_index_0_lang.BGtsBwJ4.js` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/_astro/AnalyticsBootstrap.astro_astro_type_script_index_0_lang.BJP2nsZu.js` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/_astro/AnalyticsBootstrap.astro_astro_type_script_index_0_lang.BmtbCzzz.js` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/_astro/AnalyticsBootstrap.astro_astro_type_script_index_0_lang.BsphJQHO.js` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/_astro/AnalyticsBootstrap.astro_astro_type_script_index_0_lang.BtyBE0kN.js` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/_astro/AnalyticsBootstrap.astro_astro_type_script_index_0_lang.CYobFwMm.js` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/_astro/AnalyticsBootstrap.astro_astro_type_script_index_0_lang.CwoqmRQ3.js` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/_astro/AnalyticsBootstrap.astro_astro_type_script_index_0_lang.D3NMMFhG.js` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/_astro/AnalyticsBootstrap.astro_astro_type_script_index_0_lang.D8G23MH0.js` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/_astro/AnalyticsBootstrap.astro_astro_type_script_index_0_lang.DQy9iQ8q.js` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/_astro/AnalyticsBootstrap.astro_astro_type_script_index_0_lang.DdOZMVll.js` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/_astro/AnalyticsBootstrap.astro_astro_type_script_index_0_lang.DeOcFNdk.js` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/_astro/AnalyticsBootstrap.astro_astro_type_script_index_0_lang.i2O0b2oB.js` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/_astro/AnalyticsBootstrap.astro_astro_type_script_index_0_lang.ksJnEz0a.js` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/_astro/AnalyticsBootstrap.astro_astro_type_script_index_0_lang.tCq0ZdPw.js` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/_astro/AnalyticsBootstrap.astro_astro_type_script_index_0_lang.ucmpGtgL.js` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/_astro/AnnouncementPill.astro_astro_type_script_index_0_lang.BK-mqr5d.js` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/_astro/AnnouncementPill.astro_astro_type_script_index_0_lang.BbFE-USi.js` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/_astro/AnnouncementPill.astro_astro_type_script_index_0_lang.CHIwXIhq.js` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/_astro/AnnouncementPill.astro_astro_type_script_index_0_lang.CRaDtBLM.js` | text/html | 131584 |  |
| 404 | GET | `https://antigravity.google/_astro/AnnouncementPill.astro_astro_type_script_index_0_lang.D0moc2f_.js` | text/html | 131584 |  |
| … | … | _1068 more in JSONL_ | … | … | … |

## 4. DATA FILES (accessible)

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 200 | GET | `https://antigravity-hub-auto-updater-974169037036.us-central1.run.app/releases` | application/json | 2847 |  |
| 200 | GET | `https://antigravity-ide-auto-updater-974169037036.us-central1.run.app/releases` | application/json | 541 |  |
| 200 | GET | `https://antigravity.google.com/assets/manifest.json` | application/json | 429 |  |
| 200 | GET | `https://antigravity.google/schemas/v1/plugin.json` | application/json | 4787 |  |
| 200 | GET | `https://antigravity.google/schemas/v1/settings.json` | application/json | 20298 |  |
| 200 | GET | `https://antigravity.google/sitemap-index.xml` | text/xml | 189 |  |
| 200 | GET | `https://antigravity.google/sitemap.xml` | text/xml | 15902 |  |
| 200 | GET | `https://api.github.com` | application/json | 2262 |  |
| 200 | GET | `https://api.github.com/repos/google-antigravity/antigravity-cli/releases?per_page=100` | application/json | 1712944 |  |

## 5. SUBDOMAINS (detailed)

Found **1**, DNS-resolved **1**.

| Host | Resolved | Source |
|---|---|---|
| `www.antigravity.google` | yes | passive |

## 6. VIRTUAL HOSTS (real statuses only)

_No non-blocked virtual hosts found._
Blocked/noisy vhost checks (403/530/0) are kept in `vhost_blocked.jsonl` (1).

## 7. JS ENDPOINTS (AST, evidence-backed)

_None extracted._

## 8. PARAMETERS

| URL | Params |
|---|---|
| `http://antigravity.google/?linkId=61956604` | linkId |
| `http://antigravity.google/?trk=public_profile__posts-text` | trk |
| `http://antigravity.google/docs/gcli-migration?hl=ar` | hl |
| `http://antigravity.google/docs/gcli-migration?hl=bn` | hl |
| `http://antigravity.google/docs/gcli-migration?hl=de` | hl |
| `http://antigravity.google/docs/gcli-migration?hl=es-419` | hl |
| `http://antigravity.google/docs/gcli-migration?hl=fa` | hl |
| `http://antigravity.google/docs/gcli-migration?hl=he` | hl |
| `http://antigravity.google/docs/gcli-migration?hl=hi` | hl |
| `http://antigravity.google/docs/gcli-migration?hl=id` | hl |
| `http://antigravity.google/docs/gcli-migration?hl=ko` | hl |
| `http://antigravity.google/docs/gcli-migration?hl=pl` | hl |
| `http://antigravity.google/docs/gcli-migration?hl=pt-br` | hl |
| `http://antigravity.google/docs/gcli-migration?hl=th` | hl |
| `http://antigravity.google/docs/gcli-migration?hl=tr` | hl |
| `http://antigravity.google/docs/gcli-migration?hl=vi` | hl |
| `http://antigravity.google/docs/gcli-migration?hl=zh-tw` | hl |
| `http://antigravity.google/download?trk=article-ssr-frontend-pulse_little-text-block` | trk |
| `https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fantigravity.google.com%2F&ec=GAZAgQY&followup=https%3A%2F%2Fantigravity.google.com%2F&passive=1209600&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-349897383%3A1795372128128426` | continue, dsh, ec, flowEntry, flowName, followup, passive |
| `https://antigravity.google/?_gl=1%2A1954lpy%2A_up%2AMQ..%2A_ga%2ANzYzNjM2MDI0LjE3ODc4NzE3Njk.%2A_ga_47V54ZJ3EV%2AczE3ODc4NzE3NjgkbzEkZzAkdDE3ODc4NzE3NjkkajU5JGwwJGgw` | _gl |
| `https://antigravity.google/?_gl=1%2A1a6i0vg%2A_up%2AMQ..%2A_ga%2AMTQxMTU2ODY2My4xNzgzOTI4OTcw%2A_ga_47V54ZJ3EV%2AczE3ODM5Mjg5NjkkbzEkZzAkdDE3ODM5Mjg5NjkkajYwJGwwJGgw` | _gl |
| `https://antigravity.google/?_gl=1%2A1fqz6ni%2A_up%2AMQ..%2A_ga%2AMTg4NzUxODgwMi4xNzYzNTIwMTI1%2A_ga_47V54ZJ3EV%2AczE3NjM1MjAxMjUkbzEkZzAkdDE3NjM1MjAxMjUkajYwJGwwJGgw` | _gl |
| `https://antigravity.google/?_gl=1%2A1nlfw67%2A_up%2AMQ..%2A_ga%2AMTIzMTAxNDYwNi4xNzYzNzgzMTA3%2A_ga_47V54ZJ3EV%2AczE3NjM3ODMxMDYkbzEkZzAkdDE3NjM3ODMxMDYkajYwJGwwJGgw` | _gl |
| `https://antigravity.google/?_gl=1%2A1nyr9s%2A_up%2AMQ..%2A_ga%2AMTk2MDk3NTQzNS4xNzgzOTI4OTIx%2A_ga_47V54ZJ3EV%2AczE3ODM5Mjg5MjEkbzEkZzAkdDE3ODM5Mjg5MjEkajYwJGwwJGgw` | _gl |
| `https://antigravity.google/?_gl=1%2A1te360h%2A_up%2AMQ..%2A_ga%2AMTc4ODEzNDMyMS4xNzgzMTMzNjk0%2A_ga_47V54ZJ3EV%2AczE3ODMxMzM2OTQkbzEkZzAkdDE3ODMxMzM2OTQkajYwJGwwJGgw` | _gl |
| `https://antigravity.google/?_gl=1%2Afeecck%2A_up%2AMQ..%2A_ga%2AMTk5NTgyNzYzNi4xNzc5MjE3MTQ4%2A_ga_47V54ZJ3EV%2AczE3NzkyMTcxNDgkbzEkZzAkdDE3NzkyMTcxNDgkajYwJGwwJGgw` | _gl |
| `https://antigravity.google/?_gl=1%2Afpohs0%2A_up%2AMQ..%2A_ga%2AMTg0Mjc0NjE1MC4xNzY0OTE3MjYx%2A_ga_47V54ZJ3EV%2AczE3NjQ5MTcyNjAkbzEkZzAkdDE3NjQ5MTcyNjAkajYwJGwwJGgw` | _gl |
| `https://antigravity.google/?_gl=1%2Aihpy36%2A_up%2AMQ..%2A_ga%2AMTI4Nzc0MzY5Mi4xNzgyMDM0MzM1%2A_ga_47V54ZJ3EV%2AczE3ODIwMzQzMzQkbzEkZzAkdDE3ODIwMzQzMzQkajYwJGwwJGgw` | _gl |
| `https://antigravity.google/?_gl=1%2Atxt6l8%2A_up%2AMQ..%2A_ga%2AMTAyOTg4NDMyMS4xNzc5MzcwNDYw%2A_ga_2N64Y1V9L3%2AczE3NzkzNzA0NTkkbzEkZzAkdDE3NzkzNzA0NTkkajYwJGwwJGgw` | _gl |
| `https://antigravity.google/?_gl=1%2Axipp0p%2A_up%2AMQ..%2A_ga%2AMTA1OTQwMDk2MS4xNzc5NTk2NDAw%2A_ga_47V54ZJ3EV%2AczE3Nzk1OTY0MDAkbzEkZzAkdDE3Nzk1OTY0MDAkajYwJGwwJGgw` | _gl |
| `https://antigravity.google/?_hsenc=p2ANqtz-8Tkmw9I0UeqoSjr86NGmBAeCO2T354wd9Qx4OaF7BX3fU778pY-magiSg6zmuCQYRaDRi4` | _hsenc |
| `https://antigravity.google/?amp=` | amp |
| `https://antigravity.google/?app=antigravity` | app |
| `https://antigravity.google/?app=antigravity-ide` | app |
| `https://antigravity.google/?authuser=0` | authuser |
| `https://antigravity.google/?authuser=0&%3Bhl=pt-br&hl=pt-br` | ;hl, authuser, hl |
| `https://antigravity.google/?authuser=0&%3Bhl=tr&hl=tr` | ;hl, authuser, hl |
| `https://antigravity.google/?authuser=0&hl=ar` | authuser, hl |
| `https://antigravity.google/?authuser=0&hl=bn` | authuser, hl |
| `https://antigravity.google/?authuser=0&hl=de` | authuser, hl |
| `https://antigravity.google/?authuser=0&hl=es` | authuser, hl |
| `https://antigravity.google/?authuser=0&hl=es-419` | authuser, hl |
| `https://antigravity.google/?authuser=0&hl=fa` | authuser, hl |
| `https://antigravity.google/?authuser=0&hl=fr` | authuser, hl |
| `https://antigravity.google/?authuser=0&hl=he` | authuser, hl |
| `https://antigravity.google/?authuser=0&hl=hi` | authuser, hl |
| `https://antigravity.google/?authuser=0&hl=id` | authuser, hl |
| `https://antigravity.google/?authuser=0&hl=it` | authuser, hl |
| `https://antigravity.google/?authuser=0&hl=ja` | authuser, hl |
| `https://antigravity.google/?authuser=0&hl=ko` | authuser, hl |
| `https://antigravity.google/?authuser=0&hl=pl` | authuser, hl |
| `https://antigravity.google/?authuser=0&hl=pt` | authuser, hl |
| `https://antigravity.google/?authuser=0&hl=pt-br` | authuser, hl |
| `https://antigravity.google/?authuser=0&hl=ru` | authuser, hl |
| `https://antigravity.google/?authuser=0&hl=th` | authuser, hl |
| `https://antigravity.google/?authuser=0&hl=tr` | authuser, hl |
| `https://antigravity.google/?authuser=0&hl=vi` | authuser, hl |
| `https://antigravity.google/?authuser=0&hl=zh-cn` | authuser, hl |
| `https://antigravity.google/?authuser=0&hl=zh-tw` | authuser, hl |
| `https://antigravity.google/?authuser=0&prompt=consent&state=aHb_VrydYlcsXKfTAG937w&iss=https%3A%2F%2Faccounts.google.com&code=4%2F0AeoWuM9Xcm4n2nmuTbGmTzE28jrVZ7kc2yr9Or8HAhhcxGiQKt7Fq3hds0evPIKEhXQBVw&scope=email+profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcloud-platform+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcclog+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fexperimentsandconfigs+openid` | authuser, code, iss, prompt, scope, state |

## 9. SECRET CANDIDATES

1 candidate(s) in `secrets.jsonl`. Verify manually.

## 10. TOOL RUN STATUS (no silent skips)

| Tool | Result | Detail |
|---|---|---|
| `anastasis` | exit 254 | no output produced — see logs/ |
| `dnsx` | OK | completed |
| `ffuf` | OK | off by choice — wordlist prepared |
| `gau` | OK | completed |
| `gospider` | OK | completed |
| `httpx` | OK | completed |
| `js-download` | OK | 89 chunks saved over 3 round(s) |
| `jscope` | OK | completed |
| `jsluice` | OK | 89 files parsed |
| `katana` | OK | completed |
| `methods` | OK | 1400 method responses |
| `subfinder` | OK | completed |
| `trufflehog` | OK | completed |
| `uncover` | OK | no API key configured — no external data |
| `urlfinder` | OK | completed |
| `uro` | OK | completed |
| `vhost` | OK | 0 real of 1 tested |
| `x8` | OK | parameter scan complete |

## 11. INTENTIONALLY NOT RUN

- **ffuf path brute** — off by default; `wordlist.txt` is ready. Set `enable_brute: true` later.
- **kiterunner** — off by default alongside ffuf.

## 12. OUTPUT FILES

| File | Meaning |
|---|---|
| [`all_routes.jsonl`](all_routes.jsonl) | every route, unfiltered (787,048 B) |
| [`accessible_200.jsonl`](accessible_200.jsonl) | HTTP 200 wins (308,954 B) |
| [`exists_blocked.jsonl`](exists_blocked.jsonl) | exists but blocked (7,113 B) |
| [`other_status.jsonl`](other_status.jsonl) | all other statuses (1,101,221 B) |
| [`data_files.jsonl`](data_files.jsonl) | JSON/CSV/XML among 200s (7,611 B) |
| [`params.jsonl`](params.jsonl) | parameters (336,423 B) |
| [`subdomains.jsonl`](subdomains.jsonl) | subdomains + resolution (84 B) |
| [`third_party_routes.jsonl`](third_party_routes.jsonl) | third-party URLs — kept, not deleted (6,285 B) |
| [`method_responses.jsonl`](method_responses.jsonl) | all method-probe responses — kept (238,821 B) |
| [`vhost_real.jsonl`](vhost_real.jsonl) | non-blocked virtual hosts (0 B) |
| [`vhost_blocked.jsonl`](vhost_blocked.jsonl) | blocked vhost checks — kept (55 B) |
| [`js_endpoints.jsonl`](js_endpoints.jsonl) | AST endpoints (0 B) |
| [`vhost.jsonl`](vhost.jsonl) | all vhost checks (55 B) |
| [`jsluice.jsonl`](jsluice.jsonl) | JS-derived URLs (45,418 B) |
| [`gospider.txt`](gospider.txt) | second crawler URLs (52,523 B) |
| [`jscope.txt`](jscope.txt) | evidence-ranked JS analysis (9,538 B) |
| [`secrets.jsonl`](secrets.jsonl) | secret candidates (745 B) |
| [`wordlist.txt`](wordlist.txt) | target-specific fuzz list (182,610 B) |
| [`params.txt`](params.txt) | parameter wordlist (418 B) |
| [`js_urls.txt`](js_urls.txt) | JS chunk URLs (7,042 B) |
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