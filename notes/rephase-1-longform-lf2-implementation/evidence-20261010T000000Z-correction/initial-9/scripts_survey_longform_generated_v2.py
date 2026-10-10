#!/usr/bin/env python3
"""Deterministic LONGFORM_GENERATED_V1 source rendering and receipt replay.

Initial generated-Longform integration owner (LF-2I). This module is the one
serializer/replay owner for the explicit new route:

- pure ``render_main`` / ``render_bibliography`` project ONLY the reviewed
  complete reader object (THEMATIC_FOUR_FAMILY_LINEAGE_V1) into exact
  main.tex / references.bib bytes. Every semantic value (titles, display
  dates/prefixes, cover/frontmatter/revision text, labels/kickers/table
  headers, note URLs, final summary, bibliography, citation placement/order)
  comes from the reviewed surface. Structural TeX commands mirror the
  reference layout inventory; no post-review Draft/body/sidecar reread and no
  arbitrary TeX escape hatch;
- pure ``tex_escape`` reuse only (from ``render_article_draft_tex``). The
  legacy publication writer (``run_semantic_publication_v2_interactive`` and
  its base) is never imported or invoked here;
- ``build_receipt`` / ``validate_receipt`` own the strict Longform source
  receipt (``LONGFORM_GENERATED_V1``). Public replay itself reloads and
  validates the persisted semantic review independently of the outer Gate
  (contract F1), then re-derives the reader object and replays deterministic
  output bytes;
- ``verify_tool_basis`` pins the exact committed implementation closure.
  Testing may materialize the exact selected bytes in fresh independent
  synthetic committed Git fixtures; production dirty/untracked-source checks
  stay strict.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Any

from scripts import survey_longform_derivation_v2 as longform
from scripts import survey_production_v2 as core
from scripts import survey_reader_surface_gate_v2 as surface_gate
from scripts import survey_schema_v2 as schema_gate
from scripts.render_article_draft_tex import tex_escape


RECEIPT_SCHEMA = Path("schemas/longform-publication-source-manifest-v2.schema.json")
STYLE_PATH = Path("templates/survey/jgaisurvey.sty")
ROUTE = "LONGFORM_GENERATED_V1"
SCOPE = "LONGFORM_MAIN_BIB_STYLE"
LONGFORM_BUILD_INPUTS = {"main.tex", "references.bib", "jgaisurvey.sty"}
LONGFORM_BUILD_OUTPUTS = {"main.pdf", "main.log", "main.pdf.sha256"}
# Explicit new-route closure. Unlisted shared helpers (agent/stage/drafting/
# evidence loaders, quality/fidelity/manuscript producers) are still bound by
# the control-roots + configured contract-file equality/ancestry check inside
# verify_tool_basis, so no unlisted change is exempt.
CURRENT_CLOSURE = (
    Path("scripts/survey_longform_generated_v2.py"),
    Path("scripts/survey_longform_semantic_publication_v2.py"),
    Path("scripts/survey_longform_derivation_v2.py"),
    Path("scripts/survey_drafting_citation_refs_v2.py"),
    Path("scripts/survey_bibliography_access_provenance_v2.py"),
    Path("scripts/render_article_draft_tex.py"),
    Path("schemas/longform-reader-input-v2.schema.json"),
    Path("schemas/longform-publication-source-manifest-v2.schema.json"),
    Path("schemas/reader-surface-semantic-review-v2.schema.json"),
    Path("schemas/reader-surface-gate-v2.schema.json"),
    Path("scripts/survey_reader_surface_gate_v2.py"),
    Path("scripts/survey_production_v2.py"),
    Path("scripts/survey_schema_v2.py"),
    STYLE_PATH,
)


def _rel(root: Path, path: Path) -> str:
    return str(path.resolve().relative_to(root.resolve())).replace("\\", "/")


def _safe(root: Path, raw: str | Path, label: str) -> Path:
    path = Path(raw)
    if not path.is_absolute():
        path = root / path
    if path.is_symlink():
        raise ValueError(f"{label} symlink is unsafe: {raw}")
    root_resolved = root.resolve()
    lexical = path if path.is_absolute() else (root_resolved / path)
    try:
        rel_parent = (lexical.parent).relative_to(root_resolved)
        rel_parts: tuple[str, ...] = rel_parent.parts
    except ValueError:
        raise ValueError(f"{label} escapes repository: {raw}")
    current = root_resolved
    for part in rel_parts:
        if part in ("..", ".", ""):
            raise ValueError(f"{label} has unsafe path component: {part}")
        current = current / part
        if current.is_symlink():
            raise ValueError(f"{label} has symlinked ancestor component: {current}")
    resolved = path.resolve()
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


def validate_survey_build_directory(root: Path, raw_survey_root: str) -> Path:
    """Admit only declared local inputs and known non-input Longform outputs."""
    raw = Path(raw_survey_root)
    try:
        resolved = core.repo_local_path(root, raw_survey_root, "Longform survey build directory")
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Longform survey build directory path invalid: {exc}") from exc
    lexical = root.resolve() / raw
    current = root.resolve()
    for component in raw.parts:
        current = current / component
        if current.is_symlink():
            raise ValueError(f"Longform survey build directory has symlinked component: {current}")
    if lexical != resolved:
        raise ValueError("Longform survey build directory is not at its physical canonical path")
    if not lexical.exists():
        return lexical
    if not lexical.is_dir():
        raise ValueError("Longform survey build directory is not a directory")
    allowed = LONGFORM_BUILD_INPUTS | LONGFORM_BUILD_OUTPUTS
    for entry in lexical.iterdir():
        if entry.is_symlink() or not entry.is_file() or entry.name not in allowed:
            raise ValueError(f"Longform survey build directory contains undeclared entry: {entry.name}")
    return lexical


def _cite(ids: list[str], bib_key_by_did: dict[str, str]) -> str:
    keys = []
    for did in ids:
        key = bib_key_by_did.get(did)
        if key is None:
            raise ValueError(f"citation Discovery ID has no reviewed bibliography key: {did}")
        keys.append(key)
    return "" if not keys else " \\cite{" + ",".join(keys) + "}"


def render_main(surface: dict[str, Any]) -> str:
    """Pure deterministic TeX rendering from the reviewed reader object only."""
    try:
        visible = surface["visible_text"]
        meta = surface["issue_metadata"]
        cover = surface["cover"]
        front = surface["frontmatter"]
        summary = surface["final_summary"]
        cross = surface["cross_family_synthesis"]
    except (KeyError, TypeError) as exc:
        raise ValueError(f"reviewed Longform reader object envelope invalid: {exc}") from exc
    bib_key_by_did = {row["discovery_id"]: row["key"] for row in surface.get("bibliography", [])}
    if len(bib_key_by_did) != len(surface.get("bibliography", [])):
        raise ValueError("reviewed Longform bibliography Discovery identities must be unique")
    display_as_of = meta["display_as_of"]
    lines = [
        "% Generated from the reviewed LONGFORM_GENERATED_V1 complete reader input. Do not hand-edit.",
        "\\documentclass[lualatex,a4paper,10pt]{jlreq}",
        "\\usepackage{jgaisurvey}",
        "\\addbibresource{references.bib}",
        "",
        f"\\surveysetup{{{tex_escape(surface['issue_id'])}}}{{{tex_escape(meta['title'])}}}"
        f"{{{tex_escape(visible['date_history_prefix'] + display_as_of)}}}"
        f"{{{tex_escape(visible['date_boundary_prefix'] + display_as_of)}}}",
        f"\\surveyeditiondescriptor{{{tex_escape(visible['edition_descriptor'])}}}",
        f"\\surveycoverstory{{{tex_escape(cover['headline'])}}}{{{tex_escape(cover['deck'])}}}"
        f"{{{tex_escape(' / '.join(cover['anchors']))}}}",
        f"\\surveyrepository{{{tex_escape(visible['repository_value'])}}}",
        f"\\surveybuildvalue{{{tex_escape(visible['build_value'])}}}",
        f"\\surveycoverlabels{{{tex_escape(visible['cover_cutoff_label'])}}}"
        f"{{{tex_escape(visible['cover_repository_label'])}}}{{{tex_escape(visible['cover_build_label'])}}}",
        f"\\surveystrapline{{{tex_escape(visible['strapline'])}}}",
        f"\\renewcommand{{\\contentsname}}{{{tex_escape(visible['toc_title'])}}}",
        "",
        "\\begin{document}",
        "\\surveycover",
        "\\clearpage",
        f"\\section*{{{tex_escape(front['heading'])}}}",
        f"\\addcontentsline{{toc}}{{section}}{{{tex_escape(front['heading'])}}}",
        tex_escape(front["lede"]),
        "",
        f"\\begin{{claimboundary}}[{tex_escape(visible['frontmatter_boundary'])}]",
    ]
    for note in front["scope_notes"]:
        lines.append("\\noindent " + tex_escape(note) + "\\par")
    lines.extend(["\\end{claimboundary}", "\\medskip", "\\tableofcontents", "\\clearpage"])
    for package in surface["packages"]:
        lines.append(f"% package:{package['package_id']}")
        lines.extend([
            "\\Needspace{0.24\\textheight}",
            f"\\section{{{tex_escape(package['headline'])}}}",
            f"\\label{{pkg:{tex_escape(package['package_id'])}}}",
            f"\\sectionkicker{{{tex_escape(package['kicker'])}}}",
            "\\noindent\\textbf{" + tex_escape(package["deck"]) + "}"
            + _cite(package["deck_discovery_ids"], bib_key_by_did) + "\\par\\medskip",
            f"\\begin{{themeoverview}}[{tex_escape(visible['theme_overview_title'])}]",
            "\\begin{tabularx}{\\linewidth}{@{}>{\\bfseries}p{0.22\\linewidth}X@{}}",
        ])
        for item in package["theme_at_a_glance"]:
            lines.append(
                tex_escape(item["label"]) + " & " + tex_escape(item["text"])
                + _cite(item["discovery_ids"], bib_key_by_did) + " \\\\"
            )
        lines.extend([
            "\\end{tabularx}", "\\end{themeoverview}", "\\medskip",
            "\\begin{multicols}{2}",
        ])
        for section in package["narrative_sections"]:
            lines.append("\\subsection*{" + tex_escape(section["heading"]) + "}")
            for para in section["paragraphs"]:
                lines.append(
                    "\\noindent " + tex_escape(para["text"])
                    + _cite(para["discovery_ids"], bib_key_by_did) + "\\par\\medskip"
                )
        lines.extend([
            "\\end{multicols}", "\\medskip", "\\begin{wideflow}",
            "\\subsection*{" + tex_escape(visible["timeline_heading"]) + "}",
            "\\begin{tabularx}{\\linewidth}{@{}>{\\bfseries}p{0.20\\linewidth}X@{}}",
        ])
        for item in package["timeline"]:
            lines.append(
                tex_escape(item["label"]) + " & " + tex_escape(item["text"])
                + _cite(item["discovery_ids"], bib_key_by_did) + " \\\\"
            )
        lines.extend(["\\end{tabularx}", "\\end{wideflow}", "\\medskip"])
        lines.extend([
            "\\begin{multicols}{2}",
            "\\subsection*{" + tex_escape(package["synthesis"]["heading"]) + "}",
        ])
        for para in package["synthesis"]["paragraphs"]:
            lines.append(
                "\\noindent " + tex_escape(para["text"])
                + _cite(para["discovery_ids"], bib_key_by_did) + "\\par\\medskip"
            )
        lines.extend([
            "\\end{multicols}", "\\medskip",
            f"\\begin{{claimboundary}}[{tex_escape(visible['claim_boundary'])}]",
        ])
        for para in package["reader_claim_boundary"]:
            lines.append(
                "\\noindent " + tex_escape(para["text"])
                + _cite(para["discovery_ids"], bib_key_by_did) + "\\par"
            )
        lines.extend([
            "\\end{claimboundary}", "\\medskip",
            "\\subsection*{" + tex_escape(visible["technical_notes_heading"]) + "}",
        ])
        for note in package["technical_notes"]:
            did = note["discovery_id"]
            lines.extend([
                "\\begin{technicalnote}[" + tex_escape(note["title"]) + "]",
                "\\noindent\\textbf{" + tex_escape(visible["note_chronology_label"]) + "} "
                + tex_escape(note["chronology"]) + _cite([did], bib_key_by_did) + "\\par",
                "\\smallskip\\noindent\\textbf{" + tex_escape(visible["note_points_label"]) + "}\\par",
                "\\begin{itemize}",
            ])
            for point in note["technical_points"]:
                lines.append("\\item " + tex_escape(point) + _cite([did], bib_key_by_did))
            lines.extend([
                "\\end{itemize}",
                "\\noindent\\textbf{" + tex_escape(visible["note_limitation_label"]) + "} "
                + tex_escape(note["limitation"]) + "\\par",
                "\\smallskip\\noindent\\textbf{" + tex_escape(visible["note_url_label"]) + "} "
                + "\\url{" + note["primary_url"] + "}\\par",
                "\\end{technicalnote}",
                "\\smallskip",
            ])
    table_header = visible["cross_table_header"]
    if not isinstance(table_header, list) or len(table_header) != 5:
        raise ValueError("reviewed Longform cross-family table header must carry exactly five labels")
    lines.extend([
        "\\Needspace{0.30\\textheight}",
        "\\section{" + tex_escape(cross["heading"]) + "}",
        f"\\sectionkicker{{{tex_escape(visible['cross_family_kicker'])}}}",
    ])
    for para in cross["paragraphs"]:
        lines.append(
            "\\noindent " + tex_escape(para["text"])
            + _cite(para["discovery_ids"], bib_key_by_did) + "\\par\\medskip"
        )
    lines.extend([
        f"\\begin{{themeoverview}}[{tex_escape(visible['cross_comparison_title'])}]",
        "\\scriptsize",
        "\\begin{tabularx}{\\linewidth}{@{}>{\\bfseries}p{0.12\\linewidth}XXXX@{}}",
        "\\toprule",
        " & ".join(tex_escape(cell) for cell in table_header) + " \\\\ ",
        "\\midrule",
    ])
    for row in cross["comparison_rows"]:
        lines.append(
            tex_escape(row["dimension"]) + " & " + tex_escape(row["glm"]) + " & "
            + tex_escape(row["qwen"]) + " & " + tex_escape(row["deepseek"]) + " & "
            + tex_escape(row["kimi"]) + _cite(row["discovery_ids"], bib_key_by_did) + " \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabularx}", "\\end{themeoverview}"])
    lines.extend([
        "\\Needspace{0.28\\textheight}",
        f"\\section{{{tex_escape(summary['heading'])}}}",
        "\\label{sec:issue-summary}",
        f"\\sectionkicker{{{tex_escape(visible['issue_summary_kicker'])}}}",
        "\\begin{multicols}{2}",
    ])
    for paragraph in summary["paragraphs"]:
        lines.append("\\noindent " + tex_escape(paragraph) + "\\par\\medskip")
    lines.extend([
        "\\end{multicols}",
        "\\clearpage",
        "\\onecolumn",
        f"\\printbibliography[title={{{tex_escape(visible['references_title'])}}}]",
        "\\end{document}",
        "",
    ])
    return "\n".join(lines)


def render_bibliography(surface: dict[str, Any]) -> str:
    """Pure deterministic BibLaTeX rendering from the reviewed reader object."""
    entries = []
    for row in surface.get("bibliography", []):
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
    if not entries:
        raise ValueError("reviewed Longform bibliography must cite at least one source")
    return "\n\n".join(entries) + "\n"


def validate_generated_closure(main_text: str, style_text: str) -> None:
    """Finite preflight: closed package/bibliography/style inventory, no escapes."""
    if main_text.count("\\usepackage{jgaisurvey}") != 1 or main_text.count("\\addbibresource{references.bib}") != 1:
        raise ValueError("unsupported Longform generated package/bibliography declaration")
    if main_text.count("\\renewcommand{\\contentsname}") != 1:
        raise ValueError("unsupported Longform generated contentsname declaration")
    forbidden_main = re.findall(r"\\(?:input|include)(?![A-Za-z@])", main_text)
    extra_bib = re.findall(r"\\addbibresource\s*\{([^}]+)\}", main_text)
    if forbidden_main or extra_bib != ["references.bib"]:
        raise ValueError("unsupported Longform generated include or bibliography route")
    if re.search(r"\\(?:input|include)(?![A-Za-z@])", style_text):
        raise ValueError("unsupported repository include in Longform style")


def current_closure(root: Path) -> list[dict[str, str]]:
    return [_artifact(root, path.as_posix(), root / path) for path in CURRENT_CLOSURE]


def verify_tool_basis(root: Path, tools: dict[str, Any]) -> None:
    """Pin the exact committed implementation closure for the new route.

    Requires the recorded renderer commit to be an ancestor of current HEAD,
    exact equality of every implementation-control root / configured contract
    path between that commit and HEAD, a clean HEAD over those paths, no
    uncommitted control source, and byte equality of every closure row with
    both the recorded commit and current HEAD. An uncommitted exact-source
    overlay therefore refuses as a committed implementation basis.
    """
    commit = tools["repository_commit_sha"]
    closure = tools["closure"]
    head = core.repository_commit_sha(root)
    valid_commit = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
        cwd=root, capture_output=True, check=False,
    )
    if valid_commit.returncode != 0:
        raise ValueError("Longform receipt renderer commit is missing or is not a commit")
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", commit, head],
        cwd=root, capture_output=True, check=False,
    )
    if ancestor.returncode != 0:
        raise ValueError("Longform receipt renderer commit is not an ancestor of current HEAD")
    cfg = core.load_json(root / core.DEFAULT_CONFIG)
    control_paths = [core.DEFAULT_CONFIG.as_posix(), *cfg["implementation_control_roots"]]
    control_paths.append(STYLE_PATH.as_posix())
    control_paths.extend(path for rows in cfg["contract_files"].values() for path in rows)
    control_paths = sorted(set(control_paths))
    changed = subprocess.run(
        ["git", "diff", "--quiet", commit, head, "--", *control_paths],
        cwd=root, capture_output=True, check=False,
    )
    if changed.returncode != 0:
        raise ValueError("Longform receipt implementation or contract changed since renderer commit")
    dirty = subprocess.run(
        ["git", "diff", "--quiet", "HEAD", "--", *control_paths],
        cwd=root, capture_output=True, check=False,
    )
    if dirty.returncode != 0:
        raise ValueError("Longform current implementation or contract differs from committed HEAD")
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "--", *control_paths],
        cwd=root, capture_output=True, text=True, check=False,
    )
    if untracked.returncode != 0 or any(
        "__pycache__" not in Path(row).parts and Path(row).suffix != ".pyc"
        for row in untracked.stdout.splitlines()
    ):
        raise ValueError("Longform current implementation or contract contains uncommitted source")
    expected_names = {path.as_posix() for path in CURRENT_CLOSURE}
    if len(closure) != len(expected_names) or {row.get("name") for row in closure} != expected_names:
        raise ValueError("Longform receipt current-tool closure is incomplete or unexpected")
    for row in closure:
        path = _safe(root, row["path"], f"current-tool closure {row['name']}")
        if _rel(root, path) != row["name"] or core.sha256_file(path) != row["sha256"]:
            raise ValueError(f"Longform receipt current-tool closure drift: {row['name']}")
        for basis in (commit, head):
            result = subprocess.run(
                ["git", "show", f"{basis}:{row['name']}"], cwd=root, capture_output=True, check=False
            )
            if result.returncode != 0 or core.sha256_bytes(result.stdout) != row["sha256"]:
                raise ValueError(f"Longform current-tool bytes differ from exact committed basis: {row['name']}")


def verify_closure_at_commit(root: Path, closure: list[dict[str, str]], commit: str) -> None:
    """Verify a recorded tool closure against one commit's actual Git blobs."""
    valid_commit = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
        cwd=root, capture_output=True, check=False,
    )
    if valid_commit.returncode != 0:
        raise ValueError("Longform receipt renderer commit is missing or is not a commit")
    expected_names = {path.as_posix() for path in CURRENT_CLOSURE}
    if len(closure) != len(expected_names) or {row.get("name") for row in closure} != expected_names:
        raise ValueError("Longform receipt historical closure is incomplete or unexpected")
    for row in closure:
        if _rel(root, _safe(root, row["path"], f"historical closure {row['name']}")) != row["name"]:
            raise ValueError(f"Longform receipt historical closure path mismatch: {row['name']}")
        result = subprocess.run(
            ["git", "show", f"{commit}:{row['name']}"], cwd=root, capture_output=True, check=False
        )
        if result.returncode != 0 or core.sha256_bytes(result.stdout) != row["sha256"]:
            raise ValueError(f"Longform historical closure bytes differ from recorded commit: {row['name']}")


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
            "contract": core.contract_identity(root, cfg, "THEMATIC", "LONGFORM_SPECIAL"),
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
    """Shared receipt-envelope/input inspection (no tool pinning, no replay)."""
    receipt_path = _safe(root, receipt_path, "Longform source receipt")
    receipt = schema_gate.load_and_validate_json(receipt_path, root / RECEIPT_SCHEMA, label="Longform source receipt")
    base = dict(receipt)
    recorded_digest = base.pop("receipt_sha256")
    if core.sha256_object(base) != recorded_digest:
        raise ValueError("Longform source receipt digest mismatch")
    if receipt.get("route") != ROUTE:
        raise ValueError("Longform source receipt route mismatch")
    state_file = _safe(root, state_path or receipt["production_state_basis"]["path"], "current Production State")
    authored = {row["name"]: row for row in receipt["authored_refs"]}
    if len(receipt["authored_refs"]) != 2 or set(authored) != {"publication-semantic-input", "drafting-authored-archive"}:
        raise ValueError("Longform receipt authored refs invalid")
    for group in (receipt["accepted_refs"], receipt["authored_refs"]):
        if len(group) != len({row["name"] for row in group}):
            raise ValueError("Longform receipt duplicate input names")
        for row in group:
            path = _safe(root, row["path"], row["name"])
            if core.sha256_file(path) != row["sha256"]:
                raise ValueError(f"Longform receipt exact input drift: {row['name']}")
    return {"receipt": receipt, "state_file": state_file, "authored": authored}


def validate_receipt(root: Path, receipt_path: Path, state_path: Path | None = None) -> dict[str, Any]:
    """Independently replay a Longform source receipt against current authority.

    In addition to envelope/self-digest, live accepted/authored refs and
    tool/contract pinning, this public validator itself reloads and validates
    the persisted semantic review (exact expected surface/path/Profile,
    require_pass), binds the same review file SHA, independently re-derives
    the reader object through the readback loader, and replays deterministic
    output bytes. Never proves replay on envelope inspection alone.
    """
    inspected = _inspect_receipt_envelope(root, receipt_path, state_path)
    receipt = inspected["receipt"]
    state_file = inspected["state_file"]
    authored = inspected["authored"]
    tools = receipt["current_tools"]
    verify_tool_basis(root, tools)
    cfg = core.load_json(root / core.DEFAULT_CONFIG)
    current_contract = core.contract_identity(root, cfg, "THEMATIC", "LONGFORM_SPECIAL")
    if tools["contract"] != current_contract:
        raise ValueError("Longform receipt current contract differs from current repository")
    # F1: the public receipt replay itself reloads the persisted review.
    review_file = _safe(root, receipt["semantic_review"]["path"], "persisted semantic review")
    validated_review = surface_gate.load_and_validate_reader_surface_semantic_review(
        root,
        review_file,
        expected_issue_id=receipt["issue_id"],
        expected_publication_profile="LONGFORM_SPECIAL",
        require_pass=True,
    )
    if {"path": _rel(root, review_file), "sha256": core.sha256_file(review_file)} != receipt["semantic_review"]:
        raise ValueError("Longform receipt semantic review mismatch")
    if {"path": validated_review["surface_path"], "sha256": validated_review["surface_sha256"]} != receipt["reviewed_reader_input"]:
        raise ValueError("Longform receipt reviewed target mismatch")
    context = longform.load_derivation_for_readback(
        root, state_file, _safe(root, authored["publication-semantic-input"]["path"], "authored input")
    )
    if context["state"]["issue_id"] != receipt["issue_id"]:
        raise ValueError("Longform source receipt issue identity mismatch")
    if authored["drafting-authored-archive"] != _artifact(root, "drafting-authored-archive", context["archive_path"]):
        raise ValueError("Longform receipt drafting archive differs from actual loaded archive")
    if context["accepted_refs"] != receipt["accepted_refs"]:
        raise ValueError("Longform receipt accepted authority differs from current checkpoint chain")
    expected_outputs = {
        "primary": "main.tex", "bibliography": "references.bib", "style": "jgaisurvey.sty",
    }
    survey_relative = Path(context["profile"]["paths"]["survey_root"])
    for role, filename in expected_outputs.items():
        canonical = (survey_relative / filename).as_posix()
        if receipt["outputs"][role]["path"] != canonical:
            raise ValueError(f"Longform receipt {role} output path is not canonical survey_root/{filename}")
    validate_survey_build_directory(root, context["profile"]["paths"]["survey_root"])
    surface_path = _safe(root, receipt["reviewed_reader_input"]["path"], "reviewed reader input")
    if core.sha256_file(surface_path) != receipt["reviewed_reader_input"]["sha256"]:
        raise ValueError("Longform reviewed reader input drift")
    reviewed = longform.validate_longform_reader_input(root, surface_path)
    if context["surface"] != reviewed:
        raise ValueError("Longform independently recomputed reader input differs from reviewed bytes")
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
        path = _safe(root, row["path"], f"Longform {name} output")
        if path.read_bytes() != data or core.sha256_bytes(data) != row["sha256"]:
            raise ValueError(f"Longform deterministic {name} replay mismatch")
    return receipt
