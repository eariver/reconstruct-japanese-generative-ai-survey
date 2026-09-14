# Re:Phase 1 — r2 connection evidence

Fixed baseline: `774dd39a951c9ac3818e83dfffd4c7666efb0a20`. Initial connection work was root-only. One later explicitly authorized independent review is now complete; see the closeout below. No Git operations, remote refs/main, production imports/execution/mutation or external posting.

Decision: [connection assessment](../../outputs/rephase-1-connection-assessment.md). Prior [r1 evidence](../rephase-1-contract/README.md) is unchanged historical input.

## Artifacts

- `candidate.patch`: complete five-file r2 proposal from fixed production baseline.
- `r1-to-r2.patch`: only follow-up repairs; overlay is unchanged from r1.
- `candidate-files.json`: baseline/r1/r2 hashes.
- `build_r2.py`: reconstructs r1 from its saved patch with exact hash checks, then builds r2 under ignored `.rephase-1-inputs/contract-candidate-r2/`. It does not invoke the original builder or rewrite r1 artifacts.
- `inputs.json`: 11 targeted fixed-source inputs, including reused inputs. The previous manifest plus this one cover 41 distinct files.
- `local-scan.json`: initial local-cache string scan, with blob-verified file hashes and hits. This is a snapshot of that scan, not the later capture inventory. It covered 212/212 Python scripts, 3 tests and no workflows; 190 tests and 7 workflows were not then present with matching bytes. The later 2 bridge tests, final-audit test and 2 CI files are in `inputs.json`. A name search does not prove absence of dynamically constructed calls.
- `verify.py` / `checks.json`: five grouped r2 checks, including four executed upstream document-only tests. It does not run the execution-record tests or any production module.
- `upstream-document-tests.txt`: exact four-test result. Fixed `test_survey_final_audit_rule_v2.py` imports only stdlib and reads rule, AGENTS and bootstrap; it ran against isolated real document copies, with r2 bootstrap. No reviewed-commit mocks.
- `template-examples.json`: actual saved Profile shapes, synthetic session values, AST-extracted f-strings only. The `EXAMPLE_ONLY` paths do not represent real sessions or Human decisions.

## Capture and review boundary

Missing source was acquired only through immutable raw URLs using the prior inspected `inputs.capture` helper with its output directory set here. It first reused local bytes when their blob hash matched the saved complete tree. No Git executable/database operations or ref endpoints were used. Inputs are under `.rephase-1-inputs/<fixed-ref>/`; the production checkout was not used.

The initial scan searched Python/workflow text for `execution_record`, `execution-record`, `Current lifecycle`, `Current State SHA-256`, `Final disposition`, and `execution/index.md`, using only locally available matching blobs. The decisive caller is `scripts/survey_core_execution_bridge_v2.py:285–301`; it calls initialize/validate and returns paths. The helper's CLI is unchanged. `tests/test_survey_execution_record_v2.py` has five tests and uses mocked Profile/State loaders. These tests were inspected, **not run**. Bridge E2E calls `repository_commit_sha`; it was not run. The two CI files discover the existing tests; CI was not run.

The follow-up found and repaired hardcoded review-path navigation, missing objective/mode navigation, broad Markdown wording, and the new Frozen-edition wording. Pending review navigation was clarified. The transport heading's omission predates r1; r2 adds the already-required policy heading because its new navigation points there, without retroactively requiring new headings in old records. This is a producer/policy alignment, not complete execution-record semantic validation.

`verify.py` evaluates templates, compares AST and retained sections, roundtrips the saved patch, verifies captured source hashes, and runs the inspected document-only test class. No full State dependency closure, contract/reviewed-commit reachability, Candidate/PDF, Actions, runtime or publication quality is certified. Those root checks do not establish net lifecycle savings or independent review. The separately authorized review below provides bounded independent evidence.

## Reproduction

With existing captured inputs, run `python -B -X utf8 notes/rephase-1-connection/build_r2.py`, then `python -B -X utf8 notes/rephase-1-connection/verify.py` from reconstruct. Both are Git-free. Run only when changes justify repeating them. Do not start upstream discovery suites under the current Git prohibition.

## Independent-review closeout

Human explicitly authorized one independent agent for the concrete r2 five-file scope. `independent-review-input.json` records this scope and the unchanged candidate/evidence hashes. `independent-review.md` is the reviewer-authored report: no actionable findings in the bounded scope. The reviewer independently checked all five baseline/candidate hashes, read rules/navigation/revision/caller/test context, and ran no tests. Root retained r2 unchanged; `independent-review-closeout.json` binds the report and confirms unchanged packet/candidate bytes.

Current decision: [review disposition](../../outputs/rephase-1-review-disposition.md). Original connection assessment, candidate, checks and r1 evidence remain unchanged. No repeat tests were warranted by this review. Existing Core/CLI/bridge execution compatibility, final audit, adoption, publication quality and savings remain unproven. This one-agent r2 review permission is completed, not continuing delegation authority.
