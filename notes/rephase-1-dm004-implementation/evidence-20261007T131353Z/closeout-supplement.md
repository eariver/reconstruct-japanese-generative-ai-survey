# DM-004 final closeout supplement (test-only cleanup; 34f934e preserved)

Final candidate **`409b292756dd1277b9dfae87679934c0d2ce251c`**, tree
`8ce3699861505f32d1d60bdc185d4d4f635aedb2`, parent `34f934e`, in
`/tmp/opencode/jgas-dm004-impl-20261004T234416Z`,
`codex/dm004-release-validate-state`. Single normal test-only commit on top
of 34f934e (no amend, no runtime change): runtime blob stays
`4bbf73bfacc25f487d16080afa73f9e0e2c8d612`, workflow blob stays
`de6531d70453dacf9745dae75564020da104420c`.

## Minimal delta (test file only, 3+/22−)

1. Removed `test_legacy_selection_rationale_is_source_grounded`: a pure
   string-grep rationale lock is documentation, not a behavior oracle, and
   does not belong in the accepted suite. The rationale itself is preserved
   below, not as a test.
2. Fail-fast now executes the extracted `validate-state` line UNMODIFIED and
   passes the drifted State via `STATE` in `offline_env` (the actual
   `"$STATE"` env-variable contract), replacing the `.replace()` rebuild.

Result: 7 behavioral methods / 18 subcases, no mocks, no string-grep tests.

## Preserved source-based rationale (ex-test content, kept as prose)

The legacy `survey_production_v2.py validate-state` was not selected because
its contract differs at source level: it calls `verify_state_basis` /
`validate_state_semantics` (initialization-commit pin, global current
contract comparison, legacy checkpoint-attestation rules) and exits 0/1,
while the workflow gate must reuse the shared agent-first
`validate_agent_state` (checkpoint/typed-approval/W1 authority checks) with
exit 0/2. Earlier exit-code comparison on invalid inputs is auxiliary
historical evidence only (see prior evidence-20261004 run-05 log); the
source contrast above is the selection reason. No legacy-suite run required.

## Final oracles (strict v2 runner, new absent paths, tight env)

- run-01 new **7/7 OK** (167 s), run-02 affected **14/14 OK** (7 s) at exact
  409b292; pre/post guards OK (HEAD/tree/clean + worktree-vs-HEAD-blob pins
  for both shipping files, child exits propagated).
- No parent-witness rerun, no full old-suite rerun; 34f934e evidence stands.

## Packaging (new packet, no old overwrite)

- `dm004final-e1705b7-to-409b292.pack` (48,240 B, SHA256
  `e3d94165…02279bf`; Git-counted 32 objects: 7 commits/16 trees/9 blobs —
  every intermediate commit included) + patch (+537/−0) + 2 full source
  copies + machine `final-manifest.json` (+ generator script).
- Fresh absent all-4 hash-gated restore (`restore_dm004final.sh` + raw log):
  actual HEAD/tree/parent/clean, chain to shallow-774, modes/blobs/worktree
  bytes equal, inert remotes, no alternates, full physical walk (109 vs 107
  object files, 0 shared inodes).

## Known limits

Offline synthetic fixtures only; inherited 26,309 missing blobs and
unbundled pinned runtime; no live Actions/Release/PR/production/network;
no agents; no reconstruct commit/push. Whole candidate NOT_READY. Old
runners, scripts, packs and first-failure logs preserved. End of narrowed
correction within this unit.
