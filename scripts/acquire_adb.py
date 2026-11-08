#!/usr/bin/env python3
"""Pull all APK splits for the official Play-installed apps from an authorised device."""
import argparse, hashlib, json, re, subprocess
from datetime import datetime, timezone
from pathlib import Path

def run(*args):
    p=subprocess.run(["adb",*args],capture_output=True,text=True,check=False)
    if p.returncode: raise RuntimeError(p.stderr.strip() or "ADB command failed")
    return p.stdout.strip()

def main():
    p=argparse.ArgumentParser(); p.add_argument("--app",choices=["all","chatgpt","claude","gemini"],default="all")
    p.add_argument("--out",default="input/apks"); p.add_argument("--config",default="config/apps.json"); a=p.parse_args()
    try:
        if run("get-state")!="device":
            print("No authorised ADB device. Connect phone and approve USB debugging."); return 2
    except (FileNotFoundError,RuntimeError) as exc:
        print(f"ADB unavailable: {exc}"); return 2
    config=json.loads(Path(a.config).read_text(encoding="utf-8"))["apps"]
    targets=config if a.app=="all" else {a.app:config[a.app]}
    for app,meta in targets.items():
        package=meta["package_name"]
        paths=[x.removeprefix("package:") for x in run("shell","pm","path",package).splitlines() if x.startswith("package:")]
        if not paths: print(f"[SKIP] {app}: {package} not installed"); continue
        dump=run("shell","dumpsys","package",package)
        vm=re.search(r"versionName=([^\s]+)",dump); vc=re.search(r"versionCode=(\d+)",dump)
        version=vm.group(1) if vm else "unknown"; safe=re.sub(r"[^A-Za-z0-9._+-]","_",version)
        dest=Path(a.out)/app/safe; dest.mkdir(parents=True,exist_ok=True); splits=[]
        for i,remote in enumerate(paths):
            name=Path(remote).name or f"split-{i}.apk"; local=dest/name
            run("pull",remote,str(local)); h=hashlib.sha256(local.read_bytes()).hexdigest()
            splits.append({"remote_path":remote,"file":name,"sha256":h,"size_bytes":local.stat().st_size})
        record={"app":app,"display_name":meta["display_name"],"package_name":package,
          "version_name":version,"version_code":int(vc.group(1)) if vc else None,
          "play_store_url":meta["play_store_url"],"acquired_at":datetime.now(timezone.utc).isoformat(),
          "source":"ADB pull of installed package paths; install/update via Google Play","splits":splits}
        (dest/"metadata.json").write_text(json.dumps(record,indent=2),encoding="utf-8")
        print(f"[OK] {app} {version}: {len(splits)} split APK(s)")
    return 0
if __name__=="__main__": raise SystemExit(main())
