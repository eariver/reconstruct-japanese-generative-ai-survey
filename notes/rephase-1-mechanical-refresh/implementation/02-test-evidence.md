# R1 implementation evidence — test record, failures, limits

Runtime: `/tmp/jgas-rephase-application-venv/bin/python3.12` = CPython **3.12.14**, **pypdf 6.16.2**, **jsonschema 4.23.0** (`logs/r1-deps.py`; versions via `importlib.metadata`, no `pip`/network). CWD for test runs: the fixture root. Skips: **0** in every run. Stale-import discipline: baseline built in-process at installed R1 source; every post-helper-commit refresh driven through a fresh `sys.executable` CLI subprocess with `PYTHONPATH=<subfixture>`, `PYTHONDONTWRITEBYTECODE=1`, `GIT_*` overrides stripped.

## New dedicated suite (`tests/test_survey_weekly_mechanical_refresh_v2.py`, 14 methods)

| # | Method (§7 item) | Result (final head) |
|---|---|---|
| 1 | `test_first_and_repeat_success` (§7.1: r1 null→record, r2 supersedes r1, retention exact, immutability, old receipt rejected) | PASS |
| 2 | `test_active_predecessor_not_noop_and_artifact_only_noop` (§7.2) | PASS |
| 3 | `test_pre_install_control_change_unsupported` (§7.2) | PASS |
| 4 | `test_changed_renderer_output_refused` (§7.3) | PASS |
| 5 | `test_accepted_and_authored_mutation_refused` (§7.3, 2 subTests) | PASS |
| 6 | `test_review_contract_change_refused` (§7.3) | PASS |
| 7 | `test_malformed_old_authority_refused` (§7.3, 2 subTests) | PASS |
| 8 | `test_dirty_and_untracked_control_refused` (§7.3, 2 subTests) | PASS |
| 9 | `test_occupied_guard_refuses_without_clobber` (§7.4) | PASS |
| 10 | `test_retention_collision_refuses_without_live_write` (§7.4) | PASS |
| 11 | `test_gate_failure_restores_owned_receipt` (§7.5, injected) | PASS |
| 12 | `test_revalidation_failure_restores_owned_files` (§7.5, injected) | PASS |
| 13 | `test_record_collision_preserves_foreign_record` (§7.5, mocked allocator) | PASS |
| 14 | `test_public_validators_still_reject_without_bypass` (§7.6, 3 subTests) | PASS |

- Final exact-head run: `logs/r1-final-refresh.log` — **14 tests, 742.117 s, OK, exit 0**. (An earlier full run `logs/r1-full-refresh.log` collected 22 = 8 archived increment-b + 14 new because the `Base` alias was module-visible; the alias was refactored behind `_base_suite()` and collection re-verified at exactly 14.)
- Negative oracles use specific exception/message matches outside any success sentinel (e.g. `MECHANICAL_REFRESH_NO_OP`, `unsupported control/criteria`, `Stage Checkpoint artifact drift`, `check family differs` family, `sequence collision`, `refused changed record bytes`), plus State-sha/record-listing/live-sha invariance per window.

## Revalidation rollback additions (`tests/test_survey_publication_revalidation_v2.py`, +2)

- `test_r1_record_collision_no_clobber`, `test_r1_record_tamper_rollback_refuses_removal`: PASS (`logs/r1-reval-rollback.log`, 2 tests, 2.810 s, OK).
- Full file at final head: `logs/r1-affected2.log` — **25 tests, 47.570 s, OK** (23 existing + 2 new).

## Affected existing suites (final code, no reruns for decoration)

| Suite | Result |
|---|---|
| `test_survey_reader_surface_gate_v2` + `test_survey_agent_control_v2` + `test_survey_stage_validation_v2` | 35 tests, 3.945 s, OK (`logs/r1-affected1.log`) |
| `test_survey_gate_cli_persisted_review_v2` | 5 tests, 40.900 s, OK (`logs/r1-affected3.log`) |
| `test_survey_increment_b_weekly_derivation_v2` | 8 tests, 265.852 s, OK (`logs/r1-affected4.log`) |
| `test_survey_semantic_publication_v2` + `test_survey_weekly_evidence_authority_v2` + `test_survey_agent_tool_v2` | 12 tests, 52.044 s, OK (`logs/r1-affected5.log`) |

## Preserved failures and corrections (not hidden)

1. `git archive` infeasible (promisor-missing objects) → worktree `tar` copy; worktree `diff -r` exit 0.
2. Baseline quality bundle required `IDENTIFIER_PRESERVATION` + `PDF_PREFLIGHT` checks beyond the subject check (increment-b pattern); corrected in the test fixture builder.
3. Three implementation bugs found by the new tests and fixed (all preserved in batch logs): dict-comprehension NameError (`r1-batch6` predecessor `r1-t1-first` shows the `ms_rows` NameError), directory-pathspec swallowing the single-file allowlist (rewrote as `--name-status` classification), untracked-control misread as NO_OP (clean check moved before NO_OP), absolute-vs-relative review path at Gate evaluation, non-ValueError escaping the CLI exit-2 contract (wrapped with chain).
4. Two oracle mismatches corrected without touching guards: accepted-drift refuses at strict State (`Stage Checkpoint artifact drift: candidate-matrix`) — oracle widened to that intended earlier boundary; record-collision via pre-created r1 cannot collide because the allocator picks max+1 — rewritten deterministically with a mocked empty listing so the exclusive-create guard fires.
5. Unresolved-finding variant needed schema-required `artifact` + `proposed_normalization` fields; corrected.
6. Full-run collection picked up 8 archived tests via the module-visible `Base` alias; refactored and re-verified at 14.

## Limits (not claimed)

Same-byte Weekly route only; bootstrap requires R1-installed baseline receipts (pre-install/e4-era receipts unsupported, no self-exemption); no atomic multi-file promise beyond single-file atomic replace + guarded restore; cooperating-guard only (noncooperating writers externally serialized); no crash/power-loss automation; no Candidate-stage/TeX/real-review/PDF-preflight/all-profile/lifecycle-savings evidence; whole candidate NOT_READY; seven-point audit separate. `test_no_edition_conditionals_in_new_paths` passes on the edited controller block.
