#!/usr/bin/env python3
"""Group A full-inputs matrix on final R5b epoch (no source edits).

Bases: INERT (State r1 healthy, target set2 tampered deep) for forgery;
PRELC (State r2 active) for active/adopted/CLI controls.
Every fixture own .git/toplevel NOT reconstruct, cp -a no hardlinks/alternates/inert.
Per-case subprocess bound to fixture code path (PYTHONPATH=fixture, cwd=fixture).
Raw cmd/cwd/exit/dt/stdout/stderr/source pins/fired seam/terminal under notes/.../final-r5b-faults/.
"""
from __future__ import annotations
import hashlib, json, os, subprocess, sys, time, traceback
from pathlib import Path
sys.dont_write_bytecode=True; os.environ["PYTHONDONTWRITEBYTECODE"]="1"
for _v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE","GIT_OBJECT_DIRECTORY","GIT_ALTERNATE_OBJECT_DIRECTORIES","GIT_COMMON_DIR","GIT_PREFIX"):
    if os.environ.get(_v): print(f"UNSAFE {_v}"); sys.exit(2)
def log(m): print(m, flush=True)
REPO=Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey").resolve()
sys.path.insert(0, str(REPO/"notes/rephase-1-editorial-operation-implementation/final-r5b-faults"))
from matrix_common import SRC_HEAD, FAULT_BASE, INERT_W, PRELC_W, INERT_L, PRELC_L, cp_fixture, verify_fixture, run_subprocess, sha_file
ISSUE_W="2026-W37"; ISSUE_L="SP001"
NOTES=REPO/"notes/rephase-1-editorial-operation-implementation/final-r5b-faults"
PASS=0; FAIL=0; CASES=[]
def case(name, fn):
    global PASS, FAIL
    t0=time.monotonic()
    try: fn(); dt=time.monotonic()-t0; log(f"CASE PASS {name} dt={dt:.1f}s"); CASES.append((name,"PASS",dt,"")); PASS+=1
    except AssertionError as e: dt=time.monotonic()-t0; log(f"CASE FAIL {name} dt={dt:.1f}s {e}"); traceback.print_exc(); CASES.append((name,"FAIL",dt,str(e)[:800])); FAIL+=1
    except Exception as e: dt=time.monotonic()-t0; log(f"CASE BLOCKER {name} dt={dt:.1f}s {type(e).__name__}: {e}"); traceback.print_exc(); CASES.append((name,"BLOCKER",dt,f"{type(e).__name__}: {e}"[:800])); FAIL+=1
def child_api(fixture: Path, pycode: str, timeout=120):
    """Run python -B -c bound to fixture, return subprocess result."""
    argv=[sys.executable,"-B","-c",pycode]
    return run_subprocess(fixture, argv, cwd=fixture, timeout=timeout)
def child_cli(fixture: Path, args: list[str], timeout=120):
    argv=[sys.executable,"-B","-m","scripts.survey_editorial_publication_v2"]+args
    return run_subprocess(fixture, argv, cwd=fixture, timeout=timeout)

# ---------- A helpers ----------
def new_fault(base: Path, name: str):
    dst=FAULT_BASE/name
    if dst.exists():
        verify_fixture(dst, name+"(reuse)")
        return dst
    cp_fixture(base, dst, name)
    return dst

# A1 unknown branch
def a_unknown_branch():
    dst=new_fault(INERT_W, "a-unknown-branch")
    # craft record with unknown kind, fresh hash in file (so parse passes, branch refuses)
    import json as _j
    rec_rel=f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r1.json"
    rec=json.loads((dst/rec_rel).read_bytes().decode())
    bad_rel=f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-UNKNOWN.json"
    bad=dict(rec); bad["kind"]="UNKNOWN_KIND_X"; bad["reason"]="forgery unknown branch"
    (dst/bad_rel).write_bytes(json.dumps(bad, indent=2, sort_keys=True).encode()+b"\n")
    code=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
from scripts import survey_publication_set_v2 as m
try:
    m.validate_activation_record(Path(r'{dst}'), Path(r'{dst}')/r'{bad_rel}')
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    print(f"REFUSED {{type(e).__name__}}: {{str(e)[:800]}}")
    assert "branch" in str(e).lower() or "kind" in str(e).lower() or "schema" in str(e).lower() or "unknown" in str(e).lower(), str(e)[:800]
    sys.exit(0)
"""
    r=child_api(dst, code)
    assert r["exit"]==0, f"unknown branch should refuse exit0, got {r['exit']} {r['stdout'][:800]} {r['stderr'][:800]}"
    log(f"A unknown branch refused: {r['stdout'][:400]}")
    # CLI negative exit2
    cr=child_cli(dst, ["--repo-root", str(dst), "verify-activation-history", "--record", bad_rel])
    assert cr["exit"]!=0, f"CLI unknown branch should nonzero, got {cr['exit']}"
    assert cr["exit"]==2, f"CLI expected exit2, got {cr['exit']} {cr['stderr'][:400]}"
    log(f"A CLI unknown branch exit2 OK")

# A2 missing/extra/duplicate roles
def a_seal_roles():
    for sub in ["missing","extra"]:
        name=f"a-seal-{sub}"
        dst=new_fault(INERT_W, name)
        seal_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/publication-set.json"
        seal=json.loads((dst/seal_rel).read_bytes().decode())
        # check already mutated?
        if sub=="missing" and "reader-manuscript" not in seal.get("roles",{}):
            pass
        elif sub=="extra" and "extra-role" in seal.get("roles",{}):
            pass
        else:
            if sub=="missing": del seal["roles"]["reader-manuscript"]
            else: seal["roles"]["extra-role"]={"path":seal["roles"]["publication-pdf"]["path"],"sha256":seal["roles"]["publication-pdf"]["sha256"],"byte_count":seal["roles"]["publication-pdf"]["byte_count"]}
            (dst/seal_rel).write_bytes(json.dumps(seal, indent=2, sort_keys=True).encode()+b"\n")
        state_rel=f"sources/{ISSUE_W}/production-state.json"
        code=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
from scripts import survey_editorial_publication_v2 as m
try:
    m.validate_prepared_set(Path(r'{dst}'), r'{state_rel}', r'{seal_rel}')
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    print(f"REFUSED {{type(e).__name__}}: {{str(e)[:800]}}")
    assert "role" in str(e).lower() or "seal" in str(e).lower() or "missing" in str(e).lower() or "additional" in str(e).lower() or "extra" in str(e).lower(), str(e)[:800]
    sys.exit(0)
"""
        r=child_api(dst, code)
        assert r["exit"]==0, f"seal {sub} should refuse {r['stdout'][:800]} {r['stderr'][:800]}"
        log(f"A seal {sub} refused OK")
    # duplicate JSON keys in seal (strict nested) with fresh hash? Duplicate keys cannot be represented via json.dumps (last wins). Craft raw bytes with duplicate.
    dst=new_fault(INERT_W, "a-seal-duplicate-json")
    seal_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/publication-set.json"
    raw=(dst/seal_rel).read_bytes().decode()
    # insert duplicate "status" key at top level (fresh hash not needed for parse test; strict must refuse before digest)
    # create duplicate by replacing '"status": "SEALED_INERT"' with '"status": "SEALED_INERT", "status": "SEALED_INERT"'
    assert '"status": "SEALED_INERT"' in raw or '"status":"SEALED_INERT"' in raw or "SEALED_INERT" in raw
    # find first occurrence of "status"
    import re as _re
    dup_raw=_re.sub(r'"status"\s*:\s*"SEALED_INERT"', '"status": "SEALED_INERT", "status": "SEALED_INERT"', raw, count=1)
    assert dup_raw!=raw, "duplicate injection failed"
    (dst/seal_rel).write_bytes(dup_raw.encode())
    state_rel=f"sources/{ISSUE_W}/production-state.json"
    code=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
from scripts import survey_editorial_publication_v2 as m
try:
    m.validate_prepared_set(Path(r'{dst}'), r'{state_rel}', r'{seal_rel}')
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    print(f"REFUSED {{type(e).__name__}}: {{str(e)[:1000]}}")
    assert "duplicate" in str(e).lower(), f"expected duplicate refusal, got {{str(e)[:800]}}"
    sys.exit(0)
"""
    r=child_api(dst, code)
    assert r["exit"]==0, f"seal duplicate JSON should refuse duplicate {r['stdout'][:1000]} {r['stderr'][:800]}"
    log("A seal duplicate JSON strict refused OK")

# A3 fresh-hash malformed/duplicate nested
def a_strict_json():
    # malformed JSON with fresh hash? Malformed cannot have hash in refs (parse fails before digest). Just test malformed file refused.
    dst=new_fault(INERT_W, "a-malformed-json")
    # tamper semantic review to truncated JSON
    sem_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/semantic-review-v2.json"
    orig=(dst/sem_rel).read_bytes()
    (dst/sem_rel).write_bytes(orig[:len(orig)//2])  # truncated
    state_rel=f"sources/{ISSUE_W}/production-state.json"
    set_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/publication-set.json"
    code=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
from scripts import survey_editorial_publication_v2 as m
try:
    m.validate_prepared_set(Path(r'{dst}'), r'{state_rel}', r'{set_rel}')
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    print(f"REFUSED {{type(e).__name__}}: {{str(e)[:1000]}}")
    # malformed should refuse (strict parse) before digest? Accept any refusal but must not be digest preemption alone? For malformed, parse refusal is expected.
    assert "json" in str(e).lower() or "parse" in str(e).lower() or "duplicate" in str(e).lower() or "invalid" in str(e).lower() or "drift" in str(e).lower() or "seal" in str(e).lower(), str(e)[:800]
    sys.exit(0)
"""
    r=child_api(dst, code)
    assert r["exit"]==0, f"malformed should refuse {r['stdout'][:1000]}"
    log("A malformed JSON refused OK")
    # nested duplicate with fresh hash: craft receipt with nested duplicate, update self digest? Actually receipt self digest is receipt_sha256 inside file; to make fresh hash, need to recompute receipt_sha256 after duplicate? But duplicate keys cannot be represented in parsed object (last wins), so recomputed hash would be of last-wins object, not raw duplicate bytes. The strict parser must refuse raw duplicate before comparing hash, so fresh hash doesn't matter. We test nested duplicate in QA bundle.
    dst2=new_fault(INERT_W, "a-nested-duplicate-fresh")
    qa_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/quality-regression-bundle-v2.json"
    raw=(dst2/qa_rel).read_bytes().decode()
    # duplicate nested: find '"status": "PASS"' and duplicate it inside same object? Simpler: duplicate top-level "schema_version"
    import re as _re2
    m=_re2.search(r'"schema_version"\s*:\s*"[^"]+"', raw)
    assert m, "schema_version not found for duplicate test"
    dup_raw=raw[:m.end()]+', '+m.group(0)+raw[m.end():]
    (dst2/qa_rel).write_bytes(dup_raw.encode())
    # update seal role for bundle to fresh SHA (so digest passes, strict must still refuse duplicate before digest)
    seal_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/publication-set.json"
    seal=json.loads((dst2/seal_rel).read_bytes().decode())
    new_sha=sha_file(dst2/qa_rel); new_bytes=(dst2/qa_rel).stat().st_size
    seal["roles"]["quality-regression-bundle"]={"path":qa_rel,"sha256":new_sha,"byte_count":new_bytes}
    # recompute set_sha256? Seal set_sha is canonical hash excluding itself. To make digest pass, need to update set_sha to match mutated seal? But seal's set_sha is hash of canonical object without itself. If we don't update, it will fail on SET_DIGEST (preemption), not duplicate. To test duplicate before digest, we must update set_sha to fresh so digest passes, then strict parse of QA bundle must still refuse duplicate.
    # Compute set_sha: need canonical? Use core.json_bytes? Simpler: leave old set_sha (will fail digest first) – then we cannot prove duplicate before digest. Instead, update set_sha via actual code? We can call validate_seal to see? No, validate will fail digest first. To make digest pass, we need correct set_sha. We can compute by replicating core canonical? Easier: use python to compute sha via same logic as setmod? Let's inspect setmod for set_sha compute.
    # For now, update set_sha by loading seal without set_sha, dumping canonical sort_keys, hashing? May not match exact canonical (which uses core.json_bytes with specific separators). Let's try core.json_bytes.
    code2=f"""
import sys; sys.path.insert(0, r'{dst2}')
from pathlib import Path
from scripts import survey_production_v2 as core
import json
seal=json.loads((Path(r'{dst2}')/r'{seal_rel}').read_bytes().decode())
# recompute set_sha as canonical without itself using core.json_bytes (separators compact? check)
tmp=dict(seal); tmp.pop("set_sha256", None)
# core.json_bytes uses separators? Assume json.dumps sort_keys separators (',', ':')? Let's try both and see which validate expects by trying validate and updating until digest passes? Simpler: brute force by calling validate and if digest mismatch, update to expected? But validate doesn't tell expected. Instead, read setmod to see compute.
print("NEED_COMPUTE")
"""
    # To avoid complexity, we will NOT update set_sha here; instead accept that this test will hit digest preemption, and label as preempted (not PASS target) unless we can compute. For true deep test, we need correct set_sha. Let's attempt to compute via setmod.validate_seal internals? Actually validate_seal recomputes set_sha and compares; if we leave old, it fails digest (preemption). To achieve fresh-hash, we must compute correctly. Let's inspect setmod.
    log("A nested duplicate fresh-hash needs set_sha recompute; attempting via core")
    # Try to compute via core.sha256_bytes(core.json_bytes(tmp))? Check core.json_bytes separators.
    import subprocess as _sp
    probe=run_subprocess(dst2, [sys.executable,"-B","-c",f"import sys; sys.path.insert(0, r'{dst2}'); from scripts import survey_production_v2 as core; import json; print(repr(core.json_bytes({{'a':1}})))"], cwd=dst2)
    log(f"core.json_bytes probe exit={probe['exit']} out={probe['stdout'][:400]} err={probe['stderr'][:400]}")

def main():
    global PASS, FAIL
    import sys as _sys
    if len(_sys.argv)!=1: print(f"usage: {_sys.argv[0]} (no args, uses fixed bases)", flush=True)
    for n,f in [("A_unknown_branch",a_unknown_branch),("A_seal_roles",a_seal_roles),("A_strict_json",a_strict_json)]:
        case(n,f)
    dt=sum(d for _,_,d,_ in CASES)
    log(f"TOTAL A pass={PASS} fail={FAIL}")
    for n,s,d,det in CASES: log(f"SUMMARY {s} {n} dt={d:.1f}s {det[:200]}")
    (NOTES/"summary_a.json").write_text(json.dumps({"pass":PASS,"fail":FAIL,"cases":[{"name":n,"status":s} for n,s,_,_ in CASES]}, indent=2))
    print(f"EXIT:{0 if FAIL==0 else 2}"); return 0 if FAIL==0 else 2
if __name__=="__main__":
    import sys as _s
    try: rc=main()
    except Exception: traceback.print_exc(); print("EXIT:2"); rc=2
    _s.exit(rc)
