# Stage-advance plan CANDIDATES_NORMALIZED → EVIDENCE_REVIEWED — preparatory note only (no execution)

2026-11-05. Read-only bounded operator preparation. **No active writes/import/runtime/tests/network/Production/reconstruct Git/readback executed for this note.** Active instance only as read source: `.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work`, recorded epoch `e84a82aca000c990597ea8cf60f548e2ff187bd1` parent `480823560c0c26ed2e5baa18e0e79a22b2839a27`. Old `480` rehearsal + failed `bd80` preserved, not active.

This is evidence-only preparation. It is **not** a deterministic PASS, not source validation, not a State advance, not a Human Gate.

## 1. Current readiness (actual)

- Both States `CANDIDATES_NORMALIZED`, `target ARCHITECTURE_REVIEW`, `next stage:evidence-materiality-completeness`, impl `48082356` retained (no hand-repin). Contract8 unchanged by script-only e84 repair. E84 runtime matches final139 delivery except test-only `d486809c…` vs `7b862305…`; other770 exact.
- Checkpoints each exactly 2 files: `orchestration/v2/checkpoints/ISSUE_INITIALIZED.json` + `DISCOVERY_COLLECTED.json`. `CANDIDATES_NORMALIZED.json` absent both, `EVIDENCE_REVIEWED.json` absent both. `stage-reviews/` 2 each, `stage-validation/` 2 reports each. `evidence/materiality/completeness pending/null`, `human pending/null`, `gates/` absent. From-state naming: missing producer is `CANDIDATES_NORMALIZED.json`.
- SP: NEW sets `evidence/v2/accepted/73f4bc1ec69c70925a7119a0327ff5e6f024812b56cf8edd7c49eae9f672a297/evidence-accepted.json` 49237B `65784e69…` (152 PARTIAL/8 VERIFIED) + views `5e722402…` 64222B `1557fef7…` + ledger `b7c85b4e…` 66850B + completeness `d67f7f83…` 33683B LIMITED, staged input `697a4ed0…` 355643B, supplement `ffcd0a7e…` 30922B. Final independent re-review `reviews/sp-evidence-final-rereview-20261105T011000Z.md` = `FINAL BOUNDED_PROCEED to EVIDENCE_REVIEWED` (authority-consumption/research-quality only, delta-scoped, NOT full160 semantic PASS, NOT publication/Selection/Architecture/Draft/Candidate/Preview/Freeze/Release/Human Gate). SP may advance via normal checkpoint path when ready; no Selection/Architecture PASS yet.
- W34: e84 409 outputs (`bf208f96…` 126603B `450b508c…`, views `f744e46b…` `5ad0a6ac…`, ledger `76ac53f9…`, completeness `93dbefae…`) exist but independent review `w34-evidence-authority-consumption-review-20261104.md` = `CHANGES_REQUIRED`, addendum `PROCEED_WITH_RESIDUALS_TO_SELECTION_PREP` is **not** EVIDENCE_REVIEWED, chronology addendum holds CHANGES_REQUIRED. Later W34 dispose left canonical Ledger/Completeness absent with verified backups in `retention-W34-dispose-20261105T003915Z/`; retry refused on invented split targets. **W34 run/review pending: corrected input + normal strict-facade retry + independent re-review required before any checkpoint.** Do not advance W34 now.
- Old SourceIntake/Screening BOUNDED PROCEED reviews (`source-intake-review-20261101T104700Z.md` + CORR, `screening-w34-review-20261101T111852Z.md`, `screening-efficient-llm-review-20261101T111203Z.md`) are prior-stage authority only. They do not authorize Evidence advance. Reuse their executor pattern truthfully, do not copy their verdicts as Evidence PASS.

## 2. Exact normal transport (active e84 source, read only)

No new checks/Gates/schema/module. Use existing agent-first path only; legacy `core.transition_state` / `plan_action` not selected.

```
def build_stage_checkpoint(
  repo_root: Path, cfg: dict[str, Any], state_path: Path,
  artifacts: dict[str, Path], reviews_path: Path | None,
  summary: str, recorded_at: datetime,
  implementation_sha: str | None = None) -> Path
def advance_with_checkpoint(
  repo_root: Path, cfg: dict[str, Any],
  state_path: Path, checkpoint_path: Path) -> dict[str, Any]
def validate_stage(
  repo_root: Path, cfg: dict[str, Any], state_path: Path,
  supplied: dict[str, Path], output_path: Path,
  recorded_at: datetime) -> Path
# survey_stage_validation_v2.py:852, survey_agent_control_v2.py:2227,2304
```

Config `config/survey-production-v2.json:303-310`: `CANDIDATES_NORMALIZED {handler stage:evidence-materiality-completeness, validator validate:evidence-materiality-completeness, next_state EVIDENCE_REVIEWED, checkpoints [evidence,materiality,completeness]}`. `REQUIRED_CURRENT[CANDIDATES_NORMALIZED]` = 4 names (§151-159). Schema `schemas/stage-checkpoint-v2.schema.json:200-207 evidenceArtifacts` requires all 4; `localStageValidationReview:136-171` requires exactly one `CORE_STAGE_CONTRACT DETERMINISTIC PASS`.

Review file input shape (`_load_reviews:2182`): `{"reviews":[{check_id unique non-empty, kind in [DETERMINISTIC,AGENT_RESEARCH,AGENT_EDITORIAL,AGENT_VISUAL], executor non-empty, evidence non-empty, result_path?}]}`. Allowed keys only those 5. Deterministic rows must carry `result_path`; agent rows must not. Loader sets `status PASS`; checkpoint stores `result {path,sha256}` for DETERMINISTIC, `null` for AGENT_*.

`CORE_STAGE_CONTRACT` report fields (`validate_stage:890-902`, checked in `_validate_core_stage_report:680-731`): `schema_version 2.0-rc1, check_id CORE_STAGE_CONTRACT, status PASS, issue_id, from_state CANDIDATES_NORMALIZED, to_state EVIDENCE_REVIEWED, production_state {path,sha256}, production_profile {path,sha256}, implementation_commit_sha (40 hex, current HEAD at dispatch), contract (8 keys), artifacts sorted NamedAuthority, recorded_at iso`. Rehashes State/Profile/report/result bytes; refuses on lifecycle/issue/contract/impl/artifact drift. No overwrite of existing report (`validate_stage:904-905`).

Canonical paths (from-state rule, `canonical_checkpoint_path:2132-2134`, `state_authority.agent_checkpoint_dir orchestration/v2/checkpoints`):
- `sources/<issue>/orchestration/v2/checkpoints/CANDIDATES_NORMALIZED.json` (to be built; must not pre-exist with divergent bytes)
- `sources/<issue>/orchestration/v2/stage-validation/CANDIDATES_NORMALIZED-report.json` (fresh `validate_stage` output; observed convention, reverify at dispatch)
- `sources/<issue>/orchestration/v2/stage-reviews/CANDIDATES_NORMALIZED-reviews.json` (exact input file for `reviews_path`; observed convention)
- 4 artifacts: `evidence-acceptance, edition-views-acceptance, materiality-ledger, profile-completeness` resolved via `pubset.resolve_stage_artifact_path` + `_validate_stage_artifacts`; supplied paths must equal canonical State-bound paths, not stale copies.

Required review rows for this advance (2 rows):
1. `check_id CORE_STAGE_CONTRACT, kind DETERMINISTIC, executor <truthful operator, e.g. General isolated-rehearsal deterministic stage validation (author, not independent reviewer)>, evidence <fresh report path+sha on exact current bytes>, result_path <same report path>` — author-side deterministic evidence, not independent review.
2. `check_id <existing actual review id, no invention>, kind AGENT_RESEARCH, executor <truthful independent reviewer, e.g. SAME NEW independent substantive Evidence reviewer for SP; fresh independent reviewer for W34>, evidence <exact review file path+sha + bound artifact pins + scope/limits>, no result_path` — cites actual completed review. For SP: `sp-evidence-final-rereview-20261105T011000Z.md`. For W34: pending — do not fabricate.

No Sol/Human impersonation. No `GAP` review, no legacy attestation, no PREARCH branch (forward builder/advance refuse PREARCH; `_require_dm022_ready` guard absence required at entry + prepublish).

## 3. Schema `evidence_review` clarification

No schema file/field named `evidence_review` exists in active e84 (`schemas/` + `scripts/` search: only `evidence_reviewed_sha256`, `evidence-reviewed.jsonl`, `_make_evidence_reviewed_state` test helpers). Do not create a new check/Gate/schema.

Governing rules are:
- `schemas/stage-checkpoint-v2.schema.json` `$defs/evidenceArtifacts` + `$defs/localStageValidationReview`
- `schemas/operator-execution-request-v2.schema.json` `$defs/agent_review` (`check_id/kind AGENT_RESEARCH|AGENT_EDITORIAL|AGENT_VISUAL/executor/evidence`, no result authority) for `ADVANCE_STAGE`
- `scripts/survey_stage_validation_v2.py REQUIRED_CURRENT` + `_evidence_basis` semantics
- `scripts/survey_agent_control_v2.py _load_reviews/_validate_core_stage_report/_validate_stage_artifacts`

## 4. Exact write-set when later authorized (one invocation, stop on first failure)

Preparatory DATA now: this plan only (packet-local). No State/checkpoint/report/reviews/retention writes now.

At dispatch, after fresh independent review exists and Root authorizes, allowed writes are exactly:
- one NEW `CANDIDATES_NORMALIZED-report.json` via `validate_stage` (refuse if exists)
- one NEW `CANDIDATES_NORMALIZED-reviews.json` (exact copy of reviewed packet-local reviews JSON into `stage-reviews/`)
- one NEW `CANDIDATES_NORMALIZED.json` via `build_stage_checkpoint` (refuse divergent overwrite; idempotent same-bytes only)
- then `advance_with_checkpoint` writes `production-state.json` (marks `evidence/materiality/completeness passed` + provenance, moves lifecycle to `EVIDENCE_REVIEWED`, refreshes control, revalidates)

No other writes: no source/config/schema/scripts/tests, no Profile/State repin, no Human Gate files, no Selection/Architecture/Draft/Candidate/Preview/Freeze/Release, no ledger/completeness overwrite (ordinary writers already own them), no cleanup/force/State reset/fake REQUEST_CHANGES, no reconstruct Git. New artifact reviews may be copied exactly into `sources/<issue>/orchestration/v2/stage-reviews/` / `sources/<issue>/execution/reviews/` only when that dispatch is authorized; transcription = byte-exact copy, no paraphrase as authority.

Failure handling (code-enforced, `build:2244-2251,2296-2300`, `advance:2311-2317,2326-2343,2372`, `validate:864-873,888,904-905`):
- State/Profile/contract/impl/artifact/report drift → refuse with no write.
- DM022 guard present / PREARCH misroute → `DM022_WRONG_FAMILY` / `DM022_TRANSITION_ACTIVE`, no write.
- Checkpoint path not canonical, issue/lifecycle/checkpoint-set mismatch, divergent overwrite → refuse, preserve unknown State, report exact bytes.
- `terminal_reason` set, Human Gate reached, FROZEN-only paths → refuse.
- Any failure: preserve partials, record numeric exits/raw observations in fresh exclusive packet namespace, no auto-retry/restore/cleanup, resume requires new bounded observation/decision.

## 5. Source epoch / current-proof behavior (record-owned)

State impl remains `48082356`; e84 is source commit only, Contract8 identical. `build/advance/validate` bind `implementation_commit_sha = repository_commit_sha(repo_root)` at dispatch (must be `e84a82a…`) and `contract = contract_identity(...)` (must equal current Contract8), plus `production_state/profile {path,sha256}` rehashed at dispatch. Prior `verify_renewal_source_proof CURRENT_PROOF_VALID` + SAME-proof drift refusal/repair is Weekly-only current-proof, not Evidence-stage authority. Do not claim e84 run proves normal retry for a fresh instance; preserve old480/bd80, SP old sets, W34 absent-2 + backups.

## 6. Real needs vs preparatory notes

Real needs (require execution + review, not met by this note): fresh `validate_stage` PASS on exact current bytes for each edition; actual independent `AGENT_RESEARCH` review bound to exact NEW accepted Evidence/Views/Ledger/Completeness bytes (SP done, W34 pending); dispatch-time revalidation of all bindings; canonical checkpoint + State transition.

This note provides only: pin inventory, signatures, paths, failure rules, readiness/missing list. It proves nothing about publisher truth, quality, savings, or audit.

## 7. Minimum next Selection/Architecture prep (boundary after Evidence acceptance, not authorized now)

After `EVIDENCE_REVIEWED` only: `EVIDENCE_REVIEWED {next_state SELECTION_COMPLETE, checkpoints [selection]}` requires `candidate-matrix + candidate-selection` (`REQUIRED_CURRENT`, `build_candidate_matrix.build(evidence_reviewed,pipeline_state)`); then `SELECTION_COMPLETE → ARCHITECTURE_ESTABLISHED` requires `issue-architecture + architecture-review-summary + architecture-review-attention` + `approve_architecture` + Human `ARCHITECTURE_REVIEW` Gate. No Draft/Candidate/Preview/Freeze/Release until Architecture approval. Selection must still explain exclusions (W34 30 DROP + carry-over C076/C077; SP 5 EXCLUDED DROPs + per-figure/ablation/version pins + 5 CONTEXT historical). No new generic reader, no silent Special exclusion, no synthetic PASS as approval.

## 8. Missing / stop

- SP: ready to prepare dispatch inputs; missing fresh deterministic report + canonical checkpoint/reviews files (must be created at dispatch, not now). Root may dispatch `validate→build→advance` when ready.
- W34: NOT READY — missing corrected accepted Evidence/Views/Ledger/Completeness + independent re-review. Complete input correction + normal strict-facade retry + re-review first; do not build checkpoint.
- WholeNOT_READY/step4B3OPEN/auditunstarted/DM021+022OPEN; quality/adoption/savings OPEN. Stop at Commit Point; do not auto-start checkpoint, Selection, audit, or Human Gate.
