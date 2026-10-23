# Worker B lifecycle R3c — BOTH Weekly + Longform VALIDATED_DRAFT r2 → RELEASED

TEST ONLY, NO SOURCE EDITS. Frozen SOURCE `0d9857e6132fb314a2e2ba141da79c54f4ec5e06` tree `44cbfc1864d269e338bdbd6060305e5fd558060` 718 tracked.
Positives (no Preview yet, VALIDATED_DRAFT r2 active + real 5pp PDF):
- Weekly `/tmp/opencode/jgas-weekly-r3c-20261021T150000Z/candidate-partial-b40de60` (wk-r3c-2)
- Longform `/tmp/opencode/jgas-longform-r3c-20261021T152000Z/candidate-partial-b40de60` (lf-r3c-2)
Read roots + leaf safely (editorial-corrections dirs + State pointer r2, supersedes r1, same anchor).

Scripts saved BEFORE execution in this packet (`verify_weekly_lifecycle.py`, `verify_longform_lifecycle.py`, `verify_save_negative.py`, py_compile 0).
ENV `PYTHONDONTWRITEBYTECODE=1` + `PYTHONPYCACHEPREFIX=/tmp/opencode/lifecycle-r3c-pycache` set in bash BEFORE python (no SRC pycache growth).
NEW FULL independent byte copies via `cp -a` (no hardlinks, inodes differ, no alternates, inert `example.invalid` origin), 718 hash vs frozen `source-manifest-r3c.json` 0 mismatches, originals readonly (HEAD unchanged).
No edits source/old authorities, no clean/reset/purge/raw delete/network/commits. Synthetic Human identity explicit type-only, no production semantic PASS, placeholder quality NO-GO maintained.

## Weekly + Longform lifecycle (actual generic APIs, no rebuild of first/second flows)
- `stage_validation.validate_stage` with actual `REQUIRED_CURRENT` keys (`VALIDATED_DRAFT:{publication-candidate}`, `RELEASE_CANDIDATE:{visual-review-record,freeze-record,release-manifest}` — corrected, not guess).
- `agent.build_stage_checkpoint` + `advance_with_checkpoint` VALIDATED_DRAFT→RELEASE_CANDIDATE (HUMAN_GATE_REACHED), RELEASE_CANDIDATE→FROZEN.
- `agent.approve_publication_preview` synthetic (`synthetic-weekly/longform-human-fixture`, `synthetic:...-preview-...`) with actual records.
- `profiled.build_profiled_freeze` (canonical stable `freeze-record`/`release-manifest`), active visual from candidate (`visual-review-record` follows active visual vs canonical template — config `stage_plan` has only freeze pair, alias constraint identified, used active path, no patch).
- `publication.build_merge_verification` + `build_release_record` + `release_checkpoint.build_release_checkpoint` + `advance` FROZEN→RELEASED offline.
- Strict State + active receipt/Gate/Candidate + history after FROZEN/RELEASED asserted. Old version1 (`wk/lf-r3c-1`) + old canonical/source/QA unchanged (allowlist: State + expected approval/checkpoint/freeze pair/release outputs). Public Candidate exact versioned-2 from set/State.

Exits: `weekly-exit.txt:0` (52.164s), `longform-exit.txt:0` (53.097s), `save-negative-exit.txt:0`.

## Resolvers + export (actual behaviors, no AST proof)
- Orchestrator `_configured_gate_inputs` + `_configured_expected_artifacts`, handoff `resolve_handoff_artifact_path` + `expected_output_contract`, humangate `resolve_gate_path` + `_reviewed_artifacts` — all return active versioned-2 on positive copies (loaders as well as producers tested).
- Export: extracted existing current workflow Python selection code offline (`_norm`, `_all_states`, `_selection_for_state`, `_issue_of_candidate` via `textwrap.dedent`, chdir to root for relative globs, no Actions/GitHub). Manual active matches 1 state, old-canonical differs (would refuse stale), inert set exists (lone set without candidate must refuse), ambiguity len==1.
- **Export BLOCKER (both routes, preserved, continue lifecycle):** `SystemExit: unsafe path (must be strict repo-relative): '/tmp/.../candidate-partial-b40de60/sources/.../publication-candidate-v2.json'` at `verify_*_lifecycle.py:348` (`_norm(exp.as_posix())` where `exp` is absolute `candidate_path` from `resolve_publication_selection`). Workflow passes absolute Path to strict `_norm` which rejects absolute. Exact source blocker, no patch/fake. Lifecycle continued (Freeze/Release independent).

## Final artifacts (independent inspector)
- `final-weekly-second-correction.pdf` 63397B sha `0f045d...`, `final-longform-second-correction.pdf` 79757B sha `c37368...`, both 5pp real TL2026.
- `final-*-second-correction.txt` via `pdftotext`, `final-*-second-correction-p1.png` via `pdftoppm -png -r 150 -f 1 -l 1` (page 1).
- `artifact-hashes-weekly/longform.json` (15 entries: pdf/candidate/set/receipt/gate/manuscript/State/r2/freeze/manifest/merge/release + 3 checkpoints), `rolemap-weekly/longform.json` (mode/candidate/set/anchor/effective7/roles).
- `source-manifest-r3c-frozen.json` (718 frozen pins).

## Negative (NEW negative copies, no authority rebind, no State rewind)
- `jgas-weekly-lifecycle-neg-...` + `jgas-longform-lifecycle-neg-...` via `cp -a` (no sharing/alternates).
- Temp VALIDATED_DRAFT state (history truncated -3, pending gates/checkpoints, no provenance for pending, `next_action:stage:publication-candidate`, `terminal_reason:None`, fixture-only in execution dir).
- Wrong old Candidate (`wk/lf-r3c-1`) Stage correctly refused: `StageValidationError: Publication Candidate does not bind exact reader_manuscript` (immediate fault + inventories + exact error). Healthy active (`wk/lf-r3c-2`) passed.
- No duplication of other Worker fault matrix.

## Additional blocker (longform post-RELEASED receipt, preserved)
- `longform RECEIPT BLOCKER: EditorialError ROUTE_REDERIVE ... Evidence package basis drift: state_sha256` (`survey_evidence_v2.py:741` via `survey_longform_derivation_v2.py:1066` → `survey_editorial_publication_v2.py:876`). Weekly receipt passes post-RELEASED; longform re-derives with current State whose `production-state.json` sha differs from evidence package basis. Gate/Candidate still `PASSED/READY` post-RELEASED. Exact source blocker, no patch. Lifecycle itself (stage/Preview/Freeze/Release) already `errs=[]` healthy.

## Raw
- `weekly-stdout/stderr/exit.txt`, `longform-stdout/stderr/exit.txt`, `save-negative-stdout/stderr/exit.txt` (numeric exits, elapsed per step, source pins). Old attempts preserved (`*-attempt*.txt`, `*-attempt*-quota.txt`, fixture-only harness fixes with new attempt names, no authority rebind).
- Disk quota `EDQUOT` during copies preserved in attempt raws; freed own old `wk2-verify/longform-090000` + `editorial-build-*` temps (no source/other-worker deletion) to continue.

No Human Commit Point until root closes whole unit.
