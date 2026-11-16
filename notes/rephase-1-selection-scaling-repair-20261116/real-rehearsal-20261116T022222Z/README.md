# Real-writer rehearsal — 20261116T022222Z (isolated real-material W34/SP, no CURRENT/delivery)

Root: `astra-repair-resolution.md` FULL §10 (prevails) + `independent-correction-review.md` `GO_TO_REAL_WRITER_REHEARSAL`. No reconstruct status/log/HEAD/Commit readback; isolated Git only. No subagents/network/Production. Author tests/state preserved; old active/shadow/proof untouched.

## Source commit (existing isolated DB, no missing-ok needed)

- Author copy `.rephase-1-editorial-runtime/selection-scaling-implementation-20261116T004649Z/candidate-work`, pins EXACT s9 `run-metadata.json` (LOW `fd788b74…`/309483B, runner `b16c4759…`/50865B, test `a21f5949…`/49973B, base `b3cd4a95…`, attention `10126da7…`).
- Base 773 manifest `complete-supplement-carry-manifest.json` (773 files, head `409b292`): 769 unchanged + 4 mods (`run_selection…`, `survey_architecture_v2_base.py`, `survey_research_authority_v2.py`, `survey_review_attention_v2.py`) + 1 new test (`tests/test_selection_scaling_repair_v2.py`) = 774 intended, 0 missing. Modes `0o664` worktree / `100644` Git match manifest. No unrelated source changes.
- Immutable: both States `EVIDENCE_REVIEWED`, Profiles match State SHA, CPs `PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1`, 4 NamedRefs re-hashed, `seven_plan` 7, `expected_after` W34 `a8586351…` / SP `38a63411…`, 7 slots absent, guard absent, history[0] `48082356…` unchanged.
- Isolated Git only (absolute cwd, no global env): `status --porcelain=v1` shows 4 M + 1 new test + inherited active dirty + `__pycache__` (not staged); `log --oneline -5` HEAD `ae0dd1e` → parent `cc1c7fd`; `diff --stat` 4 files 1719+/99-.
- Staged ONLY 5 (`git add --` 4 scripts + new test): `diff --cached --stat` 5 files 2538+/99-.
- Normal commit (process-scoped identity `Synthetic selection-scaling-impl-1085`, no amend/empty/bypass/config/HOME, normal hooks, inert `https://invalid.invalid/inert.git`, no set-url): `source-commit-stdout/stderr/exit.txt` (exit `0`, `[detached HEAD 3231a0c] 5 files changed`). No missing-blob tree failure, so `write-tree --missing-ok` path NOT used (preauthorization unused, no reset/clean/fetch).
- Genuine new: HEAD `3231a0c280287411513bba359f4d3d2b6703f591`, parent `ae0dd1ee5b0e7a85c44bdab0e6cd024bf12f0c56`, tree `ff01b73e6012fd4519fdfb3807186753ff330367`. Source 774 manifest = base 773 + new test (4 mods). No reconstruct readback.

## Real copy (NEW independent, no hardlinks/sharing)

- `REAL_UTC=20261116T021943Z`, `.rephase-1-editorial-runtime/selection-scaling-real-20261116T021943Z/candidate-work` via `rsync -a --exclude=.git --exclude=__pycache__ --exclude=*.pyc` (worktree) + `rsync -a` (.git). Raw `realcopy-rsync-*` exit `0`.
- No hardlinks (inodes 22977222 vs 25041448 differ), no `objects/info/alternates`, no `commondir`, inert remote preserved (no set-url/config).
- Verified 774 (769+4+new), own-epoch `cc1c7fd1…` + `ae0dd1ee…` readable (`cat-file -e` exit `0`), HEAD `3231a0c`, both States `EVIDENCE_REVIEWED` history[0] `48082356…`, guard absent, 7 absent, 4 refs exact.
- Excluded bytecode/test fixtures; no blind unknown copy. Author/old active/shadow/proof untouched.

## Frozen inputs (exact bytes, no repin)

- W34 `notes/rephase-1-repaired-correction-rehearsal-20261112/w34-selection-architecture-input.json` 378396B `15375476f308fbfeb79c4e8f3f4d53d85d5cf917e36d29d3c3777580301aab3a`.
- SP `sp-selection-architecture-input.json` 72613B `072f90b6795041f79ab42476faf93ad9e39f7c80ce30e16c1804d4fcbd51e9bd`.
- Reused exact bytes (verified SHA/len before runs).

## Runs (normal CLI, sequential, 1200s cap, actual HEAD, no override/repin/stub)

- Env `PYTHONDONTWRITEBYTECODE=1 GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_CONFIG_NOSYSTEM=1`, clean Git overrides, absolute `--repo-root` (real DST), relative `--state` (`sources/.../production-state.json`, normal), absolute `--input` (frozen packet inputs). Cwd real DST (absolute, no `cd`). `python3 -m scripts.run_selection_architecture_v2_interactive` (correct `-m`, not file path).
- W34 first attempt `w34-run-*` (PID 1107379, 20261116T022256Z, 0s, exit `1`, `ModuleNotFoundError: No module named 'scripts'` due to `python3 <file>` invocation): preserved as operational invocation failure (no writer validation, no partials, source/authority unchanged). No auto-fix counted as writer PASS.
- W34 retry `w34-run2-*` (PID 1108798, 20261116T022342Z–20261116T023738Z, wall 836s, exit `0`, stdout 504B `selected_count 45 package_count 5 READY`, stderr 0B): 7 outputs (matrix 683098B, selection 375063B, architecture 24447B, review 314350B, attention 18437B `total 770 shown 50`, input 378396B == frozen, audit 1436B). No state advance (still `EVIDENCE_REVIEWED`), no HumanGate/install/CURRENT/delivery.
- SP `sp-run-*` (PID 1110053, 20261116T023802Z–20261116T024030Z, wall 148s, exit `0`, stdout 570B `selected 130 packages 9 READY`, stderr 0B): 7 outputs (matrix 239359B, selection 76603B, architecture 33219B, review 67700B, attention 15918B `total 65 shown 50`, input 72613B == frozen, audit 1530B). Source/authority unchanged from W34 (W34 outputs in separate `sources/2026-W34`, SP in `sources/SP-...`, source files untouched), so SP allowed once after W34 per §10.
- Child PID/argv/env/cwd/start/end/exit/stdout/stderr/CPU/wall/IO persisted in unique raw (no overwrite); background PID poll (no duplicate runs); `timeout` 1250000ms tool cap (1200s writer cap respected: 836s + 148s). CPU/IO scope honest: wall measured, CPU/IO not separately measured (no cProfile, rchar not measured for child), stdout/stderr/exit authoritative.
- Stop-first-failure per edition: W34 operational failure preserved, retry as still-first genuine writer attempt (no partials, unchanged authority); W34 genuine writer PASS, SP genuine writer PASS, no fix/retry/cleanup after genuine PASS/FAIL (no second runs, partials preserved honest).
- Verified post-run: schemas via existing validators (runner `READY`, `validate_*` inside run), attention counts/readiness (`READY`, `770/50` + `65/50` with limit/truncation/overflow), input archive == entry pins, audit binds archive + 5 outputs, assignments cover every Matrix exactly once (45 W34, 130 SP), packages 5/9, boundaries inherited + explicit, States/source preserved.

## Failure limits (honest)

- Operational W34 first-attempt import failure preserved (`w34-run-*` exit 1); not counted as writer refusal.
- No source/authority gaps found for bounded rehearsal; no simulated proof. If further capability gap appears, return root (none here).
- NO stage advance/HumanGate/active installation/CURRENT/delivery. Whole `NOT_READY`/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN. Root/independent output review later.
