# FINAL INTEGRATION INPUT snapshot (not final implementation acceptance)

2026-10-25. All authors now done, root FREEZES actual candidate again. Author-side Co-Worker source freeze ONLY. DO NOT blindly use previous735 snapshot+Honly — PUB changed too. Source unchanged readonly during freeze and reviews. Documentation/source inspection only. No code/test/PASS/CommitPoint. No project imports/tests/build/network/ordinary commits.

Dedicated editor: `Write`. Guard procedure saved via `Write` before `bash -n`/execution. No old runners. Read-only `AST`/`json` as data (no project imports).

## 1. Authority and scope

- `AGENTS.md` Human boundaries: READ ONLY `eariver/japanese-generative-ai-survey`, no branches/PRs/Issues/comments, State/decisions/Gates, Freeze/Release, deployment/Actions, adoption/migration without explicit Human authorization. Isolated fixtures only in independent Git DB, inert origin, no alternates/hardlinks/sharing. Never create fixture objects in reconstruct DB. Ordinary reconstruct commit/Push Human-owned. Pause at Commit Point.
- Current task: selected renewal contract 478f0051 §11, root gate 7d7d5a45 §6 (integrated R3+R4/R5/R6 as overridden by ROOT). Parent old 721 meaningful source ancestry and actual candidate 409 separate same before (R7b `721a04d` + oldE for route workers; actual candidate `409b292` for INPUT).
- Reconstruct HEAD at freeze: `f84fcf5321be3798c862c0156278afbba01f89f6` (Human commit). Verified pre/post HEAD same, `diff --cached` empty, `diff HEAD` empty (no tracked mods). Status untracked-only (parallel packet files allowed).
- Previous snapshots immutable, no cleanup: `versioned-renewal-freeze-20261024T174422Z` (731, 81) and `versioned-renewal-combined-freeze-20261025T041436Z` (735 intended, now observed 764 total incl cache residue from test runs). Recorded actual, left untouched.

## 2. Frozen combined+perf INPUT (actual, not assumed)

- Writable candidate: `.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work`
  - Actual HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`.
  - `status --porcelain=v1 --untracked-files=all`: 39 ` M` + 52 `??` raw = 91. Excluding pycache (2 dirs, 5 `*.pyc`): 39M+47U=86 intended. Total worktree `find -path ./.git -prune -o -type f -print | wc -l` = 741 = 736 intended +5 pyc. Total intended 736 = prior735+1 confirmed actual (R7b721 + renewal10 + prev4 + new1 perf, missing 0).
  - `diff --cached` empty (index empty), `ls-files --deleted` empty, no `D` in porcelain (NO tracked deletions). Record actual source intent only.
  - `.git` 83 files, `objects/info` absent, remote inert `example.invalid`, shallow `774dd39...`, real 409 ancestry, no fake root.
- Pinned actual hashes (computed via `hashlib.sha256`, full values control):
  - H `scripts/survey_versioned_renewal_history_v2.py` 277869B `70bcdbb8602dd012cd300eba3e9972735ea5dd29e52cfb76e59cee6605230467` (perf-batched current; author 37cb vs 8f before perf inconsistent — declare observed full current, NOT adopt mistyped prefix; current perf hash 70bc source controls combined)
  - S `scripts/survey_versioned_renewal_source_v2.py` 127981B `20f63eafc96923dc7be25f3f495b94dd9add0e398d6cdc2fe47c2c9bff46c306`
  - HIGH `scripts/survey_versioned_renewal_v2.py` 202862B `9a0469ef5a6bc2b2e37fc9efb1376cfccbd0333ffaa08a59d23634345d382152`
  - PUB `scripts/survey_publication_v2.py` 92396B `90d90738dc2fc0c57a22f9656659a6e3665d262919b17f259811d035dac3d8c6` (changed 02f85134→90d90738; confirms cannot reuse prev735+Honly)
  - Reader `scripts/survey_reader_publication_v2.py` 46395B `098a2c8222f15f693c524139f2678be008a7ec9fafca275fc831ede9aa13bf1c`
  - NEW `tests/test_versioned_renewal_history_perf_batched_20261025.py` 20245B `3bcdf04daba83a327ccc554e166183e437d7c175cad2cd292ab8e18f99a49a26`
  - All 47 intended U `.py`/`.json`, JSON valid, AST parse OK (stdlib only). 85→86 delta = +1 perf test class (list in manifest).
- Baseline deltas: from actual409 39M+47U=86 (52 raw incl cache); from baseline57 14 extra M +15 new U (renewal10+prev4+new1). Current recipe.style input classification H fix old commit; root file 7d bound map unchanged.
- Outlier/cache class: 2 dirs `scripts/__pycache__`, `tests/__pycache__`, 5 `*.pyc` listed in manifest. Observed in root status, DO NOT delete, excluded from DST (DST 0 cache).

## 3. NEW INPUT snapshot

- Fresh unique id: `20261025T051343Z` (ls parent verified, no overwrite).
- Path: `.rephase-1-editorial-runtime/versioned-renewal-final-input-20261025T051343Z/snapshot-work/`
  - Absolute: `/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-final-input-20261025T051343Z/snapshot-work`
  - HEAD `409b292...`, tree `8ce36998...`, index clean, status 39M47U intended (raw 47U, DST no cache), worktree 736 exact, all 736 SHA/bytes SRC==DST identical, `dst-hash-intended` SHA256 `d7d7f6df0bbde842c0270d00f493b01e5be2d19fd48ccae56086f5cf4ca3a129` (736 lines).
  - Modes: Git `100644` (735) +`100755` (1 bridge), physical `0o664` (735) +`0o775` (same 1), recorded separately.
  - Real ancestry, shallow `774`, inert remote, no new commits (HEAD still 409). Read-only after (no edits). Route workers will clone old R3 baseline721+E, overlay this INPUT manifest exact list (736) source-only commit before NEW renewal, then fresh Python child per Core epoch; they will NOT edit shared candidate or INPUT.
- Provenance: byte-independent `.git` copy via `cp -a` (no `-l`), 83/83, no `objects/info`, own absolute gitdir, full `.git`+worktree `dev:ino` disjoint, `nlink==1`. No inherited `GIT_*`. Worktree via R7b721+10+4+1new intended list (736) with `shutil.copy2` (no `rsync` blind, no cache).
- Procedure saved BEFORE execution via `Write`: `final-integration-input-evidence-20261025T051343Z/make_final_input_20261025T051343Z.sh` (`bash -n` 0, every invocation to `*-stdout.txt`/`*-stderr.txt`/`*-exit.txt`, `commands.log` `DONE OK`, `set -u` only, explicit rc, fail-closed, no network/old runners/restore).

## 4. Runtime/tools

- `python3` 3.14.4, `PYTHONDONTWRITEBYTECODE=1`, `git` 2.53.0 sanitized, no inherited `GIT_*`. `TeX` NOT on `PATH` (local-only, not run). `pytest` absent, `pip` present NOT used. No candidate project import, no tests/build in freeze.

## 5. Evidence (no DB in notes)

- `final-integration-input-evidence-20261025T051343Z/` — authoritative raw outputs + `commands.log` (`DONE OK 20261025T051343Z`), including recon/prev731/prev735/src/dst guards, `final-verify`, `hash-intended`, `isolation`, `noalternates/config/env`, pre/post hashes (all `exit 0`).
- `final-integration-input.json` — full manifest (per-file bytes/modes/SHA via `dst-hash-intended`, 85→86 delta, new test class/list, source pre/post guards, current HEAD/index/status source intent only).
- This file `final-integration-input.md` (NEW). Existing `manifest.json`, `integrated-source-freeze.json`, `source-freeze.*` and old failures preserved — don't overwrite.

## 6. Limitations and next

- PartialDB 26309 missing retained, bulk 31466 outside scope, not full-history cert. Scoped 736, NOT full-tree clean claim. Runtime unbundled. Modes recorded separately. No new authority (HEADs still 409, no candidate/reconstruct commit, no Gate/Candidate/State/Preview/Freeze/Release, no Human approval).
- No fresh network restore; no fixture objects in reconstruct DB; no cleanup (cache retained in SRC, excluded from DST; old snapshots untouched).
- Next for parallel Weekly/Longform verification (root to delegate, NOT executed here): route workers clone old R3 baseline721+E, overlay INPUT exact 736 list source-only commit before NEW renewal, then fresh Python child per Core epoch; will NOT edit shared candidate or INPUT. Fast bounded setup: use INPUT absolute path + full manifest pin `d7d7f6df0bbde842c0270d00f493b01e5be2d19fd48ccae56086f5cf4ca3a129` (736 lines) + per-file bytes/modes in evidence.
- Representative-quality/Profile/adoption/savings OPEN; whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN.

Stop here. Human Commit Point preserved. Ordinary Commit/Push Human-owned. This INPUT is NOT final implementation acceptance and NOT a Commit Point.
