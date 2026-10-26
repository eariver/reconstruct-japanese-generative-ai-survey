#!/usr/bin/env python3
"""PHASE4 offline synthetic merge/release evidence then normal checkpoint/advance to RELEASED."""
import os, sys, json, subprocess, time
from datetime import datetime, timezone
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
PARENT = REPO / ".rephase-1-editorial-runtime/versioned-renewal-longform-lifecycle-20261025T100000Z"
FIX = PARENT / "renewal-longform-lifecycle"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-state-lifecycle/phase-release-20261025T104000Z"
EVID.mkdir(parents=True, exist_ok=True)
if not (EVID/"commands.log").exists():
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
    fh.write(f"PHASE4 start {datetime.now(timezone.utc).isoformat()} PID={os.getpid()}\n")
run_tag("wall-before",["date","-u","+%Y-%m-%dT%H:%M:%SZ"])
p=run_tag("before-state",[sys.executable,"-c","import json,hashlib,pathlib; r=pathlib.Path('"+str(FIX)+"'); s=r/'"+STATE_REL+"'; d=json.load(open(s)); print(json.dumps({'sha':hashlib.sha256(s.read_bytes()).hexdigest(),'lifecycle':d['lifecycle_state'],'machine':d['machine_checkpoints']},indent=1))"])
assert p.returncode==0 and "FROZEN" in p.stdout
time.sleep(1)
now4=datetime.now(timezone.utc).isoformat()
(EVID/"now-iso-phase4.txt").write_text(now4+"\n", encoding="utf-8")
print(f"PHASE4 now {now4}", flush=True)
CODE = r"""
import sys, json, subprocess
sys.path.insert(0, sys.argv[1])
root, state_rel, now_iso = sys.argv[1:4]
from pathlib import Path
from datetime import datetime
import os
print(f"PHASE4 child PID={os.getpid()}", flush=True)
root_p = Path(root)
from scripts import survey_production_v2 as core
from scripts import survey_agent_control_v2 as agent
from scripts import survey_publication_v2 as pubmod
from scripts import survey_release_checkpoint_v2 as relchk
assert str(Path(core.__file__).resolve()).startswith(str(root_p.resolve())), "fixture origin"
cfg = json.loads((root_p / "config/survey-production-v2.json").read_bytes())
state_path = root_p / state_rel
state = json.loads(state_path.read_bytes())
print(f"before lifecycle={state['lifecycle_state']} freeze={state['machine_checkpoints']['freeze']}", flush=True)
assert state["lifecycle_state"]=="FROZEN" and state["machine_checkpoints"]["freeze"]=="passed"
now = datetime.fromisoformat(now_iso)
# offline synthetic merge/release evidence per existing test contract (synthetic, NO genuine approval)
manifest_path = root_p / "sources/SP001/publication/v2/release-manifest-v2.json"
merge_path = root_p / "sources/SP001/publication/v2/merge-verification-v2.json"
release_path = root_p / "sources/SP001/publication/v2/release-record-v2.json"
print(f"manifest exists={manifest_path.exists()} merge exists={merge_path.exists()} release exists={release_path.exists()}", flush=True)
assert manifest_path.exists(), "manifest must exist from freeze"
assert not merge_path.exists() and not release_path.exists(), "canonical collides, must use idempotence or report blocker"
head = subprocess.run(["git","-C",str(root_p),"rev-parse","HEAD"], capture_output=True, text=True).stdout.strip()
print(f"HEAD={head}", flush=True)
assert head=="047f8adc0b7a7c005e03a8e2d374c1e5b6712b60"
# build merge verification offline synthetic
pubmod.build_merge_verification(root_p, manifest_path, head, now, merge_path)
print(f"merge={merge_path.relative_to(root_p)}", flush=True)
# build release record offline synthetic, explicit non-genuine
pubmod.build_release_record(root_p, manifest_path, merge_path, now, "synthetic:longform-lifecycle:release:high-u4; NO genuine Human approval", release_path)
print(f"release={release_path.relative_to(root_p)}", flush=True)
pubmod.validate_release_manifest(root_p, manifest_path)
pubmod.validate_release_record(root_p, release_path)
print("manifest+release validated", flush=True)
# normal stage/checkpoint/advance all the way RELEASED via release_checkpoint + agent advance
chk = relchk.build_release_checkpoint(root_p, cfg, state_path, merge_path, release_path, now)
print(f"checkpoint={chk.relative_to(root_p)}", flush=True)
updated = agent.advance_with_checkpoint(root_p, cfg, state_path, chk)
print(json.dumps({"lifecycle":updated["lifecycle_state"],"machine_release":updated["machine_checkpoints"]["release"],"next":updated["next_action"],"terminal":updated["terminal_reason"]},indent=1), flush=True)
assert updated["lifecycle_state"]=="RELEASED"
assert updated["machine_checkpoints"]["release"]=="passed"
assert updated["terminal_reason"]=="COMPLETE"
print("PHASE4_OK", flush=True)
"""
p=run_tag("phase4-release",[sys.executable,"-c",CODE, str(FIX), STATE_REL, now4])
print(open(EVID/"phase4-release-stdout.txt").read()[:8000] if (EVID/"phase4-release-stdout.txt").exists() else "no stdout", flush=True)
print(open(EVID/"phase4-release-stderr.txt").read()[:8000] if (EVID/"phase4-release-stderr.txt").exists() else "no stderr", flush=True)
if p.returncode!=0:
    print("FATAL PHASE4 blocked exact source function/public input ref above", flush=True)
    sys.exit(1)
p=run_tag("after-state",[sys.executable,"-c","import json,hashlib,pathlib; r=pathlib.Path('"+str(FIX)+"'); s=r/'"+STATE_REL+"'; d=json.load(open(s)); print(json.dumps({'sha':hashlib.sha256(s.read_bytes()).hexdigest(),'lifecycle':d['lifecycle_state'],'terminal':d['terminal_reason'],'machine':d['machine_checkpoints']},indent=1))"])
assert p.returncode==0 and "RELEASED" in p.stdout
run_tag("wall-after",["date","-u","+%Y-%m-%dT%H:%M:%SZ"])
print("PHASE4 DONE", flush=True)
