# A4 path-normalization evidence — raw preservation + source binding

Date: 2026-10-28 UTC. Preserves author-A raw outputs on a FRESH private copy
(`/tmp/dm022-a5p-priv` = current idle candidate worktree + A-owned
path-normalization files, rebuilt AFTER all A edits via rm -rf + full copy,
`.git` grafted from frozen A4 `git-independent`, pycache purged) WITHOUT
re-running old suites as proof and WITHOUT copying fixture DBs into the packet.
R1/R2/A4 snapshots untouched. No ordinary commits. Machine binding in
`a-binding.json`; private intended-source manifest in
`private-source-manifest.json` (765 files, SHA256
`f5fa1269e932598aa2899bdfaff35146ada5066ca98b49f172f00e3ec82a99cb`).

## 1. Raw byte preservation (author raw, NOT preparer transcription)

- Targeted: `dm022-a5-path-targeted-raw.txt` (77 lines, 3381B, SHA256
  `7213b03deb2cacf460b90c1a5a4f5f255eb6216578b31c33dd57811823a74de6`,
  exit 0, 4/4 PASS). Covers: new str-vs-Path loader equivalence
  (`test_loader_accepts_str_path_same_as_path`), wrong-family str control
  (`test_loader_wrong_family_str_path`), C2 refresh healthy path
  (`test_weekly_refresh_validation_healthy_legacy_accepts_whole_path` — green
  after B Path-wrap + C2 schema-fixture + A normalization), release CLI
  (`test_cli_main_success_and_error` — REG-03 resolved).
- Full A suite: `dm022-a5-full-20261028.txt` (49 lines, 5357B, SHA256
  `d77d5776a5e942ab8b74509c4e7611461cfeadbe9b8cbbeb696ae1fa43578e0d`,
  exit 0, 25/25 PASS, ~26s). Same code, full regression for the shared-path
  normalization (not decoration: every normalized entry point is executed).
- Provenance: these txts ARE the author raw run outputs. Preparation commands
  that copied/hashed them are transcribed tool-observed and are explicitly NOT
  raw. Post-hoc hashing here is observation AFTER the run, NOT retroactive
  per-run proof; no lost raw is recreated.
- Supersedes: an earlier draft of this note described the stale
  `/tmp/dm022-a4p-path` run (exit 1, old SHAs `5102c874…` / `632d41f7…`,
  21 tests). That draft text was wrong for the final runs and is replaced
  here; the final raws above are the binding evidence.

## 2. Private source binding (current candidate + only A path files)

Private: `/tmp/dm022-a5p-priv` (765 intended files excl. `.git`/caches;
independent `.git` byte-copy from frozen A4 `git-independent`: 83 files,
0 symlinks, 0 inode overlap, inert origin, HEAD `409b292…`; no `__pycache__`;
fixture DBs were temp dirs per test and are NOT in this path).

A-owned path-normalization files (all priv == candidate-work):

- `scripts/survey_research_authority_v2.py` — `2aef837faaa5…`/155892B
  (LOW `_norm_repo_path` `_norm_rel_path`; `load_typed_checkpoint_record`
  accepts `str | PathLike`)
- `scripts/survey_prearchitecture_acceptance_v2.py` — `f8af03cc5d58…`/88603B
  (HIGH `_norm_repo_root` `_norm_rel_posix`; all entry points normalize)
- `tests/test_dm022_prearchitecture_acceptance_v2.py` — `a08265175a1e…`/80610B
  (2 new loader tests; 4 human-window tests from prior unit intact)

Unchanged: A-owned evidence helper (`8b55dc6c3289…`), fixture helper
(`7fdc692ccba6…`), all 5 schemas (byte-identical A4 == candidate == private);
B/C/C1/C2 files carried byte-identical from the idle candidate, untouched by A
(B Path-wrap + C2 schema-fixture fixes present as idle-candidate state).

## 3. Packet contents / limits

- `dm022-a5-path-targeted-raw.txt` (targeted 4-test raw)
- `dm022-a5-full-20261028.txt` (full 25-test A-suite raw)
- `private-source-manifest.json` (765 intended files; SHA256
  `f5fa1269e932598aa2899bdfaff35146ada5066ca98b49f172f00e3ec82a99cb`;
  fixture DBs/caches excluded, NOT copied into packet)
- `a-binding.json` (hashes, comparisons, runtime pins)
- This file. No Git DB in packet (`find -name .git` empty). No overwrite of
  prior artifacts. No test execution, no installs, no network, no Human commit
  readback. A unit ongoing (no Commit Point claimed).
