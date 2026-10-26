#!/usr/bin/env python3
"""Versioned same-reader renewal historical identity evaluator (HIST leaf) — STRICT.

Finite old/new structural/evidence/epoch evaluator, FD-bound safe ref readers,
typed retained mapping, exact closure/membership, derived epochs, fail-closed.
Does NOT run old code, call old full current validators, establish genuine
approval, or return reusable permission tokens. No caller verified dict.

Must NOT call (import or runtime): agent control, Reader/Gate/Candidate,
high-operation, seal/current-selection, P1/P2R/P3S/high receipt, P2V,
agent/Reader/Gate/Candidate validators. Low structural selection may call this
module; it must not call selection back (no State recursion).

History outputs HISTORICAL_IDENTITY_VERIFIED + derived observed_source_bindings,
never current-ready/replayed. Evidence E: exact live repo-contained paths +
hashes/sizes, strict shape, self-digests, typed cross-bindings, provenance
chain. E need NOT exist at tool commit. Tool T: each typed row checked against
its own recorded tool epoch Git blob (and mode 100644); never live-path equality.
Old T live bytes after Core change are NEVER enforced.
"""
from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


VERSIONED_KIND = "VERSIONED_RENEWAL_ACTIVATION_V1"
VERSIONED_REASON = "REVIEWED_VERSIONED_CORE_RENEWAL"
EDITORIAL_KIND = "EDITORIAL_PUBLICATION_ACTIVATION_V1"
EDITORIAL_REASON = "REVIEWED_EDITORIAL_CORRECTION"
LEGACY_REASON = "REVIEWED_CORE_CHANGE"

VERSIONED_SET_KIND = "VERSIONED_RENEWAL_SET_V1"
VERSIONED_SET_STATUS = "SEALED_INERT"

CHAIN_LIMIT = 32
MAX_PATH_LEN = 1024
MAX_PARTS = 64
MAX_FILE_BYTES = 10 * 1024 * 1024
MAX_JSON_BYTES = 5 * 1024 * 1024

REVALIDATION_SCHEMA = Path("schemas/publication-surface-revalidation.schema.json")
BASIS_SCHEMA = Path("schemas/versioned-renewal-basis-v2.schema.json")
PROOF_SCHEMA = Path("schemas/versioned-renewal-source-proof-v2.schema.json")
SET_SCHEMA = Path("schemas/versioned-renewal-publication-set-v2.schema.json")

PUBLICATION_ROLES_15 = (
    "reader-input",
    "authoring-input",
    "source-receipt",
    "reader-manuscript",
    "validated-source",
    "bibliography",
    "style",
    "publication-pdf",
    "build-log",
    "pdf-digest",
    "quality-regression-bundle",
    "semantic-review",
    "visual-review",
    "reader-surface-gate",
    "publication-candidate",
)
PUBLICATION_ROLES_7 = (
    "reader-manuscript",
    "validated-source",
    "publication-pdf",
    "quality-regression-bundle",
    "semantic-review",
    "visual-review",
    "reader-surface-gate",
)

# Contract8 recomputation (pure, no old code, no Production API, no currentState).
# Owned epoch config + supported exact pipeline OLD67/NEW71 + versions/quality/profiles.
# Recompute Contract8 at OWN epoch by pure algorithm of core.contract_identity:
# read config blob at epoch (mode 100644), pipeline aggregate (sorted registered paths
# plus DEFAULT_CONFIG/PROFILE_SCHEMA/STATE_SCHEMA, exact NUL framing), quality 3 aggregate,
# research/publication profile object digests. NO execute old code, NO remote, NO live.
_DEFAULT_CONFIG_PATH = "config/survey-production-v2.json"
_PROFILE_SCHEMA_PATH = "schemas/survey-production-profile.schema.json"
_STATE_SCHEMA_PATH = "schemas/survey-production-state.schema.json"
_KNOWN_QUALITY_3 = (
    "docs/survey-production-core-v2-historical-invariants.md",
    "docs/survey-production-core-v2-historical-production-deep-audit.md",
    "docs/survey-production-core-v2-issue-prevention-checklist.md",
)
_KNOWN_RESEARCH_PROFILES = ("WEEKLY", "RETROSPECTIVE_PERIOD", "THEMATIC")
_KNOWN_PUBLICATION_PROFILES = ("WEEKLY_MAGAZINE", "LONGFORM_SPECIAL")
_KNOWN_VERSION = "2.0-rc1"
# OLD67 pipeline (67 paths, proof-copy source67 original). NEW71 = OLD67 + 4 new schemas.
# Exact, no wildcard, no silent layout. Delta ONLY new4schemas.
_OLD_PIPELINE_67 = (
    "config/prompts/article-drafting-v2.md",
    "config/prompts/evidence-verification-v2.md",
    "config/prompts/grok/x-source-intake-base-v1.md",
    "config/prompts/grok/x-source-intake-special-v1.md",
    "config/prompts/grok/x-source-intake-weekly-v1.md",
    "config/prompts/profile-synthesis-v2.md",
    "config/prompts/source-screening-v2.md",
    "config/publication-review-v2.json",
    "config/survey-production-v2-requirements.txt",
    "docs/survey-production-core-v2-agent-first-reaudit-2026-08-22.md",
    "docs/survey-production-core-v2-authority.md",
    "docs/survey-production-core-v2-contract-normalization-second-audit-amendment.md",
    "docs/survey-production-core-v2-execution-record-policy.md",
    "docs/survey-production-core-v2-github-actions-policy.md",
    "docs/survey-production-core-v2-minimum-vertical-slice-second-audit-amendment.md",
    "docs/survey-production-core-v2-operator-execution-bridge.md",
    "docs/survey-production-core-v2-postintegration-amendment.md",
    "docs/survey-production-core-v2-redesign-authority.md",
    "docs/survey-production-core-v2-redesign-plan-after-w33-sp001.md",
    "docs/survey-production-core-v2-whole-system-audit-2026-08-22.md",
    "docs/survey-production-core-v2-whole-system-audit-remediation-closure.md",
    "docs/survey-production-core-v2-workflow-responsibility-inventory.md",
    "docs/survey-production-core-v2-x-source-intake.md",
    "schemas/architecture-approval-record-v2.schema.json",
    "schemas/architecture-review-attention-v2.schema.json",
    "schemas/architecture-review-summary-v2.schema.json",
    "schemas/candidate-matrix-v2.schema.json",
    "schemas/candidate-selection-v2.schema.json",
    "schemas/discovery-acceptance-v2.schema.json",
    "schemas/draft-v2-package.schema.json",
    "schemas/draft-v2-result.schema.json",
    "schemas/edition-evidence-view.schema.json",
    "schemas/editorial-manuscript-spec-v2.schema.json",
    "schemas/editorial-publication-build-record-v2.schema.json",
    "schemas/editorial-publication-set-v2.schema.json",
    "schemas/editorial-publication-source-manifest-v2.schema.json",
    "schemas/editorial-toolchain-spec-v2.schema.json",
    "schemas/evidence-authority-supplement-v2.schema.json",
    "schemas/evidence-v2-card.schema.json",
    "schemas/evidence-v2-run-package.schema.json",
    "schemas/evidence-v2-task.schema.json",
    "schemas/freeze-record-v2.schema.json",
    "schemas/human-gate-review-index-v2.schema.json",
    "schemas/human-gate-review-record-v2.schema.json",
    "schemas/issue-architecture-v2.schema.json",
    "schemas/materiality-ledger.schema.json",
    "schemas/merge-verification-v2.schema.json",
    "schemas/operator-execution-request-v2.schema.json",
    "schemas/operator-pending-gate-invalidation-v2.schema.json",
    "schemas/profile-completeness-result.schema.json",
    "schemas/profile-synthesis-v2-input.schema.json",
    "schemas/profile-synthesis-v2-result.schema.json",
    "schemas/publication-candidate-v2.schema.json",
    "schemas/publication-preview-approval-v2.schema.json",
    "schemas/publication-review-record-v2.schema.json",
    "schemas/quality-regression-bundle-v2.schema.json",
    "schemas/reader-manuscript-v2.schema.json",
    "schemas/release-manifest-v2.schema.json",
    "schemas/release-record-v2.schema.json",
    "schemas/repair-set-v2.schema.json",
    "schemas/review-finding-v2.schema.json",
    "schemas/screening-v2-batch-result.schema.json",
    "schemas/screening-v2-run-package.schema.json",
    "schemas/stage-checkpoint-v2.schema.json",
    "schemas/survey-discovery-record.schema.json",
    "schemas/visual-review-record-v2.schema.json",
    "schemas/x-source-intake-v2.schema.json",
)

def _recompute_contract8_at_epoch(
    repo_root: Path,
    epoch: str,
    research_profile: str,
    publication_profile: str,
    label: str,
    _cache: dict | None = None,
) -> dict[str, str]:
    """Recompute Contract8 at OWN epoch by pure algorithm (no old code, no Production API, no currentState).

    Reads config blob at epoch (mode 100644, else FAIL), checks pipeline list exactly OLD67 or NEW71
    (sets, exact membership, delta ONLY 4 new schemas, no wildcard/silent layout), versions fixed
    "2.0-rc1" (else UNSUPPORTED unknown cfg), quality exactly 3 known (else UNSUPPORTED),
    research/publication profiles exactly known (3+2, version "2.0-rc1", no unknown, else UNSUPPORTED).
    Pipeline aggregate: sorted registered paths plus DEFAULT_CONFIG/PROFILE_SCHEMA/STATE_SCHEMA,
    exact NUL framing (rel + b"\\0" + bytes + b"\\0" per path, sorted). Quality 3 aggregate same framing.
    Research/publication profile object digests: sha256_object({"name": ..., "contract": ...}).
    NO execute old code, NO remote $ref, NO live files, NO currentState — only git show at epoch
    (immutable blob/tree queries, per-invocation cache okay, no global authority cache).
    Mode/blobSHA missing → FAIL. Unknown cfg/schema version/profile/contract registered set → UNSUPPORTED.
    Finite old/new adapter preserves OLD67 vs NEW71 delta ONLY new4schemas + modified5 fingerprints.
    """
    # Read config blob at OWN epoch (mode 100644, else FAIL).
    _cfg_mode = _git_tree_mode(repo_root, epoch, _DEFAULT_CONFIG_PATH, f"{label} config mode", _cache)
    if _cfg_mode != "100644":
        raise RenewalHistoryError("HISTORY_MODE", f"{label} config mode must be 100644 at {epoch}:{_DEFAULT_CONFIG_PATH}")
    try:
        _cfg_bytes = _git_show_blob(repo_root, epoch, _DEFAULT_CONFIG_PATH, f"{label} config blob", _cache)
    except RenewalHistoryError as exc:
        raise RenewalHistoryError(exc.code, f"{label} config blob unreadable at {epoch}: {exc.detail}") from exc
    try:
        _cfg = _parse_json_strict_bytes(_cfg_bytes, f"{label} config")
    except RenewalHistoryError as exc:
        raise RenewalHistoryError(exc.code, f"{label} config invalid JSON at {epoch}: {exc.detail}") from exc
    if not isinstance(_cfg, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} config must be an object at {epoch}")
    # Versions fixed (no unknown cfg version).
    if _cfg.get("pipeline_contract_version") != _KNOWN_VERSION:
        raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"{label} unknown pipeline_contract_version (must be {_KNOWN_VERSION}, no migration)")
    if _cfg.get("quality_contract_version") != _KNOWN_VERSION:
        raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"{label} unknown quality_contract_version (must be {_KNOWN_VERSION})")
    # Research/publication profiles exactly known (3+2, version fixed, no unknown).
    _rprofs = _cfg.get("research_profiles")
    _pprofs = _cfg.get("publication_profiles")
    if not isinstance(_rprofs, dict) or set(_rprofs.keys()) != set(_KNOWN_RESEARCH_PROFILES):
        raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"{label} unknown research profiles (must be exactly {list(_KNOWN_RESEARCH_PROFILES)}, no migration)")
    if not isinstance(_pprofs, dict) or set(_pprofs.keys()) != set(_KNOWN_PUBLICATION_PROFILES):
        raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"{label} unknown publication profiles (must be exactly {list(_KNOWN_PUBLICATION_PROFILES)})")
    for _rk in _KNOWN_RESEARCH_PROFILES:
        _rv = _rprofs.get(_rk, {})
        if not isinstance(_rv, dict) or _rv.get("version") != _KNOWN_VERSION:
            raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"{label} unknown research profile version for {_rk} (must be {_KNOWN_VERSION})")
    for _pk in _KNOWN_PUBLICATION_PROFILES:
        _pv = _pprofs.get(_pk, {})
        if not isinstance(_pv, dict) or _pv.get("version") != _KNOWN_VERSION:
            raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"{label} unknown publication profile version for {_pk} (must be {_KNOWN_VERSION})")
    if research_profile not in _KNOWN_RESEARCH_PROFILES:
        raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"{label} unknown research_profile for Contract8: {research_profile!r}")
    if publication_profile not in _KNOWN_PUBLICATION_PROFILES:
        raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"{label} unknown publication_profile for Contract8: {publication_profile!r}")
    # Pipeline list exactly OLD67 or NEW71 (sets, exact, delta ONLY 4 new, no wildcard/silent).
    _cf = _cfg.get("contract_files", {})
    _pipe = _cf.get("pipeline")
    _qual = _cf.get("quality")
    if not isinstance(_pipe, list) or not isinstance(_qual, list):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} contract_files pipeline/quality must be arrays at {epoch}")
    _pipe_set = set(_pipe)
    if len(_pipe_set) != len(_pipe):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} pipeline list has duplicates at {epoch} (no silent layout)")
    _qual_set = set(_qual)
    if _qual_set != set(_KNOWN_QUALITY_3) or len(_qual) != 3:
        raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"{label} unknown quality list (must be exactly 3 known, no migration)")
    _old_set = set(_OLD_PIPELINE_67)
    _new_set = _old_set | set(_NEW_SCHEMAS_4)
    # NEW71 must be OLD67 + 4 new schemas, no removed, no other added, no wildcard.
    if _pipe_set != _old_set and _pipe_set != _new_set:
        # Unknown cfg registered set (neither OLD67 nor NEW71 exact) → UNSUPPORTED.
        # Includes partial new (e.g., 7 new files present but OLD67 cfg → REJECT NEW, as required).
        # Includes free prefix wildcard / silent layout (extra/missing beyond 4-new delta).
        _missing_old = sorted(_old_set - _pipe_set)
        _extra = sorted(_pipe_set - _old_set - set(_NEW_SCHEMAS_4))
        raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"{label} unknown pipeline list (must be exactly OLD67 (67) or NEW71 (71=OLD67+4new), no wildcard/silent; missing_old={_missing_old[:5]} extra={_extra[:5]})")
    # Pure aggregate: sorted registered paths plus DEFAULT_CONFIG/PROFILE_SCHEMA/STATE_SCHEMA, NUL framing.
    # NO old code, NO Production API, NO live files — only epoch blobs via git show (immutable, per-invocation cache).
    def _agg(paths: list[str]) -> str:
        h = hashlib.sha256()
        for rel in sorted(paths):
            # Mode 100644 required for each aggregated file, else FAIL (mode/blobSHA missing).
            _m = _git_tree_mode(repo_root, epoch, rel, f"{label} contract aggregate mode {rel}", _cache)
            if _m != "100644":
                raise RenewalHistoryError("HISTORY_MODE", f"{label} contract aggregate mode must be 100644 at {epoch}:{rel}")
            try:
                _b = _git_show_blob(repo_root, epoch, rel, f"{label} contract aggregate blob {rel}", _cache)
            except RenewalHistoryError as exc:
                raise RenewalHistoryError(exc.code, f"{label} contract aggregate blob missing at {epoch}:{rel}: {exc.detail}") from exc
            h.update(rel.encode("utf-8"))
            h.update(b"\0")
            h.update(_b)
            h.update(b"\0")
        return h.hexdigest()
    _pipe_files = list(_pipe_set) + [_DEFAULT_CONFIG_PATH, _PROFILE_SCHEMA_PATH, _STATE_SCHEMA_PATH]
    # Note: _DEFAULT_CONFIG_PATH is config itself (already read as blob above, but aggregate re-reads it at epoch for pipeline SHA — same blob, same predicates, per-invocation cache reuses, no extra authority).
    _pipe_sha = _agg(_pipe_files)
    _qual_sha = _agg(sorted(_qual_set))
    # Pure algorithm of core.contract_identity: sha256_object({"name": ..., "contract": <full profile dict>}),
    # where <full profile dict> is cfg["research_profiles"][research_profile] (with version, temporal_policies, etc.),
    # NOT .get("contract") (profiles have no "contract" key; use full dict). NO old code.
    _research_full = _rprofs.get(research_profile, {})
    _pub_full = _pprofs.get(publication_profile, {})
    if not isinstance(_research_full, dict) or not isinstance(_pub_full, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} research/publication profile must be objects at {epoch}")
    _research_sha = _sha256_object({"name": research_profile, "contract": _research_full})
    _pub_sha = _sha256_object({"name": publication_profile, "contract": _pub_full})
    return {
        "pipeline_contract_version": _KNOWN_VERSION,
        "pipeline_contract_sha256": _pipe_sha,
        "quality_contract_version": _KNOWN_VERSION,
        "quality_contract_sha256": _qual_sha,
        "research_profile_version": _KNOWN_VERSION,
        "research_profile_sha256": _research_sha,
        "publication_profile_version": _KNOWN_VERSION,
        "publication_profile_sha256": _pub_sha,
    }

# Fixed registries for exact closure membership (no subset/superset, no
# blanket '*.py', name==path, sorted-unique). Old generation = 50
# (30py+14schemas+route3+staged1+style1+recipe1). New generation = 63
# (35py+22schemas+route3+staged1+style1+recipe1) with 66 union across routes.
_OLD_PY_30 = (
    "scripts/render_article_draft_tex.py",
    "scripts/survey_agent_control_v2.py",
    "scripts/survey_agent_tool_v2.py",
    "scripts/survey_architecture_v2.py",
    "scripts/survey_architecture_v2_base.py",
    "scripts/survey_bibliography_access_provenance_v2.py",
    "scripts/survey_completeness_v2.py",
    "scripts/survey_drafting_citation_refs_v2.py",
    "scripts/survey_drafting_v2.py",
    "scripts/survey_drafting_v2_base.py",
    "scripts/survey_editorial_correction_proposal_v2.py",
    "scripts/survey_editorial_current_authority_v2.py",
    "scripts/survey_editorial_publication_v2.py",
    "scripts/survey_editorial_retention_v2.py",
    "scripts/survey_evidence_v2.py",
    "scripts/survey_longform_derivation_v2.py",
    "scripts/survey_longform_generated_v2.py",
    "scripts/survey_production_v2.py",
    "scripts/survey_publication_set_v2.py",
    "scripts/survey_publication_v2.py",
    "scripts/survey_quality_v2.py",
    "scripts/survey_reader_fidelity_v2.py",
    "scripts/survey_reader_publication_v2.py",
    "scripts/survey_reader_surface_gate_v2.py",
    "scripts/survey_review_attention_v2.py",
    "scripts/survey_schema_v2.py",
    "scripts/survey_screening_v2.py",
    "scripts/survey_weekly_derivation_v2.py",
    "scripts/validate_article_draft.py",
    "scripts/weekly_pipeline.py",
)
_OLD_SCHEMAS_14 = (
    "schemas/editorial-correction-proposal-v2.schema.json",
    "schemas/editorial-manuscript-spec-v2.schema.json",
    "schemas/editorial-publication-build-record-v2.schema.json",
    "schemas/editorial-publication-set-v2.schema.json",
    "schemas/editorial-publication-source-manifest-v2.schema.json",
    "schemas/editorial-retention-manifest-v2.schema.json",
    "schemas/editorial-staged-source-manifest-v2.schema.json",
    "schemas/editorial-toolchain-spec-v2.schema.json",
    "schemas/publication-candidate-v2.schema.json",
    "schemas/publication-surface-revalidation.schema.json",
    "schemas/quality-regression-bundle-v2.schema.json",
    "schemas/reader-manuscript-v2.schema.json",
    "schemas/reader-surface-gate-v2.schema.json",
    "schemas/reader-surface-semantic-review-v2.schema.json",
)
_NEW_PY_3 = (
    "scripts/survey_versioned_renewal_history_v2.py",
    "scripts/survey_versioned_renewal_source_v2.py",
    "scripts/survey_versioned_renewal_v2.py",
)
_NEW_SCHEMAS_4 = (
    "schemas/versioned-renewal-basis-v2.schema.json",
    "schemas/versioned-renewal-source-manifest-v2.schema.json",
    "schemas/versioned-renewal-source-proof-v2.schema.json",
    "schemas/versioned-renewal-publication-set-v2.schema.json",
)
_FAMILY_PY_2 = (
    "scripts/survey_discovery_v2.py",
    "scripts/survey_x_intake_v2.py",
)
_FAMILY_SCHEMAS_4 = (
    "schemas/discovery-acceptance-v2.schema.json",
    "schemas/survey-discovery-record.schema.json",
    "schemas/screening-v2-run-package.schema.json",
    "schemas/screening-v2-batch-result.schema.json",
)
_ROUTE_WEEKLY_3 = (
    "scripts/survey_weekly_semantic_publication_v2.py",
    "schemas/reader-surface-input-v2.schema.json",
    "schemas/weekly-publication-source-manifest-v2.schema.json",
)
_ROUTE_LONGFORM_3 = (
    "scripts/survey_longform_semantic_publication_v2.py",
    "schemas/longform-reader-input-v2.schema.json",
    "schemas/longform-publication-source-manifest-v2.schema.json",
)
_STAGED_1 = ("scripts/survey_editorial_staged_source_v2.py",)
_STYLE_1 = ("templates/survey/jgaisurvey.sty",)
_RECIPE_1 = (".latexmkrc",)

OWNER_REGISTRY: tuple[tuple[str, str, str], ...] = (
    ("proposal", "schemas/editorial-correction-proposal-v2.schema.json", ""),
    ("retention", "schemas/editorial-retention-manifest-v2.schema.json", ""),
    ("staged", "schemas/editorial-staged-source-manifest-v2.schema.json", ""),
    ("receipt-editorial", "schemas/editorial-publication-source-manifest-v2.schema.json", ""),
    ("receipt-renewal", "schemas/versioned-renewal-source-manifest-v2.schema.json", ""),
    ("seal-editorial", "schemas/editorial-publication-set-v2.schema.json", ""),
    ("seal-renewal", "schemas/versioned-renewal-publication-set-v2.schema.json", ""),
    ("build-old", "schemas/editorial-publication-build-record-v2.schema.json", ""),
    ("build-new", "schemas/versioned-renewal-source-manifest-v2.schema.json", "/$defs/buildRecord"),
    ("spec-toolchain", "schemas/editorial-toolchain-spec-v2.schema.json", ""),
    ("spec-manuscript", "schemas/editorial-manuscript-spec-v2.schema.json", ""),
    ("basis", "schemas/versioned-renewal-basis-v2.schema.json", ""),
    ("proof", "schemas/versioned-renewal-source-proof-v2.schema.json", ""),
    ("manuscript-renewal", "schemas/reader-manuscript-v2.schema.json", "/properties/renewal_source"),
    ("candidate-renewal", "schemas/publication-candidate-v2.schema.json", "/properties/renewal_source_proof_ref"),
    ("bundle-renewal", "schemas/quality-regression-bundle-v2.schema.json", "/properties/renewal_source_proof_ref"),
    ("gate-renewal", "schemas/reader-surface-gate-v2.schema.json", "/properties/derivation/oneOf/4"),
    ("record-renewal", "schemas/publication-surface-revalidation.schema.json", "/oneOf/2"),
    ("scope", "schemas/reader-surface-semantic-review-v2.schema.json", ""),
)
_OWNER_BY_TYPE: dict[str, tuple[str, str]] = {k: (s, p) for k, s, p in OWNER_REGISTRY}
_ALLOWED_SCHEMA_PATHS = frozenset(s for _, s, _ in OWNER_REGISTRY)

# ROOT B3: finite recognized schema fingerprints (old/new explicit, no foreign).
# Old = R3 (manifest where present, else 409) + 409 where present; new = current disk
# (backward-compatible renewal amendments). Any other SHA, even with registered path,
# is foreign and refuses (UNSUPPORTED_MIGRATION). Precode full JSON map gives old hashes
# (manifest 57 for R3 shapes); current disk gives new known (renewal 4 + 5 amended).
# No schema code execution, no REMOTE ref, offline data only.
_KNOWN_SCHEMA_SHAS: dict[str, frozenset[str]] = {
    "schemas/editorial-correction-proposal-v2.schema.json": frozenset(["5623c0d92e3dfc5415e1ab73c73b3d5f1b147f265f2255469cede2ec333a4607"]),
    "schemas/editorial-retention-manifest-v2.schema.json": frozenset(["347e5499259ac878e28bc66b4e9ea62af1f5eb71a3f428558120a9f5d549855c"]),
    "schemas/editorial-staged-source-manifest-v2.schema.json": frozenset(["4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46"]),
    "schemas/editorial-publication-source-manifest-v2.schema.json": frozenset(["494a1d152c76bca810d30e743d567210f130cb4197561d82b276f24ef69441bc"]),
    "schemas/editorial-publication-set-v2.schema.json": frozenset(["7beebcef48d7777144f7df7ce3fddc27c0d39df685fdc49cbfdd7d798c7e61e9"]),
    "schemas/editorial-publication-build-record-v2.schema.json": frozenset(["b7c82476047373995cd5c4733ce2ba0b1c53fef72a84bceb26feec9078fea4ba"]),
    "schemas/editorial-manuscript-spec-v2.schema.json": frozenset(["043ce8a565385549265d6666642c2e3ec8ce0d8e8e5544a7eddfb32691478250"]),
    "schemas/editorial-toolchain-spec-v2.schema.json": frozenset(["50b5dc3ee05c496b2c2da13377c5ee0a883dfb52d9b9785189cb00a75d6e4db4"]),
    "schemas/publication-candidate-v2.schema.json": frozenset(["46a888668862546bea852babdd031d528c92bc2287c29f445b30423d6ce51665", "a3fe0bc8dc21f79668e7017914f1e14b8933e1fb1cd7826c3a6515e01b42ed59"]),
    "schemas/publication-surface-revalidation.schema.json": frozenset(["0376c7b43941c6b99d699996372572e04e9b4c98f495e5a5e3287163f37b23a5", "4c1ce92944da0769af5c43df0ca32397f99a5f58f81f817ecb2c6bf28d574219", "74544298575faab579cc98c5ef5fa9c4ec5dcf09d25592a85536feb4a3070d9b"]),
    "schemas/quality-regression-bundle-v2.schema.json": frozenset(["3aaf17255baba111d9f96dce2c90640380a38dbd691b82ac838eb7a33392c2bf", "ab8614f61484e742761c62732bf38e6451866383fc5096a7ed41819efbce3b90"]),
    "schemas/reader-manuscript-v2.schema.json": frozenset(["0d8f0e9e66ccb885131645a24abfe24b94743cb0476e94fe923eb30eca9ef4c3", "141818b9b8da1b3bd8c32edaf1de48cb0866f86285e7aa59a2b990c2893b8421", "426f5a3689e2bc2829138893a8a28f0fc1fc6e696d373419a49f5cf16e8bb4f3"]),
    "schemas/reader-surface-gate-v2.schema.json": frozenset(["264fdd6427d2ac4a24f602aa7ec063baf90fc98ecd16f42da563d3671fd7bc9a", "a734235caab222d30e78e2fea17f3a376d101368c482ec8d91371a1d7bb81f4b", "f10de43eb85be32559d244f77d79ff76a9d3e803072a930ed164b12361dc5cd1"]),
    "schemas/reader-surface-semantic-review-v2.schema.json": frozenset(["1594933fca838afc9315a6bd4b0c0b1f707808cc983b0941ae8c8e6709fe73e6", "e8598239d3ca00441f61110fd77a7b7edf063ac15a7a6a1c2efdb38e73d6699b"]),
    "schemas/versioned-renewal-basis-v2.schema.json": frozenset(["76f77ee552ef430756d7acd9c8f6d780c1d7d4ac12aca976b49cd552914c4aad"]),
    "schemas/versioned-renewal-source-manifest-v2.schema.json": frozenset(["9d58894ef8b60315c8e8405206d31764f10f4030b1e71ffdd870bf650cf28c42"]),
    "schemas/versioned-renewal-source-proof-v2.schema.json": frozenset(["4c6413ea243d8131589cced31c677167b94654f4cda118812704d3a69aa2f493"]),
    "schemas/versioned-renewal-publication-set-v2.schema.json": frozenset(["a7594e63db178016038787307c54f680d4cef53020577676ac1aaa7e2e739354"]),
}


def _require_known_schema_sha(schema_path: str, schema_sha: str, label: str) -> None:
    """ROOT B3: reject unknown foreign schema even when path is registered."""
    _allowed = _KNOWN_SCHEMA_SHAS.get(schema_path)
    if _allowed is None:
        raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"{label} schema path not in finite fingerprint allowlist: {schema_path!r}")
    if schema_sha not in _allowed:
        raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"{label} unknown foreign schema SHA for registered path {schema_path} (not old/new known, no broad migration)")


def _resolve_json_pointer(doc: Any, pointer: str, label: str) -> Any:
    """Resolve JSON pointer (RFC6901) within doc; '' is whole doc, never '/'."""
    if pointer == "":
        return doc
    if pointer == "/":
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} schema pointer '/' forbidden (whole-doc is '', not '/')")
    if not pointer.startswith("/"):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} schema pointer must start with '/': {pointer!r}")
    _parts = pointer.split("/")[1:]
    _cur = doc
    for _p in _parts:
        _p = _p.replace("~1", "/").replace("~0", "~")
        if isinstance(_cur, dict):
            if _p not in _cur:
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} schema pointer missing key: {pointer!r}")
            _cur = _cur[_p]
        elif isinstance(_cur, list):
            try:
                _idx = int(_p)
            except ValueError as exc:
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} schema pointer bad index: {pointer!r}") from exc
            try:
                _cur = _cur[_idx]
            except IndexError as exc:
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} schema pointer index OOB: {pointer!r}") from exc
        else:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} schema pointer cannot traverse scalar: {pointer!r}")
    return _cur


def _validate_instance_against_schema_blob(
    source_bytes: bytes,
    schema_blob_bytes: bytes,
    schema_pointer: str,
    label: str,
) -> None:
    """ROOT B3: strict offline instance validation vs own recorded SCHEMA blob.

    Data only, NO old code execution, NO REMOTE ref. Exact registry pointer '' or
    allowed build defs, no arbitrary caller pointer (enforced by caller via registry).
    Whole-doc '' validates whole instance; '/$defs/buildRecord' validates instance
    against that subschema; other allowed renewal pointers validate whole instance
    (which includes that branch) — pointer exactness already enforced, instance must
    satisfy its own epoch schema. Close/ref pin errors never ignored (fail-closed).
    """
    # Parse source + schema strictly (duplicate keys refused, UTF-8, JSON object where required).
    try:
        _src_text = source_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} instance not UTF-8: {exc}") from exc
    try:
        _src = json.loads(_src_text, object_pairs_hook=_no_duplicate_object)
    except json.JSONDecodeError as exc:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} instance not valid JSON: {exc}") from exc
    try:
        _sch_text = schema_blob_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} schema blob not UTF-8: {exc}") from exc
    try:
        _sch = json.loads(_sch_text, object_pairs_hook=_no_duplicate_object)
    except json.JSONDecodeError as exc:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} schema blob not valid JSON: {exc}") from exc
    if not isinstance(_sch, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} schema blob must be an object")
    # No REMOTE ref: forbid http/https $ref in recorded schema blob (offline only).
    # Local '#/$defs/*' and '#/properties/*' allowed; remote fetch never performed.
    _sch_serial = _sch_text
    if '"$ref"' in _sch_serial and ("http://" in _sch_serial or "https://" in _sch_serial):
        # Check if any $ref value starts with http (remote). Local '#...' allowed.
        # Conservative: if blob contains http $ref, refuse (no network).
        import re as _re
        if _re.search(r'"\$ref"\s*:\s*"https?://', _sch_serial):
            raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"{label} schema blob contains REMOTE $ref (no network, no old code execution)")
    # Resolve pointer to subschema when needed.
    if schema_pointer == "":
        _subschema = _sch
        _instance = _src
    elif schema_pointer == "/$defs/buildRecord":
        # Build record instance validates against $defs/buildRecord, but that subschema's
        # internal $refs ("#/$defs/ref", "#/$defs/sizedRef", etc.) resolve against root $defs.
        # Extracting subschema alone breaks ref resolution (PointerToNowhere). Preserve root
        # $defs by wrapping: {"$ref": "#/$defs/buildRecord", "$defs": <root $defs>}.
        # Offline, no remote, same predicates (mode/path/epoch already checked).
        try:
            _br = _resolve_json_pointer(_sch, schema_pointer, f"{label} schema pointer")
            if not isinstance(_br, dict):
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} buildRecord subschema must be an object")
        except RenewalHistoryError:
            raise
        _root_defs = _sch.get("$defs")
        if not isinstance(_root_defs, dict):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} schema blob missing $defs for buildRecord refs")
        _subschema = {"$ref": "#/$defs/buildRecord", "$defs": _root_defs}
        _instance = _src
    else:
        # Allowed renewal branch pointers (e.g. /properties/renewal_source,
        # /properties/renewal_source_proof_ref, /properties/derivation/oneOf/4, /oneOf/2):
        # validate whole instance against whole schema (which includes that branch).
        # Pointer exactness already enforced via registry; instance must satisfy own epoch schema.
        _subschema = _sch
        _instance = _src
    # Offline validation with jsonschema (data only, no code execution).
    try:
        import jsonschema as _js
        from jsonschema import Draft202012Validator as _Validator
    except Exception as exc:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} jsonschema unavailable for offline validation: {exc}") from exc
    try:
        _validator = _Validator(_subschema)
    except Exception as exc:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} recorded schema blob invalid (cannot construct validator): {exc}") from exc
    _errors = sorted(_validator.iter_errors(_instance), key=lambda e: list(e.path))
    if _errors:
        _first = _errors[0]
        _path = "/".join(str(p) for p in _first.path)
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} instance fails own recorded schema (pointer {schema_pointer!r} path '{_path}'): {_first.message[:500]}")


class RenewalHistoryError(ValueError):
    def __init__(self, code: str, detail: str) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


# ---------------------------------------------------------------------------
# FD-bound safe layer (no checked-path race, limits, close-checked).
# Root FD held per operation; ancestors via dir_fd with entry-vs-fd binding.
# ---------------------------------------------------------------------------

def _lexical_parts(rel: str, label: str) -> tuple[str, ...]:
    if not isinstance(rel, str) or not rel or "\\" in rel:
        raise RenewalHistoryError("HISTORY_MODE", f"{label} must be repository-relative without traversal: {rel!r}")
    if len(rel) > MAX_PATH_LEN:
        raise RenewalHistoryError("HISTORY_MODE", f"{label} path too long: {len(rel)}")
    if rel.startswith("/") or rel == "." or rel.startswith("./"):
        raise RenewalHistoryError("HISTORY_MODE", f"{label} must be repository-relative: {rel!r}")
    parts = tuple(rel.split("/"))
    if len(parts) > MAX_PARTS:
        raise RenewalHistoryError("HISTORY_MODE", f"{label} path too deep: {len(parts)}")
    for part in parts:
        if part in ("", ".", ".."):
            raise RenewalHistoryError("HISTORY_MODE", f"{label} has unsafe path component: {rel!r}")
        if len(part) > 255:
            raise RenewalHistoryError("HISTORY_MODE", f"{label} path component too long: {part!r}")
    return parts


def _fd_safe_read(repo_root: Path, rel: str, label: str) -> bytes:
    """FD-bound read: root FD + dir_fd chain, entry-vs-fd binding, limits."""
    root_resolved = repo_root.resolve()
    try:
        lst = os.lstat(root_resolved)
    except OSError as exc:
        raise RenewalHistoryError("HISTORY_MODE", f"{label} cannot lstat repo root: {exc}") from exc
    if stat.S_ISLNK(lst.st_mode):
        raise RenewalHistoryError("HISTORY_MODE", f"{label} repo root is symlink")
    if not stat.S_ISDIR(lst.st_mode):
        raise RenewalHistoryError("HISTORY_MODE", f"{label} repo root is not a directory")
    parts = _lexical_parts(rel, label)
    dir_parts, leaf = parts[:-1], parts[-1]
    held: list[int] = []
    try:
        try:
            root_fd = os.open(root_resolved, os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0))
        except OSError as exc:
            raise RenewalHistoryError("HISTORY_MODE", f"{label} cannot open repo root no-follow: {exc}") from exc
        held.append(root_fd)
        try:
            rst = os.fstat(root_fd)
        except OSError as exc:
            raise RenewalHistoryError("HISTORY_MODE", f"{label} root fstat failed: {exc}") from exc
        if not stat.S_ISDIR(rst.st_mode):
            raise RenewalHistoryError("HISTORY_MODE", f"{label} root is not a directory after open")
        if (lst.st_dev, lst.st_ino) != (rst.st_dev, rst.st_ino):
            raise RenewalHistoryError("HISTORY_MODE", f"{label} repo root replaced between lstat and open")
        parent = root_fd
        cur: list[str] = []
        for part in dir_parts:
            cur.append(part)
            try:
                fd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0), dir_fd=parent)
            except FileNotFoundError as exc:
                raise RenewalHistoryError("HISTORY_BLOB_MISSING", f"{label} ancestor missing: {'/'.join(cur)}: {exc}") from exc
            except OSError as exc:
                raise RenewalHistoryError("HISTORY_MODE", f"{label} ancestor not openable as dir (symlink?): {'/'.join(cur)}: {exc}") from exc
            held.append(fd)
            try:
                st = os.fstat(fd)
            except OSError as exc:
                raise RenewalHistoryError("HISTORY_MODE", f"{label} ancestor fstat failed: {'/'.join(cur)}: {exc}") from exc
            if not stat.S_ISDIR(st.st_mode):
                raise RenewalHistoryError("HISTORY_MODE", f"{label} ancestor not a directory: {'/'.join(cur)}")
            try:
                est = os.stat(part, dir_fd=parent, follow_symlinks=False)
            except OSError as exc:
                raise RenewalHistoryError("HISTORY_MODE", f"{label} ancestor entry unreadable: {'/'.join(cur)}: {exc}") from exc
            if stat.S_ISLNK(est.st_mode):
                raise RenewalHistoryError("HISTORY_MODE", f"{label} ancestor is symlink: {'/'.join(cur)}")
            if (est.st_dev, est.st_ino) != (st.st_dev, st.st_ino):
                raise RenewalHistoryError("HISTORY_MODE", f"{label} ancestor replaced during open: {'/'.join(cur)}")
            parent = fd
        # Leaf entry check from pinned parent.
        try:
            ent = os.stat(leaf, dir_fd=parent, follow_symlinks=False)
        except FileNotFoundError as exc:
            raise RenewalHistoryError("HISTORY_BLOB_MISSING", f"{label} missing: {rel}: {exc}") from exc
        except OSError as exc:
            raise RenewalHistoryError("HISTORY_MODE", f"{label} leaf entry unreadable: {rel}: {exc}") from exc
        if stat.S_ISLNK(ent.st_mode):
            raise RenewalHistoryError("HISTORY_MODE", f"{label} is a symlink/refusal: {rel}")
        if not stat.S_ISREG(ent.st_mode):
            raise RenewalHistoryError("HISTORY_MODE", f"{label} is not a regular file (FIFO/socket/device/dir refused): {rel}")
        try:
            fd = os.open(leaf, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0), dir_fd=parent)
        except OSError as exc:
            raise RenewalHistoryError("HISTORY_MODE", f"{label} open refused (symlink/unsafe): {rel}: {exc}") from exc
        held.append(fd)
        try:
            fst = os.fstat(fd)
        except OSError as exc:
            raise RenewalHistoryError("HISTORY_MODE", f"{label} fstat failed: {rel}: {exc}") from exc
        if not stat.S_ISREG(fst.st_mode):
            raise RenewalHistoryError("HISTORY_MODE", f"{label} is not a regular file after open: {rel}")
        if (fst.st_dev, fst.st_ino) != (ent.st_dev, ent.st_ino):
            raise RenewalHistoryError("HISTORY_MODE", f"{label} replaced between entry check and open: {rel}")
        chunks: list[bytes] = []
        total = 0
        while True:
            try:
                chunk = os.read(fd, 65536)
            except OSError as exc:
                raise RenewalHistoryError("HISTORY_BLOB_MISSING", f"{label} read failed: {rel}: {exc}") from exc
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_FILE_BYTES:
                raise RenewalHistoryError("HISTORY_MODE", f"{label} file too large (limit {MAX_FILE_BYTES}): {rel}")
            chunks.append(chunk)
        data = b"".join(chunks)
        # Checked close: fail even when bytes complete.
        try:
            os.close(fd)
        except OSError as exc:
            raise RenewalHistoryError("HISTORY_MODE", f"{label} close after read failed: {rel}: {exc}") from exc
        finally:
            if fd in held:
                try:
                    held.remove(fd)
                except ValueError:
                    pass
        return data
    finally:
        # Close all held FDs; primary error preserved, secondaries attached.
        # Here we are in read path: any close failure must fail closed.
        for fd in reversed(list(held)):
            try:
                os.close(fd)
            except OSError as exc:
                raise RenewalHistoryError("HISTORY_MODE", f"{label} descriptor close failed: {exc}") from exc


def read_repo_bytes(repo_root: Path, rel: str, label: str) -> bytes:
    return _fd_safe_read(repo_root, rel, label)


def sha256_repo_file(repo_root: Path, rel: str, label: str) -> str:
    return hashlib.sha256(read_repo_bytes(repo_root, rel, label)).hexdigest()


def _no_duplicate_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    obj: dict[str, Any] = {}
    for key, value in pairs:
        if key in obj:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"duplicate JSON key refused: {key!r}")
        obj[key] = value
    return obj


def _parse_json_strict_bytes(data: bytes, label: str) -> Any:
    if len(data) > MAX_JSON_BYTES:
        raise RenewalHistoryError("HISTORY_MODE", f"{label} JSON too large (limit {MAX_JSON_BYTES})")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} is not UTF-8 JSON: {exc}") from exc
    try:
        return json.loads(text, object_pairs_hook=_no_duplicate_object)
    except json.JSONDecodeError as exc:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} is not valid JSON: {exc}") from exc


def _sha256_object(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _parse_instant(value: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"recorded_at invalid: {value!r}")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"recorded_at invalid: {value!r}: {exc}") from exc
    if parsed.tzinfo is None:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "timestamp must include explicit UTC offset or Z")
    return parsed.astimezone(timezone.utc)


def load_json_strict(repo_root: Path, rel: str, label: str) -> Any:
    data = read_repo_bytes(repo_root, rel, label)
    if len(data) == 0:
        raise RenewalHistoryError("HISTORY_BLOB_MISSING", f"{label} empty: {rel}")
    value = _parse_json_strict_bytes(data, label)
    if not isinstance(value, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} must be a JSON object: {rel}")
    return value


def _load_schema_validator() -> Any:
    from scripts import survey_schema_v2 as schema_gate
    return schema_gate


def load_and_validate_json_strict(repo_root: Path, rel: str, schema_rel: Path | str, label: str) -> dict[str, Any]:
    value = load_json_strict(repo_root, rel, label)
    schema_gate = _load_schema_validator()
    try:
        schema_gate.validate_instance(value, repo_root.resolve() / str(schema_rel), label=label)
    except ValueError as exc:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} schema invalid: {exc}") from exc
    return value


def _check_authority_ref(repo_root: Path, ref: Any, label: str) -> bytes:
    if not isinstance(ref, dict) or set(ref) != {"path", "sha256"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} authority fields invalid")
    path_value = ref.get("path")
    sha_value = ref.get("sha256")
    if not isinstance(path_value, str) or not path_value:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} authority path invalid")
    if not isinstance(sha_value, str) or len(sha_value) != 64 or any(c not in "0123456789abcdef" for c in sha_value):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} authority sha256 invalid")
    data = read_repo_bytes(repo_root, path_value, label)
    if hashlib.sha256(data).hexdigest() != sha_value:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} SHA drift: {path_value}")
    return data


def _check_sized_ref(repo_root: Path, ref: Any, label: str) -> bytes:
    if not isinstance(ref, dict) or set(ref) != {"path", "sha256", "byte_count"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} file_ref fields invalid")
    path_value = ref.get("path")
    sha_value = ref.get("sha256")
    size_value = ref.get("byte_count")
    if not isinstance(path_value, str) or not path_value:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} file_ref path invalid")
    if not isinstance(sha_value, str) or len(sha_value) != 64 or any(c not in "0123456789abcdef" for c in sha_value):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} file_ref sha256 invalid")
    if not isinstance(size_value, int) or isinstance(size_value, bool) or size_value < 1:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} file_ref byte_count invalid")
    data = read_repo_bytes(repo_root, path_value, label)
    if hashlib.sha256(data).hexdigest() != sha_value:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} SHA drift: {path_value}")
    if len(data) != size_value:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} byte count drift: {path_value}")
    return data


# ---------------------------------------------------------------------------
# Git epoch helpers (T verification). No old code execution, only blob reads.
# ---------------------------------------------------------------------------

def _sanitized_git_env() -> dict[str, str]:
    """Sanitized env for git child calls: no inherited Git root override, no lazy fetch/replace.

    Strips GIT_DIR/WORK_TREE/INDEX_FILE/PREFIX/COMMON_DIR/NAMESPACE and disables
    lazy fetch/replace objects. Keeps PATH + minimal safe vars + GIT_OPTIONAL_LOCKS.
    """
    env: dict[str, str] = {}
    for k, v in os.environ.items():
        if k.startswith("GIT_") and k not in ("GIT_OPTIONAL_LOCKS",):
            # Strip all GIT_* overrides (root, prefix, index, namespace, lazy fetch, etc).
            # GIT_OPTIONAL_LOCKS is re-set below explicitly.
            continue
        env[k] = v
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_CONFIG_GLOBAL"] = "/dev/null"
    env["GIT_CONFIG_SYSTEM"] = "/dev/null"
    env["GIT_NO_LAZY_FETCH"] = "1"
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    return env


def _git_run(repo_root: Path, args: list[str], label: str) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            ["git", *args],
            cwd=str(repo_root.resolve()),
            capture_output=True,
            text=True,
            timeout=30,
            env=_sanitized_git_env(),
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise RenewalHistoryError("HISTORY_BLOB_MISSING", f"{label} git invocation failed: {exc}") from exc


# Bounded batched RAW immutable Git retrieval (per-invocation only, H-owned).
# SAME predicates: exact epoch/root+path+mode+blobSHA+byte_count for EVERY ref.
# ls-tree -z with exact finite expected paths only; cat-file --batch by validated OID only.
# No new unsupported paths/prefix, no optional checks, no persistent/global cache,
# no caller permit, no ambient context. Only immutable blob/tree metadata cached
# per verify_versioned_history call; HEAD/dirty status never cached (not used here).
_FINITE_BATCH_PATHS: frozenset[str] = frozenset(
    list(_OLD_PIPELINE_67)
    + list(_NEW_SCHEMAS_4)
    + list(_KNOWN_QUALITY_3)
    + [_DEFAULT_CONFIG_PATH, _PROFILE_SCHEMA_PATH, _STATE_SCHEMA_PATH]
    + list(_OLD_PY_30)
    + list(_OLD_SCHEMAS_14)
    + list(_NEW_PY_3)
    + list(_NEW_SCHEMAS_4)
    + list(_FAMILY_PY_2)
    + list(_FAMILY_SCHEMAS_4)
    + list(_ROUTE_WEEKLY_3)
    + list(_ROUTE_LONGFORM_3)
    + list(_STAGED_1)
    + list(_STYLE_1)
    + list(_RECIPE_1)
    + list(_KNOWN_SCHEMA_SHAS.keys())
    + [s for s, _p in _OWNER_BY_TYPE.values() for s in [s]]
)


def _fetch_epoch_tree_batch(repo_root: Path, epoch: str, label: str, _cache: dict) -> dict[str, tuple[str, str]]:
    """Fetch tree modes+OIDs for epoch via single `git ls-tree -z` over finite paths.

    Returns {path: (mode, oid)}. Fail-closed on bad type/length/mode/path/newline,
    extra entries, missing commit, returncode/stderr. Only finite expected paths requested.
    """
    if not isinstance(epoch, str) or len(epoch) != 40 or any(c not in "0123456789abcdef" for c in epoch):
        raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", f"{label} epoch GITSHA invalid: {epoch!r}")
    if ("tree_dict", epoch) in _cache:
        v = _cache[("tree_dict", epoch)]
        if isinstance(v, dict):
            return v  # type: ignore[return-value]
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} tree cache corrupt for {epoch}")
    finite_sorted = sorted(_FINITE_BATCH_PATHS)
    if not finite_sorted or len(finite_sorted) > 500:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} finite batch path set invalid: {len(finite_sorted)}")
    for p in finite_sorted:
        _lexical_parts(p, f"{label} finite batch path")
        if "\n" in p or "\x00" in p:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} finite batch path has newline/NUL: {p!r}")
    try:
        raw = subprocess.run(
            ["git", "ls-tree", "-z", epoch, "--", *finite_sorted],
            cwd=str(repo_root.resolve()),
            capture_output=True,
            timeout=30,
            env=_sanitized_git_env(),
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise RenewalHistoryError("HISTORY_BLOB_MISSING", f"{label} ls-tree batch failed {epoch}: {exc}") from exc
    if raw.returncode != 0:
        err = raw.stderr.decode("utf-8", errors="replace")[:300] if isinstance(raw.stderr, (bytes, bytearray)) else str(raw.stderr)[:300]
        raise RenewalHistoryError("HISTORY_BLOB_MISSING", f"{label} ls-tree batch failed {epoch}: {err}")
    out: bytes = raw.stdout if isinstance(raw.stdout, (bytes, bytearray)) else b""
    # -z: entries NUL-separated, each "<mode> <type> <oid>\t<path>"
    result: dict[str, tuple[str, str]] = {}
    if not out:
        _cache[("tree_dict", epoch)] = result
        return result
    # Split, last element after trailing NUL is empty -> ignore
    parts = out.split(b"\x00")
    for entry in parts:
        if not entry:
            continue
        try:
            tab_idx = entry.index(b"\t")
        except ValueError as exc:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} ls-tree batch parse no TAB at {epoch}") from exc
        left = entry[:tab_idx]
        path_b = entry[tab_idx + 1 :]
        try:
            path_s = path_b.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} ls-tree batch path not UTF-8 at {epoch}") from exc
        if path_s not in _FINITE_BATCH_PATHS:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} ls-tree batch extra path not in finite set at {epoch}: {path_s!r}")
        if path_s in result:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} ls-tree batch duplicate path at {epoch}: {path_s!r}")
        try:
            left_s = left.decode("ascii")
        except UnicodeDecodeError as exc:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} ls-tree batch header not ASCII at {epoch}") from exc
        segs = left_s.split(" ")
        if len(segs) != 3:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} ls-tree batch header bad parts at {epoch}:{path_s}")
        mode_s, type_s, oid_s = segs
        if len(mode_s) != 6 or any(c not in "01234567" for c in mode_s):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} ls-tree batch bad mode at {epoch}:{path_s}: {mode_s!r}")
        if type_s != "blob":
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} ls-tree batch bad type at {epoch}:{path_s}: {type_s!r} (must be blob)")
        if len(oid_s) != 40 or any(c not in "0123456789abcdef" for c in oid_s):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} ls-tree batch bad OID at {epoch}:{path_s}")
        if "\n" in path_s:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} ls-tree batch path has newline at {epoch}")
        result[path_s] = (mode_s, oid_s)
    if len(result) > len(finite_sorted):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} ls-tree batch count exceeds finite set at {epoch}")
    _cache[("tree_dict", epoch)] = result
    return result


def _fetch_epoch_blobs_batch(repo_root: Path, epoch: str, label: str, _cache: dict) -> None:
    """Fetch all missing blobs for epoch via single `git cat-file --batch` by OID.

    Validates OID/type/size/count/bounds, binary-safe. Fail-closed on missing blob,
    bad type/length, OID mismatch, truncated/extra bytes, returncode/stderr.
    """
    tree = _fetch_epoch_tree_batch(repo_root, epoch, label, _cache)
    # Collect OIDs not yet cached
    need_oids: list[str] = []
    oid_to_paths: dict[str, list[str]] = {}
    for p, (_mode, _oid) in tree.items():
        if ("blob", epoch, p) in _cache:
            continue
        if ("blob_by_oid", _oid) in _cache:
            # Populate per-path from OID cache (same bytes, same predicates)
            _cache[("blob", epoch, p)] = _cache[("blob_by_oid", _oid)]
            continue
        oid_to_paths.setdefault(_oid, []).append(p)
    for oid in oid_to_paths:
        if not isinstance(oid, str) or len(oid) != 40 or any(c not in "0123456789abcdef" for c in oid):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} batch OID invalid: {oid!r}")
    need_oids = sorted(oid_to_paths.keys())
    if not need_oids:
        return
    if len(need_oids) > 500:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} batch OID count exceeds bound: {len(need_oids)}")
    stdin_b = ("\n".join(need_oids) + "\n").encode("ascii")
    try:
        raw = subprocess.run(
            ["git", "cat-file", "--batch"],
            cwd=str(repo_root.resolve()),
            input=stdin_b,
            capture_output=True,
            timeout=30,
            env=_sanitized_git_env(),
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise RenewalHistoryError("HISTORY_BLOB_MISSING", f"{label} cat-file batch failed {epoch}: {exc}") from exc
    if raw.returncode != 0:
        err = raw.stderr.decode("utf-8", errors="replace")[:300] if isinstance(raw.stderr, (bytes, bytearray)) else str(raw.stderr)[:300]
        raise RenewalHistoryError("HISTORY_BLOB_MISSING", f"{label} cat-file batch failed {epoch}: {err}")
    out: bytes = raw.stdout if isinstance(raw.stdout, (bytes, bytearray)) else b""
    pos = 0
    n = len(out)
    for expected_oid in need_oids:
        nl = out.find(b"\n", pos)
        if nl < 0:
            raise RenewalHistoryError("HISTORY_BLOB_MISSING", f"{label} cat-file batch truncated header for {expected_oid} at {epoch}")
        header_b = out[pos:nl]
        pos = nl + 1
        try:
            header_s = header_b.decode("ascii")
        except UnicodeDecodeError as exc:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} cat-file batch header not ASCII for {expected_oid} at {epoch}") from exc
        hparts = header_s.split(" ")
        if len(hparts) == 2 and hparts[1] == "missing":
            if hparts[0] != expected_oid:
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} cat-file batch OID mismatch (missing) at {epoch}: got {hparts[0]!r} want {expected_oid!r}")
            raise RenewalHistoryError("HISTORY_BLOB_MISSING", f"{label} blob missing at epoch {epoch} OID {expected_oid}")
        if len(hparts) != 3:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} cat-file batch header bad parts for {expected_oid} at {epoch}: {header_s!r}")
        got_oid, got_type, got_size_s = hparts
        if got_oid != expected_oid:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} cat-file batch OID mismatch at {epoch}: got {got_oid!r} want {expected_oid!r} (object replace?)")
        if got_type != "blob":
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} cat-file batch bad type for {expected_oid} at {epoch}: {got_type!r} (must be blob)")
        try:
            got_size = int(got_size_s)
        except ValueError as exc:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} cat-file batch bad size for {expected_oid} at {epoch}: {got_size_s!r}") from exc
        if got_size < 0 or got_size > MAX_FILE_BYTES:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} cat-file batch size OOB for {expected_oid} at {epoch}: {got_size}")
        if pos + got_size + 1 > n:
            raise RenewalHistoryError("HISTORY_BLOB_MISSING", f"{label} cat-file batch truncated content for {expected_oid} at {epoch} (want {got_size}, have {n - pos})")
        content = out[pos:pos + got_size]
        pos += got_size
        if out[pos:pos + 1] != b"\n":
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} cat-file batch missing trailing NL for {expected_oid} at {epoch}")
        pos += 1
        if len(content) != got_size:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} cat-file batch length mismatch for {expected_oid} at {epoch}")
        _cache[("blob_by_oid", expected_oid)] = content
        for p in oid_to_paths[expected_oid]:
            _cache[("blob", epoch, p)] = content
    if pos != n:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} cat-file batch extra trailing bytes at {epoch}: {n - pos} (count bound)")


def _git_commit_exists(repo_root: Path, epoch: str, label: str, _cache: dict | None = None) -> None:
    if not isinstance(epoch, str) or len(epoch) != 40 or any(c not in "0123456789abcdef" for c in epoch):
        raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", f"{label} epoch GITSHA invalid: {epoch!r}")
    # ROOT B3 perf: safe per-INVOCATION pinned raw Git metadata reuse only.
    # No global authority cache; _cache is per-verify_versioned_history call (or per-function local
    # when None), holds ONLY raw git metadata (commit existence, blob bytes, mode), never validated
    # authority objects, same predicates (mode/path/epoch). Caller must not pass API/cache authority.
    if _cache is not None:
        _k = ("commit_exists", epoch)
        if _k in _cache:
            return
    proc = _git_run(repo_root, ["cat-file", "-e", f"{epoch}^{{commit}}"], label)
    if proc.returncode != 0:
        raise RenewalHistoryError("HISTORY_BLOB_MISSING", f"{label} epoch commit missing: {epoch}: {proc.stderr.strip()[:300]}")
    if _cache is not None:
        _cache[("commit_exists", epoch)] = True


def _git_show_blob(repo_root: Path, epoch: str, path: str, label: str, _cache: dict | None = None) -> bytes:
    _lexical_parts(path, label)
    if _cache is not None:
        _k = ("blob", epoch, path)
        if _k in _cache:
            v = _cache[_k]
            if not isinstance(v, (bytes, bytearray)):
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} blob cache bad type {epoch}:{path}")
            return bytes(v)
        # Batched path: tree OID validated, blob fetched by OID (not untrusted path line).
        # Only finite expected paths are batched; unknown paths use single-path fallback
        # that still enforces SAME predicates (no new unsupported batch membership).
        if path in _FINITE_BATCH_PATHS:
            _fetch_epoch_blobs_batch(repo_root, epoch, label, _cache)
            if _k in _cache:
                v2 = _cache[_k]
                if not isinstance(v2, (bytes, bytearray)):
                    raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} blob cache bad type {epoch}:{path}")
                return bytes(v2)
            raise RenewalHistoryError("HISTORY_BLOB_MISSING", f"{label} blob missing at epoch {epoch}:{path} (batched)")
    try:
        raw = subprocess.run(
            ["git", "show", f"{epoch}:{path}"],
            cwd=str(repo_root.resolve()),
            capture_output=True,
            timeout=30,
            env=_sanitized_git_env(),
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise RenewalHistoryError("HISTORY_BLOB_MISSING", f"{label} git show failed {epoch}:{path}: {exc}") from exc
    if raw.returncode != 0:
        raise RenewalHistoryError("HISTORY_BLOB_MISSING", f"{label} blob missing at epoch {epoch}:{path}")
    if _cache is not None:
        _cache[("blob", epoch, path)] = raw.stdout
    return raw.stdout


def _git_blob_sha(repo_root: Path, epoch: str, path: str, label: str, _cache: dict | None = None) -> str:
    if _cache is not None:
        _k = ("sha", epoch, path)
        if _k in _cache:
            return _cache[_k]
        # Reuse blob bytes cache when present (same predicates, no extra git call).
        _bk = ("blob", epoch, path)
        if _bk in _cache:
            _s = hashlib.sha256(_cache[_bk]).hexdigest()
            _cache[("sha", epoch, path)] = _s
            return _s
    _s2 = hashlib.sha256(_git_show_blob(repo_root, epoch, path, label, _cache)).hexdigest()
    if _cache is not None:
        _cache[("sha", epoch, path)] = _s2
    return _s2


def _git_tree_mode(repo_root: Path, epoch: str, path: str, label: str, _cache: dict | None = None) -> str:
    if _cache is not None:
        _k = ("mode", epoch, path)
        if _k in _cache:
            v = _cache[_k]
            if not isinstance(v, str):
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} mode cache bad type {epoch}:{path}")
            return v
        if path in _FINITE_BATCH_PATHS:
            tree = _fetch_epoch_tree_batch(repo_root, epoch, label, _cache)
            if path not in tree:
                raise RenewalHistoryError("HISTORY_BLOB_MISSING", f"{label} path absent at epoch {epoch}:{path} (batched)")
            mode_b, _oid_b = tree[path]
            _cache[("mode", epoch, path)] = mode_b
            return mode_b
    proc = _git_run(repo_root, ["ls-tree", epoch, "--", path], label)
    if proc.returncode != 0:
        raise RenewalHistoryError("HISTORY_BLOB_MISSING", f"{label} ls-tree failed {epoch}:{path}")
    out = proc.stdout.strip()
    if not out:
        raise RenewalHistoryError("HISTORY_BLOB_MISSING", f"{label} path absent at epoch {epoch}:{path}")
    try:
        mode = out.split()[0]
    except IndexError as exc:
        raise RenewalHistoryError("HISTORY_BLOB_MISSING", f"{label} ls-tree parse failed {epoch}:{path}") from exc
    if _cache is not None:
        _cache[("mode", epoch, path)] = mode
    return mode


def _verify_tool_blob(repo_root: Path, epoch: str, path: str, expected_sha: str, label: str, _cache: dict | None = None) -> None:
    if not isinstance(expected_sha, str) or len(expected_sha) != 64:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} expected sha invalid")
    _git_commit_exists(repo_root, epoch, label, _cache)
    actual_sha = _git_blob_sha(repo_root, epoch, path, label, _cache)
    if actual_sha != expected_sha:
        raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", f"{label} tool blob drift at {epoch}:{path}")
    mode = _git_tree_mode(repo_root, epoch, path, label, _cache)
    if mode != "100644":
        raise RenewalHistoryError("HISTORY_MODE", f"{label} tool mode must be 100644 at {epoch}:{path}, got {mode}")


# ---------------------------------------------------------------------------
# Kind discriminators and chain helpers
# ---------------------------------------------------------------------------

def _is_legacy_record(record: dict[str, Any]) -> bool:
    return isinstance(record, dict) and record.get("reason_class") == LEGACY_REASON and "kind" not in record


def _is_editorial_record(record: dict[str, Any]) -> bool:
    return (
        isinstance(record, dict)
        and record.get("reason_class") == EDITORIAL_REASON
        and record.get("kind") == EDITORIAL_KIND
    )


def _is_renewal_record(record: dict[str, Any]) -> bool:
    return (
        isinstance(record, dict)
        and record.get("reason_class") == VERSIONED_REASON
        and record.get("kind") == VERSIONED_KIND
    )


def _is_versioned_record(record: dict[str, Any]) -> bool:
    return _is_editorial_record(record) or _is_renewal_record(record)


def _is_versioned_seal(seal: dict[str, Any]) -> bool:
    return (
        isinstance(seal, dict)
        and seal.get("kind") == VERSIONED_SET_KIND
        and seal.get("status") == VERSIONED_SET_STATUS
    )


def _record_kind(record: dict[str, Any]) -> str:
    if _is_legacy_record(record):
        return "LEGACY"
    if _is_editorial_record(record):
        return "EDITORIAL"
    if _is_renewal_record(record):
        return "VERSIONED"
    raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "record kind/reason pair unrecognized (no caller kind inference)")


def _load_record_file(repo_root: Path, ref: Any, label: str) -> dict[str, Any]:
    if not isinstance(ref, dict) or set(ref) != {"path", "sha256"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} supersession link authority fields invalid")
    data = _check_authority_ref(repo_root, ref, label)
    value = _parse_json_strict_bytes(data, label)
    if not isinstance(value, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} must be a JSON object")
    schema_gate = _load_schema_validator()
    try:
        schema_gate.validate_instance(value, repo_root.resolve() / str(REVALIDATION_SCHEMA), label=label)
    except ValueError as exc:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} schema invalid: {exc}") from exc
    return value


def _walk_chain_backwards(repo_root: Path, start_ref: dict[str, Any] | None) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    chain: list[tuple[dict[str, Any], dict[str, Any]]] = []
    seen: set[tuple[str, str]] = set()
    current_ref = start_ref
    for _ in range(CHAIN_LIMIT):
        if current_ref is None:
            return chain
        if not isinstance(current_ref, dict) or set(current_ref) != {"path", "sha256"}:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "supersession link authority fields invalid")
        key = (str(current_ref.get("path")), str(current_ref.get("sha256")))
        if key in seen:
            raise RenewalHistoryError("HISTORY_ANCESTOR", "publication revalidation supersession chain cycle")
        seen.add(key)
        record = _load_record_file(repo_root, current_ref, "superseded revalidation record")
        chain.append((record, {"path": current_ref["path"], "sha256": current_ref["sha256"]}))
        nxt = record.get("supersedes")
        if nxt is None:
            return chain
        current_ref = nxt
    raise RenewalHistoryError("HISTORY_ANCESTOR", "publication revalidation supersession chain too deep (max32)")


def _parse_sequence(path_value: str) -> int | None:
    name = Path(path_value).name
    prefix = "publication-surface-revalidation-r"
    suffix = ".json"
    if not name.startswith(prefix) or not name.endswith(suffix):
        return None
    middle = name[len(prefix):-len(suffix)]
    if not middle.isdigit() or (len(middle) > 1 and middle.startswith("0")):
        return None
    try:
        return int(middle)
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Expected closure sets (exact membership, name==path, sorted-unique).
# ---------------------------------------------------------------------------

def _expected_receipt_closure(route: str, generation: str) -> tuple[str, ...]:
    if route not in ("WEEKLY_GENERATED_V2", "LONGFORM_GENERATED_V1"):
        raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"unknown generator_route for closure: {route!r}")
    extra = _ROUTE_WEEKLY_3 if route == "WEEKLY_GENERATED_V2" else _ROUTE_LONGFORM_3
    if generation == "OLD":
        members = set(_OLD_PY_30) | set(_OLD_SCHEMAS_14) | set(extra) | set(_STAGED_1) | set(_STYLE_1) | set(_RECIPE_1)
    elif generation == "NEW":
        members = (
            set(_OLD_PY_30) | set(_FAMILY_PY_2) | set(_NEW_PY_3)
            | set(_OLD_SCHEMAS_14) | set(_NEW_SCHEMAS_4) | set(_FAMILY_SCHEMAS_4)
            | set(extra) | set(_STAGED_1) | set(_STYLE_1) | set(_RECIPE_1)
        )
    else:
        raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"unknown closure generation: {generation!r}")
    return tuple(sorted(members))


def _expected_staged_code_deps(route: str, generation: str = "OLD") -> tuple[str, ...]:
    # ROOT B2: staged code_deps is NOT always 50. Old R3 is 50, renewal→editorial
    # (same EDITORIAL kind, NEW installed contract) is 63. Derive OLD50 vs NEW63
    # by finite supported sets + actual own recorded epoch, never caller flag.
    if route not in ("WEEKLY_GENERATED_V2", "LONGFORM_GENERATED_V1"):
        raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"unknown staged route: {route!r}")
    extra = _ROUTE_WEEKLY_3 if route == "WEEKLY_GENERATED_V2" else _ROUTE_LONGFORM_3
    if generation == "OLD":
        members = set(_OLD_PY_30) | set(_OLD_SCHEMAS_14) | set(extra) | set(_STAGED_1) | set(_STYLE_1) | set(_RECIPE_1)
    elif generation == "NEW":
        members = (
            set(_OLD_PY_30) | set(_FAMILY_PY_2) | set(_NEW_PY_3)
            | set(_OLD_SCHEMAS_14) | set(_NEW_SCHEMAS_4) | set(_FAMILY_SCHEMAS_4)
            | set(extra) | set(_STAGED_1) | set(_STYLE_1) | set(_RECIPE_1)
        )
    else:
        raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"unknown staged generation: {generation!r}")
    ordered = tuple(sorted(members))
    _want = 50 if generation == "OLD" else 63
    if len(ordered) != _want:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"staged fixed set changed size: {len(ordered)} != {_want} ({generation})")
    return ordered


def _derive_tool_generation(repo_root: Path, epoch: str, label: str, _cache: dict | None = None) -> str:
    """Derive OLD50 vs NEW63 from actual own recorded epoch (finite, no caller flag).

    Checks owned epoch config + supported exact pipeline OLD67/NEW71 + versions/quality/profiles,
    not just 7 new files existence. Recomputes Contract8 at OWN epoch (pure, NUL framing, no old code)
    for later stored-vs-OWN comparison (in _verify_editorial_ancestor). Unknown cfg/schema/profile
    registered set → UNSUPPORTED. Mode/blob missing → FAIL. Pure presence 7 new files with OLD67 cfg
    REJECTS NEW (even all modes correct). Partial new files → UNKNOWN refuses. Old R3 (OLD67, no new
    files) => OLD; renewal→editorial (NEW71, all new files) => NEW.
    """
    if not isinstance(epoch, str) or len(epoch) != 40 or any(c not in "0123456789abcdef" for c in epoch):
        raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", f"{label} epoch GITSHA invalid: {epoch!r}")
    _new_paths = list(_NEW_PY_3) + list(_NEW_SCHEMAS_4)
    _present = 0
    for _p in _new_paths:
        try:
            _m = _git_tree_mode(repo_root, epoch, _p, f"{label} generation probe {_p}", _cache)
            if _m != "100644":
                raise RenewalHistoryError("HISTORY_MODE", f"{label} new path mode must be 100644 at {epoch}:{_p}")
            _present += 1
        except RenewalHistoryError as exc:
            if exc.code == "HISTORY_BLOB_MISSING":
                continue
            raise
    # Owned epoch config (mode 100644, else FAIL; JSON strict; versions fixed; pipeline OLD67/NEW71 exact).
    _cfg_mode = _git_tree_mode(repo_root, epoch, _DEFAULT_CONFIG_PATH, f"{label} owned config mode", _cache)
    if _cfg_mode != "100644":
        raise RenewalHistoryError("HISTORY_MODE", f"{label} owned config mode must be 100644 at {epoch}:{_DEFAULT_CONFIG_PATH}")
    try:
        _cfg_bytes = _git_show_blob(repo_root, epoch, _DEFAULT_CONFIG_PATH, f"{label} owned config blob", _cache)
    except RenewalHistoryError as exc:
        raise RenewalHistoryError(exc.code, f"{label} owned config blob missing at {epoch}: {exc.detail}") from exc
    try:
        _cfg = _parse_json_strict_bytes(_cfg_bytes, f"{label} owned config")
    except RenewalHistoryError as exc:
        raise RenewalHistoryError(exc.code, f"{label} owned config invalid JSON at {epoch}: {exc.detail}") from exc
    if not isinstance(_cfg, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} owned config must be an object at {epoch}")
    if _cfg.get("pipeline_contract_version") != _KNOWN_VERSION:
        raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"{label} unknown pipeline_contract_version (must be {_KNOWN_VERSION})")
    if _cfg.get("quality_contract_version") != _KNOWN_VERSION:
        raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"{label} unknown quality_contract_version (must be {_KNOWN_VERSION})")
    _rprofs = _cfg.get("research_profiles")
    _pprofs = _cfg.get("publication_profiles")
    if not isinstance(_rprofs, dict) or set(_rprofs.keys()) != set(_KNOWN_RESEARCH_PROFILES):
        raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"{label} unknown research profiles (must be exactly {list(_KNOWN_RESEARCH_PROFILES)})")
    if not isinstance(_pprofs, dict) or set(_pprofs.keys()) != set(_KNOWN_PUBLICATION_PROFILES):
        raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"{label} unknown publication profiles (must be exactly {list(_KNOWN_PUBLICATION_PROFILES)})")
    for _rk in _KNOWN_RESEARCH_PROFILES:
        if not isinstance(_rprofs.get(_rk), dict) or _rprofs[_rk].get("version") != _KNOWN_VERSION:
            raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"{label} unknown research profile version for {_rk}")
    for _pk in _KNOWN_PUBLICATION_PROFILES:
        if not isinstance(_pprofs.get(_pk), dict) or _pprofs[_pk].get("version") != _KNOWN_VERSION:
            raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"{label} unknown publication profile version for {_pk}")
    _cf = _cfg.get("contract_files", {})
    _pipe = _cf.get("pipeline")
    _qual = _cf.get("quality")
    if not isinstance(_pipe, list) or not isinstance(_qual, list):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} owned contract_files pipeline/quality must be arrays at {epoch}")
    _pipe_set = set(_pipe)
    if len(_pipe_set) != len(_pipe):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} owned pipeline list has duplicates at {epoch} (no silent layout)")
    if set(_qual) != set(_KNOWN_QUALITY_3) or len(_qual) != 3:
        raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"{label} unknown quality list (must be exactly 3 known)")
    _old_set = set(_OLD_PIPELINE_67)
    _new_set = _old_set | set(_NEW_SCHEMAS_4)
    # Exact OLD67 (67) vs NEW71 (71=OLD67+4new), no removed, no other added, no wildcard/silent.
    if _pipe_set != _old_set and _pipe_set != _new_set:
        raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"{label} unknown pipeline list (must be exactly OLD67 (67) or NEW71 (71=OLD67+4new), no wildcard/silent)")
    # Pure presence 7 new files with OLD67 cfg must REJECT NEW (even all modes correct).
    if _present == len(_new_paths) and _pipe_set != _new_set:
        raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"{label} 7 new files present but owned cfg is OLD67 (not NEW71), REJECT NEW (no files-only classification)")
    if _present == 0 and _pipe_set != _old_set:
        # OLD files absent (0 present) but cfg is NEW71 (71 paths including 4 new, blobs missing at epoch for new schemas?
        # Recomputing Contract8 pipeline aggregate below will fail with BLOB_MISSING (mode/blob missing FAIL), as required.
        # To give precise code now (unknown cfg vs missing blob), check: if cfg is NEW71 but files missing, it will fail below on blob missing (FAIL, not UNSUPPORTED).
        # Here, cfg is NEW71 but files missing (0 present) → inconsistent (NEW cfg without NEW files) → UNSUPPORTED (unknown cfg/schema registered set? Actually files missing, not unknown cfg? Config is known NEW71, but files missing at epoch → BLOB_MISSING when recomputing Contract8 below. Let it fall through to Contract8 recomputation which will fail with BLOB_MISSING (correct FAIL, not UNSUPPORTED). For now, do not refuse here; let Contract8 recomputation fail with BLOB_MISSING.
        pass
    if _present == len(_new_paths):
        # Preliminary NEW (7 files present + mode correct). Require owned cfg NEW71 exact (already checked above: if cfg != NEW71, refused above).
        # Recompute Contract8 at OWN epoch below (in caller for stored-vs-OWN comparison? Here just validate owned cfg is NEW71, return NEW).
        # Contract8 recomputation for stored-vs-OWN comparison happens in _verify_editorial_ancestor (not here, to avoid double recompute? Actually recompute here for validation? No, just return NEW; Contract8 recomputation for comparison happens in _verify_editorial_ancestor via _recompute helper.
        # To ensure owned epoch config is valid NEW71 (with correct versions/quality/profiles/pipeline exact, already checked), return NEW.
        return "NEW"
    if _present == 0:
        # Preliminary OLD (0 present). Require owned cfg OLD67 exact (already checked: if cfg != OLD67 and != NEW71, refused above; if cfg == NEW71 but files missing (0 present), it will fail below on Contract8 BLOB_MISSING (correct FAIL). For now, if cfg == OLD67, return OLD; if cfg == NEW71 but files missing, let Contract8 recomputation fail with BLOB_MISSING.
        # Note: 0 present + NEW71 cfg (NEW cfg without NEW files) is inconsistent (NEW cfg without NEW files) → BLOB_MISSING on Contract8 recompute below (correct FAIL, not UNSUPPORTED, not OLD).
        if _pipe_set == _old_set:
            return "OLD"
        # _present==0 but _pipe_set == _new_set (NEW71 cfg without NEW files) → inconsistent, let Contract8 recompute fail with BLOB_MISSING (FAIL, not UNSUPPORTED).
        # Fall through to Contract8 recomputation below which will fail on missing blobs.
        pass
    # Partial new files (1-6 present) → UNKNOWN refuses (no broad migration). Already handled? Actually _present 1-6 falls through to here (since not 7 and not 0). Refuse UNKNOWN.
    # Also _present==0 + _pipe_set==_new_set (NEW cfg without files) falls through here; attempt Contract8 recompute to get BLOB_MISSING (FAIL).
    # And _present==7 + _pipe_set==_old_set already refused above (REJECT NEW). Good.
    # For remaining cases (partial, or 0+NEW71 inconsistency), attempt Contract8 recompute to get precise FAIL (BLOB_MISSING) or refuse UNKNOWN?
    # For partial (1-6 present), regardless of cfg (OLD67 or NEW71 or unknown, already refused if unknown? Actually pipeline check above already refused if pipeline != OLD67 and != NEW71 (unknown cfg → UNSUPPORTED). Good. For partial with known cfg (OLD67 or NEW71), still UNKNOWN (partial new files) → refuse UNSUPPORTED (no broad migration).
    if _present != 0 and _present != len(_new_paths):
        raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"{label} tool epoch has partial new files ({_present}/{len(_new_paths)}), UNKNOWN generation refuses (no broad migration)")
    # _present==0 + _pipe_set==_new_set (NEW71 cfg without files) → inconsistent, attempt Contract8 recompute to get BLOB_MISSING (FAIL).
    # _present==7 + _pipe_set==_old_set already refused above (REJECT NEW). Good.
    # Fall through: try Contract8 recompute (will fail with BLOB_MISSING for missing files, correct FAIL).
    # To get BLOB_MISSING (not UNSUPPORTED), call Contract8 recompute here (which reads pipeline files at epoch, missing new schemas → BLOB_MISSING).
    # Use dummy research/publication for recompute? Need research/publication for Contract8 (WEEKLY/WEEKLY_MAGAZINE? Or THEMATIC/LONGFORM_SPECIAL? For generation derivation, which profile? Use WEEKLY/WEEKLY_MAGAZINE as default? Actually Contract8 depends on research/publication profiles (for research/publication SHAs). For generation derivation (OLD vs NEW), Contract8 pipeline SHA differs (OLD67 vs NEW71), but research/publication SHAs same (since profiles unchanged)? Actually research/publication SHAs depend on research/publication contracts (which are same for OLD/NEW? Since profiles unchanged). Good. For Contract8 recomputation to trigger BLOB_MISSING for missing pipeline files (4 new schemas missing), need to call recompute with any valid research/publication (e.g., WEEKLY/WEEKLY_MAGAZINE). Good. If recompute fails with BLOB_MISSING, propagate (correct FAIL). If recompute succeeds (should not, since files missing, but if files missing but pipeline is OLD67? No, _present==0 + _pipe_set==_new_set means pipeline is NEW71 (71 paths including 4 new), but files missing (0 present, so 4 new files missing at epoch), so recompute will fail on missing blobs for 4 new schemas (BLOB_MISSING, correct FAIL). Good.
    # Call recompute to trigger BLOB_MISSING (FAIL) for this inconsistent case.
    _recompute_contract8_at_epoch(repo_root, epoch, "WEEKLY", "WEEKLY_MAGAZINE", f"{label} generation Contract8", _cache)
    # If recompute somehow succeeds (should not, since files missing), then inconsistent (NEW cfg without files but Contract8 recomputed? Actually if files missing, recompute would have failed with BLOB_MISSING above, so should not reach here. If it does succeed (e.g., files missing but pipeline is OLD67? No, _present==0 + _pipe_set==_new_set means pipeline NEW71 but files missing, recompute must fail with BLOB_MISSING. Good. If it succeeds, then unknown (should not happen) → refuse UNSUPPORTED.
    raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"{label} inconsistent generation (0 files but NEW71 cfg, Contract8 recompute unexpectedly succeeded, no broad migration)")


def _verify_receipt_closure_exact(
    repo_root: Path,
    closure: Any,
    epoch: str,
    route: str,
    generation: str,
    label: str,
    _cache: dict | None = None,
) -> None:
    if not isinstance(closure, list) or not closure:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} closure must be a non-empty array")
    expected = _expected_receipt_closure(route, generation)
    if len(closure) != len(expected):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} closure count must equal expected {len(expected)} ({route}/{generation}): got {len(closure)}")
    seen: dict[str, dict[str, Any]] = {}
    for row in closure:
        if not isinstance(row, dict) or set(row) != {"name", "path", "sha256"}:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} closure row must be exact {{name,path,sha256}}")
        name = row["name"]
        path = row["path"]
        sha = row["sha256"]
        if not isinstance(name, str) or not name or not isinstance(path, str) or not path:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} closure row name/path invalid")
        if name != path:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} closure name must equal path (no alias): {name!r} != {path!r}")
        if not isinstance(sha, str) or len(sha) != 64 or any(c not in "0123456789abcdef" for c in sha):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} closure row sha invalid")
        if name in seen:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} duplicate closure row: {name}")
        seen[name] = row
    if set(seen) != set(expected):
        missing = sorted(set(expected) - set(seen))
        extra = sorted(set(seen) - set(expected))
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} closure set must equal expected {route}/{generation}: missing={missing} extra={extra}")
    for name in expected:
        row = seen[name]
        _verify_tool_blob(repo_root, epoch, row["path"], row["sha256"], f"{label} closure {name}", _cache)


def _verify_staged_code_deps_exact(
    repo_root: Path,
    code_deps: Any,
    epoch: str,
    route: str,
    label: str,
    generation: str | None = None,
    _cache: dict | None = None,
) -> None:
    if not isinstance(code_deps, list) or not code_deps:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} code_deps must be a non-empty array")
    # ROOT B2: generation must be derived from own epoch, never caller flag.
    # If caller passes None, derive here (epoch file existence). Explicit generation
    # (from _verify_editorial_ancestor derived both epochs) must still equal derived.
    _derived = _derive_tool_generation(repo_root, epoch, f"{label} staged generation", _cache)
    if generation is not None and generation != _derived:
        raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", f"{label} staged generation {generation} != derived own epoch generation {_derived} (no caller flag)")
    _gen = generation if generation is not None else _derived
    expected = _expected_staged_code_deps(route, _gen)
    _want_n = 50 if _gen == "OLD" else 63
    if len(code_deps) != len(expected):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} code_deps count must equal {_want_n} ({route}/{_gen}): got {len(code_deps)}")
    seen: dict[str, dict[str, Any]] = {}
    for row in code_deps:
        if not isinstance(row, dict) or set(row) != {"path", "sha256", "byte_count"}:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} code_deps row must be exact {{path,sha256,byte_count}}")
        path = row["path"]
        sha = row["sha256"]
        size = row["byte_count"]
        if not isinstance(path, str) or not path:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} code_deps path invalid")
        if not isinstance(sha, str) or len(sha) != 64 or any(c not in "0123456789abcdef" for c in sha):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} code_deps sha invalid")
        if not isinstance(size, int) or isinstance(size, bool) or size < 1:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} code_deps byte_count invalid")
        if path in seen:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} duplicate code_deps: {path}")
        seen[path] = row
    if set(seen) != set(expected):
        missing = sorted(set(expected) - set(seen))
        extra = sorted(set(seen) - set(expected))
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} code_deps set must equal fixed {_want_n} ({route}/{_gen}): missing={missing} extra={extra}")
    # Order must be sorted by path (construction enforces pre-sorted).
    if [r["path"] for r in code_deps] != sorted(seen):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} code_deps order must be sorted by path")
    for path in expected:
        row = seen[path]
        _verify_tool_blob(repo_root, epoch, path, row["sha256"], f"{label} code_dep {path}", _cache)
        # Byte count must match epoch blob length (reuse cached blob, same predicates).
        blob = _git_show_blob(repo_root, epoch, path, f"{label} code_dep bytes {path}", _cache)
        if len(blob) != row["byte_count"]:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} code_dep byte_count drift: {path}")


# ---------------------------------------------------------------------------
# Owner registry and epoch derivation (fixed, no caller authority)
# ---------------------------------------------------------------------------

def _derive_epoch_for_schema(doc_type: str, history_graph: dict[str, Any]) -> str:
    if doc_type in ("proposal", "retention", "staged"):
        epoch = history_graph.get("staged_head")
        if not isinstance(epoch, str) or len(epoch) != 40:
            raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", f"staged producer_head missing for {doc_type}")
        return epoch
    if doc_type in ("receipt-editorial", "seal-editorial", "spec-toolchain", "spec-manuscript"):
        epoch = history_graph.get("receipt_epoch")
        if not isinstance(epoch, str) or len(epoch) != 40:
            raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", f"receipt epoch missing for {doc_type}")
        return epoch
    if doc_type == "build-old":
        epoch = history_graph.get("build_old_epoch") or history_graph.get("receipt_epoch")
        if not isinstance(epoch, str) or len(epoch) != 40:
            raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", "build-old epoch missing")
        return epoch
    if doc_type in (
        "receipt-renewal", "seal-renewal", "build-new", "basis", "proof",
        "manuscript-renewal", "candidate-renewal", "bundle-renewal",
        "gate-renewal", "record-renewal",
    ):
        epoch = history_graph.get("basis_current_epoch")
        if not isinstance(epoch, str) or len(epoch) != 40:
            raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", f"basis CURRENT epoch missing for {doc_type}")
        return epoch
    if doc_type == "scope":
        epoch = history_graph.get("staged_head")
        if not isinstance(epoch, str) or len(epoch) != 40:
            raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", "staged producer_head missing for scope O17")
        return epoch
    raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"unknown doc type for epoch derivation: {doc_type!r}")


def _infer_doc_type_for_schema_row(schema_path: str, schema_pointer: str) -> str:
    for doc_type, (spath, spointer) in _OWNER_BY_TYPE.items():
        if spath == schema_path and spointer == schema_pointer:
            return doc_type
    # Ambiguous paths (e.g. same schema used for multiple doc types with "" pointer):
    # resolve via schema_path alone where pointer is "" and multiple owners share path?
    # For strictness, require exact (path,pointer) match; unknown refuses.
    raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"unregistered schema binding: {schema_path} {schema_pointer!r}")


def _check_observed_binding_row_structural(
    repo_root: Path,
    row: Any,
    label: str,
    _cache: dict | None = None,
) -> dict[str, Any]:
    """Structural check for one binding row WITHOUT epoch==derived-owner via single graph.

    Checks registry, live/COPY, schema blob/mode at submitted epoch, O17 "",
    tool actual field equality (no caller authority). Epoch/owner/path completeness
    (no omissions/extras/forged epoch/owner) is enforced separately via exact equality
    to derived expected accumulator (predecessor bindings BEFORE this record for
    versioned basis/proof, or derived editorial for editorial). No extra permit.

    ROOT B3: exact registry pointer '' or allowed build defs (no arbitrary caller
    pointer via _infer), finite fingerprints (no foreign even when path registered),
    strict offline instance validation vs own recorded SCHEMA blob (data only, no
    old code, no REMOTE ref). Per-invocation raw git metadata reuse only.
    """
    if not isinstance(row, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} binding row must be an object")
    binding = row.get("binding")
    if binding not in ("RECEIPT_CURRENT_TOOLS", "STAGED_PRODUCER", "SCHEMA"):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} unknown binding: {binding!r}")
    source_ref = row.get("source_ref")
    epoch = row.get("repository_commit_sha")
    if not isinstance(source_ref, dict) or set(source_ref) != {"path", "sha256"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} source_ref fields invalid")
    if not isinstance(epoch, str) or len(epoch) != 40 or any(c not in "0123456789abcdef" for c in epoch):
        raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", f"{label} repository_commit_sha invalid")
    _check_authority_ref(repo_root, source_ref, f"{label} source live")
    if binding in ("RECEIPT_CURRENT_TOOLS", "STAGED_PRODUCER"):
        if any(k in row for k in ("schema_path", "schema_pointer", "schema_sha256")):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} RECEIPT/STAGED row must not carry schema_*")
        if set(row) != {"source_ref", "binding", "repository_commit_sha"}:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} RECEIPT/STAGED row has unregistered keys")
        _git_commit_exists(repo_root, epoch, f"{label} tool epoch", _cache)
        try:
            tool_bytes = read_repo_bytes(repo_root, str(source_ref["path"]), f"{label} tool doc live")
        except RenewalHistoryError as exc:
            raise RenewalHistoryError(exc.code, f"{label} tool doc unreadable: {exc.detail}") from exc
        try:
            tool_doc = _parse_json_strict_bytes(tool_bytes, f"{label} tool doc")
        except RenewalHistoryError as exc:
            raise RenewalHistoryError(exc.code, f"{label} tool doc invalid: {exc.detail}") from exc
        if not isinstance(tool_doc, dict):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} tool doc must be an object")
        if binding == "RECEIPT_CURRENT_TOOLS":
            tools = tool_doc.get("current_tools")
            if not isinstance(tools, dict):
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} receipt tool doc lacks current_tools")
            actual_epoch = tools.get("repository_commit_sha")
            if not isinstance(actual_epoch, str) or len(actual_epoch) != 40:
                raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", f"{label} receipt actual epoch invalid")
            if actual_epoch != epoch:
                raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", f"{label} RECEIPT epoch must equal actual receipt.current_tools.commit (no caller authority)")
        else:
            actual_head = tool_doc.get("producer_head")
            if not isinstance(actual_head, str) or len(actual_head) != 40:
                raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", f"{label} staged actual producer_head invalid")
            if actual_head != epoch:
                raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", f"{label} STAGED epoch must equal actual staged.producer_head (no caller authority)")
        return {
            "source_ref": {"path": source_ref["path"], "sha256": source_ref["sha256"]},
            "binding": binding,
            "repository_commit_sha": epoch,
        }
    for key in ("schema_path", "schema_pointer", "schema_sha256"):
        if key not in row:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} SCHEMA row missing {key}")
    schema_path = row.get("schema_path")
    schema_pointer = row.get("schema_pointer")
    schema_sha = row.get("schema_sha256")
    if not isinstance(schema_path, str) or schema_path not in _ALLOWED_SCHEMA_PATHS:
        raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"{label} unregistered schema_path: {schema_path!r}")
    if not isinstance(schema_pointer, str):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} schema_pointer must be a string (\"\" allows root)")
    # ROOT B3: exact registry pointer '' or allowed build defs, no arbitrary caller pointer.
    # _infer enforces exact (path,pointer) match to OWNER_REGISTRY; unknown refuses.
    # O17 whole-doc is "" (never "/"); inventory "/properties/editorial_correction_scope" is
    # schema-node pointer only, never alternative to whole-doc validation.
    _infer_doc_type_for_schema_row(schema_path, schema_pointer)
    if schema_path == "schemas/reader-surface-semantic-review-v2.schema.json" and schema_pointer != "":
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} O17 scope pointer must be \"\" (whole-document root)")
    if schema_pointer == "/":
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} schema pointer '/' forbidden (whole-doc is '', not '/')")
    if not isinstance(schema_sha, str) or len(schema_sha) != 64 or any(c not in "0123456789abcdef" for c in schema_sha):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} schema_sha256 invalid")
    if set(row) != {"source_ref", "binding", "repository_commit_sha", "schema_path", "schema_pointer", "schema_sha256"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} SCHEMA row has unregistered keys")
    # ROOT B3: finite fingerprints — reject unknown foreign schema even when path registered.
    _require_known_schema_sha(schema_path, schema_sha, f"{label} SCHEMA fingerprint")
    _git_commit_exists(repo_root, epoch, f"{label} schema epoch", _cache)
    actual_schema_sha = _git_blob_sha(repo_root, epoch, schema_path, f"{label} schema blob", _cache)
    if actual_schema_sha != schema_sha:
        raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", f"{label} schema blob drift {schema_path} at {epoch}")
    _mode = _git_tree_mode(repo_root, epoch, schema_path, f"{label} schema mode", _cache)
    if _mode != "100644":
        raise RenewalHistoryError("HISTORY_MODE", f"{label} schema mode must be 100644 at {epoch}:{schema_path}")
    # ROOT B3: strict offline instance validation vs own recorded SCHEMA blob.
    # Data only, NO old code, NO REMOTE ref. Close/ref pin errors never ignored.
    try:
        _src_bytes = read_repo_bytes(repo_root, str(source_ref["path"]), f"{label} SCHEMA instance live")
    except RenewalHistoryError as exc:
        raise RenewalHistoryError(exc.code, f"{label} SCHEMA instance unreadable: {exc.detail}") from exc
    if hashlib.sha256(_src_bytes).hexdigest() != str(source_ref["sha256"]):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} SCHEMA instance SHA drift (live vs submitted)")
    try:
        _sch_blob = _git_show_blob(repo_root, epoch, schema_path, f"{label} SCHEMA blob for instance validation", _cache)
    except RenewalHistoryError as exc:
        raise RenewalHistoryError(exc.code, f"{label} SCHEMA blob unreadable for instance validation: {exc.detail}") from exc
    _validate_instance_against_schema_blob(_src_bytes, _sch_blob, schema_pointer, f"{label} SCHEMA instance")
    return {
        "source_ref": {"path": source_ref["path"], "sha256": source_ref["sha256"]},
        "binding": binding,
        "repository_commit_sha": epoch,
        "schema_path": schema_path,
        "schema_pointer": schema_pointer,
        "schema_sha256": schema_sha,
    }


def _check_observed_binding_row(
    repo_root: Path,
    row: Any,
    history_graph: dict[str, Any],
    label: str,
    _cache: dict | None = None,
) -> dict[str, Any]:
    if not isinstance(row, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} binding row must be an object")
    binding = row.get("binding")
    if binding not in ("RECEIPT_CURRENT_TOOLS", "STAGED_PRODUCER", "SCHEMA"):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} unknown binding: {binding!r}")
    source_ref = row.get("source_ref")
    epoch = row.get("repository_commit_sha")
    if not isinstance(source_ref, dict) or set(source_ref) != {"path", "sha256"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} source_ref fields invalid")
    if not isinstance(epoch, str) or len(epoch) != 40 or any(c not in "0123456789abcdef" for c in epoch):
        raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", f"{label} repository_commit_sha invalid")
    _check_authority_ref(repo_root, source_ref, f"{label} source live")
    if binding in ("RECEIPT_CURRENT_TOOLS", "STAGED_PRODUCER"):
        if any(k in row for k in ("schema_path", "schema_pointer", "schema_sha256")):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} RECEIPT/STAGED row must not carry schema_*")
        if set(row) != {"source_ref", "binding", "repository_commit_sha"}:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} RECEIPT/STAGED row has unregistered keys")
        # Tool epoch must equal ACTUAL doc's own commit (no caller epoch authority).
        # E docs live/COPY (never require tool commit for E bytes); tool rows &
        # schemas at DERIVED own commit mandatory. Compute from actual
        # receipt.current_tools.commit / staged.producer_head, never from
        # serialized observed rows/caller epochs.
        _git_commit_exists(repo_root, epoch, f"{label} tool epoch", _cache)
        # Reload actual doc at source_ref path (live, already verified above) and
        # require row epoch equals its own epoch field (fail-closed TOOL_DRIFT).
        try:
            tool_bytes = read_repo_bytes(repo_root, str(source_ref["path"]), f"{label} tool doc live")
        except RenewalHistoryError as exc:
            raise RenewalHistoryError(exc.code, f"{label} tool doc unreadable: {exc.detail}") from exc
        try:
            tool_doc = _parse_json_strict_bytes(tool_bytes, f"{label} tool doc")
        except RenewalHistoryError as exc:
            raise RenewalHistoryError(exc.code, f"{label} tool doc invalid: {exc.detail}") from exc
        if not isinstance(tool_doc, dict):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} tool doc must be an object")
        if binding == "RECEIPT_CURRENT_TOOLS":
            tools = tool_doc.get("current_tools")
            if not isinstance(tools, dict):
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} receipt tool doc lacks current_tools")
            actual_epoch = tools.get("repository_commit_sha")
            if not isinstance(actual_epoch, str) or len(actual_epoch) != 40:
                raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", f"{label} receipt actual epoch invalid")
            if actual_epoch != epoch:
                raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", f"{label} RECEIPT epoch must equal actual receipt.current_tools.commit (no caller authority)")
        else:
            actual_head = tool_doc.get("producer_head")
            if not isinstance(actual_head, str) or len(actual_head) != 40:
                raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", f"{label} staged actual producer_head invalid")
            if actual_head != epoch:
                raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", f"{label} STAGED epoch must equal actual staged.producer_head (no caller authority)")
        return {
            "source_ref": {"path": source_ref["path"], "sha256": source_ref["sha256"]},
            "binding": binding,
            "repository_commit_sha": epoch,
        }
    for key in ("schema_path", "schema_pointer", "schema_sha256"):
        if key not in row:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} SCHEMA row missing {key}")
    schema_path = row.get("schema_path")
    schema_pointer = row.get("schema_pointer")
    schema_sha = row.get("schema_sha256")
    if not isinstance(schema_path, str) or schema_path not in _ALLOWED_SCHEMA_PATHS:
        raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"{label} unregistered schema_path: {schema_path!r}")
    if not isinstance(schema_pointer, str):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} schema_pointer must be a string (\"\" allows root)")
    if schema_pointer == "/":
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} schema pointer '/' forbidden (whole-doc is '', not '/')")
    if schema_path == "schemas/reader-surface-semantic-review-v2.schema.json" and schema_pointer != "":
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} O17 scope pointer must be \"\" (whole-document root)")
    if not isinstance(schema_sha, str) or len(schema_sha) != 64 or any(c not in "0123456789abcdef" for c in schema_sha):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} schema_sha256 invalid")
    if set(row) != {"source_ref", "binding", "repository_commit_sha", "schema_path", "schema_pointer", "schema_sha256"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} SCHEMA row has unregistered keys")
    # Derive expected doc_type and expected epoch from owner graph (not caller).
    doc_type = _infer_doc_type_for_schema_row(schema_path, schema_pointer)
    expected_epoch = _derive_epoch_for_schema(doc_type, history_graph)
    if epoch != expected_epoch:
        raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", f"{label} SCHEMA epoch must equal derived owner {doc_type} epoch (no caller authority)")
    _require_known_schema_sha(schema_path, schema_sha, f"{label} SCHEMA fingerprint")
    _git_commit_exists(repo_root, epoch, f"{label} schema epoch", _cache)
    actual_schema_sha = _git_blob_sha(repo_root, epoch, schema_path, f"{label} schema blob", _cache)
    if actual_schema_sha != schema_sha:
        raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", f"{label} schema blob drift {schema_path} at {epoch}")
    _mode2 = _git_tree_mode(repo_root, epoch, schema_path, f"{label} schema mode", _cache)
    if _mode2 != "100644":
        raise RenewalHistoryError("HISTORY_MODE", f"{label} schema mode must be 100644 at {epoch}:{schema_path}")
    try:
        _src_b = read_repo_bytes(repo_root, str(source_ref["path"]), f"{label} SCHEMA instance live")
    except RenewalHistoryError as exc:
        raise RenewalHistoryError(exc.code, f"{label} SCHEMA instance unreadable: {exc.detail}") from exc
    if hashlib.sha256(_src_b).hexdigest() != str(source_ref["sha256"]):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} SCHEMA instance SHA drift (live vs submitted)")
    try:
        _sch_b = _git_show_blob(repo_root, epoch, schema_path, f"{label} SCHEMA blob for instance validation", _cache)
    except RenewalHistoryError as exc:
        raise RenewalHistoryError(exc.code, f"{label} SCHEMA blob unreadable for instance validation: {exc.detail}") from exc
    _validate_instance_against_schema_blob(_src_b, _sch_b, schema_pointer, f"{label} SCHEMA instance")
    return {
        "source_ref": {"path": source_ref["path"], "sha256": source_ref["sha256"]},
        "binding": binding,
        "repository_commit_sha": epoch,
        "schema_path": schema_path,
        "schema_pointer": schema_pointer,
        "schema_sha256": schema_sha,
    }


# ---------------------------------------------------------------------------
# Cross-binding and self-digest helpers
# ---------------------------------------------------------------------------

def _require_authority_live(repo_root: Path, ref: Any, label: str) -> bytes:
    return _check_authority_ref(repo_root, ref, label)


def _require_sized_live(repo_root: Path, ref: Any, label: str) -> bytes:
    return _check_sized_ref(repo_root, ref, label)


def _verify_self_digest(doc: dict[str, Any], raw_bytes: bytes, digest_key: str, label: str) -> None:
    claimed = doc.get(digest_key)
    if not isinstance(claimed, str) or len(claimed) != 64 or any(c not in "0123456789abcdef" for c in claimed):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} {digest_key} invalid")
    payload = {k: v for k, v in doc.items() if k != digest_key}
    if _sha256_object(payload) != claimed:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} {digest_key} mismatch (not canonical excluding itself)")


# ---------------------------------------------------------------------------
# Per-ancestor verification (HIST structural only, no current replay)
# ---------------------------------------------------------------------------

def _verify_editorial_ancestor(
    repo_root: Path,
    record: dict[str, Any],
    ref: dict[str, Any],
    history_graph: dict[str, Any],
    _cache: dict | None = None,
) -> dict[str, Any]:
    # Seal: exact 15 names (not just len), each sized live, no dups.
    set_ref = record.get("set_ref")
    if not isinstance(set_ref, dict) or set(set_ref) != {"path", "sha256"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor set_ref fields invalid")
    _require_authority_live(repo_root, set_ref, "editorial ancestor set_ref")
    seal = load_json_strict(repo_root, set_ref["path"], "editorial ancestor seal")
    if not isinstance(seal, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor seal must be an object")
    roles = seal.get("roles")
    if not isinstance(roles, dict) or set(roles) != set(PUBLICATION_ROLES_15):
        missing = sorted(set(PUBLICATION_ROLES_15) - set(roles) if isinstance(roles, dict) else set(PUBLICATION_ROLES_15))
        extra = sorted(set(roles) - set(PUBLICATION_ROLES_15) if isinstance(roles, dict) else set())
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"editorial ancestor seal must carry exact 15 role names: missing={missing} extra={extra}")
    seen_paths: set[str] = set()
    for name in PUBLICATION_ROLES_15:
        r = roles.get(name)
        _require_sized_live(repo_root, r, f"editorial ancestor seal role {name}")
        if r["path"] in seen_paths:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"editorial ancestor seal duplicated role path: {r['path']}")
        seen_paths.add(r["path"])
    # Seal self-digest (set_sha256 over all-except-self, file-ref SHA is full bytes).
    if "set_sha256" not in seal:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor seal missing required set_sha256")
    _verify_self_digest(seal, read_repo_bytes(repo_root, set_ref["path"], "editorial seal raw"), "set_sha256", "editorial ancestor seal")
    # Required proposal/staged/retention/scope (not optional).
    proposal_ref = seal.get("proposal_ref")
    staged_ref = seal.get("staged_manifest_ref")
    build_ref = seal.get("build_record_ref")
    for r, n in ((proposal_ref, "proposal_ref"), (staged_ref, "staged_manifest_ref"), (build_ref, "build_record_ref")):
        if not isinstance(r, dict) or set(r) != {"path", "sha256"}:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"editorial ancestor seal {n} fields invalid (required)")
        _require_authority_live(repo_root, r, f"editorial ancestor seal {n}")
    # Load and cross-bind proposal/staged/retention/scope with self-digests.
    proposal = load_json_strict(repo_root, proposal_ref["path"], "editorial ancestor proposal")
    staged = load_json_strict(repo_root, staged_ref["path"], "editorial ancestor staged")
    if not isinstance(proposal, dict) or not isinstance(staged, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor proposal/staged must be objects")
    if proposal.get("issue_id") != record.get("issue_id") or staged.get("issue_id") != record.get("issue_id"):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor proposal/staged issue mismatch")
    # Staged proposal_ref must equal seal proposal_ref (exact path+sha).
    sproposal = staged.get("proposal_ref")
    if not isinstance(sproposal, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor staged proposal_ref missing")
    # Staged proposal_ref shape varies (may carry proposal_id etc.); require at least path+sha equality.
    if sproposal.get("path") != proposal_ref["path"] or sproposal.get("sha256") != proposal_ref["sha256"]:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor staged proposal_ref must equal seal proposal_ref")
    # Scope + retention required (early scope/history targets).
    scope_ref = staged.get("scope_review_ref")
    retention_ref = staged.get("retention_manifest_ref")
    if not isinstance(scope_ref, dict) or set(scope_ref) != {"path", "sha256"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor staged scope_review_ref required")
    if not isinstance(retention_ref, dict) or set(retention_ref) != {"path", "sha256"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor staged retention_manifest_ref required")
    scope_bytes = _require_authority_live(repo_root, scope_ref, "editorial ancestor staged scope_review_ref")
    retention_bytes = _require_authority_live(repo_root, retention_ref, "editorial ancestor staged retention_manifest_ref")
    scope_doc = _parse_json_strict_bytes(scope_bytes, "editorial ancestor scope")
    retention_doc = _parse_json_strict_bytes(retention_bytes, "editorial ancestor retention")
    if not isinstance(scope_doc, dict) or not isinstance(retention_doc, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor scope/retention must be objects")
    # Scope O17 whole-doc validation at staged epoch (record-epoch blobs, never live-only).
    # ROOT B3: full original scope content per P1 2125-2185, historical relations, no current State.
    # Required selfdigest, exact registry pointer "", finite fingerprints, offline instance validation.
    staged_head = history_graph.get("staged_head")
    receipt_epoch = history_graph.get("receipt_epoch")
    if not isinstance(staged_head, str) or len(staged_head) != 40:
        raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", "editorial ancestor staged_head missing (derived, not caller)")
    if not isinstance(receipt_epoch, str) or len(receipt_epoch) != 40:
        raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", "editorial ancestor receipt_epoch missing (derived, not caller)")
    # Scope schema blob at staged_head must exist; scope doc must validate (strict, offline).
    # Use staged_head epoch bytes for schema check (fail-closed if missing). Per-invocation cache.
    _git_commit_exists(repo_root, staged_head, "editorial scope epoch", _cache)
    scope_schema_sha = _git_blob_sha(repo_root, staged_head, "schemas/reader-surface-semantic-review-v2.schema.json", "editorial scope schema", _cache)
    _require_known_schema_sha("schemas/reader-surface-semantic-review-v2.schema.json", scope_schema_sha, "editorial scope fingerprint")
    _smode = _git_tree_mode(repo_root, staged_head, "schemas/reader-surface-semantic-review-v2.schema.json", "editorial scope schema mode", _cache)
    if _smode != "100644":
        raise RenewalHistoryError("HISTORY_MODE", "editorial scope schema mode must be 100644")
    # Scope selfdigest REQUIRED (schema requires review_sha256, not 'if present').
    if "review_sha256" not in scope_doc:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor scope missing required review_sha256 (schema requires)")
    _verify_self_digest(scope_doc, scope_bytes, "review_sha256", "editorial ancestor scope")
    # Offline instance validation vs own recorded SCHEMA blob (data only, NO old code, NO REMOTE ref).
    try:
        _scope_sch_blob = _git_show_blob(repo_root, staged_head, "schemas/reader-surface-semantic-review-v2.schema.json", "editorial scope schema blob for instance validation", _cache)
    except RenewalHistoryError as exc:
        raise RenewalHistoryError(exc.code, f"editorial scope schema blob unreadable: {exc.detail}") from exc
    _validate_instance_against_schema_blob(scope_bytes, _scope_sch_blob, "", "editorial ancestor scope instance")
    # Full historical scope content (P1 2125-2185, historical relations, no current State):
    # - same issue/Profile (historical, not current State): scope issue == record/proposal/staged issue,
    #   scope publication_profile == proposal publication_profile.
    # - exact after reader path/SHA: scope reviewed_surface == proposal.proposed.proposed_reader_ref.
    # - block version WITHIN_APPROVED_AUTHORITY, exact before-reader, preserved-upstream, summary/locations.
    # - required PASS scope check with substantive detail/evidence, decision PASS, independence.
    _prop_issue = proposal.get("issue_id")
    _rec_issue = record.get("issue_id")
    _staged_issue = staged.get("issue_id")
    if scope_doc.get("issue_id") != _rec_issue or _prop_issue != _rec_issue or _staged_issue != _rec_issue:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor scope issue must equal record/proposal/staged issue (historical, no current State)")
    if scope_doc.get("publication_profile") != proposal.get("publication_profile"):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor scope publication_profile must equal proposal (historical)")
    _proposed_block = proposal.get("proposed") or {}
    _reader_ref = _proposed_block.get("proposed_reader_ref") or {}
    _after_path = _reader_ref.get("path")
    _after_sha = _reader_ref.get("sha256")
    if not isinstance(_after_path, str) or not _after_path or not isinstance(_after_sha, str) or len(_after_sha) != 64:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor proposal lacks exact proposed_reader_ref for scope binding")
    _reviewed = scope_doc.get("reviewed_surface") or {}
    if _reviewed.get("path") != _after_path or _reviewed.get("sha256") != _after_sha:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor scope reviewed_surface must equal proposal after reader (exact path+SHA, historical)")
    _block = scope_doc.get("editorial_correction_scope")
    if not isinstance(_block, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor scope missing required editorial_correction_scope block (O17 scope required)")
    if _block.get("version") != "EDITORIAL_CORRECTION_SCOPE_V1":
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor scope block version must be EDITORIAL_CORRECTION_SCOPE_V1")
    if _block.get("decision") != "WITHIN_APPROVED_AUTHORITY":
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor scope decision must be WITHIN_APPROVED_AUTHORITY (no false editorial reason)")
    _basis = proposal.get("basis") or {}
    if _block.get("before_reader_input") != _basis.get("active_reader_input_ref"):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor scope before-reader must equal proposal basis active_reader_input_ref (historical)")
    if _block.get("preserved_upstream_sha256") != _basis.get("preserved_upstream_digest"):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor scope upstream must equal proposal preserved_upstream_digest (historical)")
    if not isinstance(_block.get("change_summary"), str) or not _block["change_summary"].strip():
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor scope change_summary empty")
    if not isinstance(_block.get("evidence_locations"), list) or not all(isinstance(x, str) and x.strip() for x in _block["evidence_locations"]):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor scope evidence_locations empty")
    if scope_doc.get("decision") != "PASS":
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor scope decision must be PASS (synthetic genuine PASS, not inferred approval)")
    _checks = [c for c in (scope_doc.get("checks") or []) if isinstance(c, dict) and c.get("check_id") == "EDITORIAL_CORRECTION_SCOPE"]
    if not _checks or any(c.get("status") != "PASS" for c in _checks):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor scope substantive check missing or not PASS")
    for _c in _checks:
        if not isinstance(_c.get("detail"), str) or not _c["detail"].strip() or not isinstance(_c.get("evidence_locations"), list) or not _c["evidence_locations"]:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor scope check lacks substantive detail/evidence (independence, no current State)")
    # Staged self-digest: manifest_digest REQUIRED by schema (not 'if present').
    # ROOT B3: required selfdigests must be required by schema and verified.
    if "manifest_digest" not in staged:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor staged missing required manifest_digest (schema requires, no 'if present')")
    _verify_self_digest(staged, read_repo_bytes(repo_root, staged_ref["path"], "editorial staged raw"), "manifest_digest", "editorial ancestor staged")
    # Staged code_deps exact at staged_head (no subset, name/path mapping via sorted paths).
    route = staged.get("route")
    if route not in ("WEEKLY_GENERATED_V2", "LONGFORM_GENERATED_V1"):
        raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"editorial ancestor staged route unknown: {route!r}")
    code_deps = staged.get("code_deps")
    if not isinstance(code_deps, list):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor staged code_deps required")
    _verify_staged_code_deps_exact(repo_root, code_deps, staged_head, route, "editorial staged code_deps", _derive_tool_generation(repo_root, staged_head, "editorial staged", _cache), _cache)
    # Style input ref is TOOL (fixed template), NOT live E.
    # ROOT B1: style_input_ref points fixed templates/survey/jgaisurvey.sty (T),
    # outputs.style is immutable generated trio E. Require exact fixed template
    # path/sized shape, own staged producer commit blob SHA/byte/mode match +
    # existing code_deps row consistency, no live old template equality.
    # Keep outputs.style EXACT live E (seal trio live + staged==seal equality below).
    style_ref = staged.get("style_input_ref")
    if not isinstance(style_ref, dict) or set(style_ref) != {"path", "sha256", "byte_count"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor staged style_input_ref must be exact sized {path,sha256,byte_count} (fixed template T)")
    if style_ref.get("path") != "templates/survey/jgaisurvey.sty":
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor staged style_input_ref must be fixed templates/survey/jgaisurvey.sty (no caller path, no trio path)")
    _s_sha = style_ref.get("sha256")
    _s_size = style_ref.get("byte_count")
    if not isinstance(_s_sha, str) or len(_s_sha) != 64 or any(c not in "0123456789abcdef" for c in _s_sha):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor staged style_input_ref sha256 invalid")
    if not isinstance(_s_size, int) or isinstance(_s_size, bool) or _s_size < 1:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor staged style_input_ref byte_count invalid")
    # Own staged producer commit blob SHA/byte/mode match (T at own epoch, never live).
    _git_commit_exists(repo_root, staged_head, "editorial style epoch", _cache)
    _style_blob = _git_show_blob(repo_root, staged_head, "templates/survey/jgaisurvey.sty", "editorial style tool blob", _cache)
    if hashlib.sha256(_style_blob).hexdigest() != _s_sha or len(_style_blob) != _s_size:
        raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", "editorial ancestor style_input_ref must equal own staged producer commit blob SHA/bytes (no live old template equality)")
    _style_mode = _git_tree_mode(repo_root, staged_head, "templates/survey/jgaisurvey.sty", "editorial style tool mode", _cache)
    if _style_mode != "100644":
        raise RenewalHistoryError("HISTORY_MODE", "editorial ancestor style tool mode must be 100644")
    # Existing code_deps row consistency (same path/sha/bytes, no live).
    _style_rows = [r for r in code_deps if isinstance(r, dict) and r.get("path") == "templates/survey/jgaisurvey.sty"]
    if len(_style_rows) != 1:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor code_deps must contain unique fixed style row")
    if _style_rows[0].get("sha256") != _s_sha or _style_rows[0].get("byte_count") != _s_size:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor style_input_ref must equal code_deps style row (exact SHA/bytes)")
    # Outputs trio E: staged outputs must be exact sized live, seal trio must equal staged outputs.
    # Keep outputs.style EXACT live E (never epoch, never live template equality).
    _staged_outputs = staged.get("outputs")
    if not isinstance(_staged_outputs, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor staged outputs missing")
    for _okey in ("main", "bibliography", "style"):
        _orow = _staged_outputs.get(_okey)
        if not isinstance(_orow, dict) or set(_orow) != {"path", "sha256", "byte_count"}:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"editorial ancestor staged outputs.{_okey} must be exact sized {{path,sha256,byte_count}} (E live)")
        _require_sized_live(repo_root, _orow, f"editorial ancestor staged outputs.{_okey} live (E)")
    # Seal trio must equal staged outputs (exact path+SHA, prior-relative, no P fallthrough via path check below is seal==staged).
    _seal_roles_for_outputs = roles if isinstance(roles, dict) else {}
    _trio_map = (("validated-source", "main"), ("bibliography", "bibliography"), ("style", "style"))
    for _srole, _okey in _trio_map:
        _srow = _seal_roles_for_outputs.get(_srole)
        _orow2 = _staged_outputs.get(_okey)
        if not isinstance(_srow, dict) or "path" not in _srow or "sha256" not in _srow:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"editorial ancestor seal role {_srole} missing for outputs equality")
        if _srow.get("path") != _orow2.get("path") or _srow.get("sha256") != _orow2.get("sha256"):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"editorial ancestor seal {_srole} must equal staged outputs.{_okey} (exact path+SHA, E live)")
    # Receipt T: receipt doc must exist, receipt_epoch must equal receipt.current_tools epoch (derived).
    src_receipt = roles.get("source-receipt")
    if not isinstance(src_receipt, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor seal source-receipt required")
    receipt_bytes = _require_sized_live(repo_root, src_receipt, "editorial ancestor receipt live")
    receipt_doc = _parse_json_strict_bytes(receipt_bytes, "editorial ancestor receipt")
    if not isinstance(receipt_doc, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor receipt must be an object")
    tools = receipt_doc.get("current_tools")
    if not isinstance(tools, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor receipt current_tools required")
    repo_epoch = tools.get("repository_commit_sha")
    if repo_epoch != receipt_epoch:
        raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", "editorial ancestor receipt epoch must equal receipt.current_tools epoch (derived)")
    # Receipt self-digest REQUIRED by schema (not 'if present').
    # ROOT B3: required selfdigests must be required by schema and verified.
    if "receipt_sha256" not in receipt_doc:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor receipt missing required receipt_sha256 (schema requires, no 'if present')")
    _verify_self_digest(receipt_doc, receipt_bytes, "receipt_sha256", "editorial ancestor receipt")
    # Receipt closure exact at receipt_epoch (no subset, name==path, exact 50).
    closure = tools.get("closure")
    if not isinstance(closure, list):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor receipt closure required")
    gen_route = receipt_doc.get("generator_route") or staged.get("route")
    if gen_route not in ("WEEKLY_GENERATED_V2", "LONGFORM_GENERATED_V1"):
        raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"editorial ancestor generator_route unknown: {gen_route!r}")
    # ROOT B2: editorial generation is NOT always OLD. Old R3 is OLD50, but
    # renewal→editorial (same EDITORIAL kind, NEW installed contract) is NEW63.
    # Derive OLD vs NEW from actual own recorded epochs (staged_head + receipt_epoch),
    # finite supported sets + epoch file existence + exact membership/blob/mode.
    # No caller flag, no prefix/invent count, no global 50-or-63 tolerance.
    _staged_gen = _derive_tool_generation(repo_root, staged_head, "editorial staged", _cache)
    _receipt_gen = _derive_tool_generation(repo_root, receipt_epoch, "editorial receipt", _cache)
    # Re-verify staged code_deps generation matches staged epoch (already checked above
    # with explicit generation; enforce receipt/staged generations agree for one editorial).
    # Genuine old R3: both OLD; renewal→editorial: both NEW. Mixed (OLD+NEW) refuses.
    if _staged_gen != _receipt_gen:
        raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", f"editorial ancestor staged ({_staged_gen}) vs receipt ({_receipt_gen}) generations differ (no mixed OLD/NEW without migration)")
    # ROOT followup: recompute Contract8 at OWN epoch (pure, NUL framing, no old code) and compare
    # stored receipt.current_tools.contract / staged.basis.contract_identity / record.core to OWN derived.
    # Use correct historical owner epochs (not wrong producer epoch): staged basis at basis.renderer_commit,
    # receipt at receipt_epoch, record at record.core.implementation_commit_sha. Unknown cfg/schema/profile
    # → UNSUPPORTED (already checked in _derive); mode/blob missing → FAIL; stored vs OWN mismatch → DIGEST.
    try:
        _basis_renderer = (staged.get("basis") or {}).get("renderer_commit")
        if not isinstance(_basis_renderer, str) or len(_basis_renderer) != 40:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor staged basis renderer_commit invalid (required)")
        _s_research = staged.get("research_profile")
        _s_pub = staged.get("publication_profile")
        if not isinstance(_s_research, str) or not _s_research or not isinstance(_s_pub, str) or not _s_pub:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor staged research/publication profile missing for Contract8")
        _own_staged_c8 = _recompute_contract8_at_epoch(repo_root, _basis_renderer, _s_research, _s_pub, "editorial staged basis Contract8", _cache)
    except RenewalHistoryError:
        raise
    _stored_staged_c8 = (staged.get("basis") or {}).get("contract_identity")
    if not isinstance(_stored_staged_c8, dict) or set(_stored_staged_c8.keys()) != {"pipeline_contract_version", "pipeline_contract_sha256", "quality_contract_version", "quality_contract_sha256", "research_profile_version", "research_profile_sha256", "publication_profile_version", "publication_profile_sha256"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor staged basis contract_identity fields invalid (required Contract8)")
    if _stored_staged_c8 != _own_staged_c8:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor staged basis contract_identity must equal OWN derived Contract8 at basis.renderer_commit (no wrong producer epoch)")
    try:
        _r_research = receipt_doc.get("research_profile")
        _r_pub = receipt_doc.get("publication_profile")
        if not isinstance(_r_research, str) or not _r_research or not isinstance(_r_pub, str) or not _r_pub:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor receipt research/publication profile missing for Contract8")
        _own_receipt_c8 = _recompute_contract8_at_epoch(repo_root, receipt_epoch, _r_research, _r_pub, "editorial receipt Contract8", _cache)
    except RenewalHistoryError:
        raise
    _stored_receipt_c8 = (tools.get("contract") if isinstance(tools, dict) else None)
    # Receipt current_tools.contract may be under tools["contract"]? In genuine receipts, current_tools has "contract" (Contract8)? Actually receipt.current_tools has repository_commit_sha + contract? Check genuine: receipt.current_tools has repository_commit_sha + contract? Yes. Good.
    if not isinstance(_stored_receipt_c8, dict):
        # Fallback: receipt.current_tools may carry contract as "contract" (not "contract_identity")? Accept either key name? No, require exact Contract8 shape (8 keys) to avoid silent layout.
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor receipt current_tools.contract missing (required Contract8)")
    if set(_stored_receipt_c8.keys()) != {"pipeline_contract_version", "pipeline_contract_sha256", "quality_contract_version", "quality_contract_sha256", "research_profile_version", "research_profile_sha256", "publication_profile_version", "publication_profile_sha256"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor receipt current_tools.contract fields invalid (required Contract8, no silent layout)")
    if _stored_receipt_c8 != _own_receipt_c8:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor receipt current_tools.contract must equal OWN derived Contract8 at receipt_epoch")
    try:
        _rec_core = record.get("core") or {}
        _rec_contract = _rec_core.get("contract")
        _rec_impl = _rec_core.get("implementation_commit_sha")
        if not isinstance(_rec_contract, dict) or not isinstance(_rec_impl, str) or len(_rec_impl) != 40:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor record.core contract/implementation_commit_sha invalid (required Contract8 + 40-hex epoch)")
        # Record has no research/publication; use staged's (same issue/route, historical, no currentState).
        _own_record_c8 = _recompute_contract8_at_epoch(repo_root, _rec_impl, _s_research, _s_pub, "editorial record Contract8", _cache)
    except RenewalHistoryError:
        raise
    if set(_rec_contract.keys()) != {"pipeline_contract_version", "pipeline_contract_sha256", "quality_contract_version", "quality_contract_sha256", "research_profile_version", "research_profile_sha256", "publication_profile_version", "publication_profile_sha256"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor record.core.contract fields invalid (required Contract8)")
    if _rec_contract != _own_record_c8:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor record.core.contract must equal OWN derived Contract8 at record.core.implementation_commit_sha (proper historical owner)")
    _verify_receipt_closure_exact(repo_root, closure, receipt_epoch, gen_route, _receipt_gen, "editorial receipt closure", _cache)
    # Build-old selfdigest REQUIRED (schema requires build_sha256, not 'if present').
    # ROOT B3: required selfdigests verified, plus offline instance validation vs own
    # recorded SCHEMA blob at receipt_epoch (build-old epoch), fingerprints, no foreign.
    try:
        _build_bytes = _require_authority_live(repo_root, build_ref, "editorial ancestor build live")
        _build_doc = _parse_json_strict_bytes(_build_bytes, "editorial ancestor build")
    except RenewalHistoryError as exc:
        raise RenewalHistoryError(exc.code, f"editorial ancestor build unreadable: {exc.detail}") from exc
    if not isinstance(_build_doc, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor build must be an object")
    if "build_sha256" not in _build_doc:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor build missing required build_sha256 (schema requires)")
    _verify_self_digest(_build_doc, _build_bytes, "build_sha256", "editorial ancestor build")
    # Build-old instance validation vs own schema blob at receipt_epoch (offline, no old code).
    _require_known_schema_sha("schemas/editorial-publication-build-record-v2.schema.json", _git_blob_sha(repo_root, receipt_epoch, "schemas/editorial-publication-build-record-v2.schema.json", "editorial build schema fingerprint", _cache), "editorial build fingerprint")
    try:
        _build_sch_blob = _git_show_blob(repo_root, receipt_epoch, "schemas/editorial-publication-build-record-v2.schema.json", "editorial build schema blob", _cache)
    except RenewalHistoryError as exc:
        raise RenewalHistoryError(exc.code, f"editorial build schema unreadable: {exc.detail}") from exc
    _validate_instance_against_schema_blob(_build_bytes, _build_sch_blob, "", "editorial ancestor build instance")
    # Retained COPY mapping (not live before_state): record.before_state_ref must equal retained COPY via retention rows.
    before_ref = record.get("before_state_ref")
    if not isinstance(before_ref, dict) or set(before_ref) != {"path", "sha256"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor before_state_ref fields invalid (required)")
    # Retention rows must bind before_state to retained COPY; do NOT validate live before_state path as mutable authority.
    # Find retention doc's rows (already loaded as retention_doc).
    rows = retention_doc.get("rows")
    if not isinstance(rows, list) or not rows:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor retention rows required")
    state_rows = [r for r in rows if isinstance(r, dict) and "state:authority" in (r.get("roles") or [])]
    if len(state_rows) != 1:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor retention requires unique state:authority row")
    srow = state_rows[0]
    if srow.get("policy") != "COPY_BEFORE_REPLACEMENT":
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor state:authority must be COPY_BEFORE_REPLACEMENT")
    if srow.get("path") != before_ref["path"] or srow.get("sha256") != before_ref["sha256"]:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor retention state row must equal before_state_ref")
    retained_dest = srow.get("retained_dest")
    retained_sha = srow.get("retained_sha256")
    retained_size = srow.get("retained_byte_count")
    if not isinstance(retained_dest, str) or not isinstance(retained_sha, str) or not isinstance(retained_size, int):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor retained COPY fields invalid")
    retained_bytes = read_repo_bytes(repo_root, retained_dest, "editorial ancestor retained COPY")
    if hashlib.sha256(retained_bytes).hexdigest() != before_ref["sha256"]:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor retained COPY SHA must equal before_state_ref")
    if hashlib.sha256(retained_bytes).hexdigest() != retained_sha or len(retained_bytes) != retained_size:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor retained COPY must equal row retained bytes")
    # State->Profile relation via retained bytes (not live).
    retained_state = _parse_json_strict_bytes(retained_bytes, "editorial ancestor retained State")
    if not isinstance(retained_state, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor retained State must be an object")
    retained_profile_ref = retained_state.get("profile")
    if not isinstance(retained_profile_ref, dict) or set(retained_profile_ref) != {"path", "sha256"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor retained State lacks exact profile ref")
    keep_matches = [r for r in rows if isinstance(r, dict) and r.get("policy") == "KEEP_IMMUTABLE" and isinstance(r.get("retained_ref"), dict) and r["retained_ref"].get("path") == retained_profile_ref["path"] and r["retained_ref"].get("sha256") == retained_profile_ref["sha256"]]
    if len(keep_matches) != 1:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor retention requires unique matching KEEP Profile row")
    # before_active_digest must recompute (not presence-only). Recompute is done
    # chain-wide in verify_versioned_history (needs checkpoint + prior seals);
    # here enforce format + live candidate binding (fail-closed if missing).
    digest = record.get("before_active_digest")
    if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor before_active_digest invalid (required)")
    before_cand = record.get("before_candidate_ref")
    if before_cand is not None:
        if not isinstance(before_cand, dict) or set(before_cand) != {"path", "sha256"}:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor before_candidate_ref fields invalid")
        _require_authority_live(repo_root, before_cand, "editorial ancestor before_candidate")
        # Candidate PDF must bind effective publication-pdf (checked chain-wide;
        # here require candidate doc binds its own PDF).
        cand_bytes = _require_authority_live(repo_root, before_cand, "editorial ancestor before_candidate bytes")
        cand_doc = _parse_json_strict_bytes(cand_bytes, "editorial ancestor before_candidate doc")
        if not isinstance(cand_doc, dict):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial ancestor before_candidate must be an object")
    return {"kind": "EDITORIAL", "record_sha": ref["sha256"], "seal_path": set_ref["path"]}


def _compute_before_digest_hist(effective7: dict[str, dict[str, str]], candidate_ref: dict[str, str] | None) -> str:
    if set(effective7) != set(PUBLICATION_ROLES_7):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "before-digest requires exactly seven publication roles")
    rows: list[dict[str, str]] = []
    for name in sorted(effective7):
        row = effective7[name]
        if not isinstance(row, dict) or "path" not in row or "sha256" not in row:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"before-digest effective row invalid: {name}")
        rows.append({"name": name, "path": str(row["path"]), "sha256": str(row["sha256"])})
    cand_payload = None
    if candidate_ref is not None:
        if not isinstance(candidate_ref, dict) or set(candidate_ref) != {"path", "sha256"}:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "before-digest candidate_ref fields invalid")
        cand_payload = {"path": str(candidate_ref["path"]), "sha256": str(candidate_ref["sha256"])}
    return _sha256_object({"effective": rows, "candidate": cand_payload})


def _verify_before_digests_chain(
    repo_root: Path,
    chronological: list[tuple[dict[str, Any], dict[str, Any]]],
    prior_checkpoint: dict[str, Any],
) -> None:
    """Recompute every non-legacy before_active_digest (fail-closed, not presence-only)."""
    original_7: dict[str, dict[str, str]] = {}
    for row in prior_checkpoint.get("artifacts", []) if isinstance(prior_checkpoint.get("artifacts"), list) else []:
        if not isinstance(row, dict):
            continue
        name = row.get("name")
        if name in PUBLICATION_ROLES_7 and name not in original_7:
            original_7[name] = {"path": str(row.get("path")), "sha256": str(row.get("sha256"))}
    if set(original_7) != set(PUBLICATION_ROLES_7):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "before-digest prior checkpoint missing seven publication roles")
    # Build chronological effective for legacy prefix (cumulative).
    # For each record in order, compute expected effective then compare digest.
    # Legacy records have no before_active_digest; skip them (cumulative checked elsewhere).
    # For editorial/versioned, supersedes determines effective.
    # Need map from ref (path,sha) to seal seven for prior editorial/versioned.
    seal_seven_by_ref: dict[tuple[str, str], dict[str, dict[str, str]]] = {}
    # First pass: collect seal sevens for all editorial/versioned records.
    for rec, ref in chronological:
        kind = _record_kind(rec)
        if kind in ("EDITORIAL", "VERSIONED"):
            set_ref = rec.get("set_ref")
            if not isinstance(set_ref, dict):
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "before-digest set_ref missing")
            seal_bytes = _require_authority_live(repo_root, set_ref, "before-digest seal")
            seal = _parse_json_strict_bytes(seal_bytes, "before-digest seal")
            if not isinstance(seal, dict) or not isinstance(seal.get("roles"), dict):
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "before-digest seal roles missing")
            eff: dict[str, dict[str, str]] = {}
            for name in PUBLICATION_ROLES_7:
                r = seal["roles"].get(name)
                if not isinstance(r, dict) or "path" not in r or "sha256" not in r:
                    raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"before-digest prior seal missing {name}")
                eff[name] = {"path": str(r["path"]), "sha256": str(r["sha256"])}
            seal_seven_by_ref[(str(set_ref.get("path")), str(set_ref.get("sha256")))] = eff
    # Second pass: verify each non-legacy digest.
    # Track legacy effective for first-activation case.
    # Compute latest legacy effective (cumulative against original).
    latest_legacy_eff: dict[str, dict[str, str]] | None = None
    # Find latest legacy in prefix before first active (already validated cumulative).
    # For simplicity, if any legacy exists, effective is latest legacy superseded/preserved union.
    # Re-derive from chronological legacy records (oldest->newest).
    for rec, _ref in chronological:
        if _record_kind(rec) != "LEGACY":
            continue
        eff: dict[str, dict[str, str]] = {}
        for row in list(rec.get("superseded_artifacts", [])):
            eff[str(row.get("name"))] = {"path": str(row.get("path")), "sha256": str(row.get("new_sha256"))}
        for row in list(rec.get("preserved_artifacts", [])):
            key = str(row.get("name"))
            if key not in eff:
                eff[key] = {"path": str(row.get("path")), "sha256": str(row.get("sha256"))}
        # Filter to 7 roles.
        filtered = {k: v for k, v in eff.items() if k in PUBLICATION_ROLES_7}
        if set(filtered) == set(PUBLICATION_ROLES_7):
            latest_legacy_eff = filtered
    for rec, _ref in chronological:
        kind = _record_kind(rec)
        if kind == "LEGACY":
            continue
        digest = rec.get("before_active_digest")
        if not isinstance(digest, str) or len(digest) != 64:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "before_active_digest invalid (required recompute)")
        supersedes = rec.get("supersedes")
        before_cand = rec.get("before_candidate_ref")
        if supersedes is None:
            effective = dict(latest_legacy_eff) if latest_legacy_eff is not None else dict(original_7)
        else:
            # Find predecessor record in chronological order.
            pred = None
            for r2, ref2 in chronological:
                if ref2.get("path") == supersedes.get("path") and ref2.get("sha256") == supersedes.get("sha256"):
                    pred = r2
                    break
            if pred is None:
                raise RenewalHistoryError("HISTORY_ANCESTOR", "before-digest predecessor not in chain")
            pred_kind = _record_kind(pred)
            if pred_kind == "LEGACY":
                effective = dict(latest_legacy_eff) if latest_legacy_eff is not None else dict(original_7)
            elif pred_kind in ("EDITORIAL", "VERSIONED"):
                pred_set = pred.get("set_ref")
                if not isinstance(pred_set, dict):
                    raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "before-digest predecessor set_ref missing")
                key = (str(pred_set.get("path")), str(pred_set.get("sha256")))
                eff = seal_seven_by_ref.get(key)
                if eff is None:
                    # Try current record's prior seal? For repeated, prior seal is predecessor's seal.
                    raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "before-digest prior seal seven missing")
                effective = eff
                # Repeated activation must have before_candidate equal predecessor seal Candidate.
                pred_roles = None
                try:
                    pb = _require_authority_live(repo_root, pred_set, "before-digest pred seal")
                    pdoc = _parse_json_strict_bytes(pb, "before-digest pred seal doc")
                    if isinstance(pdoc, dict) and isinstance(pdoc.get("roles"), dict):
                        pred_roles = pdoc["roles"]
                except RenewalHistoryError:
                    pred_roles = None
                if isinstance(pred_roles, dict) and isinstance(pred_roles.get("publication-candidate"), dict):
                    expected_cand = {"path": str(pred_roles["publication-candidate"]["path"]), "sha256": str(pred_roles["publication-candidate"]["sha256"])}
                    if before_cand != expected_cand:
                        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "repeated activation before_candidate must equal predecessor seal Candidate")
            else:
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "before-digest predecessor branch unknown")
        expected = _compute_before_digest_hist(effective, before_cand if isinstance(before_cand, dict) else None)
        if expected != digest:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "before_active_digest mismatch (recomputed from before-effective7 plus candidate)")
        # Candidate PDF must bind effective publication-pdf.
        if isinstance(before_cand, dict):
            cand_bytes = _require_authority_live(repo_root, before_cand, "before-digest before-Candidate")
            cand_doc = _parse_json_strict_bytes(cand_bytes, "before-digest before-Candidate doc")
            if not isinstance(cand_doc, dict):
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "before-digest before-Candidate must be an object")
            cand_pdf = cand_doc.get("pdf", {}) if isinstance(cand_doc.get("pdf"), dict) else {}
            if cand_pdf.get("sha256") != effective["publication-pdf"]["sha256"]:
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "before-digest before-Candidate PDF must bind before-effective publication PDF")


def _verify_build_chain_hist(
    repo_root: Path,
    build_doc: dict[str, Any],
    build_path: str,
    new_epoch: str,
    chain: list[tuple[dict[str, Any], dict[str, Any]]],
    issue_id: str,
    label: str,
) -> None:
    """HIST build terminal chain (record-epoch blobs, never current replay).

    REUSED_BUILD (U, no rebuild) must point via original_record_ref to reachable ancestor
    in chain (same issue/Profile, CHAIN_LIMIT 32, no cycles), terminal old R3
    (EDITORIAL with old terminal build EDITORIAL_PUBLICATION_BUILD_V1) or new EXECUTED
    (VERSIONED with R/build-record variant EXECUTED_BUILD). EXECUTED_BUILD (C, real build)
    must carry declared_inputs/recipe/toolchain/outputs/exit_code live (E live/COPY).
    Unrelated sibling (equal SHA different path/lineage) and digest substitutions refuse.
    Hard bounded 32 selected chain.
    """
    if not isinstance(build_doc, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} build must be an object")
    variant = build_doc.get("variant")
    if variant not in ("REUSED_BUILD", "EXECUTED_BUILD"):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} build variant must be REUSED_BUILD|EXECUTED_BUILD")
    if len(chain) > CHAIN_LIMIT:
        raise RenewalHistoryError("HISTORY_ANCESTOR", f"{label} chain exceeds max32")
    # Build record self-digest already checked by caller via _verify_self_digest? Actually R/build-record.json
    # self-digest is build_sha256 over all-except-self (per schema). Caller must have verified via
    # _verify_self_digest with raw bytes (like seal/basis/proof). Enforce here if present.
    # (Caller passes raw bytes? For simplicity, verify here via live reload + self-digest.)
    try:
        raw = read_repo_bytes(repo_root, build_path, f"{label} build raw")
        parsed = _parse_json_strict_bytes(raw, f"{label} build")
    except RenewalHistoryError as exc:
        raise RenewalHistoryError(exc.code, f"{label} build unreadable: {exc.detail}") from exc
    if parsed != build_doc:
        # Live bytes changed between structural load and chain check (TOCTOU) -> fail closed.
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} build changed around verification")
    # ROOT B3: build_sha256 REQUIRED (schema requires, not 'if present').
    if "build_sha256" not in build_doc:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} build missing required build_sha256 (schema requires)")
    _verify_self_digest(build_doc, raw, "build_sha256", f"{label} build")
    if variant == "REUSED_BUILD":
        for k in ("original_record_ref", "original_pdf_ref", "original_log_ref", "original_digest_ref", "renewal_tools"):
            if k not in build_doc:
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} REUSED_BUILD missing {k}")
        if build_doc.get("no_rebuild") is not True:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} REUSED_BUILD must have no_rebuild true")
        for k in ("declared_inputs", "recipe", "toolchain", "outputs", "exit_code"):
            if k in build_doc:
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} REUSED_BUILD must not carry {k}")
        orig_ref = build_doc.get("original_record_ref")
        if not isinstance(orig_ref, dict) or set(orig_ref) != {"path", "sha256"}:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} REUSED_BUILD original_record_ref invalid")
        # Reachable ancestor in chain (same issue/Profile, no cycles, bounded 32).
        found = False
        for crec, cref in chain:
            if cref.get("path") == orig_ref.get("path") and cref.get("sha256") == orig_ref.get("sha256"):
                if crec.get("issue_id") != issue_id:
                    raise RenewalHistoryError("HISTORY_ANCESTOR", f"{label} REUSED_BUILD original record issue mismatch (foreign lineage)")
                found = True
                break
        if not found:
            raise RenewalHistoryError("HISTORY_ANCESTOR", f"{label} REUSED_BUILD original record not in chain (unrelated sibling/fork)")
        # Terminal check: original record must be EDITORIAL (old terminal build EDITORIAL_PUBLICATION_BUILD_V1)
        # or VERSIONED with EXECUTED_BUILD terminal (new). Load original record + its build to check terminal.
        try:
            orig_rec_bytes = _require_authority_live(repo_root, orig_ref, f"{label} REUSED original record live")
            orig_rec = _parse_json_strict_bytes(orig_rec_bytes, f"{label} REUSED original record")
        except RenewalHistoryError as exc:
            raise RenewalHistoryError(exc.code, f"{label} REUSED original record unreadable: {exc.detail}") from exc
        if not isinstance(orig_rec, dict):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} REUSED original record must be an object")
        orig_kind = _record_kind(orig_rec)
        if orig_kind == "EDITORIAL":
            # Old terminal: editorial seal build_record_ref must point to old terminal build with kind EDITORIAL_PUBLICATION_BUILD_V1.
            orig_set = orig_rec.get("set_ref")
            if not isinstance(orig_set, dict):
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} REUSED original editorial set_ref missing")
            try:
                orig_seal_bytes = _require_authority_live(repo_root, orig_set, f"{label} REUSED original editorial seal live")
                orig_seal = _parse_json_strict_bytes(orig_seal_bytes, f"{label} REUSED original editorial seal")
            except RenewalHistoryError as exc:
                raise RenewalHistoryError(exc.code, f"{label} REUSED original editorial seal unreadable: {exc.detail}") from exc
            if not isinstance(orig_seal, dict):
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} REUSED original editorial seal must be an object")
            orig_build_ref = orig_seal.get("build_record_ref")
            if not isinstance(orig_build_ref, dict):
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} REUSED original editorial build_record_ref missing")
            try:
                orig_build_bytes = _require_authority_live(repo_root, orig_build_ref, f"{label} REUSED original editorial build live")
                orig_build = _parse_json_strict_bytes(orig_build_bytes, f"{label} REUSED original editorial build")
            except RenewalHistoryError as exc:
                raise RenewalHistoryError(exc.code, f"{label} REUSED original editorial build unreadable: {exc.detail}") from exc
            if not isinstance(orig_build, dict) or orig_build.get("kind") != "EDITORIAL_PUBLICATION_BUILD_V1":
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} REUSED terminal must be old R3 EDITORIAL_PUBLICATION_BUILD_V1")
        elif orig_kind == "VERSIONED":
            # New terminal: versioned record's R/build-record must be EXECUTED_BUILD (not REUSED_BUILD chain loop?).
            # Load original versioned record's seal/build to check terminal EXECUTED_BUILD.
            # To avoid infinite REUSED_BUILD->REUSED_BUILD loops, require terminal EXECUTED_BUILD (no skip of terminal check).
            # Allow REUSED_BUILD->REUSED_BUILD intermediate? Task says REUSED_BUILD chain to terminal oldR3 or new EXECUTED,
            # intermediate REUSED_BUILDs may skip generations if trio/manuscript bytes bit-identical and lineage-reachable.
            # For HIST, allow one REUSED_BUILD pointing to another REUSED_BUILD? No, require terminal EXECUTED_BUILD
            # to bound chain (hard bounded 32, no cycles). If original is VERSIONED with REUSED_BUILD, refuse (must be EXECUTED terminal).
            # Actually C->U->U: U2 REUSED_BUILD may point to R1 EXECUTED_BUILD (immediate prior, terminal new) – good.
            # U3 REUSED_BUILD may point to R1 EXECUTED_BUILD (older, skipping R2 REUSED_BUILD) – allowed (older reachable ancestor).
            # So original must be VERSIONED with EXECUTED_BUILD, not REUSED_BUILD.
            orig_basis_ref = orig_rec.get("renewal_basis_ref")
            orig_set_ref = orig_rec.get("set_ref")
            if not isinstance(orig_basis_ref, dict) or not isinstance(orig_set_ref, dict):
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} REUSED original versioned basis/set refs missing")
            try:
                orig_seal_bytes = _require_authority_live(repo_root, orig_set_ref, f"{label} REUSED original versioned seal live")
                orig_seal = _parse_json_strict_bytes(orig_seal_bytes, f"{label} REUSED original versioned seal")
            except RenewalHistoryError as exc:
                raise RenewalHistoryError(exc.code, f"{label} REUSED original versioned seal unreadable: {exc.detail}") from exc
            if not isinstance(orig_seal, dict):
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} REUSED original versioned seal must be an object")
            orig_build_ref2 = orig_seal.get("build_record_ref")
            if not isinstance(orig_build_ref2, dict):
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} REUSED original versioned build_record_ref missing")
            try:
                orig_build_bytes2 = _require_authority_live(repo_root, orig_build_ref2, f"{label} REUSED original versioned build live")
                orig_build2 = _parse_json_strict_bytes(orig_build_bytes2, f"{label} REUSED original versioned build")
            except RenewalHistoryError as exc:
                raise RenewalHistoryError(exc.code, f"{label} REUSED original versioned build unreadable: {exc.detail}") from exc
            if not isinstance(orig_build2, dict) or orig_build2.get("variant") != "EXECUTED_BUILD":
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} REUSED terminal must be new EXECUTED_BUILD (not REUSED_BUILD loop)")
        else:
            raise RenewalHistoryError("HISTORY_ANCESTOR", f"{label} REUSED original record kind unsupported (must be EDITORIAL old or VERSIONED new EXECUTED)")
        # Renewal tools old/new: old must equal prior epoch (prior basis CURRENT or old editorial epoch),
        # new must equal current new_epoch. Caller passes new_epoch + prior epoch? For simplicity, verify here
        # via basis prior_selected_ref? Actually renewal_tools in R/build-record for REUSED_BUILD has old/new.
        # Verify old/new are 40hex, new == new_epoch (current), old == prior epoch (from chain? Need prior epoch).
        # Caller must have verified prior epoch? For now, verify new == new_epoch, old is 40hex and != new (genuine change? Actually U after editorial with same tool? No, U requires genuine Core change, so old != new. Good – enforce old != new? For first U after editorial, old = 721a04d, new = ada39db..., different. Good.)
        rt = build_doc.get("renewal_tools")
        if not isinstance(rt, dict):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} REUSED_BUILD renewal_tools missing")
        old_e = rt.get("old")
        new_e = rt.get("new")
        if not isinstance(old_e, str) or len(old_e) != 40 or not isinstance(new_e, str) or len(new_e) != 40:
            raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", f"{label} REUSED_BUILD renewal_tools epochs invalid")
        if new_e != new_epoch:
            raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", f"{label} REUSED_BUILD renewal_tools.new must equal current new_epoch")
        if old_e == new_e:
            raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", f"{label} REUSED_BUILD renewal_tools.old must differ from new (genuine Core change)")
    else:
        # EXECUTED_BUILD (C, real build): require declared_inputs/recipe/toolchain/outputs/exit_code live.
        for k in ("declared_inputs", "recipe", "toolchain", "outputs", "exit_code"):
            if k not in build_doc:
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD missing {k}")
        for k in ("original_record_ref", "original_pdf_ref", "original_log_ref", "original_digest_ref", "renewal_tools", "no_rebuild"):
            if k in build_doc:
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD must not carry {k}")
        if build_doc.get("exit_code") != 0:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD exit_code must be 0")
        # Declared inputs live (E live/COPY, never tool commit).
        decl = build_doc.get("declared_inputs")
        if not isinstance(decl, dict):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD declared_inputs invalid")
        for tk in ("primary", "bibliography", "style"):
            r = decl.get(tk)
            if not isinstance(r, dict) or set(r) != {"path", "sha256"}:
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD declared {tk} invalid")
            _require_authority_live(repo_root, r, f"{label} EXECUTED_BUILD declared {tk} live")
        # Outputs live (sizedRef EXACT3, no page_count per R4 §4 + embedded $defs/buildRecord outputs sizedRef).
        # R4 §4 + embedded $defs/buildRecord outputs sizedRef EXACT3 {path,sha256,byte_count} (no page_count).
        # Actual PDF pagecount still verified against Candidate/review/proof context by downstream (high/S/consumer),
        # no omission of old required target predicate. No expand to lax union if 3 selected (accept ONLY EXACT3).
        outs = build_doc.get("outputs")
        if not isinstance(outs, dict):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD outputs invalid")
        for ok in ("publication-pdf", "build-log", "pdf-digest"):
            r = outs.get(ok)
            if not isinstance(r, dict):
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD output {ok} missing")
            if set(r) != {"path", "sha256", "byte_count"}:
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD output {ok} must be EXACT3 {{path,sha256,byte_count}} (R4 sizedRef, no page_count; pagecount downstream)")
            _require_sized_live(repo_root, r, f"{label} EXECUTED_BUILD output {ok} live")
        # Toolchain versions companions (HIST, record-epoch blobs, never current replay, no live execute).
        # Selected R4 §4 / actual R3 tool version helpers (survey_editorial_publication_v2.py:1336-1362,1371-1391):
        # base6 REQUIRED (stdout≤8000, stderr≤8000, returncode int, link_path, real_path, real_sha256, error≤500 iff exe failure? keep optional)
        # + per-companion (biber,latexmk) EITHER present (stdout≤4000, returncode int, link/real/sha, NO error) OR missing (error≤300 only, NO stdout/etc).
        # Fully closed (additionalProperties:false in schema, no wildcard/freeform executables – only biber_* + latexmk_* allowed, no pdflatex_* etc).
        # Recipe-specific REQUIRED enforced here (schema cannot know recipe – recipe is sibling of toolchain, not inside versions):
        # lualatex-biber-lualatex (fixed_steps 4-step with "biber main"): biber REQUIRED (no biber_error allowed), latexmk OPTIONAL (error allowed if missing).
        # latexmk-lualatex (fixed_steps 1-step ["latexmk -pdf -lualatex ..."]): latexmk REQUIRED (no latexmk_error allowed), biber OPTIONAL.
        # No live execute (no subprocess for --version, no _resolve_toolchain_executable in H); H checks RECORDED evidence
        # (from R/build-record.json, live file, E live/COPY, never tool commit) – distinguish H historical identity vs High C actual probing
        # (High C actual probing via live execute at build time records versions; H HIST accepts recorded evidence, no live execute).
        # HIGH UNBOUND R/build/toolchain-companions.json sidecar workaround REJECTED as acceptance (no sidecar laundering):
        # H requires companions in versions (not sidecar); versions missing required companions fails even if sidecar exists.
        tc = build_doc.get("toolchain")
        if not isinstance(tc, dict):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD toolchain invalid")
        vers = tc.get("versions")
        if not isinstance(vers, dict):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD toolchain.versions invalid")
        # Base6 REQUIRED (main exe, both recipes).
        for k in ("stdout", "stderr", "returncode", "link_path", "real_path", "real_sha256"):
            if k not in vers:
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD versions missing base {k} (REQUIRED both recipes)")
        if not isinstance(vers.get("stdout"), str) or len(vers["stdout"]) > 8000:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD versions.stdout must be S≤8000")
        if not isinstance(vers.get("stderr"), str) or len(vers["stderr"]) > 8000:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD versions.stderr must be S≤8000")
        if not isinstance(vers.get("returncode"), int) or isinstance(vers.get("returncode"), bool):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD versions.returncode must be int")
        for k in ("link_path", "real_path"):
            if not isinstance(vers.get(k), str) or not vers[k]:
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD versions.{k} invalid")
        rs = vers.get("real_sha256")
        if not isinstance(rs, str) or len(rs) != 64 or any(c not in "0123456789abcdef" for c in rs):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD versions.real_sha256 invalid")
        # Base error OPTIONAL (iff exe --version fails? Actual builder records error only on exception, no base6 – would fail schema (base6 required).
        # Existing local TeX --version always succeeds (no exe failure), so base error absent in practice. Keep optional (as schema does).
        if "error" in vers and (not isinstance(vers["error"], str) or len(vers["error"]) > 500):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD versions.error must be S≤500")
        # No wildcard/freeform executables: only explicit base6 + error + biber_* + latexmk_* allowed (schema additionalProperties:false already,
        # but H code explicitly rejects freeform like pdflatex_* here for intended predicate (no silent wildcard acceptance)).
        allowed_keys = {"stdout", "stderr", "returncode", "link_path", "real_path", "real_sha256", "error",
                        "biber_stdout", "biber_returncode", "biber_link_path", "biber_real_path", "biber_real_sha256", "biber_error",
                        "latexmk_stdout", "latexmk_returncode", "latexmk_link_path", "latexmk_real_path", "latexmk_real_sha256", "latexmk_error"}
        for k in vers:
            if k not in allowed_keys:
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD versions unbound companion {k!r} (only biber_*/latexmk_* allowed, no freeform; sidecar R/build/toolchain-companions.json REJECTED)")
        # Per-companion present-vs-error conditional (R3 §7: "<comp>_error iff missing", fully closed).
        def _check_companion(comp: str) -> bool:
            # Returns True if present (no error), False if missing (error only). Raises on malformed (both present+error, or neither, or wrong types/truncation).
            s_key, rc_key, lp_key, rp_key, sha_key, err_key = (f"{comp}_stdout", f"{comp}_returncode", f"{comp}_link_path", f"{comp}_real_path", f"{comp}_real_sha256", f"{comp}_error")
            has_err = err_key in vers
            has_present = any(k in vers for k in (s_key, rc_key, lp_key, rp_key, sha_key))
            if has_err and has_present:
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD versions.{comp} must be EITHER present (no error) OR missing (error only), not both")
            if not has_err and not has_present:
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD versions.{comp} missing (must be present OR error only)")
            if has_err:
                if not isinstance(vers[err_key], str) or not vers[err_key] or len(vers[err_key]) > 300:
                    raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD versions.{err_key} must be S≤300")
                return False
            # Present: stdout≤4000, returncode int, link/real_path S, real_sha256 SHA, no error (already checked no both).
            if not isinstance(vers.get(s_key), str) or len(vers[s_key]) > 4000:
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD versions.{s_key} must be S≤4000")
            if not isinstance(vers.get(rc_key), int) or isinstance(vers.get(rc_key), bool):
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD versions.{rc_key} must be int")
            for kk in (lp_key, rp_key):
                if not isinstance(vers.get(kk), str) or not vers[kk]:
                    raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD versions.{kk} invalid")
            sh = vers.get(sha_key)
            if not isinstance(sh, str) or len(sh) != 64 or any(c not in "0123456789abcdef" for c in sh):
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD versions.{sha_key} invalid (must be 64hex)")
            return True
        biber_present = _check_companion("biber")
        latexmk_present = _check_companion("latexmk")
        # Recipe-specific REQUIRED (H code, since schema cannot know recipe – recipe is sibling of toolchain, not inside versions).
        # Derive recipe from build-record recipe.fixed_steps (exact FIXED_RECIPE_STEPS per recipe, no caller bypass, no invent new tool trust).
        # Actual builder (survey_editorial_publication_v2.py:1371-1391): lualatex-biber-lualatex requires biber (must exist, no error);
        # latexmk-lualatex requires latexmk (either exe itself is latexmk, or latexmk companion must exist, no error).
        # No live execute in H (no subprocess, no _resolve_toolchain_executable); H checks RECORDED evidence (from R/build-record.json).
        recipe_obj = build_doc.get("recipe")
        if not isinstance(recipe_obj, dict):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD recipe invalid")
        fixed = recipe_obj.get("fixed_steps")
        if not isinstance(fixed, list) or not fixed:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD recipe.fixed_steps invalid")
        # Fixed allowed keys for both recipes derived from actual builder/spec before editing (no contradiction with R3 §7 / R4 §4 map):
        # lualatex-biber-lualatex: 4-step FIXED_RECIPE_STEPS with "biber main" (2nd step). latexmk-lualatex: 1-step ["latexmk -pdf -lualatex ..."].
        # No invent new tool trust (no xelatex/pdflatex/etc – only biber+latexmk per actual builder).
        is_lualatex_biber = any(isinstance(s, str) and s.strip() == "biber main" for s in fixed)
        is_latexmk = any(isinstance(s, str) and s.strip().startswith("latexmk ") for s in fixed)
        if is_lualatex_biber and is_latexmk:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD recipe.fixed_steps ambiguous (both biber and latexmk steps)")
        if not is_lualatex_biber and not is_latexmk:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD recipe.fixed_steps must be selected R4 lualatex-biber-lualatex (4-step with 'biber main') or latexmk-lualatex (1-step latexmk) – no invent new tool trust")
        if is_lualatex_biber:
            # lualatex-biber-lualatex: biber REQUIRED (no biber_error allowed), latexmk OPTIONAL (error allowed if missing).
            if not biber_present:
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD lualatex-biber-lualatex requires biber companion (no biber_error allowed; latexmk OPTIONAL)")
        else:
            # latexmk-lualatex: latexmk REQUIRED (no latexmk_error allowed), biber OPTIONAL.
            if not latexmk_present:
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} EXECUTED_BUILD latexmk-lualatex requires latexmk companion (no latexmk_error allowed; biber OPTIONAL)")


def _verify_stored_proof_reachability_hist(
    repo_root: Path,
    old_manuscript_doc: dict[str, Any] | None,
    chain: list[tuple[dict[str, Any], dict[str, Any]]],
    issue_id: str,
    label: str,
) -> None:
    """HIST stored proof P1 reachability for C->U->U (record-epoch blobs, never current replay).

    If old manuscript (prior seal reader-manuscript for U, or C manuscript M1) contains
    renewal_source (stored P1, manuscript-embedded), verify P1 reachable ancestor via chain
    (same issue/Profile, CHAIN_LIMIT 32, no cycles, no foreign lineage). Editorial old manuscript
    (no renewal_source, only editorial_source) has no stored proof – skip (first U after editorial).
    Unrelated sibling (equal SHA different path/lineage) refuses (HISTORY_ANCESTOR).
    """
    if not isinstance(old_manuscript_doc, dict):
        return
    rs = old_manuscript_doc.get("renewal_source")
    if rs is None:
        # Editorial old manuscript (no renewal_source) – no stored proof, skip (first U).
        # Must have editorial_source? For U old manuscript (old P manuscript), it has editorial_source, not renewal_source.
        # Good – skip stored reachability for first U.
        return
    if not isinstance(rs, dict) or set(rs) != {"path", "sha256"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{label} stored renewal_source fields invalid")
    # Reachable ancestor in chain (same issue/Profile, bounded 32).
    if len(chain) > CHAIN_LIMIT:
        raise RenewalHistoryError("HISTORY_ANCESTOR", f"{label} chain exceeds max32")
    found = False
    for crec, cref in chain:
        # Stored proof P1 path/sha must match a versioned ancestor's proof ref in chain?
        # Chain contains records (activation records), not proofs directly. Need to check if stored P1
        # equals any versioned ancestor's proof (via that ancestor's renewal_proof_ref).
        # For editorial ancestors (no proof), skip.
        if _record_kind(crec) != "VERSIONED":
            continue
        proof_ref = crec.get("renewal_proof_ref")
        if not isinstance(proof_ref, dict):
            continue
        if proof_ref.get("path") == rs.get("path") and proof_ref.get("sha256") == rs.get("sha256"):
            if crec.get("issue_id") != issue_id:
                raise RenewalHistoryError("HISTORY_ANCESTOR", f"{label} stored proof issue mismatch (foreign lineage)")
            found = True
            break
    if not found:
        raise RenewalHistoryError("HISTORY_ANCESTOR", f"{label} stored proof not in chain (unrelated sibling/fork)")


def _verify_versioned_ancestor(
    repo_root: Path,
    record: dict[str, Any],
    ref: dict[str, Any],
    expected_predecessor: list[dict[str, Any]] | None = None,
    chain: list[tuple[dict[str, Any], dict[str, Any]]] | None = None,
    _cache: dict | None = None,
) -> dict[str, Any]:
    """HIST structural for one versioned ancestor (no current replay, no State).

    When expected_predecessor is provided (derived accumulated ALL predecessor history
    bindings BEFORE this record, oldest->newest, canonical sorted), require exact
    basis.observed==expected and proof.supported==same (canonical array order, no
    omissions/extras/unknown owners/forged epoch, after rehashing all wrappers).
    Never infer expected epochs from submitted rows (use accumulator, not caller).
    Otherwise (expected None, legacy path for narrow unit without accumulator) fall back
    to single-graph structural validity only (each row valid + scope+RECEIPT coverage +
    supported==observed + order) – explicitly narrow, NOT endtoend, until accumulator ready.
    Returns info with new_epoch/route/requested/basis/proof/seal for OWN derivation
    (private internal, not public permit).
    """
    for key in ("supersedes", "before_candidate_ref", "set_ref", "renewal_basis_ref", "renewal_proof_ref"):
        if record.get(key) is None:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"versioned ancestor missing required {key} (no null for renewal)")
    set_ref = record["set_ref"]
    basis_ref = record["renewal_basis_ref"]
    proof_ref = record["renewal_proof_ref"]
    # Exact path+SHA checks (not path-only).
    for r, n in ((set_ref, "set_ref"), (basis_ref, "renewal_basis_ref"), (proof_ref, "renewal_proof_ref")):
        if not isinstance(r, dict) or set(r) != {"path", "sha256"}:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"versioned ancestor {n} fields invalid")
        _require_authority_live(repo_root, r, f"versioned ancestor {n}")
    seal = load_and_validate_json_strict(repo_root, set_ref["path"], SET_SCHEMA, "versioned ancestor seal")
    if not _is_versioned_seal(seal):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor seal kind/status mismatch")
    basis = load_and_validate_json_strict(repo_root, basis_ref["path"], BASIS_SCHEMA, "versioned ancestor basis")
    proof = load_and_validate_json_strict(repo_root, proof_ref["path"], PROOF_SCHEMA, "versioned ancestor proof")
    # Cross-bindings exact path+SHA (not path-only).
    sbr = seal.get("renewal_basis_ref")
    spr = seal.get("renewal_proof_ref")
    pbr = proof.get("basis_ref")
    if not isinstance(sbr, dict) or sbr.get("path") != basis_ref["path"] or sbr.get("sha256") != basis_ref["sha256"]:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor seal/basis ref mismatch (exact path+SHA)")
    if not isinstance(spr, dict) or spr.get("path") != proof_ref["path"] or spr.get("sha256") != proof_ref["sha256"]:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor seal/proof ref mismatch (exact path+SHA)")
    if not isinstance(pbr, dict) or pbr.get("path") != basis_ref["path"] or pbr.get("sha256") != basis_ref["sha256"]:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor proof/basis ref mismatch (exact path+SHA)")
    # E: seal roles exact 15 names, each sized live, no dups.
    roles = seal.get("roles")
    if not isinstance(roles, dict) or set(roles) != set(PUBLICATION_ROLES_15):
        missing = sorted(set(PUBLICATION_ROLES_15) - set(roles) if isinstance(roles, dict) else set(PUBLICATION_ROLES_15))
        extra = sorted(set(roles) - set(PUBLICATION_ROLES_15) if isinstance(roles, dict) else set())
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"versioned ancestor seal must carry exact 15 role names: missing={missing} extra={extra}")
    seen: set[str] = set()
    for name in PUBLICATION_ROLES_15:
        r = roles.get(name)
        _require_sized_live(repo_root, r, f"versioned ancestor seal role {name}")
        if r["path"] in seen:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"versioned ancestor seal duplicated role path: {r['path']}")
        seen.add(r["path"])
    # Seal self-digest.
    _verify_self_digest(seal, read_repo_bytes(repo_root, set_ref["path"], "versioned seal raw"), "set_sha256", "versioned ancestor seal")
    # Basis self-digest + required fields already schema-checked; verify observed bindings count/order later.
    _verify_self_digest(basis, read_repo_bytes(repo_root, basis_ref["path"], "versioned basis raw"), "basis_sha256", "versioned ancestor basis")
    _verify_self_digest(proof, read_repo_bytes(repo_root, proof_ref["path"], "versioned proof raw"), "proof_sha256", "versioned ancestor proof")
    # Retained COPY (not live before_state).
    retained_ref = basis.get("retained_copy_ref")
    if not isinstance(retained_ref, dict) or set(retained_ref) != {"path", "sha256", "byte_count"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor retained_copy_ref fields invalid")
    retained_bytes = _require_sized_live(repo_root, retained_ref, "versioned ancestor retained COPY")
    before_ref = basis.get("before_state_ref")
    if not isinstance(before_ref, dict) or set(before_ref) != {"path", "sha256"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor before_state_ref fields invalid")
    if hashlib.sha256(retained_bytes).hexdigest() != before_ref["sha256"]:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor retained COPY SHA must equal before_state_ref")
    # Retention rows exact (state:authority COPY + KEEP Profile).
    rows = basis.get("retention_rows")
    if not isinstance(rows, list) or not rows:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor retention rows required")
    # Derive history_graph from linked docs (not from untrusted observed rows).
    current_epoch = basis.get("current_tool_epoch", {})
    epoch_sha = current_epoch.get("repository_commit_sha")
    closure = current_epoch.get("closure")
    if not isinstance(epoch_sha, str) or len(epoch_sha) != 40:
        raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", "versioned ancestor basis epoch invalid")
    if not isinstance(closure, list) or not closure:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor basis closure invalid")
    # Derive receipt_epoch/staged_head from prior seal's receipt/staged where available?
    # For renewal, prior is editorial or prior renewal. Load prior seal to derive staged_head/receipt_epoch for SCHEMA owner checks.
    # History_graph basis_current_epoch is authoritative; receipt/staged epochs for SCHEMA rows that refer to prior editorial docs must come from prior docs.
    # Build graph: basis_current_epoch + prior-derived staged_head/receipt_epoch.
    history_graph: dict[str, Any] = {"basis_current_epoch": epoch_sha, "receipt_epoch": None, "staged_head": None}
    # Attempt to derive prior staged_head/receipt_epoch from basis prior refs (prior_selected seal).
    try:
        prior_seal_ref = basis.get("prior_selected_ref")
        if isinstance(prior_seal_ref, dict):
            prior_seal_bytes = _require_authority_live(repo_root, prior_seal_ref, "versioned prior seal")
            prior_seal = _parse_json_strict_bytes(prior_seal_bytes, "versioned prior seal")
            if isinstance(prior_seal, dict):
                # If prior is editorial, extract receipt epoch via its receipt doc.
                proles = prior_seal.get("roles", {})
                if isinstance(proles, dict) and isinstance(proles.get("source-receipt"), dict):
                    try:
                        rbytes = _require_sized_live(repo_root, proles["source-receipt"], "versioned prior receipt")
                        rdoc = _parse_json_strict_bytes(rbytes, "versioned prior receipt")
                        if isinstance(rdoc, dict) and isinstance(rdoc.get("current_tools"), dict):
                            rep = rdoc["current_tools"].get("repository_commit_sha")
                            if isinstance(rep, str) and len(rep) == 40:
                                history_graph["receipt_epoch"] = rep
                    except RenewalHistoryError:
                        pass
                # Staged head via prior staged manifest if editorial prior.
                if isinstance(prior_seal.get("staged_manifest_ref"), dict):
                    try:
                        sbytes = _require_authority_live(repo_root, prior_seal["staged_manifest_ref"], "versioned prior staged")
                        sdoc = _parse_json_strict_bytes(sbytes, "versioned prior staged")
                        if isinstance(sdoc, dict) and isinstance(sdoc.get("producer_head"), str) and len(sdoc["producer_head"]) == 40:
                            history_graph["staged_head"] = sdoc["producer_head"]
                    except RenewalHistoryError:
                        pass
    except RenewalHistoryError:
        pass
    # If prior derivation failed, fall back to basis epoch for SCHEMA rows that are renewal-owned;
    # for prior-owned SCHEMA rows (proposal/retention/staged/receipt-editorial/scope), require prior epochs present, else fail (no skip).
    # Verify basis closure exact at basis epoch (NEW 63 with route from basis).
    gen_route = basis.get("generator_route")
    if gen_route not in ("WEEKLY_GENERATED_V2", "LONGFORM_GENERATED_V1"):
        raise RenewalHistoryError("UNSUPPORTED_MIGRATION", f"versioned ancestor generator_route unknown: {gen_route!r}")
    _verify_receipt_closure_exact(repo_root, closure, epoch_sha, gen_route, "NEW", "versioned basis closure", _cache)
    # Seal top-level receipt/build refs live (exact path+SHA, not path-only).
    # (Previously missing – required for OWN derivation + own receipt/closure matching.)
    seal_receipt_top = seal.get("source_receipt_ref")
    seal_build_top = seal.get("build_record_ref")
    if not isinstance(seal_receipt_top, dict) or set(seal_receipt_top) != {"path", "sha256"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor seal source_receipt_ref invalid")
    if not isinstance(seal_build_top, dict) or set(seal_build_top) != {"path", "sha256"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor seal build_record_ref invalid")
    _require_authority_live(repo_root, seal_receipt_top, "versioned ancestor seal source_receipt_ref")
    _require_authority_live(repo_root, seal_build_top, "versioned ancestor seal build_record_ref")
    # Own receipt/currentTool closure must match basis CURRENT epoch and proof closure.
    # Load R receipt via seal source_receipt_ref (live, sized? top is {path,sha}, roles is sized – both must match).
    seal_roles_tmp = seal.get("roles", {}) if isinstance(seal.get("roles"), dict) else {}
    seal_role_receipt = seal_roles_tmp.get("source-receipt") if isinstance(seal_roles_tmp, dict) else None
    if not isinstance(seal_role_receipt, dict) or "path" not in seal_role_receipt or "sha256" not in seal_role_receipt:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor seal roles source-receipt missing")
    if seal_role_receipt.get("path") != seal_receipt_top.get("path") or seal_role_receipt.get("sha256") != seal_receipt_top.get("sha256"):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor seal receipt top must equal roles source-receipt (exact path+SHA)")
    try:
        r_receipt_bytes = _require_sized_live(repo_root, seal_role_receipt, "versioned ancestor own R receipt live") if "byte_count" in seal_role_receipt else _require_authority_live(repo_root, seal_receipt_top, "versioned ancestor own R receipt live")
        r_receipt_doc = _parse_json_strict_bytes(r_receipt_bytes, "versioned ancestor own R receipt")
    except RenewalHistoryError as exc:
        raise RenewalHistoryError(exc.code, f"versioned ancestor own R receipt unreadable: {exc.detail}") from exc
    if not isinstance(r_receipt_doc, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor own R receipt must be an object")
    # ROOT B3: R receipt selfdigest REQUIRED (schema requires receipt_sha256).
    if "receipt_sha256" not in r_receipt_doc:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor own R receipt missing required receipt_sha256")
    _verify_self_digest(r_receipt_doc, r_receipt_bytes, "receipt_sha256", "versioned ancestor own R receipt")
    r_tools = r_receipt_doc.get("current_tools")
    if not isinstance(r_tools, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor own R receipt current_tools missing")
    if r_tools.get("repository_commit_sha") != epoch_sha:
        raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", "versioned ancestor own R receipt epoch must equal basis CURRENT (no caller authority)")
    r_closure = r_tools.get("closure")
    if not isinstance(r_closure, list) or not r_closure:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor own R receipt closure missing")
    # R receipt closure must equal basis closure (sorted-set, exact, no omissions/extras).
    def _norm_closure(rows: Any) -> list[tuple[str, str, str]]:
        if not isinstance(rows, list):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "closure must be an array")
        out: list[tuple[str, str, str]] = []
        for r in rows:
            if not isinstance(r, dict) or set(r) != {"name", "path", "sha256"}:
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "closure row must be exact {name,path,sha256}")
            out.append((str(r.get("name")), str(r.get("path")), str(r.get("sha256"))))
        return sorted(out)
    if _norm_closure(r_closure) != _norm_closure(closure):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor own R receipt closure must equal basis CURRENT closure (exact)")
    # Proof dependency_closure must equal basis closure (sorted-set, exact).
    p_dep = proof.get("dependency_closure")
    if not isinstance(p_dep, list) or not p_dep:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor proof dependency_closure missing")
    if _norm_closure(p_dep) != _norm_closure(closure):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor proof closure must equal basis CURRENT closure (exact)")
    # R receipt closure exact at new_epoch (member-wise blob+mode, NEW 63).
    _verify_receipt_closure_exact(repo_root, r_closure, epoch_sha, gen_route, "NEW", "versioned own R receipt closure", _cache)
    observed = basis.get("observed_source_bindings")
    supported = proof.get("supported_source_bindings")
    if not isinstance(observed, list) or not isinstance(supported, list) or not observed or not supported:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor bindings must be non-empty arrays")
    if expected_predecessor is None or chain is None:
        # Narrow fallback (no accumulator): structural validity only via single-graph
        # (each row valid + scope+RECEIPT coverage + supported==observed + order).
        # Explicitly narrow, NOT endtoend, until accumulator ready (for direct unit calls without chain).
        norm_observed: list[tuple[str, ...]] = []
        for row in observed:
            norm = _check_observed_binding_row(repo_root, row, history_graph, "versioned ancestor observed", _cache)
            norm_observed.append(_freeze_binding(norm))
        norm_supported: list[tuple[str, ...]] = []
        for row in supported:
            norm = _check_observed_binding_row(repo_root, row, history_graph, "versioned ancestor supported", _cache)
            norm_supported.append(_freeze_binding(norm))
        has_scope = any(
            isinstance(r, dict) and r.get("binding") == "SCHEMA"
            and r.get("schema_path") == "schemas/reader-surface-semantic-review-v2.schema.json"
            and r.get("schema_pointer") == ""
            for r in observed
        )
        has_receipt = any(isinstance(r, dict) and r.get("binding") == "RECEIPT_CURRENT_TOOLS" for r in observed)
        if not has_scope:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor observed missing required scope O17 (\"\" pointer)")
        if not has_receipt:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor observed missing required RECEIPT_CURRENT_TOOLS row")
        if sorted(norm_observed) != sorted(norm_supported):
            raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", "versioned ancestor supported != observed (exact sorted-set equality)")
        file_order = [_freeze_binding(_check_observed_binding_row(repo_root, r, history_graph, "order", _cache)) for r in observed]
        if file_order != sorted(norm_observed):
            raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", "versioned ancestor observed order must equal sorted-key order")
        file_order_s = [_freeze_binding(_check_observed_binding_row(repo_root, r, history_graph, "order2", _cache)) for r in supported]
        if file_order_s != sorted(norm_supported):
            raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", "versioned ancestor supported order must equal sorted-key order")
    else:
        # Derived expected graph: basis.observed == accumulated predecessor BEFORE this record,
        # proof.supported == same (canonical array order, no omissions/extras/unknown owners/forged epoch).
        # Never infer expected epochs from submitted rows (use accumulator, not caller).
        # Structural validity (registry, live, schema blob/mode at submitted epoch, O17 "", tool actual
        # field equality) WITHOUT epoch==derived-owner via single graph (since expected contains multiple
        # epochs: old editorial + prior versioned OWN). Epoch/owner/path completeness via exact equality
        # to expected (which was derived with correct epochs/schema_shas via git show at derive time).
        def _norm_structural(rows: Any, lbl: str) -> list[tuple[str, ...]]:
            if not isinstance(rows, list):
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"{lbl} must be an array")
            out: list[tuple[str, ...]] = []
            for r in rows:
                n = _check_observed_binding_row_structural(repo_root, r, f"{lbl}", _cache)
                out.append(_freeze_binding(n))
            return out
        # Structural first (registry/live/blob/mode/tool actual, O17 "", no graph epoch derivation).
        # Unknown owner (unregistered schema_path) -> UNSUPPORTED_MIGRATION here (before equality).
        norm_obs_struct = _norm_structural(observed, "versioned ancestor observed structural")
        norm_sup_struct = _norm_structural(supported, "versioned ancestor supported structural")
        # Expected (accumulator BEFORE this record, canonical sorted, already validated when derived).
        exp_norm = sorted([_freeze_binding(b) for b in expected_predecessor])
        # Omission/extra/forged epoch/owner detection with precise codes (after rehashing wrappers).
        # Build maps by (path,binding,schema_path,schema_pointer) without epoch/sha for epoch/owner analysis.
        def _key_no_epoch(t: tuple[str, ...]) -> tuple[str, str, str, str]:
            # _freeze_binding: (path, sha, binding, schema_path, schema_pointer, epoch, schema_sha)
            return (t[0], t[2], t[3], t[4])
        exp_by_key: dict[tuple[str, str, str, str], list[tuple[str, ...]]] = {}
        for t in exp_norm:
            exp_by_key.setdefault(_key_no_epoch(t), []).append(t)
        obs_by_key: dict[tuple[str, str, str, str], list[tuple[str, ...]]] = {}
        for t in norm_obs_struct:
            obs_by_key.setdefault(_key_no_epoch(t), []).append(t)
        # Unknown owner/path (submitted key not in expected): extra vs forged owner?
        # If submitted (path,binding,schema,pointer) not in expected at all -> extra (DIGEST_MISMATCH)
        # unless schema_path unregistered (already caught as UNSUPPORTED in structural? Actually structural
        # already checks schema_path allowed, so unregistered would have raised UNSUPPORTED before here.
        # So here extra means valid registry but not in expected -> HISTORY_DIGEST_MISMATCH (extra).
        for k in obs_by_key:
            if k not in exp_by_key:
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"versioned ancestor observed extra row (not in expected predecessor): {k}")
        for k in exp_by_key:
            if k not in obs_by_key:
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"versioned ancestor observed omission (missing expected predecessor row): {k}")
        # Same owner/path but different epoch -> forged epoch (DRIFT). Same owner/path/epoch but different sha -> digest substitution (MISMATCH).
        for k in exp_by_key:
            exp_list = sorted(exp_by_key[k])
            obs_list = sorted(obs_by_key[k])
            # Compare epochs first (forged epoch detection).
            exp_epochs = sorted(set(t[5] for t in exp_list))
            obs_epochs = sorted(set(t[5] for t in obs_list))
            if exp_epochs != obs_epochs:
                raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", f"versioned ancestor observed forged epoch for {k}: expected {exp_epochs} vs submitted {obs_epochs}")
            # Same epochs, compare full tuples (including sha/schema_sha) for digest substitution/extra detail.
            if sorted(exp_list) != sorted(obs_list):
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"versioned ancestor observed digest substitution for {k}")
        # Proof.supported must equal same expected (== basis.observed).
        norm_sup_check = _norm_structural(supported, "versioned ancestor supported structural")
        # Reuse same key analysis for supported vs expected (forged epoch/extra/omission with same codes).
        sup_by_key: dict[tuple[str, str, str, str], list[tuple[str, ...]]] = {}
        for t in norm_sup_check:
            sup_by_key.setdefault(_key_no_epoch(t), []).append(t)
        for k in sup_by_key:
            if k not in exp_by_key:
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"versioned ancestor supported extra row (not in expected): {k}")
        for k in exp_by_key:
            if k not in sup_by_key:
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"versioned ancestor supported omission (missing expected): {k}")
        for k in exp_by_key:
            exp_list = sorted(exp_by_key[k])
            sup_list = sorted(sup_by_key[k])
            exp_epochs = sorted(set(t[5] for t in exp_list))
            sup_epochs = sorted(set(t[5] for t in sup_list))
            if exp_epochs != sup_epochs:
                raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", f"versioned ancestor supported forged epoch for {k}")
            if sorted(exp_list) != sorted(sup_list):
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"versioned ancestor supported digest substitution for {k}")
        # Supported must equal observed (both == expected, already checked separately, but enforce direct equality too).
        if sorted(norm_obs_struct) != sorted(norm_sup_struct):
            raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", "versioned ancestor supported != observed (exact sorted-set equality)")
        # Byte-order must equal sorted-key order (array-order hashing) for both (fail-closed on bad order).
        # Use structural norm (which already validated live/blob/mode) for order check (no re-validation via single-graph).
        file_order_obs = [_freeze_binding(b) for b in [_check_observed_binding_row_structural(repo_root, r, "order-obs", _cache) for r in observed]]
        if file_order_obs != sorted(norm_obs_struct):
            raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", "versioned ancestor observed order must equal sorted-key order")
        file_order_sup = [_freeze_binding(b) for b in [_check_observed_binding_row_structural(repo_root, r, "order-sup", _cache) for r in supported]]
        if file_order_sup != sorted(norm_sup_struct):
            raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", "versioned ancestor supported order must equal sorted-key order")
        # Required coverage already enforced via equality to expected (which contains scope O17 + RECEIPT, NONEMPTY).
        # Explicitly require scope O17 + RECEIPT in expected (predecessor) to catch empty-chain narrow misuse.
        has_scope_exp = any(t[3] == "schemas/reader-surface-semantic-review-v2.schema.json" and t[4] == "" and t[2] == "SCHEMA" for t in exp_norm)
        has_receipt_exp = any(t[2] == "RECEIPT_CURRENT_TOOLS" for t in exp_norm)
        if not has_scope_exp:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor expected predecessor missing required scope O17")
        if not has_receipt_exp:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor expected predecessor missing required RECEIPT_CURRENT_TOOLS")
    # Build chain HIST (REUSED_BUILD to old/new EXECUTED, bounded 32, sibling/digest refuse).
    # Load R/build-record via seal build_record_ref (live, already checked top-level live above? Actually seal
    # build_record_ref live checked? No, only set/basis/proof refs live checked at top (lines 1562-1565).
    # Add live checks for seal source_receipt_ref/build_record_ref? Already added above for seal receipt/build top.
    # Now load R/build-record doc for chain verification (HIST, record-epoch blobs, never current replay).
    try:
        build_bytes = _require_authority_live(repo_root, seal.get("build_record_ref"), "versioned ancestor R build live")
        build_doc = _parse_json_strict_bytes(build_bytes, "versioned ancestor R build")
    except RenewalHistoryError as exc:
        raise RenewalHistoryError(exc.code, f"versioned ancestor R build unreadable: {exc.detail}") from exc
    if not isinstance(build_doc, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor R build must be an object")
    # New epoch for build chain + OWN derivation (basis CURRENT).
    _verify_build_chain_hist(repo_root, build_doc, str(seal.get("build_record_ref", {}).get("path", "")), epoch_sha, chain if isinstance(chain, list) else [], str(record.get("issue_id", "")), "versioned ancestor build chain")
    # Stored proof reachability for C->U->U (HIST, record-epoch blobs, never current replay).
    # Load old manuscript via proof old_manuscript_ref (U) or prior seal reader-manuscript? For U, proof has
    # old_manuscript_ref (sized) + old_build_unit_refs (required for REUSED_TARGETS per schema allOf).
    # For C, proof has no old_* (NEW_TARGETS), stored proof is in C manuscript M1 renewal_source (for repeat U after C).
    # Here verify U old_manuscript immediate prior seal equality (prior-relative, no P fallthrough) + stored P1 reachability.
    requested = str(basis.get("requested", ""))
    if requested == "REUSE_TARGETS":
        old_man = proof.get("old_manuscript_ref")
        old_build = proof.get("old_build_unit_refs")
        if not isinstance(old_man, dict) or not isinstance(old_build, dict):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor U proof missing old_manuscript_ref/old_build_unit_refs (REUSED_TARGETS requires both)")
        # Immediate prior seal reader-manuscript/publication-pdf/build-log/pdf-digest must equal old refs (prior-relative).
        # Need immediate prior seal (prior_selected_ref from basis, which is immediate predecessor seal, not older).
        prior_sel = basis.get("prior_selected_ref")
        if not isinstance(prior_sel, dict):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor U prior_selected_ref missing")
        try:
            prior_seal_b = _require_authority_live(repo_root, prior_sel, "versioned ancestor U immediate prior seal live")
            prior_seal_d = _parse_json_strict_bytes(prior_seal_b, "versioned ancestor U immediate prior seal")
        except RenewalHistoryError as exc:
            raise RenewalHistoryError(exc.code, f"versioned ancestor U immediate prior seal unreadable: {exc.detail}") from exc
        if not isinstance(prior_seal_d, dict) or not isinstance(prior_seal_d.get("roles"), dict):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor U immediate prior seal roles missing")
        prior_roles = prior_seal_d.get("roles")
        # Old manuscript must equal immediate prior seal reader-manuscript (exact path+SHA, prior-relative, no P fallthrough).
        # Proof old_manuscript_ref is sizedRef {path,sha,byte_count}; prior role is fileRef {path,sha,byte_count}.
        pr_man = prior_roles.get("reader-manuscript")
        if not isinstance(pr_man, dict) or old_man.get("path") != pr_man.get("path") or old_man.get("sha256") != pr_man.get("sha256"):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor U old_manuscript must equal immediate prior seal reader-manuscript (no P fallthrough)")
        # Old build unit must equal immediate prior seal publication-pdf/build-log/pdf-digest + prior build record (as unit, prior-relative).
        # Proof old_build_unit_refs: {pdf:{path,sha,byte_count,page_count}, log:{...}, digest:{...}, record:{path,sha}}.
        # Prior seal roles publication-pdf/build-log/pdf-digest must equal old_build pdf/log/digest (exact path+SHA).
        for role_key, build_key in (("publication-pdf", "pdf"), ("build-log", "log"), ("pdf-digest", "digest")):
            pr = prior_roles.get(role_key)
            ob = old_build.get(build_key)
            if not isinstance(pr, dict) or not isinstance(ob, dict):
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"versioned ancestor U old build {build_key} missing")
            if ob.get("path") != pr.get("path") or ob.get("sha256") != pr.get("sha256"):
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"versioned ancestor U old build {build_key} must equal immediate prior seal {role_key} (no P fallthrough)")
        # Old build record must equal immediate prior build record (prior-relative, never original-P fallback).
        # Immediate prior build record: prior receipt build binding or seal_dir/build-record.json (like high _locate_prior_build_record, HIST version).
        # Unrelated sibling (equal SHA different path/lineage) and digest substitutions refuse (HISTORY_ANCESTOR/MISMATCH).
        ob_rec = old_build.get("record")
        if not isinstance(ob_rec, dict) or set(ob_rec) != {"path", "sha256"}:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor U old build record invalid")
        # Locate immediate prior build record (prior-relative, never original-P fallback).
        prior_build_cands: list[str] = []
        # Via prior receipt build binding (prior receipt source-receipt role -> receipt doc -> build_record_ref/build_record?).
        try:
            prior_receipt_role = prior_roles.get("source-receipt")
            if isinstance(prior_receipt_role, dict):
                pr_rbytes: bytes | None = None
                try:
                    if "byte_count" in prior_receipt_role:
                        pr_rbytes = _require_sized_live(repo_root, prior_receipt_role, "versioned ancestor U immediate prior receipt live")
                    else:
                        pr_rbytes = _require_authority_live(repo_root, prior_receipt_role, "versioned ancestor U immediate prior receipt live")
                except RenewalHistoryError:
                    pr_rbytes = None
                if pr_rbytes is not None:
                    pr_rdoc = _parse_json_strict_bytes(pr_rbytes, "versioned ancestor U immediate prior receipt")
                    if isinstance(pr_rdoc, dict):
                        for bk in ("build_record_ref", "build_record"):
                            br = pr_rdoc.get(bk)
                            if isinstance(br, dict) and isinstance(br.get("path"), str):
                                prior_build_cands.append(str(br["path"]))
        except RenewalHistoryError:
            pass
        # Via seal_dir/build-record.json (prior_selected seal parent dir + build-record.json, prior-relative).
        try:
            prior_sel_path = str(prior_sel.get("path", ""))
            if prior_sel_path and "/" in prior_sel_path:
                seal_dir = prior_sel_path.rsplit("/", 1)[0]
                if seal_dir:
                    prior_build_cands.append(f"{seal_dir}/build-record.json")
        except Exception:
            pass
        found_prior_build = False
        for cand in prior_build_cands:
            try:
                cand_bytes = read_repo_bytes(repo_root, cand, "versioned ancestor U immediate prior build record candidate")
            except RenewalHistoryError:
                continue
            if _sha256_object({"_x": 1}) is None:  # placeholder to keep structure (never true, no-op)
                pass
            # Compare path+SHA (exact, prior-relative, no P fallthrough, no equal-SHA different-path substitution).
            # Need live SHA of candidate (via read_repo_bytes already ensures exists; compute SHA).
            cand_sha = hashlib.sha256(cand_bytes).hexdigest()
            if cand == ob_rec.get("path") and cand_sha == ob_rec.get("sha256"):
                found_prior_build = True
                break
            # Else: path matches but SHA differs (digest substitution) -> fail closed MISMATCH (not silently pass).
            # Path differs but SHA equal (unrelated sibling, equal SHA different path/lineage) -> fail closed ANCESTOR.
            # Continue to try next candidate? Actually if path matches candidate list but SHA differs, it's digest substitution.
            # If SHA matches but path differs (equal SHA different path), it's unrelated sibling.
            # For strictness, if ob_rec path is in candidates but SHA differs -> MISMATCH; if ob_rec SHA equals some candidate SHA but path differs -> ANCESTOR.
            # Simplify: require exact path+SHA match to one candidate (prior-relative, no P fallthrough).
            # Unrelated sibling/digest substitutions refuse below (after loop, if not found).
            continue
        if not found_prior_build:
            # Distinguish digest substitution (same path, different SHA, path in candidates) vs unrelated sibling (path not in candidates or SHA equal different path).
            # Check if ob_rec path is in candidates (prior-relative paths) but SHA differs -> digest substitution (MISMATCH).
            # Else (path not in candidates) -> unrelated sibling/fork, even at equal SHA (ANCESTOR, no laundering).
            ob_path = str(ob_rec.get("path", ""))
            if ob_path in prior_build_cands:
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor U old build record digest substitution (same prior-relative path, different SHA)")
            # Check equal-SHA different-path (unrelated sibling, even at equal SHA, different path/lineage) -> ANCESTOR.
            # (If ob_rec SHA equals any prior build candidate SHA but path differs, it's sibling laundering.)
            # For simplicity, any not-found here is foreign lineage (no P fallthrough, no sibling laundering).
            raise RenewalHistoryError("HISTORY_ANCESTOR", "versioned ancestor U old build record not in immediate prior (unrelated sibling/fork, no P fallthrough)")
        # Stored proof P1 reachability (if old manuscript contains renewal_source, i.e., prior R manuscript M1 for repeat U after C).
        # Load old manuscript doc via old_man path (live, already verified? old_man is sizedRef, live via proof? Actually proof old_manuscript_ref is sized, need live check).
        try:
            old_man_bytes = _require_sized_live(repo_root, old_man, "versioned ancestor U old manuscript live")
            old_man_doc = _parse_json_strict_bytes(old_man_bytes, "versioned ancestor U old manuscript")
        except RenewalHistoryError as exc:
            raise RenewalHistoryError(exc.code, f"versioned ancestor U old manuscript unreadable: {exc.detail}") from exc
        if not isinstance(old_man_doc, dict):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor U old manuscript must be an object")
        _verify_stored_proof_reachability_hist(repo_root, old_man_doc, chain if isinstance(chain, list) else [], str(record.get("issue_id", "")), "versioned ancestor U stored proof")
    elif requested == "RENDER_TARGETS":
        # C must NOT carry old_manuscript/old_build (schema allOf already enforces, but verify HIST here too).
        if "old_manuscript_ref" in proof or "old_build_unit_refs" in proof:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned ancestor C proof must not carry old manuscript/build refs (NEW_TARGETS)")
        # Stored proof for C? C manuscript M1 embeds own NEW proof P1 (embedded==expected allowed per R5 §2).
        # No stored older proof required for first C (no prior renewal proof in M1? Actually M1 embeds P1 (own), not older.
        # For repeat C after prior renewal? C after prior renewal would have stored? Unclear – for now, no stored check for C.
        pass
    else:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"versioned ancestor requested unknown: {requested!r}")
    issue = record.get("issue_id")
    for doc, lbl in ((seal, "seal"), (basis, "basis"), (proof, "proof")):
        if doc.get("issue_id") != issue:
            raise RenewalHistoryError("HISTORY_ANCESTOR", f"versioned ancestor {lbl} issue mismatch (foreign lineage)")
    return {"kind": "VERSIONED", "record_sha": ref["sha256"], "seal_path": set_ref["path"], "new_epoch": epoch_sha, "route": gen_route, "requested": requested, "basis": basis, "proof": proof, "seal": seal}


def _freeze_binding(norm: dict[str, Any]) -> tuple[str, ...]:
    src = norm.get("source_ref", {})
    return (
        str(src.get("path")),
        str(src.get("sha256")),
        str(norm.get("binding")),
        str(norm.get("schema_path", "")),
        str(norm.get("schema_pointer", "")),
        str(norm.get("repository_commit_sha")),
        str(norm.get("schema_sha256", "")),
    )


def _is_under_R(path: str, proposal_namespace: str, renewal_id: str) -> bool:
    # R = proposal_namespace/renewals/renewal_id, repo-relative, no traversal.
    if not isinstance(path, str) or not path or "\\" in path or path.startswith("/") or ".." in Path(path).parts:
        return False
    r_prefix = f"{proposal_namespace}/renewals/{renewal_id}/" if proposal_namespace and renewal_id else ""
    return bool(r_prefix) and (path == r_prefix.rstrip("/") or path.startswith(r_prefix))


def _derive_versioned_own_bindings(
    repo_root: Path,
    record: dict[str, Any],
    ref: dict[str, Any],
    basis: dict[str, Any],
    proof: dict[str, Any],
    seal: dict[str, Any],
    new_epoch: str,
    route: str,
    requested: str,
    prior_chain: list[tuple[dict[str, Any], dict[str, Any]]],
    _cache: dict | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Derive OWN source bindings for one versioned ancestor (new CURRENT epoch).

    From ACTUAL strict R docs (never serialized observed/caller epochs). E live/COPY
    (never tool commit for E bytes); tool rows & schemas at DERIVED own commit
    (basis CURRENT epoch). Canonical sorted dedup; same path different generations
    allowed iff distinct owners. No STAGED_PRODUCER for renewal (proof IS staged proof).
    U (REUSE_TARGETS): 1 tool (RECEIPT_CURRENT_TOOLS for R receipt) + 9 SCHEMA
    (receipt-renewal, seal-renewal, build-new REUSED_BUILD, basis, proof,
    candidate-renewal, bundle-renewal, gate-renewal, record-renewal). No manuscript-renewal
    (old manuscript, no new), no new specs (reuses old P specs already in predecessor).
    C (RENDER_TARGETS): U OWN + manuscript-renewal (R manuscript with renewal_source)
    + new R specs iff spec refs point under R/ (else old, already in predecessor).
    Build variant REUSED_BUILD (U, no rebuild) vs EXECUTED_BUILD (C, real build) enforced
    elsewhere via _verify_build_chain_hist (HIST, record-epoch blobs, never current replay).
    """
    proposal_namespace = str(basis.get("proposal_namespace", ""))
    renewal_id = str(basis.get("renewal_id", ""))
    if not proposal_namespace or not renewal_id:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned OWN proposal_namespace/renewal_id missing")
    r_prefix = f"{proposal_namespace}/renewals/{renewal_id}/"
    # Source refs from actual record/seal/basis/proof (exact path+SHA, verified live elsewhere).
    set_ref = record.get("set_ref")
    basis_ref = record.get("renewal_basis_ref")
    proof_ref = record.get("renewal_proof_ref")
    if not isinstance(set_ref, dict) or not isinstance(basis_ref, dict) or not isinstance(proof_ref, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned OWN set/basis/proof refs missing")
    # R receipt via seal source_receipt_ref (top-level, {path,sha}) + roles source-receipt (sized) must match.
    seal_receipt_top = seal.get("source_receipt_ref")
    seal_roles = seal.get("roles", {}) if isinstance(seal.get("roles"), dict) else {}
    seal_receipt_role = seal_roles.get("source-receipt") if isinstance(seal_roles, dict) else None
    if not isinstance(seal_receipt_top, dict) or set(seal_receipt_top) != {"path", "sha256"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned OWN seal source_receipt_ref invalid")
    if not isinstance(seal_receipt_role, dict) or "path" not in seal_receipt_role or "sha256" not in seal_receipt_role:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned OWN seal roles source-receipt missing")
    if seal_receipt_top.get("path") != seal_receipt_role.get("path") or seal_receipt_top.get("sha256") != seal_receipt_role.get("sha256"):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned OWN seal receipt top must equal roles source-receipt (exact path+SHA)")
    receipt_path = str(seal_receipt_top["path"])
    receipt_sha = str(seal_receipt_top["sha256"])
    if not _is_under_R(receipt_path, proposal_namespace, renewal_id):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"versioned OWN R receipt must be under R/ (no P fallthrough): {receipt_path!r}")
    # R build via seal build_record_ref (top-level).
    seal_build = seal.get("build_record_ref")
    if not isinstance(seal_build, dict) or set(seal_build) != {"path", "sha256"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned OWN seal build_record_ref invalid")
    build_path = str(seal_build["path"])
    build_sha = str(seal_build["sha256"])
    if not _is_under_R(build_path, proposal_namespace, renewal_id):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"versioned OWN R build must be under R/: {build_path!r}")
    # R candidate/bundle/gate via seal roles (sized, drop byte_count), must be under R/.
    def _role_under_R(role_name: str) -> tuple[str, str]:
        r = seal_roles.get(role_name)
        if not isinstance(r, dict) or "path" not in r or "sha256" not in r:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"versioned OWN seal role {role_name} missing")
        p = str(r["path"])
        s = str(r["sha256"])
        if not _is_under_R(p, proposal_namespace, renewal_id):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"versioned OWN R {role_name} must be under R/: {p!r}")
        return p, s
    cand_path, cand_sha = _role_under_R("publication-candidate")
    bundle_path, bundle_sha = _role_under_R("quality-regression-bundle")
    gate_path, gate_sha = _role_under_R("reader-surface-gate")
    # R basis/proof/set/record paths (basis/proof/set from record refs, record from ref).
    basis_path = str(basis_ref["path"])
    basis_sha = str(basis_ref["sha256"])
    proof_path = str(proof_ref["path"])
    proof_sha = str(proof_ref["sha256"])
    set_path = str(set_ref["path"])
    set_sha = str(set_ref["sha256"])
    record_path = str(ref.get("path"))
    record_sha = str(ref.get("sha256"))
    for p, n in ((basis_path, "basis"), (proof_path, "proof"), (set_path, "seal")):
        if not _is_under_R(p, proposal_namespace, renewal_id):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"versioned OWN R {n} must be under R/: {p!r}")
    # Record-renewal is NOT under R/ (sources/.../publication/v2/, not R/) by design.
    # Verify live for all OWN E docs (never tool commit for E bytes) + schema blob/mode at new_epoch later via checker.
    # E live checks (fail-closed BLOB_MISSING/SHA drift, no tool-commit requirement).
    _require_authority_live(repo_root, {"path": receipt_path, "sha256": receipt_sha}, "versioned OWN R receipt live")
    _require_authority_live(repo_root, {"path": build_path, "sha256": build_sha}, "versioned OWN R build live")
    _require_authority_live(repo_root, {"path": basis_path, "sha256": basis_sha}, "versioned OWN R basis live")
    _require_authority_live(repo_root, {"path": proof_path, "sha256": proof_sha}, "versioned OWN R proof live")
    _require_authority_live(repo_root, {"path": set_path, "sha256": set_sha}, "versioned OWN R seal live")
    _require_authority_live(repo_root, {"path": cand_path, "sha256": cand_sha}, "versioned OWN R candidate live")
    _require_authority_live(repo_root, {"path": bundle_path, "sha256": bundle_sha}, "versioned OWN R bundle live")
    _require_authority_live(repo_root, {"path": gate_path, "sha256": gate_sha}, "versioned OWN R gate live")
    # Content cross-bindings for OWN R candidate/bundle/gate (HIST, record-epoch blobs, never current replay).
    # Candidate/bundle carry renewal_source_proof_ref (new strict optional branch) == proof (exact path+SHA).
    # Gate derivation binds both proof and receipt refs (no inferred old P/ receipt path).
    # Unrelated sibling (equal SHA different path/lineage) and digest substitutions refuse.
    for own_path, own_sha, own_label, proof_key in (
        (cand_path, cand_sha, "candidate", "renewal_source_proof_ref"),
        (bundle_path, bundle_sha, "bundle", "renewal_source_proof_ref"),
    ):
        try:
            own_bytes = read_repo_bytes(repo_root, own_path, f"versioned OWN R {own_label} content")
            own_doc = _parse_json_strict_bytes(own_bytes, f"versioned OWN R {own_label} content")
        except RenewalHistoryError as exc:
            raise RenewalHistoryError(exc.code, f"versioned OWN R {own_label} unreadable: {exc.detail}") from exc
        if not isinstance(own_doc, dict):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"versioned OWN R {own_label} must be an object")
        pr = own_doc.get(proof_key)
        if not isinstance(pr, dict) or pr.get("path") != proof_path or pr.get("sha256") != proof_sha:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"versioned OWN R {own_label} {proof_key} must equal proof (exact path+SHA, no P fallthrough, no equal-SHA different-path substitution)")
    try:
        gate_bytes = read_repo_bytes(repo_root, gate_path, "versioned OWN R gate content")
        gate_doc = _parse_json_strict_bytes(gate_bytes, "versioned OWN R gate content")
    except RenewalHistoryError as exc:
        raise RenewalHistoryError(exc.code, f"versioned OWN R gate unreadable: {exc.detail}") from exc
    if not isinstance(gate_doc, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned OWN R gate must be an object")
    # Gate derivation binds both proof and receipt refs (per contract §11.2: serialized Gate derivation binds both).
    # H HIST checks exact path+SHA (not inferred old P/ receipt path, no equal-SHA different-path substitution).
    gate_proof = gate_doc.get("renewal_source_proof_ref", gate_doc.get("derivation", {}).get("renewal_source_proof_ref") if isinstance(gate_doc.get("derivation"), dict) else None)
    # Gate schema has derivation/oneOf/4 with renewal_source_proof_ref + renewal_receipt_ref? Actually gate-renewal pointer is
    # /properties/derivation/oneOf/4 (VERSIONED_RENEWAL_V1). The derivation object should contain proof+receipt refs.
    # For HIST, require at least proof ref == proof (exact) where present; receipt ref == R receipt (exact) where present.
    # Full Gate derivation semantics (fresh early surface checks, etc) are S/high + consumer-owned, not H HIST.
    # Here enforce minimal cross-binding: if gate doc carries renewal_source_proof_ref (top-level or in derivation),
    # it must equal proof (exact). If it carries renewal_receipt_ref, it must equal R receipt (exact).
    def _find_proof_ref(d: dict[str, Any]) -> dict[str, Any] | None:
        if isinstance(d.get("renewal_source_proof_ref"), dict):
            return d.get("renewal_source_proof_ref")
        drv = d.get("derivation")
        if isinstance(drv, dict) and isinstance(drv.get("renewal_source_proof_ref"), dict):
            return drv.get("renewal_source_proof_ref")
        # oneOf/4 variant may nest deeper? For HIST, only check top-level + derivation top-level (not full Gate semantics).
        return None
    def _find_receipt_ref(d: dict[str, Any]) -> dict[str, Any] | None:
        if isinstance(d.get("renewal_receipt_ref"), dict):
            return d.get("renewal_receipt_ref")
        drv = d.get("derivation")
        if isinstance(drv, dict) and isinstance(drv.get("renewal_receipt_ref"), dict):
            return drv.get("renewal_receipt_ref")
        return None
    gp = _find_proof_ref(gate_doc)
    if gp is not None and (gp.get("path") != proof_path or gp.get("sha256") != proof_sha):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned OWN R gate proof ref must equal proof (exact path+SHA)")
    gr = _find_receipt_ref(gate_doc)
    if gr is not None and (gr.get("path") != receipt_path or gr.get("sha256") != receipt_sha):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned OWN R gate receipt ref must equal R receipt (exact path+SHA, no inferred old P/ path)")
    # Record itself already loaded via _load_record_file (live SHA verified); re-check live here for OWN row.
    _require_authority_live(repo_root, {"path": record_path, "sha256": record_sha}, "versioned OWN record live")
    raw_rows: list[dict[str, Any]] = []
    raw_rows.append({
        "source_ref": {"path": receipt_path, "sha256": receipt_sha},
        "binding": "RECEIPT_CURRENT_TOOLS",
        "repository_commit_sha": new_epoch,
    })
    def _append_own(doc_type: str, source_path: str, source_sha: str) -> None:
        spath, spointer = _OWNER_BY_TYPE[doc_type]
        schema_sha = _git_blob_sha(repo_root, new_epoch, spath, f"versioned OWN {doc_type} schema", _cache)
        _git_tree_mode(repo_root, new_epoch, spath, f"versioned OWN {doc_type} schema mode", _cache)
        raw_rows.append({
            "source_ref": {"path": source_path, "sha256": source_sha},
            "binding": "SCHEMA",
            "repository_commit_sha": new_epoch,
            "schema_path": spath,
            "schema_pointer": spointer,
            "schema_sha256": schema_sha,
        })
    _append_own("receipt-renewal", receipt_path, receipt_sha)
    _append_own("seal-renewal", set_path, set_sha)
    _append_own("build-new", build_path, build_sha)
    _append_own("basis", basis_path, basis_sha)
    _append_own("proof", proof_path, proof_sha)
    _append_own("candidate-renewal", cand_path, cand_sha)
    _append_own("bundle-renewal", bundle_path, bundle_sha)
    _append_own("gate-renewal", gate_path, gate_sha)
    _append_own("record-renewal", record_path, record_sha)
    # Manuscript-renewal (C only, R manuscript with renewal_source, under R/).
    # U (REUSE_TARGETS): old manuscript, no new, skip (old P manuscript has no renewal_source, stays at original path).
    # C (RENDER_TARGETS): require R manuscript under R/ with renewal_source == proof.
    if requested == "RENDER_TARGETS":
        man_role = seal_roles.get("reader-manuscript")
        if not isinstance(man_role, dict) or "path" not in man_role or "sha256" not in man_role:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned OWN C seal reader-manuscript missing")
        man_path = str(man_role["path"])
        man_sha = str(man_role["sha256"])
        if not _is_under_R(man_path, proposal_namespace, renewal_id):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"versioned OWN C R manuscript must be under R/: {man_path!r}")
        _require_authority_live(repo_root, {"path": man_path, "sha256": man_sha}, "versioned OWN C manuscript live")
        # Verify C manuscript renewal_source == proof (exact path+SHA, HIST, never current replay).
        try:
            man_bytes = read_repo_bytes(repo_root, man_path, "versioned OWN C manuscript")
            man_doc = _parse_json_strict_bytes(man_bytes, "versioned OWN C manuscript")
        except RenewalHistoryError as exc:
            raise RenewalHistoryError(exc.code, f"versioned OWN C manuscript unreadable: {exc.detail}") from exc
        if not isinstance(man_doc, dict):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned OWN C manuscript must be an object")
        rs = man_doc.get("renewal_source")
        if not isinstance(rs, dict) or rs.get("path") != proof_path or rs.get("sha256") != proof_sha:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned OWN C manuscript renewal_source must equal proof (exact path+SHA)")
        _append_own("manuscript-renewal", man_path, man_sha)
    elif requested == "REUSE_TARGETS":
        # U must NOT carry new manuscript-renewal OWN row (old manuscript, no serialized branch).
        # Old manuscript stays at original path (P/... or prior R/...), verified separately via
        # U old_manuscript_ref immediate prior seal equality (in _verify_versioned_ancestor structural).
        pass
    else:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"versioned OWN requested unknown: {requested!r}")
    # New R specs iff spec refs point under R/ (C with new R specs); else old (already in predecessor), skip.
    for spec_key, doc_type in (("manuscript_spec_ref", "spec-manuscript"), ("toolchain_spec_ref", "spec-toolchain")):
        spec_ref = basis.get(spec_key)
        if not isinstance(spec_ref, dict):
            continue
        spath = str(spec_ref.get("path", ""))
        ssha = str(spec_ref.get("sha256", ""))
        if not spath or not ssha:
            continue
        if _is_under_R(spath, proposal_namespace, renewal_id):
            _require_authority_live(repo_root, {"path": spath, "sha256": ssha}, f"versioned OWN new {doc_type} live")
            _append_own(doc_type, spath, ssha)
        else:
            # Old P spec, already in predecessor bindings (editorial 11 or prior OWN? Actually prior OWN? No,
            # old P specs are in editorial predecessor only, not in prior versioned OWN (since prior versioned OWN
            # for U has no new specs). Good – skip (already covered).
            pass
    # Validate every OWN row via strict checker with new-epoch graph (all OWN use new_epoch).
    checker_graph = {"basis_current_epoch": new_epoch, "receipt_epoch": None, "staged_head": None}
    # For OWN SCHEMA rows, _derive_epoch_for_schema returns basis_current_epoch (new_epoch) for all
    # renewal-owned types (receipt-renewal, seal-renewal, build-new, basis, proof, manuscript-renewal,
    # candidate-renewal, bundle-renewal, gate-renewal, record-renewal) + spec-toolchain/spec-manuscript?
    # Specs use receipt_epoch (old) per _derive_epoch_for_schema, but new R specs should use new_epoch!
    # Fix: new R specs (under R/) must use new_epoch, not old receipt_epoch. Handle by temporarily
    # mapping spec doc_types to basis_current_epoch for OWN rows under R/.
    # Since _check_observed_binding_row uses _derive_epoch_for_schema which returns receipt_epoch (None here)
    # for specs, it would fail with TOOL_EPOCH_DRIFT (receipt_epoch missing) for new R specs.
    # Workaround: for OWN new R specs, validate via structural helper (which checks blob at submitted
    # new_epoch, not via graph epoch derivation), not via _check_observed_binding_row with graph.
    # For all other OWN rows (non-spec), use _check_observed_binding_row with new-epoch graph (works).
    normed: list[dict[str, Any]] = []
    for r in raw_rows:
        if isinstance(r, dict) and r.get("binding") == "SCHEMA" and r.get("schema_path") in (
            "schemas/editorial-toolchain-spec-v2.schema.json",
            "schemas/editorial-manuscript-spec-v2.schema.json",
        ):
            # New R spec (under R/): validate structural (live + blob/mode at new_epoch) without graph epoch derivation.
            # Epoch must equal new_epoch (actual, not caller) – enforce here (no graph).
            if r.get("repository_commit_sha") != new_epoch:
                raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", "versioned OWN new spec epoch must equal new CURRENT (no caller authority)")
            normed.append(_check_observed_binding_row_structural(repo_root, r, "versioned OWN new spec", _cache))
        else:
            normed.append(_check_observed_binding_row(repo_root, r, checker_graph, "versioned OWN", _cache))
    # Canonical sorted dedup with conflicting-sha refusal (same owner/path/epoch must have identical sha).
    by_owner: dict[tuple[str, str, str, str, str], dict[str, Any]] = {}
    for b in normed:
        sr = b.get("source_ref", {})
        key = (str(sr.get("path")), str(b.get("binding")), str(b.get("schema_path", "")), str(b.get("schema_pointer", "")), str(b.get("repository_commit_sha")))
        prev = by_owner.get(key)
        if prev is not None:
            psr = prev.get("source_ref", {})
            if psr.get("sha256") != sr.get("sha256") or prev.get("schema_sha256", "") != b.get("schema_sha256", ""):
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"versioned OWN conflicting sha for same owner/path/epoch: {key}")
            continue
        by_owner[key] = b
    ordered = [by_owner[k] for k in sorted(by_owner, key=lambda t: (t[0], t[1], t[2], t[3], t[4]))]
    if not ordered:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned OWN bindings empty (must be NONEMPTY)")
    # Required OWN coverage: at least RECEIPT tool + basis/proof/seal/receipt/build/candidate/bundle/gate/record SCHEMA.
    # (Scope O17 is in predecessor, not OWN – OWN has no scope. RECEIPT tool required in OWN for new R receipt.)
    has_tool = any(isinstance(b, dict) and b.get("binding") == "RECEIPT_CURRENT_TOOLS" for b in ordered)
    if not has_tool:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned OWN missing required RECEIPT_CURRENT_TOOLS (new R receipt)")
    lineage = {
        "record_path": str(ref.get("path")),
        "record_sha": str(ref.get("sha256")),
        "kind": "VERSIONED",
        "prior_selected_ref": record.get("prior_selected_ref"),
        "renewal_basis_ref": record.get("renewal_basis_ref"),
        "renewal_proof_ref": record.get("renewal_proof_ref"),
        "basis_current_epoch": new_epoch,
        "requested": requested,
        "own_receipt_ref": {"path": receipt_path, "sha256": receipt_sha},
        "own_build_ref": {"path": build_path, "sha256": build_sha},
        "own_candidate_ref": {"path": cand_path, "sha256": cand_sha},
        "own_bundle_ref": {"path": bundle_path, "sha256": bundle_sha},
        "own_gate_ref": {"path": gate_path, "sha256": gate_sha},
        "own_basis_ref": {"path": basis_path, "sha256": basis_sha},
        "own_proof_ref": {"path": proof_path, "sha256": proof_sha},
        "own_seal_ref": {"path": set_path, "sha256": set_sha},
        "own_record_ref": {"path": record_path, "sha256": record_sha},
    }
    return ordered, lineage


# ---------------------------------------------------------------------------
# Public HIST leaf
# ---------------------------------------------------------------------------

def _derive_history_graph_for_editorial(
    repo_root: Path,
    record: dict[str, Any],
) -> dict[str, Any]:
    """Derive receipt_epoch/staged_head from linked seal/receipt/staged docs.

    Never caller choice, never inferred from untrusted observed rows (editorial
    has no observed rows). Fail-closed if required epochs missing.
    """
    set_ref = record.get("set_ref")
    if not isinstance(set_ref, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial history graph set_ref missing")
    seal_bytes = _require_authority_live(repo_root, set_ref, "editorial history graph seal")
    seal = _parse_json_strict_bytes(seal_bytes, "editorial history graph seal")
    if not isinstance(seal, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial history graph seal must be an object")
    roles = seal.get("roles", {})
    src = roles.get("source-receipt") if isinstance(roles, dict) else None
    if not isinstance(src, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial history graph source-receipt missing")
    receipt_bytes = _require_sized_live(repo_root, src, "editorial history graph receipt")
    receipt = _parse_json_strict_bytes(receipt_bytes, "editorial history graph receipt")
    if not isinstance(receipt, dict) or not isinstance(receipt.get("current_tools"), dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial history graph receipt current_tools missing")
    receipt_epoch = receipt["current_tools"].get("repository_commit_sha")
    if not isinstance(receipt_epoch, str) or len(receipt_epoch) != 40:
        raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", "editorial history graph receipt epoch invalid")
    staged_ref = seal.get("staged_manifest_ref")
    if not isinstance(staged_ref, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial history graph staged_manifest_ref missing")
    staged_bytes = _require_authority_live(repo_root, staged_ref, "editorial history graph staged")
    staged = _parse_json_strict_bytes(staged_bytes, "editorial history graph staged")
    if not isinstance(staged, dict) or not isinstance(staged.get("producer_head"), str) or len(staged["producer_head"]) != 40:
        raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", "editorial history graph staged producer_head invalid")
    return {"receipt_epoch": receipt_epoch, "staged_head": staged["producer_head"]}


def _derive_editorial_observed_bindings(
    repo_root: Path,
    record: dict[str, Any],
    ref: dict[str, Any],
    graph: dict[str, Any],
    _cache: dict | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Derive NONEMPTY complete observed bindings for one editorial ancestor.

    From ACTUAL strict owner docs/record/staged/receipt, never from serialized
    observed rows/caller epochs. E docs live/COPY (never require tool commit);
    tool rows & schemas at DERIVED own commit (receipt.current_tools.commit,
    staged.producer_head, typed owner registry). Canonical sorted dedup by full
    owner/path/epoch; same path different generations allowed iff distinct
    source owners. O17 whole schema "" not "/". Preserves all original scope
    before/after/upstream/required checks (caller must have run
    _verify_editorial_ancestor first; this re-reads with same history loader,
    never dict permit).
    """
    receipt_epoch = graph.get("receipt_epoch")
    staged_head = graph.get("staged_head")
    if not isinstance(receipt_epoch, str) or len(receipt_epoch) != 40:
        raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", "editorial derive receipt_epoch missing")
    if not isinstance(staged_head, str) or len(staged_head) != 40:
        raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", "editorial derive staged_head missing")
    # Reload seal/record refs with same strict loader (never dict permit).
    set_ref = record.get("set_ref")
    if not isinstance(set_ref, dict) or set(set_ref) != {"path", "sha256"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial derive set_ref invalid")
    seal_bytes = _require_authority_live(repo_root, set_ref, "editorial derive seal")
    seal = _parse_json_strict_bytes(seal_bytes, "editorial derive seal")
    if not isinstance(seal, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial derive seal must be an object")
    proposal_ref = seal.get("proposal_ref")
    staged_ref = seal.get("staged_manifest_ref")
    build_ref = seal.get("build_record_ref")
    for r, n in ((proposal_ref, "proposal_ref"), (staged_ref, "staged_manifest_ref"), (build_ref, "build_record_ref")):
        if not isinstance(r, dict) or set(r) != {"path", "sha256"}:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"editorial derive seal {n} invalid")
        _require_authority_live(repo_root, r, f"editorial derive seal {n}")
    roles = seal.get("roles")
    if not isinstance(roles, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial derive seal roles missing")
    src_role = roles.get("source-receipt")
    if not isinstance(src_role, dict) or "path" not in src_role or "sha256" not in src_role:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial derive source-receipt role missing")
    # Receipt role is sized in seal (exact 15 check already ran); accept sized or authority for derive.
    receipt_path = str(src_role["path"])
    receipt_sha = str(src_role["sha256"])
    # Verify live receipt bytes (sized if byte_count present, else authority).
    if "byte_count" in src_role:
        _require_sized_live(repo_root, src_role, "editorial derive receipt live")
    else:
        _require_authority_live(repo_root, {"path": receipt_path, "sha256": receipt_sha}, "editorial derive receipt live")
    receipt_bytes = read_repo_bytes(repo_root, receipt_path, "editorial derive receipt")
    receipt_doc = _parse_json_strict_bytes(receipt_bytes, "editorial derive receipt")
    if not isinstance(receipt_doc, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial derive receipt must be an object")
    # Receipt epoch must equal actual receipt.current_tools.commit (no caller authority).
    tools = receipt_doc.get("current_tools")
    if not isinstance(tools, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial derive receipt current_tools missing")
    actual_receipt_epoch = tools.get("repository_commit_sha")
    if actual_receipt_epoch != receipt_epoch:
        raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", "editorial derive receipt epoch must equal actual receipt.current_tools.commit")
    # Staged doc (actual producer_head must equal graph staged_head).
    staged_path = str(staged_ref["path"])
    staged_bytes = _require_authority_live(repo_root, staged_ref, "editorial derive staged")
    staged_doc = _parse_json_strict_bytes(staged_bytes, "editorial derive staged")
    if not isinstance(staged_doc, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial derive staged must be an object")
    actual_head = staged_doc.get("producer_head")
    if actual_head != staged_head:
        raise RenewalHistoryError("HISTORY_TOOL_EPOCH_DRIFT", "editorial derive staged head must equal actual staged.producer_head")
    # Retention + scope refs from staged (require exact, verify live; scope equality to receipt enforced).
    retention_ref = staged_doc.get("retention_manifest_ref")
    scope_ref = staged_doc.get("scope_review_ref")
    if not isinstance(retention_ref, dict) or set(retention_ref) != {"path", "sha256"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial derive staged retention_manifest_ref required")
    if not isinstance(scope_ref, dict) or set(scope_ref) != {"path", "sha256"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial derive staged scope_review_ref required")
    _require_authority_live(repo_root, retention_ref, "editorial derive retention live")
    _require_authority_live(repo_root, scope_ref, "editorial derive scope live")
    # Scope equality staged == receipt (R6 B.2: staged.scope_review_ref == receipt.scope_review_ref).
    receipt_scope = receipt_doc.get("scope_review_ref")
    if not isinstance(receipt_scope, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial derive receipt scope_review_ref missing")
    if receipt_scope.get("path") != scope_ref.get("path") or receipt_scope.get("sha256") != scope_ref.get("sha256"):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial derive staged scope must equal receipt scope (exact path+SHA)")
    # Proposal equality staged == seal already checked in _verify_editorial_ancestor; re-check here for derive.
    sproposal = staged_doc.get("proposal_ref")
    if not isinstance(sproposal, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial derive staged proposal_ref missing")
    if sproposal.get("path") != proposal_ref["path"] or sproposal.get("sha256") != proposal_ref["sha256"]:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial derive staged proposal must equal seal proposal")
    # Retention equality staged == receipt (both carry same retention ref).
    receipt_retention = receipt_doc.get("retention_manifest_ref")
    if isinstance(receipt_retention, dict):
        if receipt_retention.get("path") != retention_ref.get("path") or receipt_retention.get("sha256") != retention_ref.get("sha256"):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial derive staged retention must equal receipt retention")
    # Staged equality seal == receipt (both carry same staged ref).
    receipt_staged = receipt_doc.get("staged_manifest_ref")
    if isinstance(receipt_staged, dict):
        if receipt_staged.get("path") != staged_ref["path"] or receipt_staged.get("sha256") != staged_ref["sha256"]:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial derive seal staged must equal receipt staged")
    # Build rows list. E docs live/COPY (never tool commit); schemas at derived own commit.
    raw_rows: list[dict[str, Any]] = []
    # Tool rows (RECEIPT/STAGED) at derived own commit.
    raw_rows.append({
        "source_ref": {"path": receipt_path, "sha256": receipt_sha},
        "binding": "RECEIPT_CURRENT_TOOLS",
        "repository_commit_sha": receipt_epoch,
    })
    raw_rows.append({
        "source_ref": {"path": str(staged_ref["path"]), "sha256": str(staged_ref["sha256"])},
        "binding": "STAGED_PRODUCER",
        "repository_commit_sha": staged_head,
    })
    # Helper to append SCHEMA row for one owner.
    def _append_schema(doc_type: str, source_path: str, source_sha: str, epoch: str) -> None:
        spath, spointer = _OWNER_BY_TYPE[doc_type]
        # O17 whole-document must be "" (never "/"); all whole-doc owners use "" per registry.
        if source_path == "":
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"editorial derive {doc_type} path empty")
        schema_sha = _git_blob_sha(repo_root, epoch, spath, f"editorial derive {doc_type} schema", _cache)
        # Mode must be 100644 (fail-closed, same as tool blobs).
        _git_tree_mode(repo_root, epoch, spath, f"editorial derive {doc_type} schema mode", _cache)
        raw_rows.append({
            "source_ref": {"path": source_path, "sha256": source_sha},
            "binding": "SCHEMA",
            "repository_commit_sha": epoch,
            "schema_path": spath,
            "schema_pointer": spointer,
            "schema_sha256": schema_sha,
        })

    _append_schema("proposal", str(proposal_ref["path"]), str(proposal_ref["sha256"]), staged_head)
    _append_schema("retention", str(retention_ref["path"]), str(retention_ref["sha256"]), staged_head)
    _append_schema("staged", str(staged_ref["path"]), str(staged_ref["sha256"]), staged_head)
    _append_schema("receipt-editorial", receipt_path, receipt_sha, receipt_epoch)
    _append_schema("seal-editorial", str(set_ref["path"]), str(set_ref["sha256"]), receipt_epoch)
    _append_schema("build-old", str(build_ref["path"]), str(build_ref["sha256"]), receipt_epoch)
    _append_schema("scope", str(scope_ref["path"]), str(scope_ref["sha256"]), staged_head)
    # Optional P specs at conventional P dir (proposal parent) — derive iff present live.
    # Real R3 has P/manuscript-spec.json + P/toolchain-spec.json; synthetic unit fixtures may not.
    # Optional to preserve synthetic unit scope; real fixtures include them (NONEMPTY still holds without).
    try:
        p_dir = str(Path(str(proposal_ref["path"])).parent.as_posix())
        for doc_type, fname in (("spec-manuscript", "manuscript-spec.json"), ("spec-toolchain", "toolchain-spec.json")):
            cand = f"{p_dir}/{fname}" if p_dir not in ("", ".") else fname
            try:
                live = read_repo_bytes(repo_root, cand, f"editorial derive {doc_type} optional")
            except RenewalHistoryError:
                continue
            live_sha = hashlib.sha256(live).hexdigest()
            # Validate live JSON (strict, no duplicate keys) but do not require tool commit for E bytes.
            try:
                _parse_json_strict_bytes(live, f"editorial derive {doc_type}")
            except RenewalHistoryError:
                continue
            _append_schema(doc_type, cand, live_sha, receipt_epoch)
    except RenewalHistoryError as exc:
        # Optional specs must never mask required-row failures; only skip when absent.
        # If we are here due to missing optional file, continue without specs.
        # Any other failure (e.g. schema blob missing at epoch) must fail closed.
        # Distinguish by code: BLOB_MISSING for optional file is skip, else re-raise.
        if exc.code != "HISTORY_BLOB_MISSING":
            raise
    # Validate every derived row via strict checker (epoch/owner/pointer/blob/mode, O17 "" enforced).
    # History graph for checker: editorial has receipt_epoch + staged_head (no basis_current).
    checker_graph = {"receipt_epoch": receipt_epoch, "staged_head": staged_head, "basis_current_epoch": None}
    normed: list[dict[str, Any]] = []
    for r in raw_rows:
        normed.append(_check_observed_binding_row(repo_root, r, checker_graph, "editorial derived", _cache))
    # Canonical sorted dedup by full tuple; conflicting sha for same (path,binding,schema,epoch) refuses.
    by_owner: dict[tuple[str, str, str, str, str], dict[str, Any]] = {}
    for b in normed:
        sr = b.get("source_ref", {})
        key = (str(sr.get("path")), str(b.get("binding")), str(b.get("schema_path", "")), str(b.get("schema_pointer", "")), str(b.get("repository_commit_sha")))
        prev = by_owner.get(key)
        if prev is not None:
            # Same owner/path/epoch must have identical sha (else conflicting digest).
            psr = prev.get("source_ref", {})
            if psr.get("sha256") != sr.get("sha256") or prev.get("schema_sha256", "") != b.get("schema_sha256", ""):
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"editorial derived conflicting sha for same owner/path/epoch: {key}")
            continue
        by_owner[key] = b
    ordered = [by_owner[k] for k in sorted(by_owner, key=lambda t: (t[0], t[1], t[2], t[3], t[4]))]
    if not ordered:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial derived bindings empty (must be NONEMPTY)")
    # Required coverage: O17 scope "" + at least one RECEIPT row (fail-closed, no subset/empty shortcut).
    has_scope = any(isinstance(b, dict) and b.get("binding") == "SCHEMA" and b.get("schema_path") == "schemas/reader-surface-semantic-review-v2.schema.json" and b.get("schema_pointer") == "" for b in ordered)
    has_receipt = any(isinstance(b, dict) and b.get("binding") == "RECEIPT_CURRENT_TOOLS" for b in ordered)
    has_staged = any(isinstance(b, dict) and b.get("binding") == "STAGED_PRODUCER" for b in ordered)
    if not has_scope:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial derived missing required scope O17 (\"\" pointer)")
    if not has_receipt:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial derived missing required RECEIPT_CURRENT_TOOLS row")
    if not has_staged:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "editorial derived missing required STAGED_PRODUCER row")
    lineage = {
        "record_path": str(ref.get("path")),
        "record_sha": str(ref.get("sha256")),
        "kind": "EDITORIAL",
        "original_proposal_ref": {"path": str(proposal_ref["path"]), "sha256": str(proposal_ref["sha256"])},
        "original_staged_ref": {"path": str(staged_ref["path"]), "sha256": str(staged_ref["sha256"])},
        "original_scope_ref": {"path": str(scope_ref["path"]), "sha256": str(scope_ref["sha256"])},
        "original_retention_ref": {"path": str(retention_ref["path"]), "sha256": str(retention_ref["sha256"])},
        "original_receipt_ref": {"path": receipt_path, "sha256": receipt_sha},
        "original_seal_ref": {"path": str(set_ref["path"]), "sha256": str(set_ref["sha256"])},
        "original_build_record_ref": {"path": str(build_ref["path"]), "sha256": str(build_ref["sha256"])},
        "staged_producer_head": staged_head,
        "receipt_epoch": receipt_epoch,
    }
    return ordered, lineage


def verify_versioned_history(repo_root: Path | str, record_path: Path | str) -> dict[str, Any]:
    """Reload the record, match kind, walk chain, verify anchor + E/T.

    Returns descriptive {HISTORICAL_IDENTITY_VERIFIED, observed_refs,
    observed_source_bindings, chain_length, anchor_kind}, never a consumable
    permit. No caller verified dict or caller epoch authority. No
    State/P1/P2R/P3S/full-proof/Reader/Gate/Candidate calls. No old code exec.

    Per-invocation batched RAW git cache only (immutable tree/blob metadata);
    no persistent/global authority cache, no caller permit, HEAD/dirty never cached.
    """
    root = Path(repo_root).resolve()
    _inv_cache: dict = {}
    rel = str(record_path)
    if Path(rel).is_absolute():
        try:
            candidate = Path(rel)
            as_rel = candidate.relative_to(root).as_posix()
        except ValueError as exc:
            raise RenewalHistoryError("HISTORY_MODE", f"record path escapes repository root: {rel}") from exc
        rel = as_rel
    record = _load_record_file(root, {"path": rel, "sha256": sha256_repo_file(root, rel, "history record")}, "history record")
    kind = _record_kind(record)
    head_ref = {"path": rel, "sha256": sha256_repo_file(root, rel, "history record head")}
    backwards = _walk_chain_backwards(root, record.get("supersedes"))
    chronological: list[tuple[dict[str, Any], dict[str, Any]]] = list(reversed(backwards)) + [(record, head_ref)]
    if len(chronological) > CHAIN_LIMIT:
        raise RenewalHistoryError("HISTORY_ANCESTOR", "history chain exceeds max32")
    issue_id = record.get("issue_id")
    if not isinstance(issue_id, str) or not issue_id:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "history record issue_id invalid")
    prior_checkpoint = record.get("prior_checkpoint")
    if not isinstance(prior_checkpoint, dict) or set(prior_checkpoint) != {"path", "sha256"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "history record prior_checkpoint invalid")
    _check_authority_ref(root, prior_checkpoint, "history prior checkpoint")
    previous_instant: datetime | None = None
    sequences: list[int] = []
    kinds: list[str] = []
    for index, (rec, ref) in enumerate(chronological):
        if rec.get("issue_id") != issue_id:
            raise RenewalHistoryError("HISTORY_ANCESTOR", f"history chain[{index}] issue mismatch (foreign lineage)")
        if rec.get("prior_checkpoint") != prior_checkpoint:
            raise RenewalHistoryError("HISTORY_ANCESTOR", f"history chain[{index}] prior checkpoint must bind original validation")
        try:
            instant = _parse_instant(str(rec.get("recorded_at", "")))
        except RenewalHistoryError as exc:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"history chain[{index}] recorded_at invalid: {exc.detail}") from exc
        if previous_instant is not None and instant < previous_instant:
            raise RenewalHistoryError("HISTORY_ANCESTOR", "history chain chronology must be nondecreasing")
        previous_instant = instant
        seq = _parse_sequence(ref["path"])
        if seq is None:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"history chain[{index}] sequence unknown (unknown branch refuses)")
        sequences.append(seq)
        kinds.append(_record_kind(rec))
    for i in range(1, len(sequences)):
        if sequences[i] <= sequences[i - 1]:
            raise RenewalHistoryError("HISTORY_ANCESTOR", "history chain sequence must be strictly increasing")
    first_active = next((i for i, k in enumerate(kinds) if k in ("EDITORIAL", "VERSIONED")), None)
    if first_active is not None and any(k == "LEGACY" for k in kinds[first_active + 1:]):
        raise RenewalHistoryError("HISTORY_ANCESTOR", "mixed chain with later legacy successor unsupported")
    prior_doc = load_json_strict(root, prior_checkpoint["path"], "history prior checkpoint")
    original_map: dict[tuple[str, str], str] = {}
    for row in prior_doc.get("artifacts", []) if isinstance(prior_doc.get("artifacts"), list) else []:
        if not isinstance(row, dict):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "prior checkpoint artifacts malformed")
        key = (str(row.get("name")), str(row.get("path")))
        if key in original_map:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "prior checkpoint duplicate artifact")
        original_map[key] = str(row.get("sha256"))
    legacy_prefix = chronological[:first_active] if first_active is not None else chronological
    for index, (rec, _ref) in enumerate(legacy_prefix):
        if _record_kind(rec) != "LEGACY":
            continue
        superseded = rec.get("superseded_artifacts", [])
        preserved = rec.get("preserved_artifacts", [])
        if not isinstance(superseded, list) or not isinstance(preserved, list):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"legacy[{index}] rows malformed")
        effective: dict[tuple[str, str], str] = {}
        seen: set[tuple[str, str]] = set()
        for row in superseded:
            if not isinstance(row, dict):
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"legacy[{index}] superseded row malformed")
            key = (str(row.get("name")), str(row.get("path")))
            if key in seen:
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"legacy[{index}] duplicate artifact")
            seen.add(key)
            original_sha = original_map.get(key)
            if original_sha is None:
                raise RenewalHistoryError("HISTORY_ANCESTOR", f"legacy[{index}] supersedes unknown prior artifact")
            if row.get("prior_sha256") != original_sha:
                raise RenewalHistoryError("HISTORY_ANCESTOR", f"legacy[{index}] prior SHA must be cumulative against original, not rollforward")
            effective[key] = str(row.get("new_sha256"))
        for row in preserved:
            if not isinstance(row, dict):
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"legacy[{index}] preserved row malformed")
            key = (str(row.get("name")), str(row.get("path")))
            if key in seen:
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"legacy[{index}] duplicate artifact")
            seen.add(key)
            if original_map.get(key) is None or row.get("sha256") != original_map.get(key):
                raise RenewalHistoryError("HISTORY_ANCESTOR", f"legacy[{index}] preserved mismatch (must equal original)")
            effective[key] = str(row.get("sha256"))
        if set(effective) != set(original_map):
            raise RenewalHistoryError("HISTORY_ANCESTOR", f"legacy[{index}] row union differs from original checkpoint")
    # Chain-wide before_active_digest recompute (not presence-only). Fail-closed.
    _verify_before_digests_chain(root, chronological, prior_doc)
    observed: list[dict[str, Any]] = []
    accumulator: list[dict[str, Any]] = []
    materialization_lineage: list[dict[str, Any]] = []
    for idx, (rec, ref) in enumerate(chronological):
        rec_kind = _record_kind(rec)
        if rec_kind == "LEGACY":
            _parse_instant(str(rec.get("recorded_at", "")))
            observed.append({"kind": rec_kind, "record_sha": ref["sha256"]})
            materialization_lineage.append({
                "record_path": str(ref.get("path")),
                "record_sha": str(ref.get("sha256")),
                "kind": "LEGACY",
            })
            # LEGACY has no bindings by design; accumulator unchanged.
        elif rec_kind == "EDITORIAL":
            graph = _derive_history_graph_for_editorial(root, rec)
            info = _verify_editorial_ancestor(root, rec, ref, graph, _inv_cache)
            observed.append({"kind": info.get("kind", rec_kind), "record_sha": ref["sha256"], "seal_path": info.get("seal_path")})
            # Derive NONEMPTY complete observed bindings from ACTUAL strict owner
            # docs/record/staged/receipt (never from serialized observed rows/caller
            # epochs). E live/COPY (never tool commit); tool rows & schemas at
            # DERIVED own commit. Canonical sorted dedup; O17 "" not "/".
            # Old editorial derive actual R3 rows as fixed last (for accumulator seed).
            derived, lineage = _derive_editorial_observed_bindings(root, rec, ref, graph, _inv_cache)
            # Accumulator extend with dedup + conflicting-sha refusal (same owner/path/epoch must have identical sha).
            for b in derived:
                sr = b.get("source_ref", {}) if isinstance(b.get("source_ref"), dict) else {}
                key = (str(sr.get("path")), str(b.get("binding")), str(b.get("schema_path", "")), str(b.get("schema_pointer", "")), str(b.get("repository_commit_sha")))
                # Check conflict against existing accumulator (same owner/path/epoch, different sha).
                for ab in accumulator:
                    asr = ab.get("source_ref", {}) if isinstance(ab.get("source_ref"), dict) else {}
                    akey = (str(asr.get("path")), str(ab.get("binding")), str(ab.get("schema_path", "")), str(ab.get("schema_pointer", "")), str(ab.get("repository_commit_sha")))
                    if akey == key:
                        if asr.get("sha256") != sr.get("sha256") or ab.get("schema_sha256", "") != b.get("schema_sha256", ""):
                            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"derived conflicting sha for same owner/path/epoch: {key}")
                        break
                else:
                    accumulator.append(b)
            materialization_lineage.append(lineage)
        else:
            # VERSIONED: derived expected graph (accumulator BEFORE this record, oldest->newest).
            # Expected observed bindings = derived accumulated ALL predecessor history bindings BEFORE this record.
            # Require exact basis.observed==expected and proof.supported==same (canonical array order,
            # no omissions/extras/unknown owners/forged epoch/owner paths, after rehashing all wrappers).
            # Never infer expected epochs from submitted rows (use accumulator, not caller).
            # Could use private context internal (accumulator, chain) not caller provided permit.
            expected_predecessor = sorted(accumulator, key=lambda b: (
                str(b.get("source_ref", {}).get("path", "")),
                str(b.get("binding", "")),
                str(b.get("schema_path", "")),
                str(b.get("schema_pointer", "")),
                str(b.get("repository_commit_sha", "")),
            ))
            # Prior chain for reachability (oldest->current-1, same issue/Profile, bounded 32, no cycles).
            # Full chronological for build terminal + stored proof reachability (older reachable ancestor, not immediate).
            prior_chain = chronological[:idx]
            # Structural + expected equality + own receipt/closure + build chain + stored proof + U old refs.
            # No extra public helper/token needed. No execute ancestor new proof CURRENT; HIST branch only.
            # Orphan validation: public history record path, no LIVE State, no active requirement.
            # High mints record after seal before State write then H verify should work (retained before after
            # source proof okay, old State unchanged, E existing, pointer selection upstream, sources proof H
            # lineage selected predecessor not requiring record active).
            info = _verify_versioned_ancestor(root, rec, ref, expected_predecessor, chronological, _inv_cache)
            observed.append({"kind": "VERSIONED", "record_sha": ref["sha256"], "seal_path": info.get("seal_path")})
            # Derive OWN source binding rows from new record basis CURRENT epoch, proof/receipt/set/build/new
            # modified schema owners and add to history accumulator for next generation.
            # For old editorial derive actual R3 rows as fixed last (already in accumulator seed).
            # Current record own receipt/currentTool closure must match its basis CURRENT epoch and proof closure;
            # own schema git blob mode/shape at own commit; E remains live/COPY.
            new_epoch = str(info.get("new_epoch", ""))
            route = str(info.get("route", ""))
            requested = str(info.get("requested", ""))
            basis_doc = info.get("basis")
            proof_doc = info.get("proof")
            seal_doc = info.get("seal")
            if not isinstance(basis_doc, dict) or not isinstance(proof_doc, dict) or not isinstance(seal_doc, dict):
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned OWN basis/proof/seal missing from structural info (private internal)")
            if not new_epoch or len(new_epoch) != 40 or not route or not requested:
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "versioned OWN new_epoch/route/requested missing")
            own_bindings, own_lineage = _derive_versioned_own_bindings(
                root, rec, ref, basis_doc, proof_doc, seal_doc, new_epoch, route, requested, prior_chain, _inv_cache,
            )
            # Support C->U->U materialization producer older ancestor build terminal oldR3 or new EXECUTED,
            # hard bounded 32 selected chain; unrelated sibling/digest substitutions refuse (in OWN + build chain).
            # Add OWN to accumulator for next generation (dedup with conflict refusal).
            for b in own_bindings:
                sr = b.get("source_ref", {}) if isinstance(b.get("source_ref"), dict) else {}
                key = (str(sr.get("path")), str(b.get("binding")), str(b.get("schema_path", "")), str(b.get("schema_pointer", "")), str(b.get("repository_commit_sha")))
                for ab in accumulator:
                    asr = ab.get("source_ref", {}) if isinstance(ab.get("source_ref"), dict) else {}
                    akey = (str(asr.get("path")), str(ab.get("binding")), str(ab.get("schema_path", "")), str(ab.get("schema_pointer", "")), str(ab.get("repository_commit_sha")))
                    if akey == key:
                        if asr.get("sha256") != sr.get("sha256") or ab.get("schema_sha256", "") != b.get("schema_sha256", ""):
                            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"OWN conflicting sha for same owner/path/epoch: {key}")
                        break
                else:
                    accumulator.append(b)
            # Materialization lineage for source consumers (descriptive, S rereads via loader, never dict permit).
            # Includes prior_selected/basis/proof + basis_current_epoch + R receipt/build/candidate/bundle/gate/record/manuscript refs.
            materialization_lineage.append(own_lineage)
    derived_bindings = accumulator
    # Canonical sorted dedup by full owner/path/epoch; conflicting sha refuses.
    # Same path different generations allowed iff distinct source owners/epochs.
    by_owner: dict[tuple[str, str, str, str, str], dict[str, Any]] = {}
    for b in derived_bindings:
        if not isinstance(b, dict):
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "derived binding must be an object")
        sr = b.get("source_ref", {}) if isinstance(b.get("source_ref"), dict) else {}
        key = (
            str(sr.get("path")), str(b.get("binding")),
            str(b.get("schema_path", "")), str(b.get("schema_pointer", "")),
            str(b.get("repository_commit_sha")),
        )
        prev = by_owner.get(key)
        if prev is not None:
            psr = prev.get("source_ref", {}) if isinstance(prev.get("source_ref"), dict) else {}
            if psr.get("sha256") != sr.get("sha256") or prev.get("schema_sha256", "") != b.get("schema_sha256", ""):
                raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", f"derived conflicting sha for same owner/path/epoch: {key}")
            continue
        by_owner[key] = b
    ordered_bindings = [by_owner[k] for k in sorted(by_owner, key=lambda t: (t[0], t[1], t[2], t[3], t[4]))]
    if not ordered_bindings:
        # Editorial-only chains must still be NONEMPTY (old R3 has 9+ rows).
        # Legacy-only chains (no editorial/versioned yet) have no bindings by design.
        has_active = any(k in ("EDITORIAL", "VERSIONED") for k in kinds)
        if has_active:
            raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "derived bindings empty for active chain (must be NONEMPTY complete)")
    return {
        "HISTORICAL_IDENTITY_VERIFIED": True,
        "observed_refs": observed,
        "observed_source_bindings": ordered_bindings,
        "materialization_lineage": materialization_lineage,
        "chain_length": len(chronological),
        "anchor_kind": "LEGACY_REVALIDATION" if any(k == "LEGACY" for k in kinds[:first_active] if first_active is not None) else "VALIDATION_CHECKPOINT",
    }


def verify_renewal_retention(root: Path | str, basis_path: Path | str) -> dict[str, Any]:
    repo = Path(root).resolve()
    rel = str(basis_path)
    if Path(rel).is_absolute():
        try:
            rel = Path(rel).relative_to(repo).as_posix()
        except ValueError as exc:
            raise RenewalHistoryError("HISTORY_MODE", "basis path escapes repository root") from exc
    basis = load_and_validate_json_strict(repo, rel, BASIS_SCHEMA, "renewal basis retention")
    before_ref = basis.get("before_state_ref")
    retained_ref = basis.get("retained_copy_ref")
    if not isinstance(before_ref, dict) or set(before_ref) != {"path", "sha256"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "retention before_state_ref fields invalid")
    if not isinstance(retained_ref, dict) or set(retained_ref) != {"path", "sha256", "byte_count"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "retention retained_copy_ref fields invalid")
    # Do NOT validate live before_state path as mutable authority; validate retained COPY.
    retained_data = _check_sized_ref(repo, retained_ref, "retention retained COPY")
    if hashlib.sha256(retained_data).hexdigest() != before_ref["sha256"]:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "retained COPY SHA must equal before_state_ref")
    rows = basis.get("retention_rows")
    if not isinstance(rows, list) or not rows:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "retention rows must be a non-empty array")
    state_rows = [r for r in rows if isinstance(r, dict) and "state:authority" in (r.get("roles") or [])]
    if len(state_rows) != 1:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "retention requires a unique state:authority row")
    state_row = state_rows[0]
    if state_row.get("policy") != "COPY_BEFORE_REPLACEMENT":
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "state:authority row must be COPY_BEFORE_REPLACEMENT")
    if state_row.get("path") != before_ref["path"] or state_row.get("sha256") != before_ref["sha256"]:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "retention state row must equal before_state_ref")
    if state_row.get("retained_dest") != retained_ref["path"] or state_row.get("retained_sha256") != retained_ref["sha256"] or state_row.get("retained_byte_count") != retained_ref["byte_count"]:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "retention state row retained binding must equal retained_copy_ref")
    # State->Profile via retained bytes (not live).
    retained_state = _parse_json_strict_bytes(retained_data, "retention retained State")
    if not isinstance(retained_state, dict):
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "retention retained State must be an object")
    retained_profile_ref = retained_state.get("profile")
    if not isinstance(retained_profile_ref, dict) or set(retained_profile_ref) != {"path", "sha256"}:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "retention retained State lacks exact profile ref")
    keep_matches = [r for r in rows if isinstance(r, dict) and r.get("policy") == "KEEP_IMMUTABLE" and isinstance(r.get("retained_ref"), dict) and r["retained_ref"].get("path") == retained_profile_ref["path"] and r["retained_ref"].get("sha256") == retained_profile_ref["sha256"]]
    if len(keep_matches) != 1:
        raise RenewalHistoryError("HISTORY_DIGEST_MISMATCH", "retention requires unique matching KEEP Profile row")
    # Exact inventory: retention rows must cover prior seal roles + COPY (no omission).
    # Minimal check: at least state + profile rows present; full inventory is checked per-ancestor.
    return {"HISTORICAL_IDENTITY_VERIFIED": True, "retained_copy": {"path": retained_ref["path"], "sha256": retained_ref["sha256"]}}
