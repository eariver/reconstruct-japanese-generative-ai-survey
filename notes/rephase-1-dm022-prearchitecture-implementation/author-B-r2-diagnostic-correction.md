# Owner-B R2 diagnostic correction — test_10 oracle + full positive coverage plan

2026-10-28. Corrects `integration-r2-diagnostics.md` §6 B-01 on the fixed R2
source (`snapshot-r2-20261028T124706Z`, manifest `53fde56…`, 756 files).
Raw own failure read: `evidence/integration-r2-20261028T125129Z/run-02-B-ordinary-consumers/stdout-stderr-raw.txt`
(`e17c8e66…`, 30 lines): 11/12 B pass; `test_10` FAIL because the oracle
expected the brittle string `"must not carry CORE_STAGE_CONTRACT"` while the
runtime correctly raised the strict sole-proof error
`"PREARCH record requires exactly one DM022_SUPERSESSION_PROOF review"`.
No source edits to green snapshots/exec/candidate beyond B-owned paths below;
no ordinary commit/push, no Human readback, no network/cleanup, no live
candidate execution while A3/C1/C2 edit (static AST on own files only).
No completion claimed without execution.

## 1. B-owned changes (only)

- `tests/test_dm022_prearch_b_ordinary_consumers_v2.py`
  - `test_10`: oracle now asserts the real required wrong-review refusal
    without a brittle string: `assertRaises(AgentControlError)` + `assertIn
    ("DM022_SUPERSESSION_PROOF", ...)` for the mixed CORE+PREARCH case, plus
    no-authority/no-writes checks (file set before/after identical for both
    the sole-proof pass and the mixed refusal). Runtime untouched (no
    weakening): `_validate_core_stage_report` strict sole branch stays
    (`len != 1` → sole-proof error; mixed `CORE_STAGE_CONTRACT` presence →
    separate must-not-carry error, unreachable when 2 reviews). The 11 other
    positives are retained unchanged.
  - Added `test_13_full_prearch_state_validates_and_resolves_four`,
    `test_14_later_selection_architecture_forward_uses_r4`,
    `test_15_guard_held_diagnosed_writers_refuse_no_recursion` (see §3).
    They import only A2 real chain helpers (`test_survey_evidence_v2`
    `make_chain`/`sandbox`/`init_profile`/`make_screening`/`make_evidence`/
    `make_views` + `low`/`high` + `fix`), never minimal invalid CP, mock LOW
    proof, or self-raised errors. They run in the integrated snapshot later;
    not executed here.

No `scripts/` runtime change was needed for B-01 (runtime was already
strict). All 12 B scripts + drafting/architecture pure wiring from the R1
correction are unchanged except where noted in §4 audit.

## 2. What the R2 raw actually proves (B scope)

- B strict paths 11/11 positives retained: discriminator `reason` (not
  `reason_class`), exact `{from_state,to_state}` operation/boundary, full
  schema-shaped content branch, wrong-family for validation/freeze/release/
  selection, forward-field/lineage, triplet same/split, 7-slot exact + audit
  preflight zero-writes, legacy discriminators, drafting R4 missing-refuse.
- `test_10` mixed refusal is valid strict behavior: 2 reviews (1 PREARCH + 1
  CORE) cannot satisfy “exactly one DM022_SUPERSESSION_PROOF”; the first
  sole-proof gate correctly refuses before the must-not-carry gate. The old
  oracle pinned the wrong one of two valid strict messages. The corrected
  oracle pins the required property (wrong-review refusal + no new authority
  file + no byte writes), not the string.

## 3. Remaining required positive coverage (new tests, run later)

`test_13`: real HIGH adopt → `agent.validate_agent_state` returns `[]` on
the full PREARCH State + `agent.resolve_active_research_four_refs` and
`low.resolve_research_authority` return PREARCH with `artifact_refs` = 4
NamedRefs (paths reloadable). Uses A2 `_chain_root(WEEKLY)` +
`_make_evidence_reviewed_state` + `_prepare_and_decide(rev-b13)` +
`high.adopt_revision` (real guard/State/slot/completion IO, independent Git
DB, synthetic provenance). No mock proof, no self-raise: failures are real
code refusals.

`test_14`: later Selection/Architecture forward uses R4. After the same real
adoption, B strict validation still passes (forward history truthful, no
EVIDENCE_REVIEWED window reimposed, no live-before equality), four-ref
readback survives, and `materiality-ledger`/`profile-completeness` R4 paths
exist for the normal Selection runner. Proves readback survives forward
progress, not just the adoption instant.

`test_15`: guard-held separation with no recursion. After real adoption,
detached `low.check_supersession_record_from_paths(root, cp, report, copy)`
passes with guard absent, then a synthetic held guard is planted:
writers (`sel_runner._dm022_require_ready`) refuse with
`DM022_TRANSITION_ACTIVE`, while detached proof still passes (no operational
READY inside LOW, no call into `validate_agent_state`) and B State validation
stays diagnostic (no guard error smuggled as State error, no new writes).
Proves LOW detached proof ≠ operational READY and writers fail closed.

A3 replaces weak full validation but keeps the API unchanged
(`check_supersession_record_from_paths(root, checkpoint_path, report_path,
before_copy_path)`, `load_typed_checkpoint_record -> {family, record}`,
`resolve_research_authority -> {family, checkpoint, artifacts(parsed),
lineage, artifact_refs}`); these tests bind only that API plus real file
bytes, so they survive A3.

## 4. B diagnostics vs writers audit (no recursion in B)

Checked all 12 B scripts statically (no execution): every diagnostic
(`validate_agent_state`, `_validate_checkpoint_record`,
`_resolve_checkpoint_artifact`, `resolve_active_evidence_views`,
`resolve_active_research_four_refs`, `_resolve_prearchitecture_artifact`,
`_evidence_basis`, `_selection_basis`, `_prior_artifacts`,
`_current_artifacts`, `_load_drafting_basis`, `derive_candidate_matrix`,
`validate_self_contained`, `_current_pending_gate`) performs file/path/schema/
content checks with no `low.require_research_operation_ready` /
`low.require_no_active_guard` call. Every normal writer
(`run` in selection/evidence/drafting runners, `validate_stage`,
`execute_action`, `_advance_stage`, `record_*/invalidate/request_changes`,
`build_stage_checkpoint`, `advance_with_checkpoint`, `approve_architecture`)
does READY entry + prepublish. No B diagnostic inserts writer readiness; no
`agent.validate_agent_state` recursion via LOW (LOW never calls agent/HIGH/
`verify_state_basis`). Runtime State validator diagnoses guard-held only via
writer READY at producer entry, never inside detached proof.

## 5. Precise cross-owner request (C2, B does not edit)

- File: `scripts/survey_reader_surface_gate_v2.py`,
  function `validate_reader_surface_gate(repo_root, path, ..., state_path, ...)`.
  When `state_path is not None` it calls
  `_dm022_require_ready_profile_bound` (writer READY) inside a diagnostic
  validator that performs no writes. B calls it diagnostically from
  `survey_stage_validation_v2._validate_stage_semantics`
  (DRAFT_COMPLETE/VALIDATED_DRAFT) with `state_path`, so guard-held detached/
  historical replay would incorrectly refuse. `evaluate_reader_surface_gate`
  already shows the correct split (READY only when `output_path is not None`,
  i.e. writing; diagnostic with `output_path=None` has no READY).
- Request: C2 splits `validate_reader_surface_gate` the same way —
  diagnostic replay (retained lineage, live re-hash, no guard check, no READY)
  vs mutating producer entry (READY entry + prepublish with explicit
  canonical STATE derived via source_root/config, no guard-skip, no generic
  dict). Keep `validate_manuscript_surface` and
  `survey_reader_publication_v2._validate_renewal_manuscript_binding` as
  pure diagnostics (they already are); keep READY only in
  `build_manuscript_manifest`/`build_review_record`/`evaluate_*` with
  `output_path`. No B file depends on the current validate-with-READY
  behavior except via the documented producer-READY at `validate_stage`
  entry, which stays.
- Related C2 surface (no change requested now, for awareness):
  `survey_execution_record_v2.validate`/`_load_state` correctly have no
  READY (diagnostic); READY lives only in `initialize` entry + prepublish.
  `survey_reader_publication_v2` correctly has READY only in build paths.

## 6. Execution status (honest)

- Static `ast.parse` passes for all 12 B scripts + rewritten B test (13/13).
  No `pytest`/`unittest` executed here (would touch live `candidate-work`
  while A3/C1/C2 edit). Existing R2 11/11 B positives retained by
  construction; corrected `test_10` + new `test_13/14/15` run in the next
  frozen integrated snapshot with real A2→A3 chain, independent Git DBs,
  raw logs/exit codes, and independent review. No whole-acceptance,
  Profile/quality/audit/adoption/savings claim.

Author: Owner B. Scope is B-owned test + audit only; runtime B scripts
unchanged in this turn except as needed to keep the corrected oracle honest
(none needed beyond the R1 correction).
