#!/usr/bin/env python3
"""Weekly integration STEP1 — bootstrap U1 + controls on FIXED G1.
Fresh subprocess per public call, FILE refs only, synthetic fixture QA labels.
Covers: U prepare/finalize/activate/history + CURRENT readback, LIVE State,
old receipt stale note, artifact-only descendant PASS, ALREADY_ACTIVE + alias refusals,
no-write alias/style/reason/wrong-target controls.
"""
import os, sys, json, subprocess, hashlib
from datetime import datetime, timezone
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
STAMP_SETUP = "20261025T052132Z"
FIX = REPO / f".rephase-1-editorial-runtime/versioned-renewal-weekly-{STAMP_SETUP}/renewal-weekly"
STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
EVID = REPO / f"notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-integration/step1-{STAMP}"
EVID.mkdir(parents=True, exist_ok=True)
LOG = EVID / "commands.log"
LOG.write_text("", encoding="utf-8")
def log_cmd(cmd, tag, rc):
    with open(LOG, "a") as fh:
        fh.write(f"$ {' '.join(cmd[:7])}... # {tag} -> exit={rc}\n")
def run(cmd, cwd, tag, timeout=1200, env=None):
    if env is None:
        env = dict(os.environ)
        env["PYTHONDONTWRITEBYTECODE"]="1"
        env["LC_ALL"]="C"
    for k in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
        if os.environ.get(k):
            raise RuntimeError(f"inherited {k}")
    # heartbeat: print PID
    print(f"START {tag} pid-subprocess timeout={timeout}s", flush=True)
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout, env=env)
    (EVID/f"{tag}-stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (EVID/f"{tag}-stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    (EVID/f"{tag}-exit.txt").write_text(str(proc.returncode), encoding="utf-8")
    log_cmd(cmd, tag, proc.returncode)
    print(f"DONE {tag} exit={proc.returncode}", flush=True)
    return proc
PY = sys.executable
ISSUE="2026-W37"; PROP="wk-boot-1"; RID="high-u1-weekly"
PDIR=f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP}"
RDIR=f"{PDIR}/renewals/{RID}"
STATE=f"sources/{ISSUE}/production-state.json"
MSPEC=f"{PDIR}/manuscript-spec.json"
now_iso = datetime.now(timezone.utc).isoformat()
print(f"STEP1 STAMP {STAMP} FIX {FIX} HEAD {subprocess.run(['git','--no-optional-locks','rev-parse','HEAD'],cwd=str(FIX),capture_output=True,text=True).stdout.strip()}", flush=True)
# 1a prepare U
p1 = run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "prepare","--root",str(FIX),"--state",STATE,"--renewal-id",RID,"--intent","REUSE_TARGETS","--manuscript-spec",MSPEC,"--executor","weekly-integration-step1","--recorded-at",now_iso],
 REPO, "s1-prepare-u1")
if p1.returncode!=0:
    print("FATAL prepare failed", flush=True); sys.exit(1)
basis_rel = json.loads((EVID/"s1-prepare-u1-stdout.txt").read_text())["basis_path"] if False else None
# parse basis_path from stdout JSON (contains renewal_dir etc? prepare prints basis_path)
try:
    j=json.loads((EVID/"s1-prepare-u1-stdout.txt").read_text())
    basis_rel=j.get("basis_path") or f"{RDIR}/renewal-basis.json"
except: basis_rel=f"{RDIR}/renewal-basis.json"
print(f"basis_rel {basis_rel}", flush=True)
# 1b QA fresh (U_QA_BUILDER inline, fixture-first, synthetic labels)
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
scope = f"renewal {rid} fresh U bootstrap re-assertion (weekly integration step1, synthetic fixture, no genuine approval)"
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
    p = qroot / f"{cid.lower()}.json"
    p.write_bytes(core.json_bytes(payloads[cid]))
    rows.append({"check_id": cid, "kind": "DETERMINISTIC", "status": "PASS", "executor": executor,
                 "evidence": "Weekly step1 fresh re-assertion: exact current bytes inspected, synthetic fixture.",
                 "recorded_at": now_iso,
                 "result": {"path": str(p.relative_to(root_p)), "sha256": core.sha256_file(p)}})
checks_path = root_p / pdir / f"renewal-qa-checks-{rid}.json"
checks_path.write_bytes(core.json_bytes({"checks": rows}))
print(str(checks_path.relative_to(root_p)))
"""
q1 = run([PY,"-c",U_QA, str(FIX), basis_rel, RDIR, PDIR, now_iso, "weekly-integration-step1 U bootstrap"], REPO, "s1-qa-u1")
if q1.returncode!=0:
    print("FATAL qa failed", flush=True); sys.exit(1)
checks_rel=(EVID/"s1-qa-u1-stdout.txt").read_text().strip().splitlines()[-1].strip()
print(f"checks_rel {checks_rel}", flush=True)
# 1c finalize U (no new reviews, predecessor reuse)
f1 = run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "finalize","--root",str(FIX),"--state",STATE,"--basis",basis_rel,"--checks",checks_rel,"--executor","weekly-integration-step1","--recorded-at",now_iso],
 REPO, "s1-finalize-u1")
if f1.returncode!=0:
    print("FATAL finalize failed", flush=True); sys.exit(1)
fin=json.loads((EVID/"s1-finalize-u1-stdout.txt").read_text())
set_path=fin["set_path"]
print(f"set_path {set_path} disposition {fin.get('disposition')}", flush=True)
# 1d validate-set + validate-receipt (CURRENT)
vset = run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "validate-set","--root",str(FIX),"--state",STATE,"--set",set_path], REPO, "s1-validate-set")
print(f"validate-set exit {vset.returncode}", flush=True)
receipt_rel=fin.get("receipt_path") or fin.get("receipt_rel") or f"{RDIR}/validated-source-manifest.json"
# receipt path from finalize stdout? finalize prints receipt_path
try:
    receipt_rel=fin.get("receipt_path", receipt_rel)
except: pass
vrc = run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "validate-receipt","--root",str(FIX),"--receipt",receipt_rel], REPO, "s1-validate-receipt")
print(f"validate-receipt exit {vrc.returncode}", flush=True)
# 1e activate U1
reason="Core change: versioned renewal HIGH+consumer implementation (FIXED 736 G1 bootstrap U1, Weekly integration)"
a1 = run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "activate","--root",str(FIX),"--state",STATE,"--set",set_path,"--reason",reason,"--executor","weekly-integration-step1","--recorded-at",now_iso],
 REPO, "s1-activate-u1")
if a1.returncode!=0:
    print("FATAL activate failed", flush=True); sys.exit(1)
act=json.loads((EVID/"s1-activate-u1-stdout.txt").read_text())
record_path=act["record_path"]
print(f"ACTIVATED {record_path} observed {act.get('observed')}", flush=True)
# 1f history + CURRENT readback (detached proof)
h1 = run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "history","--root",str(FIX),"--record",record_path], REPO, "s1-history-u1")
print(f"history exit {h1.returncode}", flush=True)
# strict LIVE State via agent.validate_agent_state (fresh process)
live_code = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
root=Path(sys.argv[1]); state_rel=sys.argv[2]
from scripts import survey_production_v2 as core
from scripts import survey_agent_control_v2 as agent
assert str(Path(agent.__file__).resolve()).startswith(str(root.resolve())), "fixture origin"
cfg=core.load_json(root / "config/survey-production-v2.json")
state=core.load_json(root / state_rel)
errs=agent.validate_agent_state(root, cfg, state)
print(json.dumps({"live_errors": errs, "live_ok": len(errs)==0}))
sys.exit(0 if len(errs)==0 else 2)
"""
lv = run([PY,"-c",live_code, str(FIX), STATE], REPO, "s1-live-state")
print(f"live-state exit {lv.returncode}", flush=True)
# old receipt stale note: show old editorial receipt tool epoch vs current HEAD
oldnote_code = r"""
import sys, json, hashlib
sys.path.insert(0, sys.argv[1])
from pathlib import Path
root=Path(sys.argv[1])
old_manifest=json.loads((root / "sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/publication/validated-source-manifest.json").read_bytes())
print(json.dumps({"old_manifest_keys": sorted(old_manifest.keys())[:10], "old_path": "sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/publication/validated-source-manifest.json"}, indent=1))
"""
on = run([PY,"-c",oldnote_code, str(FIX)], REPO, "s1-old-receipt-note")
# artifact-only descendant control: create docs-only commit, verify history still passes (readback only)
# do via git in fixture (artifact-only, no tool closure)
art = run(["git","--no-optional-locks","rev-parse","HEAD"], str(FIX), "s1-art-pre-head")
# create artifact file outside tool closure (docs/artifact-note)
# use bash to create file then git add/commit
import subprocess as _sp
artifact_rel = "docs/weekly-integration-artifact-note-STEP1.md"
(FIX/artifact_rel).write_text("# Weekly integration STEP1 artifact-only note\nSynthetic fixture, no Core change, readback only.\n", encoding="utf-8")
ar_add = run(["git","--no-optional-locks","add","--",artifact_rel], str(FIX), "s1-art-add")
ar_commit = run(["git","--no-optional-locks","commit","-m","TEST-ONLY artifact-only note (no Core change, readback only)","--no-verify"], str(FIX), "s1-art-commit")
ar_head = run(["git","--no-optional-locks","rev-parse","HEAD"], str(FIX), "s1-art-head")
ar_anc = run(["git","--no-optional-locks","merge-base","--is-ancestor","85eac6f4e2c042c45603552a729770683982c7be","HEAD"], str(FIX), "s1-art-ancestor")
print(f"artifact-only HEAD {open(EVID/'s1-art-head-stdout.txt').read().strip()}", flush=True)
# readback after artifact commit should still pass (history on same record)
h_art = run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "history","--root",str(FIX),"--record",record_path], REPO, "s1-history-after-artifact")
print(f"history-after-artifact exit {h_art.returncode} (PASS expected, readback only)", flush=True)
# ALREADY_ACTIVE: second activate same set (canonical path)
a2 = run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "activate","--root",str(FIX),"--state",STATE,"--set",set_path,"--reason",reason,"--executor","weekly-integration-step1","--recorded-at",datetime.now(timezone.utc).isoformat()],
 REPO, "s1-activate-already")
print(f"ALREADY_ACTIVE exit {a2.returncode}", flush=True)
try:
    print(open(EVID/"s1-activate-already-stdout.txt").read()[:2000], flush=True)
except: pass
# alias refusal: same set via ./ prefix (different lexical spelling, same bytes)
alias_set = "./"+set_path
a_alias = run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "activate","--root",str(FIX),"--state",STATE,"--set",alias_set,"--reason",reason,"--executor","weekly-integration-step1","--recorded-at",datetime.now(timezone.utc).isoformat()],
 REPO, "s1-activate-alias-refuse")
print(f"alias-activate exit {a_alias.returncode} (REFUSE expected, NOT ALREADY_ACTIVE)", flush=True)
# no-write alias for state: state via ./ prefix
alias_state = "./"+STATE
a_state_alias = run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "history","--root",str(FIX),"--record",record_path], REPO, "s1-history-canonical")
# state alias via prepare with alias state (should refuse before writes)
prep_alias = run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "prepare","--root",str(FIX),"--state",alias_state,"--renewal-id","high-alias-probe","--intent","REUSE_TARGETS","--manuscript-spec",MSPEC,"--executor","weekly-integration-step1"],
 REPO, "s1-prepare-state-alias-refuse")
print(f"state-alias-prepare exit {prep_alias.returncode} (REFUSE expected)", flush=True)
# reason control: empty reason should refuse (ARGS)
reason_empty = run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; import sys as _s; _s.exit(main(_s.argv[2:]))", str(FIX),
 "activate","--root",str(FIX),"--state",STATE,"--set",set_path,"--reason","","--executor","weekly-integration-step1"],
 REPO, "s1-activate-empty-reason-refuse")
print(f"empty-reason exit {reason_empty.returncode} (REFUSE expected)", flush=True)
# wrong-target control: finalize with stale QA (bootstrap deterministic-checks) should refuse QA_MISSING
wrong_qa = run([PY,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts import survey_versioned_renewal_v2 as high; high.finalize_renewal(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], None, None, 'x', sys.argv[5])", str(FIX), STATE, basis_rel, f"{PDIR}/deterministic-checks.json", now_iso], REPO, "s1-finalize-wrong-qa-refuse")
print(f"wrong-qa exit {wrong_qa.returncode} (REFUSE expected)", flush=True)
# style control at G1 (no style change, so reuse should PASS; we already passed. To show style oracle, try to document current vs retained style equality)
style_code = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
root=Path(sys.argv[1]); basis_rel=sys.argv[2]
basis=json.loads((root/basis_rel).read_bytes())
print(json.dumps({"basis_issue": basis.get("issue_id"), "renewal_id": basis.get("renewal_id"), "requested": basis.get("requested")}, indent=1))
"""
st = run([PY,"-c",style_code, str(FIX), basis_rel], REPO, "s1-style-note")
print("STEP1 DONE", flush=True)
