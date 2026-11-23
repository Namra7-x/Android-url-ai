# Hunt Report — https://modelstudio.console.alibabacloud.com

Generated: 2026-11-23T16:16:01Z &nbsp;|&nbsp; Duration: 93m 15s

> **Nothing is filtered during collection. This report is only a grouping.**

## Summary

| What | Count | Meaning |
|---|---:|---|
| Routes collected | 714 | Every URL found, nothing removed |
| Distinct routes verified | 696 | One row per URL (method probes excluded) |
| HTTP responses | 1896 | Includes method probes — kept in `method_responses.jsonl` |
| **Accessible (200)** | **661** | Confirmed live — the wins |
| Exists but different status | 13 | 301/302/401/403/405 — real route, blocked |
| Other responses | 22 | 404/500/etc — kept, not discarded |
| Subdomains (resolved) | 1 | DNS-verified |
| Virtual hosts (real) | 0 | Cloudflare 403/530/0 excluded |
| Parameters | 37 | URLs with query params |
| JS endpoints (AST) | 442 | anastasis evidence-backed |
| First-party URLs | 421 | modelstudio.console.alibabacloud.com and subdomains |
| Third-party URLs | 293 | kept in `third_party_routes.jsonl` |
| Method responses | 1400 | kept in `method_responses.jsonl` |
| Blocked vhost checks | 1 | kept in `vhost_blocked.jsonl` |
| Secret candidates | 0 | verify manually |

> Collection keeps third-party URLs by design (293). See `third_party_routes.jsonl`. Method-probe responses are in `method_responses.jsonl`.

## 0. TOP ROUTE PATTERNS (IDs collapsed)

| Pattern | Count |
|---|---:|
| `/` | 33 |
| `/g` | 5 |
| `/data/api.json` | 4 |
| `/login/login.htm` | 3 |
| `/wcfg.json` | 3 |
| `/rp` | 3 |
| `/login/fast_login_config` | 2 |
| `/error` | 2 |
| `/Release/pkgs/${id` | 2 |
| `/AWSC/AWSC/awsc.js` | 2 |
| `/intl/blog` | 2 |
| `/data/publicCustom.json` | 2 |
| `/efm/{id}` | 2 |
| `/model/{id}` | 2 |
| `/model/experience/omni` | 2 |
| `/sd/baxia` | 2 |
| `/service/create-ticket` | 2 |
| `/eg.js` | 1 |
| `/tongyi-cn.bailian-intl.exp_back_to_legacy_entry` | 1 |
| `/tongyi-cn.bailian-intl.expose_feature_section` | 1 |
| `/tongyi-cn.bailian-intl.expose_header_nav` | 1 |
| `/tongyi-cn.bailian-intl.page_view` | 1 |
| `/console.js` | 1 |
| `/AWSC/fireyejs/1.234.24/fireyejs.js` | 1 |
| `/BigDipper/diagnosis/js/track.js` | 1 |
| `/alicloud-components/common/feedback/feedback.js` | 1 |
| `/bailian-fe/bailian-site-fe/0.0.241/assets/APIKeyEmpty.js` | 1 |
| `/bailian-fe/bailian-site-fe/0.0.241/assets/ActionsColumn.js` | 1 |
| `/bailian-fe/bailian-site-fe/0.0.241/assets/ApiKeyCreateSuccessModal.js` | 1 |
| `/bailian-fe/bailian-site-fe/0.0.241/assets/ApiKeyEditModal.js` | 1 |
| `/bailian-fe/bailian-site-fe/0.0.241/assets/BfalAlertCircle.js` | 1 |
| `/bailian-fe/bailian-site-fe/0.0.241/assets/BfalAlertCircleFilled.js` | 1 |
| `/bailian-fe/bailian-site-fe/0.0.241/assets/BfalArrowUp.js` | 1 |
| `/bailian-fe/bailian-site-fe/0.0.241/assets/BfalArrowUpRight.js` | 1 |
| `/bailian-fe/bailian-site-fe/0.0.241/assets/BfalArrowsMinimize.js` | 1 |
| `/bailian-fe/bailian-site-fe/0.0.241/assets/BfalChartLine.js` | 1 |
| `/bailian-fe/bailian-site-fe/0.0.241/assets/BfalCheck.js` | 1 |
| `/bailian-fe/bailian-site-fe/0.0.241/assets/BfalCheckupList.js` | 1 |
| `/bailian-fe/bailian-site-fe/0.0.241/assets/BfalChevronDown.js` | 1 |
| `/bailian-fe/bailian-site-fe/0.0.241/assets/BfalChevronUp.js` | 1 |

## 1. SUCCESS — HTTP 200

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 200 | GET | `https://account.alibabacloud.com/login/login.htm?oauth_callback=EXPR&clearRedirectCookie=1` | text/html | 16340 |  |
| 200 | GET | `https://account.aliyun.com/login/login.htm?oauth_callback=EXPR` | text/html | 6954 |  |
| 200 | GET | `https://acjs.aliyun.com/error?v=` | application/octet-stream | 0 |  |
| 200 | GET | `https://aplus.alibabacloud.com/eg.js` | application/javascript | 91 |  |
| 200 | GET | `https://aplus.alibabacloud.com/tongyi-cn.bailian-intl.exp_back_to_legacy_entry?gmkey=EXP` | image/gif | 43 |  |
| 200 | GET | `https://aplus.alibabacloud.com/tongyi-cn.bailian-intl.expose_feature_section?gmkey=EXP` | image/gif | 43 |  |
| 200 | GET | `https://aplus.alibabacloud.com/tongyi-cn.bailian-intl.expose_header_nav?gmkey=EXP` | image/gif | 43 |  |
| 200 | GET | `https://aplus.alibabacloud.com/tongyi-cn.bailian-intl.page_view?gmkey=EXP` | image/gif | 43 |  |
| 200 | GET | `https://bdc.alibabachengdun.com/wcfg.json` | application/json | 58 |  |
| 200 | GET | `https://cloud-assets.alicdn.com/console.js` | application/javascript | 464 |  |
| 200 | GET | `https://fourier.taobao.com/rp?ext=51&data=jm_` | application/javascript | 1441 |  |
| 200 | GET | `https://g.alicdn.com/AWSC/AWSC/awsc.js` | application/javascript | 17444 |  |
| 200 | GET | `https://g.alicdn.com/AWSC/fireyejs/1.234.24/fireyejs.js` | application/javascript | 550996 |  |
| 200 | GET | `https://g.alicdn.com/BigDipper/diagnosis/js/track.js` | application/javascript | 27772 |  |
| 200 | GET | `https://g.alicdn.com/alicloud-components/common/feedback/feedback.js` | application/javascript | 0 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/APIKeyEmpty.js` | application/javascript | 2400 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/ActionsColumn.js` | application/javascript | 1516 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/ApiKeyCreateSuccessModal.js` | application/javascript | 13298 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/ApiKeyEditModal.js` | application/javascript | 6828 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/BfalAlertCircle.js` | application/javascript | 514 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/BfalAlertCircleFilled.js` | application/javascript | 644 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/BfalArrowUp.js` | application/javascript | 469 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/BfalArrowUpRight.js` | application/javascript | 482 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/BfalArrowsMinimize.js` | application/javascript | 541 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/BfalChartLine.js` | application/javascript | 483 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/BfalCheck.js` | application/javascript | 456 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/BfalCheckupList.js` | application/javascript | 979 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/BfalChevronDown.js` | application/javascript | 472 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/BfalChevronUp.js` | application/javascript | 467 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/BfalCircleCheck.js` | application/javascript | 512 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/BfalCircleCheckFilled.js` | application/javascript | 662 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/BfalCode.js` | application/javascript | 475 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/BfalCopy.js` | application/javascript | 562 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/BfalExclamationCircle.js` | application/javascript | 532 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/BfalExternalLink.js` | application/javascript | 538 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/BfalFileText.js` | application/javascript | 553 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/BfalFilter.js` | application/javascript | 527 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/BfalHelpCircle.js` | application/javascript | 558 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/BfalInfoCircle.js` | application/javascript | 517 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/BfalLoader.js` | application/javascript | 905 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/BfalPlus.js` | application/javascript | 455 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/BfalReload.js` | application/javascript | 523 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/BfalRobot.js` | application/javascript | 633 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/BfalSearch.js` | application/javascript | 490 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/BfalTrash.js` | application/javascript | 545 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/BfalUser.js` | application/javascript | 2369 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/BfalVideo.js` | application/javascript | 579 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/BfalX.js` | application/javascript | 450 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/CheckOutlined.js` | application/javascript | 696 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/CloseOutlined.js` | application/javascript | 702 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/ContextIsolator.js` | application/javascript | 162659 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/CopyableIdColumn.js` | application/javascript | 3663 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/CreateApiKeyModal.js` | application/javascript | 8653 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/CutConfirm.js` | application/javascript | 786 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/FilterBar.js` | application/javascript | 17232 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/FilterSelect.js` | application/javascript | 9640 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/GlobalNotice.js` | application/javascript | 3419 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/GuideEmpty.js` | application/javascript | 7938 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/HighlightedCode.js` | application/javascript | 690652 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/Icon.js` | application/javascript | 1643 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/InitLoadingPage.js` | application/javascript | 16855 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/InnerLayout.js` | application/javascript | 19753 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/IpWhitelistInput.js` | application/javascript | 44186 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/LayoutContainerContext.js` | application/javascript | 166 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/LoadingOutlined.js` | application/javascript | 12679 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/ModelChooseModal.js` | application/javascript | 135231 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/ModelOfflineTag.js` | application/javascript | 13600 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/PlusOutlined.js` | application/javascript | 696 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/PrismHighlighter.js` | application/javascript | 159806 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/ResizeObserver.es.js` | application/javascript | 7638 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/SearchOutlined.js` | application/javascript | 1253 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/SpaceDetailModal.js` | application/javascript | 14438 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/StartErrorContent.js` | application/javascript | 5229 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/Table2.js` | application/javascript | 5031 |  |
| 200 | GET | `https://g.alicdn.com/bailian-fe/bailian-site-fe/0.0.241/assets/TablePagination.js` | application/javascript | 20351 |  |
| … | … | _586 more in JSONL_ | … | … | … |

## 2. EXISTS BUT DIFFERENT STATUS (301/302/401/403/405)

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 302 | GET | `https://account.aliyun.com/login/fast_login_config` | text/html | 0 |  |
| 403 | GET | `https://assets.alicdn.com` | application/xml | 385 |  |
| 403 | GET | `https://assets.aliexpress-media.com` | application/xml | 390 |  |
| 403 | GET | `https://at.alicdn.com` | application/xml | 342 |  |
| 302 | GET | `https://bailian-singapore-cs.alibabacloud.com/data/api.json?action=IntlBroadScopeAspnGateway` | text/html | 258 |  |
| 307 | GET | `https://docs.modelstudio.console.alibabacloud.com` | text/html | 5624918 |  |
| 302 | GET | `https://fecs.console.aliyun.com` |  | 0 |  |
| 403 | GET | `https://g.lazcdn.com` | application/xml | 380 |  |
| 302 | GET | `https://help.aliyun.com` |  | 0 |  |
| 403 | GET | `https://lzd-g.slatic.net` | application/xml | 380 |  |
| 308 | GET | `https://modelstudio.alibabacloud.com/intl/blog` | text/plain | 11 |  |
| 302 | GET | `https://modelstudio.console.alibabacloud.com/error?v=` |  | 0 |  |
| 403 | GET | `https://uaction.alicdn.com` | application/xml | 369 |  |

## 3. OTHER RESPONSES — kept, never discarded

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 404 | GET | `https://aeis.alicdn.com` | application/xml | 381 |  |
| 404 | GET | `https://assets.alicdn.com/g/?%3F%2FAWSC%2FAWSC%2Fawsc.js=` | application/xml | 386 |  |
| 404 | GET | `https://assets.alicdn.com/g/?%3F=` | application/xml | 386 |  |
| 404 | GET | `https://cws.alicdn.com` | text/html | 22 |  |
| 404 | GET | `https://cws.alicdn.com/Release/pkgs/${id` | text/html | 22 |  |
| 404 | GET | `https://g.alicdn.com` | application/xml | 386 |  |
| 404 | GET | `https://g.alicdn.com/?%3F%2FAWSC%2FAWSC%2Fawsc.js=` | application/xml | 386 |  |
| 404 | GET | `https://g.alicdn.com/?%3F=` | application/xml | 386 |  |
| 404 | GET | `https://g.alicdn.com/code/npm/@ali/bfal-antd/6.6.8/esm/dayjs/plugin` | application/xml | 432 |  |
| 404 | GET | `https://g.alicdn.com/one-mcms/wind-v2/[object` | application/xml | 410 |  |
| 404 | GET | `https://g.lazcdn.com/g/?%3F=` | text/html | 77843 |  |
| 404 | GET | `https://g.mrvcdn.com/?%3F=` | application/xml | 381 |  |
| 404 | GET | `https://laz-g-cdn.alicdn.com/?%3F=` | application/xml | 381 |  |
| 404 | GET | `https://lzd-g.slatic.net/g/?%3F=` | application/xml | 381 |  |
| 404 | GET | `https://umdc-global.alibaba.com` | application/json | 89 |  |
| 404 | GET | `https://umdc-global.aliexpress.com` | application/json | 89 |  |
| 404 | GET | `https://umdc.alibaba-inc.com` | application/json | 89 |  |
| 404 | GET | `https://umdc.alibaba-inc.com/EXPR` | application/json | 93 |  |
| 404 | GET | `https://umdc.goofish.com` | application/json | 89 |  |
| 404 | GET | `https://umdc.tmall.hk` | application/json | 89 |  |
| 404 | GET | `https://umdcv4.taobao.com` | application/json | 89 |  |
| 404 | GET | `https://umdcv4.tmall.com` | application/json | 89 |  |

## 4. DATA FILES (accessible)

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 200 | GET | `https://bdc.alibabachengdun.com/wcfg.json` | application/json | 58 |  |
| 200 | GET | `https://modelstudio.console.alibabacloud.com/api.json` | application/json | 128 |  |
| 200 | GET | `https://modelstudio.console.alibabacloud.com/data/api.json?%24%7Bt.toString%28=` | application/json | 128 |  |
| 200 | GET | `https://modelstudio.console.alibabacloud.com/data/api.json?EXPR=` | application/json | 128 |  |
| 200 | GET | `https://modelstudio.console.alibabacloud.com/data/custom.json` | application/json | 128 |  |
| 200 | GET | `https://modelstudio.console.alibabacloud.com/data/publicCustom.json?action=QueryOrderLight` | application/json | 136 |  |
| 200 | GET | `https://modelstudio.console.alibabacloud.com/risk/sendVerifyMessage.json` | application/json | 128 |  |
| 200 | GET | `https://modelstudio.console.alibabacloud.com/sitemap.xml` | text/html | 22338 |  |
| 200 | GET | `https://modelstudio.console.alibabacloud.com/tool/user/info.json` | application/json | 128 |  |
| 200 | GET | `https://umdc.taobao.com/wcfg.json` | application/json | 58 |  |
| 200 | GET | `https://umdc.tmall.com/wcfg.json` | application/json | 58 |  |

## 5. SUBDOMAINS (detailed)

Found **1**, DNS-resolved **1**.

| Host | Resolved | Source |
|---|---|---|
| `docs.modelstudio.console.alibabacloud.com` | yes | passive |

## 6. VIRTUAL HOSTS (real statuses only)

_No non-blocked virtual hosts found._
Blocked/noisy vhost checks (403/530/0) are kept in `vhost_blocked.jsonl` (1).

## 7. JS ENDPOINTS (AST, evidence-backed)

| Method | Path | Confidence |
|---|---|---|
| GET | `/compatible-mode/v1` | 0.7 |
| UNKNOWN | `/apps/anthropic` | 0.7 |
| UNKNOWN | `/subscription/uac-admin/organization/members/list` | 0.7 |
| GET | `/20)` | 0.7 |
| UNKNOWN | `/cli` | 0.7 |
| GET | `/?p=guardrail` | 0.7 |
| UNKNOWN | `/settings/security` | 0.7 |
| UNKNOWN | `/home/billing/overview?target=recharge` | 0.7 |
| UNKNOWN | `/?spm=` | 0.7 |
| UNKNOWN | `/__vite_openapi_mock` | 0.7 |
| GET | `/home/settings/account` | 0.7 |
| UNKNOWN | `/fortune/fund-management/recharge` | 0.7 |
| UNKNOWN | `/zh/user-center/developer-reference/api-calling-authorization` | 0.7 |
| UNKNOWN | `/data/api.json` | 0.7 |
| UNKNOWN | `/data/publicCustom.json` | 0.7 |
| UNKNOWN | `/tool/user/info.json` | 0.7 |
| UNKNOWN | `/data/custom.json` | 0.7 |
| UNKNOWN | `/login/fast_login_config` | 0.7 |
| UNKNOWN | `/v1` | 0.7 |
| UNKNOWN | `/${n}@@@@${h}` | 0.6 |
| UNKNOWN | `/login/login.htm?oauth_callback=${encodeURIComponent(t)}` | 0.6 |
| UNKNOWN | `/login/login.htm?oauth_callback=${encodeURIComponent(t)}&clearRedirectCookie=1` | 0.6 |
| UNKNOWN | `/ap-southeast-1` | 0.7 |
| UNKNOWN | `/bailian.console.aliyun.com` | 0.7 |
| UNKNOWN | `/bailian.web.event` | 0.7 |
| UNKNOWN | `/cn-beijing` | 0.7 |
| GET | `/costing-balance/budget` | 0.7 |
| GET | `/costing-balance/free-quota` | 0.7 |
| GET | `/costing-balance/overview` | 0.7 |
| GET | `/costing-balance/quota-managements` | 0.7 |
| GET | `/costing-balance/usage-statistics` | 0.7 |
| UNKNOWN | `/home` | 0.7 |
| GET | `/model/alert` | 0.7 |
| GET | `/model/asset-center` | 0.7 |
| GET | `/model/batch` | 0.7 |
| GET | `/model/compress` | 0.7 |
| GET | `/model/confidential-inference` | 0.7 |
| GET | `/model/custom` | 0.7 |
| GET | `/model/data` | 0.7 |
| GET | `/model/deploy` | 0.7 |
| GET | `/model/evaluate` | 0.7 |
| GET | `/model/experience/omni` | 0.7 |
| GET | `/model/experience/text` | 0.7 |
| GET | `/model/experience/vision` | 0.7 |
| GET | `/model/experience/voice` | 0.7 |
| GET | `/model/high-speed-inference` | 0.7 |
| GET | `/model/logs` | 0.7 |
| GET | `/model/market` | 0.7 |
| GET | `/model/model-telemetry` | 0.7 |
| GET | `/model/settings/kms` | 0.7 |
| GET | `/model/smart-routing` | 0.7 |
| GET | `/model/telemetry` | 0.7 |
| GET | `/model/tpm-reservation` | 0.7 |
| GET | `/model/tuning` | 0.7 |
| UNKNOWN | `/modelstudio.console.alibabacloud.com` | 0.7 |
| UNKNOWN | `/pre-bailian.console.aliyun.com` | 0.7 |
| UNKNOWN | `/pre-modelstudio.console.alibabacloud.com` | 0.7 |
| GET | `/settings/app-model-config` | 0.5 |
| GET | `/settings/network-config` | 0.7 |
| GET | `/settings/quota-management` | 0.7 |
| GET | `/settings/security` | 0.7 |
| GET | `/settings/user-management` | 0.7 |
| GET | `/settings/workspace` | 0.7 |
| UNKNOWN | `/us-east-1` | 0.7 |
| UNKNOWN | `/xx.yy.` | 0.7 |
| UNKNOWN | `/liveme-console` | 0.7 |
| UNKNOWN | `/model/settings/api-key` | 0.7 |
| UNKNOWN | `/settings/api-key` | 0.7 |
| UNKNOWN | `/help/en/content-moderation/latest/how-to-use-ai-security-guardrail-service-on-alibaba-cloud` | 0.7 |
| UNKNOWN | `/micro` | 0.7 |
| UNKNOWN | `/#` | 0.7 |
| UNKNOWN | `/?commodityCode=lvwang_guardrail_public_cn` | 0.7 |
| UNKNOWN | `/risk/sendVerifyMessage.json` | 0.7 |
| UNKNOWN | `/?commodityCode=lvwang_guardrail_public_intl` | 0.7 |
| UNKNOWN | `/${Ll}/data/publicCustom.json` | 0.6 |
| UNKNOWN | `/api.json` | 0.7 |
| UNKNOWN | `/Release` | 0.7 |
| GET | `/__get_micro_app__` | 0.7 |
| UNKNOWN | `/dev.g.alicdn.com` | 0.7 |
| UNKNOWN | `/axios/axios.git` | 0.7 |
| UNKNOWN | `/axios/axios/issues` | 0.7 |
| GET | `/api-key` | 0.5 |
| UNKNOWN | `/costing-balance/budget` | 0.7 |
| UNKNOWN | `/costing-balance/free-quota` | 0.7 |
| GET | `/flow-agent/app-task-center` | 0.5 |
| GET | `/flow-agent/app-ui` | 0.5 |
| GET | `/flow-agent/component-manage` | 0.5 |
| GET | `/flow-agent/mcp-manage` | 0.5 |
| GET | `/flow-agent/plugin-manage` | 0.5 |
| GET | `/flow-agent/prompt-manage` | 0.5 |
| GET | `/flow-agent/quick-start` | 0.5 |
| GET | `/flow-agent/skill` | 0.5 |
| GET | `/rag/channel` | 0.5 |
| GET | `/rag/playground` | 0.5 |
| GET | `/rag/qa` | 0.5 |
| GET | `/rag/retrieval` | 0.5 |
| GET | `/rag/usage` | 0.5 |
| GET | `/sandbox/high-code` | 0.5 |
| GET | `/store/app-market` | 0.5 |
| GET | `/store/mcp` | 0.5 |

## 8. PARAMETERS

| URL | Params |
|---|---|
| `https://account.alibabacloud.com/login/login.htm?oauth_callback=EXPR&clearRedirectCookie=1` | clearRedirectCookie, oauth_callback |
| `https://account.aliyun.com/login/login.htm?oauth_callback=EXPR` | oauth_callback |
| `https://acjs.aliyun.com/error?v=` | v |
| `https://aplus.alibabacloud.com/tongyi-cn.bailian-intl.exp_back_to_legacy_entry?gmkey=EXP` | gmkey |
| `https://aplus.alibabacloud.com/tongyi-cn.bailian-intl.expose_feature_section?gmkey=EXP` | gmkey |
| `https://aplus.alibabacloud.com/tongyi-cn.bailian-intl.expose_header_nav?gmkey=EXP` | gmkey |
| `https://aplus.alibabacloud.com/tongyi-cn.bailian-intl.page_view?gmkey=EXP` | gmkey |
| `https://assets.alicdn.com/g/?%3F%2FAWSC%2FAWSC%2Fawsc.js=` | ?/AWSC/AWSC/awsc.js |
| `https://assets.alicdn.com/g/?%3F=` | ? |
| `https://bailian-singapore-cs.alibabacloud.com/data/api.json?action=IntlBroadScopeAspnGateway` | action |
| `https://fourier.taobao.com/rp?ext=51` | ext |
| `https://fourier.taobao.com/rp?ext=51&data=jm_` | data, ext |
| `https://g.alicdn.com/?%3F%2FAWSC%2FAWSC%2Fawsc.js=` | ?/AWSC/AWSC/awsc.js |
| `https://g.alicdn.com/?%3F=` | ? |
| `https://g.lazcdn.com/g/?%3F=` | ? |
| `https://g.mrvcdn.com/?%3F=` | ? |
| `https://laz-g-cdn.alicdn.com/?%3F=` | ? |
| `https://lzd-g.slatic.net/g/?%3F=` | ? |
| `https://modelstudio.console.alibabacloud.com/?%28%5B%5E=` | ([^ |
| `https://modelstudio.console.alibabacloud.com/?commodityCode=lvwang_guardrail_public_cn` | commodityCode |
| `https://modelstudio.console.alibabacloud.com/?commodityCode=lvwang_guardrail_public_intl` | commodityCode |
| `https://modelstudio.console.alibabacloud.com/?commodityCode=sfm_platform_public_cn` | commodityCode |
| `https://modelstudio.console.alibabacloud.com/?p=guardrail` | p |
| `https://modelstudio.console.alibabacloud.com/?spm=` | spm |
| `https://modelstudio.console.alibabacloud.com/ModelStudioAI?s=20` | s |
| `https://modelstudio.console.alibabacloud.com/data/api.json?%24%7Bt.toString%28=` | ${t.toString( |
| `https://modelstudio.console.alibabacloud.com/data/api.json?EXPR=` | EXPR |
| `https://modelstudio.console.alibabacloud.com/data/publicCustom.json?action=QueryOrderLight` | action |
| `https://modelstudio.console.alibabacloud.com/error?v=` | v |
| `https://modelstudio.console.alibabacloud.com/g/?%3F=` | ? |
| `https://modelstudio.console.alibabacloud.com/home/billing/overview?target=recharge` | target |
| `https://modelstudio.console.alibabacloud.com/login/login.htm?oauth_callback=%24%7BencodeURIComponent%28t` | oauth_callback |
| `https://modelstudio.console.alibabacloud.com/model/experience/omni?%24%7Bt=` | ${t |
| `https://modelstudio.console.alibabacloud.com/rp?ext=51&data=jm_` | data, ext |
| `https://modelstudio.console.alibabacloud.com/service/create-ticket-intl?activeTab=1` | activeTab |
| `https://modelstudio.console.alibabacloud.com/service/create-ticket?product=bailian` | product |
| `https://modelstudio.console.alibabacloud.com/zh/user-center/cancel-subscription/?spm=a2c4g.11186623.0.i0` | spm |

## 9. SECRET CANDIDATES

_None found._

## 10. NUCLEI FINDINGS (verified exposures / misconfigs)

_No nuclei findings on live hosts._

## 11. TOOL RUN STATUS (no silent skips)

| Tool | Result | Detail |
|---|---|---|
| `anastasis` | OK | 442 endpoints, 31 params |
| `cariddi` | OK | completed |
| `dnsx` | OK | completed |
| `ffuf` | OK | off by choice — wordlist prepared |
| `getJS` | exit 2 | see logs/ |
| `httpx` | OK | completed |
| `js-download` | OK | 214 chunks saved over 3 round(s) |
| `jscope` | OK | completed |
| `jsluice` | OK | 214 files parsed in batches of 100 |
| `katana` | exit 124 | see logs/ |
| `methods` | OK | 1400 method responses |
| `noseyparker` | OK | completed |
| `nuclei` | OK | 0 findings on 300 live hosts |
| `subfinder` | OK | completed |
| `subjs` | OK | completed |
| `trufflehog` | OK | completed |
| `uncover` | OK | no API key configured — no external data |
| `urlfinder` | OK | completed |
| `uro` | OK | completed |
| `vhost` | OK | 0 real of 1 tested |
| `waybackurls` | OK | completed |
| `x8` | OK | parameter scan complete |

## 12. INTENTIONALLY NOT RUN

- **ffuf path brute** — off by default; `wordlist.txt` is ready. Set `enable_brute: true` later.
- **kiterunner** — off by default alongside ffuf.

## 13. OUTPUT FILES

| File | Meaning |
|---|---|
| [`all_routes.jsonl`](all_routes.jsonl) | every route, unfiltered (110,574 B) |
| [`accessible_200.jsonl`](accessible_200.jsonl) | HTTP 200 wins (600,253 B) |
| [`exists_blocked.jsonl`](exists_blocked.jsonl) | exists but blocked (10,568 B) |
| [`other_status.jsonl`](other_status.jsonl) | all other statuses (16,192 B) |
| [`data_files.jsonl`](data_files.jsonl) | JSON/CSV/XML among 200s (8,672 B) |
| [`params.jsonl`](params.jsonl) | parameters (4,310 B) |
| [`subdomains.jsonl`](subdomains.jsonl) | subdomains + resolution (103 B) |
| [`third_party_routes.jsonl`](third_party_routes.jsonl) | third-party URLs — kept, not deleted (38,142 B) |
| [`method_responses.jsonl`](method_responses.jsonl) | all method-probe responses — kept (204,570 B) |
| [`vhost_real.jsonl`](vhost_real.jsonl) | non-blocked virtual hosts (0 B) |
| [`vhost_blocked.jsonl`](vhost_blocked.jsonl) | blocked vhost checks — kept (74 B) |
| [`js_endpoints.jsonl`](js_endpoints.jsonl) | AST endpoints (41,751 B) |
| [`vhost.jsonl`](vhost.jsonl) | all vhost checks (74 B) |
| [`jsluice.jsonl`](jsluice.jsonl) | JS-derived URLs (490,293 B) |
| [`cariddi.txt`](cariddi.txt) | crawl + secrets/endpoints (404 B) |
| [`wayback_urls.txt`](wayback_urls.txt) | archive URLs (1 B) |
| [`noseyparker.jsonl`](noseyparker.jsonl) | fast secret scan (1,733 B) |
| [`nuclei.jsonl`](nuclei.jsonl) | verified exposure findings (0 B) |
| [`anastasis_endpoints.jsonl`](anastasis_endpoints.jsonl) | AST endpoints (41,751 B) |
| [`jscope.txt`](jscope.txt) | evidence-ranked JS analysis (46,972 B) |
| [`secrets.jsonl`](secrets.jsonl) | secret candidates (0 B) |
| [`wordlist.txt`](wordlist.txt) | target-specific fuzz list (33,708 B) |
| [`params.txt`](params.txt) | parameter wordlist (136 B) |
| [`js_urls.txt`](js_urls.txt) | JS chunk URLs (16,640 B) |
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