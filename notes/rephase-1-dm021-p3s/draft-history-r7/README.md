# Draft-history R7 — R6 preservation (pre-R7 O4 repair)

2026-10-18. Preserved BEFORE implementing root-selected O4 whitespace-only
repair (`astra-batch-a-resolution-selection.md`). `prior-bytes-r7/` holds byte
copies of the R6-corrected new3; hashes match R6 working pins
(`7059166e…` / `0e1cc20f…` / `4fa61723…`, test 141792 B). `static21-r6-preserved.json`
is a byte copy of `draft-history-r6/static21.json` (`f37cf825…`, 3670 B).
All previous reports (`draft-history-r1/` through `draft-history-r6/`,
`source-implementation/batch-a-diagnosis-r6.md`,
`astra-batch-a-resolution-selection.md`, `astra-batch-a-selection-r6.md`,
`smoke-r6-batch-a-20261018T083224Z/`) preserved untouched — not duplicated here.

Preservation method: `apply_patch` CLI absent in this executor (`which
apply_patch` → not found); used `cp -a` for exact byte copies + `Write`
for this README (equivalent exact preservation, no content change).
SHA256/stat verified after copy (see packet record).

## Prior pins (measured at preservation, read-only sha256sum/stat)

| File | Bytes | Mode | SHA256 |
|---|---|---|---|
| `scripts/survey_editorial_staged_source_v2.py` | 126181 | 0o664 | `7059166e075d1a10aacdd375bb8193881f0bfb2ca3e67dd142e175a349031c65` (unchanged R5→R6) |
| `schemas/editorial-staged-source-manifest-v2.schema.json` | 5627 | 0o664 | `4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46` (unchanged) |
| `tests/test_survey_editorial_staged_source_v2.py` | 141792 | 0o664 | `0e1cc20fa0d34f6d4096bd1f99865513d4c4f1e07e6fdf20a2c36dfff6c52d9d` (R6) |

New3 live at: `/tmp/opencode/jgas-dm021p3s-impl-20261017T092635Z/candidate-partial-b40de60`
(detached `409b292`, tree `8ce36998`, index_empty, inert, full105;
inherited18 18/18, 84 caches; only O4 test body changes under R7).

## Correction scope (fresh author, this unit)

Test-only O4 whitespace repair only (module/schema unchanged — no
implementation defect per diagnosis). All edits via exact-match replacement
in `tests/test_survey_editorial_staged_source_v2.py` O4 body only; no
`verification-tools/` writes, no root-doc edits, no inherited18/84 changes,
no imports/tests/fixture runs except the single authorized remainder batch,
no network/commit/push. Cheap `ast.parse` (incl. every embedded child
program via literal-eval) + `jsonschema` shape checks only
(`PYTHONDONTWRITEBYTECODE=1`, stdlib/third-party imports only, cwd inside
the copy but no candidate-module imports). Cache content rehashed read-only
for the new static21 artifact; no baseline rewrite.
