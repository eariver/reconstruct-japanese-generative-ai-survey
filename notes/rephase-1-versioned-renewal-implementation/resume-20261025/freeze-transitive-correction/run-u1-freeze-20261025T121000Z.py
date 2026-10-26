#!/usr/bin/env python3
"""Freeze-transitive FULL Freeze V2 — fresh weekly U1 (REUSE) + synthetic Preview + Freeze.
Corrected CLI (basis/checks/set/receipt/record) per weekly step1. 1200s bound, PID logs.
Preserves V1 harness-bug failure (missing args) in run-u1-freeze-20261025T120000Z/ (not deleted).
"""
import os, sys, json, subprocess, hashlib, time
from datetime import datetime, timezone
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-freeze-transitive-20261025T120000Z/renewal-weekly"
STAMP = "20261025T121000Z"
EVID = REPO / f"notes/rephase-1-versioned-renewal-implementation/resume-20261025/freeze-transitive-correction/run-u1-freeze-{STAMP}"
EVID.mkdir(parents=True, exist_ok=True)
LOG = EVID / "commands.log"
LOG.write_text("", encoding="utf-8")
def log_cmd(cmd, tag, rc, dur=None):
    with open(LOG, "a") as fh:
        fh.write(f"$ {' '.join(cmd[:8])}... # {tag} -> exit={rc} dur={dur}\n")
def run(cmd, cwd, tag, timeout=1200, env=None):
    if env is None:
        env = dict(os.environ)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["LC_ALL"] = "C"
        tmpdir = FIX.parent / "tmp-tex"
        tmpdir.mkdir(parents=True, exist_ok=True)
        env["TMPDIR"] = str(tmpdir); env["TMP"] = str(tmpdir); env["TEMP"] = str(tmpdir)
    for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        if os.environ.get(k):
            raise RuntimeError(f"inherited {k}")
    print(f"START {tag} pid={os.getpid()} timeout={timeout}s", flush=True)
    t0 = time.time()
    try:
        proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout, env=env)
    except subprocess.TimeoutExpired:
        dur = time.time() - t0
        print(f"TIMEOUT {tag} after {dur:.1f}s (profile, no fake PASS)", flush=True)
        (EVID/f"{tag}-timeout.txt").write_text(f"timeout after {dur:.1f}s\n", encoding="utf-8")
        raise
    dur = time.time() - t0
    (EVID/f"{tag}-stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (EVID/f"{tag}-stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    (EVID/f"{tag}-exit.txt").write_text(str(proc.returncode), encoding="utf-8")
    (EVID/f"{tag}-dur.txt").write_text(f"{dur:.2f}\n", encoding="utf-8")
    log_cmd(cmd, tag, proc.returncode, f"{dur:.2f}s")
    print(f"DONE {tag} exit={proc.returncode} dur={dur:.2f}s", flush=True)
    return proc
PY = sys.executable
ISSUE = "2026-W37"; PROP = "wk-boot-1"; RID = "high-u1-weekly"
PDIR = f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP}"
RDIR = f"{PDIR}/renewals/{RID}"
STATE = f"sources/{ISSUE}/production-state.json"
MSPEC = f"{PDIR}/manuscript-spec.json"
now_iso = datetime.now(timezone.utc).isoformat()
print(f"RUN STAMP {STAMP} FIX {FIX} HEAD {subprocess.run(['git','--no-optional-locks','rev-parse','HEAD'],cwd=str(FIX),capture_output=True,text=True).stdout.strip()}", flush=True)
(EVID/"now-iso.txt").write_text(now_iso, encoding="utf-8")
(EVID/"recorded-at.json").write_text(json.dumps({"recorded_at": now_iso}, indent=1))
p1 = run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "prepare","--root",str(FIX),"--state",STATE,"--renewal-id",RID,"--intent","REUSE_TARGETS","--manuscript-spec",MSPEC,"--executor","freeze-transitive-u1","--recorded-at",now_iso],
 REPO, "u1-prepare")
if p1.returncode != 0:
    print("FATAL prepare failed", flush=True); sys.exit(1)
try:
    j = json.loads((EVID/"u1-prepare-stdout.txt").read_text())
    basis_rel = j.get("basis_path") or f"{RDIR}/renewal-basis.json"
except:
    basis_rel = f"{RDIR}/renewal-basis.json"
print(f"basis_rel {basis_rel}", flush=True)
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
# write quality result files under r_dir/quality (for finalize checks? finalize needs checks file, not quality dir)
# For U finalize, checks file is pdir/renewal-qa-checks-<rid>.json with rows {check_id,path,sha256,...}? Actually weekly step1 U_QA writes checks file, not quality dir.
# Reuse weekly step1 exact U_QA that writes checks file:
qroot = root_p / r_dir / "quality"
qroot.mkdir(parents=True, exist_ok=True)
scope = f"renewal {rid} fresh U bootstrap (freeze-transitive V2, synthetic fixture, no genuine approval)"
# Build payloads then checks file at pdir/renewal-qa-checks-<rid>.json
from scripts import survey_production_v2 as core2
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
assert set(payloads) == set(kinds), f"{sorted(payloads)} != {sorted(kinds)}"
rows = []
for cid in sorted(payloads):
    # Write each check result under r_dir/quality/<cid>.json then reference in checks file
    p = qroot / f"{cid.lower()}.json"
    p.write_bytes(core.json_bytes(payloads[cid]))
    rows.append({"check_id": cid, "kind": "DETERMINISTIC", "status": "PASS", "executor": executor,
                 "evidence": "freeze-transitive V2 fresh re-assertion: exact current bytes inspected, synthetic fixture.",
                 "recorded_at": now_iso,
                 "result": {"path": str(p.relative_to(root_p)), "sha256": core.sha256_file(p)}})
checks_path = root_p / pdir / f"renewal-qa-checks-{rid}.json"
checks_path.write_bytes(core.json_bytes({"checks": rows}))
print(str(checks_path.relative_to(root_p)))
"""
qa = run([PY,"-c",U_QA, str(FIX), basis_rel, RDIR, PDIR, now_iso, "freeze-transitive-u1"], REPO, "u1-qa")
if qa.returncode != 0:
    print("FATAL qa failed", flush=True); sys.exit(1)
checks_rel = (EVID/"u1-qa-stdout.txt").read_text().strip().splitlines()[-1].strip()
print(f"checks_rel {checks_rel}", flush=True)
fin = run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "finalize","--root",str(FIX),"--state",STATE,"--basis",basis_rel,"--checks",checks_rel,"--executor","freeze-transitive-u1","--recorded-at",now_iso],
 REPO, "u1-finalize")
if fin.returncode != 0:
    print("FATAL finalize failed", flush=True); sys.exit(1)
finj = json.loads((EVID/"u1-finalize-stdout.txt").read_text())
set_path = finj["set_path"]
print(f"set_path {set_path} disposition {finj.get('disposition')}", flush=True)
receipt_rel = finj.get("receipt_path") or finj.get("receipt_rel") or f"{RDIR}/validated-source-manifest.json"
try:
    receipt_rel = finj.get("receipt_path", receipt_rel)
except:
    pass
vs = run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "validate-set","--root",str(FIX),"--state",STATE,"--set",set_path], REPO, "u1-validate-set")
if vs.returncode != 0:
    print("FATAL validate-set failed", flush=True); sys.exit(1)
vr = run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "validate-receipt","--root",str(FIX),"--receipt",receipt_rel], REPO, "u1-validate-receipt")
if vr.returncode != 0:
    print("FATAL validate-receipt failed", flush=True); sys.exit(1)
reason = "Core change: freeze-transitive U1 (PUB shared wrapper + M1-M6)"
act = run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "activate","--root",str(FIX),"--state",STATE,"--set",set_path,"--reason",reason,"--executor","freeze-transitive-u1","--recorded-at",now_iso],
 REPO, "u1-activate")
if act.returncode != 0:
    print("FATAL activate failed", flush=True); sys.exit(1)
actj = json.loads((EVID/"u1-activate-stdout.txt").read_text())
record_path = actj["record_path"]
print(f"ACTIVATED {record_path} observed {actj.get('observed')}", flush=True)
hist = run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "history","--root",str(FIX),"--record",record_path], REPO, "u1-history")
if hist.returncode != 0:
    print("FATAL history failed", flush=True); sys.exit(1)
print("U1 DONE, proceeding to synthetic Preview+Freeze", flush=True)
LIFECYCLE = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
root, issue, prop, rid, now_iso = sys.argv[1:6]
from pathlib import Path
from datetime import datetime
root_p = Path(root)
from scripts import survey_production_v2 as core
from scripts import survey_stage_validation_v2 as stage
from scripts import survey_publication_v2 as pubmod
from scripts import survey_publication_set_v2 as setmod
assert str(Path(core.__file__).resolve()).startswith(str(root_p.resolve())), "fixture origin"
cfg = json.loads((root_p / "config/survey-production-v2.json").read_bytes())
state_path = root_p / f"sources/{issue}/production-state.json"
state = json.loads(state_path.read_bytes())
sel = setmod.resolve_publication_selection(root_p, cfg, state)
assert sel.get("mode") == "VERSIONED_ACTIVE", sel.get("mode")
pdir = f"sources/{issue}/publication/v2/editorial-corrections/{prop}"
r_dir = f"{pdir}/renewals/{rid}"
seal = json.loads((root_p / f"{r_dir}/publication-set.json").read_bytes())
roles = seal["roles"]
supplied = {"publication-candidate": root_p / roles["publication-candidate"]["path"],}
now = datetime.fromisoformat(now_iso)
stage_out = root_p / pdir / f"lifecycle-stage-{rid}.json"
stage.validate_stage(root_p, cfg, state_path, supplied, stage_out, now)
lc_dir = root_p / pdir / f"lifecycle-{rid}"
lc_dir.mkdir(parents=True, exist_ok=True)
appr = lc_dir / "preview-approval.json"
pubmod.build_preview_approval(root_p, supplied["publication-candidate"], appr,
    "freeze-transitive synthetic preview reviewer; NO genuine Human approval",
    now, f"freeze-transitive:{rid}:synthetic-preview")
pubmod.validate_preview_approval(root_p, appr, issue_id=issue)
frz = lc_dir / "freeze-record.json"
man = lc_dir / "release-manifest.json"
pubmod.build_freeze(root_p, supplied["publication-candidate"], appr, now, frz, man)
pubmod.validate_release_manifest(root_p, man)
from pypdf import PdfReader
pdf_path = root_p / roles["publication-pdf"]["path"]
pages = len(PdfReader(str(pdf_path)).pages)
print(json.dumps({"stage":str(stage_out.relative_to(root_p)),"approval":str(appr.relative_to(root_p)),
 "freeze":str(frz.relative_to(root_p)),"manifest":str(man.relative_to(root_p)),
 "candidate_sha":__import__("hashlib").sha256((root_p / roles["publication-candidate"]["path"]).read_bytes()).hexdigest()[:12],
 "pdf_pages":pages,"pdf_sha":__import__("hashlib").sha256(pdf_path.read_bytes()).hexdigest()},indent=1))
"""
state_before = (FIX / f"sources/{ISSUE}/production-state.json").read_bytes()
lc = run([PY,"-c",LIFECYCLE, str(FIX), ISSUE, PROP, RID, now_iso], REPO, "u1-lifecycle-freeze")
print(f"lifecycle exit {lc.returncode}", flush=True)
if lc.returncode != 0:
    print("FATAL lifecycle Freeze failed (shared wrapper/M1-M6 still open?)", flush=True); sys.exit(1)
state_after = (FIX / f"sources/{ISSUE}/production-state.json").read_bytes()
print(f"State pinned={state_before==state_after} (no mutation expected, Preview synthetic)", flush=True)
(EVID/"state-pinned.json").write_text(json.dumps({"pinned": state_before==state_after}, indent=1))
print("FULL FREEZE SUCCESS", flush=True)
