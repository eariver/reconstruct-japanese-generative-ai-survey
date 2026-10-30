# C2 A4-regression correction — scoped status (no Commit Point)

2026-10-28 UTC. Owner C2 (publication/editorial consumers). This unit implements
ONLY the A4-disposition C2 items; no ordinary commits, no Human readback, no
network, no Git config mutation, no live-candidate test execution, no old-runner
reuse. A3/B/C1 files untouched. LOW (`survey_research_authority_v2.py`) NOT
edited (narrow A Path-str coercion fix lands separately).

## 1. What A4 found in C2 scope, and what changed

A4 diagnostics (integration-a4-20261028T160708Z) reported for C2: new test
`test_finalize_entry_refuses_with_guard` failed at `MISSING_ANCESTOR` (fixture
lacked the proposal ancestor, so no READY seam was proved); readerGate (20) +
publication (7) fixture failures all hit missing-State lstat (`production state
lstat failed`) instead of their content/quality oracles; release CLI had the
`str`-path `AttributeError`. Root disposition for C2:

- C2 owns the new finalize guard test + the 27 readerGate/publication fixture
  failures (missing State). DO NOT change LOW missing-State handling to
  legacy permission.
- Update the two legacy C2 test files with synthetic schema-valid
  Profile-bound State via the real `core.initial_state` constructor; preserve
  the original content/quality negative oracles; do NOT fake genuine approved
  full State (fixtures are unit context, not a full publication witness).
  Keep a distinct missing/unreadable-State guard refusal test.
- Runtime public-writer State derivation must use canonical Profile exact SHA
  + config state path; malformed source profile fails closed.
- C2 finalize guard test: do NOT widen the regex to cover the preemption;
  make a healthy public fixture positive, then plant guard at the intended
  entry/prepublish seam, prove no writes, assert the exact typed error. Same
  for activate/resume/candidate/gate tests with broad regexes.
- `validate_refresh_validation_checkpoint` must keep the full anchor checks as
  real legacy controls (not shape-only acceptance on State mismatch).
- New tests + existing C2 files only. Private fixed copy for C2 target
  regressions from saved A4 snapshot + C2 correction ONLY.

## 2. C2 source changes (2 files, exact)

- `scripts/survey_weekly_mechanical_refresh_v2.py`:
  `load_typed_checkpoint_record(root, Path(validation_ref["path"]))` (was str;
  A4 LOW expects `Path`, A-side coercion lands separately — C2 callers pass
  `Path` per contract either way).
- `scripts/survey_release_checkpoint_v2.py`: same `Path(...)` wrap.
- `validate_refresh_validation_checkpoint` keeps the full legacy anchor chain:
  exact ref shape, repository-local safe file, SHA drift check, explicit
  PREARCH wrong-family refusal (exact `reason`, never `reason_class`), full
  LOW typed validation, stage-checkpoint schema validation, then
  issue/from/to/checkpoints identity (State mismatch still refuses). No
  behavior weakened; the lightweight classification now uses duplicate-refusing
  strict parse to match its documented contract.

No other runtime files touched. HIGH sole-mutator rule untouched; detached
validators still require no guard; writers still require READY entry+prepublish.

## 3. C2 test changes (4 files)

- `tests/test_survey_dm022_c2_consumers_v2.py`: new
  `validate_refresh_validation_checkpoint` healthy-legacy test copies the real
  `schemas/stage-checkpoint-v2.schema.json` into the fixture (valid legacy
  checkpoint passes PUBLIC validator, no writes); writer tests rebuilt on a
  healthy P1+P2R+scope fixture proven past the entry READY seam (positive
  fails strictly later at editorial-receipt validation, never a guard error),
  then a planted guard refuses with exact
  `DM022_TRANSITION_ACTIVE: [FINALIZE|ACTIVATE|RESUME/REFUSED_PRE_WRITE]` or
  `DM022_TRANSITION_ACTIVE: guard present` (candidate/gate) with no writes;
  new distinct missing-State test (no legacy fallback). No broad regex, no
  early-preemption counting, no helper-only or mocked-validator cases.
- `tests/test_survey_reader_surface_gate_v2.py` and
  `tests/test_survey_publication_v2.py`: fixtures now write a synthetic
  schema-valid Profile-bound State via the real `core.initial_state`
  constructor (ISSUE_INITIALIZED, no Human decisions, no checkpoint
  provenance, no reviews). Original content/quality negative oracles
  preserved byte-for-byte in intent; each file gains an explicit
  missing-State test proving fail-closed READY (`lstat failed`), not silent
  legacy permission.
- `tests/test_survey_execution_record_v2.py`: same synthetic-State treatment
  (module validators stay mocked for their own logic; the real State file
  serves READY only).

## 4. Private fixed-copy regression evidence (A4 snapshot + C2-only overlay)

- Base: `snapshot-a4-20261028T160708Z/worktree` (756 files, manifest
  `2eb615b41307e86cc86770c9f4ba259e2626f88c4e898f3672a2cdc86621`) +
  byte-copied `.git` (83 objects, HEAD `409b292`, inert
  `example.invalid` origin, 0 inode overlap both trees).
- Overlay: exactly the 6 C2 files above (SHA256-pinned in
  `evidence/integration-c2-a4fix-20261028T171309/source-pin.txt`;
  candidate-work copies verified byte-identical post-sync).
- Pre/post invariant held: 756 worktree files, 0 `__pycache__`, no fixture
  objects in reconstruct, process-scoped Git identity, inert origin, no
  network, no commits.

| run | file | ran | pass | fail | err | exit |
|-----|------|-----|------|------|-----|------|
| 01 | test_survey_dm022_c2_consumers_v2 | 17 | 17 | 0 | 0 | 0 |
| 02 | test_survey_reader_surface_gate_v2 | 28 | 28 | 0 | 0 | 0 |
| 03 | test_survey_publication_v2 | 9 | 9 | 0 | 0 | 0 |
| 04 | test_survey_release_checkpoint_v2 | 9 | 9 | 0 | 0 | 0 |
| 05 | test_survey_execution_record_v2 | 5 | 5 | 0 | 0 | 0 |
| 06 | test_survey_agent_control_v2 (sanity) | 5 | 5 | 0 | 0 | 0 |
| 07 | test_survey_active_evidence_views_v2 (sanity) | 2 | 2 | 0 | 0 | 0 |
| 08 | test_run_selection_architecture_v2_interactive (sanity) | 2 | 2 | 0 | 0 | 0 |

Raw logs + per-run headers + exit codes:
`notes/rephase-1-dm022-prearchitecture-implementation/evidence/integration-c2-a4fix-20261028T171309/run-*-stdout-stderr-raw.txt`
(+ `-header.txt`, `-exit-code.txt`). Intermediate iteration failures (missing
schemas copy, relative-path resolution against CWD, guard file counted in
snapshot) were fixed in-place and are superseded by the final green runs;
final diffs are limited to the intended C2 files (verified byte-identical
candidate-work ↔ private copy at run time).

Positive-phase seam proof (no guard): finalize fails strictly later at the
editorial-receipt missing-file check; activate fails at the prepared-set
schema check; resume fails at the activation-record schema check; candidate
fails at the manuscript-schema check; gate fails at the missing
semantic-review check — each with NO `DM022_TRANSITION_ACTIVE` and no
writes, proving the entry READY seam was passed. Guard phase then refuses
with the exact typed error above and no canonical writes.

## 5. Concrete call matrix (writers: READY entry + prepublish; diagnostics: no guard)

- `finalize_publication`: READY entry after scope-bound + prepublish checks
  before bundle/Gate/candidate/seal writes (unchanged code paths, now
  exercised by a healthy P1+P2R+scope fixture).
- `activate_publication`, `resume_activation`: READY entry + pre-State
  READY (unchanged code; tests now prove the seam instead of tripping the
  earlier fixture-shape error).
- `build_candidate`, `build_preview_approval`, `build_visual_review`,
  `build_freeze`, `build_manuscript_manifest`, `build_review_record`,
  `evaluate_reader_surface_gate` (when writing), `refresh_mechanical_evidence`,
  `build_release_checkpoint`, execution-record `initialize`: unchanged READY
  entry+prepublish; new/updated tests prove each seam fails closed on a
  planted guard and passes READY without one.
- `validate_reader_surface_gate` (diagnostic): NO READY by design — detached
  read-only validation MUST work while a transition guard is held (HIGH
  post-State validation calls it with state bound). Read-only validators
  (`validate_*`, retained-history verification, P2V observation) never take
  the guard; only mutating writers do. No optional readiness bypass flag was
  added anywhere.
- Runtime State derivation (`_dm022_state_from_manuscript`,
  `_dm022_canonical_state_path`, per-file equivalents) binds the canonical
  State via validated Profile exact SHA + config `state_authority`
  authoritative filename; malformed source profile fails closed. No
  generic verified-dict or no-State fallback.

## 6. Real remaining blockers / explicit non-claims

- P1/P2R/P3S/renewal tests were NOT run here (left for the next task per root
  instruction); C2-owned P1 test helpers were reused as-is for fixtures.
- A4's narrow LOW Path-str coercion fix lands separately; C2 call sites now
  pass `Path` objects, which is correct with or without it. LOW itself was
  NOT edited here.
- The new `validate_refresh_validation_checkpoint` keeps the full legacy
  behavior (schema + identity) and adds explicit PREARCH wrong-family refusal
  before CANONICAL fallback; unknown/malformed records still fail closed and
  are never treated as legacy.
- No whole-lifecycle witness is claimed; this correction covers the A4 C2
  regression scope only (defined writer/validator seams + affected legacy
  suites). No Commit Point taken; unit remains open per root.
