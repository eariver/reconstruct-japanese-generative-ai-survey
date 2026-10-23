#!/usr/bin/env python3
"""Common fail-closed JSON Schema conformance for Survey Production Core v2.

Model/external artifacts must pass this layer before a semantic validator may
accept them as Production State authority. Semantic validators remain necessary:
JSON Schema proves structural conformance, not editorial/provenance correctness.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    import jsonschema
except ImportError as exc:  # fail closed rather than silently skipping schema validation
    raise RuntimeError(
        "Survey Production Core v2 requires jsonschema; install config/survey-production-v2-requirements.txt"
    ) from exc


class SchemaConformanceError(ValueError):
    """Raised when an artifact fails its declared JSON Schema."""


def _format_path(parts: list[Any]) -> str:
    if not parts:
        return "$"
    value = "$"
    for part in parts:
        if isinstance(part, int):
            value += f"[{part}]"
        else:
            value += f".{part}"
    return value


def load_schema(schema_path: Path) -> dict[str, Any]:
    if schema_path.is_symlink() or not schema_path.is_file():
        raise SchemaConformanceError(f"schema path is missing or unsafe: {schema_path}")
    try:
        value = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SchemaConformanceError(f"cannot load schema {schema_path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SchemaConformanceError(f"schema must be a JSON object: {schema_path}")
    try:
        jsonschema.Draft202012Validator.check_schema(value)
    except jsonschema.exceptions.SchemaError as exc:
        raise SchemaConformanceError(f"invalid JSON Schema {schema_path}: {exc.message}") from exc
    return value


def validate_instance(instance: Any, schema_path: Path, *, label: str = "artifact") -> None:
    """Fail closed if *instance* does not conform to *schema_path*.

    Errors are deterministically sorted by JSON path so CI and production logs
    identify the first stable structural defect without depending on dict order.
    """

    schema = load_schema(schema_path)
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    errors = sorted(validator.iter_errors(instance), key=lambda err: (list(err.absolute_path), err.message))
    if errors:
        first = errors[0]
        location = _format_path(list(first.absolute_path))
        raise SchemaConformanceError(f"{label} fails {schema_path}: {location}: {first.message}")


def load_and_validate_json(path: Path, schema_path: Path, *, label: str = "artifact") -> dict[str, Any]:
    if path.is_symlink() or not path.is_file():
        raise SchemaConformanceError(f"{label} path is missing or unsafe: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SchemaConformanceError(f"cannot load {label} {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SchemaConformanceError(f"{label} must be a JSON object: {path}")
    validate_instance(value, schema_path, label=label)
    return value
