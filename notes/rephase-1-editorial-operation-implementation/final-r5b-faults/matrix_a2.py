#!/usr/bin/env python3
"""Group A2: State clone/retained, deep forgery, reviews, tamper, candidate, adopted, build."""
from __future__ import annotations
import hashlib, json, os, sys, time, traceback
from pathlib import Path
sys.dont_write_bytecode=True; os.environ["PYTHONDONTWRITEBYTECODE"]="1"
for _v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE","GIT_OBJECT_DIRECTORY","GIT_ALTERNATE_OBJECT_DIRECTORIES","GIT_COMMON_DIR","GIT_PREFIX"):
    if os.environ.get(_v): print(f"UNSAFE {_v}"); sys.exit(2)
def log(m): print(m, flush=True)
REPO=Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey").resolve()
sys.path.insert(0, str(REPO/"notes/rephase-1-editorial-operation-implementation/final-r5b-faults"))
from matrix_common import FAULT_BASE, INERT_W, PRELC_W, INERT_L, PRELC_L, cp_fixture, verify_fixture, run_subprocess, sha_file
ISSUE_W="2026-W37"; ISSUE_L="SP001"
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

def a_state_clone_retained():
    # canonical accepted, retained/cloned rejected, historical separate valid
    dst=new_fault(INERT_W, "a-state-canonical")
    state_rel=f"sources/{ISSUE_W}/production-state.json"
    set_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/publication-set.json"
    # canonical must pass validate_prepared_set (inert valid against old current State)
    code=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
from scripts import survey_editorial_publication_v2 as m
v=m.validate_prepared_set(Path(r'{dst}'), r'{state_rel}', r'{set_rel}')
print(f"INERT_VALID {{v.get('issue_id')}}"); assert v.get('issue_id')=="{ISSUE_W}"
"""
    r=child_api(dst, code); assert r["exit"]==0, f"canonical inert should validate {r['stdout'][:800]} {r['stderr'][:800]}"
    log("A canonical inert valid OK")
    # retained copy must refuse for current APIs
    # retained State COPY path from retention manifest
    code2=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import json
from scripts import survey_production_v2 as core
staged=core.load_json(Path(r'{dst}')/r'sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/staged-source/staged-source-manifest.json')
ret_rel=staged['retention_manifest_ref']['path']
ret=json.loads((Path(r'{dst}')/ret_rel).read_bytes().decode())
# find State COPY retained_dest
srow=[x for x in ret['rows'] if x.get('path')==r'{state_rel}'][0]
retained_dest=srow['retained_dest']
print(f"retained_dest={{retained_dest}}")
from scripts import survey_editorial_publication_v2 as m
try:
    m.validate_editorial_receipt(Path(r'{dst}'), r'sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/validated-source-manifest.json', retained_dest)
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    print(f"REFUSED {{type(e).__name__}}: {{str(e)[:1000]}}")
    assert "canonical" in str(e).lower() or "retained" in str(e).lower() or "not_canonical" in str(e).lower() or "state_not_canonical" in str(e).lower() or "state" in str(e).lower(), str(e)[:800]
    sys.exit(0)
"""
    r2=child_api(dst, code2); assert r2["exit"]==0, f"retained State should refuse current API {r2['stdout'][:1000]} {r2['stderr'][:800]}"
    log("A retained State refused current API OK")
    # historical separate valid (record-only, no State)
    rec_rel=f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r1.json"
    code3=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
from scripts import survey_editorial_publication_v2 as m
h=m.verify_activation_history(Path(r'{dst}'), r'{rec_rel}')
print(f"HIST {{h.get('status')}}"); assert h.get('status') in ("HISTORICAL_VALID","CURRENT_ACTIVE","INERT"), h
"""
    r3=child_api(dst, code3); assert r3["exit"]==0, f"history should be valid {r3['stdout'][:800]} {r3['stderr'][:800]}"
    log("A historical separate valid OK")
    # CLI: validate-prepared-set with retained State must exit2
    # get retained_dest via python (reuse)
    import json as _j
    staged=_j.loads((dst/f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/staged-source/staged-source-manifest.json").read_bytes().decode())
    ret=_j.loads((dst/staged["retention_manifest_ref"]["path"]).read_bytes().decode())
    srow=[x for x in ret["rows"] if x.get("path")==state_rel][0]
    retained_dest=srow["retained_dest"]
    cr=child_cli(dst, ["--repo-root", str(dst), "validate-prepared-set", "--state", retained_dest, "--set", set_rel])
    assert cr["exit"]==2, f"CLI retained State should exit2, got {cr['exit']} {cr['stderr'][:500]}"
    log("A CLI retained State exit2 OK")

def a_deep_research():
    # changed accepted research with fresh digests -> true replay refusal, not digest preemption
    dst=new_fault(INERT_W, "a-deep-research")
    # tamper accepted Draft? Find accepted ref: use architecture? Actually accepted research: check receipt accepted_refs
    import json as _j
    rec_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/validated-source-manifest.json"
    rec=_j.loads((dst/rec_rel).read_bytes().decode())
    # pick first accepted ref that is a file (e.g., accepted-draft-archive?)
    acc=rec.get("accepted_refs",[])
    assert acc, "no accepted_refs"
    # choose architecture or draft file that exists
    target=None
    for a in acc:
        p=a.get("path")
        if p and (dst/p).is_file() and p.endswith(".json"):
            target=a; break
    assert target, f"no suitable accepted file {acc[:3]}"
    tpath=target["path"]
    orig=(dst/tpath).read_bytes()
    # tamper one byte (append space inside JSON? To keep valid JSON, add whitespace? That changes bytes but still valid JSON with same semantic? Need semantic change: change a value.
    # For deep test, change file bytes minimally but validly, then update all dependent refs to fresh SHA so digest passes, expect replay refusal.
    # Simplest: append newline (whitespace) – still valid JSON, same semantic, but bytes differ. Replay check compares FILE bytes? The receipt rederives reader and compares canonical reader FILE bytes + rendered outputs. Whitespace-only change in accepted research might still cause rederive mismatch? Or might still pass? Better to change a value: load JSON, change a field, dump.
    try:
        obj=_j.loads(orig.decode())
        # change a field if dict, else append
        if isinstance(obj, dict):
            obj["__forgery"]="deep-test"
            new_bytes=json.dumps(obj, indent=2, sort_keys=True).encode()+b"\n"
        else:
            new_bytes=orig+b"\n"
    except Exception:
        new_bytes=orig+b" "
    (dst/tpath).write_bytes(new_bytes)
    new_sha=sha_file(dst/tpath); new_bytes_len=(dst/tpath).stat().st_size
    # update ONLY declared dependent refs: receipt accepted_refs entry + seal? Seal doesn't pin accepted research directly? Receipt does. Also retention? Retention pins upstream? For forgery, update receipt accepted_refs entry + receipt_sha? Receipt has receipt_sha256 self-digest – must recompute? Actually receipt validation checks accepted research via strict State + route loaders (reloads actual file and compares to pin?). If we update pin to fresh, digest passes, but rederived reader should mismatch (since accepted changed, rederived reader differs from reviewed input).
    # Update receipt file: accepted_refs entry + receipt_sha256 (recompute canonical without itself? Need core logic). Simpler: update receipt JSON entry, then recompute receipt_sha256 via core? Let's inspect receipt schema for receipt_sha256 compute.
    # For now, update accepted_ref entry SHA/byte_count if present, and if receipt has byte_count? Check.
    rec2=_j.loads((dst/rec_rel).read_bytes().decode())
    for a in rec2.get("accepted_refs",[]):
        if a.get("path")==tpath:
            a["sha256"]=new_sha
            if "byte_count" in a: a["byte_count"]=new_bytes_len
    # receipt_sha256: hash of canonical object without itself. Try to recompute via core.json_bytes if available, else leave old (will cause digest preemption). To achieve fresh-hash, must recompute correctly. Let's try via subprocess bound to fixture.
    code_update=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import json
from scripts import survey_production_v2 as core
p=Path(r'{dst}')/r'{rec_rel}'
rec=json.loads(p.read_bytes().decode())
# update accepted entry already done on disk? Reload and ensure.
for a in rec.get('accepted_refs',[]):
    if a.get('path')==r'{tpath}':
        a['sha256']=r'{new_sha}'
        # byte_count if present
        # find byte_count key?
        pass
tmp=dict(rec); tmp.pop('receipt_sha256', None)
# core.json_bytes canonical?
new_hash=core.sha256_object(tmp)
rec['receipt_sha256']=new_hash
p.write_bytes(core.json_bytes(rec))
print(f"updated receipt_sha={{new_hash[:16]}}")
"""
    r_up=child_api(dst, code_update)
    assert r_up["exit"]==0, f"receipt fresh-hash update failed {r_up['stdout'][:800]} {r_up['stderr'][:800]}"
    # also update seal? Seal doesn't directly pin accepted research, but receipt does. Seal pins source-receipt (receipt file) – need to update seal source-receipt SHA to fresh receipt SHA.
    seal_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/publication-set.json"
    code_seal=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import json
from scripts import survey_production_v2 as core
seal_p=Path(r'{dst}')/r'{seal_rel}'
seal=json.loads(seal_p.read_bytes().decode())
rec_p=Path(r'{dst}')/r'{rec_rel}'
new_rec_sha=core.sha256_bytes(rec_p.read_bytes())
new_rec_bytes=rec_p.stat().st_size
# update source-receipt role
seal['roles']['source-receipt']=dict(path=r'{rec_rel}', sha256=new_rec_sha, byte_count=new_rec_bytes)
tmp=dict(seal); tmp.pop('set_sha256', None)
seal['set_sha256']=core.sha256_object(tmp)
seal_p.write_bytes(core.json_bytes(seal))
print(f"updated seal set={{seal['set_sha256'][:16]}}")
"""
    r_seal=child_api(dst, code_seal)
    assert r_seal["exit"]==0, f"seal fresh update failed {r_seal['stdout'][:800]} {r_seal['stderr'][:800]}"
    # now validate – should refuse with true replay (not digest)
    state_rel=f"sources/{ISSUE_W}/production-state.json"
    set_rel=seal_rel
    code_v=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
from scripts import survey_editorial_publication_v2 as m
try:
    m.validate_prepared_set(Path(r'{dst}'), r'{state_rel}', r'{set_rel}')
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    out=str(e); print(f"REFUSED {{type(e).__name__}}: {{out[:1500]}}")
    low=out.lower()
    assert "digest" not in low and "drift" not in low or "replay" in low or "scope" in low or "family" in low or "fidelity" in low or "coverage" in low or "closure" in low or "research" in low or "accepted" in low, f"preempted not deep: {{out[:1000]}}"
    assert any(k in low for k in ["replay","scope","family","fidelity","coverage","closure","research","accepted","manifest","receipt"]), f"no deep seam {{out[:1000]}}"
    sys.exit(0)
"""
    r=child_api(dst, code_v)
    assert r["exit"]==0, f"deep research should refuse deep, got {r['stdout'][:1500]} {r['stderr'][:800]}"
    log(f"A deep research forged fresh-hash refused deep OK: {r['stdout'][:400]}")

def a_deep_reader():
    # new reader from old authored inconsistency with fresh digests
    dst=new_fault(INERT_W, "a-deep-reader")
    import json as _j
    # reader-surface-input is proposed reader; authoring-input is proposed authoring. Tamper reader to new bytes inconsistent with authoring, update digests fresh.
    reader_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/reader-surface-input-v2.json"
    orig=_j.loads((dst/reader_rel).read_bytes().decode())
    # change headline or paragraphs to new inconsistent
    if isinstance(orig, dict):
        # try cover/headline
        if "cover" in orig and isinstance(orig["cover"], dict) and "headline" in orig["cover"]:
            orig["cover"]["headline"]="FORGED inconsistent headline"
        else:
            orig["__forged"]="inconsistent"
    new_reader_bytes=json.dumps(orig, indent=2, sort_keys=True).encode()+b"\n"
    (dst/reader_rel).write_bytes(new_reader_bytes)
    new_sha=sha_file(dst/reader_rel); new_len=(dst/reader_rel).stat().st_size
    # update declared dependents: proposal proposed_reader_ref? + seal reader-input + receipt reviewed_reader_input?
    # Update via subprocess to recompute self digests correctly.
    code_up=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import json
from scripts import survey_production_v2 as core
# proposal
prop_rel=r'sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/proposal.json'
prop=json.loads((Path(r'{dst}')/prop_rel).read_bytes().decode())
# proposal has proposed reader ref? Update if matches
for k in ["proposed","proposal"]:
    pass
# Find any dict with path == reader_rel and update sha
def walk(o):
    if isinstance(o, dict):
        if o.get("path")==r'{reader_rel}' and "sha256" in o:
            o["sha256"]=r'{new_sha}'
            # byte_count if present? proposal may not have byte_count
        for v in o.values(): walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
walk(prop)
(Path(r'{dst}')/prop_rel).write_bytes(core.json_bytes(prop))
# receipt reviewed_reader_input?
rec_rel=r'sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/validated-source-manifest.json'
rec=json.loads((Path(r'{dst}')/rec_rel).read_bytes().decode())
walk(rec)
# receipt has reviewed_reader_input? Check shape: reviewed_reader_input is ref? Update.
# Also receipt_sha recompute
tmp=dict(rec); tmp.pop('receipt_sha256', None)
rec['receipt_sha256']=core.sha256_object(tmp)
(Path(r'{dst}')/rec_rel).write_bytes(core.json_bytes(rec))
# seal reader-input + source-receipt
seal_rel=r'sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/publication-set.json'
seal=json.loads((Path(r'{dst}')/seal_rel).read_bytes().decode())
seal['roles']['reader-input']=dict(path=r'{reader_rel}', sha256=r'{new_sha}', byte_count={new_len})
# update source-receipt to fresh receipt
rec_p=Path(r'{dst}')/rec_rel
seal['roles']['source-receipt']=dict(path=rec_rel, sha256=core.sha256_bytes(rec_p.read_bytes()), byte_count=rec_p.stat().st_size)
tmp2=dict(seal); tmp2.pop('set_sha256', None)
seal['set_sha256']=core.sha256_object(tmp2)
(Path(r'{dst}')/seal_rel).write_bytes(core.json_bytes(seal))
print("forged reader fresh")
"""
    r_up=child_api(dst, code_up); assert r_up["exit"]==0, f"reader forgery update failed {r_up['stdout'][:800]} {r_up['stderr'][:800]}"
    state_rel=f"sources/{ISSUE_W}/production-state.json"; set_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/publication-set.json"
    code_v=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
from scripts import survey_editorial_publication_v2 as m
try:
    m.validate_prepared_set(Path(r'{dst}'), r'{state_rel}', r'{set_rel}')
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    out2=str(e); print(f"REFUSED: {{out2[:1500]}}")
    low=out2.lower()
    assert "digest" not in low or any(k in low for k in ["rederive","reader","author","propos","mismatch","scope","family"]), f"preempted {{out2[:1000]}}"
    assert any(k in low for k in ["reader","author","propos","rederive","mismatch","scope","family"]), f"no deep reader seam {{out2[:1000]}}"
    sys.exit(0)
"""
    r=child_api(dst, code_v); assert r["exit"]==0, f"deep reader should refuse deep {r['stdout'][:1500]}"
    log("A deep reader forged refused deep OK")

def a_equal_sha_wrong_path():
    dst=new_fault(INERT_W, "a-equal-sha-wrong-path")
    # same SHA different path: copy semantic review bytes to new path, point seal there with same SHA (fresh path, same SHA). Should refuse path, not SHA.
    import shutil as _sh
    sem_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/semantic-review-v2.json"
    new_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/semantic-review-forged.json"
    _sh.copy(str(dst/sem_rel), str(dst/new_rel))
    assert sha_file(dst/sem_rel)==sha_file(dst/new_rel)
    seal_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/publication-set.json"
    import json as _j
    seal=_j.loads((dst/seal_rel).read_bytes().decode())
    # point to new path with same SHA (so SHA passes, path must refuse)
    seal["roles"]["semantic-review"]={"path":new_rel,"sha256":seal["roles"]["semantic-review"]["sha256"],"byte_count":seal["roles"]["semantic-review"]["byte_count"]}
    (dst/seal_rel).write_bytes(json.dumps(seal, indent=2, sort_keys=True).encode()+b"\n")
    # Note: set_sha now stale (digest preemption) – to test path not digest, need fresh set_sha. Update via core.
    code_up=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import json
from scripts import survey_production_v2 as core
seal=json.loads((Path(r'{dst}')/r'{seal_rel}').read_bytes().decode())
tmp=dict(seal); tmp.pop('set_sha256', None)
seal['set_sha256']=core.sha256_object(tmp)
(Path(r'{dst}')/r'{seal_rel}').write_bytes(core.json_bytes(seal))
print("fresh set")
"""
    r_up=child_api(dst, code_up); assert r_up["exit"]==0
    state_rel=f"sources/{ISSUE_W}/production-state.json"
    code_v=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
from scripts import survey_editorial_publication_v2 as m
try:
    m.validate_prepared_set(Path(r'{dst}'), r'{state_rel}', r'{seal_rel}')
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    msg=str(e); print(f"REFUSED: {{msg[:1200]}}")
    low=msg.lower()
    assert "path" in low or "role" in low or "namespace" in low or "allowed" in low, f"expected path refusal, got {{msg[:1000]}}"
    sys.exit(0)
"""
    r=child_api(dst, code_v); assert r["exit"]==0, f"equal SHA wrong path should refuse path {r['stdout'][:1200]}"
    log("A equal SHA wrong path refused path OK")

def main():
    for n,f in [("A_state_clone_retained",a_state_clone_retained),("A_deep_research",a_deep_research),("A_deep_reader",a_deep_reader),("A_equal_sha_wrong_path",a_equal_sha_wrong_path)]:
        case(n,f)
    log(f"TOTAL A2 pass={PASS} fail={FAIL}")
    for n,s,d,det in CASES: log(f"SUMMARY {s} {n} dt={d:.1f}s {det[:200]}")
    (NOTES/"summary_a2.json").write_text(json.dumps({"pass":PASS,"fail":FAIL,"cases":[{"name":n,"status":s} for n,s,_,_ in CASES]}, indent=2))
    print(f"EXIT:{0 if FAIL==0 else 2}"); return 0 if FAIL==0 else 2
if __name__=="__main__":
    try: rc=main()
    except Exception: traceback.print_exc(); print("EXIT:2"); rc=2
    sys.exit(rc)
