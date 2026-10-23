#!/usr/bin/env python3
"""R6 remaining negatives: predecessor drift, approved/foreign, old canonical, nonPASS."""
from __future__ import annotations
import json, os, sys, time, traceback
from pathlib import Path
sys.dont_write_bytecode=True; os.environ["PYTHONDONTWRITEBYTECODE"]="1"
for _v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE","GIT_OBJECT_DIRECTORY","GIT_ALTERNATE_OBJECT_DIRECTORIES","GIT_COMMON_DIR","GIT_PREFIX"):
    if os.environ.get(_v): print(f"UNSAFE {_v}"); sys.exit(2)
def log(m): print(m, flush=True)
REPO=Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey").resolve()
sys.path.insert(0, str(REPO/"notes/rephase-1-editorial-operation-implementation/final-r6-faults"))
from matrix_common import FAULT_BASE, INERT_W, PRELC_W, cp_fixture, verify_fixture, run_subprocess
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
def r6_rest():
    # predecessor drift
    dst=new_fault(INERT_W, "r6-neg-drift")
    import json as _j
    st_rel=f"sources/{ISSUE_W}/production-state.json"
    st=_j.loads((dst/st_rel).read_bytes().decode()); st["contract"]["pipeline_contract_sha256"]="00"+st["contract"]["pipeline_contract_sha256"][2:]
    (dst/st_rel).write_bytes(json.dumps(st, indent=2, sort_keys=True).encode()+b"\n")
    set_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-2/publication/publication-set.json"
    code=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
from scripts import survey_editorial_publication_v2 as m
try:
    m.activate_publication(Path(r'{dst}'), r'{st_rel}', r'{set_rel}', "drift R6", "tester", __import__("datetime").datetime.now(__import__("datetime").timezone.utc))
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    assert "drift" in str(e).lower() or "before_state" in str(e).lower() or "contract" in str(e).lower(), str(e)[:1200]
    print("drift refused"); sys.exit(0)
"""
    r=child_api(dst, code); assert r["exit"]==0, f"drift R6 must refuse {r['stdout'][:1500]}"
    log("R6 predecessor drift PASS")
    # approved
    dst2=new_fault(INERT_W, "r6-neg-approved")
    st2=_j.loads((dst2/st_rel).read_bytes().decode()); st2["human_gates"]["publication_preview"]="approved"
    (dst2/st_rel).write_bytes(json.dumps(st2, indent=2, sort_keys=True).encode()+b"\n")
    code2=code.replace("drift R6","approved R6").replace("drift\" in", "predecision\" in or \"preview\" in")
    # simpler: reuse generic predecision check
    code2=f"""
import sys; sys.path.insert(0, r'{dst2}')
from pathlib import Path
from scripts import survey_editorial_publication_v2 as m
try:
    m.activate_publication(Path(r'{dst2}'), r'{st_rel}', r'{set_rel}', "approved R6", "tester", __import__("datetime").datetime.now(__import__("datetime").timezone.utc))
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    assert "predecision" in str(e).lower() or "preview" in str(e).lower(), str(e)[:1200]
    print("approved refused"); sys.exit(0)
"""
    r2=child_api(dst2, code2); assert r2["exit"]==0, f"approved R6 must refuse {r2['stdout'][:1000]}"
    log("R6 approved PASS")
    # old canonical (PRELC State r2, old canonical file standalone fine but not selected)
    dst3=new_fault(PRELC_W, "r6-neg-oldcanon")
    code3=f"""
import sys; sys.path.insert(0, r'{dst3}')
from pathlib import Path
from scripts import survey_publication_set_v2 as s, survey_production_v2 as core, survey_publication_v2 as p
cfg=core.load_json(Path(r'{dst3}')/core.DEFAULT_CONFIG)
st=core.load_json(Path(r'{dst3}')/r'{st_rel}')
sel=s.resolve_publication_selection(Path(r'{dst3}'), cfg, st)
assert sel.get('mode')=="VERSIONED_ACTIVE" and "wk-r6-2" in (sel.get('candidate_ref') or {{}}).get("path","")
canon=Path(r'{dst3}')/r'sources/{ISSUE_W}/publication/v2/publication-candidate-v2.json'
if canon.is_file():
    try: p.validate_candidate(Path(r'{dst3}'), canon); print("canon standalone fine")
    except Exception as e: print(f"canon standalone invalid {{e}}")
else: print("canon absent")
"""
    r3=child_api(dst3, code3); assert r3["exit"]==0, f"old canon R6 failed {r3['stdout'][:1000]}"
    log("R6 old canonical PASS")
    dst4=new_fault(INERT_W, "r6-neg-nonpass")
    code4=f"""
import sys; sys.path.insert(0, r'{dst4}')
from pathlib import Path
import json
from scripts import survey_production_v2 as core
# load semantic review path from seal
seal_rel=r'sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-2/publication/publication-set.json'
seal=json.loads((Path(r'{dst4}')/seal_rel).read_bytes().decode())
sem_path=seal['roles']['semantic-review']['path']
rp=Path(r'{dst4}')/sem_path
rev=json.loads(rp.read_bytes().decode())
rev['status']="FAILED"
# recompute review_sha256 if present
if 'review_sha256' in rev:
    base={{k: rev[k] for k in ("schema_version","issue_id","research_profile","publication_profile","review_kind","status","production_profile","reader_manuscript","source","pdf","page_count","checks","reviewed_by","recorded_at")}}
    rev['review_sha256']=core.sha256_object(base)
rp.write_bytes(core.json_bytes(rev))
new_sha=core.sha256_bytes(rp.read_bytes()); new_bytes=rp.stat().st_size
# update candidate semantic_review + seal
cand_rel=r'sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-2/publication/publication-candidate-v2.json'
cp=Path(r'{dst4}')/cand_rel
cand=json.loads(cp.read_bytes().decode())
cand['semantic_review']=dict(path=sem_path, sha256=new_sha, byte_count=new_bytes)
base_cand={{k: cand[k] for k in ("schema_version","issue_id","publication_profile","status","reader_manuscript","source","pdf","quality_bundle","semantic_review","visual_review")}}
cand['candidate_sha256']=core.sha256_object(base_cand)
cp.write_bytes(core.json_bytes(cand))
new_cand_sha=core.sha256_bytes(cp.read_bytes())
sp=Path(r'{dst4}')/seal_rel
seal=json.loads(sp.read_bytes().decode())
seal['roles']['semantic-review']=dict(path=sem_path, sha256=new_sha, byte_count=new_bytes)
seal['roles']['publication-candidate']=dict(path=cand_rel, sha256=new_cand_sha, byte_count=cp.stat().st_size)
tmp=dict(seal); tmp.pop('set_sha256', None)
seal['set_sha256']=core.sha256_object(tmp)
sp.write_bytes(core.json_bytes(seal))
print("forged nonPASS fresh")
"""
    r4_pre=child_api(dst4, code4); assert r4_pre["exit"]==0, f"nonPASS forgery failed {r4_pre['stdout'][:1500]} {r4_pre['stderr'][:800]}"
    code4v=f"""
import sys; sys.path.insert(0, r'{dst4}')
from pathlib import Path
from scripts import survey_editorial_publication_v2 as m
try:
    m.validate_prepared_set(Path(r'{dst4}'), r'sources/{ISSUE_W}/production-state.json', r'sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-2/publication/publication-set.json')
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    out=str(e); print(f"REFUSED nonPASS: {{out[:2000]}}")
    assert "status" in out.lower() or "pass" in out.lower() or "failed" in out.lower(), out[:1200]
    import sys as _s; _s.exit(0)
"""
    r4=child_api(dst4, code4v); assert r4["exit"]==0, f"nonPASS R6 must refuse {r4['stdout'][:2000]}"
    log("R6 nonPASS (fresh) PASS")
def main():
    for n,f in [("R6_rest",r6_rest)]:
        case(n,f)
    log(f"TOTAL rest pass={PASS} fail={FAIL}")
    for n,s,d,det in CASES: log(f"SUMMARY {s} {n} dt={d:.1f}s {det[:200]}")
    (NOTES/"summary_r6_neg2.json").write_text(json.dumps({"pass":PASS,"fail":FAIL,"cases":[{"name":n,"status":s} for n,s,_,_ in CASES]}, indent=2))
    print(f"EXIT:{0 if FAIL==0 else 2}"); return 0 if FAIL==0 else 2
if __name__=="__main__":
    try: rc=main()
    except Exception: traceback.print_exc(); print("EXIT:2"); rc=2
    import sys as _s; _s.exit(rc)
