# Versioned same-reader renewal — integrated pre-code R3 (author-side, single consistent map)

2026-10-23 JST. Fresh AUTHOR-side integration worker, NOT independent review.
Human HEAD at read time `ce0de1a` lineage (root observed `main...origin/main` clean at task start).
Governing: `outputs/rephase-1-versioned-renewal-contract-decision.md` SHA256
`478f00510791b76af24aa7d61f398f0608f7ad8ae7808008c660f2bea6fbfdcf` INCLUDING §11;
mandatory `notes/rephase-1-versioned-renewal-contract/astra-review-resolution.md` (R1–R8);
BOTH independent design reviews WITH final-binding addenda;
author inventory `notes/rephase-1-versioned-renewal-contract/accepted-authority-predicate-map.md` (F1–F8);
R2 pre-code returns in this packet (`interfaces-schemas-digests-r2.md` 627 lines,
`accepted-authority-readiness-r2.md` 462 lines, `fingerprints-closures-consumers-r2.md` 421 lines
+ twin `.json`, `operation-oracles.md` + §8 R2 corrections);
independent gate review `independent-readiness-review.md` (CHANGES_REQUIRED/NOT READY, §§1–12).
Read-only source: `.rephase-1-editorial-runtime/final-source-packaging/proof-copy/candidate-partial-b40de60`
(actual409/tree8ce + intended57, applied state). No source edits/runtime code/imports/tests/build/
fixture/restore/network/Git writes. This file `integrated-precode-r3.md` (+ optional twin
`integrated-precode-r3.json`) is the ONLY write in this unit. All R1/R2/contract/resolution/review
files preserved unchanged. Every R1/R2 occurrence contradicted below is superseded explicitly;
silence is not supersession. No `apply_patch`/shell file writes used for source.

Method: `Read` + read-only `bash` (`sha256sum`/`grep`/`stat`/`git ls-files -s` where available,
`python3 -c` stdlib `json`/`ast`/`pathlib` file reads, NO project imports, NO repo-code execution).
AST data parse allowed; no project import executed. All `PC` line citations verified 2026-10-23
in this unit or adopted from R2 with explicit re-verification noted.

## 0. Verdict, binding choices, and what R3 is

**Status: MAP-COMPLETE, READY-FOR-ROOT-GATE. NOT self-certified GO. Implementation remains BLOCKED
until Astra confirms this R3 jointly per decision §§9/11.3. No conditional-GO, no
"implementer delivers map after code".** R3 replaces the three R2 maps jointly with ONE internally
consistent map. All independent-review §§1–12 checklist items are closed as MAP (concrete
names/lists/expressions/pins/proofs); code/tests/build remain unstarted and unclaimed. If any
§12 item below cannot be built without weakening, the outcome is the listed precise NO-GO,
never a weakened checker. Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN.
Production semantic NO-GO on placeholder editions; synthetic approvals labelled.

Root-fixed bindings (no reopening, applied throughout):

- 3 NEW modules (fixed names): `scripts/survey_versioned_renewal_history_v2.py`
  (`verify_versioned_history` + `verify_renewal_retention` typed E/T readers),
  `scripts/survey_versioned_renewal_source_v2.py` (session constructor + Layer-A/B orchestration +
  `validate_renewal_basis` + `verify_renewal_source_proof`, NO validator bodies),
  `scripts/survey_versioned_renewal_v2.py` (`prepare/finalize/validate-receipt/validate-set/
  activate/resume/history` + CLI).
- 4 NEW schemas (new paths): `versioned-renewal-basis-v2.schema.json`,
  `versioned-renewal-source-proof-v2.schema.json`, `versioned-renewal-source-manifest-v2.schema.json`,
  `versioned-renewal-publication-set-v2.schema.json` (+ `R/build-record.json` variant tags in-file).
- 5 EXISTING schemas amended (branches only, §1): `reader-manuscript-v2`,
  `publication-candidate-v2`, `quality-regression-bundle-v2`, `reader-surface-gate-v2`,
  `publication-surface-revalidation`. All other existing branches/digest behavior preserved verbatim;
  legacy branch never amended. ONE new Gate derivation `VERSIONED_RENEWAL_V1` for BOTH U and C;
  4 old Gate variants verbatim, never augmented.
- Predecessor MUST be an existing versioned active set (editorial activation or prior renewal
  activation) with live seal + live record + live Candidate, all REQUIRED nonnull. Legacy-only
  (`REVIEWED_CORE_CHANGE` without separate activation record) is UNSUPPORTED. Renewal ONLY after
  versioned; no canonical install. U targets are derived exact roles of the immediate selected
  predecessor (could be C at prior `R/` paths), never fallback to original `P/`. Same original
  reader/authoring path preserved through renewal until a new editorial creates a new `P`.
- Historical build-unit resolution is typed `REUSED_BUILD` chain: U `REUSED_BUILD` refs the immediate
  prior build record (which may itself be a prior `R/EXECUTED_BUILD` or a prior `R/REUSED_BUILD`
  chaining to the old R3 `EXECUTED_BUILD`), with bounded consistent refs (§2). No invented C P3S
  manifest; proof IS the staged proof; C manuscript `renewal_source` is exactly
  `{path,sha256}=R/renewal-source-proof.json` (one ref, XOR with `editorial_source`).
- History predecessor union is `R3_EDITORIAL` (prior seal refs `P/publication/publication-set.json` +
  `P/publication/validated-source-manifest.json` + `P/staged-source/staged-source-manifest.json`)
  vs `VERSIONED_RENEWAL` (prior seal refs prior `R/publication-set.json` + prior
  `R/renewal-source-proof.json` + prior `R/renewal-basis.json`); own epochs derived from actual
  prior record/receipt/staged (`receipt_epoch`/`staged_producer_head`/per-schema epochs) OR
  proof→basis `current_tool_epoch` as CURRENT epoch for renewal predecessors; never assume each
  renewal owns an old P3S staged manifest. Historian traverses EVERY predecessor typed chain with
  recorded real epoch sources; old-schema validation fingerprint/epoch map per exact type+path (§2).
  E docs live/COPY (never required at tool commit); T at own source commit mandatory EVERY
  operation/proof readback, not audit-only (§§2/6/9). Unknown schema/epoch/ref → refuse
  (`HISTORY_BLOB_MISSING`/`HISTORY_TOOL_EPOCH_DRIFT`/`UNSUPPORTED_MIGRATION`), never forged.
- Full detached proof CURRENT tool closure/runtime/import/schema check on EVERY readback, no current
  State; accepted-content subloader (Layer-A) no-Git separate (§§8–9). No recursive current validation
  of ancestor proof stale after epoch change: ancestor uses HIST structural branch only.
- Shared pure primitives live in existing family modules with current wrappers unchanged; new helper
  holds NO public verified-dict token (§8). Supplemental checkpoint-graph dependencies derive exact
  retained-State→wrapper→typed-row; basis accepted name-map never trusted without that binding (§8).
  Same accepted-State historical SHA exception is EXACTLY decision §11.3 (do NOT alter result basis);
  helper context needs `basis_path` or internally constructed same-invocation private session,
  no ambient basis (§8).
- Successor closure per route is 63 = shared35(py) + schema22 + route3 + staged1 + style1 + recipe1
  (§6), NOT 59. All validated research schema/config/prompt dependencies explicitly enumerated,
  split runtime `code_deps` vs content `contract` so the verifier binds every file. Pipeline registry
  delta is ONLY +4 new schemas (67→71), no `.py` (control-roots already cover `scripts/`), preserving
  steady-state code-only change eligibility. Legacy never in required canonical changes; unknown
  schema/recipe contract modification → `UNSUPPORTED_MIGRATION`.
- U-after-C, C-after-U, repeat, renewal→editorial, fresh bootstrap with Profile unchanged and normal
  strict State/Candidate/Freeze/Release explicit calls are MANDATORY same-unit capability tests (§11).
  Freeze is a typed exact snapshot membership function including roots and schema/tool/evidence refs,
  no generic dictionary walker, with alias checks (§10). Toolchain fields are exact current high/schema
  fields (no `object-exact-map` placeholders); digests use actual key sets; arrays use canonical order
  = exact SOURCE order for writer bytes with sorted-set `_norm` equality for comparison — never both
  "stored sorted AND byte-verbatim" contradiction (§§1/5/10). CLI/fault map enumerated (§11).

Supersession: R2-A §8 (1-file branch) superseded by §1 (5-file); R2-I §§2.1–2.2 P-literals superseded
by §§2–3 (conditional epochs + prior-relative U); R2-I §2.1 `schema_epochs` SHA-only superseded by §4;
R2-I §2.1 `authoring_refs` sorted-example superseded by §5; R2-F §4.5 `59` + `14→18` superseded by §6
(`63`, `14→22`); R2-I §2.3 `object-exact-map` superseded by §7; R2-A §11 `CLOSED` + R2-F §11
`GO-CONDITIONAL` superseded by §12 (RULE-FIXED/MAP-COMPLETE, no conditional pass); R2-I §6 DAG
without Layer-B superseded by §9; R2-F §8 "all reachable evidence" + R2-I §4.5 "9 keys"/`contract:object`/
retained-dest wording superseded by §§1/10; R1 §4.4 N1/N2 + R1 "50+7"/"new files only" superseded by §6.
All other R1/R2 `file:line` locations remain valid where cited.

## 1. Schema bytes — 5 amended + 4 new (replaces R2-A §8; closes review §1)

Source ground truth (PC, verified in this unit):

- `PC/schemas/reader-manuscript-v2.schema.json` (5751 B): `additionalProperties:false`,
  `required` 15 keys incl `manifest_sha256`, `properties` has only `editorial_source`
  `{proposal_ref,staged_manifest_ref}` (`:101-112`), NO `renewal_source`. Any serialized
  `renewal_source` in a C file fails validation unless amended.
- `PC/schemas/publication-candidate-v2.schema.json` (2980 B): `additionalProperties:false`,
  `required` 11 keys ending `candidate_sha256`, NO renewal. Builder
  `PC/scripts/survey_publication_v2.py:668-746` digests base 10 (`:730-743`); validator `:749-814`
  recomputes 10 (`:753-766`). 11th serialized key requires amendment.
- `PC/schemas/quality-regression-bundle-v2.schema.json` (3908 B): `additionalProperties:false`,
  `required` 10 keys, NO renewal. Builder `:193-229` digests 9-key basis (`:213-224`);
  validator `:232-274` recomputes 9 (`:259-263`). 10th key requires amendment.
- `PC/schemas/reader-surface-gate-v2.schema.json` (7492 B): `derivation.oneOf` exactly 4 variants
  (`:160-217`); builder `:1333-1694` digests 13-key base (`:1650-1685`); validator `:1737-1753`
  recomputes 13. 5th variant requires amendment.
- `PC/schemas/publication-surface-revalidation.schema.json` (9162 B): `oneOf` exactly 2 (`:6-9`),
  legacy + `EDITORIAL_PUBLICATION_ACTIVATION_V1` (`:97-245`). 3rd branch requires amendment.

R3 fix (verbatim old/new per file; "new files only, old bytes untouched" DELETED):

1. `reader-manuscript-v2`: OLD `required` 15 + `additionalProperties:false` + `properties.editorial_source`
   preserved verbatim. NEW strict OPTIONAL `renewal_source:{path:S,sha256:SHA}` with
   `allOf` XOR: exactly one of `editorial_source`/`renewal_source` for renewed sets; legacy/editorial
   files keep `editorial_source` only. U: NO serialized change (old bytes/digest unchanged; context is
   function keyword ONLY, §9). C (new file ONLY): serialized `renewal_source` present. Digest: old
   `manifest_sha256 == core.sha256_object({14 keys excl self})` where 14 =
   `schema_version,issue_id,research_profile,publication_profile,status,production_profile,
   architecture,architecture_approval,primary_source,supporting_files,architecture_coverage,
   reader_requirements,authored_by,recorded_at` (`PC/scripts/survey_reader_publication_v2.py:427-442`);
   `editorial_source` 15th iff present (`:443-447`); C `renewal_source` 15th iff present (14+1).
   State base-without-self vs required-incl-self explicitly per object (no "14 keys" confusion).
2. `publication-candidate-v2`: OLD `required` 11 + `additionalProperties:false` preserved. NEW strict
   OPTIONAL `renewal_source_proof_ref:{path:S,sha256:SHA}` (new files ONLY, U+C). Builder base 10
   (`schema_version,issue_id,publication_profile,status,reader_manuscript,source,pdf{+page_count},
   quality_bundle,semantic_review,visual_review` `:730-743`) → renewed digest
   `core.sha256_object({10 keys + renewal_source_proof_ref})` (11-key base excl self; required 12
   incl `candidate_sha256`). Validator derives from own payload; outer expected ref must be identical.
   Old files validate against OLD schema SHA (record epoch); renewal validates against NEW disk bytes.
3. `quality-regression-bundle-v2`: OLD `required` 10 preserved. NEW strict OPTIONAL
   `renewal_source_proof_ref` (new files ONLY, U+C). Builder 9-key basis
   (`schema_version,issue_id,production_profile,research_profile,publication_profile,source,pdf,
   checks,status` `:213-224`) → renewed digest 10-key base excl self (required 11 incl
   `bundle_sha256`); `checks` stored `sorted(check_id)`. Validator recomputes same (§10 order).
4. `reader-surface-gate-v2`: OLD 4 variants verbatim, never augmented. NEW 5th variant
   `VERSIONED_RENEWAL_V1/RENEWAL_MAIN_BIB_STYLE` BOTH U and C:
   `{route:const VERSIONED_RENEWAL_V1, scope:const RENEWAL_MAIN_BIB_STYLE, receipt:{path,sha256},
   renewal_source_proof_ref:{path,sha256}, renewal_receipt_ref:{path,sha256}}`
   where `receipt` = `R/validated-source-manifest.json`, `renewal_source_proof_ref` =
   `R/renewal-source-proof.json`, `renewal_receipt_ref` = same receipt path+SHA (redundant pair binds
   proof+receipt per decision §11.2). Present renewal refs live inside `derivation`, thus in 13-key
   digest (`schema_version,issue_id,publication_profile,status,scanned_surfaces,rules_checked,
   suppressions,findings,summary,evaluated_by,recorded_at,derivation,semantic_authority`
   `:1650-1685` / `:1737-1753`). Old Gates keep 4 variants + 13-key digest without renewal refs.
5. `publication-surface-revalidation`: OLD 2 branches verbatim. NEW 3rd branch
   `VERSIONED_RENEWAL_ACTIVATION_V1` + `REVIEWED_VERSIONED_CORE_RENEWAL` per decision §7 (all REQUIRED,
   no nullables; `supersedes` REQUIRED nonnull prior versioned record; `before_candidate_ref` REQUIRED
   nonnull; `before_active_digest` recomputed via existing effective7+Candidate, basis/proof covered by
   new set/record refs; chain/anchor/sequence/time/cycle rules `CHAIN_LIMIT=32`
   `PC/scripts/survey_publication_set_v2.py:109,1023-1051,1060-1230`; later legacy successor unsupported
   `:1189`; R1/canonical pre-write refusal kept). Old/new pins separate per §2.

Review-record schema/bytes UNCHANGED: binding lives in containing NEW Candidate/bundle/Gate
(nested `validate_manuscript_manifest:643-647` threads SAME reloaded proof explicitly). Old U review
files stay byte-identical.

4 NEW schemas are new paths (no conflict): `versioned-renewal-basis-v2`,
`versioned-renewal-source-proof-v2`, `versioned-renewal-source-manifest-v2`,
`versioned-renewal-publication-set-v2` (+ in-file `R/build-record.json` `REUSED_BUILD`/
`EXECUTED_BUILD` variants, §7). Any drift in an old schema file outside the 5 listed branches →
`UNSUPPORTED_MIGRATION`.

## 2. Old tool epochs — conditional staged + repeat-chain rule (closes review §2)

`old_tool_epochs` in basis (R2-I §2.1 shape retained, semantics fixed):

```text
old_tool_epochs: {
  receipt_epoch: {repository_commit_sha:GITSHA, contract:Contract8, closure:NamedRow[1..]},
  staged_epoch: PRESENT iff predecessor kind==R3_EDITORIAL else ABSENT (see below),
  schema_epochs: per-schema {epoch,sha} per §4 (replaces SHA-only)
}
```

- Each T row checked against ITS OWN recorded epoch blob
  (`git cat-file -e <epoch>^{commit}` + `git show <epoch>:<path>` SHA (+`byte_count` where sized);
  never live-path equality; never cross-substituted; missing (incl partialDB-26309) →
  `HISTORY_BLOB_MISSING`; overlap rows (same path in receipt+staged+schema epochs) must agree else
  `HISTORY_TOOL_EPOCH_DRIFT`. `receipt_epoch.repository_commit_sha` is receipt `current_tools`
  epoch; `staged_epoch.producer_head` is `survey_editorial_staged_source_v2.py:1039` shape; per-schema
  epochs are record-epoch SHAs (§4). Publication artifacts (manuscript/PDF/build/record/reviews) are
  NOT required at the tool commit (positive control, decision §3): "old evidence absent from tool
  commit" MUST pass history.
- Conditional: `staged_epoch PRESENT iff prior seal refs `P/publication/publication-set.json` +
  `P/publication/validated-source-manifest.json` + `P/staged-source/staged-source-manifest.json`
  (editorial predecessor). `ABSENT iff prior seal refs prior `R/publication-set.json` + prior
  `R/renewal-source-proof.json` (renewal predecessor)`: prior `R` trio FILES live under prior
  `R/staged-source/{main.tex,references.bib,jgaisurvey.sty}` with NO manifest file (proof IS the
  staged proof; forging old-format P3S manifest at renewal path refuses, §7). Prior proof carries
  `supported_epochs:{receipt_epoch,staged_producer_head}` (R2-I §2.2) + prior basis `old_tool_epochs`
  as the staged history; requiring a fresh `staged_epoch.code_deps` blob check against prior `R`
  path has no defined source and MUST NOT be attempted.
- Repeat-chain rule: for repeat/C→U/renewal→editorial, EVERY prior activation's basis/proof/epochs
  along `_walk_chain_backwards:1023-1051` (newest→oldest over `supersedes`, `CHAIN_LIMIT=32`,
  `1060-1230` anchor/sequence/time) are required — not just the latest original staged manifest.
  New proof `supported_epochs` = union of walked ancestor epochs (receipt epochs + staged producer_heads
  + per-schema epochs per §4). Any missing ancestor epoch → `HISTORY_BLOB_MISSING`, never forged.
  Anchor is latest legacy immediately before FIRST versioned activation, never rolled forward; mixed
  chain active-inclusive max32, strictly increasing sequence, nondecreasing time, no cycles; later
  legacy successor unsupported.

History entry: `verify_versioned_history(root,record_path)` (HIST leaf, record-only, no State arg)
reloads record/schema/kind/anchor/supersedes/set/receipt/renewal-proof/basis/retention + original
scope evidence; epochs from those records (per-document), typed E/T classification from typed
`RECEIPT_TOOL_CLOSURE` edges + fixed closure membership (never KEEP/prefix/wildcard), COPY
mapping/inventory, old self-/cross-digests; returns `HISTORICAL_IDENTITY_VERIFIED` + observed refs,
never a permit. Cannot call current low `validate_seal`/selection, P2R/P3S, high receipt, P2V,
agent/Reader/Gate/Candidate. New high `verify_renewal_history` delegates; structural loading of a
renewal proof does not execute its current-replay branch (decision §11.1). New basis/COPY validator
`validate_renewal_basis(root,basis_path)` lives in SOURCE module (decision §11).

Bootstrap recognized R3 formats (finite, closed): P1 proposal shape + `_before_graph` + retention
plan; retention layout `<P>/retained/before/<original_path>` (`_expected_retained_dest:831`,
`_retained_expected_sets:835`, `capture_retention:857`, `verify_retention:1737`); staged closed trio
+ manifest + `verify_staged_source:1772` replay (exact `{main,bibliography,style}`); editorial/Weekly/
Longform receipt shapes with `current_tools{repository_commit_sha,contract,closure}`; editorial seal
fixed `<P>/publication/publication-set.json` exact 15 roles (`PUBLICATION_ROLES_15`); revalidation
exactly 2 branches; P3S fixed-50 code deps + Weekly-22/Longform-27 subsets; style + `.latexmkrc`
(`REQUIRED_RECIPE_MARKERS`, `FIXED_RECIPE_STEPS`); manuscript/Gate/QA/Candidate old branches verbatim.
Unrecognized (unknown schema version/code_deps name/style/recipe bytes, missing/foreign/ambiguous
authority, dirty control roots, unavailable blobs, nonancestor epoch, unsafe path, changed
research/Profile) refuses BEFORE writes. Second-generation `R/retained/before/` + 4 new schemas +
3 new modules + 5 amended branches are NEW (§§1/6), never recognized as old.

## 3. U prior-relative (closes review §3)

ALL U "original" refs are redefined as **prior-selected refs** (from `prior_selected_ref` seal roles:
trio/manuscript/build3/reviews at whatever paths the prior seal pins, whether `P/...` or prior `R/...`).
R2-I §2.2/§2.4 `P/` literals are FIRST-RENEWAL EXAMPLES ONLY.

- U `output_trio_refs`: prior seal trio paths (old `P/staged-source/...` on editorial predecessor;
  prior `R/staged-source/...` FILES on renewal predecessor). U `old_manuscript_ref`: prior seal
  `reader-manuscript` role path+SHA (original `P/publication/reader-manuscript-v2.json` OR prior
  `R/reader-manuscript-v2.json`). U `old_build_unit_refs`: prior seal `publication-pdf/build-log/
  pdf-digest` + prior build-record as a unit at prior paths. Seal roles for U point at those ORIGINAL
  immutable paths; receipt/QA-bundle/Gate/Candidate point at NEW `R/` paths. C roles per R2-I §2.4
  retained (reader/authoring/retention/scope-history at ORIGINAL `P/` paths; all else NEW `R/` paths
  except external postrender review RECORDs where pinned, §10).
- Negative `REVIEW_TARGET_MISMATCH` for U that points at non-active `P/` when active predecessor is
  prior `R/` (stale-`P` revalidation refused; State-selected predecessor equality per decision §7/§11.1
  is mandatory). Source discipline is prior-relative binding (editorial receipt binds staged
  main→primary `PC/scripts/survey_reader_publication_v2.py:253-269`, Gate `:1225-1251`; seal roles
  checked as exact recorded paths `PC/scripts/survey_publication_set_v2.py:492-511,
  _check_doc_refs_against_seal:433-442`), not hardcoded `P/` strings.
- Positive `C→U` oracle (mandatory): C then U with unchanged trio at prior `R/` paths yields
  `REUSED_TARGETS` (U renderer-equality vs prior `R/` bytes, §7/§11); U-then-C, C-then-U, U-then-U
  (repeat with new Core commit), and renewal→editorial are all explicit DAG edges (§§9/11).

Historical build-unit chain: U `REUSED_BUILD` (`original_record_ref/original_pdf_ref/original_log_ref/
original_digest_ref` + `renewal_tools:{old,new}` + `no_rebuild:true`) refs the IMMEDIATE prior build
record path+SHA (prior `P/publication/build-record.json` on first renewal; prior `R/build-record.json`
on repeat). If prior is itself `REUSED_BUILD`, the chain is walked historically (HIST) to the
terminal `EXECUTED_BUILD` (old R3 `EXECUTED_BUILD` or prior `R/EXECUTED_BUILD`) with bounded consistent
refs (same issue/Profile/recipe spec, exact `fixed_steps`, toolchain executable family per §7);
any break → `HISTORY_ANCESTOR`/`REVIEW_TARGET_MISMATCH`, never synthesized.

## 4. Schema epochs with epoch binding (closes review §4)

R2-I §2.1 `schema_epochs` SHA-only is superseded. R3:

```text
schema_epochs: {
  proposal: {epoch:GITSHA, sha256:SHA}, retention: {epoch:GITSHA, sha256:SHA},
  staged: {epoch:GITSHA, sha256:SHA}, receipt: {epoch:GITSHA, sha256:SHA},
  set: {epoch:GITSHA, sha256:SHA}, revalidation: {epoch:GITSHA, sha256:SHA}
}
```

- Each row verified via `git show <epoch>:<schema-path>` SHA (+ old-schema validation
  fingerprint/epoch map per exact type+path from §2 chain); content SHA alone never selects the blob;
  live-disk equality never accepted (decision §3: "recorded receipt hashes cannot be accepted merely
  because a receipt lists them"). Where dependency rows overlap (same schema path in receipt closure +
  schema epoch), epochs must agree else `HISTORY_TOOL_EPOCH_DRIFT`; missing → `HISTORY_BLOB_MISSING`
  (partialDB-26309 included). Historical schemas supported by finite compatibility adapter + epoch
  cross-check; no arbitrary historical schema code or remote `$ref` execution/fetch (all `$ref` local
  `#/$defs/*` verified: candidate/QA/manuscript/gate/revalidation use only `#/$defs/*` + inline
  `const/enum`).
- Old-schema validation uses record-epoch bytes; renewal validation uses current-disk bytes (§1 pins).
  Steady-state requires exact schema shape equality apart from §1 five-branch additions
  (`CONTRACT_MISMATCH`/`CLOSURE_SET` on relaxation/new kind/route-semantics change, §6).

## 5. Authoring/accepted ordering (closes review §5)

- `authoring_refs`: array len2 exact SET `{proposed-publication-authoring, accepted-draft-archive}`
  (R2-I "sorted by name" example `[{proposed},{accepted}]` was backwards and is superseded). Actual
  writer order is SOURCE order `[proposed-publication-authoring, accepted-draft-archive]`
  (`PC/scripts/survey_editorial_publication_v2.py:1881-1884` literal). R3: file-bytes order MUST equal
  exact predecessor bytes order (`[proposed, accepted]`); equality is sorted-set via `_norm`
  (`name,path,sha256` tuples, no dups; `PC/...:963-979,1032-1048,1838-1848`): `set(authored)=={...}`
  checks (`:846,:1705`) are the precedent. "Stored sorted" MUST NOT be required for authoring (would
  mismatch predecessor bytes).
- `accepted_refs`: array minItems1, unique `name`, items `{name,path,sha256}`; MUST equal EXACT prior
  receipt list. Writer stores SORTED order (`:1885` via `_norm_prep` sorted), comparison is sorted-set
  via `_norm`/`_norm2`/`_norm_prep` (sorted `(name,path,sha256)` tuples, no dups). "Verbatim" means
  sorted-set equality, NOT byte-order verbatim when prior writer sort key differs; same-SHA
  different-path refused. Cite `survey_weekly_derivation_v2.py:587-590` (`sorted(accepted_refs)`),
  `survey_longform_derivation_v2.py:1092`, editorial receipt `:1885`.

## 6. Single closed closure 63 (closes review §6; math 63 NOT 59)

R2-F §4.5 `59` (`35py+18schemas+3route+1staged+1style+1recipe`) + `14→18` is superseded.
R3 is ONE closed set (no N1/N2 alternates; R1 §4.4 N1/N2 deleted): **per-route 63 =
shared35(py) + schema22 + route3 + staged1 + style1 + recipe1**. Union across both routes = 66
distinct (63 per route + other route's 3). "35py + route-3 double-count" resolved: 35 is
route-independent shared; route-3 is per-route conditional disjoint from 35/22.

### 6.1 `.py` runtime closure — shared35 (exact, finite, disjoint)

- P3S50 `_SHARED_PY` 30 (verified present; `PC/scripts/survey_editorial_staged_source_v2.py:92-123`):
  `scripts/render_article_draft_tex.py`, `scripts/survey_agent_control_v2.py`,
  `scripts/survey_agent_tool_v2.py`, `scripts/survey_architecture_v2.py`,
  `scripts/survey_architecture_v2_base.py`, `scripts/survey_bibliography_access_provenance_v2.py`,
  `scripts/survey_completeness_v2.py`, `scripts/survey_drafting_citation_refs_v2.py`,
  `scripts/survey_drafting_v2.py`, `scripts/survey_drafting_v2_base.py`,
  `scripts/survey_editorial_correction_proposal_v2.py`,
  `scripts/survey_editorial_current_authority_v2.py`, `scripts/survey_editorial_publication_v2.py`,
  `scripts/survey_editorial_retention_v2.py`, `scripts/survey_evidence_v2.py`,
  `scripts/survey_longform_derivation_v2.py`, `scripts/survey_longform_generated_v2.py`,
  `scripts/survey_production_v2.py`, `scripts/survey_publication_set_v2.py`,
  `scripts/survey_publication_v2.py`, `scripts/survey_quality_v2.py`,
  `scripts/survey_reader_fidelity_v2.py`, `scripts/survey_reader_publication_v2.py`,
  `scripts/survey_reader_surface_gate_v2.py`, `scripts/survey_review_attention_v2.py`,
  `scripts/survey_schema_v2.py`, `scripts/survey_screening_v2.py`,
  `scripts/survey_weekly_derivation_v2.py`, `scripts/validate_article_draft.py`,
  `scripts/weekly_pipeline.py`.
- Transitive +2 REQUIRED by shared-core placement (verified reachable via function-local/dynamic
  edges, NOT P3S top-level AST): `scripts/survey_discovery_v2.py` (12757 B; screening `:397`
  function-local `import survey_discovery_v2`; discovery→x_intake top-level `:12`),
  `scripts/survey_x_intake_v2.py` (23144 B; discovery top-level import; x_intake `:360`
  function-local `import survey_discovery_v2`). Proof is `file:line` of the import reaching a shared
  core (not size): screening top-level imports EXCLUDE discovery (function-local `:397` only),
  discovery top-level `survey_x_intake_v2`, x_intake imports `core+schema_gate+discovery` only. All
  other family modules already in 30. No `survey_draft_profile_v2`/`stage_validation`/`orchestrator`/
  `handoff`/`human_gate`/`weekly_pipeline` additions: consumers, not leaf transitives.
- NEW +3 (fixed): `scripts/survey_versioned_renewal_history_v2.py`,
  `scripts/survey_versioned_renewal_source_v2.py`, `scripts/survey_versioned_renewal_v2.py`.
- Total `.py` shared: 30+2+3=**35**. Any actual extra top-level `scripts.*` import beyond these 35
  (+ route-conditional semantic producer per route, §6.3) → `CODE_DEPS_EXPANSION_REQUIRED`, never
  silent omit. Location principle (accepted-R2 §9 adopted): State-free CONTENT cores as NARROW private
  shared helpers IN existing family files (same pure helpers, `citation_refs`/`_source_class`/token/URL/
  archive reuse); original publics keep UNCHANGED signatures via thin wrappers (State block + delegation);
  source module holds ONLY session constructor + §11.3 six-condition enforcement + Layer-A/B orchestration.

### 6.2 Schema closure — shared22 (exact, finite; `$ref` local only)

- P3S50 `_SHARED_SCHEMAS` 14 (verified): `editorial-correction-proposal`,
  `editorial-manuscript-spec`, `editorial-publication-build-record`, `editorial-publication-set`,
  `editorial-publication-source-manifest`, `editorial-retention-manifest`, `editorial-staged-source-manifest`,
  `editorial-toolchain-spec`, `publication-candidate-v2`, `publication-surface-revalidation`,
  `quality-regression-bundle-v2`, `reader-manuscript-v2`, `reader-surface-gate-v2`,
  `reader-surface-semantic-review-v2` (all `schemas/*.schema.json`).
- NEW +4 (§1): `versioned-renewal-basis-v2`, `versioned-renewal-source-proof-v2`,
  `versioned-renewal-source-manifest-v2`, `versioned-renewal-publication-set-v2`.
- Family +4 REQUIRED by shared cores but missing from P3S50 (verified `required` by accepted-R2 §4
  table + pipeline membership): `discovery-acceptance-v2`, `survey-discovery-record`,
  `screening-v2-run-package`, `screening-v2-batch-result`. Evidence package/task/card, supplement,
  edition view, ledger, completeness, matrix, selection, architecture, approval, summary, attention,
  synthesis input/result, draft package/result are either already in 14 or pipeline content (§6.4);
  the 4 above are the ONLY schema files the shared cores validate absent from BOTH P3S50-14 and new-4.
  All `$ref` local `#/$defs/*` + inline `const/enum`; no remote `$ref`, no network.
- Total schemas shared: 14+4+4=**22**.

### 6.3 Route-conditional 3 per route (disjoint from shared)

- Weekly: `scripts/survey_weekly_semantic_publication_v2.py` +
  `schemas/reader-surface-input-v2.schema.json` + `schemas/weekly-publication-source-manifest-v2.schema.json`
  (resolves `READER_INPUT_SCHEMA/RECEIPT_SCHEMA` in `survey_weekly_derivation_v2.py:22-27`;
  `CURRENT_CLOSURE` Weekly 22 `PC/...:28-51` verified present).
- Longform: `scripts/survey_longform_semantic_publication_v2.py` +
  `schemas/longform-reader-input-v2.schema.json` + `schemas/longform-publication-source-manifest-v2.schema.json`
  (`CURRENT_CLOSURE` Longform 27 `PC/...generated_v2.py:52-80` verified present).
- Staged 1: `scripts/survey_editorial_staged_source_v2.py` (`STAGED_MODULE`). Style 1:
  `templates/survey/jgaisurvey.sty` (6569 B, `035645ca…`). Recipe 1: `.latexmkrc` (218 B, `18199fd8…`)
  with `REQUIRED_RECIPE_MARKERS` + `FIXED_RECIPE_STEPS` + `EXPECTED_ARGV_*` (§7).

Per-route total: 35+22+3+1+1+1=**63**. Gates to update in same unit (decision §8):
`survey_editorial_staged_source_v2.py` `_SHARED_PY/_SHARED_SCHEMAS` + `_route_code_deps`
(30→35 py, 14→22 schemas; union 50→63 with route/staged/style/recipe constants unchanged);
`_editorial_closure_rows` (`survey_editorial_publication_v2.py:1958-1993`) + `len==50` gate → `len==63`
same sorted-unique + AST edge-audit; `test_group_c_editorial_consumers_v2.py:119-121`
(`==30/==14` → `==35/==22`); Weekly `CURRENT_CLOSURE` 22→29 / Longform 27→34 (each += same 7
renewal files: 3py+4schemas; insertion points `weekly:37-50` / `generated:67-79`).

### 6.4 Content-contract (pinned bytes, NOT `.py` runtime — finite, no hiding)

Prompts (current-disk SHA, TC-content): `config/prompts/source-screening-v2.md`,
`config/prompts/evidence-verification-v2.md`, `config/prompts/article-drafting-v2.md`,
`config/prompts/profile-synthesis-v2.md`, `config/prompts/grok/x-source-intake-base-v1.md`,
`config/prompts/grok/x-source-intake-weekly-v1.md`, `config/prompts/grok/x-source-intake-special-v1.md`.
Config: `config/survey-production-v2.json` (control roots + 67 pipeline + 3 quality contract files;
`implementation_control_roots:["config","schemas","scripts",".github/workflows"]`),
`config/publication-review-v2.json`, `config/survey-production-v2-requirements.txt`.
Schemas-as-content: all §6.2 schemas + pipeline family schemas (`evidence-v2-run-package/task/card`,
`evidence-authority-supplement`, `edition-evidence-view`, `materiality-ledger`,
`profile-completeness-result`, `candidate-matrix-v2`, `candidate-selection-v2`, `issue-architecture-v2`,
`architecture-review-summary/attention/approval-record`, `draft-v2-package/result`,
`profile-synthesis-v2-input/result`, `publication-review-record-v2`, `visual-review-record-v2`,
`publication-preview-approval-v2`, `freeze-record-v2`, `release-manifest-v2`, `stage-checkpoint-v2`,
plus docs contract files; full 67+3 list is `config/survey-production-v2.json:6`
(`PIPELINE_N 67 / QUALITY_N 3` verified). Distinction: runtime `code_deps` (AST-verified imports,
§6.1–6.3) vs content `contract` (pipeline/quality file hashes via `core.contract_identity:210-228` +
prompt/schema bytes). The verifier binds BOTH: Layer-B-2 recomputes CURRENT closure member-wise vs
`proof.dependency_closure` AND recomputes `contract_identity` vs `proof.supported_contract`; missing/
extra/drift → `BASIS_CURRENT_TOOL_DRIFT` / `UNSUPPORTED_MIGRATION`. No validated file hidden outside
either set.

### 6.5 Registration deltas (exact — ONLY control/contract list changes)

- `config/survey-production-v2.json`: `contract_files.pipeline` += 4 NEW schema paths (§6.2) ONLY
  (67→71). `implementation_control_roots` UNCHANGED (already covers `scripts/`; no new control root).
  `contract_files.quality` UNCHANGED (3). NO `.py` in `contract_files.pipeline` (py files are closure
  members, not contract files) — this preserves steady-state code-only change eligibility: py-only
  changes move closure/tool epoch without pipeline contract migration; schema/contract/route-semantics/
  research/Profile changes remain migration (decision §2). No prefix rule, no caller allowlist, no
  literal-50 retention.

Steady-state allowed-change (MECHANICAL predicate, §6 gate): post-bootstrap committed change is
supported same-contract Core renewal IFF ALL hold (missing/extra/drift lists where applicable):
(1) `git show <new_epoch>:<path>` succeeds for every §6.1–6.3 member; `merge-base --is-ancestor
<old_epoch> <new_epoch>` holds; no symlink in new tree; no mode change except 5 amended + 7 new
(`100644`, §2); (2) closure membership `set(new)==set(§6.1∪§6.2∪route3∪{staged,style,recipe})`
sorted-unique else `CLOSURE_SET`; (3) per-file bytes: every file EXCEPT §1 amended/new set +
`templates/survey/jgaisurvey.sty` + executable/tool files under SAME fixed recipe is byte-identical
else `CLOSURE_DRIFT` (style MAY differ for C rendering evolution; recipe `.latexmkrc` MUST equal
pinned markers/steps else `RECIPE_INCONSISTENT`); (4) schema/contract: every schema `required/
additionalProperties/oneOf` equals recorded shape apart from §1 five branches else
`CONTRACT_MISMATCH`/`CLOSURE_SET`; `contract_identity` recomputed equals `proof.supported_contract`
apart from pipeline SHA movement caused SOLELY by §6.5 new-4 entries; (5) research/Profile/
Architecture/Draft/pipeline-quality semantic/review-requirements/route/recipe-SPECIFICATION all
byte-identical else `UNSUPPORTED_MIGRATION` (never renewal); U retains historical build unit (no new
build), C executable versions MAY change under SAME fixed recipe (§7); (6) classification by identity:
same SHA at different target path is C, source-only/comment-only TeX altering trio bytes is C,
PDF-metadata-only deltas are C with new visual review; U mismatch → `REUSE_TARGET_MISMATCH` (no
auto-convert). Legacy never in required canonical changes; unknown schema/recipe modification rejected.

## 7. Toolchain exact schema (replaces `object-exact-map`; closes review §7)

Spec schema (`schemas/editorial-toolchain-spec-v2.schema.json`: `required` 8 keys
`schema_version/kind/executor/absolute_executable/recipe/argv/env/recorded_at`; `argv` string array;
`env` object) has NO `versions` key. R3 fixes the RECORDED `versions` object schema (build-record
`toolchain.versions`, NOT spec) + exact `argv`/`env` + variant branches:

- Spec `recipe` ∈ `{"lualatex-biber-lualatex","latexmk-lualatex"}`; spec `argv` MUST EXACTLY equal the
  expected const tuple for its recipe (not permissive membership):
  `EXPECTED_ARGV_LUALATEX_BIBER = FIXED_RECIPE_STEPS` =
  `("lualatex -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error main.tex",
  "biber main", "lualatex ... main.tex", "lualatex ... main.tex")`
  (`PC/scripts/survey_editorial_publication_v2.py:60-74,1202-1213,1372-1383`);
  `EXPECTED_ARGV_LATEXMK = ("latexmk -pdf -lualatex -interaction=nonstopmode main.tex",)`.
  Bare tool names in `argv` (no absolute paths); absolute exe/companion recorded separately.
- Spec `env` allowlist (enumerated, no `GIT_*/PATH/PYTHONPATH`): `ALLOWED_ENV_KEYS =
  {TEXMFHOME,TEXMFVAR,TEXMFCONFIG,SOURCE_DATE_EPOCH,TZ,LANG,LC_ALL,HOME}` + build-set
  `PATH=<toolbin>:/usr/bin:/bin` (`CONTROLLED_SYSTEM_PATH_SUFFIX`, `:106-118,:1404-1410`).
  `PATH` refused in spec; `GIT_*`/`PYTHONPATH`/`LD_LIBRARY_PATH` refused (`:1219-1227`); values plain
  strings, no newline/NUL; recipe `.latexmkrc` MUST contain `REQUIRED_RECIPE_MARKERS`
  `($pdf_mode=4;,$lualatex,$biber,$max_repeat,)` (`:1228-1244`).
- Recorded `versions` (exact schema, `additionalProperties:false` + truncation):
  REQUIRED `stdout:S[≤8000],stderr:S[≤8000],returncode:int,link_path:S,real_path:S,
  real_sha256:SHA` (exe `--version`, `:1336-1347`) + per-companion (`biber`,`latexmk` in same bin dir,
  resolved chain, no arbitrary PATH): `"<comp>_stdout":S[≤4000],"<comp>_returncode":int,
  "<comp>_link_path":S,"<comp>_real_path":S,"<comp>_real_sha256":SHA`, `"<comp>_error":S[≤300]`
  iff missing (`:1348-1362`); on exe failure `error:S[≤500]`. `argv` = executed list =
  `list(expected_argv)` (`:1400`); `env` = `{k:allowed_env[k] for k in sorted(allowed_env)}` (`:1540`).
- `R/build-record.json` variant-tagged (one variant REQUIRED, `additionalProperties:false`):
  Common `schema_version:2.0-rc1,variant:REUSED_BUILD|EXECUTED_BUILD,issue_id,proposal_ref,
  renewal_basis_ref,renewal_proof_ref,recipe_ref:{path,sha256}=.latexmkrc,recorded_at,
  build_sha256=core.sha256_object({all except self})` (INCL input/output refs).
  `REUSED_BUILD` (U-ONLY, basis `RENDER_TARGETS` absent + `toolchain_spec_path=None`, no spawn):
  `original_record_ref/original_pdf_ref(PdfRef:{path,sha256,byte_count,page_count})/
  original_log_ref/original_digest_ref` (prior build3 as unit) + `renewal_tools:{old:GITSHA,new:GITSHA}`
  + `no_rebuild:true`; NO `declared_inputs/recipe/toolchain/outputs/exit_code`.
  `EXECUTED_BUILD` (C-ONLY, basis `RENDER_TARGETS` + explicit spec, disposable root + exclusive transfer
  + readback): `declared_inputs:{primary,bibliography,style}` (new `R/` trio) +
  `recipe:{fixed_steps:S[1..]}` (fixed recipe under selected existing recipe) +
  `toolchain:{executable:S,versions:<above>,argv:S[],env:object}` + `outputs:{publication-pdf,
  build-log,pdf-digest}` (SizedRefs under `R/build/`) + `exit_code:const 0`; NO `original_*`.
  Receipt binds build-record, never precedes it (decision §11.1; corrects reviewer illustrative remedy).

## 8. Accepted-authority map — RULE-FIXED + MAP-COMPLETE (closes review §8)

R2-A §11 `CLOSED (rule)` relabelled **RULE-FIXED/MAP-COMPLETE** (this R3 IS the map); R2-F §11
`GO-CONDITIONAL` ("implementation may proceed ONLY after Astra confirms" permitting pre-confirmation
prep) DELETED. New text: **IMPLEMENTATION BLOCKED until Astra confirms this R3 jointly per §§9/11.3.**
Per-family extraction diffs + oracles are IN this R3 (not deferred):

- Layer-A accepted-content subloader: `load_renewal_accepted_authority(root:Path,basis_path:Path)`
  ONLY (no `*_statefree(root,package_path)` publics; R1 §5 16-signature list superseded). Builds SAME-
  invocation private session `_RenewalAuthoritySession={root,basis,basis_sha,profile_ref,reader_ref,
  authoring_refs,accepted_refs,before_state_ref,retained_copy_ref,retained_bytes,prior_refs:
  {seal,record,candidate,validation_checkpoint,anchor},old_tool_epochs,current_tool_epoch}` from
  `basis_path` bytes + live re-reads only; never caller/ambient/global/cached. All other validators are
  PRIVATE same-invocation `(session,...)` taking session-pinned values (full list in R2-A §2 adopted).
  Finite anti-arbitrary-map match (session constructor, before content): `basis.accepted_refs` MUST equal
  prior receipt `accepted_refs` verbatim (sorted `_norm`, unique, exact `{name,path,sha256}`; §5),
  `basis.authoring_refs/reviewed_reader_ref/profile_ref` MUST equal prior set bytes,
  `basis.prior_*` MUST equal HIGH-observed live prior seal/record/Candidate,
  `basis.original_validation_ref` MUST equal HIGH-observed original checkpoint; else
  `BASIS_ACCEPTED_SET_DRIFT` before content. Basis name-map carries NO self-authority.
- Manuscript/Gate/bundle CONTENT leaves the loader (R2-A §1 adopted): loader returns ONLY
  `{surface,records,accepted_refs,authored_refs}` where `surface` is PURE projector output
  (`weekly.build_reader_input:300-394`, `longform.build_longform_reader_input:608-926`) AFTER all
  authority checks; `records` is DID→bibliography map. It NEVER calls `validate_manuscript_manifest`,
  review contextual validation, Gate derivation/evaluation, Candidate build/validate,
  `quality.validate_bundle` as authority, seal, full receipt. Pure shape/render helpers allowed
  (`validate_reader_input:397-407`, `validate_longform_reader_input:927-948`, `render_main/
  render_bibliography/validate_generated_closure:414-486`, Longform canonical-bytes/render helpers).
  U predicate list (decision §11.2) is DOWNSTREAM on typed renewal-aware validators (§§1/9/10),
  not leaf body. Standalone old validators WITHOUT proof keep current P3S refusal.
- Tool split: Layer-A (no Git, no `repository_commit_sha`, no closure/contract/commit, no epoch blob)
  vs Layer-B full detached verifier (SOURCE module, still NO State, on EVERY proof readback incl after
  activation: reload proof+basis, recompute self-digests, verify `proof.basis_ref/accepted/reader/
  authoring/trio`, recompute CURRENT closure/contract/schemas from CURRENT disk via safe helpers,
  require HIST verdict; §9) vs HIST epochs (record-only). R2-A §1.2 W4 "leaf doesn't check tools"
  holds ONLY for Layer-A (superseded as stated for whole module).
- Labels: per-schema fields ONLY (R2-A §4 table adopted; R1 W2/L2 blanket rule superseded). Route from
  Profile only (`profile.research/publication_profile` must equal `basis.*` + `generator_route`
  `WEEKLY/WEEKLY_MAGAZINE→WEEKLY_GENERATED_V2`, `THEMATIC/LONGFORM_SPECIAL→LONGFORM_GENERATED_V1`).
  Enforcement `_check_leaf_labels_s(session)` iterates basis rows, checks schema-listed fields + cross-row
  `issue_id` + `research_profile` (where schema carries) + `publication_profile` (where schema carries).
- A1–A7 source expressions + checkpoint-wrapper provenance + finite prior-receipt match (R2-A §5 adopted
  verbatim as MAP): A1 `derive_candidate_matrix`, A2 `validate_selection:291-448`, A3 `validate_architecture
  :451-…`, A4 `validate_architecture_approval:105-134`, A5 `build_synthesis_input:706-774`/
  `validate_synthesis_result:777-831`, A6 `validate_self_contained_draft_package` + `validate_draft_package`/
  `derive_draft_package` + `validate_draft_result:589-703`, A7 `_validate_archive_authorization:530-581`
  + Weekly `:531-554`; HIST owns wrapper existence/shape/digest/chain, DETACHED runs content on
  session-pinned bytes (never `resolve_checkpoint_artifact`), CURRENT is HIGH. `Path(".")` bugfix DROPPED
  (R2-A §7: `expected_result_basis:595-603` `repo_root` unused; call-site `:670` harmless; NO fix goal).
  U-mismatch ≠ migration (R2-A §6: `REUSE_TARGET_MISMATCH` → `REFUSED_PRE_WRITE` exit 2, new-id C supported;
  `UNSUPPORTED_MIGRATION` reserved for research/Profile/Architecture/Draft/contract/review/route/recipe-spec).
- Placement: NARROW private shared CONTENT cores IN existing family files (same helpers; e.g.
  `_validate_evidence_package_basis_content(root,package,package,expectations)` in `survey_evidence_v2.py`
  minus `:764-770` State block minus `implementation_sha`, with `expectations={acceptance_sha,
  canonical_source_state_path,issue_id,...}` from session; similarly `_validate_screening_package_basis_content`,
  `_validate_result_batch_content`, `_validate_discovery_set_content`/`_validate_expansion_content`,
  `_normalize_record_content`+`_validate_graph_content`+`_validate_x_integration_content`,
  `_validate_ledger_content`, `_validate_completeness_content`, `_validate_view_content`,
  `_validate_supplement_content`, `_validate_selection_content`/`_validate_architecture_content`/
  `_validate_draft_content`). Original publics keep UNCHANGED signatures via thin wrappers (State block +
  delegation). Source module holds ONLY session + §11.3 six-condition enforcement + Layer-A/B orchestration.
  Exception ONLY with justified lines + equivalence oracle: run BOTH existing public (State-bound) and
  renewal core (session bytes) over identical accepted graphs, assert identical accept/refuse on every
  §11 oracle targeting that family; divergence without passing oracle → NO-GO. Honest gaps CLOSED as MAP:
  Ledger/Discovery/X/Materiality/completeness State-free bodies ADDED (E6/E8/E9/D1/X1 rows in R2/R1 adopted:
  `validate_edition_view:1170-1224`, `validate_edition_views_acceptance:1288-1330`,
  `validate_materiality_ledger:1410-1479` via `build_materiality_ledger:1331-1408`,
  `validate_completeness:1487-1607` + `survey_completeness_v2`, `discovery.validate_acceptance:245-269`
  + `_validate_graph:156-173` + `_validate_x_integration:179-202`, `x_intake.validate_manifest:344-396`
  + `_validate_spec:78-143`/`_policy_and_category:146-166`/`_validate_raw_ref:305-313`/
  `_validate_manifest_basis:315-342`; S1/S2/S4/S6–S10 verbatim; F6 directive/archive/token/URL/access
  verbatim). Hash-only forbidden; if any body proves unpreservable without weakening → precise NO-GO
  (none asserted in R3; oracles decide in implementation).
- Accepted State-SHA follows §0 correction (R2 `accepted-authority-readiness.md` §0 + decision §11.3,
  NOT predicate-map F3/F4 wording): historical `package.basis.state_sha256` stays ORIGINAL (no package
  mutation, no retained-dest compare); drift tolerated ONLY under §11.3 1–6 (acceptance `package_sha256`
  binding + acceptance==basis + same canonical SOURCE path from Profile `source_root` + config
  `state_authority.authoritative_filename` + same issue/Profile + valid retained COPY chain + every other
  predicate). Failure taxonomy `BASIS_STATE_PATH_IDENTITY`/`BASIS_ACCEPTANCE_BINDING_DRIFT`/
  `BASIS_ISSUE_PROFILE_DIVERGENCE`/`RETAINED_COPY_MISSING`/`HISTORY_PACKAGE_MUTATED`; LEAF owns
  package/acceptance/basis binding, HIST owns retained-COPY provenance, HIGH owns live-before.

## 9. Detached proof — Layer-B shape + binding (closes review §9)

Layer-A/B split (R2-A §3 + R2-F §6) is correct in shape; R3 completes binding:

- Layer-A (accepted subloader, NO Git): `load_renewal_accepted_authority(root,basis_path)` → session →
  session-scoped shared-core privates (R2-A §2 list; bodies R1 §§2.2–2.8 locations). Content only. ONLY
  meaning of "leaf doesn't check tools".
- Layer-B (full detached verifier, source module, still NO State — runs at startup AND on EVERY proof
  readback INCLUDING after activation): `verify_renewal_source_proof(root,basis_path,proof_path)` +
  `validate_renewal_basis(root,basis_path)` (detached retained-COPY + unchanged-evidence on every readback,
  decision §11.1). MUST: (1) reload proof+basis, recompute self-digests, verify `proof.basis_ref`,
  accepted/reader/authoring equality, trio refs sized+SHA; (2) recompute CURRENT closure from CURRENT
  disk (Weekly `current_closure:587-588` discipline; longform-generated equivalent; editorial union
  `survey_editorial_publication_v2.py:1959-2000` as updated to **63** in §6.5 — R2-F §6 "59" superseded),
  member-wise vs `proof.dependency_closure`/`basis.current_tool_epoch.closure` (missing/extra/drift →
  `BASIS_CURRENT_TOOL_DRIFT`); recompute `contract_identity` vs `proof.supported_contract` (apart from
  permitted implementation/style per §6 steady-state, else `UNSUPPORTED_MIGRATION`); verify schema files
  equal current disk bytes (§1 pins); all via `_safe`/no-follow/bounded reads, `git show <epoch>:<path>`
  NEVER (that's HIST), `core.verify_state_basis` NEVER, State load NEVER; (3) require HIST verdict
  (`verify_versioned_history` matching observed epochs; else `HISTORY_TOOL_EPOCH_DRIFT`/`HISTORY_BLOB_MISSING`).
  Consumes HIST verdict, never re-implements Git epoch reads, never issues permit.
- No-current-before-State-call PROVED as MAP (not asserted): Layer-B allowed-import list (exact):
  `core.load_json/sha256_file/sha256_object/sha256_bytes/repo_local_path/parse_instant/iso_utc/
  aggregate_file_hash/contract_identity(pure file read only)`, `schema_gate.parse_json_strict_bytes/
  loads_strict/load_json_strict/load_and_validate_json/validate_instance`, `citation_refs.refs`,
  `drafting.validate_synthesis_result/validate_draft_result`, `provenance.resolve_source_access_provenance`,
  pure token/URL/archive helpers (`_did/_package_id/_bib_key/_check_url/_resolve_primary_entity/
  _safe_card_path/_preflight_evidence_tree` containment), bounded `O_NOFOLLOW` `_safe`-equivalent reads.
  BANNED (AST non-reachability required, same `CODE_DEPS_EXPANSION_REQUIRED` discipline as P3S `:172-201`):
  `agent.validate_agent_state/_validate_agent_state/built_checked_pending_publication_basis/
  _collect_pending_rows/resolve_checkpoint_artifact/_resolve_checkpoint_artifact/
  resolve_active_screening_acceptance/resolve_active_evidence_views`, `core.verify_state_basis`,
  `runtime_tool.current_stage_basis_override`, `screening._canonical_root_acceptance` State branch,
  `screening.resolve_effective_discovery_basis` State branch, `observe_current/renewal_authority`,
  Reader/Gate/Candidate/seal/full receipt/P1/P2R/P3S, `core.repository_commit_sha` AS AUTHORITY
  (allowed ONLY as pinned `current_tool_epoch` value recomputed from disk, never as gate),
  `pending_basis/already_verified/caller dicts/seal_path/ambient/cache`. Implementation MUST deliver
  static `ast` edge proof that no banned name is reachable from Layer-A/B (same audit as P3S).
- DAG fixed (R2-I §6 superseded): `prior history + fresh before-State/selection + unchanged accepted
  inputs → _observe_renewal_entry(HIGH, no basis) → exclusive COPY claim+inventory → basis LAST +
  pin recheck → observe_renewal_authority(HIGH, basis-bound) → load_renewal_accepted_authority
  (SOURCE leaf, persisted basis_path) → pure projection AFTER authority → source proof → **Layer-B
  post-proof node (CURRENT closure/contract/schema + HIST verdict, still NO State)** → C trio FILES
  (C only) → C manuscript + real disposable build/transfer (C only, after proof, both before external
  review) → build record (REUSED vs EXECUTED) → receipt (AFTER build-record) → fresh QA + postrender
  reviews → QA/Gate/Candidate (SAME proof ref) → seal LAST → validate → activate → normal active
  Candidate → direct stage → synthetic Preview/Freeze/Release`. After-activation readback edge:
  `validate_candidate:749-814 → validate_manuscript_manifest:413-451 (reloaded renewal_source_proof_ref)
  → verify_renewal_source_proof (Layer-B 1-3)` rejects further Core drift WITHOUT live-before equality
  (live-before stays HIGH write-boundary-only). Detached `validate_renewal_basis` validates RETAINED
  before-State only. HIGH NEVER runs on readback; detached NEVER calls `observe_renewal_authority`.
- Ancestor stale-epoch rule: Layer-B current recompute NEVER revalidates ancestor proofs as current;
  ancestors use HIST structural branch only (record-epoch blobs + `HISTORICAL_IDENTITY_VERIFIED`).
  Current proof stale after further Core commit → `BASIS_CURRENT_TOOL_DRIFT` (fresh basis required),
  not ancestor current-replay.

Allowed-caller edge (low→history): low structural selection MAY call history
(`verify_versioned_history`); history MUST NOT call selection back (no State recursion). HIGH
`verify_renewal_history` delegates to HIST typed loader; historical structural loading of renewal proof
does not execute current-replay branch.

## 10. Remaining exact maps (closes review §10)

- Digests (canonical order = SOURCE insertion order for writer bytes; equality is value equality via
  `core.sha256_object(sort_keys=True)` + `_norm` sorted-set for lists — never "stored sorted AND
  byte-verbatim" contradiction): manuscript 14-key base excl self (`:427-442`) + optional 15th
  (`editorial_source` `:443-447` XOR `renewal_source` C-only); review 14 keys
  (`schema_version,issue_id,research_profile,publication_profile,review_kind,status,
  production_profile,reader_manuscript,source,pdf,page_count,checks,reviewed_by,recorded_at`
  `:617-636`); bundle 9-key base excl self (`:213-224`) → 10-key renewed base excl self (§1);
  Gate 13-key base excl self (`:1650-1685` / `:1737-1753` digest fields) with new 5th variant value;
  Candidate 10-key base excl self (`:730-743`) → 11-key renewed base excl self (§1); basis/proof/
  receipt/seal EVERY declared field except one self-digest; file-ref SHA is full serialized bytes,
  distinct from self-digest. State base-without-self vs required-incl-self per §1 (manuscript required
  15 incl self; candidate required 11→12; bundle required 10→11; Gate required 14 incl self).
  `accepted_refs` file-bytes order MUST be writer sorted order (`:1885`); comparison sorted-set (§5).
  `authoring_refs` file-bytes order MUST be SOURCE order `[proposed, accepted]`; comparison sorted-set.
- Freeze snapshot (FINITE typed-ref function, replaces "all reachable evidence"; no generic walker):
  `renewal_freeze_snapshot_set(validated Candidate C, seal S, basis B, proof P) =
  {C.path,approval.path,visual.path,bundle.path,profile.path,manuscript.path,source.path,pdf.path,
  semantic_review.path}` (existing 9 `:213-229`) `∪ {S.renewal_basis_ref.path,S.renewal_proof_ref.path,
  B.retained_copy_ref.path, P.output_trio_refs.{primary,bibliography,style}.path,
  B.old_tool_epochs.receipt_epoch closure rows (names §6.1–6.2, old SHAs — pinned list),
  B.current_tool_epoch.closure rows (names §6.1–6.3 per-route 63, new SHAs — pinned list),
  C.renewal_source_proof_ref.path (=P.path), Gate.renewal_receipt_ref.path (=receipt.path)}`
  deduped by exact `(path,sha256)`; each `_safe_file` + `sha256_file` into `{rel:sha256}`;
  `_recheck_snapshot:248-256` fails on delta (fresh id, never in-place overwrite).
  `_preflight_freeze_pair` authority/overlap checks (`authority_raw:359-376`,
  `identities/spellings:377-390`) extended with SAME finite set (proof/basis/retained COPY/closure rows
  as typed refs); target/input aliasing refuses. External C postrender review RECORDs ARE snapshot
  members (pinned, not writer-owned, never deleted/rewritten; writer paths cannot alias supplied paths);
  directory inventories pinned by exact file list (no untracked sweep; exclusive inventory = explicitly
  declared evidence files inside `R` + pinned externals, per `operation-oracles.md` §0 rule).
- Bootstrap tripwire grep DELIVERED (not OPEN): pre-code `grep -rn` for State-contract equality outside
  Layer-B-2/HIST split finds ONLY current-vs-current safe checks: `survey_agent_control_v2.py:325-329`
  (`report.contract != current disk contract`, current-vs-current), `survey_stage_validation_v2.py:749`
  + `survey_editorial_publication_v2.py:1121,1807` (current recompute), `survey_production_v2.py:980`
  (State-gated current expected), `survey_weekly_derivation_v2.py:748` + `generated_v2.py:695`
  (current receipt replay). NO old-State stored-contract equality for renewal paths; historical
  `survey_editorial_correction_proposal_v2.py:1713` (`receipt.contract != current`) and
  `survey_weekly_mechanical_refresh_v2.py:1120-1121` (old receipt vs current) are R1/canonical paths
  kept under pre-write refusal in versioned mode (decision §8), not renewal admission. If any new
  equality outside Layer-B-2/HIST is introduced → precise NO-GO with `file:line`.
- Repeat/renewal→editorial DAG edges (R2-I U/C order superseded): second-renewal entry (prior = prior
  `R`, `staged_epoch` ABSENT per §2, anchor never rolled forward, `supersedes` chain) + renewal→editorial
  P1 repeated pre-Preview (prior immutable versions KEEP + fresh State COPY via `capture_retention:857+`,
  `_expected_retained_dest:831`, `verify_retention:1737-2086` mapping only, never as historian; P1
  identical-reader refusal preserved; original P2V epoch checks preserved; R1×2→editorial→renewal anchor
  preserved). All MANDATORY same-unit capability tests, not existing-module claims.

## 11. Entries, CLI, faults, oracles (consolidates R2 operation-oracles §§1–6 + R2 corrections)

Entries (all paths `str|Path` repo-local no-follow; all refs untrusted fully reloaded: lexical →
`_safe`, bounded read, strict JSON, CURRENT-disk schema for E docs, self-digest recompute, live SHA/size,
cross-bind, pin recheck after work; no caller dict/verified set/`pending_basis`/`already_verified`/
route-kind enum/`seal_path`/ambient/cache; `recorded_at` via `core.parse_instant/iso_utc`):

```text
_observe_renewal_entry(root,state_path) -> {state,state_sha,prior_history:{seal,receipt,proof_or_staged,
 retention,scope_refs,epochs},current_nonpublication_authority,current_tool_predicates,pins}
 # HIGH private before capture; in-memory pins only; no basis yet; no verified out-param.
prepare_renewal(root,state_path,renewal_id:RID,intent:REUSE_TARGETS|RENDER_TARGETS,
 manuscript_spec_path,toolchain_spec_path|None,executor,recorded_at)
 -> {renewal_dir:R,basis_path:R/renewal-basis.json,retained_copy:R/retained/before/<rel>,pins}
 # U: toolchain_spec_path MUST be None (CLI omits --toolchain-spec); no build spawn.
 # C: toolchain_spec_path REQUIRED (explicit spec, rechecked, never synthesized).
load_renewal_accepted_authority(root,basis_path) -> {surface,records,accepted_refs,authored_refs}
validate_renewal_basis(root,basis_path) -> {basis,retained,unchanged_evidence}
verify_versioned_history(root,record_path) -> {HISTORICAL_IDENTITY_VERIFIED,observed_refs}
observe_renewal_authority(root,state_path,basis_path) -> {live_current_before,retained_before,
 selected_predecessor,current_tools,pins}  # after basis, before finalize, immediately before activate
finalize_renewal(root,state_path,basis_path,checks_path,semantic_review_path|None,
 visual_review_path|None,executor,recorded_at) -> {set_path:R/publication-set.json,seal,pins}
 # NULL reviews ONLY for validated U (derive predecessor RECORD refs; replacement at different path
 # never silently reused). C requires new postrender reviews at exact new targets + actual QA.
validate_renewal_receipt(root,receipt_path) / validate_prepared_renewal_set(root,state_path,set_path)
activate_renewal(root,state_path,set_path,reason,executor,recorded_at)  # reason free-text Core-change;
 # reason_class fixed REVIEWED_VERSIONED_CORE_RENEWAL, never from CLI flag
resume_renewal_activation(root,state_path,record_path)  # reloads record+set+basis; compares COMPLETE
 # §11.1 intent (branch/issue/checkpoint/anchor/supersedes/before-State/digest/Candidate/set/basis/
 # new-core/executor/reason/time), not set SHA alone; recompute before_active_digest via existing
 # effective7+Candidate; basis/proof covered by new set/record refs
verify_renewal_history(root,record_path)  # HIGH wrapper delegating to verify_versioned_history
verify_renewal_rerender_equality(root,basis_path,proof_path) -> {reader_equal,trio_equal,disposition}
 # U NEW: CURRENT renderer/style → disposable temp trio + complete reader vs OLD prior-relative bytes
 # at PRIOR paths; never P/publication vs R confusion; mismatch → REUSE_TARGET_MISMATCH, no auto-C
```

Errors: `EditorialError(code,phase,disposition,detail)` (`.code/.phase/.disposition/.detail`
`survey_editorial_publication_v2.py:181-191`); low `PublicationSetError` (`CHAIN_LIMIT=32`
`survey_publication_set_v2.py:109`). Codes: `HISTORY_*` (`HISTORICAL_IDENTITY_VERIFIED` vs
`HISTORY_COMMIT_MISSING/HISTORY_BLOB_MISSING/HISTORY_SCHEMA_MISSING/HISTORY_DIGEST_MISMATCH/
HISTORY_ANCESTOR/HISTORY_MODE/HISTORY_TOOL_EPOCH_DRIFT/HISTORY_PACKAGE_MUTATED`), `BASIS_*`
(`BASIS_ENTRY_INELIGIBLE/BASIS_ACCEPTED_SET_DRIFT/BASIS_ACCEPTED_SHA_DRIFT/BASIS_STATE_PATH_IDENTITY/
BASIS_ACCEPTANCE_BINDING_DRIFT/BASIS_ISSUE_PROFILE_DIVERGENCE/BASIS_CURRENT_TOOL_DRIFT/
RETAINED_COPY_MISSING`), `RENEWAL_PROOF_*`, `REUSE_TARGET_MISMATCH`, `UNSUPPORTED_MIGRATION`
(+ `CONTRACT_MISMATCH/CLOSURE_SET/CODE_DEPS_EXPANSION_REQUIRED/TOOL_DRIFT/STYLE_MISMATCH/
REPLAY_MISMATCH` with missing/extra/drift lists), `REVIEW_TARGET_MISMATCH`, `RECORD_COLLISION`,
`INTENT_MISMATCH`/`INTENT_COLLISION`, `INDETERMINATE`, readonly `ALREADY_ACTIVE`.
CLI: `prepare/finalize/validate-receipt/validate-set/activate/resume/history` in new high module
(`--state/--renewal-id/--intent/--manuscript-spec/[--toolchain-spec U-absent/C-required]/--basis/
--checks/[--semantic-review/--visual-review U-null-only]/--receipt/--set/--reason/--executor/
--recorded-at/--record`); success `0`, refusal-or-operation-failure `2` (`main():3914-3917` discipline),
unexpected nonzero never PASS. Structured `phase,code,disposition`, primary/secondary errors, observed
State status on stderr.

Faults (every record/State write/close/fsync/replace/postread/foreign-inode seam, decision §7 six rows +
§11.1 taxonomy; snapshot window entry pins → basis LAST → proof → build-record → receipt → QA/Gate/
Candidate → seal → validate → activate/resume; pins rechecked BEFORE capture, AFTER basis
(`observe_renewal_authority`), BEFORE finalize, IMMEDIATELY BEFORE activate, AFTER each phase
(`prepare:1610-1611`, finalize `2047-2054`, Freeze `_recheck_snapshot:248-256`); any drift refuses +
repair per table): `TARGET_EXISTS` (exclusive `O_CREAT|O_EXCL|O_NOFOLLOW` claim must refuse, precedents
`survey_editorial_publication_v2.py:493,1577,1617,1627,2138,2221,2267,2317,3152,3387,3545`), close/fsync/
replace/postread mismatch/foreign-inode (`st_dev,st_ino` per Freeze `:377-390`); preserve PRIMARY+
SECONDARY + observed old/new/unknown; incomplete → `PRESERVED_INCOMPLETE` + fresh id (no takeover/
cleanup); inert-seal-no-record → explicit `activate_renewal`; record-exactly-before → explicit
`resume_renewal_activation` with §11.1 full intent; expected-after → readonly `ALREADY_ACTIVE` (full
strict active readback, no regenerated approval); neither/unsafe → `INDETERMINATE` preserve (no
rollback/overwrite/adoption/deletion). Healthy control for every fault (same operation without fault
→ expected disposition) proves seam. No global CAS/crash atomicity.

Positives (real accepted fixture graphs, genuine eligible pinned Core changes, both routes, both cases;
synthetic approvals labelled; production semantic NO-GO retained): **P-U1** (Weekly U after genuine
pinned implementation change leaving trio/reader bit-identical; `toolchain None`; entry→COPY/basis
(`REUSE_TARGETS`)→proof (`REUSED_TARGETS`)→reused-build wrapper/receipt→fresh QA→Gate (early scope,
proof+receipt-bound)→Candidate (SAME proof)→seal→activate→active readback→normal active Candidate→
direct stage→synthetic Preview/Freeze/Release; old bytes preserved; bootstrap from actual R3 authority
under real older tool source); **P-U2** (Longform U same); **P-C1** (Weekly C after current-source change;
`RENDER_TARGETS` + explicit spec; derived trio → proof (`NEW_TARGETS`) → C manuscript + real disposable
build/transfer → `EXECUTED_BUILD` (`exit_code==0`) → receipt → NEW external postrender semantic+visual at
exact new targets + actual QA → QA/Gate/Candidate → seal → activate → lifecycle; old closed4 untouched);
**P-C2** (Longform C same); **P-S1** (source-only/comment-only → C; same-trio/different-PDF incl
metadata-only → C with new visual; byte-derived U/C; same SHA different path is C);
**P-N1** (active normal Candidate → direct stage → synthetic Preview/Freeze/Release; State-selected
Candidate/proof; full normal validations; Profile-bound Freeze/Manifest; producer AND loader recomputed
hash comparison; unsupported handoff explicitly refused); **P-N2** (bootstrap + steady-state + repeat with
new Core commit + renewal→editorial via P1 repeated pre-Preview KEEP/COPY + R1×2→editorial→renewal anchor
permanent + `ALREADY_ACTIVE` readonly retry; mixed chain max32/sequence/time/cycle/anchor; R1/canonical
pre-write refusal in versioned mode); **P-N3** (history/current readback + readonly already-active retry;
HIST descriptive, detached retained-only, HIGH live-before at write boundaries only).
Negatives hit intended seams (earlier refusal ≠ later-seam evidence): **N-H1** stale validators refuse
without proof; **N-H2** same-SHA different targets/proofs; **N-H3** false reason (no P1/canonical laundering);
**N-H4** reader/research/Profile delta; **N-H5** unsupported contract/recipe/schema migration; **N-H6**
forged tool row/epoch/blob; **N-H7** tool-KEEP vs evidence-KEEP + absent-from-tool-commit positive control;
**N-H8** forged package/acceptance/State basis (§11.3 six conditions); **N-H9** fake `SCOPE_BOUND`;
**N-H10** U mismatch; **N-H11** C missing/stale postrender + no fresh QA + proof mismatch; **N-H12** inert
rival Candidate; **N-H13** foreign/missing COPY + postactivation without before-State; **N-H14**
32/33/cycle/anchor + every ownership/write fault; **N-H15** Freeze nested review without proof + proof/basis/
COPY/closure mutation + target alias (`_prepare_freeze_inputs:171-245`, `_preflight_freeze_pair:323-390`,
`_recheck_snapshot:248-256`). Fixture/source epoch discipline (independent DB, inert origin, no alternates/
hardlinks/sharing, no reconstruct-DB fixtures, no `--allow-empty`, code committed before authorities, no
ordinary candidate commits, full run bookkeeping) per `operation-oracles.md` §6.

## 12. Gate checklist (all MAP; implementation BLOCKED until Astra confirms)

- [x] §1: 5-file amended list + per-file branch/digest/old-new pins; "new files only" deleted.
- [x] §2: `staged_epoch` conditional + repeat-chain epoch rule + HIST entry + E/T/C trichotomy.
- [x] §3: U prior-relative + `C→U` oracle + `REUSED_BUILD` chain.
- [x] §4: per-schema `{epoch,sha}` + blob-read rule + overlap agreement.
- [x] §5: authoring SOURCE order + accepted sorted-set via `_norm`; example fixed.
- [x] §6: ONE closed 63 (66 union) with per-file provenance + `file:line` import-edge proof + gate updates
  + pipeline 67→71 (schemas only) + runtime-vs-contract split + steady-state predicate.
- [x] §7: `versions`/`argv`/`env` exact schemas + variant branches + receipt-after-build.
- [x] §8: `CLOSED`→RULE-FIXED/MAP-COMPLETE; `GO-CONDITIONAL` deleted; per-family extraction MAP + oracles.
- [x] §9: Layer-B number fixed + allowed-import `ast` proof obligation + post-proof/readback DAG nodes +
  low→history edge + ancestor HIST-only rule.
- [x] §10: digest key orders + Freeze externals/inventory/no-walker + tripwire grep delivered + repeat/
  renewal→editorial edges.
- [x] §11: entries/signatures/errors/CLI/faults/positives/negatives/fixture discipline (this R3 + adopted
  oracles, no deferred map).

**Honest status:** R3 closes every mechanical pre-code map item the independent review marked
CHANGES_REQUIRED. No open mandatory MAP item remains in this integration. Remaining work is
IMPLEMENTATION (code/tests/build/fixtures per §§6–11 + meaningful regressions for affected original
routes/R1/DM004 with source/run/skip/failure/quota bookkeeping; no unrelated-suite decoration) +
Astra confirmation of this R3 + Human continuation. **Implementation stays BLOCKED until Astra confirms
this R3.** Any unpreservable predicate found in implementation → contract revision or precise NO-GO
(`file:line` + required migration/separate-contract), never a weakened checker/hash-only/caller-dict/
`pending`/ambient/same-byte-takeover/retrospective-PASS/genuine-approval laundering. Whole NOT_READY/
step4B3 OPEN/audit unstarted/DM021+022 OPEN. Stop at internal return; no code, no ordinary Commit/Push
(Human-owned).

(End — R3 supersedes listed R1/R2 occurrences; R1/R2 preserved unchanged; no independence claim;
no runtime evidence; no adoption/approval/audit claims.)
