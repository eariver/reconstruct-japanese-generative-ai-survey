# Test oracle inventory — DM022 supplement-carry repair

Read-only inventory. No tests, imports, Git commands, network, Production or
reconstruct readback, and no source edits were performed for this document.
Path prefix `SRC` below means:

`.rephase-1-editorial-runtime/evidence-scaling-packaging-20261103T174718Z/proof-copy/candidate-partial-b40de60`

This is an inventory of existing oracles, not an interface-policy decision and
not an integration map. Line numbers are for `SRC` only.

## 1. Current public source entry points

### LOW supplement unit / producer

- `SRC/scripts/survey_evidence_v2.py`
  - `prepare_evidence_package(repo_root, state_path, discovery_path, screening_acceptance_path, output_dir, implementation_sha, supplement_manifest_path: Path | None = None)` — line 828.
  - supplement branch: path resolve/validate 868-892; task `authority_supplement_source_ids` 929-942; package `authority_supplement` + `contracts.supplement` 973-980.
  - `validate_evidence_authority_supplement(repo_root, supplement_path, implementation_sha=None, *, expected_issue_id=..., expected_source_root=..., expected_discovery_path=..., expected_screening_acceptance_path=..., screening_acceptance=..., discoveries=...)` — line 523.
  - `build_evidence_authority_supplement(..., *, supplement_id, implementation_sha=None)` — line 638.
  - `_resolve_phase_supplement_context(repo_root, package, *, implementation_sha, screening_acceptance, discoveries)` — line 300.
  - `_merge_supplement_task_sources(base_sources, task, entries)` — line 469.
  - `_build_card_core(task, meta, package, record, runner, source_authorities)` — line 2228; `source_bindings` gate 2243-2247.
  - `validate_evidence_card(...)` — line 1464; private shared core `_validate_card_core` line 1270; supplement authority branch 1323-1375.
  - `_validate_evidence_package_basis_content` line 1144; `_validate_evidence_acceptance_content` line 1738; `_validate_edition_views_acceptance_content` line 1856; digests `_evidence_result_set_digest` line 1484 and `_view_set_digest` line 2415.

### LOW revision builders used by HIGH

- `SRC/scripts/survey_research_authority_v2.py`
  - `build_revision_package_from_paths(repo_root, request_path, before_copy_path, output_dir)` — line 2128. It derives the package/tasks from Discovery/Screening and does not read `request.supplement_manifest`; the package dict 2225-2268 has no `authority_supplement` and its tasks have no `authority_supplement_source_ids`.
  - `build_revision_cards_views_from_paths(..., *, before_copy_path)` — line 2277; supplement context from the package at 2350, task authority merge 2400/2407.
  - `accept_revision_evidence_views_from_paths(...)` — line 2457; supplement acceptance context 2535/2576.
  - `build_versioned_ledger_from_paths` line 2668; `build_versioned_completeness_from_paths` line 2834; `prove_revision_from_paths` line 3080; `check_supersession_record_from_paths` line 3483.
  - `derive_ordinary_root_effective_context` line 1861; `derive_current_root_effective_context` line 1912.

### True HIGH operation

- `SRC/scripts/survey_prearchitecture_acceptance_v2.py`
  - `prepare_revision(repo_root, state_path, request_path, revision_id)` — line 456.
  - `_contract_and_tools(repo_root, cfg, state)` — line 437; seven tool-pin paths 439-447.
  - request tool-pin live checks 516-522.
  - `adopt_revision(repo_root, state_path, revision_path, decision_path)` — line 1100; tool-pin re-check 1136-1140.
  - `resume_bound_attempt(repo_root, state_path, revision_path)` — line 1348; `resume_revision` line 1444.
  - `readback_revision(repo_root, state_path, revision_path=None)` — line 1449.
  - CLI `main` prepare/adopt/resume/readback — line 1483.
  - Manifest echo of request supplement ref: line 786 (`"supplement_manifest": request.get("supplement_manifest")`).

### Current gap pointers (source, not policy)

- `build_revision_package_from_paths` (line 2128) has no supplement read/carry; `prepare_revision` only echoes the request field into the manifest (line 786).
- Card build already resolves supplement context from the **package** (`survey_evidence_v2._resolve_phase_supplement_context`), and `_merge_supplement_task_sources` requires task `authority_supplement_source_ids`. Therefore, if a request binds a supplement ID in `source_bindings` but the package/task carry is absent, the actual failure is at card build, not at request schema validation.

## 2. Supplement LOW unit — existing tests and fixtures

All are in `SRC/tests/`.

### Core supplement validator / producer

- `test_survey_evidence_v2.py::SurveyEvidenceV2Tests::test_evidence_authority_supplement_binds_exact_raw_source_and_card` — line 666.
  Real `build_evidence_authority_supplement`, `prepare_evidence_package(..., manifest_path)`, task `authority_supplement_source_ids`, `task_authority_sources`, card source update, `validate_evidence_card`, unbound-URL negative.
- `...::test_evidence_authority_supplement_rejects_drop_unknown_path_sha_and_symlink` — line 755.
  Exact DROP, unknown Discovery, traversal, Raw SHA drift, source-class mismatch, byte-count drift, symlink refusals.
- `...::test_zero_byte_authority_fails_schema_and_independent_runtime_without_output` — line 855.
- `...::test_discovery_source_class_must_match_derived_authority_without_supplement` — line 484.
- `...::test_evidence_package_is_exact_and_preserves_task_bytes` — line 365; result-set directory equality at 376.
- `...::test_evidence_result_set_rejects_extra_artifacts_and_detects_accepted_tampering` — line 378.

### `source_bindings` input contract

- `test_run_evidence_v2_interactive.py::InteractiveEvidenceProfileContractTests::test_multiple_task_bound_sources_require_explicit_bindings` — line 163.
- `...::test_single_source_legacy_input_remains_backward_compatible` — line 172.

### Scaling-repair LOW oracles

- `test_evidence_scaling_v2.py::EvidenceScalingRepairTests::test_golden_full_card_public_builder_matches_reviewed_baseline_and_validates_clean` — line 316.
- `...::test_unit_private_slices_match_public_authority_map` — line 427.
- `...::test_repo_root_none_structural_nonsupplement_unbound_cases_are_exact` — line 599.
- `...::test_lazy_error_order_invalid_card_triggers_no_supplement_io` — line 661.
- `...::test_standalone_two_public_calls_after_raw_change_second_refuses_exact` — line 697.
- `...::test_standalone_two_public_calls_after_manifest_change_second_refuses_exact` — line 727.
- `...::test_two_healthy_operations_with_changed_source_metadata_yield_new_values` — line 756.
- `...::test_late_raw_drift_after_context_before_public_accept_refuses_exact_and_preserves_inventory` — line 807.
- `...::test_late_task_mutation_after_load_before_accept_refuses_exact` — line 888.
- `...::test_post_validation_package_field_drift_refuses_before_first_write` — line 950.
- `...::test_post_evidence_accept_views_failure_preserves_earlier_absent_later` — line 1028.
- `...::test_historical_readback_never_reads_live_state_and_validates_content` — line 1124.
- `...::test_readback_result_mutation_after_check_before_return_refuses_exact` — line 1327.
- `...::test_low_derived_copy_build_accept_readback_with_supplement_raw_succeeds` — line 1375.
  Uses C/A2 operation helpers; manually constructs a supplemented package + request `source_bindings`; asserts `build_revision_cards_views_from_paths`, `accept_revision_evidence_views_from_paths`, HIGH adopt/readback. Its own docstring says HIGH prepare threads an unsupplemented revision package, so this is not a HIGH producer witness.
- `...::test_low_copy_and_none_refusals_are_exact` — line 1588.
- `...::test_live_views_return_view_mutation_after_check_before_return_refuses_exact` — line 1603.
- `...::test_history_views_content_view_mutation_after_check_before_return_refuses_exact` — line 1662.
- `...::test_runner_epoch_advance_executes_new_finish_callbacks_inside_facade` — line 1732.

### LOW fixtures

- `test_evidence_scaling_v2.py::ScalingFixture` — line 135.
  - `base(dids)` — line 145: real `test_survey_evidence_v2` sandbox, real `core.initialize`, real screening acceptance, `agent.validate_agent_state`.
  - `add_supplement(root, discovery_path, screening_acceptance, dids)` — line 248: real `build_evidence_authority_supplement`.
  - `record_for(task, ...)` — line 284.
- `EvidenceScalingRepairTests._make_evidence_chain` — line 1147; `_make_evidence_views_chain` — line 1170.
  Both call `prepare_evidence_package(..., manifest_path)`, `build_research_card_content`, `accept_evidence_results`, `accept_edition_views`.

## 3. True HIGH prepare/adopt/resume/readback — existing tests and fixtures

All are in `SRC/tests/`.

### A2 operation suite

`test_dm022_prearchitecture_acceptance_v2.py::Dm022A2OperationTests`

- `_chain_root(research_profile, named_obligations=())` — line 163.
  Real helper sandbox, real public screening/evidence/views, real Ledger builder, test-built completeness; returns the accepted chain and initial `state_path`.
- `_materialize_production_discovery_acceptance(chain, discovery_path=None)` — line 258.
  Real Discovery acceptance + real X manifest/intake; DCP binds acceptance, never raw JSONL.
- `_make_evidence_reviewed_state(chain, root_acceptance_path=None, extra_dcp_artifacts=(), extra_dcp_reviews=())` — line 340.
  Builds 3 real checkpoint records + State at `EVIDENCE_REVIEWED`; validates with `agent.validate_agent_state` (line 492 area). It is a test fixture state, not a public Gate transition.
- `_build_request_and_decision(chain, state_abs, revision_id, affected, extra_obligations=())` — line 498; `supplement_manifest: None` at line 615.
- `_prepare_and_decide(...)` — line 629; calls `high.prepare_revision` and writes the external synthetic decision.
- `_write_prior_human_review(chain, state_abs)` — line 89: real typed `REQUEST_CHANGES` record + index, `approval=None`; used only to test refusal.
- `test_weekly_prepare_adopt_resume_readback` — line 665.
- `test_thematic_prepare_adopt_resume_readback` — line 699.
- `test_low_typed_loader_dispatch` — line 718; `test_loader_accepts_str_path_same_as_path` — line 744; `test_loader_wrong_family_str_path` — line 770; `test_low_guard_and_slots` — line 796.
- `test_high_cli_prepare_adopt` — line 809.
- `test_raw_binding_refuses_unbound_claim` — line 829.
- `test_late_final_plant_blocks_and_resume_recovers` — line 854.
- `test_completion_tamper_refuses_and_resume_indeterminate` — line 891.
- `test_absent_slot_regeneration_ready_and_readback` — line 919.
- `test_repeat_correction_preserves_original_anchor_both_routes` — line 946.
- `test_malformed_review_result_refuses` — line 992.
- `test_stale_and_unsupported_inputs_refuse` — line 1007.
- `test_named_obligation_complete_row_passes` — line 1047.
- `test_interrupted_clear_resume_cleared` — line 1067.
- `test_unknown_live_resume_indeterminate` — line 1106.
- `test_prepare_refuses_prior_request_changes_history` — line 1218.
- `test_adopt_refuses_late_human_review` — line 1242.
- `test_arch_gate_readback_after_adopt` — line 1282.

### C direct/derived suite

`test_dm022_c_direct_operation_v2.py::Dm022CDirectOperationTests`

- `_chain_root_real_head(research_profile, extra_records=(), extra_decisions=None, base_obligations=(), include_base_in_effective=True, primary_did="target-source")` — line 84.
  Uses the shared helper sandbox's real committed HEAD, real screening/evidence/views/Ledger and test-built completeness.
- `test_c_direct_weekly_prepare_adopt_readback` — line 231.
- `test_c_thematic_direct_prepare_adopt_readback` — line 255.
- `test_c_derived_weekly_true_r_not_equal_e` — line 304.
- `test_c_negatives_profile_copy_retention_refuse_no_write` — line 441.
- `test_c_binding_ref_mismatch` — line 533.
- `test_c_binding_integrity_drift` — line 615.
- `test_c_report_positive_control_extra_rows_pass` — line 726.

### Full lifecycle / heavy witnesses

`test_dm022_full_lifecycle_v2.py::Dm022FullLifecycleWitnessTests`

- `_copy_publication_support_files(root)` — line 76; imports `weekly_mod.CURRENT_CLOSURE` + `longform_mod.CURRENT_CLOSURE` and copies every member (lines 95-108).
- `_build_request_and_decision(chain, state_abs, revision_id, affected)` — line 380; `supplement_manifest: None` at line 486.
- `_prepare_and_decide(...)` — line 511.
- `test_weekly_dm022_to_selection_stage` — line 851; `test_thematic_dm022_to_selection_stage` — line 855.
- `test_weekly_present_old_seven_slots_retain_clear_regenerate` — line 859.
- `test_repeat_correction_preserves_anchor_and_wrong_role_refuses` — line 4558.
- Renewal/C/U/U witnesses: lines 3149, 3457, 3568, 3650, 3825, 4006, 4286. These are full publication/renewal witnesses, not targeted supplement-carry regressions.

## 4. Weekly genuine DERIVED true R != E

- `test_dm022_c_direct_operation_v2.py::Dm022CDirectOperationTests::test_c_derived_weekly_true_r_not_equal_e` — line 304.
  Root JSONL holds base `target-source` with `O-ROOT-1`; effective set holds only `derived-source` with raw `parent_refs=["target-source"]`; asserts `root_ids == ["target-source"]`, `"derived-source" in eff_ids`, `root_ids != eff_ids`; then HIGH adopt/readback, LOW checker, repeat correction, resolver.
- `test_evidence_scaling_v2.py::EvidenceScalingRepairTests::test_low_derived_copy_build_accept_readback_with_supplement_raw_succeeds` — line 1375.
  Reuses `Dm022CDirectOperationTests._chain_root_real_head` (line 1417) and A2 `_make_evidence_reviewed_state`; asserts true R/E on the retained COPY and request before/after COPY SHA equality; direct LOW supplement build/accept plus HIGH adopt/readback.
- `test_profile_support_upstream_repair_v2.py::DerivedOperationTests::test_23_healthy_derived_many_to_many_named5_to_7_with_selection` — line 1565.
  THEMATIC many-to-many `R-1/R-2` roots, `C-1/C-2` children, real resolver `prepackage_root_effective`/`effective_basis`, named5 -> 7 and actual Selection consumption. Not Weekly.
- `...::test_24_lossy_derived_shared_oid_refuses_new_prewrite_with_full_inventory` — line 1711.
- Supporting unit checks: `DM017UniverseLossTests::test_07` line 696, `test_08` line 704, `test_09` line 716; `DM017OrdinaryInputTests::test_14` line 828, `test_14b` line 927.

## 5. Thematic full obligations

- `Dm022A2OperationTests._chain_root` — line 163: `completeness.obligations` derived from Profile `initial_obligations`; `closure` present only for `THEMATIC` (lines 193-210).
- `Dm022A2OperationTests._build_request_and_decision` — line 498: initial obligations plus `extra_obligations`; Thematic closure object at 595-612.
- `Dm022A2OperationTests::test_thematic_prepare_adopt_resume_readback` — line 699: Thematic HIGH operation positive, but only Profile-initial obligations and a COMPLETE closure; no named obligation or KEEP+DROP row.
- `Dm022A2OperationTests::test_named_obligation_complete_row_passes` — line 1047: named obligation positive on the **WEEKLY** route, not Thematic.
- `test_profile_support_upstream_repair_v2.py::DM017OrdinaryInputTests::test_14_builder_derives_through_real_ledger_and_passes_full_validators` — line 828: real THEMATIC KEEP+DROP chain, named obligation `O-NEW`, full 7-field rows, `validate_completeness`.
- `...::test_14b_named5_to_accepted7_for_weekly_and_retro_with_selection_refs` — line 927: WEEKLY/RETROSPECTIVE named5 -> 7.
- `test_survey_evidence_v2.py::test_thematic_closure_requires_no_open_material_obligations_and_gap_fill` — line 554; `test_weekly_completeness_does_not_require_thematic_closure` — line 625.

Gap: the Thematic HIGH positive does not exercise named obligations, KEEP+DROP declaration accounting, or the full 7-field builder. Those are covered only on the ordinary (non-DM022) path.

## 6. Unaffected semantic preservation, CURRENT proof, digest families

### Unaffected preservation

- Implementation: `survey_research_authority_v2.py::prove_revision_from_paths` — line 3080.
  - affected/unaffected card and ledger comparison: 3331-3409.
  - mechanical digest projections: 3430-3460.
  - result/view digest recompute: 3150-3160.
- Existing test: `Dm022A2OperationTests::test_repeat_correction_preserves_original_anchor_both_routes` — line 946; assertion on `unaffected_comparison.mechanical_projections` at line 968.
- Gap: existing DM022 positives use a single non-DROP DID. No positive has a non-empty `unaffected_dids` set; `test_repeat_correction...` checks the proof's mechanical projection only. A discriminating regression needs at least two non-DROP DIDs (one affected, one unchanged) and must assert unchanged card and ledger semantics plus `unaffected_comparison.rows_checked`.

### Full source proof CURRENT

- `survey_versioned_renewal_source_v2.py::verify_renewal_source_proof(root, basis_path, proof_path)` — line 1533; returns `CURRENT_PROOF_VALID` at line 1913.
- Heavy existing controls:
  - `test_dm022_g71_g76_compatibility_v2.py::test_weekly_g71_to_g76_renewal_control` — line 129; depends on `OLD_ROOT` (old final93 proof copy) and TinyTeX.
  - `test_dm022_publication_depth_boundary_v2.py::test_03_provided30_editorial31_renewal32_33refuses` — line 341; full publication chain.
  - `test_versioned_renewal_source_phase_s.py::TestPhaseSLayerB::test_closure_names_placeholders_drift_refuse_weekly` — line 821; `test_stale_closure_and_u_mismatch_weekly` — line 848; `test_layerb_full_reused_positive_weekly` — line 904.
- These are not targeted supplement-carry tests. They matter only because source-closure bytes changed by the repair invalidate old recorded CURRENT proofs and require fresh source-bound proof.

### Digest families asserted by existing tests

- `test_survey_evidence_v2.py::test_evidence_package_is_exact_and_preserves_task_bytes` — line 365; `result_set_sha256 == accepted.parent.name` at 376.
- `...::test_evidence_result_set_rejects_extra_artifacts_and_detects_accepted_tampering` — line 378.
- `test_evidence_scaling_v2.py::test_two_healthy_operations_with_changed_source_metadata_yield_new_values` — line 756; result-set inequality at 799.
- `test_dm022_prearchitecture_acceptance_v2.py::test_repeat_correction_preserves_original_anchor_both_routes` — line 946; per-file manifest refs 960-966 and `evidence-package.sha256` mechanical projection 968.
- `prove_revision_from_paths` recomputes `result_set_sha256` and `view_set_sha256` (3150-3160) and records these family names in `mechanical` (3439-3459):
  `evidence-package.sha256`, `evidence-acceptance.package_sha256`, `evidence-acceptance.result_set_sha256`, `edition-views-acceptance.view_set_sha256`, `materiality-ledger.basis.evidence_acceptance_sha256`, `materiality-ledger.basis.edition_views_acceptance_sha256`, `materiality-ledger.basis.evidence_set_sha256`, `materiality-ledger.basis.edition_view_set_sha256`, `profile-completeness.basis.materiality_ledger_sha256`.

## 7. Fixture helpers yielding real accepted State / request / decision without public approval

- `test_survey_evidence_v2.py::SurveyEvidenceV2Tests.sandbox` — line 33: real temp repo, real config contract files, independent Git DB with committed fixture source before initialize.
- `...::init_profile` — line 104: real `core.initialize`; returns ISSUE_INITIALIZED State, not EVIDENCE_REVIEWED.
- `...::make_screening` — line 138; `make_evidence` — line 266; `make_views` — line 299: real public producers/acceptors.
- `...::make_chain` — line 348: accepted screening/evidence/views chain, State remains ISSUE_INITIALIZED.
- `test_dm022_prearchitecture_acceptance_v2.py::Dm022A2OperationTests._chain_root` — line 163: accepted artifacts plus real Ledger; returns initial `state_path`.
- `...::_materialize_production_discovery_acceptance` — line 258: real DCP acceptance and X intake.
- `...::_make_evidence_reviewed_state` — line 340: test-built EVIDENCE_REVIEWED State with real checkpoint records/artifacts and real `agent.validate_agent_state`; not a public Human/Architecture Gate transition.
- `...::_build_request_and_decision` — line 498: synthetic `request` plus external `decision`; reviewer is `SYNTHETIC_FIXTURE_*`; no public approval.
- `...::_prepare_and_decide` — line 629: real `high.prepare_revision`, then writes the synthetic decision.
- `...::_write_prior_human_review` — line 89: real typed `REQUEST_CHANGES` record/index, `approval=None`; strict refusal fixture only.
- `test_dm022_c_direct_operation_v2.py::Dm022CDirectOperationTests._chain_root_real_head` — line 84: real accepted chain on real HEAD.
- `test_evidence_scaling_v2.py::ScalingFixture.base` — line 145: real CANDIDATES_NORMALIZED State validated by `agent.validate_agent_state`; `add_supplement` — line 248 uses the real supplement builder.
- `test_profile_support_upstream_repair_v2.py::_sandbox_copy` — line 221; `_init_weekly_through_factory` — line 265; `_init_thematic_through_factory` — line 272; `_init_retro_through_factory` — line 285; `_full_discovery_record` — line 450; `_ensure_x_and_marker` — line 480.

None of these calls a public approval writer. `test_survey_human_gate` approval APIs are not used by the DM022 positives.

## 8. Current `supplement_manifest: None` shape and a discriminating new positive

### Exact current shapes

- `SRC/tests/test_dm022_prearchitecture_acceptance_v2.py`
  - `Dm022A2OperationTests._build_request_and_decision` — line 498; `"supplement_manifest": None` — line 615.
  - Caller `_prepare_and_decide` — line 629.
- `SRC/tests/test_dm022_full_lifecycle_v2.py`
  - `Dm022FullLifecycleWitnessTests._build_request_and_decision` — line 380; `"supplement_manifest": None` — line 486.
  - Caller `_prepare_and_decide` — line 511.
- `SRC/tests/test_evidence_scaling_v2.py:1488` is a comment describing the same limitation; it is not a request shape.

There is no existing DM022 HIGH test with a non-None `supplement_manifest`.

### How a new positive exposes the parent failure rather than a token or patched validator

A discriminating positive should:

1. Build a real fixture with at least two non-DROP DIDs (one affected, one unchanged) and a real supplement manifest/Raw produced by `build_evidence_authority_supplement`.
2. Set `request["supplement_manifest"]` to a schema-valid `SizedRef` and set `source_bindings` on the affected record to the exact `supplement_source_id`.
3. Call real `high.prepare_revision` and inspect `candidate/package.json`, `candidate/tasks/*`, and `candidate/results/*`; then run real `validate_evidence_card`, adopt/readback, and `check_supersession_record_from_paths`.
4. Assert package-level authority, supplement contract registration, task `authority_supplement_source_ids`, actual card source fields, and unchanged-card equality — not just the request/manifest echo.

Failure surfaces to expect before a real carry exists:

- Package-level carry missing: `_resolve_phase_supplement_context` sees no `authority_supplement` and returns empty context; `_merge_supplement_task_sources` sees no task IDs; `_build_card_core` rejects the record's supplement `source_bindings` with `"source_bindings must explicitly select task-bound sources"` (`survey_evidence_v2.py:2243-2247`).
- Package-level carry present but task IDs missing: `_merge_supplement_task_sources` raises `"Evidence Task references unbound supplement source"` (`survey_evidence_v2.py:476-482`).
- Task IDs present but package authority missing: `_resolve_phase_supplement_context` returns empty entries; the same unbound-source failure occurs.
- Token trap: asserting only `revision-manifest.json.candidate_outputs.supplement_manifest` passes today because `survey_prearchitecture_acceptance_v2.py:786` copies the request value. That assertion does not prove package/task/card carry.
- Patched-validator trap: stubbing `_resolve_phase_supplement_context`, `_merge_supplement_task_sources`, `_build_card_core`, `validate_evidence_card`, or `build_revision_package_from_paths` hides the parent failure. The positive must use the real public `prepare_revision` path and real validators.
- Write-window note: `prepare_revision` writes candidate package/tasks before `build_revision_cards_views_from_paths`; a card-build refusal can therefore leave partial inert R files. Prepare does not write State/guard. A new positive should use a fresh revision root and assert the actual R inventory/refusal, not assume zero writes.

## 9. Targeted existing regressions — meaningful subset

Use these for the repair; do not run a whole-suite sweep or count-decoration tests.

### LOW supplement / scaling

- `test_survey_evidence_v2.py::test_evidence_authority_supplement_binds_exact_raw_source_and_card` (666)
- `test_survey_evidence_v2.py::test_evidence_authority_supplement_rejects_drop_unknown_path_sha_and_symlink` (755)
- `test_survey_evidence_v2.py::test_zero_byte_authority_fails_schema_and_independent_runtime_without_output` (855)
- `test_survey_evidence_v2.py::test_evidence_package_is_exact_and_preserves_task_bytes` (365)
- `test_survey_evidence_v2.py::test_evidence_result_set_rejects_extra_artifacts_and_detects_accepted_tampering` (378)
- `test_run_evidence_v2_interactive.py::test_multiple_task_bound_sources_require_explicit_bindings` (163)
- `test_run_evidence_v2_interactive.py::test_single_source_legacy_input_remains_backward_compatible` (172)
- `test_evidence_scaling_v2.py::test_golden_full_card_public_builder_matches_reviewed_baseline_and_validates_clean` (316)
- `test_evidence_scaling_v2.py::test_unit_private_slices_match_public_authority_map` (427)
- `test_evidence_scaling_v2.py::test_standalone_two_public_calls_after_raw_change_second_refuses_exact` (697)
- `test_evidence_scaling_v2.py::test_standalone_two_public_calls_after_manifest_change_second_refuses_exact` (727)
- `test_evidence_scaling_v2.py::test_late_raw_drift_after_context_before_public_accept_refuses_exact_and_preserves_inventory` (807)
- `test_evidence_scaling_v2.py::test_late_task_mutation_after_load_before_accept_refuses_exact` (888)
- `test_evidence_scaling_v2.py::test_post_validation_package_field_drift_refuses_before_first_write` (950)
- `test_evidence_scaling_v2.py::test_historical_readback_never_reads_live_state_and_validates_content` (1124)
- `test_evidence_scaling_v2.py::test_readback_result_mutation_after_check_before_return_refuses_exact` (1327)
- `test_evidence_scaling_v2.py::test_low_derived_copy_build_accept_readback_with_supplement_raw_succeeds` (1375)
- `test_evidence_scaling_v2.py::test_low_copy_and_none_refusals_are_exact` (1588)
- `test_evidence_scaling_v2.py::test_live_views_return_view_mutation_after_check_before_return_refuses_exact` (1603)
- `test_evidence_scaling_v2.py::test_history_views_content_view_mutation_after_check_before_return_refuses_exact` (1662)

### HIGH operation

- `test_dm022_prearchitecture_acceptance_v2.py::test_weekly_prepare_adopt_resume_readback` (665)
- `...::test_thematic_prepare_adopt_resume_readback` (699)
- `...::test_raw_binding_refuses_unbound_claim` (829)
- `...::test_late_final_plant_blocks_and_resume_recovers` (854)
- `...::test_completion_tamper_refuses_and_resume_indeterminate` (891)
- `...::test_absent_slot_regeneration_ready_and_readback` (919)
- `...::test_repeat_correction_preserves_original_anchor_both_routes` (946)
- `...::test_named_obligation_complete_row_passes` (1047)
- `...::test_interrupted_clear_resume_cleared` (1067)
- `...::test_unknown_live_resume_indeterminate` (1106)
- `...::test_prepare_refuses_prior_request_changes_history` (1218)
- `...::test_adopt_refuses_late_human_review` (1242)
- `...::test_arch_gate_readback_after_adopt` (1282)
- `...::test_high_cli_prepare_adopt` (809)
- `test_dm022_c_direct_operation_v2.py::test_c_direct_weekly_prepare_adopt_readback` (231)
- `...::test_c_thematic_direct_prepare_adopt_readback` (255)
- `...::test_c_derived_weekly_true_r_not_equal_e` (304)
- `...::test_c_negatives_profile_copy_retention_refuse_no_write` (441)
- `...::test_c_binding_ref_mismatch` (533)
- `...::test_c_binding_integrity_drift` (615)

### Thematic / obligations

- `test_dm022_prearchitecture_acceptance_v2.py::test_thematic_prepare_adopt_resume_readback` (699)
- `test_dm022_prearchitecture_acceptance_v2.py::test_named_obligation_complete_row_passes` (1047)
- `test_profile_support_upstream_repair_v2.py::test_14_builder_derives_through_real_ledger_and_passes_full_validators` (828)
- `test_profile_support_upstream_repair_v2.py::test_14b_named5_to_accepted7_for_weekly_and_retro_with_selection_refs` (927)
- `test_profile_support_upstream_repair_v2.py::test_23_healthy_derived_many_to_many_named5_to_7_with_selection` (1565)
- `test_profile_support_upstream_repair_v2.py::test_24_lossy_derived_shared_oid_refuses_new_prewrite_with_full_inventory` (1711)
- `test_survey_evidence_v2.py::test_thematic_closure_requires_no_open_material_obligations_and_gap_fill` (554)
- `test_survey_evidence_v2.py::test_weekly_completeness_does_not_require_thematic_closure` (625)

### Excluded as non-targeted / heavy

- `test_dm022_full_lifecycle_v2.py` PDF/TinyTeX/full publication witnesses (851, 859, 936, 1020, 1113, 1586, 1693, 2129, 2457, 2665, 3143, 4006, 4286, 4558): use only if the repair itself changes full publication/renewal behavior. They depend on TinyTeX and complete support trees.
- `test_dm022_g71_g76_compatibility_v2.py::test_weekly_g71_to_g76_renewal_control` (129): depends on `OLD_ROOT` old proof copy and TinyTeX.
- `test_dm022_publication_depth_boundary_v2.py::test_03...` (341) and `test_04...` (690): full publication chain; not supplement-carry regression.
- `test_versioned_renewal_source_phase_s.py` (734/761/788/821/848/904): CURRENT-proof unit witnesses; heavy fixtures, only relevant if source closure changes invalidate old CURRENT proof.

## 10. Actual source closure memberships

### Test files

`SRC/tests/*.py` are not members of any of:

- `config/survey-production-v2.json` `contract_files.pipeline` (6-84),
- `_DM022_7` in Weekly/Longform,
- `_SHARED_PY_G71` / `_SHARED_PY_G76` in staged source,
- `_OLD_PY_30` / `_NEW_DM022_MODULES_2` in renewal history,
- `_contract_and_tools` seven tool pins.

Therefore test-only edits do not change Contract8, HIGH tool pins, or G76 closure. They also do not create source-proof CURRENT obligations. Fixture Git commits are test data, not the shipping source epoch.

### `scripts/survey_research_authority_v2.py` and `scripts/survey_prearchitecture_acceptance_v2.py`

Both are in:

- Weekly `_DM022_7` — `survey_weekly_derivation_v2.py:70-78`; G76 current closure 36 — line 79/81.
- Longform `_DM022_7` — `survey_longform_generated_v2.py:92-100`; G76 current closure 41 — line 101/103.
- Staged `_DM022_PY_2` — `survey_editorial_staged_source_v2.py:92-95`; G76 shared 70 per-route / 73 union — lines 88, 140-143, 173-213.
- Renewal history `_NEW_DM022_MODULES_2` — `survey_versioned_renewal_history_v2.py:374-377`; G76 pipeline 76 — lines 362-377.
- HIGH tool pins — `survey_prearchitecture_acceptance_v2.py:439-447`.

They are not in `contract_files.pipeline`, so script-only edits do not change Contract8. They are not test-closure members.

### Five DM022 schemas

`schemas/dm022-preadoption-report-v2.schema.json`, `dm022-revision-manifest-v2`, `dm022-revision-proof-v2`, `dm022-revision-request-v2`, `dm022-supersession-checkpoint-v2` are in:

- Weekly/longform `_DM022_7` (same lines above).
- Staged `_DM022_SCHEMAS_5` — `survey_editorial_staged_source_v2.py:96-102`.
- Renewal history `_NEW_DM022_SCHEMAS_5` — `survey_versioned_renewal_history_v2.py:367-373`.
- HIGH tool pins — `survey_prearchitecture_acceptance_v2.py:442-446`.
- `config/survey-production-v2.json` `contract_files.pipeline` — lines 79-83. Because `contract_identity` includes `contract_files.pipeline` (`survey_production_v2.py:210-228`), **schema content edits change Contract8**; script-only edits do not.

### `scripts/survey_evidence_v2.py` (LOW supplement validator/producer)

- Staged G76 exact closure row: `_SHARED_PY_G71` at `survey_editorial_staged_source_v2.py:120`; union `_SHARED_PY_G76` line 143 (70 per-route / 73 union).
- Renewal history exact closure row: `_OLD_PY_30` at `survey_versioned_renewal_history_v2.py:318`.
- Weekly control-bound loader, not a G76 closure blob: `survey_weekly_derivation_v2.py:798-805` (`survey_evidence_v2.py` at 802); actual-import allowance only.
- Longform: not in `_control_bound` (`survey_longform_generated_v2.py:578-585`), but all `scripts` are in the control-path diff/ancestry check (`implementation_control_roots`; `survey_longform_generated_v2.py:622-639`).
- Not in HIGH `_contract_and_tools`; not in `contract_files.pipeline`; not a test file.

### Contract8 vs pipeline content tree vs tooling registration

- Contract8: `survey_production_v2.py::contract_identity` — line 210; eight keys at 219-228; `pipeline_files` from `cfg["contract_files"]["pipeline"]` + `DEFAULT_CONFIG` + `PROFILE_SCHEMA` + `STATE_SCHEMA`; quality files and profile objects. Scripts and tests are absent.
- Pipeline file content tree: `config/survey-production-v2.json:6-84`; includes the 5 DM022 schemas at 79-83, no scripts and no tests.
- Tooling registration: HIGH `_contract_and_tools` — `survey_prearchitecture_acceptance_v2.py:437-453`; request copies in A2 `_build_request_and_decision` 503-511 and full lifecycle 391-399; live equality checks 516-522 and 1136-1140. Any change to the seven pinned files makes old request/manifest `tool_shas` stale and is refused; a fresh request must pin the new bytes.
- G76 closure: Weekly 36 (`survey_weekly_derivation_v2.py:70-81`), Longform 41 (`survey_longform_generated_v2.py:92-103`), staged 70/73 (`survey_editorial_staged_source_v2.py:85-102`, 140-143, 173-213), renewal history 76 (`survey_versioned_renewal_history_v2.py:362-377`). Source edits to the seven members change closure bytes; old recorded closure pins/CURRENT proof become stale.

## 11. Gaps and qualifications

- No existing DM022 HIGH test exercises `supplement_manifest` other than `None`.
- No existing DM022 positive has a non-empty unaffected set; `prove_revision_from_paths` enforces equality, but no test proves preservation across a multi-DID supplement correction.
- The Thematic HIGH positive covers only Profile-initial obligations and a COMPLETE closure; full 7-field/named/KEEP+DROP obligations are covered on the ordinary path, not DM022 HIGH.
- `test_low_derived_copy_build_accept_readback_with_supplement_raw_succeeds` is explicitly not a HIGH producer witness: it manually assembles a supplemented package/request and calls the LOW builders; HIGH prepare/adopt in that test sees an unsupplemented revision package.
- The heavy full-lifecycle/G71-G76/depth tests depend on TinyTeX and/or the old proof-copy source. They are not targeted supplement-carry regressions.
- Test-only edits do not alter source closure, Contract8, or tool pins. Source edits to the two DM022 modules or five schemas do.
- No test was executed for this inventory; all statements are source/test-file inspection at the stated final139 proof-copy path.
