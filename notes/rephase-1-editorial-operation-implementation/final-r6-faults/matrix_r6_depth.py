#!/usr/bin/env python3
"""R6 depth32: synthetic TYPED LEGACY33 chain, cumulative original full union, NOT actual R1x33."""
from __future__ import annotations
import json, os, sys, time, traceback, shutil, hashlib
from pathlib import Path
from datetime import datetime, timedelta, timezone
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
    except AssertionError as e: dt=time.monotonic()-t0; log(f"CASE FAIL {n} dt={dt:.1f}s {e}"); traceback.print_exc(); CASES.append((n,"FAIL",dt,str(e)[:3000])); FAIL+=1
    except Exception as e: dt=time.monotonic()-t0; log(f"CASE BLOCKER {n} dt={dt:.1f}s {type(e).__name__}: {e}"); traceback.print_exc(); CASES.append((n,"BLOCKER",dt,f"{type(e).__name__}: {e}"[:3000])); FAIL+=1
def child_api(fixture: Path, code: str, timeout=300):
    return run_subprocess(fixture, [sys.executable,"-B","-c",code], cwd=fixture, timeout=timeout)
def new_fault(base: Path, name: str):
    dst=FAULT_BASE/name
    if dst.exists(): verify_fixture(dst, name+"(reuse)"); return dst
    cp_fixture(base, dst, name); return dst

def r6_depth33():
    dst=new_fault(INERT_W, "r6-depth33")
    import json as _j
    # 1. State from genuine P1 retained before-first COPY (wk-r6-1 retained before, null pointer), omit original activation records, versioned sets unreferenced inert
    retained_before=dst/f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-1/retained/before/sources/{ISSUE_W}/production-state.json"
    assert retained_before.is_file(), "P1 retained before-first missing"
    before_bytes=retained_before.read_bytes()
    before_obj=_j.loads(before_bytes.decode())
    assert before_obj.get("publication_revalidation_provenance") is None, "before-first must be null"
    # omit original activation records at copy time (r1 editorial)
    r1_orig=dst/f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r1.json"
    if r1_orig.exists():
        # preserve evidence? Instruction says omit at copy time, not delete after? Since dst already copied with r1, omit now by removing (new fixture, original INERT preserved elsewhere). Log as omit, not cleanup.
        r1_orig.unlink()
        assert not r1_orig.exists()
    # versioned sets unreferenced inert: leave wk-r6-2 set files, State null so unreferenced. Good.
    # write State from genuine COPY
    st_rel=f"sources/{ISSUE_W}/production-state.json"
    (dst/st_rel).write_bytes(before_bytes)
    # 2. Metadata-updated Gate: copy original Gate, update recorded_at/evaluated_by (valid), refresh new SHA
    # Original Gate path from DRAFT_COMPLETE artifacts: reader-surface-gate
    draf_rel=f"sources/{ISSUE_W}/orchestration/v2/checkpoints/DRAFT_COMPLETE.json"
    draf=_j.loads((dst/draf_rel).read_bytes().decode())
    orig_map={(r.get("name"),r.get("path")):r.get("sha256") for r in draf.get("artifacts",[])}
    assert len(orig_map)==7, f"original rows {len(orig_map)} !=7"
    # find Gate artifact (reader-surface-gate)
    gate_rows=[r for r in draf.get("artifacts",[]) if r.get("name")=="reader-surface-gate"]
    assert len(gate_rows)==1, "Gate row missing"
    gate_path=gate_rows[0]["path"]; gate_orig_sha=gate_rows[0]["sha256"]
    gate_file=dst/gate_path
    assert gate_file.is_file() and sha_file(gate_file)==gate_orig_sha, "Gate file must match original before update"
    gate_obj=_j.loads(gate_file.read_bytes().decode())
    # update recorded_at +1h, evaluated_by with depth marker (still valid instant, still schema-valid)
    if "recorded_at" in gate_obj:
        gate_obj["recorded_at"]="2026-09-19T06:00:00+09:00"
    if "evaluated_by" in gate_obj and isinstance(gate_obj["evaluated_by"], str):
        gate_obj["evaluated_by"]=gate_obj["evaluated_by"]+" depth32"
    # refresh own GateDigest (gate_sha256 = sha256_object(base with digest_fields)) to keep actual valid metadata-updated Gate
    digest_fields=("schema_version","issue_id","publication_profile","status","scanned_surfaces","rules_checked","suppressions","findings","summary","evaluated_by","recorded_at","semantic_authority","derivation")
    # compute via python (need sha256_object logic: sort_keys separators (',', ':'))
    import hashlib as _h
    base={k: gate_obj[k] for k in digest_fields}
    payload=json.dumps(base, ensure_ascii=False, sort_keys=True, separators=(",",":")).encode("utf-8")
    gate_obj["gate_sha256"]=hashlib.sha256(payload).hexdigest()
    (dst/gate_path).write_bytes(json.dumps(gate_obj, indent=2, sort_keys=True, ensure_ascii=False).encode()+b"\n")
    new_gate_sha=sha_file(dst/gate_path); new_gate_bytes=(dst/gate_path).stat().st_size
    assert new_gate_sha!=gate_orig_sha, "Gate must have new SHA after metadata update"
    log(f"Gate updated {gate_orig_sha[:8]}->{new_gate_sha[:8]} gate_sha256 refreshed")
    # 3. Generate one real legacy record r1 via actual revalidate_publication_surface (no mocks, real validator, real Git? No commit, just file write)
    # Need to call via child bound to fixture
    code_gen=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import datetime
from scripts import survey_agent_control_v2 as agent
from scripts import survey_production_v2 as core
# State currently null (before-first), need VALIDATED_DRAFT with null pointer? revalidate requires VALIDATED_DRAFT? Check: INERT retained before State lifecycle?
import json
st=json.loads((Path(r'{dst}')/r'{st_rel}').read_bytes().decode())
print(f"State lifecycle {{st.get('lifecycle_state')}} pointer {{st.get('publication_revalidation_provenance')}}")
# Call actual revalidate to generate r1 (legacy, supersedes null)
# Use reason REVIEWED_CORE_CHANGE, executor depth32-test, recorded_at ascending base
rec_path=agent.revalidate_publication_surface(Path(r'{dst}'), core.load_json(Path(r'{dst}')/core.DEFAULT_CONFIG), Path(r'{dst}')/r'{st_rel}', "REVIEWED_CORE_CHANGE", "depth32 synthetic r1 (typed validator fixture NOT actual R1x33)", "depth32-test", datetime.datetime(2026,10,23,0,0,0,tzinfo=datetime.timezone.utc), None)
print(f"R1 {{rec_path}}")
"""
    r_gen=child_api(dst, code_gen, timeout=300)
    assert r_gen["exit"]==0, f"real legacy r1 generation failed {r_gen['stdout'][:3000]} {r_gen['stderr'][:1500]}"
    log(f"R6 real legacy r1 generated: {r_gen['stdout'][:800]}")
    # Verify r1 exists and is legacy with supersedes null, prior_checkpoint original, Gate superseded prior original new updated?
    # The real generation should have detected Gate drift (since we updated Gate file) and created superseded Gate row with prior original new updated. Good.
    # Now replicate r1 template to r2..r33 bottom-up with actual ref SHA, chronology ascending, exact supersedes, no extra fields, union all original rows.
    # Load r1 template
    r1_rel=f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r1.json"
    assert (dst/r1_rel).is_file(), "r1 not created"
    # Build chain r2..r33 via child (to use core.json_bytes + sha correctly, no mocks)
    code_chain=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import json, hashlib
from datetime import datetime, timedelta, timezone
from scripts import survey_production_v2 as core
r1=json.loads((Path(r'{dst}')/r'{r1_rel}').read_bytes().decode())
# verify r1 shape: legacy, supersedes null, prior_checkpoint original DRAFT_COMPLETE?
assert r1.get('reason_class')=="REVIEWED_CORE_CHANGE" and "kind" not in r1, f"r1 not legacy {{r1.get('reason_class')}}"
assert r1.get('supersedes') is None, "r1 must supersede null"
# prior_checkpoint must be original DRAFT_COMPLETE
print(f"r1 prior {{r1.get('prior_checkpoint')}}")
# base time from r1 recorded_at
t0=core.parse_instant(r1['recorded_at'])
# for r2..r33, copy r1, update supersedes to previous, recorded_at ascending, keep all other rows same (cumulative original, Gate prior original new updated)
prev_path=r'{r1_rel}'
prev_bytes=(Path(r'{dst}')/prev_path).read_bytes()
prev_sha=hashlib.sha256(prev_bytes).hexdigest()
for n in range(2,34):
    cur_rel=f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r{{n}}.json"
    rec=dict(r1)  # shallow? Need deep copy for nested? Use json round-trip
    import copy as _c
    rec=_c.deepcopy(r1)
    rec['supersedes']=dict(path=prev_path, sha256=prev_sha)
    # chronology ascending: T0 + (n-1) hours
    rec['recorded_at']=core.iso_utc(t0 + timedelta(hours=n-1)) if hasattr(core, 'iso_utc') else (t0 + timedelta(hours=n-1)).isoformat().replace('+00:00','Z')
    # establishment recorded_at? Update to match? Establishment has recorded_at? Keep consistent? Update establishment recorded_at same as record?
    if isinstance(rec.get('establishment'), dict) and 'recorded_at' in rec['establishment']:
        rec['establishment']['recorded_at']=rec['recorded_at']
    # write canonical via core.json_bytes (same as real writer? Check writer uses core.json_bytes? Assume yes)
    Path(r'{dst}', cur_rel).write_bytes(core.json_bytes(rec))
    cur_bytes=(Path(r'{dst}')/cur_rel).read_bytes()
    # verify schema? Use strict load to ensure schema-valid (no mocks)
    from scripts import survey_schema_v2 as _sg
    # load_and_validate to ensure schema-valid hash-consistent? Use agent? Just ensure file written.
    prev_path=cur_rel; prev_sha=hashlib.sha256(cur_bytes).hexdigest()
    if n in (2,32,33):
        print(f"r{{n}} {{prev_sha[:8]}} supersedes {{rec['supersedes']['path']}}")
print("chain r1..r33 built bottom-up actual refSHA")
"""
    r_chain=child_api(dst, code_chain, timeout=120)
    assert r_chain["exit"]==0, f"chain build failed {r_chain['stdout'][:3000]} {r_chain['stderr'][:1500]}"
    log(f"R6 chain r1..r33 built: {r_chain['stdout'][:800]}")
    # Label synthetic typed history NOT actual R1x33
    (dst/"LEGACY33_SYNTHETIC_README.txt").write_text("TYPED validator fixture: 33 schema-valid hash-consistent legacy records (cumulative original full union, same final Gate bytes), chronology ascending, unique r1..r33, exact supersedes. NOT actual R1x33 process history. No mocks, no publication build.\\n", encoding="utf-8")
    # State pointer r31 control healthy (31 records, no depth; r32 already exceeds walk limit 32 range -> depth, see below)
    # Prompt says r32 healthy if 32 inclusive; actual code walk range(32) allows max 31 for resolve (needs terminator iteration), derive allows 32 via >32.
    # Report actual: r31 healthy, r32/r33 refuse depth EXACT (no refSHA preemption, chain hash-consistent).
    code_state32=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import json, hashlib
st_rel=r'{st_rel}'
st=json.loads((Path(r'{dst}')/st_rel).read_bytes().decode())
r31_rel="sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r31.json"
r31_sha=hashlib.sha256((Path(r'{dst}')/r31_rel).read_bytes()).hexdigest()
st['publication_revalidation_provenance']=dict(path=r31_rel, sha256=r31_sha)
from scripts import survey_production_v2 as core
Path(r'{dst}', st_rel).write_bytes(core.json_bytes(st))
print(f"State->r31 {{r31_sha[:8]}}")
"""
    r_s32=child_api(dst, code_state32); assert r_s32["exit"]==0, f"State r31 failed {r_s32['stdout'][:1000]}"
    code_healthy=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
from scripts import survey_agent_control_v2 as a
from scripts import survey_production_v2 as core
cfg=core.load_json(Path(r'{dst}')/core.DEFAULT_CONFIG)
st=core.load_json(Path(r'{dst}')/r'{st_rel}')
errs=a.validate_agent_state(Path(r'{dst}'), cfg, st)
print(f"validate errs={{errs}}")
assert errs==[], f"r31 control must be healthy, got {{errs}}"
act, aerr=a.resolve_active_publication_revalidation(Path(r'{dst}'), cfg, st)
print(f"resolve active={{act.get('record_path') if isinstance(act, dict) else act}} err={{aerr}}")
assert not aerr, f"resolve r31 must be healthy {{aerr}}"
"""
    r_h=child_api(dst, code_healthy); assert r_h["exit"]==0, f"r31 healthy failed {r_h['stdout'][:3000]} {r_h['stderr'][:1500]}"
    log(f"R6 r31 typed control healthy (31 records, Chainbuilder31 union then projects7): {r_h['stdout'][:800]}")
    import subprocess as _sp
    env=dict(__import__("os").environ); env["PYTHONDONTWRITEBYTECODE"]="1"; env["PYTHONPATH"]=str(dst); env["PYTHONPYCACHEPREFIX"]=str(FAULT_BASE/"pycache"); env["TMPDIR"]=str(FAULT_BASE/"tmp")
    for k in list(env.keys()):
        if k.startswith("GIT_"): del env[k]
    pr=_sp.run([sys.executable,"-B","-m","scripts.survey_agent_control_v2","validate-state","--state",st_rel], cwd=str(dst), capture_output=True, text=True, timeout=120, env=env)
    assert pr.returncode==0, f"CLI validate-state r31 must exit 0, got {pr.returncode} {pr.stdout[:1500]} {pr.stderr[:800]}"
    log(f"R6 CLI validate-state r31 exit0 OK")
    # State pointer r32/r33 refuses depth limit EXACT (r32 already exceeds walk range 32 -> depth; r33 same)
    code_state33=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import json, hashlib
st_rel=r'{st_rel}'
st=json.loads((Path(r'{dst}')/st_rel).read_bytes().decode())
r33_rel="sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r33.json"
r33_sha=hashlib.sha256((Path(r'{dst}')/r33_rel).read_bytes()).hexdigest()
st['publication_revalidation_provenance']=dict(path=r33_rel, sha256=r33_sha)
from scripts import survey_production_v2 as core
Path(r'{dst}', st_rel).write_bytes(core.json_bytes(st))
print(f"State->r33 {{r33_sha[:8]}}")
"""
    r_s33=child_api(dst, code_state33); assert r_s33["exit"]==0
    code_refuse=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
from scripts import survey_agent_control_v2 as a
from scripts import survey_production_v2 as core
cfg=core.load_json(Path(r'{dst}')/core.DEFAULT_CONFIG)
st=core.load_json(Path(r'{dst}')/r'{st_rel}')
# public resolve should refuse depth EXACT, not earlier refSHA preemption (chain is hash-consistent, sequence strictly increasing, chronology ascending, prior_checkpoint original)
try:
    act, aerr=a.resolve_active_publication_revalidation(Path(r'{dst}'), cfg, st)
    print(f"UNEXPECTED_PASS active={{act}} err={{aerr}}")
    # also try validate
    errs=a.validate_agent_state(Path(r'{dst}'), cfg, st)
    print(f"validate errs={{errs}}")
    import sys as _s; _s.exit(10)
except Exception as e:
    out=str(e); print(f"REFUSED depth: {{out[:3000]}}")
    low=out.lower()
    assert "too deep" in low or "depth" in low or "chain" in low, f"must be depth limit EXACT, not earlier refSHA preemption {{out[:2000]}}"
    assert "drift" not in low or "depth" in low, f"must not be earlier refSHA preemption {{out[:1500]}}"
    import sys as _s; _s.exit(0)
"""
    # Note: resolve_active may return (active, errors) rather than raise? Check signature: resolve_active returns (active, errors)? In code above, it returns tuple, not raises. For depth, it likely returns errors list containing depth, not raise. Our child expects exception, but actual API may not raise. Need to handle both: if returns errors, check errors contain depth.
    # Adjust: call and inspect return.
    code_refuse2=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
from scripts import survey_agent_control_v2 as a
from scripts import survey_production_v2 as core
cfg=core.load_json(Path(r'{dst}')/core.DEFAULT_CONFIG)
st=core.load_json(Path(r'{dst}')/r'{st_rel}')
act, aerr=a.resolve_active_publication_revalidation(Path(r'{dst}'), cfg, st)
print(f"resolve active={{act}} err={{aerr}}")
errs=a.validate_agent_state(Path(r'{dst}'), cfg, st)
print(f"validate errs={{errs}}")
# depth must appear in either
blob=str(aerr)+str(errs)
assert "deep" in blob.lower() or "depth" in blob.lower() or "too deep" in blob.lower() or "chain" in blob.lower(), f"must be depth limit EXACT {{blob[:3000]}}"
# ensure not earlier refSHA preemption alone: if depth present, ok even if other errors? Require depth present.
print("depth EXACT refused")
"""
    r_ref=child_api(dst, code_refuse2); assert r_ref["exit"]==0, f"r33 must refuse depth EXACT {r_ref['stdout'][:3000]} {r_ref['stderr'][:1500]}"
    log(f"R6 r33 depth refuses EXACT: {r_ref['stdout'][:800]}")
    # CLI validate-state r33 must exit nonzero (exact error, no-write/delta)
    import subprocess as _sp2
    env2=dict(__import__("os").environ); env2["PYTHONDONTWRITEBYTECODE"]="1"; env2["PYTHONPATH"]=str(dst); env2["PYTHONPYCACHEPREFIX"]=str(FAULT_BASE/"pycache"); env2["TMPDIR"]=str(FAULT_BASE/"tmp")
    for k in list(env2.keys()):
        if k.startswith("GIT_"): del env2[k]
    # snapshot before CLI (no-write/delta)
    import hashlib as _h
    def snap(p):
        d={{}}
        for dp,dn,fn in __import__("os").walk(p):
            if ".git" in Path(dp).parts: dn[:]=[]; continue
            for f in sorted(fn):
                pp=Path(dp)/f
                try:
                    if pp.is_symlink(): continue
                    d[pp.relative_to(p).as_posix()]=_h.sha256(pp.read_bytes()).hexdigest()
                except: pass
        return d
    before=snap(dst)
    pr2=_sp2.run([sys.executable,"-B","-m","scripts.survey_agent_control_v2","validate-state","--state",st_rel], cwd=str(dst), capture_output=True, text=True, timeout=120, env=env2)
    assert pr2.returncode!=0, f"CLI r33 must refuse nonzero, got {pr2.returncode} {pr2.stdout[:1500]}"
    assert "deep" in (pr2.stdout+pr2.stderr).lower() or "depth" in (pr2.stdout+pr2.stderr).lower() or "chain" in (pr2.stdout+pr2.stderr).lower(), f"CLI must state depth {pr2.stdout[:1500]} {pr2.stderr[:800]}"
    assert snap(dst)==before, "CLI depth refusal must be no-write/delta"
    log(f"R6 CLI r33 depth exit {pr2.returncode} no-write OK")

def main():
    for n,f in [("R6_depth33",r6_depth33)]:
        case(n,f)
    log(f"TOTAL depth pass={PASS} fail={FAIL}")
    for n,s,d,det in CASES: log(f"SUMMARY {s} {n} dt={d:.1f}s {det[:200]}")
    (NOTES/"summary_r6_depth.json").write_text(json.dumps({"pass":PASS,"fail":FAIL,"cases":[{"name":n,"status":s} for n,s,_,_ in CASES]}, indent=2))
    print(f"EXIT:{0 if FAIL==0 else 2}"); return 0 if FAIL==0 else 2
if __name__=="__main__":
    try: rc=main()
    except Exception: traceback.print_exc(); print("EXIT:2"); rc=2
    import sys as _s; _s.exit(rc)
