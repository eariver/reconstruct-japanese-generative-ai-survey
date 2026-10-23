#!/usr/bin/env python3
"""Foundation contracts and authoritative state for Survey Production Core v2.

The Production State is the sole lifecycle/gate authority. State transitions are
fail-closed: exact profile/contract/implementation identity, lifecycle history,
machine-checkpoint evidence, Human Gate evidence, and controller fields must
agree. Passed checkpoints and resolved Human Gates pin exact provenance bytes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from scripts import weekly_pipeline

DEFAULT_CONFIG = Path("config/survey-production-v2.json")
PROFILE_SCHEMA = Path("schemas/survey-production-profile.schema.json")
STATE_SCHEMA = Path("schemas/survey-production-state.schema.json")
WEEKLY_ISSUE_RE = re.compile(r"^(?P<year>\d{4})-W(?P<week>\d{2})$")
ISSUE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")

LIFECYCLE = (
    "ISSUE_INITIALIZED",
    "DISCOVERY_COLLECTED",
    "CANDIDATES_NORMALIZED",
    "EVIDENCE_REVIEWED",
    "SELECTION_COMPLETE",
    "ARCHITECTURE_ESTABLISHED",
    "DRAFT_COMPLETE",
    "VALIDATED_DRAFT",
    "RELEASE_CANDIDATE",
    "FROZEN",
    "RELEASED",
)

CHECKPOINTS = (
    "discovery",
    "screening",
    "evidence",
    "materiality",
    "completeness",
    "selection",
    "architecture",
    "draft",
    "validation",
    "publication_preview",
    "freeze",
    "release",
)

CONTRACT_KEYS = {
    "pipeline_contract_version",
    "pipeline_contract_sha256",
    "quality_contract_version",
    "quality_contract_sha256",
    "research_profile_version",
    "research_profile_sha256",
    "publication_profile_version",
    "publication_profile_sha256",
}

GATE_KEYS = {
    "ARCHITECTURE_REVIEW": "architecture_review",
    "PUBLICATION_PREVIEW": "publication_preview",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        value = json.load(fh)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def json_bytes(data: dict[str, Any]) -> bytes:
    return (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json_bytes(data))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sha256_object(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(payload)


def aggregate_file_hash(repo_root: Path, paths: list[str]) -> str:
    digest = hashlib.sha256()
    for rel in sorted(paths):
        path = repo_root / rel
        if not path.is_file():
            raise ValueError(f"contract file does not exist: {rel}")
        digest.update(rel.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def parse_instant(value: str) -> datetime:
    return weekly_pipeline.parse_instant(value)


def iso_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def repository_commit_sha(repo_root: Path, override: str | None = None) -> str:
    if override is not None:
        if len(override) != 40 or any(c not in "0123456789abcdef" for c in override):
            raise ValueError("implementation commit override must be a lowercase 40-hex SHA")
        return override
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ValueError("cannot resolve implementation repository commit; pass --implementation-sha") from exc
    value = result.stdout.strip()
    if len(value) != 40 or any(c not in "0123456789abcdef" for c in value):
        raise ValueError("git rev-parse HEAD did not return a lowercase 40-hex commit")
    return value


def contract_identity(repo_root: Path, cfg: dict[str, Any], research_profile: str, publication_profile: str) -> dict[str, str]:
    research = cfg["research_profiles"].get(research_profile)
    publication = cfg["publication_profiles"].get(publication_profile)
    if research is None:
        raise ValueError(f"unknown research profile: {research_profile}")
    if publication is None:
        raise ValueError(f"unknown publication profile: {publication_profile}")
    pipeline_files = list(cfg["contract_files"]["pipeline"])
    pipeline_files.extend([str(DEFAULT_CONFIG), str(PROFILE_SCHEMA), str(STATE_SCHEMA)])
    return {
        "pipeline_contract_version": cfg["pipeline_contract_version"],
        "pipeline_contract_sha256": aggregate_file_hash(repo_root, pipeline_files),
        "quality_contract_version": cfg["quality_contract_version"],
        "quality_contract_sha256": aggregate_file_hash(repo_root, list(cfg["contract_files"]["quality"])),
        "research_profile_version": research["version"],
        "research_profile_sha256": sha256_object({"name": research_profile, "contract": research}),
        "publication_profile_version": publication["version"],
        "publication_profile_sha256": sha256_object({"name": publication_profile, "contract": publication}),
    }


def validate_temporal_policy(research_profile: str, policy: dict[str, Any], cfg: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    mode = policy.get("mode")
    allowed = cfg["research_profiles"].get(research_profile, {}).get("temporal_policies", [])
    if mode not in allowed:
        return [f"temporal policy {mode!r} is not allowed for research profile {research_profile}"]

    def required(*keys: str) -> None:
        for key in keys:
            if not policy.get(key):
                errors.append(f"temporal policy {mode} requires {key}")

    if mode == "ROLLING_WINDOW":
        required("window_start", "window_end", "cutoff", "timezone")
        forbidden = {"start", "end", "as_of"}
    elif mode == "BOUNDED_PERIOD":
        required("start", "end", "as_of", "timezone")
        forbidden = {"window_start", "window_end", "cutoff"}
    elif mode in {"OPEN_HISTORY_AS_OF", "CURRENT_STATE_AS_OF"}:
        required("as_of")
        forbidden = {"start", "end", "window_start", "window_end", "cutoff", "timezone"}
    else:
        return [f"unsupported temporal policy: {mode}"]
    for key in forbidden:
        if key in policy:
            errors.append(f"temporal policy {mode} forbids {key}")
    for key, value in policy.items():
        if key in {"mode", "timezone"}:
            continue
        try:
            parse_instant(str(value))
        except ValueError:
            errors.append(f"temporal policy {mode} field {key} must be an offset-aware ISO-8601 instant")
    return errors


def _nonempty_string_list(value: Any) -> bool:
    return (
        isinstance(value, list)
        and len(value) == len(set(value))
        and all(isinstance(item, str) and bool(item.strip()) for item in value)
    )


def _safe_relative_repo_path(value: Any) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = Path(value)
    return not path.is_absolute() and ".." not in path.parts


def repo_local_path(repo_root: Path, value: str, label: str) -> Path:
    if not _safe_relative_repo_path(value):
        raise ValueError(f"{label} must be a repository-relative path without traversal")
    root = repo_root.resolve()
    resolved = (root / value).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{label} escapes repository root") from exc
    return resolved


def _validate_initial_obligations(scope: dict[str, Any], errors: list[str]) -> None:
    dimensions = scope.get("scope_dimensions")
    if not _nonempty_string_list(dimensions) or not dimensions:
        errors.append("research_scope.scope_dimensions must be a non-empty unique string array")
        dimensions = []
    allowed_dimensions = set(dimensions)
    obligations = scope.get("initial_obligations")
    if not isinstance(obligations, list) or not obligations:
        errors.append("research_scope.initial_obligations must contain at least one obligation")
        return
    seen_ids: set[str] = set()
    covered_dimensions: set[str] = set()
    expected_fields = {"obligation_id", "dimension", "description"}
    for index, obligation in enumerate(obligations):
        prefix = f"research_scope.initial_obligations[{index}]"
        if not isinstance(obligation, dict) or set(obligation) != expected_fields:
            errors.append(f"{prefix} fields must exactly match the v2 Profile contract")
            continue
        obligation_id = obligation.get("obligation_id")
        dimension = obligation.get("dimension")
        description = obligation.get("description")
        if not isinstance(obligation_id, str) or not obligation_id.strip():
            errors.append(f"{prefix}.obligation_id must be non-empty")
        elif obligation_id in seen_ids:
            errors.append(f"duplicate initial obligation_id: {obligation_id}")
        else:
            seen_ids.add(obligation_id)
        if dimension not in allowed_dimensions:
            errors.append(f"{prefix}.dimension must reference a declared scope dimension")
        else:
            covered_dimensions.add(dimension)
        if not isinstance(description, str) or not description.strip():
            errors.append(f"{prefix}.description must be non-empty")
    missing_dimensions = sorted(allowed_dimensions - covered_dimensions)
    if missing_dimensions:
        errors.append(f"initial obligations do not cover Profile dimensions: {missing_dimensions}")


def validate_profile(profile: dict[str, Any], cfg: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {"schema_version", "issue_id", "research_profile", "publication_profile", "research_scope", "paths", "contract"}
    if set(profile) != required:
        missing = sorted(required - set(profile))
        extra = sorted(set(profile) - required)
        if missing:
            errors.append(f"profile missing required fields: {', '.join(missing)}")
        if extra:
            errors.append(f"profile has unsupported fields: {', '.join(extra)}")
        return errors
    if profile["schema_version"] != cfg["schema_version"]:
        errors.append("profile schema_version does not match v2 contract manifest")
    if not isinstance(profile.get("issue_id"), str) or not ISSUE_ID_RE.fullmatch(profile["issue_id"]):
        errors.append("issue_id must be a path-safe identifier")
    research_profile = profile["research_profile"]
    publication_profile = profile["publication_profile"]
    if research_profile not in cfg["research_profiles"]:
        errors.append(f"unknown research profile: {research_profile}")
    if publication_profile not in cfg["publication_profiles"]:
        errors.append(f"unknown publication profile: {publication_profile}")
    if research_profile == "WEEKLY" and publication_profile != "WEEKLY_MAGAZINE":
        errors.append("WEEKLY research profile requires WEEKLY_MAGAZINE publication profile")
    if research_profile in {"RETROSPECTIVE_PERIOD", "THEMATIC"} and publication_profile != "LONGFORM_SPECIAL":
        errors.append(f"{research_profile} research profile requires LONGFORM_SPECIAL publication profile")

    scope = profile.get("research_scope")
    scope_keys = {"question", "inclusion", "exclusion", "scope_dimensions", "initial_obligations", "temporal_policy"}
    if not isinstance(scope, dict):
        errors.append("research_scope must be an object")
    elif set(scope) != scope_keys:
        errors.append("research_scope fields must exactly match the v2 Profile contract")
    else:
        if not isinstance(scope.get("question"), str) or not scope["question"].strip():
            errors.append("research_scope.question must be non-empty")
        for key in ("inclusion", "exclusion"):
            value = scope.get(key)
            if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
                errors.append(f"research_scope.{key} must be an array of non-empty strings")
        _validate_initial_obligations(scope, errors)
        policy = scope.get("temporal_policy")
        if isinstance(policy, dict) and research_profile in cfg["research_profiles"]:
            errors.extend(validate_temporal_policy(research_profile, policy, cfg))
        elif policy is not None:
            errors.append("research_scope.temporal_policy must be an object")

    paths = profile.get("paths")
    if not isinstance(paths, dict) or set(paths) != {"source_root", "survey_root", "work_branch"}:
        errors.append("paths fields must exactly match the v2 Profile contract")
    else:
        for key in ("source_root", "survey_root"):
            if not _safe_relative_repo_path(paths.get(key)):
                errors.append(f"paths.{key} must be a repository-relative path without traversal")
        branch = paths.get("work_branch")
        if not isinstance(branch, str) or not branch.strip() or branch.startswith("/") or ".." in branch.split("/"):
            errors.append("paths.work_branch must be a non-empty relative branch name without traversal segments")

    contract = profile.get("contract")
    if not isinstance(contract, dict) or set(contract) != CONTRACT_KEYS:
        errors.append("contract fields must exactly match the v2 Profile contract")
    else:
        for key in (
            "pipeline_contract_version", "quality_contract_version",
            "research_profile_version", "publication_profile_version",
        ):
            if not isinstance(contract.get(key), str) or not contract[key]:
                errors.append(f"contract.{key} must be non-empty")
        for key in (
            "pipeline_contract_sha256", "quality_contract_sha256",
            "research_profile_sha256", "publication_profile_sha256",
        ):
            value = contract.get(key)
            if not isinstance(value, str) or len(value) != 64 or any(ch not in "0123456789abcdef" for ch in value):
                errors.append(f"contract.{key} must be a lowercase SHA-256")
    return errors


def weekly_cutoff_for_issue(issue_id: str, weekly_cfg: dict[str, Any]) -> datetime:
    match = WEEKLY_ISSUE_RE.fullmatch(issue_id)
    if match is None:
        raise ValueError(f"invalid Weekly issue id: {issue_id}; expected YYYY-Www")
    year = int(match.group("year"))
    week = int(match.group("week"))
    editorial = weekly_cfg["editorial"]
    iso_weekday = weekly_pipeline.weekday_number(editorial["cutoff_weekday"]) + 1
    try:
        day = datetime.fromisocalendar(year, week, iso_weekday)
    except ValueError as exc:
        raise ValueError(f"invalid Weekly issue id: {issue_id}") from exc
    zone = ZoneInfo(editorial["cutoff_timezone"])
    cutoff = datetime(
        day.year, day.month, day.day,
        int(editorial["cutoff_hour"]),
        int(editorial.get("cutoff_minute", 0)),
        tzinfo=zone,
    )
    if weekly_pipeline.issue_id_from_cutoff(cutoff) != issue_id:
        raise ValueError(f"Weekly issue id does not map to configured cutoff calendar: {issue_id}")
    return cutoff


def weekly_profile(repo_root: Path, cfg: dict[str, Any], now: datetime, issue_id: str | None = None) -> dict[str, Any]:
    weekly_cfg = load_json(repo_root / "config/weekly-pipeline.json")
    now_utc = now.astimezone(timezone.utc)
    if issue_id is None:
        cutoff = weekly_pipeline.latest_cutoff(now_utc, weekly_cfg)
        resolved_issue = weekly_pipeline.issue_id_from_cutoff(cutoff)
    else:
        cutoff = weekly_cutoff_for_issue(issue_id, weekly_cfg)
        if cutoff.astimezone(timezone.utc) > now_utc:
            raise ValueError(f"requested Weekly issue {issue_id} has not completed its editorial cutoff yet")
        resolved_issue = issue_id
    start, end = weekly_pipeline.editorial_window(cutoff, weekly_cfg)
    dimensions = ["current relevance", "technical significance", "carry-over obligations"]
    initial_obligations = [
        {
            "obligation_id": "weekly:current-relevance",
            "dimension": "current relevance",
            "description": "Establish which developments materially belong in this completed Weekly issue and why they matter to the issue.",
        },
        {
            "obligation_id": "weekly:technical-significance",
            "dimension": "technical significance",
            "description": "Verify and prioritize the technical significance of candidate developments without relying on Weekly timing alone.",
        },
        {
            "obligation_id": "weekly:carry-over",
            "dimension": "carry-over obligations",
            "description": "Explicitly dispose every carry-over obligation inherited from prior Weekly work.",
        },
    ]
    profile = {
        "schema_version": cfg["schema_version"],
        "issue_id": resolved_issue,
        "research_profile": "WEEKLY",
        "publication_profile": "WEEKLY_MAGAZINE",
        "research_scope": {
            "question": f"What materially changed in generative AI for {resolved_issue}, and why does it matter now?",
            "inclusion": ["material generative-AI technical developments relevant to the issue window or explicit carry-over"],
            "exclusion": ["items without material technical/editorial relevance to the issue"],
            "scope_dimensions": dimensions,
            "initial_obligations": initial_obligations,
            "temporal_policy": {
                "mode": "ROLLING_WINDOW",
                "window_start": start.isoformat(timespec="seconds"),
                "window_end": end.isoformat(timespec="seconds"),
                "cutoff": cutoff.isoformat(timespec="seconds"),
                "timezone": weekly_cfg["editorial"]["cutoff_timezone"],
            },
        },
        "paths": {
            "source_root": f"sources/{resolved_issue}",
            "survey_root": f"surveys/weekly/{resolved_issue}",
            "work_branch": f"weekly/{resolved_issue}-v2-work",
        },
        "contract": contract_identity(repo_root, cfg, "WEEKLY", "WEEKLY_MAGAZINE"),
    }
    errors = validate_profile(profile, cfg)
    if errors:
        raise ValueError("invalid generated Weekly profile: " + "; ".join(errors))
    return profile


def _thematic_initial_obligations(spec: dict[str, Any], dimensions: list[str]) -> list[dict[str, str]]:
    supplied = spec.get("initial_obligations")
    if supplied is not None:
        if not isinstance(supplied, list):
            raise ValueError("thematic initial_obligations must be an array")
        return [dict(row) if isinstance(row, dict) else row for row in supplied]
    return [
        {
            "obligation_id": f"scope:{index:02d}",
            "dimension": dimension,
            "description": f"Establish evidence-backed coverage for the thematic scope dimension: {dimension}.",
        }
        for index, dimension in enumerate(dimensions, start=1)
    ]


def thematic_profile(repo_root: Path, cfg: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    required = ("issue_id", "question", "temporal_mode", "as_of", "scope_dimensions")
    missing = [key for key in required if not spec.get(key)]
    if missing:
        raise ValueError("thematic spec missing required fields: " + ", ".join(missing))
    temporal_mode = spec["temporal_mode"]
    if temporal_mode not in {"OPEN_HISTORY_AS_OF", "CURRENT_STATE_AS_OF"}:
        raise ValueError("Thematic temporal_mode must be OPEN_HISTORY_AS_OF or CURRENT_STATE_AS_OF")
    policy = {"mode": temporal_mode, "as_of": iso_utc(parse_instant(spec["as_of"]))}
    issue_id = spec["issue_id"]
    dimensions = list(spec["scope_dimensions"])
    if not dimensions:
        raise ValueError("Thematic scope_dimensions must not be empty")
    profile = {
        "schema_version": cfg["schema_version"],
        "issue_id": issue_id,
        "research_profile": "THEMATIC",
        "publication_profile": "LONGFORM_SPECIAL",
        "research_scope": {
            "question": spec["question"],
            "inclusion": list(spec.get("inclusion", [])),
            "exclusion": list(spec.get("exclusion", [])),
            "scope_dimensions": dimensions,
            "initial_obligations": _thematic_initial_obligations(spec, dimensions),
            "temporal_policy": policy,
        },
        "paths": {
            "source_root": spec.get("source_root", f"sources/{issue_id}"),
            "survey_root": spec.get("survey_root", f"surveys/special/{issue_id}"),
            "work_branch": spec.get("work_branch", f"special/{issue_id}-v2-work"),
        },
        "contract": contract_identity(repo_root, cfg, "THEMATIC", "LONGFORM_SPECIAL"),
    }
    errors = validate_profile(profile, cfg)
    if errors:
        raise ValueError("invalid generated Thematic profile: " + "; ".join(errors))
    return profile


def derive_control_fields(state: dict[str, Any], cfg: dict[str, Any]) -> tuple[str | None, str | None]:
    if state["exception_gate"]["status"] == "required":
        return "EXCEPTION", "EXCEPTION_GATE_REQUIRED"
    lifecycle = state["lifecycle_state"]
    gate = cfg["orchestration"]["gate_at_state"].get(lifecycle)
    if gate:
        key = GATE_KEYS[gate]
        status = state["human_gates"][key]
        if status == "pending":
            return gate, "HUMAN_GATE_REACHED"
        if status == "rejected":
            return "EXCEPTION", "EXCEPTION_GATE_REQUIRED"
    if lifecycle == "RELEASED":
        return None, "COMPLETE"
    stage = cfg["orchestration"]["stage_plan"].get(lifecycle)
    if not isinstance(stage, dict):
        raise ValueError(f"no orchestration stage registered for lifecycle state {lifecycle}")
    return stage["handler"], None


def refresh_state_control(state: dict[str, Any], cfg: dict[str, Any]) -> dict[str, Any]:
    updated = deepcopy(state)
    action, terminal = derive_control_fields(updated, cfg)
    updated["next_action"] = action
    updated["terminal_reason"] = terminal
    return updated


def _checkpoint_attestation_path(repo_root: Path, cfg: dict[str, Any], profile: dict[str, Any], checkpoint: str) -> Path:
    source_root = repo_local_path(repo_root, profile["paths"]["source_root"], "paths.source_root")
    return source_root / cfg["state_authority"]["checkpoint_attestation_dir"] / f"{checkpoint}.json"


def _authority_ref(repo_root: Path, path: Path) -> dict[str, str]:
    return {
        "path": str(path.resolve().relative_to(repo_root.resolve())),
        "sha256": sha256_file(path),
    }


def _validate_authority_ref(repo_root: Path, value: Any, expected_path: Path | None, label: str) -> tuple[list[str], Path | None]:
    if not isinstance(value, dict) or set(value) != {"path", "sha256"}:
        return [f"{label} authority fields invalid"], None
    try:
        path = repo_local_path(repo_root, value.get("path"), label)
    except (TypeError, ValueError) as exc:
        return [str(exc)], None
    errors: list[str] = []
    if expected_path is not None and path != expected_path.resolve():
        errors.append(f"{label} authority path is not canonical")
    if not path.is_file():
        errors.append(f"{label} authority file missing")
    elif value.get("sha256") != sha256_file(path):
        errors.append(f"{label} authority SHA drift")
    return errors, path


def _validate_artifact_ref(repo_root: Path, ref: Any, label: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(ref, dict) or set(ref) != {"name", "path", "sha256", "required"}:
        return [f"{label} artifact ref fields invalid"]
    if not isinstance(ref.get("name"), str) or not ref["name"]:
        errors.append(f"{label} artifact ref name required")
    if not isinstance(ref.get("required"), bool):
        errors.append(f"{label} artifact ref required flag invalid")
    path_value = ref.get("path")
    sha_value = ref.get("sha256")
    if path_value is None:
        if sha_value is not None:
            errors.append(f"{label} pathless artifact ref cannot claim SHA")
    else:
        try:
            path = repo_local_path(repo_root, path_value, label)
        except (TypeError, ValueError) as exc:
            errors.append(str(exc))
            return errors
        if not path.is_file():
            errors.append(f"{label} artifact missing: {path_value}")
        elif sha_value != sha256_file(path):
            errors.append(f"{label} artifact SHA drift: {path_value}")
    return errors


def _validate_checkpoint_attestation(repo_root: Path, cfg: dict[str, Any], profile: dict[str, Any], checkpoint: str, issue_id: str, authority: Any) -> list[str]:
    canonical = _checkpoint_attestation_path(repo_root, cfg, profile, checkpoint)
    authority_errors, path = _validate_authority_ref(repo_root, authority, canonical, f"checkpoint {checkpoint}")
    if authority_errors or path is None:
        return authority_errors
    value = load_json(path)
    required = {
        "schema_version", "issue_id", "checkpoint", "action_id",
        "action_spec_sha256", "validator", "validator_version", "validated_at",
        "required_inputs", "outputs", "status",
    }
    errors: list[str] = []
    if set(value) != required:
        return [f"checkpoint attestation fields invalid: {checkpoint}"]
    if value.get("schema_version") != "2.0-rc1" or value.get("issue_id") != issue_id or value.get("checkpoint") != checkpoint or value.get("status") != "PASSED":
        errors.append(f"checkpoint attestation identity/status invalid: {checkpoint}")
    for key in ("action_id", "validator", "validator_version"):
        if not isinstance(value.get(key), str) or not value[key].strip():
            errors.append(f"checkpoint attestation {key} required: {checkpoint}")
    sha_value = value.get("action_spec_sha256")
    if not isinstance(sha_value, str) or len(sha_value) != 64 or any(c not in "0123456789abcdef" for c in sha_value):
        errors.append(f"checkpoint attestation action_spec_sha256 invalid: {checkpoint}")
    try:
        parse_instant(str(value.get("validated_at", "")))
    except ValueError:
        errors.append(f"checkpoint attestation validated_at invalid: {checkpoint}")
    for label, rows in (("input", value.get("required_inputs")), ("output", value.get("outputs"))):
        if not isinstance(rows, list):
            errors.append(f"checkpoint attestation {label}s must be array: {checkpoint}")
            continue
        for index, row in enumerate(rows):
            errors.extend(_validate_artifact_ref(repo_root, row, f"{checkpoint} attestation {label}[{index}]"))
    return errors


def _completed_stage_checkpoints(cfg: dict[str, Any], lifecycle: str) -> set[str]:
    current_index = LIFECYCLE.index(lifecycle)
    completed: set[str] = set()
    for state_name in LIFECYCLE[:current_index]:
        stage = cfg["orchestration"]["stage_plan"].get(state_name)
        if isinstance(stage, dict):
            completed.update(stage.get("checkpoints", []))
    return completed


def _valid_durable_publication_pdf(repo_root: Path, pdf_ref: dict[str, Any]) -> bool:
    storage = pdf_ref.get("storage")
    path_value = pdf_ref.get("path")
    sha_value = pdf_ref.get("sha256")
    byte_count = pdf_ref.get("byte_count")
    if not isinstance(sha_value, str) or len(sha_value) != 64 or any(c not in "0123456789abcdef" for c in sha_value):
        return False
    if not isinstance(byte_count, int) or isinstance(byte_count, bool) or byte_count < 1:
        return False
    if storage == "REPOSITORY_FILE":
        if not isinstance(path_value, str):
            return False
        try:
            path = repo_local_path(repo_root, path_value, "Publication Preview PDF")
        except ValueError:
            return False
        return path.is_file() and path.stat().st_size == byte_count and sha256_file(path) == sha_value and pdf_ref.get("actions_artifact") is None
    if storage == "GITHUB_ACTIONS_ARTIFACT":
        if not _safe_relative_repo_path(path_value):
            return False
        artifact = pdf_ref.get("actions_artifact")
        if not isinstance(artifact, dict) or set(artifact) != {"repository", "workflow_run_id", "artifact_id", "artifact_name", "artifact_digest"}:
            return False
        repository = artifact.get("repository")
        run_id = artifact.get("workflow_run_id")
        artifact_id = artifact.get("artifact_id")
        name = artifact.get("artifact_name")
        digest = artifact.get("artifact_digest")
        return (
            isinstance(repository, str)
            and re.fullmatch(r"[^/]+/[^/]+", repository) is not None
            and isinstance(run_id, int) and not isinstance(run_id, bool) and run_id >= 1
            and isinstance(artifact_id, int) and not isinstance(artifact_id, bool) and artifact_id >= 1
            and isinstance(name, str) and bool(name.strip())
            and isinstance(digest, str)
            and re.fullmatch(r"sha256:[0-9a-f]{64}", digest) is not None
        )
    return False


def validate_state_semantics(repo_root: Path, cfg: dict[str, Any], state: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if state.get("lifecycle_state") not in LIFECYCLE:
        return ["Production State lifecycle_state invalid"]
    checkpoint_value = state.get("machine_checkpoints")
    provenance_value = state.get("checkpoint_provenance")
    if not isinstance(checkpoint_value, dict) or set(checkpoint_value) != set(CHECKPOINTS):
        errors.append("Production State machine_checkpoints must exactly match canonical checkpoint set")
        checkpoints = checkpoint_value if isinstance(checkpoint_value, dict) else {}
    else:
        checkpoints = checkpoint_value
    if not isinstance(provenance_value, dict) or set(provenance_value) != set(CHECKPOINTS):
        errors.append("Production State checkpoint_provenance must exactly match canonical checkpoint set")
        checkpoint_provenance = provenance_value if isinstance(provenance_value, dict) else {}
    else:
        checkpoint_provenance = provenance_value
    expected_passed = _completed_stage_checkpoints(cfg, state["lifecycle_state"])
    if state.get("human_gates", {}).get("publication_preview") == "approved":
        expected_passed.add("publication_preview")
    try:
        profile_path = repo_local_path(repo_root, state["profile"]["path"], "state.profile.path")
        profile = load_json(profile_path)
    except (KeyError, OSError, ValueError) as exc:
        errors.append(f"Production State profile unavailable for semantic validation: {exc}")
        profile = None
    for name in CHECKPOINTS:
        status = checkpoints.get(name)
        expected = "passed" if name in expected_passed else "pending"
        if status != expected:
            errors.append(f"Production State checkpoint {name}={status!r}; expected {expected!r} for lifecycle {state['lifecycle_state']}")
        authority = checkpoint_provenance.get(name)
        if expected == "passed":
            if authority is None:
                errors.append(f"passed checkpoint lacks pinned provenance: {name}")
            elif profile is not None and name != "publication_preview":
                errors.extend(_validate_checkpoint_attestation(repo_root, cfg, profile, name, state.get("issue_id", ""), authority))
            elif name == "publication_preview":
                auth_errors, _ = _validate_authority_ref(repo_root, authority, None, "Publication Preview checkpoint")
                errors.extend(auth_errors)
        elif authority is not None:
            errors.append(f"pending checkpoint must not carry provenance: {name}")

    current_index = LIFECYCLE.index(state["lifecycle_state"])
    history = state.get("history")
    if not isinstance(history, list) or len(history) != current_index + 1:
        errors.append("Production State history length must exactly match lifecycle position")
    else:
        previous_time: datetime | None = None
        for index, row in enumerate(history):
            expected_to = LIFECYCLE[index]
            expected_from = None if index == 0 else LIFECYCLE[index - 1]
            if not isinstance(row, dict) or row.get("from") != expected_from or row.get("to") != expected_to:
                errors.append(f"Production State history[{index}] does not match canonical lifecycle path")
                continue
            if row.get("repository_commit_sha") != state.get("implementation", {}).get("repository_commit_sha"):
                errors.append(f"Production State history[{index}] implementation SHA divergence")
            try:
                instant = parse_instant(str(row.get("recorded_at", "")))
                if previous_time is not None and instant < previous_time:
                    errors.append("Production State history timestamps must be monotonic")
                previous_time = instant
            except ValueError:
                errors.append(f"Production State history[{index}].recorded_at invalid")

    gate_provenance = state.get("human_gate_provenance")
    if not isinstance(gate_provenance, dict) or set(gate_provenance) != {"architecture_review", "publication_preview"}:
        errors.append("Production State human_gate_provenance fields invalid")
        gate_provenance = {}
    arch_index = LIFECYCLE.index("ARCHITECTURE_ESTABLISHED")
    arch_status = state.get("human_gates", {}).get("architecture_review")
    arch_authority = gate_provenance.get("architecture_review")
    if current_index < arch_index and arch_status != "pending":
        errors.append("Architecture Review cannot be resolved before ARCHITECTURE_ESTABLISHED")
    if current_index > arch_index and arch_status != "approved":
        errors.append("post-Architecture lifecycle requires approved Architecture Review")
    if arch_status == "pending":
        if arch_authority is not None:
            errors.append("pending Architecture Review must not carry gate provenance")
    else:
        if arch_authority is None:
            errors.append("resolved Architecture Review lacks pinned gate provenance")
        elif profile is not None:
            source_root = repo_local_path(repo_root, profile["paths"]["source_root"], "paths.source_root")
            approval = source_root / cfg["state_authority"]["architecture_approval_path"]
            authority_errors, approval_path = _validate_authority_ref(repo_root, arch_authority, approval, "Architecture Review")
            errors.extend(authority_errors)
            architecture = source_root / "architecture-v2.json"
            review = source_root / "architecture-review-summary-v2.json"
            attention = source_root / "architecture-review-attention-v2.json"
            if arch_status == "approved" and approval_path is not None and architecture.is_file() and review.is_file() and attention.is_file():
                try:
                    record = load_json(approval_path)
                except (OSError, ValueError, json.JSONDecodeError):
                    errors.append("Architecture Approval Record unreadable")
                else:
                    if (
                        record.get("decision") != "APPROVED"
                        or record.get("issue_id") != state.get("issue_id")
                        or record.get("architecture_sha256") != sha256_file(architecture)
                        or record.get("architecture_review_summary_sha256") != sha256_file(review)
                        or record.get("architecture_review_attention_sha256") != sha256_file(attention)
                    ):
                        errors.append("Architecture Approval Record does not bind current canonical review bytes")
            elif arch_status == "approved":
                errors.append("approved Architecture Review lacks canonical Architecture/Review/Attention bytes")

    pub_index = LIFECYCLE.index("RELEASE_CANDIDATE")
    pub_status = state.get("human_gates", {}).get("publication_preview")
    pub_authority = gate_provenance.get("publication_preview")
    if current_index < pub_index and pub_status != "pending":
        errors.append("Publication Preview cannot be resolved before RELEASE_CANDIDATE")
    if current_index > pub_index and pub_status != "approved":
        errors.append("post-Publication Preview lifecycle requires approved Publication Preview")
    if pub_status == "pending":
        if pub_authority is not None:
            errors.append("pending Publication Preview must not carry gate provenance")
    elif pub_authority is None:
        errors.append("resolved Publication Preview lacks pinned gate provenance")
    else:
        if profile is None:
            errors.append("Publication Preview authority cannot be validated without Production Profile")
        else:
            source_root = repo_local_path(repo_root, profile["paths"]["source_root"], "paths.source_root")
            approval = source_root / cfg["state_authority"]["publication_preview_approval_path"]
            auth_errors, approval_path = _validate_authority_ref(repo_root, pub_authority, approval, "Publication Preview")
            errors.extend(auth_errors)
            candidate = source_root / "publication/v2/publication-candidate-v2.json"
            if pub_status == "approved" and approval_path is not None and candidate.is_file():
                try:
                    record = load_json(approval_path)
                    candidate_record = load_json(candidate)
                except (OSError, ValueError, json.JSONDecodeError):
                    errors.append("Publication Preview authority bytes unreadable")
                else:
                    candidate_rel = str(candidate.resolve().relative_to(repo_root.resolve()))
                    pdf_ref = candidate_record.get("pdf") if isinstance(candidate_record.get("pdf"), dict) else {}
                    if (
                        record.get("decision") != "APPROVED"
                        or record.get("gate") != "PUBLICATION_PREVIEW"
                        or record.get("issue_id") != state.get("issue_id")
                        or record.get("publication_candidate_path") != candidate_rel
                        or record.get("publication_candidate_sha256") != sha256_file(candidate)
                        or candidate_record.get("issue_id") != state.get("issue_id")
                        or candidate_record.get("status") != "READY_FOR_PUBLICATION_PREVIEW"
                        or record.get("pdf_path") != pdf_ref.get("path")
                        or record.get("pdf_sha256") != pdf_ref.get("sha256")
                        or record.get("page_count") != pdf_ref.get("page_count")
                        or not _valid_durable_publication_pdf(repo_root, pdf_ref)
                    ):
                        errors.append("Publication Preview Approval Record does not bind current canonical Candidate/PDF bytes")
            elif pub_status == "approved":
                errors.append("approved Publication Preview lacks canonical Candidate bytes")

    try:
        expected_action, expected_terminal = derive_control_fields(state, cfg)
    except (KeyError, ValueError) as exc:
        errors.append(f"Production State controller fields cannot be derived: {exc}")
    else:
        if state.get("next_action") != expected_action:
            errors.append(f"Production State next_action drift: {state.get('next_action')!r} != {expected_action!r}")
        if state.get("terminal_reason") != expected_terminal:
            errors.append(f"Production State terminal_reason drift: {state.get('terminal_reason')!r} != {expected_terminal!r}")
    exception = state.get("exception_gate")
    if not isinstance(exception, dict) or set(exception) != {"status", "reason"}:
        errors.append("Production State exception_gate fields invalid")
    elif exception.get("status") == "required" and not isinstance(exception.get("reason"), str):
        errors.append("required Exception Gate needs reason")
    elif exception.get("status") != "required" and exception.get("reason") is not None:
        errors.append("inactive/resolved Exception Gate reason must be null")
    return errors


def initial_state(
    repo_root: Path,
    cfg: dict[str, Any],
    profile: dict[str, Any],
    profile_path: Path,
    implementation_sha: str,
    target_gate: str,
    recorded_at: datetime,
) -> dict[str, Any]:
    if target_gate not in cfg["human_gates"]:
        raise ValueError(f"unsupported target Human Gate: {target_gate}")
    source_root = repo_local_path(repo_root, profile["paths"]["source_root"], "paths.source_root")
    legacy_path = source_root / cfg["state_authority"]["legacy_filename"]
    legacy_present = legacy_path.is_file()
    legacy_sha = sha256_file(legacy_path) if legacy_present else None
    state = {
        "schema_version": cfg["schema_version"],
        "issue_id": profile["issue_id"],
        "research_profile": profile["research_profile"],
        "publication_profile": profile["publication_profile"],
        "lifecycle_state": "ISSUE_INITIALIZED",
        "profile": {
            "path": str(profile_path.relative_to(repo_root.resolve())),
            "sha256": sha256_file(profile_path),
        },
        "contract": dict(profile["contract"]),
        "implementation": {
            "repository_commit_sha": implementation_sha,
            "orchestrator_version": cfg["orchestrator_version"],
        },
        "human_gates": {
            "architecture_review": "pending",
            "publication_preview": "pending",
        },
        "human_gate_provenance": {
            "architecture_review": None,
            "publication_preview": None,
        },
        "target_gate": target_gate,
        "next_action": None,
        "terminal_reason": None,
        "exception_gate": {"status": "inactive", "reason": None},
        "machine_checkpoints": {name: "pending" for name in CHECKPOINTS},
        "checkpoint_provenance": {name: None for name in CHECKPOINTS},
        "legacy_compatibility": {
            "mode": cfg["state_authority"]["legacy_mode"],
            "legacy_state_path": str(legacy_path.relative_to(repo_root.resolve())),
            "legacy_state_present": legacy_present,
            "legacy_state_sha256": legacy_sha,
        },
        "history": [
            {
                "from": None,
                "to": "ISSUE_INITIALIZED",
                "recorded_at": iso_utc(recorded_at),
                "repository_commit_sha": implementation_sha,
            }
        ],
    }
    state = refresh_state_control(state, cfg)
    errors = validate_state_semantics(repo_root, cfg, state)
    if errors:
        raise ValueError("generated Production State invalid: " + "; ".join(errors))
    return state


def verify_state_basis(
    repo_root: Path,
    cfg: dict[str, Any],
    state: dict[str, Any],
    implementation_sha: str,
) -> None:
    profile_path = repo_local_path(repo_root, state["profile"]["path"], "state.profile.path")
    if not profile_path.is_file():
        raise ValueError("production profile referenced by state does not exist")
    if sha256_file(profile_path) != state["profile"]["sha256"]:
        raise ValueError("production profile bytes changed after state initialization")
    profile = load_json(profile_path)
    profile_errors = validate_profile(profile, cfg)
    if profile_errors:
        raise ValueError("production profile no longer satisfies v2 contract: " + "; ".join(profile_errors))
    if profile.get("issue_id") != state.get("issue_id"):
        raise ValueError("production profile/state issue_id divergence")
    if profile.get("research_profile") != state.get("research_profile") or profile.get("publication_profile") != state.get("publication_profile"):
        raise ValueError("production profile/state Profile identity divergence")
    if profile.get("contract") != state.get("contract"):
        raise ValueError("production profile/state contract divergence")
    expected_contract = contract_identity(repo_root, cfg, state["research_profile"], state["publication_profile"])
    if expected_contract != state["contract"]:
        raise ValueError("current semantic contract files differ from state contract identity")
    if state["implementation"]["repository_commit_sha"] != implementation_sha:
        raise ValueError("implementation commit differs from authoritative state; explicit rebase/reinitialization is required")
    if state["implementation"]["orchestrator_version"] != cfg["orchestrator_version"]:
        raise ValueError("orchestrator version differs from authoritative state")
    legacy = state["legacy_compatibility"]
    legacy_path = repo_local_path(repo_root, legacy["legacy_state_path"], "legacy_state_path")
    actual_present = legacy_path.is_file()
    actual_sha = sha256_file(legacy_path) if actual_present else None
    if actual_present != legacy["legacy_state_present"] or actual_sha != legacy["legacy_state_sha256"]:
        raise ValueError("legacy compatibility artifact changed after v2 initialization; it cannot silently affect v2 state")
    semantic_errors = validate_state_semantics(repo_root, cfg, state)
    if semantic_errors:
        raise ValueError("Production State semantic inconsistency: " + "; ".join(semantic_errors))


def transition_state(
    repo_root: Path,
    cfg: dict[str, Any],
    state: dict[str, Any],
    to_state: str,
    implementation_sha: str,
    recorded_at: datetime,
    checkpoint_updates: dict[str, str] | None = None,
    checkpoint_provenance_updates: dict[str, dict[str, str]] | None = None,
) -> dict[str, Any]:
    verify_state_basis(repo_root, cfg, state, implementation_sha)
    if to_state not in LIFECYCLE:
        raise ValueError(f"unsupported lifecycle state: {to_state}")
    current = state["lifecycle_state"]
    current_index = LIFECYCLE.index(current)
    target_index = LIFECYCLE.index(to_state)
    if target_index != current_index + 1:
        raise ValueError(f"non-monotonic transition refused: {current} -> {to_state}; exactly one forward step is required")
    stage = cfg["orchestration"]["stage_plan"].get(current, {})
    required = set(stage.get("checkpoints", []))
    updates = checkpoint_updates or {}
    provenance_updates = checkpoint_provenance_updates or {}
    if set(updates) != required or any(value != "passed" for value in updates.values()):
        raise ValueError(f"transition {current} -> {to_state} requires exact passed checkpoint updates: {sorted(required)}")
    if set(provenance_updates) != required:
        raise ValueError(f"transition {current} -> {to_state} requires exact checkpoint provenance updates: {sorted(required)}")
    profile_path = repo_local_path(repo_root, state["profile"]["path"], "state.profile.path")
    profile = load_json(profile_path)
    for checkpoint in required:
        canonical = _checkpoint_attestation_path(repo_root, cfg, profile, checkpoint)
        authority_errors, _ = _validate_authority_ref(repo_root, provenance_updates[checkpoint], canonical, f"transition checkpoint {checkpoint}")
        if authority_errors:
            raise ValueError("invalid checkpoint provenance update: " + "; ".join(authority_errors))
    updated = deepcopy(state)
    for checkpoint in required:
        updated["machine_checkpoints"][checkpoint] = "passed"
        updated["checkpoint_provenance"][checkpoint] = deepcopy(provenance_updates[checkpoint])
    updated["lifecycle_state"] = to_state
    updated["history"].append(
        {
            "from": current,
            "to": to_state,
            "recorded_at": iso_utc(recorded_at),
            "repository_commit_sha": implementation_sha,
        }
    )
    updated = refresh_state_control(updated, cfg)
    errors = validate_state_semantics(repo_root, cfg, updated)
    if errors:
        raise ValueError("refusing inconsistent Production State transition: " + "; ".join(errors))
    return updated


def initialize(
    repo_root: Path,
    cfg: dict[str, Any],
    profile: dict[str, Any],
    implementation_sha: str,
    target_gate: str,
    recorded_at: datetime,
) -> tuple[Path, Path]:
    errors = validate_profile(profile, cfg)
    if errors:
        raise ValueError("invalid v2 Production Profile: " + "; ".join(errors))
    source_root = repo_local_path(repo_root, profile["paths"]["source_root"], "paths.source_root")
    profile_path = source_root / cfg["state_authority"]["profile_filename"]
    state_path = source_root / cfg["state_authority"]["authoritative_filename"]
    if profile_path.exists() or state_path.exists():
        raise ValueError(f"refusing destructive v2 initialization: {profile_path} or {state_path} already exists")
    source_root.mkdir(parents=True, exist_ok=True)
    write_json(profile_path, profile)
    state = initial_state(repo_root, cfg, profile, profile_path, implementation_sha, target_gate, recorded_at)
    write_json(state_path, state)
    return profile_path, state_path


def cmd_init_weekly(args: argparse.Namespace, repo_root: Path, cfg: dict[str, Any]) -> int:
    now = parse_instant(args.now) if args.now else datetime.now(timezone.utc)
    impl = repository_commit_sha(repo_root, args.implementation_sha)
    profile = weekly_profile(repo_root, cfg, now, args.issue_id)
    profile_path, state_path = initialize(repo_root, cfg, profile, impl, args.target_gate, now)
    print(json.dumps({"profile": str(profile_path.relative_to(repo_root)), "state": str(state_path.relative_to(repo_root))}, indent=2))
    return 0


def cmd_init_thematic(args: argparse.Namespace, repo_root: Path, cfg: dict[str, Any]) -> int:
    spec_path = Path(args.spec)
    if not spec_path.is_absolute():
        spec_path = repo_root / spec_path
    spec = load_json(spec_path)
    now = parse_instant(args.recorded_at) if args.recorded_at else datetime.now(timezone.utc)
    impl = repository_commit_sha(repo_root, args.implementation_sha)
    profile = thematic_profile(repo_root, cfg, spec)
    profile_path, state_path = initialize(repo_root, cfg, profile, impl, args.target_gate, now)
    print(json.dumps({"profile": str(profile_path.relative_to(repo_root)), "state": str(state_path.relative_to(repo_root))}, indent=2))
    return 0


def cmd_validate_profile(args: argparse.Namespace, repo_root: Path, cfg: dict[str, Any]) -> int:
    path = Path(args.profile)
    if not path.is_absolute():
        path = repo_root / path
    errors = validate_profile(load_json(path), cfg)
    print(json.dumps({"passed": not errors, "errors": errors}, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


def cmd_validate_state(args: argparse.Namespace, repo_root: Path, cfg: dict[str, Any]) -> int:
    path = Path(args.state)
    if not path.is_absolute():
        path = repo_root / path
    state = load_json(path)
    impl = repository_commit_sha(repo_root, args.implementation_sha or state.get("implementation", {}).get("repository_commit_sha"))
    try:
        verify_state_basis(repo_root, cfg, state, impl)
        errors: list[str] = []
    except ValueError as exc:
        errors = [str(exc)]
    print(json.dumps({"passed": not errors, "errors": errors}, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


def cmd_transition(args: argparse.Namespace, repo_root: Path, cfg: dict[str, Any]) -> int:
    state_path = Path(args.state)
    if not state_path.is_absolute():
        state_path = repo_root / state_path
    state = load_json(state_path)
    impl = repository_commit_sha(repo_root, args.implementation_sha)
    now = parse_instant(args.recorded_at) if args.recorded_at else datetime.now(timezone.utc)
    updates = {name: "passed" for name in args.checkpoint}
    provenance_updates: dict[str, dict[str, str]] = {}
    profile = load_json(repo_local_path(repo_root, state["profile"]["path"], "state.profile.path"))
    for name in args.checkpoint:
        attestation = _checkpoint_attestation_path(repo_root, cfg, profile, name)
        if not attestation.is_file():
            raise ValueError(f"checkpoint attestation missing: {name}")
        provenance_updates[name] = _authority_ref(repo_root, attestation)
    updated = transition_state(repo_root, cfg, state, args.to_state, impl, now, updates, provenance_updates)
    write_json(state_path, updated)
    print(state_path)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    sub = parser.add_subparsers(dest="command", required=True)

    weekly = sub.add_parser("init-weekly")
    weekly.add_argument("--now")
    weekly.add_argument("--issue-id")
    weekly.add_argument("--target-gate", choices=["ARCHITECTURE_REVIEW", "PUBLICATION_PREVIEW"], default="ARCHITECTURE_REVIEW")
    weekly.add_argument("--implementation-sha")

    thematic = sub.add_parser("init-thematic")
    thematic.add_argument("--spec", required=True)
    thematic.add_argument("--recorded-at")
    thematic.add_argument("--target-gate", choices=["ARCHITECTURE_REVIEW", "PUBLICATION_PREVIEW"], default="ARCHITECTURE_REVIEW")
    thematic.add_argument("--implementation-sha")

    validate_p = sub.add_parser("validate-profile")
    validate_p.add_argument("--profile", required=True)

    validate_s = sub.add_parser("validate-state")
    validate_s.add_argument("--state", required=True)
    validate_s.add_argument("--implementation-sha")

    transition = sub.add_parser("transition")
    transition.add_argument("--state", required=True)
    transition.add_argument("--to-state", choices=LIFECYCLE, required=True)
    transition.add_argument("--checkpoint", action="append", default=[])
    transition.add_argument("--recorded-at")
    transition.add_argument("--implementation-sha")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    repo_root = Path(args.repo_root).resolve()
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = repo_root / config_path
    try:
        cfg = load_json(config_path)
        if args.command == "init-weekly":
            return cmd_init_weekly(args, repo_root, cfg)
        if args.command == "init-thematic":
            return cmd_init_thematic(args, repo_root, cfg)
        if args.command == "validate-profile":
            return cmd_validate_profile(args, repo_root, cfg)
        if args.command == "validate-state":
            return cmd_validate_state(args, repo_root, cfg)
        if args.command == "transition":
            return cmd_transition(args, repo_root, cfg)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
