# Re:Phase 1 Increment A — Astra review

2026-09-22 JST (continuation recorded at 2026-09-21T16:48:03Z). **Increment A complete within its bounded scope: Astra review, independent implementation review and independent evidence-resolution supplement support the exact candidate.** This is not Human adoption or whole-B3/application acceptance.

## Authorized scope and starting identity

Human requested continuation from the current workspace entry. Reconstruct was clean at `369c95499b0d1068e6909c33c68278fb05a9a115`. The implementation plan selects Increment A only for the first Co-Worker task. Fresh Sol Co-Worker `increment_a_sol` owns implementation, fixture preparation and test execution; Astra owns scope decisions and review.

Fixed production baseline remains `774dd39a951c9ac3818e83dfffd4c7666efb0a20`. Starting f1 is `bf32edf98ba8f605169d7188bbc764de74ee4f6e`, tree `ebd351479ec222a08b8ea67ae4aae64ad0eb927e`, parent a1 `d38f023ce200619f7f49ce17a348755f05e0e021`. No production mutation, main refresh, adoption, or reconstruct commit/Pull/Push is authorized by this continuation.

## Inventory decision

Fixed source inspection confirms that both `DRAFT_COMPLETE` and `VALIDATED_DRAFT` already select a manuscript but supply only issue/Profile to `validate_reader_surface_gate`. The validator checks scanned bytes and the presence of a primary source without checking the selected manifest relationship. Tests must isolate that admission defect using valid alternative manuscripts for the same issue/Profile, rather than malformed documents or setup errors.

Sol's proposed three-module runtime scope is accepted: `survey_reader_surface_gate_v2.py`, `survey_stage_validation_v2.py`, and `survey_agent_control_v2.py`. The publication wrapper already produces a Gate from a selected manuscript and needs no new argument. Publication revalidation separately establishes authority without reading back the Gate: it should validate the Gate from existing superseded/preserved artifact rows against its selected manuscript before writing authority. No duplicate ledger or schema change is selected. Later stage validation must retain exact admission after active revalidation. Resolver byte checks and stage semantic admission must be described separately in the evidence.

Standalone Gate inspection may inspect its own unique manifest; neither active stage may use that fallback. Manifest and primary uniqueness, paths, hashes, schema/issue/Profile, disk bytes and existing semantic-review checks remain necessary. Reader-input completeness, derivation, supporting semantics and full profile integration remain outside A.

## Review required before an A completion claim

- Verify independent Git database, inert origin, exact parent/tree/file hashes and preservation of f1; distinguish setup failures from defect witnesses.
- Read all runtime/test changes and check that positives traverse real authority validators and negatives reach the intended admission boundary.
- Review raw parent failures and exact successor results, including counts, skips, failures, fixture corrections and untested boundaries.
- Bind conclusions to the final exact candidate; obtain a fresh independent scoped implementation review before transferring any review claim to that candidate.

## Interrupted Worker and continuation

The first Sol stopped at a reported usage limit after creating uncommitted runtime changes in the three agreed modules in `/tmp/jgas-rephase-increment-a-sol-copy`. Root read this partial diff; its structure matched the accepted scope, but no final test result or candidate packet was available. Root requested a docstring correction so existing semantic-review checks are not described as proof of the later derivation boundary. This is preliminary author-side review only.

Human explicitly requested continuation. Fresh replacement Sol `increment_a_sol_resume` is assigned to inspect/preserve the partial work, complete tests and package the exact candidate. Astra did not take over implementation or test execution. The initial `git clone --no-local` missing-promisor-object setup failure and subsequent independently copied object files must remain distinguishable from test results.

## Exact candidate and Astra evidence review

Sol fixed candidate `1a9649129d1745fed0b98db46ef15f014407e6fc`, tree `5e933aa54034ed227216252a2c8707a59f293acf`, with f1 as its direct parent. [Candidate manifest](../notes/rephase-1-increment-a/candidate.json), [delta patch](../notes/rephase-1-increment-a/increment-a.patch), and [full application patch](../notes/rephase-1-increment-a/application.patch) identify the candidate. The delta contains three runtime modules and one dedicated test module; it changes no schema or approval producer. Reconstruct's ordinary final commit remains Human-owned.

Astra read the complete runtime delta, all dedicated test methods and helpers, relevant fixed-source caller/manifest paths, and the packet's raw final runs, parent witnesses and isolation/failure records. The two stage callers supply their selected `manuscript_path`; publication revalidation resolves unique existing artifact rows and checks Gate admission before writing new authority. The validator compares one manifest's exact path/hash with the selected file, schema-loads it, checks issue/Profile, and compares one primary path/hash with that manifest. Existing on-disk hash/byte-count and semantic-review checks remain. Standalone self-bound inspection does not replace the stage-selected reference.

The [dedicated exact-head run](../notes/rephase-1-increment-a/dedicated-unittest.log) passed 11 test methods, including six missing/duplicate/conflicting manifest/primary subcases. The [affected existing run](../notes/rephase-1-increment-a/affected-regression.log) passed 61 tests across Reader-Surface Gate, publication revalidation and Freeze boundary modules. Both exited 0; no failures/errors/skips were reported. These are targeted results, not full CI.

The [separate f1 witnesses](../notes/rephase-1-increment-a/parent-witness.log) ran four selected rejection tests against actual parent modules. All failed because the expected exception was not raised: DRAFT_COMPLETE, inherited VALIDATED_DRAFT, revalidation establishment and active-revalidation later stage admission accepted the wrong manuscript's Gate. These were not unknown-keyword, schema or setup failures. Successor positives traverse the real `validate_stage` entry; negatives use valid same-issue/Profile alternate manuscripts, refreshed Gate digests and, for active readback, refreshed revalidation row/State hashes. The successor no-write test also checks unchanged State bytes and no new revalidation file on rejection.

The [isolation record](../notes/rephase-1-increment-a/isolation.log) supports independent candidate and parent databases, inert origins, no alternates/inherited Git environment/multiply linked objects, clean tracked candidate bytes, and unchanged f1 identity/eight hashes. [Failure history](../notes/rephase-1-increment-a/failure-history.md) separately retains clone setup failure, the initial swapped-primary fixture-construction error, preliminary working-tree runs and a diagnostic quoting error. The fixture correction did not weaken runtime validation. Initial raw evidence availability is narrower than the final full test transcripts; subsequent green runs do not erase that history.

The full application patch's saved hash matches its exact Git diff, and the f1 delta passed its apply check. A later temporary-index full-patch check emitted a missing unrelated historical promisor-object diagnostic despite exit 0; [that output](../notes/rephase-1-increment-a/application-patch-check.log) is not a clean full-application proof. No hydration/current-main recovery or broader test run was added to hide that limitation.

The fresh [independent bounded implementation review](../notes/rephase-1-increment-a/independent-review.md) saved a PASS for this exact candidate with no actionable implementation finding. Its author subsequently hit a usage limit. Fresh Sol `increment_a_evidence_resolution` separately verified the later evidence-only clarifications in an [independent supplement](../notes/rephase-1-increment-a/evidence-resolution-review.md): actual parent exit code, saved isolation command body, explicit initial-run excerpt limit, subtest counts and full-patch diagnostic. It found no material discrepancy or reason to change the bounded PASS, and independently checked exact candidate/file/patch identities. The original Auditor report remains intact; the supplement supersedes only its now-stale statement that the isolation command body was absent. Runtime/test bytes and candidate identity have not changed.

The supplement also identifies the packet-verification log's size listing as a pre-clarification inventory, not a final packet manifest. Preserve that historical output and its qualification; candidate-file/patch hash checks remain valid. No code change or repeated test run is required for this bookkeeping limitation.

## Limits and next boundary

Astra judges the exact-manuscript admission repair supported within Increment A. Active revalidation resolution remains a byte/record-authority check; the adversarial test deliberately shows that a consistently refreshed record can resolve, then fails at the independently enforced stage semantic admission. No claim of a comprehensive revalidation redesign follows.

The reused fixture has schema-valid Reader Manuscripts but uses the known invalid reader-input field `final_summary` in place of `final_summary_paragraphs`. It is not complete publisher-valid input. Synthetic research/editorial/visual/Human records, fixture PDF and low-level authority are not real Human Gate/publication evidence. Complete reader-input schema/meaning, deterministic derivation, supporting semantics, direct-primary support closure, Special/Retrospective routes, Windows, Actions, historical closure and application prerequisites remain unproven. f1's earlier acceptance is not automatically transferred to this successor.

Next is Increment B's concrete contract table, before any B code: actual bibliography values, renderer/style/helper paths, unsupported include behavior, provenance split and existing authorities. Keep DM-001/003/004 as separate later dispositions. This continuation has added a bounded admission check and targeted evidence; net lifecycle saving is unknown and is not inferred from artifact/test counts.

B3 remains OPEN, whole candidate NOT_READY, and canonical seven-point audit not started. Fresh Sol `increment_b_contract` completed the required read-only [B contract table](../notes/rephase-1-increment-b/contract-analysis.md). Astra selected the concrete contract and defined the implementation task in [the B decision](rephase-1-increment-b-contract-decision.md). B was not dispatched at this A closeout; its later execution status is recorded in [the B assessment](rephase-1-increment-b-assessment.md). This closes A implementation/review and the following B contract-analysis unit without promoting either into whole-candidate readiness.
