# Tool installation and analysis

The project uses several independent tools. Missing optional tools are reported as skipped; raw APK scanning remains available.

## Ubuntu / Debian

    sudo apt update
    sudo apt install -y adb apksigner default-jre python3 python3-venv python3-pip unzip p7zip-full file binutils
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -e '.[dev]'

Install official upstream releases:
- JADX: https://github.com/skylot/jadx
- Apktool: https://apktool.org/
- Ghidra: https://github.com/NationalSecurityAgency/ghidra
- Androguard: https://github.com/androguard/androguard
- Rizin: https://rizin.re/
- Frida: https://frida.re/docs/installation/

Check each project's release notes for its current Java/Python requirements. Do not install reverse-engineering binaries from untrusted mirrors.

## Run every analysis pass

    python scripts/acquire_adb.py --app all
    python scripts/androguard_extract.py input/apks
    python scripts/native_analysis.py --apk-root input/apks --ghidra /opt/ghidra
    python -m url_atlas.cli scan --app all

JADX and Apktool are invoked by the main scan when installed. The Androguard pass independently extracts DEX files and string pools. The native pass extracts every .so from every split, runs Rizin/rabin2 and strings when available, and imports libraries into Ghidra headless when a Ghidra path is supplied.

For Ghidra, the headless executable is normally GHIDRA_HOME/support/analyzeHeadless. Ghidra performs auto-analysis on imported ELF libraries. Review projects and decompiler output in the Ghidra GUI for deeper function-level analysis. Official headless guide: https://ghidra.re/ghidra_docs/analyzeHeadlessREADME.html

## Signature and provenance

    apksigner verify --print-certs base.apk
    sha256sum base.apk
    aapt dump badging base.apk

The ADB collector stores SHA-256 for every APK split. Preserve the complete split set and metadata as one app-version acquisition. Compare signing certificate fingerprints across releases; unexpected changes should be reviewed rather than silently accepted.

## Important coverage distinction

JADX/Apktool source trees and raw APK bytes are scanned by URL Atlas. Androguard DEX/string-pool output and native ELF/Rizin string output are ingested by the scan as static URL candidates. Ghidra project databases are retained for interactive native analysis and are not recursively scanned as evidence. Ghidra decompilation and runtime instrumentation are additional independent passes, not guarantees of complete endpoint discovery.
