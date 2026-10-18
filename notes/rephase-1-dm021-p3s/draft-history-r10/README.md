# Draft-history R10 — R9 preservation (pre-R10 seven-method correction)

2026-10-18. Preserved BEFORE implementing root-selected seven-method
correction (`astra-seven-correction-selection.md`). `prior-bytes-r10/` holds
byte copies of the R9-corrected new3; hashes match R9 working pins
(`7059166e…` / `b9f41323…` / `4fa61723…`, test 144928 B). `static21-r9-preserved.json`
is a byte copy of `draft-history-r9/static21.json` (`fc33a030…`, 3670 B).
All previous reports (`draft-history-r1/` through `draft-history-r9/`,
`astra-seven-correction-selection.md`,
`source-implementation/batch-d-diagnosis-r9.md`,
`smoke-r9-batch-d-20261018T100340Z/`, `smoke-r9-batch-e-20261018T112025Z/`)
preserved untouched — not duplicated here.

Tool-adapter record:
- Agent harness exposes dedicated `Edit`/`Write` (no tool literally named
  `apply_patch`; root acknowledgement recorded). This turn uses AVAILABLE
  dedicated `Edit`/`Write` per instructions (not shell `apply_patch`/shell
  rewrites). Preservation above used archival `cp -a` byte copies only (no
  candidate source rewrite); seven-method correction below uses dedicated
  `Edit` only. Prior blocked-turn (no work/run) recorded in R9 report.
- Blocked-turn record carried forward: previous `apply_patch`-literal
  requirement returned explicit availability with zero edits/batch; this R10
  proceeds per clarification.

## Prior pins (measured at preservation, read-only sha256sum/stat)

| File | Bytes | Mode | SHA256 |
|---|---|---|---|
| `scripts/survey_editorial_staged_source_v2.py` | 126181 | 0o664 | `7059166e075d1a10aacdd375bb8193881f0bfb2ca3e67dd142e175a349031c65` (unchanged) |
| `schemas/editorial-staged-source-manifest-v2.schema.json` | 5627 | 0o664 | `4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46` (unchanged) |
| `tests/test_survey_editorial_staged_source_v2.py` | 144928 | 0o664 | `b9f413234dcc4230be1dcc7865d649efcbadca284dde37e6d9284aa3f43c5604` (R9) |

New3 live at: `/tmp/opencode/jgas-dm021p3s-impl-20261017T092635Z/candidate-partial-b40de60`
(detached `409b292`, tree `8ce36998`, index_empty, inert, full105;
inherited18 18/18, 84 caches; only 7 methods + required fault/R1 helpers change under R10).

## Correction scope (fresh author, this unit)

Test-only seven-method correction only (module/schema frozen — no
implementation defect per diagnoses). All edits via dedicated `Edit`
exact-match in `tests/test_survey_editorial_staged_source_v2.py`:
O9/O10/O11b/O11c/O11e/O11f/R1 bodies + required `_P3S_FAULT_SCRIPT`
observer wrapping/outcome + `_commit_r1_nonemitted_comment` allowed path +
`_R1_FIXTURE_PREPARE_SCRIPT` if needed (constants only, no semantic change
beyond selection). No `verification-tools/` writes, no root-doc edits, no
inherited18/84 changes, no imports/tests/fixture runs except the single
authorized diagnostic batch, no network/commit/push. Cheap `ast.parse`
(incl. embedded child programs via literal-eval) + `jsonschema` shape checks
only (`PYTHONDONTWRITEBYTECODE=1`, stdlib/third-party imports only, cwd
inside copy but no candidate-module imports). Cache rehashed read-only for
new static21; no baseline rewrite. Fault-script change affects prior
fault-using successes; their evidence stays bound to old pins (no full26 transfer).
