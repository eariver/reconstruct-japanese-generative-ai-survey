# Re:Phase 1 — r2 application review

Work begun 2026-09-16; root closeout 2026-09-21 JST. Result: **NOT_READY; no production adoption; canonical seven-point final audit not started**.

## Read

- [Root assessment](../../outputs/rephase-1-application-assessment.md)
- [Independent preparatory review](auditor/review.md), with [independent source checks](auditor/source-checks.json)
- [Diagnostic disposition](diagnostic-disposition.md), including interrupted runs and remaining gaps
- [Proposed application scope](application-scope.md), including contract/history/cost handling

## Candidate and isolation

`prepare_candidate.py` fetched only the Human-fixed SHA into an independent, sparse Linux repository. `acquisition.log` records the fixed-SHA fetch. The full tree is preserved; sources/surveys were initially unmaterialized. The acquisition remote was removed before tests; origin is `https://example.invalid/rephase-application.git`, with no alternates or shared object database.

Original unchanged five-file r2: `46472e41e353de56685e737fc91e85fcc2005312`, recorded in `candidate.json`. Its production file hashes match the earlier r2 packet. Worker found an existing document test requiring the removed live status. Root accepted the bounded test correction in `worker/test-contract-update.patch`, preserving generic history, release, review and Human-boundary assertions.

Application **a1**, six files: `d38f023ce200619f7f49ce17a348755f05e0e021`, tree `960585ef29b55567efdf08901de489e4f3bb8fe5`, direct parent `774dd39a951c9ac3818e83dfffd4c7666efb0a20`. See `application-candidate.json`, `apply_test_contract.py`, and `application.patch`. The original r2 commit remains reachable on a separate local fixture ref. These are local review commits only; no production branch or ordinary reconstruct final commit was created.

`seal_review_packet.py` verifies the unchanged head/tree/diff/hashes, saves the raw commit object and six-file patch, checks continuity with 13 fixed-baseline witness inputs, and binds external evidence in `review-input.json`. This is an input seal, not a final-audit freeze/PASS. The isolated Auditor copy has its own database; the earlier independent review inspected the source fixture read-only. `/tmp` environments are disposable. Patch, hashes and raw commit metadata remain durable here; reproducing a candidate does not transfer approval to a new head.

Raw `git diff --check` reports one existing Markdown two-space hard break on the changed Status line. It is recorded rather than silently removed from reviewed r2. With end-of-line whitespace excluded, the diff check passes. No content mutation was made for that formatting diagnostic.

## Roles and evidence

- Root: candidate preparation, test-patch acceptance, contract impact, Python 3.12 provisioning, final diagnostics and disposition.
- Worker: fresh-context `gpt-5.6-sol`, high reasoning, CI prerequisite diagnosis and one-file test correction; usage limit stopped the Worker after patch delivery. Raw initial logs remain in `worker/`.
- Auditor: fresh-context `gpt-6-astra`, high reasoning, no authorship or candidate mutation. Chosen for the whole-candidate authority/trust reasoning; independent findings are in its own report. Earlier r2 reviewers were not reused as the application Auditor.

No role simulated Human approval. Prior bounded reviews/tests retain their old scope. The Auditor's report is an independent preparatory NOT_READY decision, not a 7/7 audit. Later targeted execution/closeout belongs to root, not to the Auditor.

`contract_impact.py` / `contract-impact.json` compute the real contract identities from 68 verified inputs: pipeline hash changes; quality/Profile hashes and version labels do not. This is not an edition migration test. The additional a1 test file is outside the aggregate and leaves all measured production inputs unchanged.

`run_diagnostics.py`, `workflow_checks.py`, `hydrate_test_assets.py`, runtime documentation and their result/log files explain execution and reproduction. Do not rerun successful checks merely for coverage or treat interrupted logs as complete CI.

## Boundary

Production remained read-only. No newer main lookup, rebaseline, PR/Issue/comment, Actions dispatch, adoption, State/approval mutation, release, ordinary reconstruct commit/Pull/Push occurred. Synthetic Git review objects/refs remained in separate fixture databases. Untracked pycache and an old interrupted-test temp directory are fixture debris, not candidate changes or authority; they were not blindly deleted.

Known Freeze artifact/type and reader-binding blockers are retained as separate baseline maintenance matters. r2 remains a proposal. Full CI, seven-point acceptance, full Profile publication/quality, historical dependency closure and net lifecycle savings remain unestablished.
