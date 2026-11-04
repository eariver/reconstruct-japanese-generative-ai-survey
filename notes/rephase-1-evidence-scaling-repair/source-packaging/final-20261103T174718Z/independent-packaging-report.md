# Independent packaging report — Evidence scaling repair COMPLETE DIRECT409 delivery (packaging only)

Date: 2026-11-03 UTC TS 20261103T174718Z. NEW independent packaging owner, not source author. Source QUIESCENT author workcopy `.rephase-1-editorial-runtime/evidence-scaling-implementation-20261103T114312Z/candidate-work`, actual409b292756dd1277b9dfae87679934c0d2ce251c/tree8ce3699861505f32d1d60bdc185d4d4f635aedb2+overlay. No source/tests/candidate Git index/config edits, no ordinary candidate/reconstruct Commit/Push, no Human Commit readback/root Git status/log/HEAD, no network/Production/current checkout. Other verifier uses NEW separate snapshot read source, no source changes. No subagents. Preserve prior packets/source/rehearsal bd80/e84 fixtures/55 Gitlinks/child dirt. No cleanup/reset/old runner execution.

## 0. Authority read + delta verification (fail-closed, no assumption)

- Old final138 `notes/rephase-1-profile-support-implementation/source-packaging/final-20261031T202327Z/`: patch `efb505e44c1ccb3c83121db2fbaa9fec05ed900c252184765ca3b50f7b28254e`/5247647B, manifest `634d41f9807e8cd60ca3d839245358fa5e5da312f6d1b58ae84c1619481a03dc`/186847B, 770 files (689 tracked +81 new, 57M+81A=138).
- Verified actual workcopy 771 intended (excluding .git/__pycache__/*.pyc): `workcopy-before` 771, `workcopy-after` 771 STABLE, 0 mismatch. New only `tests/test_evidence_scaling_v2.py`, missing 0, modified vs old exactly 3 runtimes. Previous views/head tests existed only snapshots; must all 19 deliver — verified all 19 deliver in merged author copy (see §4).
- `gen-verify689`: orig_new 81 new82 0 intended 771 base689 689
ls-tree lines 689 match True
batch-check 689 missing 0
BASE689-AVAILABLE
- `gen-verify771`: CAND 771 GEN 771
only_c 0 only_g 0 mismatch 0
GEN==CAND 771/771 0 mismatch
- New delta `gen-diff-names` 139 files, `gen-diff-namestatus` 82A/57M/0 D/R, `gen-diff-stat` 139 files changed, 84615 insertions(+), 975 deletions(-). M set identical to old diff_M (0 extra/missing), new_A = old81 +1 new test. Inherited138 included, 0 missing; extra-in-new =1 (new test). If any other change existed, packaging would have aborted — none found; other 767 SHA/bytes identical to old manifest.
- Runtime pins re-verified UNCHANGED vs expected (see §4): Evidence/Runner/LOW match final review; test FINAL19 matches.

## 1. Delivery artifacts (NEW unique packet, old intact)

`notes/rephase-1-evidence-scaling-repair/source-packaging/final-20261103T174718Z/`:

- `complete-evidence-scaling-409.patch` — SHA256 `de0af9cbd58665dc632a53cee5a0605da30ba9cdd3dc63202268565ba9887d49` / 5408065B. ONE complete DIRECT actual409-relative full-index binary patch (`git diff --cached --full-index --binary HEAD` temp index): 139 files, 84615 insertions, 975 deletions. Covers ALL current deltas INCLUDING inherited138 (old138 − new139 =0 missing; no incremental old138 layer, no old overlay layering).
- `complete-evidence-scaling-manifest.json` — SHA256 `c5a6b230c975dc94a45e651f48cd42687f84d060c65b37f49d9917ff1bf0f143` / 202204B. All 771 intended paths {SHA256, bytes, git_mode, physical_mode, kind} + delta (diff_M 57, new_A 82) + pins. Full 64-char hashes, no mistranscription; HIGH/LOW etc. verified in manifest + workcopy.
- Raw GEN/proof logs: `cp-git-*`, `workcopy-before/after-*`, `workcopy-pins-*`, `gen-count-*`, `gen-pyc-*`, `gen-head-*`, `gen-revparse-*`, `gen-remote-*`, `gen-noalternates-*`, `gen-gitlinks-*`, `gen-lstree-*`, `gen-lsfiles-stage-*` + `-after-*`, `gen-add-*`, `gen-status-*`, `gen-diff-names-*`, `gen-diff-namestatus-*`, `gen-diff-stat-*`, `gen-diff-numstat-*`, `gen-diff-*`, `gen-diff-check-*`, `manifest-gen*`, `patch-sha256/bytes`, `manifest-sha256/bytes`, proof `indep-*`, `real409-compare-*`, `inode-check-*`. No Git DB in packet. Old packet `final-20261031T202327Z` untouched.

## 2. Freeze root + isolation (ignored runtime, fresh DBs)

- GEN: `.rephase-1-editorial-runtime/evidence-scaling-packaging-20261103T174718Z/gen-copy/candidate-partial-b40de60/` (771 files, `.git` byte-copied `cp -a` no `--link`) + `gen-index` TEMP (outside packet, candidate/root indexes untouched). GEN DB 83 files at copy (222 after staging 139 new blobs, expected), 0 inode overlap vs candidate, no alternates/commondir, inert `example.invalid` origin, HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`/tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`. GEN == CAND 771/771 0 mismatch.
- PROOF (FINAL applied path for verifier): `.rephase-1-editorial-runtime/evidence-scaling-packaging-20261103T174718Z/proof-copy/candidate-partial-b40de60/` (+ `.git` separate byte-copy 83 files, 0 overlap, inert origin, HEAD/tree same). NEW fail-closed restore via `git show HEAD:<path>` per-file (no fake-root/commit/network/lazy fetch, no old runner), then mode fix 775 for single 755 file before check. Before = clean 689 base only (see §6); after =771 (actual complete-patch applied source, not ad-hoc copy).
- No blind-copy residue: GEN/PROOF/CAND 0 `*.pyc` files; 1 empty `__pycache__` dir excluded (pyc_files 0, pyc_dirs 1). No `GIT_*` env; `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_TERMINAL_PROMPT=0`, `GIT_NO_LAZY_FETCH=1` for GEN/PROOF Git only. No `git config`, no empty commit, no fixture commits. No old `/tmp/opencode/jgas-*` runners executed; fresh fail-closed inline procedure only.

## 3. Measured actuals (derived, expected 139/771 verified)

- Intended **771** = **689** tracked + **82** untracked. Worktree 771, missing 0, extra 0, pyc files 0.
- Delta **57M + 82A =139** (`git diff --cached --name-status HEAD`: 82 A, 57 M, 0 D/R, exit 0; `gen-diff-names` 139). Insertions 84615 (+2685 vs prior 81930 from test growth + runtime deltas), deletions 975 (+120 vs prior 855).
- Single new path vs original manifest: `tests/test_evidence_scaling_v2.py` (new_A extra beyond old). Modified vs old exactly 3 (Evidence/Runner/LOW, see §4). All other 767 SHA/bytes identical to original manifest.
- Unchanged inherited: all original 138 paths in new 139 (0 missing); extra-in-new =1 (new test, no M/A shift). Base689 availability: `ls-tree HEAD -- <689>` 689, `cat-file -e HEAD:<path>` 689 missing 0 (`BASE689-AVAILABLE`). Bulk missing26309/bulk31466/runtimeTeX unbundled (qualified). No `.tmp`/`*~`. Git modes 770×`100644`→`0o664` +1×`100755`→`0o775`, 0 mismatch. Physical modes 0/771 mismatch.

## 4. Pins (full 64-char, machine-generated, no mistranscription)

- CAND HEAD `409b292756dd1277b9dfae87679934c0d2ce251c` (`cat .git/HEAD`), shallow `774dd39a951c9ac3818e83dfffd4c7666efb0a20`, origin inert, no `GIT_*`; after stable.
- Frozen pins (workcopy/GEN/PROOF identical, from `workcopy-pins-stdout.txt`):
```
7b862305db39afde93c44ca0f1ce2d4b5faf512729e6956a8166b16f09c0e12e  /home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/evidence-scaling-implementation-20261103T114312Z/candidate-work/tests/test_evidence_scaling_v2.py
487425385052fa181b0a24954815c6fbb6882a0af1fc7256ef7352b309359c2a  /home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/evidence-scaling-implementation-20261103T114312Z/candidate-work/scripts/survey_evidence_v2.py
5e195730d1553b2359eb5729cebaa49e9bd616b4b3f63b65dca413ef33c3e543  /home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/evidence-scaling-implementation-20261103T114312Z/candidate-work/scripts/run_evidence_v2_interactive.py
0974c709b55365ef93cded5e97707e705b8a59aae01734e52c40e3b40c1a008b  /home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/evidence-scaling-implementation-20261103T114312Z/candidate-work/scripts/survey_research_authority_v2.py
```
- Full test file: `tests/test_evidence_scaling_v2.py` 106616B `7b862305db39afde93c44ca0f1ce2d4b5faf512729e6956a8166b16f09c0e12e` (FINAL19, 19 methods: 1c95f675 16 + Views 2 + runner 1; old-16 behavior byte-identical save one landed F5 docstring; final19 snapshot `evidence-scaling-final19-20261103T173758Z` same hash verified).
- Runtimes: Evidence `487425385052fa181b0a24954815c6fbb6882a0af1fc7256ef7352b309359c2a`/158943B, runner `5e195730d1553b2359eb5729cebaa49e9bd616b4b3f63b65dca413ef33c3e543`/45833B, LOW `0974c709b55365ef93cded5e97707e705b8a59aae01734e52c40e3b40c1a008b`/218692B (all 64-char, verified in workcopy + manifest + final19 + e84 retry).
- Contract hashes preserved; all 771 SHA/bytes/modes in manifest.

## 5. GEN zero/non-zero (numeric)

`cp-git` 0, `gen-count` 0 (771), `gen-pyc` 0 (0), `gen-head/revparse/remote` 0/0/0, `noalternates` 2 (absent expected), `read-tree` 0, `lstree` 0 (32155 HEAD; staged 32237=32155+82 after add), `lsfiles-stage-after` 0, `add` 0, `status` 0 (31605 incl bulk D, correctly EXCLUDED from `--cached`), `diff-names` 0 (139), `namestatus` 0 (82A/57M, only M/A), `stat/numstat/diff` 0/0/0 (139, 84615+/975-). `diff-check` exit **2** with 392B whitespace preserved (trailing + blank-EOF, identical to prior 392B). No suppression. Patch 5408065B exit 0.

## 6. Independent proof (NEW separate DB, clean 689, no old overlay, no wrong-cwd overwrite)

- Proof root above (ignored, NEW unique). Source: candidate `.git` independent `cp -a` (`indep-cp-git` 0). HEAD/tree/inert/noalternates as GEN.
- Baseline: 689 via read-only objects (`RESTORED 689/689` exit 0). Before: worktree 689, new82 absent 82/82, `proof vs HEAD mismatch 0`, `proof vs manifest unchanged 632 differ 57` == `diff_M`, modes 0/689 `BEFORE-689-OK` (see `proof 689 new82 absent 82/82
proof vs HEAD mismatch 0
proof vs manifest unchanged 632 differ 57
BEFORE-689-OK`). No apply on old138.
- Numeric: first `apply --check` exit **0** 0B/85B with mode warning `scripts/survey_core_execution_bridge_v2.py has type 100644, expected 100755` (restoration wrote 664, not 775; preserved as genuine). After `chmod 775` to match HEAD, second `apply --check` exit **0** 0B/0B (no `--whitespace=fix`, no `--reject`; two checks logged uniquely, no overwrite). Actual `apply` ONCE exit **0** 0B/1085B with whitespace warnings preserved (line numbers shifted vs prior 74529/44849 etc. to 77498/45958/49842 etc.; same files, test growth shift). No `no warnings` claim.
- Full 771 +139: proof 771, manifest 771, missing 0, unexpected 0; content 0/771 vs manifest across CAND/GEN/PROOF; physical 0/771; gitmode 1×755 rest 644; delta 57/82; `FULLVERIFY-OK` (not sample-only):
```
CAND 771 GEN 771 PROOF 771 MANIFEST 771
only_c 0 only_g 0 only_p 0
mismatch CG 0 CP 0 CM 0 PM 0
delta M 57 A 82 delta_ok True
FULLVERIFY-OK
```
- Lineage: new patch supersedes old138 TEST-oracle + Evidence scaling repair (3 runtimes +1 test), not evidence invalidation of unchanged runtime/other tests (carried as source-bound composite). Old138 included (0 missing). No reapply beyond single required apply. No ordinary/reconstruct commit/new HEAD. No unread historical objects.
- DB/inode: `cand 854 (771+83) / gen 993 (771+222 after staging) / proof 854 (771+83)`, all distinct inodes, `OVERLAP 0/0/0` (`INODE-SEPARATION-OK`):
```
cand 854 gen 993 proof 854
overlap cg 0 cp 0 gp 0
```
nlink 1, symlinks 0, no `160000` gitlinks (`gen-gitlinks` exit 1 0 lines), no alternates/commondir, inert origin, no `git config`. Packet has no `.git`. No Human HEAD/status/log/readback (no reconstruct `.git` inspection; scoped CAND/GEN/PROOF only).

## 7. Real409 e84 comparison (test19 verification, actual409 source3 same as delivered)

- Real409 clone `.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work` HEAD `e84a82aca000c990597ea8cf60f548e2ff187bd1` (NEW copy of 48082356, 3 runtimes + test d486). Completed with `d486809c4ae88c0e78784ade8e456cd9227b25a29c12cde9700664a1eec3edad` (18-method file) + same three runtimes as delivered.
- Compare all771 vs e84 (DATA extra outside source excluded):
```
e84 total 3104 extra 2333 missing 0
diffs 1
tests/test_evidence_scaling_v2.py CAND 7b862305 E84 d486809c
```
- Result: e84 total intended-like 3104 (771 intended +2333 DATA extra excluded), missing 0, diffs among 771 =1 ONLY `tests/test_evidence_scaling_v2.py` CAND `7b862305` vs E84 `d486809c` (additive runner test + helpers; all other 770 identical). Runtime3 same as delivered. No tests/runtime build here; composite carefully later. Real409 DATA extra (sources/2026-W34/...) excluded from source comparison.

## 8. Exclusions/limits

PartialDB `26309`/bulk `31466`/runtimeTeX unbundled; scoped `689+82` only (staged `32237` vs materialized `771`). No tests/build/import/runtime, no adoption/semantic/production, no migration/audit, no certified rerunner/globalCAS/crash-atomicity, no suite-count decoration. No driver scripts shipped (`gen-index` in WORKROOT, `/tmp` lists outside packet, not shipping source). No reapply. Source stable (`workcopy-before/after` 771/771 0 mismatch `SOURCE-STABLE`; HEAD/shallow unchanged). Old packet superseded only as above.

## 9. Failures/warnings/deviations

- `gen-diff-check` 2 + `apply` 1085B whitespace preserved (not normalized). Identical 392B diagnostics as prior, not autofixed.
- First `apply --check` 85B mode warning preserved (restoration mode gap, fixed to 775 before second check + apply; no overwrite, both checks logged uniquely).
- No `apply_patch` binary (consistent with prior); new packet files via `Write`/bash for generated artifacts (allowed). No source edits via file tools.
- Old runners read as DATA only, never executed; fresh inline procedure only.
- No wrong-cwd `apply --check` failure this round (first-round preserved in old packet, not repeated/overwritten here).
- No old PASS transferred; no behavioral tests/build run here; independent final + affected-7 verification separate. Available FINAL applied path for verifier: `.../evidence-scaling-packaging-20261103T174718Z/proof-copy/candidate-partial-b40de60` (771 files, patch applied, exits check 0/0 + apply 0/1085B). Executable/full-source binding: frozen pins §4 + manifest (all 771) + patch (139).

## 10. Scope

Checked: 3-runtime deltas +1 new test (1/771 new, 3/770 modified, 767 unchanged) + other 767 SHA/bytes identical to old manifest; saved patch/manifest FULL hash+bytes (64-char); before HEAD/tree/689/new82/clean; numeric `check0/0 + check2 0/0 + apply0/1085B` + whitespace retained; all 139 +771 byte-exact across CAND/GEN/PROOF; inherited138 inclusion; DB/inode/alternates/origin/index/packet guards; old packet intact (`efb505e4…/5247647B`, `634d41f8…/186847B` re-verified). Real409 e84 1-test delta only (d486 vs 7b86), other770 identical, DATA extra excluded.

Not checked/claimed: runtime behavior, test execution, semantic approval, production quality, full-history/tree-clean, migration/adoption, audit, whole readiness. No code/adoption PASS. Baseline774, partialDB preserved, no fake root/empty commit/config change. Stop at packaging; final review separate. WholeNOT_READY/step4B3OPEN/auditunstarted/DM021+022OPEN; quality/adoption/savings OPEN.

ProofDB: `.rephase-1-editorial-runtime/evidence-scaling-packaging-20261103T174718Z/proof-copy/candidate-partial-b40de60` (83-file `.git` +771). RAW: `indep-*.txt` + `gen-*.txt` + `workcopy-*.txt` in same packet. Patch `de0af9cbd58665dc632a53cee5a0605da30ba9cdd3dc63202268565ba9887d49/5408065B`, manifest `c5a6b230c975dc94a45e651f48cd42687f84d060c65b37f49d9917ff1bf0f143/202204B`.

(End — independent packaging owner, fail-closed.)
