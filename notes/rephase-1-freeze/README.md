# B1/B2 Freeze boundary evidence

2026-09-21 JST. This is bounded maintenance within the authorized r2 application review. Production and its fixed baseline are untouched. Prior a1 NOT_READY evidence is retained in `../rephase-1-application/`.

## Candidate

- Frozen local candidate **f1**: `bf32edf98ba8f605169d7188bbc764de74ee4f6e`; tree `ebd351479ec222a08b8ea67ae4aae64ad0eb927e`.
- Parent a1: `d38f023ce200619f7f49ce17a348755f05e0e021`; authentic production ancestor `774dd39a951c9ac3818e83dfffd4c7666efb0a20`.
- [Manifest](candidate.json), [two-file repair delta](repair.patch), [eight-file complete application delta](application.patch), and exact new [runtime](candidate-files/scripts/survey_stage_validation_v2.py) / [tests](candidate-files/tests/test_survey_freeze_stage_boundary_v2.py).
- The six a1 files are unchanged. No schema, approval producer, Human Gate or Release implementation changes. [Scope and rationale](scope.md).

Native `/tmp/jgas-rephase-freeze-b1b2` is a separate copy with its own Git database, inert origin and no alternates. It preserves the full authentic tree but materializes a sparse working tree. [Preparation](prepare.py) / [setup](setup.json). This is an isolated review commit, not a production branch or the Human-owned final reconstruct commit.

## Tests and before witnesses

[Root integration runner](finalize.py) records exact command, fixture, head and runtime/test hashes. It injects the eighth test before freezing. Its historical one-shot preparation steps intentionally refuse an existing target/modified base; do not rerun it over finished evidence. To repeat only regression, use the command in its result JSON from the recorded fixture.

| Evidence | Result and limit |
|---|---|
| [B1 before log](before-b1.log) / [identity](before-b1.json) | Same new connected positive on a1 fails at `unexpected current stage artifacts: visual-review-record` |
| [B2 before log](before-b2.log) / [identity](before-b2.json) | Same typed-loader positive on a1 fails because Publication approval lacks Stage Checkpoint `artifacts` |
| [Frozen-head regression log](targeted-regression.log) / [identity](targeted-regression.json) | **24 tests passed**, 8 new boundary tests, 3 upstream stage, 5 upstream agent-control, 8 upstream publication tests; 45.154 seconds unittest runtime |

Before witnesses used a separate database copy `/tmp/jgas-rephase-freeze-before`; a1 runtime was restored from Git there, with identical new test bytes. They are intended failures at the identified boundaries, not setup errors. The candidate was not swapped while tests ran.

New positives exercise real Weekly Candidate creation, stage validation, report generation, checkpoint construction, low-level approval and State advancement to FROZEN; another positive covers active #495 publication revalidation followed by Freeze stage validation. The latter does not independently repeat the final checkpoint advance. Negatives cover missing/extra/wrong pre-preview visual, pending approval even with an inert approval file, missing/divergent approval authority, Candidate byte drift, approval-hash refresh forgery, and a non-publication checkpoint carrying the wrong type.

Research/editorial/visual/Human judgments and accepted upstream history are synthetic fixture data. No new authority mocks or Git-success stubs are used in the boundary module; the upstream fixture remains synthetic. Low-level `approve_publication_preview` is not an independent canonical durable-reviewed-commit Human Gate roundtrip. Weekly is the new connected execution; Special/Retrospective full Freeze execution is not covered. Existing profile-contract tests do not close that gap. FROZEN is not an executed publication release.

Root resumed from a seven-test file left by the fresh-context Sol Worker; no Worker completion report was available after session continuation. Root reviewed the file, observed 7/7 passing before adding the typed-loader witness, and owns all saved before/final executions. The preliminary seven-test output is in the task tool transcript, not a separate saved log. Do not attribute root results to an independent reviewer. A fresh-context Astra Auditor, separate from root/Worker and the prior readiness Auditor, owns its report under `auditor/`.

## Remaining boundary

[Independent report](auditor/review.md) concludes no actionable finding in the two-file repair. Its [own source checks](auditor/source-checks.json) bind exact candidate identity, surrounding fixed source and reviewed root logs; Auditor did not execute the tests. [Root closeout](closeout.json) verifies the unchanged prior 41 sealed inputs and six a1 files, candidate/test identity, local links and final report hashes. Root closeout is not an Auditor signature.

This is not the interrupted broad a1 suite, full CI, canonical seven-point audit or production approval. B3 reader coverage/derivation remains unresolved. Windows execution, full Special/Retrospective paths, real Actions/transport, historical closure and net lifecycle savings remain unproven. Do not broaden or repeat successful checks solely to decorate this bounded result.
