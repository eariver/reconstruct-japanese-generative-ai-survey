# Versioned renewal pre-code — old-format fingerprints, closures, consumers (author-side)

2026-10-23 JST. Author-side General pre-code return (third-agent half: fingerprints / closures /
consumers). NOT independent review, NOT implementation authorization.
Human HEAD `ce0de1a` (root observed clean `main...origin/main` at task start).
Governing: `outputs/rephase-1-versioned-renewal-contract-decision.md` (192 lines,
SHA256 `478f00510791b76af24aa7d61f398f0608f7ad8ae7808008c660f2bea6fbfdcf`) INCLUDING §11;
mandatory `notes/rephase-1-versioned-renewal-contract/astra-review-resolution.md` (R1–R8);
BOTH independent reviews WITH final-binding addenda; author inventory
`notes/rephase-1-versioned-renewal-contract/accepted-authority-predicate-map.md` (F1–F8, OPEN gaps);
siblings `notes/rephase-1-versioned-renewal-precode/accepted-authority-readiness.md` (predicate half)
+ `interfaces-schemas-digests.md` (schema/digest/entry/call-map half, C1–C8 proposals) +
`operation-oracles.md` (oracle half). This file is the ONLY new write in this unit (plus optional
machine-readable `.json` twin). All old docs preserved. No source edits/imports/tests/build/fixture/
restore/network/Git writes. Read-only source below.

## 0. Source, method, coverage (read first — what is proved here vs adopted)

- Read-only input: `.rephase-1-editorial-runtime/final-source-packaging/proof-copy/candidate-partial-b40de60`
  = actual detached `409b292` / tree `8ce36998` + intended 57 overlay (`25M + 32A`), applied state.
  Proof-copy HEAD/tree/log/remote/status transcribed in packet `source-observation.md` §§2–3; NOT
  re-certified here. Reconstruct HEAD at write time is task-premise `ce0de1a`; this file does not
  mutate it.
- Full-57 identity is ADOPTED from the saved packaging manifest
  `notes/rephase-1-editorial-operation-implementation/source-packaging/complete-r3-operation-manifest.json`
  (delta 57 = 25 tracked-modified + 32 untracked-new; patch
  `complete-r3-operation-409.patch` 2018112 B SHA256
  `659063dc27f0926aaf6e8a33f322937076563c4a23f6cf0d80ca970e1b2abd5b`, DIRECT 409, verified
  `ls`+`sha256sum` fresh in this unit: size 2018112 present, digest match). Manifest per-file
  `{bytes, sha256, git_blob, git_mode, physical_mode, git_status}` table is the old-format
  fingerprint authority for §1. It is NOT re-hashed in full here.
- Fresh verification in THIS unit (read-only stdlib/`sha256sum`/`git ls-files -s`/`stat`, no repo-code
  imports, no `__pycache__`): (a) patch file digest/size match above; (b) 23 closure-critical files
  (all of §4 P3S-shared 30+14 + route extras + staged/style/recipe + key schemas/modules) re-hashed,
  all match manifest SHAs where the path is in the 57 set (list in §1.3); (c) `git ls-files -s`
  + `--others` + `diff --name-only HEAD` counts re-checked: 25 tracked-modified, 32 untracked-new,
  0 staged (`diff --cached` empty); (d) physical `0o664` vs Git `100644` spot-checked
  (`scripts/survey_editorial_publication_v2.py`, `templates/survey/jgaisurvey.sty`, `.latexmkrc`,
  `config/survey-production-v2.json`, `scripts/survey_weekly_derivation_v2.py`); (e) top-level
  `scripts.*` import edges re-parsed with stdlib `ast` (no execution) for §6.
- Explicit NON-coverage: full 57-file byte re-hash was NOT done here (adopted from manifest +
  packaging `proof-after-721-ok` / `snap-721-pins` records); no claim of fresh all-57 proof, no
  full-tree hydration, no missing-26309 blob census, no guard/isolation/CAS certification, no
  runtime/test evidence. Any consumer of §1 must cite manifest rows as adopted pins + §1.3 subset
  as fresh spot-checks, never as "all 57 freshly proved in this unit".
- Critical manifest-vs-index distinction (§5.1): manifest records `git_mode: 100644` for ALL 57
  INCLUDING the 32 `A` rows as the INTENDED post-commit mode. Current proof-copy index has NO
  entry for those 32 (they are untracked `??` today; `git ls-files -s -- <new-path>` returns
  empty; `diff --cached` empty). Manifest `A/100644` is therefore an intended-mode pin, NOT a
  claim that the artifact already exists at the tool commit. §1 lists both columns separately.

## 1. Exact current old-format fingerprints (R3 adapter input — finite)

### 1.1 The 57-path manifest (adopted pins; sorted; M=tracked-modified, A=untracked-new)

`git_status | bytes | sha256 (full in manifest) | path`. Fresh-subset marker `*` = re-hashed in
this unit and matched (§1.3). All rows `git_mode 100644 / physical_mode 0o664` per manifest.

```text
M  8341 *8c779e60… .github/workflows/build-special-pdf.yml
M  4724  82840cf5… .github/workflows/build-weekly-survey.yml
M 37815  050661e5… .github/workflows/survey-production-v2-export-publication-preview.yml
M 18563 *cde4f115… config/survey-production-v2.json
A  3945 *5623c0d9… schemas/editorial-correction-proposal-v2.schema.json
A  2338 *043ce8a5… schemas/editorial-manuscript-spec-v2.schema.json
A  2972 *b7c82476… schemas/editorial-publication-build-record-v2.schema.json
A  3107 *7beebcef… schemas/editorial-publication-set-v2.schema.json
A  3047 *494a1d15… schemas/editorial-publication-source-manifest-v2.schema.json
A  5618 *347e5499… schemas/editorial-retention-manifest-v2.schema.json
A  5627 *4fa61723… schemas/editorial-staged-source-manifest-v2.schema.json
A   868 *50b5dc3e… schemas/editorial-toolchain-spec-v2.schema.json
A  2720  4dadf873… schemas/longform-publication-source-manifest-v2.schema.json
A 10624  7bae9d2a… schemas/longform-reader-input-v2.schema.json
M  9162 *4c1ce929… schemas/publication-surface-revalidation.schema.json
M  5751 *0d8f0e9e… schemas/reader-manuscript-v2.schema.json
M  7492 *f10de43e… schemas/reader-surface-gate-v2.schema.json
M  4219 *e8598239… schemas/reader-surface-semantic-review-v2.schema.json
M  4455  b3e0d976… scripts/run_semantic_publication_v2_interactive.py
M 19271  c6cd1957… scripts/run_semantic_publication_v2_interactive_base.py
M 149677 cd8af389… scripts/survey_agent_control_v2.py
A 136407 *23e3a45f… scripts/survey_editorial_correction_proposal_v2.py
A 40853 *fcbeee43… scripts/survey_editorial_current_authority_v2.py
A 256725 *98f8ff8b… scripts/survey_editorial_publication_v2.py
A 122624 *036d258f… scripts/survey_editorial_retention_v2.py
A 131124 *0fb23e83… scripts/survey_editorial_staged_source_v2.py
M 12510  e8d69212… scripts/survey_handoff_v2.py
M 66711  757743e0… scripts/survey_human_gate_v2.py
A 62260 *c09c5558… scripts/survey_longform_derivation_v2.py
A 40754 *2da1da8c… scripts/survey_longform_generated_v2.py
A 36224  4d235a38… scripts/survey_longform_semantic_publication_v2.py
M 56106  38e6bfa9… scripts/survey_orchestrator_v2.py
M 58572 *cdc6474b… scripts/survey_production_v2.py
M  8636  3c3a8ffa… scripts/survey_profiled_freeze_v2.py
A 127802 *ecd7faca… scripts/survey_publication_set_v2.py
M 32030 *2f7691db… scripts/survey_reader_publication_v2.py
M 102815 *879eedd2… scripts/survey_reader_surface_gate_v2.py
M 12381 *fb246e51… scripts/survey_schema_v2.py
M 10415  ddee6577… scripts/survey_semantic_quality_v2.py
M 41555  de02bf98… scripts/survey_stage_validation_v2.py
M 44421 *2d3be54c… scripts/survey_weekly_derivation_v2.py
M 91234  036601ac… scripts/survey_weekly_mechanical_refresh_v2.py
M  6569 *035645ca… templates/survey/jgaisurvey.sty
A  7908  07ede73a… tests/test_group_c_editorial_consumers_v2.py
M 26330  6ed1c1f2… tests/test_survey_dm004_release_validate_state_v2.py
A  7564  8cdda79c… tests/test_survey_editorial_activation_faults_r4c.py
A 113327  93b39b44… tests/test_survey_editorial_correction_proposal_v2.py
A 74632  323c7377… tests/test_survey_editorial_current_authority_v2.py
A 19229  638112d7… tests/test_survey_editorial_r5_gaps_v2.py
A 18956  77ab305e… tests/test_survey_editorial_r7_boundary_v2.py
A 94304  954f8586… tests/test_survey_editorial_retention_v2.py
A 148482 851d5e1e… tests/test_survey_editorial_staged_source_v2.py
A 91161  ce687447… tests/test_survey_longform_derivation_v2.py
A 107757 4a03b564… tests/test_survey_longform_publication_integration_v2.py
A 13539  ab6c9ca4… tests/test_survey_publication_r3_anchor_shape_v2.py
A 61487  d51d74e3… tests/test_survey_publication_set_v2.py
A  7710  c5db5940… tests/test_survey_schema_cache_v2.py
```

Full per-file `git_blob` (index/staged blob for M rows; `hash-object` model for A rows) is in the
manifest and is NOT repeated here to avoid transcription drift. Consumers must read the manifest
JSON directly; the table above is an index, not a second pin source.

### 1.2 Bootstrap-recognized R3 shapes (finite adapter scope — unrecognized refuses)

The finite old-format adapter recognizes EXACTLY the R3 shapes present in actual57. No
`scripts/**` wildcard, no caller-supplied allowlist, no remote `$ref` fetch.

- Proposal: `schemas/editorial-correction-proposal-v2.schema.json` (`5623c0d9…`, A) as read by
  `survey_editorial_correction_proposal_v2.py:13 validate_proposal / :2188 prepare` with P1 header/
  basis/proposed/plan + `_before_graph` + retention-plan shapes (§2). Any other proposal schema
  version refuses (`UNSUPPORTED_MIGRATION`).
- Retention: `schemas/editorial-retention-manifest-v2.schema.json` (`347e5499…`, A) + retained
  layout `<P>/retained/before/<original_path>` (`survey_editorial_retention_v2.py:831–854`,
  `_expected_retained_dest` + `_retained_expected_sets`), `capture_retention` one-shot
  `O_EXCL` claim, `verify_retention:1737–2086`. Second-generation `R/retained/before/` is NEW
  (C8, unclosed placement) and is NOT an old recognized shape.
- Staged: `schemas/editorial-staged-source-manifest-v2.schema.json` (`4fa61723…`, A) + closed
  `<P>/staged-source/{main.tex,references.bib,jgaisurvey.sty}` + staged manifest LAST +
  `verify_staged_source:1772–2169` standalone replay. Only `main|bibliography|style` exact trio;
  `primary`/`staged_refs` aliases refused (`survey_reader_publication_v2.py:253–264`,
  `survey_publication_set_v2.py:535–536`).
- Receipt: `schemas/editorial-publication-source-manifest-v2.schema.json` (`494a1d15…`, A) for
  `EDITORIAL_PUBLICATION_SOURCE_V1` + Weekly `schemas/weekly-publication-source-manifest-v2.schema.json`
  (`c11ad525…`, tracked-409, unchanged) + Longform
  `schemas/longform-publication-source-manifest-v2.schema.json` (`4dadf873…`, A), each with
  `current_tools{repository_commit_sha,contract,closure}` + `contract` + `closure` exact rows.
  Renewal receipt KIND `VERSIONED_RENEWAL_SOURCE_V1` is NEW (sibling C5, unclosed) and is NOT an
  old recognized shape; reusing the editorial kind at `R/` paths must refuse.
- Seal/set: `schemas/editorial-publication-set-v2.schema.json` (`7beebcef…`, A) for editorial
  sets at fixed `<P>/publication/publication-set.json` with exact 15 roles (§2.4) +
  `schemas/publication-surface-revalidation.schema.json` (`4c1ce929…`, M) with exactly two
  branches (`oneOf` lines 6–9: legacy + editorial). Renewal set KIND `VERSIONED_RENEWAL_SET_V1`
  + activation `VERSIONED_RENEWAL_ACTIVATION_V1` / `REVIEWED_VERSIONED_CORE_RENEWAL` are NEW
  (§§3–4 of sibling interfaces file) and are NOT old shapes.
- Code deps: `_SHARED_PY` 30 + `_SHARED_SCHEMAS` 14 + route-3 + staged-1 + style-1 + recipe-1
  = 50 exact (§4). Any actual extra top-level `scripts.*` import beyond this set requires
  `CODE_DEPS_EXPANSION_REQUIRED` (`survey_editorial_staged_source_v2.py:188–192`), never silent
  omit. `Weekly CURRENT_CLOSURE` 22 / Longform 27 are the control-root subsets (§4), not the
  full P3S set.
- Style/recipe: `templates/survey/jgaisurvey.sty` (`035645ca…`, M, 6569 B) + `.latexmkrc`
  (`18199fd8…`, 218 B) with `REQUIRED_RECIPE_MARKERS` (`survey_editorial_publication_v2.py:74`)
  and fixed steps (`:60–70`). Style bytes may evolve for C under the SAME recipe specification;
  recipe-specification change is migration (§5.2).
- Manuscript/Gate/QA/Candidate: `schemas/reader-manuscript-v2.schema.json` (`0d8f0e9e…`, M),
  `schemas/reader-surface-gate-v2.schema.json` (`f10de43e…`, M),
  `schemas/reader-surface-semantic-review-v2.schema.json` (`e8598239…`, M),
  `schemas/quality-regression-bundle-v2.schema.json` (`ab8614f6…`, tracked-409),
  `schemas/publication-candidate-v2.schema.json` (`46a88866…`, tracked-409). Old branches stay
  verbatim; renewal `renewal_source_proof_ref` / `renewal_source` / `renewal_receipt_ref`
  branches are NEW (sibling C1/C2, unclosed carrier).

### 1.3 Fresh spot-check hashes (this unit; subset — NOT full-57 proof)

Read-only `sha256sum` of live proof-copy bytes (first 16 hex shown; full digests verified equal
to manifest `sha256` for every row below):

```text
0fb23e83caec01f7  scripts/survey_editorial_staged_source_v2.py  131124
98f8ff8bb74f5fc0  scripts/survey_editorial_publication_v2.py   256725
2d3be54c9f42fa73  scripts/survey_weekly_derivation_v2.py       44421
2da1da8ccd263c27  scripts/survey_longform_generated_v2.py       40754
ecd7facac09a5c97  scripts/survey_publication_set_v2.py         127802
2f7691db90f8bd55  scripts/survey_reader_publication_v2.py      32030
879eedd24ef7f850  scripts/survey_reader_surface_gate_v2.py    102815
f3b73d857a7281a4  scripts/survey_publication_v2.py             51835
f8a3ef6affd236d2  scripts/survey_quality_v2.py                 13322
23e3a45f5adb4c2b  scripts/survey_editorial_correction_proposal_v2.py 136407
036d258fa58fc876  scripts/survey_editorial_retention_v2.py     122624
fcbeee43ceaac80d  scripts/survey_editorial_current_authority_v2.py  40853
cdc6474b3c46e42b  scripts/survey_production_v2.py               58572
4c1ce92944da0769  schemas/publication-surface-revalidation.schema.json 9162
0d8f0e9e66cc8853  schemas/reader-manuscript-v2.schema.json     5751
f10de43eb85be325  schemas/reader-surface-gate-v2.schema.json   7492
494a1d152c76bca8  schemas/editorial-publication-source-manifest-v2.schema.json 3047
7beebcef48d77773  schemas/editorial-publication-set-v2.schema.json 3107
ab8614f61484e742  schemas/quality-regression-bundle-v2.schema.json 3908
46a888668862546b  schemas/publication-candidate-v2.schema.json 2980
4fa6172338072258  schemas/editorial-staged-source-manifest-v2.schema.json 5627
035645caa06eb77e  templates/survey/jgaisurvey.sty               6569
18199fd85e3e3c46  .latexmkrc                                    218
```

Plus P3S-shared rows (all matched, first-16 shown): `9c64ebce render_article_draft_tex`,
`cd8af389 agent_control`, `0ff3bd9a agent_tool`, `b444bb43 architecture`, `e1d61713
architecture_base`, `b51bcab8 bibliography_access`, `dd78603e completeness`, `57b62c5f
citation_refs`, `ac7d6942 drafting`, `692e70c6 drafting_base`, `f7478d86 evidence`,
`c09c5558 longform_derivation`, `0d29b304 reader_fidelity`, `be50e5e3 review_attention`,
`fb246e51 schema_gate`, `9b7ff109 screening`, `bef91a53 validate_article_draft`,
`f6ceaf80 weekly_pipeline`; schemas `5623c0d9 correction-proposal`, `043ce8a5 manuscript-spec`,
`b7c82476 build-record`, `347e5499 retention-manifest`, `50b5dc3e toolchain-spec`,
`46a88866 candidate` (dup), `e8598239 semantic-review`; route extras `8db11d4a
reader-surface-input`, `c11ad525 weekly-receipt`, `53315030 weekly_semantic_publication`.
Coverage = closure-relevant subset only; full-57 freshness is NOT claimed.

## 2. Historical E/T/capture-graph role, schema, epoch maps (actual-source)

### 2.1 Graph construction (P1 — classification only, never a leaf callee)

- Builder: `survey_editorial_correction_proposal_v2.py:687–1470 _build_graph` with `_Graph:578–605`
  (`node` HASH/POLICY conflict, `edge`, `canonical`), `_pol:783–791` (mutable publication bytes
  → `COPY_BEFORE_REPLACEMENT`, else `KEEP_IMMUTABLE`), `_add_file:787–792` (ref must carry
  `{path,sha256}`; pins via collector; node role + policy).
- Tool rows are NORMALLY KEEP under `_pol`, so classification MUST use typed edges + fixed
  membership, never KEEP/dir-prefix/wildcard (decision §3 + Astra R2):
  `receipt.get("current_tools").closure[] → _add_file(row, "receipt:tool-closure:<name>")` +
  `graph.edge(receipt_rel, "RECEIPT_TOOL_CLOSURE <name>", rel, sha)` (`:955–958`); accepted/capture
  rows → `RECEIPT_CLOSURE` edges (`:953–954`); outputs → `RECEIPT_CLOSURE output:<role>` (`:959–961`);
  QA results → `QUALITY_OUTPUT` (`:963–968`); bundle bindings → `QUALITY_OUTPUT` (`:969–995`);
  reviews → `SEMANTIC_EDITORIAL/VISUAL` (`:997+`). Historian owns this typed E/T split
  (`verify_versioned_history`, §6.1); leaf consumes only basis-pinned refs.
- Mutable set (COPY) = versioned-effective7 + Candidate + State + operational authoring inputs +
  `<P>/retained/before` COPY dests; everything else KEEP. Live State node is operational COPY,
  never a frozen digest member (`:794–800`).

### 2.2 Evidence (E) — live + retained-COPY recheck rows

Roles: `checkpoint:original-record`, `checkpoint-row:<name>` (7-row effective map +
`VERSIONED_ACTIVE` 7-row variant `:470–538`), `state:authority` (operational), accepted refs
(evidence-acceptance, candidate-matrix, materiality-ledger, discovery-acceptance, architecture,
synthesis-input/result, per-package draft-package/result, archive, authored inputs),
`RECEIPT_CLOSURE` accepted/capture/output rows, `QUALITY_OUTPUT` rows, staged trio
`{main,bibliography,style}`, manuscript `{primary_source + supporting BIBLIOGRAPHY/STYLE}`,
PDF/log/digest, Gate `derivation` bound refs, Candidate nested refs, seal 15 roles.
Evidence rows require LIVE original bytes at recorded paths + `sha256 == ref.sha256`
(+ `len == byte_count` where sized) + seal/self-digest equality + typed cross-bindings.
Drift → `HISTORY_DIGEST_MISMATCH` / `RENEWAL_PROOF_*`. Old evidence absent from the tool commit
is a POSITIVE control (records are produced after that commit; decision §3) — it must PASS
history, never be demanded as a blob at the epoch.

### 2.3 Tool (T) — own-epoch blob rows (never live-path equality)

Rows: every `receipt:tool-closure:*` member (= the fixed P3S 50 set, §4) + staged `code_deps`
+ `style_input_ref` + `capture_inputs`. Each row is checked ONLY against its OWN recorded tool
epoch's Git blob (`git cat-file -e <epoch>:<name>` + blob SHA), never by requiring old tool
bytes to still occupy the live path. Epoch fields are SEPARATE and must agree where dependency
rows overlap: old P3S `producer_head` (staged manifest `:1039`) vs receipt
`current_tools.repository_commit_sha` (minted at prepare BEFORE publication authorities exist).
A field is never silently replaced by HEAD. Forged row / epoch cross-substitution / missing blob
(partialDB-26309) → `HISTORY_TOOL_EPOCH_DRIFT` / `HISTORY_BLOB_MISSING` (never reconstructed
from network, never forged ancestry). External executable evidence (absolute path, `real_sha256`,
versions/argv/env, `.latexmkrc` markers) is recorded evidence, never a Git blob.

### 2.4 Capture/retention mapping (P2R — layout only, verifier stays high-side)

- One-shot `capture_retention:857+` (imports P1 lazily `:859`); `_expected_retained_dest
  (proposal_dir, original_path) = proposal_dir + "/retained/before/" + original_path` (`:831–832`);
  `_retained_expected_sets:835–854` (every COPY dest + manifest; retained root + every ancestor
  dir below it; late new file/empty dir refuses); `_Session:181–527` (`safe_read`, dirfd/no-follow,
  `reverify`, `_close_all`); `verify_retention:1737–2086` (header/basis/proposed equalities,
  ordered plan↔rows, KEEP vs COPY, I1 chain State→retained State→Profile→KEEP Profile,
  provisional COPY-dest, retained inventory, `repinned` KEEP recheck, `capture_inputs`,
  canonical-bytes, reverify/close).
- Fresh renewal COPY is second generation `R/retained/before/<original-State-relative-path>`
  (sibling interfaces §8). `expected_dir` derivation from renewal Profile + inventory scope for
  `R/` + renewal retention verifier `verify_renewal_retention` are PROPOSED (Siblings C8) and
  UNIMPLEMENTED — blocker B-COPY (§8). Existing `verify_retention` is NEVER called as historian
  after a Core change (correct refusal); leaf reuses ONLY the mapping rule.

### 2.5 Seal / chain / anchor (low — structural only)

- `survey_publication_set_v2.py:480–542`: seal path must be `<P>/publication/publication-set.json`
  (old branch); proposal/staged/build refs must be the fixed `<P>/` paths (`:480–487`);
  roles must be EXACTLY the 15 names below with listed fixed paths for 10 roles (`:492–511`),
  semantic/visual reviews repo-contained (inside-only NOT required, `:512–526`), no duplicate
  role paths, staged trio must be exact `{main,bibliography,style}` (no `primary`/`staged_refs`
  alias), `set_sha256 == sha256_object(except self)` (`:463–468`).
- `PUBLICATION_ROLES_15` (exact, verified): `reader-input, authoring-input, source-receipt,
  reader-manuscript, validated-source, bibliography, style, publication-pdf, build-log,
  pdf-digest, quality-regression-bundle, semantic-review, visual-review, reader-surface-gate,
  publication-candidate`.
- Chain: `CHAIN_LIMIT 32` (`:109`), `_walk_chain_backwards:1023–1051`, anchor/sequence/time/cycle
  rules (`:1060–1230`), activation branch validation (`:1239–1314`), `_recompute_before_digest`
  + `_validate_proposal_retention_identity:1309–1420`, `before_candidate_ref` nullable-only-when-
  absent (`:1443–1462`), `VERSIONED_ACTIVE` selection + `require_active_or_canonical:2118+`
  + `resolve_publication_mode` (`:2093–2141`). Latest legacy immediately before FIRST versioned
  activation is the permanent anchor; never rolled forward; later legacy successor unsupported.

## 3. Bootstrap adapter vs steady-state (exact boundary)

### 3.1 Bootstrap (selected bounded compatibility — this renewal implementation only)

- Adds the strict branches WITHOUT changing old bytes: 4 new schemas
  (`VERSIONED_RENEWAL_BASIS_V1`, `VERSIONED_RENEWAL_SOURCE_PROOF_V1`, `VERSIONED_RENEWAL_SOURCE_V1`,
  `VERSIONED_RENEWAL_SET_V1` + `SEALED_INERT`) + activation branch
  (`VERSIONED_RENEWAL_ACTIVATION_V1` + `REVIEWED_VERSIONED_CORE_RENEWAL`) + U
  `renewal_source_proof_ref` context + C `renewal_source` branch + Candidate/QA/Gate/bundle
  proof branches + `renewal_receipt_ref` on Gate derivation (sibling interfaces §§3–5, C1/C2/C5
  carriers unclosed). Old schema/manifest/receipt/seal bytes stay verbatim (Astra R7).
- Explicitly registers its new schema/module closure and preserves legacy shapes (decision §2).
  This is a compatibility ADAPTER, not an assertion that old and new tool/schema bytes are equal.
- Recognized R3 inputs = EXACTLY §1.2 shapes. Unrecognized old shape (unknown schema version,
  unknown `code_deps` name, unknown style/recipe bytes, missing/foreign/ambiguous authority,
  dirty/untracked control roots, unavailable tool blobs, non-ancestor epoch, unsafe path,
  changed research/Profile) refuses BEFORE operation writes (`BASIS_ENTRY_INELIGIBLE` +
  specific `HISTORY_*/BASIS_*`).

### 3.2 Steady state (renewal-capable source → later committed change, same contract)

- Requires exact current closure membership + schema/contract equality APART FROM permitted
  implementation/style bytes. Runtime derives actual old/new tool commits + changed paths
  (prose alone insufficient). Artifact-only commits never qualify as Core renewal.
- Recognized same-contract style/rendering implementation changes are classified by actual
  source/target identity (U = exact-target reuse, C = new targets; same SHA at a different
  target path is STILL C). Executable tool versions may change for C under the SAME fixed
  recipe/specification; U retains the historical build unit (no new build).
- The following REFUSE and require a separate migration (never a renewal): research acceptance,
  Profile, Architecture, Draft authority, pipeline/quality semantic contract, review
  requirements, route family, build recipe SPECIFICATION changes; unsupported
  contract/recipe/schema migration; `CONTRACT_MISMATCH` / `CLOSURE_SET` /
  `CODE_DEPS_EXPANSION_REQUIRED` / `TOOL_DRIFT` / `STYLE_MISMATCH` / `REPLAY_MISMATCH`.
- Dirty/untracked control roots, unavailable historical blobs, non-ancestor epochs, unsafe paths,
  changed research/Profile, unrecognized old shapes refuse the same way in steady state as in
  bootstrap. No wildcard `scripts/**` historical exemption, no caller-supplied allowlist,
  no `implementation_sha` caller param, no ambient/global/cached authority.

## 4. Exact existing closures + proposed successor lists (finite; counts explicitly conditional)

### 4.1 Existing canonical22 (Weekly — verified present, 22/22)

`survey_weekly_derivation_v2.py:28–51 CURRENT_CLOSURE` (all exist; fresh subset §1.3):

```text
scripts/survey_weekly_derivation_v2.py
scripts/survey_weekly_semantic_publication_v2.py
scripts/survey_drafting_citation_refs_v2.py
scripts/survey_bibliography_access_provenance_v2.py
scripts/render_article_draft_tex.py
schemas/reader-surface-input-v2.schema.json
schemas/weekly-publication-source-manifest-v2.schema.json
templates/survey/jgaisurvey.sty
scripts/survey_publication_set_v2.py
scripts/survey_editorial_publication_v2.py
scripts/survey_editorial_current_authority_v2.py
schemas/editorial-publication-source-manifest-v2.schema.json
schemas/editorial-publication-set-v2.schema.json
schemas/editorial-publication-build-record-v2.schema.json
schemas/editorial-manuscript-spec-v2.schema.json
schemas/editorial-toolchain-spec-v2.schema.json
schemas/reader-manuscript-v2.schema.json
schemas/reader-surface-gate-v2.schema.json
schemas/publication-surface-revalidation.schema.json
schemas/quality-regression-bundle-v2.schema.json
schemas/publication-candidate-v2.schema.json
.latexmkrc
```

### 4.2 Existing canonical27 (Longform — verified present, 27/27)

`survey_longform_generated_v2.py:52–80 CURRENT_CLOSURE` (all exist):

```text
scripts/survey_longform_generated_v2.py
scripts/survey_longform_semantic_publication_v2.py
scripts/survey_longform_derivation_v2.py
scripts/survey_drafting_citation_refs_v2.py
scripts/survey_bibliography_access_provenance_v2.py
scripts/render_article_draft_tex.py
schemas/longform-reader-input-v2.schema.json
schemas/longform-publication-source-manifest-v2.schema.json
schemas/reader-surface-semantic-review-v2.schema.json
schemas/reader-surface-gate-v2.schema.json
scripts/survey_reader_surface_gate_v2.py
scripts/survey_production_v2.py
scripts/survey_schema_v2.py
templates/survey/jgaisurvey.sty
scripts/survey_publication_set_v2.py
scripts/survey_editorial_publication_v2.py
scripts/survey_editorial_current_authority_v2.py
schemas/editorial-publication-source-manifest-v2.schema.json
schemas/editorial-publication-set-v2.schema.json
schemas/editorial-publication-build-record-v2.schema.json
schemas/editorial-manuscript-spec-v2.schema.json
schemas/editorial-toolchain-spec-v2.schema.json
schemas/reader-manuscript-v2.schema.json
schemas/publication-surface-revalidation.schema.json
schemas/quality-regression-bundle-v2.schema.json
schemas/publication-candidate-v2.schema.json
.latexmkrc
```

### 4.3 Existing editorial/P3S50 (verified: 30 py + 14 schemas + 3 route + 1 staged + 1 style + 1 recipe)

`survey_editorial_staged_source_v2.py:92–140 _SHARED_PY/_SHARED_SCHEMAS` + `:143–201
_route_code_deps` (all 44 shared rows exist; route extras add 3; staged/style/recipe add 3):

- `_SHARED_PY` (30): `render_article_draft_tex`, `survey_agent_control_v2`,
  `survey_agent_tool_v2`, `survey_architecture_v2`, `survey_architecture_v2_base`,
  `survey_bibliography_access_provenance_v2`, `survey_completeness_v2`,
  `survey_drafting_citation_refs_v2`, `survey_drafting_v2`, `survey_drafting_v2_base`,
  `survey_editorial_correction_proposal_v2`, `survey_editorial_current_authority_v2`,
  `survey_editorial_publication_v2`, `survey_editorial_retention_v2`, `survey_evidence_v2`,
  `survey_longform_derivation_v2`, `survey_longform_generated_v2`, `survey_production_v2`,
  `survey_publication_set_v2`, `survey_publication_v2`, `survey_quality_v2`,
  `survey_reader_fidelity_v2`, `survey_reader_publication_v2`, `survey_reader_surface_gate_v2`,
  `survey_review_attention_v2`, `survey_schema_v2`, `survey_screening_v2`,
  `survey_weekly_derivation_v2`, `validate_article_draft`, `weekly_pipeline` (all
  `scripts/<name>.py`).
- `_SHARED_SCHEMAS` (14): `editorial-correction-proposal`, `editorial-manuscript-spec`,
  `editorial-publication-build-record`, `editorial-publication-set`,
  `editorial-publication-source-manifest`, `editorial-retention-manifest`,
  `editorial-staged-source-manifest`, `editorial-toolchain-spec`, `publication-candidate`,
  `publication-surface-revalidation`, `quality-regression-bundle`, `reader-manuscript`,
  `reader-surface-gate`, `reader-surface-semantic-review` (all
  `schemas/<name>.schema.json`).
- Route-3 per route: Weekly adds `reader-surface-input` + `weekly-publication-source-manifest`
  + `survey_weekly_semantic_publication_v2`; Longform adds `longform-reader-input` +
  `longform-publication-source-manifest` + `survey_longform_semantic_publication_v2`.
- Plus `STAGED_MODULE + STYLE_PATH + RECIPE_PATH` (3). Total `30+14+6 = 50`, gate `len==50`
  (`:162–167`) + AST edge audit `:172–201` (extra import → `CODE_DEPS_EXPANSION_REQUIRED`).

### 4.4 Proposed successor lists (EXPLICITLY CONDITIONAL — do NOT cite as fact)

Siblings fix module/function names but leave the FILE-count choice open (interfaces C1: in-place
amendment vs new schema files; C8: verifier placement; accepted file §5: 16 leaf twins INSIDE
the source module, +0 files). Until Astra selects C1–C8, there is NO single future exact count.
Finite options:

- New modules (FIXED names, decision §4): `scripts/survey_versioned_renewal_history_v2.py`,
  `scripts/survey_versioned_renewal_source_v2.py`, `scripts/survey_versioned_renewal_v2.py`
  (+0 test/doc/config files in this count; tests/registrations are separate additions).
- New schemas (FIXED kinds, carrier UNFIXED): `versioned-renewal-basis-v2`,
  `versioned-renewal-source-proof-v2`, `versioned-renewal-source-manifest-v2`,
  `versioned-renewal-publication-set-v2` (+ activation branch in
  `publication-surface-revalidation.schema.json` + old Candidate/QA/manuscript/Gate strict
  branches).
- Option N1 (new-files carrier, sibling PROPOSAL): successor P3S union = 50 + 3 modules + 4
  schemas = **57** (route-conditional 60 with route-3 counted once; canonical22 → 22+7=29
  IF all 7 renewal files join the Weekly control subset, canonical27 → 27+7=34 likewise —
  membership of renewal files in canonical subsets is ITSELF unclosed and must be fixed in
  pre-code; do NOT report 29/34 as fact).
- Option N2 (in-place carrier, alternative): successor P3S union = 50 + 3 modules + 0 new
  schema files (4 old files amended, `additionalProperties:false` preserved, old required
  lists unchanged) = **53** (canonical deltas likewise −4 vs N1).
- Leaf twins (16 NEW functions, all inside `survey_versioned_renewal_source_v2.py`, +0 files):
  `_load_basis_accepted_ref`, `load_renewal_accepted_authority`,
  `strict_evidence_sources_statefree`, `records_from_authorities_statefree`,
  `longform_records_statefree`, `validate_evidence_package_basis_statefree`,
  `validate_evidence_acceptance_statefree`, `validate_screening_package_basis_statefree`,
  `validate_screening_acceptance_statefree`, `validate_discovery_acceptance_statefree`,
  `validate_x_manifest_statefree`, `validate_materiality_ledger_statefree`,
  `validate_completeness_statefree`, `validate_edition_view(s)_acceptance_statefree`,
  `validate_supplement_statefree`, `validate_selection/architecture/matrix/approval_statefree`
  family (sibling accepted file §5; exact signatures there). Plus `verify_renewal_retention`
  (PROPOSED in history module, C8) + `verify_renewal_rerender_equality` + `derive_renewal_staged`
  (source/high, siblings §§6–7). None of these is a file-count increment beyond the 3 modules.
- Transitive import closure for the 3 new modules (derived from actual top-level + function-local
  edges + sibling bans; ALLOWED only): `core` (pure `load_json/sha256_*/repo_local_path/
  parse_instant/contract_identity` — NEVER `verify_state_basis/verify_state_semantics/
  repository_commit_sha`), `schema_gate` (`load_and_validate_json/validate_instance`),
  `citation_refs.refs`, `drafting.validate_synthesis_result/validate_draft_result`,
  `provenance.resolve_source_access_provenance`, pure token/URL/archive helpers, bounded
  `O_NOFOLLOW` readers with `_safe`-equivalent discipline; history additionally needs
  `retention` mapping helpers + `subprocess cat-file/merge-base` epoch probes (audit-only);
  high additionally needs `publication_set` low resolver (structural only), `publication`
  Candidate/seal builders, `quality.validate_checks` (supplied-only), `reader_surface_gate`
  derivation (proof-bound), `agent_control` State validator (high-side ONLY), `P2V` observer
  (high-side ONLY via lazy import, never in leaf/closure). BANNED transitives for leaf/history:
  `agent.validate_agent_state`, `resolve_checkpoint_artifact`, `current_stage_basis_override`,
  `verify_state_basis`, `observe_current/renewal_authority`, Reader/Gate/Candidate/seal/full
  receipt/P1/P2R/P3S (sibling accepted §§1.2/5 + interfaces §7).
- Old57 remains the FIXED input, NOT proof that all new imports are already in its closure
  (decision §8). Any actual extra import beyond the fixed 50 set MUST surface as
  `CODE_DEPS_EXPANSION_REQUIRED` / `CLOSURE_SET` / `CLOSURE_DRIFT`, never silent omit. There
  is NO 57-path budget for the successor; changes are justified only by the §8 map.

## 5. Mode, style/recipe, epoch, dirt, trust disciplines (actual-source)

### 5.1 Git tree modes vs physical permissions (no symlink / no unselected mode migration)

- Tracked-409 files: Git mode `100644` (from `git ls-files -s`; e.g. `.latexmkrc
  078cba92…`, `config/survey-production-v2.json cffe16fe…`,
  `scripts/survey_weekly_derivation_v2.py 6d14009c…`, `templates/survey/jgaisurvey.sty
  16c68ba2…`). Physical mode `0o664` (from `stat`; spot-checked §0). Manifest records the
  same pair (`git_mode 100644 / physical_mode 0o664`) for all 57 rows. Git-vs-physical
  difference is EXPECTED (workspace umask) and is NOT a mode change.
- 32 new (A) files: NO current index entry (`git ls-files -s -- <path>` empty); manifest
  `git_mode 100644` is the INTENDED post-commit mode, not a current tree fact. Mode-change
  detection (`diff --summary` mode-change + R1 `1099–1101` refuse) applies at commit/HEAD
  comparison time; current-eligibility checks must state mode discipline per §12.4 of sibling
  interfaces file. No symlink is present in the closure lists; any symlink (leaf, ancestor,
  or retained dest) refuses (`_safe` / `_safe_file` / `_lexical_rel` / `_check_ancestors_no_symlink`
  precedent). No unselected mode migration is permitted.

### 5.2 Style-vs-recipe specification predicate (exact)

- Style: `templates/survey/jgaisurvey.sty` bytes are a CLOSURE member (Weekly `:36`, Longform
  `:66` via `STYLE_PATH`, P3S `:159`). `validate_generated_closure` pins exact style bytes
  (`weekly:478–486`); staged replay refuses on `STYLE_MISMATCH` (`staged:2061/2072`,
  `TOOL_DRIFT :617`, `CODE_DEPS_MISMATCH :1052/1862`). U requires the CURRENT renderer/style
  to yield EXACTLY the old trio + complete reader (byte equality); mismatch →
  `REUSE_TARGET_MISMATCH`, never auto-convert to C.
- Recipe: `.latexmkrc` bytes are a CLOSURE member with `REQUIRED_RECIPE_MARKERS` +
  `FIXED_RECIPE_STEPS` + `EXPECTED_ARGV_LUALATEX_BIBER`
  (`survey_editorial_publication_v2.py:40/60–74/1207–1243/1311–1321/1395/1521–1525/1651/1902–1927`).
  Recipe file is live-rehashed (`recipe_ref`), markers enforced at PIN and BUILD, drift during
  build → `RECIPE_DRIFT` (preserved-incomplete). C `EXECUTED_BUILD` must run the FIXED recipe
  with explicitly selected executable + allowlisted env (no `GIT_*/PATH/PYTHONPATH`); failed
  build → no set. Recipe SPECIFICATION change (steps/markers/semantics) is a migration trigger
  (`UNSUPPORTED_MIGRATION`), never a renewal parameter. Same-trio/different-PDF (incl.
  metadata-only `CreationDate/Producer/ID` or `page_count` delta) is C, not U.

### 5.3 Old-tool own epoch (three separate fields — never substituted)

- Receipt `current_tools.repository_commit_sha` (40-hex, ancestor-of-HEAD check `:1136–1138`,
  `TOOLS_SHAPE :1091`, `CONTRACT_MISMATCH :1124`, head/closure/contract checks `:1088–1176`).
- Staged `producer_head` (`staged:1039`) — own epoch of the staged derivation; checked against
  fixed `code_deps` set + replay, not against receipt epoch.
- `before_state` / acceptance `state_sha256` values (historical values stay ORIGINAL; §11.3
  six-condition content-addressed exception only — sibling accepted §0 + interfaces §0 BINDING;
  NO package mutation, NO original-`state_path`-vs-retained-dest compare).
- Where dependency rows overlap, epochs must agree; otherwise `HISTORY_TOOL_EPOCH_DRIFT`.
  Recorded historical hashes are never accepted merely because a receipt lists them; historical
  schemas are supported by the finite adapter + epoch cross-check, never by executing arbitrary
  historical schema code or remote `$ref`.

### 5.4 Dirty/untracked control roots + inventory controls

- Reconstruct root at task start: clean (`status --porcelain normal` empty per packet; task
  premise `ce0de1a` clean). Proof-copy is dirty BY DESIGN (25M+32A applied overlay; index
  clean, worktree delta 57). Dirty/untracked CONTROL roots
  (`implementation_control_roots: ["config","schemas","scripts",".github/workflows"]` +
  `contract_files.pipeline[67]+quality[3]` from `config/survey-production-v2.json:6/92`,
  verified fresh §0) refuse entry (`BASIS_ENTRY_INELIGIBLE`); clean roots + expected membership
  + current contract/tool checks are HIGH predicates, never leaf predicates.
- Exclusive inventory: writer-owned paths under `R/` claimed with `O_CREAT|O_EXCL|O_NOFOLLOW`
  (`TARGET_EXISTS`/`PUBLICATION_EXISTS` precedents
  `survey_editorial_publication_v2.py:493/1577/1617/1627/2138/2221/2267/2317/3152/3387/3545`);
  supplied QA/review files are pinned read-only inputs with exact dependency manifest
  (`path/hash/size/type`, directory inventories, before/after rechecks), never writer-owned,
  never deleted/rewritten; writer-owned paths cannot alias supplied paths; incomplete `R`
  stays inert, retry uses a new id; no same-byte takeover or foreign/unknown cleanup.

### 5.5 No wildcard trust (exact)

No `scripts/**` historical exemption, no caller-supplied compatibility allowlist, no
`pending_basis` / `already_verified` / verified-dict / `seal_path` shortcut / route/kind enum
from caller / ambient/global/cached authority / `implementation_sha` caller param. Every
path/ref is lexical-first (`_lexical_rel`), `_safe` no-follow, bounded read, strict JSON
(duplicate-key refusal), CURRENT-disk schema validation for E docs, self-digest recompute,
live SHA/size recheck, cross-binding (`_check_doc_refs_against_seal` discipline: only
seal-bound refs compared), pin recheck after work. Same-SHA different-path refused everywhere.

## 6. Concrete import/call DAG (actual edges + new layering; lifecycle-dependent calls marked *)

```text
prior history + fresh before-State/selection + unchanged accepted inputs
 → [_observe_renewal_entry] HIGH private, no basis yet; in-memory pins only
    reads: canonical State + profile_ref + checkpoint provenance + prior seal/receipt/
           staged/retention/scope refs + current nonpublication authority + current
           closure/contract/HEAD (actual: agent_control.validate_agent_state:498/503,
           core.verify_state_basis:959–996, weekly.verify_tool_basis:591–787,
           longform-generated.verify_tool_basis:558–616)
 → [prepare_renewal] HIGH capture; owns exclusive R + COPY + inventory; writes basis LAST;
    rechecks entry pins (actual: retention.capture_retention:857+ with P1 lazy import:859;
    P1._before_graph:687–1470 + _retention_rows:1472–1549; O_EXCL claim precedents §5.4)
 → [observe_renewal_authority] HIGH basis-bound; after basis, before finalize,
    immediately before activate; reopens + compares ALL inputs; demands live State ==
    fresh before ref (actual: P2V observe_current_authority:10 observer as TEMPLATE ONLY —
    renewal op is NEW, P2V_AFTER_ACTIVATION_REFUSED:197 proves detached need)
 → [validate_renewal_basis + load_renewal_accepted_authority] SOURCE leaf, by persisted
    basis_path; NO State object / NO implementation_sha / NO verified-records param
    reads ONLY basis-pinned {path,sha256[,byte_count]} refs; MAY read PRIOR seals/records
    as typed history, NEVER the new seal/activation (decision §4 bans)
    actual pure callees: core.load_json/sha256_*/repo_local_path/parse_instant (NEVER
      verify_state_basis/repository_commit_sha), schema_gate.load_and_validate_json,
      citation_refs.refs, drafting.validate_synthesis/draft_result (prompt SHA = current
      disk file), provenance.resolve_source_access_provenance, discovery/screening/evidence
      State-free twins (§5 of sibling accepted file); BANNED: agent.validate_agent_state,
      resolve_checkpoint_artifact, current_stage_basis_override:122–143, _canonical_root_acceptance
      State branch:325–350, resolve_active_screening_acceptance:442–489, Reader/Gate/Candidate/
      seal/P1/P2R/P3S/full receipt (* lifecycle recursion cut here — see below)
 → [current projection/render comparison] pure AFTER all authority checks:
    weekly.build_reader_input:300–394 + validate_reader_input:397–407 + render_main:414–456 +
    render_bibliography:459–475 + validate_generated_closure:478–486; longform
    build_longform_reader_input:608–926 + validate:927–948 + canonical_reader_bytes:949–956 +
    _validate_archive_authorization:530–581 + _preflight_evidence_tree:365–419
 → [source proof] SOURCE; U-only old manuscript/build-unit refs OR C-only new trio refs;
    comparison {reader_equal,trio_equal,disposition} VALIDATED (U mismatch →
    REUSE_TARGET_MISMATCH, no auto-C)
 → [derive_renewal_staged] C ONLY; R/staged-source/{main.tex,references.bib,jgaisurvey.sty,
    staged-source-manifest.json}; old closed4 untouched (actual: P3S materialize:867 lazy P2V
    import + verify_staged_source:1772 replay as TEMPLATE)
 → [C manuscript (renewal_source branch) + real disposable build/transfer] C ONLY;
    independently preparable AFTER proof, BOTH BEFORE external review; auxiliaries disposable
    (actual: editorial_publication FIXED_RECIPE_STEPS/REQUIRED_RECIPE_MARKERS/toolchain checks
    :60–74/1183–1244/1311–1525 as TEMPLATE)
 → [build-record] variant-tagged; REUSED_BUILD (U: original record/PDF/log/digest refs +
    renewal_tools{old,new} + no_rebuild, NO toolchain spawn) OR EXECUTED_BUILD (C: declared
    inputs + fixed recipe + toolchain{executable,versions,argv,env} + outputs + exit_code 0);
    receipt binds build-record, NEVER precedes it (corrects illustrative remedy)
 → [renewal receipt] validated-source-manifest; binds proof+build+retained COPY
 → [externally supplied fresh QA + new QA bundle + new postrender reviews (C ONLY; U derives
    predecessor RECORD refs)] validator executes NOTHING: quality.validate_checks:132–174
    validates SUPPLIED rows only (actual, verified)
 → [new Gate] proof+receipt-bound derivation, NO inferred P/publication/ receipt path (actual:
    _derivation_for_manuscript:1145–1330 4-way dispatch; editorial branch live
    verify_staged_source:1173 + fixed receipt path:1182–1185 is the OLD path being replaced)
 → [new Candidate] nested manuscript/reviews/bundle bindings + renewal_source_proof_ref branch
    (actual: build_candidate:668–746 digest 9 keys:730–741; validate_candidate:749–814 10-key
    recompute:753–766 + cross-bindings:769–811; manuscript digest 14 keys + editorial_source?
    :427–448; bundle digest 9 keys:224/259–263)
 → [seal] R/publication-set.json; 15 roles + proof/basis/receipt refs; seal LAST
    (actual: low validate_seal:460 CURRENT-disk schemas + roles:492–511 + staged trio:535–542)
 → [validate_prepared_renewal_set] strict State + closure/replay + manuscript/bundle/reviews/
    Gate/Candidate/build/PDF/log/digest/current-research + cross-refs + closed inventory
 → [activate_renewal] explicit; full current-before + full leaf revalidation; exclusive new
    record; known-byte State temp/replace on publication_revalidation_provenance ONLY
    (actual: activate:3155/resume:3643/verify_history:3782 + INTENT_COLLISION:3152 +
    RECORD_COLLISION:3387/3545 + post-State VERSIONED_ACTIVE readback:3611–3616/3765–3766 as TEMPLATES)
 → [full new active readback] current-before vs retained-before + selected Candidate/digest agree
 → [normal active Candidate → direct stage → synthetic Preview/Freeze/Release]
```

State-lifecycle recursion that the layering cuts (verified actual edges):
`State→Candidate→Reader→State` would recurse if leaf called `agent.validate_agent_state`
(`agent_control:498/503` → `verify_state_basis production:959–996` → checkpoint/pending-basis
`agent:382–996`) or `resolve_active_screening_acceptance (screening:442–489)` or
`current_stage_basis_override (agent_tool:122–143)` or full `Reader/Gate/Candidate`
(`reader:237–247 verify_staged_source`, `gate:1173–1177`, `publication:668–814`). The leaf calls
NONE of these (*); low resolver hashes + cross-binds ONLY (* never full semantics);
HIGH owns all live-State/HEAD/commit/closure/contract predicates (*); HIST owns epoch blobs
(*); detached readback validates RETAINED before-State only (*).

## 7. Normal consumer inventory (renewal-aware or explicit revised-mode refusal — same unit)

| Consumer (actual path) | Current behavior (verified) | Renewal requirement (decision §8) |
|---|---|---|
| `survey_editorial_correction_proposal_v2.py` (P1) | `validate_proposal:2188`, `_before_graph:687–1470`, `_active_effective:467–538`, `VERSIONED_ACTIVE` map `:470–538/732/1023–1029`, `NO_EDITORIAL_CHANGE:1640–1670`, `VERSIONED_MAP_SHAPE:485/487` | Renewal-aware before-graph + receipt dispatch + dependency/history mapping so renewed active set supports later changed-reader editorial; KEEP prior immutable versions, COPY fresh State; P1 identical-reader refusal + `NO_EDITORIAL_CHANGE` preserved; renewal NEVER mints P1 same-reader proposal |
| `survey_editorial_retention_v2.py` (P2R) | `capture_retention:857+`, `verify_retention:1737–2086`, `_expected_retained_dest:831`, `_retained_expected_sets:835`, I1 chain State→retained→Profile→KEEP | Existing roots unchanged; NEW `verify_renewal_retention` in history module for `R/retained/before/` (C8 PROPOSED, §8 blocker); current `verify_retention` NEVER called as historian after Core change |
| `survey_editorial_current_authority_v2.py` (P2V) | `observe_current_authority:10` + `P2V_AFTER_ACTIVATION_REFUSED:197`, 3-way comparison (current vs proposal / retained / entry-to-final) | Original entry correctly refuses after activation; NEW high `observe_renewal_authority` + `_observe_renewal_entry` basis-bound observation (sibling interfaces §6); leaf ungated until HIGH exists (§8 blocker) |
| `survey_editorial_staged_source_v2.py` (P3S) | `materialize:867` (lazy P2V inside invocation) + `verify_staged_source:1772` standalone replay + `_route_code_deps:143–201` fixed-50 + `CODE_DEPS_MISMATCH/TOOL_DRIFT/STYLE_MISMATCH` | Unchanged for old paths; renewal uses source proof (NOT forged P3S manifest at renewal path); C staged derivation is NEW wiring (§8 blocker); U historical identity + current semantics/trio against new proof via reloadable `renewal_source_proof_ref` context, standalone legacy path keeps P3S refusal |
| Editorial high `survey_editorial_publication_v2.py` | `prepare:1552/finalize:2013/validate_receipt:692/validate_set:2555/activate:3155/resume:3643/history:3782`, `_fail:181–191`, CLI `:3837–3917` exits `:3914–3917`, `P2V_MISSING:622/STAGED_MISSING:668`, closure `:1958–2010`, recipe/toolchain `:1183–1525`, `INTENT_COLLISION:3152`, `VERSIONED_ACTIVE` guards `:3217/3293/3611/3765` | Renewal-aware (new high module `survey_versioned_renewal_v2.py` with `prepare/finalize/validate-receipt/validate-set/activate/resume/history` + `toolchain None` for U + explicit spec for C); existing R1/canonical writers keep pre-write refusal in versioned mode (`weekly_mechanical_refresh:837`, `agent_control:2210–2229`) |
| `survey_publication_set_v2.py` (low) | Structural-only seal/chain/selection (`:445–454` docstring), `before_active_digest:353–415`, chain `:1023–1230`, activation `:1239–1314`, `CHAN_LIMIT 32:109`, `require_active_or_canonical:2118`, `resolve_publication_mode:2093`, `VERSIONED_ACTIVE:1970/2008/2042/2082` | New strict `VERSIONED_RENEWAL_*` kind/set parsing + typed historical predecessor + chain/anchor/before-digest + low role/proof projection; low hashes + cross-binds ONLY, never full Reader/Gate/source semantics |
| Reader/manuscript `survey_reader_publication_v2.py:218–270/347–451/601–692` | `editorial_source` unconditional live `verify_staged_source:237–247` + trio main→primary mapping `:253–269` + digest 14 keys `:427–448` | U explicit `renewal_source_proof_ref` context (historical identity + all current semantics/trio); C mutually exclusive `renewal_source` branch; nested review threading `validate_review_record:643–647`; old bytes never edited; digest present-included rule (sibling interfaces §5) |
| Gate `survey_reader_surface_gate_v2.py:1145–1330/1333–1769/1893+` | 4-variant `oneOf:160–217`, `_derivation_for_manuscript` dispatch, Gate digest 13 keys `:1650–1681/1737–1753`, receipt inference `:1182–1185` | New proof+receipt-bound derivation (`renewal_source_proof_ref` + `renewal_receipt_ref`); no inferred old receipt path (sibling C2 variant-name choice OPEN) |
| QA `survey_quality_v2.py:132–274` | `validate_checks` + `build_bundle:193–229` digest 9 keys `:224` + `validate_bundle:232–274` 9-key `:259–263` | Proof binding + digest + exact fresh supplied-result/PDF checks; validator executes nothing (preserved) |
| Candidate/publication `survey_publication_v2.py:171–390/668–814` | `validate_candidate` 10-key digest + cross-bindings, `_prepare_freeze_inputs:171–245` (Candidate+approval+VISUAL+bundle+Profile+snapshot `:213–229`), `_recheck_snapshot:248–256`, `_preflight_freeze_pair:323+` overlap/alias `:347–390` | Proof derived from validated Candidate, passed to direct review loader, bundle equality; snapshot + preflight cover proof/basis/retained COPY/current closure/all reachable evidence deduped by exact path/hash (sibling interfaces §10; snapshot file list OPEN) |
| Stage/agent Preview/production/profiled Freeze | `_require_active_candidate_binding:73–100` (`survey_stage_validation_v2.py`), `VERSIONED_ACTIVE` guards in orchestrator `:169–234`/human-gate `:266–280`/handoff `:131–142`/profiled-freeze `:48`/production `:63` | Select exact active Candidate/proof via sole State; full normal validations; Profile-bound canonical Freeze/Manifest conventions; producer AND loader recompute selected paths + hash compare; unsupported handoff explicitly refused (`handoff:101–102` basis-preemption is NOT stage coverage) |
| Orchestrator/handoff/human-gate/handlers/export/release | `survey_orchestrator_v2.py`, `survey_handoff_v2.py`, `survey_human_gate_v2.py`, `survey_handlers_v2.py`, export-preview workflow (M `survey-production-v2-export-publication-preview.yml`), build workflows (M `build-weekly-survey/build-special-pdf.yml`) | Producer AND loader recompute selected paths + compare hashes; no fallback to canonical Candidate; no Production Actions execution in development (`handoff_required:false` preserved); export/release recognize State-selected renewal, preserve inert-set nonadoption + ordinary direct workflow |
| Config/docs/closures | `config/survey-production-v2.json` (control roots + 67 pipeline + 3 quality contract files), `survey_schema_v2.py` strict duplicate-key gate, `test_group_c_editorial_consumers_v2.py:119–121` (`_SHARED_PY==30/_SHARED_SCHEMAS==14` gate) | Register ALL new modules/schemas + transitive extracted helpers in contract/control lists + canonical22/27 + editorial/P3S50 successors with ACTUAL new counts/sets (Option N1 vs N2, §4.4); no literal-50 retention, no prefix widening |
| R1/canonical/revision/canonical-build | `survey_weekly_mechanical_refresh_v2.py:52–54/828–833` + `survey_agent_control_v2.py:2210–2229` | Existing versioned refusal MAINTAINED including renewal kind; no false editorial/Core routing |

Repeat renewal + renewal→editorial are MANDATORY same-unit capability tests (repeat needs another
genuine eligible Core change + fresh basis; retry of exact active record is readonly
`ALREADY_ACTIVE`; renewal→editorial is P1 repeated pre-Preview with prior KEEP + fresh COPY +
true-repeat P2V on the NEW pointer; R1×2→editorial→renewal anchor preserved), NOT claims that
existing P1/P2R already support the new kind.

## 8. Discrepancies with siblings = BLOCKERS (finite gate-ready options; no silent adoption)

- **B-SCHEMA-CARRIER (sibling C1 — UNLOSED choice).** Interfaces file proposes in-place amendment
  of 4 old schema files with strict optional `renewal_source_proof_ref` (+ Gate
  `renewal_receipt_ref`), rejects new-file fork. Root has NOT selected. IMPACT: successor file
  count is N1=57 vs N2=53 (§4.4); closure registration + `contract_files` deltas differ.
  OPTIONS: (O1a) Astra selects in-place → this file's N2 binds, old required lists unchanged;
  (O1b) Astra selects new files → N1 binds, validator dispatch fork reviewed. Either way digest
  present-included rule is unchanged. Implementation BLOCKED until selected.
- **B-GATE-VARIANT (C2 — UNLOSED).** Proposed U keeps `EDITORIAL_PUBLICATION_V1 /
  EDITORIAL_MAIN_BIB_STYLE` + proof context, C adds `VERSIONED_RENEWAL_V1 /
  RENEWAL_MAIN_BIB_STYLE`. Unselected. OPTIONS: select as-proposed (honest reuse vs visible new)
  or rename; C reuse of `EDITORIAL_*` is REJECTED (review-target confusion).
- **B-FREEZE-THREAD (C3 + O-B2 — UNLOSED mechanics).** Proposed: NO signature change to
  `_prepare_freeze_inputs(repo_root, candidate_path, approval_path)`; renewal derives proof FROM
  validated Candidate, threads explicitly to direct `validate_review_record(...,
  renewal_source_proof_ref=...)`, extends snapshot/alias sets; wrapper with optional
  expected-proof param ONLY for active-selection callers. Exact snapshot file list
  (proof/basis/retained COPY/current closure/all reachable evidence deduped) + recheck-stage
  wiring remain OPEN. OPTIONS: accept C3 proposal or fix alternative threading; snapshot list
  must be enumerated before code.
- **B-BEFORE-DIGEST (C4 — UNLOSED payload).** Proposed: recompute from RETAINED before-effective7
  (old active set at `before_state_ref`) + observed before-Candidate, NOT from new `R/` roles;
  new refs covered by `set_ref`/`renewal_basis_ref`/`renewal_proof_ref`. Unselected. OPTIONS:
  accept or correct; low invariant (before-context measure) must hold either way.
- **B-RECEIPT-KIND (C5 — UNLOSED).** Proposed: NEW kind `VERSIONED_RENEWAL_SOURCE_V1` at same
  filename `R/validated-source-manifest.json` (NOT relaxed old `<P>/` path, NOT reused editorial
  kind). Unselected. OPTIONS: accept new kind (prevents stale-validator acceptance) or define
  alternative kind routing; reuse of `EDITORIAL_PUBLICATION_SOURCE_V1` at `R/` is REJECTED.
- **B-ROLE-PATHS (C6 — UNLOSED but bounded).** Proposed: seal role `path` = ACTUAL file locations
  (U: manuscript/trio/build3/reviews = ORIGINAL `P/` paths; receipt/bundle/Gate/Candidate = NEW
  `R/` paths; C: reader/authoring/retention/scope-history = ORIGINAL, rest NEW) + low namespace
  check extended (`proposal_ref` stays `P/proposal.json`, set path `R/publication-set.json`, no
  inferred `P/publication/` prefix for renewal roles). Copy-old-targets-into-`R/` is FORBIDDEN
  (same-SHA different-path refused). OPTIONS: accept or correct path table; no third option
  (copying old bytes to `R/` violates U identity).
- **B-CLI-REASON (C7 — rule stated, enforcement OPEN).** Proposed: `activate --reason` takes
  free-text Core-change reason, `reason_class` FIXED by kind branch, no `--reason-class` flag.
  CLI non-empty/truthful-wording check is review-based, not regex. Pre-code must fix the exact
  refusal when a false-editorial reason is supplied (`UNSUPPORTED_MIGRATION` vs
  `REVIEW_TARGET_MISMATCH` mapping per seam).
- **B-COPY-LAYOUT (C8 + predicate-map §4.1 — UNNAMED).** Fresh `R/retained/before/` second-generation
  dest layout, `expected_dir` derivation from renewal Profile, inventory scope for `R/`, and
  `verify_renewal_retention` owner are PROPOSED (history module, called by
  `validate_renewal_basis` + high observation) but have NO code. Leaf assumes
  `basis.before_state_ref` + retained-COPY binding; if they cannot be fixed without
  basename/current-State shortcut → precise NO-GO (decision §9 stop rule).
- **B-P2V-RENEWAL (predicate-map §4.2).** No renewal-aware `observe_renewal_authority` entry
  exists yet. Leaf is ungated until HIGH exists; if HIGH cannot check current nonpublication
  authority without consuming leaf proof (cycle) → NO-GO.
- **B-RENDERER-U / B-STAGED-C (predicate-map §4.3–4.4).** U renderer-equality runner
  (`verify_renewal_rerender_equality`, disposable-temp trio + complete reader, `RERENDER_MISMATCH`
  refusal, no auto-C) + C staged-derivation wiring (`derive_renewal_staged`, new trio/manifest
  under `R/staged-source/`, `renewal_source` branch, proof-as-staged-proof) are NAMED but have
  NO code. If U equality cannot be byte-exact without semantic weakening → NO-GO.
- **B-F3/F4 WORDING (CORRECTED, needs Astra confirm).** Old predicate-map F3/F4
  "retained-COPY equality" (`package.basis.state_sha256 == sha256(retained)` AND `state_path ==
  retained_dest`) is SUPERSEDED by decision §11.3 + both final addenda + sibling accepted §0 +
  sibling interfaces §0 (historical SHA stays original; 6-condition content-addressed rule; same
  canonical SOURCE path; NO package mutation; NO original-`state_path`-vs-retained-dest compare).
  Technical addendum §67 shorthand must be read under §11.3, never as retained-COPY equality.
  OPTIONS: Astra confirms §0 wording as binding pre-code rule (RECOMMENDED), or issues corrected
  wording; any weakening (hash-only, package mutation, arbitrary substitution) → NO-GO.
- **B-CLOSURE-COUNT (this file — UNFIXED by siblings).** Neither sibling fixes successor
  canonical22/27 counts (renewal-file membership in canonical subsets unclosed) nor the
  N1-vs-N2 total. This file returns BOTH options (§4.4) and explicitly does NOT report a
  future exact count as fact. OPTIONS: Astra selects N1+N-subset or N2+N-subset with exact
  per-route member lists; no code until then.
- NO-GO criteria (any one fires → blocked, contract revision or migration decision, never a
  weakened checker): a §2 RC predicate dropped or replaced by SHA-only acceptance; §0 F3/F4
  correction violated; leaf/history/high bans violated (State→Candidate→Reader→proof recursion);
  DM-class change treated as U reuse or generic pending bypass; old review targets rewritten;
  same-SHA different-path/target accepted as U; C without real build + new postrender reviews;
  synthetic approval promoted to genuine; same-byte takeover / foreign cleanup / retrospective
  PASS / genuine-approval laundering.

## 9. Gate-ready checklist (this file) + stop rule

- [x] Exact current old-format fingerprints: 57-path manifest index (§1.1, adopted pins) + R3
      recognized-shape list (§1.2) + fresh closure-subset rehash (§1.3, coverage-limited) with
      patch digest/size match + 25M/32A + 0-staged recount + manifest-A-vs-index distinction.
- [x] Historical E/T/capture-graph role/schema/epoch maps (§2) grounded in actual P1 graph
      (`955–958` tool edges, `_pol 783–791`), retention layout (`831–854`), seal 15 roles +
      fixed paths (`480–542`), chain/anchor/mode rules, three-epoch separation.
- [x] Bootstrap vs steady-state boundary (§3): finite adapter scope, no-wildcard/no-allowlist
      rules, U/C byte-identity classification, DM migration triggers, style-vs-recipe predicate.
- [x] Exact existing canonical22/27/P3S50 lists (§4.1–4.3, all-exist verified) + CONDITIONAL
      proposed successor lists with transitive import deps (§4.4, N1 vs N2 + 16 leaf twins + C8
      verifier; no false exact-count claim).
- [x] Git-modes vs physical-permissions (§5.1), style-vs-recipe predicate (§5.2), old-tool own
      epoch (§5.3), dirty/untracked controls (§5.4), no-wildcard trust (§5.5).
- [x] Concrete import/call DAG with lifecycle-recursion cut + low/history/leaf/high layering
      (§6, actual `file:line` edges + `*` lifecycle marks + new-function names).
- [x] Normal consumer inventory with P1/P2R/P2V/P3S renewed-before→editorial mapping, Freeze
      snapshot/alias coverage, export workflows, refusal paths (§7).
- [x] Sibling discrepancies as finite blockers with gate-ready options (§8, B-carrier through
      B-closure-count + NO-GO criteria).
- [ ] Sibling halves (predicate bodies, schema field text, oracles): REFERENCED, not duplicated.
- [ ] Astra confirmation of THIS file + both siblings: OPEN (implementation BLOCKED per
      decision §§9/11.3 until all three are confirmed).

**Stop rule:** if any §8 blocker cannot close without weakening a predicate (hash-only
acceptance, dropped coverage, broad `pending`, caller verified dict, ambient proof, same-byte
takeover, retrospective PASS, genuine-approval laundering), return the precise contract issue or
NO-GO plus a migration/separate-contract decision — never a weakened checker. Whole NOT_READY /
step4B3 OPEN / audit unstarted / DM021+022 OPEN. Production semantic NO-GO on placeholder
editions. Stop at internal return; no code, no ordinary Commit/Push (Human-owned).

(End — author-side pre-code fingerprints/closures/consumers; no independence claim; no runtime
evidence; read-only standardlib hash + `git ls-tree`/AST inspection only.)
