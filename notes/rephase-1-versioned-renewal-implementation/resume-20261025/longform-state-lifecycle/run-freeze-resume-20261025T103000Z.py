#!/usr/bin/env python3
"""PHASE3 resume: reuse existing freeze/manifest (idempotence), then stage+checkpoint+advance to FROZEN."""
import os, sys, json, subprocess, time
from datetime import datetime, timezone
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
PARENT = REPO / ".rephase-1-editorial-runtime/versioned-renewal-longform-lifecycle-20261025T100000Z"
FIX = PARENT / "renewal-longform-lifecycle"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-state-lifecycle/phase-freeze-20261025T103000Z"
for k in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
    assert not os.environ.get(k)
ENV=dict(os.environ); ENV["PYTHONDONTWRITEBYTECODE"]="1"; ENV["LC_ALL"]="C"
ENV["TMPDIR"]=str(PARENT/"tmp"); ENV["TMP"]=str(PARENT/"tmp"); ENV["TEMP"]=str(PARENT/"tmp")
TIMEOUT=1200
ISSUE="SP001"; STATE_REL=f"sources/{ISSUE}/production-state.json"
def run_tag(tag, cmd, timeout=TIMEOUT):
    print(f"START {tag} PID={os.getpid()}", flush=True)
    t0=time.time()
    try:
        proc=subprocess.run(cmd, cwd=str(REPO), capture_output=True, text=True, timeout=timeout, env=ENV)
    except subprocess.TimeoutExpired:
        dur=time.time()-t0
        (EVID/f"{tag}-timeout.txt").write_text(f"timeout after {dur:.1f}s\n", encoding="utf-8")
        (EVID/f"{tag}-exit.txt").write_text("TIMEOUT", encoding="utf-8")
        raise
    dur=time.time()-t0
    (EVID/f"{tag}-stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (EVID/f"{tag}-stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    (EVID/f"{tag}-exit.txt").write_text(str(proc.returncode), encoding="utf-8")
    (EVID/f"{tag}-dur.txt").write_text(f"{dur:.2f}\n", encoding="utf-8")
    (EVID/f"{tag}-pid.txt").write_text(f"pid={os.getpid()} wall={datetime.now(timezone.utc).isoformat()}\n", encoding="utf-8")
    with open(EVID/"commands.log","a",encoding="utf-8") as fh:
        fh.write(f"$ {' '.join(cmd[:6])}... tag={tag} -> exit={proc.returncode} dur={dur:.2f}s\n")
    print(f"DONE {tag} exit={proc.returncode} dur={dur:.2f}s", flush=True)
    return proc
with open(EVID/"commands.log","a",encoding="utf-8") as fh:
    fh.write(f"PHASE3 resume start {datetime.now(timezone.utc).isoformat()} PID={os.getpid()}\n")
run_tag("wall-resume",["date","-u","+%Y-%m-%dT%H:%M:%SZ"])
time.sleep(1)
now3=datetime.now(timezone.utc).isoformat()
(EVID/"now-iso-phase3-resume.txt").write_text(now3+"\n", encoding="utf-8")
print(f"PHASE3 resume now {now3}", flush=True)
CODE = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
root, state_rel, now_iso = sys.argv[1:4]
from pathlib import Path
from datetime import datetime
import os
print(f"PHASE3 resume child PID={os.getpid()}", flush=True)
root_p = Path(root)
from scripts import survey_production_v2 as core
from scripts import survey_stage_validation_v2 as stage
from scripts import survey_agent_control_v2 as agent
from scripts import survey_profiled_freeze_v2 as pfreeze
from scripts import survey_publication_v2 as pubmod
from scripts import survey_publication_set_v2 as setmod
assert str(Path(core.__file__).resolve()).startswith(str(root_p.resolve())), "fixture origin"
cfg = json.loads((root_p / "config/survey-production-v2.json").read_bytes())
state_path = root_p / state_rel
state = json.loads(state_path.read_bytes())
print(f"before lifecycle={state['lifecycle_state']}", flush=True)
assert state["lifecycle_state"]=="RELEASE_CANDIDATE"
now = datetime.fromisoformat(now_iso)
# reuse existing freeze/manifest with idempotence check (no overwrite, known same bytes)
freeze_path = root_p / "sources/SP001/publication/v2/freeze-record-v2.json"
manifest_path = root_p / "sources/SP001/publication/v2/release-manifest-v2.json"
assert freeze_path.exists() and manifest_path.exists(), "freeze/manifest must exist from prior attempt"
print(f"reuse freeze={freeze_path.relative_to(root_p)} manifest={manifest_path.relative_to(root_p)}", flush=True)
# verify they bind exact U4 candidate and approval (State-bound)
cand_path = Path(setmod.resolve_publication_artifact_path(root_p, cfg, json.loads(state_path.read_bytes()), "publication-candidate"))
cand = pubmod.validate_candidate(root_p, cand_path, issue_id=state["issue_id"])
print(f"candidate={cand_path.relative_to(root_p)} pdf={cand['pdf']['sha256'][:12]}", flush=True)
freeze = pubmod.validate_release_manifest(root_p, manifest_path)  # also validates freeze linkage
# check freeze binds candidate/approval/visual
import json as _j
fr = _j.loads(freeze_path.read_bytes())
assert fr["publication_candidate_path"]==str(cand_path.relative_to(root_p)), fr
assert fr["publication_candidate_sha256"]==core.sha256_file(cand_path)
print(f"freeze binds candidate OK frozen_at={fr['frozen_at']}", flush=True)
# ensure recorded_at >= freeze frozen_at and >= r7
assert now_iso >= fr["frozen_at"], f"{now_iso} < {fr['frozen_at']}"
print(f"chrono now {now_iso} >= frozen {fr['frozen_at']} OK", flush=True)
visual_path = root_p / cand["visual_review"]["path"]
supplied = {"freeze-record": freeze_path, "release-manifest": manifest_path, "visual-review-record": visual_path}
report = root_p / "sources/SP001/orchestration/v2/reviews/RELEASE_CANDIDATE-core-contract.json"
reviews_p = root_p / "sources/SP001/orchestration/v2/reviews/RELEASE_CANDIDATE-reviews.json"
# these must not exist yet (no collision); if they exist from killed attempt, check idempotence or fail
if report.exists() or reviews_p.exists():
    print(f"report exists={report.exists()} reviews exists={reviews_p.exists()} -> checking idempotence, not overwriting", flush=True)
    # if both exist, verify they are valid for current State/supplied, else blocker
    if report.exists():
        print(f"existing report sha={core.sha256_file(report)[:12]}", flush=True)
    raise SystemExit("BLOCKER: canonical report collides, need manual idempotence check, not overwriting")
stage.validate_stage(root_p, cfg, state_path, supplied, report, now)
print(f"stage report={report.relative_to(root_p)}", flush=True)
core.write_json(reviews_p, {"reviews":[{"check_id":"CORE_STAGE_CONTRACT","kind":"DETERMINISTIC","executor":"synthetic-longform-lifecycle-fixture","evidence":"actual stage guard PASS for profiled Freeze exact U4 Candidate/PDF/gates","result_path":str(report.relative_to(root_p))}]})
print(f"reviews={reviews_p.relative_to(root_p)}", flush=True)
cp = agent.build_stage_checkpoint(root_p, cfg, state_path, supplied, reviews_p, "Synthetic longform lifecycle profiled Freeze exact U4 Candidate; NO genuine Human approval", now)
print(f"checkpoint={cp.relative_to(root_p)}", flush=True)
updated = agent.advance_with_checkpoint(root_p, cfg, state_path, cp)
print(_j.dumps({"lifecycle":updated["lifecycle_state"],"machine_freeze":updated["machine_checkpoints"]["freeze"],"next":updated["next_action"],"terminal":updated["terminal_reason"]},indent=1), flush=True)
assert updated["lifecycle_state"]=="FROZEN"
print("PHASE3_RESUME_OK", flush=True)
"""
p=run_tag("phase3-freeze-resume",[sys.executable,"-c",CODE, str(FIX), STATE_REL, now3])
print(open(EVID/"phase3-freeze-resume-stdout.txt").read()[:8000] if (EVID/"phase3-freeze-resume-stdout.txt").exists() else "no stdout", flush=True)
print(open(EVID/"phase3-freeze-resume-stderr.txt").read()[:8000] if (EVID/"phase3-freeze-resume-stderr.txt").exists() else "no stderr", flush=True)
if p.returncode!=0:
    print("FATAL PHASE3 resume blocked exact source function/public input ref above", flush=True)
    sys.exit(1)
p=run_tag("after-state-resume",[sys.executable,"-c","import json,hashlib,pathlib; r=pathlib.Path('"+str(FIX)+"'); s=r/'"+STATE_REL+"'; d=json.load(open(s)); print(json.dumps({'sha':hashlib.sha256(s.read_bytes()).hexdigest(),'lifecycle':d['lifecycle_state'],'machine':d['machine_checkpoints']},indent=1))"])
assert p.returncode==0 and "FROZEN" in p.stdout
run_tag("wall-after-resume",["date","-u","+%Y-%m-%dT%H:%M:%SZ"])
print("PHASE3 RESUME DONE", flush=True)
