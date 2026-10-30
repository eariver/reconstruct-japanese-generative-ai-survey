# DM022 normal-writer late-guard evidence — General test-author/executor (unit ongoing)

Date: 2026-10-29 UTC. Test-author/executor General ONLY, NOT reviewer. Runtime
fixed-source-bound `SOURCEPASS` on EXACT snapshot-review worktree764
(`snapshot-review-20261029T053058Z/worktree/`, 764 files, SHA256
`60aaaee8539f69432a01d0ad72c1131b23951fd87a5531981876642d877ecee`/158161B,
delta vs actual409 **52M+75A=127**). Pins verified in exec before/after:
LOW `2aef837f…`, HIGH `3d1d87d8…`, release `b9433b9e…`, publication `705bcee…`,
refresh `dd01fa01…`, agent `b6506a8b…`, H `a9de2c97…`, S `b139f493…`.
Whole latest both-route C→U→U + genuine Weekly G71→G76 RELEASED green on EXACT
runtime (after C2 `b943`/`705`/`dd01`) is the authority for healthy paths;
this unit adds required operation late-seam runtime coverage before closeout.

Read: independent-final-operation-review §§2/4/6 (entry+prepublish helper,
C2 entry-only qualification, late seam OPEN), precode R3 normal-writer rows +
oracles, R4 40 rows + `require_research_operation_ready` passive oracle,
`guard-resume-oracles-r2.md` failure table. C2 current tests prove ENTRY only
(positive fails later invalid receipt), NOT prepublish.

## Method (no existing runtime/test edits)

- New files ONLY: `tests/test_dm022_normal_writer_late_guard_v2.py` (this suite)
  + `tests/dm022_late_guard_fixture_v2.py` (LateGuardInjector + snapshot).
  No existing `scripts/` or `tests/` edited. Exec is private byte copy
  `/tmp/dm022-late-guard-20261029T060000Z/exec/` (incl `.git` for HEAD pins,
  no hardlinks/alternates, `PYTHONDONTWRITEBYTECODE=1`, `unset GIT_*`,
  `/usr/bin/python3` 3.14.4). Workspace packet has NO GitDB/pycache.
- DURABLE latest both-route prePreview/canonical + VERSIONED fixtures from
  `evidence/full-lifecycle-v2-fixture-manifests/durable-versioned-20261029T064541Z/durable-fixture-manifest.json`
  (independent DBs under `.rephase-1-editorial-runtime/`, outside packet)
  copied NEW per fault (`_copy_durable_to_temp`, `__pycache__` ignored).
  Fresh EVIDENCE_REVIEWED via `test_dm022_full_lifecycle_v2` helpers
  (`_chain_root` + `_make_evidence_reviewed_state` + `_materialize_…` +
  `_build_selection_input`); fresh C2 ready roots via
  `test_survey_dm022_c2_consumers_v2._make_c2_ready_root`; P1 scope helper
  invoked for retention attempt (not unsafe saved runner).
- Wrap REAL `low.require_research_operation_ready` (never mock PASS).
  `LateGuardInjector` records direct (`_dm022_require_*`, line 88 etc.) +
  outer (business fn, exact line) via `inspect.stack()[2]/[3]` (fixed after
  initial off-by-one: first run showed outer as wrapper itself, corrected to
  skip fixture frames). Injects owned synthetic guard
  (`{"phase":"TEST","nonce":"synthetic-late-guard-v2-<fn>-<line>-<pid>"}`) ONLY
  when outer matches exact prepublish seam (file sub + fn + line); ANY present
  refuses (no legal HIGH owner needed). Entry vs prepublish traced by exact
  caller line, NOT approximate second-call counts. Target reached asserted;
  entry reached asserted where same fn (selection/manuscript/etc.); for
  entry/target in different fns (draft `_upstream`→`main`) `entry_fn` param
  supported but not needed for passing cases.
- Healthy counterpart reaches REAL write via legitimate NEW output path
  (fresh slots absent → 7 writes; NEW session_id; NEW candidate/preview/review/
  gate/visual/freeze out filenames; no clearing of accepted data). Fault uses
  FRESH independent copy, plants guard AFTER entry succeeds BEFORE actual
  prepublish READY read, then REAL helper must refuse with
  `DM022_TRANSITION_ACTIVE`. Immediate pre/post full output inventory scoped to
  exact write window, excluding fault injection ONLY (`new_keys == {guard}` or
  `<= allowed partials` for multi-write selection; no byte drift otherwise).
  Guard/file/partial allowed outputs preserved (no business cleanup; temp dirs
  cleaned by unittest only).
- No new acceptance flags, caller-verified tokens, or authority mocking.
  No global CAS claim. Injection is before checked seam, never after final
  checkpoint. Test Git commits (fixture DBs) use meaningful synthetic content +
  process-scoped identity (`Synthetic DM022-Late-Guard Fixture`,
  `late-guard@example.invalid`, inert `example.invalid` origin), no root DB
  objects, no `GIT_*` inheritance, no ordinary commits/Human readback/network/
  Gitconfig/cleanup/inherited-fixture mutation.
- Raw: `evidence/late-guards-20261029T060000Z/raw.txt` (18 tests, 54.4s,
  exit 0, PID 4123560, `2026-10-29T072358Z→072452Z`), `header.txt` (date/PID/
  exec/snapshot/pins/python), `pins-after.txt` (9/9 pins match pre), `exit.txt`,
  test files + SHA. Failed setups logged separately (none; 3 skips with exact
  missing capability, unique, no overwrite).

## Result: 15 PASS, 0 FAIL, 3 SKIP (remaining OPEN, no waiver)

`python3 -m unittest tests.test_dm022_normal_writer_late_guard_v2 -v`:
`Ran 18 tests in 54.407s — OK (skipped=3)`. 15 meaningful late-guard cases
prove prepublish refusal with zero non-guard writes; 3 skipped with exact
missing capability (see Remaining). No runtime bug found in covered seams;
no patch. Unit ongoing.

### Per-family table (actual oracles, not count-only grep)

| Family / R4 row(s) | Mutating entry (public) | Entry line | Prepublish line(s) | Healthy proof (real write, NEW path) | Fault proof (late guard, no-write) | Status |
|---|---|---|---|---|---|---|
| Selection 7 writes incl AUDIT (R4 row7, R3 §7) | `run_selection_architecture_v2_interactive.run` | 260 | 316 matrix, 362 selection, 427 architecture, 440 summary, 444 attention, 451 archive, 456 audit | Fresh EVIDENCE_REVIEWED (WEEKLY 2026-W33 via full-lifecycle chain, production Discovery acceptance materialized) → 7/7 slots written, audit `interactive_input` binds generated archive (path≠caller input, bytes equal), second regen refuses overwrite | 7 cases, each fresh copy, inject at exact slot prepublish: matrix case `new=={guard}`; selection case matrix partial allowed, selection absent; arch/sum/att/arc cases earlier partials allowed, target absent; audit case 6 partials allowed, audit absent; all `DM022_TRANSITION_ACTIVE`, guard preserved | **PASS ×7** |
| Draft runner (R4 row9) | `run_drafting_synthesis_v2_interactive.main` (`_upstream` entry 81 + 5 prepublish 218/223/229/242/247) | 81 (`_upstream`) | 218/223/229/242/247 (`main`) | — | — | **OPEN** — needs ARCHITECTURE_ESTABLISHED + approved Gate + canonical accepted-evidence tree mirror + valid drafting input (full witness to arch approval, ~30s + P1 helpers); exact missing: fresh ARCHITECTURE_ESTABLISHED fixture with `_materialize_canonical_accepted_evidence_tree` + `_build_drafting_input` |
| Evidence ledger/completeness (R4 row8) | `run_evidence_v2_interactive.run` | 623 | 742 ledger, 758 completeness | — | — | **OPEN** — needs CANDIDATES_NORMALIZED (discovery+screening valid, evidence pending) with full checkpoint validity; `_chain_root` gives ISSUE_INITIALIZED, `_make_evidence_reviewed_state` gives EVIDENCE_REVIEWED (wrong lifecycle: evidence runner requires CANDIDATES_NORMALIZED, would fail before prepublish); exact missing: CANDIDATES_NORMALIZED builder (discovery+screening checkpoints + State with `machine_checkpoints`/`checkpoint_provenance` for CANDIDATES_NORMALIZED, `agent.validate==[]`) |
| Agent advance (R4 row40) | `survey_agent_control_v2.advance_with_checkpoint` | 2306 (`_require_dm022_ready`) | — (single seam in snapshot; no second READY before `core.write_json` State) | — | — | **OPEN (entry-only in snapshot)** — code has single READY at entry, no prepublish before State write; late seam N/A without code change; R4 map claims entry+prepublish, snapshot has entry-only; requires Astra disposition whether entry-only sufficient or prepublish must be added; no waiver, no patch |
| HumanGate approve/invalidate/record (R4 rows18-20) | `survey_agent_control_v2.approve_architecture` (2381), `survey_human_gate_v2.record_*` (707/767), `invalidate_pending_gate` (1232/1406) | 2381 / 707/767 / 1232/1406 | — (single seam per function in snapshot) | — | — | **OPEN (entry-only)** — each presentation/invalidation has single READY at entry, no second prepublish before review/approval/State writes; late seam N/A; needs Astra disposition + ARCHITECTURE_ESTABLISHED fixtures for healthy |
| Orchestrator (R4 row16) | `survey_orchestrator_v2.execute_action` | 667 | 722 | — | — | **OPEN** — needs valid spec + HandlerRegistry + ... with NEW result path; exact missing: minimal valid `execute_action` spec (stage-matched, NEW `result_path`) on EVIDENCE_REVIEWED fixture |
| Stage validation (R4 rows13/15) | `survey_stage_validation_v2.validate_stage` | 869 | 888 | — | — | **OPEN** — needs valid stage artifacts + reviews for SELECTION_COMPLETE etc.; exact missing: minimal valid `validate_stage` with NEW? (stage writes? Actually `validate_stage` is validator with mutating path; needs mutating-path fixture) |
| Bridge (R4 row17) | `survey_core_execution_bridge_v2._advance_stage` | 384 | — (single) | — | — | **OPEN (entry-only)** — single READY, no prepublish; same disposition as advance |
| Editorial prepare (R4 row26 family) | `survey_editorial_publication_v2.prepare_publication` | 1733 | 1783 (build-transfer) + … | — | — | **OPEN** — needs P1 chain + retention + scope + staged + manuscript-spec + toolchain-spec with NEW proposal/build dir + TinyTeX? (durable VERSIONED_ACTIVE has valid inputs but outputs exist; NEW proposal with new IDs + retained dir needed); exact missing: NEW editorial phase fixture (new proposal ID, new `publication/build/` dir, valid receipt chain) |
| Editorial finalize (same) | `finalize_publication` | 2301 | 2431/2512/2565/2597 | — | — | **OPEN** — same as prepare + deterministic/semantic/visual + bundle/gate/candidate/seal with NEW bundle/gate/candidate/seal paths; `_build_finalize_scope_fixture` gives staged+retention+scope but receipt missing (healthy fails at receipt before prepublish, as C2 proves); needs full valid receipt chain |
| Editorial activate/resume | `activate_publication` 3466/3805/3839, `resume_activation` 3954/4025 | 3466/3954 | 3805/3839/4025 | — | — | **OPEN** — needs valid set + P2V + record + State replace with NEW record/State (durable VERSIONED_ACTIVE has set but State already advanced; NEW activation intent needed); exact missing: NEW activation intent (new set + record + expected State) |
| Publication Candidate (R4 row31 family) | `survey_publication_v2.build_candidate` | 1932 | 2013 | Durable VALIDATED_DRAFT (WEEKLY 2026-W33, REAL main.pdf 68035B/5pp, manuscript/bundle/sem/vis valid) + NEW `publication-candidate-late-<tag>.json` → `READY_FOR_PUBLICATION_PREVIEW` | Fresh durable copy, inject at 2013 → `DM022_TRANSITION_ACTIVE`, `new=={guard}`, candidate absent | **PASS** |
| Publication Preview | `build_preview_approval` | 2123 | 2161 | Healthy candidate (above) + NEW `publication-preview-late-healthy.json` → APPROVED | Fresh copy + healthy candidate, inject at 2161 → refuse, `new=={guard}` | **PASS** |
| Publication Visual | `build_visual_review` | 2209 | 2245 | Healthy candidate+preview + NEW `visual-late-healthy.json` → PASSED | Fresh copy, inject at 2245 → refuse | **PASS** |
| Publication Freeze/Release | `build_freeze` | 2294 | 2338 | Healthy candidate+preview + NEW `freeze-late-healthy.json` + `release-manifest-late-healthy.json` → installed | Fresh copy, inject at 2338 → refuse, both absent, `new=={guard}` | **PASS (freeze)**; Release (`build_release_checkpoint` 67/147/231 + `build_release_record`) **OPEN** — needs FROZEN + merge verification + release record with NEW release paths (full FROZEN witness) |
| Manuscript (R4 row36) | `survey_reader_publication_v2.build_manuscript_manifest` | 606 | 661 | Fresh C2 ready root (2026-W35) + arch PKG-1 + approval + main.tex/bib (setup in fixture, pre-snapshot includes them) + NEW `reader-manuscript-late.json` → `READER_FACING_AUTHORED` | Fresh copy, inject at 661 → `DM022_TRANSITION_ACTIVE`, `new=={guard}` | **PASS** |
| Review (same family) | `build_review_record` | 799 | 898 | Durable VALIDATED_DRAFT manuscript + REAL pdf + full 11-check family (reused from durable semantic review) + NEW `review-late-healthy.json` | Fresh copy, inject at 898 → refuse | **PASS** |
| Gate (R4 row34) | `survey_reader_surface_gate_v2.evaluate_reader_surface_gate` | 1475 | 1830 | Durable manuscript + `reader-surface-semantic-review-v2.json` (NOT editorial; editorial fallback prohibited) + NEW `reader-surface-gate-late-healthy.json` | Fresh copy, inject at 1830 → refuse | **PASS** |
| Execution (R4 row35) | `survey_execution_record_v2.initialize` | 170 | 302 | Fresh C2 ready root + NEW `session_id=late-guard-<tag>` → NEW `execution/index.md` + `sessions/<id>.md` | Fresh copy + NEW session, inject at 302 → refuse, `new=={guard}` | **PASS** |
| Retention (R4 row33) | `survey_editorial_retention_v2.capture_retention` | 942 | 1519 | Genuine capture inside `_build_finalize_scope_fixture` (manifest exists) | — | **OPEN (SKIP)** — second capture with same pid collides `RETAINED_ROOT_EXISTS` before 1519; NEW proposal with NEW retained dir needed but helper hardcodes `fixture-wk-fin-1`; exact missing: NEW P1 proposal builder with new pid + new `retained/` dir |

No count-only source-grep tests; no invalid-missing-proposal early-fail assert
regex (all healthy prove passage via strictly-later exact errors or real writes;
all faults assert exact `DM022_TRANSITION_ACTIVE` at exact seam with
caller file/fn/line). No second-call-count ambiguity (exact outer line asserted).

## Remaining oracles (no waiver, no automatic takeover)

- Evidence (2), Draft (1), Orchestrator (1), Stage (1), Editorial 4, Release 2
  (freeze PASS, release OPEN), Retention (1), Agent/HumanGate/Bridge entry-only
  disposition (4 families) — all OPEN as above with exact missing capability.
  Priority order for closeout: selection 7 DONE; manuscript/review/gate/execution
  DONE; candidate/preview/visual/freeze DONE; next: evidence CANDIDATES_NORMALIZED
  builder → draft ARCHITECTURE_ESTABLISHED fixture → advance/approve entry-only
  disposition → orchestrator/stage minimal specs → editorial NEW-phase fixtures →
  release FROZEN witness → retention NEW-pid builder.
- No global CAS/crash-atomicity claimed (single-writer guarded transition only;
  incomplete op can have new State + old stale files with normal writers blocked
  by guard; no multi-file atomicity or auto-rollback per contract §11.3).
- No genuine approval/Production (all reviewers synthetic
  `SYNTHETIC_FIXTURE_*`, never genuine; no W40 reproduction).
- Whole `NOT_READY/step4B3OPEN/audit unstarted/DM021+022OPEN`; Profile/quality/
  adoption/savings OPEN. Stop at Human Commit Point; ordinary Commit/Push
  Human-owned.

## Independence

General test-author/executor ONLY, NOT reviewer, NOT Owner A/B/C1/C2/G71.
No source/schema/test/fixture/config edits (only NEW test + helper in private
exec + packet evidence/report). No network, no Human readback, no ordinary
commit/push, no Gitconfig/cleanup/inherited-fixture mutation, no GitDB in packet.
Early operation late-guard only; may later final-review only with fresh fixed
all-owner snapshot + full raw + affected regressions + independent implementation
review.
