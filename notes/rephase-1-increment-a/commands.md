# Commands and outcomes

All commands ran under WSL Ubuntu. Test output combines stdout and stderr as returned by the runner.

## Exact-head dedicated tests

Working directory: `/tmp/jgas-rephase-increment-a-sol-copy`

```sh
/tmp/jgas-rephase-application-venv/bin/python -m unittest -v tests.test_survey_exact_manuscript_admission_v2
```

Exit 0. 11 test methods passed in 12.066 seconds. The unique-surface method ran 6 passing subtests (missing, duplicate, and conflicting manifest/primary). No skips were reported.

## Exact-head affected existing regressions

Working directory: `/tmp/jgas-rephase-increment-a-sol-copy`

```sh
/tmp/jgas-rephase-application-venv/bin/python -m unittest tests.test_survey_reader_surface_gate_v2 tests.test_survey_publication_revalidation_v2 tests.test_survey_freeze_stage_boundary_v2
```

Exit 0. 61 tests passed in 72.959 seconds. No skips were reported.

## Separate parent defect witnesses

Working directory: `/tmp/jgas-rephase-increment-a-parent-witness`

```sh
PYTHONPATH=. /tmp/jgas-rephase-application-venv/bin/python /tmp/jgas-rephase-increment-a-sol-copy/tests/test_survey_exact_manuscript_admission_v2.py ExactManuscriptAdmissionV2Tests.test_draft_complete_rejects_valid_same_identity_alternate_manuscript ExactManuscriptAdmissionV2Tests.test_validated_draft_rejects_valid_same_identity_alternate_manuscript ExactManuscriptAdmissionV2Tests.test_revalidation_rejects_wrong_gate_before_authority_write ExactManuscriptAdmissionV2Tests.test_later_stage_rejects_fresh_wrong_gate_under_active_revalidation
```

Exit 1 as intended. Four assertions failed because f1 raised no rejection. These are defect witnesses, not a failed successor run.

## Runtime

`/tmp/jgas-rephase-application-venv/bin/python`: CPython 3.12.14; jsonschema 4.23.0; pypdf 6.16.2. No dependency installation or refresh occurred during Increment A.

## Isolation and identity

The executed shell body is preserved in `isolation-command.sh`; its raw combined output is in `isolation.log`. They cover candidate/parent/original-f1 commit and tree identities, status, inert remotes, alternates, inherited Git environment, multiply linked Git object search, runtime, changed-file hashes, and all eight original f1 hashes.
