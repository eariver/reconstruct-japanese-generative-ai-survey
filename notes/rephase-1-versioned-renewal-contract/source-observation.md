# Versioned renewal — source observation (Worker A, historical-vs-current authority)

2026-10-23 JST. Worker A scope only: historical-vs-current CODE/TOOL authority + source availability. No operator 2-case / review-reuse (other Worker). No consumer/R1-compat audit (Explore). DESIGN/CONTRACT SELECTION only per `outputs/rephase-1-editorial-operation-implementation-assessment.md §5`. No source edits/tests/imports/build/fixture/Git writes/network/old runners in this unit.

Editor: `apply_patch` unavailable in this environment; new files written via dedicated `Write` file tool (not shell heredoc/echo). No existing files edited.

Governing (read, not re-argued): contract `d880f53e…` (`outputs/rephase-1-editorial-operation-contract-decision.md`), assessment `outputs/rephase-1-editorial-operation-implementation-assessment.md`, `notes/rephase-1-editorial-operation-implementation/astra-closeout-resolution.md`, `independent-final-operation-resolution.md` WITH `independent-final-packaging-resolution.md`, `independent-final-reader-visual-inspection.md`. Contract d880 unchanged.

## 1. Observation scope and method (transcribed, not saved-raw)

All commands below were tool-observed read-only in this session. No raw stdout/stderr/exit files were persisted for this unit; values are transcribed here. This is NOT a saved-raw/all-entry proof and NOT a general guard/isolation certification.

- No `python -c` imports of repo `scripts.*`. One stdlib `json.load` of the packaging manifest was executed once to echo `m['patch']` (no repo-code import, no `__pycache__` created). All other checks used `git --no-optional-locks`, `ls`, `sha256sum`, `grep`, `wc`, `Read`/`Grep` (no execution).
- `PYTHONDONTWRITEBYTECODE=1` sanitization and `GIT_*` unset were NOT re-applied per-invocation here because no packaging GEN/PROOF writes were performed; packaging-time sanitization is a Worker record in `source-packaging/README.md §4`, not re-certified here.
- No cache reads, no `__pycache__` traversal, no TeX/Python runtime bundling claims.

Actual commands (transcribed exits: all 0 unless noted):

1. `git --no-optional-locks rev-parse HEAD` / `HEAD^{tree}` / `log --oneline -3` / `remote -v` / `status --porcelain=v1 --untracked-files=all` in `.rephase-1-editorial-runtime/final-source-packaging/proof-copy/candidate-partial-b40de60`.
2. Same `status` tail + `wc -l` + `diff --cached --name-only | wc -l` + `diff HEAD --name-only | wc -l` in proof-copy.
3. `git --no-optional-locks rev-parse HEAD`, `rev-parse HEAD^{tree}`, `status --porcelain=v1 --untracked-files=normal` in workspace root.
4. `ls -lh …/complete-r3-operation-409.patch; sha256sum …; grep -A … manifest` (patch + 2 pins + count).
5. `sha256sum scripts/…` + `wc -c` in proof-copy (5 key files, 2 sizes).
6. `grep -c '"bytes":' …/complete-r3-operation-manifest.json`.

## 2. Reconstruct HEAD (Human commit point)

- `rev-parse HEAD` → `8f775714fa2dd85ce863e690c7d111d2c99a79e5` (matches task premise Human `8f77571`).
- `rev-parse HEAD^{tree}` → `04ffa24e3c2cc036436806777636c5640919017b` (transcribed).
- `status --porcelain=v1 --untracked-files=normal` → empty, count `0` (clean; transcribed).
- No claim about full-tree object hydration, no million-deletion inventory. Scope is exactly the two commands above.

## 3. Available intended source (read-only, do NOT restore)

Path: workspace `.rephase-1-editorial-runtime/final-source-packaging/proof-copy/candidate-partial-b40de60` (workspace-ignored scratch per `workspace-runtime-decision.md`; EDQUOT history retained in closeout).

- `rev-parse HEAD` → `409b292756dd1277b9dfae87679934c0d2ce251c`.
- `rev-parse HEAD^{tree}` → `8ce3699861505f32d1d60bdc185d4d4f635aedb2`.
- `log --oneline -3` → `409b292 DM-004 final cleanup …` / `34f934e …` / `c4aa3b5 …` (DM004 lines; transcribed, not re-validated).
- `remote -v` → `origin https://example.invalid/rephase-candidate-recovery.git (fetch/push)` (inert; transcribed).
- `status --porcelain=v1 --untracked-files=all` → `57` entries = `25M + 32A` (transcribed counts):
  - `diff --cached --name-only | wc -l` → `0` (index clean; apply was without `--index`, per packaging README §4).
  - `diff HEAD --name-only | wc -l` → `25` (tracked modified).
  - Remainder `32` untracked new (inferred `57-25`, filenames observed `?? schemas/…`, `?? scripts/…`, `?? tests/…`).
- This is the APPLIED proof-copy state (post single direct `apply`), not the scoped-clean pre-apply state. Scoped-clean `689 + 32-absent` and `apply --check 0 / apply 0` are packaging Worker records (`source-packaging/proof-apply-check-exit.txt:0`, `proof-apply-exit.txt:0`, `proof-before-721-stdout.txt:fails=0/total=721`, `proof-after-721-stdout.txt:fails=0/total=721+delta57`), adopted here as records, NOT re-executed.
- No blind copy of untracked residue. DST `/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/…` (60 raw incl. notes/cache/tmp residue) was NOT read here; use manifest-selected 57 only.

## 4. Corrected manifest + patch pins (adopted, spot-verified)

Manifest: `notes/rephase-1-editorial-operation-implementation/source-packaging/complete-r3-operation-manifest.json` (555 lines, FULL valid JSON per `manifest-valid-stdout.txt:manifest valid FULL`, adopted as Worker record).

- `head: 409b292…`, `head_tree: 8ce369…`, `snapshot_head: 721a04d85532d7855f3e54cc411f5847c787726e`, `snapshot_tree: ac7cb0bd2e977b46e957450816eddd779799e144`, `intended_721: 721`, `intended_721_verified: true`.
- `delta_count: 57`, `tracked_modified: 25`, `untracked_new: 32`, `status_summary: 25M+32A=57 (raw 60 incl. notes/pycache/tmp excluded; LC_ALL=C sorted)`.
- `patch: {path: complete-r3-operation-409.patch, bytes: 2018112, sha256: 659063dc27f0926aaf6e8a33f322937076563c4a23f6cf0d80ca970e1b2abd5b}`.
- `proof.scope: scoped 689 tracked at HEAD + 32 absent (sources/surveys 31466 outside scope); final 721 exact + delta 57; HEAD stays 409, no commit/new ancestry`.
- `notes:` partialDB 26309 missing retained (not full-history cert); runtime unbundled; whitespace warnings preserved; Git `100644` vs physical `0o664` recorded separately.

Patch file observed (transcribed):

- `ls -lh` → `2.0M`, `sha256sum` → `659063dc27f0926aaf6e8a33f322937076563c4a23f6cf0d80ca970e1b2abd5b` == manifest `patch.sha256`. Byte count `2018112` per manifest `patch.bytes` (not re-`stat`-verified here; `ls` showed `2.0M` only).
- `grep -c '"bytes":'` → `58` = 57 files + 1 patch entry (consistent).

Spot pins vs live proof-copy bytes (transcribed `sha256sum`, manifest `grep -A7`):

- `scripts/survey_publication_set_v2.py`: observed `ecd7facac09a5c977396803e130d600b75a441767d87ea585024f38c490bfb8a`, bytes `127802` == manifest `sha256` + `bytes` (match).
- `scripts/survey_editorial_retention_v2.py`: observed `036d258fa58fc876956c79cae9f51b861a731b3128a73084af921ead28a52771` == manifest `sha256` (match; `bytes 122624` per manifest).
- `scripts/survey_editorial_publication_v2.py`: observed `98f8ff8bb74f5fc0899f4adb5795953ca4513617e1075afaedada6bf89ec5dc4` (manifest key exists; full equality not re-diffed here beyond this row).
- `scripts/survey_editorial_staged_source_v2.py`: observed `0fb23e83caec01f7d94a80bdaaa5714741d9d8c6496a0f630d99e06c206ea355`.
- `scripts/survey_editorial_current_authority_v2.py`: observed `fcbeee43ceaac80d16b2b9afceee784321f7ccca2cf80e250d718eb5e4eaed5d`.
- Full 57 SHA/bytes/mode vs `SNAP721` equality is a packaging proof record (`proof-after-721-ok.txt`, `snap-721-pins-stdout.txt:SNAP721 fails=0/total=721`, `src-snap-57-equal`), NOT re-hashed here. No claim of full 57 re-hash in this unit.

## 5. Availability + limits

- Available: reconstruct HEAD `8f77571` clean; actual409 `409b292/tree8ce` + intended57 at proof-copy (applied state, 57 delta visible); corrected manifest + patch `659063dc…/2018112B`; SNAP R7b `721a04d/treeac7cb0` (Worker record, not re-observed here).
- Missing/out-of-scope: `sources/surveys` bulk 31466 (unchanged, not in patch); full hydrated/tree-clean certification; missing26309 blobs/history; unbundled TeX/Python; `proof-copy/.git` census not walked here; no inode/hardlink/no-alternates re-certification (packaging-time observation only).
- Dirty-root distinction: reconstruct root clean (`0`); proof-copy dirty by design (`57` applied overlay); SNAP vs DST HEADs distinct (`409b292` vs `721a04d`); Git `100644` vs physical `0o664` distinct per manifest (no faking equal).
- Do NOT restore available source, do NOT run old runners, do NOT claim full-status million-deletion inventory, do NOT certify guards/isolation/continuity/CAS/rerunner.
- Old-ancestry note: proof-copy HEAD `409b292` is detached candidate base (NOT fixed Production baseline `774dd39a`); no e4/481 ancestry claim; four portable parent inputs + complete57 DIRECT apply per AGENTS.md governs any future restore (not executed here).

## 6. What this observation supports (and does not)

Supports: Worker A historical-vs-current analysis may cite proof-copy paths/lines as CURRENT code under analysis, manifest/patch pins as intended57 identity, and transcribed HEAD/tree/status as availability bounds.

Does NOT support: full-matrix PASS transfer, old-epoch validator validity after a Core change, handoff-build success, public-cycle forgery, actual R1×33, genuine Human approval, or Production readiness. WholeNOT_READY / step4B3OPEN / audit-unstarted / DM021+022OPEN unchanged.
