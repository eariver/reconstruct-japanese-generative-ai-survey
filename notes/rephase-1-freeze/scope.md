# B1/B2 bounded Freeze repair

2026-09-21 JST. Human accepted the prior NOT_READY disposition and instructed continuation. This unit repairs its two connected Freeze prerequisites in an isolated candidate. Production stays read-only; fixed production baseline remains `774dd39a951c9ac3818e83dfffd4c7666efb0a20`.

## Boundary and implementation

Start from application a1 `d38f023ce200619f7f49ce17a348755f05e0e021`. Preserve a1 and all prior reports. A separate repository at `/tmp/jgas-rephase-freeze-b1b2` owns its own Git database, no alternates, inert origin; `prepare.py` records the copy. The five r2 production files and one a1 test correction remain unchanged.

- B1: use the existing three-artifact Freeze checkpoint schema: `freeze-record`, `release-manifest`, `visual-review-record`. The third artifact is the already-reviewed **Candidate pre-preview VISUAL record**, with exact Candidate path/hash equality. It is not a new post-approval review or legacy Visual Review gate.
- B2: the named Publication Preview checkpoint slot is a typed approval, also referenced by Human Gate provenance. Resolve it through its own existing validator only after approved/passed status, equality of both references, configured canonical path, exact bytes and Profile identity checks. Seed its approved Candidate into the normal artifact map so an inconsistent prior checkpoint cannot substitute another Candidate. Other checkpoint records continue through Stage Checkpoint schema/hash checks. No generic unknown-record skip.
- Retain active publication revalidation and its supersession rules from fixed #495/#496. Do not change schema, approval producer, Gate count, reviewed-commit checks, State initialization history or current-implementation checkpoint binding.

Historical `notes/phase-5-runtime-repair/` is relevant fixture/design evidence only. Its old patch also modified Release handling and predates the fixed baseline. Do not transplant it. This repair adds no FROZEN local stage, release producer patch, new resolver, workflow or migration. B3 reader coverage/derivation remains unresolved and outside this unit.

## Roles and verification

Root owns runtime changes and candidate integration. A fresh-context Sol Worker owns a new regression test module and its fixture adaptation, not runtime design or independent audit. A separate fresh-context Auditor will inspect the completed exact candidate and targeted results; neither the earlier readiness report nor Worker tests substitute for that review.

Verify real stage validation, report creation, checkpoint construction/advance and retained fail-close conditions on explicit synthetic publication fixtures. Earlier research, semantic/visual judgments and Human decisions in those fixtures are not actual publication/approval evidence. If tests use the real low-level approval producer, disclose that this does not independently exercise the canonical durable-reviewed-commit Human Gate protocol. Existing Git checks must not be mocked or weakened.

Use targeted affected tests and a before/after witness, not a repeat of the interrupted broad a1 suite. Preserve setup failures and avoid duplicate discovery of imported TestCase fixtures. Check active publication revalidation because it changes the accepted publication surface at exactly this boundary. After candidate bytes are complete, record a local test commit and bind final tests/review to it.

## Supported stopping point

A repaired and independently reviewed B1/B2 unit can remove these prerequisites; it cannot establish whole-candidate readiness while B3 and full-CI/seven-point/publication gaps remain. No production application, rebaseline, ordinary reconstruct final commit or publishing is authorized. Record precise residuals and next responsibility in the handoff.
