#!/usr/bin/env python3
"""Loader binding probe (packet-only, not shipping).

Verifies same-process loaded module __file__ paths are under snapshot-fixed,
hashes match frozen pins, and working files match committed Git blobs at HEAD.
"""
from __future__ import annotations
import hashlib
import subprocess
import sys
from pathlib import Path

SNAP = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/evidence-scaling-affected-verify-20261103T175000Z/snapshot-fixed")
EXPECTED = {
    "scripts/survey_evidence_v2.py": ("487425385052fa181b0a24954815c6fbb6882a0af1fc7256ef7352b309359c2a", 158943),
    "scripts/run_evidence_v2_interactive.py": ("5e195730d1553b2359eb5729cebaa49e9bd616b4b3f63b65dca413ef33c3e543", 45833),
    "scripts/survey_research_authority_v2.py": ("0974c709b55365ef93cded5e97707e705b8a59aae01734e52c40e3b40c1a008b", 218692),
    "tests/test_evidence_scaling_v2.py": ("7b862305db39afde93c44ca0f1ce2d4b5faf512729e6956a8166b16f09c0e12e", 106616),
}

def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main() -> int:
    if str(SNAP) not in sys.path:
        sys.path.insert(0, str(SNAP))
    import importlib
    mods = ["scripts.survey_evidence_v2", "scripts.run_evidence_v2_interactive", "scripts.survey_research_authority_v2"]
    ok = True
    for m in mods:
        mod = importlib.import_module(m)
        f = Path(mod.__file__).resolve()
        print(f"{m} __file__={f}")
        if str(f) != str((SNAP / m.replace(".", "/")).with_suffix(".py").resolve()):
            # allow .pyc? must be .py under snapshot
            if not str(f).startswith(str(SNAP.resolve())):
                print(f"WRONG_LOADER_PATH: {m} -> {f} not under {SNAP}")
                ok = False
                continue
        h = sha256_file(Path(f))
        sz = Path(f).stat().st_size
        rel = Path(f).relative_to(SNAP.resolve()).as_posix() if str(f).startswith(str(SNAP.resolve())) else "OUTSIDE"
        exp = EXPECTED.get(rel)
        print(f"  rel={rel} sha256={h} bytes={sz} mode={oct(Path(f).stat().st_mode & 0o777)}")
        if exp and (h != exp[0] or sz != exp[1]):
            print(f"  MISMATCH expected {exp}")
            ok = False
        # committed blob check: git diff --quiet for file + git show HEAD:rel | sha256
        r = subprocess.run(["git", "-C", str(SNAP), "show", f"HEAD:{rel}"], capture_output=True)
        if r.returncode != 0:
            print(f"  GIT_SHOW_FAIL {rel} rc={r.returncode}")
            ok = False
        else:
            gh = hashlib.sha256(r.stdout).hexdigest()
            print(f"  committed_blob_sha256={gh} match_working={gh==h}")
            if gh != h:
                print(f"  WORKING_VS_COMMITTED_MISMATCH {rel}")
                ok = False
    # git status clean?
    r = subprocess.run(["git", "-C", str(SNAP), "status", "--porcelain"], capture_output=True, text=True)
    print(f"git_status_porcelain_len={len(r.stdout.strip())} body={r.stdout.strip()[:500]!r}")
    if r.stdout.strip() != "":
        print("DIRTY_SNAPSHOT")
        ok = False
    r = subprocess.run(["git", "-C", str(SNAP), "rev-parse", "HEAD"], capture_output=True, text=True)
    print(f"HEAD={r.stdout.strip()}")
    print("LOADER_BINDING_OK" if ok else "LOADER_BINDING_FAIL")
    return 0 if ok else 2

if __name__ == "__main__":
    raise SystemExit(main())
