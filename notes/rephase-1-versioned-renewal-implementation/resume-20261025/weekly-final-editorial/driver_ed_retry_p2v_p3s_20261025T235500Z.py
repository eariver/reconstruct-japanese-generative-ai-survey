#!/usr/bin/env python3
"""Weekly-final ED retry: P2V WITH_SCOPE correct result key + P3S63 fresh.
Preserves prior P1/P2R/scope partials, fixes harness wrong outcome key (was outcome, correct is result).
No 35 preload for P3S, bounded 1200s, heartbeat/result/exit.
"""
import os, sys, json, subprocess
from datetime import datetime, timezone
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
BASE = REPO / ".rephase-1-editorial-runtime/versioned-renewal-weekly-final-20261025T235500Z"
FIX = BASE / "renewal-weekly-final"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-final-editorial/ed-retry-p2v-p3s-20261025T235500Z"
EVID.mkdir(parents=True, exist_ok=True)
LOG = EVID / "commands.log"
LOG.write_text("", encoding="utf-8")
CTRL_HB = EVID / "controller-heartbeat.txt"
CTRL_RES = EVID / "controller-result.txt"
CTRL_EXIT = EVID / "controller-exit.txt"
import datetime as _dt
import atexit as _atexit
CTRL_HB.write_text(f"{_dt.datetime.now(_dt.timezone.utc).isoformat()} retry start pid={os.getpid()}\n", encoding="utf-8")
CTRL_RES.write_text("RUNNING\n", encoding="utf-8")
if not CTRL_EXIT.exists():
    CTRL_EXIT.write_text("running\n", encoding="utf-8")
def beat(msg):
    with open(CTRL_HB, "a", encoding="utf-8") as fh:
        fh.write(f"{_dt.datetime.now(_dt.timezone.utc).isoformat()} {msg} pid={os.getpid()}\n")
beat("init")
def _finalize_exit():
    try:
        cur = CTRL_EXIT.read_text(encoding="utf-8").strip() if CTRL_EXIT.exists() else "missing"
    except Exception:
        cur = "unreadable"
    if cur == "running":
        try:
            CTRL_RES.write_text("UNREPORTED_FAIL (atexit)\n", encoding="utf-8")
            CTRL_EXIT.write_text("1\n", encoding="utf-8")
            beat("atexit UNREPORTED_FAIL -> 1")
        except Exception:
            pass
_atexit.register(_finalize_exit)
def log(m):
    print(m, flush=True)
    open(LOG, "a").write(m+"\n")
def run(cmd, cwd, tag, timeout=1200, env=None):
    if env is None:
        env=dict(os.environ)
        env["PYTHONDONTWRITEBYTECODE"]="1"; env["LC_ALL"]="C"
        env["GIT_NO_LAZY_FETCH"]="1"; env["GIT_CONFIG_NOSYSTEM"]="1"; env["GIT_CONFIG_GLOBAL"]="/dev/null"; env["GIT_OPTIONAL_LOCKS"]="0"
        tmpdir=BASE/"tmp-tex"; tmpdir.mkdir(parents=True, exist_ok=True)
        env["TMPDIR"]=str(tmpdir); env["TMP"]=str(tmpdir); env["TEMP"]=str(tmpdir)
        tlbin="/tmp/opencode/jgas-texlive-20261019T133205Z/texlive/bin/x86_64-linux"
        env["PATH"]=tlbin+":"+env.get("PATH","")
    log(f"$ {' '.join(cmd[:6])}... # {tag}")
    beat(f"start {tag}")
    try:
        proc=subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout, env=env)
    except subprocess.TimeoutExpired:
        (EVID/f"{tag}-stdout.txt").write_text("", encoding="utf-8")
        (EVID/f"{tag}-stderr.txt").write_text(f"Timeout ({timeout}s)\n", encoding="utf-8")
        (EVID/f"{tag}-exit.txt").write_text("TIMEOUT", encoding="utf-8")
        log(f"DONE {tag} TIMEOUT"); beat(f"TIMEOUT {tag}"); return None
    (EVID/f"{tag}-stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (EVID/f"{tag}-stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    (EVID/f"{tag}-exit.txt").write_text(str(proc.returncode), encoding="utf-8")
    log(f"DONE {tag} exit={proc.returncode}"); beat(f"done {tag} exit={proc.returncode}"); return proc
PY=sys.executable
ISSUE="2026-W37"
STATE=f"sources/{ISSUE}/production-state.json"
PROP_NEW="wk-ed-final-1"
PDIR_NEW=f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP_NEW}"
proposal_rel=f"{PDIR_NEW}/proposal.json"
manifest_rel=f"{PDIR_NEW}/retained/retention-manifest.json"
scope_rel=f"{PDIR_NEW}/scope-review-v2.json"
log(f"prereq proposal {(FIX/proposal_rel).is_file()} manifest {(FIX/manifest_rel).is_file()} scope {(FIX/scope_rel).is_file()}")
log("harness fix: prior ed-resume P2V checked res.get(outcome) wrong key, correct is res.get(result); this retry uses result")
log("owner P2V survey_editorial_current_authority_v2.observe_current_authority")
log("owner P3S survey_editorial_staged_source_v2.materialize/verify (no 35 preload)")
P2V_OBS=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_editorial_current_authority_v2 as p2v
root=Path(sys.argv[1])
res=p2v.observe_current_authority(str(root), sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
print(json.dumps({"result":res.get("result")},indent=1))
result=res.get("result")
if result!="CURRENT_BASIS_OBSERVED_SCOPE_BOUND":
    print(f"WRONG_RESULT {result} expected CURRENT_BASIS_OBSERVED_SCOPE_BOUND")
    import sys as _s; _s.exit(2)
"""
pp2v=run([PY,"-c",P2V_OBS,str(FIX),STATE,proposal_rel,manifest_rel,scope_rel],REPO,"p2v-with-scope-fixed",timeout=1200)
if pp2v is None:
    log("P2V TIMEOUT")
    CTRL_RES.write_text("TIMEOUT p2v\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("timeout p2v"); sys.exit(2)
if pp2v.returncode!=0:
    log("FATAL p2v fixed")
    CTRL_RES.write_text("FAIL p2v-fixed\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("fail p2v-fixed"); sys.exit(1)
log("P2V WITH_SCOPE CURRENT_BASIS_OBSERVED_SCOPE_BOUND OK (fixed harness)")
P3S_MAT=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_editorial_staged_source_v2 as p3s
root=Path(sys.argv[1])
res=p3s.materialize_staged_source(str(root), sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
print(json.dumps({"staged":res.get("staged_manifest_ref",{}).get("path") if isinstance(res,dict) else str(res)},indent=1))
"""
pp3s=run([PY,"-c",P3S_MAT,str(FIX),STATE,proposal_rel,manifest_rel,scope_rel],REPO,"p3s-materialize",timeout=1200)
if pp3s is None:
    log("P3S TIMEOUT")
    CTRL_RES.write_text("TIMEOUT p3s-mat\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("timeout p3s"); sys.exit(2)
if pp3s.returncode!=0:
    txt=(EVID/"p3s-materialize-stderr.txt").read_text() if (EVID/"p3s-materialize-stderr.txt").is_file() else ""
    if "STAGED_ROOT_EXISTS" in txt:
        log("STAGED_ROOT_EXISTS resume")
    else:
        log("FATAL p3s mat")
        CTRL_RES.write_text("FAIL p3s-mat\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("fail p3s-mat"); sys.exit(1)
staged_manifest_rel=f"{PDIR_NEW}/staged-source/staged-source-manifest.json"
log(f"staged exists={(FIX/staged_manifest_rel).is_file()}")
P3S_VER=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_editorial_staged_source_v2 as p3s
root=Path(sys.argv[1])
v=p3s.verify_staged_source(str(root), sys.argv[2], sys.argv[3])
import json as _j
sm=_j.loads((Path(sys.argv[1])/sys.argv[3]).read_bytes())
code_deps=sm.get("code_deps") or []
print(json.dumps({"verify_ok":True,"code_deps_count":len(code_deps) if isinstance(code_deps,list) else "unknown"},indent=1))
if isinstance(code_deps,list) and len(code_deps)!=63:
    print(f"WRONG_COUNT {len(code_deps)}")
    import sys as _s; _s.exit(2)
"""
pv=run([PY,"-c",P3S_VER,str(FIX),proposal_rel,staged_manifest_rel],REPO,"p3s-verify",timeout=1200)
if pv is None or pv.returncode!=0:
    log("FATAL p3s verify 63")
    CTRL_RES.write_text("FAIL p3s-verify\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("fail p3s-verify"); sys.exit(1)
log("P3S 63 VERIFIED")
(EVID/"p3s-done.json").write_text(json.dumps({"staged_manifest_rel":staged_manifest_rel,"proposal_rel":proposal_rel,"manifest_rel":manifest_rel,"scope_rel":scope_rel},indent=1))
log("RETRY P2V-P3S SUCCESS")
CTRL_RES.write_text("SUCCESS P2V-P3S63 fixed\n",encoding="utf-8")
CTRL_EXIT.write_text("0\n",encoding="utf-8")
beat("success")
