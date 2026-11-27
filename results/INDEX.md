# Hunt Results

Generated: 2026-11-27T15:07:52Z

Open a target's **REPORT.md** for the human summary or **ai_feed.json** for compact LLM-ready leads.

| Target | Duration | Report | AI Feed | Accessible 200 | Exists/Blocked | Subdomains | JS Endpoints | Secrets/Flags | AI Leads | Nuclei | Routes |
|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `claude.ai` | 5:37 | [REPORT.md](claude.ai/REPORT.md) | [ai_feed.json](claude.ai/ai_feed.json) | 259 | 276 | 15 | 77 | 0/15 | 39 | 75 | 686 |
| `higgsfield.ai` | 8:47 | [REPORT.md](higgsfield.ai/REPORT.md) | [ai_feed.json](higgsfield.ai/ai_feed.json) | 581 | 1580 | 86 | 3021 | 0/238 | 200 | 0 | 103049 |
| `modelstudio.console.alibabacloud.com` | 4:54 | [REPORT.md](modelstudio.console.alibabacloud.com/REPORT.md) | [ai_feed.json](modelstudio.console.alibabacloud.com/ai_feed.json) | 783 | 7 | 1 | 0 | 0/0 | 200 | 0 | 1688 |

- **Duration** = wall-clock time (`min:sec`, capped at `<= 12:00`).
- **AI Feed** = deduplicated, ranked intelligence JSON (`ai_feed.json`) for LLM analysis.
- **Secrets/Flags** = secret candidates (`titus` + `trufflehog` + `jsluice` + `xnLinkFinder`) / feature flags & role guards (`Jscope`).
- **AI Leads** = `/v1alpha`, `/v1beta`, `/api/`, `graphql`, `llms.txt`, `openapi`, `$discovery`, model/config routes.
- **Accessible 200** = confirmed live routes; **Exists/Blocked** = `301/302/401/403/405`.
