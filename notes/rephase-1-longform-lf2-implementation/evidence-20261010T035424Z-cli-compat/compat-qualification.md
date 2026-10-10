# Gate CLI compat — qualification (closeout-only, no candidate edits)

2026-10-10. Justified missing-route regression, not coverage decoration.
Selected LF-2 contract requires affected Weekly generated + direct-primary
compatibility. Prior 43-method result ran 27 `test_survey_reader_surface_gate_v2`
methods (leakage/direct-primary) but no real generated-Weekly receipt/CLI
admission. This dir runs only the 2 affected CLI positives at exact final 9
hashes. No 43-suite rerun, no old whole runner, no candidate code/test edits.

## Source identity (exact final 9, correction3 hash-manifest)

- Design `/tmp/opencode/jgas-lf2-design-20261009T113013Z`, HEAD
  `409b292756dd1277b9dfae87679934c0d2ce251c`, tree
  `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, parent
  `34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4`.
- All 9 SHA256/mode 664 match
  `evidence-20261010T120000Z-correction3/hash-manifest.json` pre AND finally
  post (manifest `identity_pre`/`identity_post` overlay verified, status
  exactly 2M+7A plus `__pycache__` side effects, HEAD/tree/parent unchanged).
- No fresh source patch (code unchanged); old proof scripts and empty-commit
  deviation left untouched; no candidate/reconstruct commits, branches, refs,
  network, Production, or subagents. All fixture DBs/temp work independent
  under `/tmp/opencode` (`TMPDIR=/tmp/opencode` for runner and child).

## Fixture setup inspection (before execution)

Target module `tests/test_survey_gate_cli_persisted_review_v2.py` (689 lines):

- Own docstring (lines 11-15): process-local Git author/committer env identity
  instead of `git config`; only sandbox/profile/fixture constructors patched;
  no authority validator or Git-success check stubbed.
- Own git invocations (lines 224-250): `git ls-files`, `git init -q`,
  `git remote add origin https://example.invalid/...`, `git add -A`,
  `git commit -q -m ...` with `env={**os.environ, **identity}` where identity
  is `GIT_AUTHOR_NAME/EMAIL` + `GIT_COMMITTER_NAME/EMAIL`. No
  `git config user.*`, no `--allow-empty` in this file.
- Inherited `IncrementBWeeklyDerivationV2Tests.setUp` (lines 41-71 in
  `tests/test_survey_increment_b_weekly_derivation_v2.py`) DOES contain
  persistent `["git", "config", "user.name", ...]` /
  `["git", "config", "user.email", ...]`. It is NOT invoked by the two target
  methods. They call `_make_env_identity_weekly_fixture` (lines 213-256),
  which constructs `base` without `base.setUp()`, replicates tracked-file copy
  + `git init/add/commit` with process-scoped identity env, and rejects
  inherited `GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE/GIT_OBJECT_DIRECTORY/
  GIT_ALTERNATE_OBJECT_DIRECTORIES/GIT_COMMON_DIR` via explicit raise.
- Direct path `_direct_fixture` (lines 124-139) calls
  `gate_fixture.SurveyReaderSurfaceGateV2Tests.setUp`, which only copies
  `schemas`/`config` to a temp dir (no git config, no allow-empty).
- Result: no runner-level setup adapter needed beyond the module's own
  narrowly labelled `_make_env_identity_weekly_fixture`. Test bodies/oracles
  unchanged, real git/validators, no success mocks. No blocker; proceeded.

## Original body vs fixture adaptation (precise)

- Original bodies (unchanged, candidate bytes as run):
  - `test_direct_primary_cli_admission_absolute_relative_and_cwd` (line 335):
    absolute + relative-cwd-root + relative-cwd-differs CLI admission via
    `_direct_fixture` + `_run_cli`, PASSED Gate + `validate_reader_surface_gate`
    route `DIRECT_PRIMARY`, plus input snapshot no-write check.
  - `test_generated_weekly_cli_admission_and_readback` (line 637): real
    `_build_generated_weekly` (accepted-chain → surface → persisted review →
    receipt → manuscript), CLI `scan-manuscript` with `--state`, tree-snapshot
    single-new-file oracle, `validate_reader_surface_gate` route
    `weekly.ROUTE`, receipt `reviewed_reader_input`/`semantic_review` binding +
    `weekly.validate_receipt`.
- Fixture adaptation: none in runner; module's own
  `_make_env_identity_weekly_fixture` is the process-scoped-identity adapter
  for the weekly path. Runner executes `python -m unittest -v <2 IDs>` directly
  against candidate, with forced `GIT_NO_LAZY_FETCH=1/GIT_OPTIONAL_LOCKS=0/
  GIT_ALLOW_PROTOCOL=file` for both parent git and child, `PYTHONDONTWRITEBYTECODE=1`,
  `GIT_TERMINAL_PROMPT=0`, `TMPDIR=/tmp/opencode`, routing overrides rejected
  via explicit raises (no `assert`), bytecode-optimized mode rejected.

## Distinct methods and exact binding

- Distinct methods: 2.
- Exact binding: `tests/test_survey_gate_cli_persisted_review_v2.py`,
  class `GateCliPersistedReviewV2Tests`,
  `test_generated_weekly_cli_admission_and_readback` + 
  `test_direct_primary_cli_admission_absolute_relative_and_cwd`.
- Runner `run_gate_cli_compat.py` records both IDs in `tests`/`child_argv`,
  `distinct_methods: 2`.

## Result

- Child `exit 0`, `timeout false`, `Ran 2 tests in 99.827s / OK` (stderr).
  Stdout holds only real publisher surface/receipt prints (766 bytes).
- Pre PASS, finally-post PASS (HEAD/tree/parent/9 hashes/modes/status).
- New small runner uses explicit raises, exclusive
  `manifest.json`/`run.stdout.log`/`run.stderr.log`/`run.log`, records child
  argv/runtime (`CPython 3.14.4`)/returncode, captures timeout partial (not
  triggered). Old whole runner NOT invoked.

Whole candidate remains NOT_READY; step4/B3 OPEN; canonical audit unstarted.
STOP here; no commits.
