# Typed agent-stage path inputs — ISSUE_INITIALIZED → DISCOVERY_COLLECTED (record only, no advance)

Root-selected path: `agent.build_stage_checkpoint` + `advance_with_checkpoint` with real
deterministic CORE_STAGE_CONTRACT report; NOT legacy `core.transition_state`/machine attestation,
NOT guessed `plan_action` dispatch. Code read from final138 `scripts/survey_agent_control_v2.py`
(`build_stage_checkpoint` :2227, `advance_with_checkpoint` :2304, report validator :605) and
`scripts/survey_stage_validation_v2.py` (`validate_stage` :852, ISSUE_INITIALIZED semantics :587).
Source unchanged. No checkpoint/state writes in this turn.

## Deterministic reports built (normal public API, exact current bytes)

- W34: `sources/2026-W34/orchestration/v2/stage-validation/ISSUE_INITIALIZED-report.json`
  1461B sha256 `678253235c1ec61444aa30fe23b4a3b20061089c5afe8225bab5a102e63be119`,
  PASS, from ISSUE_INITIALIZED to DISCOVERY_COLLECTED, artifacts [discovery-acceptance],
  state `078c34119c576522becaf78e39ae82ee902cb98972d55f3735fb503309f72ab8`,
  profile `2a8c3089cec29eb64e121cdf0429eed38670df704ebe955079751198557cfeb1`,
  impl `48082356…`, recorded_at `2026-11-01T10:42:52Z` (real clock; log `13-stage-reports.*`).
- SP: `sources/SP-efficient-llm-2026/orchestration/v2/stage-validation/ISSUE_INITIALIZED-report.json`
  1513B sha256 `4922f9843b8d49bccdf4e9d8d04fc69eb75085534e53f9fc92a074dd00df6d79`,
  PASS, same transition, state `ea77482e40529608aefb18b8a0399d6bc1a3ba600d3cbe3c512c329a51b5785e`,
  profile `aff05fd573ce873afa24c0ede26c2b4591ee28b7048c9ed528e8fc389ed8ee45`,
  impl `48082356…`, recorded_at same.
- States re-verified after builds: still ISSUE_INITIALIZED, zero checkpoints passed,
  bytes identical to report-embedded shas (no state mutation by report builds).

## Exact `build_stage_checkpoint` inputs (for root dispatch, post independent review)

Per edition, call with (paths repo-relative to workdir root):
- `artifacts = {"discovery-acceptance": <sources/<issue>/discovery/discovery-accepted-v2.json>}`
  (canonical template `{source_root}/discovery/discovery-accepted-v2.json` per stage_plan;
  fresh bytes: W34 369 graph `a13afd9e…`, SP 165 graph `441f488b…`).
- `reviews_path` = NEW reviews file (to be written at dispatch), exact content:
  `{"reviews": [{"check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC",
  "executor": "General isolated-rehearsal deterministic stage validation (author, not independent reviewer)",
  "evidence": "validate_stage PASS report <report relpath above> sha <report sha above> on exact current bytes; independent SourceIntake content review tracked separately in review-seam-sourceintake.md (pending assignment)",
  "result_path": "<report relpath above>"}]}`
  (one row; `_load_reviews` requires deterministic rows to carry `result_path`,
  agent rows must not; validator requires exactly one CORE_STAGE_CONTRACT deterministic PASS.)
- `summary` (proposed, non-empty required): `"Discovery acceptance validated (W34 369 / SP 165) with COMPLETE X intake bound to fresh Profiles; advancing ISSUE_INITIALIZED→DISCOVERY_COLLECTED after independent SourceIntake review."`
- `recorded_at`: fresh real clock at dispatch (not reused).
- `implementation_sha`: None (= current HEAD; must still be `48082356…`, states/reports bound to it).
- Canonical checkpoint output (verified ABSENT, must not pre-exist):
  W34 `sources/2026-W34/orchestration/v2/checkpoints/ISSUE_INITIALIZED.json`,
  SP `sources/SP-efficient-llm-2026/orchestration/v2/checkpoints/ISSUE_INITIALIZED.json`.
- Dispatch-time re-verification (code-enforced): agent state basis, DM022 READY (guard absence),
  profile/state authority equality vs dispatch-time bytes, contract == current
  `contract_identity`, report artifacts == checkpoint artifacts. Any drift refuses (no overwrite of divergent checkpoint).

## Exact `advance_with_checkpoint` call (root dispatches only after review decision)

`agent.advance_with_checkpoint(repo_root=WORK, cfg, state_path=<sources/<issue>/production-state.json>, checkpoint_path=<canonical path above>)`.
Code re-validates checkpoint-vs-lifecycle/contract/impl/artifacts/report, marks `discovery` passed
with checkpoint provenance, moves lifecycle, refreshes control, re-validates, re-checks READY,
then writes State. NOT executed here.

## Why not the alternatives (read from code, not reimplemented)

- Legacy `core.transition_state` + machine attestation bypasses the agent-first validator,
  contract/implementation binding, and DM022 READY/role gates (`:2304–2374`); wrong model.
- `plan_action`/`execute_action` dispatch was not traced to a matching handler contract for
  this typed checkpoint in this turn; not guessed. The two functions above are the root-selected
  typed path with deterministic reports already bound.
- No test-fixture manual DCP/SCP rows were crafted; history shows test helpers
  (`_advance_to_discovery_collected` etc.) rewrite lifecycle/history directly — prohibited here
  (no state-basis stub/current-before hack).
