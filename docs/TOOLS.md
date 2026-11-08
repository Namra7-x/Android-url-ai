# CI-installed tools

The GitHub workflow installs all required tools on a hosted Ubuntu runner. No local installation is necessary.

| Tool | CI installation | Role |
|---|---|---|
| apkeep 1.1.0 | Official EFF release binary | Acquire current APKs |
| Android SDK build-tools | Google SDK manager | `apksigner`, `aapt` |
| JADX | Latest official GitHub release | DEX decompilation |
| Apktool | Latest official GitHub release | Manifest/resources/Smali |
| Androguard | Python dependency | Independent DEX parsing |
| Ghidra | Latest official NSA GitHub release | Native ELF analysis |
| Rizin | Latest official release | Native strings and imports |

The installation script is `scripts/install_ci_tools.sh`. Ghidra runs headlessly through `analyzeHeadless`; it does not require a graphical desktop.

## Local reproduction (optional)

For maintainers who want to reproduce the CI run locally:

    python -m pip install -e '.[dev]'
    bash scripts/install_ci_tools.sh
    python scripts/fetch_latest_apks.py
    python -m url_atlas.cli scan --app all

The APK acquisition step uses the APKPure research-only source by default. Do not use downloaded packages as installable software unless you have independently reviewed their provenance.
