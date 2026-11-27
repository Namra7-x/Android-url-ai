# Web Hunt Report: `modelstudio.console.alibabacloud.com`

- **Target:** https://modelstudio.console.alibabacloud.com/
- **Scope Apex:** `modelstudio.console.alibabacloud.com`
- **Duration:** `4:54` (294.5s)
- **Generated:** 2026-11-27T10:55:35Z

## Wave Timings

| Wave | Elapsed (s) |
|---|---:|
| Wave 1 (Discovery) | 103.8 |
| Wave 2 (Chunks) | 3.7 |
| Wave 3 (Offline AST/Secrets) | 6.6 |
| Wave 4 (Verify/Fuzz/Feed) | 180.4 |

## Headline Counts

| Metric | Count | Artifact |
|---|---:|---|
| Total collected routes | 1688 | `all_routes.jsonl` |
| Accessible 200 | 783 | `accessible_200.jsonl` |
| Exists / blocked (30x/401/403/405) | 7 | `exists_blocked.jsonl` |
| Other status (404/500/etc) | 0 | `other_status.jsonl` |
| Live subdomains | 1 | `subdomains.jsonl` |
| Real virtual hosts | 0 | `vhost_real.jsonl` |
| Blocked vhost checks | 1 | `vhost_blocked.jsonl` |
| JS endpoints | 0 | `js_endpoints.jsonl` |
| Feature flags / role guards | 0 | `jscope_findings.json` |
| AI & API candidates | 200 | `ai_feed.json` |
| Secret candidates | 0 | `secrets.jsonl` |
| Unpacked sourcemap files | 0 | `sourcemap_files.txt` |
| Nuclei findings | 0 | `nuclei.jsonl` |
| Third-party URLs | 45 | `third_party_routes.jsonl` |
| Method probe rows | 0 | `method_responses.jsonl` |

## High-Signal AI & API Candidates

| Status | Score | URL |
|---:|---:|---|
| 200 | 115 | `https://modelstudio.console.alibabacloud.com/$discovery` |
| 200 | 115 | `https://modelstudio.console.alibabacloud.com/$discovery/rest` |
| 200 | 115 | `https://modelstudio.console.alibabacloud.com/$discovery/rest?version=v1alpha` |
| 200 | 115 | `https://modelstudio.console.alibabacloud.com/$discovery/rest?version=v1beta` |
| 200 | 115 | `https://modelstudio.console.alibabacloud.com/.well-known/ai-plugin.json` |
| 200 | 115 | `https://modelstudio.console.alibabacloud.com/api/v1alpha` |
| 200 | 115 | `https://modelstudio.console.alibabacloud.com/api/v1beta` |
| 200 | 115 | `https://modelstudio.console.alibabacloud.com/llms-full.txt` |
| 200 | 115 | `https://modelstudio.console.alibabacloud.com/llms.txt` |
| 200 | 115 | `https://modelstudio.console.alibabacloud.com/swagger-ui` |
| 200 | 115 | `https://modelstudio.console.alibabacloud.com/v1alpha` |
| 200 | 115 | `https://modelstudio.console.alibabacloud.com/v1alpha/models` |
| 200 | 115 | `https://modelstudio.console.alibabacloud.com/v1beta` |
| 200 | 115 | `https://modelstudio.console.alibabacloud.com/v1beta/models` |
| 403 | 90 | `https://modelstudio.console.alibabacloud.com/openapi.json` |
| 403 | 90 | `https://modelstudio.console.alibabacloud.com/openapi.yaml` |
| 403 | 90 | `https://modelstudio.console.alibabacloud.com/swagger.json` |
| 403 | 90 | `https://modelstudio.console.alibabacloud.com/swagger.yaml` |
| 200 | 75 | `https://docs.modelstudio.console.alibabacloud.com/custom.js` |
| 200 | 75 | `https://modelstudio.console.alibabacloud.com/` |
| 200 | 75 | `https://modelstudio.console.alibabacloud.com/&amp` |
| 200 | 75 | `https://modelstudio.console.alibabacloud.com/&tab=dashboard` |
| 200 | 75 | `https://modelstudio.console.alibabacloud.com/)` |
| 200 | 75 | `https://modelstudio.console.alibabacloud.com/).` |
| 200 | 75 | `https://modelstudio.console.alibabacloud.com/...` |
| 200 | 75 | `https://modelstudio.console.alibabacloud.com/.well-known` |
| 200 | 75 | `https://modelstudio.console.alibabacloud.com/.well-known/aplus.js` |
| 200 | 75 | `https://modelstudio.console.alibabacloud.com/.well-known/apple-app-site-association` |
| 200 | 75 | `https://modelstudio.console.alibabacloud.com/.well-known/assetlinks.json` |
| 200 | 75 | `https://modelstudio.console.alibabacloud.com/.well-known/at.alicdn.com` |
| 200 | 75 | `https://modelstudio.console.alibabacloud.com/.well-known/at.alicdn.com/t/a/font_4647901_6oigtfhrla.css` |
| 200 | 75 | `https://modelstudio.console.alibabacloud.com/.well-known/bailian-fe/agent-playground` |
| 200 | 75 | `https://modelstudio.console.alibabacloud.com/.well-known/bailian-fe/bailian-agent-infra` |
| 200 | 75 | `https://modelstudio.console.alibabacloud.com/.well-known/bailian-fe/bailian-asset-center` |
| 200 | 75 | `https://modelstudio.console.alibabacloud.com/.well-known/bailian-fe/bailian-cli-landing` |
| 200 | 75 | `https://modelstudio.console.alibabacloud.com/.well-known/bailian-fe/bailian-connector` |
| 200 | 75 | `https://modelstudio.console.alibabacloud.com/.well-known/bailian-fe/bailian-costing-balance` |
| 200 | 75 | `https://modelstudio.console.alibabacloud.com/.well-known/bailian-fe/bailian-managed-agents` |
| 200 | 75 | `https://modelstudio.console.alibabacloud.com/.well-known/bailian-fe/bailian-memory` |
| 200 | 75 | `https://modelstudio.console.alibabacloud.com/.well-known/bailian-fe/bailian-micro-fe-agent-detail` |

## Feature Flags & Role Guards

_None found._

## Secret Candidates (Redacted)

_None found._

## Collapsed Route Patterns

| Pattern | Count | Sample |
|---|---:|---|
| `modelstudio.console.alibabacloud.com/ap-southeast-1` | 189 | `https://modelstudio.console.alibabacloud.com/ap-southeast-1` |
| `docs.modelstudio.console.alibabacloud.com/{locale}/model-studio/{slug}` | 138 | `http://docs.modelstudio.console.alibabacloud.com/en/model-studio/access-model-studio-through-privatelink` |
| `modelstudio.console.alibabacloud.com/` | 79 | `http://modelstudio.console.alibabacloud.com/` |
| `docs.modelstudio.console.alibabacloud.com/{locale}/model-studio/get-api-key` | 14 | `http://docs.modelstudio.console.alibabacloud.com/en/model-studio/get-api-key` |
| `modelstudio.console.alibabacloud.com/data/api.json` | 14 | `https://modelstudio.console.alibabacloud.com/data/api.json` |
| `docs.modelstudio.console.alibabacloud.com/{locale}/model-studio/token-plan-overview` | 12 | `http://docs.modelstudio.console.alibabacloud.com/en/model-studio/token-plan-overview` |
| `docs.modelstudio.console.alibabacloud.com/{locale}/model-studio/what-is-model-studio` | 12 | `http://docs.modelstudio.console.alibabacloud.com/en/model-studio/what-is-model-studio` |
| `docs.modelstudio.console.alibabacloud.com/{locale}/model-studio/model-pricing` | 11 | `http://docs.modelstudio.console.alibabacloud.com/en/model-studio/model-pricing` |
| `docs.modelstudio.console.alibabacloud.com/{locale}/model-studio/cli` | 11 | `https://docs.modelstudio.console.alibabacloud.com/en/model-studio/cli` |
| `docs.modelstudio.console.alibabacloud.com/{locale}/model-studio/first-api-call-to-qwen` | 10 | `http://docs.modelstudio.console.alibabacloud.com/en/model-studio/first-api-call-to-qwen` |
| `docs.modelstudio.console.alibabacloud.com/{locale}/model-studio/models` | 10 | `http://docs.modelstudio.console.alibabacloud.com/en/model-studio/models` |
| `docs.modelstudio.console.alibabacloud.com/{locale}/model-studio/new-free-quota` | 9 | `http://docs.modelstudio.console.alibabacloud.com/en/model-studio/new-free-quota` |
| `docs.modelstudio.console.alibabacloud.com/{locale}/model-studio/quota-management` | 9 | `http://docs.modelstudio.console.alibabacloud.com/en/model-studio/quota-management` |
| `docs.modelstudio.console.alibabacloud.com/{locale}/model-studio/rate-limit` | 9 | `http://docs.modelstudio.console.alibabacloud.com/en/model-studio/rate-limit` |
| `docs.modelstudio.console.alibabacloud.com/{locale}/model-studio/regions` | 9 | `http://docs.modelstudio.console.alibabacloud.com/en/model-studio/regions` |
| `modelstudio.console.alibabacloud.com/ap-southeast-1/costing-balance/free-quota` | 9 | `https://modelstudio.console.alibabacloud.com/ap-southeast-1/costing-balance/free-quota` |
| `modelstudio.console.alibabacloud.com/us-east-1` | 9 | `https://modelstudio.console.alibabacloud.com/us-east-1` |
| `modelstudio.console.alibabacloud.com/ap-southeast-1/model/market` | 8 | `https://modelstudio.console.alibabacloud.com/ap-southeast-1/model/market` |
| `modelstudio.console.alibabacloud.com/ap-southeast-1/model/market/detail/qwen3.8-flash` | 7 | `http://modelstudio.console.alibabacloud.com/ap-southeast-1/model/market/detail/qwen3.8-flash?file=qwen3.8-flash&serviceSite=international&spm=a2c63.p38356.0.0.5b93776ffI0ynv` |
| `docs.modelstudio.console.alibabacloud.com/{locale}/model-studio/base-url` | 7 | `https://docs.modelstudio.console.alibabacloud.com/en/model-studio/base-url` |
| `modelstudio.console.alibabacloud.com/ap-southeast-1/subscription/overview` | 7 | `https://modelstudio.console.alibabacloud.com/ap-southeast-1/subscription/overview` |
| `modelstudio.console.alibabacloud.com/ap-southeast-1/subscription/token-plan` | 7 | `https://modelstudio.console.alibabacloud.com/ap-southeast-1/subscription/token-plan` |
| `modelstudio.console.alibabacloud.com/eu-central-1` | 7 | `https://modelstudio.console.alibabacloud.com/eu-central-1` |
| `docs.modelstudio.console.alibabacloud.com/{locale}/model-studio/budget-management` | 6 | `http://docs.modelstudio.console.alibabacloud.com/en/model-studio/budget-management` |
| `modelstudio.console.alibabacloud.com/cn-beijing` | 6 | `https://modelstudio.console.alibabacloud.com/cn-beijing` |
| `modelstudio.console.alibabacloud.com/cn-hongkong` | 6 | `https://modelstudio.console.alibabacloud.com/cn-hongkong` |
| `docs.modelstudio.console.alibabacloud.com/{locale}` | 4 | `http://docs.modelstudio.console.alibabacloud.com/en` |
| `modelstudio.console.alibabacloud.com/{locale}` | 4 | `https://modelstudio.console.alibabacloud.com/ap` |
| `modelstudio.console.alibabacloud.com/ap-northeast-1` | 4 | `https://modelstudio.console.alibabacloud.com/ap-northeast-1` |
| `modelstudio.console.alibabacloud.com/ap-northeast-1/model/market` | 4 | `https://modelstudio.console.alibabacloud.com/ap-northeast-1/model/market` |
| `modelstudio.console.alibabacloud.com/ap-southeast-1/model/market/detail/qwen-image-2.1-turbo` | 4 | `https://modelstudio.console.alibabacloud.com/ap-southeast-1/model/market/detail/qwen-image-2.1-turbo` |
| `modelstudio.console.alibabacloud.com/ap-southeast-1/model/market/detail/qwen3.8-max` | 4 | `https://modelstudio.console.alibabacloud.com/ap-southeast-1/model/market/detail/qwen3.8-max` |
| `modelstudio.console.alibabacloud.com/ap-southeast-1/subscription/token-plan/personal` | 4 | `https://modelstudio.console.alibabacloud.com/ap-southeast-1/subscription/token-plan/personal` |
| `docs.modelstudio.console.alibabacloud.com/{locale}/model-studio/cli/overview` | 3 | `http://docs.modelstudio.console.alibabacloud.com/en/model-studio/cli/overview` |
| `docs.modelstudio.console.alibabacloud.com/{locale}/model-studio/optimize-prompt` | 3 | `https://docs.modelstudio.console.alibabacloud.com/en/model-studio/optimize-prompt` |
| `docs.modelstudio.console.alibabacloud.com/{locale}/model-studio/prompt-custom-template` | 3 | `https://docs.modelstudio.console.alibabacloud.com/en/model-studio/prompt-custom-template` |
| `docs.modelstudio.console.alibabacloud.com/{locale}/model-studio/prompt-template` | 3 | `https://docs.modelstudio.console.alibabacloud.com/en/model-studio/prompt-template` |
| `docs.modelstudio.console.alibabacloud.com/{locale}/model-studio/token-plan-personal-faq` | 3 | `https://docs.modelstudio.console.alibabacloud.com/en/model-studio/token-plan-personal-faq` |
| `docs.modelstudio.console.alibabacloud.com/{locale}/model-studio/workflow-application` | 3 | `https://docs.modelstudio.console.alibabacloud.com/en/model-studio/workflow-application` |
| `modelstudio.console.alibabacloud.com/$discovery/rest` | 3 | `https://modelstudio.console.alibabacloud.com/$discovery/rest` |

## Nuclei Findings

_None found._

## Tool Status

| Tool | Exit | Duration (s) | Detail |
|---|---:|---:|---|
| `scrapling` | 0 | 1.3 | 0 URLs/JS captured |
| `katana` | 2 | 12.3 | p1=1, p2=0 |
| `subfinder+dnsx` | 0 | 26.5 | 1 subs, 1 live |
| `wellknown_ai` | 0 | 23.0 | 19 paths checked |
| `waymore` | 0 | 67.1 | 932 archive URLs |
| `urlfinder` | 0 | 36.6 | 889 URLs |
| `chunk_download` | 0 | 3.7 | 29 fetched -> 26 unique SHA-256 chunks |
| `sourcemapper` | 0 | 0.0 | 0 maps -> 0 unpacked sources |
| `jsluice` | 0 | 0.2 | 4 chunks -> 60 URLs |
| `xnLinkFinder` | 0 | 0.4 | 0 endpoints |
| `jscope` | 0 | 0.7 | 4 files -> 0 flags/models |
| `secrets_offline` | 0 | 6.6 | 0 candidates |
| `httpx` | 124 | 75.2 | 1 probed |
| `vhost` | 0 | 1.2 | 0 real / 1 tested |
| `targeted_fuzz` | 0 | 53.0 | 1 prefixes -> 789 hits |
| `x8` | 0 | 50.8 | 8 API routes scanned |
| `methods` | 0 | 0.0 | 0 probes |
| `nuclei` | 1 | 0.1 | 0 findings across 150 URLs |
