# Versioned renewal pre-code — fingerprints / closures / consumers R2 (author-side, Astra CHANGES_REQUIRED)

2026-10-23 JST. Author-side General pre-code return R2. Human HEAD `ce0de1a`.
Governing: `outputs/rephase-1-versioned-renewal-contract-decision.md` (192 lines, SHA256
`478f00510791b76af24aa7d61f398f0608f7ad8ae7808008c660f2bea6fbfdcf`) INCLUDING §11;
mandatory `notes/rephase-1-versioned-renewal-contract/astra-review-resolution.md`;
BOTH independent reviews WITH final-binding addenda;
siblings `notes/rephase-1-versioned-renewal-precode/interfaces-schemas-digests-r2.md` (R2, exact
basis carrier) + `accepted-authority-readiness-r2.md` (R2, session/shared-core rules).
R1 `fingerprints-closures-consumers.md` + `.json` are PRESERVED unchanged; every R1 occurrence
superseded below is listed explicitly. This file `fingerprints-closures-consumers-r2.md` (+ twin
`.json`) is the ONLY new write in this unit. No source edits/imports/tests/build/fixture/restore/
network/Git writes. Read-only source:
`.rephase-1-editorial-runtime/final-source-packaging/proof-copy/candidate-partial-b40de60`
(actual409/tree8ce + intended57, applied state).

## 0. What R1 got right, what Astra rejected, what R2 fixes (single gate, no alternates)

- Preserved from R1: 57-path manifest index (25M+32A, patch `659063dc…/2018112B` fresh-verified),
  P3S50 exact lists (30py+14schemas+3route+1staged+1style+1recipe), canonical22/27 exact lists
  (all-exist verified), E/T split (typed `RECEIPT_TOOL_CLOSURE` edges, never KEEP/prefix/wildcard),
  seal 15 roles + fixed `<P>/` paths, chain-32/anchor rules, mode/style/recipe/dirt/trust
  disciplines, consumer table. All `file:line` citations in R1 §§2/5/6 remain valid locations.
- REJECTED (Astra, stop reopening): R1 §4.4 Option N2 (0-new-schema variant, "50+3+0=53").
  Selected contract fixes 4 NEW schema files + 3 named new modules. R2 states ONE successor
  (§4). Any sentence in R1 offering N1-vs-N2 as alternatives is superseded by §4 of this file.
- CORRECTED (Astra + source crosscheck, sibling R2 trusted only after verification):
  (a) accepted-R2 §8 "1 existing branch, no other files" is WRONG. Source schemas all carry
  `additionalProperties:false` with no renewal fields (§1); renewal requires modifying at least
  5 existing schema files (§1). (b) accepted-R2 §9 shared-core placement is adopted ONLY with
  the exact transitive file lists in §4 (discovery/X were missing from R1's "50+7" guess and
  from the P3S50 set; R2 enumerates them). (c) interfaces-R2 "all reachable evidence" Freeze
  snapshot and "current closure checked by HIGH only" readback are narrowed to finite typed
  refs (§§6/8). (d) old fingerprints are re-anchored per-commit with artifact/tool-commit
  separation (§2). (e) steady-state allowed-change is a mechanical file predicate, not prose
  (§7). (f) config-contract registration vs old State/Profile is traced end-to-end (§9).

## 1. Existing schemas that MUST change bytes (5, verified) + 4 new files (fixed)

Source crosscheck (proof-copy, current disk): all four candidate schemas carry
`additionalProperties:false` and have NO renewal property today, so a strict optional renewal
branch CHANGES their bytes by definition:

- `schemas/reader-manuscript-v2.schema.json` (5751 B, `0d8f0e9e…`): `required` 14 keys, `editorialSource`
  `{proposal_ref,staged_manifest_ref}` (`:101-112`), no `renewal_source`. Renewal: C-only new
  mutually-exclusive `renewal_source:{path,sha256}` = `R/renewal-source-proof.json` path+SHA
  (XOR with `editorial_source`; never both/neither for renewed sets); U reuses old bytes with
  EXTERNAL `renewal_source_proof_ref` function keyword only (never serialized, never in digest).
- `schemas/publication-candidate-v2.schema.json` (2980 B, `46a88866…`): `required` 10 keys
  (`:7-19`), no renewal field. Renewal: new strict OPTIONAL `renewal_source_proof_ref:{path,sha256}`
  (new files only, U+C), digest 10→11 keys when present.
- `schemas/quality-regression-bundle-v2.schema.json` (3908 B, `ab8614f6…`): `required` 9 keys
  (`:7-18`), no renewal field. Renewal: new strict OPTIONAL `renewal_source_proof_ref` (new
  files only, U+C), digest 9→10 keys when present.
- `schemas/reader-surface-gate-v2.schema.json` (7492 B, `f10de43e…`): `derivation.oneOf` has
  exactly 4 variants (`DIRECT_PRIMARY`, `WEEKLY_GENERATED_V2`, `LONGFORM_GENERATED_V1`,
  `EDITORIAL_PUBLICATION_V1`, `:160-217`). Renewal: ONE new 5th variant
  `VERSIONED_RENEWAL_V1 / RENEWAL_MAIN_BIB_STYLE` BOTH U and C (`{route:const, scope:const,
  receipt:{path,sha256}, renewal_source_proof_ref:{path,sha256},
  renewal_receipt_ref:{path,sha256}}`); 4 old variants verbatim, never augmented.
- `schemas/publication-surface-revalidation.schema.json` (9162 B, `4c1ce929…`): `oneOf` exactly
  2 branches (legacy + `EDITORIAL_PUBLICATION_ACTIVATION_V1`, `:6-9`, `:97-245`). Renewal:
  third branch `VERSIONED_RENEWAL_ACTIVATION_V1` + `REVIEWED_VERSIONED_CORE_RENEWAL`
  (legacy/editorial verbatim).
- Review-record schema/bytes UNCHANGED: binding lives in the containing NEW Candidate/bundle/
  Gate (nested `validate_manuscript_manifest:643-647` threads the SAME reloaded proof ref
  explicitly). Old U review files stay byte-identical.

4 NEW schema files (new paths, no conflict): `versioned-renewal-basis-v2`,
`versioned-renewal-source-proof-v2`, `versioned-renewal-source-manifest-v2`,
`versioned-renewal-publication-set-v2` (+ build-record variant tags in `R/build-record.json`).
3 NEW modules (fixed names): `scripts/survey_versioned_renewal_history_v2.py`,
`scripts/survey_versioned_renewal_source_v2.py`, `scripts/survey_versioned_renewal_v2.py`.
Old/new pins are separate: historical validation of pre-renewal records uses OLD schema SHAs
(record epochs); renewal validation uses NEW disk bytes. Any drift in an old schema file
outside the 5 listed branches → `UNSUPPORTED_MIGRATION`.

## 2. Old fingerprints: per-commit pins, artifact/tool-commit separation, honest modes

- Old schema/closure pins live under THEIR OWN source commits, not at the tool commit:
  each T row is checked ONLY against its own recorded epoch blob
  (`git cat-file -e <epoch>^{commit}` + `git show <epoch>:<path>` SHA (+`byte_count` where
  sized); never live-path equality; never cross-substituted; missing → `HISTORY_BLOB_MISSING`,
  partialDB-26309 included). Separate epochs (interfaces-R2 §2.1, adopted):
  `receipt_epoch.repository_commit_sha` (receipt `current_tools`) vs staged `producer_head`
  (`survey_editorial_staged_source_v2.py:1039` manifest shape) vs per-schema epochs
  (`proposal/retention/staged/receipt/set/revalidation_schema_sha256`). Where dependency rows
  overlap, epochs must agree; otherwise `HISTORY_TOOL_EPOCH_DRIFT`.
- Publication artifacts are NOT at the tool commit (positive control, decision §3): review/
  manuscript/PDF/build/record files are produced AFTER the commit that built the tools, so
  "old evidence absent from the tool commit" MUST pass history. Recorded receipt hashes are
  never accepted merely because a receipt lists them; historical schemas are supported by the
  finite adapter + epoch cross-check (no arbitrary historical code execution, no remote
  `$ref` fetch).
- Chain + current schemas at bootstrap are BOTH known formats: chain walk
  `_walk_chain_backwards:1023-1051` newest→oldest over `supersedes` links (cycle/depth
  `CHAIN_LIMIT=32` refusal, `1060-1230` anchor/sequence/time rules); legacy-only predecessor
  (`REVIEWED_CORE_CHANGE` without a separate activation record) is UNSUPPORTED as a renewal
  predecessor (interfaces-R2 §0: prior seal + record + Candidate all REQUIRED nonnull).
  For repeat C→U→renewal and renewal→editorial, ALL ancestor epoch records are required —
  every prior activation's basis/proof/epochs along the walked chain, not just the latest
  original staged manifest. Any missing ancestor epoch → `HISTORY_BLOB_MISSING` (never forged).
- Historical modes from the ACTUAL git tree (honest): `git ls-tree HEAD` in proof-copy shows
  `100644 blob` for all 409-tracked paths (e.g. `.latexmkrc 078cba92…`,
  `schemas/reader-manuscript-v2 a751a4bc…`, `scripts/survey_weekly_derivation_v2 6d14009c…`,
  `templates/survey/jgaisurvey.sty 16c68ba2…`) and EMPTY for all new paths
  (`schemas/versioned-renewal-basis-v2.schema.json`, `scripts/survey_versioned_renewal_source_v2.py`
  return no entry — actual409 lacks new files, verified). Physical mode is `0o664` (umask,
  not a mode change). Manifest `git_mode:100644` for the 32 A-rows is the INTENDED post-commit
  mode, NOT a current tree fact (R1 §0 distinction retained). Recount fresh in this unit:
  25 tracked-modified + 32 untracked-new + 0 staged, matching manifest delta 57.

## 3. Bootstrap recognized R3 formats (finite, closed)

Exactly the R1 §1.2 set (adopted, no wildcard, no caller allowlist): P1 proposal shape
(`editorial-correction-proposal-v2.schema.json` + `validate_proposal:2188` + `_before_graph`
+ retention plan); retention layout `<P>/retained/before/<original_path>`
(`_expected_retained_dest:831`, `_retained_expected_sets:835`, `capture_retention:857`,
`verify_retention:1737`); staged closed trio + manifest + `verify_staged_source:1772` replay
(exact `{main,bibliography,style}`, no `primary`/`staged_refs` alias); editorial/Weekly/
Longform receipt shapes with `current_tools{repository_commit_sha,contract,closure}`;
editorial seal at fixed `<P>/publication/publication-set.json` with exact 15 roles
(`PUBLICATION_ROLES_15` verified); revalidation exactly 2 branches; P3S fixed-50 code deps
+ Weekly-22/Longform-27 control subsets; style + `.latexmkrc` (`REQUIRED_RECIPE_MARKERS`,
`FIXED_RECIPE_STEPS`); manuscript/Gate/QA/Candidate old branches verbatim. Unrecognized old
shape (unknown schema version, unknown `code_deps` name, unknown style/recipe bytes,
missing/foreign/ambiguous authority, dirty control roots, unavailable blobs, non-ancestor
epoch, unsafe path, changed research/Profile) refuses BEFORE writes.
Second-generation `R/retained/before/` + 4 new schemas + 3 new modules + 5 amended branches
are NEW (§§1/4), never recognized as old.

## 4. Proposed EXACT successor closure memberships (single concrete set — no alternates)

Location principle (accepted-R2 §9, adopted with exact lists): State-free CONTENT cores live
as NARROW private shared helpers IN the existing family files that own the predicates
(same pure helpers, same `citation_refs`/`_source_class`/token/URL/archive reuse); original
public validators keep UNCHANGED signatures via thin wrappers (State block + delegation);
`survey_versioned_renewal_source_v2.py` holds ONLY the session constructor (§2 of accepted-R2),
the §11.3 six-condition enforcement, Layer A/B orchestration, and calls into shared cores —
NO duplicated validator bodies (duplication only with justified equivalence oracle, accepted-R2
§9). Therefore the successor closure = P3S50 + family-transitive files the shared cores
reach + 3 new modules + 4 new schemas. Four disjoint categories (no prefix walks):

### 4.1 `.py` runtime closure (35 files — exact, finite)

- P3S50 `_SHARED_PY` 30 (R1 §4.3, all-exist verified — NOT repeated here; see R1 + manifest).
- Transitive family additions REQUIRED by shared-core placement (verified reachable, missing
  from P3S50): `scripts/survey_discovery_v2.py` (12757 B; screening `:397` function-local
  import; discovery→x_intake top-level), `scripts/survey_x_intake_v2.py` (23144 B; discovery
  top-level import). Proof: `survey_screening_v2` top-level imports exclude discovery
  (function-local `:397` only), `survey_discovery_v2` top-level imports `survey_x_intake_v2`,
  `survey_x_intake_v2` imports `core` + `schema_gate` + `discovery` only. All other family
  modules are already in the 30 (`survey_architecture_v2` + `_base`, `survey_drafting_v2` +
  `_base`, `survey_evidence_v2`, `survey_screening_v2`, `survey_completeness_v2`). No
  `survey_draft_profile_v2`, `survey_stage_validation_v2`, `survey_orchestrator_v2`,
  `survey_handoff_v2`, `survey_human_gate_v2`, `weekly_pipeline` additions: consumers, not
  leaf transitives (stage/orchestrator/handoff call renewal only via HIGH/active selection,
  §8 of decision; their imports do not enter the proof closure).
- 3 NEW modules (fixed): `scripts/survey_versioned_renewal_history_v2.py`
  (`verify_versioned_history` + `verify_renewal_retention` + typed E/T readers),
  `scripts/survey_versioned_renewal_source_v2.py` (session constructor + Layer A/B
  orchestration + `validate_renewal_basis` + `verify_renewal_source_proof`, NO validator
  bodies), `scripts/survey_versioned_renewal_v2.py` (`prepare/finalize/validate-receipt/
  validate-set/activate/resume/history` + CLI).
- Total `.py`: 30 + 2 + 3 = **35**. Any actual extra top-level `scripts.*` import beyond
  these 35 (+ route-conditional semantic producers below) → `CODE_DEPS_EXPANSION_REQUIRED`,
  never silent omit.

### 4.2 Schema / `$ref` closure (22 files — exact, finite; `$ref` is local `#/$defs` only)

- P3S50 `_SHARED_SCHEMAS` 14 (R1 §4.3).
- 4 NEW schema files (§1).
- 4 family schemas REQUIRED by shared cores but missing from P3S50 (verified `required`
  by accepted-R2 §4 table + pipeline contract membership):
  `schemas/discovery-acceptance-v2.schema.json`, `schemas/survey-discovery-record.schema.json`,
  `schemas/screening-v2-run-package.schema.json`, `schemas/screening-v2-batch-result.schema.json`.
  (Evidence package/task/card/supplement, edition view, ledger, completeness, matrix, selection,
  architecture, approval, summary, attention, synthesis input/result, draft package/result are
  either already in the 14 or in the pipeline-contract content set below; the four above are the
  only schema files the shared cores validate that are absent from BOTH the P3S50-14 AND the new-4.
  All `$ref` targets are local `#/$defs/*` (verified: candidate/QA/manuscript/gate/revalidation
  schemas use only `#/$defs/*` + inline `const/enum`; no remote `$ref`, no network fetch).)
- Total schema files in closure: 14 + 4 + 4 = **22**. Route-conditional reader/receipt schemas
  (Weekly `reader-surface-input` + `weekly-publication-source-manifest`; Longform
  `longform-reader-input` + `longform-publication-source-manifest`; semantic-publication
  producers `survey_weekly_semantic_publication_v2.py` /
  `survey_longform_semantic_publication_v2.py`) are the existing route-3 per route (already
  counted in the 50-union accounting; no new route files).

### 4.3 Content-contract files (pinned bytes, NOT `.py` runtime — exact, finite)

- Prompts (current-disk SHA equality, TC-content): `config/prompts/source-screening-v2.md`,
  `config/prompts/evidence-verification-v2.md`, `config/prompts/article-drafting-v2.md`,
  `config/prompts/profile-synthesis-v2.md`, `config/prompts/grok/x-source-intake-base-v1.md`,
  `config/prompts/grok/x-source-intake-weekly-v1.md`,
  `config/prompts/grok/x-source-intake-special-v1.md`.
- Config: `config/survey-production-v2.json` (control roots + 67 pipeline + 3 quality contract
  files; `implementation_control_roots: ["config","schemas","scripts",".github/workflows"]`),
  `config/publication-review-v2.json`, `config/survey-production-v2-requirements.txt`.
- Schemas-as-content (validated shape, current-disk equality where the leaf checks them):
  all §4.2 schemas + pipeline-contract family schemas (`evidence-v2-run-package/task/card`,
  `evidence-authority-supplement`, `edition-evidence-view`, `materiality-ledger`,
  `profile-completeness-result`, `candidate-matrix-v2`, `candidate-selection-v2`,
  `issue-architecture-v2`, `architecture-review-summary/attention/approval-record`,
  `draft-v2-package/result`, `profile-synthesis-v2-input/result`, `publication-review-record-v2`,
  `visual-review-record-v2`, `publication-preview-approval-v2`, `freeze-record-v2`,
  `release-manifest-v2`, `stage-checkpoint-v2`, plus docs contract files). Full 67+3 list is
  `config/survey-production-v2.json:6` (verified `PIPELINE_N 67 / QUALITY_N 3`); renewal
  registration APPENDS the §4.2 new-4 (+ the 5 amended files stay at their existing entries —
  no new entries for amendments).

### 4.4 Tooling / recipe (exact, finite — versions may change for C, specification may not)

- `templates/survey/jgaisurvey.sty` (6569 B, `035645ca…`), `.latexmkrc` (218 B, `18199fd8…`)
  with `REQUIRED_RECIPE_MARKERS` + `FIXED_RECIPE_STEPS` + `EXPECTED_ARGV_LUALATEX_BIBER`
  (`survey_editorial_publication_v2.py:40/60–74/1183–1244`). Executable evidence
  (absolute path, `real_sha256`, versions/argv/env, markers) is recorded per build, never
  Git-blobbed, never re-probed from an absent executable, never forged into an old log.

### 4.5 Registration deltas (exact — the ONLY control/contract list changes)

- `config/survey-production-v2.json`: `contract_files.pipeline` += 4 new schema paths
  (§4.2) + `implementation_control_roots` UNCHANGED (already covers `config/schemas/scripts/
  .github/workflows`). No new control root. `contract_files.quality` unchanged.
- Coverage gates to update (same unit, decision §8): `survey_editorial_staged_source_v2.py`
  `_SHARED_PY/_SHARED_SCHEMAS` + `_route_code_deps` (30→35 py, 14→18 schemas; union 50→59
  with route/staged/style/recipe constants unchanged: 35+18+3+1+1+1=59);
  `_editorial_closure_rows` (`survey_editorial_publication_v2.py:1958–1993`) + `len==50` gate
  → `len==59` with the same sorted-unique + AST edge-audit discipline;
  `test_group_c_editorial_consumers_v2.py:119–121` (`==30/==14` → `==35/==18`);
  canonical22→29 / canonical27→34 ONLY IF the 7 renewal files (3py+4schemas) join the
  route control subsets — decision: they DO (proof/basis/closure must be control-pinned at
  HIGH; Weekly `CURRENT_CLOSURE:28–51` + Longform `:52–80` each += the same 7, verified
  insertion points `weekly:37–50` / `longform:67–79`). Response to "guessing 50+7": the 7
  are the fixed 3+4 (§1); the +2 transitive (discovery/X) are proven reachable (§4.1), not
  guessed. Total successor union = **59** (35py + 18schemas + 3route + 1staged + 1style +
  1recipe). No prefix rule, no caller allowlist, no literal-50 retention.

## 5. Producer source proof: NO P3S manifest for C + mandatory old blob verification

- C has NO new old-format P3S staged manifest. New trio FILES under
  `R/staged-source/{main.tex,references.bib,jgaisurvey.sty}` (NO manifest file; proof IS the
  staged proof). C manuscript `renewal_source` is exactly `{path,sha256}` =
  `R/renewal-source-proof.json` (one ref, per interfaces-R2 §4.1 — R1's 4-ref shape is
  superseded). Forging an old-format P3S manifest at a renewal path refuses.
- Old tool-blob verification is MANDATORY in operation/normal proof, not audit-only
  (interfaces-R2 §0 rule, adopted): every T row at its own recorded epoch
  (`receipt_epoch`, `staged_producer_head`, schema epochs per §2) via
  `git cat-file -e` + `git show` SHA (+`byte_count` where sized); digest-only attestation
  is forbidden. Multiple epochs are an exact map, never a collapsed digest. U narrow
  condition is byte-derived (current renderer/style yields exactly old trio + complete
  reader; mismatch → `REUSE_TARGET_MISMATCH`, never auto-C; same SHA at a different target
  path is C).

## 6. Readback edges: startup + EVERY detached proof readback verifies current tools fresh

Accepted-R2 §3 split is adopted with exact call edges (source-crosschecked, no State recursion):

- Layer A (accepted-content subloader, NO Git): `load_renewal_accepted_authority(root,
  basis_path)` → session constructor → session-scoped shared-core privates (accepted-R2 §2
  list; bodies in R1 §§2.2–2.8 locations). Checks content predicates only. No
  `repository_commit_sha`, no closure/contract/commit compare, no epoch blob read, no
  `verify_state_basis`, no State load.
- Layer B (full detached proof verifier, source module, still NO State — runs at startup AND
  on EVERY proof readback, INCLUDING after activation): `verify_renewal_source_proof(root,
  basis_path, proof_path)` + `validate_renewal_basis(root, basis_path)` (decision §11.1:
  detached retained-COPY + unchanged-evidence checks on every proof readback). Layer B MUST:
  1. reload proof+basis, recompute self-digests, verify `proof.basis_ref`, accepted/reader/
     authoring equality, trio refs sized + SHA-verified;
  2. recompute CURRENT closure from CURRENT disk bytes (Weekly `current_closure:587–588`
     discipline; longform-generated equivalent; editorial union discipline
     `survey_editorial_publication_v2.py:1959–2000` as updated to 59 in §4.5), compare
     member-wise vs `proof.dependency_closure` / `basis.current_tool_epoch.closure`
     (missing/extra/drift → `BASIS_CURRENT_TOOL_DRIFT`); recompute `contract_identity`
     from current disk vs `proof.supported_contract` (apart from permitted
     implementation/style bytes per §7, else `UNSUPPORTED_MIGRATION`); verify schema files
     used in validation equal current disk bytes (§1/§4.2 pins); all via `_safe`/no-follow/
     bounded reads;
  3. require HIST verdict: `verify_versioned_history(record_path)` (record-only, no State;
     typed E/T classification, per-document epochs from records, COPY mapping/inventory,
     self-/cross-digests → descriptive `HISTORICAL_IDENTITY_VERIFIED`) reports matching
     observed epochs for this proof's `supported_epochs`; else `HISTORY_TOOL_EPOCH_DRIFT` /
     `HISTORY_BLOB_MISSING`. Layer B consumes the HIST verdict, never re-implements Git
     epoch reads, never issues a reusable permit.
- After-activation readback path (closes the hole): normal active consumers
  `validate_candidate:749–814` → `validate_manuscript_manifest:413–451` (with reloaded
  `renewal_source_proof_ref`) → `verify_renewal_source_proof` (Layer B steps 1–3) → rejects
  further Core drift WITHOUT demanding live-before equality (live-before equality stays
  HIGH write-boundary-only: `_observe_renewal_entry` before capture, `observe_renewal_authority`
  after basis/before finalize/immediately before activate). Detached `validate_renewal_basis`
  validates RETAINED before-State only. No authority transfers through returned dicts; every
  use reloads by persisted path. Forbidden in Layer A/B (enforced by pre-code DAG + review):
  `agent.validate_agent_state`, `resolve_checkpoint_artifact`, `current_stage_basis_override`,
  `_canonical_root_acceptance` State branch, `resolve_active_screening_acceptance`,
  `observe_current/renewal_authority`, Reader/Gate/Candidate/seal/full receipt/P1/P2R/P3S,
  `repository_commit_sha` as authority, `pending_basis`/`already_verified`/caller dicts.

## 7. Steady-state allowed change: MECHANICAL predicate (not semantic prose)

A post-bootstrap committed change is a supported same-contract Core renewal IFF ALL hold
(checked mechanically; any failure → `UNSUPPORTED_MIGRATION` + separate migration contract):

1. `git show <new_epoch>:<path>` succeeds for every closure member in §4.1–4.2 (no missing
   blob); `merge-base --is-ancestor <old_epoch> <new_epoch>` holds (non-ancestor epoch
   refuses); no symlink in any new tree entry; no mode change except the 5 amended schema
   files + 7 new files (mode `100644`, §2).
2. Closure membership: `set(new closure names) == set(§4.1 py ∪ §4.2 schemas ∪ route-3 ∪
   {staged,style,recipe})` exactly (sorted-unique; missing/extra → `CLOSURE_SET`).
3. Per-file bytes: every file EXCEPT the §1 amended/new set + `templates/survey/jgaisurvey.sty`
   + executable/tool files under the SAME fixed recipe is byte-identical to the recorded
   blob (`CLOSURE_DRIFT` on mismatch). Style bytes MAY differ (rendering evolution for C);
   recipe `.latexmkrc` bytes MUST equal pinned markers/steps (`RECIPE_INCONSISTENT` on drift).
4. Schema/contract: every schema file's `required`/`additionalProperties`/`oneOf` shape
   equals the recorded shape apart from the §1 five-branch additions
   (`CONTRACT_MISMATCH`/`CLOSURE_SET` on relaxation/new kind/route-semantics change);
   `contract_identity` recomputed from current disk equals `proof.supported_contract`
   apart from pipeline SHA movement caused SOLELY by the §4.5 registration (new-4 entries).
5. Research acceptance, Profile, Architecture, Draft authority, pipeline/quality semantic
   contract, review requirements, route family, recipe SPECIFICATION: all byte-identical
   (any change → `UNSUPPORTED_MIGRATION`, never renewal). U retains the historical build
   unit (no new build); C executable versions may change under the SAME fixed recipe (§4.4).
6. Classification by identity: same SHA at a different target path is C; source-only/comment-only
   TeX changes altering trio bytes are C; PDF-metadata-only deltas are C with new visual review.
   U mismatch → `REUSE_TARGET_MISMATCH` (refuse, no auto-convert).

## 8. Freeze snapshot: FINITE typed-ref algorithm (no generic walk)

Renewal extends `_prepare_freeze_inputs:171–245` + `_preflight_freeze_pair:323–390` with an
EXPLICIT finite member function (replaces interfaces-R2 "all reachable evidence" wording):

```text
renewal_freeze_snapshot_set(validated Candidate C, seal S, basis B, proof P) =
  { C.path, approval.path, visual.path, bundle.path, profile.path,
    manuscript.path, source.path, pdf.path, semantic_review.path }        # existing :213–229 (9)
  ∪ { S.renewal_basis_ref.path, S.renewal_proof_ref.path,                  # 2
      B.retained_copy_ref.path,                                            # 1 (R/retained/before/<rel>)
      P.output_trio_refs.{primary,bibliography,style}.path (old P/ or new R/ per disposition),  # 3
      B.old_tool_epochs.receipt_epoch closure rows (names in §4.1–4.2, old SHAs — pinned list),# N_old
      B.current_tool_epoch.closure rows (names in §4.1–4.2, new SHAs — pinned list),           # N_new
      C.renewal_source_proof_ref.path (= P.path), Gate.renewal_receipt_ref.path (= receipt.path) } # 2 (dedup)
```

- Deduplicate by exact `(path,sha256)`; each member `_safe_file` + `sha256_file` into
  `{rel:sha256}`; `_recheck_snapshot:248–256` fails on any delta between preparation and
  install (repair: fresh id, never in-place overwrite).
- `_preflight_freeze_pair` authority/overlap checks (`authority_raw:359–376` = manuscript/
  source/pdf/bundle/reviews + Candidate/approval/visual/bundle/Profile paths;
  `identities/spellings:377–390`) are extended with the SAME finite set above (proof/basis/
  retained COPY/closure rows as typed refs); target-overlap/aliasing (freeze/manifest target
  vs any snapshot member; nested outputs; target/input aliasing) refuses. Generic
  "walk everything reachable" is FORBIDDEN (unbounded, unreviewable). Snapshot file list beyond
  this rule (per-seam manifest procedure) stays a pre-code enumeration obligation, but the
  MEMBERSHIP FUNCTION is closed here.

## 9. Config-contract registration vs old State/Profile (root question — traced, NO silent rebind)

- Mechanism (verified): `contract_identity(repo_root, cfg, research_profile, publication_profile)
  :210–228` = `aggregate_file_hash(pipeline_files + [DEFAULT_CONFIG, PROFILE_SCHEMA,
  STATE_SCHEMA])` + quality/research/publication pins. Registering the §4.5 new-4 schema entries
  in `contract_files.pipeline` (67→71) changes `pipeline_contract_sha256` → new tool epoch.
  State/Profile bytes stay OLD (no rebind: `state.implementation.repository_commit_sha` and
  Profile content are history; renewal basis pins them as `old_tool_epochs` + `profile_ref`,
  never rewrites them).
- Why this is NOT a blocker (mechanical trace, not prose): (a) old receipt closure/contract
  are verified HISTORICALLY against old blobs (§2/§6 Layer B-3), never required to equal the
  new disk; (b) new closure/contract are verified CURRENTLY against live+loaded bytes (§6
  Layer B-2) with the §4.5 registration as the expected set — the pipeline SHA movement
  caused SOLELY by the 4 new entries is the predicted delta, any OTHER movement refuses;
  (c) stage `validate_stage:740–767` computes `current_contract` from CURRENT disk + current
  Profile labels and embeds it in the `CORE_STAGE_CONTRACT` PASS report; `agent_control`
  `_validate_stage_contract:280–343` compares report contract vs current disk
  (`report.contract != contract → mismatch :328–329`) + Profile/State authority
  (`:310–320`) — all consistent under the new epoch because the report is minted AFTER
  registration with the UNCHANGED Profile bytes (Profile validity `validate_profile` is shape,
  not epoch equality; `_profile:179–186` + stage artifact Profile-identity checks
  `:215–218/599–605/659–660` compare labels/bytes, not contract SHA); (d) Preview (`validate_
  preview_approval` + Candidate binding), Freeze (`_prepare_freeze_inputs` + §8 snapshot),
  Release (manifest + reconciliation review) all derive from the State-selected NEW set +
  current disk contract — no Profile rebind occurs (Profile path/bytes identical; only the
  tooling contract advances, which is exactly what `old_tool_epochs` vs `current_tool_epoch`
  separate in the basis).
- Latent risk that WOULD flip this to NO-GO (explicit tripwire): if ANY stage/Preview/Freeze/
  Release validator compares the OLD State's stored implementation contract (or the old receipt's
  `current_tools.contract`) for EQUALITY with the new disk contract instead of the
  history-vs-current split above, the bootstrap self-bricks (new tools refuse old authority
  AND old tools refuse new closure). Pre-code MUST grep-confirm that no such equality exists
  outside the Layer B-2/HIST split (§6) and the `_validate_stage_contract` current-vs-current
  check (`:325–329`, which is current-vs-current and therefore safe). If such an equality is
  found → precise NO-GO with `file:line`, not a weakened checker.

## 10. Consumer inventory deltas from R1 (renewal-aware, same unit)

R1 §7 table stands EXCEPT: P1/P2R/P2V/P3S/editorial-high are renewal-aware ONLY via the
session/shared-core + Layer B/HIST split (§6) + finite prior-receipt match
(`BASIS_ACCEPTED_SET_DRIFT`, accepted-R2 §5.2); they are NEVER called as renewal entries
(P1 `validate_proposal` never mints a renewal basis; `verify_retention` never runs as
historian; `observe_current_authority` never gates renewal — new `observe_renewal_authority`
+ `_observe_renewal_entry` + `validate_renewal_basis` own the three timings). Repeat renewal
+ renewal→editorial + R1×2→editorial→renewal anchor + history/current readback + readonly
`ALREADY_ACTIVE` retry are MANDATORY same-unit capability tests with ALL ancestor epochs
(§2), not claims about existing modules. `quality.validate_checks` executes nothing (supplied
rows only, verified `:132–174`); operation authors no semantic/visual PASS; placeholder
editions stay production-semantic NO-GO.

## 11. Gate verdict (single, concrete)

**GATE: GO-CONDITIONAL — implementation may proceed ONLY after Astra confirms this file +
siblings R2 jointly AND the implementer delivers the §4.5 registration + §6 Layer B + §8
snapshot enumeration + §9 tripwire grep with exact `file:line` evidence.** No N1/N2
alternatives remain (N2 rejected). Any unclosable predicate (shared-core extraction that
changes existing-file control flow without equivalence oracle; Layer B drift undetectable
without State load; Freeze member beyond §8 function; stage equality outside the §9 safe
checks; missing ancestor epoch; forged blob; same-SHA different-path acceptance; C without
real build + new postrender reviews; synthetic approval promotion) → precise NO-GO with
`file:line` + required migration/separate-contract decision, never a weakened checker.
Whole NOT_READY / step4B3 OPEN / audit unstarted / DM021+022 OPEN. Production semantic NO-GO
on placeholder editions. Stop at internal return; no code, no ordinary Commit/Push
(Human-owned).

(End — R2 supersedes R1 N2/50+7/"1 existing branch"/generic-walk/current-only-tool-check
occurrences; R1 preserved unchanged; no independence claim; no runtime evidence.)
