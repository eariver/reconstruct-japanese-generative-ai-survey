# Correction to initial materialization analysis (M1–M6)

2026-10-16 JST. General correction. Initial `analysis.md` (623 lines) and
`source-binding.md` are PRESERVED intact; nothing there is edited. This file
supersedes only the items listed in §0. Design-only, no code/tests/fixtures/
network. All line cites re-verified read-only against active
`candidate-partial-b40de60` (HEAD `409b292`, 18/18 v5 MATCH — see
`source-binding.md` §1). Summaries, not raw; cache bytes still inherited
from P2V TB1 proof. No Human Commit Point, no implementation until root
selects.

## 0. Withdrawals and citation corrections

| # | Initial claim | Correction (verified) |
|---|---|---|
| M1 | Changed live reader JSON "would hit" pending refusal `control:740`; reader JSON "must become a direct role" | **Withdrawn.** `_collect_pending_rows` def `survey_agent_control_v2.py:711`, loop `for row in record["artifacts"]` at `:726` — it iterates the validation CHECKPOINT's artifact rows only. Uniterated files never reach the kept/changed classification (`:735–740`). Consequence: absent reader JSON proves nothing either way. New editorial authority/full closure is still needed, but no direct role, no fourth Gate route, and no stage-config / seven-row / reason+role schema change is compelled. None selected here. |
| M1 | — | Preserved contracts are current selected constraints, not immutable architecture against a justified later decision. |
| M2 | Writer preflight calls public P1 `validate_proposal` after retention | **Withdrawn — impossible.** Public P1 always refuses on retained destinations (`_retention_plan` + `_require_retention_dests_absent`, `survey_editorial_correction_proposal_v2.py:1302–1306`, absence check `:1287–1301`). Corrected preflight (§2): the writer/materializer calls actual P2V `observe_current_authority(..., scope_review_path)` in its OWN invocation and requires `CURRENT_BASIS_OBSERVED_SCOPE_BOUND` (`survey_editorial_current_authority_v2.py:36–37,419–431`) — never a prior returned dict, never an ignore flag, never destination-strict public P1 on a retained proposal. |
| M2 | "Adoption→readback" resolves the healthy-State cycle; "P4 fully specified, no cycle" | **Withdrawn — circular as stated.** Measured chain: revalidation calls Gate at `control:1931` → Gate calls Longform receipt at `survey_reader_surface_gate_v2.py:1174` (Weekly `:1207`) → receipt calls healthy-State readback at `survey_longform_generated_v2.py:698` (context via `load_derivation_for_readback`) — all BEFORE the State write at `control:2042` (`_atomic_replace_state_bytes`; record create `:2031`). Postponing readback alone establishes nothing. Initial §5.3 also ordered generation/QA after adoption; correct order is install → generation/QA/reviews → revalidation (record+State) → fresh Candidate chain. The cycle is representation debt, not ordering debt (§3). |
| M3 | Versioned-target relation gives "zero invalid-live window" | **Withdrawn — false.** A versioned relation preserves the pre-TeX review path; it does not cover the interval between live replacement and State adoption. Three distinct phases: (a) staged-only healthy-live preparation (no live writes — genuinely zero window); (b) BOUNDED invalid-live install window (live bytes replaced, State not yet adopted — owned, classified, never zero); (c) ordinary post-build semantic/visual + Human Preview obligations. No review cost asserted as zero or unbounded by fiat; no extra mandatory semantic review by default. |
| M3 | Preflight "refuses existing outputs" + "originals unchanged after failure" | **Contradiction withdrawn; replaced by §2 phases.** Refusal covers (i) leftovers in the writer's OWNED namespaces (staged dir, prior attempt outputs — no overwrite-to-rerun) and (ii) live targets when basis is not fresh. Replacement of live canonical targets inside the owned install phase is the job, not a violation. After a live-write failure, originals are NOT reported "unchanged": per-file disposition (replaced-verified / replaced-unverified / untouched / unknown-unreadable), partials preserved, manual recovery. Retention-only no-write guarantees are not borrowed for the install phase. "Zero downstream changes" unproved — existing unadopted Candidate files (P1 observes at `proposal_v2.py:828–862`) get an explicit disposition in §3 (writer never touches Candidate; post-adoption chain builds fresh per existing immutable-write rules; collision behavior is a P4 proof obligation, not assumed). |
| M4 | P3 = reader-JSON-only writer (2A/0schema) as next unit | **Withdrawn as the recommendation.** P1 `prepare` already derives proposed canonical reader bytes independently and current tests stage those exact bytes (not opaque content); a reader-only helper duplicates that and does not advance post-review TeX materialization. Replaced by the post-review staged source materializer (§2). No 2A budget assumed — real module/schema/test budget in §4. |
| M6 | Weekly `validate_reader_input` at `:726`; Longform `validate_receipt` "starts :660" | **Corrected:** Weekly `validate_reader_input` def `survey_weekly_derivation_v2.py:383` (`:726` is `validate_receipt`); Longform `validate_receipt` def `survey_longform_generated_v2.py:665` (`:660` is an envelope input-drift check inside `_inspect_receipt_envelope`). All other initial cites re-checked; the table in `source-binding.md` §2 stands except these two lines. |

## 1. Corrected source/consumer matrix (explicit-path vs canonical-path audit)

The initial matrix wrongly implied all downstream validators uniformly
require live canonical paths. Measured split:

- **Accept explicit paths (object-level, no canonical-path refusal in the
  validator):** `validate_manuscript_manifest(repo_root, path, ...)`
  (`survey_reader_publication_v2.py:358` — digest + semantics, no path
  restriction); `validate_review_record` (`:544`); `validate_bundle`
  (`survey_quality_v2.py:232` — refs checked by recorded path, storage
  `REPOSITORY_FILE` rehashed `:269–272`); `validate_candidate`
  (`survey_publication_v2.py:749`); Gate `validate_reader_surface_gate`
  takes an explicit Gate path (`survey_reader_surface_gate_v2.py:1794`)
  BUT step 9 always replays full current derivation via
  `_derivation_for_manuscript` (`:1832`), which enforces the canonical
  `publication/v2/reader-surface-input-v2.json` suffix (`:1162–1169`,
  `:1201–1203`) and receipt-next-to-surface (`:1173`, `:1206`).
- **Require canonical live paths + committed tools:** both receipt
  validators (Longform `:665–758`, Weekly `:726–773`), both tool-basis
  pins (Longform `:519–582`, Weekly `:577–631`), Gate derivation binding
  above. P1 itself exercises this whole chain read-only in its final
  recheck (`proposal_v2.py:1430`, `:1880`) — healthy pre-install, which is
  exactly why the chain bites only post-install (§3).
- **No PDF-build entry exists:** only closed-inventory
  `validate_survey_build_directory` (Weekly `:100`, Longform `:168`).
  Therefore staged TeX has NO build-into-PDF consumer today; claiming
  "build input" means byte input to inspection/replay, never a PDF or
  approval claim.

Real present consumers of post-review staged TeX (§2 outputs): (a) the
materializer's own replay oracle (same FILE-byte oracle as receipt
`:741–742`, scoped to versioned paths — genuine, internal); (b) checked
operator inspection/diff of staged source; (c) co-existence oracles —
P1 validate still bound + P2R verify still VERIFIED after staging (the
existing validators consume the proposal, not the TeX, and must be proven
unperturbed). NOT P1/P2R/P2V as TeX consumers. NOT manuscript/bundle/
Candidate/Gate as staged consumers (their staged use would be the
dead-end receipt M5 forbids — no staged receipt/Gate/manuscript objects
are emitted).

## 2. Post-review staged source materializer (candidate boundary, not selected)

**Entry:** existing scope-bound authority only — proposal + staged reader +
retention manifest + scope review, with actual P2V consumed FRESH inside
the materializer's own call (M2-corrected preflight). No new role/Gate,
no production fixture (synthetic accepted-chain Longform/Weekly/R1 as in
P1/P2R/P2V).

**Namespace (disjoint, canonical, proposal-owned):**
`<proposal_dir>/staged-source/` holding `main.tex`, `references.bib`,
`jgaisurvey.sty` (copied bytes), `staged-source-manifest.json`. Disjointness
basis (observed, oracle-obligated not proved): P2R retained inventory is
scoped to `<proposal_dir>/retained` (`survey_editorial_retention_v2.py:
1927–1952` — siblings invisible to it); P2R staged refs are checked at
exact canonical names (`:1964–1969`); P1 layout pins expected files without
enumerating proposal-dir siblings. P3 tests must PROVE non-disturbance
(P1-bound + P2R-VERIFIED after staging); any enumeration refusal found in
implementation is a blocker, not a patch license.

**Two explicitly distinct APIs (M5 decision — not one conflated API):**

- `materialize_staged_source(root, state_path, proposal_path,
  manifest_path, scope_review_path)` — **current-before readiness.**
  State machine: (1) PIN raw-safe narrow inputs (State/Profile/config/
  proposal/manifest/scope/staged authoring+reader) + sanitized HEAD;
  alias/traversal/nonregular refusal. (2) FRESH AUTHORITY: call actual
  P2V with scope in-call → require SCOPE_BOUND; compare returned
  path/sha refs to pins (P2V already embeds P2R retained verification —
  no separate call needed). (3) DERIVE without live writes: re-derive
  proposed surface from staged authoring via the actual route loader
  (Weekly strict form — pending fallback at `:481–487` FORBIDDEN;
  Longform readback-shaped); require FILE bytes == staged proposed
  reader (P1's `:1865–1867` oracle reused, not duplicated); require
  proposed ≠ active reader (same-byte → explicit no-correction refusal,
  never R1 routing). (4) PREFLIGHT owned namespace: `staged-source/`
  fully absent — any existing file/dir/alias refuses (no
  overwrite-to-rerun, no cleanup); recheck P2V pins (drift between P2V
  return and write refuses). (5) WRITE owned set ONLY (four files above,
  manifest LAST — record-last, P2R §5 pattern): exclusive creates,
  close-error handling, per-file readback. (6) REPLAY: re-render from
  pinned staged reader, byte-compare all three outputs; manifest
  self-digest; final pin reverify (new files match expected bytes).
  Result `STAGED_MATERIALIZED` + stable refs (§3 manifest rule).
- `verify_staged_source(root, staged_manifest_path)` —
  **artifact-integrity-only, authority-free.** Rehash staged files +
  manifest; re-render from the STAGED reader (never live inputs); byte
  equality; manifest digest. NO State/Profile/HEAD/P2V-map calls; valid
  before AND after live adoption (historical staged set stays verifiable).
  Result `STAGED_SOURCE_VERIFIED`. Never compares against a fresh P2V
  `input_hashes` map (self-inclusion trap — §3).

**Failure/ownership/close/record/retry (exact):** pre-write refusal →
prove owned namespace + live tree untouched (snapshot compare), no files
created. Mid-write failure → preserve owned partials with per-file
classification (written-verified / written-unverified / not-attempted);
live originals proven unchanged; manifest absent or explicitly
`STAGED_INCOMPLETE` — never retrofitted to success (P2R §5.5 pattern).
Close fault on any file → INCOMPLETE, cause pinned. Retry against any
existing `staged-source/` entry refuses; stale/incomplete staged trees
need a separately authorized recovery decision (never delete-to-rerun).
No global CAS/crash-atomicity/hostile-writer exclusion beyond
close+readback. Build aux/cleanup: renderers emit no aux files (pure
string→bytes, Weekly `:400`/`:445`, Longform `:293`/`:468`); style is a
verbatim copy of `(root / STYLE_PATH)` bytes; no PDF, no manuscript, no
QA objects — boundaries explicit, no rendering/approval acceptance
implied.

## 3. Readback semantics, manifest bindings, and the precise adoption debt

**Manifest content (new small schema required — §4 budget, not 0-schema):**
`kind: STAGED_CORRECTION_SOURCE_V1`, `status: STAGED_ONLY`
(`STAGED_INCOMPLETE` on failure); `proposal_ref`, `staged_reader_ref`,
`scope_review_ref`, `authoring_input_ref` (path+sha256+size each);
`before_graph_digest` + `preserved_upstream_digest` (historical
fingerprints copied from the scope-bound P2V `measured`, never authority);
`tool_basis` = closure rows (name+sha, CURRENT_CLOSURE shape) +
`contract_identity` + `producer_HEAD` (informational: which committed
tools produced the bytes); `renderer_refs` (module path+sha for the two
renderer modules used); `rendered_refs` (three output path+sha+size);
`accepted_refs` (name+path+sha list as bound at materialization).
**Traps closed:** (i) NO full P2V `input_hashes` map inside the manifest —
after emitting outputs, requiring equality to a fresh observer map would
self-include the manifest (M5); store named stable refs + digests only,
future calls re-pin fresh. (ii) `producer_HEAD` is provenance, not
validity: a later artifact-only HEAD never invalidates staged artifacts;
only adoption-time tool predicates (`verify_tool_basis` analogues at
adoption) judge tools. (iii) Manifest digest covers all fields except
itself (no self-hash recursion). Proposed-reader/scope path+SHA,
before/active/proposed identities, actual old-byte retention (P2R), and
no generated PASS are preserved exactly.

**How future adoption consumes staged bytes without circularity — and
where it stops (the precise debt).** Under copy-canonical promotion the
writer installs proposal authoring + reader + regenerated outputs at live
canonical paths WITHOUT touching the State file; old-State equality holds
where live validators require it (State bytes unchanged until the
revalidation write), nothing manufactured, no pending token. The live
chain then runs on new bytes — and the FIRST check that cannot pass on
existing representation is review binding: receipts bind a persisted
semantic review whose target is the STAGED path (scope review after-binding,
P1 `:1786–1835`), while Gate derivation (`:1174`/`:1207`) demands the
review target the LIVE canonical path with a live receipt beside it.
Same SHA never rebinds (triple rule preserved). So the unsolved item is
exactly: **staged-scope-review → live-receipt/Gate admission
representation.** Two honest alternatives, NEITHER selected here (no
premature reason/pointer choice, M1): (C) copy-canonical + versioned
review-carry relation (bounded receipt/Gate binding parameters; loaders,
State schema, role set untouched; per-correction cost = one genuine
pre-TeX scope review, already existing duty); (V) versioned-active
authority refs (State/Profile-anchored proposal pointer readable by
loaders/receipt/State checks — touches loaders + State schema + every
authority resolver, permanent fork, for a one-shot-per-correction event).
The install→adoption window itself is NOT the gap: it is bounded by the
existing pending-basis → revalidation mechanism
(`_collect_pending_rows` `:711–743` classifies live-changed checkpoint
roles; revalidation `:1773–2042` with owner-aware rollback `:2047–2088`
closes it). Full end-to-end (integrated writer) is preferred ONLY if a
proposal actually closes the review-binding representation, not by
naming the phases; otherwise the staged component above stands alone as
the coherent useful next step with the debt below marked, not reflexively
micro-incremented.

## 4. Budget, oracles, blockers

**Budget: 3A / 0M** (any modification to P1/P2R/P2V, loaders, or live
validators is a blocker back to Astra): A builder module (two APIs +
staged-manifest writer), A `staged-source-manifest` schema (strict keys,
unknown-field rejection, `2.0-rc1` convention per P2R §4), A test module
(~10–14 methods, P2V-class runtime, no number promised pre-diff).

**Oracle plan (synthetic accepted-chain only — Longform prose primary,
Weekly envelope-only, real R1-predecessor active-before distinction; never
genuine approvals):** staged determinism (rebuild → same bytes);
canonical-FILE-byte equality incl. noncanonical-serialization refusal;
immutable-body/upstream negatives; namespace coexistence (P1 still bound,
P2R still VERIFIED after staging); existing-staged-namespace refusal;
P2V-drift-between-authority-and-write refusal; alias/FIFO/traversal;
close-fault INCOMPLETE classification with preserved partials;
manifest-tamper refusal; `verify_staged_source` independence (passes with
live tree mutated/adopted); HEAD-advance (artifact-only commit) does not
invalidate staged verification. No old-suite transfer, no decorative
rerun; saved-patch proof pattern reused.

**Blockers:** none for the staged component beyond implementation-found
enumeration refusals (returned exact, not patched). Before ANY promotion
implementation: Astra must select the review-binding representation (C vs
V above); selecting the reason class / State pointer shape is part of
THAT decision, not this one.
