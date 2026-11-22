# COMPLETE DIRECT409 packaging — final-20261122T114000Z (delivery-bound source/run composite)

Source: `e59fa9bc5f323a640fd922412de7757e60eb5944` parent `d591` tree `e5e8...` (full, no prefix, no f591). Base actual409 head `409b292756dd1277b9dfae87679934c0d2ce251c` tree `8ce36998...` (genuine prior proof DB, read-only copy, no fake root). No reconstruct Git/status/log/HEAD/readback, no ordinary commit/push, no network/Production/configHOME/source edits. SOURCE FROZEN.

## Freeze + isolation (ignored runtime, fresh DBs)

- GEN `.rephase-1-editorial-runtime/prior-artifact-reader-packaging-20261122T114000Z/gen-copy/candidate-partial-b40de60`: base `.git` byte-copied `rsync -a` (no `-H`, no hardlinks) + intended775 files only (`shutil.copyfile` + `chmod` from CAND, no `__pycache__`/`*.pyc`, no bulk/sources/material/DBs). Inodes differ vs CAND/BASE, no `alternates`/`commondir`, inert origin preserved (no set-url/config). `gen-index` TEMP outside packet. HEAD `409b292...`/tree `8ce36998...` verified. GEN==CAND 775/775 (7 pins OK), 0 mismatch.
- PROOF `.rephase-1-editorial-runtime/prior-artifact-reader-packaging-20261122T114000Z/proof-copy/candidate-partial-b40de60`: separate base `.git` byte-copy, NEW fail-closed restore via `git show HEAD:<path>` for 689 (`proof-restore689-exit.txt` 0, `RESTORED 689/689`), correct physical modes (775 bridge `survey_core_execution_bridge_v2.py`, else 664) BEFORE check. Before: 689 present, 86 new absent (checked), `vs HEAD mismatch 0`.

## Measured actuals (computed, not assumed)

- Intended **775** = 689 tracked + 86 new. Worktree intended 775, missing 0, extra 0 (scoped, not hydrated/tree-clean).
- Delta **58M+86A=144** (`diff --cached --name-status HEAD`: 86A/58M/0D/R exit 0, `names` 144). Prior143 (58M+85A) preserved +1A new test `test_prior_artifact_reader_repair_v2.py` + stage update within existing M (`survey_stage_validation_v2.py` `ec15f5ba.../49688B` → `1e4c818b.../51927B`, still M). Unchanged inherited: all old143 in new144 (0 missing). Base689: `ls-tree` 689, `cat-file -e` 0 missing. Bulk missing26309/bulk31466/runtimeTeX nonbundled qualified. No `.tmp`/`*~`. Git 774×`100644`→`0o664` +1×`100755`→`0o775`, 0 mismatch. Physical 0/775 mismatch.
- Harness `run_packaging.py` NEW via Write only (no shell text editing), executed with `PYTHONDONTWRITEBYTECODE=1 GIT_NO_LAZY_FETCH=1`, cleaned `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null`.

## Delivery artifacts (NEW unique packet, old intact)

- `complete-prior-artifact-reader-409.patch` — SHA256 `f032097389ad39f92cd5f1753b176cc3d89278d67fbc096b040091804f51ea39` /5724474B. ONE complete actual409-relative full-index binary patch (`git diff --cached --full-index --binary HEAD` temp index): 144 files. Covers ALL current deltas INCLUDING inherited final143 + stage `1e4c...` + new test `1fb8...`; 0 missing; no incremental layer, no old overlay.
- `complete-prior-artifact-reader-manifest.json` — SHA256 `aa54944ff032450fc4cb5701668c6b5ad01a53b3000c73b078292ac27bcbdb15` /187642B. All 775 intended `{SHA256, bytes, git_mode, physical_mode, kind}` + delta (`diff_M` 58, `new_A` 86). Full 64-char, no typos. Source identity `e59.../d591/e5e8...` from observed Git (no hand f591/prefix).
- Raw: `gen-*`, `proof-*`, `indep-*`, `patch-*`, `manifest-*`, `gen-counts.json`, `source-identity.txt`, `inode-*.txt`. No Git DB in packet.

## Independent proof (NEW separate DB, clean 689, correct mode BEFORE check)

- `RESTORED 689/689` exit 0. Before: 689, new86 absent86/86, `vs HEAD mismatch 0`.
- `apply --check` exit 0 0B/0B clean, actual `apply --verbose` ONCE exit 0 with whitespace preserved (`trailing whitespace` + `new blank line at EOF` + verbose checking, see `indep-apply-stderr.txt`). No `no warnings` claim. `gen-diff-check` exit 2 with whitespace (`trailing whitespace` + `new blank line at EOF`, same family as prior, preserved not normalized). No mode-warning repeat (correct 775 BEFORE check, no `--whitespace=fix`, no `--reject`). Correct cwd `proof-copy/...` for all apply calls (no wrong-cwd).
- Full 775+144: proof775, manifest775, missing 0, unexpected 0; content 0/775 CAND/GEN/PROOF/manifest; physical0/775; gitmode1×755 rest644; delta57? No, delta M58 A86 `delta_ok True`; `FULLVERIFY-OK`:
```
CAND 775 GEN 775 PROOF 775 MANIFEST 775
only_c 0 only_g 0 only_p 0
mismatch CG 0 CP 0 CM 0 PM 0
delta M 58 A 86 delta_ok True
FULLVERIFY-OK
```
- DB/inode: `cand775/gen775/proof83` (base 83), overlap 0/0/0 `INODE-SEPARATION-OK`. No symlinks, no `160000` gitlinks, no alternates/commondir, inert origin, no `git config`. No reconstruct HEAD/status/log/readback.

## Exclusions/limits/failures

- PartialDB `26309`/bulk `31466`/runtimeTeX unbundled; scoped `689+86` only (staged `32240?` vs materialized `775`), not hydrated/tree-clean. No tests/build/import/runtime, no adoption/semantic/production, no migration/audit, no certified rerunner/globalCAS/crash-atomicity, no suite-count decoration. No driver scripts shipped (`gen-index` in WORKROOT). No reapply. Source stable.
- `diff-check` exit 2 + `apply` whitespace preserved (trailing + blank-EOF, same family as prior). No mode-warning repeat (correct 775 BEFORE check). No wrong-cwd failure. No old PASS transferred; affected 8/10 + CURRENT proof separate, no behavioral tests here. Available FINAL applied path: `.rephase-1-editorial-runtime/prior-artifact-reader-packaging-20261122T114000Z/proof-copy/candidate-partial-b40de60` (775 files, check0 + apply0). Old prefinal/final139/773/774 preserved, not overwritten.
- No blind copy of author untracked files (only intended775). Excluded old temporary runners/test fixtures/materials. States/Profiles real untouched.
- Verification 8/10 STOP preserved (2 failures require root triage, source unchanged). This packaging does not claim verification PASS; independent final review will judge bounded reader repair separately from real W34 still incomplete.

## Scope

Checked: 2-file final deltas (stage `1e4c818b...` + test `1fb83167...`) + other773 identical to old774 except stage; saved patch/manifest FULL hash+bytes (64-char); before HEAD/tree/689/86new/clean; numeric `check0 + apply0` + whitespace retained; all144+775 byte-exact CAND/GEN/PROOF; inherited old143 inclusion; DB/inode/alternates/origin/index/packet guards. Whole NOT_READY/step4B3OPEN/auditunstarted/DM021+022OPEN; quality-adoption-savings OPEN.

ProofDB: `.rephase-1-editorial-runtime/prior-artifact-reader-packaging-20261122T114000Z/proof-copy/candidate-partial-b40de60` (83-file `.git` +775). Patch `f03209.../5724474B`, manifest `aa54944f.../187642B`.
