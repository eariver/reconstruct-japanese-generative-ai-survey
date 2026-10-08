# DM-004 evidence qualification (mandatory)

- Guard discipline: new saved runner `run_dm004.py` wrote literal argv/cwd/
  runtime/env + fresh expected-HEAD/tree/source-hash/clean assertions to
  `guard-pre.json` BEFORE and `guard-post.json` AFTER every run (00–06),
  with raw `stdout.log`/`stderr.log`/`exit` files. Pre/post guards all OK;
  runner aborts (exit 3) on drift. Nothing is session-only.
- Run identity: run-00 parent witness at e170 (exit 2 argparse, not import
  error). run-01/02 are first-failure records at 3dc4288/d80b5ee with full
  tracebacks, preserved unmodified. run-03 new 6/6 at 22598f1 (superseded
  only by the 1-line typo fix). run-05 new 6/6 + run-06 affected 14/14 are
  the final oracles at 6ffed32/c3d6ad6. run-04 affected 14/14 at 22598f1
  (runtime identical to final; only the new-test file changed after).
- Fixture honesty: all new authority oracles use REAL validators; no
  authority/Git success mocks in new cases (grep-verifiable: no `mock`
  import). Old checkpoint tests keep their mocks and are labeled affected-
  only. Mutations restored from saved snapshot bytes per subcase; final
  bytes re-asserted; worktree clean pre/post every run.
- Restoration: actual `restore_dm004.sh` + `restore.log` +
  `restore-verification.log` saved (not later-manifest-only). Hash gates
  for all 4 inputs passed; absent-destination; actual HEAD switch;
  clean/chain/mode/blob/inode checks observed, not transcribed.
- Scope: synthetic SpecialFixture content; offline; inherited missing blobs
  and shallow-at-774 remain disclosed. No live Actions/Release/PR, no
  reconstruct commit/push, no subagents.
