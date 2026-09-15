# Re:Phase 1 — fixed-baseline r2 integration evidence

Human lifted the Git prohibition for necessary work and Git-aware verification. Production baseline remains `774dd39a951c9ac3818e83dfffd4c7666efb0a20`; production mutation/adoption and tracking new main remain unauthorized. No independent agents were used in this unit.

Current [assessment](../../outputs/rephase-1-integration-assessment.md); [aggregated results](results.json). Candidate remains the unchanged [five-file r2 patch](../rephase-1-connection/candidate.patch).

## Inputs and environments

- `prepare.py`, `inputs.json`, `setup.json`: 485 hash-verified fixed-tree blobs, 463 cache hits and 22 fixed raw GETs. Control/document/template/Special definition roots plus three test modules; production sources/surveys history is excluded. This is an intentionally bounded snapshot, not a full production checkout.
- Initial independent root: `.rephase-1-inputs/integration-r2/`. Two synthetic commits represent the captured subset and its r2 delta. They are not actual production history. `git diff` between them names exactly the five candidate paths.
- `setup_native.py`, `native-environment.json`: final independent Ubuntu root `/tmp/jgas-rephase-r2-502b3781`. Cloned locally with `--no-local`, verified `.git` root and absence of alternates, then changed origin to an inert URL and removed clone-created remote-tracking refs. Source reconstruct/production Git databases were not used for fixture objects.
- `requirements-resolved.txt`: resolved Python dependencies in workspace-local `integration-venv`. Fixed Core requirements are jsonschema 4.23.0 and pypdf 6.16.2. Bootstrap used the official pip zipapp because Ubuntu had neither pip nor ensurepip; no system package install.

`prepare.py` is one-shot and refuses to overwrite a prior fixture. Native setup is also for a dedicated fixture, never a production checkout. `/tmp` contents are disposable; durable inputs/hashes/scripts here preserve the reconstruction route. Generated CLI editions remain only in that fixture and are synthetic. No source/survey production history was changed or regenerated.

## Tests and results

- `run_suite.py`: executes the three named unchanged upstream test classes, avoiding duplicate discovery of the imported fixture class. The final run selects only previously failed IDs. Test Profile/State/Gate functions are real; no new mocks. A test-side audit guard permits inspected local Git verbs only, asserts subprocess cwd/private index are inside the fixture, and rejects network operations. It returns no fake Git success.
- `linux-guard-attempt-suite.txt`: first Linux run, 27 tests / 18 pass / 9 guard errors.
- `upstream-suite.txt`, `upstream-results.json`: final 9 previously incomplete tests / 9 pass / no errors, skips or blocked operations. They include real Git review snapshots, branch reachability and exact committed-file checks. HEAD and normal index unchanged; temporary remote refs cleaned.
- `run_cli.py`, `cli-commands.json`, `cli-results.json`: 21 actual child CLI calls across Weekly, Thematic and configured monthly Retrospective. Real Core initialize/validate-state plus execution-record init/validate; Profile byte drift, destructive reinit and issue mismatch negatives. No loader mock or implementation-SHA override. Git resolves the actual synthetic r2 HEAD.
- `run_navigation.py`, `navigation-results.json`: actual synthetic Architecture gate pending/revision/approval transitions with unchanged index bytes and successful execution-record validation. Removing the active approval is rejected even when review history contains APPROVED. Synthetic research/Human decisions are not real publication/review evidence; session prose completeness is not evaluated.
- `summarize.py`, `results.json`: combines distinct passing test IDs (18+9=27), checks all captured bytes against fixed baseline/r2, and verifies r2 and its original review packet remain unchanged. It does not rerun tests.

Final test execution used Ubuntu Python 3.10.6 with the recorded dependencies. Entry command pattern is `REPHASE_FIXTURE_DIR=/tmp/jgas-rephase-r2-502b3781 <workspace integration-venv>/bin/python3 -I -B -X utf8 <script>`. CLI children run their real `-m scripts.*` entry points inside the fixture. Do not rerun successes without a changed concern.

## Setup attempts, kept distinct

- `setup-attempt-suite.txt`: first Windows guard had incorrectly assumed audit-event executable/argv shapes. unittest reported 21 tests and 6 errors (including setup failure), not the eventual 27-test result. Fixed only the wrapper.
- `windows-suite.txt`, `windows-results.json`: Windows-corrected guard run, 27 tests / 11 errors. Ten hit fixed Core's backslash-versus-relative-path authority mismatch; one lacked Asia/Tokyo tzdata. The r2 helper had not caused these initial-State failures. Windows integration is not certified.
- `linux-guard-attempt-results.json`: missing test-side allowlist entry `check-ref-format` caused nine failures. The next partial run's `linux-tree-guard-attempt-suite.txt`/`...results.json` preserves nine `ls-tree` guard failures. Allowed those inspected read-only Git checks (and `show-ref`), with no Core change, then reran only these nine IDs. The final guard reports zero rejected requests.
- `cli-cutoff-attempt.json`: initial fixture time preceded W36's cutoff and was rejected before initialization; corrected fixture time to 2026-09-08. The cutoff rule was not changed.

An initial shell read of an old fixture commit used an unquoted PowerShell `^{commit}` expression and failed parsing; quoted retry showed that old fixture lacked the fixed production object. No test result derives from that probe. These setup errors are not concealed as product repairs or successful first runs.

## Limits and isolation

There are real new Git objects/commits/temporary refs in the independent fixtures. This is authorized test work, not a claim of no Git mutation. No remote production fetch/main tracking, production checkout changes, posting, Actions dispatch, production commit or adoption occurred. Reconstruct's ordinary final commit/Pull/Push remain Human-owned.

This is bounded synthetic integration, not full upstream CI, all Profile publication execution, final seven-point audit, real quality review or net lifecycle savings. Existing full-production Frozen/reader counterexamples were not repaired or replayed wholesale. Prior independent-review scope remains unchanged and is not promoted to an independent integration audit.
