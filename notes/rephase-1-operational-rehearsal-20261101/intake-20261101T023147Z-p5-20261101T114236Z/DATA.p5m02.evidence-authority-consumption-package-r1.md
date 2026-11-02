# Evidence Authority-Consumption Package r1 — SP-efficient-llm-2026

Status: `STAGE_BLOCKED / LUNA_INPUT_READY / AWAITING_SOL_REVIEW`
Date: `2026-09-22`
Author role: Muse (Luna/Work execution role). This package is Luna-side
Evidence work product and gap-fill ledger; it is NOT a Sol review and does
not substitute the Sol authority-consumption / materiality review.

## 0. Stage state (read first)

- The canonical Evidence / Materiality / Completeness **production run did
  NOT complete**: `run_evidence_v2_interactive.py` fail-closes on a
  shared-Core defect (Evidence `SOURCE_CLASS_MAP` lacks 10 Thematic
  Discovery source types; 67/160 tasks blocked; first error `PRIMARY_DOC`
  on EFF-D004). Defect record:
  `execution/defects/shared-core-evidence-source-map-gap-20260922.md`.
  Shared Core unchanged.
- What IS complete: (a) Screening correction + Sol Screening PASS (separate
  records); (b) 160-record interactive Evidence input, validated against
  Core-built task targets
  (`execution/evidence-interactive-input/interactive-evidence.json`, SHA
  `6cac92b1a51e109a9596752d60263e7341506025211cca8dc619fa80f4229c85`);
  (c) this pass's authority-consumption findings below, which Sol can use
  directly after the Core repair re-run.
- Machine lifecycle remains `CANDIDATES_NORMALIZED`. Selection NOT started.

## 1. Evidence input counts

- Total non-DROP candidates entering Evidence: **160** (135 KEEP + 20 MAYBE
  + 5 INSPECT; 5 DROPs excluded).
- Interactive input census: status **155 PARTIAL / 5 VERIFIED**; materiality
  **134 MATERIAL / 24 CONTEXT / 2 HOLD** (HOLD: EFF-D032, EFF-D093).
- The 5 VERIFIED records: EFF-D070 (Jev launch), EFF-D071 (System One
  concepts), EFF-D141 (Jev models page), EFF-D163 (vLLM V4.1 recipe),
  EFF-D165 (llama.cpp Qwen PR) — each fully consumed from bound-locator
  pages with all task targets resolved.
- Source/authority-class counts (Discovery classes over the 160): see
  screening-review-package-r2 §9 minus the 5 PRIMARY_PAPER DROPs, i.e.
  PRIMARY_PAPER 92, PRIMARY_DOC 13, PRIMARY_REPO 21, PRIMARY_ANNOUNCEMENT 8,
  PRIMARY_MODEL_CARD 6, PRIMARY_SPEC 4, SECONDARY_REFERENCE 8,
  SECONDARY_TECHNICAL 4, x-community-signal 1, RUNTIME_RECIPE 1,
  PACKAGING_DOCS 1, RUNTIME_PR 1.

## 2. Primary bodies retrieved vs consumed (this pass)

Retrieved and consumed (claims extracted into the input):

- arXiv API metadata (title/abstract/dates/authors/category) for **all 95
  arXiv-linked Discovery records** — includes all abstract-consumable
  papers (foundations through 2026 capstones, benchmarks, O13–O15 lanes).
- Full pages fetched and consumed: DeepSeek V3.2-Exp launch + API-docs
  excerpts (D032 gap-fill), ezyang V4.1 parameter study (D077), NVIDIA
  Triton GenAI-Perf docs (D119), vLLM DeepSeek-V4.1-Flash recipe (D163),
  Unsloth GLM-5.3-Flash docs (D164), llama.cpp PR 27742 incl. commit
  messages (D165), TypeSafe Jev launch blog (D070), TypeSafe System One
  concepts (D071), TypeSafe Models page (D141).
- Search-excerpt gap-fill: SWE-bench-Pro true identity + results (D093),
  Terminal-Bench 2.0 identity (D094), DoReMi paper + CRFM summary (D139).

`AUTHORITY_CONSUMED` (claims extracted from retrieved bytes): the 95
abstract-consumed papers (at abstract scope, explicitly), the 9
fully-consumed pages above, and the X r3 ledger record (D162, via accepted
Sol-reviewed import, not re-crawled).

## 3. AUTHORITY_CAPTURED_BUT_UNCONSUMED list

Locator/summary-bound with no body consumption beyond Discovery summary
(repo/doc/spec/announcement/card bodies not fetched or audited):

- EFF-D004, EFF-D009, EFF-D017, EFF-D028, EFF-D029, EFF-D030, EFF-D031,
  EFF-D039, EFF-D048, EFF-D049, EFF-D050, EFF-D051, EFF-D052, EFF-D054,
  EFF-D056, EFF-D058, EFF-D063, EFF-D064, EFF-D065, EFF-D066, EFF-D072,
  EFF-D074, EFF-D075, EFF-D076, EFF-D078, EFF-D079, EFF-D080, EFF-D081,
  EFF-D082, EFF-D083, EFF-D084, EFF-D085, EFF-D086, EFF-D087, EFF-D095,
  EFF-D097, EFF-D099, EFF-D100, EFF-D113, EFF-D114, EFF-D118, EFF-D120,
  EFF-D121, EFF-D122, EFF-D127, EFF-D129, EFF-D130, EFF-D131, EFF-D132,
  EFF-D136, EFF-D142, EFF-D144, EFF-D157.
- Plus abstract-scope-only papers where full-body tables/proofs remain
  outstanding (all PARTIAL paper records; scope stated per-record).
- The 9 wrong-identity-locator records (§7) are additionally
  captured-but-unconsumed **at their bound bytes** (the bound bytes belong
  to unrelated papers).

## 4. AUTHORITY_RETRIEVAL_FAILED list

None. Every fetch attempted this pass succeeded (arXiv API batches,
9 full-page fetches, 4 search resolutions). No transient failure is pending
retry.

## 5. AUTHORITY_NOT_FOUND list

- F4 Jev independent writeup: `INDEPENDENT_WRITEUP_NOT_RESOLVED` (no
  Discovery record; unchanged from Screening).
- Standalone AIPerf product surface: successor named in current NVIDIA docs
  (GenAI-Perf phased out in favor of AIPerf) but no product page located or
  consumed (D119 limitation; upgraded from `NOT_FOUND` to
  `SUCCESSOR_NAMED_PRODUCT_UNCONSUMED`).
- Original Terminal-Bench v1 arXiv ID: family verified via 2.0 (2601.11868,
  ICLR 2026); v1 ID unpinned (D094 limitation).
- Standalone DeepSWE primary (D100 limitation).
- Independent peer-reviewed Jev reproduction/evaluation (D073/D142
  limitation; central Jev gap).
- Public calibration-measurement protocol for Jev confidence (D142).
- Non-MSR native-1-bit industrial deployment (D047/D135 limitation).

## 6. PARTIAL / UNRESOLVED summary

- 155/160 input records are PARTIAL (abstract-scope or locator-bound with
  explicit per-record limitations). This is the honest steady state, not a
  defect: full-body consumption of ~95 papers plus ~50 repo/doc/spec bodies
  exceeds one Luna pass and is scheduled across Sol-directed gap-fill loops.
- UNRESOLVED verification targets by record: D004-t2, D005, D028-t2,
  D039-t2, D047-t2, D050-t2, D051-t2, D052-t2, D054-t2, D058-t2, D061,
  D062, D063-t2, D064-t2, D066-t2, D075-t2, D076-t2, D078-t2, D084-t2,
  D085-t2, D086 (both), D087 (both), D088-t2, D089-t2, D091-t2, D093 (both),
  D094-t1, D095-t2, D097 (both), D098, D099 (both), D100-t2, D112, D113-t2,
  D114-t2, D117, D119-t2, D127-t2, D129-t2, D132-t2, D135-t2, D139, D142-t2,
  D152-t2, D156-t2, D164-t2. (t2 = second task target; full text in the
  input JSON.)
- HOLD materiality: D032, D093 (need Sol locator/binding judgment).

## 7. Locator-identity defects found (gap-fill triggers G-EV-01–11)

Mechanical arXiv-API title verification of all 95 arXiv-linked locators
found **9 wrong-identity bound locators** (typo-class: digit swaps/prefix
errors). Screening substance is unaffected (decisions were on described
substance), but no locator-cited publication use may rely on these bytes:

| Trigger | Record | Bound (wrong) | True identity (verified) |
|---|---|---|---|
| G-EV-01 | D005 FP8 Formats | 2206.06277 (gas-flow pipes) | 2209.05433 (direct ID fetch verified) |
| G-EV-03 | D061 Mooncake | 2411.01181 (dynamics) | 2407.00079 (title search verified) |
| G-EV-04 | D062 SARATHI | 2308.16315 (quantum dots) | 2308.16369 (title search verified) |
| G-EV-05 | D093 SWE-bench-Pro | 2503.01324 (federated learning) | 2509.16941 (web search; +2609.08149 Verified follow-up) |
| G-EV-06 | D094 Terminal-Bench | 2406.06750 (optics) | family via 2.0: 2601.11868 (v1 ID open) |
| G-EV-07 | D098 RULER | 2404.18532 (MileBench) | 2404.06654 (title search verified) |
| G-EV-08 | D112 PyramidKV | 2406.02032 (M2D-CLAP audio) | 2406.02069 (title search verified) |
| G-EV-09 | D117 DeeBERT | 2004.12918 (game theory) | 2004.12993 (title search verified) |
| G-EV-11 | D139 DoReMi | 2308.01833 (nano-drone) | 2305.10429 (web search; NeurIPS 2023) |
| G-EV-02 | D032 DSA URLs | homepage-only (no body) | v3-2-exp launch + deepseek-v3-2 pages isolated (bodies summarized from excerpts) |
| G-EV-10 | D119 AIPerf | product NOT located | successor named in NVIDIA docs; product surface open |

No Discovery/Evidence bytes were added (bounded gap-fill recorded only);
locator amendment deferred to Sol judgment. My own guessed IDs for FP8 /
DeeBERT / DoReMi were verified-WRONG before assertion (see session record);
only API-/search-verified identities are reported above.

## 8. INSPECT outcomes (all five resolved to a disposition)

- **D032** (DSA trace): PARTIAL/HOLD. Dedicated first-party URLs isolated
  (G-EV-02); homepage carries no authority. DSA substance rests on
  D125/D126. Needs Sol binding decision.
- **D077** (ezyang study): PARTIAL/CONTEXT. Page fully consumed; 552B/196B/
  16B/8B/890B derivations traced to report PDF + config + model.py +
  safetensors headers with on-page AI-drafted disclosure; handled as lead,
  not authority.
- **D093** (SWE-bench-Pro): PARTIAL/HOLD. True identity isolated (G-EV-05)
  with public/commercial/held-out + Verified-follow-up structure; bound
  locator wrong; body unconsumed. Needs Sol locator/binding judgment.
- **D119** (GenAI-Perf/AIPerf): PARTIAL/CONTEXT. Tooling authority consumed
  (metrics, load model, repo location match bound locator); AIPerf product
  surface open (G-EV-10).
- **D150** (ThinkPrune): PARTIAL/CONTEXT. Mechanism confirmed as learned RL
  pruning (token-limit + iterative tightening; R1-Distill-Qwen-1.5B halved
  on AIME24 at ~2% drop; code linked); full tradeoff tables outstanding.
  Real weight confirmed — no substitute needed.

## 9. MAYBE outcomes (20)

- Corroboration/context role confirmed: D072, D073 (with peer-reviewed-
  reproduction negative finding), D074, D075, D079, D080 (prefix-hit
  quarantine), D082, D084 (harness warning), D085 (KDA collision left open),
  D117 (precedent + locator defect), D120, D146, D147, D152, D156
  (follow-ups deferred to Sol).
- Watch items held for Sol pursue/park: D086 (MiniMax), D087 (gpt-oss),
  both PARTIAL/CONTEXT with mechanism unconfirmed.
- Validity exhibits held with rules, not numbers: D097, D099, D100.
- Pricing sample held as sample-only: D076 (official D031 schedule takes
  precedence).
- None promoted to KEEP-core; none discarded. Promotion is a Sol
  materiality judgment after the Core-repair re-run.

## 10. 2026 capstone Evidence status

- **DeepSeek V4.1 Flash**: report abstract consumed (D123: CED 8B/16B,
  CSA2, FP4-KV 890B/tok, SWA replay, 45T tokens, scaffold-bound appendix);
  recipe fully consumed (D163); card/launch corroborated (D030/D031);
  Dynamo dual-lens corroborated (D004/D063); V4 report consumed (D124);
  V3.2 DSA report + launch consumed (D125/D126); D032/D077 held as above.
- **Qwen3.8-Flash-Next**: architecture report consumed (D008: 125B/6B+51B,
  GDN/QSA, Muon, 1/3-tok/1/9-FLOP vendor ratios quarantined); README/card
  corroborated (D029); blog corroborated (D081); repo variant-boundary
  recorded (D127, footnote text open); llama.cpp PR fully consumed (D165);
  NVIDIA GB300 figures prefix-hit-quarantined (D080); llm-stats analysis
  quarantined (D079).
- **Kimi Linear**: paper consumed (D027: KDA, 48B/3B, KV-75%, 6x-decode
  vendor claims); repo release-level (D028, version pin open); FLA KDA
  release-level (D132, numerics open).
- **GLM-5.3-Flash**: GLM-5 report consumed (D128: 744B/40B, DSA adoption,
  async RL); repo matrix recorded (D129, IndexPool open); card identity
  recorded (D130); Z.ai ratios quarantined (D131); transformers port
  MTP-exclusion recorded (D083); Unsloth packaging fully consumed (D164,
  multipliers quarantined); Ascend tutorial corroborated (D052); NIM KDA
  collision open (D085); LM Studio table quarantined (D084).

## 11. Jev Evidence status

First-party core consumed (D070 launch incl. nuance admissions; D071
concepts incl. calibration-group caveat; D141 models page incl.
alias-drift); API contract summary-level (D142); community leads
existence-level with peer-reviewed-reproduction negative finding (D073);
wiki/explainer corroboration-only (D072/D074); X corpus LOW_SIGNAL on
production-failure evidence (D162). Vendor speed/cost/intelligence figures
quarantined throughout. Independent evaluation/reproduction + calibration
protocol remain the central open gaps (NOT_FOUND list, §5).

## 12. X/community Evidence status (D162)

PARTIAL/MATERIAL with X_OBSERVATION boundary preserved into
claims/limitations: reception/deployment/friction + bottleneck reports
usable; architecture/scores/prices/license/causal claims prohibited;
self-reported measurements configuration-bound. Ledger acceptance
(Sol r3 PASS) reused, not re-verified.

## 13. F1–F4 status

- F1 (D163): VERIFIED — version floor, DSpark-only/MTP-dropped, AMD
  refusal, layouts, offload validation scope.
- F2 (D164): PARTIAL — packaging facts verified; 3.3x/MTP multipliers
  quarantined.
- F3 (D165): VERIFIED — merged status, QSA/PLE/host-memory, validation
  method, documented gaps.
- F4: `INDEPENDENT_WRITEUP_NOT_RESOLVED` — no record, no substitution.

## 14. EFF-O13/O14/O15 status

- O13 (conditional memory): Engram paper consumed (D143: O(1) lookup,
  U-shaped law, iso-wins author-framed); repo release-level (D144);
  Qwen-PLE lineage ruled PARALLEL_OR_UNRESOLVED (D145); kNN-LM/RETRO
  boundary precedents consumed (D146/D147).
- O14 (test-time compute): lane origin (D148), s1 budget-forcing (D149),
  ThinkPrune resolved-to-weight (D150), overthinking cost case (D151),
  survey taxonomy adopted with follow-ups deferred (D152), effort-control
  binding corroborated via D163 (D153).
- O15 (routing): FrugalGPT cascade origin with staleness caveat (D154),
  RouteLLM preference routing (D155), 2026 survey unifier with follow-ups
  deferred (D156), fragility counterexample (D157); D158 accepted DROP.

## 15. Benchmark-methodology status (EFF-O12)

Seed taxonomy consumed (MMLU-Pro/GPQA/HLE/LiveCodeBench/SWE-bench/tau-bench
+ RULER-role with locator defect + Terminal-Bench family with v1 ID open +
  SWE-Pro identity resolved); harness standards recorded (BFCL
paper-counterpart open; lm-eval-harness; HELM; MLPerf scenarios); system
metrics tooling consumed (GenAI-Perf; LLMPerf as caveat exhibit); validity
rules recorded (version/split/harness/reasoning-budget/hardware binding;
name-is-not-contract; public-vs-private; pass@k semantics). No naked
cross-condition comparison made anywhere in the input.

## 16. Source bodies richer than the normalized claims

Any full-body paper inevitably is; explicitly flagged for Sol's
unselected-evidence sampling: V4.1 report eval appendix (D123), Qwen
ablations (D008), Kimi fair-comparison protocols (D027), GLM-5 RL infra
(D128), ThinkPrune tradeoff curves (D150), overthinking flip mechanism
(D151), Engram allocation law (D143), s1 ablations (D149), TTC survey
benchmarks (D152), routing survey follow-ups (D156), ezyang tensor audit
(D077), vLLM recipe benchmark annexes (D163), PR 27742 follow-up commits
(D165), Unsloth KLD/accuracy plots (D164).

## 17. Unresolved source conflicts

- D085 NIM "KDA" vs Kimi KDA: collision flagged, no conflation, unresolved.
- D145 Qwen-PLE vs Engram: ruled parallel/unresolved, no ancestry inferred.
- D031/D076 pricing: official schedule takes precedence over provider
  sample; no reconciliation performed.
- D079/D100 DeepSWE figures vs harness-dependence note: figures
  quarantined on both sides consistently; no conflict asserted.
- V4.1 "552B" counting conventions (backbone vs +Engram/DSpark/scales):
  D163/D077 conventions recorded; publication must pick one convention
  explicitly.

## 18. Reasons Selection must NOT yet proceed

1. The canonical Evidence/Materiality/Completeness production run never
   executed (shared-Core block, §0): no Evidence Cards, Edition Views,
   Materiality Ledger, or Completeness artifact exists. There is nothing
   for Selection to select from.
2. Nine locator-identity defects + two HOLD records require Sol
   locator/binding/pursue-park judgments first.
3. Materiality annotations in the preserved input are provisional
   (Luna-authored); Sol materiality/Selection review is pending by
   governance.
4. The failed run is failed evidence: after reviewed Core repair, the
   preserved input must be re-executed cleanly with zero carried-forward
   verdicts.

Successful stop wording for this run:
`EVIDENCE_STAGE_BLOCKED_BY_SHARED_CORE_DEFECT / SELECTION NOT STARTED`
(Sol Evidence review readiness will be declared after the Core-repair
re-run, not from this package alone).
