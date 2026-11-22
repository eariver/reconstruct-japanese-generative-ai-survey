# TEST-ONLY supplement — late guard + direct PREARCH collision (no code change)

Root: `../../astra-repair-resolution.md` FULL §§1–2. Independent `GO_SCOPED_AFTER_TEST_SUPPLEMENT` (`../independent-implementation-review.md` + machine): code `1e4c…`/51927B frozen, 47-line diff accepted, 8/8 PASS transcribed, 2 TEST-only oracles pending. This supplement adds ONLY those 2 tests in SAME `tests/test_prior_artifact_reader_repair_v2.py`; production `scripts/survey_stage_validation_v2.py` unchanged frozen `1e4c818b…`/51927B.

Author copy: `.rephase-1-editorial-runtime/prior-artifact-reader-implementation-20261122T062101Z/candidate-work` (HEAD `d591`, no commit, no config/HOME/network/source-old writes/subagents). Original test `22782B 926af0…` + 8-run raw preserved in `../raw/`; not rewritten. New exclusive raw here `supplement-20261122T064124Z/raw/` (combined + per-test). Source 774 baseline +1M+new test =775.

## Final test identity + old-8 preservation

- Final: `30019B 1fb831673b8291813ab0480720f84467e334374619a87fe072ff00c63438d4db` `0o664` (`0o100664` full), 520 lines (was 408).
- Reconstruction proof: strip doc-qualifier (`no fake validators…` → `no mocks`) + remove `TestPriorArtifactLateGuardPrepublish` + `TestPriorArtifactDirectCollisionPrearchMerge` → `22782B 926af092…` exact (`raw/test-diff.patch` 131 lines, doc-only + 2 classes). `raw/ast-old8.txt` lists old 8 methods (Weekly/Thematic full, LEGACY, wrong-family/unknown/SELF-split/drift-missing-collision/guard-entry) present with stable bodies; `raw/final-test-hash.txt` gives final SHA. No old body edited.

## 1) Late (post-semantics/prepublish) guard — `TestPriorArtifactLateGuardPrepublish.test_prearch_late_guard_refuses_prepublish_no_report`

Genuine tiny HIGH adopt +7 outputs (`_adopted_prearch_with_outputs` WEEKLY `late`, own epoch, inert origin, no 480 reuse/repin). `unittest.mock.patch.object(stage_validation,_validate_stage_semantics,side_effect=_inject_then_return)` where `_inject` calls ORIGINAL then creates owned guard (`low.guard_path_for`) right before return — never replacing with PASS. Doc `no mocks` qualified to `no fake validators` (probe only).

- Before: guard absent, State/matrix/selection pinned.
- `validate_stage` EVIDENCE (matrix+selection) → refuses `DM022_TRANSITION_ACTIVE` (prepublish `_dm022_require_ready`), fresh report `EVIDENCE-late-bad.json` absent, State/matrix/selection bytes immediate unchanged except intentional guard (`guard.is_file()`).
- Restore own fault (`guard.unlink`), recovery `validate_stage` → `EVIDENCE-late-restore.json` PASS (separate recovery, not claimed as immediate proof of refusal).

Fixture class/boundary: synth DB (temp independent Git, meaningful contents, process identity), family PREARCH (LOW `resolve_research_authority`), lifecycle EVIDENCE_REVIEWED, same-record triplet, `implementation_commit_sha==HEAD`.

## 2) Direct `_prior_artifacts` PREARCH-merge collision — `TestPriorArtifactDirectCollisionPrearchMerge.test_direct_prior_collision_hits_prearch_merge_disagree`

Direct helper negative (fault State-argument copy only), not genuine accepted malformed State. Keeps PREARCH record/proof valid + role triplet; no real/shipping config modified.

- Base genuine adopted PREARCH (`collide`); `agent._validate_checkpoint_record(...,evidence,ev_ref,None,None)==[]` proves PREARCH valid.
- Reuse actual LEGACY screening checkpoint as genuine-prior-shaped base: copy record+report to disposable `disposable-screening-collision*.json` inside independent DB, add contradictory `evidence-acceptance` row (path = screening-acceptance file, sha its sha; different from PREARCH evidence path) to BOTH record and report, repoint review result to disposable report. `bad_state` copies State, repoints only `screening` provenance to disposable (new SHA); `evidence/materiality/completeness` still share PREARCH path (triplet kept).
- Prove LEGACY disposable validates (`_validate_checkpoint_record screening ==[]`) and PREARCH evidence validates (`==[]`), so failure is merge not early schema/provenance.
- `stage_validation._prior_artifacts(root,cfg,bad_state)` → `prior Stage Checkpoints disagree on artifact name: evidence-acceptance`. Screening LEGACY merges first (dict order discovery→screening→evidence), PREARCH merges second and hits `existing.resolve()!=artifact.resolve()`. Asserts PREARCH-branch new merge (disagree on PREARCH name, both sides valid, triplet kept). Old `_merge_artifacts` temp-file probe (in `test_artifact_drift_missing_collision`) remains different coverage.

## Runs (TEST-ONLY, no code change, no real W34/SP/CURRENT)

- Combined new-only: `2026-11-22T06:42:23Z–06:43:10Z` UTC (~47s wall), `exit 0`, `Ran 2 tests OK` (`raw/stderr.txt` 0 stdout). CWD new copy, `PYTHONDONTWRITEBYTECODE=1 GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0`, scrubbed `GIT_*`, PID 1501887.
- Per-test: late `real 41.06s` (`raw/per-late/`), collision `real 6.70s` (`raw/per-collision/`), each exit 0, same cwd/env. No old-8 repeat, no real-material stage.

Stop for review before commit/real. Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN.
