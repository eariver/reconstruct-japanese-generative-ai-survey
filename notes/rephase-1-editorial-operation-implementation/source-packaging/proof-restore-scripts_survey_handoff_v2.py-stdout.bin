#!/usr/bin/env python3
"""Build canonical exact-byte Stage Handoffs for Survey Production Core v2.

The builder never discovers a "latest" run. Callers must name every input and
output artifact explicitly. The builder derives only semantic authority from the
current Production State/Profile/contract and verifies that outputs exactly match
the configured stage contract before writing the canonical handoff.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from scripts import survey_handlers_v2 as handlers
from scripts import survey_production_v2 as core
from scripts import survey_schema_v2 as schema_gate

REQUEST_SCHEMA = Path("schemas/stage-handoff-request-v2.schema.json")


def _rel(repo_root: Path, path: Path, label: str) -> str:
    root = repo_root.resolve()
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(root))
    except ValueError as exc:
        raise ValueError(f"{label} must be repository-local: {path}") from exc


def _file_ref(repo_root: Path, name: str, path: Path) -> dict[str, str]:
    rel = _rel(repo_root, path, name)
    resolved = core.repo_local_path(repo_root, rel, name)
    if resolved.is_symlink() or not resolved.is_file():
        raise ValueError(f"{name} missing or unsafe: {rel}")
    return {"name": name, "path": rel, "sha256": core.sha256_file(resolved)}


def _expand(template: str, profile: dict[str, Any]) -> str:
    value = template.replace("{source_root}", profile["paths"]["source_root"])
    if "{" in value or "}" in value:
        raise ValueError(f"unsupported stage artifact template: {template}")
    return value


def expected_output_contract(cfg: dict[str, Any], state: dict[str, Any], profile: dict[str, Any]) -> dict[str, dict[str, Any]]:
    stage = cfg["orchestration"]["stage_plan"].get(state["lifecycle_state"])
    if not isinstance(stage, dict):
        raise ValueError(f"no executable stage for lifecycle {state['lifecycle_state']}")
    rows: dict[str, dict[str, Any]] = {}
    for checkpoint in stage.get("checkpoints", []):
        if checkpoint in rows:
            raise ValueError(f"duplicate stage output name: {checkpoint}")
        rows[checkpoint] = {"checkpoint": checkpoint, "path": None}
    for artifact in stage.get("artifacts", []):
        name = artifact["name"]
        if name in rows:
            raise ValueError(f"duplicate stage output name: {name}")
        rows[name] = {"checkpoint": None, "path": _expand(artifact["path"], profile)}
    return rows


def build_handoff(
    repo_root: Path,
    cfg: dict[str, Any],
    state_path: Path,
    inputs: dict[str, Path],
    outputs: dict[str, Path],
    *,
    output_path: Path | None = None,
) -> Path:
    state = core.load_json(state_path)
    pinned = state["implementation"]["repository_commit_sha"]
    core.verify_state_basis(repo_root, cfg, state, pinned)
    profile_path = core.repo_local_path(repo_root, state["profile"]["path"], "state.profile.path")
    profile = core.load_json(profile_path)
    stage = cfg["orchestration"]["stage_plan"].get(state["lifecycle_state"])
    if not isinstance(stage, dict) or stage.get("handoff_required") is not True:
        raise ValueError(f"lifecycle does not require a production Stage Handoff: {state['lifecycle_state']}")
    handler = stage.get("handler")
    if not isinstance(handler, str) or not handler:
        raise ValueError("stage handler identity missing")

    if not inputs or len(inputs) != len(set(inputs)):
        raise ValueError("Stage Handoff requires uniquely named explicit inputs")
    input_rows = [_file_ref(repo_root, name, path) for name, path in sorted(inputs.items())]

    expected = expected_output_contract(cfg, state, profile)
    if set(outputs) != set(expected):
        raise ValueError(
            f"Stage Handoff outputs must exactly match stage contract: expected={sorted(expected)} actual={sorted(outputs)}"
        )
    output_rows: list[dict[str, Any]] = []
    for name in sorted(outputs):
        ref = _file_ref(repo_root, name, outputs[name])
        contract = expected[name]
        if contract["path"] is not None and ref["path"] != contract["path"]:
            raise ValueError(f"configured artifact output must use canonical path for {name}: {contract['path']}")
        output_rows.append({**ref, "checkpoint": contract["checkpoint"]})

    payload = {
        "schema_version": "2.0-rc1",
        "issue_id": state["issue_id"],
        "lifecycle_state": state["lifecycle_state"],
        "handler": handler,
        "basis": {
            "production_state_sha256": core.sha256_file(state_path),
            "production_profile_sha256": core.sha256_file(profile_path),
            "pipeline_contract_sha256": state["contract"]["pipeline_contract_sha256"],
            "quality_contract_sha256": state["contract"]["quality_contract_sha256"],
            "implementation_commit_sha": pinned,
        },
        "inputs": input_rows,
        "outputs": output_rows,
    }
    schema_gate.validate_instance(payload, repo_root / handlers.HANDOFF_SCHEMA, label="Stage Handoff")
    canonical = handlers.canonical_handoff_path(repo_root, state)
    target = output_path.resolve() if output_path is not None else canonical.resolve()
    if target != canonical.resolve():
        raise ValueError(f"Stage Handoff must use canonical path: {_rel(repo_root, canonical, 'Stage Handoff')}")
    if target.exists():
        if core.load_json(target) != payload:
            raise ValueError(f"refusing to overwrite divergent Stage Handoff: {target}")
        return target
    core.write_json(target, payload)
    return target


def canonical_request_path(repo_root: Path, state: dict[str, Any]) -> Path:
    profile = core.load_json(core.repo_local_path(repo_root, state["profile"]["path"], "state.profile.path"))
    source_root = core.repo_local_path(repo_root, profile["paths"]["source_root"], "paths.source_root")
    return source_root / "orchestration" / "v2" / "handoff-requests" / f"{state['lifecycle_state']}.json"


def _paths_from_request(repo_root: Path, rows: Any, label: str) -> dict[str, Path]:
    if not isinstance(rows, list):
        raise ValueError(f"{label} must be an array")
    result: dict[str, Path] = {}
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != {"name", "path"}:
            raise ValueError(f"{label}[{index}] fields invalid")
        name = row.get("name")
        path = row.get("path")
        if not isinstance(name, str) or not name or name in result or not isinstance(path, str) or not path:
            raise ValueError(f"{label}[{index}] name/path invalid or duplicated")
        resolved = core.repo_local_path(repo_root, path, f"{label} {name}")
        result[name] = resolved
    return result


def build_handoff_from_request(
    repo_root: Path,
    cfg: dict[str, Any],
    state_path: Path,
    request_path: Path,
) -> Path:
    state = core.load_json(state_path)
    canonical = canonical_request_path(repo_root, state)
    if request_path.resolve() != canonical.resolve():
        raise ValueError(f"Stage Handoff Request must use canonical path: {_rel(repo_root, canonical, 'Stage Handoff Request')}")
    request = schema_gate.load_and_validate_json(
        request_path, repo_root / REQUEST_SCHEMA, label="Stage Handoff Request"
    )
    if request["issue_id"] != state["issue_id"] or request["lifecycle_state"] != state["lifecycle_state"]:
        raise ValueError("Stage Handoff Request identity does not match current Production State")
    return build_handoff(
        repo_root,
        cfg,
        state_path,
        _paths_from_request(repo_root, request["inputs"], "Stage Handoff Request inputs"),
        _paths_from_request(repo_root, request["outputs"], "Stage Handoff Request outputs"),
    )


def _parse_named_path(values: list[str], label: str) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"{label} must use NAME=PATH")
        name, raw_path = value.split("=", 1)
        if not name or not raw_path or name in result:
            raise ValueError(f"{label} names/paths must be unique and non-empty")
        result[name] = Path(raw_path)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--state", required=True)
    parser.add_argument("--request", help="Canonical Stage Handoff Request; mutually exclusive with explicit --input/--output")
    parser.add_argument("--input", action="append", default=[], help="NAME=PATH; explicit, repeatable")
    parser.add_argument("--output", action="append", default=[], help="NAME=PATH; explicit, repeatable")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    try:
        cfg = core.load_json(root / core.DEFAULT_CONFIG)
        state_path = (root / args.state).resolve()
        if args.request:
            if args.input or args.output:
                raise ValueError("--request may not be combined with --input/--output")
            path = build_handoff_from_request(root, cfg, state_path, (root / args.request).resolve())
        else:
            path = build_handoff(
                root,
                cfg,
                state_path,
                {name: (root / path).resolve() for name, path in _parse_named_path(args.input, "--input").items()},
                {name: (root / path).resolve() for name, path in _parse_named_path(args.output, "--output").items()},
            )
        print(_rel(root, path, "Stage Handoff"))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
