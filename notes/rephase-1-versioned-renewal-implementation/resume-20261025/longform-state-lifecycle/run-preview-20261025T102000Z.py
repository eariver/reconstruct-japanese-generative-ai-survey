#!/usr/bin/env python3
"""PHASE2 synthetic public agent Preview approval exact selected U4 Candidate/PDF/gates agreement."""
import os, sys, json, subprocess, time
from datetime import datetime, timezone
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
PARENT = REPO / ".rephase-1-editorial-runtime/versioned-renewal-longform-lifecycle-20261025T100000Z"
FIX = PARENT / "renewal-longform-lifecycle"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-state-lifecycle/phase-preview-20261025T102000Z"
EVID.mkdir(parents=True, exist_ok=True)
if (EVID/"commands.log").exists():
    pass
else:
    (EVID/"commands.log").write_text("", encoding="utf-8")
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
        with open(EVID/"commands.log","a",encoding="utf-8") as fh:
            fh.write(f"$ ... tag={tag} TIMEOUT\n")
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
    fh.write(f"PHASE2 start {datetime.now(timezone.utc).isoformat()} PID={os.getpid()}\n")
run_tag("wall-before",["date","-u","+%Y-%m-%dT%H:%M:%SZ"])
p=run_tag("before-state",[sys.executable,"-c","import json,hashlib,pathlib; r=pathlib.Path('"+str(FIX)+"'); s=r/'"+STATE_REL+"'; d=json.load(open(s)); print(json.dumps({'sha':hashlib.sha256(s.read_bytes()).hexdigest(),'lifecycle':d['lifecycle_state'],'human':d['human_gates'],'machine':d['machine_checkpoints']},indent=1))"])
assert p.returncode==0 and "RELEASE_CANDIDATE" in p.stdout and "pending" in p.stdout
time.sleep(1)
now2=datetime.now(timezone.utc).isoformat()
(EVID/"now-iso-phase2.txt").write_text(now2+"\n", encoding="utf-8")
print(f"PHASE2 now {now2}", flush=True)
CODE = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
root, state_rel, now_iso = sys.argv[1:4]
from pathlib import Path
from datetime import datetime
import os
print(f"PHASE2 child PID={os.getpid()}", flush=True)
root_p = Path(root)
from scripts import survey_production_v2 as core
from scripts import survey_agent_control_v2 as agent
from scripts import survey_publication_v2 as pubmod
from scripts import survey_publication_set_v2 as setmod
assert str(Path(core.__file__).resolve()).startswith(str(root_p.resolve())), "fixture origin"
cfg = json.loads((root_p / "config/survey-production-v2.json").read_bytes())
state_path = root_p / state_rel
state = json.loads(state_path.read_bytes())
print(f"before lifecycle={state['lifecycle_state']} preview={state['human_gates']['publication_preview']}", flush=True)
assert state["lifecycle_state"]=="RELEASE_CANDIDATE" and state["human_gates"]["publication_preview"]=="pending"
# exact selected U4 Candidate/PDF/gates agreement via shared resolver
cand_path = Path(setmod.resolve_publication_artifact_path(root_p, cfg, state, "publication-candidate"))
print(f"active candidate={cand_path.relative_to(root_p)}", flush=True)
cand = pubmod.validate_candidate(root_p, cand_path, issue_id=state["issue_id"])
print(f"candidate pdf={cand['pdf']['path']} sha={cand['pdf']['sha256'][:12]} visual={cand['visual_review']['path']}", flush=True)
# synthetic public agent Preview approval exact selected U4 Candidate/PDF/gates agreement, explicit non-genuine
now = datetime.fromisoformat(now_iso)
updated = agent.approve_publication_preview(root_p, cfg, state_path, "synthetic-longform-lifecycle-fixture; NO genuine Human approval; content quality NO-GO, not creating Production release", now, "synthetic:longform-lifecycle:preview:high-u4")
print(json.dumps({"lifecycle":updated["lifecycle_state"],"human":updated["human_gates"],"machine_preview":updated["machine_checkpoints"]["publication_preview"],"next":updated["next_action"],"terminal":updated["terminal_reason"]},indent=1), flush=True)
assert updated["lifecycle_state"]=="RELEASE_CANDIDATE"
assert updated["human_gates"]["publication_preview"]=="approved"
assert updated["machine_checkpoints"]["publication_preview"]=="passed"
# verify approval binds exact candidate PDF
appr_ref = updated["human_gate_provenance"]["publication_preview"]
print(f"approval={appr_ref}", flush=True)
appr = pubmod.validate_preview_approval(root_p, root_p / appr_ref["path"], issue_id=state["issue_id"])
print(f"approval pdf={appr['pdf_sha256'][:12]} candidate={appr['publication_candidate_path']}", flush=True)
assert appr["publication_candidate_sha256"]==core.sha256_file(cand_path)
assert appr["pdf_sha256"]==cand["pdf"]["sha256"]
print("PHASE2_OK", flush=True)
"""
p=run_tag("phase2-preview",[sys.executable,"-c",CODE, str(FIX), STATE_REL, now2])
print(open(EVID/"phase2-preview-stdout.txt").read()[:5000], flush=True)
print(open(EVID/"phase2-preview-stderr.txt").read()[:8000], flush=True)
if p.returncode!=0:
    print("FATAL PHASE2 blocked exact source function/public input ref above", flush=True)
    sys.exit(1)
p=run_tag("after-state",[sys.executable,"-c","import json,hashlib,pathlib; r=pathlib.Path('"+str(FIX)+"'); s=r/'"+STATE_REL+"'; d=json.load(open(s)); print(json.dumps({'sha':hashlib.sha256(s.read_bytes()).hexdigest(),'lifecycle':d['lifecycle_state'],'human':d['human_gates'],'machine':d['machine_checkpoints'],'approval':d['human_gate_provenance']['publication_preview']},indent=1))"])
assert p.returncode==0 and "approved" in p.stdout
run_tag("wall-after",["date","-u","+%Y-%m-%dT%H:%M:%SZ"])
print("PHASE2 DONE", flush=True)
