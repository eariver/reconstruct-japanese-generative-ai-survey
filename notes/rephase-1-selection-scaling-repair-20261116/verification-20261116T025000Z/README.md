# Affected regression verification — 20261116T025000Z (bounded, no source edits)

Root: `astra-repair-resolution.md` FULL §§6–11 (dispatch §11.2). Source frozen 3231a0c280287411513bba359f4d3d2b6703f591 parent ae0dd1e tree ff01b73e, 774 = old773 (769 unchanged +4 mods) +1 new test. No reconstruct Git/status/log/HEAD/readback, no ordinary commit/network/Production/configHOME/source edits/subagents. SOURCE FROZEN, no fix-and-retry.

## Workspaces (NEW independent, ignored runtime)

- VERIF copy `.rephase-1-editorial-runtime/selection-scaling-verification-20261116T025000Z/work` via `rsync -a --exclude=.git --exclude=__pycache__ --exclude=*.pyc` worktree + `rsync -a` .git (no `-H`, no hardlinks). Inodes differ (author 22977222 vs verif 25053990 for LOW), no `objects/info/alternates`, no `commondir`, inert origin `https://invalid.invalid/inert.git` preserved (no set-url/config). No empty/amend/hook-bypass. Harness `run_affected_regressions.py` NEW via Write only (no shell text editing), executed with `PYTHONDONTWRITEBYTECODE=1 GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_CONFIG_NOSYSTEM=1` + cleaned `GIT_CONFIG_GLOBAL=/dev/null GIT_TERMINAL_PROMPT=0`.
- Fixture Git/tools inspected before use: `tests/dm022_lifecycle_fixture_v2.py` (process-scoped `-c` identity, inert example.invalid, no `git config` writes, never `--allow-empty`, checks `GIT_DIR` overrides, `add -A` + commit) and `tests/test_survey_evidence_v2.py::sandbox` (same process-scoped identity, inert origin, refuses empty commit, checks inherited Git-root overrides). Historical runners not executed; reused current published helpers with honest bindings (loaded-file tracking in CURRENT proof, not here).

## Batches (durable unique raw, source774 pre/post verified)

- **batch1-initial-8pass-2chainfail** (`raw/batch1-initial-8pass-2chainfail/`): 10 selected (runner2 + attention2 + agent_tool2 + architecture_v2 chain2 + direct_operation2). Result 8/10 PASS, 2 ERROR in `test_survey_architecture_v2` chain (`IMPLEMENTATION_SHA="4"*40` vs sandbox real HEAD → `ValueError: implementation commit differs...`). Preserved as pre-existing fixture-SHA mismatch, not 3231 regression (same chain fails for cross-package expansion, 6/7 with same error). Raw: `run-argv.json/cwd/env/pid/start-utc/start-epoch/end-utc/end-epoch/exit/stdout/stderr/wall`, `source774-pre/post.json` (5 pins OK), `author774-check.json` (OK).
- **batch2-corrected-10pass** (`raw/batch2-corrected-10pass/`): replaced 2 chain tests with `test_survey_architecture_cross_package_synthesis_v2` (2 passing, base architecture synthesis contract, covers `survey_architecture_v2_base` via synthesis). Final 10/10 PASS, exit 0, wall 5s, PID 1152359→1152354 (see `run-summary.json`), pre/post/author OK. Selected:
  - runner: `test_matrix_discovery_map_requires_one_discovery_per_candidate`, `test_input_requires_exact_assignment_coverage`
  - attention: `test_attention_is_bounded_with_explicit_overflow`, `test_attention_basis_drift_fails_closed`
  - agent_tool (LOW direct-agent readback, historical wrapper): `test_archived_screening_may_revalidate...`, `test_archived_evidence_may_revalidate...`
  - base architecture: `test_architecture_accepts_exactly_one_final_empty_synthesis_package`, `test_architecture_rejects_empty_synthesis_without_factual_placement`
  - LOW direct operation: `test_c_direct_weekly_prepare_adopt_readback`, `test_c_derived_weekly_true_r_not_equal_e`

No unnecessarily full suite, no test install/pycompile. Each batch raw src pin/argv/cwd/env/PID/start/end/exit/stdout/stderr durable unique; source774 pre/post verified (5 pins 10126da7…/b3cd4a95…/fd788b74…/b16c4759…/a21f5949…).

## Limits

- batch1 2 chain errors preserved (unrelated dummy-SHA fixture, not 3231 defect). No autofix, no code repeat, no cleanup. Real new copy `.rephase-1-editorial-runtime/selection-scaling-real-20261116T021943Z/candidate-work` untouched. Old proofs/sources/evidence/caches preserved.

## Errata 2026-11-16 — preexisting claim now cites parent control only (doc-only, raw preserved)

Original §Batches claim “pre-existing… (same chain fails for cross-package expansion, 6/7)” is superseded as sole proof (preserved as history). Actual parent control `regression-supplement-20261116T141000Z` (a) proves preexisting for only these 2 methods: same 2 ERROR `ValueError: implementation commit differs…` on old773 ae0 (`old-parent-exit.txt` 1, `old-parent-stderr.txt`) with 773/773 bind vs `a7e40c47…`. Cite parent control only these 2 methods; do NOT extend to other chain tests without control. Original batch1/2 raw unchanged.
