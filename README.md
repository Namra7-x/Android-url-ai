# Android URL Atlas

Private research toolkit for extracting, comparing, and preserving URL and endpoint evidence from the official Android applications for ChatGPT, Claude, and Gemini.

> **Scope and limits:** "All URLs" is the target, but no static or dynamic technique can prove that it has discovered every URL an app could ever use. URLs can be assembled at runtime, returned by remote configuration, enabled only for particular accounts/regions, or delivered by future server responses. This project therefore combines multiple independent methods, records provenance, and distinguishes static discoveries from runtime observations.

## Supported official Android packages

| App | Android package | Official Play listing |
|---|---|---|
| ChatGPT | `com.openai.chatgpt` | [Google Play](https://play.google.com/store/apps/details?id=com.openai.chatgpt) |
| Claude | `com.anthropic.claude` | [Google Play](https://play.google.com/store/apps/details?id=com.anthropic.claude) |
| Gemini | `com.google.android.apps.bard` | [Google Play](https://play.google.com/store/apps/details?id=com.google.android.apps.bard) |

Install or update the apps through Google Play on your own Android device. This repository deliberately does not use third-party APK mirrors or scrape unofficial APK download sites. The acquisition script pulls every APK path returned by Android Package Manager, including base and split APKs, from the connected device.

Package name is an app identifier, not proof of publisher identity by itself. The acquisition manifest records APK hashes and signing-certificate details where `apksigner` is installed. Keep the device's Play-installed version and signing information as the provenance baseline.

## Analysis stack

- **JADX**: DEX decompilation into readable Java-like source.
- **Apktool**: AndroidManifest, resources, assets and Smali extraction.
- **Androguard**: independent programmatic APK/DEX inspection.
- **Ghidra**: native ELF shared-library analysis and decompilation.
- **Rizin / rabin2**: independent native strings and binary inspection.
- **Frida**: optional, authorised runtime URL observation on a device you control.
- **Python URL Atlas**: recursive extraction, normalisation, provenance, deduplication, reports and historical comparison.

The pipeline inspects every APK split, multiple DEX files, decoded resource trees, raw assets and native `.so` files. Ghidra and Rizin are additional native-analysis passes; they complement rather than replace byte-level scanning.

## Quick start

Requirements: Linux, Python 3.11+, Android Platform Tools (`adb`), and a USB-connected Android device with USB debugging authorised. Use a dedicated test device/profile when possible.

1. Install all three official apps from Google Play and open them once so installation is complete.
2. Connect the device and check:

   ```bash
   adb devices
   ```

3. Install Python dependencies and the analysis tools. See [docs/TOOLS.md](docs/TOOLS.md).
4. Acquire all installed APK splits:

   ```bash
   python scripts/acquire_adb.py --out input/apks
   ```

5. Run the static analysis:

   ```bash
   python -m url_atlas.cli scan --apk-root input/apks --config config/apps.json
   ```

   If the package is not installed, it is reported as skipped; other installed targets continue.

6. Review `reports/` and `data/history/`. Commit those outputs to this private repository to retain history across machines and scans.

### Run a specific app

```bash
python scripts/acquire_adb.py --app gemini --out input/apks
python -m url_atlas.cli scan --apk-root input/apks --app gemini --config config/apps.json
```

### Frida runtime observation

Frida is optional. First install Frida tools on the analysis host and a compatible Frida server/ Gadget on a device you own and are authorised to test. Then use the agent under `runtime/frida_url_observer.js` with the instructions in [docs/RUNTIME.md](docs/RUNTIME.md). Runtime output is evidence from the actions actually exercised; it is not an exhaustive record of every server-side route.

The observer records URL-like destinations only. It intentionally does not collect request bodies, cookies, authorisation headers, passwords, prompts, chat contents, or response bodies.

## Output layout

For each app and version, the report contains:

- `all-urls.jsonl`: one evidence record per URL occurrence.
- `all-urls.csv`: spreadsheet-friendly evidence table.
- `all-urls.txt`: deduplicated URL candidates.
- `domains.txt`: unique hostnames.
- `api-endpoints.txt`: likely API paths and URL candidates classified as APIs.
- `websocket-endpoints.txt`: WebSocket destinations.
- `new-urls.txt` / `removed-urls.txt`: comparison against the prior history snapshot.
- `report.md`: counts, methods, versions and caveats.

Historical data is append-preserving in `data/history/<app>/url-history.jsonl`; an URL missing from a new version is not deleted from history. Every occurrence retains source path, evidence type, line number when available, extraction method, app version and confidence.

## GitHub Actions

- `CI` runs unit tests on GitHub-hosted runners.
- `Device scan` is a manual workflow intended for a **self-hosted runner** tagged `android-url-atlas`, with an authorised Android device connected by USB. GitHub-hosted runners cannot see your local USB phone.

Never commit APKs, decompiled source trees, app databases, personal account data, credentials, cookies, access tokens or Frida logs containing sensitive information. The supplied `.gitignore` excludes APK inputs and temporary work directories. Review reports before committing because endpoint paths and query parameters can still reveal internal implementation details.

## Responsible use

Use this project only on official app builds you obtained lawfully, devices and accounts you control, and network activity you are authorised to inspect. Do not bypass access controls, extract other users' data, evade security protections, or use discoveries to attack services. Certificate-pinning bypass is not included. Runtime observation is limited to visible destination metadata from an authorised test session.

## Current project status

This repository contains the analysis framework and tooling. It does not yet contain APKs or scan results. A real scan requires the official apps installed on an Android device and the local/self-hosted analysis environment.
