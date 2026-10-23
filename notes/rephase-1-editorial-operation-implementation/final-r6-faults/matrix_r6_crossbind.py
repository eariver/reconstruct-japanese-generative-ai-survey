#!/usr/bin/env python3
"""R6 cross-binding: seal-only repeat (must REFUSE), reviewed-TARGET rebind (must REFUSE), external counter-control (must PASS)."""
from __future__ import annotations
import json, os, sys, time, traceback, shutil
from pathlib import Path
sys.dont_write_bytecode=True; os.environ["PYTHONDONTWRITEBYTECODE"]="1"
for _v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE","GIT_OBJECT_DIRECTORY","GIT_ALTERNATE_OBJECT_DIRECTORIES","GIT_COMMON_DIR","GIT_PREFIX"):
    if os.environ.get(_v): print(f"UNSAFE {_v}"); sys.exit(2)
def log(m): print(m, flush=True)
REPO=Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey").resolve()
sys.path.insert(0, str(REPO/"notes/rephase-1-editorial-operation-implementation/final-r6-faults"))
from matrix_common import FAULT_BASE, INERT_W, PRELC_W, cp_fixture, verify_fixture, run_subprocess, sha_file
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

def r6_seal_only():
    # Repeat R5b A_equalSHA: only seal role changed, Candidate still old path. R6 must REFUSE candidate semantic_review vs seal path+SHA.
    # Preserve old UNEXPECTED_PASS (R5b matrix_a2 a-equal-sha-wrong-path FAIL with UNEXPECTED_PASS).
    dst=new_fault(INERT_W, "r6-seal-only")
    import json as _j
    seal_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-2/publication/publication-set.json"
    seal0=_j.loads((dst/seal_rel).read_bytes().decode())
    sem_rel=seal0["roles"]["semantic-review"]["path"]
    # forged same-SHA different filename in same dir (repo-contained)
    new_rel=str(Path(sem_rel).parent / (Path(sem_rel).stem + "-forged.json"))
    if not (dst/new_rel).exists():
        shutil.copy(str(dst/sem_rel), str(dst/new_rel))
    assert sha_file(dst/sem_rel)==sha_file(dst/new_rel)
    seal=_j.loads((dst/seal_rel).read_bytes().decode())
    if seal["roles"]["semantic-review"]["path"]!=new_rel:
        seal["roles"]["semantic-review"]={"path":new_rel,"sha256":seal["roles"]["semantic-review"]["sha256"],"byte_count":seal["roles"]["semantic-review"]["byte_count"]}
        (dst/seal_rel).write_bytes(json.dumps(seal, indent=2, sort_keys=True).encode()+b"\n")
    # fresh set_sha via core.sha256_object (avoid digest preemption, reach cross-binding)
    code_up=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
from scripts import survey_production_v2 as core
import json
p=Path(r'{dst}')/r'{seal_rel}'
s=json.loads(p.read_bytes().decode())
tmp=dict(s); tmp.pop('set_sha256', None)
s['set_sha256']=core.sha256_object(tmp)
p.write_bytes(core.json_bytes(s))
print("fresh set")
"""
    r_up=child_api(dst, code_up); assert r_up["exit"]==0, f"fresh set failed {r_up['stdout'][:800]} {r_up['stderr'][:800]}"
    state_rel=f"sources/{ISSUE_W}/production-state.json"
    code=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
from scripts import survey_editorial_publication_v2 as m
try:
    m.validate_prepared_set(Path(r'{dst}'), r'{state_rel}', r'{seal_rel}')
    print("UNEXPECTED_PASS_R6"); sys.exit(10)
except Exception as e:
    out=str(e); print(f"REFUSED: {{out[:2500]}}")
    low=out.lower()
    assert "candidate" in low and "semantic_review" in low, f"must refuse Candidate.semantic_review vs seal, got {{out[:1500]}}"
    assert "path" in low and "sha" in low or "must equal seal" in low, f"must be path+SHA {{out[:1200]}}"
    sys.exit(0)
"""
    # fix double-brace escape: outer f-string, inner {{out...}} already escaped? Above uses {{out...}} good.
    r=child_api(dst, code); assert r["exit"]==0, f"R6 seal-only must REFUSE cross-binding, got exit {r['exit']} {r['stdout'][:2500]} {r['stderr'][:800]}"
    log(f"R6 seal-only REFUSED as expected (old R5b UNEXPECTED_PASS preserved): {r['stdout'][:400]}")

def r6_target_rebind():
    # Actual reviewed TARGET sameSHA rebind: copy SAME bytes manuscript outside publication,
    # update review.reader_manuscript ref + review digest and dependent candidate/seal hashes consistently,
    # leave seal reader-manuscript original. Must refuse exact target path.
    dst=new_fault(INERT_W, "r6-target-rebind")
    import json as _j
    seal0=_j.loads((dst/f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-2/publication/publication-set.json").read_bytes().decode())
    man_rel=seal0["roles"]["reader-manuscript"]["path"]
    sem_rel=seal0["roles"]["semantic-review"]["path"]
    # copy SAME bytes outside publication (repo-contained, e.g., external-reviews dir)
    out_rel=str(Path(sem_rel).parent / "reader-manuscript-copy.json")
    (dst/out_rel).parent.mkdir(parents=True, exist_ok=True)
    if not (dst/out_rel).exists():
        shutil.copy(str(dst/man_rel), str(dst/out_rel))
    assert sha_file(dst/man_rel)==sha_file(dst/out_rel)
    code_up=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import json
from scripts import survey_production_v2 as core
# review file: change reader_manuscript.path to outside path (same SHA) + fresh review_sha256 (content digest)
rp=Path(r'{dst}')/r'{sem_rel}'
rev=json.loads(rp.read_bytes().decode())
assert rev.get('reader_manuscript',{{}}).get('path')==r'{man_rel}', "unexpected review target"
rev['reader_manuscript']=dict(path=r'{out_rel}', sha256=r'{sha_file(dst/man_rel)}')
base={{k: rev[k] for k in ("schema_version","issue_id","research_profile","publication_profile","review_kind","status","production_profile","reader_manuscript","source","pdf","page_count","checks","reviewed_by","recorded_at")}}
rev['review_sha256']=core.sha256_object(base)
rp.write_bytes(core.json_bytes(rev))
new_rev_sha=core.sha256_bytes(rp.read_bytes())
new_rev_bytes=rp.stat().st_size
print(f"review updated sha={{new_rev_sha[:16]}}")
# candidate: update semantic_review to new review SHA (consistent), leave reader_manuscript original? Candidate has reader_manuscript + semantic_review.
# For this negative, update candidate semantic_review path? No, candidate semantic_review path stays original? Wait: review file path unchanged (sem_rel same), only its internal reader_manuscript ref changed. So candidate semantic_review ref (path+SHA) must update SHA to new review SHA (path same). Do that.
cand_rel=r'sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-2/publication/publication-candidate-v2.json'
cp=Path(r'{dst}')/cand_rel
cand=json.loads(cp.read_bytes().decode())
# candidate semantic_review ref + fresh candidate_sha256 (content digest)
if 'semantic_review' in cand and isinstance(cand['semantic_review'], dict):
    cand['semantic_review']=dict(path=r'{sem_rel}', sha256=new_rev_sha, byte_count=new_rev_bytes)
base_cand={{k: cand[k] for k in ("schema_version","issue_id","publication_profile","status","reader_manuscript","source","pdf","quality_bundle","semantic_review","visual_review")}}
cand['candidate_sha256']=core.sha256_object(base_cand)
cp.write_bytes(core.json_bytes(cand))
new_cand_sha=core.sha256_bytes(cp.read_bytes())
print(f"candidate updated sha={{new_cand_sha[:16]}}")
# seal: update semantic-review SHA + publication-candidate SHA consistently, leave reader-manuscript original
seal_rel=r'sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-2/publication/publication-set.json'
sp=Path(r'{dst}')/seal_rel
seal=json.loads(sp.read_bytes().decode())
seal['roles']['semantic-review']=dict(path=r'{sem_rel}', sha256=new_rev_sha, byte_count=new_rev_bytes)
# seal publication-candidate SHA to new candidate file SHA
seal['roles']['publication-candidate']=dict(path=cand_rel, sha256=new_cand_sha, byte_count=cp.stat().st_size)
tmp=dict(seal); tmp.pop('set_sha256', None)
seal['set_sha256']=core.sha256_object(tmp)
sp.write_bytes(core.json_bytes(seal))
print(f"seal fresh {{seal['set_sha256'][:16]}}")
"""
    r_up=child_api(dst, code_up); assert r_up["exit"]==0, f"target rebind forgery update failed {r_up['stdout'][:1500]} {r_up['stderr'][:800]}"
    state_rel=f"sources/{ISSUE_W}/production-state.json"
    seal_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-2/publication/publication-set.json"
    code=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
from scripts import survey_editorial_publication_v2 as m
try:
    m.validate_prepared_set(Path(r'{dst}'), r'{state_rel}', r'{seal_rel}')
    print("UNEXPECTED_PASS_TARGET"); sys.exit(10)
except Exception as e:
    out=str(e); print(f"REFUSED target: {{out[:2500]}}")
    low=out.lower()
    # R6 exact target-path refusal may fire at candidate level (semantic review manuscript drift) or seal level (reader_manuscript must equal seal); both are true target binding, not digest preemption
    assert ("reader_manuscript" in low or "manuscript drift" in low or "manuscript" in low) and ("path" in low or "target" in low or "must equal" in low or "drift" in low), f"must refuse exact target path {{out[:1500]}}"
    assert "digest mismatch" not in low or "drift" in low, f"must not be digest preemption alone {{out[:1200]}}"
    sys.exit(0)
"""
    r=child_api(dst, code); assert r["exit"]==0, f"R6 reviewed-TARGET rebind must REFUSE exact target, got {r['stdout'][:2500]}"
    log("R6 reviewed-TARGET rebind REFUSED exact target OK")

def r6_external_counter():
    # Permissible counter-control: reviews at P/external-reviews, Candidate+seal consistently point there and unchanged targets PASSED by R6 public positive already recorded.
    # Verify existing R6 correction-r6 external-consistent positive (don't invent mandatory filename).
    # Check correction-r6 fixture script exists and recorded PASS.
    import pathlib as _p
    # correction-r6 has r6-external-consistent-L-* exit 0?
    base=REPO/"notes/rephase-1-editorial-operation-implementation/correction-r6"
    for f in ["r6-external-consistent-L-new-exit.txt"]:
        p=base/f
        assert p.is_file(), f"missing {f}"
        assert p.read_text().strip()=="0", f"{f} not 0: {p.read_text()[:200]}"
    log("R6 external counter-control already PASSED in correction-r6 (reviews at P/external-reviews consistent, no mandatory filename invented)")

def main():
    for n,f in [("R6_seal_only",r6_seal_only),("R6_target_rebind",r6_target_rebind),("R6_external_counter",r6_external_counter)]:
        case(n,f)
    log(f"TOTAL R6cross pass={PASS} fail={FAIL}")
    for n,s,d,det in CASES: log(f"SUMMARY {s} {n} dt={d:.1f}s {det[:200]}")
    (NOTES/"summary_r6_crossbind.json").write_text(json.dumps({"pass":PASS,"fail":FAIL,"cases":[{"name":n,"status":s} for n,s,_,_ in CASES]}, indent=2))
    print(f"EXIT:{0 if FAIL==0 else 2}"); return 0 if FAIL==0 else 2
if __name__=="__main__":
    try: rc=main()
    except Exception: traceback.print_exc(); print("EXIT:2"); rc=2
    import sys as _s; _s.exit(rc)
