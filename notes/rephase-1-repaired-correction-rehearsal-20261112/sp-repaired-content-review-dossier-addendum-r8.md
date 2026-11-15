# SP r8 dossier addendum — closure shape correction (DATA only, no active write)

Role: DATA author, offline read-only. No source/state/runtime/import/test/network/Git/Production/subagents. No python imports (Read + sha256sum + jq + grep only). Epoch correct `cc1c7fd1cf979e71fda4ae2164828b37bc1b2325` parent e84. R3–R7 + all raw preserved as history; this r8 corrects ONLY the closure shape below. No shared README/ROOT edits.

## 1. Correction (what was wrong, what r8 does)

Previous r5 (and r6/r7 reviews/dossiers referencing it) treated the ordinary interactive 3-field closure `{targeted_gap_fill_completed, limitations[5], status}` as DM022 request-valid. It is not: `schemas/dm022-revision-request-v2.schema.json` `completeness.closure` is `$ref: closureOrNull` (lines 39-48, 246-265), which is `oneOf: [null, closureFULL]` where closureFULL requires 8 fields (`expansion_passes, final_pass_new_sources, final_pass_new_material_obligations, final_pass_new_material_obligations_open, targeted_gap_fill_completed, open_material_obligations, limitations, status`). The SP r6 dispatch correctly schema-refused BEFORE request/R (after 4 Raw + new Supp staged, zero SP writes) — old wrong review statements claiming closure-3 validity are preserved in place, corrected here, not silently edited.

R8 (`sp-repaired-completeness-request-r8.json` 33895B `6929d9ca…`, request shape keys ONLY `obligations/residual_limitations/closure`): keeps r5's approved 15×7 obligations byte-identical (O10 archive-aware LIMITATION, hash `bb7165cd…` unchanged) and residual 5 unchanged (`97469688…`), and replaces closure with the factual 8-field FULL copied verbatim from accepted result `profile-completeness-v2.json` 33683B `d67f7f83…` (closure hash `629c43d9…` identical on both sides). No new Human question, no source fix, no counter invention, no autoSAT.

## 2. Actual 8-field source pins (accepted result d67f, same Discovery/Screening unchanged)

- `expansion_passes: 3`, `final_pass_new_sources: 4`, `final_pass_new_material_obligations: 8`, `final_pass_new_material_obligations_open: 0`, `targeted_gap_fill_completed: true`, `open_material_obligations: 0`, `limitations: [5 same strings as interactive residual/closure]`, `status: LIMITED`.
- Field provenance: these are the accepted result's recorded expansion counters/status/limitations (same Discovery `7074cef2…` / Screening `6ff524b0…` as base; no new Discovery/Screening in this correction). Reused as factual baseline for the request because this correction proposes no new expansion passes (archive rebinding is replacement within the 30-entry supplement scope: 27 preserved + 3 replaced, taskbound 28 = 25 + 3; D142 no entry). Counters are NOT re-derived for the request and NOT zeroed; inventing `final_pass_new_sources: 0` would falsify history. If result-vs-request semantics differ, the exact before values are those above from `d67f…` (quoted verbatim); the request carries them unchanged as the factual baseline the correction builds on.
- W34 closure null unaffected (Weekly request permits null; separate edition, not touched by SP r8).

## 3. Preserved (unchanged in r8)

- 156 unaffected incl D165 (`d455f722…`, `16f046f5…`), 4 records r7 (`0a54004e…` 17947B: D142 key omitted not null, lineage CORE all 4, INFERENCE token + narrow summary-scope + HOLD ceiling, D141 rate qualifier, targets exact 2/1/2/2), full30 r4 (`e2bfb30a…` 31522B, FULL DID, canonical types, hex16 stable), staging r4 + routing r7 (FULL DID, clean pointers, D142 summary routing with tied `…18672662`), O10 archive-aware LIMITATION + residual 5 + relevance/ledger sentences (from r5, byte-identical in r8 obligations/residual).
- 5 staged SP files from the refused dispatch (4 Raw + new Supp) unchanged by this packet author (no restage/rewrite); r8 only replaces the un-staged request completeness DATA so a new dispatch can be built.

## 4. Status counts + new hashes

- 160 = 156 preserved + 4 replaced; 15 obligations (2 SAT O01/O07, 13 LIM incl O10); closure FULL 8-field (counters 3/4/8/0, true/0/LIMITED); residual 5; supplement 30 = 27 + 3; taskbound 28 = 25 + 3; D142 no supplement entry.
- r8 files: completeness-request `6929d9ca…` 33895B (3 keys only); assembly-r8 (this packet: update hash after write; points records-4-r7 `0a54004e…`, completeness-r8, full30-r4 `e2bfb30a…`); this addendum (hash after write). r5 `cc4ce34d…` + all r7 raw/records/routing/supplement preserved as history.
- No validator executed, no imports, no runtime/tests/Git/network/Production/subagents. No acceptance/decision/semantic PASS. Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN. Stop at Human Commit Point.
