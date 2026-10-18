# Draft-history R9 — R8 preservation (pre-R9 O8 correction)

2026-10-18. Preserved BEFORE implementing root-selected O8 correction
(`astra-replay-fault-batch-selection.md`). `prior-bytes-r9/` holds byte
copies of the R8-corrected new3; hashes match R8 working pins
(`7059166e…` / `955f6fb5…` / `4fa61723…`, test 144795 B). `static21-r8-preserved.json`
is a byte copy of `draft-history-r8/static21.json` (`267dc51e…`, 3670 B).
All previous reports (`draft-history-r1/` through `draft-history-r8/`,
`astra-batch-b-resolution-selection.md`, `astra-replay-fault-batch-selection.md`,
`smoke-r7-batch-b-20261018T083224Z/`, `smoke-r8-batch-c-20261018T094324Z/`)
preserved untouched — not duplicated here.

Tool-adapter record:
- Prior blocked attempt (previous turn): agent harness exposes dedicated
  `Edit`/`Write` (plus `Read`/`Bash`) but no tool literally named
  `apply_patch`. Per exact instruction to use `apply_patch` TOOL if available
  and otherwise return explicit availability rather than calling shell
  `apply_patch`, the agent returned blocked with NO work/run (no
  `draft-history-r9`, no candidate edit, no static21, no batch). No shell
  `apply_patch` was called; no source edits were substituted.
- This turn: root tool-adapter clarification authorizes continuing with
  AVAILABLE dedicated `Edit`/`Write` per tool instructions (not shell
  `apply_patch`/shell rewrites). Preservation above used `cp -a` archival
  byte copies only (no candidate source rewrite); O8 correction below uses
  dedicated `Edit` only. This clarification is tool-adapter only, not source
  scope expansion.

## Prior pins (measured at preservation, read-only sha256sum/stat)

| File | Bytes | Mode | SHA256 |
|---|---|---|---|
| `scripts/survey_editorial_staged_source_v2.py` | 126181 | 0o664 | `7059166e075d1a10aacdd375bb8193881f0bfb2ca3e67dd142e175a349031c65` (unchanged) |
| `schemas/editorial-staged-source-manifest-v2.schema.json` | 5627 | 0o664 | `4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46` (unchanged) |
| `tests/test_survey_editorial_staged_source_v2.py` | 144795 | 0o664 | `955f6fb5dd65e2e731d9de38e093f42d499d1f425186848834ecaf109cd800e9` (R8) |

New3 live at: `/tmp/opencode/jgas-dm021p3s-impl-20261017T092635Z/candidate-partial-b40de60`
(detached `409b292`, tree `8ce36998`, index_empty, inert, full105;
inherited18 18/18, 84 caches; only O8 test expectation changes under R9).

## Correction scope (fresh author, this unit)

Test-only O8 contract-identity correction only (module/schema unchanged —
selected full-field binding, not runtime bug). All edits via dedicated `Edit`
exact-match in `tests/test_survey_editorial_staged_source_v2.py` O8
`o8_cases` contract-identity tuple only; no `verification-tools/` writes, no
root-doc edits, no inherited18/84 changes, no imports/tests/fixture runs
except the single authorized diagnostic batch, no network/commit/push. Cheap
`ast.parse` (incl. embedded child programs via literal-eval) + `jsonschema`
shape checks only (`PYTHONDONTWRITEBYTECODE=1`, stdlib/third-party imports
only, cwd inside copy but no candidate-module imports). Cache rehashed
read-only for new static21; no baseline rewrite.
