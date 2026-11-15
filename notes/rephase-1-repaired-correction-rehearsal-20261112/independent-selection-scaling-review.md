# Independent Selection scaling review — preflight timeout (Root §20)

Reviewer: Fresh independent reviewer. Not author/operator/root/Human, no prior W34/SP authorship in this packet.
Authority: `notes/rephase-1-repaired-correction-rehearsal-20261112/astra-operation-resolution.md` FULL §20 ONLY.
Scope: `selection-preflight-20261115T042533Z/selection-preflight-20261115T042533Z-execution-report.md` + machine,
`selection-revalidation-call-map.md`, `diagnostic-20261115T051801Z/diagnostic-report.md` + machine + raw profiler
(`W34-ready.partial-signal.json`, `SP-ready.raw.json`, `W34/SP-ready.pstats.txt`, `diagnose_ready_profile.py`,
`before-hashes.json`, `before/after-*-status.txt`, `after-check.txt`).
Method: read-only. `Read` + packet JSON/parse only. No project imports, tests, probes, Git, network,
Production/reconstruct readback, active writes, subagents. New review files are the only writes.
This review does not authorize code. It is not Selection/Architecture PASS, not R4, not Human approval.

## 1. What was verified

### 1.1 60 AG / 92 AG are finite-path source estimates, not measured invocation totals — CONFIRMED

Traced in shadow source
`.rephase-1-editorial-runtime/selection-preflight-20261115T042533Z/candidate-work/scripts/`:

- Runner `run_selection_architecture_v2_interactive.py:run()` order verified:
  `:249 agent.validate_agent_state`, `:260 _dm022_require_ready`, `:264 _dm022_resolve_ledger_completeness`,
  `:270 _dm022_pinned_family`, `:271 resolve_research_authority`, `:283 screening.resolve_active_screening_acceptance`,
  `:286 resolve_effective_discovery_basis`, `:304 _dm022_preflight_seven`, `:310 derive_candidate_matrix`,
  `:316/:362/:427/:440/:444/:451/:456 _dm022_require_ready` (8 gates), writes at `:319/:365/:430/:443/:454/:459`.
- `_dm022_require_ready:46-47` -> `low.require_research_operation_ready:4087-4140` ->
  `_verify_completion_full:996-1125` -> `_verify_adopted_graph_full:802-993` at `:1018` AND `:1073`.
  Therefore 1 READY = 2 AG. 8 runner gates = 16 AG. Verified in source.
- `resolve_research_authority:1128-1228` -> `_verify_adopted_graph_full:1177` = 1 AG + final triplet/file recheck
  `:1205-1213`. Verified.
- `agent.validate_agent_state:919-999` loops expected checkpoints; for these PREARCH same-record States
  evidence/materiality/completeness each dispatch via `_validate_checkpoint_record:770-805` ->
  `_validate_prearchitecture_core_proof:290-321` -> `check_supersession:3848-3976` ->
  `_verify_adopted_graph_full:3885` = 3 AG per state validation. Under
  `agent_tool.current_stage_basis_override:122-143`, `core.verify_state_basis` becomes
  `verify_current_stage_basis:42-50` -> `agent.validate_agent_state:48` = 3 AG.
  Verified override chain in `survey_agent_tool_v2.py:42-50,122-143`.
- `_load_upstream survey_architecture_v2_base.py:279-353` calls 5 public validators
  (`:292 screening`, `:299 evidence`, `:302 views`, `:310 ledger`, `:321 completeness`).
  Each internally reaches `core.verify_state_basis` at e.g. `screening:1336`, `evidence:1223/1993/2781-2786`.
  Call-map 15 state validations -> 45 AG on PREARCH is source-plausible; spot-checked validator
  sites (`screening:771,1102-1103,1123,1336`, `evidence:839,1223`, `survey_architecture_v2_base:292-331`,
  override use in runner `:309/:432`) match the shape. Exact 1+2+2+5+5 split was not independently
  re-counted validator-by-validator here; accept as estimate, not audited exact per-validator total.
- W34 pre-matrix block `:249(3)+:260(2)+:264(1)+:271(1)+:283(6)+:310 EU(45)+:316(2)` = 60 AG.
  `:283` 6 = `agent.resolve_checkpoint_artifact -> _validate_agent_state (3)` + `validate_acceptance`
  under override -> `verify_state_basis` -> `validate_agent_state` (3). Plausible from
  `screening:1102-1103` override + `survey_agent_control_v2.py:1210` resolve path cited in call-map.
- SP post-Architecture block `:432 EU(45) + :432 validate_candidate_matrix/derive/_load_upstream(45) + :440(2)` = 92 AG.
  Double upstream (`architecture:866` + `:880/:373`) has no new input between them — verified as
  structural duplication in call-map §4; `survey_architecture_v2.py` wrapper delegates to base,
  no new family introduced.
- Per-AG content: `_verify_adopted_graph_full:945-972` runs 6 Evidence + 3 View passes
  (`:946 evidence`, `:950 views+ nested evidence :1876`, `:957 ledger direct+nested`, `:965 completeness
  direct+nested`). Each Evidence pass `:1738-1793` does capture/load/recheck + supplement closure
  `:300-386/:389-424`. View pass `:1856-1893` re-enters Evidence at `:1876`. Own-epoch
  `:639-799` does `cat-file -e/show/ls-tree/batch` + schema/Contract8 recompute per AG.
  Verified signatures, not line-by-line re-audit.
- Finite DAG, no infinite recursion — CONFIRMED in structure:
  AG calls evidence/views/ledger/completeness + own-epoch; AG does not call completion/resolve/ready.
  Completion calls AG twice; resolve calls AG once; `_load_upstream` -> validators -> state ->
  `check_supersession` -> AG leaf. No back-edge found. Sibling duplication + internal duplication
  (`low:1018/1073`, runner `:264/:271`, summary double upstream, 8 READY gates, nested 6x/3x
  revalidation) explains cost without a cycle hypothesis.
- Why estimates, not measured: saved preflight raw has stdout/stderr 0B, no stack, no per-phase timing.
  Diagnostic probes measured ONLY `require_research_operation_ready` (2 AG), not the full 60/92 path.
  The 367 Evidence + 184 View passes pre-matrix and 565 + 283 post-Architecture are arithmetic
  `AG*(6/3) + EU*(6/3) + P(1/1)` with N=409/160, not profiler-observed totals. cProfile counts below
  belong to the READY probe only.

### 1.2 Bounded probes — CONFIRMED with scope limits

- Selected entry `low.require_research_operation_ready` is the correct pre-first-write gate:
  it runs before any matrix write, performs FULL completion (2x AG over 409/160), and W34 0/7 with
  zero stdout is consistent with blocking there. `validate_agent_state` lighter provenance checks
  correctly not selected as primary. No facade/bypass: direct call, no `current_stage_basis_override`,
  no writer/prepare/adopt, no canonical artifacts. `diagnose_ready_profile.py:1-247` source-guard
  (HEAD `ae0dd1e`, LOW sha/bytes) before shadow import verified.
- W34-ready: PID 740047, wall 85.01s, exit 124 via internal `alarm(85)` + external `timeout -s TERM 90`,
  `received signal 14, flushed stats`. utime 0.24->78.75 (Δ78.51s), stime 0.02->5.68 (Δ5.66s),
  maxrss 85952KB, rchar 4826432->8859139015 (Δ8854312583 ≈8.85GB logical), read_bytes 98304->139264
  (Δ40960 ≈40KB disk). cProfile 90176914 calls (87096096 primitive) in 84.998s.
  `W34-ready.partial-signal.json` + `W34-ready.pstats.txt` preserved; no `W34-ready.raw.json` by design.
- SP-ready: PID 747458, wall 27.98s, exit 0, `returned None` (READY returns None).
  utime 0.24->26.08 (Δ25.83s), stime 0.03->2.09 (Δ2.06s), maxrss 56636KB,
  rchar 4826432->1180697679 (Δ1175871247 ≈1.18GB logical), read_bytes 0->0 (Δ0, page-cached).
  cProfile 37064332 calls in 27.980s. `SP-ready.raw.json` + `SP-ready.pstats.txt` preserved.
- Hotspots (cumulative, W34/SP): READY 84.998/27.980 -> completion 84.997/27.978 -> 2x AG 84.825/27.794;
  evidence 61.743(8)/19.972(12); ledger 37.788(2)/15.578(4); views 32.975(4)/13.376(6);
  `openssl_sha256` 23.321/3.096, `_assert_pin_repo_ancestors` 23.034/15.888, `relative_to` 19.461/7.939,
  `_repo_file` 18.625/12.903, `lstat` 14.111/6.039, `derive_ordinary_root_effective_context` 13.711/2.386,
  schema validate ~10/~4. W34 timeout stack via controlled signal:
  `evidence:515 _supplement_source_file (relative_to)` <- `:372 _resolve_phase_supplement_context`
  <- `:1779 _validate_evidence_acceptance_content` <- `:1876 views` <- `:950 AG` <- `:1073 completion`
  <- `:4139 READY`. Same chain returns for SP.
- CPU + I/O scope — CONFIRMED as observation only:
  Both probes ~99% CPU-bound (W34 84.17 CPU / 85.01 wall; SP 27.89 / 27.98), huge logical rchar vs
  tiny/zero disk read_bytes = page-cache logical work, NOT disk-wait proof. Same-process
  `/proc/self/io` + `resource` only; no child breakdown, no Git subprocess vs JSON vs Path split beyond
  pstats cumulative. Preflight outer-shell PIDs (710005/712363) vs Python child ambiguity preserved
  (wall times authoritative, no inference that outer PID equals Python PID). cProfile overhead inflates
  absolute wall but preserves relative hotspot ordering; quantitative overhead not isolated.
  No physical-savings/deadlock claim: timeout bound is observation limit only, not deadlock proof or
  universal performance result. No memory-pressure/filesystem/page-cache/Git-latency exclusion beyond
  the observed run.

### 1.3 States / slots / processes — CONFIRMED

- Active `.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work`
  HEAD `ae0dd1e` parent cc1c tree `ec11cf6c…` verified pre/post unchanged; shadow byte-copy same HEAD/tree,
  `.git` dir no symlink/commondir/worktrees/alternates, hardlinks 0, inodes differ, objects 231/231,
  origin inert. Source773 manifest `a7e40c47…`/202833B, head `409b292`, 773/773 both runtimes.
  Spot HIGH/LOW/runner pins unchanged.
- Both States EVIDENCE_REVIEWED init480 Human pending guard absent pre/post:
  W34 `a8586351…`/4162, SP `38a63411…`/4266; PREARCH W34 `73ab28ea…`/6054, SP `2a528ed5…`/6300;
  completions unchanged; 8 four-refs match checkpoint record pre/post (typed `artifact_refs`, not prose).
  Active 7 slots absent (status 33, no matrix/selection/architecture/summary/attention/archive/audit).
  Shadow 36 = active 33 + 3 SP partials (`2f62e2a8…`/239359 matrix, `4e6884d6…`/76603 selection,
  `4af84ab3…`/33219 architecture); 4 absent (summary/attention/archive/audit); W34 0/7.
  `before-hashes.json`, `after-check.txt NONE`, before/after status files confirm no drift/overwrite.
- No writer still running: recorded outer PIDs 710005/712363 absent via `ps -o ...` (no output),
  no `pgrep -af .../run_selection` except own string, wall times authoritative
  (W34 20261115T042735Z->044750Z exit 124; SP 044836Z->050841Z exit 124; stdout/stderr 0B each).
  No kills, no Python-child inference. Diagnostic probes 1 per edition, no repeat/fix, source/state/slots
  unchanged after (`after-check.txt NONE`, no `__pycache__`/pyc in shadow). Preservation holds.

### 1.4 Minimal safe next investment — code-grounded boundary

Examined runner + LOW + agent/screening/evidence/architecture-base sites above.
Safe investment is ONLY:

- Private invocation-scoped authority/content reuse + logical-write/return freshness checks,
  created/consumed inside one `run()` invocation after the first full authority check, carrying at most
  exact State path+sha, checkpoint path+sha, already-read four-ref bytes/hashes, retention/completion
  identity, last guard/slot state. Every reuse must preserve: exact State/checkpoint identity,
  same-record triplet, live file rehash, own-epoch Git proof, full content/report/proof/decision/retention
  checks, cheap freshness at each write boundary. Must not survive invocations or State/checkpoint/guard/slot change.
- Call-shape deduplication only: completion double AG (`low:1018/1073`), runner double resolve
  (`:264/:271` no intervening write), summary double upstream (`architecture:866` + `:880/:373`),
  adjacent READY gates (`:440/:444`, `:451/:456`), nested 6x/3x revalidation inside one AG/EU.
  Optimize redundant paths, not freshness invariants.

Explicitly forbidden (would violate current/history/guard/own-epoch rules):
global/epoch cache, caller-verified dict, public skip flags, third validator, new family/schema/module,
mirrored validator stubs, writer patches that weaken validation, hydration as proof, or any bypass of
LIVE rehash / COPY-derived expected-after / triplet / own-epoch commit proof.

## 2. Judgment

- Do NOT simply raise timeout (e.g. unlimited/7200s): READY alone costs 85s (W34, timeout) and 28s (SP);
  full 7-slot run is 162 AG + 3 EU + 2 P by source estimate. Longer bound would eventually emit slots
  but retains honest per-record FULL cost at every gate, no scaling fix, and normalizes waste as PASS.
- Do NOT copy partial shadow products into active authority: SP 3/7 are timeout mid-write with 4/7 absent
  (no summary/attention/archive/audit, no closing shapes, no overflow check, no byte-eq archive).
  Copying would violate seven-slot no-overwrite, guard/provenance, independent-review binding, and
  active untouched invariant (active HEAD `ae0dd1e` status 33 preserved).
- SELECT bounded existing PREARCH-readiness/Selection validation scaling repair:
  private invocation-scoped checked-authority/freshness context + redundant-path elimination,
  preserving all predicates above. This is the only option consistent with §20 diagnosis and call-map
  boundaries A/B/C. Requires Astra pre-code map + independent readiness confirmation BEFORE code,
  then whole repair, meaningful affected tests, actual W34/SP completion, fresh CURRENT proof,
  independent implementation review to Commit Point. No new feature/family/reader/CLI bypass.

## 3. Next task recommendation

After Human continuation, Astra returns concrete pre-code interface/call/freshness map for the bounded
repair on actual `ae0dd1e` + final773: exact private-context type/lifetime/invalidation (State/checkpoint/
guard/slot/own-epoch), which duplicate AG/EU/P paths are removed vs which freshness rechecks remain,
per-write-boundary cheap checks, import/digest/closure/write-set/failure oracles, affected/normal
consumers, and why global/cache/verified-dict/public-flag/third-validator/new-family are excluded.
Independent scoped readiness review + Astra confirmation BEFORE code. Then implement whole repair,
not a detached helper; no active canonical generation until repaired runtime passes real W34+SP runs
with fresh proof and independent final review. Preserve all old attempts/partials/proofs.

## 4. Preserved semantic reviews vs runtime failure (do not conflate)

- `reviews/W34-selection-architecture-review.md` + machine (`PROPOSAL_READY_FOR_PREFLIGHT`, 409/45/5,
  24 PRIMARY + 21 SUPPORTING, page 15/16, inherited boundaries) and
  `reviews/SP-selection-architecture-review.md` + machine (`PROPOSAL_READY_FOR_PREFLIGHT`, 160/130/9,
  Jev/D142/deployment/Engram/GenAI-Perf/X rules, 60/75pp) remain input-scope DATA findings.
- Preflight timeout (W34 0/7, SP 3/7, exit 124) is runtime cost evidence; it neither invalidates those
  editorial judgments nor promotes them to Selection/Architecture PASS, Human approval, Draft/PDF, or R4.
  Semantic scope and runtime scaling are separate verdicts.

## 5. Uncertain claims (explicit)

- Full-runner 60/92 AG and 367/184 + 565/283 pass arithmetic are source-derived estimates; no measured
  full-runner invocation total exists (preflight raw 0B, no stack/timing; diagnostic measured READY only).
- 15-validators->45-AG multiplier per EU uses call-map accounting; per-validator 1/2/2/5/5 split accepted
  as plausible here, not validator-by-validator re-audited.
- Single slow graph pass vs repeated cost: READY-gate repetition is measured (2x AG per READY, 8 gates,
  nested 6x/3x); full-runner deadlock vs slow-pass vs filesystem/page-cache/memory/Git latency cannot be
  distinguished from saved preflight alone. Diagnostic CPU/rchar evidence applies to READY probe only.
- cProfile absolute times include profiler overhead; relative ordering only. Parent vs child (Git batch,
  file I/O) contribution not separated. Cold-cache vs warm-cache I/O not measured.
- SP 3 partial artifact hashes/bytes are actual, but content is partial-timeout output, not semantic PASS
  and not adoptable authority. No physical disk-savings, speedup, or deadlock claim is made.

Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN. Stop at Human Commit Point.
Ordinary Commit/Push Human-owned. No code authorized by this review.
