from __future__ import annotations
import argparse, json, os, shutil, subprocess, sys
from pathlib import Path
from .extract import scan_file, scan_tree
from .history import append_history
from .report import write_reports

def tool(command, log):
    if not shutil.which(command[0]): return False
    log.parent.mkdir(parents=True,exist_ok=True)
    with log.open("w",encoding="utf-8") as f:
        return subprocess.run(command,stdout=f,stderr=subprocess.STDOUT,check=False).returncode==0

def scan(args):
    config=json.loads(Path(args.config).read_text(encoding="utf-8"))["apps"]
    targets=config if args.app=="all" else {args.app:config[args.app]}
    apk_root=Path(args.apk_root); work_root=Path(args.work)
    # Independent parser and native passes run once per scan. They gracefully skip
    # unavailable tools; the primary APK byte scan always remains enabled.
    scripts=Path("scripts")
    if (scripts/"androguard_extract.py").exists():
        subprocess.run([sys.executable,str(scripts/"androguard_extract.py"),str(apk_root),
                        "--out",str(work_root/"androguard")],check=False)
    native_cmd=[sys.executable,str(scripts/"native_analysis.py"),
                "--apk-root",str(apk_root),"--out",str(work_root/"native")]
    if os.environ.get("GHIDRA_HOME"): native_cmd += ["--ghidra",os.environ["GHIDRA_HOME"]]
    if (scripts/"native_analysis.py").exists(): subprocess.run(native_cmd,check=False)
    any_scanned=False
    for app,meta in targets.items():
        app_dir=apk_root/app
        if not app_dir.exists():
            print(f"[SKIP] {app}: no APKs. Run scripts/acquire_adb.py first."); continue
        for version_dir in sorted(p for p in app_dir.iterdir() if p.is_dir()):
            version=version_dir.name; work=work_root/app/version; work.mkdir(parents=True,exist_ok=True)
            apks=list(version_dir.glob("*.apk"))
            if not apks: continue
            decoded=[]
            for apk in apks:
                stem=apk.stem
                j=work/"jadx"/stem; a=work/"apktool"/stem
                if tool(["jadx","-d",str(j),str(apk)],work_root/"logs"/f"jadx-{app}-{stem}.log"): decoded.append(j)
                if tool(["apktool","d","-f","-o",str(a),str(apk)],work_root/"logs"/f"apktool-{app}-{stem}.log"): decoded.append(a)
            rows=[]
            for apk in apks: rows.extend(scan_file(apk,version_dir,app,version,"apk-binary-scan"))
            for tree in decoded: rows.extend(scan_tree(tree,app,version))
            # Androguard DEX/string pools and native ELF/Rizin strings are independent
            # evidence sources. Ghidra project databases are intentionally not scanned.
            ag=work_root/"androguard"/app/version
            if ag.exists(): rows.extend(scan_tree(ag,app,version))
            native=work_root/"native"
            extracted=native/"extracted"/app/version
            if extracted.exists(): rows.extend(scan_tree(extracted,app,version))
            if native.exists():
                for textfile in native.glob(f"extracted_{app}_*.txt"):
                    rows.extend(scan_file(textfile,native,app,version,"native-tool-output"))
            meta_file=version_dir/"metadata.json"
            build=json.loads(meta_file.read_text()) if meta_file.exists() else {}
            for r in rows:
                r["package_name"]=meta["package_name"]
                r["version_name"]=build.get("version_name",version)
                r["version_code"]=build.get("version_code")
            new,removed=append_history(Path(args.history)/app/"url-history.jsonl",rows)
            write_reports(Path(args.reports)/app/version,app,version,rows,new,removed)
            print(f"[OK] {app} {version}: {len(rows)} evidence rows, {len({r['url'] for r in rows})} unique candidates")
            any_scanned=True
    return 0 if any_scanned else 2

def main():
    p=argparse.ArgumentParser(prog="url-atlas"); s=p.add_subparsers(dest="command",required=True)
    q=s.add_parser("scan"); q.add_argument("--apk-root",default="input/apks"); q.add_argument("--config",default="config/apps.json")
    q.add_argument("--app",choices=["all","chatgpt","claude","gemini"],default="all")
    q.add_argument("--work",default="work"); q.add_argument("--reports",default="reports"); q.add_argument("--history",default="data/history")
    q.set_defaults(func=scan); args=p.parse_args(); raise SystemExit(args.func(args))
if __name__=="__main__": main()
