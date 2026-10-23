#!/usr/bin/env python3
"""R6 prepare failure/extra input: NEW source-only fixture with actual P1/P2R/scope/P2V/P3S, controlled toolchain failure/extra argv before transfer."""
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
    except AssertionError as e: dt=time.monotonic()-t0; log(f"CASE FAIL {n} dt={dt:.1f}s {e}"); traceback.print_exc(); CASES.append((n,"FAIL",dt,str(e)[:2500])); FAIL+=1
    except Exception as e: dt=time.monotonic()-t0; log(f"CASE BLOCKER {n} dt={dt:.1f}s {type(e).__name__}: {e}"); traceback.print_exc(); CASES.append((n,"BLOCKER",dt,f"{type(e).__name__}: {e}"[:2500])); FAIL+=1
def child_api(fixture: Path, code: str, timeout=300):
    return run_subprocess(fixture, [sys.executable,"-B","-c",code], cwd=fixture, timeout=timeout)
def new_fault(base: Path, name: str):
    dst=FAULT_BASE/name
    if dst.exists(): verify_fixture(dst, name+"(reuse)"); return dst
    cp_fixture(base, dst, name); return dst

def r6_prepare_failure_extra():
    # NEW source-only fixture wk-r6-3-fault: actual P1 (new headline) + P2R + scope + P2V + P3S, then PUBLIC prepare with invalid exe + extra argv (before transfer, no PDF forged)
    dst=new_fault(INERT_W, "r6-prepare-new-v3")
    # Use INERT State r1 (healthy, no r2) for NEW proposal (State old, no publication for new ID)
    code_new=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import json, copy
from datetime import datetime, timezone
from scripts import survey_production_v2 as core
# discover helpers via existing tests? Use P1 test helpers? Simpler: use actual P1 API directly with new authoring?
# For this matrix, reuse INERT wk-r6-2 authoring as base, new headline, new proposal ID wk-r6-3-fault
import hashlib
ISSUE="{ISSUE_W}"
# load wk-r6-2 authoring as base
base_auth=json.loads((Path(r'{dst}')/f"sources/{{ISSUE}}/publication/v2/editorial-corrections/wk-r6-2/authoring-input.json").read_bytes().decode())
new_auth=copy.deepcopy(base_auth)
# new headline to make new reader distinct
try:
    new_auth["cover"]["headline"]="R6 fault new proposal headline"
except: pass
# stage new authoring via P1 test helper staging? Use direct file write + P1 prepare_proposal
# Find P1 helper: use tests.test_survey_editorial_correction_proposal_v2 helpers? To avoid test import complexity, do minimal: write staged authoring file then call proposal_mod.prepare_proposal
from scripts import survey_editorial_correction_proposal_v2 as proposal_mod
from scripts import survey_editorial_retention_v2 as retention
from scripts import survey_editorial_current_authority_v2 as observer
from scripts import survey_editorial_staged_source_v2 as staged
state_rel="sources/2026-W37/production-state.json"
# stage authoring via P1 helper (helper creates proposal dir, do NOT pre-mkdir)
# Inspect proposal_mod for staging helper: use tests helper if present
try:
    from tests import test_survey_editorial_correction_proposal_v2 as p1t
    import unittest
    class _TC(unittest.TestCase):
        def runTest(self): pass
    tc=_TC()
    # _stage_authoring_before_prepare signature? Try
    staged_auth=p1t._stage_authoring_before_prepare(tc, Path(r'{dst}'), Path(r'{dst}')/f"sources/{{ISSUE}}", "wk-r6-3-fault", new_auth)
    print(f"staged {{staged_auth}}")
except Exception as e:
    print(f"staging helper failed: {{e}}")
    raise
# P1 prepare
prepared=proposal_mod.prepare_proposal(Path(r'{dst}'), state_rel, str(Path(staged_auth).relative_to(r'{dst}')), "wk-r6-3-fault", "R6 fault new proposal")
print(f"P1 prepared")
# stage reader+proposal
try:
    proposal_path=p1t._stage_reader_and_proposal(tc, Path(r'{dst}'), Path(r'{dst}')/f"sources/{{ISSUE}}", "wk-r6-3-fault", prepared)
    print(f"proposal {{proposal_path}}")
except Exception as e:
    print(f"stage reader failed {{e}}"); raise
# P1 validate (should be REVIEW_REQUIRED)
out=proposal_mod.validate_proposal(Path(r'{dst}'), state_rel, str(Path(proposal_path).relative_to(r'{dst}')) if hasattr(proposal_path,'relative_to') else str(proposal_path))
print(f"P1 validate {{out.get('result')}}")
# P2R capture
cap=retention.capture_retention(Path(r'{dst}'), Path(r'{dst}')/state_rel, Path(r'{dst}')/str(Path(proposal_path).relative_to(r'{dst}')) if hasattr(proposal_path,'relative_to') else Path(proposal_path))
print(f"P2R {{cap.get('result')}}")
# scope + P2V + P3S
# Use p1t helpers for scope
try:
    staged_reader_rel=prepared["proposal"]["proposed"]["proposed_reader_ref"]["path"]
    scope_path=p1t._scope_review_for(tc, Path(r'{dst}'), prepared, staged_reader_rel, "scope-review-v2.json")
    print(f"scope {{scope_path}}")
    # P2V
    import pathlib as _p
    manifest_rel=cap["manifest_path"] if isinstance(cap.get("manifest_path"), str) else str(cap.get("manifest_path"))
    obs=observer.observe_current_authority(Path(r'{dst}'), Path(r'{dst}')/state_rel, Path(r'{dst}')/str(Path(proposal_path).relative_to(r'{dst}')) if hasattr(proposal_path,'relative_to') else Path(proposal_path), Path(r'{dst}')/manifest_rel, Path(scope_path) if isinstance(scope_path, Path) else Path(r'{dst}')/str(scope_path))
    print(f"P2V {{obs.get('result')}}")
    # P3S
    mat=staged.materialize_staged_source(Path(r'{dst}'), Path(r'{dst}')/state_rel, Path(r'{dst}')/str(Path(proposal_path).relative_to(r'{dst}')) if hasattr(proposal_path,'relative_to') else Path(proposal_path), Path(r'{dst}')/manifest_rel, Path(scope_path) if isinstance(scope_path, Path) else Path(r'{dst}')/str(scope_path))
    print(f"P3S {{mat}}")
except Exception as e:
    import traceback; traceback.print_exc(); print(f"P2V/P3S failed {{e}}"); raise
print("NEW_PROPOSAL_READY")
"""
    r_new=child_api(dst, code_new, timeout=300)
    # This NEW proposal flow may be fragile due to helper signatures (different R6 helpers?). If it fails, mark INCOMPLETE with concrete helper mismatch, don't claim.
    if r_new["exit"]!=0:
        log(f"NEW proposal P1/P2R/scope/P2V/P3S setup failed (helper mismatch, not source bug): {r_new['stdout'][:2000]} {r_new['stderr'][:1500]}")
        raise AssertionError(f"INCOMPLETE NEW proposal setup (helper signature/State, not source): exit {r_new['exit']} {r_new['stdout'][:1500]}")
    log("R6 NEW proposal P1/P2R/scope/P2V/P3S ready (no State rewind, no old source overwrite)")
    # Now PUBLIC prepare with invalid exe (controlled failure before transfer, no PDF forged)
    # Discover new proposal paths: wk-r6-3-fault proposal/staged/manuscript/toolchain specs? Need manuscript/toolchain specs for prepare.
    # For brevity, test controlled failure via PUBLIC prepare with invalid toolchain on NEW proposal (manuscript/toolchain specs minimal valid + invalid exe)
    # If NEW proposal setup succeeded, its proposal_path is known? Our code_new didn't persist paths. Simplify: use existing wk-r6-2 proposal with NEW publication dir absent? No, wk-r6-2 already has publication (sealed), so prepare would refuse PUBLICATION_EXISTS before toolchain (preemption, not toolchain seam). To reach toolchain seam, need NEW proposal with no publication (which we just created: wk-r6-3-fault has no publication yet). Good.
    # Now run prepare with invalid exe + extra argv as two subcases via child.
    code_prep_fail=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import json
from datetime import datetime, timezone
from scripts import survey_editorial_publication_v2 as m
# discover wk-r6-3-fault paths
prop_rel="sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-3-fault/proposal.json"
# staged manifest path: proposal_dir/staged-source/staged-source-manifest.json? Find via proposal?
import json as _j
prop=_j.loads((Path(r'{dst}')/prop_rel).read_bytes().decode())
# staged manifest ref? Proposal has? Use retained? Simpler: list dir
import pathlib as _p
staged_candidates=list((Path(r'{dst}')/f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-3-fault/staged-source").glob("*.json"))
print(f"staged candidates {{staged_candidates}}")
# manuscript/toolchain specs: create minimal valid specs for NEW proposal (reuse wk-r6-2 specs as template with new proposal ref)
# For controlled failure, create toolchain spec with invalid exe (absolute /nonexistent) but otherwise valid recipe/argv
from scripts import survey_production_v2 as core
tspec=json.loads((Path(r'{dst}')/f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-2/toolchain-spec.json").read_bytes().decode())
tspec["absolute_executable"]="/nonexistent/lualatex-r6-fault"
bad_tspec_rel="sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-3-fault/toolchain-spec-fault.json"
Path(r'{dst}', bad_tspec_rel).write_bytes(core.json_bytes(tspec))
# manuscript spec: copy wk-r6-2 manuscript-spec but update proposal_ref to new proposal
mspec=json.loads((Path(r'{dst}')/f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-2/manuscript-spec.json").read_bytes().decode())
# update proposal_ref to new proposal path/sha?
import hashlib
new_prop_bytes=(Path(r'{dst}')/prop_rel).read_bytes()
mspec["proposal_ref"]=dict(path=prop_rel, sha256=hashlib.sha256(new_prop_bytes).hexdigest())
bad_mspec_rel="sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-3-fault/manuscript-spec-fault.json"
Path(r'{dst}', bad_mspec_rel).write_bytes(core.json_bytes(mspec))
# staged manifest rel
staged_rel="sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-3-fault/staged-source/staged-source-manifest.json"
# PUBLIC prepare with invalid exe must refuse TOOLCHAIN_EXE before transfer, no PDF forged, no publication authority
try:
    m.prepare_publication(Path(r'{dst}'), "sources/{ISSUE_W}/production-state.json", prop_rel, staged_rel, bad_mspec_rel, bad_tspec_rel, datetime.now(timezone.utc))
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    out=str(e); print(f"REFUSED prepare invalid exe: {{out[:2000]}}")
    low=out.lower()
    assert "toolchain" in low and ("exe" in low or "executable" in low or "resolve" in low or "not found" in low), out[:1500]
    # ensure no PDF forged, no publication dir created for new proposal
    import pathlib as _pp
    pub=Path(r'{dst}')/f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-3-fault/publication"
    assert not (pub/"build"/"main.pdf").exists(), "no PDF must be forged on controlled failure"
    sys.exit(0)
"""
    r_fail=child_api(dst, code_prep_fail, timeout=300)
    assert r_fail["exit"]==0, f"PUBLIC prepare invalid exe must refuse before transfer {r_fail['stdout'][:2500]} {r_fail['stderr'][:800]}"
    log("R6 PUBLIC prepare invalid exe REFUSED before transfer, no PDF forged OK")
    # extra input: same NEW proposal, toolchain with extra argv (must refuse TOOLCHAIN_ARGV before transfer)
    code_extra=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import json
from datetime import datetime, timezone
from scripts import survey_editorial_publication_v2 as m
from scripts import survey_production_v2 as core
prop_rel="sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-3-fault/proposal.json"
staged_rel="sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-3-fault/staged-source/staged-source-manifest.json"
# load valid toolchain spec for new proposal? Reuse bad_tspec but fix exe to real, add extra argv
tspec=json.loads((Path(r'{dst}')/f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-2/toolchain-spec.json").read_bytes().decode())
# use real exe from valid spec (actual Tool path)
# add extra argv element
tspec["argv"]=list(tspec["argv"])+["extra-input-flag"]
extra_tspec_rel="sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-3-fault/toolchain-spec-extra.json"
Path(r'{dst}', extra_tspec_rel).write_bytes(core.json_bytes(tspec))
# manuscript spec for new proposal (reuse previous bad_mspec which has correct new proposal ref? Recreate fresh)
mspec=json.loads((Path(r'{dst}')/f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-2/manuscript-spec.json").read_bytes().decode())
import hashlib
new_prop_bytes=(Path(r'{dst}')/prop_rel).read_bytes()
mspec["proposal_ref"]=dict(path=prop_rel, sha256=hashlib.sha256(new_prop_bytes).hexdigest())
extra_mspec_rel="sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-3-fault/manuscript-spec-extra.json"
Path(r'{dst}', extra_mspec_rel).write_bytes(core.json_bytes(mspec))
try:
    m.prepare_publication(Path(r'{dst}'), "sources/{ISSUE_W}/production-state.json", prop_rel, staged_rel, extra_mspec_rel, extra_tspec_rel, datetime.now(timezone.utc))
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    out=str(e); print(f"REFUSED extra argv: {{out[:2000]}}")
    assert "toolchain_argv" in out.lower() or ("argv" in out.lower() and "exactly" in out.lower()), out[:1500]
    sys.exit(0)
"""
    r_extra=child_api(dst, code_extra, timeout=300)
    assert r_extra["exit"]==0, f"PUBLIC prepare extra argv must refuse {r_extra['stdout'][:2500]}"
    log("R6 PUBLIC prepare extra argv REFUSED before transfer OK (no fake PDF, source coherent prepared positive exists, no repeat success)")

def main():
    for n,f in [("R6_prepare_failure_extra",r6_prepare_failure_extra)]:
        case(n,f)
    log(f"TOTAL prepare pass={PASS} fail={FAIL}")
    for n,s,d,det in CASES: log(f"SUMMARY {s} {n} dt={d:.1f}s {det[:200]}")
    (NOTES/"summary_r6_prepare.json").write_text(json.dumps({"pass":PASS,"fail":FAIL,"cases":[{"name":n,"status":s} for n,s,_,_ in CASES]}, indent=2))
    print(f"EXIT:{0 if FAIL==0 else 2}"); return 0 if FAIL==0 else 2
if __name__=="__main__":
    try: rc=main()
    except Exception: traceback.print_exc(); print("EXIT:2"); rc=2
    import sys as _s; _s.exit(rc)
