# skills.md — Hidden Foundry: Reusable Early-Signal Hunting Skill

This is the short, human-readable doctrine behind
`.agents/skills/early-leak-hunter/SKILL.md`.

It is deliberately a **method**, not a list of endpoints. Targets change.
The method should survive the change.

## One-line goal

Find what a product has already shipped before the product says it exists.

## What counts as a real early signal

A real signal is:

- **First-party** — it comes from the vendor’s own public artifact.
- **Deploy-ahead** — it is present in a build before the announcement.
- **Specific** — a model ID, route, service method, flag, environment name,
  schema field, manifest entry, build date, or key rotation.
- **Reproducible** — you can show the artifact, the timestamp, and the diff.
- **Verified** — the claim matches the evidence level.

A real signal is not:

- a docs page, changelog, sitemap, or marketing page;
- a public launch described as a leak;
- a 401, 403, or 405;
- a guessed endpoint;
- a key with no demonstrated capability;
- a counter, nonce, cache-buster, or timestamp;
- “it looks internal.”

## The Hidden Foundry model

Every web product is assembled in layers. Each layer can leak a different
kind of signal:

1. **Shell** — HTML, route map, script tags, linked manifests.
2. **Asset graph** — main bundles, lazy chunks, CSS, workers, source maps.
3. **Runtime config** — inline JSON, hydration state, build IDs, flags.
4. **Transport** — RPC methods, REST paths, GraphQL operations, SDK clients.
5. **Release metadata** — build dates, version tags, environment selectors.
6. **Supply chain** — SDK packages, type definitions, examples, tarballs.
7. **Operations** — status feeds, incident history, public config endpoints.

The useful question is not “what does the page say?”
It is “what did the build have to ship in order for the page to work?”

## The loop

```text
baseline -> map -> extract -> normalize -> diff -> verify -> score -> monitor
```

1. **Baseline** the current public artifact.
2. **Map** the asset graph: shell, scripts, workers, manifests, config.
3. **Extract** identifiers, routes, hosts, flags, schemas, build metadata.
4. **Normalize** case, hashes, ordering, and duplicate shapes.
5. **Diff** sets, not raw text.
6. **Verify** only public, anonymous, read-only surfaces.
7. **Score** the signal by deploy-ahead value and evidence quality.
8. **Monitor** the smallest set of sources that produced real signals.

## Source ladder

Strongest to weakest:

1. Public source maps with original source.
2. Service workers and environment maps.
3. Build manifests and lazy-chunk graphs.
4. Inline runtime config and hydration state.
5. API schemas, RPC method lists, and SDK type definitions.
6. Public anonymous data endpoints.
7. Status and incident feeds.
8. Docs, changelogs, sitemaps, and announcement pages.

The bottom of the ladder is confirmation, not discovery.

## Service workers are underrated

A service worker is production JavaScript with a different job: it handles
push, caching, offline routing, and cross-origin fetches. That makes it a
high-value artifact.

Look for:

- hostname-to-environment selectors;
- backend hosts for dev, autopush, staging, preprod, and production;
- client keys paired with each environment;
- `fetch` handlers and request paths;
- `push` and `notificationclick` handlers;
- auth hints such as `credentials`, `authorization`, or API-key headers;
- deep-link schemes and internal route names.

The signal is the **environment map**, not the key. A key in a public artifact
is a client identifier. It is not a login, and it is not proof of access.
Extract the map. Do not use the keys. Do not touch the internal hosts.

## Verification ladder

Use precise language:

| Level | Evidence | What you can say |
|---|---|---|
| 0 | A string in a bundle | “Observed string” |
| 1 | Same string in two artifacts | “Corroborated build signal” |
| 2 | Public anonymous response | “Verified public surface” |
| 3 | Deploy-ahead response or source | “Verified deploy-ahead signal” |
| 4 | New capability with clear impact | “Leak” |
| 5 | Exploitable exposure with real data | “Incident” |

Do not jump from level 0 to level 4. Most bundle strings are just strings.

## Safety boundaries

- Use public artifacts and anonymous, read-only requests.
- Never use discovered keys, cookies, tokens, or sessions.
- Never bypass authentication or authorization.
- Never probe internal, corp, staging, or preprod hosts.
- Never mass-fuzz sensitive methods.
- Stop at `401`, `403`, or `405`; record it as blocked, not as a leak.
- Do not download or redistribute personal data.
- Do not put target-specific keys or hosts into this skill.

The skill is for **understanding what is exposed**, not for entering what is
supposed to be closed.

## Tracker recipe

Track only the sources that produce deploy-ahead signals:

- service worker;
- main bundle and build manifest;
- inline runtime config;
- API schema or SDK types;
- public status feed.

For each source:

1. Fetch with conditional headers where available.
2. Store a raw hash and a normalized set.
3. Baseline silently on the first run.
4. Diff added, removed, changed, and moved items.
5. Ignore counters and cache-busters.
6. Alert with source, timestamp, old value, new value, and evidence.
7. Deduplicate by source and identifier.

A good tracker is small, boring, and hard to fool.

## Report format

```text
Claim:
Source:
Artifact:
Captured at:
Evidence:
What changed:
Why it is deploy-ahead:
Confidence:
Boundary:
Next check:
```

## Reuse checklist

- [ ] Define the first-party boundary.
- [ ] Collect the shell and asset graph.
- [ ] Fingerprint the build.
- [ ] Inspect the service worker.
- [ ] Extract the chunk graph.
- [ ] Extract runtime config and flags.
- [ ] Extract API/schema/SDK identifiers.
- [ ] Normalize and diff.
- [ ] Verify only public surfaces.
- [ ] Score the evidence.
- [ ] Monitor the smallest useful set.

---

**Rule of thumb:** if the finding would survive without the word “maybe,” it is
probably real. If it needs “maybe,” it is a lead, not a leak.
