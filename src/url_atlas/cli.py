from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from .extract import scan_apk, scan_file, scan_tree
from .history import append_history
from .report import write_reports


def tool(command, log):
    if not shutil.which(command[0]):
        return False
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("w", encoding="utf-8") as stream:
        return subprocess.run(
            command, stdout=stream, stderr=subprocess.STDOUT, check=False
        ).returncode == 0


def scan(args):
    config = json.loads(Path(args.config).read_text(encoding="utf-8"))["apps"]
    targets = config if args.app == "all" else {args.app: config[args.app]}
    apk_root = Path(args.apk_root)
    work_root = Path(args.work)
    scripts = Path("scripts")

    # Independent passes are supplemental. A failed optional parser must not
    # prevent the direct APK archive scan from running.
    if (scripts / "androguard_extract.py").exists():
        result = subprocess.run(
            [sys.executable, str(scripts / "androguard_extract.py"), str(apk_root),
             "--out", str(work_root / "androguard")],
            check=False,
        )
        if result.returncode:
            print(f"[WARN] Androguard pass exited with {result.returncode}; continuing.")

    native_cmd = [
        sys.executable, str(scripts / "native_analysis.py"),
        "--apk-root", str(apk_root), "--out", str(work_root / "native"),
    ]
    if os.environ.get("GHIDRA_HOME"):
        native_cmd += ["--ghidra", os.environ["GHIDRA_HOME"]]
    if (scripts / "native_analysis.py").exists():
        result = subprocess.run(native_cmd, check=False)
        if result.returncode:
            print(f"[WARN] Native analysis exited with {result.returncode}; continuing.")

    any_scanned = False
    for app, meta in targets.items():
        app_dir = apk_root / app
        if not app_dir.exists():
            print(f"[SKIP] {app}: no APKs were acquired.")
            continue

        for version_dir in sorted(path for path in app_dir.iterdir() if path.is_dir()):
            version = version_dir.name
            work = work_root / app / version
            work.mkdir(parents=True, exist_ok=True)
            apks = sorted(version_dir.glob("*.apk"))
            if not apks:
                continue

            decoded = []
            for apk in apks:
                stem = apk.stem
                jadx_dir = work / "jadx" / stem
                apktool_dir = work / "apktool" / stem
                if tool(["jadx", "-d", str(jadx_dir), str(apk)],
                        work_root / "logs" / f"jadx-{app}-{stem}.log"):
                    decoded.append(jadx_dir)
                if tool(["apktool", "d", "-f", "-o", str(apktool_dir), str(apk)],
                        work_root / "logs" / f"apktool-{app}-{stem}.log"):
                    decoded.append(apktool_dir)

            rows = []
            # Critical path: inspect every split APK and every decompressed ZIP
            # entry (DEX, manifest, resources, assets, native ELF, bundled ZIPs).
            for apk in apks:
                rows.extend(scan_apk(apk, version_dir, app, version))

            # Decompiled trees add decoded strings and resource values.
            for tree in decoded:
                rows.extend(scan_tree(tree, app, version))

            # Androguard extracts every DEX entry and its string pool.
            androguard_dir = work_root / "androguard" / app / version
            if androguard_dir.exists():
                rows.extend(scan_tree(androguard_dir, app, version))

            # Native ELF strings, imports and tool output are a separate source.
            native_dir = work_root / "native"
            extracted = native_dir / "extracted" / app / version
            if extracted.exists():
                rows.extend(scan_tree(extracted, app, version))
            if native_dir.exists():
                for text_file in sorted(native_dir.glob(f"extracted_{app}_*.txt")):
                    rows.extend(scan_file(
                        text_file, native_dir, app, version, "native-tool-output"
                    ))

            # De-duplicate evidence while retaining distinct source paths and
            # extraction methods for auditability.
            unique_rows = {}
            for row in rows:
                key = (
                    row["url"], row["category"], row["source_file"],
                    row["extraction_method"], row["encoding"],
                )
                unique_rows.setdefault(key, row)
            rows = list(unique_rows.values())

            metadata_file = version_dir / "metadata.json"
            build = json.loads(metadata_file.read_text(encoding="utf-8")) \
                if metadata_file.exists() else {}
            for row in rows:
                row["package_name"] = meta["package_name"]
                row["version_name"] = build.get("version_name", version)
                row["version_code"] = build.get("version_code")

            new, removed = append_history(
                Path(args.history) / app / "url-history.jsonl", rows
            )
            write_reports(
                Path(args.reports) / app / version, app, version, rows, new, removed
            )
            url_count = len({
                row["url"] for row in rows if row["category"] != "domain-reference"
            })
            print(
                f"[OK] {app} {version}: {len(rows)} evidence rows, "
                f"{url_count} unique URL candidates (bare domains separate)",
                flush=True,
            )
            any_scanned = True

    return 0 if any_scanned else 2


def main():
    parser = argparse.ArgumentParser(prog="url-atlas")
    subparsers = parser.add_subparsers(dest="command", required=True)
    command = subparsers.add_parser("scan")
    command.add_argument("--apk-root", default="input/apks")
    command.add_argument("--config", default="config/apps.json")
    command.add_argument(
        "--app", choices=["all", "chatgpt", "claude", "gemini"], default="all"
    )
    command.add_argument("--work", default="work")
    command.add_argument("--reports", default="reports")
    command.add_argument("--history", default="data/history")
    command.set_defaults(func=scan)
    args = parser.parse_args()
    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main()
