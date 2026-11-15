# W34 R2 POST-prepare review — independent (mechanical-gated content PASS, no approval)

Reviewer: author-independent substantive reviewer, not input writer/operator/mechanical reviewer (opencode-General; serving model unknown, not fabricated).
Scope: actual R2 HIGH prepare output `w34-repaired-20261112-r2` in selected cc1c only. No adopt/proof/resume/readback/Selection/Architecture, no synthetic external decision, no Human approval.
Method: Read + Glob + Grep + data-only stdlib hash (no project imports/Git/network/Production writes/subagents, no source edits, no test execution). Repaired runtime cc1c path READONLY. Independent mechanical gate relied upon (not repeated): packet `w34-r2-mechanical-postprepare-comparison.md` + machine below.
Recorded_at: 2026-11-14T00:53:08Z (actual UTC at write).

## 1. Mechanical gate relied upon (actual machine, not operator claim)

- Machine: `w34-r2-mechanical-postprepare-comparison.json` SHA256 `a8288b8f48ed480d72a91383f1c626710dbc65127f623bdcc9c0d5c9091924f5`/1602390B; report md `4c19de7146e08ddb1da597c226836ebf145a8aa8254463b72ad657f8115c3a1f`/5817B. Basis OLD active only (`5ca6…/574b…/f089…/e8…`), R1 inert comparator preserved.
- Verdict quoted: `PASS — exact preservation for all unaffected; no remaining mechanical issue.`
  - Cards 409: 405/405 unaffected byte+parsed exact (entity order preserved original, top order identical; no R1 252-byte reorder drift), 4 affected differ only `claims/limitations/verification.finding`.
  - Views 409: 405/405 unaffected byte+parsed exact (`evidence_sha256` identical because card bytes identical; materiality/rationale/scope identical), 4 affected exact `['evidence_sha256','materiality','profile_annotations']` (new card sha derivation + CONTEXT→MATERIAL + same rationale).
  - Tasks 409/409 byte+parsed identical (correction lives in request records, not tasks).
  - Ledger 439 rows: 435/435 unaffected parsed-identical (incl 4 DUPLICATE/DROP, 354 CONTEXT, 26 EXCLUDED, 10 HOLD); affected 4 exact 3 fields CONTEXT→MATERIAL; file +12B (7→8 chars ×3×4).
  - Request order-preserving `bb6042c6…`/1654899: all 409 `records[].entity` order == base, no `sort_keys` alphabetization.
  - Raw 4 byte-identical reuse, never re-copied.
- Strict equality holds with NO per-field ignored mechanical. Prior R1 false byte claim stays withdrawn; R1 decision `c7ba…` stays HELD, untouched.

## 2. R2 manifest/request/refs bound (actual bytes read)

- Manifest `sources/2026-W34/research/v2/acceptance-revisions/w34-repaired-20261112-r2/revision-manifest.json` `867eba96242eab0cf3e34277048e8497952c804f0805b4d09feacdb51b392a7b`/438583B, `revision_id w34-repaired-20261112-r2`.
- Request `sources/2026-W34/research/v2/acceptance-revision-inputs/w34-repaired-20261112-r2.json` `bb6042c67c4d2c2c81a857a5a26a211f33a181cd913a53c5894dcab8a6bf5ea6`/1654899B (409 = 405+4, supp `ce6f977a…`/389414 explicit, R1 request/manifest/Raw preserved per r6 report).
- beforeState `sources/2026-W34/production-state.json` `d7acd29b1518399ffc2376eb07e102491a6ec9782b3fdd79815c5f230e1886b0`/4087 EVIDENCE_REVIEWED, guard absent, 7 slots absent. beforeCheckpoint all three `CANDIDATES_NORMALIZED.json 0979f9f7703a25c2bd3424824bc4ad9f8719e8e7bcc49c19c5573d0f70ab593a`. Old four refs active (evidence `edf21e4de…`/126592, views `3777133c…`/159498, ledger `f089cc4e…`/186202, completeness `e8c432dd…`/71532 LIMITED).

## 3. Content bounded PASS — same approved R1 input, verified on actual R2 bytes

- 15127: Q1 shifting-workloads literal, Q2 arrivals/orchestrator §§3/7, Q3 29-40%/4.5x/4.6x/35.2%/5-10/28GB/32x §§4-6 maker-reported, Q4 artifact presence; PARTIAL AUTHOR_CLAIM; target `8fab99aa…` lane agents_tools score14; binding `supplement-src-6f78fb828e6ec113`; VERIFIED; `observed_at 2026-09-08T15:34:01Z`, `accessed_at 2026-09-08T14:33:56Z`; view MATERIAL box P2 rationale.
- 16096: Q1 Enterprises literal, Q2 13x8/HippoRAG-2/Tasks A-D §§3-4/App, Q3 floor/cost/checklist §§4-5 discussion; target `5841bec7…` score9; binding `c980beaaa7c4448a`; VERIFIED; historical profile dates retained.
- 21100: Q1 While-MLLMs literal, Q2 B.2-only/academic/RQ1-5, Q3 37.28→45.95 POPE/Math/Physics §§5.2-5.6; target `b6357aec…` score17; binding `70c044a81cc5695d`; VERIFIED; `observed_at` historical.
- 18389: Q1 full sentence with `\n` natural break, Q2 2x4 SWE-bench paired, Q3 6.7pp/6-of-16/simpler-robust/non-transfer; target `0dd05128…` score17; binding `c54d707262dc6b1b`; VERIFIED (first-evaluation authors-describe only).
- All Q1–Q3 AUTHOR_CLAIM (no independent reproduction), Q4 PRIMARY_FACT presence-only (no availability/version fetch), no deployment assertion. Raw staged copies FULL-DID, byte-identical reuse (`85c70376…/314048`, `a4c2aafe…/414077`, `56b48291…/388712`, `da737a85…/711224`); literal necessary not sole truth; hidden chrome ignored.
- Views MATERIAL total 45 (41+4); ledger 439; completeness LIMITED/closure-null/residuals identical (MiniMax rechecked; provisional-materiality-awaits-Sol) — old rationale still honest, no stale universal claim.

## 4. Decision

SuppliedDecision R2 `w34-supplied-decision-r2.json` (packet root, parallel to HELD r1) is truthful on actual R2 bytes + this content pass + the mechanical machine above. It is research input for root proof/adopt decision — NOT Human approval, NOT adoption. Normal prepare success implied nothing; only this gated review + machine do. R1 originals/copies/decision `c7ba…` preserved untouched. Await root proof/adopt disposition; no Selection claimed (event semantics: awaits independent Selection review).

Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN. Stop at Human Commit Point.
