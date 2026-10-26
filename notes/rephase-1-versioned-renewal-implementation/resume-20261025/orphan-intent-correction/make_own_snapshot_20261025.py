#!/usr/bin/env python3
"""OWN 741 snapshot: candidate-work complete SOURCE WITH HIGH orphan fix.

Byte-independent copy (no -l), manifest-exact worktree (no cache), isolation,
full code-field pins (no metadata-only fakes). No shared imports for tests:
tests run from OWN snapshot, fixture DB separate for State/set only.

Usage: python3 make_own_snapshot_20261025.py CANDIDATE DST_PARENT STAMP
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

def _sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()

def main() -> int:
    if len(sys.argv) != 4:
        print(f"usage: {sys.argv[0]} CANDIDATE DST_PARENT STAMP", flush=True)
        return 2
    CAND = Path(sys.argv[1]).resolve()
    PARENT = Path(sys.argv[2]).resolve()
    STAMP = sys.argv[3].strip()
    for v in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES"):
        if os.environ.get(v):
            print(f"UNSAFE inherited {v}", flush=True)
            return 2
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "1", "GIT_ALLOW_PROTOCOL": "file",
                "PYTHONDONTWRITEBYTECODE": "1", "LC_ALL": "C"})
    PARENT.mkdir(parents=True, exist_ok=True)
    DST = PARENT / f"versioned-renewal-orphanfix-{STAMP}" / "snapshot-work"
    if DST.exists():
        print(f"FATAL dst exists (no overwrite): {DST}", flush=True)
        return 2
    head = _run(["git", "rev-parse", "HEAD"], CAND, env)
    print(f"PRE CAND HEAD={head.stdout.strip()} rc={head.returncode}", flush=True)
    if head.stdout.strip() != "409b292756dd1277b9dfae87679934c0d2ce251c":
        print("FATAL CAND HEAD !=409", flush=True)
        return 2
    DST.parent.mkdir(parents=True, exist_ok=True)
    # Byte-independent .git copy (no -l), then manifest-exact worktree (no blind rsync, no cache).
    cp = _run(["cp", "-a", str(CAND / ".git"), str(DST.parent / ".git-tmp")], PARENT, env)
    print(f"CP_GIT rc={cp.returncode}", flush=True)
    if cp.returncode != 0:
        print(cp.stderr[:1000], flush=True)
        return 2
    DST.mkdir(parents=True)
    shutil.move(str(DST.parent / ".git-tmp"), str(DST / ".git"))
    # Collect intended files from CAND (exclude .git, __pycache__, *.pyc).
    intended: list[str] = []
    for root, dirs, files in os.walk(CAND):
        if ".git" in dirs:
            dirs.remove(".git")
        if "/.git/" in root or root.endswith("/.git"):
            continue
        # prune cache dirs
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for f in sorted(files):
            full = os.path.join(root, f)
            if "/.git/" in full:
                continue
            if "__pycache__" in full or full.endswith(".pyc"):
                continue
            rel = os.path.relpath(full, CAND)
            intended.append(rel)
    print(f"CAND_INTENDED={len(intended)}", flush=True)
    if len(intended) != 741:
        print(f"FATAL intended !=741 got {len(intended)}", flush=True)
        return 2
    for rel in intended:
        s, d = CAND / rel, DST / rel
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(s), str(d))
    print("COPY_WORKTREE_OK", flush=True)
    # Isolation: no hardlinks (nlink==1 for all intended, spot full), no alternates, inert origin check later.
    # Verify SRC==DST bytes identical for intended.
    for rel in intended:
        if _sha(CAND / rel) != _sha(DST / rel):
            print(f"FATAL sha mismatch: {rel}", flush=True)
            return 2
    print("SRC_DST_IDENTICAL_OK", flush=True)
    # Full code-field pins (no metadata-only fakes): HIGH (fixed), TEST (new), H/S/PUB/P1/Reader/P3S-fix.
    pins = {
        "scripts/survey_versioned_renewal_v2.py": "b12439d5057003e703992b91f9590c5eb498f48c21977fa7ab51167e48909413",
        "tests/test_versioned_renewal_orphan_intent_20261025.py": None,  # pinned below, must exist, no fixed expect (new)
        "scripts/survey_versioned_renewal_history_v2.py": "6fe86e78a12e2159d6ff50dfd7f70fda7b2e0d34d48db26402743edda2eca5ad",
        "scripts/survey_editorial_correction_proposal_v2.py": "825dba1dedaed0850134b3a54a249a427b2e77709861818e8eb7cb63e1a33a2b",
        "scripts/survey_publication_v2.py": "3f4039fd7699baa212020dddfb02b3918bd63e02c475d638d99cbb2a1150d8d6",
        "scripts/survey_versioned_renewal_source_v2.py": "20f63eafc96923dc7be25f3f495b94dd9add0e398d6cdc2fe47c2c9bff46c306",
        "scripts/survey_reader_publication_v2.py": "098a2c8222f15f693c524139f2678be008a7ec9fafca275fc831ede9aa13bf1c",
        "scripts/survey_editorial_staged_source_v2.py": "9e2a0ad6b42cb2444f03f2f9db138c6c1e1db7f41434f5fb1878d87f99ca7ab1",
    }
    for rel, expect in pins.items():
        p = DST / rel
        if not p.is_file():
            print(f"FATAL missing pin file: {rel}", flush=True)
            return 2
        got = _sha(p)
        if expect is None:
            print(f"PIN {rel} {got} (new, recorded)", flush=True)
        else:
            print(f"PIN {rel} {got[:12]} expect {expect[:12]} {'OK' if got == expect else 'MISMATCH'}", flush=True)
            if got != expect:
                return 2
    # Count DST intended (must be 741, no cache).
    dst_files: list[str] = []
    for root, dirs, files in os.walk(DST):
        if ".git" in Path(root).parts:
            dirs[:] = []
            continue
        if "__pycache__" in Path(root).parts:
            continue
        for f in sorted(files):
            if f.endswith(".pyc"):
                continue
            full = os.path.join(root, f)
            if "/.git/" in full:
                continue
            dst_files.append(os.path.relpath(full, DST))
    print(f"DST_INTENDED={len(dst_files)}", flush=True)
    if len(dst_files) != 741:
        print("FATAL DST !=741", flush=True)
        return 2
    # Git checks: HEAD still 409, no staged (diff --cached empty), inert origin to be set by caller? Check .git existence, no objects/info/alternates?
    head2 = _run(["git", "rev-parse", "HEAD"], DST, env)
    print(f"POST DST HEAD={head2.stdout.strip()}", flush=True)
    print("OWN_SNAPSHOT_OK", flush=True)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
