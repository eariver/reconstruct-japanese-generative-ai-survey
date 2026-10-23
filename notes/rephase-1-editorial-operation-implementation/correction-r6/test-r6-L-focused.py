#!/usr/bin/env python3
"""R6 L-focused cross-binding tests (new SOURCE R6, INERT_W, no ToolDrift).

L validate_seal is identity-only (no runtime/tool closure), so old INERT
fixtures remain valid for L after R6 code change (healthy passes). H fullset
on old INERT would ToolDrift (receipt current_tools pins old code SHAs vs new
R6 code) - do NOT edit receipts to green; H fresh authority via new SOURCE
Weekly operation is separate (r6-external-positive via actual finalize).

Cases (all L, independent, explicit path+SHA):
  healthy: INERT_W original seal must PASS L.
  seal-only: existing a-equal-sha-wrong-path (seal points to same-byte copy,
    fresh set_sha, Candidate old). Old L UNEXPECTED_PASS, new L must refuse
    with path/candidate/bind.
  cand-only: new fault from INERT_W (Candidate points to same-byte copy,
    fresh candidate_sha + seal candidate role + fresh set_sha, seal review old).
    New L must refuse.
  target-rebind: new fault (review internal reader_manuscript points to
    same-byte copy new path, fresh review_sha + candidate + seal digests,
    seal manuscript old). New L must refuse (reviewed-target path).
  external-consistent: new fault (review copied outside <P>/publication to
    <P>/external-reviews/, Candidate + seal both point there consistently,
    reviewed targets unchanged, fresh candidate_sha + set_sha). New L must
    PASS (permitted external pinned dependency, not inside-only).

Saves raw old/new, before/after/no-write (State SHA). No /tmp, no SRC tests.
"""
from __future__ import annotations
import hashlib
import json
import os
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
SEM_REL = f"{PUBDIR}/semantic-review-v2.json"

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
    sys.path.insert(0, str(NEW_SRC))
    from scripts import survey_production_v2 as core_new
    results = []

    # healthy L
    log("=== R6 healthy L (INERT_W original, new code) ===")
    tmp_h = R6_BASE / "tmp" / "healthy-L"
    tmp_h.mkdir(parents=True, exist_ok=True)
    code_h = f"""
import sys; sys.path.insert(0, r'{NEW_SRC}')
from pathlib import Path
from scripts import survey_publication_set_v2 as low
repo=Path(r'{INERT_W}')
s=low.validate_seal(repo, r'{SET_REL}')
print(f"LOW_PASS {{s.get('issue_id')}}")
"""
    rh = run_child(NEW_SRC, INERT_W, code_h, tmp_h)
    log(f"healthy L new exit={rh['exit']} {rh['stdout'][:500]}")
    (NOTES_R6 / "r6-healthy-L-stdout.txt").write_text(rh["stdout"])
    (NOTES_R6 / "r6-healthy-L-stderr.txt").write_text(rh["stderr"])
    (NOTES_R6 / "r6-healthy-L-exit.txt").write_text(str(rh["exit"]))
    assert rh["exit"] == 0 and "LOW_PASS" in rh["stdout"], f"healthy L must PASS {rh['stdout'][:800]} {rh['stderr'][:800]}"
    results.append(("healthy-L", "PASS"))

    # seal-only: old vs new L on existing fault
    log("=== R6-SEAL-ONLY L (old fault fixture) ===")
    assert FAULT_OLD.is_dir()
    state_p = FAULT_OLD / STATE_REL
    before_sha = sha_file(state_p)
    tmp_old = R6_BASE / "tmp" / "seal-old-L"
    tmp_new = R6_BASE / "tmp" / "seal-new-L"
    tmp_old.mkdir(parents=True, exist_ok=True)
    tmp_new.mkdir(parents=True, exist_ok=True)
    code_seal = """
import sys; sys.path.insert(0, r'__SRC__')
from pathlib import Path
from scripts import survey_publication_set_v2 as low
repo=Path(r'__FAULT__')
try:
    low.validate_seal(repo, r'__SET__')
    print("L_UNEXPECTED_PASS")
except Exception as e:
    print(f"L_REFUSED {type(e).__name__}: {str(e)[:1500]}")
""".replace("__SRC__", "__SRC_PLACEHOLDER__").replace("__FAULT__", str(FAULT_OLD)).replace("__SET__", SET_REL)
    r_old = run_child(OLD_SRC, FAULT_OLD, code_seal.replace("__SRC_PLACEHOLDER__", str(OLD_SRC)), tmp_old)
    r_new = run_child(NEW_SRC, FAULT_OLD, code_seal.replace("__SRC_PLACEHOLDER__", str(NEW_SRC)), tmp_new)
    log(f"seal-only OLD: {r_old['stdout'][:800]}")
    log(f"seal-only NEW: {r_new['stdout'][:1200]}")
    (NOTES_R6 / "r6-seal-only-L-old-stdout.txt").write_text(r_old["stdout"])
    (NOTES_R6 / "r6-seal-only-L-old-stderr.txt").write_text(r_old["stderr"])
    (NOTES_R6 / "r6-seal-only-L-old-exit.txt").write_text(str(r_old["exit"]))
    (NOTES_R6 / "r6-seal-only-L-new-stdout.txt").write_text(r_new["stdout"])
    (NOTES_R6 / "r6-seal-only-L-new-stderr.txt").write_text(r_new["stderr"])
    (NOTES_R6 / "r6-seal-only-L-new-exit.txt").write_text(str(r_new["exit"]))
    after_sha = sha_file(state_p)
    assert before_sha == after_sha, "seal-only L must be no-write"
    (NOTES_R6 / "r6-seal-only-L-state.txt").write_text(f"before {before_sha}\nafter {after_sha}\nno-write OK\n")
    assert "UNEXPECTED_PASS" in r_old["stdout"], f"old seal-only L should UNEXPECTED_PASS {r_old['stdout'][:800]}"
    assert "REFUSED" in r_new["stdout"] and "UNEXPECTED_PASS" not in r_new["stdout"], f"new seal-only L must refuse {r_new['stdout'][:1000]}"
    assert any(k in r_new["stdout"].lower() for k in ["path", "candidate", "bind"]), "refusal should mention path/candidate/bind"
    results.append(("seal-only-L", "PASS"))

    # cand-only: new fault from INERT_W
    log("=== R6-CAND-ONLY L (new fault, fresh digests) ===")
    dst_c = R6_BASE / "r6-cand-only"
    if dst_c.exists():
        import shutil as _sh
        _sh.rmtree(dst_c)
    cp_fixture(INERT_W, dst_c, "r6-cand-only")
    # same-byte copy to new path inside publication
    sem_orig = dst_c / SEM_REL
    new_rel = f"{PUBDIR}/semantic-review-forged.json"
    new_p = dst_c / new_rel
    new_p.write_bytes(sem_orig.read_bytes())
    assert sha_file(new_p) == sha_file(sem_orig)
    # update Candidate semantic_review to new path (same SHA), fresh candidate_sha
    cand_rel = f"{PUBDIR}/publication-candidate-v2.json"
    cand_p = dst_c / cand_rel
    cand = json.loads(cand_p.read_bytes().decode())
    old_sem = cand["semantic_review"]
    cand["semantic_review"] = {"path": new_rel, "sha256": old_sem["sha256"], "byte_count": old_sem["byte_count"]}
    base_c = {k: cand[k] for k in ("schema_version","issue_id","publication_profile","status","reader_manuscript","source","pdf","quality_bundle","semantic_review","visual_review")}
    cand["candidate_sha256"] = core_new.sha256_object(base_c)
    cand_p.write_bytes(core_new.json_bytes(cand))
    # update seal publication-candidate role to fresh candidate file (fresh SHA), fresh set_sha; seal semantic-review stays old
    seal_p = dst_c / SET_REL
    seal = json.loads(seal_p.read_bytes().decode())
    cand_bytes = cand_p.read_bytes()
    seal["roles"]["publication-candidate"] = {"path": cand_rel, "sha256": core_new.sha256_bytes(cand_bytes), "byte_count": len(cand_bytes)}
    base_s = {k: v for k, v in seal.items() if k != "set_sha256"}
    seal["set_sha256"] = core_new.sha256_object(base_s)
    seal_p.write_bytes(core_new.json_bytes(seal))
    # validate L new (must refuse)
    tmp_c = R6_BASE / "tmp" / "cand-only-L"
    tmp_c.mkdir(parents=True, exist_ok=True)
    code_c = f"""
import sys; sys.path.insert(0, r'{NEW_SRC}')
from pathlib import Path
from scripts import survey_publication_set_v2 as low
repo=Path(r'{dst_c}')
try:
    low.validate_seal(repo, r'{SET_REL}')
    print("L_UNEXPECTED_PASS")
except Exception as e:
    print(f"L_REFUSED {{type(e).__name__}}: {{str(e)[:1500]}}")
"""
    rc = run_child(NEW_SRC, dst_c, code_c, tmp_c)
    log(f"cand-only NEW: {rc['stdout'][:1500]}")
    (NOTES_R6 / "r6-cand-only-L-new-stdout.txt").write_text(rc["stdout"])
    (NOTES_R6 / "r6-cand-only-L-new-stderr.txt").write_text(rc["stderr"])
    (NOTES_R6 / "r6-cand-only-L-new-exit.txt").write_text(str(rc["exit"]))
    # no-write: State unchanged
    st_c = dst_c / STATE_REL
    # State was copied from INERT, should be unchanged by validation (read-only)
    # verify file still exists and validation refused for path reason
    assert "REFUSED" in rc["stdout"] and "UNEXPECTED_PASS" not in rc["stdout"], f"cand-only must refuse {rc['stdout'][:1000]}"
    assert any(k in rc["stdout"].lower() for k in ["candidate", "path", "semantic"]), "cand-only refusal should mention candidate/path"
    results.append(("cand-only-L", "PASS"))

    # target-rebind: review internal manuscript to new same-byte path, fresh digests
    log("=== R6-TARGET-REBIND L (review manuscript new path, fresh digests) ===")
    dst_t = R6_BASE / "r6-target-rebind"
    if dst_t.exists():
        import shutil as _sh2
        _sh2.rmtree(dst_t)
    cp_fixture(INERT_W, dst_t, "r6-target-rebind")
    # copy manuscript to new path same bytes
    man_rel = f"{PUBDIR}/reader-manuscript-v2.json"
    man_p = dst_t / man_rel
    man_new_rel = f"{PUBDIR}/reader-manuscript-forged.json"
    man_new_p = dst_t / man_new_rel
    man_new_p.write_bytes(man_p.read_bytes())
    assert sha_file(man_new_p) == sha_file(man_p)
    # update semantic review internal reader_manuscript to new path (same SHA), fresh review_sha
    sem_p = dst_t / SEM_REL
    rev = json.loads(sem_p.read_bytes().decode())
    old_rm = rev["reader_manuscript"]
    rev["reader_manuscript"] = {"path": man_new_rel, "sha256": old_rm["sha256"]}
    base_r = {k: rev[k] for k in ("schema_version","issue_id","research_profile","publication_profile","review_kind","status","production_profile","reader_manuscript","source","pdf","page_count","checks","reviewed_by","recorded_at")}
    rev["review_sha256"] = core_new.sha256_object(base_r)
    sem_p.write_bytes(core_new.json_bytes(rev))
    # update candidate semantic_review SHA to fresh review file (path same, SHA fresh), fresh candidate_sha
    cand_p2 = dst_t / cand_rel
    cand2 = json.loads(cand_p2.read_bytes().decode())
    rev_bytes = sem_p.read_bytes()
    cand2["semantic_review"] = {"path": SEM_REL, "sha256": core_new.sha256_bytes(rev_bytes), "byte_count": len(rev_bytes)}
    base_c2 = {k: cand2[k] for k in ("schema_version","issue_id","publication_profile","status","reader_manuscript","source","pdf","quality_bundle","semantic_review","visual_review")}
    cand2["candidate_sha256"] = core_new.sha256_object(base_c2)
    cand_p2.write_bytes(core_new.json_bytes(cand2))
    # update seal semantic-review + candidate roles to fresh, fresh set_sha; seal reader-manuscript stays old
    seal_p2 = dst_t / SET_REL
    seal2 = json.loads(seal_p2.read_bytes().decode())
    seal2["roles"]["semantic-review"] = {"path": SEM_REL, "sha256": core_new.sha256_bytes(rev_bytes), "byte_count": len(rev_bytes)}
    cand2_bytes = cand_p2.read_bytes()
    seal2["roles"]["publication-candidate"] = {"path": cand_rel, "sha256": core_new.sha256_bytes(cand2_bytes), "byte_count": len(cand2_bytes)}
    base_s2 = {k: v for k, v in seal2.items() if k != "set_sha256"}
    seal2["set_sha256"] = core_new.sha256_object(base_s2)
    seal_p2.write_bytes(core_new.json_bytes(seal2))
    tmp_t = R6_BASE / "tmp" / "target-rebind-L"
    tmp_t.mkdir(parents=True, exist_ok=True)
    code_t = f"""
import sys; sys.path.insert(0, r'{NEW_SRC}')
from pathlib import Path
from scripts import survey_publication_set_v2 as low
repo=Path(r'{dst_t}')
try:
    low.validate_seal(repo, r'{SET_REL}')
    print("L_UNEXPECTED_PASS")
except Exception as e:
    print(f"L_REFUSED {{type(e).__name__}}: {{str(e)[:1500]}}")
"""
    rt = run_child(NEW_SRC, dst_t, code_t, tmp_t)
    log(f"target-rebind NEW: {rt['stdout'][:1500]}")
    (NOTES_R6 / "r6-target-rebind-L-new-stdout.txt").write_text(rt["stdout"])
    (NOTES_R6 / "r6-target-rebind-L-new-stderr.txt").write_text(rt["stderr"])
    (NOTES_R6 / "r6-target-rebind-L-new-exit.txt").write_text(str(rt["exit"]))
    assert "REFUSED" in rt["stdout"] and "UNEXPECTED_PASS" not in rt["stdout"], f"target-rebind must refuse {rt['stdout'][:1000]}"
    assert any(k in rt["stdout"].lower() for k in ["manuscript", "path", "bind"]), "target refusal should mention manuscript/path"
    results.append(("target-rebind-L", "PASS"))

    # external-consistent: review outside publication, Candidate+seal consistent, targets unchanged -> PASS
    log("=== R6-EXTERNAL-CONSISTENT L (outside pub, consistent) ===")
    dst_e = R6_BASE / "r6-external-consistent"
    if dst_e.exists():
        import shutil as _sh3
        _sh3.rmtree(dst_e)
    cp_fixture(INERT_W, dst_e, "r6-external-consistent")
    ext_rel = f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP}/external-reviews/semantic-review-v2.json"
    ext_p = dst_e / ext_rel
    ext_p.parent.mkdir(parents=True, exist_ok=True)
    ext_p.write_bytes((dst_e / SEM_REL).read_bytes())
    # update Candidate to external (same SHA, reviewed targets unchanged), fresh candidate_sha
    cand_pe = dst_e / cand_rel
    cande = json.loads(cand_pe.read_bytes().decode())
    old_se = cande["semantic_review"]
    cande["semantic_review"] = {"path": ext_rel, "sha256": old_se["sha256"], "byte_count": old_se["byte_count"]}
    base_ce = {k: cande[k] for k in ("schema_version","issue_id","publication_profile","status","reader_manuscript","source","pdf","quality_bundle","semantic_review","visual_review")}
    cande["candidate_sha256"] = core_new.sha256_object(base_ce)
    cand_pe.write_bytes(core_new.json_bytes(cande))
    # update seal to external consistently, fresh set_sha
    seal_pe = dst_e / SET_REL
    seale = json.loads(seal_pe.read_bytes().decode())
    seale["roles"]["semantic-review"] = {"path": ext_rel, "sha256": old_se["sha256"], "byte_count": old_se["byte_count"]}
    cande_bytes = cand_pe.read_bytes()
    seale["roles"]["publication-candidate"] = {"path": cand_rel, "sha256": core_new.sha256_bytes(cande_bytes), "byte_count": len(cande_bytes)}
    base_se = {k: v for k, v in seale.items() if k != "set_sha256"}
    seale["set_sha256"] = core_new.sha256_object(base_se)
    seal_pe.write_bytes(core_new.json_bytes(seale))
    tmp_e = R6_BASE / "tmp" / "external-L"
    tmp_e.mkdir(parents=True, exist_ok=True)
    code_e = f"""
import sys; sys.path.insert(0, r'{NEW_SRC}')
from pathlib import Path
from scripts import survey_publication_set_v2 as low
repo=Path(r'{dst_e}')
try:
    s=low.validate_seal(repo, r'{SET_REL}')
    print(f"L_PASS {{s.get('issue_id')}}")
except Exception as e:
    print(f"L_REFUSED {{type(e).__name__}}: {{str(e)[:1500]}}")
"""
    re_ = run_child(NEW_SRC, dst_e, code_e, tmp_e)
    log(f"external-consistent NEW: {re_['stdout'][:1500]}")
    (NOTES_R6 / "r6-external-consistent-L-new-stdout.txt").write_text(re_["stdout"])
    (NOTES_R6 / "r6-external-consistent-L-new-stderr.txt").write_text(re_["stderr"])
    (NOTES_R6 / "r6-external-consistent-L-new-exit.txt").write_text(str(re_["exit"]))
    assert "L_PASS" in re_["stdout"], f"external consistent must PASS L {re_['stdout'][:1000]} {re_['stderr'][:500]}"
    results.append(("external-consistent-L", "PASS"))

    log(f"TOTAL R6 L focused pass={len(results)}")
    (NOTES_R6 / "r6-L-focused-summary.json").write_text(json.dumps([{"name": n, "status": s} for n, s in results], indent=2))
    print("EXIT:0")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        import traceback
        traceback.print_exc()
        print("EXIT:2")
        sys.exit(2)
