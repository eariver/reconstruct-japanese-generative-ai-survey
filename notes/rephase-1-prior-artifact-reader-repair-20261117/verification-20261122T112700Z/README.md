# Affected regression verification — 20261122T112700Z (bounded, no source edits, STOP on 2 failures)

Root: `notes/rephase-1-prior-artifact-reader-repair-20261117/astra-repair-resolution.md` FULL §4 (dispatch §§48–55). Source frozen `e59fa9bc5f323a640fd922412de7757e60eb5944` parent full `d591` tree `e5e8...`; stage `1e4c818b.../51927B` + test `1fb83167.../30019B`; old774 `0dc3...` other773 unchanged =>775. No reconstruct Git/status/log/HEAD/readback, no network/install/Production/configHOME/source edits/subagents. SOURCE FROZEN.

## Workspaces (NEW independent, ignored runtime)

- VERIF copy `.rephase-1-editorial-runtime/prior-artifact-reader-verification-20261122T112700Z/work` via `rsync -a --exclude=.git --exclude=__pycache__ --exclude=*.pyc` worktree + `rsync -a` `.git` (no `-H`, no hardlinks). Inodes differ (author 25199359 vs verif 25315966 for stage file), no `objects/info/alternates`, no `commondir`, inert origin `https://invalid.invalid/inert.git` preserved (no set-url/config). Harness `run_affected_regressions.py` NEW via Write only (no shell text editing), executed with `PYTHONDONTWRITEBYTECODE=1 GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_CONFIG_NOSYSTEM=1` + `GIT_CONFIG_GLOBAL=/dev/null`.
- Fixture helpers inspected before use: `tests/test_versioned_renewal_source_phase_s.py:Scratch` (process-scoped identity, inert origin, no config writes, never `--allow-empty`, checks `GIT_DIR` overrides) reused only for CURRENT, not here; here direct `unittest` with cwd VERIF_WORK ensures actual loaded modules from e59 copy. Historical runners not executed.
- Real copy `.rephase-1-editorial-runtime/prior-artifact-reader-real-20261122T065145Z/candidate-work` untouched (HEAD `e59...` read-only `rev-parse` only, no writes, 45 inherited porcelain lines preserved).

## Source binding (775 pre/post, author check)

- `source775-pre.json` / `source775-post.json` / `author775-check.json` each 7 pins OK: attention `10126da7...`, base `b3cd4a95...`, LOW `fd788b74...`, runner `b16c4759...`, scaling test `a21f5949...`, stage `1e4c818b.../51927`, prior-reader test `1fb83167.../30019`. Pre/post/author all `ok true`, physical `0o664`, no drift. Committed blobs match worktree (`git show HEAD:<path>` SHA matches worktree), modes `100644`.
- Full HEAD `e59...`, parent `d591`, tree `e5e8...` verified via `git rev-parse` (no prefix), `f591` missing (`cat-file -e` exit1), `d591` exists (exit0), 390B commit body SHA1 recompute matches HEAD. 773 unchanged vs old774 manifest (0 mismatch except expected stage update), new test present. Other `M/?? sources/*` are inherited worktree-vs-HEAD real-material deltas, not this unit.

## Batches (durable unique raw, no aggregation)

- **batch1-harness-selection-error** (`raw/batch1-harness-selection-error/`): 10 selected included 2 `test_group_c_editorial_consumers_v2` plain functions (not `unittest.TestCase`), loader `TypeError: calling ... returned None, not a test`, exit1, wall1s, pre/post/author OK. Preserved as operator harness-selection error, not source defect. No overwrite.
- **batch2-corrected-10pass** (`raw/batch2-corrected-10pass/`): corrected SELECTED 10 (exact 3 `survey_stage_validation_v2` + 2 `publication_set` seal/revalidation + 1 writer `selection_matrix_late_guard` + 2 `freeze_stage_boundary` non-publication/active-revalidation + 2 `dm022_c_direct` weekly/derived). Result **8/10 PASS, 2 FAIL, exit1, wall13s, PID 1575591** (`run-summary.json` pre_ok/post_ok/author_ok true). Raw `run-argv/cwd/env/pid/start-utc/start-epoch/end-utc/end-epoch/exit/stdout/stderr/wall`, `source775-pre/post.json`, `author775-check.json` durable unique.
  - PASS 8: 3 stage_validation (`same_named_but_invalid...`, `current_tool_basis...`, `draft_stage...`), 2 publication_set (`seal_requires_exact_15`, `revalidation_has_two...`), 1 freeze active (`active_publication_revalidation_survives...`), 2 direct (`c_direct_weekly...`, `c_derived_weekly...`).
  - FAIL 2 preserved, no fix/retry/adapt:
    - `TestNormalWriterLateGuardV2.test_selection_matrix_late_guard`: `AssertionError: Exception not raised` at `_run_healthy_and_fault` (healthy wrote, fault guard did not refuse `DM022_TRANSITION_ACTIVE`). Target `run_selection_architecture_v2_interactive.py:run:316` entry `260`, guard `sources/2026-W33/.../acceptance-revision.guard.json`.
    - `FreezeStageBoundaryV2Tests.test_non_publication_checkpoint_typed_record_is_not_silently_skipped`: expected `Stage Checkpoint` but got `Production State invalid before stage validation: legacy checkpoint schema invalid: ... 'artifacts' is a required property` (`StageValidationError` fail-closed but different predicate).
  - Existing tests used as-is, no adaptation pending root permission; errors reported not waived. No full R3 PDF build. Loaded modules actual via cwd VERIF_WORK (no old copies).

## STOP (source unchanged, no fix)

Per dispatch §55 / operator FROZEN rule, unexpected verification failures STOP this workstream before fix/additional tests/source changes. Source pins pre/post/author OK, so other independent streams (CURRENT, packaging) may proceed. No parent-control additional runs, no source/test edits, no retries. Real validation retry/advance/current output writer not attempted. Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN.

## Limits

- 8/10 PASS provides bounded `_prior_artifacts` active7 LEGACY unaffected evidence (stage 3 + publication 2 + freeze active 1 + direct 2), but full 10 NOT met. 2 failures require root triage (stale line/error-message vs regression). PartialDB missing26309/bulk31466/runtimeTeX nonbundled carry. No suite-count decoration.

## Qualification per ROOT §5 (docs-only append, raw preserved, no source change)

- Initial `batch1-harness-selection-error` TypeError + rerun as `batch2-corrected-10pass` after frozen-verification stop rule is preserved as unauthorized local retry in this workstream per ROOT §5, not a source defect or clean first run. Plain-function loader calls are not counted as successful unittest methods. No later proof retroactively authorizes the retry. Raw both batches untouched.
- Narrow parent controls `../regression-parent-controls-20261122T114100Z/` ran EXACT same 2 FAIL methods on NEW independent parent d591/774 copy (FULL `d591`, 774/774 OK, test files unchanged): 0/2 PASS, same locations/messages as e59 (writer `Exception not raised` :147→:74; freeze early `Production State invalid...artifacts required` vs expected `Stage Checkpoint` :300), wall6s/5.072s vs e59 10 in 11.856s. Same state, NOT regression, NOT whole-suite PASS. Root/independent must still assess intended predicate coverage from focused/public tests, not blanket old-suite PASS. CURRENT/pack frozen, no real retry/advance.
