# Draft-history R4 — R3 preservation (pre-R4)

2026-10-18. Preserved BEFORE implementing root pre-smoke B1/B2. `prior-bytes-r4/`
holds byte copies of the R3-corrected new3; hashes match R3 working pins
(`be133819…` / `ebc82355…` / `4fa61723…`). All previous reports
(`draft-history-r1/`, `draft-history-r2/`, `draft-history-r3/`,
`source-implementation/independent-presmoke-review-r3.md`,
`astra-presmoke-disposition-r3.md`) are preserved untouched elsewhere — not
duplicated here.

## Prior pins (measured at preservation, read-only sha256sum/stat)

| File | Bytes | Mode | SHA256 |
|---|---|---|---|
| `scripts/survey_editorial_staged_source_v2.py` | 114460 | 0o664 | `be133819b00a9f7c635d67466d309563e735441fa17992ba6e8619b869c37dfd` |
| `schemas/editorial-staged-source-manifest-v2.schema.json` | 5627 | 0o664 | `4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46` |
| `tests/test_survey_editorial_staged_source_v2.py` | 112080 | 0o664 | `ebc8235524177956238e464006e22a5199ed84701b1f7cc2e415c3ba29030af8` |

New3 live at: `/tmp/opencode/jgas-dm021p3s-impl-20261017T092635Z/candidate-partial-b40de60`
(detached `409b292`, inherited18 18/18, 84 caches; only new3 changes under R4).

## Correction scope (fresh author, this unit)

All edits restricted to new3 via exact-match replacements; no
`verification-tools/` writes, no root-doc edits, no inherited18/84 changes, no
imports/tests/fixtures/long runs, no network/commit/push. Cheap `ast.parse`
(incl. every embedded child program via literal-eval) + `jsonschema` shape
checks only (`PYTHONDONTWRITEBYTECODE=1`, stdlib/third-party imports only,
cwd inside the copy but no candidate-module imports). Cache content rehashed
read-only for the new static21 artifact; no baseline rewrite of inherited/cache
pins. Prior wrong `PIN_DRIFT` expectation for `drift-before-manifest`
preserved in `draft-history-r3/` (now `REVERIFY_FAILED`; see correction
report).
