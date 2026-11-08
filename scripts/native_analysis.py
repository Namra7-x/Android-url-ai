#!/usr/bin/env python3
"""Extract ELF libraries from acquired APK splits and run available native analyzers."""
import argparse, shutil, subprocess, zipfile
from pathlib import Path

def main():
    p=argparse.ArgumentParser(); p.add_argument("--apk-root",default="input/apks"); p.add_argument("--out",default="work/native")
    p.add_argument("--ghidra",default=""); a=p.parse_args()
    root,out=Path(a.apk_root),Path(a.out); out.mkdir(parents=True,exist_ok=True)
    libs=[]
    for apk in root.rglob("*.apk"):
        try:
            with zipfile.ZipFile(apk) as z:
                for name in z.namelist():
                    if name.startswith("lib/") and name.endswith(".so"):
                        dest=out/"extracted"/apk.parent.parent.name/apk.parent.name/name
                        dest.parent.mkdir(parents=True,exist_ok=True)
                        dest.write_bytes(z.read(name)); libs.append(dest)
        except (OSError,zipfile.BadZipFile) as e: print(f"[WARN] {apk}: {e}")
    for lib in libs:
        tag=str(lib.relative_to(out)).replace("/","_")
        if shutil.which("rabin2"):
            for suffix,cmd in (("strings",["rabin2","-zz",str(lib)]),("info",["rabin2","-I",str(lib)]),("imports",["rabin2","-i",str(lib)])):
                with (out/f"{tag}.{suffix}.txt").open("w") as f:
                    subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,check=False)
        if shutil.which("strings"):
            with (out/f"{tag}.ascii.txt").open("w") as f:
                subprocess.run(["strings","-a","-n","5",str(lib)],stdout=f,check=False)
        if a.ghidra:
            headless=Path(a.ghidra)/"support"/"analyzeHeadless"
            if headless.exists():
                project=out/"ghidra-projects"; project.mkdir(exist_ok=True)
                subprocess.run([str(headless),str(project),"AndroidUrlAtlas","-import",str(lib),
                                "-analysisTimeoutPerFile","300"],check=False)
        print(f"[NATIVE] {lib}")
    print(f"Extracted {len(libs)} native libraries. Ghidra runs only when --ghidra points to its installation.")
    return 0
if __name__=="__main__": raise SystemExit(main())
