# Runner-epoch facade dispatch — single new test, fresh snapshot

Fixed snapshot (NEW, old snapshots/logs untouched):
`.rephase-1-editorial-runtime/evidence-scaling-fixed-20261103T172903Z/candidate-work/`
(771 files / 805 entries), independent DB HEAD `4555c301…` —
`SYNTHETIC FIXTURE-ONLY execution snapshot commit, NOT an ordinary
candidate/reconstruct commit` (independent DB, inert origin, no ancestry/shared
objects). Author workcopy `1c95f675` + ordinary HEAD untouched; no network/
Git-readback/Production/rehearsal changes; no runtime edits (owner paused);
real409 clone untouched.

Bytes (before/after every batch, unchanged except the TEST-only workcopy file):
Evidence `48742538…`/158943B, runner `5e195730…`/45833B (F5 fix), LOW
`0974c709…`/218692B; tests `1b48169a…` (= `1c95f675` + ONE runner test +
helpers; `TEST-ONLY-DIFF.md` recorded for later composite). Full 771-file/sha/
mode manifests MATCH pre/post every batch; snapshot tree otherwise clean
(single `M tests/test_evidence_scaling_v2.py`); no `__pycache__` (all runs
`PYTHONDONTWRITEBYTECODE=1`).

## Batches (exclusive raw stdout/stderr + argv/env/cwd/PID/wall-times/exit/timeout + full manifests + same-process LOADED bindings)

- `test-runs/batch-01-runner-epoch/` — the new test, attempt 1. EXIT 1:
  PUBLIC `run()` COMPLETED (all new finish callbacks passed under the facade;
  outputs written), then the test's own post-run standalone readback (bare,
  outside any facade) correctly refused with `implementation commit
  differs...rebase required` (`survey_production_v2.py:984`). Fixture/oracle
  fault of mine, not a runtime bug: readbacks must use the runner's own
  facade-mediated calling convention.
- `test-runs/batch-01b-runner-epoch-retry/` — same test, facade-mediated
  readbacks. EXIT 0, 1/1 ok, 1.8s, PID 3535980.

No full-16 rerun (additive single test; no shared-helper changes — new code
only touches the new method + its own CAND helper; failure was a test-oracle
fix, not runtime). No old-version run executed (source-based c9 expectation
recorded in the test docstring, explicitly not faked).
