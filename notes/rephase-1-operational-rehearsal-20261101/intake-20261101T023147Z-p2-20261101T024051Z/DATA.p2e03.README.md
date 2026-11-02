# Edition-local Evidence source-class projection (CV2-DM-016 workaround)

Status: `WORKAROUND_VALIDATED` (edition-local). Shared Core remains frozen;
CV2-DM-016 stays `OPEN_CORE / EDITION_WORKAROUND`. This directory never states
`CORE_FIXED`.

## Problem

Frozen Core accepts an open Discovery `source_type` vocabulary through
Discovery/Screening, but `survey_evidence_v2._source_class` fail-closes on 10
Thematic types (67/160 non-DROP tasks). Full record:
`execution/defects/shared-core-evidence-source-map-gap-20260922.md`.

## Principle (Human-authorized)

`EDITION_LOCAL / DETERMINISTIC / REPRODUCIBLE / FAIL_CLOSED / FROZEN_CORE_VALIDATED`

- Frozen Core creates the normal Evidence package/tasks from canonical bytes.
- This adapter derives a **compatibility copy**: the ONLY permitted semantic
  difference is `source_records[*].source_type`, projected per the reviewed
  map below (provenance-class projection, not a correction of Discovery).
- Canonical Discovery/Screening bytes are never rewritten; no Screening
  disposition changes; no Core module modified, no runtime monkey-patching by
  this adapter, no Core script copied/edited here, no validator weakened.
- The derived package passes through the **unchanged** frozen validators and
  acceptance functions. A package that only works with a patched validator is
  prohibited (and impossible here: validators are imported, not copied).
- Frozen override contexts (`current_stage_basis_override`) are entered at
  exactly the same call sites as the frozen runner, for their designed
  purpose only (historical pre-advance State-SHA tolerance for accepted
  packages; all other basis checks rerun; source-class fail-closed untouched).

## Projection map (reviewed, §5 of the execution brief)

| Canonical `source_type` | Compatibility `source_type` | Rule |
|---|---|---|
| PRIMARY_DOC | PRIMARY_OFFICIAL | CV2DM016-MAP:… |
| PRIMARY_REPO | PRIMARY_REPOSITORY | CV2DM016-MAP:… |
| PRIMARY_ANNOUNCEMENT | PRIMARY_OFFICIAL | CV2DM016-MAP:… |
| PRIMARY_MODEL_CARD | PRIMARY_OFFICIAL | CV2DM016-MAP:… |
| PRIMARY_SPEC | PRIMARY_OFFICIAL | CV2DM016-MAP:… |
| SECONDARY_REFERENCE | SECONDARY | CV2DM016-MAP:… |
| SECONDARY_TECHNICAL | SECONDARY | CV2DM016-MAP:… |
| RUNTIME_RECIPE | PRIMARY_OFFICIAL | CV2DM016-MAP:… |
| PACKAGING_DOCS | PRIMARY_OFFICIAL | CV2DM016-MAP:… |
| RUNTIME_PR | PRIMARY_REPOSITORY | CV2DM016-MAP:… |

Counts on current canonical bytes: 67 projected / 93 passthrough / 160 tasks
(recomputed by the builder; unexpected vocabulary fail-closes).

## Files

- `build_supplement_r1.py` — builds the frozen-validated Evidence Authority
  Supplement r1 (13 corrected/additional post-Screening sources with immutable
  Raw under `external/evidence-supplement/raw/`) via frozen
  `build_evidence_authority_supplement`. Manifest SHA recorded in the session
  record; Raw bytes covered by the manifest.
- `build_compat_evidence_package.py` — normal package (frozen, temp) →
  projection with per-task §7 invariant checks → persisted `compat-package/`
  → frozen `validate_evidence_package_basis` (must PASS).
- `reproducibility_test.py` — builds twice in clean temp dirs; requires
  identical task bytes/hashes, package bytes/hash, ledger semantics.
  Result: `COMPATIBILITY_REPRODUCIBILITY: PASS`.
- `run_frozen_evidence_chain.py` — replicates the frozen
  `run_evidence_v2_interactive.run()` call sequence with the compat package
  substituted; all judgment steps are frozen Core functions (see file
  docstring for the exact list).
- `compat-package/` — persisted derived package (package.json + tasks/).
- `projection-ledger.json` — per-task original/projected types + task SHAs +
  locators + rule IDs (160 rows).
- `task-targets.json` — per-task verification targets dumped from the
  Core-built normal package (input contract for r2 authorship).
- `validation-report.md` — frozen validation outcomes + identity audit.

## Resume / re-execution

1. `build_supplement_r1.py` refuses overwrite (delete + rebuild only
   deliberately; manifest SHA would change and invalidate downstream pins).
2. `build_compat_evidence_package.py` refuses overwrite; reproducibility via
   `reproducibility_test.py` (temp dirs).
3. `run_frozen_evidence_chain.py` refuses to overwrite ledger/completeness;
   acceptance dirs are content-addressed (re-run with identical inputs
   revalidates and returns existing acceptance).
