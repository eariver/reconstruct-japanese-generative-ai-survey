# DM022 whole-lifecycle witness progress (General)

Author: General (whole-operation witness author/executor, NOT independent reviewer).
Binding: contract `a345bb95` INCLUDING §11, pre-code ROOT `0425c530` INCLUDING §5.2,
coordination `astra-implementation-coordination.md`, `astra-a3-integration-resolution.md`,
author A4 return. Working source:
`.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/candidate-work`
(all runtime authors returned idle). General owns ONLY
`tests/test_dm022_full_lifecycle_v2.py` + `tests/dm022_lifecycle_fixture_v2.py`
plus this progress doc and `evidence/full-lifecycle-v2-*`. No edits to any
existing code/tests/helpers.

## Attempt 1 — 2026-10-28T161838Z (PRIVATE /tmp/dm022-full-lifecycle-private-20261028T120000Z)

Raw: `evidence/full-lifecycle-v2-20261028T161838Z/dm022-full-v2-test-raw-20261028.txt`
(SHA256 `de5b3e5d…`, 602B, exit 0). Manifest 758 files SHA256 `17358b2f…`.
Binding: `evidence/full-lifecycle-v2-20261028T161838Z/full-lifecycle-v2-binding.md`.

### Reached (actual lifecycle APIs, both routes unless noted)

- `high.prepare_revision` + external synthetic decision bind (manifest_ref) —
  WEEKLY + THEMATIC, revision `rev-full-weekly-full-v2` / `rev-full-thematic-full-v2`.
- `high.adopt_revision` → `ADOPTED` + `guard_released` — both routes.
- 7-slot exact inventory: `adopted.seven_plan` has 7 rows, keys `slot`,
  set equals `sel_runner.DM022_SEVEN_SLOTS` and `low.SEVEN_SLOTS`; all
  `absent_legitimate` (fresh fixture, no stale canonical outputs).
- Public strict LIVE validation: `agent.validate_agent_state` == [] after adopt.
- `high.readback_revision` → family `PREARCH`, `triplet` true.
- `low.resolve_research_authority` → `PREARCH`, 4 artifacts; `check_supersession_record_from_paths`
  passes; `require_completion_consistent` + `require_research_operation_ready` pass.
- Old canonical Ledger/Completeness never reused: active refs under
  `/research/v2/acceptance-revisions/`, new Ledger SHA != old canonical SHA,
  active Ledger path != old canonical path.
- Ordinary regeneration: `sel_runner.run` with NEW independent Selection input
  (outside source_root, profile-namespaced roles `WEEKLY_MAGAZINE:`/`WEEKLY:` and
  `LONGFORM_SPECIAL:`/`THEMATIC:`, disposition SELECTED/PRIMARY) →
  `review_readiness READY_FOR_ARCHITECTURE_REVIEW`; all 7 slots present incl audit;
  audit `interactive_input.path` is the generated archive
  (`sources/<issue>/orchestration/...`, not caller input path); archived bytes ==
  caller bytes (copy provenance via path); second `run` refuses `refusing to overwrite`
  (audit no-overwrite proven, no bytes changed).
- Public stage advance: `agent.build_stage_checkpoint` +
  `agent.advance_with_checkpoint` EVIDENCE_REVIEWED→SELECTION_COMPLETE
  (candidate-matrix + candidate-selection, deterministic CORE_STAGE_CONTRACT
  review, recorded_at 2026-10-28T01:00:00Z for monotonic history) — both routes;
  post-advance `validate_agent_state` == [].
- Repeat correction (WEEKLY): rev-full-r1-v2 → rev-full-r2-v2, `ADOPTED` both,
  `parent_checkpoint` binds rev1 FILE sha, `original_anchor` preserved,
  `supersedes` appends rev1; resolver/checker pass on second generation.
- Wrong-role refusal: PREARCH as `publication_revalidation_provenance` refuses
  `DM022_WRONG_FAMILY` via `resolve_publication_mode`; PREARCH as activation
  record refuses via `validate_activation_record`. Old canonical never fallback.
- Own-epoch/current tools retained every readback: fixture Git DBs independent
  (process-scoped identity, inert example.invalid origin, no alternates, meaningful
  synthetic commits); `HEAD`/`tree` pins recorded per attempt; no Status-mutation
  fake advance; no fixture objects in reconstruct; no ordinary commits.
- Production discovery authority truthfully materialized (own helper, not old runner):
  `root/raw/source.json` real bytes + real X manifest (WEEKLY REQUIRED run-001 with
  recorded Grok result binding target-source; THEMATIC NOT_REQUIRED) + real
  `discovery.build_acceptance` + `validate_acceptance` before runner.

### NOT reached (remaining selected scope, no PASS claimed) — Attempt 1 close

- SELECTION_COMPLETE→ARCHITECTURE_ESTABLISHED stage advance +
  genuine-type synthetic ArchitectureGate (`approve_architecture`) into
  Draft/reader — NOT attempted yet in Attempt 1 (see Attempt 2).
- Normal initial publication REAL PDF via TinyTeX lualatex+biber + strict
  receipt/Gate/QA/Candidate — NOT attempted yet.
- Later editorial + renewal Preview/Freeze/Release public APIs — NOT attempted yet.
- G71→G76 unchanged-upstream compatibility control (genuine historical G71
  source epoch + new G76 committed tool epoch) — NOT attempted yet.
- Failure/resume seams beyond adopted-path coverage (late plant, interrupt,
  unknown State are A4-covered; later-lifecycle seams open).

### Blockers / failures this attempt

- None blocking the core witness. Four witness-author fixes within own new files
  only (new raw dir NOT overwritten; private copy re-synced each fix):
  seven_plan key `slot` (not `rel`); Ledger path assertion (R namespace);
  production Discovery acceptance materialization (X manifest + raw bytes);
  profile-namespaced Selection roles; audit path expectation (repo-relative
  `sources/<issue>/...`); monotonic checkpoint timestamp (01:00Z).
  No foreign-scope patches, no downgrades, no toy-count folding.

Next: extend own new tests with Architecture stage + synthetic ArchitectureGate,
then Draft/reader, then REAL PDF publication, stopping at first real blocker with
exact raw/state/fixture + minimal repro returned as owner-code failure to ROOT.
No premature Commit Point / whole PASS.

## Attempt 2 — 2026-10-28T162132Z (same private copy, own tests extended)

Raw: `evidence/full-lifecycle-v2-20261028T161838Z/dm022-full-v2-test-raw-20261028-attempt2.txt`
(SHA256 `ef3a36db…`, exit 0, 4 tests OK in 55.378s). Manifest-attempt2 758 files
SHA256 `2e684ea9…`. Own test file now `49392600…`/50436B (added
`test_weekly_full_to_architecture_approval`); fixture helper unchanged
`dc76b2e7…`. Binding addendum: same base HEAD `409b292…`/tree `8ce36998…`,
same runtime pins (3.14.4 / jsonschema 4.23.0 / pypdf 6.16.2).

### Newly reached (WEEKLY, actual APIs)

- `agent.build_stage_checkpoint` + `agent.advance_with_checkpoint`
  SELECTION_COMPLETE→ARCHITECTURE_ESTABLISHED with the three regenerated
  Architecture authorities (issue-architecture + review-summary + attention),
  deterministic CORE_STAGE_CONTRACT review, recorded_at 2026-10-28T02:00:00Z —
  `lifecycle_state` == `ARCHITECTURE_ESTABLISHED`, strict validation passes.
- Genuine-type synthetic ArchitectureGate: `agent.approve_architecture`
  (reviewer `SYNTHETIC_FIXTURE_REVIEWER_GENERAL_FULL_V2`, explicit nongenuine,
  ref `synthetic-full-v2-architecture-gate`) → `human_gates.architecture_review`
  == `approved`, strict validation passes.
- Adopted PREARCH remains readable after forward progress:
  `high.readback_revision` → family `PREARCH` (no creation-window reimposed on
  later LIVE readback).

### Still NOT reached (no PASS claimed)

- ARCHITECTURE_ESTABLISHED→DRAFT_COMPLETE (drafting-synthesis) → Draft/reader —
  NOT attempted yet (next blocker surface).
- Normal initial publication REAL PDF via TinyTeX lualatex+biber + strict
  receipt/Gate/QA/Candidate — NOT attempted yet.
- Later editorial + renewal Preview/Freeze/Release public APIs — NOT attempted yet.
- G71→G76 unchanged-upstream compatibility control — NOT attempted yet.
- Thematic Architecture approval (WEEKLY proven; THEMATIC same code path but
  not yet witnessed) — open.

### Blockers / failures this attempt

- None. Attempt 1 core witness (3 tests) still green; new Architecture test
  green first run. No foreign-scope edits, no Status-mutation, no old-runner
  reuse, no fixture objects in reconstruct, no ordinary commits.

Next: Draft/reader synthesis witness, then REAL PDF publication, then
editorial/renewal + G71→G76 control, stopping at first real blocker. No
premature Commit Point / whole PASS.

## Attempt 3 — 2026-10-28T163527Z (same frozen private copy, own tests extended; FIRST REAL BLOCKER — owner-code failures, foreign scope NOT patched)

Raw: `evidence/full-lifecycle-v2-20261028T163527Z/dm022-full-v2-test-raw-20261028T163336Z.txt`
(SHA256 `6a1d8963…`, exit 1, 7 tests in 97.441s: 5 ok, 1 error, 1 failure).
Minimal-repro probe + transcript:
`evidence/full-lifecycle-v2-20261028T163527Z/dm022-dual-repro-20261028T163326Z.txt`
(SHA256 `4c9c3ec5…`, probe exit 0, both parts reproduced) and
`dm022-dual-repro-probe.py` (SHA256 `67efd4e6…`, the exact probe source).
Manifest 758 files SHA256 `58fc324e…`. Own test file now `899ff146…`/63094B
(added present-old-slots + thematic-approval + draft tests + shared
`_approve_architecture_for` helper; own-harness `-m` invocation fix and
monotonic-timestamp fixes are setup corrections, not target faults);
fixture helper unchanged `dc76b2e7…`. Same frozen base HEAD `409b292…`/tree
`8ce36998…`, same runtime pins. No foreign-scope edits, no live-candidate
execution, no ordinary commits.

### Still green (5/7)

- Both-route DM022 prepare→adopt→7-slot→regeneration→SELECTION_COMPLETE,
  repeat + wrong-role refusal (Attempts 1–2 scope, unchanged).
- THEMATIC Architecture stage + synthetic Gate (new `test_thematic_full_to_architecture_approval`):
  SELECTION_COMPLETE→ARCHITECTURE_ESTABLISHED→approved, PREARCH readback survives.
  Both-route Architecture approval now witnessed.

### BLOCKER 1 — B-owned runner misroutes LEGACY same-triplet states (disposition §4 present-old-slots case)

- Required case: ordinary selection/architecture run BEFORE adopt on the still
  unaccepted EVIDENCE_REVIEWED graph (no Human presentation anywhere).
- Failure: `run_selection_architecture_v2_interactive.run` line 252 →
  `_dm022_resolve_ledger_completeness` line 78 raises
  `ValueError: PREARCH research resolution did not return PREARCH family`.
- Root cause (read, not patched):
  `run_..._v2_interactive._dm022_is_prearch_state` (triplet path+sha equality
  heuristic) returns True on the LEGACY same-triplet fixture state, while
  `low.resolve_research_authority` (strict kind dispatch) returns LEGACY
  (correct: record kind is legacy, no PREARCH kind). The heuristic and the
  kind dispatch disagree; the runner trusts the heuristic and then refuses the
  resolver's LEGACY answer instead of using the healthy legacy branch
  (`agent.resolve_active_evidence_views` + canonical Ledger/Completeness, all
  verified present/valid in the probe).
- Minimal repro (Part A, probe exit 0): hand-built EVIDENCE_REVIEWED fixture
  state with evidence/materiality/completeness refs identical
  (`checkpoint-evidence.json` sha `8e8a0acb…`), `_dm022_is_prearch_state` True,
  resolve family LEGACY, strict State errors [], legacy 4-ref resolve OK,
  canonical `materiality-ledger-v2.json` (`28f53106…`) and
  `profile-completeness-v2.json` (`7778410e…`) present, runner raises the exact
  ValueError. Exact transcript in the dual-repro file.
- This is a target fault, not a setup fault: the triplet shape (all three refs
  to one record) is what real stage advancement produces
  (`advance_with_checkpoint` writes the same authority to every checkpoint in
  the stage), and no DM022 operation is involved (pre-adopt State). B-owned
  file `scripts/run_selection_architecture_v2_interactive.py`; returned to ROOT,
  foreign scope NOT patched. Disposition §4 present-old-slots case cannot
  proceed until B routes legacy same-triplet states to the legacy branch.

### BLOCKER 2 — screening package basis pins preparation-era State SHA; any later State advance breaks drafting (no DM022 involved)

- Failure: `test_weekly_draft_synthesis_reader` FAIL at the drafting runner:
  `survey_drafting_v2_base.derive_draft_package:461` →
  `_load_drafting_basis:389` → `_resolve_effective_screening_discovery:244` →
  `screening.validate_package_basis:707` raises
  `ValueError: Screening package basis drift: state_sha256`.
- Root cause (read, not patched): `prepare_package` pins
  `basis.state_sha256` = live State file SHA at preparation (ISSUE_INITIALIZED
  era). `validate_package_basis` requires the CURRENT live State file SHA to
  still equal that pin. Every faithful State advance (real
  `build_stage_checkpoint`+`advance_with_checkpoint` or the DM022 hand-built
  EVIDENCE_REVIEWED) rewrites the State file, so drafting can never run after
  any forward progress. No existing test covers drafting-after-advance (all
  drafting/architecture chains keep the init state file byte-identical).
- Minimal repro (Part B, probe exit 0, zero DM022 code, zero hand-built states):
  real `make_screening` at ISSUE_INITIALIZED, ONE real stage advance
  ISSUE_INITIALIZED→DISCOVERY_COLLECTED via public
  `agent.build_stage_checkpoint`+`agent.advance_with_checkpoint`, then the exact
  drafting-basis loader call `screening.validate_package_basis` on the accepted
  package copy → same `state_sha256` ValueError. Exact transcript in the
  dual-repro file.
- Foreign scope (`scripts/survey_screening_v2.py:704-707`,
  `scripts/survey_drafting_v2_base.py:244`); returned to ROOT, NOT patched.
  Blocks the entire downstream witness: Draft/reader → REAL PDF →
  receipt/Gate/QA/Candidate → editorial/renewal → Preview/Freeze/Release →
  G71→G76 control.

### NOT reached behind the blockers (no PASS claimed)

- Present-old-7slots retain/clear/regenerate (blocked by Blocker 1).
- ARCHITECTURE_ESTABLISHED→DRAFT_COMPLETE and Draft/reader (blocked by Blocker 2).
- REAL TinyTeX PDF, strict receipt/Gate/QA/Candidate, editorial, renewal,
  Preview/Freeze/Release, G71→G76 epoch control (all behind Blocker 2).
- A19 helper scope note: existing `test_dm022_prearchitecture_acceptance_v2`
  (19 tests) remains research-operation scope, not a real-PDF claim; not folded
  into this witness count.

### Setup corrections vs target faults (bounded per instruction)

- Own-harness `-m` invocation fix (draft subprocess `ModuleNotFoundError`) and
  probe-side git-init/`--implementation-sha` handling: setup failures, fixed in
  own files only, preserved in transcripts before repair, never counted as
  target faults.
- No late-seam proof from earlier guard refusals is claimed; the two blockers
  are at their actual seams (pre-adopt regeneration, drafting basis load).

Next: blocked on ROOT disposition of Blocker 1 (B runner legacy same-triplet
routing) and Blocker 2 (screening basis vs faithful State advance). On unblock,
continue in own files only: present-old-slots → Draft → REAL PDF (isolated
disposable transfer, exact digest/snapshots) → receipt/Gate/QA/Candidate →
editorial/renewal + Preview/Freeze/Release → G71→G76 epoch control. No
premature Commit Point / whole PASS.

## Attempt 4 — 2026-10-28T183023Z (fresh FIXED snapshot; BOTH Attempt-3 blockers fixed by B; FIRST new blocker in C2 scope)

Scope: B `author-B-lifecycle-correction.md` implemented `astra-lifecycle-blocker-resolution.md`
§§1–2 on B-owned paths only (strict `_dm022_pinned_family` in runner/drafting/handlers/
stage/agent; new `derive_draft_package_from_accepted_state` facade + runner threading;
Screening creation wrapper untouched). Raw pre-manifest 758 files SHA256 `392776b1…`.
Fresh private copy `.rephase-1-editorial-runtime/dm022-full-lifecycle-fixed-20261028T175919Z`
(current ALL intended candidate + General own 2 files, never modified the old failing
private copy). Own test file `2c665f94…`; fixture helper unchanged `dc76b2e7…`.

Raw: `evidence/full-lifecycle-v2-20261028T183023Z/dm022-full-v2-test-raw-20261028T182623Z.txt`
(SHA256 `7793b699…`, exit 1, 9 tests in 226.610s: 8 ok, 1 failure). Manifest 758 files
SHA256 `b65f78e4…`. Binding: `evidence/full-lifecycle-v2-20261028T183023Z/README.md`.
Prior transcripts preserved (Attempts 1–3 dirs intact, nothing discarded/overwritten).

### Reached (actual lifecycle APIs; new this attempt)

- Blocker 1 CLOSED end-to-end: `test_weekly_present_old_seven_slots_retain_clear_regenerate`
  green — ordinary selection/architecture run BEFORE adopt on LEGACY same-triplet state
  (pinned family LEGACY → legacy branch), all 7 old slots written; prepare retains all 7
  exact bytes (present, SHAs match, retained COPYs match, accepted/gate-bound false);
  adopt switches triplet then clears exactly the 7 old slots (`disposition cleared`,
  `captured_sha` attests old bytes); NEW independent Selection input regenerates 7 slots.
- Blocker 2 CLOSED for drafting: ordinary drafting runner now calls
  `derive_draft_package_from_accepted_state` (accepted-state facade, no State SHA pin);
  canonical accepted-Evidence tree mirrored from revised R4 bytes passes the frozen
  raw-authority check. `test_weekly_draft_synthesis_reader` green (WEEKLY ARCHITECTURE_
  ESTABLISHED → DRAFT_COMPLETE with synthesis-input/result + paired draft-package/
  draft-result checkpoint artifacts).
- THEMATIC Architecture approval green (both-route approval now witnessed).
- WEEKLY Reader → REAL PDF → strict admission green
  (`test_weekly_publication_real_pdf_to_validated_draft`): independent derivation input
  bound to approved synthesis → surface-only materialization → explicit synthetic surface
  review → full render (main.tex/references.bib/jgaisurvey.sty/validated-source-manifest)
  → REAL lualatex+biber PDF in an isolated disposable dir (every step pid/exit/log-tail
  recorded; `%PDF` magic + pypdf page count asserted) with exact byte transfer to the
  canonical survey root → manuscript manifest (BIBLIOGRAPHY+STYLE closure) → deterministic
  QA bundle over the exact real source/PDF → explicit synthetic SEMANTIC_EDITORIAL +
  VISUAL reviews (never genuine) → reader-surface gate → stage checkpoint with all 7
  DRAFT_COMPLETE artifacts → VALIDATED_DRAFT, strict State valid, PREARCH readback survives.
- WEEKLY Candidate → Preview → Freeze green within `test_weekly_candidate_to_released`:
  `build_candidate` from exact reviewed bytes, publication-candidate checkpoint →
  RELEASE_CANDIDATE, synthetic Preview approval, `build_freeze` pair, freeze checkpoint
  (freeze-record + release-manifest + candidate pre-preview visual-review-record) →
  FROZEN; `build_merge_verification` + `build_release_record` succeed on exact bytes.

### BLOCKER 3 — C2 release CLI refuses legitimate PREARCH research lineage (foreign scope, NOT patched)

- Failure: `test_weekly_candidate_to_released` ERROR at the release-checkpoint CLI
  (pid recorded in transcript): `DM022_WRONG_FAMILY for release checkpoint: PREARCH
  research node refused at completeness (expected FROZEN->RELEASED release)`.
- Exact site: `scripts/survey_release_checkpoint_v2.py:68-81`
  (`build_release_checkpoint`; identical gate in CLI `main`): loads every
  `checkpoint_provenance` entry via `low.load_typed_checkpoint_record` and raises on
  ANY PREARCH family — including the adopted research triplet
  (evidence/materiality/completeness), which is permanent after adoption.
- Why this is overbroad (read, not patched): R6 site 15
  (`integrated-readiness-r6-role-map.json` row n=15, `release:121 validate_instance`)
  selects refusal for a PREARCH record *supplied as the release checkpoint payload*
  (FROZEN->RELEASED + freeze/manifest/record artifacts). Research roles with a valid
  PREARCH record must be ADMITTED: R6 site 2 (`agent:489` — ADMIT iff expected
  checkpoint in {evidence,materiality,completeness}), contract §11.2 (normal forward
  publication transitions must continue to validate and consume the adopted
  checkpoint), ROOT §3 (publication walkers use the detached research-history
  validator at upstream nodes). The CLI payload here IS FROZEN->RELEASED; the
  refusal fires on upstream research lineage, so no DM022-adopted issue can ever
  reach RELEASED through this CLI.
- Returned to ROOT with exact function + verbatim traceback + pid; C2-owned
  `survey_release_checkpoint_v2.py` (B-doc §5 cross-owner note on the sibling
  gate validator stays untouched by General). No foreign edit, no test adaptation
  to a wrong runtime.

### NOT reached behind Blocker 3 (no PASS claimed)

- RELEASED advance (CLI blocked; merge-verification + release-record files built OK).
- THEMATIC Reader → REAL PDF → admission (THEMATIC arch approval green; longform
  render path not yet attempted).
- Later editorial + renewal Preview/Freeze/Release public APIs (need VALIDATED_DRAFT —
  reachable; renewal activation path is distinct from the blocked FROZEN CLI).
- G71→G76 unchanged-upstream compatibility control with genuine historical G71
  source epoch (needs renewal path + read-only final93 proof copy; not membership
  counts).

### Setup corrections vs target faults (bounded per instruction)

- Own-harness/input fixes only (unique log, failures preserved): seven_plan
  `captured_sha`/`disposition` keys; draft block PARAGRAPH + runner `run_reference`;
  discovery acceptance (not JSONL) as State artifact; closure-member fixture copy
  imported from runtime modules; canonical accepted-Evidence tree; draft/freeze
  checkpoint artifact sets; manuscript BIBLIOGRAPHY+STYLE closure; empty
  architecture coverage matching empty must-cover requirements.
- No late-seam proof from earlier guard refusals claimed; Attempt-3 dual-repro
  (Part A/B) transcripts preserved in the Attempt-3 evidence dir.

Next: blocked on ROOT/C2 disposition of Blocker 3 (release CLI research-role
admission). On unblock, continue in own files only: RELEASED → THEMATIC full
publication → later editorial/renewal + G71→G76 epoch control. No premature
Commit Point / whole PASS.

## Attempt 5 — 2026-10-28T202317Z (C2 release fix verified; overlay copy; BOTH routes REAL initial publication → RELEASED; renewal/G71-G76 parked awaiting C1)

Scope: C2 `author-C2-release-fixture-correction.md` narrowed the release gate
(research trio allowed; wrong-role validation/freeze/release/pub-pointer still
refuse) + corrected P1/P2R/P2V fixture closures (53+new7). New frozen copy
`.rephase-1-editorial-runtime/dm022-full-lifecycle-fixed2-20261028T192129Z`
= prior fixed witness + KNOWN exact 4-file C2 overlay (SHAs verified
`a5e84668…`/`36ca8afe…`/`403beeed…`/`cf7a5bd5…`; file list identical; old
snapshots preserved, never modified; candidate whole NOT captured — C1 history
wiring editing live). Pre-manifest 758 files SHA256 `258331f1…`.

Raw: `evidence/full-lifecycle-v2-20261028T202317Z/dm022-full-v2-test-raw-20261028T201654Z.txt`
(SHA256 `d4c9c422…`, exit 0, 12 tests in 372.629s: 12 ok). Post-manifest 758
files SHA256 `c5a9d2ed…`. Binding: `evidence/full-lifecycle-v2-20261028T202317Z/README.md`.
Own test file `e26eaa6b…` (+3 THEMATIC release/retain/log-dir fixes since Attempt 4);
fixture helper unchanged `dc76b2e7…`. Prior transcripts preserved (Attempts 1–4 dirs
intact; retained run dirs accumulate under `evidence/full-lifecycle-v2-retained/`,
14+ runs, never overwritten).

### Reached (actual lifecycle APIs; new this attempt)

- Blocker 3 CLOSED end-to-end (C2 narrow gate): WEEKLY FROZEN→RELEASED via the
  ordinary release-checkpoint CLI with upstream PREARCH trio resident
  (`test_weekly_candidate_to_released` green; terminal COMPLETE, strict State
  valid, PREARCH readback survives; wrong-role publication pointers still refused
  by C2 narrow gates — helper-scope negatives preserved, not counted as positive).
- THEMATIC full normal lifecycle green on the same copy:
  DM022→7-slot→regen→SELECTION_COMPLETE→Architecture approval (synthetic Gate,
  clear label)→Draft (accepted facade)→DRAFT_COMPLETE→longform render→REAL
  lualatex+biber PDF (isolated disposable, pid/exit/full-log per step, `%PDF` +
  pypdf asserted, exact transfer)→author inspect loop (explicitly NOT independent
  visual)→manuscript (THEMATIC FINAL_SYNTHESIS bound to exact TeX block)→QA→
  synthetic SEMANTIC/VISUAL reviews→gate→VALIDATED_DRAFT→Candidate→Preview
  approval→Freeze→merge-verification + release-record→release-checkpoint CLI→
  RELEASED (`test_thematic_candidate_to_released` green).
- Both routes genuine-type Synthetic Human Gates with clear labels (Architecture
  + Preview approvals all `SYNTHETIC_FIXTURE_*`, never genuine).
- Retained per route+run (later independent all-page inspection): real PDFs
  (WEEKLY 5 pages/68KB, THEMATIC per-run), main.tex/bib/sty, FULL TeX logs
  (commands/pids/exits, not tails), transferred digests, author inspections,
  QA/manifest/review/gate JSONs + retained-manifests.

### NOT reached (reported then waiting — no foreign patch, no downgrade)

- Later editorial + versioned renewal Preview/Freeze/Release: needs C1's pending
  H-positive (tool-commit-predates-CP fixture + H verifier + S source proof +
  renewal graph) and affected batch incl. full P3S 26 (~2210s), per
  `author-C1-historian-wiring-correction.md` §§4–5. Current C1-old would block
  renewal; per instruction no renewal witness attempted against uncorrected C1,
  no C1 files touched, no old-runner reuse. Await C1 availability.
- G71→G76 unchanged-upstream compatibility control with genuine historical G71
  source epoch (read-only final93 proof copy) + new G76 committed tool epoch
  (not membership counts): needs C1's corrected renewal machinery above.
- Other workers' regression exec stays frozen elsewhere; General touched ONLY
  the 2 own files in candidate-work (SHAs above, identical in snapshot).

### Setup corrections vs target faults (bounded per instruction)

- Own-harness/input fixes only (unique logs, failures preserved): `-D###` locator
  sanitization for reader-visible URLs, synthetic entity canonical-name without
  embedded IDs, fidelity-block reader locations parsed from rendered TeX,
  THEMATIC deterministic QA family (+EMPTY_WRAPPER_SUPPRESSION) and
  LONGFORM review evidence sets from `reader._expected_review_checks`,
  author-inspect/log dirs out of the surveyed build directory.
- C2 release CLI now passes with upstream PREARCH trio resident — the Attempt-4
  Blocker 3 is closed, not worked around (no test adaptation to a wrong runtime).

Next: on C1 availability, editorial + versioned renewal + G71→G76 epoch control
in own files only. No premature Commit Point / whole PASS.

## Attempt 6 — 20261028T213412Z (prePreview exposure for C1 PhaseS; editorial/renewal probed to precise foreign blockers; G71 base verified)

Scope: astra-historian-execution-resolution (delete invented absence-at-epoch gate;
preserve fingerprints; new source-bound fixtures; later-operation witness stops at
VALIDATED_DRAFT/prePreview, no rewind). Work under KNOWN snapshot fixed2 (old H);
new fixed copy with latest H/S awaits C1 change message + root coordination (NOT
created here; live candidate never captured while C1 edits history wiring). Own
2 files only (`e26eaa6b…` + helper `dc76b2e7…`).

Raw: `evidence/full-lifecycle-v2-20261028T213412Z/` (manifest test
`44b4bc1f…` exit 0; renewal probe `68c43312…` exit 2; P1 probes `b34e8a84…` +
`618be8d0…` exit 2; probe sources preserved; post-manifest `e8fa9f65…`, 758
files). Binding: `evidence/full-lifecycle-v2-20261028T213412Z/README.md`.
Definitive 12-test transcript stays Attempt-5 `dm022-full-v2-raw-20261028T201654Z`
(`d4c9c422…`, exit 0, 12/12); nothing re-run unnecessarily, nothing overwritten.

### Reached

- Fresh both-route prePreview fixtures + packet manifest for C1 PhaseS pointers
  (`test_expose_prepreview_fixture_manifest_both_routes` green): stops normal
  public path at VALIDATED_DRAFT (no RELEASED rewind/old-State fake), corrected
  PREARCH active + readback, real PDFs retained; manifest
  (`../full-lifecycle-v2-fixture-manifests/prepreview-both-routes-<UTC>/`)
  documents construction entry points, canonical rel paths, key SHAs/lifecycle/
  refs, toolchain (TinyTeX abs path), synthetic-review labels — C1 pointer
  update needs no adopted old artifact metadata.
- Retained PDFs/full TeX logs (commands/pids/exits, not tails) keep accumulating
  run-unique under `evidence/full-lifecycle-v2-retained/` (15+ runs) for later
  independent all-page inspection; author inspect loops stay labeled NON-independent.

### Precise foreign blockers (preserved raw+fixture, NOT patched)

1. Editorial P1 entry: `agent.revalidate_publication_surface` (REVIEWED_CORE_CHANGE)
   on adopted VALIDATED_DRAFT → B-owned `_verify_preserved_provenance`
   (`survey_agent_control_v2.py:2517`) refuses the PREARCH research node:
   `revalidation basis checkpoint completeness invalid: ... 'from_state' is a
   required property`. The walker demands legacy checkpoint shape for the adopted
   research triplet instead of dispatching it to the detached research-history
   validator (ROOT §3; cf. same overbreadth class as closed Blocker 3). For root
   disposition: B walker gap vs. editorial-on-adopted uses a different basis path.
   (First probe error `pending publication requires changed publication bytes` was
   probe-setup — fixed by a genuine marker byte change, preserved in transcript.)
2. Renewal U `prepare_renewal` on fresh VALIDATED_DRAFT (no prior versioned set):
   `BASIS_ENTRY_INELIGIBLE: State pointer must select a nonnull versioned active
   set` — correct gate for re-renewal; first-activation bootstrap is C1's pending
   dual-epoch work (needs A2-style tool-predates-CP fixture + H-positive +
   affected batch incl. source_phase_s 3 faults per C1 integration doc §6).
3. G71→G76 control: G71 base verified read-only available (final93 proof-copy,
   HEAD `409b292…`, actual409/tree8ce). Dual-epoch renewal run awaits C1's
   renewal construction + root disposition; no fixture DB created from it here.

Next: on C1 availability (H-positive dual-epoch application to General-helper
VALIDATED_DRAFT + affected batch + root disposition of (1)–(3) above), continue
in own files only: editorial P1/P3S/publication on adopted state → renewal U/C →
G71→G76 epoch control. No premature Commit Point / whole PASS.

## Attempt 7 — 20261028T222347Z (fixed3 with C1 epoch-presence H/S; P1→P2R→P2V→P3S green; editorial prepare blocked on C2 hardcoded G71 closure count)

Scope: C1 `author-C1-epoch-presence-correction.md` (absence gate deleted, stage-checkpoint
fingerprint `a1b97759…` kept, G76 `71d67aa9…`/presence `a8ce8794…` greens) overlaid onto
KNOWN snapshot fixed2 → fresh fixed3 (10 C1 paths; file list otherwise identical; B agent
file untouched/disjoint; pre-manifest 758→759 files SHA256 `e28f31f1…`). Own 2 tests only
(`0daa7ef9…` + helper `dc76b2e7…`; fixture copies whole scripts/config/templates/.github
+ dotfiles for session control roots, plus closure members imported from runtime).
Raw: `evidence/full-lifecycle-v2-20261028T222347Z/` (editorial staged run
`6b9c4810…` exit 1 at prepare with verbatim C2 traceback + pid + full subprocess
stdout/stderr in retained dirs; P1/P2R/P2V/P3S setup-failure raws preserved, never
overwritten). Binding: same-dir README. Post-manifest 759 files SHA256 `de991a8e…`
(only own test file delta `8c7901db…`→`0daa7ef9…`; no runtime edits, no hot-edit of
admitted fixture tools).

### Reached

- WEEKLY P1 correction proposal on adopted VALIDATED_DRAFT with a REAL revised
  reader scope (corrected deck, not a fake Core reason): prepare → `REVIEW_REQUIRED`.
- P2R retention capture (`RETAINED_SET_CAPTURED` + manifest; 17 copy/72 keep refs).
- Scope review (explicit synthetic nongenuine) → P2V `CURRENT_BASIS_OBSERVED_SCOPE_BOUND`.
- P3S staged4 materialized via fresh fixture-code subprocess (fixture-bound runtime
  modules; pid/exit/full raw recorded, unique run dirs).
- Misclassification corrected per instruction: `agent.revalidate_publication_surface
  (REVIEWED_CORE_CHANGE)` is canonical R1 mechanical revalidation, NOT P1's
  prerequisite — R1 attempt on adopted state preserved as probe (B walker refuses
  PREARCH shape; B fixes its walker independently); editorial does NOT park on it.

### BLOCKER (foreign, C2-owned, NOT patched — first actual blocker on this path)

- Editorial `prepare_publication` → P3S staged verification → `CLOSURE_SHAPE:
  editorial closure expected 63, got 70` (`survey_editorial_publication_v2.py:2163`,
  `_editorial_closure_rows`). The route deps are generation-aware (C1 P3S 63/70);
  the count predicate hardcodes G71. C2-owned fix (derive expected count from route
  family or drop count for exact membership — same class as C1's generation fix).
  Blocks editorial prepare→reviews→finalize→activate→VERSIONED_ACTIVE → renewal
  U/C (+ normal release) → G71→G76 control.
- Renewal U entry `BASIS_ENTRY_INELIGIBLE` without prior VERSIONED_ACTIVE is
  EXPECTED correct entry behavior (not a bug, not a C1 block); first-activation
  bootstrap is C1's pending dual-epoch work + my VERSIONED_ACTIVE fixture.
- R1-on-adopted refusal and THEMATIC P1/editorial/draft scope remain open behind
  the blockers above; G71→G76 control awaits C1 renewal + root disposition
  (G71 base verified read-only: final93 proof-copy, HEAD `409b292…`).

### Setup corrections vs target faults (bounded)

- Own-harness/input fixes only (unique logs, failures preserved): fixture support
  copy (scripts/.github/dotfiles for session control roots); P2R result literal;
  runtime binding via fresh fixture-code subprocesses (C1 precedent, not old runners);
  editorial spec/toolchain authoring per schema with real TinyTeX paths.
- No late-seam proof from earlier guard refusals claimed; no test-count sums.

Next: blocked on C2 (closure generation-awareness) + C1 (dual-epoch renewal) + root
disposition. On unblock, continue in own files only: editorial finalize/activate →
readback → renewal U/C → normal release → G71→G76 control. No premature Commit
Point / whole PASS.

## Attempt 8 — 20261029T012936Z (NEW General; C2 CURRENT-only 3a87 + C1 H/S + B R1 fixed; editorial + U activation green; post-renewal release foreign blocker)

Scope: fresh frozen copy `.rephase-1-editorial-runtime/dm022-full-lifecycle-attempt8-20261029T012936Z`
(760 intended files, 0 `__pycache__`, 83 git files, HEAD `409b292…`/tree `8ce36998…`,
inert `example.invalid`, no alternates, 0 inode overlap vs candidate (new inodes),
no `GIT_*`, process-scoped identity). Pins for every run:
C2 `3a8721569d3cb1512501699ecf78d7c7e3679120cfb9b06504fa1471bfdee722`
(CURRENT-only, no OWN fallback), H `a9de2c97…`, S `b139f493…`,
stage `a1b97759…`, B `b6506a8b…` (R1 PREARCH preserved walker),
own test `7c5b55ae…` (was `0264ea5a…` before Attempt8 harness fixes) +
helper `dc76b2e7…`. Candidate-work own 2 files synced at close
(`7c5b55ae…` + `dc76b2e7…`). Prior fixed/fixed2/fixed3/fixed4 + all Attempt1–7
evidence dirs preserved, never overwritten. Previous whole initial 12/12 (Attempt5)
was older qualified composite; NOT claimed as new full-run transfer.

Raw: `evidence/full-lifecycle-v2-20261029T012936Z/` (headers + pins + exit codes,
unique raws, never overwritten):
- `dm022-full-v2-test-raw-20261029T013026Z.txt` (editorial finalize/activate,
  exit 0, 1 test in 387.763s) — CURRENT70 prepare + reviews + finalize + activate.
- `dm022-full-v2-test-raw-20261029T014500Z.txt` (U first, exit 1, 440.905s) —
  `HISTORY_TOOL_EPOCH_DRIFT old must differ from new` (no new tool commit yet).
- `dm022-full-v2-test-raw-20261029T020500Z.txt` (U with new epoch, exit 1, 459.789s) —
  harness `setmod` NameError (own-code, fixed, preserved).
- `dm022-full-v2-test-raw-20261029T021500Z.txt` (U with setmod fix, exit 1, 459.538s) —
  harness `cfg` NameError (own-code, fixed, preserved).
- `dm022-full-v2-test-raw-20261029T023000Z.txt` (U with cfg fix, exit 1, 465.141s) —
  `BASIS_CURRENT_TOOL_DRIFT loaded history module wrong root` in in-process
  Preview (own-harness scope, fixed via fixture-subprocess release helper).
- `dm022-full-v2-test-raw-20261029T030000Z.txt` (U with fixture release, exit 1, 512.720s) —
  FOREIGN `build_freeze` PREARCH trio refusal (see Blocker below, NOT patched).
- `dm022-full-v2-test-raw-20261029T032000Z.txt` (expose both-route prePreview,
  exit 0, 1 test in 109.343s).
- `dm022-full-v2-test-raw-20261029T033000Z.txt` (durable fixtures, exit 0, 1 test
  in 436.240s).
Binding: same-dir `pins-before-attempt8.json` + `header-attempt8-editorial.txt`.
Retained run dirs accumulate under `evidence/full-lifecycle-v2-retained/` (112+ dirs,
unique, never overwritten) + `evidence/full-lifecycle-v2-fixture-manifests/`
(prepreview + durable manifests, unique).

### Reached (actual runtime, TinyTeX REAL PDFs, synthetic nongenuine reviews)

- Fresh both-route canonical VALIDATED_DRAFT/prePreview green
  (`test_expose_prepreview_fixture_manifest_both_routes`, exit 0, 109s):
  normal public initial path stops at VALIDATED_DRAFT (no RELEASED rewind),
  adopted PREARCH active + readback, real PDFs retained, toolchain
  `/home/eariver/.TinyTeX/bin/x86_64-linux/lualatex+biber` from start.
- WEEKLY editorial full chain green
  (`test_weekly_editorial_finalize_activate`, exit 0, 387s):
  P1 changed-reader correction REVIEW_REQUIRED → P2R RETAINED_SET_CAPTURED →
  external synthetic scope → P2V CURRENT_BASIS_OBSERVED_SCOPE_BOUND → P3S staged4
  (fresh fixture-code subprocess) → `prepare_publication` REAL new TinyTeX PDF
  (CURRENT70 closure, CURRENT-only admission 3a87) → external synthetic
  postrender semantic/visual reviews exact new manuscript/PDF →
  finalize Candidate+seal → activate VERSIONED_ACTIVE → normal strict readbacks
  (PREARCH family, mode VERSIONED_ACTIVE). R1 `revalidate_publication_surface`
  NOT used as P1 prerequisite (misclassification preserved per instruction);
  `prepare_renewal` correctly requires VERSIONED_ACTIVE (no pending-bootstrap).
- WEEKLY renewal U prepare→finalize→verify→activate green (new tool epoch):
  genuine new meaningful fixture tool commit (`sources/renewal-tool-epoch-*.json`,
  non-closure path, `fixture_commit`, old HEAD != new HEAD, no empty commit,
  process-scoped identity) satisfies REUSED_BUILD old != new;
  `u_prepare_finalize` exit 0, `u_verify` CURRENT_PROOF_VALID true,
  `u_activate` exit 0 mode VERSIONED_ACTIVE (all in fixture-code subprocesses,
  pid/exit/raw preserved). Proof CURRENT on every readback via detached
  `verify_renewal_source_proof` (no caller-verified dict, no pending).
- DURABLE prePreview fixtures stable for C1 (exit 0, 436s,
  `test_expose_durable_versioned_fixture`):
  `.rephase-1-editorial-runtime/dm022-durable-validated-prepreview-20261029T023302Z`
  (HEAD `4d990f9d…`, VALIDATED_DRAFT, CANONICAL mode, REAL PDF 68035B) and
  `.rephase-1-editorial-runtime/dm022-durable-versioned-active-prepreview-20261029T023302Z`
  (HEAD `f289de07…`, VALIDATED_DRAFT lifecycle + VERSIONED_ACTIVE mode via
  `resolve_publication_selection`, REAL TinyTeX PDF, PREARCH trio same-record).
  Packet `full-lifecycle-v2-fixture-manifests/durable-versioned-20261029T023302Z/
  durable-fixture-manifest.json` exposes actual existing root + source/db pins
  (HEAD/tree/state SHA/set_rel/toolchain), NOT manifest-to-TempDirectory path.
  No GitDB in packet, no old toolchain record rewrite. Kept stable for C1 HighU2
  (AVAILABLE TinyTeX, NOT legacy absolute path).

### BLOCKER (foreign, C2-owned, NOT patched — exact for root)

- Post-renewal normal Preview→Freeze→Release refuses in
  `scripts/survey_publication_v2.py:791 _prepare_freeze_inputs`:
  `ValueError: renewal checkpoint wrapper evidence+materiality+completeness
  from/to/checkpoints mismatch: None->None ['evidence','materiality','completeness']`.
- Cause (read, not patched): renewal freeze loads retained State
  `checkpoint_provenance` evidence/materiality/completeness (DM022-adopted
  PREARCH trio, same path+sha `.../acceptance-revisions/.../checkpoint/record.json`,
  a research record with no `from_state`/`to_state`) as a stage-checkpoint
  wrapper expecting `CANDIDATES_NORMALIZED->EVIDENCE_REVIEWED` with
  `checkpoints==[evidence,materiality,completeness]`. The grouped PREARCH file
  has `None->None`, so the exact predicate refuses. This is the same overbreadth
  class as closed Blocker 3 (research trio vs legacy shape), now in C2 freeze
  (not release). Blocks post-renewal Preview/Freeze/Release to RELEASED for
  DM022-adopted issues (both U and C, since both use same retained provenance).
  Initial publication Preview/Freeze/Release to RELEASED remains green per
  Attempt5 (older composite, not transferred); editorial activation (no freeze)
  and renewal U activation (no freeze) are green above.
- Returned with exact function (`_prepare_freeze_inputs`), verbatim traceback
  (512s raw `...T030000Z.txt` + retained `...-renew-release-20261029T022138Z/`
  `stdout/stderr/meta`), bound fixture (durable VERSIONED_ACTIVE HEAD `f289de07…`,
  retained COPY + PREARCH trio same-record). No foreign edit, no predicate waiver,
  no Status-mutation fake advance.

### NOT reached (no PASS claimed)

- C-route (RENDER_TARGETS new build + new postrender reviews + finalize/verify/activate):
  driver design mapped (prepare + `prepare_renewal_targets` + external reviews +
  finalize with new checks), NOT yet witnessed (needs another ~600s TinyTeX chain).
- G71→G76 unchanged-upstream compatibility control (genuine old G71 + new G76 tool
  commits, SAME Evidence/Profile/Architecture/Draft/reader, CURRENT proof new70):
  old base verified read-only (final93 proof-copy HEAD `409b292…`, pipeline71),
  new base candidate G76 (+2 modules +5 schemas), no fixture DB created yet.
  Needs C1 renewal construction + root disposition of freeze blocker if release
  is required; CURRENT proof alone (no freeze) is feasible via existing
  `verify_renewal_source_proof` detached path.
- THEMATIC editorial/renewal, repeated C→U→U, normal post-renewal release to
  RELEASED (blocked above), full 12-test rerun (not claimed as transfer).

### Setup corrections vs target faults (bounded, preserved)

- Own-harness fixes only (unique raws, failures preserved, never counted as target):
  `setmod` import in `_run_fixture_renewal` driver, `cfg`/`source_root` bindings
  in U test, fixture-subprocess release helper (`_run_fixture_renewal_release`
  with cwd=fixture root for Layer-B module-root binding + CLI cwd=fixture),
  genuine new tool-epoch committer (`_commit_new_tool_epoch`, non-closure intent
  file, `fixture_commit`, old != new), durable copier (`copytree` no pycache,
  HEAD/tree/alternates/origin checks). No late-seam proof from guard refusals;
  no test-count sums; no inherited cleanup (fixed3/fixed4 + all prior raws intact).

Next: on root/C2 disposition of freeze PREARCH-trio handling, continue in own
files only: C-route activation (no release until unblocked) → G71→G76 CURRENT-proof
control (no release) → repeated U (new epoch, terminal EXECUTED) → post-renewal
release (after fix) → THEMATIC editorial/renewal. Keep durable fixtures stable;
no premature Commit Point / whole PASS. Root unit ongoing.

## Attempt 9 — 20261029T040000Z+ (NEW General; THEMATIC + C green before Preview; artifact vs genuine documented; G71 genuine still open)

Scope: same frozen `attempt8-20261029T012936Z` (pins C2 `3a872156`, H `a9de2c97`,
S `b139f493`, B `b6506a8b`, own `6622550d…` + helper `dc76b2e7…`; candidate own
2 files synced at close). C2 Freeze fix in progress in candidate (own files only,
no snapshot of C2 until return; privately recorded pins above). Prior Attempt8
(659 lines) preserved; new raws unique, never overwritten.

Raw: `evidence/full-lifecycle-v2-20261029T012936Z/` continued:
- `...T040000Z` (THEMATIC editorial pre-fix, exit 1, 57s) — P1 `GATE_RECEIPT_SHAPE`
  (own-harness THEMATIC gate DIRECT_PRIMARY, fixed, preserved).
- `...T042000Z` (THEMATIC VALIDATED_DRAFT with fixed gate, exit 0, 59s).
- `...T043000Z` (THEMATIC editorial pre-fix, exit 1, 239s) — `MANUSCRIPT_BUILD`
  LONGFORM location `["main.tex"]` (own-harness, fixed to exact section).
- `...T044000Z` (THEMATIC editorial pre-fix, exit 1, 240s) — `ARCHITECTURE_CONTENT_FIDELITY`
  missing `package:pkg-core` (own-harness generic evidence, fixed to longform mapping).
- `...T045000Z` (THEMATIC editorial, exit 0, 377s) — THEMATIC P1→P2R→P2V→P3S→
  REAL TinyTeX PDF (CURRENT70, CURRENT-only) → longform postrender reviews
  (exact section/package/density evidence) → finalize → VERSIONED_ACTIVE.
- `...T051000Z` (THEMATIC U before Preview, exit 0, 455s) — new epoch (artifact,
  see below) → `u_prepare_finalize` + `u_verify` CURRENT_PROOF_VALID true +
  `u_activate` VERSIONED_ACTIVE.
- `...T052000Z`/`...T053000Z`/`...T054000Z` (WEEKLY C before Preview fails then green,
  414s/413s/500s) — `NameError _new_pubdir` (own, fixed) → `renewed manuscript
  requires explicit renewal proof context` (own, fixed via `renewal_proof` ref in
  `reviews_explicit`) → exit 0 with new build + exact new reviews (no old rebind).
- `...T060000Z`/`...T061000Z` (THEMATIC C before Preview, 496s+; exit 0) — same
  new-build + longform evidence + renewal proof context, CURRENT proof + activate.

### Reached (before Preview, no Freeze — independent of C2 Freeze fix)

- THEMATIC editorial to VERSIONED_ACTIVE green (377s): P1 (fixed gate with receipt
  binding via `reader-surface-input`, not DIRECT_PRIMARY) → P2R → P2V → P3S →
  REAL TinyTeX PDF → longform postrender reviews with exact evidence
  (`ARCHITECTURE_CONTENT_FIDELITY→package:pkg-core`,
  `LONGFORM_TECHNICAL_DEPTH→package+density`, `FINAL_SYNTHESIS_QUALITY→final_loc+role+package`,
  `LONGFORM_MIXED_LAYOUT→wide/one-column/balanced`, det 4 with `EMPTY_WRAPPER_SUPPRESSION`)
  → finalize → VERSIONED_ACTIVE, PREARCH readback.
- THEMATIC renewal U before Preview green (455s): artifact new epoch (see below) →
  prepare/finalize/verify CURRENT true → activate VERSIONED_ACTIVE, PREARCH readback.
- WEEKLY renewal C before Preview green (500s): artifact new epoch → `c_prepare`
  (RENDER_TARGETS + toolchain TinyTeX) → `c_targets` (new trio/manuscript/REAL
  disposable build + receipt, EXECUTED_BUILD) → new det checks (3, exact new paths)
  + new semantic/visual reviews at exact new `renewal-c-v2/` paths (NOT old editorial
  paths, even equal SHA; `renewal_proof` ref passed to `build_review_record` for
  renewed manuscript) → `c_finalize` → `c_verify` CURRENT true → `c_activate`
  VERSIONED_ACTIVE, PREARCH readback.
- THEMATIC renewal C before Preview green (496s): same with THEMATIC requirements
  (FINAL_SYNTHESIS exact section `_floc3` from validated main.tex), det 4,
  longform evidence (package/density/final_loc/layout) at exact new paths,
  renewal proof context, CURRENT true, VERSIONED_ACTIVE.
- Exact new-review paths: C reviews written to `.../publication/renewal-c-v2/`
  (new det/sem/vis + deterministic-checks.json), never `.../publication/`
  editorial paths; old reviews KEEP exact (no rebind, no overwrite).

### Artifact vs genuine (IMPORTANT correction, no overclaim)

- Prior ` _commit_new_tool_epoch` (non-closure `renewal-tool-epoch-*.json` + `git add -A` +
  `fixture_commit`) advances fixture HEAD (`old != new`, 40-hex, no empty commit,
  process-scoped identity) and satisfies U REUSED_BUILD `old != new`, BUT it is
  **artifact HEAD advance, NOT genuine changed tool**: diff is exactly one new
  non-closure intent JSON + committed working-tree state (editorial VERSIONED_ACTIVE
  files); control-set (70 CURRENT closure: 2 modules +5 schemas + pipeline76 +
  stage `a1b97759…` + Contract8) is byte-identical old vs new (verified via
  `_verify_current_tools_committed` CURRENT closure member-wise + `basis.current_tool_epoch`
  recompute; no tool file SHA/mode change, no config pipeline change).
  Documented exact diff in retained `...-renew-u_activate-*/meta.json` (pid) +
  `git show --stat HEAD` in fixture (intent file + state). Do NOT claim tool change
  outside controls; genuine G71→G76 control below requires real delta.
- Same for C artifact epochs (same non-closure intent, same closure preserved).
  C new trio bytes DO change (NEW_TARGETS, `trio_equal False`, EXECUTED_BUILD with
  real disposable TinyTeX build + transfer + receipt), but tool closure (70) is
  unchanged (same G76). Genuine tool change (G71→G76: pipeline71→76 + 7 renewal +
  7 DM022 files + Contract8 + 5 schemas) is separate control, NOT claimed here.

### NOT reached / open (no PASS claimed)

- Genuine G71→G76 unchanged-upstream compatibility control (REAL delta, SAME upstream,
  FULL CURRENT proof, every readback):
  old base read-only final93 proof-copy (HEAD `409b292…`, 742 files, pipeline71,
  7 renewal files, no DM022) vs new candidate G76 (760 files, pipeline76 +2 modules
  +5 schemas + Contract8, stage `a1b97759…` pinned). Requires: fresh independent
  fixture DB, G71 source commit (final93 tools, TinyTeX from start, meaningful
  ancestry/source commits before authority, no fake legacy proof JSON/manual count),
  G71 initial+editorial via true G71 helpers (if normal Draft hits old Screening
  StateSHA bug — final93 has pre-B screening pin, candidate B fix `derive_draft_package_from_accepted_state`
  MUST NOT be patched into G71 epoch; label as G71 compat control, NOT whole G71
  public Draft witness; synthetic nongenuine approvals allowed typed complete),
  then SAME fixture new commit installing REVIEWED G76 intended files (real delta,
  old Evidence/Profile/Architecture/Draft/reader/reviews KEEP exact, prove via
  live re-hash + `check_supersession_record_from_paths` + LOW typed loader),
  public `prepare_renewal`/`prepare_renewal_targets`/`finalize_renewal`/
  `verify_renewal_source_proof` CURRENT70 + `activate_renewal` VERSIONED_ACTIVE,
  verify every readback (PREARCH family + CURRENT closure member-wise + contract).
  Independent review §8 is source-feasibility only, NOT runtime approval.
  If true existing renewal entry CURRENT old proof blocks real changed tools
  (unlike first VERSIONED_ACTIVE expected `BASIS_ENTRY_INELIGIBLE` gate),
  return exact actual call graph (unlike artifact `old!=new` gate above);
  do NOT downgrade genuine epoch test to artifact commit.
  For G76 C mode: new trio + new manuscript/PDF + new external reviews at exact
  new R paths (never rebind old reviews even equal SHA — already proven above
  for same-G76 C; same discipline for G71→G76 C).
- Repeat C→U→U in SAME fixture (source byte changes → new trio): C (EXECUTED) →
  U1 (REUSED, terminal C EXECUTED, new epoch) → U2 (REUSED, terminal C EXECUTED
  skipping U1 REUSED, new epoch), preserving old CURRENT proof controls
  (detached `verify_renewal_source_proof` CURRENT on every readback, no pending/
  verified-dict, no fake intent reason). Have C + U separately (same-G76, artifact
  epochs); chained C→U→U with genuine delta still open.
- Post-renewal normal Preview→Freeze→Release to RELEASED (FOREIGN C2 Freeze
  `evidence+materiality+completeness` PREARCH-trio wrapper bug, Attempt8 §BLOCKER;
  C2 fixing, needs new CURRENT proof to consume changed code, NOT pinned old proof
  bypass). Independent THEMATIC/WEEKLY U/C before Preview above do NOT park on it.
- Existing durable fixtures (`dm022-durable-*-20261029T023302Z`) MUST NOT mutate
  old source in place behind proof; new independent copies for new runs with
  source committed before data/new epoch honest (already: durable are stable,
  new runs use fresh Temp fixtures + new durable only on explicit expose, never
  in-place edit).

### Setup / harness fixes (bounded, preserved)

- THEMATIC gate: `surface_review` (reader-surface-input, LONGFORM_SPECIAL, receipt
  binding) not `surface_sem` on `main.tex` (DIRECT_PRIMARY, no receipt) — own-harness.
- THEMATIC manuscript/renewal specs: exact section `_final_loc` from validated
  `main.tex` via `fidelity.parse_longform_blocks` (not `["main.tex"]`).
- THEMATIC reviews: `reviews_explicit` driver op with `renewal_proof` ref for
  renewed manuscripts + longform evidence mapping (package/density/final_loc/layout)
  + det 4 (with `EMPTY_WRAPPER_SUPPRESSION`); WEEKLY keeps generic + det 3.
- C drivers: `c_prepare`/`c_targets`/`c_finalize`/`c_verify`/`c_activate` in
  `_run_fixture_renewal` (fixture binding, cwd=fixture, pid/exit/raw unique);
  `reviews_explicit` accepts `renewal_proof` for C (exact new paths, no old rebind).
- All raws/setup failures preserved (57s P1 gate, 239s manuscript location, 240s
  fidelity evidence, 268s det family, 414s `_new_pubdir` typo, 413s renewal proof
  context); no cleanup/reset/network/old-runners/Human readback/ordinary commits.

Next: genuine G71→G76 control (real delta, SAME upstream, FULL CURRENT70, every
readback) + chained C→U→U (preserved controls) in own 2 files only, new packet
dirs (never overwrite durable/stable). On C2 Freeze fix, new CURRENT proof run
to consume changed code (not pinned old proof). No healthy-half stop; unit ongoing.

## Attempt 10 — 20261029T040600Z+ (NEW frozen with C2 Freeze fix f0486c54; WEEKLY C→U→U to FROZEN green, release CLI new VERSIONED blocker; new durable both-route green)

Scope: NEW frozen `.rephase-1-editorial-runtime/dm022-full-lifecycle-newfreeze-20261029T040600Z`
(761 files = 760 + C2 new test, 0 pycache, 83 git, HEAD `409b292…`, inert origin,
no alternates, 0 inode overlap vs candidate (new inodes), no `GIT_*`,
process-scoped identity). Pins for every run (recorded in
`evidence/full-lifecycle-v2-newfreeze-20261029T040600Z/pins-before-*.txt`):
C2 Freeze `f0486c54e8a6e1579d0c9a5edefcee3bd712f066341040b3c1aaa8bdeff86960`,
C2 editorial `3a872156…`, H `a9de2c97…`, S `b139f493…`, stage `a1b97759…`,
B `b6506a8b…`, own `554ffa06…` (was `6622550d…` before chained + durable both-route)
+ helper `dc76b2e7…`; candidate own 2 files synced at close (`554ffa06…`).
Prior frozen attempt8 + all Attempt1–9 raws/retained/durable preserved, never
overwritten. Separate G71–G76 General owns new control 2 files — NOT duplicated
here, its `dm022-g71-g76-durable-20261029T044241Z` preserved untouched.
Old `dm022-durable-*-20261029T023302Z` (old source, old Freeze) preserved, never
mutated in place.

Raw: `evidence/full-lifecycle-v2-newfreeze-20261029T040600Z/` (headers + pins +
exit codes, unique raws, never overwritten) + `evidence/full-lifecycle-v2-retained/`
(new `weekly-full-cuu-*` + `*-rel-cli-*` + `...-renew-*` dirs, unique) +
`evidence/full-lifecycle-v2-fixture-manifests/durable-versioned-*/` (new).

### Reached (new source, CURRENT every readback, PREARCH every readback)

- WEEKLY C→U→U same fixture to FROZEN green (870s,
  `dm022-weekly-cuu-raw*.txt` exit 1 at release CLI only; Freeze to FROZEN passed):
  editorial VERSIONED_ACTIVE (REAL TinyTeX, CURRENT70, CURRENT-only) →
  C (RENDER_TARGETS + TinyTeX toolchain, `c_prepare` → `c_targets` new trio/manuscript/
  REAL disposable build + receipt EXECUTED_BUILD, exact new `renewal-c-v2/` det/sem/vis
  with `renewal_proof` ref, no old rebind, `c_finalize` → `c_verify` CURRENT true →
  `c_activate` VERSIONED_ACTIVE, PREARCH readback, C EXECUTED terminal preserved) →
  U1 (artifact new epoch, re-hash C det exact clone, `u_prepare_finalize` →
  `u_verify` CURRENT true → `u_activate` VERSIONED_ACTIVE, terminal C EXECUTED,
  PREARCH readback, old ref stable, exact U targets, current-before unchanged full
  research/Profile/Architecture/Draft/reader) →
  U2 (artifact new epoch, same C terminal skipping U1 REUSED, same CURRENT/verify/
  activate/readback) →
  normal Preview/Freeze to FROZEN green (new C2 Freeze UPSTREAM trio branch for
  PREARCH `evidence+materiality+completeness` same-record + FULL LOW/H/S + snapshot
  binds + CURRENT G76, no quiet stale; `_run_fixture_renewal_release` fixture-bound
  + release-manifest/merge-verification, lifecycle FROZEN, strict validation passes).
  Proves C2 Freeze fix consumes new CURRENT proof (fresh source-before-data fixtures
  from latest full source, NOT pinned old proof reuse).
- New durable both-route VERSIONED_ACTIVE prePreview green (875s,
  `dm022-durable-newfreeze-raw.txt` exit 0):
  `dm022-durable-validated-prepreview-{weekly,thematic}-20261029T051100Z` (VALIDATED_DRAFT,
  CANONICAL, REAL PDFs) + `dm022-durable-versioned-active-prepreview-{weekly,thematic}-20261029T051100Z`
  (VALIDATED_DRAFT lifecycle + VERSIONED_ACTIVE mode via `resolve_publication_selection`,
  PREARCH trio same-record, REAL TinyTeX PDFs, independent DBs no hardlinks, no alternates,
  inert origin, source committed before data). Manifest
  `.../durable-versioned-20261029T051100Z/durable-fixture-manifest.json` with actual
  sources/self-contained DB outside packet (durable paths) + content pins (HEAD/tree/
  state SHA/set_rel/toolchain f0486c54 + relevant PDF targets only: final initial/
  editorial per route; 120+ intermediates preserved in retained dirs, NOT required
  for visual inspection). For C1 HighU2 (AVAILABLE TinyTeX, NOT legacy path).
  Old durable `...023302Z` preserved (old source), never mutated; new durable stable,
  no dangling Temp paths (Temp fixtures byte-copied to durable with own DB, no hardlinks,
  preserve history).
- THEMATIC C→U→U + Release same pattern as WEEKLY (same drivers, longform evidence,
  det 4, exact section) — code complete in own 2 files (`554ffa06…`), NOT yet rerun
  with new source (WEEKLY proves Freeze fix + new blocker; THEMATIC expected same,
  open to rerun next, no healthy-half stop).

### New foreign blocker (C2-owned release-checkpoint, NOT patched — exact for root)

- Post-C→U→U release CLI to RELEASED refuses:
  `unknown checkpoint kind refused: 'VERSIONED_RENEWAL_ACTIVATION_V1'`
  (`survey_research_authority_v2.py:354` via `survey_release_checkpoint_v2.py:93-94`
  `load_typed_checkpoint_record(publication_revalidation_provenance)`).
- Cause (read, NOT patched): after renewal U2 activation, State
  `publication_revalidation_provenance` = `.../publication-surface-revalidation-r4.json`
  (U2 VERSIONED activation record, kind `VERSIONED_RENEWAL_ACTIVATION_V1`, r4 = editorial+C+U1+U2).
  Release-checkpoint loads it via LOW (which knows ONLY LEGACY stage + PREARCH research,
  NOT VERSIONED) to check PREARCH wrong-role, but LOW refuses unknown kind before
  family check. Expected: VERSIONED activation is valid (current active renewal, NOT
  wrong-role PREARCH); release FROZEN→RELEASED with VERSIONED_ACTIVE prior should admit
  it (via `validate_activation_record`, NOT LOW research loader) or skip LOW for VERSIONED.
  Freeze to FROZEN already green above (new Freeze UPSTREAM branch handles PREARCH trio);
  only release CLI blocked. Initial RELEASED (Attempt5 older composite, NOT transferred)
  had LEGACY revalidation pointer (no renewal), so unaffected.
- Returned with exact function (`release_checkpoint:93-94` → LOW `:354`), verbatim one-line
  `stderr.txt` + `pre-release-state-snapshot.json` (validation/freeze/release refs + kinds:
  validation `DRAFT_COMPLETE.json` kind null (LEGACY stage), freeze `RELEASE_CANDIDATE.json`
  kind null (LEGACY stage), release null (FROZEN, not yet RELEASED), evidence/materiality/
  completeness PREARCH same-record `9be31c52…`, publication_preview approval, lifecycle FROZEN)
  in retained `weekly-full-cuu-rel-cli-20261029T045410Z/` (pid 3207547/3339147, exit 2),
  bound fixture (pre-release FROZEN State + r4 VERSIONED record + retained COPY + PREARCH trio).
  No foreign edit, no predicate waiver, no fake intent (artifact epochs labelled, NOT genuine).
  If required real Core change for selected truthful reason, high checks force fail — report
  real error (here: release-checkpoint LOW), do NOT fabricate intent; genuine G71 control
  separate covers actual tool update.
- Wrong-role refusals unaffected (PREARCH as `publication_revalidation_provenance` still
  refuses `DM022_WRONG_FAMILY` where expected; here pointer is VERSIONED, NOT PREARCH,
  so wrong-role test still passes — verified in chained test post-RELEASED checks would-be,
  but RELEASED blocked above; PREARCH readback + CURRENT proof every readback preserved).

### NOT reached / open (no PASS claimed)

- THEMATIC C→U→U + Preview/Freeze/Release to RELEASED with new source (same code as
  WEEKLY, longform evidence, det 4; WEEKLY proves Freeze fix + new release blocker;
  THEMATIC expected same blocker, open to rerun next).
- Genuine G71→G76 control (separate General, NOT duplicated here).
- Post-C→U→U RELEASED terminal COMPLETE (blocked by new release-checkpoint VERSIONED
  blocker above; Freeze to FROZEN green proves Freeze fix; needs C2 release-checkpoint
  VERSIONED handling, then new CURRENT proof rerun, NOT pinned old proof).
- Full 12-test rerun NOT claimed as transfer (old composite preserved).

### Setup / pins (bounded, preserved)

- New frozen 761f/0 pycache/83 git, pins before each run (`pins-before-weekly-cuu.txt`,
  per-run `header` + `stdout/stderr-raw` + `exit-code`), pre/post `scripts HEAD` + file
  counts (own test code changes between runs recorded as separate pins `6622550d…` →
  `554ffa06…`, no fixed source overclaim). Full TeX/PDF/raw/setup failures unique
  (864s/870s C→U→U + 875s durable, TinyTeX REAL PDFs/logs/digests/semantic/visual
  synthetic nongenuine retained, old 120+ preserved). No network/Production/ordinary
  commits/Human readback/Gitconfig/old-runner/cleanup. C2 editing candidate untouched
  except own 2 files (synced at close). No G71 files written.

Next: on C2 release-checkpoint VERSIONED disposition, rerun THEMATIC C→U→U + both-route
Preview/Freeze/Release to RELEASED terminal COMPLETE (new CURRENT proof, NOT pinned old),
then independent review. Keep new durable stable; no premature Commit Point. Unit ongoing.

## Attempt 11 — 20261029T053058Z+ FINAL (new snapshot 764f b9433b9e/705bcee3/dd01fa01; BOTH routes C→U→U → RELEASED/COMPLETE green; new durable both-route green; no new blocker)

Scope: NEW private exec `dm022-full-lifecycle-final-20261029T053058Z` from FINAL
review snapshot `snapshot-review-20261029T053058Z/worktree` (764 intended files,
0 pycache, 83 git files, HEAD `409b292…`, inert origin, no alternates, 0 inode
overlap vs snapshot (new inodes), no `GIT_*`, process-scoped identity; manifest
`60aaaee8539f69432a01d0ad72c1131b23951fd87a5531981876642d877eceee`/158161B/764
entries). Pins for every run (`evidence/full-lifecycle-v2-final-20261029T053058Z/
pins-before-*.txt`): C2 Release decoder `b9433b9e…`/14505, publication `705bcee3…`/
155658 (contains correct old COPY pub decoder, replaces old `f0486c54…`), refresh
`dd01fa01…`/96623, editorial `3a872156…`, H `a9de2c97…`, S `b139f493…`, stage
`a1b97759…`, B `b6506a8b…`, own `373e6b98…` (was `554ffa06…` before final chained +
durable both-route + fixture final-checks) + helper `dc76b2e7…`; candidate own 2
files synced at close (`373e6b98…`, 4538 lines). Prior f048 frozen + Attempts1–10
raws/retained/durable preserved, never overwritten, no PASS transfer (old f048
evidence kept, new run needed C2 source 3 changed). Separate G71–G76 General owns
new control 2 files — NOT duplicated here, its `dm022-g71-g76-*-20261029T*` durables
preserved untouched. All runtime writers idle, independent read-only review in parallel
(snapshot, NOT candidate) — used snapshot worktree, NOT live candidate, for new exec
(source-before-data fresh fixtures from latest full source).

Raw: `evidence/full-lifecycle-v2-final-20261029T053058Z/` (pins + `dm022-weekly-final*.txt`/
`dm022-thematic-final*.txt`/`dm022-durable-final*.txt` + exits, unique UTC, never
overwrite) + `evidence/full-lifecycle-v2-retained/` (new `*-cuu-*` + `*-rel-cli-*` +
`*-final-checks-*` + `...-renew-*`, unique) + `evidence/full-lifecycle-v2-fixture-manifests/
durable-versioned-20261029T064541Z/` (new, both-route).

### Reached (BOTH routes, new source, CURRENT+PREARCH every readback, REAL built PDFs)

- WEEKLY C→U→U → RELEASED/COMPLETE green (1000s, `dm022-weekly-final-raw.txt` exit 0):
  editorial VERSIONED_ACTIVE (REAL TinyTeX CURRENT70, CURRENT-only) →
  C (RENDER_TARGETS + TinyTeX, `c_prepare` → `c_targets` new trio/manuscript/REAL disposable
  build + receipt EXECUTED_BUILD, exact new `renewal-c-v2/` det/sem/vis with `renewal_proof`
  ref, no old rebind, `c_finalize` → `c_verify` CURRENT true → `c_activate` VERSIONED_ACTIVE,
  PREARCH readback, C EXECUTED terminal preserved) →
  U1 (artifact epoch, re-hash C det exact clone, `u_prepare_finalize` → `u_verify` CURRENT true →
  `u_activate` VERSIONED_ACTIVE, terminal C EXECUTED, PREARCH readback, old ref stable, exact U
  targets, current-before unchanged full research/Profile/Architecture/Draft/reader) →
  U2 (artifact epoch, terminal C skipping U1, same CURRENT/verify/activate/readback) →
  normal public Candidate/direct Preview/Freeze/Release (fixture-bound Preview/Freeze to FROZEN
  with new Freeze UPSTREAM trio + CURRENT G76 + snapshot binds; release CLI to RELEASED with new
  Release proper pub decoder `b9433b9e` handling VERSIONED activation as valid prior (NOT LOW
  research loader); lifecycle RELEASED, terminal COMPLETE (where present), strict
  `validate_agent_state` [] via fixture final-checks (module-root binding), PREARCH readback,
  wrong-role PREARCH as validation/publication still refuses `DM022_WRONG_FAMILY`). Real built PDFs
  retained (initial/editorial/C + TeX/log/manuscript/review/digest, synthetic nongenuine).
- THEMATIC C→U→U → RELEASED/COMPLETE green (990s, `dm022-thematic-final-raw.txt` exit 0):
  same with THEMATIC specifics (FINAL_SYNTHESIS exact section `_fl0/_floc` from validated main.tex,
  det 4 with `EMPTY_WRAPPER_SUPPRESSION`, longform evidence package/density/final_loc/layout at exact
  new paths + renewal proof, no old rebind, CURRENT true every readback, PREARCH every readback,
  VERSIONED_ACTIVE → FROZEN → RELEASED/COMPLETE, strict State, wrong-role unaffected).
- New durable both-route VERSIONED_ACTIVE prePreview fresh latest source green (872s,
  `dm022-durable-final-raw.txt` exit 0):
  `dm022-durable-{validated,versioned}-*-{weekly,thematic}-20261029T064541Z` (VALIDATED_DRAFT
  CANONICAL + VERSIONED_ACTIVE prePreview (no Preview, no FROZEN State rewrite), PREARCH trio
  same-record, REAL TinyTeX PDFs, independent DBs no hardlinks, no alternates, inert origin,
  source-before-data). Manifest `.../durable-versioned-20261029T064541Z/durable-fixture-manifest.json`
  with actual root/Git/source/tree/State+activeSet+Raw/PDF/review target pins (HEAD/tree/state SHA/
  set_rel/toolchain `b9433b9e/705bcee3/dd01fa01` + relevant PDF targets only: final initial/editorial/C
  per route + TeX/log/reader/manuscript exact SHA; U same-byte reuse needs NO duplicate visual;
  120+ intermediates preserved in retained dirs, NOT required for inspection). For C1 PhaseS U2
  (NOT after FROZEN copy). Old durables preserved, never mutated; new durables stable, no dangling
  Temp paths (Temp fixtures byte-copied to durable with own DB, no hardlinks, preserve history).
  DB kept outside packet (durable paths), no GitDB in packet, content pins only.
- Artifact epoch truthful (non-closure intent JSON + working-state commit, old != new for U REUSED_BUILD,
  same 70 closure byte-identical, no tool SHA/mode/pipeline change; C new trio bytes DO change via REAL
  build, tool closure unchanged same G76). No genuine claim; genuine G71→G76 owned separately (in progress
  final Release, NOT duplicated). If required real Core change for selected truthful reason, high checks
  force fail — no new failure here (all green); do NOT fabricate intent.
- Previous f048 frozen evidence kept, no PASS transfer; new run needed (C2 source 3 changed:
  `b9433b9e` Release proper pub decoder + `705bcee3` publication with correct old COPY (replaces `f0486c54`)
  + `dd01fa01` refresh). New CURRENT proof consumed new code (fresh fixtures from new snapshot, NOT quiet
  reuse of old proof against new files).

### Setup / pins (bounded, preserved, no fixed overclaim)

- New exec 764f/0 pycache/83 git, pins before each run (`pins-before-weekly-final.txt`,
  `pins-before-durable-final.txt`, per-run `header/cmd/runtime/PID/exit` + full TeX logs/PDF/source
  pre/post raw, unique UTC; scripts HEAD/private file count pre/post (own test `554ffa06…` →
  `373e6b98…` between runs recorded as separate pins). Full RAW unique all steps (1000s+990s+872s,
  TinyTeX REAL PDFs/logs/digests/semantic/visual synthetic-nongenuine, old hundreds preserved).
  No state rewind/tool pin bypass/hotpatch Frozen fixture (fresh source-before-data, all authority real
  exact paths, external nongenuine reviews). No network/Production/ordinary commits/Human readback/
  Gitconfig/old-runner/cleanup. C2 editing untouched except own 2 files (synced, no whole snapshot until
  return). No G71 files written. No all-test count sum (exact per-test Ran/OK only).

Next: independent review (parallel, snapshot `60aaaee…`); no premature Commit Point. Unit ongoing, all required
capabilities done (both-route C→U→U → RELEASED/COMPLETE + new durable both-route prePreview + relevant PDF
manifests). Return no new blocker (all green).
