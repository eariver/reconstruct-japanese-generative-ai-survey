# Retained-aware current-authority validator (P2V) — concrete contract proposal

2026-10-14. Design Co-Worker (General), design-only unit. No code/schema/test
edits, no fixtures/runs/adoption. Source basis is exact actual409
`409b292…`/tree `8ce36998…` +16file overlay (3M+13A) verified in
`source-binding.md` §§1–3 (direct HEAD/tree/status/16-hash/84-cache
observation). Fixed contracts unchanged: P1 `07e89990…`, P2R `194fd7de…`.
Mandatory bounds read: P2R assessment §4, Astra closeout (late-plant/proof-
logger narrowing, 1818-line erratum) + independent final §10. This is an
**initial General proposal, NOT selected until Astra review**; it will be
preserved with corrections.

## 0. Problem (why P2R verify alone is insufficient)

`verify_retention` (`retention_v2.py:1731-2080`) proves a supplied proposal’s
retained set is complete/consistent **now**: exact proposal→retained State
COPY→State.profile→KEEP Profile chain (`:1827-1900`), COPY/KEEP rehash
(`:1953-1963`), staged refs (`:1964-1988`), inventory closure (`:1926-1955`,
`:2043-2056`). It deliberately never calls P1/Git/HEAD/current-State and never
requires live COPY originals or current eligibility. Therefore:

- A forged former State with a self-consistent manifest, an old-byte rollback,
  a deleted-retention replay, or a stale proposal after live
  State/receipt/Gate/upstream/code drift can still `RETAINED_SET_VERIFIED`.
- Capture’s `capture_inputs` are historical observations, not live authority
  (independent §5, `:2009-2019` scope comment). Same-byte identity continuity
  without a baseline is beyond a fresh verifier.
- P1 public `validate_proposal` (`proposal_v2.py:1698-1830`) still refuses the
  same proposal after capture via `_retention_plan:1278-1284`
  (`RETENTION_DEST_CONFLICT`), by design (P2R contract §6). There is no
  “fresh P1 after retention” composition.

P2V (name used only to distinguish this read-only observer; not a reason/state
pointer, not a promotion writer) must bind **the SAME supplied
proposal/manifest/retained State/Profile** to **fresh P1-equivalent current
authority** in one invocation, read-only, without weakening P1, deleting
retention, forging former State, or treating persistence as adoption.

## 1. Fresh authority predicate (Q1/Q3)

P2V success means: the live current authority **now** still validates the
exact supplied proposal **and** the exact verified retained set is present.
All conjuncts required; any failure refuses (typed codes, §5):

1. **Live State/Profile/eligibility independent validation.** Same predicates
   as P1 `_pipeline:1291-1311` + `_validated_state_profile_for_tree:1536-1569`:
   strict `validate_agent_state` (pending publication never active),
   `_eligibility` (healthy VALIDATED_DRAFT, approved Architecture, pending
   Preview without provenance, pending downstream, inactive exception),
   State-bound Profile path/sha + issue binding, canonical State path
   (`state_file.resolve()==canonical`). No pending-basis bypass, no
   manufactured DRAFT_COMPLETE dict, no unreferenced-clone State.
2. **Original checkpoint (immutable).** Same as P1 `:355-377`: State-pinned
   `validation` ref exact path/sha, live bytes equal pin, identity/producer
   (`issue_id`, DRAFT_COMPLETE→VALIDATED_DRAFT, `validation` in checkpoints),
   7-row shape, no duplicates. Must equal proposal
   `basis.validation_checkpoint_ref` exactly (rederived basis equality, §2).
3. **Active-before (State-bound, R1-aware).** Same as P1 `:380-411`:
   `resolve_active_publication_revalidation` with fail-closed invalid (never
   fallback), exact coverage of original roles once, `ACTIVE_PATH_REBIND`
   refusal on path change, live-byte agreement (superseded `new_sha256` vs
   preserved pin). After real R1 predecessor(s) `active_revalidation_ref` is
   non-null; P2V requires live `active_revalidation_ref` **byte-equal** to
   proposal `basis.active_revalidation_ref` (null↔null, ref↔same ref). A new
   R1 after proposal (different active record) is `STALE_ACTIVE`, not a
   migration. Forged/unreferenced active file is a stop, never filename-
   selected.
4. **Before-graph/retention-plan equality (rederived, not trusted).** Same
   derivation routing as P1 `:431-451` (Longform `load_derivation_for_readback`
   allowlist vs Weekly `load_derivation`, no pending bypass), canonical bytes
   (`_canonical`), `NO_EDITORIAL_CHANGE` (before≠proposed), upstream equality
   (`_proposed_upstream_check`, `_frozen_names_check`), full receipt/Gate/
   bundle/pre-TeX validation (`:1393-1430`), graph+digests
   (`before_graph_digest`, `preserved_upstream_digest`), **except destination
   policy** (§2). Rederived `basis`/`proposed` (path+sha+digests)/`retention_plan`
   must equal supplied proposal exactly; staged reader FILE bytes must equal
   rederived canonical proposed bytes. Supplied `change_description` need only
   be nonempty (P1 `:1755-1794` rule preserved).
5. **Retained-set binding (same bytes).** Same checks as `verify_retention`
   `:1764-2056` on the SAME proposal/manifest bytes pinned in this invocation
   (header/basis/proposed, ordered plan projection, I1 chain, dest
   recomputation provisional+canonical, inventory, COPY/KEEP rehash, staged
   refs, `capture_inputs` required bindings, canonical bytes, final
   re-inventory). Historical `capture_inputs` extras remain observations;
   required plan/staged/proposal/P2R-dep bindings enforced. KEEP drift refuses;
   live mutable COPY-original drift does **not** by itself fail this conjunct
   (persistence), but it fails conjunct 4 (freshness) — see §6 oracle.
6. **Control/code/epoch/lifecycle (strict, no migration).**
   - **State file: strict byte equality.** Live State bytes must byte-equal
     `basis.state_ref.sha256` (rederived `basis.state_ref` equals supplied).
     **No permitted metadata changes to the State file.** Any State mutation
     (new revalidation pointer, new lifecycle, new profile ref, timestamps,
     counters) makes the proposal stale (`STALE_STATE`/`BASIS_MISMATCH`).
     Re-prepare, do not migrate.
   - **Control inventory: strict byte equality.** All P1-consumed dynamic deps
     (config, all `input_hashes` paths) must byte-equal proposal-time hashes
     (rederived equality + P2V snapshot recheck). No “metadata-only” control
     drift.
   - **Edition trees: strict except verified retained delta.** Live
     source_root/survey_root byte maps must equal proposal-time maps **plus
     exactly the verified retained files/dirs** (COPY dests + manifest +
     ancestor closure). Any other addition/change/disappearance/type/alias
     change refuses (`EDITION_DRIFT`). This mirrors P2R capture finalization
     (`:1390-1422`: owned delta only) applied to observation.
   - **Code epoch: current-code revalidation, no old-epoch migration.**
     `contract_identity` must equal current `core.contract_identity(...)`;
     full `validate_receipt` (Longform `:665-757` incl. review reload/contract/
     canonical-path/replay, or Weekly `:726`) must pass with **current code**
     on the **same receipt bytes** (`_final_full_receipt_recheck:1572-1598`
     pattern, not contract-only). `renderer_commit` must be a valid commit
     (`git cat-file -e`, Weekly `_verify_head_bytes` pattern); live HEAD must
     be stable during the call (P1 `_Collector.head`/`reverify` rule) but need
     **not** equal `renderer_commit` (artifact-only HEAD moves with same
     contract are not automatic staleness; contract change is). If current code
     epoch changed the contract, refuse `STALE_EPOCH` — do not re-derive the
     old proposal with new code and claim the same proposal still valid. Old
     P2R proposals prepared under a different epoch require a new
     `prepare_proposal` under current code, not P2V migration.
   - **Lifecycle: healthy VALIDATED_DRAFT throughout** (P1 eligibility mirrors
     controller `:1799-1812`); later multi-file promotion may temporarily fail
     closed rather than stay valid (P1 contract §6, preserved).

Forged former State, old-byte rollback, deleted retention, unchecked caller
assertion, and ignore-destination flags are all refused by construction (§2).

## 2. Minimal factoring vs duplication (Q2) — recommended factoring F

### 2.1 Why public P1 must stay strict

P1 `_retention_plan:1278-1284` refuses if any COPY dest already exists
(`RETENTION_DEST_CONFLICT`), even for the verified retained set. Public
`prepare_proposal`/`validate_proposal` must retain this: after capture they
refuse the same proposal. Any “ignore-destination” boolean flag, trusted
`input_hashes` token, or caller assertion that destinations are “already
verified” would let a caller bypass the absence check and manufacture
eligibility. Forbidden.

### 2.2 Recommended split (factoring F, not duplication)

Factor two **private** helpers; no new public P1 API, no public behavior change:

- **P1: `_retention_plan_with_policy(col, graph, proposal_dir, dest_policy,
  verified_set=None)`** — exact current `_retention_plan:1231-1288` logic with
  the absent-check parameterized by an enum, **not a boolean**:
  - `ABSENT_REQUIRED`: current behavior (any existing dest, incl. dangling
    alias, refuses). Used by existing `_retention_plan` wrapper and therefore
    by all public P1 paths.
  - `RETAINED_BOUND`: dest may exist **iff** it is in the caller-supplied
    `verified_set` (exact dest strings from the same-invocation retained
    verification, §4) **and** the caller has already verified those bytes +
    closed inventory in this invocation. Any dest outside the set, any missing
    set member, any extra file/dir in retained inventory, or any byte mismatch
    refuses. No “skip destination checks” path exists; both policies check
    destinations, with different acceptance sets.
- **P1: `_pipeline_common(col, root, state_path, new_authored_value,
  proposal_id, tree_entry, change_description, dest_policy, verified_set)`** —
  exact current `_pipeline:1291-1492` with `_retention_plan_with_policy` in
  place of `_retention_plan`. Existing `_pipeline` becomes a thin wrapper
  calling with `(ABSENT_REQUIRED, None)`. P2V calls with `(RETAINED_BOUND,
  verified_set)`.

Why each public success necessarily checks its required policy: there is no
shared success return that bypasses the policy branch. Public P1 success can
only exit via `ABSENT_REQUIRED` (refused if any dest exists); P2V success can
only exit via `RETAINED_BOUND` (refused unless dests exactly match the
same-invocation verified set + closed inventory + byte equality). Policy is
fixed per entry point, never caller-controlled. A reviewer can verify by
reading the two call sites (one line each) plus the enum definition; no
general resolver, no flag plumbing through public APIs.

P2R reuse needs **no P2R modification** (0M P2R): P2V calls existing
`verify_retention` as a black-box historical check **first**, then re-pins
**all** same proposal/manifest/retained/KEEP/staged bytes in its **own**
collector/session and rechecks them before and after the fresh-authority step
(§4). The `VERIFIED` token is never trusted as proof; it is only a necessary
precondition whose bytes are re-observed. This avoids a second P2R refactor
while closing the token-trust window.

**Rejected alternative D (separate verifier with full duplication):**
duplicate P1 rederivation (≈600 lines: eligibility/checkpoint/active/derive/
receipt/Gate/bundle/graph) + P2R inventory inside a new module with 0M P1/P2R.
Cost: large duplicated surface, guaranteed drift (any P1 fix must be ported),
reviewer must diff two implementations instead of one factored branch.
Only acceptable as fallback if Astra rejects even a private P1 refactor; it is
not recommended.

**Rejected general resolver:** a generic “follow every path-looking string”
graph walker or lock/journal framework is explicitly out of scope (P1 contract
§3, P2R contract §5). Per-helper snapshots + reverify + close (P1 `_Collector`,
P2R `_Session`) already close checked boundaries without global CAS.

### 2.3 Exact budget (not 2A2M, no reason/State pointer)

Recommended factoring F:

- **1A module** `scripts/survey_editorial_current_authority_v2.py` — public
  `observe_current_authority(root, state_path, proposal_path, manifest_path,
  scope_review_path=None)` + private snapshot/binding helpers (reuses P1
  `_Collector`-style safe reads or P2R `_Session`-style dirfd reads; final
  choice at implementation return, no generic framework).
- **1M module** `scripts/survey_editorial_correction_proposal_v2.py` —
  private-only factoring (`_retention_plan_with_policy`,
  `_pipeline_common`, wrapper preservation). **No public signature/behavior
  change, no new reason literal, no State pointer, no controller/Gate/receipt/
  publisher change.** Diff must show public `prepare_proposal`/
  `validate_proposal` byte-identical behavior (oracle §6 proves post-retention
  refusal preserved).
- **0 schema changes** — reuse proposal/manifest/review schemas byte-identical.
  P2V result is an in-memory dict (see §3 return shape); no new
  `*_schema.json`, no `RETENTION_MANIFEST_V1` shorthand, no new review block.
- **1A test** `tests/test_survey_editorial_current_authority_v2.py` — focused
  oracles §6 only; no P1-36/LF2I-43+2 transfer, no decorative full-suite rerun.
  Counts selected after diff (estimate 12–16 focused methods, not a promise).

Total: **2A1M, 0 schema deltas.** No new normal Human role/Gate, no
production-owned fixture prerequisite, no candidate commit (uncommitted overlay
is expected; HEAD stays 409).

If Astra rejects the 1M P1 refactor, fallback is 2A0M duplication D with
explicit drift cost (§7); return the decision, do not silently duplicate.

## 3. Call ordering + snapshot binding (Q5, no global CAS)

P2V is read-only (no writes, no cleanup, no retry). One invocation binds the
SAME proposal/manifest/retained State/Profile/KEEP/live-current
control+edition across helpers. Reusing a helper’s past success never covers
the next helper’s window. Order (each step re-pins + reverifies before the
next; any drift refuses, nothing written):

1. **Narrow pins (no broad walk from unvalidated Profile).** Safe-read State,
   config, State-bound Profile, proposal, manifest, both schemas (raw-first
   lexical→alias→regular→read, FIFO/device refused, bytes pinned). Pin live
   HEAD (sanitized Git env, `GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0
   GIT_ALLOW_PROTOCOL=file`, rc checked). Validate schemas; recheck schema
   bytes after validation (P2R `:952-954` pattern). Refuse retained-root
   absence here (P2V requires an existing retained set; missing/partial is
   `INCOMPLETE_RETENTION`, not success).
2. **Historical retained verification (same bytes).** Run existing
   `verify_retention` logic on the pinned proposal/manifest bytes (black-box
   call first for exact S3 precision, including provisional dest mapping
   `:1844-1860` before retained-State read and canonical dir `:1901-1925`).
   Then **re-pin in P2V’s own collector**: every COPY dest bytes+size, every
   KEEP ref bytes+size, retained State/Profile bytes, staged authoring/reader
   bytes, manifest/proposal bytes, `capture_inputs` required bindings. Final
   re-inventory (files+dirs) must equal `_retained_expected_sets` closure.
   Record `verified_set` (exact dest strings + manifest path) for §2 policy.
3. **Fresh current-authority rederivation (same live snapshots).** Snapshot
   live control inventory + edition trees (source_root/survey_root full byte
   maps, P1 `_tree_map` pattern) **after** step 2. Call factored
   `_pipeline_common` with `(RETAINED_BOUND, verified_set)` on the SAME live
   State/Profile/receipt/Gate/upstream paths. It re-pins all P1 inputs in its
   own `_Collector` (returning `input_hashes`), rederives graph/digests/
   proposal, checks eligibility/checkpoint/active/derivation/receipt/Gate/
   bundle/pre-TeX, compares all fields to supplied proposal, checks staged
   bytes, runs `_final_full_receipt_recheck` (full validator, not
   contract-only), reverifies tree+stability. Destination acceptance uses
   `verified_set` only; all else exact equality (no migration).
4. **Cross-binding.** Assert: rederived `before_graph_digest`/`preserved_upstream_digest`/
   `state_ref`/`generated_receipt_ref`/`contract_identity` equal supplied
   `basis`; rederived `retention_plan` (policies/paths/hashes/sizes/dests)
   equals supplied plan; manifest `rows.retained_sha256`/`retained_byte_count`
   equal plan row sha/size; live State bytes equal `basis.state_ref.sha`;
   live control/edition snapshots equal step-3 pins plus exactly the verified
   retained delta (§1). Any mismatch is staleness/drift, not a repair.
5. **Optional scope review (unchanged role, §4).** If supplied, bind via
   existing `_validate_scope` logic on SAME before/after/upstream bytes;
   absent → needs-scope observation (not bound). No new review production.
6. **Final boundary.** Re-inventory retained tree + re-read all consumed
   manifest/proposal/retained/KEEP/staged bytes + recheck live control/edition
   inventories (only verified retained delta allowed) + HEAD stability +
   close-all (P2R `_close_all` pattern: secondary close failures attached,
   never silent success). Only then return observation.

No global CAS, no crash-atomicity, no hostile-concurrency exclusion claimed
(P2R contract §5 preserved). Detectable drift at checked boundaries fails
closed; a crash leaves no success token (read-only, so no partials to
preserve; late drift before return is still refusal with pre/post evidence,
§6).

## 4. Optional scope review + output identity (Q4)

Reuse exact P1 `_validate_scope:1635-1695` + existing review schema block
(`EDITORIAL_CORRECTION_SCOPE_V1`, `EDITORIAL_CORRECTION_SCOPE` substantive
PASS with old/new/authority evidence). No new role/Gate, no generated PASS:

- Absent `scope_review_path` → `CURRENT_READINESS_NEEDS_SCOPE` (analogous to
  P1 `REVIEW_REQUIRED`): fresh authority + retained set observed, scope not
  bound. Not adoption.
- Supplied + PASS + WITHIN_APPROVED_AUTHORITY + exact before
  (`basis.active_reader_input_ref`)/after (`proposed_reader_ref`+canonical
  sha)/upstream (`preserved_upstream_digest`) bindings + substantive detail/
  evidence → `CURRENT_READINESS_SCOPE_BOUND` (analogous to
  `REVIEW_BOUND_PROPOSAL`). Non-WITHIN/wrong-before/wrong-after/stale-upstream/
  non-PASS refuses (`SCOPE_*`, never bound).
- Ordinary pre-TeX reviews without the block remain valid but do not bind.

Return shape (in-memory dict, no new schema file; code-validated, strict keys):

```python
{"result": "CURRENT_READINESS_NEEDS_SCOPE" | "CURRENT_READINESS_SCOPE_BOUND",
 "proposal_sha256": ..., "manifest_sha256": ...,
 "measured": {"before_graph_digest": ..., "preserved_upstream_digest": ...,
              "copy_files": int, "keep_refs": int, "staged_refs": 2},
 "input_hashes": {rel: sha256, ...}}  # all consumed bytes in this invocation
```

Refusals raise `CurrentAuthorityError(ValueError)` with `CODE: [phase/
disposition] detail` (P1/P2R pattern). Result names are observation-only
(`CURRENT_READINESS_*`); no `PROMOTION_GRANTED`/`ADOPT`/`PUBLISH`/`PASS` token,
no State-adoption permission, no future-mutation authorization. A reader cannot
mistake the result for granted promotion without misreading the literal.

## 5. Failure matrix (predicates → codes)

| Predicate violated | Code (phase) | Persistence vs freshness note |
|---|---|---|
| Proposal/manifest schema/header/basis/proposed/plan-order mismatch | `HEADER_MISMATCH`/`BASIS_MISMATCH`/`PROPOSED_MISMATCH`/`RETENTION_*` | Both fail; no rebind by equal SHA |
| Retained COPY/KEEP/staged/inventory/capture-input drift, missing/extra/duplicate, wrong dest, label mismatch | `INVALID_RETENTION`/`COPY_DRIFT`/`PROFILE_DRIFT`/`LABEL_MISMATCH`/`RETENTION_DEST_MISMATCH`/`CAPTURE_INPUT_*` | Verify fails; P2V fails (historical) |
| Live mutable COPY original replaced (retained still intact) | P2V `BASIS_MISMATCH`/`RETENTION_MISMATCH` (rederived graph differs); verify still `VERIFIED` | **Persistence-positive / freshness-negative** (key oracle §6) |
| Live State bytes ≠ `basis.state_ref` (any State mutation) | `STALE_STATE`/`BASIS_MISMATCH` | Refuse; re-prepare, no migration |
| Live active record ≠ basis (new R1, forged, path-rebind) | `STALE_ACTIVE`/`ACTIVE_*` | Refuse; original checkpoint still checked |
| Upstream/Draft/Architecture/archive drift | `UPSTREAM_*`/`PROPOSED_UPSTREAM_*` | Refuse; Weekly envelope-only preserved |
| Receipt/Gate/bundle/pre-TeX invalid, contract drift, renderer invalid | `RECEIPT_*`/`GATE_*`/`BUNDLE_*`/`PRETEX_*`/`RECEIPT_CONTRACT_DRIFT` | Full replay, not contract-only |
| Code epoch changed (contract ≠ current) | `STALE_EPOCH` | Refuse; no old-epoch migration |
| Control/edition drift beyond verified retained delta | `CONTROL_DRIFT`/`EDITION_DRIFT`/`FINALIZATION_REFUSED`-analog | Snapshots §3 |
| Scope absent/wrong/stale/non-WITHIN/non-PASS | `SCOPE_*` → needs-scope or refuse | No new Gate |
| Late drift between helpers, HEAD moved, close failure | `STABILITY_VIOLATION`/`HEAD_MOVED`/`TREE_MOVED`/`CLOSE_FAILED` | No-write read-only still proved via pre/post |
| Existing retained root absent/partial/foreign | `INCOMPLETE_RETENTION`/`INVALID_RETENTION` | No takeover/cleanup/retry |

All P1 destination-absence behavior preserved: public P1 on the same proposal
after capture still `RETENTION_DEST_CONFLICT` (oracle §6).

## 6. Concrete oracle plan (Q6 — both routes, actual R1, no execution here)

Synthetic accepted-chain fixtures only (Longform prose primary, Weekly
envelope-only per P1 contract; accepted Draft/upstream unchanged; no
production-owned edition, no new Human Gate, no genuine semantic/Human
approval). Real R1 predecessor case distinguishes original checkpoint from
active-before (construct valid predecessor pointer when possible per P1
evidence; never forged/filename-selected). Each oracle snapshots before any
comparison and proves no writes (read-only: pre/post tree+`input_hashes`
equality; no cleanup to mask drift):

1. **Unchanged-live positive after retention (Longform + Weekly).** Capture,
   then P2V observes readiness (needs-scope without review, scope-bound with
   valid scope). Same invocation proves: `verify_retention` VERIFIED,
   public P1 still refuses (`RETENTION_DEST_CONFLICT`), only verified retained
   files added, live originals unchanged.
2. **R1-predecessor positive.** Fixture with real valid active revalidation
   chain (R1-like supersession with byte agreement, no path rebind); P2V
   observes readiness with non-null `active_revalidation_ref` equal to basis.
   Mutate to a different active record → P2V `STALE_ACTIVE`.
3. **Persistence-positive / freshness-negative.** After capture, mutate a
   mutable live COPY original: `verify_retention` still VERIFIED, P2V refuses
   (rederived graph/basis mismatch). Mutate retained COPY/KEEP/proposal/staged
   → both refuse. Proves readback ≠ eligibility.
4. **Stale State/epoch/upstream.** Mutate live State (any byte), accepted
   upstream ref, receipt, Gate, bundle, control file, or code contract
   (simulate epoch change via contract mismatch): P2V refuses with
   stale/drift code; verify may still pass (historical). Old-epoch proposal
   (different `contract_identity`) → `STALE_EPOCH`, no migration.
5. **Partial/foreign retention.** Incomplete manifest, missing COPY, extra
   file/empty dir in retained, foreign same-byte root, wrong-dest manifest,
   same-SHA wrong-path manifest → P2V + verifier refuse (no path rebinding,
   no takeover).
6. **Scope binding.** Absent block → needs-scope (not bound); wrong-before/
   wrong-after/stale-upstream/REJECT/REQUIRES_OWNER/non-PASS/substance-less
   → refuse; valid synthetic scope PASS with exact bindings → scope-bound.
   Ordinary reviews without block remain compatible (affected check only).
7. **Late-drift / no-write.** Inject control/edition/retained drift at seams:
   between retained verification and fresh rederivation, and after final
   checks. Assert refusal + pre/post equality (only injected delta differs) +
   no files written by P2V (owned trees/State/refs unchanged). Read-only, so
   “no-write before cleanup” means no writes at all (no cleanup path).
8. **Affected regressions (selected after diff).** Existing P1 strict-absence
   behavior (post-capture refusal), existing Gate/review/receipt compatibility,
   P2R historical precision — rerun only affected mechanisms, not full P1-36/
   P2R-25 suites.

Genuine semantic/visual/Human Preview, rendered-PDF acceptance, and normal
Candidate→Preview→Freeze→Release remain outside these oracles (operator/Human-
owned).

## 7. Alternatives, costs, coupling, blockers (Q7)

| Option | Budget | Cost/risk |
|---|---|---|
| **F (recommended): minimal factoring + read-only P2V** | 2A1M, 0 schema (§2.3) | Small private P1 diff (reviewable in one sitting); P2V reuses exact P1/P2R semantics with no drift; storage/test/review cost bounded (one module+test, affected regressions only). No reason/State/Gate/receipt/publisher change. |
| D (fallback duplication, 0M) | 2A0M, 0 schema | ~600-line duplicated rederivation + inventory; every future P1/P2R fix must be ported; reviewer must diff two implementations; higher long-term lifecycle work. Accept only if Astra rejects 1M refactor. |
| Full promotion now (writer + receipt/Gate/QA + reason/State + Candidate) | Unbounded (new reason literal, State pointer, writer, receipt/Gate/QA rebuild, Candidate/Preview) | Couples retention durability + admission + adoption into one unreviewable step; revalidation rows bind OLD bytes only (`control_v2.py:1844-1886`); installing changed reader without fresh chain is false completion (promotion analysis §§2–4, preserved). **Unselected.** |
| Ignore-flag / trusted-token shortcut | 0–1M | Permissive bypass of destination checks or acceptance of prior `VERIFIED`/`input_hashes` without re-observation; forges eligibility. **Forbidden.** |

**Coupling:** P2V is bounded independently of the still-open staged-review/
materialization/receipt/Gate/QA/reason/State promotion cycle. It observes
read-only readiness now; it does not select, require, or certify that cycle.
If a useful read-only boundary could not be separated safely, the correct
return would be an exact blocker (e.g., “retained Profile cannot be resolved
without trusting mutable State” or “destination policy cannot be factored
without public P1 behavior change”). No such blocker found in this analysis:
I1 chain (proposal→manifest→State COPY→retained State→Profile→KEEP→canonical
dir) is exact in current source (`verify:1827-1925`); I2 raw/snapshot/ownership
primitives exist in both P1 `_Collector` and P2R `_Session`; I3 result/error
shapes are typed; I4 budget fits 2A1M. **No blocker; factoring F recommended.**

**Artifact/receipt/code closure (no implicit migration, no commit required):**

- *Artifact:* P2V rederives live artifact bytes with current loaders
  (`load_derivation_for_readback` vs `load_derivation`) and compares to
  supplied proposal/canonical bytes; it never blesses an old captured
  production proposal (e.g., intake `afdb3df3`, a production evidence capture,
  not authority) as still eligible after live bytes moved. Same SHA at a
  different path authorizes nothing (no path rebind, P1 `:401-402` + verify
  `:1911-1925` preserved).
- *Receipt:* P2V re-runs the full route receipt validator with current code
  (review reload, contract, canonical paths, replay) plus
  `_final_full_receipt_recheck`; a receipt valid under an old epoch but
  invalid under current code refuses. Captured `generated_receipt_ref` is a
  fingerprint, not renewed authority.
- *Code:* P2V pins its own + P1/P2R module/schema bytes as inputs (like
  `capture_inputs`) and requires HEAD stability during the call, but HEAD
  remains 409 with uncommitted overlay (16 files now, 18–19 after P2V) —
  **no candidate commit required or implied.** An uncommitted overlay is not an
  instruction to commit; source-overlay identity and future fixture commits
  remain explicitly bound at promotion time (P2R contract §1). P2V does not
  certify that old captured bytes are migratable to current code; it refuses
  stale epochs.

Lifecycle-work reading: P1 paid for proposal/closure semantics, P2R paid for
persistence/ownership; P2V converts the remaining trust assumption (“verified
retained set + once-valid proposal ⇒ still eligible”) into checked evidence by
reusing both, with one small module and one private refactor. No net-savings
claim; storage/test/review cost is explicit.

## 8. Recommendation

**Recommend Astra select factoring F with the §2.3 budget (2A1M, 0 schema
deltas) and the §§1/3–6 predicates/ordering/snapshots/oracles as the P2V
contract**, preserving public P1 strictness, read-only observation-only
results, and all P1/P2R evidence qualifications. No full promotion, no new
reason/State pointer, no new Human Gate, no production-owned fixture, no
candidate commit selected. Implementation (interface/fixture return, then code
after Astra approval of concrete details) follows Human continuation; this
analysis makes no runtime acceptance claim. Whole NOT_READY, step4/B3 OPEN,
canonical audit unstarted, DM021 OPEN. Stop at Human Commit Point; ordinary
Commit/Push Human-owned, candidate commit requires explicit authorization.
