# Versioned renewal — source-complete immutable-for-review snapshot (BEFORE parallel review/test)

2026-10-24. Author-side Co-Worker source freeze ONLY. No implementation edits/tests/build/project imports/network/ordinary candidate or reconstruct commit. Source FROZEN root no authors writing during round. This unit is documentation/source inspection only.

Dedicated editor used: `Write` (no `apply_patch`). Guard procedures saved via `Write` before `bash -n`/execution. No shell heredoc file edits. No old runners. Read-only `AST`/`json` validation as data (no project imports). No full test/build.

## 1. Authority and scope read

- `AGENTS.md` Human boundaries: `eariver/japanese-generative-ai-survey` READ ONLY, no branches/PRs/Issues/comments, State/decisions/Gates, Freeze/Release, deployment/Actions, adoption/migration without explicit Human authorization. Isolated fixture objects only in independent Git DB, inert origin, no alternates/hardlinks/object sharing/inherited Git-root overrides. Never create fixture objects in reconstruct DB. No fixture objects/refs/commits in reconstruct. Ordinary final reconstruct commit/Pull/Push Human-owned. Pause at Commit Point, no auto next unit.
- Current renewal task: `outputs/rephase-1-versioned-renewal-precode-assessment.md` PRE_CODE_READY bounded design/interface map ONLY (contract 478f0051 §11 unchanged, root gate 7d7d5a45 §6 binding, integrated R3+R4/R5/R6 as overridden by ROOT). Requires whole selected bootstrap + U/C operation in fresh isolated workspace-local scratch under `.rephase-1-editorial-runtime/`, independent DB, no inherited overrides, no reconstruct DB fixtures, no saved-runner reuse. Both routes, genuine changed-tool epochs in isolated synthetic fixtures, repeat C→U→U, renewal→editorial, normal direct Candidate/Preview/Freeze/Release, failure/resume, affected regressions, independent final review.
- Root HEAD at start: `f84fcf5321be3798c862c0156278afbba01f89f6` (Human commit, clean except untracked parallel packet files under `notes/rephase-1-versioned-renewal-implementation/resume-20261025/`). Verified pre/post HEAD same, no staged changes, no tracked modifications (untracked-only allowed for parallel workers).
- User requests parallelization. This freeze creates a NEW source-complete immutable snapshot for parallel review/test without mutating the authoritative WORK.

## 2. Rejected M1 preserved untouched (no reset/clean/deletion)

- Path: `.rephase-1-editorial-runtime/versioned-renewal-impl-20261023T181352Z/candidate-work/`
- Observed read-only (no writes, no `git clean/reset`, no deletion):
  - HEAD `a8890d4ff612563e71b7dcf5db76287acfe4ea35`, log 3 commits only (`72d6830` milestone, `f360b67` M1 test, `a8890d4` pycache removal), `rev-list --count` = 3, root `72d6830` has no parent (new root `git init -b main`, NOT real 409 ancestry).
  - `status --porcelain=v1 --untracked-files=all` clean (empty), NOT 57M. `find -path ./.git -prune -o -type f -print | wc -l` = 729 per prior correction (NOT 761 claimed in `worklog.md`, NOT 721 intended). Discrepancy preserved as rejection reason, not repaired.
  - Remote inert `https://example.invalid/versioned-renewal-fixture.git`, `.git` 83 files but distinct DB with fake-root replacement — MUST NOT be used as actual candidate identity.
  - No modifications by this freeze unit (pre/post HEAD `a8890d4` identical, status clean identical). Original M1 docs untouched.
- Task claim contrast preserved: `rsync -a --exclude=.git/__pycache__/*.pyc` (untracked copy, NOT manifest-exact) and `761 files` lack `proof-diff-names`/`ls-files -s`/SHA inventory tying to manifests.

## 3. Frozen source verified (not assumed via same status)

Input (authoritative corrected WORK, FROZEN during round):

- `.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work/`
  - Actual base HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2` (actual409, verified via `rev-parse HEAD`/`HEAD^{tree}`, exits 0).
  - `status --porcelain=v1 --untracked-files=all` = 39 ` M` + 42 `??` = 81, `diff HEAD --name-only` 39, `diff --cached --name-only` empty (index clean for tracked).
  - Worktree `find -path ./.git -prune -o -type f -print | wc -l` = 731 = R7b721 + 10 renewal (no extra, no missing, verified via stdlib walk vs `source-manifest-r7b.json` 721 paths + 10 explicit renewal paths).
  - `M` = 35 consumer/schema/config overlap + 4 workflow/style (39 total); `U` = 32 baseline + 10 renewal (42 total). Baseline25M+32A are subsets of current39M+42U. Extra vs baseline57 = 14 modified + 10 new (see manifest).
  - All 42 untracked are `.py`/`.json` under `schemas/`/`scripts/`/`tests/`, no `__pycache__`/`*.pyc`, no blind cache/tmp. All 14 schemas JSON-valid, all `.py` AST-parse OK via stdlib (no project import).
  - Modes: Git `100644` (730) + `100755` (1 `scripts/survey_core_execution_bridge_v2.py`) via `ls-files -s`; physical `0o664` (730) + `0o775` (same 1 file) via `stat` (umask 002), recorded separately (not faked equal).
  - Real available Git ancestry: `log --oneline -3` = `409b292 DM-004 final cleanup...`, `34f934e...`, `c4aa3b5...`; shallow `774dd39a951c9ac3818e83dfffd4c7666efb0a20`; NO new root, NO fake replacement. Synthetic fixture SOURCE commits for future tests must be in SEPARATE isolated DB, meaningful source-only before authorities (not yet done, not in this freeze).
- Portable patch and manifests (unchanged, not re-applied):
  - `notes/rephase-1-editorial-operation-implementation/source-packaging/complete-r3-operation-409.patch` — `sha256sum` `659063dc27f0926aaf6e8a33f322937076563c4a23f6cf0d80ca970e1b2abd5b`, `wc -c` 2018112, `git apply --stat` 57 (per packet). Directly applicable to clean409.
  - `complete-r3-operation-manifest.json` — `delta_count` 57, `tracked_modified` 25, `untracked_new` 32, `head` 409b292, `head_tree` 8ce36998, `intended_721_verified` true.
  - `correction-r7/source-manifest-r7b.json` — `head` `721a04d85532d7855f3e54cc411f5847c787726e`, `tree` `ac7cb0bd2e977b46e957450816eddd779799e144`, `count` 721. Used as authoritative intended-721 list (NOT `rsync` untracked).
- Baseline721 + intended new3modules+4schemas+testfiles verified intent:
  - CUR paths = R7b721 + 10 renewal, missing 0. Renewal10 = 4 `versioned-renewal-*.schema.json` + 3 `survey_versioned_renewal_*.py` (HIST/S/HIGH) + 3 `test_versioned_renewal_*.py` (high/history/source phases). Fixed3newmodules/4newschemas per root map; 5 existing-schema branches and replay63/route/66union/pipeline67→71 are map memberships, NOT measured successor source.

## 4. NEW immutable snapshot (authoritative for parallel review/test)

- Fresh unique id: `20261024T174422Z` (after rejected `181352Z`, after corrected `185000Z` env, after failed strict-recon `174224Z` preserved below).
- Path: `.rephase-1-editorial-runtime/versioned-renewal-freeze-20261024T174422Z/snapshot-work/`
  - Absolute: `/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-freeze-20261024T174422Z/snapshot-work/`
  - Actual base HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2` (same as SRC, verified post-copy).
  - Intended delta 39M42U=81 exact (status 39 ` M` +42 `??`, `diff HEAD --name-only` 39, `diff --cached` empty, SRC==DST identical).
  - Files 731 exact (no extra, no pycache, no `.git` in count), all 731 SHA/bytes SRC==DST identical, `dst-hash-everything` SHA256 `24083f0abbeebbba3ff3df516b42e3834c3f33827f71e7d33b8f474319083606` (731 lines `SHA bytes relpath`).
  - Modes: Git `100644`/`100755` vs physical `0o664`/`0o775` recorded separately (1 executable `survey_core_execution_bridge_v2.py` distinguished).
  - Real available Git ancestry: `log --oneline -3` starts `409b292`, shallow `774dd39...`; NO new root, NO fake replacement, NO new commits in DST (HEAD still 409). Future meaningful synthetic fixture SOURCE commits must be in NEW independent DB before authorities, not this snapshot as fake candidate commit. Optional fixed test SOURCE separate DB (independent copy existing `721a04d` lineage + current intended overlay + sourceONLY commit for future tests, preserve old tool ancestry) deferred as ambiguous until root instruction — NOT done here to avoid fake-candidate confusion.
- Provenance: byte-independent `.git` copy via `cp -a SRC/.git DST/.git` (no `-l`/`--link`, no hardlinks). Verified:
  - `.git` 83 files (same as SRC), `objects/info` absent, `objects/info/alternates` absent, remotes inert `example.invalid` (no `github.com`), `rev-parse --absolute-git-dir` = own `.../versioned-renewal-freeze-20261024T174422Z/snapshot-work/.git`, `config --list --show-origin` only own `.git/config`.
  - Full `.git` `dev:ino` walk src vs dst disjoint (0 collisions, 0 cross-domain), worktree 731/731 `dev:ino` disjoint, dst `nlink==1` for all (no hardlink sharing).
  - No inherited `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` (outer `env | grep ^GIT_` empty pre-run except sanitization vars; inner sanitized `GIT_NO_LAZY_FETCH=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_OPTIONAL_LOCKS=0` only, verified via corrected `env-check` for `^GIT_(DIR|WORK_TREE|INDEX_FILE)=` absent).
  - Worktree populated ONLY via R7b721+10renewal intended list (731 paths) with `shutil.copy2` (preserves bytes/mode), NOT `rsync -a` untracked. Parent dirs created as needed, each file SHA/bytes verified post-copy and SRC==DST.
- Procedure saved BEFORE execution via `Write` (dedicated editor): `source-freeze-evidence-20261024T174422Z/make_source_freeze_20261024T174422Z.sh` (`bash -n` 0, every `git`/`cp`/`python` invocation captured to unique `*-stdout.txt`/`*-stderr.txt`/`*-exit.txt` (numeric `printf "%s"`), appended to `commands.log`; `set -u` only, explicit rc checks, pre-checks before `mkdir DST` (fail-closed, no `GIT_*` inheritance, `PYTHONDONTWRITEBYTECODE=1`, `LC_ALL=C`, no network, no old runners, no restore).
- First attempt `174224Z` FAILED only on overly strict `recon-status` clean check (parallel packet untracked files `evidence-reconciliation.*` + own evidence mistaken for dirt). All source/isolation verifications had not yet run; no source/input/reconstruct/rejected modifications (pre/post HEAD identical). Preserved as `source-freeze-evidence-20261024T174224Z/` with `FAIL` in `commands.log` (disclosed, not concealed, not deleted). Retry `174422Z` with corrected untracked-only recon check (`diff --cached` empty + `diff HEAD` empty + every `status` line `?? `) succeeded `DONE OK`. No `Git DB` in `notes/` (evidence dirs contain only `.txt`/`.log`/`.sh`/`.json`/`.md`, no `.git`).

## 5. Runtime / tools (local only, no install, no network)

- `python3` `/usr/bin/python3` `Python 3.14.4`, `jsonschema` `4.23.0`, `PYTHONDONTWRITEBYTECODE=1` (no `__pycache__` created in source/dest/packet).
- `git` `/usr/bin/git` `2.53.0`, `GIT_NO_LAZY_FETCH=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_OPTIONAL_LOCKS=0`, `git --no-optional-locks`, no `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` inherited.
- `TeX`: NOT on `PATH` (`which pdflatex/latexmk` absent). Available local-only at `/tmp/opencode/jgas-texlive-20261019T133205Z/texlive/bin/x86_64-linux/pdflatex` (`pdfTeX 3.141592653-2.6-1.40.29 TeX Live 2026`) and `latexmk` `4.88`. Not installed, not run, no PDF built in this unit. Unbundled runtime limitation retained.
- `pytest` absent (`which pytest` empty), `pip` `26.2.1` present but NOT used. No candidate project import, no tests executed in this freeze unit.
- Existing old workspaces under `.rephase-1-editorial-runtime/` and `/tmp/opencode/` treated as unknown user work — preserved, not listed/deleted except where explicitly needed for this freeze (SRC reads only).

## 6. Evidence (no DB in notes)

- `notes/rephase-1-versioned-renewal-implementation/resume-20261025/source-freeze-evidence-20261024T174224Z/` — first raw outputs + `commands.log` (ends `FAIL recon status not clean`, all prior `rc=0`), preserved as failure disclosure, superseded.
- `notes/rephase-1-versioned-renewal-implementation/resume-20261025/source-freeze-evidence-20261024T174422Z/` — authoritative raw outputs + `commands.log` (`DONE OK 20261024T174422Z`), including `recon-head/status/diff-cached/diff-head/untracked-only`, `rejected-head/log/status`, `src-head/tree/log/status/diff-cached/diff-names/others/count/git-count/remote/shallow/pycache/intended-verify/ls-files-s/hash-everything`, `mkdir-freeze/cp-git`, `dst-git-count/head/tree/gitdir/remote/log`, `populate-snapshot`, `dst-count/status/diff-names/diff-cached/others/manifest-verify/isolation/noalternates/config-show/env-check/hash-everything`, `src-head-post/status-post/recon-head-post/rejected-head-post` (all `exit 0`).
- `notes/rephase-1-versioned-renewal-implementation/resume-20261025/manifest.json` — machine manifest for new SNAPSHOT (base/tree/delta/files/modes, ancestry, tools, evidence list, ROOT §7 corrections, limitations).
- This file `source-freeze.md` (NEW, original M1/worklog/recovery docs untouched).

## 7. Limitations and next (ROOT §7 binding)

- PartialDB `26309` missing retained (present `2376`/missing `26309` per prior census, 13 commits, shallow `774`), archive preserves available partial content + 689 relevant HEAD blobs, NOT full-history backup. Missing-blob diagnostics would have fail-closed `read-tree`/`add` (none triggered). Not a full-history/full-suite certification.
- Scope: SRC/DST worktrees contain ONLY 731 intended files (relevant subset: 689 tracked at HEAD with 39 modified + 42 untracked intended); `sources/surveys` 31466 unchanged, not in patch, outside proof scope. Scoped clean = tracked + intended untracked, NOT full `status empty` claim (which would show bulk deletions). `apply --check` only checks 57 pre-images, bounded proof for patch applicability, not full-tree clean certification.
- Runtime unbundled (TeXLive not on PATH, Python local, no source imports/builds/tests in this unit). Cache/tmp/evidence excluded from patch (`notes/`, pycache, tmp scratch). Whitespace: one inherited `trailing whitespace` warning at patch:29461 preserved (not normalized). Modes Git vs physical recorded separately.
- No new authority: HEADs still 409 (SRC/DST) and 721a04 (R7b SNAP); no candidate/reconstruct commit, no Gate/Candidate/State/Preview/Freeze/Release, no Human approval, no production adoption. Independent review + root synthesis remain separate.
- Astra status-review corrections (binding over earlier recovery wording):
  1. `FILE SHA everywhere EXCEPT proof basis_ref SELF` is incorrect. **Every cross-document `{path,sha256}` ref, including `proof.basis_ref`, is FILE-BYTE SHA256.** SELF digests appear only in the artifact's explicitly named internal digest field. The root decision by S and HIGH stands; H companions record-bound, no new sidecar.
  2. Later source/run evidence is **unreviewed/unbound in the TURN3 summary**, not established to be unexecuted. Run35–61 artifacts (including run36 48× exit 0) show later activity requiring inspection. Workdir HIGH hash difference from TURN3 is not a reason to revert it or rerun all later positives. First correlate later run commands/exits, fixture commits, exact source bytes and current States. Preserve all snapshots/partials. Determine actual latest successful boundary and only then resume still-unexecuted/failed obligations. Do not revalidate high22 with different current tools expecting eligibility transfer.
  At root's status inspection the last newly discovered evidence mtime was ~2026-10-25 02:02 JST, whereas worklog TURN3 stopped at 2026-10-24 16:55 JST. Worklog had lagged subsequent activity; this was not evidence of no work after run34.
- Next for parallel review/test (root to delegate, NOT executed here): use SNAPSHOT `/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-freeze-20261024T174422Z/snapshot-work/` (actual409+57+H/S/high, 731, 39M42U, 83-file partial DB, inert remote, no hardlinks) as read-only source for independent review and isolated test fixtures. Implement whole selected renewal per assessment §5 in separate writable workspace (NOT this immutable snapshot): typed historian/current source-proof/high, 4 new schemas/5 amended/3 new modules, bootstrap, U/C, repeat C→U→U, renewal→editorial, normal lifecycle, failure/resume, regressions, independent final review. If map contradicts source, return exact predicate to Astra before broadening. Do NOT use rejected `.../versioned-renewal-impl-.../candidate-work` (fake root) or unrelated root commits as candidate identity. Do NOT commit in this snapshot (HEAD must stay 409); future meaningful synthetic fixture SOURCE commits must be in NEW independent DB before authorities.
- Optional fixed test SOURCE separate DB (independent copy existing `721a04d` lineage + current intended overlay + sourceONLY commit for future tests, preserve old tool ancestry) deferred as ambiguous until root instruction — NOT done here.

Stop here. Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN. Human Commit Point preserved. Ordinary Commit/Push Human-owned. This freeze is NOT whole-unit completion and NOT a Commit Point.
