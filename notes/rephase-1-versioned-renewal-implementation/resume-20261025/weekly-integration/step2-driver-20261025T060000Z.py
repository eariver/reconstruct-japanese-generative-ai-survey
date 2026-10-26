#!/usr/bin/env python3
"""Weekly STEP2 G2 — U refuse + C real build.
Fresh subprocess per call, 1200s timeout, synthetic fixture labels.
"""
import os, sys, json, subprocess
from datetime import datetime, timezone
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-weekly-20261025T052132Z/renewal-weekly"
STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
EVID = REPO / f"notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-integration/step2-{STAMP}"
EVID.mkdir(parents=True, exist_ok=True)
LOG = EVID / "commands.log"
LOG.write_text("", encoding="utf-8")
def run(cmd, cwd, tag, timeout=1200, env=None):
    if env is None:
        env=dict(os.environ); env["PYTHONDONTWRITEBYTECODE"]="1"; env["LC_ALL"]="C"
        # TeX disposable under workspace TMPDIR (not /tmp quota) if helper honors TMPDIR
        tmpdir = FIX.parent / "tmp-tex"
        tmpdir.mkdir(parents=True, exist_ok=True)
        env["TMPDIR"]=str(tmpdir)
        env["TMP"]=str(tmpdir); env["TEMP"]=str(tmpdir)
    for k in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
        if os.environ.get(k): raise RuntimeError(f"inherited {k}")
    print(f"START {tag} timeout={timeout}s", flush=True)
    proc=subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout, env=env)
    (EVID/f"{tag}-stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (EVID/f"{tag}-stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    (EVID/f"{tag}-exit.txt").write_text(str(proc.returncode), encoding="utf-8")
    with open(LOG,"a") as fh: fh.write(f"$ {' '.join(cmd[:7])}... # {tag} -> exit={proc.returncode}\n")
    print(f"DONE {tag} exit={proc.returncode}", flush=True)
    return proc
PY=sys.executable
ISSUE="2026-W37"; PROP="wk-boot-1"
PDIR=f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP}"
STATE=f"sources/{ISSUE}/production-state.json"
MSPEC=f"{PDIR}/manuscript-spec.json"
TSPEC=f"{PDIR}/toolchain-spec.json"
# old style T must pass own old commit: already proved by step1 U1 PASS at 85eac6f (no edit to old authority)
# record old style SHA vs new
old_style_sha="035645caa06eb77e5416ae7a54bc1fb7b987e0b575a02bd4b512bccb5d683aec"
import hashlib
new_style_data=(FIX/"templates/survey/jgaisurvey.sty").read_bytes()
new_style_sha=hashlib.sha256(new_style_data).hexdigest()
print(f"old_style {old_style_sha} new_style {new_style_sha} changed={old_style_sha!=new_style_sha}", flush=True)
(EVID/"style-change.json").write_text(json.dumps({"old_style_sha":old_style_sha,"new_style_sha":new_style_sha,"new_bytes":len(new_style_data)},indent=1))
# U reuse attempt (should refuse REUSE_TARGET_MISMATCH) — use high-u2-weekly (prior r2)
now_iso=datetime.now(timezone.utc).isoformat()
RID_U="high-u2-weekly"
RDIR_U=f"{PDIR}/renewals/{RID_U}"
u_prep=run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "prepare","--root",str(FIX),"--state",STATE,"--renewal-id",RID_U,"--intent","REUSE_TARGETS","--manuscript-spec",MSPEC,"--executor","weekly-integration-step2","--recorded-at",now_iso],
 REPO, "s2-u-prepare-refuse")
print(f"U prepare exit {u_prep.returncode} (REUSE path: prepare should succeed, finalize should refuse mismatch)", flush=True)
# if prepare succeeded, try QA+finalize to trigger mismatch
if u_prep.returncode==0:
    try: basis_rel=json.loads((EVID/"s2-u-prepare-refuse-stdout.txt").read_text()).get("basis_path", f"{RDIR_U}/renewal-basis.json")
    except: basis_rel=f"{RDIR_U}/renewal-basis.json"
    # QA (same U builder, fresh)
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
scope = f"renewal {rid} U refuse probe (weekly step2, synthetic)"
payloads = {
    "SUBJECT_ENTITY_PROPERTY_BINDING": {"check_id": "SUBJECT_ENTITY_PROPERTY_BINDING", "status": "PASS",
        "trio_sha256": core.sha256_bytes(main_bytes), "trio_path": trio_primary["path"], "scope": scope},
    "IDENTIFIER_PRESERVATION": {"check_id": "IDENTIFIER_PRESERVATION", "status": "PASS",
        "source_sha256": core.sha256_bytes(main_bytes), "inspected_identifiers": [issue_id], "scope": scope},
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
                 "evidence": "Weekly step2 U refuse probe.", "recorded_at": now_iso,
                 "result": {"path": str(p.relative_to(root_p)), "sha256": core.sha256_file(p)}})
checks_path = root_p / pdir / f"renewal-qa-checks-{rid}.json"
checks_path.write_bytes(core.json_bytes({"checks": rows}))
print(str(checks_path.relative_to(root_p)))
"""
    qproc=run([PY,"-c",U_QA, str(FIX), basis_rel, RDIR_U, PDIR, now_iso, "weekly-integration-step2 U refuse"], REPO, "s2-u-qa")
    if qproc.returncode==0:
        checks_rel=(EVID/"s2-u-qa-stdout.txt").read_text().strip().splitlines()[-1].strip()
        fproc=run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
         "finalize","--root",str(FIX),"--state",STATE,"--basis",basis_rel,"--checks",checks_rel,"--executor","weekly-integration-step2","--recorded-at",now_iso],
         REPO, "s2-u-finalize-refuse")
        print(f"U finalize exit {fproc.returncode} (REUSE_TARGET_MISMATCH expected)", flush=True)
        try: print(open(EVID/"s2-u-finalize-refuse-stderr.txt").read()[:2000], flush=True)
        except: pass
    else:
        print("U QA failed, cannot test finalize mismatch", flush=True)
else:
    print("U prepare itself refused (check stderr for REUSE_TARGET_MISMATCH vs other)", flush=True)
    try: print(open(EVID/"s2-u-prepare-refuse-stderr.txt").read()[:2000], flush=True)
    except: pass
# Keep failed U root inert: do NOT delete RDIR_U, use new ID for C
# Fresh C: high-c1-weekly (prior r2) with REAL TL2026 build
RID_C="high-c1-weekly"; RDIR_C=f"{PDIR}/renewals/{RID_C}"
now_c=datetime.now(timezone.utc).isoformat()
c_prep=run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "prepare","--root",str(FIX),"--state",STATE,"--renewal-id",RID_C,"--intent","RENDER_TARGETS","--manuscript-spec",MSPEC,"--toolchain-spec",TSPEC,"--executor","weekly-integration-step2","--recorded-at",now_c],
 REPO, "s2-c-prepare")
if c_prep.returncode!=0:
    print("FATAL C prepare failed", flush=True); sys.exit(1)
try: basis_c=json.loads((EVID/"s2-c-prepare-stdout.txt").read_text()).get("basis_path", f"{RDIR_C}/renewal-basis.json")
except: basis_c=f"{RDIR_C}/renewal-basis.json"
print(f"C basis {basis_c}", flush=True)
c_targ=run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "prepare-targets","--root",str(FIX),"--basis",basis_c,"--executor","weekly-integration-step2","--recorded-at",now_c],
 REPO, "s2-c-targets")
if c_targ.returncode!=0:
    print("FATAL C targets (real build) failed", flush=True)
    try: print(open(EVID/"s2-c-targets-stderr.txt").read()[:5000], flush=True)
    except: pass
    sys.exit(1)
print("C targets (real build) OK", flush=True)
# C reviews+QA (real postrender, synthetic fixture labels)
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
import subprocess as _sp
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
scope = f"renewal {rid} fresh C deterministic re-assertion on new R targets (weekly step2, synthetic, no genuine approval)"
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
                 "evidence": "Weekly step2 C fresh deterministic re-assertion: exact new R bytes inspected, synthetic.",
                 "recorded_at": now_iso,
                 "result": {"path": str(p.relative_to(root_p)), "sha256": core.sha256_file(p)}})
checks_path = root_p / pdir / f"renewal-qa-checks-{rid}.json"
checks_path.write_bytes(core.json_bytes({"checks": rows}))
out["checks"] = str(checks_path.relative_to(root_p))
print(json.dumps(out, indent=1))
"""
c_qa=run([PY,"-c",C_QA, str(FIX), ISSUE, PROP, RID_C, now_c, "weekly-integration-step2 C fresh"], REPO, "s2-c-reviews-qa")
if c_qa.returncode!=0:
    print("FATAL C reviews-qa failed", flush=True); sys.exit(1)
outs=json.loads((EVID/"s2-c-reviews-qa-stdout.txt").read_text())
sem_rel=outs["SEMANTIC_EDITORIAL"]; vis_rel=outs["VISUAL"]; checks_rel=outs["checks"]
c_fin=run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "finalize","--root",str(FIX),"--state",STATE,"--basis",basis_c,"--checks",checks_rel,"--semantic-review",sem_rel,"--visual-review",vis_rel,"--executor","weekly-integration-step2","--recorded-at",now_c],
 REPO, "s2-c-finalize")
if c_fin.returncode!=0:
    print("FATAL C finalize failed", flush=True); sys.exit(1)
cfin=json.loads((EVID/"s2-c-finalize-stdout.txt").read_text())
print(f"C finalize {cfin.get('disposition')} set {cfin.get('set_path')}", flush=True)
# verify build-record BEFORE receipt, no companions sidecar, full set match (check files exist, receipt binds build)
brec_path=f"{RDIR_C}/build-record.json"
receipt_path=cfin.get("receipt_path") or f"{RDIR_C}/validated-source-manifest.json"
print(f"build {brec_path} receipt {receipt_path}", flush=True)
# activate C
reason_c="Core change: same-reader renewal with new rendered targets (real TL2026 build, Weekly step2 G2 C)"
c_act=run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "activate","--root",str(FIX),"--state",STATE,"--set",cfin["set_path"],"--reason",reason_c,"--executor","weekly-integration-step2","--recorded-at",now_c],
 REPO, "s2-c-activate")
if c_act.returncode!=0:
    print("FATAL C activate failed", flush=True); sys.exit(1)
cact=json.loads((EVID/"s2-c-activate-stdout.txt").read_text())
print(f"C ACTIVATED {cact.get('record_path')}", flush=True)
c_hist=run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "history","--root",str(FIX),"--record",cact["record_path"]], REPO, "s2-c-history")
print(f"C history exit {c_hist.returncode}", flush=True)
print("STEP2 DONE", flush=True)
