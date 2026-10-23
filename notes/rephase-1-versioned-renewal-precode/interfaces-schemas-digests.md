# Versioned renewal pre-code — interfaces / schemas / digests / call & file map (author-side)

2026-10-23 JST. Author-side General pre-code return. Human HEAD `ce0de1a`
(root observed clean `main...origin/main`).
Governing: `outputs/rephase-1-versioned-renewal-contract-decision.md` (192 lines,
SHA256 `478f00510791b76af24aa7d61f398f0608f7ad8ae7808008c660f2bea6fbfdcf`)
INCLUDING §11; mandatory `notes/rephase-1-versioned-renewal-contract/astra-review-resolution.md`;
BOTH independent reviews WITH final-binding addenda;
author inventory `notes/rephase-1-versioned-renewal-contract/accepted-authority-predicate-map.md` (F1–F8, OPEN gaps preserved).
Read-only source: `.rephase-1-editorial-runtime/final-source-packaging/proof-copy/candidate-partial-b40de60`
(actual409/tree8ce + intended57). No source edits/imports/tests/build/fixture/restore/network/Git writes.
These two files are the ONLY writes in this unit. All old docs preserved.

Scope of THIS file: concrete COMPLETE field/type/required/conditional definitions for
four new schemas + activation branch + old Candidate/QA/manuscript/Gate strict branches
and digest expressions; exact entries/signatures/error/CLI shapes; acyclic U/C phase/call map;
file/pin read-write inventory incl freshly captured COPY; source proof after current trio
derivation; build record BEFORE receipt; U no-build original manuscript context; C new proof;
caller untrusted path/ref full reload (no dict token); context propagation incl nested reviews
and Freeze `_prepare_freeze_inputs` / `_preflight_freeze_pair` snapshots; full State/candidate
active selection vs standalone inert. Accepted detailed predicates are owned by sibling
`accepted-authority-readiness.md` (this file refers to its `load_renewal_accepted_authority`
contract, does not duplicate it). Old-format supported fingerprints / successor closure sets /
control-diff classification are owned by a third agent (this file states the exact shape that
agent must deliver, does not invent fingerprints). Historical accepted State evolution obeys
decision §11.3 + both final addenda, NOT old predicate-map F3/F4 "retained-COPY equality"
wording (superseded; see §0). No implementation yet.

## 0. Binding corrections (read first)

### 0.1 Accepted State-SHA rule is §11.3, not predicate-map F3/F4

Old `accepted-authority-predicate-map.md` F3/F4 S→replacement
(`package.basis.state_sha256 == sha256(basis.retained_before_state_path)` AND
`state_path == basis.retained_before_state_rel`) is SUPERSEDED by decision §11.3
(lines 186–189) + technical addendum §67 + operator addendum §66 + sibling
`accepted-authority-readiness.md` §0. The leaf MUST NOT mutate the persisted package,
MUST NOT rewrite its `state_sha256` to the fresh retained-COPY SHA, and MUST NOT compare
the package's original `state_path` string to the fresh retained dest
(`R/retained/before/<original-State-relative-path>`). The ONLY allowed State-SHA evolution is
the already content-addressed accepted-package rule reimplemented path-based (no
`current_stage_basis_override`, no `pending_basis`, no `implementation_sha`, no monkeypatch):

1. `sha256(package file bytes) == acceptance.package_sha256`;
2. `sha256(acceptance file bytes) == basis.<family>_acceptance_sha256`;
3. same canonical SOURCE path: `package.basis.state_path` equals the canonical State path
   string derived from the accepted Profile `source_root` + config
   `state_authority.authoritative_filename` (P1 `_canonical_state_path` /
   `_validated_state_profile_for_tree`, `survey_editorial_correction_proposal_v2.py:1877–1918`;
   `survey_production_v2.py:1062–1064`), NOT a compare of original `state_path` to the fresh
   retained dest;
4. same `issue_id` + same `research_profile`/`publication_profile`;
5. valid retained before-State/COPY chain exists (fresh `R/retained/before/...` COPY pinned by
   basis `before_state_ref` + retained-COPY binding, rechecked by `validate_renewal_basis` on
   every proof readback and by high `observe_renewal_authority` at write boundaries);
6. every other predicate remains (prompt/contract/schema file-SHA, task/result exact-set,
   card/decision/coverage/digest/dirname, all content predicates in the sibling file).

Old acceptance-stage State bytes never retained are NOT demanded. Arbitrary substitution is
refused. Old acceptance provenance is history (historian); current content predicates run on
that exact accepted graph (leaf); current nonpublication selection agreement is checked OUTSIDE
the leaf by high invocation. This file assumes that rule and names owners accordingly
(LEAF = package/acceptance/basis bindings + canonical-path derivation; HIST = COPY mapping
existence/provenance; HIGH = live-before equality at write boundaries).

### 0.2 What this file does not decide

- Accepted-content predicate bodies, State-free replacements, and Ledger/Discovery/X/
  Materiality/completeness closure: sibling `accepted-authority-readiness.md` §§1–2 (F1–F8).
  This file names the leaf entry, bans, and call position only.
- Concrete old-format fingerprints (`R3 shape` bytes), old/new closure name sets, controlled
  bootstrap additions, control-diff classification, recipe-specification boundary, Git-tree-mode
  vs physical-permission discipline: third agent. This file states the exact deliverable shape
  (§12) so Astra can judge completeness.
- No numeric savings, no finish date, no Production semantic PASS, no genuine approval.

## 1. Fixed names, paths, and renewal-id rules

- `P` is the original editorial proposal namespace, unchanged (e.g. `source/.../proposal` dir
  containing `proposal.json`). `R = P/renewals/<renewal_id>`.
- `renewal_id` is a nonempty single lowercase ASCII segment matching
  `[a-z0-9][a-z0-9-]{0,63}`. Verified lexically before any IO (no `..`, `/`, `\`, empty).
  Repeated renewal stays under the same `P` with a distinct id; no recursive
  `renewals/.../renewals` and no latest-directory selection.
- `intent` is `REUSE_TARGETS` (request to attempt U) or `RENDER_TARGETS` (request C).
  Derived disposition stored in proof is `REUSED_TARGETS` or `NEW_TARGETS`. Intent never waives
  derived checks. U mismatch refuses with `REUSE_TARGET_MISMATCH`; never auto-switches an
  already claimed root into C (new `RENDER_TARGETS` attempt needs a fresh id).
- All refs are strict: `{path,sha256}` (authority) or `{path,sha256,byte_count}` (sized file)
  or `{name,path,sha256}` (named closure/accepted rows). `additionalProperties:false`,
  strict duplicate-key refusal (`survey_schema_v2.parse_json_strict_bytes` /
  `loads_strict`), lowercase 40-hex commits / 64-hex SHAs, strict instants
  (`core.parse_instant` / `core.iso_utc`), `byte_count >= 1` integers, no symlinks, no Git,
  no network, no writes in validators. Path must equal recorded path exactly; same-SHA
  different-path is refused everywhere (cf. `survey_publication_set_v2.py:765–795` precedent,
  `_check_doc_refs_against_seal:433–442` seal-map equality, `validate_candidate:778–779`
  manuscript/source divergence, Gate `1250–1251` receipt/manuscript trio binding).
- Repo-local no-follow reads only: `_lexical_rel` raw-first lexical containment BEFORE resolve
  (`survey_editorial_publication_v2.py:223–237`: absolute/backslash/dot/dotdot refused),
  `_safe` / `_safe_file` / `_read_bytes_bounded` / `_Session.safe_read` discipline, bounded
  reads, `O_NOFOLLOW`. Basis/proof/seal/activation paths are untrusted data fully reloaded on
  every use. No caller-supplied dict, verified set, `pending_basis`, `already_verified`,
  route/kind enum, `seal_path` shortcut, ambient/global context, or cache.

## 2. New module responsibilities (names fixed by decision §4)

Three selected modules, DAG bans enforced by import/call graph (pre-code must show the graph;
code begins only after Astra confirms):

1. `survey_versioned_renewal_history_v2.py`: finite old/new structural/evidence/epoch
   evaluator, safe ref readers, typed retained mapping. No agent/Reader/Gate/Candidate/
   high-operation calls. Low structural selection may call this module; it must not call
   selection back.
2. `survey_versioned_renewal_source_v2.py`: detached basis/source-proof validation,
   accepted-authority assembly, current projection/render comparison. Function-local imports
   where needed; no current State validation, seal resolution, P1/P2V/P3S/full receipt or
   Reader/Gate/Candidate calls. May read PRIOR seals/records as typed historical data, never
   the new seal/activation being constructed.
3. `survey_versioned_renewal_v2.py`: current invocation authority, exclusive capture/prepare,
   build transfer, finalize, activation/resume/CLI. Calls lower modules + ordinary content
   validators with explicit proof bindings. Current State authority is checked here, outside
   the source-proof leaf.

Existing `survey_publication_set_v2` (low seal/chain/selection), agent State/revalidation
schema, Weekly/Longform derivation, Evidence/Screening helpers, Reader/manuscript schema,
`survey_reader_surface_gate_v2`, `survey_quality_v2`, `survey_publication_v2`,
stage/agent Preview/production/profiled Freeze, orchestrator/handoff/human-gate/handlers,
export/release, P1/P2R/P2V/P3S, R1/canonical, config/docs/closures are modified ONLY per §8
table in this file. No detached helper-only completion.

## 3. Four new schemas — COMPLETE field/type/required/conditional definitions

Conventions: `S` = string `minLength:1`; `SHA` = `^[0-9a-f]{64}$`; `GITSHA` = `^[0-9a-f]{40}$`;
`INST` = `format:date-time` strict via `core.parse_instant`; `INT1` = integer `minimum:1`;
all objects `additionalProperties:false`; `schema_version` const `2.0-rc1`.
Self-digest rule: new basis/proof/receipt/seal include EVERY declared field except their one
self-digest field; file-ref SHA is the full serialized bytes, distinct from self-digest.
Old absent-field digest behavior stays unchanged; present renewal fields are included in
Candidate/bundle/manuscript/Gate digest payloads (§5).

### 3.1 `versioned-renewal-basis-v2.schema.json` — `VERSIONED_RENEWAL_BASIS_V1`

Required keys (exact, in this order for canonical bytes; order is semantic-free but the
digest base in §5 lists the same set):

- `schema_version`: const `2.0-rc1`.
- `kind`: const `VERSIONED_RENEWAL_BASIS_V1`.
- `renewal_id`: `S` matching `^[a-z0-9][a-z0-9-]{0,63}$`.
- `proposal_namespace`: `S` = `P` (repo-relative proposal dir, e.g. `.../proposal` parent of
  `proposal.json`; no trailing slash).
- `issue_id`: `S`.
- `research_profile`: enum `["WEEKLY","THEMATIC"]` (must equal Profile/basis/architecture labels).
- `publication_profile`: enum `["WEEKLY_MAGAZINE","LONGFORM_SPECIAL"]`.
- `generator_route`: enum `["WEEKLY_GENERATED_V2","LONGFORM_GENERATED_V1"]`
  (must equal Profile route; Weekly→Weekly, Thematic→Longform).
- `original_proposal_ref`: `{path,sha256}` = `P/proposal.json` (live bytes at entry).
- `retained_copy_ref`: `{path,sha256,byte_count}` where `path == R/retained/before/<original-State-relative-path>`
  (fresh COPY written during capture; see §9). `byte_count` is `len(retained bytes)`.
- `before_state_ref`: `{path,sha256}` = canonical live before-State path+SHA at entry
  (fresh, NOT old proposal `basis.state_ref`; old proposal stays history).
- `prior_selected_ref`: `{path,sha256}` = old active seal path
  (e.g. `P/publication/publication-set.json` or prior `R'/publication-set.json` for repeat).
- `prior_record_ref`: `{path,sha256}` or `null` (old activation record; `null` only when the
  prior set is a legacy `REVIEWED_CORE_CHANGE` row without a separate record file — conditional).
- `prior_candidate_ref`: `{path,sha256}` or `null` (`null` only when no canonical Candidate
  exists on disk at entry, same nullable rule as low `before_candidate_ref`
  `survey_publication_set_v2.py:1443–1462`).
- `original_validation_ref`: `{path,sha256}` = original validation checkpoint
  (`State.checkpoint_provenance.validation` at entry; must remain immutable).
- `canonical_anchor`: `{kind,ref}` where `kind` enum `["VALIDATION_CHECKPOINT","LEGACY_REVALIDATION"]`,
  `ref` `{path,sha256}` (latest legacy immediately before FIRST versioned activation is the
  permanent anchor; repeated operations never roll it forward).
- `authoring_ref`: `{path,sha256}` = NEW proposed authoring input (same authoring bytes that
  the source proof will re-derive; authoring identity is part of accepted authority).
- `accepted_refs`: array `minItems:1` of `{name,path,sha256}` — FULL accepted set pinned at
  capture (evidence-acceptance, candidate-matrix, materiality-ledger, discovery-acceptance,
  architecture, synthesis-input/result, per-package draft-package/result, archive, Profile,
  authored inputs). Sorted by `name`, no duplicate `name`. This is the pin list the leaf
  resolves; live bytes must equal these SHAs on every readback.
- `old_tool_epoch`: `{repository_commit_sha:GITSHA, contract:object, closure_digest:SHA}`
  where `closure_digest == sha256_object(sorted closure rows)` of the OLD recorded closure
  (from old receipt `current_tools` / staged `code_deps`; recorded, never re-probed at old
  commit by the operation gate — historian audit-only may use commit blobs, but the gate uses
  these recorded pins).
- `current_tool_epoch`: `{repository_commit_sha:GITSHA, contract:object, closure:[{name,path,sha256}]}`.
  `closure` is the CURRENT `_editorial_closure_rows` union-50
  (`survey_editorial_publication_v2.py:1958–1993`) + `core.contract_identity`
  (`survey_production_v2.py:210–228`); pinned from CURRENT bytes at capture via CURRENT disk
  (live+loaded+clean roots, expected membership, current contract/tool checks).
- `retention_rows`: array of closed typed rows `{roles,policy,path,sha256,byte_count,retained_dest,retained_sha256}`
  where `policy` enum `["KEEP_IMMUTABLE","COPY_BEFORE_REPLACEMENT"]`. Exactly one
  `state:authority` row with `COPY_BEFORE_REPLACEMENT`, `path/sha256 == before_state_ref`,
  `retained_dest == R/retained/before/<path>`, `retained_sha256 == retained_copy_ref.sha256`.
  All other rows are `KEEP_IMMUTABLE` live+retained-COPY recheck rows (prior seal/Candidate/
  trio/manuscript/PDF/reviews/build-record). No wildcard `scripts/**`, no caller allowlist.
- `requested`: enum `["REUSE_TARGETS","RENDER_TARGETS"]` (intent only; see §1).
- `toolchain_spec_ref`: `{path,sha256}` or `null`. `null` REQUIRED iff `requested == REUSE_TARGETS`
  (U has no toolchain arg; Python `toolchain_spec_path=None`, CLI omits `--toolchain-spec`).
  Non-null REQUIRED iff `requested == RENDER_TARGETS` (C explicit spec; executable/recipe
  evidence rechecked, never synthesized).
- `manuscript_spec_ref`: `{path,sha256}` (manuscript spec sibling outside yet-unclaimed `R`,
  pinned dependency, not writer-owned output — same discipline as
  `prepare_publication:1564–1569`).
- `executor`: `S`; `recorded_at`: `INST`.
- `basis_sha256`: `SHA` = `core.sha256_object({every key except basis_sha256})`.

Conditional summary: `prior_record_ref`/`prior_candidate_ref` nullable per disk reality;
`toolchain_spec_ref` null⟺`REUSE_TARGETS`, non-null⟺`RENDER_TARGETS`. All other keys required.
No `set_ref`, `candidate_ref`, `gate_ref`, `bundle_ref`, review-RECORD refs, activation hash,
or State-pointer value inside basis (detached; §11.1 ordering).

### 3.2 `versioned-renewal-source-proof-v2.schema.json` — `VERSIONED_RENEWAL_SOURCE_PROOF_V1`

Required keys:

- `schema_version`: const `2.0-rc1`.
- `kind`: const `VERSIONED_RENEWAL_SOURCE_PROOF_V1`.
- `basis_ref`: `{path,sha256}` = `R/renewal-basis.json` (basis bytes at proof time).
- `issue_id`, `research_profile`, `publication_profile`, `generator_route`: same enums as
  basis; must agree across proposal/basis/staged/proof.
- `reviewed_reader_ref`: `{path,sha256}` = same `P/reader-surface-input-v2.json` path+SHA
  (complete canonical reader at the existing reviewed path; content equality is the complete
  canonical reader bytes, not headline/prose equality — after pure helpers
  `build_reader_input` / `validate_reader_input` / `render_main` / `render_bibliography` /
  `validate_generated_closure` and Longform projection/archive-authorization/canonical-bytes/
  render helpers, per decision §4).
- `authoring_ref`: `{path,sha256}` (must equal basis `authoring_ref`).
- `accepted_refs`: array `minItems:1` of `{name,path,sha256}` (must equal basis `accepted_refs`
  exactly; same-SHA different-path refused).
- `supported_contract_ref`: `{path,sha256}` + `supported_epoch_refs`: `{old:GITSHA, new:GITSHA}`
  + `contract_identity`: object (old/new contract pins; steady-state requires exact current
  closure membership + schema/contract equality apart from permitted implementation/style bytes;
  bootstrap additions are the finite R3 adapter, not a wildcard).
- `dependency_closure`: array `minItems:1` of `{name,path,sha256}` (CURRENT closure at proof
  time; must equal basis `current_tool_epoch.closure` unless a genuine eligible Core commit
  landed between capture and proof — then refuse with `BASIS_CURRENT_TOOL_DRIFT` and require a
  fresh basis; no silent update).
- `output_trio_refs`: `{primary:{path,sha256,byte_count}, bibliography:{...}, style:{...}}`.
  U: OLD trio paths at original `P/staged-source/{main.tex,references.bib,jgaisurvey.sty}`-equivalent
  (exact old paths). C: NEW trio paths under `R/staged-source/{main.tex,references.bib,jgaisurvey.sty}`.
  Same SHA at a different target path is still C.
- `reader_digest`: `SHA` = `sha256(canonical_reader_bytes)` freshly rederived via the
  State-free leaf + pure projector at proof time.
- `trio_digest`: `SHA` = `sha256_object({primary:trio[0], bibliography:trio[1], style:trio[2]})`
  over CURRENT derived trio bytes at the proof paths.
- `comparison`: `{reader_equal:boolean, trio_equal:boolean, disposition:enum["REUSED_TARGETS","NEW_TARGETS"]}`.
  `disposition` is VALIDATED, never accepted as caller permission. `REUSED_TARGETS` requires
  `reader_equal && trio_equal` AND exact old targets/build-unit validation (§7); else
  `REUSE_TARGET_MISMATCH` (no auto-convert to C).
- `old_manuscript_ref` / `old_build_unit_refs`: OPTIONAL, U-ONLY.
  `old_manuscript_ref` `{path,sha256,byte_count}` (original `P/publication/reader-manuscript-v2.json`);
  `old_build_unit_refs` `{pdf:{path,sha256,byte_count,page_count}, log:{...}, digest:{...}, record:{path,sha256}}`.
  Present REQUIRED iff `disposition == REUSED_TARGETS`; absent REQUIRED iff `NEW_TARGETS`.
  No duplicate trio/manuscript/PDF/log/review copies for U (U writes no duplicate
  reader/trio/manuscript/PDF/log/reviews; build auxiliaries stay disposable).
- `executor`: `S`; `recorded_at`: `INST`.
- `proof_sha256`: `SHA` = `core.sha256_object({every key except proof_sha256})`.

No future refs: no new manuscript hash, Candidate/seal/activation ref, or own digest inside the
digested payload. Each self-digest excludes only its declared digest field. Old prior set refs
are not a cycle to the new set. Basis carries no proof ref; proof carries basis ref (one-way).

### 3.3 `versioned-renewal-source-manifest-v2.schema.json` — `VERSIONED_RENEWAL_SOURCE_V1`

Required keys (mirrors `EDITORIAL_PUBLICATION_SOURCE_V1` shape in
`editorial-publication-source-manifest-v2.schema.json:7–24`, with renewal refs):

- `schema_version`: const `2.0-rc1`; `kind`: const `VERSIONED_RENEWAL_SOURCE_V1`.
- `issue_id`, `research_profile` (`WEEKLY|THEMATIC`), `publication_profile`
  (`WEEKLY_MAGAZINE|LONGFORM_SPECIAL`), `generator_route`
  (`WEEKLY_GENERATED_V2|LONGFORM_GENERATED_V1`).
- `proposal_ref`: `{path,sha256}` = `P/proposal.json`.
- `renewal_basis_ref`: `{path,sha256}` = `R/renewal-basis.json`.
- `renewal_proof_ref`: `{path,sha256}` = `R/renewal-source-proof.json`.
- `retention_manifest_ref`, `staged_manifest_ref` (U: OLD closed manifest at original path;
  C: NEW derivation manifest under `R/staged-source/`), `scope_review_ref`
  (U: old scope path+SHA as history; C: old-as-history or new scope),
  `reviewed_reader_ref`, `authored_refs` (exact 2: `proposed-publication-authoring` +
  `accepted-draft-archive`, cf. `survey_editorial_publication_v2.py:1881–1884`),
  `accepted_refs` (FULL, `minItems:1` named rows).
- `current_tools`: `{repository_commit_sha:GITSHA, contract:object, closure:[named rows]}`
  (CURRENT pins at manifest time; must equal proof `dependency_closure` + contract).
- `outputs`: `{primary,bibliography,style}` exact trio (U: old paths; C: new `R/` paths;
  staged main→receipt primary mapping explicit, NOT primary alias, no `staged_refs`
  — cf. Gate `1231–1236`, manuscript `253–264`).
- `build_record_ref`: `{path,sha256}` = `R/build-record.json` (exactly one tagged variant, below).
- `receipt_sha256`: `SHA` = `core.sha256_object({every key except receipt_sha256})`.
  Build record exists BEFORE receipt (receipt binds build-record, so receipt cannot precede it;
  this corrects the illustrative receipt-before-build remedy — decision §11.1, technical
  addendum §64, operator addendum §§53/57).

`build-record.json` (same file, variant-tagged; NOT a separate schema file):

- Common: `schema_version:2.0-rc1`, `issue_id`, `proposal_ref`, `renewal_basis_ref`,
  `renewal_proof_ref`, `recipe_ref:{path,sha256}` (`.latexmkrc`, `REQUIRED_RECIPE_MARKERS`
  `survey_editorial_publication_v2.py:1228–1243`), `recorded_at`, `build_sha256`
  (`core.sha256_object` excluding only itself, INCLUDING input/output refs — output binding is
  essential, `survey_editorial_publication_v2.py:1648–1650` map-resolution rejection preserved).
- `variant`: enum `["REUSED_BUILD","EXECUTED_BUILD"]`, exactly one (mutually exclusive):
  - `REUSED_BUILD` (U-ONLY): `original_record_ref:{path,sha256}` + `original_pdf/log/digest_refs`
    (original `P/publication/build/{main.pdf,main.log,main.pdf.sha256}` as a unit; never substitute
    a fresh probe log into the seal's `build-log` role), `renewal_tools:{old,new}` pins,
    `no_rebuild:true`, NO `toolchain` execution evidence, NO new manuscript/PDF/build. Truthful
    `no_rebuild` claim only (no rebuild lie).
  - `EXECUTED_BUILD` (C-ONLY): `declared_inputs:{primary,bibliography,style}` (new `R/` trio),
    `recipe:{fixed_steps:[...]}` (fixed recipe under the selected existing recipe; new recipe
    specification refuses and requires a separate migration), `toolchain:{executable,versions,argv,env}`
    (absolute executable, exact argv allowlist, allowlisted env without `GIT_*/PATH/PYTHONPATH`,
    `.latexmkrc` markers — `survey_editorial_publication_v2.py:1183–1244`; live rehash,
    link→real resolve + `real_sha256` pin, companions pinned), `outputs:{publication-pdf,build-log,pdf-digest}`
    sized refs under `R/build/`, `exit_code:const 0` (cf. low `990`), real input/output/tool/exit
    evidence under the fixed recipe, failed build → no set.
- U `REUSED_BUILD` requires `toolchain_spec_ref == null` in basis and no build process spawn;
  C `EXECUTED_BUILD` requires explicit toolchain spec (never synthesized) + disposable build root
  + exclusive transfer + readback (same discipline as `prepare_publication:1609–1644`).

### 3.4 `versioned-renewal-publication-set-v2.schema.json` — `VERSIONED_RENEWAL_SET_V1`, `SEALED_INERT`

Required keys (mirrors `editorial-publication-set-v2.schema.json:7–19`, new kind):

- `schema_version`: const `2.0-rc1`; `kind`: const `VERSIONED_RENEWAL_SET_V1`;
  `status`: const `SEALED_INERT`.
- `issue_id`, `research_profile` (string, must equal basis/proof), `publication_profile`
  (`WEEKLY_MAGAZINE|LONGFORM_SPECIAL`).
- `proposal_ref`: `{path,sha256}` = `P/proposal.json` (namespace kept, not relocated).
- `renewal_basis_ref`, `renewal_proof_ref`, `source_receipt_ref` (`R/validated-source-manifest.json`),
  `build_record_ref` (`R/build-record.json`).
- `roles`: EXACT same 15 role names as editorial seal
  (`reader-input,authoring-input,source-receipt,reader-manuscript,validated-source,bibliography,style,publication-pdf,build-log,pdf-digest,quality-regression-bundle,semantic-review,visual-review,reader-surface-gate,publication-candidate`),
  each `{path,sha256,byte_count}`. U: reader/authoring/retention/scope-history/manuscript/
  trio/build3/semantic/visual RECORD roles point at ORIGINAL immutable paths; receipt/QA-bundle/
  Gate/Candidate roles point at NEW `R/` paths. C: all-renewal roles except reader/authoring/
  retention/scope-history point at NEW `R/` paths (manuscript/trio/build3/receipt/bundle/reviews/
  Gate/Candidate). No `external_reviews` duplicate map, no activation hash in seal.
  Seal path must be `R/publication-set.json` (new renewal layout, not the old fixed
  `P/publication/publication-set.json` — low `survey_publication_set_v2.py:486–487` is extended
  by the new strict branch only; old branch verbatim).
- `set_sha256`: `SHA` = `core.sha256_object({every key except set_sha256})`.

The low validator cross-binds proof/basis/receipt refs in addition to role maps (not only the
15 roles). Full set validation demands Candidate/QA/Gate/receipt/seal agree on the SAME proof;
equal-SHA different proof paths are never silently substituted.

Owned files in `R` (decision §5): `renewal-basis.json` (written after owned COPY/inventory),
`retained/before/<original-State-relative-path>`, `renewal-source-proof.json`,
`validated-source-manifest.json`, `build-record.json`, `quality-regression-bundle-v2.json`,
`reader-surface-gate-v2.json`, `publication-candidate-v2.json`, `publication-set.json`;
C additionally `staged-source/{main.tex,references.bib,jgaisurvey.sty}`,
`build/{main.pdf,main.log,main.pdf.sha256}`, `reader-manuscript-v2.json`. U writes no duplicate
reader/trio/manuscript/PDF/log/reviews. Supplied QA/review records can be external safe
repo paths; they are pinned, not writer-owned. Actual exclusive inventory includes explicitly
declared evidence files inside `R`, not arbitrary untracked files.

## 4. New strict activation branch — `VERSIONED_RENEWAL_ACTIVATION_V1`

Extends `publication-surface-revalidation.schema.json` (`oneOf` legacy + editorial, lines 6–9)
with a third strict branch preserving legacy (`97–166`) + editorial (`167–245`) verbatim.
Required keys (decision §7; low `validate_activation_record:1239–1314` extended, NOT relaxed):

- `schema_version`: const `2.0-rc1`.
- `kind`: const `VERSIONED_RENEWAL_ACTIVATION_V1`.
- `issue_id`: `S`.
- `reason_class`: const `REVIEWED_VERSIONED_CORE_RENEWAL`.
- `reason`: `S` truthful free-text Core-change reason (never false editorial; new same-reader
  basis is permitted without inventing an editorial change; using P1 changed-reader authority
  for this would be false).
- `lifecycle`: const `VALIDATED_DRAFT`.
- `prior_checkpoint` (`prior_checkpoint` in editorial branch is `original validation checkpoint`;
  here: REQUIRED original checkpoint, unchanged canonical anchor — same authority shape
  `{path,sha256}`).
- `supersedes`: `{path,sha256}` or `null` (exact authority ref to the prior revalidation/
  activation record this activation supersedes, or `null` for the first activation; common
  chain edge for all branches; mixed chain with later legacy successor fails closed —
  low `1189`).
- `canonical_anchor`: `{kind,ref}` where `kind` enum `["VALIDATION_CHECKPOINT","LEGACY_REVALIDATION"]`,
  `ref` `{path,sha256}` (permanent anchor: latest legacy immediately before FIRST versioned
  activation; repeated editorial/renewal operations never roll it forward).
- `before_state_ref`: `{path,sha256}` (fresh canonical before-State at capture).
- `retained_copy_ref`: `{path,sha256,byte_count}` (`R/retained/before/...` COPY binding;
  decision §7 "exact renewal basis ref binds the COPY and old/new epochs" — NEW vs editorial
  branch which binds via proposal/retention identity `survey_publication_set_v2.py:1317–1420`).
- `before_active_digest`: `SHA` recomputed with the existing effective7+Candidate algorithm
  (low `before_active_digest:353–415`: exactly the seven publication roles, sorted, unique
  identities/paths, `{name,path,sha256}` digest + `{path,sha256}`-or-null Candidate via
  `core.sha256_object({effective,candidate})`). Basis/proof are additionally covered by new set
  and record refs, not by effective7 alone.
- `before_candidate_ref`: `{path,sha256}` or `null` (nullable ONLY when no canonical Candidate
  exists on disk — low `1443–1462` rule preserved verbatim).
- `set_ref`: `{path,sha256}` = `R/publication-set.json` (new set, not canonical install).
- `renewal_basis_ref`: `{path,sha256}` = `R/renewal-basis.json` (binds COPY + old/new epochs).
- `renewal_proof_ref`: `{path,sha256}` = `R/renewal-source-proof.json`.
- `core`: `{contract:object, implementation_commit_sha:GITSHA}` (new core/establishment evidence).
- `executor`: `S`; `recorded_at`: `INST`.
- `establishment`: `{state_sha256:SHA, lifecycle:const VALIDATED_DRAFT, architecture_review:const approved,
  publication_preview:const pending, freeze:const pending, release:const pending,
  implementation_commit_sha:GITSHA, recorded_at:INST}` (same pre-decision sanctions as
  legacy/editorial branches, lines 144–164 / 220–244).

Chain/anchor rules preserved: legacy cumulative rows measured against the original validation
checkpoint; one mixed editorial/renewal chain, active-inclusive maximum 32, strictly increasing
sequence, nondecreasing time, no cycles; later legacy successor remains unsupported; existing
R1 and canonical writer keep pre-write refusal in versioned mode
(`survey_weekly_mechanical_refresh_v2.py:837`; `survey_agent_control_v2.py:2210–2229`).
Sole live mutation remains existing State `publication_revalidation_provenance`: exclusive new
record, known-byte State temp/replace, full new active readback.

## 5. Old strict branches — renewal proof threading (no schema-byte change without root decision)

### 5.1 Reader manuscript (`reader-manuscript-v2.schema.json:101`, `survey_reader_publication_v2.py:218–270,347–451`)

- Current `editorial_source` branch (`{proposal_ref,staged_manifest_ref}`, lines 104–112)
  preserved VERBATIM for legacy/U manuscripts. Validators: `build_manuscript_manifest:347–410`
  (`editorial_source` optional dict, exact 2 keys), `validate_manuscript_manifest:413–451`
  (digest base = 14 canonical keys + `editorial_source` when present, lines 427–447;
  `manifest_sha256 == sha256_object(base)` line 448), `_validate_manifest_semantics:218–344`
  (unconditional live `verify_staged_source:237–247` in current-P3S mode, trio main→primary
  mapping `253–269`, coverage/requirements/fidelity/gate `288–344`).
- NEW strict optional renewal branch (U-ONLY context, C uses §5.2):
  `renewal_source_proof_ref` keyword on builders/validators = exact `{path,sha256}` or `null`,
  default `None` (decision §11.2 keyword `renewal_source_proof_ref=None`, reloaded). It changes
  no old schema/bytes and has no meaning unless a fully valid proof explicitly binds that exact
  manuscript and its source. With a valid matching U proof, validators check old source-proof
  identity HISTORICALLY (typed E/T classification, live+retained-COPY E, epoch-blob T, never
  CURRENT `verify_staged_source` as historian) PLUS all current manuscript semantics and exact
  trio against the new proof (U current list in decision §11.2: schema/self-digest/issue,
  Profile, exact Architecture+typed approval, primary/source/support sizes, unique paths,
  complete Architecture coverage, Profile reader requirements, author/time, fidelity,
  surface/suppression, exact supporting trio). Without that context, standalone old editorial
  validation keeps its existing current P3S requirement and refusal. Never edit an old
  manuscript or review record to add context. Digest: old absent-field behavior unchanged;
  present `renewal_source_proof_ref` is INCLUDED in manuscript digest payload (present renewal
  fields are included — §11.2 digest rule). Concrete expression:
  `manifest_sha256 == sha256_object({14 canonical keys + editorial_source? + renewal_source_proof_ref?})`
  where each `?` is included iff present (no silent omission, no extra authority field without
  root review).

### 5.2 C manuscript branch (new mutually exclusive field)

C manuscripts carry a NEW mutually exclusive `renewal_source` ref to the source proof
(`{proposal_ref, renewal_basis_ref, staged_manifest_ref, renewal_proof_ref}`, each
`{path,sha256}`). `editorial_source` and `renewal_source` are mutually exclusive (XOR):
U manuscripts use `editorial_source` + `renewal_source_proof_ref` context; C manuscripts use
`renewal_source` (new staged proof under `R/staged-source/`), never both, never neither for
renewed sets. Old manuscripts are never edited to add `renewal_source`. Digest includes the
present branch field (same present-included rule).

### 5.3 Review records (`survey_reader_publication_v2.py:601–692`)

`validate_review_record` digest base is the 14 keys lines 617–634
(`schema_version,issue_id,research_profile,publication_profile,review_kind,status,production_profile,reader_manuscript,source,pdf,page_count,checks,reviewed_by,recorded_at`);
`review_sha256 == sha256_object(base)` line 636. Review schema/bytes need NOT change:
validators receive a reloaded exact proof ref from their containing Candidate/prepare invocation
(`renewal_source_proof_ref` passed through). Nested manuscript validation inside
`validate_review_record:643–647` propagates the SAME proof context (contains the exact
`{path,sha256}`, reloaded, never ambient). Reviews retain kind/status/check-family/depth, exact
manuscript/source/PDF/page-count and digest checks, with the same proof context for nested
manuscript validation (decision §11.2). Historical same-reader scope is reloaded and exact old
before/after scope relationships checked; never fresh P2V `SCOPE_BOUND`, never Core-change
approval. Changed review/check requirements are migration triggers, not U reuse exceptions.
Digest: present `renewal_source_proof_ref` in the CONTAINING Candidate/bundle/Gate (not in the
review file itself) covers the binding; review file bytes stay byte-identical for U reuse
(old RECORD files at original immutable paths, TARGET refs still matching).

### 5.4 Quality bundle (`quality-regression-bundle-v2.schema.json`, `survey_quality_v2.py:193–274`)

`build_bundle:193–229` digest `bundle_sha256 == sha256_object(basis)` line 224 where `basis`
is 9 keys (`schema_version,issue_id,production_profile,research_profile,publication_profile,source,pdf,checks,status`);
`validate_bundle:232–274` recomputes the same 9-key base lines 259–263. `validate_checks:132–174`
validates SUPPLIED rows only (exact fields, applicable-family completeness, all `PASS`,
executor/evidence/recorded_at/result refs) and never executes tests — decision §§5–6 rule
preserved. NEW strict optional renewal branch: builders/validators accept the same
`renewal_source_proof_ref=None` keyword, serialize it in the new strict optional branch, and
include it in the digest base when present:
`bundle_sha256 == sha256_object({9 canonical keys + renewal_source_proof_ref?})`.
Validators derive it from their own payload; if an outer expected ref exists it must be
identical (decision §11.2). Supplied QA inputs come from fresh actual checks with exact
evidence refs; `quality.validate_checks` validates supplied results only. Which QA evidence
fields prove actual fresh results (executor + evidence path/SHA + recorded_at + result ref +
applicable `check_id`/kind) is pinned by the supply boundary (§9); no invented execution
metadata.

### 5.5 Reader-surface Gate (`reader-surface-gate-v2.schema.json`, `survey_reader_surface_gate_v2.py:1145–1330,1640–1769`)

Current `derivation` oneOf has 4 variants (lines 160–217): `DIRECT_PRIMARY`, `WEEKLY_GENERATED_V2`,
`LONGFORM_GENERATED_V1`, `EDITORIAL_PUBLICATION_V1` (each with `route/scope/receipt` where
applicable). `_derivation_for_manuscript:1145–1330` implements the 4-way dispatch:
editorial branch `1159–1253` (live `verify_staged_source:1173`, receipt at
`P/publication/validated-source-manifest.json:1182–1185`, early scope reload `1195–1224`,
trio main→primary mapping `1225–1251`), direct/generated branches `1254–1330`.
Gate builder `evaluate_reader_surface_gate:1333–1694` digest
`gate_sha256 == sha256_object(base)` line 1685 where `base` is 13 keys lines 1650–1681
(`schema_version,issue_id,publication_profile,status,scanned_surfaces,rules_checked,suppressions,findings,summary,evaluated_by,recorded_at,derivation,semantic_authority`);
validator `_inspect_gate_record` + `validate_reader_surface_gate:1893–...` recomputes the same
13-key base lines 1737–1753. NEW: Gate derivation additionally takes `renewal_receipt_ref`
(exact `{path,sha256}`, reloaded). Serialized Gate `derivation` binds BOTH proof and receipt
refs for renewed sets (decision §11.2: "Gate derivation additionally takes `renewal_receipt_ref`;
serialized Gate binds both"). Concrete: renewed `derivation` object = existing variant fields
PLUS `renewal_source_proof_ref:{path,sha256}` PLUS `renewal_receipt_ref:{path,sha256}`
(augmenting `EDITORIAL_PUBLICATION_V1`-shaped derivation for U, or the new renewal route
variant for C — see §13 choice C1). Digest includes both present renewal refs:
`gate_sha256 == sha256_object({13 canonical keys incl. augmented derivation})`.
Full set validates equality among these fields and the seal's top-level proof/receipt refs.
The context never selects a live Candidate; State-selected ref equality stays mandatory at
normal admission. New full-set validation demands Candidate/QA/Gate/receipt/seal agree on the
SAME proof; equal-SHA different-path is refused.

### 5.6 Publication Candidate (`publication-candidate-v2.schema.json`, `survey_publication_v2.py:668–814`)

`build_candidate:668–746` digest `candidate_sha256 == sha256_object(base)` line 743 where `base`
is 9 keys lines 730–741 (`schema_version,issue_id,publication_profile,status,reader_manuscript,source,pdf,quality_bundle,semantic_review,visual_review`);
`pdf` includes `page_count` line 737. `validate_candidate:749–814` recomputes the 10-key digest
base lines 753–766 (same 9 + `candidate_sha256` excluded). Cross-bindings lines 769–811 enforce
manuscript/source/bundle/PDF/review equality (manuscript `primary_source == source` line 778,
bundle source/PDF equality `784–788`, review manuscript/source/PDF/size/page drift `801–811`,
PDF drift `792–793`). NEW strict optional renewal branch: same `renewal_source_proof_ref`
keyword on builders/validators, serialized in the new strict optional branch, included in digest
when present:
`candidate_sha256 == sha256_object({9 canonical keys + renewal_source_proof_ref?})`.
Validators derive it from their own payload; outer expected ref must be identical when present.
No fallback to canonical Candidate; producer AND loader recompute selected paths and compare
hashes (decision §8).

Digest-rule summary (decision §11.2): old absent-field behavior unchanged; present renewal
fields are included in Candidate/bundle/manuscript/Gate payloads; new basis/proof/receipt/seal
include EVERY declared field except their one self-digest field; file-ref SHA is the full
serialized bytes, distinct from self-digest; seal and activation bind basis/proof/COPY through
exact refs, not just effective7. Pre-code (this file) shows each concrete expression; code must
implement exactly these.

## 6. Exact entries, signatures, error and CLI shapes

All paths are repo-local no-follow `str|Path` (lexical first, `_lexical_rel` discipline);
all refs are untrusted data fully reloaded (strict JSON duplicate-key refusal + new
basis/proof/receipt/seal schema validation + `basis_sha256`/`proof_sha256`/etc. canonical
recompute). No caller dict token. Python API uses `datetime|None` for `recorded_at`
(`core.iso_utc` / `core.parse_instant`); CLI passes `--recorded-at` ISO strings.

```text
# private entry (high, before capture; no basis yet; in-memory pins for drift detection only)
_observe_renewal_entry(root: Path|str, state_path: Path|str)
  -> {state, state_sha, prior_history:{seal,receipt,staged,retention,scope_refs,epochs},
      current_nonpublication_authority, current_tool_predicates, pins:{...}}
  # owns: exact canonical State reload, prior history, current nonpublication authority/tool
  # predicates. No public verified-object parameter. Pins used ONLY to detect drift while
  # claiming/writing COPY. Errors: BASIS_ENTRY_INELIGIBLE, HISTORY_* (see §6.1).

# high capture (owns NEW COPY + inventory; writes basis LAST, then rechecks entry pins)
prepare_renewal(root, state_path, renewal_id, intent, manuscript_spec_path,
                toolchain_spec_path|None, executor, recorded_at)
  -> {renewal_dir:R, basis_path:R/renewal-basis.json, retained_copy:R/retained/before/...,
      pins:{...}}
  # U: toolchain_spec_path MUST be None (Python) / CLI omits --toolchain-spec; no build runs.
  # C: toolchain_spec_path REQUIRED (explicit spec; executable/recipe rechecked, never synthesized).
  # intent ∈ {REUSE_TARGETS, RENDER_TARGETS}; no power to waive derived checks.

# source leaf (detached; no State object, no implementation_sha, no verified-records param)
load_renewal_accepted_authority(root: Path, basis_path: Path)
  -> {surface, records, accepted_refs, authored_refs}
  # called by source proof via persisted path. Full contract + bans in sibling file §§1–2.
  # May read PRIOR seals/records as typed historical data, never the new seal/activation.

# source proof (detached; validates RETAINED before-State, never live-before equality)
validate_renewal_basis(root, basis_path) -> {basis, retained:{...}, unchanged_evidence:{...}}
verify_renewal_history(root, record_path)
  -> {HISTORICAL_IDENTITY_VERIFIED, observed_refs:{...}}  # record-only, no State arg
  # reloads record, schema/kind, canonical anchor/supersedes chain, exact set/receipt/
  # staged-or-renewal-proof/basis/retention refs + original scope evidence. Epochs from those
  # records, not a caller commit/verified map. Owns typed E/T classification, COPY mapping/
  # inventory, old self-/cross-digests. Returns descriptive VERIFIED + observed refs, never a
  # consumable permit. MUST NOT call current low validate_seal/selection, P2R/P3S, high receipt,
  # P2V, agent/Reader/Gate/Candidate (decision §11.1 forbidden-callee parallel to §4 leaf bans).

# high observation (basis-bound; after basis write, before finalize, immediately before activate)
observe_renewal_authority(root, state_path, basis_path)
  -> {live_current_before, retained_before, selected_predecessor, current_tools, pins:{...}}
  # reopens and compares ALL inputs. Demands current live State == fresh before ref.
  # Distinct from _observe_renewal_entry (before capture) and validate_renewal_basis (detached
  # retained-COPY + unchanged-evidence checks on every proof readback). Roles do not transfer
  # authority through returned dicts.

# high finalize (build transfer already done for C; QA/Gate/Candidate/seal; seal LAST)
finalize_renewal(root, state_path, basis_path, checks_path,
                 semantic_review_path|None, visual_review_path|None, executor, recorded_at)
  -> {set_path:R/publication-set.json, seal:{...}, pins:{...}}
  # NULL new-review args ONLY for validated U (old review RECORD refs derived from predecessor;
  # a replacement review at a different path is never silently treated as reused).
  # C requires new postrender semantic+visual reviews at exact new targets + actual QA inputs.
  # Supplied QA/review files are read-only inputs (finalize reloads schemas/results/targets,
  # computes an exact dependency manifest path/hash/size/type incl. files inside R, excludes
  # unlisted files, pins directory inventories, rechecks before/after writes). Externally produced
  # files are never deleted/rewritten; writer-owned paths cannot alias supplied paths.

# low/high validators (no permission token)
validate_renewal_receipt(root, receipt_path) -> receipt  # strict State + closure + proof + scope + replay
validate_prepared_renewal_set(root, state_path, set_path) -> validated_set
activate_renewal(root, state_path, set_path, reason, executor, recorded_at) -> result
  # reason MUST be REVIEWED_VERSIONED_CORE_RENEWAL for the renewal kind (see §4).
resume_renewal_activation(root, state_path, record_path) -> result
  # reloads record+set+basis and compares the COMPLETE branch/issue/original-checkpoint/anchor/
  # supersedes/before-State/digest/Candidate/set/basis/new-core/executor/reason/time intent,
  # not set SHA alone (see operation-oracles.md for the full equality list).
verify_renewal_history(root, record_path) -> historical_result  # high wrapper delegating to the
  # typed history leaf above; historical structural loading of a renewal proof does NOT execute
  # its current-replay branch.
```

Renderer-equality runner (U narrow condition, NEW — no current API exists):

```text
verify_renewal_rerender_equality(root, basis_path, proof_path)
  -> {reader_equal:bool, trio_equal:bool, disposition}
  # current renderer/style → disposable temp trio + complete canonical reader comparison vs OLD
  # trio bytes at ORIGINAL paths + reviewed_reader_input bytes. Temp is disposable outside the
  # publication inventory (never P/publication/ or R/). Mismatch → REUSE_TARGET_MISMATCH (refuse
  # pre-write, exit 2), never auto-convert to C. Same-trio/different-PDF (incl. metadata-only
  # CreationDate/Producer/ID or page_count delta) is C, not U. Source-only/comment-only TeX
  # changes that alter trio bytes are C. Any canonical reader byte delta is neither (editorial path).
```

C staged-derivation wiring (NEW — no current API exists):

```text
derive_renewal_staged(root, basis_path)
  -> {staged_dir:R/staged-source/, manifest:R/staged-source/staged-source-manifest.json, trio:{...}}
  # new staged derivation under R/ (old closed4 untouched; new manifest own scope_review_ref).
  # Manuscript (C renewal_source branch) + real disposable build/transfer are independently
  # preparable AFTER proof, both BEFORE external review (decision §11.1). Receipt binds
  # build-record, so receipt cannot precede that record.
```

### 6.1 Error categories (structured `phase/code/disposition`, primary+secondary, observed State status)

Existing carriers: `EditorialError(code,phase,disposition,detail)` with `.code/.phase/.disposition/.detail`
(`survey_editorial_publication_v2.py:181–191`); low `PublicationSetError(<message>)` with
`CHAIN_LIMIT=32` (`survey_publication_set_v2.py:109`), `before_active_digest` typed errors
(`353–415`), chain/anchor typed errors (`1060–1230`), activation typed errors (`1239–1314`).
New codes (decision §11.1; per-seam mapping in operation-oracles.md):

- `HISTORY_*`: `HISTORICAL_IDENTITY_VERIFIED` (success, descriptive only) vs
  `HISTORY_COMMIT_MISSING` / `HISTORY_BLOB_MISSING` / `HISTORY_SCHEMA_MISSING` /
  `HISTORY_DIGEST_MISMATCH` / `HISTORY_ANCESTOR` / `HISTORY_MODE` / `HISTORY_TOOL_EPOCH_DRIFT`
  / `HISTORY_PACKAGE_MUTATED` (refusals, never waived; partialDB-26309 missing → `HISTORY_BLOB_MISSING`).
- `BASIS_*`: `BASIS_ENTRY_INELIGIBLE` / `BASIS_LIVE_STATE_INVALID` / `BASIS_ACCEPTED_REF_MISSING` /
  `BASIS_ACCEPTED_SHA_DRIFT` / `BASIS_ACCEPTED_PATH_MISMATCH` / `BASIS_CURRENT_TOOL_DRIFT` /
  `BASIS_STATE_PATH_IDENTITY` / `BASIS_ACCEPTANCE_BINDING_DRIFT` / `BASIS_ISSUE_PROFILE_DIVERGENCE` /
  `RETAINED_COPY_MISSING` / `BASIS_STATE_PATH_IDENTITY`.
- `RENEWAL_PROOF_*`: proof/content/binding refusals (sibling file failure column; e.g.
  `RENEWAL_PROOF_EVIDENCE_CARD_DRIFT`, `RENEWAL_PROOF_X_MANIFEST`, `RENEWAL_PROOF_LEDGER`,
  `RENEWAL_PROOF_COMPLETENESS`, `RENEWAL_PROOF_PROFILE_MISMATCH`, `RENEWAL_PROOF_TOKEN_URL`, ...).
- `REUSE_TARGET_MISMATCH` (U renderer/trio/manuscript/PDF/build3 mismatch; refuse, never convert).
- `UNSUPPORTED_MIGRATION` (research/Profile/Architecture/Draft/pipeline-quality contract/review-requirements/
  route/recipe-spec change; contract/closure/schema/route/toolchain-rule B-trigger).
- `REVIEW_TARGET_MISMATCH` (wrong issue/manuscript/source/PDF/proof path/hash/basis; C missing/stale
  postrender review; no fresh QA; mismatched proof in Candidate/QA/Gate/receipt/seal; inert rival).
- `RECORD_COLLISION` (complete inert seal, no record → explicit activate with full revalidation).
- `INTENT_COLLISION` / `INTENT_MISMATCH` (ordinary activate refuses when the exact operation intent
  already exists at the record path — `survey_editorial_publication_v2.py:3152` precedent; explicit
  resume reloads the full intent, never auto-adopts).
- `INDETERMINATE` (State neither before nor expected after, unsafe/unreadable; preserve, no
  rollback/overwrite/adoption, no deletion of referenced or possibly-referenced records).
- `ALREADY_ACTIVE` (readonly: State exactly expected after; full strict active readback, no
  regenerated approval).

Dispositions: `REFUSED_PRE_WRITE` (before any write), `PRESERVED_INCOMPLETE` (incomplete R stays
inert; retry uses a new id; no same-byte takeover or foreign/unknown cleanup),
`REFUSED_POST_WRITE_RECHECK` (pin recheck after work fails), `INSTALLED` (sole State-pointer
mutation), `ALREADY_ACTIVE` (readonly), `INDETERMINATE` (preserve all bytes).
CLI success `0`, refusal-or-operation-failure `2` (existing `main():3914–3917` prints to stderr,
returns `2`; unexpected failures must be nonzero, never converted to PASS).

### 6.2 CLI shapes (new high module; ordinary agent validate-state + consumers recognize the new branch)

```text
survey_versioned_renewal_v2.py [--repo-root .] [--config config/survey-production-v2.json]
  prepare   --state <State> --renewal-id <id> --intent REUSE_TARGETS|RENDER_TARGETS
            --manuscript-spec <spec> [--toolchain-spec <spec>] [--executor <name>] [--recorded-at <instant>]
            # U: --toolchain-spec OMITTED (absent, not empty string). C: REQUIRED.
  finalize  --state <State> --basis <R/renewal-basis.json> --checks <deterministic-checks.json>
            [--semantic-review <path>] [--visual-review <path>] [--executor <name>] [--recorded-at <instant>]
            # NULL review args ONLY for validated U (derive predecessor RECORD refs); C requires both.
  validate-receipt --receipt <R/validated-source-manifest.json> [--state <State>]
  validate-set     --state <State> --set <R/publication-set.json>
  activate  --state <State> --set <R/publication-set.json> --reason <free-text Core-change reason>
            --executor <name> [--recorded-at <instant>]
            # --reason allowlist accepts ONLY REVIEWED_VERSIONED_CORE_RENEWAL for this kind
            # (never editorial/core values); reason_class is fixed by kind branch.
  resume    --state <State> --record <activation-record.json>
  history   --record <activation-record.json>   # record-only, no --state
```

Exits: `0` success; `2` refusal-or-operation-failure (all typed `EditorialError`/`PublicationSetError`
mapped to `2` with structured `phase/code/disposition` + primary/secondary + observed State status
on stderr); unexpected failures nonzero, never `0`. Ordinary agent `validate-state` and all §8
consumers explicitly recognize `VERSIONED_RENEWAL_ACTIVATION_V1` / `REVIEWED_VERSIONED_CORE_RENEWAL`
(no fallback to canonical Candidate, no generic pending bypass).

## 7. Acyclic U/C phase/call map (preseal DAG; lifecycle-dependent calls shown)

```
prior history + fresh before-State/selection + unchanged accepted inputs
  → _observe_renewal_entry (HIGH, before capture; in-memory pins, no basis yet)
  → exclusive COPY claim + inventory + basis LAST + pin recheck
  → observe_renewal_authority (HIGH, basis-bound; after basis, before finalize, immediately before activate)
  → load_renewal_accepted_authority (SOURCE LEAF, by persisted basis_path; pure content predicates)
  → current projection/render comparison (pure helpers AFTER all authority checks)
  → source proof (SOURCE; U-only old manuscript/build-unit refs OR C new trio refs)
  → C staged derivation (C ONLY; R/staged-source/; old closed4 untouched)
  → C manuscript (renewal_source branch) + real disposable build/transfer (C ONLY; independently
       preparable AFTER proof, BOTH BEFORE external review; build auxiliaries disposable)
  → build record (C EXECUTED_BUILD with real evidence; U REUSED_BUILD wrapper with original
       record/PDF/log/digest refs + renewal_tools{old,new} + no_rebuild; receipt binds build-record)
  → renewal receipt (validated-source-manifest; binds proof+build+retained COPY)
  → externally supplied fresh QA inputs + new QA bundle (quality.validate_checks validates SUPPLIED
       rows only; never executes tests) + new postrender reviews (C ONLY; U derives predecessor RECORD refs)
  → new Gate (proof+receipt-bound derivation; no inferred old P/publication/ receipt path)
  → new Candidate (nested manuscript/reviews/bundle bindings; renewal_source_proof_ref branch)
  → seal (R/publication-set.json; 15 roles; proof/basis/receipt refs; 15-role cross-binds; seal LAST)
  → validate_prepared_renewal_set (strict State + closure/replay + manuscript/bundle/reviews/Gate/Candidate/build/PDF/log/digest/current-research + cross-refs + closed inventory)
  → explicit activate (full current-before + full leaf revalidation; exclusive new record;
       known-byte State temp/replace on publication_revalidation_provenance ONLY)
  → full new active readback (current-before vs retained-before + selected Candidate/digest must agree)
  → normal active Candidate → direct stage → synthetic Preview/Freeze/Release (synthetic approvals
       labelled; production semantic NO-GO on placeholder editions)
```

Bans (decision §§4/11.1): history leaf MUST NOT call current low `validate_seal`/selection,
P2R/P3S, high receipt, P2V, agent/Reader/Gate/Candidate. Source-proof leaf MUST NOT call current
State validation, seal resolution, P1/P2V/P3S/full receipt, Reader/Gate/Candidate; function-local
imports only; may read PRIOR seals/records as typed historical data, never the new seal/activation.
Low structural selection may call the history module; it must not call selection back. Low resolver
hashes and cross-binds only; it must not call full Reader/Gate/source-proof semantics and recurse
into State (no State→Candidate→Reader→proof recursion). No monkeypatch, caller `already_verified`
records, arbitrary implementation-SHA substitution, or broad `pending` allowance.

Lifecycle-dependent calls (must appear in the implementation call graph, not as unconditional edges):

- `_verify_head_bytes` (`survey_weekly_derivation_v2.py:591–645`) / `Longform.verify_tool_basis` +
  `core.contract_identity` (`survey_production_v2.py:210–228`) + receipt `current_tools` closure
  (`survey_editorial_publication_v2.py:1091–1118`) + `cat-file -e` / `merge-base --is-ancestor` +
  filtered-canonical + extra-closure (`1134–1176`): HIGH + historian (current eligibility vs epoch
  blobs), never leaf.
- P1 `_active_effective` / `_versioned_active_selection` / retention-plan KEEP/COPY shapes are
  templates for the renewal basis, never called as renewal entries (P1 `validate_proposal` never
  called for renewal; P1 stays identical-reader-refusing).
- `verify_staged_source` (`survey_editorial_staged_source_v2.py:1772–2169`) is called ONLY in
  current-eligibility paths (prepare/finalize Gate/manuscript), NEVER as the historian (history uses
  typed E/T classification + COPY mapping/inventory + old self-/cross-digests via
  `verify_versioned_history`).
- `observe_current_authority` (P2V) is never called for renewal after activation except true repeat;
  renewal uses `observe_renewal_authority` / `_observe_renewal_entry` + `validate_renewal_basis`.

U sequence (decision §11.1): entry → exclusive COPY/basis → in-memory reader/trio comparison
(`verify_renewal_rerender_equality`) + exact old targets/build-unit validation → proof →
reused-build wrapper/receipt → externally supplied fresh QA inputs → new QA/Gate/Candidate →
seal → explicit activate. No new manuscript/PDF/build executable. `toolchain_spec_path=None`
(Python); CLI omits the option. Supplied semantic/visual args are either absent (derive predecessor
records) or exact predecessor refs; a replacement review at a different path is never silently
treated as reused.

C sequence (decision §11.1): entry → COPY/basis → derived trio at new `R/` paths → proof →
C manuscript + real disposable build/transfer (independently after proof, both before external
review) → executed-build record → receipt → new external postrender reviews + actual QA inputs →
QA/Gate/Candidate → seal → explicit activate. Manuscript and build can be prepared independently
after proof; both exist before external review. Receipt binds build-record, so receipt cannot
precede that record. C uses source proof, not an extra old-format P3S staged manifest.

## 8. File/pin read-write inventory incl freshly captured COPY (two-phase)

Two-phase snapshot capture (decision §5): compute/pin/refuse IN MEMORY → claim exclusive `R` →
write COPY → basis LAST → recheck ALL entry pins. Incomplete `R` remains inert; retry uses a new
id. No same-byte takeover or cleanup of foreign/unknown residue. Existing P2R retained roots and
original P3S closed4 are unchanged.

| Phase | Reads (pinned, rechecked before/after writes) | Writes (exclusive, no takeover) | Forbidden |
|---|---|---|---|
| Entry (`_observe_renewal_entry`) | canonical State + `profile_ref` + checkpoint provenance + prior seal/receipt/staged/retention/scope refs + current nonpublication authority + current closure/contract/HEAD + Profile-bound canonical Freeze/Manifest conventions | NONE (in-memory pins only) | No basis read (not yet existent); no verified-object out-param; no State mutation |
| Capture (`prepare_renewal`) | entry pins + original proposal/retention/staged/Candidate/manuscript/trio/PDF/build3/review RECORD bytes at RECORDED paths (live+retained-COPY E) + old tool-epoch pins (recorded, not re-probed) + manuscript/toolchain specs (pinned deps, outside unclaimed `R`) + Profile/config for route labels | exclusive `R/` dir + `R/retained/before/<original-State-relative-path>` COPY (fresh second generation; `_expected_retained_dest` renewal-dir variant; `retained_dest == R/retained/before/<path>`, `sha256 == row.sha256`, `len == byte_count`) + owned inventory + `R/renewal-basis.json` LAST | No `P/publication/` overwrite; no canonical Candidate install; no second pointer; no latest-scan; no Profile/role rebind; no old-file mutation; writer-owned paths cannot alias supplied paths |
| Proof (`validate_renewal_basis` + leaf + rerender/staged) | basis (reloaded) + ALL basis-pinned `{path,sha256[,byte_count]}` refs (live SHA recheck + size where sized) + prior seals/records as typed history + CURRENT derived trio/reader via pure helpers AFTER authority checks + style file for `validate_generated_closure` | `R/renewal-source-proof.json` (after trio derivation for C; after in-memory comparison for U) + C `R/staged-source/{main.tex,references.bib,jgaisurvey.sty,staged-source-manifest.json}` (C only) | No new seal/activation read (not yet existent); no State load in leaf; no HEAD/commit/Git; no network; no publisher |
| Build transfer (C only) | staged trio + toolchain spec + fixed recipe (`.latexmkrc` markers) + executable evidence | disposable build root (outside inventory) → exclusive `R/build/{main.pdf,main.log,main.pdf.sha256}` transfer + readback + `R/build-record.json` (EXECUTED_BUILD) | Failed build → no set; no fresh probe log substituted into U seal; no rebuild lie |
| Finalize | State + basis + proof + staged + manuscript + build-record + supplied checks/reviews (schemas/results/targets reloaded; exact dependency manifest `path/hash/size/type` incl. files inside `R`; unlisted files excluded; directory inventories pinned) + receipt + QA bundle + Gate + Candidate | `R/validated-source-manifest.json` (AFTER build-record) → `R/quality-regression-bundle-v2.json` → `R/reader-surface-gate-v2.json` → `R/publication-candidate-v2.json` → `R/publication-set.json` LAST | Supplied files never deleted/rewritten; no claiming an already-existing foreign `R`; no same-byte takeover; incomplete `R` stays inert |
| Activate/resume | State + record + set + basis + seal + retained COPY + before-effective7 + Candidate (full revalidation; `before_active_digest` recomputed, never accepted as caller value) | exclusive new activation record on the canonical chain + known-byte State temp/replace on `publication_revalidation_provenance` ONLY | No root deletion; no automatic stale adoption; no retrospective PASS; no deletion of referenced/possibly-referenced records |

Fresh COPY layout (second generation): `R/retained/before/<original-State-relative-path>`
(e.g. `R/retained/before/publication/v2/...` mirrors the original relative path). `expected_dir`
derivation from renewal Profile `paths.source_root` (same discipline as P2R `1908–1912`);
`observed_dir == expected_dir`, manifest path canonical, full retained inventory exact
(`_retained_expected_sets` discipline `survey_editorial_retention_v2.py:835–854`: every COPY dest
+ manifest; retained root + every ancestor dir below it; late new file/empty dir refuses).
KEEP evidence rows (Profile, reader, authoring where KEEP) rehashed live (`repinned` semantics).
Old KEEP rows stay live-rechecked. Full P2R semantics stay high-side; current `verify_retention`
is NOT called as historian after a Core change.

Snapshot window (Freeze boundary, §10): `_prepare_freeze_inputs` captures a bounded byte snapshot
of every authority input for install-boundary rechecks (`survey_publication_v2.py:213–229`:
Candidate + approval + visual + bundle + Profile + manuscript + source + PDF + semantic review
→ `{rel:sha256}`); `_recheck_snapshot:248–256` fails when any snapshotted byte changed since
preparation; `_preflight_freeze_pair:323–...` performs the complete pre-install gate (both schemas,
target/parent conflicts incl. nested outputs and target/input aliasing, equal-payload bytes,
Freeze SHA over the bytes that will be ensured). Renewal extends the snapshot/alias set (§10);
the window is preparation→install (any drift inside refuses; repair is a fresh id, never an
in-place overwrite).

## 9. Source proof after trio derivation; build record BEFORE receipt; U no-build; C new proof

- Source proof is C's staged proof; never forge an old P3S manifest at an unsupported renewal path.
  For C, the NEW trio/manifest under `R/staged-source/` exists BEFORE proof validation (proof
  references sized trio refs + comparison digests, so the staged derivation precedes it), while
  the PDF build/record follows proof (manuscript + build independently preparable AFTER proof,
  both BEFORE external review — decision §11.1). Acyclicity holds: proof precedes only artifacts
  that reference it; nothing proof references is created after it (U old refs are prior; C trio
  precedes proof; manuscript/build/receipt follow).
- Build record exists BEFORE receipt in BOTH cases (receipt binds build-record). U reused-build
  wrapper (`REUSED_BUILD` with original record/PDF/log/digest refs) precedes the reused-build
  receipt; C executed-build record (real inputs/outputs/tool/exit evidence under the fixed recipe)
  precedes the new receipt. This is the corrected order (technical addendum §64, operator
  addendum §§53/57); the illustrative receipt-before-build remedy is superseded.
- U no-build: `toolchain_spec_path=None` (Python) / CLI omits `--toolchain-spec`; NO new
  manuscript/PDF/build executable; NO disposable build spawn; NO staged trio/manuscript/PDF/log
  copies to renewal paths (same-SHA different-path refused). New files under `R/` are ONLY
  basis/proof/receipt/QA-bundle/Gate/Candidate/seal/activation (no trio/build/manuscript
  duplicates). Old semantic/visual RECORDs reused at SAME original RECORD paths+SHAs because
  their TARGET refs still match; U creates NO new semantic/visual RECORDs. Log nuance: reuse old
  `build/main.log`+digest as a unit with old PDF; never substitute a fresh probe log into the
  seal's `build-log` role (provenance lie).
- C new proof: new staged derivation + real disposable-root build with explicitly selected
  executable + fixed recipe + exclusive transfer + readback + new manuscript
  (`renewal_source` branch) + new receipt + RE-EXECUTED deterministic checks + new QA bundle +
  new Gate (new scope-history + new trio/manuscript) + new Candidate (new bundle/Gate pins) +
  new seal LAST. Ordinary external postrender semantic + visual review is MANDATORY against NEW
  manuscript + NEW PDF at new paths+SHAs (early scope may be reused ONLY as HISTORICAL input iff
  reader-identical + current-contract-valid + recognised as history, never as approval of the new
  Core change and never waiving postrender).

## 10. Context propagation incl nested reviews + Freeze snapshots + active vs inert

- Keyword (decision §11.2): `renewal_source_proof_ref=None` (exact `{path,sha256}`, reloaded)
  on Reader manuscript/review builders + validators, Candidate/QA builders + validators.
  Gate derivation additionally takes `renewal_receipt_ref` (exact `{path,sha256}`, reloaded).
  Serialized Gate derivation binds both; full-set validates equality among these fields and the
  seal's top-level proof/receipt refs. It changes no old schema/bytes and has no meaning unless
  a fully valid proof explicitly binds that exact manuscript and its source. C manuscript schema
  branch carries its matching proof ref. Candidate/QA builders serialize the keyword in their new
  strict optional renewal branch; validators derive it from their own payload (outer expected ref
  must be identical when present). The context never selects a live Candidate; State-selected ref
  equality stays mandatory at normal admission. No ambient/global context or cached authority.
- Nested reviews: `validate_review_record:643–647` calls `validate_manuscript_manifest` internally;
  the renewal implementation MUST thread the SAME reloaded proof ref into that nested call
  (explicit parameter, not ambient). `validate_candidate:775` (manuscript), `795–800` (reviews),
  `781` (bundle) similarly propagate the containing Candidate's proof ref to each direct review/
  bundle/manuscript loader and require bundle equality where applicable. Equal-SHA different-path
  is refused at every hop (manuscript/source/PDF/size/page bindings `668–669,723–728,801–811`).
- Freeze `_prepare_freeze_inputs(repo_root, candidate_path, approval_path)`
  (`survey_publication_v2.py:171–245`): renewal derives proof from its VALIDATED Candidate
  (State-selected set → Candidate → `renewal_source_proof_ref` field, reloaded and fully
  validated), passes it to its DIRECT review loader (`reader.validate_review_record` for the
  pre-preview VISUAL, line 193–195), and requires bundle equality (Candidate/bundle/manuscript/
  source/PDF bindings `196–208`). Snapshot (`213–229`) and `_preflight_freeze_pair` authority/
  overlap checks (`323–...`: `authority_raw` lines 359–376 = manuscript/source/pdf/bundle/reviews
  + Candidate/approval/visual/bundle/Profile paths; `identities`/`spellings` lines 377–390;
  target-overlap refusal `387–...`) cover proof, basis, retained COPY, current tool closure, and
  ALL reachable evidence used by the contextual validators, deduplicated by exact path/hash, with
  no omission because a dependency is outside the new `R`. Generic Candidate/Release validators
  derive from Candidate; stage/Preview/handoff additionally compare against the State-selected
  seal. Low projection returns proof/basis refs STRUCTURALLY (hash + cross-bind only), never runs
  source semantic replay (no State recursion). Standalone old reviews without proof can still
  refuse after a Core change; that is not a hidden global waiver.
- Active vs inert: a self-validating inert Candidate is NOT live selection. Preseal calls may
  provide explicit UNTRUSTED proof refs and MUST reload them. Normal active consumers derive proof
  from the State-selected set (`resolve_publication_selection:1807–...`,
  `require_active_or_canonical:2118–...`, `_require_active_candidate_binding:73–100`) and demand
  equality with Candidate/QA/Gate bindings. Stage `_require_active_candidate_binding:73–100`
  recomputes active refs via the frozen low resolver and refuses stale/drifted canonical
  Candidates in `VERSIONED_ACTIVE`. Detached source readback validates its RETAINED before-State,
  never a requirement that live State still be the before-State; ONLY high prepare/finalize/
  activate/resume compare live current-before (this separates authority timing without a public
  skip flag).

## 11. Caller-untrusted reload rules (no dict token)

- Every path/ref argument is untrusted: lexical containment FIRST (`_lexical_rel`), then
  `_safe`/`_safe_file` no-follow open, bounded read, strict JSON (duplicate-key refusal),
  schema validation against CURRENT disk schema bytes (for E docs; T rows are epoch-blob
  observations per §0/§12), self-digest recompute (`sha256_object` excluding only the declared
  digest field), live SHA/size recheck, cross-binding (`_check_doc_refs_against_seal` discipline:
  only seal-bound refs compared, SHA + `byte_count` where present), and pin recheck AFTER work
  (fresh P2V recheck after async build window precedent `prepare_publication:1610–1611`;
  finalize recheck `2047–2054`; snapshot recheck `248–256`).
- No `already_verified` / verified-dict / `pending` / `active_set` token, no route/kind enum
  from caller, no `seal_path` shortcut, no `implementation_sha` parameter from caller (extracted
  primitives drop it; `current_tools`/`contract`/`closure` belong to historian + high observation).
  `before_active_digest` is RECOMPUTED from retained/observed effective7 + Candidate
  (`survey_publication_set_v2.py:353–415`), never accepted as a caller value. Resume compares the
  full intent (operation-oracles.md), not set SHA alone. `pending_basis` plumbing, override
  context (`survey_agent_tool_v2.py:122–143`), and monkeypatch are never entered by the leaf.

## 12. Third-agent deliverables referenced here (exact shape required, values not invented)

The third agent (old-format/closure owner) MUST deliver, and Astra MUST confirm before code:

1. Exact old-format fingerprints from actual57: R3 shapes in scope (which proposal/retention/
   staged/receipt/set/revalidation schemas + which `code_deps` names + which style/recipe bytes
   are supported; unrecognized refuses). Derived from the saved57 manifest + proposed code graph;
   no wildcard `scripts/**`, no caller-supplied compatibility allowlist.
2. Full successor closure lists + controlled bootstrap additions: successors of canonical22/27
   (`survey_editorial_publication_v2.py:1996–2010`) and editorial/P3S50
   (`survey_editorial_staged_source_v2.py:143–201`, `survey_editorial_publication_v2.py:1958–1993`,
   `CODE_DEPS_SHAPE`/`CLOSURE_SHAPE` `len==50`) with renewal additions enumerated (no literal-50
   retention, no prefix widening). Report actual new counts/sets.
3. Control-diff path classification + recipe-specification boundary: `config/survey-production-v2.json:92`
   `implementation_control_roots` + `_verify_head_bytes` (`survey_weekly_derivation_v2.py:591–645`)
   + `Longform.verify_tool_basis` + contract-identity fields vs fixed recipe/specification
   (`survey_editorial_publication_v2.py:1183–1244`, low `992–1015`); recognized same-contract
   style/rendering path list vs specification/contract/schema/route/research/Profile migration
   triggers. Executable tool versions may change for C under the same fixed recipe/specification;
   U retains the historical build unit.
4. Git tree modes vs physical permissions: historical membership via `cat-file -e` /
   `merge-base --is-ancestor` + blob SHA (modes are current-eligibility only: `diff --summary`
   mode-change + R1 `1099–1101` refuse; no symlink or unselected mode migration).
5. Source/fixture/CLI/write/seam map confirmation for the above (which files are read vs written
   vs pinned; which seams refuse).

Until Astra confirms these PLUS the sibling accepted-authority return PLUS this file, implementation
is BLOCKED (decision §§9/11.3 stop rule: unpreservable predicate → contract revision or precise
NO-GO, never a weakened checker).

## 13. Choice contradictions the selected document does NOT determine — proposals (root selects, not silently adopted)

Each item names the gap, the concrete proposal grounded in source, and why the alternative is worse.
Astra MUST select or correct; this file does NOT implement any of them.

- **C1 — Renewal Candidate/QA/Gate schema carrier: new optional branch (PROPOSED) vs new schema files.**
  Gap: decision §§5–6/11.2 say "new strict optional renewal branch" + "inventing an extra authority
  field requires root review" but do not state whether old schema files are amended in place or new
  schema files are added. Proposal (grounded): AMEND the four old schema files IN PLACE with a new
  STRICT optional `renewal_source_proof_ref` (`{path,sha256}`) property (+ Gate `renewal_receipt_ref`),
  `additionalProperties:false` preserved, old required lists UNCHANGED, digest bases extended ONLY
  when present (§5). Reason: low `validate_seal:460` loads CURRENT disk schemas; a new schema file
  would fork the validator dispatch and risk silent old-branch bypass, while an in-place strict
  optional branch keeps legacy/editorial bytes valid verbatim (bootstrap verbatim-preservation rule,
  Astra R7) and makes the present-included digest rule enforceable in the existing
  `validate_candidate:753–766` / `validate_bundle:259–263` / Gate `1737–1753` / manuscript `427–448`
  recompute sites. Alternative (new schema files + new validator dispatch) is rejected as a larger
  fork with duplicated cross-binding logic. ROOT SELECTS.
- **C2 — Renewed Gate `derivation` variant name.**
  Gap: decision §11.2 says Gate "additionally takes `renewal_receipt_ref`" and "serialized Gate binds
  both" but does not name the renewed variant (`route/scope` values). Proposal: keep the
  `EDITORIAL_PUBLICATION_V1 / EDITORIAL_MAIN_BIB_STYLE` route/scope strings for U (same reviewed
  reader/trio, new proof context) and add a NEW variant `VERSIONED_RENEWAL_V1 / RENEWAL_MAIN_BIB_STYLE`
  for C (new `R/` trio/manuscript), each carrying BOTH `renewal_source_proof_ref` + `renewal_receipt_ref`.
  Reason: preserves the existing 4-way `oneOf` dispatch (`reader-surface-gate-v2.schema.json:160–217`)
  and `_derivation_for_manuscript:1145–1330` structure; U stays visibly editorial-shaped (honest reuse),
  C is visibly new (no laundering). Alternative (reuse `EDITORIAL_*` for C) is rejected as review-target
  confusion. ROOT SELECTS.
- **C3 — Freeze proof threading: derive-from-Candidate (PROPOSED) vs extra optional param.**
  Gap: decision §8/§11.2 say `_prepare_freeze_inputs` "derives proof from its validated Candidate,
  passes it to its direct review loader" but the actual signature is
  `(repo_root, candidate_path, approval_path)` with no proof param. Proposal: NO signature change for
  the existing entry; the renewal implementation derives the proof ref FROM the validated Candidate's
  own `renewal_source_proof_ref` field (reloaded + fully validated), threads it explicitly to the
  direct `reader.validate_review_record(..., renewal_source_proof_ref=...)` call, and extends the
  snapshot/alias sets (§10). A NEW wrapper with an optional expected-proof param is added ONLY for
  active-selection callers that must compare against the State-selected seal (stage/Preview/handoff).
  Reason: avoids forking every Freeze caller while keeping the explicit (non-ambient) threading;
  matches "derives proof from its validated Candidate" verbatim. Alternative (mandatory extra param
  on the existing function) would fork all callers including legacy paths. ROOT SELECTS.
- **C4 — `before_active_digest` payload for renewal.**
  Gap: decision §7 says "recompute with existing effective7+Candidate algorithm; basis/proof are
  additionally covered by new set and record refs" but does not state whether the 7 roles are the
  OLD `P/` roles or the NEW `R/` roles at activation time. Proposal: recompute from the RETAINED
  before-effective7 (old active set at `before_state_ref`, via `_recompute_before_digest` discipline
  `survey_publication_set_v2.py:1311–1313` + `_validate_proposal_retention_identity:1317–1420`) PLUS
  the observed before-Candidate (nullable per disk reality `1443–1462`), NOT from the new `R/` roles.
  New `R/` refs are covered by `set_ref` + `renewal_basis_ref` + `renewal_proof_ref` exact refs.
  Reason: matches "current-before vs retained-before and selected Candidate/digest must agree"
  (§7) and preserves the low invariant that `before_active_digest` measures the BEFORE context.
  ROOT SELECTS.
- **C5 — Renewal receipt `kind` reuse vs new kind.**
  Gap: decision §5 names `VERSIONED_RENEWAL_SOURCE_V1` for the manifest but the receipt file is still
  called `validated-source-manifest.json`; operator analysis debated reuse vs new rows. Proposal: NEW
  `kind` `VERSIONED_RENEWAL_SOURCE_V1` (same filename `R/validated-source-manifest.json`, new kind
  value, new strict schema file `versioned-renewal-source-manifest` is §3.3, NOT a relaxed old `<P>/`
  path). Reason: Gate `_derivation_for_manuscript:1182–1192` + low receipt bindings (`577–582,872–878`)
  dispatch on `kind`/route; reusing `EDITORIAL_PUBLICATION_SOURCE_V1` at a new namespace would let a
  stale validator accept a renewal receipt as editorial. ROOT SELECTS.
- **C6 — `R/publication-set.json` role paths: new `R/` paths (PROPOSED) vs mixed old/new.**
  Gap: decision §5 says U keeps "original target paths and exact old manuscript/source/PDF/page count,
  build record/log/digest and review records" while owned files list puts receipt/bundle/Gate/Candidate
  under `R/`. Proposal: seal ROLE `path` values point at the ACTUAL file locations (U: manuscript/trio/
  build3/reviews = ORIGINAL `P/` paths; receipt/bundle/Gate/Candidate = NEW `R/` paths; C: reader/authoring/
  retention/scope-history = ORIGINAL `P/` paths, all else NEW `R/` paths), and the low namespace check
  (`survey_publication_set_v2.py:480–487`: `proposal_ref == P/proposal.json` etc.) is extended so that
  `proposal_ref` stays `P/proposal.json` while `set path == R/publication-set.json` and role paths are
  validated as exact pinned locations (no inferred `P/publication/` prefix for renewal roles). Reason:
  matches "same exact 15 role names, new set kind, not a relaxation of old fixed `<P>/publication` paths"
  (§5) + operator verified U/C operability (§19). Alternative (copy old targets into `R/`) is forbidden
  (same-SHA different-path refused). ROOT SELECTS.
- **C7 — CLI `--reason` shape.**
  Gap: decision §7 lists `prepare/finalize/.../activate` with `reason` but the existing
  `activate-publication --reason` (`survey_editorial_publication_v2.py:3867–3872`) accepts free text.
  Proposal: renewal `activate --reason` takes the SAME free-text Core-change reason string, while
  `reason_class` is FIXED by the kind branch to `REVIEWED_VERSIONED_CORE_RENEWAL` (never from CLI).
  CLI validates that `--reason` is non-empty and truthful (non-false-editorial wording checked by
  review, not by regex), and refuses any `--reason-class` flag (no such flag is added). Reason: matches
  "truthful free-text Core-change reason" (§7) + distinct `reason_class/kind` routing by construction
  (no routing collision — technical review §25). ROOT SELECTS.
- **C8 — Renewal retention verifier placement.**
  Gap: decision §§3/8 say "existing P2R retained roots unchanged" + "P1/P2R/P2V/P3S renewal-aware"
  but do not name the new verifier. Proposal: NEW function in the history module
  `verify_renewal_retention(root, basis_path) -> {inventory, labels, digests}` implementing the
  second-generation `R/retained/before/` mapping rule (§8) + KEEP live rechecks, called by
  `validate_renewal_basis` (detached, every proof readback) and by high observation (live-before
  equality at boundaries). Existing `verify_retention:1737–2086` stays UNCHANGED for current
  authority (never called as historian after a Core change). Reason: preserves "existing P2R retained
  roots unchanged" while giving the fresh COPY a named owner (predicate-map §4 blocker 1). ROOT SELECTS.

No other silent adoptions. If Astra rejects any proposal, the outcome is a corrected map, never an
implementation with a weakened predicate.

## 14. Gate-ready checklist (this file)

- [x] Four new schemas with COMPLETE field/type/required/conditional definitions (§3) + digest
      expressions (§§3/5) grounded in actual `core.sha256_object` bases
      (`survey_publication_v2.py:743,766`; `survey_quality_v2.py:224,262–263`;
      `survey_reader_publication_v2.py:448`; `survey_reader_surface_gate_v2.py:1685,1753`;
      `survey_editorial_publication_v2.py:1893,1937,2348`; low `467,647`).
- [x] Activation branch `VERSIONED_RENEWAL_ACTIVATION_V1` + `REVIEWED_VERSIONED_CORE_RENEWAL` (§4)
      preserving legacy/editorial verbatim, with chain/anchor/before-digest/establishment rules
      grounded in low `1023–1230,1239–1314,1443–1462`.
- [x] Old Candidate/QA/manuscript/Gate strict branches + present-included digest rule (§5) grounded
      in actual builder/validator pairs (`build_manuscript_manifest`/`validate_manuscript_manifest`,
      `build_candidate`/`validate_candidate`, `build_bundle`/`validate_bundle`,
      `evaluate_reader_surface_gate`/`_inspect_gate_record`, `_derivation_for_manuscript`).
- [x] Exact entries/signatures/error/CLI shapes (§6) grounded in actual high signatures
      (`prepare_publication:1552`, `finalize_publication:2013`, `validate_editorial_receipt:692`,
      `validate_prepared_set:2555`, `activate_publication:3155`, `resume_activation:3643`,
      `verify_activation_history:3782`), `_fail`/`EditorialError` (`181–191`), CLI (`3837–3917`,
      exits `3914–3917`), low chain/digest/select (`before_active_digest:353`, `CHAIN_LIMIT:109`,
      `resolve_publication_selection:1807`, `require_active_or_canonical:2118`,
      `_require_active_candidate_binding:73`).
- [x] Acyclic U/C phase/call map (§7) with bans + lifecycle-dependent calls, fixing B1/B2/B4/B5 +
      O-B1 at design level per §11.1 (entry vs basis-bound observation split; proof after trio,
      manuscript+build after proof, receipt after build-record; no future refs; no caller trust).
- [x] File/pin read-write inventory incl freshly captured COPY + snapshot window (§8) grounded in
      two-phase capture, `_expected_retained_dest:831`, `_retained_expected_sets:835`,
      exclusive-write discipline (`TARGET_EXISTS`/`PUBLICATION_EXISTS` precedents
      `survey_editorial_publication_v2.py:493,1577,1617,1627,2138,2221,2267,2317,3152,3387,3545`),
      Freeze snapshot/preflight (`survey_publication_v2.py:171–390`).
- [x] Source proof after trio / build-before-receipt / U no-build / C new proof (§9) per §11.1
      (corrects the illustrative receipt-before-build remedy).
- [x] Context propagation incl nested reviews + Freeze snapshots + active vs inert (§10) per §11.2
      (keyword `renewal_source_proof_ref=None` + `renewal_receipt_ref`, nested threading, Freeze
      derivation + snapshot/alias coverage, State-selected equality, low structural-only projection).
- [x] Caller-untrusted reload rules (§11), third-agent shape (§12), and EIGHT explicit root choices
      (§13, C1–C8) flagged as selections, not adoptions.
- [ ] Sibling accepted-authority return: REFERENCED, not repeated (owned by another agent).
- [ ] Old-format fingerprints / successor closures / control-diff / mode discipline: REFERENCED as
      third-agent deliverables (§12), not invented here.

**Disposition:** THIS FILE is gate-ready as a map. IT IS NOT an implementation authorization.
Implementation stays BLOCKED until Astra confirms THIS file + the sibling accepted-authority return
+ the third-agent fingerprint/closure return under decision §§9/11.3. Any unclosable predicate
yields the exact blocker or precise NO-GO, never a weakened checker. Whole NOT_READY /
step4B3 OPEN / audit unstarted / DM021+022 OPEN. Stop at Human Commit Point; no ordinary
candidate/reconstruct commits; no genuine approvals.

(End — author-side pre-code map, interfaces/schemas/digests. No independence claim.)
