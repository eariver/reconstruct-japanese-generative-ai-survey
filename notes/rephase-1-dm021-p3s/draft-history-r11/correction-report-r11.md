# P3S R11 correction report — R1 fixture-script only (pre-execution)

2026-10-18. Implements root-selected R1 fixture repair
(`astra-r1-fixture-resolution-selection.md`; R10 batch-F 6/7 pass, R1 failed
after genuine refresh) on the R10 candidate. Module (`7059166e…`) and schema
(`4fa61723…`) FROZEN. All 26 test methods FROZEN. Only
`_R1_FIXTURE_PREPARE_SCRIPT` string changed in
`tests/test_survey_editorial_staged_source_v2.py`: 147930 B `6b6bd1f0…` →
147845 B `a3bb0f23…`, 2628 → 2622 lines (-6 net: stub removal). No method
bodies, no other helpers/constants, no imports, no test/fixture runs in this
unit, no network/commit/push; no `verification-tools/` or root-doc edits.
R10 bytes preserved in `draft-history-r11/prior-bytes-r11/` +
`static21-r10-preserved.json`; R5–R10 reports untouched.

Tool-adapter: AVAILABLE dedicated `Edit`/`Write` used (no shell
`apply_patch`/shell rewrites for candidate edit). Preservation via archival
`cp -a`; new artifacts via `Write`.

## Corrected new3 identity (measured, read-only sha256sum/stat)

| File | Bytes | Mode | SHA256 |
|---|---|---|---|
| `scripts/survey_editorial_staged_source_v2.py` | 126181 | 0o664 | `7059166e075d1a10aacdd375bb8193881f0bfb2ca3e67dd142e175a349031c65` (frozen) |
| `schemas/editorial-staged-source-manifest-v2.schema.json` | 5627 | 0o664 | `4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46` (frozen) |
| `tests/test_survey_editorial_staged_source_v2.py` | 147845 | 0o664 | `a3bb0f2369ffc131e8ad645759105d165a62fa114e9b4088a2497e4a13dfa036` |

Module AST-OK (25 defs), test outer AST-OK (49 defs, 26 methods + helpers),
schema Draft202012Validator.check_schema OK. Embedded scripts via
literal-eval + `ast.parse`: `_P3S_MATERIALIZE_SCRIPT` 1120 (`55884c2b…`)
unchanged, `_P3S_VERIFY_SCRIPT` 729 (`2497eb0fae67…`) unchanged,
`_P3S_FAULT_SCRIPT` 13343 (`2b7d0586…`) unchanged R10→R11,
`_R1_FIXTURE_PREPARE_SCRIPT` 3473 (`5f469984…`) → 3388 (`11da8e5f…`) — ONLY
change (see below). No `...[truncated`; single `__main__`. Status 105 rows.

## Evidence-transfer body hashes (R10→R11, scoped)

Top-level `ast.dump` R10 prior vs R11 current (49 funcs + 4 script constants):

- CHANGED exactly 1: `_R1_FIXTURE_PREPARE_SCRIPT` `44b0e988743a→1e9fa71a945a`.
- All 49 funcs IDENTICAL (all 26 methods incl. O9/O10/O11b/O11c/O11e/O11f/R1
  bodies, all 24 shared helpers, `_commit_r1_nonemitted_comment`), other 3
  script constants IDENTICAL. Class aggregate unchanged (no method changed).
- R10 fault-script observer wrapper preserved byte-identical; its effect on
  fault-using prior successes (O11/O11d/O12a-f among 19) stays bound to old
  pins — NO full26 transfer. R10 batch-F 6 passes stay bound to R10.

## R1 fixture repair detail (prescribed test-only, saved raw root-caused)

Saved `p3s-fixture-code-nwfqxli6/child.script.py:28-32` took `snap0` BEFORE
`_stage_authoring_before_prepare:29`, then `prepare:30`, then no-write:32 —
intentional staging falsely attributed to prepare. It also used P1 file-only
`_snapshot:60` while expected capture delta:61 includes directories —
second guaranteed mismatch. Both are fixture oracle defects, not runtime.

Repaired script (ONLY change):
- Stage authored input FIRST via real `p1t._stage_authoring_before_prepare`
  with real `unittest.TestCase` (`_TC/runTest`), then raw-safe snapshot
  immediately before actual prepare: `snap0 = _p3s_snapshot(root)` (fixture
  committed P3S `_snapshot`, file+dir, `__pycache__`-excluded).
- `prepared = proposal_mod.prepare_proposal(...)` (real, read-only per P1
  docstring), then `_p3s_assert_no_write(tc, snap0, _p3s_snapshot(root))`.
- Real `unittest.TestCase` (`_TC`) replaces hand-written `_Asserts` stub
  (preferred per selection); all asserts via `tc.assertEqual/True`.
- Capture/verify: real `proposal_mod.validate_proposal`,
  `retention.capture_retention/verify_retention`, `p1t._scope_review_for`;
  `snap1 = _p3s_snapshot(root)`, `before=dict(snap1)`, `after=_p3s_snapshot`,
  `assertEqual(set(after)-set(before), new_files|new_dirs)`,
  `_p3s_assert_no_write_except(tc, before, after, new_files|new_dirs, set())`
  — exact planned COPY/manifest ancestor delta + unchanged originals with
  directories. SAME refreshed State/chain, no P1/current-authority bypass.

## Static21 / caches (NEW, read-only)

`draft-history-r11/static21.json` 3670 B `1c0e339c…`: canonical flat JSON,
exact 21 entries. New3: module `7059166e…` 126181 B, test `a3bb0f23…`
147845 B, schema `4fa61723…` 5627 B, all `0o664`. Inherited18 18/18 match
`expected18-source-correction-v5.json`; 84 caches 84/84 match
`cache-inventory-static.json`; 0 mismatches.

## Remaining concerns

- No execution PASS claimed post-edit; R10 batch-F 6/7 + prior 19 stay bound
  to old pins; qualified 7-method remainder (R1/O11d/O12b-f) is for root
  selection. Fault-script shared-wrapper transfer qualification preserved.
