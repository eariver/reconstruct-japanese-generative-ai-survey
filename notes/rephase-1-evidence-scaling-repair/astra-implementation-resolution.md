# Astra Evidence scaling repair — implementation gate

Human continued after the rehearsal Commit/Push; no Human Commit readback. **Working gate: NOT_READY for code until the concrete delta and independent scoped review close.** This is the selected repair unit, not another broad Profile/reader design cycle.

## 1. Binding source and scope

Use final138 actual409/tree8ce/770; full DIRECT409 patch `efb505e44c1ccb3c83121db2fbaa9fec05ed900c252184765ca3b50f7b28254e` /5247647B and manifest **`634d41f9807e8cd60ca3d839245358fa5e5da312f6d1b58ae84c1619481a03dc` /186847B**. R1 map's repeated `e5` in the manifest pin is a transcription error, not another identity.

Prior rehearsal ROOT FULL INCLUDING§7 governs facts/limits. No global/epoch/dynamic-scope authority cache, public verified-dict/context flag, third mirrored validator, new runtime module/schema/family or generic reader unit. Preserve canonical10, ordinary3/5→7, true R/E, new-admission/history separation, DM0227 semantics and existing no-overwrite/readiness guards.

## 2. Root choices closing R1 ambiguities

- Select **one canonical card-construction/checking core** with public reload wrappers and internally owned batch paths. Use a lazy private source resolver where required to preserve the public validator's original error/IO order; resolving all sources before CARD_KEYS/identity/entity checks is not equivalent. Likewise preserve Discovery-source classification before supplement loading in standalone `task_authority_sources`.
- Each public operation/validation phase may independently re-derive its private context package-linearly. No context is threaded through a new public kwarg or ambient module state. Private pure slices do not grant operational authority.
- **Include the two LOW bulk builder/acceptance loops** where they invoke the same card helpers repeatedly. They are part of the already-selected correction operation on the real-sized corpus, not a new research route. Keep required public PATH arguments and COPY/true-R/E validation. Do not import the interactive runner into LOW or run LIVE validation in detached context.
- A context must describe its exact expected input bindings and lifetime. Rechecks use authoritative expected refs/loaded-byte pins, never re-seal changed bytes after validation as a new baseline. State pin handling must distinguish current checked bytes from historical logical-path-only expectations; a historical package's old State SHA must not become a new LIVE-State equality requirement.
- Recheck at **logical publication boundaries**, not once per copied task/result file (which would recreate quadratic work). Preserve partial run directories on late failure, final acceptance-record checks, read-only return freshness, and the archive/audit boundary after temporary package cleanup. Existing accepted package copies must be explicitly bound when used for a later phase; do not probe a deleted/future temporary path.
- Public writers with only a payload/path retain their existing responsibility: place additional source freshness checks at the actual checked owner with the required input paths, rather than guessing missing authority inside a generic writer. No strengthened O_EXCL/CAS/atomicity claim.

## 3. Required compact R2 return

Give concrete private signatures/return fields (including pin/recheck helpers), exact current/error branches, phase-by-phase construction/recheck/discard points, actual input paths per mode, and all normal/shared/LOW caller changes. State precisely which public wrappers retain their bodies/signatures and which delegate to a single private core. Replace vague repeated line references with module/function names. Include the final return and prepublication sites and tests for transient/late failure windows. A short table is sufficient; source citation alone is not a mechanism.

## 4. Epoch continuation choice and execution guard

Explore's read-only trace found that the normal agent-first path permits a committed script-only epoch while retaining State initialization identity and record-owned earlier checkpoints. Contract8 has no script members in its current pipeline/quality lists. This supports **testing continuation of the existing CANDIDATES_NORMALIZED states in a NEW independent copy of the preserved rehearsal**, applying only reviewed runtime/test changes and making a meaningful isolated source commit before execution. Do not mutate the old rehearsal workcopy or hand-repin State/Profile/checkpoints. Fresh reports for the new stage must use the actual new HEAD. This is a candidate/test epoch, not an ordinary shipping commit or Production write.

Important: the CAND path checks actual supplied/current SHA but does not itself prove a clean/identical executed worktree. Do not claim dirty code would be refused. New execution fixtures require independently checked intended bytes/modes, actual committed blobs and loaded module paths, pre/post checks and source separation. If actual runtime contradicts the source-read continuation trace, return the concrete failure; do not weaken validators or switch invisibly to restart.

## 5. SP retry boundary retained

Current SP Ledger/Completeness are CAND-owned canonical regeneration outputs with pending/null Evidence-stage authority and no current Human Gate. Old accepted Evidence/Views and audit must remain immutable; the audit references those singleton output paths without pinning their hashes. The ordinary runner refuses existing outputs and has no standalone disposal API. This does not automatically require a new Core feature. No cleanup is authorized yet: a concrete guarded preservation/ownership/current-reference decision is still needed before SP retry. W34 has no canonical Evidence products, so its actual409 verification can proceed without that disposal. Do not call a fresh instance proof of same-stage retry.

## 6. R2 / independent G1–G4 resolution (binding delta, awaiting confirmation)

R2 is not code-ready by itself. Resolve the four findings as follows; this overrides conflicting R2/review suggestions without rewriting them.

### G1 — expected inputs, not a hash-of-disk compared to itself

Keep the supplement context separate from the owner's phase pins. Private data shapes:

```
FilePin = (label: str, path: Path, expected_sha256: str, expected_bytes: int)
PhasePins = tuple[FilePin, ...]
SupplementContext = {
  "manifest_ref": FilePin | None,
  "entries": read-only mapping[source_id, read-only entry],
  "raw_refs": tuple[FilePin, ...],
  "basis_refs": tuple[FilePin, ...],
  "source_root": Path | None
}
```

- `_capture_phase_pins(paths: tuple[tuple[str, Path], ...]) -> PhasePins`: an internal **pre-validation** observation only, not a permission. Compute expected SHA and length from the same read. For JSON that contributes to the context, parse those same captured bytes with the existing parser/schema semantics, not a different post-validation read silently substituted as baseline.
- `_recheck_phase_pins(pins: PhasePins) -> None`: compare actual safe regular-file bytes to immutable expected values; never update/reseal the pins. Preserve existing path/no-follow rules; explicitly owned temporary package/task paths remain allowed.
- `_load_pinned_json(pin: FilePin) -> dict`: read once, require that buffer's SHA/length to equal the expected pin, then parse that same buffer with the existing JSON semantics. This is a private phase-binding helper, not a generic reader module. Reuse the existing full supplement validator; compare its returned manifest to the pinned parsed manifest before constructing cached entries (or factor its single canonical validation body to validate that same parsed value). Do not copy a second validator or trust a separately read, unbound dict.
- `_resolve_phase_supplement_context(repo_root, package, *, implementation_sha, screening_acceptance, discoveries) -> SupplementContext`: validate exact `package.authority_supplement` FILE ref, same loaded manifest bytes/schema and existing supplement predicates. `manifest_ref.expected_sha256` comes from the package's authority ref; `raw_refs` come from **every validated manifest entry's declared raw_sha256/byte_count**, not newly observed bytes. `basis_refs` use manifest-declared Discovery/Screening file hashes and the verified lengths. No `phase` string chooses authority semantics.
- `_recheck_supplement_context(repo_root, ctx) -> None`: recheck manifest/basis pins and all declared Raw refs with the existing containment/no-follow/size/hash predicates. It cannot turn a changed manifest into a new map or reload new declarations as replacement expected values.
- `_finish_authority_phase(repo_root, ctx, pins, *, revalidate_owner: Callable[[], None]) -> None`: recheck immutable phase/supplement pins, invoke the **existing role-correct owner validator**, then recheck pins again before the logical return/publication boundary. The callback is constructed inside the owner, never supplied through a public API. It must not recursively invoke the same batch finalizer; use package-basis/current or package-basis-content/history validation rather than a whole acceptance wrapper that re-enters this phase.

Owner pin construction precedes the phase's validation and first cached use. Existing authoritative refs win where available (acceptance.package SHA, task meta SHAs, Profile/accepted-input refs); compare them with the captured pins as part of that validation. Recheck the captured set immediately after validation, before accepting it for reuse. Phase paths are explicit: package and all declared tasks; relevant profile/accepted input files; current actual State for a LIVE phase. Current readback pins the checked **current** State bytes, not the old accepted package's State SHA. History phases never read/pin canonical LIVE State; logical path checks stay in their existing content validator. LOW adds the exact required retained COPY pin and keeps its request/retention predicates.

At the archive boundary, start a new phase using the exact accepted package copy/ref and input file; never retain a temporary path past its lifetime. Generic payload-only writers gain no authority-guessing behavior. Full source/runtime identity is independently guarded outside the CAND validator as §4 specifies. These checks establish explicit observation boundaries, not an atomic filesystem snapshot or every-interleaving guarantee.

### G2 — full manifest Raw closure

`raw_refs` always includes all manifest entries (428 declared refs/425 distinct paths for W34); identical duplicates may simply be checked again. It is never derived from one task's source bindings. Phase task-file pins cover the complete declared package task set separately. No optional task list suppresses Raw rechecking. `_recheck_publication_unit_pins`'s ambiguous R2 PATH-only interface is replaced by the two explicit pin/context recheck helpers and owner callback above.

### G3 — preserve the real branch/order

The original first source-resolution call is at `validate_evidence_card:1070`, **after source-array/id checks at1057–1063 and before the per-source fallback loop**, not “after1088” as the review suggested. `_validate_card_core(..., get_sources: Callable[[], dict] | None)` retains the full original early returns, supplement-without-repo-context error, source loop and exception handling. Invoke `get_sources()` at that original branch only. No-supplement validation retains its original Discovery-only structural branch.

For source-map construction, factor pure `_discovery_task_sources(task) -> dict` and `_merge_supplement_task_sources(base_sources, task, entries) -> dict`. Public `task_authority_sources` classifies Discovery first, and loads the supplement only when that task declares supplement IDs, then merges. A batch provider does the same classification for the current task before its first context access. **Do not pre-scan all future tasks' classes before the first task**: that would change original ordering. Batch context creation may be lazy at first supplemented task; no public cache or ambient handoff. The canonical builder obtains its authority map in the original position and delegates to the one shared construction core.

### G4 — absence is not a new refusal; no mutable authority escapes

An actual package without `authority_supplement` gets an internal empty context (`manifest_ref/source_root=None`, empty entries/raw_refs/basis_refs). This is legitimate existing behavior, not a requires-context error. Public non-supplement card validation never creates an IO provider. A package with supplement but an unbound task keeps the old Discovery-only task map; absence of task IDs does not change the package-level full validation responsibilities.

Context values are private immutable/copy-owned data: read-only mappings for entries, tuples for pins, per-task results copied on return; no property-triggered IO or mutable map escape to an operator/public result. Owners may recheck the same context at multiple boundaries within that phase (e.g. before copies and before final acceptance record); discard it at phase completion/exception, not after the first recheck. There is no persistent reusable authority token or runtime “verified” flag. Standalone public calls construct fresh local data each time.

### Implementation gate

Independent confirmation of this full resolution plus R2's otherwise unchanged census/oracles precedes code. Implementation may refine private names/types without changing these semantics; any missing input/owner callback or public-behavior contradiction returns before broadening. Required runtime surface is Evidence + ordinary runner + LOW bulk owners, no path budget preventing necessary same-contract wiring. No source edits or tests have occurred in this readiness step.

## 7. Astra confirmation — implement the selected whole repair

Independent map confirmation closes G1–G4 as bounded PRE_CODE_READY on §6 plus R2's corrected census/oracles. **Code is now authorized in this repair unit** under §§1–6. This supersedes the working NOT_READY heading; prior drafts/findings remain preserved. No implementation/runtime acceptance is inferred from map readiness.

General prepares a NEW independent final138-derived author workcopy, implements the selected Evidence/runner/LOW repair and meaningful affected tests, and returns actual diffs/raw outcomes. No change to the preserved rehearsal workcopy, shipping proof or frozen contracts. Standalone public reload/error semantics, historical DATA/no-LIVE behavior, required LOW paths and source/guard invariants remain binding.

After source review and affected checks, use a NEW independent copy of the preserved real rehearsal for a genuine committed script-only test epoch. Keep old State/Profile/checkpoint bytes, verify Contract8 equality rather than repinning, verify actual committed/loaded source externally, and test normal continuation through the 409-task workload. This is a meaningful isolated testing commit, not an ordinary candidate/reconstruct commit. SP owned-output disposition remains held; no cleanup is authorized by the scaling implementation gate.

Finish with source-bound CURRENT/affected verification, complete DIRECT409 delivery and author-independent implementation review, then Human Commit Point. No automatic new research/reader unit, Production action or R4 audit. Any essential map contradiction returns to Astra before expanding the repair.
