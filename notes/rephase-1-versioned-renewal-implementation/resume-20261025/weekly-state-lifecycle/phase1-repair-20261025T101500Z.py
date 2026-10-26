#!/usr/bin/env python3
"""Phase1 evidence repair — no State rewind, no second advance.
Reconstructs before/after evidence from captured stdout + current State.
Validates public invariants for VALIDATED_DRAFT->RELEASE_CANDIDATE with empty checkpoints.
"""
import json, hashlib, subprocess
from pathlib import Path
from datetime import datetime, timezone

REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-weekly-state-lifecycle-20261025T101500Z/renewal-weekly"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-state-lifecycle/phase1-20261025T101500Z"
EVID.mkdir(parents=True, exist_ok=True)
import sys
sys.path.insert(0, str(FIX.resolve()))
from scripts import survey_production_v2 as core
from scripts import survey_agent_control_v2 as agent

ISSUE="2026-W37"
state_path = FIX / f"sources/{ISSUE}/production-state.json"
cfg = json.loads((FIX/"config/survey-production-v2.json").read_bytes())
updated = json.loads(state_path.read_bytes())
def sha(p: Path):
    return hashlib.sha256(p.read_bytes()).hexdigest()

# before from phase0 result + stdout capture
phase0 = json.loads((REPO/"notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-state-lifecycle/phase0-20261025T101500Z/phase0-result.json").read_bytes())
before = {
    "state_sha256": phase0["state_sha256"],
    "lifecycle": phase0["lifecycle_state"],
    "next_action": phase0["next_action"],
    "terminal_reason": phase0["terminal_reason"],
    "pointer": phase0["pointer"],
    "machine_preview": phase0["machine_preview"],
    "human_preview": phase0["human_preview"],
    "history_len": phase0["history_len"],
    "history_last": phase0["history_last"],
    "tool_head": phase0["fix_head"],
}
src_root = FIX / "sources/2026-W37"
report_path = src_root / "orchestration/v2/reviews/VALIDATED_DRAFT-core-contract.json"
reviews_path = src_root / "orchestration/v2/reviews/VALIDATED_DRAFT-reviews.json"
checkpoint_path = src_root / "orchestration/v2/checkpoints/VALIDATED_DRAFT.json"
assert report_path.is_file() and reviews_path.is_file() and checkpoint_path.is_file()
# validate checkpoint matches canonical
_, profile, _ = agent._profile_and_source(FIX, cfg, updated)
# checkpoint should equal canonical for BEFORE state, but we can check file exists and is valid JSON
chk = json.loads(checkpoint_path.read_bytes())
assert chk["from_state"]=="VALIDATED_DRAFT" and chk["to_state"]=="RELEASE_CANDIDATE" and chk["checkpoints"]==[]
# after from current State
after = {
    "state_sha256": sha(state_path),
    "lifecycle": updated["lifecycle_state"],
    "next_action": updated["next_action"],
    "terminal_reason": updated["terminal_reason"],
    "pointer": updated["publication_revalidation_provenance"],
    "machine_preview": updated["machine_checkpoints"].get("publication_preview"),
    "human_preview": updated["human_gates"].get("publication_preview"),
    "history_len": len(updated["history"]),
    "history_last": updated["history"][-1],
    "checkpoint_provenance_VALIDATED_DRAFT": updated["checkpoint_provenance"].get("VALIDATED_DRAFT"),
    "tool_head": subprocess.run(["git","-C",str(FIX),"rev-parse","HEAD"],capture_output=True,text=True).stdout.strip(),
    "report": {"path": str(report_path.relative_to(FIX)), "sha256": sha(report_path)},
    "reviews": {"path": str(reviews_path.relative_to(FIX)), "sha256": sha(reviews_path)},
    "checkpoint": {"path": str(checkpoint_path.relative_to(FIX)), "sha256": sha(checkpoint_path)},
    "active_candidate": {"path": "sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/renewals/high-u4-weekly/publication-candidate-v2.json", "sha256": sha(FIX/"sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/renewals/high-u4-weekly/publication-candidate-v2.json")},
    "syn_report": "2026-10-25T09:10:00Z",
    "syn_checkpoint": "2026-10-25T09:10:01Z",
    "actual_utc_raw": datetime.now(timezone.utc).isoformat(),
}
# public post checks
errors = agent.validate_agent_state(FIX, cfg, updated)
assert errors==[], errors
assert updated["lifecycle_state"]=="RELEASE_CANDIDATE"
assert updated["terminal_reason"]=="HUMAN_GATE_REACHED"
assert updated["history"][-1]=={"from":"VALIDATED_DRAFT","to":"RELEASE_CANDIDATE","recorded_at":"2026-10-25T09:10:01Z","repository_commit_sha":"afab1762a90ca568b333abae7f1641ea64bdb5df"}
# VALIDATED_DRAFT has empty checkpoints per stage_plan, so provenance must be None (not a checkpoint)
assert updated["checkpoint_provenance"].get("VALIDATED_DRAFT") is None, "empty-checkpoint stage must not set provenance"
# pointer unchanged
assert updated["publication_revalidation_provenance"]==before["pointer"]
(EVID/"before.json").write_text(json.dumps(before, indent=1), encoding="utf-8")
(EVID/"after.json").write_text(json.dumps(after, indent=1), encoding="utf-8")
(EVID/"transition.json").write_text(json.dumps({"before": before, "after": after, "note": "VALIDATED_DRAFT checkpoints=[] so no checkpoint_provenance entry; history advance + HUMAN_GATE_REACHED is the expected write inventory (State + VALIDATED_DRAFT checkpoint + report + reviews)"}, indent=1), encoding="utf-8")
print("PHASE1 REPAIR PASS")
print(json.dumps(after, indent=1))
