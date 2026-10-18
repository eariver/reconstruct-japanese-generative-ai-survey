# Draft-history R1 — initial new3 preservation (pre-correction)

2026-10-18. Preserved BEFORE implementing Astra R1 + independent B1–B4/Q1–Q8
corrections. `initial-new3/` holds byte copies of the reviewed initial draft;
hashes match the independent review §2 pins. Original reports
(`source-implementation/`, `interface-*.md`, `source-binding.md`,
`astra-code-draft-review-r1.md`,
`source-implementation/independent-preexecution-review.md`) are preserved
untouched elsewhere in this directory — not duplicated here.

## Initial pins (measured at preservation)

| File | Bytes | Mode | SHA256 |
|---|---|---|---|
| `scripts/survey_editorial_staged_source_v2.py` | 77172 | 0o664 | `49a5564371ae57c2ed5925dbe96241f943167e16dd5092218de617df3b0854f0` |
| `schemas/editorial-staged-source-manifest-v2.schema.json` | 5627 | 0o664 | `4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46` |
| `tests/test_survey_editorial_staged_source_v2.py` | 40738 | 0o664 | `92fcc964838991e8bd6aec4647a88092239dedcfbb0f0aea4a1855a2e930c550` |

New3 live at: `/tmp/opencode/jgas-dm021p3s-impl-20261017T092635Z/candidate-partial-b40de60`
(detached `409b292`, inherited18 18/18, 84 caches; only new3 changes under R1–R5).

## Correction scope (author A, this unit)

All edits restricted to new3 via the file-edit tool (exact-match replacements;
harness-truncated payloads completed by follow-ups; stray harness marker lines
removed with byte-verification). No `verification-tools/` writes, no root-doc
edits, no imports/tests/fixtures/long runs, no network/commit/push.
