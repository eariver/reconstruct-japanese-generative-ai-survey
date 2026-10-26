# R1 oracle final — TEST-ONLY tightened pointer (no whole PASS, no CommitPoint)

2026-10-25. Bounded TEST-only. Candidate
`.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work`
(HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree
`8ce3699861505f32d1d60bdc185d4d4f635aedb2`). No runtime edits.
Only `tests/test_survey_weekly_mechanical_refresh_v2.py` lines 552-585 pointer case
tightened (ROOT-approved TEST-only).

## Test-only edit (this file only, no runtime code patch)

Previous empty workers DID apply recipe-copy (`.latexmkrc` exact copy + SHA check,
lines 84-96) + pointer-oracle update (loose OR
`VERSIONED_ACTIVE/invalid|selection mode probe missing|versioned renewal unselected`
+ `before` snapshot + `record_list` + lock/retention absence). Preserved.

Tightened 2026-10-25 (hash `52e15457d153efe687e0a61de360d92b7ba9053d08b53820579bb9c10e1549c7`,
prev `609e59513eb29b7b960e254241a23c83bd838a6dbd7bfee228142892d9b15042`):

```python
self.assertEqual(proc.returncode, 2, msg=proc.stdout)
# Tightened 2026-10-25 ROOT-approved TEST-ONLY: require actual
# missing-r9.json selection-missing cause (not loose OR).
self.assertIn("missing-r9.json", proc.stderr)
self.assertRegex(proc.stderr, "selection mode probe missing")
self.assertRegex(proc.stderr, "VERSIONED_ACTIVE/invalid")
self.assertRegex(proc.stderr, "versioned renewal unselected")
self.assertEqual(before, self._snapshot([state_path, edition["receipt_path"], edition["gate_path"]]))
```

Requires actual `missing-r9.json` / `selection mode probe missing` cause plus
`returncode 2` plus existing no-write inventory (`before` equality,
`record_list==[]`, `.mechanical-refresh.lock` absent,
`.mechanical-refresh-retention` absent). Loose OR rejected.

Runtime diff preserved: `diff HEAD --name-only | grep -v ^tests/ | wc -l` = 38
(pre-existing inherited 38, no new runtime patch). Total `diff HEAD --stat` = 40
(38 runtime + 2 tests: `test_survey_dm004_release_validate_state_v2.py`,
`test_survey_weekly_mechanical_refresh_v2.py`). Intended source 741 preserved
(filesystem walk excluding `.git/__pycache__/*.pyc`).

## NEW independent complete-source snapshot (no shared candidate execution)

- Base: `.rephase-1-editorial-runtime/versioned-renewal-r1-oracle-final-20261025T191500Z/snapshot-work`
- `cp -a SRC/.git DST/.git` (no `-l`), own absolute gitdir, inert
  `origin https://example.invalid/weekly-mechanical-refresh-fixture.git`,
  `objects/info` absent, `NO_ALTERNATES_OK`, `NO_GIT_OVERRIDE_OK`,
  `nlink==1` all, `dev:ino` disjoint (see `dst-isolation-*`).
- Worktree populated via `populate_snapshot_20261025T191500Z.py` filesystem walk
  (all 741 intended, **not `git ls-files`-only** — includes all untracked intended
  scripts/schemas + `.latexmkrc`). `SRC_INTENDED_COUNT 741`,
  `DST_POPULATE_OK 741`, `cmp` SRC==DST for both test file and `.latexmkrc` exit 0.
- Candidate AND tested file hash both same:
  `52e15457d153efe687e0a61de360d92b7ba9053d08b53820579bb9c10e1549c7` (SRC + DST).
- Helper `.latexmkrc` copied:
  `18199fd85e3e3c46ede9322a709e4f64e39470f69c6c20935e598d4c08adbc26`
  (SRC + DST, `cmp` exit 0; test internal recipe SHA check also passes).
- Workspace TMPDIR: `$DST_BASE/tmp` exported as `TMPDIR` for both unittest runs
  (see `commands.log` `TMPDIR=.../tmp`), `PYTHONDONTWRITEBYTECODE=1`,
  `PYTHONPATH=DST`, `cwd=DST`. No network/old runners/cleanup.
- No candidate or reconstruct commit: SRC HEAD still `409b292`, RECON HEAD still
  `f84fcf5321be3798c862c0156278afbba01f89f6`, RECON `diff --cached` empty,
  `status` untracked-only (parallel packet files allowed).

## Source-only meaningful fixture commits BEFORE authorities (independent DB only)

- `cbb9a13` parent `409b292`: `R1 oracle final TEST-ONLY tightened pointer`
  (1 file `tests/test_survey_weekly_mechanical_refresh_v2.py`, 26+/1-, real bytes,
  process-scoped `Synthetic-R1-Oracle-Final`, not `--allow-empty`).
- `0f3ce53` parent `cbb9a13`: `R1 oracle final complete 741 SOURCE
  (all untracked intended now tracked) before authorities` (`git add -A`,
  no pycache, status clean post-commit, `ls-files` now 32207 includes
  `schemas/editorial-manuscript-spec-v2.schema.json`). Required because test
  `setUp` copies via `git ls-files -- config schemas scripts ...` — untracked
  renewal schemas would otherwise miss contract file (first-attempt failure
  disclosed below). Both commits source-only, before successful authorities.
  Old fixture DBs untouched, no deletion.

## Actual 2-method results (ONLY these two, same old 33 already PASS not rerun)

Successful run (HEAD `0f3ce535cf878c7380424ab32dd4daa794a66157`):

- `test_malformed_old_authority_refused` — exit `0`,
  `Ran 1 test in 12.235s`, `OK` (`test-malformed-old-authority-refused-*.txt`).
  Tightened pointer subTest `case="pointer"` requires `missing-r9.json` +
  `selection mode probe missing` + `VERSIONED_ACTIVE/invalid` +
  `versioned renewal unselected` + `returncode 2` + no-write inventory.
  `case="gate-bytes"` unchanged.
- `test_first_and_repeat_success` (healthy R1 control) — exit `0`,
  `Ran 1 test in 31.787s`, `OK` (`test-first-and-repeat-success-*.txt`).
  Proves tightened oracle causes no healthy-path regression.

First attempt (HEAD `cbb9a13`, before complete commit) BOTH exit `1` in `0.32s`
with `ValueError: contract file does not exist:
schemas/editorial-manuscript-spec-v2.schema.json` (test `setUp` `ls-files`
missed untracked renewal schema). Preserved as
`test-*-first-*.txt` (stdout/stderr/exit), not cleaned, not adopted.
No other methods run (same old 33 already PASS, per task).

## Evidence files (this dir)

- `make_r1_oracle_final_20261025T191500Z.sh` (`bash -n` 0) + `commands.log`
  (every `git/cp/python` to unique `*-stdout.txt/*-stderr.txt/*-exit.txt`).
- `populate_snapshot_20261025T191500Z.py` (filesystem copy, not ls-files-only).
- `make_complete_20261025T191500Z.sh` (second complete commit) + log entries.
- `run_r1_oracle_final_20261025T191500Z.sh` (`bash -n` 0) + authority pins
  (`authority-dst-head/test-sha/latexmkrc-*`) + 2-method outputs + first-failure
  copies (`*-first-*`).
- Source pins: `src-head/tree/test-sha/latexmkrc-sha/count/status/diff-names/remote`,
  `dst-head/gitdir/remote/noalternates/env-check/count/test-sha/latexmkrc-sha/cmp/status/diff-names/isolation/add/commit/head-post/log-post/status-post/show-stat`,
  plus complete-commit pins (`dst-*-complete-*`, `dst-ls-files-count`).

No whole PASS claimed (only 2/34 methods in this file, not full 33/34 suite).
No CommitPoint. Ordinary candidate/reconstruct Commit/Push Human-owned.
Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN preserved.
