# LF-2I correction evidence qualification

2026-10-10. Correction implementation Co-Worker closeout (not independent review).

## Source identity
- Design copy `/tmp/opencode/jgas-lf2-design-20261009T113013Z` on unchanged
  HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`,
  tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`,
  parent `34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4`.
- Final overlay 2M+7A with modes 664 (see `hash-manifest.json` + runner EXPECTED):
  - M `scripts/survey_reader_surface_gate_v2.py` `e73058…bbe4` (Longform canonical suffix check)
  - M `schemas/reader-surface-gate-v2.schema.json` `fe4a96…13322c` (unchanged since first return)
  - A `schemas/longform-publication-source-manifest-v2.schema.json` `4dadf8…3e8ca`
  - A `schemas/longform-reader-input-v2.schema.json` `7bae9d…d0643` (LF-1 unchanged)
  - A `scripts/survey_longform_derivation_v2.py` `c09c55…41149` (strict raw-first _safe)
  - A `scripts/survey_longform_generated_v2.py` `d480e1…97d3c2` (strict paths, heading syntax, canonical replay)
  - A `scripts/survey_longform_semantic_publication_v2.py` `1020e4…d90e7` (two-pass split, pre-mkdir preflight, snapshots, retained partial)
  - A `tests/test_survey_longform_derivation_v2.py` `ce6874…f913` (LF-1 unchanged)
  - A `tests/test_survey_longform_publication_integration_v2.py` `16864f…92e7`
    (5 new methods + extended matrix; 11 integration total).
- No candidate/reconstruct commits/branches; no original/LF1/verify-copy mutation;
  no network/Production actions/subagents; no DM021 reason or EXCEPTION_* path.
- `config/survey-production-v2.json` unchanged per `config-note.md` mechanism
  (closure + control-roots pinning, no new authority).

## Preservation
- `initial-9/` + `initial-9-manifest.json` + `initial-2M.patch` +
  `initial-complete.patch` preserve the exact first-return nine files/modes/hashes
  BEFORE edits (old 191-line overlay.patch omitted 7A; now complete).
- `lf2i-dev1.log` (`ab676d…6547`) + `lf2i-dev2.log` (`080891…5eef`) preserved.
- `attempt1-env-failure/` preserves the correction-runner setup failure
  (child `PYTHONNOUSERSITE=1` hid `pypdf`; fixed to minimal forced env,
  reran green). Old artifacts/caches were not deleted blindly.
- New runner `run_lf2i_correction.py` is a new tool, not an old-script rerun.

## Verification (R8 runner)
- `run.log`: 44 tests (11 LF-2I integration + schema/contract/Gate/LF-1 affected)
  all PASS in 1462.728s, exit 0, Python 3.14.4, exclusive logs, timeout-retained
  output, direct returncodes, forced `PYTHONDONTWRITEBYTECODE=1` +
  `GIT_TERMINAL_PROMPT=0`, Git/Python routing overrides rejected.
- `manifest.json`: pre/post identity PASS (HEAD/tree/parent + all 9 hashes/modes +
  status 2M+7A, cache side effects listed separately, not claimed untouched),
  disposable pre-drift/child-fail/post-drift proofs PASS on temp copies only
  (no real-candidate canary).
- `apply.log` + `complete-overlay.patch` + `hash-manifest.json`: independent
  byte-copy of HEAD blobs for 2M + `git apply --check/apply` exit 0 +
  7A byte/mode compare with zero mismatches. Partial DB required no `git archive`.
- Old 6+33/guard claims remain historical/retracted, not new PASS.

## Scope / stops
- Same selected-path budget only (new helper/publisher/receipt schema; LF-1 loader
  split; Gate runtime/schema; integration test; config only-if-actual-needed —
  not needed). No new dispatcher/reason-taxonomy/fidelity-schema/Production changes.
- Healthy normal FROZEN/RELEASED readback proved at final source (existing test
  retained). No DM021 shortcut, no regeneration owner, no build transfer claim.
- Whole NOT_READY, step4/B3 OPEN, canonical audit unstarted (unless root proves
  otherwise). Stop for root code/oracle/evidence review + fresh independent review.
  No automatic next unit, no Commit/Push. If limit reached, partial state is
  preserved exactly (not claimed complete) — here complete.
