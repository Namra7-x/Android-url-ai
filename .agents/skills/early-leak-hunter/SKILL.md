---
name: early-leak-hunter
description: >-
  Reusable field manual for discovering deploy-ahead, first-party signals in
  public web artifacts: service workers, environment maps, build manifests,
  JavaScript chunks, source maps, inline runtime config, API schemas, SDK type
  definitions, status feeds, and public data surfaces. Use when hunting for new
  model IDs, unreleased features, internal environment names, staging routes,
  feature flags, or early infrastructure changes without using credentials,
  bypassing authentication, or probing internal hosts.
---

# Early Leak Hunter — Hidden Foundry Field Manual

This skill is a reusable method for finding what a product has already shipped
before it announces it. It is written for public-source, first-party artifact
analysis. It is not a list of endpoints, and it is not a target-specific dump.

> **Core rule:** find the artifact that had to exist for the product to work.
> A page is a rendering. A bundle, worker, manifest, schema, or build graph is
> the machinery. The machinery is where the early signal lives.

> **Claim rule:** do not call something a leak because it looks internal.
> A leak needs first-party, deploy-ahead evidence and a reproducible capture.
> A key, a hostname, or a 403 is a lead until proven otherwise.

> **Boundary rule:** extract names and structure from public artifacts.
> Never use discovered keys, cookies, tokens, or sessions. Never bypass auth.
> Never probe corp, internal, staging, or preprod hosts.

---

## 0. Mission

Given a target product, find:

- model IDs and capability names that are not public yet;
- routes, services, and methods that the UI does not expose;
- environment maps that reveal the release pipeline;
- feature flags and experiment names before they flip on;
- build metadata that dates a deployment;
- schema fields and SDK types for unreleased features;
- public data surfaces that answer anonymously;
- operational signals that explain a rollout or outage.

The output is not a pile of URLs. The output is a small set of **verified,
deploy-ahead signals** with evidence and a monitoring plan.

---

## 1. Operating rules

1. **Public artifacts only.** If it is not served to an anonymous visitor, it is
   out of scope for extraction.
2. **No credential use.** Never send a discovered key, cookie, token, or
   session to any backend.
3. **No auth bypass.** Do not test for IDOR, privilege escalation, token
   forwarding, path traversal, or open redirects.
4. **No internal host access.** You may record an internal hostname found in a
   public artifact. You may not resolve, fetch, or scan it.
5. **No mass fuzzing.** A small number of targeted, read-only requests is
   enough. One request per candidate is the default.
6. **Stop at the wall.** `401`, `403`, and `405` mean “blocked,” not “leak.”
7. **Evidence over adjectives.** Record status, content type, size, timestamp,
   and the exact artifact. Do not rely on memory.
8. **Docs are confirmation.** Changelogs, sitemaps, announcement pages, and
   marketing copy are useful for context, not for early discovery.
9. **No target-specific findings in this skill.** Keys, hosts, and codenames
   belong in a report or tracker, never in the reusable playbook.
10. **Do not overclaim.** A surface is not a leak because it is interesting.

---

## 2. The mental model: every product is a foundry

A web product is assembled from layers. Each layer answers a different
question and leaks a different kind of signal.

| Layer | Question | Typical signal |
|---|---|---|
| Shell | What does the browser load first? | Script tags, manifests, route names |
| Asset graph | What code exists beyond the first page? | Lazy chunks, workers, source maps |
| Runtime config | What does the app know before it renders? | Build IDs, flags, model lists |
| Transport | How does the app talk to the backend? | RPC methods, REST paths, GraphQL ops |
| Release metadata | How is the build identified? | Dates, versions, environment names |
| Supply chain | What ships to developers? | SDKs, type definitions, examples |
| Operations | How does the vendor run it? | Status feeds, incident history |

The early signal is usually in the layer the marketing site does not show:
the worker, the lazy chunk, the manifest, the embedded config, the schema, or
the SDK.

---

## 3. Source ladder

Track from strongest to weakest:

1. **Public source maps with original source** — rare, highest value.
2. **Service workers and environment maps** — pipeline names, backend stages,
   client keys, notification routes.
3. **Build manifests and lazy-chunk graphs** — code paths never linked on the
   visible page.
4. **Inline runtime config and hydration state** — model registries, flags,
   build IDs, experiment IDs.
5. **API schemas, RPC method lists, SDK types** — capability names and shapes.
6. **Public anonymous data endpoints** — verified data, not guesses.
7. **Status and incident feeds** — operational context.
8. **Docs, changelogs, sitemaps, announcements** — confirmation only.

If a source is at level 8, do not present it as an early signal.

---

## 4. The loop

```text
baseline -> map -> extract -> normalize -> diff -> verify -> score -> monitor
```

### 4.1 Baseline

Capture the current public state of the target:

- shell HTML and headers;
- all script and link URLs;
- service worker registration and scope;
- manifest files;
- main bundle and chunk URLs;
- build ID, version, or date strings;
- inline JSON/config blocks.

Store a hash and a timestamp. Do not alert on the first run.

### 4.2 Map

Build the asset graph:

- shell → scripts → chunks → workers → manifests;
- script → dynamic import targets;
- worker → `importScripts`, cache list, fetch handlers;
- page → inline state blocks;
- bundle → API client strings and route templates.

Do not stop at the first bundle. The interesting code is often lazy-loaded or
registered separately.

### 4.3 Extract

Extract identifiers, not prose. Typical categories:

- hosts and origins;
- paths and route templates;
- service and method names;
- model-like and product-like identifiers;
- feature flags, experiment names, and gate names;
- build IDs, versions, dates, and environment names;
- header names and auth hints;
- schema fields and enum values;
- chunk names and source-map references.

### 4.4 Normalize

Normalize before diffing:

- lowercase hostnames;
- strip volatile hashes from file names;
- canonicalize URL paths;
- sort sets;
- separate identifiers from values;
- collapse duplicate shapes;
- ignore cache-busters, nonces, timestamps, and counters.

### 4.5 Diff

Diff sets, not raw text. Report:

- **added** — new identifier, host, route, flag, key, chunk;
- **removed** — retired capability or endpoint;
- **changed** — same key, new value or new mapping;
- **moved** — same value, new path or environment.

A raw text diff is noisy. A normalized set diff is a signal.

### 4.6 Verify

Verify only what is public and anonymous:

- fetch the artifact itself;
- confirm content type and size;
- check that a source map is real JSON with `sources`, not an HTML soft-404;
- test an endpoint only if it is clearly public and read-only;
- use minimal bodies and a normal browser `Origin`/`Referer`;
- stop at `401`, `403`, or `405`.

### 4.7 Score

Score by deploy-ahead value and evidence quality. See section 9.

### 4.8 Monitor

Monitor the smallest set of sources that produced real signals. See section 10.

---

## 5. Surface playbooks

### 5.1 Service workers and environment maps

A service worker is production code with a separate lifecycle. It often
contains routing, push handling, and environment selection that the page
bundle does not.

Look for:

- registration path and scope;
- `importScripts`, cache names, and precache lists;
- `fetch`, `push`, and `notificationclick` handlers;
- hostname-to-environment selector functions;
- objects pairing an environment name, a backend origin, and a client key;
- `credentials`, `authorization`, and API-key header usage;
- request paths such as versioned API routes;
- deep-link schemes and internal notification targets.

**What the signal is:** the environment matrix. It reveals the release
pipeline, stage names, new hosts, and key rotations.

**What the signal is not:** a key by itself. A public client key is an
identifier, not a login. The same code often also needs cookies or an
authorization token. Do not test the key. Do not visit the hosts.

**Generic pattern to recognize:**

```text
environment object = { app name, client key, backend origin }
selector(hostname) -> environment object
request = backend origin + versioned path
headers = client key + optional authorization
credentials = include
```

When this pattern appears, extract the selector and the object table. Then
diff for new stages, new hosts, new routes, and new keys.

### 5.2 Build manifests and chunk graphs

Modern frontends split code across many files. The visible page loads only a
fraction of them.

Look for:

- script `src` and module `import` targets;
- dynamic import calls and chunk maps;
- `asset-manifest.json`, `manifest.json`, `_buildManifest.js`,
  `_ssgManifest.js`, or framework-specific equivalents;
- chunk names that mention models, billing, settings, agents, or admin;
- worker files and separately registered scripts;
- build IDs and content hashes.

The goal is to find the chunk that the UI loads only after a feature is
enabled. That chunk is often deployed before the feature is visible.

### 5.3 Source maps

Source maps are the highest-value artifact because they can contain original
source code.

Procedure:

1. Inspect the end of each JavaScript file for `sourceMappingURL`.
2. Request the referenced map.
3. Confirm the response is JSON with `version`, `sources`, and optionally
   `sourcesContent`.
4. If it is HTML, a login page, or an app shell, it is a soft-404. Do not call
   it a source map.
5. If it is real, extract type definitions, enum values, comments, API clients,
   and feature names.
6. Never execute the source; read it.

A 200 response is not enough. Content type and structure decide.

### 5.4 Inline runtime config and hydration state

Server-rendered apps often embed state before the client boots.

Look for:

- framework hydration blocks;
- `window.__INITIAL_STATE__`, `window.__CONFIG__`, or similar globals;
- inline JSON containing model lists, flags, tiers, or build IDs;
- bootstrap callbacks with escaped JSON;
- config objects whose keys look like environments or capabilities.

Extract the object, unescape it, and diff the sets. Do not scrape the rendered
text and call it a leak.

### 5.5 API schemas, RPC methods, and GraphQL operations

The transport layer names capabilities before the UI exposes them.

Look for:

- service names and method names;
- route templates with version prefixes;
- GraphQL operation names and field names;
- OpenAPI/JSON schema paths;
- SDK client methods;
- auth annotations or middleware names.

Classify each surface:

| Class | Meaning | Action |
|---|---|---|
| Public anonymous | Answers without credentials | Verify with a minimal read-only request |
| API-key-gated | Needs a public client key | Do not use a discovered key |
| Cookie/OAuth-gated | Needs a user session | Do not test |
| Blocked | 401/403/405 | Record as blocked, not a leak |

Do not try to turn an API-key-gated surface into an anonymous one.

### 5.6 SDKs, packages, and type definitions

Developer-facing packages often ship before the public announcement.

Look for:

- package registries and release tarballs;
- TypeScript type definitions and enums;
- example code and test fixtures;
- generated API clients;
- changelogs inside packages;
- source maps or bundled source in the package.

SDK types are strong because they are specific: a new enum member or method
name is harder to explain away than a marketing string.

### 5.7 Status and incident feeds

Public status feeds are operational, not model leaks, but they explain
rollouts and regressions.

Track:

- incident IDs;
- affected products;
- start and resolution times;
- new incident categories.

Use them as context. Do not present a status incident as an unreleased model.

### 5.8 Public storage and tenant surfaces

Only inspect storage that is linked from a public artifact and only at the
metadata level.

- Anonymous listing is a finding; downloading records is not necessary.
- Do not collect personal data.
- Do not enumerate tenants.
- Do not test write, delete, or upload operations.
- Record the smallest evidence that proves the exposure.

This surface is high-risk. Prefer to stop early and report the boundary.

---

## 6. Extraction vocabulary

### What to extract

- `host` and `origin`
- `path` and `route template`
- `service` and `method`
- `model` and `product` identifiers
- `flag`, `gate`, `experiment`, `toggle`
- `build`, `version`, `date`, `environment`
- `header` and `auth hint`
- `schema field` and `enum`
- `chunk` and `source map`
- `deep link` and `notification target`

### How to recognize model-like identifiers

Do not hardcode a list of vendor names. Use context:

- a string near `model`, `models`, `modelId`, `slug`, `variant`, or `alias`;
- a value in an enum or selector array;
- a value paired with context window, pricing, or capability fields;
- a value repeated across bundle, config, and SDK;
- a date-stamped or versioned identifier in a catalog.

A regex match alone is not a finding. Context makes it real.

### What not to extract

- personal data;
- session cookies;
- authorization headers;
- private keys;
- user identifiers;
- billing records;
- anything that requires a login to see.

If a string looks like a secret, record its **location and type**, not its
value, unless the value is already public and necessary to prove the exposure.

---

## 7. Normalization and diff rules

1. Normalize before comparing.
2. Diff sets, not lines.
3. Ignore counters, nonces, timestamps, and cache-busters.
4. Ignore build hashes unless the hash is the only change.
5. Keep “added,” “removed,” “changed,” and “moved” separate.
6. Deduplicate by `(source, category, identifier)`.
7. Preserve the raw artifact hash for evidence.
8. Timestamp every capture in UTC.

A good diff answers: “What new thing exists now that did not exist in the
previous build?”

---

## 8. Verification ladder

Use the weakest accurate label:

| Level | Evidence | Label |
|---|---|---|
| 0 | One string in one artifact | Observed |
| 1 | Same string in multiple artifacts | Corroborated |
| 2 | Public anonymous response | Verified public |
| 3 | Deploy-ahead response or source | Verified deploy-ahead |
| 4 | New capability with clear impact | Leak |
| 5 | Exploitable exposure with real data | Incident |

Rules:

- A hostname is level 0 until it is corroborated.
- A key is level 0 until its capability is demonstrated without using it.
- A 403 is not evidence of a leak.
- A public launch is not a leak.
- A source map that returns HTML is not a source map.
- Do not use “critical” for a string.

---

## 9. Scoring

| Priority | Criteria | Examples |
|---|---|---|
| **P0** | Deploy-ahead, specific, new capability or environment | New model enum, new stage host, new auth-less data endpoint, real source map |
| **P1** | Deploy-ahead but partial | New route, new method, new flag, key rotation, new manifest entry |
| **P2** | Context or confirmation | Build-only change, schema refresh, status incident, docs update |
| **Noise** | Not a signal | Counters, nonces, timestamps, cache-busters, unchanged rebuilds |

P0 does not mean “publish immediately.” It means “verify carefully and report
with evidence.”

---

## 10. Tracker design

### Schedule

- Fast-moving artifacts: every 6 hours.
- Slow-moving schemas and SDKs: every 24 hours.
- Status feeds: every 15–60 minutes if you actually need operational alerts.

### Storage

For each source, keep:

- URL;
- fetch timestamp;
- HTTP status and content type;
- SHA-256 of the raw body;
- normalized set of identifiers;
- previous normalized set;
- diff summary.

### Alerts

Alert only when a normalized set changes:

- new host;
- new stage name;
- new key identifier;
- new route or method;
- new model-like identifier;
- new flag or gate;
- new source-map reference;
- new build date that implies a deployment.

Do not alert on:

- a rebuild with identical sets;
- a counter increment;
- a changed hash with no semantic change;
- a docs refresh;
- a public launch you already knew about.

### Deduplication

Use a key such as:

```text
(source, category, identifier, value)
```

Store it in a small database or JSONL file. Never send the same event twice.

### Safety

The tracker fetches public artifacts only. It does not log in, does not send
keys, does not use cookies, and does not touch internal hosts.

---

## 11. Report template

```text
Claim:
Source:
Artifact:
Captured at (UTC):
Evidence:
What changed:
Why it is deploy-ahead:
Confidence:
Boundary:
Next check:
```

Write the claim so it survives scrutiny:

- “New environment name appears in the public worker” — good.
- “Internal staging is exposed” — only if you have a verified public response.
- “Key found” — not a leak by itself.
- “New model ID appears in the bundle and SDK types” — strong.

---

## 12. Anti-patterns

- Diffing documentation and calling it a leak.
- Treating a marketing page as an early signal.
- Calling a 403 a vulnerability.
- Calling a public key an access grant.
- Using a discovered key “just to check.”
- Hitting a corp, staging, or preprod host.
- Mass-fuzzing RPC methods.
- Reporting a soft-404 HTML page as a source map.
- Treating a regex match as a model launch.
- Reporting a public launch as a leak.
- Leaving target-specific findings in the reusable skill.

---

## 13. Reuse checklist

- [ ] Define the first-party boundary.
- [ ] Capture the shell and headers.
- [ ] Enumerate scripts, workers, manifests, and chunks.
- [ ] Fingerprint the build.
- [ ] Inspect the service worker for environment maps.
- [ ] Extract runtime config and hydration state.
- [ ] Extract RPC/REST/GraphQL/SDK identifiers.
- [ ] Check source maps structurally, not just by status.
- [ ] Normalize and diff sets.
- [ ] Verify only public anonymous surfaces.
- [ ] Score with the evidence ladder.
- [ ] Write the report with UTC timestamps.
- [ ] Build the smallest useful tracker.

---

## 14. Reference files

- `references/web-reversing-guide.md` — artifact graph, workers, chunks,
  source maps, runtime config, and verification.
- `references/discovery-archetypes.md` — reusable structural patterns for
  environment maps, build manifests, API gateways, SDKs, status feeds, and
  historical snapshots.
- `scripts/probe_endpoint.py` — optional read-only probe utility. Use it only
  on public, anonymous endpoints.

---

**Final rule:** the best early signal is a build artifact that is specific,
first-party, and already shipped. The worst early signal is a confident story
built on a string.
