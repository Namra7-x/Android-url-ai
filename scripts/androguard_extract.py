#!/usr/bin/env python3
"""Use Androguard directly on every DEX entry, avoiding full APK/resource parsing."""
import argparse
import zipfile
from pathlib import Path

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("apk_root",nargs="?",default="input/apks")
    parser.add_argument("--out",default="work/androguard")
    args=parser.parse_args()
    try:
        from androguard.core.dex import DEX
    except ImportError:
        print("Androguard is not installed. Run: pip install -e .")
        return 2

    count=0
    for apk in sorted(Path(args.apk_root).rglob("*.apk")):
        try:
            with zipfile.ZipFile(apk) as archive:
                dex_names=sorted(name for name in archive.namelist()
                                 if name.lower().endswith(".dex"))
                for index,name in enumerate(dex_names):
                    data=archive.read(name)
                    dest=Path(args.out)/apk.parent.parent.name/apk.parent.name/apk.stem
                    dest.mkdir(parents=True,exist_ok=True)
                    (dest/f"{name.replace('/', '_')}").write_bytes(data)
                    try:
                        parsed=DEX(data)
                        strings=sorted({str(value) for value in parsed.get_strings()})
                        (dest/f"{name.replace('/', '_')}-strings.txt").write_text(
                            "\n".join(strings),encoding="utf-8")
                    except Exception as exc:
                        (dest/f"{name.replace('/', '_')}-strings-error.txt").write_text(
                            str(exc),encoding="utf-8")
                    count+=1
            print(f"[ANDROGUARD] {apk}: {len(dex_names)} DEX file(s)",flush=True)
        except (OSError,zipfile.BadZipFile) as exc:
            print(f"[WARN] {apk}: {exc}",flush=True)
    print(f"Extracted {count} DEX file(s) with Androguard.",flush=True)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
