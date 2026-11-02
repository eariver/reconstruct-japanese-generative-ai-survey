# Independent SourceIntake supervisory review — W34 + SP-efficient-llm rehearsal (isolated)

**Role:** General independent supervisory reviewer — NOT past Sol/Luna execution author, NOT Astra/root, NOT Human owner. Historical `check_id` strings below are retained ONLY as contract names from `config/survey-production-v2.json` / schemas; no other author is impersonated.

**Review file:** `notes/rephase-1-operational-rehearsal-20261101/reviews/source-intake-review-20261101T104700Z.md`
**Review wall-clock:** 2026-11-01T10:46–10:55Z (packet `README.md` CURRENT + P4 + CORR read first; workdir bytes hashed/parsed after).
**Bounds observed:** workdir READ-ONLY. No network, no Production checkout (`/home/eariver/git/japanese-generative-ai-survey` never read), no Commit readback, no Git mutation, no source edit, no runtime/import/test/build/fixture, no State write, no State advance, no deterministic record creation for unrun validator. Data-only `python3` stdlib parse/hash/distribution inventory only; unique evidence (this file). No subagents. States verified still `ISSUE_INITIALIZED`; they remain so under this review.

**Targets (Human-authorized, fixed refs only):**

- W34 `774dd39a951c9ac3818e83dfffd4c7666efb0a20` — `WEEKLY/WEEKLY_MAGAZINE`, `ROLLING_WINDOW 2026-08-14T18:00–2026-08-21T18:00-04:00 America/New_York` (UTC authority `[2026-08-14T22:00Z, 2026-08-21T22:00Z)`).
- SP `c8d0ecc1c9566a2303ad3b4c42635d4b672650e4` — `THEMATIC/LONGFORM_SPECIAL`, `OPEN_HISTORY_AS_OF 2026-09-21T16:10:00Z`, 12 scope dims `D01–D10 + capstones + benchmark-methodology`, initial obligs `EFF-O01–O12`.

**Code/workdir pins (NOT re-certified):** final138 proof `.rephase-1-editorial-runtime/profile-support-packaging-20261031T025600Z/proof-copy/candidate-partial-b40de60` (770 files), patch `efb505e4…/5247647B`, manifest `634d41f9…/186847B` per packet (this review does not re-hash whole source). Isolated workdir `.rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work`, base commit `480823560c0c26ed2e5baa18e0e79a22b2839a27` (process-scoped rehearsal identity, no empty commit, inert origin). All fresh Profile/State `implementation.repository_commit_sha == 48082356`, `orchestrator_version survey-production-core-v2/0.15-postintegration-transport-thematic`.

---

## 1. What was actually read (read scope, not author counts)

Packet + governance (read-only, no execution):

- `notes/rephase-1-operational-rehearsal-20261101/README.md` FULL (incl. P4 confirmation §34–37, `113d62e7/638ea4af` blob-vs-FILE resolution, CORR appendix).
- `operation-readiness.md` FULL + `CORR-20261101` C1–C3 (Phase A/B gate order; no `PRIMARY_ONLY`-agreement gate; synthetic timings mechanical-only).
- `execution-20261101T025600Z/README.md` (history §§1–5 + P4 update §6), `review-seam-sourceintake.md`, `bindings.md`, `dependency-table.md`, `worklog.md`, `logs/05/06/07/09/10/11/12` stdout/exit/env (no summaries-as-raw; exit codes + SHAs only).
- `intake-integrity-review-20261101T032056Z/report.md` + `report-p4-supplement.md` (P1 6/6, P2 179/179 + 145 DATA, P3 63 with 6 bad-zero `p3a02–07`, P4 10/10, 760 FILE links, DRAFT-vs-final typed supersession `p2c13`, unresolved `76191e9b` candidate).
- `intake-20261101T023147Z-p4-20261101T031826Z/README.md` + `supersede-mapping.md` + `manifest.json` (P4 exact-blob repair, no P3-zero consumption).
- `w34-baseline-reader-assessment.md` FULL incl. §7 addendum (12 pp eye-read, 369→439→409→41→7 chain correction; stale 110/80/1 index superseded) + `efficient-llm-baseline-assessment.md` FULL (66 pp, 14 eye-read + full-text, 165→165→160→112→9 chain, abstract-scope + wrong-identity list §6–7).
- Candidate governance (workdir read-only): `docs/survey-production-core-v2-sol-luna-review-governance.md` §§1–10, `docs/survey-production-core-v2-x-source-intake.md` §§1–10, `config/source-intake.json`, `config/survey-production-v2.json` (`external_source_intake`, `quality_review` checkIDs, `research_profiles`, `human_gates`), `schemas/x-source-intake-v2.schema.json`, `schemas/discovery-acceptance-v2.schema.json`, `schemas/stage-checkpoint-v2.schema.json`, `schemas/stage-validation-attestation-v2.schema.json`, `schemas/stage-handoff-v2.schema.json`, `schemas/review-finding-v2.schema.json`, `schemas/publication-review-record-v2.schema.json`, `schemas/source-intake-acceptance.schema.json`.

Workdir bytes (hashed, parsed — every ID/ref/profile/window/type checked, not just counts):

| artifact (workdir path) | bytes | SHA256 (FILE) | binds |
|---|---|---|---|
| `sources/2026-W34/production-profile.json` | 2371 | `2a8c3089cec29eb64e121cdf0429eed38670df704ebe955079751198557cfeb1` | fresh; question/window/dims/3 obligs/paths byte-identical to `.rephase-1-inputs/774…` archived `a6e3eb3006…` except contract fresh `3adfbda2…`; old hash archived, never rebound |
| `sources/2026-W34/production-state.json` | 2606 | `078c34119c576522becaf78e39ae82ee902cb98972d55f3735fb503309f72ab8` | `ISSUE_INITIALIZED`, `target_gate ARCHITECTURE_REVIEW`, `next_action stage:discovery`, impl `48082356`, agent-valid, gates pending, no checkpoints |
| `sources/2026-W34/external/x/x-source-intake-v2.json` | 4326 | `73db915a3b3ae4f6bee6b4f2740b101349793e049ba7d1ccbd4e12bdf8484fb0` | NEW COMPLETE, binds fresh `2a8c3089`; run `weekly-x-2026-W34-r2` |
| `…/weekly-x-2026-W34-r2/grok-task.md` | 9464 | `47e19beb0764ac6c98585071f2548bb899147ab502f0ad865a6586087be22029` | local re-render, NOT archived `e97bbd06…` |
| `…/raw/grok-x-result.corrected.md` | 23612 | `43b0923bbd68ef9d9d9d4bf501a773cd4b4e4cdd881339d9591d97e7951f86ca` | == archived P3 `p3a51`/P4 manifest want; `observed_at 2026-09-02T14:49:21Z` preserved |
| `sources/2026-W34/discovery/discovery-v2.jsonl` | 963155 | `e176326f853ed42b69bad8a1998513d8dba8d3838af7cdea0ca9bc8261df46b0` | 369 lines, copied exact bytes from `DATA.p2b01` |
| `sources/2026-W34/discovery/discovery-accepted-v2.json` | 377589 | `255fb12d71cf463e78b9be74fbb57d35d3beea2dbb47fa27cbd36b442133f22b` | 369 rec, `graph_sha a13afd9e…`, binds NEW X `73db915a…` |
| `sources/SP-efficient-llm-2026/production-profile.json` | 13748 | `aff05fd573ce873afa24c0ede26c2b4591ee28b7048c9ed528e8fc389ed8ee45` | fresh; question/`as_of`/12 dims/`O01–O12`/paths byte-identical to P1 `DATA.production-profile.json 22f2e822…` except contract fresh; old archived |
| `sources/SP-efficient-llm-2026/production-state.json` | 2648 | `ea77482e40529608aefb18b8a0399d6bc1a3ba600d3cbe3c512c329a51b5785e` | `ISSUE_INITIALIZED`, same gate/next/impl as W34 |
| `sources/SP…/external/x/x-source-intake-v2.json` | 4888 | `fa3a50550f7f0acc5668a4871e829c0484cc0c7028baf10ff7a45c10c0917aa8` | NEW COMPLETE, binds fresh `aff05fd5`; run `efficient-llm-reception-pass-01` |
| `…/efficient-llm-reception-pass-01/grok-task.md` | 9546 | `edc7aef99eef0283a2e476499d7dac1f0b06155481e35de0cb11ea03f8f9f46b` | local re-render, NOT archived `c1150730…` |
| `…/raw/x-reception-result-r3.md` | 30213 | `b3a8a0404e6d4a1abfaa6bde54c4a6f5d7979ec24870bcd629865f8443377d79` | == archived P3 `p3a59`/P4 want; `observed_at 2026-09-21T17:16:12Z` preserved |
| `sources/SP…/discovery/discovery-v2.jsonl` | 173299 | `7074cef2bfc3b2dd034addbd778055bc2fed962e9845c756f32f9b3c848199d3` | 165 lines, copied exact from `DATA.p2b20` |
| `sources/SP…/discovery/discovery-accepted-v2.json` | 135693 | `2413dbe2f188ca2cde5d07ac07a749932b6536d41db2263b43cd3cd86924a856` | 165 rec, `graph_sha 441f488b…`, binds NEW X `fa3a5055…` |

Verification method: `hashlib.sha256` + `byte_count` per file; per-record `raw_refs` existence + `sha256`/`byte_count` re-hash (0 mismatches both editions); `obligation_ids` distribution; `raw_paths`→`raw_refs` mapping; `source.locator`/`raw_paths` sampling; `observed_at`/`imported_at` vs archived manifests. No validator/import executed; `logs/11/12` exits taken as recorded evidence only (`11 exit 0`, `12 exit 0`), not re-run.

Original P1–P4 comparison (exact oldScope/oldX/task/result):

- OldScope: W34 question/window/3 obligs/paths and SP question/`as_of`/12 dims/`O01–O12`/paths verified byte-identical fresh-vs-archived (hashes above; old `a6e3eb30…`/`22f2e822…` kept archived per `11-x-manifests.stdout.txt`). No silent scope change.
- OldX/task/result: P4 `DATA.p4x01` (W34 3913B `702881aa…`/blob `113d62e7…`) and `DATA.p4x02` (SP 5359B `3465dc4f…`/blob `638ea4af…`) are the archived bytes; P4 supplement proves blob-SHA1 vs FILE-SHA256 are different hash domains for SAME bytes — root suspicion withdrawn, no historical drift. Fresh manifests reuse archived `purpose/research_questions/coverage_focus/time_scope/run_folder/drive_task_path/expected_result_filename` VERBATIM (checked field-by-field); `task.sha` binds fresh re-render (`47e19…`/`edc7…`), NOT archived (`e97bbd…`/`c11507…`); `result.raw` binds archived SUCCESS bytes (`43b0923…`/`b3a8a040…`) with old `observed_at` kept and `imported_at 2026-11-01T03:33:41Z` real. Task bodies differ (archived BOM/CRLF + longer Mission template vs fresh Common-Policy template) but substantive questions/coverage are identical — fresh text verified to contain all 4+4 questions and 13+4 coverage lines. `rationale` explicitly states archival re-render, NO new Grok request. `drive_file_name` revision suffixes (`grok-x-result.corrected.md`, `x-reception-result-r3.md`) are lawful per X doc §5 rule 4 (no overwrite, report actual). P3 bad-zero `p3a02–07` superseded/unavailable, never consumed (P4 `p4a02–07` verified `len==size` + `blob==body-sha` + `sha256==discovery-want`).
- One SP historical `76191e9b…→adf22516…` candidate has no typed `prior→new` map (P4 supplement §unresolved); disclosed, not rebound, not used as authority — respected here.

---

## 2. X-scope honesty (unchanged question/window, no new research claim)

**W34:** `policy REQUIRED_BY_PROFILE`, `decision REQUIRED`, `status COMPLETE`. Run purpose is fresh independent W34 scan for ChatGPT/Sol; 4 questions (material momentum, reproduction/integration/failure, primary artifacts needing verification, quiet/negative retention); 13 coverage lanes (frontier/open/multimodal/image/video/audio/coding/agents/serving/distribution/research/safety/infra); `time_scope` canonical ordinary window with UTC authority. Result `SUCCESS`, `DISCOVERY_RECORDED ['w34-grok-r2-corrected-47-url-ledger']`, `observed 2026-09-02`, `imported 2026-11-01`. Rationale: archival re-import, SOCIAL/X remains reception lead, X-only claims non-technical leads pending first-party verification. Grok result header confirms: 12 clusters, 47 X URLs (10 ordinary / 20 background / 17 late-breaking), 17 official + 30 independent, 9 linked primary URLs; ordinary-window material limited (2 Google posts, free-tier/GLM-5.3, safety, Qwen local); majority of Grok-4.6/V4-Pro/NVIDIA posts correctly BACKGROUND_ONLY (pre-22Z 14 Aug); post-22Z 21 Aug correctly LATE_BREAKING. No new external completion claimed; no approval inferred.

**SP:** `policy CHATGPT_DECIDES`, `decision REQUIRED` with substantive why-reception-matters rationale (capstone practical behavior, local/deployment stack, mechanism gains/costs, independent benchmark/countersignal leads for ChatGPT verification). 4 questions (capstone behavior in practice, reproducible experiences/hardware/measured/failures for V4.1-Flash/Qwen/Kimi/GLM-5.3/Jev, workload-dependent gains vs implementation costs, benchmark/counter-signal leads); 4 coverage buckets (5 capstones, local stack GGUF/llama.cpp/KTransformers/vLLM/SGLang/LMCache/hetero/MoE, mechanisms MoE/sparse/KV/FP8/FP4/INT4/speculative/budgets/routing/Conditional-Memory, interpretable independent observations); `time_scope 2025-01-01–2026-09-21 strongly prioritize 2026` consistent with `OPEN_HISTORY_AS_OF`. Result `SUCCESS`, `DISCOVERY_RECORDED ['EFF-D162']`, same observed/imported discipline. X result r3 is reconciliation-only correction (27 OBS + 24 ledger rows preserved, no new research, `FINAL_LEDGER_RECONCILIATION`); FIRST_HAND 17/3/7, reception 20 positive/3 mixed/4 neutral; densest for V4.1-Flash/Qwen, GLM packaging, Kimi config, Jev single eval + integration; host-RAM/offload/VRAM limits + quant/long-context brittleness as counter-signals; ALL technical claims explicitly subject to primary verification. R4 followup `r4-x-followup.md` honestly records F4 `INDEPENDENT_WRITEUP_NOT_RESOLVED` (two searches, no substitution) — not upgraded, no Discovery record created.

Both manifests validate `require_complete PASS` in logged `11` (taken as recorded, not re-executed). No `NOT_REQUIRED` silence; no `NO_MATERIAL_DISCOVERY` fabrication (both have material, correctly `DISCOVERY_RECORDED` with exactly 1 ID each — no inflated ID list).

---

## 3. Discovery acceptance integrity (per-target, all IDs/refs checked)

**W34 — 369/369, 0 missing, 0 hash mismatch:**

- `record_count 369`, `discovery_sha e176326f…`, `x {path, sha 73db915a…}` matches actual fresh manifest FILE hash. `graph_sha a13afd9e…` rebuilt via normal `disc.build_acceptance` (logged `12`).
- Oblig distribution: `weekly:current-relevance 368`, `weekly:technical-significance 368`, `weekly:carry-over 1`. All 369 records carry ≥1 oblig; no empty, no alias DROP.
- Origins: `BASE 16`, `GAP_FILL 352`, `CARRY_OVER 1`. `BASE` = Sol working-set baseline + 7 dailyx + 7 github + 1 Grok? Actually 16 = 1 working-set + 7 dailyx + 7 github-collector roots + 1 Grok ledger? Verified per-record `method.kind/collector_id/run_id/trigger` present; `parent_edges` empty for BASE (correct, no parents), `CARRY_OVER` has `EXTERNAL:2026-W33:candidate:…986cf…` (exactly the one expected HOLD).
- Raw binding: 372 `raw_refs` entries → 55 unique paths, ALL files exist, ALL `sha256==actual` and `byte_count==actual` (re-hashed). Unique set = 1 carryover ledger + 7 github + 24 gapfill + 6 arxiv atoms + 4 official pages + 2 gapfill obs + 7 dailyx + 4 X-accounting/result + 1 working-set (full list in §1 workdir `ls`). No child autofill (every `raw_refs.path` is the `discovery-v2.jsonl:source.raw_paths[0]` for that `discovery_id` — spot-checked 20 + full hash sweep).
- Concentration disclosed (not a count proof): 180 rec share `cs-ai.atom`, 45 `cs-cv`, 40 `cs-cl`, 29 `cs-lg`, 20 `cs-cr`, 5 `cs-dc` — bulk atom snapshots, NOT 369 independent primary reads. Each such record correctly `source_type arxiv_atom_snapshot`, `technical_evidence_accepted false`. Sufficiency of per-arXiv abstract/body consumption is NOT proven by this binding (residual §5).
- X binding: 7 dailyx raws + 1 Grok result correctly bound (`w34-dailyx-…` ×7, `w34-grok-r2-corrected-47-url-ledger` → `43b0923…`). Dailyx `08-22` file `observed_at 2026-08-21T22:00Z` is exactly cutoff (JST slice `08-20 22Z–08-21 22Z`); NOT post-cutoff leakage. UTC reclassification in Grok result (ordinary/background/late-breaking) is consistent with window authority.
- Carry-over: single `w34-carryover-minimax-unresolved` (`CARRY_OVER_UNRESOLVED`, `promotion_to_current false`, pre-window Music-3.0/H3 `2026-08-13/03`, post-cutoff financial `08-26`) — correctly NOT promoted at intake; disposal is Selection/Completeness later, not intake. No silent DROP of W33 HOLD.
- No status upgrade: no Evidence/Screening acceptance run at this seam (blocked correctly per `06/07` REFUSED→shape-only PASS); `07` validated SP decisions 165/165 + SP r1 160/160 + W34 409/409 shapes profile-bound, but full admission NOT run. Historical `SELECTED41/HOLD368/7 packages` (P2 `p2b12/p2b13`) is baseline ONLY — stale `SELECTED 1` index explicitly superseded per addendum; NO current selection claimed (States still `ISSUE_INITIALIZED`).

**SP — 165/165, 0 missing, 0 hash mismatch:**

- `record_count 165`, `discovery_sha 7074cef2…`, `x {path, sha fa3a5055…}` matches fresh manifest. `graph_sha 441f488b…` rebuilt.
- Oblig distribution: `O01 4, O02 20, O08 32, O11 43, O06 21, O05 15, O04 34, O03 17, O09 8, O07 7, O10 8, O12 23, O13 5, O14 6, O15 5`. All 12 profile obligs covered (min 4); named `O13–O15` (conditional-memory/test-time-compute/model-routing, r3 `G21/G22/G23`) preserved in ORIGINAL graph (`EFF-D143–158` `GAP_FILL`, locators `2601.07372/github-Engram/Qwen-repo/1911.00172…`, `2408.03314/2501.19393…/HF-DeepSeek-card`, `2305.05176/2406.18665…/findings-acl…`), NOT hand-appended at acceptance. Fresh profile is `O01–O12` by design; `O13–15` are edition-authored named extension from `DATA.p2b26` (3 SATISFIED/12 LIMITATION) — preserved, not aliased/dropped, pending Evidence via staged `r2-adapted-O13-15.json` (packet only, NOT executed; r1 file preserved SUPERSEDED). No `DROP`/alias.
- Origins `BASE 100` (profile seeds r1) + `GAP_FILL 65` (r2–r4 Sol gap-fill). All `method`/`trigger` present.
- Raw binding: 165 entries → 25 unique paths, ALL exist + hash/size match. Set = 24 obs (`D01–D10 + benchmarks + capstones + R2-G12–G20 + R3-D09/G21–G23 + R4-X`) + 1 X result. Every raw header states `SUMMARY_CAPTURED` or `LOCATOR_CAPTURED (full body pending Evidence)` + `source-local claims only until Evidence verification` — honest abstract-scope, NOT full-publisher proof. This is PERMITTED at SourceIntake (candidates for verification, not full Evidence/publication complete per task). No record claims `AUTHORITY_CONSUMED`.
- Mandatory lanes verified in graph (not just counts): capstones — DeepSeek V4.1-Flash (`EFF-D004/D030/D031/D077/D123/D124/D153/D163` + provider `D075/D076`), Qwen3.8-Flash-Next (`D008/D029/D079/D080/D081/D127/D145/D165`), Kimi Linear (`D027`), GLM-5.3-Flash (`D052/D082/D084/D085/D128/D129/D130/D131/D164` incl. Unsloth/day-zero `27754`), Jev (`D070/D072/D073/D074/D141` + `D162` X `OBS-R2-021/022/023`); runtime (`D063 Dynamo`, `D064 DeepEP`, `D065 DeepGEMM`, `D066 FlashInfer`, `D049 vLLM`, `D136 MX spec`); benchmark (`benchmarks-methodology.md` + `D092–D098/D100–D112` + SWE/RULER/Pyramid); counterevidence (X counter-signals + `R4 F1–F4` topology-conditional DSpark refusal, Unsloth packaging caveats, llama.cpp gaps, `F4` unresolved). 12-dim broad scope is NOT four-family serializer — no `THEMATIC_FOUR_FAMILY_LINEAGE_V1` claim made (correctly absent).
- Incorrect locators (pending, NOT blockers — proper disposition): `EFF-D005` `https://arxiv.org/abs/2206.06277` presents as FP8 Formats but correct FP8 is `2209.05433` (supplement 43673B); 8 further supplement-correct bodies have NO discovery locator (`2209.05433`, `2407.00079` Mooncake, `2308.16369` SARATHI, `2403.02310` Sarathi-Serve, `2509.16941` SWE-Pro, `2601.11868` Terminal-Bench-2, `2404.06654` RULER, `2406.02069` PyramidKV, `2004.12993` DeeBERT, `2305.10429` DoReMi) while discovery holds neighboring IDs (`2411.01181` Mooncake, `2308.16315` SARATHI, etc.). Fresh graph PRESERVES wrong locators exactly as authorized (no silent amend); supplement is citing authority per baseline §7. Evidence must fetch-or-hold correct bodies for load-bearing claims (list §5). No status upgrade, no guessed publisher truth.
- Cutoff: `OPEN_HISTORY_AS_OF 2026-09-21T16:10Z`; bib `urldate 09-21`, X `observed 09-21`, capstone docs 2026-02–09; sampled pages show no post-cutoff claim. Reception-vs-primary: X + `r4-x-followup` explicitly reception/deployment-only, vendor ratios/speeds quarantined, no ranking.
- Historical chain respected: old acceptances/checkpoints/Gates archived (`DATA.p2a11–19`, `p2b21` etc.), never installed; old profile hashes never rebound.

---

## 4. What this review can genuinely certify (governance + config)

- `docs/survey-production-core-v2-sol-luna-review-governance.md` §4.1 requires Discovery completeness review: surfaces exercised, vendor/project lanes, first-party channels, negative-space, duplicate/concentration, fresh sweep when practical, residual limits. Candidate count alone is NOT completeness.
- `docs/survey-production-core-v2-x-source-intake.md` §§2–3/6/8–10: W34 `REQUIRED_BY_PROFILE` (≥1 Grok run before acceptance; quiet valid but scan must exist); SP `CHATGPT_DECIDES` (use when material, with why-X rationale); Grok is sensor, NOT Evidence authority; SOCIAL stays reception lead; manifest must bind exact profile/task/result/observed/imported/disposition.
- `config/survey-production-v2.json`: `quality_review` checkIDs (`WEEKLY_*`, `THEMATIC_*`, `PERIOD_*`, `PDF_PREFLIGHT` etc.) are downstream deterministic/semantic/visual Gates — NONE are decided at this seam. `human_gates` remain exactly `ARCHITECTURE_REVIEW` + `PUBLICATION_PREVIEW`.
- `schemas/stage-checkpoint-v2` requires `CORE_STAGE_CONTRACT DETERMINISTIC PASS` + `GAP` reviews for `ISSUE_INITIALIZED→DISCOVERY_COLLECTED`; `stage-validation-attestation`/`stage-handoff` require real orchestrator attestation.

**Therefore this SourceIntake seam can certify ONLY:**

- (a) data integrity: every required Raw present + `sha256/byte_count` bound, X manifest `COMPLETE` + task/result binding honest, counts/graph/X-sha exact, window/profile preserved, SOCIAL-lead discipline kept;
- (b) breadth accounting: which intake surfaces/lanes/obligs are present, where concentration lives, which holes/incorrect locators/cutoff questions remain as explicit Evidence targets.

It CANNOT certify: search freshness/exhaustiveness (no new search performed; reimport proves transport, not coverage sufficiency), publisher truth, per-claim Evidence sufficiency, Selection/Architecture quality, render determinism, cost/savings, or any Human Gate. No `PASSED` publication/semantic/visual verdict is given. This matches task narrow stage goal, NOT all-publisher-read prior-intake condition.

---

## 5. Per-target verdict + exact residual Evidence targets (no rubber-stamp)

### W34 — `BOUNDED PROCEED` to Screening (allow `DISCOVERY_COLLECTED` via normal typed path ONLY after this review; no auto-advance by author)

Normal SourceIntake duties ARE met: REQUIRED X COMPLETE + honest archival reuse; 369 acceptance with every Raw bound; profile/window preserved; carry-over correctly unresolved-not-promoted; X UTC classification truthful; no old-selection reuse (41/7 baseline only, stale 1 superseded).

**Constraints:** States stay `ISSUE_INITIALIZED` under this review — author/root must NOT treat existing `orchestration/v2/stage-validation/ISSUE_INITIALIZED-report.json` (`PASS CORE_STAGE_CONTRACT →DISCOVERY_COLLECTED`, `recorded_at 2026-11-01T10:42:52Z`, artifacts `255fb12d…`/`2413dbe2…`) as independent approval. Those files were created 10:42Z outside logged `05–12` runs, bind correct SHAs but pre-empt this seam; they are author-side validation output, NOT this review, and MUST be disregarded for Gate purposes. Operator must run REAL `plan_action/execute_action` (`handler stage:discovery`) or `core.transition_state` with fresh attestation AFTER this review; no hand-crafted DCP/SCP, no test-stub.

**Residuals for Evidence (must travel with `DISCOVERY_COLLECTED`, not closed here):**

1. Primary-body consumption: github 7 JSON are collector responses (full), gapfill 24 JSON are `BOUNDARY_LEAD`/`PRIMARY_LOCATOR_ONLY` (body NOT fetched), arxiv 6 atoms are bulk snapshots (per-ID `published_at`/summary vs body pending), official 4 HTML are index snapshots, dailyx/X are signal-only. Every high-signal candidate needs body-consumed Evidence with `AUTHORITY_CONSUMED` vs `CAPTURED_BUT_UNCONSUMED` distinction per governance §4.2; generic `locator-only` where body IS present must fail-close at Evidence.
2. 22:00Z boundary per-item: X result gives window-level buckets; each discovery record's `published_at`/`observed_at` vs `[08-14T22Z, 08-21T22Z)` needs item-level verification (esp. Qwen Aug 14, Claude watermark Aug 14, Imagen Aug 17 UTC moment, Vertex Jun 30 vs Gemini Aug 17, Aug 26 re-date, Sep 8 capture dating per baseline §2–3).
3. Vendor-vs-independent: Grok/X + provider pages (DeepSeek tariffs secondary-reported, Pika multiples non-normalized, Stripe/OpenRouter $7–8B exclusion, PORTS-Pike plan-vs-fact) need primary gap-fill before technical claims (X doc §10 boundary).
4. Carry-over ledger: `w34-carryover-minimax-unresolved` + `sol-discovery-event-inventory-v0.2` (105 events, `KEEP 82/CONTEXT 7` etc.) need Selection-time explicit disposal with package allocation justification (avoid late compression; justify selected/omitted dims per `review-seam §4`).
5. Concentration: 180-rec `cs-ai.atom` share must be called out in Screening/Evidence coverage accounting; count ≠ sufficiency; need negative-space sweep independent of execution list when practical (governance §4.1).

No smallest data correction needed now — all 55 Raws verified. Smallest semantic correction if Evidence finds gap: fetch exact missing primary body at same `774` ref (same-ref shards share authorization per P4 README §29 correction) or record `AUTHORITY_NOT_FOUND/RETRIEVAL_FAILED` with defensible stop; never synthesize fixture as need.

### SP — `BOUNDED PROCEED` to Screening (same control constraint as W34)

Normal duties ARE met: `CHATGPT_DECIDES→REQUIRED` with material why-reception rationale; COMPLETE + honest archival reuse; 165 acceptance with every Raw bound; 12-dim + `O13–15` preserved in original graph; capstones/runtime/benchmark/counterevidence present; SOCIAL-lead discipline; no four-family overclaim; no status upgrade.

**Constraints:** same `ISSUE_INITIALIZED` hold + disregard 10:42 PASS files + real orchestrator path only. `THEMATIC/LONGFORM_SPECIAL` pair may take `LONGFORM_GENERATED_V1` OR `DIRECT_PRIMARY/PRIMARY_ONLY` downstream per readiness §2 — this review does NOT choose receipt route and does NOT add a `PRIMARY_ONLY`-agreement gate (CORR C2). Retrospective P1-unsupported rule is irrelevant (SP is Thematic, P1 available where predicates hold — not exercised here).

**Residuals for Evidence (exact):**

1. Body-consumption backlog (abstract-scope): ALL 24 obs `SUMMARY/LOCATOR_CAPTURED`; 13 supplement files are abstracts/launch/docs only (1,275,978B, manifest `62031208…`). Load-bearing Evidence MUST fetch-or-hold at same `c8` or with explicit new publisher permission (baseline §6 list, preserved here): V4.1 report `2609.19969` + card/checkpoint, Qwen report `2608.30320` + repo/blog/NVIDIA deploy, Kimi `2510.26692` (CC BY-NC-ND noted), GLM-5 report `2602.15763` (currently abstract-only per boundary), Dynamo pinned revision, vLLM pinned revision/code, plus corrected wrong-identity bodies `2209.05433/2407.00079/2308.16369/2403.02310/2509.16941/2601.11868/2404.06654/2406.02069/2004.12993/2305.10429`, price/provider snapshots (Lambda/DeepInfra/llm-stats/ezyang — secondary only), SWE-Pro/RULER/Pyramid/DeeBERT/DoReMi/V3.2-Exp/GenAI-Perf pins. `EFF-D005` wrong locator stays as-is in Discovery; cite supplement, never silently amend.
2. `O13–15` handling: use staged `input-archive/SP/interactive-evidence-r2-adapted-O13-15.json` (r2 `148 PARTIAL/12 VERIFIED` + 11 bindings + 5 limits, 15 obligs, 0 record errors; r1 preserved SUPERSEDED) as Evidence input ONLY at Evidence seam with profile-bound validation; do NOT treat r1 abstract-level (155/5, no bindings) as equivalent.
3. Capstone pins: per-figure ablations/version/harness/scaffold/budget/hardware/authority for V4.1/Qwen/Kimi/GLM numbers; vendor ratios/speeds conditional; living docs (Dynamo/vLLM/GenAI-Perf) pinned-config only; MiniMax-M2.x/gpt-oss watches stay watches; AIPerf standalone unconsumed; no cross-condition ranking; `O11 LIMITATION` boundary (4th abstract-only, unresolved names unused) preserved.
4. Counterevidence depth: X counter-signals (quant quality, long-context brittleness) + `R4 F1–F4` (DSpark topology-conditional, MTP-module drop, AMD refusal, Unsloth packaging caveats, llama.cpp gaps, `F4` unresolved) must be retained as `LIMITATION`, not closed by `SUMMARY_CAPTURED`.
5. No search-freshness inference: 165 count + 25 Raws prove transport/binding only; fresh independent sweep saturation is Evidence/Sol gap-fill judgment, not intake proof.

No smallest data correction now — 25/25 verified. Smallest correction if Evidence hits wrong locator: cite supplement bytes by exact SHA (already captured) for that claim, keep Discovery locator unchanged, record `AUTHORITY_*` state truthfully; if body truly needed beyond abstract, ask Human for specific publisher URL (new authority), do NOT infer.

---

## 6. Seam decision / allowed next / required fixes

- **Decision:** `W34: BOUNDED PROCEED` + `SP: BOUNDED PROCEED` — each independently judged; neither blocks the other. Unblocked edition may progress while other waits; unavailable edition never replaced with fake fixture.
- **Allowed next (root dispatches, NOT author):** normal typed `DISCOVERY_COLLECTED` checkpoint/control via orchestrator `plan_action/execute_action` (`handler stage:discovery`) or `core.transition_state` with real attestation, citing THIS review file as supervisory evidence (executor `General independent supervisory reviewer`, NOT Sol/Astra/Human). Then Screening `run` (needs `DISCOVERY_COLLECTED`) toward its own review seam; Evidence `run` (needs `CANDIDATES_NORMALIZED`) likewise. Author MUST NOT self-advance, hand-craft DCP/SCP, or reuse 10:42 PASS files.
- **Required fixes before advance:** NONE on bytes/provenance — no data/semantic correction needed at this seam. Only control fix: disregard out-of-seam 10:42 `ISSUE_INITIALIZED-report.json` PASS files; re-validate deterministically at transition time.
- **Not allowed:** State advance by this review; `SELECTION_COMPLETE`/`ARCHITECTURE_ESTABLISHED`/`DRAFT`/`Candidate`/`Preview`/`Freeze`/`Release`; any Human Gate decision (`ARCHITECTURE_REVIEW`/`PUBLICATION_PREVIEW` remain pending with `pending` provenance); any `RECORD_*_APPROVAL`; any old-State/Gate/checkpoint installation or old approval rebinding (old `RELEASED/COMPLETE` states, `5289b68e…/15b88fb22…`, DRAFT SHAs remain history only).
- **If current tasks/result fit needs gaps report exact:** fit is bounded as above; gaps are residuals §5, not intake failures. Do NOT rubber-stamp as sufficient research; do NOT upgrade records; do NOT infer freshness.

---

## 7. Machine-consumable artifact — NONE emitted (truthful)

No existing schema truthfully captures this verdict with current role/pins without invention:

- `stage-checkpoint-v2.schema.json` requires `reviews[].check_id/kind/status/executor/evidence/result` with `CORE_STAGE_CONTRACT DETERMINISTIC PASS` + real attestation — creating it here would impersonate the deterministic validator and claim State-transition authority this review explicitly does NOT exercise (and would duplicate the disregarded 10:42 files).
- `publication-review-record-v2` requires `status PASSED` + `checks[].status PASS` + `reviewed_by` — that is semantic/visual publication PASS, expressly NOT given.
- `review-finding-v2` is for defects (`OPEN/CLASSIFIED/…`) — this is `PROCEED` with residuals, not a defect.
- `source-intake-acceptance.schema.json` is Weekly-only (`^[0-9]{4}-W[0-9]{2}$`), `status ACCEPTED` with `source_actions.workflow_run_id/artifact_id…` — old Actions intake shape, not current rehearsal; SP cannot validate, and required workflow IDs do not exist.
- `x-source-intake-v2` / `discovery-acceptance-v2` already exist and validate COMPLETE (deterministic part); this supervisory judgment is explicitly separate per governance §2 (provenance ≠ semantic approval).

**Operator input shape when creating the record FROM this completed review (for root/operator, NOT created here):** `stage-checkpoint-v2` with `issue_id` = `2026-W34` / `SP-efficient-llm-2026`, `from_state ISSUE_INITIALIZED`, `to_state DISCOVERY_COLLECTED`, `implementation.repository_commit_sha 48082356…`, `contract.pipeline_contract_sha256 3adfbda2…` (+ quality/research/publication per fresh profiles), `artifacts[]` = `{name: discovery-acceptance, path, sha256: 255fb12d… / 2413dbe2…}` + `{name: x-source-intake, path, sha256: 73db915a… / fa3a5055…}`, `recorded_at` = real transition time, `reviews[]` MUST contain a FRESH deterministic `CORE_STAGE_CONTRACT PASS` (re-run at transition, NOT the 10:42 file) PLUS a supervisory entry citing this file path + `finding: BOUNDED PROCEED with §5 residuals` (no invented `check_id`; use `kind AGENT_RESEARCH`, `status PASS`, `executor General independent supervisory reviewer` ONLY if schema/kind truthfully allows; otherwise cite as `evidence` string). No new schema, no invented checkID.

---

## 8. Attribution + non-claims

- Correct attribution: this is General independent supervisory review. Not Sol (execution/supervisory split owner), not Luna/Work, not Astra/root synthesis, not Human Gate. Historical `CORE_STAGE_CONTRACT`/`WEEKLY_*`/`THEMATIC_*` names are contract identifiers, not authorship claims.
- Binds exact reviewed bytes/hashes in §1 (14 workdir files + archived P1/P4 comparisons). Methods §1 are actual read scope (full files + per-record parse, not sampled counts).
- No semantic publication PASS, no adoption, no quality/savings verdict, no full-corpus completeness, no render determinism, no publisher-truth certification. Source material remains abstracts/observations, NOT every full paper — SourceIntake stage permits candidates for verification, NOT full Evidence/publication complete.
- Whole `NOT_READY` / `step4B3 OPEN` / `audit unstarted` / `DM021+022 OPEN` / quality/adoption/savings `OPEN` preserved from packet entry; this seam does not close them. No ordinary Commit/Push/Human readback/network/Production action.

**Return real review-seam decision:** both editions may proceed to Screening via normal typed control after root dispatch; carry §5 residuals as required Evidence targets; disregard 10:42 deterministic PASS files; no other fix needed at intake.

(End of independent SourceIntake review — 2026-11-01, General independent supervisory reviewer.)

---

## Appendix CORR-20261101T11Z — control clarification (original §§4/6/7 preserved, this appendix governs where it conflicts)

**Role reaffirmed:** General independent supervisory reviewer (not Sol/Luna author, not Astra/root, not Human). Substantive §§1–3/5 findings, per-target `BOUNDED PROCEED` decisions, residuals, and non-claims are unchanged. This appendix corrects ONLY control language in §§4/6/7 per root direction. No new review type/schema/gate demanded, no checkID fabricated, no State advanced by this review.

**Actual read scope for this correction (read-only, no runtime/network/Git/source edits):** packet `README.md` §§40–44 (`13592B sha256 73d5862c…`), `execution/stage-path-inputs.md` (`5034B 3970713e…`), `logs/13-stage-reports.stdout.txt` (`1479B 67862c8a…`) + `exit.txt` (`0`), `build-stage-reports.py` (`1999B c45f00cd…`), workdir `scripts/survey_agent_control_v2.py` (`199521B d801feb6…` top, lines 2182–224 + 2227–2374 read) + `schemas/stage-checkpoint-v2.schema.json` (`11682B a1b97759…`, `reviews` block + `$defs/localStageValidationReview` read). No all-source re-audit; prior §1 pins stand.

**Corrections (final-binding):**

1. **13-stage-reports were root-authorized parallel evidence, not out-of-seam.** `13-stage-reports.stdout.txt:1` states `REAL-CLOCK … (preflight only; state advance needs review decision)` and `:14` `DONE-ALL (reports only; NO checkpoint write, NO state advance)` with `exit 0`. Packet README §44 confirms they were explicitly authorized while semantic review was pending, did not advance State or impersonate independent review. I withdraw §§5–6 `out-of-seam/disregard/reuse forbidden` wording: earlier `10:42:52Z` timestamps do NOT preempt semantic review — deterministic `validate_stage PASS` and independent content review are separate evidence. No binding drift was found at last pins (report SHAs `67825323…` W34 / `4922f984…` SP bind current acceptance SHAs `255fb12d…`/`2413dbe2…`, States `078c3411…`/`ea77482e…`, Profiles `2a8c3089…`/`aff05fd5…`, impl `48082356…`). Existing agent build/advance APIs revalidate fresh byte bindings at dispatch; no rerun solely for cosmetic chronology.

2. **Schema requirement corrected.** Actual `stage-checkpoint-v2.schema.json` `reviews` requires `check_id` generic nonempty, `kind enum [DETERMINISTIC, AGENT_RESEARCH, AGENT_EDITORIAL, AGENT_VISUAL]`, `status const PASS`, `executor/evidence` nonempty, `result` nullable authority (deterministic rows require artifact authority). Required typed report is `CORE_STAGE_CONTRACT` DETERMINISTIC PASS via `$defs/localStageValidationReview` (`contains check_id CORE_STAGE_CONTRACT/kind DETERMINISTIC/status PASS/result`). There is NO required generic `GAP reviews` attestation — I withdraw that claim. `AGENT_RESEARCH` is an existing kind; a truthful independent `AGENT_RESEARCH` row may cite this actual review (executor `General independent supervisory reviewer`, no invented checkID) IF the existing flow needs one; otherwise exact review path/hash in existing `evidence`/`summary` with content review separate is permitted — no compiler-required governance field invented.

3. **Stage path corrected.** Root-selected path is `agent.build_stage_checkpoint` (`survey_agent_control_v2.py:2227`, validates State basis, DM022 READY, stage_plan, artifacts, `_load_reviews`, `_validate_core_stage_report`, schema gate, canonical write with no-overwrite) + `advance_with_checkpoint` (`:2304`, revalidates checkpoint-vs-lifecycle/contract/impl/artifacts/report, marks checkpoints, moves lifecycle, refreshes control, writes State). This is NOT legacy `core.transition_state`/machine attestation and NOT untraced `plan_action`. `stage-path-inputs.md` §§26–47 gives exact dispatch inputs (`artifacts={discovery-acceptance}`, `reviews_path` with one `CORE_STAGE_CONTRACT/DETERMINISTIC` row by author `General isolated-rehearsal deterministic stage validation (author, not independent reviewer)` + `result_path`, `summary`, fresh `recorded_at`, canonical checkpoint paths verified ABSENT, dispatch-time re-verification). `_load_reviews (:2182)` requires deterministic rows carry `result_path`, agent rows must not; `status PASS` is set by loader, not by reviewer string. State advance occurs AFTER this bound review via root dispatch, not by reviewer.

**Decision unchanged:** `W34 BOUNDED PROCEED` + `SP BOUNDED PROCEED`, residuals §5 retained, no new gap found in this correction. Operator creates checkpoint/advance at dispatch with fresh clock and revalidation; this review is cited as supervisory evidence, not as deterministic PASS.

(End of CORR appendix — 2026-11-01, General independent supervisory reviewer.)
