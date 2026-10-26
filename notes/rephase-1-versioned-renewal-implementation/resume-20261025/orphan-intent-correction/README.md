# Orphan intent-collision correction — AUTHOR HIGH (no CommitPoint)

2026-10-25. AUTHOR HIGH correctness repair, ROOT failure/resume disposition
in `../astra-integration-corrections.md` appended § (Failure/resume oracle
correction). Whole unit ongoing, NOT READY, no Human CommitPoint, no
independent PASS.

OWN ONLY: `scripts/survey_versioned_renewal_v2.py` (HIGH `9a0469ef…` →
`b12439d5…`, +167 lines narrow fail-closed matching-intent detection) +
NEW `tests/test_versioned_renewal_orphan_intent_20261025.py` (`4b5a9d7e…`).
No H/S/PUB/P1/edpub/P3S/schema edits. P3S runtime fix `9e2a0ad…` (existing,
741-file base) preserved, not re-edited.

Candidate base: actual409/tree8ce + current writable
`versioned-renewal-env-20261023T185000Z/candidate-work` (HEAD `409b292`,
39M + 52U intended incl. new test, 741 files). Fault-worker raw
`../failure-resume-verification/raw/` original defect preserved, never
overwritten; this packet uses NEW unique `orphan-intent-correction/` only.

Layout:
- `make_own_snapshot_20261025.py` — byte-independent complete SOURCE
  snapshot (own 741, no `-l`, manifest-exact, no cache, isolation, pins).
- `make_fixture_20261025.py` — NEW independent fixture DB (721 ancestry,
  fixed own SOURCE-only commit before authority, old E uncommitted).
- `healthy_u1_20261025.py` — NEW healthy SEALED_U (`or1-weekly`) via public
  prepare/finalize (real PDF/reviews reuse from `wk-boot-1`, no activation).
- `fault_orphan_20261025.py` — OS fault (`os.replace` once) after record
  complete before State switch yields orphan; ordinary SAME then changed
  reason/time both refuse (INTENT_COLLISION, no new r3/State change);
  explicit resume r2→RESUMED + strict current State/set/history; repeated
  resume ALREADY_ACTIVE readonly; unrelated new set allocates; malformed/
  foreign/symlink refuses preserves, no unowned delete. Guards record/State
  counts/inventory immediately before repair. Only OS seam, no validator
  mocks.
- `manifest.json` — source IDs, pins, counts.
- `raw/` — per-phase UTC dirs (`own-snap-…`, `fixture-…`, `healthy-…`,
  `orphan-…`), each with `commands.log`, `pid.txt`, `stdout/stderr/exit`,
  byte-independent forks, no hardlinks/alternates, no inherited GIT_*,
  fresh Python 3.14.4 + `PYTHONDONTWRITEBYTECODE=1`, workspace TMPDIR.

Public oracles: P-U1/U2 style SEALED base + P-N3 ALREADY_ACTIVE + §7
record-before/expected-after/neither + §11.1 full 15-field resume vs narrow
same-set ordinary collision. FIX vs failure: FIX = INTENT_COLLISION (no
r3) + RESUMED + ALREADY_ACTIVE; failure (old code) = ACTIVATED r3 duplicate
intent (defect, qualified, not green).
