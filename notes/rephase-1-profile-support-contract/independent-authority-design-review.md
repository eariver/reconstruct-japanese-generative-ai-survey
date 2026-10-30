# Independent authority DESIGN review — selected Profile/support contract (selection ONLY)

Status: **DESIGN REVIEW ONLY, selection scope. No code/tests/runtime/imports/fixtures/build/Git/Human-commit readback/network. Acquired Python DATA never executed/imported (text-read only).**
Independent of Astra/author; prior `independent-obligation-contract-review.md`
(DESIGN_NOT_READY §§1–4) preserved unchanged — this file adds the final
selected-contract verdict only.
Task: final DESIGN review of selected ROOT contract
`outputs/rephase-1-profile-support-contract-decision.md` FULL +
`notes/rephase-1-profile-support-contract/astra-review-resolution.md` (mandatory).

Source boundary: final133 READONLY
`/tmp/opencode/jgas-dm022-indep-20261029T235900Z/proof-candidate`
(actual409/tree8ce +133 paths/768 files, patch `25b48878`/4931836B,
manifest `31fa4a72`/185422B). Baseline `774dd39a` unchanged.
Contract `a345bb95` §11 + precode `0425c530` §5 unchanged.
No implementation authorization by this review.

Reviewed bindings (data-only file bytes, no Git object/commit as authority):

- Decision `outputs/rephase-1-profile-support-contract-decision.md`
  SHA256 `e5aed7a4d3da3f50bf0fd14448690053dbd58fb5e936d8cb51948e6f894bedd8` / 18663B.
- ROOT resolution `notes/rephase-1-profile-support-contract/astra-review-resolution.md`
  SHA256 `34ee4891ec49a1796c155f74a5410c227e3f67d9a5b3f3931ec127d230955858` / 4745B.
- If ROOT revises either file, this review needs final confirmation against the new bytes;
  the verdict below binds only the above bytes.

Verdict: **DESIGN_BOUNDED_PASS — contract selection ONLY.**
Selection semantics are source-grounded and close all four prior blockers at
selection level. Code remains **blocked** until the mandatory concrete pre-code
map (§6 of decision) is returned, independently reviewed, and Astra confirms.
Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN unchanged.

## 1. Intake + DM016 table — normative NEW selection, not historical approval (PASS)

- Human-authorized 4 fixed GETs at `c8d0ecc1c9566a2303ad3b4c42635d4b672650e4`
  complete in `intake-20261030T124140Z/` (summary + manifest + 4 `DATA.*`,
  4/4 HTTP200/size/blob-checked per summary §§1–2). No current-main follow,
  extra records, code adoption, or script execution. Compat `.py` is DATA only.
  Decision §1 + ROOT §2 correctly bound this scope; decision §5
  "Nothing here executes or adopts the acquired compat script" is confirmed.
- Decision §3 table is **normative NEW ROOT selection from defect RECOMMENDED**,
  not promotion of workaround bytes: 10 EXACT literals with counts
  13/21/8/6/4/8/4/1/1/1 (67 blocked / 93 passthrough) match defect §2 +
  validation-report §2 as recorded in intake-summary §§2–3. All 10 carry exact
  resource provenance (maintainer recipe/package docs as first-party to that
  runtime/package subject; repo-native PR as primary of its own proposal).
- Decision §3 + ROOT §§1–2 explicitly reject: conditional classifier, default
  SECONDARY, PR-never-primary, URL-sniff (`run_special_interactive_evidence.py:41-47`),
  alias/projection ledger, new module, legacy-enum edits, supplement-SOCIAL
  expansion. Source-grounded: active gate is canonical
  `survey_evidence_v2.SOURCE_CLASS_MAP/_source_class` via `task_authority_sources`
  (`survey_evidence_v2.py:44-109,177-184,413-446`, call `422-423`
  `_source_class(source.get("source_type"))` + supplement `304-305` exactness);
  runner 6-map (`run_evidence_v2_interactive.py:49-56,110-114`) is dead
  (3 grep hits, zero in-file calls; card path `:321` + `:666` use canonical).
  Legacy 4-enums (`screening-record.schema.json:12`, `evidence-task.schema.json:25`)
  are v1 path, correctly not edited.
- Resource/proof distinction explicit: `source_class` ≠ `evidence_class`/
  verification/materiality/completeness promotion (decision §3 ¶2, intake §§3–4).
  Per-record Raw **not fetched** is explicitly stated as limiting TS-001 claims
  (decision §3 ¶2, proposal §6, intake §§3/5: vLLM-recipe / PR-27742 associations
  UNVERIFIED, PACKAGING counterpart unidentified) and **now NOT claimed** —
  no existing edition source/assertion approved, no CORE_FIXED. Genuine-type
  witnesses with full source API (collector + `raw_refs` + instants + publisher +
  claim binding per literal) are deferred to mandatory oracles (§6.4), not assumed.
  The 3 `PRIMARY_*` single-task rows remain a pre-code oracle gate (proposal §6
  BLOCKING question preserved): no PRIMARY authority may be asserted until that
  oracle closes; selection does not waive it.

## 2. Callers + new-vs-history gates (PASS at selection)

Full actual callers pinned (source-read, no runtime):

- `validate_interactive_input`: prod 1 (`run_evidence_v2_interactive.py:674-676`),
  test 1 (`tests/test_run_evidence_v2_interactive.py:101-106`, positional 4-arg
  today), frozen edition driver (`DATA.run_frozen_evidence_chain.py:166-167`,
  edition-local NOT Core). Internal `_validate_completeness_input` caller 1 (`:309`).
- `_build_completeness`: prod 1 (`:767-775` tuple
  `(repo_root,profile,profile_path,discovery_records,ledger_path,ledger,input_value)`),
  adapter wrapper 1 (`run_evidence_v2_agent_first.py:88-91` `*args/**kwargs`
  forward), frozen driver 1 (`:222-223`).
- Decision §4.2 + §6.1 require the concrete pre-code return to pin all
  direct/agent-first/CLI/handler callers + DM022 HIGH eligibility + test/adapter
  signatures. Exact import/digest/closure/epoch map is **permitted open pre-code**;
  decision §6 states "not a path budget" and "any additional necessity returns to
  Astra" — this is an explicit compatibility-map obligation, not an essential
  semantics waiver. No caller-verified dict, no State recursion (LOW header
  `survey_research_authority_v2.py:1-36` detached PATHS-only preserved).

New-vs-history separation (critical policy, PASS):

- Decision §4.1 + ROOT §3 scope the new per-parent loss rule to **new**
  Screening prepare/accept + ordinary Evidence input preflight + DM022 HIGH
  new-operation eligibility **before owned writes**. They forbid blindly tightening
  shared historical `validate_discovery_expansion:243-322` or detached `_content`
  validators: old records stay interpretable under their accepted contract;
  historic validity ≠ new-operation eligibility. Source-grounded because that
  shared function is called by current (`resolve_effective_discovery_basis:428`),
  renewal content (`_resolve_effective:855`), and acceptance validation
  (`validate_acceptance:915`) — global tightening would rewrite history.
  Pre-code must prove the separation without caller-verified flags.

## 3. Per-parent OID preservation on actual `parent_refs` (prior §1 CLOSED)

- Decision §4.1 correctly restates source: expansion checks child ⊆ declared-parent
  union (`survey_screening_v2.py:303-311`) + DID closure (`313-318`), excludes
  GAP_FILL/BASE/CARRY_OVER from derived (`37-43,272-275`); derived cannot invent.
  New gap-fill IDs are root research expansion, not child invention. R2
  "expansion-added IDs" erratum is corrected; proposal §2 records it.
- Selected `U = P ∪ named(R) ∪ named(E)` from the SAME resolved
  `resolve_effective_discovery_basis:353-439` dict (`root_records` + `records`,
  `run():641-648` already holds both; no second fetch, no compact acceptance
  as `U` source, no supplement-DID universe per `prepare_evidence_package:563-591`).
- Per-parent rule cites the actual source field: string-array
  `provenance.parent_refs` (`survey_screening_v2.py:144-159`,
  `survey_discovery_v2.py:96-115`), not normalized `parent_edges`. Every
  `(parent,OID)` needs an effective carrier (identical DIRECT record or valid
  derived child with that parent in its `parent_refs`); global-set equality
  insufficient when two parents share one OID (prior two-parent counterexample
  retained as the reason). `lost` (global + per-parent uncovered) → `DECLARATION_LOSS`
  refuse before writes; no auto-add, no accepted-child rewrite (acceptance
  immutability `validate_acceptance:897-916`, `accept_results:919-979` digest).
  On pass `U` collapses to `initial ∪ named(effective)`; final derive uses
  effective DIDs only (`sorted(declaring.get(oid,[]))`, profile-only `[]`,
  ledger exact map per LOW `1898-1908` pattern), traceable via validated parent graph.
  Prior §1 blocker closed at selection; caller/epoch proof of the gate order is
  pre-code §6.1/6.5 business.

## 4. 3/5 keyword-only, no OLD, no altered schemas (prior §2 + §4 CLOSED)

- Proposed direction
  `validate_interactive_input(value,profile,expected_ids,task_source_ids=None,*,
  discovery_records,root_discovery_records)` +
  keyword-only `_validate_completeness_input` (decision §4.2, proposal §2)
  fixes the prior required-after-optional SyntaxError as written. `_build_completeness`
  tuple retained. Concrete pin deferred to pre-code — permitted, not a waiver.
- Exact 3-for-`P` / 5-for-`U−P` / refuse `∉U`, exact cover, dupe/extra/omission
  refuse, 5-on-initial refuse (not tolerance), explicit status/rationale, no
  autostatus (decision §4.2). Preserves Profile authorship
  (`survey_completeness_v2.py:211-212` dimension-change error) and
  `_validate_obligation_shape:62-63` dimension membership. Final 7 rows, result
  schema (`profile-completeness-result.schema.json:27`, `OBLIGATION_KEYS:25-33`),
  Profile/DM022-request/consumer schemas unchanged; DM022 `fullObligation`
  (`dm022-revision-request-v2.schema.json:232-244` `minLength:1`) separate; ordinary
  path has no OLD (refuse-overwrite `run():763-766`); LOW fallback `:1886-1897`
  dead under schema-first `load_revision_request:1149-1162` noted only.
  Old 3-only inputs valid exactly when `U==P`. Prior §2/§4 blockers closed.

## 5. Early preflight, canonical resolver, residual parity (prior §3 CLOSED)

- Early preflight feasible as selected: root/effective available at `run():641-648`
  **before** `prepare_evidence_package:653-661` and all owned writes
  (`:694,727,748,764,805` guards; ledger/completeness refuse-overwrite
  `:749-750,765-766`; Evidence package non-empty refusal
  `survey_evidence_v2.py:595-596`; Screening `prepare_package:517-518`,
  `accept_results` digest path). Decision §4.3 requires shape/`U`/loss validation
  before owned/package writes while keeping record/task-dependent checks on the
  generated universe — no "invalid input is pre-write because final schema rejects
  it" inference.
- Canonical resolver already reloads: `resolve_effective_discovery_basis:353-439`
  does `read_jsonl` + `validate_discovery_set` + SHA/pin/ID checks and returns
  full JSONL `root_records`/`records`. Decision §4.3 + ROOT §3 forbid repeating the
  stale "direct runner necessarily gets compact summaries" claim; compact
  `acceptedRecord`s (`discovery-acceptance-v2.schema.json:85-98`) are never a `U`
  source. Count/schema outer-boundary confirmation is pre-code work.
- Residual union + parity: adapter `55-76` unions residual into THEMATIC
  `closure.limitations`; builder `:525-556` + validator
  `survey_evidence_v2.py:2239-2240` (LIMITED must preserve residual) already
  require it. Consolidating the union into the normal builder with a thin
  delegation adapter after caller proof (decision §4.3, proposal §3) gives
  identical direct/agent-first semantics with no mutable-monkey-patch cleanup
  beyond proof and no collector rewrite. Prior §3 closed at selection.

## 6. Routes — no silent drop, no all-Profile acceptance (PASS)

Decision §2 + ROOT §4 preserve every necessary route with completion conditions:
Weekly generated (required, extend upstream); four-family generated (required
existing case, `THEMATIC_FOUR_FAMILY_LINEAGE_V1` + fixed display
`survey_longform_derivation_v2.py:109,118-136`, not generic); other-Thematic
**required remaining** reader/correction gate (not solved by source-class fix);
bounded Retrospective **required remaining** gate (keep period semantics, never
relabel as Thematic; `--spec` transport sufficient if Human-authorized,
`survey_period_v2.py:193-216`, no new engine; Foundations planning-only
`survey_x_intake_v2.py:86,152-154`); manual DIRECT_PRIMARY/PRIMARY_ONLY preserved
with honest byte-hash scope (`survey_reader_surface_gate_v2.py:1352-1356` vs
trio `:1335-1349`) + post-render/Human reviews, never blanket post-VALIDATED
repair (genuine REQUEST_CHANGES/new edition only). Order (shared upstream →
reader/correction → quality → candidate/audit → adoption → measured improvement,
no numeric saving) matches assessment §5. No independent-source all-Profile
acceptance claimed; DM016/017 are shared prerequisites. Prior §6 condition carried.

## 7. Old blockers → closed list; remaining gates (no code)

- Prior §1 (effective-only `U` + expansion wording) → **CLOSED** by §§3–4.1 above.
- Prior §2 (invalid signature) → **CLOSED** by keyword-only direction (§4).
- Prior §3 (adapter/compact trace) → **CLOSED** by canonical-resolver +
  compact-never-`U` + parity rule (§5).
- Prior §4 (dim/desc + DM022 split) → **CLOSED** by exact 3/5 + refusal + no-OLD +
  unchanged schemas (§4).
- Remaining: mandatory pre-code map per decision §6.1–6.5 (sites, ten mappings,
  strict alternatives, file/import/digest/closure/epoch map, behavioral witnesses
  incl. per-parent loss/two-parents-share-OID/DROP/HOLD/CONTEXT cases, parity,
  history-vs-new rejection, downstream consumers without PASS-count transfer);
  RUNTIME_* PRIMARY oracle (§1 above); independent readiness + Astra confirmation.
  These are explicitly open and block code — not waived by this PASS.

No code/implementation authorized. Next: Human Commit Point; pre-code return on
final133 only.

## 8. FINAL-BINDING confirmation on updated decision INCLUDING §7 + ROOT INCLUDING §5 (selection ONLY, no implementation)

Reviewed FULL updated bytes (data-only, no Git authority):

- Decision `outputs/rephase-1-profile-support-contract-decision.md` INCLUDING §7
  SHA256 `62b14add5e50d7e5f7996c4b7536f95b5d74cdbc9b205b1eec54bde260527e2d` / 20472B.
- ROOT `notes/rephase-1-profile-support-contract/astra-review-resolution.md` INCLUDING §5
  SHA256 `021a0d7ce696a1d386ff2accd803e97033a297872ea65a0d7646a9953ded217a` / 7225B.
- Prior pins (`e5aed7a4…/18663B`, `34ee4891…/4745B`) are superseded history for the
  pre-§7/§5 bytes; §§1–7 above bind only those earlier bytes and remain preserved.
  This §8 binds only the new FULL bytes. If ROOT revises again, reconfirmation needed.
- Source final133 unchanged; 4-GET scope completed, no extra fetch/network.
  No runtime/tests/Git/Commit readback; DATA `.py` never executed. Source-read only.

§7 + §5 resolve inherited proposal §6 oracle ambiguity without contradiction:

- Fixed 10-table is normative NEW design (decision §§3+7, ROOT §§1+5). No
  SECONDARY fallback, no PR-never-primary, no conditional classifier. Operation
  `SECONDARY-or-refuse` phrase and proposal §6 fallback question are explicitly
  superseded (ROOT §5 ¶2). No conditional waiver.
- Accurately-represented provenance + claim limitations + oracle fixtures are
  mandatory **pre-code** (decision §7 ¶2, ROOT §5 ¶¶2–3): real category semantics,
  correctly represented maintainer/repo-native fixtures (synthetic labelled as such),
  explicit limitations, independent research/claim assessment under existing
  admission/content rules. Not retrospective approval of the actual 67 TS-001
  records, not new network/capture, not genuine-publisher machine proof, not a new
  Human Gate. Mismatched/unsupported inputs fail closed; accepted inputs never
  relabelled. This matches the required "no per-record Raw needed to certify old
  tasks (now NOT claimed)" boundary.
- All remaining pre-code import/predicate/phase-map work stays **CODE BLOCKED**:
  decision §§6–7 + ROOT §5 require exact signatures/callers/schema shapes, canonical
  root/effective loading, per-parent loss placement, unknown-source refusal placement,
  residual parity, guard/no-overwrite/failure windows, family/digest/closure/epoch
  handling, with historical validators uncontaminated. No helper-only completion,
  no new family/module/schema presumed. Not waived by this PASS.

Contradiction check: none requiring NOT_READY. §7/§5 are consistent with §§1–6
(route order, no silent drop, no all-Profile acceptance, resource-vs-claim split,
new-gates-only policy, keyword-only direction, early-preflight feasibility,
canonical-resolver + residual parity). No reintroduction of effective-only `U`,
positional signature, compact-as-`U`, OLD fallback, global expansion tightening,
or batch maintenance.

Verdict: **DESIGN_BOUNDED_PASS — contract selection ONLY (FINAL-BINDING).**
Prior DESIGN_NOT_READY stays history; §§1–6 closures stand; §7/§5 ambiguity closed
as above. No implementation authorized; pre-code readiness OPEN and CODE BLOCKED.
