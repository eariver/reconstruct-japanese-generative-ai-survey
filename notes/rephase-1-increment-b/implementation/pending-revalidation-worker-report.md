# Increment B pending publication revalidation — Sol worker packet

2026-09-26 JST. This is a bounded implementation and test result, not B acceptance or an independent audit.

## Fixed development identity and scope

- Isolated fixture: Ubuntu `/tmp/jgas-rephase-increment-b-sol-implementation`, branch `codex/rephase-1-increment-b`, inert `https://example.invalid/rephase-increment-b.git` origin, independent `.git` database, no alternates or inherited Git-root overrides at start.
- Milestone commit: `e0d72c7b25fcf42271c30d51073938c57f77ad27`, parent `daa1dd3b0f1294a83bea1738d9bdfb3dcac80712`.
- Explicit commit paths: `scripts/survey_agent_control_v2.py`, `scripts/survey_agent_tool_v2.py`, `scripts/survey_weekly_derivation_v2.py`, `tests/test_survey_increment_b_weekly_derivation_v2.py`, and two precise rejection-assertion changes in `tests/test_survey_publication_revalidation_v2.py`.
- No runtime edits occurred after `e0d72c7`. `git diff --cached --check` passed before the commit. The only tracked worktree difference on recovery was the pre-existing, separate three-test obsolete-fixture cleanup in `tests/test_survey_reader_surface_gate_v2.py`. The untracked boundary matrix test and Python caches also remained. None of those files was invoked as a test module in this packet.

The controller builds a checked, immutable pending basis from the canonical State, exact validation checkpoint, current configured publication roles and bytes, actual HEAD, and immutable predecessor. The private complete-State validator applies only that checked basis; public State and artifact resolution remain strict. Weekly receipt replay and the existing Evidence current-stage wrapper use it while publication bytes legitimately differ. The writer checks the same row set and full basis before writing, rejects a no-op repeat and wrong implementation override, and restores the original State/removes its new record on the tested post-write failure. The older chain now applies shared immutable row and QA-reference checks to each link; equal recorded instants are valid, while later predecessor instants fail. A copied State or directory-symlink alias cannot substitute for the canonical path.

## Raw commands and outcomes

All commands ran from the isolated fixture using the executable `/tmp/jgas-rephase-application-venv/bin/python3.12` (Python runtime version 3.12.14) with installed `jsonschema 4.23` / `pypdf 6.16`. Full raw output is in the linked log files. The exact-head commands used `python3.12 -m unittest -v` followed by the listed modules.

```powershell
wsl -d Ubuntu --cd /tmp/jgas-rephase-increment-b-sol-implementation -- /tmp/jgas-rephase-application-venv/bin/python3.12 -m unittest -v tests.test_survey_increment_b_weekly_derivation_v2 2>&1 | Tee-Object -FilePath notes/rephase-1-increment-b/implementation/pending-exact-head-dedicated.log; exit $LASTEXITCODE
wsl -d Ubuntu --cd /tmp/jgas-rephase-increment-b-sol-implementation -- /tmp/jgas-rephase-application-venv/bin/python3.12 -m unittest -v tests.test_survey_publication_revalidation_v2 tests.test_survey_human_gate_revalidation_revision_v2 tests.test_survey_exact_manuscript_admission_v2 tests.test_survey_agent_tool_v2 tests.test_survey_agent_control_v2 2>&1 | Tee-Object -FilePath notes/rephase-1-increment-b/implementation/pending-exact-head-regressions.log; exit $LASTEXITCODE
wsl -d Ubuntu --cd /tmp/jgas-rephase-increment-b-sol-implementation -- /tmp/jgas-rephase-application-venv/bin/python3.12 -m unittest -v tests.test_survey_stage_validation_v2 tests.test_survey_freeze_stage_boundary_v2 2>&1 | Tee-Object -FilePath notes/rephase-1-increment-b/implementation/pending-exact-head-stage.log; exit $LASTEXITCODE
```

| Modules / command suffix | Raw log | Observed result |
| --- | --- | --- |
| `tests.test_survey_increment_b_weekly_derivation_v2` | [pending-exact-head-dedicated.log](pending-exact-head-dedicated.log) | 8 tests, 202.418 s, `OK`. The final log survived the prior agent usage-limit stop; its original shell exit status was not retained. |
| `tests.test_survey_publication_revalidation_v2 tests.test_survey_human_gate_revalidation_revision_v2 tests.test_survey_exact_manuscript_admission_v2 tests.test_survey_agent_tool_v2 tests.test_survey_agent_control_v2` | [pending-exact-head-regressions.log](pending-exact-head-regressions.log) | 52 tests, 101.260 s, `OK`, captured exit 0. |
| `tests.test_survey_stage_validation_v2 tests.test_survey_freeze_stage_boundary_v2` | [pending-exact-head-stage.log](pending-exact-head-stage.log) | 11 tests, 42.599 s, `OK`, captured exit 0. |

The dedicated test uses an isolated Git fixture and real six-stage producer chain through `DRAFT_COMPLETE`, then generated Gate, `VALIDATED_DRAFT`, first and repeated publication revalidation, active State/receipt/Gate readback, and negative checks for copied/aliased State, controller/history drift, stale basis, wrong role/path, malformed predecessor/chain, upstream and QA mutation, wrong implementation override, no-op repeat, and bounded rollback. Its reviews and blank PDF are explicitly synthetic. It also probes artifact-only HEAD movement, control changes, generated text/bibliography, and the historic omission matrix.

Intermediate raw failures remain in [jgas-b-pending-renewal-1.log](jgas-b-pending-renewal-1.log) (absolute State-path setup failure) and [pending-affected-regressions-1.log](pending-affected-regressions-1.log) (52 tests: two errors from equal-time chain chronology and two assertions expecting older error wording). The repaired renewal probes and earlier two-pass logs remain alongside them. These failures are not reclassified as clean initial runs.

## Selected test identities at the milestone

The eight invoked test modules below matched `e0d72c7` bytes on recovery; SHA-256 values are filesystem bytes, not Git object IDs.

| Test module | SHA-256 |
| --- | --- |
| `test_survey_increment_b_weekly_derivation_v2.py` | `dc11e58ddfb624fd5234e6ecd4e2df197a591433dfe8b2a299b073df16e90068` |
| `test_survey_publication_revalidation_v2.py` | `b28411bac3772622a833cc6c2a66445d0ab1b5e82a648dd1c21b7884b0aa053a` |
| `test_survey_human_gate_revalidation_revision_v2.py` | `1ec4b8ff13efd1ad3e8ee46af0da49148270080b4e0bce9ce61c980e900c6890` |
| `test_survey_exact_manuscript_admission_v2.py` | `f695ba6611ef0d7c3eb88a261176f2e6b774916570215437c525c6f026b0a10d` |
| `test_survey_agent_tool_v2.py` | `415b5b0e80929b218e5c6b673b2b9533ef3e7bc0a2d34ef7f5a702017c029689` |
| `test_survey_agent_control_v2.py` | `4d4fc489505607cbb2516b20885fe64e840b842366702b28f58c7f26a1b9cdfa` |
| `test_survey_stage_validation_v2.py` | `6b376293d00c141b24ac8d29eb68f5ca151d46a7e1358cdee31be9839e53071c` |
| `test_survey_freeze_stage_boundary_v2.py` | `6a1c83da7fff56e99d53df60e6cd1ec14e91df5c06231dda01f7a5c40cb1f0c1` |

On 2026-09-26 recovery, the separate uncommitted `test_survey_reader_surface_gate_v2.py` hash was `2157c7fb55c21f469161480ce4942ab28fff8730571d8b086eca625efbffa21b`; untracked `test_survey_increment_b_boundary_matrix_v2.py` was `b15bef8d5e6fea008101deae35a2befc7ebc66b39fb8f91811104f05cc289b06`. The latter changed from its September 25 working hash while the other worker continued. Neither is part of this committed milestone's test claim.

The selected run does not establish real Human/editorial approval, a real TeX publication, all profiles, or the complete reviewed-Core CLI regeneration flow at `VALIDATED_DRAFT`. The publisher CLI remains `DRAFT_COMPLETE`-only with no overwrite. A subsequent combined candidate commit changes HEAD and requires its own final matrix and independent review; this packet does not transfer PASS to it.
