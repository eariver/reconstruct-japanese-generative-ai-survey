# P3S R7 correction report — O4 whitespace-only repair (pre-execution)

2026-10-18. Implements root-selected O4 repair
(`astra-batch-a-resolution-selection.md`) on the R6 candidate. Module
(`7059166e…`) and schema (`4fa61723…`) UNCHANGED — no implementation defect
(per `source-implementation/batch-a-diagnosis-r6.md` §6). Only
`tests/test_survey_editorial_staged_source_v2.py` changed: 141792 B
`0e1cc20f…` → 142747 B `cf2bddd6…`, 2521 → 2535 lines (+14), still 26 test
methods (no method added/removed; no new constant). No imports, no
test/fixture runs in this unit, no network/commit/push; no
`verification-tools/` or root-doc edits. R6 bytes preserved in
`draft-history-r7/prior-bytes-r7/` + `static21-r6-preserved.json`;
R5/R6 reports untouched.

## Corrected new3 identity (measured, read-only sha256sum/stat)

| File | Bytes | Mode | SHA256 |
|---|---|---|---|
| `scripts/survey_editorial_staged_source_v2.py` | 126181 | 0o664 | `7059166e075d1a10aacdd375bb8193881f0bfb2ca3e67dd142e175a349031c65` (unchanged) |
| `schemas/editorial-staged-source-manifest-v2.schema.json` | 5627 | 0o664 | `4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46` (unchanged) |
| `tests/test_survey_editorial_staged_source_v2.py` | 142747 | 0o664 | `cf2bddd6b7b253af069e1ce66bbb9fc901f1ecc8130d7db161c88df3738247ad` |

Module AST-OK (25 defs), test outer AST-OK (49 defs, 26 test methods +
helpers), schema Draft202012Validator.check_schema OK. Every embedded child
program AST-OK via literal-eval + `ast.parse` (no fixture execution):
`_P3S_MATERIALIZE_SCRIPT` 1120 (`55884c2b…`), `_P3S_VERIFY_SCRIPT` 729
(`2497eb0f…`), `_P3S_FAULT_SCRIPT` 11997 (`a6ecf378…`),
`_R1_FIXTURE_PREPARE_SCRIPT` 3473 (`5f469984…`) — all four byte-identical
R6→R7. No `...[truncated` markers; single `__main__` only. Status 105 rows
(3M + 18A + 84 pyc).

## Evidence-transfer body hashes (R6→R7, scoped)

AST-body (`ast.dump`, `include_attributes=False`) comparison R6 prior vs R7
current (49 funcs each):

- CHANGED exactly 1: `EditorialStagedSourceV2Tests.test_o4_live_state_mutation_replay_ok_materializer_refuses`
  `b5909575970f` → `5acd8ad70cc7`.
- All other 48 funcs IDENTICAL, including O1/O2/O3/O5/O6a/O6b/O7/O8/O9 and
  all 24 shared helpers (`_lf_prepare`, `_weekly_prepare`,
  `_weekly_prepare_from`, `_capture`, `_scope_for`, `_materialize`,
  `_verify`, `_retamper_manifest`, `_snapshot`, `_assert_no_write`,
  `_assert_no_write_except`, `_assert_owned_delta_only`,
  `_run_p3s_fixture`, `_launch_durable_child`, `_durable_base`,
  `_make_p3s_source_root`, `_copy_base`, `_run_fixture_code`,
  `_commit_r1_nonemitted_comment`, `_run_git`, `_fresh_lf_root`,
  `_fault_run`; full verified list equal).

Module/schema bodies unchanged (`diff -q` identical). R6 O3 success stays
bound to R6; transfer qualification (scoped) is for root selection, not
claimed here — no new runtime PASS claimed in this unit.

## O4 repair detail (prescribed test-only)

Replaced semantic extra-key mutation:

```python
live_state = core.load_json(prep["state_path"])
live_state["p3s_artifact_probe"] = "mutable non-KEEP live change"
core.write_json(prep["state_path"], live_state)
```

with whitespace-only byte drift (P2V B1 precedent):

```python
snap_clean = _snapshot(root)
orig_state_bytes = prep["state_path"].read_bytes()
orig_state_parsed = core.load_json(prep["state_path"])
orig_state_sha = core.sha256_bytes(orig_state_bytes)
prep["state_path"].write_bytes(orig_state_bytes + b"\n")
drifted_bytes = prep["state_path"].read_bytes()
# assert parsed equality + sha inequality + exact trailing-newline
```

Retained: `snap = _snapshot(root)` after injection, replay `_verify` +
immediate fault-present `_assert_no_write`, writer `_run_p3s_fixture`
materialize, exact `PIN_FAILED/PIN/REFUSED_PRE_WRITE` + `REF_DRIFT`,
plus new prescribed guards — `state_ref` in error (stale State ref is the
earlier intended refusal), `STAGED_ROOT_EXISTS` absent (existing output root
is not the reason), drift bytes present at refusal, fault-present no-write,
then `write_bytes(orig_state_bytes)` restore + original-bytes equality +
`_assert_no_write(snap_clean, …, "o4 restored")`. Whitespace keeps
`validate_agent_state` passing and layout passing, so
`_prepin_known_live_refs` `live.pinned(state_ref)` fails with `REF_DRIFT`
wrapped as `PIN_FAILED` — the intended prepin seam. No module/schema change.

## Static21 / caches (NEW, read-only)

`draft-history-r7/static21.json` 3670 B `b0ba134a…`: canonical flat JSON
(outer sorted, inner `sha256/bytes/mode`), exact 21 entries (18 inherited +
3 new). New3: module `7059166e…` 126181 B, test `cf2bddd6…` 142747 B,
schema `4fa61723…` 5627 B, all `0o664`. Inherited18 18/18 match
`expected18-source-correction-v5.json`; 84 caches 84/84 match
`cache-inventory-static.json`; 0 mismatches, no baselining.

## Remaining concerns (no execution in this unit; for root selection)

- Same as R6 § “Remaining concerns” preserved; additionally O4 restore
  relies on `write_bytes` truncating in place (inode-preserving) so
  `snap_clean` equality holds — matches O6b `write_bytes(original)` +
  `_assert_no_write(snap, …, "restored")` precedent, but runtime proof
  awaits the single authorized remainder batch.
- No execution PASS claimed: all 26 methods unaudited at runtime post-edit;
  R6 batch-A O3 success + O4 failure preserved in
  `smoke-r6-batch-a-20261018T083224Z/`; a qualified scoped remainder (O4–O9
  without O3) is for root selection, not claimed here.
