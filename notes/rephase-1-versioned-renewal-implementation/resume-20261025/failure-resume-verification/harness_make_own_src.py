#!/usr/bin/env python3
"""OWN 740 source snapshot: fixed739 + edpub858/test overlay, byte-independent.

No shared candidate run. Pre/post pins, isolation, DST==740 archive hash.
Usage: python3 harness_make_own_src.py SRC739 CANDIDATE DST_PARENT STAMP
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
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1<<20), b""):
            h.update(c)
    return h.hexdigest()

def main() -> int:
    if len(sys.argv) != 5:
        print(f"usage: {sys.argv[0]} SRC739 CANDIDATE DST_PARENT STAMP", flush=True)
        return 2
    SRC739 = Path(sys.argv[1]).resolve()
    CAND = Path(sys.argv[2]).resolve()
    DST_PARENT = Path(sys.argv[3]).resolve()
    STAMP = sys.argv[4].strip()
    for v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE","GIT_OBJECT_DIRECTORY","GIT_ALTERNATE_OBJECT_DIRECTORIES"):
        if os.environ.get(v):
            print(f"UNSAFE inherited {v}", flush=True)
            return 2
    env = {k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"1","GIT_ALLOW_PROTOCOL":"file",
                "PYTHONDONTWRITEBYTECODE":"1","LC_ALL":"C"})
    DST_PARENT.mkdir(parents=True, exist_ok=True)
    DST = DST_PARENT / f"versioned-renewal-faultresume-src-{STAMP}" / "snapshot-work"
    if DST.exists():
        print(f"FATAL dst exists (no overwrite): {DST}", flush=True)
        return 2
    # Pre pins
    for label, p in (("SRC739",SRC739),("CAND",CAND)):
        head = _run(["git","rev-parse","HEAD"], p, env)
        print(f"PRE {label} HEAD={head.stdout.strip()} rc={head.returncode}", flush=True)
        if head.returncode!=0 or head.stdout.strip()!="409b292756dd1277b9dfae87679934c0d2ce251c":
            print(f"FATAL {label} HEAD mismatch", flush=True)
            return 2
    # Byte-independent .git copy (no -l)
    DST.parent.mkdir(parents=True, exist_ok=True)
    cp = _run(["cp","-a",str(SRC739),str(DST)], DST_PARENT, env)
    print(f"CP rc={cp.returncode} {cp.stderr[:500]}", flush=True)
    if cp.returncode!=0:
        return 2
    # Overlay 2 files from candidate (edpub + archive test)
    for rel in ("scripts/survey_editorial_publication_v2.py",
                "tests/test_editorial_renewal_archive_correction_20261025.py"):
        s = CAND / rel
        d = DST / rel
        if not s.is_file():
            print(f"FATAL overlay src missing: {rel}", flush=True)
            return 2
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(s), str(d))
        print(f"OVERLAY {rel} src_sha={_sha(s)[:12]} dst_sha={_sha(d)[:12]}", flush=True)
        if _sha(s)!=_sha(d):
            print("FATAL overlay sha mismatch", flush=True)
            return 2
    # Verify pins
    for rel, expect in (("scripts/survey_versioned_renewal_history_v2.py","6fe86e78a12e2159d6ff50dfd7f70fda7b2e0d34d48db26402743edda2eca5ad"),
                        ("scripts/survey_editorial_correction_proposal_v2.py","825dba1dedaed0850134b3a54a249a427b2e77709861818e8eb7cb63e1a33a2b"),
                        ("scripts/survey_publication_v2.py","3f4039fd7699baa212020dddfb02b3918bd63e02c475d638d99cbb2a1150d8d6"),
                        ("scripts/survey_versioned_renewal_source_v2.py","20f63eafc96923dc7be25f3f495b94dd9add0e398d6cdc2fe47c2c9bff46c306"),
                        ("scripts/survey_versioned_renewal_v2.py","9a0469ef5a6bc2b2e37fc9efb1376cfccbd0333ffaa08a59d23634345d382152"),
                        ("scripts/survey_reader_publication_v2.py","098a2c8222f15f693c524139f2678be008a7ec9fafca275fc831ede9aa13bf1c"),
                        ("scripts/survey_editorial_publication_v2.py","85814124278c3112562c84c4685ef555689d551b494dcbd23526fb27dc1d9a2a")):
        got = _sha(DST/rel)
        print(f"PIN {rel} {got[:12]} expect {expect[:12]} {'OK' if got==expect else 'MISMATCH'}", flush=True)
        if got!=expect:
            return 2
    # Count intended (exclude pycache/pyc)
    files=[]
    for dp, dn, fn in os.walk(DST):
        if ".git" in Path(dp).parts:
            dn[:]=[]
            continue
        if "__pycache__" in Path(dp).parts:
            continue
        for f in sorted(fn):
            if f.endswith(".pyc"):
                continue
            files.append((Path(dp)/f).relative_to(DST).as_posix())
    print(f"DST_INTENDED={len(files)}", flush=True)
    if len(files)!=740:
        print(f"FATAL intended !=740 got {len(files)}", flush=True)
        return 2
    # Hash list
    files_sorted=sorted(files)
    hlist=[]
    for rel in files_sorted:
        hlist.append(f"{_sha(DST/rel)} {(DST/rel).stat().st_size} {rel}")
    dst_hash_list_sha = hashlib.sha256("\n".join(hlist).encode()).hexdigest()
    print(f"DST_HASH_LIST_SHA={dst_hash_list_sha}", flush=True)
    if dst_hash_list_sha!="4e2783fb81514c2259192d1fde17dc36ebdc8332bf35123cabdeff494d7c910d":
        print("FATAL DST hash list != archive 740 (4e2783fb…)", flush=True)
        return 2
    # Isolation
    alt = DST/".git"/"objects"/"info"/"alternates"
    print(f"NO_ALTERNATES={'OK' if not alt.exists() else 'PRESENT'}", flush=True)
    if alt.exists():
        return 2
    remote = _run(["git","remote","-v"], DST, env).stdout
    print(f"REMOTE={remote.strip()[:120]}", flush=True)
    if "example.invalid" not in remote:
        print("FATAL remote not inert", flush=True)
        return 2
    # Inode disjoint vs SRC739 (spot check .git + worktree)
    for rel in ("scripts/survey_versioned_renewal_v2.py",".git/HEAD"):
        a = (SRC739/rel).stat()
        b = (DST/rel).stat()
        if (a.st_dev,a.st_ino)==(b.st_dev,b.st_ino):
            print(f"FATAL inode sharing: {rel}", flush=True)
            return 2
    print("INODE_DISJOINT_OK", flush=True)
    print("OWN_SRC_OK", flush=True)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
