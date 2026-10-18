# Draft-history R3 — R2 preservation (pre-R3)

2026-10-18. Preserved BEFORE implementing root R3 readback (6 items). `prior-bytes/`
holds byte copies of the R2-corrected new3; hashes match the R2 working pins
(`821c57ba` / `fa172fd3` / `4fa61723`). Original R2 reports
(`draft-history-r2/correction-report-r2.md`, `coverage-matrix-r2.md`) are
preserved untouched elsewhere — not duplicated here.

## Prior pins (measured at preservation, read-only sha256sum/stat)

| File | Bytes | Mode | SHA256 |
|---|---|---|---|
| `scripts/survey_editorial_staged_source_v2.py` | 110461 | 0o664 | `821c57ba910d1ea8e8e8df44783f298b5a6bd0a318bdfa0c50519076ae1d7849` |
| `schemas/editorial-staged-source-manifest-v2.schema.json` | 5627 | 0o664 | `4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46` |
| `tests/test_survey_editorial_staged_source_v2.py` | 104179 | 0o664 | `fa172fd3a97a7059960f970886f3ac918a0423a1bb67155e71e475392bfaeb90` |

New3 live at: `/tmp/opencode/jgas-dm021p3s-impl-20261017T092635Z/candidate-partial-b40de60`
(detached `409b292`, inherited18 18/18, 84 caches; only new3 changes under R3).

## Correction scope (fresh author, this unit)

All edits restricted to new3 via exact-match replacements; no
`verification-tools/` writes, no root-doc edits, no inherited18/84 changes, no
imports/tests/fixtures/long runs, no network/commit/push. Cheap `ast.parse`
(incl. every embedded child program via literal-eval) + `jsonschema` shape
checks only (`PYTHONDONTWRITEBYTECODE=1`, stdlib/third-party imports only,
cwd inside the copy but no candidate-module imports). Cache content rehashed
read-only for the static21 artifact; no baseline rewrite of inherited/cache
pins.
