# DM022 pre-Architecture — Task B pre-code map: schemas / producers / generation DAG

AUTHOR-side pre-code return, Task B only. No implementation, no runtime/import/tests/build/fixtures/restore/network/Git mutation/source writes. Human `ab84b4f`; root status scoped-clean with 55 inherited bare Gitlinks left untouched. Read-only source inspection of final93 applied proof-copy only.

Binding inputs:

- Selected decision `outputs/rephase-1-dm022-prearchitecture-contract-decision.md` **including §11**, SHA256 `a345bb9524b4dfc5b5f32600d0d708687e2b6131d91a43965c97b6418388f223` / 31351 B.
- Mandatory `notes/rephase-1-dm022-prearchitecture-contract/astra-review-resolution.md` **including §5** (FINAL-BINDING closeout, next-task §5).
- BOTH independent reviews WITH FINAL-BINDING addenda (authority + operation).
- Packet `notes/rephase-1-dm022-prearchitecture-contract/README.md`.
- `AGENTS.md` current entry (DM022 BOUNDED CONTRACT SELECTION COMPLETE; pre-code OPEN; B2/B4 OPEN at entry).
- Actual source: `actual 409b292 / tree 8ce36998 + 93 paths 40M53A / 742 files`, patch `f898d33b…` DIRECT409 `3423014B`, manifest `d488c6ee…`, available applied proof-copy `.rephase-1-editorial-runtime/versioned-renewal-packaging-final-depth-20261025T205432Z/proof-copy/candidate-partial-b40de60` read-only. No restore, no rehash, no new HEAD.

Author is not independent acceptance. The externally supplied author-independent research/authority-consumption decision is ingress; no new Sol/Human Gate, no genuine PASS generated inside the writer, no hash-only/raw rebind/caller-verified-dict/pending-flag permission.

This file closes **B4 as a concrete path/call map** (versioned-R producer outputs vs canonical overwrite refusal + exact content-validator entrypoints, no fabricated `CANDIDATES_NORMALIZED` State). It does **not** close B2 (full canonical-reader/guard-caller inventory), guard write-set/IO/resume oracles, HEAD/tree predicate proof, or Profile witness predicates — those are separate pre-code tasks. §16 lists the exact remaining OPEN items honestly. Implementation remains blocked until Astra + author-independent readiness review confirms the full §10 map.

All `file:line` below refer to the proof-copy unless stated as `workspace:`.

---

## 1. Task-B scope and non-goals

Task B delivers:

- exact new immutable Evidence/View accepted-run generation at **TRUE `EVIDENCE_REVIEWED`** (no fake `CANDIDATES_NORMALIZED` State, no post-`VALIDATED` renewal reuse);
- preservation rules for Profile/Discovery/Screening/old accepted graph, affected allowlist, versioned Ledger/Completeness under `R=<source_root>/research/v2/acceptance-revisions/<RID>`;
- current family-helper predicate preservation (package/task/card/view/ledger/completeness actual entrypoints);
- new Raw article `eventSource` authority-supplement rule vs new-Discovery refusal; explicit complete existing-obligation results (DM017);
- mechanical-vs-semantic classification with actual schema paths (no generic ignore-prefix);
- smallest concrete LOW/HIGH module split with exact names/signatures/imports (ROOT CHOICES, §8), no top cycle, LOW detached with no current-State validation;
- all NEW schema paths with full strict required/conditional fields and self-vs-FILE digest expressions;
- source-epoch/current-tool/HEAD-tree refs, checkpoint kind `PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1` with truthful `EVIDENCE→EVIDENCE` operation + separate `CANDIDATES→EVIDENCE` producer boundary (4 artifacts / 3 checkpoints), before-COPY/parent/anchor/retention/review/proof, current-vs-history typed report;
- State-schema-unchanged rule + existing checkpoint-schema branch integration (`artifacts` compatible, no fictional `OldCoreStageReport`);
- import DAG with no self/future-SHA cycles + guard-owner coordination;
- fully typed refs (normalized path, sha, size, known enum), duplicate-field equality explicit;
- current source/tool commit rule + artifact-only descendant allowlist;
- exact producer funcs for arbitrary-R paths + stale-before-State proof handling.

Out of scope for Task B (remain OPEN, not “review later” for must-have — see §16): full B2 caller enumeration with refuse-or-rewire dispositions per call site, seven-slot writer/ownership/fault oracles, guard state-machine + check sites, phase HEAD/tree complete path set, owned IO/resume oracles, Profile witness allowlists (supported source-type lists, named-obligation rows, archived-HTML + retrieval provenance shape).

---

## 2. Generation at TRUE `EVIDENCE_REVIEWED` — what is proved, what is refused

### 2.1 Eligibility (HIGH-side only)

New HIGH operation requires, by re-reading pinned LIVE State (not a synthetic lifecycle):

- `agent.validate_agent_state(repo_root,cfg,state)==[]` (`survey_agent_control_v2.py:597-600,602-748`) with strict public predicates, exact `checkpoint_provenance.{evidence,materiality,completeness}` present and `machine_checkpoints` passed, `lifecycle_state==EVIDENCE_REVIEWED`, Selection/Architecture/Draft/validation/publication-preview/Freeze/Release checkpoints pending with `provenance==null`, `human_gates.architecture_review==pending` with `human_gate_provenance.architecture_review==null`, no recorded Human review/index row or presented immutable request, `exception_gate.status==inactive`, publication revalidation `null`.
- Same checks as `run_selection_architecture_v2_interactive.py:164-168` (`validate_agent_state` then `lifecycle_state==EVIDENCE_REVIEWED`), plus decision §3 window: same issue/Profile bytes/paths/initialization, passed Discovery/Screening/Evidence/Materiality/Completeness with valid checkpoint provenance (four artifacts from same producer checkpoint), affected allowlist nonempty/unique/subset of already-known non-DROP IDs, no new Discovery IDs, no changed Screening decisions.
- Current tool pins: `core.repository_commit_sha(repo_root)` (`survey_production_v2.py:189-207`), `core.contract_identity(...)` (`:210-228`), `core.sha256_file` on Profile/State/Discovery/Screening/Evidence/Views/Ledger/Completeness files. Old Evidence tool commit is **historical provenance** inside the old checkpoint `implementation` field, never re-required at authority time.

Refused pre-adoption (fail closed, preserve owned inert prep if any):

- any `CANDIDATES_NORMALIZED` interactive runner invocation with a fabricated State (`run_evidence_v2_interactive.py:599-603` requires `CANDIDATES_NORMALIZED`; DM022 HIGH must **not** call it with a synthetic old lifecycle — see §8);
- `transition_state` same/backward (`survey_production_v2.py:1014-1015` refuses non-monotonic);
- pending-Architecture operator invalidation or Human `REQUEST_CHANGES` unless its real gate/review conditions are naturally met (decision §2, R1);
- legacy `revise_*_interactive_evidence` Core-v2 rebinding (operates `sources/<issue>/pipeline-state.json`, not `production-state.json`);
- post-`VALIDATED` editorial/renewal reuse (`survey_versioned_renewal_v2.py:560-590` window, `run_evidence` renewal helpers are not DM022 admission APIs).

### 2.2 No State recursion in proof

Deterministic proof leaf (LOW) must **never** call `agent.validate_agent_state`, `agent.verify_agent_state_basis`, `agent.resolve_checkpoint_artifact`, `agent.resolve_active_evidence_views`, `core.verify_state_basis`, or `core.repository_commit_sha` as authority. It validates **proposed bytes** via pure file/SHA/schema/content checks (§5 helpers). LIVE eligibility + guard checks are HIGH-side only. Historical/detached validation uses retained before-State/lineage, never demands live State still equal before-State (decision §11.2).

---

## 3. Preserve / produce / versioned-R layout

### 3.1 Before graph and retained inputs (HIGH owns, LOW verifies)

HIGH reloads canonical State→passed-checkpoint→typed-artifact graph: package/task/card/result/View files, Discovery/Screening/X/raw/supplement provenance, Ledger/Completeness + criteria/prompt/schema bindings (`survey_evidence_v2.py` basis fields + `survey_completeness_v2.py` extra checks). All content-addressed accepts + original checkpoint bytes stay at original paths. HIGH copies mutable before-State + every present targeted unaccepted canonical output into a new owned retention root; records exact present/absent inventory + source refs. Old reviewed targets are never rebound by equal-byte copy. Exact retention-root path/manifest schema is guard/IO-task scope, referenced here only as `retention_plan` refs (§10).

### 3.2 Candidate accepted graph under `R`

Immutable namespace (decision §4):

```text
R = <source_root>/research/v2/acceptance-revisions/<revision_id>
```

- `<revision_id>` safe single segment (no `/`, no `..`, no symlink), Profile-derived root, no latest-scan selection.
- Truthful new package/task/result inputs bound to actual pre-revision State + existing Discovery/Screening. No fake `CANDIDATES_NORMALIZED` execution.
- New Evidence/View accepts: content-addressed new runs under owned revision namespace; **unchanged complete runs reused only at exact validated immutable refs** (same `evidence-accepted.json` / `edition-views-accepted.json` bytes + same `result_set_sha256` / `view_set_sha256` dir names — see §5 digests). Changed cards/Views always produce a newly validated **complete** acceptance (all non-DROP IDs), never a partial overlay interpreted as accepted.
- Ledger/Completeness: **newly generated versioned files under R** (B4 — see §4). Old canonical `materiality-ledger-v2.json` / `profile-completeness-v2.json` stay byte-identical and become inactive only after State adoption; no canonical overwrite/rebind-by-hash.
- Per affected ID: bind old/new full content + reason, newly retained Raw with source/event/clock semantics. New official article requires preserved bytes/provenance (URL, `fetched_at`, SHA, `byte_count`, `datePublished` event meaning), never a Summary quotation as evidence.
- Screening `INSPECT` preserved only where `survey_evidence_v2.validate_evidence_card` + `validate_edition_view:1437-1491` + ledger predicates actually allow (non-DROP, valid task association, `VERIFIED/PARTIAL→MATERIAL` etc.); never promoted to KEEP/MATERIAL by label; no automatic HOLD→MATERIAL/SELECTED (`survey_architecture_v2_base.py:526-527` still refuses HOLD→SELECTED).

### 3.3 Raw supplement vs new Discovery

- New Raw article authority uses **Evidence Authority Supplement** (`schemas/evidence-authority-supplement-v2.schema.json`; `survey_evidence_v2.py:212-376`): `basis={source_root,discovery_path/discovery_sha256,screening_acceptance_path/screening_acceptance_sha256}`, each `sources[]` row has `supplement_source_id ^supplement-src-[0-9a-f]{16}$`, `discovery_id`, `evidence_task_id==stable_task_id(issue_id,discovery_id)`, `locator`, `source_type→source_class` via `_source_class` (`:177-184`), `title`, `published_at`/`accessed_at` (RFC3339, `parse_instant`), `raw_path` (repo-relative under `source_root`, non-empty, `byte_count` + `raw_sha256` exact), `relation` (e.g. `hosted-article-event …`). Validated by `validate_evidence_authority_supplement`; bound per-task via `task_authority_sources (:413-446)` + `_supplement_entries_for_package (:379-410)`; package carries `authority_supplement={path,sha256}` + `contracts.supplement`.
- Supplement rows must target **existing non-DROP Discovery tasks**; `DROP` targeting refused (`:300-301`). Supplement does **not** create Discovery IDs. Any new Discovery ID or changed Screening decision requires an earlier regeneration contract and is refused by this bounded operation (decision §3).

### 3.4 Completeness: union, not builder default

DM017: `run_evidence_v2_interactive._build_completeness:471-507` iterates **only** `profile.research_scope.initial_obligations`; `_validate_completeness_input:217-258` enforces `set(by_id)==initial_ids` (extra/missing both refuse). The unchanged full guard `survey_completeness_v2.validate_profile_completeness:265-290` additionally requires every Profile-initial **and** every Discovery-named obligation with traceability (`_check_profile_completeness_extra_content:145-238`), plus Thematic closure derived from Discovery provenance (`_thematic_closure_errors:81-142`).

DM022 therefore:

- must **not** silently call the incomplete builder and claim completeness;
- must consume **explicitly provided complete obligation results** (supplied decision + interactive revision request carry per-obligation `status`/`rationale` for the union of initial + named IDs — see §9 request schema);
- must build obligations with a new LOW builder that enumerates the union (initial + `provenance.obligation_ids` over all Discovery records), derives `discovery_ids` (declaring DIDs) + `evidence_task_ids` (via ledger), preserves `dimension`/`description` from Profile for initial IDs, and validates with the **unchanged** `validate_profile_completeness` + `schema_gate.validate_instance(..., profile-completeness-result.schema.json)`.

---

## 4. B4 closure — versioned-R producer paths vs canonical overwrite refusal (CLOSED by this map)

Existing refusal (source-grounded, not re-decided):

- `survey_evidence_v2.write_materiality_ledger:1797-1801` refuses if `path.exists()`; `run_evidence_v2_interactive:715-717` refuses canonical `materiality-ledger-v2.json` overwrite; `:730-732` refuses canonical `profile-completeness-v2.json` overwrite; `accept_evidence_results:1190-1194` / `accept_edition_views:1532-1538` refuse incomplete pre-existing content-addressed dirs and return only after revalidation.

B4 required: versioned write paths + checkpoint artifact refs showing canonical files stay byte-identical and go inactive via provenance switch (not overwrite), with exact present/absent inventory and source refs. This map closes it as follows (implementation still needs readiness confirmation, but no further design choice remains):

| Producer output | Existing func (arbitrary-path capable, cited — do NOT invent wrappers) | DM022 versioned path (ROOT CHOICE, fixed — no budget beyond these) | Canonical path (must stay byte-identical until adoption; never written here) |
|---|---|---|---|
| Evidence run package (transient build dir) | `survey_evidence_v2.prepare_evidence_package(repo_root,state_path,discovery_path,screening_acceptance_path,output_dir,implementation_sha,supplement_manifest_path)` (`:539-681`) — basis includes `state_path/state_sha256`, `discovery/screening` SHAs, `prompt/contracts/tasks`; per-DID task via `stable_task_id` + `task_filename` | `R/work/evidence-package/package.json` + `R/work/evidence-package/tasks/task-<20hex>.json` (LOW detached variant binds `basis.state_path` to retained before-State COPY path, see §8 — not canonical live State) | n/a (transient, never canonical) |
| Evidence acceptance | `survey_evidence_v2.accept_evidence_results(repo_root,package_path,results_dir,accepted_root,implementation_sha)` (`:1159-1213`): `accepted_root` is already a parameter; digest `_evidence_result_set_digest(package_sha,entries)` (`:1152-1156`); `run_dir=accepted_root/result_set_sha256`, `acceptance_path=run_dir/evidence-accepted.json`; idempotent iff revalidates | `accepted_root = R/evidence/v2/accepted`; `run_dir=R/evidence/v2/accepted/<result_set_sha256>/`, files `package.json`, `tasks/*`, `results/*`, `evidence-accepted.json` (+ archived `interactive-evidence.json` + `interactive-audit.json` per `_archive_input` shape in runner `:562-583`, adapted to R) | never `source_root/evidence/v2/accepted` rewrite; old accepts immutable |
| Edition Views acceptance | `survey_evidence_v2.accept_edition_views(repo_root,profile_path,evidence_acceptance_path,views_dir,accepted_root,implementation_sha)` (`:1498-1552`): `accepted_root` is a parameter; digest `_view_set_digest(rows)` (`:1494-1495`); `run_dir=accepted_root/view_set_sha256`, `acceptance_path=run_dir/edition-views-accepted.json` | `accepted_root = R/evidence/v2/views/accepted`; `run_dir=R/evidence/v2/views/accepted/<view_set_sha256>/`, files `views/view-<20hex>.json`, `edition-views-accepted.json` | never old views dirs rewrite |
| Materiality Ledger (versioned file) | `survey_evidence_v2.build_materiality_ledger(repo_root,profile_path,discovery_path,screening_acceptance_path,evidence_acceptance_path,views_acceptance_path,implementation_sha)` (`:1579-1655`) returns dict + `validate_materiality_ledger` (`:1771-1794`); `write_materiality_ledger(path,ledger)` (`:1797-1801`) takes arbitrary `path` and refuses overwrite | `R/materiality-ledger-v2.json` via `write_materiality_ledger(R/…,ledger)` (LOW builds via State-free content core §8, HIGH writes once with exclusive-create + post-write re-hash) | `source_root/materiality-ledger-v2.json` (read-only input; `run_selection_architecture:176` reads it — B2 must rewire, not this task) |
| Profile Completeness (versioned file) | LOW new builder (union, §3.4) + `survey_completeness_v2.validate_profile_completeness(result,repo_root,profile_path,discovery_path,screening_acceptance_path,evidence_acceptance_path,views_acceptance_path,ledger_path,implementation_sha)` (`:265-290`) + `schema_gate.validate_instance(result, repo_root/schemas/profile-completeness-result.schema.json)` (runner `:742-746` pattern); write via `core.write_json(path,result)` (runner `:761` pattern, but under R with refuse-if-exists) | `R/profile-completeness-v2.json` (refuse if exists; `basis.materiality_ledger_sha256==sha256(R/ledger)`, `basis.production_profile_sha256==sha256(profile)`) | `source_root/profile-completeness-v2.json` (read-only input; runner `:177` reads it — B2 must rewire) |

Why this is the smallest sufficient set: all five producer funcs already accept arbitrary output roots/paths (no code-shape invention); only the **call sites** change from canonical constants (`run_evidence_v2_interactive:667,697,715,730`; `run_selection_architecture:176-177`) to explicit R paths. No new ledger/completeness schemas (existing `materiality-ledger.schema.json`, `profile-completeness-result.schema.json` validate versioned files unchanged). Canonical files are read as **before-inputs** for proof and stay pinned; after adoption the State triplet points at R (via new checkpoint `artifacts`), so normal consumers must resolve via the new checkpoint (B2), never fall back to old singleton paths.

Later loaded-proof stale-before-State handling (same funcs, State-free layer — no new shapes):

- package: `_validate_evidence_package_basis_content(repo_root,package_path,package,expectations,root_records,root_path)` (`:839-895`) — enforces `basis.state_path==canonical_state_path` identity without live SHA equality, checks profile/discovery/screening/prompt/contract drift, tasks/supplement via `_check_evidence_tasks_content (:769-836)`; never loads State, never calls `verify_state_basis`/`repository_commit_sha`.
- evidence: `_validate_evidence_acceptance_content` (`:1255-1283`) + `_check_evidence_acceptance_results_content` (`:1216-1253`) — verifies `package_sha256`, `screening_acceptance_sha256`, per-task/file SHAs, `validate_evidence_card` per card, `result_set_sha256==dirname` content-addressed identity.
- views: `_validate_edition_views_acceptance_content` (`:1322-1349`) + `_check_views_acceptance_rows_content` (`:1286-1319`) — verifies `profile_sha256`, `evidence_acceptance_sha256`, exact task coverage, per-view bytes, `validate_edition_view`, `view_set_sha256==dirname`.
- ledger: `_validate_materiality_ledger_content` (`:1725-1768`) + `_check_ledger_rows_content` (`:1658-1723`) — verifies 7-hash basis + exactly-one-row-per-Discovery + DROP/non-DROP disposition rules.
- completeness: `_validate_profile_completeness_content` (`survey_completeness_v2.py:241-262`) = `_validate_completeness_content` (`survey_evidence_v2.py:1915-1941`) + `_check_profile_completeness_extra_content` (`:145-238`) — verifies basis, obligation shape/identity/traceability, Thematic closure derivation.
- supplement: `validate_evidence_authority_supplement(...,implementation_sha=None, screening_acceptance=…, discoveries=…)` (`:212-324`) in State-free mode (no `validate_screening_acceptance` with impl SHA).

HIGH resume/adoption must reload the **recorded before-State bytes** (retained COPY) and re-run these State-free validators against R, then separately validate LIVE State eligibility (§2.1). If LIVE State ≠ recorded before bytes and ≠ recorded expected-after bytes (or unreadable ownership), INDETERMINATE — preserve, no restore/delete/adopt (decision §7).

---

## 5. Family-helper predicate preservation (actual entrypoints — no caller dicts)

| Family | New-R producer path uses | Must preserve (actual predicates, not summaries) |
|---|---|---|
| Package | `prepare_evidence_package` shape + State-free `_validate_evidence_package_basis_content` / `_check_evidence_tasks_content` | `evidence-v2-run-package.schema.json`: `basis.{profile_path/profile_sha256,state_path/state_sha256,discovery_path/discovery_sha256,screening_acceptance_path/screening_acceptance_sha256}` exact; `prompt.path==config/prompts/evidence-verification-v2.md`; `contracts.{run_package,task,card}(+.supplement iff supplement)` const paths + SHAs; `tasks[].{evidence_task_id,path ^tasks/task-[0-9a-f]{20}\.json$,sha256,discovery_ids[1],?authority_supplement_source_ids}`; `expected_outputs=={one_result_per_task:true,filename_rule:same-basename-as-task}`; task filenames `task_filename(task_id)` (`:472-474`), `stable_task_id(issue_id,discovery_id)` (`:467-469`); non-DROP exactly-once coverage; supplement bound exactly once per task (`:819-835`). |
| Card | `validate_evidence_card(card,task,task_sha,package)` (`:965-…`) + `_check_evidence_acceptance_results_content` | `evidence-v2-card.schema.json` exact `CARD_KEYS` (`:32-36`); `basis=={task_sha256,screening_acceptance_sha256,prompt_sha256,result_contract_sha256}`; `status∈{VERIFIED,PARTIAL,REJECTED,NEEDS_MORE}` with REJECTED→view NON_MATERIAL / NEEDS_MORE→HOLD coupling; entities/artifact/temporal/events/sources/claims/metrics/limitations/verification subject/role/source binding (`:949-…` continuation); `task_authority_sources` Discovery-bounded + supplement-only sources (`:413-446`). No source-type alias relabelling: `_source_class` (`:177-184`) + `SOURCE_CLASS_MAP` (`:44-109`) authoritative; `run_evidence_v2_interactive.SOURCE_CLASS_MAP (:38-45)` 6-entry map is runner-local — DM022 witnesses must use genuinely supported types and report DM016 non-closure (decision §8). |
| View | `validate_edition_view(view,profile,evidence_sha,evidence_status)` (`:1437-1491`) + `_check_views_acceptance_rows_content` | `edition-evidence-view.schema.json`: `evidence_task_id`, `evidence_sha256==sha256(card file)`, `materiality.{status∈{MATERIAL,CONTEXT,NON_MATERIAL,HOLD},rationale}`, `scope_dimensions⊆profile.research_scope.scope_dimensions`, `profile_annotations` per Profile (WEEKLY `{why_this_issue,window_relation∈{MAIN_EVENT,…},carry_over}` / THEMATIC `{lineage_role,branch_ids,transition_ids,inheritance_note,historical_attribution_caveat}` / PERIOD `{period_role,chronology_relevance}`); `evidence_acceptance_sha256==sha256(evidence-accepted.json)`, `profile_sha256==sha256(profile)`, exact task coverage, `view_set_sha256==dirname`. |
| Ledger | `build_materiality_ledger` / `validate_materiality_ledger` / `_validate_materiality_ledger_content` + `_check_ledger_rows_content` | `materiality-ledger.schema.json`: `basis` 7 SHAs (`production_profile/discovery/screening_acceptance/evidence_acceptance/edition_views_acceptance/evidence_set/edition_view_set`); `rows[]` exact `{discovery_id,origin,screening_decision∈{KEEP,MAYBE,DROP,INSPECT},downstream_disposition∈{MATERIAL,CONTEXT,NON_MATERIAL,HOLD,DUPLICATE,EXCLUDED},evidence_task_ids,evidence_view_statuses,duplicate_group,rationale}`; exactly one row per Discovery; DROP→`EXCLUDED` (or `DUPLICATE` iff `duplicate_group`) with no tasks; non-DROP exactly one task + View disposition; `rationale==Screening=…; Edition View=…` shape preserved (builder `:1625`). |
| Completeness | `validate_profile_completeness` + `_validate_profile_completeness_content` + `_check_completeness_result_content` + `_check_profile_completeness_extra_content` | `profile-completeness-result.schema.json`: `basis=={production_profile_sha256,materiality_ledger_sha256}`; `overall_status` derived (`INCOMPLETE` iff any `NEEDS_RESEARCH` else `LIMITED` iff limitations/residual else `READY`); `obligations[]` exact 7 keys (`survey_completeness_v2.OBLIGATION_KEYS`), `status∈{SATISFIED,LIMITATION,NEEDS_RESEARCH,NOT_APPLICABLE}`, unique IDs, `discovery_ids⊆ledger DIDs`, `evidence_task_ids⊆ledger task IDs`, `dimension∈profile.scope_dimensions`; initial union + named-Discovery union with declaring-DID traceability; Thematic `closure` 8 keys with provenance-derived counters (`expansion_passes==max(1,max_pass)`, final-pass counts from `research_pass==max_pass`, `open_material_obligations==NEEDS_RESEARCH count`, `status` mapping, gap-fill/limitation rules). |

No CALLER-verified dicts, no generic `pending` bypass, no `production.verify_state_basis` substitution (distinct globally-current-pinned API, decision §11.2 / R2).

---

## 6. Independent supplied decision (immutable files only)

The externally supplied author-independent research/authority-consumption decision binds the exact before/after graphs, affected IDs, Raw/event semantics and claimed interpretation. It is the existing reasoning responsibility (ingress), not a new gate. It must be an immutable file bundle referenced by hash, never a live fetch or caller dict:

- `decision_path` (repo-relative normalized) + `decision_sha256` + `byte_count`;
- `before_*` refs: before-State COPY, before Evidence/Views/Ledger/Completeness acceptances + package/task files, Discovery JSONL + Screening acceptance, Profile — each `{path,sha256,byte_count}`;
- `after_*` refs: proposed R package/tasks/cards/views/ledger/completeness + supplement manifest — each `{path,sha256,byte_count}`;
- `affected_ids` allowlist (sorted unique, subset non-DROP — checked against Screening decisions + ledger rows);
- `raw_refs`: each new Raw `{raw_path,raw_sha256,byte_count,url,fetched_at,published_at(event meaning),relation}`;
- `interpretation`: per-affected-ID `{old_content_sha,new_content_sha,reason_kind,event_semantics}` with `reason_kind∈{HOSTED_ARTICLE_EVENT_CORRECTION,…}` (closed enum in request schema, no free-text authority);
- `reviewer`: `{executor,recorded_at}` (informational; authority comes from file binding + revalidation, not role string).

The writer must **not** generate a genuine PASS record; the supplied decision is validated (hashes re-hashed, allowlist checked, Raw bytes re-read, Ledger/Completeness revalidated) but never mutated into a writer PASS.

---

## 7. Mechanical-vs-semantic classification (no generic ignore-prefix)

Unaffected IDs are those **not** in `affected_ids`. Their proposition/status/rationale/content must be **fully equal**; only explicitly listed mechanical SHA propagations may differ. Every mechanical projection must be mapped per-field below, never excluded by directory prefix (decision §4).

### 7.1 Mechanical (permitted to differ; must be listed in proof `mechanical_projections`)

- `evidence-accepted.json`: `result_set_sha256`, `package_sha256` (package lists affected task SHAs), `evidence_acceptance_sha256` file SHA, `parent dirname==result_set_sha256` — all change when any affected task changes; per-row `sha256` for **unaffected** rows must equal old bytes.
- `edition-views-accepted.json`: `view_set_sha256`, `evidence_acceptance_sha256`, file SHA, `dirname==view_set_sha256` — same propagation; unaffected `view_sha256` must equal old bytes.
- `materiality-ledger-v2.json` (R): `basis.{evidence_acceptance_sha256,edition_views_acceptance_sha256,evidence_set_sha256,edition_view_set_sha256,materiality_ledger_sha256(self — see §10)}` change mechanically; unaffected `rows[]` semantic fields must be byte-equal (see §7.2).
- `profile-completeness-v2.json` (R): `basis.materiality_ledger_sha256` changes mechanically; unaffected obligation `status/rationale/discovery_ids/evidence_task_ids` must be equal unless the obligation references an affected DID/task (then it is affected, see §7.3).
- Run-dir names (`<result_set_sha256>`, `<view_set_sha256>`) and `R` revision-id path segment — mechanical by construction.
- `package.json`: `tasks[].sha256` for affected tasks only; `basis.state_sha256` points at retained before-State COPY (different path/SHA by design — recorded explicitly, not a silent drift).

### 7.2 Unaffected semantic equality (must hold byte-for-byte unless listed above)

- Card (`evidence-v2-card.schema.json`): `status,entities,artifact,temporal.events,sources,claims,metrics,limitations,verification` — full equality (file SHA equality is the check: `core.sha256_file(path)==row.sha256`).
- View (`edition-evidence-view.schema.json`): `materiality.status/rationale,scope_dimensions,profile_annotations,evidence_sha256` — full equality.
- Ledger row (`materiality-ledger.schema.json:31-42`): `discovery_id,origin,screening_decision,downstream_disposition,evidence_task_ids,evidence_view_statuses,duplicate_group,rationale` — full equality for unaffected DIDs.
- Completeness obligation (`profile-completeness-result.schema.json:23-37`): `dimension,description,status,discovery_ids,evidence_task_ids,rationale` — full equality for obligations not referencing affected DIDs/tasks; `overall_status/residual_limitations/closure` must still re-derive consistently (if they change only due to affected rows, the proof must show the derivation).

### 7.3 Affected permitted fields (actual schema paths/tables — NOT generic `ignore_paths`)

Only these may differ for `discovery_id ∈ affected_ids` (all other fields must equal old or be mechanical per §7.1):

- `evidence-v2-task.schema.json`: `source_records` unchanged (Discovery-bounded); `authority_supplement_source_ids` may gain exactly the new supplement IDs bound to this task; `screening_basis` unchanged (Screening decisions immutable).
- `evidence-v2-run-package.schema.json:88-102 tasks[]`: `sha256` for affected `evidence_task_id` only; `authority_supplement_source_ids` for affected tasks only.
- `evidence-v2-card.schema.json`: `status`, `entities[]`, `artifact`, `temporal.events[]` (new `SOURCE_PUBLICATION_OR_RELEASE` with `event_date==published_at`), `sources[]` (new supplement `source_id` with `url/title/published_at/accessed_at/role==Post-Screening exact authority supplement: …`), `claims[]`, `metrics[]`, `limitations[]`, `verification.targets[].{status,finding}` + derived `unresolved_questions/contradictions`; `basis.task_sha256` (new task SHA), `basis.screening_acceptance_sha256` unchanged, `issue_id/evidence_task_id` immutable.
- `edition-evidence-view.schema.json`: `evidence_sha256` (new card SHA), `materiality.status/rationale`, `scope_dimensions` (must stay ⊆ Profile), `profile_annotations` (per-Profile shape preserved); `issue_id/research_profile/evidence_task_id` immutable.
- `materiality-ledger.schema.json:31-42` row for affected DID: `downstream_disposition`, `evidence_task_ids` (same stable IDs — IDs don’t change, bytes do), `evidence_view_statuses`, `rationale` may change; `discovery_id,origin,screening_decision,duplicate_group` immutable (Screening frozen).
- `profile-completeness-result.schema.json:23-37` obligations referencing affected DIDs/tasks: `status,rationale,evidence_task_ids` (task IDs same, statuses may change), `discovery_ids` (declaring set unchanged — Discovery frozen; only `evidence_task_ids` linkage re-derived); `dimension/description/obligation_id` immutable; `overall_status/residual_limitations/closure` re-derived via unchanged rules.
- Raw supplement (`evidence-authority-supplement-v2.schema.json:41-70`): **new rows only** for affected DIDs; no mutation of existing Discovery/Screening rows.

Any other difference (e.g. `origin` change, `screening_decision` change, `discovery_id` rename, `dimension` change, `source_class` alias fix, new Discovery ID) is a refusal, not a projection.

---

## 8. Smallest LOW/HIGH split (PROPOSED ROOT CHOICES — reasons inline)

Names below are **author-proposed fixed names** requiring Astra/root confirmation; no arbitrary file budget beyond these two modules + four schemas (§9). Reasons: follow existing `survey_*_v2.py` / `run_*_v2_interactive.py` shape, keep LOW leaf-detached (renewal Layer-A precedent), keep HIGH as the sole LIVE/guard/State owner.

### 8.1 LOW — detached content-only (no State, no HEAD, no guard)

**PROPOSED ROOT CHOICE:** `scripts/survey_dm022_revision_content_v2.py`

Reason: mirrors `survey_versioned_renewal_source_v2.py` Layer-A role; name states DM022 revision content without implying authority.

Imports allowed (leaf — no cycle): `core`, `schema_gate`, `survey_evidence_v2 as evidence`, `survey_screening_v2 as screening`, `survey_completeness_v2 as completeness`, `survey_discovery_v2 as discovery` (for `read_jsonl`/`validate_discovery_set` only). **Must not** import `survey_agent_control_v2`, `survey_agent_tool_v2`, `survey_production_v2.verify_state_basis` (call), `survey_human_gate_v2`, operator/bridge modules.

Exact proposed signatures (existing-shape conventions, `Path` + explicit refs, no bare `dict` placeholders):

```python
def build_revision_package(
    repo_root: Path,
    profile_path: Path,
    before_state_copy_path: Path,
    discovery_path: Path,
    screening_acceptance_path: Path,
    supplement_manifest_path: Path | None,
    output_dir: Path,  # R/work/evidence-package
) -> Path  # returns package.json path; writes tasks/task-<20hex>.json
def build_revision_cards_views(
    repo_root: Path,
    package_path: Path,
    revision_request_path: Path,  # §9 request (interactive records + completeness explicit results)
    results_dir: Path,  # temp, caller-owned
    views_dir: Path,    # temp, caller-owned
) -> tuple[Path, Path]  # (results_dir, views_dir) with one file per non-DROP task, validated via validate_evidence_card / validate_edition_view
def accept_revision_evidence_views(
    repo_root: Path,
    package_path: Path,
    results_dir: Path,
    views_dir: Path,
    profile_path: Path,
    evidence_accepted_root: Path,  # R/evidence/v2/accepted
    views_accepted_root: Path,     # R/evidence/v2/views/accepted
) -> tuple[Path, Path]  # (evidence-accepted.json, edition-views-accepted.json) via accept_evidence_results / accept_edition_views
def build_versioned_ledger(
    repo_root: Path,
    profile_path: Path,
    discovery_path: Path,
    screening_acceptance_path: Path,
    evidence_acceptance_path: Path,  # R path
    views_acceptance_path: Path,     # R path
) -> dict[str, Any]  # via _validate_*_content + _check_ledger_rows_content (State-free); caller writes via write_materiality_ledger(R/…)
def build_versioned_completeness(
    repo_root: Path,
    profile_path: Path,
    discovery_path: Path,
    screening_acceptance_path: Path,
    evidence_acceptance_path: Path,  # R path
    views_acceptance_path: Path,     # R path
    ledger_path: Path,               # R path
    completeness_input: dict[str, Any],  # union explicit results from request
) -> dict[str, Any]  # union builder (§3.4) + _check_completeness_result_content + _check_profile_completeness_extra_content; caller validates via validate_profile_completeness + schema_gate then writes R/…
def validate_revision_graph(
    repo_root: Path,
    profile_path: Path,
    discovery_path: Path,
    screening_acceptance_path: Path,
    evidence_acceptance_path: Path,  # R path
    views_acceptance_path: Path,     # R path
    ledger: dict[str, Any],
    completeness: dict[str, Any],
    expectations: dict[str, Any],  # {issue_id, research_profile, canonical_state_path}
) -> list[str]  # State-free full revalidation (package + evidence + views + ledger + completeness + supplement binding); [] == PASS
def compare_affected_unaffected(
    old_ledger: dict[str, Any],
    new_ledger: dict[str, Any],
    old_completeness: dict[str, Any],
    new_completeness: dict[str, Any],
    affected_ids: set[str],
) -> list[str]  # §7 checks; mechanical projections listed explicitly, no prefix exclusion
```

LOW rules: no `validate_agent_state` / `verify_state_basis` / `repository_commit_sha` / `resolve_checkpoint_artifact` / `current_stage_basis_override` usage; file SHA via `core.sha256_file`, object digests via `core.sha256_object`; schema via `schema_gate.validate_instance` / `load_and_validate_json`; path safety via `_repo_file`/`_repo_output_path` shapes (no traversal/symlink).

### 8.2 HIGH — coordinated LIVE operation (sole State/guard/retention owner)

**PROPOSED ROOT CHOICE:** `scripts/run_dm022_revision_v2_interactive.py`

Reason: follows `run_evidence_v2_interactive.py` / `run_selection_architecture_v2_interactive.py` interactive-runner shape; name states DM022 revision with explicit interactive (supplied-decision + request) semantics.

Imports allowed: `core`, `agent (survey_agent_control_v2)`, `agent_tool`, `low (survey_dm022_revision_content_v2)`, `evidence`, `screening`, `completeness`, `discovery`, `schema_gate`, `architecture` (for post-adoption regeneration readiness only — no write here), stdlib (`argparse/json/shutil/tempfile/pathlib`). Must not be imported by LOW or by `survey_agent_control_v2` (one-way: HIGH→agent, HIGH→LOW, agent→LOW allowed for future resolver branch — no cycle).

Exact proposed entrypoints:

```python
def run(
    repo_root: Path,
    state_path: Path,          # canonical production-state.json (LIVE, pinned)
    request_path: Path,        # §9 revision request (immutable file)
    decision_path: Path,       # §6 supplied decision bundle (immutable file)
    revision_id: str,          # safe single segment; R derived from Profile source_root
) -> dict[str, Any]  # {revision_id, R, evidence_acceptance, views_acceptance, ledger, completeness, checkpoint, report} rel paths + SHAs
def resume(
    repo_root: Path,
    state_path: Path,
    revision_id: str,
) -> dict[str, Any]  # explicit resume per §7 table (reloads record/graph/COPY/guard; may switch or clear or return ALREADY_ACTIVE)
def verify_before_state(...) -> ...  # pinned LIVE eligibility (§2.1) + before-COPY inventory re-hash
```

HIGH owns: pin-current-basis (HEAD/tree/contract + live evidence pins), retain COPYs/inventory, claim/revalidate guard (guard file/shape owned by guard task — HIGH only checks + coordinates, never invents a second authority), invoke LOW for candidate outputs, bind supplied decision, run LOW proof, complete typed checkpoint (§10), prevalidate expected State, perform single-file State triplet switch, checked clearing of old slots (seven, decision §11.1 — writer/ownership/fault oracles are guard-task scope, HIGH calls the coordinated writer), postread/inventory verification, release guard, return typed report (§11). HIGH validates LIVE State via `agent.validate_agent_state` + `core.repository_commit_sha(repo_root)` (actual current work-branch HEAD); LOW never does.

### 8.3 Shared authority consumer (Owner A)

**Owner A = `scripts/survey_agent_control_v2.py`** (existing, no new file). Future resolver branch for the new kind lives **inside** this file (not a new importer), calling LOW State-free validators for historical/detached proof and enforcing same-record triplet + lineage. Import direction: `survey_agent_control_v2 → survey_dm022_revision_content_v2` (for pure checks only) is permitted; reverse is forbidden. HIGH→agent + HIGH→LOW completes the DAG with no top cycle:

```text
LOW (leaf) ← agent (Owner A) ← HIGH (coordinator)
LOW ← HIGH (direct)
(no LOW→agent, no LOW→HIGH, no agent→HIGH)
```

---

## 9. NEW schemas (exact paths — PROPOSED ROOT CHOICES)

All paths repo-relative. All refs fully typed as `{path,sha256,byte_count}` (+ `kind` enum where the artifact role matters). `path` must satisfy `core.repo_local_path` safety (relative, no `..`, no `\`, no symlink traversal; resolved stays under `repo_root`). `sha256` is `^[0-9a-f]{64}$`; `byte_count` is `integer ≥1` and must equal `stat().st_size`. No bare `object`/`...`/`CHECKED` placeholders; every duplicate metadata field states equality explicitly (e.g. `package_sha256 == sha256(package file) == acceptance.package_sha256`).

Digests: `SELF` = `core.sha256_object(canonical JSON without self field)`; `FILE` = `core.sha256_file(path)`. Checkpoint/proof/report state both and require `SELF == recomputed` + every `FILE == recorded sha256` + `byte_count == stat`.

### 9.1 `schemas/dm022-revision-request-v2.schema.json` (NEW)

Immutable revision request (author-prepared, independently reviewed — not authority until validated).

Required: `schema_version=="2.0-rc1"`, `issue_id`, `revision_id` (safe segment `^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$`), `research_profile∈{WEEKLY,THEMATIC}` (initial witnesses; other Profiles refused), `before_state={path,sha256,byte_count}` (canonical State path, pinned bytes), `before_checkpoint={evidence,materiality,completeness: {path,sha256}}` (same-record old refs), `affected_ids` (nonempty unique sorted, subset non-DROP — checked), `supplement_manifest={path,sha256,byte_count}|null` (must be non-null iff any affected ID needs new Raw; validated via `validate_evidence_authority_supplement`), `records` (one per non-DROP DID — same shapes as `run_evidence_v2_interactive._validate_record` per Profile: COMMON + WEEKLY/THEMATIC fields; `source_bindings` required iff multiple task-bound sources), `completeness={obligations:[{obligation_id,status∈{SATISFIED,LIMITATION,NEEDS_RESEARCH,NOT_APPLICABLE},rationale}],residual_limitations[],closure}` covering the **union** of Profile-initial + Discovery-named IDs (missing/extra both refuse; `dimension/description/discovery_ids/evidence_task_ids` derived by LOW builder, not caller-supplied), `runner={provider,model,invocation,generated_at(RFC3339)}`, `tool_pins={repository_commit_sha(40hex),orchestrator_version,contract(pipeline/quality/research/publication SHAs)}` (current HEAD at request time — recorded, not self-containing future SHA).

Conditional: `supplement_manifest==null` iff all affected IDs reuse existing Discovery-bounded sources only (no new Raw); `closure` non-null iff `research_profile==THEMATIC` (same 3-field interactive shape as runner `:247-257`, expanded by LOW to full 8-field result).

### 9.2 `schemas/dm022-revision-proof-v2.schema.json` (NEW)

Deterministic proof bound to proposed bytes (LOW output, HIGH-checked before checkpoint).

Required: `schema_version`, `issue_id`, `revision_id`, `R`, `before={state,checkpoint_triplet,discovery,screening,evidence,views,ledger,completeness,profile}` each `{path,sha256,byte_count}`, `proposed={package,tasks[],cards[],views[],supplement,evidence_acceptance,views_acceptance,ledger,completeness}` each `{path,sha256,byte_count}` + `{result_set_sha256,view_set_sha256}` equality (`dirname==digest`, `acceptance.result_set_sha256==digest(package_sha,entries)` etc.), `affected_ids`, `unaffected_comparison={rows_checked,mechanical_projections[]}` (each projection `{field_path,old_sha,new_sha,reason}` with `field_path` an actual schema path e.g. `materiality-ledger.basis.evidence_acceptance_sha256` — no directory-prefix rules), `decision_binding={path,sha256,byte_count,before_match,after_match}` (re-hashed), `validations[]` (each `{check_id,kind==DETERMINISTIC,status==PASS,executor,result={path,sha256}}` — local content checks, never a genuine approval), `recorded_at`, `executor`, `SELF={sha256}` (`sha256_object` over all above minus SELF).

`FILE` rule: every listed `path` re-hashed at proof time; any drift refuses.

### 9.3 `schemas/dm022-supersession-checkpoint-v2.schema.json` (NEW, strict branch compatible with existing iterators)

Typed superseding checkpoint record. Keeps `artifacts` as `[{name,path,sha256}]` (same `namedAuthority` shape as `stage-checkpoint-v2.schema.json:126-134`) so `_artifact_map`, `_resolve_checkpoint_artifact`, `resolve_active_evidence_views` iterators work unchanged after adding the new-kind branch.

Required: `schema_version=="2.0-rc1"`, `kind=="PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1"`, `reason=="REVIEWED_ACCEPTED_UPSTREAM_CORRECTION"`, `issue_id`, `operation={from_state=="EVIDENCE_REVIEWED",to_state=="EVIDENCE_REVIEWED"}` (truthful same-State lifecycle), `producer_boundary={from_state=="CANDIDATES_NORMALIZED",to_state=="EVIDENCE_REVIEWED"}` (separately named artifact family re-attested — not a fabricated execution), `checkpoints==["evidence","materiality","completeness"]` (exactly these three, same order-insensitive set), `artifacts` (exactly 4, names `evidence-acceptance,edition-views-acceptance,materiality-ledger,profile-completeness`, each `{name,path,sha256}` with R paths for ledger/completeness + content-addressed R paths for accepts; `path` normalized, `sha256==FILE`), `before_state={path,sha256,byte_count}` (retained COPY ref) + `before_checkpoint={evidence,materiality,completeness:{path,sha256}}` (same old record ref thrice — same-record invariant) + `parent_checkpoint={path,sha256}` (exact predecessor) + `original_anchor={path,sha256}` (original checkpoint anchor before any supersession chain), `supersedes=[{path,sha256,revision_id}]` (append-only lineage, oldest-first; empty iff first supersession), `revision_id`, `R`, `request={path,sha256}`, `retention_plan={path,sha256,byte_count}` (present/absent inventory + source refs), `proof={path,sha256}` (§9.2), `decision={path,sha256}` (§6), `contract` (same 8-field shape as stage-checkpoint `:40-63`), `implementation={repository_commit_sha,orchestrator_version}` (current tool at completion, not old-E tool), `profile={path,sha256}`, `executor`, `recorded_at`, `SELF={sha256}`.

Conditional: `supersedes==[]` iff `parent_checkpoint==original_anchor`; else last `supersedes[]` entry `==parent_checkpoint`. `reviews[]` (min 1): must contain `CORE_STAGE_CONTRACT`-shaped deterministic review **only** for the producer-boundary family? No — decision §5 forbids forging old `CORE_STAGE_CONTRACT` lifecycle fields. Therefore this checkpoint’s `reviews[]` carries the **new** `DM022_SUPERSESSION_PROOF` deterministic PASS (`check_id=="DM022_SUPERSESSION_PROOF"`, `kind==DETERMINISTIC`, `status==PASS`, `result==proof {path,sha256}`) + the supplied-decision binding (`check_id=="DM022_SUPPLIED_DECISION"`, `kind==AGENT_RESEARCH`, `status==PASS`, `result==decision {path,sha256}` — admit, not Selection/Architecture/Human approval). No `CORE_STAGE_CONTRACT` row with forged `EVIDENCE→EVIDENCE` lifecycle is permitted; `_validate_core_stage_report` is **not** invoked for this kind (new branch bypasses it and instead verifies `proof` + `decision` + `SELF` + artifact re-hash — see §10).

Digest: `SELF==sha256_object(record minus SELF)`; every `artifacts[].sha256==sha256_file(artifacts[].path)`; `proof/decision/request/retention` FILE re-hash.

### 9.4 `schemas/dm022-current-vs-history-report-v2.schema.json` (NEW)

Current-vs-history typed report (truthful same-State adoption proof; not a forged stage report).

Required: `schema_version`, `issue_id`, `revision_id`, `checkpoint={path,sha256}` (§9.3), `history_basis={before_state:{path,sha256,byte_count},retained_copy:{path,sha256,byte_count},lineage_match:bool}` (detached validation: retained COPY bytes == recorded before bytes; lineage `supersedes` chain verified), `current_observation={lifecycle_state=="EVIDENCE_REVIEWED",triplet_match:bool,expected_after:{evidence,materiality,completeness:{path,sha256}},live_state_sha256,file_sha256}` (HIGH-side: LIVE State re-read + `validate_agent_state==[]` + triplet `==checkpoint` refs + file SHA), `slot_inventory={present[],absent[],retained[]}` (seven canonical slots per decision §11.1 with `{rel_path,sha256|nul,byte_count|nul}`), `guard={path,state,owner}` (coordination ref — shape owned by guard task, referenced here), `work_ref={repository_commit_sha,tree_sha,contract SHAs}` (phase HEAD/tree observation), `verdict∈{READY_TO_SWITCH,ALREADY_ACTIVE,INDETERMINATE}` (+ `reasons[]`), `recorded_at`, `SELF`.

No fictional `OldCoreStageReport`: this report never mimics `CORE_STAGE_CONTRACT` fields (`check_id/from/to` lifecycle). It is a distinct `DM022_CURRENT_VS_HISTORY` document consumed only by HIGH adoption/resume + readiness review.

---

## 10. Checkpoint truth + State integration

- **Kind/reason (fixed):** `kind=PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1`, `reason=REVIEWED_ACCEPTED_UPSTREAM_CORRECTION` (decision §5). Actual operation `EVIDENCE_REVIEWED→EVIDENCE_REVIEWED`; producer boundary `CANDIDATES_NORMALIZED→EVIDENCE_REVIEWED` (artifact family, not executed transition). No `EVIDENCE_SUPERSESSION_V1` alternate (superseded author prose).
- **Four artifacts / three checkpoints:** `checkpoints=[evidence,materiality,completeness]`; `artifacts=[evidence-acceptance,edition-views-acceptance,materiality-ledger,profile-completeness]` (names must match `stage-checkpoint-v2.schema.json:200-208 evidenceArtifacts` containment so shared validators recognise the family; `from_state` branch is new — see below).
- **Existing schema branch integration:** `stage-checkpoint-v2.schema.json` gains a strict conditional branch (schema edit is implementation scope, field contract fixed here): `if kind==PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1 then require operation.from/to==EVIDENCE_REVIEWED + producer_boundary==CANDIDATES→EVIDENCE + checkpoints==[evidence,materiality,completeness] + artifacts contains all four names + reviews contains DM022_SUPERSESSION_PROOF + no CORE_STAGE_CONTRACT lifecycle forgery`. Consumer iterators (`_artifact_map`, `_resolve_checkpoint_artifact:839-860`, `resolve_active_evidence_views:902-938`) need only the compatible `artifacts[]` shape — no iterator rewrite (B2 still must add the new Ledger/Completeness resolver + mode refusals, but the record shape does not break them).
- **State schema unchanged:** `survey-production-state.schema.json` requires no edit. Sole active selection update is a known-byte single-file replacement changing `checkpoint_provenance.evidence/.materiality/.completeness` **together to the same new record ref** (`{path,sha256}` each equal). Lifecycle/passed flags, forward `history` (length `==index+1`, monotonic), Profile/initialization contract, other checkpoints, Human gates remain unchanged. No second live selector, no extra pointer, no same-State `history` row (decision §5/R3).
- **Validation:** `agent._validate_checkpoint_record` gains a precise new-kind branch (implementation scope): verify `kind/reason/operation/producer_boundary/checkpoints/artifacts lineage` + `SELF` + artifact/review re-hash + `proof/decision/contract/implementation` binding; verify lineage `supersedes`/parent/anchor; **skip** `_validate_core_stage_report` lifecycle match (which would demand `report.from==lifecycle && report.to==next_state` for forward stages) and instead verify the truthful current-vs-history report (§9.4). Full strict State predicates retained; no `production.verify_state_basis` substitution (R2).

---

## 11. Current-vs-history report fields (typed, HIGH-owned)

See §9.4 schema. Semantics:

- `history_basis`: proves the record’s retained basis (retained before-State COPY bytes + original checkpoint anchor + `supersedes` chain) without touching LIVE State (detached, LOW-validated).
- `current_observation`: proves HIGH-side LIVE State still satisfies §3 window + triplet equals the new record + file bytes equal expected-after + `validate_agent_state==[]`.
- `verdict`: `READY_TO_SWITCH` (before bytes + proof + guard held) / `ALREADY_ACTIVE` (after bytes + cleanup complete + full readback) / `INDETERMINATE` (neither/nor or unreadable ownership — preserve, no restore/delete/adopt).
- Consumers: HIGH `run`/`resume` pre/post oracles + readiness reviewer. Later forward transitions (Selection→Architecture→Draft/publication) validate and consume the adopted checkpoint via its original operation context from retained lineage, never by demanding live State still equal before-State (decision §11.2).

---

## 12. Import DAG + SHA acyclicity (no self/future cycles)

Allowed imports (one-way, no top cycle):

```text
survey_dm022_revision_content_v2 (LOW leaf)
  ↑ (pure calls only)
survey_agent_control_v2 (Owner A, existing — new-kind branch calls LOW pure validators)
  ↑
run_dm022_revision_v2_interactive (HIGH — calls agent + LOW + family validators)
```

LOW imports `core/schema_gate/evidence/screening/completeness/discovery` only. Agent never imports HIGH. HIGH never imported by LOW/agent. `survey_agent_tool_v2.current_stage_basis_override` is **not** used by DM022 LOW (it would reintroduce State pinning); HIGH uses direct `agent.validate_agent_state` + `core.repository_commit_sha` instead of the override’s historical-State allowance (the override’s content-addressed State-SHA drift is for normal stage helpers with old accepted packages, not for DM022 before-State COPY linkage — DM022 binds `basis.state_path` to the retained COPY explicitly).

SHA/data DAG (each node may reference only prior-node SHAs; no node contains its own or a future SHA):

```text
(1) before-State COPY + parent/anchor/retention inventory
  → (2) revision request (refs (1) SHAs) + candidate R outputs (package/tasks/cards/views/ledger/completeness under R, refs (1)+(2))
  → (3) supplied independent decision (refs (1)+(2) SHAs + Raw SHAs + allowlist; immutable file, no live fetch)
  → (4) deterministic proof §9.2 (refs (1)+(2)+(3) SHAs; SELF computed last, never self-contained)
  → (5) supersession checkpoint §9.3 (refs (4)+(3)+(2)+(1) SHAs + SELF last)
  → (6) current-vs-history report §9.4 (refs (5)+(1) + LIVE observation; no future State SHA)
  → (7) State triplet refs (three {path,sha256} pointing at (5); State file SHA computed after write + postread verification)
```

Guard (transient coordination, not authority — shape owned by guard task) is claimed/revalidated between (2) and (5) and released after (7) postread; HIGH checks it at entry/before-publishing; unknown/unreadable/mismatched fails closed. Guard owner coordinates artifact-only descendant admissibility (§14); no second active-authority pointer.

---

## 13. Typed refs + duplicate equality (no placeholders)

Every file ref in request/proof/checkpoint/report/retention is:

```json
{"path": "research/v2/acceptance-revisions/<RID>/… (repo-relative, normalized, no traversal/symlink)",
 "sha256": "…64hex…",
 "byte_count": 1234,
 "kind": "<known enum where role matters: e.g. evidence-acceptance|edition-views-acceptance|materiality-ledger|profile-completeness|discovery|screening-acceptance|package|task|card|view|supplement|state|checkpoint|proof|decision|retention|report>"}
```

`path` validated by `repo_local_path`/`_repo_file` shapes; `sha256==sha256_file(path)`; `byte_count==stat().st_size`. No bare `object`, no `…`, no `CHECKED` dict. Where the same bytes appear twice, equality is explicit, e.g.:

- `acceptance.package_sha256 == sha256(package.json) == package-listed sha`;
- `ledger.basis.evidence_acceptance_sha256 == sha256(R evidence-accepted.json)`;
- `views_acceptance.evidence_acceptance_sha256 == sha256(R evidence-accepted.json)`;
- `checkpoint.artifacts[i].sha256 == sha256(checkpoint.artifacts[i].path) == proof.proposed.*.sha256 == report.*.sha256`;
- `State.checkpoint_provenance.{evidence,materiality,completeness} == checkpoint authority {path,sha256}` thrice-equal (same-record invariant).

---

## 14. Source epoch / current tools / HEAD-tree + artifact-only descendant rule

- **Current source/tool commit required before authority:** HIGH pins `repository_commit_sha==git rev-parse HEAD`, `tree sha` (via `git rev-parse HEAD^{tree}` observation, read-only), `contract_identity` (all pipeline/quality/profile SHAs), plus full live evidence pins (Profile/Discovery/Screening/old accepts) **before** generating R outputs. Old Evidence bytes are historical (old checkpoint `implementation` field); they are **not** required to equal current HEAD (decision §4: evidence need not exist in a tool-source commit).
- **Artifact-only descendant during review:** admissible **only if** (a) ancestry is the pinned HEAD plus exactly one descendant commit, (b) exact changed-path set ⊆ allowlisted operation paths for the declared attempt (`R/…`, retained COPYs/inventory, guard file, `request/proof/checkpoint/report` files, audit copies), (c) every prior pin (Profile/Discovery/Screening/old accepts/contracts) unchanged, (d) current controls/contract identical, (e) guard owner coordinated the descendant (guard task owns the allowlist + ancestry check). Otherwise refuse and require a new bounded attempt with a fresh RID; no standing main-follow, no generic dirty allowance, no future self-containing SHA in request/proof (decision §7 work-ref rule).

---

## 15. Owner-A + exact producer funcs (arbitrary-R + stale-proof handling)

Owner A (`survey_agent_control_v2.py`) references LOW/HIGH per §8.3 (ROOT CHOICE). No new authority file beyond the two modules + four schemas.

Exact producer funcs (actual existing — return here verbatim, do not rename):

- arbitrary-R writes: `survey_evidence_v2.accept_evidence_results(...,accepted_root=R/evidence/v2/accepted,...)`; `survey_evidence_v2.accept_edition_views(...,accepted_root=R/evidence/v2/views/accepted,...)`; `survey_evidence_v2.write_materiality_ledger(R/materiality-ledger-v2.json,ledger)`; `core.write_json(R/profile-completeness-v2.json,result)` after `validate_profile_completeness` + `schema_gate.validate_instance(...,profile-completeness-result.schema.json)`; `survey_evidence_v2.build_evidence_authority_supplement(...,output_path=R/…supplement….json, supplement_id=…)` for new Raw.
- arbitrary-R builders (State-free cores for LOW reuse): `survey_evidence_v2.build_materiality_ledger` (HIGH canonical path — LOW uses `_validate_materiality_ledger_content` + `_check_ledger_rows_content` instead to avoid `verify_state_basis`); new LOW union completeness builder (replaces `run_evidence_v2_interactive._build_completeness` incomplete initial-only loop) + `survey_completeness_v2.validate_profile_completeness`.
- later loaded-proof stale-before-State handling (State-free, no `verify_state_basis`): `survey_evidence_v2._validate_evidence_package_basis_content` (+ `_check_evidence_tasks_content`, `_check_evidence_package_files_content`), `_validate_evidence_acceptance_content` (+ `_check_evidence_acceptance_results_content`), `_validate_edition_views_acceptance_content` (+ `_check_views_acceptance_rows_content`), `_validate_materiality_ledger_content` (+ `_check_ledger_rows_content`), `survey_completeness_v2._validate_profile_completeness_content` (= `_validate_completeness_content` + `_check_profile_completeness_extra_content`), `survey_evidence_v2.validate_evidence_authority_supplement(...,implementation_sha=None, screening_acceptance=…, discoveries=…)` + `_supplement_entries_for_package(...,implementation_sha=None,...)`, `survey_evidence_v2.task_authority_sources`, `validate_evidence_card`, `validate_edition_view`, `validate_materiality_ledger` (pure row/basis part), plus `screening._validate_screening_acceptance_content` / `_resolve_effective_discovery_basis_content` (session-root, no State).

Stale rule: loaded R proof re-runs all State-free validators against retained before-State COPY + R bytes; any drift (SHA, coverage, supplement binding, obligation union, closure derivation) refuses. LIVE State is checked **separately** by HIGH (§2.1); proof never calls current-State acceptance recursively.

---

## 16. Ready vs unclosed — honest boundary for Task B

**Ready by this Task-B map (B4 CLOSED as map, pending readiness confirmation):**

- versioned-R producer paths + arbitrary-root funcs + canonical-no-overwrite proof (§4);
- LOW/HIGH split with exact proposed names/signatures/imports and no-cycle DAG (§8);
- four NEW schema contracts with strict fields + SELF/FILE digests (§9);
- checkpoint kind/operation/producer-boundary/4-artifact/3-checkpoint/lineage + State-unchanged + `artifacts`-compatible branch rule (§10);
- current-vs-history report shape (§§9.4/11);
- mechanical-vs-semantic classification with actual schema paths, affected permitted fields (§7);
- supplement-vs-Discovery + completeness-union rules (§§3.3-3.4);
- typed-ref + duplicate-equality + HEAD/descendant + SHA-acyclicity rules (§§12-14);
- supplied-decision immutable binding + no-PASS-producer prohibitions (§6).

**Explicitly UNCLOSED (not in Task B; required before code by other pre-code tasks; must not be waived as “review later” for selected must-have):**

- B2 full caller inventory: every direct canonical `materiality-ledger/profile-completeness/matrix/selection` reader + `resolve_active_evidence_views` callers + Draft/Synthesis/Reader/publication/operator/handoff/Gate/checkpoint-history/R1/editorial/renewal walkers, each with refuse-or-rewire disposition + `file:line` + post-acceptance tests. Known surfaces include `run_selection_architecture_v2_interactive:176-181`, `run_drafting_synthesis_v2_interactive:65-89`, `survey_drafting_v2.py:130`, `run_evidence_v2_interactive:715-732`, `survey_handlers_v2.py:204-280`, `survey_stage_validation_v2.py:402-543`, Weekly/Longform derivation + editorial/proposal + semantic-publication callers (authority review §8/B2 list) — enumeration + proof is a separate deliverable.
- Seven-slot exact path/owner/inventory (including `selection-architecture-audit.json:328-343` unguarded-write repair + successor no-overwrite/guard preflight for all seven + caller-input vs generated-archive distinction — decision §11.1).
- Guard state-machine/file/shape + claim/revalidate/release protocol + all check call sites + unknown/mismatched fail-closed + guard-release-failure row (operation review §3.4/§3.6).
- Phase HEAD/tree complete path set + reread discipline + artifact-only descendant allowlist enforcement code + stale refusal oracles.
- Owned IO/resume oracles (retain/copy/inventory, pre-unlink re-verify, State snapshot/restore, postread/inventory, explicit resume per §7 row) + failure-table implementation.
- Profile witness predicates: exact supported source-type allowlists per witness (DM016 two-map inconsistency + 10 absent Thematic types), exact Discovery-named obligation rows (DM017), archived-HTML + retrieval-provenance + `datePublished` event-meaning + timestamp-parser fields.
- CLI/API surface (if any new CLI flags — none selected; no new caller flags/verified dicts).

If any required predicate or normal writer cannot be included without weakening it, return the exact blocker and revisit A1-vs-A2 (decision §11.4) — never implement a partially guarded A1.

---

## 17. Stop

Design/source-inspection only. No new operation, no W40 reproduction, no upstream CORE_FIXED, no deployment/publication acceptance, no runtime/import/test/build/fixture/restore/network/ordinary Commit/Push, no Gitlink cleanup. Next is the remaining pre-code returns + independent readiness review + Astra confirmation before code. Whole NOT_READY / step4B3 OPEN / audit unstarted / DM021+022 OPEN preserved.

---

*Task: AUTHOR-side Task B (schemas/producers/DAG). Bound to decision `a345bb95…` including §11 + root §5 + both FINAL-BINDING reviews. Proof-copy read-only; implementation blocked.*
