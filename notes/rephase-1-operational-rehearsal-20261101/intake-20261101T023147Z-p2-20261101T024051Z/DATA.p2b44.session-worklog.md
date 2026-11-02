# W34 Issue #491 Repair & Fresh Publication Preview — Execution Worklog

Execution agent: Gemini 3.8 Flash (inheriting from Muse Spark 1.3)
Date: 2026-09-13 JST
Starting W34: `6f68fd09...` (canonical Human Publication Preview REQUEST_CHANGES r2 recorded; Issue #491)

## 1. Context & Authority Integration

- Inherited workspace in `weekly/2026-W34-v2-work` preserved via git stash `31cf92c4...`.
- Reviewed Core PR #492 (main@`74708eb2`) integrated via non-fast-forward merge commit `8df4c638...`.
- Stash applied cleanly with zero conflicts; working tree reconciled.

## 2. Issue #491 Defect Repairs

### Defect 1: Reader-Facing Claim Boundary Normalization
- Target: `surveys/weekly/2026-W34/sections/20-agent-workflows.tex` line 18 tail.
- Removed internal pipeline leakage: `regional processing is NOT part of this package after Selection r2; it belongs to Package 4`.
- Replaced with canonical reader-facing prose: `Regional processing is outside the scope of this section and is discussed with deployment and model-distribution conditions`.
- Contextual scan across all 10 TeX sources confirmed 0 improper leaks of internal pipeline terms.

### Defect 2: Bibliography Retrieval Access Provenance Reconciled
- Applied Core #492 `scripts/survey_bibliography_access_provenance_v2.py` against active accepted Evidence (`647cde46...` / `8437905d...`).
- All 41 citations resolved: 41 MATCH, 0 MISMATCH, 0 AMBIGUOUS, 0 MISSING.
- Expected canonical access date for all 41 entries: `2026-09-08` (superseding blanket `2026-08-21` weekly cutoff).
- Regenerated `surveys/weekly/2026-W34/references.bib` byte-identical to Core #492 output.
- Dedicated `w34-event-c066` chronology proof recorded:
  - Event date: 2026-08-21 (DailyX X observation 2026-08-21T17:29:36Z)
  - Page dateline: 2026-08-26 (post-event edited page per Evidence limitation-1)
  - Actual capture date: 2026-09-08T14:52:53Z
  - Proof: `2026-08-21 != 2026-08-26 != 2026-09-08`; BibTeX strictly uses capture date `2026-09-08`.
- Full audit table documented in `sources/2026-W34/execution/luna/w34-human-preview-r2-issue491-repair/bibliography-provenance-audit-r2.md`.
- Shared Core note recorded in `sources/2026-W34/execution/defects/w34-issue491-bibliography-urldate-core-note-20260913.md`.

## 3. Fresh PDF Build & Exact Verification

- Authoring commit `07c4b6a7...` pushed to `origin/weekly/2026-W34-v2-work`.
- CI build: GitHub Actions workflow `build-weekly-survey.yml` run `34762344518` completed in 3m45s (conclusion: `success`, TeX log gate: `PASS`).
- Materialized `surveys/weekly/2026-W34/main.pdf`:
  - SHA-256: `e93db71a5be8249d65d66c5f3b0284875447d953eeadf3b66ca23a9318bd06de`
  - Byte count: 338,722 bytes
  - Page count: 12 pages (unencrypted)
  - Supersedes prior reviewed PDF `1818e8669963a0d965966b6d2f4a0ef4cc8df2bdf9ed129c64fa96be7c28ed84` (338,707 bytes).
- Text layer verification:
  - Section 20 claim boundary renders: `Regional processing is outside the scope of this section and is discussed with deployment and model-distribution conditions`.
  - Zero occurrences of `Selection r2` or `Package 4`.
  - Exactly 41 occurrences of `visited on 09/08/2026` across bibliography pages (pages 10-12).
  - Zero occurrences of `08/21/2026` in bibliography.

## 4. Downstream Publication Authority Regeneration

- `sources/2026-W34/publication/v2/reader-manuscript-v2.json`:
  - Updated supporting file digests for `20-agent-workflows.tex` and `references.bib`.
  - Recomputed `manifest_sha256 = "c453bea798f6d7693d2e92d1dbae3fc7838b24d90df382c2547f3ad033b7c10e"`.
  - Validated with `survey_reader_publication_v2.validate_manuscript_manifest` -> PASS.
- `sources/2026-W34/publication/v2/deterministic/pdf-preflight.json`:
  - Bound fresh PDF SHA-256 `e93db71a...`, 338,722 bytes, 12 pages, CI run `34762344518`.
- `sources/2026-W34/publication/v2/quality-regression-bundle-v2.json`:
  - Bound fresh PDF and `pdf-preflight.json`.
  - Recomputed `bundle_sha256 = "e1bd647975f6d8676a12a5e8b842bcd4fdb7d0cbf4c82d1f08ab572cd9012ef6"`.
  - Validated with `survey_quality_v2.validate_bundle` -> PASS.
- `sources/2026-W34/publication/v2/semantic-editorial-review-v2.json`:
  - Bound fresh manuscript and PDF; updated checks for boundary normalization and Core #492 bibliography dates.
  - Recomputed `review_sha256 = "4d852488ff111e8c0868ca60c73967e953e52aaa7aea1f96e3a8e76e5dc5f2ec"`.
  - Validated with `survey_reader_publication_v2.validate_review_record(SEMANTIC_EDITORIAL)` -> PASS.
- `sources/2026-W34/publication/v2/visual-review-v2.json`:
  - Bound fresh manuscript and PDF; verified exact rendered layout and text layer.
  - Recomputed `review_sha256 = "692321069f001c966a008e490cddb7cac4dbb559b7b35ece7b4ca4adc6f66edb"`.
  - Validated with `survey_reader_publication_v2.validate_review_record(VISUAL)` -> PASS.
- `DRAFT_COMPLETE -> VALIDATED_DRAFT`:
  - Deterministic stage contract validation report written to `sources/2026-W34/execution/luna/w34-human-preview-r2-issue491-repair/validation/reader-publication-stage-validation-r4.json`.
  - Advanced via `survey_agent_control_v2 advance-stage`; checkpoint created at `sources/2026-W34/orchestration/v2/checkpoints/DRAFT_COMPLETE.json`.
- `sources/2026-W34/publication/v2/publication-candidate-v2.json`:
  - Bound fresh manuscript, source, PDF, quality bundle, semantic review, visual review.
  - Recomputed `candidate_sha256 = "52c8d0bcc85140a2727d1867a908d7077d40c7088a7c1e83f10b66044c50f3ba"`.
  - Validated with `survey_publication_v2.validate_candidate` -> PASS.
- `VALIDATED_DRAFT -> RELEASE_CANDIDATE`:
  - Deterministic candidate validation report written to `sources/2026-W34/execution/luna/w34-human-preview-r2-issue491-repair/validation/publication-candidate-stage-validation-r4.json`.
  - Advanced via `survey_agent_control_v2 advance-stage`; checkpoint created at `sources/2026-W34/orchestration/v2/checkpoints/VALIDATED_DRAFT.json`.

## 5. End State & Human Gate Readiness

- `production-state.json`:
  - `lifecycle_state`: `RELEASE_CANDIDATE`
  - `next_action`: `PUBLICATION_PREVIEW`
  - `terminal_reason`: `HUMAN_GATE_REACHED`
  - `human_gates.publication_preview`: `pending`
  - `human_gate_provenance.publication_preview`: `null`
  - `machine_checkpoints.validation`: `passed`
  - `machine_checkpoints.publication_preview`: `pending`
  - `publication_revalidation_provenance`: `null`
  - State validation (`agent.validate_agent_state`): PASS (0 errors).
- Clean separation maintained: Issue #491 left open for Human review; no artificial Human approval generated; no freeze or release attempted.

Markers:
`W34_ISSUE_491_REPAIRED_FRESH_PUBLICATION_PREVIEW_READY_FOR_HUMAN_REVIEW`
