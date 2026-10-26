#!/usr/bin/env python3
"""Phase2: synthetic approve_publication_preview on RELEASE_CANDIDATE.
Bounded exact selected Candidate/PDF, explicit fixture decision, no genuine Human/Production claim.
Typed Human/checkpoint agreement via public agent.approve_publication_preview.
"""
import os, sys, json, hashlib, subprocess
from pathlib import Path
from datetime import datetime, timezone

REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-weekly-state-lifecycle-20261025T101500Z/renewal-weekly"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-state-lifecycle/phase2-20261025T101500Z"
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

before_state = json.loads(state_path.read_bytes())
before = {
    "state_sha256": sha(state_path),
    "lifecycle": before_state["lifecycle_state"],
    "human_preview": before_state["human_gates"].get("publication_preview"),
    "human_provenance": before_state["human_gate_provenance"].get("publication_preview"),
    "machine_preview": before_state["machine_checkpoints"].get("publication_preview"),
    "pointer": before_state["publication_revalidation_provenance"],
    "history_len": len(before_state["history"]),
    "history_last": before_state["history"][-1],
    "tool_head": subprocess.run(["git","-C",str(FIX),"rev-parse","HEAD"],capture_output=True,text=True).stdout.strip(),
}
print("BEFORE "+json.dumps(before, indent=1), flush=True)
assert before["lifecycle"]=="RELEASE_CANDIDATE", before["lifecycle"]
assert before["human_preview"]=="pending" and before["human_provenance"] is None

sel = setmod.resolve_publication_selection(FIX, cfg, before_state)
assert sel["mode"]=="VERSIONED_ACTIVE"
cand_path = FIX / sel["candidate_ref"]["path"]
cand = pubmod.validate_candidate(FIX, cand_path, issue_id=ISSUE)
print(f"CANDIDATE {sel['candidate_ref']['path']} pdf={cand['pdf']['sha256'][:12]} pages={cand['pdf'].get('page_count')}", flush=True)
assert cand["pdf"]["sha256"]=="8fb8aca78a28fb2dc12c54b0cb2609a0d3d4575d09fb5e3a2d064cfc3133dc43"
assert cand["pdf"]["page_count"]==5

syn_at = core.parse_instant("2026-10-25T09:20:00Z")
actual_raw = datetime.now(timezone.utc).isoformat()
print(f"SYN_APPROVAL {core.iso_utc(syn_at)} ACTUAL_RAW {actual_raw}", flush=True)

# canonical approval path must not exist (fresh collision-safe)
_, _, src_root = agent._profile_and_source(FIX, cfg, before_state)
approval_rel = cfg["state_authority"]["publication_preview_approval_path"]  # gates/publication-preview-approval.json
approval_path = src_root / approval_rel
assert not approval_path.exists(), f"canonical collision: approval exists {approval_path}"

updated = agent.approve_publication_preview(FIX, cfg, state_path, "synthetic-human-fixture", syn_at, "synthetic:weekly-u4-preview; NO genuine Human/Production approval; explicit fixture decision bounded to exact U4 Candidate/PDF")
print(f"APPROVED lifecycle={updated['lifecycle_state']} human={updated['human_gates']['publication_preview']} machine={updated['machine_checkpoints']['publication_preview']}", flush=True)

after = {
    "state_sha256": sha(state_path),
    "lifecycle": updated["lifecycle_state"],
    "human_preview": updated["human_gates"].get("publication_preview"),
    "human_provenance": updated["human_gate_provenance"].get("publication_preview"),
    "machine_preview": updated["machine_checkpoints"].get("publication_preview"),
    "checkpoint_preview": updated["checkpoint_provenance"].get("publication_preview"),
    "pointer": updated["publication_revalidation_provenance"],
    "history_len": len(updated["history"]),
    "history_last": updated["history"][-1],
    "tool_head": subprocess.run(["git","-C",str(FIX),"rev-parse","HEAD"],capture_output=True,text=True).stdout.strip(),
    "approval": {"path": str(approval_path.relative_to(FIX)), "sha256": sha(approval_path)},
    "syn_approval": core.iso_utc(syn_at),
    "actual_utc_raw": actual_raw,
}
print("AFTER "+json.dumps(after, indent=1), flush=True)

# strict checks
errors = agent.validate_agent_state(FIX, cfg, updated)
assert errors==[], errors
assert updated["lifecycle_state"]=="RELEASE_CANDIDATE", "approval must stay RELEASE_CANDIDATE"
assert updated["human_gates"]["publication_preview"]=="approved"
assert updated["machine_checkpoints"]["publication_preview"]=="passed"
assert updated["human_gate_provenance"]["publication_preview"]==updated["checkpoint_provenance"]["publication_preview"], "Human/checkpoint agreement"
assert updated["human_gate_provenance"]["publication_preview"]["path"]==str(approval_path.relative_to(FIX))
# approval binds exact candidate/PDF
appr = pubmod.validate_preview_approval(FIX, approval_path, issue_id=ISSUE)
assert appr["publication_candidate_sha256"]==sha(cand_path), "approval must bind exact active Candidate"
assert appr["pdf_sha256"]==cand["pdf"]["sha256"], "approval must bind exact PDF"
# history must NOT advance on approval? Check: approve_publication_preview does not append history? It only updates gates. Verify history_len unchanged.
assert len(updated["history"])==len(before_state["history"]), f"approval should not append history (got {len(updated['history'])} vs {len(before_state['history'])})"
assert updated["publication_revalidation_provenance"]==before["pointer"], "sole active pointer unchanged"

(EVID/"before.json").write_text(json.dumps(before, indent=1), encoding="utf-8")
(EVID/"after.json").write_text(json.dumps(after, indent=1), encoding="utf-8")
(EVID/"transition.json").write_text(json.dumps({"before": before, "after": after, "note": "Synthetic preview approval bounded to exact U4 Candidate/PDF; no genuine Human/Production claim; history unchanged, gates+provenance advanced, sole pointer exact"}, indent=1), encoding="utf-8")
print("PHASE2 PASS", flush=True)
