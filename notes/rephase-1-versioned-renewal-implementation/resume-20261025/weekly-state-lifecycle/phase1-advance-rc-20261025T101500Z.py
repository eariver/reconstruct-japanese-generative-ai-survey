#!/usr/bin/env python3
"""Phase1: VALIDATED_DRAFT->RELEASE_CANDIDATE via public validators.
- before/after State hash/lifecycle/checkpoint/gate/pointer/history/tool HEAD persisted
- artifacts resolved role-aware from State-selected U4 Candidate
- stage.validate_stage + agent.build_stage_checkpoint + agent.advance_with_checkpoint ONLY
No handmade State fields, no monkeypatch, no direct overwrite.
"""
import os, sys, json, hashlib, subprocess
from pathlib import Path
from datetime import datetime, timezone

REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-weekly-state-lifecycle-20261025T101500Z/renewal-weekly"
EVID_BASE = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-state-lifecycle"
EVID = EVID_BASE / "phase1-20261025T101500Z"
EVID.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(FIX.resolve()))
for k in ["GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"]:
    assert k not in os.environ, f"GIT var leaked {k}"
assert not (FIX/".git/objects/info/alternates").exists()

from scripts import survey_production_v2 as core
from scripts import survey_agent_control_v2 as agent
from scripts import survey_stage_validation_v2 as stage
from scripts import survey_publication_set_v2 as setmod

assert str(Path(core.__file__).resolve()).startswith(str(FIX.resolve()))

ISSUE="2026-W37"
state_path = FIX / f"sources/{ISSUE}/production-state.json"
cfg = json.loads((FIX/"config/survey-production-v2.json").read_bytes())

def sha(p: Path):
    return hashlib.sha256(p.read_bytes()).hexdigest()

before_bytes = state_path.read_bytes()
before_state = json.loads(before_bytes)
before = {
    "state_sha256": sha(state_path),
    "lifecycle": before_state["lifecycle_state"],
    "next_action": before_state["next_action"],
    "terminal_reason": before_state["terminal_reason"],
    "pointer": before_state["publication_revalidation_provenance"],
    "machine_preview": before_state["machine_checkpoints"].get("publication_preview"),
    "machine_freeze": before_state["machine_checkpoints"].get("freeze"),
    "human_preview": before_state["human_gates"].get("publication_preview"),
    "history_len": len(before_state["history"]),
    "history_last": before_state["history"][-1],
    "tool_head": subprocess.run(["git","-C",str(FIX),"rev-parse","HEAD"],capture_output=True,text=True).stdout.strip(),
}
print("BEFORE "+json.dumps(before, indent=1), flush=True)
assert before["lifecycle"] == "VALIDATED_DRAFT", f"expected VALIDATED_DRAFT got {before['lifecycle']}"

# resolve active candidate role-aware
sel = setmod.resolve_publication_selection(FIX, cfg, before_state)
assert sel["mode"] == "VERSIONED_ACTIVE", sel["mode"]
active_cand_rel = sel["candidate_ref"]["path"]
active_cand_path = FIX / active_cand_rel
assert active_cand_path.is_file(), f"active candidate missing {active_cand_rel}"
assert sha(active_cand_path) == sel["candidate_ref"]["sha256"], "active candidate drift"
print(f"ACTIVE_CANDIDATE {active_cand_rel} {sha(active_cand_path)[:12]}", flush=True)

# synthetic clock monotonic >= selected record (r6 08:41:00.502366Z) + actual UTC separate
syn_report = core.parse_instant("2026-10-25T09:10:00Z")
syn_checkpoint = core.parse_instant("2026-10-25T09:10:01Z")
actual_raw = datetime.now(timezone.utc).isoformat()
print(f"SYN_REPORT {core.iso_utc(syn_report)} SYN_CHECKPOINT {core.iso_utc(syn_checkpoint)} ACTUAL_RAW {actual_raw}", flush=True)

# stage report output fresh canonical: orchestration/v2/reviews/VALIDATED_DRAFT-core-contract.json (must not exist)
source_root = FIX / before_state["profile"]["path"]
# profile path is sources/.../production-profile.json -> source_root from _profile_and_source
_, profile, src_root = agent._profile_and_source(FIX, cfg, before_state)
assert src_root.resolve() == (FIX / "sources/2026-W37").resolve(), f"source_root {src_root}"
report_path = src_root / "orchestration/v2/reviews/VALIDATED_DRAFT-core-contract.json"
assert not report_path.exists(), f"canonical collision: report exists {report_path}"
reviews_path = src_root / "orchestration/v2/reviews/VALIDATED_DRAFT-reviews.json"
assert not reviews_path.exists(), f"canonical collision: reviews exists {reviews_path}"

supplied = {"publication-candidate": active_cand_path}
# public validator
stage.validate_stage(FIX, cfg, state_path, supplied, report_path, syn_report)
print(f"VALIDATE_STAGE PASS report={report_path.relative_to(FIX)} sha={sha(report_path)[:12]}", flush=True)
report = json.loads(report_path.read_bytes())
assert report["from_state"] == "VALIDATED_DRAFT" and report["to_state"] == "RELEASE_CANDIDATE"

# reviews file for checkpoint (deterministic)
core.write_json(reviews_path, {"reviews": [{
    "check_id": "CORE_STAGE_CONTRACT",
    "kind": "DETERMINISTIC",
    "executor": "weekly-state-lifecycle-phase1 synthetic; exact U4 active Candidate authority",
    "evidence": "Public stage.validate_stage PASS for exact State-selected U4 Candidate/QA/Gate; no genuine Human approval",
    "result_path": str(report_path.relative_to(FIX)),
}]})
print(f"REVIEWS_WRITTEN {reviews_path.relative_to(FIX)}", flush=True)

# build checkpoint via public API
checkpoint_path = agent.build_stage_checkpoint(FIX, cfg, state_path, supplied, reviews_path, "Weekly U4 VALIDATED_DRAFT->RELEASE_CANDIDATE via exact State-selected Candidate; synthetic; no genuine approval", syn_checkpoint, None)
print(f"CHECKPOINT {checkpoint_path.relative_to(FIX)} sha={sha(checkpoint_path)[:12]}", flush=True)
# canonical path check
expected_canonical = agent.canonical_checkpoint_path(FIX, cfg, before_state)
assert checkpoint_path.resolve() == expected_canonical.resolve(), f"checkpoint not canonical {checkpoint_path} vs {expected_canonical}"
assert expected_canonical.relative_to(FIX) == Path("sources/2026-W37/orchestration/v2/checkpoints/VALIDATED_DRAFT.json"), f"unexpected canonical {expected_canonical}"

# advance via public API
updated = agent.advance_with_checkpoint(FIX, cfg, state_path, checkpoint_path)
print(f"ADVANCED lifecycle={updated['lifecycle_state']} next={updated['next_action']} terminal={updated['terminal_reason']}", flush=True)

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
    "active_candidate": {"path": active_cand_rel, "sha256": sha(active_cand_path)},
    "syn_report": core.iso_utc(syn_report),
    "syn_checkpoint": core.iso_utc(syn_checkpoint),
    "actual_utc_raw": actual_raw,
}
print("AFTER "+json.dumps(after, indent=1), flush=True)

# strict post checks via public API
errors = agent.validate_agent_state(FIX, cfg, updated)
assert errors == [], f"post validate errors {errors}"
assert updated["lifecycle_state"] == "RELEASE_CANDIDATE", updated["lifecycle_state"]
assert updated["terminal_reason"] == "HUMAN_GATE_REACHED", f"expected HUMAN_GATE_REACHED got {updated['terminal_reason']}"
# history monotonic
assert updated["history"][-1]["from"] == "VALIDATED_DRAFT" and updated["history"][-1]["to"] == "RELEASE_CANDIDATE"
assert updated["history"][-1]["recorded_at"] == core.iso_utc(syn_checkpoint)
# checkpoint provenance must equal checkpoint authority
assert updated["checkpoint_provenance"]["VALIDATED_DRAFT"] == {"path": str(checkpoint_path.relative_to(FIX)), "sha256": sha(checkpoint_path)}

# persist evidence
(EVID/"before.json").write_text(json.dumps(before, indent=1), encoding="utf-8")
(EVID/"after.json").write_text(json.dumps(after, indent=1), encoding="utf-8")
(EVID/"transition.json").write_text(json.dumps({"before": before, "after": after}, indent=1), encoding="utf-8")
print("PHASE1 PASS", flush=True)
