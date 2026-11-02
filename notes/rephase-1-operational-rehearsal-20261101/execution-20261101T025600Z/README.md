# Isolated rehearsal execution — W34 @774 + SP-efficient-llm @c8 (pre-Architecture, actual work)

2026-11-01. General isolated rehearsal execution/research-author owner. Actual work in NEW ignored isolated DB, not planning-only. Source CORR applies: initial intake → research/Selection/Architecture+dossier only until genuine Architecture approval. No Draft/Preview/Gate fabrication, no rollback of historical State, no Production writes/adoption.

## 1. Source / workdir / refs (no commits outside isolated fixture)

- Code authority: final138 proof `.rephase-1-editorial-runtime/profile-support-packaging-20261031T202327Z/proof-copy/candidate-partial-b40de60` (770 files), patch `efb505e44c1ccb3c83121db2fbaa9fec05ed900c252184765ca3b50f7b28254e`/5247647B, manifest `634d41f9807e8cd60ca3d839245358fa5e5da312f6d1b58ae84c1619481a03dc`/186847B. Proof preserved, not mutated.
- Isolated workdir: `.rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work`. Copy via `tar --exclude=.git` (770 files, 0 pyc) + `cp -a .git` (independent, no hardlinks — inodes distinct, nlink 1). Inert origin `https://example.invalid/rephase-candidate-recovery.git`, no alternates file, no `GIT_*` env, sparse-aware. Before: HEAD `409b292756dd1277b9dfae87679934c0d2ce251c` dirty 138. Source commit (meaningful rehearsal base, process-scoped `General Rehearsal rehearsal-20261101T025600Z-*@example.invalid`, no empty): HEAD `480823560c0c26ed2e5baa18e0e79a22b2839a27` clean for sparse worktree. No push, no reconstruct Git/readback, no ordinary candidate HEAD changes.
- Targets: W34 `774dd39a951c9ac3818e83dfffd4c7666efb0a20` (WEEKLY/WEEKLY_MAGAZINE, ROLLING_WINDOW 2026-08-14–21 America/New_York) + SP `c8d0ecc1c9566a2303ad3b4c42635d4b672650e4` (THEMATIC/LONGFORM_SPECIAL, OPEN_HISTORY_AS_OF 2026-09-21T16:10:00Z, 12 dims, O01–O12). Intake P2 ready (`ready-sufficiency.md`, 179 GETs, 145 DATA, 12,194,416B) is DATA reference; acquired `.py` never executed.
- Current stage (both editions): fresh `ISSUE_INITIALIZED`, `target_gate ARCHITECTURE_REVIEW`, implementation `48082356` (= HEAD, CURRENT). No old production State/Gates/checkpoints installed; old bytes stay in intake DATA + `input-archive/` only.

## 2. What actually ran (normal public paths, real bytes, logged)

All runs use workdir `scripts/` (final138) with real recorded bytes, process PIDs, captured cmd/env/stdout/stderr/exit in `logs/`. No old runners, no overwrites of intake DATA.

- `05-buildprofiles`: `core.weekly_profile` (W34, issue_id fixed, now 2026-08-25T00:00:00Z) + `core.thematic_profile` (SP spec from authorized profile: question/dims/asof/paths verbatim, fresh contract) + `core.initialize` ×2. Outcome: PASS. W34 question/window/dims/obligs/paths match authorized profile; SP question/dims/temporal/paths preserved byte-identical, contract fresh from current implementation. States agent-valid, exit 0. Logs `05-*`.
- `06-discovery-validate`: `disc.read_jsonl` + `_normalize_record` + `_validate_graph` on active discovery JSONL (W34 369, SP 165). Outcome: both REFUSED fail-close on missing immutable Raw (W34 `sources/2026-W34/intake/working-set/sol-discovery-event-inventory-v0.2.md`; SP `sources/SP-efficient-llm-2026/external/x/efficient-llm-reception-pass-01/raw/x-reception-result-r3.md`). Historical acceptance DATA exists but not installed (correct per no-old-State rule). Logs `06-*`.
- `07-interactive-shape`: current loaders on intake DATA (not installed): `scr.validate_decision` on SP decisions 165/165 PASS and cover accepted 165 exactly; `run_evidence._validate_record` on SP r1 160/160 PASS and W34 409/409 PASS (profile-bound with fresh Profiles). Outcome: input shapes valid; full admission (package/accept) NOT run — blocked on Discovery acceptance (needs X manifest + Raw above). Logs `07-*`.
- `input-archive/SP/interactive-evidence-adapted-O13-15.json` (346320B): p2c01 r1 base (12×3-field, ts001-substantive 155 PARTIAL/5 VERIFIED) + O13–O15 appended as exact 5-field with original dimension/description/status/rationale from `DATA.p2b26` (all LIMITATION, no upgrade, no aliases/drop). Shapes verified (12×3 + 3×5). Staged in packet input-archive only, not executed as admission (blocked). W34 needs no adaptation (3×3-field universe, no named).
- Root/effective preserved, not switched: W34 root 369 (`DATA.p2b01`) vs effective 439 event expansion (`DATA.p2b19`, REFERENCE_EXPANSION with parent_refs) kept distinct; no E-as-R; stale index (110/80) superseded by checkpoint-selected 369/439/409/41/9-package graph. SP original unprojected inputs used (p2b20/p2b21/p2g14/p2c01+p2c02); compat-projected accepted (`dba89409…`, ledger `b99a3068…`) comparison-only, never adopted.

Research/fidelity note: no semantic PASS claimed. Records incomplete where Raw missing — honestly LIMITED/NEEDS_RESEARCH preserved; no Grok/X completeness invented, no primary body invented. Supplement Raw (W34 61 bodies, SP 13 files 1,275,978B) referenced, not re-verified as publisher proof here.

## 3. Exact missing inputs needed (intake owner has same-fixed-ref approval, no new Human permission)

Request to intake owner/root (no self-fetch; no other-ref fetch):

- W34 @774: `sources/2026-W34/external/x/x-source-intake-v2.json` (expected SHA `702881aa75cc09ff3e65f5220e47076c8f67a8c97d4a8e87e41f5a98b2` from `DATA.p2b02`), `sources/2026-W34/intake/working-set/sol-discovery-event-inventory-v0.2.md` + 54 further collector Raw paths enumerated from discovery (github-releases 7, gapfill 24, arxiv/official rerun sets, carryover ledger already available as `DATA` tree path). Full list reproducible via `check-schemas.py` enumeration; ask intake owner to fetch X manifest first (unblocks acceptance validation), then working-set + collector raws in discovery-record order.
- SP @c8: `sources/SP-efficient-llm-2026/external/x/x-source-intake-v2.json` (expected `3465dc4f4d9d3bce73cc33cb16820aa771816fa4d8de850336ef56c46d8275b0` from `DATA.p2b21`), `sources/SP-efficient-llm-2026/external/x/efficient-llm-reception-pass-01/raw/x-reception-result-r3.md` (unblocks graph; single file). Supplement Raw 13/13 and 24/25 obs already present.
- If any listed path 404 at the fixed ref, return gap as missing (no fallback to main/other ref).

No other edition/outside-fixed-ref fetch. No broad new feature: data types supported where checked; no unsupported-type/semantic-capability gap hit beyond missing bytes (if hit later, return exact predicate + legitimate alternative to Astra before code). Shipping runtime/schema/source unchanged.

## 4. Pending reviews / current seams (stop, no fabrication)

- No Selection/Architecture proposals yet: research acceptance not genuinely ready (Discovery acceptance blocked above). When intake owner delivers missing bytes, next is: Discovery acceptance build/validate → Screening `run` (needs DISCOVERY_COLLECTED via normal orchestrator transition, not test stub) → Evidence `run` (needs CANDIDATES_NORMALIZED + supplement where applicable) with adapted O13–15 → Ledger/Completeness → Selection/Architecture proposals + Human-facing dossier (avoiding W34 late compression: justify selected/omitted dims, sufficiency/limits, title/package allocation, reader questions). Initial authorship separate from independent review (root assigns); no synthetic independent PASS, no Human approval inferred; stop at needed review seam with artifacts + explicit pending.
- Unblocked target may progress while other waits; unavailable edition never replaced with fake fixture.
- Work removed (SP projection/hand-append vs new normal path) vs added (research/validation/handoff/build-prep) tracked in worklog; wall-clock actual where captured (log times/PIDs), LLM UNKNOWN (no telemetry), no savings claimed from test seconds.

## 5. Worklog (append-only, minimal)

See `worklog.md` (one row per attempt: date_utc | edition | stage/op | input ref | role | wall_clock | llm | outcome | rework_reason | blocker). All rows UNKNOWN for LLM/tokens; wall-clock from log timestamps where available, else UNKNOWN.

Bounds: isolated rehearsal only, no Production/network/current-checkout/extra-intake/reconstruct-Git/Commit-readback/ordinary-commit. Scope may end blocked Raw/review, not fabricated complete. Artifacts: workdir (HEAD `48082356`, dirty: 2 modified W34 fresh Profile/State + untracked SP dir + staged discovery/Raw), packet `input-archive/`, `bindings/`, `logs/`. No live process duplication.

## 6. Update 2026-11-01T03:3xZ — P4 landed; Discovery acceptance built, review seam reached (history §§1–5 preserved)

- P4 verified + consumed per rule (API blob/size self-verify; P3 zeros never consumed): 6 github-release Raws (`p4a02–07`, sizes+blobs MATCH, content-sha == checker discovery-want `f75f…` etc.) + 74 other required Raws (all 80 required paths staged, `10-stage-raw` exit 0, FAIL 0). W34 result raw `p3a51` 23612B `43b0923b…` verified == P4 manifest want.
- X note (validated, not semantic): old accepted Discovery refs bind OLD manifest bytes (W34 `702881aa…`, SP `3465dc4f…`); P4 DATA files ARE those old bytes (actual sha confirms). New manifests built via normal `x_intake.build_manifest` tied to NEW profiles (W34 `2a8c3089…`, SP `aff05fd5…`; old `a6e3eb30…`/`22f2e822…` kept archived, never installed/rewritten), criteria verbatim from archived runs, rationale explicitly archival (same edition/window, old `observed_at` kept, `imported_at` real `2026-11-01T03:33:41Z`, NO new Grok request, SOCIAL reception-lead). `record_result` re-imports archived SUCCESS raws; both manifests `validate_manifest require_complete` PASS → COMPLETE (`11-x-manifests` exit 0).
- Fresh Discovery acceptances built+validated via normal `disc.build_acceptance`/`validate_acceptance`: W34 369 graph `a13afd9e…` binding NEW X `73db915a…`; SP 165 graph `441f488b…` binding NEW X `fa3a5055…` (`12-discovery-accept` exit 0). Old acceptances stay archived; no old checkpoint claimed for current paths.
- SP evidence basis corrected to r2 (semantic inspection, not ease): r2 = supplement-bound + body-consumed (148 PARTIAL/12 VERIFIED, 11 source_bindings, closure 5 limits) vs r1 abstract-level (155/5, no bindings); new file `input-archive/SP/interactive-evidence-r2-adapted-O13-15.json` (r2 + O13–15 5-field, 15 obligs, 0 record errors); r1-adapted preserved with SUPERSEDED note. W34: R369/E439 distinct (no E-as-R), evidence 409-input/3-oblig universe, selection 41 / packages 7 (W34 7, SP 9 — §2 "41/9-package" conflation corrected here).
- CURRENT STAGE: both editions have Profile/State (`ISSUE_INITIALIZED`), COMPLETE X, validated Discovery acceptance — and STOP. State transition to `DISCOVERY_COLLECTED` needs the normal typed checkpoint/control path ONLY after real independent SourceIntake review (author will not author PASS, no test-stub advance, no validator stubs). Exact review inputs/paths + check items in `review-seam-sourceintake.md` (root assigns reviewer). Screening/Evidence runs wait on that seam (`DISCOVERY_COLLECTED`/`CANDIDATES_NORMALIZED`); shapes pre-validated (SP decisions 165/165, r2 160/160, W34 409/409). No Gates/approval/Draft/Preview/Production.
- Source proof pin: workdir HEAD still `48082356`; new artifacts are workdir files + packet files only (X manifests/tasks, acceptances, staged Raws, `dependency-table.md`, review seam, r2-adapted input). No source/CAND commit (base commit only, prior unit), no network/readback. Logs `10/11/12-*` are raw cmd/stdout/stderr/exit (no summaries-as-raw).

## 7. Withdrawal + accounting corrections (2026-11-01T10:4xZ; history above preserved)

- **X 'mismatch confirmed' withdrawn.** `113d62e7…`/`638ea4af…` are Git blob SHA1s of the
  archived X-manifest files, NOT FILE SHA256s. Actual manifest FILE SHA256s
  (`702881aa…` W34, `3465dc4f…` SP — P4 DATA bytes rehashed locally) match the old
  Discovery `x_source_intake` refs. No historical X drift was established; root's suspected
  mismatch and my chat-side 'confirmed' wording were both incorrect. Fresh-manifest byte
  diffs come from the new Profile binding (W34 `2a8c3089…`, SP `aff05fd5…`), the locally
  re-rendered task, and the new import record — not from repairing an old mismatch.
  Old manifests/tasks/raws stay archived untouched; both hash domains preserved explicitly.
- **Archival-reuse rationale verified true** (review-seam doc restated, code paths confirm):
  no new external/Grok request (execution performed zero network; X ops were local
  `build_manifest`+`record_result` only); run criteria verbatim from archived runs
  (W34 purpose/window `2026-08-14T18:00–08-21T18:00-04:00` == fresh profile window;
  SP bounded reception pass through `as_of` `2026-09-21T16:10:00Z`); `observed_at`
  preserved (`2026-09-02T14:49:21.833Z` W34, `2026-09-21T17:16:12+00:00` SP),
  `imported_at` real (`2026-11-01T03:33:41Z`); SOCIAL stays reception lead per archived
  result rationales. No source change needed.
- **Raw counts, not forced.** Distinct JSONL-referenced Raw paths actually enumerated:
  W34 55 + SP 25 = 80, zero overlap, staged 80/80 (`10-stage-raw` FAIL 0). The SP-adjacent
  26th file (`sources/SP-efficient-llm-2026/raw/discovery-negative-space-2026-09-21.md`,
  4161B `ee785885…`, P2 `DATA.p2c14`) is inventory, NOT referenced by any discovery
  record's `raw_paths`/`locator` — an extra for Sol negative-space review, not a Raw
  requirement. No count is forced; sets above are the requirement.
- **SP basis fixed to r2.** Adapted input is r2-based (148 PARTIAL/12 VERIFIED,
  11 source_bindings, closure 5 limits) + O13–15; r1 file preserved SUPERSEDED. 148/12 are
  preserved input statuses, NOT a true-verification judgment — that judgment belongs to
  the Evidence independent review (governance §4.2), still pending.
- **Typed path staged, not advanced.** Deterministic CORE_STAGE_CONTRACT reports built
  (`sources/<issue>/orchestration/v2/stage-validation/ISSUE_INITIALIZED-report.json`:
  W34 1461B `67825323…`, SP 1513B `4922f984…`, both PASS, `13-stage-reports` exit 0);
  checkpoint paths verified ABSENT; exact checkpoint/review inputs recorded in
  `stage-path-inputs.md` for root dispatch after independent SourceIntake review.
  No checkpoint/state writes, no legacy transition, no guessed dispatch.
  Clock note: packet ID `025600Z` is a label; real invocation clocks are per-log
  (`13-stage-reports` recorded_at `2026-11-01T10:42:52Z`); requested editorial times
  (W34 `2026-08-25`, SP `= as_of`) are fixture-logical window refs, not real clock.
  W34 packages 7 / SP 9 (conflation corrected). Partial/sparse tree — no whole-clean claim.

## 8. Dispatch executed 2026-11-01T11:0xZ — DISCOVERY_COLLECTED both; SP Screening accepted; W34 blocked with exact gap (history preserved)

- **Independent review stored/cited truthfully.** `reviews/source-intake-review-20261101T104700Z.md`
  (38557B `1d46058e…`, CORR-20261101T11Z final-binding): BOUNDED PROCEED both, residuals §5
  retained as Evidence targets. Review file hash/bytes verified locally before use; no new
  Gate/checkschema/semantic PASS invented. No prior Gates copied.
- **Advance via dispatched typed path only** (public CLI `advance-stage` = build+advance;
  no legacy transition, no hand-crafted DCP, no plan_action guess). Reviews files (new):
  one CORE_STAGE_CONTRACT DETERMINISTIC row (13 reports) + one AGENT_RESEARCH row citing
  the review (executor `General independent supervisory reviewer`, no invented checkID).
  W34 exit 0 → DISCOVERY_COLLECTED (`11:00:03Z`, checkpoint `3c64e40b…`);
  SP exit 0 → DISCOVERY_COLLECTED (`11:00:23Z`, checkpoint `5b9910c9…`).
  Before/after strict agent validation PASS both; `discovery passed/screening pending`;
  HEAD still `48082356` (no source commit between report and build; reports still bound).
  Logs `14/15/16/17-*` raw.
- **SP Screening accepted (product only, review seam next).** Archived decisions staged exact
  (`DATA.p2g14` 68226B `9290f406…`, 165/165 exact coverage vs FRESH acceptance — verified,
  not assumed). Normal runner exit 0 → `screening/v2/accepted/9b979629…/
  screening-accepted.json` (69226B `6ff524b0a…`), KEEP135/MAYBE20/INSPECT5/DROP5 =
  archived counts (no mislabeled verifications, no status upgrades). STOP: no checkpoint,
  no transition — independent Screening review/control advance owns the next move.
  Exact review inputs (workdir paths): accepted + `package.json` + `results/` +
  `interactive-audit.json` + archived proposed `screening/proposed-input/
  interactive-decisions.json`. Author self-certifies no substantive PASS. Log `18a/b-*`.
- **W34 Screening blocked — exact gap returned, no fabrication.** (i) Current runner requires
  exactly the 369 accepted-root IDs; archived latest decisions (415…) are 439 event IDs,
  disjoint sets (missing 369 / extra 439) — verified, not assumed. (ii) The 439 event
  expansion cannot normalize under current code: 439/439 records carry bare parent_refs,
  refused by `survey_discovery_v2._parse_parent` (`local:`/`external:` namespace required;
  first ref `w34-discovery-sol-event-baseline-v0_2`, log `19-*`). Bare refs == root ID set
  exactly (369/369, all roots referenced) — format gap vs current contract, not corrupt data.
  Stale 105/110 subsets explicitly NOT fetched/used. No decisions authored, no IDs rewritten,
  no autofill, no runner executed without valid input. Alternatives for Astra (no code fix
  by author): (a) author 369 root decisions from archived event semantics under independent
  Screening review first; (b) rule whether expansion-package screening remains a supported
  normal path (code: resolver supports DERIVED_EXPANSION, runner is root-only); (c) fetch
  archived 415… `interactive-decisions.json` + audit at same ref for provenance completeness.
- Evidence/Selection/Architecture remain future seams; review §5 residuals travel unchanged
  (not re-listed here to avoid a second recap — see review §§5–6 + seam doc).
  No network/readback/Production/ordinary commit; source138 unchanged.

## 10. SP advance + Evidence accept (2026-11-01T11:2xZ; W34 untouched, history preserved)

- **Independent SP Screening review stored/cited** (`reviews/screening-efficient-llm-review-20261101T111203Z.md`,
  15613B `f450573d…` full hash verified locally): BOUNDED PROCEED, no mandatory input
  correction, exact current SP165 bytes bound, residuals §§2–4 kept explicit. Root accepts
  scoped decision. No new schema/checkID/Gate; AGENT_RESEARCH row only (honest completed review).
- **Typed advance via public CLI** (`23-*` report PASS 1591B `84d73fc2…`; reviews file with
  CORE row + AGENT_RESEARCH row citing `f450573d…`; `advance-stage` exit 0 `24-*`):
  SP `DISCOVERY_COLLECTED` → `CANDIDATES_NORMALIZED` (`11:21:00Z`, checkpoint `481d965f…`,
  agent-valid before/after, HEAD `48082356` unchanged). W34 remains `DISCOVERY_COLLECTED`
  (parallel independent review, no SP-advance side effects).
- **Supplement re-basis (existing builder, no old-manifest edit).** Old r1 manifest binds old
  screening sha `65330476…` (file absent in workdir) → builder-internal validation would
  refuse; returned as predicate, not worked around. NEW manifest
  `external/evidence-supplement/evidence-authority-supplement-r1-fresh-basis.json`
  built from 13 verbatim source rows + fresh basis (discovery `7074cef2…`, screening
  `6ff524b0a…`), 13/13 Raw staged verified (size+sha vs old entries; P2 checker PASS).
  Old manifest/tasks untouched in intake.
- **Substantive reads before use.** 12/13 supplement files topically match bound claims
  (arXiv IDs + titles present; D119 tooling doc title-confirmed). 11/12 VERIFIED findings
  reference publisher bodies NOT in captured corpus (only D032's launch page is bound);
  9 wrong-locator correct bodies ARE held as supplement (cited SHAs) with discovery locators
  unchanged. No status changed, no body invented.
- **Evidence accepted via normal runner** (`27-*` exit 0): r2-adapted input staged exact
  (`345202B f46dcf2f…`), NEW supplement bound; accepted 160 results (PARTIAL148/VERIFIED12
  preserved verbatim — NOT new substantiation), Views 160, Ledger 165, Completeness
  LIMITED (15 obligs, O13–15 LIMITATION preserved). Outputs:
  `evidence/v2/accepted/09f487ab…/evidence-accepted.json` (`9c254319…`),
  views `50c919b9…`, ledger, completeness. STOP: still `CANDIDATES_NORMALIZED`,
  no EVIDENCE_REVIEWED transition, no checkpoint, no independent PASS authored.
  Correlated: card source_class vs discovery source_type
  (PAPER→PAPER 94 incl. 2 supplement extras = 162 card sources; REPO→REPOSITORY 20,
  1 REPO→OFFICIAL quirk noted; others→OFFICIAL/SECONDARY/SOCIAL; zero UNKNOWN),
  named-15 trace bindings intact, tool ran under current impl `48082356` with strict
  validators (DM022 READY + 4 prepublish points, per-runner).
- **Removed vs migration work (observed, no savings claim):** compat projection
  (`dba89409…`) and hand-append-at-accept NOT used; O13–15 entered via validated input
  adaptation (prior turn, provenance explicit) with universe derived from discovery
  (named R/E), task IDs via `stable_task_id`. Migration = X re-import + supplement
  re-basis + input adaptation (all logged); review work = 2 independent reviews consumed.
  Break-even UNKNOWN until proper before/after comparison on equivalent scope.
- **Exact pending-research gaps (not closed, no proof invented):**
  (a) 11 VERIFIED bodies absent from corpus (D036 EAGLE, D070/D071/D141 Jev pages,
  D148/D149/D150/D151 TTC/reasoning bodies, D154 routing, D163 vLLM recipe, D165 PR) —
  if `execution/**/evidence-bodies/*` exists at c8, intake fetch shares same-ref
  authorization (no new Human question); else record AUTHORITY_* states at Evidence review.
  (b) 9 wrong-locator correct bodies held as supplement (cite per-body SHAs), discovery
  unchanged; fetch-or-hold rule per load-bearing claim (review §5.1).
  (c) Capstone pins + counterevidence stay LIMITATION (review §5.3–4).
- **W34 argv-fault resolution:** attempt-1 stdio overwritten; only quoted predicate preserved
  in `logs/21-*-attempt1-note.txt`, marked lost-not-reconstructed, NOT counted as runtime
  evidence (admission evidence = attempt-2 exit-0 only). Source138 verified byte-identical
  workdir-vs-proof for all 6 runtime modules (`29-*`, mismatch 0; `28-*` DRIFT flags were
  mistyped expected constants in that script — corrected, history preserved).
  P4 DATA transport validated (checker + own size/blob/sha checks `09/10-*`).
  No state/commit/network/readback/production/ordinary commit. Next: independent Evidence
  review (SP authority-consumption/semantic + W34 Screening), root dispatches.

## 9. W34 expansion Screening accepted via authorized existing transport (2026-11-01T11:1xZ; history preserved)

- **Read-only E validation first (log `20-*`, exit 0):** event DATA 1335444B
  (`0a23be47…`, blob `06eb26bb…` == tree@774 both canonical paths) — 439 records,
  schema PASS, expansion accounting `accounted_roots=369/369` (DERIVED_EXPANSION),
  universe U = 3 weekly obligs (no autofill), DECLARATION_LOSS none. Root 369 graph
  re-validated. Archived 439 decisions == event IDs exactly; stale 105/110 explicitly
  NOT fetched/used. (Correction to §8 analysis: `Discovery._normalize_record`
  local/external rule is root-only; E validates via Screening's own
  `validate_discovery_expansion` — the earlier `_parse_parent` refusal was
  wrong-validator-for-E, preserved in `19-*` logs, not a data defect.)
- **Staged canonical E path** (`sources/2026-W34/screening/input/event-discovery-v2.jsonl`,
  tree@774 path, bytes self-verified) + **prepared expansion package** via existing
  `screening.prepare_package` under strict `current_stage_basis_override`
  (`21-*`, exit 0 after one harness-argv fault: first attempt passed
  `implementation_sha=None`, refused `must record the actual current work-branch
  implementation commit`; fixed by passing actual HEAD `48082356`; fault quoted here
  because attempt-1 stdio was overwritten by the retry — future logs use unique names).
  Package: 439 records / 12 batches (basis binds event E + fresh profile/state).
- **Results from unchanged archived decisions + accept via existing API** (`22-*`, exit 0):
  all 439 archived decisions pass real `validate_decision` (0 errors; counts
  DROP30/INSPECT200/MAYBE136/KEEP73 preserved); per-batch `basis` = real
  `expected_result_basis` on the fresh package (no stale rebind);
  `reuse-provenance.json` in owned `proposed-input/` (NOT in results/ — accept enforces
  exact file set), historical runner identity NOT claimed.
  Accepted: `screening/v2/accepted/e193ad05…/screening-accepted.json`
  (543880B `b9d963d8…`; package copy + 12 inputs + 12 results alongside).
  Cross-check: `decisions` array byte-identical to archived 415…; batch-001 input sha
  identical (`6ff2bf50…`, deterministic partitioning); result/package/digest shas differ
  (fresh basis) → new run dir, no old-run rebind. States remain DISCOVERY_COLLECTED
  (no checkpoint write — that needs independent Screening review first).
- **Review seams (root assigns; author self-certifies nothing substantive):**
  SP: accepted `9b979629…` (165, KEEP135/MAYBE20/INSPECT5/DROP5) + package/results/audit/proposed input.
  W34: accepted `e193ad05…` (439, counts as archived) + package copy/inputs/results/reuse provenance.
  Both await independent Screening review + control advance (checkpoint/transition).
  No state/commit/network/production mutation this turn.
