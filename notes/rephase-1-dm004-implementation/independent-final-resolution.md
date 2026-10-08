# DM-004 independent final resolution — scope fixed 409b292 (read-only, source/evidence-only)

Status: **BOUNDED_PASS** (final test-only cleanup scope; no open findings).
Scope is exactly **`409b292756dd1277b9dfae87679934c0d2ce251c`**,
tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`,
parent `34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4`,
in `/tmp/opencode/jgas-dm004-impl-20261004T234416Z`,
branch `codex/dm004-release-validate-state`.
Packet `notes/rephase-1-dm004-implementation/evidence-20261007T131353Z/`.
No broad audit, no publication/adoption claim.

## 1. Method (no runtime/tests/probes/network/mutations/agents)

- No test execution, probes, network, checkouts, ref/config/source writes, or
  subagents. All Git reads offline with scrubbed env
  `GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file
  PATH=/usr/bin:/bin` via `env -i … git -C <repo> …`.
- Read: `evidence-20261007T131353Z/` (`closeout-supplement.md`,
  `evidence-qualification.md`, `final-manifest.json`, `gen_manifest_final.py`,
  `dm004final-*.pack/.patch`, `restore_dm004final.sh`, `restore.log`,
  `restore-verification.log`, `run-01-final-newmod/` + `run-02-final-affected/`
  guard-pre/post + stdout/stderr/exit, `source-copies/`); live HEAD/tree/
  parent/status/diff/ls-tree/rev-list at fixed HEAD; pack `sha256sum`.
- Only write is this NEW file. Old reviews, root/Worker sources, and prior
  packets untouched. Saved restore script treated as evidence for this exact
  packet, not a certified general reuse tool.

## 2. Exact identity and test-only delta (actual)

- `rev-parse HEAD` = `409b292756dd1277b9dfae87679934c0d2ce251c`,
  `HEAD^{tree}` = `8ce3699861505f32d1d60bdc185d4d4f635aedb2`,
  `HEAD^` = `34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4`,
  `status --porcelain` empty, branch `codex/dm004-release-validate-state`.
- `diff --stat 34f..HEAD`: **1 file, `+3/−22`** —
  `tests/test_survey_dm004_release_validate_state_v2.py` only
  (`diff --numstat`: `3 22`). No runtime/workflow/config change.
- Live `diff 34f..HEAD` confirms exactly the two intended hunks:
  (a) fail-fast executes the extracted line **UNMODIFIED**
  (`f"{validation_line}\n"`, `.replace('$STATE',…)` removed) with drifted
  State passed via `STATE` in `offline_env` (actual `"$STATE"` env contract);
  (b) deletion of `test_legacy_selection_rationale_is_source_grounded`
  (20-line string-grep lock). Nothing else touched.
- `ls-tree -r HEAD`: runtime `100644` blob
  `4bbf73bfacc25f487d16080afa73f9e0e2c8d612` (unchanged from 34f manifest),
  workflow `100644` blob `de6531d70453dacf9745dae75564020da104420c`
  (unchanged), test `100644` blob `f72c12e0d0723956af729291b6757bf22d753346`.
- `rev-list --count e170..HEAD` = 7; `rev-list --objects … | wc -l` = 32,
  matching manifest 32 (7 commits/16 trees/9 blobs).
- Old `34f934e` object present (`cat-file -e` OK) and its
  `evidence-20261007T125126Z/run-03+run-04` 8+14 evidence preserved;
  nothing transferred — final 7+14 stands on its own runs.

## 3. Root cleanup assessment (source-grounded)

- **Removing the static rationale test is correct.** It asserted source
  substrings (`verify_state_basis`, `validate_state_semantics`,
  `return 0 if not errors else 1`, workflow script names) — documentation, not
  a behavior oracle. Its removal leaves 7/7 BEHAVIORAL methods, 18 subcases,
  zero mocks, zero string-grep tests. The source-based legacy rationale is
  retained as prose in `closeout-supplement.md` (§Preserved rationale), which
  is the proper place: selection reason stays reviewable without polluting the
  accepted suite or requiring an unrelated legacy-suite run.
- **Unmodified-line fail-fast is strictly stronger.** Prior 34f rebuilt the
  line via `.replace('$STATE', drifted-rel)`; final runs the exact extracted
  `validation_line` byte-identical with `STATE=drifted-rel` in env, under
  `set -euo pipefail` + trailing `touch sentinel`. Source-copies lines 479-510
  assert exit 2, semantic `checkpoint release provenance SHA drift`, sentinel
  suppressed, inventory + valid bytes stable. This exercises the real
  `"$STATE"` expansion path instead of a Python-substituted reconstruction.
  No `gh`/live content in the line (asserted `NotIn "gh "`).

## 4. Final oracles (persisted strict guards, not log-only)

- `run-01-final-newmod`: new **7/7 OK** (167.039 s, exit 0); `run-02-final-
  affected`: existing controller-5 + checkpoint-9 **14/14 OK** (7.481 s,
  exit 0). Total **7+14=21 success** at exact 409b292.
- Guard files bind the result: pre/post `guard-pre/post.json` record literal
  argv/cwd/pinned 3.12.14 runtime, tight allowlist env, expected HEAD/tree,
  `status=""`, inert `example.invalid` remote, no alternates, and BOTH shipping
  files as worktree-vs-`HEAD:`-blob vs expected content-hash triple pins
  (`match:true`, `guard_ok:true` both sides). v2 runner unchanged from the
  correction packet (rc-checked Git reads, banned `GIT_DIR/WORK_TREE/INDEX/
  OBJECT` overrides asserted absent, child-exit propagation). No parent-witness
  or old-suite rerun, correctly — 34f evidence stands separately.

## 5. Packaging and fresh restore (actual commands/results)

- Pack `dm004final-e1705b7-to-409b292.pack` 48,240 B SHA256
  `e3d941653eadf2459a13f1b85b9fbbffd819f0a0ad6bb77eb121b2cba02279bf`
  (verified `sha256sum` + byte count); manifest machine counts (32/7/16/9)
  match live `rev-list` outputs; generator script saved.
- `restore_dm004final.sh` + `restore.log` + `restore-verification.log`:
  all-4 hash gates OK (b40 archive, successor-20, w1-7, dm004final pack);
  absent destination; `unpack-objects` in order; final/e170/222 present;
  actual `update-ref` + `symbolic-ref` + `reset --hard` to final; clean;
  full chain `409b292→…→e1705b7→222a37e→…→b40→774` with shallow-774
  (`774dd39a951c9ac3818e83dfffd4c7666efb0a20`); both paths modes `100644`,
  blobs, and worktree SHA256/bytes equal (`controller-equal`/`test-equal`);
  source copies match; inert remotes; no alternates; full physical walk
  (impl 109 paths/109 distinct inodes, restore 107/107, **0 shared (dev,ino)**).

## 6. Verdict

**BOUNDED_PASS — no open findings, no correction required** in this narrowed
final scope. F1 containment, verbatim whole-block execution, exact write
window, immediate no-write, discriminative errors, extracted-line fail-fast,
and strict guard/pack/restore disciplines established at 34f are preserved
through a runtime-identical, behavior-only test cleanup. Prior 8+14 (34f) and
6+14 (6ff) results remain historical boundaries, not transferred.

Remaining limitations (unchanged): offline synthetic fixtures only; inherited
26,309 missing blobs + unbundled pinned runtime; no live Actions/Release/PR/
network/production; no full-suite rerun; no reconstruct commit/push. Whole
candidate stays `NOT_READY`. Restore script/pack are evidence for this exact
packet, not a general safe-restore or publication-adoption authority.
