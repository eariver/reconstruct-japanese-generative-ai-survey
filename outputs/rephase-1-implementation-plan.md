# Re:Phase next-session implementation plan

Original plan: 2026-09-21 JST. Current status 2026-09-27 JST: **Increment A complete at `1a9649129d1745fed0b98db46ef15f014407e6fc`; Increment B complete within its selected scope at `c04f32ad46109403e8a63faaa8394a90ee6b869c`: exact-head 132 methods (131 successes, one historical skip), Astra review, independent finding resolution and a fresh final bounded implementation PASS. Initial step-4 Profile/support/application inventory and Astra disposition are complete; next selected unit is Gate CLI persisted-review admission, implementation not started. Whole B3/whole candidate remain OPEN/NOT_READY.** This is an isolated reconstruction plan, not production adoption authority. Read with the [compact handoff](../handoff/rephase-1-continuation.md), [Astra Increment A assessment](rephase-1-increment-a-assessment.md), [B contract/task](rephase-1-increment-b-contract-decision.md), [B assessment](rephase-1-increment-b-assessment.md), [current step-4 decision](rephase-1-profile-application-assessment.md), and [later Summary intake](../notes/rephase-1-session-transition/deferred-intake.md). Original starting identities and completed A/B task definitions below remain historical scope.

## Objective and fixed starting point

**Continuation update 2026-09-27:** step 4's initial bounded inventory and Astra disposition are complete; implementation/integration is not. Read [Profile/application assessment and next General task](rephase-1-profile-application-assessment.md) and [source inventory](../notes/rephase-1-profile-application/analysis.md). Next selected unit is persisted-review admission through the Gate CLI, not yet started; no new tests or candidate change. Human now directs **General/Explore** SubAgents (reportedly DeepSeek v4.1 Flash; actual serving model unverified), superseding historical Sol/Luna selection below while preserving their original attribution. Astra/Co-Worker/independent-review/Human responsibilities remain separate.

Continue the r2 application path only through justified, bounded prerequisites. Minimize total research/review/repair/CI/LLM/Human/migration work while preserving publication quality, exact authority and historical evidence. Do not treat every deferred maintenance item as an automatic prerequisite or a cost of r2 that must be paid without reconsideration.

- Production baseline: `774dd39a951c9ac3818e83dfffd4c7666efb0a20`, unchanged until explicit Human rebaseline.
- Isolated candidate: **f1** `bf32edf98ba8f605169d7188bbc764de74ee4f6e`, tree `ebd351479ec222a08b8ea67ae4aae64ad0eb927e`; parent a1 `d38f023ce200619f7f49ce17a348755f05e0e021`.
- f1 retains a1's six files, adds stage-validator B1/B2 repair and one test module. Its 24 tests and independent bounded review passed within their recorded scope. Whole candidate is **NOT_READY**; B3 open; canonical seven-point audit not started.
- B3 has design/function witnesses only, including 10 unprojected output mutations and 2 covered controls. The full-render-input prototype is rejected as a production format. It must not be copied into Core.
- The later Summary snapshot is **evidence only**. No follow of main, automatic refresh, code import, or Core restart is authorized. DM-001/003/004 remain separate application-path questions; DM-014 informs r2's alternative to status-copy maintenance.

## Roles and delegation — effective for future work

| Role | Responsibility | Selection |
|---|---|---|
| Astra/root | Architecture, scope/contract decisions, Co-Worker task definition, diff and evidence review, correction decisions, acceptance claims and durable synthesis | Does **not** become the normal code implementer or test runner; previous root-run experiments are historical, not a role precedent |
| Implementation Co-Worker | Source/test changes, isolated Git fixture preparation, test execution, failure investigation within assigned scope, raw evidence | **Sol for B3 Core/authority changes**, because type/admission/semantic boundary and Git-aware negative tests need substantial reasoning. Escalate scope concerns to Astra; no silent weakening |
| Bounded mechanical Co-Worker | Hash inventories, packaging, exact known commands or repetitive low-risk test execution after harness approval | **Luna when sufficient**. If fixture repair, authority interpretation, unexpected errors or nontrivial coverage reasoning is needed, use Sol instead; don't leave difficult work with Luna merely for price |
| Independent Auditor | Review fixed candidate and actual evidence without participating in its design/code/test authorship | Separate fresh context/persona from author and Worker. Choose capability by scope; B3 cross-authority acceptance normally warrants Astra-class independent review; small evidence-resolution checks can use fresh Sol. Not a relabelled Worker |
| Human | Production mutation/adoption/rebaseline decisions; ordinary final reconstruct commit/Pull/Push; actual Human Gates | No synthetic agent substitute |

Co-Worker “PASS” is execution evidence. Astra must review actual changed bytes, oracle strength, test scope, skipped/incomplete cases, failed setup attempts, negative controls, and candidate hash. Astra review is not independent audit. An interrupted/usage-limited Worker or Auditor report is partial; preserve it and assign a suitable replacement/resolution task. Do not have Astra quietly take over implementation/test execution when a Worker stops.

## Architecture decisions to implement

### A. Exact manuscript admission first — a bounded, implementable increment

Existing `validate_reader_surface_gate` verifies its recorded surfaces and same issue/Profile, but stage callers do not supply the exact selected Reader Manuscript. The Gate may therefore be valid for a different manuscript. Implement this relationship independently of the larger reader-input redesign; label the result **partial B3**, never B3 closure.

- Extend the existing Gate validator's admission contract to receive the expected manuscript selected by the caller. At active stage boundaries this reference is required, not optional fallback.
- Require exactly one matching MANUSCRIPT_MANIFEST path/hash and the corresponding PRIMARY_SOURCE path/hash; schema-load the actual expected manifest and preserve issue/Profile/hash/byte-count/review checks. Reject missing/duplicate/conflicting recorded surfaces. Do not accept equal issue/Profile alone or infer the desired file by directory scanning.
- Thread the expected manuscript through both `DRAFT_COMPLETE` and inherited `VALIDATED_DRAFT`, and any wrapper/revalidation caller that uses Gate authority. Standalone inspection may inspect its own bound manifest, but cannot be used to satisfy stage admission without the stage-selected reference.
- Prefer existing `scanned_surfaces` authority over a new duplicate ledger. No generic resolver, new Human Gate, status bypass, or arbitrary executable selector.

Primary files to inspect/change: `scripts/survey_reader_surface_gate_v2.py`, `scripts/survey_stage_validation_v2.py`; existing forwarding helpers in `survey_reader_publication_v2.py` and active publication revalidation in `survey_agent_control_v2.py` only where caller threading is actually required. Scope growth beyond these requires Astra's concrete decision, not automatic refusal or a new Human permission question.

### B. Complete Weekly reader input and derivation — one coherent later increment

Replace the incomplete reviewed projection and render from that same complete reader input. Include all emitted cover/frontmatter/section/result-only boundary/final-summary prose, visible issue/date/window metadata and citation identity/order. Use rendered Draft result content after existing spec/result validation. Internal rationale is not reader content merely because it is present in an upstream record.

- Preserve the Weekly two-pass `--materialize-surface-only` flow and non-PASS/missing semantic-review stop before TeX/Bib source materialization. No generated review PASS.
- Schema-validate the exact reviewed object and its declared route/Profile; remove best-effort acceptance of malformed derived JSON. Existing fixtures with `final_summary` instead of required `final_summary_paragraphs` must be corrected as fixtures, with failure history recorded, not by weakening schema validation.
- Validate projection equality from accepted upstream authority and deterministic output equality at both Gate creation and independent revalidation. Fresh hashes on unrelated input/output do not establish derivation. Explicit structured-surface arguments must match the actual reviewed target.
- Bind the actual renderer and relevant helper/style contract through existing current-tool/contract/source-manifest mechanisms. Review-driven Core change/revalidation remains effective; no invented evergreen renderer hash or initialization-commit substitution.
- Do not copy every upstream object into semantic input. Nonreader runner/debug/provenance changes may update mechanical derivation evidence but cannot by themselves require semantic re-judgment if the complete reader content/meaning is unchanged. This is not permission to reuse stale PDF/visual/Human approval after output bytes change.

Likely files: Weekly publisher, Reader-Surface Gate/builder, existing reader-input schema and relevant manuscript/source-manifest producer; tests in `test_survey_reader_surface_gate_v2.py`, `test_survey_semantic_publication_v2.py`, `test_survey_publication_revalidation_v2.py`. Final path list comes from Co-Worker's bounded callsite inventory before edits, reviewed by Astra. A shared helper is acceptable only for a concrete responsibility; avoid a universal rendering framework.

### C. Supporting-source and provenance split — selected responsibility, bounded unresolved details

| Surface/input | Responsibility selected for the implementation | Acceptance limit |
|---|---|---|
| Reader prose, emitted metadata and citations | Semantic reader input and substantive semantic review; the renderer consumes this single authority | Exact byte equality is necessary but does not prove intelligibility/research sufficiency |
| Reader-visible bibliography/source-note values | Include the visible citation/source representation in the reviewed input for the generated route, sourced from existing Evidence/provenance; independently render and compare the bibliography/support files | No raw internal ledger serialization, loss of public targets, forced translation, or conflation of displayed/announcement/access dates |
| Restricted provenance comments | Derive from existing accepted authority; constrain output to safe generated comments/hex identifiers, not arbitrary unreviewed TeX | Mechanical authority can change without semantic content change; existing exact-output approvals may still become stale |
| Trusted shared style/renderer helpers | Exact source closure/current contract + existing visual/publication review; preserve layout behavior | Arbitrary content-emitting style/support changes are not presumed “layout only”; if they emit variable semantics, model those inputs or reject the unsupported generated route |
| Supporting TeX/includes/macros beyond the declared generated closure | Explicitly enumerate and validate; no hidden dynamic include/command route | Do not claim complete coverage by comparing only `main.tex`. Unsupported dependencies cause a bounded stop/design decision, not silent acceptance or a new universal TeX parser |
| Direct-primary review | Exact review target equals selected manifest primary path/bytes; preserve this existing capability with a real positive/negative test | Supports primary identity only until supporting-surface semantic coverage is demonstrated; cannot be presented as whole Special/manual closure |

Before increment B is coded, Co-Worker must present a small contract table with the actual bibliography fields, style/helper dependency paths, unsupported include behavior, and the existing authority each consumes. Astra resolves it against this responsibility split. This is a concrete design gate within authorized work, not a request for renewed Human approval. If the existing source/publication review cannot cover supporting semantics without a new review obligation or authority consolidation, stop at that decision; do not invent a silent reuse adapter.

### D. Profile handling

Implement/prove Weekly generated route first while preserving explicit direct-primary capability. LONGFORM_SPECIAL currently lacks the same pre-TeX producer; Retrospective caller generality is unproved. Do not force Weekly fields onto Special or quietly accept unbound legacy JSON for compatibility.

Before **whole B3 closure**, supply a real Thematic/Longform route and Retrospective route evidence, or retain explicit unsupported/NOT_READY dispositions. Choose between a Longform reader adapter and an explicitly scoped direct-source route by its actual caller/review contract. Consolidating older Publication Review with Reader-Surface judgment changes authority and is not a casual schema adapter. No extra review or removal of necessary independent review is selected by this plan.

## Execution sequence and concrete deliverables

1. **Restart inventory and isolation (Co-Worker; no broad tests):** read only compact entry/plan; verify reconstruct status, baseline, f1 identity and hashes, runtime availability; copy f1 to an independent database with no hardlinks/alternates/inherited Git overrides and inert origin. Leave f1 untouched. Return identity and targeted callsite list. If native fixture is missing, use [recovery](../notes/rephase-1-session-transition/restart-context.md), not current main.
2. **Increment A (Sol):** implement exact manuscript admission and forwarding; add dedicated positive/negative tests. Run parent failure witnesses on a separate parent copy and affected new/existing tests in the successor. Tests must demonstrate wrong same-issue/Profile manuscript rejection, not merely malformed JSON or setup failure. Return patch and raw outcomes; Astra reviews before expanding scope.
3. **Increment B contract table (Sol analysis, Astra decision), then code/tests (Sol):** complete the responsibilities above using existing producer/manifest/contract paths. Include source-only and end-to-end bounded Weekly positives, all known omission controls, derivation negatives, and mechanical/semantic identity separation. Preserve prior intermediate candidate rather than rewriting its evidence.
4. **Profile/application integration:** resolve direct-primary/support and Special/Retrospective claims; exercise affected stage and #495 revalidation connections. Revisit DM-001/003/004 before a full application-ready assertion as separate prerequisite dispositions. Do not implement them merely to obtain green B3 tests.
5. **Freeze a reviewable isolated candidate:** all intended candidate bytes complete; local review commit and parent/tree/files/hashes recorded; final relevant checks bind that exact head. No final reconstruct commit or production publish. Astra reviews failures, diffs and test evidence; requests scoped corrections if needed.
6. **Fresh independent implementation review:** review runtime/schema/callers and evidence from a separate author context. Correct findings and rebind affected results to any changed candidate. Later required diagnostic/synchronization/full CI and canonical seven-point audit are distinct; never transfer f1's limited review or this planning review to final acceptance.

## Minimum verification matrix

| Boundary | Positive/control | Required negative evidence |
|---|---|---|
| Exact stage-selected manuscript | Gate for the exact selected manifest accepted at both stage sites | Different manifest same issue/Profile, swapped primary, missing/duplicate manifest or primary, stale bytes, forged fresh report digest |
| Weekly coverage | Covered headline/summary controls and all emitted fields represented | Mutate each of 10 historical omitted output categories; stale review rejected; distinguish citation identity from prose |
| Derivation | Same accepted input/current generated source passes | Modify TeX/Bib/support and refresh manifest/Gate hashes while keeping reviewed input; unrelated JSON, missing field, wrong renderer/source closure |
| Schema/identity | Schema-valid matching route/issue/Profile | Invalid `final_summary` shape, wrong Profile, wrong explicit surface, unknown route, missing/non-PASS review; source files remain unwritten on pre-review failure |
| Semantic/build split | Permitted nonreader metadata leaves reader input stable but rebuilds required mechanical evidence | Unreviewed prose introduced via comment/style/helper/include path; accidental stale PDF/Human approval reuse after byte change |
| Direct-primary/profile | Exact primary review positive; actual declared caller exercised | Review of another file with valid hash; no implicit legacy JSON fallback; unsupported profile remains fail-closed/uncertified |
| Existing connection | Active publication revalidation then affected stage report/checkpoint; exact Candidate/visual authority retained | Historical record tamper, conflicting Candidate, unrelated revalidation, suppressed mandatory authority check |
| Reader-public constraints | Public repository permalink, qualified temporal values, supplied public citation target preserved | Broad suppression/malformed suppression accepted, temporal strength/date meaning silently changed, internal rationale serialized |

Tests execute real loaders/validators and actual isolated Git when required, without authority/Git-success stubs. Synthetic research/review/Human fixtures must be labelled; they do not become real approval or publication evidence. Before/after witnesses must fail for the intended defect. Don't re-run successful f1/full suites for decoration; run affected existing checks once the change justifies them, then broader required diagnostics when candidate readiness actually warrants it.

Co-Worker evidence per run: command/cwd/runtime/dependencies; exact candidate/parent/tree and changed-file hashes; raw stdout/stderr and exit code; counts including skips/subtests; failed setup attempts and fixture-only fixes; whether actual canonical Human Gate or low-level producer was used; untested profiles/platforms/history/publication boundaries. Preserve INCOMPLETE results as such. Never infer independent review from filenames, artifact count, or missing logs.

## Stop, correction and audit rules

- Stop implementation and return a bounded finding to Astra for unsupported source closure, necessary new authority/review consolidation, unexpected unrelated baseline defect, or scope/cost growth beyond the selected interface. Do not solve it by relaxing validation or making every backlog item mandatory.
- Stop a test run that reaches real production refs/remotes, uncontrolled Git root, network dispatch or real Human/publication mutation. Repair the fixture boundary before rerunning; preserve failure history.
- An increment may be complete while B3/whole candidate remain open. Report exactly which boundary is repaired; no `CORE_FIXED`, application-ready, all-profile or seven-point claim without corresponding evidence.
- Net lifecycle saving remains unknown. Record concrete avoided/added work and re-review invalidation behavior; do not create telemetry infrastructure or assume extra documents prove saving.
- Production changes/adoption, current-main tracking/rebaseline and ordinary final reconstruct commit/Pull/Push remain outside Co-Worker authority. The Summary capture is a one-document exception already consumed, not ongoing tracking permission.

## Original first Co-Worker task — completed as Increment A

Use fresh **Sol** with scope **Increment A only**. “Read `handoff/rephase-1-continuation.md`, this plan, and the referenced f1 manifest. Verify/copy f1 into an independent inert-origin Git database. Produce a short callsite inventory for exact stage-selected Reader Manuscript admission. Implement mandatory expected-manuscript binding at active stage callers and exact recorded manifest/primary checks, preserving existing authority. Add positive and wrong-same-issue/Profile-manuscript negative tests at DRAFT_COMPLETE and VALIDATED_DRAFT; run intended parent failure witnesses and affected regressions. Do not implement the reader IR, suppression overhaul, Freeze/Release backlog or production mutation. Save patch, exact-head metadata and raw test/failure/limitation evidence in a new Increment-A packet; preserve existing artifacts. Return for Astra diff/evidence review before the next increment.”

Astra's first action is this dispatch after reading the compact entry and checking for new Human constraints—not writing implementation code, running the tests itself, rereading the entire chat, or refreshing production main.
