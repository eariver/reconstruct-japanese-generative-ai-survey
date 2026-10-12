# Attempt 01 analysis (exit=1: 4 failures + 4 errors of 32; source freeze identical pre/post)

All 27 affected gate-control tests passed. All 5 new P1 tests failed on ONE
root cause in `scripts/survey_editorial_correction_proposal_v2.py`
`_active_effective` no-record branch: the full original checkpoint row
(`{name,path,sha256}`) was passed to `Collector.pinned()`, which requires an
exact `{path,sha256}` record → `REF_SHAPE: active-before artifact
publication-pdf is not an exact {path,sha256} record` (first row order).
Matrix sub-cases (alias/traversal/noncanonical) failed consequently: active
resolution precedes authoring-path handling, so their codes were never reached.
No fixture, graph, scope, or predecessor logic was exercised yet.

Fix (candidate source, uncommitted): extract `{path,sha256}` before pinning in
that branch. Rerun authorized as new attempt-02 with exclusive outputs;
attempt-01 logs/scripts/freeze preserved unmodified.
