# Draft-history R8 — R7 preservation (pre-R8 O7 repair)

2026-10-18. Preserved BEFORE implementing root-selected O7 correction
(`astra-batch-b-resolution-selection.md`). `prior-bytes-r8/` holds byte
copies of the R7-corrected new3; hashes match R7 working pins
(`7059166e…` / `cf2bddd6…` / `4fa61723…`, test 142747 B). `static21-r7-preserved.json`
is a byte copy of `draft-history-r7/static21.json` (`b0ba134a…`, 3670 B).
All previous reports (`draft-history-r1/` through `draft-history-r7/`,
`source-implementation/batch-a-diagnosis-r6.md`,
`astra-batch-a-resolution-selection.md`, `astra-batch-b-resolution-selection.md`,
`smoke-r6-batch-a-20261018T083224Z/`, `smoke-r7-batch-b-20261018T090542Z/`)
preserved untouched — not duplicated here.

Preservation method: `cp -a` for exact byte copies + `Write` for this README
(dedicated tool for file creation; no content edits via shell). SHA256/stat
verified after copy. Subsequent O7 edit uses dedicated `Edit` tool only, not
shell executables.

## Prior pins (measured at preservation, read-only sha256sum/stat)

| File | Bytes | Mode | SHA256 |
|---|---|---|---|
| `scripts/survey_editorial_staged_source_v2.py` | 126181 | 0o664 | `7059166e075d1a10aacdd375bb8193881f0bfb2ca3e67dd142e175a349031c65` (unchanged) |
| `schemas/editorial-staged-source-manifest-v2.schema.json` | 5627 | 0o664 | `4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46` (unchanged) |
| `tests/test_survey_editorial_staged_source_v2.py` | 142747 | 0o664 | `cf2bddd6b7b253af069e1ce66bbb9fc901f1ecc8130d7db161c88df3738247ad` (R7) |

New3 live at: `/tmp/opencode/jgas-dm021p3s-impl-20261017T092635Z/candidate-partial-b40de60`
(detached `409b292`, tree `8ce36998`, index_empty, inert, full105;
inherited18 18/18, 84 caches; only O7 test body changes under R8).

## Correction scope (fresh author, this unit)

Test-only O7 repair only (module/schema unchanged — no implementation defect
per diagnosis). All edits via dedicated Edit tool exact-match replacements
in `tests/test_survey_editorial_staged_source_v2.py` O7 body only; no
`verification-tools/` writes, no root-doc edits, no inherited18/84 changes,
no imports/tests/fixture runs except the single authorized remainder batch,
no network/commit/push. Cheap `ast.parse` (incl. every embedded child
program via literal-eval) + `jsonschema` shape checks only
(`PYTHONDONTWRITEBYTECODE=1`, stdlib/third-party imports only, cwd inside
the copy but no candidate-module imports). Cache content rehashed read-only
for the new static21 artifact; no baseline rewrite.
