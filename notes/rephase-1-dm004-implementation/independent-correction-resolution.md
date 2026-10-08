# DM-004 independent correction resolution — scope fixed 34f934e (read-only)

Status: **BOUNDED_PASS** (correction scope only; no generic/full-history/publication approval).
Scope is exactly final corrected candidate
**`34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4`**,
tree `12161c86d245f8b4140e38ec03202639c4621099`,
parent `c4aa3b510c4137bd636431f4eca2732b77d4b152`,
chain `34f934e→c4aa3b5→6ffed32→22598f1→d80b5ee→3dc4288→e1705b7`
in `/tmp/opencode/jgas-dm004-impl-20261004T234416Z`,
branch `codex/dm004-release-validate-state`.
Old `6ffed32` preserved (`cat-file -e` succeeds); old packet/reports untouched.

## 1. Independence and method

- Did not author code/tests/design; no agents, no runtime tests/probes,
  no network, no ref/checkout operations, no Worker/root/source/old-review edits.
- All Git reads offline with scrubbed env
  `GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file PATH=/usr/bin:/bin`
  via `env -i … git -C <repo> …`. No worktree mutation.
- Read: `correction-task.md`; new packet `evidence-20261007T125126Z/`
  (`correction-report.md`, `evidence-qualification.md`,
  `correction-manifest.json`, `run_dm004_v2.py` vs preserved `run_dm004.py`,
  `gen_manifest_final.py`, `dm004corr-*.pack/.patch`, `restore_dm004corr.sh`,
  `restore.log`, `restore-verification.log`, `run-01…run-04/` guards/logs,
  `source-copies/` controller + test); live `diff`/`rev-parse`/`ls-tree`/
  `rev-list` at fixed HEAD. Only write is this NEW file.

## 2. Exact identity (actual, not reported-only)

- `HEAD=34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4`,
  `HEAD^{tree}=12161c86d245f8b4140e38ec03202639c4621099`,
  `HEAD^=c4aa3b510c4137bd636431f4eca2732b77d4b152`,
  `status` empty, branch `codex/dm004-release-validate-state`,
  origin `https://example.invalid/…` inert.
- `rev-list --count e170..HEAD` = 6; `rev-list --objects` count = 28,
  matching manifest 28 (6 commits/14 trees/8 blobs).
- `diff --stat e170..HEAD`: 2 files `+556` total
  (controller +23, new test 533 lines); `6ff..HEAD` controller hunk is exactly
  the 4-line containment + 1-line canonical-report change (see §3).
- `ls-tree HEAD`: controller `100644` blob
  `4bbf73bfacc25f487d16080afa73f9e0e2c8d612` (worktree SHA256
  `278dc404…`, 124636 B); test `100644` blob
  `6b73abda6b7d452030ca008587c20eb755b3dd5e` (SHA256 `a9931c0b…`,
  26687 B); workflow blob `de6531d70453dacf9745dae75564020da104420c`
  unchanged. Matches manifest/patch/restore logs.
- Pack `dm004corr-e1705b7-to-34f934e.pack` 47,825 B SHA256
  `3ba7cb708e0f0a17c01e070f829366cfae6a57a262d8e88fc0d65e65eeac34bd`
  (verified `sha256sum`); 6-commit chain includes 4 old + 2 correction commits
  (`c4aa3b5` runtime+tests, `34f934e` test-only typo fixes).

## 3. F1 fix — before-load containment + canonical rel (source-verified)

Controller `source-copies/survey_agent_control_v2.py:2362-2380`:

```python
state_path = core.repo_local_path(
    root,
    _rel(root, _path(root, args.state), "Production State"),
    "Production State")
state = core.load_json(state_path)   # after containment
…
"state": _rel(root, state_path, "Production State"),
```

`_rel` resolves (`..`, symlinks) and raises `must be repository-local` on
escape; `repo_local_path` re-validates. Both load and report go through
helpers before any byte read — the exact task §Runtime remedy. Ordinary
repo-relative, absolute in-repo, and normalized interior `..` remain supported.

- **4 escape controls** (`test_validate_state_rejects_outside_paths`, 4 subcases,
  sibling under `/tmp/opencode/dm004-escape-ESC`, no source overwrite):
  absolute-outside, repo-relative `../` escape, outside-invalid-JSON
  (asserts containment message, explicitly `NotIn "Production State invalid"` —
  proves early boundary vs later parser), symlink-in-repo→outside. All require
  exit 2 + `must be repository-local` + no `valid:true`; in-repo bytes unchanged.
- **cwd≠root proper imports** (`accepts_from_other_cwd`, 3 subcases):
  cwd sibling `/tmp/opencode/dm004-escape-CWD`, absolute controller path +
  absolute `--repo-root` + absolute `PYTHONPATH=ROOT`; rel/abs/normalized-`..`-
  inside all exit 0 with canonical `"state": rel`. Proves no false import failure.
- **Generic API preserved** (`generic_cli_accepts…`): real FROZEN exit 0 +
  real RELEASED/COMPLETE exit 0 with canonical `state` echo and full
  authority-inventory stability (not State-bytes-only).

## 4. ROOT additional oracle gaps — all addressed in true code

- **Whole block verbatim:** `locate_closure_block()` requires the named step
  exactly once, a following step boundary, exactly one `run: |`, `set -euo
  pipefail`, one heredoc, one `validate-state`, exact argv tokens, and rejects
  neighbor/live content (`gh release/pr/api`, `git push/switch/config`,
  `actions/checkout`, `setup-python`, `GITHUB_OUTPUT`, adjacent Release/PR step
  names). Test writes the extracted `block` to a script file and runs
  `["bash", script]` with pinned-python PATH + allow-listed offline env —
  actual whole-block execution, not heredoc+2 hand-built argv.
- **Exact write window:** pre/post `inventory([src,survey])` diff asserts
  `added={release-record, core-stage-contract-v2.json, FROZEN.json}`,
  `modified={production-state.json}`, `removed={}`, plus final
  RELEASED/COMPLETE, `release=passed`, provenance path/sha binding, shared
  validator clean. Proves selected synthetic closure only.
- **Immediate no-write:** negatives capture `pre_inv`/`pre_state` post-mutation
  pre-CLI, then assert `inventory==pre_inv` and `post_state==pre_state`
  immediately AFTER CLI and BEFORE `finally: restore()`. Positives/contract-
  refusals likewise compare full inventories. Fixture repair stays in `finally`
  for the next case only.
- **Distinctive errors:** drift→`checkpoint release provenance SHA drift`;
  removed-record→`Stage Checkpoint artifact drift: release-record`;
  pending-on-RELEASED→`expected 'passed'`; schema-parseable→
  `Production State fails`; malformed/missing→exit 2 WITHOUT `Production State
  invalid` prefix. Setup/schema/parser families cannot masquerade as semantic
  refusal. Unknown-command/missing-arg/extra-flag refusals stay separate.
- **Extracted-line failfast:** uses the actual `validation_line` from the block
  (asserted `validate-state`, no `gh `) with `$STATE`→drifted copy under
  `set -euo pipefail` + trailing `touch sentinel`: exit 2, semantic SHA-drift
  error, sentinel suppressed, inventory + valid bytes stable. Semantic, not
  parse-only; no real PR step.
- **No mocks:** new file has no `mock` import; all authority oracles use real
  `SpecialFixture`/validators/builders/CLIs. Affected controller-5 +
  checkpoint-9 retain their mock scope as regression-only. Legacy weak
  exit-code test replaced by static rationale lock (legacy
  `verify_state_basis`/`validate_state_semantics`/0-1 style vs agent-first
  `validate_agent_state`; workflow still routes to agent CLI).

## 5. v2 runner + final 8+14=22 green (persisted, strict)

- `run_dm004_v2.py` (old runner unchanged): tight allowlist env
  (PATH=pinned-interpreter-dir, PYTHONPATH, BYTECODE, 3 GIT_*, HOME only;
  asserts banned `GIT_DIR/WORK_TREE/INDEX/OBJECT/ALTERNATE` absent); every Git
  read asserts rc==0; both shipping files compare worktree-SHA256 vs
  `git show HEAD:path` bytes vs expected content-hash pre AND post;
  HEAD/tree/clean/no-alternates asserted; child exit propagates (no auto-0);
  absent run dirs; `guard-pre/post.json` + raw stdout/stderr/numeric exit.
- Final: `run-03` new **8/8 OK** (167 s, exit 0, pre/post `guard_ok:true`,
  blob pins match) + `run-04` affected **14/14 OK** (7 s, same guards).
  Subcases 18 code-counted. Initial 6+14 at 6ff stays with 6ff; nothing
  transferred.
- Preserved strictness/failure evidence: `run-01` harness-arg abort
  (`ABORTED-DRIFT`, `guard_ok:false` — blob-ID vs content-SHA expected values
  correctly refused, not executed); `run-02` 3F+1E first-failure
  (released-tuple reuse + relative cwd script path) with full tracebacks;
  corrected by `c4aa3b5/34f934e`.

## 6. Pack + fresh all-4 restore (actual commands/results saved)

- `restore_dm004corr.sh` + `restore.log` + `restore-verification.log`:
  4 hash gates (b40 archive, successor-20, w1-7, dm004corr pack) OK;
  absent destination; `unpack-objects` in order; `cat-file -e` final/e170/222;
  actual `update-ref` + `symbolic-ref` + `reset --hard` to final; clean;
  full chain to shallow-774 (`774dd39…`); changed-file modes/blobs/worktree
  bytes equal (`controller-equal`/`test-equal`); no alternates; inert remotes.
- Full physical walk (not directory-inode sampling): impl 105 paths/105
  distinct inodes, restore 103/103, **0 shared (dev,ino) pairs** —
  `FULL-PHYSICAL-NO-SHARING-PROVEN`. Count asymmetry is sidecar layout, not
  sharing. Stale-parent refs not accepted.

## 7. Prior-review overclaim qualifications (old review NOT edited)

Prior `independent-implementation-review.md` overstated two points, judged on
true old code:

- Called old negative `finally: restore()` + final equality “no-write proof.”
  True old code (`evidence-20261004` test lines ~244/287) overwrote
  State/checkpoint/record in `finally` BEFORE the final byte asserts, which
  could hide CLI writes. Corrected here by immediate post-CLI inventory/state
  comparison (§4).
- Called old heredoc-split + manually rebuilt two CLI argv “actual full step.”
  True old code (lines ~296/310-323) extracted only the heredoc and hand-copied
  the checkpoint/validation argv. Corrected here by verbatim bash-script
  execution of the whole extracted block (§4).

Old 6ff report also misstated diffstat `+394/-1` (actual `+394/-0`) and recorded
source hashes without HEAD-blob comparison while returning 0 on child failure;
both qualified in the correction report and fixed by the v2 runner. These
qualifications do not retroactively pass 6ff; 6ff remains CHANGES_REQUIRED
history with its own 6+14 boundary.

## 8. Verdict and remaining limitations

**BOUNDED_PASS** for the correction scope: F1 containment + all six ROOT oracle/
runner/pack gaps are implemented in source and evidenced by final 8+14 with
strict persisted guards and a fresh hash-gated restore. Reports correctly bound
6ff as history and state exact new-acceptance boundaries.

Remaining limitations (no new work started): offline synthetic fixtures only;
inherited missing-blob/shallow-774 limits; no live Actions/Release/PR/network/
production; no full-suite rerun; no reconstruct commit/push; no publication or
generic safe-script/full-history claim. Saved runners/scripts are evidence, not
certified rerun tools. Whole candidate remains `NOT_READY`; stop at Human
Commit Point.
