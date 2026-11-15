# W34 correction proposal review — repaired runtime (independent content reviewer)

Reviewer: independent content reviewer, not DATA author/setup operator.
Scope: W34 `w34-repaired-patch4.json` proposal DATA only. No HIGH prepare/adopt, no manifest/decision PASS, no synthetic external decision.
Method: Read + Grep read-only. No project imports/runtime/tests/Git binary/network/Production/active writes/subagents. Repaired runtime `cc1c` path read as source+material READONLY.
Date: 2026-11-12. Folder date is not execution-time evidence.

## 1. Basis identities (as recorded, string-equality checked)

- New runtime: `.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work`
- True source epoch (setup independent review, decoded commit + saved raw): `cc1c7fd1cf979e71fda4ae2164828b37bc1b2325`, parent actual e84 `e84a82aca000c990597ea8cf60f548e2ff187bd1`, tree `ed2dc4ddd4a9486ccc9d0944bbd48653199b2485`, init480 `480823560c0c26ed2e5baa18e0e79a22b2839a27`. Both States EVIDENCE_REVIEWED. Final773 manifest `a7e40c4711a66b4d1d2541e6af1a97fd0e531d217e233f45ce43b40e19cef40c`/202833B, patch `171812f686c05d8494de8bd32a6c00e043dc5ff1aa7452204a8e35f16848600d`/5532921B, head `409b292756dd1277b9dfae87679934c0d2ce251c`.
- Note: `w34-repaired-pins.json` `actual_runtime.source_epoch` reads `cc1c7fd1cf979e71fda4ae2164828b3d37bc1b2325` (extra `3d`, 42 chars, invalid SHA). Non-blocking for patch content; HIGH operator must use true `cc1c...b37...` epoch above from setup independent review + decoded commit, not pins typo. Recommend DATA fix to pins before next packet, no re-review of patch required for this typo alone.
- Base interactive: `sources/2026-W34/evidence/v2/accepted/5ca6f31033dcaed6a153f0eb6f838f18bc9bdd1674a19a941f8c8378f88e4e48/interactive-evidence.json` 1576279B `15e87eef65753bd0eeff8c512651859d6cb3b8b57127d0243925628acbf1d112` (== `w34-corrected-input-r3-20261104.json` per dossier). Base supplement: `sources/2026-W34/external/evidence-supplement/evidence-authority-supplement-r2-fresh-basis.json` 389414B `ce6f977a3e690e779c380b7b035d9247207e262b5c50a5b14b6b6b8f0fbc704e`, 428 sources.
- CP four refs (from Evidence checkpoint `CANDIDATES_NORMALIZED.json` `0979f9f7703a25c2bd3424824bc4ad9e8e7bcc49c19c5573d0f70ab593a`, not setup-owner Discovery/Screening/Evidence summary): Evidence `edf21e4de5f7ab8db2d5189f45abc8cc6d0cf6475e532b20bcc56b0ce5660218`/126592, Views `3777133cc09d0189ab97cc1d8ff1f8b420108d43880f69f1745356508b8acfce`/159498, Ledger `f089cc4eedb49a81b4b925c1219f22a77237d16f28fdee73f20a3744e725e91d`/186202, Completeness `e8c432dd6275e81df5286cb8e0d55d99e27aa0812c52a114d870dddaf0d2795f`/71532 LIMITED. Checkpoints: ISSUE `3c64e40bde778b6b6ecdcf73e2403079373a79cc47bee764ed8eb5cea0de92cf`, DISCOVERY `4d3221d347d15a6b041703ce2cf3133546636e3066e37a02cf67f5fcbc7d4611`.
- Unaffected405: hash `20a5313741d54bf89afd856b3e56950b62954a6d317f14c6ae7ce7783852433d`/1358779B, full409 = 405+4. Patch contains only 4 new_records, no unaffected record present.

## 2. Original task targets EXACT (no split-schema repeat)

Read 4 task files in repaired runtime, compared string-equal to `w34-repaired-patch4.json` `verification.target`:

- 15127 `task-ef1d67cebe6877951aae.json`: `evidence_task_id evidence:2026-W34:8fab99aa7093acb9`, `discovery w34-event-arxiv-2608-15127`, `supplement-src-6f78fb828e6ec113`, `verification_targets[0]` == patch `verification[0].target` (Abstract-level arXiv Discovery lead 15127 lane agents_tools, matched=agents_tools,evaluation,inference_serving,language_models,memory_context,retrieval_embeddings; title_matches=agents_tools,inference_serving,language_models; score=14; provisional Sol review; abstract excerpt `Agentic applications are shifting...`). PASS.
- 16096 `task-4fe332e988709b31c162.json`: `evidence:2026-W34:5841bec7775ece26`, `supplement-src-c980beaaa7c4448a`, target == patch (lane evaluation, matched=evaluation,language_models,retrieval_embeddings; title_matches=evaluation,retrieval_embeddings; score=9; excerpt `Enterprises connect...`). Preserves `cc-by-nc-4.0` as plain text from discovery summary, no `<span>`/`<math>` split. PASS.
- 21100 `task-f49a436a94e02b9e94ee.json`: `evidence:2026-W34:b6357aec74216e97`, `supplement-src-70c044a81cc5695d`, target == patch (lane evaluation, matched 7 groups; title_matches 4; score=17; excerpt `While multimodal...`). Quotes first sentence only, avoids later `<span>ReFrame</span>` split. PASS.
- 18389 `task-56725e6005598b70b8c4.json`: `evidence:2026-W34:0dd05128103b336c`, `supplement-src-c54d707262dc6b1b`, target == patch (lane agents_tools, matched 5; title_matches 5; score=17; excerpt `AI code agents are increasingly deployed...variations remains poorly understood.` with space, discovery-normalized). Patch first-claim correctly uses body newline variant (see §4), target correctly uses discovery space variant. No confusion. PASS.

Source_bindings in patch match `authority_supplement_source_ids` in tasks for all 4. Evidence task IDs match. No old split-schema error.

## 3. Substantive new claims (all 16 claims + limitations)

All `status PARTIAL`, `entity_type PAPER`, `artifact_type PAPER`, `organization null`, `canonical_url https://arxiv.org/abs/2608.XXXXX` correct. All Q1-Q3 `AUTHOR_CLAIM`, Q4 `PRIMARY_FACT` presence-only. All `materiality MATERIAL` with bounded Research-Notes rationale, `scope_dimensions [current relevance, technical significance]`, `window MAIN_EVENT`, `carry false`.

### 15127 — From LLM Inference to Agentic Workloads (2608_15127.html 314048B 85c70376aa8fc521ef4877aafe69402a4a18b79496cac8032316b07d275c67c9)
- Q1 (claims[0]): `Agentic applications are shifting AI serving from isolated model inference to long-running workloads in which LLMs coordinate tools, environments, and persistent state.` Literal at `abstract1.1` line 259 first sentence. Context `Method/system as reported Abstract/§§2-3, not reproduced, no deployment` — honest. No deployment/W34-event upgrade.
- Q2: workload generator (one-by-one/Poisson/trace-driven via orchestrator protocol), measurement toolkit, default benchmarking settings, §§3/§7. Grounded lines 827-830 (generator owns R, arrival processes, orchestrator protocol). Labeled `not audited`. No independent proof claimed.
- Q3: maker-reported `29-40%, up to 4.5x, 4.6x, 35.2%, 5/10, 28GB, 32x`. Grounded abstract lines 263-271 (5/10 +28GB, 32x with math, 29–40%/4.5x/4.6x/35.2% +19.3% aggregate). Patch omits 19.3% — omission, not fabrication. Explicit `maker-reported, §§4-6, design explorations, no reproduction/significance/holdout`. Correct.
- Q4 PRIMARY_FACT: artifact-link presence observed. True: github langchain/claude-code/pi-autoresearch/firecrawl/grafana/cadvisor/dcgm/codex/mini-swe-agent + huggingface nsfw/transformers/text-embeddings lines 1927-2341. Claim says presence only, availability/version not fetch-verified. Correct, no availability assertion.
- Limitations (3): maker-reported only, benchmark suite proposal not W34 deployment, no deployment/reproduction/first-priority, HKUST/Alibaba/ByteDance attribution not deployment proof. Sound.
- Verification VERIFIED: confirms §§2-3 method, §3/§7 eval, §§4-6 results as span-grounded AUTHOR_CLAIM. No PASS fabricated.

### 16096 — The Commercial Tax (2608_16096.html 414077B a4c2aafef170bd915418979475983b009f4236786f67ce81a370747568e44f75)
- Q1: `Enterprises connect language models to their own data through retrieval.` Literal at `abstract1.1` line 281 first sentence, before `<span>cc-by-nc-4.0</span>`/`<math>`. Avoids split-schema error correctly; licensing fact stays in bounded Q2 context.
- Q2: `13 embedders/8 makers, HippoRAG-2 fixed anchor, Tasks A-D, panel/re-measurement, §§3-4 + Appendices`. Grounded abstract line 281 (thirteen embedders/eight makers/one identical harness), §§2.1/3.x/4.x, Appendices. Labeled not audited.
- Q3: maker-reported discussion `commercial-embedder floor, indexing/embedding/answering cost breakdown (one-time vs recurring), buyer checklist`, §§4-5, no retrieval deployment. Grounded §§4.4-4.7/§5, cost tables, buyer discussion. No vendor corroboration claimed.
- Q4 PRIMARY_FACT presence only. True: `https://github.com/Toryx-AI/commercial-tax-multihop-retrieval` line 1306 + Zenodo DOI + huggingface NV-Embed links. No availability fetch. Correct.
- Limitations: maker-reported only, audit only, no deployment/vendor corroboration/W34 event. Sound, includes Limitations §6 per finding.
- Verification VERIFIED §§3.1/4.1 license audit, §§3.2/4.2 floor, §§3.4/4.5-4.7/§5 cost/discussion. Numbers remain author-reported. No numeric table fabricated in claims (2.31/CI/p=0.001/Nemotron 2026-07-16 stay in body, not asserted as independent fact). Sound restraint.

### 21100 — ReFrame (2608_21100.html 711224B da737a85b9fad92509ba08e9877c1ba359d47adf00cb3bd2c99ceccf5152e383)
- Q1: `While multimodal large language models (MLLMs) extend model capabilities beyond text, they also make safety alignment increasingly challenging.` Literal at `abstract1.1` line 298 first sentence, before `<span>ReFrame</span>`. Correct split avoidance; ReFrame mechanism stays bounded Q1 context, closed-source applicability author-described not proven.
- Q2: `previously released benchmarks cited in Appendix B.2 only (no newly collected data), strictly for academic research/safety evaluation not operational/commercial/harmful purposes; RQ1&2 main, RQ3 ablations, RQ4 scalability, RQ5 runtime, plus case studies.` Grounded TOC lines 204-208 (RQ1&2/RQ3/RQ4/case/RQ5), line 232 (B.2 Details of Dataset), lines 1087-1088 (POPE/MMMU Math/Physics/CS, Appendix B.2), evaluation scope. No protocol audit claimed.
- Q3: maker-reported `best average accuracy 37.28 to 45.95 with gains on POPE/Math/Physics; ablations/scalability/runtime §§5.2-5.6`. Grounded lines 1111-1113 (POPE/Math/Physics headers), 1126 (37.28), 1188 (45.95 +8.67 gain). Labeled author-reported, no reproduction/significance/holdout. Correct.
- Q4 PRIMARY_FACT presence only. True: huggingface Qwen3-VL-8B/4B/Qwen3.5-9B/Qwen3.6-35B/Qwen3-VL-235B lines 2324-2372. No availability/version fetch. Correct.
- Limitations: maker-reported only, test-time only, no retraining-free deployment proof for closed-source beyond author description, cross-modal/over-refusal scope author-framed, no general MLLM safety resolution. Sound.
- Verification VERIFIED §4 method, §5.1/B.2 eval, §§5.2-5.6 gains as AUTHOR_CLAIM. No PASS.

### 18389 — Jagged Frontier (2608_18389.html 388712B 56b4829134fcf85b0131b70ef8ce0641d5289c57c4edd9cb5c79735d3a9d37ea)
- Q1 exact contiguous sentence with source newline, JSON `\\n` legal: `AI code agents are increasingly deployed to resolve real software issues, yet their reliability under superficial code\\nvariations remains poorly understood.` Verified lines 347-348 (`...superficial code` newline `variations remains...`). Full sentence used, not generic prefix truncation. Natural line-break context, not injected. Context `Method as reported Abstract/Introduction/SPT Definition/Catalog/Validation/Composition; not reproduced; authors describe as first such evaluation (description only, not asserted fact here).` Honest — line 379 `We present, to our knowledge, the first such evaluation` is reported as description, not independent fact. Correct.
- Q2: `2 scaffolds (mini-SWE agent, OpenCode) each with 4 frontier models (Claude Opus 4.5, Kimi K2.5, MiniMax M2.5, Qwen 3.6-27B) across SWE-bench Verified/Pro instances; multiple runs per unperturbed/perturbed yielding paired resolve-rate; two-randomness protocol + one-run-per-variant efficient split.` Grounded lines 351-354 (2 scaffolds/4 models/Verified+Pro/paired runs), 391 (54 instances: 28 Verified +26 Pro), 819-820 (scaffolds +4 models, 16 configs), 2055 (20 runs/condition, Newcombe). Paraphrase `two-randomness/one-run-per-variant` is author-described protocol shorthand, labeled `benchmark/scaffold choice not audited`. Bounded, not independent proof.
- Q3: maker-reported `small degradation most configs, up to 6.7pp mean drop most affected, significant in 6/16, simpler scaffold more robust, concentrated not diffuse, rankings do not transfer`. Grounded lines 355 (6.7pp/6 of 16), 356-357 (Qwen most robust mini-SWE/Verified yet most brittle OpenCode, simpler more robust), 395-396, 964,968,971, 2028-2029. Labeled RQ1/RQ2 author-reported, no independent reproduction beyond reported protocol. Correct, table actual not made up.
- Q4 PRIMARY_FACT presence only. True: `https://github.com/CSU-TrustLab/jagged-frontier` lines 372,1941 + huggingface MiniMax/opencode/astroid lines 1304-1350. No availability fetch. Correct.
- Limitations: maker-reported only, robustness counterweight to vendor GA claims only, no invalidation of specific deployment, no first-priority, no deployment/reproduction. Sound.
- Verification VERIFIED SPT method, 2x4 paired eval, RQ1/RQ2 6.7pp/6-of-16/simpler-robust/non-transfer as AUTHOR_CLAIM.

Hidden chrome: `<p id="selectedTextModalDescription" hidden>Content selection saved. Describe the issue below:</p>` line 79 in all 4 bodies. Ignored by patch/routing/dossier, never used as claim/procedure. Correctly treated as untrusted DATA.

## 4. Future Raw routing (FULL DID, byte-identical copy proposal, no write now)

- `w34-repaired-raw-routing-map.json`: 4 entries, `future_raw_path sources/2026-W34/external/evidence-supplement/raw/w34-event-arxiv-2608-XXXXX.html`, `basename_contains_full_did true` all 4, `source_file .../evidence-bodies/arxiv/2608_XXXXX.html` with bytes/sha matching §3, `note: Future Raw = byte-identical copy, files NOT written now, hidden chrome untrusted`.
- `w34-repaired-staging-map.json`: same 4 future paths (order 15127/16096/18389/21100, same set), `sourceManifestPointers: supplement already carries 428 sources incl 4 affected; future Raw copies are byte-identical routing copies, not new supplement entries`, `No active source_root/external write`. Correct — no supplement inflation, no LOW proof bypass.
- Literal predicate alone is not semantic proof: patch/dossier explicitly state first-claim literal is mechanical proof predicate only, other claims require §§-bounded support, trivial fragment does not verify rest of card. Observed. No overclaim.

## 5. Unaffected 405 + Views

- Patch changes only 4 DIDs, preserves `unaffected405_hash`, no Views/Ledger write. Current Views in runtime remain provisional execution annotations (`peer-style research lead...Sol decisions` for research leads, distinct first-party rationales for product items). No View rationale mutation proposed. Ledger/Completeness untouched here. Bounded PASS: structural (no unaffected record in patch) + hash string equality to pins; full 405-byte recomputation awaits HIGH prepare-time verification, not fabricated here.

## 6. DM022 completeness (no autoload PROMOTE)

- `profile-completeness-v2.json` `overall_status LIMITED`, `closure null` line 1749. Three 7-field rows (`obligation_id/dimension/description/status/discovery_ids/evidence_task_ids/rationale`): `weekly:current-relevance LIMITATION` (434 screened/409 evidenced, residual long-tail/date-precision), `weekly:technical-significance LIMITATION` (first-party bodies high-signal, paper results maker-reported, provisional materiality awaits Sol), `weekly:carry-over SATISFIED` (C076/C077 rechecked, no promotion). Residual limitations 5 preserved. No promotion to SAT, no autoload completeness SAT. Dossier §4 preserves status/rationale, requires no Human confirmation for repository-owned shape. Correct.

## 7. Materiality CONTEXT→MATERIAL (bounded Research-Notes, not blanket)

- 4 MATERIAL with destination-restricted rationales: 15127→P2 box (serving shift/I-O cost backgrounds pay-and-collaborate), 16096→P1 sidebar (license/cost audit qualifies pricing/SOTA/throughput), 21100→P4 box (test-time mechanism note, c055 class with full body+limitations), 18389→P2 box single destination (scaffold-dependent robustness counterweights vendor GA Slack/Copilot/Kimi, stronger date/body than c066/c099-101). All `SUPPORTING`, restricted to box/sidebar, not core event. Justified research-notes use vs unread-cluster blanket exclusion. No claim that unread cluster is MATERIAL. Sound.

## 8. Schema-read check (honest, no validator execution)

- `w34-repaired-schema-read-check.json`: `honest_not_runtime_pass true`, `validator_not_executed`, `no acceptance PASS claimed`. 7 read checks all PASS-read: weeklyRecord shape, verification target names exact, source_bindings/taskIDs stable (8fab99aa/6f78fb, 5841bec/c980beaa, b6357aec/70c044a8, 0dd05128/c54d70726), raw sha/size/DID, first-claim literals (18389 newline, hidden chrome ignored), claims 2-4 §§-bounded, record shape preserved (claims[0] literal + MATERIAL rationale only, 405 hash, 7-field x3). Read scope only, independent review needed. No false runtime PASS. Correct.

## Verdict: PROPOSAL_READY (bounded, for HIGH prepare only)

Proposal DATA is truthful, span-grounded, and bounded: exact discovery targets preserved, source bindings stable, first-claim literals present with FULL-DID future Raw routing proposed (not written), numerics maker-reported not independently proven, no deployment assertion, artifact presence only, 405/Views/Ledger/Completeness preserved, materiality narrowly justified, no synthetic decision fabricated.

Approve for normal HIGH prepare on selected new runtime `cc1c7fd...` (true epoch, not pins typo) via separate concrete root dispatch with exact new HEAD/tree/tool pins, preserving all unaffected semantics. Stage only root-authorized exact new Raw/input/supplement paths, then normal HIGH prepare.

NOT adoption: no prepared manifest, no after-graph review, no Selection/Architecture. No synthetic external decision permitted for real research. Later final review of exact HIGH outputs + actual supplied Decision may follow if positive, but not now.

Read scope: `README.md`, `astra-operation-resolution.md`, `setup-independent-review.md`, `w34-repaired-patch4.json`, `w34-repaired-pins.json` (lines 1-15 + grep + 1800-1839), `w34-repaired-raw-routing-map.json`, `w34-repaired-staging-map.json`, `w34-repaired-schema-read-check.json`, `w34-repaired-content-review-dossier.md`, 4 task files (`task-ef1d.../4fe3.../f49a.../5672...`), 4 HTML bodies (lines + grep: 15127:259/271/827-830/1927ff, 16096:281/1306/1309, 21100:298/1111-1113/1126/1188/2324ff, 18389:347-358/391/395-396/819-820/964/971/1941), Views sample, `profile-completeness-v2.json` closure/overall/obligations, `CANDIDATES_NORMALIZED` refs via setup review. No execution, no hash recomputation via code, string-equality + locator inspection only.

Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN. Stop at Human Commit Point.
