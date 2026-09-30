# R1 e4-lineage assembly — milestone-2 selected verification report

Worker: FRESH General Co-Worker (bounded verification, not independent reviewer). Task: `notes/rephase-1-r1-assembly/verification-task.md` (read fully). Candidate and sources unchanged; only new unique evidence in this run dir. Milestone-1 originals supplemented, never silently rewritten. No code changes, no new commits, no full-97 rerun.

## 1. Fixed candidate and preconditions

- Candidate `481dec0c0233d7871df79a07a88aa5fe2291daa3`, tree `657032438c6ed8b1c055d5a120b67b4b261a5092`, parent exact `e4c82692abee6acedbba07815b0d74ccefb80a7e`, branch `codex/rephase-1-r1-assembly`, fixture `/tmp/jgas-rephase-r1-assembly-20260929T143833Z`.
- Before EVERY process (tests, diagnostic, observation): fail-closed check of expected HEAD/tree/parent, clean tracked bytes and index (`status --porcelain` shows only `??` pycache, `diff`/`diff --cached` empty), and no inherited Git overrides (env scan for `GIT_*` empty). `PYTHONDONTWRITEBYTECODE=1` set for every process. Actual source paths/hashes recorded (seven SHA-256 match milestone-1 manifest; module `scripts/survey_weekly_derivation_v2.py` SHA-256 `1cb1f705cd2481b93ddacc93e5c20e2f0adf1622effe86e5ccf0fce4ce6ed2cc`).
- Python MUST `/tmp/jgas-rephase-application-venv/bin/python3.12`, version `3.12.14` (3.10 was stdlib-only Git copying in milestone-1; all Core imports here are 3.12). Distributions via stdlib `importlib.metadata` (pip itself absent: `python3.12 -m pip freeze` → `No module named pip`, recorded separately, not a test failure): attrs 26.1.0, jsonschema 4.23.0, jsonschema-specifications 2025.9.1, pypdf 6.16.2, referencing 0.37.0, rpds-py 2026.6.3, typing_extensions 4.16.0 — identical to R1 manifest.
- Class/method existence verified BY SOURCE before running (no malformed argv attempted): `tests/test_survey_weekly_mechanical_refresh_v2.py` has single class `WeeklyMechanicalRefreshV2Tests` at line 63; methods at lines 328 (`test_first_and_repeat_success`), 424 (`test_active_predecessor_not_noop_and_artifact_only_noop`), 444 (`test_pre_install_control_change_unsupported`), 1525 (`test_metadata_revalidation_effective_rows_then_refresh`). Worker's initial proposal examples omitted the class and were unexecuted; the executed argv below is the corrected root selection.

## 2. Four selected tests — one argv, synthetic fixtures

Exact single argv (multiline display is not a shell script), CWD assembly checkout:

```text
/tmp/jgas-rephase-application-venv/bin/python3.12 -m unittest -v
  tests.test_survey_weekly_mechanical_refresh_v2.WeeklyMechanicalRefreshV2Tests.test_first_and_repeat_success
  tests.test_survey_weekly_mechanical_refresh_v2.WeeklyMechanicalRefreshV2Tests.test_metadata_revalidation_effective_rows_then_refresh
  tests.test_survey_weekly_mechanical_refresh_v2.WeeklyMechanicalRefreshV2Tests.test_active_predecessor_not_noop_and_artifact_only_noop
  tests.test_survey_weekly_mechanical_refresh_v2.WeeklyMechanicalRefreshV2Tests.test_pre_install_control_change_unsupported
```

Outcome (one run, no retry): exit `0`; `Ran 4 tests in 332.190s`; `OK`; 0 failures/errors/skips. Per-test lines all `... ok` with fully qualified names (see `raw/four-tests.stderr`, 818 bytes). Stdout (3064 bytes) is synthetic publisher JSON for `2026-W37` (`SURFACE_MATERIALIZED`, validated-source-manifest, main.tex/bindings) — exact output/authority synthetic, not historical-edition revalidation. Raw files: `raw/four-tests.stdout`, `raw/four-tests.stderr`, `raw/four-tests.exit`.

Scope truth: these tests instantiate fresh synthetic Git repos using assembled SOURCE; their fixture histories are NOT the e4 lineage. Assembly checkout itself unchanged (HEAD/tree/status identical before/after; no State/Gate/receipt/data writes; synthetic child fixtures only inside tests' temp dirs). Pycache prevented via `PYTHONDONTWRITEBYTECODE=1` (inherited by test child process); existing pycache left untouched, never cleaned.

## 3. Assembled-database diagnostic — binds real inherited history

Fresh process importing exact assembly source (`sys.path` DST first), read-only against actual assembly repository. No lazy-fetch/network/hydration, no alternate DB, no fabricated stubs, no diagnostic artifacts committed.

1. Confirmed exact HEAD/tree/parent, clean tracked/index, module path/hash (see manifest; `E4_IS_ANCESTOR_OF_HEAD` exit 0; `LOG2` shows `481dec0 parent e4`, `e4 parent 6d87edd`).
2. Current closure (8 rows, `current_closure(root)`) passes: `_verify_head_bytes(repo, 481dec0, current_closure)` → pass. Rows recorded in manifest (derivation `1cb1f7...`, plus seven unchanged).
3. Historical eight-file closure at exact e4 built from available local committed blobs via `git show e4:<name>` (NOT current hashes relabelled): `verify_closure_at_commit(repo, e4_closure, e4)` → pass. Rows in manifest; derivation differs (`e4 e2e403...` vs current `1cb1f7...`), other seven identical — proving real historical-vs-current distinction. (Git blob IDs are SHA-1 and are not conflated with closure SHA-256.)
4. Ordinary current-tool replay with e4 generating basis rejects as intended: `_verify_head_bytes(repo, e4, e4_closure)` raises `ValueError: Weekly receipt implementation or contract changed since renderer commit` — exact type/message kept, success sentinel `DIAG_SENTINEL_OK` printed OUTSIDE the handler. All eight `git show e4:<name>` succeeded, ancestor check passed, so this is the intended control-diff rejection, not missing-object/setup failure.
5. No-write before/after: HEAD/tree/parent identical, tracked-dirty 0, empty diffs; no State/Gate/receipt/historical-data mutation; pycache prevented, never cleaned.

Exit `0`, stderr empty, stdout 3581 bytes (`raw/diagnostic.*`). This is a source-history function diagnostic, not real edition revalidation; no old receipt authority manufactured.

## 4. Preserved comparison evidence and observation gap

- `scripts/` holds byte copies of all 17 actual scripts used across milestone-1 assembly verification and this verification (hashes in manifest). They are historical evidence, not rerun instructions. Only unrelated temp files excluded. No secrets or global config dump included.
- Observation gap: milestone-1 `verify_assembly`/`verify_preimage`/`verify_equivalence`/`verify_post` full stdouts were observed in tool-call records and summarized in milestone-1 manifest/report, but NOT saved as separate raw files then. Do not reconstruct them from summaries. Script sources above preserve the procedures; pre-copy refs and check-time source status remain as observed-not-recreated in milestone-1 manifest.
- NEW OBSERVATION (labeled, current scope after commit, not historic recreation): post-commit read-only check shows refs now 7 (6 old + new assembly branch), objects SRC 6235 → DST 6247 (larger expected: 7 new blobs + trees + commit), all 6235 old source object paths present with 0 same-inode and 0 hash mismatch (physically independent). Exit 0 (`raw/new-observation.*`).

## 5. Qualifications (corrections to unexecuted proposals)

- Hooks: milestone-1 commit used normal args with no bypass flags; that does NOT independently prove any particular hook existed or executed. No new hook run here. Prior `hooks ran normally` phrasing is qualified accordingly.
- Metadata: immutable tree comparison establishes unchanged REFERENCES for inaccessible promisor data, not validation of missing blob content nor complete fixed-baseline application.
- No full-97 rerun; old b74 matrix stays original scope. No PASS transfer. Whole candidate NOT_READY; step 4/B3 open.

## 6. Files new this unit / return

New only under `notes/rephase-1-r1-assembly/20260929T145048Z-verification/`: `manifest.json` (this packet's noncompact IDs), `report.md` (this file), `raw/` (9 log/exit files), `scripts/` (17 .py). Milestone-1 originals untouched. No reconstruct commit/push. Candidate `481dec0`/`6570324`/parent e4 fixed; e4/B/R1 heads untouched.

Actual returns: four-test exit 0 / 4 ran / OK / 332.190s / 0 skips; diagnostic three controls (current-pass at 481dec0, historical-pass at e4 with real e2e403-vs-1cb1f7 derivation distinction, intended `ValueError` stale rejection) exit 0; NEW OBSERVATION 6235→6247 independent-plus-new exit 0. Root next commissions separate author-independent bounded assembly review. Worker stops after return; no implementation or further delegation.
