#!/usr/bin/env python3
"""Fetch current ChatGPT, Claude and Gemini APKs in CI and validate publisher signatures."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPS_FILE = ROOT / "config" / "apps.json"
SIGNERS_FILE = ROOT / "config" / "signers.json"
DOWNLOAD_ROOT = ROOT / "input" / "downloads"
APK_ROOT = ROOT / "input" / "apks"
MANIFEST_OUT = ROOT / "reports" / "acquisition-manifest.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def get_apks(root: Path) -> list[Path]:
    """Find APKs and unpack APKM/XAPK/APKS containers using safe output names."""
    found: list[Path] = []
    unpack_root = root / "_unpacked"
    unpack_root.mkdir(parents=True, exist_ok=True)
    for path in sorted(root.rglob("*")):
        if not path.is_file() or unpack_root in path.parents:
            continue
        if path.suffix.lower() == ".apk":
            found.append(path)
        elif path.suffix.lower() in {".xapk", ".apkm", ".apks", ".zip"}:
            try:
                with zipfile.ZipFile(path) as archive:
                    for info in archive.infolist():
                        if info.is_dir() or not info.filename.lower().endswith(".apk"):
                            continue
                        basename = Path(info.filename).name
                        if basename:
                            target = unpack_root / f"{path.stem}_{basename}"
                            target.write_bytes(archive.read(info))
                            found.append(target)
            except (OSError, zipfile.BadZipFile) as exc:
                print(f"[WARN] Could not unpack {path.name}: {exc}", file=sys.stderr)
    unique: dict[str, Path] = {}
    for path in found:
        try:
            unique.setdefault(sha256(path), path)
        except OSError:
            continue
    return list(unique.values())


def run_download(package: str, output: Path, source: str, email: str | None, token: str | None) -> None:
    command = ["apkeep", "-a", package, "-d", source, "-r", "1"]
    if source == "google-play":
        if not email or not token:
            raise RuntimeError("Google Play selected but GOOGLE_PLAY_EMAIL / GOOGLE_PLAY_AAS_TOKEN are missing.")
        command += ["-e", email, "-t", token, "--accept-tos", "-o", "split_apk=true"]
    else:
        # apkeep documents this acknowledgement for its APKPure research-only source.
        command += ["-o", "acknowledge_dangers=true"]
    command.append(str(output))
    subprocess.run(command, check=True, timeout=900)


def read_package(apk_path: Path):
    from androguard.core.apk import APK
    apk = APK(str(apk_path))
    package = apk.get_package()
    version_name = apk.get_androidversion_name() or "unknown"
    version_code = apk.get_androidversion_code()
    try:
        version_code = int(version_code)
    except (TypeError, ValueError):
        version_code = 0
    return package, str(version_name), version_code


def read_signers(apk_path: Path) -> list[str]:
    if not shutil.which("apksigner"):
        raise RuntimeError("apksigner missing; CI did not install Android build-tools.")
    result = subprocess.run(
        ["apksigner", "verify", "--print-certs", str(apk_path)],
        capture_output=True, text=True, check=False,
    )
    if result.returncode:
        raise RuntimeError(f"APK signature verification failed: {result.stderr.strip()}")
    matches = re.findall(r"certificate SHA-256 digest:\s*([0-9a-fA-F:]+)", result.stdout, re.I)
    return sorted({item.replace(":", "").lower() for item in matches})


def download_one(app_key: str, app: dict, signer: dict, source: str,
                 email: str | None, token: str | None) -> dict:
    output = DOWNLOAD_ROOT / app_key
    output.mkdir(parents=True, exist_ok=True)
    run_download(app["package_name"], output, source, email, token)

    accepted = set(signer["accepted_certificate_sha256"])
    candidates = get_apks(output)
    valid = []
    rejected = []

    for apk_path in candidates:
        try:
            package, version_name, version_code = read_package(apk_path)
            if package != app["package_name"]:
                rejected.append(f"{apk_path.name}: wrong package {package!r}")
                continue
            fingerprints = read_signers(apk_path)
            matches = sorted(set(fingerprints) & accepted)
            if not matches:
                rejected.append(f"{apk_path.name}: unapproved signer {fingerprints!r}")
                continue
            valid.append({
                "path": apk_path, "version_name": version_name,
                "version_code": version_code, "sha256": sha256(apk_path),
                "fingerprints": fingerprints, "approved_signer": matches[0],
            })
        except Exception as exc:
            rejected.append(f"{apk_path.name}: {exc}")

    if not valid:
        details = "\n".join(f"  - {line}" for line in rejected[:20])
        raise RuntimeError(
            f"No signed APKs accepted for {app_key} ({app['package_name']}). "
            "The downloader returned no app package, or the signing key changed. "
            "The scan stops instead of analysing an unverified APK.\n" + details
        )

    newest_code = max(item["version_code"] for item in valid)
    newest = [item for item in valid if item["version_code"] == newest_code]
    version_name = newest[0]["version_name"]
    safe_name = re.sub(r"[^A-Za-z0-9._+-]", "_", version_name)[:80]
    version_dir = APK_ROOT / app_key / f"{safe_name}_{newest_code}"
    version_dir.mkdir(parents=True, exist_ok=True)

    split_rows = []
    for index, item in enumerate(newest):
        destination = version_dir / item["path"].name
        if destination.exists():
            destination = version_dir / f"{index}_{destination.name}"
        shutil.copy2(item["path"], destination)
        split_rows.append({
            "file": destination.name,
            "sha256": item["sha256"],
            "size_bytes": destination.stat().st_size,
            "signing_certificates_sha256": item["fingerprints"],
            "approved_signer_sha256": item["approved_signer"],
        })

    metadata = {
        "app": app_key,
        "display_name": app["display_name"],
        "package_name": app["package_name"],
        "version_name": version_name,
        "version_code": newest_code,
        "download_source": source,
        "source_note": (
            "APKPure mirror; package ID and APK signing certificate were checked against the "
            "pre-reviewed publisher signer allowlist."
            if source == "apk-pure" else
            "Downloaded directly from Google Play using an AAS token."
        ),
        "play_store_url": app["play_store_url"],
        "acquired_at": datetime.now(UTC).isoformat(),
        "splits": split_rows,
    }
    (version_dir / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(f"[ACCEPTED] {app_key}: {version_name} ({newest_code}), {len(split_rows)} APK(s)")
    return metadata


def main() -> int:
    apps = json.loads(APPS_FILE.read_text(encoding="utf-8"))["apps"]
    signers = json.loads(SIGNERS_FILE.read_text(encoding="utf-8"))
    email = os.getenv("GOOGLE_PLAY_EMAIL")
    token = os.getenv("GOOGLE_PLAY_AAS_TOKEN")
    source = os.getenv("APK_DOWNLOAD_SOURCE") or ("google-play" if email and token else "apk-pure")
    if source not in {"apk-pure", "google-play"}:
        raise RuntimeError("APK_DOWNLOAD_SOURCE must be apk-pure or google-play.")

    selected = os.getenv("APK_APP", "all")
    targets = apps if selected == "all" else {selected: apps[selected]}
    results = []
    for app_key, app in targets.items():
        print(f"\n=== {app['display_name']} ({app['package_name']}) ===", flush=True)
        results.append(download_one(app_key, app, signers[app_key], source, email, token))

    MANIFEST_OUT.parent.mkdir(parents=True, exist_ok=True)
    previous = {}
    if MANIFEST_OUT.exists():
        try:
            previous = json.loads(MANIFEST_OUT.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            previous = {}
    history = previous.get("scans", [])
    history.append({"timestamp": datetime.now(UTC).isoformat(), "source": source, "apps": results})
    MANIFEST_OUT.write_text(json.dumps({"latest": history[-1], "scans": history[-30:]},
                                       indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
