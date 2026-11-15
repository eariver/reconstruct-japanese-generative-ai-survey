# SP R2 post-prepare review — BOUNDED_RESEARCH_DECISION_READY (no adopt, no Human approval)

Reviewer: independent content+mechanical reviewer (not DATA author/setup/operator). Provider `opencode-General`, serving model unknown (no verification; Human defers comparison). Invocation `independent POSTPREPARE content+mechanical-gated review sp-repaired-20261112-r2`, actual UTC `2026-11-14T13:04:18Z` (packet writes/data-hash/json datetime explicitly allowed).
Scope: SP R2 `sp-repaired-20261112-r2` after-graph review vs OLD active (not only vs R1), per root §14-16. Old SP State `180db8c3…`/CP `1233b1f6…`/4-refs still active (no adopt here); old R1 `694f5e49…` + decision `b7a78bfa…` (source cc1c) preserved unadopted, NOT rebound by operator. W34 `73ab28ea…` readback noted only (SP review does NOT assert W34 old State baseline; W34 adopt may run independently). No proof/adopt/project runtime/imports/tests/Git/network/Production/subagents. No SYNTHETIC approval, no Human approval.

## 1. Actual R2 bindings (genuine exact)

- New artifact-only epoch `ae0dd1ee5b0e7a85c44bdab0e6cd024bf12f0c56` parent `cc1c7fd1…`, tree `ec11cf6c49b3cdf54c7aa98703f6d3e74806dc58` (2 Profile files only: W34 `2a8c3089…`/2371 + SP `aff05fd5…`/13748; source773 `a7e40c…`, live aff/2a8 bytes, States/CPs/old graphs unchanged; missing `b797…` preserved, no hydration).
- R2 manifest `sources/SP-efficient-llm-2026/research/v2/acceptance-revisions/sp-repaired-20261112-r2/revision-manifest.json` 183765B `de462dc79294da41e84d8eb1116a698cbbd23df715285ef0acddee039cf79ee4`, work ae0dd/ec11cf6c, request `1587dbb7930f…`/389945 (OEXCL, NO sort, epoch meta only).
- R2 request `research/v2/acceptance-revision-inputs/sp-repaired-20261112-r2.json` 389945B `1587dbb7930f…` differs R1 `67fa3d9e…`/389945 ONLY `revision_id r1→r2`, `work cc1c/ed2dc4→ae0dd/ec11cf`, `tool_pins.repository_commit_sha cc1c→ae0dd`, `executor/recorded_at` new; records160/completeness8closure/runner/all refs/Raw4/supp identical (verified key-by-key).
- beforeState SP `180db8c3…`/4194 EVIDENCE_REVIEWED, beforeCheckpoint CP `1233b1f6…` (evidence/materiality/completeness same file), work ae0dd/ec11cf6c, tool contract `3adfbda2/b5b955d5/0f575e6d/a6859559` unchanged (old Contract8 same, Profile bytes present, needed objects readable).
- R2 namespace 970 files: tasks/cards/views 160 each, ledger 165 rows, completeness 15 obs, evidence-accepted 49237B, views-acceptance 64222B, ledger 66850B, completeness 34249B, supp `ff3ba775…`/31530 (27+3, D142 absent; source full30 `e2bfb30a`/31522).
- Staged Raw4 FULLDID exact (reused, no copy): D070/D071/D141/D142 as in R1 (hashes/bytes/literails re-verified in §2).

## 2. Mechanical rebind R2 vs OLD active 73f4/5e722 (not only vs R1)

Stdlib `read_bytes` + `sha256` + `json.loads` compared separately (no parsed==bytes inference):
- Cards `results/task-*.json` 160 names identical R2 vs OLD: 156 unaffected byte-eq AND parsed-eq (both 156/156); 4 affected differ (D070/D071/D141/D142) expected. R2 vs R1 candidate 0 diff (all 160 byte-identical) — contents 4 unchanged from approved R1 post-review.
- Views `views/view-*.json` 160 names identical: 156 unaffected byte-eq AND parsed-eq (both 156/156, `evidence_sha256` identical); 4 affected differ with correct derivation. R2 vs R1 0 diff.
- Tasks `tasks/task-*.json` 160 names identical: 157 byte+parsed exact (156 unaffected + D142 identical, no authority_supplement_source_ids both sides) + 3 affected supp-ID rotations only (D070 `6a5ae38a→ea9b086e`, D071 `0d550497→793903f4`, D141 `95365faf→228b8166`; `source_records/verification_targets` identical, D142 no bindings). 160-universe holds, NOT full-160-fresh-content claim (scope §4).
- Ledger 165/165 rows parsed-identical (0 diff) incl 5 DROP (`EFF-D140/D158/D159/D160/D161`); downstream CONTEXT×3/MATERIAL×1 unchanged (SP ledger is record-ownership, not card promotion). 161 unaffected + 4 affected identical in ledger (total 165 identical).
- Supplement `ff3ba775`/31530: 27 preserved byte-identical + 3 archive exact pins (`ea9b086e 253542 14ae3118`, `793903f4 307198 35770834`, `228b8166 350662 97a5dd74`), retired 3 current-only, D142 no entry. FULLDID Raw4 + literals FOUND in retained bytes (visible bodies, 0 hidden `Content selection saved`).
- Request records 160 match r7 `0a54004e` (lineage CORE all4, D142 key omitted, targets 2/1/2/2); completeness r8 `6929d9ca` (O10 archive-aware, residual5, FULL 8-field closure).

## 3. Content deep review (4 after-cards + completeness, vs R1 approved)

R2 after-cards byte-identical to R1 (0 diff, §2) — contents 4 unchanged from R1 `b7a78bfa` post-review, re-verified here (not assumed):
- D070/D071/D141 PARTIAL PRODUCT VENDOR_CLAIM×3 with bound visible-body literals (207 div/`<strong>`/nuance; content-area/646 span/callout with 255-absent; 652 span/PLATFORM RATE LIMIT row caps NOT measured throughput/customizing), served Sept20/21 CDX MATCH (requested-row NO-MATCH never cited), 1.13-only vs Nov 1.14 drift noted; verification VERIFIED-historical-conditional + UNRESOLVED quarantine; materiality CONTEXT (Ledger CONTEXT until accepted revision + re-review).
- D142 PARTIAL API INFERENCE×2 (`INDEPENDENT_EVIDENCE_NOT_FOUND_AS_OF_2026-09-21` token S142 line44 + summary-scope `API body uninspected, not global proof`), key absent (not null), S142 provenance 3751B `f7eeec68…18672662`, UNRESOLVED×2, MATERIAL-as-potential-relevance + HOLD ceiling + no-verified-facts caveat; built-card `src-1 Discovery-bounded` bound with UNRESOLVED (attempted, not passed) — honest, no publisher fact/supplement/global `published on the reference` claim.
- Temporal `observed_at 2026-09-22T15:00:00Z` retained historical (NOT new review time) per root §4; executor/recorded_at carry new operation. Completeness R 34249B overall LIMITED, 15×7 O01/O07 SAT rest LIM, O10 archive-aware LIMITATION (no autoSAT), residual5 same, closure FULL 8-field `3/4/8/0/true/0/LIMITED/5` verbatim from `d67f…` (factual baseline, no new expansion invented, Discovery `7074cef2`/SCP `6ff524b0` unchanged).
- Scope: 4 changed deep-read above + prior r4-r8 unchanged observations reused (156/D165, full30, staging/routing, O10/residual, literals/keys/targets, pin `62662→72662`, closure 3→8 FULL); NOT a fresh full-160 semantic re-read.

## 4. Profile epoch check + no fake history

New tree `ec11cf…` vs old 32239-entry map = exactly 2-line diff (W34 profile modified `155b78cf→c2990d4f`, SP profile added `9251f487`; all other mode/type/OIDs identical incl `b797…`, no deletions/forged objects). Committed bytes match files (`2a8c3089`/`aff05fd5`); needed 7 tools + config + 2 profiles `cat-file -e` readable; `b797…` still missing (not claimed). Old Contract8 bytes unchanged; live Profiles are data at epoch, not authority change. Old R1/decision `b7a78bfa` source-cc1 preserved, NOT rebound (R2 decision is NEW, operator did not rewrite R1 expected-head/tree). W34 `73ab28ea` readback under ae0dd still complete via parent objects; no W34 baseline asserted here.

## 5. Decision

No defect. **Actual BOUNDED_RESEARCH_DECISION_READY** — see `sp-supplied-decision-r2.json` (`$defs.suppliedDecision`) + this review + machine in FULL packet paths below. No adopt/State/proof/Selection/Production mutation; W34 adopt independent. Old R1/decision preserved. Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN. Stop at Human Commit Point.

## 6. Read scope + full pins

Read: root §14-16 + R2 report/machine (`sp-r2-…125815Z`) + artifact/epoch reports + R2 manifest/request/R candidate (160/160/160/165/15) + OLD active 73f4/5e722/b7c/d67 + SP State 180/CP 1233 + R1 manifest/request/decision (preserved) + staged Raw4/supp + r4-r8 DATA/dossiers/reviews + DM022/result/runner schemas (as DATA). Method stdlib hash/JSON/compare + Read/sha256sum/grep only. Full pins in machine companion. Packet writes/data-hash/json datetime explicitly allowed; no active/proof/adopt/project runtime/imports/tests/Git/network/Production/subagents.
