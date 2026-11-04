# TEST-only diff for later composite (vs 1c95f675)

Base `1c95f675…` (16 tests, archived at
`notes/rephase-1-evidence-scaling-repair/test-archive-1c95f675-20261103T170500Z/`,
also pinned in F5 snapshot commit `4d13640a…` and untouched in the author
workcopy). This snapshot's workcopy file: `1b48169a…` (+1 test method, +1
fixture helper, +1 inventory use; no existing-test edits, no runtime edits).

Additive:
- helper `_make_candidates_normalized_state(...)` — CAND fixture: real
  Discovery acceptance (A2 `_materialize_production_discovery_acceptance`) +
  discovery/screening checkpoint records + reports (same required shapes) +
  CANDIDATES_NORMALIZED State, agent facade asserted `[]`, derived
  next_action/terminal_reason. No evidence checkpoint, no EVIDENCE_REVIEWED.
- `test_runner_epoch_advance_executes_new_finish_callbacks_inside_facade` —
  PUBLIC `run()` with State-init A and actual artifact-only HEAD B
  (single unrelated probe file; State/Profile/checkpoints byte-identical;
  CLEARLY labelled artifact-only, not a repair epoch). Full outputs +
  facade-mediated readbacks + old init SHA still A + READY. Old-c9
  expectation recorded source-based only (no old-runtime execution, not faked):
  bare pre-accept `_finish` owner → `validate_evidence_package_basis` →
  bare `core.verify_state_basis` compares A vs B and raises
  `implementation commit differs...rebase required` before the first copy.
- run-2 fix inside the same test: post-run readbacks wrapped in
  `agent_tool.current_stage_basis_override()` (the runner's own calling
  convention; bare standalone readback with mismatched epoch correctly
  refuses — verified in attempt 1 raw, exit 1, `ValueError` at
  `survey_production_v2.py:984`).
