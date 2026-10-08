# DM-004 final evidence qualification

- v2 runner reused unchanged from evidence-20261007T125126Z (tight
  allowlist env, rc-checked Git reads, worktree-vs-HEAD-blob pins for both
  shipping files pre/post, child-exit propagation, banned Git overrides
  asserted absent). New absent run dirs run-01/run-02 with in-file
  guard-pre/post, raw stdout/stderr, numeric exit; both `guard_ok:true`.
- New suite is 7 behavioral methods / 18 subcases (code-counted sites:
  2+4+3+6+3 executions); no mocks, no string-grep tests. Affected 14/14
  retain their mock scope as regression-only.
- Counts (7 commits, 32 objects, +537/−0) are `rev-list`/`verify-pack`/
  `diff` outputs captured via the saved generator, not hand-typed.
- Restore literals reference the NEW final (`409b292…`, new pack hash);
  old script/pack/log evidence preserved unmodified in their own dirs.
- Scope: synthetic, offline, NOT_READY; no live/network/agents/production;
  no reconstruct commit/push.
