# SP correction final addendum r8 — DM022 closure shape (preserves priors, qualifies prior error)

Reviewer: NEW independent content reviewer (same as r4/r5/r6/r7 reviews, all preserved, NOT rewritten).
Scope: r8 closure-shape DATA only. No source/state write, no HIGH prepare/adopt/resume/readback, no Selection/Architecture, no R4/Draft/PDF/Human Gate, no synthetic decision/approval.
Method: Read + stdlib hash/compare only (Read, sha256sum, python stdlib json/hashlib). DM022 + result schemas read as DATA (never imported/executed). No project imports/runtime/tests/Git binary/network/Production/subagents. No reconstruct readback. cc1c/e84/P2 read as DATA only.

## 1. Prior error qualified (explicit)

Prior r5 addendum + r6/r7 reviews PASSED `sp-repaired-completeness-request-r5.json` closure 3-field `{targeted_gap_fill_completed, limitations[5], status}` as `request shape (not wrapper)` valid. That PASS was for ordinary interactive completeness shape only — INCORRECT for DM022 revision-request input.
Actual `schemas/dm022-revision-request-v2.schema.json` `completeness.closure` is `$ref: closureOrNull` (lines 39-48, 246-265): `oneOf [null, closureFULL]` where FULL requires 8 fields (`expansion_passes, final_pass_new_sources, final_pass_new_material_obligations, final_pass_new_material_obligations_open, targeted_gap_fill_completed, open_material_obligations, limitations, status`). Actual SP dispatch `prepare-normal-high-r6-SP-20261114T003738Z` correctly schema-refused AFTER 4 Raw + supp build/validate, BEFORE request/R: `SchemaConformanceError: … $.completeness.closure: {3-field…} is not valid under any of the given schemas` at `gate.validate_instance` (exit 2, zero SP request/R writes, 4 Raw + new Supp partials preserved). Old wrong PASS statements are preserved in place, qualified here, not silently edited.

## 2. r8 correction (factual, no invention)

- `sp-repaired-completeness-request-r8.json` 33895B `6929d9ca219f91b70bd3de698359b9148621a26333b8d0c0d064be17e4e688b6`, keys ONLY `obligations/residual_limitations/closure` (request shape, no `overall_status/basis` wrapper).
- 15 obligations 7-field each byte-identical to r5 approved (O10 archive-aware LIMITATION `vendor-historical BOUND u1/u2/u3 Sept20/21 CDX MATCH + D142 unfetched + RLCD + indep gap + vLLM/Dynamo current-only true + 1.14 drift note`, O01/O07 SAT rest LIM). Residual 5 byte-identical to r5/profile/interactive.
- Closure replaced with factual 8-field FULL copied verbatim from accepted result `profile-completeness-v2.json` 33683B `d67f7f8363407b30d58dbe2dbe562b3666ea9483f9f16303859cfe459ab5e805`: `expansion_passes 3, final_pass_new_sources 4, final_pass_new_material_obligations 8, final_pass_new_material_obligations_open 0, targeted_gap_fill_completed true, open_material_obligations 0, limitations[5 same strings], status LIMITED` (closure hash `629c43d9…` identical both sides per dossier). No new Human question, no source fix, no counter invention, no autoSAT, no zeroing (inventing `0` would falsify history).
- Field provenance: counters/status/limitations are the accepted result's recorded expansion baseline (same Discovery `7074cef2…` / Screening `6ff524b0…` as base; no new Discovery/Screening in this correction; archive rebinding is replacement within 30-entry supplement scope 27+3, taskbound 28=25+3, D142 no entry). Reused as factual baseline because correction proposes no new expansion passes. W34 closure null unaffected (Weekly permits null, separate edition).
- r8 dossier addendum + assembly r8 confirm: r5 `cc4ce34d` preserved as history (O10/residual/obligations correct, closure superseded for prepare); r7 records/routing/staging/supplement unchanged.

## 3. r7 + reused pins still valid (unchanged)

- records-4-r7 17947B `0a54004eefe12b5412ebca733826f4401c5dfcb8ac644f32111e2d547785cb06` (D142 key omitted not null, lineage CORE all4, INFERENCE token + summary-scope + HOLD, D141 rate qualifier, targets 2/1/2/2), routing-r7 4061B `af4e043c…` (correct `…18672662`), staging-r7 2644B `b7fac760…`, full30 r4 31522B `e2bfb30a…`, 156 `d455f722…` + D165 `16f046f5…`, base 697a/ffcd/Evidence/Views/Ledger/Completeness/S142 `f7eeec68…18672662`/u1/u2/u3 (per r7 review, re-verified via assembly). Assembly r8 3971B `5985c99e…` points r7 + r8 + r4 with explicit `closure is 8-field FULL … NOT 3-field, NOT null`.
- Actual schema/source checked: `dm022-revision-request-v2` `closureOrNull` 8-field vs null; `profile-completeness-result` `fullObligation` 7-field; `run_evidence_v2_interactive` record keys (prior r6); interactive 3-field closure (ordinary shape) vs result 8-field closure (DM022 shape) distinguished — not assumed same.

## 4. Verdict

Closure-shape blocker CLOSED with factual verbatim copy (no invention). All other r7-approved content preserved.

**Final PROPOSAL_READY for DM022 input ONLY** (r8 completeness `6929d9ca` + r7 records `0a54004e` + routing `af4e043c` + staging `b7fac760` + full30 `e2bfb30a` on cc1c exact773). Actual external Decision requires after graph: HIGH prepare with HEAD/tree/tool pins → proof/adopt/resume/readback → independent re-review → root dispatch → Selection/Architecture. No synthetic approval, no semantic PASS, no acceptance. DATA only. Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN. Stop at Human Commit Point.

## 5. Read scope

r8 completeness/assembly/dossier-addendum; r6 SP dispatch execution report (schema-refused closure3, 4 Raw+supp staged, zero request/R); DM022 request schema (`closureOrNull` 8-field) + result schema (`fullObligation` 7-field) + runner contract (prior); accepted result `d67f` closure/obligations/residual + interactive closure (3-field ordinary) + Discovery/SCP pins; r7 records/routing/staging + prior reviews (preserved). No validator, no imports, no Git/network/Production.
