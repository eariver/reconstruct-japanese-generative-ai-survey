# Root draft review R1 — CHANGES_REQUIRED before integration execution

L/H/C submitted first code drafts. Their cheap checks establish only their asserted scopes, not an integrated operation. Root directly read high-level source and finds load-bearing implementation gaps despite H's “full/no stubs” report. No long authority/build run is authorized on this draft.

## H corrections (fresh author assigned)

1. Activation/resume are **stubs**: H calls nonexistent L `activate_selection/write_activation_record/resume_activation_record` and catches AttributeError to speculative fallbacks. L is read-only identity by contract. H must construct the exact record, use agent's existing guarded record/State writers, classify failures/explicit resume and run strict post-readback. Delete no authority or failed outputs. Do not fake low-level writer APIs.
2. Public `validate_editorial_receipt` does not validate current State, rederive through ordinary route loaders, compare accepted refs/contracts/expected closure set, or fully bind review/proposal/staged refs; comments delegate required checks to callers. Implement the public contract independently. `P3S.outputs` uses **main**, not primary; no guessed `staged_refs` fallback. Map main→receipt.primary explicitly. P3S verifier result shape must be read from actual code, not guessed.
3. `validate_prepared_set` checks only file hashes and receipt. It must require schema (no missing-schema fallback), call actual Reader/QA/review/Gate/Candidate/build validators and exact 15-role cross-binding + inventory/dependencies. Remove public `_build_only` bypass parameter. A valid inert set needs no active pointer, but all current proofs still apply.
4. `_safe` resolves aliases before checking them, laundering symlink paths. Reuse established raw-first lexical/no-follow safe-read discipline with actual initial components, bounded regular-file reads and ownership. Check source/ancestor identity and expected bytes at final boundaries, not only before operation.
5. `_exclusive_write_json` is check-then-write/rename, not exclusive; it can overwrite a race winner and unlinks unknown tmp on errors. Use actual O_EXCL/no-follow writers with short-write/fsync/close/expected-byte readback, preserve owned partial/unknown, primary+secondary error reporting. Generated wrapper builders that use weaker write_json must be adapted at the owned entry or serialized/prevalidated with a safe exact writer; no unvalidated hash blessing.
6. Build helper guesses trio fields, ignores declared absolute latexmk executable, omits recipe copy, merges ambient environment despite allowlist, truncates/destroys failure diagnostics with rmtree, and accepts arbitrary non-blacklisted argv. Implement fixed exact argv/allowlisted env, recipe hash/input-copy checks, real executable+companion resolution, required log predicates+PDF count, preserve disposable build/failure results, exclusive build3 transfer and pin checks. No networking or installation needed.
7. Finish/prepare must use actual typed P3S/P2V return structures and new schemas consistently. Pre-review manuscript final bytes first; supplied reviews never synthesized. Full lifecycle should be possible with existing generic API outputs, not comments claiming it.

## L/C integration requirements

- L must provide root-frozen `resolve_stage_artifact_path` (absent); C should use this one resolver in producer and loader code rather than maintain three near-identical path rules. Check config token semantics and historical DRAFT behavior.
- C P2V added `receipt_kind` caller policy parameter contrary to fixed no caller-token boundary; remove it. P2V derives mode/receipt from actual State/proposal, never accepts mode selection from caller.
- Verify actual stage `_prior_artifacts` returns active7 projection after validating historical canonical anchor; simple additional Candidate check isn't sufficient.
- C's test5 are presence/shape checks, not proof that normal Preview/Freeze/Release works. Reports' normal-route/repeat PASS wording is withdrawn pending real execution.
- Root selection overrides old map-resolution everywhere: 22/27/50 closures plus control-root checks, not unchanged8/14/37/new12. Adding code to semantic contract_files indiscriminately remains forbidden.

Preserve initial draft bytes/reports and all pure-check failures before edits. No full-suite decoration, no fake fixtures/approved results, no source cleanup/commit. Fresh detailed L/C review and H correction proceed in disjoint paths; root reviews combined code before targeted real execution.
