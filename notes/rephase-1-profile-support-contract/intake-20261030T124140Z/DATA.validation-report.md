# Validation report — frozen-Core compatibility execution

Status: `WORKAROUND_VALIDATED` (edition-local; CV2-DM-016 remains `OPEN_CORE`).

## 1. Frozen validators executed (all PASS, unmodified code)

- `evidence.validate_evidence_package_basis` over derived compat package: PASS
  (during `build_compat_evidence_package.py`).
- `COMPATIBILITY_REPRODUCIBILITY: PASS` (two clean-temp builds byte-identical;
  package SHA `60860c88de9f9ab5bc8adecdd9b9ed1c2c689c4c1ac5f8a997f85a7a6a474790`).
- `evidence.validate_evidence_package_basis` re-run inside chain driver: PASS.
- `validate_interactive_input` (frozen runner module): PASS (160 records,
  11 supplement bindings task-bound verified).
- `evidence.validate_evidence_card` × 160: PASS.
- `evidence.accept_evidence_results` + `validate_evidence_acceptance`: PASS
  → `evidence/v2/accepted/dba89409c1cdcfb6a8b319ef35e0e1ee1b5ffdc74cad4715dbe44e10345e5603/evidence-accepted.json`
  (result_count 160; PARTIAL 148 / VERIFIED 12).
- `evidence.validate_edition_view` × 160 + `accept_edition_views` +
  `validate_edition_views_acceptance`: PASS →
  `evidence/v2/views/accepted/2bf475f518d80c8088dff7a67a0bc5cae5e2fa5c9a309d56695e66b1d54d7762/edition-views-accepted.json`
  (160 views).
- `evidence.build_materiality_ledger` + `validate_materiality_ledger` (inside
  stage validation): PASS → `materiality-ledger-v2.json` (165 rows;
  downstream MATERIAL 137 / CONTEXT 23 / EXCLUDED 5).
- `schema_gate.validate_instance` (Profile Completeness schema): PASS.
- `completeness.validate_profile_completeness`: PASS →
  `profile-completeness-v2.json` (overall LIMITED; 15 obligations:
  3 SATISFIED / 12 LIMITATION, incl. edition-authored O13/O14/O15 rows with
  Profile-declared dimensions).
- `stage_validation.validate_stage` (CANDIDATES_NORMALIZED): PASS →
  `execution/evidence-stage-advance/validation/evidence-stage-validation-r1.json`.
- `agent.build_stage_checkpoint` + `advance_with_checkpoint`: PASS →
  `orchestration/v2/checkpoints/CANDIDATES_NORMALIZED.json`
  (SHA `b69d2a0b4936c5122bd9a6f63b4186f46c5baee4f8f3156b8a01b2ac5a287038`);
  lifecycle `CANDIDATES_NORMALIZED` → `EVIDENCE_REVIEWED`;
  State SHA `e5f1875fbe9352d0bc33c85f62fef220d39ec66b84a683376c3962bd2832792c`.
- `agent.validate_agent_state` before and after: clean.

## 2. Compatibility accounts

- Tasks: 160 (one per non-DROP Discovery). Projected 67 / passthrough 93
  (matches brief expectation; recomputed, not forced).
- Per-type projected counts: PRIMARY_DOC 13, PRIMARY_REPO 21,
  PRIMARY_ANNOUNCEMENT 8, PRIMARY_MODEL_CARD 6, PRIMARY_SPEC 4,
  SECONDARY_REFERENCE 8, SECONDARY_TECHNICAL 4, RUNTIME_RECIPE 1,
  PACKAGING_DOCS 1, RUNTIME_PR 1.
- §7 invariant held for all 160 tasks (only `source_records[*].source_type`
  differs; verified field-by-field; any other drift would have raised
  `COMPATIBILITY_PROJECTION_INVALID`).
- Supplement: `external/evidence-supplement/evidence-authority-supplement-r1.json`
  (SHA `62031208a5614bc6c75bceaaaa7e421d2fc3329eeeef69474649cc2a97a0f839`;
  13 sources / 1,275,978 Raw bytes), built + validated by frozen
  `build_evidence_authority_supplement`.
- Interactive input r2: `execution/evidence-interactive-input-r2/interactive-evidence-r2.json`
  (SHA `5f8395d03e51586bfc54821bb50b4fca4f5d51fb588295aa9d63e235bf71c841`;
  160 records; 11 supplement-bound). Prior r1 input preserved untouched.

## 3. Frozen-Core identity audit (end of execution)

- `git status` shows no modification under `scripts/`, `schemas/`,
  `config/`, `.github/workflows/` (verified at report time; see session).
- No runtime monkey-patching by edition tooling: Core modules imported
  read-only; the only rebinding executed is frozen Core's own
  `current_stage_basis_override` context, entered at the same call sites as
  the frozen runner for its designed historical-basis purpose.
- No Core source copied under the execution tree (adapter files are new
  edition tooling importing frozen modules; verified by filename audit).
- No canonical Discovery rewrite (Discovery SHA `7074cef2…` unchanged; wrong
  locators preserved; corrections cite the supplement).
- No Screening disposition change (acceptance SHA `65330476…` unchanged).
- Current main (`e69187f7…`, PR #518) contributes only the CV2-DM-016
  documentation entry (`docs/core-v2-deferred-maintenance-summary.md`);
  runtime Core untouched by the merge (empty diff on implementation roots).
- CV2-DM-016 disposition: `OPEN_CORE / EDITION_WORKAROUND`. This report
  states `WORKAROUND_VALIDATED`, never `CORE_FIXED`.
