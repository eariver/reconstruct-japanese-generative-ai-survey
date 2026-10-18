# Draft-history R5 — R4 preservation (pre-R5)

2026-10-18. Preserved BEFORE implementing root pre-smoke R5 (A/B/C). `prior-bytes-r5/`
holds byte copies of the R4-corrected new3; hashes match R4 working pins
(`5dbf9d4e…` / `71dfeabc…` / `4fa61723…`). All previous reports
(`draft-history-r1/` through `draft-history-r4/`,
`source-implementation/independent-presmoke-review-r3.md`,
`astra-presmoke-disposition-r3.md`) are preserved untouched elsewhere — not
duplicated here.

## Prior pins (measured at preservation, read-only sha256sum/stat)

| File | Bytes | Mode | SHA256 |
|---|---|---|---|
| `scripts/survey_editorial_staged_source_v2.py` | 124504 | 0o664 | `5dbf9d4e082a3ce6594b3d24112fca914daba7fe9d05d0f0b27e2064a3567afc` |
| `schemas/editorial-staged-source-manifest-v2.schema.json` | 5627 | 0o664 | `4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46` |
| `tests/test_survey_editorial_staged_source_v2.py` | 114642 | 0o664 | `71dfeabcdb152238247bafaacf106c8ba94f443c516ad2c98c916cf3380ccc3e` |

New3 live at: `/tmp/opencode/jgas-dm021p3s-impl-20261017T092635Z/candidate-partial-b40de60`
(detached `409b292`, inherited18 18/18, 84 caches; only new3 changes under R5).

## Correction scope (fresh author, this unit)

(A) durable launcher lifecycle under single try/finally with owned-child
kill+reap and persistence-failure propagation; (B) no live-pinning of
historical checkpoint artifacts to old sha and no supplemental conflict against
them (R1 same-chain viability; history via retained verification); (C) first
stable before/upstream/digest checks precede supplemental construction.
All edits restricted to new3 via exact-match replacements; no
`verification-tools/` writes, no root-doc edits, no inherited18/84 changes, no
imports/tests/fixtures/long runs, no network/commit/push. Cheap `ast.parse`
(incl. every embedded child program via literal-eval) + `jsonschema` shape
checks only. Cache content rehashed read-only for the new static21 artifact;
no baseline rewrite. Prior wrong `PIN_DRIFT` expectation for
`drift-before-manifest` (R4) preserved in `draft-history-r4/` (now
`REVERIFY_FAILED` since R4; unchanged here).
