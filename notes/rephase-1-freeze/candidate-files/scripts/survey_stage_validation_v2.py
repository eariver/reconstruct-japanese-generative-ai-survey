#!/usr/bin/env python3
"""Deterministic stage-contract validation for the compact agent-first hot path.

This module validates the exact artifacts ChatGPT intends to adopt at the next
local lifecycle transition. It deliberately does not create Action Specs,
Handoffs, Action Results, or Validation Attestations. The output is one small
PASS report referenced by the Stage Checkpoint's CORE_STAGE_CONTRACT review.

Post-W33/SP001 redesign note: DRAFT_COMPLETE now validates an explicitly
reader-facing manuscript plus deterministic, semantic/editorial, and exact-PDF
visual authority before VALIDATED_DRAFT. Shared Core does not author that prose.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from scripts import survey_agent_control_v2 as agent
from scripts import survey_agent_tool_v2 as runtime_tool
from scripts import survey_architecture_v2 as architecture
from scripts import survey_completeness_v2 as completeness
from scripts import survey_draft_profile_v2 as draft_profile
from scripts import survey_drafting_v2 as drafting
from scripts import survey_evidence_v2 as evidence
from scripts import survey_production_v2 as core
from scripts import survey_publication_v2 as publication
from scripts import survey_quality_v2 as quality
from scripts import survey_reader_publication_v2 as reader
from scripts import survey_reader_surface_gate_v2 as surface_gate
from scripts import survey_review_attention_v2 as review_attention
from scripts import survey_schema_v2 as schema_gate
from scripts import survey_screening_v2 as screening

LOCAL_STAGES = {
    "ISSUE_INITIALIZED",
    "DISCOVERY_COLLECTED",
    "CANDIDATES_NORMALIZED",
    "EVIDENCE_REVIEWED",
    "SELECTION_COMPLETE",
    "ARCHITECTURE_ESTABLISHED",
    "DRAFT_COMPLETE",
    "VALIDATED_DRAFT",
    "RELEASE_CANDIDATE",
}

REQUIRED_CURRENT = {
    "ISSUE_INITIALIZED": {"discovery-acceptance"},
    "DISCOVERY_COLLECTED": {"screening-acceptance"},
    "CANDIDATES_NORMALIZED": {
        "evidence-acceptance",
        "edition-views-acceptance",
        "materiality-ledger",
        "profile-completeness",
    },
    "EVIDENCE_REVIEWED": {"candidate-matrix", "candidate-selection"},
    "SELECTION_COMPLETE": {
        "issue-architecture",
        "architecture-review-summary",
        "architecture-review-attention",
    },
    "ARCHITECTURE_ESTABLISHED": {"synthesis-input", "synthesis-result"},
    "DRAFT_COMPLETE": {
        "reader-manuscript",
        "validated-source",
        "publication-pdf",
        "quality-regression-bundle",
        "semantic-review",
        "visual-review",
        "reader-surface-gate",
    },
    "VALIDATED_DRAFT": {"publication-candidate"},
    "RELEASE_CANDIDATE": {"freeze-record", "release-manifest", "visual-review-record"},
}


class StageValidationError(ValueError):
    pass


def _rel(repo_root: Path, path: Path) -> str:
    root = repo_root.resolve()
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(root)).replace("\\", "/")
    except ValueError as exc:
        raise StageValidationError(f"stage artifact must be repository-local: {path}") from exc


def _safe_file(repo_root: Path, path: Path, label: str) -> Path:
    rel = _rel(repo_root, path)
    resolved = core.repo_local_path(repo_root, rel, label)
    if resolved.is_symlink() or not resolved.is_file():
        raise StageValidationError(f"{label} missing or unsafe: {rel}")
    return resolved


def _authority(repo_root: Path, name: str, path: Path) -> dict[str, str]:
    file = _safe_file(repo_root, path, name)
    return {"name": name, "path": _rel(repo_root, file), "sha256": core.sha256_file(file)}


def _authority_ref_path(repo_root: Path, ref: dict[str, Any], label: str) -> Path:
    if not isinstance(ref, dict) or set(ref) != {"path", "sha256"}:
        raise StageValidationError(f"{label} authority fields invalid")
    path = core.repo_local_path(repo_root, ref["path"], label)
    if path.is_symlink() or not path.is_file() or core.sha256_file(path) != ref["sha256"]:
        raise StageValidationError(f"{label} authority drift")
    return path


def _profile(repo_root: Path, cfg: dict[str, Any], state: dict[str, Any]) -> tuple[Path, dict[str, Any]]:
    path = _authority_ref_path(repo_root, state["profile"], "Production Profile")
    payload = core.load_json(path)
    errors = core.validate_profile(payload, cfg)
    if errors:
        raise StageValidationError("Production Profile invalid under current contract: " + "; ".join(errors))
    if payload.get("issue_id") != state.get("issue_id"):
        raise StageValidationError("Production Profile/State issue identity mismatch")
    return path, payload


def _publication_approval_artifacts(repo_root: Path, cfg: dict[str, Any], state: dict[str, Any]) -> dict[str, Path]:
    """Resolve the typed approval also stored in checkpoint provenance.

    This is Human authority, not a Stage Checkpoint. Bind its approved Candidate
    into the same artifact map so a different prior Candidate cannot replace it.
    """
    human = state.get("human_gate_provenance", {}).get("publication_preview")
    checkpoint = state.get("checkpoint_provenance", {}).get("publication_preview")
    if state.get("human_gates", {}).get("publication_preview") != "approved":
        if human is not None or checkpoint is not None or state.get("lifecycle_state") in {"RELEASE_CANDIDATE", "FROZEN", "RELEASED"}:
            raise StageValidationError("publication transition requires approved Human Preview authority")
        return {}
    if human is None or human != checkpoint or state.get("machine_checkpoints", {}).get("publication_preview") != "passed":
        raise StageValidationError("Human Preview and checkpoint approval authorities disagree")
    _, _, source_root = agent._profile_and_source(repo_root, cfg, state)
    approval_path = _authority_ref_path(repo_root, human, "Publication Preview Approval")
    canonical = source_root / cfg["state_authority"]["publication_preview_approval_path"]
    if human["path"] != _rel(repo_root, canonical):
        raise StageValidationError("Publication Preview approval path is not canonical")
    approval = publication.validate_preview_approval(repo_root, approval_path, issue_id=state["issue_id"])
    candidate_path = _authority_ref_path(repo_root, {
        "path": approval["publication_candidate_path"],
        "sha256": approval["publication_candidate_sha256"],
    }, "approved Publication Candidate")
    candidate = core.load_json(candidate_path)  # recursively validated by approval
    if candidate["publication_profile"] != state["publication_profile"]:
        raise StageValidationError("approved Candidate publication Profile mismatch")
    manuscript = core.load_json(core.repo_local_path(repo_root, candidate["reader_manuscript"]["path"], "approved Reader Manuscript"))
    if manuscript["research_profile"] != state["research_profile"]:
        raise StageValidationError("approved Candidate research Profile mismatch")
    return {"publication-candidate": candidate_path}


def _prior_artifacts(repo_root: Path, cfg: dict[str, Any], state: dict[str, Any]) -> dict[str, Path]:
    result = _publication_approval_artifacts(repo_root, cfg, state)
    seen_checkpoint_paths: set[str] = set()
    revalidation, revalidation_errors = agent.resolve_active_publication_revalidation(repo_root, cfg, state)
    if revalidation_errors:
        raise StageValidationError("active publication revalidation invalid: " + "; ".join(revalidation_errors))
    superseded: dict[tuple[str, str], str] = {}
    bound_prior: str | None = None
    if revalidation is not None:
        bound_prior = revalidation["prior_checkpoint"]["path"]
        superseded = {
            (row["name"], row["path"]): row["new_sha256"]
            for row in revalidation.get("superseded_artifacts", [])
        }
    for name, ref in state.get("checkpoint_provenance", {}).items():
        if name == "publication_preview":
            # Fully validated above through its own schema and active pointers.
            continue
        if ref is None:
            continue
        path = _authority_ref_path(repo_root, ref, "prior Stage Checkpoint")
        rel = _rel(repo_root, path)
        if rel in seen_checkpoint_paths:
            continue
        seen_checkpoint_paths.add(rel)
        record = schema_gate.load_and_validate_json(path, repo_root / agent.CHECKPOINT_SCHEMA, label="prior Stage Checkpoint")
        if record.get("issue_id") != state.get("issue_id"):
            raise StageValidationError("prior Stage Checkpoint issue identity mismatch")
        for row in record.get("artifacts", []):
            artifact = core.repo_local_path(repo_root, row["path"], f"prior artifact {row['name']}")
            expected = row["sha256"]
            if bound_prior is not None and rel == bound_prior:
                expected = superseded.get((row["name"], row["path"]), expected)
            if artifact.is_symlink() or not artifact.is_file() or core.sha256_file(artifact) != expected:
                raise StageValidationError(f"prior Stage Checkpoint artifact drift: {row['name']}")
            existing = result.get(row["name"])
            if existing is not None and existing.resolve() != artifact.resolve():
                raise StageValidationError(f"prior Stage Checkpoints disagree on artifact name: {row['name']}")
            result[row["name"]] = artifact
    return result


def _current_artifacts(repo_root: Path, state: dict[str, Any], values: dict[str, Path]) -> dict[str, Path]:
    lifecycle = state["lifecycle_state"]
    required = REQUIRED_CURRENT.get(lifecycle)
    if required is None:
        raise StageValidationError(f"no compact local stage validator for lifecycle: {lifecycle}")
    missing = sorted(required - set(values))
    if missing:
        raise StageValidationError("current stage artifacts missing: " + ", ".join(missing))
    if lifecycle != "ARCHITECTURE_ESTABLISHED":
        extra = sorted(set(values) - required)
        if extra:
            raise StageValidationError("unexpected current stage artifacts: " + ", ".join(extra))
    else:
        extras = set(values) - set(required)
        if any(not (name.startswith("draft-package:") or name.startswith("draft-result:")) for name in extras):
            raise StageValidationError("Draft stage extras must use draft-package:<id> or draft-result:<id>")
        packages = {name.split(":", 1)[1] for name in extras if name.startswith("draft-package:")}
        results = {name.split(":", 1)[1] for name in extras if name.startswith("draft-result:")}
        if not packages or packages != results:
            raise StageValidationError("Draft stage requires exactly paired draft-package:/draft-result: artifacts")
    return {name: _safe_file(repo_root, path, f"current artifact {name}") for name, path in values.items()}


def _merge_artifacts(prior: dict[str, Path], current: dict[str, Path]) -> dict[str, Path]:
    merged = dict(prior)
    for name, path in current.items():
        if name in merged and merged[name].resolve() != path.resolve():
            raise StageValidationError(f"current stage attempts to replace accepted upstream artifact: {name}")
        merged[name] = path
    return merged


def _require(mapping: dict[str, Path], *names: str) -> list[Path]:
    missing = [name for name in names if name not in mapping]
    if missing:
        raise StageValidationError("stage validation missing artifact authorities: " + ", ".join(missing))
    return [mapping[name] for name in names]


def _discovery_path(repo_root: Path, artifacts: dict[str, Path], issue_id: str) -> Path:
    (accepted_path,) = _require(artifacts, "discovery-acceptance")
    accepted = core.load_json(accepted_path)
    if accepted.get("issue_id") != issue_id:
        raise StageValidationError("Discovery acceptance issue identity mismatch")
    discovery_path = core.repo_local_path(repo_root, accepted.get("discovery_path"), "accepted Discovery JSONL")
    if discovery_path.is_symlink() or not discovery_path.is_file():
        raise StageValidationError("accepted Discovery JSONL missing")
    return discovery_path


def _evidence_basis(
    repo_root: Path,
    state: dict[str, Any],
    profile_path: Path,
    artifacts: dict[str, Path],
    implementation_sha: str,
) -> dict[str, Path]:
    root_discovery_path = _discovery_path(repo_root, artifacts, state["issue_id"])
    screening_path, evidence_path, views_path, ledger_path, completeness_path = _require(
        artifacts,
        "screening-acceptance",
        "evidence-acceptance",
        "edition-views-acceptance",
        "materiality-ledger",
        "profile-completeness",
    )
    package_path = screening_path.parent / "package.json"
    effective = screening.resolve_effective_discovery_basis(
        repo_root,
        package_path,
        implementation_sha,
        accepted_root_path=root_discovery_path,
    )
    discovery_path = effective["path"]
    evidence.validate_screening_acceptance(repo_root, screening_path, discovery_path, state["issue_id"], implementation_sha)
    evidence.validate_evidence_acceptance(repo_root, evidence_path, implementation_sha)
    evidence.validate_edition_views_acceptance(repo_root, profile_path, evidence_path, views_path, implementation_sha)
    ledger = core.load_json(ledger_path)
    evidence.validate_materiality_ledger(
        ledger,
        repo_root,
        profile_path,
        discovery_path,
        screening_path,
        evidence_path,
        views_path,
        implementation_sha,
    )
    completeness_payload = schema_gate.load_and_validate_json(
        completeness_path,
        repo_root / Path("schemas/profile-completeness-result.schema.json"),
        label="Profile Completeness",
    )
    errors = completeness.validate_profile_completeness(
        completeness_payload,
        repo_root,
        profile_path,
        discovery_path,
        screening_path,
        evidence_path,
        views_path,
        ledger_path,
        implementation_sha,
    )
    if errors:
        raise StageValidationError("Profile Completeness invalid: " + "; ".join(errors))
    return {
        "discovery": discovery_path,
        "screening": screening_path,
        "evidence": evidence_path,
        "views": views_path,
        "ledger": ledger_path,
        "completeness": completeness_path,
    }


def _selection_basis(
    repo_root: Path,
    state: dict[str, Any],
    profile_path: Path,
    artifacts: dict[str, Path],
    implementation_sha: str,
) -> dict[str, Path]:
    basis = _evidence_basis(repo_root, state, profile_path, artifacts, implementation_sha)
    matrix_path, selection_path = _require(artifacts, "candidate-matrix", "candidate-selection")
    matrix = schema_gate.load_and_validate_json(matrix_path, repo_root / Path("schemas/candidate-matrix-v2.schema.json"), label="Candidate Matrix")
    errors = architecture.validate_candidate_matrix(
        matrix,
        repo_root,
        profile_path,
        basis["discovery"],
        basis["screening"],
        basis["evidence"],
        basis["views"],
        basis["ledger"],
        basis["completeness"],
        implementation_sha,
    )
    if errors:
        raise StageValidationError("Candidate Matrix invalid: " + "; ".join(errors))
    selection = schema_gate.load_and_validate_json(
        selection_path, repo_root / Path("schemas/candidate-selection-v2.schema.json"), label="Candidate Selection"
    )
    errors = architecture.validate_selection(repo_root, selection, profile_path, matrix_path, basis["completeness"], basis["ledger"])
    if errors:
        raise StageValidationError("Candidate Selection invalid: " + "; ".join(errors))
    return {**basis, "matrix": matrix_path, "selection": selection_path}


def _validate_stage_semantics(
    repo_root: Path,
    cfg: dict[str, Any],
    state: dict[str, Any],
    profile_path: Path,
    profile: dict[str, Any],
    artifacts: dict[str, Path],
    current: dict[str, Path],
    implementation_sha: str,
) -> None:
    lifecycle = state["lifecycle_state"]
    if lifecycle == "ISSUE_INITIALIZED":
        (accepted_path,) = _require(current, "discovery-acceptance")
        accepted = __import__("scripts.survey_discovery_v2", fromlist=["validate_acceptance"]).validate_acceptance(repo_root, accepted_path)
        if accepted["issue_id"] != state["issue_id"]:
            raise StageValidationError("Discovery acceptance issue identity mismatch")
        return

    if lifecycle == "DISCOVERY_COLLECTED":
        discovery_path = _discovery_path(repo_root, artifacts, state["issue_id"])
        (screening_path,) = _require(current, "screening-acceptance")
        accepted = screening.validate_acceptance(repo_root, screening_path, implementation_sha)
        if accepted["issue_id"] != state["issue_id"]:
            raise StageValidationError("Screening acceptance issue identity mismatch")
        screening.resolve_effective_discovery_basis(
            repo_root,
            screening_path.parent / "package.json",
            implementation_sha,
            accepted_root_path=discovery_path,
        )
        return

    if lifecycle == "CANDIDATES_NORMALIZED":
        _evidence_basis(repo_root, state, profile_path, artifacts, implementation_sha)
        return

    if lifecycle == "EVIDENCE_REVIEWED":
        _selection_basis(repo_root, state, profile_path, artifacts, implementation_sha)
        return

    if lifecycle == "SELECTION_COMPLETE":
        basis = _selection_basis(repo_root, state, profile_path, artifacts, implementation_sha)
        architecture_path, review_path, attention_path = _require(
            current, "issue-architecture", "architecture-review-summary", "architecture-review-attention"
        )
        plan = schema_gate.load_and_validate_json(architecture_path, repo_root / Path("schemas/issue-architecture-v2.schema.json"), label="Issue Architecture")
        errors = architecture.validate_architecture(
            repo_root,
            plan,
            profile_path,
            basis["completeness"],
            basis["ledger"],
            basis["matrix"],
            basis["selection"],
            require_approved=False,
        )
        if errors:
            raise StageValidationError("Issue Architecture invalid: " + "; ".join(errors))
        review = schema_gate.load_and_validate_json(
            review_path,
            repo_root / Path("schemas/architecture-review-summary-v2.schema.json"),
            label="Architecture Review Summary",
        )
        expected = architecture.build_architecture_review_summary(
            repo_root,
            profile_path,
            basis["discovery"],
            basis["screening"],
            basis["evidence"],
            basis["views"],
            basis["ledger"],
            basis["completeness"],
            basis["matrix"],
            basis["selection"],
            architecture_path,
            implementation_sha,
        )
        if review != expected:
            raise StageValidationError("Architecture Review Summary differs from validated derivation")
        review_attention.validate_attention(repo_root, attention_path)
        return

    if lifecycle == "ARCHITECTURE_ESTABLISHED":
        architecture_path, review_path = _require(artifacts, "issue-architecture", "architecture-review-summary")
        approval_ref = state.get("human_gate_provenance", {}).get("architecture_review")
        approval_path = _authority_ref_path(repo_root, approval_ref, "Architecture Approval")
        approval = core.load_json(approval_path)
        errors = drafting.validate_architecture_approval(approval, architecture_path, review_path, state["issue_id"])
        if errors:
            raise StageValidationError("Architecture Approval invalid: " + "; ".join(errors))
        package_ids = sorted(name.split(":", 1)[1] for name in current if name.startswith("draft-package:"))
        draft_pairs: list[tuple[Path, Path]] = []
        for package_id in package_ids:
            package_path = current[f"draft-package:{package_id}"]
            result_path = current[f"draft-result:{package_id}"]
            package = core.load_json(package_path)
            result = core.load_json(result_path)
            errors = draft_profile.validate_extension_propagation(result, package)
            if errors:
                raise StageValidationError(f"Draft extension propagation invalid for {package_id}: " + "; ".join(errors))
            draft_pairs.append((package_path, result_path))
        expected_input = drafting.build_synthesis_input(repo_root, profile_path, architecture_path, review_path, approval_path, draft_pairs)
        synthesis_input_path, synthesis_result_path = _require(current, "synthesis-input", "synthesis-result")
        if core.load_json(synthesis_input_path) != expected_input:
            raise StageValidationError("Profile Synthesis Input differs from validated Draft Package/Result set")
        synthesis_result = schema_gate.load_and_validate_json(
            synthesis_result_path, repo_root / drafting.SYNTHESIS_RESULT_SCHEMA, label="Profile Synthesis Result"
        )
        errors = drafting.validate_synthesis_result(synthesis_result, synthesis_input_path, repo_root / drafting.SYNTHESIS_PROMPT)
        if errors:
            raise StageValidationError("Profile Synthesis Result invalid: " + "; ".join(errors))
        return

    if lifecycle == "DRAFT_COMPLETE":
        (
            manuscript_path,
            source_path,
            pdf_path,
            bundle_path,
            semantic_path,
            visual_path,
            gate_path,
        ) = _require(
            current,
            "reader-manuscript",
            "validated-source",
            "publication-pdf",
            "quality-regression-bundle",
            "semantic-review",
            "visual-review",
            "reader-surface-gate",
        )
        manuscript = reader.validate_manuscript_manifest(repo_root, manuscript_path, issue_id=state["issue_id"])
        if manuscript["research_profile"] != profile["research_profile"] or manuscript["publication_profile"] != profile["publication_profile"]:
            raise StageValidationError("Reader Manuscript Profile identity differs from Production Profile")
        if manuscript["primary_source"]["path"] != _rel(repo_root, source_path) or manuscript["primary_source"]["sha256"] != core.sha256_file(source_path):
            raise StageValidationError("Reader Manuscript does not bind exact validated source")
        bundle = quality.validate_bundle(repo_root, bundle_path, issue_id=state["issue_id"])
        if bundle["research_profile"] != profile["research_profile"] or bundle["publication_profile"] != profile["publication_profile"]:
            raise StageValidationError("Quality Bundle Profile identity differs from Production Profile")
        if bundle["source"]["path"] != _rel(repo_root, source_path) or bundle["source"]["sha256"] != core.sha256_file(source_path):
            raise StageValidationError("Quality Bundle does not bind exact validated source")
        if bundle["pdf"]["storage"] != "REPOSITORY_FILE":
            raise StageValidationError("validated draft requires repository-resident exact PDF bytes for ChatGPT/Human review")
        if (
            bundle["pdf"]["path"] != _rel(repo_root, pdf_path)
            or bundle["pdf"]["sha256"] != core.sha256_file(pdf_path)
            or bundle["pdf"]["byte_count"] != pdf_path.stat().st_size
        ):
            raise StageValidationError("Quality Bundle does not bind exact publication PDF bytes")
        semantic = reader.validate_review_record(repo_root, semantic_path, issue_id=state["issue_id"], expected_kind="SEMANTIC_EDITORIAL")
        visual = reader.validate_review_record(repo_root, visual_path, issue_id=state["issue_id"], expected_kind="VISUAL")
        for label, review in (("Semantic", semantic), ("Visual", visual)):
            if review["reader_manuscript"]["path"] != _rel(repo_root, manuscript_path) or review["reader_manuscript"]["sha256"] != core.sha256_file(manuscript_path):
                raise StageValidationError(f"{label} review does not bind exact Reader Manuscript")
            if review["source"]["path"] != _rel(repo_root, source_path) or review["source"]["sha256"] != core.sha256_file(source_path):
                raise StageValidationError(f"{label} review does not bind exact validated source")
            if review["pdf"]["path"] != _rel(repo_root, pdf_path) or review["pdf"]["sha256"] != core.sha256_file(pdf_path):
                raise StageValidationError(f"{label} review does not bind exact publication PDF")
        try:
            surface_gate.validate_reader_surface_gate(
                repo_root,
                gate_path,
                issue_id=state["issue_id"],
                publication_profile=profile["publication_profile"],
            )
        except ValueError as exc:
            raise StageValidationError(f"Reader-Surface Gate validation failed: {exc}") from exc
        return

    if lifecycle == "VALIDATED_DRAFT":
        (candidate_path,) = _require(current, "publication-candidate")
        (
            manuscript_path,
            source_path,
            pdf_path,
            bundle_path,
            semantic_path,
            visual_path,
            gate_path,
        ) = _require(
            artifacts,
            "reader-manuscript",
            "validated-source",
            "publication-pdf",
            "quality-regression-bundle",
            "semantic-review",
            "visual-review",
            "reader-surface-gate",
        )
        candidate = publication.validate_candidate(repo_root, candidate_path, issue_id=state["issue_id"])
        if candidate["publication_profile"] != profile["publication_profile"]:
            raise StageValidationError("Publication Candidate publication Profile mismatch")
        expected_refs = {
            "reader_manuscript": manuscript_path,
            "source": source_path,
            "quality_bundle": bundle_path,
            "semantic_review": semantic_path,
            "visual_review": visual_path,
        }
        for key, expected_path in expected_refs.items():
            if candidate[key]["path"] != _rel(repo_root, expected_path) or candidate[key]["sha256"] != core.sha256_file(expected_path):
                raise StageValidationError(f"Publication Candidate does not bind exact {key}")
        if (
            candidate["pdf"]["path"] != _rel(repo_root, pdf_path)
            or candidate["pdf"]["sha256"] != core.sha256_file(pdf_path)
            or candidate["pdf"]["byte_count"] != pdf_path.stat().st_size
        ):
            raise StageValidationError("Publication Candidate does not bind exact publication PDF bytes")
        try:
            surface_gate.validate_reader_surface_gate(
                repo_root,
                gate_path,
                issue_id=state["issue_id"],
                publication_profile=profile["publication_profile"],
            )
        except ValueError as exc:
            raise StageValidationError(f"Reader-Surface Gate validation failed: {exc}") from exc
        return

    if lifecycle == "RELEASE_CANDIDATE":
        (candidate_path,) = _require(artifacts, "publication-candidate")
        freeze_path, manifest_path, visual_path = _require(current, "freeze-record", "release-manifest", "visual-review-record")
        approval_ref = state.get("human_gate_provenance", {}).get("publication_preview")
        approval_path = _authority_ref_path(repo_root, approval_ref, "Publication Preview Approval")
        approval = publication.validate_preview_approval(repo_root, approval_path, issue_id=state["issue_id"])
        candidate = publication.validate_candidate(repo_root, candidate_path, issue_id=state["issue_id"])
        candidate_visual_path = core.repo_local_path(repo_root, candidate["visual_review"]["path"], "Candidate Visual Review")
        if _rel(repo_root, visual_path) != candidate["visual_review"]["path"] or core.sha256_file(visual_path) != candidate["visual_review"]["sha256"]:
            raise StageValidationError("Freeze visual-review-record must be the Candidate pre-preview Visual Review")
        visual = reader.validate_review_record(repo_root, candidate_visual_path, issue_id=state["issue_id"], expected_kind="VISUAL")
        freeze = schema_gate.load_and_validate_json(freeze_path, repo_root / publication.FREEZE_SCHEMA, label="Freeze record")
        manifest = publication.validate_release_manifest(repo_root, manifest_path)
        if freeze.get("publication_candidate_path") != _rel(repo_root, candidate_path) or freeze.get("publication_candidate_sha256") != core.sha256_file(candidate_path):
            raise StageValidationError("Freeze record does not bind exact Publication Candidate")
        if freeze.get("publication_preview_approval_path") != _rel(repo_root, approval_path) or freeze.get("publication_preview_approval_sha256") != core.sha256_file(approval_path):
            raise StageValidationError("Freeze record does not bind exact Publication Preview approval")
        if freeze.get("visual_review_path") != _rel(repo_root, candidate_visual_path) or freeze.get("visual_review_sha256") != core.sha256_file(candidate_visual_path):
            raise StageValidationError("Freeze record does not bind Candidate pre-preview Visual Review")
        if candidate["pdf"]["sha256"] != approval["pdf_sha256"] or visual["pdf"]["sha256"] != approval["pdf_sha256"] or manifest["pdf_sha256"] != approval["pdf_sha256"]:
            raise StageValidationError("Publication Preview/Candidate Visual/Freeze/Manifest PDF authority diverged")
        return

    raise StageValidationError(f"unsupported local lifecycle: {lifecycle}")


def validate_stage(
    repo_root: Path,
    cfg: dict[str, Any],
    state_path: Path,
    supplied: dict[str, Path],
    output_path: Path,
    recorded_at: datetime,
) -> Path:
    state = core.load_json(state_path)
    if state.get("lifecycle_state") not in LOCAL_STAGES:
        raise StageValidationError("stage-contract validation is only for local pre-release lifecycle stages")
    errors = agent.validate_agent_state(repo_root, cfg, state)
    if errors:
        raise StageValidationError("Production State invalid before stage validation: " + "; ".join(errors))
    if state.get("terminal_reason") == "HUMAN_GATE_REACHED":
        raise StageValidationError("cannot validate a local transition while the State is waiting at a Human Gate")
    if state.get("terminal_reason") not in {None, ""}:
        raise StageValidationError(f"cannot validate terminal State: {state.get('terminal_reason')}")

    profile_path, profile = _profile(repo_root, cfg, state)
    current = _current_artifacts(repo_root, state, supplied)
    prior = _prior_artifacts(repo_root, cfg, state)
    artifacts = _merge_artifacts(prior, current)
    current_impl = core.repository_commit_sha(repo_root)

    with runtime_tool.current_stage_basis_override():
        _validate_stage_semantics(repo_root, cfg, state, profile_path, profile, artifacts, current, current_impl)

    current_contract = core.contract_identity(repo_root, cfg, state["research_profile"], state["publication_profile"])
    report = {
        "schema_version": "2.0-rc1",
        "check_id": "CORE_STAGE_CONTRACT",
        "status": "PASS",
        "issue_id": state["issue_id"],
        "from_state": state["lifecycle_state"],
        "to_state": cfg["orchestration"]["stage_plan"][state["lifecycle_state"]]["next_state"],
        "production_state": {"path": _rel(repo_root, state_path), "sha256": core.sha256_file(state_path)},
        "production_profile": {"path": _rel(repo_root, profile_path), "sha256": core.sha256_file(profile_path)},
        "implementation_commit_sha": current_impl,
        "contract": current_contract,
        "artifacts": sorted((_authority(repo_root, name, path) for name, path in current.items()), key=lambda row: row["name"]),
        "recorded_at": core.iso_utc(recorded_at),
    }
    if output_path.exists():
        raise StageValidationError(f"refusing to overwrite stage validation report: {output_path}")
    core.write_json(output_path, report)
    return output_path


def _parse_artifacts(values: list[str]) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for value in values:
        if "=" not in value:
            raise StageValidationError("--artifact must use NAME=PATH")
        name, raw = value.split("=", 1)
        if not name or not raw or name in result:
            raise StageValidationError("--artifact names/paths must be unique and non-empty")
        result[name] = Path(raw)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--config", default=str(core.DEFAULT_CONFIG))
    parser.add_argument("--state", required=True)
    parser.add_argument("--artifact", action="append", default=[])
    parser.add_argument("--output", required=True)
    parser.add_argument("--recorded-at")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    cfg_path = Path(args.config)
    if not cfg_path.is_absolute():
        cfg_path = root / cfg_path
    state_path = Path(args.state)
    if not state_path.is_absolute():
        state_path = root / state_path
    output = Path(args.output)
    if not output.is_absolute():
        output = root / output
    artifacts = {name: (path if path.is_absolute() else root / path) for name, path in _parse_artifacts(args.artifact).items()}
    now = core.parse_instant(args.recorded_at) if args.recorded_at else datetime.now(timezone.utc)
    try:
        path = validate_stage(root, core.load_json(cfg_path), state_path, artifacts, output, now)
        print(path)
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
