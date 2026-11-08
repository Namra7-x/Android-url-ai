# Architecture

Official Play installation on an authorised Android device
-> ADB package path inventory
-> base APK and every split APK
-> SHA-256, signer and version metadata
-> JADX + Apktool + raw binary scan
-> Androguard DEX and string pool pass
-> native ELF extraction + strings + Rizin + Ghidra
-> optional Frida URL destination observation
-> URL candidate extraction and secret redaction
-> classification, provenance and deduplication
-> per-version reports and append-only history

## Coverage strategy

1. Acquire all APK paths returned by Android Package Manager, not just base.apk.
2. Decompile every split and scan decoded resources, Smali and source trees.
3. Scan raw APK bytes independently, including compressed binary payloads where visible to byte-pattern scanning.
4. Extract DEX pools independently with Androguard.
5. Extract ELF libraries from every split and inspect strings/imports in Rizin; import into Ghidra for native analysis.
6. Observe common URL constructors at runtime during authorised test sessions.
7. Preserve evidence source, extraction method, encoding, app version and confidence.

## Confidence and limits

Static URL matches are candidates, not proof that an endpoint is live. Runtime-observed destinations are stronger evidence for the exercised session only. Some URLs are dynamically assembled, encrypted, fetched from remote configuration or available only to certain accounts, regions or experiments. "Removed" means not observed in the latest scan, not confirmed deleted by the service.
