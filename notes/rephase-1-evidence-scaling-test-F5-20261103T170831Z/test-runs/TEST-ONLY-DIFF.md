# TEST-only diff for later composite (new snapshot vs 1c95f675)

Base: `tests/test_evidence_scaling_v2.py` at `1c95f675…` (16 methods; archived at
`notes/rephase-1-evidence-scaling-repair/test-archive-1c95f675-20261103T170500Z/`,
also pinned in F5 snapshot commit `4d13640a…` and author workcopy — untouched).
This snapshot's workcopy file: `d486809c…` (+205/−5 lines, TEST-ONLY, uncommitted).

Additive (no existing test/method altered except one docstring line):
- module helper `_inventory_rel_dirs(root, rels)` — full SHA/mode/type/dir
  inventory over several repo-relative dirs (reuses `_sha_file`).
- method helper `_make_evidence_views_chain(...)` — valid accepted Evidence +
  Views chain (PUBLIC builder + FULL PUBLIC validators + accept APIs).
- `test_live_views_return_view_mutation_after_check_before_return_refuses_exact`
  — LIVE `validate_edition_views_acceptance` RETURN freshness.
- `test_history_views_content_view_mutation_after_check_before_return_refuses_exact`
  — history `_validate_edition_views_acceptance_content` RETURN freshness with
  `verify_state_basis` must-not-call.
- docstring line on the Evidence readback test updated (F5 landed; was
  "in-progress").

Runtime files: ZERO changes (Evidence `48742538…`, runner `c9b7c70b…`, LOW
`0974c709…` identical). Later composite: apply this exact test file over the
real409 clone's `1c95f675` + same three runtime bytes; no other file differs.
