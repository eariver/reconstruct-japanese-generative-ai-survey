# W34 repaired correction — content review dossier (DATA only, no active write)

Role: DATA author, offline read-only. No project imports/runtime/tests/Git/network/Production/subagents.
Offline DATA/HTML parse only (stdlib). Runtime owner separately does new-copy HEAD/tool pins later.

## 1. Basis (READONLY)

- New runtime: `.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work`, epoch `cc1c7fd1cf979e71fda4ae2164828b3d37bc1b2325`, parent e84 `e84a82aca000c990597ea8cf60f548e2ff187bd1`, tree `ed2dc4ddd4a9486ccc9d0944bbd48653199b2485`. Initialization480 preserved, both EVIDENCE_REVIEWED, Profile/Contract8/checkpoints unchanged. Saved e84 + final 773 proof preserved.
- Base interactive: `sources/2026-W34/evidence/v2/accepted/5ca6f31…/interactive-evidence.json` 1576279B `15e87eef65753bd0eeff8c512651859d6cb3b8b57127d0243925628acbf1d112` (== `w34-corrected-input-r3-20261104.json`). CP four refs from `CANDIDATES_NORMALIZED.json` (not setup-owner summary): Evidence `edf21e4d…`/126592, Views `3777133c…`/159498, Ledger `f089cc4e…`/186202, Completeness `e8c432dd…`/71532 LIMITED.
- Proposals read: `w34-four-paper-correction-proposal.json` r3 DATA-only BLOCKED + ledgers. Preserved as history; stale first-claim summaries fixed as NEW DATA below, original r3 retained.
- Supplement: `evidence-authority-supplement-r2-fresh-basis.json` 389414B `ce6f977a…`, 428 sources. 4 affected supplement-only, 397+8 unaffected preserved. No new supplement entry needed; future Raw copies are byte-identical routing copies only.
- Unaffected 405 hash `20a5313741d54bf89afd856b3e56950b62954a6d317f14c6ae7ce7783852433d` (canonical sorted JSON). Full 409 = 405 + 4.
- No fetch, no active State/source write, no producer run. Request `work/tool_pins` later operator from new copy actual; no fake manifest/decision PASS.

## 2. Genuine quoted spans (literal UTF8 verified in captured bodies)

All spans verified via substring search in new-runtime bodies. Future Raw basename contains FULL DID (staging map). No appended claim, no derived-notes-as-primary, no trivial-fragment verification of rest of card.

Hidden page chrome `Content selection saved. Describe the issue below…` is present in all bodies as `<p hidden>` UI text. Ignored as untrusted DATA, never used as claim/procedure.

### 15127 — `2608_15127.html` 314048B `85c70376…`

- Q1 (claims[0]): `Agentic applications are shifting AI serving from isolated model inference to long-running workloads in which LLMs coordinate tools, environments, and persistent state.`
- Q2: workload generator arrival processes (one-by-one/Poisson/trace-driven via orchestrator protocol), §§3/7 evaluation design, not audited.
- Q3: maker-reported design explorations 29–40% / 4.5x / 4.6x / 35.2% / 28GB / 32x, §§4–6, no reproduction.
- Q4: artifact-link presence observed, no availability fetch. Title/entity `paper-2608.15127` unchanged.

### 16096 — `2608_16096.html` 414077B `a4c2aafe…`

- Q1: `Enterprises connect language models to their own data through retrieval.`
- Q2: 13 embedders/8 makers, HippoRAG-2 fixed anchor, Tasks A–D, panel/re-measurement, §§3–4 + Appendices, not audited.
- Q3: commercial-embedder floor, cost breakdown, buyer checklist, §§4–5 discussion, no deployment.
- Avoids `<span>cc-by-nc-4.0</span>` / `<math>` split by quoting first sentence only; full licensing fact stays in bounded Q2 context, vendor scope.

### 21100 — `2608_21100.html` 711224B `da737a85…`

- Q1: `While multimodal large language models (MLLMs) extend model capabilities beyond text, they also make safety alignment increasingly challenging.`
- Q2: released benchmarks only, Appendix B.2, academic safety-eval scope, RQ1–5 + cases.
- Q3: maker-reported 37.28→45.95, POPE/Math/Physics gains, ablations/scalability/runtime, §§5.2–5.6.
- Avoids later `<span>ReFrame</span>` by quoting first sentence; ReFrame mechanism stays bounded Q1 context, closed-source applicability author-described.

### 18389 — `2608_18389.html` 388712B `56b48291…`

- Q1 (exact contiguous sentence incl source newline, JSON `\n` legal): `AI code agents are increasingly deployed to resolve real software issues, yet their reliability under superficial code\nvariations remains poorly understood.`
  - Verified present with `\n` between `code` and `variations` (body lines 347–348). Short prefix alone would be generic; full sentence used instead of arbitrary truncation. Context cannot claim unsupported beyond reliability-under-rewrite.
- Q2: 2 scaffolds (mini-SWE, OpenCode) x4 frontier models, SWE-bench Verified/Pro, paired resolve-rate, two-randomness/one-run-per-variant protocol.
- Q3: maker-reported 6.7pp max drop, 6/16 significant, simpler-robust, non-transfer, RQ1/RQ2.
- Authors describe as first such evaluation (description only, not asserted fact).

## 3. Source class / provenance (no promotion)

- All 4 `AUTHOR_CLAIM` maker-reported, no independent reproduction/significance/holdout; no deployment/W34-event assertion. Q4 artifact-link `PRIMARY_FACT` presence-only.
- Verification `VERIFIED` = span-grounded method/eval/results above, numbers remain author-reported. No `PASS`/independent decision fabricated.
- Views/Ledger/Completeness: 405 unaffected + Views rationales preserved byte-identical (hash above). No materiality promotion beyond 4 CONTEXT→MATERIAL for Research-Notes SUPPORTING boxes.

## 4. Obligations — 3 explicit, 7 fields each, preserved status/rationale

Basis `profile-completeness-v2.json` (see pins exact copy), overall LIMITED. Each row has `obligation_id/dimension/description/status/discovery_ids/evidence_task_ids/rationale`. No Human question needed for repository-owned shape.

- `weekly:current-relevance` LIMITATION, `weekly:technical-significance` LIMITATION, `weekly:carry-over` SATISFIED (C076/C077 rechecked, no promotion). Residual limitations + `closure:null` preserved.

## 5. Supplementary Raw428 + 4 future-only routing copies

- Preserved 428 supplement sources incl 4 affected IDs unchanged. Future Raw = copy of captured bytes with DID filename (routing + staging maps). No active `source_root/external` write now. Wire/decoded distinction N/A (arXiv HTML plain, no gzip/CDX).

## 6. Stale r3 fixes as NEW DATA (original preserved)

- First claims summaries → literal UTF8 spans above (18389 newline preserved, hidden chrome ignored).
- Other claims keep §§ bounds genuine as-of, source class not truth.
- Entity/metrics/task/source bindings unchanged, 405 hash preserved.
- Claim classes remain AUTHOR_CLAIM (+ PRIMARY_FACT artifact presence); no VENDOR/PROJECT relabel needed for arXiv papers.

## 7. Limits + next

- Packet DATA only. No State/source/producer/Selection/Architecture/R4/Draft/PDF/Human Gate. Independent content review + HIGH prepare/adopt/resume/readback require separate root dispatches.
- Manual schema-read check scope only (`w34-repaired-schema-read-check.json`); validator not executed.
- Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN. Stop at Human Commit Point.
