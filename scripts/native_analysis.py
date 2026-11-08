#!/usr/bin/env python3
"""Extract native ELF libraries, inspect strings/imports and selectively run Ghidra."""
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

NETWORK_HINTS = re.compile(
    rb"(?i)https?://|wss?://|graphql|grpc|cronet|okhttp|curl|websocket|"
    rb"boringssl|openssl|ssl_write|ssl_read|websocket|connect"
)
NETWORK_NAMES = re.compile(r"(?i)cronet|grpc|ssl|crypto|curl|http|network|websocket|okhttp")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apk-root", default="input/apks")
    parser.add_argument("--out", default="work/native")
    parser.add_argument("--ghidra", default="")
    parser.add_argument("--ghidra-limit", type=int, default=12)
    parser.add_argument("--ghidra-timeout", type=int, default=90)
    args = parser.parse_args()

    root = Path(args.apk_root)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    libs: list[Path] = []
    seen_hashes: set[str] = set()

    for apk in sorted(root.rglob("*.apk")):
        try:
            with zipfile.ZipFile(apk) as archive:
                for name in archive.namelist():
                    if not name.startswith("lib/") or not name.endswith(".so"):
                        continue
                    data = archive.read(name)
                    digest = hashlib.sha256(data).hexdigest()
                    if digest in seen_hashes:
                        continue
                    seen_hashes.add(digest)
                    destination = out / "extracted" / apk.parent.parent.name / apk.parent.name / name
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    destination.write_bytes(data)
                    libs.append(destination)
        except (OSError, zipfile.BadZipFile) as exc:
            print(f"[WARN] {apk}: {exc}")

    ghidra_candidates = []
    for lib in libs:
        tag = str(lib.relative_to(out)).replace("/", "_")
        data = lib.read_bytes()

        if shutil.which("rabin2"):
            for suffix, command in (
                ("strings", ["rabin2", "-zz", str(lib)]),
                ("info", ["rabin2", "-I", str(lib)]),
                ("imports", ["rabin2", "-i", str(lib)]),
            ):
                with (out / f"{tag}.{suffix}.txt").open("w", encoding="utf-8") as stream:
                    subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT, check=False)

        if shutil.which("strings"):
            with (out / f"{tag}.ascii.txt").open("w", encoding="utf-8") as stream:
                subprocess.run(["strings", "-a", "-n", "5", str(lib)],
                               stdout=stream, check=False)

        if NETWORK_HINTS.search(data) or NETWORK_NAMES.search(lib.name):
            ghidra_candidates.append(lib)

    if args.ghidra:
        headless = Path(args.ghidra) / "support" / "analyzeHeadless"
        if not headless.exists():
            print(f"[WARN] Ghidra headless launcher not found: {headless}")
        else:
            project = out / "ghidra-projects"
            project.mkdir(exist_ok=True)
            selected = ghidra_candidates[:max(0, args.ghidra_limit)]
            print(f"[GHIDRA] Analysing {len(selected)} network-relevant native libraries "
                  f"(candidate count: {len(ghidra_candidates)}, cap: {args.ghidra_limit})")
            for lib in selected:
                result = subprocess.run(
                    [str(headless), str(project), "AndroidUrlAtlas",
                     "-import", str(lib),
                     "-analysisTimeoutPerFile", str(args.ghidra_timeout)],
                    check=False,
                )
                if result.returncode:
                    print(f"[WARN] Ghidra returned {result.returncode} for {lib.name}")
    print(f"Extracted and scanned {len(libs)} unique native libraries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
