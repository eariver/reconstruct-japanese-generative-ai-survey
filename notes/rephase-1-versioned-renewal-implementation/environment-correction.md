# Versioned renewal — author-side environment/provenance correction (BEFORE implementation)

2026-10-23. Author-side correction ONLY. No implementation, no tests, no builds, no fixture restores, no network, no candidate/reconstruct commits. Source implementation to be assigned after this return; this is NOT whole-unit completion.

Dedicated editor used: `Write` (no `apply_patch` available in this environment — fallback reported). No shell heredoc edits for procedure scripts; scripts saved via `Write` before `bash -n`/execution.

## 1. Authority and scope read

- `AGENTS.md` Human boundaries: `eariver/japanese-generative-ai-survey` READ ONLY, no branches/PRs/Issues/comments, State/decisions/Gates, Freeze/Release, deployment/Actions, adoption/migration without explicit Human authorization. Isolated fixture objects only in independent Git DB, inert origin, no alternates/hardlinks/object sharing/inherited Git-root overrides. Never create fixture objects in reconstruct DB. No fixture objects/refs/commits in reconstruct. No arbitrary path budget. Ordinary final reconstruct commit/Pull/Push Human-owned. Do not fix stale/dirty production checkout. Pause at Commit Point, no auto next unit.
- Current renewal task: `outputs/rephase-1-versioned-renewal-precode-assessment.md` PRE_CODE_READY bounded design/interface map ONLY (contract 478f0051 §11 unchanged, root gate 7d7d5a45 §6 binding, integrated R3+R4/R5/R6 as overridden by ROOT). Requires whole selected bootstrap + U/C operation in fresh isolated workspace-local scratch under `.rephase-1-editorial-runtime/`, independent DB, no inherited overrides, no reconstruct DB fixtures, no saved-runner reuse. Both routes, genuine changed-tool epochs, repeat C→U→U, renewal→editorial, normal direct Candidate/Preview/Freeze/Release, failure/resume, affected regressions, independent final review.
- Root HEAD at start: `c5b0d7cff9f978a2823f9a9e00ae1e0f9d5b3e1f` (Human commit, clean except untracked `notes/rephase-1-versioned-renewal-implementation/` from prior worker). Verified pre/post unchanged (HEAD same, no staged changes).

## 2. Rejected M1 preserved untouched (no reset/clean/deletion)

- Path: `.rephase-1-editorial-runtime/versioned-renewal-impl-20261023T181352Z/candidate-work/`
- Observed read-only (no writes, no `git clean/reset`, no deletion):
  - HEAD `a8890d4ff612563e71b7dcf5db76287acfe4ea35`, log 3 commits only (`72d6830` milestone, `f360b67` M1 test, `a8890d4` pycache removal), `rev-list --count HEAD` = 3, root `72d6830` has no parent (new root `git init -b main`, NOT real 409 ancestry).
  - `status --porcelain=v1 --untracked-files=all` clean (empty), NOT 57M. No raw/source inventory proof for claimed 761 files vs 721 intended.
  - `find . -path ./.git -prune -o -type f -print | wc -l` = 729 (read-only count, NOT 761 claimed in `worklog.md`, NOT 721 intended). Discrepancy preserved as rejection reason, not repaired.
  - Remote inert `https://example.invalid/versioned-renewal-fixture.git`, `.git` 827 files (vs proof 83), distinct DB but fake-root replacement — MUST NOT be used as actual candidate identity.
  - No modifications by this correction unit (pre/post HEAD `a8890d4` identical, status clean identical). Original M1 docs (`README.md`, `evidence-m1.md`, `source-manifest.md`, `worklog.md`) unmodified.
- Task claim contrast: M1 `worklog.md` says `rsync -a --exclude=.git/__pycache__/*.pyc` (untracked copy, NOT manifest-exact) and `761 files: base 409+57 plus renewal changes`; task notes actual is `721 intended` and `25M32A` (not 57M). Rejected evidence lacks `proof-diff-names`/`ls-files -s`/SHA inventory tying 761 to manifests. Preserved as rejected evidence.

## 3. Corrected source verified (not assumed via same status)

Input (available proof-copy, preferred, no restore):

- `.rephase-1-editorial-runtime/final-source-packaging/proof-copy/candidate-partial-b40de60`
  - HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2` (actual409, verified via `rev-parse HEAD`/`HEAD^{tree}`, exits 0).
  - `status --porcelain=v1 --untracked-files=normal` = 25 ` M` + 32 `??` = 57, exactly matching `complete-r3-operation-manifest.json` partitioning (`tracked_modified` 25, `untracked_new` 32, `delta_count` 57). `diff HEAD --name-only` 25, `diff --cached --name-only` empty (index clean).
  - Worktree `find -path ./.git -prune -o -type f -print | wc -l` = 721, exactly matching R7b intended 721 set (no extra, no missing, verified via Python stdlib walk vs `source-manifest-r7b.json` 721 paths).
  - All 57 delta SHA256/bytes match complete manifest; all 721 SHA256/bytes match R7b manifest (0 mismatches, verified via `hashlib.sha256`, no candidate import, no tests).
  - Sparse scope: `.git/info/sparse-checkout` present (`/*`, `!/*/`, plus `/.github/`, `/config/`, `/docs/`, `/schemas/`, `/scripts/`, `/specials/`, `/templates/`, `/tests/`), `config.worktree` `sparseCheckout=true/cone=true`, `ls-files --deleted` 0, `diff HEAD --stat` 25 files only. Bulk `sources/surveys` 31466 outside scope (disclosed, not in patch). `ls-files | wc -l` 32155 (full HEAD index), worktree scoped 721 — NOT full-tree clean claim.
  - `.git` 83 files, `objects/info` absent (hence `objects/info/alternates` absent — no alternates), remote inert `https://example.invalid/rephase-candidate-recovery.git`, `shallow` `774dd39a951c9ac3818e83dfffd4c7666efb0a20` (partial DB, 26309 missing retained).

Portable patch and manifests:

- `notes/rephase-1-editorial-operation-implementation/source-packaging/complete-r3-operation-409.patch` — `sha256sum` `659063dc27f0926aaf6e8a33f322937076563c4a23f6cf0d80ca970e1b2abd5b`, `wc -c` 2018112, `git apply --stat` 57 (per packet). Directly applicable to clean409 (packet proof `--check` 0/`apply` 0, not re-applied here).
- `complete-r3-operation-manifest.json` — `delta_count` 57, `tracked_modified` 25, `untracked_new` 32, `head` 409b292, `head_tree` 8ce36998, `intended_721_verified` true, `patch` bytes/SHA as above, `proof` scope `scoped 689 +32 absent →721`, `source_before_after` unchanged.
- `correction-r7/source-manifest-r7b.json` — `head` `721a04d85532d7855f3e54cc411f5847c787726e`, `tree` `ac7cb0bd2e977b46e957450816eddd779799e144`, `count` 721, 721 entries with `path/sha256/bytes/mode`. Used as authoritative intended-721 list (NOT `rsync` untracked).
- SNAP R7b reference (untouched): `.rephase-1-editorial-runtime/jgas-editorial-r7b-20261023T034500Z/candidate-partial-b40de60`, HEAD `721a04...`, tree `ac7cb0...`, worktree 725 files (721 + 4 `scripts/__pycache__/` pyc, `status` only pycache). Proof 721/721 SHA match R7b manifest, 57/57 match complete manifest.

## 4. NEW isolated writable candidate copy (authoritative corrected)

- Fresh unique id: `20261023T185000Z` (after rejected `181352Z`, after first failed correction `184000Z` disclosed below).
- Path: `.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work/`
  - Actual base HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2` (same as proof, verified post-copy).
  - Intended delta 25M32A=57 exact (status 25 ` M` +32 `??`, `diff HEAD --name-only` 25, `diff --cached` empty, partitioning exactly equals complete manifest `M`/`A` sets).
  - Files 721 exact (no extra, no pycache, no `.git` in count), all 721 SHA match R7b manifest, all 57 SHA match complete manifest.
  - Modes: Git `100644` (via `ls-files -s`, e.g. `AGENTS.md 174a812a...`, `config/survey-production-v2.json cffe16fe...`), physical `0o664` (via `stat`, e.g. `664 AGENTS.md`), recorded separately (not faked equal, umask 002).
  - Real available Git ancestry: `log --oneline -3` = `409b292 DM-004 final cleanup...`, `34f934e...`, `c4aa3b5...`; `rev-list --count` full partial history (not 3); shallow `774dd39...`; NO new root, NO fake replacement, NO unrelated root commits as candidate identity. Synthetic fixture commits for future implementation must be in SEPARATE isolated DB, meaningful source-only before authorities (not yet done, not in this correction).
- Provenance: byte-independent `.git` copy via `cp -a PROOF/.git WORK/.git` (no `-l`/`--link`, no hardlinks). Verified:
  - `.git` 83 files (same as proof), `objects/info` absent, `objects/info/alternates` absent, remotes inert `example.invalid` (no `github.com`), `rev-parse --absolute-git-dir` = own `.../versioned-renewal-env-20261023T185000Z/candidate-work/.git`, `config --list --show-origin` only own `.git/config`.
  - Full `.git` `dev:ino` walk src vs dst disjoint (0 collisions, 0 cross-domain), worktree 721/721 `dev:ino` disjoint, dst `nlink==1` for all (no hardlink sharing).
  - No inherited `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` (outer `env | grep ^GIT_` empty pre-run; inner sanitized `GIT_NO_LAZY_FETCH=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_OPTIONAL_LOCKS=0` only, verified via corrected `env-check` for `^GIT_(DIR|WORK_TREE|INDEX_FILE)=` absent).
  - Worktree populated ONLY via R7b manifest 721 list with `shutil.copy2` (preserves bytes/mode), NOT `rsync -a` untracked. Parent dirs created as needed, each file SHA/bytes verified post-copy.
- Procedure saved BEFORE execution via `Write` (dedicated editor): `make_corrected_env_20261023T185000Z.sh` (`bash -n` 0), every `git`/`cp`/`python` invocation captured to unique `*-stdout.txt`/`*-stderr.txt`/`*-exit.txt` (numeric `printf "%s"`), appended to `commands.log`; `set -u` only, explicit rc checks, pre-checks before `mkdir WORK` (fail-closed, no `GIT_*` inheritance, `PYTHONDONTWRITEBYTECODE=1`, `LC_ALL=C`, no network, no old runners, no restore).
- First attempt `184000Z` FAILED only on overly strict `env-check` (`grep ^GIT_` matched sanitization vars `GIT_CONFIG_*`); all source/isolation verifications had passed (721, 25M32A, 83, no sharing). Preserved as `environment-correction-evidence-20261023T184000Z/` with `FAIL` in `commands.log` (disclosed, not concealed, not deleted). Retry `185000Z` with corrected `^GIT_(DIR|WORK_TREE|INDEX_FILE)=` check succeeded `DONE OK`. No source/input/reconstruct/rejected modifications in either attempt (pre/post HEAD/status identical).
- Never staged/added/committed/reset in reconstruct or input (`diff --cached` empty pre/post in proof/WORK, no `git add/commit/reset` in reconstruct). No ordinary candidate commits (WORK has no new commits, HEAD still 409). No `Git DB` in `notes/` (`packet-find-git` equivalent: evidence dirs contain only `.txt`/`.log`/`.sh`/`.json`/`.md`, no `.git`).

## 5. Runtime / tools (local only, no install, no network)

- `python3` `/usr/bin/python3` `Python 3.14.4`, `jsonschema` `4.23.0` (`importlib.metadata`, `__version__` deprecation warning preserved), `PYTHONDONTWRITEBYTECODE=1` (no `__pycache__` created in source/dest/packet).
- `git` `/usr/bin/git` `2.53.0`, `GIT_NO_LAZY_FETCH=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_OPTIONAL_LOCKS=0`, `git --no-optional-locks`, no `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` inherited.
- `TeX`: NOT on `PATH` (`which pdflatex/latexmk` absent). Available local-only at `/tmp/opencode/jgas-texlive-20261019T133205Z/texlive/bin/x86_64-linux/pdflatex` (`pdfTeX 3.141592653-2.6-1.40.29 TeX Live 2026`) and `latexmk` `4.88` (John Collins). Not installed, not run, no PDF built in this unit. Unbundled runtime limitation retained.
- `pytest` absent (`which pytest` empty), `pip` `26.2.1` present but NOT used for install. No candidate project import, no tests executed in this correction unit.
- Existing old workspaces under `.rephase-1-editorial-runtime/` and `/tmp/opencode/` treated as unknown user work — preserved, not listed/deleted except where explicitly needed for this correction (proof/SNAP reads only).

## 6. Evidence (no DB in notes)

- `notes/rephase-1-versioned-renewal-implementation/make_corrected_env_20261023T184000Z.sh` — first procedure (overly strict check, `FAIL`), preserved.
- `notes/rephase-1-versioned-renewal-implementation/environment-correction-evidence-20261023T184000Z/` — first raw outputs + `commands.log` (ends `FAIL GIT_ env inherited`, all prior verifications `rc=0`).
- `notes/rephase-1-versioned-renewal-implementation/make_corrected_env_20261023T185000Z.sh` — corrected procedure (`bash -n` 0, `DONE OK`).
- `notes/rephase-1-versioned-renewal-implementation/environment-correction-evidence-20261023T185000Z/` — authoritative raw outputs + `commands.log` (`DONE OK 20261023T185000Z`), including `recon-head/status`, `rejected-head/log/status`, `proof-head/tree/status/diff-names/diff-cached`, `patch-sha/bytes`, `snap-head/tree`, `proof-manifest-verify`, `work-git-count/head/tree/gitdir/remote`, `populate-worktree`, `work-count/status/diff-names/diff-cached`, `work-manifest-verify`, `isolation-check`, `work-noalternates/config-show/env-check`, `proof-head-post/status-post`, `recon-head-post`, `rejected-head-post` (all `exit 0`).
- `notes/rephase-1-versioned-renewal-implementation/environment-correction-manifest-20261023T185000Z.json` — machine manifest for new WORK (base/tree/delta/files/modes, ancestry, tools, evidence list).
- This file `environment-correction.md` (NEW, original M1 docs untouched).

## 7. Limitations and next

- PartialDB `26309` missing retained (present `2376`/missing `26309` per prior census, 13 commits, shallow `774`), archive preserves available partial content + 689 relevant HEAD blobs, NOT full-history backup. Missing-blob diagnostics would have fail-closed `read-tree`/`add` (none triggered). Not a full-history/full-suite certification.
- Scope: GEN/PROOF/WORK worktrees contain ONLY 721 intended files (relevant subset); `sources/surveys` 31466 unchanged, not in patch, outside proof scope. Scoped clean = 689 tracked at HEAD +32 absent, NOT full `status empty` (which would show bulk deletions). `apply --check` only checks 57 pre-images (verified vs HEAD blobs), bounded proof for patch applicability, not full-tree clean certification.
- Runtime unbundled (TeXLive not on PATH, Python local, no source imports/builds/tests in this unit). Cache/tmp/evidence excluded from patch (`notes/`, pycache, tmp scratch). Whitespace: one inherited `trailing whitespace` warning at patch:29461 preserved (not normalized). Modes Git vs physical recorded separately.
- No new authority: HEADs still 409 (proof/WORK) and 721a04 (SNAP); no candidate/reconstruct commit, no Gate/Candidate/State/Preview/Freeze/Release, no Human approval, no production adoption. Independent review + root synthesis remain separate.
- Next after Human continuation: assign source implementation to General in NEW WORK `.../versioned-renewal-env-20261023T185000Z/candidate-work/` (actual409+57, 721, 25M32A, 83-file partial DB, inert remote, no hardlinks). Implement whole selected renewal per assessment §5 (typed historian/current source-proof/high, 4 new schemas/5 amended/3 new modules, bootstrap, U/C, repeat C→U→U, renewal→editorial, normal lifecycle, failure/resume, regressions, independent final review). If map contradicts source, return exact predicate to Astra before broadening. Do NOT use rejected `.../versioned-renewal-impl-.../candidate-work` (fake root) or unrelated root commits as candidate identity. Do NOT start from `184000Z` failed-check dir (superseded, preserved only as failure disclosure).

Stop here. Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN. Human Commit Point preserved. Ordinary Commit/Push Human-owned.
