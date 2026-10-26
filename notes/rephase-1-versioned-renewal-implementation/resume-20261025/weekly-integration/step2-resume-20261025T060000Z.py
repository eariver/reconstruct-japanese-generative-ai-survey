#!/usr/bin/env python3
"""Resume C high-c1-weekly after harness bug fix — reviews-qa+finalize+activate only.
Preserves existing basis/targets/build partial, no deletion.
"""
import os, sys, json, subprocess
from datetime import datetime, timezone
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-weekly-20261025T052132Z/renewal-weekly"
# find latest step2 evid dir (directory only)
import glob
evids=sorted([p for p in glob.glob(str(REPO/"notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-integration/step2-*")) if Path(p).is_dir()])
EVID=Path(evids[-1])
print(f"RESUME in {EVID}", flush=True)
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
# need now_c later than original prepare (use now)
now_c=datetime.now(timezone.utc).isoformat()
print(f"now_c {now_c}", flush=True)
C_QA = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
root, issue, prop, rid, now_iso, executor = sys.argv[1:7]
from pathlib import Path
root_p = Path(root)
sys.path.insert(0, str(root_p))
from scripts import survey_production_v2 as core
from scripts import survey_quality_v2 as quality
from scripts import survey_reader_publication_v2 as reader_pub
assert str(Path(core.__file__).resolve()).startswith(str(root_p.resolve())), "fixture import origin"
pdir = f"sources/{issue}/publication/v2/editorial-corrections/{prop}"
r_dir = f"{pdir}/renewals/{rid}"
basis = json.loads((root_p / f"{r_dir}/renewal-basis.json").read_bytes())
proof = json.loads((root_p / f"{r_dir}/renewal-source-proof.json").read_bytes())
proof_ref = {"path": f"{r_dir}/renewal-source-proof.json",
             "sha256": __import__("hashlib").sha256((root_p / f"{r_dir}/renewal-source-proof.json").read_bytes()).hexdigest()}
man_rel = f"{r_dir}/reader-manuscript-v2.json"
trio = proof["output_trio_refs"]
from pypdf import PdfReader
brec = json.loads((root_p / f"{r_dir}/build-record.json").read_bytes())
pdf_rel = brec["outputs"]["publication-pdf"]["path"]
pages = len(PdfReader(str(root_p / pdf_rel)).pages)
rev_dir = root_p / r_dir / "reviews"
rev_dir.mkdir(parents=True, exist_ok=True)
out = {}
man_doc = json.loads((root_p / man_rel).read_bytes())
def _ev(cid):
    return [f"renewal-c:{rid}:{trio['primary']['path']}"]
for kind_name, fname in (("SEMANTIC_EDITORIAL", "semantic-review-v2.json"), ("VISUAL", "visual-review-v2.json")):
    checks = [{"check_id": cid, "status": "PASS",
               "detail": f"Renewal C fixture synthetic {kind_name} reviewer on new R targets; no genuine approval.",
               "evidence_locations": _ev(cid)}
              for cid in sorted(reader_pub._expected_review_checks(root_p, core.load_json(root_p / basis["profile_ref"]["path"]), kind_name))]
    reader_pub.build_review_record(
        root_p, root_p / man_rel, root_p / pdf_rel, pages, kind_name, checks,
        f"renewal-c-fixture synthetic {kind_name} reviewer; no genuine approval",
        __import__("datetime").datetime.fromisoformat(now_iso), rev_dir / fname,
        renewal_source_proof_ref=dict(proof_ref))
    out[kind_name] = str((rev_dir / fname).relative_to(root_p))
cfg = json.loads((root_p / "config/survey-production-v2.json").read_bytes())
kinds = quality.expected_checks_by_kind(cfg, basis["research_profile"], basis["publication_profile"], {"DETERMINISTIC"})
qroot = root_p / r_dir / "quality"
qroot.mkdir(parents=True, exist_ok=True)
scope = f"renewal {rid} fresh C deterministic re-assertion on new R targets (weekly step2 resume, synthetic, no genuine approval)"
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
rows = []
for cid in sorted(payloads):
    p = qroot / f"{cid.lower()}.json"
    p.write_bytes(core.json_bytes(payloads[cid]))
    rows.append({"check_id": cid, "kind": "DETERMINISTIC", "status": "PASS", "executor": executor,
                 "evidence": "Weekly step2 C resume: exact new R bytes inspected, synthetic.",
                 "recorded_at": now_iso,
                 "result": {"path": str(p.relative_to(root_p)), "sha256": core.sha256_file(p)}})
checks_path = root_p / pdir / f"renewal-qa-checks-{rid}.json"
checks_path.write_bytes(core.json_bytes({"checks": rows}))
out["checks"] = str(checks_path.relative_to(root_p))
print(json.dumps(out, indent=1))
"""
c_qa=run([PY,"-c",C_QA, str(FIX), ISSUE, PROP, RID_C, now_c, "weekly-integration-step2 C resume"], REPO, "s2-c-reviews-qa-resume")
if c_qa.returncode!=0:
    print("FATAL resume QA failed", flush=True); sys.exit(1)
outs=json.loads((EVID/"s2-c-reviews-qa-resume-stdout.txt").read_text())
sem_rel=outs["SEMANTIC_EDITORIAL"]; vis_rel=outs["VISUAL"]; checks_rel=outs["checks"]
c_fin=run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "finalize","--root",str(FIX),"--state",STATE,"--basis",basis_c,"--checks",checks_rel,"--semantic-review",sem_rel,"--visual-review",vis_rel,"--executor","weekly-integration-step2","--recorded-at",now_c],
 REPO, "s2-c-finalize-resume")
if c_fin.returncode!=0:
    print("FATAL resume finalize failed", flush=True); sys.exit(1)
cfin=json.loads((EVID/"s2-c-finalize-resume-stdout.txt").read_text())
print(f"C finalize resume {cfin.get('disposition')} set {cfin.get('set_path')}", flush=True)
reason_c="Core change: same-reader renewal with new rendered targets (real TL2026 build, Weekly step2 G2 C)"
c_act=run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "activate","--root",str(FIX),"--state",STATE,"--set",cfin["set_path"],"--reason",reason_c,"--executor","weekly-integration-step2","--recorded-at",now_c],
 REPO, "s2-c-activate-resume")
if c_act.returncode!=0:
    print("FATAL resume activate failed", flush=True); sys.exit(1)
cact=json.loads((EVID/"s2-c-activate-resume-stdout.txt").read_text())
print(f"C ACTIVATED resume {cact.get('record_path')}", flush=True)
c_hist=run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "history","--root",str(FIX),"--record",cact["record_path"]], REPO, "s2-c-history-resume")
print(f"C history resume exit {c_hist.returncode}", flush=True)
print("RESUME DONE", flush=True)
