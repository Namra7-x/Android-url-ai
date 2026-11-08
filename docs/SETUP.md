# First run

1. Create a dedicated test environment and install/update ChatGPT, Claude and Gemini from Google Play.
2. Enable USB debugging on your Android device and authorise the computer.
3. Install the tools in TOOLS.md.
4. Confirm ADB sees the device: adb devices
5. Pull all installed APK splits: python scripts/acquire_adb.py --app all
6. Run Androguard: python scripts/androguard_extract.py
7. Run native inspection: python scripts/native_analysis.py --ghidra /path/to/ghidra
8. Run JADX/Apktool extraction: python -m url_atlas.cli scan --app all
9. Review reports under reports/ and historical data under data/history/.
10. Review sensitive values and findings before committing reports.

The first scan is a framework run only after APKs are acquired; no APKs are stored in Git. GitHub-hosted runners cannot access a local USB device. Use the manual device-scan workflow only from a secured self-hosted runner with the android-url-atlas label.
