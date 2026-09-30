# R1 e4-lineage assembly — selected fresh verification

Root selection after milestone-1 source/identity review. Candidate **481dec0c0233d7871df79a07a88aa5fe2291daa3**, tree **657032438c6ed8b1c055d5a120b67b4b261a5092**, parent **e4c82692abee6acedbba07815b0d74ccefb80a7e**. New independent fixture `/tmp/jgas-rephase-r1-assembly-20260929T143833Z`; branch `codex/rephase-1-r1-assembly`. Seven reviewed files are unchanged from b74db67; no new code feature is selected.

## Scope and exact selected methods

General runs the following four methods, using `/tmp/jgas-rephase-application-venv/bin/python3.12`, from the assembly checkout with a clean Git-root-override environment:

```text
python3.12 -m unittest -v
  tests.test_survey_weekly_mechanical_refresh_v2.WeeklyMechanicalRefreshV2Tests.test_first_and_repeat_success
  tests.test_survey_weekly_mechanical_refresh_v2.WeeklyMechanicalRefreshV2Tests.test_metadata_revalidation_effective_rows_then_refresh
  tests.test_survey_weekly_mechanical_refresh_v2.WeeklyMechanicalRefreshV2Tests.test_active_predecessor_not_noop_and_artifact_only_noop
  tests.test_survey_weekly_mechanical_refresh_v2.WeeklyMechanicalRefreshV2Tests.test_pre_install_control_change_unsupported
```

Use one actual argv list (the multiline display is not a shell script). The Worker's initial proposed examples omitted the TestCase class; those were unexecuted proposals, corrected here before running. The tests exercise assembled source in fresh synthetic Git fixtures; **their fixture histories are not the e4 lineage**. Exact output/authority remains synthetic, not historical-edition revalidation or real publication.

## Actual assembled-database diagnostic

In a fresh process importing the exact assembly source, perform a read-only diagnostic against the **actual assembly repository**:

1. Confirm exact HEAD/tree/parent, clean tracked bytes/index and source module path/hash.
2. Build current closure from current files; `_verify_head_bytes(repo, actual_HEAD, current_closure)` must pass, with actual e4 parent/ancestry recorded.
3. Obtain the historical eight-file closure at exact e4 from available local committed blobs (not current hashes relabelled as historical); `verify_closure_at_commit` must verify those historical bytes.
4. Calling ordinary current-tool replay verification with that e4 generating basis must reject specifically because the implementation/control bytes changed. Keep actual exception type/message, with success sentinel outside the exception handler. Missing-object/setup failure is not the intended rejection.
5. Preserve no-write before/after evidence for tracked source, current index/refs/HEAD and repository edition authority paths; no State/Gate/receipt or historical data mutation in the assembly checkout. Python cache activity must be prevented or separately reported, never silently cleaned.

No lazy-fetch/network/hydration, alternate Git database or fabricated success stubs. If required local closure blobs are unavailable, stop with exact object/path evidence; do not call that successful stale-tool rejection. Do not commit diagnostic artifacts into the assembly candidate.

## Evidence and role constraints

Use new absent run/output paths; refuse overwrite of every log, exit and report. Record command/cwd/Python/dependencies, exact commit/tree/parent, seven source hashes, raw stdout/stderr, numeric outcomes/counts/skips, and any setup failure separately. Preserve the assembly candidate fixed throughout. No complete 97-method rerun for decoration; the old b74 matrix stays its original scope. Normal candidate assembly commit used no bypass flags; that does not independently prove that particular hooks existed or ran.

Copy any necessary comparison/verification scripts out of temporary-only locations into the new evidence packet and retain their observed outputs; they are historical evidence, not automatic rerun instructions. No raw output reconstruction from a summary. Immutable source tree comparison establishes unchanged **references** for inaccessible promisor data, not validation of missing blob content or complete fixed-baseline application.

Root reviews fresh outcomes and a separate reviewer checks the fixed assembly/evidence. Human requested interruption at useful Commit Points; stop this unit after verification/review and updated handoff, before the next implementation unit. Ordinary reconstruct Commit/Push remains Human-owned.
