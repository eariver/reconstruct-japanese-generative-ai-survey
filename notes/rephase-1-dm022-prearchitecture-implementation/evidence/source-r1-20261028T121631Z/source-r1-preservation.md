# Source R1 preservation — rejected first-integration snapshot (freeze prerequisite)

Date: 2026-10-28 UTC. Preservation prerequisite to repairs. All 4 implementation
authors returned and STOPPED (per task premise). Root found a major incomplete
placeholder implementation in author A; this snapshot freezes that FIRST
integration source as rejected author R1 (NOT accepted) before any correction
edits candidate-work. Prior initial-preparation artifacts kept unchanged.
No runtime/tests executed. No Human commit readback (no git commands in
workspace reconstruct root).

## 1. Snapshot root (immutable-by-policy)

- `.../.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/snapshot-r1-20261028T121631Z/`
- `worktree/` — intended source + new authored files ONLY (756 files; no `.git`,
  no `__pycache__`, no `*.pyc`, no runtime residue; exact file inventory =
  `snapshot-r1-manifest.json` `files` keys)
- `git-independent/.git` — INDEPENDENT byte-copied `.git` for source provenance
  (`cp -a`, no `--link`/hardlinks; 83 files; 0 inode overlap with candidate
  `.git`; no alternates/commondir; inert `example.invalid` origin preserved;
  HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`; no commits/staging/config
  mutation)
- Policy: IMMUTABLE. Do not edit, clean, re-copy over, or delete. Corrections
  edit `candidate-work` only, never this snapshot. No Git DB in packet (snapshot
  lives under ignored runtime; evidence dir holds only manifest/logs/md).

## 2. Manifest (exact full SHA/bytes)

- Path: `notes/rephase-1-dm022-prearchitecture-implementation/evidence/source-r1-20261028T121631Z/snapshot-r1-manifest.json`
- SHA256: `f67ad9b6253324854823b04ef4c3dbf08b1cf046d0c1b9240dce09f8527200dc`
- Bytes: 149981
- Scope: 756 intended files, each `{kind, sha256, bytes, mode}` (`mode` =
  `oct(st_mode & 0o7777)`); sorted keys; excluded `.git`, `__pycache__`, `*.pyc`
- Execution record: `evidence/source-r1-20261028T121631Z/copy-commands.log`
  (actual commands + exits, tool-observed, durably saved; no saved-runner use)

## 3. Source copy check (status)

- PASS: snapshot `worktree` equals ALL current candidate intended bytes/modes:
  756/756 paths, 0 candidate-only, 0 snapshot-only, 0 SHA/bytes/mode/kind
  mismatches, 0 symlinks both sides.
- PASS: git independence: candidate `.git` 83 files vs snapshot `.git` 83 files,
  0 `(dev,ino)` overlap; no symlinks/hardlinks; no alternates/commondir.
- Candidate parent HEAD stays actual409 (file bytes `409b292…`); no ordinary
  commits/staging. Candidate intended count is now 756 (742 baseline + 14 new:
  2 modules + 5 schemas + 7 test/helper files across A/B/C1/C2).
- Bound: full all-entry comparison (756 worktree + 83/83 git files), no sampling.
  Mode compared as permission bits; times/uid/xattr not compared (expected copy
  difference). No reconstruct content inference; reconstruct untouched.

## 4. Root observations (recorded, NOT worker acceptance)

Root reviewed author A and found, preserved here as root observations (this worker
neither accepts nor re-verifies implementation correctness):

- A `_exclusive_write` uses replace-overwrite (root-flagged; correction must use
  exclusive create + verified byte-copy semantics per map).
- Fake content digests / automatic SATISFIED (root-flagged; correction must bind
  real content SHAs, no auto-pass).
- No-op resume (root-flagged; correction must implement explicit bound-intent
  resume per §7, not a silent success).
- pytest-only instructions contrary to repo unittest (root-flagged; repo tests
  observed stdlib unittest — see preparation appendix; correction tests run via
  `python -m unittest`, not pytest-only).

First author returns (`author-A/B/C1/C2-return.md`) are KEPT UNCHANGED as rejected
R1 evidence. Superseding corrections append later; no overwrite of R1 returns or
of `source-preparation*` / appendix artifacts.

## 5. Worker-activity assumption + next

- Assumption: no other worker edited `candidate-work` during copy+verify (authors
  STOPPED per premise; 0-mismatch post-copy supports quiescence but does not
  prove continuous isolation).
- Once this snapshot is durably saved (manifest hash above), corrections MAY edit
  `candidate-work`. This preservation task makes no candidate edits and claims no
  implementation acceptance. Whole NOT_READY/DM021+022 OPEN preserved except
  implementation progress; independent implementation review still required.
