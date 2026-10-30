# DM017 R2 contract correction — minimal 3/5 nested input (DESIGN ONLY)

Status: DESIGN ONLY, no code/tests/runtime/network/Git/Human readback.
Preserves `named-obligation-applicability.md/json` (R1); this file corrects the
repair contract per ROOT: not 8–12 files + 3 schemas. Baseline `774dd39a`.
Read-only source `/tmp/opencode/jgas-dm022-indep-20261029T235900Z/proof-candidate`
(final133/768, patch `25b48878`). Contract `a345bb95` §11, precode `0425c530` §5 unchanged.

## 1. Actual ordinary call sequence (source-grounded)

`run_evidence_v2_interactive.py` `run()` (`:600-811`):

1. ENTRY guard + State check `:610-623` (`validate_agent_state`, `CANDIDATES_NORMALIZED`,
   `_dm022_require_ready` guard-absence; PREARCH triplet refuses `:624-631`).
2. Discovery basis `:632-648`: `discovery.validate_acceptance` → `screening.resolve_active_screening_acceptance`
   `:637-640` → `screening.resolve_effective_discovery_basis(... accepted_root_path=root_discovery_path)`
   `:641-646` → `discovery_path = effective["path"]`, `discovery_records = effective["records"]` `:647-648`.
3. `prepare_evidence_package(... discovery_path, screening_acceptance_path, ... supplement_manifest_path)` `:653-661`
   → `package["tasks"]`, `task_meta`, `expected_ids = set(task_meta)` `:663-664` (non-DROP task DIDs).
4. `validate_interactive_input(doc, profile, expected_ids, task_source_ids)` `:674-676`
   → inside, `_validate_completeness_input(value["completeness"], profile)` `:309`.
   Discovery records are **already available** at this point (`discovery_records`) but **not passed**
   to the completeness input validator — the gap. Card building, Evidence/Views accepts, Ledger build,
   then `_build_completeness(..., discovery_records, ledger_path, ledger, completeness_input)` `:767-775`
   follow, each preceded by prepublish `_dm022_require_ready` `:694,727,748,764,805`.
5. Late: schema-gate + `validate_profile_completeness` `:776-794`, archive `:806`.

So the fix point is step 4: thread the SAME validated `discovery_records` (+ ledger task universe,
already derivable) into completeness input validation/derivation. No new policy flag, no
caller-verified dict.

## 2. Universe `U` derivation (same validated basis, no retype)

- `U = profile.initial_ids ∪ ALL named in effective records`
  (`effective["records"]`, not a second fetch). `effective` mode is `DIRECT` or `DERIVED_EXPANSION`
  (`survey_screening_v2.py:353-439`). In expansion, `records` = derived records,
  `root_records` = accepted root; `validate_discovery_expansion:243-322` already enforces
  child ⊆ parent-union and full parent closure. Named universe therefore includes expansion-added IDs
  (e.g. GAP_FILL `EFF-O13/14/15` class) while forbidding invented IDs outside parents.
- Supplement manifest (`prepare_evidence_package:563-591`) adds Evidence Authority Supplement
  **sources**, not Discovery IDs; it does not extend `U`. Supplement DIDs still resolve through the same
  `effective` Discovery + `task_source_ids` binding (`:665-672`).
- `discovery_ids`/`evidence_task_ids` for final rows are **derived internally** from the same
  `discovery_records` declaring map + `ledger["rows"]` task map (LOW pattern
  `survey_research_authority_v2.py:1898-1908`), never retyped by the operator.

## 3. ROOT candidate: 3/5 nested in existing `completeness.obligations` array

No new top-level catalog, no Profile rewrite, no new Gate, no final-7-field/schema change.
Final rows stay exactly 7 fields (`profile-completeness-result.schema.json:27`).

| Input row class | Allowed shape (exact set) | `dimension/description` | `discovery_ids/task_ids` |
|---|---|---|---|
| `oid ∈ initial_ids` | Exactly `{obligation_id,status,rationale}` (3) | Forbidden in input; taken from Profile | Derived internally (declaring DIDs or `[]` if profile-only) |
| `oid ∉ initial, oid ∈ named` | Exactly `{obligation_id,status,rationale,dimension,description}` (5) | Required, non-empty; `dimension` must be a declared Profile dimension | Derived internally; operator must not supply |
| Any other `oid` | Refuse (extra) | — | — |

Rules: exact cover `set(input) == U` (dupe/extra/omission refuse); `status ∈ {SATISFIED,LIMITATION,NEEDS_RESEARCH,NOT_APPLICABLE}`
explicit for every `U` member (no autostatus); `rationale` non-empty; same-ID initial cannot redefine
semantics — a 5-field row whose `oid ∈ initial_ids` is refused (unambiguous 3-for-initial / 5-for-named-only;
no silent 5-with-exact-identity acceptance); named-only `dimension` must satisfy
`_validate_obligation_shape:62-63` + non-empty `description`.

## 4. No OLD Completeness in ordinary generation; DM022 schema note

Ordinary path creates `profile-completeness-v2.json` only if absent (`:763-766` refuse-overwrite);
no OLD artifact exists yet, so no OLD fallback is required or allowed. DM022 7-field request schema
(`dm022-revision-request-v2.schema.json:232-244` `fullObligation` requires `dimension/description`
`minLength:1`) plus LOW fallback (`survey_research_authority_v2.py:1886-1897` fill-empty-from-OLD)
means the empty-fallback branch is **dead under schema validation** (`load_revision_request`
validates schema before Python fallback): a missing/empty `dim/desc` fails schema first and never
reaches the fallback. State this to avoid misstatement; DM022 keeps its separate 7-field + valid-OLD
contract, ordinary path uses §3 with no OLD.

## 5. Exact API change (minimal) + caller count + guards

Proposed (names illustrative, ROOT confirms):

- `_validate_completeness_input(value, profile, discovery_records)` — add one required positional
  `discovery_records: list[dict]`; compute `U` internally; enforce §3 shapes + exact cover. No policy flag.
- `validate_interactive_input(value, profile, expected_ids, task_source_ids, discovery_records)` —
  add one required `discovery_records`, forward to above. Call-site `:674-676` already holds
  `discovery_records`; change is one added argument.
- `_build_completeness(...)` signature **unchanged** (already receives `discovery_records, ledger`);
  only its input-row handling branches on 3- vs 5-field per §3, then derives bindings as today `:499-508`.

Caller count: production `validate_interactive_input` 1 site (`:674`), `_build_completeness` 1 site
(`:767`); test 1 site (`tests/test_run_evidence_v2_interactive.py:101`); adapter
`run_evidence_v2_agent_first.py:81-98` monkey-patches `_build_completeness` only (compatible: same
signature, new input shapes flow through). No caller-verified dict, no new CLI flag.
Namespace/guard preserved: ENTRY `:623`, prepublish `:694,727,748,764`, late `:805`
`_dm022_require_ready` calls untouched; `O_NOFOLLOW/O_EXCL` IO discipline unchanged.

## 6. Full-validator minimal trace (no over-claim)

Existing `_check_profile_completeness_extra_content:213-236` enforces lower bounds: all named present
(`:221-223`), each named row covers its declaring DIDs (`:232-236`), initial present + dimension match
(`:207-212`); it does **not** enforce extra-obligation refusal nor exact-DID equality (extras beyond
declaring pass shape/unknown checks). Proposed §3 input gate adds exact-cover at entry, so the full
validator stays unchanged and still catches drift. Proposed internal derive must be exact
(`dids = sorted(declaring.get(oid, []))`, profile-only `[]`) and must **not** drop old-permitted
initial-linked DIDs (current `_build_completeness:499-508` already links initial IDs to declaring DIDs;
keep that). `NOT_APPLICABLE`/`NEEDS_RESEARCH`/missing status stay explicit per-row; no autostatus.

## 7. Comparison + recommendation

| Option | Operator work | Collision/versioning |
|---|---|---|
| **3/5 nested (this correction, recommended)** | Types only `status/rationale` (+`dim/desc` for named-only); no derived-field retype | Single array; no dual-source collision; version = input shape only |
| 2 arrays (definition catalog + 3-field decisions) | Two places to keep in sync per ID | Catalog-vs-decision skew, extra top-level versioning |
| Full-7-row O1 (R1 file §5) | Retypes `discovery_ids/task_ids`, invites drift vs internal derive | Operator bytes can collide with ledger/Discovery truth |

Recommend 3/5 nested as source-grounded most minimal: it matches the actual gap (input validator
blind to Discovery), reuses the actual derive site, and leaves final 7 fields, Profile, schemas,
and downstream consumers untouched.

## 8. Downstream, backcompat, coupled item

No Selection/Architecture/Draft change: they consume final 7-field Completeness via active resolvers
(`run_selection_architecture_v2_interactive.py:70-109`, `survey_architecture_v2_base.py:93-180`,
`run_drafting_synthesis_v2_interactive.py:98-129`); no new input fields propagate. Do not claim
schema-family/closure unchanged without the affected own-epoch map (precode §5.1 family pin scope).
Backcompat: old 3-field-only inputs validate **iff** Discovery adds no IDs (`U == initial_ids`);
otherwise refuse with missing-named (no silent green). Unchanged Profile/raw accepts still hold.
DM016 10 source types remain separately needed at the same Evidence entry
(`SOURCE_CLASS_MAP:49-56` vs 10 Thematic types) but no maintenance batch in this unit.

### Root questions

1. Confirm 3-for-initial / 5-for-named-only with exact-cover + internal derive (§3–§5)?
2. Confirm refusal (not exact-identity tolerance) for 5-field rows on initial IDs?
3. Confirm dead-fallback reading of DM022 schema vs LOW code, keeping DM022 contract separate?
