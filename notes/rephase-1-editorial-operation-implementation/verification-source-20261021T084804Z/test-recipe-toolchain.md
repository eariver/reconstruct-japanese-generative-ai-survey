# Ready test recipes (read-only scripts) + actual toolchain path (for parallel workers)

No DST edits. All paths read-only, no execution here (smoke R2V already proved terminal 0).

## Test recipes (adapted, not old runners; do NOT run saved R2/historical runner scripts)

- `tests/test_survey_editorial_correction_proposal_v2.py:_new_weekly_helper`, `_build_weekly_validated` (fast base, blank initial PDF only label type), `_stage_authoring_before_prepare`, `_stage_reader_and_proposal`, `_scope_review_for` (external synthetic scope via actual helper)
- `tests/test_survey_editorial_correction_proposal_v2.py:_new_longform_helper` (for Longform follow-up, not run here)
- Actual P1 `prepare_proposal`/`validate_proposal`, P2R `capture_retention`/`verify_retention`, P2V `observe_current_authority`, P3S `materialize_staged_source`/`verify_staged_source`, high `prepare_publication`/`finalize_publication`/`activate_publication`/`resume_activation`/`validate_*`, Reader/Gate/quality/candidate builders (all actual public functions/CLI, no mocked validators/Git authority success; tests adapt accepted helpers, never `run oldSetUpIncompleteOverlay`)
- Smoke harness `integration-20261021T120000Z/smoke-weekly-activation.py` (saved BEFORE execute, adapted recipes, saves full raw/numeric exit/persistent unique attempt files + source binding; timed long process has terminal result before next launch; no source `.pyc` via `PYTHONDONTWRITEBYTECODE=1` + external cache)

## Actual toolchain path (external, not in SOURCE; recorded, not approval)

- `absolute_executable`: `/tmp/opencode/jgas-texlive-20261019T133205Z/texlive/bin/x86_64-linux/lualatex` (symlink → `luahbtex` real, pinned link+real+hash/version in build record; `argv0` lualatex formatting preserved via link path; stable recheck; controlled `PATH=toolbin:/usr/bin:/bin`, no ambient `TEXMF*`/`TZ`/`LANG` merge)
- Fixed recipes: `lualatex-biber-lualatex` (`EXPECTED_ARGV_LUALATEX_BIBER`) and `latexmk-lualatex` (`EXPECTED_ARGV_LATEXMK`); recipe `.latexmkrc` (`$pdf_mode=4;`, `$lualatex`, `$biber`, `$max_repeat`) pinned pre/post, blocking log patterns enforced, real exit/log/versions/digests, exclusive `build3` transfer, no network install.

## Parallel worker use

- Clone stable snapshot root `/tmp/opencode/jgas-editorial-r2v-20261021T084804Z/candidate-partial-b40de60` (`SOURCE_HEAD 4ff2d8562502db36223332c45c9cc5d01bb93156`, tree `4a0c5343937151af0c0ad4522177441acd0e8fcc`, 717 files) to independent DBs (new `git init`, no alternates/hardlinks, inert `example.invalid` origin); keep source immutable during parallel tests (no writes to `scripts/`/`schemas/`/`config/` in fixture; R1 per-fixture test-allowed source comment commit isolated only with explicit `user.name/email`, no shared DB).
- Reuse successful REAL builds only if exact sources/tools/build basis unchanged and code pins constant (same `SOURCE_HEAD`, same `toolchain --version`, same `recipe_ref` sha, same `staged trio` sha); otherwise regenerate (new fixture epoch, no pin rebinding).
