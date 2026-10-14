# P2R PhaseA source binding (read-only)

Candidate: `/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z/candidate-partial-b40de60` — detached `409b292756dd1277b9dfae87679934c0d2ce251c`/tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, 3M10A, all13 exact vs `notes/rephase-1-dm021-p1/evidence-20261012T072355Z-correction4/freeze-post.json`. Raw: `evidence-20261013T122831Z-phaseA/`.

## P1 helpers/APIs bound (all read, no execution)

- `scripts/survey_editorial_correction_proposal_v2.py` (`5d2fde45…`, 110155B): header `:1-23` (read-only, two entries); `_Collector:87-234` (`safe/pinned/reverify`, raw-first, FIFO/device refusal); `_tree_map:267-318`; `_eligibility:327-342`; `_route_of:345-352`; `_load_profile:414-428`; `_derive:431-445`; `_canonical:448-451`; `_Graph:454-481`; `_check_bundle_profile_exact:491-514`; `_build_graph:563-…` (mutable set `:574-595`, State node `:608-614`, bundle/manuscript Profile `:768-776`, candidate observed `:822-862`, checkpoint wrappers/transitives `:864-1092`); `_retention_plan:1231-1288` (dest derivation `:1247`, alias/overlap `:1250-1274`, absent-required `:1278-1282` — post-capture refusal hook); `_pipeline:1291-1492` (proposal dir `:1323-1330`, basis `:1462-1476`, proposed `:1477-1483`); `_validated_state_profile_for_tree:1536-1569`; `_final_full_receipt_recheck:1572-1598`; `prepare_proposal:1601-1632`; `_validate_scope:1635-1695`; `validate_proposal:1698-1830` (layout `:1729-1753`, rederivation equality `:1778-1801`, `input_hashes` + measured `:1823-1830`). Constants: `PROPOSAL_SCHEMA`, `PROPOSAL_ID_RE`, `PROPOSAL_FILES`, `RESULT_REQUIRED/BOUND`, routes.
- `schemas/editorial-correction-proposal-v2.schema.json` (`5623c0d9…`): `schema_version 2.0-rc1`, `proposal_id` grammar, `basis` (9 keys), `proposed` (4 keys), `retention_plan` rows (`roles/path/sha256/byte_count/policy` + XOR `retained_ref/retained_dest`).
- `scripts/survey_production_v2.py`: `DEFAULT_CONFIG` (`config/survey-production-v2.json`), `json_bytes:86`, `sha256_bytes:95`, `sha256_file:99`, `sha256_object:103`, `repository_commit_sha:129`, `contract_identity:150`, `repo_local_path:222`.
- `scripts/survey_schema_v2.py`: `validate_instance:55`, `load_and_validate_json:71`.
- `scripts/survey_longform_derivation_v2.py`: `canonical_reader_bytes:949`, `load_derivation_for_readback:1142`.
- `scripts/survey_agent_control_v2.py`: `CHECKPOINT_SCHEMA`, `REVALIDATION_CHAIN_LIMIT=32`, `validate_agent_state:348`, `resolve_checkpoint_artifact:502`, `resolve_active_evidence_views:615`, `_publication_revalidation_roles:685`, `_pending_conditions:696`, `resolve_active_publication_revalidation:1084`.
- Cited control/receipt/Gate sites (per contract/independent review, re-observed via prior reads, not re-read this unit except P1 above): `survey_agent_control_v2.py:1844-1886` (changed-row support, restricted reason), `survey_longform_derivation_v2.py:1101-1182`, `survey_longform_generated_v2.py:698-730`, `survey_weekly_derivation_v2.py:481-487`, `survey_publication_v2.py:668-746`, `survey_longform_semantic_publication_v2.py:480-486`.

## P1 tests/fixtures bound (read, not executed)

- `tests/test_survey_editorial_correction_proposal_v2.py` (`f581fad0…`, 1847 lines): `_run_git:63` (sanitized `GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file` + synthetic identity), `_make_source_root:75` (`UNTRACKED_SOURCES` 10), `_snapshot:118`/`_assert_no_write:157`, `_new_weekly_helper:164` + `_build_weekly_validated:174` (W_ISSUE), `_new_longform_helper:296` (L_ISSUE), `_stage_authoring_before_prepare:588` + `_stage_reader_and_proposal:600`, `_scope_review_for:612`, `_assert_transitives_expected_set:652`; positives `test_longform_prose_correction_end_to_end:832`, `test_weekly_envelope_positive_and_body_negatives:933`; predecessors `test_honest_predecessor_original_vs_active:1021`, `test_r1_mechanical_refresh_owner:1733` (primary R1: two comment-only commits + `refresh_mechanical_evidence` x2, supersedes depth, ACTIVE origin).

## Raw paths (this unit)

- `evidence-20261013T122831Z-phaseA/README.md` (method + verdict)
- `raw-candidate-head.txt`, `raw-candidate-tree.txt`, `raw-candidate-status.txt`, `raw-candidate-diff-name-only.txt`, `raw-candidate-13hashes.txt`, `raw-candidate-p2r-absence.txt`, `raw-candidate-git-config-remote.txt`, `raw-candidate-git-entries-runtime.txt`
- `raw-reconstruct-head-status.txt`, `raw-contract-p1-sha.txt`
- Fixed inputs: `outputs/rephase-1-dm021-retention-contract-decision.md` (`194fd7de…`), `notes/rephase-1-dm021-promotion/astra-review-resolution.md` (I1–I4), `independent-design-review.md` (§8 incl. §8 resolution), `notes/rephase-1-dm021-p2r/task.md`, P1 freezes `notes/rephase-1-dm021-p1/evidence-20261012T072355Z-correction4/freeze-{pre,post}.json` + `complete-p1-correction-13path.patch` (`85e9d9ab…`).

No code/test/fixture/build/recovery/intake this unit. Limitations: observations are read-only tool outputs transcribed to `raw-*` (no persisted shell transcript); prior P1 qualifications (filtered statuses, HEAD-inode apply proof, transient `add -N`, snapshot≠continuous-proof, synthetic fixtures≠approvals, retention plan≠retained bytes) remain in force.
