# DM022 pre-Architecture implementation — source/environment preparation

Date: 2026-10-28 UTC. Pre-code preparation ONLY. No runtime code, tests, fixtures,
restore/network/ordinary Commit/Push. Root remains reviewer. Human Commit/Push
readback SKIPPED per instruction (no `git status/show/log/rev-parse` in workspace root).

## 1. Authority read (binding)

- Assessment `outputs/rephase-1-dm022-prearchitecture-precode-assessment.md`
  (sha256 `071d05901be3afb9c8f2727d729382b6753f74f687864ec5082e94beee118d55`, 8549B), §5 is next-unit scope.
- Contract `outputs/rephase-1-dm022-prearchitecture-contract-decision.md` INCLUDING §11
  (sha256 `a345bb9524b4dfc5b5f32600d0d708687e2b6131d91a43965c97b6418388f223`, 31351B).
- Packet `notes/rephase-1-dm022-prearchitecture-precode/README.md`.
- Mandatory Astra `notes/rephase-1-dm022-prearchitecture-precode/astra-precode-gate-resolution.md`
  INCLUDING §5 (sha256 `0425c5300c9c7211e4468d3b842c4e3af1acb9f5bf1eba00e90f7ba72ef44a5a`, 13788B).
- Prior carryover `notes/rephase-1-dm022-prearchitecture-contract/source-and-carryover-observation.md`
  (55 bare Gitlinks basis; NOT re-authenticated here; child dirt untouched).

## 2. Reused source (read-only, no restore/network/clone)

Proof-copy AVAILABLE in place (not restored):

- `.rephase-1-editorial-runtime/versioned-renewal-packaging-final-depth-20261025T205432Z/proof-copy/candidate-partial-b40de60`
- HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`
- `find -path ./.git -prune -o -type f -print | wc -l` = **742**, `__pycache__` = 0
- remote `https://example.invalid/rephase-candidate-recovery.git` (inert), no `alternates`/`commondir`, own path-local gitdir
- Patch `complete-versioned-renewal-409.patch`: sha256 `f898d33b…`, 3423014B — matches AGENTS pin
- Manifest `complete-versioned-renewal-manifest.json`: sha256 `d488c6ee…`, 43355B;
  fields `head 409b292…`, `head_tree 8ce36998…`, `delta 93`, `40M+53A`, `intended_final 742`,
  `scoped 689 tracked at HEAD + 53 absent`

No old runners executed; no saved-restore scripts run.

## 3. New independent writable workcopy

Parent verified before creation (`ls -ld .rephase-1-editorial-runtime` exists; ignored via
`.gitignore:13:/.rephase-1-editorial-runtime/`; UTC `20261028T113126Z` from `date -u`).

- Parent: `.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/`
- Workroot: `.../dm022-prearchitecture-implementation-20261028T113126Z/candidate-work`
- Method: `cp -a SRC/.git DST/.git` (byte copy, no `--link`), then
  `tar --exclude=.git --hard-dereference -cf - -C SRC . | tar -xf - -C DST`
  (intended worktree only; no caches/tmp/old-fixture-DB blind copy; no `cp` hardlinks/deletes).
- No `GIT_*` env observed. Inert origin preserved. No config mutation, no staging, no commits.
- Candidate parent HEAD stays actual409 by file bytes.

New-copy identity (necessary source binding, NOT Human commit readback):

- HEAD `409b292…`, tree `8ce36998…`, remote inert `example.invalid/rephase-candidate-recovery.git`
- absolute gitdir under new workroot; `alternates`/`commondir` absent
- `git status --porcelain=v1` = 93 lines; `git diff --cached --raw` = 0; `git ls-files` = 32155
- worktree files (excl. `.git`) = **742**, pycache dirs = 0

Scope proof (new copy vs manifest):

- **93/93** delta entries SHA256+bytes match; 742 count holds
- 5-file spot matches prior observation: HIGH `3dbdedb8…`, H `74275d22…`, S `2290ddd0…`,
  agent `a32072e7…`, evidence `a57bce69…`
- Full-742 rehash NOT performed here; prior final-depth all-entry guard remains authority.
  No new full93/742/inode recertification beyond §4 separation is claimed.

## 4. Separation (read-only; no Human HEAD/status readback)

- SRC vs DST `.git/objects`: 57 files each, **0 inode overlap**, 0 hardlinked files both sides
- `HEAD`/`config` sample inodes distinct; `os.path.samefile(HEAD)` = False (dev 2050/2050, same fs, no links)
- No `alternates`/`commondir` in SRC, DST, and no `GIT_DIR`/`GIT_WORK_TREE` env
- Workspace reconstruct `.git` NOT inspected (no HEAD/status/log/show/rev-parse there per Human order).
  Separation from reconstruct rests on: distinct absolute gitdir under ignored runtime +
  absent alternates + inert origin + byte-copy (no hardlinks) + untouched workspace DB.
- Existing 55 bare Gitlinks/child dirt: untouched; no cleanup/relocation/index repair;
  no `submodule` operations; no per-child re-verification this unit.

## 5. Runtime availability (read-only; no install/network/execution)

- Usable python: `/usr/bin/python3`, Python **3.14.4** (satisfies 3.12+)
- Present (system): `jsonschema 4.23.0`, `PyYAML 6.0.3`, `Jinja2 3.1.6`, `pillow 12.1.1`
- Missing: **no isolated venv with pytest found** (`versioned-renewal-env-20261023T185000Z`
  holds only `candidate-work`, no `.venv`; `/tmp/opencode/candidate-recovery-tooling*` absent;
  `python3 -m pytest` → No module named pytest)
- TeX/build: **absent** — no `pdflatex`/`xelatex`/`lualatex`/`latexmk` (only `pdftotext`);
  PDF builds cannot run in this environment as-is
- `git 2.53.0`; disk 24% used; prior `/tmp/opencode` scratch partially present but venv gone

Implementation workers must bring their own isolated env (pytest + pinned deps) and TeX
(or document PDF non-build) before running tests/builds. Do NOT install/network or run old runners
without fresh authorization.

## 6. Files written / blocker

Written (no Git DB in packet):

- `notes/rephase-1-dm022-prearchitecture-implementation/source-preparation.md` (this file)
- `notes/rephase-1-dm022-prearchitecture-implementation/source-preparation-data.json`
  (pins, counts, inode separation, raw command/exit list, runtime, limitations)

Blocker: **NONE for preparation**. Environment gaps above are limitations for the next
implementation workers, not a failed copy. Workroot is clean for parallel assignment.
NO implementation yet — other worker scopes can be assigned without overlap.

## 7. Raw provenance (honest)

Shell byte-copy used only for `.git` + worktree (`cp -a`, `tar --hard-dereference`).
Docs/JSON written via dedicated Write tool. Command/exit list in the JSON is transcribed
from tool-observed outputs at execution time (no separate tee logs; no old-runner execution).
All errors preserved (none on copy path; missing pytest/TeX recorded as limitations, not hidden).
