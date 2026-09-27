# Re:Phase step-4 next unit — Gate CLI persisted-review admission (milestone 1)

- Recorded: **2026-09-27 JST** by **General implementation Co-Worker** (not Sol/Luna, not independent reviewer). Root/Astra owns scope and review; this packet is Co-Worker evidence. Actual serving model not independently verified.
- Status: **first milestone only.** Independent B DB copied and verified; real CLI parent witnesses executed; concrete path inventory and proposed test plan returned. **No runtime fix implemented; no source bytes changed; no B suite rerun.**
- Scope: persisted reader-surface review admission through `scan-manuscript` only. No publisher/schema/lifecycle/build/Freeze/Release change. No production/main/network/Actions.
- All persisted review records in this packet are **explicitly synthetic and labelled** (`reviewed_by = "synthetic-parent-witness (not human)"`); they are not real Human review, publication or adoption evidence.

## 1. Candidate and independent DB identity

| Item | Value |
|---|---|
| Candidate (preserved B) | `c04f32ad46109403e8a63faaa8394a90ee6b869c` |
| Tree | `7dbcbbdb499ea6c7d33417a16144107320e1fd06` |
| Parent | `cb96ab97045b0d0767f38806809d33e383bac73d` |
| Branch | `codex/rephase-1-increment-b` |
| Source fixture (read-only, not mutated) | `/tmp/jgas-rephase-increment-b-sol-implementation` |
| **New independent DB** | **`/tmp/jgas-rephase-gate-cli`** |
| Inert origin | `https://example.invalid/rephase-increment-b.git` |
| Shallow/partial boundary | `774dd39a951c9ac3818e83dfffd4c7666efb0a20` (`.git/shallow`) |

The source B fixture is a **shallow, partial (promisor) clone**: `.git/shallow` pins the fixed baseline and `pack-*.promisor` files mark unavailable historical blobs. A full clone/bootstrap against the inert origin would hit the known missing-object problem, so the new DB was produced as an **independent byte copy** (`setup/01-copy-b-db.sh`, `cp -r --preserve=mode,timestamps,ownership`), never a clone or alternates link.

Isolation verification (`setup/02-verify-isolation.sh`, log `logs/02-verify-isolation.log`):
- HEAD/tree/parent/branch identical to B; refs identical (a, b, r2, freeze, r2-original).
- `NO_ALTERNATES`; no `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE`/`GIT_OBJECT_DIRECTORY`/`GIT_ALTERNATE_OBJECT_DIRECTORIES` overrides; `--git-common-dir` = `.git`.
- `find -type l` empty (no symlinks); `find -type f -links +1` empty (no hardlinks); cross-DB inode intersection empty (7037 src vs 7037 dst files, `comm -12` empty).
- `git count-objects` identical (6219 loose, 2277 in-pack, 44M). `git fsck` reports the pre-existing promisor "missing blob" set (inherited, not caused by the copy).
- Key file SHA-256 equals `notes/rephase-1-increment-b/candidate.json` (`logs/04-fingerprint-db.log`): `survey_reader_surface_gate_v2.py` = `7eb1210d…c588d`, `survey_reader_publication_v2.py` = `d2145042…1ff69`, `survey_weekly_semantic_publication_v2.py` = `53315030…f3f7`, `survey_weekly_derivation_v2.py` = `e2e403ac…354a4`.
- Pack SHA-256: `pack-7d6ac066…` = `804b58c0…16ee`; `pack-fed0279f…` = `2e56f9b8…5270`.
- Runtime/environment: WSL Ubuntu native ext4 (`/dev/sdd`), git 2.34.1, `/tmp/jgas-rephase-application-venv/bin/python3.12` = CPython 3.12.14.

## 2. Concrete runtime/test path inventory

Runtime (single file):
- `scripts/survey_reader_surface_gate_v2.py`
  - `main()` CLI: lines 1796–1926; `scan-manuscript` dispatch 1862–1920. Inputs: `--semantic-authority` (authority object **or** review record), `--semantic-review` (**findings array only**), `--synthesis-result`, `--output`, `--state`. There is **no** `--semantic-review-path` CLI option.
  - Defective review-record branch: lines 1870–1883. Line **1877** reads `sem_data.get("source", {}).get("sha256")` but `reader-surface-semantic-review-v2` carries **`reviewed_surface`**, so `surface_sha256` becomes `None`. Line **1879** applies `Path(args.semantic_authority).relative_to(repo_root)` to the **unnormalized** argument (`repo_root = Path(args.repo_root).resolve()`, line 1823).
  - `evaluate_reader_surface_gate`: lines 1121–1471. Requires semantic authority (1144–1147). `semantic_review_path` branch 1155–1164 (strict loader). `semantic_authority` branch 1165–1194 rejects missing `surface_sha256` (1169–1173). Route/receipt selection: `_derivation_for_manuscript` 1396–1399; DIRECT_PRIMARY vs WEEKLY_GENERATED_V2 at 1071–1118.
  - Strict loader `load_and_validate_reader_surface_semantic_review`: 884–1045 (schema, digest, `reviewed_surface`, stale-bytes, checks, `READER_PIPELINE_INDEPENDENCE`, identity).
  - Helpers: `_resolve_repo_path` 462–473; `_rel` 476–478; `_derivation_for_manuscript` 1071–1118.
- `scripts/survey_production_v2.py` `repo_local_path` (line 222) requires a **repository-relative** path string (rejects absolute with "must be a repository-relative path without traversal").
- Correct working reference (do not modify in this unit): `scripts/survey_reader_publication_v2.py` `build_reader_surface_gate` lines 638–706. It validates via the strict loader, then builds `semantic_authority` with `surface_sha256 = validated_sem["surface_sha256"]` (from `reviewed_surface`) and `review_path = _rel(repo_root, semantic_review_path)` (normalized). This is the behavior the CLI branch should match.
- Schema: `schemas/reader-surface-semantic-review-v2.schema.json` — `review_kind const SEMANTIC_EDITORIAL`, required `reviewed_surface {path, sha256}`, `READER_PIPELINE_INDEPENDENCE` check convention.

Reusable fixtures / affected tests:
- `tests/test_survey_reader_surface_gate_v2.py` — **direct-primary fixture**, 27 methods. `_setup_edition` 29–177, `_build_valid_manifest` 179–235, `_create_semantic_surface_and_review` 237–313 (writes a schema-valid persisted review; default reviewed surface == manifest primary → DIRECT_PRIMARY). No CLI/subprocess usage today.
- `tests/test_survey_increment_b_weekly_derivation_v2.py` — **accepted Weekly publisher fixture**, 8 methods. `_chain` 77–121, `_complete_authorities` 122–221, `_current_state` 242–300, `test_accepted_weekly_two_pass_publication` 313–440 (publisher CLI → canonical `reader-surface-input-v2.json`, synthetic persisted review, then `build_reader_surface_gate` **API**). This is the justified generated-route connection. **Precise mocking note (correction):** `_chain` patches only fixture-constructor helpers — `SurveyEvidenceV2Tests.sandbox` (noop cleanup/root/cfg), `SurveyEvidenceV2Tests.init_profile` (real `weekly_profile`+`initialize`), `SurveyArchitectureV2Tests.architecture_for` (real plan plus publication extensions) and the `IMPLEMENTATION_SHA` module constants. It does **not** stub any authority validator, stage validator, publisher, receipt replay or Git check: those run for real. No validator or Git-success stub is present or permitted.
- `tests/test_survey_publication_revalidation_v2.py` — module-level `Fixture` 46–461 (importable), 23 methods; writes `reader-surface-semantic-review-v2.json` and calls `build_reader_surface_gate`.
- `tests/test_survey_exact_manuscript_admission_v2.py` — the **importlib module-qualified fixture pattern** (lines 25–36) to copy for the new CLI test module; do not import TestCase aliases into discovery.
- `tests/test_survey_increment_b_boundary_matrix_v2.py` — 7 methods.
- No `tests/__init__.py` (namespace package); suites are run with `python -m unittest tests.<module>` from the repo root (see `notes/rephase-1-increment-b/final-matrix-c04f32a.sh`).

## 3. Parent witnesses (real CLI subprocess, no fix)

Runner `witness/run_parent_witness.py` (SHA-256 `58b1b00d…7596`) reuses the existing direct-primary fixture via `importlib` (no unittest discovery), writes a **schema-valid** persisted review with an accurately-synthetic reviewer, and invokes the real CLI via `subprocess` (venv `python3.12`, clean `GIT_*` env, `PYTHONPATH` = DB root). Logs: `logs/parent-witness/`.

Fixture facts (schema-valid, DIRECT_PRIMARY): manifest `primary_source.path = surveys/weekly/2026-W35/main.tex`, sha256 `37a4cd01…da6e`; `reviewed_surface.path` identical; `review_kind = SEMANTIC_EDITORIAL`; `review_sha256 = 8d79fc87…6fe7`.

| Witness | argv path form | cwd | exit | observed (raw stderr) |
|---|---|---|---|---|
| `absolute-contained` | absolute path inside `--repo-root` | temp repo root | 1 | `ValueError: semantic_authority missing required field: surface_sha256; synthetic PASS dictionary is rejected` (gate_v2.py:1171) |
| `repo-relative` | `sources/2026-W35/.../reader-surface-semantic-review-v2.json` | temp repo root | 1 | `ValueError: 'sources/…json' is not in the subpath of '/tmp/tmp…'` (gate_v2.py:1879) |
| `relative-cwd-differs-supplementary` | same repo-relative path | fixture git root | 1 | `FileNotFoundError: 'sources/…json'` (gate_v2.py:1871, unnormalized load) |

Positive controls (same fixture, same persisted review, in-process — prove no setup failure masking):
- `strict-loader semantic_review_path (repo-relative)` → **PASSED** (`evaluate_reader_surface_gate(..., semantic_review_path=REVIEW_REL)`).
- `authority-object (correctly built)` → **PASSED** (strict loader output passed as `semantic_authority`).

Interpretation: the persisted review and direct-primary fixture are sound; the failures are confined to the CLI review-record branch (wrong field `source` vs `reviewed_surface`; unnormalized path). Absolute path reaches the field mismatch; repo-relative path reaches the `relative_to` bug. Both lower-level entry points already work.

### Failure/setup history (preserved)
- First runner invocation (not a defect): the strict-loader positive control initially passed an **absolute** review path to `semantic_review_path`, which failed with `ValueError: semantic review record must be a repository-relative path without traversal` because `evaluate_reader_surface_gate`/`core.repo_local_path` require a repo-relative string. Corrected to `REVIEW_REL`; both controls then passed. Recorded here; no separate log retained (logs were regenerated by the corrected run).
- `git fsck` "missing blob" output is the inherited promisor/shallow state of the source fixture, not a copy defect.

## 4. API / containment details relevant to the bounded fix

- `--semantic-authority` currently conflates two input kinds. Preserve the authority-object branch (1869,1882–1883) unchanged; only the reader-surface review-record branch is defective.
- Correct route for a persisted `reader-surface-semantic-review-v2` record: normalize relative to `--repo-root` (e.g. `_resolve_repo_path`/`_rel`), then feed **`evaluate_reader_surface_gate(..., semantic_review_path=<repo-relative>)`** so the existing strict loader (including containment and stale-bytes checks) is the sole authority source. `semantic_review_path` must be repo-relative (not absolute) because `evaluate` calls `core.repo_local_path`.
- Preserve repository containment: the normalized path must still be rejected if it escapes `--repo-root`; the loader's `_resolve_repo_path` and `core.repo_local_path` already enforce this.
- `--semantic-review` is a **findings array**; it must not be treated as a review record or authority object. No silent conversion of legacy `publication-review-record-v2` (the strict loader rejects it by design).

## 5. Proposed implementation test plan (for root approval; not started)

Runtime change (single bounded region): `scripts/survey_reader_surface_gate_v2.py` `scan-manuscript` handler only.
New focused test module (importlib fixture pattern): `tests/test_survey_gate_cli_persisted_review_v2.py`.
CLI invocation: real subprocess of `scripts/survey_reader_surface_gate_v2.py` with a clean env, absolute/relative path and differing-cwd cases (pattern: `witness/run_parent_witness.py`).

Cases:
1. DIRECT_PRIMARY persisted review, absolute contained path → exit 0, `--output` Gate `PASSED`, Gate validates via `validate-gate` and against selected manuscript.
2. DIRECT_PRIMARY persisted review, repo-relative path with cwd == repo root → exit 0.
3. Same relative path with cwd != repo root (normalization to `--repo-root`) → exit 0 (fixes the FileNotFoundError case).
4. Generated Weekly via accepted upstream fixture (reuse `test_survey_increment_b_weekly_derivation_v2` publisher setup + `--state`) → exit 0; independently validate emitted Gate against selected manuscript and receipt.
5. Negatives (must not PASS or mutate State/authority): missing review, schema-invalid/legacy review, stale (drifted surface bytes), wrong-target (different surface), non-PASS decision, unresolved blocking finding, path escaping repo root, invalid authority object.
6. Authority-object branch regression: correctly-built authority object still PASSES; malformed/synthetic authority object still rejected.
7. `--semantic-review` findings-array behavior unchanged.

Regressions: run only `tests.test_survey_reader_surface_gate_v2`, `tests.test_survey_increment_b_weekly_derivation_v2` (generated-route connection), and the new module. Do **not** rerun the full 132-method matrix.

## 6. Scope blockers / decisions for root

- No new schema, authority, producer, Gate, approval or Release change appears necessary; the fix is confined to CLI argument handling. If root prefers to build the authority dict instead of routing via `semantic_review_path`, the minimum correction is `reviewed_surface.sha256` + `_rel(repo_root, ...)`; the strict-loader route is recommended and matches the task.
- Generated-Weekly CLI proof depends on the heavy B publisher fixture (real isolated Git repo; patches only fixture-constructor helpers `sandbox`/`init_profile`/`architecture_for` and `IMPLEMENTATION_SHA`, never validators or Git checks). It is reusable but must be invoked in a way that avoids unittest discovery duplication (importlib or in-process `main()` mirroring B), and it needs the `--state` file. No authority expansion required.
- `--semantic-authority` accepting both input kinds is an existing public contract; the fix must keep the authority-object meaning and document the review-record meaning.
- Whole-profile/Step-4/B3 acceptance is **not** claimed; this unit only repairs the advertised `scan-manuscript` contract.

## 7. Reproduce

```
wsl -d Ubuntu -- bash /mnt/d/Git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-gate-cli/setup/01-copy-b-db.sh
wsl -d Ubuntu -- bash /mnt/d/Git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-gate-cli/setup/02-verify-isolation.sh
wsl -d Ubuntu -- bash /mnt/d/Git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-gate-cli/witness/03-run-parent-witness.sh
wsl -d Ubuntu -- bash /mnt/d/Git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-gate-cli/setup/04-fingerprint-db.sh
```

Packet hashes: `setup/01` `97eb1190…5ed7`; `setup/02` `34e9f37e…ba9c`; `setup/04` `9a21138e…d5d0`; `witness/run_parent_witness.py` `58b1b00d…7596`; `witness/03` `03d7c7d3…9fd9`.

No B suite was rerun; no reconstruct/fixture runtime bytes were changed; the source B fixture remains read-only.
