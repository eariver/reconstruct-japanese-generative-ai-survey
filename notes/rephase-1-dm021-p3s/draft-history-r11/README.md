# Draft-history R11 — R10 preservation (pre-R11 R1 fixture repair)

2026-10-18. Preserved BEFORE implementing root-selected R1 fixture repair
(`astra-r1-fixture-resolution-selection.md`). `prior-bytes-r11/` holds byte
copies of the R10-corrected new3; hashes match R10 working pins
(`7059166e…` / `6b6bd1f0…` / `4fa61723…`, test 147930 B). `static21-r10-preserved.json`
is a byte copy of `draft-history-r10/static21.json` (`67978bc2…`, 3670 B).
All previous reports (`draft-history-r1/` through `draft-history-r10/`,
`astra-seven-correction-selection.md`,
`astra-r1-fixture-resolution-selection.md`,
`source-implementation/batch-d-diagnosis-r9.md`,
`smoke-r9-batch-d-20261018T100340Z/`, `smoke-r9-batch-e-20261018T112025Z/`,
`smoke-r10-batch-f-20261018T130506Z/`) preserved untouched.

Tool-adapter: AVAILABLE dedicated `Edit`/`Write` used (no shell
`apply_patch`/shell rewrites for candidate edit). Preservation via archival
`cp -a` only; R1 fixture repair via dedicated `Edit` only.

## Prior pins (measured at preservation, read-only sha256sum/stat)

| File | Bytes | Mode | SHA256 |
|---|---|---|---|
| `scripts/survey_editorial_staged_source_v2.py` | 126181 | 0o664 | `7059166e075d1a10aacdd375bb8193881f0bfb2ca3e67dd142e175a349031c65` (frozen) |
| `schemas/editorial-staged-source-manifest-v2.schema.json` | 5627 | 0o664 | `4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46` (frozen) |
| `tests/test_survey_editorial_staged_source_v2.py` | 147930 | 0o664 | `6b6bd1f0cd02bf0ae60e8f1a1fb6a88e6185f90cfd2442ed265ce0973accaba0` (R10) |

New3 live at: `/tmp/opencode/jgas-dm021p3s-impl-20261017T092635Z/candidate-partial-b40de60`
(detached `409b292`, tree `8ce36998`, index_empty, inert, full105;
inherited18 18/18, 84 caches; ONLY `_R1_FIXTURE_PREPARE_SCRIPT` changes under R11).

## Correction scope (fresh author, this unit)

Test-only R1 fixture-script repair only (module/schema/all methods/other
helpers + 3 other script constants frozen). All edits via dedicated `Edit`
exact-match in `_R1_FIXTURE_PREPARE_SCRIPT` string only; no
`verification-tools/` writes, no root-doc edits, no inherited18/84 changes,
no imports/tests/fixture runs except the single authorized diagnostic batch,
no network/commit/push. Cheap `ast.parse` (incl. embedded scripts via
literal-eval) + `jsonschema` shape checks only (`PYTHONDONTWRITEBYTECODE=1`).
Cache rehashed read-only for new static21; prior fault-using successes stay
bound to old pins (no full26 transfer).
