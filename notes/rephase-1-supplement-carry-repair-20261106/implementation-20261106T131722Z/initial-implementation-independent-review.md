# Supplement-carry initial implementation — independent source/test-evidence review

Role: NEW independent implementation/source+test-evidence reviewer, not author/map reviewer, not Astra/root, not implementer, not Human.
Date: 2026-11-06.
Method: read-only file/text reads + Python hashlib/pathlib hash/parse only. No `git` binary, no reconstruct Git readback, no imports of repo scripts, no test/runtime execution, no network/Production/subagents, no source edits except this NEW review + machine companion.

Read scope (FULL unless noted):
- `notes/rephase-1-supplement-carry-repair-20261106/README.md`
- `notes/rephase-1-supplement-carry-repair-20261106/astra-implementation-resolution.md` FULL (§§1-4)
- `notes/rephase-1-supplement-carry-repair-20261106/integration-map-r2.md` FULL (§§1-7)
- `notes/rephase-1-supplement-carry-repair-20261106/integration-map-r2-review.md` FULL (§§1-3, incl §2.8 clarification)
- `notes/rephase-1-supplement-carry-repair-20261106/integration-map-independent-review.md` §§1/3 (10 corrections) + `test-oracle-inventory.md` §§3-10 (as DATA)
- `implementation-20261106T131722Z/README.md` FULL, `initial-implementation.diff` FULL (366 lines), `focused-test-raw.txt` FULL
- Actual workcopy source: `candidate-work/scripts/survey_research_authority_v2.py` (helper + package + prove seams, via diff + targeted reads), `candidate-work/scripts/survey_prearchitecture_acceptance_v2.py` (HIGH seams), `candidate-work/scripts/survey_evidence_v2.py` §§232-451/523-635 (pin/resolve/recheck/finish + validator, unmodified reference)
- Actual new tests: `candidate-work/tests/test_dm022_supplement_carry_v2.py` FULL (463 lines)
- Identity only: `candidate-work/.git/HEAD`, `.git/refs/heads/main`, `.git/config`, `.git/COMMIT_EDITMSG`, `.git/logs/HEAD`, `.git/logs/refs/heads/main`, `.git/refs` listing, file/inode counts + manifest comparison via Python (no git)

## 1. Verdict

**CHANGES_REQUIRED — code + tests not ready for packaging/CURRENT proof or real-material use.**

No broad recycle, no new schema/module/family/cache/public-dict/CLI-flag needed. Base identity is clean (see §2). HIGH/LOW seams match selected r2 surface and r2-review §2.8. Real HIGH positives, DERIVED, 3-task pattern, byte-identical unaffected, and genuine card-build red control are present. Failures are concrete map-vs-code/test gaps below, not style.

Do NOT package DIRECT409, run CURRENT proof, or start real W34/SP 409/160 correction until §4 code + §5 test corrections are implemented and re-reviewed. Root reviews the diff itself; this judges source/test evidence only.

## 2. Source identity — NO divergence, hash domains explained

- Workcopy HEAD: `ref: refs/heads/main` → `5eef790bd8d492c557cc4db9c29425e3e410d47d`. Logs: `0000… → 4d2829ff… → 5eef…` (initial + amend), message `isolated base: already-applied final139 771 files (patch de0af9cbd5 manifest c5a6b230); new isolated epoch, not shipping HEAD409 claim`. Parent: none (isolated root, not ordinary `409b292`). As selected (new independent DB, not shipping HEAD).
- Config: `origin https://invalid.invalid/inert.git`, `user supplement-carry-impl <…@invalid.invalid>`. No `objects/info/alternates`, no `shallow`, no `grafts`. Process-scoped fixture identity only; no `HOME`/gitconfig mutation evidence. No ordinary candidate/reconstruct commit.
- Author `base-staged e6c56ba3… / 37f22ab…` vs `shipping final139 0974c709… / 388c899…` is **same files, different hash domains**, not a divergence:
  - Proof LOW file SHA256 `0974c709b55365ef93cded5e97707e705b8a59aae01734e52c40e3b40c1a008b` (218692B) == manifest `files[scripts/survey_research_authority_v2.py]`; git blob SHA1 `e6c56ba3978f8323ab54b55e3986393f0ae9a077` == author base-staged. Verified via Python (header `blob <len>\0` + SHA1).
  - Proof HIGH file SHA256 `388c89941cef393868c9a2cef5ad7276889ffa01aeda294e756c9f76b6f9efd4` (92741B) == manifest; blob `37f22ab4c94ec5a75ea8f842ca8bb5efc5a82357` == author base-staged.
  - Work LOW SHA256 `30ac6432fc0c5423f7d406ba6167e20061d4d606014e76e5b980a8454f6f7aca` (232379B), blob `6d3754f983c4b3e324f7afb9ddb70807d15d0972`; work HIGH SHA256 `69032c5b16cda28f090ad8c386479f8a950f1a4ab392d68f85da720d2c267651` (95257B), blob `b95aa9c32460ae33e95774a9141901758d573696`. Match author `worktree 30ac… / 69032…`.
  - New test SHA256 `abf1c9e0c82e5657b423da4c74371de3812bbc2928148b19224e1b4362ea2db2` (32757B), blob `377c1a386d60e9601d1c123a2928dca83db0bc97`. Match author `abf1c9e…`.
- File set: manifest `intended_files 771`; workcopy has 0 missing, 769 unmodified SHAs match manifest, 2 modified differ as intended, +1 extra `tests/test_dm022_supplement_carry_v2.py` = 772 total excl `.git`. Inodes: work vs proof LOW differ (`24904331` vs `24656495`, `nlink 1`), `samefile False` — no hardlink sharing presumed. Tree `a851584…` not independently recomputed (no git run per bounds); file-byte comparison above is the identity evidence.
- Saved e84/proof not mutated by this unit: proof LOW/HIGH bytes still equal manifest SHAs above; workcopy is a copy with `.git` excluded then new DB. E84 instance not read here beyond prior DATA.

Author identity return is truthful; correct the record only to note blob-vs-file domains.

## 3. Code — largely selected surface, 2 required fixes

Keep (verified in diff + targeted source reads):
- Narrow private helper `_bind_selected_supplement_for_revision` in existing `survey_research_authority_v2.py` only. No new module/staticmethod/cache/public verified-dict/CLI flags. Signatures unchanged. `MappingProxyType` via `_resolve`, discarded at phase end (no global). Good.
- Effective DS: `screening_acceptance=ds.screening_acceptance` + `discoveries=ds.effective_records`, both non-None enforced, `implementation_sha=None`. Provisional package carries `issue_id=request.issue_id` + `basis.discovery/screening` from `request.discovery_ref/screening_ref`; `_resolve → validate` enforces issue/discovery-path/screening-path + unknown/DROP/identity/class/duplicate/Raw/symlink checks. `source_root` checked explicitly vs COPY-bound profile `source_root` (same predicate as `prepare_evidence_package:879-881`). No `None+None` fallback. Good.
- Record coverage: `affected_ids` nonempty unique, subset non-DROP + known DIDs, `record_ids == non_drop` (KEEP/MAYBE/INSPECT). Exact non-DROP reuse of `derive_before_context:2066-2076` logic. Good.
- OLD prompt verbatim, non-supplement `run_package/task/card` verbatim + drift refusal via `_check_evidence_package_files_content`, supplement contract from `SUPPLEMENT_SCHEMA` live bytes + rehash, rule string byte-exact vs `prepare_evidence_package:981-983`. Tasks sorted discovery order, `stable_task_id`/`task_filename`/`core.json_bytes` recompute, sorted supplement IDs, meta `authority_supplement_source_ids` == task, exact-once binding, IDs-require-manifest / contract-requires-manifest enforced. Good.
- HIGH prepare: request `SizedRef` shape + `_verify_sized_ref_bytes` before any package/task write; package `authority_supplement == request {path,sha256}` before writes; `candidate_outputs.supplement_manifest == request` before manifest. Null enforces no authority/contract/IDs. Good.
- Prove: request shape+bytes, manifest shape+bytes, `man_supp == req_supp`, `new_auth == req {path,sha}`, null enforces no authority + manifest null. Covers r2-review §2.8 (manifest↔request leg). Good. No proof-schema change. Contract8 unchanged (scripts absent from identity); tool SHAs will change for 2 modules — fresh pins + `expected_head/tree` required at packaging (not done yet).

Required (CHANGES_REQUIRED):
- **C1 — package-path pin discipline missing.** R2 §3 requires `_capture_phase_pins` before validation + `_recheck_supplement_context` + `_recheck_phase_pins` + `_finish_authority_phase` (no reseal). Implementation only calls `_recheck_supplement_context` before return (diff `survey_research_authority_v2.py` ~2465-2469). No `_capture/_recheck_phase_pins` for request/COPY/OLD/basis in `build_revision_package_from_paths`; COPY drift checked once at start (~2249-2251) but not rechecked before return; OLD package/request/screening pins never rechecked. Cards path already does capture/recheck (~2506-2529) — package path must match that discipline. Minimum: capture pins for request + COPY + OLD package + selected manifest/basis + ALL Raw before derivation, then before return `_recheck_supplement_context` + `_recheck_phase_pins` + owner revalidate via `_finish_authority_phase` (or explicit equivalent order: recheck supp + recheck pins + revalidate + recheck again). Never reseal, never claim zero-all-write.
- **C2 — dead-code cross-check + unused reads.** Helper computes `expected_disc_abs`/`expected_scp_abs`/`manifest_abs` then does `if …resolve() != ds.effective_path…: pass` and `_ = (expected_scp_abs, manifest_abs)` — a check that enforces nothing. Real discovery/screening-path enforcement currently lives inside `_resolve → validate` via provisional `basis`, but the helper text suggests an explicit check. Minimum: delete the `pass` branch and unused `_safe_read_bytes`/`_` tuple, or replace with an explicit equality (`request.discovery_ref.path` == ds effective path already bound by kernel `1630-1651`, and manifest basis == request refs) with a refusal. Do not leave a no-op that reads as a guard.

No private→public bypass found for the parts above; C1/C2 are weaker-invariant gaps, not style.

## 4. Tests — real HIGH, truthful scope, 1 mislabel + deferred coverage

Keep (verified in `test_dm022_supplement_carry_v2.py` FULL, no mocks/patches):
- Real `high.prepare_revision` + real validators + real `build_evidence_authority_supplement`, isolated fixture DBs with meaningful commits, process-scoped Git identity, `PYTHONDONTWRITEBYTECODE=1`, no manual `supp-candidate` as HIGH witness, no stubbed `_resolve/_merge/_build_card/validate/build_revision_package`, no fake repo/empty root/stub proof. Good.
- WEEKLY DERIVED novel→unchanged (`test_weekly_derived_novel_then_unchanged_carry`): 3 DIDs (`derived-alpha/beta/gamma` via `_chain_root_real_head` + `include_base_in_effective=False` + `parent_refs`), supplement on 2 + Discovery-only on 1, rev1 all-3 affected then rev2 `derived-alpha` only, unaffected `beta/gamma` byte-identical cards, `adopt`×2 + `readback` + `resume` (`ALREADY_ACTIVE/RESUME_*`), true `R!=E` oracle on pinned COPY via `derive_ordinary_root_effective_context`. Genuine DERIVED, not fixture enum.
- THEMATIC direct novel→unchanged (`test_thematic_direct_novel_then_unchanged_carry`): same 3-task pattern via `_build_3did_direct_chain`, `adopt`×2 + `readback`. Covers Special route with recorded limitation (Profile-initial + COMPLETE only; full 7-field/named/KEEP+DROP remains ordinary-path `828/927b` — correctly not claimed as extended).
- Red control (`test_red_control_null_manifest_with_supplement_bindings_refuses_at_card`): null manifest + `supplement-src-*` binding refuses at actual card build `source_bindings must explicitly select task-bound sources`, asserts `candidate_outputs.supplement_manifest` absent from message — genuine original-producer failure, not token. Fresh revision root. Good.
- Raw `focused-test-raw.txt`: 4 tests OK, `11.187s` (author `11.225s` is run variance, truthful), 1 `ResourceWarning` (tempdir implicit cleanup in weekly) — minor, fix with explicit cleanup.
- Author scope/unresolved explicitly defers: replaced version, late/readback oracles (`807/888/950/1124/1327/1603/1662`), retention/guard/resume beyond `ALREADY_ACTIVE`, full ledger `rows_checked` beyond byte-identical cards, no whole old suites, no CURRENT proof/packaging/DIRECT, no real W34/SP 409/160. Explicit, not hidden.

Required (CHANGES_REQUIRED):
- **T1 — decoy test mislabeled, triangle unproved.** `test_decoy_request_manifest_mismatch_refuses` does NOT craft a decoy `SizedRef` (unrelated-file path/sha that passes schema) and attempt `prepare`/`prove`. It checks OLD+null fail-fast via direct helper + unknown-DID refusal at supplement builder. Rename and add real decoy negatives: (a) request manifest bytes valid but `package.authority_supplement` tampered before first write, (b) `candidate_outputs.supplement_manifest != request`, (c) null vs non-null mismatches on both `prepare` and `prove` paths, each with exact refusal + R inventory + guard/State preservation. Current name claims coverage it does not provide.
- **T2 — replaced version missing.** R2 requires unchanged (W34 same) + replaced (SP 27+3) + novel + no-supp compat. Only novel→unchanged covered for both routes. Add OLD-supplemented + NEW-different-manifest positive with same ≥3-task asserts + byte-identical unaffected + ledger identity.
- **T3 — ledger/rows_checked asserts missing.** Positives assert package authority/contract, per-task IDs, card `supplement-src-*` vs `src-1`, byte-identical unaffected cards — but NOT ledger rows identical for unaffected, task-identity + Discovery→task binding identical, `unaffected_comparison.rows_checked` covering all non-DROP + ledger rows, `mechanical_projections` allowlist. Add per r2 §6 or mark as explicit next-verification (author already notes beyond byte-identical cards remains).
- **T4 — regressions + CURRENT/proof still open (expected for initial return, record as blockers).** Targeted subset per `test-oracle-inventory.md` §9 (LOW supplement/scaling + HIGH A2/C + Thematic obligations), no-supp compat (`:615`/`:486` + C regressions), fresh `verify_renewal_source_proof` CURRENT via actual API with new `expected_head/tree` + tool pins, then exact complete delivery. Do not treat 4-test OK as operation acceptance, semantic review, Human approval, or R4 audit.

## 5. Bounds

- No source edits/tests/runtime/imports/network/Production/subagents performed or selected. Hash/parse via Python stdlib only; no `git` binary invoked.
- Uses only final139 applied proof + authorized packet DATA (fixed774/c8 + 17 SP URLs/version metadata + P1-P6/publisher intake/supplement captures as DATA, never refetched). Three-archive-URL permission used/completed, not standing.
- Whole NOT_READY/step4B3OPEN/audit unstarted/DM021+022OPEN; quality/adoption/savings OPEN. Next is code/test corrections above + scoped re-review, then affected verification + CURRENT proof + exact delivery + independent implementation review before Human Commit Point. Ordinary Commit/Push Human-owned.
