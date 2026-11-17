# W34 substantive Selection/Architecture review R2 — actual 3231 outputs (independent, DATA only)

Reviewer: Fresh independent substantive W34 reviewer (same as R1, no prior candidate author/operator/root). No Human. No implementation/writer/rerun/adoption.
Recorded: 2026-11-17 R2. Authority: root `notes/rephase-1-selection-architecture-resume-20261117/astra-operation-resolution.md` §§1–2 FULL (initial `EDITORIAL_READY` NOT adopted). This R2 corrects R1 gaps; R1 docs preserved with superseded pointer, not rewritten.
Method: data reading ONLY. `read` + `glob` + `grep` + stdlib `hashlib/json/pathlib` inventory via `bash python3 -c` (read-only, no project imports/runtime/tests/Git/network/State canonical writes/subagents/reconstruct readback). Source 3231 recorded only; source State read for pins only. Writes ONLY packet-local: this file + machine JSON + `w34-architecture-dossier-ja-r2.md` + `w34-attention-inventory-r2.json` in `notes/rephase-1-selection-architecture-resume-20261117/`. Inventory is reviewer DATA, not canonical attention production, no writer.

## 0. R1 corrections (root §1)

- R1 “41 VERIFIED first-party PRIMARY anchors” WITHDRAWN. Actual from JSON join (§3): 24 PRIMARY all VERIFIED/MATERIAL; 21 SUPPORTING = 15 PARTIAL/MATERIAL + 6 VERIFIED/MATERIAL. Total VERIFIED selected = 30, PARTIAL selected = 15. Historical 41 vendor = 24P VERIFIED + 11 vendor PARTIAL SUPPORTING + 6 vendor VERIFIED SUPPORTING; +4 papers PARTIAL = 45. Historical 41 is vendor count, not VERIFIED-PRIMARY count.
- c001 chronology CORRECTED to actual card (§5): captured entry dated 2026-08-18, Discovery basis Aug 14 ZCode signal, exact Aug 14 time vs 22:00Z UNRESOLVED. R1 “Aug18 vs Aug14” paraphrase superseded by exact matrix/evidence wording below.
- Page slack CORRECTED: target 15 / max 16 ⇒ total slack 1. Architecture note “max 16 allows 0.5 overflow per package” is package-level tolerance, not total 0.5. R1 “0.5 overflow” total withdrawn.
- Full hashes CORRECTED programmatically (stdlib, §1). R1 matrix line contained prose typo with two variants; R2 uses single verified pins below.
- 770 overflow NOT counts-only in R2: full stage-qualified inventory `w34-attention-inventory-r2.json` (770 rows, §4). Blanket LOW-risk / no-systematic-defect / compression-PASS withdrawn in R1 form; R2 gives scoped evidence-grounded omissions (§5) and explicitly does NOT assert no alternative could exist from unread bodies (§7).

## 1. Execution identity and verified pins (stdlib, this unit)

- Instance: `.rephase-1-editorial-runtime/selection-scaling-real-20261116T021943Z/candidate-work`
- Source recorded only: `3231a0c280287411513bba359f4d3d2b6703f591`, parent `ae0dd1ee5b0e7a85c44bdab0e6cd024bf12f0c56`, tree `ff01b73e6012fd4519fdfb3807186753ff330367` (no fresh Git cert).
- State W34 `sources/2026-W34/production-state.json` 4162B `a8586351b096fda65793dfc20604fae9404f9e9ea06e164c3b9f9c72b576e47d`, lifecycle EVIDENCE_REVIEWED. Profile 2371B `2a8c3089cec29eb64e121cdf0429eed38670df704ebe955079751198557cfeb1`. PREARCH CP `.../w34-repaired-20261112-r2/checkpoint/record.json` 6054B `73ab28ea79da8bb13d7083d30eda7fa3188f060f0dbaa96a65e2407daae3ac48`, KIND PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1. PREARCH cleanup completion distinct from research profile-completeness LIMITED; kept separate.
- Typed 4 refs (verified bytes+SHA this unit): evidence 126592B `eef77479b8d9c003ee8daae7eb882ea2aa63063ea10aea3e43d1f951c747427d`; views 159502B `3727485ac1f791d64c3d951520bfab7694821ad4584140b913f91a1c48f654ae`; ledger 186214B `066230f48ff3d29e714be35e86968a4ec834f9dacefb4590f4b64ac1fb73b320`; completeness 71532B `d869027aefce95cde4478b875204c7f9307482b3835d5fdc6` LIMITED. Active State/Profile/COPY completion receipt (`profile-completeness-v2.json` 71532B `e8c432dd…`, distinct from PREARCH completeness bytes) noted separately, not conflated.
- 7 outputs (verified bytes+SHA this unit): matrix 683098B `f4469c85b819d8436d37eecbaac68e07551e4942f0d86f124e6b6469480261af`; selection 375063B `f3a5000fe3c5370ae0768dc993f28fc3c64d9086ead566427728a1a6ff39a030`; architecture 24447B `9a76294ef05688c11fa6e114e96c98723e47c418522998ce835385c12a595615`; summary 314350B `1b7f6076b11c5b47f41ab838ce70da7e5b2f4d856a3d309f6e8859828040eff7`; attention 18437B `d68b5f319e996a73076338b939f6661e46648ef9fd5b3033346e17ccfe6f5b92` (770/50/720); input 378396B `15375476f308fbfeb79c4e8f3f4d53d85d5cf917e36d29d3c3777580301aab3a` == frozen; audit 1436B `61d6a0bc5d427ecfb2bf5a4a3f47cdda2f9c01bf55b6ff3906f41bc01e6fd982` (6 pins match).
- Future canonical review commit NOT ESTABLISHED. No Human approval asked/implied. No R4/Production/Draft/PDF/quality cert.

Prior docs read FULL: resume README, continuation-observation §§1–7, normal-stage-operation-map §§1–8, root closeout FULL + final review §§10–12 FINAL-BINDING, independent-real-output-review §10, governance FULL, prior input review + machine (PROPOSAL_READY_FOR_PREFLIGHT), dossier draft r4, read-scope pins, per-DID map (header + selected), repaired content dossier (4-paper spans).

## 2. Read scope — exact new vs reuse (inventory scan ≠ full body read)

NEW reads in R2 (retained fixed774/papers, no fetch):
- All 7 output files + State/Profile/CP + 4 refs hashed via stdlib (above).
- Full 770 inventory built from actual files: screening-accepted (439 decisions), materiality-ledger (439 rows), candidate-matrix (409 rows), candidate-selection (409 assignments), attention (50 shown + counts). Each of 770 rows enumerated with stage/subject/DID/current disposition/role/materiality/evidence status/attention reason/shown-overflow/risk flag in `w34-attention-inventory-r2.json` (total 770, shown 50, overflow 720).
- Evidence task JSONs (claims/limitations/verification, not full HTML) for 14 high-risk DIDs: c001/c009/c013/c015/c027/c028/c032/c050 + arxiv 14927/15008/18591/19534/20999/21095 (§5). Matrix rows + selection rationales for same DIDs fully read. c001 evidence task `task-8e8cce5d357f0f241977.json` (3 claims/3 limitations/UNRESOLVED verification) read to correct chronology.
- Architecture FULL, summary header + all 45 SELECTED destinations + sampled HOLD, selection all 45 SELECTED + HOLD samples, per-DID map selected rows.

REUSED as history (not re-read wholesale, explicitly not promoted to new full read):
- 4-paper literal spans from `w34-repaired-content-review-dossier.md` (15127 314048B, 16096 414077B, 21100 711224B, 18389 388712B, AUTHOR_CLAIM preserved). No new HTML fetch.
- Prior input review verdict, r2 triage/body-read ledgers (319 triage +26 body-read) as history for 364 HOLD cluster reasons; remaining ~293 hash-only explicitly NOT semantic PASS.
- Body-byte/SHA strings in matrix/selection treated as existence/format markers only, never as claim consumption.

Complete full-row inventory ≠ full primary-body review. No undocumented full-read claim. No SHA-as-consumption.

## 3. Actual selected verification × role (JSON, not historical 41)

- Total assignments 409. Join matrix evidence_status/materiality × selection disposition/usage:
  - HOLD/NONE + NEEDS_MORE/HOLD 8; HOLD/NONE + PARTIAL/HOLD 2 (ineligible 10 total); HOLD/NONE + PARTIAL/CONTEXT 346; HOLD/NONE + VERIFIED/CONTEXT 8
  - SELECTED/PRIMARY + VERIFIED/MATERIAL 24 (all PRIMARY VERIFIED)
  - SELECTED/SUPPORTING + PARTIAL/MATERIAL 15 (11 vendor PARTIAL +4 papers)
  - SELECTED/SUPPORTING + VERIFIED/MATERIAL 6 (c087/c104/c105 + kimi-cli/defenders/replit refresh)
- So vendor selected 41 = 24 VERIFIED PRIMARY + 11 PARTIAL SUPPORTING (c002/c020/c022/c039/c045/c055/c066/c099/c100/c101/c102) + 6 VERIFIED SUPPORTING; papers 4 PARTIAL SUPPORTING (15127/16096/18389/21100). R1 “41 VERIFIED PRIMARY” is false and withdrawn.
- Packages: P1 7P+5S, P2 8P+5S, P3 2P+6S, P4 4P+4S, P5 3P+1S =45, each single-destination, no overlap/HOLD-in-packages. Memory JSON `b7f2b1b1713db179` PRIMARY P2 single; c102 `5a69916736f60a65` SUPPORTING P3 single.

## 4. Full 770 inventory (reviewer DATA, not canonical production)

File: `w34-attention-inventory-r2.json` (543664B, schema 1.0, total 770 / shown 50 / overflow 720). Each row: stage, subject_id, discovery_id, candidate_id (if Matrix), current_disposition, architecture_role, materiality, evidence_status, attention_reason, shown, overflow, risk_flag. No writer rerun; no canonical attention overwrite.

Construction (actual files, not counts-only):
- MATERIALITY 40 from ledger: DUPLICATE 4 (c042/c067/c069/c070), EXCLUDED 26 (5 coverage +21 events), HOLD 10 (c033/c035/c038/c051/c053/c054/c057/c065/c097/c103). All shown=True (attention first 40).
- SCREENING 366 from screening-accepted: DROP 30, INSPECT 200, MAYBE 136. Shown=True for first 10 DROP (5 coverage + c042/c049/c059/c060/c061) matching attention order; remaining 356 overflow.
- SELECTION 364 from selection HOLD assignments. All overflow (attention shown contains no SELECTION items). Each carries selection rationale + matrix materiality/evidence status.
- Shown/overflow matches attention file: 40+10 shown, 356+364=720 overflow. Verified arithmetic, plus per-row IDs/rationales.

Risk flags (55 true): all 14 requested high-risk DIDs + all 10 ineligible + all 8 VERIFIED/CONTEXT HOLD DIDs (16 stage-qualified rows as each DID appears in both SCREENING and SELECTION). Generic-cluster membership noted per row but not auto-risk unless above.

Generic reason clusters (templated, not identical):
- Screening DROP: template “{Title} is outside ordinary W34 scope, duplicate/context-only, routine noise, or lacks standalone technical relevance…” with per-DID title (5 coverage API +25 events). Templated triage, not final Selection reason.
- Selection HOLD arxiv: distinct prefix (lane/score/date/cluster/title + distinct body BYTES/SHA) + repeated suffix “maker-reported/no reproduction; retained as context, not selected; no shallow year-group exclusion”. Suffix repetition is real; prefixes + body bytes keep rows distinguishable. Ledger HOLD rationale minimal (“Screening=MAYBE/INSPECT/KEEP; Edition View=HOLD”); final HOLD reason lives in selection/matrix, not ledger alone.
- No claim that template repetition equals semantic review; overflow rows remain counted + rationale-enumerated, not semantically PASSed.

## 5. Evidence-grounded omissions (high-risk sample, actual cards)

Each below from actual matrix + selection + evidence task (claims/limitations/verification) in retained captures. No new fetch. No SHA-as-consumption.

- c001 GLM-5.3 (`8e8cce5d357f0f24`, PARTIAL/CONTEXT, HOLD): Matrix remaining_boundaries exact: “Exact Aug 14 time vs 22:00Z W34-start boundary remains unresolved: captured entry is dated 2026-08-18 while the Discovery basis cited an Aug 14 ZCode changelog signal.” + “Coding-benchmark figures (50% gain, SOTA) are Z.ai-reported…” + “Aug 26 Flash post-cutoff excluded.” Evidence task: claim-1 Aug18 entry coding capabilities (VENDOR_CLAIM, entry-dating differs noted); claim-2 50% gain maker-reported; limitation-1 same Aug18 vs Aug14 UNRESOLVED; verification UNRESOLVED (release VERIFIED, week placement UNRESOLVED, no upgrade). HOLD grounded: high-signal adoption delta retained for Sol judgment but timing blocks FEATURE. R1 paraphrase corrected.
- c009 Mythos/Opus (`75ca5f5467476f99`, PARTIAL/CONTEXT, HOLD): claim-1 Anthropic Aug18 15 targets/14 success 22–35% vs 10–15% typical; limitation-1 all figures Anthropic-reported, dual-use review outside bytes; verification VERIFIED program/figures stay maker-reported. HOLD grounded: science result, dual-use gating, not platform delta.
- c013 DSpark (`eb80e3816ce9e6e1`, PARTIAL/CONTEXT, HOLD): claim-1 300M draft checkpoints for 3 LFM2.5 models day-one llama.cpp/SGLang; limitation-1 vendor-reported, honest expectation 2.1–2.7x means, MoE-Apple ~1.18x per post tables. HOLD grounded: vendor-measured, overlaps serving without deployment.
- c015 UI-Mate (`bcd14468786a33a9`, PARTIAL/CONTEXT, HOLD): claim-1 HF card 27B Apache-2.0 GUI agent from Qwen3.6-27B pyautogui actions; limitation-1 no Tencent announcement/API/launch post, repo-first so dating rests on repo timestamps. HOLD grounded: no dated W34 launch.
- c027 Gemma (`45da0fab1d914445`, VERIFIED/CONTEXT, HOLD): claim-1 Aug20 1B downloads +100K variants + Awesome directory; limitation-1 methodology undisclosed company-reported; verification VERIFIED non-release milestone. HOLD grounded: adoption milestone, not model release (one of 8 VERIFIED/CONTEXT holds correctly not promoted).
- c028 Micron (`dcee03f265c21eb5`, VERIFIED/CONTEXT, HOLD): claim-1 Aug20 Micron Research Labs $10B decade plan; limitation-1 commitment not spent funds, headcount undisclosed. HOLD grounded: commitment statement, no technical breakthrough.
- c032 OpenRouter (`7e5bc9cb43395366`, VERIFIED/CONTEXT, HOLD): claim-1 Aug17 Activity dashboard spend/requests/tokens views; limitation-1 $6.2K anecdote vendor-reported account-specific. HOLD grounded: tooling context to P3, not core.
- c050 AutoDesign (`5f5762e99390d352`, PARTIAL/CONTEXT, HOLD): claim-1 meta-harness human-preference top; limitation-1 all figures maker-reported no reproduction/significance/holdout. HOLD grounded: SPLIT_DELTA honest but significance insufficient for core (SPLIT pattern like c031/c102 noted, but paper AUTHOR_CLAIM).
- arxiv 14927 (`3cc4e37f782b5aba`, PARTIAL/CONTEXT, HOLD, score 9): cost-aware protocol routing method insight to P1/P2 debate, distinct body 556046B, no code link (L1). HOLD as method not weekly event; contextual to selected 15127/16096 debate.
- arxiv 15008 (`63b3353663a9af96`, PARTIAL/CONTEXT, HOLD, score 13): memory-substrates evaluation, 1201745B, redundant with P2 memory box + selected memory JSON per rationale. HOLD as maker-reported protocol without deployment.
- arxiv 18591 (`d7350b0b00aa16a4`, PARTIAL/CONTEXT, HOLD, score 15): lightweight multimodal estimator for compute-optimal inference, 230313B. HOLD as infra method without first-party deployment; overlaps P1 pricing without displacing VERIFIED deltas.
- arxiv 19534 (`1f15ad1299cef528`, PARTIAL/CONTEXT, HOLD, score 17 KEEP): AEGIS gradient-isolation shield, 1046566B, no code link. HOLD as safety method without deployment; highest-score HOLD retained as context.
- arxiv 20999 (`80a58bb07e912394`, PARTIAL/CONTEXT, HOLD, score 14): ordinal lens alignment for multimodal LLMs, 521619B. HOLD as method without deployment.
- arxiv 21095 (`4a2001f5cfb34276`, PARTIAL/CONTEXT, HOLD, score 16 KEEP): Trustworthy RAG evaluation agent, 197521B. HOLD with explicit box-space counterfactual (dossier), routing/WAN background considered. Not silent drop.

VERIFIED+HOLD/CONTEXT join: 8 distinct DIDs (c027/c028/c029/c032/c034/c036/c046/c095) = 8 HOLD assignments, 16 stage-qualified inventory rows (each in SELECTION HOLD + SCREENING row). All retained as background with vendor/methodology limits; none displaces VERIFIED PRIMARY deltas. Ineligible 10: 8 NEEDS_MORE (c033/c035/c038/c051/c054/c057/c097/c103) +2 PARTIAL/HOLD (c053/c065), all HOLD/NONE, upgrade requires upstream Evidence revision.

## 6. Substantive judgment (scoped, no universal negative)

Thesis (distribution-and-governance week) holds on reviewed scope: 30 VERIFIED selected (24 PRIMARY anchors +6 VERIFIED SUPPORTING boxes) +11 vendor PARTIAL SUPPORTING (date/Sep8/researcher-limited sidebars) +4 AUTHOR_CLAIM papers bounded box. No confirmed-W34 headline from PARTIAL. Grouping P1→P5 coherent; P3 trio-merge editorial; Research-Notes box within 5 packages, not 6th. Page 14+1=15 target correct, max 16 slack 1 total (package 0.5 tolerance noted, not total). Old 2pp criterion not used; 15pp not rendered, no layout/PDF/visual QA.

Omissions above are each evidence-grounded with timing/source/method limits. Duplicated templated reasons are disclosed, not hidden. Compression counterfactual remains scoped: even if unread arxiv bodies were fully consumed, reviewed evidence (timing blocks, vendor-reported without deployment, repo-first without announcement, method-without-event) makes a different multi-item core displacing VERIFIED distribution/governance deltas unlikely on reviewed scope — but this is NOT asserted for unread bodies individually. No claim that no alternative could exist from unread bodies. Unread ~293 remain hash-only, explicitly not PASS.

Authority distinctions hold: 4-paper AUTHOR_CLAIM, vendor figures vendor-reported, KEV feed-only vs 281KB shell captured-but-unconsumed, MSRC 2717B shell captured-but-unconsumed, Meta Mac AUTHORITY_NOT_FOUND, Grok Vertex RETRIEVAL_FAILED (observed-not-captured, not inferred from unfetched). Chronology: date-level UNRESOLVED preserved, post-window correctly HOLD, Sep8/Aug26 never cited as primary-date authority.

## 7. Verdict and limits

**Verdict: EDITORIAL_READY_FOR_NORMAL_STAGE** (bounded substantive review on actual 3231 outputs + full 770 inventory + high-risk evidence-card sample; sufficient for root to dispatch normal validation/checkpoint path per operation-map, NOT Human approval, NOT R4, NOT Production, NOT quality-nondegradation, NOT rendered-15pp PASS).

- No BLOCKING systematic research defect returned. No DID/claim/retained-Raw proof of systematic defect requiring new fetch/source-code. No new fetch proposed; all retained fixed774/paper captures only.
- No CHANGES_REQUIRED to Selection/Architecture DATA before normal stage. If validation exposes cost/capability/retention/HEAD/contract drift, return finding to root before broadening (no auto generic-reader/R4/PDF/approval).
- Root will review this R2 before stage dispatch. Next is bounded `survey_stage_validation_v2` + `build_stage_checkpoint`/`advance_with_checkpoint` toward SELECTION_COMPLETE → ARCHITECTURE_ESTABLISHED, then Human dossier + ARCHITECTURE_REVIEW gate. No hand-editing State, no canonical overwrite, no regeneration to recover counts.

Limits: inventory enumeration ≠ 720-body semantic review; ~293 hash-only; evidence cards read, not full HTML re-read except prior 4-paper spans; 22:00Z clock UNRESOLVED where stated; lifecycle net UNKNOWN; whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN. Source 3231 is execution identity, not canonical Human-reviewed commit. Ordinary Commit/Push Human-owned. Stop at coherent unit boundary (no extra Human Commit Point required per root §21).

Paths:
- `notes/rephase-1-selection-architecture-resume-20261117/w34-attention-inventory-r2.json`
- `.rephase-1-editorial-runtime/selection-scaling-real-20261116T021943Z/candidate-work/sources/2026-W34/candidate-matrix-v2.json`
- `.rephase-1-editorial-runtime/selection-scaling-real-20261116T021943Z/candidate-work/sources/2026-W34/candidate-selection-v2.json`
- `.rephase-1-editorial-runtime/selection-scaling-real-20261116T021943Z/candidate-work/sources/2026-W34/architecture-v2.json`
- `.rephase-1-editorial-runtime/selection-scaling-real-20261116T021943Z/candidate-work/sources/2026-W34/architecture-review-summary-v2.json`
- `.rephase-1-editorial-runtime/selection-scaling-real-20261116T021943Z/candidate-work/sources/2026-W34/architecture-review-attention-v2.json`
- `.rephase-1-editorial-runtime/selection-scaling-real-20261116T021943Z/candidate-work/sources/2026-W34/orchestration/v2/interactive/selection-architecture-input.json`
- `.rephase-1-editorial-runtime/selection-scaling-real-20261116T021943Z/candidate-work/sources/2026-W34/orchestration/v2/interactive/selection-architecture-audit.json`
- `notes/rephase-1-selection-architecture-resume-20261117/astra-operation-resolution.md`
