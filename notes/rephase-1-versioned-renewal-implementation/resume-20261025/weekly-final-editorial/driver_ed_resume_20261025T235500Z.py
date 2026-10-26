#!/usr/bin/env python3
"""Weekly-final ED resume: stage proposal+reader from P1 valid, then P2R->scope->P2V WITH_SCOPE->P3S63 fresh (no 35 preload).
Preserves prior invalid orphans + valid authoring, no overwrite, no cleanup.
"""
import os, sys, json, subprocess
from datetime import datetime, timezone
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
BASE = REPO / ".rephase-1-editorial-runtime/versioned-renewal-weekly-final-20261025T235500Z"
FIX = BASE / "renewal-weekly-final"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-final-editorial/ed-resume-20261025T235500Z"
EVID.mkdir(parents=True, exist_ok=True)
LOG = EVID / "commands.log"
LOG.write_text("", encoding="utf-8")
CTRL_HB = EVID / "controller-heartbeat.txt"
CTRL_RES = EVID / "controller-result.txt"
CTRL_EXIT = EVID / "controller-exit.txt"
import datetime as _dt
import atexit as _atexit
CTRL_HB.write_text(f"{_dt.datetime.now(_dt.timezone.utc).isoformat()} resume start pid={os.getpid()}\n", encoding="utf-8")
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
    log(f"$ {' '.join(cmd[:6])}... # {tag} timeout={timeout}s")
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
dest_rel=f"{PDIR_NEW}/authoring-input.json"
log(f"resume prereq authoring exists={(FIX/dest_rel).is_file()}")
log(f"proposal exists before stage={(FIX/proposal_rel).is_file()} (expected False, will stage)")
# Stage2: prepare again + write reader + proposal (preserve if exists with same bytes)
STAGE2=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
root=Path(sys.argv[1]); prop_new=sys.argv[2]
from scripts import survey_production_v2 as core
from scripts import survey_editorial_correction_proposal_v2 as p1mod
issue="2026-W37"
pdir_new=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}"
dest=root/pdir_new/"authoring-input.json"
res=p1mod.prepare_proposal(root, root/f"sources/{issue}/production-state.json", dest, prop_new, "Weekly-final renewal-to-editorial on r2-active")
proposal_dir=root/pdir_new
reader_file=proposal_dir/"reader-surface-input-v2.json"
proposal_file=proposal_dir/"proposal.json"
if not reader_file.exists():
    reader_file.write_bytes(res["proposed_canonical"])
    print(f"staged reader {reader_file.relative_to(root)}")
else:
    assert reader_file.read_bytes()==res["proposed_canonical"], "reader bytes differ, need new ID"
    print(f"reader exists same")
if not proposal_file.exists():
    proposal_file.write_bytes(core.json_bytes(res["proposal"]))
    print(f"staged proposal {proposal_file.relative_to(root)}")
else:
    print(f"proposal exists")
print(f"STAGE2 OK")
"""
s2=run([PY,"-c",STAGE2,str(FIX),PROP_NEW],REPO,"p1-stage2-proposal",timeout=1200)
if s2 is None or s2.returncode!=0:
    log("FATAL stage2")
    CTRL_RES.write_text("FAIL stage2\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("fail stage2"); sys.exit(1)
log(f"after stage2 proposal exists={(FIX/proposal_rel).is_file()}")
# P2R capture
P2R_CAP=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_editorial_retention_v2 as p2r
root=Path(sys.argv[1])
res=p2r.capture_retention(str(root), sys.argv[2], sys.argv[3])
print(json.dumps(res,indent=1))
"""
pcap=run([PY,"-c",P2R_CAP,str(FIX),STATE,proposal_rel],REPO,"p2r-capture",timeout=1200)
if pcap is None or pcap.returncode!=0:
    log("FATAL p2r capture")
    CTRL_RES.write_text("FAIL p2r-capture\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("fail p2r-capture"); sys.exit(1)
try:
    txt=(EVID/"p2r-capture-stdout.txt").read_text()
    resj=json.loads(txt.strip())
    manifest_rel=resj.get("manifest_path") or resj.get("manifest_rel") or ""
    log(f"manifest {manifest_rel}")
except Exception as e:
    log(f"manifest parse fail {e}")
    manifest_rel=""
if not manifest_rel:
    retdir=FIX/PDIR_NEW/"retained"
    cands=list(retdir.glob("*.json")) if retdir.is_dir() else []
    log(f"cands {[p.name for p in cands]}")
    if (retdir/"retention-manifest.json").is_file():
        manifest_rel=f"{PDIR_NEW}/retained/retention-manifest.json"
    elif cands:
        manifest_rel=str(cands[0].relative_to(FIX))
    log(f"fallback {manifest_rel}")
P2R_VER=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_editorial_retention_v2 as p2r
root=Path(sys.argv[1])
res=p2r.verify_retention(str(root), sys.argv[2], sys.argv[3])
print(json.dumps({"VERIFIED":True},indent=1))
"""
pver=run([PY,"-c",P2R_VER,str(FIX),proposal_rel,manifest_rel],REPO,"p2r-verify",timeout=1200)
if pver is None or pver.returncode!=0:
    log("FATAL p2r verify")
    CTRL_RES.write_text("FAIL p2r-verify\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("fail p2r-verify"); sys.exit(1)
log("P2R VERIFIED")
# Scope
SCOPE_BUILD=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
root_s, proposal_rel, scope_rel = sys.argv[1:4]
from pathlib import Path
root=Path(root_s)
from scripts import survey_production_v2 as core
proposal=json.loads((root/proposal_rel).read_bytes())
staged_reader_rel=proposal["proposed"]["proposed_reader_ref"]["path"]
after_sha=proposal["proposed"]["proposed_reader_canonical_sha256"]
block={"version":"EDITORIAL_CORRECTION_SCOPE_V1","decision":"WITHIN_APPROVED_AUTHORITY","before_reader_input":proposal["basis"]["active_reader_input_ref"],"preserved_upstream_sha256":proposal["basis"]["preserved_upstream_digest"],"change_summary":"Synthetic Weekly scope judgment inside approved Architecture authority (weekly-final, no genuine approval).","evidence_locations":["synthetic-fixture:proposal"]}
review={"schema_version":"2.0-rc1","issue_id":proposal["issue_id"],"publication_profile":proposal["publication_profile"],"review_kind":"SEMANTIC_EDITORIAL","reviewed_surface":{"path":staged_reader_rel,"sha256":after_sha},"checks":[{"check_id":"READER_PIPELINE_INDEPENDENCE","status":"PASS","detail":"Synthetic scope reviewer judged proposed reader independently understandable.","evidence_locations":["synthetic-fixture:proposed-reader"]},{"check_id":"EDITORIAL_CORRECTION_SCOPE","status":"PASS","detail":"Synthetic scope reviewer judged delta inside approved Architecture authority.","evidence_locations":["synthetic-fixture:proposal"]}],"decision":"PASS","reviewed_by":"synthetic Weekly scope reviewer (weekly-final)","reviewed_at":"2026-10-26T00:00:00+00:00","recorded_at":"2026-10-26T00:00:00+00:00","status":"PASSED","findings":[],"summary":"Synthetic scope PASS for weekly-final.","editorial_correction_scope":block}
review["review_sha256"]=core.sha256_object(review)
p=root/scope_rel
p.parent.mkdir(parents=True,exist_ok=True)
if p.exists():
    print(f"EXISTS {scope_rel}")
else:
    p.write_bytes(core.json_bytes(review))
    print(f"WROTE {scope_rel}")
"""
scope_rel=f"{PDIR_NEW}/scope-review-v2.json"
pscope=run([PY,"-c",SCOPE_BUILD,str(FIX),proposal_rel,scope_rel],REPO,"scope-build",timeout=300)
if pscope is None or pscope.returncode!=0:
    if (FIX/scope_rel).is_file():
        log("scope exists already")
    else:
        log("FATAL scope")
        CTRL_RES.write_text("FAIL scope\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("fail scope"); sys.exit(1)
log("SCOPE persisted")
# P2V WITH_SCOPE
P2V_OBS=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_editorial_current_authority_v2 as p2v
root=Path(sys.argv[1])
res=p2v.observe_current_authority(str(root), sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
print(json.dumps({"outcome":res.get("outcome")},indent=1))
outcome=res.get("outcome")
if outcome!="CURRENT_BASIS_OBSERVED_SCOPE_BOUND":
    print(f"WRONG_OUTCOME {outcome}")
    import sys as _s; _s.exit(2)
"""
pp2v=run([PY,"-c",P2V_OBS,str(FIX),STATE,proposal_rel,manifest_rel,scope_rel],REPO,"p2v-with-scope",timeout=1200)
if pp2v is None:
    log("P2V TIMEOUT")
    CTRL_RES.write_text("TIMEOUT p2v\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("timeout p2v"); sys.exit(2)
if pp2v.returncode!=0:
    log("FATAL p2v")
    CTRL_RES.write_text("FAIL p2v\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("fail p2v"); sys.exit(1)
log("P2V SCOPE_BOUND OK")
# P3S fresh (no 35 preload)
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
(EVID/"p3s-done.json").write_text(json.dumps({"staged_manifest_rel":staged_manifest_rel,"proposal_rel":proposal_rel,"manifest_rel":manifest_rel,"scope_rel":scope_rel,"prop_new":PROP_NEW},indent=1))
log("RESUME P1-P3S SUCCESS")
CTRL_RES.write_text("SUCCESS P1-P3S63\n",encoding="utf-8")
CTRL_EXIT.write_text("0\n",encoding="utf-8")
beat("success")
