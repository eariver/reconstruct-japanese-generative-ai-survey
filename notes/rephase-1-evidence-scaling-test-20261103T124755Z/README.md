# Evidence scaling TEST dispatch — fixed snapshot runs (no PASS claimed)

Fixed source snapshot (independent DB, no sharing, inert origin):
`.rephase-1-editorial-runtime/evidence-scaling-fixed-20261103T124755Z/candidate-work/`
(771 files), HEAD `a7245948…`, `origin https://example.invalid/evidence-scaling-fixed-20261103T124755Z.git`,
no `objects/info/alternates`. Pins (before/after every batch, unchanged):
Evidence `dfc5e27f…`/156966B, runner `c9b7c70b…`/45501B, LOW `0974c709…`/218692B —
author §9 quiescent pins. Test module `1c95f675…` (attempt 3; synced exact to
the author workcopy after green runs). Old workcopies/rehearsal untouched; no
normal commit/network/readback/Production. Runtime owners paused during runs;
TEST-only edits (fixture/oracle faults, no runtime edits, no
authority mocks/stubs, no weakening).

## Batches (exclusive raw subprocess stdout/stderr + argv/env/cwd/PID/times/exit/timeout + pre/post pins)

- `test-runs/batch-00-diagnostic/` — Raw read-site diagnostic (not a test):
  per-Raw reads during PUBLIC accept+readback = 12, sites: basis validation
  ×4 (`validate_evidence_package_basis:1242` re-validates the supplement),
  accept resolve ×1, accept 2×finish ×2 rechecks, readback resolve ×1,
  check-boundary recheck ×1, pre-RETURN recheck ×1. Grounded the slope bound.
- `test-runs/batch-01-golden/` — focused positive first: golden test only.
  1/1 ok (0.18s, PID 3398792). Common setup green → dependents ran.
- `test-runs/batch-02-full16-reattempt3/` — full 16 (attempt pin `1c95f675`).
  15/16 pass (5.5s, PID 3415160); the single failure is the readback-RETURN
  freshness gap below (genuine runtime finding, fixture correct).
- `test-runs/batch-03-affected/` — selected affected regressions, 14/14 ok
  (2.2s, PID 3417180): old Evidence binds-exact (positive) +
  rejects-drop-unknown (negative); runner module 8/8; Profile DM016
  `test_03` + `test_04`; DM022 LOW `test_low_typed_loader_dispatch` +
  `test_raw_binding_refuses_unbound_claim`. No whole-suite decoration.
- Earlier `batch-02-full16` (attempt pin `a02a38b8`) is preserved history:
  8/16 (6 test-oracle/fixture faults of mine + 2 runtime-shape findings);
  all mine repaired in attempt 3 except the returned runtime gap.

## Results (new module, attempt 3)

PASS (15): golden baseline+full validation; unit private-vs-public slices
(+old-vs-new count, labelled unit); N/M slope constancy (per-Raw equal across
scales) within grounded bound ≤16 (measured exactly 12); repo_root=None
3 cases; lazy error-order zero-Raw-IO; standalone Raw change; standalone
manifest change; two healthy ops new digests + both readbacks; late Raw drift;
late task mutation (+control); post-validation reseal; Evidence/Views partial
window; history no-LIVE; LOW DERIVED COPY/R!=E + direct supplemented bulk
(cards cite exact supp authority, PUBLIC validator `== []`, accept payloads
bind SHAs) + HIGH adopt/readback/checker `[]`; LOW typed refusals.
FAIL (1, runtime): `test_readback_result_mutation_after_check_before_return_refuses_exact`
— `ValueError not raised`. Fixture correct (real hook calls the original
checker, same-size planted drift, inventory before restore). Root cause:
`validate_evidence_acceptance` pre-RETURN rechecks pins (acceptance/package/
State) + supplement ctx but never re-pins/rechecks the accepted task/result
files after `_check_..._with_context` returns; a result mutated in that
window is not refused. Returned to Root + runtime owner (no rubber-stamp).

## Gaps / notes

- HIGH producer limitation (author §9, recorded not worked around): HIGH
  `build_revision_package_from_paths` carries no `authority_supplement` and
  the HIGH request builder sets `supplement_manifest: None` with no
  `source_bindings`; supplemented LOW proof runs through the direct LOWER
  public bulk APIs on an actually-supplemented package copy (mirror of the
  existing producer contract fields), not through HIGH.
- Finding4 untouched (LOW `evidence_acceptance_sha256` stays the planned
  `core.json_bytes` file hash; HIGH writes + validates the exact bytes).
- `tests/__pycache__` empty in snapshot (all runs `PYTHONDONTWRITEBYTECODE=1`);
  the one prior `py_compile` pyc (`test_evidence_scaling_v2.cpython-314.pyc`,
  74116B/`88880545…`) was mine, recorded and removed narrowly — history, no
  source cleaning beyond it.
- No real409 (Root + independent review gate first, then W34 409).
