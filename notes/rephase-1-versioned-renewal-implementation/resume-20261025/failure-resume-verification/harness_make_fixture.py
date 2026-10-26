#!/usr/bin/env python3
"""New isolated weekly fixture: 721 ancestry + 740 source-only commit, old E uncommitted.

Clones READONLY bootstrap-weekly (721a04d) to new DB, copies untracked old E,
overlays full 740 OWN source, commits source-only (never git add -A).
Usage: python3 harness_make_fixture.py BOOT_WEEKLY OWN_SRC DST_PARENT STAMP
"""
from __future__ import annotations
import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

def _run(cmd, cwd, env):
    p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=120, env=env)
    return p

def _sha(p: Path) -> str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1<<20), b""):
            h.update(c)
    return h.hexdigest()

def main()->int:
    if len(sys.argv)!=5:
        print(f"usage: {sys.argv[0]} BOOT_WEEKLY OWN_SRC DST_PARENT STAMP", flush=True)
        return 2
    BOOT=Path(sys.argv[1]).resolve()
    OWN=Path(sys.argv[2]).resolve()
    PARENT=Path(sys.argv[3]).resolve()
    STAMP=sys.argv[4].strip()
    for v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE","GIT_OBJECT_DIRECTORY","GIT_ALTERNATE_OBJECT_DIRECTORIES"):
        if os.environ.get(v):
            print(f"UNSAFE inherited {v}", flush=True)
            return 2
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"1","GIT_ALLOW_PROTOCOL":"file",
                "PYTHONDONTWRITEBYTECODE":"1","LC_ALL":"C"})
    PARENT.mkdir(parents=True, exist_ok=True)
    DST=PARENT/f"versioned-renewal-faultresume-{STAMP}"/"renewal-weekly"
    if DST.exists():
        print(f"FATAL dst exists: {DST}", flush=True)
        return 2
    # Pre: BOOT HEAD 721a04d, OWN HEAD 409
    h=_run(["git","rev-parse","HEAD"],BOOT,env)
    print(f"BOOT HEAD={h.stdout.strip()} rc={h.returncode}", flush=True)
    if h.stdout.strip()!="721a04d85532d7855f3e54cc411f5847c787726e":
        print("FATAL BOOT HEAD !=721a04d", flush=True)
        return 2
    h2=_run(["git","rev-parse","HEAD"],OWN,env)
    print(f"OWN HEAD={h2.stdout.strip()} rc={h2.returncode}", flush=True)
    if h2.stdout.strip()!="409b292756dd1277b9dfae87679934c0d2ce251c":
        print("FATAL OWN HEAD !=409", flush=True)
        return 2
    # Clone --no-hardlinks
    cp=_run(["git","clone","--no-hardlinks",str(BOOT),str(DST)],PARENT,env)
    print(f"CLONE rc={cp.returncode}", flush=True)
    if cp.returncode!=0:
        print(cp.stderr[:1000], flush=True)
        return 2
    _run(["git","remote","set-url","origin","https://example.invalid/versioned-renewal-faultresume-weekly.git"],DST,env)
    _run(["git","config","user.name","rephase-fixture"],DST,env)
    _run(["git","config","user.email","fixture@example.invalid"],DST,env)
    _run(["git","config","commit.gpgsign","false"],DST,env)
    # Copy untracked old E from BOOT (byte copy, no hardlinks)
    src_stat=_run(["git","status","--porcelain=v1","--untracked-files=normal"],BOOT,env).stdout
    e_paths=[]
    for line in src_stat.splitlines():
        if not line.startswith("??"):
            continue
        rel=line[3:].strip().strip('"')
        if ".git" in Path(rel).parts:
            continue
        if (BOOT/rel).exists():
            e_paths.append(rel)
    print(f"E_PATHS={len(e_paths)}", flush=True)
    for rel in sorted(e_paths):
        s,d=BOOT/rel, DST/rel
        if d.exists():
            print(f"FATAL E target exists: {rel}", flush=True)
            return 2
        if s.is_dir() and not s.is_symlink():
            shutil.copytree(str(s),str(d),symlinks=True,copy_function=shutil.copy2)
        else:
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(s),str(d))
    # Verify E bytes + inode disjoint (spot 20)
    for rel in sorted(e_paths)[:20]:
        s,d=BOOT/rel, DST/rel
        if s.is_file():
            if _sha(s)!=_sha(d):
                print(f"FATAL E sha mismatch: {rel}", flush=True)
                return 2
            if (s.stat().st_dev,s.stat().st_ino)==(d.stat().st_dev,d.stat().st_ino):
                print(f"FATAL E inode sharing: {rel}", flush=True)
                return 2
    print("E_COPY_OK", flush=True)
    # Overlay full 740 OWN source (tracked code/schemas only, never E)
    # Collect OWN intended files via same os.walk per-dir (740)
    own_files=[]
    for root,dirs,files in os.walk(OWN):
        if ".git" in dirs:
            dirs.remove(".git")
        if ".git" in root.split(os.sep):
            continue
        for f in sorted(files):
            full=os.path.join(root,f)
            if "/.git/" in full:
                continue
            if "__pycache__" in full or full.endswith(".pyc"):
                continue
            rel=os.path.relpath(full,OWN)
            own_files.append(rel)
    print(f"OWN_FILES={len(own_files)}", flush=True)
    if len(own_files)!=740:
        print("FATAL OWN !=740", flush=True)
        return 2
    for rel in own_files:
        s,d=OWN/rel, DST/rel
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(s),str(d))
    print("OVERLAY_OK", flush=True)
    # Git add ONLY own 740 paths (never -A, never E)
    # Build add list: only those that are tracked or new but in own list
    add=_run(["git","add","--"]+own_files,DST,env)
    print(f"ADD rc={add.returncode} {add.stderr[:500]}", flush=True)
    if add.returncode!=0:
        return 2
    status=_run(["git","status","--porcelain=v1","--untracked-files=all"],DST,env).stdout
    # Ensure no E staged: staged must be subset of own_files
    for line in status.splitlines():
        code,path=line[:2],line[3:].strip().strip('"')
        if code[0] in ("A","M") and path not in own_files and path not in [p for p in own_files]:
            # Allow renames? No renames expected
            print(f"FATAL staged non-source: {line}", flush=True)
            return 2
    # Ensure E still untracked
    untracked=[l for l in status.splitlines() if l.startswith("??")]
    print(f"UNTRACKED_AFTER_ADD={len(untracked)} (E preserved)", flush=True)
    if len(untracked)==0:
        print("FATAL E missing (should be untracked)", flush=True)
        return 2
    commit=_run(["git","commit","-m","HIGH phase TEST-ONLY: fault-resume 740 source (byte-identical 740, trio untouched, before authority)","--no-verify"],DST,env)
    print(f"COMMIT rc={commit.returncode} {commit.stdout[:500]} {commit.stderr[:500]}", flush=True)
    if commit.returncode!=0:
        return 2
    head=_run(["git","rev-parse","HEAD"],DST,env).stdout.strip()
    print(f"NEW_HEAD={head}", flush=True)
    log=_run(["git","log","--oneline","-3"],DST,env).stdout
    print(f"LOG:\n{log}", flush=True)
    if "721a04d" not in _run(["git","log","--oneline"],DST,env).stdout:
        print("FATAL ancestry missing 721a04d", flush=True)
        return 2
    alt=DST/".git"/"objects"/"info"/"alternates"
    if alt.exists():
        print("FATAL alternates", flush=True)
        return 2
    print("FIXTURE_OK", flush=True)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
