# P3S R10 correction report — seven-method test-only correction (pre-execution)

2026-10-18. Implements root-selected seven-method correction
(`astra-seven-correction-selection.md`; diagnosis
`source-implementation/batch-d-diagnosis-r9.md` overridden for O11c per
selection) on the R9 candidate. Module (`7059166e…`) and schema
(`4fa61723…`) FROZEN — no implementation defect per diagnoses. Only
`tests/test_survey_editorial_staged_source_v2.py` changed: 144928 B
`b9f41323…` → 147930 B `6b6bd1f0…`, 2572 → 2628 lines (+56), still 26 test
methods (no method added/removed; no new constant beyond observer counter
fields in fault outcome). No imports, no test/fixture runs in this unit, no
network/commit/push; no `verification-tools/` or root-doc edits. R9 bytes
preserved in `draft-history-r10/prior-bytes-r10/` +
`static21-r9-preserved.json`; R5–R9 reports untouched.

Tool-adapter record:
- Previous `apply_patch`-literal turn returned blocked with NO work/run;
  recorded in R9 report and carried forward in R10 README. This turn uses
  AVAILABLE dedicated `Edit`/`Write` per clarification (not shell
  `apply_patch`/shell rewrites). Preservation via archival `cp -a`; all
  source edits via dedicated `Edit`; new artifacts via `Write`.

## Corrected new3 identity (measured, read-only sha256sum/stat)

| File | Bytes | Mode | SHA256 |
|---|---|---|---|
| `scripts/survey_editorial_staged_source_v2.py` | 126181 | 0o664 | `7059166e075d1a10aacdd375bb8193881f0bfb2ca3e67dd142e175a349031c65` (frozen) |
| `schemas/editorial-staged-source-manifest-v2.schema.json` | 5627 | 0o664 | `4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46` (frozen) |
| `tests/test_survey_editorial_staged_source_v2.py` | 147930 | 0o664 | `6b6bd1f0cd02bf0ae60e8f1a1fb6a88e6185f90cfd2442ed265ce0973accaba0` |

Module AST-OK (25 defs), test outer AST-OK (49 defs, 26 test methods +
helpers), schema Draft202012Validator.check_schema OK. Embedded child
programs via literal-eval + `ast.parse` (no fixture execution):
`_P3S_MATERIALIZE_SCRIPT` 1120 (`55884c2b…`) unchanged,
`_P3S_VERIFY_SCRIPT` 729 (`2497eb0fae67…`) unchanged,
`_P3S_FAULT_SCRIPT` 11997 (`a6ecf378…`) → 13343 (`2b7d0586…`) — required
observer/second-P2V wrapping + `observer_calls` outcome (see below),
`_R1_FIXTURE_PREPARE_SCRIPT` 3473 (`5f469984…`) unchanged. No
`...[truncated` markers; single `__main__` only. Status 105 rows
(3M + 18A + 84 pyc).

## Evidence-transfer body hashes (R9→R10, scoped)

Top-level `ast.dump` (`include_attributes=False`) comparison R9 prior vs R10
current (49 funcs + 4 script constants):

- CHANGED exactly 9 nodes: 6 test methods + R1 helper + fault script + class
  aggregate (class changes only via its 6 changed methods):
  - `test_o9_alias_fifo_no_read` `533f36380fab→7ef934fbdfea` (timeout bool)
  - `test_o10_same_inode_vs_new_inode` `e80073e8ba0b→a52537115537` (differing byte+inode)
  - `test_o11b_midcall_reader_drift` `8c953325ca4a→513a29e690b2` (first-P2V doc + observer_calls==1)
  - `test_o11c_late_control_retained` `ab9f7c33bb56→234e1b82daa3` (FINAL owned5+probe, observer_calls==2)
  - `test_o11e_post_readback_replay` `d9a80440c810→1c59fb866f2d` (SNAPSHOT_FAILED + nested FILE_REPLACED)
  - `test_o11f_root_ancestor_replace` `7b40adc45e2e→053221a66056` (branch codes)
  - `_commit_r1_nonemitted_comment` `2a965ae15e28→a048c90c8a9d` (allowed derivation path)
  - `_P3S_FAULT_SCRIPT` `8488fdcb6248→4ebd89328282` (observer first/second return, outcome observer_calls, restore)
  - `EditorialStagedSourceV2Tests` aggregate `0e0eb6299563→6f96ef68cd04` (only via above 6 methods)
- All other 41 funcs + 3 script constants IDENTICAL, including O1/O2/O3/O4/
  O5/O6a/O6b/O7/O8/O11/O11d/O12a-f/O13/O14 and 24 shared helpers.
- `_R1_FIXTURE_PREPARE_SCRIPT` byte-identical R9→R10 (real same-chain refresh
  preserved; only helper target changed, not the prepare script).

Module/schema bodies unchanged (`diff -q` identical). Fault-script change is
shared by fault-using methods (O11/O11d/O12a-f among 19 prior successes);
their prior passes stay bound to old pins — NO false full26 transfer claimed.
R1 helper change recorded separately from unchanged 19 methods/shared helpers;
no old R1 pass claimed. Batch-E 8 passes (O12a-f/O13/O14) stay bound to R9 pin.

## Seven repairs detail (prescribed test-only, actual APIs inspected)

1. O9 FIFO: `assertNotIn("timeout", json.dumps(outcome))` → `assertFalse(outcome.get("timeout"))`.
   `_run_p3s_fixture` always sets `timeout=False` non-timeout vs `True` on real
   timeout (`938-977`); substring can never pass. Keep `LAYOUT_REFUSED/PIN/`
   `REFUSED_PRE_WRITE` + regex + fault-present no-write. No hang reclassified.
2. O10: differing first byte (`X` if `%` else `%`), `snap_before` pre-write,
   `assertNotEqual bytes` + `assertEqual dev/ino` before verifier. Keep
   `REPLAY_MISMATCH/REPLAY/INVALID` + no-write. Restores + same-byte/new-inode
   positive unchanged.
3. O11b: fault calls genuine first P2V then injects (observer wrapper count1);
   never manufactures authority. Test asserts `fired==1`, `observer_calls==1`,
   `STABILITY_VIOLATION/PRE_WRITE/REFUSED_PRE_WRITE`, exact drift bytes,
   `allowed_changed={reader_rel}` no-new-output. Layout/prepin/first-P2V pass
   with originals; use-check `894-904` sees drift. Never broaden to LAYOUT_REFUSED.
4. O11c (selection override, NOT diagnosis preclaim): inject immediately AFTER
   SECOND REAL P2V return. Both observations genuine/successful. Expect
   `ORIGINAL_DRIFT/FINAL/INDETERMINATE_INVOCATION`, full owned 4-file+root set
   PLUS precisely the known injection (`owned5|{probe}` / `owned5|{retained-dir}`),
   originals otherwise identical. Assert `observer_calls==2` + timing (owned
   outputs prove CLAIM/MANIFEST/REPLAY/OBSERVE2 passed before FINAL).
   Existing O11d covers post-render/preclaim; no duplicate weaker timing.
5. O11e samebyte: outer `FILE_REPLACED` → `SNAPSHOT_FAILED` + `assertIn("FILE_REPLACED")`;
   keep `FINAL/INDETERMINATE` + owned4 complete-bytes + no leftovers. First
   subcase (`REPLAY_UNVERIFIED/REPLAY`) unchanged (field success, not method pass).
6. O11f branch: `root-replace→STAGED_ROOT_REPLACED`, `ancestor-replace→
   STAGED_ROOT_ENTRY_FAILED` (+ `assertIn symlink`), both `CLAIM/OWNED_PARTIAL`
   + exact deltas/injection-bytes/unchanged-originals. Real-dir pass is field
   success, not method pass.
7. R1: helper target `survey_weekly_mechanical_refresh_v2.py` → actual allowed
   `scripts/survey_weekly_derivation_v2.py` (`ALLOWED_CHANGED_PATH`), pure
   `# fixture R1 non-emitted Python comment` above `def build_reader_input(`,
   AST-equal retained, `git add` allowed path, committed fixture code SAME
   State/active receipt chain into P3S via unchanged `_R1_FIXTURE_PREPARE_SCRIPT`.
   Never relax refresh allowlist or runtime source. No old R1 pass claimed.

## Static21 / caches (NEW, read-only)

`draft-history-r10/static21.json` 3670 B `67978bc2…`: canonical flat JSON
(outer sorted, inner `sha256/bytes/mode`), exact 21 entries (18 inherited +
3 new). New3: module `7059166e…` 126181 B, test `6b6bd1f0…` 147930 B,
schema `4fa61723…` 5627 B, all `0o664`. Inherited18 18/18 match
`expected18-source-correction-v5.json`; 84 caches 84/84 match
`cache-inventory-static.json`; 0 mismatches, no baselining.

## Remaining concerns (no execution in this unit; for root selection)

- Fault-script observer wrapping is shared; prior fault-using successes
  (O11/O11d/O12a-f etc. among 19) do NOT transfer to R10 pin — scoped
  diagnostic only.
- O11c FINAL expectation `ORIGINAL_DRIFT` subject to exact current helper code
  (selection wording); if helper maps differently, return raw for diagnosis —
  no oracle relaxation in this unit.
- No execution PASS claimed: all 26 methods unaudited at runtime post-edit;
  R9 batch-D (3 pass/6 fail) + batch-E (8 pass/1 fail) preserved; qualified
  scoped remainder (O9/O10/O11b/O11c/O11e/O11f/R1) is for root selection.
