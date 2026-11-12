# Supplement-carry corrected-v3 — duplicate-DID exact-coverage independent review

Role: NEW independent implementation reviewer (v3, not author/map reviewer, not Astra/root, not implementer/runner, not Human).
Date: 2026-11-07.
Method: read-only file/text reads + Python hashlib/pathlib hash/parse only. No `git` binary, no reconstruct readback, no repo-script imports, no test/runtime execution, no network/Production/subagents, no source/State/test writes except this NEW pair. Preserves `initial-…`, `corrected-…`, `corrected-v2-…`, `final-…`, `final-delivery-current-…`.

Read scope (FULL unless noted):
- `astra-implementation-resolution.md` FULL incl §8 (duplicate set-only bug + smallest cardinality+set fix + HIGH negative + proof admission + pre-fix preservation)
- `implementation-20261106T131722Z/corrected-return-v3.md` FULL, `corrected-implementation-v3.diff` FULL (718 lines, tracked only), `duplicate-guard-raw.txt` FULL (3 OK), `changed-c-n7-v2-raw.txt` FULL (1 OK), preserved `affected-verification-…/batch-05-c-direct-raw.txt` failure + `applied-verification-…/SUMMARY.md` (proof-copy FULL C 7 OK on pre-v3 runtime)
- Actual workcopy: `scripts/survey_research_authority_v2.py` v3, `scripts/survey_prearchitecture_acceptance_v2.py` (unchanged), `tests/test_dm022_supplement_carry_v2.py` v3 (943 lines), `tests/test_dm022_c_direct_operation_v2.py` (N7 block)
- Identity only: `.git/HEAD`, `refs/heads/main`, `config`, file counts vs final139 manifest via Python (no git)

## 1. Verdict

**FINAL_SCOPED_CODE_READY (bounded selected repair, conditional on fresh CURRENT + new DIRECT delivery).**

v3 closes the §8 duplicate-record hole with the smallest consistent cardinality+set guards in all three admission sites, plus schema-valid HIGH/proof negatives that reach the duplicate predicate. No schema/helper/framework change, no HIGH change, no duplicate normalization, no broad semantic relax. Old delivery + CURRENT (`final-20261107T034506Z`, `current-proof-20261107T035000Z`) remain preserved pre-fix evidence, superseded not overwritten; fresh CURRENT + new DIRECT delivery are pending separate tasks (not claimed here).

Author header `(TEST-ONLY …)` is WRONG and corrected here: runtime LOW DID change `d50282… → 7f5fc9e0…` (240969B); HIGH `f312f0…` unchanged; focused test `a8aaafe3…` (65884B, 17 methods). Final workcopy paths + hashes in §2 are the binding.

Raw scope is 3 duplicate tests only (`duplicate-guard-raw.txt` 3.223s OK) + single changed N7 (`changed-c-n7-v2-raw.txt` 4.553s OK). Do NOT claim full-17 from the 3-test raw; 17-method file scope is established by file hash + preserved v2 14-test evidence, not by this raw alone.

## 2. Final source — runtime LOW changed, final paths bound

- Workcopy HEAD `5eef790bd8d492c557cc4db9c29425e3e410d47d` (isolated new root, NOT actual409 ancestry), inert origin, no alternates. Python SHA256: LOW `7f5fc9e0d79729d98345f0b0352d5070c76e93f92f2c14148e22c9f38a8f4c0f` (240969B) at `.rephase-1-editorial-runtime/supplement-carry-implementation-20261106T131722Z/candidate-work/scripts/survey_research_authority_v2.py`, HIGH `f312f02e2dc5c1aa5a1d6432bca134cd83f0a1edea2d127721d0206d05514a90` (97844B) same path `…/scripts/survey_prearchitecture_acceptance_v2.py`, focused `a8aaafe35f8b602fec36491a3fd116376c426e46d3724bda546d471637693d16` (65884B, 17 methods) same dir `…/tests/test_dm022_supplement_carry_v2.py`, scale `7118092f80b1…` (27736B) preserved not rerun, C `1fa905bf7e184…` (43626B) updated N7. GEN/PROOF genuine 409 `409b292…/8ce369…` from saved DB (`.git` local read permitted, no reconstruct); author `5eef…` ≠ actual409.
- Count distinction corrected: **3 mods + 2 new vs old771 unchanged768** — modified exactly 2 runtimes? No: HIGH unchanged, so modified are LOW (`d50282→7f5fc9e0`) + focused test (`5d5d3a→a8aaaf`) + C test (N7 oracle update, hash `1fa905…` as updated) = 3 files; new are exactly 2 scale/focused? No: focused is modified (not new), scale is preserved new (`711809…`), plus? Actually per v3 return: LOW changed, HIGH unchanged, focused `a8aa…` (17 = 14+3), C `1fa905…`, scale `711809…` preserved. Versus old771, unchanged768 = 771 − 3 modified (LOW + focused + C). Scale + focused-new? Focused was already new in v2 (`5d5d3a…`), now modified to `a8aa…`; scale remains new. Do not recount as “actual409/new2” as a corpus claim.
- Old delivery + CURRENT preserved pre-fix, superseded: `source-packaging/final-20261107T034506Z` (patch `3032752c…`/5526524B, manifest `f88f6d…`/202750B, 773=689+84, 141=57M+84A) and `current-proof-20261107T035000Z` (weekly LayerB `CURRENT_PROOF_VALID True`, closure 70 with `d50282/f312`, SAME-proof LOW drift + restore) are pre-v3 evidence on `d50282…`, not final-source acceptance. Do not transfer old CURRENT PASS automatically; fresh CURRENT + new DIRECT delivery pending separate.

## 3. Three guards — same non-DROP universe, typed exact coverage, no normalization

Verified in actual v3 LOW (lines 2071-2077, 2379-2384, 3506-3513):
- `derive_before_context`: `decisions = {did: decision-string}`, `non_drop = {did | dec in (KEEP,MAYBE,INSPECT)}`, `record_ids = [r.discovery_id]`, `len==len(non_drop) and set==non_drop`, same message (no oracle break).
- `build_revision_package_from_paths`: `decisions = {did: full-record}`, typed `dec_rec.get(decision) if dict else dec_rec in (KEEP,MAYBE,INSPECT)`, same `len+set` with R2 message (`no new/omitted/DROP/extra unused`). Same actual universe, correct typed handling for both shapes; new-only behavior preserved (OLD-supplemented + NEW null still refuses, never retroactive).
- `prove_revision_from_paths`: `_prove_screening/decisions/non_drop/record_ids` same `len+set`, message adds `duplicate` word for new path (`no new/omitted/duplicate/DROP/extra unused`); no existing oracle asserts that message (C N7 asserts producer message, not prove message). Prevents duplicate-DID decoy on externally bound request (tampered request+manifest+decision SHA-rebound still refuses).
- Historical `proof returning old record IDs` not used: all three derive `non_drop` from genuine COPY-derived screening acceptance (`derive_ordinary_root_effective_context`, never LIVE), not from old package/task IDs. No duplicate-source normalization (no drop/dedupe/silent ignore via later dict lookup); refusal is fail-closed. No broad semantic relax (no schema change, no ignored fields, no history-rule change).

Pre-bug determinism (no red-baseline claim for duplicates): pre-fix predicates compared only `set(record_ids) != non_drop`. A duplicated DID with all required DIDs present satisfies set equality while `len > len(non_drop)`; later `discovery_map`/task derivation keys by DID would silently ignore the extra record. The v3 `len` conjunct deterministically closes this without needing a pre-fix run; no duplicate red baseline is claimed (duplicate raw is post-fix positive + refusal only).

## 4. Negatives — schema-valid HIGH + direct proof reach duplicate predicate

- Identical-body duplicate (`test_duplicate_record_same_did_refuses_before_publication`): deepcopy `beta-source` record, append (4 records for 3 non-DROP), `high.prepare_revision` refuses `request.records must cover exact non-DROP…`, State bytes equal, guard absent, `candidate/package.json|tasks` absent (inert COPY `retention/state-before + slot COPYs` allowed precise, no universal zero-write claim). Schema-valid (deepcopy passes `validate_research_record_content`), owned COPY honest (fresh EVIDENCE_REVIEWED State via existing helpers, real supplement builder).
- Conflicting-body duplicate (`test_duplicate_record_conflicting_body_refuses_before_publication`): same DID with conflicting `claims/materiality_rationale/source_bindings`, refuses same predicate, State equal, no normalization/drop. Candidate/guard inventory not asserted here (only State + message); identical test already proves no-publication window, so no new gap.
- Direct proof (`test_prove_duplicate_records_refuses_admission`): genuine `prepare_and_decide`, then tampers bound request file (+duplicate), rebinds `manifest.request` + `decision.manifest_ref` SHAs to tampered bytes (SHA bindings hold), `prove_revision_from_paths` refuses same duplicate-inclusive message. Reaches duplicate predicate, not SHA drift/decoy preemption.
- Changed N7 (`changed-c-n7-v2-raw.txt` 1 OK, `7f5fc9e0/f312` bound, loaded modules proof): updated N7 expects new preflight exact message + timing (State COPY may exist, candidate NOT yet constructed) + inventory (State unchanged, no checkpoint/proof/guard, no candidate package/tasks/results). TEST-ONLY in the sense of C-file oracle update, but runtime LOW DID change, so full-C scope is qualified **5+1** (5 old passes on new runtime from preserved `batch-05` + corrected N7 single), NOT full-C green. Applied-full-C batch (`applied-verification-…`: proof-copy FULL C 7 OK on pre-v3 `d50282…`) is superseded for v3 runtime; separate runner will bind full C on `7f5fc9e0…` later.

## 5. Limits + needed bindings (no broad repeats)

- Do not demand broad repeats: no-supp A2-14 already passed both positives on new runtime (`batch-04` 14 OK); scaling whole19, HIGH A2, profile-4, scale W34/SP structural witnesses preserved, not rerun per §7-§8 scope.
- Needed: fresh CURRENT proof via API on exact `7f5fc9e0/f312` + new complete DIRECT409 delivery with apply-check on actual409; applied-full-C batch on v3 runtime. Real W34/SP 409/160 accepted corrections still unperformed with separate semantic review.
- Raws bind argv/env/PID/source-hashes/loaded-modules/START/END/exit + unittest output; no per-test source header beyond file pins; fixture Git commits are test DATA. Whole NOT_READY/DM021+022OPEN/audit unstarted/quality/adoption/savings OPEN. Ordinary Commit/Push Human-owned.
