# Reconciled failure/boundary ledger — named IDs, actual source, exits (NO guessing)

TEST-only. Old 16 sum confused (see `failure-resume-verification/testmatrix.md`
§§6/9: §6 counted 12 fault HIT with depth double-count ambiguity + 3 partial +
3 seam-miss; §9 revised to 16 HIT (11+5) + 5 partial + 3 seam-miss + 5 defects +
11 OPEN, mixing stale vs CURRENT and counting H-ACT setups as separate methods).
This ledger reconciles by **named ID with actual source/exit read from disk**
(`raw/case-*/exit.txt` + `result-*.json` + manifest/testmatrix source markers).
NO new counts from guessing. Methods/subcases/harness errors/earlier-guard
controls split (distinct, no false aggregation). No whole-unit/independent PASS.

## A. 39 old raw case dirs (failure-resume-verification, preserved, NOT rerun)

Actual scan 2026-10-25 (see
`boundary-verification/raw/case-ledger-reconcile-20261025T000000Z/result-ledger-reconcile.json`):
**39 raw case dirs: 37 exit 0, 1 exit 1, 1 missing.**
Non-case dirs (NOT counted here): `fixture-current-20261026T000000Z`,
`healthy-current-20261026T000100Z`, `healthy-u1-20261025T150000Z`,
`own-current-20261026T000000Z`.

| Case ID | Exit (actual `exit.txt`) | Source (actual pins/manifest) | Result file (actual) | Cited verdict (testmatrix, preserved) |
|---|---|---|---|---|
| `case-rec-write-20261025T150200Z` | 0 | STALE 9a0469ef/H6fe/S20f (e211e6e, fr-u1-weekly) | `result-rec-write.json:HIGH_UNREADABLE` | HIT (record write → PRESERVED_INCOMPLETE, State unchanged) |
| `case-rec-short-20261025T150300Z` | 0 | STALE (same) | `result-rec-short.json:HIGH_UNREADABLE` | HIT (short-write → post-read mismatch) |
| `case-rec-fsync-20261025T150300Z` | 0 | STALE | `result-rec-fsync.json:HIGH_UNREADABLE` | HIT (fsync) |
| `case-rec-close-20261025T150300Z` | 0 | STALE | `result-rec-close.json:HIGH_UNREADABLE` | HIT (close) |
| `case-rec-combined-20261025T150300Z` | 0 | STALE | `result-rec-combined.json:HIGH_UNREADABLE` | HIT (write+close, both preserved) |
| `case-state-temp-write-20261025T150300Z` | 0 | STALE | `result-state-temp-write.json:INDETERMINATE` | HIT (temp write, orphan r2 preserved) |
| `case-state-temp-fsync-20261025T150300Z` | 0 | STALE | `result-state-temp-fsync.json:INDETERMINATE` | HIT (temp fsync) |
| `case-state-temp-close-20261025T150300Z` | 0 | STALE | `result-state-temp-close.json:INDETERMINATE` | HIT (temp close) |
| `case-state-replace-fail-20261025T150300Z` | 0 | STALE | `result-state-replace-fail.json:INDETERMINATE` | HIT (replace, orphan+tmp preserved) |
| `case-postread-new-20261025T150400Z` | 0 | STALE | `result-postread-new.json` (ACTIVATED, patch missed dir_fd) | Seam-miss (injection ineffective, preserved) |
| `case-foreign-symlink-20261025T150400Z` | 0 | STALE | `result-foreign-symlink.json` (ACTIVATED r3, max-advance) | Seam-miss (naive, no race hiding; BUG-adjacent per root, preserved) |
| `case-indeterminite-20261025T150400Z` | 0 | STALE | `result-indeterminite.json:SELECTION_BEFORE` | Partial (earlier guard, NOT resume-INDETERMINATE) |
| `case-already-active-20261025T150400Z` | 0 | STALE | `result-already-active.json` (ALREADY_ACTIVE) | HIT (readonly ALREADY_ACTIVE, full readback) |
| `case-alias-refuse-20261025T150400Z` | 0 | STALE | `result-alias-refuse.json` (HIGH_MODE symlink) | Partial (earlier symlink guard, NOT alias-identity) |
| `case-drift-copy-20261025T150400Z` | 0 | STALE | `result-drift-copy.json:HISTORY_DIGEST_MISMATCH` | HIT (late guard, pre-write, no record) |
| `case-drift-tool-20261025T150400Z` | 0 | STALE | `result-drift-tool.json:BASIS_CURRENT_TOOL_DRIFT` | HIT (CURRENT check every readback) |
| `case-excl-conflict-20261025T150100Z` | 0 | STALE | `result-excl-conflict.json` (ACTIVATED r3, naive) | Seam-miss (naive max-advance; BUG-adjacent, preserved) |
| `case-orphan-resume-20261025T150400Z` | **MISSING** (timeout-incomplete, preserved, NOT adopted) | STALE | `result-orphan-resume.json` (partial, no exit) | Timeout-incomplete (complete `150500Z` supersedes for setup, NOT as RESUMED PASS) |
| `case-orphan-resume-20261025T150500Z` | 0 | STALE | `result-orphan-resume.json` (INDETERMINATE temp-exists) | Partial (orphan proven, temp-blocked, RESUMED OPEN) |
| `case-healthy-activate-20261025T150500Z` | 0 | STALE (H-ACT control) | `result-healthy-activate.json` (ACTIVATED) | Healthy control (proves fault caused refusal, NOT counted inside setups) |
| `case-high-prepare-33-20261025T150600Z` | 0 | STALE (typed33 `9b5c…`) | `result-high-prepare-33.json:BASIS_ENTRY_INELIGIBLE` | HIT (ENTRY depth, no R, State unchanged, typed — NOT 32 real ops) |
| `case-excl-race-conflict-20261025T151000Z` | 0 | STALE | `result-excl-race-conflict.json:TypeError` | Harness defect (scandir context-manager, preserved, NOT counted) |
| `case-excl-race-conflict-20261025T151500Z` | 0 | STALE | `result-excl-race-conflict.json:RECORD_COLLISION` | HIT (race-hiding conflict, no takeover) |
| `case-excl-race-samebytes-20261025T151600Z` | 0 | STALE | `result-excl-race-samebytes.json` (wrong-root harness_error) | Harness defect (wrong-root, preserved, fixed in `152000Z`) |
| `case-excl-race-samebytes-20261025T152000Z` | 0 | STALE | `result-excl-race-samebytes.json:RECORD_COLLISION` | HIT (same bytes still collides, no takeover, no new writer) |
| `case-foreign-race-symlink-20261025T152100Z` | 0 | STALE | `result-foreign-race-symlink.json:RECORD_COLLISION` | HIT (exact-target ино, no unowned delete) |
| `case-postread-dirfd-20261025T152200Z` | 0 | STALE | `result-postread-dirfd.json:HIGH_MODE` | Partial (open-fail, State NEW + record preserved, BUT code HIGH_MODE NOT INDETERMINATE mismatch) |
| `case-indeterminite-resume-20261025T152300Z` | 0 | STALE | `result-indeterminite-resume.json` (INDETERMINATE neither-nor) | HIT (resume with State neither before nor after, preserve) |
| `case-alias-hardlink-20261025T152400Z` | 0 | STALE | `result-alias-hardlink.json` (SEAL_BIND different-leaf) | Partial (earlier set-shape, NOT alias-identity; same inode/SHA/different spelling + NOT ALREADY proven) |
| `case-orphan-manual-resume-20261025T152500Z` | 0 | STALE | `result-orphan-manual-resume.json` (wrong-root harness_error) | Harness defect (preserved, fixed in `152700Z` fork2 subprocess) |
| `case-orphan-manual-resume-20261025T152600Z` | 0 | STALE | `result-orphan-manual-resume.json` (wrong-root) | Harness defect (same, preserved) |
| `case-orphan-manual-resume-20261025T152700Z` | 0 | STALE (HIGH `9a0469ef` defect code) | `result-orphan-manual-resume.json` (ordinary ACTIVATED r3 + resume RESUMED) | Reclassified per ROOT: ordinary r3 = **PRODUCT BUG** (must be INTENT_COLLISION, NOT green max-advance; fixed in `b12439d5`); resume RESUMED still valid (preserved). NOT counted as HIT for ordinary. |
| `case-cycle-proper-rehash-20261026T000200Z` | 0 | **CURRENT** 1dad1ad/H74275d/S2290ddd (4851523, cu1-weekly) | `result-cycle-proper-rehash.json:HISTORY_DIGEST_MISMATCH` | Qualified preemption (digest, NOT cycle HIT; true cycle OPEN) |
| `case-sequence-nonincreasing-time-20261026T000200Z` | 0 | **CURRENT** (same) | `result-sequence-nonincreasing-time.json:HISTORY_ANCESTOR` | HIT (sequence/chronology, proper rehash, CURRENT) |
| `case-postreplace-true-mismatch-20261026T000200Z` | 0 | **CURRENT** | `result-postreplace-true-mismatch.json:INDETERMINATE` | HIT (true mismatch, `os.read` wrong-bytes, State NEW + record preserved) |
| `case-parent-alias-same-leaf-20261026T000200Z` | 0 | **CURRENT** | `result-parent-alias-same-leaf.json` (HIGH_MODE ancestor) | HIT as legitimate path guard (symlink ancestor, BEFORE writes, NOT ALREADY; per task label as path guard, NOT alias-identity) |
| `case-healthy-activate-current-20261026T000500Z` | 0 | **CURRENT** (H-ACT CURRENT control) | `result-healthy-activate-current.json` (ACTIVATED r2) | Healthy CURRENT control (for CURRENT faults, same pins, no mixing) |
| `case-high-prepare-33-current-20261026T000300Z` | **1** | CURRENT attempt | *(no result; harness defect `_copy` requires renewal modules absent in R6 typed33)* | Harness defect (preserved, NOT counted; fixed in `000400Z`) |
| `case-high-prepare-33-current-20261026T000400Z` | 0 | **CURRENT** (typed33 `9b5c…`, CURRENT HIGH/H) | `result-high-prepare-33-current.json:BASIS_ENTRY_INELIGIBLE` | HIT (cap33 prewrite no newR, CURRENT, typed legacy 33, NOT 32 real renewals) |

Cited verdicts above are from `testmatrix.md` §§6/8/9 + `continuation-current-20261026T000000Z.md`
§§1–7 (preserved, NOT re-derived here). Counts: distinct raw dirs (39), NOT
methods/subcases. verifies: 37 exit 0 (1 of which is defect `151000Z` TypeError
but exit 0 with `code=TypeError`, NOT PASS), 1 exit 1 (defect `000300Z`), 1
missing (timeout-incomplete `150400Z`). No whole-unit PASS inferred.

## B. 6 NEW boundary dirs (THIS unit, CURRENT 1dad1ad/H74275d/S2290ddd)

| Case ID (new UTC) | Exit (actual) | Source (actual, verified SHA before exec) | Observed (actual code) | Verdict |
|---|---|---|---|---|
| `case-cycle-defensive-20261025T000000Z` | 0 | OWN boundary snapshot (H74275d/HIGH1dad/S2290ddd, no fixture, no authority) | `HISTORY_ANCESTOR cycle` (2-cycle via controlled seam) + `HISTORY_ANCESTOR too deep` (33-linear) ; `CHAIN_LIMIT==32` | **HIT (standalone defensive unit, NOT public; no duplicate count with public citation)** |
| `case-alias-samleaf-20261025T000000Z` | 2 | OWN + fork H-ACT CURRENT (ACTIVATED r2) but wrong-root code | `BASIS_CURRENT_TOOL_DRIFT wrong-root` (product fail-closed, State unchanged, no new record) | Harness defect (preserved, NOT HIT; fixed in `010000Z`) |
| `case-alias-samleaf-20261025T010000Z` | 0 | OWN + fork H-ACT CURRENT (same CURRENT pins, fork code SHA verified before exec) ; real dir + hardlink same leaf (`alias-r-samleaf/publication-set.json`, `nlink==2`, same inode/SHA, different spelling) | `RECORD_COLLISION alias-identity (NOT ALREADY_ACTIVE, BEFORE writes)` ; State unchanged, no `r3`, alias preserved ; helper `_check_already_active_set` same alias refusal (confirmation subcase) | **HIT (public, true B3 seam; helper NOT separate method)** |
| `case-depth32-attempt-20261025T000000Z` | 2 | OWN + fork CURRENT base (editorial r1 template, read-only, synthetic untracked E) | `HISTORY_DIGEST_MISMATCH: repeated activation before_candidate must equal predecessor seal Candidate` (30 editorial clones, read-only, State unchanged, no new R) | Exact predicate failure (NOT HIT for 32-valid; proves naive editorial cloning unconstructible without re-deriving bindings) |
| `case-depth32-legacy-20261025T010000Z` | 0 | OWN + fork anchor-fix fixture (legacy r1 `8974df…` template, read-only) | `HISTORICAL_IDENTITY_VERIFIED` (30 legacy clones, REAL SHAs, same issue/prior_checkpoint/rows, increasing sequence/time) | **HIT (bounded 30-legacy valid, fixture-provided typed history ≠ 32 real ops; NOT 32-valid for renewal)** |
| `case-ledger-reconcile-20261025T000000Z` | 0 | Read-only scan of `failure-resume-verification/raw/case-*` (no fixture, no authority) | 39 dirs: 37 exit 0, 1 exit 1, 1 missing (actual) | **HIT (reconcile, NO new counts from guessing)** |

NEW total: **6 raw dirs (4 HIT: cycle-defensive, alias-public, legacy-30, ledger;
1 exact-predicate failure: editorial-30; 1 defect: alias wrong-root)**. No
product edits, no new authority (alias reuses existing ACTIVATED r2, no new r3;
depth read-only, synthetic untracked E only, no State write, no new R; cycle/
ledger no fixture/authority). Fresh Python per SOURCE epoch, owned PID, workspace
TMPDIR, timeout-guarded, terminal exits persisted. No network/old-runner/
candidate/reconstruct commit/cleanup. Failed partial/foreign preserved (alias
defect fork + depth synth dirs + all old forks untouched).

## C. Reconciliation note (why old 16 sum was confused)

- Depth double-count: `high-prepare-33` counted in both healthy/depth (5) and
  fault-hit (12) in §6; §9 clarified as 11 activation/state/drift/already +
  1 depth already in healthy (total HIT 11+5=16 incl. continuation, plus depth/
  history/R7 in healthy). This ledger splits raw dirs (39) from methods/subcases
  (healthy H-U1 has 3 subcases; orphan-manual-resume has ordinary+resume 2
  subcases but counts as 1 method; R7-DEPTH is existing regression, NOT new).
- H-ACT setups inside already-active/alias/orphan re-ACTIVATE as prerequisites;
  only `H-ACT`/`H-ACT CURRENT` count as healthy ACTIVATED controls (NOT re-counted
  inside setups).
- Stale vs CURRENT: old cases (150100Z–152700Z) use stale 9a (`9a0469ef/H6fe/S20f`,
  fixture `e211e6e`, `fr-u1-weekly`); new cases (000200Z–000500Z + THIS unit)
  use CURRENT 1dad1ad/H74275d/S2290ddd (fixture `4851523`, `cu1-weekly`). Do NOT
  mix (continuation uses pinned 740 ONLY for old, CURRENT ONLY for new; P3S fix
  `9e2a0ad` out-of-scope for HIGH per manifest, U prototype new proof direct).
- Harness defects (5 old + 1 new alias wrong-root + 1 current `000300Z`) preserved,
  NOT counted as HIT/PASS; fixed re-runs are new UTC dirs (old NOT overwritten).
- Seam-miss naive (`excl-conflict-naive`, `foreign-symlink-naive`, `postread-new`)
  preserved as false previous (max-advance/ineffective, BUG-adjacent per root,
  NOT HIT); race-fixed continuations supersede for refusal (NOT deleted).
- Partial (earlier guard/temp-blocked/qualified preemption, 5 old + 0 new here
  except editorial-30 exact-predicate which is NOT partial but exact blocker)
  proves refusal/preservation BUT NOT intended seam; honest, NOT counted as HIT.

**No whole-unit/independent PASS, no CommitPoint.** Production semantic NO-GO
retained. Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN.
