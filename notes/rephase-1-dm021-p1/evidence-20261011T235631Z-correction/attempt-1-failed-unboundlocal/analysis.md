# Attempt-1 analysis (failed, preserved)

Date: 2026-10-11T235631Z-correction, run exit=1, 36 tests (9 P1 + 27 gate), 1673.491s.
Failures: 6 failures + 6 errors (all P1, gate 27/27 OK).

## Load-bearing defect: UnboundLocalError `receipt` (6 errors)

Location: `scripts/survey_editorial_correction_proposal_v2.py:1011`
`_frozen_names_check(receipt, before_context)` called BEFORE `receipt =
validate_receipt(...)`. `receipt` undefined at that point (only `envelope`
exists). All 6 P1 fixture tests that reach derivation (longform, weekly,
predecessor via fixture code, binding, drift, candidate) errored with
`UnboundLocalError: cannot access local variable 'receipt'`.

Fix: keep only `_proposed_upstream_check(before, proposed)` before receipt
validation (needs only contexts); move `_frozen_names_check(receipt, before)`
to AFTER validated receipt (post `RECEIPT_BINDING_CHANGED` check, pre-Gate).
Preserved in active source (hash c1c3...).

## Alias/FIFO/shadow oracle gaps (4 subfailures in matrix)

- `alias` expected `PATH_ALIAS` but got `TREE_ALIAS` (alias file inside
  edition tree triggers `_tree_map` before `safe`). Both are fail-closed alias
  refusals; test now accepts `PATH_ALIAS|TREE_ALIAS`.
- `ancestor-alias` same (symlink dir triggers `TREE_ALIAS`); plus snapshot was
  taken BEFORE linkdir creation, so injected symlink dir itself caused
  no-write diff. Fixed to snapshot AFTER mutation, accept `TREE_ALIAS`.
- `fifo-sentinel` expected `PATH_NOT_REGULAR` but got `TREE_NOT_REGULAR`
  (FIFO inside tree triggers tree walk before safe). Accept `TREE_NOT_REGULAR`;
  snapshot moved AFTER mkfifo.
- `shadow-state` snapshot BEFORE shadow file creation caused injected file diff
  to fail no-write. Fixed to snapshot AFTER shadow creation (records deliberate
  injected delta, then proves P1 adds no further write).

## Predecessor/R1 via fixture code

Both `test_honest_predecessor` and `test_r1` failed via the same UnboundLocalError
(through `_run_fixture_code` subprocess using fixture's committed P1 bytes,
which carried the same bug). No separate fixture-code bug; fixed by module fix.

## Next

Active source corrected (module c1c3..., test b26b...). Failed logs preserved
under `attempt-1-failed-unboundlocal/` (exact bytes, no edit). Rerun as attempt-2
with same strict runner (new freeze-pre).
