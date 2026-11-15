# W34 R2 mechanical post-prepare comparison — exact preservation check (DATA only)

Role: NEW independent mechanical/data reviewer. Stdlib only, no runtime/project imports/tests/Git/network/Production/active writes/subagents. No validator loosening. No content reconstruction.
Basis: OLD active only (`5ca6…/574b…/f089…/e8…`), not R1. Prior R1 comparator preserved.
Machine: `w34-r2-mechanical-postprepare-comparison.json` (full per-file hashes/diffs).

## 1. Refs

Runtime `.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work`, cc1c/parent e84.

- OLD CP `0979f9f7703a25c2bd3424824bc4ad9f8719e8e7bcc49c19c5573d0f70ab593a`/4549, State `d7acd29b…`/4087 EVIDENCE_REVIEWED, `evidence-accepted.json` `edf21e4de5f7ab8db2d…`/126592, `edition-views-accepted.json` `3777133c…`/159498, ledger `f089cc4e…`/186202, completeness `e8c432dd…`/71532.
- NEW R2 manifest `sources/2026-W34/research/v2/acceptance-revisions/w34-repaired-20261112-r2/revision-manifest.json` `867eba96242eab0cf3e34277048e8497952c804f0805b4d09feacdb51b392a7b`/438583. Request `research/v2/acceptance-revision-inputs/w34-repaired-20261112-r2.json` `bb6042c67c4d2c2c81a857a5a26a211f33a181cd913a53c5894dcab8a6bf5ea6`/1654899 order-preserving `core.json_bytes`, 409 records (405+4). Supplement `ce6f977a…`/389414 explicit.
- R1 inert preserved: manifest `54de43ed…`/438583, request `057e186f…`/1434802, 4 Raw unchanged, never re-copied. Source 773 `a7e40c…` drift-checked pre-write, `files773` unchanged post. SP State `180db8c3…` untouched. Guard absent, 7 slots absent.

Root §§8–9 + R2 execution `prepare-normal-high-r6-W34-20261114T002948Z` exit 0 read.

## 2. Strict comparison (no per-field ignored mechanical)

| artifact | total | byte_equal | parsed_equal | unaffected exact | affected |
|---|---|---|---|---|---|
| cards `results/task-*.json` | 409 | 405 | 405 | 405/405 byte+parsed | 4 differ |
| views `views/view-*.json` | 409 | 405 | 405 | 405/405 byte+parsed | 4 differ |
| tasks `tasks/task-*.json` | 409 | 409 | 409 | 409/409 | — (4 affected tasks identical) |
| ledger rows | 439 | — (file 186202→186214) | 435 | 435/435 parsed | 4 differ |

Filenames identical OLD vs R2 (409/409 each).

Cards unaffected 405: byte `==` AND parsed `==`, exact bytes, no ignored fields. Entity order preserved original `entity_id,canonical_name,entity_type,organization,canonical_url` 409/409, top order identical. No 252-byte reorder drift as in R1.

Cards affected 4 (`task-ef1d67ce…/15127`, `task-4fe332e9…/16096`, `task-56725e60…/18389`, `task-f49a436a…/21100`): entity/top order preserved original; diff only `claims` (Q1 literal spans + §§ contexts), `limitations` 2→3, `verification.targets[].finding` (body refs). No mechanical order diff.

Views unaffected 405: byte `==` AND parsed `==`. `evidence_sha256` identical (card bytes identical, e.g. `view-0129…` 844B file sha preserved, `evidence_sha 4ac632…` preserved, materiality `CONTEXT` rationale identical). Top order identical.

Views affected 4: exact `['evidence_sha256','materiality','profile_annotations']`. `evidence_sha` = new card sha (correct derivation); `materiality.status CONTEXT→MATERIAL` + box/sidebar rationale (P2/P1/P4/P2); `profile_annotations.why_this_issue` same rationale; `window_relation MAIN_EVENT`, `carry_over false`, `scope_dimensions` preserved.

Tasks 409/409 byte+parsed identical (including 4 affected task files; correction lives in request records).

Ledger 435/435 unaffected parsed-identical, incl 4 `DUPLICATE/DROP` (`c042/c067/c069/c070`) + 354 `CONTEXT`, 26 `EXCLUDED`, 10 `HOLD`. Affected 4 exact 3 fields: `downstream_disposition CONTEXT→MATERIAL`, `evidence_view_statuses [CONTEXT]→[MATERIAL]`, `rationale …CONTEXT→…MATERIAL` (`KEEP/INSPECT` preserved). File +12B (7→8 chars ×3×4) `f089…`→`066230f4…`. R1 ledger `523df6…` vs R2 `066230…` differ only in `basis.{evidence_acceptance_sha,edition_views_acceptance_sha,evidence_set_sha,edition_view_set_sha}` (R1 drift digests vs R2 exact-preservation digests); row diffs beyond basis are the same 4 promotions. R1 files preserved, not basis.

Completeness: overall `LIMITED`, `closure null`, residual identical (5 bullets incl Sol-review caveat), 3 obligations content-identical by ID (`current-relevance`, `technical-significance`, `carry-over`), order rotated only, `basis.production_profile_sha 2a8c3089…` preserved, `basis.materiality_ledger_sha f089…→066230…` (R2 ledger). Bytes 71532 same length, hash old `e8c432…` vs new `d869027a…`. Body rationale genuine, not false.

Request order-preserving: `bb604…`/1654899. All 409 `records[].entity` order `==` base `interactive-evidence.json` (0 mismatches); record keys preserve base original (`discovery_id,status,entity,artifact_type,claims,limitations,verification,materiality,materiality_rationale,scope_dimensions,window_relation,carry_over,source_bindings`); sample `rec0` identical. No `sort_keys` alphabetization.

Raw 4 byte-identical to captured originals: `85c70376…`/314048, `a4c2aafe…`/414077, `da737a85…`/711224, `56b48291…`/388712 (4/4 match, reuse, never re-copied).

## 3. Verdict

`PASS — exact preservation for all unaffected; no remaining mechanical issue.`

- 405 cards byte+parsed exact, 405 views byte+parsed exact, 409 tasks byte+parsed exact, 435 ledger rows parsed exact.
- Affected 4 only expected `claims/materiality` (+`limitations/verification/ledger rationale/view sha` derivation), no mechanical order drift.
- No per-field ignored mechanical; strict equality holds.
- Prior R1 comparator `w34-mechanical-postprepare-comparison.json` preserved.

Not approval: no semantic/Human/State/adopt approval; independent content/Selection review still required. Stop at Human Commit Point.
