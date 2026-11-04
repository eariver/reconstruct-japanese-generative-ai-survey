# Astra first implementation review — CHANGES_REQUIRED

Read actual three-file implementation and all606 lines of initial scaling tests at workcopy `evidence-scaling-implementation-20261103T114312Z/candidate-work`. Initial author five-green tests are not sufficient coverage. No real409 run is authorized until these source/oracle findings are corrected and reviewed.

## Runtime findings

1. **Pins are captured after reads/validation.** `accept_evidence_results` loads/validates the package at1471–1472 but pins at1496; historical acceptance likewise pins after parsing/validating at1676. Several readback paths recheck observations rather than the bytes actually validated. A persistent mutation planted after validation but before capture can be resealed; callbacks using the cached old `package` dict do not fix this. Capture first, parse pinned bytes, validate that same data, bind declared package/task/ref SHAs, and recheck before first reuse. Preserve existing accepted-State drift semantics without using old package State SHA as current-state equality.
2. **Dummy guarded context bypass.** `_check_evidence_acceptance_results_content:1628–1635` loads real supplement entries but sets `manifest_ref=None`, `raw_refs=()`, `basis_refs=()`. `_recheck_supplement_context` then returns immediately. A supplement cannot be represented as a no-supplement context, even in a private compatibility wrapper. Use the real DATA-mode constructor with full declared closure.
3. **Missing phase completion/final boundaries.** Runner creates `_run_ctx` then sets it toNone without a recheck; its new current Screening validation is outside the agent facade. Ledger/Completeness writes have no new full-source finalizer; archive only pins three files without Raw/owner validation. LOW bulk paths have context creation but no `_finish`/pin rechecks. Historical readback lacks role-correct final owner validation and complete input pins. Complete the selected return/write map; no per-task full Raw reload and no LIVE validation in history.
4. Preserve no-follow at rechecks, including manifest/basis ancestors as required by existing repository-file rules. Leaf `is_symlink()` alone is not equivalent to `_repo_file`'s ancestor checks. Avoid an unused `by_id` plus a nested full-Raw search per entry in `_recheck_supplement_context`; the required closure is package-linear, with identical duplicate refs permitted.

## Test draft findings — preserve and replace misleading claims

- The “public-vs-private cards” test invokes the same `_build_card_core` twice and checks a few fields; no independent old body/full golden comparison and no successful full-card validation. It modifies a loaded task without updating its stored hash.
- The scaling counter tests only manual helper use, not actual public acceptance/readback wiring.
- “Late drift” is helper-only or plants before public acceptance entry; it does not exercise cached-use→final-boundary refusal. The canonical inventory is filenames only. No actual post-Evidence-accept/Views-failure case is present.
- “Standalone no-reuse” does not perform the claimed second public call after a change.
- “DIRECT/DERIVED/history/LOW” constructs no DERIVED graph, no successful LOW bulk operation, uses a nonexistent request with broad Exception, and source-string import assertions. Those do not prove the names advertised.

Archive the exact initial test/source snapshots and raw failures; reassign tests with genuine fixtures/public operations. Useful pure helper probes may remain labelled as such. Meaningful required positives must pass full validators before negatives, and injected failures must reach their intended predicate with immediate SHA/mode/dir inventories. Test-only success stubs/authority mocks/false coverage must not replace runtime evidence.

## Independent early-review disposition

- Readback task/result freshness (finding5) is material: pin every declared task/result to the authoritative meta/acceptance SHA before checks and recheck before return. Checking a file before parsing it does not establish the final-return boundary.
- Reapply existing ancestor/no-follow rules at cached rechecks (finding3), while preserving legitimate external owned staging paths. Do not mechanically feed external temp paths to repo-only `_repo_file` or turn this into an unrelated path-policy rewrite.
- Finding4 is **not an established digest mismatch**: LOW computes SHA256 of `core.json_bytes(ev_acceptance)`, and HIGH writes those exact serialized bytes at `survey_prearchitecture_acceptance_v2.py:699` (then validates at716). That is a planned FILE hash, not `core.sha256_object`/SELF digest. Do not try to read a future acceptance file inside a pure pre-write builder. Verify the serialization equality with an actual write/readback witness; change only if an actual different-byte producer is found.
- Inherited dead code and LOW metadata lookup complexity (findings1/2) are not the measured Raw-I/O blocker. One canonical-body requirement still applies; remove/factor only what the selected change needs. Do not make unrelated cleanup a new gate, and do not replace first-match behavior with last-wins indexing for ambiguous records without checking existing validation guarantees.
- New test scope must include a genuine supplemented LOW bulk path where supported. A no-supplement HIGH fixture plus a private source-slice probe does not demonstrate that path. Inspect actual package construction: if HIGH does not carry supplements, record that pre-existing producer limitation rather than adding a new capability during this repair. A valid direct LOW package-path case can verify the selected lower API without pretending HIGH creates it.

## Actual409 attempt — escaped current-stage facade

New independent real-rehearsal copy at `evidence-scaling-w34-verification-20261103T170921Z/candidate-work` committed genuine three-runtime-file epoch `bd80d603…` over48082356, with old State/Profile/checkpoints unchanged and Contract8 unchanged. Its normal run stopped exit2 after17.56s at runner's new phase-finalizer callback: bare legacy `core.verify_state_basis` compared historical initialization48082356 with currentbd80d60. No canonical outputs; old rehearsal preserved.

This does **not** disprove supported agent-first epoch continuation. The newly added callback ran outside `current_stage_basis_override`; correct its execution scope, not State/Profile/contract fields and not the validator. Census all new runner preaccept/ledger/completeness/archive current-owner callbacks for the same escaped-facade mistake. Do not put agent-first overrides into historical Evidence/LOW content validators or broaden public standalone semantics.

Add a small meaningful HEAD-advance/old-initialization regression through the real public runner. An honestly labelled artifact-only HEAD-advance control is adequate for this specific comparison predicate; it is not the proof of a genuine runtime-repair epoch. The actual409 source-delta run provides that latter proof after the fix. Preserve the failed run and its genuine `/proc`/time/raw/source records; no duplicate launch or repin/restart to hide it.
