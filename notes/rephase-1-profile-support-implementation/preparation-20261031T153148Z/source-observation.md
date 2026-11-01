# Preparation / source observation report — 20261031T153148Z

General preparation-only. No source implementation or tests beyond setup checks.
No independent approval. WholeNOT_READY/step4B3OPEN/auditunstarted/DM021+022OPEN preserved.

## 1. Workdir

- Unique: `.rephase-1-editorial-runtime/profile-support-implementation-20261031T153148Z/candidate-work`
- Ignored: `/.rephase-1-editorial-runtime/` in workspace `.gitignore` (verified).
- Parents verified before creation via directory reads.
- Creation: `mkdir -p` for workroot + packet logs dir (necessary for copying).

## 2. Derivation (no restore, no blind residue)

- Source: `/tmp/opencode/jgas-dm022-indep-20261029T235900Z/proof-candidate`
  (`drwxrwxr-x`, 2026-10-30, available).
- Worktree: `tar --exclude=.git -cf - -C <proof> . | tar -xf - -C <candidate-work>`
  → exit 0, 768 files. Log: `logs/cp-worktree-*.txt`.
- PartialDB: `cp -a <proof>/.git <candidate-work>/.git`
  → exit 0, 57 objects, ~9.0M. Log: `logs/cp-git-*.txt`.
- Residue: proof 0 `*.pyc`/0 `__pycache__`; new workdir 0/0. Author 33pyc/2dirs
  residue (in `.../dm022-prearchitecture-implementation-20261028T113126Z/candidate-work`)
  never copied. Manifest `excluded`/`excluded_cache_actual` (33pyc/2dirs) understood as
  author-workcopy note, not proof content.
- No cleanup/reset/old runners/saved scripts executed.

## 3. Independent DB (separate, inert, no sharing)

- `candidate-work/.git/config` origin `https://example.invalid/rephase-candidate-recovery.git`
  (inert). `config.worktree` sparseCheckout true/cone true (inherited, preserved).
- `HEAD` `409b292756dd1277b9dfae87679934c0d2ce251c` (actual parent, preserved as reference).
- `shallow` `774dd39a951c9ac3818e83dfffd4c7666efb0a20` (fixed baseline774, no rebaseline).
- `objects/info/alternates` absent. `refs/heads/codex/rephase-candidate-recovery` present
  (inherited refs, no new refs created).
- `GIT_DIR/GIT_WORK_TREE/GIT_CEILING` unset at check time.
- Inode spot-check (`logs/inode-check-*.txt`): sample worktree file
  src ino 1846609/dev45 vs dst ino 24009412/dev2050, nlink 1/1, shared=False;
  3 sample objects distinct inodes, shared=False. No hardlinks/shared inodes.
- No new commits/branches/PRs/HEAD moves in this invocation.
  Log: `logs/git-config-*.txt`.

## 4. Identity vs manifest (verified, limits stated)

- Manifest `complete-dm022-manifest.json` 185422B, verified sha/manifest-size match delivery.
- Patch `complete-dm022-prearchitecture-409.patch` 4931836B, verified sha match.
- Manifest content: `intended_files` 768, `delta` A79/M54, `head` 409b292…, `head_tree`
  8ce3699…, `tracked_at_head_in_intended` 689, `files` dict path→{bytes,git_mode,
  physical_mode,sha256}.
- Verification (`logs/manifest-verify-*.txt`, exit 0):
  768/768 sha256+bytes PASS; worktree excl `.git` 768; extra 0; missing 0; pyc 0.
- Proof worktree excl `.git` independently counted 768; proof `.git` 57 objects/8.8M.
- Precode ROOT `astra-precode-gate-resolution.md` FULL bfb72…/20159B re-verified.
- Limits: bytes/sha comparison only; modes recorded not re-certified per-file git-mode;
  no full133/768/inode recertification beyond manifest; no hydrated/full-tree claim;
  inherited missing26309/bulk31466/runtimeTeX/55Gitlinks qualifications retained.
  Candidate modules never imported for verification (stdlib json/hashlib/os only).

## 5. Runtime introspection (authorized, no installs)

- Log: `logs/runtime-env-*.txt` (exit 0).
- `/usr/bin/python3` 3.14.4 (`3.14.4 main GCC15.2.0`), jsonschema 4.23.0, pypdf 6.16.2.
- TeX absent (`which` empty; `pdflatex --version` not found). Not a blocker for
  preparation; only if affected real-build verification later requires it.
- Delivery hashes re-recorded in runtime log (patch/manifest/precode-ROOT all match).
- No installs until actual need and permission.

## 6. Boundaries observed

- No reconstruct `git status/HEAD/log`, no Human Commit readback, no network, no
  Production writes, no extra intake (4GET capture reused as DATA per prior units).
- Fixed baseline774 `774dd39a951c9ac3818e83dfffd4c7666efb0a20` (commit, not SHA256 field).
- Prior55 Gitlinks/child dirt untouched (no reconstruct git ops).
- No source edits, no tests run, no fixtures created, no synthetic commits yet.
  Future synthetic fixture commits authorized later with process-scoped identity only,
  no `allow-empty`, never in reconstruct DB.

## 7. File census for dispatch (read-only listing, no edits)

- `scripts/survey_evidence_v2.py` has `_source_class:177`; `scripts/survey_completeness_v2.py`
  present; `_build_completeness`/`validate_interactive_input` in
  `run_evidence_v2_interactive.py:228,272,482` + `run_screening_v2_interactive.py:42`;
  `derive_before_context`/4 LOW builders in `survey_research_authority_v2.py` +
  `survey_prearchitecture_acceptance_v2.py`; runner trio
  `run_evidence_v2_interactive/run_screening_v2_interactive/run_evidence_v2_agent_first`
  plus weekly/special interactive wrappers; 229 `scripts/*.py`; relevant tests include
  `test_survey_evidence_v2/test_survey_screening_v2/test_run_evidence_v2_agent_first/
  test_dm022_* /test_survey_completeness* /test_survey_discovery_v2` + fixture helpers
  `dm022_*_fixture_v2.py`. Full lists in packet README §Task partition.
- Ownership proposal in packet README keeps A/B/C/D files disjoint; coupled
  Screening↔DM022 interface explicit; tests need dedicated owner D.

## 8. Status / blocker / ready

- Preparation outputs complete: unique workdir + independent DB + 768 verification +
  runtime logs + packet docs. No actual blocker. No missing dependency/authority/contract
  contradiction found in preparation; implementers must return exact gaps to Astra before
  broadening if discovered.
- Ready-to-dispatch: root chooses bounded parallel assignments (A/B/C/D) on the fixed
  snapshot above; do not spawn workers in this invocation. No implementation/tests yet.
  Do NOT claim independent approval or whole-ready. Stop at preparation return.

## 9. Supplement qualification — 20261031T153547Z (appended, no overwrite)

- Scope: bounded preparation qualification only. A/B/C are concurrently editing assigned
  workcopy runtime files; this supplement does NOT rehash mutable worktree bytes as
  initial proof and does NOT touch implementation files (no writes to `candidate-work/`
  beyond the initial copy; this supplement only lstats modes and reads `.git`/env).
  No tests/fixtures/commits. No subagents. All new raw outputs in
  `supplement-20261031T153547Z/logs/`; existing `logs/*` untouched.
- §3 qualified: prior `logs/inode-check-*.txt` was a 1-workfile + 3-object sample only.
  Full-DB check (`supplement-.../logs/gitdb-kinds-*.txt`, `gitdb-shared-*.txt`, exit 0):
  candidate `.git` has 83 files / 0 symlinks / 49 dirs (all entries FILE or DIR, no
  SYMLINK); proof `.git` 83 files / 0 symlinks; shared `(dev,ino)` candidate↔proof = 0;
  shared candidate↔reconstruct `.git/objects` (5377 files, OBJECTS ONLY, no HEAD/ref/log
  readback) = 0; internal duplicate `(dev,ino)` within candidate = 0. `objects/info/`
  absent (hence no `alternates` file). `shallow` = baseline774, origin inert, sparse
  cone true preserved. Candidate HEAD/tree confirmed via candidate-only plumbing
  (`git --git-dir=<candidate>/.git rev-parse HEAD` → `409b292…`,
  `HEAD^{tree}` → `8ce3699…`, exit 0, no mutation; `supplement-.../logs/candidate-head-tree-*.txt`).
  Inherited sparse/promisor/partialDB qualifications retained
  (`objects/pack/*.promisor`, `*.rev`, `dm004-32/successor-20/w1-7` packs observed, not validated).
  No child Gitlinks inspected. First copy pipeline exit (tar excl `.git` 0, `cp -a` `.git` 0)
  preserved as-is; no atomic guard/copy-time enforcement claimed retroactively.
- §4 mode note (`supplement-.../logs/mode-check-*.txt`, exit 0): current worktree still has
  768/768 manifest paths present with 768/768 physical-mode matches via `lstat` only
  (no content read/hash). Files are now mutated by A/B/C, so this is NOT initial-byte
  proof and does not supersede the initial 768/768 sha+bytes copy-time verification.
- §5 TeX corrected (`supplement-.../logs/tinytex-*.txt`, exit 0): prior "TeX absent" was
  PATH-only (`which` empty, `pdflatex --version` not found, PATH has no TeX). Explicit
  known paths exist and are executable: `/home/eariver/.TinyTeX/bin/x86_64-linux/lualatex`
  (symlink → `luahbtex`, LuaHBTeX 1.24.0 TeX Live 2026) and `.../biber` (biber 2.22).
  No installs/network/build performed; version probes read-only. TeX remains not-a-blocker
  for preparation; available via explicit path if affected real-build verification needs it.
- Blocker from this supplement: none. Independent-DB separation holds on full entry check.
