# Owner-B2 rollback-guard resolution — no rollback writes under ANY guard

2026-10-29. Owner B (12 scripts + B tests only, no A). Unit ongoing, no author acceptance,
no premature CommitPoint, no Human readback/ordinary commit/Gitconfig/network/cleanup.
Root read `survey_human_gate_v2.py:1377-1413`: prepublish READY inside `try` can raise on new guard,
then `except` unconditionally did `record.unlink`/`state.write_bytes`/`snapshots.write_bytes` WHILE GUARD HELD.
This violates HIGH sole mutator and late-failure preservation. Fixed narrowly in B-owned files only;
existing normal unguarded rollback stays iff guard absence + known State ownership checked.
No global transaction framework, no A edits, no generic verified ctx. Late-test author helper reused
read-only (own `_Injector`, `test_b_*` names, no regex early-bad-fixture, no skip flags).

Previous B2 (`author-B2-final-prepublish-correction.md`, 10 late + 23 ordinary, late raw `59f6549e…`,
ordinary `afed431d…`) preserved; this appends actual rollback-guard changes (15 late + 23 ordinary,
late `bf4ac40b…`, ordinary `233bec90…`). Runtime frozen `60aaaee` SOURCE PASS + both-route full runs stay
older binding; source changed requires affected confirmation later.

Working source: `.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/candidate-work`.
Private frozen copy for all runs below (no live candidate): `/tmp/dm022-b2-private-20261029T174500Z/`
(tar byte-copy from `candidate-work` after all B2-rollback patches, `--exclude=__pycache__/*.pyc`,
`.git` byte-copied, no hardlinks/alternates, `PYTHONDONTWRITEBYTECODE=1`, `unset GIT_*`,
`/usr/bin/python3` 3.14.4). Independent fixture GitDBs with process identity
(`Synthetic DM022-B2*`, `b2-*-example.invalid`, inert `example.invalid` origin) where git init required;
no config/empty/hardlinks/root objects/ordinary commits.

## 1. Source pins (candidate-work, after B2-rollback patches)

- `scripts/survey_agent_control_v2.py` `d801feb679c99d2ed0839e41e6dbf91d5b1adcbeeb2a042af24f62d9c37`
  (prev B2 `647b0f36…`; this adds rollback-guard at `except:3270` — readiness check before any `unlink/replace/restore`)
- `scripts/survey_human_gate_v2.py` `101792ad8070607e8237c2e1e5ccfa1ab9f5ff1e731a4a914df91bb3ccaf3b9`
  (prev B2 `447ac7c8…`; failed-attempt prepublishes preserved; this adds rollback-guard at `except:1404`
  — no `unlink/write_bytes` under guard/unknown readiness)
- `scripts/survey_orchestrator_v2.py` `491888fe2d089edb1bef8a8cfa5bad942438148f9b630ac4cf18610a27a26b76` (unchanged from B2; failure-result prepublish `721` preserved)
- `scripts/survey_stage_validation_v2.py` `ec15f5ba6b0a1516` (unchanged)
- `scripts/survey_core_execution_bridge_v2.py` `2fd8a6a24569333` (unchanged)
- `scripts/run_selection_architecture_v2_interactive.py` `553bf22bb7d218af` (unchanged)
- `scripts/run_evidence_v2_interactive.py` `949a124838d953dc` (unchanged)
- `scripts/run_drafting_synthesis_v2_interactive.py` `ad6cdea70a35d412` (unchanged)
- `scripts/survey_drafting_v2.py` `4f332258b5801d02`, `survey_drafting_v2_base.py` `2fad48283609c2db`,
  `survey_handlers_v2.py` `946e2671b2fcf0c7`, `survey_architecture_v2_base.py` `ac52c842afa12c92` (unchanged, no canonical writes)
- `tests/test_dm022_prearch_b_ordinary_consumers_v2.py` `bc0d92cac9c0a513` (unchanged, 23 tests)
- `tests/test_dm022_b_late_prepublish_v2.py` `552bcf52f420b3fcdd6f4a681ebf68a8cae873fe7da0cf0b8519a84e486f6986`
  (prev B2 `5c4f4cdd0…` 10 tests; this adds invalidate 3 + orchestrator execute/apply_arch + revalidate State prefix fix, total 15 tests, self-contained)

No new runtime module; `validate_agent_state` guard-free preserved; no Source validation strengthening beyond selected map.

## 2. Rollback-guard fix (narrow, B-owned only)

### HumanGate `invalidate_pending_gate:1377-1413`

Before: prepublish `1377` outside `try` (good, fails before try, no rollback), but `1390`/`1394` inside `try`;
`except:1404` unconditionally did `record.unlink`/`state.write_bytes`/`snapshots.write_bytes` even when
`DM022_TRANSITION_ACTIVE` was raised by `1390`/`1394` with newly injected guard held → HIGH sole-mutator violation.

After (`except:1404`):
- First try `_dm022_require_ready(repo_root,state_path)` (read-only, no writes). If it raises (ANY guard present,
  completion mismatch when PREARCH active, unknown/unreadable) → NO rollback writes at all; re-raise original
  with preservation note (`prefix preserved (cleanup + record if any), no rollback writes under guard`).
  Prefix (cleanup deletions + record if created before fault) and all State/record evidence preserved; guard preserved.
- Only if readiness passes (guard absent + completion consistent) → verify State ownership
  (`_cur == state_bytes(original)` or `== core.json_bytes(updated)`, else unknown → preserve, no rollback),
  then existing restore (`record.unlink(missing_ok)`, `state.write_bytes(state_bytes)`, snapshots restore).
  Normal unguarded rollback preserved, no global atomicity claimed.

### Agent `revalidate_publication_surface:3270-3422` (audit, same rule)

Before: `except:3270` did owner-aware disposition (State original/new/unknown, record identity, `unlink`/`_atomic_replace`)
even when failure was `DM022_TRANSITION_ACTIVE` at `3247`/`3263` with guard held → could `unlink` owned record
while guard held (State fault previously expected `new=={guard}` only because rollback deleted prefix).

After (`except:3270`): first try `_require_dm022_ready`. If fails (guard/unknown) → NO `unlink/replace/restore` at all;
re-raise with `prefix preserved (record if created), no rollback writes under guard`. Only if readiness passes
→ existing owner-aware rollback (unknown State → preserve; `State==new` → replace back then orphan-record identity
checks; `State==original` → record identity checks then `unlink`) runs. Happy-path guards unchanged
(entry `3004`, prepublish `3247` record, `3263` State).

Other B `except`/rollback paths audited: `human_gate.request_changes` (no `try`/rollback, sequential writes, no restore —
preserves prefix naturally under guard via prepublish refusals `1489/1494/1530`); `agent.approve_*` (no rollback,
approval prefix allowed on second State refusal `2461/2512`, no deletion); `orchestrator.execute/apply_*`
(no rollback, `_commit_state_and_result` only after prepublish `744/899/980`); `stage.validate_stage`,
`bridge._advance_stage/execute_request`, runners (no `try` restore, fail-closed, no writes on refuse).
Only `invalidate` + `revalidate` had rollback writes; both now guard-aware. No `entry+prepub complete` claimed
until rollback guarded — now guarded, but closeout still requires independent review + affected confirmation
(unit ongoing).

## 3. Tests — meaningful late faults (healthy + guard-after-entry-before-target, REAL helper, no mock)

All in private copy only (no live candidate). `_Injector` wraps REAL `low.require_research_operation_ready`,
exact `file/fn/line` via `inspect.stack()[2]/[3]`, `entry_fn` support for bridge receipt cross-fn,
owned synthetic guard `{"phase":"TEST","nonce":...}`, ANY present refuses, `entry_reached`+`target_reached` asserted,
immediate full write-set snapshot (`_snapshot` bytes, not names only), `new=={guard}` or explicit allowed prefix
(approval/record/snapshot/cleanup), State bytes unchanged when target is State, record preserved (not deleted) under guard.

- `test_b_agent_build_prepublish` (2242/2295, LEGACY thematic, NEW checkpoint, `new=={guard}`)
- `test_b_agent_advance_prepublish` (2311/2372, LEGACY, State unchanged, `new=={guard}`)
- `test_b_agent_approve_arch_approval_file` (2390/2446, PREARCH via `_full_route_witness` + build+advance to ESTABLISHED, no approval, `new=={guard}`)
- `test_b_agent_approve_arch_state` (2390/2461, PREARCH, approval prefix allowed, State unchanged)
- `test_b_agent_approve_preview_state` (2481/2512, durable VALIDATED_DRAFT + NEW canonical candidate + advance to RELEASE_CANDIDATE, child `build_preview_approval` entry 2123/prepublish 2161 checked delegate, approval prefix allowed, State unchanged)
- `test_b_agent_revalidate_record` (3004/3247, synthetic VALIDATED_DRAFT with drift via `test_survey_publication_revalidation_v2.Fixture`, no record, `new=={guard}`)
- `test_b_agent_revalidate_state` (3004/3263, synthetic, State unchanged, **record prefix preserved (not deleted) + guard** — proves rollback-guard fix; previously `new=={guard}` only via buggy deletion)
- `test_b_stage_validate_prepublish` (869/888, chain + production discovery acceptance + git init, NEW report, `new=={guard}`)
- `test_b_humangate_record_arch_prepublish` (718/765, LEGACY ARCH pending via human-gate helpers + work-branch review commit, snapshot+agent prefix allowed, review `gates/reviews/architecture-r1.json` absent)
- `test_b_humangate_request_prepublish` (1472/1530, LEGACY ARCH pending, review/index absent beyond prefix — note line shift from B2 `1443/1501` due to invalidate rollback-guard lines)
- `test_b_humangate_invalidate_healthy` (full valid ARCH pending via `_arch_pending` PREARCH full summary + work-branch `refs/remotes/origin/<branch>` to HEAD + committed State (reviewed commit bytes == current), no invalid-summary preemption, NEW invalidation record + State)
- `test_b_humangate_invalidate_record_fault` (1258/1390, full ARCH, guard after cleanup/before record, no record, `new=={guard}` (cleanup deletions are prefix, not NEW), State unchanged, no rollback writes under guard)
- `test_b_humangate_invalidate_state_fault` (1258/1394, full ARCH, **record prefix preserved + guard, State unchanged, no State rollback/deletion while guard** — proves rollback-guard fix)
- `test_b_orchestrator_execute_prepublish` (667/726, LEGACY sandbox + `stage_registry`, NEW result, `new=={guard}`, no result)
- `test_b_orchestrator_apply_arch_state` (788/899, LEGACY sandbox + `advance_to_gate` to ARCH + terminal spec, approval prefix allowed, State unchanged)

Raw (packet, unique dirs, not `/tmp`-only): `notes/rephase-1-dm022-prearchitecture-implementation/evidence/b2-rollback-guard-20261029T180000Z/`
- `b2-late-15-raw.txt` SHA256 `bf4ac40bbe4171e0c9470bd93b18b0ca83fd7062b00690cadf02e3ba5d6d15f5`, `Ran 15 tests in 168.000s OK`, exit 0
- `b2-ordinary-23-raw.txt` SHA256 `233bec90f396999a4a5615743fabf942953d5ab4da9d6b12041f566691012391`, `Ran 23 tests in 74.339s OK`, exit 0
- `test_dm022_b_late_prepublish_v2.py` `552bcf52…` (15 tests)
Previous B2 raw preserved via `author-B2-final-prepublish-correction.md` (10 late `59f6549e…`, 23 ordinary `afed431d…`); this appends rollback-guard changes (15 late, same 23 ordinary with new source).

Existing B ordinary 23 tests still PASS with new source (no role/4ref/epoch/refcount regression).

## 4. Remaining B normal-write expectations (OPEN, no waiver, no skip flags, no `entry+prepub complete` claim)

Source entry+prepublish is complete for all B writes (§2 table + B2 table, exact lines, not grep counts).
Tests above prove previously ENTRY ONLY gaps (`build/advance/approve_arch/approve_preview` per `astra-final-runtime-gap-resolution.md` §1)
plus `revalidate` (new B2-rollback fix), `stage`, `human_gate record/request/invalidate` (presentation/review/approval/invalidation
with rollback-guard), `orchestrator execute/apply_arch` (own writes vs checked delegate). Still OPEN for meaningful fault proof
(same REAL-helper pattern, healthy+fault, exact target/entry, counters, immediate outputs with allowed prefixes):

- `human_gate.record_publication_preview_approval` (786/810/832): needs LEGACY RELEASE_CANDIDATE with valid seven-role validation checkpoint including `reader-surface-gate` (`_reach_publication_gate` + C2 `publication_set` seven-role binding); synthetic human-gate preview fixture gives six roles (missing gate) → fails before prepublish (setup, not B code). Durable `approve_publication_preview` State (2512, child prefix) already proves wrapper prepublish; record preview shares `_write_review_record` + snapshot pattern with proven `record_arch` (742/765) — precise call-graph checked delegate (`agent.approve_publication_preview` exact child entry 2481/prepublish 2512, tested) + same-helper (`_snapshot_approval`, `_write_review_record` with `state_path`, tested via record_arch/request).
- `bridge._advance_stage` own reviews (384/414) + `execute_request` receipt (571, entry 384 via `entry_fn`): needs `ADVANCE_STAGE` request JSON (`INITIALIZE_WEEKLY` → `ADVANCE_STAGE` chain, work_branch + source_root + operation, 5 lines) + thematic init + discovery advance (LEGACY, fast, like `test_bridge_executes_thematic_init_then_discovery_advance_end_to_end`). Own writes vs checked delegates exact: `_write_reviews` own (414, tested pattern via stage/agent), `agent.build/advance` + `stage.validate_stage` + `human_gate.record_*/request_*` delegates (all entry+prepublish tested). No skip, no fake PASS.
- `orchestrator.apply_publication_preview_approval` (917/980): needs LEGACY RELEASE_CANDIDATE with canonical orchestrator attestation (human-gate preview fixture gives RELEASE_CANDIDATE but `plan_action` expects SP001-style canonical attestation, not HG-ROUNDTRIP minimal — setup mismatch between human-gate fixture and orchestrator `verify_state_basis`, not B code). Call graph: `publication.build_preview_approval` exact child (C2 entry 2123/prepublish 2161, proven via agent preview durable test) + own State+result prepublish 980 (same pattern as proven `apply_arch` 899 with approval prefix).
- `run_evidence_v2_interactive.run` (623/694/727/748/764/805): needs CANDIDATES_NORMALIZED with full checkpoint validity (`discovery+screening` checkpoints + State `machine_checkpoints`/`checkpoint_provenance` for CANDIDATES_NORMALIZED, `agent.validate==[]`); `_chain_root` gives ISSUE_INITIALIZED, `_make_evidence_reviewed_state` gives EVIDENCE_REVIEWED (wrong lifecycle, fails before prepublish). Exact missing: CANDIDATES_NORMALIZED builder (stop `_make_evidence_reviewed_state` after screening, no DM022 adopt for LEGACY proof).
- `run_drafting_synthesis_v2_interactive` (`_upstream` 81 + `main` 218/223/229/242/247): needs ARCHITECTURE_ESTABLISHED + approved Gate + canonical accepted-evidence tree mirror + valid drafting input (via `_full_route_witness` + `_approve_...` + `_materialize_canonical_accepted_evidence_tree` + `_build_drafting_input`, ~30s + P1 helpers). Exact missing: fresh ARCHITECTURE_ESTABLISHED fixture with those helpers (full witness to arch approval, not just SELECTION_COMPLETE).
- `run_selection_architecture_v2_interactive.run` 7 writes: already General 7× PASS (`normal-writer-late-guard-evidence.md`), narrowed to avoid duplicate (no B re-test).
- `request_changes` record/index before cleanup with source ROOT history idx prevents A entry as correct (A new HIGH `f8af…` global history fix ready — B `request_changes` order `1490` review/index → `1494` cleanup → `1501` State preserved, no B change needed).

No global CAS/crash-atomicity (single-writer guarded transition only; incomplete op can have new State + old stale files with normal writers blocked by guard; unknown State preserved, no automatic rollback/global atomicity per contract §11.3).
No genuine approval/Production (all reviewers synthetic, never genuine; no W40 reproduction).
Whole NOT_READY/step4B3OPEN/audit unstarted/DM021+022OPEN; Profile/quality/adoption/savings OPEN. Stop at Human Commit Point; ordinary Commit/Push Human-owned.

Author: Owner B2 (rollback-guard). Scope is B12 rollback-guard source fixes (§2) + B late tests (§3, 15 new + 23 existing PASS in private with new source).
Implementation acceptance remains with root + independent implementation review + affected confirmation on new source (`101792ad`/`d801feb6` vs frozen `60aaaee`).
