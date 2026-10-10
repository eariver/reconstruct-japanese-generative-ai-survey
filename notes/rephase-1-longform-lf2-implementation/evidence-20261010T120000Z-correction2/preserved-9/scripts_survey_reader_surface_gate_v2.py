#!/usr/bin/env python3
"""Pre-Publication Reader-Surface Gate for Survey Production Core v2.

This module enforces a strict, fail-fast boundary between internal Core v2
production/architecture/screening/review metadata and reader-facing publication
prose. It executes before expensive TeX/layout materialization, LuaLaTeX PDF
compilation, and candidate assembly.

The gate operates across two complementary layers on reader-facing fields only:
1. Deterministic Lexical Lint: scans reader-facing text (TeX body blocks,
   headings, bibliography fields, publication payloads, reader manuscript
   details) for prohibited internal vocabulary, stage names, pipeline
   operations, and repository-internal identifiers.
2. Bounded Semantic Review: validates machine-checkable review contracts
   ensuring no reader-facing sentence requires internal production pipeline
   knowledge to make sense to an ordinary technical reader.

A narrow, audited suppression mechanism allows legitimate technical discussion
of similarly named external concepts without globally disabling protection.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from scripts import survey_production_v2 as core
from scripts import survey_reader_fidelity_v2 as fidelity
from scripts import survey_schema_v2 as schema_gate

SURFACE_GATE_SCHEMA = Path("schemas/reader-surface-gate-v2.schema.json")
MANUSCRIPT_SCHEMA = Path("schemas/reader-manuscript-v2.schema.json")
SURFACE_INPUT_SCHEMA = Path("schemas/reader-surface-input-v2.schema.json")
SEMANTIC_REVIEW_SCHEMA = Path("schemas/reader-surface-semantic-review-v2.schema.json")


@dataclass(frozen=True)
class RuleDefinition:
    rule_id: str
    layer: str  # "LEXICAL_LINT" | "SEMANTIC_REVIEW"
    description: str
    severity: str  # "BLOCKING" | "WARNING"


@dataclass(frozen=True)
class SurfaceFinding:
    finding_id: str
    rule_id: str
    artifact: str
    path: str
    field_or_block: str
    locator: str
    text_span: str
    severity: str  # "BLOCKING" | "WARNING" | "INFO" | "SUPPRESSED"
    reason: str
    proposed_normalization: str
    disposition: str  # "UNRESOLVED" | "SUPPRESSED" | "NORMALIZED"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


RULES: list[RuleDefinition] = [
    RuleDefinition(
        rule_id="RSG-LEX-CORE-VOCAB",
        layer="LEXICAL_LINT",
        description="Core v2 pipeline and architecture internal terminology in reader-facing prose",
        severity="BLOCKING",
    ),
    RuleDefinition(
        rule_id="RSG-LEX-SELECTION-SCREENING",
        layer="LEXICAL_LINT",
        description="Candidate screening, selection rounds, and negative selection decisions in reader prose",
        severity="BLOCKING",
    ),
    RuleDefinition(
        rule_id="RSG-LEX-DISCOVERY-INTAKE",
        layer="LEXICAL_LINT",
        description="Discovery intake, observation metadata, and candidate reviews in reader prose",
        severity="BLOCKING",
    ),
    RuleDefinition(
        rule_id="RSG-LEX-VERIFICATION-MATERIALITY",
        layer="LEXICAL_LINT",
        description="Internal verification obligations and materiality markers in reader prose",
        severity="BLOCKING",
    ),
    RuleDefinition(
        rule_id="RSG-LEX-INTERNAL-IDENTIFIERS",
        layer="LEXICAL_LINT",
        description="Internal package identifiers and raw evidence IDs in reader prose",
        severity="BLOCKING",
    ),
    RuleDefinition(
        rule_id="RSG-LEX-STAGE-LIFECYCLE",
        layer="LEXICAL_LINT",
        description="Internal stage and checkpoint lifecycle names used as publication prose",
        severity="BLOCKING",
    ),
    RuleDefinition(
        rule_id="RSG-LEX-INTERNAL-PATHS",
        layer="LEXICAL_LINT",
        description="Internal repository, transport, or Grok paths in reader prose or URLs",
        severity="BLOCKING",
    ),
    RuleDefinition(
        rule_id="RSG-LEX-BIBLIOGRAPHY-LEAKAGE",
        layer="LEXICAL_LINT",
        description="Internal evidence tags and materiality leaked into bibliography records",
        severity="BLOCKING",
    ),
    RuleDefinition(
        rule_id="RSG-LEX-EDITORIAL-PROCESS",
        layer="LEXICAL_LINT",
        description="Internal editorial operations explained as prose rather than underlying facts",
        severity="BLOCKING",
    ),
    RuleDefinition(
        rule_id="RSG-LEX-REVIEW-RATIONALE-COP-OUT",
        layer="LEXICAL_LINT",
        description="Architecture review meta-rebuttals and cop-out coverage assertions",
        severity="BLOCKING",
    ),
    RuleDefinition(
        rule_id="RSG-SEM-PROCESS-LEAKAGE",
        layer="SEMANTIC_REVIEW",
        description="Reader-facing sentence requiring internal pipeline knowledge to make sense",
        severity="BLOCKING",
    ),
]

RULE_BY_ID = {rule.rule_id: rule for rule in RULES}

# Patterns for lexical lint
# Each entry is (rule_id, regex_pattern, default_reason, normalization_hint)
LEXICAL_PATTERNS: list[tuple[str, re.Pattern[str], str, str]] = [
    # RSG-LEX-CORE-VOCAB
    (
        "RSG-LEX-CORE-VOCAB",
        re.compile(r"承認済み\s*Architecture", re.IGNORECASE),
        "Leaks internal approved Architecture status into reader prose",
        "Explain the survey structure or topic directly without citing approval state",
    ),
    (
        "RSG-LEX-CORE-VOCAB",
        re.compile(r"\bapproved\s+architecture\b", re.IGNORECASE),
        "Leaks internal Architecture approval phrasing into reader prose",
        "State the editorial focus or topic structure directly",
    ),
    (
        "RSG-LEX-CORE-VOCAB",
        re.compile(r"Core\s*v2\s*contract", re.IGNORECASE),
        "Leaks Core v2 contract into reader prose",
        "Remove pipeline contract reference",
    ),
    (
        "RSG-LEX-CORE-VOCAB",
        re.compile(r"Core\s*v2\s*Evidence", re.IGNORECASE),
        "Leaks Core v2 Evidence terminology into reader prose",
        "Refer to the underlying sources or factual claims directly",
    ),
    (
        "RSG-LEX-CORE-VOCAB",
        re.compile(r"\bCore\s+v2\b", re.IGNORECASE),
        "Leaks Core v2 repository engine name into reader prose",
        "Remove Core v2 reference from publication text",
    ),
    (
        "RSG-LEX-CORE-VOCAB",
        re.compile(r"Evidence\s+Card", re.IGNORECASE),
        "Leaks internal Evidence Card artifact name into reader prose",
        "Refer to primary documentation or vendor specifications",
    ),
    (
        "RSG-LEX-CORE-VOCAB",
        re.compile(r"本\s*Evidence"),
        "Leaks internal Evidence artifact reference into reader prose",
        "Refer to the source, benchmark, or announcement directly",
    ),
    (
        "RSG-LEX-CORE-VOCAB",
        re.compile(r"Evidence\s+pass", re.IGNORECASE),
        "Leaks internal Evidence pass evaluation into reader prose",
        "State the verified technical findings directly",
    ),
    (
        "RSG-LEX-CORE-VOCAB",
        re.compile(r"Selection\s*済み\s*Evidence"),
        "Leaks Selection-bound Evidence metadata into reader prose",
        "Discuss the selected systems or models on their factual merits",
    ),
    (
        "RSG-LEX-CORE-VOCAB",
        re.compile(r"\bnormalized\s+claim\b", re.IGNORECASE),
        "Leaks internal claim normalization vocabulary into reader prose",
        "State the claim in natural reader-facing prose",
    ),
    (
        "RSG-LEX-CORE-VOCAB",
        re.compile(r"\bSource-bound\s+record\b", re.IGNORECASE),
        "Leaks internal record binding phrase into reader prose",
        "Describe the source materials directly",
    ),
    (
        "RSG-LEX-CORE-VOCAB",
        re.compile(r"\bThis\s+retained\s+evidence\s+note\b", re.IGNORECASE),
        "Leaks internal retained evidence phrasing into reader prose",
        "Frame as an observation or limitation on available data",
    ),
    (
        "RSG-LEX-CORE-VOCAB",
        re.compile(r"\bThe\s+bound\s+[A-Za-z0-9_-]+", re.IGNORECASE),
        "Leaks internal binding phrasing into reader prose",
        "Describe the referenced entity naturally",
    ),

    # RSG-LEX-SELECTION-SCREENING
    (
        "RSG-LEX-SELECTION-SCREENING",
        re.compile(r"(?<![A-Za-z0-9])Selection\s+r\d+(?![A-Za-z0-9])", re.IGNORECASE),
        "Leaks internal Selection revision round (e.g. Selection r2) into reader prose",
        "Remove selection round reference and discuss the topic directly",
    ),
    (
        "RSG-LEX-SELECTION-SCREENING",
        re.compile(r"Candidate\s+Selection", re.IGNORECASE),
        "Leaks internal Candidate Selection stage name into reader prose",
        "Discuss selected developments directly",
    ),
    (
        "RSG-LEX-SELECTION-SCREENING",
        re.compile(r"Selection\s*済み"),
        "Leaks internal Selection state into reader prose",
        "Refer to surveyed or featured developments",
    ),
    (
        "RSG-LEX-SELECTION-SCREENING",
        re.compile(r"(?:一次|二次)?Screening\s*(?:で|段階|passed|判定|において|結果|を通過|済み|落ち)"),
        "Leaks internal screening pipeline stage into reader prose",
        "Discuss inclusion scope or criteria substantively",
    ),
    (
        "RSG-LEX-SELECTION-SCREENING",
        re.compile(r"(?<![A-Za-z0-9])(?:candidate|evidence|source)\s+screening(?![A-Za-z0-9])", re.IGNORECASE),
        "Leaks candidate screening pipeline concept into reader prose",
        "Discuss editorial scope or research methodology in reader-facing terms",
    ),
    (
        "RSG-LEX-SELECTION-SCREENING",
        re.compile(r"(?<![A-Za-z0-9])DROP\s*(?:判定|とした|と判定|された|扱い|理由)"),
        "Leaks internal DROP candidate disposition into reader prose",
        "Explain non-inclusion through scope boundaries or lack of public data",
    ),
    (
        "RSG-LEX-SELECTION-SCREENING",
        re.compile(r"(?<![A-Za-z0-9_])HOLD_OUT(?:_ONLY)?(?![A-Za-z0-9_])"),
        "Leaks internal HOLD_OUT candidate disposition enum into reader prose",
        "Describe ongoing monitoring or future observation focus",
    ),
    (
        "RSG-LEX-SELECTION-SCREENING",
        re.compile(r"(?<![A-Za-z0-9_])SOCIAL_OBSERVATION(?:_ONLY)?(?![A-Za-z0-9_])"),
        "Leaks internal SOCIAL_OBSERVATION enum into reader prose",
        "Describe community discussion or social reception naturally",
    ),

    # RSG-LEX-DISCOVERY-INTAKE
    (
        "RSG-LEX-DISCOVERY-INTAKE",
        re.compile(r"(?<![A-Za-z0-9])Discovery\s+observation(?![A-Za-z0-9])", re.IGNORECASE),
        "Leaks internal Discovery observation terminology into reader prose",
        "Attribute observations to public posts, repository activity, or changelogs",
    ),
    (
        "RSG-LEX-DISCOVERY-INTAKE",
        re.compile(r"(?<![A-Za-z0-9])Discovery\s+sources?(?![A-Za-z0-9])", re.IGNORECASE),
        "Leaks internal Discovery sources terminology into reader prose",
        "Cite the specific public sources directly",
    ),
    (
        "RSG-LEX-DISCOVERY-INTAKE",
        re.compile(r"(?<![A-Za-z0-9])Discovery\s+ID(?![A-Za-z0-9])", re.IGNORECASE),
        "Leaks Discovery identifier label into reader prose",
        "Cite the public source by author and title",
    ),
    (
        "RSG-LEX-DISCOVERY-INTAKE",
        re.compile(r"(?<![A-Za-z0-9])candidate-specific\s+review(?![A-Za-z0-9])", re.IGNORECASE),
        "Leaks candidate-specific review terminology into reader prose",
        "Discuss the system properties directly without referencing review tasks",
    ),

    # RSG-LEX-VERIFICATION-MATERIALITY
    (
        "RSG-LEX-VERIFICATION-MATERIALITY",
        re.compile(r"(?<![A-Za-z0-9])materiality:\s*", re.IGNORECASE),
        "Leaks internal materiality ledger tag into reader prose",
        "Explain the practical significance of the development directly",
    ),
    (
        "RSG-LEX-VERIFICATION-MATERIALITY",
        re.compile(r"Core\s*v2\s*Evidence:\s*", re.IGNORECASE),
        "Leaks internal Core v2 Evidence status prefix into reader prose",
        "Remove internal verification prefix",
    ),
    (
        "RSG-LEX-VERIFICATION-MATERIALITY",
        re.compile(r"(?<![A-Za-z0-9])Verify\s+[A-Za-z0-9_-]+", re.IGNORECASE),
        "Leaks internal verification obligation prose into reader prose",
        "State verified findings or noted limits without raw 'Verify ...' imperative",
    ),

    # RSG-LEX-INTERNAL-IDENTIFIERS
    (
        "RSG-LEX-INTERNAL-IDENTIFIERS",
        re.compile(r"(?<![A-Za-z0-9])Package\s+\d+(?![A-Za-z0-9])"),
        "Leaks internal Package number (e.g. Package 4) into reader prose",
        "Refer to the section or thematic topic by title rather than package number",
    ),
    (
        "RSG-LEX-INTERNAL-IDENTIFIERS",
        re.compile(r"本\s*package(?![A-Za-z0-9])", re.IGNORECASE),
        "Leaks internal package reference ('本 package') into reader prose",
        "Refer to '本節' (this section) or the specific topic name",
    ),
    (
        "RSG-LEX-INTERNAL-IDENTIFIERS",
        re.compile(r"本パッケージ(?![A-Za-z0-9])"),
        "Leaks internal package reference ('本パッケージ') into reader prose",
        "Refer to '本節' (this section) or the specific topic name",
    ),
    (
        "RSG-LEX-INTERNAL-IDENTIFIERS",
        re.compile(r"(?<![A-Za-z0-9._-])[A-Za-z0-9._-]+-D\d{3,}(?![A-Za-z0-9._-])"),
        "Leaks repository-internal Discovery identifier into reader prose",
        "Use public citations (\\cite) or name the source publication directly",
    ),
    (
        "RSG-LEX-INTERNAL-IDENTIFIERS",
        re.compile(r"(?<![A-Za-z0-9])D\d{3,}(?![A-Za-z0-9])"),
        "Leaks short internal Evidence/Discovery identifier (e.g. D017, D021) into reader prose",
        "Distinguish claims by source type (e.g. technical spec vs license) instead of internal IDs",
    ),

    # RSG-LEX-STAGE-LIFECYCLE
    (
        "RSG-LEX-STAGE-LIFECYCLE",
        re.compile(
            r"(?<![A-Za-z0-9_])(?:ISSUE_INITIALIZED|DISCOVERY_COLLECTED|CANDIDATES_NORMALIZED|"
            r"EVIDENCE_REVIEWED|SELECTION_COMPLETE|ARCHITECTURE_ESTABLISHED|"
            r"DRAFT_COMPLETE|VALIDATED_DRAFT|RELEASE_CANDIDATE)(?![A-Za-z0-9_])"
        ),
        "Leaks internal lifecycle stage enum into reader prose",
        "Remove internal stage name from publication text",
    ),

    # RSG-LEX-INTERNAL-PATHS
    (
        "RSG-LEX-INTERNAL-PATHS",
        re.compile(r"/tmp/[A-Za-z0-9._/-]+"),
        "Leaks temporary executor path into reader prose or URLs",
        "Use repository-stable or public canonical URLs",
    ),
    (
        "RSG-LEX-INTERNAL-PATHS",
        re.compile(r"sources/(?:2026-W\d+|SP\d+)/[A-Za-z0-9._/-]*"),
        "Leaks repository internal sources/ path into reader prose or URLs",
        "Use public web URLs or omit internal paths from reader prose",
    ),
    (
        "RSG-LEX-INTERNAL-PATHS",
        re.compile(r"surveys/(?:weekly|special)/[A-Za-z0-9._/-]*"),
        "Leaks repository internal surveys/ path into reader prose or URLs",
        "Use public web URLs or omit internal paths from reader prose",
    ),
    (
        "RSG-LEX-INTERNAL-PATHS",
        re.compile(r"grok/sources/[A-Za-z0-9._/-]*", re.IGNORECASE),
        "Leaks internal Grok intake path into reader prose or URLs",
        "Use public post URLs",
    ),

    # RSG-LEX-BIBLIOGRAPHY-LEAKAGE
    (
        "RSG-LEX-BIBLIOGRAPHY-LEAKAGE",
        re.compile(r"Evidence\s+tags?:", re.IGNORECASE),
        "Leaks internal Evidence tags label into bibliography",
        "Bibliography entries must contain public bibliographic metadata only",
    ),
    (
        "RSG-LEX-BIBLIOGRAPHY-LEAKAGE",
        re.compile(r"\[[VPMCHE]/[VPMCHE]\]"),
        "Leaks internal evidence/materiality matrix tag (e.g. [V/M]) into bibliography",
        "Retain classification in internal ledgers; do not serialize into BibTeX",
    ),

    # RSG-LEX-EDITORIAL-PROCESS
    (
        "RSG-LEX-EDITORIAL-PROCESS",
        re.compile(r"一次資料(?:として|へ)?昇格させない"),
        "Explains internal evidence promotion operation rather than facts",
        "State that findings are based on community testing rather than vendor documentation",
    ),
    (
        "RSG-LEX-EDITORIAL-PROCESS",
        re.compile(r"一次資料(?:として|へ)?昇格"),
        "Discusses evidence promotion process rather than the factual development",
        "Describe the source's authority and scope directly",
    ),
    (
        "RSG-LEX-EDITORIAL-PROCESS",
        re.compile(r"coverage\s*を(?:広げる|拡大|狭める|制限)"),
        "Discusses internal coverage expansion/contraction rather than domain facts",
        "State the scope of analyzed systems directly",
    ),
    (
        "RSG-LEX-EDITORIAL-PROCESS",
        re.compile(r"カバレッジを(?:広げる|拡大|狭める|制限)"),
        "Discusses internal coverage operations rather than domain facts",
        "State the scope of analyzed systems directly",
    ),
    (
        "RSG-LEX-EDITORIAL-PROCESS",
        re.compile(r"本\s*package\s*では"),
        "Uses internal package packaging phrasing to frame content",
        "Use '本節では' or frame by subject matter directly",
    ),

    # RSG-LEX-REVIEW-RATIONALE-COP-OUT
    (
        "RSG-LEX-REVIEW-RATIONALE-COP-OUT",
        re.compile(r"W\d+は三つの(?:Feature|トピック|話題)だけではない"),
        "Meta-rebuttal to prior Architecture Review comment serialized into reader prose",
        "Directly present the multifaceted developments without referencing earlier drafts",
    ),
    (
        "RSG-LEX-REVIEW-RATIONALE-COP-OUT",
        re.compile(r"\bnot\s+a\s+three-story\s+week\b", re.IGNORECASE),
        "Meta-rebuttal to prior Architecture Review comment serialized into reader prose",
        "Present the breadth of developments directly without arguing against prior scope",
    ),
    (
        "RSG-LEX-REVIEW-RATIONALE-COP-OUT",
        re.compile(r"(?:前回の|Reviewでの|レビューでの|Architecture\s*Reviewでの)指摘(?:を|に|により|を受けて|に基づき)"),
        "Serializes internal review feedback history into publication prose",
        "State the established analysis directly without referencing review feedback",
    ),
    (
        "RSG-LEX-REVIEW-RATIONALE-COP-OUT",
        re.compile(r"Architecture\s*(?:requires|要求|は.*を観察軸としている|の要求)"),
        "Asserts Architecture requirement as a cop-out rather than explaining content",
        "Explain the technical mechanisms, tradeoffs, and findings substantively",
    ),
]


def _resolve_repo_path(repo_root: Path, path: Path | str, label: str) -> tuple[Path, str]:
    root = repo_root.resolve()
    p = Path(path)
    if not p.is_absolute():
        p = root / p
    resolved = p.resolve()
    try:
        rel = str(resolved.relative_to(root)).replace("\\", "/")
    except ValueError as exc:
        raise ValueError(f"{label} escapes repository root: {path}") from exc
    safe_path = core.repo_local_path(repo_root, rel, label)
    return safe_path, rel


def _rel(repo_root: Path, path: Path | str) -> str:
    _, rel = _resolve_repo_path(repo_root, path, "path")
    return rel


def _safe_file(repo_root: Path, path: Path | str, label: str) -> Path:
    safe_path, rel = _resolve_repo_path(repo_root, path, label)
    if safe_path.is_symlink() or not safe_path.is_file():
        raise ValueError(f"{label} missing or unsafe: {rel}")
    return safe_path


def _iso_or_now(val: datetime | str | None) -> str:
    if isinstance(val, str):
        return val
    if isinstance(val, datetime):
        return core.iso_utc(val)
    return core.iso_utc(datetime.now(timezone.utc))


def mask_tex_comments_and_structural_macros(source_text: str) -> tuple[str, list[str]]:
    """Mask TeX comments and purely structural non-reader commands.

    Preserves exact offsets, line breaks, section/subsection titles, kickers,
    and visible paragraph/body text. Masks out LaTeX macro declarations that
    contain internal technical keys (e.g. \\label{pkg:...}, \\cite{...},
    \\Needspace{...}, \\usepackage{...}, \\input{...}) so citation keys and
    cross-reference labels do not trigger false positive lexical matches,
    while scanning all visible reader prose.
    """
    # 1. Mask % comments
    masked = list(fidelity._mask_tex_comments(source_text))

    text = "".join(masked)
    # 2. Mask purely structural non-reader commands
    structural_patterns = [
        re.compile(r"\\label\{[^{}]*\}"),
        re.compile(r"\\(?:auto|text|paren)?cite\w*\{[^{}]*\}"),
        re.compile(r"\\Needspace\{[^{}]*\}"),
        re.compile(r"\\documentclass(?:\[[^\]]*\])?\{[^{}]*\}"),
        re.compile(r"\\usepackage(?:\[[^\]]*\])?\{[^{}]*\}"),
        re.compile(r"\\bibliography\{[^{}]*\}"),
        re.compile(r"\\addbibresource\{[^{}]*\}"),
        re.compile(r"\\input\{[^{}]*\}"),
        re.compile(r"\\include\{[^{}]*\}"),
        re.compile(r"\\pagestyle\{[^{}]*\}"),
        re.compile(r"\\thispagestyle\{[^{}]*\}"),
        re.compile(r"\\bibliographystyle\{[^{}]*\}"),
        re.compile(r"\\ref\{[^{}]*\}"),
        re.compile(r"\\pageref\{[^{}]*\}"),
    ]

    for pat in structural_patterns:
        for match in pat.finditer(text):
            start, end = match.span()
            for i in range(start, end):
                if masked[i] not in "\r\n":
                    masked[i] = " "

    result = "".join(masked)
    lines = result.splitlines(keepends=True)
    return result, lines


def _is_suppressed(
    suppressions: list[dict[str, Any]],
    rule_id: str,
    path: str,
    matched_text: str,
) -> tuple[bool, str]:
    for sup in suppressions:
        if not isinstance(sup, dict):
            continue
        if sup.get("rule_id") == rule_id and sup.get("path") == path:
            target = sup.get("matched_text", "")
            if target and (target in matched_text or matched_text in target):
                reason = sup.get("reason", "").strip()
                if reason:
                    return True, reason
    return False, ""


def scan_reader_text_lines(
    lines: list[str],
    artifact_label: str,
    path_str: str,
    suppressions: list[dict[str, Any]] | None = None,
    block_context: str | None = None,
) -> list[SurfaceFinding]:
    """Scan line-split reader text for lexical lint violations."""
    active_suppressions = suppressions or []
    findings: list[SurfaceFinding] = []
    finding_counter = 0

    current_block = block_context or "body"

    for line_idx, line in enumerate(lines, start=1):
        # Update current block context if heading is detected
        heading_match = re.search(r"\\(?:section|subsection|subsubsection)\*?\{([^}]+)\}", line)
        if heading_match:
            current_block = heading_match.group(1).strip()

        for rule_id, pattern, default_reason, norm_hint in LEXICAL_PATTERNS:
            for match in pattern.finditer(line):
                matched_span = match.group(0)
                finding_counter += 1
                fid = f"{rule_id}-{path_str}-{line_idx}-{finding_counter}"

                suppressed, sup_reason = _is_suppressed(
                    active_suppressions, rule_id, path_str, matched_span
                )

                if suppressed:
                    findings.append(
                        SurfaceFinding(
                            finding_id=fid,
                            rule_id=rule_id,
                            artifact=artifact_label,
                            path=path_str,
                            field_or_block=current_block,
                            locator=f"Line {line_idx}",
                            text_span=matched_span,
                            severity="SUPPRESSED",
                            reason=f"Suppressed: {sup_reason}",
                            proposed_normalization=norm_hint,
                            disposition="SUPPRESSED",
                        )
                    )
                else:
                    findings.append(
                        SurfaceFinding(
                            finding_id=fid,
                            rule_id=rule_id,
                            artifact=artifact_label,
                            path=path_str,
                            field_or_block=current_block,
                            locator=f"Line {line_idx}",
                            text_span=matched_span,
                            severity="BLOCKING",
                            reason=default_reason,
                            proposed_normalization=norm_hint,
                            disposition="UNRESOLVED",
                        )
                    )
    return findings


def scan_tex_file(
    repo_root: Path,
    file_path: Path,
    suppressions: list[dict[str, Any]] | None = None,
    artifact_label: str = "TeX Source",
) -> list[SurfaceFinding]:
    """Scan one TeX source file for reader-surface leakage."""
    resolved = _safe_file(repo_root, file_path, artifact_label)
    rel_path = _rel(repo_root, resolved)
    text = resolved.read_text(encoding="utf-8")
    _, lines = mask_tex_comments_and_structural_macros(text)
    return scan_reader_text_lines(
        lines, artifact_label, rel_path, suppressions=suppressions
    )


def scan_bib_file(
    repo_root: Path,
    file_path: Path,
    suppressions: list[dict[str, Any]] | None = None,
    artifact_label: str = "Bibliography",
) -> list[SurfaceFinding]:
    """Scan a BibTeX bibliography file for leaked evidence metadata."""
    resolved = _safe_file(repo_root, file_path, artifact_label)
    rel_path = _rel(repo_root, resolved)
    text = resolved.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    active_suppressions = suppressions or []
    findings: list[SurfaceFinding] = []
    finding_counter = 0

    entry_key = "preamble"
    for line_idx, line in enumerate(lines, start=1):
        # Detect @entry{key,
        entry_match = re.search(r"@\w+\s*\{\s*([^,]+),", line)
        if entry_match:
            entry_key = entry_match.group(1).strip()

        # Check all lexical patterns against bibliography lines
        for rule_id, pattern, default_reason, norm_hint in LEXICAL_PATTERNS:
            for match in pattern.finditer(line):
                matched_span = match.group(0)
                finding_counter += 1
                fid = f"{rule_id}-{rel_path}-{line_idx}-{finding_counter}"

                suppressed, sup_reason = _is_suppressed(
                    active_suppressions, rule_id, rel_path, matched_span
                )

                if suppressed:
                    findings.append(
                        SurfaceFinding(
                            finding_id=fid,
                            rule_id=rule_id,
                            artifact=artifact_label,
                            path=rel_path,
                            field_or_block=f"entry:{entry_key}",
                            locator=f"Line {line_idx}",
                            text_span=matched_span,
                            severity="SUPPRESSED",
                            reason=f"Suppressed: {sup_reason}",
                            proposed_normalization=norm_hint,
                            disposition="SUPPRESSED",
                        )
                    )
                else:
                    findings.append(
                        SurfaceFinding(
                            finding_id=fid,
                            rule_id=rule_id,
                            artifact=artifact_label,
                            path=rel_path,
                            field_or_block=f"entry:{entry_key}",
                            locator=f"Line {line_idx}",
                            text_span=matched_span,
                            severity="BLOCKING",
                            reason=default_reason,
                            proposed_normalization=norm_hint,
                            disposition="UNRESOLVED",
                        )
                    )
    return findings


def scan_publication_payload(
    payload: dict[str, Any],
    source_path_str: str,
    suppressions: list[dict[str, Any]] | None = None,
) -> list[SurfaceFinding]:
    """Scan publication_payload text fields in Profile Synthesis."""
    findings: list[SurfaceFinding] = []
    finding_counter = 0
    active_suppressions = suppressions or []

    def _walk(obj: Any, prefix: str) -> None:
        nonlocal finding_counter
        if isinstance(obj, str):
            for rule_id, pattern, default_reason, norm_hint in LEXICAL_PATTERNS:
                for match in pattern.finditer(obj):
                    matched_span = match.group(0)
                    finding_counter += 1
                    fid = f"{rule_id}-synthesis-{prefix}-{finding_counter}"
                    suppressed, sup_reason = _is_suppressed(
                        active_suppressions, rule_id, source_path_str, matched_span
                    )
                    findings.append(
                        SurfaceFinding(
                            finding_id=fid,
                            rule_id=rule_id,
                            artifact="Profile Synthesis Result",
                            path=source_path_str,
                            field_or_block=prefix,
                            locator=prefix,
                            text_span=matched_span,
                            severity="SUPPRESSED" if suppressed else "BLOCKING",
                            reason=f"Suppressed: {sup_reason}" if suppressed else default_reason,
                            proposed_normalization=norm_hint,
                            disposition="SUPPRESSED" if suppressed else "UNRESOLVED",
                        )
                    )
        elif isinstance(obj, dict):
            for k, v in obj.items():
                _walk(v, f"{prefix}.{k}" if prefix else k)
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                _walk(item, f"{prefix}[{idx}]")

    _walk(payload, "publication_payload")
    return findings


def scan_structured_reader_surface(
    payload: dict[str, Any],
    source_label: str,
    *,
    suppressions: list[dict[str, Any]] | None = None,
) -> list[SurfaceFinding]:
    """Scan canonical structured pre-TeX reader surface fields for prohibited internal metadata."""
    findings: list[SurfaceFinding] = []
    if payload.get("route") == "LONGFORM_GENERATED_V1":
        # Longform branch: walk the defined reader schema's actual display
        # strings and citation representations (including bibliography and all
        # visible constants). Internal identifiers (package_id, discovery_ids,
        # bibliography keys, route/format/Profile markers) are never scanned
        # as prose.
        fields: list[tuple[str, str]] = []
        for group in ("issue_metadata", "visible_text"):
            for key, value in payload.get(group, {}).items():
                fields.append((f"{group}:{key}", str(value)))
        cover = payload.get("cover", {})
        for key in ("headline", "deck"):
            fields.append((f"cover:{key}", str(cover.get(key, ""))))
        fields.extend(
            (f"cover:anchors:{idx+1}", str(item))
            for idx, item in enumerate(cover.get("anchors", []))
        )
        front = payload.get("frontmatter", {})
        for key in ("heading", "lede"):
            fields.append((f"frontmatter:{key}", str(front.get(key, ""))))
        fields.extend(
            (f"frontmatter:scope_notes:{idx+1}", str(item))
            for idx, item in enumerate(front.get("scope_notes", []))
        )
        for idx, package in enumerate(payload.get("packages", [])):
            tag = f"package:{idx+1}"
            for key in ("headline", "deck", "kicker"):
                fields.append((f"{tag}:{key}", str(package.get(key, ""))))
            for gidx, cell in enumerate(package.get("theme_at_a_glance", [])):
                for key in ("label", "text"):
                    fields.append((f"{tag}:glance:{gidx+1}:{key}", str(cell.get(key, ""))))
            for sidx, section in enumerate(package.get("narrative_sections", [])):
                fields.append((f"{tag}:narrative:{sidx+1}:heading", str(section.get("heading", ""))))
                for pidx, para in enumerate(section.get("paragraphs", [])):
                    fields.append((f"{tag}:narrative:{sidx+1}:p{pidx+1}", str(para.get("text", ""))))
            for tidx, cell in enumerate(package.get("timeline", [])):
                for key in ("label", "text"):
                    fields.append((f"{tag}:timeline:{tidx+1}:{key}", str(cell.get(key, ""))))
            synthesis = package.get("synthesis", {})
            fields.append((f"{tag}:synthesis:heading", str(synthesis.get("heading", ""))))
            for pidx, para in enumerate(synthesis.get("paragraphs", [])):
                fields.append((f"{tag}:synthesis:p{pidx+1}", str(para.get("text", ""))))
            for bidx, para in enumerate(package.get("reader_claim_boundary", [])):
                fields.append((f"{tag}:boundary:{bidx+1}", str(para.get("text", ""))))
            for nidx, note in enumerate(package.get("technical_notes", [])):
                ntag = f"{tag}:note:{nidx+1}"
                for key in ("title", "chronology", "limitation", "primary_url"):
                    fields.append((f"{ntag}:{key}", str(note.get(key, ""))))
                fields.extend(
                    (f"{ntag}:point:{pidx+1}", str(point))
                    for pidx, point in enumerate(note.get("technical_points", []))
                )
        cross = payload.get("cross_family_synthesis", {})
        fields.append(("cross:heading", str(cross.get("heading", ""))))
        for pidx, para in enumerate(cross.get("paragraphs", [])):
            fields.append((f"cross:p{pidx+1}", str(para.get("text", ""))))
        for ridx, row in enumerate(cross.get("comparison_rows", [])):
            for key in ("dimension", "glm", "qwen", "deepseek", "kimi"):
                fields.append((f"cross:row:{ridx+1}:{key}", str(row.get(key, ""))))
        summary = payload.get("final_summary", {})
        fields.append(("final_summary:heading", str(summary.get("heading", ""))))
        fields.extend(
            (f"final_summary:p{idx+1}", str(item))
            for idx, item in enumerate(summary.get("paragraphs", []))
        )
        for idx, row in enumerate(payload.get("bibliography", [])):
            for key in ("title", "author", "url", "urldate"):
                fields.append((f"bibliography:{idx+1}:{key}", str(row.get(key, ""))))
        for locator, value in fields:
            findings.extend(scan_reader_text_lines(
                [value], "Structured Longform Reader Surface", source_label,
                suppressions=suppressions, block_context=locator,
            ))
        return findings
    if payload.get("route") == "WEEKLY_GENERATED_V2":
        fields: list[tuple[str, str]] = []
        fields.extend((f"issue_metadata:{key}", str(value)) for key, value in payload["issue_metadata"].items())
        fields.extend((f"visible_text:{key}", str(value)) for key, value in payload["visible_text"].items())
        for group in ("cover", "frontmatter", "final_summary"):
            for key, value in payload[group].items():
                if isinstance(value, list):
                    fields.extend((f"{group}:{key}:{idx+1}", str(item)) for idx, item in enumerate(value))
                else:
                    fields.append((f"{group}:{key}", str(value)))
        fields.append(("closing_synthesis", payload["closing_synthesis"]))
        for idx, package in enumerate(payload["packages"]):
            for key in ("section_label", "headline", "deck"):
                fields.append((f"package:{idx+1}:{key}", package[key]))
            for bidx, block in enumerate(package["blocks"]):
                fields.append((f"package:{idx+1}:block:{bidx+1}", block["text"]))
        for idx, row in enumerate(payload["bibliography"]):
            for key in ("title", "author", "url", "urldate"):
                fields.append((f"bibliography:{idx+1}:{key}", row[key]))
        for locator, value in fields:
            findings.extend(scan_reader_text_lines(
                [value], "Structured Weekly Reader Surface", source_label,
                suppressions=suppressions, block_context=locator,
            ))
        return findings
    closing = payload.get("closing_synthesis", "")
    if isinstance(closing, str) and closing.strip():
        findings.extend(
            scan_reader_text_lines(
                [closing],
                "Structured Reader Surface (closing_synthesis)",
                source_label,
                suppressions=suppressions,
                block_context="closing_synthesis",
            )
        )
    if payload.get("headline"):
        findings.extend(
            scan_reader_text_lines(
                [str(payload["headline"])],
                "Structured Reader Surface (headline)",
                source_label,
                suppressions=suppressions,
                block_context="headline",
            )
        )
    if payload.get("deck"):
        findings.extend(
            scan_reader_text_lines(
                [str(payload["deck"])],
                "Structured Reader Surface (deck)",
                source_label,
                suppressions=suppressions,
                block_context="deck",
            )
        )
    for idx, p in enumerate(payload.get("final_summary_paragraphs", [])):
        findings.extend(
            scan_reader_text_lines(
                [str(p)],
                f"Structured Reader Surface (final_summary p{idx+1})",
                source_label,
                suppressions=suppressions,
                block_context=f"final_summary:p{idx+1}",
            )
        )
    for pkg in payload.get("packages", []):
        pid = str(pkg.get("package_id", "unknown"))
        if pkg.get("headline"):
            findings.extend(
                scan_reader_text_lines(
                    [str(pkg["headline"])],
                    f"Structured Reader Surface (package {pid} headline)",
                    source_label,
                    suppressions=suppressions,
                    block_context=f"package:{pid}:headline",
                )
            )
        if pkg.get("deck"):
            findings.extend(
                scan_reader_text_lines(
                    [str(pkg["deck"])],
                    f"Structured Reader Surface (package {pid} deck)",
                    source_label,
                    suppressions=suppressions,
                    block_context=f"package:{pid}:deck",
                )
            )
        for b_idx, block in enumerate(pkg.get("blocks", [])):
            bid = str(block.get("block_id", b_idx + 1))
            b_text = str(block.get("text", ""))
            if b_text:
                findings.extend(
                    scan_reader_text_lines(
                        [b_text],
                        f"Structured Reader Surface (package {pid} block {bid})",
                        source_label,
                        suppressions=suppressions,
                        block_context=f"package:{pid}:block:{bid}",
                    )
                )
    return findings


def build_weekly_reader_surface_input(
    repo_root: Path,
    issue_id: str,
    publication_profile: str,
    closing_synthesis: str,
    final_summary_paragraphs: list[str],
    packages: list[dict[str, Any]],
    *,
    headline: str | None = None,
    deck: str | None = None,
    output_path: Path | None = None,
) -> Path:
    """Legacy builder cannot construct the complete Weekly canonical input."""
    raise ValueError(
        "legacy Weekly reader-surface builder is obsolete; use the accepted-authority complete projection"
    )


def load_and_validate_reader_surface_semantic_review(
    repo_root: Path,
    review_path: Path | str,
    *,
    expected_issue_id: str | None = None,
    expected_publication_profile: str | None = None,
    expected_surface_path: Path | str | None = None,
    expected_surface_sha256: str | None = None,
    require_pass: bool = True,
) -> dict[str, Any]:
    """Independently load and validate a persisted semantic review record from disk.

    Enforces all strict Reader-Surface Semantic Review verification rules:
      1. Repository-local regular file exists on disk.
      2. Strictly validates against SEMANTIC_REVIEW_SCHEMA (reader-surface-semantic-review-v2).
         Legacy publication-review-record-v2 fallback is strictly prohibited.
      3. review_kind must be 'SEMANTIC_EDITORIAL'. VISUAL reviews are rejected.
      4. Digest validity: review_sha256 matches recomputation over all fields except review_sha256.
      5. Reviewed surface existence, repository-local path, and unmutated disk bytes SHA-256 match.
      6. Required semantic check 'READER_PIPELINE_INDEPENDENCE' must be present, substantive, and PASS.
      7. All semantic checks must contain non-empty detail and substantive evidence_locations.
      8. If decision == PASS, all checks must have status == 'PASS', and unresolved blocking count == 0.
      9. Identity matches expected_issue_id and expected_publication_profile.
      10. reviewed_by and reviewed_at/recorded_at presence.
    """
    review_file, review_rel = _resolve_repo_path(repo_root, review_path, "semantic review record")
    if not review_file.is_file():
        raise ValueError(f"Semantic review record missing on disk: {review_path}")

    raw = core.load_json(review_file)
    if not isinstance(raw, dict):
        raise ValueError(f"Semantic review record must be a JSON object: {review_path}")

    if "reviewed_surface" not in raw or raw.get("review_kind") != "SEMANTIC_EDITORIAL":
        raise ValueError(
            f"Invalid semantic review record at {review_path}: must be reader-surface-semantic-review-v2 "
            f"with review_kind='SEMANTIC_EDITORIAL'. Legacy publication-review-record-v2 fallback is prohibited."
        )

    schema_gate.validate_instance(
        raw, repo_root / SEMANTIC_REVIEW_SCHEMA, label="Semantic Review Record"
    )
    base = {k: v for k, v in raw.items() if k != "review_sha256"}
    expected_digest = core.sha256_object(base)
    if raw.get("review_sha256") != expected_digest:
        raise ValueError(
            f"Semantic review record digest mismatch: expected {expected_digest}, got {raw.get('review_sha256')}"
        )

    surface_rel = raw["reviewed_surface"]["path"]
    surface_sha = raw["reviewed_surface"]["sha256"]
    decision = raw["decision"]
    status = raw.get("status", "PASSED" if decision == "PASS" else "FAILED")
    findings = raw.get("findings", [])
    unresolved_blocking = sum(
        1 for f in findings
        if f.get("severity") == "BLOCKING"
        and f.get("disposition", "UNRESOLVED") not in ("SUPPRESSED", "NORMALIZED", "RESOLVED")
    )

    # Substantive semantic checks verification
    checks = raw.get("checks", [])
    if not isinstance(checks, list) or not checks:
        raise ValueError("Semantic review record lacks required checks array")

    pipeline_check = None
    for c in checks:
        if c.get("check_id") == "READER_PIPELINE_INDEPENDENCE":
            pipeline_check = c
            break

    if pipeline_check is None:
        raise ValueError(
            "Semantic review record missing required semantic check 'READER_PIPELINE_INDEPENDENCE'"
        )

    for c in checks:
        cid = c.get("check_id")
        detail = c.get("detail", "")
        locs = c.get("evidence_locations", [])
        if not isinstance(detail, str) or not detail.strip():
            raise ValueError(f"Semantic check '{cid}' has empty detail")
        if not isinstance(locs, list) or not locs or not all(isinstance(loc, str) and loc.strip() for loc in locs):
            raise ValueError(f"Semantic check '{cid}' lacks substantive evidence_locations")

    if decision == "PASS":
        if pipeline_check.get("status") != "PASS":
            raise ValueError(
                "Semantic review decision is PASS but required check 'READER_PIPELINE_INDEPENDENCE' status is not PASS"
            )
        failed_checks = [c.get("check_id") for c in checks if c.get("status") != "PASS"]
        if failed_checks:
            raise ValueError(
                f"Semantic review decision is PASS but check(s) failed: {', '.join(failed_checks)}"
            )
        if status != "PASSED":
            raise ValueError(f"Semantic review decision is PASS but status is {status}")

    # Identity checks
    if expected_issue_id is not None and raw.get("issue_id") != expected_issue_id:
        raise ValueError(
            f"Semantic review issue_id mismatch: expected {expected_issue_id}, got {raw.get('issue_id')}"
        )
    if expected_publication_profile is not None and raw.get("publication_profile") != expected_publication_profile:
        raise ValueError(
            f"Semantic review publication_profile mismatch: expected {expected_publication_profile}, got {raw.get('publication_profile')}"
        )

    # Reviewed surface disk verification (stale review check)
    surface_file, _ = _resolve_repo_path(repo_root, surface_rel, f"reviewed surface {surface_rel}")
    if not surface_file.is_file():
        raise ValueError(f"Reviewed surface file missing on disk: {surface_rel}")
    current_disk_sha = core.sha256_file(surface_file)
    if current_disk_sha != surface_sha:
        raise ValueError(
            f"Reviewed surface bytes drifted for {surface_rel}: recorded {surface_sha}, current disk {current_disk_sha}"
        )

    if expected_surface_path is not None:
        _, expected_rel = _resolve_repo_path(repo_root, expected_surface_path, "expected surface")
        if surface_rel != expected_rel:
            raise ValueError(
                f"Reviewed surface path mismatch: expected {expected_rel}, got {surface_rel}"
            )
    if expected_surface_sha256 is not None and surface_sha != expected_surface_sha256:
        raise ValueError(
            f"Reviewed surface SHA-256 mismatch: expected {expected_surface_sha256}, got {surface_sha}"
        )

    # Decision and findings check
    if decision == "PASS" and unresolved_blocking > 0:
        raise ValueError(
            f"Semantic review decision is PASS but contains {unresolved_blocking} unresolved blocking finding(s)"
        )
    if require_pass and (decision != "PASS" or status != "PASSED"):
        raise ValueError(
            f"Semantic review did not yield PASS decision: decision={decision}, status={status}"
        )

    # Reviewer identity and timestamp presence
    reviewed_by = raw.get("reviewed_by")
    if not reviewed_by or not isinstance(reviewed_by, str) or not reviewed_by.strip():
        raise ValueError("Semantic review lacks valid reviewed_by identity")
    recorded_at = raw.get("recorded_at") or raw.get("reviewed_at")
    if not recorded_at:
        raise ValueError("Semantic review lacks recorded_at/reviewed_at timestamp")

    return {
        "status": status,
        "decision": decision,
        "reviewed_by": reviewed_by,
        "surface_path": surface_rel,
        "surface_sha256": surface_sha,
        "recorded_at": recorded_at,
        "reviewed_at": raw.get("reviewed_at") or recorded_at,
        "review_path": review_rel,
        "review_sha256": raw["review_sha256"],
        "checks": checks,
        "findings": findings,
        "unresolved_blocking_count": unresolved_blocking,
        "summary": raw.get("summary", ""),
    }


load_and_validate_semantic_review = load_and_validate_reader_surface_semantic_review


def build_semantic_authority(
    primary_source_path: Path | None = None,
    *,
    review_path: Path | None = None,
    repo_root: Path | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Adopt semantic authority ONLY from an independently validated persisted review artifact.

    Synthetic PASS generation without a persisted review record is strictly prohibited.
    """
    if review_path is None:
        raise ValueError(
            "build_semantic_authority() cannot synthesize PASS; a validated persisted semantic review "
            "artifact on disk is required via review_path or load_and_validate_reader_surface_semantic_review()."
        )
    root = repo_root or Path(".")
    return load_and_validate_reader_surface_semantic_review(root, review_path)


def _derivation_for_manuscript(
    repo_root: Path,
    manuscript: dict[str, Any],
    reviewed_surface_path: str,
    review_path: str,
    review_sha256: str,
    *,
    state_path: Path | None = None,
) -> dict[str, Any]:
    """Select the explicit primary-only or complete generated Weekly route."""
    primary = manuscript["primary_source"]
    if reviewed_surface_path == primary["path"]:
        if core.sha256_file(core.repo_local_path(repo_root, primary["path"], "direct primary")) != primary["sha256"]:
            raise ValueError("DIRECT_PRIMARY reviewed primary drift")
        return {"route": "DIRECT_PRIMARY", "scope": "PRIMARY_ONLY"}
    if manuscript.get("research_profile") == "THEMATIC" and manuscript.get("publication_profile") == "LONGFORM_SPECIAL":
        surface_path = core.repo_local_path(repo_root, reviewed_surface_path, "generated reader input")
        if surface_path.name != "reader-surface-input-v2.json":
            raise ValueError("Longform generated review target must be canonical reader input")
        # Exact canonical edition publication suffix (not basename only): the
        # reader input must live at .../publication/v2/reader-surface-input-v2.json
        # and the receipt sibling is bound to the same directory.
        surface_rel_parts = Path(reviewed_surface_path).parts
        if len(surface_rel_parts) < 3 or surface_rel_parts[-3:] != ("publication", "v2", "reader-surface-input-v2.json"):
            raise ValueError("Longform generated review target must be canonical publication/v2 reader input")
        from scripts import survey_longform_derivation_v2 as longform_derivation
        from scripts import survey_longform_generated_v2 as generated
        longform_derivation.validate_longform_reader_input(repo_root, surface_path)
        receipt_path = surface_path.parent / "validated-source-manifest.json"
        receipt = generated.validate_receipt(repo_root, receipt_path, state_path)
        receipt_ref = {"path": _rel(repo_root, receipt_path), "sha256": core.sha256_file(receipt_path)}
        if receipt["route"] != generated.ROUTE or receipt["issue_id"] != manuscript["issue_id"]:
            raise ValueError("Longform receipt route or issue identity mismatch")
        if receipt["reviewed_reader_input"] != {"path": reviewed_surface_path, "sha256": core.sha256_file(surface_path)}:
            raise ValueError("Longform receipt reviewed target mismatch")
        if receipt["semantic_review"] != {"path": review_path, "sha256": review_sha256}:
            raise ValueError("Longform receipt semantic review mismatch")
        survey_dir = core.repo_local_path(repo_root, primary["path"], "Longform primary").parent
        expected = {
            "primary": primary,
            "bibliography": next((r for r in manuscript["supporting_files"] if r["role"] == "BIBLIOGRAPHY"), None),
            "style": next((r for r in manuscript["supporting_files"] if r["role"] == "STYLE"), None),
        }
        if len(manuscript["supporting_files"]) != 2 or any(row is None for row in expected.values()):
            raise ValueError("unsupported Longform generated support closure")
        for name, filename in (("primary", "main.tex"), ("bibliography", "references.bib"), ("style", "jgaisurvey.sty")):
            row = expected[name]
            assert row is not None
            if row["path"] != _rel(repo_root, survey_dir / filename):
                raise ValueError(f"unsupported Longform generated {name} path")
            output = receipt["outputs"][name]
            if output["path"] != row["path"] or output["sha256"] != row["sha256"]:
                raise ValueError(f"Longform receipt output differs from selected Reader Manuscript {name}")
        return {"route": generated.ROUTE, "scope": generated.SCOPE, "receipt": receipt_ref}
    if manuscript.get("research_profile") != "WEEKLY" or manuscript.get("publication_profile") != "WEEKLY_MAGAZINE":
        raise ValueError("structured review target requires supported Weekly generated route")
    surface_path = core.repo_local_path(repo_root, reviewed_surface_path, "generated reader input")
    if surface_path.name != "reader-surface-input-v2.json":
        raise ValueError("Weekly generated review target must be canonical reader input")
    from scripts import survey_weekly_derivation_v2 as weekly
    weekly.validate_reader_input(repo_root, surface_path)
    receipt_path = surface_path.parent / "validated-source-manifest.json"
    receipt = weekly.validate_receipt(repo_root, receipt_path, state_path)
    receipt_ref = {"path": _rel(repo_root, receipt_path), "sha256": core.sha256_file(receipt_path)}
    if receipt["route"] != weekly.ROUTE or receipt["issue_id"] != manuscript["issue_id"]:
        raise ValueError("Weekly receipt route or issue identity mismatch")
    if receipt["reviewed_reader_input"] != {"path": reviewed_surface_path, "sha256": core.sha256_file(surface_path)}:
        raise ValueError("Weekly receipt reviewed target mismatch")
    if receipt["semantic_review"] != {"path": review_path, "sha256": review_sha256}:
        raise ValueError("Weekly receipt semantic review mismatch")
    survey_dir = core.repo_local_path(repo_root, primary["path"], "Weekly primary").parent
    expected = {
        "primary": primary,
        "bibliography": next((r for r in manuscript["supporting_files"] if r["role"] == "BIBLIOGRAPHY"), None),
        "style": next((r for r in manuscript["supporting_files"] if r["role"] == "STYLE"), None),
    }
    if len(manuscript["supporting_files"]) != 2 or any(row is None for row in expected.values()):
        raise ValueError("unsupported Weekly generated support closure")
    for name, filename in (("primary", "main.tex"), ("bibliography", "references.bib"), ("style", "jgaisurvey.sty")):
        row = expected[name]
        assert row is not None
        if row["path"] != _rel(repo_root, survey_dir / filename):
            raise ValueError(f"unsupported Weekly generated {name} path")
        output = receipt["outputs"][name]
        if output["path"] != row["path"] or output["sha256"] != row["sha256"]:
            raise ValueError(f"Weekly receipt output differs from selected Reader Manuscript {name}")
    return {"route": weekly.ROUTE, "scope": "WEEKLY_MAIN_BIB_STYLE", "receipt": receipt_ref}


def evaluate_reader_surface_gate(
    repo_root: Path,
    manuscript_path: Path,
    *,
    semantic_authority: dict[str, Any] | None = None,
    semantic_review_path: Path | None = None,
    structured_surface_path: Path | None = None,
    suppressions: list[dict[str, Any]] | None = None,
    semantic_review_findings: list[dict[str, Any]] | None = None,
    synthesis_result_path: Path | None = None,
    evaluated_by: str = "Core v2 Pre-Publication Reader-Surface Gate",
    recorded_at: datetime | None = None,
    output_path: Path | None = None,
    state_path: Path | None = None,
) -> dict[str, Any]:
    """Evaluate Pre-Publication Reader-Surface Gate for a reader manuscript.

    Scans all declared reader-facing source files, bibliography, synthesis
    publication payload, structured pre-TeX reader surface, and manifest details.
    Evaluates lexical lint and mandatory independently validated semantic review authority,
    applies suppressions, and returns a structured gate report conforming to
    schemas/reader-surface-gate-v2.schema.json.
    """
    if semantic_authority is None and semantic_review_path is None:
        raise ValueError(
            "Reader-Surface Gate requires machine-checkable semantic_authority; omitting semantic review cannot PASS"
        )

    ts_str = _iso_or_now(recorded_at)
    m_file = _safe_file(repo_root, manuscript_path, "Reader Manuscript Manifest")
    manuscript = schema_gate.load_and_validate_json(
        m_file, repo_root / MANUSCRIPT_SCHEMA, label="Reader Manuscript Manifest"
    )

    if semantic_review_path is not None:
        rev_file = core.repo_local_path(repo_root, semantic_review_path, "semantic review record")
        validated_sem = load_and_validate_semantic_review(
            repo_root,
            rev_file,
            expected_issue_id=manuscript["issue_id"],
            expected_publication_profile=manuscript["publication_profile"],
            require_pass=False,
        )
        sem_auth_input = validated_sem
    else:
        assert semantic_authority is not None
        if not isinstance(semantic_authority, dict):
            raise ValueError("semantic_authority must be an object")
        for req_key in ("status", "decision", "reviewed_by", "surface_sha256", "recorded_at", "review_path", "review_sha256"):
            if not semantic_authority.get(req_key):
                raise ValueError(
                    f"semantic_authority missing required field: {req_key}; synthetic PASS dictionary is rejected"
                )
        rev_file, _ = _resolve_repo_path(repo_root, semantic_authority["review_path"], "semantic review record")
        if not rev_file.is_file():
            raise ValueError(
                f"Reader-Surface Gate referenced semantic review record missing on disk: {semantic_authority['review_path']}"
            )
        validated_sem = load_and_validate_semantic_review(
            repo_root,
            rev_file,
            expected_issue_id=manuscript["issue_id"],
            expected_publication_profile=manuscript["publication_profile"],
            require_pass=False,
        )
        if semantic_authority["review_sha256"] != validated_sem["review_sha256"]:
            raise ValueError(
                f"semantic_authority review_sha256 mismatch: expected {validated_sem['review_sha256']}, got {semantic_authority['review_sha256']}"
            )
        if validated_sem["unresolved_blocking_count"] > 0 and semantic_authority.get("decision") == "PASS":
            raise ValueError(
                f"semantic_authority claims PASS but review record at {semantic_authority['review_path']} contains {validated_sem['unresolved_blocking_count']} unresolved blocking finding(s)"
            )
        sem_auth_input = semantic_authority

    active_suppressions = list(suppressions or [])
    all_findings: list[SurfaceFinding] = []
    scanned_surfaces: list[dict[str, Any]] = []

    # 1. Primary Source
    primary_ref = manuscript["primary_source"]
    primary_path = core.repo_local_path(repo_root, primary_ref["path"], "primary source")
    scanned_surfaces.append(
        {
            "path": primary_ref["path"],
            "sha256": primary_ref["sha256"],
            "kind": "PRIMARY_SOURCE",
            "byte_count": primary_path.stat().st_size,
        }
    )
    primary_findings = scan_tex_file(
        repo_root, primary_path, suppressions=active_suppressions, artifact_label="Primary Source"
    )
    all_findings.extend(primary_findings)

    # 2. Supporting Files
    for support_ref in manuscript.get("supporting_files", []):
        support_path = core.repo_local_path(repo_root, support_ref["path"], "supporting file")
        role = support_ref.get("role")
        kind_label = (
            "BIBLIOGRAPHY"
            if role == "BIBLIOGRAPHY"
            else "SUPPORTING_SOURCE"
        )
        scanned_surfaces.append(
            {
                "path": support_ref["path"],
                "sha256": support_ref["sha256"],
                "kind": kind_label,
                "byte_count": support_path.stat().st_size,
            }
        )
        if role == "BIBLIOGRAPHY":
            bib_findings = scan_bib_file(
                repo_root,
                support_path,
                suppressions=active_suppressions,
                artifact_label=f"Supporting {role}",
            )
            all_findings.extend(bib_findings)
        elif role == "SUPPORTING_SOURCE" and support_path.suffix == ".tex":
            supp_findings = scan_tex_file(
                repo_root,
                support_path,
                suppressions=active_suppressions,
                artifact_label=f"Supporting Source ({support_ref['path']})",
            )
            all_findings.extend(supp_findings)

    # 3. Manuscript Manifest Details (coverage detail fields)
    m_rel = _rel(repo_root, m_file)
    scanned_surfaces.append(
        {
            "path": m_rel,
            "sha256": core.sha256_file(m_file),
            "kind": "MANUSCRIPT_MANIFEST",
            "byte_count": m_file.stat().st_size,
        }
    )
    for idx, cov in enumerate(manuscript.get("architecture_coverage", [])):
        detail_text = cov.get("detail", "")
        pkg = cov.get("package_id", "")
        req = cov.get("requirement", "")
        lines = [detail_text]
        cov_findings = scan_reader_text_lines(
            lines,
            "Architecture Coverage Detail",
            m_rel,
            suppressions=active_suppressions,
            block_context=f"coverage:{pkg}/{req}",
        )
        all_findings.extend(cov_findings)

    # 4. Optional Synthesis Result publication_payload
    if synthesis_result_path is not None and synthesis_result_path.is_file():
        syn_data = core.load_json(synthesis_result_path)
        pub_payload = syn_data.get("publication_payload")
        syn_rel = _rel(repo_root, synthesis_result_path)
        if isinstance(pub_payload, dict) and pub_payload:
            scanned_surfaces.append(
                {
                    "path": syn_rel,
                    "sha256": core.sha256_file(synthesis_result_path),
                    "kind": "SYNTHESIS_PAYLOAD",
                    "byte_count": synthesis_result_path.stat().st_size,
                }
            )
            syn_findings = scan_publication_payload(
                pub_payload, syn_rel, suppressions=active_suppressions
            )
            all_findings.extend(syn_findings)

    # 5. Scan the exact reviewed structured target when generated Weekly is selected.
    rev_target = validated_sem["surface_path"]
    if structured_surface_path is not None:
        supplied_rel = _rel(repo_root, _safe_file(repo_root, structured_surface_path, "structured reader surface"))
        if supplied_rel != rev_target:
            raise ValueError("explicit structured reader surface differs from semantic review target")
    if rev_target != primary_ref["path"]:
        if manuscript.get("research_profile") == "THEMATIC" and manuscript.get("publication_profile") == "LONGFORM_SPECIAL":
            from scripts import survey_longform_derivation_v2 as longform_derivation
            st_file = core.repo_local_path(repo_root, rev_target, "reviewed Longform reader input")
            st_data = longform_derivation.validate_longform_reader_input(repo_root, st_file)
            st_rel = _rel(repo_root, st_file)
            scanned_surfaces.append({
                "path": st_rel, "sha256": core.sha256_file(st_file),
                "kind": "STRUCTURED_READER_SURFACE", "byte_count": st_file.stat().st_size,
            })
            all_findings.extend(scan_structured_reader_surface(st_data, st_rel, suppressions=active_suppressions))
        elif manuscript.get("research_profile") != "WEEKLY" or manuscript.get("publication_profile") != "WEEKLY_MAGAZINE":
            raise ValueError("unsupported structured reader review target")
        else:
            from scripts import survey_weekly_derivation_v2 as weekly
            st_file = core.repo_local_path(repo_root, rev_target, "reviewed Weekly reader input")
            st_data = weekly.validate_reader_input(repo_root, st_file)
            st_rel = _rel(repo_root, st_file)
            scanned_surfaces.append({
                "path": st_rel, "sha256": core.sha256_file(st_file),
                "kind": "STRUCTURED_READER_SURFACE", "byte_count": st_file.stat().st_size,
            })
            all_findings.extend(scan_structured_reader_surface(st_data, st_rel, suppressions=active_suppressions))

    # 6. Semantic Review Findings & Authority Checks (Layer 2)
    sem_status = sem_auth_input.get("status")
    sem_decision = sem_auth_input.get("decision")
    sem_surface_sha = sem_auth_input.get("surface_sha256")
    rev_surface_rel = validated_sem.get("surface_path", primary_ref["path"])
    rev_surface_file, _ = _resolve_repo_path(repo_root, rev_surface_rel, "reviewed surface")
    actual_rev_surface_sha = core.sha256_file(rev_surface_file) if rev_surface_file.is_file() else None

    if actual_rev_surface_sha is None or sem_surface_sha != actual_rev_surface_sha:
        all_findings.append(
            SurfaceFinding(
                finding_id="RSG-SEM-SURFACE-SHA-MISMATCH",
                rule_id="RSG-SEM-PROCESS-LEAKAGE",
                artifact="Semantic Review Authority",
                path=rev_surface_rel,
                field_or_block="surface_sha256",
                locator="semantic_authority",
                text_span=str(sem_surface_sha),
                severity="BLOCKING",
                reason=f"semantic authority surface_sha256 {sem_surface_sha} does not match current disk file sha256 {actual_rev_surface_sha}",
                proposed_normalization="Re-evaluate semantic review on exact current surface bytes",
                disposition="UNRESOLVED",
            )
        )
    if sem_status != "PASSED" or sem_decision != "PASS" or validated_sem["decision"] != "PASS":
        all_findings.append(
            SurfaceFinding(
                finding_id="RSG-SEM-AUTHORITY-FAILED",
                rule_id="RSG-SEM-PROCESS-LEAKAGE",
                artifact="Semantic Review Authority",
                path=rev_surface_rel,
                field_or_block="status/decision",
                locator="semantic_authority",
                text_span=f"{sem_status}/{sem_decision}",
                severity="BLOCKING",
                reason="Semantic review authority did not yield PASS decision",
                proposed_normalization="Resolve semantic review findings to obtain PASS authority",
                disposition="UNRESOLVED",
            )
        )

    all_sem_findings = list(semantic_review_findings or [])
    if isinstance(validated_sem.get("findings"), list):
        for f in validated_sem["findings"]:
            if f not in all_sem_findings:
                all_sem_findings.append(f)
    elif isinstance(sem_auth_input.get("findings"), list):
        for f in sem_auth_input["findings"]:
            if f not in all_sem_findings:
                all_sem_findings.append(f)

    if all_sem_findings:
        for idx, sem in enumerate(all_sem_findings):
            if not isinstance(sem, dict):
                continue
            fid = sem.get("finding_id") or f"RSG-SEM-PROCESS-LEAKAGE-{idx+1}"
            rule_id = sem.get("rule_id", "RSG-SEM-PROCESS-LEAKAGE")
            path_str = sem.get("path", m_rel)
            span = sem.get("text_span", "")
            suppressed, sup_reason = _is_suppressed(
                active_suppressions, rule_id, path_str, span
            )
            sev = sem.get("severity", "BLOCKING")
            disp = sem.get("disposition", "UNRESOLVED")
            if suppressed:
                sev = "SUPPRESSED"
                disp = "SUPPRESSED"

            all_findings.append(
                SurfaceFinding(
                    finding_id=fid,
                    rule_id=rule_id,
                    artifact=sem.get("artifact", "Semantic Review"),
                    path=path_str,
                    field_or_block=sem.get("field_or_block", "semantic-review"),
                    locator=sem.get("locator", f"Finding {idx+1}"),
                    text_span=span,
                    severity=sev,
                    reason=f"Suppressed: {sup_reason}" if suppressed else sem.get("reason", "Requires internal pipeline knowledge"),
                    proposed_normalization=sem.get("proposed_normalization", "Rewrite into reader-facing domain prose"),
                    disposition=disp,
                )
            )

    derivation = _derivation_for_manuscript(
        repo_root, manuscript, rev_surface_rel,
        _rel(repo_root, rev_file), core.sha256_file(rev_file), state_path=state_path,
    )

    # Summary calculation
    blocking_count = sum(
        1 for f in all_findings if f.severity == "BLOCKING" and f.disposition == "UNRESOLVED"
    )
    warning_count = sum(
        1 for f in all_findings if f.severity == "WARNING" and f.disposition == "UNRESOLVED"
    )
    suppressed_count = sum(
        1 for f in all_findings if f.disposition == "SUPPRESSED"
    )
    normalized_count = sum(
        1 for f in all_findings if f.disposition == "NORMALIZED"
    )

    authority_clean = (
        sem_status == "PASSED"
        and sem_decision == "PASS"
        and validated_sem["decision"] == "PASS"
        and validated_sem["unresolved_blocking_count"] == 0
        and actual_rev_surface_sha is not None
        and sem_surface_sha == actual_rev_surface_sha
    )
    verdict = "PASSED" if (blocking_count == 0 and authority_clean) else "FAILED"

    rules_checked_dicts = [asdict(r) for r in RULES]

    base: dict[str, Any] = {
        "schema_version": "2.0-rc1",
        "issue_id": manuscript["issue_id"],
        "publication_profile": manuscript["publication_profile"],
        "status": verdict,
        "scanned_surfaces": scanned_surfaces,
        "rules_checked": rules_checked_dicts,
        "suppressions": active_suppressions,
        "findings": [f.to_dict() for f in all_findings],
        "summary": {
            "total_findings": len(all_findings),
            "blocking_findings": blocking_count,
            "warning_findings": warning_count,
            "suppressed_findings": suppressed_count,
            "normalized_findings": normalized_count,
            "verdict": verdict,
        },
        "evaluated_by": evaluated_by,
        "recorded_at": ts_str,
        "derivation": derivation,
        "semantic_authority": {
            "status": "PASSED" if verdict == "PASSED" and authority_clean else "FAILED",
            "decision": "PASS" if verdict == "PASSED" and authority_clean else "FAIL",
            "reviewed_by": str(sem_auth_input.get("reviewed_by", validated_sem["reviewed_by"])),
            "surface_path": str(sem_auth_input.get("surface_path", rev_surface_rel)),
            "surface_sha256": str(sem_auth_input.get("surface_sha256", validated_sem["surface_sha256"])),
            "recorded_at": str(sem_auth_input.get("recorded_at", ts_str)),
            "reviewed_at": str(sem_auth_input.get("reviewed_at", validated_sem.get("reviewed_at", ts_str))),
            "review_path": str(sem_auth_input["review_path"]),
            "review_sha256": str(sem_auth_input["review_sha256"]),
            **({"summary": sem_auth_input["summary"]} if "summary" in sem_auth_input else {}),
        },
    }

    report = dict(base)
    report["gate_sha256"] = core.sha256_object(base)

    schema_gate.validate_instance(
        report, repo_root / SURFACE_GATE_SCHEMA, label="Reader-Surface Gate Record"
    )

    if output_path is not None:
        core.write_json(output_path, report)

    return report


def _inspect_gate_record(
    repo_root: Path,
    path: Path,
    *,
    issue_id: str | None = None,
    publication_profile: str | None = None,
    expected_manuscript_path: Path | None = None,
) -> dict[str, Any]:
    """Private non-authoritative structural/semantic inspection of a Gate record.

    Performs every ``validate_reader_surface_gate`` check EXCEPT the generated
    derivation replay (receipt/current-tool binding).  Shared by the public
    validator (which always runs full derivation replay afterwards) and the
    mechanical-refresh owner (which calls this only after the old raw Gate
    hash has been anchored to strict live State authority, then checks the
    receipt link and historical closure independently).  Never an admission
    path on its own: inspection alone does not prove current replay.
    """
    gate_file = _safe_file(repo_root, path, "Reader-Surface Gate record")
    payload = schema_gate.load_and_validate_json(
        gate_file, repo_root / SURFACE_GATE_SCHEMA, label="Reader-Surface Gate"
    )
    if issue_id is not None and payload.get("issue_id") != issue_id:
        raise ValueError(
            f"Reader-Surface Gate issue_id mismatch: expected {issue_id}, got {payload.get('issue_id')}"
        )
    if publication_profile is not None and payload.get("publication_profile") != publication_profile:
        raise ValueError(
            f"Reader-Surface Gate publication_profile mismatch: expected {publication_profile}, got {payload.get('publication_profile')}"
        )
    if payload.get("status") != "PASSED":
        raise ValueError(f"Reader-Surface Gate status must be PASSED, got {payload.get('status')}")

    summary = payload.get("summary", {})
    if summary.get("verdict") != "PASSED":
        raise ValueError(f"Reader-Surface Gate summary verdict must be PASSED, got {summary.get('verdict')}")
    if summary.get("blocking_findings", 0) != 0:
        raise ValueError(f"Reader-Surface Gate contains {summary.get('blocking_findings')} unresolved blocking finding(s)")

    # 4. gate_sha256 recalculation
    digest_fields = (
        "schema_version",
        "issue_id",
        "publication_profile",
        "status",
        "scanned_surfaces",
        "rules_checked",
        "suppressions",
        "findings",
        "summary",
        "evaluated_by",
        "recorded_at",
        "semantic_authority",
        "derivation",
    )
    base = {key: payload[key] for key in digest_fields}
    expected_gate_sha = core.sha256_object(base)
    if payload.get("gate_sha256") != expected_gate_sha:
        raise ValueError(
            f"Reader-Surface Gate digest mismatch: expected {expected_gate_sha}, got {payload.get('gate_sha256')}"
        )

    # 5. Scanned surfaces verification against current files on disk
    scanned = payload.get("scanned_surfaces", [])
    if not scanned:
        raise ValueError("Reader-Surface Gate record contains no scanned surfaces")
    manuscript_surfaces = [s for s in scanned if s.get("kind") == "MANUSCRIPT_MANIFEST"]
    if len(manuscript_surfaces) != 1:
        raise ValueError(
            "Reader-Surface Gate must contain exactly one MANUSCRIPT_MANIFEST in scanned surfaces; "
            f"found {len(manuscript_surfaces)}"
        )
    primary_surfaces = [s for s in scanned if s.get("kind") == "PRIMARY_SOURCE"]
    if len(primary_surfaces) != 1:
        raise ValueError(
            "Reader-Surface Gate must contain exactly one PRIMARY_SOURCE in scanned surfaces; "
            f"found {len(primary_surfaces)}"
        )

    manuscript_surface = manuscript_surfaces[0]
    manuscript_file = _safe_file(
        repo_root,
        expected_manuscript_path if expected_manuscript_path is not None else manuscript_surface["path"],
        "expected Reader Manuscript Manifest",
    )
    manuscript_rel = _rel(repo_root, manuscript_file)
    manuscript_sha = core.sha256_file(manuscript_file)
    if (
        manuscript_surface.get("path") != manuscript_rel
        or manuscript_surface.get("sha256") != manuscript_sha
    ):
        raise ValueError(
            "Reader-Surface Gate MANUSCRIPT_MANIFEST does not bind the exact expected Reader Manuscript: "
            f"expected {manuscript_rel} ({manuscript_sha}), got "
            f"{manuscript_surface.get('path')} ({manuscript_surface.get('sha256')})"
        )
    manuscript = schema_gate.load_and_validate_json(
        manuscript_file,
        repo_root / MANUSCRIPT_SCHEMA,
        label="expected Reader Manuscript Manifest",
    )
    if manuscript.get("issue_id") != payload.get("issue_id"):
        raise ValueError(
            "Reader-Surface Gate/expected Reader Manuscript issue_id mismatch: "
            f"{payload.get('issue_id')} != {manuscript.get('issue_id')}"
        )
    if manuscript.get("publication_profile") != payload.get("publication_profile"):
        raise ValueError(
            "Reader-Surface Gate/expected Reader Manuscript publication_profile mismatch: "
            f"{payload.get('publication_profile')} != {manuscript.get('publication_profile')}"
        )
    primary_surface = primary_surfaces[0]
    primary_ref = manuscript["primary_source"]
    if (
        primary_surface.get("path") != primary_ref.get("path")
        or primary_surface.get("sha256") != primary_ref.get("sha256")
    ):
        raise ValueError(
            "Reader-Surface Gate PRIMARY_SOURCE does not match the expected Reader Manuscript primary_source: "
            f"expected {primary_ref.get('path')} ({primary_ref.get('sha256')}), got "
            f"{primary_surface.get('path')} ({primary_surface.get('sha256')})"
        )

    for s in scanned:
        rel = s["path"]
        target = core.repo_local_path(repo_root, rel, f"scanned surface {rel}")
        if not target.is_file():
            raise ValueError(f"Reader-Surface Gate scanned surface missing on disk: {rel}")
        actual_bytes = target.read_bytes()
        actual_sha = core.sha256_bytes(actual_bytes)
        if actual_sha != s["sha256"]:
            raise ValueError(
                f"Reader-Surface Gate scanned surface bytes drifted for {rel}: "
                f"recorded {s['sha256']}, current disk {actual_sha}"
            )
        if len(actual_bytes) != s["byte_count"]:
            raise ValueError(
                f"Reader-Surface Gate scanned surface byte_count drifted for {rel}: "
                f"recorded {s['byte_count']}, current disk {len(actual_bytes)}"
            )

    # 6. Required semantic review authority verification
    sem = payload.get("semantic_authority")
    if not isinstance(sem, dict):
        raise ValueError("Reader-Surface Gate record missing required semantic_authority object")
    for req_key in ("status", "decision", "reviewed_by", "surface_sha256", "recorded_at", "review_path", "review_sha256"):
        if not sem.get(req_key):
            raise ValueError(
                f"Reader-Surface Gate semantic_authority missing required field: {req_key}; synthetic PASS is forbidden"
            )
    if sem.get("status") != "PASSED" or sem.get("decision") != "PASS":
        raise ValueError(
            f"Reader-Surface Gate semantic review authority not PASS: status={sem.get('status')}, decision={sem.get('decision')}"
        )
    if not sem.get("reviewed_by") or not isinstance(sem.get("reviewed_by"), str):
        raise ValueError("Reader-Surface Gate semantic review authority lacks reviewed_by identity")

    rev_file, _ = _resolve_repo_path(repo_root, sem["review_path"], "semantic review record")
    if not rev_file.is_file():
        raise ValueError(f"Reader-Surface Gate referenced semantic review record missing on disk: {sem['review_path']}")

    validated_sem = load_and_validate_semantic_review(
        repo_root,
        rev_file,
        expected_issue_id=payload.get("issue_id"),
        expected_publication_profile=payload.get("publication_profile"),
        expected_surface_sha256=sem["surface_sha256"],
        require_pass=True,
    )
    if sem["review_sha256"] != validated_sem["review_sha256"]:
        raise ValueError(
            f"Reader-Surface Gate referenced semantic review record digest mismatch: expected {validated_sem['review_sha256']}, got {sem['review_sha256']}"
        )
    if sem["surface_sha256"] != validated_sem["surface_sha256"]:
        raise ValueError("Reader-Surface Gate semantic authority surface_sha256 mismatch")
    if sem.get("surface_path") and sem["surface_path"] != validated_sem["surface_path"]:
        raise ValueError("Reader-Surface Gate semantic authority surface_path mismatch")

    # Unresolved blocking findings verification (shared; runs inside the
    # private inspection so the refresh owner cannot miss it).
    for f in payload.get("findings", []):
        if f.get("severity") == "BLOCKING" and f.get("disposition") == "UNRESOLVED":
            raise ValueError(
                f"Reader-Surface Gate has unresolved blocking finding: {f.get('finding_id')} ({f.get('text_span')})"
            )

    return {
        "payload": payload,
        "manuscript": manuscript,
        "manuscript_file": manuscript_file,
        "validated_sem": validated_sem,
        "rev_file": rev_file,
        "scanned": scanned,
    }


def validate_reader_surface_gate(
    repo_root: Path,
    path: Path,
    *,
    issue_id: str | None = None,
    publication_profile: str | None = None,
    expected_manuscript_path: Path | None = None,
    state_path: Path | None = None,
) -> dict[str, Any]:
    """Independently validate a Reader-Surface Gate record.

    Verifies:
      1. Schema validity.
      2. Issue identity and publication profile identity.
      3. Report status == PASSED and summary verdict == PASSED with 0 blocking findings.
      4. gate_sha256 recomputation over all canonical digest fields.
      5. Exactly one bound manuscript manifest and its corresponding primary source.
      6. Scanned surfaces existence, exact sha256 and byte counts matching current disk files.
      7. Required semantic review authority present, status PASSED, decision PASS,
         and surface_sha256 matching the exact persisted semantic-review target.
      8. No unresolved blocking findings.
      9. Full current generated-derivation replay (receipt/current-tool binding).

    ``expected_manuscript_path`` is mandatory for stage admission callers.  A
    standalone inspection may omit it, in which case the validator inspects
    the Gate's single recorded manuscript manifest as its own bound target.
    """
    inspected = _inspect_gate_record(
        repo_root,
        path,
        issue_id=issue_id,
        publication_profile=publication_profile,
        expected_manuscript_path=expected_manuscript_path,
    )
    payload = inspected["payload"]
    manuscript = inspected["manuscript"]
    validated_sem = inspected["validated_sem"]
    rev_file = inspected["rev_file"]
    expected_derivation = _derivation_for_manuscript(
        repo_root, manuscript, validated_sem["surface_path"],
        _rel(repo_root, rev_file), core.sha256_file(rev_file), state_path=state_path,
    )
    if payload["derivation"] != expected_derivation:
        raise ValueError("Reader-Surface Gate derivation route or receipt mismatch")

    return payload


def validate_manuscript_surface(
    repo_root: Path,
    manuscript: dict[str, Any],
    suppressions: list[dict[str, Any]] | None = None,
    semantic_authority: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Fail-fast reader surface validation for a validated manuscript manifest.

    Scans the primary source and all supporting files. Raises ValueError with
    complete finding details if any unresolved blocking findings exist.
    """
    active_suppressions = list(suppressions or [])
    all_findings: list[SurfaceFinding] = []

    # Primary source
    primary_ref = manuscript["primary_source"]
    primary_path = core.repo_local_path(repo_root, primary_ref["path"], "primary source")
    primary_findings = scan_tex_file(
        repo_root, primary_path, suppressions=active_suppressions, artifact_label="Primary Source"
    )
    all_findings.extend(primary_findings)

    # Supporting files
    for support_ref in manuscript.get("supporting_files", []):
        support_path = core.repo_local_path(repo_root, support_ref["path"], "supporting file")
        role = support_ref.get("role")
        if role == "BIBLIOGRAPHY":
            bib_findings = scan_bib_file(
                repo_root,
                support_path,
                suppressions=active_suppressions,
                artifact_label=f"Supporting {role}",
            )
            all_findings.extend(bib_findings)
        elif role == "SUPPORTING_SOURCE" and support_path.suffix == ".tex":
            supp_findings = scan_tex_file(
                repo_root,
                support_path,
                suppressions=active_suppressions,
                artifact_label=f"Supporting Source ({support_ref['path']})",
            )
            all_findings.extend(supp_findings)

    # Coverage detail
    for cov in manuscript.get("architecture_coverage", []):
        detail = cov.get("detail", "")
        pkg = cov.get("package_id", "")
        req = cov.get("requirement", "")
        findings = scan_reader_text_lines(
            [detail],
            "Architecture Coverage Detail",
            manuscript.get("production_profile", {}).get("path", "manifest"),
            suppressions=active_suppressions,
            block_context=f"coverage:{pkg}/{req}",
        )
        all_findings.extend(findings)

    # Semantic review authority check if supplied
    if semantic_authority is not None:
        sem_status = semantic_authority.get("status")
        sem_decision = semantic_authority.get("decision")
        sem_surface_sha = semantic_authority.get("surface_sha256")
        if sem_surface_sha != primary_ref["sha256"]:
            all_findings.append(
                SurfaceFinding(
                    finding_id="RSG-SEM-SURFACE-SHA-MISMATCH",
                    rule_id="RSG-SEM-PROCESS-LEAKAGE",
                    artifact="Semantic Review Authority",
                    path=primary_ref["path"],
                    field_or_block="surface_sha256",
                    locator="semantic_authority",
                    text_span=str(sem_surface_sha),
                    severity="BLOCKING",
                    reason=f"semantic authority surface_sha256 {sem_surface_sha} does not match primary source sha256 {primary_ref['sha256']}",
                    proposed_normalization="Re-evaluate semantic review on exact current primary source bytes",
                    disposition="UNRESOLVED",
                )
            )
        if sem_status != "PASSED" or sem_decision != "PASS":
            all_findings.append(
                SurfaceFinding(
                    finding_id="RSG-SEM-AUTHORITY-FAILED",
                    rule_id="RSG-SEM-PROCESS-LEAKAGE",
                    artifact="Semantic Review Authority",
                    path=primary_ref["path"],
                    field_or_block="status/decision",
                    locator="semantic_authority",
                    text_span=f"{sem_status}/{sem_decision}",
                    severity="BLOCKING",
                    reason="Semantic review authority did not yield PASS decision",
                    proposed_normalization="Resolve semantic review findings to obtain PASS authority",
                    disposition="UNRESOLVED",
                )
            )

    blocking = [
        f for f in all_findings
        if f.severity == "BLOCKING" and f.disposition == "UNRESOLVED"
    ]

    if blocking:
        lines = [
            f"Pre-Publication Reader-Surface Gate FAILED: {len(blocking)} blocking finding(s) detected:"
        ]
        for idx, f in enumerate(blocking, start=1):
            lines.append(
                f"  [{idx}] {f.rule_id} at {f.path} ({f.locator}, {f.field_or_block}): "
                f"leaked {f.text_span!r} - {f.reason}. Normalization: {f.proposed_normalization}"
            )
        raise ValueError("\n".join(lines))

    return {
        "status": "PASSED",
        "total_findings": len(all_findings),
        "blocking_findings": 0,
        "suppressed_findings": sum(1 for f in all_findings if f.disposition == "SUPPRESSED"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Pre-Publication Reader-Surface Gate for Survey Production Core v2"
    )
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    sub = parser.add_subparsers(dest="command", required=True)

    scan_m = sub.add_parser("scan-manuscript", help="Scan a reader manuscript manifest and its files")
    scan_m.add_argument("--manuscript", required=True, help="Path to reader-manuscript-v2.json")
    scan_m.add_argument("--suppressions", help="Path to suppressions JSON array")
    scan_m.add_argument(
        "--semantic-authority",
        help="Path to a persisted reader-surface semantic review record (validated by the strict loader) "
        "or a semantic authority JSON object",
    )
    scan_m.add_argument("--semantic-review", help="Path to semantic review findings JSON array")
    scan_m.add_argument("--synthesis-result", help="Path to profile-synthesis-result.json")
    scan_m.add_argument("--output", help="Path to write reader-surface-gate-v2.json report")
    scan_m.add_argument("--state", help="Current Production State for generated Weekly replay")

    val_g = sub.add_parser("validate-gate", help="Independently validate a reader-surface-gate-v2.json record")
    val_g.add_argument("--gate", required=True, help="Path to reader-surface-gate-v2.json")
    val_g.add_argument("--issue-id", help="Expected issue_id")
    val_g.add_argument("--profile", help="Expected publication_profile")
    val_g.add_argument("--state", help="Current Production State for generated Weekly replay")

    scan_f = sub.add_parser("scan-file", help="Scan an individual TeX or BibTeX file")
    scan_f.add_argument("--file", required=True, help="Path to TeX or BibTeX file")
    scan_f.add_argument("--suppressions", help="Path to suppressions JSON array")

    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()

    if args.command == "validate-gate":
        gate_path = Path(args.gate)
        if not gate_path.is_absolute():
            gate_path = repo_root / gate_path
        try:
            payload = validate_reader_surface_gate(
                repo_root, gate_path, issue_id=args.issue_id, publication_profile=args.profile,
                state_path=Path(args.state) if args.state else None,
            )
            print(f"PASSED: Reader-Surface Gate valid for {payload['issue_id']} ({payload['publication_profile']})")
            return 0
        except ValueError as exc:
            print(f"FAILED: {exc}")
            return 1

    if args.command == "scan-file":
        target = Path(args.file)
        if not target.is_absolute():
            target = repo_root / target
        suppressions = []
        if args.suppressions:
            suppressions = core.load_json(Path(args.suppressions))

        if target.suffix == ".bib":
            findings = scan_bib_file(repo_root, target, suppressions=suppressions)
        else:
            findings = scan_tex_file(repo_root, target, suppressions=suppressions)

        blocking = [f for f in findings if f.severity == "BLOCKING" and f.disposition == "UNRESOLVED"]
        for f in findings:
            print(f"[{f.severity}] {f.rule_id} at {f.path}:{f.locator} ({f.field_or_block}) - {f.text_span!r}: {f.reason}")
        if blocking:
            print(f"FAILED: {len(blocking)} blocking findings")
            return 1
        print("PASSED: Zero blocking findings")
        return 0

    if args.command == "scan-manuscript":
        m_path = Path(args.manuscript)
        if not m_path.is_absolute():
            m_path = repo_root / m_path
        suppressions = []
        if args.suppressions:
            suppressions = core.load_json(Path(args.suppressions))
        sem_authority = None
        sem_review_path = None
        if args.semantic_authority:
            authority_file, authority_rel = _resolve_repo_path(
                repo_root, args.semantic_authority, "semantic authority record"
            )
            sem_data = core.load_json(authority_file)
            if isinstance(sem_data, dict) and sem_data.get("review_kind") == "SEMANTIC_EDITORIAL":
                # Persisted reader-surface semantic review records are admitted only through
                # the strict semantic_review_path loader, which independently validates the
                # schema, digest, reviewed_surface and identity. No authority dictionary is
                # synthesized here, and no legacy publication review is silently converted.
                sem_review_path = authority_rel
            else:
                sem_authority = sem_data
        sem_findings = []
        if args.semantic_review:
            sem_findings = core.load_json(Path(args.semantic_review))
        syn_path = None
        if args.synthesis_result:
            syn_path = Path(args.synthesis_result)
            if not syn_path.is_absolute():
                syn_path = repo_root / syn_path
        out_path = None
        if args.output:
            out_path = Path(args.output)
            if not out_path.is_absolute():
                out_path = repo_root / out_path

        report = evaluate_reader_surface_gate(
            repo_root,
            m_path,
            semantic_authority=sem_authority,
            semantic_review_path=sem_review_path,
            suppressions=suppressions,
            semantic_review_findings=sem_findings,
            synthesis_result_path=syn_path,
            output_path=out_path,
            state_path=Path(args.state) if args.state else None,
        )

        status = report["status"]
        summary = report["summary"]
        print(f"Reader-Surface Gate: {status}")
        print(f"  Total findings: {summary['total_findings']}")
        print(f"  Blocking: {summary['blocking_findings']}")
        print(f"  Suppressed: {summary['suppressed_findings']}")
        if status != "PASSED":
            for f in report["findings"]:
                if f["severity"] == "BLOCKING" and f["disposition"] == "UNRESOLVED":
                    print(f"  - [{f['rule_id']}] {f['path']}:{f['locator']} ({f['field_or_block']}): {f['text_span']!r} -> {f['reason']}")
            return 1
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
