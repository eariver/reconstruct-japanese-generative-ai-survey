# Attempt-3 analysis (failed, preserved)

Run exit=1, 36 tests, 2705s, 1 failure + 1 error (gate 27/27 OK, 7/9 P1 OK).

## Weekly aggregate (1 failure)

`staged` snapshot taken before `fixture-wk-env-same` dir creation; aggregate
compared staged (without same dir) vs after (with same dir) -> diff due to
injected dir, not P1 write. Fixed by rmtree same dir before aggregate
(records deliberate removal, then proves no further P1 write).

## Control-drift (1 error, now fixed)

`weekly.validate_receipt` raised bare `ValueError` (dirty control) instead of
`ProposalError`, so `assertRaisesRegex(ProposalError)` missed it (ERROR not
FAIL). Fixed by wrapping receipt/gate/pretex/bundle/manuscript/later-review
validators in `_pipeline`/`_build_graph` to `ProposalError` with
`RECEIPT_INVALID`/`GATE_INVALID`/`PRETEX_INVALID`/`BUNDLE_INVALID`/
`MANUSCRIPT_INVALID`/`LATER_REVIEW_INVALID` (all contain expected
`RECEIPT|CLOSURE|DRIFT|CONTRACT` substrings via `RECEIPT_INVALID`).

## Next

Active hashes updated (module receipt/gate wrapping, test same-dir cleanup).
Rerun as attempt-4.
