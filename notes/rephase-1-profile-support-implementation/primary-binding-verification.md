# Primary binding verification — contract §6.4 multi-source/multi-DID ambiguous primary subject

2026-10-31. Final source quiescent/packaged; NO shipping source/tests or old packet edits in this unit. One exact contract oracle disposition before closeout. This is within the chosen oracle (§6.4 behavioral witness), not extra feature/cadence/unit. Final packaging: no code changes.

Authority: contract `outputs/rephase-1-profile-support-contract-decision.md` §6.4 (`multi-source and multi-DID with ambiguous primary subject rejected rather than coerced`); independent final `independent-final-implementation-review.md:29,100` (`not separately re-demonstrated`, DROP-unknown/mismatch as multi-source boundary); root disposition in task (DROP-unknown/mismatch does NOT establish subject ambiguity; don't silently waive).

## 1. What existing tests cover (precise file lines + test names, no rerun)

- `tests/test_run_evidence_v2_interactive.py:163-170`
  `InteractiveEvidenceProfileContractTests.test_multiple_task_bound_sources_require_explicit_bindings`
  (already in final affected 26): multi-source (2 authorities `src-1` + `supplement-src-…` for single DID `D-1`) with missing `source_bindings` → `ValueError "source_bindings is required"`; with explicit `["supplement-src-…"]` → passes. Proves multi-source explicit binding (no coercion to default `src-1`). Single DID, unambiguous primary (`entity-1`). Covers source ambiguity, NOT multi-DID, NOT primary-subject ambiguity.
- `tests/test_survey_evidence_v2.py:500-525`
  `SurveyEvidenceV2Tests.test_issue_191_comparator_owned_metric_cannot_bind_primary_subject`
  (already in same 26): single task/card (single DID, single source `source-1`), metric with `subject_id=target` + `subject_role=COMPARATOR` → `any("COMPARATOR cannot bind artifact.primary_subject_id")`; fixed to `subject_id=comparator` → `== []`. Proves subject ROLE (comparator vs primary), NOT multi-source/multi-DID, NOT ambiguous primary (clearly wrong role, not conflicting primaries).
- `tests/test_profile_support_upstream_repair_v2.py:test_03` (`DM016CanonicalTenTests.test_03_all_ten_through_actual_task_card_acceptance_zero_errors`):
  10 genuine single-source single-DID tasks, each `errors == []` for expected class + mismatch refuses `source_class does not match task-bound authority`. Unambiguous primary (`target`). No multi-source/multi-DID/ambiguous primary.
- `tests/test_profile_support_upstream_repair_v2.py:test_23/test_24` (`DerivedOperationTests`):
  multi-DID roots R-1/R-2 + multi-DID effective C-1/C-2, shared OID, same sourceidentity/Rawunion, no entities (Discovery obligations, not Evidence cards). No primary subjects, no source ambiguity (same locator/class). Covers multi-DID for obligations, NOT primary subjects.

Verdict: existing raw/bodies do NOT establish multi-source AND multi-DID with ambiguous PRIMARY_SUBJECT refusal. DROP-unknown (unknown `source_type` incl prospective DROP) + mismatch (`source_class does not match`) are source-classification boundaries, not subject-ambiguity proof. No silent waiver — narrow regression below was required.

## 2. ONE narrow evidence-only regression (outside shipping tree, final proof immutable)

Harness: `/tmp/opencode/primary-binding-20261031T233000Z/harness.py` (ignored runtime, NOT shipping source/tests, NOT proof-copy, NOT old packet). Imports ACTUAL final proof modules (immutable, no edits):
`PROOF=/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/profile-support-packaging-20261031T202327Z/proof-copy/candidate-partial-b40de60`
`from scripts import survey_evidence_v2 as evidence` (proof `survey_evidence_v2.py` 130152B `36b7b5832845ea8a984c69a3097f9846976805c556679ed980b0148fdf454736`; proof-copy excl .git 770 files before/after unchanged).

- No mocks/success forcers (`mock` not imported, no `patch`, no forced return). No false `many different primaryIDs` passing another error (2 entities only; control vs negative differ by one `subject_id`; sources correct in both so failure is precisely subject, not source/basis).
- No SOURCE aliases/class default: expected classes via real `evidence._source_class("paper")=="PRIMARY_PAPER"`, `evidence._source_class("SECONDARY_REFERENCE")=="SECONDARY"` (asserted, not hardcoded alias).
- Actual task/card schema/`primary_subject_id`/claim subject binding roles; source ambiguity (which source?) vs entity subject (which entity is primary?) distinguished by keeping sources correct in both cases.
- Genuine valid control first + ambiguous negative, precise full-validator errors, no coercion.
- New meaningful independent fixture source commit: NOT needed (evidence-only, in-memory dicts, no supplement → `repo_root=None` allowed, no repo I/O, no Git, no network). Disclosed, not skipped to hide. Temporary evidence critical bytes: none (no temp files). No candidate commit/Git readback.

Strict oracles:
- Control `test_control_multi_source_multi_did_unambiguous_primary_passes`: multi-source (paper PRIMARY_PAPER `…/primary` + SECONDARY_REFERENCE SECONDARY `…/secondary`) + multi-DID (`["D-1","D-2"]`), 2 entities (target primary + other), artifact `primary_subject_id="target"`, claim `subject_id="target"`/`subject_role="PRIMARY_SUBJECT"`/`source_ids=["source-1","source-2"]` (both correct classes) → `validate_evidence_card(...) == []`.
- Negative `test_negative_multi_source_multi_did_ambiguous_primary_refused_no_coercion`: same task/package/sources (correct, so source ambiguity resolved), same entities/artifact primary (`target`), but claim `subject_id="other"`/`subject_role="PRIMARY_SUBJECT"` (conflicting primary: artifact says target, claim says other) → `== ["claims claim-1 PRIMARY_SUBJECT must bind artifact.primary_subject_id"]` (single precise error, no other errors, no pass-coercion to target).

Test IDs for final-evidence owner:
`harness.PrimaryBindingTests.test_control_multi_source_multi_did_unambiguous_primary_passes`,
`harness.PrimaryBindingTests.test_negative_multi_source_multi_did_ambiguous_primary_refused_no_coercion`;
harness path `/tmp/opencode/primary-binding-20261031T233000Z/harness.py` (ignored runtime, outside shipping tree; freeze after this run — no further edits).

## 3. Direct full raw (execution needed, no hand summary, no 28 re-run)

- Command: `bash -c 'echo RUN_PID:$$; echo CMD: env PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -m unittest harness -v 2>&1; exec env PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -m unittest harness -v 2>&1'; echo "EXIT:$?"`
  Workdir `/tmp/opencode/primary-binding-20261031T233000Z`. Env `PYTHONDONTWRITEBYTECODE=1`, `/usr/bin/python3` 3.14.4, no installs/network. PID 2640012. EXIT 0.
- BEFORE/AFTER proof-copy excl .git: 770 / 770 unchanged; `survey_evidence_v2.py` 130152 `36b7b583…` unchanged (imports only, no writes, no pyc).
- STDOUT/STDERR (exact tool-output archival, combined `2>&1`, per-test verbose):
```
RUN_PID:2640012
CMD: env PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -m unittest harness -v
test_control_multi_source_multi_did_unambiguous_primary_passes (harness.PrimaryBindingTests.test_control_multi_source_multi_did_unambiguous_primary_passes) ... ok
test_negative_multi_source_multi_did_ambiguous_primary_refused_no_coercion (harness.PrimaryBindingTests.test_negative_multi_source_multi_did_ambiguous_primary_refused_no_coercion) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
EXIT:0
```
  Saved verbatim (no hand-summarized “raw”) to
  `notes/rephase-1-profile-support-implementation/primary-binding-verification-20261031T233000Z/logs/harness-233000Z-{stdout-stderr,command,env,pid,exit,pins-before,pins-after}.txt`
  (7 exclusive files). If no actual streams existed I would disclose; here they do — no manufacture, no 173500Z summary reconstruction. `tests/test_profile_support_upstream_repair_v2` 28-test suite NOT re-run here (per instruction; frozen at 115763B `926e2e0a…` with DERIVED 2/2 raw already archived in `.../175500Z/logs/`).

## 4. Precise completion vs limitation (no broader claim — FIRST harness scope, preserved as history; see §5 for root qualification)

Completion CLAIMED in §§2-3 for the first harness (multi-source + multi-DID single-task with ambiguous primary) is WITHDRAWN as valid-accepted-task/full-combined-operation proof (see §5). Preserved below as history; do NOT rely on §§2-4 alone for §6.4 closeout.

Original §§2-4 claim (history): multi-source (2 source_records, distinct locators/classes via real `_source_class`) + multi-DID (2 discovery_ids) with ambiguous PRIMARY_SUBJECT (artifact primary `target` vs claim PRIMARY_SUBJECT `other`, sources correct) is refused with the precise single error above, not coerced; unambiguous control with same multi-source/multi-DID passes `== []`. Source vs entity distinguished (sources correct in both; only subject differs). No new contract/capability gap found; no runtime change made to make the test pass (validator already refused; harness only demonstrates it).

Limitation (original): evidence-only (`validate_evidence_card` full validator, no Screening/Discovery/State/Git/build). Does NOT prove Screening prepackage admission, U/loss, agent parity, Selection/Architecture consumption, DM022, or all-Profile quality — those remain under their own oracles/final review. No all-format demand, no generic reader, no cadence/unit expansion. Independent final `not separately re-demonstrated` is now superseded for this oracle by the above genuine negative; DROP-unknown/mismatch remain source-classification boundaries (not claimed as subject proof). Preserve root/independent errors as history. Running children: none. No whole PASS.

## 5. Root qualification + corrected valid-task harness (2026-10-31, frozen, no shipping edits)

Root checks (evidence:744/746 → `survey_evidence_v2.py:749-751`):
`_validate_task` requires `len(task["discovery_ids"]) == 1` (`"WU-007 Evidence Task must bind exactly its declared Discovery ID"`) and `len(task["source_records"]) == len(task["discovery_ids"])` (`"Evidence Task source_records must match Discovery cardinality"`). First-harness task (`discovery_ids ["D-1","D-2"]`, 2 source_records) therefore FAILS task schema/basis (`len==2 != 1`) even though `validate_evidence_card` passed (card validator does NOT check DID count). Do NOT call the first harness a valid accepted task or full combined-operation proof.

- First harness/raw preserved as LEAF PROBE (card-gate only, not task/basis proof) with explicit limitation (this section). Archived exact harness bytes durably in packet (not just /tmp):
  `notes/rephase-1-profile-support-implementation/primary-binding-verification-20261031T233000Z/harness-233000Z.py` 7327B `ecd40183b2e286b4f8c31c0df8205d2506840cb543f80c7bade918cb8d90cddd`
  (same bytes as `/tmp/.../harness.py` at PID 2640012 run; original raw in `.../233000Z/logs/harness-233000Z-stdout-stderr.txt` preserved, NOT recreated). Do NOT rerun first harness to re-prove; its 2/2 card-gate raw (control `== []`, negative single precise subject error, no coercion) stands as card-gate probe only.
- If the first-harness control task were actually valid, `_validate_task(task, meta, acceptance_sha)` would return `[]`; in fact with 2 DIDs it returns `["WU-007 Evidence Task must bind exactly its declared Discovery ID"]` per source lines above (explained by exact `validate_task` call shape/result, no new execution, no widened semantics).

Corrected narrow harness (SECOND, valid-task subject negative, no combined-invalid claim):
Harness `/tmp/opencode/primary-binding-20261031T233100Z/harness2.py` (ignored runtime, outside shipping tree), archived durably as
`notes/rephase-1-profile-support-implementation/primary-binding-verification-20261031T233000Z/harness2-233100Z.py` 6542B `51c771e86c70ea935db8a00bd986c342737c2a8636ed3e13c35490b371c71f79`
(no shipping source/tests or old packet edits to create it; packet archival is new evidence, not old-packet mutation).
Imports ACTUAL final proof modules + actual existing fixture APIs (`test_survey_evidence_v2.SurveyEvidenceV2Tests.sandbox/init_profile/make_screening/make_evidence/card_for_task` on `candidate-partial-b40de60`, per-fixture real Git HEAD before authority, process identity, inert origin, never `--allow-empty`, no `git config`, no mocks/state-basis stub/fake class default).
Multi-DID = >=2 separately valid single-DID tasks in one package (2 KEEP discoveries → 2 tasks, each `len(discovery_ids)==1`, each `len(source_records)==len(discovery_ids)==1`); multiple sources per task follow existing authoritative supplement/explicit-allowed contract — NOT re-proved here (existing `runner.test_multiple...` + supplement `test_evidence_authority_supplement_binds_exact_raw_source_and_card` + DERIVED multi-DID operation already cover those boundaries; root composes valid boundaries explicitly, not phantom one combined end-to-end).
Then primary mismatch negative changes ONLY `claims[0].subject_id` (`target`→`comparator`, both registered so not `not a registered entity`) with `subject_role` still `PRIMARY_SUBJECT` against artifact primary `target`; asserts exact one error `["claims claim-1 PRIMARY_SUBJECT must bind artifact.primary_subject_id"]` and no coercion.
Valid control passes task/package checks AND card validator (not only card partial gate): for each of the 2 tasks, `evidence._validate_task(task, meta, package["basis"]["screening_acceptance_sha256"]) == []` (real task shape, real SHAs from builders, no dummy basis) + `evidence.validate_evidence_card(card, task, meta["sha256"], package, repo_root=root) == []` (genuine valid cards).

Direct full raw (SECOND harness, execution needed, no hand summary, no 28 re-run):
Command `bash -c 'echo RUN_PID:$$; echo CMD: env PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -m unittest harness2 -v 2>&1; exec env PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -m unittest harness2 -v 2>&1'; echo "EXIT:$?"`, workdir `/tmp/opencode/primary-binding-20261031T233100Z`, env `PYTHONDONTWRITEBYTECODE=1`, `/usr/bin/python3` 3.14.4, no installs/network. PID 2648207. EXIT 0.
BEFORE/AFTER proof-copy excl .git 770/770 unchanged; `survey_evidence_v2.py` 130152 `36b7b5832845ea8a984c69a3097f9846976805c556679ed980b0148fdf454736` unchanged (imports only, no writes, no pyc; fixtures isolated temp dirs).
STDOUT/STDERR verbatim:
```
RUN_PID:2648207
CMD: env PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -m unittest harness2 -v
test_control_two_valid_single_did_tasks_pass_task_package_and_card (harness2.ValidTaskSubjectTests.test_control_two_valid_single_did_tasks_pass_task_package_and_card) ... ok
test_negative_valid_task_primary_mismatch_refused_no_coercion (harness2.ValidTaskSubjectTests.test_negative_valid_task_primary_mismatch_refused_no_coercion) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.253s

OK
EXIT:0
```
Saved verbatim to `.../primary-binding-verification-20261031T233000Z/logs/harness2-233100Z-{stdout-stderr,command,env,pid,exit,pins-before,pins-after}.txt` (7 exclusive files). Test IDs for final-evidence owner: `harness2.ValidTaskSubjectTests.test_control_...`, `...test_negative_...`; harness archived path/hash above; raw captures above; what cannot be claimed below.

What cannot be claimed (honest scope, no widening): SECOND harness proves ambiguity refusal on VALID single-DID single-source tasks (subject binding), with package-level multi-DID (>=2 tasks) for DID coverage; it does NOT prove a single task with 2 DIDs + 2 sources is valid (that shape is INVALID per `_validate_task` — first harness preserved as leaf probe only). Multi-source explicit binding remains covered by `runner.test_multiple...` + supplement authority test; real multi-DID operation by DERIVED test_23/24. Root composes these valid boundaries; no phantom combined 2DID-task end-to-end is claimed. No new capability gap; no runtime change to make tests pass. All before/after 770 unchanged. Running children: none. No whole PASS.
