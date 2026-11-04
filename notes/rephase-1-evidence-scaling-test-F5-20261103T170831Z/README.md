# F5 + Views-RETURN dispatch — fresh snapshots, focused scope (no decoration)

Fixed snapshot (NEW, old snapshots/logs untouched):
`.rephase-1-editorial-runtime/evidence-scaling-fixed-20261103T170831Z/candidate-work/`
(771 files / 805 entries), independent DB HEAD `a6f73314…` —
`SYNTHETIC FIXTURE-ONLY execution snapshot commit, NOT an ordinary
candidate/reconstruct commit` (independent DB, inert origin, no ancestry/shared
objects). Author workcopy ordinary HEAD `409b292…` untouched; old test `1c95f675`
archived at `notes/rephase-1-evidence-scaling-repair/test-archive-1c95f675-20261103T170500Z/`.
No network/Git-readback/Production/rehearsal changes; no runtime edits (owner paused).

Bytes (before/after every batch, unchanged): Evidence `48742538…`/158943B,
runner `c9b7c70b…`, LOW `0974c709…`; test module `d486809c…` (= `1c95f675` +
TEST-only Views additions, uncommitted workcopy delta, documented in
`test-runs/TEST-ONLY-DIFF.md` for later composite onto the real409 clone).
Full 771-file/sha/mode manifests MATCH pre/post every batch; snapshot tree
otherwise clean; no `__pycache__` (all runs `PYTHONDONTWRITEBYTECODE=1`).

## Batches (exclusive raw stdout/stderr + argv/env/cwd/PID/wall-times/exit/timeout + full manifests)

- `test-runs/batch-01-f5only/` — exact previously-failed F5 test only.
  EXIT 0, 1/1 ok, 0.3s, PID 3450059.
- `test-runs/batch-02-full16/` — full 16 (unchanged from F5 dispatch).
  EXIT 0, 16/16 ok, 5.5s.
- `test-runs/batch-03-dm022readback/` — single dependency-justified existing
  test (`test_c_direct_weekly_prepare_adopt_readback`: prepare→adopt→readback→checker).
  EXIT 0, 1/1 ok, 2.1s, PID 3453513.
- `test-runs/batch-04-viewsreturn/` — the 2 NEW Views-RETURN tests.
  EXIT 0, 2/2 ok, 0.9s, PID 3482136. Same-process LOADED bindings incl. the
  helper test module (`test_survey_evidence_v2.py` `ed0155cd…`); valid
  task/meta/card zero errors; hooked REAL `_check_views_acceptance_rows_content`
  (original called, then same-size accepted-view drift); exact
  `Accepted Edition View <task_id> bytes changed` at OUTER RETURN in both
  routes; history route under `verify_state_basis` must-not-call; full
  inventories pre-restore; restored bytes read back clean.

## Scope for the Root real409 gate

Green: 1 + 16 + 1 + 2 across 4 focused batches (no full-suite rerun, no
16-repeat beyond the F5 dispatch — new tests are additive and the 2 failures
there were fixture bugs, not runtime). Views-RETURN now has direct LIVE +
history regression coverage; the F5 Evidence analog stays green. TEST-only
diff recorded for composite; real409 clone (old `1c95` + same three runtime
bytes) was not touched and no real run was started.
