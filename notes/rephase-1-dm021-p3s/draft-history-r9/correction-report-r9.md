# P3S R9 correction report — O8 contract-identity expectation only (pre-execution)

2026-10-18. Implements root-selected O8 correction
(`astra-replay-fault-batch-selection.md`) on the R8 candidate. Module
(`7059166e…`) and schema (`4fa61723…`) UNCHANGED — selected full-field
binding, not runtime bug. Only `tests/test_survey_editorial_staged_source_v2.py`
changed: 144795 B `955f6fb5…` → 144928 B `b9f41323…`, 2570 → 2572 lines (+2
comment), still 26 test methods (no method added/removed; no new constant).
No imports, no test/fixture runs in this unit, no network/commit/push; no
`verification-tools/` or root-doc edits. R8 bytes preserved in
`draft-history-r9/prior-bytes-r9/` + `static21-r8-preserved.json`;
R5–R8 reports untouched.

Tool-adapter record:
- Previous turn blocked: harness exposes dedicated `Edit`/`Write` but no
  tool literally named `apply_patch`; agent returned explicit availability
  with NO work/run (no R9, no edit, no batch), no shell `apply_patch`.
- This turn root clarified to use AVAILABLE dedicated `Edit`/`Write` (not
  shell `apply_patch`/shell rewrites). O8 edit used dedicated `Edit` only;
  preservation used archival `cp -a` byte copies; new artifacts via `Write`.

## Corrected new3 identity (measured, read-only sha256sum/stat)

| File | Bytes | Mode | SHA256 |
|---|---|---|---|
| `scripts/survey_editorial_staged_source_v2.py` | 126181 | 0o664 | `7059166e075d1a10aacdd375bb8193881f0bfb2ca3e67dd142e175a349031c65` (unchanged) |
| `schemas/editorial-staged-source-manifest-v2.schema.json` | 5627 | 0o664 | `4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46` (unchanged) |
| `tests/test_survey_editorial_staged_source_v2.py` | 144928 | 0o664 | `b9f413234dcc4230be1dcc7865d649efcbadca284dde37e6d9284aa3f43c5604` |

Module AST-OK (25 defs), test outer AST-OK (49 defs, 26 test methods +
helpers), schema Draft202012Validator.check_schema OK. Every embedded child
program AST-OK via literal-eval + `ast.parse` (no fixture execution):
`_P3S_MATERIALIZE_SCRIPT` 1120 (`55884c2b…`), `_P3S_VERIFY_SCRIPT` 729
(`2497eb0fae67…`), `_P3S_FAULT_SCRIPT` 11997 (`a6ecf378…`),
`_R1_FIXTURE_PREPARE_SCRIPT` 3473 (`5f469984…`) — all four byte-identical
R8→R9. No `...[truncated` markers; single `__main__` only. Status 105 rows
(3M + 18A + 84 pyc).

## Evidence-transfer body hashes (R8→R9, scoped)

AST-body (`ast.dump`, `include_attributes=False`) comparison R8 prior vs R9
current (49 funcs each):

- CHANGED exactly 1: `EditorialStagedSourceV2Tests.test_o8_path_ref_schema_inventory_tamper`
  `645b2aca4efb` → `5299ec184df9`.
- All other 48 funcs IDENTICAL, including O1/O2/O3/O4/O5/O6a/O6b/O7/O9/O10/
  O11/O11b/O11c/O11d/O11e/O11f and all 24 shared helpers.

Module/schema bodies unchanged (`diff -q` identical). R8 O7 success + R7
O4–O6b successes stay bound to their pins; transfer qualification (scoped)
is for root selection, not claimed here — no new runtime PASS claimed.

## O8 repair detail (prescribed test-only)

Contract-identity mutation also changes complete staged `basis`; verifier's
complete-basis equality rejects first as `BASIS_MISMATCH` (selected
full-field binding, not missing contract protection). Changed ONLY:

```python
# contract-identity tampers complete staged basis; verifier's
# complete-basis equality rejects first as BASIS_MISMATCH.
("contract-identity",
 ...
 "BASIS_MISMATCH", "PIN", "INVALID"),
```

Retained exact `PIN`/`INVALID`, semantic mutation
(`basis.contract_identity.pipeline_contract_version=tampered`), recomputed
digest via `_retamper_manifest`, fault-present `_assert_no_write`, pristine
restore + final `_verify`. No validation reorder. `CONTRACT_IDENTITY_MISMATCH`
expectation was the test oracle error, not runtime behavior.

## Static21 / caches (NEW, read-only)

`draft-history-r9/static21.json` 3670 B `fc33a030…`: canonical flat JSON
(outer sorted, inner `sha256/bytes/mode`), exact 21 entries (18 inherited +
3 new). New3: module `7059166e…` 126181 B, test `b9f41323…` 144928 B,
schema `4fa61723…` 5627 B, all `0o664`. Inherited18 18/18 match
`expected18-source-correction-v5.json`; 84 caches 84/84 match
`cache-inventory-static.json`; 0 mismatches, no baselining.

## Remaining concerns (no execution in this unit; for root selection)

- No execution PASS claimed: all 26 methods unaudited at runtime post-edit;
  R8 batch-C O7 pass + O8 fail preserved in
  `smoke-r8-batch-c-20261018T094324Z/`; qualified scoped diagnostic
  (O8–O11f) is for root selection, not claimed here.
- Previous blocked turn performed zero work/run by design; recorded above.
