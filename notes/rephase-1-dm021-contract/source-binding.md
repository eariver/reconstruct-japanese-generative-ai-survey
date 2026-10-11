# DM-021 contract analysis — honest source-binding record

2026-10-10. General read-only Co-Worker. Packet `notes/rephase-1-dm021-contract/`.
Task `task.md` + AGENTS + LF-2I assessment/qualifications + DM-021 intake read fully.

## Identities observed (read-only, no mutation)

- Reconstruct: HEAD `c50be33a0f1508c0ce306827d10a7c7746001384` (`git rev-parse HEAD`).
  `git status --porcelain=v1` shows only `?? notes/rephase-1-dm021-contract/`
  (this packet); no other dirty/tracked changes observed at analysis time.
- Source worktree `/tmp/opencode/jgas-lf2-design-20261009T113013Z`:
  HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`,
  tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`,
  parent `34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4` (`git rev-parse`, `log --oneline -1`).
- Worktree delta: `git diff --name-status/--stat HEAD` shows exactly 2M tracked
  (`schemas/reader-surface-gate-v2.schema.json`, `scripts/survey_reader_surface_gate_v2.py`);
  `git status` additionally shows 7 untracked LF-2I source paths + `__pycache__`
  caches (disclosed, not authority). Total 2M+7A overlay as claimed.
- All 9 overlay SHA256 re-hashed via `sha256sum` and match
  `evidence-20261010T120000Z-correction3/hash-manifest.json` and the task pins:
  publisher `4d235a38…`, test `4a03b564…`, derivation `c09c5558…`,
  helper/generated `d480e11d…`, Gate `e7305884…`, plus `fe4a96f4…/4dadf873…/7bae9d2a…/ce687447…`.
  Complete-patch `5c7e7503…` not re-applied here (independent apply proof already
  saved at `/tmp/opencode/jgas-lf2i-409bytecopy-20261010T033640Z`).

## Commands used (no routing overrides, no fetch, no writes to source DB)

- `git -C <reconstruct> rev-parse HEAD`, `status --porcelain=v1`.
- `GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 git -C <source> rev-parse HEAD / HEAD^{tree} / log --oneline -1 / status`.
- `GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file git -C <source> diff --name-status/--stat HEAD`.
- `sha256sum` on the 9 overlay paths. Read-only `read/grep` of source files
  listed in `analysis.md` with file/line citations.
- No new copy/recovery, fixture/test/build execution, refs/branches/commits,
  source DB mutation, old proof/runner scripts, network calls, empty commits,
  or current-main/Main/Summary/Issues/primary-record/corpus acquisition.

## Evidence reuse and limits

- DM-021: reused saved Summary `afdb3df3faa20af3bb5798be429bba8dbd2100b1` /
  blob `62ee6a6b9792cc96e42f378c5cff67faebaeef43` / SHA256 `7c84b6d8…`,
  lines 690–727, plus `README.md`/`astra-disposition.md` static pins
  (`survey_agent_control_v2.py:45,1789-1790`, `publication-surface-revalidation.schema.json:26`).
  Re-corroborated statically by direct reads in this unit.
- TS-003/Issue560/PR561/run37955511006/edition artifacts: reported-secondary only,
  not opened/adopted. Fixed baseline `774…` unchanged; no rebaseline.
- LF-2I assessment `outputs/rephase-1-longform-lf2-implementation-assessment.md`,
  `astra-closeout-qualification.md`, `independent-closeout-supplement.md` read;
  43+2 method claims cited as bounds, not re-executed or transferred.
- Static analysis only: normal-continuation stale-rejection (§6) is conceptually
  proved from exact-SHA bindings, not an executed correction witness. No
  print-only script is advertised as a guard. New files in this packet only:
  `analysis.md` (234 lines), this record.
