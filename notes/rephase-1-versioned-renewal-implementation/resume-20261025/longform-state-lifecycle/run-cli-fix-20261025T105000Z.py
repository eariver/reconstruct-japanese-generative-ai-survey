#!/usr/bin/env python3
"""CLI fix: correct validate-state CLI per existing test contract."""
import os, sys, json, subprocess, time
from datetime import datetime, timezone
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
PARENT = REPO / ".rephase-1-editorial-runtime/versioned-renewal-longform-lifecycle-20261025T100000Z"
FIX = PARENT / "renewal-longform-lifecycle"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-state-lifecycle/phase-final-20261025T105000Z"
ISSUE="SP001"; STATE_REL=f"sources/{ISSUE}/production-state.json"
rel = STATE_REL
# sanitized env like weekly
env = {"PATH": f"/usr/bin:/bin:{Path(sys.executable).parent}","PYTHONPATH": ".","PYTHONDONTWRITEBYTECODE":"1","GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file","LC_ALL":"C"}
if "HOME" in os.environ:
    env["HOME"]=os.environ["HOME"]
for k in ["TMPDIR","PYTHONPYCACHEPREFIX"]:
    if k in os.environ:
        env[k]=os.environ[k]
tmpdir = PARENT/"tmp"
tmpdir.mkdir(parents=True, exist_ok=True)
env["TMPDIR"]=str(tmpdir); env["TMP"]=str(tmpdir); env["TEMP"]=str(tmpdir)
for k in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
    assert k not in os.environ
    assert k not in env
print(f"CLI fix start PID={os.getpid()}", flush=True)
t0=time.time()
proc=subprocess.run([sys.executable,"scripts/survey_agent_control_v2.py","--repo-root",".","validate-state","--state",rel], cwd=str(FIX), env=env, capture_output=True, text=True, timeout=1200)
dur=time.time()-t0
(EVID/"cli-validate-state-fix-stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
(EVID/"cli-validate-state-fix-stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
(EVID/"cli-validate-state-fix-exit.txt").write_text(str(proc.returncode), encoding="utf-8")
(EVID/"cli-validate-state-fix-dur.txt").write_text(f"{dur:.2f}\n", encoding="utf-8")
with open(EVID/"commands.log","a",encoding="utf-8") as fh:
    fh.write(f"$ python scripts/survey_agent_control_v2.py --repo-root . validate-state --state {rel} -> exit={proc.returncode} dur={dur:.2f}s\n")
print(f"DONE CLI fix exit={proc.returncode} dur={dur:.2f}s", flush=True)
print(proc.stdout[:3000], flush=True)
print(proc.stderr[:3000], flush=True)
if proc.returncode!=0:
    print("FATAL CLI blocked", flush=True)
    sys.exit(1)
payload=json.loads(proc.stdout)
assert payload["valid"]==True and payload["lifecycle_state"]=="RELEASED" and payload["state"]==rel
print("CLI_FIX_OK", flush=True)
# also persist HEAD/tree/ancestor import/source guard if not already
def run_tag(tag, cmd):
    print(f"START {tag}", flush=True)
    t0=time.time()
    pr=subprocess.run(cmd, cwd=str(REPO), capture_output=True, text=True, timeout=1200, env={**os.environ, "PYTHONDONTWRITEBYTECODE":"1","LC_ALL":"C","TMPDIR":str(tmpdir),"TMP":str(tmpdir),"TEMP":str(tmpdir)})
    dur=time.time()-t0
    (EVID/f"{tag}-stdout.txt").write_text(pr.stdout or "", encoding="utf-8")
    (EVID/f"{tag}-stderr.txt").write_text(pr.stderr or "", encoding="utf-8")
    (EVID/f"{tag}-exit.txt").write_text(str(pr.returncode), encoding="utf-8")
    (EVID/f"{tag}-dur.txt").write_text(f"{dur:.2f}\n", encoding="utf-8")
    print(f"DONE {tag} exit={pr.returncode}", flush=True)
    return pr
run_tag("head-final",["git","-C",str(FIX),"rev-parse","HEAD"])
run_tag("tree-final",["git","-C",str(FIX),"rev-parse","HEAD^{tree}"])
run_tag("ancestor-final",["git","-C",str(FIX),"merge-base","--is-ancestor","721a04d85532d7855f3e54cc411f5847c787726e","HEAD"])
run_tag("import-guard",[sys.executable,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts import survey_production_v2 as core; print(core.__file__); assert '"+str(FIX)+"' in core.__file__; print('IMPORT_GUARD_OK')", str(FIX)])
run_tag("wall-after",["date","-u","+%Y-%m-%dT%H:%M:%SZ"])
print("CLI FIX DONE", flush=True)
