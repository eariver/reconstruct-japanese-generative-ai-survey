# DM021-P3S — reviewed staged source materialization / replay contract

2026-10-16 JST. Astra selects **P3S: post-review staged TeX/Bib/style materialization and independent staged-set replay**, not live replacement or State adoption. Design-only decision on unchanged P2V18 source. Whole NOT_READY, step4/B3 OPEN, canonical audit unstarted, DM021 OPEN. Full promotion remains unselected.

Basis: [P2V assessment](rephase-1-dm021-p2v-assessment.md) §4, contracts07e89990/194fd7de/2ea1d98f and mandatory evidence bounds. [Analysis packet](../notes/rephase-1-dm021-materialization/README.md) retains General initial/corrections and root feedback. This selection supersedes contradictory proposals; read the independent design review and mandatory Astra resolution with it. P2V closeout was committed/pushed as5595d214375f77c93fc3376799fb29b145bc5e32 by Astra under the Human's explicit one-off request; no candidate/Production commit authority follows.

## 1. Why this is the next useful boundary

P1 already derives proposed canonical reader bytes; P2R persists before bytes; P2V checks current-before authority with an existing scope review. None materializes the **corrected main.tex/references.bib/style**. Reader-JSON-only staging automation repeats existing P1 functionality and is not selected.

P3S produces an exact, independently replayable source set in a proposal-owned namespace while live publication and State remain healthy/unchanged. It supports checked source inspection/diff and supplies ordinary source files for a separately controlled disposable build. It creates no managed PDF-build workflow, manuscript, quality bundle, Gate, Candidate, Preview approval or live receipt. Build auxiliaries/PDFs must not be written inside its closed source set. Existing repository build tooling is not declared absent; its staged integration and rendered acceptance are outside this component.

A staged source set has immediate use through its own verifier and inspection, independently of later adoption. Existing P1/P2R/P2V are **coexistence checks**, not consumers of the new TeX. Coexistence means public P1 still refuses occupied retention, P2R still verifies persistence, and fresh scoped P2V still observes the current basis. No artifact-only result is a publication/adoption token.

## 2. Corrected adoption diagnosis — still open

`_collect_pending_rows` iterates validation-checkpoint `artifacts` (`survey_agent_control_v2.py:726`), not every changed file. Reader JSON absent from the seven direct rows does not automatically trigger noncanonical-row refusal. No new role, stage-config change or fourth Gate route is selected solely from that inference. Existing revalidation supports changed surface rows under restricted REVIEWED_CORE_CHANGE; that is not truthful editorial authority.

State JSON bytes unchanged does **not** imply healthy State after live artifact replacement. Revalidation calls Gate (`:1931`) → Longform receipt (`survey_reader_surface_gate_v2.py:1174`) → strict healthy-State readback (`survey_longform_generated_v2.py:698`), before the new State write. Longform has no checked-pending entry; existing Weekly fallback is not editorial permission. “Adoption first, readback later” does not close this cycle.

Full promotion must still select: versioned-reviewed-target/live-output binding; a genuinely checked editorial transition and public post-adoption readback; truthful reason/record/chain/pointer semantics; owned live replacement/failure/recovery boundaries; existing unadopted Candidate collision; and normal fresh review/Candidate/Preview/Freeze/Release admission. These are not fully specified here. A versioned pre-TeX target can avoid gratuitous duplicate semantic review, but cannot by itself eliminate the live-invalid install/adoption interval. A10-file change is not intrinsically unreviewable; current deferral follows unresolved predicates, not an arbitrary file limit.

Generic manuscript/bundle/Candidate validators accept explicit artifact paths subject to their own validation; generated Gate/receipt bindings impose additional constraints (Longform exact canonical suffix, Weekly basename/sibling plus receipt requirements). Do not conflate them, or use DIRECT_PRIMARY fallback to evade the generated correction contract. Normal post-build semantic/visual review and Human Preview remain separate from pre-TeX scope review.

## 3. Selected API / scope / exact budget

Expected **3A /0M**, including one new schema, relative to current18:

1. `scripts/survey_editorial_staged_source_v2.py`
2. `schemas/editorial-staged-source-manifest-v2.schema.json`
3. `tests/test_survey_editorial_staged_source_v2.py`

No edits to P1/P2R/P2V, existing schemas/loaders/renderers/receipt/Gate/controller/config/CLI. Future composite21paths3M18A vs409 is only planned; current18 remains unchanged. More paths require an exact blocker and scope decision.

```
materialize_staged_source(root, state_path, proposal_path,
                          retention_manifest_path, scope_review_path) -> result
verify_staged_source(root, proposal_path, staged_manifest_path) -> result
```

The writer requires actual `observe_current_authority(..., scope_review_path)` to return SCOPE_BOUND **inside its own invocation**, with returned refs matched to independently pinned input bytes. No earlier returned dict, enum, caller-verified set, alternate State or public P1-after-retention call. Optional/no-block review is insufficient for source materialization; do not manufacture one. Existing public P1 remains destination-strict.

The verifier is read-only **retained/staged artifact consistency and deterministic replay**, not current-before readiness. It does not call P2V/current State validation or require live mutable COPY originals. It does require exact immutable refs, full P2R retained-set verification, historical canonical layout and scope binding, plus the supported replay-code dependencies below. It may remain usable after live State/source changes **only if** those required immutable refs/dependencies remain intact. This is not proof that any future full-adoption architecture is already supported.

## 4. Canonical owned set and manifest

Derive proposal namespace from validated Profile/source_root + proposal_id. Own only the previously absent `<proposal_dir>/staged-source/` directory, containing exactly:

```
main.tex
references.bib
jgaisurvey.sty
staged-source-manifest.json
```

No caller output-dir override, paths into live survey_root, unknown files/empty dirs, aliases/special files, build auxiliaries or temp files in the final closed set. The proposal directory preexists and is not owned. Existing staged-source root (empty, partial, complete, same bytes, alias or foreign) refuses writer ownership; no takeover/retry/cleanup. An existing complete set can be checked with the separate verifier, without claiming this writer created it.

Manifest schema uses `schema_version: "2.0-rc1"`, `kind: "EDITORIAL_STAGED_SOURCE_V1"`, immutable completion `status: "STAGED_ONLY"`. This is a new staged source manifest, **not** an established legacy generated source receipt or Gate. Strict objects/unknown-field rejection, duplicate-key refusal, normalized canonical paths, unique fixed output roles, canonical serialization and self-digest excluding the digest field. Exact names/types/digest representation return before code.

Required bindings:

- Exact supplied `proposal_ref` and `retention_manifest_ref`; exact `scope_review_ref`; issue/research/publication labels and supported renderer route (Longform-generated or Weekly-generated only).
- Exact complete `proposal.basis` (original checkpoint/active-before/State/reader/receipt/control fingerprints) and `proposal.proposed` or an equally explicit lossless field binding, including staged authoring/reader refs and canonical reader digest. No historical before identity omitted to save bytes; descriptive text is not approval.
- Output refs for the exact3 source files (path/SHA256/byte_count), style-input ref to the actual fixed template path/bytes, explicit supported replay dependency list with path/SHA/size, and recorded producer HEAD as historical provenance. Fixed schemas/self-digests are checked, not treated as signatures.
- No full P2V input_hashes map compared to a later observation as historical truth: it includes edition snapshots and would self-include the new outputs/manifest. Invocation snapshots stay in memory; named stable refs/digests are persisted. There is no self-hash cycle through observer output.

## 5. Materialization sequence / closure / failures

1. Raw-safe narrow pins before any reopening validator: State/config/State-bound Profile, proposal, retention manifest, scope, staged reader/authoring and schemas. Establish strict current canonical roots before broad inventory using existing actual checks; do not trust unvalidated Profile roots or manifest prefixes. Record actual HEAD and current runtime/source dependencies under sanitized checked Git routing.
2. Snapshot full validated input/control/edition sets (files/dirs/types/relevant identities), including existing retention, before mutation. Call fresh P2V-with-scope and require SCOPE_BOUND; match its refs/current facts and pin every dynamically discovered consumed byte against the original expected hashes. Missing/invalid/ordinary-without-block scope, stale basis/retention/upstream, aliases/overlap/tool drift or existing output root refuses before writes. P1 public validate is not called after retention.
3. Use the already independently rederived, byte-bound proposed reader from this invocation. Reusing P1's data-only derivation or route loaders is permitted only without destination-absence acceptance, forged State/Profile or editorial use of Weekly's pending fallback. Compare canonical FILE bytes to the exact reviewed proposed-reader ref. Render via existing route `render_main`/`render_bibliography`, existing syntax/closure checks and exact fixed style-template bytes; no arbitrary raw TeX, extra authored payload or hand-edited source override.
4. Preflight all4 prospective outputs/parent relationships/schema bytes and expected data before claiming the root. Exclusively create the absent root, pin actual root/ancestor/file identities; perform exclusive dirfd/no-follow writes, exact short-write handling, close/readback checks and identity checks. Write only3 source files first. Source bytes are the originally pinned/rederived expected values, not a second reading that changes the basis.
5. Before publishing the manifest, compare all original consumed inputs/HEAD/control and edition inventories with only the exact invocation-owned delta allowed; verify all3 output bytes/sizes and closed directory set. No prefix-based exemption of the whole proposal subtree. Serialize and exclusively write the manifest LAST, close and read back exact bytes.
6. Invoke actual standalone staged-set verification, then fresh P2V SCOPE_BOUND again while live State/publication are still unchanged. Match **stable original facts**: State/proposal/retention/scope refs, before/upstream/proposed-reader digests and within-call HEAD. Newly materialized files legitimately appear in the second observation's input map; never demand full-map equality to the first observation or regard the second map as a new baseline.
7. Final original-input/control/edition/retained/staged inventories, output expected hashes/sizes and owned identities are checked after those later helpers; close every fd before returning `STAGED_SOURCE_MATERIALIZED` with exact manifest/output refs. A new self-readback session must compare against the original expected output bytes, not merely rehash freshly changed data into agreement.

Pre-write refusal leaves no files/dirs. Post-claim failure preserves owned partials and structured phase/per-file/primary+secondary close disposition, with live originals unchanged under this staged-only write set. No truncation/overwrite/automatic rollback/cleanup/partial-resume. Do not rewrite completion status to STAGED_INCOMPLETE. **A failure during manifest write/close/final checks can leave partial OR complete valid bytes**; the invocation must report incomplete/indeterminate rather than success. Later artifact verification may truthfully verify a complete matching set without attesting that prior invocation succeeded. This supersedes correction2§5's blanket “failed invocation writes no manifest/torn bytes always invalid”.

No global CAS, all-writer exclusion, crash-atomic multi-file transaction, power-loss/replica guarantee or continuous no-drift. Test checked boundaries; no promise about an injection after every final observation.

## 6. Independent staged verification — exact meaning

`verify_staged_source(root, proposal_path, staged_manifest_path)` must:

1. Safe-pin exact supplied proposal and staged manifest before schema/loader reads. Require manifest.proposal_ref path/SHA to equal the supplied proposal; derive expected retention/staged paths, not basename-only or a trusted manifest root. Call actual P2R verification on that proposal and exact bound retention manifest; compare returned SHAs to original pins. Follow verified historical `state:authority` COPY→retained State.profile→matching KEEP Profile to establish source_root/proposal_id/canonical paths, not current mutable State. Pin each typed hop and reject ambiguity/shape/identity mismatch.
2. Recheck the exact scope review path/SHA, reviewed staged reader, before-reader ref and preserved-upstream digest with existing substantive scope rules. Prefer reusing P1 `_validate_scope` through a narrowly scoped `_Session` safe-reader adapter and the **actual retained State/Profile data**; this helper uses metadata for review identity, not current State admission. It must require scope-bound success and reverify raw pins after the reopening public review loader. Do not construct P1 `_Collector` merely to satisfy an interface (it would add current HEAD/config assumptions), duplicate a weakened subset of the scope rules, or fabricate a former live State. If exact reuse is not feasible within3A, return the concrete interface blocker.
3. Validate and byte-bind the canonical proposed reader through the actual supported reader schema/canonicalizer. Re-render main/bibliography with the selected current functions and compare exact FILE bytes/hashes/sizes; staged style must equal the independently pinned style-input bytes, not a self-referential output hash only. No independent current accepted-research derivation is claimed by this artifact API; creation correctness uses actual P2V, and P2R verifies retained dependencies.
4. Enforce an **exact fixed route-specific replay dependency set**, derived by the implementation rather than chosen by manifest contents. It must include renderer/canonicalizer/reader schemas and transitive repo helpers (including tex_escape, citation/access helpers as actually used), scope/review/schema/retention validation code, this new module/schema and style input. A direct-renderer-only list is insufficient. Use existing route CURRENT_CLOSURE plus explicitly enumerated extra dependencies if appropriate; justify actual coverage at pre-code return. Require the set and current bytes to match recorded replay pins; unsupported dependency changes refuse with TOOL_DRIFT, without executing historical code. Pin schemas before parsing and recheck them after. Source-import/runtime identity must match the declared code basis, not merely another file at the same relative path.
5. Do NOT require current HEAD==producer_HEAD or current-before State validity. Artifact-only commits with unchanged replay/KEEP refs remain compatible. Later tool/schema/KEEP/path changes can refuse; version migration/full adoption compatibility is not automatically granted. No blanket equality for arbitrary historical P2R capture_inputs extras. This is dependency-bearing, not self-contained permanent backup or creator attestation.
6. Verify exact4file/ancestor closure and all refs, canonical manifest bytes/self-digest and outputs, then repeat full staged/retained inventory and original consumed-byte/identity checks after later helpers. Close with explicit error handling; no writes. Return `STAGED_SOURCE_REPLAY_VERIFIED` plus exact observed refs/digests, never current eligibility, publication admission or a future write token.

## 7. Required future evidence / pre-code stop

General must return concrete API/error/result/schema shapes, exact fixed replay dependency list and import graph, scope-adapter method contract, canonical historical-layout chain, preflight/final snapshot ordering and actual fixture/test plan BEFORE code. More than3A or a necessary change to existing P1/P2R/P2V/receipt/Gate/schema is an exact blocker, not implicit permission. Future21path3M18A component/source identity must be explicit; meaningful independently committed fixture source precedes authority. Current uncommitted review worktree is not a positive committed renderer basis or a candidate-commit instruction.

Meaningful synthetic Longform-primary/Weekly-envelope/R1 tests: real P1 prepare/stage→P2R capture→genuine-in-form synthetic scope→fresh P2V→P3S outputs +independent replay; meaningful prose/envelope edits must produce expected changed source, not copied old live files. Prove live originals/State/retention unchanged, exact4file write window, public P1 still destination-conflict and P2R/P2V coexistence, artifact-only HEAD compatibility and TOOL_DRIFT, scope/path/ref/schema/output/inventory tampering, malformed/ordinary-no-block review refusal, no-read alias/FIFO, drift before write/after helper/self-readback, root/file ownership replacement, short/zero write/fsync/close/partial manifest fault classifications, and no observer writes before any fixture repair.

Artifact API independence is tested with live mutable State/source mutation while all required KEEP/replay refs remain intact; that is not a simulated successful live adoption or bypass. Demonstrate current-before materialization would then refuse. A full valid completion left by a failed close is distinguished from a successfully returned invocation. No live Gate/DIRECT_PRIMARY workaround, PDF/quality/review PASS producer or new Human Gate. Build/rendered acceptance/all-profile/migration/performance savings remain unproved. Selected tests follow actual diff; no old13+1/25/36 transfer or decorative full-suite rerun.

## 8. Cost and next unit

Expected investment: one module/schema/test, source storage for3 outputs+manifest, deterministic replay +P2R+scope validation and two fresh P2V checks around materialization, explicit filesystem fault tests/review. This is more work than a trivial reader writer, but removes the actual post-review source-generation gap without a live-invalid window. No measured net savings or fixed test runtime/count promised. Safe shared fixture setup may reduce verification cost when equivalence is demonstrated.

After qualified independent design review and Human continuation: General's concrete P3S interface/dependency/fixture return, then selected staged materialization implementation after Astra return. Full promotion/checked transition/reason/State/Candidate architecture is still design-open; staged verification is not its admission proof. Stop at this design Human Commit Point. Ordinary reconstruct Commit/Push remains Human-owned except the already-executed explicit preceding P2V commit request; no candidate/Production action authorized.
