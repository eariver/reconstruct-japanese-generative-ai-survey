#!/usr/bin/env python3
"""Minimal repro probes for two foreign-scope integration faults (no foreign edits).

Part A (B-owned runner routing): ordinary selection/architecture runner on a
  LEGACY same-triplet EVIDENCE_REVIEWED state.
  _dm022_is_prearch_state (triplet-shape heuristic) == True, but
  low.resolve_research_authority (kind dispatch) == LEGACY, so
  sel_runner.run raises "PREARCH research resolution did not return PREARCH
  family" while all legacy-branch inputs are healthy.

Part B (screening/drafting basis, no DM022, no hand-built states): screening
  package prepared at ISSUE_INITIALIZED, then ONE real stage advance
  (ISSUE_INITIALIZED->DISCOVERY_COLLECTED via public agent APIs), then
  screening.validate_package_basis (as drafting basis loader calls it)
  raises "Screening package basis drift: state_sha256".

Exit codes: 0 = both reproduced exactly; 1 = probe setup failure (not target
fault); 2 = unexpected outcome (bug absent or different).
"""
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

PRIVATE = Path("/tmp/dm022-full-lifecycle-private-20261028T120000Z")
sys.path.insert(0, str(PRIVATE))

from tests.test_dm022_full_lifecycle_v2 import Dm022FullLifecycleWitnessTests  # noqa: E402


def _new_case():
    return Dm022FullLifecycleWitnessTests(
        methodName="test_weekly_present_old_seven_slots_retain_clear_regenerate")


def part_a() -> int:
    print("=== Part A: legacy same-triplet runner routing ===")
    case = _new_case()
    try:
        chain = case._chain_root("WEEKLY")
        state_abs = case._make_evidence_reviewed_state(chain)
        case._materialize_production_discovery_acceptance(chain)
        root = chain["root"]
        cfg = chain["cfg"]

        from scripts import survey_production_v2 as core
        from scripts import survey_research_authority_v2 as low
        from scripts import survey_agent_control_v2 as agent
        from scripts import run_selection_architecture_v2_interactive as sel_runner
        from scripts import survey_screening_v2 as screening_mod

        state = core.load_json(state_abs)
        prov = state["checkpoint_provenance"]
        print("triplet same path+sha:",
              prov["evidence"] == prov["materiality"] == prov["completeness"])
        print("_dm022_is_prearch_state:", sel_runner._dm022_is_prearch_state(state))
        resolved = low.resolve_research_authority(root, state_abs)
        print("resolve family:", resolved.get("family"))
        print("strict State errors:", agent.validate_agent_state(root, cfg, state))
        print("legacy evidence/views resolve:",
              bool(agent.resolve_active_evidence_views(root, cfg, state)))

        discoveries = screening_mod.read_jsonl(chain["discovery_path"])
        screening_doc = core.load_json(chain["screening_acceptance"])
        dec_map = {r["discovery_id"]: r["decision"] for r in screening_doc.get("decisions", [])}
        expected_ids = {d["discovery_id"] for d in discoveries
                        if dec_map.get(d["discovery_id"]) in ("KEEP", "MAYBE", "INSPECT")}
        old_input = case._build_selection_input(
            root, chain["issue_id"], expected_ids, "old-repro", "WEEKLY")
        try:
            sel_runner.run(root, state_abs, old_input)
        except ValueError as exc:
            print("sel_runner.run raised ValueError:", str(exc)[:200])
            if "PREARCH research resolution did not return PREARCH family" in str(exc):
                print("PART A REPRODUCED")
                return 0
            print("PART A DIFFERENT ValueError (unexpected)")
            traceback.print_exc()
            return 2
        print("PART A UNEXPECTED: runner succeeded")
        return 2
    finally:
        try:
            case.tearDown()
        except Exception:
            pass


def part_b() -> int:
    print("=== Part B: screening basis drift after one real advance (no DM022) ===")
    case = _new_case()
    try:
        chain = case._chain_root("WEEKLY")
        case._materialize_production_discovery_acceptance(chain)
        root = chain["root"]
        cfg = chain["cfg"]
        head, _ = case._git_init(root)
        impl = head

        from scripts import survey_production_v2 as core
        from scripts import survey_agent_control_v2 as agent
        from scripts import survey_screening_v2 as screening_mod

        profile = core.load_json(chain["profile_path"])
        source_root = root / profile["paths"]["source_root"]
        state_path = chain["state_path"]
        # Screening package prepared at ISSUE_INITIALIZED (real helper).
        print("state lifecycle at prepare:",
              core.load_json(state_path)["lifecycle_state"])
        # ONE real stage advance via public APIs (no hand-built states).
        disc_accept = source_root / "discovery" / "discovery-accepted-v2.json"
        from tests.test_dm022_full_lifecycle_v2 import _sha_file  # noqa
        result_path = source_root / "reviews" / "probe-b-core.json"
        result_path.parent.mkdir(parents=True, exist_ok=True)
        state = core.load_json(state_path)
        profile_path = chain["profile_path"]
        stage = cfg["orchestration"]["stage_plan"][state["lifecycle_state"]]
        core.write_json(result_path, {
            "schema_version": "2.0-rc1", "check_id": "CORE_STAGE_CONTRACT",
            "status": "PASS", "issue_id": state["issue_id"],
            "from_state": state["lifecycle_state"], "to_state": stage["next_state"],
            "production_state": {"path": str(state_path.relative_to(root)),
                                 "sha256": core.sha256_file(state_path)},
            "production_profile": {"path": str(profile_path.relative_to(root)),
                                   "sha256": core.sha256_file(profile_path)},
            "implementation_commit_sha": core.repository_commit_sha(root, impl),
            "contract": core.contract_identity(
                root, cfg, state["research_profile"], state["publication_profile"]),
            "artifacts": [{"name": "discovery-acceptance",
                           "path": str(disc_accept.relative_to(root)),
                           "sha256": core.sha256_file(disc_accept)}],
            "recorded_at": "2026-10-28T05:00:00Z",
        })
        reviews_path = source_root / "reviews" / "probe-b-reviews.json"
        core.write_json(reviews_path, {"reviews": [{
            "check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC",
            "executor": "probe-b", "evidence": "probe",
            "result_path": str(result_path.relative_to(root))}]})
        checkpoint = agent.build_stage_checkpoint(
            root, cfg, state_path,
            {"discovery-acceptance": disc_accept}, reviews_path,
            "Probe B discovery stage.", datetime(2026, 10, 28, 5, 0, 0, tzinfo=timezone.utc))
        updated = agent.advance_with_checkpoint(root, cfg, state_path, checkpoint)
        print("advanced lifecycle:", updated["lifecycle_state"])
        # Drafting-basis loader call on the accepted package copy.
        run_dirs = sorted((root / "sources" / chain["issue_id"] / "screening" / "v2" / "runs").glob("*"))
        screening_acceptance = None
        for run_dir in run_dirs:
            cand = run_dir / "screening-accepted.json"
            if cand.is_file():
                screening_acceptance = cand
                break
        assert screening_acceptance is not None, "screening acceptance missing"
        package_path = screening_acceptance.parent / "package.json"
        package = core.load_json(package_path)
        try:
            screening_mod.validate_package_basis(
                root, package_path, package, core.repository_commit_sha(root, impl))
        except ValueError as exc:
            print("validate_package_basis raised ValueError:", str(exc)[:200])
            if "state_sha256" in str(exc):
                print("PART B REPRODUCED")
                return 0
            print("PART B DIFFERENT ValueError (unexpected)")
            traceback.print_exc()
            return 2
        print("PART B UNEXPECTED: basis valid after advance")
        return 2
    finally:
        try:
            case.tearDown()
        except Exception:
            pass


def main() -> int:
    try:
        ra = part_a()
    except Exception as exc:
        print("PART A PROBE SETUP FAILURE:", type(exc).__name__, str(exc)[:500])
        traceback.print_exc()
        return 1
    try:
        rb = part_b()
    except Exception as exc:
        print("PART B PROBE SETUP FAILURE:", type(exc).__name__, str(exc)[:500])
        traceback.print_exc()
        return 1
    print(f"summary: part_a={ra} part_b={rb}")
    return 0 if (ra == 0 and rb == 0) else 2


if __name__ == "__main__":
    sys.exit(main())
