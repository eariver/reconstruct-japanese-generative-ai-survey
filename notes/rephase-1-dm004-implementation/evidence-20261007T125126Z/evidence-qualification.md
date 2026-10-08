# DM-004 correction evidence qualification

- v2 runner `run_dm004_v2.py` (old `run_dm004.py` unchanged): child env built
  from a tight allowlist (PATH pinned to the executing interpreter's dir,
  PYTHONPATH, PYTHONDONTWRITEBYTECODE, 3 GIT_* flags, HOME only); every Git
  read asserts return code; both shipping files' worktree SHA256 are compared
  to `git show HEAD:path` bytes AND to expected content hashes pre/post;
  expected HEAD/tree/clean asserted pre/post; child exit propagates (no
  automatic 0). Banned GIT_DIR/WORK_TREE/INDEX/OBJECT overrides asserted
  absent. Old evidence-20261004 dir is preserved byte-identical; its
  run-00 parent witness was NOT rerun.
- New runs: run-01 (harness-arg abort, guard correctly refused, preserved),
  run-02 (3F+1E first-failure record with full tracebacks, preserved),
  run-03 new 8/8 OK, run-04 affected 14/14 OK — all with in-file
  guard-pre/post, raw stdout/stderr, numeric exit. Subcase count 18
  (2+4+3+6+3) is code-counted, not hand-typed; object counts are
  `verify-pack`/`rev-list` outputs saved in the manifest generator.
- Restore: actual new script + raw log + verification log with full
  (dev,ino) walk (not directory-inode comparison). Counts differ
  legitimately (impl 105 vs restore 103 object files: sidecar layout);
  sharing is 0 pairs either way.
- Scope: synthetic fixtures, offline, no network/live/Actions/Release/PR,
  no reconstruct commit/push, no subagents. Initial 6+14 at 6ffed32 stays
  with 6ffed32; nothing transferred. Whole candidate NOT_READY.
