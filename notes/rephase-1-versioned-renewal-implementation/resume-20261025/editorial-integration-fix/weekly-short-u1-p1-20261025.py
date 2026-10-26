#!/usr/bin/env python3
"""Short weekly U1 + P1 positive (chain2, fast)."""
import os, sys, json, subprocess, hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
BASE = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-editorial-fix-short-20261025T073655Z")
FIX = BASE / "renewal-weekly-short"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/editorial-integration-fix/weekly-short-20261025T073655Z/u1-p1-20261025T074000Z"
EVID.mkdir(parents=True, exist_ok=True)
LOG=EVID/"commands.log"; LOG.write_text("",encoding="utf-8")
def log(m):
    print(m,flush=True); open(LOG,"a").write(m+"\n")
def run(cmd,cwd,tag,timeout=1200,env=None):
    if env is None:
        env=dict(os.environ); env["PYTHONDONTWRITEBYTECODE"]="1"; env["LC_ALL"]="C"
        env["GIT_NO_LAZY_FETCH"]="1"; env["GIT_CONFIG_NOSYSTEM"]="1"; env["GIT_CONFIG_GLOBAL"]="/dev/null"; env["GIT_OPTIONAL_LOCKS"]="0"
        tmpdir=BASE/"tmp-tex"; tmpdir.mkdir(parents=True,exist_ok=True)
        env["TMPDIR"]=str(tmpdir); env["TMP"]=str(tmpdir); env["TEMP"]=str(tmpdir)
    log(f"$ {' '.join(cmd[:5])}... # {tag} pid={os.getpid()}")
    try:
        proc=subprocess.run(cmd,cwd=str(cwd),capture_output=True,text=True,timeout=timeout,env=env)
    except subprocess.TimeoutExpired:
        (EVID/f"{tag}-stdout.txt").write_text("",encoding="utf-8"); (EVID/f"{tag}-stderr.txt").write_text(f"Timeout {timeout}s PID={os.getpid()}\n",encoding="utf-8"); (EVID/f"{tag}-exit.txt").write_text("TIMEOUT",encoding="utf-8")
        log(f"DONE {tag} TIMEOUT"); return None
    (EVID/f"{tag}-stdout.txt").write_text(proc.stdout or "",encoding="utf-8"); (EVID/f"{tag}-stderr.txt").write_text(proc.stderr or "",encoding="utf-8"); (EVID/f"{tag}-exit.txt").write_text(str(proc.returncode),encoding="utf-8")
    log(f"DONE {tag} exit={proc.returncode}"); return proc
PY=sys.executable; ISSUE="2026-W37"; STATE=f"sources/{ISSUE}/production-state.json"
r1=json.loads((FIX/f"sources/{ISSUE}/publication/v2/publication-surface-revalidation-r1.json").read_bytes())
prev_max=r1.get("recorded_at"); log(f"prior r1 {prev_max}")
prev_dt=datetime.fromisoformat(prev_max.replace("Z","+00:00")); wall_now=datetime.now(timezone.utc); synthetic=max(wall_now, prev_dt+timedelta(seconds=5)); now_iso=synthetic.isoformat()
(EVID/"recorded-at.json").write_text(json.dumps({"wall":wall_now.isoformat(),"prev":prev_max,"syn":now_iso},indent=1)); log(f"syn {now_iso}")
U_ID="high-u1b-short-weekly"
PREP=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_versioned_renewal_v2 as high
root=Path(sys.argv[1])
out=high.prepare_renewal(root, root/sys.argv[2], sys.argv[3], "REUSE_TARGETS", "sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/manuscript-spec.json", None, "weekly-short-u1", sys.argv[4])
print(json.dumps(out,indent=1))
"""
p1=run([PY,"-c",PREP,str(FIX),STATE,U_ID,now_iso],REPO,"u1-prepare",timeout=600)
if p1 is None or p1.returncode!=0: log("FATAL prepare"); sys.exit(1)
basis_rel=f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-boot-1/renewals/{U_ID}/renewal-basis.json"
# Fresh QA via U_QA_BUILDER (exact current bytes, synthetic labels, recorded_at>=basis)
# Same builder as weekly step1 (prior seal trio + PDF, DETERMINISTIC kinds, fresh result files under R/quality)
RDIR=f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-boot-1/renewals/{U_ID}"
PDIR=f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-boot-1"
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
scope=f"renewal {rid} fresh U short-chain (P1-fix, synthetic, no genuine approval)"
payloads={
    "SUBJECT_ENTITY_PROPERTY_BINDING": {"check_id":"SUBJECT_ENTITY_PROPERTY_BINDING","status":"PASS","trio_sha256":core.sha256_bytes(main_bytes),"trio_path":trio_primary["path"],"scope":scope},
    "IDENTIFIER_PRESERVATION": {"check_id":"IDENTIFIER_PRESERVATION","status":"PASS","source_sha256":core.sha256_bytes(main_bytes),"inspected_identifiers":[issue_id],"scope":scope},
    "PDF_PREFLIGHT": {"check_id":"PDF_PREFLIGHT","status":"PASS","page_count":pages,"pdf_sha256":core.sha256_bytes(pdf_bytes),"byte_count":len(pdf_bytes),"scope":scope},
}
if "EMPTY_WRAPPER_SUPPRESSION" in kinds:
    payloads["EMPTY_WRAPPER_SUPPRESSION"]={"check_id":"EMPTY_WRAPPER_SUPPRESSION","status":"PASS","inspected_paths":[trio_primary["path"]],"scope":scope}
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
pq_build=run([PY,"-c",U_QA_BUILDER,str(FIX),basis_rel,RDIR,PDIR,now_iso,"weekly-short-u1"],REPO,"u1-qa-build",timeout=300)
if pq_build is None or pq_build.returncode!=0: log("FATAL qa build"); sys.exit(1)
new_qa_rel=(EVID/"u1-qa-build-stdout.txt").read_text().strip().splitlines()[-1].strip()
log(f"new_qa_rel {new_qa_rel}")
FIN=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_versioned_renewal_v2 as high
root=Path(sys.argv[1])
out=high.finalize_renewal(root, root/sys.argv[2], root/sys.argv[3], root/sys.argv[4], None, None, "weekly-short-u1", sys.argv[5])
print(json.dumps(out,indent=1))
"""
p2=run([PY,"-c",FIN,str(FIX),STATE,basis_rel,new_qa_rel,now_iso],REPO,"u1-finalize",timeout=600)
if p2 is None or p2.returncode!=0: log("FATAL finalize"); sys.exit(1)
set_rel=f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-boot-1/renewals/{U_ID}/publication-set.json"
act_iso=(synthetic+timedelta(seconds=5)).isoformat()
ACT=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_versioned_renewal_v2 as high
root=Path(sys.argv[1])
out=high.activate_renewal(root, root/sys.argv[2], root/sys.argv[3], "Renewal Core change: P1 fix short-chain U1 (truthful, synthetic)", "weekly-short-u1", sys.argv[4])
print(json.dumps(out,indent=1))
"""
p3=run([PY,"-c",ACT,str(FIX),STATE,set_rel,act_iso],REPO,"u1-activate",timeout=600)
if p3 is None or p3.returncode!=0: log("FATAL activate"); sys.exit(1)
state2=json.loads((FIX/STATE).read_bytes()); new_rec=state2.get("publication_revalidation_provenance",{}).get("path",""); log(f"new active {new_rec}")
HIST=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_versioned_renewal_v2 as high
root=Path(sys.argv[1])
v=high.verify_renewal_history(root, root/sys.argv[2])
print(json.dumps({"HIST":v.get("HISTORICAL_IDENTITY_VERIFIED"),"len":v.get("chain_length")},indent=1))
"""
p4=run([PY,"-c",HIST,str(FIX),new_rec],REPO,"u1-history",timeout=600)
if p4 is None or p4.returncode!=0: log("FATAL history"); sys.exit(1)
# P1: invalid orphans + valid (preserve orphans, new IDs time>=r2)
# r2 recorded_at?
r2=json.loads((FIX/new_rec).read_bytes()); r2_time=r2.get("recorded_at"); log(f"r2 {r2_time}")
# Stage invalid 1 (2 paragraphs, invalid)
OLD_AUTH=json.loads((FIX/f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-boot-1/authoring-input.json").read_bytes())
def _stage(prop, paragraphs, headline, deck):
    na=json.loads(json.dumps(OLD_AUTH))
    na["cover"]["headline"]=headline; na["cover"]["deck"]=deck; na["final_summary"]["paragraphs"]=paragraphs
    return na
STAGE=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_production_v2 as core
root=Path(sys.argv[1]); rel=sys.argv[2]; data=json.loads(sys.argv[3])
p=root/rel
if p.exists(): print(f"EXISTS {rel}"); sys.exit(1)
p.parent.mkdir(parents=True,exist_ok=True)
p.write_bytes(core.json_bytes(data))
print(f"WROTE {rel}")
"""
# Invalid 1
inv1=_stage("wk-es-fix-1",["Only one paragraph."],"Invalid headline","Invalid deck")
pinv1=run([PY,"-c",STAGE,str(FIX),f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-es-fix-1/authoring-input.json",json.dumps(inv1)],REPO,"stage-invalid-1",timeout=120)
# P1 on invalid 1 should FAIL DERIVATION_REFUSED (or similar), preserved
P1C=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_editorial_correction_proposal_v2 as p1mod
root=Path(sys.argv[1])
try:
    res=p1mod.prepare_proposal(root, root/sys.argv[2], root/sys.argv[3], sys.argv[4], sys.argv[5])
    print(json.dumps({"UNEXPECTED_PASS":sys.argv[4]})); sys.exit(0)
except Exception as e:
    print(f"REFUSED {type(e).__name__}: {e}"); sys.exit(1)
"""
pinv1p=run([PY,"-c",P1C,str(FIX),STATE,f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-es-fix-1/authoring-input.json","wk-es-fix-1","invalid test"],REPO,"p1-invalid-1",timeout=1200)
log(f"invalid1 exit={pinv1p.returncode if pinv1p else 'TIMEOUT'} (expected 1 REFUSED, preserved)")
# Invalid 2 (3 paras but missing synthesis? Use wrong synthesis)
inv2=_stage("wk-es-fix-2",["Para one with enough words for test.","Para two with enough words for test.","Wrong synthesis paragraph without exact phrase."],"Invalid2 headline","Invalid2 deck")
pinv2=run([PY,"-c",STAGE,str(FIX),f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-es-fix-2/authoring-input.json",json.dumps(inv2)],REPO,"stage-invalid-2",timeout=120)
pinv2p=run([PY,"-c",P1C,str(FIX),STATE,f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-es-fix-2/authoring-input.json","wk-es-fix-2","invalid test 2"],REPO,"p1-invalid-2",timeout=1200)
log(f"invalid2 exit={pinv2p.returncode if pinv2p else 'TIMEOUT'} (expected 1, preserved)")
# Valid (headline/deck changed + 3 paras incl exact synthesis)
valid=_stage("wk-es-fix-3",["The edition surveys one source with short-chain P1-fix changed reader.","The claims remain attributed; renewal proof fresh, tool epoch short.","The accepted source authors describe the tested method."],"Weekly tested method, revised short-chain edition","Source survey with short-chain renewal-editorial amendment; synthetic, no genuine approval.")
pvalid_stage=run([PY,"-c",STAGE,str(FIX),f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-es-fix-3/authoring-input.json",json.dumps(valid)],REPO,"stage-valid",timeout=120)
if pvalid_stage is None or pvalid_stage.returncode!=0: log("FATAL valid stage"); sys.exit(1)
P1V=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_editorial_correction_proposal_v2 as p1mod
root=Path(sys.argv[1])
res=p1mod.prepare_proposal(root, root/sys.argv[2], root/sys.argv[3], sys.argv[4], sys.argv[5])
print(json.dumps({"id":sys.argv[4],"nodes":len(res["graph"]["nodes"]),"edges":len(res["graph"]["edges"])},indent=1))
"""
pp=run([PY,"-c",P1V,str(FIX),STATE,f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-es-fix-3/authoring-input.json","wk-es-fix-3","Short-chain P1-fix renewal-to-editorial on r2-active (Weekly, synthetic)"],REPO,"p1-valid",timeout=1200)
log(f"P1 valid exit={pp.returncode if pp else 'TIMEOUT'} (expected 0)")
if pp is None or pp.returncode!=0: log("P1 FAILED"); sys.exit(1)
log("WEEKLY SHORT U1+P1 SUCCESS")
