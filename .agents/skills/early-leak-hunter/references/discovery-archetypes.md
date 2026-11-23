# Web Endpoint & Artifact Discovery Archetypes

This reference describes reusable structural patterns, not vendor-specific
endpoints. Use the placeholders as a search vocabulary, then let the target's
own artifacts supply the real names.

---

## Archetype 1: Service worker environment matrix

A service worker often selects a backend by hostname and carries a table of
environment names, origins, and client keys.

### Structural patterns

```text
/{service-worker}.js
/{scope}/sw.js
/environment selector function:
    hostname includes {stage-host} -> {stage-object}
    hostname includes {other-stage-host} -> {other-stage-object}
environment object:
    { appName, clientKey, backendOrigin }
request:
    backendOrigin + /{version}/{method}
headers:
    {api-key-header}
    authorization
credentials:
    include
```

### Discovery heuristics

1. Find the service worker registration in the shell or main bundle.
2. Fetch the worker and inspect `fetch`, `push`, and `notificationclick`
   handlers.
3. Locate the hostname selector and the environment object table.
4. Extract stage names, origins, paths, and key **locations**.
5. Diff for new stages, new hosts, new routes, and key rotations.
6. Do not use the keys. Do not fetch the backend origins.

### Strong signals

- a new environment name;
- a new stage host;
- a new versioned request path;
- a key rotation for an existing stage;
- a new deep-link scheme or notification target.

### Weak signals

- a key alone;
- an internal-looking hostname alone;
- a comment or variable name alone.

---

## Archetype 2: Build manifest and lazy-chunk graph

The visible page loads only part of the application. Build manifests and
dynamic imports reveal the rest.

### Structural patterns

```text
/{framework}/static/{buildId}/_buildManifest.js
/{framework}/static/{buildId}/_ssgManifest.js
/asset-manifest.json
/manifest.json
/{chunk-path}/{name}-{hash}.js
import("./{chunk}")
__webpack_require__.e(...)
```

### Discovery heuristics

1. Extract every script, module, and manifest URL from the shell.
2. Parse the manifest to get the full chunk list.
3. Prioritize chunks whose names mention models, billing, settings, agents,
   admin, preview, or debug.
4. Search chunks for route templates, service names, flags, and identifiers.
5. Compare chunk lists across builds.

### Strong signals

- a new lazy chunk for an unreleased capability;
- a new route template in a chunk;
- a new service or method name;
- a new feature flag registry entry.

---

## Archetype 3: Runtime config and hydration state

Server-rendered apps often embed model registries, flags, and build metadata
before the client boots.

### Structural patterns

```text
<script id="__NEXT_DATA__" type="application/json">...</script>
window.__INITIAL_STATE__ = {...}
window.__CONFIG__ = {...}
self.__next_f.push(...)
AF_initDataCallback({...})
WIZ_global_data = {...}
```

### Discovery heuristics

1. Inspect raw HTML, not the rendered DOM.
2. Extract inline JSON and unescape it.
3. Look for model lists, tiers, flags, experiment IDs, and build IDs.
4. Compare the object across builds.
5. Corroborate a new identifier in a bundle or SDK before promoting it.

### Strong signals

- a new model or capability key;
- a new experiment or gate name;
- a new environment or tier;
- a new build ID paired with semantic changes.

---

## Archetype 4: API gateway, RPC, REST, and GraphQL surfaces

The transport layer names capabilities before the UI exposes them.

### Structural patterns

```text
/api/{version}/{resource}
/rest/{version}/{resource}
/{service}/{method}
/$rpc/{package}.{Service}/{Method}
/graphql
/{service}/Get{Resource}
/{service}/List{Resources}
/openapi.json
/swagger.json
```

### Discovery heuristics

1. Extract service and method names from bundles and SDKs.
2. Classify auth requirements before testing.
3. Test only public anonymous, read-only methods.
4. Use a minimal body and normal browser headers.
5. Stop at the first `401`, `403`, or `405`.
6. Record blocked surfaces as discovery, not leaks.

### Strong signals

- a new method name with a clear capability;
- a public anonymous read-only catalog;
- a new schema field or enum value;
- a new route that returns deploy-ahead data.

---

## Archetype 5: SDK, package, and type definitions

Developer packages are versioned, specific, and often ship before the public
announcement.

### Structural patterns

```text
/{package}/-/ {package}-{version}.tgz
/{package}/dist/index.d.ts
/{package}/dist/{client}.js
/{package}/examples/{feature}.ts
/{package}/CHANGELOG.md
```

### Discovery heuristics

1. Inspect registry metadata and tarballs.
2. Read TypeScript declarations and enums.
3. Search examples and tests for new capability names.
4. Compare versions and diff the public API surface.
5. Corroborate bundle strings against SDK types.

### Strong signals

- a new enum member;
- a new client method;
- a new request/response field;
- a new example for an unreleased feature.

---

## Archetype 6: Status and incident feeds

Operational feeds explain rollouts and outages, but they are not model leaks.

### Structural patterns

```text
/status
/incidents
/incidents/history
/api/status
/{service}/ListIncidents
```

### Discovery heuristics

1. Find the status feed or public incident RPC.
2. Extract incident IDs, products, start times, and resolution times.
3. Track new categories and repeated failures.
4. Use this as context, not as an early model signal.

### Strong signals

- a new product category;
- a new incident pattern;
- a rollout-related outage.

---

## Archetype 7: Public storage and tenant surfaces

Only inspect storage linked from a public artifact, and only at the metadata
level.

### Structural patterns

```text
https://{bucket}.{storage}.{domain}/?list-type=2
https://{bucket}.{storage}.{domain}/?restype=container&comp=list
https://{cdn}/{tenant}/{config}.json
```

### Discovery heuristics

1. Confirm the storage URL is referenced by a public artifact.
2. Check for anonymous listing, not for file contents.
3. Record the smallest evidence of exposure.
4. Do not download personal data.
5. Do not enumerate tenants.
6. Do not test write or delete operations.

### Strong signals

- anonymous listing enabled;
- public config files with non-secret structure;
- cross-tenant paths.

### Boundary

This archetype is high-risk. Stop early and report the boundary.

---

## Archetype 8: Historical snapshots and archive replay

Archives reveal how a public surface changed over time.

### Structural patterns

```text
https://web.archive.org/cdx/search/cdx?url={domain}&matchType=domain&output=json
https://arquivo.pt/wayback/cdx?url={domain}/*
```

### Discovery heuristics

1. Query for JSON and JavaScript artifacts, not just HTML.
2. Compare old and new artifact sets.
3. Identify when a route, model, or flag first appeared.
4. Use archives to date a deploy-ahead signal.

### Strong signals

- a model or route present in an old build but absent from the current docs;
- a staged endpoint that later disappeared;
- a build date that predates the announcement.

---

## Cross-archetype rules

1. **Context first.** A string is not a finding until it has a role.
2. **Corroborate.** Prefer two artifacts over one.
3. **Normalize.** Diff sets, not lines.
4. **Verify.** Public, anonymous, read-only.
5. **Do not use credentials.** Ever.
6. **Do not touch internal hosts.** Record the name only.
7. **Downgrade the claim.** A lead is not a leak.
