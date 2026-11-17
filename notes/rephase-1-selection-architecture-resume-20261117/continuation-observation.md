# Continuation observation — selection/architecture resume 20261117 (read-only operation-map/setup verification)

> ROOT QUALIFICATION (20261117 `astra-operation-resolution.md` §§1–2): this R1 observation reused prior hashes (`fresh_rehash_here:false`) and carries malformed SP views/ledger/W34 arch transcriptions. Do not use R1 pins for dispatch. Current replacement is `entry-binding-r2.md` + `entry-binding-r2-machine.json` (fresh stdlib 774 + State/Profile/CP/completion/COPY/8 refs/14 outputs/audit). Old body preserved below for history.


Role: read-only OPERATION-MAP / setup verification. Not source implementation, not reviewer, not stage execution. No project imports, runtime, tests, writer, checkpoint/stage writes, network, source edits, subagents, reconstruct Git status/log/HEAD/readback. Used dedicated file tools + stdlib-parse observation only; necessary read-only Git explicitly isolated ONLY if needed was not invoked (no fresh Git cert in this unit). Prior root closeout §7 governs continuation.

Governing: `notes/rephase-1-selection-architecture-resume-20261117/README.md` FULL. Prior: `notes/rephase-1-selection-scaling-repair-20261116/astra-closeout-resolution.md` FULL incl §7, `astra-repair-resolution.md` §§10–13, `final-implementation-review.md` §§10–11 + machine WITH FINAL-BINDING, `independent-real-output-review.md` §10 + machine, `closeout-evidence-index.md`. Role AGENTS: workspace `AGENTS.md` + selected-repo `AGENTS.md` (normal Human Gates `ARCHITECTURE_REVIEW`, `PUBLICATION_PREVIEW`; durable review surface commit/push/retain exact SHA; no inferred decision).

User reported Commit/Push, explicitly without Commit readback. This unit performs no reconstruct readback.

## 1. Selected instance (recorded-only, no fresh Git cert here)

- Path: `.rephase-1-editorial-runtime/selection-scaling-real-20261116T021943Z/candidate-work`
- Source `3231a0c280287411513bba359f4d3d2b6703f591`, parent `ae0dd1ee5b0e7a85c44bdab0e6cd024bf12f0c56`, tree `ff01b73e6012fd4519fdfb3807186753ff330367`. Recorded from `real-rehearsal-20261116T022222Z/README.md` + independent machines; no fresh `git rev-parse` in this mapping action.
- Base distinguished: actual409 `409b292756dd1277b9dfae87679934c0d2ce251c` / tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`.
- This dossier never claims `3231a0c` as future canonical Human-reviewed commit/branch. Canonical Human-reviewed commit/branch push remains NOT AUTHORIZED. Future Human review must commit/push/retain exact review bytes on Profile-bound work branch and use that exact SHA as `reviewed_repository_commit_sha` per selected-repo AGENTS.md.

## 2. FULL774 delivery availability (prior packet, reused as bounded evidence)

- Directory: `notes/rephase-1-selection-scaling-repair-20261116/source-packaging/final-20261116T031000Z/`
- `complete-selection-scaling-manifest.json`: SHA256 `0dc361cb8284f3465243120b7cea8e20476c3fbe81d90a71ce3028dd43eed150` / 187361B (`manifest-sha256.txt`, `manifest-bytes.txt`, `machine.json`, `packaging-report.md` observed).
- `complete-selection-scaling-409.patch`: SHA256 `76ac1318cd58311a5a7c0d924ee26b2bdff68dc815e75014a1aacd517e51fd6b` / 5691014B (`patch-sha256.txt`, `patch-bytes.txt`, `machine.json`).
- Delta: 143 names = 58M+85A / 0D (`gen-counts.json`, `gen-diff-*`). Old141 (57M+84A) wholly included; +1M `scripts/survey_review_attention_v2.py`, +1A `tests/test_selection_scaling_repair_v2.py`, LOW still A new SHA `fd788b74…`, runner/base still M new SHAs.
- Modes (separate domains): Git 773×`100644`→physical `0o664` + 1×`100755`→`0o775`, mismatch 0 (`packaging-report.md` §FULLVERIFY-OK, reviewer machine `mode_mismatch:0`). Do not conflate Git mode with physical mode.
- Proof: `.rephase-1-editorial-runtime/selection-scaling-packaging-20261116T031000Z/proof-copy/candidate-partial-b40de60` (`.git` +774). Saved `proof-restore689-exit 0`, `RESTORED 689/689`, `apply --check 0`, `apply 0` with whitespace preserved (`diff-check 2`), `FULLVERIFY-OK` (`CAND 774 GEN 774 PROOF 774 MANIFEST 774`, `mismatch CG/CP/CM/PM 0`, `delta M58 A85`). Inodes differ, no hardlinks/alternates/commondir, inert origin, no symlinks/`160000` gitlinks. Observed via packaging report + final-implementation-review-machine `delivery_direct409`; no re-execution here.
- 5 pins (final bytes bound): `survey_review_attention_v2.py` `10126da7482ff5203aa47663c5795ff96c14a452b67ed60b74d690a86d0e5718`/7796B, `survey_architecture_v2_base.py` `b3cd4a95f5123fbf34150bcd09921f035d12480cdaa69382fc58f4b55b8133c0`/51050B, `survey_research_authority_v2.py` `fd788b7444e5c38988d9946eec2542e35c5b9671e1bfaf9cddac5420120e5bf1`/309483B, `run_selection_architecture_v2_interactive.py` `b16c47599856919a38367aa412889baef8df02aeaf3325048e3796c5921869c7`/50865B, `tests/test_selection_scaling_repair_v2.py` `a21f5949434a3a7b787df13556d9ff4cf559d41529c6ef27bf46258dc952ba18`/49973B.
- Reuse scope: prior independent reviewer hashed all 774 across author/real/GEN/PROOF vs manifest (0 missing/mismatch). This mapping reuses those hashes as bounded evidence; no fresh full-774 re-hash in this action. Actual hash needed for any future stage execution must be re-observed at execution time (State/Profile/CP/artifact re-hash + `repository_commit_sha`), not carried forward as PASS transfer.

## 3. Both States / init480 / Profiles (file-observed, no State write)

W34 `sources/2026-W34/production-state.json` (4162B, SHA `a8586351b096fda65793dfc20604fae9404f9e9ea06e164c3b9f9c72b576e47d` per prior machine; file parsed here for lifecycle/history, hash reused):

- `lifecycle_state: EVIDENCE_REVIEWED`, `research_profile: WEEKLY`, `publication_profile: WEEKLY_MAGAZINE`, `issue_id: 2026-W34`.
- `profile: {path: sources/2026-W34/production-profile.json, sha256: 2a8c3089cec29eb64e121cdf0429eed38670df704ebe955079751198557cfeb1}`.
- `contract`: pipeline `3adfbda22131eac4017ef867aef2ebb2f346f884731c4ea8343e9062392eabd5`, quality `b5b955d524fb438c0f1b2c9490bea1da2083e79028d67a55ca424bbfc20f2958`, research `666f8a064b190ffd35216e26d6fdf2dd0fa932cac7b1b0d6448e262ded77b9a8`, publication `99adff93ff443e02bdcce639ce5fc4d4c959ee45a804da70efc4277db57fdddb`.
- `implementation: {repository_commit_sha: 480823560c0c26ed2e5baa18e0e79a22b2839a27, orchestrator_version: survey-production-core-v2/0.15-postintegration-transport-thematic}` (init provenance, not current 3231 tool identity; stage checkpoint will pin current tool separately).
- `human_gates: {architecture_review: pending, publication_preview: pending}`, `human_gate_provenance: {architecture_review: null, publication_preview: null}`, `target_gate: ARCHITECTURE_REVIEW`, `next_action: stage:selection`, `terminal_reason: null`, `exception_gate: {status: inactive}`.
- `machine_checkpoints`: discovery/screening/evidence/materiality/completeness `passed`, selection/architecture/draft/validation/publication_preview/freeze/release `pending`. `checkpoint_provenance`: discovery `3c64e40b…`, screening `4d3221d3…`, evidence/materiality/completeness same triplet `73ab28ea79da8bb13d7083d30eda7fa3188f060f0dbaa96a65e2407daae3ac48` at `sources/2026-W34/research/v2/acceptance-revisions/w34-repaired-20261112-r2/checkpoint/record.json`, selection/architecture/draft/validation/publication_preview/freeze/release `null`.
- `legacy_compatibility: {mode: NON_AUTHORITATIVE_READ_ONLY, legacy_state_path: sources/2026-W34/pipeline-state.json, legacy_state_present: false, legacy_state_sha256: null}`.
- `history` length 4 = index of EVIDENCE_REVIEWED: `null→ISSUE_INITIALIZED @48082356… 2026-08-25`, `ISSUE_INITIALIZED→DISCOVERY_COLLECTED @48082356…`, `DISCOVERY_COLLECTED→CANDIDATES_NORMALIZED @48082356…`, `CANDIDATES_NORMALIZED→EVIDENCE_REVIEWED @e84a82aca000c990597ea8cf60f548e2ff187bd1 2026-11-05`. Init480 preserved, no repin.

SP `sources/SP-efficient-llm-2026/production-state.json` (4266B, SHA `38a6341107a401128d32537cda101321b42b5ec9088d07baba43b2adc4014bde` reused):

- `lifecycle_state: EVIDENCE_REVIEWED`, `research_profile: THEMATIC`, `publication_profile: LONGFORM_SPECIAL`, `issue_id: SP-efficient-llm-2026`, same pending gates/target/next/terminal/exception shape, same passed/pending checkpoint shape.
- `profile: {path: sources/SP-efficient-llm-2026/production-profile.json, sha256: aff05fd573ce873afa24c0ede26c2b4591ee28b7048c9ed528e8fc389ed8ee45}`.
- `contract`: pipeline/quality same as W34, research `0f575e6d97caec72b2bf8b7f6b78a562d97ca67b2071193417b968ba3d73e6e8`, publication `a6859559dd1b9d42ab8fb4402b74b7bdd8611dbe65c8e02a7b022b545c20f4eb`.
- `implementation.repository_commit_sha: 48082356…` same init provenance.
- `checkpoint_provenance` triplet `2a528ed533010da6acc9efaef0e24fb59be62417724b00919e0c2f6983fec9f5` at `sources/SP-efficient-llm-2026/research/v2/acceptance-revisions/sp-repaired-20261112-r2/checkpoint/record.json`, others same shape. History length 4 with same init480 + `CANDIDATES_NORMALIZED→EVIDENCE_REVIEWED @e84a82ac… 2026-11-05`.

Profiles file-observed:

- W34 `production-profile.json` (2371B, `2a8c3089…` reused): `research_profile: WEEKLY`, `publication_profile: WEEKLY_MAGAZINE`, `paths: {source_root: sources/2026-W34, survey_root: surveys/weekly/2026-W34, work_branch: weekly/2026-W34-v2-work}`, research_scope question/inclusion/exclusion/scope_dimensions/initial_obligations (weekly:current-relevance/technical-significance/carry-over), `temporal_policy: {mode: ROLLING_WINDOW}`, contract binds same pipeline/quality/research/publication SHAs above.
- SP `production-profile.json` (13748B, `aff05fd5…` reused): `research_profile: THEMATIC`, `publication_profile: LONGFORM_SPECIAL`, `paths: {source_root: sources/SP-efficient-llm-2026, survey_root: surveys/special/efficient-llm-2026, work_branch: special/efficient-llm-2026-work}`, 12-dimension EFF-O01…O12 scope + 2026 capstone + benchmark methodology, `temporal_policy: {mode: OPEN_HISTORY_AS_OF, as_of: 2026-09-21T16:10:00Z}`.

## 4. PREARCH CP / completion / guard absent / typed 4 refs

- CP files exist: W34 `…/w34-repaired-20261112-r2/checkpoint/record.json` (6054B, `73ab28ea…`), SP `…/sp-repaired-20261112-r2/checkpoint/record.json` (6300B, `2a528ed5…`), both `kind: PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1`, `reason: REVIEWED_ACCEPTED_UPSTREAM_CORRECTION`, `operation: {from_state: EVIDENCE_REVIEWED, to_state: EVIDENCE_REVIEWED}`, `producer_boundary: {from_state: CANDIDATES_NORMALIZED, to_state: EVIDENCE_REVIEWED}`, `checkpoints: [evidence, materiality, completeness]`, 4 NamedRefs, lineage `parent_checkpoint/original_anchor/supersedes`, SizedRefs `before_state/request/retention_plan/proof/decision/report` + `before_checkpoint/parent_checkpoint/original_anchor/profile`. File head verified for W34 (same shape for SP per prior machine).
- Guard absent: `DM022_GUARD_REL = orchestration/v2/acceptance-revision.guard.json` (`survey_research_authority_v2.py:64`). Glob `acceptance-revision.guard.json` under both `sources/2026-W34/orchestration/v2` and SP returns no file; `*.guard.json` returns none. Passive `require_no_active_guard`/`require_research_operation_ready` would see absent, but this mapping does not invoke them.
- Completion: prior machine records active completion `LIMITED` (W34 71532B `e8c432dd…`, SP 33683B `d67f7f83…`; profile-completeness `d869027a…`/`b4378609…`). `require_research_operation_ready` for PREARCH same-triplet additionally requires FULL completion verification (EXACT receipt schema, COPY-derived `expected_after` recompute W34 `a8586351…`/SP `38a63411…`, retained-inventory bind, LIVE triplet + FULL graph, seven_plan vs inventory vs slots with legitimate-regeneration tolerance). No completion bypass claimed here.
- Typed 4 refs (prior machine 8/8 match, reused): W34 evidence `eef77479…`/126592B, views `3727485a…`/159502B, ledger `066230f4…`/186214B, completeness `d869027a…`/71532B; SP evidence `7f04e9ad…`/49237B, views `45d60f9f…`/64222B, ledger `5cf81f8f…`/66850B, completeness `b4378609…`/34249B (note SP completeness active bytes 34249B vs retained completion receipt 33683B are distinct records; do not conflate).

## 5. All 7 outputs + frozen inputs / archive / audit pins (per edition, no stage advance)

Directory-observed: each `sources/<edition>/` holds top 5 (`candidate-matrix-v2.json`, `candidate-selection-v2.json`, `architecture-v2.json`, `architecture-review-summary-v2.json`, `architecture-review-attention-v2.json`) + `orchestration/v2/interactive/selection-architecture-input.json` + `selection-architecture-audit.json` = 7. Prior independent output review binds bytes/SHA (reused, 13/14 SHA +14/14 sizes; SP audit own-SHA corrected to 64hex):

- W34: matrix 683098B `f4469c85…`, selection 375063B `f3a5000f…`, architecture 24447B `9a76294e…`, summary 314350B `1b7f6076…` (`readiness.status: READY_FOR_ARCHITECTURE_REVIEW`), attention 18437B `d68b5f31…` (`total 770 shown 50 overflow 720`), input archive 378396B `15375476…` == frozen, audit 1436B `61d6a0bc…` pins all 6.
- SP: matrix 239359B `2f62e2a8…`, selection 76603B `4e6884d6…`, architecture 33219B `4af84ab3…`, summary 67700B `d0092e13…` (`READY_FOR_ARCHITECTURE_REVIEW`), attention 15918B `482f3c21…` (`total 65 shown 50 overflow 15`), input archive 72613B `072f90b6…` == frozen, audit 1530B corrected `ad5474dafb79276d41a580aa48c394757195b7fe53a60bcd3092498254d15449` (superseded 61hex `ad5474…8254d…` do not use), pins all 6.
- Frozen packet inputs (exact bytes, no repin): W34 `w34-selection-architecture-input.json` 378396B `15375476…`, SP `sp-selection-architecture-input.json` 72613B `072f90b6…` (real-rehearsal README + audit `interactive_input.{path,sha256}` match).
- Assignments/packages/roles/page/boundaries/summary/attention (prior binding, reused): W34 409 assignments (45 SELECTED/364 HOLD, PRIMARY 24/SUPPORTING 21, 5 packages, pages 15target/16max, boundaries 97 non-empty, major-dests 399/residual 5/LIMITED); SP 160 (130 SELECTED/30 HOLD, PRIMARY 14/SUPPORTING 116, 9 packages, pages 60target/75max, boundaries 199 non-empty, major-dests 160/residual 5/LIMITED); audit `outputs.{candidate_matrix,candidate_selection,issue_architecture,architecture_review_summary,architecture_review_attention}` + `interactive_input` SHA bind; `human_review: {reviewed_by: null, reviewed_at: null, review_reference: null}` in architecture (no approval invented).
- Both States remain `EVIDENCE_REVIEWED` with `selection/architecture: pending/null`; generation is not stage acceptance or Human approval. Attention truncation explicit (shown 50 is not complete review of 770/65).

## 6. Prior review reuse + actual-hash boundary

- Reused as explicitly scoped evidence: `final-implementation-review` §§10–11 `BOUNDED_IMPLEMENTATION_PASS` + §12 `BOUNDED_IMPLEMENTATION_CLOSEOUT_PASS` (documentary binding, no fresh full773 runtime cert), `independent-real-output-review` F1–F11 `GO_TO_SEPARATE_VERIFICATION_PACKAGING` with SP audit §10 correction, `real-rehearsal` wall 836s/148s + exit/stdout/stderr/PID/missing-argv/env/CPU/rchar limits, `regression-supplement` old773 parent 2 ERROR vs final774 adapted 4 + equivalence `7ff77fa3…`/`df159445…`, `current-proof` Weekly70. No mechanical PASS transfer; substantive Selection/Architecture dossier still open per resume README §§2–3.
- Actual-hash rule for new entry: this packet records only file-observed identities + reused prior hashes; it does not create fresh full-774/state/CP/output re-hashes. Root stage execution must re-observe `repository_commit_sha`, State/Profile/contract, CP/artifact re-hash, `CORE_STAGE_CONTRACT` report, and checkpoint/State bytes at execution time.

## 7. Permitted write-set, stops, blocker

- Permitted in this resume unit (README §3): packet-local `continuation-observation.md + machine.json` (this file) and `normal-stage-operation-map.md + machine.json`; packet-local reviewer findings/dossier drafts using retained authorized captures only. No source/State/canonical/output/guard writes, no new source commit, no Production action, no R4/Draft/PDF/Human decision, no reconstruct Git/status/log/HEAD/Commit readback, no broad DB search, no worker subagents.
- Stops: stop unexpected failures and return before retry (prior unauthorized local retry with `-m` after `No module named 'scripts'` is not precedent); no hand-editing State, canonical overwrite, or automatic regeneration to recover counts; no new network fetch (reuse retained captures); no `core.transition_state`, manual State, or fake provided review; no inferring remote/Production writes from continuation plan.
- Blocker: none for operation-map completion. Substantive Selection/Architecture dossier + fresh seven-point R4 remain open; `Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN`. Map must close before root stage execution (see `normal-stage-operation-map.md`).
- Human Commit Point — stop; ordinary Commit/Push Human-owned.

(End of file)
