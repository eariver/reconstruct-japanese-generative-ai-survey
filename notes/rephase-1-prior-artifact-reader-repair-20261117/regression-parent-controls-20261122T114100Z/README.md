# Narrow parent controls — 20261122T114100Z (2 unchanged methods, no source/test edits)

Root: `notes/rephase-1-prior-artifact-reader-repair-20261117/astra-repair-resolution.md` FULL §5 (dispatch §§57–65). Source e59/pack frozen, no fixes/adapters. No reconstruct Git/status/log/HEAD/readback, no network/install/Production/configHOME/source edits/subagents. No real stage retry/advance.

## Parent copy (NEW independent, FULL d591)

- SRC saved `.rephase-1-editorial-runtime/selection-scaling-real-20261116T021943Z/candidate-work` (HEAD `d591` parent `ae0` tree `ff01`, no alternates, inert origin).
- NEW copy `.rephase-1-editorial-runtime/prior-artifact-reader-parent-controls-20261122T114100Z/work` via `rsync -a --exclude=.git --exclude=__pycache__ --exclude=*.pyc` + `rsync -a .git` (no `-H`, no hardlinks). Inodes differ (src 25041453 vs new 25431168 for stage file), no `objects/info/alternates`, no `commondir`, inert origin `https://invalid.invalid/inert.git` preserved (no set-url/config). No empty/amend/bypass.
- Verified FULL: `git rev-parse HEAD` `3231a0c280287411513bba359f4d3d2b6703d591`, parent `ae0dd1ee5b0e7a85c44bdab0e6cd024bf12f0c56`, tree `ff01b73e6012fd4519fdfb3807186753ff330367` (full, no prefix, no f591 copy). All774 vs frozen `0dc361cb…/187361B`: missing0, mismatch0 (`source774-pre-summary.json` 774/774 OK, `source774-post-summary.json` 774/774 OK). Stage old `ec15f5ba…/49688B`, test files unchanged (`fc11c8a9…`, `6a1c83da…` match old manifest and e59 copy). Modes from manifest, states irrelevant (tests use new independent fixture temp scope, synthetic EVIDENCE_REVIEWED, process-scoped identity, inert origin).

## Methods (EXACT unchanged, no runtime/test patch)

- `tests.test_dm022_normal_writer_late_guard_v2.TestNormalWriterLateGuardV2.test_selection_matrix_late_guard`
- `tests.test_survey_freeze_stage_boundary_v2.FreezeStageBoundaryV2Tests.test_non_publication_checkpoint_typed_record_is_not_silently_skipped`
- Test files unchanged (SHA matches old774 and e59), no assertion weakening. Harness `run_parent_controls.py` NEW via Write only, `PYTHONDONTWRITEBYTECODE=1 GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_CONFIG_NOSYSTEM=1` + `GIT_CONFIG_GLOBAL=/dev/null`. CWD parent work ensures loaded source from parent copy (pins pre/post bind all774).

## Raw (durable, no aggregation)

- `run-argv.json/cwd.txt/env.json/pid.txt/start-utc.txt/start-epoch.txt/end-utc.txt/end-epoch.txt/exit.txt/stdout.txt/stderr.txt/wall.txt/run-summary.json`, `source774-pre.json/post.json` + `*-summary.json` (774 each, OK). PID 1602121, wall6s, `Ran 2 tests in 5.072s`, exit1. Real copy untouched, CURRENT/pack frozen.

## Result vs e59 (same, NOT regression)

- Parent: 0/2 PASS, 2 FAIL exit1.
  - Writer: `AssertionError: Exception not raised` at `test_dm022_normal_writer_late_guard_v2.py:147` → `_run_healthy_and_fault:74` `assertRaisesRegex(DM022_TRANSITION_ACTIVE)`.
  - Freeze: `StageValidationError: Production State invalid before stage validation: legacy checkpoint schema invalid: ... 'artifacts' is a required property` at `validate_stage:865`, mismatch vs expected `"Stage Checkpoint"` at `test_...:300`.
- e59 batch2 (10 tests, 11.856s): same 2 FAIL with identical locations/messages (only worktree path prefix differs: `.../parent-controls-.../work/` vs `.../verification-.../work/`), same exit1. No new error, no timing anomaly indicating regression (parent 2 in 5.072s vs e59 10 in 11.856s; per-method wall consistent, no hang).
- Do NOT rerun e59 2 for counts; comparison uses saved e59 batch2 raw. If parent differed, would return regression with no side fix — not triggered (same).

## Diagnosis (actual source, not guess)

- Writer injection target stale in BOTH parent and e59 (runner identical `b16c4759…/50865B`):
  - Test injects via `LateGuardInjector(guard, "run_selection_architecture_v2_interactive.py", "run", 316, entry 260)` wrapping REAL `low.require_research_operation_ready`, firing only when outer caller is `run:316` / entry `run:260`.
  - Actual callee: `scripts/run_selection_architecture_v2_interactive.py` total892 lines, `def run` at555, sole `_dm022_require_ready` at393 (`low.require...` at102). Lines260/316 are plan-validation/blank, never `run`. Thus `is_target/is_entry` never True, `injected/target_reached/entry_reached` stay False, guard never planted, REAL helper never sees guard, no `DM022_TRANSITION_ACTIVE`. Verified by reading test + `dm022_late_guard_fixture_v2.py` injector + runner grep (single `_dm022_require_ready` call at393). Old `_dm022_require_ready`-once hypothesis consistent, but precise actual is target-line mismatch; `private_check_boundary` not reached because guard absent. True on parent and e59 (runner SHA identical), so pre-existing harness/callee drift, not e59 stage-reader regression (stage change is after, `_prior_artifacts` at880).
- Freeze early strict State check unchanged by one-function repair:
  - `validate_stage:863-865` `agent.validate_agent_state` → `Production State invalid...` before `869 _dm022_require_ready` and `880 _prior_artifacts`. Test copies `publication_preview` to `architecture` provenance, causing `validate_agent_state` legacy-schema `artifacts required` error. Expected `"Stage Checkpoint"` (from `_prior_artifacts`) never reached. Repair touches only `_prior_artifacts` (after early check), so early refusal identical in parent/e59. Actual from reading `survey_stage_validation_v2.py:852-881` + test `make_fixture/build_candidate/approve_and_build_freeze/validate_freeze_stage` path.

## What was / was NOT proven

- Proven scoped: 2 failures unchanged vs parent d591/774, NOT caused by e59 `1e4c…` stage change; same location/message/timing class. Test files unchanged.
- NOT proven: whole-suite PASS (only 2 methods run here; e59 batch2 8/10 PASS remains 8/10, not 10/10). NOT predicate coverage transfer: root/independent must still assess intended `_prior_artifacts` active7/LEGACY coverage from actual focused/public tests (`test_prior_artifact_reader_repair_v2` 8+2 + e59 8 PASS), not from old-suite blanket PASS.
- Preserved harness TypeError retry deviation per ROOT §5 (initial `batch1-harness-selection-error` TypeError + rerun after frozen-verification stop rule is unauthorized local retry, not source defect, not clean first run; plain-function loader calls not counted as unittest methods). No later proof retroactively authorizes retry.

## Limits

- 2-method parent control only, no broad suite, no assertion adaptation, no new dispatch. CURRENT/pack frozen, no real SP/W34 retry. PartialDB26309/bulk31466/TeX unbundled carry. Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN.
