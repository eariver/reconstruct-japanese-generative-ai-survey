# DM021-P2R — bounded retention capture/readback contract

2026-10-13 JST. Astra design selection following P1, on unchanged actual409 +13file overlay. **Select a retention-only component, DM021-P2R**, with one-shot capture and independent read-only retained-set verification. Full correction promotion/reason/State-adoption architecture remains **unselected**. This document is a design, not implemented behavior or publication authority. Whole NOT_READY, step4/B3 OPEN, canonical audit unstarted, DM021 OPEN.

Source basis and initial/corrected proposals: [packet](../notes/rephase-1-dm021-promotion/README.md). Existing P1 contract07e89990 and final patch85e9d9ab remain unchanged. General's initial analysis and correction are evidence of proposals, not authority where this selection differs. Read the final independent design review and root resolution with this decision.

## 1. Why this boundary

P1 validates an exact healthy before state, proposed reader and typed retention plan. It retains no bytes. Every destructive-promotion alternative needs actual old-byte retention first. Capturing that finite set has utility without selecting a second State pointer or review-path policy. The next implementation can prove persistence and fail-closed ownership independently of the unresolved adoption cycle.

The full-promotion gaps are concrete:

- Existing controller revalidation **does support changed publication rows** (`survey_agent_control_v2.py:1844–1886`) but only its restricted `REVIEWED_CORE_CHANGE` reason. Editorial authority, typed full closure and ownership cannot be supplied by changing that enum alone.
- Initial Longform publisher is DRAFT_COMPLETE-only and refuses existing outputs; later receipt replay demands canonical reader/archive/receipt paths and strict healthy-State derivation (`survey_longform_derivation_v2.py:1101–1182`, `survey_longform_generated_v2.py:698–730`). Installing new bytes invalidates old State before the new adoption can be verified. No bounded, noncircular editorial replay context has yet been selected.
- Weekly has a checked pending-basis fallback (`survey_weekly_derivation_v2.py:481–487`) without proof that it supplies the required editorial scope/retention authority. No blanket bypass is authorized for either route.
- Keeping staged review path identity may require an explicit versioned-target relation in receipt/Gate validators. Obtaining a genuine second review on the live canonical path instead adds semantic work and an invalid-live waiting window. Neither choice is selected here; same-SHA retargeting is forbidden.
- Correct order is reader derivation/materialization, genuine pre-TeX scope/semantic review, generation, then the applicable build/manuscript/Gate/QA/post-build reviews and Candidate admissions according to their actual dependencies. A receipt consumes the pre-TeX review. Post-build semantic/editorial, VISUAL and Human Preview are separate obligations; this list is not a new certified topological scheduler.
- `build_candidate` (`survey_publication_v2.py:668–746`) consumes already-reviewed source/PDF/manuscript/bundle/reviews and writes an immutable Candidate; it does **not** itself re-enter publishers. Correction-specific provisioning and normal stage admission still need analysis. Source-overlay identity, current tools/contract closure and future fixture commits must be explicitly bound; an uncommitted overlay is not by itself an instruction to commit or a proof of impossibility.

General's proposed tiny full-writer budget and unchanged-validator bridge are withdrawn. A new second State pointer/reason is an alternative, not the chosen design. Net lifecycle savings remain unmeasured; P2R adds storage/readback/test/review work to remove a necessary missing retention guarantee. One-shot failure handling deliberately limits initial recovery complexity; its manual-intervention cost is explicit, not zero.

## 2. APIs and exact budget

Expected shipping delta relative to P1: **3 added paths**, no modifications:

1. `scripts/survey_editorial_retention_v2.py`
2. `schemas/editorial-retention-manifest-v2.schema.json`
3. `tests/test_survey_editorial_retention_v2.py`

Proposed API signatures:

```
capture_retention(root, state_path, proposal_path) -> result
verify_retention(root, proposal_path, manifest_path) -> result
```

P1's existing `validate_proposal` remains unchanged and strict. Capture calls it without a scope review; a valid `REVIEW_REQUIRED` proposal is sufficient to copy old bytes, not to promote them. No new review producer or semantic-PASS requirement is added for retention. If an already reviewed proposal is used, no review is regenerated, rebound or adopted by P2R.

No CLI, config registration, reason enum, State/controller/Gate/receipt/publisher changes, live artifact writes, new candidate commit or generic journal framework. Before code, General must return actual module imports/helper feasibility, complete schema/return/error shapes, safe filesystem algorithm and synthetic accepted-fixture plan to Astra. Any necessary change beyond3A is a blocker requiring a scope decision, not implicit authority.

## 3. Finite paths and retained-set semantics

P1 derives the proposal directory from validated Profile source_root and proposal_id:
`<source_root>/publication/v2/editorial-corrections/<proposal_id>`.

P2R exclusively claims its previously **absent** `retained/` directory. Existing directory/file/dangling alias at that root refuses capture, including an empty directory. No equality-based takeover of someone else's paths.

- COPY destinations are exactly P1's `retained_dest` values, each `<proposal_dir>/retained/before/<original_repo_relative_path>`.
- KEEP rows remain exact original immutable `retained_ref` references; they are not copied and must be present with the recorded hash and size for a successful retained-set verification.
- Completion path is exactly `<proposal_dir>/retained/retention-manifest.json`.
- The only allowed regular files below `retained/` are the COPY destinations and final manifest. Directories are exactly the ancestor closure needed for those files, including the owned root. Unexpected entries, even empty directories, aliases or special files refuse completion/readback. Implementation must account for any necessary temporary entry in the reviewed ownership protocol or avoid it; no undeclared temp writes.
- P1 proposal, staged authoring and staged proposed reader paths/bytes remain unchanged and are verified through their exact refs. Nothing is moved into a new authority path. The manifest must not infer a new review target.

This is a dependency-bearing retained set, **not** a self-contained backup. COPY can remain valid after its original live source is replaced; KEEP still depends on immutable original bytes. Captured State/checkpoint/receipt refs are historical identifiers only.

## 4. Manifest and verifier meaning

Use repository schema convention `schema_version: "2.0-rc1"`; separate discriminator `kind: "EDITORIAL_RETENTION_V1"`, `status: "CAPTURED"`. `RETENTION_MANIFEST_V1` is not a replacement schema-version convention. Schema objects reject unknown fields. Canonical serialization and digest definitions must be specified before code using existing helpers, without self-hash recursion.

Required content:

- `proposal_ref` with exact original path/SHA256, `proposal_id`, `issue_id`, research/publication Profile labels.
- `basis`: the exact complete P1 `proposal.basis` object, including State, original validation checkpoint, optional active revalidation, active reader, before_graph_digest, preserved_upstream_digest, generated receipt, renderer_commit and contract_identity. These are copied fingerprints, not new active authority.
- `proposed`: exact P1 proposed-input refs/canonical reader digest/change description, still unadopted.
- `rows`: one-to-one with P1's canonical retention_plan. Same ordered roles, original path/hash/byte_count/policy and KEEP ref or COPY destination; COPY additionally records read-back retained SHA256 and byte count, required equal to the source row. No omitted/extra/duplicate path or role, conflicting policy or identity.
- `capture_inputs`: sorted unique path/SHA256 observations returned by P1's successful public validator, augmented with explicitly enumerated P2R module/schema dependencies. At minimum this includes the supplied proposal and its staged inputs. These bind the capture's input snapshot; they are not a signature, independent approval or a full reconstruction of P1's graph edges.

`verify_retention(root, proposal_path, manifest_path)` does not call P1, does not require current live COPY originals or current State eligibility, and never modifies anything. It:

1. Performs lexical/raw safe-path checks before reading. Loads the explicitly supplied proposal and exact bound manifest bytes; validates both schemas, header/basis/proposed/row equalities and path derivations. It must derive proposal layout from the exact bound retained Profile/source-root relation, not a basename guess or blindly trusted manifest prefix. Mutable Profile is forbidden by P1's retained graph; verifier checks the required KEEP Profile bytes before using its paths.
2. Recomputes the finite expected retained inventory, COPY mappings and required immutable refs; rehashes COPY and KEEP regular files with exact byte counts. No graph traversal of arbitrary strings/URLs. Reads and rechecks staged authoring/reader refs without re-deriving editorial semantics or changing their paths.
3. Returns `RETAINED_SET_VERIFIED` only for the complete matching manifest + exact inventory + all required refs. Missing/malformed manifest or partial data is incomplete/invalid, never success. KEEP drift is failure, even when every COPY matches. Captured `capture_inputs` need not all remain live after later replacement; they are not used to claim current eligibility.
4. Rechecks all actually consumed manifest/proposal/retained/KEEP/staged file bytes and inventory before returning. No computed output that silently repairs supplied claims.

The verifier proves consistency and presence of the bytes bound to a supplied exact proposal, **not** that an independent actor witnessed capture, that P1 ran historically, that a graph is semantically complete under later code, or that current correction eligibility still holds. No cryptographic attestation or adoption authority is inferred from a self-consistent manifest. Initial capture correctness is tested through the actual P1 call and writer checks.

## 5. Capture sequence, ownership and failure

1. Safe-read the canonical proposal/State/Profile and reject an existing retained root. Run unmodified P1 public validation against real current authority. Compare supplied proposal unchanged and keep its returned input hashes. Pin actual current HEAD, P2R source/schema, relevant config/control inventory and validated source/survey tree snapshot; use checked Git operations without inherited routing. Capture raw inputs before any validator capable of rereading them and recheck afterwards.
2. Preflight the entire plan, paths, aliases/nonregular files, namespace overlaps, COPY bytes and KEEP refs. Raw-safe regular-file reads must match P1 plan hash/size. Snapshot all inputs actually consumed and finite required inventories. Never open a FIFO/device before checking type. No directories/files are written on predictable preflight failure.
3. Claim the absent retained root exclusively; record its actual identity for this invocation. Creation failure does not confer ownership. Build only required ancestor directories and COPY files under that root. Each write uses exclusive creation, exact bytes pinned from source, close-error handling and readback. Before/after writes recheck root/ancestor ownership and safety; an unexpected replacement stops, with no foreign cleanup.
4. Before publishing the manifest, recheck all P1 input hashes (including State/control/proposal/staged refs), all retained bytes/KEEP refs, actual HEAD/P2R dependencies, and the input inventories except this invocation's precisely owned new retained entries. Extra or changed input, disappearance, changed mode/type where relevant, or unowned output refuses finalization. Source/survey snapshot comparison must allow only the exact owned retention delta, not exclude the whole proposal tree.
5. Serialize the full manifest from measured bytes; publish it last with exclusive create, full write/close and readback; invoke standalone verification and final no-drift checks before reporting capture success (`RETAINED_SET_CAPTURED`). A merely existing manifest is insufficient. A partial, malformed or close-failed final artifact is preserved and reported as incomplete/indeterminate, never retroactively rewritten into success.

No rollback, recursive cleanup, truncation, overwrite, deletion-to-rerun, automatic repair or partial-resume is selected. Failure after root claim leaves owned partials and an actionable report of observed paths/status, with live original bytes untouched. A retry of `capture_retention` against any existing retained root refuses. A caller with a previously successful result may call read-only `verify_retention`; that is verification, **not** writer idempotent adoption or current-state renewal. A stale or incomplete retained tree needs a separately authorized recovery decision; P2R never directs deleting it just to make P1 pass.

Manifest completion is observational: no global CAS, no exclusion of a hostile concurrent writer, no multi-file crash atomicity, disk/replica durability or tamper-proof storage guarantee. Detectable drift at checked boundaries fails closed. A crash may leave a physically valid manifest even when no success return was delivered; readback may establish retained-set consistency but cannot invent a historical success event. No success count is inferred from file presence.

## 6. Post-capture P1 and future adoption — explicit stop

P1 `_retention_plan:1278–1282` rejects existing COPY destinations. Therefore an unchanged P1 call on this same proposal will refuse after capture. Neither automatic partial retry nor “fresh P1 validation after retention” is part of P2R. General correction.md's contrary retry/future-validation claims are superseded by this section.

A later promotion contract must explicitly solve a retained-aware **current-authority** check, binding fresh State/receipt/control/accepted upstream and proposal before identity while validating the existing exact retained set. It may refactor P1 with a narrowly verified retained-context path, or use another reviewed authority verifier. No permissive flag, trusted caller assertion, deletion of retained files or manufactured former State is authorized here. P2R readback alone cannot supply that check.

This integration debt is a known boundary, not a hidden promise that P1 composes unchanged. If before implementation the concrete P2R schema cannot preserve the identities needed by that future check without selecting full adoption, return the exact blocker to Astra. No reason/pointer or second review policy is smuggled into retention.

## 7. Required engineering evidence in the future implementation unit

Use real accepted-chain **synthetic** Longform and Weekly fixtures at exact source, as P1 did. Longform prose is primary, Weekly envelope-only; accepted Draft/upstream unchanged. No production-owned edition or new Human Gate is required to test mechanics. Genuine semantic/visual/Publication Preview acceptance remains separate.

- Positive COPY+KEEP inventory/bytes on both routes, meaningful before/proposed inequality; old originals unchanged, only the exact allowed retention files added. Include a P1 fixture after real R1 predecessor(s) to distinguish original checkpoint from active-before.
- Refuse unsafe path/ancestor alias, nonregular/FIFO (prove no read), out-of-root or overlapping destination, empty/preexisting retained root, same-byte foreign files, malformed plan/manifest, omitted/extra/duplicate rows and unexpected files/directories. No writes for preflight refusal.
- Inject source/State/control/proposal/staged/KEEP drift at meaningful pre-finalization seams; only injected and owned output changes may remain. Snapshot before any cleanup; no cleanup in the oracle.
- Inject short/write/close/readback/final-manifest faults and root identity replacement. Partial output is preserved and accurately classified, live originals unchanged, subsequent capture refuses, readback rejects incomplete/bad content. Valid-manifest readback is distinguished from a delivered success response.
- After capture, mutate a mutable live COPY original: persistence readback may still succeed while current eligibility is expressly unproved. Mutate a retained COPY, required KEEP ref, bound proposal or staged reader: readback must fail. Exact manifest at wrong proposal path must fail; same SHA is not a path rebind.
- Prove unmodified P1 rejects after successful capture; verify_retention works without bypassing P1 or creating State authority. Test ordinary P1 behavior/regressions only as affected, not a decorative full old-suite rerun.

Runner must pin exact full source delta, actual HEAD/tree/runtime/argv/env and full raw statuses; preserve failures and script versions; compare before/after without cleanup masking. Concrete test commands/counts are selected after the implementation diff, not borrowed from P1's36 or prior suites. No runtime evidence was produced in this design unit.

## 8. Next work and Human boundary

After author-independent design resolution and Human continuation, General's next unit is **P2R interface/fixture return to Astra, then only the selected retention component after approval of concrete details**. Source remains actual409+13file until that separate unit changes it. Full adoption remains design-open; no automatic P2b/P2c, source promotion, reason enum, State transition, review generation, new branch/commit or Production action.

Stop at Human Commit Point for this design unit. Ordinary reconstruct Commit/Push is Human-owned.
