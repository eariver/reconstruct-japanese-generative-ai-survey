# Selection / Architecture source route map (read-only observation)

Scope: active isolated source
`.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work`
(`CW` below). Read-only source/JSON inspection; no project execution, imports,
tests, fixtures, network, or Git/HEAD/status/log/commit readback. This does not
authorize State writes, architecture approval, commits, or publication.

## 1. Current observed starting point

Both editions are at `EVIDENCE_REVIEWED`, `next_action = stage:selection`,
`terminal_reason = null`. Their research checkpoints are legacy
`CORE_STAGE_CONTRACT` records (`kind` absent, `from_state/to_state` present), not
DM022 PREARCH records.

| edition | State | checkpoint | family | guard |
|---|---|---|---|---|
| 2026-W34 | `d7acd29b1518399ffc2376eb07e102491a6ec9782b3fdd79815c5f230e1886b0` | `0979f9f7703a25c2bd3424824bc4ad9f8719e8e7bcc49c19c5573d0f70ab593a` | LEGACY | absent |
| SP-efficient-llm-2026 | `180db8c30721825d40461cd5e1b92edb704f3630f518bfd693b4732211538220` | `1233b1f6ca3301d6430d4d157788d0a45a613c9ce1e1563e7c06fe11d73993f0` | LEGACY | absent |

Checkpoint artifacts (all live SHA-checked):

- W34: Evidence `edf21e4d…` / Views `3777133c…` / Ledger `f089cc4e…` /
  Completeness `e8c432dd…`; 409 Evidence rows, 439 Ledger rows, completeness
  `LIMITED` (3 obligations: 1 SATISFIED, 2 LIMITATION).
- SP: Evidence `65784e69…` / Views `1557fef7…` / Ledger `b7c85b4e…` /
  Completeness `d67f7f83…`; 160 Evidence rows, 165 Ledger rows, completeness
  `LIMITED` (15 obligations: 2 SATISFIED, 13 LIMITATION).

No `candidate-matrix-v2.json`, `candidate-selection-v2.json`,
`architecture-v2.json`, review summary/attention, `gates/`, `handoffs/`, or
`orchestration/v2/interactive/` exists for either edition. The writer has not
run in this instance. Packet-local prose/machine drafts may exist concurrently;
they are not source/State authority and were not used for this map.

State `implementation` is still initialization commit `48082356…`; the latest
checkpoint/implementation is e84 `e84a82ac…`. The normal agent Stage Checkpoint
path below uses the **current executing HEAD** for new checkpoints, not the
State initialization pin.

## 2. Actual code path (there is no `survey_selection_v2.py`)

The names are:

- `CW/scripts/run_selection_architecture_v2_interactive.py`
  `run(repo_root: Path, state_path: Path, input_path: Path) -> dict[str, Any]`
  at line 243. Its docstring (lines 2–10) says it does not advance State and
  never records Human Gate approval. It requires `EVIDENCE_REVIEWED` at
  lines 247–253.
- `CW/scripts/survey_architecture_v2.py` is a thin wrapper around
  `survey_architecture_v2_base.py`. Matrix/selection/architecture/review
  implementation is in the base module:
  - `derive_candidate_matrix(...)` line 356
  - `validate_candidate_matrix(...)` line 388
  - `validate_selection(...)` line 407
  - `validate_architecture(...)` line 567
  - `build_architecture_review_summary(...)` line 852
  - CLI `matrix` / `selection-check` / `architecture-check` /
    `review-summary` at lines 1052–1165.
- `CW/scripts/survey_review_attention_v2.py`
  `build_attention(repo_root, screening_acceptance_path, materiality_ledger_path,
  candidate_selection_path, output_path, *, limit=50)` at line 31.
- `CW/scripts/survey_stage_validation_v2.py`
  `validate_stage(repo_root, cfg, state_path, supplied, output_path,
  recorded_at)` at line 852. It writes one `CORE_STAGE_CONTRACT` PASS report;
  it does not write State.
- `CW/scripts/survey_agent_control_v2.py`
  - `build_stage_checkpoint(...)` line 2227
  - `advance_with_checkpoint(...)` line 2304
  - `approve_architecture(...)` line 2377
  - `resolve_checkpoint_artifact(...)` line 1149
  - `resolve_active_evidence_views(...)` line 1329
- `CW/scripts/survey_human_gate_v2.py`
  - `record_architecture_approval(...)` line 702
  - `_review_commit(...)` line 651
  - `_require_review_commit_reachable(...)` line 542
- `CW/scripts/survey_research_authority_v2.py`
  - `load_typed_checkpoint_record(...)` line 329 (strict `kind` dispatch)
  - `resolve_research_authority(state_path)` line 1128 (PREARCH four-ref)
  - `require_research_operation_ready(...)` line 3722 (guard/completion)
- `CW/scripts/survey_screening_v2.py`
  - `resolve_effective_discovery_basis(...)` line 973
  - `resolve_active_screening_acceptance(...)` line 1062

Legacy v0.1 scripts are present but are not the v2 path:
`apply_special_selection_and_propose_architecture.py` expects
`sources/<id>/pipeline-state.json` and old `gates`/matrix v0.1;
`build_architecture_input.py`, `candidate_selection_gate.py`,
`validate_issue_architecture.py` are the old v0.1 architecture-input/gate
implementation (schema `1.0`, role enums, `MAX_PACKAGE_PAGES`), not used by the
v2 interactive writer. Do not invoke them for these v2 states.

## 3. Input contract (code-defined; no JSON Schema file)

`run_selection_architecture_v2_interactive.py` validates the input at
`_validate_input` (lines 133–227). Required top-level fields are exactly:

```json
{
  "schema_version": "2.0-rc1",
  "issue_id": "<exact State issue_id>",
  "runner": {
    "provider": "<non-empty>",
    "model": "<non-empty>",
    "invocation": "<non-empty>",
    "generated_at": "<non-empty>"
  },
  "assignments": [
    {
      "discovery_id": "<Matrix Discovery ID>",
      "disposition": "SELECTED|HOLD|REJECT|INSPECT",
      "rationale": "<non-empty>",
      "architecture_usage": "PRIMARY|SUPPORTING|NONE",
      "publication_role": "<string|null>",
      "architecture_role": "<string|null>",
      "profile_extensions": {}
    }
  ],
  "architecture": {
    "editorial_thesis": "<non-empty>",
    "architecture_goals": ["<unique non-empty>"],
    "page_plan": {"target_pages": 1, "max_pages": 1, "notes": null},
    "packages": [
      {
        "package_id": "<unique non-empty>",
        "title": "<non-empty>",
        "purpose": "<non-empty>",
        "primary_discovery_ids": [],
        "supporting_discovery_ids": [],
        "must_cover_requirements": [],
        "boundaries": [],
        "drafting_order": 1,
        "profile_extensions": {},
        "publication_extensions": {}
      }
    ],
    "selected_exceptions": [],
    "profile_extensions": {},
    "publication_extensions": {}
  }
}
```

Assignment input addresses **Discovery IDs**, not candidate IDs. Every Matrix
Discovery must appear exactly once; unknown/duplicate IDs refuse (lines
156–169). The Matrix is derived from Evidence acceptance results (one row per
`evidence_task_id`), and `_matrix_discovery_map` refuses a row with more than one
Discovery or a Discovery mapped more than once (lines 230–240). Both current
editions have exactly one unique Discovery per Evidence result: W34 409/409,
SP 160/160. So the Discovery-ID input contract fits the current data.

The writer maps Discovery IDs to the deterministic candidate IDs
`candidate:<issue_id>:sha256(evidence_task_id)[:16]` (base module lines 28–30)
and builds final Selection/Architecture objects with:
`candidate-selection-v2.json` `status = ESTABLISHED` (runner lines 338–357) and
`architecture-v2.json` `status = PROPOSED`, `human_review` all null (lines
399–420). Output schemas:
`CW/schemas/candidate-selection-v2.schema.json`,
`CW/schemas/issue-architecture-v2.schema.json`,
`CW/schemas/architecture-review-summary-v2.schema.json`,
`CW/schemas/architecture-review-attention-v2.schema.json`,
`CW/schemas/candidate-matrix-v2.schema.json`.

Historical DATA examples (outputs, not current input authority):
`notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2b12.candidate-selection-v2.json`
and `DATA.p2b13.architecture-v2.json`. They show the envelope, but their
extension keys are historical; do not treat them as the current required
contract.

## 4. Four-ref / history behavior

`_dm022_pinned_family` (runner lines 50–67) classifies the pinned Evidence
checkpoint with `load_typed_checkpoint_record`. Current checkpoints have no
`kind`, so the branch is `LEGACY`.

LEGACY branch in the runner (lines 270–282):

- `agent.resolve_active_evidence_views(repo_root, cfg, state)` resolves Evidence
  and Views from the **same passed checkpoint**; it revalidates the checkpoint,
  exact artifact names, path safety and live SHA. It refuses cross-run joins and
  requires the View acceptance to bind the Evidence acceptance SHA.
- Ledger and Completeness are **canonical source_root paths**
  (`materiality-ledger-v2.json`, `profile-completeness-v2.json`), not re-read
  from the checkpoint artifact rows. In this instance those canonical paths and
  SHAs are identical to the checkpoint rows, so the four refs coincide.
- Historical accepted directories are storage only; no “latest accepted”
  selection is made.

PREARCH branch (not active here; future/DM022): `low.resolve_research_authority(
repo_root, state_path)` returns the exact four `NamedRefs` from the same typed
record, with live re-hash, lineage/SELF/proof and a final State/checkpoint
recheck; no canonical fallback after supersession. `require_research_operation_ready`
requires guard absence, and for PREARCH also full completion consistency.
Both current guards are absent.

Screening/Discovery basis is also checkpoint-bound:
`resolve_active_screening_acceptance` uses the Screening Stage Checkpoint;
`resolve_effective_discovery_basis` validates DERIVED_EXPANSION vs the accepted
root Discovery. Historical Screening accepted directories are not selected by
recency.

## 5. Authoring and write order (single writer)

`run_selection_architecture_v2_interactive.run` order:

1. Validate State (`agent.validate_agent_state`, line 249), require
   `EVIDENCE_REVIEWED` (252–253), load Profile/source root, DM022 readiness.
2. Resolve active Evidence/Views (legacy) or four PREARCH refs, active Screening
   and effective Discovery (258–292).
3. Define the seven canonical output slots (294–300).
4. Preflight all seven slots with `lstat` semantics: **any present regular,
   symlink or nonregular file refuses** (304–307; helper 101–114).
5. Derive and schema-validate the Candidate Matrix (309–314); preflight again;
   `write_candidate_matrix` (319), which itself refuses overwrite.
6. Load and validate interactive input against the derived Matrix (322–323).
7. Build assignments in Matrix candidate-ID order (324–336); construct Selection
   (338–357); schema/`validate_selection` checks (358–361); preflight; write
   Selection (362–365).
8. Map package Discovery IDs to candidate IDs, union each placed candidate’s
   Matrix `remaining_boundaries` into package `boundaries`, map exceptions, build
   `PROPOSED` Architecture (367–420); schema/`validate_architecture` checks
   (421–426); preflight; write Architecture (427–430).
9. Derive review summary via `build_architecture_review_summary` (432–436);
   require `READY_FOR_ARCHITECTURE_REVIEW` (437–438); schema validate; preflight;
   write summary (439–443).
10. Build/validate attention (444–448).
11. Create `orchestration/v2/interactive/`, copy the caller input to
    `selection-architecture-input.json` (450–454), then write
    `selection-architecture-audit.json` (455–471).

The actual write order is Matrix → Selection → Architecture → Summary →
Attention → input archive → audit. `DM022_SEVEN_SLOTS` (lines 35–43) includes
the input and audit, but those two are **not** State checkpoint artifacts and
are not in the Architecture Gate inputs. The EVIDENCE_REVIEWED checkpoint contains
`candidate-matrix` and `candidate-selection` only; the SELECTION_COMPLETE
checkpoint contains `issue-architecture`, `architecture-review-summary`,
`architecture-review-attention` (config lines 271–279, 312–334).

Guards/no-overwrite:

- Preflight refuses any of the seven slots before the first write and before
  each subsequent write; it does not accept same bytes.
- No rollback and no automatic cleanup: a failure after Matrix/Selection/
  Architecture/Summary/Attention leaves earlier files in place; rerunning the
  writer will refuse them. Preserve the failure and stop.
- `survey_stage_validation_v2.validate_stage` refuses to overwrite its report
  (line 905).
- `build_stage_checkpoint` refuses a divergent checkpoint; identical payload is
  accepted (2298). `advance_with_checkpoint` requires the canonical checkpoint
  path (2317), current lifecycle (2323), and current executing implementation
  (2331).
- `agent.approve_architecture` refuses divergent approval overwrite (2448).
- `require_research_operation_ready` is called at mutating entries/prepublish
  points; any guard file at
  `source_root/orchestration/v2/acceptance-revision.guard.json` refuses.

## 6. Candidate coverage and eligibility

Matrix rows = accepted Evidence results, not all Ledger rows. Ledger/discovery
rows with no Evidence task (W34: 26 EXCLUDED + 4 DUPLICATE; SP: 5 EXCLUDED) do
not become Matrix candidates and cannot be Selection assignments. They remain
visible in review-summary counts and attention.

`validate_selection` (base module lines 407–566) requires:

- exactly all Matrix candidates once (line 548);
- exact assignment envelope, non-empty rationale, valid disposition/usage;
- SELECTED ⇒ `PRIMARY|SUPPORTING`, at least one Profile/Publication role,
  correct namespace prefix, materiality not `NON_MATERIAL|HOLD`, evidence status
  not `REJECTED|NEEDS_MORE` (lines 522–536);
- non-SELECTED ⇒ `NONE`, both roles null (539–543);
- summary counts exactly match assignments.

Current eligibility (before the author’s substantive selection/package choices):

| edition | Matrix candidates | status split | materiality split | SELECTED-eligible under validator | not SELECTED-eligible |
|---|---:|---|---|---:|---:|
| W34 | 409 | 38 VERIFIED / 363 PARTIAL / 8 NEEDS_MORE | 41 MATERIAL / 358 CONTEXT / 10 HOLD | 399 | 10 HOLD (8 NEEDS_MORE + 2 PARTIAL) |
| SP | 160 | 8 VERIFIED / 152 PARTIAL | 132 MATERIAL / 28 CONTEXT | 160 | 0 |

W34 status×materiality detail: `VERIFIED/MATERIAL 30`, `VERIFIED/CONTEXT 8`,
`PARTIAL/MATERIAL 11`, `PARTIAL/CONTEXT 350`, `PARTIAL/HOLD 2`,
`NEEDS_MORE/HOLD 8`. SP: `VERIFIED/MATERIAL 8`, `PARTIAL/MATERIAL 124`,
`PARTIAL/CONTEXT 28`.

`PARTIAL` is eligible; only `REJECTED`/`NEEDS_MORE` are blocked. `CONTEXT` is
eligible; only `NON_MATERIAL`/`HOLD` are blocked. HOLD/REJECT/INSPECT
dispositions remain assignable with no package role; the rationale is the
Human-facing audit text.

## 7. Architecture package/compression rules

`validate_architecture` (base module lines 567–850) requires:

- selection valid first;
- only SELECTED candidates may appear in packages; non-selected IDs refuse
  (742);
- same candidate cannot be PRIMARY and SUPPORTING (736); package kind must match
  the Selection `architecture_usage` (749);
- every placed candidate’s `remaining_boundaries` must be present in package
  `boundaries` (764); the writer auto-unions them (runner 373–378);
- SELECTED PRIMARY must have exactly one package destination; SELECTED
  SUPPORTING must have at least one (810, 816);
- selected exceptions are only for SELECTED candidates, must have a reason/kind,
  and cannot coexist with a package placement (786–801);
- package IDs and drafting orders unique (767–769); at least one package (677);
- page plan positive/consistent (`max_pages >= target_pages`, 658); no page cap
  is enforced by this validator;
- `status` may only be `PROPOSED|APPROVED`; writer emits PROPOSED; PROPOSED
  must have all `human_review` fields null (845); `require_approved` is false
  for the pre-Gate validation.

The wrapper `survey_architecture_v2.py` adds: at most one **empty-placement**
cross-package synthesis package, it must be last in drafting order, and another
package must own factual candidate placements (lines 49–95). This is relevant if
a final WEEKLY_SYNTHESIS-style package has no candidates.

There is no fixed section enum in the v2 Architecture validator. Package
`profile_extensions` / `publication_extensions` are pass-through objects. The
old DATA example’s `section_kind` is not the current Weekly contract.

Downstream constraints not enforced at this gate (concrete future blockers):

- Weekly reader derivation requires each package
  `publication_extensions.section_label` (non-empty) and requires architecture
  `publication_extensions.closing_summary` plus
  `profile_extensions.weekly_closing_summary` in the exact shape at
  `CW/scripts/survey_weekly_derivation_v2.py:404–413, 481–483`.
- Longform derivation requires package IDs in its token subset
  (`^[A-Za-z0-9][A-Za-z0-9._-]*$`) and exact Draft/Architecture package coverage
  (`CW/scripts/survey_longform_derivation_v2.py:37–38, 603–620, 741–752`).
- Page target/max is author-supplied; neither current Production Profile carries
  a page budget.

## 8. Obligation/compression audit surface

`build_architecture_review_summary` (base 852 onward) emits:

- selection/materiality/evidence/screening/discovery counts;
- completeness `overall_status` + obligation status counts;
- `major_material_destinations`: one row for every MATERIAL/CONTEXT candidate
  with destination kind PRIMARY/SUPPORTING/EXCEPTION/NOT_SELECTED and the
  exception/selection rationale;
- residual limitations;
- architecture status, thesis, package count/titles, page plan.

It blocks readiness only when the underlying validation errors exist or
completeness is `INCOMPLETE` (current both LIMITED, so not blocking). There is no
machine check that every completeness obligation is mapped to a package, and no
“compression ratio” gate. `must_cover_requirements` is free-form; the hard
compression rules are the package coverage rules above.

`build_attention` (review_attention lines 31–147) adds a bounded audit surface:
Screening DROP/MAYBE/INSPECT, Materiality HOLD/NON_MATERIAL/EXCLUDED/DUPLICATE,
Selection HOLD/REJECT/INSPECT. Default limit is 50; overflow is counted. Current
attention pools are large (W34 366 screening-eligible + 40 materiality-eligible
+ selection non-selections; SP 30 + 5 + selection non-selections), so the
Human-facing view will truncate.

## 9. Stage and Human-Gate boundary

| Boundary | Current/from | Artifacts | Checkpoint | Result |
|---|---|---|---|---|
| Authoring | EVIDENCE_REVIEWED (state unchanged) | 7 slots written by interactive runner | none | files exist but are not State-bound |
| Selection transition | EVIDENCE_REVIEWED | Matrix + Selection | `orchestration/v2/checkpoints/EVIDENCE_REVIEWED.json` | `SELECTION_COMPLETE` |
| Architecture transition | SELECTION_COMPLETE | Architecture + Summary + Attention | `.../SELECTION_COMPLETE.json` | `ARCHITECTURE_ESTABLISHED`, pending Architecture Gate |
| Human approval | ARCHITECTURE_ESTABLISHED + pending | gate inputs + exact reviewed commit | approval + review record/index | `human_gates.architecture_review = approved`; architecture file remains PROPOSED |

**Can the writer produce architecture while State is EVIDENCE_REVIEWED? Yes.**
The writer only checks `EVIDENCE_REVIEWED` (runner 252–253) and writes
`architecture-v2.json`; it does not advance State. That architecture is
provisional/unbound until the SELECTION_COMPLETE transition consumes it. The
selection validation ignores the already-present architecture; the architecture
validation later requires it. If the writer fails after writing some slots, the
no-overwrite preflight blocks a clean retry.

After the architecture transition, `derive_control_fields` sees
`ARCHITECTURE_ESTABLISHED` + pending gate and sets `next_action =
ARCHITECTURE_REVIEW`, `terminal_reason = HUMAN_GATE_REACHED`
(`survey_production_v2.py:550–567`). `build_stage_checkpoint` refuses while
`terminal_reason` is set (agent-control 2247), so no Draft/PDF stage can run
before Human approval.

Human approval is **not** an Architecture JSON edit. The low-level
`agent.approve_architecture` writes `gates/architecture-approval.json` and
mutates State; it requires `ARCHITECTURE_ESTABLISHED`, pending Gate, completed
Architecture checkpoint and canonical PROPOSED Architecture/Summary/Attention
(agent-control 2377–2470). The canonical durable Human review path is
`survey_human_gate_v2.record_architecture_approval` (702): it additionally
requires a pending Gate, a review index, a commit that exists and is reachable
from `profile.paths.work_branch`, and exact committed bytes of the State and
all Architecture Gate inputs (`_review_commit`, 651; reachability 542). It
snapshots the approval and writes the review record/index. This is where the
Profile-bound canonical work branch / reviewed commit boundary lives. No gate
directory or review index exists in this instance; no commit/approval is
authorized here.

## 10. Public CLI answers (do not execute in this read-only unit)

Authoring/prep (single command; writes both Selection and Architecture
proposals; no State advance):

```text
python scripts/run_selection_architecture_v2_interactive.py \
  --repo-root . --state sources/<issue>/production-state.json \
  --input <interactive-selection-architecture.json>
```

Read-only/offline matrix derivation (optional; write outside source_root if you
do not intend to consume the slot yet, because the combined runner refuses a
pre-existing Matrix):

```text
python scripts/survey_architecture_v2_base.py matrix \
  --profile <profile> --discovery <jsonl> --screening <screening-accepted> \
  --evidence <evidence-accepted> --views <views-accepted> \
  --ledger <ledger> --completeness <completeness> --output <path>
```

Selection stage report (no State write):

```text
python scripts/survey_stage_validation_v2.py --repo-root . \
  --state sources/<issue>/production-state.json \
  --artifact candidate-matrix=sources/<issue>/candidate-matrix-v2.json \
  --artifact candidate-selection=sources/<issue>/candidate-selection-v2.json \
  --output sources/<issue>/orchestration/v2/stage-validation/EVIDENCE_REVIEWED-report.json
```

Selection transition (builds the EVIDENCE_REVIEWED checkpoint and advances one
step):

```text
python scripts/survey_agent_control_v2.py --repo-root . advance-stage \
  --state sources/<issue>/production-state.json \
  --artifact candidate-matrix=sources/<issue>/candidate-matrix-v2.json \
  --artifact candidate-selection=sources/<issue>/candidate-selection-v2.json \
  --reviews sources/<issue>/orchestration/v2/stage-reviews/EVIDENCE_REVIEWED-reviews.json \
  --summary "<stage summary>"
```

Architecture stage: repeat the last two commands while State is
`SELECTION_COMPLETE`, with `--artifact issue-architecture=...`,
`--artifact architecture-review-summary=...`,
`--artifact architecture-review-attention=...`, output/report
`SELECTION_COMPLETE-report.json`, and reviews
`SELECTION_COMPLETE-reviews.json`. That advances to `ARCHITECTURE_ESTABLISHED`.

The review JSON must contain at least one deterministic
`CORE_STAGE_CONTRACT` review with `result_path` pointing at the stage-validation
report (see current `stage-reviews/CANDIDATES_NORMALIZED-reviews.json` for the
observed shape). `build_stage_checkpoint` requires at least one review row
(2260), and `_validate_core_stage_report` requires exactly one deterministic
CORE_STAGE_CONTRACT PASS (605–731).

Human approval (only after the pending Gate; not authorized now):

```text
python scripts/survey_human_gate_v2.py --repo-root . record-architecture-approval \
  --state sources/<issue>/production-state.json \
  --reviewed-by <name> --reviewed-at <ISO> --review-reference <ref> \
  --reviewed-commit-sha <reachable-commit> --expected-revision 1
```

Do **not** use `survey_orchestrator_v2.py advance-to-gate` as the normal
selection/architecture path here: the config has `handoff_required: false` for
both stages, while `survey_handoff_v2.build_handoff` refuses unless it is true
(101–102) and `stage:selection`/`stage:architecture` are registered as
`stage_handoff_handler`, which requires a `stage-handoff` input. Also,
`survey_orchestrator_v2.verify_runtime_implementation` (107–119) compares the
State-pinned initialization commit 4808 to observed HEAD e84/control roots,
which is not the same contract as the agent Stage Checkpoint path. The source-
consistent local path is `survey_agent_control_v2.py advance-stage`.

## 11. Concrete blockers / missing inputs

1. **No runner input document exists.** Neither edition has
   `interactive-selection-architecture.json`. Packet-local drafts may exist
   concurrently, but they are not the validated runner input and are not
   State-bound. All 409/160 runner-format assignments and the package design
   remain to be validated/adopted through the writer.
2. **W34 cannot select 10 candidates** (8 `NEEDS_MORE/HOLD` + 2
   `PARTIAL/HOLD`). They must be HOLD/REJECT/INSPECT with `NONE` and rationale;
   399 are SELECTED-eligible. SP has no HOLD/NEEDS_MORE and all 160 are eligible.
3. **Package coverage is a hard authoring constraint**, not an automatic
   optimizer: every selected non-exception candidate must be placed exactly once
   as PRIMARY or at least once as SUPPORTING; exceptions must be selected and
   unplaced; non-selected candidates cannot be placed; empty-placement synthesis
   is at most one/last.
4. **Page plan is author-supplied.** Neither Production Profile contains a page
   target/max; W34/SP do not currently have a v2 architecture page budget.
5. **No stage-validation report or stage-review file exists** for
   EVIDENCE_REVIEWED. The review file must reference a report produced from the
   exact current bytes.
6. **No commit/Gate surface exists** for actual Human approval. `gates/`,
   `gates/review-index.json`, and the canonical work-branch reviewed commit are
   absent/unverified. Git readback is prohibited in this unit; approval remains
   impossible and unauthorized.
7. **No-overwrite is strict and there is no rollback.** A mid-writer failure
   leaves earlier slots; rerun refuses. Do not clean/force/retry locally without
   a concrete root decision.
8. **Legacy four-ref asymmetry:** in the current LEGACY family, Evidence/Views
   come from the checkpoint, but Ledger/Completeness are canonical source_root
   paths. They match the checkpoint rows here, but a noncanonical legacy
   checkpoint's Ledger/Completeness refs would be ignored. This is the actual
   behavior; only the future PREARCH path resolves all four from one typed
   record.
9. **Wrong-CLI risk:** orchestrator `advance-to-gate`/handoff path is not
   compatible with `handoff_required: false` and the State-pinned 4808 vs HEAD
   e84 distinction. Use the agent-control stage path.
10. **Downstream keys not checked at this gate:** Weekly `section_label` and
    closing-summary keys, and Longform package-ID/coverage rules, can pass the
    Architecture validator but fail later. Author them now if the target is
    eventual publication.
11. **Attention truncation:** default 50 items; W34/SP exception surfaces will
    overflow. The counts remain exact, but the reviewer sees only the first
    sorted 50.

No authorization is inferred from this map. Stop at the next Human Commit
Point; no architecture approval, State write, Draft/PDF, commit, or push is
performed by this observation.
