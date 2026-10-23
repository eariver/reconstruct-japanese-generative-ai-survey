# Worker B Weekly REPEAT — concrete code blocker (no source edits)

**Status: BLOCKED before second-correction capture. Truthful unfinished, no writer-helper completion.**

- Source snapshot (readonly, no clean/reset): `/tmp/opencode/jgas-editorial-r2v-20261021T084804Z/candidate-partial-b40de60`
  HEAD `4ff2d8562502db36223332c45c9cc5d01bb93156`, tree `4a0c5343937151af0c0ad4522177441acd0e8fcc`, `git ls-files` 717.
  After this unit: HEAD/tree/ls-files unchanged, 717 hash compare 0 mismatches (see stdout). New `scripts/__pycache__` residue grew in both SRC (pre-existing Birth 17:57 + 18:03 additions from this interpreter) and DST; untracked only, no tracked mutation. No source clean per instruction — residue preserved, not deleted.
- New independent copy: `/tmp/opencode/jgas-editorial-wk2-verify-20261021T090000Z/candidate-partial-b40de60` via `cp -a` (no hardlinks, inodes differ, link count 1, no alternates, remote empty/inert). Same HEAD/tree, 717 set equal, 717 SHA vs recorded `snapshot-manifest.json` 0 mismatches.
- Healthy confirm in copy (no PDF rebuild): receipt/Gate/Candidate `READY_FOR_PUBLICATION_PREVIEW`, `ALREADY_ACTIVE` read-only, selection `VERSIONED_ACTIVE` wk-smoke-1. Elapsed: receipt 5.978s, Gate 0.266s, Candidate 0.669s, ALREADY_ACTIVE 14.543s. See `stdout.txt`/`stderr.txt`/`exit.txt` (exit 2 due to blocker, not healthy failure).
- Second correction `wk-smoke-2` (new headline `Weekly tested method — Second Editorial Correction`, new semantic paragraph, new id) blocked at `P1.prepare_proposal` on active before:

```
ProposalError: VERSIONED_ROW_SHAPE: versioned row fields invalid (expected path/sha256/byte_count/origin): reader-manuscript
  at survey_editorial_correction_proposal_v2.py:478 in _active_effective
  called from _pipeline_data:1517 via prepare_proposal:1984
```

  Minimal proof:
  - L `survey_publication_set_v2.resolve_publication_selection` documents and returns `canonical7/effective7` rows as exactly `{path,sha256,origin}` (3 keys, see docstring line 1431 and constructors `_canonical7_from_validation:1414`, editorial `active7` at `1561-1562`).
  - P1 `survey_editorial_correction_proposal_v2._active_effective:478` requires versioned `effective7` rows as exactly `{path,sha256,byte_count,origin}` (4 keys) and raises `VERSIONED_ROW_SHAPE` otherwise.
  - Observed `effective7` in this copy (via `resolve_publication_selection`) carries 3-key rows, e.g. `reader-manuscript: {path,sha256,origin: ACTIVE}`, no `byte_count`. Hence every repeat pre-Preview correction after activation fails before any writes.
  - First correction succeeded only because State was CANONICAL (record None path, no versioned branch) — repeat path untested until now.

- Root fix central only (no worker edit per NO SOURCE EDITS):
  - Either L adds `byte_count` to `effective7`/`canonical7` (file length, checked against live bytes) and updates docstring/callers, or P1 accepts 3-key rows and validates `byte_count` via live file length (as it already does for `col.pinned` + `len(col.files[rel])` check). Must be single central decision, with updated `CURRENT_CLOSURE`/P3S/interface assertions and repeat-correction regression. Do not patch locally in worker copy.
  - Prior `wk-smoke-1` publication/staged/proposal/seal/Candidate KEEP verified (13 files, hashes unchanged before blocker). Current State COPY unchanged (`VALIDATED_DRAFT` r1, sha `4bab695d...` before, still r1 after). No canonical Candidate/source/QA mutation (no new record, no State replace). Old `r1` remains valid historic (not re-verified after blocker due to early exit, but untouched).

- Not run due to blocker (truthfully unfinished, no skip without record):
  - `P2R capture → scope → P2V → P3S → PUBLIC REAL TL2026 prepare → reviews/QA → finalize → activate` for `wk-smoke-2`.
  - Normal lifecycle `VALIDATED_DRAFT→RELEASE_CANDIDATE→synthetic Preview→profiled Freeze→FROZEN→offline Release→RELEASED` on second active set.
  - Orchestrator/handoff/human-gate expected-Candidate + wrong-old rejection, export workflow offline predicate, stable canonical Freeze/Manifest checks.
  - Wrong-old-Candidate negative copy (NEW copy not created; DST holds only `wk-smoke-2/authoring-input.json` partial, no State mutation).
  - Final real PDF/text/PNG + stage/State/records/rolemap hashes.

- Tooling: type fixtures synthetic, placeholder quality NO-GO maintained. No old saved harness run. No network. No candidate/reconstruct commit.

**Next:** General/lead fixes L/P1 interface centrally, then Worker B reruns this exact script (new timestamp, new independent copy) for repeat + lifecycle + consumers + negative + artifacts.
