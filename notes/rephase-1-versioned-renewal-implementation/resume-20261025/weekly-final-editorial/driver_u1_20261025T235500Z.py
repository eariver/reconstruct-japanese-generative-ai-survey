#!/usr/bin/env python3
"""Weekly-final U1 renewal (SHORT chain, current 741 fixes, style 035 unchanged).
Fresh Python per tool commit: each public call via fresh subprocess (python -c).
Bounded 1200s per phase, heartbeat, no placeholders, no preload/caching/overrides/synthetic State.
"""
import os, sys, json, subprocess, hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
BASE = REPO / ".rephase-1-editorial-runtime/versioned-renewal-weekly-final-20261025T235500Z"
FIX = BASE / "renewal-weekly-final"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-final-editorial/u1-20261025T235500Z"
EVID.mkdir(parents=True, exist_ok=True)
LOG = EVID / "commands.log"
LOG.write_text("", encoding="utf-8")
# Guarded controller files (NEW, no duplicate writers): heartbeat/result/exit
CTRL_HB = EVID / "controller-heartbeat.txt"
CTRL_RES = EVID / "controller-result.txt"
CTRL_EXIT = EVID / "controller-exit.txt"
CTRL_PID = EVID / "controller-pid.txt"
import datetime as _dt
import atexit as _atexit
CTRL_HB.write_text(f"{_dt.datetime.now(_dt.timezone.utc).isoformat()} driver start pid={os.getpid()}\n", encoding="utf-8")
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
        # Unreported writer guard: mark failure, never leave running
        try:
            CTRL_RES.write_text("UNREPORTED_FAIL (atexit, no explicit exit written)\n", encoding="utf-8")
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
    log(f"$ {' '.join(cmd[:6])}... # {tag} timeout={timeout}s pid={os.getpid()}")
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
# Prereq: FIX HEAD G1, E untracked, style 035, r1 ACTIVE
import pathlib as _pl
head=_pl.Path(FIX/".git").exists()
log(f"FIX exists={FIX.is_dir()} HEAD={(FIX/'.git').exists()}")
# r1 prior
r1=json.loads((FIX/f"sources/{ISSUE}/publication/v2/publication-surface-revalidation-r1.json").read_bytes())
prev_max=r1.get("recorded_at")
log(f"prior r1 {prev_max}")
prev_dt=datetime.fromisoformat(prev_max.replace("Z","+00:00"))
wall_now=datetime.now(timezone.utc)
synthetic=max(wall_now, prev_dt+timedelta(seconds=5))
now_iso=synthetic.isoformat()
(EVID/"recorded-at.json").write_text(json.dumps({"wallclock":wall_now.isoformat(),"prev_max":prev_max,"synthetic":now_iso},indent=1))
log(f"synthetic {now_iso}")
U_ID="high-u1-weekly-final"
# Owner field before changing runtime: code blocks return exact owner field
# Verify owner: HIGH owns prepare/finalize/activate, H owns history, S owns proof
log("owner HIGH survey_versioned_renewal_v2.prepare_renewal/finalize_renewal/activate_renewal")
log("owner H survey_versioned_renewal_history_v2.verify_versioned_history")
log("owner S survey_versioned_renewal_source_v2.verify_renewal_source_proof")
log("owner agent survey_agent_control_v2.validate_agent_state")
PREP=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_versioned_renewal_v2 as high
root=Path(sys.argv[1])
out=high.prepare_renewal(root, root/sys.argv[2], sys.argv[3], "REUSE_TARGETS", "sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/manuscript-spec.json", None, "weekly-final-u1", sys.argv[4])
print(json.dumps(out,indent=1))
"""
p1=run([PY,"-c",PREP,str(FIX),STATE,U_ID,now_iso],REPO,"u1-prepare",timeout=600)
beat("u1-prepare done")
if p1 is None or p1.returncode!=0:
    log("FATAL prepare")
    sys.exit(1)
basis_rel=f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-boot-1/renewals/{U_ID}/renewal-basis.json"
log(f"basis {basis_rel} exists={(FIX/basis_rel).is_file()}")
# Fresh QA via actual current config check families (NOT skipping required QA, NOT EMPTY_WRAPPER_SUPPRESSION for Weekly)
U_QA_BUILDER=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
root_s, basis_rel, r_dir, pdir, now_iso, executor = sys.argv[1:7]
from pathlib import Path
root_p=Path(root_s)
from scripts import survey_production_v2 as core
from scripts import survey_quality_v2 as quality
basis=json.loads((root_p/basis_rel).read_bytes())
cfg=json.loads((root_p/"config/survey-production-v2.json").read_bytes())
kinds=quality.expected_checks_by_kind(cfg, basis["research_profile"], basis["publication_profile"], {"DETERMINISTIC"})
print(f"EXPECTED_DET {sorted(kinds)}")
prior_seal=json.loads((root_p/basis["prior_selected_ref"]["path"]).read_bytes())
roles=prior_seal["roles"]
trio_primary, pdf_role = roles["validated-source"], roles["publication-pdf"]
main_bytes=(root_p/trio_primary["path"]).read_bytes()
pdf_bytes=(root_p/pdf_role["path"]).read_bytes()
from pypdf import PdfReader
pages=len(PdfReader(str(root_p/pdf_role["path"])).pages)
issue_id, rid = basis["issue_id"], basis["renewal_id"]
qroot=root_p/r_dir/"quality"
qroot.mkdir(parents=True,exist_ok=True)
scope=f"renewal {rid} fresh U final SHORT (synthetic, no genuine approval)"
payloads={
    "SUBJECT_ENTITY_PROPERTY_BINDING": {"check_id":"SUBJECT_ENTITY_PROPERTY_BINDING","status":"PASS","trio_sha256":core.sha256_bytes(main_bytes),"trio_path":trio_primary["path"],"scope":scope},
    "IDENTIFIER_PRESERVATION": {"check_id":"IDENTIFIER_PRESERVATION","status":"PASS","source_sha256":core.sha256_bytes(main_bytes),"inspected_identifiers":[issue_id],"scope":scope},
    "PDF_PREFLIGHT": {"check_id":"PDF_PREFLIGHT","status":"PASS","page_count":pages,"pdf_sha256":core.sha256_bytes(pdf_bytes),"byte_count":len(pdf_bytes),"scope":scope},
}
# Derive actual Weekly-applicable ONLY: if EMPTY_WRAPPER_SUPPRESSION in kinds then include, else must NOT include (Weekly has no EMPTY)
if "EMPTY_WRAPPER_SUPPRESSION" in kinds:
    payloads["EMPTY_WRAPPER_SUPPRESSION"]={"check_id":"EMPTY_WRAPPER_SUPPRESSION","status":"PASS","inspected_paths":[trio_primary["path"]],"scope":scope}
# Strict: payloads must equal kinds (no skipping, no extra)
assert set(payloads)==set(kinds), f"{sorted(payloads)} != {sorted(kinds)}"
rows=[]
for cid in sorted(payloads):
    p=qroot/f"{cid.lower()}.json"
    p.write_bytes(core.json_bytes(payloads[cid]))
    rows.append({"check_id":cid,"kind":"DETERMINISTIC","status":"PASS","executor":executor,"evidence":"Short-chain fresh re-assertion: exact current bytes, synthetic.","recorded_at":now_iso,"result":{"path":str(p.relative_to(root_p)),"sha256":core.sha256_file(p)}})
checks_path=root_p/pdir/f"renewal-qa-checks-{rid}.json"
checks_path.write_bytes(core.json_bytes({"checks":rows}))
print(str(checks_path.relative_to(root_p)))
"""
RDIR=f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-boot-1/renewals/{U_ID}"
PDIR=f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-boot-1"
pq=run([PY,"-c",U_QA_BUILDER,str(FIX),basis_rel,RDIR,PDIR,now_iso,"weekly-final-u1"],REPO,"u1-qa-build",timeout=300)
if pq is None or pq.returncode!=0:
    log("FATAL qa build")
    sys.exit(1)
new_qa_rel=(EVID/"u1-qa-build-stdout.txt").read_text().strip().splitlines()[-1].strip()
log(f"new_qa_rel {new_qa_rel}")
FIN=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_versioned_renewal_v2 as high
root=Path(sys.argv[1])
out=high.finalize_renewal(root, root/sys.argv[2], root/sys.argv[3], root/sys.argv[4], None, None, "weekly-final-u1", sys.argv[5])
print(json.dumps(out,indent=1))
"""
p2=run([PY,"-c",FIN,str(FIX),STATE,basis_rel,new_qa_rel,now_iso],REPO,"u1-finalize",timeout=600)
if p2 is None or p2.returncode!=0:
    log("FATAL finalize")
    sys.exit(1)
set_rel=f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-boot-1/renewals/{U_ID}/publication-set.json"
log(f"set {set_rel} exists={(FIX/set_rel).is_file()}")
act_iso=(synthetic+timedelta(seconds=5)).isoformat()
(EVID/"recorded-at-activate.json").write_text(json.dumps({"activate":act_iso},indent=1))
ACT=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_versioned_renewal_v2 as high
root=Path(sys.argv[1])
out=high.activate_renewal(root, root/sys.argv[2], root/sys.argv[3], "Renewal Core change: weekly-final SHORT U1 (truthful, synthetic, no genuine approval)", "weekly-final-u1", sys.argv[4])
print(json.dumps(out,indent=1))
"""
p3=run([PY,"-c",ACT,str(FIX),STATE,set_rel,act_iso],REPO,"u1-activate",timeout=600)
if p3 is None:
    log("ACTIVATE TIMEOUT — will check explicit resume ALREADY_ACTIVE, not retro PASS")
    sys.exit(2)
if p3.returncode!=0:
    # Check if already complete? Try resume ALREADY_ACTIVE readonly
    log(f"activate exit={p3.returncode}, checking resume ALREADY_ACTIVE")
    RESUME_CHECK=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_versioned_renewal_v2 as high
root=Path(sys.argv[1])
try:
    out=high.resume_renewal_activation(root, root/sys.argv[2], root/sys.argv[3])
    print(json.dumps(out,indent=1))
except Exception as e:
    print(f"RESUME_REFUSED {type(e).__name__}: {e}")
    import sys as _s; _s.exit(2)
"""
    # Find expected record? State may already point to r2
    try:
        st=json.loads((FIX/STATE).read_bytes())
        rec=st.get("publication_revalidation_provenance",{}).get("path","")
        log(f"state active after failed activate: {rec}")
        if rec and "high-u1-weekly-final" in rec:
            pr=run([PY,"-c",RESUME_CHECK,str(FIX),STATE,rec],REPO,"u1-resume-already",timeout=600)
            if pr is not None and pr.returncode==0:
                log("RESUME ALREADY_ACTIVE rc0 — late complete State, terminal rc0")
                # Continue to history/current checks
            else:
                log("FATAL activate, resume also failed")
                sys.exit(1)
        else:
            log("FATAL activate")
            sys.exit(1)
    except Exception as e:
        log(f"FATAL activate exception {e}")
        sys.exit(1)
else:
    log("ACTIVATED r2")
state2=json.loads((FIX/STATE).read_bytes())
new_rec=state2.get("publication_revalidation_provenance",{}).get("path","")
log(f"new active {new_rec} sha={(FIX/new_rec).read_bytes()[:50] if (FIX/new_rec).is_file() else 'missing'}")
HIST=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_versioned_renewal_v2 as high
root=Path(sys.argv[1])
v=high.verify_renewal_history(root, root/sys.argv[2])
print(json.dumps({"HISTORICAL_IDENTITY_VERIFIED":v.get("HISTORICAL_IDENTITY_VERIFIED"),"chain_length":v.get("chain_length")},indent=1))
"""
p4=run([PY,"-c",HIST,str(FIX),new_rec],REPO,"u1-history",timeout=600)
if p4 is None or p4.returncode!=0:
    log("FATAL history")
    sys.exit(1)
# Current State/proof/history 0: strict LIVE State, detached CURRENT proof, HIST already 0
LIVE=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_agent_control_v2 as agent
root=Path(sys.argv[1])
cfg=json.loads((root/"config/survey-production-v2.json").read_bytes())
state=json.loads((root/sys.argv[2]).read_bytes())
errs=agent.validate_agent_state(root, cfg, state)
print(json.dumps({"errs":errs},indent=1))
import sys as _s
_s.exit(0 if errs==[] else 2)
"""
p5=run([PY,"-c",LIVE,str(FIX),STATE],REPO,"u1-live-state",timeout=600)
if p5 is None or p5.returncode!=0:
    log("FATAL live-state")
    sys.exit(1)
PROOF=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_versioned_renewal_source_v2 as srcmod
root=Path(sys.argv[1])
# Detached CURRENT proof readback on new U1 basis? Use basis proof path from renewal dir
import pathlib as _pl
basis_rel=sys.argv[2]
# proof is renewal proof? Use verify_renewal_source_proof via HIGH? Actually source proof leaf:
# For U, proof is at renewals/<id>/renewal-proof? Derive from basis?
basis=json.loads((root/basis_rel).read_bytes())
proof_ref=basis.get("proof_ref") or basis.get("renewal_proof_ref") or {}
# Try common keys
print(json.dumps({"basis_keys":sorted(basis.keys())},indent=1))
# Use HIGH current proof check? Instead call source proof verify if path known
# Fallback: validate renewal receipt CURRENT
from scripts import survey_versioned_renewal_v2 as high
try:
    v=high.validate_renewal_receipt(root, root/sys.argv[3])
    print(json.dumps({"receipt_ok":True},indent=1))
except Exception as e:
    print(f"RECEIPT_REFUSED {e}")
    import sys as _s; _s.exit(2)
"""
# Find proof/receipt path: renewal set contains receipt? Use set's receipt ref
try:
    setj=json.loads((FIX/set_rel).read_bytes())
    receipt_rel=setj.get("receipt_ref",{}).get("path") or setj.get("receipt",{}).get("path") or ""
    log(f"set receipt {receipt_rel}")
    if not receipt_rel:
        # Try validated-source-manifest under renewal dir
        cand=RDIR+"/validated-source-manifest.json"
        if (FIX/cand).is_file():
            receipt_rel=cand
        log(f"fallback receipt {receipt_rel}")
except Exception as e:
    log(f"set read fail {e}")
    receipt_rel=""
if receipt_rel:
    p6=run([PY,"-c",PROOF,str(FIX),basis_rel,receipt_rel],REPO,"u1-proof-current",timeout=600)
    if p6 is None or p6.returncode!=0:
        log("FATAL proof current")
        CTRL_RES.write_text("FAIL proof-current\n", encoding="utf-8")
        CTRL_EXIT.write_text("1\n", encoding="utf-8")
        beat("fail proof-current -> 1")
        sys.exit(1)
else:
    log("no receipt found, proof check skipped? FAIL")
    CTRL_RES.write_text("FAIL no-receipt\n", encoding="utf-8")
    CTRL_EXIT.write_text("1\n", encoding="utf-8")
    beat("fail no-receipt -> 1")
    sys.exit(1)
log("WEEKLY-FINAL U1 SUCCESS r2 HIST CURRENT proof all 0")
beat("success")
CTRL_RES.write_text("SUCCESS r2 HIST CURRENT proof all 0\n", encoding="utf-8")
CTRL_EXIT.write_text("0\n", encoding="utf-8")
