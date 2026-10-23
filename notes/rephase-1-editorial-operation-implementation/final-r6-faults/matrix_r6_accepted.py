#!/usr/bin/env python3
"""R6 TRUE accepted/authored boundary on INERT (P2R KEEP unchanged, fresh receipt digest)."""
from __future__ import annotations
import json, os, sys, time, traceback, shutil
from pathlib import Path
sys.dont_write_bytecode=True; os.environ["PYTHONDONTWRITEBYTECODE"]="1"
for _v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE","GIT_OBJECT_DIRECTORY","GIT_ALTERNATE_OBJECT_DIRECTORIES","GIT_COMMON_DIR","GIT_PREFIX"):
    if os.environ.get(_v): print(f"UNSAFE {_v}"); sys.exit(2)
def log(m): print(m, flush=True)
REPO=Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey").resolve()
sys.path.insert(0, str(REPO/"notes/rephase-1-editorial-operation-implementation/final-r6-faults"))
from matrix_common import FAULT_BASE, INERT_W, cp_fixture, verify_fixture, run_subprocess, sha_file
ISSUE_W="2026-W37"
NOTES=REPO/"notes/rephase-1-editorial-operation-implementation/final-r6-faults"
PASS=0; FAIL=0; CASES=[]
def case(n,fn):
    global PASS, FAIL
    t0=time.monotonic()
    try: fn(); dt=time.monotonic()-t0; log(f"CASE PASS {n} dt={dt:.1f}s"); CASES.append((n,"PASS",dt,"")); PASS+=1
    except AssertionError as e: dt=time.monotonic()-t0; log(f"CASE FAIL {n} dt={dt:.1f}s {e}"); traceback.print_exc(); CASES.append((n,"FAIL",dt,str(e)[:2000])); FAIL+=1
    except Exception as e: dt=time.monotonic()-t0; log(f"CASE BLOCKER {n} dt={dt:.1f}s {type(e).__name__}: {e}"); traceback.print_exc(); CASES.append((n,"BLOCKER",dt,f"{type(e).__name__}: {e}"[:2000])); FAIL+=1
def child_api(fixture: Path, code: str, timeout=180):
    return run_subprocess(fixture, [sys.executable,"-B","-c",code], cwd=fixture, timeout=timeout)
def new_fault(base: Path, name: str):
    dst=FAULT_BASE/name
    if dst.exists(): verify_fixture(dst, name+"(reuse)"); return dst
    cp_fixture(base, dst, name); return dst

def r6_accepted_profile():
    # TRUE current accepted-ref: copy same-byte Profile to alt repo path outside publication,
    # change ONLY receipt.accepted_refs row.path + fresh receipt_sha; call PUBLIC validate_editorial_receipt directly while State1 healthy.
    # P2R original KEEP refs unchanged so avoids earlier retention drift. Expect ACCEPTED_MISMATCH/path-current binding, not stale State.
    dst=new_fault(INERT_W, "r6-accepted-profile")
    import json as _j
    rec_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-2/publication/validated-source-manifest.json"
    rec=_j.loads((dst/rec_rel).read_bytes().decode())
    # find Profile accepted ref (production Profile? Or research_profile? Look for Profile)
    # receipt has accepted_refs? Check shape: accepted_refs vs authored_refs?
    # For R6, receipt has accepted_refs including Profile? Let's inspect via child.
    code_inspect=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import json
rec=json.loads((Path(r'{dst}')/r'{rec_rel}').read_bytes().decode())
print(list(rec.keys()))
print("accepted:", rec.get('accepted_refs', [])[:2])
print("authored:", rec.get('authored_refs', [])[:2])
"""
    r_ins=child_api(dst, code_inspect); log(f"receipt keys: {r_ins['stdout'][:1500]}")
    # Choose Profile file: production-profile.json (outside publication, repo-contained)
    prof_rel=f"sources/{ISSUE_W}/production-profile.json"
    assert (dst/prof_rel).is_file(), f"profile missing {prof_rel}"
    alt_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-2/external-reviews/profile-copy.json"
    (dst/alt_rel).parent.mkdir(parents=True, exist_ok=True)
    if not (dst/alt_rel).exists():
        shutil.copy(str(dst/prof_rel), str(dst/alt_rel))
    assert sha_file(dst/prof_rel)==sha_file(dst/alt_rel)
    # update ONLY receipt.accepted_refs row.path for Profile + fresh receipt_sha
    code_up=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import json
from scripts import survey_production_v2 as core
p=Path(r'{dst}')/r'{rec_rel}'
rec=json.loads(p.read_bytes().decode())
# find accepted ref with path == profile
found=False
for a in rec.get('accepted_refs',[]):
    if a.get('path')==r'{prof_rel}':
        a['path']=r'{alt_rel}'
        found=True
        break
assert found, "profile accepted ref not found"
tmp=dict(rec); tmp.pop('receipt_sha256', None)
rec['receipt_sha256']=core.sha256_object(tmp)
p.write_bytes(core.json_bytes(rec))
print("forged accepted profile alt path fresh receipt")
"""
    r_up=child_api(dst, code_up); assert r_up["exit"]==0, f"forgery update failed {r_up['stdout'][:1500]} {r_up['stderr'][:800]}"
    state_rel=f"sources/{ISSUE_W}/production-state.json"
    code_v=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
from scripts import survey_editorial_publication_v2 as m
try:
    m.validate_editorial_receipt(Path(r'{dst}'), r'{rec_rel}', r'{state_rel}')
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    out=str(e); print(f"REFUSED: {{out[:2500]}}")
    low=out.lower()
    assert "accepted" in low and ("mismatch" in low or "path" in low or "current" in low or "binding" in low), f"must be ACCEPTED_MISMATCH/path-current, got {{out[:1500]}}"
    assert "stale" not in low or "accepted" in low, f"must not be stale State preemption {{out[:1200]}}"
    sys.exit(0)
"""
    r=child_api(dst, code_v); assert r["exit"]==0, f"accepted-profile must refuse ACCEPTED_MISMATCH {r['stdout'][:2500]}"
    log("R6 accepted-profile alt path REFUSED current binding OK")

def r6_authored_before():
    # Old-authoring/new-reader similar: receipt authored ref path to before authoring + fresh digest must AUTHORED_MISMATCH
    dst=new_fault(INERT_W, "r6-authored-before")
    import json as _j
    rec_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-2/publication/validated-source-manifest.json"
    # authored ref: proposed-publication-authoring? Find authored_refs
    code_ins=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import json
rec=json.loads((Path(r'{dst}')/r'{rec_rel}').read_bytes().decode())
print("authored:", rec.get('authored_refs', []))
"""
    r_ins=child_api(dst, code_ins); log(f"authored refs: {r_ins['stdout'][:1500]}")
    # Use before authoring: wk-r6-1 authoring-input.json (old) vs wk-r6-2 proposal's new authoring? Actually receipt authored_refs should point to wk-r6-2 authoring. Change to wk-r6-1 authoring path (old) with fresh digest? But old file has different bytes (different SHA), so need to update SHA to old file's SHA (fresh). Then receipt will claim old authoring, but proposal expects new? Should refuse AUTHORED_MISMATCH (not rederive? Actually distinct from actual rederive already covered in A_deep_reader).
    # Find wk-r6-1 authoring
    old_auth_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-1/authoring-input.json"
    assert (dst/old_auth_rel).is_file(), "old authoring missing"
    code_up=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import json
from scripts import survey_production_v2 as core
p=Path(r'{dst}')/r'{rec_rel}'
rec=json.loads(p.read_bytes().decode())
# find authored ref for proposed-publication-authoring (path contains wk-r6-2/authoring)
found=False
for a in rec.get('authored_refs',[]):
    if 'wk-r6-2/authoring' in a.get('path',''):
        import hashlib
        old_p=Path(r'{dst}')/r'{old_auth_rel}'
        a['path']=r'{old_auth_rel}'
        a['sha256']=hashlib.sha256(old_p.read_bytes()).hexdigest()
        if 'byte_count' in a: a['byte_count']=old_p.stat().st_size
        found=True
        break
assert found, "authored wk-r6-2 not found"
tmp=dict(rec); tmp.pop('receipt_sha256', None)
rec['receipt_sha256']=core.sha256_object(tmp)
p.write_bytes(core.json_bytes(rec))
print("forged authored before fresh")
"""
    r_up=child_api(dst, code_up); assert r_up["exit"]==0, f"authored forgery failed {r_up['stdout'][:1500]}"
    state_rel=f"sources/{ISSUE_W}/production-state.json"
    code_v=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
from scripts import survey_editorial_publication_v2 as m
try:
    m.validate_editorial_receipt(Path(r'{dst}'), r'{rec_rel}', r'{state_rel}')
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    out=str(e); print(f"REFUSED: {{out[:2500]}}")
    low=out.lower()
    assert "authored" in low and ("mismatch" in low or "path" in low or "current" in low or "binding" in low), f"must be AUTHORED_MISMATCH {{out[:1500]}}"
    sys.exit(0)
"""
    r=child_api(dst, code_v); assert r["exit"]==0, f"authored-before must refuse {r['stdout'][:2500]}"
    log("R6 authored-before REFUSED OK (distinct from rederive scope)")

def main():
    for n,f in [("R6_accepted_profile",r6_accepted_profile),("R6_authored_before",r6_authored_before)]:
        case(n,f)
    log(f"TOTAL accepted pass={PASS} fail={FAIL}")
    for n,s,d,det in CASES: log(f"SUMMARY {s} {n} dt={d:.1f}s {det[:200]}")
    (NOTES/"summary_r6_accepted.json").write_text(json.dumps({"pass":PASS,"fail":FAIL,"cases":[{"name":n,"status":s} for n,s,_,_ in CASES]}, indent=2))
    print(f"EXIT:{0 if FAIL==0 else 2}"); return 0 if FAIL==0 else 2
if __name__=="__main__":
    try: rc=main()
    except Exception: traceback.print_exc(); print("EXIT:2"); rc=2
    import sys as _s; _s.exit(rc)
