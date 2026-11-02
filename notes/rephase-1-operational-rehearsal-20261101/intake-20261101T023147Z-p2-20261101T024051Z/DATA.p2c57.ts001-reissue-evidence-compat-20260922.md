# Survey Production session — ts001-reissue-evidence-compat-20260922

Issue: `SP-efficient-llm-2026`
Started: `2026-09-22 UTC`
Branch: `special/efficient-llm-2026-work` (existing, no force/rebase/reset/merge)
Start HEAD: `e1c7a52712f2fa3141b7df04bb23dc56dbfe3dae` (matches brief)
Reviewed main guard: `e69187f751db5eb9b242b5c1a091d5e546040691` (remote main equal at start)
Reviewed decision: `KEEP_CORE_V2_FROZEN / USE_REPRODUCIBLE_EDITION_LOCAL_COMPATIBILITY`
  (CV2-DM-016 stays `OPEN_CORE / EDITION_WORKAROUND`; no Core repair attempted)

## Objective (issue brief)

Frozen-Core compatibility → complete Evidence/Materiality/Completeness →
`EVIDENCE_REVIEWED` → stop before Selection.

## Outcome

`SOL_EVIDENCE_REVIEW_READY / FROZEN-CORE COMPATIBILITY VALIDATED / SELECTION NOT STARTED`.
Lifecycle `CANDIDATES_NORMALIZED` → `EVIDENCE_REVIEWED`
(checkpoint `orchestration/v2/checkpoints/CANDIDATES_NORMALIZED.json`,
SHA `b69d2a0b4936c5122bd9a6f63b4186f46c5baee4f8f3156b8a01b2ac5a287038`;
State SHA `e5f1875fbe9352d0bc33c85f62fef220d39ec66b84a683376c3962bd2832792c`).

## Guards performed (all PASS before any write)

1. Remote branch HEAD == `e1c7a52…`; 2. remote main == `e69187f…`;
3. main delta `f85539c…→e69187f…` docs-only (single file
   `docs/core-v2-deferred-maintenance-summary.md`; empty diff on
   `scripts schemas config .github/workflows`); 4. lifecycle
   `CANDIDATES_NORMALIZED`; 5. Screening acceptance SHA `65330476…` +
   Discovery SHA `7074cef2…` unchanged; 6. no `evidence/` tree, ledger, or
   completeness present; 7. Selection pending.
Prior defect record + prior session read; prior failed run treated as failed
evidence (nothing carried forward); r1 interactive input reused only as
starting work product (new r2 revision built, r1 preserved).

## Actions performed

1. **Supplement authorities**: independently re-resolved all 9 wrong-identity
   arXiv locators via arXiv API title checks (all 9 wrong + all 9 true
   identities verified; my prior recalled FP8/DeeBERT/DoReMi IDs re-checked).
   Brief's Sarathi-Serve 2403.02310 verified as the same-line 2024 follow-up
   and bound additively alongside the described 2023 paper (2308.16369).
   DeeBERT independently resolved (2004.12993). Captured 13 immutable Raw
   files (1,275,978 bytes, content-verified per file) under
   `external/evidence-supplement/raw/`; built frozen-validated supplement
   manifest r1 (SHA `62031208…`, 13 sources) via frozen
   `build_evidence_authority_supplement` (frozen override context only).
2. **Compat adapter** (`execution/compat/evidence-source-class-projection/`):
   frozen normal package (with supplement) → projection of ONLY
   `source_records[*].source_type` per reviewed map (67 projected / 93
   passthrough; per-type counts match brief; §7 field-identity asserted per
   task; unexpected vocabulary fail-closes) → persisted `compat-package/`
   (SHA `60860c88…`) → frozen `validate_evidence_package_basis` PASS →
   `COMPATIBILITY_REPRODUCIBILITY: PASS` (two clean-temp builds
   byte-identical, incl. persisted output).
3. **Deeper consumption** (14 full-text bodies + launch/docs pages):
   ThinkPrune results table + protocol, overthinking cost-utility +
   crossover stats, Snell 4x/14x, s1 curation + o1-preview comparison,
   FrugalGPT Table 3 + pricing, RouteLLM data pipeline, EAGLE results,
   MTP mechanism + gains, V4.1 CSA2/FP4-KV/SWA/appendix/pipeline sections,
   Qwen Tab.11/three-axis/GR/Muon sections, Kimi interleave/DPLR/license
   (CC BY-NC-ND 4.0), V3.2 DSA equations, V4 section structure, Engram
   adaptations + delta table, DSA launch page (full read).
4. **Fresh input r2** (new revision; r1 untouched): 160 records,
   148 PARTIAL / 12 VERIFIED, 137 MATERIAL / 23 CONTEXT / 0 HOLD,
   11 supplement-bound; Completeness O01–O12 (closure limitations now
   preserve residual verbatim). JSON SHA `5f8395d0…`.
5. **Frozen chain** (`run_frozen_evidence_chain.py`, replicates frozen
   `run()` call sequence with compat package substituted; all judgments
   frozen): 160 Cards + 160 Views accepted (`dba89409…`, `2bf475f5…`),
   ledger (165 rows: MATERIAL 137 / CONTEXT 23 / EXCLUDED 5), completeness
   LIMITED (15 obligations: 3 SATISFIED / 12 LIMITATION incl.
   edition-authored O13/O14/O15 rows with Profile-declared dimensions —
   required by the frozen named-obligation guard; frozen builder emits
   initial rows only; deviation documented in driver; all rows frozen-judged).
6. **Advance**: frozen stage validation PASS → reviews → frozen checkpoint →
   frozen advance to `EVIDENCE_REVIEWED` (next_action `stage:selection`,
   NOT entered).
7. **Packages**: authority-consumption r2 (supersedes blocked r1);
   compat `validation-report.md` (frozen outcomes + identity audit);
   index updated.

## Commits (existing branch only, normal, no force)

1. `TS-001 reissue: add frozen-Core Evidence compatibility authority`
   (adapter + supplement + Raw + r2 input tooling + r2 input).
2. `TS-001 reissue: complete Evidence through Sol review readiness`
   (evidence outputs + advance + r2 package + session + index).

## End state / resume

- Lifecycle `EVIDENCE_REVIEWED`; evidence/materiality/completeness `passed`;
  selection/architecture pending. Selection NOT started.
- Shared Core unchanged; CV2-DM-016 `OPEN_CORE / EDITION_WORKAROUND`;
  `WORKAROUND_VALIDATED` stated, never `CORE_FIXED`.
- Next: Sol authority-consumption + materiality review (package r2), then
  Sol-reviewed Selection semantics. Session status: `COMPLETE`.
