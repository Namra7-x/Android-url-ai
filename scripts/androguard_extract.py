#!/usr/bin/env python3
"""Use Androguard independently to enumerate DEX files and dump their string literals."""
import argparse
from pathlib import Path

def main():
    p=argparse.ArgumentParser(); p.add_argument("apk_root",nargs="?",default="input/apks"); p.add_argument("--out",default="work/androguard")
    a=p.parse_args()
    try:
        from androguard.core.apk import APK
    except ImportError:
        print("Androguard is not installed. Run: pip install -e ."); return 2
    count=0
    for apk in Path(a.apk_root).rglob("*.apk"):
        try:
            parsed=APK(str(apk))
            dex_files=parsed.get_all_dex()
            dest=Path(a.out)/apk.parent.parent.name/apk.parent.name/apk.stem
            dest.mkdir(parents=True,exist_ok=True)
            for i,dex in enumerate(dex_files):
                (dest/f"classes-{i+1}.dex").write_bytes(dex)
                try:
                    from androguard.core.dex import DEX
                    d=DEX(dex)
                    strings=sorted({str(s) for s in d.get_strings()})
                    (dest/f"classes-{i+1}-strings.txt").write_text("\n".join(strings),encoding="utf-8")
                except Exception as e:
                    (dest/f"classes-{i+1}-strings-error.txt").write_text(str(e),encoding="utf-8")
                count+=1
            print(f"[ANDROGUARD] {apk}: {len(dex_files)} DEX file(s)")
        except Exception as e: print(f"[WARN] {apk}: {e}")
    print(f"Extracted {count} DEX file(s) with Androguard.")
    return 0
if __name__=="__main__": raise SystemExit(main())
