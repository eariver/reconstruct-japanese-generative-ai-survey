# DM022 BC integration diagnostics — B-lifecycle + A-path + C2 fixtures (NEW composite, no source edits)

Date: 2026-10-28 UTC. All runtime authors idle (B-lifecycle correction + A path-normalization + C2 bound-State fixtures landed). No source edits by executor; no Human readback; no ordinary commits; no network/cleanup. Author reports are NOT authority — ONLY frozen-exec actuals below count.

## 1. Fixed source (ONLY tested)

- Current candidate: 758 intended files (includes 2 new longitudinal witness files owned solely by witness author).
- Regression base: 756 files with exact exclusion ONLY:
  - `tests/test_dm022_full_lifecycle_v2.py` (63094B at freeze)
  - `tests/dm022_lifecycle_fixture_v2.py` (3892B at freeze)
- Snapshot: `.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/snapshot-bc-20261028T175932Z/worktree` (756 files)
- Manifest: `notes/rephase-1-dm022-prearchitecture-implementation/evidence/source-bc-20261028T175932Z/snapshot-bc-manifest.json`
  - SHA256: `e7d9235ac958f7efd219ed589bad205f3ae6340d45bd49c85a1837d64eca0bae` / 149939B / 756 entries
  - Excluded: `['.git','.git/*','__pycache__','*.pyc','tests/test_dm022_full_lifecycle_v2.py','tests/dm022_lifecycle_fixture_v2.py']`
- Snapshot git: 83 files, HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, origin `example.invalid` inert, no alternates, overlap 0 vs candidate.
- Preservation: `evidence/source-bc-20261028T175932Z/source-bc-preservation.md` (CAND-minus-2 vs SNAP 0 mismatches).
- Snapshot IMMUTABLE. Longitudinal witness copy (`/tmp` private) and old A4/R2 exec/logs NOT reused. C2 author raw under `evidence/integration-c2-a4fix-20261028T171309` qualifies as history only; this composite is the required new proof.

## 2. Exec copy (ignored parent, 409 DB)

- Exec: `.../exec-bc-20261028T175932Z/` (756 files, 83 git, HEAD matches, overlap 0 vs snapshot, 0 manifest mismatches, 0 pycache via `PYTHONDONTWRITEBYTECODE=1`).
- Git env: `NO_GIT_ENV_OVERRIDES` pre-run; per-run `unset GIT_*`; process-scoped `GIT_AUTHOR/COMMITTER=dm022-test-fixture/example.invalid`; no global config mutation; no `git clean/reset`; no fixture deletion.
- Separate witness copy preserved (longitudinal author owns own 2 tests only; will edit own tests separately; not captured while changing per exclusion).

## 3. Runtime (unittest, no pytest dep)

- `/usr/bin/python3` 3.14.4, `jsonschema 4.23.0`, `pypdf 6.16.2`; `python -m unittest` only. Bare-function legacy tests invoked explicitly via unittest where selected. TinyTeX available outside PATH, no install, no PDF build in this task.

## 4. Method (raw-first, unique dir per run)

- Base: `notes/rephase-1-dm022-prearchitecture-implementation/evidence/integration-bc-20261028T175932Z/`
- Per run `run-XX-<name>/` with `header.txt` (command/cwd/python/sourcepin/HEAD/origin/GIT env/PRE-POST), `stdout-stderr-raw.txt` (full tracebacks), `exit-code.txt` (numeric).
- `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -m unittest [discover -s tests -p "<file>" -v | specific-test-path -v]`, `cwd=EXEC`.
- Timeout 600-900s; no timeout occurred (no timeout→PASS). No old runners. No broad full-suite burn (19 runs total). 0 skipped everywhere collected.

## 5. Actual results (collection actuals)

### Targeted fixes — ALL GREEN (89 tests)

| Run | File / selection | Ran | OK | FAIL | ERR | Skip | Exit | Raw SHA |
|-----|------------------|-----|----|------|-----|------|------|---------|
| 01-A-path2 | `test_dm022_prearchitecture_acceptance_v2.Dm022A2OperationTests.test_loader_accepts_str_path_same_as_path + test_loader_wrong_family_str_path` (A path-normalization 2, NOT full A21) | 2 | 2 | 0 | 0 | 0 | 0 | `d1b02c62...` (9 lines) |
| 02-B19 | `test_dm022_prearch_b_ordinary_consumers_v2.py` (changed, 16-19 new lifecycle facade) | 19 | 19 | 0 | 0 | 0 | 0 | `f24008a2...` (45 lines, 9.2s) |
| 03-C2-17 | `test_survey_dm022_c2_consumers_v2.py` (corrected 17) | 17 | 17 | 0 | 0 | 0 | 0 | `3b9aa077...` (55 lines, 41.7s) |
| 04-readerGate-28 | `test_survey_reader_surface_gate_v2.py` (corrected 28) | 28 | 28 | 0 | 0 | 0 | 0 | `89821bef...` (61 lines) |
| 05-pub-9 | `test_survey_publication_v2.py` (corrected 9) | 9 | 9 | 0 | 0 | 0 | 0 | `ad814264...` (15 lines) |
| 06-release-9 | `test_survey_release_checkpoint_v2.py` (corrected 9) | 9 | 9 | 0 | 0 | 0 | 0 | `e96efbfd...` (79 lines) |
| 07-exec-5 | `test_survey_execution_record_v2.py` (5) | 5 | 5 | 0 | 0 | 0 | 0 | `85476b74...` (10 lines) |

- Full A21 NOT rerun (per instruction: unchanged green A21 unnecessary unless B legacy wiring affects A prepare/validState). Justification for skip: B19 exercises real HIGH adopt + `agent.validate_agent_state==[]` + LOW resolve/checker (tests 13-19) and passes; A path2 proves loader normalization preserves adopted-PREARCH identical result; no A prepare/validState failure observed in B19/C2 paths. Exact A21 rerun remains available if root requires it.

### Legacy 9 + Draft/architecture — ALL GREEN (35 tests)

| Run | File | Ran | OK | Exit | Raw SHA |
|-----|------|-----|----|------|---------|
| 08-agent-5 | `test_survey_agent_control_v2.py` | 5 | 5 | 0 | `95e1be5d...` |
| 09-views-2 | `test_survey_active_evidence_views_v2.py` | 2 | 2 | 0 | `77eb8059...` (same bytes as A4 run — stable) |
| 10-selarch-2 | `test_run_selection_architecture_v2_interactive.py` | 2 | 2 | 0 | `a1c69cd3...` |
| 11-draft-5 | `test_survey_drafting_v2.py` | 5 | 5 | 0 | `d8c94ada...` |
| 12-basis-8 | `test_survey_drafting_basis_v2.py` | 8 | 8 | 0 | `90a1ee4a...` |
| 13-histJSON-6 | `test_survey_drafting_historical_json_binding_v2.py` | 6 | 6 | 0 | `c75cf6a7...` |
| 14-integrity-1 | `test_survey_drafting_integrity_v2.py` | 1 | 1 | 0 | `9b59fbdf...` |
| 15-arch-6 | `test_survey_architecture_v2.py` | 6 | 6 | 0 | `3adea311...` |

- All use actual fresh fixtures (temp dirs, independent Git DBs where applicable); no skip-complete (0 skipped); no fake fresh source (real chain helpers, real file bytes/SHAs).

### REQUIRED P1/P2R/P2V/P3S/renewal — SYSTEMIC FIXTURE FAILURES (stopped affected batch)

| Run | File | Ran | OK | FAIL | ERR | Exit | Raw SHA | Root cause |
|-----|------|-----|----|------|-----|------|---------|------------|
| 16-staged-26 | `test_survey_editorial_staged_source_v2.py` | 26 | 0 | 0 | 26 | 1 | `beb84a98...` (889 lines) | `ValueError: contract file does not exist: schemas/dm022-preadoption-report-v2.schema.json` via `survey_production_v2.py:173 aggregate_file_hash` — temp fixture repo lacks `schemas/` tree |
| 17-retention-25 | `test_survey_editorial_retention_v2.py` | 25 | 0 | 0 | 25 | 1 | `551dc955...` (779 lines) | `ValueError: contract file does not exist: schemas/editorial-manuscript-spec-v2.schema.json` — same pattern (helper chain `_build_weekly_validated → _chain → build_authorized_chain → architecture.chain`) |
| 18-longform-31 | `test_survey_longform_derivation_v2.py` | 31 | 1 | 0 | 30 | 1 | `dde569d1...` (813 lines) | Same `schemas/dm022-preadoption-report...` missing (1/31 passes, 30 error) |
| 19-renewal-6 | `test_survey_versioned_renewal_depth_prewrite_v2.py` | 6 | 5 | 0 | 1 | 1 | `f7429849...` (37 lines) | `RenewalHistoryError: HISTORY_BLOB_MISSING: history record ancestor missing: sources: ENOENT 'sources'` at `survey_versioned_renewal_history_v2.py:687 _fd_safe_read` via `verify_versioned_history sources/2026-W37/...r31.json` — temp repo lacks `sources/` tree |

- Per instruction, broad testing stopped for this affected batch after systemic fixture failures (minimal raw returned, no repeat burn of weekly_mechanical/dm001/dm003/dm004 or full suite). Further P1/P2R/P2V files NOT run behind this systemic cause.
- These are NOT DM022 B-lifecycle/A-path/C2 regressions: identical contract-file/sources-tree absence would fail on any base (tests construct isolated temp repos without `schemas/` or `sources/`). No DM022 code change in this composite creates `schemas/` or `sources/` — fixtures must supply them or tests must bind to a repo fixture. Mapping:
  - staged/longform (C1-owned `survey_editorial_staged_source_v2`, `survey_longform_derivation_v2`, `survey_versioned_renewal_*`): fixtures need `schemas/` + `sources/` trees or repo-root binding; return to **C1** (do NOT weaken `aggregate_file_hash` existence check or history blob existence to green).
  - retention (C2-owned `survey_editorial_retention_v2` via drafting/architecture helpers): same fixture-tree gap; return to **C2** (helper `_build_weekly_validated` chain needs repo fixture, not dict-only).
- No DM022 integration fault proved by these 4 runs; prior targeted/Draft/architecture greens (124 tests) stand.

## 6. Totals (this composite)

- Targeted + legacy + Draft/arch: 124 ran (2+19+17+28+9+9+5+5+2+2+5+8+6+1+6), 124 pass, 0 fail/error, 0 skipped.
- P1/P2R/P2V/P3S/renewal attempted: 88 ran (26+25+31+6), 6 pass, 0 fail, 82 errors, 0 skipped.
- Grand: 212 ran, 130 pass, 82 errors, 0 skipped. Later lifecycle seams NOT proved by earlier passes; no whole-acceptance inference.
- Exec invariant held (PRE/POST 756, 0 pycache throughout; failures are fixture-tree absence / functional contract, NOT source drift, NOT import/setup systemic for DM022 scope).

## 7. Identity/proof limits + handoff

- Fixed 756-base `e7d9235a...` + exec `...175932Z` + HEAD `409b292...` + inert origin; independent DBs with synthetic provenance (process identity); no genuine approvals; no Production semantic claim. Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN preserved except progress. Longitudinal 2-file witness is SEPARATE (witness author owns only those 2, will run own new tests only, no existing files).
- Full A21 rerun NOT done per instruction (unnecessary green repeat); B-lifecycle new facade does NOT break A prepare/validState in this composite (B19 real-adopt paths green). If root requires exact A21 for B-legacy-wiring proof, run `tests.test_dm022_prearchitecture_acceptance_v2` (21 tests) on this same exec and append raw — no new freeze needed unless candidate moves.
- Return to root: assign C1/C2 fixture-tree bindings for staged/retention/longform/renewal (supply `schemas/`/`sources/` repo fixtures, do NOT weaken existence checks), then run remaining P1/P2R/P2V/P3S/renewal + weekly_mechanical/dm001/dm003/dm004 as applicable + later lifecycle witness (present-old-seven-slots retain/clear/regenerate already unblocked by B Blocker1 fix, Draft accepted-authority unblocked by Blocker2 fix) + independent implementation review. No premature whole acceptance. Stop at Human Commit Point.
