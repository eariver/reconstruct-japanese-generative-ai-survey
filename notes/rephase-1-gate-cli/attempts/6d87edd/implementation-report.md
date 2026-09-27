# Gate CLI persisted-review admission — bounded implementation report

- Recorded: **2026-09-27 JST** by **General implementation Co-Worker** (not Sol/Luna, not independent reviewer). Root/Astra approved this bounded unit; this report is Co-Worker evidence, not adoption or independent acceptance.
- Candidate: **`6d87edd28a1be8893ca2ab67fed6e32e54b0de6c`**, tree `777c65e9e51fa5c31953808520ee00db65514d03`, parent B `c04f32ad46109403e8a63faaa8394a90ee6b869c`, branch `codex/rephase-1-gate-cli`, in isolated DB `/tmp/jgas-rephase-gate-cli`.
- Scope: single runtime path `scripts/survey_reader_surface_gate_v2.py` `scan-manuscript` + new `tests/test_survey_gate_cli_persisted_review_v2.py`. No publisher, schema, lifecycle, build, Freeze/Release, State or authority change. No production/main/network/Actions access.
- All manifests, reviews and authorities exercised are **synthetic and labelled** (`reviewed_by = "synthetic Gate CLI reviewer (not human)"`). No real Human Gate, publication or adoption is asserted.

## 1. Change mechanism (exact)

`scan-manuscript` previously loaded `--semantic-authority` with `Path(...)` (cwd-relative, before containment) and, for any `review_kind == SEMANTIC_EDITORIAL` record, synthesized an authority dict reading the wrong field (`source.sha256` instead of `reviewed_surface.sha256`) and calling `Path(args.semantic_authority).relative_to(repo_root)` on the unnormalized argument. The bounded change:

1. Resolves `--semantic-authority` through `_resolve_repo_path(repo_root, ..., "semantic authority record")` **before loading**, so containment is enforced and the returned repository-relative path is used.
2. If the loaded object is a persisted review record (`dict` with `review_kind == SEMANTIC_EDITORIAL`), it is passed **as `semantic_review_path=<repo-relative>`** to `evaluate_reader_surface_gate`, i.e. through the existing strict loader (`load_and_validate_reader_surface_semantic_review`). No authority dictionary is synthesized; no ad-hoc PASS/reviewer default.
3. Any other JSON object is passed through the **authority-object branch unchanged** (`semantic_authority=sem_data`).
4. `--semantic-review` remains a separate findings argument; it is not treated as authority.
5. CLI help for `--semantic-authority` corrected to describe both accepted forms. `--semantic-review` help unchanged.
6. Invalid input fails nonzero via the existing paths (load/loader/validator errors); no broad error framework added.

Diff: `increment-gate-cli.patch` (SHA-256 `f8593bdd…b1d`, 35134 bytes). Changed files with verified byte copies in `changed-files/` (disk copy Git object id equals the committed blob):
- `scripts/survey_reader_surface_gate_v2.py` — blob `ea1eb652…`, sha256 `78f136a0…`, 84430 bytes.
- `tests/test_survey_gate_cli_persisted_review_v2.py` — blob `258ec363…`, sha256 `d5bd97f5…`, 30903 bytes.

## 2. Test evidence

Command/cwd/runtime/dependency inventory is recorded in the raw log itself (via `importlib.metadata`; `pip` was not invoked and no missing-`pip` command was repeated). Relevant run (committed successor, clean tracked tree): `logs/candidate-relevant-tests-6d87edd.log` (sha256 `85785b1a…`), exit `0`, **32 tests, 32 ok, 45.031 s**, modules `tests.test_survey_reader_surface_gate_v2` (27) + `tests.test_survey_gate_cli_persisted_review_v2` (5). The generated-route connection is exercised by the new module; the full historical matrix and the other 7 Weekly methods were deliberately not run.

Dependency/runtime inventory (from the committed run): CPython 3.12.14 at `/tmp/jgas-rephase-application-venv/bin/python3.12`; jsonschema 4.23.0, pypdf 6.16.2, attrs 26.1.0, rpds-py 2026.6.3, referencing 0.37.0, jsonschema-specifications 2025.9.1, typing-extensions 4.16.0.

New-module cases:
- `test_direct_primary_cli_admission_absolute_relative_and_cwd`: real CLI subprocess PASS for absolute, repo-relative (cwd == repo root) and repo-relative with **cwd differing from repo root**; each emitted Gate independently read back and validated (`validate_reader_surface_gate(..., expected_manuscript_path=...)`), route `DIRECT_PRIMARY`; main.tex/manifest/review unchanged.
- `test_direct_primary_cli_negative_cases`: missing review; digest mismatch (renewed digest); malformed record missing `reviewed_surface` (renewed digest); legacy publication-review shape (renewed digest); non-PASS review (renewed digest); PASS-with-unresolved-blocking (renewed digest); wrong-target surface; path escape `../`; outside-symlink escape; malformed authority object; bare-array authority JSON. Each exits nonzero and never yields an admissible PASSED Gate; state/upstream snapshot unchanged. Non-PASS writes a **diagnostic FAILED report** (existing CLI behavior, distinct from an authority write) and still fails validation.
- `test_authority_object_and_findings_argument_paths`: correctly-built authority object PASS; `--semantic-review` JSON object is treated as findings, not authority (does not replace the persisted review); bare-array findings argument recorded as a pre-existing load limitation (see §4).
- `test_unrelated_same_issue_manuscript_rejected`: a valid same-issue alternate manuscript is rejected by independent expected-manuscript validation (`... does not bind the exact expected Reader Manuscript`) while the original manuscript still validates; CLI with the alternate manuscript and the original review is rejected.
- `test_generated_weekly_cli_admission_and_readback`: real accepted Weekly chain via the publisher, persisted review routed through the CLI with `--state`; emitted Gate independently validated (route `WEEKLY_GENERATED_V2` == `weekly.ROUTE`), receipt re-read and bound paths/digests checked, `weekly.validate_receipt` re-run; production-state and upstream bytes unchanged.

Generated-Weekly fixture identity: the new module builds an equivalent bounded setup using process-local `GIT_AUTHOR_*`/`GIT_COMMITTER_*` env (no `git config`) and an inert origin; the B test was not edited. Only fixture-constructor helpers `sandbox`/`init_profile`/`architecture_for` and `IMPLEMENTATION_SHA` are patched (as documented); no validator, publisher, receipt or Git check is stubbed.

## 3. Parent witnesses preserved

Milestone-1 parent witnesses (pre-fix) remain under `logs/parent-witness/` with raw stdout/stderr/exit: absolute-contained → missing `surface_sha256`; repo-relative (cwd == root) → `relative_to` path bug; relative with cwd differing → `FileNotFoundError`; plus strict-loader and authority-object positive controls. The first in-development setup attempt's log was overwritten (already disclosed in `inventory.md`); it is not recreated or called clean. All later logs use unique attempt names and are append-only.

## 4. Observations and limitations (not silently fixed)

- **`--semantic-review` is advertised as a findings JSON array, but `core.load_json` is object-only**, so a bare array cannot be loaded and the argument fails nonzero. This is a pre-existing, separate CLI defect outside the selected unit and was left unchanged (no runtime expansion). The new tests record it explicitly. Astra may decide a separate bounded unit.
- Negative non-PASS runs write a diagnostic **FAILED** report before returning nonzero; this is the existing `evaluate` behavior and is asserted to be non-admissible rather than treated as an unauthorized write.
- `git fsck` missing blobs in the DB are the inherited shallow/promisor state of B, not a copy or commit defect.
- No independent review, no seven-point audit, no whole-profile/Step-4/B3 completion, no adoption is claimed. `.gitattributes` gained one `-text` rule for this packet (artifact byte fidelity), matching the A/B precedent.

## 5. Recovery / reproduce

Successor recovery: DB `/tmp/jgas-rephase-gate-cli` at `6d87edd`; or apply `increment-gate-cli.patch` to B `c04f32a` and verify the changed-file sha256 above. Reproduce candidate tests: `wsl -d Ubuntu -- bash notes/rephase-1-gate-cli/run-candidate-tests.sh`. Rewriting the log overwrites recorded evidence, so future runs must use new attempt names.

Awaiting Astra source/oracle/evidence review; no further delegation performed.
