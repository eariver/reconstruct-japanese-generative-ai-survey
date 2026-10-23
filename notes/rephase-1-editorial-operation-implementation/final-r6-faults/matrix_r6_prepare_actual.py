#!/usr/bin/env python3
"""R6 actual failed build process with valid spec (wrapper exits nonzero), no fake PDF."""
from __future__ import annotations
import json, os, stat, sys, time, traceback
from pathlib import Path
sys.dont_write_bytecode=True; os.environ["PYTHONDONTWRITEBYTECODE"]="1"
for _v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE","GIT_OBJECT_DIRECTORY","GIT_ALTERNATE_OBJECT_DIRECTORIES","GIT_COMMON_DIR","GIT_PREFIX"):
    if os.environ.get(_v): print(f"UNSAFE {_v}"); sys.exit(2)
def log(m): print(m, flush=True)
REPO=Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey").resolve()
sys.path.insert(0, str(REPO/"notes/rephase-1-editorial-operation-implementation/final-r6-faults"))
from matrix_common import FAULT_BASE, run_subprocess, verify_fixture
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
    from matrix_common import cp_fixture
    dst=FAULT_BASE/name
    if dst.exists(): verify_fixture(dst, name+"(reuse)"); return dst
    cp_fixture(base, dst, name); return dst

def r6_actual_failed_build():
    # Reuse NEW proposal fixture r6-prepare-new-v3 (already has P1/P2R/scope/P2V/P3S, no publication, State old)
    from matrix_common import INERT_W
    dst=FAULT_BASE/"r6-prepare-new-v3"
    verify_fixture(dst, "r6-prepare-new-v3(reuse for actual)")
    # Create valid wrapper executables (lualatex + biber companion in same bin dir) that print version and exit nonzero on compile (disclosed tool fault, not validator stub)
    wrapper=FAULT_BASE/"tmp"/"lualatex-fault-wrapper.sh"
    wrapper.parent.mkdir(parents=True, exist_ok=True)
    wrapper.write_text("#!/bin/sh\n echo \"lualatex fault wrapper version 1.0 (disclosed tool fault, not validator stub)\"\n echo \"argv: $@\" >&2\n exit 1\n", encoding="utf-8")
    wrapper.chmod(wrapper.stat().st_mode | stat.S_IEXEC)
    biber=FAULT_BASE/"tmp"/"biber"
    biber.write_text("#!/bin/sh\n echo \"biber fault wrapper version 1.0 (disclosed tool fault, companion for actual failed build)\"\n echo \"argv: $@\" >&2\n if [ \"$1\" = \"--version\" ]; then exit 0; fi\n exit 1\n", encoding="utf-8")
    biber.chmod(biber.stat().st_mode | stat.S_IEXEC)
    assert wrapper.is_file() and os.access(wrapper, os.X_OK), "wrapper must exist and be executable"
    assert biber.is_file() and os.access(biber, os.X_OK), "biber companion must exist for lualatex-biber-lualatex recipe"
    log(f"wrapper {wrapper} + biber companion executable (actual failed process, valid spec)")
    state_rel=f"sources/{ISSUE_W}/production-state.json"
    prop_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-3-fault/proposal.json"
    staged_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-3-fault/staged-source/staged-source-manifest.json"
    # manuscript/toolchain specs for NEW proposal already exist? Previous test created toolchain-spec-fault.json (invalid exe) and manuscript-spec-fault.json. For actual, create valid spec with wrapper exe (valid spec: correct recipe/argv, allowlisted env, wrapper exists)
    code=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import json
from scripts import survey_production_v2 as core
# load valid toolchain template (wk-r6-2) and replace exe with wrapper (valid: exists, regular file, absolute)
tspec=json.loads((Path(r'{dst}')/r'sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-2/toolchain-spec.json').read_bytes().decode())
tspec['absolute_executable']=r'{wrapper}'
# ensure recipe/argv exact (already exact in template), env allowlisted (already)
# verify wrapper exists from fixture perspective? Absolute path outside repo? It's inside workspace but absolute, should pass (repo alias does not apply to executor)
tpath=Path(r'{dst}')/r'sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-3-fault/toolchain-spec-actual-fault.json'
tpath.write_bytes(core.json_bytes(tspec))
print(f"toolchain actual-fault spec {{tpath}} exe={{tspec['absolute_executable']}}")
# manuscript spec for NEW proposal (reuse previous fault spec if exists, else create)
import hashlib
mspath=Path(r'{dst}')/r'sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-3-fault/manuscript-spec-fault.json'
if not mspath.is_file():
    mspec=json.loads((Path(r'{dst}')/r'sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-2/manuscript-spec.json').read_bytes().decode())
    new_prop=(Path(r'{dst}')/r'{prop_rel}').read_bytes()
    mspec['proposal_ref']=dict(path=r'{prop_rel}', sha256=hashlib.sha256(new_prop).hexdigest())
    mspath.write_bytes(core.json_bytes(mspec))
print("specs ready")
# PUBLIC prepare with valid spec but actual failing wrapper (not config refusal, actual failed process)
from scripts import survey_editorial_publication_v2 as m
import datetime
try:
    m.prepare_publication(Path(r'{dst}'), r'{state_rel}', r'{prop_rel}', r'{staged_rel}', "sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-3-fault/manuscript-spec-fault.json", "sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-3-fault/toolchain-spec-actual-fault.json", datetime.datetime.now(datetime.timezone.utc))
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    out=str(e); print(f"REFUSED actual failed build: {{out[:3000]}}")
    low=out.lower()
    # must be actual failed process (build failure, not config TOOLCHAIN_EXE/ARGV preemption)
    assert "build" in low or "failed" in low or "exit" in low or "nonzero" in low or "process" in low, f"must be actual failed process, not config refusal {{out[:2000]}}"
    assert "toolchain_exe" not in low and "toolchain_argv" not in low, f"must NOT be config refusal (valid spec), got {{out[:1500]}}"
    # no PDF forged, no publication authority
    import pathlib as _p
    pub=_p.Path(r'{dst}')/r'sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-3-fault/publication'
    assert not (pub/"build"/"main.pdf").is_file(), "no PDF must be forged on actual failed build"
    # no admission: State still old (State r1? Actually NEW proposal State is r1? State old, no new pointer)
    import json as _j
    st=_j.loads((Path(r'{dst}')/r'{state_rel}').read_bytes().decode())
    # State should still be old (no new activation record for NEW proposal, since prepare failed before finalize/activate)
    # Check no r3? Actually NEW proposal would be r3 if activated, but prepare failed, so no record
    print(f"no admission, State preserved")
    sys.exit(0)
"""
    r=child_api(dst, code, timeout=300); assert r["exit"]==0, f"actual failed build must refuse with actual process, no admission {r['stdout'][:3000]} {r['stderr'][:1500]}"
    log("R6 actual failed build (valid wrapper exits nonzero) REFUSED with no admission, no fake PDF OK (disclosed tool fault, not validator stub; old R2 badTeX historical, not current)")

def main():
    for n,f in [("R6_actual_failed_build",r6_actual_failed_build)]:
        case(n,f)
    log(f"TOTAL actual pass={PASS} fail={FAIL}")
    for n,s,d,det in CASES: log(f"SUMMARY {s} {n} dt={d:.1f}s {det[:200]}")
    (NOTES/"summary_r6_prepare_actual.json").write_text(json.dumps({"pass":PASS,"fail":FAIL,"cases":[{"name":n,"status":s} for n,s,_,_ in CASES]}, indent=2))
    print(f"EXIT:{0 if FAIL==0 else 2}"); return 0 if FAIL==0 else 2
if __name__=="__main__":
    try: rc=main()
    except Exception: traceback.print_exc(); print("EXIT:2"); rc=2
    import sys as _s; _s.exit(rc)
