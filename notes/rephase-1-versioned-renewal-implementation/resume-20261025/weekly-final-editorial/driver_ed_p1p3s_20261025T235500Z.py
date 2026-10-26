#!/usr/bin/env python3
"""Weekly-final editorial witness: changed-reader P1->P2R->scope->P2V->P3S63 (fresh child, no 35 preload)->edpub prepare (real TL)->Weekly QA (derived, no EMPTY)->finalize->activate r3->readbacks.
SHORT chain, current 741 fixes, style 035, no placeholders/preload/caching/overrides/synthetic State.
Each public call via fresh subprocess (python -c), bounded 1200s, heartbeat/result/exit.
"""
import os, sys, json, subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
BASE = REPO / ".rephase-1-editorial-runtime/versioned-renewal-weekly-final-20261025T235500Z"
FIX = BASE / "renewal-weekly-final"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-final-editorial/ed-20261025T235500Z"
EVID.mkdir(parents=True, exist_ok=True)
LOG = EVID / "commands.log"
LOG.write_text("", encoding="utf-8")
CTRL_HB = EVID / "controller-heartbeat.txt"
CTRL_RES = EVID / "controller-result.txt"
CTRL_EXIT = EVID / "controller-exit.txt"
import datetime as _dt
import atexit as _atexit
CTRL_HB.write_text(f"{_dt.datetime.now(_dt.timezone.utc).isoformat()} ed driver start pid={os.getpid()}\n", encoding="utf-8")
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
        # Real TL2026 on PATH for edpub prepare (local-only, not installed)
        tlbin="/tmp/opencode/jgas-texlive-20261019T133205Z/texlive/bin/x86_64-linux"
        env["PATH"]=tlbin+":"+env.get("PATH","")
    log(f"$ {' '.join(cmd[:6])}... # {tag} timeout={timeout}s")
    beat(f"start {tag}")
    try:
        proc=subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout, env=env)
    except subprocess.TimeoutExpired:
        (EVID/f"{tag}-stdout.txt").write_text("", encoding="utf-8")
        (EVID/f"{tag}-stderr.txt").write_text(f"Timeout ({timeout}s) PID-parent={os.getpid()}\n", encoding="utf-8")
        (EVID/f"{tag}-exit.txt").write_text("TIMEOUT", encoding="utf-8")
        log(f"DONE {tag} TIMEOUT")
        beat(f"TIMEOUT {tag}")
        return None
    (EVID/f"{tag}-stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (EVID/f"{tag}-stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    (EVID/f"{tag}-exit.txt").write_text(str(proc.returncode), encoding="utf-8")
    log(f"DONE {tag} exit={proc.returncode}")
    beat(f"done {tag} exit={proc.returncode}")
    return proc
PY=sys.executable
ISSUE="2026-W37"
STATE=f"sources/{ISSUE}/production-state.json"
# Prereq: U1 r2 ACTIVE, State VALIDATED_DRAFT, HEAD G1 + U1? Check active
st0=json.loads((FIX/STATE).read_bytes())
active0=st0.get("publication_revalidation_provenance",{}).get("path","")
log(f"prereq active {active0}")
assert "high-u1-weekly-final" in active0 or "r2" in active0, f"expected U1 r2 active, got {active0}"
log("owner P1 survey_editorial_correction_proposal_v2.prepare_proposal")
log("owner P2R survey_editorial_retention_v2.capture_retention/verify_retention")
log("owner P2V survey_editorial_current_authority_v2.observe_current_authority")
log("owner P3S survey_editorial_staged_source_v2.materialize_staged_source/verify_staged_source (shipping 9e2a0ad imports deps itself, no manual 35 preload)")
log("owner EDPUB survey_editorial_publication_v2.prepare_publication/finalize_publication/activate_publication")
log("owner Reader survey_reader_publication_v2.build_review_record/validate_review_record")
log("owner QA survey_quality_v2.expected_checks_by_kind/validate_checks (derive Weekly families, no EMPTY_WRAPPER_SUPPRESSION)")
# P1: stage invalid 1, invalid 2 (expected REFUSE, preserved), then valid 3 paras incl exact synthesis
OLD_AUTH=json.loads((FIX/f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-boot-1/authoring-input.json").read_bytes())
def _make_auth(headline, deck, paras):
    na=json.loads(json.dumps(OLD_AUTH))
    na["cover"]["headline"]=headline
    na["cover"]["deck"]=deck
    na["final_summary"]["paragraphs"]=paras
    return na
STAGE=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_production_v2 as core
root=Path(sys.argv[1]); rel=sys.argv[2]; data=json.loads(sys.argv[3])
p=root/rel
if p.exists():
    print(f"EXISTS {rel}"); import sys as _s; _s.exit(1)
p.parent.mkdir(parents=True,exist_ok=True)
p.write_bytes(core.json_bytes(data))
print(f"WROTE {rel}")
"""
P1C_INVALID=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_editorial_correction_proposal_v2 as p1mod
root=Path(sys.argv[1])
try:
    res=p1mod.prepare_proposal(root, root/sys.argv[2], root/sys.argv[3], sys.argv[4], sys.argv[5])
    print(json.dumps({"UNEXPECTED_PASS":sys.argv[4]})); import sys as _s; _s.exit(0)
except Exception as e:
    print(f"REFUSED {type(e).__name__}: {e}"); import sys as _s; _s.exit(1)
"""
# Invalid 1: 2 paras (too few)
inv1=_make_auth("Invalid headline 1","Invalid deck 1",["Only one paragraph here.","Second paragraph here."])
p_inv1_stage=run([PY,"-c",STAGE,str(FIX),f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-ed-final-invalid1/authoring-input.json",json.dumps(inv1)],REPO,"p1-stage-invalid1",timeout=120)
log(f"invalid1 stage exit={p_inv1_stage.returncode if p_inv1_stage else 'TIMEOUT'} (expected 0 stage, then P1 REFUSE)")
p_inv1=run([PY,"-c",P1C_INVALID,str(FIX),STATE,f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-ed-final-invalid1/authoring-input.json","wk-ed-final-invalid1","invalid test 1"],REPO,"p1-invalid1",timeout=1200)
log(f"invalid1 P1 exit={p_inv1.returncode if p_inv1 else 'TIMEOUT'} (expected 1 REFUSED, preserved)")
# Invalid 2: 3 paras but missing exact synthesis
inv2=_make_auth("Invalid headline 2","Invalid deck 2",["Para one with enough words for test.","Para two with enough words for test.","Wrong synthesis without exact phrase."])
p_inv2_stage=run([PY,"-c",STAGE,str(FIX),f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-ed-final-invalid2/authoring-input.json",json.dumps(inv2)],REPO,"p1-stage-invalid2",timeout=120)
p_inv2=run([PY,"-c",P1C_INVALID,str(FIX),STATE,f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-ed-final-invalid2/authoring-input.json","wk-ed-final-invalid2","invalid test 2"],REPO,"p1-invalid2",timeout=1200)
log(f"invalid2 P1 exit={p_inv2.returncode if p_inv2 else 'TIMEOUT'} (expected 1, preserved)")
# Valid: headline/deck changed + 3 paras incl exact accepted synthesis
valid=_make_auth("Weekly tested method, revised final edition","Source-based survey with weekly-final renewal-editorial amendment; synthetic, no genuine approval.",["The edition surveys one source with weekly-final changed reader.","The claims remain attributed; renewal proof fresh, tool epoch final.","The accepted source authors describe the tested method."])
PROP_NEW="wk-ed-final-1"
dest_rel=f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP_NEW}/authoring-input.json"
p_valid_stage=run([PY,"-c",STAGE,str(FIX),dest_rel,json.dumps(valid)],REPO,"p1-stage-valid",timeout=120)
if p_valid_stage is None or p_valid_stage.returncode!=0:
    log("FATAL valid stage")
    CTRL_RES.write_text("FAIL stage-valid\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("fail stage-valid"); sys.exit(1)
P1V=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_editorial_correction_proposal_v2 as p1mod
root=Path(sys.argv[1])
res=p1mod.prepare_proposal(root, root/sys.argv[2], root/sys.argv[3], sys.argv[4], sys.argv[5])
print(json.dumps({"id":sys.argv[4],"nodes":len(res["graph"]["nodes"]),"edges":len(res["graph"]["edges"])},indent=1))
"""
pp=run([PY,"-c",P1V,str(FIX),STATE,dest_rel,PROP_NEW,"Weekly-final renewal-to-editorial on r2-active (changed reader, synthetic, no genuine approval)"],REPO,"p1-valid",timeout=1200)
if pp is None:
    log("P1 VALID TIMEOUT — record timeout, not retro PASS")
    CTRL_RES.write_text("TIMEOUT p1-valid\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("timeout p1-valid"); sys.exit(2)
if pp.returncode!=0:
    log("FATAL P1 valid")
    CTRL_RES.write_text("FAIL p1-valid\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("fail p1-valid"); sys.exit(1)
log("P1 VALID SUCCESS")
# P2R capture/verify (fresh child per call, no preload)
PDIR_NEW=f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP_NEW}"
proposal_rel=f"{PDIR_NEW}/proposal.json"
assert (FIX/proposal_rel).is_file(), f"proposal missing {proposal_rel}"
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
# Parse manifest path from capture stdout (json dump of res)
try:
    txt=(EVID/"p2r-capture-stdout.txt").read_text()
    resj=json.loads(txt.strip())
    manifest_rel=resj.get("manifest_path") or resj.get("manifest_rel") or ""
    log(f"manifest_rel from capture {manifest_rel}")
except Exception as e:
    log(f"manifest parse fail {e}, fallback glob")
    manifest_rel=""
if not manifest_rel:
    retdir=FIX/PDIR_NEW/"retained"
    cands=list(retdir.glob("*.json")) if retdir.is_dir() else []
    log(f"retained cands {[p.name for p in cands]}")
    # Usually retention-manifest.json
    if (retdir/"retention-manifest.json").is_file():
        manifest_rel=f"{PDIR_NEW}/retained/retention-manifest.json"
    elif cands:
        manifest_rel=str(cands[0].relative_to(FIX))
    log(f"fallback manifest {manifest_rel}")
log(f"manifest_rel {manifest_rel}")
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
# Early scope (persisted synthetic review, no genuine approval)
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
    print(f"EXISTS {scope_rel}"); import sys as _s; _s.exit(1)
p.write_bytes(core.json_bytes(review))
print(f"WROTE {scope_rel}")
"""
scope_rel=f"{PDIR_NEW}/scope-review-v2.json"
pscope=run([PY,"-c",SCOPE_BUILD,str(FIX),proposal_rel,scope_rel],REPO,"scope-build",timeout=300)
if pscope is None or pscope.returncode!=0:
    # If exists already (resume), treat as ok if file exists
    if (FIX/scope_rel).is_file():
        log("scope exists already, continue")
    else:
        log("FATAL scope")
        CTRL_RES.write_text("FAIL scope\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("fail scope"); sys.exit(1)
log("SCOPE persisted")
# P2V WITH_SCOPE (fresh child, expect CURRENT_BASIS_OBSERVED_SCOPE_BOUND, NOT NEEDS_SCOPE)
P2V_OBS=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_editorial_current_authority_v2 as p2v
root=Path(sys.argv[1])
res=p2v.observe_current_authority(str(root), sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
print(json.dumps({"outcome":res.get("outcome"),"basis":str(res.get("basis"))[:200]},indent=1))
# Strict: must be SCOPE_BOUND, not NEEDS_SCOPE
outcome=res.get("outcome")
if outcome!="CURRENT_BASIS_OBSERVED_SCOPE_BOUND":
    print(f"WRONG_OUTCOME {outcome} expected CURRENT_BASIS_OBSERVED_SCOPE_BOUND")
    import sys as _s; _s.exit(2)
"""
pp2v=run([PY,"-c",P2V_OBS,str(FIX),STATE,proposal_rel,manifest_rel,scope_rel],REPO,"p2v-with-scope",timeout=1200)
if pp2v is None:
    log("P2V TIMEOUT — record, not retro PASS")
    CTRL_RES.write_text("TIMEOUT p2v\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("timeout p2v"); sys.exit(2)
if pp2v.returncode!=0:
    log("FATAL p2v (expected SCOPE_BOUND)")
    CTRL_RES.write_text("FAIL p2v\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("fail p2v"); sys.exit(1)
log("P2V WITH_SCOPE CURRENT_BASIS_OBSERVED_SCOPE_BOUND OK")
# P3S materialize/verify 63 in FRESH child WITHOUT manual 35 preload (shipping 9e2a0ad imports itself)
P3S_MAT=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
# NO manual 35 preload: only import p3s (it lazy-imports New5 itself)
from pathlib import Path
from scripts import survey_editorial_staged_source_v2 as p3s
root=Path(sys.argv[1])
res=p3s.materialize_staged_source(str(root), sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
print(json.dumps({"staged":res.get("staged_manifest_ref",{}).get("path") if isinstance(res,dict) else str(res)},indent=1))
"""
pp3s=run([PY,"-c",P3S_MAT,str(FIX),STATE,proposal_rel,manifest_rel,scope_rel],REPO,"p3s-materialize",timeout=1200)
if pp3s is None:
    log("P3S TIMEOUT — record, not retro PASS")
    CTRL_RES.write_text("TIMEOUT p3s-mat\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("timeout p3s"); sys.exit(2)
if pp3s.returncode!=0:
    # Check STAGED_ROOT_EXISTS resume case? If already exists, verify existing
    log("P3S materialize non-zero, checking if STAGED_ROOT_EXISTS resume")
    txt=(EVID/"p3s-materialize-stderr.txt").read_text() if (EVID/"p3s-materialize-stderr.txt").is_file() else ""
    if "STAGED_ROOT_EXISTS" in txt:
        log("STAGED_ROOT_EXISTS — will verify existing")
    else:
        log("FATAL p3s materialize")
        CTRL_RES.write_text("FAIL p3s-mat\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("fail p3s-mat"); sys.exit(1)
staged_manifest_rel=f"{PDIR_NEW}/staged-source/staged-source-manifest.json"
log(f"staged {staged_manifest_rel} exists={(FIX/staged_manifest_rel).is_file()}")
P3S_VER=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_editorial_staged_source_v2 as p3s
root=Path(sys.argv[1])
v=p3s.verify_staged_source(str(root), sys.argv[2], sys.argv[3])
# Check 63
deps=v.get("code_deps") or v.get("verified_deps") or []
# The verifier returns replay info; log code_deps count via manifest
import json as _j
sm=_j.loads((Path(sys.argv[1])/sys.argv[3]).read_bytes())
code_deps=sm.get("code_deps") or sm.get("code_dependencies") or []
print(json.dumps({"verify_ok":True,"code_deps_count":len(code_deps) if isinstance(code_deps,list) else "unknown"},indent=1))
if isinstance(code_deps,list) and len(code_deps)!=63:
    print(f"WRONG_COUNT {len(code_deps)} expected 63")
    import sys as _s; _s.exit(2)
"""
pv=run([PY,"-c",P3S_VER,str(FIX),proposal_rel,staged_manifest_rel],REPO,"p3s-verify",timeout=1200)
if pv is None or pv.returncode!=0:
    log("FATAL p3s verify (expected 63)")
    CTRL_RES.write_text("FAIL p3s-verify\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("fail p3s-verify"); sys.exit(1)
log("P3S 63 VERIFIED")
# Record P3S success, continue to edpub in next driver? For single driver, continue
beat("p3s done, continuing to edpub")
# Save intermediate state for next phase (edpub) — write marker
(EVID/"p3s-done.json").write_text(json.dumps({"staged_manifest_rel":staged_manifest_rel,"proposal_rel":proposal_rel,"manifest_rel":manifest_rel,"scope_rel":scope_rel,"prop_new":PROP_NEW},indent=1))
log("ED P1-P3S SUCCESS")
CTRL_RES.write_text("SUCCESS P1-P3S63\n",encoding="utf-8")
CTRL_EXIT.write_text("0\n",encoding="utf-8")
beat("success P1-P3S")
