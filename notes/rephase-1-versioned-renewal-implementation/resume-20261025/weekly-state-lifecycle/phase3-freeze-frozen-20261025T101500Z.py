#!/usr/bin/env python3
"""Phase3: profiled Freeze + RELEASE_CANDIDATE->FROZEN via public validators.
- profiled.build_profiled_freeze (canonical outputs fresh, no delete/overwrite)
- stage.validate_stage + agent.build_stage_checkpoint + agent.advance_with_checkpoint
- artifacts: freeze-record, release-manifest, visual-review-record (exact Candidate Visual Review)
"""
import os, sys, json, hashlib, subprocess
from pathlib import Path
from datetime import datetime, timezone

REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-weekly-state-lifecycle-20261025T101500Z/renewal-weekly"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-state-lifecycle/phase3-20261025T101500Z"
EVID.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(FIX.resolve()))
for k in ["GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"]:
    assert k not in os.environ
assert not (FIX/".git/objects/info/alternates").exists()

from scripts import survey_production_v2 as core
from scripts import survey_agent_control_v2 as agent
from scripts import survey_stage_validation_v2 as stage
from scripts import survey_profiled_freeze_v2 as profiled
from scripts import survey_publication_set_v2 as setmod
from scripts import survey_publication_v2 as pubmod

assert str(Path(core.__file__).resolve()).startswith(str(FIX.resolve()))

ISSUE="2026-W37"
state_path = FIX / f"sources/{ISSUE}/production-state.json"
cfg = json.loads((FIX/"config/survey-production-v2.json").read_bytes())
def sha(p: Path):
    return hashlib.sha256(p.read_bytes()).hexdigest()

before_state = json.loads(state_path.read_bytes())
before = {
    "state_sha256": sha(state_path),
    "lifecycle": before_state["lifecycle_state"],
    "human_preview": before_state["human_gates"].get("publication_preview"),
    "machine_freeze": before_state["machine_checkpoints"].get("freeze"),
    "pointer": before_state["publication_revalidation_provenance"],
    "history_len": len(before_state["history"]),
    "history_last": before_state["history"][-1],
    "tool_head": subprocess.run(["git","-C",str(FIX),"rev-parse","HEAD"],capture_output=True,text=True).stdout.strip(),
}
print("BEFORE "+json.dumps(before, indent=1), flush=True)
assert before["lifecycle"]=="RELEASE_CANDIDATE"
assert before_state["human_gates"]["publication_preview"]=="approved"
assert before_state["machine_checkpoints"]["freeze"]=="pending"

sel = setmod.resolve_publication_selection(FIX, cfg, before_state)
assert sel["mode"]=="VERSIONED_ACTIVE"
cand_path = FIX / sel["candidate_ref"]["path"]
cand = pubmod.validate_candidate(FIX, cand_path, issue_id=ISSUE)
visual_rel = cand["visual_review"]["path"]
visual_path = FIX / visual_rel
assert visual_path.is_file(), f"visual missing {visual_rel}"
assert sha(visual_path)==cand["visual_review"]["sha256"]
print(f"CANDIDATE {sel['candidate_ref']['path']} VISUAL {visual_rel}", flush=True)

# canonical freeze outputs must be fresh (no collision with noncanonical low-level paths)
_, _, src_root = agent._profile_and_source(FIX, cfg, before_state)
freeze_path = src_root / "publication/v2/freeze-record-v2.json"
manifest_path = src_root / "publication/v2/release-manifest-v2.json"
assert not freeze_path.exists(), f"canonical collision freeze exists {freeze_path}"
assert not manifest_path.exists(), f"canonical collision manifest exists {manifest_path}"
# noncanonical low-level may exist at renewal pdir lifecycle-* — must not be used, must not be deleted
noncanon = FIX / f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-boot-1/lifecycle-high-u4-weekly-continuation/freeze-record.json"
print(f"NONCANON_EXISTS {noncanon.exists()} (must be preserved, not used/deleted)", flush=True)

syn_freeze = core.parse_instant("2026-10-25T09:30:00Z")
syn_report = core.parse_instant("2026-10-25T09:31:00Z")
syn_checkpoint = core.parse_instant("2026-10-25T09:31:01Z")
actual_raw = datetime.now(timezone.utc).isoformat()
print(f"SYN_FREEZE {core.iso_utc(syn_freeze)} SYN_REPORT {core.iso_utc(syn_report)} SYN_CHECKPOINT {core.iso_utc(syn_checkpoint)} ACTUAL_RAW {actual_raw}", flush=True)

# profiled Freeze via public API (no handmade fields)
out_freeze, out_manifest = profiled.build_profiled_freeze(FIX, cfg, state_path, syn_freeze)
print(f"FREEZE_BUILT freeze={out_freeze.relative_to(FIX)} sha={sha(out_freeze)[:12]} manifest={out_manifest.relative_to(FIX)} sha={sha(out_manifest)[:12]}", flush=True)
assert out_freeze.resolve()==freeze_path.resolve() and out_manifest.resolve()==manifest_path.resolve(), "profiled outputs must be canonical stable paths"
# validate manifest via public validator
pubmod.validate_release_manifest(FIX, out_manifest)
print("MANIFEST_VALID", flush=True)
# freeze must bind exact active Candidate (State-bound in revised mode)
frz = json.loads(out_freeze.read_bytes())
assert frz["publication_candidate_path"]==str(cand_path.relative_to(FIX)) and frz["publication_candidate_sha256"]==sha(cand_path), "freeze must bind active Candidate"
man = json.loads(out_manifest.read_bytes())
assert man["pdf_sha256"]==cand["pdf"]["sha256"], "manifest PDF must equal Candidate PDF"

# stage report fresh canonical
report_path = src_root / "orchestration/v2/reviews/RELEASE_CANDIDATE-core-contract.json"
reviews_path = src_root / "orchestration/v2/reviews/RELEASE_CANDIDATE-reviews.json"
assert not report_path.exists() and not reviews_path.exists(), "canonical collision on stage report/reviews"

supplied = {"freeze-record": out_freeze, "release-manifest": out_manifest, "visual-review-record": visual_path}
stage.validate_stage(FIX, cfg, state_path, supplied, report_path, syn_report)
print(f"VALIDATE_STAGE PASS report={report_path.relative_to(FIX)} sha={sha(report_path)[:12]}", flush=True)

core.write_json(reviews_path, {"reviews": [{
    "check_id": "CORE_STAGE_CONTRACT",
    "kind": "DETERMINISTIC",
    "executor": "weekly-state-lifecycle-phase3 synthetic; exact frozen authority",
    "evidence": "Public stage.validate_stage PASS for exact profiled Freeze + Candidate Visual Review; no genuine Human approval",
    "result_path": str(report_path.relative_to(FIX)),
}]})
checkpoint_path = agent.build_stage_checkpoint(FIX, cfg, state_path, supplied, reviews_path, "Weekly U4 RELEASE_CANDIDATE->FROZEN via exact profiled Freeze; synthetic; no genuine approval", syn_checkpoint, None)
print(f"CHECKPOINT {checkpoint_path.relative_to(FIX)} sha={sha(checkpoint_path)[:12]}", flush=True)
expected_canonical = agent.canonical_checkpoint_path(FIX, cfg, before_state)
assert checkpoint_path.resolve()==expected_canonical.resolve()
assert expected_canonical.relative_to(FIX)==Path("sources/2026-W37/orchestration/v2/checkpoints/RELEASE_CANDIDATE.json")

updated = agent.advance_with_checkpoint(FIX, cfg, state_path, checkpoint_path)
print(f"ADVANCED lifecycle={updated['lifecycle_state']} terminal={updated['terminal_reason']}", flush=True)

after = {
    "state_sha256": sha(state_path),
    "lifecycle": updated["lifecycle_state"],
    "next_action": updated["next_action"],
    "terminal_reason": updated["terminal_reason"],
    "pointer": updated["publication_revalidation_provenance"],
    "machine_freeze": updated["machine_checkpoints"].get("freeze"),
    "machine_release": updated["machine_checkpoints"].get("release"),
    "history_len": len(updated["history"]),
    "history_last": updated["history"][-1],
    "checkpoint_provenance_freeze": updated["checkpoint_provenance"].get("freeze"),
    "tool_head": subprocess.run(["git","-C",str(FIX),"rev-parse","HEAD"],capture_output=True,text=True).stdout.strip(),
    "freeze": {"path": str(out_freeze.relative_to(FIX)), "sha256": sha(out_freeze)},
    "manifest": {"path": str(out_manifest.relative_to(FIX)), "sha256": sha(out_manifest)},
    "visual": {"path": str(visual_path.relative_to(FIX)), "sha256": sha(visual_path)},
    "report": {"path": str(report_path.relative_to(FIX)), "sha256": sha(report_path)},
    "reviews": {"path": str(reviews_path.relative_to(FIX)), "sha256": sha(reviews_path)},
    "checkpoint": {"path": str(checkpoint_path.relative_to(FIX)), "sha256": sha(checkpoint_path)},
    "syn_freeze": core.iso_utc(syn_freeze),
    "syn_report": core.iso_utc(syn_report),
    "syn_checkpoint": core.iso_utc(syn_checkpoint),
    "actual_utc_raw": actual_raw,
}
print("AFTER "+json.dumps(after, indent=1), flush=True)

errors = agent.validate_agent_state(FIX, cfg, updated)
assert errors==[], errors
assert updated["lifecycle_state"]=="FROZEN"
assert updated["machine_checkpoints"]["freeze"]=="passed"
assert updated["history"][-1]=={"from":"RELEASE_CANDIDATE","to":"FROZEN","recorded_at":core.iso_utc(syn_checkpoint),"repository_commit_sha":"afab1762a90ca568b333abae7f1641ea64bdb5df"}
assert updated["checkpoint_provenance"]["freeze"]=={"path": str(checkpoint_path.relative_to(FIX)), "sha256": sha(checkpoint_path)}
assert updated["publication_revalidation_provenance"]==before["pointer"]
# noncanonical preserved
assert noncanon.exists(), "noncanonical low-level must be preserved, not deleted"

(EVID/"before.json").write_text(json.dumps(before, indent=1), encoding="utf-8")
(EVID/"after.json").write_text(json.dumps(after, indent=1), encoding="utf-8")
(EVID/"transition.json").write_text(json.dumps({"before": before, "after": after}, indent=1), encoding="utf-8")
print("PHASE3 PASS", flush=True)
