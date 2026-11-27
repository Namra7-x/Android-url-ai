# Hunt Results

Generated: 2026-11-27T11:15:33Z

Open a target's **REPORT.md** for the human summary or **ai_feed.json** for compact LLM-ready leads.

| Target | Duration | Report | AI Feed | Accessible 200 | Exists/Blocked | Subdomains | JS Endpoints | Secrets/Flags | AI Leads | Nuclei | Routes |
|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

- **Duration** = wall-clock time (`min:sec`, capped at `<= 12:00`).
- **AI Feed** = deduplicated, ranked intelligence JSON (`ai_feed.json`) for LLM analysis.
- **Secrets/Flags** = secret candidates (`titus` + `trufflehog` + `jsluice` + `xnLinkFinder`) / feature flags & role guards (`Jscope`).
- **AI Leads** = `/v1alpha`, `/v1beta`, `/api/`, `graphql`, `llms.txt`, `openapi`, `$discovery`, model/config routes.
- **Accessible 200** = confirmed live routes; **Exists/Blocked** = `301/302/401/403/405`.
