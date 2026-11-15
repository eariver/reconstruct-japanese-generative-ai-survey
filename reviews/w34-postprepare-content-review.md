# W34 POST-prepare content/delta review — repaired runtime (independent, BOUNDED_RESEARCH_DECISION_READY)

Reviewer: author-independent reviewer, not input writer (General independent; serving model unknown, not fabricated).
Scope: actual HIGH CLI prepare output `w34-repaired-20261112-r1` in selected cc1c only. No adopt/proof/resume/readback/Selection/Architecture, no synthetic external decision, no Human approval.
Method: Read + Grep + stdlib read-only compare (json/hashlib/pathlib, no project imports, no Git/network/Production writes/subagents). Repaired runtime cc1c path READONLY. Actual validation/proof later root operator.
Prior proposal review preserved: `reviews/w34-correction-proposal-review.md` (+machine) untouched.

## 1. Actual outputs bound

- Root: `notes/rephase-1-repaired-correction-rehearsal-20261112/astra-operation-resolution.md` §7: absolute-root CLI SUCCESS exit0, no State/guard changes.
- CLI report: `cli-prepare-W34-20261113T135946Z-execution-report.md` + machine json + raw `pid257617/` (argv/env-whitelist/wall-start 20261113T135957Z/wall-end 20261113T140300Z/pid/stdout/stderr/exit 0).
- Manifest: `sources/2026-W34/research/v2/acceptance-revisions/w34-repaired-20261112-r1/revision-manifest.json` SHA256 `54de43edc49a24e2fd8ffaf02144a83c5812a2c59290eb1d3a914709e8583da2`/438583B, `revision_root` same, `work {cc1c7fd1cf979e71fda4ae2164828b37bc1b2325, ed2dc4ddd4a9486ccc9d0944bbd48653199b2485}`, `supplement_manifest ce6f977a…`/389414, request `057e186fb…`/1434802, 409 records (405 preserved +4), candidate package 409 tasks, candidate files 2460. First-claim literals in retained Raw (mechanical only). SEMANTIC now independently decided here; no proof/adopt.
- First wrapper relative-root failure retained 5 new (4 Raw + request) with no R manifest; root explicit absolute CLI continuation, no rewrite/delete, no new State. Preserved per §6.

## 2. Before graph still active, no Guard

- `production-state.json` EVIDENCE_REVIEWED, impl 48082356, human pending/pending, 7 pending (selection/architecture/draft/validation/preview/freeze/release), exception inactive, target ARCHITECTURE_REVIEW. SHA `d7acd29b1518399ffc2376eb07e102491a6ec9782b3fdd79815c5f230e1886b0`/4087 == manifest `before_state` == CLI `old_unchanged.state`.
- CP `CANDIDATES_NORMALIZED.json 0979f9f7703a25c2bd3424824bc4ad9f8719e8e7bcc49c19c5573d0f70ab593a` == manifest `before_checkpoint` all three.
- Old four refs still active: Evidence `edf21e4de…`/126592, Views `3777133c…`/159498, Ledger `f089cc4e…`/186202, Completeness `e8c432dd…`/71532 LIMITED. No guard file, retention 7 slots all absent/false, no State/guard/decision/adopt/SP writes. Old 773 manifest `a7e40c…` intact.

## 3. Task universe complete (409/409)

- Old tasks 409 == new candidate tasks 409, same filenames. Sample `task-0129bae…` (15762) byte-identical old vs new (all 78 lines). Affected task files preserve `evidence_task_id/discovery_ids/source_records/summary_text/verification_targets/screening_basis/authority_supplement_source_ids`.
- Original targets exact (no split-schema repeat):
  - 15127 `8fab99aa7093acb9` / `supplement-src-6f78fb828e6ec113` lane agents_tools score14
  - 16096 `5841bec7775ece26` / `c980beaaa7c4448a` lane evaluation score9 (cc-by-nc-4.0 plain, no span split)
  - 21100 `b6357aec74216e97` / `70c044a81cc5695d` lane evaluation score17 (first sentence only, avoids ReFrame span)
  - 18389 `0dd05128103b336c` / `c54d707262dc6b1b` lane agents_tools score17 (space-normalized discovery target vs newline body claim correctly distinguished)
- Candidate `tasks/` SizedRefs 409 in manifest lines 158-2204; `package.json` tasks list same 409 with discovery_ids + supplement source IDs.

## 4. 405 unaffected programmatic compare (not author claim)

Executed stdlib-only JSON compare old vs new (no project code):
- Results: `old_res 409` vs `new_res 409`, same filenames. `same_unaffected_exact=405`, `diff_unaffected=0`. 4 affected differ only `['claims','limitations','verification']`; status/entities/artifact/temporal/sources preserved.
- Tasks: 409 vs 409, same set; unaffected sample identical.
- Views: `old_views 409` vs `new_views 409`, same set. 405 unaffected differ only `['evidence_sha256']` (mechanical new-set binding); `materiality/rationale/scope_dimensions/profile_annotations` identical. 4 affected differ `['evidence_sha256','materiality','profile_annotations']` with CONTEXT→MATERIAL.
- Ledger: 439 vs 439, same ID set. `diff_unaffected=0`. 4 affected differ only `['downstream_disposition','rationale','evidence_view_statuses']` CONTEXT→MATERIAL.
- Only permitted mechanical bases differ (evidence_sha256 new-set hash, retention absent slots, manifest/tool set hashes). No semantic drift in unaffected.

## 5. Four new paper claims (maker conditions, as-of versions)

Candidate `results/task-*.json` 141 lines each, `temporal.observed_at 2026-09-08T15:34:01Z` retained historical (not new review time), `sources[0].source_class PRIMARY_PAPER`, `accessed_at` preserved per-paper (14:33:56/14:35:36/14:40:46/14:37:57).
- 15127 claims[0] shifting-workloads literal, Q2 workload-generator arrivals/orchestrator §§3/7, Q3 29-40%/4.5x/4.6x/35.2%/5-10/28GB/32x §§4-6 maker-reported, Q4 artifact presence only. Limitations no deployment/reproduction. Verification VERIFIED 314048B 85c70376…
- 16096 Q1 Enterprises literal, Q2 13x8/HippoRAG-2/Tasks A-D §§3-4/App, Q3 floor/cost/checklist §§4-5 discussion, Q4 `Toryx-AI/commercial-tax` presence. Limitations audit-only. VERIFIED 414077B a4c2aafe…
- 21100 Q1 While-MLLMs literal, Q2 B.2-only/academic/RQ1-5, Q3 37.28→45.95 POPE/Math/Physics §§5.2-5.6, Q4 Qwen hub presence. VERIFIED 711224B da737a85…
- 18389 Q1 full sentence with `\n` lines 347-348 natural break, Q2 2x4 SWE-bench paired/two-randomness, Q3 6.7pp/6-of-16/simpler-robust/non-transfer RQ1/RQ2, authors describe first-evaluation (description only). VERIFIED 388712B 56b48291…
All `AUTHOR_CLAIM` except Q4 `PRIMARY_FACT` presence-only, no availability/version fetch, no deployment assertion. As-of: arXiv 2608 bodies Aug 15/17/21/18, Nemotron 2026-07-16 cited in body not claimed as new, Qwen/OpenCode versions as body-reported.

## 6. Raw FULL DID + primary bytes (necessary not sole truth)

Staged copies `sources/2026-W34/external/evidence-supplement/raw/w34-event-arxiv-2608-{15127,16096,18389,21100}.html` byte-identical to captured `evidence-bodies/arxiv/2608_*.html` (314048/414077/388712/711224, sha 85c70376/a4c2aafe/56b48291/da737a85 match), basename contains FULL DID, no traversal. Literal presence is mechanical predicate only; rest of card requires §§-bounded AUTHOR_CLAIM support (observed). Hidden `Content selection saved` line79 ignored. Unaffected old claim bug (`Content selection saved` in 15762 claim-1) preserved exact, not silently fixed — correct preservation.

## 7. Status/materiality + completeness

- Requested 4 PARTIAL MATERIAL correct; candidate views MATERIAL total 45 (41 old +4 new). Results status PARTIAL 363 / VERIFIED 38 / NEEDS_MORE 8 preserved (new 4 PARTIAL within 363).
- Ledger 439 IDs preserved, 4 CONTEXT→MATERIAL with Research-Notes SUPPORTING rationales (P2 box serving/I-O, P1 sidebar license/cost, P4 box test-time safety, P2 box scaffold-robustness counterweight), restricted box/sidebar, not blanket unread-cluster promotion.
- Completeness candidate `profile-completeness.json` LIMITED, closure null, 3 obligations equal by ID to old (order differs only), residual 5 identical, no stale universal unconsumed claim, no auto SAT. Meaningful: long-tail/date-precision + maker-reported/provisional-materiality-awaits-Sol + MiniMax rechecked.

## 8. SizedRefs complete

Manifest `candidate_outputs`: package `26b1960be…`/157155, tasks 409 SizedRefs, cards 409 (lines 2205-4251), views 409 (4252-6298), `evidence_acceptance bcf35af5…`/126592 (same bytes as old edf21e4d but new set hash), `views_acceptance a09c2cb4…`/159502 (+4B vs old 159498 from 4 MATERIAL upgrades), `ledger 523df63c…`/186214 (+12B), `completeness d9c455da…`/71532 (same bytes, new set hash), `supplement_manifest ce6f977a…`/389414. `tool_pins` contract8 + orchestrator `survey-production-core-v2/0.15-postintegration-transport-thematic` + repo `cc1c…` + 7 tools (5 schemas incl `a99f0dc1…` request schema + 2 scripts `7f5fc9e0…/f312f02e…`). `work` expected head/tree cc1c/ed2dc4. `recorded_at 2026-11-13T14:01:53Z`, `executor HIGH prepare_revision`.

## Verdict: BOUNDED_RESEARCH_DECISION_READY

Actual content passes for supplied decision. No CHANGES_REQUIRED. Decision JSON written in PACKET only (no workspace adoption), reviewer General independent model unknown, actual UTC, not SYNTHETIC/Human.

Decision: `notes/rephase-1-repaired-correction-rehearsal-20261112/w34-supplied-decision-r1.json` SHA256 `c7ba7f2a5c9413b25ac149c4f47bd16a4a71a41e1e7ef43c6033977a0a95e19c`/4213B.
Source files: manifest `54de43ed…`/438583, beforeState `d7acd29b…`/4087, CP `0979f9f7…`, 4 Raw above, request `057e186f…`/1434802.
Read scope: astra §7, CLI report/machine/raw pid257617, manifest (158-2204 tasks, 2205 cards, 4252 views, 6299-6375 outputs/tool/work), candidate results/tasks/views ×4 affected + 0129 unaffected sample, package, ledger old/new, completeness old/new, State, retention inventory, 4 staged Raw vs 4 captured bodies, old tasks/results/views samples.
Restrictions: decision is research-input only; no manifest/decision PASS fabricated beyond this bounded decision; no adopt/proof/resume/readback/Selection/Architecture; later root operator owns actual validation/proof/adopt; prior proposal review preserved.

Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN. Stop at Human Commit Point.
