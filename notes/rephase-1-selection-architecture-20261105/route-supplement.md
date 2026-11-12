# Selection / Architecture follow-up: exact stage order and preflight

Read-only source follow-up on the e84 candidate-work tree. No execution,
imports, tests, network, Git, Production writes, or approval.

`CW` = `.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work`.

## 1. Exact order: ArchitectureEstablished is pre-approval

The normal order is:

```text
EVIDENCE_REVIEWED
  writer -> matrix + selection + PROPOSED architecture (State unchanged)
  stage validation -> EVIDENCE_REVIEWED report
  advance-stage -> SELECTION_COMPLETE
  stage validation -> SELECTION_COMPLETE report (architecture/review/attention)
  advance-stage -> ARCHITECTURE_ESTABLISHED
                   next_action = ARCHITECTURE_REVIEW
                   terminal_reason = HUMAN_GATE_REACHED
  STOP
  Human commit/push exact Gate surface + Human decision
  record-architecture-approval -> human_gates.architecture_review = approved
  then drafting
```

So yes:

- The writer can produce the PROPOSED Architecture while State is still
  `EVIDENCE_REVIEWED`.
- Candidate Selection is internal (`status = ESTABLISHED`); there is no Human
  Selection Gate in this v2 path. The Selection transition to
  `SELECTION_COMPLETE` happens before the Architecture transition.
- `ARCHITECTURE_ESTABLISHED` is reachable without Human approval. It is the
  pre-approval state, not an approved state.
- The Human Architecture Gate is reached **after** the
  `SELECTION_COMPLETE -> ARCHITECTURE_ESTABLISHED` transition, and the State is
  terminal at that pending gate.
- Approval is required only to leave `ARCHITECTURE_ESTABLISHED` and begin
  Drafting.

Normal command boundary, with no approval command:

```text
# 1. while EVIDENCE_REVIEWED, current artifacts = Matrix + Selection
survey_stage_validation_v2.py --state ... \
  --artifact candidate-matrix=... --artifact candidate-selection=... \
  --output .../stage-validation/EVIDENCE_REVIEWED-report.json
# 2. write reviews JSON with CORE_STAGE_CONTRACT result_path -> report
survey_agent_control_v2.py advance-stage --state ... \
  --artifact candidate-matrix=... --artifact candidate-selection=... \
  --reviews .../stage-reviews/EVIDENCE_REVIEWED-reviews.json \
  --summary "..."
# -> SELECTION_COMPLETE

# 3. while SELECTION_COMPLETE, current artifacts = Architecture + Summary + Attention
survey_stage_validation_v2.py --state ... \
  --artifact issue-architecture=... --artifact architecture-review-summary=... \
  --artifact architecture-review-attention=... \
  --output .../stage-validation/SELECTION_COMPLETE-report.json
# 4. write reviews JSON with CORE_STAGE_CONTRACT result_path -> report
survey_agent_control_v2.py advance-stage --state ... \
  --artifact issue-architecture=... --artifact architecture-review-summary=... \
  --artifact architecture-review-attention=... \
  --reviews .../stage-reviews/SELECTION_COMPLETE-reviews.json \
  --summary "..."
# -> ARCHITECTURE_ESTABLISHED, pending ARCHITECTURE_REVIEW, terminal HUMAN_GATE_REACHED

# 5. STOP. Do not call record-architecture-approval here.
```

The full-lifecycle fixture executes the same order: selection advance at
`tests/test_dm022_full_lifecycle_v2.py:827-841`, architecture advance at
`:949-965`, then approval at `:967-973`.

`advance-stage` refuses while `terminal_reason` is set
(`CW/scripts/survey_agent_control_v2.py:2246-2247`); stage validation refuses a
state waiting at the Human Gate
(`CW/scripts/survey_stage_validation_v2.py:870-873`). The next action is the
Human Gate presentation/commit step, not an agent continuation.

There is **no `human_gate_after` field** in the config or Stage Checkpoint
schema. The actual mechanism is:

- `orchestration.gate_at_state.ARCHITECTURE_ESTABLISHED = "ARCHITECTURE_REVIEW"`
  (`CW/config/survey-production-v2.json:228-236`);
- `derive_control_fields` returns the Gate when the current lifecycle is
  `ARCHITECTURE_ESTABLISHED` and the Gate is pending
  (`CW/scripts/survey_production_v2.py:550-567`);
- the Stage Checkpoint schema has `additionalProperties: false` and no
  `human_gate_after` field (`CW/schemas/stage-checkpoint-v2.schema.json:6`,
  and the `from_state`-conditional artifact blocks at lines 209-223).

## 2. Stage artifact validation is not, by itself, an exact-set gate

`_validate_stage_artifacts` (`CW/scripts/survey_agent_control_v2.py:2146-2179`):

- rejects duplicate names;
- for each configured `stage_plan` artifact, requires the named row; resolves
  the canonical path and requires exact path equality (`2146-2179`);
- does **not** reject extra named artifacts.

The Stage Checkpoint schema likewise uses `contains` for the selection and
architecture artifacts
(`CW/schemas/stage-checkpoint-v2.schema.json:209-223`), not exact-set equality.
So a lower-level manually built checkpoint is not by itself an exact-set
barrier.

The normal path is still exact because:

- `validate_stage` builds `current` through `_current_artifacts`
  (`CW/scripts/survey_stage_validation_v2.py:428-460, 852-906`). At
  `EVIDENCE_REVIEWED` the exact current set is
  `{candidate-matrix, candidate-selection}`; at `SELECTION_COMPLETE` it is
  `{issue-architecture, architecture-review-summary,
  architecture-review-attention}` (`151-168`). Extra current artifacts refuse.
- Prior artifacts come only from the State-bound checkpoints
  (`_prior_artifacts`, 380-527) and are merged with current
  (`_merge_artifacts`).
- The produced `CORE_STAGE_CONTRACT` report contains exactly the `current`
  artifacts (`890-903`).
- `build_stage_checkpoint` and `advance_with_checkpoint` require the report
  artifact map to equal the checkpoint artifact map
  (`CW/scripts/survey_agent_control_v2.py:605-731, 2334-2343`).

Therefore, on the normal path, the `EVIDENCE_REVIEWED` checkpoint carries only
Matrix/Selection, and the `SELECTION_COMPLETE` checkpoint carries only
Architecture/Summary/Attention. The normal order is enforced by stage
validation plus report/checkpoint equality, not by `_validate_stage_artifacts`
alone.

## 3. Stage semantics and `require_approved`

`_validate_stage_semantics` (`CW/scripts/survey_stage_validation_v2.py:575-656`):

- `EVIDENCE_REVIEWED`: `_selection_basis` only; it never reads the
  already-authored Architecture.
- `SELECTION_COMPLETE`: `_selection_basis` (prior Matrix/Selection) plus
  `issue-architecture`, summary, attention; calls
  `architecture.validate_architecture(..., require_approved=False)` at
  `622-631`; recomputes the review summary exactly and validates attention at
  `634-655`.

`validate_architecture(require_approved=True)` only adds the final status check
`status == APPROVED` (`CW/scripts/survey_architecture_v2_base.py:847-848`).
That mode is **not** used by the normal stage validation (`630`) or the writer
(`CW/scripts/run_selection_architecture_v2_interactive.py:421-426`). The normal
Architecture artifact is `PROPOSED` with null `human_review`, and approval is a
separate record; drafting also requires the exact immutable `PROPOSED`
Architecture plus the Approval Record
(`CW/scripts/survey_drafting_v2_base.py:320-334, 404-422`).

`build_architecture_review_summary` readiness
(`CW/scripts/survey_architecture_v2_base.py:911, 985-986`):

- adds an error and sets `BLOCKED` if completeness is `INCOMPLETE` (`911`);
- is `READY_FOR_ARCHITECTURE_REVIEW` only when there are no errors.
- The writer refuses to write a BLOCKED summary
  (`CW/scripts/run_selection_architecture_v2_interactive.py:437-438`).
- `agent.approve_architecture` refuses a non-READY summary
  (`CW/scripts/survey_agent_control_v2.py:2414-2415`).
- Stage validation compares the supplied summary to the exact derivation
  (`CW/scripts/survey_stage_validation_v2.py:639-654`); it does not separately
  test `readiness.status`. A manually forged BLOCKED summary that exactly
  equals the derivation could pass that comparison, but approval would still
  refuse it. The normal writer guarantees READY.

## 4. Low-level approval vs canonical Human Gate

`agent.approve_architecture` (`CW/scripts/survey_agent_control_v2.py:2377-2462`):

- requires `ARCHITECTURE_ESTABLISHED`, pending Architecture Gate, passed
  Architecture checkpoint, canonical Architecture/Summary/Attention,
  `status == PROPOSED`, and `READY_FOR_ARCHITECTURE_REVIEW`;
- writes `gates/architecture-approval.json` and sets State
  `human_gates.architecture_review = approved`;
- does **not** require a reviewed commit, review index, or approval snapshot.

`survey_human_gate_v2.record_architecture_approval`
(`CW/scripts/survey_human_gate_v2.py:702-767`):

- requires the same pending `ARCHITECTURE_ESTABLISHED` Gate (`719`);
- loads/creates the review index (`720-721`);
- resolves the exact Gate artifacts (`723`);
- requires the reviewed commit to exist and be reachable from
  `profile.paths.work_branch`, and exact committed bytes for State and all
  Architecture Gate inputs (`724-730`; `_review_commit` 651-700;
  `_require_review_commit_reachable` 542-552);
- delegates the actual approval-file/State mutation to
  `agent.approve_architecture` (`731-738`);
- snapshots the approval and writes the review record/index (`739-766`).

This is the durable canonical branch boundary: the reviewed State and Gate
inputs must already be committed/reachable before the canonical Human record is
written. No Gate directory or review index currently exists; absence of the
review index is not a blocker because `_load_review_index` returns an empty
index when absent (`188-203`), but the reviewed commit/reachability still is.

## 5. Primary/supporting bounds and extension keys

Selection (`CW/scripts/survey_architecture_v2_base.py:407-566`):

- every Matrix candidate exactly once (`548`);
- SELECTED requires `PRIMARY|SUPPORTING`, at least one role, owned namespace,
  and non-HOLD/non-unresolved Evidence (`522-536`);
- non-SELECTED requires `NONE` and null roles (`539-543`);
- assignment `profile_extensions` is only required to be a dict; it is not
  checked against the Matrix row’s view annotations.

Architecture (`CW/scripts/survey_architecture_v2_base.py:567-849`):

- only selected candidates may be placed (`742`);
- same candidate cannot be both primary and supporting (`736`); package
  placement kind must equal Selection `architecture_usage` (`749`);
- SELECTED PRIMARY: exactly one package destination (`810`);
- SELECTED SUPPORTING: one or more package destinations (`816`);
- selected exception: selected only, no placement (`786-801`);
- every placed candidate’s Matrix `remaining_boundaries` must appear (`764`);
- no maximum number of primary/supporting candidates per package;
- at least one package (`677`); package IDs/orders unique (`767-769`);
- package `profile_extensions`/`publication_extensions` are only dicts
  (`721-722`); architecture-level extensions likewise (`633-634`);
- empty-placement package is at most one, last, and requires prior factual
  placements (`CW/scripts/survey_architecture_v2.py:49-95`).

Downstream, not checked by the Architecture validator:

- WEEKLY: each package needs non-empty
  `publication_extensions.section_label`; architecture needs
  `publication_extensions.closing_summary` with `required: true`,
  non-empty `heading`, `placement: "after_body_before_references"`, and
  `profile_extensions.weekly_closing_summary` with `required: true`,
  `source: "profile_synthesis.current_interpretation"`
  (`CW/scripts/survey_weekly_derivation_v2.py:404-415, 481-483`).
- LONGFORM: no `section_label`/`closing_summary` consumer was found in the
  current source. Instead, package IDs must match
  `^[A-Za-z0-9][A-Za-z0-9._-]*$` and Draft/Architecture package coverage must
  be exact (`CW/scripts/survey_longform_derivation_v2.py:37-38, 603-620,
  741-752`).
- The test-only `thematic_closing_summary` key appears only in
  `tests/test_dm022_full_lifecycle_v2.py:570-571`; current source does not
  consume it. Do not treat it as a current requirement.

Authoritative synthetic input example:

- `tests/test_dm022_full_lifecycle_v2.py:551-616` builds a complete
  `interactive-selection-architecture.json`: all assignments SELECTED
  PRIMARY, one package, `section_label`, Weekly closing keys, page plan.
- `tests/test_survey_architecture_v2.py:131-223` shows the Matrix/Selection/
  Architecture shapes and primary package boundaries.
- `tests/test_survey_reader_surface_gate_v2.py:123, 127-147` shows the Weekly
  `section_label` and closing-summary keys.
- `tests/test_run_selection_architecture_v2_interactive.py:7-57` shows the
  minimal runner-input envelope.

## 6. Pure scratch preflight with existing canonical functions

There is no single exported “preflight” function and no pure public builder for
the runner’s input-to-Selection/Architecture normalization. Existing canonical
functions are sufficient for a packet-scratch preflight; no new engine is
needed.

Existing callables:

- `derive_candidate_matrix(...)` returns the Matrix in memory
  (`CW/scripts/survey_architecture_v2_base.py:356-387`).
- `validate_candidate_matrix(matrix, *args)` validates that in-memory Matrix
  against a fresh canonical rederivation (`388-398`).
- `write_candidate_matrix(scratch_matrix, matrix)` is the canonical Matrix
  writer and refuses overwrite (`400-405`).
- `validate_selection(repo_root, selection, profile_path, matrix_path,
  completeness_path, ledger_path)` requires a Matrix **path** (`407-566`).
- `validate_architecture(repo_root, architecture, profile_path,
  completeness_path, ledger_path, matrix_path, selection_path,
  require_approved=False)` requires Matrix and Selection paths (`567-849`).
- `build_architecture_review_summary(...)` requires Matrix, Selection, and
  Architecture paths and returns the summary in memory (`852-1044`).
- `build_attention(repo_root, screening_acceptance_path,
  materiality_ledger_path, candidate_selection_path, output_path, *,
  limit=50)` writes the attention file (`CW/scripts/survey_review_attention_v2.py:32-143`).

Practical scratch sequence, using only existing functions and fresh packet
scratch:

```text
matrix = derive_candidate_matrix(...)
validate_candidate_matrix(matrix, ...)

write_candidate_matrix(<scratch>/candidate-matrix-v2.json, matrix)

validate_selection(repo_root, selection, profile,
                   <scratch>/candidate-matrix-v2.json,
                   completeness, ledger)
core.write_json(<scratch>/candidate-selection-v2.json, selection)

validate_architecture(repo_root, architecture, profile,
                      completeness, ledger,
                      <scratch>/candidate-matrix-v2.json,
                      <scratch>/candidate-selection-v2.json,
                      require_approved=False)
core.write_json(<scratch>/architecture-v2.json, architecture)

summary = build_architecture_review_summary(
    repo_root, profile, discovery, screening, evidence, views,
    ledger, completeness,
    <scratch>/candidate-matrix-v2.json,
    <scratch>/candidate-selection-v2.json,
    <scratch>/architecture-v2.json,
    implementation_sha)
assert summary["readiness"]["status"] == "READY_FOR_ARCHITECTURE_REVIEW"

build_attention(repo_root, screening, ledger,
                <scratch>/candidate-selection-v2.json,
                <scratch>/architecture-review-attention-v2.json)
```

This writes only fresh packet scratch; no source_root, State, Gate, or canonical
artifact is touched. `write_candidate_matrix` and `build_attention` refuse
overwrite; use a fresh scratch directory. `core.write_json` is the canonical
serialization helper (`CW/scripts/survey_production_v2.py:150-152`).

Caveats:

- The runner’s input-to-product normalization (Discovery-to-candidate mapping,
  boundary union, assignment order, summary counts) is inside
  `run_selection_architecture_v2_interactive.run`
  (`CW/scripts/run_selection_architecture_v2_interactive.py:322-430`); it is
  not exported as a pure builder. A manually built scratch product must
  reproduce that normalization exactly, or the scratch preflight is not proof
  of the future writer output.
- `build_architecture_review_summary` bases only on SHAs, so Matrix/Selection/
  Architecture/Summary should be byte-identical if the same bytes and
  serialization are used.
- Attention basis includes `candidate_selection_path`
  (`CW/scripts/survey_review_attention_v2.py:128-141`). A scratch Selection path
  makes the scratch Attention bytes path-distinct from the future canonical
  Attention; use it for semantic/count preflight only, not as a reusable
  canonical output.
- Existing CLI equivalents are `matrix`, `selection-check`,
  `architecture-check`, `review-summary`
  (`CW/scripts/survey_architecture_v2_base.py:1052-1195`). `review-summary`
  writes the summary to the given output and exits 1 when not READY. There is
  no attention CLI.

No execution, imports, tests, fixtures, network, Git, Production, or approval
was performed.
