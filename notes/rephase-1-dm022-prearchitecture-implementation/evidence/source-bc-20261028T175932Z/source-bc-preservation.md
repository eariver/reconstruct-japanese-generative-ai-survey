# Source BC preservation — fixed 756-base regression snapshot (758 current minus 2 longitudinal)

Date: 2026-10-28 UTC. All authors idle. Current `candidate-work` has 758 intended files including 2 new longitudinal witness files owned solely by witness author (will only edit own 2). To avoid capturing while changes, regression source base is 756 files with exact exclusion of ONLY those 2. No Human readback, no ordinary commits, no source edits by executor.

## 1. Snapshot root (immutable-by-policy)

- `.../.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/snapshot-bc-20261028T175932Z/`
- `worktree/` — 756 files (758 current minus 2 excluded; no `.git`, no `__pycache__`, no `*.pyc`)
- `git-independent/.git` — byte-copied `.git` (`cp -a`, no `--link`; 83 files; 0 `(dev,ino)` overlap with candidate `.git`; no alternates/commondir; inert `example.invalid` origin; HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`)

## 2. Exact exclusion (ONLY these 2, witness-owned, will change separately)

- `tests/test_dm022_full_lifecycle_v2.py` (63094B at freeze)
- `tests/dm022_lifecycle_fixture_v2.py` (3892B at freeze)
- ALL other runtime/tests stable (756-base manifest vs candidate-minus-2: 0 only-either-side, 0 SHA/bytes/mode mismatches).

## 3. Manifest

- Path: `notes/rephase-1-dm022-prearchitecture-implementation/evidence/source-bc-20261028T175932Z/snapshot-bc-manifest.json`
- SHA256: `e7d9235ac958f7efd219ed589bad205f3ae6340d45bd49c85a1837d64eca0bae`
- Bytes: 149939; entries: 756
- Excluded: `['.git','.git/*','__pycache__','*.pyc','tests/test_dm022_full_lifecycle_v2.py','tests/dm022_lifecycle_fixture_v2.py']`

## 4. Checks

- SNAP worktree 756, SNAP git 83, HEAD matches candidate, no alternates, git overlap 0.
- Exec `exec-bc-20261028T175932Z` from snapshot: 756 files, 83 git, 0 overlap with snapshot git, 0 manifest mismatches, 0 pycache.
- Separate witness copy (longitudinal author `/tmp` private) NOT used; old A4/R2 exec/logs NOT reused.
