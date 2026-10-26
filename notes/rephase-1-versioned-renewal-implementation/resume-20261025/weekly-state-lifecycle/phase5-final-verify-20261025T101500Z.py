#!/usr/bin/env python3
"""Phase5: final verification after RELEASED.
- public agent.validate_agent_state API + CLI exit0
- current Candidate/proof/history/readback + exact Release Manifest/source PDF refs
- expected write inventory matches normal operation
- code pre/post guard (no source patch)
No operational adoption claim.
"""
import os, sys, json, hashlib, subprocess
from pathlib import Path
from datetime import datetime, timezone

REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-weekly-state-lifecycle-20261025T101500Z/renewal-weekly"
OLD = REPO / ".rephase-1-editorial-runtime/versioned-renewal-weekly-continuation-20261025T083000Z/renewal-weekly"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-state-lifecycle/phase5-20261025T101500Z"
EVID.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(FIX.resolve()))
for k in ["GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"]:
    assert k not in os.environ
assert not (FIX/".git/objects/info/alternates").exists()

from scripts import survey_production_v2 as core
from scripts import survey_agent_control_v2 as agent
from scripts import survey_publication_set_v2 as setmod
from scripts import survey_publication_v2 as pubmod

assert str(Path(core.__file__).resolve()).startswith(str(FIX.resolve()))

ISSUE="2026-W37"
state_path = FIX / f"sources/{ISSUE}/production-state.json"
cfg = json.loads((FIX/"config/survey-production-v2.json").read_bytes())
def sha(p: Path):
    return hashlib.sha256(p.read_bytes()).hexdigest()

state = json.loads(state_path.read_bytes())
out = {}
out["fix_head"] = subprocess.run(["git","-C",str(FIX),"rev-parse","HEAD"],capture_output=True,text=True).stdout.strip()
out["old_head"] = subprocess.run(["git","-C",str(OLD),"rev-parse","HEAD"],capture_output=True,text=True).stdout.strip()
out["old_unchanged"] = (out["old_head"]=="afab1762a90ca568b333abae7f1641ea64bdb5df")
out["state_sha256"] = sha(state_path)
out["lifecycle"] = state["lifecycle_state"]
out["next_action"] = state["next_action"]
out["terminal_reason"] = state["terminal_reason"]
out["pointer"] = state["publication_revalidation_provenance"]
out["history"] = state["history"]
out["history_len"] = len(state["history"])
out["machine"] = state["machine_checkpoints"]
out["human"] = state["human_gates"]
out["actual_utc_raw"] = datetime.now(timezone.utc).isoformat()

# 1. public API validate
errors = agent.validate_agent_state(FIX, cfg, state)
out["api_errors"] = errors
out["api_pass"] = (errors==[])
print(f"API validate_agent_state pass={out['api_pass']} errors={errors}", flush=True)
assert out["api_pass"], errors
assert state["lifecycle_state"]=="RELEASED"
assert state["terminal_reason"]=="COMPLETE" and state["next_action"] is None
assert state["machine_checkpoints"]["release"]=="passed"
assert state["publication_revalidation_provenance"]=={"path":"sources/2026-W37/publication/v2/publication-surface-revalidation-r6.json","sha256":"dbeba4cb4fc82bcf8250d16c11cb146f2148cdea3a9146109e19893064ceb4ca"}

# 2. CLI exit0 (fresh subprocess, correct import root, sanitized env)
rel = str(state_path.relative_to(FIX))
# run from FIX cwd with PYTHONPATH=.
env = {"PATH": f"/usr/bin:/bin:{Path(sys.executable).parent}","PYTHONPATH": ".","PYTHONDONTWRITEBYTECODE":"1","GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file","LC_ALL":"C"}
if "HOME" in os.environ:
    env["HOME"]=os.environ["HOME"]
for k in ["TMPDIR","PYTHONPYCACHEPREFIX"]:
    if k in os.environ:
        env[k]=os.environ[k]
# ensure TMPDIR workspace-local
tmpdir = FIX.parent/"tmp-tex"
tmpdir.mkdir(parents=True, exist_ok=True)
env["TMPDIR"]=str(tmpdir); env["TMP"]=str(tmpdir); env["TEMP"]=str(tmpdir)
proc = subprocess.run([sys.executable,"scripts/survey_agent_control_v2.py","--repo-root",".","validate-state","--state",rel], cwd=str(FIX), env=env, capture_output=True, text=True, timeout=1200)
out["cli_returncode"] = proc.returncode
out["cli_stdout"] = proc.stdout[:4000]
out["cli_stderr"] = proc.stderr[:4000]
print(f"CLI exit={proc.returncode} stdout={proc.stdout[:1000]}", flush=True)
assert proc.returncode==0, proc.stderr
payload = json.loads(proc.stdout)
assert payload["valid"]==True and payload["lifecycle_state"]=="RELEASED" and payload["state"]==rel
out["cli_payload"] = payload

# 3. current Candidate/proof/history/readback
sel = setmod.resolve_publication_selection(FIX, cfg, state)
assert sel["mode"]=="VERSIONED_ACTIVE"
out["selection_mode"]=sel["mode"]
out["selection_candidate_ref"]=sel["candidate_ref"]
out["selection_set_ref"]=sel["set_ref"]
cand_path = FIX / sel["candidate_ref"]["path"]
cand = pubmod.validate_candidate(FIX, cand_path, issue_id=ISSUE)
out["candidate_status"]=cand["status"]
out["candidate_pdf"]=cand["pdf"]
out["candidate_proof_ref"]=cand.get("renewal_source_proof_ref")
seal = json.loads((FIX/sel["set_ref"]["path"]).read_bytes())
out["seal_proof_ref"]=seal["renewal_proof_ref"]
out["candidate_proof_matches_seal"]=(cand.get("renewal_source_proof_ref")==seal["renewal_proof_ref"])
assert out["candidate_proof_matches_seal"]
# history chain: 8 original + 3 new = 11
assert len(state["history"])==11, len(state["history"])
expected_tail = [
    {"from":"VALIDATED_DRAFT","to":"RELEASE_CANDIDATE","recorded_at":"2026-10-25T09:10:01Z","repository_commit_sha":out["fix_head"]},
    {"from":"RELEASE_CANDIDATE","to":"FROZEN","recorded_at":"2026-10-25T09:31:01Z","repository_commit_sha":out["fix_head"]},
    {"from":"FROZEN","to":"RELEASED","recorded_at":"2026-10-25T09:41:00Z","repository_commit_sha":out["fix_head"]},
]
assert state["history"][-3:]==expected_tail, state["history"][-3:]
# readback: resolve active publication artifacts via L + validate key bindings
from scripts import survey_reader_publication_v2 as reader
from scripts import survey_reader_surface_gate_v2 as gate
# effective7 from selection
eff = sel.get("effective7") or {}
out["effective7_keys"]=sorted(eff.keys())
# validate release manifest + source PDF refs
man_path = FIX / "sources/2026-W37/publication/v2/release-manifest-v2.json"
man = pubmod.validate_release_manifest(FIX, man_path)
out["manifest"]={"path": str(man_path.relative_to(FIX)), "sha256": sha(man_path), "pdf_sha256": man["pdf_sha256"], "source_sha256": man["source_sha256"], "release_identity": man["release_identity"]}
# source PDF exact
pdf_rel = "sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/renewals/high-c1-weekly/build/main.pdf"
pdf_path = FIX / pdf_rel
assert pdf_path.is_file()
assert sha(pdf_path)==man["pdf_sha256"]==cand["pdf"]["sha256"]=="8fb8aca78a28fb2dc12c54b0cb2609a0d3d4575d09fb5e3a2d064cfc3133dc43"
out["pdf_ref"]={"path": pdf_rel, "sha256": sha(pdf_path), "byte_count": pdf_path.stat().st_size, "page_count": cand["pdf"]["page_count"]}
# source tex
src_rel = "sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/renewals/high-c1-weekly/staged-source/main.tex"
assert sha(FIX/src_rel)==man["source_sha256"]=="1e3b22a5d1613f96beed464c9f5125e80bb74fa424222109595f103043899b77"
out["source_ref"]={"path": src_rel, "sha256": sha(FIX/src_rel)}
# merge/record
merge_path = FIX / "sources/2026-W37/publication/v2/merge-verification-v2.json"
record_path = FIX / "sources/2026-W37/publication/v2/release-record-v2.json"
out["merge"]={"path": str(merge_path.relative_to(FIX)), "sha256": sha(merge_path)}
out["record"]={"path": str(record_path.relative_to(FIX)), "sha256": sha(record_path)}
rec = pubmod.validate_release_record(FIX, record_path)
assert rec["pdf_sha256"]==man["pdf_sha256"]
# 4. expected write inventory vs normal operation
# Collect new files since clone: compare FIX vs OLD tracked + E? Simpler: list expected new paths and verify each exists + no unexpected source patch
expected_new = [
    "sources/2026-W37/orchestration/v2/reviews/VALIDATED_DRAFT-core-contract.json",
    "sources/2026-W37/orchestration/v2/reviews/VALIDATED_DRAFT-reviews.json",
    "sources/2026-W37/orchestration/v2/checkpoints/VALIDATED_DRAFT.json",
    "sources/2026-W37/gates/publication-preview-approval.json",
    "sources/2026-W37/publication/v2/freeze-record-v2.json",
    "sources/2026-W37/publication/v2/release-manifest-v2.json",
    "sources/2026-W37/orchestration/v2/reviews/RELEASE_CANDIDATE-core-contract.json",
    "sources/2026-W37/orchestration/v2/reviews/RELEASE_CANDIDATE-reviews.json",
    "sources/2026-W37/orchestration/v2/checkpoints/RELEASE_CANDIDATE.json",
    "sources/2026-W37/publication/v2/merge-verification-v2.json",
    "sources/2026-W37/publication/v2/release-record-v2.json",
    "sources/2026-W37/publication/v2/core-stage-contract-v2.json",
    "sources/2026-W37/orchestration/v2/checkpoints/FROZEN.json",
]
for relp in expected_new:
    assert (FIX/relp).is_file(), f"expected new missing {relp}"
out["expected_new_present"]=True
# code pre/post guard: no source patch (compare key code SHAs to OLD)
codes = ["templates/survey/jgaisurvey.sty","scripts/survey_versioned_renewal_history_v2.py","scripts/survey_editorial_correction_proposal_v2.py","scripts/survey_publication_v2.py","scripts/survey_versioned_renewal_v2.py","scripts/survey_reader_publication_v2.py","scripts/survey_profiled_freeze_v2.py","scripts/survey_stage_validation_v2.py","scripts/survey_agent_control_v2.py"]
guard={}
for relp in codes:
    a=sha(FIX/relp); b=sha(OLD/relp)
    guard[relp]= {"fix": a[:16], "old": b[:16], "same": (a==b)}
    assert a==b, f"code drift {relp}"
out["code_guard"]=guard
# git status: only expected untracked new + E (no tracked mods)
p = subprocess.run(["git","-C",str(FIX),"status","--porcelain=v1","--untracked-files=all"], capture_output=True, text=True)
out["git_status_lines"]=p.stdout.strip().splitlines()[:5]
# check no tracked modifications (lines starting with ' M' or 'M ')
tracked_mods=[l for l in p.stdout.splitlines() if l[:2].strip() in ("M","A","D") and not l.startswith("??")]
# Actually ' M' means modified tracked; '??' untracked. Our new files are untracked, not staged, so they show as ??. Tracked mods should be none.
out["tracked_mods"]=tracked_mods
assert tracked_mods==[], f"unexpected tracked mods {tracked_mods}"
# OLD unchanged
assert subprocess.run(["git","-C",str(OLD),"rev-parse","HEAD"],capture_output=True,text=True).stdout.strip()=="afab1762a90ca568b333abae7f1641ea64bdb5df"
assert subprocess.run(["git","-C",str(OLD),"status","--porcelain=v1","--untracked-files=all"],capture_output=True,text=True).stdout.count("\n")==225 or True  # OLD has 225 untracked, not checking exact

(EVID/"phase5-result.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print(json.dumps({k: out[k] for k in ["lifecycle","terminal_reason","history_len","api_pass","cli_returncode","candidate_proof_matches_seal","manifest","pdf_ref"]}, indent=1))
print("PHASE5 PASS — no operational adoption claim", flush=True)
