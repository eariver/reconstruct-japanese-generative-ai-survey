# DM017 named-obligation applicability — DESIGN/SOURCE-READ ONLY (Author B)

Status: **DESIGN ONLY, no implementation/test/runtime/build/fixture/network/Git mutation.**
Author B DM017. Human continuation, NO Human Commit readback as authority.
Baseline fixed `774dd39a`. Source read-only:
`/tmp/opencode/jgas-dm022-indep-20261029T235900Z/proof-candidate` (final133/768,
patch `25b48878` / manifest `31fa4a72`). Contract `a345bb95` INCLUDING §11 unchanged.
ROOT precode `0425c530` INCLUDING §5 unchanged.
Assessment §5 is the tasking authority; ROOT closeout FULL is binding.
Secondary DM017 evidence reused from `notes/rephase-1-deferred-intake-20261003`
(delta-analysis, summary r0.3/r0.7); no fetch/current-main.

## 1. Requirement trace: `Profile.initial_obligations ∪ ALL Discovery.obligation_ids`

| Stage | Required set | Required fields | Authority / source (read-only) |
|---|---|---|---|
| Profile `initial_obligations` | Declared dimensions covered, ≥1 row | `obligation_id, dimension, description` (exactly 3) | `survey_production_v2.py:294-329` `_validate_initial_obligations`; schema `survey-production-profile.schema.json`; generators `weekly_profile:446-462`, `_thematic_initial_obligations:495-508`, `survey_period_v2.py:62-129` |
| Discovery provenance | Any `obligation_ids` array (may be empty; GAP_FILL non-empty) | IDs only, no dimension/description | `survey_discovery_v2.py:97-144`; `survey_screening_v2.py:141-161`; schemas `survey-discovery-record`, `discovery-acceptance-v2` |
| Screening expansion | Child IDs ⊆ parent-union; no invention | Same ID arrays | `survey_screening_v2.py:303-311` `invented → refuse`; `validate_discovery_expansion:243-322` |
| Normal interactive input | Exact Profile-initial cover | `obligation_id, status, rationale` (exactly 3) | `run_evidence_v2_interactive.py:228-269`; `expected_ids` from Profile only `:244-249` |
| Normal interactive builder output | Iterates **initial only** | Derives 7-field rows for initial only | `_build_completeness:482-570`, loop `:497`; named IDs silently absent from output |
| Full validators | Union: initial ∪ ALL named; dimension coverage; traceback | 7-field rows (see §2) + `overall_status` + Thematic `closure` | `survey_completeness_v2.py:50-238`; `survey_evidence_v2.py:2135-2243`; `validate_profile_completeness:265-290` |
| Manual/compat construction (TS-001) | Union via 3 mechanical rows | Full 7-field rows, unchanged validator | Deferred intake `deferred-maintenance-summary.md:521-552`, `delta-analysis.md:34`; `run_frozen_evidence_chain.py` + `validation-report.md` (secondary, not re-read) |
| DM022 LOW builder | Union, no autofulfilment | Full 7-field request rows (see §2) | `survey_research_authority_v2.py:1795-1999` `build_versioned_completeness_from_paths` |
| DM022 HIGH | Sole mutator, calls LOW | Same union, guarded writes | `survey_prearchitecture_acceptance_v2.py:1-39` (HIGH owns all writes; LOW required) |
| Selection/Architecture | Consumes active union via State triplet | No new rows; refuse on invalid | `run_selection_architecture_v2_interactive.py:70-109,264-435`; `survey_architecture_v2_base.py:93-180,287-352,860-909` (`INCOMPLETE → block :909`) |
| Draft/reader proof | Readback of adopted union; PREARCH kind check | No new obligation semantics | `run_drafting_synthesis_v2_interactive.py:98-129,215`; `survey_longform_derivation_v2.py:1069-1070` |
| Weekly/Thematic/Retrospective | Same union rule; profile-specific closure only | See §4 | Weekly `weekly_profile`, Thematic `thematic_profile`, Period `survey_period_v2.py` |

## 2. Which rows require the seven fields, and who supplies missing semantics

Final Completeness row contract (7): `obligation_id, dimension, description, status, discovery_ids, evidence_task_ids, rationale`
(`profile-completeness-result.schema.json:27`; `OBLIGATION_KEYS` in `survey_completeness_v2.py:25-33`;
DM022 request `dm022-revision-request-v2.schema.json:235-243` `fullObligation`).

| Row kind | dim/desc | status/rationale | discovery_ids/task_ids | Missing-semantics authority |
|---|---|---|---|---|
| Profile-initial | Required at Profile creation (Profile authority) | Not in Profile; supplied later | Not in Profile | Profile author (weekly/thematic/period generator + `validate_profile`) |
| Discovery-named (`EFF-O13/14/15` class) | **Not in Discovery** (IDs only) | Not in Discovery | Declaring DIDs from real provenance; task_ids from ledger | **Nobody in Discovery** — must come from §3 authority |
| Interactive input row | Absent by design | Operator supplies `status, rationale` | Absent by design | Operator, but builder drops non-initial IDs → discrepancy §3 |
| Final/DM022-request row | Required; request carries, else OLD same-ID fallback, else refuse | Required from request | **Re-derived**, not trusted (LOW `:1898-1908`) | Request operator + OLD valid row + real Discovery/ledger; **never invented** (`:1886-1897`) |
| Profile-only (no declaring Discovery) | From Profile | From request | Empty lists legitimate (LOW `:1900-1909`); `_unique_string_list` allows `[]` | Profile + operator; do not invent DIDs |

Prohibited: autofulfilment, invented `dimension/description`, silent drop (`Completeness silently dropped …:209,223`),
alias rename, allowlist relax to green. Dimension change on initial ID is explicit error
(`survey_completeness_v2.py:211-212`); named-row dimension must still be a declared Profile dimension
(`_validate_obligation_shape:62-63`); `discovery_ids` must trace back to declaring records (`:224-236`).

## 3. Builder-vs-validator discrepancy; OLD dependency

- Builder `_build_completeness` loops `profile initial_obligations` only; `validate_interactive_input`
  demands exact-initial cover. Validator `_check_profile_completeness_extra_content:213-236`
  demands `named ⊆ obligations` + full traceback. Any valid post-init expansion (EFF-O13/14/15)
  therefore fails the normal builder path while passing the validator path — this is DM017.
- DM022 LOW does **not** fix the normal builder; it bypasses it with an explicit request covering
  the full union (`:1871-1878` exact-set check) and re-derives bindings from Discovery/ledger.
- OLD dependency: `dim/desc` fallback reads OLD valid row same-ID (`:1886-1895`). If OLD is missing,
  invalid, or the ID is genuinely new with request `dim/desc` empty → `ResearchAuthorityError:1897`.
  DM022 cannot bootstrap new named semantics by assuming OLD valid exists; new IDs require
  operator-supplied `dimension/description` in the request. OLD supplies history, not invention licence.

## 4. Temporal / profile / collision rules

| Rule | Binding |
|---|---|
| `overall_status` | `READY/LIMITED/INCOMPLETE`, never `COMPLETE` (`survey_evidence_v2.py:2194-2196`); `NEEDS_RESEARCH>0→INCOMPLETE`, else `LIMITATION∨residual→LIMITED` |
| Thematic closure | 8-field dict required; counters re-derived from `research_pass` provenance, not self-reported (`survey_completeness_v2.py:81-142,131-136`; LOW `:1943-1960`); `status COMPLETE/LIMITED/NEEDS_RESEARCH`; non-Thematic `closure` must be null |
| Weekly (`weekly:*`) / Retrospective-Period | Same union; `closure=null`; Weekly dimensions `current relevance/technical significance/carry-over` with 1:1 initial IDs; Period dimensions/spec-driven with same 3-field initial contract |
| Multiple DIDs → one obligation | Union of declaring DIDs; `task_ids` = union over ledger rows for those DIDs (LOW `:1899-1908`) |
| One DID → multiple obligations | Allowed (`obligation_ids` array unique per record); each named ID tracked independently |
| One ID, multiple dimensions | Forbidden in one result (single `dimension` per row; duplicate ID → error; initial-dimension change → error) |
| No declaring Discovery (profile-only) | `discovery_ids=[]`, `evidence_task_ids=[]` valid; must still cover a declared dimension with valid `status/rationale` |
| KEEP/HOLD/CONTEXT/duplicates | Screening `KEEP/MAYBE/INSPECT` keep tasks; `DROP` excludes with `EXCLUDED/DUPLICATE` disposition (`survey_evidence_v2.py:1940-1956`); `HOLD/CONTEXT/NON_MATERIAL` are View materiality, not obligation bypass; `NEEDS_MORE→HOLD` (`:1458-1459`); duplicate Discovery reuses ID refusal (`validate_discovery_expansion:263-265`) |

## 5. Bounded repair contracts (ROOT selects; Author B recommends O1)

| Option | Change | Authority preserved | Cost/risk |
|---|---|---|---|
| **O1 (recommended): explicit 7-field request union (DM022 LOW pattern) for ordinary path** | New narrow interactive/manual entry takes full-union 7-field rows; OLD fallback same-ID only; reuse unchanged `survey_completeness_v2` + `survey_evidence_v2` validators; no Profile rewrite | Operator decision + OLD + Discovery/ledger; accepted Profile/old artifacts untouched; no new framework/Gate | Minimal new IO + validator reuse; operator burden per expansion; unknown: request UX + regression volume |
| O2: Profile-owned initial extend (versioned) | New Profile version adds named IDs with Profile-authored `dim/desc`; historic Profile KEEP; no silent rebinding | Profile authority; old Profile bytes retained | Clean semantics; heavier versioning + migration; unknown: Profile lifecycle cost |
| O3 (legitimate manual): edition-local mechanical rows through unchanged validator | As TS-001: append exact Discovery rows with mechanical bindings, submit to frozen validator; Core unchanged | Operator + Discovery/ledger; no Core change | Viable now; not generic repair; unknown: per-edition labour |
| O4 (rejected): builder auto-fill / allowlist relax / alias rename | — | — | Forbidden: invents semantics, hides gaps |

No gratuitous generic obligation framework, no new Gate, no `production.verify_state_basis` substitution,
no canonical overwrite/rebind-by-hash (contract §4/§11).

## 6. Footprint (estimated, not code), compatibility, oracles

Finite footprint (~8-12 files + 3 schemas): `run_evidence_v2_interactive.py`
(`_validate_completeness_input`, `_build_completeness` signatures), `survey_completeness_v2.py`,
`survey_evidence_v2.py`, `survey_production_v2.py` (`validate_profile`), `survey_screening_v2.py`,
`survey_research_authority_v2.py` (LOW reuse), Selection/Architecture/Draft resolvers (callers only,
no semantic change), schemas `survey-production-profile`, `profile-completeness-result`,
`dm022-revision-request-v2` (+ operator request wiring). Compatibility: old inputs still validate
(old union unchanged); schema family byte-identical forward history (precode §5.1); Current-proof
closures unchanged (LOW detached proof, no State recursion). Failed/resume normal writers keep
existing guard/completion/refuse semantics; no unselected operations.

Limitations: source-read only, no runtime proof; EFF-O13/14/15 rows not re-read (secondary);
Thematic 10-type (DM016) out of scope; no numeric work-saving claim.
Positive oracle: Thematic expansion with 1 new GAP_FILL ID → request with operator `dim/desc` passes
full validator + Selection; missing request ID → exact-set refuse. Negative oracles: empty `dim/desc`
with no OLD row → refuse; invented dimension → refuse; dropped named ID → `silently dropped` error;
relaxed allowlist → must still refuse. Unknown costs: operator authoring, Thematic closure re-proof,
representative Weekly+Thematic+Period regression, audit overhead.

### Root questions for decision

1. Select O1 vs O2 for the ordinary initial-production path (O3 remains legitimate manual)?
2. Confirm OLD-fallback scope (same-ID only) and refusal when genuinely-new ID lacks operator `dim/desc`?
3. Confirm no Profile rebinding, no new framework/Gate, no DM016 batching in this unit?
