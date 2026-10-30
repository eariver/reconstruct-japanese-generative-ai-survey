# DM022 normal-writer late-guard COMPLETION evidence — General test-author/executor

Date: 2026-10-29 UTC. General ONLY, NOT reviewer. Runtime fixed-source-bound
`SOURCEPASS` on EXACT snapshot-review `worktree764` (`snapshot-review-20261029T053058Z`,
764 files, SHA256 `60aaaee8539f69432a01d0ad72c1131b23951fd87a5531981876642d877ecee`),
pins verified in exec before/after (LOW `2aef837f…`, HIGH `3d1d87d8…`,
release `b9433b9e…`, publication `705bcee3…`, refresh `dd01fa01…`,
agent `b6506a8b…` (frozen, NOT B `647b0f36…`), human `19f3e1e5…` (frozen,
NOT B `447ac7c8…`), orchestrator `9d0cc3b3…` (frozen, NOT B `491888fe…`),
bridge `f7bffbeef…` (frozen, NOT B `2fd8a6a6…`), H `a9de2c97…`, S `b139f493…`).
B ENTRY-only fixes (`agent647b…/human447ac…` etc., B2 currently correcting
rollback late-invalidation) were NOT captured while writing (frozen source +
2 test-file overlay only, exact pins, no live B).

Read: independent-final-operation-review §§2/4/6, precode R3/R4 + oracles,
B2 `author-B2-final-prepublish-correction.md` §§1-4 (B ENTRY-only → entry+
prepublish, B2 owns B12 + B tests, General owns selection/C2 families),
durable `durable-versioned-20261029T064541Z/durable-fixture-manifest.json`.

## Method (no existing runtime/test edits, 2 files only)

- NEW `tests/test_dm022_normal_writer_late_guard_v2.py` (24 tests) +
  `tests/dm022_late_guard_fixture_v2.py` (LateGuardInjector + snapshot).
  No `scripts/` edits. Exec private byte copy
  `/tmp/dm022-late-guard-20261029T060000Z/exec/` (tar byte-copy from frozen
  worktree, `__pycache__/*.pyc` excluded, `.git` byte-copied no hardlinks/
  alternates, `PYTHONDONTWRITEBYTECODE=1`, `unset GIT_*`, `/usr/bin/python3`
  3.14.4). Packet has no GitDB/pycache. Candidate sync via direct copy
  (allowed) for test files only; runtime unchanged.
- DURABLE VALIDATED prePreview (`weekly_validated_prepreview`) + VERSIONED
  (`weekly_versioned_active_prepreview`) from durable manifest (independent DBs
  outside packet) copied NEW per fault. Fresh phase fixtures via full-lifecycle
  helpers with NEW proposal IDs (`ed-late-*`, `fixture-wk-ret-*`) to avoid
  `RET_ROOT_EXISTS`; new copy saved preparedSet before activation; reuse code
  parts legal test-only helper, not runtime.
- Evidence CANDIDATES_NORMALIZED via real public discovery+screening stage
  checkpoints (`_make_candidates_normalized_state`: `_materialize_production_
  discovery_acceptance` + `_git_init` + contract + discovery/screening reports/
  records + State `CANDIDATES_NORMALIZED` with `machine_checkpoints`/
  `provenance`/history 3 + `refresh_state_control`, `validate_agent_state==[]`,
  no faked passed without artifacts).
- Draft via `_full_route_witness` + `_approve_architecture_for` (valid ARCH+
  approved + all records) + `_materialize_canonical_accepted_evidence_tree` +
  `_build_drafting_input` (synthetic explicit reviewer, no marker hacks).
- Retention with NEW pid (`_build_finalize_scope_with_pid`, `_prepare_new_
  proposal_in_root`) to avoid `RET_ROOT_EXISTS`; P3S via fixture-code
  subprocess (`cwd=root`, packet logs to late-guards unique, no overwrites).
- Editorial healthy phases with real valid receipt/full set (prepare via real
  TinyTeX `lualatex+biber`, reviews via fixture-code subprocess for S2 binding,
  finalize/activate/resume via subprocess drivers with cwd=root); not later
  missing-error as prepublish (healthy proves REAL write, fault proves late
  refusal at exact prepublish).
- Release FROZEN fixture prior to release (no rollback): fresh freeze via
  normal public APIs from VALIDATED prePreview durable (candidate/preview/
  HumanGate approve/freeze + advances to FROZEN, REAL PDFs, no TinyTeX rebuild
  beyond prepare) stopping at FROZEN for fault API target (entry 67,
  prepublish 231, no State advance in driver, checkpoint write only).
- Wrap REAL `low.require_research_operation_ready` (exact callsite + counter,
  `inspect.stack()[2]/[3]`, entry vs prepublish by exact file/fn/line, no
  approximate counts, no authority mocks). Good actual write counterpart, then
  fault just before final READY (guard planted at target, then REAL helper must
  refuse `DM022_TRANSITION_ACTIVE`). Immediate pre/post full inventory scoped
  exact write window excluding fault injection ONLY; guard/file/partial allowed
  preserved, no business cleanup. New independent copy per actual fault;
  legitimate NEW output via API/fresh phase (no clearing accepted data).
- Preserve unique RAWs (old `raw.txt`, `raw-full-20261029T110724Z.txt` kept,
  new `raw-full-20261029T113416Z.txt` + `ed-* / p3s-*` dirs with timestamp+PID,
  never overwrite; failed-before-target fixtures fixed, not SKIP).
- No ordinary commits/Human readback/network/Gitconfig/cleanup/inherited
  mutation. Independent ownership (author, not final review).

## Result: 24 PASS, 0 FAIL, 0 SKIP (selected late-guard families)

`python3 -m unittest tests.test_dm022_normal_writer_late_guard_v2 -v`:
`Ran 24 tests in 1524.134s OK` (exit 0, PID 682928,
`2026-10-29T113422Z→115946Z`, raw `raw-full-20261029T113416Z.txt` 107 lines).
Old RAWs preserved (`raw.txt` 15 PASS, `raw-full-20261029T110724Z.txt`
25 tests 24 PASS +1 SKIP old retention). No runtime bug outside B known flags;
no source patch. Unit ongoing.

### Per-family table (actual oracles)

| Family / R4 rows | Entry → Prepublish (exact) | Healthy (NEW, real) | Fault (late, no-write) | Status |
|---|---|---|---|---|
| Selection 7 incl AUDIT (R4 row7) | `run:260` → `316/362/427/440/444/451/456` | Fresh EVIDENCE_REVIEWED WEEKLY, 7/7 slots, audit binds archive (path≠input, bytes equal), 2nd regen refuses overwrite | 7 cases, each fresh copy, inject at slot, `DM022_TRANSITION_ACTIVE`, target absent, `new=={guard}` or allowed earlier partials | **PASS×7** |
| Evidence ledger/completeness (R4 row8) | `run:623` → `742` ledger, `758` completeness | CANDIDATES_NORMALIZED (real discovery+screening checkpoints, `validate==[]`) + valid interactive input → ledger + completeness NEW | Inject 742 → ledger+completeness absent, `new=={guard}+evidence/views prefix`; inject 758 → ledger prefix allowed, completeness absent | **PASS×2** |
| Draft (R4 row9) | `_upstream:81` → `main:218` (first package) | ARCHITECTURE_ESTABLISHED+approved+canonical tree + drafting input → `draft-package.json` NEW via `main` in-process | Inject 218 (entry_fn `_upstream`) → refuse, no packages, `new=={guard}` | **PASS** |
| Retention (R4 row33) | `capture_retention:942` → `1519` | NEW pid `fixture-wk-ret-healthy` (P1+scope, no P3S yet? Actually P1+P2R+scope, NEW retained) → manifest NEW | NEW pid `fixture-wk-ret-fault` + NEW pid2 `fixture-wk-ret-fault2` in same root (NEW retained), inject 1519 → refuse, `new=={guard}` | **PASS** |
| Editorial prepare (C2) | `prepare_publication:1733` → `1783` | NEW pid `ed-late-prep-healthy` (P1+P2R+P2V+P3S, NEW proposal/retained/staged/manuscript/toolchain) + real TinyTeX build via fixture-code subprocess → `publication/build/main.pdf` NEW | NEW pid fault, inject 1783 (disposable build partial under /tmp allowed, not in snapshot) → refuse transfer, no canonical build, `new=={guard}` | **PASS** |
| Editorial finalize | `finalize_publication:2301` → `2431` (bundle) | Prepared base (one build) copy → finalize (no rebuild) writes bundle/gate/candidate/set NEW | Copy + inject 2431 → refuse, bundle absent | **PASS** |
| Editorial activate | `activate_publication:3466` → `3805` (record) | Finalized base copy → activate writes record+State NEW (State sha changes) | Copy + inject 3805 → refuse, no record, State unchanged | **PASS** |
| Editorial resume | `resume_activation:3954` → `4025` | Finalized base + orphan record copied from activate-healthy (same old State, no guard) → resume installs State NEW | Orphan + inject 4025 → refuse, State unchanged (old), record preserved (already in pre) | **PASS** |
| Publication candidate (R4 row31) | `build_candidate:1932` → `2013` | Durable VALIDATED_DRAFT REAL pdf 68035B/5pp + NEW `candidate-late-*.json` → `READY_FOR_PUBLICATION_PREVIEW` | Fresh copy + inject 2013 → refuse | **PASS** |
| Publication preview | `build_preview_approval:2123` → `2161` | Healthy candidate + NEW preview → APPROVED | Inject 2161 → refuse | **PASS** |
| Publication visual | `build_visual_review:2209` → `2245` | Healthy candidate+preview + NEW visual → PASSED | Inject 2245 → refuse | **PASS** |
| Publication freeze | `build_freeze:2294` → `2338` | Healthy candidate+preview + NEW freeze+manifest → installed | Inject 2338 → refuse | **PASS** |
| Manuscript (R4 row36) | `build_manuscript_manifest:606` → `661` | Fresh C2 root + arch PKG-1 + approval + tex/bib → NEW manuscript | Inject 661 → refuse | **PASS** |
| Review | `build_review_record:799` → `898` | Durable manuscript + REAL pdf + full 11-check family → NEW review | Inject 898 → refuse | **PASS** |
| Gate (R4 row34) | `evaluate_reader_surface_gate:1475` → `1830` | Durable manuscript + `reader-surface-semantic-review` (not editorial) + NEW gate | Inject 1830 → refuse | **PASS** |
| Execution (R4 row35) | `initialize:170` → `302` | Fresh C2 root + NEW session → index+sessions NEW | Inject 302 → refuse | **PASS** |
| Release (R4 row31) | `build_release_checkpoint:67` → `231` (147 middle) | FROZEN via VALIDATED_DRAFT + candidate/preview/HumanGate/freeze + advances (no TinyTeX rebuild) + merge+record (canonical NEW) → checkpoint `FROZEN.json` + `core-stage-contract` NEW (driver build only, State stays FROZEN) | Inject 231 → refuse, no checkpoint | **PASS** |

No count-only grep; no invalid-missing-proposal early-fail regex (healthy proves passage via strictly-later exact error or real write; faults assert exact `DM022_TRANSITION_ACTIVE` at exact seam with caller file/fn/line). No second-call-count ambiguity (exact outer line asserted).

## Remaining (no waiver, precise)

- General mandatory DONE (24/24). No SKIPs (old 3 SKIPs fixed, old RAWs preserved).
- B-owned ENTRY-only → entry+prepublish fixes (B2 `author-B2-final-prepublish-correction.md`, pins `agent647b…/human447ac…` etc.) NOT captured (frozen pins retained); B currently correcting rollback late-invalidation — DON'T capture live B while writing (frozen exec only). B remaining late-guard (human invalidate/record/request, orchestrator execute/apply, bridge, stage already PASS in B2? Actually B2 proves 10 new +23 existing PASS in private copy with new source; remaining B families per B2 §4 still OPEN for same REAL-helper pattern, no new source needed) are B-owned, not General (see coordination). General test ownership remains author, not final review.
- No global CAS/crash-atomicity (single-writer guarded transition only; INDETERMINATE preserves, no auto-rollback per §11.3). No genuine approval/Production (all `SYNTHETIC_FIXTURE_*`). Whole `NOT_READY/step4B3OPEN/audit unstarted/DM021+022OPEN`. Stop at Human Commit Point; ordinary Commit/Push Human-owned.

## Independence

General test-author/executor ONLY. No source/schema/test/fixture/config edits (only 2 test files, allowed via patch; runtime unchanged, frozen pins). No network, Human readback, ordinary commit/push, Gitconfig/cleanup. Early completion evidence only; may later final-review only with fresh fixed all-owner snapshot + full raw + affected regressions + independent implementation review.
