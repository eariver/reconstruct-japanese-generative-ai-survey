# Survey Production session — ts001-reissue-evidence-20260922

Issue: `SP-efficient-llm-2026`
Started: `2026-09-22 UTC`
Branch: `special/efficient-llm-2026-work` (existing, no force/rebase/reset)
Start HEAD: `bece7052f8da9a5fb21bb09726f6f0cb7e0075e5` (matches issue brief)
Reviewed main guard: `f85539c31a079ab7a7fa86185f3cbb0fcad0485a` (verified in history; remote main equal at start)

## Objective (issue brief)

Correct the Screening review package (r2), record Sol Screening PASS,
execute `stage:evidence-materiality-completeness` to `EVIDENCE_REVIEWED`,
stop before Selection.

## Outcome

- Screening correction + Sol PASS: **COMPLETE** (r2 + Sol review files).
- Evidence execution: **BLOCKED by a shared-Core defect** (Evidence
  `SOURCE_CLASS_MAP` lacks 10 Thematic Discovery source types; 67/160 tasks
  fail closed). Defect recorded edition-locally; shared Core unchanged.
  Interactive Evidence input (160 records) authored, task-validated, and
  preserved for clean resume. Lifecycle remains `CANDIDATES_NORMALIZED`.
  Selection NOT started.

## Actions performed

1. Guard verification: HEAD == brief SHA; reviewed main in history and equal
   to remote main; lifecycle `CANDIDATES_NORMALIZED`; next action
   `stage:evidence-materiality-completeness`.
2. Mechanical recount from canonical bytes (`discovery-v2.jsonl` SHA
   `7074cef2…`, `screening-accepted.json` SHA `65330476…`): disposition
   totals 135/20/5/5 confirmed; source-class × disposition and obligation ×
   disposition tables recomputed cell-for-cell (all matched the brief's
   correction tables; reported as recomputed values).
3. Wrote `execution/reviews/screening-review-package-r2.md`
   (`CORRECTED / SUPERSEDES_R1_FOR_SOL_REVIEW`) with r1 defect ledger (false
   `Dropped primary authorities: None`, wrong O11 38/5 incl. D100
   mis-inclusion, undercounted obligation tallies). r1 untouched.
4. Wrote `execution/reviews/sol-screening-review-pass-20260922.md`
   (Reviewer Sol / GPT-5.6, `PASS / PROCEED_TO_EVIDENCE`; Muse claims no
   authorship; Screening acceptance unchanged; Selection not authorized).
5. Authority-consumption retrieval for Evidence authorship:
   - arXiv API bulk fetch: all 95 arXiv-linked records' metadata consumed.
   - 9 full-page fetches consumed (DSA launch/API-docs excerpts, ezyang
     V4.1 study, GenAI-Perf docs, vLLM V4.1 recipe, Unsloth GLM docs,
     llama.cpp PR 27742, Jev launch/concepts/models pages).
   - Web-search gap-fill: SWE-bench-Pro (2509.16941 + 2609.08149),
     Terminal-Bench 2.0 (2601.11868), DoReMi (2305.10429 + CRFM).
   - Mechanical title cross-check found **9 wrong-identity bound arXiv
     locators** (D005, D061, D062, D093, D094, D098, D112, D117, D139);
     true identities verified via API/search (my own recalled IDs for
     FP8/DeeBERT/DoReMi were verified-WRONG first and discarded).
     DSA dedicated URLs isolated (G-EV-02); AIPerf successor named (G-EV-10).
6. Authored 160-record interactive Evidence input
   (`execution/evidence-interactive-input/`, JSON SHA `6cac92b1…`):
   155 PARTIAL / 5 VERIFIED, 134 MATERIAL / 24 CONTEXT / 2 HOLD; exact
   task-target match asserted programmatically; Completeness block
   (O01–O12: 3 SATISFIED / 9 LIMITATION, LIMITED).
7. Ran `run_evidence_v2_interactive.py` → fail-closed:
   `unsupported source_type for Evidence authority: 'PRIMARY_DOC'`.
   Diagnosed to `survey_evidence_v2._source_class` map gap (10 Thematic
   types, 67 tasks). Verified no edition-local workaround exists
   (Discovery records always pass through the map; supplement path cannot
   substitute). Verified no partial outputs were written.
8. Recorded `execution/defects/shared-core-evidence-source-map-gap-20260922.md`
   (symptom, scope table + recommended classes, W34-precedent analysis,
   resume criteria); wrote stage-blocked
   `execution/reviews/evidence-authority-consumption-package-r1.md`;
   updated `execution/index.md`.

## End state

- Lifecycle: `CANDIDATES_NORMALIZED` (unchanged); evidence/materiality/
  completeness/selection/architecture: pending.
- New files (all edition-local under `sources/SP-efficient-llm-2026/`):
  reviews r2 + Sol PASS, defects record, evidence-interactive-input/ (8
  files + README), authority-consumption package r1, this session record,
  index update.
- Shared Core: unchanged (no edits under AGENTS.md read-only roots).
- Session status: `COMPLETE_AS_BLOCKED` (all unblocked work done; blocked
  work preserved with resume criteria).

## Resume criteria

Reviewed Core repair of the Evidence source map → re-run the preserved
input cleanly → Core-advanced State to `EVIDENCE_REVIEWED` → Sol
authority-consumption/materiality review (locator amendments G-EV-01–11,
HOLDs, watches) → Selection semantics. No verdict from the failed run may
be carried forward.
