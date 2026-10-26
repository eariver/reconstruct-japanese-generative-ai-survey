# FINAL-depth COMPLETE versioned-renewal source packaging — 20261025T205432Z UTC (FINAL, ROOT FROZEN)

Role: bounded final packaging Worker, NOT reviewer/root. No edits/tests/build/network/commit/clean.
First 92 `d6c72fb45577…` 3415062B / 741 COMPLETED but OBSOLETE (HIGH 1dad, missing depth test), preserved untouched in parent `source-packaging/` (no overwrite). This FINAL is the ROOT-FROZEN selected delivery.

## Delivery fix (only 2 changed vs first)

- `resume-20261025/depth-prewrite-correction/delivery-correction.md`: writable candidate was stale (HIGH 1dad, missing test). Transported EXACT tested bytes via dedicated editor, no new logic:
  - `scripts/survey_versioned_renewal_v2.py` `1dad1ad12ba509c…` → `3dbdedb8b44b366b129cc351b25a8bb898a62ad23e424d27e46c3df85a6a6d0b` (+27/0 guard `_require_new_chain_capacity` + ENTRY call, orphan/anchor unchanged, H742/S229 unchanged).
  - `tests/test_survey_versioned_renewal_depth_prewrite_v2.py` NEW `ea2646381a41139a950deb1b6f60e6e27649beedee5ac3c4b5169c46fc63fdb8` (106 lines, 6 tests, tested32/33 byte-identical).
- Verified: `final-pins` asserts HIGH 3db + depth ea2646 + H742 + S229 + `old92 diffs == [HIGH]` only. All other 91/92 same.

## Exact delta vs actual409

- `40M+53A=93` (LC_ALL=C, `__pycache__` 56 excluded, no notes/tmp/raw/bulk). `40M` same paths as first (HIGH now 3db bytes); `53A` = first 52 + depth test.
- Intended final `742 = 689 +53 = 721 +21` (baseline721 + 20 first-new + depth test). Scoped clean `689 at HEAD +53 absent →742`.

## Method (NEW script, no reuse, no prior errors)

- Script: `package_final_depth_20261025T205432Z.sh` (this dir, Write-before-exec, `bash -n` 0). No saved-runner reuse. Correct `git -C PROOF apply --check/apply --verbose` (no `--unsafe-paths` flag, no `--git-dir/--work-tree` relative-path inconsistency; all paths closed manifest, no bypass needed).
- Sanitized `GIT_*` unset, `GIT_NO_LAZY_FETCH=1`, `NOSYSTEM/GLOBAL=/dev/null`, `OPTIONAL_LOCKS=0`, `PYTHONDONTWRITEBYTECODE=1`. No fetch/network.
- PACKROOT (ignored): `.rephase-1-editorial-runtime/versioned-renewal-packaging-final-depth-20261025T205432Z/` with `gen-copy/`, `proof-copy/`, absolute `gen-index` outside packet. `cp -a SRC/.git` only, `shutil.copy2` (GEN) / `git show + chmod 775/664` (PROOF base) for 689, verified `remote` inert, `alternates` absent, own GitDir ≠ SRC/reconstruct, `packet-find-git` empty. Never staged candidate/reconstruct (`src diff --cached` empty pre/post).
- GEN: `read-tree HEAD` → `add -- 93 ONLY` → `diff --cached --name-only` verified `93 40M+53A` (`gen-names-ok` 0) → `ls-files -s --93` (all `100644`) → `diff --cached --binary HEAD` → SAVED patch (0, `gen-diff-stderr` 0B).
- PROOF: populated 689 HEAD bytes (executable preserved 775/664), verified `53 absent OK`, `status` clean (mode fixed), `diff HEAD --name-only` empty for base. Applied SAVED: `apply --check --verbose` (0, 5959B 93 Checking) then `apply --verbose` (0, 13548B 93 Checking/Applied + inherited trailing at 45210 + 4 blank-EOF + `5 whitespace errors`), single direct clean409, no `--index` (so `diff --cached` empty after). Validated `742/742` SHA equality (`manifest-gen` 0), HEAD stays 409.

## Outputs (this dir, FINAL)

- Patch: `complete-versioned-renewal-409.patch` — 3423014 B, SHA256 `f898d33bfe6904fd29063d5a1ff462588d11f227f5aab6a3a2d505614941da2a`. `93 files`.
- Manifest: `complete-versioned-renewal-manifest.json` — FULL valid JSON (93 entries path/SHA256/bytes/Git mode/blob/hash-object/physical mode/M-A/old_head_blob + heads/trees, intended 742 verified, patch SHA/bytes, proof check0/apply0, first-obsolete `d6c72fb…` recorded, delivery-correction pointer, source pre/post 409 unchanged). SHA256 `d488c6ee48b7cfa781f39905c4f08a61561e7bd02b234d2c60a6a1e93953497c`, 43355 B. `manifest-valid` 0 (`93 742 f898d33bfe69`).
- GEN: `/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-packaging-final-depth-20261025T205432Z/gen-copy/candidate-partial-b40de60` + `.../gen-index`.
- PROOF: `.../proof-copy/candidate-partial-b40de60` (689→742, check0/apply0).
- No tests executed (packaging only; depth bytes already tested32/33 in fixture, NOT re-run here).

## Pins / source identity

- DST FINAL: `.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work`, `409b292…` / `8ce36998…`, `40M53A93`.
- Baseline721 + old57 `659063dc…` + first-obsolete `d6c72fb…` preserved.
- FINAL code: HIGH `3dbdedb8b44b366b129cc351b25a8bb898a62ad23e424d27e46c3df85a6a6d0b`, H `74275d22…`, S `2290ddd0…`, P1 `825dba1d…`, PUB `3f4039…`, Reader `098a…`, edpub `85814124…`, P3S `9e2a…`, R1 `52e15457…`, ReaderF4 `63323adc…`, depth `ea2646…`.

## Limitations (inherited, not waived)

PartialDB26309, bulk31466 outside, runtimeTeX unbundled, current observation only, no drift/globalCAS/rerunner, whitespace preserved, Git100644 vs physical0o664 separate, no new authority/commit, independent review/root synthesis separate.

## STOP

FINAL-depth patch complete (93/742, check0/apply0). No commit/push. Next independent review + audit. Ordinary Commit/Push Human-owned. No CommitPoint/PASS/adoption claimed.
