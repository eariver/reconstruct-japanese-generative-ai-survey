# SUPERSEDED by sp-substantive-review-r2.md (root §1 corrections) — history preserved below, do not use as current binding.

# SP substantive Selection/Architecture review — fresh independent (not author/operator/root)

Reviewer: Fresh independent SUBSTANTIVE SP-efficient-llm-2026 reviewer, not SP author/operator/root/Human.
No prior authorship of `candidate-selection-v2.json`, `architecture-v2.json`, `architecture-review-summary-v2.json`,
`architecture-review-attention-v2.json`, orchestration input/audit, or packet DATA.
Read-only via `Read` + stdlib `json/hashlib/pathlib` inventory only.
No Git, no runtime/project imports, no tests, no network, no source/State/outputs/guard writes,
no subagents, no reconstruct readback. Packet-local writes only for this review.
No R4, no Human approval, no adoption/net-savings claim.

Actual UTC: 2026-11-17. Writes allowed in this new packet only:
`notes/rephase-1-selection-architecture-resume-20261117/sp-substantive-review.md` +
machine JSON + `sp-architecture-dossier-ja.md`. No source/State/canonical mutation.

Governance: `docs/survey-production-core-v2-sol-luna-review-governance.md` FULL (211 lines) controls.
Role split: Luna/Work execution + `READY_FOR_ARCHITECTURE_REVIEW` never substitutes for Sol semantic review
or Human-facing dossier. This review is Sol substantive review of actual 3231 outputs, not mechanical binding.

Prior closeout: `notes/rephase-1-selection-scaling-repair-20261116/astra-closeout-resolution.md` FULL (§§1–7),
repair §§10–13, independent `final-implementation-review.md` §§10–12 WITH FINAL-BINDING,
`independent-real-output-review.md` §10 + machine (SP audit 64-hex corrected), index + pack
`source-packaging/final-20261116T031000Z/` read. Earlier BLOCKED §§1–9 preserved as history.

## 0. Authority basis (actual pins, not historical summaries)

- Real repo: `.rephase-1-editorial-runtime/selection-scaling-real-20261116T021943Z/candidate-work`,
  frozen source `3231a0c280287411513bba359f4d3d2b6703f591`,
  parent `ae0dd1ee5b0e7a85c44bdab0e6cd024bf12f0c56`,
  tree `ff01b73e6012fd4519fdfb3807186753ff330367`.
  Complete DIRECT409 final143/774 manifest `0dc361cb8284f3465243120b7cea8e20476c3fbe81d90a71ce3028dd43eed150`/187361B,
  patch `76ac1318cd58311a5a7c0d924ee26b2bdff68dc815e75014a1aacd517e51fd6b`/5691014B.
  This execution commit is NOT a genuine Human-reviewed commit.
- SP State: `sources/SP-efficient-llm-2026/production-state.json` 4266B
  `38a6341107a401128d32537cda101321b42b5ec9088d07baba43b2adc4014bde`,
  lifecycle `EVIDENCE_REVIEWED`, init480/forward-history4/Human pending, guard absent, 7 downstream slots absent.
  Preserved, no stage advance.
- Active PREARCH record:
  `sources/SP-efficient-llm-2026/research/v2/acceptance-revisions/sp-repaired-20261112-r2/checkpoint/record.json`
  6300B `2a528ed533010da6acc9efaef0e24fb59be62417724b00919e0c2f6983fec9f5`,
  kind `PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1`, revision `sp-repaired-20261112-r2`.
  Old canonical NOT used.
- Active typed PREARCH 4 refs (CP `record.json:artifacts`, typed `artifact_refs`, all exist+match in real copy):
  - evidence-acceptance: `candidate/evidence-runs/dddee8c75d0247d21266adefde1c9e14c6043c90b9aaaaffba1f674ce3db7249/evidence-accepted.json`
    49237B `7f04e9adeddb327b085ede65de70638777a77a99810952bfdd44b6053a9a3327`, count 160.
  - edition-views-acceptance: `candidate/views-runs/e307d78f6a34fc7a708821b3d62ad83db8e52ac716c5411c6383dd6f69aab038/edition-views-accepted.json`
    64222B `45d60f9f19371ba9ae55f528cd20f674f0fbf4315bdabbfa4a4bedde6ba90939`, count 160.
  - materiality-ledger: `candidate/materiality-ledger.json`
    66850B `5cf81f8f2997d6784da12d805f5cfb54b6c9ebd3b94a2424983b5b591275bdc1`, count 165.
  - profile-completeness: `candidate/profile-completeness.json`
    34249B `b43786099456346b2eaf6f6f63f9636b5407aeedb8ba2c77840bac9adc915757`,
    overall `LIMITED`, obligations 15 (O01/O07 SAT, 13 LIM).
- Profile: `sources/SP-efficient-llm-2026/production-profile.json` 13748B
  `aff05fd573ce873afa24c0ede26c2b4591ee28b7048c9ed528e8fc389ed8ee45`,
  research `THEMATIC`, publication `LONGFORM_SPECIAL`, 12 scope_dimensions + 12 initial_obligations,
  temporal `OPEN_HISTORY_AS_OF` as_of `2026-09-21T16:10:00Z`. Named 3: Jev mandatory (O10),
  DSpark or verified equivalent (O05), as-of cutoff. O13–O15 from completeness.
- 7 generated Matrix/Selection/Architecture/Summary/Attention/Input/Audit (all `READY_FOR_ARCHITECTURE_REVIEW`,
  `ESTABLISHED`/`PROPOSED`, `human_review null/null`, no Human/stage advance):
  - `candidate-matrix-v2.json` 239359B `2f62e2a82af38ce0d8d9eaa405399a1b24df5b70d62a9872f3d5aa8549d81a8b`
  - `candidate-selection-v2.json` 76603B `4e6884d6bb8e8f5ca92b3344501687b686cd6355a65de69dfc98a9ab2e262a1f`
  - `architecture-v2.json` 33219B `4af84ab37d60145407adf393a519077aeb5debaea33f0f8305fda636a858396c`
  - `architecture-review-summary-v2.json` 67700B `d0092e132ecb9d094cf04a8ee97b1603bfaa777a18508f834a7a5a55c022a341`
  - `architecture-review-attention-v2.json` 15918B `482f3c215597e1d91726506149356f3dbd5190ac173233f1f6ee84acd362dd9f`
    (`total 65/shown 50/overflow 15/limit 50/truncated true`)
  - `orchestration/v2/interactive/selection-architecture-input.json` 72613B `072f90b6795041f79ab42476faf93ad9e39f7c80ce30e16c1804d4fcbd51e9bd` (== frozen input)
  - `orchestration/v2/interactive/selection-architecture-audit.json` 1530B `ad5474dafb79276d41a580aa48c394757195b7fe53a60bcd3092498254d15449`
    (corrected 64-hex, inner 6 refs match §3).
  Basis of matrix/selection/summary/attention equals 4 R2 SHAs + profile SHA; verified by parse.
  Active `materiality-ledger-v2.json` 66850B `b7c85b4eb009249b355445f94a4041d4374990fccb07c38595b61c1e770c8c60`
  and `profile-completeness-v2.json` 33683B `d67f7f8363407b30d58dbe2dbe562b3666ea9483f9f16303859cfe459ab5e805`
  are distinct by design (active vs CP R2), not a mismatch per output-review §4.
- Prior reuse (explicit bounded scopes, not whole-corpus PASS):
  `notes/rephase-1-repaired-correction-rehearsal-20261112/reviews/SP-selection-architecture-review.md`+machine
  (PROPOSAL_READY_FOR_PREFLIGHT, 130/14/116/30, Jev/D142/deployment/Engram/GenAI-Perf/X rules),
  `sp-selection-dossier-ja.md` + `sp-selection-per-did-map.json` + `sp-selection-read-scope.json`
  (pins/read-scope/method, 160 cards/views + 165 ledger + 15 obligations),
  accepted SP 4-record correction (D070/D071/D141 historical rebind + D142 INFERENCE narrow correction,
  r5–r8 dossiers + independent postprepare/adopt reviews, HIGH prepare/adopt binding),
  indep content review + archived captured 17 primary bodies (fixed c8 + 17 named SP URLs/version metadata
  per P5 `did-bodies.md`: papers/Jev/vLLM/PR27742/HF/Dynamo + 3 archive HTML u1/u2/u3 + S142 summary 3751B).
  Reuse is for input-to-output binding + targeted high-signal re-verification, not a substitute for
  full-corpus semantic read. Inventory ≠ full semantic read (see §5).

## 1. Counts: 130 = 14 PRIMARY + 116 SUPPORTING, HOLD 30, 5 nonmatrix DROP — verified not guessed

- Matrix 160 = SELECTED 130 + HOLD 30. Nonmatrix 5 EXCLUDED (`EFF-D140,D158,D159,D160,D161`) separate from 160;
  input covers every Matrix DID exactly once, no missing/duplicate/nonmatrix inclusion.
  Verified by stdlib parse + `candidate_id` set equality (160/160 equal, unique).
- Ledger 165 = 132 MATERIAL + 28 CONTEXT + 5 EXCLUDED.
  Selection splits MATERIAL 132 = 126 SELECTED + 6 HOLD (`D040,D049,D063,D142,D153,D162`);
  CONTEXT 28 = 4 SELECTED (`D070,D071,D119,D141`) + 24 HOLD.
  SELECTED 130 = 126 MATERIAL + 4 CONTEXT. Verified by matrix `materiality` join, not prose guess.
  This is editorial necessity, not all-MATERIAL autopick: 6 MATERIAL held for living-docs/current-only/
  unfetched/social reasons with explicit rationale; 24 CONTEXT held as secondary/pricing/watch/authority-only.
- 15 obligations honest 2 SAT / 13 LIM, no auto-SAT (O10 included as LIMITATION).
  Must-cover assignment covers all 15: p1→O01, p2→O02+O09, p3→O03, p4→O04+O13, p5→O05+O14,
  p6→O06+O07, p7→O08+O15, p8→O10, p9→O11+O12. No obligation dropped, no PRIMARY-every-obligation claim.
  New `architecture-v2.json` preserves this mapping; `selected_exceptions []` correct
  (all SELECTED placed; HOLD needs no exception).
- 9 packages 60 target / 75 max is claim-utility/pages arithmetic, not history quota and not arbitrary budget:
  14 PRIMARY × ~1pp (measured-effect + quarantine + figures) = 14pp,
  116 SUPPORTING × ~0.3pp (background/conditions) ≈ 35pp,
  thesis/intro/methodology overhead ≈ 11pp → 60pp target; layout/figure slack → 75 max.
  Inner p1 3 + p2 5 + p3 4 + p4 10 + p5 9 + p6 6 + p7 5 + p8 4 + p9 9 = 55pp + overhead 5pp = 60pp.
  HOLD 0pp, no appendix smuggling, history 66 unused. Coherent minimal split
  (major lanes + mandatory Jev + capstones/measurement) for 15 obligations.
  Page allocation in 60pp does not itself prove quality (see §4 compression analysis).
- Disposition/usage vs prior proposal: new 3231 SELECTED/HOLD + PRIMARY/SUPPORTING/NONE per discovery
  matches prior `sp-selection-architecture-input.json` 160/160 exactly (0 mismatch by stdlib join).
  Rationales preserve quarantine/boundaries; no silent re-disposition in generation.

## 2. Mandatory substantive cases (bounded vendor/current-only/social ceilings)

### 2.1 Jev historical D070/D071/D141 — included under bounded vendor case, not appendix waiver

- D070 launch SELECTED SUPPORTING p8: vendor historical served `2026-09-21T03:30:22Z`,
  wire gzip 42836B `10bf6607…`, CDX `6XH5…` MATCH, decoded 253542B `14ae3118…`.
  Claims strictly `VENDOR_CLAIM`: new arch + parallel sampler + RLCD name-only + 70–500ms / 40–200x /
  $0.042/MTok in + free out / 193.6x/444.6x with laptop/West-Coast/subsidy/authorship/OpenRouter bias admissions.
  RLCD internals undisclosed, independent repro outstanding (D073 leads only).
  Result card `task-b8b9f70a…` VERIFIED historical presence (vendor scope, conditional) + UNRESOLVED race/accuracy quarantine.
  As-of binding is memento served, not publication. Correct.
- D071 concepts SELECTED SUPPORTING p8: served `2026-09-21T04:13:55Z`,
  wire 49007B `62bf012c…`, CDX `TUIO…` MATCH, decoded 307198B `35770834…`.
  Choice/Score/Noul + parallel via state + group-level calibration verbatim first-party caveat
  (no per-answer guarantee) + text-only + decomposition/confidence-gated escalation as `VENDOR_CLAIM`.
  255-cardinality/score-then-choose ABSENT in archive visible text → excluded from as-of, stays current-only.
  API details belong to D142, not claimed here. Correct.
- D141 models SELECTED SUPPORTING p8: served `2026-09-20T20:50:53Z` via 302 from requested `21091419`
  (served-row CDX `ABQR…` MATCH, requested-row `E2BR…` NO-MATCH unserved, not served-as-requested).
  Plain 350662B `97a5dd74…`, jev-1.13.0-only (8 hits, both aliases →1.13.0, “no preview build right now”),
  $42/BTok in-only, 250k tok/s + 1200 req/min as PLATFORM RATE LIMITS (not measured throughput),
  64k (32k state + longest), text-only, shared RLCD weights, English-primary/CJK weaker.
  Nov 1.14 drift post-cutoff noted, no back-projection. Correct; table values are rate limits, not throughput proof.
- No appendix waiver: O10 stays LIMITATION, vendor quarantine retained,
  independent repro/RLCD/calibration NOT FOUND preserved. Dossier §2 + package boundaries correctly bind
  served/CDX/decoded pins and exclude current-only drift.

### 2.2 D142 unfetched — INFERENCE HOLD, no API truth

- D142 HOLD, usage NONE, no placement, no supplement entry, `source_bindings` key omitted (not null) per DM022 contract.
  Claims are INFERENCE only: token `INDEPENDENT_EVIDENCE_NOT_FOUND_AS_OF_2026-09-21`
  (S142 line 44 provenance, 3751B `f7eeec68…`) + summary-scope
  “no benchmark/calibration protocol located in that summary scope, body uninspected, not global absence proof.”
  Targets both UNRESOLVED. Materiality MATERIAL as relevant-but-unverified lead with HOLD ceiling,
  not verified claim. Correct ceiling; no schema/confidence-math/version/date/body consumption.
  U1/u2/u3 contain no API schema, so D142 is not closed by concepts.
  Models actual served Sept20 via Sept21 URL noted; no as-of smuggle of unserved `21091419`/pre-09-20 revisions.
  D071 missing cardinality claims excluded; summary-only, no independent calibration.

### 2.3 Current vLLM/Dynamo + inherited D040/D049/D063/D153 HOLD — not as-of content

- D004 Dynamo V4.1-Flash recipe HOLD (PARTIAL CONTEXT O01/O08/O11): SUMMARY_CAPTURED recipe docs,
  body not line-level, historical 09-21 UNCONFIRMED, topology/precision UNRESOLVED. No placement. Correct.
- D040 DSpark bundle HOLD (PARTIAL MATERIAL O05/O11): living vLLM docs + Dynamo recipe,
  paper-grade ablations absent, workload-measured only, as-of deployment not proved. No placement. Correct.
- D049 MXFP4 deployment HOLD (PARTIAL MATERIAL O06/O11): recipe docs current-only,
  dispatch code not audited, hardware conditions only. No placement. Correct.
- D063 Dynamo serving-lens HOLD (PARTIAL MATERIAL O04/O05/O06/O08/O11): joint reading only,
  body not line-level, experiment UNRESOLVED. No placement. Correct.
- D153 effort-control HOLD (PARTIAL MATERIAL O11/O14): current-model binding,
  card/interface not fetched, tier semantics summary-only. No placement. Correct.
- D163 vLLM recipe HOLD (PARTIAL CONTEXT O05/O08/O11): living docs current-only,
  version conditions UNRESOLVED, nightly drift, EVAL_ONLY governs serving. No placement. Correct.
- All current-only deployment held, not used as as-of factual proof. DSpark claimed only via
  V4.1 §2.4.3 + HF model architecture bounds (`dba1be0`), not deployment. No as-of smuggle.

### 2.4 D143 PRIMARY Engram — accepted actual data supports, with boundaries

- Result `task-53d9064c…` PARTIAL, PRIMARY_PAPER `https://arxiv.org/abs/2601.07372`, published 2026-01-12 (≤cutoff).
  Body-consumed §2 adaptations + allocation law + full delta table
  (MMLU +3.4/CMMLU +4.0/MMLU-Pro +1.8/BBH +5.0/ARC-C +3.7/DROP +3.3/HumanEval +3.0/MATH +2.4/GSM8K +2.2)
  + U-law/LogitLens + official repo release-level. `AUTHOR_CLAIM` quarantine preserved,
  allocation-curve/training-cost outstanding, Qwen-PLE parallel unresolved, kNN-LM/RETRO held as boundary precedents.
  PRIMARY for O13 (sparsity-axis, MoE complement) in p4-attention-engram exactly once is justified;
  O01/O03/O08/O09/O12 cross-mapped via V41/Qwen/Kimi/FrugalGPT/GenAI-Perf, not PRIMARY-every-obligation. Correct.

### 2.5 D119 GenAI-Perf vs AIPerf — unknown different, held distinct

- D119 SELECTED SUPPORTING p9 (PARTIAL CONTEXT O12): Triton tooling docs usable as `perf_analyzer` semantics,
  distinct from AIPerf open product. Result `task-d8b2a4aa…`: `LOCATOR_CAPTURED`,
  summary “Rate-controlled TTFT/ITL/throughput decomposition; AIPerf-as-product NOT located.”
  Repo not cloned, metric semantics docs-only, AIPerf identity open as LIMITATION.
  Placed for taxonomy/methodology background, no new benchmark numbers claimed. Correct separation; no conflation.

### 2.6 D162 social — no fact, HOLD lead only

- D162 HOLD, usage NONE, no placement, source_class SOCIAL, 27 obs/24 accounts/20 independent.
  Result `task-7dc41c44…`: claims are `SOCIAL_OBSERVATION` (local-deployment feasibility,
  early runtime support, self-reported 325 tok/s-class config-bound, Jev production-failure LOW_SIGNAL)
  with explicit low-signal/config-bound qualifiers. Per-observation verification absent,
  no technical/economic/license fact sourced. HOLD ceiling correct;
  O07/O08/O10/O11/O12 relevance preserved in text only, not as relevance proof.

## 3. Positive + negative cases, obligations, numerics, abstract-scope limits

- Positive measured-effect PRIMARY numerics all carry model/version/benchmark/date/harness/authority/vendor-vs-independent bindings + conditions:
  D008 Tab.11 14-benchmarks 1/3 tokens 1/9 FLOPs vendor-quarantined ablations outstanding;
  D027 fair-comparison section scope per-task tables section scope independent repro open;
  D030 README `dba1be0` CONFIRMED README-scope-only current drift UNCONFIRMED per-figure outstanding;
  D032 DSA debut URL isolated VERIFIED launch authority indexer equations belong to D125;
  D036 EAGLE 0.8 vs 0.6, greedy 3x/2x/1.6x, lossless distribution scope ablations outstanding;
  D123 V41 §2.4.3 + §3.2 section scope per-figure/scaffold outstanding figures not cited for fact;
  D125 indexer warm-up/parity excerpt scope full ablations outstanding;
  D143 delta table + U-law/LogitLens allocation-curve outstanding;
  D148 Snell 4x+ vs best-of-N 14x smaller verifier/revision ablations outstanding;
  D149 s1 s1K + budget forcing +27% over o1-preview quantity/diversity ablations structural;
  D150 ThinkPrune RL token-limit MATH500 ~83 R1-Distill-1.5B-only RL-cost outstanding;
  D151 overthinking peak-then-decline U_lambda early-stopping wins flip-mechanism section scope;
  D154 FrugalGPT cascade 50–98% Table3 matched-accuracy prices-stale-by-construction formulation outstanding;
  D165 merged PR27742 existence PR-reported numbers only no rebuild correctness not claimed.
- Negative cases explicit: HOLD 30 each with rationale (current-only/secondary/watch/unfetched/social/
  encoder-bridge/harness-caveats), 5 nonmatrix EXCLUDED separate, MiniMax/gpt-oss watches,
  AIME/DeepSWE/BrowseComp authority/methodology-only holds. No silent exclusion.
- Obligations: O01/O07 SAT with structural justification (bottleneck language; GGUF format + llama.cpp/
  KTransformers/offload + D165 existence, correctness not claimed for SAT). Other 13 LIMITATION with
  per-package `must_cover` + measured-effect PRIMARY + genealogy/background SUPPORTING split.
  Source class never treated as truth (`VENDOR_CLAIM`/`AUTHOR_CLAIM`/`PROJECT_CLAIM`/`SOCIAL_OBSERVATION`/`INFERENCE` labeled).
- Abstract-scope SUPPORTING cannot underpin unconsumed mechanism equations/per-figure:
  dossier §3/§5 + package boundaries enforce — p1 no coefficient/isoFLOP/scheduling detail + no cross-ranking;
  p2 prices/formulation outstanding; p3 per-expert micro-benchmarks excluded;
  p4 V41 Appx per-figure + Qwen ablations + Kimi per-task tables not cited + PLE parallel unresolved;
  p5 DSpark/Medusa per-body acceptance + HW/batching/quality outstanding + EAGLE/Snell/s1 ablations outstanding;
  p6 GGUF-not-algorithm + importance-matrix/mixed-quant/outlier/rebuild excluded + D165 correctness not claimed;
  p7 D061/D062 abstract-scope + survey unifier deferred; p8 vendor-as-vendor + no RLCD inference +
  no 255-as-of + no D142 schema/math + no independent bench/calibration; p9 GLM abstract-only +
  vendor ratios conditional + harness/scaffold outstanding + AIPerf distinct.
  Sampled SUPPORTING rationales consistently state “abstract scope / full-body outstanding /
  announcement/docs/spec scope.” No SUPPORTING is cited for exact equations it does not consume.
- Author's claimed missing vs already-captured-unconsumed:
  summary residual 5 (Discovery locators D005/D061/D062/D093/D094/D098/D112/D117/D139 wrong-identity bytes;
  full-body section/ablation outstanding; Jev thin; AIPerf unconsumed + MiniMax/gpt-oss unconfirmed;
  per-figure/version pins outstanding) are genuine missing/limitation, not hidden captured-but-unconsumed
  measured-effect. Where bodies ARE captured (Jev u1/u2/u3 decoded/plain bytes, S142 3751B, D143 paper,
  D030 `dba1be0`, D165 PR27742, V41/Qwen/Kimi section scope), consumption is bounded to what was read
  (vendor quarantine, section scope, README-scope, PR-reported-only) with outstanding detail explicit.
  No captured primary body would support a materially different measured-effect Architecture if fully consumed:
  held MATERIAL 6 are living-docs/current-only/unfetched/social, not concealed measured tables.
  Discovery locator wrong-identity bytes are supplemented by frozen-validated supplement (amendment deferred to Sol),
  not silently cited as locator truth.

## 4. 60-page outline: honestly answers reader question vs hiding gap + compression counterfactual

Reader question (profile research_scope): dense→“necessary compute/memory/generation/waste-avoidance/
generation-avoidance” architecture/systems co-design transition, where each technique originates,
which models adopt it, what measured effects/trade-offs with conditions.

- Thesis states vendor-vs-independent isolation, as-of 2026-09-21 primary sources,
  measured effects + trade-offs, current-only/secondary/watch held in dossier not publication.
  Goals forbid single-word speedup, cross-condition leaderboard implication, vendor-as-fact,
  appendix smuggling, and require 14 PRIMARY exactly once + 116 SUPPORTING ≥once + inherited boundaries.
- 60pp does not hide essential gaps: summary `residual_limitations` 5 + per-record boundaries preserve
  indispensable unsupported claims/gaps as LIMITATION (D142 body, RLCD internals/benchmark/calibration/
  independent repro, unserved u3 `21091419`/pre-09-20 revisions, D141 card-vs-current alias contradiction as
  root/normal-producer business, vLLM/Dynamo pinned-09-20 proof, per-figure pins V41 Appx B/C/Qwen ablations/
  Kimi tables/routing/TTC tables/harness/scaffold/version pins, AIPerf standalone surface, MiniMax/gpt-oss mechanisms).
  These are preserved, not PASSed. Outline's per-package boundaries explicitly mark outstanding detail as outstanding.
- Compression counterfactual (governance §4.4): `SELECTED 130` while `non-DROP 160` and `VERIFIED 8` —
  extreme compression test applies (SELECTED >>1, so not sparse-issue case, but 116 SUPPORTING at ~0.3pp
  still requires scrutiny). Test: *if captured primary authorities were fully consumed,
  could a materially different multi-item Architecture be supported?*
  Answer: No on current evidence. Held MATERIAL 6 cannot supply alternative measured core
  (D040 living-docs bundle, D049 recipe-only, D063 joint-reading-only, D142 unfetched INFERENCE,
  D153 summary-only current binding, D162 social-only). Held CONTEXT 24 are secondary/pricing/watch/
  authority-only. SELECTED PRIMARY 14 each carry section/table-scoped measured-effect with quarantine;
  alternative of promoting a HOLD to PRIMARY would require new historical pin (vLLM/Dynamo 09-20),
  new API body (D142), or new paper-grade ablations (DSpark) — none captured. Decompressing SUPPORTING
  to 1pp each would inflate to ~130pp without new measured claims, not a different thesis.
- Reasonable alternatives considered and rejected:
  (a) all-MATERIAL autopick (132 PRIMARY) — rejected: conflates relevance with measured-effect, ignores HOLD ceilings;
  (b) Jev appendix waiver (exclude D070/D071/D141) — rejected: mandatory O10 case must appear as quarantined vendor case, not vanish;
  (c) vLLM/Dynamo as as-of deployment proof — rejected: current-only, no pinned-09-20 proof, would smuggle as-of;
  (d) AIPerf-as-product + GenAI-Perf conflation — rejected: distinct identities, AIPerf surface unconsumed;
  (e) X promotion to SUPPORTING — rejected: social-only, no technical fact.
  9-package structure (bottleneck/scaling/MoE/attention-engram/decoding/precision/serving/Jev/capstones)
  is minimal coherent covering of 15 obligations; merging Jev into serving or capstones into methodology
  would obscure mandatory quarantine and measurement taxonomy. No silent Special narrowing:
  necessary Special viability (THEMATIC/LONGFORM_SPECIAL reader-facing technical, 9 packages, 60/75pp,
  thesis + lineage + conditions) is explicitly required, not narrowed to 2–3 lanes.
- Risk: 116 SUPPORTING at ~0.3pp could tempt equation/figure over-citation.
  Mitigated by explicit “abstract-scope background only, no per-figure/ablation/table citation” boundaries +
  per-DID limits. Draft must enforce citation-boundary check; this DATA does not authorize Draft.

## 5. Actual per-DID / high-risk / attention-overflow review (existing Raw read, no new fetch)

Method: stdlib parse of actual 3231 `candidate-matrix-v2` (160 rows) + `candidate-selection-v2` (160 assignments) +
`architecture-v2` (9 packages) + `architecture-review-summary-v2` + `architecture-review-attention-v2`
(65 total/50 shown/15 overflow) + `selection-architecture-audit.json` (input +5 outputs pins);
prior R2 `results/task-*.json` + `views/view-*.json` spot-reads + ledger/completeness/profile +
packet R2 decision/dossier/addenda reused as bounded evidence; targeted card-level `source_bindings`
only (Jev served/CDX/decoded, D142 absent, D119 docs, D143 paper, D030 `dba1be0`, D165 PR27742).
No broad Raw re-read; archive bodies as MATERIAL DATA per independent followup, not re-fetched.
No new Human question needed before normal stage.

- D070/D071/D141/D142: full re-verification above (§2.1–2.2). Literals visible-body bound,
  quarantine retained, rate-limit qualifier present, 255 absent honored, D142 narrow INFERENCE + HOLD ceiling correct.
  Prior 156/156 unaffected cards+views byte+parsed exact, 3 supp-ID rotations only, ledger 165 parsed-identical,
  O10 archive-aware LIMITATION + FULL 8-field closure verified — reused, not recounted.
- D143 Engram: body-consumed allocation law + delta table + U-law/LogitLens, repo release-level,
  PLE parallel unresolved, kNN/RETRO boundaries held. PRIMARY justified.
- D119 GenAI-Perf: docs-only SUPPORTING, AIPerf distinct open. Correct.
- D162 X: SOCIAL lead only, no fact. HOLD correct.
- D008 Qwen3.8-Next / D030 V4.1 card / D032 V3.2-Exp launch / D036 EAGLE / D148–D151 TTC /
  D154 FrugalGPT / D165 PR27742 / D123 V41 report / D125 V3.2 report / D027 Kimi Linear:
  section/table/headline numbers with per-figure/ablation outstanding, drift quarantine,
  PR-reported-only/existence-only boundaries as in §3. PRIMARY each exactly once justified.
- HOLDs D004/D040/D049/D063/D153/D163 + 24 CONTEXT holds: sampled tasks show
  SUMMARY_CAPTURED/living-docs/secondary/pricing/watch/harness-caveat status; HOLD no-placement correct, not as-of proof.
- Ledger/views/completeness: 160/160 cards/views read via prior + spot checks;
  132 MATERIAL/28 CONTEXT confirmed; 15 obligations 2 SAT/13 LIM + residual 5 + FULL 8-field closure read;
  profile 12+3 + as-of read. No count PASS alone; substantive limits above govern use.
- Attention 65 eligible rows inventoried from actual screening-ledger-selection (review DATA, not canonical producer):
  `MATERIALITY:EXCLUDED 5` (D140/D158–D161) + `SCREENING:DROP 5` (same 5, park-leaning/boundary probes) +
  `SCREENING:INSPECT 5` (D032/D077/D093/D119/D150: homepage-only locator, AI-drafted study, Which-Pro normalization,
  AIPerf identity, ThinkPrune body-unread) + `SCREENING:MAYBE 20`
  (D072/D074/D075/D076/D079/D080/D082/D084/D085/D086/D087/D097/D099/D100/D117/D120/D146/D147/D152/D156:
  secondary corroboration/pricing/launch analyses, watches, harness caveats, boundary precedents, secondary surveys) +
  `SELECTION:HOLD 30` (shown 15 + overflow 15). Shown 50 = 5+5+5+20+15; overflow 15 = remaining HOLD.
  Shown HOLD 15: D117/D082/D120/D077/D049/D142/D153/D079/D163/D146/D156/D084/D072/D100/D074
  (encoder-bridge, secondary analyses, caveated harness, infra study, MXFP4 current-only, API unfetched,
  effort-control summary-only, vLLM recipe current-only, kNN boundary, routing survey secondary,
  LM Studio secondary, Jev wiki secondary, DeepSWE note, Jev explainer).
  Overflow HOLD 15 (negative-space, not hidden): D004/D040/D063/D073/D075/D076/D080/D085/D086/D087/D097/D099/D147/D152/D162
  (Dynamo recipe, DSpark bundle MATERIAL, Dynamo lens MATERIAL, OmniJev hub, Lambda provider, DeepInfra pricing,
  NVIDIA Qwen blog, NIM GLM card, MiniMax watch, gpt-oss watch, BrowseComp, AIME authority, RETRO precedent,
  TTC survey secondary, X SOCIAL MATERIAL). High-signal MATERIAL 6 HOLD all inventoried (3 shown: D049/D142/D153;
  3 overflow: D040/D063/D162) with HOLD ceilings preserved; no silent exclusion, no appendix smuggling.
  Full 65 + 30 HOLD + 5 DROP item-level list in machine JSON; counts match
  `total 65/shown 50/overflow 15` + `SELECTED 130/HOLD 30` + `EXCLUDED 5`.
- Exact unique IDs read scope (this review, new 3231 bytes parsed):
  matrix 160 `candidate_id` + selection 160 `candidate_id` (=160 discovery-mapped: D001–D039,D041–D062,D064–D071,
  D078,D081,D083,D088–D098,D101–D116,D118/D119,D121–D145,D148–D151,D154/D155,D157,D164/D165 SELECTED;
  D004,D040,D049,D063,D072–D077,D079/D080,D082,D084–D087,D097,D099/D100,D117,D120,D142,D146/D147,D152/D153,
  D156,D162/D163 HOLD; D140/D158–D161 nonmatrix EXCLUDED) + 9 packages + summary + attention 50 shown items +
  audit 7 pins. Primary material inspected via prior bounded content review + targeted re-verification above
  (D070/D071/D141/D142 full, D143/D119/D162/D008/D030/D032/D036/D123/D125/D027/D148–D151/D154/D165 section/table scope),
  not whole-corpus semantic read. Inventory ≠ full semantic read; no whole-corpus PASS claimed.
  Prior reuse is explicit, not a substitute for future Draft citation-boundary checks.

No additional Raw fetch needed; existing Raw pins sufficient. No new Human question before normal stage.

## 6. Mechanical input schemas, placement, IDs, boundaries, future shapes

- Interactive runner shape `_validate_input` (read as DATA, no execution): top 5 keys
  (`schema_version,issue_id,runner,assignments,architecture`), assignment 7 keys
  (`discovery_id/disposition/rationale/architecture_usage/publication_role/architecture_role/profile_extensions`
  in prior input; new `candidate-selection-v2` uses `candidate_id` with same 7-shape semantics),
  architecture 7 keys (`editorial_thesis,architecture_goals,page_plan,packages,selected_exceptions,
  profile_extensions,publication_extensions`), package 10 keys
  (`package_id,title,purpose,primary_candidate_ids/supporting_candidate_ids,must_cover_requirements,
  boundaries,drafting_order,profile_extensions,publication_extensions`).
  NEW outputs obey all sets; `schema_version 2.0-rc1`, `issue_id SP-efficient-llm-2026`,
  assignments cover every Matrix DID exactly once, dispositions/usage enums valid,
  HOLD rows `NONE` + null roles, rationales non-empty, thesis/goals/page/packages/exceptions/extensions valid,
  page target/max positive, package IDs unique, discovery refs within matrix,
  primary∩supp ∅ per package, drafting_order 1–9 ints, extensions dicts.
- Placement: PRIMARY exactly one package (14/14 verified: p4×5, p5×5, p6×1, p7×1, p9×2);
  SUPPORTING ≥one package (116/116 placed, each ≥1 supporting list); HOLD unplaced (30/30 no package, usage NONE).
  `selected_exceptions []` correct (all SELECTED placed; HOLD needs no exception).
- Inherited boundaries: every package has non-empty unique `boundaries` preserving source/claim limits
  (total 199: 5/23/20/37/16/25/23/15/35 per p1–p9; W34 total 97 separate).
  Token-safe IDs: `p1-bottleneck,p2-scaling-adaptation,p3-moe,p4-attention-engram,p5-decoding-testtime,
  p6-precision-local,p7-serving-routing,p8-specialization-jev,p9-capstones-measurement`
  — lowercase hyphen, unique, drafting_order 1–9 sequential. No empty package
  (min p1 0+3, p8 0+3, others larger). Empty-last-synthesis rule satisfied
  (no empty synthesis placeholder; all packages purposeful, exceptions empty).
- Future Longform source contract shapes: this DATA is NOT canonical `candidate-selection-v2`
  (`candidate_id…`)/`issue-architecture-v2` (`primary_candidate_ids…`)/Longform reader input.
  Actual canonical generation + normal Selection/Architecture transitions require later bounded root dispatch
  with `run_selection_architecture_v2_interactive` resolving Discovery IDs → deterministic Matrix candidates,
  basis pins (profile/candidate-matrix/completeness/ledger/selection), seven-slot no-overwrite preflight,
  and independent review. No approval/Draft/PDF here. Longform Draft must use
  `longform-reader-input-v2` / derivation / synthesis shapes, not this interactive shape.

## 7. Minimal indispensable gaps (preserved LIMITATIONS, not preflight blockers)

With existing Raw read, before any Human question:

1. D142 API body unfetched; schema/confidence-math/version/date/body outstanding; INFERENCE HOLD preserved.
2. RLCD internals undisclosed; Jev benchmark/calibration methodology + independent reproduction outstanding (community leads only).
3. Unserved u3 `21091419` revision + pre-09-20 revisions unacquired (served-row only).
4. D141 accepted-side card-vs-current alias contradiction correction is root/normal-producer business (this DATA only proposes scope).
5. vLLM/Dynamo pinned-09-20 historical proof absent (current-only quarantined).
6. Per-figure pins outstanding (V41 Appx B/C, Qwen ablations, Kimi tables, routing/TTC tables, harness/scaffold/version pins)
   + AIPerf standalone surface unconsumed + MiniMax/gpt-oss mechanisms unconfirmed.
7. Abstract-scope SUPPORTING must not be cited for unconsumed equations/per-figure (boundaries enforce at Draft).

None blocks normal stage (mechanical + substantive DATA ready); all must be preserved as LIMITATION
through canonical generation and Draft citation-boundary checks.

## 8. Verdict

**EDITORIAL_READY_FOR_NORMAL_STAGE** — bounded substantive Selection/Architecture DATA ready for root
normal `build_stage_checkpoint` / `advance_with_checkpoint` toward SELECTION_COMPLETE, not Selection PASS,
not Architecture PASS, not R4 audit, not quality/adoption/savings, not Human approval.

- No concrete CHANGES required to matrix/selection/architecture/summary/attention/audit before normal stage.
  Counts, dispositions, packages, obligations, numerics conditions, Jev/D142/deployment/Engram/GenAI-Perf/X rules,
  mechanical shapes, placement, IDs, boundaries, empty-exception rule all satisfy.
- Actual canonical `candidate-selection-v2` / `architecture-v2` + seven-slot generation, normal Selection/Architecture
  transitions, Draft/PDF, R4, Human Gates remain future bounded work after root dispatch + independent review.
  `ARCHITECTURE_ESTABLISHED` remains pending Human Architecture review.
- Whole NOT_READY / DM021+022 OPEN / audit unstarted / quality-adoption-savings OPEN preserved.
  Stop at Human Commit Point; ordinary Commit/Push Human-owned.

## 9. Bounds

Independent substantive review only; no source/State/Profile/CP/supplement/Raw/guard/Selection write,
no project runtime/imports/tests/Git/network/Production, no subagents, no new fetch
(source permission completed), no R4/generic-reader/PDF/ordinary commit/readback/Production.
Evidence is durable packet-local DATA + actual 3231 reads; old ae0 proof preserved,
DATA/archives unadopted except via normal HIGH R2 already completed.
Inventory is review DATA, not canonical producer; prior bounded scopes reused explicitly, not whole-corpus PASS.
Source 3231 execution commit is NOT genuine Human-reviewed commit; State remains EVIDENCE_REVIEWED;
no approval requested. Root review required before stage actions.
