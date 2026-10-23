#!/usr/bin/env python3
"""R6 cross-binding focused tests (new SOURCE R6 vs old R5b).

Scope: narrow R6 fix only (Candidate 6 vs seal, Reader trio, Bundle, Reviews,
Gate, Build + external review pinned). No whole PASS claimed.

Fixtures: actual validated INERT_W (weekly-inert, State r1, set2 sealed wk-r5b-2).
New scratch ONLY .rephase-1-editorial-runtime/r6-tests/ (workspace-ignored).
Dedicated evidence under notes/.../correction-r6/ (raw stdout/stderr/exit).

Cases:
  R6-SEAL-ONLY: same-byte copy of semantic review to new path, seal points
    there (fresh set_sha), Candidate still old path. Old code UNEXPECTED_PASS,
    new code must refuse (Candidate<->seal path+SHA). Uses existing
    final-r5b-faults/a-equal-sha-wrong-path fixture for before/after.
  R6-CAND-ONLY: same-byte copy to new path, Candidate points there (fresh
    candidate_sha + fresh seal candidate role + fresh set_sha), seal review
    still old path. New code must refuse.
  R6-TARGET-REBIND: same-SHA manuscript copy to new path, review internal
    reader_manuscript points there (fresh review_sha + candidate + seal
    digests fresh), seal manuscript still old path. New code must refuse
    after fresh digests (reviewed-target path, not hash-only).
  R6-EXTERNAL-POSITIVE (actual finalize control): delete seal outputs from
    INERT copy, copy reviews to nondefault outside pub path
    (<P>/external-reviews/), run actual finalize_publication with external
    paths (new SOURCE), then validate (L+H) must PASS, then activate + strict
    readback must PASS (healthy control, unchanged reviewed targets).

No source edit outside DST, no ordinary commits/net/clean/reset/rawdelete.
New SourceSnapshot R6 already committed under ignored scratch; tests run in
copies, never inside SRC. Own GitDir verified NOT parent before Git writes.
"""
from __future__ import annotations
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey").resolve()
OLD_SRC = REPO / ".rephase-1-editorial-runtime/jgas-editorial-r5b-20261022T140000Z/candidate-partial-b40de60"
NEW_SRC = REPO / ".rephase-1-editorial-runtime/jgas-editorial-r6-20261023T000000Z/candidate-partial-b40de60"
INERT_W = REPO / ".rephase-1-editorial-runtime/final-r5b/weekly-inert"
FAULT_OLD = REPO / ".rephase-1-editorial-runtime/final-r5b-faults/a-equal-sha-wrong-path"
R6_BASE = REPO / ".rephase-1-editorial-runtime/r6-tests"
NOTES_R6 = REPO / "notes/rephase-1-editorial-operation-implementation/correction-r6"

ISSUE = "2026-W37"
PROP = "wk-r5b-2"
PUBDIR = f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP}/publication"
STATE_REL = f"sources/{ISSUE}/production-state.json"
SET_REL = f"{PUBDIR}/publication-set.json"

def log(m: str):
    print(m, flush=True)

def run_git(cwd: Path, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file"})
    return subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True, timeout=60, env=env)

def sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()

def base_env(pythonpath: Path, tmpdir: Path):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_") and k not in ("PYTHONPATH", "PYTHONPYCACHEPREFIX", "TMPDIR", "TEMP", "TMP")}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPYCACHEPREFIX"] = str(tmpdir / "pycache")
    env["TMPDIR"] = str(tmpdir)
    env["GIT_NO_LAZY_FETCH"] = "1"
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_ALLOW_PROTOCOL"] = "file"
    env["PYTHONPATH"] = str(pythonpath)
    (tmpdir / "pycache").mkdir(parents=True, exist_ok=True)
    tmpdir.mkdir(parents=True, exist_ok=True)
    return env

def run_child(pythonpath: Path, cwd: Path, code: str, tmpdir: Path, timeout: int = 120):
    env = base_env(pythonpath, tmpdir)
    t0 = time.monotonic()
    p = subprocess.run([sys.executable, "-B", "-c", code], cwd=str(cwd), capture_output=True, text=True, timeout=timeout, env=env)
    dt = time.monotonic() - t0
    return {"exit": p.returncode, "stdout": p.stdout, "stderr": p.stderr, "dt": dt}

def verify_copy_toplevel(dst: Path, label: str):
    toplevel = run_git(dst, "rev-parse", "--show-toplevel").stdout.strip()
    assert Path(toplevel).resolve() == dst.resolve(), f"{label} toplevel {toplevel} != {dst}"
    gitdir = run_git(dst, "rev-parse", "--absolute-git-dir").stdout.strip()
    assert Path(gitdir).resolve() == (dst / ".git").resolve(), f"{label} gitdir {gitdir}"
    assert "r6-tests" in str(dst) or "final-r5b-faults" in str(dst), f"{label} not approved scratch {dst}"

def cp_fixture(src: Path, dst: Path, label: str):
    if dst.exists():
        raise AssertionError(f"exists {dst}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["cp", "-a", str(src), str(dst)], capture_output=True, text=True, timeout=180)
    assert r.returncode == 0, f"cp {label} failed {r.stderr[:800]}"
    verify_copy_toplevel(dst, label)
    return dst

def main() -> int:
    R6_BASE.mkdir(parents=True, exist_ok=True)
    NOTES_R6.mkdir(parents=True, exist_ok=True)
    (R6_BASE / "tmp").mkdir(parents=True, exist_ok=True)
    results = []
    # Healthy control: INERT_W original must PASS with new code (L+H)
    log("=== R6 healthy control (INERT_W original, new code) ===")
    tmp_h = R6_BASE / "tmp" / "healthy"
    tmp_h.mkdir(parents=True, exist_ok=True)
    code_h = f"""
import sys; sys.path.insert(0, r'{NEW_SRC}')
from pathlib import Path
from scripts import survey_publication_set_v2 as low
from scripts import survey_editorial_publication_v2 as high
repo=Path(r'{INERT_W}')
s=low.validate_seal(repo, r'{SET_REL}')
print(f"LOW_PASS {{s.get('issue_id')}}")
v=high.validate_prepared_set(repo, r'{STATE_REL}', r'{SET_REL}')
print(f"HIGH_PASS {{v.get('issue_id')}}")
"""
    rh = run_child(NEW_SRC, INERT_W, code_h, tmp_h)
    log(f"healthy new-code exit={rh['exit']} dt={rh['dt']:.1f}s")
    log(f"STDOUT: {rh['stdout'][:1500]}")
    log(f"STDERR: {rh['stderr'][:800]}")
    (NOTES_R6 / "r6-healthy-control-stdout.txt").write_text(rh["stdout"])
    (NOTES_R6 / "r6-healthy-control-stderr.txt").write_text(rh["stderr"])
    (NOTES_R6 / "r6-healthy-control-exit.txt").write_text(str(rh["exit"]))
    assert rh["exit"] == 0, f"healthy control must PASS with new code {rh['stdout'][:800]} {rh['stderr'][:800]}"
    results.append(("healthy", "PASS"))

    # R6-SEAL-ONLY: existing fault fixture (old code UNEXPECTED_PASS, new code refuse)
    log("=== R6-SEAL-ONLY (existing a-equal-sha-wrong-path) ===")
    assert FAULT_OLD.is_dir(), f"missing old fault {FAULT_OLD}"
    # State SHA before/after (no-write check)
    state_p = FAULT_OLD / STATE_REL
    before_sha = sha_file(state_p)
    before_bytes = state_p.stat().st_size
    tmp_old = R6_BASE / "tmp" / "seal-old"
    tmp_new = R6_BASE / "tmp" / "seal-new"
    tmp_old.mkdir(parents=True, exist_ok=True)
    tmp_new.mkdir(parents=True, exist_ok=True)
    code_seal = f"""
import sys; sys.path.insert(0, r'{{SRC}}')
from pathlib import Path
from scripts import survey_publication_set_v2 as low
from scripts import survey_editorial_publication_v2 as high
repo=Path(r'{FAULT_OLD}')
# L first (independent)
try:
    low.validate_seal(repo, r'{SET_REL}')
    print("L_UNEXPECTED_PASS")
except Exception as e:
    print(f"L_REFUSED {{type(e).__name__}}: {{str(e)[:1000]}}")
# H fullset (independent)
try:
    high.validate_prepared_set(repo, r'{STATE_REL}', r'{SET_REL}')
    print("H_UNEXPECTED_PASS")
except Exception as e:
    print(f"H_REFUSED {{type(e).__name__}}: {{str(e)[:1500]}}")
"""
    # Old code (should UNEXPECTED_PASS for both L+H per R5b BLOCKER)
    r_old = run_child(OLD_SRC, FAULT_OLD, code_seal.replace("{{SRC}}", str(OLD_SRC)), tmp_old)
    log(f"seal-only OLD exit={r_old['exit']} dt={r_old['dt']:.1f}s")
    log(f"OLD STDOUT: {r_old['stdout'][:2000]}")
    (NOTES_R6 / "r6-seal-only-old-stdout.txt").write_text(r_old["stdout"])
    (NOTES_R6 / "r6-seal-only-old-stderr.txt").write_text(r_old["stderr"])
    (NOTES_R6 / "r6-seal-only-old-exit.txt").write_text(str(r_old["exit"]))
    # New code (must refuse both)
    r_new = run_child(NEW_SRC, FAULT_OLD, code_seal.replace("{{SRC}}", str(NEW_SRC)), tmp_new)
    log(f"seal-only NEW exit={r_new['exit']} dt={r_new['dt']:.1f}s")
    log(f"NEW STDOUT: {r_new['stdout'][:2000]}")
    (NOTES_R6 / "r6-seal-only-new-stdout.txt").write_text(r_new["stdout"])
    (NOTES_R6 / "r6-seal-only-new-stderr.txt").write_text(r_new["stderr"])
    (NOTES_R6 / "r6-seal-only-new-exit.txt").write_text(str(r_new["exit"]))
    after_sha = sha_file(state_p)
    assert before_sha == after_sha, "seal-only validation must be no-write (State unchanged)"
    (NOTES_R6 / "r6-seal-only-state-before-after.txt").write_text(f"before {before_sha} {before_bytes}\nafter {after_sha} {(FAULT_OLD/STATE_REL).stat().st_size}\nno-write OK\n")
    # Old must have UNEXPECTED_PASS (at least H), new must have REFUSED (both)
    assert "UNEXPECTED_PASS" in r_old["stdout"], f"old seal-only should UNEXPECTED_PASS (R5b BLOCKER) {r_old['stdout'][:800]}"
    assert "REFUSED" in r_new["stdout"] and "UNEXPECTED_PASS" not in r_new["stdout"], f"new seal-only must refuse {r_new['stdout'][:1000]}"
    # Require explicit path binding in refusal (not just digest)
    low_new = r_new["stdout"].lower()
    assert any(k in low_new for k in ["path", "candidate", "bind", "seal"]), f"new seal-only refusal should mention path/candidate/bind {r_new['stdout'][:800]}"
    results.append(("seal-only", "PASS"))

    log(f"TOTAL R6 focused part1 pass={len(results)}")
    (NOTES_R6 / "r6-focused-summary.json").write_text(json.dumps([{"name": n, "status": s} for n, s in results], indent=2))
    print("EXIT:0")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("EXIT:2")
        sys.exit(2)
