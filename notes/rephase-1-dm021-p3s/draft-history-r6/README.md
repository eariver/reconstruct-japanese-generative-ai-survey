# Draft-history R6 — R5 preservation (pre-R6)

2026-10-18. Preserved BEFORE implementing root post-smoke oracle corrections
(items 1–7). `prior-bytes-r6/` holds byte copies of the R5-corrected new3;
hashes match R5 working pins (`7059166e…` / `6b35a3e5…` / `4fa61723…`, test
114642 B). All previous reports (`draft-history-r1/` through `draft-history-r5/`,
`source-implementation/independent-presmoke-review-r3.md`,
`astra-postsmoke-oracle-review.md`, `astra-presmoke-disposition-r3.md`,
`smoke-r5*/`) are preserved untouched elsewhere — not duplicated here.

## Prior pins (measured at preservation, read-only sha256sum/stat)

| File | Bytes | Mode | SHA256 |
|---|---|---|---|
| `scripts/survey_editorial_staged_source_v2.py` | 126181 | 0o664 | `7059166e075d1a10aacdd375bb8193881f0bfb2ca3e67dd142e175a349031c65` |
| `schemas/editorial-staged-source-manifest-v2.schema.json` | 5627 | 0o664 | `4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46` |
| `tests/test_survey_editorial_staged_source_v2.py` | 114642 | 0o664 | `6b35a3e5d64817d5cdfd2ad5e06fc990089c2eb6ea4e920858a3e437fb5627c5` |

New3 live at: `/tmp/opencode/jgas-dm021p3s-impl-20261017T092635Z/candidate-partial-b40de60`
(detached `409b292`, inherited18 18/18, 84 caches; only new3 changes under R6).

## Correction scope (fresh author, this unit)

Test-only corrections (module/schema unchanged — no implementation defect found
requiring selection; see report for the one generic-code observation). All edits
via exact-match replacements; no `verification-tools/` writes, no root-doc edits,
no inherited18/84 changes, no imports/tests/fixtures/long runs, no
network/commit/push. Cheap `ast.parse` (incl. every embedded child program via
literal-eval) + `jsonschema` shape checks only (`PYTHONDONTWRITEBYTECODE=1`,
stdlib/third-party imports only, cwd inside the copy but no candidate-module
imports). Cache content rehashed read-only for the new static21 artifact; no
baseline rewrite. Prior wrong expectations (O7 SCOPE_ for missing scope,
O8 accumulated tamper/foreign dup filename, O9 byte-copy restoration, O6b
arbitrary KEEP + OBSERVE, O4 OBSERVER_REFUSED, O12a/O13/O14/O10/O11 broad
asserts) preserved in earlier drafts.
