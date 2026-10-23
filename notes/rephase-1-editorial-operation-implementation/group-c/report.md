# Group C R1 revision — CHANGES_REQUIRED corrections (no fixture execution, no WORKS claim)

Root R1 `astra-draft-review-r1.md` + independent `independent-draft-lc-review.md` §§3.1-3.8, §5 govern.
Shared root ONLY: `/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60`.
L separately fixing low/agent (syntax/indent errors in `survey_publication_set_v2.py:1467`, `survey_agent_control_v2.py:2321` block imports); H2 correcting H. C did NOT edit L/H files.
Dedicated editor only, no clean/reset/raw delete/network/commit. No code outside C ownership.
Initial draft bytes + 5 shape-tests archived in `history-20261021T012000Z/` before edits (new unique history).

L frozen APIs consumed (no invented maps): `resolve_publication_selection`, `resolve_publication_artifact_path`,
`validate_seal`, `validate_activation_record`, `derive_canonical_anchor`, `before_active_digest`,
`active_candidate_ref`, `require_active_or_canonical`, `assert_canonical_publication_mode`.
Missing `resolve_stage_artifact_path(root,cfg,state,profile,name,template)->Path` (R1 §15, selection §2):
C now calls it via thin adapters (preserving str/Path returns); when absent with pointer present fails
`NEEDS_L` (fail-closed), genuine initial uses exact legacy expansion. No duplicate candidate algorithms remain.

## 1. Owned roots (C ONLY)

- `scripts/survey_stage_validation_v2.py`, `survey_production_v2.py`, `survey_profiled_freeze_v2.py`
- `config/survey-production-v2.json` (ONLY 5 new schemas, 62→67, no scripts/self)
- `scripts/survey_orchestrator_v2.py`, `survey_handoff_v2.py`, `survey_human_gate_v2.py`
- `.github/workflows/survey-production-v2-export-publication-preview.yml`, `build-weekly-survey.yml`, `build-special-pdf.yml`
- `scripts/survey_editorial_correction_proposal_v2.py` (P1), `survey_editorial_current_authority_v2.py` (P2V),
  `survey_editorial_retention_v2.py` (P2R doc guard), `survey_editorial_staged_source_v2.py` (P3S50)
- `scripts/survey_weekly_mechanical_refresh_v2.py` (R1), `run_semantic_publication_v2_interactive.py`+base,
  `survey_semantic_quality_v2.py`
- Own test ONLY: `tests/test_group_c_editorial_consumers_v2.py` (rewritten behavioral, no fixtures)

NOT edited: `survey_publication_set_v2.py`, `survey_agent_control_v2.py`, Reader/Gate/Weeklydrv/Longformdrv/
generated/new schemas (L/H own). L/H concurrent drafts in shared copy are not claimed.

## 2. Fail-open removed (highest blocker §3.1, §3.8, §5)

All `except Exception: return base/None/canonical` + `except ImportError: return` + `catch ImportError fallback`
removed. Only genuine no-pointer canonical initial may use default (returns None → caller canonical default
or exact legacy expansion). Unknown/missing/invalid revalidation/selection fails closed at public call
(`NEEDS_L`/`SELECTION_INVALID`/propagated L error, never old canonical fallback). Legacy valid pointer derives
legacy selection via L. Recompute all 15 active refs typed via L, no trusting failed load.
Wrappers/R1/quality entry refusals use L `assert_canonical_publication_mode`/`require_active_or_canonical`
(no swallow); raw-first ancestor lstat walks (no resolve-then-check laundering).

- Stage `_require_selection` / production `_require_selection`+`_l_stage_path` / freeze `_resolve_freeze_candidate`
  (now needs profile for stage resolver) / orchestrator `resolve_configured_artifact_path(root,cfg,state,profile,name,template)`
  / handoff `resolve_handoff_artifact_path(...,name,template)` / gate `resolve_gate_path(...,name,template)`:
  all required signatures (no optional repoRoot skip), all propagate L errors.
- P1 `_versioned_active_selection` + `_require_selection_strict`: strict, no swallow.
- P2V `_require_selection_strict`: strict; `_is_versioned_active_state` swallow removed.
- R1 `_require_canonical_mode_for_r1` via `require_active_or_canonical`; quality/wrappers via
  `assert_canonical_publication_mode`; all at entry before delete/report/guard, no swallowed pointer errors.
- Import guards catch `Exception` (L SyntaxError pending) but fail-closed on pointer (`NEEDS_L`), genuine
  initial allowed. This avoids masking L defect while allowing canonical-initial cheap checks.

## 3. Stage active7 overlay (§§2.4, 3.3)

`_prior_artifacts` MUST overlay active7 after validating canonical anchor/historical original rows:
delegates L selection `canonical7` (not mapped old checkpoint SHA after R1), cross-checks historical rows vs
`canonical7` (exact 4-key rows), validates seal (propagated, no swallow), requires `effective7` exactly 7
publication roles, recomputes each active path via `resolve_publication_artifact_path` + byte check, overlays
`result` 7 paths. Revised originals retain old hash (historical), not old byte-only pass. Downstream candidate
must match active exactly (`_require_active_candidate_binding`); VERSIONED_ACTIVE without set_ref refuses;
active candidate unresolvable refuses. Raw historical inspection remains separately available.

## 4. Production/freeze/orchestrator/handoff/gate (single L stage resolver)

Remove duplicate candidate algorithms; thin adapters preserving return types (str for orchestrator/handoff/gate,
Path for production/freeze/stage) delegate central decisions to L. All callsites updated to required
`(root,cfg,state,profile,name,template)`; no missing repoRoot optional fallback. Config token explicit or
State-aware rolename table okay but shared resolver decisions central in L. Fixed DRAFT templates unchanged.

## 5. P1 versioned/generator_route/KEEP ( §3.5)

- Shape: L `effective7` rows are `{path,sha256,byte_count,origin}` (4 keys). Normalize known explicit keys,
  no expecting 3 causing TypeError. Exact7; Candidate outside 7 per contract (no `effective["publication-candidate"]`).
- Active receipt new kind actual `generator_route` (`WEEKLY_GENERATED_V2`/`LONGFORM_GENERATED_V1`), not old
  `LONGFORM_SPECIAL`/`WEEKLY_MAGAZINE` fakes. `_derive_route_for_generator` maps to derivation loader;
  `_dispatch_generated_receipt` dispatches H `validate_editorial_receipt` and checks returned `generator_route`
  + `validation-checkpoint` accepted context. Old Weekly/Longform dispatch retained for old receipts.
- Before-graph versioned KEEP all prior immutable + State COPY, original canonical false fallback removed.
  When VERSIONED_ACTIVE, discard ALL effective7 from mutable (KEEP prior immutable versioned), discard versioned
  Candidate + seal, ensure State COPY. Bound Candidate always active versioned (strict normalized repo-relative,
  no absolute-vs-relative bug), no canonical copy. Canonical initial uses canonical path + COPY.
- P1/P2V true repeated before-graph (not cosmetic): versioned KEEP + active candidate binding + H accepted context
  + final recheck below constitute repeat, not comment.

## 6. P2V receipt_kind removed (§3.6)

`observe_current_authority(..., receipt_kind=None)` removed entirely. Derives actual kind from
State/proposal/pinned receipt: strict L selection (fail-closed on pointer); if VERSIONED_ACTIVE requires
proposal basis `active_revalidation_ref` == State pointer (true repeat), else `P2V_AFTER_ACTIVATION_REFUSED`
(ordinary receipt after activation refused). No `None` bypass, no caller policy enum, no
`_is_versioned_active_state→False` swallow. P2V adapted current-before covers new review receipt.

## 7. Final recheck (no ordinary after activation)

`_final_full_receipt_recheck` peeks actual kind: editorial → H validator (generator_route check);
old → ordinary validator BUT refuses `RECEIPT_AFTER_ACTIVATION` when State pointer present and L selection is
VERSIONED_ACTIVE (propagates selection errors, no fallback). Satisfies “no ordinary validate after capture;
P2V receipt replay never after activation; second pre-Preview resolves active-set before-graph”.

## 8. Export (§3.4)

Fixed absolute-vs-relative equality bug via strict `_norm` (repo-relative posix, refuses absolute/`..`/backslash).
Chooses State-bound candidate for revision from sourceRoot issue lookup (strict normalized path):
discovers `sources/*/production-state.json` + `sources/**/…` + `specials/**/…` (expected actual rootPattern
initial source path, not guess `sources/*` only), matches `issue_id`, refuses ambiguous State paths (len!=1).
Manual+PR same identity check (both normalized, both State-bound; initial canonical allowed via selection default;
inert revision never exported — `publication-set.json` alone or without activation refuses). No swallowed
selection errors (propagate; `except …: pass/continue` removed).

## 9. Wrappers/builds (§3.8)

Canonical wrappers/refusals at entry before delete/report/guard creation; no swallowed pointer errors.
Interactive `_raw_safe_owned` raw-first lstat walks; R1/quality/base use L strict guards. Build workflows add
“Refuse revised-mode canonical build” steps (State-aware via L, fail-closed).

## 10. P3S50 + recipe (§3.7)

P3S50 REQUIRED (root selection overrides frozen37 legacy spec; reviewer frozen37 does not block new closure).
`_SHARED_PY`30 (old27+low/high/current-authority), `_SHARED_SCHEMAS`14 (old5+new5+Reader/reval/QA/Candidate4),
route3+staged1+style1+recipe1=50 asserted + edge audit (top-level AST + function-local P2V dynamic + file-pin-only
schemas/style/recipe/semantic producers; extra import requires `CODE_DEPS_EXPANSION_REQUIRED`, never silent omit).
`.latexmkrc` runtime binding: file-pin-only via `session.safe_read`+`dep_pins` (legitimate, not Python runtime;
`_check_runtime_binding` skips non-py explicitly documented). Current_closure22/27 (H owns) unchanged (not based
on stale map-resolution new12). Config ONLY 5 schemas, no scripts/self.

## 11. Behavioral tests (no fixtures, actual outcomes, no fabricated pass)

`tests/test_group_c_editorial_consumers_v2.py` rewritten (no large fixtures until combined freeze):
- `test_config_registry_exact` PASS (67, ONLY 5, no scripts/self)
- `test_p3s50_and_recipe_binding` PASS (30/14, recipe legitimate)
- `test_resolvers_use_single_stage_api` PASS (all use `resolve_stage_artifact_path`, no `except-return-base`)
- `test_orchestrator_signature_strict` PASS (required state/repo_root/cfg)
- `test_export_no_absolute_relative_bug` PASS (`_norm`, no old bug, no swallow, ambiguous/inert guards)
- `test_wrappers_entry_refusal_no_swallow` PASS (L strict guards, no swallow)
- `test_stage_fail_closed_on_pointer` FAIL (blocked by L `survey_agent_control_v2.py:2321` IndentationError via stage→agent import — actual L defect, separately fixing; C fail-closed logic present but un-runnable until L lands)
- `test_stage_genuine_initial_allowed` FAIL (same L blocker)
- `test_handoff_gate_signatures_strict` FAIL (same L blocker via handoff/handlers→… and gate→agent imports)

No WORKS/proves-repeat claim: previous 5 shape-presence PASS withdrawn per R1 §20 + independent §7.
Normal Preview/Freeze/Release in both modes, second pre-Preview, R1×2→anchor, active-vs-historical, §9 negatives
require combined freeze + targeted real execution (not run here).

## 12. Work status + needs

- C draft R1 complete for owned paths; L `resolve_stage_artifact_path` absent → C thin adapters raise `NEEDS_L`
  when pointer present (fail-closed, correct interim). Needs L to add frozen API with
  `(root,cfg,state,profile,name,template)->Path` semantics (DRAFT unchanged, candidate via selection, recompute+compare).
- Needs H `validate_editorial_receipt` generator_route/accepted context confirmation (H2 correcting; C dispatches, no parallel validator).
- Needs L agent `_validate_stage_artifacts` seven-role projection + `_resolve_checkpoint_artifact` revalidation mapping + chain/head fixes (§§2.1-2.4); C stage overlay depends on L anchor/canonical7 correctness.
- L syntax/indent blockers (`survey_publication_set_v2.py:1467`, `survey_agent_control_v2.py:2321`) prevent
  stage/P1/P2V/handoff/gate import-based behavioral proof; C modules compile (`py_compile` PASS for all C files),
  but full import proof awaits L fix. No code outside ownership touched to work around.
- No combined long-fixture execution (awaiting lead integration + root review). Reports WORKS only after run.
