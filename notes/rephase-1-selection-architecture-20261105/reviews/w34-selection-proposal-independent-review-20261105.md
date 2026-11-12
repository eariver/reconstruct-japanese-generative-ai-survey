# W34 Selection proposal independent review — author v1 (CHANGES_REQUIRED)

**Role:** NEW independent editorial Selection/Architecture reviewer — NOT proposal author, NOT Astra/root, NOT Sol/Luna, NOT Human. No false attribution.
**Date:** 2026-11-05. **Scope:** W34 author v1 only (`w34-selection-proposal.md`, `w34-per-did-disposition-machine.json`, `w34-human-dossier-draft-ja.md`, `w34-read-scope-and-pins.json`) against e84 pinned four-ref data + route-map + governance + final Evidence reviews context.
**Method:** packet DATA + isolated-runtime source/JSON read-only (`Read`/`Grep` only). No new fetch, no active/source/runtime writes, no imports/tests/Git/Production, no subagents, no State advance, no Draft/PDF, no Human Gate request.
**Verdict: `CHANGES_REQUIRED` — author proposal NOT ready as actual substance.** No approval created from counts or inherited materiality. Proposed judgment below is reviewer judgment, not a Human Gate.

## 1. Authority checked (sound)

- Instance only `.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work`, epoch e84, State `EVIDENCE_REVIEWED` `d7acd29b…` 4087B, checkpoint `CANDIDATES_NORMALIZED` `0979f9f7…` 4549B — pins match author + route-map-data §§21–67.
- Four refs live-checked in route-map: Evidence `edf21e4d…` 126592B 409, Views `3777133c…` 159498B 409, Ledger `f089cc4e…` 186202B 439, Completeness `e8c432dd…` 71532B 3 LIMITED. No matrix/selection/architecture/summary/attention/`gates/`/`interactive/` exist — writer has not run. Correct.
- Matrix 409 = one Discovery per Evidence result (route-map §4, data §§68–98). Statuses 38 VERIFIED / 363 PARTIAL / 8 NEEDS_MORE; materiality 41 MATERIAL / 358 CONTEXT / 10 HOLD; status×materiality detail matches route-map §6. SELECTED-eligible 399; 10 ineligible (8 NEEDS_MORE/HOLD + 2 PARTIAL/HOLD). Ledger 439 = 41+358+10+26+4. Correct.
- Final Evidence context reused as history, not approval: resume-output `BOUNDED_PROCEED to EVIDENCE_REVIEWED` (new 5ca6f310 outputs) + authority-consumption `CHANGES_REQUIRED` + 16-item correction table (now fixed in 5ca6f310 per resume-output §2). Author's 11 qualified PARTIAL + researcher-only + Sep8-capture qualifiers are consistent with that correction. No status upgrade claimed by author — sound.

## 2. ALL439 disposition table — coverage sound, rationales + placement accounting NOT sound

**Coverage (sound):**

- Machine has 439 rows (verified by file length 6109 lines + spot joins). All 409 evidenced rows carry exactly one `evidence_task_id`; all 30 non-matrix rows carry `[]` — 26 EXCLUDED + 4 DUPLICATE. That matches Matrix-vs-Ledger rule (route-map §6): Ledger/discovery rows with no Evidence task do not become Matrix candidates and cannot be Selection assignments. Taskless-DROP lawful accounting preserved.
- 30 breakdown sound: 5 coverage API (ComfyUI/llama.cpp/TensorRT-LLM/SGLang/vLLM), 4 DUPLICATE groups, 2 carry-over C076/C077 (Music3.0 Aug13, H3 Aug03 pre-window, explicit disposal — satisfies completeness carry-over disposal obligation), 19 other screening DROPs. No HOLD promoted (10 HOLD_OUT), no NEEDS_MORE promoted, no DROP promoted. Chronology honesty sound: 11 PARTIAL timing-UNRESOLVED kept SUPPORTING-only with explicit `date-level only, no clock-time proof`, never FEATURE-confirmed.
- No quota used (no top-N/year-group/citation filter) — sound per Astra §2 and governance §8.

**Candidate-ID / source-fact identities (partly sound, fix needed):**

- Author joins actual Discovery/Evidence/View/Ledger per DID (`ledger_disposition`, `evidence_status`, `view_materiality`, `evidence_task_ids`, `duplicate_group`, `ledger_rationale`). Counts 12+12+17=41 are source-joined uniques, not a DID-range inference — sound as far as it goes.
- BUT final runner addresses Discovery IDs mapped to deterministic `candidate:<issue_id>:sha256(evidence_task_id)[:16]` (route-map §2). Author machine is proposal DATA (discovery_id + task IDs), not runner input. Acceptable at proposal stage, but author must state the mapping step is still to be computed at writer time — currently §7 implies `evidence_task_id` lists are "derivable" without showing the candidate-ID join. Add one line: runner input will map each DID via its single `evidence_task_id` to the deterministic candidate ID. No quota claim — do not present 41 as a budget.
- Per-DID rationales for 319 arxiv + 39 non-arxiv CONTEXT are boilerplate (see §§3–4), not card-joined editorial reasons. That fails Astra §2 ("every Matrix candidate needs a concrete disposition; generic body-not-fully-consumed for an entire cluster is not substantive") and governance §4.4/§8. Counts do not substitute for reasons.

**Unique-vs-placement accounting (CHANGES_REQUIRED — exact mismatch):**

- Author summary: FEATURE 12 + SECTION 12 + SUPPORTING 17 = 41 uniques. Machine uniques verify: 12 FEATURE + 12 SECTION + 17 SUPPORTING = 41 distinct DIDs. Sound in machine.
- Prose-vs-machine placement mismatch:
  1. `w34-event-gap-aws-agentcore-memory-json` is `SECTION_CORE / P2` in machine (single placement — valid). Prose P1 lists "Memory JSON Aug20" as SECTION_CORE **and** prose P2 merges "c087+c104+c105+Memory JSON as one box". That reads as two-package reuse. Under `validate_architecture`, SELECTED SUPPORTING may sit in ≥1 package, but SELECTED PRIMARY/SECTION must have exactly one destination and the same candidate cannot be PRIMARY and SUPPORTING. A single DID cannot be SECTION in two packages. Fix: keep machine single-placement (P2 SECTION), delete Memory JSON from P1 prose list. Then P1 = FEATURE 4 + SECTION 3 (c018 + kimi-k3 + wan-prime) + SUPPORTING 4 = 11, P2 = FEATURE 4 + SECTION 4 (c019+c031+c047+memory) + SUPPORTING 3 (c087+c104+c105) = 11. Update prose P1 "SECTION 4" → 3 and P2 "SECTION 3 + SUPPORTING 4 (merged box)" → SECTION 4 + SUPPORTING 3, or re-decide placement with a single destination and single usage.
  2. `w34-event-c102` Antigravity: prose splits one DID into "Aug20 bundle SECTION-level + Aug21 addition qualified SUPPORTING". Machine correctly assigns single `SUPPORTING_EVIDENCE / P3`. One DID cannot carry two roles/packages. Fix: keep machine single SUPPORTING ceiling (honest — Aug21 part unresolved), delete prose "section-level" split language, or split into two DIDs upstream (not selected here — requires Evidence revision, so keep SUPPORTING).
- Duplicate-collapse loss note: `c067 grok-build → c025 + c066` — but `c025` itself is EXCLUDED CONTEXT in machine while `c066` is SUPPORTING selected. Collapsing a DUPLICATE into a partly-excluded primary needs explicit no-loss text (which bytes of c067 survive in c066 vs which are excluded with c025). Add one sentence per duplicate group; currently "no separate evidence, no loss" is asserted without per-group byte accounting.
- Ledger 439 = 434 expansion (incl. 2 carry-over) + 5 coverage distinct from R369/E439 bases — correctly not summed. Completeness `434 vs 439` stale count-language noted but not blocking — carry forward, do not re-litigate.

## 3. Key failure: 319 arxiv excluded as unread though captured readable (CHANGES_REQUIRED)

**What the bytes actually show (read, not inferred):**

- Sampled Evidence task cards are abstract-level triage only: `technical_claims_accepted: false`, `discovery_only: true`, `authority_class: DISCOVERY_SOURCE_ONLY`, `summary_text: Abstract-level arXiv Discovery lead … Abstract excerpt: …`. Examples:
  - `2608.14927` — title "LLMs Can Predict Failure Risk, But Struggle to Predict Which Collaboration Protocol Pays Off: Cost-Aware Protocol Routing Across Reasoning Tasks", lane training_methods, score 9, `updated_at 2026-08-14T22:35:37Z` IN_WINDOW, abstract: four protocols (Baseline/Single/PER/Broadcast) over 4,181 competition math + 4 robustness benchmarks.
  - `2608.14967` — title "When Does Distributed AI Inference Need More Wide-Area Bandwidth? A Co-Design Evaluation of Optical, Packet, and Software Levers", lane evaluation, score 11, `updated_at 2026-08-15T01:39:05Z` IN_WINDOW, abstract: CIR gap 4–5 orders, 12–19%/yr widening, KV-recompute/compression/routing/scheduling comparison.
- Both are facially relevant to Weekly technical significance (agents/eval/inference_serving/memory_context) and in-window EXACT_PUBLISHED. Authority-consumption review §4 already established: 328 arxiv supplement Raws are distinct per-DID full HTML 112–556KB (e.g. 14927 556046B vs 14967 112296B, different methods), NOT one atom ×180; 5 sampled confirm sections beyond abstract; remaining ~306 hash-only, NOT full semantic read. Author's own read-scope admits "~314 hash-only, NOT full semantic read".
- State is therefore `AUTHORITY_CAPTURED_BUT_UNCONSUMED` for the arxiv cluster, not `NOT_FOUND` / `RETRIEVAL_FAILED`.

**Why blanket EXCLUDE fails governance:**

- §4.2: for every substantive captured body that could affect materiality, Sol must inspect whether the body supports additional claims. Generic `primary still required / locator only / technical details unaccepted` is blocking if the body is present and readable. Author's identical 319× rationale ("hash-only PARTIAL maker-reported, no reproduction; distinct locators/bodies verified but not fully consumed; shallow year-group exclusion not used") is exactly such a generic placeholder applied as a cluster.
- §8: must sample and where risk indicates exhaustively inspect high-signal unselected, VERIFIED+CONTEXT/HOLD, richer-than-claims, unresolved-reason-contradicts-bytes, and same-generic-reason collapsed clusters. 319 identical rationales = same-generic-reason collapse at the largest scale in the edition. Two in-window high-score samples above already show richer-than-claims (full method/eval beyond abstract excerpt). No full-319 fulltext decoration is required, but calling all 319 irrelevant by lack of reading is not permitted.
- §4.4 compression audit: author correctly notes trigger NOT met (41>1) but then asserts counterfactual ("full arxiv consumption could support an additional methods/eval package but would supplement, not displace, VERIFIED core") **without consumption**. The counterfactual test requires asking *if fully consumed, could a materially different multi-item Architecture be supported?* — that cannot be answered for 319 unread bodies. The 6th-package dismissal is therefore unsupported.

**Minimal correction (captured bodies only; no new fetch):**

1. Triage all 319 at title/abstract/claims level (atom abstracts already captured — no new fetch): lane, deterministic score, in-window date, method/novelty/redundancy vs P1–P5. Produce per-cluster reasons (e.g. retrieval/agents/eval/safety/infra lanes), not one boilerplate string.
2. Deep-consume a risk-based subset of already-captured HTML to the depth needed for the proposed role (Astra §2): at minimum the 5 already-sampled (14927/14967/15004/15127/16096) + all KEEP→CONTEXT arxiv + top-score in-window semantic-shortlist (score ≥9). Record title/abstract/method/novelty per DID.
3. Decide explicitly: (a) confirm EXCLUDE with per-cluster/per-DID authority reason, or (b) promote a bounded set to a technical box / 6th package / SUPPORTING with maker-reported qualifier, or (c) HOLD with exact gap (e.g. needs reproduction). Replace the 319× identical string with cluster-level rationales that reference actual claims.
4. Re-run compression counterfactual on the consumed subset and restate §5 with evidence (which lanes would/would not displace P1–P5 core).

## 4. High-signal CONTEXT non-arxiv: same boilerplate pattern (CHANGES_REQUIRED)

- All 39 non-arxiv CONTEXT rows share one identical rationale ("retained as background; pre-window/post-cutoff/secondary/undated/workflow-only or insufficient W34 delta per card limitations"). Sampled cards show this hides per-DID distinctions:
  - `c001` GLM-5.3 flagship: official publisher page, `Keep W34 adoption/free-access/coding-agent delta regardless`, boundary-date-only vs 22Z. High-signal foundation-model delta reduced to boilerplate.
  - `c013` DSpark (LFM2.5 speculative-decoding checkpoints, vendor-reported throughput): FIRST_PARTY_LOCATOR via DailyX, KEEP, inference/local-AI lane. Needs per-DID novelty/redundancy vs selected inference items.
  - `c025` Grok Build (July beta → broad availability with publishing/sharing, Aug21): overlaps selected `c066` expansion and duplicate group `c067`. Needs redundancy analysis, not boilerplate.
  - `c050` AutoDesign (Aug14 base date-only + Aug15 DeepSeek Harness support clean in-window delta, SPLIT_DELTA): facially meets author's own split-delta pattern (cf. c031/c102 handling) yet excluded without split reasoning.
- Fix: replace boilerplate with per-DID (or tight per-cluster) card-joined reasons referencing actual claims/limitations/duplicate/redundancy/window relations. Minimum: expand the 15+ high-signal sample author already lists (c001/c009/c013/c015/c025/c050/c083/c092/…) with one sentence each; if that expansion reveals a systematic promotion miss, extend to the full 39. Do not upgrade statuses; give reasons.

## 5. Vendor/topic balance, page budget, qualified-boundary handling

- Thesis ("distribution-and-governance week") is coherent and fits the selected VERIFIED deltas (Bedrock/pricing/agent-GA/safety/infra). No quota, no business-only/safety-only narrowing — sound direction.
- 16–18pp target vs historical 12pp reference: author correctly does not copy historical 41/7/12pp allocation, but gives no positive rationale for +4–6pp. Route-map §7/§11: no page cap in v2 validator, no page budget in either Production Profile — page plan is author-supplied. 11 of 41 positives are timing/researcher-qualified SUPPORTING + 6 docs/how-to merged as boxes. Reader utility question: are date-level sidebars (c039/c022/c045/c066), Sep8 snapshots (c099–c101), Antigravity addition (c102), researcher-only CoSnitch (c055) worth +4–6pp, or should the issue be tighter (e.g. 12–14pp) with qualified items as boxes/omissions? Author must justify page allocation per package (why P2 5pp largest, P5 2pp) in technical-utility terms, not headcount. The asserted "~60% technical / ~40% business" mix is unmeasured — either measure it per package or drop the numbers.
- Qualified-boundary ceiling is honestly kept (SUPPORTING-only, "date-level placement, clock-time proof absent", "observed snapshots suggesting W34, not confirmed", researcher-only framing, vendor numbers as VENDOR_CLAIM/AUTHOR_CLAIM/SOCIAL_OBSERVATION). Do not headline any qualified item as a confirmed-W34 event. Dossier's 5 hesitation questions (§残る問い) correctly surface exactly these doubts to Human — preserve them; they are the reason this review is CHANGES_REQUIRED rather than a rejection of the thesis.
- Downstream keys not yet authored (route-map §7): Weekly `section_label` + closing summaries, Longform package-ID/coverage rules. Note as future authoring debt, not a current blocker.

## 6. Exact minimal corrections required (no new fetch; captured-body consumption only)

1. **Fix placement accounting (§2):** single destination + single usage per DID; remove Memory JSON from P1 prose (keep P2 SECTION), correct P1 SECTION 4→3 / P2 SECTION 3→4 + SUPPORTING counts; collapse c102 to single SUPPORTING (delete split-role language); add per-duplicate-group no-loss sentence (esp. c067→c025(excluded)+c066).
2. **Arxiv triage + subset consumption (§3):** title/abstract triage for all 319 from captured atoms; deep-read captured HTML for 5 sampled + KEEPs + score≥9 in-window shortlist; replace 319× boilerplate with per-cluster/per-DID reasons; restate compression counterfactual with evidence; decide bounded promotion vs confirmed EXCLUDE vs HOLD.
3. **Non-arxiv CONTEXT per-DID reasons (§4):** one sentence each for the 15+ high-signal sample (at minimum c001/c009/c013/c015/c025/c050/c083/c092/c024/c027/c028/c029/c032/c036/c095 + split-delta c050); extend if systematic miss found.
4. **Page/role justification (§5):** justify 16–18pp vs 12pp per package in reader-utility terms; measure or drop 60/40; keep qualified items SUPPORTING-only with explicit qualifiers; list downstream `section_label`/closing-summary debt.
5. **Runner-readiness line:** state deterministic candidate-ID mapping (Discovery → `candidate:<issue>:sha256(task)[:16]`) will be computed at writer time; carry-over disposal + HOLD/EXCLUDE handling already lawful.
- Permitted gap-fill is **consumption of already-captured bodies** (arxiv HTML 112–556KB + supplement manifest). Optional header/version URLs in proposal §8 remain optional upgrades only if Human/root later demands confirmed-W34 headlines — not required for the qualified presentation, and no fetch is authorized by this review.

## 7. What is sound (preserve)

- Four-ref pins, Matrix/Ledger/Completeness counts, 409-vs-30 accounting, carry-over explicit disposal, duplicate-group recording, no HOLD/NEEDS_MORE/DROP promotion, no status upgrade, chronology qualifiers, vendor/researcher/SOCIAL quarantining, base-vs-delta separation (Aug13 GA vs Aug16 pricing, Aug6 Dogwood vs Aug20 authoring, etc.), docs/how-to merge rationale (avoid inflating core count), rejected-alternatives structure, dossier hesitation questions, no Draft/PDF/Gate claim. Thesis direction may survive correction.

## 8. Boundary

- This is an independent reviewer judgment on author v1 DATA. It is not a Human Gate decision, not Architecture approval, not Selection acceptance, not R4 audit, not publication-quality evidence. No approval is created from 41 counts, 38 VERIFIED labels, or inherited MATERIAL labels. Whole NOT_READY/step4B3OPEN/audit unstarted/DM021+022OPEN; quality/adoption/savings OPEN. Stop at Human Commit Point; do not auto-start writer/API JSON, Selection writes, or SP work.

## Read scope + attribution

- Read: README + astra-working-resolution + route-map + route-map-data + proposal + full machine (6109 lines, all positive/HOLD/duplicate/carry-over rows + arxiv/non-arxiv EXCLUDE strings verified) + dossier + pins; governance FULL (211 lines, §§4.2/4.4/§8 applied); route four-ref + validator rules; Evidence task cards for 14927/14967/c001/c013/c025/c050; authority-consumption review FULL + resume-output review FULL (final context). Remaining ~314 arxiv + ~24 non-arxiv CONTEXT assessed via ledger/rationale strings + prior bulk hash/binding validation, not full semantic read — explicitly not claimed as PASS.
- Attribution: NEW independent Selection/Architecture reviewer. Prior BOUNDED_PROCEED/CHANGES_REQUIRED reviews cited as history, not reused as approval.
