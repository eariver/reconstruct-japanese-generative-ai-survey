# F5 readback-RETURN fix — TEST dispatch (fresh snapshot, exact scope)

Fixed snapshot (NEW, old failed snapshot/logs untouched):
`.rephase-1-editorial-runtime/evidence-scaling-fixed-20261103T170019Z/candidate-work/`
(771 files / 805 entries), independent DB HEAD `4d13640a…` —
`SYNTHETIC FIXTURE-ONLY execution snapshot commit, NOT an ordinary
candidate/reconstruct commit` (independent DB, inert origin, no
ancestry/shared objects). Qualification: this isolated synthetic commit is
the mechanism that gives the snapshot an independent Git DB; it is not
ordinary shipping history. Author workcopy ordinary HEAD `409b292…` unchanged;
no Production/network/Git-readback/rehearsal changes.

Exact bytes (before/after every batch, unchanged): Evidence `48742538…`/158943B
(F5 fix), runner `c9b7c70b…`/45501B, LOW `0974c709…`/218692B, tests
`1c95f675…`. Full 771-file/sha/mode manifests per attempt (`manifest-pre.json` /
`manifest-post.json`): MATCH in all 3 batches; snapshot tree clean (`git
status` 0) after each; no `__pycache__` created under the snapshot (all runs
`PYTHONDONTWRITEBYTECODE=1`).

## Batches (exclusive raw stdout/stderr + argv/env/cwd/PID/wall-times/exit/timeout + full manifests)

- `test-runs/batch-01-f5only/` — exact failed F5 test only:
  `test_readback_result_mutation_after_check_before_return_refuses_exact`.
  EXIT 0, 1/1 ok, 0.3s, PID 3450059. Positive → dependents ran.
- `test-runs/batch-02-full16/` — full new module (16 methods). EXIT 0,
  16/16 ok, 5.5s. Same-process bindings: Evidence `48742538…`, runner
  `c9b7c70b…`, LOW `0974c709…`, tests `1c95f675…`. Valid task/meta/card zero
  errors; supplemented LOW lowerAPI case green (honest HIGH-carry limitation
  stands); Path.read_bytes Raw counter: per-Raw exactly 12.0 both scales ≤ 16.
- `test-runs/batch-03-dm022readback/` — single dependency-justified existing
  test (changed readback paths): `test_c_direct_weekly_prepare_adopt_readback`
  (prepare→adopt→readback→checker). EXIT 0, 1/1 ok, 2.1s, PID 3453513.
  The 14 unchanged affected methods were NOT re-run (no decoration).
- `test-runs/batch-00-diagnostic/` is the PRIOR dispatch's read-site
  diagnostic (kept in the old packet, not re-run).

## Coverage notes for the Root real409 gate

- Evidence readback-RETURN freshness: covered (F5 test green).
- Views readback-RETURN pins (author §10 "analogous"): NO dedicated test, new
  or existing — no test in the tree calls `validate_edition_views_acceptance`
  / history Views-content readback. The change is the same pin-return pattern
  as Evidence (author-reviewed §10); Root decides whether a Views-RETURN
  freshness test is required before real409.
- One benign `ResourceWarning` (implicit TemporaryDirectory cleanup) appears in
  the LOW test's stderr; the test passes with all real validations — helper
  temp owned by a non-running instance, no fixture loss, no coverage impact.
- Prior `py_compile` pyc recorded narrowly as history; no source cleaning.
