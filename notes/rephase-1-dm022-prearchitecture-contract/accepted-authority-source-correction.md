# DM022 accepted-authority — source correction (Task A correction, design only)

2026-10-26. Corrects `accepted-authority-source-analysis.md` per Root CHANGES_REQUIRED.
That file is preserved; this is the ONLY new write. No code, runtime, tests, Git, network,
Production, or source edits. Final93 proof-copy is actual `409b292`+93.

## 1. What was overbroad

- `agent._validate_checkpoint_record` (`survey_agent_control_v2.py:481-594`) checks
  Stage Checkpoint `{path,sha256}` shape, schema (`stage-checkpoint-v2.schema.json`),
  producer `from/to`, checkpoint membership, artifact SHA drift, review-result drift,
  and `_validate_core_stage_report`. It does **NOT** enforce a canonical checkpoint
  path there. Canonical-path enforcement lives only in `advance_with_checkpoint`
  (`1768-1826:1772-1773`) and `_validate_stage_artifacts` (`1622-1655`), not in the
  readback validator.
- Agent resolver (`_resolve_checkpoint_artifact:761-860`,
  `resolve_active_evidence_views:902-938`) is State-bound Stage Checkpoint authority,
  NOT `core.validate_state_semantics` attestation-dir + global commit. The two must
  not be conflated.
- Pending-Architecture operator invalidation DOES exist conditionally
  (`survey_human_gate_v2.py:1179-1348`, `_current_pending_gate:440-485`,
  `gate_at_state={ARCHITECTURE_ESTABLISHED,RELEASE_CANDIDATE}`), but only at
  `ARCHITECTURE_ESTABLISHED` with `HUMAN_GATE_REACHED` + passed `architecture`
  checkpoint. It is not available at bare `EVIDENCE_REVIEWED`. The initial file was
  correct that no path exists at `EVIDENCE_REVIEWED`, wrong to imply no conditional
  path exists anywhere.
- Corrections: history does NOT unconditionally require a schema change (transcript
  stays forward-only); canonical attestations do NOT unconditionally require mutation
  (agent path resolves Stage Checkpoints, not attestation dir).

## 2. Root candidate under test (not selected, not code)

Same `EVIDENCE_REVIEWED`, no `selection`/`architecture` passed, no Human reviews/
approval/provenance, no Exception/publication pointer, healthy canonical strict agent
State. Keep Profile/Discovery/Screening identities + frozen old graph. New immutable
corrected Evidence/View accepted runs + versioned Ledger/Completeness. ONE new typed
supersession CHECKPOINT record (or record+checkpoint if justification needs it) carrying
all 4 artifacts, old checkpoint/supersedes lineage, before-State COPY/retention/decision/
input/current-tool/validation refs, truthful `EVIDENCE→EVIDENCE` operation (never a fake
`CANDIDATES→EVIDENCE` stage report). Sole LIVE mutation = atomic State replacement
re-pointing `checkpoint_provenance.{evidence,materiality,completeness}` to the SAME new
record; machine pass/lifecycle/Human/history unchanged; no extra live pointer.
`resolve_active_evidence_views` then yields the new pair iff the new kind/checkpoint
branch integrates. History stays the forward-transition transcript; supersession lineage
is append-only outside history.

## 3. Why the triplet shares one record

- `_producer_for_checkpoint` (`348-352`) derives producer from `stage_plan`; config
  `CANDIDATES_NORMALIZED.checkpoints=[evidence,materiality,completeness]` (read actual
  JSON) so all three map to `(CANDIDATES_NORMALIZED,EVIDENCE_REVIEWED)`.
- `advance_with_checkpoint:1808-1812` writes the SAME authority to every checkpoint in
  the stage. `resolve_active_evidence_views:914-923` explicitly requires
  `evidence.checkpoint_authority == views.checkpoint_authority` and View
  `evidence_acceptance_sha256` binding (`928-932`). A single supersession record is
  therefore the correct granularity, not three records.
- Schema `stage-checkpoint-v2.schema.json:200-208` `evidenceArtifacts` requires
  `from_state=CANDIDATES_NORMALIZED` to contain exactly `evidence-acceptance`,
  `edition-views-acceptance`, `materiality-ledger`, `profile-completeness`. Entry uses the
  same agent-first Stage Checkpoint shape only; no legacy attestation migration.

## 4. Constructibility: irreducible contradiction vs required new code

Contradiction: any new record with `from_state=CANDIDATES_NORMALIZED,
to_state=EVIDENCE_REVIEWED` while LIVE state is already `EVIDENCE_REVIEWED` looks like
a second lifecycle execution; any record with `from_state=to_state=EVIDENCE_REVIEWED`
has no producer in `stage_plan` (`493-500` mismatch) and no schema branch. Rebinding raw
legacy checkpoint refs without typed proof would already pass
`_validate_checkpoint_record` shape checks, but that is still an UNSELECTED public write
with wrong `from/to` report — shape acceptance is not authority. The name gap does not
mean the validator cannot parse a versioned path; it means no lawful writer exists.

Required new code (minimal, all in agent-first surface):
1. New strict typed kind/branch, e.g. `EVIDENCE_SUPERSESSION_V1` record + checkpoint
   `from_state=EVIDENCE_REVIEWED,to_state=EVIDENCE_REVIEWED` with explicit producer
   exception scoped to that kind only; `_validate_checkpoint_record` gains a
   same-State branch that checks: supersedes→old-checkpoint lineage, all-4-artifact
   presence, `issue_id` match, checkpoint set `{evidence,materiality,completeness}`,
   truthful operation tag (not `CANDIDATES→EVIDENCE`), before-State COPY hash,
   Sol decision + HEAD/Tree guards. `_validate_core_stage_report:365-442` gains a
   same-State report path: `historical_state.lifecycle=EVIDENCE_REVIEWED`,
   `report.from==report.to==EVIDENCE_REVIEWED`, before/after stage-report semantics
   (before = old checkpoint artifacts re-validated; after = new 4 artifacts
   re-derived via `_evidence_basis`-equivalent content checks, detached from LIVE
   recursion with fresh LIVE HIGH separate).
2. ONE new PUBLIC writer (agent-first, not `core.transition_state:998-1048` which stays
   forward-only, not `invalidate_pending_gate`): pre-write gates
   `lifecycle==EVIDENCE_REVIEWED`, selection/architecture pending, both Human Gates
   pending+null provenance, no Exception/publication pointer, Sol scope decision,
   exact HEAD/Tree, old-triplet exact match, affected-ID allowlist; snapshot typed
   immutable old runs + COPY mutable State; exclusive new-run dirs; atomic State
   triplet swap; full `validate_agent_state` before commit; rollback on any error.
3. `resolve_active_evidence_views` + `_resolve_checkpoint_artifact` gain the new
   kind/checkpoint branch (same-triplet equality rule preserved); all normal consumers
   unchanged in call shape: `run_selection_architecture_v2_interactive.py:179`,
   `run_drafting_synthesis_v2_interactive.py:67`,
   `run_semantic_publication_v2_interactive_base.py:131`,
   `survey_editorial_correction_proposal_v2.py:1508`, plus stage/selection/architecture/
   drafting/Reader/LF/R1/editorial/renewal validators that re-derive from the resolved
   roots. No caller-verified dict: content validators (`validate_screening_acceptance:
   survey_evidence_v2.py:490-536`, `validate_evidence_acceptance:1412-1434`,
   `validate_edition_views_acceptance:1555-1576`, `validate_materiality_ledger:1771-1794`,
   `validate_completeness:1944-1966`) re-hash live bytes; proposed admission never
   trusted.
4. No `core.verify_state_basis` global-equality shortcut: current/tool bindings are
   per-checkpoint `implementation.repository_commit_sha` + `contract`
   (`_validate_core_stage_report:424-433`, `build_stage_checkpoint:1730-1741`) as normal
   agent public validation. Old research bytes are not tool commits.

## 5. Screening INSPECT retention (checked, not unknown)

- `build_evidence_tasks.py:19 PROMOTED={KEEP,MAYBE,INSPECT}`; ledger
  `survey_evidence_v2.py:1602-1635`: non-DROP Discovery requires exactly one task,
  disposition = View materiality, irrespective of KEEP/MAYBE/INSPECT. So retaining
  `INSPECT` while promoting View HOLD→MATERIAL is structurally permitted.
- Card→View coupling `validate_edition_view:1437-1491`: `REJECTED→NON_MATERIAL:1456`,
  `NEEDS_MORE→HOLD:1458`; `VERIFIED/PARTIAL` may be MATERIAL. New official Evidence
  must therefore be `VERIFIED/PARTIAL` (not `NEEDS_MORE`) for MATERIAL; no automatic
  status promotion. Same IDs preserved; re-consumption/original-HTML proof still
  required by Issue #562 (timestamps alone insufficient).

## 6. Phase HEAD binding (no self-reference)

New Stage Checkpoint `implementation.repository_commit_sha` must bind the coherent
phase HEAD that produced the new accepts (reviewed Core/main + tool tree at DM022
review time), NOT the commit that will contain the new record itself. Writer must pin
`expected_implementation_sha` from the pre-write work HEAD (cf.
`build_stage_checkpoint:1730`, `advance_with_checkpoint:1785-1787` current-tool check)
and `advance`-equivalent must re-check HEAD freshness before State swap, otherwise the
record self-refers. Accepted Core source CURRENT vs review-wait HEAD exact-tree issue
is resolved by binding to the reviewed maintenance-branch HEAD + Tree, never to a
future record commit.

## 7. Verdict for Root

Branch is constructible with the §4 deltas; no unchanged-code path exists (raw rebind =
wrong `from/to` + unselected write; legacy `transition_state`/`invalidate_pending_gate`/
renewal entry all refuse pre-write at `EVIDENCE_REVIEWED`). Minimal template: same
agent-first `stage-checkpoint-v2` shape, `from/to=EVIDENCE_REVIEWED`, kind-gated producer
exception, all-4 artifacts, triplet-to-same-record swap, lineage outside history.
Root selects after Task B comparison + fresh review. No independent PASS, no whole READY.
