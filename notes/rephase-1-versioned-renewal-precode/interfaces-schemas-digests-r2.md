# Versioned renewal pre-code — interfaces / schemas / digests / call & file map R2 (author-side)

2026-10-23 JST. Author-side General pre-code return R2. Human HEAD `ce0de1a`.
Governing: `outputs/rephase-1-versioned-renewal-contract-decision.md` SHA256
`478f00510791b76af24aa7d61f398f0608f7ad8ae7808008c660f2bea6fbfdcf` INCLUDING §11;
mandatory `notes/rephase-1-versioned-renewal-contract/astra-review-resolution.md`;
BOTH independent reviews WITH final-binding addenda.
Read-only source: `.rephase-1-editorial-runtime/final-source-packaging/proof-copy/candidate-partial-b40de60`
(actual409/tree8ce + intended57). No source edits/imports/tests/build/fixture/restore/network/Git writes.
Preserves `interfaces-schemas-digests.md` (R1) unchanged; THIS file `interfaces-schemas-digests-r2.md`
is the ONLY new write in this unit (plus an appended superseding correction to
`operation-oracles.md` if needed, no other writes). All old docs preserved.

R1 defects corrected here (Astra CHANGES_REQUIRED 1–12). Each R1 occurrence is superseded by the
corresponding R2 section; where R1 said `null`, `NEW authoring`, `recorded pins only`,
`staged_manifest_ref`, `renewal_source{4 refs}`, `serialized U proof in manuscript digest`,
`augment EDITORIAL_*`, `in-place amend`, `9 keys`, `contract:object`, `retained_dest for KEEP`,
`all reviews in R`, `missing reader/Profile`, or unverified helper names, R2 below controls.

Conventions: `S`=string minLength1; `SHA`=pattern `^[0-9a-f]{64}$`; `GITSHA`=pattern `^[0-9a-f]{40}$`;
`INST`=string format date-time via `survey_production_v2.parse_instant:181` / `iso_utc:185-186`;
`INT1`=integer minimum1; `RID`=pattern `^[a-z0-9][a-z0-9-]{0,63}$`; all objects
`additionalProperties:false`; `schema_version` const `2.0-rc1`.
`core` = `survey_production_v2`; `schema_gate` = `survey_schema_v2` alias as imported in
`survey_editorial_publication_v2`, `survey_publication_v2`, `survey_reader_publication_v2`,
`survey_reader_surface_gate_v2`. Verified helpers in §6. Self-digest excludes only its named
digest field. File-ref SHA is full serialized bytes. Same-SHA different-path refused everywhere.

## 0. Binding rules (read first)

- Accepted State-SHA obeys decision §11.3 + both addenda + sibling
  `accepted-authority-readiness.md` §0, NOT old predicate-map F3/F4 wording. Package `state_sha256`
  stays historical; drift tolerated ONLY under §11.3 1–6 with same canonical SOURCE path +
  package==acceptance==basis + valid retained COPY chain + every other predicate. No package
  mutation; no original-`state_path`-vs-retained-dest compare.
- Renewal predecessor MUST be an existing versioned active set (editorial activation or prior
  renewal activation) with live seal + live record + live Candidate. Legacy-only
  (`REVIEWED_CORE_CHANGE` without a separate activation record) is UNSUPPORTED as a renewal
  predecessor. All prior refs nonnull. Never infer from canonical Candidate existence on disk.
- `authoring`/`reader` in basis are the SAME exact prior immutable bytes (prior set's
  `authoring-input` + complete `reader-surface-input`), not a new proposed input.
- Historical repo-tool verification at recorded epochs is MANDATORY in operation/normal proof,
  not audit-only. No digest-only attestation. Multiple epochs (`receipt_epoch`,
  `staged_producer_head`, schema epochs) are an exact map, not a collapsed digest.
- Renewal `VERSIONED_RENEWAL_SOURCE_V1` manifest has NO `staged_manifest_ref`,
  NO `retention_manifest_ref`, NO `scope_review_ref`. C has NO new old-format P3S staged manifest.
  New source proof IS the staged proof. C manuscript `renewal_source` is exactly
  `{path:S, sha256:SHA}` = `R/renewal-source-proof.json` path+SHA.
- U original manuscript bytes/digest unchanged; proof context is a function keyword ONLY, never
  serialized, never in digest. C new manuscript (new file) carries `renewal_source` and includes it.
  New Candidate/QA/Gate (all new files) carry proof refs and include them.
- Gate: ONE new `VERSIONED_RENEWAL_V1` derivation branch BOTH U and C; 4 old branches verbatim.
- Fixed by selected contract (no reopening): 4 NEW schema files
  (`versioned-renewal-basis-v2`, `versioned-renewal-source-proof-v2`,
  `versioned-renewal-source-manifest-v2`, `versioned-renewal-publication-set-v2`)
  + 1 new activation branch in existing `publication-surface-revalidation.schema.json`
  (legacy+editorial verbatim); new receipt kind `VERSIONED_RENEWAL_SOURCE_V1`;
  one new Gate branch; existing `before_active_digest` algorithm; Freeze derives proof from
  validated Candidate incl nested review + transitive snapshot; new basis/COPY validator in
  SOURCE module per §11 (`validate_renewal_basis`), history separate HIST structural
  (`verify_versioned_history`); free-text `reason` + fixed `reason_class`.
  ROOT still no code until complete crossmap (§11).

## 1. Ref shapes, paths, trust

- `P`=original proposal dir containing `proposal.json`. `R=P/renewals/<RID>`. `RID` lexical first
  (no `..`, `/`, `\`, empty). No recursive `renewals/.../renewals`, no latest-directory selection.
- `intent` ∈ `REUSE_TARGETS`|`RENDER_TARGETS`; proof `disposition` ∈ `REUSED_TARGETS`|`NEW_TARGETS`
  validated, never permission. U mismatch → `REUSE_TARGET_MISMATCH`, no auto-convert.
- Authority ref: `{"path":S,"sha256":SHA}`. Sized file ref:
  `{"path":S,"sha256":SHA,"byte_count":INT1}`. Named row: `{"name":S,"path":S,"sha256":SHA}`.
  PDF file ref with pages: `{"path":S,"sha256":SHA,"byte_count":INT1,"page_count":INT1}`.
  Closure row (receipt/current): `{"name":S,"path":S,"sha256":SHA}` (no `byte_count`).
  Code-dep row (staged): `{"path":S,"sha256":SHA,"byte_count":INT1}`.
  Contract (8 fields, `survey_production_v2.contract_identity:210-228`):
  `{"pipeline_contract_version":S,"pipeline_contract_sha256":SHA,`
  `"quality_contract_version":S,"quality_contract_sha256":SHA,`
  `"research_profile_version":S,"research_profile_sha256":SHA,`
  `"publication_profile_version":S,"publication_profile_sha256":SHA}`.
  Retention row: `{"roles":S[1..],"path":S,"sha256":SHA,"byte_count":INT1,`
  `"policy":enum["KEEP_IMMUTABLE","COPY_BEFORE_REPLACEMENT"],`
  `"retained_ref"?:{"path":S,"sha256":SHA},`
  `"retained_dest"?:S,"retained_sha256"?:SHA,"retained_byte_count"?:INT1}`
  with `allOf`: KEEP requires `retained_ref` and forbids `retained_dest|retained_sha256|
  retained_byte_count` (`editorial-retention-manifest-v2.schema.json:119-128`;
  `survey_editorial_retention_v2.py:67-68,1045-1056,1808-1820`); COPY requires
  `retained_dest+retained_sha256+retained_byte_count` and forbids `retained_ref`.
  KEEP `retained_ref` MUST equal `{"path":row.path,"sha256":row.sha256}` (live+retained-COPY E,
  never T live). COPY `retained_dest` MUST equal
  `_expected_retained_dest(proposal_dir,original_path)` (`:831-832`).
- All paths repo-local no-follow: `_lexical_rel` raw-first (`survey_editorial_publication_v2.py:223-237`),
  `_safe`/`_safe_file`/`_read_bytes_bounded`/`_Session.safe_read`, `O_NOFOLLOW`, bounded reads,
  strict JSON (`survey_schema_v2.parse_json_strict_bytes:64-87`, `loads_strict:90-101`,
  `load_json_strict:104-121`, `load_and_validate_json_strict:124-132`,
  `validate_instance:230-254`), `core.sha256_object:163-165` canonical
  (`sort_keys=True,separators=(",",":")`), `core.sha256_bytes:155-156`,
  `core.sha256_file:159-160`, `core.load_json:136-143`, `core.repo_local_path:282-290`,
  `core.aggregate_file_hash:168-178`, `core.repository_commit_sha:189-207`.
  Basis/proof/seal/activation paths are untrusted, fully reloaded every use. No caller dict,
  verified set, `pending_basis`, `already_verified`, route/kind enum, `seal_path`, ambient/global/cache.

## 2. Four NEW schemas — COMPLETE typed definitions

### 2.1 `versioned-renewal-basis-v2.schema.json` — `VERSIONED_RENEWAL_BASIS_V1`

All REQUIRED, no nullables:

- `schema_version`: const `2.0-rc1`. `kind`: const `VERSIONED_RENEWAL_BASIS_V1`.
- `renewal_id`: `RID`. `proposal_namespace`: `S` (=`P`).
- `issue_id`: `S`. `research_profile`: enum `["WEEKLY","THEMATIC"]`.
  `publication_profile`: enum `["WEEKLY_MAGAZINE","LONGFORM_SPECIAL"]`.
  `generator_route`: enum `["WEEKLY_GENERATED_V2","LONGFORM_GENERATED_V1"]`.
- `original_proposal_ref`: authority ref = `P/proposal.json`.
- `profile_ref`: authority ref = prior Production Profile file (exact prior active Profile bytes).
- `reviewed_reader_ref`: authority ref = prior complete `P/reader-surface-input-v2.json`
  (same exact prior complete reader bytes).
- `authoring_refs`: array len2, sorted by `name`, unique `name`, items named row:
  `[{"name":const "proposed-publication-authoring","path":S,"sha256":SHA},`
  ` {"name":const "accepted-draft-archive","path":S,"sha256":SHA}]`
  = EXACT prior set's `authored_refs` (cf. `survey_editorial_publication_v2.py:1881-1884`).
- `accepted_refs`: array minItems1, sorted by `name`, unique `name`, items named row.
  MUST equal EXACT prior receipt's `accepted_refs` list verbatim (names include
  `production-profile`, `issue-architecture`, `synthesis-input`, `synthesis-result`,
  `draft-package:<pid>`, `draft-result:<pid>`, `evidence-acceptance`, `candidate-matrix`,
  `materiality-ledger`, `discovery-acceptance`, `evidence-card:<task_id>` per
  `survey_weekly_derivation_v2.py:533-572`; Longform same families per
  `survey_longform_derivation_v2`). No Profile/authoring addition/removal/relabel.
  Authoritative base refs (§1 profile/reader/authoring) are separate top-level pins;
  where names overlap (e.g. `production-profile`), values MUST be equal; meaning of
  `accepted_refs` is unchanged (route accepted graph, not supplemental deps).
- `original_validation_ref`: authority ref = original validation checkpoint
  (`State.checkpoint_provenance.validation`).
- `prior_selected_ref`: authority ref = prior active seal (`P/.../publication-set.json` or
  prior `R/publication-set.json`). `prior_record_ref`: authority ref = prior activation record.
  `prior_candidate_ref`: authority ref sized? = prior active Candidate
  (`R` or `P` `publication-candidate-v2.json` path+SHA; Candidate file ref for basis pin is
  `{"path":S,"sha256":SHA}`; live `byte_count` checked via `_check_file_ref`, not stored here).
  All three REQUIRED (no null; legacy-only without record/Candidate refuses as predecessor).
- `canonical_anchor`: `{"kind":enum["VALIDATION_CHECKPOINT","LEGACY_REVALIDATION"],`
  `"ref":authority ref}` (permanent anchor: latest legacy immediately before FIRST versioned
  activation; never rolled forward).
- `before_state_ref`: authority ref = fresh canonical live before-State path+SHA at entry.
- `retained_copy_ref`: sized file ref = `R/retained/before/<original-State-relative-path>`
  (fresh second-generation COPY; `byte_count`=len(retained bytes)).
- `old_tool_epochs`: `{"receipt_epoch":{"repository_commit_sha":GITSHA,"contract":Contract8,`
  `"closure":NamedRow[1..]},`
  `"staged_epoch":{"producer_head":GITSHA,`
  `"code_deps":CodeDepRow[1..],"style_input_ref":SizedRef},`
  `"schema_epochs":{"proposal_schema_sha256":SHA,"retention_schema_sha256":SHA,`
  `"staged_schema_sha256":SHA,"receipt_schema_sha256":SHA,"set_schema_sha256":SHA,`
  `"revalidation_schema_sha256":SHA}}`
  (separate epochs per `survey_editorial_staged_source_v2:1039` vs receipt
  `current_tools.repository_commit_sha`; each T row checked against ITS OWN epoch blob via
  `git cat-file -e <epoch>^{commit}` + `git show <epoch>:<path>` SHA (+`byte_count` where sized);
  never live-path equality; never cross-substituted; missing → `HISTORY_BLOB_MISSING`).
- `current_tool_epoch`: `{"repository_commit_sha":GITSHA,"contract":Contract8,`
  `"closure":NamedRow[1..]}` (CURRENT `_editorial_closure_rows` union-50
  `survey_editorial_publication_v2.py:1958-1993` + `core.contract_identity`; pinned from CURRENT
  disk at capture).
- `retention_rows`: array minItems1, items RetentionRow (§1). MUST contain exactly one
  `state:authority` COPY row with `path/sha256==before_state_ref`,
  `retained_dest==R/retained/before/<path>`, `retained_sha256==retained_copy_ref.sha256`,
  `retained_byte_count==retained_copy_ref.byte_count`; all other rows KEEP with
  `retained_ref=={path,sha256}` (prior seal/Candidate/trio/manuscript/PDF/reviews/build-record).
- `requested`: enum `["REUSE_TARGETS","RENDER_TARGETS"]`.
- `toolchain_spec_ref`: authority ref REQUIRED iff `requested==RENDER_TARGETS`; ABSENT iff
  `requested==REUSE_TARGETS` (U has no toolchain arg; Python `toolchain_spec_path=None`, CLI omits
  `--toolchain-spec`). No `null` sentinel stored; key presence is the signal.
- `manuscript_spec_ref`: authority ref (manuscript spec sibling outside unclaimed `R`).
- `executor`: `S`. `recorded_at`: `INST`. `basis_sha256`: `SHA` =
  `core.sha256_object({all keys except basis_sha256})`.
- No `set_ref`, `candidate_ref`, `gate_ref`, `bundle_ref`, review-RECORD refs, activation hash,
  or live State pointer inside basis. Basis carries no proof ref; proof carries basis ref (one-way).

### 2.2 `versioned-renewal-source-proof-v2.schema.json` — `VERSIONED_RENEWAL_SOURCE_PROOF_V1`

All REQUIRED except U-only refs (conditional presence, §11):

- `schema_version`: const `2.0-rc1`. `kind`: const `VERSIONED_RENEWAL_SOURCE_PROOF_V1`.
- `basis_ref`: authority ref = `R/renewal-basis.json`.
- `issue_id`: `S`. `research_profile`: enum `["WEEKLY","THEMATIC"]`.
  `publication_profile`: enum `["WEEKLY_MAGAZINE","LONGFORM_SPECIAL"]`.
  `generator_route`: enum `["WEEKLY_GENERATED_V2","LONGFORM_GENERATED_V1"]`
  (must agree with basis).
- `reviewed_reader_ref`: authority ref (MUST equal basis `reviewed_reader_ref`).
- `authoring_refs`: array len2 named rows (MUST equal basis `authoring_refs`).
- `accepted_refs`: array minItems1 named rows (MUST equal basis `accepted_refs`).
- `supported_contract`: Contract8 (old/new contract pins; steady-state requires exact closure
  membership + schema/contract equality apart from permitted implementation/style bytes).
- `supported_epochs`: `{"receipt_epoch":GITSHA,"staged_producer_head":GITSHA}` (the two old epochs
  this proof was checked against; each T row bound to its own epoch, §2.1).
- `dependency_closure`: array minItems1 named rows (CURRENT closure at proof time; MUST equal
  basis `current_tool_epoch.closure` unless a genuine eligible Core commit landed between capture
  and proof → `BASIS_CURRENT_TOOL_DRIFT`, fresh basis required).
- `output_trio_refs`: `{"primary":SizedRef,"bibliography":SizedRef,"style":SizedRef}`.
  U: OLD trio paths at original `P/staged-source/{main.tex,references.bib,jgaisurvey.sty}`.
  C: NEW trio paths under `R/staged-source/{main.tex,references.bib,jgaisurvey.sty}`
  (trio FILES only, NO manifest file; proof IS the staged proof).
  Same SHA at a different target path is C.
- `reader_digest`: `SHA` = `sha256(canonical_reader_bytes)` freshly rederived via State-free leaf +
  pure projector at proof time.
- `trio_digest`: `SHA` = `core.sha256_object({"primary":SHA,"bibliography":SHA,"style":SHA})`
  over CURRENT derived trio bytes at the proof paths.
- `comparison`: `{"reader_equal":boolean,"trio_equal":boolean,`
  `"disposition":enum["REUSED_TARGETS","NEW_TARGETS"]}` (validated, never permission).
- U-ONLY (present REQUIRED iff `disposition==REUSED_TARGETS`; ABSENT iff `NEW_TARGETS`):
  `old_manuscript_ref`: SizedRef = original `P/publication/reader-manuscript-v2.json`;
  `old_build_unit_refs`: `{"pdf":PdfRef,"log":SizedRef,"digest":SizedRef,`
  `"record":authority ref}` where `PdfRef={"path":S,"sha256":SHA,"byte_count":INT1,"page_count":INT1}`
  = original `P/publication/build/{main.pdf,main.log,main.pdf.sha256}` as a unit +
  original `P/publication/build-record.json`. No duplicate trio/manuscript/PDF/log/review copies.
- `executor`: `S`. `recorded_at`: `INST`. `proof_sha256`: `SHA` =
  `core.sha256_object({all keys except proof_sha256})`.
- No future refs (no new manuscript hash, Candidate/seal/activation ref, or own digest in payload).

### 2.3 `versioned-renewal-source-manifest-v2.schema.json` — `VERSIONED_RENEWAL_SOURCE_V1`

All REQUIRED (no staged/retention/scope refs):

- `schema_version`: const `2.0-rc1`. `kind`: const `VERSIONED_RENEWAL_SOURCE_V1`.
- `issue_id`: `S`. `research_profile`: enum `["WEEKLY","THEMATIC"]`.
  `publication_profile`: enum `["WEEKLY_MAGAZINE","LONGFORM_SPECIAL"]`.
  `generator_route`: enum `["WEEKLY_GENERATED_V2","LONGFORM_GENERATED_V1"]`.
- `proposal_ref`: authority ref = `P/proposal.json`.
- `renewal_basis_ref`: authority ref = `R/renewal-basis.json`.
- `renewal_proof_ref`: authority ref = `R/renewal-source-proof.json`.
- `reviewed_reader_ref`: authority ref (MUST equal proof `reviewed_reader_ref`).
- `authoring_refs`: array len2 named rows (MUST equal proof `authoring_refs`).
- `accepted_refs`: array minItems1 named rows (MUST equal proof `accepted_refs`).
- `current_tools`: `{"repository_commit_sha":GITSHA,"contract":Contract8,`
  `"closure":NamedRow[1..]}` (MUST equal proof `dependency_closure` + contract).
- `outputs`: `{"primary":SizedRef,"bibliography":SizedRef,"style":SizedRef}`
  (U old paths; C new `R/` paths; staged main→receipt primary mapping explicit).
- `build_record_ref`: authority ref = `R/build-record.json` (exactly one variant below).
- `receipt_sha256`: `SHA` = `core.sha256_object({all keys except receipt_sha256})`.
  Build record exists BEFORE receipt (receipt binds build-record).

`R/build-record.json` (same file, variant-tagged, one variant REQUIRED):

- Common REQUIRED: `schema_version`: const `2.0-rc1`. `variant`:
  enum `["REUSED_BUILD","EXECUTED_BUILD"]`. `issue_id`: `S`.
  `proposal_ref`: authority ref. `renewal_basis_ref`: authority ref.
  `renewal_proof_ref`: authority ref. `recipe_ref`: authority ref = `.latexmkrc`
  (`REQUIRED_RECIPE_MARKERS` `survey_editorial_publication_v2.py:1228-1243`).
  `recorded_at`: `INST`. `build_sha256`: `SHA` =
  `core.sha256_object({all keys except build_sha256})` (INCLUDING input/output refs).
- `REUSED_BUILD` (U-ONLY, requires basis `requested==REUSE_TARGETS` + absent toolchain spec,
  no build spawn): `original_record_ref`: authority ref = original
  `P/publication/build-record.json`; `original_pdf_ref`: PdfRef;
  `original_log_ref`: SizedRef; `original_digest_ref`: SizedRef (original build3 as a unit);
  `renewal_tools`: `{"old":GITSHA,"new":GITSHA}`; `no_rebuild`: const `true`.
  No `declared_inputs`/`recipe`/`toolchain`/`outputs`/`exit_code` keys.
- `EXECUTED_BUILD` (C-ONLY, requires basis `requested==RENDER_TARGETS` + explicit toolchain spec,
  disposable root + exclusive transfer + readback): `declared_inputs`:
  `{"primary":authority ref,"bibliography":authority ref,"style":authority ref}` (new `R/` trio);
  `recipe`: `{"fixed_steps":S[1..]}` (fixed recipe under the selected existing recipe);
  `toolchain`: `{"executable":S,"versions":object-exact-map,"argv":S[],"env":object-exact-map}`
  where `versions`/`argv`/`env` are the EXACT recorded maps (absolute executable, exact argv
  allowlist, allowlisted env without `GIT_*/PATH/PYTHONPATH`, `.latexmkrc` markers
  `survey_editorial_publication_v2.py:1183-1244`); `outputs`:
  `{"publication-pdf":SizedRef,"build-log":SizedRef,"pdf-digest":SizedRef}` under `R/build/`;
  `exit_code`: const `0`. No `original_*`/`renewal_tools`/`no_rebuild` keys.

### 2.4 `versioned-renewal-publication-set-v2.schema.json` — `VERSIONED_RENEWAL_SET_V1`, `SEALED_INERT`

All REQUIRED:

- `schema_version`: const `2.0-rc1`. `kind`: const `VERSIONED_RENEWAL_SET_V1`.
  `status`: const `SEALED_INERT`.
- `issue_id`: `S`. `research_profile`: `S` (must equal basis/proof).
  `publication_profile`: enum `["WEEKLY_MAGAZINE","LONGFORM_SPECIAL"]`.
- `proposal_ref`: authority ref = `P/proposal.json`.
- `renewal_basis_ref`: authority ref. `renewal_proof_ref`: authority ref.
  `source_receipt_ref`: authority ref = `R/validated-source-manifest.json`.
  `build_record_ref`: authority ref = `R/build-record.json`.
- `roles`: object with EXACT 15 keys
  `reader-input,authoring-input,source-receipt,reader-manuscript,validated-source,bibliography,`
  `style,publication-pdf,build-log,pdf-digest,quality-regression-bundle,semantic-review,`
  `visual-review,reader-surface-gate,publication-candidate`, each SizedRef.
  U: manuscript/trio/build3/review RECORD roles point at ORIGINAL immutable paths;
  receipt/QA-bundle/Gate/Candidate point at NEW `R/` paths.
  C: reader/authoring/retention/scope-history point at ORIGINAL `P/` paths; all else NEW `R/` paths
  EXCEPT supplied postrender reviews MAY be external repo-contained immutable paths (pinned,
  not writer-owned, never deleted/rewritten; writer-owned paths cannot alias supplied paths).
  No `external_reviews` duplicate map, no activation hash. Seal path MUST be
  `R/publication-set.json` (new layout; old fixed `P/publication/publication-set.json`
  `survey_publication_set_v2.py:486-487` preserved verbatim for old branch).
- `set_sha256`: `SHA` = `core.sha256_object({all keys except set_sha256})`.
- Low validator cross-binds proof/basis/receipt refs in addition to role maps; full set demands
  Candidate/QA/Gate/receipt/seal agree on the SAME proof path+SHA.

Owned files in `R`: `renewal-basis.json` (after COPY/inventory), `retained/before/<rel>`,
`renewal-source-proof.json`, `validated-source-manifest.json`, `build-record.json`,
`quality-regression-bundle-v2.json`, `reader-surface-gate-v2.json`,
`publication-candidate-v2.json`, `publication-set.json`; C additionally
`trio FILES staged-source/{main.tex,references.bib,jgaisurvey.sty}` (NO manifest),
`build/{main.pdf,main.log,main.pdf.sha256}`, `reader-manuscript-v2.json` (C only).
U writes no duplicate reader/trio/manuscript/PDF/log/reviews. Supplied QA/review records may be
external safe repo paths (pinned, not writer-owned). Exclusive inventory = explicitly declared
evidence files inside `R` only.

## 3. New strict activation branch — `VERSIONED_RENEWAL_ACTIVATION_V1`

Extends `publication-surface-revalidation.schema.json` `oneOf` with a third branch; legacy
(`97-166`) + editorial (`167-245`) verbatim. All REQUIRED, no nullables:

- `schema_version`: const `2.0-rc1`. `kind`: const `VERSIONED_RENEWAL_ACTIVATION_V1`.
- `issue_id`: `S`. `reason_class`: const `REVIEWED_VERSIONED_CORE_RENEWAL`.
- `reason`: `S` truthful free-text Core-change reason (never false editorial; `reason_class`
  fixed by kind, never from CLI flag).
- `lifecycle`: const `VALIDATED_DRAFT`.
- `prior_checkpoint`: authority ref = original validation checkpoint.
- `supersedes`: authority ref = prior versioned activation record (REQUIRED; no null; first
  versioned activation supersedes the prior editorial activation record, never a legacy-only row).
- `canonical_anchor`: `{"kind":enum["VALIDATION_CHECKPOINT","LEGACY_REVALIDATION"],`
  `"ref":authority ref}` (permanent anchor; never rolled forward).
- `before_state_ref`: authority ref = fresh canonical before-State.
- `retained_copy_ref`: sized file ref = `R/retained/before/<rel>` COPY binding.
- `before_active_digest`: `SHA` recomputed by existing
  `survey_publication_set_v2.before_active_digest:353-415`
  (exactly 7 publication roles, sorted, unique, `{"name":S,"path":S,"sha256":SHA}` +
  `candidate:{"path":S,"sha256":SHA}` via `core.sha256_object({"effective":rows,"candidate":...})`).
- `before_candidate_ref`: authority ref = observed before-Candidate (REQUIRED; no null;
  renewal predecessor MUST have a live Candidate).
- `set_ref`: authority ref = `R/publication-set.json`.
- `renewal_basis_ref`: authority ref. `renewal_proof_ref`: authority ref
  (bind COPY + old/new epochs through exact refs, not effective7 alone — decision §11.2).
- `core`: Contract8 + `{"implementation_commit_sha":GITSHA}` (exact 9 keys: 8 contract + commit).
- `executor`: `S`. `recorded_at`: `INST`.
- `establishment`: `{"state_sha256":SHA,"lifecycle":const "VALIDATED_DRAFT",`
  `"architecture_review":const "approved","publication_preview":const "pending",`
  `"freeze":const "pending","release":const "pending",`
  `"implementation_commit_sha":GITSHA,"recorded_at":INST}`.
- Chain/anchor: mixed editorial/renewal chain active-inclusive max32, strictly increasing sequence,
  nondecreasing time, no cycles (`CHAIN_LIMIT=32` `:109`, `_walk_chain_backwards:1023-1051`,
  `1060-1230`); later legacy successor unsupported (`:1189`); R1/canonical pre-write refusal kept
  (`survey_weekly_mechanical_refresh_v2.py:837`, `survey_agent_control_v2.py:2210-2229`).
  Sole live mutation remains `publication_revalidation_provenance` (exclusive new record,
  known-byte State temp/replace, full new active readback).

## 4. Old strict branches — renewal proof threading (old bytes verbatim)

### 4.1 Reader manuscript (`reader-manuscript-v2.schema.json`, `survey_reader_publication_v2.py:218-270,347-451`)

- Current `editorial_source` = `{"proposal_ref":authority ref,"staged_manifest_ref":authority ref}`
  (`:104-112`) preserved VERBATIM. `build_manuscript_manifest:347-410`,
  `validate_manuscript_manifest:413-451`, `_validate_manifest_semantics:218-344`
  (live `verify_staged_source:237-247` in current-P3S mode, trio main→primary `:253-269`).
- U: NO schema change, NO new serialized field, NO digest change. Original file bytes and
  `manifest_sha256` unchanged. Proof context is a FUNCTION keyword ONLY:
  `renewal_source_proof_ref=None` (`{"path":S,"sha256":SHA}` reloaded) on builders/validators.
  With a fully valid matching U proof, validators check old source-proof identity HISTORICALLY
  (typed E/T, live+retained-COPY E, epoch-blob T, never CURRENT `verify_staged_source`) PLUS all
  current manuscript semantics + exact trio against the new proof (decision §11.2 U list).
  Without that context, standalone old validation keeps current P3S refusal. Never edit an old
  manuscript to add context. Digest: `manifest_sha256 == core.sha256_object({14 keys})` where 14 =
  `schema_version,issue_id,research_profile,publication_profile,status,production_profile,`
  `architecture,architecture_approval,primary_source,supporting_files,architecture_coverage,`
  `reader_requirements,authored_by,recorded_at` (`:427-442`); `editorial_source` included as 15th
  iff present (`:443-447`); `renewal_source_proof_ref` NEVER serialized for U, never in digest.
- C (new file ONLY): `renewal_source`: `{"path":S,"sha256":SHA}` = `R/renewal-source-proof.json`
  path+SHA (EXACTLY one ref, no extra basis/staged/proposal). Mutually exclusive with
  `editorial_source` (XOR; never both, never neither for renewed sets). Digest:
  `manifest_sha256 == core.sha256_object({14 keys + renewal_source})` (15 keys total when C).

### 4.2 Review records (`survey_reader_publication_v2.py:601-692`)

Unchanged schema/bytes for U reuse. `validate_review_record` digest:
`review_sha256 == core.sha256_object({14 keys})` where 14 =
`schema_version,issue_id,research_profile,publication_profile,review_kind,status,`
`production_profile,reader_manuscript,source,pdf,page_count,checks,reviewed_by,recorded_at`
(`:617-636`). Nested `validate_manuscript_manifest:643-647` propagates the SAME reloaded proof
ref (explicit param, never ambient). Historical same-reader scope reloaded with exact
before/after relationships; never fresh P2V `SCOPE_BOUND`. No proof field serialized in the
review file; binding lives in the containing NEW Candidate/bundle/Gate.

### 4.3 Quality bundle (`quality-regression-bundle-v2.schema.json`, `survey_quality_v2.py:193-274`)

Old branch verbatim. `build_bundle:193-229` digest:
`bundle_sha256 == core.sha256_object({9 keys})` where 9 =
`schema_version,issue_id,production_profile,research_profile,publication_profile,source,pdf,`
`checks,status` (`:213-224`). `validate_bundle:232-274` recomputes the same 9 (`:259-263`).
`validate_checks:132-174` validates SUPPLIED rows only (exact `check_id/kind/status/executor/`
`evidence/recorded_at/result`, applicable-family completeness, all `PASS`), never executes tests.
NEW (new files ONLY, both U and C): builders/validators take
`renewal_source_proof_ref=None` (`{"path":S,"sha256":SHA}` reloaded), serialize it as
`renewal_source_proof_ref` in the new strict optional branch, digest =
`core.sha256_object({9 keys + renewal_source_proof_ref})` (10 keys when renewed).
Validators derive from own payload; outer expected ref must be identical when present.

### 4.4 Reader-surface Gate (new branch BOTH U and C, old branches verbatim)

Old 4 `derivation` variants (`DIRECT_PRIMARY`, `WEEKLY_GENERATED_V2`, `LONGFORM_GENERATED_V1`,
`EDITORIAL_PUBLICATION_V1`) in `reader-surface-gate-v2.schema.json:160-217` + dispatcher
`_derivation_for_manuscript:1145-1330` preserved VERBATIM (editorial branch `:1159-1253` with
live `verify_staged_source:1173`, fixed receipt `P/publication/validated-source-manifest.json`
`:1182-1185`, early scope reload `:1195-1224`, trio mapping `:1225-1251`).
NEW 5th variant (BOTH U and C): `{"route":const "VERSIONED_RENEWAL_V1",`
`"scope":const "RENEWAL_MAIN_BIB_STYLE","receipt":authority ref,`
`"renewal_source_proof_ref":authority ref,"renewal_receipt_ref":authority ref}`
where `receipt` = `R/validated-source-manifest.json` path+SHA,
`renewal_source_proof_ref` = `R/renewal-source-proof.json` path+SHA,
`renewal_receipt_ref` = same receipt path+SHA (redundant path+SHA pair binds proof+receipt
explicitly per decision §11.2; validators check all three agree + full-set SAME-proof equality).
Gate builder `evaluate_reader_surface_gate:1333-1694` digest:
`gate_sha256 == core.sha256_object({13 keys})` where 13 =
`schema_version,issue_id,publication_profile,status,scanned_surfaces,rules_checked,`
`suppressions,findings,summary,evaluated_by,recorded_at,derivation,semantic_authority`
(`:1650-1685`); validator `_inspect_gate_record` recomputes the same 13 (`:1737-1753`).
Renewed Gate `derivation` is the new 5th variant (old variants never augmented); present renewal
refs are inside `derivation` and thus in digest. Old Gates keep old 4 variants + 13-key digest
without renewal refs. Context never selects a live Candidate; State-selected equality mandatory.

### 4.5 Publication Candidate (`publication-candidate-v2.schema.json`, `survey_publication_v2.py:668-814`)

Old branch verbatim. `build_candidate:668-746` digest:
`candidate_sha256 == core.sha256_object({10 keys})` where 10 =
`schema_version,issue_id,publication_profile,status,reader_manuscript,source,pdf,`
`quality_bundle,semantic_review,visual_review` (`:730-743`; `pdf` includes `page_count` `:737`).
`validate_candidate:749-814` recomputes the same 10 (`:753-766`) + cross-bindings `:769-811`
(manuscript `primary_source==source` `:778`, bundle source/PDF `:784-788`, review
manuscript/source/PDF/size/page `:801-811`, PDF drift `:792-793`).
NEW (new files ONLY, both U and C): same `renewal_source_proof_ref=None` keyword, serialized in
new strict optional branch, digest =
`core.sha256_object({10 keys + renewal_source_proof_ref})` (11 keys when renewed).
Validators derive from own payload; outer expected ref must be identical when present.

Digest summary (§11.2): old absent-field behavior unchanged; present renewal fields in NEW
Candidate/bundle/Gate (and C manuscript) payloads are included; new basis/proof/receipt/seal
include EVERY declared field except their one self-digest; file-ref SHA is full serialized bytes;
seal+activation bind basis/proof/COPY through exact refs, not effective7 alone.

## 5. Exact entries, signatures, errors, CLI (consistent with §11, no verified dict)

All paths `str|Path` repo-local no-follow; all refs untrusted fully reloaded (lexical → `_safe`,
bounded read, strict JSON, CURRENT-disk schema for E docs, self-digest recompute, live SHA/size,
cross-bind, pin recheck after work). No caller dict/verified set/`pending_basis`/
`already_verified`/route-kind enum/`seal_path`/ambient/cache. `recorded_at` via
`core.parse_instant` / `core.iso_utc`.

```text
_observe_renewal_entry(root:Path|str, state_path:Path|str)
  -> {state,state_sha,prior_history:{seal,receipt,proof_or_staged,retention,scope_refs,epochs},
      current_nonpublication_authority,current_tool_predicates,pins}
  # HIGH private before capture; in-memory pins only; no basis yet; no verified out-param.
  # Errors: BASIS_ENTRY_INELIGIBLE, HISTORY_*.

prepare_renewal(root, state_path, renewal_id:RID, intent:REUSE_TARGETS|RENDER_TARGETS,
  manuscript_spec_path:Path|str, toolchain_spec_path:Path|str|None,
  executor:S, recorded_at:datetime|None)
  -> {renewal_dir:R, basis_path:R/renewal-basis.json,
      retained_copy:R/retained/before/<rel>, pins}
  # U: toolchain_spec_path MUST be None (CLI omits --toolchain-spec); no build spawn.
  # C: toolchain_spec_path REQUIRED (explicit spec; rechecked, never synthesized).

load_renewal_accepted_authority(root:Path, basis_path:Path)
  -> {surface,records,accepted_refs,authored_refs}
  # SOURCE leaf detached; no State object, no implementation_sha, no verified-records param.
  # Called by source proof via persisted path. Full bodies/bans in sibling
  # accepted-authority-readiness.md §§1-2 (referenced, not duplicated).

validate_renewal_basis(root:Path|str, basis_path:Path|str)
  -> {basis,retained:{...},unchanged_evidence:{...}}
  # SOURCE module; detached retained-COPY + unchanged-evidence checks on EVERY proof readback;
  # validates retained before-State, never live-before equality.

verify_versioned_history(root:Path|str, record_path:Path|str)
  -> {HISTORICAL_IDENTITY_VERIFIED, observed_refs:{...}}
  # HISTORY leaf record-only, no State arg. Reloads record/schema/kind/anchor/supersedes chain/
  # set/receipt/renewal-proof/basis/retention refs + original scope evidence. Epochs from those
  # records, never caller commit/verified map. Owns typed E/T classification, COPY mapping/
  # inventory, old self-/cross-digests. Returns descriptive VERIFIED + observed refs, never a permit.
  # MUST NOT call current low validate_seal/selection, P2R/P3S, high receipt, P2V,
  # agent/Reader/Gate/Candidate.

observe_renewal_authority(root, state_path, basis_path)
  -> {live_current_before,retained_before,selected_predecessor,current_tools,pins}
  # HIGH basis-bound; after basis write, before finalize, immediately before activate.
  # Reopens/compares ALL inputs; demands live State == fresh before ref.

finalize_renewal(root, state_path, basis_path, checks_path,
  semantic_review_path:Path|str|None, visual_review_path:Path|str|None,
  executor:S, recorded_at:datetime|None)
  -> {set_path:R/publication-set.json, seal,pins}
  # NULL review args ONLY for validated U (derive predecessor RECORD refs; replacement review at
  # a different path never silently reused). C requires new postrender reviews at exact new targets
  # (external repo-contained immutable final paths allowed, pinned not writer-owned) + actual QA.
  # Supplied files are read-only inputs (reload schemas/results/targets, exact dependency manifest
  # path/hash/size/type incl files inside R, exclude unlisted, pin dir inventories, recheck
  # before/after writes). Externals never deleted/rewritten; writer paths cannot alias supplied paths.

validate_renewal_receipt(root, receipt_path) -> receipt
validate_prepared_renewal_set(root, state_path, set_path) -> validated_set
activate_renewal(root, state_path, set_path, reason:S, executor:S, recorded_at:datetime|None)
  -> result  # reason free-text Core-change reason; reason_class fixed REVIEWED_VERSIONED_CORE_RENEWAL.
resume_renewal_activation(root, state_path, record_path) -> result
  # Reloads record+set+basis; compares COMPLETE §11.1 intent (branch/issue/checkpoint/anchor/
  # supersedes/before-State/digest/Candidate/set/basis/new-core/executor/reason/time), not set SHA alone.
verify_renewal_history(root, record_path) -> historical_result
  # HIGH wrapper delegating to verify_versioned_history; structural loading of a renewal proof
  # does NOT execute its current-replay branch.
```

Renderer-equality (U, NEW): `verify_renewal_rerender_equality(root, basis_path, proof_path)
-> {reader_equal:bool,trio_equal:bool,disposition}` (CURRENT renderer/style → disposable temp trio
+ complete reader comparison vs OLD bytes at ORIGINAL paths; never `P/publication/` or `R/`;
mismatch → `REUSE_TARGET_MISMATCH`, no auto-C). C staged derivation (NEW):
trio FILES under `R/staged-source/` (NO manifest file; proof IS staged proof); manuscript (C
`renewal_source` branch) + real disposable build/transfer independently preparable AFTER proof,
BOTH BEFORE external review. Receipt binds build-record, never precedes it (corrects illustrative
receipt-before-build remedy).

Errors: `EditorialError(code,phase,disposition,detail)` (`.code/.phase/.disposition/.detail`
`survey_editorial_publication_v2.py:181-191`); low `PublicationSetError` (`CHAIN_LIMIT=32`
`survey_publication_set_v2.py:109`). New codes per decision §11.1: `HISTORY_*`
(`HISTORICAL_IDENTITY_VERIFIED` vs `HISTORY_COMMIT_MISSING/HISTORY_BLOB_MISSING/`
`HISTORY_SCHEMA_MISSING/HISTORY_DIGEST_MISMATCH/HISTORY_ANCESTOR/HISTORY_MODE/`
`HISTORY_TOOL_EPOCH_DRIFT/HISTORY_PACKAGE_MUTATED`); `BASIS_*`; `RENEWAL_PROOF_*`;
`REUSE_TARGET_MISMATCH`; `UNSUPPORTED_MIGRATION`; `REVIEW_TARGET_MISMATCH`;
`RECORD_COLLISION`; `INTENT_COLLISION`/`INTENT_MISMATCH`; `INDETERMINATE`; readonly
`ALREADY_ACTIVE`. CLI: `prepare/finalize/validate-receipt/validate-set/activate/resume/history`
in new high module (`--state/--renewal-id/--intent/--manuscript-spec/[--toolchain-spec U-absent/
C-required]/--basis/--checks/[--semantic-review/--visual-review U-null-only]/--receipt/--set/`
`--reason/--executor/--recorded-at/--record`); success `0`, refusal-or-operation-failure `2`
(`main():3914-3917` discipline), unexpected nonzero never PASS.

Verified helper existence (actual source): `survey_production_v2.load_json:136`,
`sha256_bytes:155`, `sha256_file:159`, `sha256_object:163`, `aggregate_file_hash:168`,
`parse_instant:181`, `iso_utc:185`, `repository_commit_sha:189`, `contract_identity:210`,
`repo_local_path:282`; `survey_schema_v2.parse_json_strict_bytes:64`,
`loads_strict:90`, `load_json_strict:104`, `load_and_validate_json_strict:124`,
`validate_instance:230`, `load_and_validate_json:257`; `survey_weekly_derivation_v2._artifact:140`,
`_safe:71`, `load_derivation:489`, `current_closure:587`, `_verify_head_bytes:591`;
`survey_publication_set_v2.before_active_digest:353`, `validate_seal:445`,
`_check_doc_refs_against_seal:433`, `_walk_chain_backwards:1023`,
`validate_activation_record:1239`, `require_active_or_canonical:2118`,
`resolve_publication_selection:1807`; `survey_editorial_publication_v2._fail:190`,
`_lexical_rel:223`, `prepare_publication:1552`, `finalize_publication:2013`,
`validate_editorial_receipt:692`, `validate_prepared_set:2555`, `activate_publication:3155`,
`resume_activation:3643`, `verify_activation_history:3782`, CLI `3837-3917`;
`survey_reader_publication_v2.build_manuscript_manifest:347`,
`validate_manuscript_manifest:413`, `validate_review_record:601`;
`survey_reader_surface_gate_v2._derivation_for_manuscript:1145`,
`evaluate_reader_surface_gate:1333`; `survey_quality_v2.validate_checks:132`,
`build_bundle:193`, `validate_bundle:232`; `survey_publication_v2._prepare_freeze_inputs:171`,
`_preflight_freeze_pair:323`, `build_candidate:668`, `validate_candidate:749`;
`survey_stage_validation_v2._require_active_candidate_binding:73`;
`survey_editorial_retention_v2._expected_retained_dest:831`,
`_retained_expected_sets:835`, `capture_retention:857`, `verify_retention:1737`.

## 6. Acyclic U/C map; file/pin inventory; context/Freeze/active vs inert

DAG: prior history + fresh before-State/selection + unchanged accepted inputs
→ `_observe_renewal_entry` (HIGH, no basis) → exclusive COPY claim + inventory + basis LAST +
pin recheck → `observe_renewal_authority` (HIGH basis-bound) → `load_renewal_accepted_authority`
(SOURCE leaf, persisted basis_path) → pure projection/render AFTER all authority checks →
source proof → C trio FILES (C only, old closed4 untouched) → C manuscript (`renewal_source`
`{path,sha256}`) + real disposable build/transfer (C only, after proof, both before external review)
→ build record (REUSED vs EXECUTED) → receipt (AFTER build-record) → fresh QA + new QA bundle
(`validate_checks` supplied-only) + postrender reviews (C new exact targets incl external final
paths; U derive predecessor RECORD refs) → Gate (new `VERSIONED_RENEWAL_V1` both U/C) →
Candidate (nested manuscript/reviews/bundle with SAME proof ref) → seal (`R/publication-set.json`)
LAST → `validate_prepared_renewal_set` → explicit activate (sole `publication_revalidation_provenance`
mutation, known-byte temp/replace, full new active readback) → normal active Candidate → direct
stage → synthetic Preview/Freeze/Release. Bans per decision §4/§11.1 (history/source/high layering;
low structural-only, no State recursion; no monkeypatch/caller verified set/pending/implementation_sha).

Two-phase inventory: compute/pin/refuse IN MEMORY → claim exclusive `R` (`O_CREAT|O_EXCL|O_NOFOLLOW`;
`TARGET_EXISTS`/`PUBLICATION_EXISTS` precedents `survey_editorial_publication_v2.py:493,1577,1617,`
`1627,2138,2221,2267,2317,3152,3387,3545`) → write COPY + inventory → basis LAST → recheck pins.
Incomplete `R` inert; retry new id; no takeover/cleanup. E inventory (live+retained-COPY): proposal,
Profile, reader, authoring, staged trio FILES, manuscript, build3, QA bundle, Gate, Candidate, seal,
reviews (original RECORD paths for U; new `R/` or external final paths for C new reviews), scope
history, State via COPY, KEEP Profile (`retained_ref=={path,sha256}`). T inventory (own-epoch blobs
ONLY): receipt closure rows vs `receipt_epoch`, staged `code_deps`+`style_input_ref` vs
`producer_head`, `capture_inputs` vs capture epoch, external toolchain via recorded
`versions/argv/env` (never Git-blobbed). KEEP rows are E, never T live; unknown/ambiguous roles refuse.
Snapshot window: entry pins → basis LAST → proof → build-record → receipt → QA/Gate/Candidate →
seal → validate → activate/resume; pins rechecked before capture, after basis, before finalize,
immediately before activate, after each write (async-build recheck
`prepare_publication:1610-1611`, finalize `2047-2054`, Freeze `_recheck_snapshot:248-256`).

Context/Freeze/active: keyword `renewal_source_proof_ref=None` (`{path,sha256}` reloaded) on
Reader/manuscript/review + Candidate/QA builders/validators (NEW files only) + `renewal_receipt_ref`
on Gate derivation; validators derive from own payload with outer-expected identity; full-set SAME
proof path+SHA; context never selects live Candidate. Nested `validate_review_record:643-647`
threads the SAME ref; `validate_candidate:775,795-800` + bundle `:781` similarly. Freeze
`_prepare_freeze_inputs:171-245` derives proof from VALIDATED Candidate, passes to direct review
loader (`:193-195`), requires bundle equality (`:196-208`); snapshot (`:213-229`) + `_preflight_freeze_pair`
(`:323-390`: `authority_raw :359-376`, `identities/spellings :377-390`) cover proof/basis/retained COPY/
current closure/all reachable evidence deduped by exact path/hash, no outside-`R` omission.
Generic Candidate/Release derive from Candidate; stage/Preview/handoff compare vs State-selected seal
(`_require_active_candidate_binding:73-100`, `resolve_publication_selection:1807`,
`require_active_or_canonical:2118`). Detached readback validates RETAINED before-State; HIGH demands
live-before equality ONLY at write boundaries.

## 7. Fixed decisions (ACCEPTED, no reopening) + honest unresolved vs exact map

ACCEPTED: 4 NEW schema files + 1 new activation branch (legacy/editorial verbatim); new receipt
kind `VERSIONED_RENEWAL_SOURCE_V1`; ONE new Gate branch `VERSIONED_RENEWAL_V1` BOTH U/C; existing
`before_active_digest` algorithm (retained before-effective7 + observed Candidate; basis/proof
additionally covered by set+record refs); Freeze derive-from-Candidate incl nested review +
transitive snapshot (§6); new basis/COPY validator in SOURCE module (`validate_renewal_basis` per
§11), history separate HIST structural (`verify_versioned_history`; NEVER move source validator
into history); free-text `reason` + fixed `reason_class`. Same naming across modules/schemas:
`renewal_source_proof_ref`, `renewal_receipt_ref`, `renewal_source`, `VERSIONED_RENEWAL_*`,
`REVIEWED_VERSIONED_CORE_RENEWAL`.

EXACT map in THIS file (simple, closed): all field/type/required/conditional/pattern lists (§§2-4),
all digest bases with exact key lists (§4), all entry signatures + error/CLI shapes + verified helper
names (§5), U/C order + inventory + threading (§6). UNRESOLVED semantics (honest, NOT closed here):
Ledger/Discovery/X/Materiality/completeness State-free bodies (sibling accepted file owns bodies;
this file owns pins/owners); old-format fingerprint bytes + successor closure name sets + controlled
bootstrap additions + control-diff classification + recipe-spec boundary + tree-mode vs physical
discipline (third agent `fingerprints-closures-consumers.*` owns values; §2.1 states required shape);
U renderer-equality runner + C trio-derivation implementation bodies (NEW code, only signatures/pins
here); Freeze snapshot exact file list beyond §6 rule (implementation must enumerate proof/basis/
retained COPY/closure/all reachable evidence deduped; no omission); QA evidence fresh-result field
list beyond `check_id/kind/status/executor/evidence/recorded_at/result` (finalize supply boundary);
per-seam error/CLI mapping beyond §5 taxonomy (operation-oracles owns oracles). Implementation stays
BLOCKED until Astra confirms THIS file + sibling accepted file + third-agent fingerprint/closure file
jointly per §§9/11.3 (unpreservable predicate → contract revision or precise NO-GO, never weakened checker).

**Disposition:** R2 is a map, NOT implementation authorization. Whole NOT_READY/step4B3 OPEN/
audit unstarted/DM021+022 OPEN. Stop at Human Commit Point; no ordinary commits; no genuine approvals.

(End — R2 supersedes R1 occurrences listed above; R1 preserved unchanged.)
