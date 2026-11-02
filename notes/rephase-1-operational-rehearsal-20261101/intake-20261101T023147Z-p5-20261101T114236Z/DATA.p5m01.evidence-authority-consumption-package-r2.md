# Evidence Authority-Consumption Package r2 — SP-efficient-llm-2026

Status: `EVIDENCE_ACCEPTED / SOL_EVIDENCE_REVIEW_READY / SELECTION NOT STARTED`
Date: `2026-09-22`
Author role: Muse (Luna/Work execution role). Luna-side Evidence product and
consumption ledger; NOT a Sol review and no substitute for the Sol
authority-consumption / materiality review now due.
Lifecycle: `EVIDENCE_REVIEWED` (frozen-advanced; checkpoint
`orchestration/v2/checkpoints/CANDIDATES_NORMALIZED.json`,
SHA `b69d2a0b4936c5122bd9a6f63b4186f46c5baee4f8f3156b8a01b2ac5a287038`).
Supersedes the stage-blocked r1 package (preserved as history).

## 1. Acceptance identities

- Evidence acceptance:
  `sources/SP-efficient-llm-2026/evidence/v2/accepted/dba89409c1cdcfb6a8b319ef35e0e1ee1b5ffdc74cad4715dbe44e10345e5603/evidence-accepted.json`
  (result_count 160).
- Edition Views acceptance:
  `sources/SP-efficient-llm-2026/evidence/v2/views/accepted/2bf475f518d80c8088dff7a67a0bc5cae5e2fa5c9a309d56695e66b1d54d7762/edition-views-accepted.json`
  (160 views).
- Materiality Ledger: `sources/SP-efficient-llm-2026/materiality-ledger-v2.json`
  (165 rows).
- Profile Completeness: `sources/SP-efficient-llm-2026/profile-completeness-v2.json`
  (overall `LIMITED`; 15 obligations).
- Compat package: `execution/compat/evidence-source-class-projection/compat-package/package.json`
  (SHA `60860c88de9f9ab5bc8adecdd9b9ed1c2c689c4c1ac5f8a997f85a7a6a474790`;
  160 tasks; 67 projected / 93 passthrough; `COMPATIBILITY_REPRODUCIBILITY: PASS`).
- Supplement manifest:
  `sources/SP-efficient-llm-2026/external/evidence-supplement/evidence-authority-supplement-r1.json`
  (SHA `62031208a5614bc6c75bceaaaa7e421d2fc3329eeeef69474649cc2a97a0f839`;
  13 sources / 1,275,978 Raw bytes; frozen-built + frozen-validated).
- Interactive input r2: `execution/evidence-interactive-input-r2/interactive-evidence-r2.json`
  (SHA `5f8395d03e51586bfc54821bb50b4fca4f5d51fb588295aa9d63e235bf71c841`).

## 2. Evidence status distribution (accepted Cards)

- VERIFIED (12): EFF-D032, EFF-D036, EFF-D070, EFF-D071, EFF-D141, EFF-D148,
  EFF-D149, EFF-D150, EFF-D151, EFF-D154, EFF-D163, EFF-D165.
- PARTIAL (148): all other 148 accepted records (scope stated per-record;
  abstract-scope retained only where claims are scoped accordingly).
- NEEDS_MORE / REJECTED: 0.

## 3. MATERIAL / CONTEXT / HOLD (Views + Ledger downstream)

- MATERIAL (137 Views; 137 ledger downstream): all KEEP except none excluded —
  full ID list equals the 135 KEEP + D032/D093 resolutions (see §6).
  Ledger: MATERIAL 137 / CONTEXT 23 / EXCLUDED 5 (the 5 accepted DROPs
  D140 D158 D159 D160 D161).
- CONTEXT (23 Views; 23 ledger downstream): the 20 MAYBE records (D072 D074
  D075 D076 D079 D080 D082 D084 D085 D086 D087 D097 D099 D100 D117 D120 D146
  D147 D152 D156) + D073 (KEEP community-reproduction hub, corroboration
  only) + D077 (INSPECT, lead-only study) + D119 (INSPECT, tooling usable /
  AIPerf open). Exact per-record materiality is in the accepted Views.
- HOLD: 0 (both r1 HOLDs resolved via supplement: D032→MATERIAL,
  D093→MATERIAL).

## 4. AUTHORITY_CONSUMED (claims extracted from retrieved bytes)

- 95 arXiv abstract records (identity + headline mechanism/figures at stated
  scope).
- Full-text body sections consumed: V4.1 report (D123: CSA2 modes, FP4-KV
  training, SWA replay, appendix map, post-training pipeline), Qwen report
  (D008: Tab.11, three-axis eval, GR, Muon/stability sections), Kimi report
  (D027: 3:1 interleave, DPLR, drop-in compat, CC BY-NC-ND license), V3.2
  report (D125: indexer equations, ReLU/FP8, MLA-MQA), V4 report (D124:
  section structure), ThinkPrune (D150: results table + protocol),
  overthinking (D151: cost-utility + crossover stats), Snell (D148: 4x/14x),
  s1 (D149: curation + budget forcing + o1-preview comparison), FrugalGPT
  (D154: Table 3 + pricing analysis), RouteLLM (D155: data pipeline + eval
  design), EAGLE (D036: speedups + guarantee scope), MTP (D038: mechanism +
  HumanEval/MBPP gains), Engram (D143: adaptations + delta table + LogitLens).
- Full pages: DSA launch (D032), GenAI-Perf docs (D119), vLLM V4.1 recipe
  (D163), Unsloth GLM docs (D164), llama.cpp PR 27742 (D165), Jev launch /
  concepts / models pages (D070/D071/D141).
- Supplement Raws (13 files, §7): captured + consumed at stated scope
  (abs records + SWE-Pro full-text excerpts + launch/docs pages).
- X r3 ledger (D162) via accepted Sol-reviewed import.

## 5. AUTHORITY_CAPTURED_BUT_UNCONSUMED

- Repo/doc/spec/announcement/card bodies not fetched line-level (release- or
  summary-level evidence only): EFF-D004, EFF-D009, EFF-D017, EFF-D028,
  EFF-D029, EFF-D030, EFF-D031, EFF-D039, EFF-D048, EFF-D049, EFF-D050,
  EFF-D051, EFF-D052, EFF-D054, EFF-D056, EFF-D058, EFF-D063, EFF-D064,
  EFF-D065, EFF-D066, EFF-D075, EFF-D076, EFF-D078, EFF-D079, EFF-D080,
  EFF-D081, EFF-D082, EFF-D083, EFF-D084, EFF-D085, EFF-D086, EFF-D087,
  EFF-D095, EFF-D097, EFF-D099, EFF-D100, EFF-D113, EFF-D114, EFF-D118,
  EFF-D120, EFF-D121, EFF-D122, EFF-D127, EFF-D129, EFF-D130, EFF-D131,
  EFF-D132, EFF-D136, EFF-D142, EFF-D144, EFF-D157.
- Abstract-scope-only paper sections/ablations as stated per-record
  limitations (all PARTIAL paper records).
- Captured-but-section-unread: SWE-Pro 597KB full-text Raw beyond excerpts
  (D093 limitation).

## 6. Former INSPECT outcomes (all five closed with dispositions)

- D032 → VERIFIED/MATERIAL (launch Raw consumed + supplement-bound).
- D077 → PARTIAL/CONTEXT (study traced; lead-not-authority retained).
- D093 → PARTIAL/MATERIAL (identity resolved + body captured; section read outstanding).
- D119 → PARTIAL/CONTEXT (docs consumed + bound; AIPerf open).
- D150 → VERIFIED/MATERIAL (body results + protocol consumed).

## 7. Supplement sources + locator corrections (13 entries)

| Supplement source | Task | Class | Raw bytes |
|---|---|---|---|
| FP8 identity record (2209.05433) | D005 | PRIMARY_PAPER | supp-d005-fp8-abs.html |
| Mooncake identity record (2407.00079) | D061 | PRIMARY_PAPER | supp-d061-mooncake-abs.html |
| SARATHI 2023 identity record (2308.16369) | D062 | PRIMARY_PAPER | supp-d062-sarathi2023-abs.html |
| Sarathi-Serve 2024 identity record (2403.02310) | D062 | PRIMARY_PAPER | supp-d062-sarathiserve2024-abs.html |
| SWE-Pro identity record (2509.16941) | D093 | PRIMARY_PAPER | supp-d093-swepro-abs.html |
| SWE-Pro full text v2 | D093 | PRIMARY_PAPER | supp-d093-swepro-html.html |
| Terminal-Bench 2.0 identity record (2601.11868) | D094 | PRIMARY_PAPER | supp-d094-tbench2-abs.html |
| RULER identity record (2404.06654) | D098 | PRIMARY_PAPER | supp-d098-ruler-abs.html |
| PyramidKV identity record (2406.02069) | D112 | PRIMARY_PAPER | supp-d112-pyramidkv-abs.html |
| DeeBERT identity record (2004.12993) | D117 | PRIMARY_PAPER | supp-d117-deebert-abs.html |
| DoReMi identity record (2305.10429) | D139 | PRIMARY_PAPER | supp-d139-doremi-abs.html |
| V3.2-Exp launch page (DSA debut) | D032 | PRIMARY_OFFICIAL | supp-d032-v32exp-launch.html |
| GenAI-Perf Triton docs | D119 | PRIMARY_OFFICIAL | supp-d119-genai-perf-docs.html |

Wrong-identity canonical locators preserved untouched as defect provenance:
D005 (2206.06277), D061 (2411.01181), D062 (2308.16315), D093 (2503.01324),
D094 (2406.06750), D098 (2404.18532), D112 (2406.02032), D117 (2004.12918),
D139 (2308.01833). Canonical amendment deferred to Sol. All identities
independently re-verified this run via arXiv API title checks (the brief's
Sarathi-Serve 2403.02310 confirmed as the same-line 2024 follow-up and bound
additively alongside the described 2023 paper).

## 8. AUTHORITY_RETRIEVAL_FAILED

None. All fetches succeeded; no transient retry pending.

## 9. AUTHORITY_NOT_FOUND (retained limitations)

F4 Jev independent writeup; AIPerf standalone product surface; Terminal-Bench
v1 original ID; standalone DeepSWE primary; peer-reviewed Jev reproduction/
evaluation; public Jev calibration protocol; non-MSR native-1-bit industrial
deployment. (Same as r1; none closed by assertion.)

## 10. MAYBE outcomes (20; none promoted/discarded)

Corroboration/context roles accepted for D072/D074/D075/D079/D080/D082/D084/
D085/D117/D120/D146/D147/D152/D156 (+ validity exhibits D097/D099/D100,
pricing sample D076); watches D086 (MiniMax) / D087 (gpt-oss) held for Sol
pursue/park; KDA collision (D085), IndexPool-adjacent harness gaps (D084),
follow-up pools (D152/D156) deferred to Sol. Promotion is a Sol materiality
judgment.

## 11. Capstone status (2026, body-consumed where load-bearing)

- V4.1 Flash: report §-level + recipe/PR-verified; per-figure appendix pins open.
- Qwen3.8-Flash-Next: report §-level + Tab.11 + port-verified; ablation tables open.
- Kimi Linear: report §-level + NC-ND license fact; per-task tables + independent repro open.
- GLM-5.3-Flash: report/release/packaging-verified; multipliers quarantined; IndexPool + KDA-collision open.

## 12. Jev status

First-party core consumed with vendor quarantine; suitability/task-class
bounds documented; independent reproduction + calibration protocol + CJK
accuracy remain thin (stated limitation, not closed).

## 13. X-community status (D162, PARTIAL/MATERIAL)

X_OBSERVATION boundary preserved into accepted Card; reception/friction/
bottleneck claims only; self-reported measurements configuration-bound.

## 14. F1–F4 status

F1 VERIFIED (D163), F2 PARTIAL/multipliers-quarantined (D164), F3 VERIFIED
(D165), F4 `INDEPENDENT_WRITEUP_NOT_RESOLVED` (no record, no substitution).

## 15. EFF-O13/O14/O15 status (Completeness rows, all LIMITATION)

- O13 (attention_sequence_kv_cache): D143/D144/D145/D146/D147 bound; bodies
  section-scope; PLE lineage parallel/unresolved.
- O14 (decoding_acceleration): D148/D149/D150/D151/D152/D153 bound with
  body-consumed numbers; survey follow-ups deferred.
- O15 (inference_kernels_serving): D154/D155/D156/D157 bound with body
  results; D158 accepted DROP recorded.

## 16. Benchmark-methodology status (O12, LIMITATION)

Seed taxonomy + harness standards + GenAI-Perf tooling accepted; SWE-Pro/
RULER/TBench identities supplement-bound; AIPerf open; per-figure pins open.
No naked cross-condition comparison in any accepted Card.

## 17. Remaining PARTIAL/UNRESOLVED records

148 PARTIAL Cards (scope per accepted Card limitations); 40 records carry
UNRESOLVED verification targets (enumerated from accepted Cards): D004-t2,
D017-t2, D028-t2, D031-t2, D039-t2, D047-t2, D050-t2, D051-t2, D052-t2,
D054-t2, D058-t2, D063-t2, D064-t2, D066-t2, D075-t2, D076-t2, D078-t2,
D084-t2, D085-t2, D086 (both), D087 (both), D088-t2, D089-t2, D091-t2,
D095-t2, D097 (both), D099 (both), D100-t2, D113-t2, D114-t2, D119-t2
(AIPerf), D123-t2 (appendix pins), D127-t2, D129-t2, D132-t2, D135-t2,
D142-t2, D152-t2, D156-t2, D164-t2 (MTP independence). Full finding text in
the accepted Cards. Former HOLDs (D032/D093) carry no UNRESOLVED target.

## 18. Compatibility + frozen validation accounts

- Projection: 160 tasks, 67 projected / 93 passthrough; per-type counts
  PRIMARY_DOC 13, PRIMARY_REPO 21, PRIMARY_ANNOUNCEMENT 8,
  PRIMARY_MODEL_CARD 6, PRIMARY_SPEC 4, SECONDARY_REFERENCE 8,
  SECONDARY_TECHNICAL 4, RUNTIME_RECIPE 1, PACKAGING_DOCS 1, RUNTIME_PR 1.
- `COMPATIBILITY_REPRODUCIBILITY: PASS`.
- Frozen Core judged every output (see compat `validation-report.md`).
  CV2-DM-016: `OPEN_CORE / EDITION_WORKAROUND`; `WORKAROUND_VALIDATED`.

## 19. Bodies richer than normalized claims (Sol sampling list)

V4.1 appendix/§3-§4 detail, Qwen ablations, Kimi per-task tables, V3.2/V4
ablations, MTP appendices, s1 ablations, RouteLLM results tables, TTC- and
routing-survey follow-ups, ezyang tensor audit,
recipe benchmark annexes, PR follow-up commits, Unsloth plots, SWE-Pro
full-text sections, Sarathi-Serve tradeoff analysis.
