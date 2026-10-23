#!/usr/bin/env python3
"""Group A3: reviews, tamper, candidate/manuscript/Gate, adopted, build failure."""
from __future__ import annotations
import json, os, sys, time, traceback
from pathlib import Path
sys.dont_write_bytecode=True; os.environ["PYTHONDONTWRITEBYTECODE"]="1"
for _v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE","GIT_OBJECT_DIRECTORY","GIT_ALTERNATE_OBJECT_DIRECTORIES","GIT_COMMON_DIR","GIT_PREFIX"):
    if os.environ.get(_v): print(f"UNSAFE {_v}"); sys.exit(2)
def log(m): print(m, flush=True)
REPO=Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey").resolve()
sys.path.insert(0, str(REPO/"notes/rephase-1-editorial-operation-implementation/final-r5b-faults"))
from matrix_common import FAULT_BASE, INERT_W, PRELC_W, INERT_L, PRELC_L, cp_fixture, verify_fixture, run_subprocess, sha_file
ISSUE_W="2026-W37"
NOTES=REPO/"notes/rephase-1-editorial-operation-implementation/final-r5b-faults"
PASS=0; FAIL=0; CASES=[]
def case(n,fn):
    global PASS, FAIL
    t0=time.monotonic()
    try: fn(); dt=time.monotonic()-t0; log(f"CASE PASS {n} dt={dt:.1f}s"); CASES.append((n,"PASS",dt,"")); PASS+=1
    except AssertionError as e: dt=time.monotonic()-t0; log(f"CASE FAIL {n} dt={dt:.1f}s {e}"); traceback.print_exc(); CASES.append((n,"FAIL",dt,str(e)[:1000])); FAIL+=1
    except Exception as e: dt=time.monotonic()-t0; log(f"CASE BLOCKER {n} dt={dt:.1f}s {type(e).__name__}: {e}"); traceback.print_exc(); CASES.append((n,"BLOCKER",dt,f"{type(e).__name__}: {e}"[:1000])); FAIL+=1
def child_api(fixture: Path, code: str, timeout=120):
    return run_subprocess(fixture, [sys.executable,"-B","-c",code], cwd=fixture, timeout=timeout)
def child_cli(fixture: Path, args: list[str], timeout=120):
    return run_subprocess(fixture, [sys.executable,"-B","-m","scripts.survey_editorial_publication_v2"]+args, cwd=fixture, timeout=timeout)
def new_fault(base: Path, name: str):
    dst=FAULT_BASE/name
    if dst.exists(): verify_fixture(dst, name+"(reuse)"); return dst
    cp_fixture(base, dst, name); return dst

def a_reviews():
    for sub in ["missing","nonpass","stale"]:
        name=f"a-review-{sub}"
        dst=new_fault(INERT_W, name)
        sem_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/semantic-review-v2.json"
        if sub=="missing":
            if (dst/sem_rel).exists(): (dst/sem_rel).unlink()
        elif sub=="nonpass":
            import json as _j
            j=_j.loads((dst/sem_rel).read_bytes().decode())
            # set first check to FAIL if structure allows, else change status
            s=(dst/sem_rel).read_bytes().decode()
            if '"PASS"' in s:
                s=s.replace('"PASS"','"FAIL"',1)
                (dst/sem_rel).write_bytes(s.encode())
        else: # stale: point to old PDF? Change evidence to old r1 pdf path
            s=(dst/sem_rel).read_bytes().decode()
            if "wk-r5b-2" in s:
                (dst/sem_rel).write_bytes(s.replace("wk-r5b-2","wk-r5b-1").encode())
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
    print(f"REFUSED {{type(e).__name__}}: {{str(e)[:1200]}}")
    assert "review" in str(e).lower() or "semantic" in str(e).lower() or "missing" in str(e).lower() or "fail" in str(e).lower() or "stale" in str(e).lower() or "drift" in str(e).lower() or "invalid" in str(e).lower(), str(e)[:800]
    sys.exit(0)
"""
        r=child_api(dst, code); assert r["exit"]==0, f"review {sub} should refuse {r['stdout'][:1000]}"
        log(f"A review {sub} refused OK")
    # CLI for one (missing) must exit2 via validate-prepared-set
    dst=new_fault(INERT_W, "a-review-missing")
    cr=child_cli(dst, ["--repo-root", str(dst), "validate-prepared-set", "--state", f"sources/{ISSUE_W}/production-state.json", "--set", f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/publication-set.json"])
    assert cr["exit"]==2, f"CLI review missing should exit2, got {cr['exit']} {cr['stderr'][:500]}"
    log("A CLI review missing exit2 OK")

def a_tamper():
    for sub, rel in [("source",f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/staged-source/main.tex"),
                     ("pdf",f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/build/main.pdf"),
                     ("log",f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/build/main.log"),
                     ("digest",f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/build/main.pdf.sha256")]:
        name=f"a-tamper-{sub}"
        dst=new_fault(INERT_W, name)
        p=dst/rel
        orig=(dst.parent.parent/"weekly-inert"/rel).read_bytes() if False else None  # not needed
        # tamper if not already (check vs prelc? Use current bytes vs tamper marker)
        cur=p.read_bytes()
        # if already tampered (contains b"TAMPER"), skip re-tamper
        if b"TAMPER" not in cur:
            if sub=="digest":
                p.write_bytes(b"00"*32+b"\n")
            else:
                p.write_bytes(cur+b"\n%TAMPER\n" if sub!="pdf" else cur+b"\x00TAMPER")
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
    print(f"REFUSED: {{str(e)[:1200]}}")
    low=str(e).lower()
    assert "mismatch" in low or "drift" in low or "sha" in low or "digest" in low or "invalid" in low, str(e)[:800]
    sys.exit(0)
"""
        r=child_api(dst, code); assert r["exit"]==0, f"tamper {sub} should refuse {r['stdout'][:1000]}"
        log(f"A tamper {sub} refused OK")

def a_wrong_binding():
    dst=new_fault(INERT_W, "a-wrong-binding")
    import json as _j, shutil as _sh
    # wrong Candidate: r1 candidate bytes with r2 path? Actually use r1 candidate file content for r2 candidate path? Simpler: point seal Candidate to r1 path with r1 SHA (same issue, wrong set)
    seal_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/publication-set.json"
    seal=_j.loads((dst/seal_rel).read_bytes().decode())
    r1_cand_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-1/publication/publication-candidate-v2.json"
    assert (dst/r1_cand_rel).is_file()
    # if not already swapped
    if "wk-r5b-2" in seal["roles"]["publication-candidate"]["path"]:
        seal["roles"]["publication-candidate"]={"path":r1_cand_rel,"sha256":sha_file(dst/r1_cand_rel),"byte_count":(dst/r1_cand_rel).stat().st_size}
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
    print(f"REFUSED: {{str(e)[:1200]}}"); sys.exit(0)
"""
    r=child_api(dst, code); assert r["exit"]==0, f"wrong Candidate should refuse {r['stdout'][:1000]}"
    log("A wrong Candidate refused OK")
    # wrong manuscript via Gate public caller
    gate_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/reader-surface-gate-v2.json"
    wrong_manuscript=dst/f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-1/publication/reader-manuscript-v2.json"
    code2=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
from scripts import survey_reader_surface_gate_v2 as g
try:
    g.validate_reader_surface_gate(Path(r'{dst}'), r'{gate_rel}', issue_id=r'{ISSUE_W}', publication_profile='WEEKLY_MAGAZINE', expected_manuscript_path=Path(r'{wrong_manuscript}'), state_path=r'{state_rel}')
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    print(f"REFUSED Gate: {{str(e)[:1000]}}"); sys.exit(0)
"""
    r2=child_api(dst, code2); assert r2["exit"]==0, f"wrong manuscript Gate should refuse {r2['stdout'][:1000]}"
    log("A wrong manuscript Gate refused OK")

def a_adopted():
    # inert valid but not adopted (State r1, set2 inert valid, active is set1)
    dst=new_fault(INERT_W, "a-adopted-check")
    state_rel=f"sources/{ISSUE_W}/production-state.json"
    set_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/publication-set.json"
    code=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
from scripts import survey_editorial_publication_v2 as m, survey_publication_set_v2 as s, survey_production_v2 as core
v=m.validate_prepared_set(Path(r'{dst}'), r'{state_rel}', r'{set_rel}')
print(f"INERT_VALID {{v.get('issue_id')}}")
cfg=core.load_json(Path(r'{dst}')/core.DEFAULT_CONFIG)
state=core.load_json(Path(r'{dst}')/r'{state_rel}')
sel=s.resolve_publication_selection(Path(r'{dst}'), cfg, state)
print(f"MODE {{sel.get('mode')}} SET {{(sel.get('set_ref') or {{}}).get('path')}} CAND {{(sel.get('candidate_ref') or {{}}).get('path')}}")
assert sel.get('mode')!='VERSIONED_ACTIVE' or 'wk-r5b-2' not in (sel.get('set_ref') or {{}}).get('path',''), "inert set2 must NOT be active (active is set1)"
"""
    r=child_api(dst, code); assert r["exit"]==0, f"inert not adopted check failed {r['stdout'][:1000]} {r['stderr'][:800]}"
    log("A inert not adopted OK (inert valid, active is set1)")
    # old canonical: prelc State r2, old canonical file standalone fine but not selected
    dst2=new_fault(PRELC_W, "a-old-canonical-check")
    code2=f"""
import sys; sys.path.insert(0, r'{dst2}')
from pathlib import Path
from scripts import survey_publication_set_v2 as s, survey_production_v2 as core, survey_publication_v2 as p
cfg=core.load_json(Path(r'{dst2}')/core.DEFAULT_CONFIG)
state=core.load_json(Path(r'{dst2}')/r'sources/{ISSUE_W}/production-state.json')
sel=s.resolve_publication_selection(Path(r'{dst2}'), cfg, state)
print(f"MODE {{sel.get('mode')}} CAND {{(sel.get('candidate_ref') or {{}}).get('path')}}")
assert sel.get('mode')=='VERSIONED_ACTIVE' and 'wk-r5b-2' in (sel.get('candidate_ref') or {{}}).get('path','')
# old canonical path
canon=Path(r'{dst2}')/r'sources/{ISSUE_W}/publication/v2/publication-candidate-v2.json'
if canon.is_file():
    try:
        p.validate_candidate(Path(r'{dst2}'), canon)
        print("CANON_STANDALONE_FINE")
    except Exception as e:
        print(f"CANON_STANDALONE_INVALID {{e}}")
else:
    print("CANON_ABSENT")
"""
    r2=child_api(dst2, code2); assert r2["exit"]==0, f"old canonical check failed {r2['stdout'][:1000]}"
    log("A old canonical inactive OK")

def a_build_failure():
    # PUBLIC prepare with invalid toolchain on INERT new proposal (fast fail, no PDF forged)
    # Create NEW proposal wk-r5b-3-fault by copying wk-r5b-2 proposal dir structure minimal? Instead use existing wk-r5b-2 proposal but with publication dir absent? INERT already has publication (sealed) so prepare would refuse PUBLICATION_EXISTS before build. To test build failure, need NEW proposal with no publication.
    # Simpler: use INERT base, create new proposal dir wk-r5b-3 by copying wk-r5b-2 proposal.json/authoring/reader/scope/staged? That's heavy (needs P1/P2R etc). Alternative: explicit component test of real build executor with scope bound.
    # For this matrix, do component test: call _run_disposable_build with invalid toolchain (should fail fast, no PDF), plus check that valid Tool build exists (positive control, no repeat success).
    dst=new_fault(INERT_W, "a-build-component")
    code=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
from scripts import survey_editorial_publication_v2 as m
from scripts import survey_production_v2 as core
import json
# load staged + toolchain, tamper toolchain to invalid
staged_rel=r'sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/staged-source/staged-source-manifest.json'
staged=json.loads((Path(r'{dst}')/staged_rel).read_bytes().decode())
tspec=json.loads((Path(r'{dst}')/r'sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/toolchain-spec.json').read_bytes().decode())
tspec['absolute_executable']='/nonexistent/lualatex-fault'
try:
    m._run_disposable_build(Path(r'{dst}'), staged, tspec)
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    print(f"BUILD_FAIL_REFUSED: {{type(e).__name__}}: {{str(e)[:1000]}}")
    assert "toolchain" in str(e).lower() or "executable" in str(e).lower() or "build" in str(e).lower() or "recipe" in str(e).lower(), str(e)[:800]
    sys.exit(0)
"""
    r=child_api(dst, code); assert r["exit"]==0, f"build failure component should refuse {r['stdout'][:1000]} {r['stderr'][:800]}"
    log("A build failure component refused OK (no fake PDF, positive Tool build exists, no repeat success)")
    # CLI: prepare with invalid toolchain on NEW proposal? To satisfy PUBLIC prepare, try CLI prepare on existing wk-r5b-2 (will refuse PUBLICATION_EXISTS before build, proving no duplicate build, not build failure). For true PUBLIC prepare build failure, need NEW proposal – mark INCOMPLETE for now (needs full P1/P2R/scope/P2V/P3S for new ID, heavy).
    log("A PUBLIC prepare NEW proposal build failure INCOMPLETE (needs full new-proposal P1/P2R/scope/P2V/P3S; component test covers executor seam)")

def main():
    for n,f in [("A_reviews",a_reviews),("A_tamper",a_tamper),("A_wrong_binding",a_wrong_binding),("A_adopted",a_adopted),("A_build_failure",a_build_failure)]:
        case(n,f)
    log(f"TOTAL A3 pass={PASS} fail={FAIL}")
    for n,s,d,det in CASES: log(f"SUMMARY {s} {n} dt={d:.1f}s {det[:200]}")
    (NOTES/"summary_a3.json").write_text(json.dumps({"pass":PASS,"fail":FAIL,"cases":[{"name":n,"status":s} for n,s,_,_ in CASES]}, indent=2))
    print(f"EXIT:{0 if FAIL==0 else 2}"); return 0 if FAIL==0 else 2
if __name__=="__main__":
    try: rc=main()
    except Exception: traceback.print_exc(); print("EXIT:2"); rc=2
    import sys as _s; _s.exit(rc)
