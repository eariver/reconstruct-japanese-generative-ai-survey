# Independent Screening supervisory review — SP-efficient-llm-2026 ONLY (isolated)

**Role:** General independent supervisory reviewer — NOT Luna/Work execution author, NOT Sol, NOT Astra/root, NOT Human. No false attribution.

**File:** `notes/rephase-1-operational-rehearsal-20261101/reviews/screening-efficient-llm-review-20261101T111203Z.md`
**Wall-clock:** 2026-11-01T11:12–11:20Z.
**Bounds:** workdir READ-ONLY. No network, no Production checkout, no Commit readback, no Git mutation, no source edit, no runtime/import/test/build/fixture, no State write/advance, no deterministic record creation. Data-only `python3` stdlib hash/parse; unique evidence this file. No subagents. **SP ONLY** — W34 transport handled separately, unrun W34 not reviewed.

**Actual State (read-only):** SP `DISCOVERY_COLLECTED` (`machine_checkpoints.discovery passed, screening pending`), history last `ISSUE_INITIALIZED→DISCOVERY_COLLECTED 2026-11-01T11:00:23Z impl 48082356`. Checkpoint `orchestration/v2/checkpoints/ISSUE_INITIALIZED.json` exists (prior dispatch); NO screening checkpoint exists; NO advance attempted by this review.

**Workdir base:** `.rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work`, HEAD `480823560c0c26ed2e5baa18e0e79a22b2839a27`.

---

## 1. Exact read scope + input SHAs (current correct bytes only)

Fresh product (reviewed):

| artifact | bytes | SHA256 | notes |
|---|---|---|---|
| `sources/SP-efficient-llm-2026/screening/v2/accepted/9b9796295c2ddf28b087fc725b78b7d089d6e946a5a5ba65ab51601d58f558a9/screening-accepted.json` | 69226 | `6ff524b0a2c2c8f79603348acb86d18d39b180498a72ca92dc12f852dc786bf4` | 165 rec, KEEP135/MAYBE20/INSPECT5/DROP5, `result_set 9b979629…` |
| `…/package.json` | 2440 | `b094bacabd20159fba47d5238e39849086ccc70c54c6cb8661bcdd2b786acdb4` | basis profile `aff05fd5…`/state `c680db5a…`/discovery `7074cef2…`, prompt `3e45900e…`, contract `a05b65b4…`, 4 batches 50/50/50/15 |
| `…/interactive-audit.json` | 984 | `fc75f7d05d5423dd366ce3836be6630c8c5a387747d099173a0f74f126619697` | runner `Muse Spark (Luna/Work) 2026-09-22`, counts match accepted |
| `…/interactive-decisions.json` (accepted copy) | 68226 | `9290f406f640ce7fe231bd3aaa02ca5957c294808da23f1c10c1e1b6bead2ae3` | == proposed-input bytes, archived `DATA.p2g14` exact |
| `…/results/batch-001.json` | 21075 | `80b971a030d4…` | 50 decisions, schema `screening-v2-batch-result` |
| `…/results/batch-002.json` | 21460 | `4058e449aabf…` | 50 |
| `…/results/batch-003.json` | 20799 | `48a43f5fead2…` | 50 |
| `…/results/batch-004.json` | 7239 | `315fd3b32df2…` | 15 |
| `…/input/batches/batch-001.jsonl` | 49567 | `373b841635f9…` | 50 |
| `…/input/batches/batch-002.jsonl` | 48318 | `ef94487c18f6…` | 50 |
| `…/input/batches/batch-003.jsonl` | 50834 | `148cab870b9…` | 50 |
| `…/input/batches/batch-004.jsonl` | 17617 | `7384d1aadb8f…` | 15 |
| `sources/SP-efficient-llm-2026/screening/proposed-input/interactive-decisions.json` | 68226 | `9290f406f640ce7fe231bd3aaa02ca5957c294808da23f1c10c1e1b6bead2ae3` | staged archived decisions, `18a` missing 0/extra 0 vs fresh 165 |

Basis (not re-audited, pinned for binding):

- `sources/SP-efficient-llm-2026/production-profile.json` 13748B `aff05fd573ce873afa24c0ede26c2b4591ee28b7048c9ed528e8fc389ed8ee45` (THEMATIC/LONGFORM_SPECIAL, `OPEN_HISTORY_AS_OF 2026-09-21T16:10:00Z`, 12 dims, `O01–O12`, 12 inclusion + 11 exclusion).
- `sources/SP-efficient-llm-2026/discovery/discovery-v2.jsonl` 173299B `7074cef2…` (165), `discovery-accepted-v2.json` 135693B `2413dbe2…` (165, graph `441f488b…`, X `fa3a5055…`).
- `sources/SP-efficient-llm-2026/production-state.json` 3036B `c680db5ab2b1e35546fc48253dae06d0951d5c0bd18e2efed908af8e44b93e79` (current `DISCOVERY_COLLECTED`).
- Previous SourceIntake review FULL+CORR `reviews/source-intake-review-20261101T104700Z.md` 38557B `1d46058e…` (BOUNDED PROCEED both, residuals §5 retained).
- Intake original: 165 discovery + 25 Raws (per SourceIntake §1, 0 missing/mismatch); 26th `discovery-negative-space-2026-09-21.md` is Sol inventory, not Raw requirement.
- Pending Evidence: `execution/input-archive/SP/interactive-evidence-r2-adapted-O13-15.json` 345202B `f46dcf2f…` (160 rec PARTIAL148/VERIFIED12, 11 bindings, 15 obligs incl O13–15; r1 SUPERSEDED). Staged only, NOT accepted — body consumption NOT certified here.
- Governing docs read (no execution): `docs/survey-production-core-v2-sol-luna-review-governance.md` §§4.1–4.4/5, `docs/survey-production-core-v2-x-source-intake.md` §§2–3/6/10, `schemas/screening-v2-batch-result.schema.json` + `screening-v2-run-package.schema.json`, `config/prompts/source-screening-v2.md` via package pin (not re-read as text beyond pin).

Method: per-decision `discovery_id/decision/reason/scope_tags/duplicate_group/verification_targets/confidence` parsed for all 165; cross-checked against discovery `locator/source_type/summary_text/raw_paths` and raw headers (`SUMMARY_CAPTURED/LOCATOR_CAPTURED`) where meaningful; counts not used as proof.

---

## 2. Substantive judgment (not count comparison)

**Coverage, no silent narrow:** 165/165 exact (`18a` missing 0/extra 0). `scope_tags` span all lanes: `capstone-2026 43, serving 32, attention-kv 34, scaling-training 20, quantization 21, decoding 15, moe-routing 17, benchmark-methodology 23, efficiency-fundamentals 4, local-inference 7, specialization-jev 8, distillation-adaptation 8, conditional-memory 5, test-time-compute 6, model-routing 5`. All 12 profile dims + O13–15 represented. `duplicate_group` used truthfully for 6 lens-duplicate readings (`dynamo-v41-recipe-readings` D004/D063, `hf-qwen-card-readings` D029/D100, `hf-v41-card-readings` D030/D153); all others null — no false dedup, no hidden drop. Confidence `high 113/medium 34/low 18`; every decision has nonempty `reason` + ≥1 `verification_targets`; none empty.

**Question/inclusion/exclusion/asof consistency:** KEEP core tracks D01 bottleneck vocabulary, D02 scaling/Muon, D03 MoE lineage, D04 attention major lane, D05 decoding/MTP/DSpark, D06 precision/GGUF-as-format, D07 local/GGUF/llama.cpp/KTransformers, D08 serving/disaggregation, D09 distillation, D10 Jev mandatory case, capstones (V4.1-Flash/Qwen/Kimi/GLM-5.3), benchmark taxonomy — all within 12 inclusion lanes. Exclusions honored: no ranking/leaderboard (vendor numbers quarantined, comparability refused), no param-count-only comparison, no national ranking, no semiconductor/datacenter/prompt-catalog/consumer-rec/agent-list/multimodal-history/full-benchmark-history as thesis, and X/secondary NEVER as spec authority (see below).

**Needed sources/counterevidence retained (KEEP/MAYBE/INSPECT = selection for Evidence, NOT verification):**

- Capstones: D008 Qwen report, D027 Kimi, D030 V4.1 card, D123 V4.1 report, D128 GLM-5 report, D070 Jev launch — all KEEP with `vendor quarantine/spec binding` VTs. Runtime/PR/packaging: D004/D063 Dynamo (topology-conditional), D029 Qwen README (self-report quarantine), D031 launch (paper outstanding), D052 Ascend tutorial, D075 Lambda MAYBE secondary-rebind, D076 DeepInfra MAYBE not-official, D079/D082 llm-stats MAYBE quarantine, D080 NVIDIA MAYBE condition-bound, D084 MAYBE harness warning, D085 MAYBE KDA-collision, D127 GitHub source-of-truth, D129/D130/D131 GLM card/docs, D163 vLLM recipe (DSpark-only + AMD refusal separates architecture vs maturity), D164 Unsloth packaging (3.3x quarantined), D165 llama.cpp port (gaps documented). All bounded, no primary overclaim.
- Benchmark lane: D092 SWE-bench, D094 Terminal-Bench (version suffix), D098 RULER, D112 PyramidKV KEEP; D093 Which-Pro, D097 BrowseComp, D099 AIME/MAA, D100 DeepSWE, D117 DeeBERT, D119 GenAI-Perf/AIPerf, D120 LLMPerf MAYBE/INSPECT with version/harness/standalone VTs — validity-first preserved.
- Counterevidence: X counter-signals (quant/long-context brittleness) via D162 + R4 F1–F4 retained (DSpark topology, MTP drop, AMD refusal, packaging caveats, `F4` unresolved `INDEPENDENT_WRITEUP_NOT_RESOLVED`, no Discovery record) — not closed.
- X reception lead: single X record D162 KEEP, reason `never spec authority`, scope `benchmark/capstone/local/serving/jev`, VT full-body + boundary. No model spec/benchmark/date/license/priority asserted from X alone — exclusion honored.

**DROP5 justified (all match discovery's own park flags, not silent):** D140 phi synthetic (`park-leaning, indirect, no distinct mechanism`), D158 MoA (`collaboration not selection`), D159 DistilBERT / D160 MiniLM / D161 Wanda (`PARK_WITH_REASON`: encoder-era / pre-LLM / training-free-metric, off decoder-reasoning/serving-cost thesis). Each discovery summary already states park-leaning; screening preserves it. No material lane emptied: scaling-training retains 20, distillation-adaptation retains 8, routing retains 5.

**INSPECT5 correct (insufficient identity, not upgrade):** D032 DSA homepage-only (`source identity insufficient`), D077 ezyang AI-drafted UNEDITED (`verify derivations`), D093 Which-Pro (`isolate exact Pro variant + body`), D119 AIPerf product (`locate/confirm identity`), D150 ThinkPrune body unread (`confirm weight or substitute`). All mirror discovery `LOCATOR_ONLY/UNEDITED/pending` — proper.

**MAYBE20 correct (secondary/watch, quarantine + corroboration VTs):** D072 wiki / D074 DataCamp (not spec authority, vs official docs), D075/D076 provider pages (secondary, rebind/official pricing), D079/D082 llm-stats (quarantine), D080 NVIDIA (condition-bound), D084/D085 (harness/KDA), D086 MiniMax-M2.x / D087 gpt-oss (mechanism unverified watches per inclusion `materiality judgment`), D097/D099/D100/D117/D120 (version/harness/standalone), D146 kNN-LM / D147 RETRO (boundary precedents), D152/D156 surveys (secondary taxonomy, primary follow-ups). No secondary promoted to primary.

**Wrong locators + 67 labels (no misrepresentation):** Discovery preserves EFF-D005 `2206.06277` as FP8 origin and 8 neighbors with supplement-correct bodies absent from discovery (`2209.05433/2407.00079/2308.16369/2403.02310/2509.16941/2601.11868/2404.06654/2406.02069/2004.12993/2305.10429`; discovery holds `2411.01181/2308.16315` etc.). Screening KEEP reasons state topic relevance (e.g., D005 `FP8 origin`, D061 `Mooncake pooled KV`, D062 `SARATHI chunked prefill`) WITHOUT asserting locator correctness, and every such record carries `verification_targets [Evidence-stage full-body verification, …]` deferring body check to Evidence. Original `source_type` labels (`PRIMARY_PAPER/SECONDARY_TECHNICAL/PRIMARY_REPO…`, 67 projected/93 passthrough in historical compat, originals preserved here) are untouched by screening; screening reasons quarantine vendor/secondary claims rather than equating resource class with claim truth. Supplement remains citing authority (r2 completeness explicitly `supplement-bound` for D005/D139/D117/D061/D062/D112 etc.); discovery locators unamended. This is permissible explicit limitation, NOT misrepresentation — Evidence must fetch-or-hold correct bodies (residuals §3). Staged r2 `148 PARTIAL/12 VERIFIED + 11 bindings` are preserved input statuses, NOT true-verification judgments — not certified here per governance §4.2 (still pending Evidence independent review).

---

## 3. Per-record/issue findings (compact, actionable)

- **No empty/malformed rows:** 0 empty `reason`, 0 empty `verification_targets`, 6 correctly grouped duplicates, 159 null-group correctly distinct lenses.
- **D005 + 8 neighbors:** retain as above; action for Evidence in §4, no Screening rewrite (archived decisions reused exact `9290f406…`; rewriting would be new authorship).
- **D032/D077/D093/D119/D150:** INSPECT VTs already name the exact missing piece (dedicated URL / derivations / Pro variant+body / product identity / weight-vs-substitute) — Evidence must close or record `AUTHORITY_*` with defensible stop.
- **D072/D074/D075/D076/D079/D080/D082/D084/D085/D086/D087:** MAYBE quarantines already name rebind/comparison/KDA/mechanism gaps — Evidence must corroborate vs official/primary, not promote.
- **D140/D158–D161:** DROPs stand; do NOT reintroduce without new material mechanism + independent review.
- **D162:** X boundary stands; do NOT cite X result `b3a8a040…` for spec/benchmark truth at Evidence.
- **Capstone pins (D004/D008/D027/D030/D031/D123/D128/D163–D165 etc.):** VTs already require spec/precision/topology/version/scaffold/harness binding — Evidence must pin exact report/card/recipe revisions, not vendor headlines.

**No mandatory semantic input correction before `CANDIDATES_NORMALIZED`.** All limitations above are explicitly worded in `reason` + `verification_targets` and match discovery/raw `SUMMARY/LOCATOR_CAPTURED` + supplement scope. They travel as permissible explicit limitations. The only hard gate at Screening is exact 165 coverage + valid decision shape (met: `18a` 0/0, `18b` runner exit 0, schema-valid batches). Publisher-body proof (`AUTHORITY_CONSUMED` vs `CAPTURED_BUT_UNCONSUMED`, per-figure pins, supplement-body consumption) belongs to Evidence independent review (governance §4.2–4.3), NOT this gate. No generic all-publisher proof demanded; no extra Human question inside allowed fixed refs.

---

## 4. Verdict + allowed next (existing stage contract only)

**Verdict: `SP BOUNDED PROCEED` to `CANDIDATES_NORMALIZED` via root-selected typed checkpoint/advance (reports revalidated at dispatch).**

Permit current correct bytes ONLY: `screening-accepted.json 6ff524b0a…` (165, 135/20/5/5, `9b979629…`), `package.json b094bac…`, `results/batch-00*.json` + `input/batches/*` SHAs §1, proposed `9290f406…`, discovery `7074cef2…`/acceptance `2413dbe2…`, profile `aff05fd5…`, state `c680db5a…` (current `DISCOVERY_COLLECTED`). No checkpoint advance by this review; root dispatches after this decision; existing agent build/advance revalidates fresh State/contract/impl/artifact/report bindings (no rerun for chronology).

**Residual Evidence targets carried (not closed):** fetch-or-hold correct bodies for 9 wrong-identity lanes via supplement SHAs (list §2) keeping discovery locators unchanged; consume bodies for load-bearing capstone/report/card/recipe claims with per-figure/harness/scaffold pins; close INSPECT identities (DSA URL, ezyang derivations, Which-Pro variant+body, AIPerf product, ThinkPrune weight); corroborate MAYBE secondary/watch vs official/primary; retain X/R4 counterevidence as `LIMITATION`; use staged r2+O13–15 `f46dcf2f…` as Evidence input ONLY at Evidence seam with profile-bound validation (r1 superseded); apply governance §4.2 four-state + §4.3 iterative gap-fill + §4.4 materiality/compression review before Selection.

**Not allowed:** State advance by reviewer; Selection/Architecture/Draft/Candidate/Preview/Freeze/Release; Human Gate decisions; old approval rebinding; source edits; W34 advance on this review.

---

## 5. Machine artifact — none (truthful)

No new schema invented, no checkID fabricated. A truthful `AGENT_RESEARCH` row citing this actual review (executor `General independent supervisory reviewer`) is legitimate ONLY if the existing checkpoint flow requires an agent row; otherwise exact review path/hash in existing `evidence`/`summary` suffices with content review separate. Operator binds completed review path/hash at dispatch; root owns the record.

**Attribution:** General independent supervisory reviewer. Prior `CORE_STAGE_CONTRACT` and quality checkIDs are contract names only, not authorship.

(End of independent SP Screening review — 2026-11-01.)
