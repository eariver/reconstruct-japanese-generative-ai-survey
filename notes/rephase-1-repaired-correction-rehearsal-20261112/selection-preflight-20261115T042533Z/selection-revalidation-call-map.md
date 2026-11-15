# Selection/Architecture normal-writer revalidation call map

Status: read-only source analysis for Root §20. No imports, execution, tests, Git, network, Production/reconstruct readback, active writes, or subagent use. No State/source file changed. This document is analysis only; it is not Selection/Architecture PASS, not a repair selection, and not a runtime measurement.

## 0. Observed snapshot used

- Shadow workspace read (not the active rehearsal):
  `.rephase-1-editorial-runtime/selection-preflight-20261115T042533Z/candidate-work`
- Shadow HEAD `ae0dd1ee5b0e7a85c44bdab0e6cd024bf12f0c56`, tree `ec11cf6c49b3cdf54c7aa98703f6d3e74806dc58`.
- Runner: `scripts/run_selection_architecture_v2_interactive.py`, SHA256 `553bf22bb7d218af3b20f7ba303110b7c7918da4de5e39e07c756675503f2b31`, 27766B.
- LOW helper: `scripts/survey_research_authority_v2.py`, SHA256 `7f5fc9e0d79729d98345f0b0352d5070c76e93f92f2c14148e22c9f38a8f4c0f`, 240969B.
- HIGH helper: `scripts/survey_prearchitecture_acceptance_v2.py`, SHA256 `f312f02e2dc5c1aa5a1d6432bca134cd83f0a1edea2d127721d0206d05514a90`, 97844B. It is in the own-epoch mapped codeset but is **not imported by this normal-writer call graph**.
- Both shadow States are `EVIDENCE_REVIEWED` with the same PREARCH record in the evidence/materiality/completeness provenance triplet:
  - W34: `73ab28ea79da8bb13d7083d30eda7fa3188f060f0dbaa96a65e2407daae3ac48`
  - SP: `2a528ed533010da6acc9efaef0e24fb59be62417724b00919e0c2f6983fec9f5`
- Saved preflight raw: W34 `0/7` slots, SP `3/7` slots (matrix, selection, architecture), both `exit 124`, stdout/stderr `0B`, each wall time about 1200s. The saved raw contains no call stack or per-phase timing.

The source counts below are static call counts, not observed runtime counts. The actual `N` is the accepted Evidence task/result count: W34 `409`, SP `160`.

## 1. Normal-writer entry sequence

`run_selection_architecture_v2_interactive.py:run()` lines 243-481.

| Step | Site | What it invokes | PREARCH revalidation effect |
|---|---|---|---|
| 1 | `:249` | `agent.validate_agent_state(repo_root, cfg, state)` | 3 whole adopted-graph validations (see §2.1) |
| 2 | `:260` | `_dm022_require_ready()` -> `low.require_research_operation_ready()` | 1 completion verification = 2 whole adopted-graph validations |
| 3 | `:264` | `_dm022_resolve_ledger_completeness()` -> `resolve_research_authority()` | 1 whole adopted-graph validation |
| 4 | `:270` | `_dm022_pinned_family()` | typed checkpoint load only |
| 5 | `:271` | `low.resolve_research_authority()` | 1 whole adopted-graph validation; **same State/checkpoint already resolved at `:264`** |
| 6 | `:283` | `screening.resolve_active_screening_acceptance()` | 2 state validations = 6 whole adopted-graph validations (see §2.4) |
| 7 | `:286` | `screening.resolve_effective_discovery_basis()` | no whole adopted graph |
| 8 | `:304` | `_dm022_preflight_seven()` | lstat only |
| 9 | `:310` | `architecture.derive_candidate_matrix()` | 1 upstream load = 45 whole adopted-graph validations + 6 Evidence / 3 View content passes + matrix projection |
| 10 | `:316` | `_dm022_require_ready()` | 2 whole adopted-graph validations |
| 11 | `:319` | write `candidate-matrix-v2.json` | first possible write |
| 12 | `:338-359` | build and validate Selection | small JSON/hash checks; `validate_selection` |
| 13 | `:362` | `_dm022_require_ready()` | 2 whole adopted-graph validations |
| 14 | `:365` | write `candidate-selection-v2.json` | |
| 15 | `:368-426` | build and validate Architecture | small JSON/hash checks; `validate_architecture` internally calls `validate_selection` again |
| 16 | `:427` | `_dm022_require_ready()` | 2 whole adopted-graph validations |
| 17 | `:430` | write `architecture-v2.json` | |
| 18 | `:432` | `architecture.build_architecture_review_summary()` | 2 upstream loads = 90 whole adopted-graph validations + 12 Evidence / 6 View content passes + matrix projection |
| 19 | `:440` | `_dm022_require_ready()` | 2 whole adopted-graph validations |
| 20 | `:443` | write `architecture-review-summary-v2.json` | |
| 21 | `:444` | `_dm022_require_ready()` | 2 whole adopted-graph validations |
| 22 | `:447` | `review_attention.build_attention` / `validate_attention` | small JSON/hash checks |
| 23 | `:451` | `_dm022_require_ready()` | 2 whole adopted-graph validations |
| 24 | `:454` | archive input | |
| 25 | `:456` | `_dm022_require_ready()` | 2 whole adopted-graph validations |
| 26 | `:459` | write audit | |

`_dm022_require_ready()` itself is only:

```text
run_selection_architecture_v2_interactive.py:46-47
  -> low.require_research_operation_ready(repo_root, state_path)
       low:4087-4140
         -> require_no_active_guard(source_root)                    # :4119
         -> structural State/profile/triplet peek                   # :4104-4138
         -> _verify_completion_full(repo_root, source_root, ref)    # :4139
              -> _verify_adopted_graph_full(...)                    # :1018
              -> _verify_adopted_graph_full(...)                    # :1073
```

For PREARCH, the guard check is cheap; the completion check is not. Each `_dm022_require_ready` therefore costs **2 whole adopted-graph validations**. There are **8** calls before the seven writes: lines 260, 316, 362, 427, 440, 444, 451, 456.

## 2. Revalidation units and their internal repeats

### 2.1 Whole adopted-graph unit (`AG`)

`low._verify_adopted_graph_full(repo_root, checkpoint_path, checkpoint_sha)` at `low:802-993`.

Exact sequence:

1. Read checkpoint file and rehash: `:824-827`.
2. `load_typed_checkpoint_record`: `:828` (schema/kind/operation/boundary).
3. `_load_typed_four_refs`: `:832` (classification, file SHA, artifact schema/digest/shape; not per-card content).
4. `_verify_sized_ref_bytes` for request/profile/discovery/screening refs: `:837-856`.
5. Manifest and retention-plan binding: `:858-920`.
6. Retained COPY read and hash/byte check: `:918-925`.
7. `derive_ordinary_root_effective_context` (DCP/SCP, request, profile, root/effective Discovery): `:929-935`.
8. Full content validators: `:945-972`.
9. `_verify_own_epoch_commit`: `:979`.
10. Return loaded pieces: `:980-993`.

The full content block is the expensive part. Its effective content calls are:

| Site | Call | Evidence content passes | View content passes |
|---|---|---|---|
| `:946` | `evidence._validate_evidence_acceptance_content` | 1 | 0 |
| `:950` | `evidence._validate_edition_views_acceptance_content` | 1 (nested evidence at `evidence:1876`) | 1 |
| `:957` | `evidence._validate_materiality_ledger_content` | 1 direct + 1 nested via views (`evidence:2749`, `:2752`, `:1876`) | 1 nested via views (`:2752`) |
| `:965` | `completeness._validate_profile_completeness_content` | 1 direct + 1 nested via completeness->ledger->views (`completeness:255`, `evidence:2934`, `:2749`, `:2752`, `:1876`) | 1 nested |
| **Total per AG** | | **6 Evidence content passes** | **3 View content passes** |

A single Evidence content pass (`evidence._validate_evidence_acceptance_content`, `:1738-1793`) does at least:

- `_capture_phase_pins` over every accepted task and result: `:1652`.
- `_load_pinned_json` for every task and every result: `:1670`, `:1673`.
- `_recheck_phase_pins` over the same task/result set: `:1664`, `:1693`.
- `_resolve_phase_supplement_context`: `:1779`.
- `_recheck_supplement_context`: `:1791`.

The entry helper `_check_evidence_acceptance_results_with_context` (`:1621-1695`) therefore reads each task/result file at least four times per pass (capture, load, two rechecks), plus the full declared supplement manifest/Raw closure twice (`_resolve_phase_supplement_context` `:300-386`, `_recheck_supplement_context` `:389-424`). This is a source-based count; it does not assume a filesystem speed.

The View content pass (`:1856-1893`, row checks `:1796-1853`) also re-runs the Evidence content pass at `:1876`, pins/loads all views at `:1826`, `:1837`, and rechecks at `:1834`, `:1852`. So **every AG is not one graph walk; it is six Evidence walks and three View walks, with nested re-entry into Evidence from Views, Ledger, and Completeness.**

`_verify_own_epoch_commit` (`low:639-799`) per AG:

- `git cat-file -e` commit, `git show` config: `:671-673`.
- `git ls-tree -r` over the mapped codeset/config/profile: `:696`.
- `git cat-file --batch` over all needed code/config/schema/profile blobs: `:716-726`.
- Schema `$id` and Contract8 recomputation: `:754-798`.

This is a Git object read, not a worktree read, but it is repeated on every AG.

### 2.2 Completion verification unit

`low._verify_completion_full` (`:996-1125`):

- `_verify_adopted_graph_full` at `:1018`.
- Reads completion/inventory/COPY, validates receipt, recomputes expected-after: `:1022-1063`.
- Re-reads LIVE State/triplet: `:1064-1072`.
- `_verify_adopted_graph_full` again at `:1073`.

The second AG is an exact duplicate of the first for the same checkpoint. Therefore one `_dm022_require_ready` call = **2 AG** for PREARCH.

### 2.3 Path resolver unit

`low.resolve_research_authority` (`:1128-1228`):

- `_load_typed_four_refs` at `:1164`.
- `_verify_adopted_graph_full` at `:1177`; this itself calls `_load_typed_four_refs` again at `:832`.
- Report/proof/decision/request/retention/COPY reload and cross-bind: `:1181-1201`.
- Final State re-read, triplet recheck, checkpoint FILE rehash: `:1205-1213`.

So one resolve = one AG plus duplicated four-ref loading plus a final freshness recheck.

### 2.4 State-validation path and the PREARCH multiplier

`agent.validate_agent_state` (`survey_agent_control_v2.py:919-1099`) at `EVIDENCE_REVIEWED`:

- `_expected_completed_checkpoints`: `:958`, includes discovery, screening, evidence, materiality, completeness.
- Loop over checkpoints: `:969-998`.
- For each passed checkpoint with provenance, `_validate_checkpoint_record`: `:996`.

For a PREARCH same-record triplet, evidence/materiality/completeness all dispatch to the PREARCH branch:

```text
_validate_checkpoint_record                         agent:770-805
  -> _validate_prearchitecture_core_proof            agent:805 -> :290-321
       -> check_supersession_record_from_paths       low:3848-3976
            -> _verify_adopted_graph_full            low:3885   (one AG)
```

Thus **one `agent.validate_agent_state` call on these States = 3 AG** (one for each of evidence, materiality, completeness). The duplicate record is validated three times.

`survey_agent_tool_v2.verify_current_stage_basis` (`:42-50`) calls `agent.validate_agent_state` at `:48`. Under `current_stage_basis_override()` (`:121-143`), every public package basis checker that calls `core.verify_state_basis` becomes another state validation. This is why the normal matrix/review path also triggers many AGs:

- `screening.validate_package_basis`: `survey_screening_v2.py:1322-1338`; calls `core.verify_state_basis` at `:1336`.
- `evidence.validate_evidence_package_basis`: `survey_evidence_v2.py:1203-1251`; calls `core.verify_state_basis` at `:1223`.
- Under the override, each such call invokes `agent.validate_agent_state` once = **3 AG** on PREARCH States.

### 2.5 Upstream load unit (`EU`) used by matrix/review

`survey_architecture_v2_base._load_upstream` (`:279-353`) is called by:

- `derive_candidate_matrix` at `:373`; from the runner at `:310`.
- `build_architecture_review_summary` at `:866`.
- `validate_candidate_matrix` at `:390`, called by `build_architecture_review_summary` at `:880`; that re-enters `derive_candidate_matrix` and therefore `_load_upstream` a second time.

`_load_upstream` calls these public validators in order:

| Site | Public validator | State validations inside it (under the override) |
|---|---|---|
| `:292` | `evidence.validate_screening_acceptance` | 1 (screening package basis) |
| `:299` | `evidence.validate_evidence_acceptance` | 2 (evidence package basis + nested screening at `evidence:1993`) |
| `:302` | `evidence.validate_edition_views_acceptance` | 2 (it calls `validate_evidence_acceptance` at `:2543`) |
| `:310` | `evidence.validate_materiality_ledger` | 5 (screening + evidence + views/evidence: `:2781-2786`) |
| `:321` | `completeness.validate_profile_completeness` | 5 (it calls `evidence.validate_completeness` -> `validate_materiality_ledger`: `completeness:276`, `evidence:2958`) |

Total per `_load_upstream`: **15 state validations**. On PREARCH, each is 3 AG, so one EU = **45 AG**, plus its own **6 Evidence / 3 View content passes**, plus (for matrix) the projection.

The matrix projection `_derive_matrix_rows_content` (`:183-276`) is not a full semantic revalidation, but it does re-read every accepted card and view:

- `core.sha256_file(card_path)` `:213`
- `core.sha256_file(view_path)` `:215`
- `core.load_json(card_path)` `:217`
- `core.load_json(view_path)` `:218`

Call this `P`: **1 Evidence + 1 View byte read/parse per task**, in addition to EU.

## 3. W34: the block before the first matrix write

W34 produced `0/7` slots. The first possible write is `candidate-matrix-v2.json` at `run:319`. Between entry and that write, the source order is:

| Runner site | Unit | AG count |
|---|---|---|
| `:249` | `agent.validate_agent_state` | 3 |
| `:260` | `_dm022_require_ready` | 2 |
| `:264` | `_dm022_resolve_ledger_completeness` -> resolve | 1 |
| `:270` | `_dm022_pinned_family` | 0 (typed load only) |
| `:271` | `resolve_research_authority` again | 1 |
| `:283` | `screening.resolve_active_screening_acceptance` | 6 |
| `:310` | `derive_candidate_matrix` -> `_load_upstream` | 45 |
| `:316` | `_dm022_require_ready` | 2 |
| **Total before matrix write** | | **60 AG** |

The `:283` count is 6, not 3, because:

1. `agent.resolve_checkpoint_artifact("screening", ...)` calls `_validate_agent_state` at `agent:1210` -> 3 AG.
2. `validate_acceptance` is entered under `current_stage_basis_override()` at `screening:1102-1103`; its `validate_package_basis` reaches `core.verify_state_basis` -> `verify_current_stage_basis` -> `agent.validate_agent_state` at `agent_tool:48` -> another 3 AG.

So before `candidate-matrix-v2.json` can exist, the source calls the equivalent of:

```text
60 AG + 1 EU own-content + 1 P
= 60*(6 Evidence + 3 View) + (6 Evidence + 3 View) + (1 Evidence + 1 View)
= 367 Evidence content passes + 184 View content passes
```

before any Source/State write. With W34 `N=409`, that is arithmetic for `367 x 409 = 150,103` Evidence task/result content validations and `184 x 409 = 75,256` View validations, before the matrix row projection. Each Evidence pass additionally performs the pin/load/recheck reads described in §2.1. These are source-derived counts, not measured runtime counts.

The exact call that consumed the 1200s cannot be identified from the saved raw: stdout/stderr are 0B and there is no stack. The source order says the timeout is somewhere inside this pre-write block, and the largest blocks are the `:249` state validation, `:283` screening resolution, `:310` matrix upstream load, and the repeated `:260`/`:316` readiness gates.

Notably, `:264` and `:271` are an exact duplicate resolve of the same State/checkpoint with no intervening write. `:270` also repeats the typed family load already performed inside `_dm022_resolve_ledger_completeness` at `:83`.

## 4. SP: the block after Architecture and before Review Summary

SP produced `3/7` slots: matrix (`run:319`), selection (`:365`), architecture (`:430`). The timeout therefore occurred after `:430`, in one of these source positions:

1. `:432-439` `build_architecture_review_summary`.
2. `:440` `_dm022_require_ready`.
3. before `:443` writes `architecture-review-summary-v2.json`.

The source block is:

| Runner site | Unit | AG count |
|---|---|---|
| `:432` | `build_architecture_review_summary` -> `_load_upstream` at `:866` | 45 |
| `:432` | `validate_candidate_matrix` at `:880` -> `derive_candidate_matrix` -> `_load_upstream` again | 45 |
| `:432` | `_derive_matrix_rows_content` projection (via the second derive) | 0 AG, 1 P |
| `:432` | `validate_selection` at `:892` | 0 (small JSON/hash checks) |
| `:432` | `validate_architecture` at `:900` -> base `validate_architecture` -> `validate_selection` again | 0 (small JSON/hash checks) |
| `:440` | `_dm022_require_ready` | 2 |
| **Total after Architecture, before review write** | | **92 AG** |

That is:

```text
92 AG + 2 EU own-content + 1 P
= 92*(6 Evidence + 3 View) + 2*(6 Evidence + 3 View) + (1 Evidence + 1 View)
= 565 Evidence content passes + 283 View content passes
```

With SP `N=160`, that is `565 x 160 = 90,400` Evidence task/result content validations and `283 x 160 = 45,280` View validations after the Architecture write and before the review summary write. This is consistent with the observed `3/7` partial output: the run crossed the three writes and then entered the heaviest remaining block.

The two `_load_upstream` calls in `build_architecture_review_summary` are not two independent graph variants. The first at `:866` validates and loads the upstream graph. The second at `:880` is `validate_candidate_matrix` re-deriving the exact Matrix from the same paths, which recursively calls `_load_upstream` again at `architecture:373`. There is no new input between them.

If the run had continued past `:440`, the remaining readiness gates at `:444`, `:451`, `:456` would each add 2 AG, and `build_attention`/`validate_attention` would add only small JSON/hash work. The full seven-slot run would therefore be:

```text
27 direct AG (initial/resolve/screening + 8 readiness gates x 2)
+ 3 EU x 45 AG = 135 AG
= 162 AG, plus 3 EU own-content and 2 P projections
```

This full-run count is source-based, not observed; the actual W34/SP runs stopped earlier.

## 5. LEGACY vs PREARCH comparison

| Path | LEGACY | PREARCH (these States) |
|---|---|---|
| `agent.validate_agent_state` | Legacy checkpoint schema/report/artifact checks; no whole adopted graph | 3 AG, one per evidence/materiality/completeness, via `_validate_prearchitecture_core_proof` -> `check_supersession` -> AG |
| `_dm022_require_ready` | Guard absence only (after State/profile checks) | Guard absence + `_verify_completion_full` = 2 AG per call |
| `_dm022_resolve_ledger_completeness` | Returns canonical `materiality-ledger-v2.json` / `profile-completeness-v2.json`; no low resolve | `resolve_research_authority` = 1 AG |
| Four-ref branch in `run` | `agent.resolve_active_evidence_views`; no low resolve | Second `resolve_research_authority` = 1 AG |
| `screening.resolve_active_screening_acceptance` | `_validate_agent_state` once, plus state validation inside `validate_acceptance`, but legacy checks only | 2 state validations, each 3 AG = 6 AG |
| `_load_upstream` public validators | 15 state validations; legacy checkpoint/artifact rehash only, plus 6 Evidence / 3 View content passes | 15 state validations, each 3 AG = 45 AG, plus 6 Evidence / 3 View content passes |

The important comparison is that the matrix/review path is **not PREARCH-free**. `_load_upstream` executes public validators under `current_stage_basis_override()`, and each public package basis check calls `core.verify_state_basis`, which under the override calls `agent.validate_agent_state`. On PREARCH States that state validation contains the three nested AGs. Therefore the same `_load_upstream` that would be expensive-but-bounded on LEGACY becomes `45 AG + own-content` on PREARCH. This is the main reason the normal Selection writer is much heavier on these post-DM022 States than a legacy edition would be.

## 6. What is actually repeated, and what is not

### Repeated full Raw / accepted bytes

- Every Evidence content pass re-pins and re-reads the accepted Evidence task/result set, plus the declared supplement manifest and Raw closure.
- The same accepted Evidence set is revalidated 6 times inside one AG, and the same AG is invoked repeatedly by state validation, completion, resolve, and upstream loads.
- View content passes likewise re-read the full accepted View set 3 times per AG and re-enter Evidence each time.

### Repeated whole 409/160 graph

- The whole accepted graph is revalidated at every AG. The graph is not reduced to a projection during these passes.
- The full W34/SP task/result/view sets are the `N=409`/`N=160` multiplier. The source call counts in §§3-4 are not per-record loops written by the runner; the runner invokes the validators, and the validators loop over all records each time.

### Old/new graph reads

- The PREARCH path does not reopen old canonical Ledger/Completeness. `_load_typed_four_refs` and `_verify_adopted_graph_full` use the pinned PREARCH record's four refs.
- "Old" reads that do occur are the retained `before_state` COPY, request/report/proof/decision/retention lineage, and previous checkpoint data in `resolve_research_authority` (`low:1181-1201`). They are not a second full old graph validation.
- The same record is parsed repeatedly, but the graph content is the new adopted graph, not the old legacy graph.

### Profile / code objects

- `_verify_own_epoch_commit` (`low:639-799`) performs Git object-DB reads of the mapped DM022 codeset, config, schemas, and request Profile on every AG. This is repeated whole-profile/code-object verification, but from the recorded commit, not the live worktree.
- `_verify_adopted_graph_full` also loads the request Profile bytes through `_verify_sized_ref_bytes` and `_context_from_before_state`.
- `HIGH` (`survey_prearchitecture_acceptance_v2.py`) is pinned in the own-epoch codeset but is not imported/called by this writer.

### Pure projection

- `_derive_matrix_rows_content` is the projection: it rehashes and reloads each card/view (`architecture:213-218`) and builds rows/summary. It does not re-run card semantics.
- `build_architecture_review_summary` assembles counts, major destinations, readiness, and residual limitations from already-validated upstream data. The projection itself is cheap relative to the repeated full content passes; the expensive part is that the summary builder calls `_load_upstream` and `validate_candidate_matrix` again.
- `validate_selection` and `validate_architecture` are small JSON/hash/shape checks. `validate_architecture` calls `validate_selection` a second time, but that is not a full graph walk.

### No infinite recursion

No self-recursive cycle was found:

- `AG` does not call `check_supersession`, `resolve_research_authority`, or `require_research_operation_ready`.
- `check_supersession` calls `AG`; `AG` does not call `check_supersession`.
- `require_research_operation_ready` calls completion; completion calls `AG`; `AG` does not call completion.
- `resolve_research_authority` calls `AG`; `AG` does not call resolve.
- `_load_upstream` calls public validators; those call state validation; state validation calls `check_supersession`; `check_supersession` calls `AG`. This is a finite DAG of repeated calls, not an unbounded loop.

The repeated work is sibling duplication and internal duplication (completion lines 1018/1073, runner lines 264/271, nested Evidence revalidation inside Views/Ledger/Completeness), not a cyclic recursion.

## 7. Candidate optimization boundary (not selected, not implemented)

The candidate boundary suggested by this call map is one of the following, but **no option is selected here**:

### Boundary A: private per-invocation checked-authority/freshness context

A private context created and consumed inside one `run()` invocation, after the first full authority check, carrying only:

- exact State path+sha and checkpoint path+sha;
- the already-read four-ref artifact bytes and hashes;
- retention/completion identity and freshness pins;
- the last observed guard/slot state.

Every reuse would need to preserve the same invariants: exact State/checkpoint identity, same-record triplet, live file rehash, own-epoch Git proof, full content/report/proof/decision/retention checks, and a cheap freshness check at each write boundary. It must not become a global cache, a caller-verified dict, a public bypass flag, or a new schema/module. It must not survive across invocations or across a State/checkpoint/guard/slot change.

### Boundary B: call-shape duplication

Source-level exact duplicates that a bounded optimization would have to account for:

- `_verify_completion_full` calls the same AG twice at `low:1018` and `:1073`.
- The runner calls `resolve_research_authority` twice at `:264` and `:271` with no intervening write.
- `build_architecture_review_summary` loads the same upstream graph at `architecture:866` and again inside `validate_candidate_matrix`/`derive_candidate_matrix` at `:880`/`:373`.
- `_dm022_require_ready` is called at adjacent points `:440` and `:444` with only the review write between them; `:451` and `:456` similarly bracket the archive write.
- Within one `_load_upstream`, the same Evidence content is revalidated six times through direct/Views/Ledger/Completeness nesting.

This boundary is about removing redundant call paths, not about weakening freshness. The critical invariant is that any write-boundary freshness check remains, and that a changed State/checkpoint/guard/slot invalidates the reused result.

### Boundary C: missing call / missing cheap freshness

A different boundary is that the current code may be doing **full** graph verification where only a **cheap freshness** check is needed, or may be missing a single scoped check that would allow a narrower invariant. This document does not select that interpretation. It only records that the current source makes no distinction between:

- the first full authority check of an invocation, and
- repeated pre-write checks in the same invocation with no observed mutation.

Any candidate boundary must state explicitly which of these two it is optimizing, and must not claim that a repeated full check is unnecessary without preserving the exact State/checkpoint/triplet/guard/own-epoch/freshness predicates.

## 8. Timeout classification and minimal read-only probes

### Classification

From source alone:

- There is **no infinite loop** in the normal-writer call graph.
- The timeout is **most likely repeated I/O plus repeated JSON/card validation**, because the source shows 60 AG-equivalent work before W34's first matrix write and 92 AG-equivalent work for SP between the Architecture write and the Review Summary write. Each AG contains six Evidence content passes and three View content passes, and each Evidence pass pins/loads/rechecks every accepted task/result file and rechecks the supplement Raw closure.
- The saved preflight raw cannot distinguish disk I/O from CPU/JSON parsing from Git subprocess latency. It has no stack, no per-phase timing, and 0B stdout/stderr.
- A single exceptionally slow graph pass, filesystem/page-cache effects, memory pressure, or Git object latency are not excluded. The "repeated I/O" conclusion is a source-based likelihood, not a measured proof.

### Minimal read-only probe entries (recommendation only; not executed)

Use the shadow workspace only, no `run()`, no writes, no State changes. Probe in increasing cost and stop at the first over-budget result:

1. One AG:
   `low.resolve_research_authority(repo_root, state_path)`.
   This is read-only and exercises one AG plus resolver report/COPY/final recheck.
2. Three AGs:
   `agent.validate_agent_state(repo_root, cfg, state)`.
   This localizes the three nested PREARCH checkpoint proofs.
3. Two AGs:
   `low.require_research_operation_ready(repo_root, state_path)`.
   This localizes the completion double-AG.
4. Six AGs:
   `screening.resolve_active_screening_acceptance(repo_root, state_path, implementation_sha)`.
   This localizes the screening resolver's two state validations.
5. One EU:
   `architecture.derive_candidate_matrix(...)` with the exact PREARCH four-ref paths and implementation SHA.
   This should dominate if the matrix pre-write block is the W34 limit.
6. Two EU + one readiness gate:
   `architecture.build_architecture_review_summary(...)` on SP's three already-present partial slots.
   This localizes the SP post-Architecture block. It is read-only and does not overwrite the review summary.

Instrumentation for each probe:

- `timeout 90s` plus `/usr/bin/time -v` for wall/CPU/RSS.
- If available, `strace -f -c -e trace=file,read` to separate file I/O from CPU.
- Read `/proc/<pid>/io` at the 90s point if the process is still running.
- If available, `py-spy dump --pid <pid>` for the current Python stack.
- Use `PYTHONPATH=<shadow>`, `PYTHONDONTWRITEBYTECODE=1`, `GIT_NO_LAZY_FETCH=1`, and the same shadow root; do not use the active rehearsal.

The smallest decisive probe is (1) for each edition. If one `resolve_research_authority` is already near the 90s budget, the 60-AG pre-matrix block and the 92-AG post-Architecture block fully explain the 1200s timeout without any loop hypothesis. If (1) is fast but (2)/(3) are slow, the PREARCH state-validation multiplier is the dominant cost. If (1)-(3) are fast but (5)/(6) are slow, the `_load_upstream` EU multiplier is dominant.

## 9. Read-only preservation statement

Only this document was created. No source, State, Profile, checkpoint, completion, slot, Git object, index, or active rehearsal byte was read back, modified, or executed. All paths and line sites above are from the shadow source and the saved preflight report. No import, test, build, fixture, network, Git command, or subagent was used.
