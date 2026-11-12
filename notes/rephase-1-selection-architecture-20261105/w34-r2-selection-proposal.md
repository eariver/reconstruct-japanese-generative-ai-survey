# W34 Selection proposal r2 (author, preserves v1)

**Role:** W34 research/editorial proposal AUTHOR (not independent reviewer). **Date:** 2026-11-05 r2. **Preserves:** `w34-selection-proposal.md` (v1), `w34-per-did-disposition-machine.json` (v1), `w34-human-dossier-draft-ja.md` (v1) unchanged as history. This r2 addresses independent review `reviews/w34-selection-proposal-independent-review-20261105.md` + machine FULL (CHANGES_REQUIRED F1–F5) and Astra working-resolution §2. No active writes, no API JSON, no Draft/PDF/Gate, no independent approval.

**Instance only:** `.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work` e84. State `EVIDENCE_REVIEWED` `d7acd29b…`, CP `CANDIDATES_NORMALIZED` `0979f9f7…` binding 4 refs (Evidence `edf21e4d…`409, Views `3777133c…`409, Ledger `f089cc4e…`439, Completeness `e8c432dd…`3 LIMITED). Window UTC `[2026-08-14T22:00Z,2026-08-21T22:00Z)`. Full r2 machine `w34-r2-per-did-disposition-machine.json` (439 rows: 409 Matrix +30 nonMatrix separate), triage `w34-r2-arxiv-triage.json` (319), body ledger `w34-r2-body-read-ledger.md` (26 bodies actually read) + raw `w34-r2-body-read-raw.json`, counts `w34-r2-counts.json`, dossier `w34-r2-human-dossier-draft-ja.md`. Read scope DATA-only, no new network, no project imports/runtime/tests, no reconstruct Git, no subagents.

## F1 — Placement accounting fixed (exact mismatch corrected)

- `gap-aws-agentcore-memory-json`: machine single `SECTION_CORE / P2-agent-platform-GA` (valid). Prose v1 listed it in P1 SECTION and P2 merged box — deleted from P1 prose. Corrected: P1 = FEATURE 4 + SECTION 3 (c018 + kimi-k3 + wan-prime) + SUPPORTING 4 =11; P2 = FEATURE 4 + SECTION 4 (c019+c031+c047+memory) + SUPPORTING 3 (c087+c104+c105) =11. Machine uniques verify 12+12+17=41 distinct DIDs, no double placement. Single destination + single usage per DID enforced; SELECTED SUPPORTING may sit in ≥1 package in validator, but this proposal keeps one package each for audit clarity.
- `c102` Antigravity: machine single `SUPPORTING_EVIDENCE / P3` (honest ceiling — Aug21 addition UNRESOLVED). Deleted v1 prose split “Aug20 SECTION + Aug21 SUPPORTING”. One DID carries one role/package; no split-role. Upstream split into two DIDs not selected (requires Evidence revision, not done here).
- `c067 grok-build` duplicate no-loss: DUPLICATE misc updates, no separate bytes. Survives as (a) c025 Build 1.0.x cadence v1.0.7 Aug19 retained as HOLD CONTEXT background (cadence vs broad-availability gap: configured locator resolves to SpaceXAI Console, not Build GA), and (b) c066 Plus/Pro+/Teams expansion scope retained as SELECTED SUPPORTING qualified (plan-list VERIFIED, timing X-lead UNRESOLVED, page re-dated Aug26 never authority). Other groups: c042→c023/c024, c069→c031, c070→c029 each with retained primary stated in machine; no bytes lost, no double-count.
- Runner-readiness (F5): writer maps each Matrix Discovery via its single `evidence_task_id` to deterministic `candidate:<issue>:sha256(task)[:16]` at writer time (route-map §2). Ledger 439 = 409 Matrix assignable +30 nonMatrix separate accounting (26 EXCLUDED +4 DUPLICATE, 0 tasks/0 views, not assignable). R2 machine fields `matrix_candidate / runner_disposition / runner_usage` encode this: 41 SELECTED (PRIMARY for FEATURE+SECTION, SUPPORTING for SUPPORTING) +368 HOLD/NONE (10 ineligible HOLD +358 CONTEXT HOLD).

## F2 — 319 arxiv triaged from captured atoms + 26 bodies actually read (no new fetch)

**Triage (all 319 from captured task atoms, not unread):** lane/score/updated_at/screening/abstract excerpt joined per DID in `w34-r2-arxiv-triage.json`. Clusters concrete, not boilerplate:
- CL-C coding-robustness 68 (code agents, TDD, SQL, structural inference) — overlaps P2/P3 developer surfaces as method without product delta
- CL-G lm-training 60 — pre/post-training methods, no W34 release
- CL-D eval-benchmarks 48 (FloodReasonBench, Holtercare, ReFrame, K-Bench, etc.) — benchmark methods, eval interest only
- CL-B serving-efficiency 33 (15127 agentic workloads, 14967 WAN CIR, 18591 estimator, AEGIS, MoE) — infra debate background, no deployment
- CL-H out-of-window 29 (updated_at outside [08-14T22Z,08-21T22Z): 08-22 to 09-02, e.g., 16032 08-29, 15389 08-24) — post-window, cannot be W34 main event
- CL-A agent-memory 28 (QUMem, Proof-of-Execution, D2ACCI, Remember-Verify-Ask, Beyond Majority, rEDMRec) — redundant with P2 memory box as maker-reported protocols
- CL-D retrieval-cost 26 (14927 4-protocol/4181-math routing, 16096 commercial-tax license/cost, Trustworthy RAG) — cost debate contextual, not weekly event
- CL-E multimodal 13, CL-G niche 8 (FZ-VLM clinical etc.), CL-F safety 6

Per-DID rationale in r2 machine references title fragment + lane/score/date/screening/cluster + bytes/sha + redundancy vs P1–P5 (e.g., “14927 [training_methods score9 08-14T22:35Z INSPECT CL-D]: cost-aware protocol routing 4181-math … overlaps P1/P2 cost debate as maker-reported routing accuracy, no W34 deployment → HOLD context”). No “unread therefore exclude”; 29 out-of-window have date reason, rest have method/redundancy reason.

**Deep consumption (26 captured HTML 112KB–1.5MB actually read, stdlib strip):** reviewer 5 (14927/14967/15004/15127/16096) + 21 KEEP 2608 + refresh K-bench KEEP. Body sections verified present (Abstract/Introduction/Method/Evaluation/Results/Limitations where present), text_len 30–152KB. Qualitative ledger `w34-r2-body-read-ledger.md` records per-body supported findings + limits:
- 14927 routing: 4-protocol matched benchmark confirmed in body §§2–5, but router precision weaker than failure-risk probe, no code link, no deployment → contextual, not event.
- 14967 WAN: CIR 4–5 orders, 12–19%/yr, crossover/compression/packet/optical levers, agentic compounding long-haul case confirmed §§2–4, but analytical pre-measurement + Lightstorm vendor → background.
- 15004 FZ-VLM: Florence-2 + Zephyr-7B pulmonary (77.18%/67.96%/79.13%, MAE 2.58mm, Stage2 89.5%) confirmed, but clinical niche NLST single-dataset → negative triage example, HOLD.
- 15127 agentic workloads: long-running tool/state/I-O, non-LLM bottlenecks, pay-go breakdown confirmed §§3–5, strongest serving background to P1/P2, but suite proposal maker-measured → HOLD, KEEP retained.
- 16096 commercial-tax: MuSiQue/HippoRAG-2 license audit +13 embedders cost model confirmed §§3–4, but disclosure audit not deployment → HOLD.
- 21 KEEPs (memory, code robustness, eval, safety, serving): each confirms method/eval beyond abstract (e.g., 18389 code-agent robustness transforms, 19534 AEGIS triple-masking, 21100 ReFrame safety alignment, 21470 mobile-DB forensics) but all maker-reported without reproduction or W34 first-party deployment; overlap selected P2/P4 mechanisms as background with redundancy; retained as HOLD context, KEEP screening honored (not demoted to DROP). K-bench scientific-agent requests similarly method-only.
- No promotion: desired load-bearing weekly-event claim (e.g., “W34 serving breakthrough”, “W34 memory product”) is missing in accepted Evidence; bodies support method insight only. If such claim were material, exact DID/claim/location/body-SHA + upstream Evidence revision would be returned to Root — none returned here because no promotion selected; do not silently promote or add unbound claim to Architecture.

**Compression counterfactual restated with evidence:** trigger NOT met (41>1). Consumed subset shows 6th technical package (retrieval/agents/eval/safety methods) is supportable as *background box*, but would supplement, not displace, P1–P5 VERIFIED first-party deltas (Bedrock/pricing/GA/safety/infra). Sparse 1-package alternative still rejected with reason. Full 319 consumption would add depth to CL-A/B/C/D, not create confirmed W34 events (all PARTIAL maker-reported, 29 post-window).

## F3 — 39 non-arxiv CONTEXT per-DID (≥15 high-signal expanded, no template)

R2 machine gives per-DID card-joined reasons (artifact + limitation + redundancy/window). High-signal 20 expanded, e.g.:
- c001 GLM-5.3 08-18 entry 50% Code Bench Z.ai-reported boundary-date vs 22Z UNRESOLVED, Discovery Aug14 vs captured Aug18; adoption delta high-signal but timing blocks FEATURE → HOLD.
- c009 Mythos/Opus binders + NMR 25min Anthropic-reported, dual-use gating limits general availability → HOLD science background.
- c013 DSpark 3.18x/2.87x (means 2.1–2.7x) greedy-only Liquid-reported → HOLD inference background.
- c015 UI-Mate repo-first no Tencent announcement → HOLD.
- c025 Build cadence vs availability gap (locator resolves to Console), overlaps c066/c067 → HOLD background with no-loss note.
- c050 AutoDesign SPLIT_DELTA pattern (Aug14 base + Aug15 Harness) honest but 7-config AUTHOR_CLAIM no reproduction → HOLD (split recognized, core denied).
- c083/c092 paper surveys, c024 observed-not-captured, c027–c029 vendor-counted/planned/background, c032 beta-drift, c036 agenda-not-results, c095 note-lines. Remainder 19 with tight card-joined limits (undated/secondary/pre/post/workflow-only). No status upgrade; all HOLD/NONE.

## F4 — Page cost / reader synthesis vs prior 12 (no automatic 17pp)

- Prior 12pp reference only; no page cap in v2 validator or Production Profile (route-map §§7/11). Author-supplied plan must be justified in utility, not headcount — 60/40 dropped (unmeasured).
- r2 plan tightened to **14–15pp** (from v1 16–18pp): P1 3–4pp (distribution/pricing deltas need tables, boundary sidebars as 0.5pp boxes), P2 4pp (largest — 4 GA primaries + control-plane box justifies largest share: pay-and-collaborate is the W34 mechanism shift), P3 2–3pp (enterprise snapshots qualified, trio as one box), P4 3pp (safety terms need verbatim limits), P5 2pp (infra/economics closing). Total 14–15pp saves 2–3pp vs v1 by merging docs/how-to (c087/c104/c105/memory) into one P2 box and keeping 11 qualified SUPPORTING as sidebars/boxes, not full sections.
- Reader synthesis per package in v1 §2 preserved; downstream debt noted: Weekly `section_label` + closing summaries, Longform package-ID/coverage rules not yet authored (route-map §7) — future authoring debt, not current blocker.
- Qualified-boundary ceiling kept: 11 PARTIAL SUPPORTING-only with explicit “date-level only / Sep8 snapshot / researcher-only” qualifiers, never headlined as confirmed-W34. Dossier hesitation questions preserved.

## Indispensable existing-data / upstream gaps (no new fetch authorized)

- None indispensable for qualified presentation above. Optional upgrades only if Human/root later demands confirmed headlines: Aug14/21 clock-time headers/sitemap/archived versions (c002/c020/c039/c022/c045/c066/c102-addition), Sep8→entry-dated bytes (c099–c101), MSRC+NVD for c055/c006, Aug21 listing bytes for c024, HOLD first-party durables. No fetch performed; any gap-fill returns to Root with specific scope.
- No upstream Evidence revision requested in r2 (no promotion). If future review promotes any arxiv/non-arxiv method to core, exact DID/claim/location/body-SHA + revision will be returned before Selection write; not hidden in prose.

## Counts (computed, not inferred)

`w34-r2-counts.json`: ledger 439 = Matrix 409 (41 SELECTED +368 HOLD) + nonMatrix 30. SELECTED 41 (12 FEATURE /12 SECTION /17 SUPPORTING with 11 qualified). Packages P1 11 / P2 11 / P3 8 / P4 7 / P5 4. Statuses 38V/363P/8N, materiality 41M/358C/10H, ledger 358C/41M/10H/26E/4D. Triage 319 clusters as above, bodies read 26, non-arxiv per-DID 39. Selection count unchanged from v1 (fixes are placement/rationale, not count).

## Attribution

Author r2 DATA only. v1 preserved. Independent re-review still required before Architecture dossier + Human ARCHITECTURE_REVIEW. No Draft/PDF/Gate/R4.
