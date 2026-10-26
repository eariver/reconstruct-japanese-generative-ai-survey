# Fixed COMBINED source snapshot for parallel Weekly/Longform verification

2026-10-25. Author-side Co-Worker source freeze ONLY. Previous snapshot `versioned-renewal-freeze-20261024T174422Z` KEEP READONLY. Writable candidate now all authors finished, root FREEZES source. Source unchanged readonly during freeze and reviews. Documentation/source inspection only. No code edits/tests/import/build/network/candidate/reconstruct commit/cleanup. No Commit Point/acceptance.

Dedicated editor: `Write`. Guard procedure saved via `Write` before `bash -n`/execution. No old runners. Read-only `AST`/`json` as data (no project imports). No full test/build.

## 1. Authority and scope

- `AGENTS.md` Human boundaries: READ ONLY `eariver/japanese-generative-ai-survey`, no branches/PRs/Issues/comments, State/decisions/Gates, Freeze/Release, deployment/Actions, adoption/migration without explicit Human authorization. Isolated fixtures only in independent Git DB, inert origin, no alternates/hardlinks/sharing/inherited root overrides. Never create fixture objects in reconstruct DB. Ordinary reconstruct commit/Push Human-owned. Pause at Commit Point, no auto next unit.
- Current task: selected renewal contract 478f0051 §11, root gate 7d7d5a45 §6 (integrated R3+R4/R5/R6 as overridden by ROOT). Requires whole selected bootstrap + U/C operation in fresh isolated scratch under `.rephase-1-editorial-runtime/`, independent DB, no inherited overrides, no reconstruct DB fixtures, no saved-runner reuse. Both routes, genuine changed-tool epochs, repeat C→U→U, renewal→editorial, normal lifecycle, failure/resume, affected regressions, independent final review.
- Reconstruct HEAD at freeze: `f84fcf5321be3798c862c0156278afbba01f89f6` (Human commit). Verified pre/post HEAD same, `diff --cached` empty, `diff HEAD` empty (no tracked mods). Status untracked-only (parallel packet files under `resume-20261025/` allowed).
- Previous snapshot KEEP READONLY: `.rephase-1-editorial-runtime/versioned-renewal-freeze-20261024T174422Z/snapshot-work`, HEAD `409b292...`, tree `8ce36998...`, status 81 (39M42U), worktree 731. Verified pre/post unchanged, no writes.

## 2. Frozen combined source (actual, not assumed)

- Writable candidate: `.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work`
  - Actual HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2` (actual409).
  - `status --porcelain=v1 --untracked-files=all`: 39 ` M` + 49 `??` raw = 88. Excluding 2 cache dirs (`scripts/__pycache__`, `tests/__pycache__`, 3 `*.pyc`): 39M+46U=85 intended. DO NOT delete cache; cache excluded from snapshot but retained in SRC.
  - Total worktree `find -path ./.git -prune -o -type f -print | wc -l` = 738 = 735 intended + 3 pyc. Total intended baseline 731+4 tests=735 confirmed actual (R7b721 + renewal10 + new4, missing 0).
  - `diff --cached` empty (index empty), `ls-files --deleted` empty, no `D` in porcelain (NO tracked deletions). H author claimed M/D: record actual not author claim — H `scripts/survey_versioned_renewal_history_v2.py` is `??` new (untracked), NOT tracked M/D; M true for 39 tracked mods (H not among them), D false.
  - `.git` 83 files, `objects/info` absent (hence `alternates` absent), remote inert `example.invalid` (no `github.com`), shallow `774dd39...`, real 409 ancestry (`log --oneline -3` starts `409b292`), no fake root.
- Pinned actual hashes (computed via `hashlib.sha256`, author suffix inconsistent → use full actual):
  - H `scripts/survey_versioned_renewal_history_v2.py` 234213B `1667c190003a114559d259f54e4c5fe8b109d98abf0246e71b8d3e6f5fa1798f`
  - S `scripts/survey_versioned_renewal_source_v2.py` 127981B `20f63eafc96923dc7be25f3f495b94dd9add0e398d6cdc2fe47c2c9bff46c306`
  - HIGH `scripts/survey_versioned_renewal_v2.py` 202862B `9a0469ef5a6bc2b2e37fc9efb1376cfccbd0333ffaa08a59d23634345d382152`
  - PUB `scripts/survey_publication_v2.py` 60268B `02f8513445b1a264fbb5172af44bf3d85a553e4fc58ebf404e9b9a028e53c365`
  - Reader `scripts/survey_reader_publication_v2.py` 46395B `098a2c8222f15f693c524139f2678be008a7ec9fafca275fc831ede9aa13bf1c`
  - +4 new dedicated tests:
    - `tests/test_versioned_renewal_history_author_h_20261025.py` 84250B `03d8acbb765dff3291f5cb6407bac865d4e441a3741bdd7ebfe1fa283e681e54`
    - `tests/test_versioned_renewal_source_author_s_f1f2f3_20261025.py` 51552B `995080e49c654ff59bc02290eccf2b844265ae56610ff37c057d8cf71d597124`
    - `tests/test_versioned_renewal_operation_correction_b1b2b3.py` 16147B `37766d6bbdcf3665500cac1d195977976be877bafbe06ccd93613f27c0f83070`
    - `tests/test_versioned_renewal_reader_f4_20261025.py` 9916B `58e33ccacb77e8e077ebc642b1d293e8990c810d98ff0c20651a326dee7cca6f`
- Baseline deltas:
  - From actual409: 39M+46U intended (raw 49U incl cache), total 85 intended (88 raw). `M_list` 39, `U_list` 46 (baseline32+renewal10+new4). All intended U `.py`/`.json`, JSON valid, AST parse OK (stdlib only).
  - From baseline57 (25M32A=57): extra 14M + 10+4 new U. Extra M list (14): `publication-candidate/quality-regression` schemas +12 scripts `architecture*2/bibliography/completeness/discovery/drafting*2/evidence/publication/quality/screening/x_intake`. New U 14 = renewal10 + new4.
  - Current recipe.style input classification H fix old commit; root file 7d bound map unchanged (contract/root gate as above).
- Outlier/cache class: 2 dirs `scripts/__pycache__`, `tests/__pycache__`, 3 `*.pyc` listed in manifest. Observed in root status, DO NOT delete, excluded from DST (DST has 0 cache, verified). DST 735 files, no cache.

## 3. NEW combined immutable snapshot

- Fresh unique id: `20261025T041436Z` (after `174422Z` freeze, `ls` parent verified, no overwrite).
- Path: `.rephase-1-editorial-runtime/versioned-renewal-combined-freeze-20261025T041436Z/snapshot-work/`
  - Absolute: `/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-combined-freeze-20261025T041436Z/snapshot-work`
  - HEAD `409b292...`, tree `8ce36998...` (same as SRC), index clean, status 39M46U intended (raw 46U, DST has no cache), worktree 735 exact, all 735 SHA/bytes SRC==DST identical, `dst-hash-intended` SHA256 `ad1f6da99e32a133477877a1ab143dc38f1585e0f06d3e346528610660efa416` (735 lines).
  - Modes: Git `100644` (734) +`100755` (1 `survey_core_execution_bridge_v2.py`), physical `0o664` (734) +`0o775` (same 1), recorded separately (umask 002).
  - Real ancestry, shallow `774`, inert remote, no new commits (HEAD still 409, no fake-root candidate). Future meaningful synthetic fixture SOURCE commits must be in NEW independent DB before authorities, NOT this snapshot. Fixed test SOURCE separately NOT needed here — route workers clone REAL old bootstrap HEAD `721a04d`+oldE then overlay this COMBINED intended source 735 and meaningful SOURCE commit ONLY code before NEW authority (preserve old tool ancestry).
- Provenance: byte-independent `.git` copy via `cp -a SRC/.git DST/.git` (no `-l`), `.git` 83/83, no `objects/info`, inert remote, own absolute gitdir, full `.git`+worktree `dev:ino` disjoint, `nlink==1` (no hardlinks). No inherited `GIT_*`. Worktree populated ONLY via R7b721+10+4new intended list (735) with `shutil.copy2` (no `rsync` blind, no cache copy). Each file SHA/bytes verified post-copy and SRC==DST.
- Procedure saved BEFORE execution via `Write`: `integrated-source-freeze-evidence-20261025T041436Z/make_combined_freeze_20261025T041436Z.sh` (`bash -n` 0, every invocation captured to `*-stdout.txt`/`*-stderr.txt`/`*-exit.txt`, `commands.log` `DONE OK`, `set -u` only, explicit rc, pre-checks before `mkdir DST`, fail-closed, no network/old runners/restore).

## 4. Runtime/tools

- `python3` `/usr/bin/python3` 3.14.4, `jsonschema` 4.23.0, `PYTHONDONTWRITEBYTECODE=1` (no `__pycache__` created in DST/packet).
- `git` 2.53.0, sanitized `GIT_NO_LAZY_FETCH=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_OPTIONAL_LOCKS=0`, `git --no-optional-locks`, no inherited `GIT_DIR`/`WORK_TREE`/`INDEX_FILE`.
- `TeX` NOT on `PATH`; local-only `/tmp/opencode/jgas-texlive-...`, not run, no PDF. `pytest` absent, `pip` present NOT used. No candidate project import, no tests/build in freeze.

## 5. Evidence (no DB in notes)

- `integrated-source-freeze-evidence-20261025T041436Z/` — authoritative raw outputs + `commands.log` (`DONE OK 20261025T041436Z`), including recon/prev/src/dst guards, `combined-verify`, `hash-intended`, `isolation`, `noalternates/config/env`, pre/post hashes (all `exit 0`).
- `integrated-source-freeze.json` — machine manifest (base/tree/delta/files/modes, ancestry, tools, evidence, limitations, ROOT corrections).
- This file `integrated-source-freeze.md` (NEW). Previous `manifest.json`/`source-freeze.md` and old failures (`source-freeze-evidence-20261024T174224Z/` FAIL preserved) untouched — DO NOT overwrite.

## 6. Limitations and next

- PartialDB 26309 missing retained, bulk 31466 outside scope, not full-history cert. Scoped 735, NOT full-tree clean claim. Runtime unbundled. Modes recorded separately. No new authority (HEADs still 409, no candidate/reconstruct commit, no Gate/Candidate/State/Preview/Freeze/Release, no Human approval).
- No fresh network restore; no fixture objects in reconstruct DB; no cleanup (cache retained in SRC, excluded from DST).
- Next for parallel Weekly/Longform verification (root to delegate, NOT executed here): route workers clone REAL old bootstrap HEAD `721a04d`+oldE then overlay this COMBINED 735 and meaningful SOURCE commit ONLY code before NEW authority. Use this snapshot `/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-combined-freeze-20261025T041436Z/snapshot-work` as read-only source.
- Representative-quality/Profile/adoption/savings OPEN; whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN.

Stop here. Human Commit Point preserved. Ordinary Commit/Push Human-owned. This freeze is NOT whole-unit completion and NOT acceptance.
