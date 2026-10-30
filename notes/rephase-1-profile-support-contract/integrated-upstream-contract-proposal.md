# Integrated upstream contract proposal — DM016 + DM017 + adapter parity (DESIGN ONLY, contract selection)

Status: **DESIGN ONLY, contract selection. NO code/runtime/tests/Git/network/Human readback.**
Preserves all previous unchanged:
`source-class-applicability.md/json` (R1 NOT selected),
`source-class-contract-correction.md/json`,
`named-obligation-applicability.md/json` (R1 O1 superseded for ordinary path, preserved),
`named-obligation-contract-correction.md/json` (R2 3/5 direction kept, §§2/5 corrected below),
`route-requirements-and-disposition.md/json` (Author C, conditional PASS),
`independent-obligation-contract-review.md` (DESIGN_NOT_READY, §§1–4 binding),
`intake-20261030T124140Z/` (4 docs, DATA text-read only, `DATA.run_frozen_evidence_chain.py` never executed).
Baseline `774dd39a` fixed. Source-read only final133 proof
`/tmp/opencode/jgas-dm022-indep-20261029T235900Z/proof-candidate`
(patch `25b48878…4931836B`, manifest `31fa4a72…`, 133 paths/768 files).
Contract `a345bb95` §11 + precode ROOT `0425c530` §5 unchanged.
Task authority assessment §5 (`outputs/rephase-1-dm022-prearchitecture-implementation-assessment.md:52-60`).
Code permission **BLOCKED** until ROOT + independent concrete pre-code map confirms interfaces.

## 1. DM016 — fixed canonical map 10 EXACT per defect RECOMMENDED (NEW design, NOT historical authority)

Defect source `DATA.shared-core-evidence-source-map-gap-20260922.md:§2`
(blob `d9f58479…`, sha256 `7a3c89dd…`), corroborated counts by
`DATA.validation-report.md:§2` (projected 67 / passthrough 93, per-type identical).
This is NEW design ROOT may select; do NOT cite as historical canonical authority.

| EXACT literal (preserve) | Selected class | Count (defect §2 / validation §2) |
|---|---|---:|
| `PRIMARY_DOC` | `PRIMARY_OFFICIAL` | 13 |
| `PRIMARY_REPO` | `PRIMARY_REPOSITORY` | 21 |
| `PRIMARY_ANNOUNCEMENT` | `PRIMARY_OFFICIAL` | 8 |
| `PRIMARY_MODEL_CARD` | `PRIMARY_OFFICIAL` | 6 |
| `PRIMARY_SPEC` | `PRIMARY_OFFICIAL` | 4 |
| `SECONDARY_REFERENCE` | `SECONDARY` | 8 |
| `SECONDARY_TECHNICAL` | `SECONDARY` | 4 |
| `RUNTIME_RECIPE` | `PRIMARY_OFFICIAL` | 1 |
| `PACKAGING_DOCS` | `PRIMARY_OFFICIAL` | 1 |
| `RUNTIME_PR` | `PRIMARY_REPOSITORY` | 1 |
| blocked total / runnable (`PRIMARY_PAPER` 92 + `x-community-signal` 1) | — | 67 / 93 |

Rules (ROOT):

- `source_class` = resource provenance for the resource's own statement/proposal.
  NOT model-vendor status/weights/mergedness/performance; NOT claim truth
  (`evidence_class` + `verification.targets` remain claim strength).
- No generic `PR-never-Primary` / default-`SECONDARY` / conditional-iff map.
  `current_source_class` accepts type only (simple map admission).
  Correction `§2` ambiguous/conditional wording is NOT selected.
- ALL old mappings in `survey_evidence_v2.py:44-109` unchanged; new literals append only.
  Preserve original `source_type` in Discovery (`survey_discovery_v2.py:84-153`,
  `survey_screening_v2.py:49-60` `SOURCE_KEYS`) and tasks
  (`survey_evidence_v2.py:601-621` `source_records=[discovery source]`, open passthrough).
  No URL-sniff (`run_special_interactive_evidence.py:41-47` rejected),
  no alias/projection ledger, no new module.
- Intake 4 docs are class-recommendation only; per-record Raw not read in scope
  (intake-summary `§§3-5`). Tests require genuine-type representation +
  independent research semantics, NOT machine `CLAIM-verified`.
- Dead local 6 map `run_evidence_v2_interactive.py:49-56` + helper `:110-114`
  delegates to canonical OR is removed after caller proof (grep 3 hits 49/110/111,
  zero in-file calls; `_build_card:321` + `:666` use canonical
  `evidence.task_authority_sources:413-446`). NOT an active Weekly gap.
- Unknown `source_type`: early canonical classification preflight BEFORE accepted
  Screening/package writes on all v2 Discovery records bound to validated
  root/effective (`resolve_effective_discovery_basis:353-439` returns
  `root_records` + `records` together); Discovery archive open retained,
  unknown = explicit refusal, NOT coerced `DROP` shortcut. Same check early in
  Evidence (`prepare_evidence_package:539-681`, `task_authority_sources:413-446`
  via `_source_class:177-184`) before owned writes for historical/preexisting unknown.
  No legacy 4-enum schema edit (`screening-record:12`, `evidence-task:25` are v1 path),
  no supplement `SOCIAL` addition (`evidence-authority-supplement-v2:60-61` optional path,
  possibly deliberate policy).
- Callsite predicate pinned: `task_authority_sources:422-423`
  `_source_class(source.get("source_type"))` + supplement `:304-305`
  `source_class==_source_class(source_type)`. Cycle safety: `survey_evidence_v2.py:21`
  top-level imports `screening`; `survey_screening_v2.py:397` uses function-local
  `from scripts import survey_discovery_v2`. Any Screening→Evidence preflight MUST be
  function-local, never top-level; no new dep-membership/fingerprint claim unless
  verified in pre-code.

## 2. DM017 — 3 initial / 5 named-only exact array, full-7 result unchanged

Select R2 3/5 nested (`named-obligation-contract-correction.md:§3`) with review §§1–2 corrections:

- Input `completeness.obligations` array only; final rows stay exact 7
  (`profile-completeness-result.schema.json:27`, `OBLIGATION_KEYS` at
  `survey_completeness_v2.py:25-33`).
  `oid ∈ initial` → exactly `{obligation_id,status,rationale}` (3);
  `oid ∉ initial ∧ oid ∈ named` → exactly `{obligation_id,status,rationale,dimension,description}` (5,
  non-empty, `dimension` ∈ declared Profile dimensions per `_validate_obligation_shape:62-63`);
  any other `oid` → refuse; exact cover `set(input)==U`; dupe/extra/omission refuse;
  5-field on initial ID → refuse (not tolerance); `status ∈ {SATISFIED,LIMITATION,NEEDS_RESEARCH,NOT_APPLICABLE}`,
  `rationale` non-empty, no autostatus.
- REQUIRED `U := initial_ids ∪ named(root_records) ∪ named(effective records)`,
  both from SAME already-resolved `resolve_effective_discovery_basis` dict
  (`run_evidence_v2_interactive.py:641-648` already holds both; no second fetch).
  Compact acceptance `records` (normalized `parent_edges`/`raw_refs`, cf.
  `survey_discovery_v2.py:139-153` vs canonical JSONL `provenance`/`source`) NEVER a `U` source.
  Supplement manifest (`prepare_evidence_package:563-591`) adds sources, NOT Discovery IDs.
- Existing expansion forbids new OIDs: `validate_discovery_expansion:243-322`
  enforces child ⊆ parent-union (`:303-311` invented→refuse) + DID closure (`:313-318`);
  `EXPANSION_REQUIRING_PARENT:37-43` excludes `GAP_FILL/BASE/CARRY_OVER`
  (`:272-275`), so derived cannot add `GAP_FILL`; `GAP_FILL EFF-O13/14/15`-class enters as
  root named only. R2 "expansion-added IDs" wording is erratum; canonical gap-fill /
  root Discovery expansion ≠ `DERIVED_EXPANSION`.
- Per-parent declaration preservation (beyond global set): every `(parent,oid)` with
  `oid` in root `provenance.obligation_ids` MUST be represented by a valid child
  containing `oid` with `parent` in actual `provenance.parent_refs` (source field at
  `survey_screening_v2.py:144-159`, `survey_discovery_v2.py:96-115`; NOT invented),
  or by an unchanged root record. Global DID accounting (`accounted_root_ids==root_ids`)
  alone is insufficient (review §1 counterexample). Loss gate before Evidence writes:
  `lost = named(root)-named(effective)` (+ per-parent uncovered) → refuse
  (`DECLARATION_LOSS`), no auto-add, no accepted-child rewrite (acceptance immutability
  `validate_acceptance:897-916`, `accept_results:919-979` digest). On pass `U` collapses
  to `initial ∪ named(effective)`; downstream unchanged.
- Final-row derive: effective DIDs only (`sorted(declaring.get(oid,[]))`);
  initial-only with no declaring DID → `[]` allowed (`_unique_string_list` allows `[]`,
  LOW `:1900-1909` pattern); shared-OID parent coverage explicit per above;
  `evidence_task_ids` derive exact ledger map (`ledger["rows"]`, LOW `:1898-1908` pattern
  in `survey_research_authority_v2.py`), never retyped by operator.
- Signatures (keyword-only, SyntaxError fix per review §2):
  `validate_interactive_input(value,profile,expected_ids,task_source_ids=None,*,discovery_records,root_discovery_records)`
  + `_validate_completeness_input(value,profile,*,discovery_records,root_discovery_records)`.
  Outer runner derives validated full canonical JSONL itself (SHA/count/schema via
  `screening.read_jsonl` + `validate_discovery_set`, cf. adapter `:46-49`), NOT a
  caller-provided verified token. `_build_completeness(repo_root,profile,profile_path,discovery_records,ledger_path,ledger,input_value)`
  signature stays; only 3-vs-5 branch + internal derive change; root-loss check before create.
  No OLD fallback in ordinary path (completeness absent-checked `:763-766`);
  DM022 existing-7 `fullObligation` schema (`dm022-revision-request-v2:232-244`,
  `minLength:1`) unchanged; LOW empty-fallback `:1886-1897` dead under schema-first load
  (`load_revision_request:1149-1162`) noted only.
- Callers pinned: `validate_interactive_input` prod 1 (`:674-676`), test 1
  (`tests/test_run_evidence_v2_interactive.py:101-106`), frozen edition driver
  (`DATA.run_frozen_evidence_chain.py:166-167`, edition-local NOT Core);
  `_build_completeness` prod 1 (`:767-775`), adapter wrapper 1 (`run_evidence_v2_agent_first.py:88-91`),
  frozen driver 1 (`:222-223`); `_validate_completeness_input` internal 1 (`:309`).
  Writer discipline: ordinary Ledger/Completeness refuse-overwrite is
  exists-or-symlink check (`run():749-750,765-766`); NO invented `O_NOFOLLOW` writer claim
  for this path (exclusive `O_EXCL/O_NOFOLLOW` lives in other modules, unverified for this unit).

## 3. Adapter parity (direct/agent-first, NOT unrelated cleanup)

Source `run_evidence_v2_agent_first.py:33-52,55-99`:

- `acceptance_with_canonical_discovery_records` = validate accepted →
  `sha256_file(discovery_path)==accepted["discovery_sha256]` →
  `screening.read_jsonl` + `validate_discovery_set(records,issue_id)` →
  `len==record_count` → substitute `result["records"]=records` (compact lacks
  `provenance` needed by `_build_completeness:499-540` + `survey_completeness_v2.py:101-119`).
- `completeness_with_preserved_residual_limitations:55-76` = if `THEMATIC`, union
  `residual_limitations` into `closure.limitations` (truth-preserving, no omission).
- `main:80-99` mutable monkey-patches `runner.discovery.validate_acceptance` +
  `runner._build_completeness`, calls `runner.main()`, restores in `finally`.

Contract: canonical direct runner normalizes SAME two steps itself so both entries
produce valid rows with no fabricated provenance/branch: (a) direct `run():632-648`
already holds validated effective canonical JSONL — state compact-never-`U` + self-derive
SHA/count/schema explicitly; (b) fold residual-union into ordinary `_build_completeness`
as required existing validator contract (adapter docstring + Thematic closure rule),
adapter becomes thin delegation or preserves compatible helpers without mutable
monkey-patch IF source-read proves no external dependency (argument tuple
`(repo_root,profile,profile_path,discovery_records,ledger_path,ledger,input_value)`
preservation at `:767-775` vs wrapper `*args/**kwargs`). Parity prerequisite for
Weekly/Thematic/Retro, not cleanup.

## 4. Scope — FIRST bounded unit UPSTREAM only

Weekly/Thematic/Retro research Profiles through actual existing downstream consumer
paths (`run_selection_architecture_v2_interactive.py:70-109`,
`survey_architecture_v2_base.py:93-180,287-352,860-909`,
`run_drafting_synthesis_v2_interactive.py:98-129,215`,
`survey_longform_derivation_v2.py:1069-1070`, readers via `Views/Ledger` validators).
Does NOT generalize fixed four-family IR
(`FORMAT="THEMATIC_FOUR_FAMILY_LINEAGE_V1"`, `FIXED_TITLE/EDITION/FINAL_HEADING/TOC_TITLE`
+ 4-model cross-table at `survey_longform_derivation_v2.py:109,118-136`) or claim
manual complete-reader/correction. Non-four-family Thematic / Retro full-reader +
normal correction stays REQUIRED future gate; `DIRECT_PRIMARY` `PRIMARY_ONLY`
(`survey_reader_surface_gate_v2.py:1352-1356`, byte-hash NOT complete-reader `:1335-1349`)
preserved; custom Retro `--spec` CLI allowed if Human-authorized, no extra engine
(`survey_period_v2.py:193-216`); Foundations planning-only, NOT new Profile
(`survey_x_intake_v2.py:86,152-154`). No silent Special narrowing/alias/drop.

Footprint (estimate, pre-code must confirm): NO 3-new-schema budget; likely
`survey_evidence_v2.py` (map + `_source_class` + `task_authority_sources`),
`survey_screening_v2.py` (preflight + loss gate + effective basis),
`run_evidence_v2_interactive.py` (validators + `_build_completeness` + residual fold),
`run_evidence_v2_agent_first.py` (thin), tests/docs only. Pre-code must confirm
closure/source-families/current-vs-history (precode §5.1 family pin), not claim unchanged.
No new source-family ID guess.

## 5. Oracles / alternatives / cost / next

- Positive: multi-source/multi-DID package (Weekly 4 + ≥3 newly admitted Thematic
  literals across ≥2 DIDs; supplement + Discovery-bounded mix; ledger row per DID);
  Thematic expansion with 1 root `GAP_FILL` named-only 5-field row passes full validator
  + Selection; residual limitation survives into THEMATIC closure via both entries.
- Negative: unknown literal → `unsupported source_type` refuse pre-write
  (`_source_class:177-184`, `task_authority_sources:423`); class-drifted card →
  refuse (`validate_evidence_card:965-1055`); alias-labelled input → refuse;
  missing named → `silently dropped` refuse (`survey_completeness_v2.py:209,221-223`);
  per-parent uncovered → `DECLARATION_LOSS` refuse; extra/dup/omission → exact-cover refuse;
  5-on-initial → refuse; invented dimension → refuse; compact-acceptance as `U` → refuse path.
- Legitimate alternatives: (A, selected) centralize canonical map + 3/5 nested + residual fold;
  (B) versioned Profile-owned initial extend (clean semantics, heavier versioning);
  (C) edition-local mechanical rows via unchanged validator (TS-001 / frozen-driver pattern,
  viable now, NOT generic repair); (D, rejected) task-stage projection/alias/allowlist-relax
  (destroys provenance, verifies projection not original). No batch maintenance, no new Gate,
  no `production.verify_state_basis` substitution, no canonical overwrite/rebind-by-hash.
- Cost UNKNOWN (no numeric saving/date): per-literal collector + genuine-oracle cost;
  full cross-profile regression volume; manifest/fingerprint review; operator authoring burden;
  translation-table cost N/A (no table selected). No shared-Core code in this unit.

Next: ROOT selects → independent concrete pre-code map (old/new producer input schemas,
version compat, classification-unknown-before-writes, expansion-loss, multi-DID, guards,
import-closure) → independent review → Human Commit Point. No implementation now.

## 6. Remaining essential design question (BLOCKING, do NOT assert complete)

1. `RUNTIME_RECIPE / PACKAGING_DOCS / RUNTIME_PR → PRIMARY_*` per RECOMMENDED table
   has NO per-record Raw/publisher bytes in 4-doc scope (intake-summary §3: 1 task each,
   vLLM-recipe / llama.cpp-PR-27742 associations UNVERIFIED, PACKAGING counterpart
   unidentified). Correction flagged PR-unmerged/ambiguous-publisher risk. If genuine-type
   representation + independent research-semantics oracle (collector + `raw_refs` +
   `published/accessed` instants + publisher identity + claim binding per literal) cannot be
   produced at contract time, must those 3 stay fail-closed `SECONDARY`-or-refuse rather than
   admit as `PRIMARY_*`? Do NOT assert PRIMARY authority until oracle closes; needs ROOT ruling
   before pre-code membership/fingerprint claims.

Evidence bounds: source-read only; no runtime proof; EFF-O13/14/15 rows from frozen driver
`EXTRA_OBLIGATIONS` (Luna provisional, NOT DM017 satisfaction); W34 gap-fill siblings
(`:80-108`) cited as precedent only; `b650`-era pins untouched; whole NOT_READY/step4B3 OPEN.
