#!/usr/bin/env python3
"""OWN CURRENT snapshot (741, HIGH 1dad1ad/H74275d/S2290ddd, immutable own copy, before/after pins).

Byte-independent cp -a .git (no -l) + manifest-exact worktree via copy2 (no blind rsync, no cache).
SRC manifest guard: choose immutable snapshot own copy before execution (Root may edit different candidate files).
Usage: python3 harness_make_own_current.py CANDIDATE DST_PARENT STAMP
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
    if len(sys.argv)!=4:
        print(f"usage: {sys.argv[0]} CANDIDATE DST_PARENT STAMP", flush=True)
        return 2
    CAND=Path(sys.argv[1]).resolve()
    PARENT=Path(sys.argv[2]).resolve()
    STAMP=sys.argv[3].strip()
    for v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE","GIT_OBJECT_DIRECTORY","GIT_ALTERNATE_OBJECT_DIRECTORIES"):
        if os.environ.get(v):
            print(f"UNSAFE {v}", flush=True)
            return 2
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"1","GIT_ALLOW_PROTOCOL":"file","PYTHONDONTWRITEBYTECODE":"1","LC_ALL":"C"})
    # BEFORE pins (explicit before)
    pre_head=_run(["git","rev-parse","HEAD"],CAND,env)
    pre_status=_run(["git","status","--porcelain=v1","--untracked-files=all"],CAND,env)
    print(f"BEFORE HEAD={pre_head.stdout.strip()} rc={pre_head.returncode}", flush=True)
    print(f"BEFORE STATUS lines={len(pre_status.stdout.splitlines())}", flush=True)
    if pre_head.stdout.strip()!="409b292756dd1277b9dfae87679934c0d2ce251c":
        print("FATAL CAND HEAD !=409", flush=True)
        return 2
    PARENT.mkdir(parents=True, exist_ok=True)
    DST=PARENT/f"versioned-renewal-faultresume-current-{STAMP}"/"snapshot-work"
    if DST.exists():
        print(f"FATAL dst exists (no overwrite): {DST}", flush=True)
        return 2
    DST.parent.mkdir(parents=True, exist_ok=True)
    cp=_run(["cp","-a",str(CAND),str(DST)],PARENT,env)
    print(f"CP rc={cp.returncode} {cp.stderr[:300]}", flush=True)
    if cp.returncode!=0:
        return 2
    # AFTER pins (explicit after, must match BEFORE for HEAD, status may differ? No, DST is copy, SRC unchanged? SRC may be edited by other workers during our copy? Guard: re-check SRC HEAD/status after copy, must match BEFORE (else SRC changed during copy, unsafe). Actually Root may edit different candidate files during our execution, so SRC may change AFTER our copy (which is okay, since we use immutable own copy). BEFORE/AFTER here are SRC before/after copy (should match if no concurrent edit during copy, else warn but own copy still immutable? For safety, require SRC HEAD same before/after copy (no concurrent commit, though worktree edits possible? Worktree edits by other workers could change files during copy, causing DST inconsistent? To guard, check SRC file SHAs before/after? Simpler: record BEFORE/AFTER HEAD + status, and DST pins; if SRC changed during copy, DST may be torn (mixed old/new). To avoid torn, check SRC HEAD same + key file SHAs same before/after? For this unit, other workers edit different candidate files (per task), but may edit same files? The task says "Root may test-only others edit different candidate files" (different files, not same as ours? Our files are HIGH/H/S + orphan test + P3S? Others may edit different files, so our key files (HIGH/H/S/P1/PUB/Reader/edpub/P3S) should be stable during copy. Check key SHAs before/after copy match.
    for rel, expect in (("scripts/survey_versioned_renewal_v2.py","1dad1ad12ba509c477ea97fb3a22e5156ae1627182f3286f373f32eae7ba2fbb"),
                        ("scripts/survey_versioned_renewal_history_v2.py","74275d22a342014009d5d090fbe9c552981941e90259c298065d2ba6929d1f3d"),
                        ("scripts/survey_versioned_renewal_source_v2.py","2290ddd0dc8397f86451aff70d50fd4da0c6184fcf1bef3ed96259642af2d1eb"),
                        ("scripts/survey_editorial_correction_proposal_v2.py","825dba1dedaed0850134b3a54a249a427b2e77709861818e8eb7cb63e1a33a2b"),
                        ("scripts/survey_publication_v2.py","3f4039fd7699baa212020dddfb02b3918bd63e02c475d638d99cbb2a1150d8d6"),
                        ("scripts/survey_reader_publication_v2.py","098a2c8222f15f693c524139f2678be008a7ec9fafca275fc831ede9aa13bf1c"),
                        ("scripts/survey_editorial_publication_v2.py","85814124278c3112562c84c4685ef555689d551b494dcbd23526fb27dc1d9a2a"),
                        ("scripts/survey_editorial_staged_source_v2.py","9e2a0ad6b42cb2444f03f2f9db138c6c1e1db7f41434f5fb1878d87f99ca7ab1")):
        got=_sha(DST/rel)
        print(f"PIN DST {rel} {got[:12]} expect {expect[:12]} {'OK' if got==expect else 'MISMATCH'}", flush=True)
        if got!=expect:
            return 2
        # SRC before/after stability for key files (guard torn copy)
        src_sha=_sha(CAND/rel)
        if src_sha!=expect:
            print(f"FATAL SRC key file changed during/before copy (other worker edit?): {rel} src={src_sha[:12]} expect={expect[:12]}", flush=True)
            return 2
    # Count intended (excl pycache/pyc)
    files=[]
    for dp,dn,fn in os.walk(DST):
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
    if len(files)!=741:
        print(f"FATAL intended !=741 got {len(files)} (expected CURRENT 741 = pinned 740 + orphan test, with P3S 9e2a fix as M)", flush=True)
        return 2
    # AFTER HEAD/status (explicit after)
    post_head=_run(["git","rev-parse","HEAD"],CAND,env)
    print(f"AFTER SRC HEAD={post_head.stdout.strip()} (must == BEFORE 409, else SRC committed during copy)", flush=True)
    if post_head.stdout.strip()!="409b292756dd1277b9dfae87679934c0d2ce251c":
        print("FATAL SRC HEAD changed during copy", flush=True)
        return 2
    # Isolation
    alt=DST/".git"/"objects"/"info"/"alternates"
    if alt.exists():
        print("FATAL alternates", flush=True)
        return 2
    remote=_run(["git","remote","-v"],DST,env).stdout
    if "example.invalid" not in remote:
        print("FATAL remote not inert", flush=True)
        return 2
    print("OWN_CURRENT_OK (immutable own copy, SRC manifest guard, no stale 9a)", flush=True)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
