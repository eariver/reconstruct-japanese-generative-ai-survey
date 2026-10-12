# Current-restoration qualification (read-only corroboration)

2026-10-11T16:15:49Z. Restored copy accepted as available; NOT re-extracted,
deleted, or modified. Phase A scripts/raw/proposal preserved unmodified.
New files only in `evidence-20261011T161549Z-qualification/`: `current_checks.py`
(v1, executed once, exit=10), `current_checks_v2.py` (XY-literal fix, executed
once, exit=0), `check.stdout/stderr/exit`, `check-v2.*`. Stdlib only, no app
imports/tests/fixtures/network. Restored worktree still exact 2M7A after checks.

## Current observations (v2, ALL_CURRENT_CHECKS_PASS)

- Identity: HEAD409b292/tree8ce36998/parent34f934e verified; C222/CE170/FINAL
  `cat-file -e` present; chain 409→…→e170→222→…→b40→774; status exactly the 9
  accepted paths (` M`×2 + `??`×7).
- Nine files: all regular non-symlink, SHA256 match manifest, mode 0o664 match,
  bytes>0 (2720…107757).
- Separation (correct `os.stat` st_dev/st_ino): restored DB 107 files, all
  nlink=1, single device; workspace DB 1045 files; shared (dev,ino) = 0.
- Archive (stdlib tarfile, no extraction): 760 members, single topdir, all
  regular-file type, 0 absolute, 0 `..`, 0 duplicates, 0 symlinks/hardlinks,
  0 devices, no FETCH_HEAD.
- Config/hooks/routes: `.git/config` = bare repo + inert `example.invalid`
  origin only, no `core.hooksPath`; hooks dir holds 14 `*.sample` files, 0
  active; no alternates; no inherited `GIT_*` env (incl. `GIT_COMMON_DIR`).

## Explicit qualifications (no general-safe-restorer claim)

1. v1 `find -printf '%d %i'` recorded directory depth, not device; its
   workspace comparison used `stat %d` (device), so the old zero-intersection
   claim proved nothing. Superseded ONLY by the v2 `st_dev/st_ino` result above.
2. The overlay verifier asserted hashes only; modes were printed, status was
   count-only (`2M`/`7`). Now asserted: exact per-path mode equality, exact
   status path+code rows, regular-file/non-symlink types.
3. Old restore scripts never rejected/cleared inherited `GIT_COMMON_DIR` and
   printed (not rejected) hooks/config; traversal grep escaping was fragile;
   not all stdout writes were exclusive. They remain historical exact-run
   evidence, not reusable safe tools.
4. This audit ran AFTER extraction against preserved bytes: it corroborates
   current state only and is not a retroactive pre-extraction proof.

## Failed attempts preserved

- Phase A `attempt-01` (outer redirect before `raw/` existed; script never ran).
- v1 `status-exact-2M7A` FAIL: comparator literal `"M"` vs true porcelain `" M"`;
  observed rows already showed exact 2M7A; v1 log kept, v2 confirms.
- Stray empty `current_checks_v2.py` written to repo root by a wrong-cwd `sed`
  redirection; removed immediately (`rm`), workspace re-verified clean (only
  intended untracked `notes/rephase-1-dm021-p1/`).
