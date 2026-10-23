# Versioned same-reader renewal — integrated pre-code R5 (author-side delta, Astra 2 fatals)

2026-10-23 JST. Fresh AUTHOR-side integration worker, NOT independent review.
Governing: `outputs/rephase-1-versioned-renewal-contract-decision.md` SHA256
`478f00510791b76af24aa7d61f398f0608f7ad8ae7808008c660f2bea6fbfdcf` INCLUDING §11;
mandatory `notes/rephase-1-versioned-renewal-contract/astra-review-resolution.md`;
BOTH independent design reviews WITH final-binding addenda; R2 returns;
`independent-readiness-review.md` §§0–12 + final-binding R3 addendum §§134–205;
R3 822 lines SHA256 `d080c182b1e627467c2c6c001408233db0e77669e1fbb8f74814c28a518d6402`;
R4 492 lines SHA256 `b8e422bb214448113cc64b33272efe8be4a05c42aae4fc88139c87426f3479a5`
(DELTA-COMPLETE claimed, Astra REJECTED as `5/5 map closed`);
Astra R4 rejection (2 fatal invariants + rest review + bootstrap honesty rule).
Read-only source: `.rephase-1-editorial-runtime/final-source-packaging/proof-copy/candidate-partial-b40de60`
(actual409/tree8ce + intended57). No source edits/runtime code/imports/tests/build/fixture/
restore/network/Git writes. This file `integrated-precode-r5.md` (+ twin `.json`) is the ONLY write
in this unit. R3/R4 preserved as submitted (not edited). Method: `Read` + read-only `bash`
(`grep -rn`, `python3 -c` stdlib `json`/`ast`/`pathlib`, NO project imports, NO repo-code execution).
All `PC` citations verified 2026-10-23 in this unit.

## 0. Scope, verdict, supersession (read first — honest, not all-closed)

**Status: R5 DELTA-MAP for Astra 2 fatals as specified below; REMAINING MAP RISK retained on
bootstrap HIGH call-list completeness (§3). NOT self-certified all-closed. Implementation remains
BLOCKED until Astra confirms R3+R4+R5 jointly per decision §§9/11.3.** This R5 supersedes ONLY:

- R4 §1 (`supported_epochs` `(kind,name)` unique + 8×generations + invented `sha256`) — REPLACED by §1
  OBSERVED SOURCE BINDINGS (finite typed rows derived from history graph, owner registry, same
  representation for basis/proof, no 256/8 caps, explicit array-order hash).
- R4 §2 (`stored P1 must equal immediate prior seal proof P2`, `NEW distinct by construction` for all
  cases) — REPLACED by §2 lineage-reachable stored proof + immediate-bind NEW proof + C-normal
  `embedded==expected` allowance (§2).

All other R4 sections RETAINED with review in §3 (71-table, build container with §4 clarification,
tripwire/HIGH adapter with honesty note). Silence is not supersession. No new modules/schemas beyond
R3 fixed 3+4 (build container remains embedded `$defs` in `versioned-renewal-source-manifest-v2`,
R4 §4; `supportedEpoch` `$defs` in `versioned-renewal-source-proof-v2` is REPLACED by §1 shape in the
same host file, still fixed 4). No `EXECUTED_BUILD` as old kind; no extra unregistered artifact.
No extra authority token: bindings arrays are descriptive observed refs (like
`HISTORICAL_IDENTITY_VERIFIED`), never a consumable permit; every use reloads by persisted path.

If any §1–§2 definition proves unimplementable without weakening → precise NO-GO with `file:line`.
Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN. Production semantic NO-GO.

## 1. Observed source bindings (replaces R4 §1; closes Astra fatal 1)

R4 §1 fails as stated by Astra and is REPLACED in full (conditional PRESENT/ABSENT logic for
`staged_epoch` is also REMOVED as a compound field; derivation below yields the exact list):

- `(kind,name)` unique vs 8×generations impossible with real Core changes: R4 forced same
  `(kind,name)` to one `(epoch,sha)` across generations, forbidding genuine tool change. Fixed by
  per-source-row key below (different owners/epochs permitted different hash as genuine history).
- `sha256 = git show <epoch>:<schema-or-closure-path>` undefined for receipt full closure: receipt
  closure is a NAME LIST (`current_tools.closure: NamedRow[1..]`), not one blob. Fixed by
  receipt/staged rows carrying NO invented hash — historian checks EVERY closure row against the commit.
- `sort_keys=True` does not ignore ARRAY order: R4 "order immaterial to hash" is wrong for arrays.
  Fixed by canonical storage order = sorted-key order, hash over ordered serialization (§1.3).
- Overlap commit equality across generations forbids actual change: R4 required same commit where rows
  overlap across ancestors. Fixed by same-operation overlap match vs cross-generation change allowance
  (§1.5).

### 1.1 Exact row shape (one choice, in `versioned-renewal-source-proof-v2` host `$defs`, fixed 4 kept)

```json
"observed_source_bindings": {
  "type": "array", "minItems": 1,
  "items": {"$ref": "#/$defs/observedSourceBinding"},
  "uniqueItems": true
}
// $defs.observedSourceBinding:
{
  "type": "object", "additionalProperties": false,
  "required": ["source_ref","binding","repository_commit_sha"],
  "properties": {
    "source_ref": {"type": "object", "additionalProperties": false,
      "required": ["path","sha256"],
      "properties": {
        "path": {"type": "string","minLength": 1},
        "sha256": {"type": "string","pattern": "^[0-9a-f]{64}$"}}},
    "binding": {"enum": ["RECEIPT_CURRENT_TOOLS","STAGED_PRODUCER","SCHEMA"]},
    "repository_commit_sha": {"type": "string","pattern": "^[0-9a-f]{40}$"},
    "schema_path": {"type": "string","minLength": 1},
    "schema_pointer": {"type": "string","minLength": 1},
    "schema_sha256": {"type": "string","pattern": "^[0-9a-f]{64}$"}
  },
  "allOf": [
    {"if": {"properties": {"binding": {"const": "SCHEMA"}}},
     "then": {"required": ["source_ref","binding","repository_commit_sha","schema_path","schema_pointer","schema_sha256"]}},
    {"if": {"properties": {"binding": {"enum": ["RECEIPT_CURRENT_TOOLS","STAGED_PRODUCER"]}}},
     "then": {"not": {"anyOf": [{"required": ["schema_path"]},{"required": ["schema_pointer"]},{"required": ["schema_sha256"]}]}}}
  ]
}
```

- RECEIPT/STAGED rows: `source_ref` = actual receipt (`P/.../validated-source-manifest.json` or
  `R/validated-source-manifest.json`) or staged manifest (`P/staged-source/staged-source-manifest.json`)
  file in the history graph (path+SHA of that validated doc); `repository_commit_sha` comes from the
  ACTUAL field (`receipt.current_tools.repository_commit_sha`, `staged.producer_head`
  `PC/scripts/survey_editorial_staged_source_v2.py:1039`); NO `schema_*`, NO invented closure hash.
  Historian checks EVERY corresponding closure row against the commit with exact expected
  membership/bytes/modes (`_route_code_deps`/`_editorial_closure_rows`/`current_closure` member-wise
  + `git show <commit>:<path>` SHA + `git_mode:100644` vs physical `0o664` distinction per R3 §2;
  missing → `HISTORY_BLOB_MISSING`).
- SCHEMA rows: `source_ref` = validated document bytes in the history graph (e.g. proposal file,
  retention manifest, staged manifest, receipt, set, build record, manuscript, candidate, bundle, gate,
  revalidation record, renewal basis/proof/manifest/set/record); `repository_commit_sha` DERIVED by
  finite typed owner registry (§1.2), NOT caller choice; `schema_path` = exact schema file
  (e.g. `schemas/editorial-correction-proposal-v2.schema.json`); `schema_pointer` = fixed registered
  JSON pointer (§1.2, `/` = whole doc or `/properties/<branch>` etc); `schema_sha256` =
  `git show <derived-epoch>:<schema_path>` SHA. Unknown source/schema/pointer/epoch → refuse
  (`UNSUPPORTED_MIGRATION` for unknown registry, `HISTORY_BLOB_MISSING` for missing blob,
  `HISTORY_TOOL_EPOCH_DRIFT` for mismatch). No remote `$ref` (all local `#/$defs/*`, verified).
- Sorted unique key: `(source_ref.path, binding, schema_path|"", schema_pointer|"", repository_commit_sha)`
  lexicographically sorted; `uniqueItems:true` on that key; conflicting `source_ref.sha256` for same
  `(path,binding,…)` → `HISTORY_DIGEST_MISMATCH`; different owners/epochs permitted different
  `schema_sha256`/`source_ref.sha256` as genuine history (no cross-generation commit-equality demand).
  No arbitrary `256` cap / `8` per record: exact list derived from bounded typed chain32
  (`_walk_chain_backwards:1023-1051`, `CHAIN_LIMIT=32`) × finite registered families (§1.2);
  per-document unique typed rows; duplicates/omissions/extras → refuse (`HISTORY_DIGEST_MISMATCH` /
  `HISTORY_TOOL_EPOCH_DRIFT`). Canonical storage order = sorted-key order; proof hash serializes the
  array AS ORDERED (`core.sha256_object` `sort_keys=True` sorts OBJECT keys only, NOT array order
  `PC/scripts/survey_production_v2.py:163-166` — R4 "immaterial" corrected here).
- Basis vs proof SAME representation (no compound conditional ambiguity): authoritative field is
  `basis.observed_source_bindings` (observed at capture from history graph via §1.4 walk); proof field
  is `proof.supported_source_bindings` with IDENTICAL row shape above and rule
  `proof.supported_source_bindings == basis.observed_source_bindings` exactly (sorted-set equality on
  the full row tuple). R3 `old_tool_epochs` compound `{receipt_epoch,staged_epoch,schema_epochs}` map
  and R4 `(kind,name)` map are both REMOVED as containers (values preserved as rows above). No duplicate
  old field map remains; no `staged_epoch PRESENT/ABSENT` conditional field — absence is simply no
  `STAGED_PRODUCER` row for renewal ancestors (proof IS staged proof). No extra authority token:
  arrays are descriptive, reload-by-path every use, never a permit.

### 1.2 Finite typed owner registry (epoch DERIVED, not caller; includes new4+modified5+old + contract-bound)

`repository_commit_sha` for SCHEMA rows is DERIVED by this registry from history-graph fields:

| # | Validated doc (history graph `source_ref.path` type) | Schema (`schema_path`) | Pointer (`schema_pointer`) | Epoch owner (typed derivation) |
|---|---|---|---|---|
| O1 | `P/proposal.json` (editorial proposal) | `schemas/editorial-correction-proposal-v2.schema.json` | `/` | staged producer_head of the staged manifest materialized from this proposal (`staged.producer_head:1039`; P1/P2R/P3S from staged producer) |
| O2 | `*/retention-manifest.json` (P retention or `R/retained/before` COPY binding record) | `schemas/editorial-retention-manifest-v2.schema.json` | `/` | same staged producer_head as O1 (retention plan fixed at staged time) |
| O3 | `P/staged-source/staged-source-manifest.json` | `schemas/editorial-staged-source-manifest-v2.schema.json` | `/` | own `producer_head` (self; `:1039`) |
| O4 | `P/publication/validated-source-manifest.json` or `R/validated-source-manifest.json` (editorial/renewal receipt) | `schemas/editorial-publication-source-manifest-v2.schema.json` for P; `schemas/versioned-renewal-source-manifest-v2.schema.json` + `#/$defs/buildRecord` host for R (R4 §4) | `/` | own `current_tools.repository_commit_sha` (editorial receipt/set/activation from receipt tool commit; renewal receipt from its own basis CURRENT epoch) |
| O5 | `P/publication/publication-set.json` or `R/publication-set.json` (seal) | `schemas/editorial-publication-set-v2.schema.json` for P; `schemas/versioned-renewal-publication-set-v2.schema.json` for R | `/` | editorial: receipt tool commit; renewal: its own basis CURRENT epoch (`basis.current_tool_epoch.repository_commit_sha`) |
| O6 | `P/publication/build-record.json` (old terminal) | `schemas/editorial-publication-build-record-v2.schema.json` | `/` | own build record tool context + original receipt binding (old build terminal own build-record/original-receipt binding; kind `EDITORIAL_PUBLICATION_BUILD_V1:24`, `required`13) |
| O7 | `R/build-record.json` (new) | host `versioned-renewal-source-manifest-v2` `#/$defs/buildRecord` (`REUSED_BUILD`/`EXECUTED_BUILD`, R4 §4) | `/$defs/buildRecord` | renewal: its own basis CURRENT epoch (R4 §4) |
| O8 | `schemas/editorial-toolchain-spec-v2` instances + `schemas/editorial-manuscript-spec-v2` instances (specs) | respective spec schemas | `/` | receipt tool commit for P specs; basis CURRENT epoch for R specs (`toolchain_spec_ref`/`manuscript_spec_ref` in basis, decision §5) |
| O9 | `templates/survey/jgaisurvey.sty`, `.latexmkrc` (old templates) | N/A (bytes + `REQUIRED_RECIPE_MARKERS`/`FIXED_RECIPE_STEPS`/`EXPECTED_ARGV_*` `:60-74,:1183-1244`) | N/A (closure row, not SCHEMA row) | staged producer_head for style bytes; receipt tool commit for recipe markers (checked as closure rows via RECEIPT/STAGED bindings, not SCHEMA rows) |
| O10 | `R/renewal-basis.json` | `schemas/versioned-renewal-basis-v2.schema.json` | `/` | own `current_tool_epoch.repository_commit_sha` (renewal basis/proof/set/record from its own basis CURRENT epoch) |
| O11 | `R/renewal-source-proof.json` | `schemas/versioned-renewal-source-proof-v2.schema.json` | `/` + `#/$defs/observedSourceBinding` for §1.1 rows | own basis CURRENT epoch |
| O12 | `R/reader-manuscript-v2.json` (C only) | `schemas/reader-manuscript-v2.schema.json` | `/properties/renewal_source` (C branch; U has no serialized branch, keyword only R3 §1) | renewal: its own basis CURRENT epoch |
| O13 | `R/publication-candidate-v2.json` (new U/C) | `schemas/publication-candidate-v2.schema.json` | `/properties/renewal_source_proof_ref` | renewal: its own basis CURRENT epoch |
| O14 | `R/quality-regression-bundle-v2.json` (new U/C) | `schemas/quality-regression-bundle-v2.schema.json` | `/properties/renewal_source_proof_ref` | renewal: its own basis CURRENT epoch |
| O15 | `R/reader-surface-gate-v2.json` (new U/C) | `schemas/reader-surface-gate-v2.schema.json` | `/properties/derivation/oneOf/4` (`VERSIONED_RENEWAL_V1`, R3 §1; 4 old verbatim) | renewal: its own basis CURRENT epoch |
| O16 | activation record (`State.publication_revalidation_provenance` new record) | `schemas/publication-surface-revalidation.schema.json` | `/oneOf/2` (`VERSIONED_RENEWAL_ACTIVATION_V1`, R3 §1; legacy/editorial verbatim) | editorial: receipt tool commit; renewal: its own basis CURRENT epoch + `core.implementation_commit_sha` |

Content research schemas (discovery/screening/evidence/X/ledger/completeness/matrix/selection/
architecture/draft/synthesis/cards/views, R4 §3 rows 24–67) are CONTRACT-BOUND, not epoch-fabricated:
bound via recorded `contract_identity` aggregate (`pipeline_files + [DEFAULT_CONFIG,PROFILE_SCHEMA,
STATE_SCHEMA]` `:210-228`, `aggregate_file_hash` sorted `rel\0bytes\0` `:168-178`) + Layer-B-2
current-equality predicates (CURRENT closure member-wise + `contract_identity` recompute vs
`proof.supported_contract`, R3 §§6/9). No SCHEMA epoch rows for them; unknown schema/pointer/epoch
refuses. All used shared schema/prompt files bound exact per R4 §3 71-table (retained).

### 1.3–1.5 Predicates (exact)

- HIST walk (§1.1 key): for each ancestor record in chain32, emit exactly the required rows per §1.2
  (per-document unique typed rows). Historian verifies each RECEIPT/STAGED row's full closure list
  against its commit (exact expected membership/bytes/modes, `100644` vs `0o664` distinction) and each
  SCHEMA row's doc (`source_ref.sha256` live recheck) + `git show <derived-epoch>:<schema_path>` SHA +
  `schema_gate` validation at that epoch bytes + pointer branch. Same-operation receipt/staged overlap
  bytes/modes MUST match where contract requires (e.g. style bytes in both closures,
  `current_closure` vs `_editorial_closure_rows` filtered subset `:1146-1159`) — NOT commit-identical;
  across different generations allow changed tool bytes while E exact KEEP (live+retained-COPY, R3 §2).
- Proof hash: `proof_sha256 = core.sha256_object({all keys except proof_sha256})` with
  `supported_source_bindings` stored in sorted-key order; verifiers compare sorted-set equality on full
  row tuples AND byte-order equality to sorted order (mismatch → `HISTORY_TOOL_EPOCH_DRIFT`).
- No authority token: `observed/supported_source_bindings` are never passed as a verified-dict/caller
  permit; HIST returns descriptive `HISTORICAL_IDENTITY_VERIFIED` + observed refs; Layer-B consumes the
  verdict; every use reloads by persisted path (decision §§4/11.1 preserved).

## 2. U lineage (replaces R4 §2; closes Astra fatal 2)

R4 §2 binds stored P1 to immediate prior seal proof P2 and is FALSE for `C→U→U`:
C manuscript embeds P1; immediate prior U2 seal proof is P2 (P1≠P2 by new-R id) → R4 false-fails a
valid chain. R4 "NEW distinct by construction" is also FALSE for normal C (embedded==provided expected
is allowed). Both REPLACED below. Root proof-context untrusted-paths-fully-reload preserved
(decision §11.2).

### 2.1 Stored vs new (lineage-reachable, not immediate; no two-proof bypass)

- Stored source proof (HISTORICAL, immutable manuscript-carried): the `renewal_source:{path,sha256}`
  serialized in a C-derived manuscript is the EXACT source proof carried by that immutable manuscript
  (R3 §1 XOR) and reachable in the typed selected predecessor's history/materialization lineage
  (ancestor chain via `supersedes` + seal roles + `retained/before` COPY + receipt/proof refs), NOT
  necessarily the immediate prior seal's proof. HIST loads it by persisted path, checks path+SHA,
  recomputes self-digest, verifies its §1 bindings via record-epoch blobs (HISTORY ONLY, never current
  replay), and proves lineage reachability (stored proof's record is an ancestor of the selected
  predecessor's record via `_walk_chain_backwards:1023-1051`, same issue/Profile, no cycles; stale
  branch/fork → `HISTORY_ANCESTOR`). It is NEVER current authority for the new operation.
- Current new U proof (CURRENT, immediate-bind): explicit keyword `renewal_source_proof_ref`
  (`{path,sha256}`, reloaded, Layer-B verified per R3 §9) binds the IMMEDIATE prior seal
  (`prior_selected_ref` seal roles: trio/manuscript/build3/reviews at prior `P/` or prior `R/` paths,
  R3 §3 prior-relative) + the EXACT reused manuscript bytes (including its stored ancestor ref as
  opaque bytes) + the actual derived trio (`verify_renewal_rerender_equality` disposable temp vs prior
  bytes). U `REUSED_BUILD` chain follows the SAME lineage principle (terminal old-R3 kind
  `EDITORIAL_PUBLICATION_BUILD_V1` or new `EXECUTED_BUILD`, R4 §4 retained; no "must match immediate
  artifact producer" lie — intermediate `REUSED_BUILD`s may skip generations if the trio/manuscript
  bytes are bit-identical and lineage-reachable; break → `HISTORY_ANCESTOR`/`REVIEW_TARGET_MISMATCH`).
- Fallback when supplied proof absent: if `renewal_source_proof_ref` is absent and manuscript is C
  (has serialized `renewal_source`), validators validate the OWN embedded proof as CURRENT (reloaded,
  Layer-B 1–3); it MAY stale-refuse after further Core change (`BASIS_CURRENT_TOOL_DRIFT`, never
  silent pass). If manuscript is editorial standalone (has `editorial_source` only), old P3S current
  replay applies unchanged (standalone legacy path keeps current P3S refusal, N-H1). Presence of a proof
  never allows arbitrary other issue/branch/foreign lineage even at equal SHA: issue/Profile/branch/
  `supersedes`/selection lineage must match the State-selected predecessor (same generation chain);
  equal-SHA different-path/lineage → `REVIEW_TARGET_MISMATCH` (never silently substituted).
- Corrections to R4 "distinct" sentences: NEW U proof is DISTINCT from the STORED producer proof
  (P2≠P1 by new-R id for `U` after `C`); normal C validation of its OWN proof allows
  `embedded==provided-expected` (same proof path+SHA, reloaded, Layer-B verified) — R4 blanket
  "distinct by construction" is DELETED for that case. All proof-context paths are untrusted and fully
  reloaded every use (lexical → `_safe`, bounded read, strict JSON, CURRENT-disk schema for E docs,
  self-digest recompute, live SHA/size, cross-bind, pin recheck; no caller dict/verified set/
  `pending_basis`/`already_verified`/ambient/cache).

### 2.2 Dispatch + oracles (exact codes)

`validate_manuscript_manifest(repo,manuscript_path,*,issue_id,renewal_source_proof_ref=None)`:

1. Stored HIST (if payload has `renewal_source`): HIST lineage-reachability per §2.1 (ancestor of selected
   predecessor, same issue/Profile, record-epoch blobs). Failure → `HISTORY_ANCESTOR`/
   `HISTORY_DIGEST_MISMATCH`/`HISTORY_BLOB_MISSING`. Absence on first-U editorial is expected (HIST checks
   `editorial_source` historically instead).
2. Current NEW (keyword present): ALL U predicates (decision §11.2) + prior-relative trio + complete reader
   vs NEW proof. Mismatch → `REUSE_TARGET_MISMATCH` (exit 2, no auto-C). Keyword absent + C manuscript →
   §2.1 fallback (own embedded CURRENT, may stale-refuse); keyword absent + editorial → old P3S path.
3. Seal-selected NEW: full-set SAME-proof equality for NEW Candidate/QA/Gate/receipt/seal (NEW proof
   path+SHA; R4 §1 `supported_source_bindings` equality per §1). Mismatch → `REVIEW_TARGET_MISMATCH`.
4. Stale-prior: U at non-active `P/` when active predecessor is prior `R/` → `REVIEW_TARGET_MISMATCH`.

- Positive `C→U→U` (new, closes the fatal example): C (proof P1 at `R1/`, manuscript M1 embeds P1) →
  U2 (new proof P2 at `R2/` binding prior `R1/` trio/M1 bytes; stored P1 lineage-reachable HIST, P2
  immediate-bind CURRENT, NEW set bound to P2) → U3 (new proof P3 at `R3/` binding prior `R2/` trio/M1
  bytes; stored P1 STILL lineage-reachable via `R2→R1` ancestors HIST, P3 immediate-bind CURRENT to `R2`
  seal, NEW set bound to P3). R4 would false-fail U3 (P1≠P2); R5 passes (P1 reachable, P3 immediate).
- Negative sibling-branch (new): rival proof P1' at same SHA but different issue/branch/fork lineage
  (equal bytes, foreign `supersedes`/selection) presented as stored or NEW → `REVIEW_TARGET_MISMATCH`
  even at equal SHA (presence never launders lineage).
- `REUSED_BUILD` same principle: U2 `original_record_ref` may point to R1 `EXECUTED_BUILD` while U3
  points to R2 `REUSED_BUILD→R1`; terminal is old-R3 `EDITORIAL_PUBLICATION_BUILD_V1` or new
  `EXECUTED_BUILD`; no immediate-producer lie.

## 3. Review of rest R4 (§§3–5) with actual source (honest, especially bootstrap)

- R4 §3 (71-table): RETAINED as MAP (verified `PIPELINE_N 67/QUALITY_N 3`
  `PC/config/survey-production-v2.json:6`; 4 family in pipeline; 4 new absent pre-code delta 67→71
  schemas-only; 7/7 prompts present; `$ref` local `#/$defs/*` only; implicit 3
  `DEFAULT_CONFIG/PROFILE_SCHEMA/STATE_SCHEMA` `:contract_identity:210-228` + quality 3; X docs/prompts/
  schema rows 23/3–5/67 bound exact). ADDENDUM for §1: rows marked `closure-member` remain closure rows;
  their SCHEMA-epoch derivation now follows §1.2 owner registry (not R4 §1 `(kind,name)`); contract-bound
  rows (51 + implicit + quality) remain `contract_identity`-bound per R4 §3 (no epoch fabrication).
  No table error found; implementation must pin per-file SHA from manifest + current disk (§3 origin
  column) — MAP retained, code pending.
- R4 §4 (build container): RETAINED as MAP with §1 pointer clarification (host
  `versioned-renewal-source-manifest-v2` `#/$defs/buildRecord`, `staged_manifest_ref` ABSENT,
  renewal refs PRESENT, digest incl inputs/outputs, `additionalProperties:false`, old/new pins separate;
  `versions/argv/env` exactness per `:60-74,:1183-1244,:1336-1362,:1400,:1540` retained). Terminal label
  already `EDITORIAL_PUBLICATION_BUILD_V1` in R4 (correct); R5 §2 removes the immediate-producer lie for
  the chain. No schema error found; MAP retained, code pending.
- R4 §5 (tripwire/HIGH adapter): MAP PARTIALLY RETAINED with explicit honesty note (the only non-closed
  MAP risk in R5). Verified in this unit via the §5 `grep -rn` command: live report sites are
  current-vs-current SAFE (`agent_control:1601-1610` new checkpoint, `:1652-1668` live checkpoint,
  `editorial_pub:1121-1125/1807/3403` receipt/current/activation recompute, `stage:749-760` new report,
  `weekly:748-749`/`generated:695-696` receipt replay, `production:contract_identity` recompute);
  historical sites are record-owned (`agent_control:473-481` with `record.contract/record.implementation`,
  `:325-329/:333` DUAL historical branch); bricking sites are HIGH-AVOIDED on renewal paths
  (`production:978,980-981` `verify_state_basis`, `weekly:496,501,513-514` State/pending/checkpoint,
  `screening:325-350,442-489,503,647` canonical/override, `agent_control:503,652,684,999,2427` State
  validation, `current_stage_basis_override` everywhere). `_profile_and_source:208-236` `:230`
  (`profile.contract == state.contract`) is live-live SAFE (both live same generation; renewal HIGH calls
  it on LIVE State/Profile only) and is RETAINED; it is NOT an old-State-vs-new-contract compare.
  **What R5 cannot close as MAP alone:** the COMPLETENESS of the HIGH call/DON'T-call list (that no
  unlisted renewal HIGH path will transitively reach a bricking equality via a helper not in the grep,
  e.g. future `resolve_active_*` or orchestrator/handoff wrappers). The grep + adapter in R4 §5/R5 §1
  proves the LISTED sites are correctly disposed, but a pre-code MAP cannot prove the absence of an
  unlisted transitive edge without the implementation's static `ast` non-reachability proof (same
  discipline as P3S `:172-201` `CODE_DEPS_EXPANSION_REQUIRED`, R3 §9). Therefore bootstrap is
  **MAP-CONDITIONAL**: adapter rule closed, evidence command delivered, but final closure requires the
  implementation's `ast` proof + Astra code review. This is stated here instead of claiming closed.
  No Profile rebind occurs under the adapter (Profile path/bytes identical; contract advance separated
  as observed bindings vs current recompute); if implementation introduces such an equality →
  precise NO-GO with `file:line` (not a weakened checker). Existing stage calls current-only; no fake
  State is introduced by R5 (detached `validate_renewal_basis` validates retained bytes only, HIGH demands
  live-before only at write boundaries per decision §11.1).

## 4. R5 completeness + remaining work (real, no unproven all-closed)

- [x] §1: OBSERVED SOURCE BINDINGS shape + owner registry (O1–O16 + contract-bound) + sorted-key +
  array-order hash + cross-generation + basis/proof same representation (authoritative
  `basis.observed` → `proof.supported` equality, old compound map removed) + no authority token.
- [x] §2: lineage-reachable stored + immediate-bind NEW + absent-fallback + foreign-lineage refuse +
  C-normal `embedded==expected` allowance + `C→U→U` positive + sibling-branch negative + REUSED_BUILD
  same principle + untrusted-reload preserved.
- [x] §3: R4 §§3–4 retained as MAP (no table/schema error found; code pending); R4 §5 retained as
  MAP-CONDITIONAL with explicit `ast`-proof remainder (only non-closed MAP risk, stated above).

**R5 closes the 2 Astra fatals as MAP and corrects the R4 false-failure/false-distinct claims.**
Bootstrap HIGH remains MAP-CONDITIONAL pending the implementation `ast` proof + Astra code review;
all else in §§1–2 is MAP-exact per the shapes/predicates above. **Implementation stays BLOCKED until
Astra confirms R3+R4+R5 jointly.** Any unpreservable predicate in implementation → contract revision
or precise NO-GO (`file:line`), never a weakened checker/hash-only/caller-dict/`pending`/ambient/
same-byte-takeover/retrospective-PASS/foreign-lineage laundering. Whole NOT_READY/step4B3 OPEN/audit
unstarted/DM021+022 OPEN. Stop at internal return; no code, no ordinary Commit/Push (Human-owned).

(End — R5 supersedes R4 §§1–2 only; R3/R4 preserved; all other R3/R4 maps referenced, not duplicated;
no independence claim; no runtime evidence.)
