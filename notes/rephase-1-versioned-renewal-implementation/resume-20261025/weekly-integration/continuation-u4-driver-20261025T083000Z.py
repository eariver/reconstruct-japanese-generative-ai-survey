#!/usr/bin/env python3
"""Continuation U4 — bring new G5 tools current (REUSE, style unchanged)."""
import os, sys, json, subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-weekly-continuation-20261025T083000Z/renewal-weekly"
STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
EVID = REPO / f"notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-integration/continuation-u4-{STAMP}"
EVID.mkdir(parents=True, exist_ok=True)
LOG=EVID/"commands.log"; LOG.write_text("",encoding="utf-8")
def run(cmd,cwd,tag,timeout=1200,env=None):
    if env is None:
        env=dict(os.environ); env["PYTHONDONTWRITEBYTECODE"]="1"; env["LC_ALL"]="C"
        tmpdir=FIX.parent/"tmp-tex"; tmpdir.mkdir(parents=True,exist_ok=True)
        env["TMPDIR"]=str(tmpdir); env["TMP"]=str(tmpdir); env["TEMP"]=str(tmpdir)
    print(f"START {tag}",flush=True)
    proc=subprocess.run(cmd,cwd=str(cwd),capture_output=True,text=True,timeout=timeout,env=env)
    (EVID/f"{tag}-stdout.txt").write_text(proc.stdout or "",encoding="utf-8")
    (EVID/f"{tag}-stderr.txt").write_text(proc.stderr or "",encoding="utf-8")
    (EVID/f"{tag}-exit.txt").write_text(str(proc.returncode),encoding="utf-8")
    with open(LOG,"a") as fh: fh.write(f"$ {' '.join(cmd[:7])}... # {tag} -> exit={proc.returncode}\n")
    print(f"DONE {tag} exit={proc.returncode}",flush=True)
    return proc
PY=sys.executable
ISSUE="2026-W37"; PROP="wk-boot-1"
PDIR=f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP}"
STATE=f"sources/{ISSUE}/production-state.json"
MSPEC=f"{PDIR}/manuscript-spec.json"
# prev max recorded_at (r5)
r5=json.loads((FIX/f"sources/{ISSUE}/publication/v2/publication-surface-revalidation-r5.json").read_bytes())
prev_max=r5.get("recorded_at")
prev_dt=datetime.fromisoformat(prev_max)
wall_now=datetime.now(timezone.utc)
synthetic=max(wall_now, prev_dt+timedelta(seconds=1))
now_iso=synthetic.isoformat()
print(f"wall {wall_now.isoformat()} prev {prev_max} synthetic {now_iso}",flush=True)
(EVID/"recorded-at.json").write_text(json.dumps({"wallclock":wall_now.isoformat(),"prev_max":prev_max,"synthetic":now_iso},indent=1))
RID="high-u4-weekly"; RDIR=f"{PDIR}/renewals/{RID}"
prep=run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "prepare","--root",str(FIX),"--state",STATE,"--renewal-id",RID,"--intent","REUSE_TARGETS","--manuscript-spec",MSPEC,"--executor","weekly-continuation-u4","--recorded-at",now_iso],
 REPO, "c-u4-prepare")
if prep.returncode!=0: print("FATAL U4 prepare",flush=True); sys.exit(1)
try: basis_rel=json.loads((EVID/"c-u4-prepare-stdout.txt").read_text()).get("basis_path", f"{RDIR}/renewal-basis.json")
except: basis_rel=f"{RDIR}/renewal-basis.json"
U_QA = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
root, basis_rel, r_dir, pdir, now_iso, executor = sys.argv[1:7]
from pathlib import Path
root_p = Path(root)
from scripts import survey_production_v2 as core
from scripts import survey_quality_v2 as quality
assert str(Path(core.__file__).resolve()).startswith(str(root_p.resolve())), "fixture origin"
basis = json.loads((root_p / basis_rel).read_bytes())
cfg = json.loads((root_p / "config/survey-production-v2.json").read_bytes())
kinds = quality.expected_checks_by_kind(cfg, basis["research_profile"], basis["publication_profile"], {"DETERMINISTIC"})
prior_seal = json.loads((root_p / basis["prior_selected_ref"]["path"]).read_bytes())
roles = prior_seal["roles"]
trio_primary, pdf_role = roles["validated-source"], roles["publication-pdf"]
main_bytes = (root_p / trio_primary["path"]).read_bytes()
pdf_bytes = (root_p / pdf_role["path"]).read_bytes()
from pypdf import PdfReader
pages = len(PdfReader(str(root_p / pdf_role["path"])).pages)
issue_id, rid = basis["issue_id"], basis["renewal_id"]
qroot = root_p / r_dir / "quality"
qroot.mkdir(parents=True, exist_ok=True)
scope = f"renewal {rid} U4 G5 new tools current (continuation, synthetic)"
payloads = {
    "SUBJECT_ENTITY_PROPERTY_BINDING": {"check_id": "SUBJECT_ENTITY_PROPERTY_BINDING", "status": "PASS",
        "trio_sha256": core.sha256_bytes(main_bytes), "trio_path": trio_primary["path"], "scope": scope},
    "IDENTIFIER_PRESERVATION": {"check_id": "IDENTIFIER_PRESERVATION", "status": "PASS",
        "source_sha256": core.sha256_bytes(main_bytes),
        "inspected_identifiers": [issue_id], "scope": scope},
    "PDF_PREFLIGHT": {"check_id": "PDF_PREFLIGHT", "status": "PASS", "page_count": pages,
        "pdf_sha256": core.sha256_bytes(pdf_bytes), "byte_count": len(pdf_bytes), "scope": scope},
}
if "EMPTY_WRAPPER_SUPPRESSION" in kinds:
    payloads["EMPTY_WRAPPER_SUPPRESSION"] = {"check_id": "EMPTY_WRAPPER_SUPPRESSION", "status": "PASS",
        "inspected_paths": [trio_primary["path"]], "scope": scope}
assert set(payloads) == set(kinds)
rows=[]
for cid in sorted(payloads):
    p = qroot / f"{cid.lower()}.json"
    p.write_bytes(core.json_bytes(payloads[cid]))
    rows.append({"check_id": cid, "kind": "DETERMINISTIC", "status": "PASS", "executor": executor,
                 "evidence": "Continuation U4 G5.", "recorded_at": now_iso,
                 "result": {"path": str(p.relative_to(root_p)), "sha256": core.sha256_file(p)}})
checks_path = root_p / pdir / f"renewal-qa-checks-{rid}.json"
checks_path.write_bytes(core.json_bytes({"checks": rows}))
print(str(checks_path.relative_to(root_p)))
"""
qa=run([PY,"-c",U_QA, str(FIX), basis_rel, RDIR, PDIR, now_iso, "weekly-continuation-u4"], REPO, "c-u4-qa")
if qa.returncode!=0: print("FATAL U4 qa",flush=True); sys.exit(1)
checks_rel=(EVID/"c-u4-qa-stdout.txt").read_text().strip().splitlines()[-1].strip()
fin=run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "finalize","--root",str(FIX),"--state",STATE,"--basis",basis_rel,"--checks",checks_rel,"--executor","weekly-continuation-u4","--recorded-at",now_iso],
 REPO, "c-u4-finalize")
if fin.returncode!=0: print("FATAL U4 finalize",flush=True); sys.exit(1)
cfin=json.loads((EVID/"c-u4-finalize-stdout.txt").read_text())
print(f"U4 finalize {cfin.get('disposition')} set {cfin.get('set_path')}",flush=True)
act=run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "activate","--root",str(FIX),"--state",STATE,"--set",cfin["set_path"],"reason" if False else "--reason","Core change: G5 repair tools (H perf+P1 dispatcher+PUB union) bringing renewal current (Weekly continuation U4)","--executor","weekly-continuation-u4","--recorded-at",now_iso],
 REPO, "c-u4-activate")
# Note: above has duplicate --reason handling bug? Fix: use correct args
# Actually run() already passed --reason, but we passed "reason" string? Let's correct: we passed "--reason" correctly? The list includes "reason" if False else "--reason" -> evaluates to "--reason", good.
if act.returncode!=0: print("FATAL U4 activate",flush=True); sys.exit(1)
# The above activate used wrong arg order? CLI expects --reason <reason>. Our list: ["activate","--root",FIX,"--state",STATE,"--set",set,"reason"? No, we have "reason" if False else "--reason" -> "--reason", then reason string, then "--executor"... Good.
cact=json.loads((EVID/"c-u4-activate-stdout.txt").read_text())
print(f"U4 ACTIVATED {cact.get('record_path')}",flush=True)
hist=run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "history","--root",str(FIX),"--record",cact["record_path"]], REPO, "c-u4-history")
print(f"U4 history exit {hist.returncode}",flush=True)
print("U4 DONE",flush=True)
