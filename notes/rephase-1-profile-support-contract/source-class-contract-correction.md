# DM016 source-class contract CORRECTION (supersedes R1 applicability errors, preserves original)

2026-10-30. DESIGN/SOURCE-READ ONLY. R1 `source-class-applicability.md/json`
NOT selected — preserved unchanged. This correction fixes source errors found by
ROOT + Explore. No runtime/import/tests/build/fixtures/network/Git/Human readback.
Read-only source: final133 proof `/tmp/opencode/jgas-dm022-indep-20261029T235900Z/proof-candidate`
(patch `25b48878…`, manifest `31fa4a72…`); snapshots by read + hash, no imports.

## 1. R1 errors corrected (rootable)

1. **Runner map is dead, not Weekly admission.**
   `run_evidence_v2_interactive.py:49-56` defines 6 UPPER keys
   (`PRIMARY_OFFICIAL/PAPER/REPOSITORY,SOCIAL,SECONDARY_INVESTOR_ACCOUNT,SECONDARY`);
   `_source_class:110-114` exists. Call-site proof of non-use: `grep` over that
   file returns exactly 3 hits (49,110,111) — zero invocations in-file; sole
   importer `run_evidence_v2_agent_first.py:28,80-99` monkey-patches only
   `discovery.validate_acceptance` + `_build_completeness`, never `_source_class`.
   Live card path `_build_card:321` + task inventory `:666` both call canonical
   `evidence.task_authority_sources` (`survey_evidence_v2.py:413-446`), never the
   runner helper. R1's "runner6 maps Weekly4" is false: 6 literals contain no
   lowercase Weekly `source_type`; it is a class→class identity + 1 alias, not
   source admission.
2. **Legacy 4-enum path is NOT v2.** `schemas/screening-record.schema.json:12`,
   `schemas/evidence-task.schema.json:25` (4-enum `paper,github-release,
   official-feed-item,official-index-snapshot`) + `scripts/build_screening_index.py`,
   `build_evidence_tasks.py`, `build_candidate_matrix.py:171-172`,
   `validate_evidence_run.py` are the legacy v1 interactive path
   (`prepare_screening_run`, `prepare_evidence_run`, `merge/accept`,
   `apply_special_selection` import them; zero v2 imports). The v2 path uses:
   `survey_discovery_v2.py` + `survey_screening_v2.py:171-173` (open non-empty
   string, no enum) + `discovery-acceptance-v2.schema.json` (acceptedRecord has
   NO `source_type`, only `source_locator/raw_refs`) + `screening-v2-run-package/
   batch-result` (no `source_type`) + `evidence-v2-run-package/task` schemas
   (`evidence-v2-task.schema.json:13-14` `source_records: object[]`, open) +
   `survey_evidence_v2.py:prepare_evidence_package:601-621`
   (`source_records=[discovery source]`, open passthrough). DO NOT extend legacy
   schemas to fix v2.
3. **Views `build_candidate_matrix` is legacy.** Same separation as above; v2
   Ledger/Views derive from `survey_evidence_v2.py:1663-1910`
   (`task_authority_sources`, `build_research_card_content`,
   `build_research_view_content`, `build_materiality_ledger`), not the legacy counter.
4. **SUPPLEMENT `SOCIAL` omission is not auto-added.** `evidence-authority-
   supplement-v2.schema.json:60-61` (`source_type` open, `source_class` 4-enum
   without `SOCIAL`) vs `evidence-v2-card.schema.json:85` (5 with `SOCIAL`).
   Normal Discovery SOCIAL is allowed upstream; supplement is an OPTIONAL
   post-Screening exact-manifest path. Omission may be deliberate policy. No
   automatic add in this unit.
5. **No new module / URL guess / ledger / second authority.** Rejected:
   `run_special_interactive_evidence.py:41-47` locator-sniff, edition projection
   ledger, permanent translation table. Preserve original type labels.

## 2. Rootable proposed mapping (provenance only, NOT claim truth)

`source_class` = resource provenance. `evidence_class` (`PRIMARY_FACT/
VENDOR_CLAIM/...`) + `verification.targets` = claim strength. Shared map never
proves claim truth. Only `PRIMARY_DOC` blocked directly in TS-001; other 9 are
known edition vocab coverage (67/160 audit), not individually executed — do not
claim all10 used.

| EXACT literal (preserve) | Proposed class | Semantic justification + precondition |
|---|---|---|
| `PRIMARY_DOC` | `PRIMARY_OFFICIAL` | First-party official document (release notes/changelog/docs family: canonical siblings `first_party_product_docs/changelog :91-92` → OFFICIAL). Precondition: publisher-controlled doc + raw + locator. Directly observed block. |
| `PRIMARY_REPO` | `PRIMARY_REPOSITORY` | Version-controlled code host (siblings `first_party_repository :93`, `official_project_repo :63` → REPOSITORY). Precondition: repo host + rev-pinned raw. |
| `PRIMARY_ANNOUNCEMENT` | `PRIMARY_OFFICIAL` | First-party announcement channel (siblings `:96,100` → OFFICIAL). Precondition: owner-published locator. |
| `PRIMARY_MODEL_CARD` | `PRIMARY_OFFICIAL` | Owner-published model card (first-party doc, not peer review). Precondition: card publisher == model owner; mirror/fork fails closed. |
| `PRIMARY_SPEC` | `PRIMARY_OFFICIAL` | Normative spec from issuing authority (cf `government_security_*`, `official_conference_paper :105-108`). Precondition: issuing authority identity. |
| `SECONDARY_REFERENCE` | `SECONDARY` | Citing/reference work, not primary source. Precondition: none beyond valid raw. |
| `SECONDARY_TECHNICAL` | `SECONDARY` | Third-party technical analysis. Same. |
| `RUNTIME_RECIPE` | `SECONDARY` (AMBIGUOUS, default) | Build/run instructions of unclear publisher. Admit as `PRIMARY_REPOSITORY` ONLY with oracle: official-repo path + rev pin + byte-identical raw; else `SECONDARY`. Needs genuine oracle before any PRIMARY use. |
| `PACKAGING_DOCS` | `PRIMARY_OFFICIAL` iff owner-published else `SECONDARY` (AMBIGUOUS) | Packaging instructions. Precondition: publisher == package owner + raw. Default `SECONDARY` until proven. |
| `RUNTIME_PR` | `SECONDARY` (NEVER PRIMARY) | Unmerged proposal, not merged proof. A primary runtime PR is NOT first-party proof of model weights/behavior; at most secondary signal pending merge + independent verification target. `PRIMARY_*` for a PR is refused. |

No per-literal provenance/collector invented: actual Thematic records not captured
in this workspace (only literals in deferred captures). Each PRIMARY admission
requires a representative genuine oracle (collector + raw_refs + published/
accessed instants + publisher identity + claim binding) at contract time; until
then the literal stays fail-closed.

## 3. Route DM016 coverage (v2 only) + active caller lineage

Discovery(open `survey-discovery-record:51`, `survey_screening_v2:171`) →
Screening v2 (no enum) → `prepare_evidence_package:601-621` (open `source_records`)
→ `task_authority_sources:413-446` (`_source_class:177-184` + canonical
`SOURCE_CLASS_MAP:44-109`) → `build_research_card_content:1663-1690`
(canonical authority, DM022-extracted pure helper) → `validate_evidence_card:
965-1055` → Views/Ledger (`1782-,1910-`) → reader. Normal interactive
`_build_card:321` + `survey_research_authority_v2:1511-1536`
(`build_research_card_content` + `validate_evidence_card/validate_edition_view`)
+ `prearchitecture_acceptance_v2:682` all reuse the SAME canonical helper.
Dead runner map removal = delegate private helper to canonical OR delete with no
runtime-authority claim (dead code, zero call sites above).

## 4. Minimal footprint + compatibility (no 3-schema edit)

- Touch ONLY: `scripts/survey_evidence_v2.py:44-109,177-184` (admit listed
  literals per §2) + `scripts/run_evidence_v2_interactive.py:49-56,110-114`
  (delegate/remove dead map). No new runtime module (dependency cost).
- No legacy schema edits, no supplement `SOCIAL` add, no URL mapping, no ledger.
- Compatibility: ALL old mappings unchanged; new admission applies to new
  sources only; accepted historic Evidence/Views/Ledger bytes never rewritten.
- Exact code/closure/own-schema pre-code map MUST precede impl; no
  "`closures unchanged`" hand-wave.

## 5. Mandatory selection questions (ROOT)

1. Approve §2 class per literal, esp. ambiguous `RUNTIME_RECIPE/PACKAGING_DOCS`
   default-`SECONDARY` + `RUNTIME_PR`-never-`PRIMARY` rule?
2. Which literals are necessary genuine product scope vs explicitly unsupported?
3. Supplement `SOCIAL` omission: deliberate policy (keep) or separate defect?
4. Dead-map disposition: delegate vs delete; owner + fingerprint update?
5. Required genuine oracle per PRIMARY literal + pre-code code/closure/schema map —
   who owns, what closes it before any impl?
