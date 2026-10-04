# DM-003 witness — fresh author-independent review (file-only, no execution)

Reviewer role: fresh author-independent reviewer of DM-003 witness/disposition ONLY.
Not source implementation. No candidate/harness authorship, no agents, no
tests/probes/network/Git mutation, no editing of Worker/root files.
Original 222 shipping untouched. This review executed nothing; it only read files.
No independent HEAD/tree/clean claim beyond file-recorded guards.

Review mode: read-only file review on 2026-10-04 packet context
(`dm003-witness-20261003T200937Z`, task/execution-decision/source-and-cases).
No wall-clock/Git/process execution per task constraint; no fresh
time/HEAD observation is claimed. All pins below are file-recorded values.

## Scope and sources read

- `AGENTS.md` (current entry / boundaries).
- `notes/rephase-1-dm003-witness/task.md`,
  `execution-decision.md`, `source-and-cases.md`.
- Packet `dm003-witness-20261003T200937Z/`:
  `REPORT.md`,
  `run_dm003_witness.py` (689 lines, final),
  `run_dm003_witness.v1.py` (first 100 lines + failure record),
  `evidence-rerun/summary-final.json` (header/canonical/limits, truncated long line),
  `evidence/summary.json`, `evidence/v1-leftover-inventory.txt`,
  `evidence/run-manifest.json`, `evidence-rerun/guard.baseline.json`,
  `evidence-rerun/C1..C5/ops.json`, `C6-R2/ops.json + 2 tracebacks`,
  `C7-R4/ops.json + orphan-vs-report-rows.json`,
  `C1/provenance-paths.json + freeze-record.json + guard.before/after.json`,
  `C5/guard.before.json + state-errors.json + stage traceback`,
  `C4/state-errors.json`.
- Actual 222 source read-only (no execution):
  `scripts/survey_publication_v2.py:171-189` (`_prepare_freeze_inputs`),
  `scripts/survey_stage_validation_v2.py:126-156,159-198,201-212,621-622`,
  `scripts/survey_agent_control_v2.py:387-423,1461-1493`,
  `scripts/survey_profiled_freeze_v2.py:33-64` (`_safe_state_profile`/`build_profiled_freeze`),
  `scripts/survey_reader_publication_v2.py:218-219`,
  `tests/test_survey_dm001_019_freeze_equivalence_v2.py:153,572-626,761-839,908-927`.

## Source pins (file-recorded, not freshly executed)

Candidate identity as recorded in every reviewed guard:
HEAD `222a37e9ee2aa96724a491f2c04c2583a86b9650`,
tree `dbabeed5e70d79b51abb09b64666ca9e1d0fd5dd`,
parent `ff6c67f68e12b3093901248219f2de2872e54d73`,
branch `codex/dm001019-freeze-implementation`,
witness copy `/tmp/opencode/jgas-dm003-witness-20261003T200937Z`.

Five source hashes as recorded in `evidence-rerun/guard.baseline.json`
and repeated identically in reviewed `C1/guard.before.json`,
`C1/guard.after.json`, `C5/guard.before.json`:
- `config/survey-production-v2.json`: `30042258ae01e153507461e51e356c61ae385f1dd33085ca9187586d78fac317`
- `scripts/survey_agent_control_v2.py`: `5e38b86b609e2726f9a3af6f0686426b4237b9d6e388e39d8efc360f6ede4bc0`
- `scripts/survey_profiled_freeze_v2.py`: `092f1a2db8a728684cd2c5bcee80d8ef01e5353091cc03e732e5fc5b10a07c05`
- `scripts/survey_publication_v2.py`: `f3b73d857a7281a45fab807659acd8f7a1d869d52ef05e360af703a7626ceec5`
- `scripts/survey_stage_validation_v2.py`: `0f2393dadab72cecba5672b945d2be35e41089e4face5f0e2753b84a6a4b5806`

No independent git re-assertion was performed. Guard records show
`tracked_changes: []` but `status_lines` contain many `??` untracked entries
(pycache + leftover `SP-DM003-C6/C7` fixture files + rival `main-rival.*`).
REPORT phrase “empty status” is therefore inaccurate; correct scope is
HEAD/tree/parent/branch + tracked-clean + source-hash equality, not fully
clean. Fixture files are untracked by design, so per-scenario repo guards do
not prove fixture no-write; only fixture-level snapshots can.

## Counts and truthful scope (7 scenarios, not 86 tests)

REPORT correctly states “86 recorded operations total across 7 scenarios
(operations, not test methods).” Uphold: 86 is harness `ops.json` entries
(`ok` + `raised-as-expected`), not unittest methods. Do not cite 86 as test
coverage.

Truthful scope supported by genuine evidence:
single `LONGFORM_SPECIAL` scaffold (`SpecialFixture` + real advance/approve
helpers), synthetic upstream/PDF/Human rows, real validators/builders
throughout, no Weekly/all-profile claim, no FROZEN advance in witness
(prior unit). Binding is per-scenario asserted repo guards + op-level
snapshots/tracebacks, not continuous per-module attestation. Canonical map
per `summary-final.json`: C1–C5 → `evidence-rerun/C1..C5`, C6 → `C6-R2`,
C7 → `C7-R4`; other `C6/C7/C7-R2/R3` dirs are superseded retries, not
independent passes.

## Per-scenario assessment: genuine evidence vs overclaim

- **C1 canonical omitted positive.** Genuine: producer creates
  `VALIDATED_DRAFT.json` with `checkpoints == []`; `provenance-paths.json`
  shows 12 refs with orphan absent and named `validation =
  DRAFT_COMPLETE.json` distinct; `validate_agent_state == []`;
  approval binds C1 sha; wrapper Freeze binds exact C1 path+sha
  (`freeze-record.json` path + sha); stage PASS; State identical across
  wrapper (`state_pre_freeze`) and across stage (`state_pre_stage`).
  Overclaim: `inputs-unchanged-across-freeze-admission` op
  (`run_dm003_witness.py:337-340`) captures `cand_pre/appr_pre` AFTER
  stage then immediately compares — tautological. Strike that op as
  no-write proof; genuine input-stability proof requires pre-Freeze capture.
- **C2 sibling removed after advance, before approval.** Genuine: orphan
  deleted post-transition, `validate_agent_state == []`, real
  approve/wrapper/stage PASS, orphan not recreated. This shows consumption
  at transition, not re-discovery, at operation-success level.
  Overclaim: no fixture State/Candidate/approval snapshots before/after
  Freeze/stage exist in `run_c2` (lines 347-378). REPORT “State/inputs
  byte-stable” / “no State/input writes at Freeze” is unsupported beyond
  repo tracked-clean (which ignores `??` fixtures). Correction: PASS
  observed; no-write not demonstrated by fixture bytes.
- **C3 corrupted unreferenced sibling after approval.** Genuine: original
  orphan preserved, corrupted bytes saved, `validate_agent_state == []`,
  C1 bytes checked pre-Freeze, wrapper + stage PASS. Correctly recorded as
  ignored content, not validation of corruption. Same no-write gap as C2:
  no State snapshot across Freeze/stage; byte-stability claim must be
  narrowed to operation success + pre-corruption C1 check.
- **C4 approved-Candidate byte drift.** Genuine and sound: proper
  `state_pre` snapshot (line 431), wrapper rejects with exact
  `ValueError: Production State invalid before Freeze: Publication Preview
  approved candidate bytes drifted`, `freeze/manifest` absent, State
  identical, direct `validate_preview_approval` same drift, State entry
  reports `["Publication Preview approved candidate bytes drifted"]`.
  V2 pin correction (full wrapper prefix) properly supersedes V1
  `evidence/summary.json` C4 `unexpected raised` entry. No correction needed
  beyond retaining V1 raw.
- **C5 disagreeing human-vs-checkpoint refs.** Genuine (stage-only):
  A1/A2 distinct (`A1=...c614fc... A2=...aa626b...`), A2 standalone
  `validate_preview_approval` PASS binding same C1, State deliberately split
  (human→A2, checkpoint A1), `state-errors.json == []`, stage rejects exact
  `StageValidationError: Human Preview and checkpoint approval authorities
  disagree` with raw traceback at `stage_validation.py:139` via
  `_prior_artifacts:160`, no report written, pre-existing Freeze/Manifest
  bytes unchanged, State kept mutated bytes.
  Major overclaim: wrapper NEVER called after split (lines 459-511 call
  wrapper only before mutation, lines 468-469). Freeze/Manifest already
  existed (`freeze_pre/manifest_pre` captured post-wrapper, pre-mutation),
  so “rejects before any write across Freeze operation” and “existing
  outputs unchanged” do not prove fail-closed Freeze. Source shows why this
  matters: `validate_agent_state:403-416` checks only checkpoint-side
  `publication_preview` provenance, never `human == checkpoint`, so `[]`
  on split is current-code behavior; wrapper `_safe_state_profile`
  (`survey_profiled_freeze_v2.py:59-62`) consumes
  `state["human_gate_provenance"]["publication_preview"]` only and
  `_prepare_freeze_inputs` (`survey_publication_v2.py:185-189`) checks
  path+hash binding but not human-vs-checkpoint equality. With A2 binding
  the same C1, a post-split wrapper would likely SUCCEED via human side,
  silently admitting a split. Untested. “Residual observation (not a defect)”
  / “no selected-path blocker” for the wrapper path is therefore
  unjustified. Correct to: stage-entry rejection demonstrated; wrapper/state
  split behavior unknown; residual is a potential narrow defect
  (missing human==checkpoint check in wrapper/state validator),
  not dispositioned.
  Note also A1/A2 both bind the same C1 bytes, so C5 proves
  conflicting-approval-authority rejection at stage, not
  conflicting-Candidate rejection; distinct-Candidate conflict belongs to C6.
- **C6 valid rival, same PDF.** Genuine as a distinct-path same-byte
  boundary: `build_rival_candidate` (lines 250-274) copies identical bytes
  to `publication-candidate-rival-v2.json`, `validate_candidate` PASS, same
  pdf-sha, same sha distinct path; direct `build_freeze(C2,A1)` rejects exact
  `ValueError: ... does not bind the exact Publication Candidate ...`
  before writes (raw traceback at `survey_publication_v2.py:189`, rival
  outputs absent, State identical); surplus stage key rejects exact
  `StageValidationError: unexpected current stage artifacts:
  publication-candidate` at `_current_artifacts:212` via `validate_stage:621`
  (not merge), then correct C1 admission PASS. This validates exact
  path+hash binding (path distinguishes even when sha identical) and the
  extra-key guard, consistent with execution-decision C5/C6 oracle.
  Overclaims: (a) REPORT “content-distinct rival structurally infeasible”
  is false as a general invariant. Prior genuine DM-001/019 evidence at the
  same lifecycle proves byte-distinct same-PDF rivals are feasible:
  `_build_second_chain` / `_build_special_second_chain`
  (`test_survey_dm001_019_freeze_equivalence_v2.py:761-839`) keep same
  source/manuscript/PDF but distinct bundle/reviews/candidate, and
  `test_l4_mixed_candidate_same_pdf_rejected_before_writes` asserts
  `assertNotEqual(sha(c1),sha(c2))` with equal pdf-sha and exact-bind
  rejection. The V1 failure (raw in `evidence/summary.json`) only proves
  one rival-manuscript construction with `main-rival.tex` violates the
  canonical `survey_root/main.tex` rule (`reader:219`); it does not prove
  all content-distinct rivals impossible. Current helper merely copies
  identical bytes (lines 267,271,526), so C6 does not exercise the stronger
  feasible boundary. Correct to: distinct-path same-byte rejection shown;
  byte-distinct same-PDF conflict not exercised. (b) `run_c6:562`
  `snap_file(c1_path)==sha256_file(c1_path)` is same-moment self-comparison,
  tautological; `active-c1-approval-state-unchanged` must require pre/post
  State/approval snapshots, not guards+self-hash.
- **C7 rival orphan ignored.** Genuine: altered orphan schema-valid,
  `orphan-vs-report-rows.json` proves transition-inconsistency (orphan
  `rival-v2.json` vs report `candidate-v2.json`), wrapper + stage PASS on C1,
  State stable (`state_pre` comparison valid). Overclaim determinative:
  `orphan-vs-report-rows.json` shows both rows share sha
  `ec82ad97...` differing only by path, and `run_c7:617` asserts only
  `freeze["publication_candidate_sha256"] == c1_pre`. Same-sha C1/C2 cannot
  be distinguished by sha alone. Winner claim “freeze binds C1; orphan C2
  ignored” is unsupported without path assertion. Correction required:
  assert `freeze["publication_candidate_path"] == C1 rel path` (as C1 does
  at lines 326-327) plus sha; with identical bytes the test as run only
  proves ignored-orphan PASS, not path-sensitive promotion refusal.

No broader generic-resolver repair presumed — REPORT correctly proposes none;
uphold. No DM-004 work justified by this witness; uphold.

## Execution deviations (all must stay preserved)

- V1 raw preserved: rival-manuscript `main-rival.tex` canonical-path
  failures for C6/C7 (`ValueError: Reader primary source must be the
  canonical survey_root/main.tex`), C4 pin mismatch (wrapper prefix), C7
  row-comparison bug, kept in `evidence/summary.json`,
  `v1-leftover-inventory.txt`, and versioned `C6/C7` dirs. Good discipline;
  do not overwrite.
- Unintended full V2 rerun: after switching rival helper to identical-byte
  copy, C1–C5 were rerun wholesale (`evidence-rerun/C1..C5`) though
  `evidence/C1..C5` already COMPLETE. REPORT discloses this as “one
  unintended full v2 rerun kept as `evidence-rerun/C1–C5`.” Canonical mapping
  now points at rerun; duplication inflates the 86-op denominator and creates
  `-R2/R3/R4` versioning (`C6-R2`, `C7-R4`, two pre-existing-path guard
  refusals kept). Retain both generations; do not re-canonicalize by deletion.
- `__pycache__` write into witness copy removed with final status empty:
  disclosed, but it is a post-run untracked-file mutation. Final reviewed
  guards still list `?? __pycache__` and `??` leftover fixtures, confirming
  “empty status” was never achieved; correct isolation claim to
  tracked-clean as above.
- No-overwrite discipline otherwise holds (`write_once`/`versioned`/
  `alloc_dir`, unique `orphan.*`, `state-errors`, tracebacks, snapshots).
  Raw expected/actual exceptions and numeric exits retained via `attempt`
  + `ops.json`. Do not rerun saved harnesses as shipping guards.

## Precise corrections required (vs current genuine evidence)

1. Replace “structurally infeasible” with the narrow truth: one
   rival-manuscript route infeasible per `reader:219`; byte-distinct
   same-PDF rival via distinct bundle/reviews remains feasible per prior
   `_build_second_chain` / L4 and was not exercised. Downgrade C6/C7 as-run
   to distinct-path same-byte boundary.
2. Fix C7 (and C6 final) winner to assert `publication_candidate_path ==
   C1 rel` plus sha; sha-only cannot distinguish same-sha C1/C2.
3. Strike/repair tautological no-write ops: C1:337-340 and C6:562. Require
   pre-Freeze/pre-stage `snap_file` captures for State/Candidate/approval
   with post-op equality; C2/C3 must add missing before/after fixture
   snapshots before claiming byte-stability across Freeze/stage.
4. Restrict C5 claim to stage-entry rejection. Withdraw “before any write
   across Freeze” and “not defect.” Record split-`[]` from
   `validate_agent_state` as current-code observation consistent with
   source (no human==checkpoint check), and wrapper post-split behavior as
   untested and likely admitting (human-side only). Residual is an open
   narrow question, not a closed non-defect.
5. Correct isolation language everywhere from “empty status” to
   “tracked-clean; untracked fixtures/pycache present by design.”
   Keep 86 as operations, not tests.

## Minimal followup matrix (no full-suite rerun)

Do not demand successful control all-suite reruns; C1 core omitted-map
positive, C3 ignored-corruption PASS, C4 drift rejection, C5 stage split
rejection, and C6 path-binding + extra-key rejections stand as operation
evidence subject to above narrowing. Required narrow re-entries only:

- **F1 — real byte-distinct same-PDF rival (C6/C7).** Via
  `_build_special_second_chain` pattern: same issue/Profile/source/
  manuscript/PDF, distinct bundle/reviews/candidate, `validate_candidate`
  PASS for C2, `assertNotEqual(sha(C1),sha(C2))`, equal pdf-sha. Then
  direct `build_freeze(C2,A1)` exact-bind rejection with no rival outputs
  + State unchanged; stage surplus/replace entry per execution-decision
  (extra-key vs merge distinguished); orphan-retarget to C2 with distinct
  sha so winner asserts path+sha == C1. This replaces the infeasibility
  claim with the feasible boundary. Prior identical-byte rejection stays
  as weaker evidence, not discarded.
- **F2 — real C2 no-write + tautology repair (C1/C2/C6).** Fresh C2
  (sibling removed pre-approval): snapshot State/Candidate/approval before
  wrapper Freeze and before stage, compare after; assert orphan still absent.
  Same pre/post pattern to repair C1 `inputs-unchanged` and C6
  `active-unchanged`. No other control rerun needed.
- **F3 — real C5 wrapper entry after split.** Fresh fixture,
  advance→approve→capture/remove Freeze/Manifest so the post-split call is
  tested before any write (use fresh rival output paths or delete
  pre-existing outputs first, recording the removal as setup). Mutate
  human→A2 (standalone valid, same C1) keeping checkpoint A1. Then call
  `profiled.build_profiled_freeze` AFTER split and record exact
  outcome/traceback + before/after State/output snapshots. Compare with
  `validate_agent_state` (`[]` expected per current code) and stage split
  rejection. Outcome decides narrow defect vs phase distinction; do not
  pre-judge “not defect.” If wrapper admits via human side, file as narrow
  defect (missing human==checkpoint gate) before any repair selection.

Any future restore/harness needs fresh hash/member/pack gates, HEAD switch,
and clean/object verification per AGENTS.md; saved runners are
evidence-only, not certified rerun tools.

## Verdict

**CHANGES_REQUIRED** (not `BOUNDED_PASS`, not `no selected-path blocker`).

Genuine evidence supports the omitted-pointer route (typed Preview carries
exact Candidate; `_prior_artifacts` never consults the sibling), ignored
orphan content for removed/corrupted cases at operation level, drift
rejection, stage split rejection, and distinct-path same-byte binding +
extra-key guard. But the five corrections above — especially the false
infeasibility generalization, sha-only C7 winner, tautological/missing
no-write snapshots, and untested C5 wrapper with premature “not defect” —
must be repaired via narrow F1–F3 before any “no selected-path blocker”
disposition or downstream provenance change can be adopted. No generic
provenance repair and no DM-004 work is justified by the witness as it stands.

Author-independence: this reviewer authored no candidate/harness code, ran no
agents/tests/probes, performed no network/Git mutation, edited no
Worker/root files, and makes no independent HEAD/tree claim from headers
alone. New file only; all else untouched.
