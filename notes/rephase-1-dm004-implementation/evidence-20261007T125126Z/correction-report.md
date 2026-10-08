# DM-004 correction report (same unit; 6ffed32 preserved, CHANGES_REQUIRED addressed)

Final corrected candidate **`34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4`**,
tree `12161c86d245f8b4140e38ec03202639c4621099`, parent `c4aa3b5`,
chain 34f934e→c4aa3b5→6ffed32→22598f1→d80b5ee→3dc4288→e1705b7, in
`/tmp/opencode/jgas-dm004-impl-20261004T234416Z`, branch
`codex/dm004-release-validate-state`. Same two shipping files only; no
workflow/schema/config/helper edits; four normal new commits on top of 6ff
(c4aa3b5 runtime+tests, 34f934e test-only ×2 — second fixes a residual typo
site); no amend/bypass. Source e170 DBs untouched (verified still e170).

## Blocking F1 fix

`validate-state` now normalizes/contain the State path through existing
helpers BEFORE any byte load and reports the canonical rel:

```python
state_path = core.repo_local_path(
    root, _rel(root, _path(root, args.state), "Production State"),
    "Production State")
...
"state": _rel(root, state_path, "Production State"),
```

`_rel` resolves (symlinks, `..`) and raises repository-local containment;
`repo_local_path` re-validates. Absolute/relative escapes and symlink escapes
reject with `must be repository-local` before `load_json`; ordinary
repo-relative, absolute in-repo and normalized interior `..` still validate.

## Correction→test matrix (all real validators, zero mocks)

| Task item | Test |
|---|---|
| Contain escapes pre-load | `rejects_outside_paths`: absolute-outside, `../` escape, outside-invalid-JSON (containment msg, no `Production State invalid`, no `valid:true`), symlink escape; in-repo bytes unchanged |
| cwd≠root positives | `accepts_from_other_cwd`: rel/abs/normalized-`..`-inside with explicit `--repo-root`/abs `PYTHONPATH`, canonical `state` echoed |
| Whole local block | `closure_block_offline`: unique-step fail-closed extraction (neighbor/live tokens rejected) executed VERBATIM via bash script file with pinned `python`; exact write window added={release-record, core-stage-contract, FROZEN.json} modified={state} removed={} |
| Immediate no-write | negatives snapshot inventory+bytes post-mutation, compare right after CLI BEFORE `finally` repair; positives compare full authority inventories |
| Discriminative errors | drift→`checkpoint release provenance SHA drift`; removed→`Stage Checkpoint artifact drift: release-record`; pending→`expected 'passed'`; schema-parseable→`Production State fails`; malformed/missing→exit 2 WITHOUT semantic prefix |
| Extracted-line failfast | actual `validate-state` line from block vs drifted copy: exit 2, semantic error, sentinel suppressed, authority stable |
| Legacy | replaced weak exit-code test with static rationale lock (legacy `verify_state_basis`/`validate_state_semantics`/0-1 style vs agent-first API; workflow still routes to agent CLI) |

Final: new **8/8 OK** (run-03, 167 s) + affected **14/14 OK** (run-04, 7 s)
via versioned v2 runner with tight env, rc-checked Git reads, worktree-vs-
HEAD-blob pins pre/post, child-exit propagation. First failures preserved:
run-02 (3 failures+1 error: tuple reuse, relative script path) and the
run-01 arg-harness abort (blob-id vs content-sha expected values; guard
correctly refused).

## Packaging

Pack `dm004corr-e1705b7-to-34f934e.pack` (47,825 B, SHA256
`3ba7cb70…34bd`, Git-counted 28 objects: 6 commits/14 trees/8 blobs) +
patch + source copies + machine manifest. New absent all-4 restore
(`restore_dm004corr.sh` + log): actual HEAD/tree/parent/clean, chain to
shallow-774, modes `100644`/blobs/bytes equal, FULL physical walk
(105 vs 103 object files, **0 shared (dev,ino)**).

## Prior-overclaim qualifications (old reports NOT edited)

- Original e170→6ffed32 diffstat is **+394/−0**, not +394/−1 as first reported.
- Prior no-write assertions could hide writes via `finally: restore()`; corrected by pre-repair comparison.
- Prior “whole block” ran a hand-rebuilt argv; corrected by verbatim bash execution.
- Prior guards recorded source hashes without HEAD-blob comparison and returned 0 on test failure; v2 runner pins and propagates.
- run-04@22598f1 affected result stays runtime-identical history, not transferred.

Limits: offline synthetic only; inherited missing blobs/shallow; no live
Actions/Release/PR/production; whole candidate NOT_READY. For Astra +
independent resolution within this same unit.
