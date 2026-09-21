# Independent r2 application-readiness review

Date: 2026-09-16 JST. Disposition: **NOT_READY for production application / canonical final seven-point audit not started**.

Reviewed candidate: `d38f023ce200619f7f49ce17a348755f05e0e021`, tree `960585ef29b55567efdf08901de489e4f3bb8fe5`, authentic parent `774dd39a951c9ac3818e83dfffd4c7666efb0a20`.

This is an independent preparatory application review. The Auditor did not author the five-file r2 proposal, its one-file test adjustment, or the root diagnostic harness. The root's proposed application scope was treated as an input to assess, not authority for acceptance. No production writes, current-main lookup, candidate edits, candidate fixture tests, Git object/ref mutations, or independent claims of Human approval were made. Auditor writes are confined to this directory.

## Decision

No actionable defect was found in the six-file delta within the reviewed scope. The test adjustment changes the obsolete requirement to copy live status; it does not relax actual reviewed-commit, Human-Gate, schema, or authority validation. This conclusion is **not** whole-candidate approval. The unchanged Core contains concrete contradictions on the normal Publication Preview-to-Freeze route and unresolved reader-review binding limitations. Those matter to the existing full-candidate acceptance rule even though r2 did not cause them.

Do not present this candidate as 7/7 PASS, ready to adopt, or ready for Human full-candidate approval. Keep r2 as a reviewed proposal; separately decide the smallest maintenance scope needed to make whole-candidate acceptance supportable. This report does not authorize that repair work or adoption. A later repaired candidate requires new diagnostic/synchronization/freeze work and a fresh seven-point audit from Point 1.

## Input and evidence boundary

`source-checks.json`, produced by `inspect_candidate.py`, independently verifies exact HEAD/tree/parent, all six changed file hashes and full diff path set, the inert origin, own `.git`, and absence of alternates. It also verifies that all 13 script/schema/test inputs referenced by the fixed-baseline reconciliation witnesses still have the same SHA-256 and Git blob identities on this candidate. `candidate.diff` preserves the reviewed delta.

The Auditor read `final-audit-rule.md` and `postintegration-amendment.md` first, then the actual candidate diff, execution-record policy, applicable authority, the test change, and targeted source/schema connections. Historical `notes/phase-5-upstream-reconciliation/probe.py`, `probe-results.json`, `README.md`, and `inputs.json` were read before reuse. Their observations remain function/schema witnesses, not a full workflow, successful production run, or newly executed independent regression. No successful prior r2 test was rerun merely for coverage.

## Actionable baseline blockers

All line numbers below are candidate-relative at the reviewed SHA. None of these paths changed in r2/a1.

### B1 — P1: Freeze checkpoint and validator demand incompatible artifact sets

Locations: `scripts/survey_stage_validation_v2.py:76`, `:173-176`, `:598`; `schemas/stage-checkpoint-v2.schema.json:244-248`; `scripts/survey_agent_control_v2.py:199-200`.

At `RELEASE_CANDIDATE`, the local validator accepts exactly `freeze-record` and `release-manifest` and rejects any extra current artifact. The Stage Checkpoint schema requires `visual-review-record` as well. The report contains only current artifacts, and the controller requires the report artifact map to equal the checkpoint artifact map. Consequently, adding the schema-required third artifact is rejected by the validator, while omitting it cannot satisfy the checkpoint schema; appending it only to the checkpoint cannot satisfy report equality. This is a connected source-level contradiction, independently checked here, with the existing `_current_artifacts` rejection witness as supporting function evidence.

Impact: the ordinary validated Freeze transition cannot meet these combined requirements. This blocks an unqualified Point-7 claim that approved Publication Preview resumes Freeze, and consequently ordinary Weekly/Special completion claims. Minimal resolution must align the actual Freeze artifact contract while retaining exact Candidate/PDF/visual/approval binding; do not remove validation or invent a success stub. Evidence type: current source/schema inspection plus retained fixed-baseline function witness. No full new workflow was executed.

### B2 — P1: Publication approval is read as a Stage Checkpoint

Locations: `scripts/survey_agent_control_v2.py:1209-1211`; `scripts/survey_stage_validation_v2.py:140-148`, `:578-580`; `schemas/stage-checkpoint-v2.schema.json:7-18`.

The canonical approval producer writes the Publication Preview approval authority into both `human_gate_provenance.publication_preview` and `checkpoint_provenance.publication_preview`. The next local stage validator iterates all checkpoint provenance and schema-loads every record as a Stage Checkpoint. A Human approval is a different typed record and lacks the Stage Checkpoint fields. The historical witness checked an actual hash-matching W34 approval against that schema and observed rejection; source inspection confirms the producer/consumer mismatch remains on this candidate. This does not imply that W34 was never released: the saved State/release remains historical evidence, and the witness did not validate its entire dependency closure.

Impact: even after B1 were corrected, the normal post-approval stage-validation route still has this separate type failure. Minimal resolution must preserve type-aware approval validation and exact provenance instead of skipping unknown records. Evidence type: current connected source inspection and retained actual-record/schema witness; not a newly executed full State/production test.

### B3 — P1: Reader review projection/binding is insufficient for a full exact-source claim

Locations: `scripts/survey_weekly_semantic_publication_v2.py:309-310`, `:516-526`; `scripts/survey_reader_surface_gate_v2.py:841-881`, `:1284-1289`, `:1545-1558`.

The Weekly renderer emits `frontmatter.lede`, but the structured surface builder's input and serialized payload omit that field. The preserved projection/render witness changed that reader-facing text while leaving the reviewed surface hash unchanged. Separately, the Gate validates the semantic review against its named reviewed surface file, without proving that this structured surface covers the current primary manuscript. The preserved Gate witness changed primary TeX and its manifest hash while leaving the same-issue persisted reviewed JSON unchanged; new Gate generation and revalidation accepted it. The positive control rejected drift in the reviewed JSON itself, so the limitation is the relationship between the two surfaces, not absence of all hash checking.

Impact: passing these Gate checks alone cannot support complete reader-source semantic-review binding under final-audit rule section 6. This is a concrete prerequisite to a broad exact-reader-surface assertion, not evidence that a whole publication or Human Gate was bypassed. Other publication checks may reject other defects; no full stage advance was attempted in the witness. Resolve the coverage/derivation relationship or produce an exact-head counter-demonstration of the complete required route before claiming full acceptance. Evidence type: current source inspection plus retained fixed-baseline function/projection witnesses. Synthetic review records remain fixtures, not independent editorial approval.

The retained internal `architecture_coverage.detail` lexical-rejection witness is additional scope evidence, not a fourth independently established lifecycle blocker; this review does not expand into a general reader repair specification.

## Six-file delta assessment

- Authority/index changes preserve generic immutability, separate edition authorization, mandatory governance, fixed-head audit/invalidation, and historical access via the fixed parent. They do not declare missing acceptance evidence to be approval.
- Execution-record changes keep substantive session/review obligations and active State provenance. The initialized navigation explicitly distinguishes history, pending review, active approvals and Candidate authority; it does not substitute a display for existing validation. Existing historical indexes remain preserved.
- The Python implementation change is confined to output templates. It changes no loader, Gate/reviewed-commit algorithm, lifecycle transition, schema or authority resolver.
- `tests/test_survey_findings_v2.py:149-195` retains Repair Set/Finding historical checks, worklog/closure checks, autonomous bootstrap boundary, seven-point audit restart and transport checks. It replaces obsolete copied current-status requirements with generic scope/immutability, missing-evidence, and fixed-history checks. Removing the invalidated candidate SHA substring check is acceptable here because historical access is retained and non-reuse is still explicit. These prose assertions are limited document regression checks; they are not a proof of runtime authority.
- The pipeline contract hash changes because three edited documents are configured contract inputs. The root's `contract-impact.json` makes that explicit; it must not be treated as a cosmetic or identity-preserving migration. Its exact identity computation covers the original five production files, unchanged in a1. No executed edition migration or old-State compatibility certification follows from it.

## Final-audit prerequisites

`docs/survey-production-core-v2-final-audit-rule.md:9-22` requires all candidate changes, diagnostic repair, repository synchronization and full-scope cross-check before freeze and seven-point audit. The postintegration amendment preserves exact-head CI and a fresh seven-point audit for later candidates. The authority index retains the five CI families at `:337-343`; these are not interchangeable with the seven acceptance points.

At preparation time, root reported completion of local parse/compile checks while the full Python 3.12 unittest diagnostic remained in progress. Its final results and input seal are pending this report's diagnostic closeout. Raw Worker logs are partial diagnostics, not complete CI. No seven-point audit has started and no point is marked PASS. Even green final diagnostics cannot discharge B1/B2/B3 or replace the required full acceptance evidence.

A live Actions run/transport execution, real research/editorial/visual judgments, actual Human decisions, all-profile publication viability, historical dependency closure, measured lifecycle savings, and production adoption have not been certified by this review. Post-integration real branch matrix requirements remain after the separate audit/approval/integration boundary; this review does not demand unauthorized production execution to manufacture them now.

The immediate result is a complete independent **pre-audit NOT_READY** decision, subject only to recording the final root diagnostic inputs without converting it into a final seven-point audit.
