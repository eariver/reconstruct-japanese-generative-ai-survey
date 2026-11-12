# Supplement-carry corrected-v2 — independent source/test-evidence review

Role: NEW independent implementation/source+test-evidence reviewer (v2 followup, not author/map reviewer, not Astra/root, not implementer, not Human).
Date: 2026-11-07.
Method: read-only file/text reads + Python hashlib/pathlib hash/parse only. No `git` binary, no reconstruct readback, no repo-script imports, no test/runtime execution, no network/Production/subagents, no source/State writes except this NEW pair. Preserves `initial-…` + `corrected-…` reviews/machines.

Read scope (FULL unless noted):
- `astra-implementation-resolution.md` FULL incl §6 (views + factory + fixture + bound control)
- `implementation-20261106T131722Z/corrected-return-v2.md` FULL, `corrected-implementation-v2.diff` FULL (612 lines), `corrected-batch-v2-raw.txt` FULL, `baseline-control-original-final139-raw.txt` FULL, preserved `corrected-return.md`/`corrected-batch-raw.txt`/`baseline-control-raw.txt`/`initial-…` as history
- Actual workcopy: `scripts/survey_research_authority_v2.py` v2 (`d50282…`), `scripts/survey_prearchitecture_acceptance_v2.py` (`f312f0…` unchanged since prior correction), `tests/test_dm022_supplement_carry_v2.py` v2 (`e3041b…`/`5d5d3a…`, 861 lines), `scripts/survey_evidence_v2.py` unmodified reference (resolve/recheck/finish, `_safe_read_bytes` O_NOFOLLOW, `view_filename`, views builder `2389/2395/2408`)
- Identity only: `.git/HEAD`, `.git/refs/heads/main`, `.git/config`, file/inode counts + final139 manifest comparison via Python (no git)

## 1. Verdict

**SCOPED_CODE_READY (bounded selected repair only).**

V2 closes the prior CHANGES_REQUIRED: unaffected-views proof seam, canonical empty-context factory, ALL-field fixture preservation with cards/views/ledger asserts, view-only real proof/adopt negative, and bound original-final139 red control. No new schema/module/family/cache/public-dict/CLI change, no LOW LIVE, no future pins, no history relaxation, no affected-views semantic overreach.

Not full PASS, not R4 audit, not semantic/Human approval. Remaining blockers in §9 (targeted regressions, no-supp compat, CURRENT proof, exact delivery, full 401/28 scale) are explicitly deferred, not hidden. Do not sum 4+10+14 counts or claim real W34/SP 409/160 coverage.

## 2. Source identity — meaningfully scoped, proof untouched

- Workcopy HEAD `ref: refs/heads/main` → `5eef790bd8d492c557cc4db9c29425e3e410d47d` (same isolated root, no amend/replace per `corrected-return-v2.md`). New root, NOT actual409 ancestry, not shipping candidate. Inert origin, no alternates/shallow, process-scoped identity. No ordinary candidate/reconstruct commit.
- Hashes (Python SHA256): LOW `d50282bf0812a4d07e3da13cf3574961add0466cd27a3ef3c648b89fe40330dd` (239978B), HIGH `f312f02e2dc5c1aa5a1d6432bca134cd83f0a1edea2d127721d0206d05514a90` (97844B, unchanged), test `5d5d3aadec70bc5d5c22fdec3e3c65d4f38d73aa995d326d8927fb8f73e26f00` (60569B, 14 tests). Match return doc + v2 raw header.
- File set: 0 missing vs manifest, 769 unmodified SHA match, 2 modified as above +1 new test. Proof `0974c709…`/`388c899…` still match manifest — old proof untouched. Tree not recomputed (no git per bounds); byte comparison is the evidence.

## 3. Actual OLD/NEW unaffected Views — pinned, unaffected-only, no history relaxation

Verified in corrected LOW `prove_revision_from_paths` (v2 diff §§577-609 + surrounding §§3442-3532):
- OLD 4 via `manifest.before_checkpoint.evidence` → `_repo_rel` + SHA vs `before_cp_ref.sha256` (3444-3447) → typed record → `old_by_name` artifacts → each OLD acceptance `_repo_rel` + SHA vs `ref.sha256` (3462-3466). NEW 4 via `manifest.candidate_outputs` `SizedRef` + `_verify_sized_ref_bytes` (SHA + `byte_count>=1`, repo-local via `_repo_rel` → `repo_local_path`, `O_NOFOLLOW` safe read) (3470-3474, 3508-3509). NEW per-file `tasks/cards/views` also `SizedRef` + bytes verified, empty arrays refused (3526-3532). Request itself pinned via manifest `request` SizedRef + schema + identity + profile/discovery/screening SizedRefs (3483-3495).
- Views dirs: `old_vw_acc_path.parent/"views"` from verified OLD acceptance ref, `new_vw_acc_path.parent/"views"` from verified NEW acceptance ref (581-588). View files `view_filename(task_id)` read via `_safe_read_bytes` (O_NOFOLLOW, lstat regular-file, FD/inode match) + `_strict_parse_object` (no lenient parse). NEW views additionally bound by manifest `candidate_outputs.views` SizedRefs; OLD views bound by verified OLD acceptance + sibling layout (no standing LIVE/history bypass, no E-as-R — `_old_ctx` from manifest request + retained COPY, `_prove_request_abs` + `before_copy_path`, §§3503-3506).
- Comparison is unaffected-only: for `did in affected`, only `old_view_raw == new_view_raw` refuses (must carry new evidence, bytes-level, no semantic-difference requirement). For unaffected, `old_view_doc != new_view_doc` refuses + `old_view_raw != new_view_raw` refuses (no ignored `materiality`/`profile_annotations`, no digest-only permission). `view_set_sha256` remains allowed mechanical propagation at field level, not blanket view permission. No broader schema/history redesign; contradiction returns case (refusal, no silent weakening) per root §6.
- Alias/symlink + current/history safety: every input via `_repo_rel` (rejects `\`, absolute, `..`), `repo_local_path` containment, `_safe_read_bytes` `O_NOFOLLOW`, `_assert_pin_repo_ancestors` per-component NoFollow, `_recheck_phase_pins` SHA/len + `is_symlink` refusal. Package path pins request/COPY + OLD checkpoint/package + profile/discovery/screening + prompt/3 contracts (+ supplement schema when supplemented) BEFORE DS derivation, `_finish_authority_phase` (recheck supp + recheck pins + owner revalidate fields/files + recheck, no reseal). DS via `derive_ordinary_root_effective_context` (COPY, never `derive_current_*`/LIVE). Full Raw closure via helper `_resolve` (manifest/basis/ALL Raw pins, `len(raw_refs)==len(entries)`, `_recheck_supplement_context` before return). Covers all r2 sites: missing/drift/symlink/traversal/cross-source_root, wrong/DROP/unknown/duplicate/unbound, IDs/contract-without-manifest, OLD+null, plus late request/COPY/basis/supplement-manifest drifts exercised as failing tests (v2 raw 8-18).

## 4. Canonical no-supp factory — PASS

Null case now `evidence_mod._resolve_phase_supplement_context(repo_root, {}, implementation_sha=None, screening_acceptance=None, discoveries=None)` (v2 diff §§158-164) yielding exact `MappingProxyType` empties, not the prior guessed mutable `empty_ctx` dict with hand-written keys. Preserves no-supp operation/history; `_finish` with `manifest_ref None` is early-return no-op. No third shape, no public dict, no cache.

## 5. Fixture ALL-field preservation + cards/views/ledger asserts — PASS

- `_build_request(..., prior_records_by_did)` deepcopies the entire prior record for unaffected DIDs (187-199), rebinding only `source_bindings` to current `sid_by_did` (same IDs by design) and defensively dropping stray bindings for Discovery-only. Covers `materiality_rationale` + view-bearing `window_relation/lineage_role/branch_ids/transition_ids/inheritance_note/historical_attribution_caveat` + claims/limitations/verification/scope, not just claim text. Replaced/novel rev2 tests pass `prior_records = {load(req1)["records"]}` for unaffected (585-586/613-614/749-754), so unaffected cards/views/ledger are byte-identical by construction.
- `_assert_full_unaffected` asserts nonempty unaffected, task identity + Discovery→task map identical, unaffected cards byte-identical AND unaffected views byte-identical (512-514), ledger rows identical for unaffected, `rows_checked == len(tasks)+len(ledger rows)`, mechanical allowlist exactly r2 9 fields. Both routes: weekly DERIVED + thematic direct, novel→unchanged and replaced (same + replaced Raw, `sid_a == sid_b`, distinct `raw/auth-<did>-r2.html`, no invalidation of A). 3 tasks (affected supp + unaffected supp + Discovery-only), 2 nonempty unaffected.
- History semantics preserved: no stripping/normalizing of `source_bindings`/envelope to force pass; unbound `supplement-src-*` still refuses at card build (red control).

## 6. View-only negative — real proof/adopt, State/guard preserved — PASS

`test_unaffected_view_field_only_change_refuses_prove_adopt` mutates only `materiality_rationale` for `beta-source` (unaffected), asserts cards stay identical (rationale not in cards), then `high.adopt_revision` (which calls `prove`) refuses `unaffected Discovery beta-source view semantic drift`, State bytes equal + guard absent. Real HIGH path, not patched validator; inert R partials allowed (candidate files remain, no State/guard writes, no cleanup). Proves the new seam is load-bearing, not decorative.

## 7. Bound original-final139 control — PASS (as red control, not coverage)

`baseline-control-original-final139-raw.txt`: ARGV/ENV/PID/START/END + `SOURCE_ROOT` = proof-copy, `SOURCE_SHA256_LOW 0974c709…`, `HIGH 388c899…`, `TEST_SHA256 5d5d3a…`, `LOADED_MODULES` 3 files, 1 test exit 1. Traceback paths are proof-copy (not workcopy imports), normal `high.prepare_revision:651 → build_revision_cards_views_from_paths → _build_card_core:2247` failure `source_bindings must explicitly select task-bound sources` (card build, not token). Selected thematic novel positive fails on original producer, passes on corrected workcopy (v2 raw 26-27). Prior workcopy-checkout `baseline-control-raw.txt` preserved as historical observation. Limit: single-positive control only; not a full-suite original run.

## 8. Late/input drifts — PASS as failing tests (code covers more than exercised)

V2 raw 8-18: late request (HIGH late recheck), late Raw/COPY/basis/supplement-manifest (LOW pin/supplement recheck, seam fault calling original then mutating, no stub positive), plus decoys (unrelated-file at prepare with State/guard checks; manifest-swap at prove with rebound decision so triangle is what refuses) and null/unknown + red control. Code pins cover OLD checkpoint/package + profile/discovery/screening + prompt/contracts in addition to exercised request/Raw/COPY/basis/manifest drifts; unexercised combinations remain in §9, not claimed.

## 9. Remaining blockers (no broad decorations)

- Targeted regressions (`test-oracle-inventory.md` §9), no-supp compat (`:615`/`:486` + C direct), fresh `verify_renewal_source_proof` CURRENT via API with new pins/`expected_head/tree`, exact complete DIRECT409 delivery with apply-check. No PDF/R4/general suite.
- Full-scale 27+3 / 401 patterns need real-material rehearsal + separate semantic review (current replaced is 1 replaced + 1 same + 1 Discovery-only per route). If valid history contradicts exact unaffected-views equality in real 409/160, return concrete case before altering history rules (root §6).
- Raws bind argv/env/PID/source-hashes/loaded-modules/timing/exit + unittest stdout/stderr; source hashes live in raw header (v2) + return doc; no per-test source header; no proof/report/checkpoint bytes in raw (only asserts). Fixture Git commits are test DATA. Whole NOT_READY/DM021+022OPEN/audit unstarted/quality/adoption/savings OPEN. Ordinary Commit/Push Human-owned.
