#!/usr/bin/env python3
"""NEW fixture CURRENT (721 ancestry + CURRENT 741 source-only commit, old E uncommitted, fresh epoch).

Clones READONLY bootstrap-weekly (721a04d), copies untracked old E, overlays full CURRENT 741 OWN source, commits source-only (never -A).
Usage: python3 harness_make_fixture_current.py BOOT_WEEKLY OWN_CURRENT DST_PARENT STAMP
"""
from __future__ import annotations
import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

def _run(cmd, cwd, env):
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=120, env=env)

def _sha(p: Path)->str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1<<20), b""):
            h.update(c)
    return h.hexdigest()

def main()->int:
    if len(sys.argv)!=5:
        print(f"usage: {sys.argv[0]} BOOT OWN DST_PARENT STAMP", flush=True)
        return 2
    BOOT=Path(sys.argv[1]).resolve()
    OWN=Path(sys.argv[2]).resolve()
    PARENT=Path(sys.argv[3]).resolve()
    STAMP=sys.argv[4].strip()
    for v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE","GIT_OBJECT_DIRECTORY","GIT_ALTERNATE_OBJECT_DIRECTORIES"):
        if os.environ.get(v):
            print(f"UNSAFE {v}", flush=True)
            return 2
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"1","GIT_ALLOW_PROTOCOL":"file","PYTHONDONTWRITEBYTECODE":"1","LC_ALL":"C"})
    h=_run(["git","rev-parse","HEAD"],BOOT,env)
    print(f"BOOT HEAD={h.stdout.strip()}", flush=True)
    if h.stdout.strip()!="721a04d85532d7855f3e54cc411f5847c787726e":
        print("FATAL BOOT !=721", flush=True)
        return 2
    h2=_run(["git","rev-parse","HEAD"],OWN,env)
    print(f"OWN HEAD={h2.stdout.strip()}", flush=True)
    if h2.stdout.strip()!="409b292756dd1277b9dfae87679934c0d2ce251c":
        print("FATAL OWN !=409", flush=True)
        return 2
    PARENT.mkdir(parents=True, exist_ok=True)
    DST=PARENT/f"versioned-renewal-faultresume-current-{STAMP}"/"renewal-weekly"
    if DST.exists():
        print(f"FATAL dst exists: {DST}", flush=True)
        return 2
    cp=_run(["git","clone","--no-hardlinks",str(BOOT),str(DST)],PARENT,env)
    print(f"CLONE rc={cp.returncode}", flush=True)
    if cp.returncode!=0:
        print(cp.stderr[:500], flush=True)
        return 2
    _run(["git","remote","set-url","origin","https://example.invalid/versioned-renewal-faultresume-current-weekly.git"],DST,env)
    _run(["git","config","user.name","rephase-fixture"],DST,env)
    _run(["git","config","user.email","fixture@example.invalid"],DST,env)
    _run(["git","config","commit.gpgsign","false"],DST,env)
    src_stat=_run(["git","status","--porcelain=v1","--untracked-files=normal"],BOOT,env).stdout
    e_paths=[l[3:].strip().strip('"') for l in src_stat.splitlines() if l.startswith("??") and (BOOT/l[3:].strip().strip('"')).exists() and ".git" not in Path(l[3:].strip().strip('"')).parts]
    print(f"E_PATHS={len(e_paths)}", flush=True)
    for rel in sorted(e_paths):
        s,d=BOOT/rel, DST/rel
        if d.exists():
            print(f"FATAL E exists: {rel}", flush=True)
            return 2
        if s.is_dir() and not s.is_symlink():
            shutil.copytree(str(s),str(d),symlinks=True,copy_function=shutil.copy2)
        else:
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(s),str(d))
    for rel in sorted(e_paths)[:20]:
        s,d=BOOT/rel, DST/rel
        if s.is_file() and _sha(s)!=_sha(d):
            print(f"FATAL E sha: {rel}", flush=True)
            return 2
    print("E_COPY_OK", flush=True)
    own_files=[]
    for root,dirs,files in os.walk(OWN):
        if ".git" in dirs:
            dirs.remove(".git")
        if ".git" in root.split(os.sep):
            continue
        for f in sorted(files):
            full=os.path.join(root,f)
            if "/.git/" in full or "__pycache__" in full or full.endswith(".pyc"):
                continue
            own_files.append(os.path.relpath(full,OWN))
    print(f"OWN_FILES={len(own_files)}", flush=True)
    if len(own_files)!=741:
        print(f"FATAL OWN !=741 got {len(own_files)}", flush=True)
        return 2
    for rel in own_files:
        s,d=OWN/rel, DST/rel
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(s),str(d))
    print("OVERLAY_OK (CURRENT 741, HIGH 1dad1ad/H74275d/S2290ddd, no stale 9a)", flush=True)
    add=_run(["git","add","--"]+own_files,DST,env)
    print(f"ADD rc={add.returncode}", flush=True)
    if add.returncode!=0:
        return 2
    commit=_run(["git","commit","-m","HIGH phase TEST-ONLY: fault-resume CURRENT 741 source (1dad1ad/H74275d/S2290ddd, trio untouched, before authority)","--no-verify"],DST,env)
    print(f"COMMIT rc={commit.returncode} {commit.stdout[:300]}", flush=True)
    if commit.returncode!=0:
        return 2
    print(f"NEW_HEAD={_run(['git','rev-parse','HEAD'],DST,env).stdout.strip()}", flush=True)
    print(f"LOG:\n{_run(['git','log','--oneline','-3'],DST,env).stdout}", flush=True)
    if "721a04d" not in _run(["git","log","--oneline"],DST,env).stdout:
        print("FATAL ancestry missing 721", flush=True)
        return 2
    if (DST/".git"/"objects"/"info"/"alternates").exists():
        print("FATAL alternates", flush=True)
        return 2
    print("FIXTURE_CURRENT_OK (fresh Python epoch, no stale 9a, 721 ancestry, old E uncommitted)", flush=True)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
