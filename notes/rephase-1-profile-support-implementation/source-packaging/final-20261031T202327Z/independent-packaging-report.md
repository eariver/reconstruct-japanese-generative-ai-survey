# Independent packaging report — Profile/support COMPLETE DIRECT409 delivery (TEST-oracle supersession, packaging only)

Date: 2026-10-31 UTC. NEW packaging owner, not source author. Source QUIESCENT; concurrent final verifier reads/runs separate snapshot, does not modify source. No source/tests edits, no candidate Git/index/config edits, no ordinary commit, no reconstruct git status/HEAD/log/readback/network/restore-from-remote/Production/intake/cleanup/reset. Existing 55 Gitlinks/child dirt untouched. No README edit (root preparing closeout other files; race avoided — report only).

## 0. Authority read + delta verification (fail-closed, no assumption)

- `notes/rephase-1-profile-support-implementation/astra-implementation-review.md` last section §§64–72 (final evidence/oracle corrections before closeout): only new C test module needs selected oracle/retention correction unless execution reveals real defect; after that run affected methods on final applied source and regenerate complete patch/manifest in NEW packet; keep first packaging/raw; unchanged runtime/other-test evidence carried as source-bound composite.
- `notes/rephase-1-profile-support-implementation/dm022-integration-verification.md` §11 (fifth return): only `tests/test_dm022_c_direct_operation_v2.py` changed 35636B `ac44154f…` → 42156B `6ffde575a21b3748147fda3f662d7934a78c5082a062a4f174519d4902aee585` (7 methods; initial pin preserved in review/packaging history). Runtime pins re-verified UNCHANGED (`546bbad1`/`388c8994`/`f0f28954`/`36b7b583`/`5a6280ac`/`ed0155cd`); snapshot 770 files. Retention hardcoded writer removed; extra preservation ONLY under explicit `PROFILE_SUPPORT_RETAIN_ROOT` (normalized/jailed/fresh mkdtemp/exclusive `xb`; ordinary run temp-only). Exact predicates (N1/N4/N5/N6 full texts, N7 ghost-DID with owned-partial window, N3a/b, N2 single-error, N8 stored-manifest `present`-flip, N9a/b request-integrity + real tool-bytes drift) + SHA/mode/dir/symlink inventories (`_sha_tree`); ordinary 3/5/LOW7 untouched. Focused runs `c-narrow`/`c-integrity4`/`c-changed-rest`/`c-retain-env` exit 0 (real captures, unchanged positives not rerun).
- Verified against original manifest `final-20261031T200637Z/complete-profile-support-manifest.json` (770, 57M/81A, HEAD `409b292…`, tree `8ce3699…`): workcopy 770, missing 0, extra 0, modified exactly 1 (`tests/test_dm022_c_direct_operation_v2.py` 42156B `6ffde575a21b3748147fda3f662d7934a78c5082a062a4f174519d4902aee585`, 64 chars, matches §11; old pin 35636B `ac44154fa0ba7e4b3d83bbbdda8e242e03fd50b048b92a293820da805b56b97a`). If other changes existed, packaging would have aborted — none found; runtime + other 769 unchanged as claimed.

## 1. Delivery artifacts (NEW unique packet, old intact)

`notes/rephase-1-profile-support-implementation/source-packaging/final-20261031T202327Z/`:

- `complete-profile-support-409.patch` — SHA256 `efb505e44c1ccb3c83121db2fbaa9fec05ed900c252184765ca3b50f7b28254e` / 5247647B. ONE complete DIRECT actual409-relative full-index binary patch (`git diff --cached --full-index --binary HEAD` temp index): 138 files, 81930 insertions, 855 deletions. Covers ALL current deltas INCLUDING inherited 133 (old133 − new138 = 0; no incremental on old patch, no old overlay layering).
- `complete-profile-support-manifest.json` — SHA256 `634d41f9807e8cd60ca3d839245358fa5e5da312f6d1b58ae84c1619481a03dc` / 186847B. All 770 intended paths `{SHA256, bytes, git_mode, physical_mode, kind}` + delta (`diff_M` 57, `new_A` 81) + pins. Full 64-char hashes, no mistranscription; HIGH `388c89941cef393868c9a2cef5ad7276889ffa01aeda294e756c0d76b6f9efd4` (64, verified in manifest + workcopy).
- Raw GEN/proof logs: `cp-git-*`, `tar-*`, `gen-count-*`, `gen-pyc-*`, `gen-head-*`, `gen-revparse-*`, `gen-remote-*`, `gen-noalternates-*`, `inode-check-*`, `gen-verify770-*`, `gen-read-tree-*`, `gen-verify689-*`, `gen-lstree-*`, `gen-lsfiles-stage-*` + `-after-*`, `gen-add-*`, `gen-status-*`, `gen-diff-names-*`, `gen-diff-namestatus-*`, `gen-diff-stat-*`, `gen-diff-numstat-*`, `gen-diff-check-*`, `gen-diff-*`, `manifest-gen*`, `patch-sha256/byts`, `manifest-sha256/bytes`, proof `indep-*`, `workcopy-before/after-*`, `candidate-head-after-*`, `gen-gitlinks-*`. No Git DB in packet. Old packet `final-20261031T200637Z` untouched: patch `e0ca796f6091f0ab2c824e616dc43705d6234ba9b15c827a132010249985a938`/5240998B, manifest `5a34afe827d1a2fa15e4325a20fded8de54339dd624c4c3d5447bd8646d215fa`/186595B re-verified intact.

## 2. Freeze root + isolation (ignored runtime, fresh DBs)

- GEN: `.rephase-1-editorial-runtime/profile-support-packaging-20261031T202327Z/gen-copy/candidate-partial-b40de60/` (770 files, `.git` byte-copied `cp -a` no `--link`) + `gen-index` TEMP (outside packet; candidate/root indexes untouched). GEN DB 83 files at copy (221 after staging 138 new blobs, expected), 0 inode overlap vs candidate, no alternates/commondir, inert `example.invalid` origin, HEAD `409b292…`/tree `8ce3699…`. GEN == CAND 770/770 0 mismatch.
- PROOF (FINAL applied path for affected-7 verifier): `.rephase-1-editorial-runtime/profile-support-packaging-20261031T202327Z/proof-copy/candidate-partial-b40de60/` (+ `.git` separate byte-copy 83 files, 0 overlap, inert origin, HEAD/tree same). NEW helper `restore689-new.py` (ignored runtime, not packet, not old runner) via `git show HEAD:<path>` per-file, no fake-root/commit/network/lazy fetch. Before = clean 689 base only (see §6); after = 770 (actual complete-patch applied source, not ad-hoc copy).
- No blind-copy residue: GEN/PROOF/CAND 0 `*.pyc`/0 `__pycache__`. No `GIT_*` env; `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_TERMINAL_PROMPT=0`, `GIT_NO_LAZY_FETCH=1` for GEN/PROOF Git only. No `git config`, no empty commit, no fixture commits. No old `/tmp/opencode/jgas-*` runners executed; fresh fail-closed inline procedure only.

## 3. Measured actuals (derived, expected 138/770 verified)

- Intended **770** = **689** tracked + **81** untracked. Worktree 770, missing 0, extra 0, pyc 0.
- Delta **57M + 81A = 138** (`git diff --cached --name-status HEAD`: 81 A, 57 M, 0 D/R, exit 0; `gen-diff-names` 138). Same counts as first package (expected: TEST-only content change within existing A file, not new path/M/A shift). Insertions 81930 (+129 vs first 81801 from 6520B test growth), deletions 855 unchanged.
- Single changed path vs original manifest: `tests/test_dm022_c_direct_operation_v2.py` 35636 `ac44154f…` → 42156 `6ffde575a21b3748147fda3f662d7934a78c5082a062a4f174519d4902aee585` (64, 7 methods, portable env-gated unique retention replacing hardcoded workspace overwrite, exact error/SHA no-write oracles per §11). All other 769 SHA/bytes identical to original manifest.
- Unchanged inherited: all original 133 paths in new 138 (0 missing); extra-in-new = 5 (3 newly-M +2 new-A from first package, unchanged here). Base689 availability: `ls-tree HEAD -- <689>` 689, `cat-file --batch-check` 689 missing 0 (`BASE689-AVAILABLE`). Bulk missing26309/bulk31466/runtimeTeX unbundled (qualified). No `.tmp`/`*~`. Git modes 769×`100644`→`0o664` +1×`100755`→`0o775`, 0 mismatch.

## 4. Pins (full 64-char, no mistranscription)

- CAND HEAD `409b292756dd1277b9dfae87679934c0d2ce251c` (`cat .git/HEAD`), shallow `774dd39a951c9ac3818e83dfffd4c7666efb0a20`, origin inert, no `GIT_*`; after stable.
- Frozen pins (workcopy/GEN/PROOF identical): Screening 82277 `f0f289540302753b2e7cad5f4fded1df0387ca1403309aa032a733199c42d5a1`; Evidence 130152 `36b7b5832845ea8a984697f980b0148fdf454736`; Runner 45084 `5a6280ac19986a05e363a673dd57294ed6d4257355fdb888d9cdd9466fe5d812`; Agent-first 3684 `f73f2ab91fc88a794d4f734d0952e80edff438259d3ad2315001df60b8d61910`; LOW 212084 `546bbad1cfc84cd28e984b3652df08b52a07e5015dcf2836717fb64238212737`; HIGH 92741 `388c89941cef393868c9a2cef5ad7276889ffa01aeda294e756c0d76b6f9efd4` (64); shared helper 43662 `ed0155cdf97c1baa8381113e775f232c4641c2f52a3c1f815970f5dbf4c03adc`; ordinary tests 115763 `926e2e0a0ee2f7104ed5c92d7bbdd50ef3610b2d7f6fd542c51a5bcb597632d6`; C-direct 42156 `6ffde575a21b3748147fda3f662d7934a78c5082a062a4f174519d4902aee585` (64, 7 methods). Contract hash preserved correctly `62b14add5e50d7e5f7996c4b7536f95b5d74cdbc9b205b1eec54bde260527e2d` (…`54bde…`, not …`54de…`); all 770 SHA/bytes/modes in manifest.

## 5. GEN zero/non-zero (numeric)

`cp-git` 0, `tar` 0/0, `gen-count` 0 (770), `gen-pyc` 0 (0), `gen-head/revparse/remote` 0, `noalternates` 2 (absent expected), `read-tree` 0, `lstree` 0 (32155 HEAD; staged 32236=32155+81 after add), `lsfiles-stage-after` 0, `add` 0, `status` 0 (31604 incl bulk D, correctly EXCLUDED from `--cached`), `diff-names` 0 (138), `namestatus` 0 (81A/57M, only M/A), `stat/numstat/diff` 0 (138, 81930+/855-). `diff-check` exit **2** with 5 whitespace lines preserved (trailing +4 blank-EOF, 392B). No suppression. Patch 5247647B exit 0.

## 6. Independent proof (NEW separate DB, clean 689, no old overlay, no wrong-cwd overwrite)

- Proof root above (ignored, NEW unique). Source: candidate `.git` independent `cp -a` (`indep-cp-git` 0). HEAD/tree/inert/noalternates as GEN.
- Baseline: 689 via read-only objects (`RESTORED 689/689` exit 0). Before: worktree 689, new81 absent 81/81, `diff --name-only -- <689>` exit 0 0B, 632 unchanged == manifest, 57 differ == `diff_M`, modes 0/689 `BEFORE-689-OK`. No apply on old133.
- Numeric: `apply --check` with `workdir=PROOF` exit **0** 0B/0B (no `--whitespace=fix`, no `--reject`; single correct invocation — no wrong-cwd attempt, no overwrites). Actual `apply` ONCE exit **0** 0B/1115B with 5 whitespace warnings preserved (line numbers 74529/44849/48733/74529/81658 + summary; same files as first, shifted by test growth). No `no warnings` claim.
- Full 770 +138: proof 770, manifest 770, missing 0, unexpected 0; content 0/770 vs manifest across CAND/GEN/PROOF; physical 0/770; gitmode 1×755 rest 644; delta 57/81; `FULLVERIFY-OK` (not sample-only).
- Lineage: first patch superseded TEST-oracle only (C-direct bytes), not evidence invalidation of unchanged runtime/other tests (carried as source-bound composite per astra §72; runtime/other769 byte-identical). Old133 included (0 missing). No reapply beyond single required apply. No ordinary/reconstruct commit/new HEAD. No unread historical objects.
- DB/inode: `cand 853 / gen 991 (770+221 after staging) / proof 853`, all distinct inodes, `OVERLAP 0/0/0` (`INODE-SEPARATION-OK`), nlink 1, symlinks 0, no `160000` gitlinks (`gen-gitlinks` exit 1 0 lines), no alternates/commondir, inert origin, no `git config`. Packet has no `.git`. No HumanHEAD/status/log/readback (no reconstruct `.git` inspection; scoped CAND/GEN/PROOF only).

## 7. Exclusions/limits

PartialDB `26309`/bulk `31466`/runtimeTeX unbundled; scoped `689+81` only (staged `32236` vs materialized `770`). No tests/build/import/runtime, no adoption/semantic/production, no migration/audit, no certified rerunner/globalCAS/crash-atomicity, no suite-count decoration. No driver scripts shipped (`restore689-new.py` in WORKROOT, `/tmp/intended770c.txt` outside packet, not shipping source). No reapply. Source stable (`workcopy-before/after` 770/770 0 mismatch `SOURCE-STABLE`; HEAD/shallow unchanged). First package superseded TEST-oracle only.

## 8. Failures/warnings/deviations

- `gen-diff-check` 2 + `apply` 1115B whitespace preserved (not normalized).
- No `apply_patch` binary (consistent with A/B/C/D); new packet files via `Write` (new exclusive) + `bash` for generated artifacts (allowed). No source edits via file tools.
- Old runners read as DATA only, never executed; fresh inline procedure only.
- No wrong-cwd `apply --check` failure this round (first round `exit 1` preserved in old packet, not repeated/overwritten here).
- No old PASS transferred; no behavioral tests/build run here; independent final + affected-7 verification separate. Available FINAL applied path for verifier: `.../profile-support-packaging-20261031T202327Z/proof-copy/candidate-partial-b40de60` (770 files, patch applied, exits 0/0/1115B). Executable/full-source binding: frozen pins §4 + manifest (all 770) + patch (138).

## 9. Scope

Checked: single TEST-only delta (1/770, exact 64-char hash, 7-method oracle/retention per §11) + other769 unchanged; saved patch/manifest FULL hash+bytes (64-char); before HEAD/tree/689/new81/clean; numeric `check0/apply0 + 0/1115B` + whitespace retained; all 138 +770 byte-exact across CAND/GEN/PROOF; inherited133 inclusion; DB/inode/alternates/origin/index/packet guards; old packet intact (`e0ca796f…/5240998B`, `5a34afe8…/186595B` re-verified).

Not checked/claimed: runtime behavior, test execution, semantic approval, production quality, full-history/tree-clean, migration/adoption, audit, whole readiness. No code/adoption PASS. Baseline774, partialDB preserved, no fake root/empty commit/config change. Stop at packaging; final review separate. WholeNOT_READY/step4B3OPEN/auditunstarted/DM021+022OPEN; quality/adoption/savings OPEN.

ProofDB: `.rephase-1-editorial-runtime/profile-support-packaging-20261031T202327Z/proof-copy/candidate-partial-b40de60` (83-file `.git` +770). RAW: `indep-*.txt` + `gen-*.txt` + `workcopy-*.txt` in same packet. Patch `efb505e44c1ccb3c83121db2fbaa9fec05ed900c252184765ca3b50f7b28254e/5247647B`, manifest `634d41f9807e8cd60ca3d839245358fa5e5da312f6d1b58ae84c1619481a03dc/186847B`.

(End — independent packaging owner, fail-closed.)
