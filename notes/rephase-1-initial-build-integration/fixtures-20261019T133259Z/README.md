# Fixture generation ONLY — initial build integration — 20261019T133259Z

Scope: `astra-execution-selection.md` items 3–5 first half ONLY. No TeX builds,
no publisher pass2, no test-suite, no candidate/reconstruct commit, no Production
mutation. Both existing sources held READ ONLY. Toolchain setup NOT duplicated
(separate Worker owns `/tmp/opencode/jgas-texlive-*`).

Root remains reviewer; this packet claims NO independent PASS, NO genuine semantic
PASS, NO Human approval. Existing synthetic upstream Architecture approvals are
labelled test type authority. Source-generated review records beyond upstream wait
for independent reviewer.

Tool difference: `apply_patch` absent in this environment. Packet dir created with
`mkdir` (after parent `ls`), new files with `Write` (dedicated editor). No historical
runners executed. No source imports; `PYTHONDONTWRITEBYTECODE=1` everywhere.

## 1. Inputs

- Selection: `notes/rephase-1-initial-build-integration/astra-execution-selection.md`
- Decision §5: `outputs/rephase-1-integrated-admission-feasibility-decision.md` §5
- Prep: `notes/rephase-1-initial-build-integration/README.md` (R2 pre-step, toolchain-blocked locally)
- Available exact source (READ ONLY, unmodified, re-verified this run):
  `/tmp/opencode/jgas-initial-build-20261019T132209Z/candidate-partial-b40de60`
  HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`,
  `status --porcelain=v1 --untracked-files=all` 3M18A, static21 `1c0e339c…` 21/21
  (sha+bytes per-file, see `make_fixture_dbs-commands.log`).
- Reconstruct workspace HEAD untouched; no commit created here.

Required helper methods read before execution:
- Weekly `tests/test_survey_increment_b_weekly_derivation_v2.py` `_chain:77`,
  `_complete_authorities:122`, `_current_state:242`
- Longform `tests/test_survey_longform_publication_integration_v2.py` `_chain:205`,
  `_complete:249`, `_state_path:272` + underlying
  `tests/test_survey_longform_derivation_v2.py` `_chain:156`,
  `_complete_authorities:401`, `_current_state:585`, setUp narrow adapter 169–201
  (DID-free clean Discovery locators for lexical gate, replicated narrowly).

## 2. New harness / commands / evidence (durable, in this dir)

- `make_fixture_dbs.py` — creates both isolated DBs, copies complete worktree,
  commits source basis BEFORE authority. Run:
  `PYTHONDONTWRITEBYTECODE=1 python3 make_fixture_dbs.py`
  `> make_fixture_dbs-stdout.txt 2> make_fixture_dbs-stderr.txt`,
  exit `make_fixture_dbs-exit.txt` (`0`), raw log `make_fixture_dbs-commands.log`.
- `gen_weekly_surface.py` — Weekly authority + surface-only CLI (actual helpers,
  no `setUp`). v1 guard too narrow (`sources/` only, missed root chain
  intermediates) failed exit 10, preserved as `gen_weekly_surface-stdout/stderr/exit.txt`
  + `gen_weekly_surface-faulty-v1.py` (archived faulty bytes) + `weekly-*-attempt1.*`.
  Fixed guard allows `sources/2026-W37/` + root intermediates
  (`architecture-*.json`, `selection-v2.json`, `raw/`, `views-input/`, `views-accepted/`,
  `draft-package-/draft-result-`). Attempt2:
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<weekly-fixture> python3 gen_weekly_surface.py`
  `> gen_weekly_surface-attempt2-stdout.txt 2> gen_weekly_surface-attempt2-stderr.txt`,
  exit `gen_weekly_surface-attempt2-exit.txt` (`0`, `weekly surface OK`).
- `gen_special_surface.py` — Special authority + surface-only CLI with narrow
  clean-Discovery adapter (URL_BY_DID). Run with
  `PYTHONPATH=<special-fixture>`, `> gen_special_surface-stdout.txt`,
  exit `gen_special_surface-exit.txt` (`0`, `special surface OK`). No retry needed;
  guard pre-fixed to allow `sources/SP001/` + same root intermediates.

All `EVIDENCE` writes used unique before/after/copy names; no log overwritten.
Inner pins (`weekly-state.json`, `weekly-authored.json`, etc.) from failed v1
backed up as `*-attempt1.*` before attempt2 regeneration.

## 3. New independent fixture DBs (outside notes, no embedded .git)

Parent (pre-checked, created): `/tmp/opencode/jgas-initial-fixtures-20261019T133259Z/`

- Weekly: `/tmp/opencode/jgas-initial-fixtures-20261019T133259Z/weekly-fixture`
  source-commit `88813a01accb320b5948e368618e4061a4d72e0b`,
  tree `3e01284d3fd716e02a5dd6f15d972e33287229ec`, status clean at commit,
  inert origin `https://example.invalid/initial-build-fixture.git`,
  no `user.name/email` in local config, no alternates, `.git` 765 files,
  overlap src 0 / recon 0, worktree21 hardlink-shared 0.
  Message: `Synthetic isolated Weekly initial-build fixture source basis (synthetic snapshot, not 409 ancestry)`.
- Special: `/tmp/opencode/jgas-initial-fixtures-20261019T133259Z/special-fixture`
  source-commit `d4078d1bc851b9977289acf4b9cd6560c080b69e`,
  same tree `3e01284d3fd716e02a5dd6f15d972e33287229ec` (identical content),
  same isolation (765 files, 0/0 overlap, 0 hardlinks).
  Message: `Synthetic isolated Special initial-build fixture source basis (...)`.

Content: full worktree byte-copy (707 files) excluding `.git/__pycache__/.pytest_cache`,
including all21 overlay working-tree bytes (static21 content equality 21/21 in both),
plus `.latexmkrc`, `config/`, `schemas/`, `scripts/`, `templates/`, `prompts/`, `docs/`,
`data/`, `tests/`. Process-scoped synthetic identity only (`-c user.*` + env,
no persistent `user.*`, no `--allow-empty`, no hooks bypass). Synthetic snapshot
ancestry explicitly distinct from actual409; no original ancestry fabricated.
Exact commit commands/exits in `make_fixture_dbs-commands.log`;
per-fixture `fixture-<name>-head/tree/status/config/remote.txt`.

Full-entry separation (not pack-only): full `.git` `dev:ino` sets vs source (83 files)
vs reconstruct (2567 files), cross-domain collisions 0; worktree21 `dev:ino` equality 0.
Inherited `GIT_*` asserted absent before every run; per-invocation sanitized env
(`GIT_NO_LAZY_FETCH=1`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`,
`GIT_OPTIONAL_LOCKS=0`) + `git --no-optional-locks`.

## 4. Results — both actual accepted input surfaces ready (DRAFT_COMPLETE)

### Weekly (2026-W37, WEEKLY_MAGAZINE), fixture `weekly-fixture`

- Fixture source HEAD at authority: `88813a01…` (record `weekly-fixture-source-head.txt`).
- Helpers: `_chain` → `_complete_authorities` → `_current_state` via actual
  producer/validator paths; `sys.path` fixture-first, `core.__file__` asserted inside
  fixture; `cwd` = fixture so internal `Path(".")` resolves to fixture, not source.
- State: `sources/2026-W37/production-state.json`,
  sha256 `de45bc659cbddc603c4dfb58f05a47123adb7ebf3c0c19f5fb4e11d16b5aceb1`,
  5392B, `lifecycle_state DRAFT_COMPLETE`, `next_action stage:reader-publication-validation`
  (record `weekly-state.json`).
- Authored: `sources/2026-W37/semantic-publication-input.json` (record `weekly-authored.json`).
- CLI (actual subprocess):
  `python3 scripts/survey_weekly_semantic_publication_v2.py --repo-root <fixture> --state <actual State> --input <authored> --materialize-surface-only`
  (record `weekly-surface-command.txt`), exit `0`
  (`weekly-surface-exit.txt`), stdout `SURFACE_MATERIALIZED`
  (`weekly-surface-stdout.txt`, stderr empty).
- Surface: `sources/2026-W37/publication/v2/reader-surface-input-v2.json`,
  sha256 `136c0dd8a2bf4c5b4323993ff3882524c760d902f2a463b93bcd6fe95a948635`,
  2648B, `issue_id 2026-W37` (record `weekly-surface-pin.json`).
- Guards: HEAD unchanged across authority+CLI (`weekly-before-head.txt` =
  `weekly-final-head.txt` = `88813a01…`); `diff HEAD` clean of control files;
  delta = research outputs only (`sources/2026-W37/` + 9 root chain intermediates,
  record `weekly-authority-delta.json`); no `main.tex`/`references.bib`/`jgaisurvey.sty`,
  no `validated-source-manifest.json` (surface-only stop verified).

### Special (SP001, LONGFORM_SPECIAL), fixture `special-fixture`

- Fixture source HEAD: `d4078d1b…` (record `special-fixture-source-head.txt`).
- Helpers: `LongformDerivationV2Tests` object with `root/cfg/head/workspace=fixture`,
  narrow `_bound_authored` (primary_url `https://example.invalid/papers/lineage-note-one`)
  + `_clean_evidence_helper` (Discovery `source = helper.source(URL_BY_DID[did])`),
  then actual `_chain(dids=(DID1,))` → `_complete_authorities` → `_current_state`.
  Same fixture-only import/cwd enforcement as Weekly.
- State: `sources/SP001/production-state.json`,
  sha256 `907bffd0eda7d5a9980c4aa2755ca46e36bd7fb5c02753a844a8a2f9b19e70d7`,
  5359B, `DRAFT_COMPLETE` / `stage:reader-publication-validation`
  (record `special-state.json`).
- Authored: `sources/SP001/semantic-publication-input.json` (record `special-authored.json`).
- CLI: `python3 scripts/survey_longform_semantic_publication_v2.py --repo-root <fixture> --state <actual State> --input <authored> --materialize-surface-only`
  exit `0`, stdout `SURFACE_MATERIALIZED` (records `special-surface-*`).
- Surface: `sources/SP001/publication/v2/reader-surface-input-v2.json`,
  sha256 `f40db7f6f88f099e13162f51296d0b24874922d80a7ef31fd85329b85a957cd5`,
  7071B, `issue_id SP001` (record `special-surface-pin.json`).
- Guards: HEAD unchanged (`d4078d1b…`); delta = `sources/SP001/` + root intermediates
  (`architecture-*`, `selection-v2.json`, `draft-package/result-pkg-001.json`,
  `raw/`, `views-input/accepted/`, record `special-authority-delta.json`); no TeX
  outputs, no receipt (surface-only stop verified).

No `__pycache__` in either fixture (`find -name __pycache__` empty).
Original source still `409b292…` 3M18A (read-only held, §4 probe).
No runtime blocker: both routes exit 0. No candidate modification made or proposed;
fixture-only harness fix (v1 narrow guard) used unique attempts + archived faulty bytes.

## 5. Schema / check families (this phase only)

- State/lifecycle: `config/survey-production-v2.json` contract + actual
  `survey_agent_control_v2` / `survey_stage_validation_v2` stage validators
  (deterministic `CORE_STAGE_CONTRACT` PASS recorded in `orchestration/v2/reviews/`,
  checkpoint `advance_with_checkpoint`).
- Surface derivation: actual `survey_weekly_derivation_v2.load_derivation` /
  `survey_longform_derivation_v2.load_derivation` + structured
  `scan_structured_reader_surface` (Weekly) / Longform pass1 loader; surface bytes
  pinned, no TeX/Bib/style materialized.
- NOT done: pass2 TeX/Bib/style/receipt, manuscript/Gate, QA bundle, Candidate/State
  readback, semantic/visual review records beyond upstream synthetic Architecture
  fixture, PDF/log/digest. Those wait for independent reviewer + toolchain builds.

## 6. Paths for reviewer (author-independent pre-TeX inspection entry)

- Weekly surface: `/tmp/opencode/jgas-initial-fixtures-20261019T133259Z/weekly-fixture/sources/2026-W37/publication/v2/reader-surface-input-v2.json`
- Weekly authored: `…/weekly-fixture/sources/2026-W37/semantic-publication-input.json`
- Weekly State: `…/weekly-fixture/sources/2026-W37/production-state.json`
- Special surface: `/tmp/opencode/jgas-initial-fixtures-20261019T133259Z/special-fixture/sources/SP001/publication/v2/reader-surface-input-v2.json`
- Special authored: `…/special-fixture/sources/SP001/semantic-publication-input.json`
- Special State: `…/special-fixture/sources/SP001/production-state.json`
- Fixture code/control context: each fixture root (complete source+21 overlay,
  `.latexmkrc`, configs/schemas/scripts/templates/prompts/docs/data/tests).
- Evidence: `notes/rephase-1-initial-build-integration/fixtures-20261019T133259Z/`
  (harness + commands/exits + pins + raw CLI outputs + deltas).

## 7. STOP

Fixture generation phase COMPLETE. Surfaces ready for author-independent pre-TeX
inspection. Do NOT generate genuine semantic PASS or Human approval. Do NOT start
TeX builds / publisher pass2 / Gate / QA / Candidate / State integration until
root selects execution after inspection. Ordinary commit/push remains Human-owned.
