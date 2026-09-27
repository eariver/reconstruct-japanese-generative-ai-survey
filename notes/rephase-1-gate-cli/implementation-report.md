# Gate CLI persisted-review admission — corrected test/evidence report

- Recorded: **2026-09-27 JST** by **General implementation Co-Worker** (not Sol/Luna, not independent reviewer). Root/Astra approved the runtime correction and required test/evidence fixes; this is Co-Worker evidence, not adoption or independent acceptance.
- Successor: **`e4c82692abee6acedbba07815b0d74ccefb80a7e`**, tree `bc377b6b7eb1e47dacd719e0f76b5a86703f3f3e`, parent `6d87edd28a1be8893ca2ab67fed6e32e54b0de6c` (test-corrected successor), in isolated DB `/tmp/jgas-rephase-gate-cli`, branch `codex/rephase-1-gate-cli`.
- Antecedent: `6d87edd` (runtime + first test draft) archived at `attempts/6d87edd/`. **Runtime bytes are identical** at both heads (`scripts/survey_reader_surface_gate_v2.py` blob `ea1eb652ab49eb479e17318712d84c318bfaf475`); the successor commits only `tests/test_survey_gate_cli_persisted_review_v2.py`.
- All manifests, reviews and authorities are **synthetic and labelled** (`synthetic Gate CLI reviewer (not human)`). No real Human Gate, publication or adoption is asserted.

## 1. Astra corrections applied (runtime unchanged)

1. **Unrelated same-issue manuscript negative now uses a genuinely valid second manifest.** The alt manifest keeps the canonical primary/support and changes only permitted accountability metadata (`authored_by`, `recorded_at`) with a fresh digest, distinct path. Both manifests are positively validated with the real `reader.validate_manuscript_manifest`, and their primaries are asserted equal. The test now asserts the selected exact match passes and the different valid same-issue manifest fails with the exact-binding error (message contains the alt path and alt file sha256). The previous invalid `alternate.tex` manifest and its `cli-manuscript-mismatch` subcase were removed; the separate wrong-reviewed-target negative remains.
2. **Findings transport no longer institutionalized.** The arbitrary-object acceptance and bare-array "expected failure" assertions were removed from the normative test. The main separation property is now asserted: a valid persisted review supplied **only** via `--semantic-review` (no `--semantic-authority`) is rejected with `requires machine-checkable semantic_authority`. The inherited array/object behavior is preserved as an observational, non-normative probe (`witness/run_findings_transport_probe.*`, raw output `logs/findings-transport-probe-20260927T1/`) with an explicit **deferred disposition**: fixing array loading/suppressions transport is out of scope for this unit.
3. **Wrong-target negative asserts the intended boundary.** The wrong-target review is first positively validated by the strict loader (schema + digest + bound surface), then the CLI failure is asserted to be the route/target boundary (`Weekly complete reader input`), not merely any nonzero. The legacy-shaped record is now described as **legacy-shaped invalid pre-TeX input** (not a schema-valid publication review); the canonical valid legacy rejection remains covered by the existing 27 Gate methods (`test_required_f_legacy_publication_review_rejected`).
4. **Evidence counting and oracle accuracy.** Counts are reported as **test methods and subtests**, not "scenarios": 32 methods (27 existing + 5 dedicated) with 16 `subTest` blocks / 18 executed subcases. The deliberate `review_sha256` corruption is labelled "deliberately broken review_sha256", not "renewed". The generated-Weekly oracle was broadened from a watchlist to a **whole-tree no-upstream-write snapshot** (every regular file under the fixture repo except `.git`): the CLI adds only its declared Gate output and modifies no existing file. Root's source review that the diff adds no upstream write call is thereby separated from an *executed* unchanged-tree result.
5. **Immutability, repro hygiene, attempt preservation.** The `6d87edd` manifest/patch/changed-files/report/raw log were archived under `attempts/6d87edd/` before re-packaging. The new commit is local and test-only, with env identity, normal `status`/`diff`/`log` inspection, no amend/config write/identity backdating. All failed attempts are preserved and listed below. Reproduction requires the absolute WSL path and is explicitly **not** a safe re-run.

No candidate `.gitattributes` change was added; the existing reconstruct artifact-fidelity rule for `/notes/rephase-1-gate-cli/**` (added at milestone 1 and accepted) is retained.

## 2. Change mechanism (runtime; unchanged from `6d87edd`)

`scan-manuscript`: `--semantic-authority` is resolved through `_resolve_repo_path` **before** loading (containment enforced, returned repo-relative path used). A persisted review record (`dict` with `review_kind == SEMANTIC_EDITORIAL`) is passed as `semantic_review_path=<repo-relative>` through the strict loader; no authority dict/PASS/reviewer is synthesized. Other JSON objects take the authority-object branch unchanged. `--semantic-review` remains a separate findings argument. CLI help for `--semantic-authority` corrected. Invalid input fails nonzero via existing paths.

Diff: `increment-gate-cli.patch` (sha256 `29b7f187…b726`, 34507 bytes). Changed files (disk copies verified against committed blobs):
- `scripts/survey_reader_surface_gate_v2.py` — blob `ea1eb652…`, sha256 `78f136a0…`, 84430 bytes.
- `tests/test_survey_gate_cli_persisted_review_v2.py` — blob `c839a2fe…`, sha256 `1bf1451f…`, 30300 bytes.

## 3. Test evidence

Committed final run: `logs/candidate-relevant-tests-e4c8269.log` (sha256 `20831ed9…`), exit **0**, **32 test methods, 32 ok, 65.075 s**; modules `tests.test_survey_reader_surface_gate_v2` (27 unchanged) + `tests.test_survey_gate_cli_persisted_review_v2` (5 dedicated). Command/cwd/runtime/dependency inventory is embedded in the raw log via `importlib.metadata` (no `pip` repeated): CPython 3.12.14 at `/tmp/jgas-rephase-application-venv/bin/python3.12`; jsonschema 4.23.0, pypdf 6.16.2, attrs 26.1.0, rpds-py 2026.6.3, referencing 0.37.0, jsonschema-specifications 2025.9.1, typing-extensions 4.16.0.

The unchanged-runtime 27-method result at `6d87edd` is cited as the antecedent (`attempts/6d87edd/`); the combined 32 was run once at the final single head and not repeated after passing.

## 4. Preserved attempts (including failures)

| Attempt | Outcome |
|---|---|
| Parent-witness first setup control (milestone 1) | Failed: absolute path to `semantic_review_path`; log overwritten, disclosed, not recreated/clean |
| `logs/dev-run-new-module-20260927T1.log` | 4 failures — test-harness assumptions (load_json object-only; diagnostic FAILED report; snapshot filter) |
| `logs/dev-run-new-module-20260927T2.log` | 5/5 pending methods pass (pre-commit draft) |
| `attempts/6d87edd/` | 32 methods OK at `6d87edd`; superseded by these corrections (runtime identical) |
| `logs/dev-run-new-module-20260927T3.log` | 1 failure + 1 error — wrong-target pre-validation used bib path; alt digest assertion used content digest |
| `logs/dev-run-new-module-20260927T4.log` | 5/5 corrected methods pass (pre-commit) |
| `logs/candidate-relevant-tests-e4c8269.log` | Final combined run, 32 methods OK, exit 0 |

## 5. Deferred disposition

- `--semantic-review` transport: `core.load_json` is object-only, so the advertised findings array cannot load; a JSON object is passed through as a mapping. **Deferred** — no fix attempted, no normative acceptance encoded. Probe: `logs/findings-transport-probe-20260927T1/` (`bare-array` exit 1 `expected JSON object`; `object+authority` exit 0; `review-only-via-semantic-review` exit 1 `requires machine-checkable semantic_authority`).
- Negative non-PASS runs write a diagnostic FAILED report (existing `evaluate` behavior); asserted non-admissible, not an authority write.

## 6. Reproduction (warning)

```
wsl -d Ubuntu -- bash /mnt/d/Git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-gate-cli/run-candidate-tests.sh
```
`run-candidate-tests.sh` **overwrites** its fixed-named log/exit and is **not** a safe re-run stability check; any new run must use a new unique attempt name. Use the absolute WSL path; do not rely on a relative current cwd. Recovery: DB at `e4c8269`, or apply `increment-gate-cli.patch` to B `c04f32a` and verify the changed-file sha256.

## 7. Non-claims

No independent review, seven-point audit, whole-profile/Step-4/B3 completion, real accepted-manuscript/publication, or adoption. Awaiting Astra source/oracle/evidence review; no further delegation performed.
