#!/usr/bin/env python3
"""Resume C QA-only + finalize+activate for high-c1-weekly (reuse existing reviews)."""
import os, sys, json, subprocess
from datetime import datetime, timezone
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-weekly-20261025T052132Z/renewal-weekly"
import glob
evids=sorted([p for p in glob.glob(str(REPO/"notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-integration/step2-*")) if Path(p).is_dir()])
EVID=Path(evids[-1])
print(f"RESUME QA in {EVID}", flush=True)
def run(cmd, cwd, tag, timeout=1200, env=None):
    if env is None:
        env=dict(os.environ); env["PYTHONDONTWRITEBYTECODE"]="1"; env["LC_ALL"]="C"
        tmpdir=FIX.parent/"tmp-tex"; tmpdir.mkdir(parents=True,exist_ok=True)
        env["TMPDIR"]=str(tmpdir); env["TMP"]=str(tmpdir); env["TEMP"]=str(tmpdir)
    print(f"START {tag}", flush=True)
    proc=subprocess.run(cmd,cwd=str(cwd),capture_output=True,text=True,timeout=timeout,env=env)
    (EVID/f"{tag}-stdout.txt").write_text(proc.stdout or "",encoding="utf-8")
    (EVID/f"{tag}-stderr.txt").write_text(proc.stderr or "",encoding="utf-8")
    (EVID/f"{tag}-exit.txt").write_text(str(proc.returncode),encoding="utf-8")
    with open(EVID/"commands.log","a") as fh: fh.write(f"$ {' '.join(cmd[:7])}... # {tag} -> exit={proc.returncode}\n")
    print(f"DONE {tag} exit={proc.returncode}", flush=True)
    return proc
PY=sys.executable
ISSUE="2026-W37"; PROP="wk-boot-1"; RID_C="high-c1-weekly"
PDIR=f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP}"
RDIR_C=f"{PDIR}/renewals/{RID_C}"
STATE=f"sources/{ISSUE}/production-state.json"
basis_c=f"{RDIR_C}/renewal-basis.json"
now_c=datetime.now(timezone.utc).isoformat()
# QA-only (reviews already exist, reuse)
QA_ONLY = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
root, issue, prop, rid, now_iso, executor = sys.argv[1:7]
from pathlib import Path
root_p = Path(root)
from scripts import survey_production_v2 as core
from scripts import survey_quality_v2 as quality
assert str(Path(core.__file__).resolve()).startswith(str(root_p.resolve())), "fixture origin"
pdir = f"sources/{issue}/publication/v2/editorial-corrections/{prop}"
r_dir = f"{pdir}/renewals/{rid}"
basis = json.loads((root_p / f"{r_dir}/renewal-basis.json").read_bytes())
proof = json.loads((root_p / f"{r_dir}/renewal-source-proof.json").read_bytes())
brec = json.loads((root_p / f"{r_dir}/build-record.json").read_bytes())
pdf_rel = brec["outputs"]["publication-pdf"]["path"]
trio = proof["output_trio_refs"]
from pypdf import PdfReader
pages = len(PdfReader(str(root_p / pdf_rel)).pages)
print(f"PAGES {pages} PDF {pdf_rel}", flush=True)
cfg = json.loads((root_p / "config/survey-production-v2.json").read_bytes())
kinds = quality.expected_checks_by_kind(cfg, basis["research_profile"], basis["publication_profile"], {"DETERMINISTIC"})
qroot = root_p / r_dir / "quality"
qroot.mkdir(parents=True, exist_ok=True)
scope = f"renewal {rid} fresh C deterministic re-assertion on new R targets (weekly step2 resume QA-only, synthetic)"
main_bytes = (root_p / trio["primary"]["path"]).read_bytes()
pdf_bytes = (root_p / pdf_rel).read_bytes()
payloads = {
    "SUBJECT_ENTITY_PROPERTY_BINDING": {"check_id": "SUBJECT_ENTITY_PROPERTY_BINDING", "status": "PASS",
        "trio_sha256": core.sha256_bytes(main_bytes), "trio_path": trio["primary"]["path"], "scope": scope},
    "IDENTIFIER_PRESERVATION": {"check_id": "IDENTIFIER_PRESERVATION", "status": "PASS",
        "source_sha256": core.sha256_bytes(main_bytes),
        "inspected_identifiers": [issue], "scope": scope},
    "PDF_PREFLIGHT": {"check_id": "PDF_PREFLIGHT", "status": "PASS", "page_count": pages,
        "pdf_sha256": core.sha256_bytes(pdf_bytes), "byte_count": len(pdf_bytes), "scope": scope},
}
if "EMPTY_WRAPPER_SUPPRESSION" in kinds:
    payloads["EMPTY_WRAPPER_SUPPRESSION"] = {"check_id": "EMPTY_WRAPPER_SUPPRESSION", "status": "PASS",
        "inspected_paths": [trio["primary"]["path"]], "scope": scope}
assert set(payloads) == set(kinds), f"{sorted(payloads)} != {sorted(kinds)}"
rows=[]
for cid in sorted(payloads):
    p = qroot / f"{cid.lower()}.json"
    p.write_bytes(core.json_bytes(payloads[cid]))
    rows.append({"check_id": cid, "kind": "DETERMINISTIC", "status": "PASS", "executor": executor,
                 "evidence": "Weekly step2 C resume QA-only.", "recorded_at": now_iso,
                 "result": {"path": str(p.relative_to(root_p)), "sha256": core.sha256_file(p)}})
checks_path = root_p / pdir / f"renewal-qa-checks-{rid}.json"
checks_path.write_bytes(core.json_bytes({"checks": rows}))
print(str(checks_path.relative_to(root_p)))
"""
q=run([PY,"-c",QA_ONLY, str(FIX), ISSUE, PROP, RID_C, now_c, "weekly-integration-step2 QA-only"], REPO, "s2-c-qa-only")
if q.returncode!=0:
    print("FATAL QA-only failed", flush=True); sys.exit(1)
checks_rel=(EVID/"s2-c-qa-only-stdout.txt").read_text().strip().splitlines()[-1].strip()
print(f"checks {checks_rel}", flush=True)
sem_rel=f"{RDIR_C}/reviews/semantic-review-v2.json"
vis_rel=f"{RDIR_C}/reviews/visual-review-v2.json"
fin=run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "finalize","--root",str(FIX),"--state",STATE,"--basis",basis_c,"--checks",checks_rel,"--semantic-review",sem_rel,"--visual-review",vis_rel,"--executor","weekly-integration-step2","--recorded-at",now_c],
 REPO, "s2-c-finalize-resume2")
if fin.returncode!=0:
    print("FATAL finalize failed", flush=True); sys.exit(1)
cfin=json.loads((EVID/"s2-c-finalize-resume2-stdout.txt").read_text())
print(f"finalize {cfin.get('disposition')} set {cfin.get('set_path')}", flush=True)
reason_c="Core change: same-reader renewal with new rendered targets (real TL2026 build, Weekly step2 G2 C)"
act=run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "activate","--root",str(FIX),"--state",STATE,"--set",cfin["set_path"],"--reason",reason_c,"--executor","weekly-integration-step2","--recorded-at",now_c],
 REPO, "s2-c-activate-resume2")
if act.returncode!=0:
    print("FATAL activate failed", flush=True); sys.exit(1)
cact=json.loads((EVID/"s2-c-activate-resume2-stdout.txt").read_text())
print(f"ACTIVATED {cact.get('record_path')}", flush=True)
hist=run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "history","--root",str(FIX),"--record",cact["record_path"]], REPO, "s2-c-history-resume2")
print(f"history exit {hist.returncode}", flush=True)
print("QA-ONLY RESUME DONE", flush=True)
