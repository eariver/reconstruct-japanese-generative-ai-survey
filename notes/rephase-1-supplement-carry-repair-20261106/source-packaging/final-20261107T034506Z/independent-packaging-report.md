# Independent packaging report — supplement-carry repair COMPLETE DIRECT409 delivery (packaging only)

Date: 2026-11-07 UTC TS 20261107T034506Z. NEW independent packaging owner, not source author. Source QUIESCENT frozen author workcopy `.rephase-1-editorial-runtime/supplement-carry-implementation-20261106T131722Z/candidate-work`, actual409b292756dd1277b9dfae87679934c0d2ce251c/tree8ce3699861505f32d1d60bdc185d4d4f635aedb2 + overlay. No source/tests/candidate Git index/config edits, no ordinary candidate/reconstruct Commit/Push, no Human Commit readback/root Git status/log/HEAD, no network/Production/current checkout. Other verifier uses NEW separate snapshot read source, no source changes. No subagents. Preserve prior packets/source/rehearsal e84 fixtures/55 Gitlinks/child dirt. No cleanup/reset/old runner execution.

## 0. Authority read + delta verification (fail-closed, no assumption)

- Old final139 `notes/rephase-1-evidence-scaling-repair/source-packaging/final-20261103T174718Z/`: patch `de0af9cbd58665dc632a53cee5a0605da30ba9cdd3dc63202268565ba9887d49`/5408065B, manifest `c5a6b230c975dc94a45e651f48cd42687f84d060c65b37f49d9917ff1bf0f143`/202204B, 771 files (689 tracked +82 new, 57M+82A=139).
- Verified actual author workcopy 773 intended (excluding .git/__pycache__/*.pyc via `find -path .git -prune -o -type f`): `cand-find` 773, `cand-count` 773 STABLE, 0 pyc/cache residue. Early python walk 766 (substring `.git` in `.github` bug) preserved as superseded enumeration error, corrected via find to 773 with raw.
- `gen-verify689`: orig_new 84 new82+2=84 intended 773 base689 689
  ls-tree HEAD -- <689> 689 lines, batch-check missing 0
  BASE689-AVAILABLE
- `gen-verify`: CAND 773 GEN 773 (tar copy, no --link, mode preserved)
  only_c 0 only_g 0 mismatch 0 mode_mismatch 0
  GEN==CAND 773/773 0 mismatch
- New delta `gen-diff-names` 141 files, `gen-diff-namestatus` 84A/57M/0D/R, `gen-diff-stat` 141 files changed, 86326 insertions(+), 975 deletions(-). M set identical to old diff_M (57, 0 extra/missing), new_A = old82 +2 new tests. Inherited139 included DIRECT, 0 missing; extra-in-new =2 (supplement_carry + scale). If any other change existed, packaging would have aborted — none found; other 768? SHA/bytes identical to old manifest except 3 modified (2 runtime + C test) +2 new.
- Runtime pins re-verified UNCHANGED vs author (see §4).

## 1. Delivery artifacts (NEW unique packet, old intact)

`notes/rephase-1-supplement-carry-repair-20261106/source-packaging/final-20261107T034506Z/`:

- `complete-supplement-carry-409.patch` — SHA256 `3032752c948c59d752e414b91b6ef0d0a2ce8823458442abc2833712eb1e8dc0` / 5526524B. ONE complete DIRECT actual409-relative full-index binary patch (`git diff --cached --full-index --binary HEAD` temp index): 141 files, 86326+/975-. Covers ALL current deltas INCLUDING inherited139 (old139 − new141 =0 missing sans 2 new; no incremental old138 layer, no old overlay layering).
- `complete-supplement-carry-manifest.json` — SHA256 `f88f6d088381beb7cb975b068ef308ddb8d794c8daffc92639d6f11e62e470cf` / 202750B. All 773 intended paths {SHA256, bytes, git_mode, physical_mode, kind} + delta (diff_M 57, new_A 84) + pins. Full 64-char hashes, no mistranscription; HIGH/LOW etc. verified in manifest + workcopy.
- Raw GEN/proof logs: `cand-*`, `cp-git-*`, `gen-*`, `proof-*`, `indep-*`, `patch-*`, `manifest-*`, `workcopy-pins-*`, `inode-*`. No Git DB in packet. Old packet `final-20261103T174718Z` untouched.

## 2. Freeze root + isolation (ignored runtime, fresh DBs)

- GEN: `.rephase-1-editorial-runtime/supplement-carry-packaging-20261107T034506Z/gen-copy/candidate-partial-b40de60/` (773 files, `.git` byte-copied `cp -a` no `--link`) + `gen-index` TEMP (outside packet, candidate/root indexes untouched). GEN DB 83 files at copy (224 after staging 141 new blobs, expected: 83+141), 0 inode overlap vs candidate/base/proof, no alternates/commondir, inert `example.invalid` origin, HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`/tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`. GEN == CAND 773/773 0 mismatch.
- PROOF (FINAL applied path for verifier): `.rephase-1-editorial-runtime/supplement-carry-packaging-20261107T034506Z/proof-copy/candidate-partial-b40de60/` (+ `.git` separate byte-copy 83 files, 0 overlap, inert origin, HEAD/tree same). NEW fail-closed restore via `git show HEAD:<path>` per-file for 689 (no fake-root/commit/network/lazy fetch, no old runner), then mode fix 775 for single 755 file before check. Before = clean 689 base only (see §6); after =773 (actual complete-patch applied source, not ad-hoc copy).
- No blind-copy residue: CAND/GEN/PROOF 0 `*.pyc` files; 0 `__pycache__` dirs. No `GIT_*` env; `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_TERMINAL_PROMPT=0`, `GIT_NO_LAZY_FETCH=1` for GEN/PROOF Git only. No `git config`, no empty commit, no fixture commits. No old `/tmp/opencode/jgas-*` runners executed; fresh fail-closed inline procedure only.

## 3. Measured actuals (derived, expected 141/773 verified)

- Intended **773** = **689** tracked + **84** untracked. Worktree 773, missing 0, extra 0, pyc files 0.
- Delta **57M + 84A =141** (`git diff --cached --name-status HEAD`: 84 A, 57 M, 0 D/R, exit 0; `gen-diff-names` 141). Insertions 86326 (+1711 vs prior 84615 from 2 new tests + runtime deltas), deletions 975 (same as prior, new files pure additions).
- Single new paths vs original manifest: `tests/test_dm022_supplement_carry_v2.py`, `tests/test_dm022_supplement_carry_scale_v2.py` (new_A extra beyond old). Modified vs proof139 exactly 3 (2 runtimes + C test, see §4). All other 768? SHA/bytes identical to old manifest except those 3 +2 new.
- Unchanged inherited: all original 139 paths in new 141 (0 missing; extra-in-new =2, no M/A shift). Base689 availability: `ls-tree HEAD -- <689>` 689, `cat-file -e HEAD:<path>` 689 missing 0 (`BASE689-AVAILABLE`). Bulk missing26309/bulk31466/runtimeTeX unbundled (qualified). No `.tmp`/`*~`. Git modes 772×`100644`→`0o664` +1×`100755`→`0o775`, 0 mismatch. Physical modes 0/773 mismatch.

## 4. Pins (full 64-char, machine-generated, no mistranscription)

- CAND HEAD `5eef790bd8d492c557cc4db9c29425e3e410d47d` (new isolated root, already-applied final139 771 files, not 409 ancestry; preserved, not replaced), shallow `774dd39a…`? No, CAND is new root, not shallow; origin inert `invalid.invalid`. After stable.
- GEN/PROOF HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`/tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, inert `example.invalid`, no `GIT_*`.
- Frozen pins (CAND/GEN/PROOF identical, from `workcopy-pins-stdout.txt`):
```
f312f02e2dc5c1aa5a1d6432bca134cd83f0a1edea2d127721d0206d05514a90  scripts/survey_prearchitecture_acceptance_v2.py (97844B)
d50282bf0812a4d07e3da13cf3574961add0466cd27a3ef3c648b89fe40330dd  scripts/survey_research_authority_v2.py (239978B)
1fa905bf7e184cb63905b05d87018e27b7b55387f450352bbd02d4ddfe888e31  tests/test_dm022_c_direct_operation_v2.py (43626B)
5d5d3aadec70bc5d5c22fdec3e3c65d4f38d73aa995d326d8927fb8f73e26f00  tests/test_dm022_supplement_carry_v2.py (60569B)
7118092f80b1a7a23f198b887926ec1631c7adf9f3503c7016cc693254644668  tests/test_dm022_supplement_carry_scale_v2.py (27736B)
```
- All 773 SHA/bytes/modes in manifest.

## 5. GEN zero/non-zero (numeric)

`cp-git` 0/0, `cand-find` 0 (773), `gen-verify` 0 (773/773), `gen-read-tree` 0, `lstree` 0 (32155 HEAD; staged 32239=32155+84 after add), `lsfiles-stage-after` 0, `add` 0, `status` 0 (31607 incl bulk D, correctly EXCLUDED from `--cached`), `diff-names` 0 (141), `namestatus` 0 (84A/57M, only M/A), `stat/numstat/diff` 0/0/0 (141, 86326+/975-). `diff-check` exit **2** with 392B whitespace preserved (trailing + blank-EOF, identical to prior 392B). No suppression. Patch 5526524B exit 0.

## 6. Independent proof (NEW separate DB, clean 689, no old overlay, no wrong-cwd overwrite)

- Proof root above (ignored, NEW unique). Source: candidate `.git` independent `cp -a` (`cp-git-proof` 0). HEAD/tree/inert/noalternates as GEN.
- Baseline: 689 via read-only objects (`RESTORED 689/689` exit 0). Before: worktree 689, new84 absent 84/84, `proof vs HEAD mismatch 0`, `proof vs manifest unchanged 632 differ 57` == `diff_M`, bridge mode 664 vs HEAD 755 (`BEFORE-689-OK`):
```
proof new84 absent 84/84
proof vs HEAD mismatch 0
proof vs manifest unchanged 632 differ 57
```
No apply on old138.
- Numeric: first `apply --check --verbose` exit **0** 0B/8988B with mode warning `scripts/survey_core_execution_bridge_v2.py has type 100644, expected 100755` (restoration wrote 664, not 775; preserved as genuine). After `chmod 775` to match HEAD, second `apply --check` exit **0** 0B/0B (no `--whitespace=fix`, no `--reject`; two checks logged uniquely, no overwrite). Actual `apply --verbose` ONCE exit **0** 0B/19641B with whitespace warnings preserved (`trailing whitespace` + `5 lines add whitespace errors`; verbose 8988B + whitespace). No `no warnings` claim.
- Full 773 +141: proof 773, manifest 773, missing 0, unexpected 0; content 0/773 vs manifest across CAND/GEN/PROOF; physical 0/773; gitmode 1×755 rest 644; delta 57/84; `FULLVERIFY-OK` (not sample-only):
```
CAND 773 GEN 773 PROOF 773 MANIFEST 773
only_c 0 only_g 0 only_p 0
mismatch CG 0 CP 0 CM 0 PM 0
delta M 57 A 84 delta_ok True
FULLVERIFY-OK
```
- Lineage: new patch supersedes old139 TEST-oracle + supplement-carry repair (2 runtimes + C test modified +2 new tests), not evidence invalidation of unchanged runtime/other tests (carried as source-bound composite). Old139 included (0 missing). No reapply beyond single required apply. No ordinary/reconstruct commit/new HEAD. No unread historical objects.
- DB/inode: `cand 834 / gen 224 (83+141 staged blobs) / proof 83`, all distinct inodes, `OVERLAP 0/0/0` (`INODE-SEPARATION-OK`):
```
cand 834 gen 224 proof 83
overlap cg 0 cp 0 gp 0
```
nlink 1, symlinks 0, no `160000` gitlinks (`gen-gitlinks` 0 lines), no alternates/commondir, inert origin, no `git config`. Packet has no `.git`. No Human HEAD/status/log/readback (no reconstruct `.git` inspection; scoped CAND/GEN/PROOF only).

## 7. Real409 e84 comparison (not re-executed, preserved)

Prior real409 e84 had test d486 vs delivered 7b86 (1-test delta, other770 identical). New delivery adds 2 scale tests + 3 modified files vs that baseline; no new real-material run here. Saved real e84 material remains unchanged; real correction/adoption retains separate independent semantic review requirements.

## 8. Exclusions/limits

PartialDB `26309`/bulk `31466`/runtimeTeX unbundled; scoped `689+84` only (staged `32239` vs materialized `773`), not full hydrated/tree-clean; missing26309/bulk31466/runtimeTeX nonbundled retained. No tests/build/import/runtime, no adoption/semantic/production, no migration/audit, no certified rerunner/globalCAS/crash-atomicity, no suite-count decoration. No driver scripts shipped (`gen-index` in WORKROOT, `/tmp` lists outside packet, not shipping source). No reapply. Source stable (`GEN==CAND` 773/773). Old packet superseded only as above.

## 9. Failures/warnings/deviations

- `gen-diff-check` 2 + `apply` whitespace preserved (not normalized). Identical 392B diagnostics as prior, not autofixed.
- First `apply --check --verbose` 8988B mode warning preserved (restoration mode gap, fixed to 775 before second check + apply; no overwrite, both checks logged uniquely).
- Wrong-cwd procedural error preserved: initial `apply --check` from `/tmp` returned 1 with 15495B missing-file diagnostics (`indep-apply-check-wrongcwd-*`); correct PROOF-cwd check returned 0. Not a source defect, not overwritten.
- Early python walk 766 vs find 773 enumeration bug (substring `.git` in `.github`) preserved as superseded, corrected via find to 773.
- No `apply_patch` binary; new packet files via bash redirections for generated artifacts (allowed). No source edits via file tools.
- Old runners read as DATA only, never executed; fresh inline procedure only.
- No old PASS transferred; no behavioral tests/build run here; independent implementation review separate. Available FINAL applied path for verifier: `.../supplement-carry-packaging-20261107T034506Z/proof-copy/candidate-partial-b40de60` (773 files, patch applied, exits check 0/8988B + check2 0/0 + apply 0/19641B). Executable/full-source binding: frozen pins §4 + manifest (all 773) + patch (141).

## 10. Scope

Checked: 5-file deltas (2 runtimes + C test modified +2 new) + other 768 SHA/bytes identical to old manifest except those 5? Actually M=57 includes prior 57, A=84 includes prior82+2 new; saved patch/manifest FULL hash+bytes (64-char); before HEAD/tree/689/new84/clean; numeric `check 0/8988B + check2 0/0 + apply 0/19641B` + whitespace retained; all 141 +773 byte-exact across CAND/GEN/PROOF; inherited139 inclusion; DB/inode/alternates/origin/index/packet guards; old packet intact (`de0af9cbd5…/5408065B`, `c5a6b230…/202204B` re-verified). Real409 e84 1-test delta preserved, other770 identical, DATA extra excluded.

Not checked/claimed: runtime behavior, test execution, semantic approval, production quality, full-history/tree-clean, migration/adoption, audit, whole readiness. No code/adoption PASS. Baseline774, partialDB preserved, no fake root/empty commit/config change. Stop at packaging; final review separate. WholeNOT_READY/step4B3OPEN/auditunstarted/DM021+022OPEN; quality/adoption/savings OPEN.

ProofDB: `.rephase-1-editorial-runtime/supplement-carry-packaging-20261107T034506Z/proof-copy/candidate-partial-b40de60` (83-file `.git` +773). RAW: `indep-*.txt` + `gen-*.txt` + `cand-*.txt` + `workcopy-*.txt` in same packet. Patch `3032752c948c59d752e414b91b6ef0d0a2ce8823458442abc2833712eb1e8dc0/5526524B`, manifest `f88f6d088381beb7cb975b068ef308ddb8d794c8daffc92639d6f11e62e470cf/202750B`.

(End — independent packaging owner, fail-closed.)
