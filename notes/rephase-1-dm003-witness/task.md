# DM-003 witness and disposition — Astra bounded task

Issued 2026-10-04 after Human Push/continuation at reconstruct **1bb42dd** (clean/local tracking observation, no fetch). This unit is **source analysis + isolated witness + disposition**, not a generic provenance repair. Shipping candidate remains **222a37e9ee2aa96724a491f2c04c2583a86b9650**, tree **dbabeed5e70d79b51abb09b64666ca9e1d0fd5dd**. Baseline fixed774dd39a; latest Summary capture reused, no network intake.

## Question

The saved Summary DM-003 says a valid `VALIDATED_DRAFT→RELEASE_CANDIDATE` checkpoint exists with `checkpoints: []` and Candidate artifact but has no named `checkpoint_provenance` pointer. Existing f1/B stage logic instead obtains the Candidate through typed Preview approval. At fixed222, establish whether this supports the selected Freeze path without ad-hoc sibling discovery, and whether conflicting/stale **recognized** authority is rejected. Distinguish an unreferenced file's contents from an active authority claim; do not assume every filesystem sibling must become authoritative or rejected.

## Roles and scope

- General: inspect exact current route/config/callers, propose minimal cases, implement/run a **new external witness harness** in an independent byte-copy DB, preserve raw evidence/artifact snapshots and report actual results/limits.
- Astra: choose exact oracles, review source/fixture/results and decide whether any runtime change is justified. Fresh author-independent reviewer checks that disposition/evidence. Root does not run witnesses or author implementation.
- No shipping code/schema/config changes, new candidate commits, old-suite reruns, production/main/Summary/Issue reads/writes or generic checkpoint scanning. If a current defect is demonstrated, return it before any repair selection. No automatic `CORE_FIXED` or whole-provenance completeness claim.

## Internal milestone 1 — concise source/case proposal

Read current handoff and DM001/019 assessment §6, saved Summary lines126–149, then current `survey_stage_validation_v2` prior-artifact/approval extraction and current `survey_agent_control_v2` checkpoint/State/Preview admission paths with the actual config. Verify live222/tree/parent/tracked cleanliness read-only; preserve source/restored DBs.

Return a short source-grounded table: how the Candidate checkpoint is produced; why/where named map omits it; which pointer/typed approval is actually authoritative at each relevant phase; which checks bind Candidate path/hash; treatment of two conflicting **mapped/typed** authorities versus an unreferenced sibling. Propose real-case construction and expected error/no-write oracles before execution. Do not repeat whole inventory or assume the Summary's proposed remedy is the architecture.

## Internal milestone 2 — execution after Astra oracle selection

Use NEW absent `/tmp/opencode/` independent byte-copy of available222 DB, own gitdir/object files, inert origin, no alternates/hardlinks/inherited Git-root overrides. Existing pinned3.12.14 venv; no recovery/provisioning/network needed. Witness script lives in this packet/outside candidate control roots. Preserve candidate source/ref/HEAD; no new shipping commit or artificial parentage. Use actual State/checkpoint/Preview/stage validators/builders; synthetic research/reviews/PDF/Human records labelled, no authority/Git-success mocks.

Minimum conceptual matrix (refine with actual source):

1. Intact real-validator control with checkpoint created by canonical producer, approved exact Candidate and Freeze-stage admission.
2. Valid Candidate checkpoint on disk with actual `checkpoints: []` and absent named pointer, typed approval intact: show exact resolution/source and stage behavior. If this is the canonical control itself, say so and add a meaningful independent control rather than double-counting identical fixtures.
3. Missing/unreferenced sibling control, only if useful to prove discovery dependency; do not delete preserved source or old evidence. Any ignored sibling behavior must be reported as non-authority, not generic validation of its contents.
4. Stale typed approval/Candidate bytes/hash or mismatching recognized pointers: expected precise rejection, no outputs/State mutation beyond declared diagnostic output.
5. Individually valid conflicting Candidate authority (same issue/Profile/PDF if feasible), not merely schema-invalid junk; distinguish ignored orphan content from conflicting admitted input. Show current-artifact merge or named/typed conflict separately if different invariants are involved.

Do not enforce an invented new canonical-map entry simply to manufacture a control. Preserve any legitimate alias/multiple-pointer behavior in current config. If a desired mutation is structurally impossible at this lifecycle, document the actual invariant and select a case that reaches the intended boundary rather than stubbing it.

## Evidence and stop

Per case, capture fresh **asserted** HEAD/tree/tracked-clean source/hash observation before and after execution (do not print a shared observation as fresh guards), literal command/cwd/allow-listed environment, runtime, exit and raw actual exception/outcome. `GIT_NO_LAZY_FETCH=1`, `GIT_ALLOW_PROTOCOL=file`, `GIT_OPTIONAL_LOCKS=0`, `PYTHONDONTWRITEBYTECODE=1`. Snapshot relevant State/pointers/checkpoint/approval/Candidate/source/PDF and outputs before/after each operation, preserving case-specific bytes in unique no-overwrite evidence paths. Record any allowed stage report write separately from authority writes; success may produce synthetic reports/checkpoints in its own fixture. Never broad-catch exceptions as PASS; assert precise type/message and actual selected path/hash. Preserve initial failures and harness versions, no overwrite.

No production edition artifacts or live Human approvals are reconstructed. Parent and final source identity stable; all proof binds to222 and synthetic fixture scope. Return a compact report + machine-generated evidence manifest with case counts (not inflated subtests/methods), source pins, raw outcomes, setup failures, limitations, actual writes and recommendation (`no selected-path blocker`, `narrow defect`, or `unresolved`). Review and Astra disposition end at a Human Commit Point; do not automatically start DM-004 or a provenance implementation.
