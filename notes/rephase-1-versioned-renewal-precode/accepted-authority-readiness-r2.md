# Accepted-authority readiness R2 — versioned same-reader renewal (author-side pre-code return)

2026-10-23 JST. Author-side General pre-code return R2, NOT independent review.
Human HEAD `ce0de1a` (root observed clean `main...origin/main`).
Governing: `outputs/rephase-1-versioned-renewal-contract-decision.md` (192 lines,
SHA256 `478f00510791b76af24aa7d61f398f0608f7ad8ae7808008c660f2bea6fbfdcf`)
INCLUDING §11; mandatory `notes/rephase-1-versioned-renewal-contract/astra-review-resolution.md`;
BOTH independent reviews WITH final-binding addenda;
author inventory `notes/rephase-1-versioned-renewal-contract/accepted-authority-predicate-map.md` (F1–F8);
sibling `notes/rephase-1-versioned-renewal-precode/interfaces-schemas-digests-r2.md` (R2, exact new basis carrier).
Read-only source: `.rephase-1-editorial-runtime/final-source-packaging/proof-copy/candidate-partial-b40de60`
(actual409/tree8ce + intended57). No implementation/source edits/imports/tests/build/fixture/restore/network/Git writes.
This file `accepted-authority-readiness-r2.md` is the ONLY write in this unit.
R1 `accepted-authority-readiness.md` is PRESERVED unchanged; every R1 occurrence superseded below is listed
explicitly. No code/tests. No self-certified complete: §8 matrix states CLOSED (design rule fixed) vs
still-OPEN (implementation/proof still required).

## 0. What R1 got right (preserved) and what R2 corrects

Preserved from R1: §0 accepted State-SHA rule (historical SHA stays original; §11.3 1–6 ONLY; no package
mutation; no original-`state_path`-vs-retained-dest compare); route-trace bodies/transitives for Weekly
(`survey_weekly_derivation_v2.py:489–584` + `:196–272`), Longform (`survey_longform_derivation_v2.py:957–1098`
+ `:421–520`), Evidence (`survey_evidence_v2.py:719–846,865–1167`), Screening/Discovery/X
(`survey_screening_v2.py`, `survey_discovery_v2.py:84–269`, `survey_x_intake_v2.py:78–396`),
Drafting/Architecture bases, raw/access/card lineage, expansion/supplement optionality, T1–T6 contract-equality
table. All file:line citations in R1 §§2.2–2.8 remain valid as source locations.

R2 corrects 9 Astra CHANGES_REQUIRED defects. Each defect names the exact R1 text superseded:

| Astra # | R1 defect | R2 section | Design status |
|---|---|---|---|
| 1 | §2.9 row assigns manuscript/Gate/bundle CONTENT to LEAF; leaf would call contextual Reader/Gate which call proof again | §1 (layer split) + §5 | CLOSED (rule): accepted-loader NEVER validates manuscript/Gate/bundle; downstream typed validators/HIGH/fullset own them |
| 2 | `*_statefree(root, package_path)` public entries lack basis/COPY/checkpoint identity; ambient sources | §2 (basis_path-only public entries + private same-invocation session) | CLOSED (rule); OPEN (implement session + finite match checks) |
| 3 | tool predicates HIGH-only misses after-activation readback without high observation | §3 (subloader vs full proof verifier split) | CLOSED (rule); OPEN (implement verifier + HIST epoch checks) |
| 4 | file-label equality requires every doc to carry both profiles; many schemas lack `publication_profile` | §4 (per-schema label table; route from Profile only) | CLOSED (rule, replaces R1 W2/L2) |
| 5 | A1–A7 "not shown" + P1 graph/checkpoint replaced by basis SHA without wrapper validators; arbitrary basis name-map authority | §5 (source expressions + wrapper provenance + finite prior-receipt match) | CLOSED (rule); OPEN (implement validators) |
| 6 | U renderer mismatch conflated with `UNSUPPORTED_MIGRATION` | §6 | CLOSED (rule) |
| 7 | invented `Path(".")`→`repo_root` bugfix as task goal | §7 (inspection: root arg unused; NO fix; R1 S8 wording superseded) | CLOSED (dropped) |
| 8 | "schema additions WITHOUT changing old schema BYTES" false for appended branch | §8 (old/new pins separate; 4 new files + 1 existing-file branch) | CLOSED (rule) |
| 9 | `*_statefree` public copies duplicate whole modules (divergence risk) | §9 (shared-core extraction in existing files; wrappers keep behavior; duplication only with justification + equivalence oracle) | CLOSED (rule); OPEN (implement extractions + oracles) |

Primary instruction respected throughout: full predicate preservation; no monkeypatch, no caller
`already_verified`/verified-dict/`pending` data/flag bypass (decision §§4/11.1).

## 1. (Finding 1) Manuscript / Gate / bundle CONTENT leaves the accepted-loader

R1 §2.9 row ("LEAF re-executes manuscript/Gate/bundle CONTENT predicates under explicit U proof context")
is SUPERSEDED. It violates the §1.2 hard ban and constructs a cycle:

- Contextual Reader manuscript validation with proof context must call the proof: U rule (decision §11.2)
  is "historical identity PLUS new current source proof" checked inside the Reader validator that receives
  `renewal_source_proof_ref`. If the source proof's own accepted-loader called that validator, the loader
  (proof construction) would depend on proof validation — State→Candidate→Reader→proof recursion in
  VALIDATED/Preview/FROZEN/RELEASED, exactly what decision §4/§6/§11.2 forbid ("low resolver hashes and
  cross-binds only; must not call full Reader/Gate/source-proof semantics").
- Actual coupling (why the ban is load-bearing, not stylistic):
  `survey_reader_publication_v2.py:237–247` (`verify_staged_source` inside `_validate_manifest_semantics`),
  `:643–647` (nested `validate_manuscript_manifest` inside `validate_review_record`);
  `survey_reader_surface_gate_v2.py:1159–1253` (editorial `verify_staged_source` `:1173` + fixed receipt
  `:1182–1185`), `:1333–1694` (Gate evaluation threading manuscript + receipt);
  `survey_publication_v2.py:668–814` (`build_candidate` threading manuscript/source/pdf/bundle/reviews,
  `validate_candidate:749–814` re-threading manuscript `:775`, bundle `:781`, reviews `:801–811`).
  A leaf that called any of these with a proof ref would re-enter the proof it is building.

R2 rule (CLOSED):

- The accepted-loader (`load_renewal_accepted_authority`, §2) returns ONLY accepted-research assembly:
  `{surface, records, accepted_refs, authored_refs}` where `surface` is the PURE projector output
  (`weekly.build_reader_input:300–394`, `longform.build_longform_reader_input:608–926`) AFTER all
  accepted-content checks, and `records` is the DID→bibliography map. It NEVER calls
  `validate_manuscript_manifest`, review-record validation in contextual mode, Gate derivation/evaluation,
  Candidate build/validate, `quality.validate_bundle` as authority, seal, or full receipt.
- Pure shape checks that do NOT touch proof remain allowed in the loader exactly as before:
  `validate_reader_input` (`weekly:397–407`) / `validate_longform_reader_input` (`longform:927–948`) as
  schema+route check; `render_main`/`render_bibliography`/`validate_generated_closure`
  (`weekly:414–486`) and Longform canonical-bytes/render helpers as pure deterministic functions.
  These take the projected `surface` value only, never a proof ref, never State/Candidate/seal.
- Manuscript / Gate / bundle / review CONTENT under proof context is owned downstream:
  (a) typed renewal-aware validators in their existing modules (new `renewal_source_proof_ref` /
  `renewal_receipt_ref` keyword params per `interfaces-schemas-digests-r2.md` §§4.1–4.5 — owned by the
  schema/interface return, referenced not duplicated here);
  (b) HIGH normal admission (`observe_renewal_authority` + active consumers compare State-selected set);
  (c) full-set validator (Candidate/QA/Gate/receipt/seal agree on SAME proof path+SHA).
  The U predicate list (decision §11.2: schema/self-digest/issue, Profile, exact Architecture+typed approval,
  sizes, unique paths, Architecture coverage, reader requirements, author/time, fidelity,
  surface/suppression, exact trio; reviews keep kind/status/check-family/depth + exact
  manuscript/source/PDF/page-count/digest; historical same-reader scope with exact before/after relations)
  is therefore a DOWNSTREAM contract on those validators, not a leaf body. Standalone old validators
  WITHOUT proof keep current P3S refusal (no hidden waiver).
- R1 rows affected: §2.9 P1-table manuscript/Gate/bundle row reassigned LEAF→DOWNSTREAM/HIGH/FULLSET;
  R1 W10/W11/L12 "KEEP verbatim AFTER all authority checks; allowed callee" remains TRUE for the pure
  projector + pure shape/render helpers only, and is explicitly NOT extended to contextual manuscript/
  Gate/Candidate validators. Any R1 sentence reading "leaf re-executes manuscript/Gate/bundle" is
  superseded by this section.

## 2. (Finding 2) Every public reloadable entry takes `basis_path`; no ambient sources

R1 signatures of the form `validate_*_statefree(root, package_path)` / `(root, acceptance_path)` /
`(ledger, repo_root, profile_path, ...)` are SUPERSEDED as PUBLIC entries. A caller that passes an
arbitrary `package_path` cannot enforce §0 conditions 1–6 (acceptance binding, canonical SOURCE path,
issue/Profile agreement, COPY chain, checkpoint identity) because the basis, the COPY binding, and the
prior-receipt identity are absent from the call. Accepting such a call would be caller-selected authority
by path — the exact pattern decision §§4/11.1 forbid alongside caller verified dicts.

R2 rule (CLOSED as rule; implementation OPEN per §8):

- PUBLIC reloadable authority entries (the only functions any other module may call) are exactly:
  ```text
  load_renewal_accepted_authority(root: Path, basis_path: Path) -> {surface, records, accepted_refs, authored_refs}
  validate_renewal_basis(root: Path | str, basis_path: Path | str) -> {basis, retained, unchanged_evidence}
  verify_renewal_source_proof(root: Path | str, basis_path: Path | str, proof_path: Path | str) -> {proof, trio, digests, disposition}
  verify_versioned_history(root: Path | str, record_path: Path | str) -> {HISTORICAL_IDENTITY_VERIFIED, observed_refs}
  ```
  No public `*_statefree(root, package_path)` entry. No `implementation_sha`, no `pending_basis`, no
  verified-records/caller-dict param on any of them. Paths are repo-local no-follow, fully reloaded every
  use (strict JSON, schema, self-digest recompute, live SHA/size, cross-bind, pin recheck).
- Each `basis_path` entry builds, IN THE SAME INVOCATION, a validated private session object (name fixed
  for the pre-code map; implementation chooses module placement per §9):
  ```text
  _RenewalAuthoritySession = {root, basis, basis_sha,
    profile_ref, reader_ref, authoring_refs, accepted_refs,  # basis-pinned, SHA-verified
    before_state_ref, retained_copy_ref, retained_bytes,     # COPY chain, SHA+size-verified
    prior_refs:{seal, record, candidate, validation_checkpoint, anchor},  # §5 finite match
    old_tool_epochs, current_tool_epoch}                      # §3 split
  ```
  The session is constructed BY the path entry from `basis_path` bytes + live file re-reads only. It is
  never accepted from a caller, never cached across invocations, never ambient/global.
- All other validators are PRIVATE to the invocation (leading underscore, same-invocation only) and take
  the session (or session-derived pinned values), never bare paths:
  ```text
  _strict_evidence_sources_s(session, acceptance_ref) -> (sources, refs)
  _records_from_authorities_s(session, matrix_ref, ledger_ref, discovery_ref, acceptance_ref)
  _longform_records_s(session, matrix_ref, ledger_ref, discovery_ref, acceptance_ref, selected_ids)
  _validate_evidence_package_basis_s(session, package_ref)      # §0 via session.acceptance/basis/COPY
  _validate_evidence_acceptance_s(session, acceptance_ref)
  _validate_screening_package_basis_s(session, package_ref)
  _validate_screening_acceptance_s(session, acceptance_ref)
  _validate_discovery_acceptance_s(session, acceptance_ref)     # incl. graph + X-integration
  _validate_x_manifest_s(session, manifest_ref, discovery_acceptance_ref)
  _validate_materiality_ledger_s(session, ledger_ref, ...)
  _validate_completeness_s(session, completeness_ref, ...)
  _validate_edition_views_s(session, views_ref, ...)
  _validate_supplement_s(session, supplement_ref, ...)
  _validate_selection_s(session, selection_ref, ...) / _validate_architecture_s(...) /
    _validate_synthesis_s(...) / _validate_draft_s(...)          # §5 source expressions
  ```
  Exact source of every input (no implicit ambient): `profile` bytes from `session.profile_ref`
  (= `basis.profile_ref`, interfaces R2 §2.1); `reader/authoring` from `basis.reviewed_reader_ref` /
  `basis.authoring_refs`; each accepted family from the NAMED row of `basis.accepted_refs`
  (`_load_basis_accepted_ref(session, name)` = R1 W3 loader, now session-scoped); COPY bytes from
  `session.retained_copy_ref` (= `basis.retained_copy_ref` at `R/retained/before/<rel>`); prior identity
  from `session.prior_refs` (§5); tool epochs from `session.old_tool_epochs/current_tool_epoch` (§3).
  Where a check needs `cfg` (role namespaces, synthesis payload requirements, stage-plan handler NAME for
  HIGH only), `cfg` is current-disk `config/survey-production-v2.json` (TC-content), never State-derived.
- Finite match checks against arbitrary basis name-map authority (see also §5): the session constructor
  verifies `basis.accepted_refs` EQUALS the prior receipt's `accepted_refs` list verbatim
  (names+path+sha sorted, no addition/removal/relabel — interfaces R2 §2.1 rule, which this file adopts as
  the anti-arbitrary-map control), `basis.authoring_refs`/`reviewed_reader_ref`/`profile_ref` equal the
  prior set's bytes, and `basis.prior_*` equal the live prior seal/record/Candidate observed at entry
  (HIGH `_observe_renewal_entry` pins; session rechecks). A basis whose name map invents, drops, or
  relabels a row fails with `BASIS_ACCEPTED_SET_DRIFT` before any content check runs.

## 3. (Finding 3) Accepted-content subloader (no Git) vs full detached proof verifier (MUST check current tools)

R1 §1.2/§2 W4 ("`current_tools`/`contract`/`closure` are NOT checked in this leaf; they belong to HISTORIAN +
HIGH") is SUPERSEDED as stated for the whole source-proof module. It holds ONLY for the accepted-content
subloader, not for the full detached proof verifier. Otherwise normal after-activation readback has a hole:
`validate_candidate → Reader manuscript → verify_renewal_source_proof` must freshly reject further Core
drift WITHOUT running the high current-before observation (high observation is write-boundary-only per
§11.1; readback is detached by design).

R2 split (CLOSED as rule; implementation OPEN per §8):

- Layer A — accepted-content subloader: `load_renewal_accepted_authority(root, basis_path)` (§2).
  Checks accepted-research CONTENT only (R1 §§2.2–2.8 bodies as session-scoped privates). NO Git, NO
  `repository_commit_sha`, NO closure/contract/commit comparison, NO epoch blob read. This is the ONLY
  meaning of "leaf doesn't check tools".
- Layer B — full detached proof verifier (source module, same invocation discipline, still NO State):
  `verify_renewal_source_proof(root, basis_path, proof_path)` and `validate_renewal_basis(root, basis_path)`
  (called on EVERY proof readback, decision §11.1). Layer B MUST, in addition to Layer A content:
  1. reload proof + basis, recompute `proof_sha256`/`basis_sha256` (self-digest excluded), verify
     `proof.basis_ref == {basis_path, sha256(basis)}`, `proof.accepted_refs == basis.accepted_refs`,
     `proof.reviewed_reader_ref/authoring_refs` equal basis, trio refs sized + SHA-verified;
  2. verify CURRENT closure/loaded-bytes/commit/schemas via safe helpers with NO State load:
     recompute `current_closure` equivalent (Weekly `current_closure:587–588` discipline;
     longform-generated `current_closure` discipline; editorial union-50 discipline
     `survey_editorial_publication_v2.py:1959–2000`) from CURRENT disk bytes, compare member-wise
     against `proof.dependency_closure` / `basis.current_tool_epoch.closure` (exact names+SHA; missing/
     extra/drift → `BASIS_CURRENT_TOOL_DRIFT`); verify `contract_identity` recomputed from current disk
     equals `proof.supported_contract` steady-state expectation (apart from permitted
     implementation/style bytes per decision §2; anything else → `UNSUPPORTED_MIGRATION`); verify schema
     files used in validation equal current disk bytes (§8 pins); all through `_safe`/no-follow/bounded
     reads, `git show <epoch>:<path>` NEVER (that's HIST), `core.verify_state_basis` NEVER, State load NEVER;
  3. require HIST old-epoch checks to have passed for this proof's `supported_epochs`
     (`receipt_epoch`, `staged_producer_head`, schema epochs per interfaces R2 §2.1): Layer B refuses
     `HISTORY_TOOL_EPOCH_DRIFT`/`HISTORY_BLOB_MISSING` unless `verify_versioned_history` for the bound
     record/proof reports `HISTORICAL_IDENTITY_VERIFIED` with matching observed epochs. Old epochs are
     HISTORIAN-owned (`verify_versioned_history(record_path)` record-only, no State arg, typed E/T
     classification, per-document epochs from records, decision §11.1); Layer B consumes the HIST verdict,
     never re-implements Git epoch reads, never issues a reusable permit.
- After-activation readback path (why this closes the hole): normal active consumers
  (`validate_candidate:749–814` → `validate_manuscript_manifest:413–451` with `renewal_source_proof_ref` →
  `verify_renewal_source_proof`) trigger Layer B, which rejects further Core drift via (2) and stale epochs
  via (3) WITHOUT demanding live-before equality (live-before equality stays HIGH write-boundary-only).
  Detached `validate_renewal_basis` still validates RETAINED before-State only, never live-before equality.
  No authority transfers through returned dicts; every use reloads by persisted path.

## 4. (Finding 4) File-label equality itemized per actual schema (R1 W2/L2 superseded)

R1 W2/L2 ("every document same `issue_id` + same `research_profile`/`publication_profile`") is SUPERSEDED.
Inspected actual schemas (current disk, proof-copy): only SOME shapes carry `publication_profile`;
several carry neither profile. Requiring absent labels is an arbitrary requirement, not preservation.
Route is derived from the Profile (`basis.profile_ref`), never voted by the accepted set.

R2 rule (CLOSED): compare ONLY fields present in each schema's `required`; missing optional labels are
never demanded. Exact label fields (schema `required` verified 2026-10-23):

| Artifact (basis row) | Schema file | Label fields compared (exact; no more) |
|---|---|---|
| `production-profile` (top-level `profile_ref`) | `survey-production-profile.schema.json` | `issue_id`, `research_profile`, `publication_profile`. Route source: `profile.research_profile/publication_profile` must equal `basis.research_profile/publication_profile` and `generator_route` contract (`WEEKLY/WEEKLY_MAGAZINE→WEEKLY_GENERATED_V2`; `THEMATIC/LONGFORM_SPECIAL→LONGFORM_GENERATED_V1`). |
| `issue-architecture` + `architecture-review-summary` + `architecture-review-attention` | `issue-architecture-v2.schema.json` etc. | architecture: `issue_id`, `research_profile`, `publication_profile`. summary/attention: `issue_id` (+ `research_profile` where schema requires). Approval record: `issue_id` only (no profiles in `architecture-approval-record-v2.schema.json` `required`). |
| `synthesis-input`, `synthesis-result` | `profile-synthesis-v2-input/result.schema.json` | `issue_id`, `research_profile`, `publication_profile` (both schemas require all three). |
| `draft-package:<pid>`, `draft-result:<pid>` | `draft-v2-package/result.schema.json` | `issue_id`, `research_profile`, `publication_profile`, `package_id` (both require all four). |
| `evidence-acceptance`, sibling `package.json`, `tasks/*`, `results/*` (cards) | `evidence-v2-run-package/task/card.schema.json` | package+tasks: `issue_id`, `research_profile` (NO `publication_profile` in package/task schemas). cards: `issue_id`, `evidence_task_id` (NO profiles in card schema). acceptance: `issue_id`, `research_profile` (acceptance envelope carries both; checked in E5). |
| `screening-accepted.json`, sibling `package.json`, `input/batches/*`, `results/*` | `screening-v2-run-package/batch-result.schema.json` | package/batches/results: `issue_id`, `research_profile` (NO `publication_profile`). batch-result: `issue_id`, `batch_id` + `basis` (no profiles). |
| `discovery-acceptance` + `discovery JSONL` | `discovery-acceptance-v2.schema.json` + `survey-discovery-record.schema.json` | acceptance: `issue_id` ONLY (no profiles). each JSONL record: `issue_id`, `discovery_id` (+ provenance/source). |
| `x-source-intake` manifest + `task` + `raw` | `x-source-intake-v2.schema.json` | manifest: `issue_id`, `research_profile` (NO `publication_profile`). runs: `run_id` + result `discovery_ids`/`discovery_disposition`. |
| `evidence-authority-supplement` | `evidence-authority-supplement-v2.schema.json` | `issue_id`, `supplement_id` (NO profiles). per-source: `discovery_id`, `evidence_task_id`, `supplement_source_id`. |
| `edition-views-acceptance` + `views/*` | `edition-evidence-view.schema.json` | acceptance+views: `issue_id`, `research_profile` (NO `publication_profile`). per-view: `evidence_task_id`. |
| `materiality-ledger` | `materiality-ledger.schema.json` | `issue_id`, `research_profile` (NO `publication_profile`). |
| `profile-completeness` | `profile-completeness-result.schema.json` | `issue_id`, `research_profile` (NO `publication_profile`). |
| `candidate-matrix` | `candidate-matrix-v2.schema.json` | `issue_id`, `research_profile` (NO `publication_profile`). |
| `candidate-selection` | `candidate-selection-v2.schema.json` | `issue_id`, `research_profile`, `publication_profile` (requires both). |
| authored inputs (`publication-authored-input`, `drafting-archive`) | authoring envelope (Weekly `:160–195`; Longform authored) | `issue_id` (+ `runner` where envelope requires). Profile labels come from the pinned Profile, not the authored file voting. |

Enforcement: `_check_leaf_labels_s(session)` iterates basis rows by family and checks the row's schema-listed
fields only, plus cross-row `issue_id` agreement across ALL rows and `research_profile` agreement across all
rows that carry it, plus `publication_profile` agreement across all rows that carry it, plus route agreement
with the Profile. A family missing `publication_profile` in its schema is never failed for that label.
Live Profile binding remains HIGH; leaf checks file-label agreement only.

## 5. (Finding 5) A1–A7 source expressions + checkpoint-wrapper provenance + finite prior-receipt match

R1 §2.6 A1–A7 ("KEEP verbatim", bodies "not shown") and R1 §2.9 P1-graph/checkpoint rows ("replaced by basis
SHA") are SUPERSEDED as acceptance criteria. R2 gives the exact source expressions (file:line) the private
session validators must re-execute, the checkpoint-wrapper provenance owners, and the finite match that
stops arbitrary basis name-map authority.

### 5.1 A1–A7 exact source expressions (private session validators re-execute these bodies State-free)

- A1 matrix: `survey_architecture_v2_base.derive_candidate_matrix` (called by `validate_candidate_matrix
  :272–281`; `matrix != expected → refuse`). Session validator `_validate_matrix_s(session, matrix_ref)`:
  re-derive from session-pinned Evidence/views/ledger inputs (E5/E6/E8 outputs in-session) and compare
  byte-exact. NO State, NO `implementation_sha`. (Derivation body itself is the oracle; no separate spec.)
- A2 selection: `validate_selection (architecture_base:291–448)` verbatim: exact 9 fields `:305–319`;
  issue/Profile/matrix identity `:322–327`; basis 4-tuple file-SHA `:328–337`
  (`production_profile_sha256/candidate_matrix_sha256/profile_completeness_sha256/materiality_ledger_sha256`
  against session-pinned bytes); `selection_version`; role namespaces from current-disk `cfg`
  (`research/publication_profiles.role_namespace`); per-assignment known-candidate + SELECTED↔
  PRIMARY/SUPPORTING + role presence + namespace prefix + `NON_MATERIAL/HOLD` refusal `:416` +
  `REJECTED/NEEDS_MORE` refusal `:418–421`; non-selected↔no roles; duplicate/exact-coverage `:427–432`;
  summary `:433–438`; Completeness/Ledger identity `:440–448`. `cfg` = current disk (TC-content).
- A3 architecture: `validate_architecture (architecture_base:451–…` + `survey_architecture_v2:98–…)`:
  selection revalidation `:461–471`; Profile/matrix identity; basis 5-tuple file-SHA `:501–509`
  (Profile/Completeness/Ledger/Matrix/Selection); thesis/goals/page_plan (`target/max/notes` numeric rules);
  per-package selected-candidate binding + `drafting_order` + `must_cover`/`boundaries` via the draft chain;
  `profile_extensions`/`publication_extensions` (incl. Weekly closing W9 / Longform equivalents).
  `status==PROPOSED` + separate Approval (A4) required.
- A4 approval: `validate_architecture_approval (drafting_base:105–134)`: exact `APPROVAL_FIELDS`; `gate==
  ARCHITECTURE_REVIEW` + `decision==APPROVED`; `architecture_sha256`/`review_summary_sha256`/attention SHA
  against session-pinned bytes; `approval_id/reviewed_by/review_reference`; `reviewed_at` instant. Plus
  Summary `readiness.status==READY_FOR_ARCHITECTURE_REVIEW` + `basis.architecture_sha256` binding
  (`_load_drafting_basis:246–256`). Genuineness (Human act) is HIST provenance; leaf checks bytes/binding.
- A5 synthesis: `build_synthesis_input (:706–774)` gates (approval revalidation, per-pair
  `validate_self_contained_draft_package` + `validate_draft_result`, package-set == Architecture set,
  `drafting_order` equality, Profile-owned `synthesis_payload_requirements` per `cfg`) + 
  `validate_synthesis_result (:777–831)`: exact 8-field envelope; issue/Profile match; 
  `basis.synthesis_input_sha256/prompt_id/prompt_sha256` (`SYNTHESIS_PROMPT=config/prompts/profile-synthesis-v2.md`
  current-disk SHA); `synthesis_version`; runner provider/model/invocation/`generated_at` instant;
  payload keys == Profile-owned requirements (`cfg.research/publication_profiles.synthesis_payload_required`:
  Weekly `signals/current_interpretation/carry_over_summary`; Thematic
  `branch_transition_synthesis/parallel_competing_relations/unresolved_lineage_questions/historical_attribution_boundaries`;
  Period `period_synthesis/…`), `_payload_value_present` per key.
- A6 draft: `validate_self_contained_draft_package (:378–…)` via `_load_drafting_basis (:191–271)` whose
  State-coupled interior (`_resolve_effective_screening_discovery :137–189`,
  `validate_package_basis`/`validate_evidence_acceptance` with `implementation_sha`) is replaced by the
  session S9/S4/E5-statefree equivalents (same bodies, session inputs); then `validate_draft_package` /
  `derive_draft_package` + `validate_draft_result (:589–703)`: exact `DRAFT_RESULT_FIELDS`; issue/Profile/
  package match; `basis.draft_package_sha256/prompt_id/prompt_sha256`
  (`DRAFT_PROMPT=config/prompts/article-drafting-v2.md` current-disk SHA); version/headline/deck; runner;
  `_card_ref_index` + `_validate_refs` + `_validate_attribution`; blocks/must_cover/boundaries/extensions.
  Per-package `must_cover`/`boundaries` + `ref_mode`/`deck_ref_mode` + `evidence_refs` via
  `citation_refs.refs` are RC content (W10/L10).
- A7 archive: `_validate_archive_authorization (longform:530–581)` + Weekly analog (`weekly:531–554` +
  `ordered` checks): exact package count/IDs (archive == Architecture set, no extra/duplicate/missing),
  per-block coverage, EVERY assigned DID through its own package `citation_refs.refs` exact-one semantics.

### 5.2 Checkpoint-wrapper provenance (HIGH historic vs detached — not "basis SHA instead")

Renewal does NOT resolve live checkpoints (`agent.resolve_checkpoint_artifact` is banned in the loader,
§1.2). Provenance is split:

- HISTORIC (HIST, `verify_versioned_history(record_path)`): the prior activation record's checkpoint
  wrappers (`State.checkpoint_provenance` entries at prior activation time) + wrapper→artifact bindings are
  reloaded as typed historical data from the prior record/seal (record epochs, never caller commit). HIST
  owns wrapper existence/shape/digest/chain; returns descriptive `HISTORICAL_IDENTITY_VERIFIED`.
- DETACHED (Layer A/B session): content predicates run on session-pinned accepted bytes (§5.1). The
  session NEVER calls `resolve_checkpoint_artifact`; it calls `_load_basis_accepted_ref(session, name)`.
- CURRENT (HIGH, `_observe_renewal_entry` / `observe_renewal_authority`): live State `checkpoint_provenance`
  + current nonpublication authority + current tool predicates at entry/capture/finalize/activate.
- Finite anti-arbitrary-map match (session constructor, before any content check — the control Finding 5
  demands): `basis.accepted_refs` MUST equal the prior receipt's `accepted_refs` verbatim (sorted by `name`,
  unique `name`, exact `{name,path,sha256}` per row; interfaces R2 §2.1 adopted); `basis.authoring_refs` /
  `basis.reviewed_reader_ref` / `basis.profile_ref` MUST equal the prior set's bytes; `basis.prior_*`
  MUST equal the HIGH-observed live prior seal/record/Candidate; `basis.original_validation_ref` MUST equal
  the HIGH-observed original validation checkpoint. Any invention/drop/relabel → `BASIS_ACCEPTED_SET_DRIFT`.
  The basis name map therefore carries NO self-authorizing power; it is a copy of prior receipt bytes
  verified by equality, plus HIGH-observed liveness.

## 6. (Finding 6) U mismatch is NOT migration

R1 §2 table (`DM` row: "U reuse mismatch … are DM, not U exceptions") and any sentence equating
`REUSE_TARGET_MISMATCH` with `UNSUPPORTED_MIGRATION` are SUPERSEDED.

R2 rule (CLOSED): `REUSE_TARGET_MISMATCH` (renderer-equality `reader_equal==false` OR `trio_equal==false`
OR old manuscript/build-unit live drift; U narrow condition decision §§1/6/11.2) → `REFUSED_PRE_WRITE`,
exit 2, never auto-switch an already-claimed `R` into C (decision §6). It is NOT a migration verdict.
A separate `RENDER_TARGETS` attempt with a NEW id (`R=P/renewals/<new-RID>`) after the U refusal is a
SUPPORTED C path (new trio at new paths + real build + executed-build record + new postrender reviews).
`UNSUPPORTED_MIGRATION` is reserved for research/Profile/Architecture/Draft authority, pipeline/quality
semantic-contract, review-requirement, route-family, or recipe-SPECIFICATION changes (decision §2),
which refuse under either intent and require a separate migration contract. The operation-oracles N-H10
(U mismatch) vs N-H4/N-H5 (migration) seam split is preserved.

## 7. (Finding 7) `expected_result_basis(Path("."), …)` — inspected, NO bugfix goal

Inspected actual `survey_screening_v2.py:595–603`:

```python
def expected_result_basis(repo_root: Path, package_path: Path, package: dict[str, Any], batch: dict[str, Any]) -> dict[str, str]:
    return {
        "package_sha256": core.sha256_file(package_path),
        "batch_sha256": batch["sha256"],
        "profile_sha256": package["basis"]["profile_sha256"],
        "state_sha256": package["basis"]["state_sha256"],
        "prompt_sha256": package["prompt"]["sha256"],
        "result_contract_sha256": package["result_contract"]["sha256"],
    }
```

`repo_root` is UNUSED in the body (all inputs are `package_path`/`batch`/`package` values). The call site
`:670` (`expected_result_basis(Path("."), package_path, package, batch)`) is therefore harmless: the first
argument cannot affect the result. R1 S8 ("must be replaced by real `repo_root`") is SUPERSEDED and DROPPED
as a task goal. R2 session validator `_validate_result_batch_s` reuses the function as-is (or its inlined
equivalent); no `repo_root` threading is required for this function. (The §0 State-SHA treatment of the
returned `state_sha256` value still applies — that is a predicate rule, not a call-site bugfix.)

## 8. (Finding 8) Schema bytes: old branch preserved AND new file bytes change — pin both

R1/T-table and R2-interfaces-R1 comments of the form "schema additions WITHOUT changing old schema BYTES"
are SUPERSEDED as stated for any EXISTING file that gains a branch. Appending a branch changes that file's
bytes by definition. R2 rule (CLOSED, aligns interfaces R2 §3 + Astra "contract fixed only 4 new schemas"):

- 4 NEW schema files (new paths, new bytes — no conflict by construction):
  `versioned-renewal-basis-v2.schema.json`, `versioned-renewal-source-proof-v2.schema.json`,
  `versioned-renewal-source-manifest-v2.schema.json`, `versioned-renewal-publication-set-v2.schema.json`.
- 1 EXISTING file gains a branch: `schemas/publication-surface-revalidation.schema.json` gains the third
  `VERSIONED_RENEWAL_ACTIVATION_V1` branch (legacy + editorial branches verbatim, interfaces R2 §3).
  That file's bytes DO change at bootstrap. Therefore bootstrap MUST pin old and new separately: historical
  validation of pre-renewal records uses the OLD schema SHA (record epoch); renewal validation uses the NEW
  schema SHA (current disk). Old branch semantics (legacy/editorial `oneOf` members) and their digest
  behavior are preserved bit-for-bit in meaning; the new branch is strictly additive (`oneOf` + 1 member).
- NO other existing schema file changes bytes: reader-manuscript / review-record / quality-bundle /
  publication-candidate schemas are NOT edited (U reuses old bytes; C/new files carry proof refs via the
  new strict OPTIONAL branch defined in interfaces R2 §§4.1–4.5 — new files only, old files/bytes/digests
  untouched). Any drift in an old schema file outside the one listed branch → `UNSUPPORTED_MIGRATION`.
- Gate: ONE new `VERSIONED_RENEWAL_V1` derivation variant BOTH U and C (old 4 variants verbatim, never
  augmented — interfaces R2 §4.4). Any statement in R1 implying "no old file bytes change at all" is
  superseded by this section.

## 9. (Finding 9) No whole-module copies: narrow shared cores in existing files + wrappers + equivalence oracle

R1 §5 items 3–16 ("Extract `*_statefree(root, …)` … same body … NEW in `survey_versioned_renewal_source_v2`")
are SUPERSEDED as implementation placement. Blindly copying whole validator bodies into the new source module
creates two divergent implementations of the same predicate (maintenance hazard + semantic-divergence risk).

R2 rule (CLOSED as rule; implementation OPEN per §8):

- For each family, the State-free CONTENT core is added as a NARROW private shared primitive IN THE
  EXISTING file that owns the predicate (same file, same pure helpers, no new module body):
  e.g. `_validate_evidence_package_basis_content(root, package, package_path, expectations)` in
  `survey_evidence_v2.py` (the `:719–846` body minus `:764–770` State block and minus `implementation_sha`,
  with `expectations = {acceptance_sha, canonical_source_state_path, issue_id, research_profile, ...}`
  passed explicitly from the session); similarly `_validate_screening_package_basis_content`,
  `_validate_result_batch_content`, `_validate_discovery_set_content` / `_validate_expansion_content`,
  `_normalize_record_content` + `_validate_graph_content` + `_validate_x_integration_content`,
  `_validate_ledger_content`, `_validate_completeness_content`, `_validate_view_content`,
  `_validate_supplement_content`, `_validate_selection_content` / `_validate_architecture_content` /
  `_validate_draft_content` (A2/A3/A6 bodies minus State-coupled interior, which itself calls the shared
  S/E cores). Location principle: the core lives next to the pure helpers it reuses (`citation_refs`,
  `_source_class`, `_check_subject_role`, token/URL/archive helpers), so a future content fix lands once.
- Original PUBLIC behavior is kept by THIN wrappers in the same existing files with UNCHANGED signatures:
  e.g. `validate_evidence_package_basis(root, package_path, package, implementation_sha)` loads
  `cfg`+`state`, runs the ONE State block (`verify_state_basis` + issue/Profile divergence), revalidates
  screening acceptance via the existing path, then delegates ALL content checks to the shared core. Existing
  callers (Weekly/Longform loaders, P1, full receipt replay) observe zero behavior change.
- The renewal source module (`survey_versioned_renewal_source_v2.py`) contains ONLY the session constructor
  (§2), the §0 six-condition enforcement, the Layer A/B orchestration (§3), and calls into the shared cores
  with session-derived `expectations`. It contains NO duplicated validator bodies.
- Exception path (discouraged): if a shared core cannot be extracted without changing existing-file control
  flow (import cycle, CLI coupling), the duplication MUST be justified in the implementation return (exact
  lines that force it) AND accompanied by a regression oracle proving equivalence: a test that runs BOTH the
  existing public validator (on a State-bound fixture) and the renewal core (on the same bytes via session)
  over identical accepted graphs and asserts identical accept/refuse on every §8 oracle (positives + all
  N-H negatives that target that family). Divergence without a passing equivalence oracle → NO-GO.
- Primary instruction enforced: no monkeypatch (`current_stage_basis_override` never entered), no caller
  verified-dict/`pending`/`already_verified` params, no data/flag bypass. The session carries verified BYTES
  (reloaded + SHA-checked by the path entry), never verified VERDICTS from a caller.

## 10. Predicate-matrix deltas (R1 → R2, exact)

- W0–W4/L0–L4: UNCHANGED except W2/L2 replaced by §4 per-schema label table (R1 blanket profile rule dropped).
- W5–W13/L5–L12/E1–E9/S1–S10/D1/X1/A1–A7/R1–R6 bodies: UNCHANGED as source locations; ownership of private
  validators changes from "NEW in renewal module" to "shared core in existing file + thin wrapper" (§9);
  PUBLIC entries change to §2 basis_path-only signatures (Finding 2).
- E3/S7/S9 §0 handling: UNCHANGED (§0 preserved); session supplies acceptance/basis/COPY proves per §2.
- S8 `Path(".")` fix: DROPPED (§7).
- §2.9 P1 manuscript/Gate/bundle row: REASSIGNED per §1 (accepted-loader → downstream/HIGH/fullset).
- T-table "no old bytes change": SUPERSEDED by §8 (4 new files + 1 existing-file branch, old/new pins separate).
- R1 §5 "16 exact signatures" list: SUPERSEDED by §§2–3/9 (basis_path-only publics + session-scoped privates
  + shared-core placement). R1 signatures with bare `(root, package_path)` MUST NOT be implemented as public.
- Basis name-map authority: R1 "basis-pinned rows" now gated by §5.2 finite prior-receipt match
  (`BASIS_ACCEPTED_SET_DRIFT` before content). No arbitrary serialized-map trust.
- U/C classification: R1 DM-row sentence equating U mismatch with migration SUPERSEDED by §6.

## 11. CLOSED vs still-OPEN matrix (no self-certified complete)

CLOSED (design rule fixed in R2; implementation must still realize it — a rule being closed does NOT authorize code):

- C1 accepted-loader scope (§1): manuscript/Gate/bundle NEVER in loader; pure projector/shape only.
- C2 entry discipline (§2): basis_path-only publics + same-invocation private session; no ambient/caller authority.
- C3 tool split (§3): subloader (no Git) vs full verifier (current closure/contract/schemas, no State) vs HIST epochs.
- C4 labels (§4): per-schema fields; route from Profile; table is the oracle.
- C5 expressions+provenance+match (§5): A1–A7 bodies, wrapper owners, prior-receipt verbatim match.
- C6 U-vs-migration (§6): mismatch ≠ migration; new-id C supported.
- C7 Path('.') (§7): no fix; dropped goal.
- C8 schema bytes (§8): 4 new files + 1 existing-file branch; old/new pins separate.
- C9 placement (§9): shared cores in existing files; wrappers unchanged; duplication only with justification + equivalence oracle.

Still-OPEN (implementation/proof required before Astra can confirm; each maps to §8-style blocker with NO-GO on weakening):

- O1 session + finite match implementation (§§2/5.2): constructor, `_load_basis_accepted_ref`, prior-receipt verbatim compare, HIGH pin interface. NO-GO if any content check needs caller verdicts/pending/override.
- O2 Layer B verifier (§3): current-closure recompute + contract/schema equality + HIST-epoch consumption + after-activation readback path (`validate_candidate→Reader→verify_renewal_source_proof`). NO-GO if drift undetectable without State load.
- O3 shared-core extractions (§9): one narrow core per family in its existing file + thin wrappers + equivalence oracles. NO-GO on semantic divergence without oracle.
- O4 downstream threading (referred to schema/interface return): `renewal_source_proof_ref`/`renewal_receipt_ref`/`renewal_source` keywords, digest bases, U predicate list enforcement, Freeze snapshot/alias exactness, full-set SAME-proof equality. This file states the loader side only.
- O5 fingerprints/closures/consumers (referred to third agent): old-format fingerprints, successor closure sets + bootstrap additions, control-diff, recipe boundary, mode discipline.
- O6 supply/error/CLI/seam oracles (referred to operation-oracles + schema returns): QA evidence field list, per-seam error/CLI map, fault/positive/negative oracles with intended seams.

Implementation stays BLOCKED until Astra confirms R2 + schema/interface R2 + operation-oracles + third-agent
fingerprint/closure returns jointly per decision §§9/11.3. Any unpreservable predicate → contract revision or
precise NO-GO, never a weakened checker. Whole NOT_READY / step4B3 OPEN / audit unstarted / DM021+022 OPEN.
Production semantic NO-GO on placeholder editions; synthetic approvals labelled. Stop at internal return; no code/tests.
