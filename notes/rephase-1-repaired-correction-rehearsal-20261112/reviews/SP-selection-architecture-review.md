# SP Selection/Architecture independent editorial review — NEW reviewer (not SP author/operator)

Reviewer: NEW independent editorial Selection/Architecture reviewer, not current SP DATA author/operator/Human. No prior authorship of `sp-selection-architecture-input.json`, `sp-selection-dossier-ja.md`, `sp-selection-per-did-map.json`, `sp-selection-read-scope.json`. Read-only review via `Read` + packet DATA; no current Source State write, no project imports, no tests, no Git, no network, no Production, no subagents. No R4, no full-corpus quality, no Human approval inferred.

Actual UTC: 2026-11-14 (packet writes explicitly allowed for this review only; no source/State mutation).

## 0. Authority basis (actual pins, not historical summaries)

- Runtime: `.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work`, artifact-only HEAD `ae0dd1ee5b0e7a85c44bdab0e6cd024bf12f0c56`, parent `cc1c7fd1cf979e71fda4ae2168282b37bc1b2325`, tree `ec11cf6c49b3cdf54c7aa98703d6b3e74806dc58`. Source773 `a7e40c4711a66b4d1d2541e6af1a97fd0e531d217e233f45ce43b40e19cef40c` unchanged.
- SP State: `sources/SP-efficient-llm-2026/production-state.json` 4266B `38a6341107a401128d32537cda101321b42b5ec9088d07baba43b2adc4014bde`, lifecycle `EVIDENCE_REVIEWED`, init480/forward-history4/Human pending, guard absent, seven downstream slots absent.
- Active PREARCH record: `sources/SP-efficient-llm-2026/research/v2/acceptance-revisions/sp-repaired-20261112-r2/checkpoint/record.json` 6300B `2a528ed533010da6acc9efaef0e24fb59be62417724b00919e0c2f6983fec9f5`, kind `PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1`, revision `sp-repaired-20261112-r2`. Old canonical four refs NOT used.
- Active R2 VERSIONED four refs (bound for this review):
  - evidence-acceptance: `candidate/evidence-runs/dddee8c75d0247d21266adefde1c9e14c6043c90b9aaaaffba1f674ce3db7249/evidence-accepted.json` 49237B `7f04e9adeddb327b085ede65de70638777a77a99810952bfdd44b6053a9a3327`, count 160.
  - edition-views-acceptance: `candidate/views-runs/e307d78f6a34fc7a708821b3d62ad83db8e52ac716c5411c6383dd6f69aab038/edition-views-accepted.json` 64222B `45d60f19371ba9ae55f528cd20f674f0fbf4315bdabbfa4a4bedde6ba90939`, count 160.
  - materiality-ledger: `candidate/materiality-ledger.json` 66850B `5cf81f8f2997d6784da12d805f5cfb54b6c9ebd3b94a2424983b5b591275bdc1`, count 165.
  - profile-completeness: `candidate/profile-completeness.json` 34249B `b43786099456346b2eaf6f6f63f9636b5407aeedb8ba2c77840bac9adc915757`, overall `LIMITED`, obligations 15 (O01/O07 SAT, 13 LIM).
- Profile: `sources/SP-efficient-llm-2026/production-profile.json` 13748B `aff05fd573ce873afa24c0ede26c2b4591ee28b7048c9ed528e8fc389ed8ee45`, research `THEMATIC`, publication `LONGFORM_SPECIAL`, 12 scope_dimensions + 12 initial_obligations (O01–O12), temporal `OPEN_HISTORY_AS_OF` as_of `2026-09-21T16:10:00Z`. Named 3: Jev mandatory (O10), DSpark or verified equivalent (O05), as-of cutoff. O13–O15 from completeness (Engram/TTC/routing).
- Packet inputs reviewed (DATA, not authority):
  - `sp-selection-architecture-input.json` (160 assignments + architecture 9 packages, runner DATA)
  - `sp-selection-dossier-ja.md` (human-facing dossier draft)
  - `sp-selection-per-did-map.json` (per-DID disposition/usage/packages/limits)
  - `sp-selection-read-scope.json` (pins/read-scope/method)
  - Root `astra-operation-resolution.md` §§1–18 FULL, esp. §18 restart-from-active-refs; packet `README.md` current.
  - Prior `outputs/rephase-1-selection-architecture-assessment.md` (PARTIAL/BLOCKED history, 63pp/85pp conditional hypothesis, not quota).

## 1. Counts: 130 = 14 PRIMARY + 116 SUPPORTING, HOLD 30, 5 nonmatrix drop — not autopick, not arbitrary budget

- Matrix 160 = SELECTED 130 + HOLD 30. Nonmatrix 5 EXCLUDED (`EFF-D140,D158,D159,D160,D161`) separate from 160; input covers every Matrix DID exactly once (lines 11–170 = 160 assignments), no missing/duplicate, no nonmatrix inclusion. Verified by line inspection + per-did-map cross-check.
- Ledger 165 = 132 MATERIAL + 28 CONTEXT + 5 EXCLUDED. Selection splits MATERIAL 132 = 126 SELECTED + 6 HOLD (`D040,D049,D063,D142,D153,D162`); CONTEXT 28 = 4 SELECTED (`D070,D071,D141,D119`) + 24 HOLD. SELECTED 130 = 126 MATERIAL + 4 CONTEXT. This is editorial necessity, not all-MATERIAL autopick: 6 MATERIAL held for living-docs/current-only/unfetched/social reasons with explicit rationale; 24 CONTEXT held as secondary/pricing/watch/authority-only.
- 15 obligations mapping honest 2 SAT / 13 LIM, no auto-SAT (O10 included as LIMITATION). Must-cover assignment covers all 15: p1→O01, p2→O02+O09, p3→O03, p4→O04+O13, p5→O05+O14, p6→O06+O07, p7→O08+O15, p8→O10, p9→O11+O12. No obligation dropped, no PRIMARY-every-obligation claim.
- 9 packages 60 target / 75 max is claim-utility/pages arithmetic, not history quota (63/85 + appendix 6 rejected as selected policy) and not arbitrary budget: 14 PRIMARY × ~1pp (measured-effect + quarantine + figures) = 14pp, 116 SUPPORTING × ~0.3pp (background/conditions) ≈ 35pp, thesis/intro/methodology overhead ≈ 11pp → 60pp target; layout/figure slack → 75pp max. Inner p1 3 + p2 5 + p3 4 + p4 10 + p5 9 + p6 6 + p7 5 + p8 4 + p9 9 = 55pp + overhead 5pp = 60pp. HOLD 0pp, no appendix smuggling, history 66 unused. Coherent minimal split (major lanes + mandatory Jev + capstones/measurement) for 15 obligations.

## 2. Mandatory substantive cases

### 2.1 Jev mandatory case — historically bound vendor scope, not appendix waiver
- D070 launch SELECTED SUPPORTING p8: vendor historical served `2026-09-21T03:30:22Z`, wire gzip 42836B `10bf6607…`, CDX `6XH5…` MATCH, decoded 253542B `14ae3118…`. Claims strictly VENDOR_CLAIM: new arch + parallel sampler + RLCD name-only; 70–500ms / 40–200x / $0.042/MTok in + free out / 193.6x/444.6x with laptop/West-Coast/subsidy/authorship/OpenRouter bias admissions. RLCD internals undisclosed, independent repro outstanding (D073 leads only). Result card `task-b8b9f70a…` VERIFIED historical presence (vendor scope, conditional) + UNRESOLVED race/accuracy quarantine. As-of binding is memento served, not publication. Correct.
- D071 concepts SELECTED SUPPORTING p8: served `2026-09-21T04:13:55Z`, wire 49007B `62bf012c…`, CDX `TUIO…` MATCH, decoded 307198B `35770834…`. Choice/Score/Noul + parallel via state + group-level calibration verbatim first-party caveat (no per-answer guarantee) + text-only + decomposition/confidence-gated escalation as VENDOR_CLAIM. 255-cardinality/score-then-choose ABSENT in archive visible text → excluded from as-of, stays current-only. API details belong to D142, not claimed here. Correct.
- D141 models SELECTED SUPPORTING p8: served `2026-09-20T20:50:53Z` via 302 from requested `21091419` (served-row CDX `ABQR…` MATCH, requested-row `E2BR…` NO-MATCH unserved, not served-as-requested). Plain 350662B `97a5dd74…`, jev-1.13.0-only (8 hits, both aliases →1.13.0, “no preview build right now”), $42/BTok in-only, 250k tok/s + 1200 req/min as PLATFORM RATE LIMITS (not measured throughput), 64k (32k state + longest), text-only, shared RLCD weights, English-primary/CJK weaker. Nov 1.14 drift post-cutoff noted, no back-projection. Correct.
- No appendix waiver: O10 stays LIMITATION, vendor quarantine retained, independent repro/RLCD/calibration NOT FOUND preserved. Dossier §2 and input rationales correctly bound served/CDX/decoded pins and exclude current-only drift.

### 2.2 D142 unfetched — INFERENCE HOLD, no API truth
- D142 HOLD, usage NONE, no placement, no supplement entry, `source_bindings` key omitted (not null) per DM022 contract. Claims are INFERENCE only: token `INDEPENDENT_EVIDENCE_NOT_FOUND_AS_OF_2026-09-21` (S142 line 44 provenance, 3751B `f7eeec68…`) + summary-scope “no benchmark/calibration protocol located in that summary scope, body uninspected, not global absence proof.” Targets both UNRESOLVED. Materiality MATERIAL as relevant-but-unverified lead with HOLD ceiling, not verified claim. Correct ceiling; no schema/confidence-math/version/date/body consumption. U1/u2/u3 contain no API schema, so D142 is not closed by concepts. Independent postprepare decision already holds this as BOUNDED gap, not proof.

### 2.3 Current vLLM/Dynamo + inherited D040/D049/D063/D153 HOLD — not as-of content
- D004 Dynamo V4.1-Flash recipe HOLD (PARTIAL CONTEXT O01/O08/O11): SUMMARY_CAPTURED recipe docs, body not line-level, historical 09-21 UNCONFIRMED, topology/precision UNRESOLVED. No placement. Correct.
- D040 DSpark bundle HOLD (PARTIAL MATERIAL O05/O11): living vLLM docs + Dynamo recipe, paper-grade ablations absent, workload-measured only, as-of deployment not proved. No placement; DSpark claimed only via V41 §2.4.3 + README dba1be0 architecture bounds, not deployment. Correct.
- D049 MXFP4 deployment HOLD (PARTIAL MATERIAL O06/O11): recipe docs current-only, dispatch code not audited, hardware conditions only. No placement. Correct.
- D063 Dynamo serving-lens HOLD (PARTIAL MATERIAL O04/O05/O06/O08/O11): joint reading only, body not line-level, experiment UNRESOLVED. No placement. Correct.
- D153 effort-control HOLD (PARTIAL MATERIAL O11/O14): current-model binding, card/interface not fetched, tier semantics summary-only. No placement. Correct.
- D163 vLLM recipe HOLD (PARTIAL CONTEXT O05/O08/O11): living docs current-only, version conditions UNRESOLVED, nightly drift, EVAL_ONLY governs serving. No placement. Correct.
- All current-only deployment held, not used as as-of factual proof. Dossier §2 correctly quarantines vLLM/Dynamo to appendix/dossier, not publication.

### 2.4 D143 PRIMARY Engram — accepted actual data supports, with boundaries
- Result `task-53d9064c…` PARTIAL, PRIMARY_PAPER `https://arxiv.org/abs/2601.07372`, published 2026-01-12 (≤cutoff). Body-consumed §2 adaptations + allocation law + full delta table (MMLU +3.4/CMMLU +4.0/MMLU-Pro +1.8/BBH +5.0/ARC-C +3.7/DROP +3.3/HumanEval +3.0/MATH +2.4/GSM8K +2.2) + U-law/LogitLens + official repo release-level. AUTHOR_CLAIM quarantine preserved, limitation allocation-curve/training-cost outstanding, Qwen-PLE parallel unresolved, kNN-LM/RETRO held as boundary precedents. PRIMARY for O13 (sparsity-axis, MoE complement) in p4-attention-engram exactly once is justified; O01/O03/O08/O09/O12 cross-mapped via V41/Qwen/Kimi/FrugalGPT/GenAI-Perf, not PRIMARY-every-obligation. Correct.

### 2.5 D119 GenAI-Perf vs AIPerf — unknown different, held distinct
- D119 SELECTED SUPPORTING p9 (PARTIAL CONTEXT O12): Triton tooling docs usable as `perf_analyzer` semantics, distinct from AIPerf open product. Result `task-d8b2a4aa…`: `LOCATOR_CAPTURED`, summary “Rate-controlled TTFT/ITL/throughput decomposition; AIPerf-as-product NOT located.” Repo not cloned, metric semantics docs-only, AIPerf identity open as LIMITATION. Placed for taxonomy/methodology background, no new benchmark numbers claimed. Correct separation; no conflation.

### 2.6 D162 social — no fact, HOLD lead only
- D162 HOLD, usage NONE, no placement, source_class SOCIAL, 27 obs/24 accounts/20 independent. Result `task-7dc41c44…`: claims are SOCIAL_OBSERVATION (local-deployment feasibility, early runtime support, self-reported 325 tok/s-class config-bound, Jev production-failure LOW_SIGNAL) with explicit low-signal/config-bound qualifiers. Per-observation verification absent, no technical/economic/license fact sourced. HOLD ceiling correct; O07/O08/O10/O11/O12 relevance preserved in text only, not as relevance proof.

## 3. Positive + negative cases, obligations, numerics, abstract-scope limits

- Positive measured-effect PRIMARY numerics all carry model/version/benchmark/date/harness/authority/vendor-vs-independent bindings + conditions:
  D008 Tab.11 14-benchmarks 1/3 tokens 1/9 FLOPs vendor-quarantined ablations outstanding; D027 fair-comparison section scope per-task tables section scope independent repro open; D030 README dba1be0 CONFIRMED README-scope-only current drift UNCONFIRMED per-figure outstanding; D032 DSA debut URL isolated VERIFIED launch authority indexer equations belong to D125; D036 EAGLE 0.8 vs 0.6, greedy 3x/2x/1.6x, lossless distribution scope ablations outstanding; D123 V41 §2.4.3 + §3.2 section scope per-figure/scaffold outstanding figures not cited for fact; D125 indexer warm-up/parity excerpt scope full ablations outstanding; D143 delta table + U-law/LogitLens allocation-curve outstanding; D148 Snell 4x+ vs best-of-N 14x smaller verifier/revision ablations outstanding; D149 s1 s1K + budget forcing +27% over o1-preview quantity/diversity ablations structural; D150 ThinkPrune RL token-limit MATH500 ~83 R1-Distill-1.5B-only RL-cost outstanding; D151 overthinking peak-then-decline U_lambda early-stopping wins flip-mechanism section scope; D154 FrugalGPT cascade 50–98% Table3 matched-accuracy prices-stale-by-construction formulation outstanding; D165 merged PR27742 existence PR-reported numbers only no rebuild correctness not claimed.
- Negative cases explicit: HOLD 30 each with rationale (current-only/secondary/watch/unfetched/social/encoder-bridge/harness-caveats), 5 nonmatrix EXCLUDED separate, MiniMax/gpt-oss watches, AIME/DeepSWE/BrowseComp authority/methodology-only holds. No silent exclusion.
- Obligations: O01/O07 SAT with structural justification (bottleneck language; GGUF format + llama.cpp/KTransformers/offload + D165 existence, correctness not claimed for SAT). Other 13 LIMITATION with per-package must_cover + measured-effect PRIMARY + genealogy/background SUPPORTING split. Source class never treated as truth (VENDOR_CLAIM/AUTHOR_CLAIM/PROJECT_CLAIM/SOCIAL_OBSERVATION/INFERENCE labeled).
- Abstract-scope SUPPORTING cannot underpin unconsumed mechanism equations/per-figure: dossier §3/§5 + package boundaries enforce — p1 no coefficient/isoFLOP/scheduling detail + no cross-ranking; p2 prices/formulation outstanding; p3 per-expert micro-benchmarks excluded; p4 V41 Appx per-figure + Qwen ablations + Kimi per-task tables not cited + PLE parallel unresolved; p5 DSpark/Medusa per-body acceptance + HW/batching/quality outstanding + EAGLE/Snell/s1 ablations outstanding; p6 GGUF-not-algorithm + importance-matrix/mixed-quant/outlier/rebuild excluded + D165 correctness not claimed; p7 D061/D062 abstract-scope + survey unifier deferred; p8 vendor-as-vendor + no RLCD inference + no 255-as-of + no D142 schema/math + no independent bench/calibration; p9 GLM abstract-only + vendor ratios conditional + harness/scaffold outstanding + AIPerf distinct. Sampled SUPPORTING rationales consistently state “abstract scope / full-body outstanding / announcement/docs/spec scope.” No SUPPORTING is cited for exact equations it does not consume.

## 4. 60-page outline: honestly answers reader question vs hiding gap

Reader question (profile research_scope): dense→“necessary compute/memory/generation/waste-avoidance/generation-avoidance” architecture/systems co-design transition, where each technique originates, which models adopt it, what measured effects/trade-offs with conditions.

- Thesis states vendor-vs-independent isolation, as-of 2026-09-21 primary sources, measured effects + trade-offs, current-only/secondary/watch held in dossier not publication. Goals forbid single-word speedup, cross-condition leaderboard implication, vendor-as-fact, appendix smuggling, and require 14 PRIMARY exactly once + 116 SUPPORTING ≥once + inherited boundaries.
- 60pp does not hide essential gaps: §6 lists indispensable unsupported claims/gaps as LIMITATION (D142 body, RLCD internals/benchmark/calibration/independent repro, unserved u3 `21091419`/pre-09-20 revisions, D141 accepted-side card-vs-current alias contradiction as root/normal-producer business, vLLM/Dynamo pinned-09-20 proof, per-figure pins V41 Appx B/C/Qwen/Kimi/routing/TTC/harness/scaffold, AIPerf standalone surface, MiniMax/gpt-oss mechanisms). These are preserved, not PASSed. Outline’s per-package boundaries explicitly mark outstanding detail as outstanding.
- Risk: 116 SUPPORTING at ~0.3pp could tempt equation/figure over-citation. Mitigated by explicit “abstract-scope background only, no per-figure/ablation/table citation” boundaries + per-DID limits. Preflight must enforce citation-boundary check at Draft; this DATA does not authorize Draft.

## 5. Actual per-DID sample / high-risk full review (existing Raw read, no new fetch)

Method: R2 candidate `results/task-*.json` + `tasks/task-*.json` + `views/view-*.json` spot-reads + ledger/completeness/profile + packet R2 decision/dossier/addenda; targeted card-level `source_bindings` only (Jev served/CDX/decoded, D142 absent, D119 docs, D143 paper, D030 dba1be0, D165 PR27742). No broad Raw re-read; archive bodies as MATERIAL DATA per independent followup, not re-fetched. 156 unaffected byte-eq noted from R2 decision; 4 affected deep-read.

- D070/D071/D141/D142: full re-verification above (§2.1–2.2). Literals visible-body bound, quarantine retained, rate-limit qualifier present, 255 absent honored, D142 narrow INFERENCE + HOLD ceiling correct. R2 decision 156/156 unaffected cards+views byte+parsed exact, 3 supp-ID rotations only, ledger 165 parsed-identical, O10 archive-aware LIMITATION + FULL 8-field closure verified.
- D143 Engram: body-consumed allocation law + delta table + U-law/LogitLens, repo release-level, PLE parallel unresolved, kNN/RETRO boundaries held. PRIMARY justified.
- D119 GenAI-Perf: docs-only SUPPORTING, AIPerf distinct open. Correct.
- D162 X: SOCIAL lead only, no fact. HOLD correct.
- D008 Qwen3.8-Next: v1 `17db868a…` 2363790B Tab.11 + 1/3–1/9 vendor self-comparison quarantine + GDN/QSA section scope, ablations outstanding. PRIMARY justified in p4 exactly once.
- D030 V4.1-Flash card: README dba1be0 `347c9db4…` 13110B CONFIRMED README-scope, current 452330B drift UNCONFIRMED, per-figure outstanding. PRIMARY in p9 exactly once justified with drift quarantine.
- D032 V3.2-Exp launch: DSA debut URL isolated VERIFIED, launch authority, indexer equations belong to D125. PRIMARY in p9 exactly once justified.
- D036 EAGLE: v3 `3484aad4…` 1865998B Fig.1 2.90x/3.07x/2.95x + 0.8 vs 0.6 + lossless + composable, ablations outstanding. PRIMARY in p5 exactly once justified.
- D148–D151 TTC: bodies section/table-consumed headline numbers (4x+/14x, +27%, ~83, peak-then-decline U_lambda), per-table ablations outstanding, effort-control via current-only, survey follow-ups deferred. PRIMARY each exactly once in p5 justified; O14 not O05 correctly separated.
- D154 FrugalGPT: v1 `035ae8b9…` Table3 50–98% matched-accuracy, prices stale, formulation outstanding. PRIMARY in p7 exactly once justified.
- D165 llama.cpp PR27742: merged existence `3728e08d…` 26122B + packet corroboration, PR-reported ppl 4.0068/4.0126 + 98% agreement + QSA/PLE scope, no rebuild/correctness. PRIMARY existence in p6 exactly once justified with no-rebuild boundary.
- D123 V4.1 report / D125 V3.2 report / D027 Kimi Linear: section/excerpt-scope measured (DSpark §2.4.3 + inference §3.2 scaffold unresolved; indexer warm-up/parity; fair-comparison section per-task tables section scope), figures/tables not cited for fact. PRIMARY each exactly once in p4 justified.
- HOLDs D004/D040/D049/D063/D153/D163 + 24 CONTEXT holds: sampled tasks show SUMMARY_CAPTURED/living-docs/secondary/pricing/watch/harness-caveat status; HOLD no-placement correct, not as-of proof.
- Ledger/views/completeness: 160/160 cards/views read via R2 decision + spot checks; 132 MATERIAL/28 CONTEXT confirmed; 15 obligations 2 SAT/13 LIM + residual 5 + FULL 8-field closure read; profile 12+3 + as-of read. No count PASS alone; substantive limits above govern use.

No additional Raw fetch needed; existing Raw pins sufficient. No new Human question needed before preflight.

## 6. Mechanical input schemas, placement, IDs, boundaries, future shapes

- Interactive runner shape `_validate_input` (read as DATA, no execution): top 5 keys (`schema_version,issue_id,runner,assignments,architecture`), assignment 7 keys (`discovery_id,disposition,rationale,architecture_usage,publication_role,architecture_role,profile_extensions`), architecture 7 keys (`editorial_thesis,architecture_goals,page_plan,packages,selected_exceptions,profile_extensions,publication_extensions`), package 10 keys (`package_id,title,purpose,primary_discovery_ids,supporting_discovery_ids,must_cover_requirements,boundaries,drafting_order,profile_extensions,publication_extensions`). NEW input obeys all sets; `schema_version 2.0-rc1`, `issue_id SP-efficient-llm-2026`, runner 4 keys non-empty, assignments cover every Matrix DID exactly once, dispositions/usage enums valid, HOLD rows `NONE` + null roles, rationales non-empty, architecture thesis/goals/page/packages/exceptions/extensions valid, page target/max positive, package IDs unique, discovery refs within matrix, primary∩supporting empty per package, drafting_order 1–9 ints, extensions dicts.
- Placement: PRIMARY exactly one package (14/14 verified: p4×5, p5×5, p6×1, p7×1, p9×2); SUPPORTING ≥one package (116/116 placed, each ≥1 supporting list); HOLD unplaced (30/30 no package, usage NONE). `selected_exceptions []` correct (all SELECTED placed; HOLD needs no exception).
- Inherited boundaries: every package has non-empty unique `boundaries` preserving source/claim limits (see §3). Token-safe IDs: `p1-bottleneck,p2-scaling-adaptation,p3-moe,p4-attention-engram,p5-decoding-testtime,p6-precision-local,p7-serving-routing,p8-specialization-jev,p9-capstones-measurement` — lowercase hyphen, unique, drafting_order 1–9 sequential. No empty package (min p1 0+3, p8 0+3, others larger). Empty-last-synthesis rule satisfied (no empty synthesis placeholder; all packages purposeful, exceptions empty).
- Future Longform source contract shapes: this DATA is NOT canonical `candidate-selection-v2` (`candidate_id…`) / `issue-architecture-v2` (`primary_candidate_ids…`) / Longform reader input. Actual canonical generation + normal Selection/Architecture transitions require later bounded root dispatch with `run_selection_architecture_v2_interactive` resolving Discovery IDs → deterministic Matrix candidates, basis pins (profile/candidate-matrix/completeness/ledger/selection), seven-slot no-overwrite preflight, and independent review. No approval/Draft/PDF here. Longform Draft must use `longform-reader-input-v2` / derivation / synthesis shapes, not this interactive shape.

## 7. Minimal indispensable gaps (preserved LIMITATIONS, not preflight blockers)

With existing Raw read, before any Human question:

1. D142 API body unfetched; schema/confidence-math/version/date/body outstanding; INFERENCE HOLD preserved.
2. RLCD internals undisclosed; Jev benchmark/calibration methodology + independent reproduction outstanding (community leads only).
3. Unserved u3 `21091419` revision + pre-09-20 revisions unacquired (served-row only).
4. D141 accepted-side card-vs-current alias contradiction correction is root/normal-producer business (this DATA only proposes scope).
5. vLLM/Dynamo pinned-09-20 historical proof absent (current-only quarantined).
6. Per-figure pins outstanding (V41 Appx B/C, Qwen ablations, Kimi tables, routing/TTC tables, harness/scaffold/version pins) + AIPerf standalone surface unconsumed + MiniMax/gpt-oss mechanisms unconfirmed.
7. Abstract-scope SUPPORTING must not be cited for unconsumed equations/per-figure (boundaries enforce at Draft).

None blocks preflight (mechanical + substantive DATA ready); all must be preserved as LIMITATION through canonical generation and Draft citation-boundary checks.

## 8. Verdict

**PROPOSAL_READY_FOR_PREFLIGHT** — bounded Selection/Architecture DATA proposal ready for root preflight + canonical generation + independent review. Not Selection PASS, not Architecture PASS, not R4 audit, not quality/adoption/savings, not Human approval.

- No concrete CHANGES required to input/dossier/per-did-map before preflight. Counts, dispositions, packages, obligations, numerics conditions, Jev/D142/deployment/Engram/GenAI-Perf/X rules, mechanical shapes, placement, IDs, boundaries, empty-exception rule all satisfy.
- Actual canonical `candidate-selection-v2` / `architecture-v2` + seven-slot generation, normal Selection/Architecture transitions, Draft/PDF, R4, Human Gates remain future bounded work after root dispatch + independent review. `ARCHITECTURE_ESTABLISHED` remains pending Human Gate.
- Whole NOT_READY / DM021+022 OPEN / audit unstarted / quality-adoption-savings OPEN preserved. Stop at Human Commit Point; ordinary Commit/Push Human-owned.

## 9. Bounds

Independent review only; no source/State/Profile/CP/supplement/Raw/guard/Selection write, no project runtime/imports/tests/Git/network/Production, no subagents, no new fetch (source permission completed), no R4/generic-reader/PDF/ordinary commit/readback/Production. Evidence is durable packet-local DATA + actual ae0dd1e runtime reads; old e84 proof preserved, DATA/archives unadopted except via normal HIGH R2 already completed.
