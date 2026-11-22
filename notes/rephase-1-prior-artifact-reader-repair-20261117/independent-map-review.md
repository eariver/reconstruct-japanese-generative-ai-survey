# Independent scoped PRE-CODE review — prior-artifact typed reader map

Role: fresh independent scoped reviewer, read-only, not author/root.
No runtime/import/tests/fixtures/Git/network/source-State writes/subagents.
Source-only reads + stdlib hash/JSON only.

## Bound inputs

- Actual readonly source: `.rephase-1-editorial-runtime/selection-scaling-real-20261116T021943Z/candidate-work` (no Git here).
- Identity authority: mandatory closeout FULL §7 corrigendum — true `3231a0c280287411513bba359f4d3d2b6703d591` (d591), parent `ae0dd1ee5b0e7a85c44bdab0e6cd024bf12f0c56`, tree `ff01b73e6012fd4519fdfb3807186753ff330367`. `…f591` is frozen wrong metadata, preserved, never used.
- Map under review:
  - `integration-map.md` SHA256 `f6e273c2520fcabffb258acf85d2e8cbf97a050b1f4054bc3d390ead36e94dd2` / 12826B
  - `integration-map-machine.json` SHA256 `19ab43692b17b5f861b6e1142a14b31e971792ffe7c13988f971568637e10245` / 6956B
  - `README.md` SHA256 `8dd3b376a6c90ae04f8d2f77b9d8e14ad054f2265618597864436c319a87b353` / 2979B
- Prior diagnosis `../rephase-1-selection-architecture-resume-20261117/prior-artifact-compatibility-assessment.md` is starting point only, not approved patch. Its §3 recommendation (`resolve_active_research_four_refs`) is superseded by this map per closeout §7.

## Verdict: GO_SCOPED

Map is approved for root dispatch to bounded implementation. No load-bearing bug. No generic pre-code cycle. Scope is exactly one function `survey_stage_validation_v2._prior_artifacts` + focused new test, existing imports only.

## What was checked source-only

- Defect exact: `_prior_artifacts` 328–423; PREARCH guard 333–337 passes; loop 351–375 line 362 unconditionally `schema_gate.load_and_validate_json(path, repo_root / agent.CHECKPOINT_SCHEMA)` where `agent.CHECKPOINT_SCHEMA = schemas/stage-checkpoint-v2.schema.json` (`survey_agent_control_v2.py:43`). Valid PREARCH (`dm022-supersession-checkpoint-v2.schema.json`, nested operation/boundary, no top-level `from_state`) correctly fails. Called from `validate_stage:880` before `_validate_stage_semantics:884–885`, before report/checkpoint/advance. SP/W34 exit2 walls are time-to-refusal, not 45AG cost. Map §1 correct.
- Chosen reuse exact:
  - `agent._validate_checkpoint_record(repo_root,cfg,state,checkpoint,authority,revalidation=None,pending_basis=None)` 770–805. Defaults are `None`; positional `None,None` equals keyword `revalidation=None, pending_basis=None`. PREARCH branch returns at 805 before legacy superseded logic 826–864 and before producer/review/report logic 815–916, so `None,None` vs passthrough is equivalent for PREARCH; `None,None` is stricter for artifact merge (no `superseded` override). No invented guard requirement. Map §2 correct.
  - Pure content 186–287 (kind/reason, exact operation/producer-boundary, exact 3-checkpoint set, 4 NamedRefs shape+sha, lineage, sole `DM022_SUPERSESSION_PROOF` SizedRef, SizedRefs, no top-level `from_state/to_state`). Core proof 290–321 → `low.check_supersession_record_from_paths(repo_root,checkpoint_path,report_path,before_copy_path)` 4949–4951, FULL graph per docstring 4952–4965, not hash-only. Map §4 correct, no predicate change.
  - `low.load_typed_checkpoint_record` 329–373: kind absent → LEGACY, `DM022_KIND` → PREARCH + strict checks, unknown kind refuses, no fallback. Map correct.
- Rejected LIVE path exact: `resolve_active_research_four_refs` 1389–1462 fans to `_resolve_prearchitecture_artifact` 1073–1146 which calls `validate_agent_state` 1098–1102 (strict LIVE State/history/guard/completion + live re-hash active four + View→Evidence). Correct to avoid in historical/diagnostic prior loop. Map follows closeout §7 (do not blindly copy prior recommendation). Load-bearing correction, approved.
- Repair shape exact:
  - Keeps 333–337, 338–350, `_authority_ref_path` provenance path+sha vs file, LEGACY 362–375 byte-for-byte with `bound_prior/superseded` allowance, Group C active7 376–422 + `_merge_artifacts` 449–455 + `_require_active_candidate_binding` + entry/prepublish READY + report. Verified against 328–423 and 860–907 (`validate_agent_state:863–865`, `_dm022_require_ready:869` entry + `888` prepublish — map cites 887, off-by-one, non-blocking).
  - Family+role BEFORE dedup via `low.load_typed` per row; PREARCH role gate `name not in DM022_PREARCH_CHECKPOINTS → DM022_WRONG_FAMILY` even if `rel` seen; LEGACY unchanged; unknown refuses. This closes the silent-skip alias bug (current 359–361 dedups before role). Load-bearing, correct.
  - Distinct `rel` + PREARCH → `_validate_checkpoint_record(...,None,None)`, merge 4 rows from `fam["record"]["artifacts"]` with live `core.sha256_file` vs `row["sha256"]`, `existing.resolve()!=artifact.resolve()` disagree, no `superseded` override, do not trust caller proof dict, paths from pinned record. `seen.add(rel)`; same-record triplet (shared path) therefore proves once. Correct.
  - Same path AND sha triplet 795–800 + `issue_id` 801–802 preserved. Correct.
  - No `validate_agent_state`/guard/HIGH recursion in `_prior_artifacts` + PREARCH branch; READY stays on mutating `validate_stage` entry/prepublish. Correct. Reused branch docstring 304–305 confirms no State/guard/recursion.
  - Pinned family decides (`_dm022_pinned_family` stage 194–209 / agent 110–128); deprecated `_dm022_state_kind` triplet heuristic never used. Healthy LEGACY same-triplet stays LEGACY. Correct.
- Imports: stage 22,30,36,39 already have `agent,low,_setmod,core,schema_gate`. No new import/module/schema/family/cache/flag/projection/third validator. Correct.

## Closed missing §5 membership (reviewer, source-only)

- `config/survey-production-v2.json`: `contract_files.pipeline` 76 rows (all docs/config/schemas/prompts, no `scripts/`), `quality` 3 rows. `implementation_control_roots` includes `scripts/` for drift, not Contract8.
- `core.contract_identity` 210–228: pipeline hash = pipeline files + `DEFAULT_CONFIG`+`PROFILE_SCHEMA`+`STATE_SCHEMA` only; quality hash = quality files only. Script-only edit does not imply Contract8 by construction; actual recompute + CURRENT proof at execution still required (map correctly claims no outcome).
- `_MAPPED_DM022_CODESET` 587–599: exactly 2 modules +5 schemas. `stage_validation`/`agent_control` not members.
- `PUBLICATION_ROLES_7` (`survey_publication_set_v2.py:124–132`) = 7; `ACTIVE_PUBLICATION_ROLES_7` (agent 54–62) same 7; stage 399 enforces exact 7. Never append runtime/validator.
- G76 closures: `_CANON_WEEKLY_G76` 36 = G71 29 + `_DM022_7`; `_CANON_LONGFORM_G76` 41 = G71 34 + `_DM022_7`. Neither contains `survey_stage_validation_v2.py` nor `survey_agent_control_v2.py`. `_DM022_7` identical 7 in both files. Family 70 per-route / 73 union, pipeline 76, LOW 7 same membership confirmed; changed stage file is control root, not CURRENT closure row. No Contract8 membership change by construction.

## Test plan adequate, no fabrication

- Builders exist: `tests/test_selection_scaling_repair_v2.py:_build_synthetic_prearch_once:207/_build_synthetic_legacy_once:318`; `tests/test_dm022_full_lifecycle_v2.py:Dm022FullLifecycleWitnessTests` with `_chain_root/_materialize_production_discovery_acceptance/_make_evidence_reviewed_state/_prepare_and_decide/_build_selection_input`; `tests/test_survey_stage_validation_v2.py` 3 methods cover only ISSUE/discovery/current-tool/draft, never PREARCH prior — map correctly does not credit them.
- Public route genuine HIGH adopt → `validate_stage` EVIDENCE → CORE report → `advance-stage` to SELECTION_COMPLETE → `validate_stage` architecture → advance to ARCHITECTURE_ESTABLISHED pending Human; Weekly+Thematic sequential, observed-only. Positives (PREARCH PASS exact report keys, no-overwrite rerun, healthy LEGACY stays LEGACY) + negatives (unknown kind, malformed SELF, role-misbound alias after seen, split-sha, drift, collision, wrong four, path drift, missing report, late guard, history-detached vs mutating READY, readback/own-epoch drift, active7 unaffected) cover closeout §7. No fake CORE report, no narrowed checks, no perf demand before observed fail; post-reader cost UNKNOWN preserved.
- Identity: synth DBs may own meaningful child epoch (d591 child preserving State-init 480 + cc1c/ae0 lineage, no repin, perms root-later); real/new author copy MUST inherit actual d591, preserve real State480 history. No `480cc1ae0`-must-equal-synth requirement imposed. Correct.

## Exact scope conditions for implementation (root enforces before code)

1. Edit only `scripts/survey_stage_validation_v2.py::_prior_artifacts`; focused new test only. No new module/schema/family/cache/flag/projection/third validator, no PREARCH→legacy projection, no caller verified-dict, no global cache, no guard in reader.
2. Use `agent._validate_checkpoint_record` PREARCH branch only; do NOT call `resolve_active_research_four_refs`/`_resolve_prearchitecture_artifact`/`validate_agent_state` in `_prior_artifacts`.
3. Role-before-dedup mandatory; `None,None` (prefer keywords `revalidation=None, pending_basis=None`); PREARCH merge ignores `superseded`; LEGACY keeps `superseded` allowance; proof once per distinct `rel`; convert loader `ResearchAuthorityError` fail-closed to `StageValidationError`; join `errs` list on raise.
4. New isolated copies only; preserve d591 ancestry for real path, `48082356` State init + `cc1c/ae0` lineage, 14 outputs/States/materials untouched; no State/Profile repin, no writer rerun, no manual CORE report, no old-runner reuse.
5. Genuine HIGH-adopted EVIDENCE_REVIEWED PREARCH + public `validate_stage→advance` tests as mapped; affected/CURRENT/delivery binding + independent implementation review after; unmeasured semantic cost returns to root before broadening. Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN.

Root dispatch required before code. Ordinary Commit/Push Human-owned.
