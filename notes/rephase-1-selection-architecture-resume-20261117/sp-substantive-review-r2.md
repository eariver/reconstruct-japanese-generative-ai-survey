# SP substantive Selection/Architecture review r2 — fresh independent, root §1 corrected (not author/operator/root)

Reviewer: Fresh independent SUBSTANTIVE SP-efficient-llm-2026 reviewer, not SP author/operator/root/Human.
No prior authorship of 3231 outputs or packet DATA. Read-only via `Read` + stdlib `json/hashlib/pathlib` only.
No Git, no runtime/project imports, no tests, no network, no source/State/outputs/guard/canonical writes,
no subagents, no reconstruct readback. Packet-local writes only for this r2 review.
No R4, no Human approval, no adoption/net-savings claim.

Actual UTC: 2026-11-17 r2. Writes: `sp-substantive-review-r2.md` + `sp-substantive-review-r2-machine.json` +
`sp-architecture-dossier-ja-r2.md` in `notes/rephase-1-selection-architecture-resume-20261117/`.
No source/State/canonical mutation. Root reviews before stage actions, no Human approval ask.

Authority: `astra-operation-resolution.md` FULL §§1–2 (prevails; corrects r1 stale statements),
governance `docs/survey-production-core-v2-sol-luna-review-governance.md` FULL,
prior `notes/rephase-1-selection-scaling-repair-20261116/astra-closeout-resolution.md` FULL,
repair §§10–13, `final-implementation-review.md` §§10–12 WITH FINAL-BINDING,
`independent-real-output-review.md` §10 + machine.
r1 `sp-substantive-review.md` + machine + `sp-architecture-dossier-ja.md` are SUPERSEDED history (top note only),
preserved, not current binding. This r2 corrects stale contradictions listed in root §1.

## 0. Authority basis — corrected (actual 3231 HAS 7 products; PREARCH R2 active; old canonical inactive)

- Real repo: `.rephase-1-editorial-runtime/selection-scaling-real-20261116T021943Z/candidate-work`,
  frozen `3231a0c280287411513bba359f4d3d2b6703f591` / parent `ae0dd1ee5b0e7a85c44bdab0e6cd024bf12f0c56` /
  tree `ff01b73e6012fd4519fdfb3807186753ff330367`. DIRECT409 final143/774 manifest `0dc361cb…`/187361B,
  patch `76ac1318…`/5691014B. Execution commit, NOT genuine Human-reviewed commit.
- SP State: `production-state.json` 4266B `38a63411…`, `EVIDENCE_REVIEWED`, init480/forward4/Human pending,
  guard absent. Preserved, no stage advance.
  CORRECTION from r1: current 3231 HAS 7 generated products present (14/14 with W34, see below).
  Old `7 slots absent` described old ae0 active (0/14) and failed shadow, not current real copy. Withdrawn.
- Active PREARCH: `sp-repaired-20261112-r2/checkpoint/record.json` 6300B `2a528ed5…`,
  `PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1`, r2. Old canonical NOT active.
- Typed PREARCH R2 4 refs (CP `record.json:artifacts`, exist+match):
  evidence `7f04e9ad…`/49237・160, views `45d60f9f…`/64222・160,
  ledger `5cf81f8f…`/66850・165, completeness `b4378609…`/34249・LIMITED 15 (O01/O07 SAT, 13 LIM).
  CORRECTION: active research authority is PREARCH R2. Old canonical Ledger/Completeness files
  `materiality-ledger-v2.json` 66850B `b7c85b…` and `profile-completeness-v2.json` 33683B `d67f7f…`
  are inactive lineage (distinct by design per output-review §4), NOT active authority. Do not label old canonicals active.
- Profile: `production-profile.json` 13748B `aff05fd5…`, THEMATIC/LONGFORM_SPECIAL, 12 dims + named3,
  as_of `2026-09-21T16:10:00Z`, `OPEN_HISTORY_AS_OF`.
- 7 generated products EXIST (generation ready done, no rerun writer needed):
  `candidate-matrix-v2.json` 239359B `2f62e2a8…`, `candidate-selection-v2.json` 76603B `4e6884d6…`,
  `architecture-v2.json` 33219B `4af84ab3…`, `architecture-review-summary-v2.json` 67700B `d0092e13…`,
  `architecture-review-attention-v2.json` 15918B `482f3c21…` (65/50/15),
  `orchestration/v2/interactive/selection-architecture-input.json` 72613B `072f90b6…` (== frozen),
  `orchestration/v2/interactive/selection-architecture-audit.json` 1530B `ad5474dafb…` (64-hex, inner 6 match).
  All `READY_FOR_ARCHITECTURE_REVIEW` / `ESTABLISHED`/`PROPOSED`, `human_review null`, no Human/stage advance.
  CORRECTION: withdraw r1 “canonical generation still future / actual canonical generation later” as generation task.
  Generation is done; no writer rerun. Future bounded work is normal stage checkpoint/advance
  (`build_stage_checkpoint` / `advance_with_checkpoint` toward SELECTION_COMPLETE), not regeneration.
- Prior reuse (explicit, bounded): prior SP-selection-architecture-review + machine, per-DID/readscope/dossier,
  accepted 4-record correction r5–r8 + indep postprepare/adopt, 17 retained bodies (fixed c8 + 3 archive u1/u2/u3 + S142).
  Reuse is input-to-output binding + targeted re-verification, not whole-corpus PASS.
  Full 65 inventory retained with bind hash below; exact 15 overflow + 3 high-signal MATERIAL preserved.

## 1. Counts (verified parse)

- Matrix 160 = SELECTED 130 + HOLD 30. Nonmatrix 5 EXCLUDED separate. 160/160 `candidate_id` equal, unique.
- Ledger 165 = 132 MATERIAL + 28 CONTEXT + 5 EXCLUDED.
  MATERIAL 132 = 126 SELECTED + 6 HOLD (D040/D049/D063/D142/D153/D162).
  CONTEXT 28 = 4 SELECTED (D070/D071/D119/D141) + 24 HOLD. SELECTED 130 = 126M+4C.
- Obligations 15: 2 SAT / 13 LIM, O10 LIMITATION, no auto-SAT. Must-cover maps p1→O01 … p9→O11+O12, `selected_exceptions []`.
- Packages 9, 60 target / 75 max (claim-utility/pages arithmetic, not history quota).
- Attention 65/50/15, counts `MATERIALITY:EXCLUDED 5 / SCREENING:DROP 5 / SCREENING:INSPECT 5 / SCREENING:MAYBE 20 / SELECTION:HOLD 30`.
  Shown 50 = 5+5+5+20+15. Overflow 15 + shown 15 = HOLD 30. Bind hash `482f3c21…`/15918B retained.
- Disposition vs prior proposal: 160/160 match, no silent re-disposition.

## 2. Mandatory cases — corrected labels

### 2.1 Jev D070/D071/D141 — bounded vendor case; D141 alias already fixed in r2

- D070 u1 served `2026-09-21T03:30:22Z` 42836B `10bf6607…` CDX MATCH 253542B `14ae3118…`,
  D071 u2 served `2026-09-21T04:13:55Z` 49007B `62bf012c…` CDX MATCH 307198B `35770834…`,
  D141 u3 served `2026-09-20T20:50:53Z` via 302 from `21091419` 350662B `97a5dd74…`
  (served CDX MATCH, requested NO-MATCH unserved). All `VENDOR_CLAIM`, quarantine retained,
  255 absent honored, rate limits (250k tok/s + 1200 req/min) as PLATFORM limits not throughput.
- CORRECTION from r1 §7.4: D141 alias historical 1.13 fix is ALREADY ADOPTED in r2
  (result VERIFIED: served-scope 1.13.0-only, both aliases→1.13.0, Nov 1.14 drift post-cutoff noted not conflicting,
  claims stable across revisions, `version/alias binding` VERIFIED). No pending card-vs-current contradiction carried.
  Do not treat as open root/normal-producer business.

### 2.2 D142 — known locator, body NOT_ACQUIRED/UNINSPECTED, UNKNOWN (not NOT_FOUND / not RETRIEVAL_FAILED)

- Locator `https://docs.typesafe.ai/api` known. Body NOT fetched, no supplement entry, `source_bindings` absent (omitted, not null).
  Task `task-21ce0892d8846adffd6b.json` + result direct-read: status PARTIAL, sources `src-1` PRIMARY_OFFICIAL,
  claims INFERENCE x2 (token `INDEPENDENT_EVIDENCE_NOT_FOUND_AS_OF_2026-09-21` from S142 line 44 3751B `f7eeec68…`;
  summary-scope “no benchmark/calibration protocol located in that summary scope, body uninspected, not global absence proof”),
  limitations “Reference page not fetched; schema/confidence-derivation outstanding”,
  verification UNRESOLVED x2 (“page body outstanding … u1/u2/u3 contain no API schema … Real gap … no fetch” /
  “No public calibration protocol located in captured summary scope; API body uninspected … not global proof”).
- CORRECTED label: UNKNOWN / NOT_ACQUIRED / UNINSPECTED. No attempt-failure evidence, so NOT `AUTHORITY_NOT_FOUND`
  and NOT `AUTHORITY_RETRIEVAL_FAILED`. Summary-scope finding, not global absence proof.
  HOLD/NONE/no-placement ceiling correct. r1 `AUTHORITY_NOT_FOUND` bucket for D142 withdrawn.
- Direct read scope: task + result JSONs (above pins) read in this r2, not prior summary reuse alone.

### 2.3 D153 / D163 — exact capture history, no fabricated failure

- D153 `task-23d7c5bbe7624e7d2f94.json` (r3, `https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash`, SUMMARY_CAPTURED):
  result PARTIAL, verification VERIFIED “Effort-control role corroborated via consumed D163 (numeric effort, mapping tables,
  budget-room warnings); card bodies outstanding.” No failed retrieval; card bodies outstanding as LIMITATION.
- D163 `task-254e4aa47881a5cf54af.json` (r4/x-followup, `https://recipes.vllm.ai/...`, supplement `dbca6218…`,
  body DATA `sp14-vllm-recipe.html` 2705796B `fa61427e…`):
  result PARTIAL, verification UNRESOLVED x2 (“Recipe current … Vercel HIT no version header … pinned 2026-09-20 NOT verified;
  gap proven 0/13 commits <=cutoff … STOP” / “0.30.0+ floor … current-only; pinned-09-20 VERIFIED pending. Highest drift risk retained.”).
  SUMMARY_CAPTURED current-only, not failed acquisition. No fabricated `AUTHORITY_RETRIEVAL_FAILED`.
- Both HOLD/no-placement correct (current-only / card outstanding), not as-of proof. DSpark bound remains
  V41 §2.4.3 + HF `dba1be0` architecture only, not deployment.

### 2.4 Other deployment HOLDs

- D004/D040/D049/D063 same ceilings (living-docs/recipe-only/joint-reading-only, historical 09-21 UNCONFIRMED, topology UNRESOLVED).
  No as-of smuggle. Full HOLD list §5.

### 2.5 Engram / GenAI-Perf / X — narrow roles preserved

- D143 PRIMARY p4: allocation law + delta table + U-law/LogitLens, `AUTHOR_CLAIM` quarantine, PLE parallel unresolved,
  kNN/RETRO HOLD boundaries. Editorial PRIMARY for O13, not universal proof (see §3).
- D119 direct-read in this r2 (not prior reuse alone):
  task `task-d8b2a4aa00c15187f7f1.json` (LOCATOR_CAPTURED `https://github.com/triton-inference-server/perf_analyzer`) +
  result PARTIAL: source `supplement-src-6fe51b459a274631` PRIMARY_OFFICIAL
  (`https://docs.nvidia.com/.../genai-perf/README.html`, accessed 2026-09-22),
  claims PROJECT_CLAIM x2 (“measures output-token throughput, TTFT, ITL, request throughput … genai-perf/ …
  matching bound repo locator. Docs bytes consumed” / “being phased out in favor of AIPerf … no standalone AIPerf product surface was located”),
  limitations INFERENCE x2 (“repo itself not cloned; metric semantics rest on docs” / “AIPerf product identity … remains open”),
  verification VERIFIED (“Docs Raw consumed … confirmed”) + UNRESOLVED (“Successor named only; standalone product surface not located …
  not closed by assertion”). SELECTED SUPPORTING p9 docs-only, AIPerf distinct open. Correct separation; AIPerf open is
  preserved LIMITATION, not loadbearing for taxonomy use (see §4 Special).
- D162 HOLD SOCIAL lead only (27 obs, LOW_SIGNAL/config-bound, no technical fact). Correct.

## 3. PRIMARY is editorial role, not universal measured-effect proof

- CORRECTION from r1 §3 “Positive measured-effect PRIMARY numerics all carry …”:
  PRIMARY denotes editorial core-measured-effect placement, not that every PRIMARY proves a universal measured effect.
- Narrow cases explicit:
  - D165 `task-22eef64d61a9d277e7d5.json` VERIFIED: merged existence CONFIRMED (PR 27742, 65 commits/28 files, merged 2026-08-27),
    bound-body numericals at PR scope (ppl 4.0068/4.0126, 98% agreement, QSA/PLE/memory/gaps, UD-IQ1 2.84e-03).
    Category “merged PR = existence authority NOT correctness/independent rebuild.” PRIMARY existence in p6, no rebuild/correctness claim.
  - D032 `task-a44df8e64e8a20d94fc3.json` VERIFIED: launch announcement narrow (DSA debut on V3.1-Terminus base,
    50%+ price cut, artifact identities HF/GitHub/TileLang/CUDA). Launch authority + dedicated URL isolated, not mechanism proof.
    PRIMARY launch anchor in p9, indexer equations belong to D125.
- Other PRIMARYs remain section/table/headline-scoped with quarantine + outstanding ablations (Qwen Tab.11 vendor-quarantined,
  Kimi fair-comparison section scope, V41 §2.4.3/§3.2 section scope, V3.2 excerpt scope, EAGLE/Snell/s1/TTC headline scope,
  FrugalGPT Table3 prices-stale). No SUPPORTING cited for unconsumed equations/per-figure.

## 4. Outline, compression (no formal trigger), counterfactual (scoped), alternatives, Special viability

- Reader question + thesis/goals/page arithmetic as r1, with corrections:
  boundaries in review DATA are descriptive limits, NOT proved future Draft enforcement.
  Draft citation-boundary check remains future independent work; boundaries text alone does not constrain a future state.
- Governance extreme compression test: formal trigger `SELECTED <=1` while `non-DROP >=20` or `VERIFIED >=10`
  does NOT apply to SELECTED 130. r1 “extreme compression test applies” withdrawn as formal trigger.
  Voluntary dense assessment: 130 in 60pp (14×~1pp + 116×~0.3pp + overhead) is dense; 116 SUPPORTING at ~0.3pp
  assessed as background/conditions-only use with over-citation risk. Mitigation is future Draft check (not proved).
  No formal compression-PASS claimed.
- Scoped counterfactual (replaces r1 universal “No captured body would …”):
  On reviewed scope (65 inventory + targeted D119/D142/D153/D163/D141 direct reads + prior bounded reuse with limits),
  no concrete materially different multi-item Architecture is supported within HOLD ceilings:
  held MATERIAL 6 are living-docs/current-only/unfetched/social (D040 bundle, D049 recipe-only, D063 joint-reading-only,
  D142 unfetched INFERENCE, D153 summary-only current binding, D162 social-only); promoting any HOLD to PRIMARY
  would require new historical pin (vLLM/Dynamo 09-20), new API body (D142), or paper-grade ablations (DSpark) — none in retained captures.
  This is scoped review judgment with limits, NOT a universal “no captured body could ever support different core” claim.
  Full-corpus semantic read not claimed.
- Alternatives rejected (same 5 as r1, scoped): all-MATERIAL autopick, Jev waiver, vLLM/Dynamo as-of proof, AIPerf conflation, X promotion.
  9-package minimal covering of 15 obligations retained.
- Special viability (requested LONGFORM_SPECIAL necessary Special, not narrowed by abstract-only 116):
  9 packages preserve mandatory Jev + capstones/measurement + major lanes; abstract-only SUPPORTING are genealogy/background,
  not a silent narrowing to 2–3 lanes. Actual missing primary reading critical?
  AIPerf standalone surface open is NOT loadbearing for D119 docs-only taxonomy use (successor pointer preserved as LIMITATION).
  D142 body missing is HOLD (not in publication). No concrete loadbearing gap found in scoped review that would require
  BLOCKING for Special viability. If future Draft requires AIPerf product facts or per-figure pins, that is a Draft-stage gap,
  not a Selection BLOCKER here. No architecture editing/fetch in this review.

## 5. Per-DID / attention-overflow — full 65 retained, 30 HOLD / 5 DROP exact, direct-read scope

- Method: stdlib parse of actual 3231 matrix/selection/architecture/summary/attention/audit;
  direct Read of retained task/result JSONs for D119 + D142 + D153 + D163 + D141/D165/D032 (pins above);
  prior bounded reuse for remaining cards/views/ledger/completeness/profile + dossier/per-DID/readscope.
  No broad Raw re-read; archive bodies as MATERIAL DATA per followup, not re-fetched. No new Human question before normal stage.
- Attention 65 = EXCLUDED 5 (D140/D158–D161) + DROP 5 (same) + INSPECT 5 (D032/D077/D093/D119/D150) + MAYBE 20 + HOLD 30
  (shown 15: D117/D082/D120/D077/D049/D142/D153/D079/D163/D146/D156/D084/D072/D100/D074;
   overflow 15: D004/D040/D063/D073/D075/D076/D080/D085/D086/D087/D097/D099/D147/D152/D162).
  High-signal MATERIAL 6: shown D049/D142/D153 + overflow D040/D063/D162. Full item list in r2 machine JSON.
  Bind hash `482f3c21…`/15918B retained.
- Exact read scope (this r2, new 3231 bytes): matrix 160 + selection 160 + 9 packages + summary + attention 50 shown + audit 7 pins
  parsed; direct task/result reads: D119 (task+result), D142 (task+result), D153 (task+result), D163 (task+result),
  D141 (result), D165 (result), D032 (result). Remaining 150+ cards/views via prior explicit bounded reuse (156 byte-eq + 4 affected deep-read history),
  not recounted. Inventory ≠ full semantic read; no whole-corpus PASS.

## 6. Mechanical shapes / placement / IDs / future

- Same as r1 §6 (schemas, PRIMARY exactly once 14/14, SUPPORTING ≥once 116/116, HOLD unplaced 30/30,
  `selected_exceptions []`, boundaries non-empty total 199, token-safe IDs, drafting_order 1–9).
- CORRECTION: future is normal stage checkpoint/advance with seven-slot no-overwrite preflight + independent review,
  not canonical regeneration. Longform Draft shapes remain future; no approval/Draft/PDF here.

## 7. Indispensable gaps (LIMITATIONS, not stage blockers in scoped review)

1. D142 API body NOT_ACQUIRED/UNINSPECTED (UNKNOWN, summary-scope INFERENCE, UNRESOLVED x2).
2. RLCD internals/benchmark/calibration/independent repro outstanding.
3. Unserved u3 `21091419`/pre-09-20 unacquired (served-row only). D141 r2 alias fix done, no pending contradiction.
4. vLLM/Dynamo pinned-09-20 NOT verified (current-only, highest drift risk for D163).
5. Per-figure/version pins outstanding + AIPerf surface open + MiniMax/gpt-oss unconfirmed.
6. Abstract-scope SUPPORTING must not be cited for unconsumed equations/per-figure (future Draft check required, not proved by boundaries).
7. Discovery locator wrong-identity bytes supplemented by frozen-validated supplement (amendment deferred to Sol).

None is a concrete loadbearing Selection BLOCKER in scoped review; all preserved as LIMITATION through normal stage + Draft checks.

## 8. Verdict

**EDITORIAL_READY_FOR_NORMAL_STAGE (scoped, r2 corrected)** — bounded substantive DATA ready for root
normal `build_stage_checkpoint` / `advance_with_checkpoint` toward SELECTION_COMPLETE, not Selection/Architecture PASS,
not R4, not quality/adoption/savings, not Human approval.

- No concrete CHANGES to matrix/selection/architecture/summary/attention/audit before normal stage on reviewed scope.
- Generation done; no writer rerun. Pending is normal mechanical checkpoint/advance + independent review + Human Architecture review.
- Whole NOT_READY / DM021+022 OPEN / audit unstarted / quality-adoption-savings OPEN preserved.
- If root finds a genuine capability/authority gap at validation, return concrete finding before broadening (no auto generic reader).

## 9. Bounds

Independent substantive review only; packet DATA + actual 3231 reads; no Git/runtime/imports/tests/network/Production,
no source/State/Profile/CP/supplement/Raw/guard/Selection writes, no subagents, no new fetch, no R4/reader/PDF/commit/readback/Production.
Prior r1 preserved as history with top superseded note. Source 3231 is execution identity, not Human-reviewed commit;
State EVIDENCE_REVIEWED; no approval requested. Root review required before stage actions.
