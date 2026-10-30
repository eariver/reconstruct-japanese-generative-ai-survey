# Independent DESIGN review — DM017 3/5 contract + route support obligations

Status: **DESIGN REVIEW ONLY. No code/tests/runtime/imports/fixtures/network/Git/Human-commit readback.**
Reviewer is independent of Author B/C; author files preserved unchanged
(`named-obligation-applicability.md/json` R1, `named-obligation-contract-correction.md/json` R2,
`route-requirements-and-disposition.md/json` Author C).
Task authority: assessment §5
(`outputs/rephase-1-dm022-prearchitecture-implementation-assessment.md:52-60`).
Contract `a345bb95` §11 + precode `0425c530` §5 unchanged.
Source read-only: `/tmp/opencode/jgas-dm022-indep-20261029T235900Z/proof-candidate`
(final133/768, patch `25b48878`, manifest `31fa4a72`). Baseline `774dd39a`.
ROOT proposal under review: 3-field initial / 5-field named-only input in existing
`completeness.obligations` array, internally derive 7-field result, no OLD/current-Profile
rewrite, no new Gate, no new schemas. No independent approval of DM016 source-class
mapping (Human 4-doc intake in parallel — explicitly out of scope).

Verdict: **DESIGN_NOT_READY (blocking).**
BOUNDED_PASS scope is limited to §6; the 3/5 direction itself is not rejected,
but it must not proceed to pre-code/implementation until §§1–4 corrections close
and ROOT re-confirms. Root decides.

## 1. BLOCKING — Universe `U = initial ∪ named(effective)` loses root OIDs (R2 §2 false)

R2 `named-obligation-contract-correction.md:34-39` claims
`validate_discovery_expansion:243-322` "already enforces child ⊆ parent-union
and full parent closure" and that the named universe "therefore includes
expansion-added IDs (e.g. GAP_FILL `EFF-O13/14/15` class) while forbidding
invented IDs outside parents."

Source reading contradicts both halves:

- `survey_screening_v2.py:303-311` enforces per-child `child_obligations ⊆
  union(declared parents)` only (`invented → refuse`). It does **not** enforce
  parent-OID preservation.
- `survey_screening_v2.py:313-318` enforces DID closure only
  (`accounted_root_ids == root_ids`, "silently omitted from derived parent
  closure"). A derived set that accounts every root DID while omitting that
  root's OIDs passes.
- `survey_screening_v2.py:272-275` requires every derived record use a
  parent-requiring expansion origin (`EXPANSION_REQUIRING_PARENT`), which
  **excludes** `GAP_FILL`/`BASE`/`CARRY_OVER`. An "expansion-added" genuinely-new
  ID in derived records is therefore `invented → refuse` at `:307-311`.
  GAP_FILL `EFF-O13/14/15`-class IDs can only enter as **root** named IDs,
  not as derived additions. R2's "includes expansion-added IDs while forbidding
  invention" is internally contradictory and source-false.

Concrete counterexample (shapes per `survey_screening_v2.py:141-161`,
no runtime — pure contract reading):

- Root JSONL (issue X): `D-R1` `BASE`, `obligation_ids=[O-KEEP,O-DROP]`,
  identity `S1`, `raw_paths=[raw/a.bin]`; `D-R2` `BASE`,
  `obligation_ids=[O-OTHER]`, identity `S2`, `raw_paths=[raw/b.bin]`.
- Derived JSONL: `D-C1` `REFERENCE_EXPANSION`, `parent_refs=[D-R1,D-R2]`,
  `obligation_ids=[O-KEEP]`, `raw_paths ⊆ {raw/a.bin,raw/b.bin}`,
  identity `S1` (rooted in a declared parent per `:297-302`).
  Single child already yields `accounted_root_ids={D-R1,D-R2}=root_ids`.

Checks: invented `∅` (`{O-KEEP} ⊆ {O-KEEP,O-DROP,O-OTHER}`) pass;
DID closure pass; raw/identity pass by construction. Yet `O-DROP`, `O-OTHER`
are absent from derived union. A two-child variant (`D-C2` on `[D-R2]` with
`obligation_ids=[]`, allowed since only `GAP_FILL` requires non-empty at
`survey_screening_v2.py:158-159`) demonstrates the same loss with
per-parent accounting.

Consequence for `U`:

- Normal `run()` sets `discovery_path = effective["path"]`,
  `discovery_records = effective["records"]`
  (`run_evidence_v2_interactive.py:641-648`).
- `_check_profile_completeness_extra_content` reads `discoveries` **only**
  from that `discovery_path` (`survey_completeness_v2.py:154`), builds `named`
  only from those records (`:213-220`), reports `missing` only against them
  (`:221-223`), and traces `discovery_ids` only to their declaring DIDs
  (`:224-236`).
- `_check_completeness_result_content` checks obligations only against ledger
  DIDs/tasks derived from the same effective basis
  (`survey_evidence_v2.py:2163-2181`), and `run():745-792` builds the ledger
  from `discovery_path` (effective) and validates completeness against that
  same `discovery_path`.
- Hence a root-only OID dropped by expansion is invisible to **both**
  validators — they pass a silently narrowed `U`. R2 §6's "full validator
  stays unchanged and still catches drift" holds only for drift *within*
  effective, not for root→effective declaration loss. Which records passed
  is therefore: effective records only, never root.

Required source-grounded repair (no auto-add, no rewrite, no new schema):

1. Define `U := initial_ids ∪ named(root_records) ∪ named(effective records)`,
   both taken from the **same already-resolved** `resolve_effective_discovery_basis`
   dict (`survey_screening_v2.py:353-439` returns `root_records` + `records`
   together; `run():641-648` already holds both — no second fetch, no retype).
2. Add a fail-closed **declaration-loss gate** before input validation:
   `lost = named(root_records) − named(effective records)`; if `lost ≠ ∅`
   refuse (`DECLARATION_LOSS: {lost}`, naming unaccounted root OIDs).
   Do **not** auto-add OIDs to derived records, do **not** inherit-rewrite
   accepted children bytes, do **not** add a schema field to carry dropped OIDs.
   Rewriting accepted bytes would violate acceptance immutability
   (`validate_acceptance:897-916`, `accept_results:919-979` content-addressed
   digest); auto-adding would invent provenance. Refusal forces a new
   preserving expansion or explicit disposition, with accepted bytes untouched.
3. On pass (`lost == ∅`), `U` collapses to `initial ∪ named(effective)` and
   downstream (`_build_completeness:499-508` exact derive, full validators
   unchanged) is sound without ledger/basis changes. If ROOT ever wants to
   *tolerate* loss, that is a separate contracted basis change (ledger +
   validator + fingerprint), not this unit.
4. Correct R2 §2 wording: DID accounting ≠ OID preservation; derived cannot
   add GAP_FILL IDs; `U` must cite both `root_records` and `records`.

## 2. BLOCKING — Proposed Python signatures are a SyntaxError as written

Current (proof-candidate source):

- `_validate_completeness_input(value, profile)` at
  `run_evidence_v2_interactive.py:228`; `validate_interactive_input(value,
  profile, expected_ids, task_source_ids=None)` at `:272-277`, forwarding at
  `:309` without discovery context.

R2 §5 proposes adding "one required positional `discovery_records`" to each,
with `validate_interactive_input(..., task_source_ids, discovery_records)`.
With `task_source_ids=None` retaining its default, a following required
positional is invalid Python (`non-default argument follows default argument`).
As written the contract cannot be implemented.

Required correction (concrete, keyword-only — fine per tasking):

```python
def _validate_completeness_input(value, profile, *, discovery_records): ...
def validate_interactive_input(value, profile, expected_ids,
                               task_source_ids=None, *, discovery_records): ...
```

- `discovery_records: list[dict]` required keyword-only, no policy flag.
- Call-site `:674-676` becomes
  `validate_interactive_input(doc, profile, expected_ids, task_source_ids,
  discovery_records=discovery_records)` (the `discovery_records` local from
  `:648` plus `root_records` for the §1 gate).
- Test caller `tests/test_run_evidence_v2_interactive.py:99-106` (positional
  4-arg) must be updated to pass `discovery_records=` explicitly; a missing
  keyword must fail closed with explicit `discovery_records required`, not a
  bare `TypeError` relied upon as a guard. No new CLI flag, no
  caller-verified dict.

## 3. REQUIRED — Adapter + "already available" trace is incomplete

- R2 §1 correctly locates the gap (`discovery_records` available at
  `run():648` but not passed to `_validate_completeness_input:309`).
  "Already available" must not become the fix description: the fix must name
  **which** basis flows where — `effective["records"]` for entry/derive **plus**
  `effective["root_records"]` for the §1 loss gate. Two different objects from
  one resolved dict, not one ambient variable.
- `run_evidence_v2_agent_first.py:81-99` monkey-patches only
  `_build_completeness` (`:88-91` `complete(*args,**kwargs)` forwards then
  `completeness_with_preserved_residual_limitations:55-76` unions residual
  into `closure.limitations`). That wrapper operates on the **result**, so new
  3/5 input shapes flow through the unchanged signature — compatible *provided*
  the wrapped `original(*args,**kwargs)` receives the same
  `(repo_root, profile, profile_path, discovery_records, ledger_path, ledger,
  input_value)` tuple as normal `run():767-775`. The contract must state this
  positional/keyword preservation explicitly; a future reordering breaks the
  adapter silently.
- Normal CLI vs agent-first payload distinction must be stated correctly:
  the accepted Discovery artifact stores compact `acceptedRecord`s
  (`discovery-acceptance-v2.schema.json:85-98`: flat `obligation_ids`,
  `parent_edges`, no `provenance` wrapper), while canonical JSONL preserves
  full `provenance`/`source` objects (`survey_discovery_v2.py:84-153`,
  `_normalize_record:139-153` projection). The adapter's
  `acceptance_with_canonical_discovery_records:33-52` substitutes hash-pinned
  JSONL records precisely because compact records lack the provenance the
  builder/closure need (`_build_completeness:499-540`,
  `survey_completeness_v2.py:101-119`). Normal `run()` does not need that
  substitution (it already holds JSONL effective records), but it still needs
  the §1 root check — compact acceptance must never be used as the `U` source.
  R2's supplement note (`prepare_evidence_package:563-591` adds sources, not
  Discovery IDs) is accepted as stated; it does not extend `U`.

## 4. REQUIRED — `dimension/description` + DM022 separation (confirm with one tightening)

- R2 §3 table (3-exact for `oid ∈ initial`, 5-exact for named-only, refuse any
  other `oid`; exact cover; 5-on-initial refused, not tolerated) is the correct
  minimal direction: it matches the actual gap (input validator blind to
  Discovery at `:228-250`), reuses the actual derive site (`:499-508`), leaves
  final 7 fields (`profile-completeness-result.schema.json:27`), Profile, schemas,
  and downstream consumers (`run_selection_architecture_v2_interactive.py:70-109`,
  `survey_architecture_v2_base.py:93-180`, `run_drafting_synthesis_v2_interactive.py:98-129`)
  untouched. 5-on-initial **refusal** (not exact-identity tolerance) is
  confirmed: it preserves Profile authorship and the existing
  dimension-change error (`survey_completeness_v2.py:211-212`); named-only
  `dimension` must satisfy `_validate_obligation_shape:62-63` + non-empty
  `description`.
- DM022 separation in R2 §4 is confirmed: ordinary path creates
  `profile-completeness-v2.json` only if absent (`run():763-766`
  refuse-overwrite, so no OLD exists to fall back to); DM022 keeps its separate
  7-field `fullObligation` (`dm022-revision-request-v2.schema.json:232-244`
  `minLength:1`) + valid-OLD contract; LOW re-derives bindings
  (`survey_research_authority_v2.py:1898-1908`) and its empty-fallback branch
  (`:1886-1897`) is dead under schema-first loading
  (`load_revision_request:1149-1162` validates schema before returning, and
  request `completeness.obligations` items are `fullObligation:44`). State this
  dead-branch reading to avoid misstatement, as R2 does. No OLD fallback in
  the ordinary 3/5 unit; no `production.verify_state_basis` substitution; no
  unselected operations.

## 5. BOUNDED_PASS (narrow — does not imply NOT_READY lift)

- Call-sequence location (§1 of R2): ENTRY `:610-623`, basis `:632-648`,
  package `:653-664`, input `:674-676` + `:309`, cards/accepts/ledger,
  `_build_completeness:767-775`, schema-gate + `validate_profile_completeness
  :776-794`, archive `:806`; prepublish `_dm022_require_ready`
  `:694,727,748,764,805` preserved; `O_NOFOLLOW/O_EXCL` discipline unchanged.
  Accurate; no new Gate/policy flag needed.
- Backcompat rule (R2 §8): old 3-field-only inputs validate **iff**
  `U == initial_ids`, else missing-named refusal (no silent green). Correct.
- Dead-fallback reading (R2 §4) per §4 above. Correct.
- No new top-level catalog / Profile rewrite / final-7 change. Correct
  minimality direction (vs rejected 2-array skew and full-7 retype drift).
- No pattern-source cleanup or batch unrelated maintenance in this unit
  (DM016 10 literals, supplement `SOCIAL` enum gap, frozen-validator touch
  stay separate). Confirmed as a binding constraint, not a suggestion.

## 6. Route disposition — conditional PASS, must not be dropped by FIRST repair

Author C `route-requirements-and-disposition.md` §§1-11 is source-cited and
provisional-policy-safe (Weekly + required Special incl. non-four-family
Thematic + Retrospective remain requirements; FIRST repair is DM016 canonical
types + DM017 ordinary union, Profile-neutral). This review concurs
**conditionally**:

- Manual/DIRECT_PRIMARY stays `PRIMARY_ONLY` (`survey_reader_surface_gate_v2.py:1352-1356`
  exact primary path+bytes) with byte-hash support binding, not complete-reader
  semantics (`:1335-1349` trio vs `:1356` early return); post-render reviews
  (`config/survey-production-v2.json:170-206` + lifecycle Human Preview) are
  distinct from pre-TeX Reader-Surface judgment. No blanket "manual unsupported
  publication," no silent upgrade to supporting-surface semantics.
- Legitimate manual repair only: pre-acceptance authoring (new bytes, no
  accepted authority to violate) **or** post-VALIDATED via genuine Human
  `REQUEST_CHANGES` reopening / new edition / proper gate — never fake Gate
  bytes, never old-State hash as current authority, never direct changed-reader
  P1 on Retro/manual (`survey_editorial_correction_proposal_v2.py:566-573`
  `UNSUPPORTED_ROUTE`; renewal `637-639`; PREARCH family refuses). Avoid
  "just republication" as a blanket path.
- Thematic generated IR stays four-family-only
  (`FORMAT="THEMATIC_FOUR_FAMILY_LINEAGE_V1"`,
  `FIXED_TITLE/EDITION/FINAL_HEADING/TOC_TITLE` + 4-model cross-table at
  `survey_longform_derivation_v2.py:109,118-136`); generic-IR claims require a
  constants/serializer diff first. Retrospective helper is generic upstream
  (`survey_period_v2.py:5-134,193-216`); `--spec` direct CLI authorization is a
  Human record, not a new engine. Non-four-family + Retro stay **OPEN** after
  the FIRST upstream repair; §9's three-way complete-reader/normal-correction
  comparison remains its own contracted unit. First repair must not silently
  narrow Special scope, relabel aliases, or drop obligations.

## 7. Required corrections checklist (ROOT gate before pre-code)

1. Replace R2 §2 `U` with §1 above (root+effective union + declaration-loss
   refuse); correct "expansion-added IDs" wording; cite
   `survey_screening_v2.py:272-275,303-318,353-439`.
2. Replace R2 §5 signatures with §2 keyword-only forms; update `:674-676` and
   test call; state adapter `*args/**kwargs` preservation per §3.
3. State the §3 basis trace (effective for entry/derive, root for loss gate;
   compact acceptance never a `U` source; supplement does not extend `U`).
4. Keep §4 (5-on-initial refusal, exact cover, internal derive
   `sorted(declaring.get(oid,[]))`, profile-only `[]`, DM022 separation,
   no OLD in ordinary path).
5. Keep §5 PASS items + §6 route conditions; no DM016 batching, no new
   schemas/Gates, no source-class approval in this unit.

No runtime, no fixtures, no Human-commit readback used. No source edits made.
