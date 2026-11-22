# Prior-artifact typed reader — integration map (MAP-ONLY, no code)

Source actual readonly: `.rephase-1-editorial-runtime/selection-scaling-real-20261116T021943Z/candidate-work`.
Corrigendum authority: true `3231a0c280287411513bba359f4d3d2b6703d591` (d591), parent `ae0dd1ee5b0e7a85c44bdab0e6cd024bf12f0c56`, tree `ff01b73e6012fd4519fdfb3807186753ff330367`.
Prior `…f591` is frozen wrong metadata, preserved, never used for operations. Frozen patch `76ac1318…`/5691014B + manifest `0dc361cb…`/187361B (final143 58M85A/774) remain byte authorities WITH corrigendum. Prior `prior-artifact-compatibility-assessment.md` is starting diagnosis, not approved patch. No Git/imports/runtime/tests/fixtures/network/source-State writes/subagents in this map.

## 1. Defect (exact)

`scripts/survey_stage_validation_v2.py::_prior_artifacts` 328–423.
Lines 333–337 PREARCH same-record guard passes. Loop 351–375 line 362 unconditionally:

```python
record = schema_gate.load_and_validate_json(path, repo_root / agent.CHECKPOINT_SCHEMA, label="prior Stage Checkpoint")
```

`agent.CHECKPOINT_SCHEMA` = `schemas/stage-checkpoint-v2.schema.json` (`survey_agent_control_v2.py:43`, required `from_state/to_state`). Valid PREARCH (`schemas/dm022-supersession-checkpoint-v2.schema.json`, kind `PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1`, nested `operation`/`producer_boundary` from/to, no top-level `from_state`) correctly fails with `'from_state' is a required property`. Called from `validate_stage:880` before `_validate_stage_semantics:884–885`, before report/checkpoint/advance. SP exit2/35.004s, W34 exit2/180.013s are time-to-refusal, not later 45AG cost.

## 2. Chosen reuse (not prior recommendation)

Reuse existing `agent._validate_checkpoint_record(repo_root,cfg,state,checkpoint,authority,revalidation=None,pending_basis=None)` PREARCH branch (`survey_agent_control_v2.py:770–805`) for each PREARCH prior.

Do NOT use `agent.resolve_active_research_four_refs` (1389–1462) here. It fans to `_resolve_prearchitecture_artifact` (1073–1146) which calls `validate_agent_state` (1098–1102) — full strict LIVE State + history/gates/completion + live re-hash of active four + View→Evidence binding. That revalidates current State, resolves only active four (not historical priors), and adds current-State/guard recursion inappropriate for a historical/diagnostic prior loop.

`_validate_checkpoint_record` PREARCH branch does:

- `pubset.sha256_repo_file` provenance SHA drift (`770–776`);
- `low.load_typed_checkpoint_record` (`survey_research_authority_v2.py:329–373`): kind absent → LEGACY via `OLD_CHECKPOINT_SCHEMA`; kind `DM022_KIND` → PREARCH via `DM022_CHECKPOINT_SCHEMA` + reason/operation/boundary/checkpoints/artifacts/SELF checks; unknown kind refuses;
- role gate `checkpoint not in DM022_PREARCH_CHECKPOINTS → DM022_WRONG_FAMILY` (788–789);
- pure `agent._validate_prearchitecture_record_content(record,checkpoint)` (186–287): kind/reason, exact `operation={EVIDENCE_REVIEWED→EVIDENCE_REVIEWED}`, exact `producer_boundary={CANDIDATES_NORMALIZED→EVIDENCE_REVIEWED}`, exact 3-checkpoint set, 4 NamedRefs shape+path+sha, lineage keys, sole `DM022_SUPERSESSION_PROOF` SizedRef shape, SizedRef/ArtifactRef shapes, no `from_state/to_state` top-level;
- same path AND sha triplet (795–800), `issue_id` (801–802);
- record-owned `agent._validate_prearchitecture_core_proof(repo_root,abs_checkpoint,precord)` (290–321) → `low.check_supersession_record_from_paths(repo_root,checkpoint_path,report_path,before_copy_path)` (4949–5077), paths derived from pinned record + `revision_root`, no caller proof dict.
- NO `validate_agent_state`, NO LIVE guard, NO HIGH recursion in this branch (returns at 805, before producer/artifact/review/core-report/history logic 806–916).

## 3. Exact repair shape (one function, existing imports only)

Edit only `survey_stage_validation_v2._prior_artifacts`. Existing imports (`agent,low,_setmod,core,schema_gate`, stage lines 22,30,36,39) already cover it. No new import/module/schema/family/verified-dict/public flag/global cache/third validator.

Keep lines 333–337, 338–350 (`_publication_approval_artifacts`, `resolve_active_publication_revalidation`, `superseded`/`bound_prior`/`seen_checkpoint_paths` decl) unchanged. Keep `_authority_ref_path` per-row provenance path+sha vs file check unchanged.

Per `for name,ref in checkpoint_provenance` (excluding `publication_preview`, skipping `None`):

1. `path=_authority_ref_path(...)`; `rel=_rel(...)`.
2. Family+role BEFORE dedup (load-bearing): `fam=low.load_typed_checkpoint_record(repo_root,path)`; `family=fam["family"]`.
   - `PREARCH`: if `name not in DM022_PREARCH_CHECKPOINTS` → `DM022_WRONG_FAMILY` (invalid PREARCH alias in selection/draft/validation/checkpoint must not skip because `rel` already seen).
   - `LEGACY`: existing legacy path unchanged (historical review/runtime contracts preserved).
   - Unknown kind already refused by loader, never falls back.
3. If `rel in seen_checkpoint_paths`: after step 2 passes, `continue` (role already admitted; proof+merge already done for this distinct record). No new cache/API beyond existing `seen` set.
4. If `rel` distinct and `family==PREARCH`:
   - `errs=agent._validate_checkpoint_record(repo_root,cfg,state,name,ref,None,None)` (pass `None` revalidation/pending so no publication `superseded` override; PREARCH branch ignores them in any case). If `errs` → raise `StageValidationError`.
   - Merge 4 artifacts from `fam["record"]["artifacts"]` with same checks as legacy but NO `superseded` override: `core.repo_local_path` per `row["path"]`, `sha256_file==row["sha256"]` else drift, `existing.resolve()!=artifact.resolve()` → disagree, else `result[row["name"]]=artifact`. Do not trust caller proof dict; paths come from pinned record.
   - `seen.add(rel)`; `continue` (never reach legacy loader line 362).
5. Else `LEGACY`: retain current lines 362–375 byte-for-byte (legacy `load_and_validate_json`, `issue_id`, artifact rehash with `bound_prior/superseded` allowance, disagree, dedup).
6. Keep Group C `VERSIONED_ACTIVE` active7 overlay (376–422) + `_merge_artifacts` (449–455) + `_require_active_candidate_binding` + `_evidence_basis`/`_selection_basis`/`validate_stage` entry/prepublish READY + report construction unchanged.

History vs operational guard: `_prior_artifacts` and the reused PREARCH branch must NOT call `_dm022_require_ready`/`validate_agent_state`/guard. Those stay on mutating path `validate_stage:869` entry + `:887` prepublish (`low.require_research_operation_ready`, full completion when PREARCH).

Capture same record/path+expected sha throughout: `_authority_ref_path` (provenance vs file) → `fam` load of same `path` → `_validate_checkpoint_record` provenance-SHA + triplet path-AND-sha + issue → artifact live re-hash vs `row["sha256"]`. `revision_root/retention/state-before.json`, `report/proof/decision/request/retention` SizedRefs and SELF digest are bound inside the proof.

PREARCH must NOT accept `revalidation.superseded` SHA override; legacy keeps it. LEGACY healthy same-triplet stays on legacy loader (pinned family decides, never triplet heuristic `_dm022_state_kind`).

## 4. Helper semantics quantified (not hash-only)

`_validate_prearchitecture_core_proof→check_supersession_record_from_paths→_verify_adopted_graph_full` enforces FULL graph, not stored-claim equality: checkpoint schema/kind/reason/operation/boundary/checkpoints/artifacts/SELF; report schema (no checkpoint/afterState/guard refs) + proof/decision/request/manifest/before cross-bindings + manifest-bytes bind; retained COPY vs `before_state` sha+byte_count + bound-layout COPY byte equality; sole `DM022_SUPERSESSION_PROOF`; retention 7 rows vs stored manifest snapshots; lineage; 4 artifacts via FULL content validators (evidence/view/ledger basis+row linkage vs discoveries/effective, completeness obligations+closure), own-epoch Contract8 recompute from commit objects + tool_pins + schema fingerprints, `View→Evidence evidence_acceptance_sha256` + SELF digest. Reuse changes no predicate; it only calls the existing branch instead of the wrong legacy schema.

## 5. Caller import / closure membership

Checked read-only: `config/survey-production-v2.json:contract_files.pipeline` (76 rows) + `quality` (3 rows) contain no `scripts/`; `core.contract_identity` pipeline hash = pipeline files + `DEFAULT_CONFIG`+`PROFILE_SCHEMA`+`STATE_SCHEMA` only. `implementation_control_roots` includes `scripts/` for drift detection, not Contract8. DM022 `_MAPPED_DM022_CODESET` is exactly 2 modules +5 schemas (`survey_research_authority_v2.py`, `survey_prearchitecture_acceptance_v2.py` +5 dm022 schemas); `survey_stage_validation_v2.py`/`survey_agent_control_v2.py` are not members. `canonical7/effective7` are exactly 7 publication roles; never append runtime/validator. So script-only `_prior_artifacts` edit does NOT imply Contract8 change by construction, but map claims no Contract8 outcome — actual `core.contract_identity` recompute + fresh CURRENT proof/binding at execution + independent review decide.

## 6. Minimal real public test plan (for root dispatch, no execution now)

New isolated synth DBs at current actual HEAD (meaningful source epoch d591 child preserves State init `48082356` + own `cc1c/ae0` lineage; Git permissions come from root later). No State repin, no writer rerun, no manual CORE report, no old-runner reuse. Use genuine HIGH adopt (`survey_prearchitecture_acceptance_v2.prepare_revision/adopt_revision`) to EVIDENCE_REVIEWED PREARCH + existing 7 writer outputs (`run_selection_architecture_v2_interactive.run` outputs already present in real instance; synth uses same genuine helpers), then public `survey_stage_validation_v2.validate_stage→CORE_STAGE_CONTRACT` report → `survey_agent_control_v2 advance-stage` (build `EVIDENCE_REVIEWED.json` + advance to SELECTION_COMPLETE) → public `validate_stage` (architecture) → advance to ARCHITECTURE_ESTABLISHED pending Human `ARCHITECTURE_REVIEW`. Both Weekly and Thematic routes, sequential, 1200s bound observed-only.

Exact builders (read, not run here): `tests/test_selection_scaling_repair_v2.py::_build_synthetic_prearch_once/_build_synthetic_prearch_with_supplement_once/_build_synthetic_legacy_once` reusing `tests/test_dm022_full_lifecycle_v2.py::Dm022FullLifecycleWitnessTests` (`_chain_root`, `_materialize_production_discovery_acceptance`, `_make_evidence_reviewed_state`, `_prepare_and_decide`, `_build_selection_input`) + full-lifecycle staged controls. Not private `_current_artifacts` projection or `ISSUE_INITIALIZED` only (`tests/test_survey_stage_validation_v2.py` 3 methods cover only ISSUE/discovery/current-tool/draft extras and never reach PREARCH prior).

Positive: synth PREARCH EVIDENCE same-record triplet via public `validate_stage` PASS with exact report keys (`from_state/to_state/production_state/production_profile/implementation_commit_sha/contract/artifacts/recorded_at`), no-overwrite refusal on rerun; healthy LEGACY same-triplet triplet stays LEGACY PASS (no misroute). Negatives (each fail-closed, no report on public path): unknown `kind`; malformed SELF digest; role-misbound PREARCH alias in selection/draft/validation with path already seen (must refuse, not dedup-skip); split-sha triplet; same-record LEGACY positive control; artifact SHA drift; artifact name collision (`_merge_artifacts` replace-refusal); wrong 4 refs; path drift; missing report result; late guard injected between entry and prepublish; history-detached read (no guard required) vs mutating path (READY required); readback byte drift; source own-epoch drift; active7 unaffected (canonical/effective + candidate binding preserved).

Likely source scope: base `scripts/survey_stage_validation_v2.py` + focused new test; no arbitrary path cap imposed by this map.

Post-reader full stage cost UNKNOWN: 35s/180s are refusal walls with same-child `/proc` windows, not whole-tree/disk/net totals; do not extrapolate 180s failure to later 45AG semantics; no new runtime profiling in repair unit.

## 7. Load-bearing gaps (READY for independent, not code)

- Confirm `None,None` revalidation/pending for PREARCH call vs passing through live `revalidation` (PREARCH branch ignores it; artifact merge must still ignore `superseded`).
- Confirm per-row `low.load_typed` + role-before-dedup + proof-once-per-distinct-record preserves pure per-role admission with no new cache exhaustion (seen set only).
- Confirm no historical `validation/freeze/release` PREARCH alias can pass (role gate + `DM022_WRONG_FAMILY` at legacy path).
- No other gap blocks map review. Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN. Stop at Commit Point; ordinary Commit/Push Human-owned.
