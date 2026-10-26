#!/usr/bin/env python3
"""Phase0: verify initial VALIDATED_DRAFT via public validators + exact readback.
No State mutation. Fresh Python, correct import root, sanitized env.
"""
import os, sys, json, hashlib, subprocess
from pathlib import Path
from datetime import datetime, timezone

REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-weekly-state-lifecycle-20261025T101500Z/renewal-weekly"
STAMP = "20261025T101500Z"
EVID_BASE = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-state-lifecycle"
EVID = EVID_BASE / f"phase0-{STAMP}"
EVID.mkdir(parents=True, exist_ok=True)

# Ensure import root is FIX, not REPO
assert str(FIX.resolve()) != str(REPO.resolve())
sys.path.insert(0, str(FIX.resolve()))
# sanitized check
for k in ["GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"]:
    assert k not in os.environ or os.environ[k]=="", f"GIT var leaked {k}"
# no alternates
assert not (FIX/".git/objects/info/alternates").exists(), "alternates present"

from scripts import survey_production_v2 as core
from scripts import survey_agent_control_v2 as agent
from scripts import survey_publication_set_v2 as setmod

# origin check
assert str(Path(core.__file__).resolve()).startswith(str(FIX.resolve())), f"wrong core origin {core.__file__}"
assert str(Path(agent.__file__).resolve()).startswith(str(FIX.resolve())), f"wrong agent origin {agent.__file__}"

ISSUE="2026-W37"
state_path = FIX / f"sources/{ISSUE}/production-state.json"
cfg = json.loads((FIX/"config/survey-production-v2.json").read_bytes())
state = json.loads(state_path.read_bytes())
state_sha_before = hashlib.sha256(state_path.read_bytes()).hexdigest()

out = {}
out["fix_head"] = subprocess.run(["git","-C",str(FIX),"rev-parse","HEAD"],capture_output=True,text=True).stdout.strip()
out["state_sha256"] = state_sha_before
out["lifecycle_state"] = state.get("lifecycle_state")
out["next_action"] = state.get("next_action")
out["terminal_reason"] = state.get("terminal_reason")
out["human_preview"] = state.get("human_gates",{}).get("publication_preview")
out["machine_preview"] = state.get("machine_checkpoints",{}).get("publication_preview")
out["pointer"] = state.get("publication_revalidation_provenance")
out["history_len"] = len(state.get("history",[]))
out["history_last"] = state.get("history",[])[-1] if state.get("history") else None
# strict LIVE validation via public API
errors = agent.validate_agent_state(FIX, cfg, state)
out["validate_agent_state_errors"] = errors
out["validate_agent_state_pass"] = (errors == [])
# selection
sel = setmod.resolve_publication_selection(FIX, cfg, state)
out["selection_mode"] = sel.get("mode")
out["selection_candidate_ref"] = sel.get("candidate_ref")
out["selection_set_ref"] = sel.get("set_ref")
out["selection_canonical_anchor"] = sel.get("canonical_anchor")
# seal + proof pins
seal_path = FIX / sel["set_ref"]["path"] if sel.get("set_ref") else None
if seal_path:
    seal = json.loads(seal_path.read_bytes())
    out["seal_status"] = seal.get("status")
    out["seal_roles_candidate_sha"] = seal["roles"]["publication-candidate"]["sha256"]
    out["seal_proof_ref"] = seal.get("renewal_proof_ref")
    out["seal_receipt_ref"] = seal.get("source_receipt_ref")
    # verify proof file exists + hash
    proof_p = FIX / seal["renewal_proof_ref"]["path"]
    out["proof_sha_match"] = (hashlib.sha256(proof_p.read_bytes()).hexdigest() == seal["renewal_proof_ref"]["sha256"])
# readback: resolve active candidate + validate via public validators
from scripts import survey_publication_v2 as pubmod
cand_ref = sel.get("candidate_ref")
cand_path = FIX / cand_ref["path"]
out["candidate_path"] = cand_ref["path"]
out["candidate_sha_match"] = (hashlib.sha256(cand_path.read_bytes()).hexdigest() == cand_ref["sha256"])
cand = pubmod.validate_candidate(FIX, cand_path, issue_id=ISSUE)
out["candidate_status"] = cand.get("status")
out["candidate_pdf_sha"] = cand["pdf"]["sha256"]
out["candidate_proof_ref"] = cand.get("renewal_source_proof_ref")
# check proof equality with seal proof (State-selected)
out["candidate_proof_matches_seal"] = (cand.get("renewal_source_proof_ref") == seal.get("renewal_proof_ref"))
# QA/Gate bindings via seal roles
out["seal_roles"] = {k: v["sha256"][:12] for k,v in seal["roles"].items()} if seal_path else None
# stage_plan for VALIDATED_DRAFT
out["stage_plan_VALIDATED_DRAFT"] = cfg["orchestration"]["stage_plan"]["VALIDATED_DRAFT"]
out["stage_plan_RELEASE_CANDIDATE"] = cfg["orchestration"]["stage_plan"]["RELEASE_CANDIDATE"]
out["stage_plan_FROZEN"] = cfg["orchestration"]["stage_plan"]["FROZEN"]
# actual UTC raw separate
out["actual_utc_raw"] = datetime.now(timezone.utc).isoformat()
# code guards
import hashlib as hl
for rel in ["templates/survey/jgaisurvey.sty","scripts/survey_versioned_renewal_history_v2.py","scripts/survey_editorial_correction_proposal_v2.py","scripts/survey_publication_v2.py"]:
    out[f"code_{rel}"] = hl.sha256((FIX/rel).read_bytes()).hexdigest()[:16]

(EVID/"phase0-result.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print(json.dumps(out, indent=1))
if not out["validate_agent_state_pass"]:
    print("FAIL: validate_agent_state errors", errors, file=sys.stderr)
    sys.exit(1)
if out["lifecycle_state"] != "VALIDATED_DRAFT":
    print(f"FAIL: expected VALIDATED_DRAFT got {out['lifecycle_state']}", file=sys.stderr)
    sys.exit(1)
if out["selection_mode"] != "VERSIONED_ACTIVE":
    print(f"FAIL: expected VERSIONED_ACTIVE got {out['selection_mode']}", file=sys.stderr)
    sys.exit(1)
if not out["candidate_proof_matches_seal"]:
    print("FAIL: candidate proof != seal proof", file=sys.stderr)
    sys.exit(1)
print("PHASE0 PASS", flush=True)
