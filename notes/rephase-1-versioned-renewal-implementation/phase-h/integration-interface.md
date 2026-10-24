# Phase-H history integration interface — for S/high workers (descriptive, not permit)

2026-10-24. H owns `scripts/survey_versioned_renewal_history_v2.py` in
`.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work/`
(actual409 + intended57 + H fix, no candidate/reconstruct commits).
S (`survey_versioned_renewal_source_v2.py`) and high (`survey_versioned_renewal_v2.py`)
must reread with same history loader; never accept a dict permit.

## Public H API (fixed names/signatures)

- `verify_versioned_history(root, record_path) -> dict`
- `verify_renewal_retention(root, basis_path) -> dict`
- `_derive_editorial_observed_bindings(root, record, ref, graph) -> (bindings, lineage)` (internal, tested via public leaf)
- `_check_observed_binding_row(root, row, history_graph, label) -> normed row`
- `_expected_receipt_closure(route, OLD|NEW)`, `_expected_staged_code_deps(route)`
- `_derive_history_graph_for_editorial(root, record) -> {receipt_epoch, staged_head}`

No State/P1/P2R/P3S/full-proof/Reader/Gate/Candidate calls. No old code exec. No caller
verified dict / caller epoch authority. FD-bound safe reads, strict JSON (no duplicate keys),
checked close, limits. All errors are `RenewalHistoryError(code, detail)` with
`HISTORY_*` / `UNSUPPORTED_MIGRATION` codes (never swallowed; fail-closed).

## `verify_versioned_history` return (descriptive, not consumable permit)

```python
{
  "HISTORICAL_IDENTITY_VERIFIED": True,
  "observed_refs": [
    {"kind": "LEGACY", "record_sha": "64hex"},
    {"kind": "EDITORIAL", "record_sha": "64hex", "seal_path": "P/.../publication-set.json"},
    {"kind": "VERSIONED", "record_sha": "64hex", "seal_path": "R/.../publication-set.json"},
    # ... chronological, supersedes walk, CHAIN_LIMIT 32, strictly increasing sequence,
    # nondecreasing instants, no cycles, later-legacy unsupported, issue/anchor bound.
  ],
  "observed_source_bindings": [
    # Canonical sorted dedup by full (path, binding, schema_path, schema_pointer, epoch).
    # Same path different generations allowed iff distinct owners/epochs.
    # Conflicting sha for same (path,binding,schema,epoch) -> HISTORY_DIGEST_MISMATCH.
    # NONEMPTY whenever chain has EDITORIAL or VERSIONED (legacy-only chains have none by design).
    # Format exact root precode R5, Astra §6 erratum (pointer "" allows root, never "/"):
    {"source_ref": {"path": "...", "sha256": "64hex"}, "binding": "RECEIPT_CURRENT_TOOLS", "repository_commit_sha": "40hex"},
    {"source_ref": {"path": "...", "sha256": "64hex"}, "binding": "STAGED_PRODUCER", "repository_commit_sha": "40hex"},
    {"source_ref": {"path": "...", "sha256": "64hex"}, "binding": "SCHEMA",
     "repository_commit_sha": "40hex",
     "schema_path": "schemas/....schema.json", "schema_pointer": "", "schema_sha256": "64hex"},
    # ... sorted by (path, binding, schema_path, schema_pointer, epoch), byte-order == sorted order
    # (array-order hashing; sort_keys=True sorts object keys only, NOT array order).
  ],
  "materialization_lineage": [
    # Descriptive refs for S C->U->U + original producer binding. S must reread each
    # via same history loader (read_repo_bytes / _require_authority_live / _require_sized_live),
    # never trust as permit. Stored producer may be older reachable ancestor, not immediate
    # prior seal proof equality.
    {
      "record_path": "sources/.../publication-surface-revalidation-rN.json",
      "record_sha": "64hex",
      "kind": "EDITORIAL",
      "original_proposal_ref": {"path": ".../proposal.json", "sha256": "64hex"},
      "original_staged_ref": {"path": ".../staged-source/staged-source-manifest.json", "sha256": "64hex"},
      "original_scope_ref": {"path": ".../scope-review-v2.json", "sha256": "64hex"},
      "original_retention_ref": {"path": ".../retained/retention-manifest.json", "sha256": "64hex"},
      "original_receipt_ref": {"path": ".../publication/validated-source-manifest.json", "sha256": "64hex"},
      "original_seal_ref": {"path": ".../publication/publication-set.json", "sha256": "64hex"},
      "original_build_record_ref": {"path": ".../publication/build-record.json", "sha256": "64hex"},
      "staged_producer_head": "40hex",  # == actual staged.producer_head
      "receipt_epoch": "40hex",          # == actual receipt.current_tools.repository_commit_sha
    },
    {
      "record_path": "sources/.../publication-surface-revalidation-rM.json",
      "record_sha": "64hex",
      "kind": "VERSIONED",
      "prior_selected_ref": {"path": "...", "sha256": "64hex"},
      "renewal_basis_ref": {"path": "R/.../renewal-basis.json", "sha256": "64hex"},
      "renewal_proof_ref": {"path": "R/.../renewal-source-proof.json", "sha256": "64hex"},
      "basis_current_epoch": "40hex",  # == actual basis.current_tool_epoch.repository_commit_sha
    },
    # ... one per chronological record (LEGACY entries have only record_path/sha/kind).
  ],
  "chain_length": int,  # len(chronological), max 32
  "anchor_kind": "VALIDATION_CHECKPOINT" | "LEGACY_REVALIDATION",
}
```

## Editorial derivation (first-renewal predecessor, real R3)

For each EDITORIAL ancestor, H derives from ACTUAL strict docs (never serialized observed/caller epochs):

- Tool rows (at DERIVED own commit, verified against actual doc fields + `git show`):
  - `RECEIPT_CURRENT_TOOLS`: `source_ref` = seal `source-receipt` role `{path,sha256}` (live/COPY, sized),
    `epoch` = actual `receipt.current_tools.repository_commit_sha` (== graph `receipt_epoch`).
  - `STAGED_PRODUCER`: `source_ref` = seal `staged_manifest_ref` (live), `epoch` = actual `staged.producer_head`
    (== graph `staged_head`).
- SCHEMA rows (E live/COPY, schema blob+mode at DERIVED epoch via `git show <epoch>:<schema_path>`):
  - O1 `proposal`: seal `proposal_ref`, epoch `staged_head`, schema `editorial-correction-proposal-v2`, `""`.
  - O2 `retention`: staged `retention_manifest_ref`, epoch `staged_head`, schema `editorial-retention-manifest-v2`, `""`.
  - O3 `staged`: seal `staged_manifest_ref`, epoch `staged_head` (own), schema `editorial-staged-source-manifest-v2`, `""`.
  - O4 `receipt-editorial`: seal `source-receipt` `{path,sha256}`, epoch `receipt_epoch` (own), schema
    `editorial-publication-source-manifest-v2`, `""`.
  - O5 `seal-editorial`: record `set_ref`, epoch `receipt_epoch`, schema `editorial-publication-set-v2`, `""`.
  - O6 `build-old`: seal `build_record_ref`, epoch `receipt_epoch`, schema `editorial-publication-build-record-v2`, `""`.
  - O17 `scope`: staged `scope_review_ref` (== receipt `scope_review_ref` exact path+SHA, enforced),
    epoch `staged_head`, schema `reader-surface-semantic-review-v2`, pointer `""` (whole-document root,
    never `"/"` per Astra §3; `/properties/editorial_correction_scope` is inventory only, never approval).
  - O8 specs (optional, iff present live at conventional `P/manuscript-spec.json`, `P/toolchain-spec.json`):
    epoch `receipt_epoch`, schemas `editorial-manuscript-spec-v2` / `editorial-toolchain-spec-v2`, `""`.
    Real R3 has both; synthetic unit fixtures may not (still NONEMPTY via required 9 rows).
- Required coverage enforced: O17 `""` + at least one RECEIPT + at least one STAGED, else
  `HISTORY_DIGEST_MISMATCH` (no subset/empty shortcut). Extra/omit/dup/reorder hit
  `HISTORY_DIGEST_MISMATCH` (conflicting sha, extra key, missing key, order != sorted) or
  `HISTORY_TOOL_EPOCH_DRIFT` (epoch != derived owner, schema blob drift at epoch).
- All original scope checks preserved: exact 15 seal names, required proposal/staged/retention/scope,
  staged `code_deps` exact 50 sorted + blob/mode/byte_count at `staged_head`, receipt closure exact 50 OLD
  + blob/mode at `receipt_epoch`, retained COPY (not live before-State), `before_active_digest` recompute
  chain-wide, E never required at tool commit (style trio explicitly NOT checked at epoch), no swallowed
  errors, pass order preserved. `len15` exact (not `len==15` + missing/extra lists), closure membership
  exact (name==path, set equality, order sorted), scope/proposal required (not skipped).

## Renewal derivation (supersedes walk + basis CURRENT epoch)

For renewal history (VERSIONED ancestors), expected = typed `supersedes` walk ancestor rows
(editorial rows above, via prior seal receipt/staged epochs) + basis CURRENT epoch own current rows
(renewal-owned: `receipt-renewal`, `seal-renewal`, `build-new` (`/$defs/buildRecord`), `basis`, `proof`,
`manuscript-renewal` (`/properties/renewal_source`), `candidate-renewal`, `bundle-renewal`,
`gate-renewal`, `record-renewal` (`/oneOf/2`), R specs; epoch = basis `current_tool_epoch.commit`).
Every prior proof historical-only (never current replay, no low→full current source-proof recursion).
Current code: narrow renewal-graph collection (submitted basis observed already verified exact via
epoch/owner/supported==observed/order) + lineage refs; full expected==submitted completeness
(no subset) pending high lifecycle. This unit is explicitly narrow unit, not end-to-end whole proof.

## For S (source) workers

- New basis must capture H `observed_source_bindings` (history derived, NONEMPTY) verbatim, sorted.
- `proof.supported_source_bindings` must exact-match `basis.observed_source_bindings` (sorted-set + byte-order),
  AND current fresh H rederived expected (via `verify_versioned_history(prior_record)` at readback).
  No subset/empty shortcut: `HISTORY_TOOL_EPOCH_DRIFT` on mismatch.
- Do NOT lookup submitted rows to infer expected owner epoch: compute from actual
  `receipt.current_tools.commit`, `staged.producer_head`, typed owner registry + supersedes walk +
  basis CURRENT epoch. Every prior proof historical-only.
- Materialization lineage: original proposal/staged/scope producer (editorial `P/...` or prior-`R/...`
  via prior seal roles, never forged old-format P3S manifest at renewal path) + stored manuscript
  producer proof/build (manuscript-embedded `renewal_source` reachable via `supersedes` + seal roles +
  `retained/before` COPY + receipt/proof refs, same issue/Profile, no cycles; may be older reachable
  ancestor for C→U→U, not forced immediate prior seal proof equality). Exposed via
  `materialization_lineage` above; S must reread each ref with same history loader.
- Known incompatibility (S worker must fix, H does NOT work around): current S
  `_validate_scope_o17` refuses ANY `schema_path == reader-surface-semantic-review-v2` row in
  `basis.observed` as "caller scope-schema". Correct history-derived O17 `""` rows (from H above)
  must be accepted when they equal H rederived expected (exact path/sha/epoch/schema_sha at
  `staged_head`), not refused as caller rows. S must distinguish derived-vs-caller via H rederived
  comparison, not blanket refuse. Do NOT edit S here; return precise `file:line` before broadening.

## For high workers

- `_observe_renewal_entry` / `observe_renewal_authority` live-before + HIST + current-tool predicates
  per Astra §§2/11.1 (never `production.verify_state_basis` on before/retained, never `validate_agent_state`
  in history/source paths). Detached readback never calls `observe_renewal_authority`; HIGH never runs
  `supported==observed` (Layer-B only in `verify_renewal_source_proof` step 4, every readback incl after
  activation, `HISTORY_TOOL_EPOCH_DRIFT` on mismatch).
- U `REUSED_TARGETS` vs C `NEW_TARGETS` per R5 §2 (stored HIST lineage-reachable vs immediate-bind NEW,
  `REUSED_BUILD` chain to terminal `EDITORIAL_PUBLICATION_BUILD_V1`, foreign lineage `REVIEW_TARGET_MISMATCH`
  even at equal SHA). C manuscript `renewal_source`, U keyword-only context, full-set SAME-proof equality.

## O17 pointer erratum (binding)

`observedSourceBinding.schema_pointer` allows `""` (remove old `minLength:1`). Whole-document uses `""`
only. Do NOT substitute `"/"` (empty-name property, not document root). `/properties/...` is inventory,
never approval. Registry still enforces exact pointer equality.
