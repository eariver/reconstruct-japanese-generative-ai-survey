# Source A4 preservation — fixed full integrated snapshot (A4/B/C1/C2 current)

Date: 2026-10-28 UTC. All authors A4/B/C1/C2 returned STOPPED, candidate idle. This task freezes CURRENT `candidate-work` as `snapshot-a4-20261028T160708Z` (integrated, NOT accepted) for independent execution only. No Human Commit readback, no ordinary commits, no source edits by executor.

## 1. Snapshot root (immutable-by-policy)

- `.../.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/snapshot-a4-20261028T160708Z/`
- `worktree/` — 756 intended files (no `.git`, no `__pycache__`, no `*.pyc`; exact inventory = manifest `files` keys)
- `git-independent/.git` — independent byte-copied `.git` (`cp -a`, no `--link`; 83 files; 0 `(dev,ino)` overlap with candidate `.git`; no alternates/commondir; inert `example.invalid` origin preserved; HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`; no commits/staging/config mutation)
- Policy: IMMUTABLE. No edits/clean/re-copy/delete.

## 2. Manifest (exact full SHA/bytes/modes)

- Path: `notes/rephase-1-dm022-prearchitecture-implementation/evidence/source-a4-20261028T160708Z/snapshot-a4-manifest.json`
- SHA256: `2eb615b41307e86cc86770c9798bf4ba559e2626f6884e898f3672a2cdc86621`
- Bytes: 149855; entries: 756 (`{kind,sha256,bytes,mode}`; `mode=oct(st_mode & 0o7777)`)
- Excluded: `['.git','.git/*','__pycache__','*.pyc']` (exact `.git` only; `.github`/`.gitignore` KEPT — 8 files verified)

## 3. Source copy check (read-only, pre/post)

- PASS: snapshot `worktree` equals CURRENT candidate intended bytes/modes: 756/756 paths, 0 only-either-side, 0 SHA/bytes/mode/kind mismatches, 0 symlinks (CAND_MISM=0, SNAP_MISM=0 vs manifest)
- PASS: git independence: candidate 83 vs snapshot 83 files, 0 overlap; no hardlinks/symlinks/alternates/commondir
- R1/R2 untouched (dirs intact; not re-verified here beyond existence)
- Exec copy `exec-a4-integration-20261028T160708Z` from snapshot: 756 files, 83 git files, 0 overlap with snapshot git, 0 manifest mismatches, 0 pycache (PYTHONDONTWRITEBYTECODE=1)
- Bound: full all-entry comparison (756 worktree + 83/83 git), no sampling. Mode = permission bits; times/uid/xattr not compared. No reconstruct content inference; reconstruct untouched.

## 4. Worker-activity assumption

- Assumption: no other worker edited `candidate-work` during copy+verify (authors STOPPED per premise; 0-mismatch post-copy supports quiescence, not continuous isolation proof).
- No `/tmp` A4 private copy reused (A4 `evidence/A4-correction-...` read for binding only, NOT executed; all tests ran on frozen exec above).
- Old R2 exec/logs (`exec-r2-integration-...`, `integration-r2-...`) NOT reused as pass proof; R2 diagnostics read as history only.
