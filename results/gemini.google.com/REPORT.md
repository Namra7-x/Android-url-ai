# Hunt Report — https://gemini.google.com

Generated: 2026-11-22T20:53:02Z &nbsp;|&nbsp; Duration: 148m 31s

> **Nothing is filtered during collection. This report is only a grouping.**

## Summary

| What | Count | Meaning |
|---|---:|---|
| Routes collected | 3634 | Every URL found, nothing removed |
| Distinct routes verified | 648 | One row per URL (method probes excluded) |
| HTTP responses | 750 | Includes method probes — kept in `method_responses.jsonl` |
| **Accessible (200)** | **14** | Confirmed live — the wins |
| Exists but different status | 562 | 301/302/401/403/405 — real route, blocked |
| Other responses | 72 | 404/500/etc — kept, not discarded |
| Subdomains (resolved) | 4 | DNS-verified |
| Virtual hosts (real) | 1 | Cloudflare 403/530/0 excluded |
| Parameters | 3041 | URLs with query params |
| JS endpoints (AST) | 0 | anastasis evidence-backed |
| First-party URLs | 1640 | gemini.google.com and subdomains |
| Third-party URLs | 1994 | kept in `third_party_routes.jsonl` |
| Method responses | 119 | kept in `method_responses.jsonl` |
| Blocked vhost checks | 3 | kept in `vhost_blocked.jsonl` |
| Secret candidates | 0 | verify manually |

> Collection keeps third-party URLs by design (1994). See `third_party_routes.jsonl`. Method-probe responses are in `method_responses.jsonl`.

## 1. SUCCESS — HTTP 200

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 200 | GET | `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Den-IN&dsh=S118289191%3A1795380176073259&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Den-IN&hl=en-IN&osid=1&TL=AAxq8nuPH_VR_VaZmXIy_5BJmBXx2S-QdCIZsfdKuhzhy2R45Lr5hAL_yAYCZLjk` | text/html | 1027360 |  |
| 200 | GET | `https://accounts.google.com/signin/v2/usernamerecovery?continue=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Den-IN&dsh=S118289191%3A1795380176073259&ec=GAZAkgU&flowEntry=ServiceLogin&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Den-IN&hl=en-IN&osid=1` | text/html | 3767750 |  |
| 200 | GET | `https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dar-EG&ec=GAZAkgU&followup=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dar-EG&hl=ar-EG&osid=1&passive=1209600&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-1508547457%3A1795380172567026` | text/html | 1265670 |  |
| 200 | GET | `https://ad.doubleclick.net/activity` | image/gif | 42 |  |
| 200 | GET | `https://apis.google.com/js/api.js` | text/javascript | 14576 |  |
| 200 | GET | `https://apis.google.com/js/client.js` | text/javascript | 14582 |  |
| 200 | GET | `https://facebook.com/tr` | text/plain | 0 |  |
| 200 | GET | `https://fonts.gstatic.com/s/e/notoemoji/search/wrapper.js` | text/javascript | 157348 |  |
| 200 | GET | `https://google.com/ccm/geo` | application/json | 75 |  |
| 200 | GET | `https://googletagmanager.com/gtag/js` | application/javascript | 242154 |  |
| 200 | GET | `https://googletagmanager.com/gtm.js?id=GTM-KKRLL9S` | application/javascript | 536694 |  |
| 200 | GET | `https://labs.google` | text/html | 282879 |  |
| 200 | GET | `https://maps.googleapis.com/maps/api/js` | text/javascript | 325010 |  |
| 200 | GET | `https://translate.google.com/translate_a/element.js` | text/javascript | 3594 |  |

## 2. EXISTS BUT DIFFERENT STATUS (301/302/401/403/405)

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 302 | GET | `https://accounts.google.com/ServiceLogin?passive=1209600` | application/binary | 0 |  |
| 301 | GET | `https://ad.doubleclick.net` | text/html | 251 |  |
| 302 | GET | `https://ads.google.com` | application/binary | 0 |  |
| 302 | GET | `https://adservice.google.com/pagead/regclk` | text/html | 0 |  |
| 301 | GET | `https://apis.google.com` | text/html | 226 |  |
| 301 | GET | `https://bid.g.doubleclick.net` | text/html | 251 |  |
| 405 | GET | `https://content-push.googleapis.com/upload` | text/plain | 18 |  |
| 405 | GET | `https://csp.withgoogle.com/csp/proto/BardChatUi` | text/html | 1695 |  |
| 403 | GET | `https://docs.google.com/picker/v2/home` | text/html | 1658 |  |
| 302 | GET | `https://enterprise.gemini.google.com` | application/binary | 0 |  |
| 302 | GET | `https://gemini.google.com` | text/html | 388 |  |
| 302 | GET | `https://gemini.google.com/?android-min-version%5Cu003d301356232%5Cu0026ios-min-version%5Cu003d322.0%5Cu0026is_sa%5Cu003d1%5Cu0026campaign_id%5Cu003dmweb_upsell_android%5Cu0026utm_source%5Cu003dmweb_upsell%5Cu0026utm_medium%5Cu003dproduct_promo%5Cu0026utm_campaign%5Cu003dmweb_upsell_android%5Cu0026pt%5Cu003d9008%5Cu0026mt%5Cu003d8%5Cu0026ct%5Cu003dp-growth-product-mweb-upsell%5C=` | text/html | 785 |  |
| 302 | GET | `https://gemini.google.com/?android-min-version=301356232&ios-min-version=322.0&is_sa=1&campaign_id=in_promptflow_1_autosubmit&pt=9008&mt=8&ct=in_promptflow&prompt_id=FqMVF4htt60C&prompt_action=autosubmit` | text/html | 599 |  |
| 302 | GET | `https://gemini.google.com/?hl=ar` | text/html | 406 |  |
| 302 | GET | `https://gemini.google.com/?lfhs=2` | text/html | 397 |  |
| 302 | GET | `https://gemini.google.com/?utm_medium%5Cu003dproduct_promo%5Cu0026utm_source%5Cu003dmarketing_led_banner%5Cu0026utm_campaign%5Cu003dmweb_upsell_banner%5Cu0026campaign_id%5Cu003dmweb_upsell_banner%5C=` | text/html | 581 |  |
| 302 | GET | `https://gemini.google.com/?utm_source%5Cu003dmarketing_led_disco_card%5Cu0026utm_medium%5Cu003dproduct_promo%5Cu0026utm_campaign%5Cu003dmweb_upsell_interstitial_1_lo%5Cu0026campaign_id%5Cu003dmweb_upsell_interstitial_1_lo%5C=` | text/html | 605 |  |
| 302 | GET | `https://gemini.google.com/?utm_source%5Cu003dmarketing_led_disco_card%5Cu0026utm_medium%5Cu003dproduct_promo%5Cu0026utm_campaign%5Cu003dmweb_upsell_interstitial_2_lo%5Cu0026campaign_id%5Cu003dmweb_upsell_interstitial_2_lo%5C=` | text/html | 607 |  |
| 302 | GET | `https://gemini.google.com/Edg` | text/html | 389 |  |
| 302 | GET | `https://gemini.google.com/\` | text/html | 391 |  |
| 302 | GET | `https://gemini.google.com/\u003e\u003col\u003e\u003cli\u003e\u003cstrong\u003eRemove` | text/html | 474 |  |
| 302 | GET | `https://gemini.google.com/\u003e\u003ctable\u003e\u003cthead\u003e\u003ctr\u003e\u003cth\u003eBook\u003c/th\u003e\u003cth\u003eAuthor\u003c/th\u003e\u003cth\u003eYear\u003c/th\u003e\u003cth\u003eDescription\u003c/th\u003e\u003c/tr\u003e\u003c/thead\u003e\u003ctbody\u003e\u003ctr\u003e\u003ctd\u003e\u003c/td\u003e\u003ctd\u003e\u003c/td\u003e\u003ctd\u003e\u003c/td\u003e\u003ctd\u003e\u003c/td\u003e\u003c/tr\u003e\u003c/tbody\u003e\u003c/table\u003e` | text/html | 1026 |  |
| 302 | GET | `https://gemini.google.com/_/BardChatUi` | text/html | 398 |  |
| 302 | GET | `https://gemini.google.com/_/BardChatUi/cspreport/fine-allowlist` | text/html | 425 |  |
| 302 | GET | `https://gemini.google.com/_/BardChatUi/data/batchexecute?rpcids=otAQ7b` | text/html | 434 |  |
| 302 | GET | `https://gemini.google.com/_/BardChatUi/manifest.json` | text/html | 412 |  |
| 302 | GET | `https://gemini.google.com/_/bscframe` | text/html | 398 |  |
| 302 | GET | `https://gemini.google.com/_/service_worker` | text/html | 404 |  |
| 302 | GET | `https://gemini.google.com/a?v=3&t=l` | text/html | 405 |  |
| 302 | GET | `https://gemini.google.com/ag/g/c` | text/html | 392 |  |
| 302 | GET | `https://gemini.google.com/agent\` | text/html | 396 |  |
| 302 | GET | `https://gemini.google.com/ai-resume-builder` | text/html | 403 |  |
| 302 | GET | `https://gemini.google.com/ai-travel-planner` | text/html | 405 |  |
| 302 | GET | `https://gemini.google.com/analytics.js` | text/html | 400 |  |
| 302 | GET | `https://gemini.google.com/app/download/mobile?android-min-version=` | text/html | 432 |  |
| 302 | GET | `https://gemini.google.com/app/download?hl=ar` | text/html | 420 |  |
| 302 | GET | `https://gemini.google.com/app?android-min-version=301779666&is_sa=1&campaign_id=in_kbcquiz_2026_paid_universal_autosubmit&pt=9008&mt=8&ct=in_kbc_quiz&prompt_id=GPRwkjZsxsfF&prompt_action=autosubmit&redirect=home` | text/html | 609 |  |
| 302 | GET | `https://gemini.google.com/app?campaign=career_resumes` | text/html | 417 |  |
| 302 | GET | `https://gemini.google.com/app?hl=ar` | text/html | 409 |  |
| 302 | GET | `https://gemini.google.com/app?hl=de&target=images&nav_id=arcade` | text/html | 445 |  |
| 302 | GET | `https://gemini.google.com/as` | text/html | 390 |  |
| 302 | GET | `https://gemini.google.com/as/d` | text/html | 390 |  |
| 302 | GET | `https://gemini.google.com/as/d/ccm/conversion` | text/html | 407 |  |
| 302 | GET | `https://gemini.google.com/as/p/c` | text/html | 394 |  |
| 302 | GET | `https://gemini.google.com/campaign/daily-habits` | text/html | 409 |  |
| 302 | GET | `https://gemini.google.com/campaign/happydiwali?hl=en-IN` | text/html | 432 |  |
| 302 | GET | `https://gemini.google.com/campaign/kbcquiz?hl=en-IN` | text/html | 430 |  |
| 302 | GET | `https://gemini.google.com/ccm/collect` | text/html | 399 |  |
| 302 | GET | `https://gemini.google.com/ccm/conversion` | text/html | 402 |  |
| 302 | GET | `https://gemini.google.com/ccm/form-data` | text/html | 401 |  |
| 302 | GET | `https://gemini.google.com/ccm/s/collect` | text/html | 401 |  |
| 302 | GET | `https://gemini.google.com/chat` | text/html | 392 |  |
| 302 | GET | `https://gemini.google.com/chrome__glic_api.js` | text/html | 405 |  |
| 302 | GET | `https://gemini.google.com/d` | text/html | 389 |  |
| 302 | GET | `https://gemini.google.com/d/ccm/form-data` | text/html | 403 |  |
| 302 | GET | `https://gemini.google.com/ddm/activity` | text/html | 398 |  |
| 302 | GET | `https://gemini.google.com/debug/bootstrap?id=` | text/html | 409 |  |
| 302 | GET | `https://gemini.google.com/download` | text/html | 394 |  |
| 302 | GET | `https://gemini.google.com/faq?hl%3Den-IN%26google_abuse%3DGOOGLE_ABUSE_EXEMPTION%253DID%253D4fa84df6e769c3a6%3ATM%253D1795379928%3AC%253D%253E%3AIP%253D132.196.21.183-%3AS%253Dl62GLfd4_3qkxvz11P1kSQ=` | text/html | 593 |  |
| 302 | GET | `https://gemini.google.com/faq?hl%3Des-ES%26google_abuse%3DGOOGLE_ABUSE_EXEMPTION%253DID%253D93675d763b6c477b%3ATM%253D1795379929%3AC%253D%253E%3AIP%253D132.196.21.183-%3AS%253DrhShFow2Kg7vI4fLD0kpxQ=` | text/html | 593 |  |
| 302 | GET | `https://gemini.google.com/faq?hl%3Did%26google_abuse%3DGOOGLE_ABUSE_EXEMPTION%253DID%253D179b830a042456e7%3ATM%253D1795379936%3AC%253D%253E%3AIP%253D132.196.21.183-%3AS%253DF4U6J3I4J8QMnrNY4oMokQ=` | text/html | 590 |  |
| 302 | GET | `https://gemini.google.com/faq?hl%3Diw%26google_abuse%3DGOOGLE_ABUSE_EXEMPTION%253DID%253D4e76d2691d028072%3ATM%253D1795379936%3AC%253D%253E%3AIP%253D132.196.21.183-%3AS%253De5CVlWmJSjxqHbcw92mcbw=` | text/html | 590 |  |
| 302 | GET | `https://gemini.google.com/faq?hl=ar` | text/html | 409 |  |
| 302 | GET | `https://gemini.google.com/faq?hl=en-IN&google_abuse=GOOGLE_ABUSE_EXEMPTION%3DID%3D4fa84df6e769c3a6%3ATM%3D1795379928%3AC%3D%3E%3AIP%3D132.196.21.183-%3AS%3Dl62GLfd4_3qkxvz11P1kSQ%3B+path%3D%2F%3B+domain%3Dgoogle.com%3B+expires%3DSun` | text/html | 235 |  |
| 302 | GET | `https://gemini.google.com/g` | text/html | 389 |  |
| 302 | GET | `https://gemini.google.com/g/collect` | text/html | 397 |  |
| 302 | GET | `https://gemini.google.com/g/d` | text/html | 391 |  |
| 302 | GET | `https://gemini.google.com/g/d/ccm/conversion` | text/html | 404 |  |
| 302 | GET | `https://gemini.google.com/ga/g/c` | text/html | 392 |  |
| 302 | GET | `https://gemini.google.com/gci_91f30755d6a6b787dcc2a4062e6e9824.js` | text/html | 425 |  |
| 302 | GET | `https://gemini.google.com/gemini/download/mobile` | text/html | 410 |  |
| 302 | GET | `https://gemini.google.com/gs` | text/html | 390 |  |
| 302 | GET | `https://gemini.google.com/gs/ccm/conversion` | text/html | 403 |  |
| 302 | GET | `https://gemini.google.com/gtag/destination` | text/html | 404 |  |
| 302 | GET | `https://gemini.google.com/gtag/js` | text/html | 393 |  |
| … | … | _487 more in JSONL_ | … | … | … |

## 3. OTHER RESPONSES — kept, never discarded

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 400 | GET | `https://*.fls.doubleclick.net` | text/html | 1555 |  |
| 400 | GET | `https://*.googleapis.com` | text/html | 1555 |  |
| 400 | GET | `https://*.googleusercontent.com` | text/html | 1555 |  |
| 400 | GET | `https://*.scf.usercontent.goog` | text/html | 1555 |  |
| 404 | GET | `https://ade.googlesyndication.com` | text/html | 1561 |  |
| 404 | GET | `https://adservice.google.com` | text/html | 1561 |  |
| 404 | GET | `https://apis.google.com/_/scs/abc-static/_/js` | text/html | 0 |  |
| 404 | GET | `https://bard.datacommons.org` |  | 0 |  |
| 502 | GET | `https://cct.google/taggy/agent.js` | text/html | 1613 |  |
| 404 | GET | `https://displayads-formats-qa-devel-sandbox.googleusercontent.com` | text/html | 1621 |  |
| 404 | GET | `https://displayads-formats.googleusercontent.com` | text/html | 1621 |  |
| 404 | GET | `https://enterprise-autopush.gemini.google.com` | text/html | 1561 |  |
| 404 | GET | `https://enterprise-staging.gemini.google.com` | text/html | 1561 |  |
| 404 | GET | `https://fonts.googleapis.com` | text/html | 1621 |  |
| 404 | GET | `https://fonts.gstatic.com` | text/html | 1561 |  |
| 204 | GET | `https://gemini.google.com/generate_204?-XM-zg=` |  | 0 |  |
| 204 | GET | `https://gemini.google.com/generate_204?22L3zw=` |  | 0 |  |
| 204 | GET | `https://gemini.google.com/generate_204?80RvHg=` |  | 0 |  |
| 204 | GET | `https://gemini.google.com/generate_204?E6EN7g=` |  | 0 |  |
| 204 | GET | `https://gemini.google.com/generate_204?IF79QA=` |  | 0 |  |
| 204 | GET | `https://gemini.google.com/generate_204?J8pAsQ=` |  | 0 |  |
| 204 | GET | `https://gemini.google.com/generate_204?LvDPgA=` |  | 0 |  |
| 204 | GET | `https://gemini.google.com/generate_204?PErePA=` |  | 0 |  |
| 204 | GET | `https://gemini.google.com/generate_204?PNesOw=` |  | 0 |  |
| 204 | GET | `https://gemini.google.com/generate_204?V5m5Zw=` |  | 0 |  |
| 204 | GET | `https://gemini.google.com/generate_204?eT4dmg=` |  | 0 |  |
| 204 | GET | `https://gemini.google.com/generate_204?fELM1g=` |  | 0 |  |
| 204 | GET | `https://gemini.google.com/generate_204?kDVA3w=` |  | 0 |  |
| 204 | GET | `https://gemini.google.com/generate_204?lKU5WA=` |  | 0 |  |
| 204 | GET | `https://gemini.google.com/generate_204?spTYWw=` |  | 0 |  |
| 204 | GET | `https://gemini.google.com/generate_204?t--L_A=` |  | 0 |  |
| 204 | GET | `https://gemini.google.com/generate_204?wssRNQ=` |  | 0 |  |
| 204 | GET | `https://gemini.google.com/generate_204?zqNVOQ=` |  | 0 |  |
| 404 | GET | `https://gemini.gstatic.com` | text/html | 1561 |  |
| 404 | GET | `https://gemini.gstatic.com/_/mss/boq-gemini-web-uiserver/_/js/k=boq-gemini-web-uiserver.BardChatUi.en_US.njWOIJ0_mRU.2018.O` | text/html | 1657 |  |
| 404 | GET | `https://gemini.gstatic.com/_/mss/boq-gemini-web-uiserver/_/js/k=boq-gemini-web-uiserver.BardChatUi.en_US.njWOIJ0_mRU.2018.O/am=hG8EQBH7AKzz98Ht_kl0oAEJKAJygiB0AQAAAACE/d=1/excm=_b/ed=1/dg=0/br=1/wt=2/ujg=1/rs=AKrAJMotU2mX7mAqBP-h2uy69id1zC0OEw/ee=EmZ2Bf:zr1jrb` | text/html | 1794 |  |
| 404 | GET | `https://gemini.gstatic.com/_/mss/boq-gemini-web-uiserver/_/js/k=boq-gemini-web-uiserver.BardChatUi.en_US.njWOIJ0_mRU.2018.O/ck=boq-gemini-web-uiserver.BardChatUi._dvMYtqox70.L.B1.O/am=hG8EQBH7AKzz98Ht_kl0oAEJKAJygiB0AQAAAACE/d=1/exm=_b/excm=_b/ed=1/br=1/wt=2/ujg=1/rs=AKrAJMpFWwxzPcitO-MDar0trSRQDrWXUw/ee=EmZ2Bf:zr1jrb` | text/html | 1853 |  |
| 404 | GET | `https://gemini.gstatic.com/_/mss/boq-gemini-web-uiserver/_/js/k=boq-gemini-web-uiserver.BardChatUi.en_US.njWOIJ0_mRU.2018.O/ck=boq-gemini-web-uiserver.BardChatUi._dvMYtqox70.L.B1.O/am=hG8EQBH7AKzz_8Ht_kl0oAEJKAJygiB0AQAAAACE/d=1/exm=_b/excm=_b/ed=1/wt=2/ujg=1/rs=AKrAJMqECJb0C0z4O2y6uchUMT3tXu2z3A/ee=EmZ2Bf:zr1jrb` | text/html | 1848 |  |
| 404 | GET | `https://google.com/gmp/conversion` | text/html | 1575 |  |
| 404 | GET | `https://google.com/js/bg` | text/html | 1566 |  |
| 404 | GET | `https://google.com/tools/feedback` | text/html | 1575 |  |
| 404 | GET | `https://google.com/tools/feedback/activate.js` | text/html | 1587 |  |
| 404 | GET | `https://google.com/tools/feedback/chat_load.js` | text/html | 1588 |  |
| 404 | GET | `https://google.com/tools/feedback/help_api.js` | text/html | 1587 |  |
| 404 | GET | `https://google.com/tools/feedback/load.js` | text/html | 1583 |  |
| 404 | GET | `https://google.com/tools/feedback/open.js` | text/html | 1583 |  |
| 404 | GET | `https://google.com/tools/feedback/open_to_help_guide_lazy.js` | text/html | 1602 |  |
| 404 | GET | `https://googleadservices.com` | text/html | 1561 |  |
| 404 | GET | `https://googleadservices.com/pagead/conversion` | text/html | 1578 |  |
| 404 | GET | `https://googletagmanager.com` | text/html | 1561 |  |
| 400 | GET | `https://googletagmanager.com/gtag/destination` | text/html | 1555 |  |
| 404 | GET | `https://googletagmanager.com/static/service_worker` | text/html | 1582 |  |
| 400 | GET | `https://lh3.googleusercontent.com` | text/html | 1555 |  |
| 404 | GET | `https://maps.googleapis.com/maps-api-v3/api/js` | text/html | 1579 |  |
| 404 | GET | `https://maps.googleapis.com/maps/api/place/js` | text/html | 1578 |  |
| 400 | GET | `https://maps.googleapis.com/maps/vt` | text/html | 1555 |  |
| 404 | GET | `https://ogads-pa.clients6.google.com` | text/html | 1652 |  |
| 404 | GET | `https://ogads-pa.googleapis.com` | text/html | 1652 |  |
| 404 | GET | `https://ogs.google.com` | text/html | 1561 |  |
| 404 | GET | `https://onegoogle-autopush.sandbox.google.com` | text/html | 1561 |  |
| 404 | GET | `https://onegoogle-staging.sandbox.google.com` | text/html | 1561 |  |
| 404 | GET | `https://pagead2.googlesyndication.com` | text/html | 1561 |  |
| 404 | GET | `https://ssl.gstatic.com` | text/html | 1561 |  |
| 400 | GET | `https://storage.googleapis.com` | application/xml | 181 |  |
| 404 | GET | `https://studio.firebase.google.com/run.api` | text/html | 171 |  |
| 404 | GET | `https://support.google.com/inapp` | text/html | 1566 |  |
| 404 | GET | `https://td.doubleclick.net` | text/html | 1561 |  |
| 404 | GET | `https://tpc.googlesyndication.com` | text/html | 1561 |  |
| 404 | GET | `https://translate.googleapis.com/_/translate_http/_/js` | text/html | 1582 |  |
| 404 | GET | `https://waa-pa.clients6.google.com` | text/html | 1561 |  |
| 404 | GET | `https://www-onepick-opensocial.googleusercontent.com/gadgets/js/rpc.js` | text/html | 134 |  |
| 404 | GET | `https://youtube-nocookie.com` | text/html | 7046 |  |

## 4. DATA FILES (accessible)

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 200 | GET | `https://google.com/ccm/geo` | application/json | 75 |  |

## 5. SUBDOMAINS (detailed)

Found **4**, DNS-resolved **4**.

| Host | Resolved | Source |
|---|---|---|
| `enterprise-autopush.gemini.google.com` | yes | passive |
| `enterprise-staging.gemini.google.com` | yes | passive |
| `enterprise.gemini.google.com` | yes | passive |
| `lti.gemini.google.com` | yes | passive |

## 6. VIRTUAL HOSTS (real statuses only)

| Host | Status |
|---|---|
| `enterprise.gemini.google.com` | 302 |
Blocked/noisy vhost checks (403/530/0) are kept in `vhost_blocked.jsonl` (3).

## 7. JS ENDPOINTS (AST, evidence-backed)

_None extracted._

## 8. PARAMETERS

| URL | Params |
|---|---|
| `https://accounts.google.com/ServiceLogin?passive=1209600` | passive |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dbn&dsh=S-736926615%3A1795380176808090&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dbn&hl=bn&osid=1&TL=AAxq8nslJXexqfvNeqqDioX4ifa4BQWcYgsFj6JzNZlZ5hBFySb-N3Z6CnznfNG-` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Den-IN&dsh=S118289191%3A1795380176073259&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Den-IN&hl=en-IN&osid=1&TL=AAxq8nuPH_VR_VaZmXIy_5BJmBXx2S-QdCIZsfdKuhzhy2R45Lr5hAL_yAYCZLjk` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dfa&dsh=S1228695011%3A1795380182377596&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dfa&hl=fa&osid=1&TL=AAxq8ntesM3FOjPu3aMEvx4JWlKJ246s_aK3DEgoTWlrdRh2L_mC9QlsGd6KcR6Y` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dfi&dsh=S1228695011%3A1795380188431581&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dfi&hl=fi&osid=1&TL=AAxq8nvGXQvfK2QgJa8pTjDtqaXjaylI-X4xDPchexYIXAv2fuImleFfpWpwdbIE` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dfr&dsh=S-1508547457%3A1795380183291578&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dfr&hl=fr&osid=1&TL=AAxq8ntg8dlOaJ7k3cU6HOi9XX1vQxMLfB4c3jrEPko2fTWYSM5qL6tPPzEXbGNs` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dfr-CA&dsh=S118289191%3A1795380180635813&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dfr-CA&hl=fr-CA&osid=1&TL=AAxq8ntKfsu7Zl6mFPw1RsgA2lfT9CGFgPC1gSMZWlgnq0lsNxPWJkuoOq_TnEbL` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dhi&dsh=S-736926615%3A1795380187845898&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dhi&hl=hi&osid=1&TL=AAxq8nvUcI14unSlsqe0I8YdTCaFoKv2jDX2cAMmiL2rGGoDZwYi5tKGfIu6YZSd` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dhu&dsh=S-736926615%3A1795380184555821&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dhu&hl=hu&osid=1&TL=AAxq8ntaY7VQI0qSgMdIiUWcMPlzpSclB04ya5SKyh6zvMTQlLdkLDCcJA2CDWH9` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dit&dsh=S-736926615%3A1795380181720042&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dit&hl=it&osid=1&TL=AAxq8ntIs2CyrRkPt6H2d32TXV1J2Uu7QhVEi_nXn8Jb_1rJXqKPDQz-Hy4UBHHf` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Diw&dsh=S118289191%3A1795380181960309&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Diw&hl=iw&osid=1&TL=AAxq8ntgVItG0LsJP1x79gwphnF0oD0LO78iqpVmkmrHF3QKVJMrGrGvO4Ctbl5X` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dlt&dsh=S-1508547457%3A1795380190779767&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dlt&hl=lt&osid=1&TL=AAxq8nvYOs3pkfigj4BMzqbxw8oVhmE0ly1UkFFUv3ip4QFH-MzrylnscqNxyeRQ` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dlv&dsh=S118289191%3A1795380189033766&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dlv&hl=lv&osid=1&TL=AAxq8nun7TntLgjEIBLdAULsktVjYE_tqBeeevX3e7MZ-6Bk4DkRwil2TI62AzdC` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dml&dsh=S-1508547457%3A1795380197746085&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dml&hl=ml&osid=1&TL=AAxq8nt73qcGYzTiNe-WvBLkBxWeqZqauzgc2-NGlLE2X_jTAhFAZTZw2vAQHW2c` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dpt&dsh=S118289191%3A1795380192958748&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dpt&hl=pt&osid=1&TL=AAxq8ntYxz66_iLI73dfEbtSVWEvI97MKlPNN2Iq_roRlIUXqGZAhn48VgoiE5SR` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dpt-BR&dsh=S-736926615%3A1795380196347869&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dpt-BR&hl=pt-BR&osid=1&TL=AAxq8nv0Dw8slp7nhveCCnba1ZKGZaS7WSuhhKgOH2cb8SYHiVu6MLaEDEb2Rwzv` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dro&dsh=S1228695011%3A1795380191041975&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dro&hl=ro&osid=1&TL=AAxq8nuyzEiXSVzh-1vx9Gn8T39848etBQl5XrAs5PTebl3sTDjJg33m9GjrrC-H` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dsl&dsh=S-1508547457%3A1795380198127729&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dsl&hl=sl&osid=1&TL=AAxq8nv3BrXVbWPvj1M5UZeCtN7dM-EJA9lHCFCWrjEZBGChIUn3JzM4oHfwdHAj` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dsv&dsh=S-736926615%3A1795380205608094&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dsv&hl=sv&osid=1&TL=AAxq8nuDcbMhq74lmOwUUIGqsTgnySDFCK82DdGFFV95CH77xbvOiO6RTJSNGrZ8` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dte&dsh=S-736926615%3A1795380199541657&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dte&hl=te&osid=1&TL=AAxq8nv1cZqvVyqXwSbCu-uKbGiQUU9rAcg_UC-88A1UqcNBgiV4G_JvzY6MBn-j` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dtr&dsh=S-736926615%3A1795380209987206&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dtr&hl=tr&osid=1&TL=AAxq8nuyz8BSiJajj0ozdOxktHHWamgAr89RCkJU8q1v0_4x_5hp2obrDSc-bTPu` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dur&dsh=S-1508547457%3A1795380196418304&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dur&hl=ur&osid=1&TL=AAxq8ntBToJco8uoPKejrhnduhPQQ97rqTddiNVaNeCDKt-73FgTUnimpEr-08v9` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dzh-CN&dsh=S1228695011%3A1795380210276406&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dzh-CN&hl=zh-CN&osid=1&TL=AAxq8nvhHo73Y5mippktWhWMUyK3tGoUDTPT90GZXJPXVPK0PMpT--zzSpBm6UOX` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dzh-TW&dsh=S118289191%3A1795380200962442&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2F%3Fhl%3Dzh-TW&hl=zh-TW&osid=1&TL=AAxq8nsRkMEBRpUSUmsxFbtHxjRSr-tgAZqX47p8cD5DVBAZnuB906mkZYjIhNfF` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Dar-EG&dsh=S118289191%3A1795380224830230&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Dar-EG&hl=ar-EG&osid=1&TL=AAxq8nvNuc-3j7Yg9PiyD_1QY_qW8HTnRxrWr6YMwurG_izsRpW1E78g2GHMtpZz` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Dar-SA&dsh=S118289191%3A1795380228742558&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Dar-SA&hl=ar-SA&osid=1&TL=AAxq8nsIi0HjTQ09rXXEEVdPRfRHxPQCeKD9VuOm_N_Lq0mX-jyilXMx-E-z5hMv` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Dde&dsh=S1228695011%3A1795380226496269&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Dde&hl=de&osid=1&TL=AAxq8nuvn72CbyPlq3nfrtSYvo8H2uJJHm0wFwMK8VKv4wv6SyG6neyYoEEMeSKm` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Des&dsh=S1228695011%3A1795380235118922&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Des&hl=es&osid=1&TL=AAxq8nsdQUJ_fJ2eTUQTQXFWh65Mqz_rJuh2WY8vaLuMIIT-0hd0repLXynIWFmj` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Des-419&dsh=S1228695011%3A1795380232346724&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Des-419&hl=es-419&osid=1&TL=AAxq8ns0Ajp144pLhs29AynjNqt4E0sOUJGX41ez3IcRz--9NDRRjcs31iotDUF1` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Des-MX&dsh=S118289191%3A1795380227383552&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Des-MX&hl=es-MX&osid=1&TL=AAxq8nspqGsB2DVIYETx7bhCxelSBUeZJ0dK4WRYXPQv8TXIqwoxqsntcYEwxcbE` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Dfr&dsh=S1228695011%3A1795380235468222&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Dfr&hl=fr&osid=1&TL=AAxq8nsJqiYRdsHTqwc2hlUYW_P-WVIc48uAQiu20vfMDuv1mSYMO8ttgwNFCHx7` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Dhe&dsh=S-1508547457%3A1795380231078331&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Dhe&hl=he&osid=1&TL=AAxq8nvEKC3R_lJQG4eN4xF5I8bwOVzXF_tmvETfVATVycSQrHzwunw3MII2Jl18` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Did&dsh=S-736926615%3A1795380230458209&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Did&hl=id&osid=1&TL=AAxq8nuJ5TK2OP0Wy6-Bar9x_cQa7MHqFv5tKUF5buAO8IABW0DyzYrXnoGJBNZe` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Diw&dsh=S118289191%3A1795380237170950&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Diw&hl=iw&osid=1&TL=AAxq8nvldGEevQAo7RL8-MXYA2umcKZ-X8XHStccps3bOM5ZkyqFWCUhDfJpb9TS` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Dml&dsh=S-736926615%3A1795380231149412&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Dml&hl=ml&osid=1&TL=AAxq8ntUDwa7oEtXU2M8Z_rQxxLh7p55F8SZF6UzVQO1ULebmaH5W0Y-8wZiKFXJ` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Dro&dsh=S118289191%3A1795380239006371&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Dro&hl=ro&osid=1&TL=AAxq8nv27sktN8UaZto4pqe8mXjRabROMTd9Canxr2NY3s-OgxOnIRTo77StfG_m` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Dte&dsh=S1228695011%3A1795380238116334&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Dte&hl=te&osid=1&TL=AAxq8ns9pN03Dhh4aHNw2gtX0yAWOq4RQ4Jp-SKYn_Dkht-dIzavchXC_TRpDxEm` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Dth&dsh=S118289191%3A1795380239736084&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Dth&hl=th&osid=1&TL=AAxq8ntDESwyPQYbuTW2BVTnU3XnmUHrkdthQ5guRjUYQqdic3B95_Z0ZePEaQ0C` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Duk&dsh=S1228695011%3A1795380240437475&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Duk&hl=uk&osid=1&TL=AAxq8ntRJgLb7ezxdrK08mDBA1wvL0WfhbpSAg-X7El8yQi0MDMQM6Tvo8JCKAlv` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Dvi&dsh=S-736926615%3A1795380240071982&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Dvi&hl=vi&osid=1&TL=AAxq8ntt_L6Kj_JgjL-MsAsFOMLWeiB6F5EwBUTYR-1TpLHZuh-Hd-ZbR43DVSzL` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Dzh&dsh=S1228695011%3A1795380243818137&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%2Fdownload%3Fhl%3Dzh&hl=zh&osid=1&TL=AAxq8nuRXjlVaiwmgJtV-M8BvhtQJFGezVueZZobwRd3MLf0HAzDKUr3CPr6VPQP` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%3Fcampaign%3Dtravel&dsh=S-1508547457%3A1795380208315879&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%3Fcampaign%3Dtravel&osid=1&TL=AAxq8nsXK7FyymkeiBjMyQHRtSF6nShQCxMfVLlnl5QvhilRvKMEOonWn3u0aEWQ` | TL, continue, dsh, ec, flowEntry, flowName, followup, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%3Fcampaign%3Dwriting&dsh=S-1508547457%3A1795380292875110&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%3Fcampaign%3Dwriting&osid=1&TL=AAxq8nud23bGST8NGAEXpTWLSx1NNmnwh9Z4DPTO9QbyW4kCEqMijIMocePO2X2R` | TL, continue, dsh, ec, flowEntry, flowName, followup, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar%26target%3Dimages%26nav_id%3Dbloom&dsh=S1228695011%3A1795380305987301&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar%26target%3Dimages%26nav_id%3Dbloom&hl=ar&osid=1&TL=AAxq8nv4TovOs3hTaC6ABKg_Bzsaf6PchbJVehefdepSFIhcJM9xkiKCSKlGV0vE` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar%26target%3Dimages%26nav_id%3Dchibi&dsh=S118289191%3A1795380314033816&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar%26target%3Dimages%26nav_id%3Dchibi&hl=ar&osid=1&TL=AAxq8ns4Z885U5QPTd_1SC1qxlpZRXZK8sBwf-TvKLh6V10WH8HHymEnCuHf-8m7` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar%26target%3Dimages%26nav_id%3Delven&dsh=S118289191%3A1795380335008711&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar%26target%3Dimages%26nav_id%3Delven&hl=ar&osid=1&TL=AAxq8nuRzwxL9iaMWCGE0PhZUaMoCgEGqP7qxPJBuqeIqKc6n4aNX8BbA94J5e3Q` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar%26target%3Dimages%26nav_id%3Dfb-mural&dsh=S-736926615%3A1795380343412427&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar%26target%3Dimages%26nav_id%3Dfb-mural&hl=ar&osid=1&TL=AAxq8nu5DsmW7NLMVnixhDrny4wHFlrfvAIY6nXFxfIqzSyuK2A5pWNok8Yp6ln1` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar%26target%3Dimages%26nav_id%3Dfb-slide&dsh=S-1508547457%3A1795380349316580&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar%26target%3Dimages%26nav_id%3Dfb-slide&hl=ar&osid=1&TL=AAxq8nuyWkDO2GK5dwmEFAGLe7qrSIjDiFTMHx6lwRs4hm_etQshkcLRq8jpKysl` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar%26target%3Dimages%26nav_id%3Dheadshot&dsh=S118289191%3A1795380364431819&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar%26target%3Dimages%26nav_id%3Dheadshot&hl=ar&osid=1&TL=AAxq8nudjYHB6GQ5SpDuqsNSSXw85jvYrUPDr37wC5eGVfXlCrw4FgHDF9LF_MPj` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar%26target%3Dimages%26nav_id%3Dlavender&dsh=S118289191%3A1795380378900067&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar%26target%3Dimages%26nav_id%3Dlavender&hl=ar&osid=1&TL=AAxq8ntAHpDewD01U8ckthmadVAhBknK3A-bxVv2o1DMQCSNC__L7KOppBnHCEVo` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar%26target%3Dimages%26nav_id%3Dmarble&dsh=S118289191%3A1795380383991746&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar%26target%3Dimages%26nav_id%3Dmarble&hl=ar&osid=1&TL=AAxq8nsak0iKroqIiVIAm1mc-Drzu29lSfdcFJt30yixVPhI1EbPJmqpWLVBqZrJ` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar%26target%3Dimages%26nav_id%3Dneon&dsh=S-736926615%3A1795380402819930&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar%26target%3Dimages%26nav_id%3Dneon&hl=ar&osid=1&TL=AAxq8nsHQiqiJErZz1qqUBUIo09VB0nc-zZzoY4-bwqbk9VfcNR8adVHknwo9iGq` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar%26target%3Dimages%26nav_id%3Dorigami&dsh=S-736926615%3A1795380414819654&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar%26target%3Dimages%26nav_id%3Dorigami&hl=ar&osid=1&TL=AAxq8ntOf0CLt2NQ3wsjUYJIhVQ2xXXx-yxGlUxut-CtCxO801cghGbEs-Kksv-_` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar%26target%3Dimages%26nav_id%3Dpaint&dsh=S-1508547457%3A1795380416570147&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar%26target%3Dimages%26nav_id%3Dpaint&hl=ar&osid=1&TL=AAxq8nsvAFmZtf_klUPrtHEq8bfLHrACR989WxwYU0_lZsf_O3HU_mDo5nxROcfj` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar%26target%3Dimages%26nav_id%3Dpin&dsh=S118289191%3A1795380425942417&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar%26target%3Dimages%26nav_id%3Dpin&hl=ar&osid=1&TL=AAxq8nv9EqYaRJdsnGiLvnZ0IpTmBa7U1dnY0Y0oXv63HKBEaDDRi5fLuqMZoyaF` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar%26target%3Dimages%26nav_id%3Dyogi&dsh=S1228695011%3A1795380454475563&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar%26target%3Dimages%26nav_id%3Dyogi&hl=ar&osid=1&TL=AAxq8nsvHinK0tH-kQ1mYRJ4ZYTTLp1exb0ZcPxma_RJRyVvTgGW1QZgi3djVN6l` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar%26target%3Dimages%26nav_id%3Dzen&dsh=S-736926615%3A1795380462199983&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar%26target%3Dimages%26nav_id%3Dzen&hl=ar&osid=1&TL=AAxq8nvLwBG2zG5BkKmotSofNAXw5LIAi4SMqVvqqVyWyYArTH6AK6qrJ8GuKXeX` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar&dsh=S-736926615%3A1795380203635011&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar&hl=ar&osid=1&TL=AAxq8ns1TAysFlkSIq-o6cOF-uFvbs6HEPvFb035v4SfoBDZONyjfZzWXyYUuHWb` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar-EG&dsh=S1228695011%3A1795380202357495&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dar-EG&hl=ar-EG&osid=1&TL=AAxq8nvsyXvjb027kahQ7nEPHg2A2e38mlnDYlS8jeTnW11jjVxuNYCk1Ni8Sjz-` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |
| `https://accounts.google.com/lifecycle/steps/signup/unknownerror?continue=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dde%26target%3Dimages%26nav_id%3Dbento&dsh=S118289191%3A1795380301431944&ec=GAZAkgU&flowEntry=SignUp&flowName=GlifWebSignIn&followup=https%3A%2F%2Fgemini.google.com%2Fapp%3Fhl%3Dde%26target%3Dimages%26nav_id%3Dbento&hl=de&osid=1&TL=AAxq8nsrGD9tV1ii04BJLXMH_qzF_-34IUSIVp6NpJkGenRqkFxZOWeDc_Vlz8WA` | TL, continue, dsh, ec, flowEntry, flowName, followup, hl, osid |

## 9. SECRET CANDIDATES

_None found._

## 10. TOOL RUN STATUS (no silent skips)

| Tool | Result | Detail |
|---|---|---|
| `anastasis` | exit 254 | no output produced — see logs/ |
| `dnsx` | OK | completed |
| `ffuf` | OK | off by choice — wordlist prepared |
| `gau` | OK | completed |
| `gospider` | OK | completed |
| `httpx` | OK | completed |
| `js-download` | OK | 172 chunks saved over 3 round(s) |
| `jscope` | OK | completed |
| `jsluice` | OK | 172 files parsed |
| `katana` | OK | completed |
| `methods` | OK | 119 method responses |
| `subfinder` | OK | completed |
| `trufflehog` | OK | completed |
| `uncover` | OK | no API key configured — no external data |
| `urlfinder` | OK | completed |
| `uro` | OK | completed |
| `vhost` | OK | 1 real of 4 tested |
| `x8` | OK | parameter scan complete |

## 11. INTENTIONALLY NOT RUN

- **ffuf path brute** — off by default; `wordlist.txt` is ready. Set `enable_brute: true` later.
- **kiterunner** — off by default alongside ffuf.

## 12. OUTPUT FILES

| File | Meaning |
|---|---|
| [`all_routes.jsonl`](all_routes.jsonl) | every route, unfiltered (861,825 B) |
| [`accessible_200.jsonl`](accessible_200.jsonl) | HTTP 200 wins (13,805 B) |
| [`exists_blocked.jsonl`](exists_blocked.jsonl) | exists but blocked (552,789 B) |
| [`other_status.jsonl`](other_status.jsonl) | all other statuses (61,583 B) |
| [`data_files.jsonl`](data_files.jsonl) | JSON/CSV/XML among 200s (811 B) |
| [`params.jsonl`](params.jsonl) | parameters (896,469 B) |
| [`subdomains.jsonl`](subdomains.jsonl) | subdomains + resolution (370 B) |
| [`third_party_routes.jsonl`](third_party_routes.jsonl) | third-party URLs — kept, not deleted (666,548 B) |
| [`method_responses.jsonl`](method_responses.jsonl) | all method-probe responses — kept (18,478 B) |
| [`vhost_real.jsonl`](vhost_real.jsonl) | non-blocked virtual hosts (61 B) |
| [`vhost_blocked.jsonl`](vhost_blocked.jsonl) | blocked vhost checks — kept (193 B) |
| [`js_endpoints.jsonl`](js_endpoints.jsonl) | AST endpoints (0 B) |
| [`vhost.jsonl`](vhost.jsonl) | all vhost checks (254 B) |
| [`jsluice.jsonl`](jsluice.jsonl) | JS-derived URLs (348,519 B) |
| [`gospider.txt`](gospider.txt) | second crawler URLs (628,624 B) |
| [`jscope.txt`](jscope.txt) | evidence-ranked JS analysis (29,855 B) |
| [`secrets.jsonl`](secrets.jsonl) | secret candidates (0 B) |
| [`wordlist.txt`](wordlist.txt) | target-specific fuzz list (13,021 B) |
| [`params.txt`](params.txt) | parameter wordlist (339 B) |
| [`js_urls.txt`](js_urls.txt) | JS chunk URLs (14,582 B) |
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