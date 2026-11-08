# Android URL Atlas

Automated GitHub-hosted research pipeline for extracting and historically tracking URL evidence from the official Android ChatGPT, Claude and Gemini apps.

**No local setup, phone, ADB connection or manually uploaded APK is required.** GitHub Actions downloads current Android packages, validates package identity and publisher signing certificates, installs analysis tools on the hosted runner, scans the APKs, and commits reviewed URL reports/history.

## Apps scanned

| App | Android package | Official listing |
|---|---|---|
| ChatGPT | `com.openai.chatgpt` | [Google Play](https://play.google.com/store/apps/details?id=com.openai.chatgpt) |
| Claude | `com.anthropic.claude` | [Google Play](https://play.google.com/store/apps/details?id=com.anthropic.claude) |
| Gemini | `com.google.android.apps.bard` | [Google Play](https://play.google.com/store/apps/details?id=com.google.android.apps.bard) |

## CI/CD operation

The workflow `.github/workflows/ci.yml`:

1. Runs on GitHub-hosted Ubuntu.
2. Installs Java, Python, Android build-tools, JADX, Apktool, Ghidra, Rizin and Androguard.
3. Downloads current Android app packages with EFF's `apkeep` (APKPure source by default).
4. Checks the Android package ID and validates the APK signature against the publisher-certificate allowlist in `config/signers.json`.
5. Runs JADX, Apktool, Androguard, native ELF/string inspection and Ghidra headless analysis.
6. Extracts, redacts, classifies and deduplicates URL candidates.
7. Compares against the previous snapshot, appends new evidence to permanent history, and commits reports to this repository.
8. Uploads reports and acquisition evidence as a 30-day workflow artifact.

It runs on pushes to relevant source/config paths, every six hours, and manually through **Actions → Android URL Atlas CI/CD → Run workflow**. Choose one app or all three.

### APK source and authenticity

The default is APKPure via apkeep. This is a third-party mirror, not Google Play. APKPure itself documents that its source is for research use and can carry risk; therefore, this project does not trust the download host alone. It checks the APK's package ID and cryptographic publisher signing certificate before analysis. If the signature is not in the allowlist, the scan stops. See [EFF apkeep APKPure warning](https://github.com/EFForg/apkeep/blob/1.1.0/USAGE-apkpure.md).

For direct Google Play downloads, set repository Actions secrets `GOOGLE_PLAY_EMAIL` and `GOOGLE_PLAY_AAS_TOKEN`, then set repository variable `APK_DOWNLOAD_SOURCE=google-play`. Google Play AAS token acquisition is an optional user-managed credential; it is not needed for the default mirror-based workflow. Do not put tokens in source files.

The signing allowlist is a trust boundary. If a publisher rotates its signing key, the workflow deliberately fails until the new fingerprint is independently verified and reviewed. References for the current fingerprints are recorded in [config/signers.json](config/signers.json).

## Run manually

Open the repository's **Actions** tab, select **Android URL Atlas CI/CD**, click **Run workflow**, and select `all`, `chatgpt`, `claude` or `gemini`. No phone or self-hosted runner is involved.

## Reports

Each app/version folder under `reports/` contains:

- `all-urls.txt` — deduplicated URL candidates
- `all-urls.jsonl` and `all-urls.csv` — URL evidence with source path and extraction method
- `domains.txt` — unique hostnames
- `api-endpoints.txt` — likely API endpoints
- `websocket-endpoints.txt` — WebSocket URLs
- `deep-links.txt` — custom URI schemes
- `new-urls.txt` / `removed-urls.txt` — comparison with the previous scan
- `report.md` — summary and coverage caveats

`data/history/<app>/url-history.jsonl` is append-only. An endpoint missing from a new version is marked "not observed", never deleted from historical records.

## Tool roles

- JADX: DEX to readable Java-like source
- Apktool: manifest, resources, assets and Smali
- Androguard: independent DEX/string-pool pass
- Ghidra: native ELF decompilation in headless mode
- Rizin/rabin2 and strings: native binary strings, imports and metadata
- Python: URL candidate extraction, provenance, normalisation, redaction and history

## Coverage limitations

Static APK analysis cannot prove that every URL an app may ever use has been found. URLs may be assembled dynamically, returned by remote configuration, enabled only for particular users/regions/experiments, or introduced server-side. The project preserves evidence and maximises coverage; it does not claim omniscient discovery. Runtime Frida collection is optional and is not required for CI.

## iOS

This repository intentionally targets Android APKs because the three Android applications are publicly distributed in APK form. App Store IPAs are not a drop-in replacement: production iOS apps are encrypted and require a separately authorised, decrypted app artifact/device workflow. Adding iOS would not make the Android pipeline more reliable.

## Responsible use

Only inspect public app packages and systems you are authorised to analyse. Do not bypass access controls, collect other users' content, or use discovered endpoints to attack services. APKs and decompiled trees are temporary CI inputs and are not committed to Git.
