# Milestones 3/4 final report — fresh checks + portable snapshot at b40de60

Date: 2026-10-03 (runs ~13:45–13:55 JST). Authority:
`verification-decision.md`. No agents, no reconstruct commits/push, no Freeze
code, no feature/test edits. Runner/probe/restore sources saved in this packet
(`run_five.py`, `run_closure.py`, `restore.sh`, `restore_check.py`); per-command
raw in `raw/` (+`raw/five/`, `raw/closure/`, `raw/restore2/`). Earlier `raw/`
v1-restore failure outputs are preserved alongside the corrected run.

Identity (guarded before/after every run): HEAD
**`b40de600e9ed1f80cb278213ccf17aa5f3cd9de3`**, tree
**`657032438c6ed8b1c055d5a120b67b4b261a5092`**, direct parent real baseline
**`774dd39a951c9ac3818e83dfffd4c7666efb0a20`**. Env for all runs:
`GIT_NO_LAZY_FETCH=1`, `GIT_ALLOW_PROTOCOL=file`, `PYTHONDONTWRITEBYTECODE=1`,
cwd the exact fixture (tests) or packet (probes), pinned venv
`/tmp/opencode/candidate-recovery-tooling-20261003T0435Z/venv`
(Python 3.12.14, jsonschema 4.23.0, pypdf 6.16.2). No inherited Git-root/object
overrides (verified absent). Guards abort on changed HEAD/tree/tracked bytes;
all guards held (before == after everywhere).

## 1. Five approved methods — all PASS, run once each (exit 0)

| # | Method (class + name) | Time | Result |
|---|---|---|---|
| 1 | `SurveyProfiledFreezeV2Tests.test_thematic_and_weekly_public_identity_remain_natural` | 0.000s | ok (no builder invocation — identity regression only) |
| 2 | `FreezeStageBoundaryV2Tests.test_weekly_approved_preview_advances_through_real_freeze_boundary` | 11.754s | ok, terminal FROZEN |
| 3 | `FreezeStageBoundaryV2Tests.test_freeze_artifact_set_rejects_missing_extra_and_wrong_visual` | 22.728s | ok — 3 subcases (missing/extra/wrong-visual) executed in-method; unittest verbose emits no per-subcase success lines, so they are reported as 3/3 within the single passing method, not as 3 methods |
| 4 | `GateCliPersistedReviewV2Tests.test_direct_primary_cli_admission_absolute_relative_and_cwd` | 0.909s | ok — 3 path/cwd subcases in-method (same reporting note) |
| 5 | `SurveyPublicationV2Tests.test_exact_reviewed_pdf_chain_reaches_release_without_postapproval_quality_gate` | 2.443s | ok (synthetic Release record, not a real Release) |

Fixture-scope distinction (read from test sources, confirmed by run):
methods 1/2/3/5 use **no Git subprocesses and no real Git repos** — synthetic
fixture data in `tempfile` sandboxes (stage temps nested under the recovered
CWD, auto-cleaned; post-run status shows none remain) with real production
validators bound to the recovered repo root for path authority. Method 4 runs
the **real recovered CLI** via subprocess (`PYTHONPATH=REPO`, one subcase with
cwd=REPO) against synthetic manifests in its own temp fixture, and its module
reads the real recovered index (`git ls-files`, cwd=REPO) for the weekly
variant path. So: recovered CODE is exercised by all five; the recovered GIT
DB is read by method 4 and by the closure diagnostic below — not "all fresh
Git fixtures". Synthetic reviews/checkpoints/PDFs are not editorial, visual,
or Human-approval evidence; workflow text assertions are source-text checks,
not executed workflow runs; no DM-repair tests were selected or run.

## 2. Git-aware closure diagnostic — positive PASS + exact negative PASS

`current_closure(root)` → 8 rows (5 scripts incl. the 2 B-new files, 2 schemas,
1 style template); `_verify_head_bytes(root, b40de60..., closure)` on the
actual recovered DB returned cleanly: ancestor check (commit==HEAD), control
diffs quiet, no uncommitted control sources (untracked `scripts/__pycache__/`
tolerated by the helper's own pycache rule), closure complete, all 8 rows byte
equal in worktree and in `git show` at both commit and head. In-memory
deep-copy with one sha256 corrupted raised exactly
`ValueError("Weekly receipt current-tool closure drift:
scripts/survey_weekly_derivation_v2.py")` — required prefix + name, no file
mutations, no replay, no old-ancestry claim. Source recorded: module file
sha256 == closure row 1; git blob `6d14009...` (R1 postimage).

## 3. Failures encountered (all preserved in raw, none hidden)

- `35-imports` (m2): wrong probe path, corrected by `35b` (see supplement C3).
- Tar build: first attempt failed (stale path bug from `split(None,2)` keeping
  the line terminator — author error, no fixture impact); member list
  regenerated from the authoritative tar listing; final tar exit 0, 760 members.
- Restore v1 script assumed `git/`+`worktree/` subdirs; actual archive holds
  `.git/`+flat worktree (better layout); v1 extracted then cleaned itself up
  (empty dest, raw preserved). v2 corrected layout but asserted 686 moved
  top-level entries where 12 dirs moved (files nested); completed manually with
  recorded `rmdir` (remnant was empty; 686 files + `.git` verified in place).
  `restore.sh` now asserts the recursive file count. All v1/v2 raw kept.

## 4. Portable archive (≤50MiB gate: PASS at ~4.9MiB)

`candidate-partial-b40de60.tar.gz` — **5,152,199 bytes**,
SHA256 `faf6792faf37ad30af2dbd7203b8896ca00964a91d00623a4f01278f2ade9f3c`
(`.sha256` alongside). Deterministic build
(`--sort=name --owner=0 --group=0 --numeric-owner --mtime=2026-10-03`, `gzip
-n`). Contents (760 members, all under `candidate-partial-b40de60/`, no
absolute/`..` paths, no symlinks): entire available `.git` (74 files:
objects, refs, HEAD, config, shallow, sparse metadata, hooks samples, index,
logs, COMMIT_EDITMSG) **minus `.git/FETCH_HEAD`** (names the real acquisition
URL; content preserved in m2 `raw/04-fetch.*`), plus the 686 materialized
tracked worktree files. Excluded and stated: untracked `scripts/__pycache__/`
(21 files), venv/tooling (163M, outside by design), test temps (none remained),
credentials (none present; configs verified clean).

Closure census (no hydration; first plain `rev-list` fatal on a missing
promisor blob, preserved as partial-closure evidence; retry with
`--missing=print`): **28,626 reachable objects — 2,317 present** (2 commits,
1,608 trees, 707 blobs; batch-check confirms 0 missing among them) and
**26,309 promisor-missing blobs** (bulk `sources/`/unmaterialized paths).
Worktree: 32,152 tracked, **686 materialized, all byte-identical to HEAD blobs
(0 mismatches)**; shallow `[774dd39a...]`, sparse cone recorded with hashes.

## 5. Offline restoration (second independent dir, no 5-test repeat)

`/tmp/opencode/jgas-recovery-restore-20261003T0445Z` (was absent; listing
pre-checked). Verified: HEAD/tree/parent identical; `ls-tree -r` byte-identical
to original; object-store inventory identical **except** `.git/FETCH_HEAD`
(deliberate exclusion) and `.git/index` (stat-refresh by read-only git, proven
content-identical via `ls-files -s` + clean `diff` both sides); worktree 686
files byte-identical (only delta = excluded pycache); **0 shared inodes, no
hardlinks either side, no alternates, inert origin only**. Restored-copy
**positive diagnostic only** (`restore_check.py`, pinned external venv):
`restored_positive=PASS rows=8`, worktree still clean afterwards.

## 6. Limitations (honest partial snapshot)

Partial DB + sparse worktree backup — not a complete repo/history; 26,309
blobs and all non-baseline ancestry unavailable offline; tree equality is
content equality, not asset closure; 41 R1 data blobs unverified; synthetic
fixtures prove type/identity/flow, not semantic/visual/Human authority;
read-only git may refresh index mtimes (bytes unaffected). No old-e4/481
ancestry or PASS is claimed or transferred.

No further work starts here: D1/D2 (test/closure argv) are now EXECUTED per
the decision; archive/restore proof complete. Awaiting Astra + fresh
independent review; Human owns any commit/push.
