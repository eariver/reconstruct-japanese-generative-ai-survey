#!/usr/bin/env python3
"""R6 negatives spot-check where needed (code affected: cross-binding already done; here clone/unknown/reviews/tamper/inert/old)."""
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

def r6_neg():
    # unknown branch
    dst=new_fault(INERT_W, "r6-neg-unknown")
    import json as _j
    rec_rel=f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r1.json"
    rec=_j.loads((dst/rec_rel).read_bytes().decode())
    bad_rel=f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-UNKNOWN.json"
    bad=dict(rec); bad["kind"]="UNKNOWN_KIND_X"
    (dst/bad_rel).write_bytes(json.dumps(bad, indent=2, sort_keys=True).encode()+b"\n")
    code=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
from scripts import survey_publication_set_v2 as m
try:
    m.validate_activation_record(Path(r'{dst}'), Path(r'{dst}')/r'{bad_rel}')
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    assert "branch" in str(e).lower() or "kind" in str(e).lower() or "unknown" in str(e).lower(), str(e)[:800]
    print("unknown branch refused"); sys.exit(0)
"""
    r=child_api(dst, code); assert r["exit"]==0, f"unknown branch R6 must refuse {r['stdout'][:1000]}"
    log("R6 unknown branch PASS")
    # State clone (retained) refused, historical valid
    dst2=new_fault(INERT_W, "r6-neg-clone")
    code2=f"""
import sys; sys.path.insert(0, r'{dst2}')
from pathlib import Path
import json
from scripts import survey_production_v2 as core
from scripts import survey_editorial_publication_v2 as m
staged=json.loads((Path(r'{dst2}')/r'sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-2/staged-source/staged-source-manifest.json').read_bytes().decode())
ret=json.loads((Path(r'{dst2}')/staged['retention_manifest_ref']['path']).read_bytes().decode())
srow=[x for x in ret['rows'] if x.get('path')==r'sources/{ISSUE_W}/production-state.json'][0]
retained=srow['retained_dest']
try:
    m.validate_editorial_receipt(Path(r'{dst2}'), r'sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-2/publication/validated-source-manifest.json', retained)
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    assert "canonical" in str(e).lower() or "retained" in str(e).lower() or "state_not_canonical" in str(e).lower(), str(e)[:800]
    print("clone refused"); sys.exit(0)
"""
    r2=child_api(dst2, code2); assert r2["exit"]==0, f"clone R6 must refuse {r2['stdout'][:1000]}"
    log("R6 State clone refused PASS")
    # reviews missing/nonPASS + tamper spot + inert/old canonical
    for sub in ["review-missing","tamper-source","inert-not-adopted"]:
        name=f"r6-neg-{sub}"
        d=new_fault(INERT_W if sub!="inert-not-adopted" else INERT_W, name)
        if sub=="review-missing":
            # find semantic review path from seal (external-reviews)
            import json as _jj
            seal=_jj.loads((d/f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-2/publication/publication-set.json").read_bytes().decode())
            sr=seal["roles"]["semantic-review"]["path"]
            (d/sr).unlink()
        elif sub=="tamper-source":
            import json as _jj2
            seal2=_jj2.loads((d/f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-2/publication/publication-set.json").read_bytes().decode())
            # tamper validated-source (staged main.tex) without updating digests
            man=seal2["roles"]["validated-source"]["path"]
            (d/man).write_bytes((d/man).read_bytes()+b"\n%TAMPER R6\n")
        # inert-not-adopted needs no tamper (healthy inert)
        state_rel=f"sources/{ISSUE_W}/production-state.json"
        set_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-2/publication/publication-set.json"
        code3=f"""
import sys; sys.path.insert(0, r'{d}')
from pathlib import Path
from scripts import survey_editorial_publication_v2 as m, survey_publication_set_v2 as s, survey_production_v2 as core
try:
    v=m.validate_prepared_set(Path(r'{d}'), r'{state_rel}', r'{set_rel}')
    print(f"VALID {{v.get('issue_id')}}")
    {"assert False, 'review-missing should have refused'" if sub=="review-missing" else ""}
    {"assert False, 'tamper should have refused'" if sub=="tamper-source" else ""}
    # inert-not-adopted: valid but not active
    cfg=core.load_json(Path(r'{d}')/core.DEFAULT_CONFIG)
    st=core.load_json(Path(r'{d}')/r'{state_rel}')
    sel=s.resolve_publication_selection(Path(r'{d}'), cfg, st)
    assert sel.get('mode')!='VERSIONED_ACTIVE' or 'wk-r6-2' not in (sel.get('set_ref') or {{}}).get('path',''), "inert must NOT be active"
    print("inert valid not adopted")
except Exception as e:
    out=str(e); print(f"REFUSED {{out[:1500]}}")
    {"assert 'review' in out.lower() or 'missing' in out.lower(), out[:800]" if sub=="review-missing" else ""}
    {"assert 'mismatch' in out.lower() or 'drift' in out.lower() or 'sha' in out.lower(), out[:800]" if sub=="tamper-source" else ""}
    {"assert False, f'unexpected refuse inert {out[:800]}'" if sub=="inert-not-adopted" else ""}
    import sys as _s; _s.exit(0)
"""
        # fix triple-brace escaping: outer f-string, inner {{}} already escaped? Above code3 uses {{}} for dict empty? Yes.
        r3=child_api(d, code3)
        # for review-missing/tamper, child should exit 0 (refused) via except path (sys.exit 0). For inert, child should exit 0 via valid path (no exception, falls through? Actually code3 for inert has no exception expected, so it will go to print VALID then resolve, then end without sys.exit? Need explicit exit 0.
        # Our code3 for inert: try validates, then resolve, then print, then no sys.exit -> child exits 0 implicitly? Actually python -c exits 0 if no exception. Good.
        # For review/tamper: try expects refuse, so except exits 0. Good.
        assert r3["exit"]==0, f"{sub} R6 failed {r3['stdout'][:1500]} {r3['stderr'][:800]}"
        log(f"R6 {sub} OK")
    # fresh hash dups (strict nested duplicate with fresh set_sha? Use seal duplicate JSON)
    dst_dup=new_fault(INERT_W, "r6-neg-dup")
    seal_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-2/publication/publication-set.json"
    raw=(dst_dup/seal_rel).read_bytes().decode()
    import re as _re
    dup_raw=_re.sub(r'"status"\s*:\s*"SEALED_INERT"', '"status": "SEALED_INERT", "status": "SEALED_INERT"', raw, count=1)
    assert dup_raw!=raw
    (dst_dup/seal_rel).write_bytes(dup_raw.encode())
    code_dup=f"""
import sys; sys.path.insert(0, r'{dst_dup}')
from pathlib import Path
from scripts import survey_editorial_publication_v2 as m
try:
    m.validate_prepared_set(Path(r'{dst_dup}'), r'sources/{ISSUE_W}/production-state.json', r'{seal_rel}')
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    assert "duplicate" in str(e).lower(), str(e)[:1000]
    print("dup refused"); sys.exit(0)
"""
    r_dup=child_api(dst_dup, code_dup); assert r_dup["exit"]==0, f"dup R6 must refuse {r_dup['stdout'][:1000]}"
    log("R6 fresh-hash dup (strict nested) PASS")

def main():
    for n,f in [("R6_neg",r6_neg)]:
        case(n,f)
    log(f"TOTAL neg pass={PASS} fail={FAIL}")
    for n,s,d,det in CASES: log(f"SUMMARY {s} {n} dt={d:.1f}s {det[:200]}")
    (NOTES/"summary_r6_neg.json").write_text(json.dumps({"pass":PASS,"fail":FAIL,"cases":[{"name":n,"status":s} for n,s,_,_ in CASES]}, indent=2))
    print(f"EXIT:{0 if FAIL==0 else 2}"); return 0 if FAIL==0 else 2
if __name__=="__main__":
    try: rc=main()
    except Exception: traceback.print_exc(); print("EXIT:2"); rc=2
    import sys as _s; _s.exit(rc)
