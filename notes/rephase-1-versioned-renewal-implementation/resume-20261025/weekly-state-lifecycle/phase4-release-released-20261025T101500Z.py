#!/usr/bin/env python3
"""Phase4: FROZEN->RELEASED via offline synthetic merge/release + public release-checkpoint/advance.
Same existing test contract, no real GitHub/network writes/tags.
"""
import os, sys, json, hashlib, subprocess
from pathlib import Path
from datetime import datetime, timezone

REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-weekly-state-lifecycle-20261025T101500Z/renewal-weekly"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-state-lifecycle/phase4-20261025T101500Z"
EVID.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(FIX.resolve()))
for k in ["GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"]:
    assert k not in os.environ
assert not (FIX/".git/objects/info/alternates").exists()

from scripts import survey_production_v2 as core
from scripts import survey_agent_control_v2 as agent
from scripts import survey_release_checkpoint_v2 as release_checkpoint
from scripts import survey_publication_v2 as pubmod
from scripts import survey_publication_set_v2 as setmod

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
    "machine_release": before_state["machine_checkpoints"].get("release"),
    "pointer": before_state["publication_revalidation_provenance"],
    "history_len": len(before_state["history"]),
    "history_last": before_state["history"][-1],
    "tool_head": subprocess.run(["git","-C",str(FIX),"rev-parse","HEAD"],capture_output=True,text=True).stdout.strip(),
}
print("BEFORE "+json.dumps(before, indent=1), flush=True)
assert before["lifecycle"]=="FROZEN"
assert before_state["machine_checkpoints"]["release"]=="pending"

# stage_plan for FROZEN
assert cfg["orchestration"]["stage_plan"]["FROZEN"]["action_kind"]=="WORKFLOW_DISPATCH"
assert cfg["orchestration"]["stage_plan"]["FROZEN"]["next_state"]=="RELEASED"

_, _, src_root = agent._profile_and_source(FIX, cfg, before_state)
pub_root = src_root / "publication/v2"
manifest_path = pub_root / "release-manifest-v2.json"
assert manifest_path.is_file(), "frozen manifest must exist from Phase3"
freeze_path = pub_root / "freeze-record-v2.json"
assert freeze_path.is_file()
merge_path = pub_root / "merge-verification-v2.json"
record_path = pub_root / "release-record-v2.json"
core_contract_path = pub_root / "core-stage-contract-v2.json"
assert not merge_path.exists(), f"canonical collision merge exists {merge_path}"
assert not record_path.exists(), f"canonical collision record exists {record_path}"
assert not core_contract_path.exists(), f"canonical collision core contract exists {core_contract_path}"
# canonical checkpoint for FROZEN must be fresh
expected_canonical = agent.canonical_checkpoint_path(FIX, cfg, before_state)
assert expected_canonical.relative_to(FIX)==Path("sources/2026-W37/orchestration/v2/checkpoints/FROZEN.json")
assert not expected_canonical.exists(), f"canonical collision checkpoint exists {expected_canonical}"

syn_merge = core.parse_instant("2026-10-25T09:40:00Z")
syn_release = core.parse_instant("2026-10-25T09:40:30Z")
syn_checkpoint = core.parse_instant("2026-10-25T09:41:00Z")
actual_raw = datetime.now(timezone.utc).isoformat()
head = subprocess.run(["git","-C",str(FIX),"rev-parse","HEAD"],capture_output=True,text=True).stdout.strip()
print(f"SYN_MERGE {core.iso_utc(syn_merge)} SYN_RELEASE {core.iso_utc(syn_release)} SYN_CHECKPOINT {core.iso_utc(syn_checkpoint)} ACTUAL_RAW {actual_raw} HEAD {head[:12]}", flush=True)
assert head=="afab1762a90ca568b333abae7f1641ea64bdb5df", "artifact-only HEAD allowed, must be afab176"

# offline synthetic external evidence via same test contract (no GitHub/network)
pubmod.build_merge_verification(FIX, manifest_path, head, syn_merge, merge_path)
print(f"MERGE_BUILT {merge_path.relative_to(FIX)} sha={sha(merge_path)[:12]}", flush=True)
pubmod.build_release_record(FIX, manifest_path, merge_path, syn_release, "weekly-u4-synthetic-release; NO real GitHub/network/tags; explicit fixture decision", record_path)
print(f"RECORD_BUILT {record_path.relative_to(FIX)} sha={sha(record_path)[:12]}", flush=True)
# public validators for record
pubmod.validate_release_record(FIX, record_path)

checkpoint_path = release_checkpoint.build_release_checkpoint(FIX, cfg, state_path, merge_path, record_path, syn_checkpoint)
print(f"CHECKPOINT {checkpoint_path.relative_to(FIX)} sha={sha(checkpoint_path)[:12]}", flush=True)
assert checkpoint_path.resolve()==expected_canonical.resolve()
# core-stage contract sidecar must exist now
assert core_contract_path.is_file(), "core-stage contract sidecar must be created by build_release_checkpoint"
print(f"CORE_CONTRACT {core_contract_path.relative_to(FIX)} sha={sha(core_contract_path)[:12]}", flush=True)

updated = agent.advance_with_checkpoint(FIX, cfg, state_path, checkpoint_path)
print(f"ADVANCED lifecycle={updated['lifecycle_state']} terminal={updated['terminal_reason']} next={updated['next_action']}", flush=True)

after = {
    "state_sha256": sha(state_path),
    "lifecycle": updated["lifecycle_state"],
    "next_action": updated["next_action"],
    "terminal_reason": updated["terminal_reason"],
    "pointer": updated["publication_revalidation_provenance"],
    "machine_release": updated["machine_checkpoints"].get("release"),
    "history_len": len(updated["history"]),
    "history_last": updated["history"][-1],
    "checkpoint_provenance_release": updated["checkpoint_provenance"].get("release"),
    "tool_head": subprocess.run(["git","-C",str(FIX),"rev-parse","HEAD"],capture_output=True,text=True).stdout.strip(),
    "merge": {"path": str(merge_path.relative_to(FIX)), "sha256": sha(merge_path)},
    "record": {"path": str(record_path.relative_to(FIX)), "sha256": sha(record_path)},
    "core_contract": {"path": str(core_contract_path.relative_to(FIX)), "sha256": sha(core_contract_path)},
    "checkpoint": {"path": str(checkpoint_path.relative_to(FIX)), "sha256": sha(checkpoint_path)},
    "manifest": {"path": str(manifest_path.relative_to(FIX)), "sha256": sha(manifest_path)},
    "syn_merge": core.iso_utc(syn_merge),
    "syn_release": core.iso_utc(syn_release),
    "syn_checkpoint": core.iso_utc(syn_checkpoint),
    "actual_utc_raw": actual_raw,
}
print("AFTER "+json.dumps(after, indent=1), flush=True)

errors = agent.validate_agent_state(FIX, cfg, updated)
assert errors==[], errors
assert updated["lifecycle_state"]=="RELEASED"
assert updated["machine_checkpoints"]["release"]=="passed"
assert updated["history"][-1]=={"from":"FROZEN","to":"RELEASED","recorded_at":core.iso_utc(syn_checkpoint),"repository_commit_sha":head}
assert updated["checkpoint_provenance"]["release"]=={"path": str(checkpoint_path.relative_to(FIX)), "sha256": sha(checkpoint_path)}
assert updated["publication_revalidation_provenance"]==before["pointer"]

(EVID/"before.json").write_text(json.dumps(before, indent=1), encoding="utf-8")
(EVID/"after.json").write_text(json.dumps(after, indent=1), encoding="utf-8")
(EVID/"transition.json").write_text(json.dumps({"before": before, "after": after}, indent=1), encoding="utf-8")
print("PHASE4 PASS", flush=True)
