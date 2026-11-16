# COMPLETE DIRECT409 packaging — final-20261116T031000Z (delivery-bound source/run composite)

Source: 3231a0c280287411513bba359f4d3d2b6703f591 parent ae0dd1e tree ff01b73e. Base actual409 head `409b292756dd1277b9dfae87679934c0d2ce251c` tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2` (genuine prior proof DB, read-only copy, no fake root). No reconstruct Git/status/log/HEAD/readback, no ordinary commit/push, no network/Production/configHOME/source edits. SOURCE FROZEN.

## Freeze + isolation (ignored runtime, fresh DBs)

- GEN `.rephase-1-editorial-runtime/selection-scaling-packaging-20261116T031000Z/gen-copy/candidate-partial-b40de60`: base `.git` byte-copied `rsync -a` (no `-H`, no hardlinks) + intended774 files only (`shutil.copyfile` + `chmod` from CAND, no `__pycache__`/`*.pyc`, no bulk/sources/material/DBs). Inodes differ vs CAND/BASE, no `alternates`/`commondir`, inert origin preserved (no set-url/config). `gen-index` TEMP outside packet. HEAD `409b292…`/tree `8ce36998…4f…` verified. GEN==CAND 774/774 (5 pins OK), 0 mismatch.
- PROOF `.rephase-1-editorial-runtime/selection-scaling-packaging-20261116T031000Z/proof-copy/candidate-partial-b40de60`: separate base `.git` byte-copy, NEW fail-closed restore via `git show HEAD:<path>` for 689 (`proof-restore689-exit.txt` 0, `RESTORED 689/689`), correct physical modes (775 bridge `survey_core_execution_bridge_v2.py`, else 664) BEFORE check. Before: 689 present, 85 new absent (checked). Correct cwd `proof-copy/...` for all apply calls (no wrong-cwd).

## Measured actuals (computed, not assumed)

- Intended **774** = 689 tracked + 85 new. Worktree intended 774, missing 0, extra 0 (scoped, not hydrated/tree-clean).
- Delta **58M+85A=143** (`diff --cached --name-status HEAD`: 85A/58M/0D/R exit 0, `names` 143). Old141 (57M+84A) preserved +1M (attention `survey_review_attention_v2.py` tracked→modified) +1A (new test `test_selection_scaling_repair_v2.py`) + LOW SHA update within A (`survey_research_authority_v2.py` still A vs BASE, `fd788b74…` vs old `7f5fc9e0…`) + runner/base SHA updates within M. Insertions/deletions via `numstat/stat` (see raw). Unchanged inherited: all old139/141 in new143 (0 missing). Base689: `ls-tree` 689, `cat-file -e` 0 missing. Bulk missing26309/bulk31466/runtimeTeX nonbundled qualified. No `.tmp`/`*~`. Git 773×`100644`→`0o664` +1×`100755`→`0o775`, 0 mismatch. Physical 0/774 mismatch.
- Harness `run_packaging.py` NEW via Write only (no shell text editing), executed with `PYTHONDONTWRITEBYTECODE=1 GIT_NO_LAZY_FETCH=1`, cleaned `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null`.

## Delivery artifacts (NEW unique packet, old intact)

- `complete-selection-scaling-409.patch` — SHA256 `76ac1318cd58311a5a7c0d924ee26b2bdff68dc815e75014a1aacd517e51fd6b` / 5691014B. ONE complete actual409-relative full-index binary patch (`git diff --cached --full-index --binary HEAD` temp index): 143 files. Covers ALL current deltas INCLUDING inherited final141 + LOW/attention/runner/base + test; 0 missing; no incremental layer, no old overlay.
- `complete-selection-scaling-manifest.json` — SHA256 `0dc361cb8284f3465243120b7cea8e20476c3fbe81d90a71ce3028dd43eed150` / 187361B. All 774 intended `{SHA256, bytes, git_mode, physical_mode, kind}` + delta (`diff_M` 58, `new_A` 85). Full 64-char, no typos.
- Raw: `gen-*`, `proof-*`, `indep-*`, `patch-*`, `manifest-*`, `gen-counts.json`, `inode-*.txt`. No Git DB in packet.

## Independent proof (NEW separate DB, clean 689, correct mode BEFORE check)

- `RESTORED 689/689` exit 0. Before: 689, new85 absent85/85, `vs HEAD mismatch 0`.
- `apply --check` exit 0 0B/0B clean (no warning, mode already correct; no `--whitespace=fix`, no `--reject`). Actual `apply --verbose` ONCE exit 0 with whitespace preserved (`trailing whitespace` + `5 lines add whitespace errors` + verbose checking, see `indep-apply-stderr.txt`). No `no warnings` claim.
- Full 774+143: proof774, manifest774, missing 0, unexpected 0; content 0/774 CAND/GEN/PROOF/manifest; physical0/774; gitmode1×755 rest644; delta57→58/84→85; `FULLVERIFY-OK`:
```
CAND 774 GEN 774 PROOF 774 MANIFEST 774
only_c 0 only_g 0 only_p 0
mismatch CG 0 CP 0 CM 0 PM 0
delta M 58 A 85 delta_ok True
FULLVERIFY-OK
```
- DB/inode: `cand774/gen774/proof83` (base 83), overlap 0/0/0 `INODE-SEPARATION-OK`. No symlinks, no `160000` gitlinks, no alternates/commondir, inert origin, no `git config`. No reconstruct HEAD/status/log/readback.

## Exclusions/limits/failures

- PartialDB `26309`/bulk `31466`/runtimeTeX unbundled; scoped `689+85` only (staged `32239+1=32240?` vs materialized `774`), not hydrated/tree-clean. No tests/build/import/runtime, no adoption/semantic/production, no migration/audit, no certified rerunner/globalCAS/crash-atomicity, no suite-count decoration. No driver scripts shipped (`gen-index` in WORKROOT). No reapply. Source stable.
- `diff-check` exit 2 + `apply` whitespace preserved (trailing + blank-EOF, same family as prior). No mode-warning repeat (correct 775 BEFORE check). No wrong-cwd failure. No old PASS transferred; affected 10/10 + CURRENT proof separate, no behavioral tests here. Available FINAL applied path: `.rephase-1-editorial-runtime/selection-scaling-packaging-20261116T031000Z/proof-copy/candidate-partial-b40de60` (774 files, check0 + apply0). Old prefinal/final139/773 preserved, not overwritten.
- No blind copy of author untracked files (only intended774). Excluded old temporary runners/test fixtures/materials. States/Profiles real untouched.

## Scope

Checked: 5-file final deltas (LOW `fd788b74…`, runner `b16c4759…`, base `b3cd4a95…`, attention `10126da7…` + test `a21f5949…`) + other769 identical to old771/773 except those; saved patch/manifest FULL hash+bytes (64-char); before HEAD/tree/689/new85/clean; numeric `check0 + apply0` + whitespace retained; all143+774 byte-exact CAND/GEN/PROOF; inherited old141 inclusion; DB/inode/alternates/origin/index/packet guards. WholeNOT_READY/step4B3OPEN/auditunstarted/DM021+022OPEN; quality-adoption-savings OPEN.

ProofDB: `.rephase-1-editorial-runtime/selection-scaling-packaging-20261116T031000Z/proof-copy/candidate-partial-b40de60` (83-file `.git` +774). Patch `76ac1318…/5691014B`, manifest `0dc361cb…/187361B`.
