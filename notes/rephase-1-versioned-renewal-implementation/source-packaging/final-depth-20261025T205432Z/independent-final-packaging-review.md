# INDEPENDENT final-depth packaging review — 20261025T205432Z (read-only, no author role)

Role: fresh independent packaging reviewer. No author role. Read-only: no source edits, no tests, no import of project code, no Git mutation, no network, no old-runner exec. Git metadata inspected read-only (`rev-parse`, `status`, `remote -v`, `ls`, `test ! -e`, file reads/hashes); no `apply`, no `add`, no `commit`, no object writes. One NEW file only: this review. No code/adoption PASS. Root stops coherent unit later after synthesis.

## Verdict: BOUNDED PASS — packaging scope only

FINAL-depth `complete-versioned-renewal-409.patch` + manifest verify exact for stated scoped delivery only. All 93 delta files and all 742 available intended worktree files byte-exact across FROZEN DST vs GEN vs PROOF (not sample-only). Apply check0/apply0 raw logs numeric-exact with preserved whitespace. Isolation/exclusion/HEAD guards hold. First-92 obsolete + inherited-57 + delivery-correction chain intact. Limitations retained; no full-hydrated/tree-clean, no safe-runner, no implementation/adoption claim.

## 1. Saved artifacts FULL hash/bytes — exact

- Patch: `notes/rephase-1-versioned-renewal-implementation/source-packaging/final-depth-20261025T205432Z/complete-versioned-renewal-409.patch`
  - `3423014 B`, SHA256 `f898d33bfe6904fd29063d5a1ff462588d11f227f5aab6a3a2d505614941da2a` — matches expected `f898d33b…da2a` / `3423014B`.
  - Independently re-hashed via `sha256sum` + `stat -c %s`; both exact.
- Manifest: `.../final-depth-20261025T205432Z/complete-versioned-renewal-manifest.json`
  - `43355 B`, SHA256 `d488c6ee48b7cfa781f39905c4f08a61561e7bd02b234d2c60a6a1e93953497c` — matches expected `d488c6ee…97c`.
  - Valid JSON, 93 entries, `delta 93 (40M+53A)`, `intended_final 742 verified true`, `patch SHA/bytes`, `proof check0/apply0 + 5959/13548B`, `heads 409b292 / 8ce36998`, `source_before_after 409 unchanged`, `gen_index_outside_packet true`.
- `manifest-gen` exit `0`, stdout `delta 93 mods=40 new=53 final=742 / 742 equality OK / patch=f898d33bfe69 3423014B`, stderr `0B`.
- `manifest-valid` exit `0`, stdout `manifest-valid OK 93 742 f898d33bfe69`, stderr `0B`.

## 2. Per-file 93 delta — all files, three trees, exact (not sample-only)

Manifest `files` count `93`; `M=40 A=53` independently recomputed from manifest.

Independent re-hash (read-only `read_bytes` + `hashlib.sha256`, no project import):
- For each of 93 `rel`, compared `SHA256 + bytes + physical_mode` against manifest for:
  - DST `…/versioned-renewal-env-20261023T185000Z/candidate-work`
  - GEN `…/versioned-renewal-packaging-final-depth-20261025T205432Z/gen-copy/candidate-partial-b40de60`
  - PROOF `…/proof-copy/candidate-partial-b40de60`
- Result: `93 entries x3 trees = 279 reads, mismatches=0`. All SHA/bytes exact; all `physical_mode == 0o664` exact (observed `0o664` on disk for all 93 in all three trees).
- Git binding: `gen-ls-files-s-stdout.txt` has `93` lines, all `100644`; dict `path -> (mode,blob)` matches manifest `git_mode/git_blob/git_blob_hash_object` for all 93, `mismatch=0`. All 93 present in `gen-ls-files-s-full` staged set.
- Key pins exact in all three worktrees (re-hashed):
  - HIGH `scripts/survey_versioned_renewal_v2.py` = `3dbdedb8b44b366b129cc351b25a8bb898a62ad23e424d27e46c3df85a6a6d0b` (FINAL, not `1dad1ad…`).
  - depth test `tests/test_survey_versioned_renewal_depth_prewrite_v2.py` = `ea2646381a41139a950deb1b6f60e6e27649beedee5ac3c4b5169c46fc63fdb8` (NEW, 5774B per manifest).
  - H `74275d22a342014009d5d090fbe9c552981941e90259c298065d2ba6929d1f3d` unchanged.
  - S `2290ddd0dc8397f86451aff70d50fd4da0c6184fcf1bef3ed96259642af2d1eb` unchanged.
- Staged diff identity:
  - `gen-diff-cached-names` 93 paths exact; `gen-names-ok` exit `0` / `gen-names-ok 93 40M+53A`.
  - `gen-diff-cached-stat`: `93 files changed, 53727 insertions(+), 608 deletions(-)`.
  - `gen-diff-cached-numstat`: 93 lines; M-file deltas present (e.g. Weekly/Special/workflows), A-files `0` deletions as expected.
  - `src-diff-names` (worktree `diff HEAD --name-only`) = 40 M paths; `src-others --exclude-standard` = `109 = 53 new + 56 __pycache__` (see §3); `src-cached-empty` exit `0` stdout empty (no original staging pre/post).

## 3. Full 742 available intended files — all files, three trees, exact

- `populate-gen-list.txt`: `742` lines, `742` unique; all manifest 93 subset (`missing 0`).
- `populate-gen-stdout`: `baseline721=721 mods=40 new=53 final=742 / copied 742`.
- `populate-proof-stdout`: `new_total=53 old32_in_baseline=32 / base689=689 / populated proof base689 / 53 absent OK`.
- Independent re-hash of every `populate-gen-list` entry across DST/GEN/PROOF: `742 x3 reads, mismatch=0` (SHA + length exact for all).
- Worktree file counts excluding `.git` (read-only `os.walk`):
  - GEN `742`, PROOF `742`, DST `798 = 742 + 56`.
  - DST extras enumerated: `56` files, all under `scripts/__pycache__/* (39)` + `tests/__pycache__/* (17)`; `non-pycache extras 0`; `notes/tmp extras []`. Exclusion of `__pycache__ 56` (LC_ALL=C, no notes/tmp/raw/bulk) holds; no fixture objects in worktrees.
- `gen-ls-files-s-full-stdout.txt`: `32208` staged entries (`32207x100644 + 1x100755`). Single `100755` is `scripts/survey_core_execution_bridge_v2.py` (`54f6bb…`) outside delta. This confirms index holds full HEAD tree while worktrees are scoped materialization — therefore NO full-hydrated/tree-clean claim (see §6).

## 4. Numeric apply/check raw logs + whitespace — preserved, not normalized

- `proof-apply-check-exit 0`, `stdout 0B`, `stderr 5959B` with `93x Checking patch …` (all 93 listed, no errors).
- `proof-apply-exit 0`, `stdout 0B`, `stderr 13548B` with `93x Checking/Applied` plus inherited content:
  - `...patch:45237: trailing whitespace.`
  - `...patch:32209: new blank line at EOF.`
  - `...patch:36088: new blank line at EOF.`
  - `...patch:45237: new blank line at EOF.`
  - `...patch:51653: new blank line at EOF.`
  - `warning: 5 lines add whitespace errors.`
- Count: `6` whitespace-related lines (1 trailing + 4 blank-EOF + 1 summary `5 lines`), matching packet claim `5 preserved`. Whitespace retained, not repaired — accepted for packaging proof.
- `proof-before-status` empty `0B` + exit `0` (clean base); `proof-before-diff-names` empty; `proof-after-diff-cached` empty `0B` + exit `0` (no `--index`, HEAD untouched); `proof-after-status` = `40M + 53 new` (pycache absent, mode fixed) matching SRC logical delta; `proof-after-head 409b292`.
- No reapply executed in this review. Raw independent proof bytes already exact for all 742 (§3); per instruction no reapply needed, and no NEW independent `apply` without root permission — readonly only.

## 5. DB origin/inode/alternates + HEAD + index isolation — read-only guards hold

- HEADs (numeric raw logs + direct read-only `rev-parse`):
  - reconstruct `f84fcf5321be3798c862c0156278afbba01f89f6` pre/post identical; `recon-status` only `?? notes/…/resume-20261025/` + `?? notes/…/source-packaging/` (no staged, no ordinary commit).
  - SRC/GEN/PROOF `409b292756dd1277b9dfae87679934c0d2ce251c` pre/post identical; `src-tree/gen-tree 8ce3699861505f32d1d60bdc185d4d4f635aedb2`.
  - Current HEAD `409` unchanged; root `f84fcf5` unchanged; no ordinary commit observed.
- GitDirs absolute-distinct: SRC `…/candidate-work/.git`, GEN `…/gen-copy/…/.git`, PROOF `…/proof-copy/…/.git`, recon `…/.git`; `*-gitdir-exit 0`.
- `*-noalternates-exit 0` (all three `test ! -e …/objects/info/alternates`); observed `.git/info` contains only `exclude/sparse-checkout`, no `alternates` file (earlier `objects/info/` path absent is expected layout variant; `info/` check is authoritative and passes).
- Origin inert (read-only `remote -v`): all three report `origin https://example.invalid/rephase-candidate-recovery.git (fetch/push)` — no real push target.
- `packet-find-git` exit `0` stdout/stderr empty — no `.git` inside packet.
- GEN index outside packet: `…/versioned-renewal-packaging-final-depth-20261025T205432Z/gen-index` exists `5770524B 0o664`; packet dir contains no `gen-index` file (only `gen-index-outside-ok*` logs, exit `0`). `src-cached-empty` + `proof-after-diff-cached` empty confirm no original staging / no index pollution.
- `cp-gen-git/cp-proof-git` exit `0` stderr empty; `gen-read-tree/gen-add/gen-diff` exits `0`; `env-check` shows sanitized `GIT_CONFIG_NOSYSTEM=1/GLOBAL=/dev/null`, `GIT_NO_LAZY_FETCH=1`, `OPTIONAL_LOCKS=0`, `PYTHONDONTWRITEBYTECODE=1`.

## 6. Lineage: first-92 obsolete, inherited-57 direct, delivery 2-file fix — intact

- First obsolete preserved untouched in parent `source-packaging/complete-versioned-renewal-409.patch`: `3415062B d6c72fb4557775691086e4b1cb804b1283b7e2864043281acd27110381771647` (matches `firstpatch-sha-stdout`, `manifest.first_obsolete`).
- Old R3 preserved: `notes/rephase-1-editorial-operation-implementation/source-packaging/complete-r3-operation-409.patch 2018112B 659063dc27f0926aaf6e8a33f322937076563c4a23f6cf0d80ca970e1b2abd5b` (matches `manifest.old_patch`).
- Baseline R7b `source-manifest-r7b.json` exists (`count 721`, `head 721a04d…`, `tree ac7cb0…`).
- Delivery correction `notes/rephase-1-versioned-renewal-implementation/resume-20261025/depth-prewrite-correction/delivery-correction.md` exists (`delivery-md-exists 0`); records HIGH `1dad1ad… -> 3dbded… +27/0` (`_require_new_chain_capacity` + ENTRY call, orphan/anchor unchanged, H742/S229 unchanged) + NEW test `ea2646…` 106 lines/6 tests, byte-for-byte transport, no other files, no commit.
- `final-pins-stdout`: `old92 diffs vs current: ['scripts/survey_versioned_renewal_v2.py'] / final pins OK: HIGH 3db, depth ea2646, H742 S229 same, only HIGH changed +1 new` — matches expected depth-3db + test-ea2646 then root delivered exact 2 files; all other 91/92 same.
- Final patch is DIRECT against `409` (`apply --check/apply --verbose` on clean `409` PROOF copy, single direct, no `--unsafe-paths`, no layered old patches); therefore direct-includes-inherited57 holds for application — no separate old-overlay layering needed for this scoped proof.

## 7. Exclusions and non-claims (retained, not waived)

PartialDB `26309`, bulk `31466` outside, runtime/TeX nonbundled retained; current observation only (no drift/globalCAS/crash-atomicity/rerunner cert); `Git100644 vs physical 0o664` separate (single `100755` bridge outside delta noted); `packet-list` complete; no tests/build/fixtures/restore/network/ordinary commit in packaging; independent review + root synthesis + audit remain separate. Do NOT claim full hydrated / tree-clean (staged `32208` vs materialized `742` proves scoping), and do NOT certify safe historical runner reuse. No reapply performed here beyond reading raw logs.

## 8. Scope statement

Checked: actual saved patch/manifest FULL hash+bytes; per-file mode/SHA/bytes for all 93 across DST/GEN/PROOF; all 742 available intended files across DST/GEN/PROOF (not sample-only); numeric `check0/apply0` + `5959/13548B` raw logs + `5` whitespace preserved; DB origin/inode/alternates + HEAD/index/packet guards read-only; first-92 obsolete + old-R3 + baseline + delivery-correction chain.

Not checked / not claimed: runtime behavior, test execution, semantic approval, production quality, full-history/tree-clean certification, migration/adoption, audit. No code/adoption PASS.
