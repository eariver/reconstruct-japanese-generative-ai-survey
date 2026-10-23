#!/usr/bin/env python3
"""Complete Weekly reader projection, deterministic rendering, and replay validation."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any

from scripts import survey_agent_control_v2 as agent
from scripts import survey_agent_tool_v2 as runtime_tool
from scripts import survey_bibliography_access_provenance_v2 as provenance
from scripts import survey_drafting_citation_refs_v2 as citation_refs
from scripts import survey_drafting_v2 as drafting
from scripts import survey_evidence_v2 as evidence
from scripts import survey_production_v2 as core
from scripts import survey_schema_v2 as schema_gate
from scripts.render_article_draft_tex import tex_escape


READER_INPUT_SCHEMA = Path("schemas/reader-surface-input-v2.schema.json")
RECEIPT_SCHEMA = Path("schemas/weekly-publication-source-manifest-v2.schema.json")
STYLE_PATH = Path("templates/survey/jgaisurvey.sty")
ROUTE = "WEEKLY_GENERATED_V2"
WEEKLY_BUILD_INPUTS = {"main.tex", "references.bib", "jgaisurvey.sty"}
WEEKLY_BUILD_OUTPUTS = {"main.pdf", "main.log", "main.pdf.sha256"}
CURRENT_CLOSURE = (
    Path("scripts/survey_weekly_derivation_v2.py"),
    Path("scripts/survey_weekly_semantic_publication_v2.py"),
    Path("scripts/survey_drafting_citation_refs_v2.py"),
    Path("scripts/survey_bibliography_access_provenance_v2.py"),
    Path("scripts/render_article_draft_tex.py"),
    READER_INPUT_SCHEMA,
    RECEIPT_SCHEMA,
    STYLE_PATH,
)
VISIBLE_TEXT = {
    "frontmatter_boundary": "Evidence / scope boundary",
    "claim_boundary": "Claim boundary",
    "summary_kicker": "WEEKLY SYNTHESIS",
    "references_title": "References / Source Notes",
    "cover_cutoff_label": "Editorial cutoff",
    "cover_repository_label": "Repository",
    "cover_build_label": "Build",
    "repository_value": "eariver/japanese-generative-ai-survey",
    "build_value": "LuaLaTeX / jlreq / LuaTeX-ja",
    "edition_descriptor": "週刊Technical Survey",
    "strapline": "一次情報・論文・OSS・X上の技術反応を分離し、検証可能なEvidence chainとして編成する",
}


def _rel(root: Path, path: Path) -> str:
    return str(path.resolve().relative_to(root.resolve())).replace("\\", "/")


def _safe(root: Path, raw: str | Path, label: str) -> Path:
    path = Path(raw)
    if not path.is_absolute():
        path = root / path
    if path.is_symlink():
        raise ValueError(f"{label} symlink is unsafe: {raw}")
    # Reject symlink ancestors/aliases before resolving: walk lexical components
    # from the repo root to the target's parent. Resolving first would erase
    # alias information and permit out-of-root retention/live writes.
    root_resolved = root.resolve()
    # Build lexical absolute path without resolving symlinks.
    lexical = path if path.is_absolute() else (root_resolved / path)
    # Normalize .. and . lexically for ancestor walk (do not resolve).
    try:
        # Use root_resolved as base; check each parent component exists as symlink.
        current = root_resolved
        # Determine relative parts from root to lexical parent.
        try:
            rel_parent = (lexical.parent).relative_to(root_resolved)
            rel_parts: tuple[str, ...] = rel_parent.parts
        except ValueError:
            # Lexical parent escapes root before resolution: refuse.
            raise ValueError(f"{label} escapes repository: {raw}")
        for part in rel_parts:
            if part in ("..", ".", ""):
                raise ValueError(f"{label} has unsafe path component: {part}")
            current = current / part
            if current.is_symlink():
                raise ValueError(f"{label} has symlinked ancestor component: {current}")
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError(f"{label} ancestor check failed: {exc}") from exc
    resolved = path.resolve()
    try:
        resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise ValueError(f"{label} escapes repository: {raw}") from exc
    if resolved.is_symlink() or not resolved.is_file():
        raise ValueError(f"{label} missing or unsafe: {raw}")
    return resolved


def validate_survey_build_directory(root: Path, raw_survey_root: str) -> Path:
    """Admit only declared local inputs and known non-input Weekly outputs."""
    raw = Path(raw_survey_root)
    try:
        resolved = core.repo_local_path(root, raw_survey_root, "Weekly survey build directory")
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Weekly survey build directory path invalid: {exc}") from exc
    lexical = root.resolve() / raw
    current = root.resolve()
    for component in raw.parts:
        current = current / component
        if current.is_symlink():
            raise ValueError(f"Weekly survey build directory has symlinked component: {current}")
    if lexical != resolved:
        raise ValueError("Weekly survey build directory is not at its physical canonical path")
    if not lexical.exists():
        return lexical
    if not lexical.is_dir():
        raise ValueError("Weekly survey build directory is not a directory")
    allowed = WEEKLY_BUILD_INPUTS | WEEKLY_BUILD_OUTPUTS
    for entry in lexical.iterdir():
        if entry.is_symlink() or not entry.is_file() or entry.name not in allowed:
            raise ValueError(f"Weekly survey build directory contains undeclared entry: {entry.name}")
    return lexical


def _artifact(root: Path, name: str, path: Path) -> dict[str, str]:
    safe = _safe(root, path, name)
    return {"name": name, "path": _rel(root, safe), "sha256": core.sha256_file(safe)}


def _window(profile: dict[str, Any]) -> tuple[str, str]:
    temporal = profile.get("research_scope", {}).get("temporal_policy", {})
    if temporal.get("mode") != "ROLLING_WINDOW":
        raise ValueError("WEEKLY_GENERATED_V2 requires ROLLING_WINDOW temporal policy")
    start, end, cutoff, timezone = (
        temporal.get("window_start"), temporal.get("window_end"),
        temporal.get("cutoff"), temporal.get("timezone"),
    )
    if not all(isinstance(value, str) and value.strip() for value in (start, end, cutoff, timezone)):
        raise ValueError("Weekly temporal policy requires window_start/window_end/cutoff/timezone")
    if end != cutoff:
        raise ValueError("Weekly publication requires window_end == cutoff")
    return end[:10], f"Window: {start[:16].replace('T', ' ')} - {end[:16].replace('T', ' ')} {timezone}"


def _validate_authored_input(data: dict[str, Any], issue_id: str, heading: str) -> None:
    if set(data) != {"schema_version", "issue_id", "runner", "cover", "frontmatter", "final_summary"}:
        raise ValueError("semantic publication input envelope invalid")
    if data.get("schema_version") != "2.0-rc1" or data.get("issue_id") != issue_id:
        raise ValueError("semantic publication input identity invalid")
    if data.get("runner") != "WEEKLY_MAGAZINE":
        raise ValueError("semantic publication input runner must be WEEKLY_MAGAZINE")
    cover = data.get("cover")
    if not isinstance(cover, dict) or set(cover) != {"headline", "deck", "anchors"}:
        raise ValueError("publication cover fields invalid")
    if not all(isinstance(cover.get(key), str) and cover[key].strip() for key in ("headline", "deck")):
        raise ValueError("publication cover invalid")
    if not isinstance(cover.get("anchors"), list) or not cover["anchors"] or not all(
        isinstance(value, str) and value.strip() for value in cover["anchors"]
    ):
        raise ValueError("publication cover anchors invalid")
    front = data.get("frontmatter")
    if not isinstance(front, dict) or set(front) != {"heading", "lede", "scope_notes"}:
        raise ValueError("publication frontmatter fields invalid")
    if not all(isinstance(front.get(key), str) and front[key].strip() for key in ("heading", "lede")):
        raise ValueError("publication frontmatter invalid")
    if not isinstance(front.get("scope_notes"), list) or not front["scope_notes"] or not all(
        isinstance(value, str) and value.strip() for value in front["scope_notes"]
    ):
        raise ValueError("publication scope notes invalid")
    summary = data.get("final_summary")
    if not isinstance(summary, dict) or set(summary) != {"heading", "paragraphs"}:
        raise ValueError("publication final summary fields invalid")
    if summary.get("heading") != heading:
        raise ValueError("Weekly final issue summary heading differs from approved Architecture")
    if not isinstance(summary.get("paragraphs"), list) or len(summary["paragraphs"]) < 3 or not all(
        isinstance(value, str) and value.strip() for value in summary["paragraphs"]
    ):
        raise ValueError("Weekly final issue summary must contain at least three substantive paragraphs")


def _strict_evidence_sources(
    root: Path, acceptance_path: Path, implementation_sha: str,
    pending_basis: agent._PendingPublicationBasis | None = None,
) -> tuple[dict[str, dict[str, Any]], list[dict[str, str]]]:
    with runtime_tool.current_stage_basis_override(pending_basis):
        acceptance, _ = evidence.validate_evidence_acceptance(root, acceptance_path, implementation_sha)
    sources: dict[str, dict[str, Any]] = {}
    refs: list[dict[str, str]] = []
    for row in acceptance["results"]:
        card_path = acceptance_path.parent / "results" / row["filename"]
        if core.sha256_file(card_path) != row["sha256"]:
            raise ValueError(f"accepted Evidence card SHA drift: {row['evidence_task_id']}")
        card = core.load_json(card_path)
        card_sources = card.get("sources")
        if not isinstance(card_sources, list) or not card_sources:
            raise ValueError(f"accepted Evidence card has no sources: {row['evidence_task_id']}")
        refs.append(_artifact(root, f"evidence-card:{row['evidence_task_id']}", card_path))
        for did in row["discovery_ids"]:
            if did in sources:
                raise ValueError(f"Discovery ID appears in multiple accepted Evidence cards: {did}")
            sources[did] = {"sources": card_sources, "card": card}
    return sources, refs


def _records_from_authorities(
    root: Path,
    matrix_path: Path,
    ledger_path: Path,
    discovery_path: Path,
    acceptance_path: Path,
    implementation_sha: str,
    pending_basis: agent._PendingPublicationBasis | None = None,
) -> tuple[dict[str, dict[str, Any]], list[dict[str, str]]]:
    matrix, ledger, discovery = map(core.load_json, (matrix_path, ledger_path, discovery_path))
    acceptance_sha = core.sha256_file(acceptance_path)
    if matrix.get("basis", {}).get("evidence_acceptance_sha256") != acceptance_sha:
        raise ValueError("Candidate Matrix does not bind checkpoint Evidence acceptance")
    if matrix.get("basis", {}).get("materiality_ledger_sha256") != core.sha256_file(ledger_path):
        raise ValueError("Candidate Matrix materiality authority drifted")
    accepted = core.load_json(acceptance_path)
    accepted_status: dict[str, str] = {}
    for row in accepted.get("results", []):
        for did in row.get("discovery_ids", []):
            if did in accepted_status:
                raise ValueError(f"Discovery ID appears more than once in Evidence acceptance: {did}")
            accepted_status[did] = row["status"]
    materiality = {row["discovery_id"]: row["downstream_disposition"] for row in ledger.get("rows", [])}
    discovery_rows = {row["discovery_id"]: row for row in discovery.get("records", [])}
    evidence_sources, card_refs = _strict_evidence_sources(root, acceptance_path, implementation_sha, pending_basis)
    records: dict[str, dict[str, Any]] = {}
    for row in matrix.get("rows", []):
        title = row.get("title")
        if not isinstance(title, str) or not title.strip():
            raise ValueError(f"Candidate Matrix row lacks title: {row.get('candidate_id')}")
        for did in row.get("discovery_ids", []):
            if did in records:
                raise ValueError(f"Candidate Matrix duplicates Discovery ID: {did}")
            if accepted_status.get(did) != row.get("evidence_status"):
                raise ValueError(f"Evidence status authority mismatch for {did}")
            if materiality.get(did) != row.get("materiality"):
                raise ValueError(f"Materiality authority mismatch for {did}")
            discovery_row = discovery_rows.get(did)
            if discovery_row is None:
                raise ValueError(f"Candidate Matrix Discovery ID missing from accepted Discovery: {did}")
            url = discovery_row.get("source_locator")
            if not isinstance(url, str) or not url.strip():
                raise ValueError(f"accepted Discovery lacks source locator: {did}")
            ev = evidence_sources.get(did)
            if ev is None:
                raise ValueError(f"cited Discovery ID {did} has no acceptance-bound Evidence card")
            resolved = provenance.resolve_source_access_provenance(ev["sources"], url.strip(), did)
            records[did] = {
                "title": title.strip(), "author": "Unknown", "url": url.strip(),
                "source_accessed_at": resolved["source_accessed_at"], "urldate": resolved["urldate"],
                "status": row["evidence_status"], "materiality": row["materiality"],
            }
    return records, card_refs


def _key(issue_id: str, discovery_id: str) -> str:
    raw = issue_id + discovery_id
    if not re.fullmatch(r"[A-Za-z0-9:_-]+", raw):
        raise ValueError(f"unsafe citation identity: {discovery_id}")
    normalized = "w" + raw
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9:_-]*", normalized):
        raise ValueError(f"unsafe citation identity: {discovery_id}")
    return normalized


def _closing_summary(architecture: dict[str, Any]) -> tuple[str, str]:
    closing = architecture.get("publication_extensions", {}).get("closing_summary", {})
    weekly = architecture.get("profile_extensions", {}).get("weekly_closing_summary", {})
    if (
        closing.get("required") is not True
        or not isinstance(closing.get("heading"), str)
        or not closing["heading"].strip()
        or closing.get("placement") != "after_body_before_references"
        or weekly.get("required") is not True
        or weekly.get("source") != "profile_synthesis.current_interpretation"
    ):
        raise ValueError("Weekly closing summary must be required and sourced from profile_synthesis.current_interpretation")
    return closing["heading"], closing["placement"]


def build_reader_input(
    issue_id: str,
    profile: dict[str, Any],
    architecture: dict[str, Any],
    authored: dict[str, Any],
    synthesis_result: dict[str, Any],
    ordered: list[dict[str, Any]],
    records: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Purely project already validated values into the complete reader object."""
    heading, _ = _closing_summary(architecture)
    _validate_authored_input(authored, issue_id, heading)
    # The validated WEEKLY synthesis contract owns this exact field. The
    # WEEKLY_MAGAZINE publication payload is required to be empty.
    payload = synthesis_result.get("profile_payload")
    if not isinstance(payload, dict):
        raise ValueError("Weekly Profile Synthesis lacks profile_payload")
    closing_text = payload.get("current_interpretation")
    if not isinstance(closing_text, str) or not closing_text.strip():
        raise ValueError("Weekly Profile Synthesis lacks current_interpretation")
    if closing_text not in authored["final_summary"]["paragraphs"]:
        raise ValueError("Weekly final summary must preserve exact approved synthesis paragraph")
    display_date, boundary = _window(profile)
    cited: list[str] = []
    packages: list[dict[str, Any]] = []
    for row in ordered:
        plan, spec, package, result = (row[name] for name in ("plan", "spec", "package", "result"))
        if result["headline"] != spec["headline"] or result["deck"] != spec["deck"]:
            raise ValueError(f"Draft semantic archive drift for {result['package_id']}")
        expected_deck_refs = citation_refs.refs(
            package, spec["deck_discovery_ids"], spec.get("deck_ref_mode", "CLAIMS")
        )
        if expected_deck_refs != result["deck_evidence_refs"]:
            raise ValueError(f"authored deck Discovery placement differs from accepted Result refs: {result['package_id']}")
        cited.extend(spec["deck_discovery_ids"])
        deck_citations = [{"discovery_id": did, "key": _key(issue_id, did)} for did in spec["deck_discovery_ids"]]
        spec_blocks = {block["block_id"]: block for block in spec["blocks"]}
        blocks: list[dict[str, Any]] = []
        for result_block in result["blocks"]:
            block_type = result_block["block_type"]
            citations: list[dict[str, str]] = []
            if block_type != "CLAIM_BOUNDARY":
                source = spec_blocks.get(result_block["block_id"])
                if source is None or source["text"] != result_block["text"]:
                    raise ValueError(
                        f"Draft block semantic archive drift for {result['package_id']}/{result_block['block_id']}"
                    )
                mode = source.get("ref_mode", "CLAIMS")
                dids = source.get("discovery_ids", [])
                expected = citation_refs.refs(package, dids, mode)
                if expected != result_block["evidence_refs"]:
                    raise ValueError(
                        f"authored block Discovery placement differs from accepted Result refs: "
                        f"{result['package_id']}/{result_block['block_id']}"
                    )
                cited.extend(dids)
                citations = [{"discovery_id": did, "key": _key(issue_id, did)} for did in dids]
            blocks.append({
                "block_id": result_block["block_id"], "block_type": block_type,
                "text": result_block["text"], "attribution_mode": result_block["attribution_mode"],
                "citations": citations,
            })
        label = plan.get("publication_extensions", {}).get("section_label")
        if not isinstance(label, str) or not label.strip():
            raise ValueError(f"Weekly package missing publication section_label: {result['package_id']}")
        packages.append({
            "package_id": result["package_id"], "section_label": label.strip(),
            "headline": result["headline"], "deck": result["deck"],
            "deck_citations": deck_citations, "blocks": blocks,
        })
    cited = list(dict.fromkeys(cited))
    bibliography: list[dict[str, str]] = []
    for did in cited:
        record = records.get(did)
        if record is None:
            raise ValueError(f"cited Discovery ID missing from accepted Core authorities: {did}")
        if record["materiality"] == "HOLD" or record["status"] == "NEEDS_MORE":
            raise ValueError(f"publication cannot cite HOLD/NEEDS_MORE Evidence: {did}")
        bibliography.append({
            "discovery_id": did, "key": _key(issue_id, did), "title": record["title"],
            "author": record["author"], "url": record["url"], "urldate": record["urldate"],
        })
    value = {
        "schema_version": "2.0-rc1", "route": ROUTE, "issue_id": issue_id,
        "research_profile": "WEEKLY", "publication_profile": "WEEKLY_MAGAZINE",
        "issue_metadata": {
            "title": "Japanese Generative AI Technical Survey",
            "display_date": display_date, "window_boundary": boundary,
        },
        "visible_text": dict(VISIBLE_TEXT),
        "cover": authored["cover"], "frontmatter": authored["frontmatter"],
        "closing_synthesis": closing_text, "final_summary": authored["final_summary"],
        "packages": packages, "bibliography": bibliography,
    }
    return value


def validate_reader_input(root: Path, value_or_path: dict[str, Any] | Path) -> dict[str, Any]:
    if isinstance(value_or_path, Path):
        value = schema_gate.load_and_validate_json(
            value_or_path, root / READER_INPUT_SCHEMA, label="Weekly complete reader input"
        )
    else:
        value = value_or_path
        schema_gate.validate_instance(value, root / READER_INPUT_SCHEMA, label="Weekly complete reader input")
    if value.get("route") != ROUTE or value.get("research_profile") != "WEEKLY" or value.get("publication_profile") != "WEEKLY_MAGAZINE":
        raise ValueError("Weekly complete reader input route/Profile mismatch")
    return value


def _cite(rows: list[dict[str, str]]) -> str:
    return "" if not rows else " \\cite{" + ",".join(row["key"] for row in rows) + "}"


def render_main(surface: dict[str, Any]) -> str:
    """Pure deterministic TeX rendering from the reviewed reader object."""
    visible, meta = surface["visible_text"], surface["issue_metadata"]
    cover, front, summary = surface["cover"], surface["frontmatter"], surface["final_summary"]
    lines = [
        "% Generated from the reviewed Core v2 complete reader input. Do not hand-edit.",
        "\\documentclass[lualatex,a4paper,10pt]{jlreq}", "\\usepackage{jgaisurvey}",
        "\\addbibresource{references.bib}", "",
        f"\\surveysetup{{{tex_escape(surface['issue_id'])}}}{{{tex_escape(meta['title'])}}}{{{tex_escape(meta['display_date'])}}}{{{tex_escape(meta['window_boundary'])}}}",
        f"\\surveycoverstory{{{tex_escape(cover['headline'])}}}{{{tex_escape(cover['deck'])}}}{{{tex_escape(' / '.join(cover['anchors']))}}}",
        f"\\surveyrepository{{{tex_escape(visible['repository_value'])}}}",
        f"\\surveybuildvalue{{{tex_escape(visible['build_value'])}}}",
        f"\\surveycoverlabels{{{tex_escape(visible['cover_cutoff_label'])}}}{{{tex_escape(visible['cover_repository_label'])}}}{{{tex_escape(visible['cover_build_label'])}}}",
        f"\\surveystrapline{{{tex_escape(visible['strapline'])}}}",
        f"\\surveyeditiondescriptor{{{tex_escape(visible['edition_descriptor'])}}}", "",
        "\\begin{document}", "\\surveycover", "\\clearpage",
        f"\\section*{{{tex_escape(front['heading'])}}}", tex_escape(front["lede"]), "",
        f"\\begin{{claimboundary}}[{tex_escape(visible['frontmatter_boundary'])}]",
    ]
    for note in front["scope_notes"]:
        lines.append("\\noindent " + tex_escape(note) + "\\par")
    lines.extend(["\\end{claimboundary}", "\\clearpage", "\\twocolumn"])
    for package in surface["packages"]:
        lines.extend([
            f"\\section{{{tex_escape(package['headline'])}}}",
            f"\\label{{pkg:{tex_escape(package['package_id'])}}}",
            f"\\sectionkicker{{{tex_escape(package['section_label'])}}}",
            "\\noindent\\textbf{" + tex_escape(package["deck"]) + "}" + _cite(package["deck_citations"]) + "\\par\\medskip",
        ])
        for block in package["blocks"]:
            text = tex_escape(block["text"])
            if block["block_type"] == "CLAIM_BOUNDARY":
                lines.extend([f"\\begin{{claimboundary}}[{tex_escape(visible['claim_boundary'])}]", text, "\\end{claimboundary}"])
            else:
                lines.append("\\noindent " + text + _cite(block["citations"]) + "\\par\\medskip")
    lines.extend(["\\clearpage", "\\onecolumn", f"\\section{{{tex_escape(summary['heading'])}}}",
                  "\\label{sec:issue-summary}", f"\\sectionkicker{{{tex_escape(visible['summary_kicker'])}}}"])
    for paragraph in summary["paragraphs"]:
        lines.append("\\noindent " + tex_escape(paragraph) + "\\par\\medskip")
    lines.extend(["\\clearpage", "\\onecolumn",
                  f"\\printbibliography[title={{{tex_escape(visible['references_title'])}}}]",
                  "\\end{document}", ""])
    return "\n".join(lines)


def render_bibliography(surface: dict[str, Any]) -> str:
    """Pure deterministic BibLaTeX rendering from the reviewed reader object."""
    entries = []
    for row in surface["bibliography"]:
        for field in ("title", "author", "url"):
            value = row[field]
            if any(ord(ch) < 32 or ord(ch) == 127 for ch in value) or "\\" in value:
                raise ValueError(f"unsafe bibliography {field} control or TeX escape")
        if any(ch in row["url"] for ch in "{}"):
            raise ValueError("unsafe bibliography URL braces")
        title = tex_escape(row["title"])
        author = tex_escape(row["author"])
        entries.append(
            f"@online{{{row['key']},\n  title = {{{{{title}}}}},\n  author = {{{{{author}}}}},\n"
            f"  url = {{{row['url']}}},\n  urldate = {{{row['urldate']}}}\n}}"
        )
    return "\n\n".join(entries) + "\n"


def validate_generated_closure(main_text: str, style_text: str) -> None:
    if main_text.count("\\usepackage{jgaisurvey}") != 1 or main_text.count("\\addbibresource{references.bib}") != 1:
        raise ValueError("unsupported Weekly generated package/bibliography declaration")
    forbidden_main = re.findall(r"\\(?:input|include)(?![A-Za-z@])", main_text)
    extra_bib = re.findall(r"\\addbibresource\s*\{([^}]+)\}", main_text)
    if forbidden_main or extra_bib != ["references.bib"]:
        raise ValueError("unsupported Weekly generated include or bibliography route")
    if re.search(r"\\(?:input|include)(?![A-Za-z@])", style_text):
        raise ValueError("unsupported repository include in Weekly style")


def load_derivation(root: Path, state_path: Path, authored_path: Path, pending_basis: agent._PendingPublicationBasis | None = None) -> dict[str, Any]:
    """Load current State/checkpoint authority and return a deterministic derivation context."""
    state_path = _safe(root, state_path, "Production State")
    authored_path = _safe(root, authored_path, "publication-authored input")
    state = core.load_json(state_path)
    cfg = core.load_json(root / core.DEFAULT_CONFIG)
    if pending_basis is None and state.get("lifecycle_state") == "VALIDATED_DRAFT":
        strict_errors = agent.validate_agent_state(root, cfg, state)
        if strict_errors:
            changed, _kept = agent._collect_pending_rows(root, cfg, state, require_change=False)
            if changed:
                pending_basis = agent.built_checked_pending_publication_basis(root, cfg, state_path)
    errors = agent._validate_agent_state(root, cfg, state, pending_basis) if pending_basis is not None else agent.validate_agent_state(root, cfg, state)
    if errors:
        raise ValueError("Production State invalid for Weekly derivation: " + "; ".join(errors))
    if core.LIFECYCLE.index(state["lifecycle_state"]) < core.LIFECYCLE.index("DRAFT_COMPLETE"):
        raise ValueError("Weekly derivation requires DRAFT_COMPLETE or later State")
    profile_path = _safe(root, state["profile"]["path"], "Production Profile")
    profile = core.load_json(profile_path)
    if profile.get("research_profile") != "WEEKLY" or profile.get("publication_profile") != "WEEKLY_MAGAZINE":
        raise ValueError("WEEKLY_GENERATED_V2 requires WEEKLY / WEEKLY_MAGAZINE")
    issue_id = state["issue_id"]
    def accepted(checkpoint: str, name: str) -> dict[str, Any]:
        if pending_basis is None:
            return agent.resolve_checkpoint_artifact(root, cfg, state, checkpoint, name)
        return agent._resolve_checkpoint_artifact(root, cfg, state, checkpoint, name, pending_basis)

    architecture_ref = accepted("architecture", "issue-architecture")
    architecture_path = architecture_ref["artifact_path"]
    architecture = core.load_json(architecture_path)
    synthesis_input_ref = accepted("draft", "synthesis-input")
    synthesis_result_ref = accepted("draft", "synthesis-result")
    synthesis_result = core.load_json(synthesis_result_ref["artifact_path"])
    syn_errors = drafting.validate_synthesis_result(
        synthesis_result, synthesis_input_ref["artifact_path"], root / drafting.SYNTHESIS_PROMPT
    )
    if syn_errors:
        raise ValueError("upstream Profile Synthesis invalid: " + "; ".join(syn_errors))
    source_root = core.repo_local_path(root, profile["paths"]["source_root"], "Weekly source root")
    survey_root = core.repo_local_path(root, profile["paths"]["survey_root"], "Weekly survey root")
    archive_path = _safe(root, source_root / "draft/v2/interactive-drafting-synthesis-input.json", "Drafting authored archive")
    archive = core.load_json(archive_path)
    spec_by_id = {row["package_id"]: row for row in archive.get("packages", [])}
    ordered: list[dict[str, Any]] = []
    accepted_refs = [_artifact(root, "production-profile", profile_path), _artifact(root, "issue-architecture", architecture_path),
                     _artifact(root, "synthesis-input", synthesis_input_ref["artifact_path"]),
                     _artifact(root, "synthesis-result", synthesis_result_ref["artifact_path"])]
    evidence_sha: str | None = None
    for plan in sorted(architecture["packages"], key=lambda row: (row["drafting_order"], row["package_id"])):
        pid = plan["package_id"]
        package_ref = accepted("draft", f"draft-package:{pid}")
        result_ref = accepted("draft", f"draft-result:{pid}")
        package, result = map(core.load_json, (package_ref["artifact_path"], result_ref["artifact_path"]))
        result_errors = drafting.validate_draft_result(result, package_ref["artifact_path"], root / drafting.DRAFT_PROMPT)
        if result_errors:
            raise ValueError(f"upstream Draft Result invalid for {pid}: " + "; ".join(result_errors))
        spec = spec_by_id.get(pid)
        if spec is None:
            raise ValueError(f"Draft authored archive missing package: {pid}")
        current_evidence = package["basis"]["evidence_acceptance_sha256"]
        if evidence_sha is None:
            evidence_sha = current_evidence
        elif evidence_sha != current_evidence:
            raise ValueError("Draft packages disagree on Evidence acceptance authority")
        ordered.append({"plan": plan, "spec": spec, "package": package, "result": result})
        accepted_refs.extend([_artifact(root, f"draft-package:{pid}", package_ref["artifact_path"]),
                              _artifact(root, f"draft-result:{pid}", result_ref["artifact_path"])])
    evidence_ref = accepted("evidence", "evidence-acceptance")
    matrix_ref = accepted("selection", "candidate-matrix")
    ledger_ref = accepted("materiality", "materiality-ledger")
    discovery_ref = accepted("discovery", "discovery-acceptance")
    if evidence_sha != core.sha256_file(evidence_ref["artifact_path"]):
        raise ValueError("Draft packages differ from checkpoint Evidence acceptance")
    implementation_sha = core.repository_commit_sha(root)
    records, card_refs = _records_from_authorities(
        root, matrix_ref["artifact_path"], ledger_ref["artifact_path"], discovery_ref["artifact_path"],
        evidence_ref["artifact_path"], implementation_sha, pending_basis,
    )
    accepted_refs.extend([
        _artifact(root, "evidence-acceptance", evidence_ref["artifact_path"]),
        _artifact(root, "candidate-matrix", matrix_ref["artifact_path"]),
        _artifact(root, "materiality-ledger", ledger_ref["artifact_path"]),
        _artifact(root, "discovery-acceptance", discovery_ref["artifact_path"]),
        *card_refs,
    ])
    surface = build_reader_input(
        issue_id, profile, architecture, core.load_json(authored_path), synthesis_result, ordered, records
    )
    validate_reader_input(root, surface)
    return {
        "surface": surface, "state": state, "state_path": state_path, "profile": profile,
        "profile_path": profile_path, "source_root": source_root,
        "survey_root": survey_root,
        "archive_path": archive_path, "authored_path": authored_path,
        "accepted_refs": sorted(accepted_refs, key=lambda row: row["name"]), "records": records,
    }


def current_closure(root: Path) -> list[dict[str, str]]:
    return [_artifact(root, path.as_posix(), root / path) for path in CURRENT_CLOSURE]


def _verify_head_bytes(root: Path, commit: str, closure: list[dict[str, str]]) -> None:
    head = core.repository_commit_sha(root)
    valid_commit = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
        cwd=root, capture_output=True, check=False,
    )
    if valid_commit.returncode != 0:
        raise ValueError("Weekly receipt renderer commit is missing or is not a commit")
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", commit, head],
        cwd=root, capture_output=True, check=False,
    )
    if ancestor.returncode != 0:
        raise ValueError("Weekly receipt renderer commit is not an ancestor of current HEAD")
    cfg = core.load_json(root / core.DEFAULT_CONFIG)
    control_paths = [core.DEFAULT_CONFIG.as_posix(), *cfg["implementation_control_roots"]]
    control_paths.append(STYLE_PATH.as_posix())
    control_paths.extend(path for rows in cfg["contract_files"].values() for path in rows)
    control_paths = sorted(set(control_paths))
    # An artifact-only commit may move HEAD. Every implementation root, style,
    # and configured contract path must still match the receipt's commit.
    changed = subprocess.run(
        ["git", "diff", "--quiet", commit, head, "--", *control_paths],
        cwd=root, capture_output=True, check=False,
    )
    if changed.returncode != 0:
        raise ValueError("Weekly receipt implementation or contract changed since renderer commit")
    dirty = subprocess.run(
        ["git", "diff", "--quiet", "HEAD", "--", *control_paths],
        cwd=root, capture_output=True, check=False,
    )
    if dirty.returncode != 0:
        raise ValueError("Weekly current implementation or contract differs from committed HEAD")
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "--", *control_paths],
        cwd=root, capture_output=True, text=True, check=False,
    )
    if untracked.returncode != 0 or any(
        "__pycache__" not in Path(row).parts and Path(row).suffix != ".pyc"
        for row in untracked.stdout.splitlines()
    ):
        raise ValueError("Weekly current implementation or contract contains uncommitted source")
    expected_names = {path.as_posix() for path in CURRENT_CLOSURE}
    if len(closure) != len(expected_names) or {row.get("name") for row in closure} != expected_names:
        raise ValueError("Weekly receipt current-tool closure is incomplete or unexpected")
    for row in closure:
        path = _safe(root, row["path"], f"current-tool closure {row['name']}")
        if _rel(root, path) != row["name"] or core.sha256_file(path) != row["sha256"]:
            raise ValueError(f"Weekly receipt current-tool closure drift: {row['name']}")
        for basis in (commit, head):
            result = subprocess.run(
                ["git", "show", f"{basis}:{row['name']}"], cwd=root, capture_output=True, check=False
            )
            if result.returncode != 0 or core.sha256_bytes(result.stdout) != row["sha256"]:
                raise ValueError(f"Weekly current-tool bytes differ from exact committed basis: {row['name']}")


def build_receipt(
    root: Path, context: dict[str, Any], surface_path: Path, review_path: Path,
    primary_path: Path, bibliography_path: Path, style_path: Path,
) -> dict[str, Any]:
    cfg = core.load_json(root / core.DEFAULT_CONFIG)
    commit = core.repository_commit_sha(root)
    authored_archive = _artifact(root, "publication-semantic-input", context["authored_path"])
    drafting_archive = _artifact(root, "drafting-authored-archive", context["archive_path"])
    receipt = {
        "schema_version": "2.0-rc1", "issue_id": context["state"]["issue_id"],
        "route": ROUTE, "status": "ESTABLISHED",
        "production_state_basis": {
            "path": _rel(root, context["state_path"]),
            "historical_sha256": core.sha256_file(context["state_path"]),
            "lifecycle_state": context["state"]["lifecycle_state"],
        },
        "accepted_refs": context["accepted_refs"],
        "authored_refs": [authored_archive, drafting_archive],
        "reviewed_reader_input": {"path": _rel(root, surface_path), "sha256": core.sha256_file(surface_path)},
        "semantic_review": {"path": _rel(root, review_path), "sha256": core.sha256_file(review_path)},
        "current_tools": {
            "repository_commit_sha": commit,
            "contract": core.contract_identity(root, cfg, "WEEKLY", "WEEKLY_MAGAZINE"),
            "closure": current_closure(root),
        },
        "outputs": {
            "primary": {"path": _rel(root, primary_path), "sha256": core.sha256_file(primary_path)},
            "bibliography": {"path": _rel(root, bibliography_path), "sha256": core.sha256_file(bibliography_path)},
            "style": {"path": _rel(root, style_path), "sha256": core.sha256_file(style_path)},
        },
    }
    receipt["receipt_sha256"] = core.sha256_object(receipt)
    return receipt


def _inspect_receipt_envelope(root: Path, receipt_path: Path, state_path: Path | None = None) -> dict[str, Any]:
    """Private shared receipt-envelope/input inspection (no tool pinning, no replay).

    Checks schema, digest, State-file resolution, authored-ref shape and exact
    live input bytes. Shared by the public current-tool replay (which always
    runs tool pinning and independent derivation afterwards) and the
    mechanical-refresh owner (which calls this only after the old receipt raw
    hash has been anchored to the bound Gate, then verifies the historical
    closure independently). Never proves replay on its own.
    """
    receipt_path = _safe(root, receipt_path, "Weekly source receipt")
    receipt = schema_gate.load_and_validate_json(receipt_path, root / RECEIPT_SCHEMA, label="Weekly source receipt")
    base = dict(receipt)
    recorded_digest = base.pop("receipt_sha256")
    if core.sha256_object(base) != recorded_digest:
        raise ValueError("Weekly source receipt digest mismatch")
    state_file = _safe(root, state_path or receipt["production_state_basis"]["path"], "current Production State")
    authored = {row["name"]: row for row in receipt["authored_refs"]}
    if len(receipt["authored_refs"]) != 2 or set(authored) != {"publication-semantic-input", "drafting-authored-archive"}:
        raise ValueError("Weekly receipt authored refs invalid")
    for group in (receipt["accepted_refs"], receipt["authored_refs"]):
        if len(group) != len({row["name"] for row in group}):
            raise ValueError("Weekly receipt duplicate input names")
        for row in group:
            path = _safe(root, row["path"], row["name"])
            if core.sha256_file(path) != row["sha256"]:
                raise ValueError(f"Weekly receipt exact input drift: {row['name']}")
    return {"receipt": receipt, "state_file": state_file, "authored": authored}


def verify_closure_at_commit(root: Path, closure: list[dict[str, str]], commit: str) -> None:
    """Verify a recorded tool closure against one commit's actual Git blobs.

    Requires exact names/cardinality of ``CURRENT_CLOSURE`` and byte equality
    of every row with ``git show <commit>:<name>``. Rejects added, removed,
    renamed or content-changed closure paths. Mode-only differences do not
    affect blob bytes and are caught separately by the control-path diff.
    """
    valid_commit = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
        cwd=root, capture_output=True, check=False,
    )
    if valid_commit.returncode != 0:
        raise ValueError("Weekly receipt renderer commit is missing or is not a commit")
    expected_names = {path.as_posix() for path in CURRENT_CLOSURE}
    if len(closure) != len(expected_names) or {row.get("name") for row in closure} != expected_names:
        raise ValueError("Weekly receipt historical closure is incomplete or unexpected")
    for row in closure:
        if _rel(root, _safe(root, row["path"], f"historical closure {row['name']}")) != row["name"]:
            raise ValueError(f"Weekly receipt historical closure path mismatch: {row['name']}")
        result = subprocess.run(
            ["git", "show", f"{commit}:{row['name']}"], cwd=root, capture_output=True, check=False
        )
        if result.returncode != 0 or core.sha256_bytes(result.stdout) != row["sha256"]:
            raise ValueError(f"Weekly historical closure bytes differ from recorded commit: {row['name']}")


def validate_receipt(root: Path, receipt_path: Path, state_path: Path | None = None, pending_basis: agent._PendingPublicationBasis | None = None) -> dict[str, Any]:
    inspected = _inspect_receipt_envelope(root, receipt_path, state_path)
    receipt = inspected["receipt"]
    state_file = inspected["state_file"]
    authored = inspected["authored"]
    tools = receipt["current_tools"]
    _verify_head_bytes(root, tools["repository_commit_sha"], tools["closure"])
    cfg = core.load_json(root / core.DEFAULT_CONFIG)
    current_contract = core.contract_identity(root, cfg, "WEEKLY", "WEEKLY_MAGAZINE")
    if tools["contract"] != current_contract:
        raise ValueError("Weekly receipt current contract differs from current repository")
    context = load_derivation(root, state_file, _safe(root, authored["publication-semantic-input"]["path"], "authored input"), pending_basis)
    if context["state"]["issue_id"] != receipt["issue_id"]:
        raise ValueError("Weekly source receipt issue identity mismatch")
    if authored["drafting-authored-archive"] != _artifact(root, "drafting-authored-archive", context["archive_path"]):
        raise ValueError("Weekly receipt drafting archive differs from actual loaded archive")
    if context["accepted_refs"] != receipt["accepted_refs"]:
        raise ValueError("Weekly receipt accepted authority differs from current checkpoint chain")
    expected_outputs = {
        "primary": "main.tex", "bibliography": "references.bib", "style": "jgaisurvey.sty",
    }
    survey_relative = Path(context["profile"]["paths"]["survey_root"])
    for role, filename in expected_outputs.items():
        canonical = (survey_relative / filename).as_posix()
        if receipt["outputs"][role]["path"] != canonical:
            raise ValueError(f"Weekly receipt {role} output path is not canonical survey_root/{filename}")
    validate_survey_build_directory(root, context["profile"]["paths"]["survey_root"])
    surface_path = _safe(root, receipt["reviewed_reader_input"]["path"], "reviewed reader input")
    if core.sha256_file(surface_path) != receipt["reviewed_reader_input"]["sha256"]:
        raise ValueError("Weekly reviewed reader input drift")
    reviewed = validate_reader_input(root, surface_path)
    if context["surface"] != reviewed:
        raise ValueError("Weekly independently recomputed reader input differs from reviewed bytes")
    style_source = (root / STYLE_PATH).read_text(encoding="utf-8")
    main_text = render_main(reviewed)
    bib_text = render_bibliography(reviewed)
    validate_generated_closure(main_text, style_source)
    expected_bytes = {
        "primary": main_text.encode("utf-8"),
        "bibliography": bib_text.encode("utf-8"),
        "style": (root / STYLE_PATH).read_bytes(),
    }
    for name, data in expected_bytes.items():
        row = receipt["outputs"][name]
        path = _safe(root, row["path"], f"Weekly {name} output")
        if path.read_bytes() != data or core.sha256_bytes(data) != row["sha256"]:
            raise ValueError(f"Weekly deterministic {name} replay mismatch")
    return receipt
