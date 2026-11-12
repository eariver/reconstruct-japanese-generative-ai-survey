# Affected verification — frozen supplement-carry implementation (independent runner, no code/test edits)

Packet: `notes/rephase-1-supplement-carry-repair-20261106/affected-verification-20261107T031826Z`
Workcopy: `.rephase-1-editorial-runtime/supplement-carry-implementation-20261106T131722Z/candidate-work`
Runner role: independent regression runner (not author/reviewer). No subagents. No source/test edits. No active e84/proof mutations. No reconstruct readback/network/Production.

## Source bounds (verified pre/post identical)

- Intended: 772 = 771 tracked (`git ls-files --cached` 771) + 1 untracked new test `tests/test_dm022_supplement_carry_v2.py`
- Exactly 2 runtime changed + 1 test added: `M scripts/survey_research_authority_v2.py`, `M scripts/survey_prearchitecture_acceptance_v2.py`, `?? tests/test_dm022_supplement_carry_v2.py` (porcelain pre/post identical, diff --stat 2 files 453+/23-)
- SHA256 worktree pre/post identical: LOW `d50282bf0812a4d07e3da13cf3574961add0466cd27a3ef3c648b89fe40330dd`, HIGH `f312f02e2dc5c1aa5a1d6432bca134cd83f0a1edea2d127721d0206d05514a90`, NEWTEST `5d5d3aadec70bc5d5c22fdec3e3c65d4f38d73aa995d326d8927fb8f73e26f00`
- HEAD isolated `5eef790bd8d492c557cc4db9c29425e3e410d47d` (new root, NOT 409 ancestry), inert origin `https://invalid.invalid/inert.git`, no alternates
- Loaded module paths: both LOW/HIGH resolve to `candidate-work/scripts/...` (see `pre-loaded-module-paths.txt`)
- Process-scoped identity: workcopy local `user.name=supplement-carry-impl`, `HOME=/home/eariver` unchanged, `GIT_*` env empty, `PYTHONDONTWRITEBYTECODE=1`, `GIT_CONFIG_NOSYSTEM=1` in fixtures, no HOME/gitconfig writes, no `--allow-empty`
- Git only explicit isolated fixture/source: only `git -C candidate-work` for status/diff/hash; no `git -C .` reconstruct readback; e84 (`.../evidence-scaling-w34-retry...`) and proof-copy (`.../evidence-scaling-packaging.../proof-copy`) mtimes Nov1/Nov4 untouched
- Fixtures: existing tests' own lifecycle normal cleanup limited legitimate temp fixture scope; preserved failed raw/explicit fault partial in batch-05 raw; no separate blanket clean. All fixture approvals remain labelled synthetic (`SYNTHETIC_FIXTURE_*`, `example.invalid`), no Human authority.

## Pre-execution inspection

- Forbidden helper config/bypass: COMPLIANT — only comments + process-scoped `GIT_AUTHOR/COMMITTER` + `GIT_CONFIG_NOSYSTEM` + `git -c user.*` on commit, never `--allow-empty`/HOME mutation/verified-dict/public-context/global-cache; `mock.patch` only fault-injection negatives (Path.read_bytes, sha256_file, validate_instance, verify_state_basis) + private-slice probes, no stub of `_resolve/_merge/_build_card/validate/build_revision_package` to hide parent failure. Safe under strict policy, no relaxed-policy needed.
- Capability: COMPLIANT — no TinyTeX/pdflatex/OLD_ROOT/Production/network/CURRENT_PROOF in 6 target files; only `https://example.invalid` synthetic URLs (no network).

## Batches (unique per-module processes, no aggregate source claims, unmasked exits)

- Batch 01 evidence LOW (7): `tests.test_survey_evidence_v2.SurveyEvidenceV2Tests` — 7 run, 7 pass, 0 fail, 0 skip, 2.010s, exit 0. Raw: `batch-01-evidence-low-raw.txt` (argv/cwd/env/PID 697828/START 20261107T031934Z/END 20261107T031936Z/pre-post SHA identical). Source bounds 772 as above.
- Batch 02 interactive (2): `tests.test_run_evidence_v2_interactive.InteractiveEvidenceProfileContractTests` — 2 run, 2 pass, 0 fail, 0 skip, 0.001s, exit 0. Raw: `batch-02-interactive-raw.txt` (PID 698324/031941Z-031942Z).
- Batch 03 scaling whole19 (19): `tests.test_evidence_scaling_v2` whole file — 19 run, 19 pass, 0 fail, 0 skip, 8.217s, exit 0. Raw: `batch-03-scaling-whole19-raw.txt` (PID 698710/031947Z-031955Z). Appropriate shared phase/no-supp/COPY/history + RAW negatives per task.
- Batch 04 HIGH A2 (14): `tests.test_dm022_prearchitecture_acceptance_v2.Dm022A2OperationTests` 14 targeted — 14 run, 14 pass, 0 fail, 0 skip, 29.947s, exit 0. Raw: `batch-04-high-a2-raw.txt` (PID 699447/032003Z-032034Z).
- Batch 05 C direct (6): `tests.test_dm022_c_direct_operation_v2.Dm022CDirectOperationTests` 6 targeted — 6 run, 5 pass, 1 fail, 0 skip, 13.273s, exit 1. Raw: `batch-05-c-direct-raw.txt` (PID 700562/032041Z-032054Z). STOPPED batch on unexpected failure, no fix/rerun/cleanup. See failure below.
- Batch 06 Profile selected (4): `DM017OrdinaryInputTests.test_14/test_14b` + `DerivedOperationTests.test_23/test_24` — 4 run, 4 pass, 0 fail, 0 skip, 2.067s, exit 0. Raw: `batch-06-profile-selected-raw.txt` (PID 701241/032110Z-032113Z). Concrete changed path: LOW prove unaffected View/ledger + HIGH prepare seam touch ledger/completeness semantics; these 4 cover real-ledger derivation + DERIVED many-to-many + lossy refusal per inventory §9 Thematic/obligations. No broader Profile sweep.

Totals (no sum claim for source): 52 run, 51 pass, 1 fail, 0 skip across 6 batches.

## Unexpected failure (batch 05, concrete, no fix)

- `test_c_binding_integrity_drift` FAIL — `AssertionError: 'request.records must cover exact non-DROP Discovery IDs [67 chars]ion)' != 'request.records[1] discovery_id is not a bound effective[51 chars]IDs)'`
  - Expected (old oracle): `request.records[1] discovery_id is not a bound effective Discovery ID (records bind E DIDs, never invented IDs)`
  - Actual (repaired code): `request.records must cover exact non-DROP Discovery IDs (no new/omitted/DROP/extra unused IDs allowed in same-State correction)`
  - Context: repaired `build_revision_package_from_paths` now enforces exact non-DROP/affected coverage per integration-map-r2 §4 before old effective-DID check; invented-ID negative now refuses earlier with new message (still fail-closed, State/guard preserved, no write). Post-SHA unchanged (d50282/f312/5d5d), exit 1 preserved in raw, no rerun/cleanup.
  - No source fix/local rerun/cleanup performed. Returned for root decision (oracle update vs precedence adjustment). Not claimed as PASS.

## Unexecuted proposed tests (explicit, not run)

- `test_survey_evidence_v2` remaining 5 (not affected subset): `test_factual_evidence_rejects_editorial_fields_and_unregistered_sources`, `test_source_type_taxonomy_is_explicit_and_rejects_lexical_spoofing`, `test_discovery_source_class_must_match_derived_authority_without_supplement`, `test_issue_191_comparator_owned_metric_cannot_bind_primary_subject`, `test_materiality_ledger_prevents_issue_166_silent_drop_and_preserves_non_material_state`
- `test_run_evidence_v2_interactive` remaining 6 profile-field validations (weekly/thematic/retrospective pass/reject): `test_weekly_input_passes_without_thematic_fields`, `test_weekly_rejects_thematic_only_fields`, `test_thematic_input_requires_and_accepts_thematic_fields`, `test_retrospective_input_passes_without_thematic_fields`, `test_retrospective_rejects_thematic_only_fields`, `test_retrospective_rejects_weekly_only_fields`
- `test_dm022_prearchitecture_acceptance_v2` remaining 11 (loader/guard/slot extras not in §9 targeted): `test_low_typed_loader_dispatch`, `test_loader_accepts_str_path_same_as_path`, `test_loader_wrong_family_str_path`, `test_low_guard_and_slots`, `test_malformed_review_result_refuses`, `test_stale_and_unsupported_inputs_refuse`, `test_slot_ownership_faults`, `test_replace_tmp_exists_refuses`, `test_completion_idempotent_reuse`, `test_explicit_empty_index_allows_prepare`, `test_unreadable_paths_fail_closed_not_coerced`
- `test_dm022_c_direct_operation_v2` remaining 1: `test_c_report_positive_control_extra_rows_pass`
- `test_profile_support_upstream_repair_v2` remaining 24 (not in selected 4): all other DM016/DM017/ProfileParity/History/Prepackage/Guard tests
- Heavy/non-affected excluded per task+inventory: `test_dm022_full_lifecycle_v2` (all PDF/TinyTeX/full publication), `test_dm022_g71_g76_compatibility_v2`, `test_dm022_publication_depth_boundary_v2`, `test_versioned_renewal_source_phase_s` (CURRENT-proof heavy)
- New test file `test_dm022_supplement_carry_v2` (14 tests) NOT run — new implementation tests, not existing regression.

## Files in this packet (never overwrite raw)

- `pre-status-porcelain.txt`, `pre-diff-stat.txt`, `pre-sha256-pins.txt`, `pre-loaded-module-paths.txt`, `pre-env.txt`, `pre-gitconfig-local.txt`, `pre-gitconfig-global.txt`, `pre-inspection.txt`
- `batch-01-evidence-low-raw.txt`, `batch-02-interactive-raw.txt`, `batch-03-scaling-whole19-raw.txt`, `batch-04-high-a2-raw.txt`, `batch-05-c-direct-raw.txt`, `batch-06-profile-selected-raw.txt`
- `post-snapshot.txt`, `SUMMARY.md` (this file)
