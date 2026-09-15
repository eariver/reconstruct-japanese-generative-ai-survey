# Re:Phase 1 — Git-free execution-record unit evidence

Fixed production baseline: `774dd39a951c9ac3818e83dfffd4c7666efb0a20`. Candidate: unchanged r2. Decision: [runtime assessment](../../outputs/rephase-1-runtime-assessment.md).

## What ran

The exact fixed-baseline `tests/test_survey_execution_record_v2.py` class ran against the complete r2 `survey_execution_record_v2.py`, with real copied fixed dependencies. All five tests passed. `initialize()` writes real fixture index/session files and `validate()` checks those files.

The upstream tests already mock `_load_profile` and `_load_state`. They were not edited and these mocks were not expanded. Thus this is a mocked-loader unit test result, not a test of authentic State/Profile/schema/contract/approval/commit validation. No additional authority mock or fake Git response was added.

## Files

- `inputs.json`: 19 source/test dependency inputs, fixed-ref URLs and hashes. Reused/fetched with the previously inspected `notes/rephase-1-contract/inputs.py` helper, with its output directory set here. No ref lookup.
- `import-audit.json`: captured source dependency inventory, external import names and module-level non-definition statements from static AST inspection. Imports inside functions were not a complete dynamic call graph. Wrapper assignments/decorators/constants were inspected; runtime denial is an additional safeguard.
- `run_unit_tests.py`: verifies hashes, copies fixed sources and r2 helper into an isolated temporary directory, then runs the unchanged five-test class. Invoked with `python -I -B -X utf8 notes/rephase-1-runtime/run_unit_tests.py`.
- `unit-tests.txt`: exact unittest output.
- `unit-results.json`: test outcome, original loader mocks, Python version, copied-file hashes, actual imported script modules, unchanged r2 identities, denied-operation requests (empty).

The baseline scripts/tests are namespace packages; no artificial `__init__.py` or production module replacement was added. Only the proposed r2 helper bytes replace the baseline helper in the isolated copy. `runpy` executes the unchanged test file under a non-main name and unittest loads its class. Imported script origins are checked to be inside the sandbox. Python isolated mode excludes the workspace's normal startup/import path.

Before target import, a Python audit hook denies process launches, network connect/bind/name lookup and `.git` file/directory reads. Denial records the event and raises an exception, never returns simulated success. This is a bounded no-Git execution safeguard, not a general malicious-code sandbox. No prohibited event was requested. Temporary fixtures were contained under the newly created ignored runtime directory and removed at completion. Source and candidate bytes were checked before/after.

## Limits

Actual fixed-code modules were imported and exercised in the copy; no production checkout or actual edition operation was used. Git operations, remote main/ref reads, production mutation, external posting and independent agents were not used. Core/CLI/bridge/Actions/full Human Gate execution remain unverified. Existing bridge E2E was statically identified as Git-dependent and not run. Old independent-review evidence remains valid only for its original bounded scope and unchanged candidate bytes.

Do not rerun successful tests without a change/new concern. Do not discover the entire upstream suite under the Git prohibition or present these five tests as full Core integration.
