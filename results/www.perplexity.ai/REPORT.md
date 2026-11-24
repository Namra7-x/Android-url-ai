# Hunt Report — https://www.perplexity.ai

Generated: 2026-11-24T19:12:09Z &nbsp;|&nbsp; Duration: 12m 12s

> **Nothing is filtered during collection. This report is only a grouping.**

## Summary

| What | Count | Meaning |
|---|---:|---|
| Routes collected | 28167 | Every URL found, nothing removed |
| Distinct routes verified | 6847 | One row per URL (method probes excluded) |
| HTTP responses | 6859 | Includes method probes — kept in `method_responses.jsonl` |
| **Accessible (200)** | **2** | Confirmed live — the wins |
| Exists but different status | 6844 | 301/302/401/403/405 — real route, blocked |
| Other responses | 1 | 404/500/etc — kept, not discarded |
| Subdomains (resolved) | 0 | DNS-verified |
| Virtual hosts (real) | 0 | Cloudflare 403/530/0 excluded |
| Parameters | 2 | URLs with query params |
| JS endpoints (AST) | 28157 | anastasis evidence-backed |
| First-party URLs | 28166 | perplexity.ai and subdomains |
| Third-party URLs | 1 | kept in `third_party_routes.jsonl` |
| Method responses | 14 | kept in `method_responses.jsonl` |
| Blocked vhost checks | 0 | kept in `vhost_blocked.jsonl` |
| Secret candidates | 0 | verify manually |

> Collection keeps third-party URLs by design (1). See `third_party_routes.jsonl`. Method-probe responses are in `method_responses.jsonl`.

## 0. TOP ROUTE PATTERNS (IDs collapsed)

| Pattern | Count |
|---|---:|
| `/ar-SA/hub/blog/{id}` | 189 |
| `/bg/hub/blog/{id}` | 189 |
| `/bn/hub/blog/{id}` | 189 |
| `/ca/hub/blog/{id}` | 189 |
| `/cs/hub/blog/{id}` | 189 |
| `/da/hub/blog/{id}` | 189 |
| `/de/hub/blog/{id}` | 189 |
| `/el/hub/blog/{id}` | 189 |
| `/en-GB/hub/blog/{id}` | 189 |
| `/es-MX/hub/blog/{id}` | 189 |
| `/es/hub/blog/{id}` | 189 |
| `/et/hub/blog/{id}` | 189 |
| `/fr-CA/hub/blog/{id}` | 189 |
| `/fr/hub/blog/{id}` | 189 |
| `/gl/hub/blog/{id}` | 189 |
| `/he/hub/blog/{id}` | 189 |
| `/hi/hub/blog/{id}` | 189 |
| `/hr/hub/blog/{id}` | 189 |
| `/hu/hub/blog/{id}` | 189 |
| `/hub/blog/{id}` | 189 |
| `/id/hub/blog/{id}` | 189 |
| `/is/hub/blog/{id}` | 189 |
| `/it/hub/blog/{id}` | 189 |
| `/ja/hub/blog/{id}` | 189 |
| `/kk/hub/blog/{id}` | 189 |
| `/kn/hub/blog/{id}` | 189 |
| `/ko/hub/blog/{id}` | 189 |
| `/lt/hub/blog/{id}` | 189 |
| `/lv/hub/blog/{id}` | 189 |
| `/ml/hub/blog/{id}` | 189 |
| `/mr/hub/blog/{id}` | 189 |
| `/nb/hub/blog/{id}` | 189 |
| `/nl/hub/blog/{id}` | 189 |
| `/pl/hub/blog/{id}` | 189 |
| `/pt-PT/hub/blog/{id}` | 189 |
| `/pt/hub/blog/{id}` | 189 |
| `/ro/hub/blog/{id}` | 189 |
| `/ru/hub/blog/{id}` | 189 |
| `/sk/hub/blog/{id}` | 189 |
| `/sr-Cyrl-ME/hub/blog/{id}` | 189 |

## 1. SUCCESS — HTTP 200

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 200 | GET | `https://challenges.cloudflare.com` | text/html | 5397 |  |
| 200 | GET | `https://perplexity.ai/cdn-cgi/challenge-platform/h/b/orchestrate/chl_page/v1?ray=a5faa8156aa8883b` | application/javascript | 616586 |  |

## 2. EXISTS BUT DIFFERENT STATUS (301/302/401/403/405)

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 301 | GET | `https://perplexity.ai` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/?__cf_chl_rt_tk=MXdvpm1x4lnDOzYLEeJ4xDz4cn4W2Zqu6Zflgm1.YEE-1795546827-1.0.1.1-T.EH3rfkS.H6DEvd.7yE03W5TExQPxvHpM0JCYqkI9c` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/academic` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/api-platform` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/api/auth/session` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/app` | text/html | 167 |  |
| 302 | GET | `https://perplexity.ai/app/sports` | text/html | 143 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/api-platform` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/changelog` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/changelog/april-2025-product-update` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/changelog/comet-voice-mode-improvements` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/academy` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/academy/how-to-use-automations` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/academy/how-to-use-connectors` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/academy/managing-computer-credits` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/academy/perplexity-computer-in-slack` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/academy/personal-computer-for-mac` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/academy/search-vs-computer` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/academy/what-is-perplexity-computer` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/blog/accelerating-sonar-through-speculation` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/careers` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/careers/interview-guide` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers/alix-partners` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers/apollo` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers/bvp` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers/clinikally` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers/combinely` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers/findly` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers/fintool` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers/get-maine-lobster` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers/gunderson` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers/inteleos` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers/ivp` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers/lambda` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers/latham-watkins` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers/lee-enterprises` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers/maeil` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers/mdnrc` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers/metal-ai` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers/model-ml` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers/nationgraph` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers/nemetschek-group` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers/paypal` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers/ramp` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers/rho` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers/rosenxt` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers/rox` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers/sap` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers/usada` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers/woven-health-collective` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/customers/zoom` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/getting-started` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/guides` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/guides/comet-for-sales` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/guides/computer-for-counsel` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/guides/computer-for-growing-businesses` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/guides/computer-for-hedge-funds` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/guides/computer-for-private-equity` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/guides/computer-for-professional-finance` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/guides/computer-for-wealth-management` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/guides/enterprise-ai-buyers-guide` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/guides/how-perplexity-uses-computer` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/guides/perplexity-at-work` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/guides/perplexity-computer-at-work` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/guides/premium-sources-guide` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/guides/strategic-planning-guide` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/legal` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/legal/ai-strategy-consultation-offer` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/legal/campus-partners-program-terms` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/legal/comet-terms-of-service` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/legal/dpa` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/legal/dsa-information` | text/html | 167 |  |
| 301 | GET | `https://perplexity.ai/ar-SA/hub/legal/enterprise-agentic-specific-terms` | text/html | 167 |  |
| … | … | _6769 more in JSONL_ | … | … | … |

## 3. OTHER RESPONSES — kept, never discarded

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 400 | GET | `https://perplexity.ai/cdn-cgi/challenge-platform/h/b/fo/4209888723:1795545021:GXpcJSTbFpB0Zf_RQmhFKJwPrfvJT9G-elbOXYuwU-A/a5faa8156aa8883b/.ZWqHy5jYZyIMxKD5xLK..b1aaSlDX1XqzKONuVLTi4-1795546827-1.2.1.1-4iML8QRpKw3.EkBGMFqrY2nlazfA0XfwfjixMUGN0oGrjaHYDi.hDY_9oKWs637v` | application/json | 121 |  |

## 4. DATA FILES (accessible)

_None in this category._

## 5. SUBDOMAINS (detailed)

Found **0**, DNS-resolved **0**.

| Host | Resolved | Source |
|---|---|---|

## 6. VIRTUAL HOSTS (real statuses only)

_No non-blocked virtual hosts found._
Blocked/noisy vhost checks (403/530/0) are kept in `vhost_blocked.jsonl` (0).

## 7. JS ENDPOINTS (AST, evidence-backed)

| Method | Path | Confidence |
|---|---|---|
| GET | `/ar-SA/changelog/april-11th-2025-product-update` | None |
| GET | `/ar-SA/changelog/april-2025-product-update` | None |
| GET | `/ar-SA/changelog/automations-inline-visualizations-and-gpt-6-1-sol` | None |
| GET | `/ar-SA/changelog/brain-faster-computer-models-website-publishing` | None |
| GET | `/ar-SA/changelog/comet-voice-mode-improvements` | None |
| GET | `/ar-SA/changelog/computer-in-email-gpt-5-6-terra-luna-and-grok-4-6` | None |
| GET | `/ar-SA/changelog/computer-in-microsoft-365-improved-context-visibility-and-new-analytics` | None |
| GET | `/ar-SA/changelog/deep-research-command-panel-forking-inline-actions-and-enterprise-controls` | None |
| GET | `/ar-SA/changelog/effort-mode-gpt-6-astra-and-skills-marketplace` | None |
| GET | `/ar-SA/changelog/improved-computer-models-and-enterprise-updates---may-4-2026` | None |
| GET | `/ar-SA/changelog/personal-computer-for-all-users-on-mac` | None |
| GET | `/ar-SA/changelog/personal-computer-on-mac-launch-and-computer-updates---april-17-2026` | None |
| GET | `/ar-SA/changelog/role-based-access-controls-api-credentials-and-brain-for-max` | None |
| GET | `/ar-SA/changelog/shared-workspaces-personal-computer-for-windows-and-model-council` | None |
| GET | `/ar-SA/changelog/teammates-fully-local-computer-on-mac-and-voice-mode` | None |
| GET | `/ar-SA/changelog/ultrafast-computer-models-decisions-api-and-connector-controls` | None |
| GET | `/ar-SA/changelog/what-we-shipped---december-12th` | None |
| GET | `/ar-SA/changelog/what-we-shipped---december-5th` | None |
| GET | `/ar-SA/changelog/what-we-shipped---february-13-2026` | None |
| GET | `/ar-SA/changelog/what-we-shipped---february-20th-2026` | None |
| GET | `/ar-SA/changelog/what-we-shipped---february-27-2026` | None |
| GET | `/ar-SA/changelog/what-we-shipped---february-6th-2026` | None |
| GET | `/ar-SA/changelog/what-we-shipped---january-16-2026` | None |
| GET | `/ar-SA/changelog/what-we-shipped---march-13-2026` | None |
| GET | `/ar-SA/changelog/what-we-shipped---march-6-2026` | None |
| GET | `/ar-SA/changelog/what-we-shipped--march-27-2026` | None |
| GET | `/ar-SA/changelog/what-we-shipped-april-18th` | None |
| GET | `/ar-SA/changelog/what-we-shipped-april-25th` | None |
| GET | `/ar-SA/changelog/what-we-shipped-august-15th` | None |
| GET | `/ar-SA/changelog/what-we-shipped-august-8th` | None |
| GET | `/ar-SA/changelog/what-we-shipped-july-18th` | None |
| GET | `/ar-SA/changelog/what-we-shipped-july-25th` | None |
| GET | `/ar-SA/changelog/what-we-shipped-june-13th` | None |
| GET | `/ar-SA/changelog/what-we-shipped-june-27th` | None |
| GET | `/ar-SA/changelog/what-we-shipped-june-6th` | None |
| GET | `/ar-SA/changelog/what-we-shipped-may-19th` | None |
| GET | `/ar-SA/changelog/what-we-shipped-may-23rd` | None |
| GET | `/ar-SA/changelog/what-we-shipped-may-2nd` | None |
| GET | `/ar-SA/changelog/what-we-shipped-may-30th` | None |
| GET | `/ar-SA/changelog/what-we-shipped-november-14th` | None |
| GET | `/ar-SA/changelog/what-we-shipped-november-22nd` | None |
| GET | `/ar-SA/changelog/what-we-shipped-october-17th` | None |
| GET | `/ar-SA/changelog/what-we-shipped-october-25th` | None |
| GET | `/ar-SA/changelog/what-we-shipped-october-3rd` | None |
| GET | `/ar-SA/changelog/what-we-shipped-september-12th` | None |
| GET | `/ar-SA/changelog/what-we-shipped-september-19th` | None |
| GET | `/ar-SA/changelog/what-we-shipped-september-26th` | None |
| GET | `/ar-SA/changelog/what-we-shipped-september-5th` | None |
| GET | `/ar-SA/hub/academy/how-to-use-automations` | None |
| GET | `/ar-SA/hub/academy/how-to-use-computer-analytics` | None |
| GET | `/ar-SA/hub/academy/how-to-use-computer-skills` | None |
| GET | `/ar-SA/hub/academy/how-to-use-connectors` | None |
| GET | `/ar-SA/hub/academy/how-to-use-model-council` | None |
| GET | `/ar-SA/hub/academy/managing-computer-credits` | None |
| GET | `/ar-SA/hub/academy/perplexity-computer-in-microsoft-teams` | None |
| GET | `/ar-SA/hub/academy/perplexity-computer-in-slack` | None |
| GET | `/ar-SA/hub/academy/perplexity-computer-query-best-practices` | None |
| GET | `/ar-SA/hub/academy/personal-computer-for-mac` | None |
| GET | `/ar-SA/hub/academy/search-vs-computer` | None |
| GET | `/ar-SA/hub/academy/what-is-perplexity-computer` | None |
| GET | `/ar-SA/hub/blog/a-good-teacher-meets-the-student-where-they-are` | None |
| GET | `/ar-SA/hub/blog/a-local-first-agent-for-private-and-cost-effective-knowledge-work` | None |
| GET | `/ar-SA/hub/blog/a-student-s-guide-to-using-perplexity-spaces` | None |
| GET | `/ar-SA/hub/blog/about-the-dow-jones-lawsuit` | None |
| GET | `/ar-SA/hub/blog/accelerating-sonar-through-speculation` | None |
| GET | `/ar-SA/hub/blog/advancing-search-augmented-language-models` | None |
| GET | `/ar-SA/hub/blog/agent-api-a-managed-runtime-for-agentic-workflows` | None |
| GET | `/ar-SA/hub/blog/agent-api-now-supports-reusable-agents` | None |
| GET | `/ar-SA/hub/blog/agent-api-one-place-to-build-with-llms-the-web-and-agents` | None |
| GET | `/ar-SA/hub/blog/agent-vs-mcp` | None |
| GET | `/ar-SA/hub/blog/agents-or-bots-making-sense-of-ai-on-the-open-web` | None |
| GET | `/ar-SA/hub/blog/agi-vs-ai` | None |
| GET | `/ar-SA/hub/blog/ai-accessibility` | None |
| GET | `/ar-SA/hub/blog/ai-agent-evaluation` | None |
| GET | `/ar-SA/hub/blog/ai-agent-memory` | None |
| GET | `/ar-SA/hub/blog/ai-agent-orchestration` | None |
| GET | `/ar-SA/hub/blog/ai-alignment` | None |
| GET | `/ar-SA/hub/blog/ai-at-work-getting-more-done-with-less-hype` | None |
| GET | `/ar-SA/hub/blog/ai-collaboration-tools` | None |
| GET | `/ar-SA/hub/blog/ai-compliance` | None |
| GET | `/ar-SA/hub/blog/ai-costs` | None |
| GET | `/ar-SA/hub/blog/ai-data-enrichment` | None |
| GET | `/ar-SA/hub/blog/ai-detector` | None |
| GET | `/ar-SA/hub/blog/ai-for-market-research` | None |
| GET | `/ar-SA/hub/blog/ai-gateway` | None |
| GET | `/ar-SA/hub/blog/ai-guardrails` | None |
| GET | `/ar-SA/hub/blog/ai-hallucination` | None |
| GET | `/ar-SA/hub/blog/ai-in-the-workplace` | None |
| GET | `/ar-SA/hub/blog/ai-integration` | None |
| GET | `/ar-SA/hub/blog/ai-literacy` | None |
| GET | `/ar-SA/hub/blog/ai-maturity` | None |
| GET | `/ar-SA/hub/blog/ai-memory` | None |
| GET | `/ar-SA/hub/blog/ai-personal-assistants` | None |
| GET | `/ar-SA/hub/blog/ai-research` | None |
| GET | `/ar-SA/hub/blog/ai-tools-for-consultants` | None |
| GET | `/ar-SA/hub/blog/announcing-comet-plus-launch-partners` | None |
| GET | `/ar-SA/hub/blog/announcing-our-global-partnership-with-motorola` | None |
| GET | `/ar-SA/hub/blog/announcing-our-partnership-with-the-united-states-government` | None |
| GET | `/ar-SA/hub/blog/announcing-our-series-a-funding-round-and-mobile-app-launch` | None |
| GET | `/ar-SA/hub/blog/announcing-premium-health-sources` | None |

## 8. PARAMETERS

| URL | Params |
|---|---|
| `https://perplexity.ai/?__cf_chl_rt_tk=MXdvpm1x4lnDOzYLEeJ4xDz4cn4W2Zqu6Zflgm1.YEE-1795546827-1.0.1.1-T.EH3rfkS.H6DEvd.7yE03W5TExQPxvHpM0JCYqkI9c` | __cf_chl_rt_tk |
| `https://perplexity.ai/cdn-cgi/challenge-platform/h/b/orchestrate/chl_page/v1?ray=a5faa8156aa8883b` | ray |

## 9. SECRET CANDIDATES

_None found._

## 10. NUCLEI FINDINGS (verified exposures / misconfigs)

| Severity | Template | Host |
|---|---|---|
| info | `dns-waf-detect` | `perplexity.ai` |
| info | `dns-waf-detect` | `challenges.cloudflare.com` |
| info | `azure-domain-tenant` | `challenges.cloudflare.com` |
| info | `waf-detect` | `perplexity.ai` |
| info | `waf-detect` | `challenges.cloudflare.com` |
| info | `tech-detect` | `challenges.cloudflare.com` |
| info | `missing-cookie-samesite-strict` | `perplexity.ai` |
| info | `tech-detect` | `perplexity.ai` |
| info | `xss-deprecated-header` | `challenges.cloudflare.com` |
| info | `http-missing-security-headers` | `challenges.cloudflare.com` |
| info | `http-missing-security-headers` | `challenges.cloudflare.com` |
| info | `http-missing-security-headers` | `perplexity.ai` |
| info | `http-missing-security-headers` | `perplexity.ai` |
| info | `http-missing-security-headers` | `perplexity.ai` |
| info | `http-missing-security-headers` | `perplexity.ai` |
| info | `http-missing-security-headers` | `perplexity.ai` |
| info | `http-missing-security-headers` | `perplexity.ai` |
| info | `http-missing-security-headers` | `perplexity.ai` |
| info | `http-missing-security-headers` | `perplexity.ai` |
| info | `http-missing-security-headers` | `perplexity.ai` |

## 11. TOOL RUN STATUS (no silent skips)

| Tool | Result | Detail |
|---|---|---|
| `anastasis` | OK | 28157 endpoints, 0 params |
| `cariddi` | OK | completed |
| `ffuf` | OK | off by choice — wordlist prepared |
| `getJS` | exit 2 | see logs/ |
| `httpx` | OK | completed |
| `js-download` | OK | no JS URLs found |
| `jscope` | OK | no local chunks to analyse |
| `jsluice` | OK | 0 files parsed in batches of 100 |
| `katana` | OK | completed |
| `methods` | OK | 14 method responses |
| `noseyparker` | OK | no chunks |
| `nuclei` | OK | 20 findings on 2 live hosts |
| `subfinder` | OK | completed |
| `subjs` | OK | completed |
| `trufflehog` | OK | completed |
| `uncover` | OK | no API key configured — no external data |
| `urlfinder` | OK | completed |
| `uro` | OK | completed |
| `vhost` | OK | no subdomain names |
| `waybackurls` | OK | completed |
| `x8` | OK | parameter scan complete |

## 12. INTENTIONALLY NOT RUN

- **ffuf path brute** — off by default; `wordlist.txt` is ready. Set `enable_brute: true` later.
- **kiterunner** — off by default alongside ffuf.

## 13. OUTPUT FILES

| File | Meaning |
|---|---|
| [`all_routes.jsonl`](all_routes.jsonl) | every route, unfiltered (5,040,905 B) |
| [`accessible_200.jsonl`](accessible_200.jsonl) | HTTP 200 wins (1,751 B) |
| [`exists_blocked.jsonl`](exists_blocked.jsonl) | exists but blocked (5,984,213 B) |
| [`other_status.jsonl`](other_status.jsonl) | all other statuses (1,426 B) |
| [`data_files.jsonl`](data_files.jsonl) | JSON/CSV/XML among 200s (0 B) |
| [`params.jsonl`](params.jsonl) | parameters (348 B) |
| [`subdomains.jsonl`](subdomains.jsonl) | subdomains + resolution (0 B) |
| [`third_party_routes.jsonl`](third_party_routes.jsonl) | third-party URLs — kept, not deleted (106 B) |
| [`method_responses.jsonl`](method_responses.jsonl) | all method-probe responses — kept (1,898 B) |
| [`vhost_real.jsonl`](vhost_real.jsonl) | non-blocked virtual hosts (0 B) |
| [`vhost_blocked.jsonl`](vhost_blocked.jsonl) | blocked vhost checks — kept (0 B) |
| [`js_endpoints.jsonl`](js_endpoints.jsonl) | AST endpoints (3,322,062 B) |
| [`jsluice.jsonl`](jsluice.jsonl) | JS-derived URLs (0 B) |
| [`cariddi.txt`](cariddi.txt) | crawl + secrets/endpoints (263 B) |
| [`wayback_urls.txt`](wayback_urls.txt) | archive URLs (1 B) |
| [`nuclei.jsonl`](nuclei.jsonl) | verified exposure findings (6,864,680 B) |
| [`anastasis_endpoints.jsonl`](anastasis_endpoints.jsonl) | AST endpoints (3,322,062 B) |
| [`secrets.jsonl`](secrets.jsonl) | secret candidates (0 B) |
| [`wordlist.txt`](wordlist.txt) | target-specific fuzz list (270,306 B) |
| [`params.txt`](params.txt) | parameter wordlist (19 B) |
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