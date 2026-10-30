# Owner-B B2 final prepublish correction — entry+prepublish on every B mutating write

2026-10-29. Owner B (12 assigned scripts + B tests only, per `astra-implementation-coordination.md`).
Human continuation without Commit readback; no ordinary commit/push, no Human readback,
no network, no Gitconfig/cleanup. Previous B invocation failed with `response.failed(server_error)`
before meaningful return; inspected own current files (`candidate-work` agent `b6506a8b` → `257d4519`
→ current `647b0f36`) and narrowed active child to avoid duplicate (General owns
`tests/dm022_late_guard_fixture_v2.py` + selection/C2 late-guard families; B owns B12 + B tests only,
self-contained injector, `test_b_*` method names, no regex early-bad-fixture).
All other root runtime writers idle (TEST-only C1/C2 parallel, no B-file edits).
This is implementation correction only; no author acceptance, no premature CommitPoint,
no old PASS transfer. Runtime frozen `60aaaee` SOURCE PASS + both-route full runs preserved
as older binding; source changed (`agent` + `orchestrator`) requires affected confirmation later.

Working source: `.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/candidate-work`
(original final93 proof-copy untouched). Mandatory roots: `astra-final-runtime-gap-resolution.md` §1
(actual snapshot `survey_agent_control_v2.py:2227–2486` ENTRY ONLY → now prepublish),
late-guard report `normal-writer-late-guard-evidence.md` (B ENTRY ONLY, not prepub), contract `a345bb95`
INCLUDING §11, precode ROOT `0425c530` INCLUDING §5, R4 40 rows + 5 schemas, R5 families, R6 roles.

## 1. Actual code pins (candidate-work, after B2 edits)

All paths relative to `candidate-work`. No cross-owner file edited (A/C1/C2 untouched).

- `scripts/survey_agent_control_v2.py` `647b0f3640b421f729e7cc49539dc0caa5c8864db59a37e6ed3fe01989580009`
  (prev snapshot `b6506a8b3344`, prev failed-attempt `257d4519d187`; this fix adds revalidate entry+2 prepublishes)
- `scripts/survey_human_gate_v2.py` `447ac7c80a18a0a6c747581dc0f7a8f35f3de0dd8854fa608ba0fcd504f04f0c`
  (prev snapshot `19f3e1e35842`; failed-attempt adds `_write_review_record(state_path)` + 3×3 prepublishes, preserved)
- `scripts/survey_orchestrator_v2.py` `491888fe2d089edb1bef8a8cfa5bad942438148f9b630ac4cf18610a27a26b76`
  (prev snapshot `9d0cc3b3aea7`; failed-attempt adds entry+prepublishes, this fix adds failure-result prepublish 721)
- `scripts/survey_core_execution_bridge_v2.py` `2fd8a6a24569333ce3a1ecabd4779fa19dc84ba4f79be6d380f47422e8a1f9ec`
  (prev snapshot `f7bffbeef8a5`; failed-attempt adds reviews+receipt prepublishes, preserved)
- `scripts/survey_stage_validation_v2.py` `ec15f5ba6b0a15162cb42543b15de63ca6ca8581ff63c8ec339229b437867d9c` (unchanged, entry+prepublish already)
- `scripts/run_selection_architecture_v2_interactive.py` `553bf22bb7d218af` (unchanged, 7-slot entry+7 prepublishes)
- `scripts/run_evidence_v2_interactive.py` `949a124838d953dc` (failed-attempt adds 3 prepublishes: 694/727/805, preserved)
- `scripts/run_drafting_synthesis_v2_interactive.py` `ad6cdea70a35d412` (unchanged, entry+5 prepublishes)
- `scripts/survey_drafting_v2.py` `4f332258b5801d02` (no canonical writes; NEW optional R4 refs, unchanged)
- `scripts/survey_drafting_v2_base.py` `2fad48283609c2db` (pure + CLI outputs only, no canonical guard, unchanged)
- `scripts/survey_handlers_v2.py` `946e2671b2fcf0c7` (validators, no writes, unchanged)
- `scripts/survey_architecture_v2_base.py` `ac52c842afa12c92` (pure + CLI outputs only, unchanged)
- `tests/test_dm022_prearch_b_ordinary_consumers_v2.py` `bc0d92cac9c0a513` (23 tests, unchanged in this turn)
- `tests/test_dm022_b_late_prepublish_v2.py` `5c4f4cdd04948b4d0add23fb21e5075e5617cc8bd5aad43131eeaca5cdae2ac3`
  (NEW in failed attempt as broken 1-test `aacc7a70`; this turn rewrites to 10 meaningful tests, self-contained)

No new runtime module (A2 LOW/HIGH/schemas untouched). `diagnostics/public validate_agent_state` remains
guard-free (allows HIGH post-read under held guard). No strengthening of global Source validation beyond
selected map, no generic verified ctx. All passed role/4ref/epoch/refcount conditions preserved
(23 ordinary tests still PASS, see §3). Atomic rollback/global concurrency not selected;
existing owner-aware cleanup preserved (revalidate rolls back record on State failure, approve allows
approval prefix on second State refusal, no global atomicity claimed).

## 2. Source write inventory — explicit function→write-site→guard-site (no grep counts)

`_require` = `_require_dm022_ready` (`agent`) / `_dm022_require_ready` (`human_gate/orchestrator/stage/bridge/runners`)
= FULL `low.require_research_operation_ready(repo_root,state_path)` (entry + immediately before each canonical
authority publish, no caller-owned guard bypass). Diagnostics (`validate_agent_state`, `_validate_checkpoint_record`,
`_resolve_checkpoint_artifact`, `resolve_active_evidence_views`, `_current_pending_gate`, pure loaders) stay guard-free.

### Agent (`survey_agent_control_v2.py`)

| Function | Canonical write site(s) | Guard site(s) (entry + immediately before) |
|---|---|---|
| `build_stage_checkpoint:2227` | `core.write_json(path,payload):2300` checkpoint | entry `2242` + prepublish `2295` |
| `advance_with_checkpoint:2304` | `core.write_json(state_path,updated):2373` State | entry `2311` + prepublish `2372` |
| `approve_architecture:2377` | `core.write_json(approval_path,approval):2450` approval file; `core.write_json(state_path,updated):2462` State | entry `2390` + prepublish `2446` (approval) + prepublish `2461` (State; approval prefix allowed) |
| `approve_publication_preview:2466` | `publication.build_preview_approval(...)` (delegated C2 guarded builder entry 2123/prepublish 2161, exact call path `survey_agent_control_v2.py:2499` → `survey_publication_v2.build_preview_approval`; wrapper relies on checked child boundary, tested) + `core.write_json(state_path,updated):2513` State (wrapper own) | entry `2481` + prepublish `2512` (State; child approval prefix allowed) |
| `revalidate_publication_surface:2972` **(B2 fix)** | `_exclusive_create_record_bytes(record_path,...):3241` record; `_atomic_replace_state_bytes(state_path,...):3252` State | entry `3004` + prepublish `3247` (record) + prepublish `3263` (State; owner-aware rollback deletes record, only guard remains) |
| `_verify_preserved_provenance:2517` | none (validates preserved bytes + new revalidation record downstream, never State triplet) | n/a (detached proof, no operational READY; R1 never adopts research) |
| `validate_agent_state:919`, resolvers/validators | none (diagnostic, no canonical publish) | n/a (guard-free, allows HIGH post-read under held guard) |

### HumanGate (`survey_human_gate_v2.py`)

| Function | Write site(s) | Guard site(s) |
|---|---|---|
| `_write_review_record:411` (helper, own writes) | `core.write_json(record_path,record):429` review record; `core.write_json(index_path,updated_index):450` index | prepublish `428` (record, when `state_path` threaded) + prepublish `449` (index; record prefix allowed) |
| `record_architecture_approval:702` | `agent.approve_architecture(...)` (delegated exact child entry+prepublish, tested) + `_snapshot_approval(...)` snapshot file (via `write_bytes`) + `_write_review_record(...,state_path):766` review/index | entry `718` + prepublish `742` (snapshot) + prepublish `765` (review/index; agent+snapshot prefix allowed) |
| `record_publication_preview_approval:770` | `agent.approve_publication_preview(...)` (delegated exact child) + snapshot + `_write_review_record(...,state_path):833` | entry `786` + prepublish `810` (snapshot) + prepublish `832` (review/index) |
| `invalidate_pending_gate:1225` | cleanup `path.unlink()` loop + `core.write_json(record_path,record):1391` record + `core.write_json(state_path,updated):1395` State | entry `1258` + prepublish `1377` (cleanup) + prepublish `1390` (record; cleanup prefix) + prepublish `1394` (State; cleanup+record prefix) |
| `request_changes:1417` (covers `request_architecture_revision:1509`, `request_publication_preview_revision:1537` via exact delegation) | `_write_review_record(...,state_path):1490` review/index + cleanup unlinks + `core.write_json(state_path,updated):1502` State | entry `1443` + prepublish `1489` (review/index) + prepublish `1494` (cleanup; review prefix) + prepublish `1501` (State; review+cleanup prefix) |
| `_current_pending_gate:461`, `_validate_gate_pending:454` | none (diagnosis) | n/a (guard-free) |

### Orchestrator (`survey_orchestrator_v2.py`)

| Function | Write site(s) | Guard site(s) |
|---|---|---|
| `execute_action:664` | `core.write_json(result_path,result):718` failure result **(B2 fix: added prepublish `721`)**; `_write_validation_attestations(...)` attestations (own) + `_commit_state_and_result(...)` State+result | entry `667` + prepublish `721` (failure result) + prepublish `726` (attestations/outputs) + prepublish `744` (State+result; attestation prefix allowed) |
| `apply_architecture_approval:782` | `core.write_json(approval_path,approval):867` approval file + `_commit_state_and_result:896` State+result | entry `788` + prepublish `866` (approval) + prepublish `899` (State+result; approval prefix) |
| `apply_publication_preview_approval:900` | `publication.build_preview_approval(...)` (delegated C2 guarded child, exact call path) + `_commit_state_and_result:977` State+result (wrapper own) | entry `917` + prepublish `980` (State+result; child approval prefix) |
| `plan_action:388`, `write_action_spec:483`, `execute_current:981`, `advance_to_gate:1029` | `write_action_spec` planning specs under `orchestration/specs/` (non-canonical planning, not authority) + `execute_current/advance_to_gate` delegate to `execute_action/apply_*` (checked child boundaries) | n/a (planning, no canonical authority publish; mutating path delegates to checked `execute_action`/`apply_*`) |
| `_commit_state_and_result:640`, `_write_validation_attestations:543` | `core.write_json(state_next,...):649` + `core.write_json(pending_result,...):653` + `core.write_json(path,payload):572` attestations | covered by caller prepublishes (`726/744/899/980`); no independent entry (internal helpers, exact caller boundaries identified+tested) |

### Stage (`survey_stage_validation_v2.py`)

| Function | Write site | Guard site |
|---|---|---|
| `validate_stage:852` | `core.write_json(output_path,report):906` report | entry `869` + prepublish `888` |
| `_evidence_basis:476`, `_selection_basis:542`, `_prior_artifacts:328`, `_current_artifacts:426` | none (resolvers/validators; pure historical stays guard-free) | n/a (diagnostic; mutating callers (`validate_stage`) enforce READY) |

### Bridge (`survey_core_execution_bridge_v2.py`)

| Function | Write site(s) | Guard site(s) |
|---|---|---|
| `_advance_stage:373` | `_write_reviews(...):415` own reviews (`core.write_json(reviews_path,...):348`) + `agent.build_stage_checkpoint` + `agent.advance_with_checkpoint` (delegated exact children entry+prepublish, tested) | entry `384` + prepublish `414` (own reviews; delegates rely on checked child boundaries) |
| `execute_request:508` | `core.write_json(receipt_path,receipt):572` receipt (bridge own) + `_advance_stage` / `_human_gate_operation` (delegated exact children) | prepublish `571` (receipt; delegates rely on checked child boundaries; no entry (derives `state_path` late from request), exact call path `_advance_stage:384` → `execute_request:571` tested) |
| `_human_gate_operation:436` | none (delegates to `human_gate.record_*/request_*` exact checked children) | n/a (no own write; relies on checked delegate boundaries) |
| `_initialize:245` | `core.initialize(...)` Profile/State (new-issue creation, requires absent) + `execution_record.initialize` | n/a (initialization, requires absent canonical files; not normal regeneration; unmapped for guard – return to Astra before broadening if guard required for new-issue path) |
| `_write_reviews:325` | `core.write_json(reviews_path,...):348` | covered by caller prepublish `414`; no independent entry (internal helper) |

### Runners (B-owned ordinary consumers)

| Runner | Write sites (canonical) | Guard sites |
|---|---|---|
| `run_selection_architecture_v2_interactive.run:243` | 7 slots: `candidate-matrix:315`, `candidate-selection:365`, `architecture:430`, `review:443`, `attention` (via `build_attention`), `archive` (`shutil.copy2`), `audit:459` | entry `260` + prepublish `316/362/427/440/444/451/456` (each slot; earlier slots allowed as prefix, audit no-overwrite) – General 7× PASS preserved |
| `run_evidence_v2_interactive.run:597` | `accept_evidence_results` (evidence-acceptance), `accept_edition_views` (views), `ledger:build_materiality_ledger`, `completeness:795`, `_archive_input` (archive/audit) – temp cards/views under `temp/` are non-canonical | entry `623` + prepublish `694` (evidence) + `727` (views) + `748` (ledger) + `764` (completeness) + `805` (archive/audit) |
| `run_drafting_synthesis_v2_interactive.main:192` (`_upstream:66` entry) | `package:219`, `result:226`, `synthesis_input:232`, `synthesis_result:245`, `archive:249` | entry `81` (`_upstream`) + prepublish `218/223/229/242/247` (each; earlier prefix allowed) |
| `survey_drafting_v2.py`, `survey_drafting_v2_base.py:540/370` (`derive_draft_package_from_accepted_state`), `survey_handlers_v2.py`, `survey_architecture_v2_base.py` | none (pure/content cores + CLI `output` writes to caller-specified non-canonical paths) | n/a (caller entry enforces READY + R4 refs; pure stays guard-free) |

If new unmapped writer outside these 12 files is found, return exact call/eligibility to root before broadening
(no broadening here; `_initialize` new-issue path noted above as unmapped initialization, not normal writer).

## 3. Tests — meaningful fault tests (healthy positive + late guard, REAL helper, no mock)

Private frozen copy: `/tmp/dm022-b2-private-20261029T174500Z/` (tar byte-copy from `candidate-work` after edits,
excluding `__pycache__/*.pyc`, `.git` byte-copied (no hardlinks/alternates), `PYTHONDONTWRITEBYTECODE=1`,
`unset GIT_*`, `/usr/bin/python3` 3.14.4). Workspace packet has no GitDB/pycache. No live candidate tests;
all runs in private copy only. Independent GitDB meaningful test source commits with process identity
(`Synthetic DM022-B2 Fixture`, `b2-late-guard@example.invalid`, inert `example.invalid` origin) for fixture DBs
where git init required (full-lifecycle helpers do `init_independent_git` internally); no config/empty/hardlinks/
root objects/ordinary candidate/reconstruct commit/network/Human readback/cleanup. `fix` helpers own fixture
lifetime (no hardlinks, `ignore=__pycache__`).

- NEW `tests/test_dm022_b_late_prepublish_v2.py` (B-owned, self-contained `_Injector` wrapping REAL
  `low.require_research_operation_ready`, exact `file/fn/line` outer matching via `inspect.stack()[2]/[3]`,
  `entry_fn` support for cross-fn (bridge receipt), synthetic owned guard `{"phase":"TEST","nonce":...}`,
  ANY present refuses, no mock PASS, no broad `Exception`, no early-reject bypass, `test_b_*` names to avoid
  duplicate with General's `test_dm022_normal_writer_late_guard_v2.py`):
  - `test_b_agent_build_prepublish` (entry 2242/target 2295, LEGACY thematic fixture, NEW checkpoint, `new=={guard}`)
  - `test_b_agent_advance_prepublish` (2311/2372, LEGACY, State bytes unchanged, `new=={guard}`)
  - `test_b_agent_approve_arch_approval_file` (2390/2446, PREARCH via `_full_route_witness` + build+advance to ESTABLISHED, no approval, `new=={guard}`)
  - `test_b_agent_approve_arch_state` (2390/2461, PREARCH, approval prefix allowed, State unchanged, `new=={approval,guard}`)
  - `test_b_agent_approve_preview_state` (2481/2512, durable VALIDATED_DRAFT + NEW canonical candidate + advance to RELEASE_CANDIDATE, child approval prefix allowed, State unchanged)
  - `test_b_agent_revalidate_record` (3004/3247, synthetic VALIDATED_DRAFT with drift via `test_survey_publication_revalidation_v2.Fixture`, no record, `new=={guard}`)
  - `test_b_agent_revalidate_state` (3004/3263, synthetic, State unchanged, rollback deletes record, `new=={guard}`)
  - `test_b_stage_validate_prepublish` (869/888, chain + production discovery acceptance + git init, NEW report, `new=={guard}`)
  - `test_b_humangate_record_arch_prepublish` (718/765, LEGACY ARCH pending via human-gate helpers + work-branch review commit, snapshot+agent prefix allowed, review record `gates/reviews/architecture-r1.json` absent)
  - `test_b_humangate_request_prepublish` (1443/1501, LEGACY ARCH pending, review/index absent, `guard` present)
  - Raw: `/tmp/dm022-b2-late-raw-20261029T180000Z.txt` SHA256 `59f6549e091f906e3da338644043ef0f9353f2e39555d48933db11be35f00182`, 30 lines, `Ran 10 tests in 98.920s OK`, exit 0.
- Existing `tests/test_dm022_prearch_b_ordinary_consumers_v2.py` (B-owned, 23 tests, strict reason/operation/boundary/SizedRef/wrong-family/triplet/7-slot/guard-split/legacy/drafting/R1, no stub-LOW):
  - Raw: `/tmp/dm022-b2-ordinary-raw-20261029T180000Z.txt` SHA256 `afed431d5a10b0fbcf44d6e45401c73b71871b8eb0c2038f4fe687cb64ec2468`, `Ran 23 tests in 73.507s OK`, exit 0.
  - Preserves all passed role/4ref/epoch/refcount conditions; B2 source changes (revalidate entry+2 prepublishes, orchestrator failure-result prepublish) do not break any (23/23 PASS in private copy with new source).

Total B2: 10 new + 23 existing = 33 meaningful tests, all PASS in private copy with new source.
No author acceptance claimed; affected confirmation + independent implementation review remain required
(source changed `agent`+`orchestrator` vs frozen `60aaaee`, so old SOURCE PASS + both-route full runs stay as older
binding only, not transferred).

## 4. Remaining late-guard families (OPEN, no waiver, exact missing)

Source entry+prepublish is complete for all B writes (§2, verified via exact lines, not grep counts).
Tests above prove previously ENTRY ONLY gaps (`build/advance/approve_arch/approve_preview` per `astra-final-runtime-gap-resolution.md` §1)
plus `revalidate` (new B2 fix), `stage`, `human_gate record/request` (presentation/review/approval/invalidation pattern).
Still OPEN for meaningful fault-test proof (same REAL-helper pattern, healthy+fault, exact target/entry, counters,
immediate outputs with allowed prefixes) – same pattern as above, no new source needed:

- `human_gate.invalidate_pending_gate` (1258/1377/1390/1394): needs ARCH pending with FULL `architecture-review-summary`
  (all research fields `discovery/screening/evidence/materiality/selection/completeness/architecture`, not minimal
  `_architecture_files` thesis-only) + valid `work_branch` head (via `_snapshot_review_commit`); current `_hg_arch_pending`
  (minimal summary) fails gate-surface `missing 'architecture'` before prepublish (setup, not code defect).
- `human_gate.record_publication_preview_approval` (786/810/832) + `request_publication_preview_revision`:
  needs RELEASE_CANDIDATE pending with valid preview gate surface (candidate + ... via `_reach_publication_gate`,
  fast synthetic, no DM022) + work-branch review commit; same REAL-helper pattern as `record_arch` (entry+prepublish,
  snapshot prefix, review/index absent).
- `orchestrator.execute_action` (667/721/726/744): needs EVIDENCE_REVIEWED + valid `plan_action` spec + `HandlerRegistry`
  (via `test_survey_orchestrator_v2.sandbox` + `stage_registry`, LEGACY, fast); healthy SUCCESS (attestation+State+result)
  + healthy FAILURE (failure result via failing handler, prepublish `721`) + fault at each prepublish (no result/attestation/State beyond guard+allowed prefix).
- `orchestrator.apply_architecture_approval` (788/866/899): needs ARCH pending (via `sandbox` + `advance_to_gate` to ARCH,
  LEGACY) + valid spec (via `plan_action` with observed HEAD) + approval path; same pattern (approval prefix for State).
- `orchestrator.apply_publication_preview_approval` (917/980): needs RELEASE_CANDIDATE (via `_release_candidate_pending`,
  durable+canonical candidate+advance, fast) + valid spec; child approval prefix allowed.
- `bridge._advance_stage` (384/414) + `execute_request` receipt (571, entry `384` via `entry_fn`): needs ADVANCE_STAGE request
  (via `test_survey_core_execution_bridge_v2` thematic init + advance, LEGACY, fast); healthy (NEW reviews + checkpoint+State via delegates + NEW receipt) + fault at each (no reviews/receipt beyond guard+delegated prefix).
- `run_evidence_v2_interactive.run` (623/694/727/748/764/805): needs CANDIDATES_NORMALIZED with full checkpoint validity
  (`discovery+screening` checkpoints + State `machine_checkpoints`/`checkpoint_provenance` for CANDIDATES_NORMALIZED,
  `agent.validate==[]`); current `_chain_root` gives ISSUE_INITIALIZED, `_make_evidence_reviewed_state` gives EVIDENCE_REVIEWED
  (wrong lifecycle, fails before prepublish – setup, not code); exact missing: CANDIDATES_NORMALIZED builder (same pattern as
  `_make_evidence_reviewed_state` stopped after screening, no DM022 adopt for LEGACY proof).
- `run_drafting_synthesis_v2_interactive` (`_upstream` 81 + `main` 218/223/229/242/247): needs ARCHITECTURE_ESTABLISHED +
  approved Gate + canonical accepted-evidence tree mirror + valid drafting input (via `_full_route_witness` + `_approve_...` +
  `_materialize_canonical_accepted_evidence_tree` + `_build_drafting_input`, ~30s + P1 helpers); exact missing: fresh
  ARCHITECTURE_ESTABLISHED fixture with those helpers (full witness to arch approval, not just SELECTION_COMPLETE).
- `run_selection_architecture_v2_interactive.run` 7 writes: already General 7× PASS (`normal-writer-late-guard-evidence.md`),
  no duplicate B test (narrowed to avoid duplicate).

No global CAS/crash-atomicity claimed (single-writer guarded transition only; incomplete op can have new State + old stale
files with normal writers blocked by guard; unknown State preserved, no automatic rollback/global atomicity per contract §11.3).
No genuine approval/Production (all reviewers synthetic `SYNTHETIC_FIXTURE_*`, never genuine; no W40 reproduction).
Whole NOT_READY/step4B3OPEN/audit unstarted/DM021+022OPEN; Profile/quality/adoption/savings OPEN.
Stop at Human Commit Point; ordinary Commit/Push Human-owned.

Author: Owner B2. Scope is B12 source prepublish corrections (§1 pins + §2 table) + B late-prepublish tests (§3, 10 new + 23 existing PASS in private copy).
Implementation acceptance remains with root + independent implementation review + affected confirmation on new source.
