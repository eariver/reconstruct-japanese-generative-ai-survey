#!/usr/bin/env python3
"""LONGFORM phases VALIDATED_DRAFT->RELEASED via normal public APIs.
Fresh Python per phase, 1200s timeout, raw fail preserved.
"""
import os, sys, json, subprocess, hashlib, time
from datetime import datetime, timezone
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
PARENT = REPO / ".rephase-1-editorial-runtime/versioned-renewal-longform-lifecycle-20261025T100000Z"
FIX = PARENT / "renewal-longform-lifecycle"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-state-lifecycle"
for k in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
    assert not os.environ.get(k), f"inherited {k}"
ENV=dict(os.environ); ENV["PYTHONDONTWRITEBYTECODE"]="1"; ENV["LC_ALL"]="C"
ENV["TMPDIR"]=str(PARENT/"tmp"); ENV["TMP"]=str(PARENT/"tmp"); ENV["TEMP"]=str(PARENT/"tmp")
TIMEOUT=1200
ISSUE="SP001"; PROP="lf-boot-1"; RID="high-u4-longform"
STATE_REL=f"sources/{ISSUE}/production-state.json"
PDIR=f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP}"
RDIR=f"{PDIR}/renewals/{RID}"
def run_tag(eviddir, tag, cmd, timeout=TIMEOUT, cwd=None):
    eviddir.mkdir(parents=True, exist_ok=True)
    if cwd is None:
        cwd=str(REPO)
    print(f"START {tag} PID={os.getpid()}", flush=True)
    t0=time.time()
    try:
        proc=subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, env=ENV)
    except subprocess.TimeoutExpired:
        dur=time.time()-t0
        (eviddir/f"{tag}-timeout.txt").write_text(f"timeout after {dur:.1f}s\n", encoding="utf-8")
        (eviddir/f"{tag}-exit.txt").write_text("TIMEOUT", encoding="utf-8")
        with open(eviddir/"commands.log","a",encoding="utf-8") as fh:
            fh.write(f"$ ... tag={tag} TIMEOUT dur={dur:.1f}s\n")
        print(f"TIMEOUT {tag}", flush=True)
        raise
    dur=time.time()-t0
    (eviddir/f"{tag}-stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (eviddir/f"{tag}-stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    (eviddir/f"{tag}-exit.txt").write_text(str(proc.returncode), encoding="utf-8")
    (eviddir/f"{tag}-dur.txt").write_text(f"{dur:.2f}\n", encoding="utf-8")
    (eviddir/f"{tag}-pid.txt").write_text(f"pid={os.getpid()} wall={datetime.now(timezone.utc).isoformat()}\n", encoding="utf-8")
    with open(eviddir/"commands.log","a",encoding="utf-8") as fh:
        fh.write(f"$ {' '.join(cmd[:8])}... tag={tag} -> exit={proc.returncode} dur={dur:.2f}s\n")
    print(f"DONE {tag} exit={proc.returncode} dur={dur:.2f}s", flush=True)
    return proc
def state_snapshot():
    s=FIX/STATE_REL
    d=json.loads(s.read_bytes())
    return d, hashlib.sha256(s.read_bytes()).hexdigest()
# Phase dirs
E1=EVID/"phase-validated-draft-20261025T101000Z"
E2=EVID/"phase-preview-20261025T102000Z"
E3=EVID/"phase-freeze-20261025T103000Z"
E4=EVID/"phase-release-20261025T104000Z"
E5=EVID/"phase-final-20261025T105000Z"
for e in [E1,E2,E3,E4,E5]:
    e.mkdir(parents=True, exist_ok=True)
    (e/"commands.log").write_text(f"{e.name} start {datetime.now(timezone.utc).isoformat()} PID={os.getpid()}\n", encoding="utf-8")
# Record wallclock distinct
run_tag(E1,"wall-before",["date","-u","+%Y-%m-%dT%H:%M:%SZ"])
# Verify before State still VALIDATED_DRAFT r7 pending, old lowlevel inert preserved
p=run_tag(E1,"before-state",[sys.executable,"-c","import json,hashlib,pathlib; r=pathlib.Path('"+str(FIX)+"'); s=r/'"+STATE_REL+"'; d=json.load(open(s)); print(json.dumps({'sha':hashlib.sha256(s.read_bytes()).hexdigest(),'lifecycle':d['lifecycle_state'],'machine':d['machine_checkpoints'],'human':d['human_gates'],'active':d['publication_revalidation_provenance']},indent=1))"])
assert p.returncode==0 and "VALIDATED_DRAFT" in p.stdout
p=run_tag(E1,"inert-preserved",[sys.executable,"-c","import pathlib; r=pathlib.Path('"+str(FIX)+"'); olds=[r/'"+PDIR+"/lifecycle-high-u3b-longform-direct/preview-approval.json', r/'"+PDIR+"/lifecycle-stage-high-u3b-longform-direct.json']; print([str(x.relative_to(r))+':'+str(x.exists()) for x in olds]); assert all(x.exists() for x in olds), 'old lowlevel inert must never delete'; print('INERT_PRESERVED')"])
assert p.returncode==0
p=run_tag(E1,"head-before",["git","-C",str(FIX),"rev-parse","HEAD"])
assert p.returncode==0 and p.stdout.strip()=="047f8adc0b7a7c005e03a8e2d374c1e5b6712b60"
# Need monotonic recorded_at >= r7 08:41:57
time.sleep(1)
now1=datetime.now(timezone.utc).isoformat()
(E1/"now-iso-phase1.txt").write_text(now1+"\n", encoding="utf-8")
print(f"PHASE1 now {now1}", flush=True)
# PHASE1: VALIDATED_DRAFT validate_stage + build_stage_checkpoint + advance to RELEASE_CANDIDATE (fresh child per public call)
PHASE1_CODE = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
root, state_rel, pdir, rdir, rid, now_iso = sys.argv[1:7]
from pathlib import Path
from datetime import datetime
import os
print(f"PHASE1 child PID={os.getpid()}", flush=True)
root_p = Path(root)
from scripts import survey_production_v2 as core
from scripts import survey_stage_validation_v2 as stage
from scripts import survey_agent_control_v2 as agent
from scripts import survey_publication_set_v2 as setmod
assert str(Path(core.__file__).resolve()).startswith(str(root_p.resolve())), "fixture origin"
cfg = json.loads((root_p / "config/survey-production-v2.json").read_bytes())
state_path = root_p / state_rel
state = json.loads(state_path.read_bytes())
print(f"before lifecycle={state['lifecycle_state']} pointer={state['publication_revalidation_provenance']['path']}", flush=True)
assert state["lifecycle_state"]=="VALIDATED_DRAFT"
# exact same active pointer role-aware Candidate resolves original C targets reused U4
expected = Path(setmod.resolve_publication_artifact_path(root_p, cfg, state, "publication-candidate"))
print(f"active candidate={expected.relative_to(root_p)}", flush=True)
# must be U4 reused C targets: high-u4 publication-candidate, whose roles point to high-c1 trio
seal = json.loads((root_p / f"{rdir}/publication-set.json").read_bytes())
cand_rel = seal["roles"]["publication-candidate"]["path"]
print(f"seal candidate={cand_rel}", flush=True)
assert str(expected.relative_to(root_p))==cand_rel, f"{expected} != {cand_rel}"
# verify U4 reuses C targets: candidate binds high-c1 trio
cand = json.loads((root_p / cand_rel).read_bytes())
print(f"candidate pdf={cand['pdf']['path']} manuscript={cand['reader_manuscript']['path']}", flush=True)
assert "high-c1-longform" in cand["pdf"]["path"] or "high-c1-longform" in cand["source"]["path"], "U4 must reuse original C targets"
# old producer proof history correctly: history chain 6, r7 active
from scripts import survey_versioned_renewal_history_v2 as hist
rec = state["publication_revalidation_provenance"]["path"]
v = hist.verify_versioned_history(str(root_p), rec)
print(f"history chain={v['chain_length']} refs={[r['record_sha'][:8] for r in v['observed_refs']]}", flush=True)
assert v["chain_length"]==6, v
# supplied
supplied = {"publication-candidate": expected}
now = datetime.fromisoformat(now_iso)
# canonical report/reviews paths (new, no collision)
report = root_p / "sources/SP001/orchestration/v2/reviews/VALIDATED_DRAFT-core-contract.json"
reviews_p = root_p / "sources/SP001/orchestration/v2/reviews/VALIDATED_DRAFT-reviews.json"
assert not report.exists(), f"canonical collides {report}"
assert not reviews_p.exists(), f"canonical collides {reviews_p}"
# stage.validate_stage actual report
stage.validate_stage(root_p, cfg, state_path, supplied, report, now)
print(f"stage report={report.relative_to(root_p)}", flush=True)
# reviews file with CORE_STAGE_CONTRACT deterministic
core.write_json(reviews_p, {"reviews":[{"check_id":"CORE_STAGE_CONTRACT","kind":"DETERMINISTIC","executor":"synthetic-longform-lifecycle-fixture","evidence":"actual stage validator PASS for exact selected U4 Candidate/PDF/gates agreement","result_path":str(report.relative_to(root_p))}]})
print(f"reviews={reviews_p.relative_to(root_p)}", flush=True)
# agent.build_stage_checkpoint and advance WITH checkpoint to RELEASE_CANDIDATE
cp = agent.build_stage_checkpoint(root_p, cfg, state_path, supplied, reviews_p, "Synthetic longform lifecycle VALIDATED_DRAFT exact U4 Candidate; NO genuine Human approval", now)
print(f"checkpoint={cp.relative_to(root_p)}", flush=True)
# canonical checkpoint path must be .../checkpoints/VALIDATED_DRAFT.json
canon = agent.canonical_checkpoint_path(root_p, cfg, json.loads(state_path.read_bytes()) if False else state)
print(f"canonical={canon.relative_to(root_p)}", flush=True)
updated = agent.advance_with_checkpoint(root_p, cfg, state_path, cp)
print(json.dumps({"lifecycle":updated["lifecycle_state"],"next":updated["next_action"],"terminal":updated["terminal_reason"]},indent=1), flush=True)
assert updated["lifecycle_state"]=="RELEASE_CANDIDATE"
# exact write window: State file SHA must have changed via allowed transition, history appended
print("PHASE1_OK", flush=True)
"""
p=run_tag(E1,"phase1-validated-draft",[sys.executable,"-c",PHASE1_CODE, str(FIX), STATE_REL, PDIR, RDIR, RID, now1])
print(open(E1/"phase1-validated-draft-stdout.txt").read()[:5000], flush=True)
print(open(E1/"phase1-validated-draft-stderr.txt").read()[:8000], flush=True)
if p.returncode!=0:
    print(f"FATAL PHASE1 blocked, exact source function/public input ref error above, not lowlevel PASS", flush=True)
    sys.exit(1)
# verify after phase1
p=run_tag(E1,"after-state",[sys.executable,"-c","import json,hashlib,pathlib; r=pathlib.Path('"+str(FIX)+"'); s=r/'"+STATE_REL+"'; d=json.load(open(s)); print(json.dumps({'sha':hashlib.sha256(s.read_bytes()).hexdigest(),'lifecycle':d['lifecycle_state'],'next':d['next_action'],'terminal':d['terminal_reason'],'machine':d['machine_checkpoints'],'human':d['human_gates']},indent=1))"])
assert p.returncode==0 and "RELEASE_CANDIDATE" in p.stdout
run_tag(E1,"wall-after",["date","-u","+%Y-%m-%dT%H:%M:%SZ"])
print("PHASE1 DONE", flush=True)
