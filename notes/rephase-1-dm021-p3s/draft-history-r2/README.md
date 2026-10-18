# Draft-history R2 — correction-R1 preservation (pre-R2)

2026-10-18. Preserved BEFORE implementing Astra R2 (10 blockers) + outstanding
R1 shape gaps. `prior-bytes/` holds byte copies of the correction-R1 new3;
hashes match the independent `independent-preexecution-resolution-r1.md` §1
pins. Original R1 reports (`draft-history-r1/`, `source-implementation/`,
`astra-code-draft-review-r1.md/r2.md`, independent reviews) are preserved
untouched elsewhere — not duplicated here.

## Prior pins (measured at preservation, read-only sha256sum/stat)

| File | Bytes | Mode | SHA256 |
|---|---|---|---|
| `scripts/survey_editorial_staged_source_v2.py` | 97353 | 0o664 | `90c950d7b1a11829c06cd6579de0222b9016e173ae4c0d5b7c87994438b95d53` |
| `schemas/editorial-staged-source-manifest-v2.schema.json` | 5627 | 0o664 | `4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46` |
| `tests/test_survey_editorial_staged_source_v2.py` | 68949 | 0o664 | `7b6912e2294ff2e46a86e8f81ae7b5102030fcadf6a62698413164c639b1b8df` |

New3 live at: `/tmp/opencode/jgas-dm021p3s-impl-20261017T092635Z/candidate-partial-b40de60`
(detached `409b292`, inherited18 18/18, 84 caches; only new3 changes under R2).

## Correction scope (fresh author, this unit)

All edits restricted to new3 via exact-match replacements; no
`verification-tools/` writes, no root-doc edits, no inherited18/84 changes, no
imports/tests/fixtures/long runs, no network/commit/push. Cheap `ast.parse`
(incl. every embedded child program via literal-eval) + `jsonschema` shape
checks only (`PYTHONDONTWRITEBYTECODE=1`, stdlib/third-party imports only,
cwd inside the copy but no candidate-module imports). Cache count unchanged
84 before and after (verified via status row census, not cache-byte proof).
