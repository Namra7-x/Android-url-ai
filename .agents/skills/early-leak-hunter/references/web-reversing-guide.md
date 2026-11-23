# Web Asset & Frontend Bundle Reverse Engineering Guide

This guide is a reusable procedure for extracting deploy-ahead, first-party
signals from public web artifacts. It is intentionally target-agnostic: use
placeholders, not vendor-specific names.

---

## 0. Scope and boundary

You may:

- fetch public HTML, JavaScript, workers, manifests, schemas, and SDK packages;
- extract strings, routes, hosts, flags, identifiers, and build metadata;
- compare two public builds;
- make a small number of anonymous, read-only requests to public endpoints.

You may not:

- use discovered keys, cookies, tokens, or sessions;
- bypass authentication or authorization;
- probe corp, internal, staging, or preprod hosts;
- mass-fuzz methods;
- download personal data;
- test write, delete, or upload operations.

The guide is for understanding what is exposed. It is not for entering what is
supposed to be closed.

---

## 1. Build the artifact graph

Start with the shell, then follow every edge.

```text
shell
  -> script src / module import
  -> stylesheet
  -> manifest
  -> service worker registration
  -> inline config / hydration JSON
  -> preload / prefetch hints
```

Then, for each JavaScript artifact:

```text
bundle
  -> dynamic import()
  -> chunk map / asset manifest
  -> worker importScripts
  -> sourceMappingURL
  -> API client strings
  -> feature flag registry
```

Collect both the URL and the context: which page or file referenced it.

### Why this matters

The visible page rarely loads the interesting chunk. The chunk may be loaded
only after a feature flag turns on, a route is visited, or a worker receives a
push message. The build still contains it.

---

## 2. Fingerprint the build

Find the identifiers that let you tell one deployment from another:

- build ID or commit hash;
- build date or version string;
- content hash in asset names;
- framework-specific build manifest;
- service worker cache version;
- inline `window.__CONFIG__` or equivalent;
- `Last-Modified` / `ETag` headers.

Normalize the fingerprint. Do not treat every hash change as a signal. The
useful question is: “Did the semantic set change?”

---

## 3. Service workers and environment maps

A service worker is a public, separately deployed JavaScript artifact. It often
contains environment selection, push handling, caching, and cross-origin
requests.

### What to inspect

1. Registration URL and scope.
2. `importScripts` calls.
3. Cache names and precache lists.
4. `fetch` event handlers and request paths.
5. `push` and `notificationclick` handlers.
6. Hostname-to-environment selector functions.
7. Objects pairing an environment name, backend origin, and client key.
8. Header names such as API-key or authorization headers.
9. `credentials` mode.
10. Deep-link schemes and notification targets.

### Generic shape

```text
environment = { appName, clientKey, backendOrigin }
selectEnvironment(hostname) -> environment
request = backendOrigin + versionedPath
headers = clientKey + optional authorization
credentials = include
```

### How to read it

- The **environment table** is the signal. It reveals stage names and pipeline
  order.
- A **new stage** or **new host** is a deploy-ahead infrastructure signal.
- A **key rotation** is a release signal, not an access grant.
- The presence of `credentials` and an authorization flow means the key alone
  is not enough.
- Do not use the key. Do not visit the backend.

### What to extract

- environment labels;
- backend origins;
- client key identifiers (record location, not use);
- versioned request paths;
- auth header names;
- deep-link schemes.

### What not to claim

- “The key gives access.” You did not test it, and you should not.
- “The staging host is public.” A hostname in a public file is not proof that
  the host is reachable or authorized for you.
- “Internal environment leaked.” Say “the public worker exposes an environment
  map” unless you have a verified public response.

---

## 4. Chunk dissection

### Identify high-value chunks

Prioritize chunks whose names or nearby strings mention:

- models, catalogs, pricing, billing;
- chat, agents, tools, settings;
- auth, sessions, accounts;
- admin, internal, debug, preview;
- feature flags, experiments, gates.

### Extract from chunks

- route templates and path prefixes;
- service and method names;
- model-like identifiers with context;
- feature flag and experiment names;
- build metadata;
- hostnames and origins;
- schema field names;
- source-map references.

### Context beats regex

A model-like string is only a candidate. Promote it when it appears:

- in an enum or selector array;
- near `model`, `modelId`, `slug`, `variant`, or `alias`;
- with pricing, context window, or capability fields;
- in more than one artifact;
- in an SDK type definition.

A regex match alone is level 0 evidence.

---

## 5. Source maps

Source maps are the highest-value artifact when they are real.

### Procedure

1. Read the end of each JavaScript file.
2. Look for `sourceMappingURL`.
3. Request the referenced map.
4. Verify the response is JSON with `version`, `sources`, and optionally
   `sourcesContent`.
5. If the response is HTML, a login page, or an app shell, it is a soft-404.
6. If it is real, extract types, enums, comments, API clients, and feature names.
7. Never execute the source.

### Evidence rule

A 200 status is not enough. A real source map has a JSON structure and source
entries. A soft-404 is not a leak.

---

## 6. Runtime config and hydration state

Server-rendered apps often embed state before the client boots.

Look for:

- framework hydration blocks;
- `window.__INITIAL_STATE__`, `window.__CONFIG__`, or equivalent globals;
- inline JSON with model lists, flags, tiers, or build IDs;
- bootstrap callbacks with escaped JSON;
- config objects with environment or capability keys.

Extract the object, unescape it, and compare sets. Do not scrape rendered text
and call it a leak.

---

## 7. API surface

### What to map

- service names;
- method names;
- REST path templates;
- GraphQL operation names;
- OpenAPI/JSON schema paths;
- SDK client methods;
- auth middleware or annotations.

### Classify before testing

| Class | Meaning | Action |
|---|---|---|
| Public anonymous | Answers without credentials | Verify with one minimal read-only request |
| API-key-gated | Needs a public client key | Do not use a discovered key |
| Cookie/OAuth-gated | Needs a user session | Do not test |
| Blocked | 401/403/405 | Record as blocked |

### Test discipline

- one request per candidate;
- normal browser `Origin` and `Referer`;
- minimal body;
- no credentials;
- stop at the first auth wall;
- record status, content type, size, and a short snippet.

---

## 8. SDKs and packages

Developer packages are strong evidence because they are specific and versioned.

Inspect:

- package tarballs and registry metadata;
- TypeScript declarations and enums;
- generated API clients;
- examples and test fixtures;
- bundled source or source maps;
- package changelogs.

A new enum member or method name in a typed SDK is stronger than a marketing
string in a bundle.

---

## 9. Verification ladder

| Level | Evidence | Label |
|---|---|---|
| 0 | One string in one artifact | Observed |
| 1 | Same string in multiple artifacts | Corroborated |
| 2 | Public anonymous response | Verified public |
| 3 | Deploy-ahead response or source | Verified deploy-ahead |
| 4 | New capability with clear impact | Leak |
| 5 | Exploitable exposure with real data | Incident |

Do not jump levels. Most findings are level 0 or 1.

---

## 10. Normalization and diff

Normalize:

- lowercase hostnames;
- strip volatile hashes from file names;
- canonicalize paths;
- sort sets;
- separate identifiers from values;
- ignore counters, nonces, timestamps, and cache-busters.

Diff:

- added;
- removed;
- changed;
- moved.

Report only semantic changes. A rebuild with the same set is not a signal.

---

## 11. Boundaries and failure modes

- A 403 is not a leak.
- A public key is not a login.
- An HTML soft-404 is not a source map.
- A hostname in a worker is not proof of access.
- A regex match is not a launch.
- A docs change is not an early signal.
- A public announcement is not a leak.

When in doubt, downgrade the claim and preserve the evidence.
