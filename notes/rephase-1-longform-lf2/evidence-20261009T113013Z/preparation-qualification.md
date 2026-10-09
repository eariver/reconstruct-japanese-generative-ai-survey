# Preparation qualification for `prepare_copy.py` (exact-run evidence only)

2026-10-09. `notes/rephase-1-longform-lf2/evidence-20261009T113013Z/prepare_copy.py`
is exact-run evidence, not a certified rerun tool. Original files preserved;
this qualification bounds its claims. No source/test/fixture execution, no
ref writes, no network in this call.

## 1. Guard omissions (bounded)

- Clears only `GIT_DIR/GIT_WORK_TREE/GIT_CEILING_DIRECTORIES/GIT_COMMON_DIR`
  in `CHILD_ENV` and logs parent values without asserting them. It does NOT
  clear or assert `GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`,
  `GIT_ALTERNATE_OBJECT_DIRECTORIES` (or `GIT_CONFIG*`). A hostile inherited
  value in those could redirect object/index reads. Bounded: current shell had
  none set (see current-verification log); the script's isolation claim rests
  on observed clean env, not on exhaustive override clearing.
- Origin check covers fetch URL only (`remote get-url origin`); push URL and
  `remote -v` all-remote listing were not asserted. Bounded: inert
  `https://example.invalid/...` fetch observed on both sides; push/all-remote
  sameness is supplied by the new current verification, not retroactively.
- `config --get extensions.partialClone` treats any nonzero exit as absence;
  a config error (not just unset key) would also pass. Bounded: exit was 1
  with empty output on both sides (key-unset signature), but error-vs-absent
  is not distinguished.
- `cp` retry branch (`--no-preserve=links` then fallback) has a precedence
  flaw: `rc != 0 and "unrecognized" in err or "invalid" in err` evaluates as
  `(rc!=0 and A) or B`. In practice first `cp` exited 0 so no retry ran;
  the branch is untested and not generally fail-closed. Do not reuse.

## 2. Counting correction

- "689 tracked bytes identical" is wrong units: 689 is materialized tracked
  FILES compared (plus symlink-target comparisons); 31466 is tracked paths
  absent on BOTH sides under sparse checkout, not the 26309 missing Git blobs
  of the recovery lineage. Content claim is only: every file present on both
  sides is byte-identical; absent sets match. History completeness is not
  claimed. Logs contain embedded NULs from `ls-files -z` capture; use `grep -a`.

## 3. First-attempt DST handling and script-byte survival

- Attempt 1 copied DST successfully (`cp` exit 0, DST HEAD/tree/status/hashes
  all PASS) then failed at tracked comparison on sparse-absent
  `sources/...` paths. Preserved as `prepare-attempt1-sparse-fail.log`
  (exit 1). Retry handling: attempt-1 logs renamed (`prepare-*-attempt1*`),
  partial DST removed with `rm -rf <DST>` (DST absent re-verified, exit-path
  `ls` 2), then the FIXED script re-ran to fresh exclusive `prepare.log`
  (exit 0). First DST bytes do not survive; no missing raw was recreated —
  attempt-1 logs are the originals. Current `prepare_copy.py` bytes include
  both fixes (sparse-aware comparison, removed invalid
  `git --is-shallow-repository` probe); the attempt-1 log still shows the old
  probe's exit-129 noise, which is preserved history, not current proof.

## 4. Current verification scope (not retroactive)

- New `current_verify.py` + `current-verification.log` assert NOW: all seven
  routing overrides absent (four GIT_* plus INDEX_FILE/OBJECT_DIRECTORY/
  ALTERNATE_OBJECT_DIRECTORIES), HEAD/tree/parent, exact 3-status, exact
  3 hashes, fetch AND push origins inert, no alternates/partialClone, zero
  shared object (dev,ino), DST regular-object nlink==1, sparse lists equal.
  It cannot retroactively certify copy-time checks; it only corroborates
  current separation/identity. No candidate imports, no tests, no fixtures,
  no ref writes.
