# B evidence preservation — raw byte copies + source binding (scope only)

Date: 2026-10-28 UTC. Documentation/evidence preservation ONLY. No source
edits, no runtime/tests, no cleanup. Candidate/private existing copies untouched.
55 child Gitlinks untouched (not inspected, not modified). C2 current editing
does not affect this B archive (all B-owned files match; diffs are C-owned only).

Reports read: `author-B-lifecycle-correction.md`,
`author-B-preserved-provenance-correction.md`.

## 1. Private-path reuse (potential overwrite — observed)

Both B reports cite the SAME private copy
`/tmp/dm022-b-lifecycle-private-20261028T180000Z`. Current private reflects the
LATER (preserved-provenance, 23-test) state: B test file is `b56ad21e…`, not the
lifecycle-run `c634fa32…` (19-test). The original 19-test private source state is
no longer separately available. Raw outputs are DISTINCT paths and all survive
(§2). Nothing is recreated; no full-lossless claim is made for the earlier
private state.

## 2. Raw files preserved byte-for-byte (NEW unique evidence)

Dir: `notes/rephase-1-dm022-prearchitecture-implementation/evidence/B-preserved-20261028T222802Z/`
(no overwrite — new unique dir; no Git DB in packet).

| raw | src | SHA256 | bytes/lines | scope | dst copy equal |
|---|---|---|---|---|---|
| lifecycle 19-test | `/tmp/dm022-b-lifecycle-raw-20261028T180000Z.txt` | `bd17c5dd53a9e98d3b5c8c35bb7bb092dbd6bcbb269753831d2d55e264e6ee3f` | 5502B / 51 | Ran 19 tests OK, exit 0 | True |
| preserved R1 23-test | `/tmp/dm022-b-preserved-r1-raw-20261028T183000Z.txt` | `7b939bdeed2da258a9278231dcbae827a76ec7999c42cf146b83eebee6397cc4` | 6814B / 63 | Ran 23 tests OK, exit 0 | True |
| legacy 9-test | `/tmp/dm022-b-legacy-raw-20261028T180000Z.txt` | `cb861b44ef9a3d895059bdb68cf4bb0b0e20ac4fd7d385658bc0e1005b12a5a6` | 2037B / 15 | 5+2+2 OK (agent_control 5, active_evidence_views 2, selection_architecture 2), exit 0 | True |

SHAs match the report claims (`bd17c5dd…`, `7b939bde…`, `cb861b44…`). `cp` exits
0/0/0. No raw missing; no raw overwritten (distinct paths, all present).

## 3. Private vs candidate B files (exact only)

Private `/tmp/dm022-b-lifecycle-private-20261028T180000Z` (758 intended files
excl `.git`; own `.git` HEAD `409b292…`, 83 files; 0 `*.pyc`) vs candidate-work.
All 13 B-owned files MATCH exactly (SHA+bytes):

- `scripts/survey_agent_control_v2.py` `b6506a8b…`/195749
- `scripts/run_selection_architecture_v2_interactive.py` `553bf22b…`/27766
- `scripts/run_evidence_v2_interactive.py` `d65de849…`/37573
- `scripts/run_drafting_synthesis_v2_interactive.py` `ad6cdea7…`/15263
- `scripts/survey_drafting_v2.py` `4f332258…`/26740
- `scripts/survey_drafting_v2_base.py` `2fad4828…`/63592
- `scripts/survey_handlers_v2.py` `946e2671…`/29764
- `scripts/survey_stage_validation_v2.py` `ec15f5ba…`/49688
- `scripts/survey_orchestrator_v2.py` `9d0cc3b3…`/59768
- `scripts/survey_core_execution_bridge_v2.py` `f7bffbee…`/25060
- `scripts/survey_human_gate_v2.py` `19f3e1e3…`/70392
- `scripts/survey_architecture_v2_base.py` `ac52c842…`/47416
- `tests/test_dm022_prearch_b_ordinary_consumers_v2.py` `b56ad21e…`/47571

Current latest B source matches, but this CANNOT retro-certify the earlier runs:
the `bd17` 19-test run executed against the earlier private state (`c634fa32…`
test file), which is superseded. Post-hoc hashes are observation, NOT per-run
proof. No lost raw is recreated.

## 4. Which runtimes differ (non-B only)

PRIV 758 vs CAND 759 (candidate +1 file). 15 diff paths, ALL C-owned (C1 renewal/
history/derivation/staged-source, C2 release, C-owned test helpers); ZERO B
files differ:

- Modified (14): `survey_editorial_staged_source_v2.py`,
  `survey_release_checkpoint_v2.py`, `survey_versioned_renewal_history_v2.py`,
  `survey_versioned_renewal_source_v2.py`,
  `test_dm022_c1_research_graph_v2.py`, `test_dm022_full_lifecycle_v2.py`,
  `test_survey_editorial_correction_proposal_v2.py`,
  `test_survey_editorial_current_authority_v2.py`,
  `test_survey_editorial_retention_v2.py`,
  `test_survey_editorial_staged_source_v2.py`,
  `test_survey_increment_b_weekly_derivation_v2.py`,
  `test_survey_longform_derivation_v2.py`,
  `test_survey_longform_publication_integration_v2.py`,
  `test_versioned_renewal_source_phase_s.py`
- Added (1, candidate-only): `tests/test_dm022_c1_h_presence_controls_v2.py`

## 5. Owned B new helper fns artifactmap (source preserved for review)

No Git DB in packet; file SHAs in §3 table. Helper entry points (candidate-work):

- `_dm022_pinned_family(repo_root, state) -> str` ×5:
  `run_selection_architecture_v2_interactive.py:50`,
  `run_drafting_synthesis_v2_interactive.py:48`,
  `survey_handlers_v2.py:40`, `survey_stage_validation_v2.py:194`,
  `survey_agent_control_v2.py:110`
- `derive_draft_package_from_accepted_state(repo_root, state_path, …) `:
  `survey_drafting_v2_base.py:540` (+ forwarder `survey_drafting_v2.py:370`)
- `_resolve_prearchitecture_artifact` `survey_agent_control_v2.py:1073`;
  `resolve_active_research_four_refs` `survey_agent_control_v2.py:1389`
- Artifact map (review shape): `{family, checkpoint, artifacts(parsed),
  lineage, artifact_refs(4 NamedRefs), evidence/views/ledger/completeness+paths}`;
  callers consume `artifact_refs` paths, never stale canonical fallback.

## 6. Copy log (transcribed tool-observed, NOT raw)

```
mkdir -p evidence/B-preserved-20261028T222802Z -> exit 0
cp /tmp/dm022-b-lifecycle-raw-20261028T180000Z.txt <ev>/... -> exit 0
cp /tmp/dm022-b-preserved-r1-raw-20261028T183000Z.txt <ev>/... -> exit 0
cp /tmp/dm022-b-legacy-raw-20261028T180000Z.txt <ev>/... -> exit 0
python sha256 src vs dst ×3 -> equal True/True/True (SHAs/sizes above)
```

These command lines are TRANSCRIBED, not raw. Only the three author-saved txt
files are raw. Process identity: no `GIT_*` overrides observed; no Human commit
readback (no git commands in workspace reconstruct root). Stop — scope only.
