#!/usr/bin/env python3
"""Source-only LONGFORM_GENERATED_V1 reader-input derivation (THEMATIC four-family lineage v1).

LF-1 input-only component. This module projects already-validated accepted
authorities plus publication-authored input into the complete reader object
validated by ``schemas/longform-reader-input-v2.schema.json``. It:

- reads State/Profile/checkpoint-bound Architecture, Draft Package/Result,
  Profile Synthesis, Evidence acceptance/cards, Candidate Matrix, Materiality
  Ledger and Discovery acceptance through the existing real loaders;
- writes NOTHING (no reader file, no main.tex/references.bib/jgaisurvey.sty,
  no Gate, no receipt, no PASS, no lifecycle/state mutation);
- never imports or invokes the legacy publication writer
  (``run_semantic_publication_v2_interactive{,_base}``) or any renderer;
- exposes no CLI (importable functions only).

Directive rule: if the legacy ``editorial/post-architecture-directives-v2.json``
entry exists under the edition source root (regular file, symlink, or dangling
symlink), loading refuses with an unsupported-directive-authority diagnostic
BEFORE projection and never reads that file as authority. A clean new synthetic
initial chain carries no such entry. This refusal is not silent ignoring: the
legacy publisher check and its manifest hash remain unresolved LF-2 scope.

Token grammar (narrow supported subset for the initial route):
- ``package_id``: ``^[A-Za-z0-9][A-Za-z0-9._-]*$`` (Architecture-bound). Refused
  otherwise. Suffix for the visible kicker is ``package_id.rsplit("-", 1)[-1]``
  with ``_`` mapped to space; an empty suffix refuses. The full kicker string
  already contains ``ordinal/total``, so no cross-package kicker-collision rule
  is applied beyond suffix validity.
- Discovery ID: ``^[A-Za-z0-9._-]+-D\\d{3,}$``. Bibliography key is
  ``"sp001" + did.lower().replace("-", "")`` (dots preserved, dashes dropped);
  key grammar is ``^[A-Za-z][A-Za-z0-9:._-]*$``. A key collision across the cited
  set refuses explicitly (lower/dash folding can collide).
- URL subset (finite, explicit): ``str``, no leading/trailing whitespace, ASCII
  only, scheme exactly ``http``/``https`` with a non-empty host, and NONE of:
  whitespace, C0/C1 controls, DEL, ``{ } \\ % # ^ ~ " < > | ` ``.
  Deliberate exclusions (refused, never transformed): percent-encoded URLs (any
  ``%``), fragments (any ``#``), non-ASCII IRI, userinfo tricks are NOT specially
  handled beyond the reject set. If a legitimate accepted canonical URL falls
  outside this subset, return the exact unsupported-URL issue for policy review;
  do NOT invent a universal TeX-safety parser here. Real ``\\url{}``/BibLaTeX
  emission safety is LF-2 serializer scope. The exact accepted URL is validated
  before any display trimming; surrounding whitespace refuses, never normalizes.

Reader-text obligation: every projected string passes the existing read-only
``survey_reader_surface_gate_v2.scan_reader_text_lines`` BLOCKING/UNRESOLVED
refusal plus the preserved forbidden-pattern/Verify/DID/TeX-inclusion checks.
The scanner module is read-only (no writer import/invocation).

Authoring envelope: ``runner``/``review_reference`` are non-reader mechanical
metadata. Profile defines THEMATIC/LONGFORM_SPECIAL. Both fields must be
non-empty strings but any non-empty value projects identically; legitimate
runner-only or review-reference-only changes retain reader bytes while the
authored binding hash changes. Reader schema carries no provenance/runner.

Accepted-source subset (first proof): accepted container/card integrity is
validated globally (duplicate DID, card SHA, single-DID per card, Matrix/
Materiality/Discovery authority mismatch, Discovery membership, card presence).
LF-1 bibliography eligibility (unique primary-subject entity, exact URL, card-only
``explicit_source_id=None`` provenance, VERIFIED/PARTIAL, non-HOLD) applies only
to the selected/authorized subset (union of Draft-Package-assigned DIDs after
full accepted validation). Unselected HOLD/ambiguous rows are preserved without
promotion and never block a healthy selected projection; citing held-back or
missing Evidence refuses at projection/bibliography. Archive packages must cover
Architecture exactly once each (no extra/duplicate/missing) and spec blocks must
cover Result non-CLAIM_BOUNDARY blocks exactly once each; EVERY assigned DID is
validated through accepted Draft-Package ``citation_refs.refs`` exact-one
semantics so no extra archive block can introduce another package's DID.
Card filenames are validated as contained relative paths before any read, and
the accepted Evidence run tree (package.json/tasks/results, including aliased
directories and symlinked children) is preflighted before the accepted-Evidence
loader reads it; exact-set authority remains that real loader's.
No sidecar ``sources``/``source_bindings`` fallback.
"""
from __future__ import annotations

import copy
import os
import re
import urllib.parse
from pathlib import Path
from typing import Any

from scripts import survey_agent_control_v2 as agent
from scripts import survey_agent_tool_v2 as runtime_tool
from scripts import survey_bibliography_access_provenance_v2 as provenance
from scripts import survey_drafting_citation_refs_v2 as citation_refs
from scripts import survey_drafting_v2 as drafting
from scripts import survey_evidence_v2 as evidence
from scripts import survey_production_v2 as core
from scripts import survey_reader_surface_gate_v2 as surface_gate
from scripts import survey_schema_v2 as schema_gate


READER_INPUT_SCHEMA = Path("schemas/longform-reader-input-v2.schema.json")
ROUTE = "LONGFORM_GENERATED_V1"
FORMAT = "THEMATIC_FOUR_FAMILY_LINEAGE_V1"
REQUIRED_LIFECYCLE = "DRAFT_COMPLETE"
REQUIRED_ACTION = "stage:reader-publication-validation"
# Authoring envelope runner metadata is non-authoritative. Profile defines the
# THEMATIC/LONGFORM_SPECIAL route. Authored runner must be a non-empty string
# (modest envelope/type policy) but any non-empty value projects identically;
# runner/review-reference changes retain reader bytes while authored hash changes.
DIRECTIVE_REL = "editorial/post-architecture-directives-v2.json"

FIXED_TITLE = "Japanese Generative AI Technical Survey Special"
FIXED_EDITION = "Thematic Longform Special"
FIXED_FINAL_HEADING = "この号の総括"
FINAL_PLACEMENT = "END_OF_PUBLICATION_BEFORE_REFERENCES_OR_END_MATTER"
FIXED_TOC_TITLE = "目次"

VISIBLE_TEXT: dict[str, Any] = {
    "frontmatter_boundary": "Scope / attribution boundary",
    "claim_boundary": "Claim boundary",
    "theme_overview_title": "Theme at a glance",
    "timeline_heading": "Transition timeline",
    "technical_notes_heading": "Source-backed Technical Notes",
    "note_chronology_label": "Chronology:",
    "note_points_label": "Technical points:",
    "note_limitation_label": "Limitation / attribution:",
    "note_url_label": "Primary URL:",
    "cross_family_kicker": "CROSS-FAMILY SYNTHESIS",
    "cross_comparison_title": "Cross-family comparison",
    "cross_table_header": ["観点", "GLM", "Qwen", "DeepSeek", "Kimi"],
    "issue_summary_kicker": "ISSUE SYNTHESIS",
    "references_title": "References / Source Notes",
    "edition_descriptor": FIXED_EDITION,
    "toc_title": FIXED_TOC_TITLE,
    "cover_cutoff_label": "Editorial cutoff",
    "cover_repository_label": "Repository",
    "cover_build_label": "Build",
    "repository_value": "eariver/japanese-generative-ai-survey",
    "build_value": "LuaLaTeX / jlreq / LuaTeX-ja",
    "strapline": "一次情報・論文・OSS・X上の技術反応を分離し、検証可能なEvidence chainとして編成する",
    "date_history_prefix": "Thematic history / as of ",
    "date_boundary_prefix": "As-of boundary: ",
}

FORBIDDEN_READER_PATTERNS = (
    "Core v2 Evidence:",
    "materiality:",
    "Selection済みEvidence",
    "normalized claim",
    "Source-bound record",
    "This retained evidence note",
    "The bound ",
    "Evidence pass",
    "本Evidence",
)

_GIT_OVERRIDE_VARS = (
    "GIT_DIR",
    "GIT_WORK_TREE",
    "GIT_INDEX_FILE",
    "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_COMMON_DIR",
)

_DISCOVERY_ID = re.compile(r"^[A-Za-z0-9._-]+-D\d{3,}$")
_PACKAGE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
# Citation key preserves DID dots (DID subset allows '.'), drops '-', lowercases,
# prefixed with sp001. Grammar therefore allows '.' alongside alnum/_/:/-.
_CITATION_KEY = re.compile(r"^[A-Za-z][A-Za-z0-9:._-]*$")
_URL_EXCLUDED = set("{} \\%#^~\"<>|`")
_ISSUE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def _rel(root: Path, path: Path) -> str:
    return str(path.resolve().relative_to(root.resolve())).replace("\\", "/")


def _safe(root: Path, raw: str | Path, label: str) -> Path:
    import os as _os

    root_resolved = root.resolve()
    lexical = Path(raw) if Path(raw).is_absolute() else (root_resolved / Path(raw))
    try:
        lexical.relative_to(root_resolved)
    except ValueError:
        raise ValueError(f"{label} escapes repository: {raw}")
    for part in lexical.relative_to(root_resolved).parts:
        if part in ("..", ".", ""):
            raise ValueError(f"{label} has unsafe path component: {part}")
    try:
        rel_parent = lexical.parent.relative_to(root_resolved)
    except ValueError:
        raise ValueError(f"{label} escapes repository: {raw}")
    current = root_resolved
    for part in rel_parent.parts:
        if part in ("..", ".", ""):
            raise ValueError(f"{label} has unsafe path component: {part}")
        current = current / part
        if current.is_symlink():
            raise ValueError(f"{label} has symlinked ancestor component: {current}")
    if _os.path.islink(lexical):
        raise ValueError(f"{label} leaf alias is unsafe: {raw}")
    resolved = lexical.resolve()
    try:
        resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise ValueError(f"{label} escapes repository: {raw}") from exc
    if resolved.is_symlink() or not resolved.is_file():
        raise ValueError(f"{label} missing or unsafe: {raw}")
    return resolved


def _artifact(root: Path, name: str, path: Path) -> dict[str, str]:
    safe = _safe(root, path, name)
    return {"name": name, "path": _rel(root, safe), "sha256": core.sha256_file(safe)}


def _nonempty(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value.strip()


def _reader_text(value: Any, label: str) -> str:
    text = _nonempty(value, label)
    # Actual read-only scanner obligation (not the writer). Any BLOCKING/
    # UNRESOLVED lexical finding refuses before the preserved local checks.
    findings = surface_gate.scan_reader_text_lines([text], label, "longform-revision")
    blocking = [f for f in findings if f.severity == "BLOCKING" and f.disposition == "UNRESOLVED"]
    if blocking:
        raise ValueError(f"{label} leaks production metadata: {blocking[0].text_span}")
    lowered = text.lower()
    for pattern in FORBIDDEN_READER_PATTERNS:
        if pattern.lower() in lowered:
            raise ValueError(f"{label} leaks production metadata: {pattern}")
    if re.search(r"\bVerify\b", text):
        raise ValueError(f"{label} leaks an internal verification obligation")
    if re.search(r"\b[A-Za-z0-9._-]+-D\d{3,}\b", text):
        raise ValueError(f"{label} exposes a repository Discovery/Evidence identifier")
    if re.search(r"\\(?:input|include)(?![A-Za-z@])", text):
        raise ValueError(f"{label} carries an unsupported TeX inclusion primitive")
    return text


def _did(value: Any, label: str) -> str:
    if not isinstance(value, str) or not _DISCOVERY_ID.fullmatch(value):
        raise ValueError(f"{label} is not a supported Discovery ID: {value!r}")
    return value


def _ids(value: Any, label: str, allowed: set[str]) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{label} must contain one or more Discovery IDs")
    out: list[str] = []
    for raw in value:
        did = _did(raw, label)
        if did not in allowed:
            raise ValueError(f"{label} cites Evidence outside the approved package: {did}")
        if did not in out:
            out.append(did)
    return out


def _validate_paragraph_rows(rows: Any, label: str, allowed: set[str]) -> list[dict[str, Any]]:
    if not isinstance(rows, list) or not rows:
        raise ValueError(f"{label} must be a non-empty list")
    out = []
    for idx, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != {"text", "discovery_ids"}:
            raise ValueError(f"{label}[{idx}] has an invalid envelope")
        out.append({
            "text": _reader_text(row["text"], f"{label}[{idx}].text"),
            "discovery_ids": _ids(row["discovery_ids"], f"{label}[{idx}].discovery_ids", allowed),
        })
    return out


def _kicker(package_id: str, ordinal: int, total: int) -> str:
    if not _PACKAGE_ID.fullmatch(package_id):
        raise ValueError(f"package_id outside the supported token subset: {package_id!r}")
    suffix = package_id.rsplit("-", 1)[-1].replace("_", " ").strip()
    if not suffix:
        raise ValueError(f"package_id yields an empty kicker suffix: {package_id!r}")
    return f"THEMATIC LINEAGE {ordinal}/{total} — {suffix}"


def _bib_key(did: str) -> str:
    key = "sp001" + did.lower().replace("-", "")
    if not _CITATION_KEY.fullmatch(key):
        raise ValueError(f"Discovery ID yields an unsafe citation key: {did!r}")
    return key


def _check_url(url: Any, label: str) -> str:
    if not isinstance(url, str) or not url:
        raise ValueError(f"{label} must be a non-empty URL string")
    if url.strip() != url:
        raise ValueError(f"{label} has surrounding whitespace: {url!r}")
    try:
        url.encode("ascii")
    except UnicodeEncodeError:
        raise ValueError(f"{label} is outside the ASCII URL subset (IRI excluded): {url!r}")
    for char in url:
        if ord(char) < 32 or ord(char) == 127:
            raise ValueError(f"{label} contains a control character: {url!r}")
        if char in _URL_EXCLUDED or char.isspace():
            raise ValueError(f"{label} contains an excluded delimiter {char!r}: {url!r}")
    try:
        parts = urllib.parse.urlsplit(url)
    except ValueError as exc:
        raise ValueError(f"{label} is not a parseable URL: {url!r}") from exc
    if parts.scheme not in ("http", "https") or not parts.hostname:
        raise ValueError(f"{label} must be an HTTP(S) URL with a host: {url!r}")
    return url


def _resolve_primary_entity(card: dict[str, Any], did: str) -> dict[str, str]:
    entities = card.get("entities")
    if not isinstance(entities, list) or not entities:
        raise ValueError(f"cited Discovery ID {did} card carries no entities")
    artifact = card.get("artifact")
    if not isinstance(artifact, dict):
        raise ValueError(f"cited Discovery ID {did} card lacks an artifact authority")
    primary = artifact.get("primary_subject_id")
    matches = [row for row in entities if isinstance(row, dict) and row.get("entity_id") == primary]
    if not isinstance(primary, str) or not primary or len(matches) != 1:
        raise ValueError(
            f"cited Discovery ID {did} has no unique primary-subject entity: {primary!r}"
        )
    entity = matches[0]
    title = entity.get("canonical_name")
    if not isinstance(title, str) or not title.strip():
        raise ValueError(f"cited Discovery ID {did} primary entity lacks a canonical name")
    raw_url = entity.get("canonical_url")
    if not isinstance(raw_url, str) or not raw_url.strip():
        raise ValueError(f"cited Discovery ID {did} primary entity lacks a canonical URL")
    # Exact accepted URL is validated BEFORE any display trimming. Surrounding
    # whitespace or excluded delimiters refuse; never silently normalize.
    checked_url = _check_url(raw_url, f"accepted entity canonical URL for {did}")
    organization = entity.get("organization")
    if organization is None or (isinstance(organization, str) and not organization.strip()):
        author = "Unknown"
    elif isinstance(organization, str):
        author = organization.strip()
    else:
        raise ValueError(f"cited Discovery ID {did} primary entity organization invalid")
    return {"title": title.strip(), "url": checked_url, "author": author}


def _safe_card_path(root: Path, acceptance_path: Path, filename: Any, label: str) -> Path:
    # Contained relative card filename must be validated BEFORE any read.
    # Only a plain basename under the acceptance results directory is accepted.
    if not isinstance(filename, str) or not filename:
        raise ValueError(f"{label} card filename must be a non-empty string: {filename!r}")
    if "/" in filename or "\\" in filename or filename in (".", ".."):
        raise ValueError(f"{label} card filename escapes results directory: {filename!r}")
    candidate = Path(filename)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError(f"{label} card filename escapes results directory: {filename!r}")
    base_resolved = (acceptance_path.parent / "results").resolve()
    # _safe enforces repository containment, symlink ancestors, regular file.
    safe = _safe(root, acceptance_path.parent / "results" / filename, label)
    try:
        safe.relative_to(base_resolved)
    except ValueError as exc:
        raise ValueError(f"{label} card path escapes results directory: {filename!r}") from exc
    return safe


def _preflight_evidence_tree(root: Path, acceptance_path: Path) -> Path:
    # Local alias preflight BEFORE the accepted-Evidence loader reads anything.
    # The existing validator rejects symlinked CHILDREN inside tasks/results but
    # `Path.is_dir()`/`is_file()` follow a symlinked DIRECTORY/FILE itself, so
    # an aliased results/tasks directory or package.json would be read through.
    # Refuse directory/file aliases, non-regular entries and symlinked children
    # here (stat-only, no content reads); exact-set authority remains the real
    # validator's, which is still called after this preflight.
    safe_acceptance = _safe(root, acceptance_path, "Evidence acceptance")
    run_dir = safe_acceptance.parent
    root_resolved = root.resolve()
    try:
        run_dir.relative_to(root_resolved)
    except ValueError as exc:
        raise ValueError(
            f"accepted Evidence run directory escapes repository: {acceptance_path}"
        ) from exc
    if run_dir.is_symlink() or not run_dir.is_dir():
        raise ValueError("accepted Evidence run directory is missing or unsafe")
    for rel, kind in (("package.json", "file"), ("tasks", "dir"), ("results", "dir")):
        candidate = run_dir / rel
        current = root_resolved
        try:
            reminder = candidate.relative_to(root_resolved)
        except ValueError as exc:
            raise ValueError(
                f"accepted Evidence {rel} escapes repository: {candidate}"
            ) from exc
        for part in reminder.parts[:-1]:
            if part in ("..", ".", ""):
                raise ValueError(f"accepted Evidence {rel} has unsafe path component: {part}")
            current = current / part
            if current.is_symlink():
                raise ValueError(
                    f"accepted Evidence {rel} has symlinked ancestor component: {current}"
                )
        if candidate.is_symlink():
            raise ValueError(f"accepted Evidence {rel} is an alias/symlink, refusing before read")
        if kind == "file":
            if not candidate.is_file():
                raise ValueError(f"accepted Evidence {rel} is missing or not a regular file")
        elif not candidate.is_dir():
            raise ValueError(f"accepted Evidence {rel} is missing or not a directory")
    for sub in ("tasks", "results"):
        for child in sorted((run_dir / sub).iterdir()):
            if child.is_symlink():
                raise ValueError(
                    f"accepted Evidence {sub} may not contain symlinks: {child.name}"
                )
            if not child.is_file():
                raise ValueError(
                    f"accepted Evidence {sub} may contain files only: {child.name}"
                )
    return safe_acceptance


def _longform_records(
    root: Path,
    matrix_path: Path,
    ledger_path: Path,
    discovery_path: Path,
    acceptance_path: Path,
    implementation_sha: str,
    selected_ids: set[str],
) -> tuple[dict[str, dict[str, str]], list[dict[str, str]]]:
    # Alias preflight runs before ANY accepted-tree content read below.
    acceptance_path = _preflight_evidence_tree(root, acceptance_path)
    matrix = core.load_json(matrix_path)
    ledger = core.load_json(ledger_path)
    discovery = core.load_json(discovery_path)
    if matrix.get("basis", {}).get("evidence_acceptance_sha256") != core.sha256_file(acceptance_path):
        raise ValueError("Candidate Matrix does not bind checkpoint Evidence acceptance")
    if matrix.get("basis", {}).get("materiality_ledger_sha256") != core.sha256_file(ledger_path):
        raise ValueError("Candidate Matrix materiality authority drifted")
    # Stage-advanced revalidation uses the production historical-basis mechanism
    # (same override context as the Weekly accepted-source loader).
    with runtime_tool.current_stage_basis_override():
        acceptance, _package = evidence.validate_evidence_acceptance(root, acceptance_path, implementation_sha)
    accepted_status: dict[str, str] = {}
    for row in acceptance.get("results", []):
        for item in row.get("discovery_ids", []):
            if item in accepted_status:
                raise ValueError(f"Discovery ID appears more than once in Evidence acceptance: {item}")
            accepted_status[item] = row["status"]
    materiality = {row["discovery_id"]: row["downstream_disposition"] for row in ledger.get("rows", [])}
    discovery_rows = {row["discovery_id"]: row for row in discovery.get("records", [])}
    card_sources: dict[str, dict[str, Any]] = {}
    card_refs: list[dict[str, str]] = []
    for row in acceptance["results"]:
        # Pre-read containment: filename is validated before SHA/read.
        card_path = _safe_card_path(root, acceptance_path, row.get("filename"), "accepted Evidence card")
        if core.sha256_file(card_path) != row["sha256"]:
            raise ValueError(f"accepted Evidence card SHA drift: {row['evidence_task_id']}")
        card = core.load_json(card_path)
        sources = card.get("sources")
        if not isinstance(sources, list) or not sources:
            raise ValueError(f"accepted Evidence card has no sources: {row['evidence_task_id']}")
        if not isinstance(row.get("discovery_ids"), list) or len(row["discovery_ids"]) != 1:
            raise ValueError(
                f"first-subset mapping requires a single DID per accepted card row: {row['evidence_task_id']}"
            )
        card_refs.append(_artifact(root, f"evidence-card:{row['evidence_task_id']}", card_path))
        for item in row["discovery_ids"]:
            if item in card_sources:
                raise ValueError(f"Discovery ID appears in multiple accepted Evidence cards: {item}")
            card_sources[item] = {"sources": sources, "card": card}
    # Global container/card integrity for EVERY Matrix row (authority bindings),
    # then selected-only LF-1 bibliography eligibility. Unselected HOLD/ambiguous
    # rows are preserved without promotion: they never block a healthy selected
    # projection and are absent from records so later citation refuses.
    seen_matrix: set[str] = set()
    for row in matrix.get("rows", []):
        for item in row.get("discovery_ids", []):
            if item in seen_matrix:
                raise ValueError(f"Candidate Matrix duplicates Discovery ID: {item}")
            seen_matrix.add(item)
            if accepted_status.get(item) != row.get("evidence_status"):
                raise ValueError(f"Evidence status authority mismatch for {item}")
            if materiality.get(item) != row.get("materiality"):
                raise ValueError(f"Materiality authority mismatch for {item}")
            if item not in discovery_rows:
                raise ValueError(f"Candidate Matrix Discovery ID missing from accepted Discovery: {item}")
            if item not in card_sources:
                raise ValueError(f"cited Discovery ID {item} has no acceptance-bound Evidence card")
    records: dict[str, dict[str, str]] = {}
    for row in matrix.get("rows", []):
        for item in row.get("discovery_ids", []):
            if item not in selected_ids:
                continue
            entry = card_sources[item]
            # _resolve_primary_entity validates the exact accepted URL before trim.
            entity = _resolve_primary_entity(entry["card"], item)
            target_url = entity["url"]
            resolved = provenance.resolve_source_access_provenance(
                entry["sources"], target_url, item, explicit_source_id=None
            )
            status = row["evidence_status"]
            if status not in ("VERIFIED", "PARTIAL"):
                raise ValueError(f"publication cannot cite {status} Evidence as factual support: {item}")
            if row.get("materiality") in ("HOLD", "NEEDS_MORE"):
                raise ValueError(f"publication cannot cite held-back materiality: {item}")
            if item in records:
                raise ValueError(f"Candidate Matrix duplicates Discovery ID: {item}")
            records[item] = {
                "title": entity["title"],
                "author": entity["author"],
                "url": target_url,
                "source_accessed_at": resolved["source_accessed_at"],
                "urldate": resolved["urldate"],
                "status": status,
                "materiality": str(row.get("materiality")),
            }
    missing = sorted(selected_ids - set(records))
    if missing:
        raise ValueError(f"selected Evidence has no eligible accepted record: {missing}")
    return records, card_refs


def _assigned_ids(spec: dict[str, Any]) -> list[str]:
    ids = list(spec.get("deck_discovery_ids", []))
    for block in spec.get("blocks", []):
        ids.extend(block.get("discovery_ids", []))
    return list(dict.fromkeys(ids))


def _validate_archive_authorization(
    architecture: dict[str, Any],
    archive: dict[str, Any],
    ordered: list[dict[str, Any]],
) -> None:
    # Exact unique archive package coverage: archive must contain exactly one row
    # per approved Architecture package, no extra/duplicate/missing.
    arch_packages = architecture.get("packages", [])
    arch_ids = [row.get("package_id") for row in arch_packages]
    if not isinstance(arch_ids, list) or not arch_ids or len(set(arch_ids)) != len(arch_ids):
        raise ValueError("Architecture package identities must be unique")
    archive_rows = archive.get("packages", [])
    if not isinstance(archive_rows, list) or len(archive_rows) != len(arch_ids):
        raise ValueError(
            "Draft authored archive package coverage differs from Architecture: "
            f"archive={len(archive_rows) if isinstance(archive_rows, list) else '?'} "
            f"architecture={len(arch_ids)}"
        )
    archive_ids = [row.get("package_id") if isinstance(row, dict) else None for row in archive_rows]
    if len(set(archive_ids)) != len(archive_ids):
        raise ValueError("Draft authored archive duplicates package identity")
    if set(archive_ids) != set(arch_ids):
        raise ValueError("Draft authored archive package coverage differs from Architecture")
    for entry in ordered:
        pid = entry["package"]["package_id"]
        spec = entry["spec"]
        package = entry["package"]
        result = entry["result"]
        spec_blocks = spec.get("blocks", [])
        if not isinstance(spec_blocks, list):
            raise ValueError(f"Draft authored archive blocks invalid for {pid}")
        spec_ids = [b.get("block_id") if isinstance(b, dict) else None for b in spec_blocks]
        if len(set(spec_ids)) != len(spec_ids):
            raise ValueError(f"Draft authored archive duplicates block identity for {pid}")
        result_blocks = [b for b in result.get("blocks", []) if b.get("block_type") != "CLAIM_BOUNDARY"]
        result_ids = [b.get("block_id") for b in result_blocks]
        if len(set(result_ids)) != len(result_ids):
            raise ValueError(f"Draft Result duplicates rendered block identity for {pid}")
        if set(spec_ids) != set(result_ids):
            raise ValueError(
                f"Draft authored archive block coverage differs from accepted Result for {pid}: "
                f"archive-only={sorted(set(spec_ids) - set(result_ids))} "
                f"result-only={sorted(set(result_ids) - set(spec_ids))}"
            )
        # EVERY assigned DID must resolve exactly once inside its own package via
        # accepted citation_refs semantics. An archive-only extra block carrying
        # another package's accepted DID therefore refuses here.
        deck_ids = spec.get("deck_discovery_ids", [])
        deck_mode = spec.get("deck_ref_mode", "CLAIMS")
        citation_refs.refs(package, list(deck_ids), deck_mode)
        for block in spec_blocks:
            citation_refs.refs(package, list(block.get("discovery_ids", [])), block.get("ref_mode", "CLAIMS"))


def _revision_ids(revision: dict[str, Any]) -> list[str]:
    values: list[str] = []
    for package in revision["packages"]:
        for row in package["theme_at_a_glance"]:
            values.extend(row["discovery_ids"])
        for section in package["narrative_sections"]:
            for row in section["paragraphs"]:
                values.extend(row["discovery_ids"])
        for row in package["timeline"]:
            values.extend(row["discovery_ids"])
        for row in package["synthesis"]["paragraphs"]:
            values.extend(row["discovery_ids"])
        for row in package["reader_claim_boundary"]:
            values.extend(row["discovery_ids"])
        for note in package["technical_notes"]:
            values.append(note["discovery_id"])
    cross = revision["cross_family_synthesis"]
    for row in cross["paragraphs"]:
        values.extend(row["discovery_ids"])
    for row in cross["comparison_rows"]:
        values.extend(row["discovery_ids"])
    return list(dict.fromkeys(values))


def build_longform_reader_input(
    issue_id: str,
    profile: dict[str, Any],
    architecture: dict[str, Any],
    authored: dict[str, Any],
    synthesis_result: dict[str, Any],
    ordered: list[dict[str, Any]],
    records: dict[str, dict[str, str]],
) -> dict[str, Any]:
    """Purely project validated values into the complete reader object."""
    if not _ISSUE_ID.fullmatch(issue_id):
        raise ValueError(f"issue_id outside the supported token subset: {issue_id!r}")
    if profile.get("issue_id") != issue_id or architecture.get("issue_id") != issue_id:
        raise ValueError("Profile/Architecture issue identity mismatch for reader projection")
    if profile.get("research_profile") != "THEMATIC" or profile.get("publication_profile") != "LONGFORM_SPECIAL":
        raise ValueError("LONGFORM_GENERATED_V1 requires THEMATIC / LONGFORM_SPECIAL")
    if synthesis_result.get("issue_id") != issue_id:
        raise ValueError("Profile Synthesis issue identity mismatch for reader projection")
    if not isinstance(authored, dict) or set(authored) != {
        "schema_version", "issue_id", "runner", "cover", "frontmatter", "final_summary", "longform_revision",
    }:
        raise ValueError("publication-authored longform input envelope invalid")
    if authored.get("schema_version") != "2.0-rc1" or authored.get("issue_id") != issue_id:
        raise ValueError("publication-authored longform input identity invalid")
    # Modest envelope/type policy only: runner is non-reader mechanical metadata.
    # Any non-empty runner string projects identically; route authority comes
    # from Profile, never from this field.
    if not isinstance(authored.get("runner"), str) or not authored["runner"].strip():
        raise ValueError("publication-authored longform input runner must be a non-empty string")
    cover = authored["cover"]
    if not isinstance(cover, dict) or set(cover) != {"headline", "deck", "anchors"}:
        raise ValueError("publication cover fields invalid")
    if not isinstance(cover.get("anchors"), list) or not cover["anchors"]:
        raise ValueError("publication cover anchors invalid")
    cover_out = {
        "headline": _reader_text(cover["headline"], "cover.headline"),
        "deck": _reader_text(cover["deck"], "cover.deck"),
        "anchors": [_reader_text(item, "cover.anchors") for item in cover["anchors"]],
    }
    front = authored["frontmatter"]
    if not isinstance(front, dict) or set(front) != {"heading", "lede", "scope_notes"}:
        raise ValueError("publication frontmatter fields invalid")
    if not isinstance(front.get("scope_notes"), list) or not front["scope_notes"]:
        raise ValueError("publication scope notes invalid")
    frontmatter_out = {
        "heading": _reader_text(front["heading"], "frontmatter.heading"),
        "lede": _reader_text(front["lede"], "frontmatter.lede"),
        "scope_notes": [_reader_text(item, "frontmatter.scope_notes") for item in front["scope_notes"]],
    }
    summary = authored["final_summary"]
    if not isinstance(summary, dict) or set(summary) != {"heading", "paragraphs"}:
        raise ValueError("publication final summary fields invalid")
    if summary.get("heading") != FIXED_FINAL_HEADING:
        raise ValueError("required final issue summary heading is missing")
    if (
        not isinstance(summary.get("paragraphs"), list)
        or len(summary["paragraphs"]) < 3
        or not all(isinstance(item, str) and item.strip() for item in summary["paragraphs"])
    ):
        raise ValueError("final issue summary must contain at least three substantive paragraphs")
    summary_out = {
        "heading": FIXED_FINAL_HEADING,
        "paragraphs": [_reader_text(item, "final_summary.paragraphs") for item in summary["paragraphs"]],
        "placement": FINAL_PLACEMENT,
    }
    plan_by_id = {row["package_id"]: row for row in architecture.get("packages", [])}
    if len(plan_by_id) != len(architecture.get("packages", [])):
        raise ValueError("Architecture package identities must be unique")
    for pid, plan in plan_by_id.items():
        if not _PACKAGE_ID.fullmatch(pid):
            raise ValueError(f"Architecture package_id outside the supported token subset: {pid!r}")
        if not isinstance(plan.get("drafting_order"), int) or plan["drafting_order"] < 1:
            raise ValueError(f"Architecture drafting_order invalid: {pid}")
    seen_rows = {row["package"]["package_id"] for row in ordered}
    if seen_rows != set(plan_by_id):
        raise ValueError("reader projection package coverage differs from Architecture")
    ranked = sorted(ordered, key=lambda row: (plan_by_id[row["package"]["package_id"]]["drafting_order"], row["package"]["package_id"]))
    revision = authored["longform_revision"]
    if not isinstance(revision, dict) or set(revision) != {
        "review_reference", "new_external_evidence", "packages", "cross_family_synthesis",
    }:
        raise ValueError("longform_revision envelope invalid")
    _nonempty(revision["review_reference"], "longform_revision.review_reference")
    if revision["new_external_evidence"] is not False:
        raise ValueError("post-draft longform revision must not introduce new external Evidence")
    rows = revision["packages"]
    if not isinstance(rows, list) or len(rows) != len(plan_by_id):
        raise ValueError("longform_revision must provide exactly one row per approved Architecture package")
    selected_union: set[str] = set()
    for row in ranked:
        assigned = _assigned_ids(row["spec"])
        for item in assigned:
            _did(item, "assigned Discovery ID")
        selected_union.update(assigned)
    normalized: list[dict[str, Any]] = []
    used: set[str] = set()
    total = len(ranked)
    for ordinal, row in enumerate(ranked, start=1):
        pid = row["package"]["package_id"]
        allowed = set(_assigned_ids(row["spec"]))
        matches = [item for item in rows if isinstance(item, dict) and item.get("package_id") == pid]
        if len(matches) != 1:
            raise ValueError(f"longform_revision must provide exactly one row for package: {pid}")
        if pid in used:
            raise ValueError(f"duplicate longform package row: {pid}")
        used.add(pid)
        item = matches[0]
        if set(item) != {
            "package_id", "theme_at_a_glance", "narrative_sections", "timeline",
            "synthesis", "reader_claim_boundary", "technical_notes",
        }:
            raise ValueError(f"longform_revision.packages row envelope invalid: {pid}")
        glance = item["theme_at_a_glance"]
        if not isinstance(glance, list) or len(glance) < 2:
            raise ValueError(f"{pid} Theme at a glance requires at least two rows")
        glance_out = []
        for pos, cell in enumerate(glance):
            if not isinstance(cell, dict) or set(cell) != {"label", "text", "discovery_ids"}:
                raise ValueError(f"{pid} theme_at_a_glance[{pos}] invalid")
            glance_out.append({
                "label": _reader_text(cell["label"], f"{pid}.glance[{pos}].label"),
                "text": _reader_text(cell["text"], f"{pid}.glance[{pos}].text"),
                "discovery_ids": _ids(cell["discovery_ids"], f"{pid}.glance[{pos}].discovery_ids", allowed),
            })
        sections = item["narrative_sections"]
        if not isinstance(sections, list) or len(sections) < 2:
            raise ValueError(f"{pid} requires at least two supplemental narrative sections")
        sections_out = []
        for pos, section in enumerate(sections):
            if not isinstance(section, dict) or set(section) != {"heading", "paragraphs"}:
                raise ValueError(f"{pid}.narrative_sections[{pos}] invalid")
            sections_out.append({
                "heading": _reader_text(section["heading"], f"{pid}.narrative_sections[{pos}].heading"),
                "paragraphs": _validate_paragraph_rows(
                    section["paragraphs"], f"{pid}.narrative_sections[{pos}].paragraphs", allowed
                ),
            })
        timeline = item["timeline"]
        if not isinstance(timeline, list) or len(timeline) < 2:
            raise ValueError(f"{pid} timeline requires at least two transition anchors")
        timeline_out = []
        for pos, cell in enumerate(timeline):
            if not isinstance(cell, dict) or set(cell) != {"label", "text", "discovery_ids"}:
                raise ValueError(f"{pid}.timeline[{pos}] invalid")
            timeline_out.append({
                "label": _reader_text(cell["label"], f"{pid}.timeline[{pos}].label"),
                "text": _reader_text(cell["text"], f"{pid}.timeline[{pos}].text"),
                "discovery_ids": _ids(cell["discovery_ids"], f"{pid}.timeline[{pos}].discovery_ids", allowed),
            })
        synthesis = item["synthesis"]
        if not isinstance(synthesis, dict) or set(synthesis) != {"heading", "paragraphs"}:
            raise ValueError(f"{pid}.synthesis invalid")
        synthesis_out = {
            "heading": _reader_text(synthesis["heading"], f"{pid}.synthesis.heading"),
            "paragraphs": _validate_paragraph_rows(synthesis["paragraphs"], f"{pid}.synthesis.paragraphs", allowed),
        }
        boundary = _validate_paragraph_rows(item["reader_claim_boundary"], f"{pid}.reader_claim_boundary", allowed)
        notes = item["technical_notes"]
        if not isinstance(notes, list) or not notes:
            raise ValueError(f"{pid} requires source-backed Technical Notes")
        note_out = []
        note_ids = []
        for pos, note in enumerate(notes):
            if not isinstance(note, dict) or set(note) != {
                "title", "discovery_id", "chronology", "technical_points", "limitation", "primary_url",
            }:
                raise ValueError(f"{pid}.technical_notes[{pos}] invalid")
            target = _did(note["discovery_id"], f"{pid}.technical_notes[{pos}].discovery_id")
            if target not in allowed:
                raise ValueError(f"{pid}.technical_notes[{pos}] cites Evidence outside the approved package: {target}")
            record = records.get(target)
            if record is None:
                raise ValueError(f"Technical Note Discovery ID missing from accepted records: {target}")
            if note["primary_url"] != record["url"]:
                raise ValueError(
                    f"{pid}.technical_notes[{pos}] primary_url differs from accepted Evidence: {target}"
                )
            points = note["technical_points"]
            if not isinstance(points, list) or len(points) < 2:
                raise ValueError(f"{pid}.technical_notes[{pos}] requires at least two technical points")
            note_out.append({
                "title": _reader_text(note["title"], f"{pid}.technical_notes[{pos}].title"),
                "discovery_id": target,
                "chronology": _reader_text(note["chronology"], f"{pid}.technical_notes[{pos}].chronology"),
                "technical_points": [
                    _reader_text(point, f"{pid}.technical_notes[{pos}].technical_points") for point in points
                ],
                "limitation": _reader_text(note["limitation"], f"{pid}.technical_notes[{pos}].limitation"),
                "primary_url": record["url"],
            })
            note_ids.append(target)
        if len(set(note_ids)) != len(note_ids):
            raise ValueError(f"{pid} Technical Notes repeat a Discovery ID")
        if set(note_ids) != allowed:
            missing = sorted(allowed - set(note_ids))
            extra = sorted(set(note_ids) - allowed)
            raise ValueError(
                f"{pid} Technical Notes must cover every assigned Evidence source exactly once; "
                f"missing={missing}, extra={extra}"
            )
        result = row["result"]
        spec = row["spec"]
        headline = _reader_text(result["headline"], f"{pid}.headline")
        deck = _reader_text(result["deck"], f"{pid}.deck")
        if headline != spec.get("headline") or deck != spec.get("deck"):
            raise ValueError(f"Draft semantic archive drift for {pid}")
        normalized.append({
            "package_id": pid,
            "drafting_order": plan_by_id[pid]["drafting_order"],
            "headline": headline,
            "deck": deck,
            "deck_discovery_ids": _ids(spec.get("deck_discovery_ids", []), f"{pid}.deck_discovery_ids", allowed),
            "kicker": _kicker(pid, ordinal, total),
            "theme_at_a_glance": glance_out,
            "narrative_sections": sections_out,
            "timeline": timeline_out,
            "synthesis": synthesis_out,
            "reader_claim_boundary": boundary,
            "technical_notes": note_out,
        })
    cross = revision["cross_family_synthesis"]
    if not isinstance(cross, dict) or set(cross) != {"heading", "paragraphs", "comparison_rows"}:
        raise ValueError("cross_family_synthesis envelope invalid")
    comparison = cross["comparison_rows"]
    if not isinstance(comparison, list) or len(comparison) < 3:
        raise ValueError("cross_family_synthesis requires at least three comparison rows")
    comp_out = []
    for pos, entry in enumerate(comparison):
        if not isinstance(entry, dict) or set(entry) != {
            "dimension", "glm", "qwen", "deepseek", "kimi", "discovery_ids",
        }:
            raise ValueError(f"cross_family_synthesis.comparison_rows[{pos}] invalid")
        comp_out.append({
            "dimension": _reader_text(entry["dimension"], f"cross comparison[{pos}].dimension"),
            "glm": _reader_text(entry["glm"], f"cross comparison[{pos}].glm"),
            "qwen": _reader_text(entry["qwen"], f"cross comparison[{pos}].qwen"),
            "deepseek": _reader_text(entry["deepseek"], f"cross comparison[{pos}].deepseek"),
            "kimi": _reader_text(entry["kimi"], f"cross comparison[{pos}].kimi"),
            "discovery_ids": _ids(entry["discovery_ids"], f"cross comparison[{pos}].discovery_ids", selected_union),
        })
    cross_out = {
        "heading": _reader_text(cross["heading"], "cross_family_synthesis.heading"),
        "paragraphs": _validate_paragraph_rows(
            cross["paragraphs"], "cross_family_synthesis.paragraphs", selected_union
        ),
        "comparison_rows": comp_out,
    }
    cited: list[str] = []
    for row in ranked:
        cited.extend(_assigned_ids(row["spec"]))
    cited.extend(_revision_ids({
        "packages": [
            {
                "theme_at_a_glance": item["theme_at_a_glance"],
                "narrative_sections": item["narrative_sections"],
                "timeline": item["timeline"],
                "synthesis": item["synthesis"],
                "reader_claim_boundary": item["reader_claim_boundary"],
                "technical_notes": item["technical_notes"],
            }
            for item in normalized
        ],
        "cross_family_synthesis": {
            "paragraphs": cross_out["paragraphs"],
            "comparison_rows": cross_out["comparison_rows"],
        },
    }))
    cited = list(dict.fromkeys(cited))
    bibliography = []
    seen_keys: set[str] = set()
    for item in cited:
        record = records.get(item)
        if record is None:
            raise ValueError(f"cited Discovery ID missing from accepted Core authorities: {item}")
        if record["status"] not in ("VERIFIED", "PARTIAL") or record["materiality"] in ("HOLD", "NEEDS_MORE"):
            raise ValueError(f"publication cannot cite held-back Evidence: {item}")
        key = _bib_key(item)
        if key in seen_keys:
            raise ValueError(f"citation key collision across cited Discovery IDs: {key}")
        seen_keys.add(key)
        bibliography.append({
            "discovery_id": item,
            "key": key,
            "title": record["title"],
            "author": record["author"],
            "url": record["url"],
            "urldate": record["urldate"],
        })
    temporal = profile.get("research_scope", {}).get("temporal_policy", {})
    if temporal.get("mode") not in ("OPEN_HISTORY_AS_OF", "CURRENT_STATE_AS_OF"):
        raise ValueError("LONGFORM_GENERATED_V1 requires a THEMATIC as-of temporal policy")
    raw_as_of = temporal.get("as_of")
    if not isinstance(raw_as_of, str) or not raw_as_of.strip():
        raise ValueError("THEMATIC temporal policy requires as_of")
    try:
        core.parse_instant(raw_as_of)
    except ValueError as exc:
        raise ValueError(f"THEMATIC as_of is not a valid instant: {raw_as_of!r}") from exc
    display_as_of = raw_as_of.replace("T", " ").replace("Z", " UTC")
    return {
        "schema_version": "2.0-rc1",
        "route": ROUTE,
        "format": FORMAT,
        "issue_id": issue_id,
        "research_profile": "THEMATIC",
        "publication_profile": "LONGFORM_SPECIAL",
        "issue_metadata": {"title": FIXED_TITLE, "display_as_of": display_as_of},
        # Deep copy isolates mutable header list so mutating one returned
        # surface cannot alter future trusted projections.
        "visible_text": copy.deepcopy(VISIBLE_TEXT),
        "cover": cover_out,
        "frontmatter": frontmatter_out,
        "packages": normalized,
        "cross_family_synthesis": cross_out,
        "final_summary": summary_out,
        "bibliography": bibliography,
    }


def validate_longform_reader_input(root: Path, value_or_path: dict[str, Any] | Path) -> dict[str, Any]:
    """Validate a projected reader object against the strict reader-only schema."""
    if isinstance(value_or_path, Path):
        # Contained-read contract applies to the path overload as well: the
        # candidate path is validated before any read.
        safe = _safe(root, value_or_path, "Longform complete reader input")
        value = schema_gate.load_and_validate_json(
            safe, root / READER_INPUT_SCHEMA, label="Longform complete reader input"
        )
    else:
        value = value_or_path
        schema_gate.validate_instance(value, root / READER_INPUT_SCHEMA, label="Longform complete reader input")
    if (
        value.get("route") != ROUTE
        or value.get("format") != FORMAT
        or value.get("research_profile") != "THEMATIC"
        or value.get("publication_profile") != "LONGFORM_SPECIAL"
    ):
        raise ValueError("Longform complete reader input route/format/Profile mismatch")
    return value


def canonical_reader_bytes(value: dict[str, Any]) -> bytes:
    """Exact reader file bytes. Digest is SHA256 of THESE bytes (not sha256_object)."""
    return core.json_bytes(value)


READBACK_LIFECYCLES = ("DRAFT_COMPLETE", "VALIDATED_DRAFT", "RELEASE_CANDIDATE", "FROZEN", "RELEASED")


def _derive_authority_context(
    root: Path,
    state: dict[str, Any],
    state_path: Path,
    profile: dict[str, Any],
    profile_path: Path,
    cfg: dict[str, Any],
    authored_path: Path,
    issue_id: str,
) -> dict[str, Any]:
    source_root = core.repo_local_path(root, profile["paths"]["source_root"], "paths.source_root")
    survey_root = core.repo_local_path(root, profile["paths"]["survey_root"], "paths.survey_root")
    directive_lexical = source_root / DIRECTIVE_REL
    if os.path.lexists(directive_lexical):
        raise ValueError(
            "unsupported directive authority: editorial/post-architecture-directives-v2.json "
            "is present (file or symlink) without an accepted producer binding; refusing before projection"
        )

    def accepted(checkpoint: str, name: str) -> dict[str, Any]:
        return agent.resolve_checkpoint_artifact(root, cfg, state, checkpoint, name)

    architecture_ref = accepted("architecture", "issue-architecture")
    architecture_path = architecture_ref["artifact_path"]
    architecture = schema_gate.load_and_validate_json(
        architecture_path, root / Path("schemas/issue-architecture-v2.schema.json"), label="Issue Architecture"
    )
    synthesis_input_ref = accepted("draft", "synthesis-input")
    synthesis_result_ref = accepted("draft", "synthesis-result")
    synthesis_result = core.load_json(synthesis_result_ref["artifact_path"])
    syn_errors = drafting.validate_synthesis_result(
        synthesis_result, synthesis_input_ref["artifact_path"], root / drafting.SYNTHESIS_PROMPT
    )
    if syn_errors:
        raise ValueError("upstream Profile Synthesis invalid: " + "; ".join(syn_errors))
    archive_path = _safe(root, source_root / "draft/v2/interactive-drafting-synthesis-input.json", "Drafting authored archive")
    archive = core.load_json(archive_path)
    if not isinstance(archive.get("packages"), list):
        raise ValueError("Draft authored archive packages invalid")
    if len({row.get("package_id") for row in archive["packages"] if isinstance(row, dict)}) != len(archive["packages"]):
        raise ValueError("Draft authored archive duplicates package identity")
    spec_by_id = {row["package_id"]: row for row in archive.get("packages", []) if isinstance(row, dict)}
    ordered: list[dict[str, Any]] = []
    accepted_refs = [
        _artifact(root, "production-profile", profile_path),
        _artifact(root, "issue-architecture", architecture_path),
        _artifact(root, "synthesis-input", synthesis_input_ref["artifact_path"]),
        _artifact(root, "synthesis-result", synthesis_result_ref["artifact_path"]),
    ]
    evidence_sha: str | None = None
    for plan in sorted(architecture["packages"], key=lambda row: (row["drafting_order"], row["package_id"])):
        pid = plan["package_id"]
        package_ref = accepted("draft", f"draft-package:{pid}")
        result_ref = accepted("draft", f"draft-result:{pid}")
        package = core.load_json(package_ref["artifact_path"])
        result = core.load_json(result_ref["artifact_path"])
        result_errors = drafting.validate_draft_result(result, package_ref["artifact_path"], root / drafting.DRAFT_PROMPT)
        if result_errors:
            raise ValueError(f"upstream Draft Result invalid for {pid}: " + "; ".join(result_errors))
        spec = spec_by_id.get(pid)
        if spec is None:
            raise ValueError(f"Draft authored archive missing package: {pid}")
        if result.get("headline") != spec.get("headline") or result.get("deck") != spec.get("deck"):
            raise ValueError(f"Draft semantic archive drift for {pid}")
        spec_blocks = {block["block_id"]: block for block in spec.get("blocks", [])}
        if len(spec_blocks) != len(spec.get("blocks", [])):
            raise ValueError(f"Draft authored archive duplicates block identity for {pid}")
        for result_block in result.get("blocks", []):
            if result_block.get("block_type") == "CLAIM_BOUNDARY":
                continue
            source = spec_blocks.get(result_block["block_id"])
            if source is None or source.get("text") != result_block.get("text"):
                raise ValueError(f"Draft block semantic archive drift for {pid}/{result_block['block_id']}")
            mode = source.get("ref_mode", "CLAIMS")
            expected = citation_refs.refs(package, source.get("discovery_ids", []), mode)
            if expected != result_block.get("evidence_refs"):
                raise ValueError(
                    f"authored block Discovery placement differs from accepted Result refs: "
                    f"{pid}/{result_block['block_id']}"
                )
        deck_mode = spec.get("deck_ref_mode", "CLAIMS")
        if citation_refs.refs(package, spec.get("deck_discovery_ids", []), deck_mode) != result.get("deck_evidence_refs"):
            raise ValueError(f"authored deck Discovery placement differs from accepted Result refs: {pid}")
        current_evidence = package["basis"]["evidence_acceptance_sha256"]
        if evidence_sha is None:
            evidence_sha = current_evidence
        elif evidence_sha != current_evidence:
            raise ValueError("Draft packages disagree on Evidence acceptance authority")
        ordered.append({"plan": plan, "spec": spec, "package": package, "result": result})
        accepted_refs.extend([
            _artifact(root, f"draft-package:{pid}", package_ref["artifact_path"]),
            _artifact(root, f"draft-result:{pid}", result_ref["artifact_path"]),
        ])
    # Exact archive/package/block authorization after per-package drift checks:
    # no extra/duplicate archive package or block survives, and EVERY assigned
    # DID is validated through its own package's exact-one citation semantics.
    _validate_archive_authorization(architecture, archive, ordered)
    evidence_ref = accepted("evidence", "evidence-acceptance")
    matrix_ref = accepted("selection", "candidate-matrix")
    ledger_ref = accepted("materiality", "materiality-ledger")
    discovery_ref = accepted("discovery", "discovery-acceptance")
    if evidence_sha != core.sha256_file(evidence_ref["artifact_path"]):
        raise ValueError("Draft packages differ from checkpoint Evidence acceptance")
    implementation_sha = core.repository_commit_sha(root)
    selected_ids: set[str] = set()
    for entry in ordered:
        for item in _assigned_ids(entry["spec"]):
            _did(item, "assigned Discovery ID")
            selected_ids.add(item)
    records, card_refs = _longform_records(
        root, matrix_ref["artifact_path"], ledger_ref["artifact_path"], discovery_ref["artifact_path"],
        evidence_ref["artifact_path"], implementation_sha, selected_ids,
    )
    accepted_refs.extend([
        _artifact(root, "evidence-acceptance", evidence_ref["artifact_path"]),
        _artifact(root, "candidate-matrix", matrix_ref["artifact_path"]),
        _artifact(root, "materiality-ledger", ledger_ref["artifact_path"]),
        _artifact(root, "discovery-acceptance", discovery_ref["artifact_path"]),
        *card_refs,
    ])
    authored = core.load_json(authored_path)
    surface = build_longform_reader_input(
        issue_id, profile, architecture, authored, synthesis_result, ordered, records
    )
    validate_longform_reader_input(root, surface)
    return {
        "surface": surface,
        "state": state,
        "state_path": state_path,
        "profile": profile,
        "profile_path": profile_path,
        "source_root": source_root,
        "survey_root": survey_root,
        "archive_path": archive_path,
        "authored_path": authored_path,
        "accepted_refs": sorted(accepted_refs, key=lambda row: row["name"]),
        "authored_refs": sorted([
            _artifact(root, "publication-authored-input", authored_path),
            _artifact(root, "drafting-archive", archive_path),
        ], key=lambda row: row["name"]),
        "records": records,
    }


def load_derivation(root: Path, state_path: Path, authored_path: Path) -> dict[str, Any]:
    """Load current accepted authority and return deterministic derivation context.

    Read-only: validates State/Profile/checkpoints/acceptance/cards/Matrix/
    Materiality/Discovery/Architecture/Draft/Synthesis/archive/authored input,
    projects the reader surface purely, validates it, and returns memory values
    only. Writes no files. Retains the exact initial DRAFT_COMPLETE write
    eligibility boundary (lifecycle plus configured next action).
    """
    for var in _GIT_OVERRIDE_VARS:
        if os.environ.get(var):
            raise ValueError(f"unsafe inherited Git root override for derivation: {var}")
    state_path = _safe(root, state_path, "Production State")
    authored_path = _safe(root, authored_path, "publication-authored input")
    state = core.load_json(state_path)
    cfg = core.load_json(root / core.DEFAULT_CONFIG)
    if cfg["orchestration"]["stage_plan"]["DRAFT_COMPLETE"]["handler"] != REQUIRED_ACTION:
        raise ValueError("configured DRAFT_COMPLETE handler is not the supported reader-publication route")
    errors = agent.validate_agent_state(root, cfg, state)
    if errors:
        raise ValueError("Production State invalid for Longform derivation: " + "; ".join(errors))
    if state.get("lifecycle_state") != REQUIRED_LIFECYCLE:
        raise ValueError(
            f"Longform derivation requires exact {REQUIRED_LIFECYCLE} State, "
            f"found {state.get('lifecycle_state')!r}"
        )
    if state.get("next_action") != REQUIRED_ACTION:
        raise ValueError(
            f"Longform derivation requires configured action {REQUIRED_ACTION}, "
            f"found {state.get('next_action')!r}"
        )
    profile_path = _safe(root, state["profile"]["path"], "Production Profile")
    profile = core.load_json(profile_path)
    if profile.get("research_profile") != "THEMATIC" or profile.get("publication_profile") != "LONGFORM_SPECIAL":
        raise ValueError("LONGFORM_GENERATED_V1 requires THEMATIC / LONGFORM_SPECIAL")
    if profile.get("issue_id") != state.get("issue_id"):
        raise ValueError("Production Profile/State issue identity mismatch")
    issue_id = state["issue_id"]
    return _derive_authority_context(root, state, state_path, profile, profile_path, cfg, authored_path, issue_id)


def load_derivation_for_readback(root: Path, state_path: Path, authored_path: Path) -> dict[str, Any]:
    """Read-only derivation replay for healthy later lifecycle authorities.

    Permits the explicit tested allowlist DRAFT_COMPLETE, VALIDATED_DRAFT,
    RELEASE_CANDIDATE, FROZEN and RELEASED. Retains validated Profile/accepted
    checkpoints/Architecture/Draft/source attribution and the legacy-directive
    presence refusal. Rejects unrecognized or terminal-invalid states,
    mismatched live authority and unsupported pending/revalidation contexts via
    the strict State validator (no pending-basis bypass, no manufactured
    former-State dictionary, no editorial-correction renewal). Never writes
    and never calls a publisher.
    """
    for var in _GIT_OVERRIDE_VARS:
        if os.environ.get(var):
            raise ValueError(f"unsafe inherited Git root override for derivation: {var}")
    state_path = _safe(root, state_path, "Production State")
    authored_path = _safe(root, authored_path, "publication-authored input")
    state = core.load_json(state_path)
    cfg = core.load_json(root / core.DEFAULT_CONFIG)
    if cfg["orchestration"]["stage_plan"]["DRAFT_COMPLETE"]["handler"] != REQUIRED_ACTION:
        raise ValueError("configured DRAFT_COMPLETE handler is not the supported reader-publication route")
    errors = agent.validate_agent_state(root, cfg, state)
    if errors:
        raise ValueError("Production State invalid for Longform readback: " + "; ".join(errors))
    if state.get("lifecycle_state") not in READBACK_LIFECYCLES:
        raise ValueError(
            "Longform readback requires a healthy lifecycle State "
            f"{list(READBACK_LIFECYCLES)}, found {state.get('lifecycle_state')!r}"
        )
    if state.get("terminal_reason") not in (None, "", "HUMAN_GATE_REACHED", "COMPLETE"):
        raise ValueError(
            f"Longform readback refuses terminal-invalid State: {state.get('terminal_reason')!r}"
        )
    profile_path = _safe(root, state["profile"]["path"], "Production Profile")
    profile = core.load_json(profile_path)
    if profile.get("research_profile") != "THEMATIC" or profile.get("publication_profile") != "LONGFORM_SPECIAL":
        raise ValueError("LONGFORM_GENERATED_V1 requires THEMATIC / LONGFORM_SPECIAL")
    if profile.get("issue_id") != state.get("issue_id"):
        raise ValueError("Production Profile/State issue identity mismatch")
    issue_id = state["issue_id"]
    return _derive_authority_context(root, state, state_path, profile, profile_path, cfg, authored_path, issue_id)
