#!/usr/bin/env python3
"""Run the frozen Evidence/Materiality/Completeness chain over the derived
compatibility package (edition-local driver).

This driver replicates scripts/run_evidence_v2_interactive.py run() call
sequence step-for-step, substituting ONLY the Evidence package: the
edition-local derived compatibility package (built + validated + repro-tested
by build_compat_evidence_package.py) instead of a freshly built normal
package. Every judgment step uses unmodified frozen Core functions:

- agent.validate_agent_state
- discovery.validate_acceptance, screening.resolve_active_screening_acceptance,
  screening.resolve_effective_discovery_basis
- evidence.validate_evidence_package_basis, evidence.task_authority_sources
- run_evidence_v2_interactive.validate_interactive_input / _build_card /
  _build_view / _build_completeness / _archive_input (imported, unmodified)
- evidence.validate_evidence_card, accept_evidence_results,
  validate_evidence_acceptance, validate_edition_view, accept_edition_views,
  validate_edition_views_acceptance, build_materiality_ledger,
  write_materiality_ledger
- schema_gate.validate_instance, completeness.validate_profile_completeness

Frozen override contexts (survey_agent_tool_v2.current_stage_basis_override)
are entered at exactly the same call sites as the frozen runner (historical
state-SHA tolerance only). No Core module is modified; no validator is
weakened; no alternative acceptance logic exists in this file.
"""
from __future__ import annotations

import json
from pathlib import Path

from scripts import run_evidence_v2_interactive as runner_mod
from scripts import survey_agent_control_v2 as agent
from scripts import survey_agent_tool_v2 as agent_tool
from scripts import survey_completeness_v2 as completeness
from scripts import survey_discovery_v2 as discovery
from scripts import survey_evidence_v2 as evidence
from scripts import survey_production_v2 as core
from scripts import survey_schema_v2 as schema_gate
from scripts import survey_screening_v2 as screening

ISSUE_ID = "SP-efficient-llm-2026"
SOURCE_ROOT_REL = "sources/SP-efficient-llm-2026"
STATE_REL = SOURCE_ROOT_REL + "/production-state.json"
COMPAT_PACKAGE_REL = ("sources/SP-efficient-llm-2026/execution/compat/"
                      "evidence-source-class-projection/compat-package/package.json")

# Edition-authored rows for Discovery-named obligations outside the Profile's
# initial set (gap-fill lanes). Dimensions are Profile-declared; ID lists use
# the frozen builder's mechanical derivation; statuses/rationales are Luna
# provisional annotations exactly like the input-supplied initial rows.
EXTRA_OBLIGATIONS = [
    {
        "obligation_id": "EFF-O13",
        "dimension": "attention_sequence_kv_cache",
        "description": ("Conditional memory via scalable lookup (Engram) as a sparsity axis "
                        "complementary to MoE conditional computation, with retrieval-precedent "
                        "boundaries (kNN-LM, RETRO) and Qwen-PLE parallel-lineage assessment."),
        "status": "LIMITATION",
        "rationale": ("Engram paper consumed at body level with allocation law and delta table; "
                      "official repo release-level; Qwen-PLE lineage ruled parallel/unresolved; "
                      "kNN-LM/RETRO boundary precedents consumed. Static-lookup fusion and "
                      "allocation-curve detail outstanding as stated per-record limitations."),
    },
    {
        "obligation_id": "EFF-O14",
        "dimension": "decoding_acceleration",
        "description": ("Test-time compute scaling: compute-optimal allocation, budget forcing, "
                        "learned chain-of-thought pruning (ThinkPrune), overthinking and "
                        "early stopping, adaptive-TTC taxonomy, and production effort-control "
                        "binding."),
        "status": "LIMITATION",
        "rationale": ("Snell/s1/ThinkPrune/overthinking bodies consumed with headline numbers; "
                      "effort-control binding corroborated via consumed recipe; survey "
                      "follow-up pools (D152/D156) deferred to Sol gap-fill judgment; "
                      "per-table ablations outstanding as stated per-record limitations."),
    },
    {
        "obligation_id": "EFF-O15",
        "dimension": "inference_kernels_serving",
        "description": ("Model routing and cascading at inference time: FrugalGPT cascade origin, "
                        "RouteLLM preference-data routing, 2026 survey unification, and "
                        "router-fragility limitation evidence."),
        "status": "LIMITATION",
        "rationale": ("FrugalGPT body results and RouteLLM data pipeline consumed; survey "
                      "unifier secondary-by-design with follow-ups deferred; fragility "
                      "counterexample bounds routing-gain claims; D158 is an accepted "
                      "Screening DROP. Results-table detail outstanding as stated."),
    },
]


def _extra_obligation_rows(discovery_records, ledger) -> list:
    ledger_task_by_discovery = {
        row["discovery_id"]: list(row["evidence_task_ids"]) for row in ledger["rows"]
    }
    rows = []
    for spec in EXTRA_OBLIGATIONS:
        oid = spec["obligation_id"]
        declaring = sorted(
            row["discovery_id"] for row in discovery_records
            if oid in row.get("provenance", {}).get("obligation_ids", []))
        if not declaring:
            raise ValueError(f"extra obligation {oid} names no Discovery records")
        task_ids = sorted({
            task_id for did in declaring for task_id in ledger_task_by_discovery.get(did, [])})
        rows.append({
            "obligation_id": oid,
            "dimension": spec["dimension"],
            "description": spec["description"],
            "status": spec["status"],
            "discovery_ids": declaring,
            "evidence_task_ids": task_ids,
            "rationale": spec["rationale"],
        })
    return rows


def main() -> int:
    root = Path(".").resolve()
    state_path = root / STATE_REL
    compat_package_path = root / COMPAT_PACKAGE_REL
    input_path = root / ("sources/SP-efficient-llm-2026/execution/"
                         "evidence-interactive-input-r2/interactive-evidence-r2.json")
    for path in (state_path, compat_package_path, input_path):
        if not path.is_file():
            raise ValueError(f"missing driver input: {path}")

    cfg = core.load_json(root / core.DEFAULT_CONFIG)
    state = core.load_json(state_path)
    errors = agent.validate_agent_state(root, cfg, state)
    if errors:
        raise ValueError("Production State invalid before Evidence: " + "; ".join(errors))
    if state.get("lifecycle_state") != "CANDIDATES_NORMALIZED":
        raise ValueError("Evidence requires CANDIDATES_NORMALIZED Production State")

    profile_path = root / state["profile"]["path"]
    profile = core.load_json(profile_path)
    source_root = core.repo_local_path(root, profile["paths"]["source_root"], "paths.source_root")
    discovery_acceptance_path = source_root / "discovery/discovery-accepted-v2.json"
    accepted_discovery = discovery.validate_acceptance(root, discovery_acceptance_path)
    root_discovery_path = core.repo_local_path(root, accepted_discovery["discovery_path"], "accepted Discovery JSONL")

    implementation_sha = core.repository_commit_sha(root)
    active_screening = screening.resolve_active_screening_acceptance(root, state_path, implementation_sha)
    screening_acceptance_path = Path(active_screening["path"])
    effective = screening.resolve_effective_discovery_basis(
        root, screening_acceptance_path.parent / "package.json",
        implementation_sha, accepted_root_path=root_discovery_path)
    discovery_path = Path(effective["path"])
    discovery_records = effective["records"]

    package = core.load_json(compat_package_path)
    with agent_tool.current_stage_basis_override():
        evidence.validate_evidence_package_basis(root, compat_package_path, package, implementation_sha)
    task_meta = {meta["discovery_ids"][0]: meta for meta in package["tasks"]}
    expected_ids = set(task_meta)
    with agent_tool.current_stage_basis_override():
        task_source_ids = {
            did: set(evidence.task_authority_sources(
                root, core.load_json(compat_package_path.parent / meta["path"]), package))
            for did, meta in task_meta.items()
        }
    interactive_doc = core.load_json(input_path)
    records_by_id, runner, completeness_input = runner_mod.validate_interactive_input(
        interactive_doc, profile, expected_ids, task_source_ids)

    import tempfile
    with tempfile.TemporaryDirectory() as temp:
        temp_root = Path(temp)
        results_dir = temp_root / "evidence-results"
        results_dir.mkdir()
        for did in sorted(task_meta):
            meta = task_meta[did]
            task = core.load_json(compat_package_path.parent / meta["path"])
            card = runner_mod._build_card(root, task, meta, package, records_by_id[did], runner)
            errs = evidence.validate_evidence_card(card, task, meta["sha256"], package, repo_root=root)
            if errs:
                raise ValueError(f"Evidence Card {did} invalid: {'; '.join(errs)}")
            core.write_json(results_dir / Path(meta["path"]).name, card)

        evidence_root = source_root / "evidence/v2/accepted"
        with agent_tool.current_stage_basis_override():
            evidence_acceptance_path = evidence.accept_evidence_results(
                root, compat_package_path, results_dir, evidence_root, implementation_sha)
            evidence_acceptance, _ = evidence.validate_evidence_acceptance(
                root, evidence_acceptance_path, implementation_sha)

        evidence_by_task = {row["evidence_task_id"]: row for row in evidence_acceptance["results"]}
        views_dir = temp_root / "views"
        views_dir.mkdir()
        for did in sorted(task_meta):
            meta = task_meta[did]
            task_id = meta["evidence_task_id"]
            entry = evidence_by_task[task_id]
            view = runner_mod._build_view(profile, task_id, entry["sha256"], records_by_id[did])
            errs = evidence.validate_edition_view(view, profile, entry["sha256"], entry["status"])
            if errs:
                raise ValueError(f"Edition View {did} invalid: {'; '.join(errs)}")
            core.write_json(views_dir / evidence.view_filename(task_id), view)

        views_root = source_root / "evidence/v2/views/accepted"
        with agent_tool.current_stage_basis_override():
            views_acceptance_path = evidence.accept_edition_views(
                root, profile_path, evidence_acceptance_path, views_dir, views_root, implementation_sha)
            evidence.validate_edition_views_acceptance(
                root, profile_path, evidence_acceptance_path, views_acceptance_path, implementation_sha)

        ledger_path = source_root / "materiality-ledger-v2.json"
        if ledger_path.exists():
            raise ValueError(f"refusing to overwrite Materiality Ledger: {ledger_path}")
        with agent_tool.current_stage_basis_override():
            ledger = evidence.build_materiality_ledger(
                root, profile_path, discovery_path, screening_acceptance_path,
                evidence_acceptance_path, views_acceptance_path, implementation_sha)
        evidence.write_materiality_ledger(ledger_path, ledger)

        completeness_path = source_root / "profile-completeness-v2.json"
        if completeness_path.exists():
            raise ValueError(f"refusing to overwrite Profile Completeness: {completeness_path}")
        result = runner_mod._build_completeness(
            root, profile, profile_path, discovery_records, ledger_path, ledger, completeness_input)
        # Frozen _build_completeness emits Profile initial obligations only, but
        # the frozen profile guard (survey_completeness_v2) additionally requires
        # every obligation ID named in Discovery provenance (here the r2/r3
        # gap-fill lanes EFF-O13/O14/O15) to appear as a row. Those rows are
        # edition-authored here with the frozen builder's own mechanical
        # derivation for discovery_ids/evidence_task_ids; every judgment step
        # below (shape, dimension membership, references, closure derivation,
        # overall status) is still performed by the unchanged frozen
        # validators. No frozen derivation is altered.
        result["obligations"] = list(result["obligations"]) + _extra_obligation_rows(
            discovery_records, ledger)
        schema_gate.validate_instance(
            result, root / "schemas/profile-completeness-result.schema.json", label="Profile Completeness")
        with agent_tool.current_stage_basis_override():
            errs = completeness.validate_profile_completeness(
                result, root, profile_path, discovery_path, screening_acceptance_path,
                evidence_acceptance_path, views_acceptance_path, ledger_path, implementation_sha)
        if errs:
            raise ValueError("Profile Completeness invalid: " + "; ".join(errs))
        core.write_json(completeness_path, result)

    outputs = {
        "evidence_acceptance": str(evidence_acceptance_path.relative_to(root)),
        "edition_views_acceptance": str(views_acceptance_path.relative_to(root)),
        "materiality_ledger": str(ledger_path.relative_to(root)),
        "profile_completeness": str(completeness_path.relative_to(root)),
    }
    runner_mod._archive_input(root, evidence_acceptance_path, input_path, runner, outputs)
    print(json.dumps({
        **outputs,
        "evidence_result_count": core.load_json(evidence_acceptance_path)["result_count"],
        "completeness_status": core.load_json(completeness_path)["overall_status"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
