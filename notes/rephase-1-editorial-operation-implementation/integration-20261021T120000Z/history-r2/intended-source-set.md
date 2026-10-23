# Intended SOURCE set for future fixture snapshots (explicit, no whole-tree copy)

## Intended = explicit tracked materialized + selected overlay/new, excluding residue/caches/evidence

- Tracked materialized (23 modified vs 409b292, all intended selected paths):
  `.github/workflows/build-special-pdf.yml`, `build-weekly-survey.yml`, `survey-production-v2-export-publication-preview.yml`,
  `config/survey-production-v2.json`,
  `schemas/publication-surface-revalidation.schema.json`, `reader-manuscript-v2.schema.json`, `reader-surface-gate-v2.schema.json`, `reader-surface-semantic-review-v2.schema.json`,
  `scripts/run_semantic_publication_v2_interactive.py`, `run_semantic_publication_v2_interactive_base.py`, `survey_agent_control_v2.py`, `survey_handoff_v2.py`, `survey_human_gate_v2.py`, `survey_orchestrator_v2.py`, `survey_production_v2.py`, `survey_profiled_freeze_v2.py`, `survey_reader_publication_v2.py`, `survey_reader_surface_gate_v2.py`, `survey_semantic_quality_v2.py`, `survey_stage_validation_v2.py`, `survey_weekly_derivation_v2.py`, `survey_weekly_mechanical_refresh_v2.py`,
  `templates/survey/jgaisurvey.sty`
- Selected overlay/new (27, all intended):
  schemas (10): `editorial-correction-proposal-v2`, `editorial-manuscript-spec-v2`, `editorial-publication-build-record-v2`, `editorial-publication-set-v2`, `editorial-publication-source-manifest-v2`, `editorial-retention-manifest-v2`, `editorial-staged-source-manifest-v2`, `editorial-toolchain-spec-v2`, `longform-publication-source-manifest-v2`, `longform-reader-input-v2` (all `.schema.json`);
  scripts (9): `survey_editorial_correction_proposal_v2.py`, `survey_editorial_current_authority_v2.py`, `survey_editorial_publication_v2.py`, `survey_editorial_retention_v2.py`, `survey_editorial_staged_source_v2.py`, `survey_longform_derivation_v2.py`, `survey_longform_generated_v2.py`, `survey_longform_semantic_publication_v2.py`, `survey_publication_set_v2.py`;
  tests (8): `test_group_c_editorial_consumers_v2.py`, `test_survey_editorial_correction_proposal_v2.py`, `test_survey_editorial_current_authority_v2.py`, `test_survey_editorial_retention_v2.py`, `test_survey_editorial_staged_source_v2.py`, `test_survey_longform_derivation_v2.py`, `test_survey_longform_publication_integration_v2.py`, `test_survey_publication_set_v2.py`
  plus new `tests/test_survey_schema_cache_v2.py` (Fix2, 1 file) → intended new total 28 after R2.
- Excluded (preserved, never deleted, never committed as SOURCE):
  `scripts/__pycache__/` (22 `.pyc`), `tests/__pycache__/` (1 `.pyc`), `tmpvr07sdme/` (43 files, tooling residue), `tmp*/`, `*.pyc`, smoke authority outputs (`sources/`, `surveys/`, `architecture-*`, `raw/`, `selection-v2.json`, `views-*` in fixtures), diagnostic `DIAG` copies, packet `smoke/` raw (evidence, not SOURCE).

## Future snapshot procedure (explicit file list, no `cp -a` whole dir + `add -A`)

1. `git -C DST rev-parse HEAD` (must be 409b292, detached, no new HEAD) + `git status --short` (record 23 M + intended new ?? only; residue `__pycache__`/`tmpvr07sdme` present but explicitly excluded).
2. Create empty dir `FIX_NEW/.../candidate-partial-b40de60`, `git init -q`, `config user.name/email`, `commit.gpgsign false`.
3. Copy ONLY intended set: for each of the 23 tracked modified paths, copy `DST/<path>` → `FIX_NEW/<path>` (parent `mkdir -p`); for each of the 28 new files, copy `DST/<path>` → `FIX_NEW/<path>`. Do NOT copy `__pycache__/`, `*.pyc`, `tmpvr07sdme/`, `tmp*/`, `.git/`, packet `smoke/`/`diagnostic-*/`, fixture authority `sources/`/`surveys/`.
4. Verify: `diff -r` per-file `sha256sum FIX_NEW/<path>` equals `sha256sum DST/<path>` at copy time (record full SHA manifest, not truncated hash); `git -C FIX_NEW ls-files --others --exclude-standard` must show 0 (no residue); `ls FIX_NEW/.git/objects/info/alternates` must be absent; `git remote -v` empty; `stat` inodes differ from DST (no hardlinks).
5. `git add` ONLY the 51 intended paths (23+28, explicit list, not `-A`), `commit -qm "SOURCE snapshot: ..." --no-verify` (meaningful independent fixture SOURCE commit before authorities). Record `rev-parse HEAD` (full 40-char, not truncated).
6. Ordinary candidate commit remains forbidden (no reconstruct commit/push). If new source bug fix after failed attempt requires new snapshot, preserve old fixture epoch (no deletion, no rebase), create new epoch dir, regenerate all authorities (no pin rebinding from old epoch).

## Old fixtures disclosure (cannot retroactively clean)

- FIX23 (and attempts 1-22) used `cp -a DST FIX; rm -rf FIX/.git FIX/scripts/__pycache__ FIX/tests/__pycache__; git add -A` → included `tmpvr07sdme/` (43 files) in SOURCE commit (759 vs 716). `__pycache__` correctly excluded (0 tracked). Preserved as-is; future epochs use explicit list above.
