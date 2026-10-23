# Versioned same-reader renewal — integrated pre-code R4 (author-side delta, 5 items only)

2026-10-23 JST. Fresh AUTHOR-side integration worker, NOT independent review.
Human HEAD at read time `ce0de1a` lineage (root observed `main...origin/main` clean at task start).
Governing: `outputs/rephase-1-versioned-renewal-contract-decision.md` SHA256
`478f00510791b76af24aa7d61f398f0608f7ad8ae7808008c660f2bea6fbfdcf` INCLUDING §11;
mandatory `notes/rephase-1-versioned-renewal-contract/astra-review-resolution.md` (R1–R8);
BOTH independent design reviews WITH final-binding addenda;
author inventory `notes/rephase-1-versioned-renewal-contract/accepted-authority-predicate-map.md` (F1–F8);
R2 returns + `independent-readiness-review.md` §§0–12 (CHANGES_REQUIRED/NOT READY);
R3 `notes/rephase-1-versioned-renewal-precode/integrated-precode-r3.md` 822 lines SHA256
`d080c182b1e627467c2c6c001408233db0e77669e1fbb8f74814c28a518d6402` + twin `.json` SHA256
`1f758b0a2e65081830b60b12473b7593522ecf068773bb2595a6d245df581f` (MAP-COMPLETE claimed);
final-binding R3 review addendum `independent-readiness-review.md` §§134–205
(CHANGES_REQUIRED/NOT READY, 5 narrow gaps §§1–5, closeout list). Read-only source:
`.rephase-1-editorial-runtime/final-source-packaging/proof-copy/candidate-partial-b40de60`
(actual409/tree8ce + intended57). No source edits/runtime code/imports/tests/build/fixture/
restore/network/Git writes. This file `integrated-precode-r4.md` (+ twin `.json`) is the ONLY write
in this unit. R3 preserved as submitted (not edited). All R1/R2/R3/contract/resolution/review files
preserved. Method: `Read` + read-only `bash` (`grep -rn`, `python3 -c` stdlib `json`/`ast`/`pathlib`,
NO project imports, NO repo-code execution). All `PC` citations verified 2026-10-23 in this unit.

## 0. Scope, verdict, supersession (read first)

**Status: R4 DELTA-COMPLETE as MAP for the 5 addendum items; READY-FOR-ROOT-GATE on those items.
NOT self-certified GO. Implementation remains BLOCKED until Astra confirms R3+R4 jointly per
decision §§9/11.3.** R3 `MAP-COMPLETE` label was rejected at gate; R3 is preserved (not rewritten).
This R4 supersedes ONLY the exact R3 occurrences listed below; every other R3 section is REFERENCED
unchanged (not duplicated). Unaffected R3 maps retained precisely:

- R3 §§0–1 (bindings, 5 amended + 4 new schemas, digests, pins), §4 (per-schema `{epoch,sha}`),
  §5 (authoring/accepted ordering), §6.1–6.3/6.5 (63/66 closure, provenance, import edges, gates,
  pipeline delta principle), §§8–9 (Layer-A/B, shared cores, DAG, allowed/banned imports, ancestor
  HIST-only, low→history edge), §10 digests/snapshot (counts/order/externals/inventory),
  §11 entries/CLI/faults/positives/negatives/fixture discipline — RETAINED, see R3 verbatim.
- R4 supersedes: R3 §2 lines 214–215 `supported_epochs` union sentence + R2-I §2.2 tuple
  (replaced by §1); R3 §§1/3/9 U-after-C dispatch gap (replaced by §2); R3 §6.4 content-contract
  examples-only list (replaced by §3 full 71-table); R3 §3 lines 267–273 terminal label +
  R3 §7 `R/build-record.json` variant tags without container schema (replaced by §4);
  R3 §10 tripwire "DELIVERED" claim (replaced by §5 full grep + HIGH adapter).
  Silence is not supersession. No new modules/schemas beyond R3 fixed 3+4 (build container is
  embedded `$defs`, §4). No `EXECUTED_BUILD` as old kind; no extra unregistered artifact.

If any §1–§5 definition proves unimplementable without weakening → precise NO-GO with `file:line`,
never a weakened checker. Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN.
Production semantic NO-GO on placeholder editions; synthetic approvals labelled.

## 1. `supported_epochs` strict serial schema + HIST predicate (closes addendum §1)

R3 §2 "union of walked ancestor epochs" + R2-I §2.2 `{receipt_epoch:GITSHA,staged_producer_head:GITSHA}`
are superseded as containers (conditional `staged_epoch` PRESENT/ABSENT logic itself is RETAINED).

### 1.1 Strict shape (one choice, no alternates)

In `versioned-renewal-source-proof-v2.schema.json` (one of fixed 4, R3 §1):

```json
"supported_epochs": {
  "type": "array", "minItems": 1, "maxItems": 256,
  "items": { "$ref": "#/$defs/supportedEpoch" },
  "uniqueItems": true
}
// $defs.supportedEpoch:
{
  "type": "object", "additionalProperties": false,
  "required": ["kind","name","epoch","sha256"],
  "properties": {
    "kind": {"enum": ["RECEIPT_EPOCH","STAGED_PRODUCER_HEAD","SCHEMA_EPOCH"]},
    "name": {"type": "string", "minLength": 1},
    "epoch": {"type": "string", "pattern": "^[0-9a-f]{40}$"},
    "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"}
  },
  "allOf": [
    {"if": {"properties": {"kind": {"const": "RECEIPT_EPOCH"}}},
     "then": {"properties": {"name": {"const": "receipt"}}}},
    {"if": {"properties": {"kind": {"const": "STAGED_PRODUCER_HEAD"}}},
     "then": {"properties": {"name": {"const": "staged"}}}},
    {"if": {"properties": {"kind": {"const": "SCHEMA_EPOCH"}}},
     "then": {"properties": {"name": {"enum": ["proposal","retention","staged","receipt","set","revalidation"]}}}}
  ]
}
```

- Ordering/dedup: file-bytes order MUST be sorted by `(kind,name)` lexicographically
  (`RECEIPT_EPOCH < SCHEMA_EPOCH < STAGED_PRODUCER_HEAD` by string compare; within `SCHEMA_EPOCH`
  by `name`); `(kind,name)` unique, no dups; same-SHA different-epoch or same-epoch different-SHA
  for same `(kind,name)` → `HISTORY_TOOL_EPOCH_DRIFT`. `$ref` is local `#/$defs/*` only (no remote).
- Cross-field: each entry's `sha256` is `git show <epoch>:<schema-or-closure-path>` SHA for that
  `(kind,name)` (receipt closure rows vs `receipt_epoch`, staged `code_deps`+`style_input_ref` vs
  staged head `:1039`, per-schema vs own epoch §4); where dependency rows overlap, epochs must agree
  else `HISTORY_TOOL_EPOCH_DRIFT`. `supported_epochs` is covered by `proof_sha256`
  (`core.sha256_object({all keys except proof_sha256})`, `sort_keys=True`
  `PC/scripts/survey_production_v2.py:163-166` so order is immaterial to hash but fixed for bytes).
- First renewal (editorial predecessor): exactly 8 entries (1 `RECEIPT_EPOCH/receipt` +
  1 `STAGED_PRODUCER_HEAD/staged` + 6 `SCHEMA_EPOCH/*`). Repeat renewal: sorted union of walked
  ancestor entries (see 1.2); length 8×generations (max 256 = 32×8, `CHAIN_LIMIT=32`
  `PC/scripts/survey_publication_set_v2.py:109,1023-1051`); exceeding → pre-write refuse (chain bound).
  No old R2 tuple conflicting union: R2-I `{receipt_epoch,staged_producer_head}` 2-GITSHA shape is
  DELETED as a container (values preserved as the 2 entries above).

### 1.2 Ancestor traversal + HIST comparison (bounded, no current hash-only)

- Walk: `_walk_chain_backwards:1023-1051` newest→oldest over `supersedes` links (cycle/depth
  `CHAIN_LIMIT=32`, `1060-1230` anchor/sequence/time; later legacy successor unsupported `:1189`).
  For each ancestor record, HIST reloads its receipt (`current_tools.repository_commit_sha` +
  `contract` + `closure`), staged head (`:1039` if `R3_EDITORIAL`, ABSENT if `VERSIONED_RENEWAL`
  per R3 §2 conditional), per-schema epochs (R3 §4). HIST-observed set = sorted union of those
  entries (same `(kind,name,epoch,sha256)` shape). Each entry verified via
  `git cat-file -e <epoch>^{commit}` + `git show <epoch>:<path>` SHA (+`byte_count` where sized);
  never live-path equality; never cross-substituted; missing (incl partialDB-26309) →
  `HISTORY_BLOB_MISSING`, never forged; unknown `kind`/`name` → `UNSUPPORTED_MIGRATION`.
- Comparison (exact equality, not subset/superset): `proof.supported_epochs` MUST equal
  HIST-observed set exactly (sorted-set equality via `(kind,name,epoch,sha256)` tuples, no dups).
  Subset (proof omits an ancestor) → `HISTORY_TOOL_EPOCH_DRIFT`; superset (proof invents an epoch) →
  `HISTORY_TOOL_EPOCH_DRIFT`; same `(kind,name)` different `(epoch,sha256)` → `HISTORY_TOOL_EPOCH_DRIFT`.
  Layer-B step 3 + §11 `resume_renewal_activation` `new_core` comparison consume this HIST verdict;
  they never re-implement Git reads. Old evidence absent from tool commit remains positive control
  (decision §3). Current-schema hash-only acceptance is FORBIDDEN as an ancestor check.

Source need: receipt `current_tools.repository_commit_sha` minted at prepare before publication
authorities exist + staged `producer_head` `:1039` + per-schema epochs are three commit domains
(decision §3); R3 conditional + repeat-chain rule already shaped; this §1 supplies the missing container.

## 2. U-after-C manuscript dispatch (closes addendum §2)

Current code knows only `editorial_source` present/absent
(`PC/scripts/survey_reader_publication_v2.py:editorial_source is None → canonical
survey_root/main.tex else verify_staged_source :237-247` via P3S); `renewal_source`/
`renewal_source_proof_ref`/`VERSIONED_RENEWAL` occur zero times in `survey_reader_publication_v2.py`,
`survey_editorial_staged_source_v2.py`, `survey_reader_surface_gate_v2.py`,
`survey_publication_set_v2.py` (verified `grep` in addendum). No existing dispatch to adopt; R3
defined the XOR/keyword model but not the U-after-C four-way split. This §2 is the dispatch.

### 2.1 Stored vs supplied proofs (no two-proof bypass)

- Stored source proof (HISTORICAL): a C-derived prior manuscript file on disk carries serialized
  `renewal_source:{path,sha256}=prior R/renewal-source-proof.json` (R3 §1 XOR: exactly one of
  `editorial_source`/`renewal_source` for renewed sets; legacy/editorial keep `editorial_source` only).
  This embedded ref is HIST data: HIST loads the PRIOR proof by persisted path, checks path+SHA,
  recomputes its self-digest, verifies its `supported_epochs` per §1 via record-epoch blobs
  (`HISTORICAL_IDENTITY_VERIFIED`, ancestor HIST-only, never current-replay), and binds it to the
  prior seal's proof ref (prior `R/publication-set.json` roles). It is NEVER current authority for the
  new operation.
- Supplied current U proof (CURRENT): explicit keyword `renewal_source_proof_ref=None`
  (`{path,sha256}`, reloaded) on `validate_manuscript_manifest`/`validate_review_record` (nested
  `:643-647` threads SAME ref) + Candidate/QA builders/validators + `renewal_receipt_ref` on Gate
  derivation (R3 §§1/9). For U it is REQUIRED (new proof at new `R/` paths, even though trio bytes
  equal prior `R/` bytes); for first-U (old editorial, no embedded `renewal_source`) it is the ONLY
  proof; for repeat-U-from-C it is the NEW proof, distinct path+SHA from the embedded PRIOR proof
  by construction (new `R/renewal-source-proof.json` id). Validators derive `renewal_source_proof_ref`
  from own NEW Candidate/bundle payload; outer expected ref must be identical when present (R3 §1).
- No arbitrary bypass: NEW proof MUST bind the exact reused manuscript/trio/build/current prior
  selection (decision §11.2 U list + exact prior-relative trio per R3 §3 + `REUSED_BUILD` chain per
  §4 + live State-selected predecessor per decision §7/§11.1). HIST MUST load the old stored renewal
  proof structurally (never current replay). Normal current direct validation without keyword on a
  renewed manuscript refuses (standalone old/current-P3S refusal, N-H1); C validation of its OWN proof
  uses its serialized `renewal_source` (own NEW proof, §2.2).

### 2.2 Four-way comparison (exact codes)

For U-after-C `validate_manuscript_manifest(repo,manuscript_path,*,issue_id,renewal_source_proof_ref)`:

1. Embedded-prior HIST: if payload has `renewal_source`, HIST verifies it historically
   (path+SHA == prior seal's proof ref; self-digest; §1 epochs; COPY mapping/inventory; old
   self-/cross-digests). Failure → `HISTORY_DIGEST_MISMATCH`/`HISTORY_BLOB_MISSING`/
   `HISTORY_ANCESTOR` (never `REUSE_TARGET_MISMATCH`). Absence on first-U editorial is expected
   (HIST checks `editorial_source` historically instead).
2. Context-new CURRENT: with reloaded NEW `renewal_source_proof_ref`, check ALL U current predicates
   (decision §11.2 list: schema/self-digest/issue, Profile, exact Architecture+typed approval,
   sizes, unique paths, coverage, reader requirements, author/time, fidelity, surface/suppression,
   exact trio) + exact prior-relative trio (`output_trio_refs` at PRIOR `R/` paths) + complete reader
   equality via `verify_renewal_rerender_equality` (disposable temp trio vs prior bytes). Mismatch →
   `REUSE_TARGET_MISMATCH` (refuse pre-write, exit 2, never auto-convert to C). Old `editorial_source`
   live-P3S entry is REPLACED by (1)+(2) only when keyword present; without keyword → stale refusal.
3. Seal-selected NEW: full-set SAME-proof equality for NEW Candidate/QA/Gate/receipt/seal (NEW proof
   path+SHA); equal-SHA different-path refused; embedded PRIOR path is NEVER a member of this equality
   (prior proof ≠ new proof by id). NEW vs seal-selected mismatch → `REVIEW_TARGET_MISMATCH`.
4. Stale-prior check: U pointing at non-active `P/` when active predecessor is prior `R/` →
   `REVIEW_TARGET_MISMATCH` (R3 §3), even if (1)–(3) would otherwise pass.

Review nesting: `validate_review_record:601-692` digest base 14 keys (`:617-636`) unchanged; nested
`validate_manuscript_manifest:643-647` receives the SAME reloaded NEW ref explicitly (never ambient);
historical same-reader scope reloaded with exact before/after relations, never fresh P2V `SCOPE_BOUND`.

### 2.3 Both U cases + oracles

- First-U (old editorial): manuscript has `editorial_source` only, no `renewal_source`. HIST checks
  old source-proof historically + live+retained-COPY E; CURRENT checks U list + trio vs NEW proof;
  seal-selected NEW equality holds. Positive oracle `P-U1/P-U2` (R3 §11) retained.
- Repeat-U-from-C: manuscript has `renewal_source`=PRIOR `R` proof. HIST checks PRIOR proof per (1);
  CURRENT checks NEW proof per (2); full-set checks NEW proof per (3). Positive oracle `C→U`
  (R3 §3 names the case; this §2 supplies the dispatch): C (proof P1 at `R1/`) then U (new proof P2 at
  `R2/` binding prior `R1/` trio bytes, P1 HIST-verified, P2 CURRENT-verified, NEW set bound to P2).
  Negatives: NEW P2 ≠ seal-selected P2 → `REVIEW_TARGET_MISMATCH` (N-H2/N-H11); P2 not binding exact
  prior trio/manuscript/build/selection → `REUSE_TARGET_MISMATCH` (N-H10); P1 HIST-invalid →
  `HISTORY_*` (N-H6/N-H8); U-after-C without keyword → stale P3S refusal (N-H1); replacement review at
  different path silently treated as reused → `REVIEW_TARGET_MISMATCH` (never silent).

## 3. Full content-contract list 71 (closes addendum §3; R3 §6.4 examples-only superseded)

R3 §6 arithmetic verified correct in addendum (per-route 63 = 35+22+3+1+1+1; union 66; `shared_py35`
= 30+2+3 new absent on disk expected; `schema22` = 14+4 new absent +4 family present; route3/staged/
style/recipe present; `$ref` local `#/$defs/*` only; 7/7 prompts present; `PIPELINE_N 67/QUALITY_N 3`
verified). Remaining gap was exhaustive 67-list with per-file pin rule. This §3 is that table
(no code needed; one table closes it). Unaffected R3 §§6.1–6.3/6.5 retained (closure sets, provenance,
import edges `screening:397`, `discovery:12`, `x_intake:360`; gates 30→35/14→22/50→63/22→29/27→34;
pipeline 67→71 schemas-only, no `.py`, control-roots unchanged).

Contract identity binds BOTH (Layer-B-2): `core.contract_identity:210-228` =
`aggregate_file_hash(pipeline_files + [DEFAULT_CONFIG,PROFILE_SCHEMA,STATE_SCHEMA])` + quality +
research/publication pins (`aggregate_file_hash` sorted `rel\0bytes\0`, `PC/...:168-178`).
`pipeline_files` = `cfg.contract_files.pipeline` (71 post-delta). Implicit 3 beyond 71:
`config/survey-production-v2.json` (`DEFAULT_CONFIG`), `schemas/survey-production-profile.schema.json`
(`PROFILE_SCHEMA`), `schemas/survey-production-state.schema.json` (`STATE_SCHEMA`)
(`PC/scripts/survey_production_v2.py:DEFAULT_CONFIG/PROFILE_SCHEMA/STATE_SCHEMA`). No silent prefix:
every validated file is either runtime `code_deps` (AST-verified imports, R3 §§6.1–6.3) or content
`contract` (this table, hash-bound via `contract_identity` + prompt/schema bytes). Machine `.json`
twin arrays match counts exactly (71 pipeline, 3 quality, 3 implicit, 35 py, 22 schema).

### 3.1 Post-delta pipeline 71 (67 + 4 new), sorted, per-file class

`closure-member` = in R3 §6.2 shared22 (hash-bound BOTH as closure row AND via `contract_identity`);
`contract-only` = hash-bound via `contract_identity` only (content contract). New 4 are `closure-member`
+ contract (67→71 schemas-only, R3 §6.5). Origin function = verifier that binds the file
(`closure` = `_route_code_deps`/`_editorial_closure_rows`/`current_closure` member-wise;
`contract` = `contract_identity` recompute in Layer-B-2).

| # | path | class | origin |
|---|---|---|---|
| 1 | `config/prompts/article-drafting-v2.md` | contract-only | contract (prompt SHA, A5/A6) |
| 2 | `config/prompts/evidence-verification-v2.md` | contract-only | contract (prompt SHA, E3–E5) |
| 3 | `config/prompts/grok/x-source-intake-base-v1.md` | contract-only | contract (X1) |
| 4 | `config/prompts/grok/x-source-intake-special-v1.md` | contract-only | contract (X1) |
| 5 | `config/prompts/grok/x-source-intake-weekly-v1.md` | contract-only | contract (X1) |
| 6 | `config/prompts/profile-synthesis-v2.md` | contract-only | contract (A5) |
| 7 | `config/prompts/source-screening-v2.md` | contract-only | contract (S9) |
| 8 | `config/publication-review-v2.json` | contract-only | contract (review config) |
| 9 | `config/survey-production-v2-requirements.txt` | contract-only | contract |
| 10 | `docs/survey-production-core-v2-agent-first-reaudit-2026-08-22.md` | contract-only | contract |
| 11 | `docs/survey-production-core-v2-authority.md` | contract-only | contract |
| 12 | `docs/survey-production-core-v2-contract-normalization-second-audit-amendment.md` | contract-only | contract |
| 13 | `docs/survey-production-core-v2-execution-record-policy.md` | contract-only | contract |
| 14 | `docs/survey-production-core-v2-github-actions-policy.md` | contract-only | contract |
| 15 | `docs/survey-production-core-v2-minimum-vertical-slice-second-audit-amendment.md` | contract-only | contract |
| 16 | `docs/survey-production-core-v2-operator-execution-bridge.md` | contract-only | contract |
| 17 | `docs/survey-production-core-v2-postintegration-amendment.md` | contract-only | contract |
| 18 | `docs/survey-production-core-v2-redesign-authority.md` | contract-only | contract |
| 19 | `docs/survey-production-core-v2-redesign-plan-after-w33-sp001.md` | contract-only | contract |
| 20 | `docs/survey-production-core-v2-whole-system-audit-2026-08-22.md` | contract-only | contract |
| 21 | `docs/survey-production-core-v2-whole-system-audit-remediation-closure.md` | contract-only | contract |
| 22 | `docs/survey-production-core-v2-workflow-responsibility-inventory.md` | contract-only | contract |
| 23 | `docs/survey-production-core-v2-x-source-intake.md` | contract-only | contract (X policy) |
| 24 | `schemas/architecture-approval-record-v2.schema.json` | contract-only | contract (A4) |
| 25 | `schemas/architecture-review-attention-v2.schema.json` | contract-only | contract (A3) |
| 26 | `schemas/architecture-review-summary-v2.schema.json` | contract-only | contract (A3) |
| 27 | `schemas/candidate-matrix-v2.schema.json` | contract-only | contract (A1) |
| 28 | `schemas/candidate-selection-v2.schema.json` | contract-only | contract (A2) |
| 29 | `schemas/discovery-acceptance-v2.schema.json` | closure-member | closure + contract (D1) |
| 30 | `schemas/draft-v2-package.schema.json` | contract-only | contract (A6) |
| 31 | `schemas/draft-v2-result.schema.json` | contract-only | contract (A6) |
| 32 | `schemas/edition-evidence-view.schema.json` | contract-only | contract (E6) |
| 33 | `schemas/editorial-manuscript-spec-v2.schema.json` | closure-member | closure + contract |
| 34 | `schemas/editorial-publication-build-record-v2.schema.json` | closure-member | closure + contract (old build, §4) |
| 35 | `schemas/editorial-publication-set-v2.schema.json` | closure-member | closure + contract |
| 36 | `schemas/editorial-publication-source-manifest-v2.schema.json` | closure-member | closure + contract |
| 37 | `schemas/editorial-toolchain-spec-v2.schema.json` | closure-member | closure + contract (§7) |
| 38 | `schemas/evidence-authority-supplement-v2.schema.json` | contract-only | contract (E7) |
| 39 | `schemas/evidence-v2-card.schema.json` | contract-only | contract (E4) |
| 40 | `schemas/evidence-v2-run-package.schema.json` | contract-only | contract (E3/E5) |
| 41 | `schemas/evidence-v2-task.schema.json` | contract-only | contract (E2) |
| 42 | `schemas/freeze-record-v2.schema.json` | contract-only | contract (Freeze) |
| 43 | `schemas/human-gate-review-index-v2.schema.json` | contract-only | contract |
| 44 | `schemas/human-gate-review-record-v2.schema.json` | contract-only | contract |
| 45 | `schemas/issue-architecture-v2.schema.json` | contract-only | contract (A3) |
| 46 | `schemas/materiality-ledger.schema.json` | contract-only | contract (E8 ledger) |
| 47 | `schemas/merge-verification-v2.schema.json` | contract-only | contract |
| 48 | `schemas/operator-execution-request-v2.schema.json` | contract-only | contract |
| 49 | `schemas/operator-pending-gate-invalidation-v2.schema.json` | contract-only | contract |
| 50 | `schemas/profile-completeness-result.schema.json` | contract-only | contract (E9) |
| 51 | `schemas/profile-synthesis-v2-input.schema.json` | contract-only | contract (A5) |
| 52 | `schemas/profile-synthesis-v2-result.schema.json` | contract-only | contract (A5) |
| 53 | `schemas/publication-candidate-v2.schema.json` | closure-member | closure + contract (amended §1) |
| 54 | `schemas/publication-preview-approval-v2.schema.json` | contract-only | contract |
| 55 | `schemas/publication-review-record-v2.schema.json` | contract-only | contract (review, §2) |
| 56 | `schemas/quality-regression-bundle-v2.schema.json` | closure-member | closure + contract (amended §1) |
| 57 | `schemas/reader-manuscript-v2.schema.json` | closure-member | closure + contract (amended §1) |
| 58 | `schemas/release-manifest-v2.schema.json` | contract-only | contract |
| 59 | `schemas/release-record-v2.schema.json` | contract-only | contract |
| 60 | `schemas/repair-set-v2.schema.json` | contract-only | contract |
| 61 | `schemas/review-finding-v2.schema.json` | contract-only | contract |
| 62 | `schemas/screening-v2-batch-result.schema.json` | closure-member | closure + contract (S8) |
| 63 | `schemas/screening-v2-run-package.schema.json` | closure-member | closure + contract (S9/S10) |
| 64 | `schemas/stage-checkpoint-v2.schema.json` | contract-only | contract (stage) |
| 65 | `schemas/survey-discovery-record.schema.json` | closure-member | closure + contract (S1) |
| 66 | `schemas/visual-review-record-v2.schema.json` | contract-only | contract (review, §2) |
| 67 | `schemas/x-source-intake-v2.schema.json` | contract-only | contract (X1; closure-excluded by design — validated via `validate_manifest_statefree`, not P3S closure; bound here so "no hidden file" holds) |
| 68 | `schemas/versioned-renewal-basis-v2.schema.json` | closure-member (NEW) | closure + contract (R3 §1) |
| 69 | `schemas/versioned-renewal-source-manifest-v2.schema.json` | closure-member (NEW) | closure + contract (hosts §4 `$defs`, R3 §1) |
| 70 | `schemas/versioned-renewal-source-proof-v2.schema.json` | closure-member (NEW) | closure + contract (hosts §1 `supportedEpoch`, R3 §1) |
| 71 | `schemas/versioned-renewal-publication-set-v2.schema.json` | closure-member (NEW) | closure + contract (R3 §1) |

Implicit beyond 71 (in `contract_identity` via `DEFAULT_CONFIG/PROFILE_SCHEMA/STATE_SCHEMA`,
`PC/scripts/survey_production_v2.py:contract_identity:210-228`): `config/survey-production-v2.json`
(contract-only, registry itself), `schemas/survey-production-profile.schema.json` (contract-only),
`schemas/survey-production-state.schema.json` (contract-only). Quality 3 (contract-only):
`docs/survey-production-core-v2-historical-invariants.md`,
`docs/survey-production-core-v2-historical-production-deep-audit.md`,
`docs/survey-production-core-v2-issue-prevention-checklist.md`
(`cfg.contract_files.quality`, verified). All 7 R3 §6.4 prompts are rows 1–7 above (bound exact);
`x-source-intake` docs/prompts/schema are rows 23/3–5/67 (bound exact, no hidden X file).
Snapshot/closure actual unique lists with origin functions are R3 §§6.1–6.3 (63/66, provenance,
`file:line` edges) + R3 §10 snapshot function (existing 9 + basis/proof/COPY/trio/closure rows +
Candidate/Gate refs, externals ARE members, exact-file inventories) — RETAINED, now backed by this
71-table so "no validated file hidden outside either set" is checkable: every file validated by shared
cores is either `closure-member` above or explicitly `contract-only` with its validator row cited.

## 4. Build-unit kinds + new container (closes addendum §4; R3 §§3/7 corrected, 4-file limit kept)

Source ground truth (verified in this unit): old build-record schema kind const is
`EDITORIAL_PUBLICATION_BUILD_V1` (`PC/schemas/editorial-publication-build-record-v2.schema.json:24`),
`required` 13 (`schema_version/kind/issue_id/proposal_ref/staged_manifest_ref/recipe_ref/
declared_inputs/recipe/toolchain/outputs/exit_code/recorded_at/build_sha256`), `toolchain` requires
`{executable,versions,argv,env}` with `versions` type object (no `additionalProperties` detail).
Old terminal R3 build is therefore `EDITORIAL_PUBLICATION_BUILD_V1`, NOT `EXECUTED_BUILD`.
R3 §3 terminal label + R3 §7 variant tags without container schema are superseded (R3 §7
`versions`/`argv`/`env` exactness per `:60-74,:1183-1244,:1336-1362,:1400,:1540` is RETAINED).

### 4.1 Terminal correction + HIST walk

HIST walk: `REUSED_BUILD.original_record_ref` → immediate prior record → if prior is itself
`REUSED_BUILD`, follow its `original_record_ref` HISTORICALLY to the terminal kind
`EDITORIAL_PUBLICATION_BUILD_V1` (old R3 `P/publication/build-record.json`, SHA+epoch from prior
receipt chain per §1) or to a prior `R/EXECUTED_BUILD` (prior `R/build-record.json` with §4.2
`EXECUTED_BUILD` branch, itself HIST-verified). Iteration bound 32 steps (same `CHAIN_LIMIT`);
exceeding → pre-write refuse. Consistency per step (bounded, same issue/Profile/recipe-spec,
`recipe.fixed_steps` exact `FIXED_RECIPE_STEPS`/`EXPECTED_ARGV_*`, toolchain executable family per §7;
style bytes MAY differ for C, recipe `.latexmkrc` MUST equal markers/steps): break →
`HISTORY_ANCESTOR` (chain break) or `REVIEW_TARGET_MISMATCH` (prior-relative bind break), never
synthesized. U performs NO execution (`toolchain_spec_path=None`, CLI omits `--toolchain-spec`,
no disposable root, no `EXECUTED_BUILD` keys).

### 4.2 New container (embedded `$defs`, fixed 4 files preserved)

No 5th new schema. Host is `versioned-renewal-source-manifest-v2.schema.json` (one of fixed 4)
new `$defs.buildRecord` (local `#/$defs/*` only):

- `R/build-record.json` validated against `#/$defs/buildRecord` (host `$defs`, not old schema);
  old records validated against OLD schema SHA at record epoch (R3 §1 old/new pins).
  `additionalProperties:false` both variants; `build_sha256=core.sha256_object({all except self})`
  INCL input/output refs (map-resolution excluding outputs rejected).
- Common REQUIRED: `schema_version:const 2.0-rc1, kind:const VERSIONED_RENEWAL_BUILD_V1,
  issue_id:S, proposal_ref:{path,sha256}=P/proposal.json, renewal_basis_ref:{path,sha256},
  renewal_proof_ref:{path,sha256}, recipe_ref:{path,sha256}=.latexmkrc, recorded_at:INST,
  build_sha256:SHA`. `staged_manifest_ref` ABSENT by construction (proof IS staged proof, §7);
  `renewal_basis_ref`/`renewal_proof_ref` PRESENT (bind COPY + epochs, not effective7 alone).
- `REUSED_BUILD` (U-ONLY, basis `requested==REUSE_TARGETS` + absent toolchain, no spawn):
  `variant:const REUSED_BUILD, original_record_ref:{path,sha256}` (immediate prior build record),
  `original_pdf_ref:{path,sha256,byte_count,page_count}`, `original_log_ref:{path,sha256,byte_count}`,
  `original_digest_ref:{path,sha256,byte_count}`, `renewal_tools:{old:GITSHA,new:GITSHA}`,
  `no_rebuild:const true`; FORBIDS `declared_inputs/recipe/toolchain/outputs/exit_code`.
- `EXECUTED_BUILD` (C-ONLY, basis `requested==RENDER_TARGETS` + explicit spec, disposable root +
  exclusive transfer + readback): `variant:const EXECUTED_BUILD`,
  `declared_inputs:{primary,bibliography,style}:{path,sha256}` (new `R/` trio),
  `recipe:{fixed_steps:S[1..]}` (exact `FIXED_RECIPE_STEPS` per recipe),
  `toolchain:{executable:S,versions:<R3 §7 exact: required stdout/stderr/returncode/link_path/real_path/
  real_sha256 + per-companion *_stdout/_returncode/_link_path/_real_path/_real_sha256/_error,
  truncation 8000/4000/500/300, argv==expected tuple, env allowlisted sorted>}`,
  `outputs:{publication-pdf,build-log,pdf-digest}:{path,sha256,byte_count}` under `R/build/`,
  `exit_code:const 0`; FORBIDS `original_*`/`renewal_tools`/`no_rebuild`.
- Receipt binds build-record (AFTER, decision §11.1); seal roles for `build-log`/`pdf-digest` point at
  `R/build-record.json:outputs` paths (prior-relative for `REUSED_BUILD`, `R/build/` for `EXECUTED_BUILD`).

Kind namespace: old `EDITORIAL_PUBLICATION_BUILD_V1` vs new `VERSIONED_RENEWAL_BUILD_V1` are disjoint
by `kind` const (no routing collision; canonical-writer allowlist branches on kind, pre-code confirms).

## 5. Stage-bootstrap tripwire + HIGH adapter (closes addendum §5; R3 §10 "DELIVERED" superseded)

R3 §10 tripwire list (7 hits) was incomplete; this §5 publishes the FULL command + disposition
(no wave-away). Command (read-only, no repo-code execution):

```text
grep -rn "contract_identity\|expected_contract\|current_contract\|contract.*!=\|contract.*==\|implementation.*repository_commit\|verify_state_basis\|validate_agent_state\|resolve_checkpoint_artifact\|current_stage_basis_override" scripts/*.py
```

Representative FULL hit disposition (all hits triaged; `PC` = proof-copy; renewal-admission vs
R1/canonical vs current-vs-current safe vs HIGH-avoided):

- `survey_agent_control_v2.py:230` (`profile.contract != state.contract` in `_profile_and_source:208-236):
  live-State vs live-Profile binding (both live, same generation). HIGH RETAINS via live-live check
  only (see adapter below); never old-State vs new-disk. Disposition: SAFE (live-live), renewal HIGH
  calls it on LIVE State/Profile only.
- `:325-329` (`report.contract != contract` where `contract = expected_contract or
  contract_identity(current disk)` in `_validate_core_stage_report:266-343`): current-vs-current when
  caller passes current contract; HISTORICAL when caller passes `record.contract`
  (`:479` historical `record.contract` + `record.implementation.repository_commit_sha`).
  Disposition: DUAL — SAFE for live reports (current-current), HISTORICAL for old reports (record-owned
  core fields, no live compare, see adapter). Renewal HIGH never passes an arbitrary `expected_contract`.
- `:333` (`report.implementation_commit_sha != implementation`): same DUAL as above.
- `:473-481` (historical State checkpoint validation with `record.contract`/`record.implementation`):
  HISTORICAL (old report `contract` vs old record, no live disk). Disposition: HISTORICAL, Layer-B MUST
  run for current (see below), old reports validated history-only.
- `:1601-1610` (`current_contract = contract_identity(...)` + `_validate_core_stage_report(...,
  expected_contract=current_contract, expected_implementation_sha=current impl)` for new checkpoint):
  current-vs-current SAFE (new report minted under current disk). Renewal Layer-B-2 same discipline.
- `:1652-1668` (`record.contract != current_contract` + same `_validate_core_stage_report` with current):
  current-vs-current SAFE (live checkpoint must be under current tools; renewal re-mints under new epoch).
- `:2409` (`contract: contract_identity(...)` for new pending basis): current SAFE (new authority).
- `survey_production_v2.py:978` (`profile.contract != state.contract`), `:980-981`
  (`expected_contract(current disk) != state.contract` in `verify_state_basis:959-996`): strict-State
  gate (old-State vs new-disk bricks by design). Disposition: HIGH-AVOIDED on renewal paths —
  renewal HIGH NEVER calls `verify_state_basis`/`validate_agent_state` on the old/before State under new
  tools (see adapter). Old-State provenance is HIST (record epochs), not a live gate.
- `survey_editorial_publication_v2.py:1121-1125` (`tools.contract != current_contract` receipt vs current):
  current-vs-current SAFE (receipt epoch consistency, Layer-B-2 equivalent). `:1807` (current recompute
  for new receipt `current_tools`): current SAFE. `:3403` (`contract_now = contract_identity(...)`
  for new activation `core.contract`): current SAFE (new record `core` under new epoch).
  `:3283` comment (State contract == cfg-derived via strict State): HIGH-AVOIDED for renewal before-State
  (strict State not run on retained before-State; detached `validate_renewal_basis` validates retained
  bytes only).
- `survey_editorial_staged_source_v2.py:291-298,1053,1836-1842` (`_check_contract_identity` 8 keys +
  staged vs proposal equality): content-contract shape + same-generation equality SAFE; renewal carries
  it via HIST (old shapes) + Layer-B (new shapes), never cross-generation.
- `survey_weekly_derivation_v2.py:748-749` / `longform_generated_v2.py:695-696`
  (`tools.contract != current_contract` current receipt replay): current-vs-current SAFE (receipt epoch
  consistency). `survey_weekly_mechanical_refresh_v2.py:1120-1121` (old receipt vs current): R1/canonical
  path kept under pre-write refusal in versioned mode (decision §8), NOT renewal admission.
  `survey_editorial_correction_proposal_v2.py:1713` (receipt vs current): P1 path, same (not renewal).
  `survey_stage_validation_v2.py:749-760` (`current_contract` minted in new `CORE_STAGE_CONTRACT` report):
  current SAFE (new report). `survey_release_checkpoint_v2.py:53,80`,
  `survey_handoff_v2.py:127`, `survey_orchestrator_v2.py:446`: report/path bindings, current SAFE or
  N/A (handoff `required:false` basis-preemption is not stage coverage, preserved).
- `current_stage_basis_override`, `resolve_checkpoint_artifact`, `resolve_active_screening_acceptance`,
  `_canonical_root_acceptance` State branch (`screening:325-350,442-489`), `observe_current_authority`:
  HIGH-AVOIDED in Layer-A/B (R3 §9 bans + `ast` obligation); renewal leaf uses basis-pinned
  `_load_basis_accepted_ref` + session, never checkpoint resolution.

Typed HIGH adapter (no arbitrary `expected_contract` arg, no public skip; State/Profile init contract
kept OLD):

- `_observe_renewal_entry(root,state_path)` (HIGH private, before capture, no basis): reloads LIVE
  canonical State + `_profile_and_source:208-236` live-live binding (profile bytes == `state.profile.sha`,
  `validate_profile` shape, issue/Profile identity, `profile.contract == state.contract` live-live `:230`
  — SAFE, both live same generation) + current nonpublication authority + current tool predicates
  (current `contract_identity` recomputed for INFO/pins only, never equality vs old State stored contract)
  + prior history via HIST (`verify_versioned_history`, record epochs). In-memory pins only; no
  `verify_state_basis`/`validate_agent_state` on any old/before State; no `expected_contract` param.
- `observe_renewal_authority(root,state_path,basis_path)` (HIGH basis-bound, after basis/before
  finalize/immediately before activate): reopens ALL inputs; demands LIVE State == fresh `before_state_ref`
  (live-live) + retained COPY == basis binding + selected predecessor == State-selected seal (prior-relative,
  §2) + `basis.current_tool_epoch` == CURRENT disk closure/contract recompute (current-current, Layer-B-2
  discipline). No `expected_contract` caller arg; no old-State-vs-new-contract compare.
- `validate_renewal_basis(root,basis_path)` (SOURCE detached, every proof readback): validates RETAINED
  before-State only (retained bytes + COPY mapping/inventory + unchanged evidence), never live-before
  equality (decision §11.1). `verify_renewal_source_proof` Layer-B MUST run on every readback incl after
  activation (CURRENT closure/contract/schemas vs proof + HIST verdict per §1); old `CORE_STAGE_REPORT`
  own-record `core` fields (`contract`/`implementation_commit_sha`) for HISTORICAL reports are validated
  history-only (record-owned, `:479` discipline, no live compare); LIVE reports use exact new current
  (`:1601-1610` discipline). Normal stage accepts bootstrap legitimately because: (a) old receipt closure/
  contract verified HISTORICALLY against old blobs (§1), (b) new closure/contract verified CURRENTLY via
  Layer-B-2 against live disk with pipeline delta SOLELY from §3 new-4 entries, (c) live State/Profile
  binding preserved (`_profile_and_source` live-live), (d) no renewal path calls the bricking equality
  (`verify_state_basis:980-981` on old State under new tools is never invoked). If any renewal HIGH path
  requires such an equality → precise NO-GO with `file:line` (not claimed closed beyond this adapter;
  implementation must preserve the call list above).

No Profile rebind occurs (Profile path/bytes identical; only tooling contract advances, separated as
`old_tool_epochs` vs `current_tool_epoch` in basis). New config registry (67→71) changes `contract`;
State/Profile initialization contract is kept OLD as history (pinned in `old_tool_epochs` +
`profile_ref`, never rewritten).

## 6. R4 completeness + remaining work (honest)

- [x] §1: `supported_epochs` strict fragment + HIST equality predicate + 256 bound + drift/missing split.
- [x] §2: U-after-C dispatch (stored HIST vs supplied CURRENT vs seal-selected NEW vs stale-prior) +
  both first-U/repeat-U semantics + `C→U` two-proof oracle + refusal codes.
- [x] §3: full 71-table (closure-member vs contract-only per file) + 3 quality + 3 implicit + X/prompts
  bound exact; machine `.json` arrays match counts.
- [x] §4: terminal `EDITORIAL_PUBLICATION_BUILD_V1` + embedded `$defs.buildRecord` in
  `versioned-renewal-source-manifest-v2` (fixed 4 kept) + digest base + old/new pins + 32-step HIST walk.
- [x] §5: tripwire `grep` command + full disposition + HIGH predicate call/DON'T-call list + Layer-B MUST
  + historical-vs-live report rule; no arbitrary `expected_contract`; no public skip.

**R4 closes the 5 addendum gaps as MAP.** Remaining work is IMPLEMENTATION (code/tests/build/fixtures
per R3 §§6–11 + R4 §§1–5 + meaningful regressions for affected original routes/R1/DM004 with
source/run/skip/failure/quota bookkeeping; `ast` non-reachability proof as implementation obligation,
not pre-code evidence) + Astra confirmation of R3+R4 jointly. **Implementation stays BLOCKED until
Astra confirms.** Any unpreservable predicate in implementation → contract revision or precise NO-GO
(`file:line`), never a weakened checker. Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN.
Stop at internal return; no code, no ordinary Commit/Push (Human-owned).

(End — R4 supersedes listed R3/R2 occurrences only; R3 preserved; all other R3 maps referenced, not
duplicated; no independence claim; no runtime evidence.)
