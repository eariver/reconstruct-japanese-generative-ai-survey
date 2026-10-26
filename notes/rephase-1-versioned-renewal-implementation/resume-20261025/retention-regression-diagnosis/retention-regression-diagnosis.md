# P2R retention regression diagnosis — 20261025T164000Z (bounded, no product edit)

## Verdict: harness/environment fault, NOT public guard regression

`test_replacement_owned_file_midcapture_refuses` fails with
`RetentionError FILE_REPLACED not raised` because the fault-injection
itself no longer changes `(dev,ino)` on workspace ext4, so the
pin-vs-reverify seam is never reached. Product guard intact.

## Authority (readonly)

- Fixed740: `.rephase-1-editorial-runtime/versioned-renewal-archive-input-20261025T133248Z/snapshot-work`
  HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, 740 files.
- Baseline57 proof-copy: `.rephase-1-editorial-runtime/final-source-packaging/proof-copy/candidate-partial-b40de60`
  HEAD `409b292…`, tree `8ce36998…`, 721 files.
- Product/test identical:
  `scripts/survey_editorial_retention_v2.py` SHA256 `036d258fa58fc876956c79cae9f51b861a731b3128a73084af921ead28a52771` both.
  `tests/test_survey_editorial_retention_v2.py` SHA256 `954f858617b8bba5e819fbc327acee35913c0cf50588f8135a5e5c85c34bd058` both.
  P1 differs (`825dba…` vs `23e3a4…`) but renewal-only branches guarded by
  `kind==VERSIONED_RENEWAL_SOURCE_V1` / `_is_renewal_receipt`; ordinary Weekly
  fixture (17 COPY paths, same `victim_rel`) does not take them.
- Reconstruct HEAD `f84fcf5321be3798c862c0156278afbba01f89f6` clean pre/post (untracked only).

## New independent DBs (workspace TMPDIR, no network/old-runners/candidate commits)

- `…/versioned-renewal-retention-diag-20261025T164000Z/test-source-current`
  HEAD `15e29906a038f2f4b2aa6cd15a0aff67cc5af5e1` (parent `409b292`), `ls-files` 32206, intended 740/740 tracked, `.git` 83 files, no alternates, inert origin, dev/ino disjoint, nlink==1.
- `…/test-source-baseline`
  HEAD `7819d511d84bf81deed37740a0a819cfe53088a0`, `ls-files` 32187, intended 721/721 tracked, same isolation.
- TMPBASE `…/tmp`, fresh child per module, `PYTHONDONTWRITEBYTECODE=1`, Python 3.14.4.

Kept fixtures = two TEST-ONLY SOURCE DBs above. Per-test `tempfile` scratch dirs are ephemeral by test design; their before/after snapshots + dev/ino are saved in JSON below.

## Bounded runs (ONLY failed + healthy control, current DB)

- Failed: `tests.test_survey_editorial_retention_v2.EditorialRetentionV2Tests.test_replacement_owned_file_midcapture_refuses`
  exit 1, 26.477s, `AssertionError: RetentionError not raised` (reproduces affected-regress 685s full-suite fail).
  Raw: `run-failed-current-stdout/stderr/exit.txt`, start `20261025T153447Z` end `20261025T153514Z`.
- Healthy control: `…test_replacement_root_ancestor_file_refuses`
  exit 0, 23.992s, OK. Pin before/after `15e2990…` unchanged.
  Raw: `run-control-current-*`.

No false PASS: control asserts `ROOT_IDENTITY_CHANGED|ANCESTOR_REPLACED` on its own seam; failed asserts `FILE_REPLACED` on owned-file seam. Distinct codes, no unrelated earlier refusal accepted.

## Instrumentation (no validator bypass, hook counts/target/dev-ino/before-after)

Replica `diag_instrument.py` (same `_fresh_weekly`, `_build_weekly_validated`, `_prepare_proposal_for`, same `proposal_id=fixture-wk-rp-own`, same `os.open` hook on `retention-manifest.json` CREATE):

- Current740 (`diag-current-obs.json`):
  `swapped_done=true`, `swapped_count=1`, `manifest_open_count=23`,
  first CREATE `retention-manifest.json flags=131265 dir_fd=10 swapped_before=false` (5th call),
  `victim_rel=sources/…/fixture-wk-rp-own/retained/before/sources/2026-W37/production-state.json`,
  `copy_paths` 17 same as baseline, `victim_before dev=2050 ino=23338920 sha=74af…`,
  `victim_after dev=2050 ino=23338920 sha=74af…`, `ino_changed=false`, `sha_same=true`,
  `result.raised=false`, `RETAINED_SET_CAPTURED`, `added_count=18`, `added_outside_owned=[]`, `live_drift=[]`.
- Baseline721 (`diag-baseline-obs.json`): identical shape,
  `swapped_done=true`, `manifest_open_count=23`, `ino_changed=false`, `raised=false`, `CAPTURED`.
  So seam missed in BOTH envs, not a current740-only product change.

Hook seam IS reached (manifest CREATE fires once, victim path exists at hook time). Replacement does NOT happen between actual pin and final reverify because `unlink+write_bytes(same bytes)` reuses same inode on ext4.

Filesystem proof (`filesystem-inode-proof.txt`, `filesystem-df.txt`):

- Workspace TMPBASE (ext4 `/dev/sda2`, dev 2050): `unlink+write` → same ino (`23334230==23334230`, `same=True`).
- `/tmp` (tmpfs, dev 45): `unlink+write` → new ino (`1892643→1892644`, `same=False`).
- `rename+write` and `temp+replace` on same ext4 → new ino (`23334333→23334334`), proving method matters.

Rename-variant probe (`diag_rename.py`, current DB, `diag-rename-current-obs.json`):

- Same hook, but `victim.rename(backup); victim.write_bytes(data)`:
  `ino_changed=true` (`23338924→23338943`), `sha_same=true`,
  `result.raised=true`, `code=FILE_REPLACED`, `phase=MANIFEST_PUBLISH`, `disposition=OWNED_PARTIAL`,
  `detail=consumed file recheck file identity changed: …production-state.json`.
- Proves public guard works when seam IS reached; no product regression.

## Transitive diff / timing (no preexisting assumption)

- `survey_editorial_retention_v2.py` diff exit 0 (identical). Test file identical.
- P1 renewal additions strictly kind-gated; ordinary Weekly `retention_plan` 17 rows, `victim_rel` identical, manifest timing identical (23 opens, swapped at CREATE). `CONTROL`/`readback` injection tests (`test_capture_readback_control_edition_injection_refuses`) still PASS with same hook, confirming manifest-open window and post-verify checks run. Only `FILE_REPLACED` via dev/ino misses due to inode reuse.
- Body old P2R unchanged inspected; not assumed preexisting — proven by SHA + hook log + rename probe.

## Proposal (TEST-ONLY, for root approval — NOT applied, shared test not edited)

File: `tests/test_survey_editorial_retention_v2.py:1537-1539` in `test_replacement_owned_file_midcapture_refuses`.

Replace:
```python
data = victim.read_bytes()
victim.unlink()
victim.write_bytes(data)
```
with ext4-stable:
```python
data = victim.read_bytes()
backup = victim.with_suffix(".bak")
try:
    backup.unlink()
except FileNotFoundError:
    pass
victim.rename(backup)
victim.write_bytes(data)
# optional cleanup backup after capture attempt (test already handles .bak elsewhere)
```
and same for `diag_instrument.py` replica. This guarantees `ino_changed=true` on ext4 and tmpfs, preserving same-bytes/new-inode oracle. No product change, no validator bypass, no `O_NOFOLLOW`/read-order change.

If product hardening desired (separate root decision, NOT required for this fail): `scripts/survey_editorial_retention_v2.py:412-413`, `338-341`, `1685-1687` currently bind only `(dev,ino)`; same-inode-number reuse with same bytes is inherently invisible. Would need birth-time/generation or write-counter, but that is new scope, not this regression.

## Raw set (this dir)

`diag-start-utc.txt`, `cp-git-*-*`, `dst-current-*-*`, `dst-baseline-*-*`, `pin-current-before/after-*`,
`run-failed-current-*`, `run-control-current-*`,
`diag_instrument.py`, `diag-current-obs.json/stdout/stderr/exit.txt`,
`diag-baseline-obs.json/*`, `diag_rename.py`, `diag-rename-current-obs.json/*`,
`filesystem-inode-proof.txt`, `filesystem-df.txt`.

No reconstruct/candidate commits, no network/pip/old-runner exec, no product/test edits. No whole-unit/CommitPoint.
