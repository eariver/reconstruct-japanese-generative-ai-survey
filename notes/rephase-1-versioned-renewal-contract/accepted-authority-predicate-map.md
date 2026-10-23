# Accepted-authority predicate map — versioned same-reader renewal (author-side DESIGN ONLY)

2026-10-23 JST. Author-side bounded DESIGN supplement to selected
`outputs/rephase-1-versioned-renewal-contract-decision.md` §§4/9 and independent
technical review B3. No code/tests/build/fixture/Git/network/source mutation.
Read-only source is `.rephase-1-editorial-runtime/final-source-packaging/proof-copy/candidate-partial-b40de60`
(= actual409/tree8ce + intended57, applied state; manifest/patch pins adopted from
`notes/rephase-1-versioned-renewal-contract/source-observation.md`, not re-hashed here).
This file is the ONLY write in this unit. Original sources preserved.
No independence claim; root uses this to resolve B3.

## 0. Loader contract (finite, pre-code)

### 0.1 Proposed path-based signature

```text
load_renewal_accepted_authority(root: Path, basis_path: Path) -> {surface, records, accepted_refs, authored_refs}
```

- `root`: repo root. `basis_path`: repo-local path to `R/renewal-basis.json`
  (`R = P/renewals/<renewal_id>`). Both validated as repo-local no-follow paths.
- Basis is untrusted data fully reloaded on every use: strict JSON
  (duplicate-key refusal), new basis-schema validation, `basis_sha256`
  canonical-without-itself recompute. No caller-supplied dict, verified set,
  `pending_basis`, `already_verified`, route/kind enum, `seal_path` shortcut,
  ambient context, or cache.
- Leaf resolves every accepted input ONLY from basis-pinned
  `{path,sha256[,byte_count]}` refs (evidence-acceptance, candidate-matrix,
  materiality-ledger, discovery, architecture, draft synthesis-input/result,
  per-package draft-package/result, profile, authored inputs, archive).
  Path must equal recorded path exactly; `sha256(file) == ref.sha256`
  (+ `len == byte_count` where sized). Same-SHA different-path refused.
- Existing current loaders stay semantically unchanged:
  `survey_weekly_derivation_v2.load_derivation(root,state_path,authored_path,pending_basis)`,
  `survey_longform_derivation_v2.load_derivation(root,state_path,authored_path)` and
  `load_derivation_for_readback(...)`. No signature/behavior change.
  The renewal leaf is NEW narrow extracted primitives (justified below),
  not a flag on the current loaders, not a monkeypatch.

### 0.2 Leaf bans (hard)

The leaf MUST NOT call, import-for-call, or transitively trigger:

- current State validation/selection: `agent.validate_agent_state`,
  `agent._validate_agent_state`, `agent.built_checked_pending_publication_basis`,
  `agent.resolve_checkpoint_artifact`, `agent._resolve_checkpoint_artifact`,
  `core.verify_state_basis`, `runtime_tool.current_stage_basis_override`,
  `resolve_active_screening_acceptance`, `resolve_effective_discovery_basis`
  State-bound branch, `observe_current_authority` / `observe_renewal_authority`
  (high-only), any `pending_basis` plumbing.
- Reader/Gate/Candidate: `build_reader_input` is allowed ONLY as pure projector
  after all authority checks (see F1/F2); `validate_reader_input` /
  `validate_longform_reader_input` allowed as pure schema+route check;
  `render_main`/`render_bibliography`/`validate_generated_closure` and Longform
  projection/archive-authorization/canonical-bytes/render helpers allowed as pure.
  No `survey_reader_publication_v2`, `survey_reader_surface_gate_v2`,
  `survey_publication_v2`, `survey_quality_v2` builder, Gate derivation,
  Candidate assembly, seal, P1/P2R/P3S/full receipt.
- No `implementation_sha` parameter from caller. No historic SHA passed to a
  current helper. Where current helpers take `implementation_sha` solely for
  `verify_state_basis`, the extracted primitive drops that parameter entirely
  (F3/F4). `current_tools`/`contract`/`closure` are NOT checked in this leaf;
  they belong to the history evaluator (§3 of decision) and high
  `observe_renewal_authority`. Lifecycle State (`VALIDATED_DRAFT`,
  Architecture approved, Preview pending, no decided Preview/Freeze/Release,
  no Exception, Profile binding, checkpoint selection) is checked OUTSIDE
  the proof by high `observe_renewal_authority(root,state_path,basis_path)`,
  before capture/finalize/activation with pin rechecks. Detached readback
  validates retained before-State, never requires live-before equality.

Allowed callees: `core.load_json`/`sha256_file`/`sha256_object`/`sha256_bytes`/
`repo_local_path`/`parse_instant`, `schema_gate.load_and_validate_json`/
`validate_instance`, `citation_refs.refs`, `drafting.validate_synthesis_result`/
`validate_draft_result`, `provenance.resolve_source_access_provenance`,
pure validators listed in §1, bounded `O_NOFOLLOW` reads with `_safe`-equivalent
discipline. File IO remains (repo-local regular files only, no symlinks,
no Git, no network, no writes). Git blob reads belong to the historian,
not this leaf.

## 1. Source-read predicate inventory

`H` = exact historical input authority (basis-pinned path+SHA, live-retained bytes).
`C` = freshly validated current content (content predicates re-executed in leaf).
`S` = current State/HEAD predicate extracted (must NOT run in leaf) → replacement binding.
`R` = predicates/IO that remain in leaf. All line refs are proof-copy `scripts/` observations.

### F1 — Weekly derivation entry and records

- Funcs: `_strict_evidence_sources:196-217`, `_records_from_authorities:220-272`,
  `build_reader_input:300-394` (pure projector), `validate_reader_input:397-407`,
  `render_main:414-456` / `render_bibliography:459-475` / `validate_generated_closure:478-486` (pure),
  `load_derivation:489-584`, `current_closure:587-588`, `_verify_head_bytes:591-645`,
  `_inspect_receipt_envelope:683-710`, `verify_closure_at_commit:713-738`,
  `validate_receipt:740-787`.
- H: checkpoint artifact paths+SHAs for architecture, synthesis-input/result,
  per-package draft-package/result (`accepted()` at `511-555`), evidence-acceptance,
  candidate-matrix, materiality-ledger, discovery-acceptance (`556-559`);
  matrix `basis.evidence_acceptance_sha256` + `materiality_ledger_sha256` bindings
  (`231-234`); acceptance `results[]` rows; Evidence card files under
  `acceptance_parent/results/<filename>`; Draft authored archive
  `source_root/draft/v2/interactive-drafting-synthesis-input.json` (`529`);
  authored input file.
- C (must be preserved State-free): synthesis-result validity
  (`522-526` via `drafting.validate_synthesis_result`); per-package draft-result
  validity (`542-544`); draft/archive drift (`546-547`, headline/deck equality
  `327-328`, `citation_refs.refs` deck/block placement `329-356`, section_label
  `362-364`); matrix↔acceptance status equality (`254`), matrix↔ledger materiality
  (`256`), discovery existence + `source_locator` non-empty (`257-262`), card
  `sources` non-empty (`210-211`), card SHA drift (`206-207`), per-DID duplication
  (`214-215`, `252`, `240`), title non-empty (`247-249`),
  `provenance.resolve_source_access_provenance` (`266`); bibliography HOLD/
  NEEDS_MORE refusal + missing-DID refusal (`375-377`); `_validate_authored_input`
  envelope (`160-195`), `_closing_summary` required+source (`285-297`),
  `closing_text in final_summary.paragraphs` (`320-321`), `_window` (`145-158`);
  `validate_reader_input` route/Profile shape (`405-406`); pure renders + closure
  (`478-486`).
- S → replacement:
  - `agent.validate_agent_state/_validate_agent_state/pending_basis` (`495-503`)
    → DROPPED in leaf. Checked outside by high observation on live State.
  - `lifecycle DRAFT_COMPLETE` (`504`) + `profile research/publication_profile`
    (`508-509`) + `issue_id` linkage → DROPPED. Profile/issue/lifecycle checked
    outside; leaf checks `profile.issue_id == architecture.issue_id`-style
    file-label agreement only from basis-pinned bytes, plus `authored.issue_id`
    envelope, never live State.
  - `accepted(checkpoint,name)` via `resolve_checkpoint_artifact` (`511-514`)
    → REPLACED by basis-pinned `_load_basis_accepted_ref(root,basis,name)`:
    path+SHA from `renewal-basis.json:accepted_refs`, live SHA recheck, no State.
  - `core.repository_commit_sha(root)` as `implementation_sha` (`562`) +
    `current_stage_basis_override(pending_basis)` (`200`) +
    `validate_evidence_acceptance(...,implementation_sha)` (`201`) +
    `_verify_head_bytes` / `verify_closure_at_commit` / `validate_receipt`
    → DROPPED in leaf. No HEAD/commit/Git in leaf. Tool/commit/contract belong
    to historian + high authority.
  - `evidence_sha` cross-package agreement (`548-552`, `560-561`) → REPLACED by
    basis-pinned `evidence-acceptance.sha256` equality: every draft-package
    `basis.evidence_acceptance_sha256` must equal `sha256(basis.evidence_path)`.
    Same predicate, different authority root (basis file, not live checkpoint).
- R: all C predicates + bounded file reads + strict JSON + SHA + `citation_refs` +
  `drafting` validators + `provenance` + pure projection/validation/render.
  No State, no HEAD, no Git, no pending, no override, no `implementation_sha`.

### F2 — Longform derivation entry and records

- Funcs: `_safe_card_path:345-364`, `_preflight_evidence_tree:365-~420`,
  `_longform_records:421-520`, `_validate_archive_authorization:530-581`,
  `build_longform_reader_input:608-~926` (pure projector), `validate_longform_reader_input:927-~948`,
  `canonical_reader_bytes:949-~956`, `_derive_authority_context:957-1098`,
  `load_derivation:1101-1139`, `load_derivation_for_readback:1142-1182`.
  Constants: `REQUIRED_LIFECYCLE DRAFT_COMPLETE:98`, `REQUIRED_ACTION:99`,
  `DIRECTIVE_REL:104`, `_GIT_OVERRIDE_VARS:151`, `READBACK_LIFECYCLES:954`.
- H: same checkpoint families as F1 plus `synthesis-input/result` (`984-985`),
  per-package `draft-package/result` (`1009-1010`), archive (`992-993`),
  `evidence/matrix/ledger/discovery` (`1054-1057`); card files via
  `_safe_card_path` containment; matrix `basis.*_sha256` bindings (`435-438`);
  authored longform envelope (`1077`).
- C: directive-lexical refusal (`970-974`); architecture schema validation
  (`981-983`); synthesis validity (`987-991`); per-package headline/deck/block
  drift + `citation_refs.refs` placement (`1019-1039`); `_validate_archive_authorization`
  exact package/block coverage + per-package citation semantics (`1053`, `530-581`);
  `evidence_sha` agreement (`1040-1044`, `1058-1059`); `_assigned_ids` + `_did`
  token check (`1061-1065`, `240-257`); `_longform_records` bindings
  (`443-488`: DID uniqueness, materiality, discovery existence, card SHA drift
  `456-457`, single-DID-per-card `462-465`, `card_sources` duplication `468-469`,
  matrix duplication `478-480`, status/materiality equality `481-484`,
  missing-card `487-488`); selected-only eligibility (`490-520`:
  `_resolve_primary_entity` URL validation, `provenance` resolution,
  `VERIFIED/PARTIAL` only `501-503`, HOLD refusal `504-505`); token subsets
  (`_ISSUE_ID:619`, `package_id:275`, `_bib_key:282`, `_check_url:289`,
  `_resolve_primary_entity:312-344`); pure projection + validation
  (`1078-1081`).
- S → replacement:
  - `_GIT_OVERRIDE_VARS` (`1110-1112`, `1154-1156`) + `cfg stage_plan handler ==
    REQUIRED_ACTION` (`1117-1118`, `1161-1162`) + `agent.validate_agent_state`
    (`1119`, `1163`) + `lifecycle == REQUIRED_LIFECYCLE` (`1122-1126`) +
    `next_action == REQUIRED_ACTION` (`1127-1131`) + readback allowlist +
    `terminal_reason` (`1166-1174`) + Profile route/issue checks (`1133-1138`,
    `1177-1180`) → ALL DROPPED in leaf. Checked outside by high observation.
    Leaf keeps only file-label agreements (profile/architecture/authored/
    synthesis `issue_id` equality, `research_profile THEMATIC /
    publication_profile LONGFORM_SPECIAL` as file-content equality from
    basis-pinned bytes, never from live State).
  - `accepted()` via `resolve_checkpoint_artifact` (`976-977`) → REPLACED by
    basis-pinned loader (same as F1).
  - `with current_stage_basis_override(): validate_evidence_acceptance(...,
    implementation_sha)` (`441-442`) + `implementation_sha =
    repository_commit_sha` (`1060`) → DROPPED (see F3/F4 State-free primitive).
  - `_preflight_evidence_tree` alias check (`431`) → RETAINED State-free
    (path containment, no State).
- R: all C + bounded reads + strict JSON/SHA + `citation_refs`/`drafting`/
  `provenance` + pure build/validate. No State/lifecycle/action/handler/Git/
  HEAD/pending/override/`implementation_sha`.
- Blocker note: `_preflight_evidence_tree` body beyond alias line was not
  line-verified here; pre-code must pin its exact State-free containment lines.
  No weakening allowed — if any line requires State, return exact blocker.

### F3 — Evidence package / acceptance validators

- Funcs: `validate_screening_acceptance:490-536` (called by Evidence),
  `_validate_task:684-716`, `validate_evidence_package_basis:719-846`,
  `validate_evidence_card:865-1049`, `accept_evidence_results:1059-1113`,
  `validate_evidence_acceptance:1116-1167`, plus `validate_edition_view:1170-1224`,
  `accept_edition_views:1231-~1287`, `validate_edition_views_acceptance:1288-~1330`,
  `validate_materiality_ledger:1410-~1479`, `validate_completeness:1487-~1607`,
  `task_authority_sources:413-~448`, `_screening_acceptance_digest:482-488`.
- H: `evidence-accepted.json` + sibling `package.json` (`511`, `1127-1128`);
  `package_sha256` binding (`511`, `1128`); Screening acceptance path+SHA in
  `package.basis` (`644-652`, `772-781`); task files + result files exact sets
  (`1138-1140`); card files.
- C: acceptance keys/identity/digest+dirname (`502-508`, `1121-1126`,
  `1164-1166`); package/tasks/result shape (`729-730`, `785-817`,
  `1144-1163`); `_validate_task` screening-basis SHA + single KEEP/MAYBE/INSPECT
  decision (`708-715`); `validate_evidence_card` exact `CARD_KEYS`,
  task/package basis hashes (`880-887`), entity/primary-subject (`895-901`),
  source authority binding (`916-966`: `task_authority_sources` or legacy
  unambiguous Discovery locator, `source_class`, supplement exact, `accessed_at`
  instant), temporal/claims/limitations/metrics/verification subject-role checks
  (`968-1049`); result/metadata divergence (`1162-1163`); edition-view and
  ledger/completeness predicates where invoked.
- S → replacement:
  - `core.verify_state_basis(repo_root,cfg,state,implementation_sha)` in
    `prepare_evidence_package:550`, `validate_evidence_package_basis:764-765`
    (+ via `validate_package_basis` inside `validate_screening_acceptance:514`)
    → REPLACED by basis binding: `package.basis.state_sha256 ==
    sha256(basis.retained_before_state_path)` AND `state_path ==
    basis.retained_before_state_rel` (retained COPY, never live State path).
    No `cfg/state/implementation_sha` in leaf. The narrow
    content-addressed exception (acceptance `package_sha256` binding) is
    reimplemented path-based: `sha256(package_path) ==
    acceptance.package_sha256` (`511`, `1128`) + `sha256(acceptance_path) ==
    basis.evidence_acceptance_sha256`, without `agent_tool_v2` wrapper.
  - `implementation_sha` param → DROPPED in extracted primitive
    (e.g. `validate_evidence_acceptance_statefree(root,acceptance_path)`).
    No historic SHA passed to current helper. Tool epoch belongs to historian.
  - `validate_screening_acceptance(...,issue_id,implementation_sha)` inside
    Evidence (`554-555`, `773-779`) → calls State-free Screening primitive with
    `issue_id` from basis-pinned package bytes, not live State.
  - `(repo_root/screening_package.basis.state_path).resolve() ==
    state_path.resolve()` (`557`) → REPLACED by retained-COPY equality above.
- R: all C + `package_sha256`/`screening_acceptance_sha256`/`discovery_sha256`/
  `profile_sha256` file-SHA equalities + contract/prompt/schema file-SHA
  equalities + task/card file-SHA + digest/dirname + supplement exact binding.
  No State, no `verify_state_basis`, no override, no `implementation_sha`.
- Honest gap: current derivation never calls `validate_materiality_ledger`,
  `validate_completeness`, `validate_edition_views_acceptance`, or
  `validate_edition_view` for the selected DID path; ledger/discovery are
  loaded as JSON and cross-bound by SHA only (`F1:242-243`, `F2:449-450`).
  Pre-code must fix whether the leaf adds those validators State-free or
  documents them as high-side QA obligations. Hash-only acceptance is forbidden —
  if ledger/discovery content predicates cannot be made State-free without
  weakening, return exact blocker.

### F4 — Screening package / acceptance validators

- Funcs: `validate_discovery:113-~185`, `validate_discovery_set:186-198`,
  `validate_discovery_expansion:243-~324`, `_canonical_root_acceptance:325-350`,
  `resolve_effective_discovery_basis:353-439`, `resolve_active_screening_acceptance:442-489`,
  `prepare_package:492-567`, `validate_decision:570-593`, `expected_result_basis:595-603`,
  `_validate_archived_screening_files:606-626`, `validate_package_basis:629-650`,
  `_validate_result_batch:653-693`, `_result_set_digest:696-704`,
  `validate_acceptance:706-749`, `accept_results:752-~814`.
- H: `screening-accepted.json` + sibling `package.json` (`716-717`);
  `package_sha256` binding (`716`); batch input/result files exact sets
  (`723-724`); Discovery JSONL bytes.
- C: `validate_decision` exact `DECISION_KEYS`, KEEP/MAYBE/DROP/INSPECT,
  reason/scope_tags/verification_targets/confidence (`570-593`);
  `_validate_result_batch` batch bytes, result shape/identity,
  `result.basis == expected_result_basis(package_sha,batch_sha,profile_sha,
  state_sha,prompt_sha,result_contract_sha)` (`670`), per-decision validity,
  duplicate/coverage-exact (`676-687`); `record_count`/`batches` metadata
  (`739-741`); sorted-decisions equality (`742-743`); digest+dirname
  (`745-747`); `_validate_archived_screening_files` input/result SHA (`618-626`);
  `validate_discovery_set` on derived+root records (`379`, `407`);
  expansion accounting (`428`).
- S → replacement:
  - `core.verify_state_basis` in `validate_package_basis:647` (+ via
    `prepare_package:503`) → REPLACED by same retained-COPY binding as F3
    (`package.basis.state_sha256 == sha256(basis.retained_before_state_path)`).
  - `expected_result_basis.state_sha256 == package.basis.state_sha256`
    (`602`) → RETAINED: must equal retained State SHA from basis, never live
    State SHA. `profile_sha256/prompt_sha/result_contract_sha` remain as
    file-SHA equalities (current content, no State call).
  - `resolve_effective_discovery_basis` State-bound branch
    (`_canonical_root_acceptance:330-350` reads `state.profile.path`) and
    `resolve_active_screening_acceptance` (`442-489`: lifecycle gate +
    `resolve_checkpoint_artifact` + override) → NOT CALLED in leaf.
    Leaf uses basis-pinned `discovery_path` + `screening_acceptance_path`
    directly with SHA rechecks + `validate_discovery_set`/`validate_acceptance`
    State-free variants.
  - `implementation_sha` → DROPPED in State-free primitive.
- R: all C + file-SHA bindings + digest/dirname. No State, no override.
- Honest gap: `validate_discovery_expansion` DERIVED_EXPANSION mode (`428-439`)
  and X intake (`survey_x_intake_v2`, `survey_discovery_v2.validate_acceptance`)
  were not line-verified in this unit. If renewal accepted set uses expansion
  mode, pre-code must pin its State-free form or return blocker. No silent
  DIRECT-only assumption.

### F5 — Agent-tool narrow State-SHA wrapper (to be removed from leaf path)

- Funcs: `verify_current_stage_basis:42-50`,
  `_historical_state_basis_wrapper:53-98`,
  `_historical_screening_basis_wrapper:101-108`,
  `_historical_evidence_basis_wrapper:111-118`,
  `current_stage_basis_override:122-143` (docstring `1-21` states the narrow
  content-addressed exception: package already content-addressed by sibling
  acceptance + acceptance binds exact archived package hash).
- Current behavior: replaces `core.verify_state_basis` for one helper lifetime
  (`127-133`) + wraps Screening/Evidence `validate_*_package_basis` to allow
  `state_sha256` drift IFF `sha256(package_path) == acceptance.package_sha256`
  (`75`, `111-118`) with path-escape/symlink guards (`84-90`).
- Replacement: leaf NEVER enters the override context. The single allowed
  exception is reimplemented path-based inside F3/F4 primitives as file-SHA
  equalities above. No monkeypatch, no `pending_basis` (`122`, `129-130`),
  no `verify_pending`. `ALLOWED_HELPERS:36-39` + `run_helper:146-180` are
  out of scope for the leaf (execution transport, not authority).
- S → replacement: `implementation_sha == current_commit` check (`43-47`) +
  `agent._validate_agent_state/validate_agent_state` (`48`) → DROPPED.
  Basis provides `current_tools` pins for historian/high only.

### F6 — Lifecycle-gated entries, token-safety, accepted-Draft, directive, archive

- Funcs/lines: Weekly `_validate_authored_input:160-195` (envelope
  `schema_version/issue_id/runner/cover/frontmatter/final_summary`),
  `_closing_summary:285-297`, `_window:145-158`; Longform `_did:240-258`,
  `_kicker:273-281`, `_bib_key:282-288`, `_check_url:289-~311`,
  `_resolve_primary_entity:312-344`, `_safe_card_path:345-364`,
  `_validate_archive_authorization:530-581`, directive refusal `969-974`,
  `REQUIRED_*`/`READBACK_*`/`_GIT_OVERRIDE_VARS` (see F2).
- H: authored envelope files + archive `draft/v2/...synthesis-input.json` +
  `DIRECTIVE_REL` absence.
- C (all retained State-free): envelope exact keys + `issue_id` + `runner`
  non-empty (Longform `626-636`; Weekly `161-195`); cover/frontmatter shape;
  `final_summary.paragraphs` + synthesis `current_interpretation` containment;
  per-package/per-block/per-DID placement via `citation_refs.refs`; DID token
  syntax (`_did`), `package_id` token (`275`), `issue_id` token (`619`),
  URL validation (`_check_url`), primary-entity resolution
  (`_resolve_primary_entity`), card/access mapping
  (`provenance.resolve_source_access_provenance`), accepted-Draft restrictions
  (archive coverage, no extra/duplicate package/block, `spec == result` text,
  `ref_mode`/`deck_ref_mode` exact citation semantics); directive lexical
  refusal (file-or-symlink present → refuse before projection).
- S → replacement: lifecycle (`DRAFT_COMPLETE`, `READBACK_LIFECYCLES`,
  `next_action`, handler, `GIT_OVERRIDE_VARS`, Profile route checks) → DROPPED.
  Checked outside. Leaf keeps pure file-content checks only.
- R: all C + file reads. No State/lifecycle/Git.

### F7 — P1 typed graph (classification only, not a leaf callee)

- Funcs: `_Graph:578-605` (`node` HASH/POLICY conflict, `edge`, `canonical`),
  `_pol:783-791` (mutable → `COPY_BEFORE_REPLACEMENT`, else `KEEP_IMMUTABLE`),
  `_build_graph:687-~1470` incl. tool-closure nodes `955-958`
  (`receipt:tool-closure:*` + `RECEIPT_TOOL_CLOSURE` edges), frozen-kind helpers
  `608-684`, `_retention_rows_for_graph:1472-1525`, `_retention_plan:1543-~1549`.
- Finding (confirms decision §3 + review E/T split): tool rows ARE normally KEEP
  under `_pol`, so historian/leaf MUST classify by typed
  `RECEIPT_TOOL_CLOSURE` edges + fixed closure membership, never by KEEP or
  directory prefix. No wildcard `scripts/**`, no caller allowlist.
- Leaf use: NONE. P1 graph is not called by the leaf. It informs which
  basis-pinned rows are evidence (live+retained-COPY recheck) vs tools
  (epoch-blob only, historian). P1 `validate_proposal`/`NO_EDITORIAL_CHANGE`
  (`1640-1670`), `_active_effective:467-535`, `_versioned_active_selection:65-74`
  stay outside; renewal never mints P1 same-reader proposal.

### F8 — P2R retained layout (mapping only, not a leaf callee)

- Funcs: `_Session:181-~527` (`safe_read`, dirfd/no-follow, `reverify`,
  `_close_all`), `verify_retention:1737-~2086` (header/basis/proposed equalities
  `1771-1783`, ordered plan↔rows `1785-1803`, KEEP `1808-1813` vs COPY `1814-1823`,
  I1 chain `1833-1893`: `state:authority COPY → retained State → State.profile
  → KEEP Profile`, provisional COPY-dest `1860-1865`, retained inventory
  `~1932-1958`, `repinned` KEEP recheck `~1959-1969`, `capture_inputs`
  `~1999-2045`, canonical-bytes `~2048`, `reverify/_close_all ~2062-2067`).
- Leaf use: NONE directly. Current `verify_retention` is NOT called as historian
  (correct refusal after Core change). Leaf reuses ONLY the mapping rule:
  `state:authority row.path/sha256 == basis.state_ref` +
  `retained_dest == _expected_retained_dest(proposal_dir,row.path)` +
  `sha256(retained_dest) == row.sha256` + Profile KEEP linkage, with paths
  rooted at `R/retained/before/` for the fresh renewal COPY (second generation).
  Old KEEP rows stay live-rechecked. Full P2R semantics stay high-side.
- Missing (blocker §3): no renewal retention verifier exists yet; fresh COPY
  dest layout, `expected_dir` derivation from retained Profile, and inventory
  scope for `R/` are unnamed. Pre-code must fix them; no basename/current-State
  shortcut.

## 2. Forbidden-pattern compliance

- No caller `already_verified` / verified-dict / `pending` / `active_set` token:
  `pending_basis` params (`weekly:198,227,501,514,565`) and override
  (`weekly:200,441; longform:441`) are absent from the new signature.
- No monkeypatch: `current_stage_basis_override` never entered.
- No historic `implementation_sha` to current helper: `implementation_sha =
  repository_commit_sha` (`weekly:562`; `longform:1060`) and its threading into
  `_records/_longform_records` → `validate_*` (`weekly:563-566`;
  `longform:1066-1069`) is cut. Leaf has no `implementation_sha` arg.
- No broad `pending` allowance, no `seal_path` shortcut, no route/kind enum,
  no ambient context. Every ref path-based with SHA.
- No hash-only acceptance: every SHA binding is paired with its content
  predicates (status/materiality/placement/primary/access/archive/directive/
  synthesis/draft/token checks + digest/dirname + task/card/decision coverage).
  Ledger/Discovery/X gaps in §1 (F3/F4 honest gaps) must close or block —
  never waived to SHA-only.

## 3. Remaining IO in leaf (finite)

Repo-local regular-file reads only (bounded, no-follow, symlink refused):
basis, profile, architecture, synthesis-input/result, per-package
draft-package/result, archive, authored inputs, evidence-acceptance+package+
tasks+cards, screening-acceptance+package+batches+results, candidate-matrix,
materiality-ledger, discovery JSONL/acceptance, trio outputs for render
comparison (read-only, no staged write), style file for `validate_generated_closure`.
Strict JSON parsing, `sha256_file/sha256_object/sha256_bytes`,
`schema_gate` validation against CURRENT disk schemas for content shape
(evidence/screening/draft/reader), `citation_refs`/`drafting`/`provenance`
pure computation. No State/Profile-from-State load, no `verify_state_basis`,
no HEAD/commit/Git, no network, no writes, no publisher, no P1/P2R/P3S/seal.

## 4. Missing retained-state / materialization blockers (honest, pre-code must close)

1. **Fresh renewal COPY layout unnamed.** Current P2R expects
   `<proposal_dir>/retained/before/<original_path>` (`831-832`, `1861-1865`,
   `1925-1930`). `R/retained/before/` second generation, `expected_dir`
   derivation from renewal Profile, and inventory scope for `R/` have no code.
   No verifier exists. Blocker until pre-code fixes paths + verifier.
2. **No renewal-aware P2V entry.** Original `observe_current_authority`
   refuses after activation (`P2V_AFTER_ACTIVATION_REFUSED`). Leaf does not
   replace it; high needs new `observe_renewal_authority` with basis params.
   Absent → leaf cannot be gated. Blocker.
3. **No U renderer-equality runner named.** U requires current renderer →
   disposable temp trio vs old trio bytes + complete canonical reader equality,
   with `RERENDER_MISMATCH`-class refusal and no auto-convert to C. Temp
   location, renderer entry, and style/recipe pinning are unnamed. Blocker.
4. **C staged derivation path unnamed.** New trio/manifest under
   `R/staged-source/`, build record, manuscript `renewal_source` branch, and
   proof-as-staged-proof wiring are design-selected but have no verifier.
   Blocker.
5. **Ledger/Discovery/X/materiality/completeness State-free form open.**
   Current derivation skips their dedicated validators; leaf must either add
   State-free variants or place them high-side with exact error taxonomy.
   Open until pre-code pins the list (B3 remedy). Hash-only is forbidden.
6. **Tool-epoch vs retained-evidence split depends on historian.**
   Leaf proves content authority; history evaluator proves tool-epoch blobs;
   high proves current closure/contract/HEAD. If pre-code cannot keep the
   three disjoint without weakening any predicate, stop with exact blocker
   (decision §9 rule), never a weakened checker.

## 5. Completeness scope (what this map does and does not do)

- Does: finite family list (F1–F8) with actual funcs/lines, H/C/S→replacement/R
  per family, path-based signature, ban list, allowed callees, remaining IO,
  and six honest blockers. Sufficient for root to judge B3 closability.
- Does not: detailed implementation, new schema text, digest bases, proof
  threading, closure sets, fingerprints, style boundary, C ordering, or
  consumer map (B1/B2/B4–B6, left to pre-code return). No runtime feasibility,
  no PASS, no adoption/approval/audit claims. Whole NOT_READY / step4B3 OPEN /
  audit unstarted / DM021+022 OPEN retained. Production semantic NO-GO on
  placeholder editions; synthetic approvals labelled separately.

(End — author-side design supplement, no independence claim.)
