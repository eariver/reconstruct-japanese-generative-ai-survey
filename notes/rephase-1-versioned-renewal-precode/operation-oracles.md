# Versioned renewal pre-code — operation oracles (author-side)

2026-10-23 JST. Author-side General pre-code return. Human HEAD `ce0de1a`
(root observed clean `main...origin/main`).
Governing: `outputs/rephase-1-versioned-renewal-contract-decision.md` (192 lines,
SHA256 `478f00510791b76af24aa7d61f398f0608f7ad8ae7808008c660f2bea6fbfdcf`)
INCLUDING §11; mandatory `notes/rephase-1-versioned-renewal-contract/astra-review-resolution.md`;
BOTH independent reviews WITH final-binding addenda.
Read-only source: `.rephase-1-editorial-runtime/final-source-packaging/proof-copy/candidate-partial-b40de60`
(actual409/tree8ce + intended57). No source edits/imports/tests/build/fixture/restore/network/Git writes.
This directory/file is the ONLY write in this unit alongside sibling
`interfaces-schemas-digests.md` (which owns schemas/digests/entries/call-map/inventory/threading;
this file owns resume equality, exit/disposition, fault + public positive/negative oracles,
fixture/source epoch discipline). Accepted detailed predicates are owned by sibling
`accepted-authority-readiness.md` (referenced, not duplicated). Old-format supported
fingerprints / successor closures are owned by a third agent (referenced, not invented).
Historical accepted State evolution obeys §11.3, not old predicate-map F3/F4 wording (see
`interfaces-schemas-digests.md` §0 + `accepted-authority-readiness.md` §0). No implementation yet.

## 0. Execution model and stop rules

- Single-writer/held-descriptor bounded guarantees only (decision §7 table bounds): no global CAS,
  no crash atomicity, no automatic stale adoption, no retrospective PASS. Every oracle below states
  the INTENDED seam (which check must refuse at which phase), the SNAPSHOT WINDOW (which pins are
  rechecked before/after which write), and the REPAIR (exact operator next action: fresh id vs
  explicit activate vs explicit resume vs preserve-INDETERMINATE).
- Earlier-stage refusal is NOT evidence for a later seam (decision §9). Each negative must hit its
  intended public seam. A supplement that proves a different seam does not close the listed seam.
- If any accepted-authority or consumer contradiction remains, stop before implementation and return
  the precise contract issue, not a weakened checker (decision §9 stop rule). Unpreservable predicate
  → contract revision or precise NO-GO, never hash-only acceptance.
- Code is committed meaningfully ONLY in independent authorized synthetic fixture DBs BEFORE
  authority creation; ordinary candidate/reconstruct commits still require Human; no fixture objects
  in reconstruct's DB (see §5). No genuine approvals: synthetic type-actor PASS is labelled, never
  promoted; production semantic quality stays NO-GO on placeholder editions.
- CLI exits: `0` success; `2` refusal-or-operation-failure (all typed `EditorialError(code,phase,disp,detail)`
  `survey_editorial_publication_v2.py:181–191` / low `PublicationSetError` mapped to `2` with structured
  `phase/code/disposition` + primary/secondary errors + observed State status on stderr, same discipline
  as existing `main():3914–3917`). Unexpected failures must be nonzero, never converted to PASS.

## 1. Full resume intent equality (exact; not set SHA alone)

`resume_renewal_activation(root, state_path, record_path)` reloads record+set+basis and compares the
COMPLETE intent below (decision §11.1). Any field mismatch → `INTENT_MISMATCH` (refuse, preserve all
bytes, direct the operator to the correct record/id); ordinary `activate_renewal` on an already-existing
exact intent → `INTENT_COLLISION` (refuse pre-write, direct to explicit resume — precedent
`survey_editorial_publication_v2.py:3152`); `RECORD_COLLISION` when the record file already exists
(precedent `:3387,3545`).

Required equal fields (all reloaded, all compared; `recorded_at` via `core.parse_instant`):

1. `branch`: `kind == VERSIONED_RENEWAL_ACTIVATION_V1` AND `reason_class == REVIEWED_VERSIONED_CORE_RENEWAL`
   (unknown branch refuses — low chain discipline `survey_publication_set_v2.py:1069–1194`).
2. `issue_id` (record vs set vs basis vs proof vs receipt vs Candidate vs State selection).
3. `original_checkpoint`: `prior_checkpoint{path,sha256}` (exact original validation checkpoint; must
   remain immutable on disk; `_check_authority_ref` live recheck).
4. `canonical_anchor`: `{kind,ref}` (must equal latest legacy immediately before FIRST versioned
   activation; repeated operations never roll it forward; mixed chain with later legacy successor
   fails closed — low `1189`).
5. `supersedes`: exact `{path,sha256}`-or-`null` edge (chain walk newest→oldest with
   `_walk_chain_backwards:1023–1051` discipline: cycle/depth `CHAIN_LIMIT 32` refusal, strictly
   increasing sequence, nondecreasing time, no duplicate links, no cycles).
6. `before_state_ref`: exact `{path,sha256}` (must equal bound proposal basis State ref AND retained
   basis State ref — low `_validate_proposal_retention_identity:1329–1360` discipline, renewal-dir
   variant per `interfaces-schemas-digests.md` §§4/8).
7. `retained_copy_ref` + `retained COPY binding`: `R/retained/before/<original-State-relative-path>`,
   `sha256 == row.sha256`, `len == byte_count`, `retained_dest == _expected_retained_dest(renewal_dir, path)`
   renewal-dir variant (`survey_editorial_retention_v2.py:831–854` discipline), full retained inventory
   exact (every COPY dest + manifest; retained root + ancestors; late new file/empty dir refuses).
8. `before_active_digest`: recomputed with the EXISTING effective7+Candidate algorithm
   (low `before_active_digest:353–415`: exactly seven publication roles, sorted, unique, `{name,path,sha256}`
   + `{path,sha256}`-or-null Candidate via `core.sha256_object({effective,candidate})`), never accepted
   as a caller value (low `1285–1313` mismatch refusal precedent).
9. `before_candidate_ref`: exact `{path,sha256}`-or-`null` (nullable ONLY when no canonical Candidate
   exists on disk — low `1443–1462` rule).
10. `set_ref` + `set_sha256`: `R/publication-set.json` path+SHA (seal `set_sha256 == sha256_object(except self)`
    low `463–468`; 15 roles exact `492–511`; role paths per `interfaces-schemas-digests.md` §13 C6).
11. `renewal_basis_ref` + `basis_sha256` (+ `retained_copy_ref` inside basis): basis bytes at resume time
    must equal the basis bytes at capture (any drift → `BASIS_ACCEPTED_SHA_DRIFT` / `RETAINED_COPY_MISSING`).
12. `renewal_proof_ref` + `proof_sha256` (+ `comparison.disposition`, `reader_digest`, `trio_digest`):
    proof bytes at resume time must equal proof bytes at finalize (equal-SHA different-path refused).
13. `new_core`: `current_tools{repository_commit_sha,contract,closure}` + `contract_identity`
    (must equal the pins at finalize; any eligible Core commit landing between finalize and activate →
    refuse and require a fresh basis/id, never silent update).
14. `executor` + `reason` (truthful free-text Core-change reason; free text equal, `reason_class` fixed
    by kind, never from CLI) + `recorded_at` + `establishment` (pre-decision sanctions:
    `VALIDATED_DRAFT/approved/pending/pending/pending` + `implementation_commit_sha` + instants —
    low `1293–1307`).
15. Observed State status at resume: exactly-before (ordinary collision → explicit resume may install
    after full revalidation) vs exactly-expected-after (readonly `ALREADY_ACTIVE`, full strict active
    readback, no regenerated approval) vs neither-before-nor-expected-after/unsafe/unreadable
    (`INDETERMINATE`, preserve all bytes, no rollback/overwrite/adoption, never delete referenced or
    possibly-referenced records).

`before_active_digest` recompute uses the existing effective7+Candidate algorithm; basis/proof are
additionally covered by new set + record refs (decision §11.1). Resume never compares set SHA alone.

## 2. Exact code/exit/disposition table (per observation/failure; decision §7 + §11.1)

| Observation / failure | Code | Phase | Exit | Disposition + repair |
|---|---|---|---|---|
| Entry ineligible (non-`VALIDATED_DRAFT`, Architecture not approved, Preview decided, Freeze/Release decided, exception active, missing/foreign/ambiguous authority, unrecognized old shape, dirty/untracked control roots, unavailable tool blobs, nonancestor epoch, unsafe path, changed research/Profile, unsupported shape) | `BASIS_ENTRY_INELIGIBLE` (+ specific `HISTORY_*`/`BASIS_*` where applicable) | `PIN`/`PREPARE` | 2 | `REFUSED_PRE_WRITE`; preserve; no R claimed; fix eligibility or open a migration contract |
| Historical identity fails (commit/blob/schema/digest/ancestor/mode) | `HISTORY_COMMIT_MISSING` / `HISTORY_BLOB_MISSING` / `HISTORY_SCHEMA_MISSING` / `HISTORY_DIGEST_MISMATCH` / `HISTORY_ANCESTOR` / `HISTORY_TOOL_EPOCH_DRIFT` / `HISTORY_PACKAGE_MUTATED` | `VERIFY_HISTORY` | 2 | `REFUSED_PRE_WRITE`; never reconstruct from network or forge ancestry (partialDB-26309 missing → `HISTORY_BLOB_MISSING`) |
| Incomplete prepare/finalize (any pin/drift/schema/digest/review/proof/basis/COPY failure before seal) | specific `BASIS_*` / `RENEWAL_PROOF_*` / `REUSE_TARGET_MISMATCH` / `REVIEW_TARGET_MISMATCH` / `UNSUPPORTED_MIGRATION` | phase of the failing pin | 2 | `PRESERVED_INCOMPLETE`; old pointer unchanged (NOT certified current-healthy); retry uses a NEW id; no same-byte takeover |
| Complete inert seal, no record | `RECORD_COLLISION` (absent record) | `ACTIVATE` | 2 | `REFUSED_PRE_WRITE`; explicit `activate_renewal` with FULL revalidation (no auto-adopt) |
| Complete record, State exactly before | `INTENT_COLLISION` on ordinary activate | `ACTIVATE` | 2 | `REFUSED_PRE_WRITE`; explicit `resume_renewal_activation` reloads record+set+basis and compares §1 full intent, then may install |
| State exactly expected after | `ALREADY_ACTIVE` | `ACTIVATE`/`RESUME` | 0 (readonly) | `ALREADY_ACTIVE`; full strict active readback; NO regenerated approval |
| State neither before nor expected after, unsafe/unreadable | `INDETERMINATE` | `ACTIVATE`/`RESUME`/`READBACK` | 2 | `INDETERMINATE`; PRESERVE all bytes; no rollback/overwrite/adoption/deletion |
| write/close/fsync/replace/postread/foreign-inode failure | specific `TARGET_EXISTS` / `BUILD_TRANSFER` / `RECORD_COLLISION` + secondary error | phase of the write | 2 | preserve PRIMARY + SECONDARY errors + observed old/new/unknown; never delete referenced or possibly-referenced records |
| U mismatch (renderer/trio/manuscript/PDF/build3 drift) | `REUSE_TARGET_MISMATCH` | `PROOF`/`PREPARE` | 2 | `REFUSED_PRE_WRITE`; never auto-switch to C; new `RENDER_TARGETS` attempt needs a new id |
| False reason / research/Profile/Architecture/Draft / pipeline-quality contract / review-requirements / route / recipe-spec change | `UNSUPPORTED_MIGRATION` (+ `CONTRACT_MISMATCH` / `CLOSURE_SET` / `CODE_DEPS_EXPANSION_REQUIRED` / `TOOL_DRIFT` / `STYLE_MISMATCH` / `REPLAY_MISMATCH` with missing/extra/drift lists where applicable) | phase of the detecting check | 2 | `REFUSED_PRE_WRITE`; route to a separate migration contract, never a reason-only plan |
| Wrong issue/manuscript/source/PDF/proof path/hash/basis; mismatched proof in Candidate/QA/Gate/receipt/seal; inert rival; foreign/missing old State COPY; postactivation readback without before-State equality; 32/33/cycle/anchor | `REVIEW_TARGET_MISMATCH` / `RECORD_COLLISION` / `INTENT_MISMATCH` / `INDETERMINATE` (per row) | phase of the binding check | 2 (0 only for readonly `ALREADY_ACTIVE`) | per §1/§3 rows; every record/State ownership/write/close/fsync/replace/postread failure reports the IMMEDIATE observed delta + explicit resume/healthy control |

Intended-seam rule: each negative in §§3–4 MUST hit its listed seam. Refusal at an earlier phase
(e.g. entry refusal when the oracle targets Gate proof threading) does NOT close the later seam.
Snapshot window: entry pins → capture (COPY claim + basis LAST) → proof → build-record → receipt →
QA/Gate/Candidate → seal LAST → validate → activate/resume; pins rechecked BEFORE capture, AFTER
basis write (`observe_renewal_authority`), BEFORE finalize, IMMEDIATELY BEFORE activate, and rechecked
AFTER each write phase (async-build-window recheck precedent `prepare_publication:1610–1611`;
finalize recheck `2047–2054`; Freeze `_recheck_snapshot:248–256`). Any drift → refuse + repair per table.

## 3. Fault oracles (every seam fault-tested with immediate observed delta + explicit resume/healthy control)

For EACH of: every record write (`R/renewal-basis.json`, `R/retained/before/...` COPY, inventory,
`R/renewal-source-proof.json`, C `R/staged-source/*`, `R/build/*`, `R/build-record.json`,
`R/validated-source-manifest.json`, `R/quality-regression-bundle-v2.json`,
`R/reader-surface-gate-v2.json`, `R/publication-candidate-v2.json`, `R/publication-set.json`,
activation record) AND every State ownership/write/close/fsync/replace/postread step
(known-byte State temp/replace on `publication_revalidation_provenance` ONLY, full new active
readback):

- Inject: `TARGET_EXISTS` (pre-existing conflicting OR same-byte target; exclusive
  `O_CREAT|O_EXCL|O_NOFOLLOW` claim must refuse — precedents
  `survey_editorial_publication_v2.py:493,1577,1617,1627,2138,2221,2267,2317,3152,3387,3545`);
  close failure; fsync failure; replace failure; postread mismatch (written bytes != readback);
  foreign-inode observation (expected path resolves to an unexpected `(st_dev,st_ino)` — Freeze
  `_preflight_freeze_pair:377–390` discipline).
- Observe: PRIMARY error + SECONDARY error + observed old/new/unknown State + which pins drifted
  (exact path/SHA/size deltas, not a bare code).
- Repair: incomplete → `PRESERVED_INCOMPLETE` + fresh id (never same-byte takeover, never cleanup
  of foreign/unknown residue); complete-inert-seal-no-record → explicit `activate_renewal` with full
  revalidation; record-exactly-before → explicit `resume_renewal_activation` with §1 full intent;
  expected-after → readonly `ALREADY_ACTIVE` (full strict active readback); neither/unsafe →
  `INDETERMINATE` preserve (no rollback/overwrite/adoption/deletion).
- Healthy control for every fault: the same operation WITHOUT the injected fault must reach the
  expected disposition (`INSTALLED` / `ALREADY_ACTIVE` readonly / `REFUSED_PRE_WRITE` for negatives)
  with identical pins, proving the fault (not the harness) caused the refusal.
- No multi-file atomicity / global CAS / crash-atomicity claim; single-writer/held-descriptor
  bounded guarantees only. No root deletion, no automatic stale adoption, no retrospective PASS.

## 4. Public positive oracles (real generated Weekly + Longform; intended seam + snapshot window + repair)

All positives use REAL accepted fixture graphs (not fabricated shape-only history), REAL derived
trio/reader bytes, and genuine eligible pinned Core changes (see §5 epoch discipline). Synthetic
approvals are labelled; production semantic NO-GO on placeholder editions is retained separately.

- **P-U1 (Weekly U after genuine changed pinned Core implementation):** bootstrap from an actual
  R3-format authority produced under its real older tool source; change a pinned implementation
  file that leaves trio/manuscript/PDF bytes bit-identical under the CURRENT renderer (U narrow
  condition via `verify_renewal_rerender_equality`: disposable-temp trio + complete canonical reader
  equality at ORIGINAL paths); run entry → COPY/basis (`REUSE_TARGETS`, `toolchain None`) → proof
  (`REUSED_TARGETS`) → reused-build wrapper/receipt → fresh QA inputs → Gate (early scope,
  proof+receipt-bound, no inferred `P/publication/` path) → Candidate (nested manuscript/reviews/
  bundle with SAME proof ref) → seal LAST → validate → activate → full active readback → normal
  active Candidate → direct stage → synthetic Preview/Freeze/Release. Intended seam: U proof threading
  + Gate early-scope binding + Freeze `_prepare_freeze_inputs` proof threading (§10) + active selection
  (`_require_active_candidate_binding`, `resolve_publication_selection`). Snapshot window: entry pins
  → basis LAST → proof → receipt (after build-record) → QA/Gate/Candidate → seal → activate; any drift
  refuses. Repair on drift: fresh id. Old bytes preserved (old trio/manuscript/PDF/log/reviews at
  ORIGINAL paths; new receipt/QA/Gate/Candidate/seal/activation under `R/`); bootstrap adapter from
  actual R3 authority; no canonical install/Profile rebind/copied review-target relocation/genuine PASS.
- **P-U2 (Longform U, same as P-U1 on the Longform route):** same seams on
  `LONGFORM_GENERATED_V1` + Longform projection/archive-authorization/canonical-bytes/render helpers
  + `LONGFORM_MAIN_BIB_STYLE` derivation. Proves both generated routes (decision §1 requires both).
- **P-C1 (Weekly C after current-source change with real PDF):** change a current source that alters
  the derived trio at NEW `R/` paths; run entry → COPY/basis (`RENDER_TARGETS`, explicit toolchain spec)
  → derived trio → proof (`NEW_TARGETS`) → C manuscript (`renewal_source` branch) + real disposable
  build/transfer (`EXECUTED_BUILD`: actual inputs/outputs/tool/exit evidence under the fixed recipe,
  `exit_code == 0`) → executed-build record → receipt → NEW external postrender semantic+visual reviews
  at exact new targets + actual QA inputs → QA/Gate/Candidate → seal → activate → active readback →
  normal lifecycle. Intended seam: C staged derivation + build-record-before-receipt + new postrender
  reviews (early scope usable ONLY as historical input, never waiving postrender) + Gate trio/manuscript
  binding (`1231–1251`). Old closed4 untouched; new staged trio/manifest/build3/manuscript under `R/`.
- **P-C2 (Longform C, same as P-C1 on the Longform route):** same seams on Longform.
- **P-S1 (source-only vs same-trio/different-PDF distinctions):** source-only/comment-only TeX change
  that alters trio bytes → MUST be C (never U); same trio + different PDF bytes (incl. metadata-only
  `CreationDate`/`Producer`/`ID` or `page_count` delta) at new paths → MUST be C with new visual review
  (exact-PDF TARGET invalidation). Intended seam: byte-derived U/C classification (same SHA at a different
  target path is C — decision §1) + `REUSE_TARGET_MISMATCH` (no auto-convert, no caller mode trust).
- **P-N1 (active normal Candidate → direct stage → synthetic Preview/Freeze/Release):** after P-U/P-C
  activation, select the State-selected Candidate/proof (NOT a standalone inert Candidate), run full
  normal validations + Profile-bound canonical Freeze/Manifest conventions + producer AND loader
  recomputed-path hash comparison (no fallback to canonical Candidate; explicitly refuse unsupported
  handoff mode — `survey_handoff_v2.py:101–102` basis-preemption is not stage coverage). Intended seam:
  `_prepare_freeze_inputs` (proof derived from validated Candidate, passed to direct review loader,
  bundle equality) + snapshot + `_preflight_freeze_pair` overlap/alias protection over the new closure
  (proof/basis/retained COPY/current closure/all reachable evidence, deduped by exact path/hash).
- **P-N2 (bootstrap + steady-state + repeat + renewal→editorial + R1×2 chain):** bootstrap from actual
  R3-format authority under its real older tool source (finite compatibility adapter, explicitly
  registered schema/module closure, legacy shapes preserved); later steady-state renewal under the same
  contract (runtime derives actual old/new tool commits + changed paths; artifact-only commits never
  qualify); repeat renewal with another genuine eligible Core commit + fresh basis (retry of the exact
  already-active record is readonly `ALREADY_ACTIVE`); renewal→editorial (P1 repeated pre-Preview:
  prior immutable versions KEEP + State COPY fresh, true-repeat P2V on the NEW pointer); R1×2 →
  editorial → renewal anchor preserved (latest legacy before FIRST activation is the permanent anchor;
  never rolled forward). Intended seam: mixed editorial/renewal chain (active-inclusive max32, strictly
  increasing sequence, nondecreasing time, no cycles; later legacy successor unsupported) + existing
  R1/canonical pre-write refusal in versioned mode. All are MANDATORY same-unit capability tests, not
  claims that existing P1/P2R already support the new kind (decision §8).
- **P-N3 (history/current readback + readonly already-active retry):** `verify_renewal_history` (record-only)
  returns descriptive `HISTORICAL_IDENTITY_VERIFIED` + observed refs (never a permit); detached
  `validate_renewal_basis` readback validates RETAINED before-State (never requires live-before equality
  after activation); high observation demands live-before equality ONLY at write boundaries; exact
  already-active retry is readonly `ALREADY_ACTIVE` (full strict active readback, no regenerated approval).
  Intended seam: authority-timing separation without a public skip flag.

## 5. Public negative oracles (each hits its intended seam; earlier refusal is not evidence)

- **N-H1 stale validators refuse without proof:** old standalone manuscript/Gate/Candidate validators
  (current-P3S mode: `verify_staged_source:237–247`, Gate `1173–1177`, seal `690–697`) refuse the old set
  under the NEW tools WITHOUT the explicit `renewal_source_proof_ref` context. Intended seam: U reloadable
  proof-ref context (historical identity + current semantics/trio against the NEW proof); standalone legacy
  path keeps current P3S refusal. A stale refusal elsewhere is not evidence for this seam.
- **N-H2 same-SHA different targets/proofs:** same trio/PDF SHA at a different target path; same proof SHA
  at a different proof path in Candidate vs QA vs Gate vs receipt vs seal. Intended seam: exact path+SHA
  equality at every hop (seal-map `_check_doc_refs_against_seal`, manuscript `263–269`, Gate `1250–1251`,
  Candidate `778–779,784–788,801–811`); equal-SHA different-path is refused, never silently substituted.
- **N-H3 false reason:** minting P1 identical-reader `NO_EDITORIAL_CHANGE`
  (`survey_editorial_correction_proposal_v2.py:1640–1670`) with a false editorial reason for a Core-only
  change, or activating renewal with an editorial/core `reason_class`. Intended seam: distinct
  `REVIEWED_VERSIONED_CORE_RENEWAL` + `VERSIONED_RENEWAL_ACTIVATION_V1` routing (no laundering through P1
  or the canonical writer; R1/canonical stay pre-write refused in versioned mode).
- **N-H4 reader/research/Profile delta:** any accepted-reader, research acceptance, Profile, Architecture,
  Draft authority, pipeline/quality semantic contract, review-requirements, route, or build recipe
  SPECIFICATION change presented as renewal. Intended seam: `UNSUPPORTED_MIGRATION` (separate migration
  contract required; P1 identical-reader refusal + original P2V epoch checks preserved).
- **N-H5 unsupported contract/recipe/schema migration:** `CONTRACT_MISMATCH` / `CLOSURE_SET` /
  `CODE_DEPS_EXPANSION_REQUIRED` / new required schema key / `additionalProperties` relaxation / new
  kind / route-semantics change / toolchain rule change. Intended seam: steady-state exact current closure
  membership + schema/contract equality (apart from permitted implementation/style bytes); bootstrap
  additions are the finite R3 adapter only.
- **N-H6 forged historical tool row / swapped epoch / missing blob:** receipt closure / staged `code_deps` /
  `style_input_ref` / `capture_inputs` row forged, epoch cross-substituted (receipt rows vs receipt epoch,
  staged rows vs `producer_head` — decision §2 separate-epoch rule), or blob missing (partialDB-26309).
  Intended seam: typed E/T classification (tool rows from typed `RECEIPT_TOOL_CLOSURE` edges + fixed closure
  membership, never `KEEP`/directory prefix) + per-document epoch binding; missing → `HISTORY_BLOB_MISSING`
  (never reconstructed, never forged from network).
- **N-H7 tool KEEP vs evidence KEEP distinction + old-evidence-absent-from-tool-commit positive control:**
  tool rows that are normally KEEP under `_pol` (`783–791`) must satisfy BOTH live+retained-COPY (as evidence
  where applicable) AND epoch-blob (as tools) where both roles hold; unknown/ambiguous roles refuse. The
  positive control (old evidence absent from the tool commit, expected because records are produced after
  that commit) must PASS history (evidence is NOT required to exist in the tool commit — decision §3).
  Intended seam: E/T/C trichotomy (identity vs replay vs current eligibility); listed hash alone proves
  nothing (decision §3).
- **N-H8 forged accepted package/acceptance/State basis:** `package_sha256` / `acceptance_sha256` /
  `state_sha256` / `state_path` / `issue_id` / Profile bindings forged; sibling-acceptance hash binding
  broken; canonical SOURCE path mismatch (§11.3 six conditions). Intended seam: §0 corrected State-SHA rule
  (package stays historical; drift tolerated ONLY under §11.3 1–6 with same canonical SOURCE path +
  package==acceptance==basis + retained-COPY chain + every other predicate; NO package mutation, NO
  original-`state_path`-vs-retained-dest compare). Any other substitution → `BASIS_*` refusal.
- **N-H9 fake scope `SCOPE_BOUND`:** original P2V `SCOPE_BOUND` on an already-activated proposal presented
  as a renewal permit. Intended seam: renewal-aware `observe_renewal_authority` (basis-bound) + fresh COPY;
  original `observe_current_authority` correctly refuses after activation (`P2V_AFTER_ACTIVATION_REFUSED`
  `survey_editorial_current_authority_v2.py:197`) unless true repeat.
- **N-H10 U mismatch:** renderer-equality runner reports `reader_equal==false` OR `trio_equal==false` OR
  old manuscript/build-unit live bytes drifted. Intended seam: `REUSE_TARGET_MISMATCH` (refuse pre-write,
  exit 2; never auto-convert to C). Source-only/comment-only, PDF-metadata-only, and different-manuscript-
  path cases are C per P-S1, not U exceptions.
- **N-H11 C missing/stale postrender review + no fresh QA + mismatched proof:** C with absent postrender
  semantic/visual reviews, stale reviews (exact manuscript/source/PDF/`page_count`/digest mismatch per
  `validate_review_record:668–690` + `validate_candidate:801–811` + Gate `1237–1251`), no fresh QA rows
  (`validate_checks:132–174` applicable-family completeness), or Candidate/QA/Gate/receipt/seal carrying
  different proof refs. Intended seam: C new-review mandate + supplied-result validation (validator executes
  nothing) + full-set SAME-proof equality (equal-SHA different-path refused).
- **N-H12 inert rival Candidate:** a self-validating inert Candidate (valid bytes, never State-selected)
  presented as the active selection. Intended seam: State-selected ref equality at normal admission
  (low projection returns refs structurally; stage `_require_active_candidate_binding:73–100` /
  `resolve_publication_selection` / `require_active_or_canonical` refuse stale/drifted canonical Candidates
  in `VERSIONED_ACTIVE`; preseal explicit untrusted proof refs are reloaded, active consumers derive proof
  from the State-selected set).
- **N-H13 foreign/missing old State COPY + postactivation readback without before-State equality:**
  renewal basis with a foreign/absent `R/retained/before/...` COPY (no recorded COPY mapping, no valid
  before-State/COPY chain) or a detached readback that demands live-before equality after activation.
  Intended seam: HISTORY validates COPY historically + `validate_renewal_basis` validates retained-COPY on
  every proof readback (detached, retained-before only) + HIGH demands live-before equality ONLY at write
  boundaries (decision §11.1 role split; no authority through returned dicts).
- **N-H14 32/33/cycle/anchor + every ownership/write/close/fsync/replace/postread failure:** chain deeper
  than 32, 33rd activation attempted before writes, cycle, duplicate link, mixed chain with later legacy
  successor, anchor rollover on repeat, nonincreasing sequence/time (low `1023–1230` discipline); every
  §3 fault row with immediate observed delta + explicit resume/healthy control. Intended seam: pre-write
  refusal (chain/anchor) + §3 fault table (no deletion, no auto-adoption).
- **N-H15 Freeze nested review + proof mutation/alias:** Freeze with a nested review validated WITHOUT the
  containing Candidate's proof ref; proof/basis/retained COPY/current closure mutated between
  `_prepare_freeze_inputs` snapshot (`213–229`) and `_preflight_freeze_pair` install gate (`323–...`);
  Freeze/Manifest target overlaps/aliases an authority input (`347–390` discipline). Intended seam: nested
  proof threading (same reloaded ref, bundle equality) + snapshot file list (proof/basis/retained COPY/
  closure/all reachable evidence, deduped by exact path/hash, no outside-`R` omission) + alias protection
  over the new closure + `_recheck_snapshot:248–256` (any drift refuses; repair is a fresh id).

## 6. Synthetic fixture-source epoch sequencing (independent DB, no object sharing, code before authorities)

- Fixture source identities: REAL accepted fixture graphs (Weekly + Longform, both routes) with exact
  checkpoint/accepted package/result graph + Screening/Evidence/Discovery/X/archive relationships +
  Selection/Synthesis/Architecture/Draft checkpoint acceptance + research raw/access/card lineage
  (sibling file owns the predicate bodies; this file requires their presence, not their shape-only form).
  No fabricated shape-only history.
- Independent DB: ALL fixture objects/refs/commits live in an INDEPENDENT Git database with an inert
  origin (`https://example.invalid/...`), NO alternates, NO hardlinks, NO object sharing with
  reconstruct's DB, NO inherited Git-root overrides. Process-scoped Git identity. Never create fixture
  objects in reconstruct's DB. Unrequested empty-root commits (`--allow-empty`) are forbidden; use
  meaningful independent fixture contents + real available ancestry.
- Epoch sequencing: source CODE is committed meaningfully in the fixture DB BEFORE any renewal authority
  is created (basis/proof/receipt/seal/activation). Tool epochs (`repository_commit_sha` in old/new
  `current_tools`, staged `producer_head`, receipt `current_tools.repository_commit_sha` minted at prepare
  before publication authorities exist) are recorded truthfully; recorded historical tool hashes are never
  accepted merely because a receipt lists them, and historical schemas are supported by the finite
  compatibility evaluator + epoch cross-check (no arbitrary historical schema code or remote `$ref`
  execution/fetch). External executable evidence is recorded (absolute path, `real_sha256`, versions/argv/env,
  recipe markers), never Git-blobbed, never re-probed from an absent executable, never forged into an old log.
- No ordinary candidate commits: ordinary final reconstruct commit/Pull/Push remain Human-owned
  (Human Commit Point). No new HEAD/candidate commit in the implementation evidence run. No Production
  Actions execution in development (`handoff_required:false` basis preemption is not stage proof; configured
  `handoff_required` false preserves the limitation).
- No genuine approvals: synthetic type-actor Preview/Reviews/Freeze/Release are labelled synthetic;
  semantic/visual PASS is never self-generated (operation authors no semantic/visual PASS — operator review
  §20); external postrender reviews are supplied records at final repo-contained immutable paths (result deps
  from validated schemas, no symlinks/latest/mtime authority). Placeholder editions stay production-semantic
  NO-GO. No approval inferred from missing records.
- Required bookkeeping per run: source/run composition (which fixture DB commit + which actual57 pins +
  which Core-change diff), skips, failures, provider/quota limits, incomplete runs. Do NOT rerun unrelated
  suites for decoration. Meaningful regressions for affected original routes/R1/DM004 only. Saved historical
  runners are evidence-only, never auto-rerun instructions; their equality policies are not shipping guards.
  First-six inactive smokes / packaging first-pre-GEN raw loss / prior R2 raw-loss qualifications are preserved
  as closed qualifications, not reconstructed.

## 7. Gate-ready checklist (this file) + exact blocker rule

- [x] Full resume intent equality (§1, 15 fields; not set SHA alone) grounded in low chain/anchor/digest/
      retention rules (`1023–1230,1239–1314,1443–1462`) + `_fail`/`INTENT_COLLISION` precedent (`3152`).
- [x] Exact code/exit/disposition table (§2) per decision §7 six rows + §11.1 error taxonomy
      (`HISTORY_*`/`BASIS_*`/`RENEWAL_PROOF_*`/`REUSE_TARGET_MISMATCH`/`UNSUPPORTED_MIGRATION`/
      `REVIEW_TARGET_MISMATCH`/`RECORD_COLLISION`/`INTENT_MISMATCH`/`INDETERMINATE`/readonly
      `ALREADY_ACTIVE`) with CLI `0`/`2` discipline (`main():3914–3917`).
- [x] Fault oracles (§3) for every record/State write/close/fsync/replace/postread/foreign-inode seam
      with intended seam + snapshot window + repair + healthy control (precedents: `TARGET_EXISTS`/
      `PUBLICATION_EXISTS` family; Freeze `_preflight_freeze_pair:323–390`; State temp/replace on
      `publication_revalidation_provenance` ONLY).
- [x] Public positives (§4: P-U1/P-U2/P-C1/P-C2/P-S1/P-N1/P-N2/P-N3) with intended seam + snapshot window +
      repair, covering both routes, both U/C cases, byte-derived U/C distinctions, bootstrap/steady-state/
      repeat/renewal→editorial/R1×2 anchor, history/current readback, readonly already-active retry.
- [x] Public negatives (§5: N-H1–N-H15) each hitting its intended public seam (stale validators without
      proof; same-SHA different targets/proofs; false reason; reader/research/Profile delta; unsupported
      migration; forged tool row/epoch/blob; KEEP distinction + absent-from-tool-commit control; forged
      package/acceptance/basis; fake scope; U mismatch; C missing/stale review + no QA + proof mismatch;
      inert rival; foreign COPY + postactivation readback; 32/33/cycle/anchor + ownership/write faults;
      Freeze nested/alias), with earlier-stage refusal explicitly NOT counting as later-seam evidence.
- [x] Fixture/source epoch discipline (§6): synthetic fixture-source epoch sequencing, independent DB / no
      object sharing / no reconstruct-DB fixtures / meaningful contents (no `--allow-empty`), code committed
      before authorities, no ordinary candidate commits, no genuine approvals, full run bookkeeping.
- [ ] Sibling `interfaces-schemas-digests.md`: REFERENCED (schemas/digests/entries/call-map/inventory/
      threading + C1–C8 root choices), not repeated.
- [ ] Sibling `accepted-authority-readiness.md`: REFERENCED (detailed State-free predicate bodies), not repeated.
- [ ] Third-agent fingerprint/closure return: REFERENCED (old-format fingerprints, successor closures,
      control-diff, recipe boundary, mode discipline), not invented.

**Exact blocker rule:** if any predicate in the sibling accepted-authority return, any fingerprint/closure
item in the third-agent return, or any C1–C8 choice in `interfaces-schemas-digests.md` §13 cannot close
without weakening a predicate (hash-only acceptance, dropped coverage, broad `pending`, caller verified
dict, ambient proof, same-byte takeover, retrospective PASS, genuine-approval laundering), the outcome is
the PRECISE contract issue or NO-GO plus a migration/separate-contract decision — never a weakened checker.
Implementation stays BLOCKED until Astra confirms all three returns. Whole NOT_READY / step4B3 OPEN / audit
unstarted / DM021+022 OPEN. Stop at Human Commit Point; no ordinary Commit/Push.

## 8. Superseding corrections R2 (2026-10-23 JST, Astra CHANGES_REQUIRED 1/4/6/10; original §§1–7 preserved above)

- **S1 (defect 1: nonnull predecessor).** §1 items 5/9 `supersedes-or-null` / `before_candidate_ref-or-null`
  and `prior_record_ref`/`prior_candidate_ref`-nullable wording are SUPERSEDED. Renewal predecessor
  MUST be an existing versioned active set (editorial or prior renewal) with live seal + live record +
  live Candidate. Legacy-only is UNSUPPORTED. All of `prior_selected_ref`, `prior_record_ref`,
  `prior_candidate_ref`, `supersedes`, `before_candidate_ref` are REQUIRED nonnull authority refs.
  Never infer from canonical Candidate existence. Resume §1 intent equality keeps all 15 fields with
  nonnull refs; `ALREADY_ACTIVE`/`INDETERMINATE` dispositions unchanged.
- **S2 (defects 4/6: no staged manifest, one new Gate branch).** §3 fault list `R/staged-source/*`
  and §4 P-C1/P-N1 `new staged trio/manifest` wording are SUPERSEDED as: C trio FILES
  `R/staged-source/{main.tex,references.bib,jgaisurvey.sty}` ONLY (NO `staged-source-manifest.json`;
  proof IS the staged proof). Renewal receipt/manifest carry NO `staged_manifest_ref`/
  `retention_manifest_ref`/`scope_review_ref` (see R2 §§2–3). C manuscript `renewal_source` is exactly
  `{path,sha256}` = `R/renewal-source-proof.json`. Gate is ONE new `VERSIONED_RENEWAL_V1` /
  `RENEWAL_MAIN_BIB_STYLE` branch BOTH U and C (old 4 branches verbatim, never augmented).
  Early-scope-as-history + new postrender review rules unchanged.
- **S3 (defect 10: external reviews).** §4 P-C1 `new postrender reviews at exact new targets` and seal
  `all NEW R/ roles` wording are SUPERSEDED as: C postrender semantic/visual RECORDs MAY be external
  repo-contained immutable final paths (pinned, not writer-owned, never deleted/rewritten; writer paths
  cannot alias supplied paths). Seal role paths point at actual locations (U original paths for
  manuscript/trio/build3/reviews; C new `R/` paths except external review RECORDs where pinned).
  Same-SHA different-path still refused; full-set SAME-proof equality unchanged.
- **S4 (defect 5/8/9/11 cross-refs).** U original manuscript bytes/digest unchanged (context-only
  `renewal_source_proof_ref` keyword, never serialized); C new manuscript carries `renewal_source`
  `{path,sha256}` (15-key digest: 14 + `renewal_source`); new Candidate (10+1)/bundle (9+1)/Gate (13
  with new 5th variant) carry proof refs per R2 §4. Contract is the 8-field
  `contract_identity` map (never `object`); KEEP rows carry `retained_ref=={path,sha256}` only,
  COPY rows carry `retained_dest+retained_sha256+retained_byte_count` only; KEEP is E (live+retained),
  T is epoch-blob only (never T live KEEP). Basis `accepted_refs` equals prior receipt list verbatim;
  authoritative `profile_ref`/`reviewed_reader_ref`/`authoring_refs` are separate top-level pins.

(End — author-side pre-code oracles + R2 superseding corrections §8. No independence claim.)
