# DM021-P1 Phase A — NEW fail-closed offline restore + overlay procedure

2026-10-11T16:00:37Z authored. General worker. No old restoration/proof
wrapper is executed; `restore.sh` / `restore_dm004final.sh` were read as
reference only. No `git archive`, no fresh-root substitute, no empty commit,
no new candidate branch/commit, no network, no hydration/fetch.

## Inputs (all 5 re-hashed fresh 2026-10-11T16:00:37Z — all match)

| # | Input | SHA256 |
|---|---|---|
| 1 | `notes/rephase-1-candidate-recovery/m3-20261003T0445Z/candidate-partial-b40de60.tar.gz` | `faf6792faf37ad30af2dbd7203b8896ca00964a91d00623a4f01278f2ade9f3c` |
| 2 | `notes/rephase-1-dm001-019-implementation/evidence-final-20261003T145621Z/20-packaging/successor-pack.pack` | `2c2a8e6f2ab5fbd71b6cddfe5d875e4a821d09ef54ba9714eaab12e438e81a99` |
| 3 | `notes/rephase-1-dm003-w1-implementation/evidence-20261004T072423Z/w1-222-to-e1705b7.pack` | `97d384fe8f7216f110cd401d1279129da83fab2000f28c24a73abe0b177b0fd9` |
| 4 | `notes/rephase-1-dm004-implementation/evidence-20261007T131353Z/dm004final-e1705b7-to-409b292.pack` | `e3d941653eadf2459a13f1b85b9fbbffd819f0a0ad6bb77eb121b2cba02279bf` |
| 5 | `notes/rephase-1-longform-lf2-implementation/evidence-20261010T120000Z-correction3/complete-overlay.patch` | `5c7e7503851f5cdbc30b6827560219f48ce75d4a6cf64ba13516ed97e0cea4f9` |

## Destinations (exclusive, verified absent before use)

- Worktree: `/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z`
  (`DEST_ABSENT_OK` observed before creation). Repo root after extraction:
  `$DEST/candidate-partial-b40de60` (`.git` + worktree, no moves).
- Evidence: `notes/rephase-1-dm021-p1/evidence-20261011T160037Z-phaseA/`
  (`procedure.md`, `phaseA_restore.sh`, `phaseA_overlay.sh`, `raw/`).

## Fail-closed gates (in execution order, any failure stops, no repair)

R1. Git route isolation: unset `GIT_DIR/WORK_TREE/PREFIX/INDEX_FILE/
OBJECT_DIRECTORY/ALTERNATE_OBJECT_DIRECTORIES`; export
`GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file`,
`GIT_CEILING_DIRECTORIES=/tmp/opencode`. No `--global` config touch,
no hook bypass flags, no remote fetch. Human git config untouched.
R2. Archive verified BEFORE extraction: full member listing; every member
under single topdir; no absolute path; no `..`; type flags only
regular/dir (reject symlink/hardlink/device/fifo/socket on sight);
duplicate member names abort; `.git/FETCH_HEAD` presence aborts.
R3. Extraction only into the absent exclusive DEST; `.git` must exist
after extract or abort.
R4. Imported config/hooks inspected locally (`cat .git/config`,
`ls .git/hooks`) before any git-aware op. Remotes must be inert
(`example.invalid`) — any live URL aborts before pack import; no fetch.
`objects/info/alternates` must be absent; no hardlink/object sharing
with the reconstruct workspace DB (dev,ino comparison, shared must be 0).
R5. Packs imported in order 20→7→32 via `git unpack-objects` from stdin
(no server, no fetch). Required commits `222a37e` (DM001/019),
`e1705b7` (W1), `409b292` (DM004 final) must each `cat-file -e` or abort.
R6. Select already-existing `409b292…` via detached checkout
(`git checkout --detach`, NO new branch/ref, NO commit). Verify
HEAD=`409b292756dd1277b9dfae87679934c0d2ce251c`,
tree=`8ce3699861505f32d1d60bdc185d4d4f635aedb2`,
parent=`34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4`, available chain
`409→…→e170→222→…→b40→774`, `status --porcelain` clean. Sparse-absent
paths stay sparse (no hydration, no fetch); missing-blob vs
sparse-absent recorded as distinct.
R7. Overlay: preconditions HEAD==409 + clean status re-checked; saved
patch `git apply --check` must pass silently; then `git apply`
(worktree only, index untouched). All 9 file SHA256 must equal the
correction3 `hash-manifest.json`; modes recorded against manifest
(`664` under umask 002); `status --porcelain` must show exactly
2 modified + 7 new (`2M7A`).
R8. Every command's argv/stdout/stderr/exit saved under `raw/`; failed
attempts preserved under unique names, never edited post-execution.
Runtime inspect-only (`python3 --version`, no app imports, no tests).

Machine: ShakeAIWS, Linux 7.0.0-38-generic x86_64, git 2.53.0,
python3 10.x probe at runtime step (recorded in raw log).
