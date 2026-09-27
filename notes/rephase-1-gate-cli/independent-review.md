# Independent scoped review — Gate CLI persisted-review admission

- **Reviewer identity:** General, **independent scoped reviewer** (not Sol/Luna/Astra; no model-identity claim). Did not author/design the candidate or run its tests; independent from the author General session and from root's author-side review.
- **Recorded:** `2026-09-27T18:44:55+09:00`.
- **Scope (bounded):** `scan-manuscript` persisted reader-surface review path normalization and strict `semantic_review_path` forwarding; authority-object compatibility and separation from `--semantic-review` findings. Runtime limited to the `scripts/survey_reader_surface_gate_v2.py` CLI; plus the new focused CLI test module. No publisher/schema/other change.
- **Head under review:** successor **`e4c82692abee6acedbba07815b0d74ccefb80a7e`**, tree `bc377b6b7eb1e47dacd719e0f76b5a86703f3f3e`, parent `6d87edd28a1be8893ca2ab67fed6e32e54b0de6c`, total diff from B `c04f32ad46109403e8a63faaa8394a90ee6b869c`.
- **Fixed production baseline (untouched):** `774dd39a951c9ac3818e83dfffd4c7666efb0a20`.

## Verdict

**BOUNDED PASS** for the selected unit (fix correctness, fail-close, removal of the CLI's hardcoded attempted synthesis/defaults, negative-boundary reach, generated-Weekly accepted-chain connection, and evidence integrity), **for the exact head reviewed and synthetic-fixture scope only.**

This is a scoped independent implementation/test review. It is **not** the canonical seven-point audit, not production adoption, not whole-B/step-4/B3/application acceptance, and makes no claim about real Human review, publication, Special/profile closure, build transfer, regeneration, Freeze/Release, or net lifecycle savings. The review is **not** a pristine read-only exercise: during verification the fixture worktree HEAD was moved by `git checkout` between `c04f32a` and `codex/rephase-1-gate-cli` for a patch display check. Exact deviation disclosure is in `integrity-verification-log.md` §Deviations; no ref was created, deleted, or repointed, and HEAD/refs are restored to the reviewed head.

---

## Evidence reviewed (actual bytes, not summaries)

- Committed runtime/test diff B→e4c8269 and 6d87edd→e4c8269 (fixed `git show`/`git diff`).
- Committed runtimes in full: `main()` CLI, `evaluate_reader_surface_gate`, strict loader `load_and_validate_reader_surface_semantic_review`, `_resolve_repo_path`/`_rel`, `_derivation_for_manuscript`, `validate_reader_surface_gate`, `core.repo_local_path`/`load_json`.
- New test module `tests/test_survey_gate_cli_persisted_review_v2.py` (full) and its 6d87edd→e4c8269 correction diff.
- Final raw 32-test log + numeric exit; preserved failed attempts T1/T3 and the antecedent `attempts/6d87edd` archive.
- Raw parent witnesses (subprocess stderr/stdout/exit, controls) and the deferred findings-transport probe.
- Isolation/fingerprint logs; packet-level and blob-level hashes; `candidate.json`.

Details and hashes: `independent-review.md` + `integrity-verification-log.md` (this packet).

## What the runtime change actually is

`git diff c04f32a e4c8269 -- scripts/survey_reader_surface_gate_v2.py` is 31 changed lines confined to `main()` plus a help-string correction:

- `--semantic-authority` is now resolved through the **pre-existing** `_resolve_repo_path(repo_root, args.semantic_authority, "semantic authority record")` (containment enforced; returns a normalized repo-relative string).
- A persisted record with `isinstance(sem_data, dict) and review_kind == "SEMANTIC_EDITORIAL"` sets `sem_review_path = authority_rel` and is forwarded to the **pre-existing** `evaluate_reader_surface_gate(..., semantic_review_path=sem_review_path)`. No authority dict / `decision="PASS"` / reviewer default is synthesized.
- Any other JSON object keeps the unchanged authority-object branch.

The `semantic_review_path` branch of `evaluate_reader_surface_gate` and the strict loader are **unchanged in B** (verified: `semantic_review_path` existed at B lines 1126/1155; only the CLI wiring is new). The candidate therefore reuses an already-existing strict path, not newly invented trust logic.

## Findings

### Defect claim is real (not manufactured)

Raw parent witnesses at B (before fix), genuine CLI subprocess tracebacks:
- `absolute-contained` → exit 1, `ValueError: semantic_authority missing required field: surface_sha256` (old branch read `source.sha256`, but reader-surface reviews carry `reviewed_surface`).
- `repo-relative` → exit 1, `ValueError: '…json' is not in the subpath of '…'` (unnormalized `relative_to`).
- positive controls (strict loader `semantic_review_path`; correctly-built authority object) → **PASSED** at B.
This localizes the defect to the CLI branch and shows the lower layer already worked. Fix addresses exactly this.

### Synthetic-default removal (not a proven old acceptance bypass); fail-close preserved

Correction (evidence clarified after root review): the old CLI review-record branch **attempted** to synthesize an authority dict with hardcoded `decision="PASS"` and `status` defaulted to `PASSED`, but this is **not** a proven acceptance bypass. Inspected evaluator flow (B commit `c04f32a`; runtime blob `927ef11`, lines 1165–1194):

- The synthesized dict is passed as `semantic_authority`, so it takes the **authority-object branch**, which then (a) computes `rev_file` from `semantic_authority["review_path"]` and **re-opens the on-disk review through the strict loader** (`load_and_validate_semantic_review`), (b) re-checks `semantic_authority["review_sha256"]` against `validated_sem["review_sha256"]`, and (c) applies the unresolved-blocking guard before `sem_auth_input = semantic_authority`. The synthesized `decision` alone could not yield a PASSED Gate: the strict loader and digest/blocking checks still ran.
- Furthermore, the old branch read the wrong field (`source.sha256` instead of `reviewed_surface.sha256`) and applied an unnormalized `relative_to`, so canonical persisted records actually **failed** (parent witnesses: `surface_sha256` missing → exit 1; repo-relative → `not in the subpath` → exit 1). The observed outcome was **rejection**, not acceptance.
- Therefore the defensible statement is: the old CLI branch contained **hardcoded attempted synthesis / unsafe defaults**; the reviewer found **no inspected-path proof that a canonical persisted review was ever accepted as PASS through this branch**. I retract the earlier wording "force-promoted to PASS authority" / "real bypass".
- What the fix changes is nonetheless real and correct: the review-record branch no longer synthesizes an authority dict at all; it forwards the record through the **existing `semantic_review_path` strict path** (schema, `review_kind`, digest, `reviewed_surface` disk-bytes, `READER_PIPELINE_INDEPENDENCE`, non-empty evidence, identity), and the CLI now normalizes the path so canonical records reach that loader instead of failing. `isinstance`/`_resolve_repo_path` also remove the unguarded `.get` and the unnormalized `relative_to`.
- In the new branch `sem_auth_input = validated_sem`, so `sem_status`/`sem_decision`/`sem_surface_sha` derive from validated fields; `authority_clean` and the `RSG-SEM-AUTHORITY-FAILED` / `RSG-SEM-SURFACE-SHA-MISMATCH` blocking findings continue to apply. A non-PASS review yields a `FAILED` diagnostic and cannot validate.
- `--semantic-review` is still loaded independently into `semantic_review_findings`; supplying a review record **only** there (no `--semantic-authority`) raises `requires machine-checkable semantic_authority` (asserted). Findings transport cannot substitute authority.
- Non-`dict` payloads cannot reach the CLI branch/`evaluate` at all: `core.load_json` (line 78–82) raises `expected JSON object: <path>` on any non-object before returning, so `sem_data`/`sem_findings` are always dicts (or an exception). The `isinstance(sem_data, dict)` guard is therefore **redundant under the current loader**, not a demonstrated new defense; it is defensive-only. (The deferred array-transport probe's `expected JSON object` error is this loader behavior.)
- `scan-manuscript` has no try/except, so failures propagate → nonzero exit (same as B); negative cases cannot produce a PASSED Gate (diagnostic FAILED report write is pre-existing and non-admissible).

### Negative oracles reach intended boundaries

- path-escape and outside-symlink → `escapes repository root` from `_resolve_repo_path` (symlink is resolved, so real containment, not string-only).
- digest-broken → `digest mismatch`; malformed/legacy-shaped → strict-loader schema message; pass-with-unresolved-blocking → `unresolved blocking`.
- **wrong-target** is first **positively** validated by the strict loader (schema+digest+bound surface), then the CLI failure is asserted to hit the route/target boundary (`Weekly complete reader input` via `weekly.validate_reader_input`), not merely nonzero — a genuinely stronger oracle than the antecedent.
- **unrelated same-issue manuscript**: a second genuinely validator-valid manifest is built by changing only schema-permitted `authored_by`/`recorded_at` + recomputed `manifest_sha256` (matches `validate_manuscript_manifest` base definition; primary/support equal), and the exact-binding failure message contains the alt path + alt sha256.
- stale surface bytes and non-PASS/error mutations leave the **limited watched files** unchanged (the direct-primary negative test snapshots an explicit watchlist plus `root/sources/2026-W35/production-state.json`). This is a **limited-watchlist** oracle, not a whole-upstream-tree guarantee; it does not prove absence of writes to files outside the watchlist. Whole-tree positive no-write evidence exists only for the generated-Weekly test (below).

### Generated-Weekly accepted-chain + CLI + independent readback is real

- The fixture reuses B's accepted publisher chain with patches **only** on fixture constructors (`sandbox`, `init_profile` using the real `weekly_profile`+`initialize`, `architecture_for` adding publication extensions to the real plan, `IMPLEMENTATION_SHA` constants bound to the real head) — no validator, receipt-replay, or Git-success stub (grep-confirmed; mocked objects are `sys.argv` only, for in-process publisher `main()`).
- The real CLI subprocess emits the Gate; `surface_gate.validate_reader_surface_gate(..., expected_manuscript_path=manuscript_path, state_path=state_path)` independently validates it and returns `route == weekly.ROUTE`; `weekly.validate_receipt` re-validates the receipt. Whole-tree no-upstream-write snapshot (all regular files except `.git`) asserts only the declared Gate is added and no existing file changes.

### Evidence integrity (exact head, counts)

- Committed blobs, disk copies, patch bytes/sha256, log sha256/exit all MATCH `candidate.json`; `setup/16` re-verifies copies via `git hash-object` and prints `FINAL_ARTIFACTS_OK`.
- Final raw log binds HEAD/TREE/PARENT = e4c8269/bc377b6/6d87edd at run time, `Ran 32 tests … OK`, numeric exit 0, 32 OK = 27 + 5, 16 subTest blocks / 18 subcases, no skips. Trailing JSON is test stdout, not failure.
- Runtime identical between 6d87edd and e4c8269 (blob `ea1eb652…`); the 6d87edd→e4c8269 change is test-only.
- Isolation genuine: independent byte copy, `NO_ALTERNATES`, no `GIT_*` overrides, no symlinks/hardlinks, empty cross-DB inode intersection, inert origin, shallow boundary pinned to the fixed baseline. Promisor missing-blob fsck output is inherited, not a copy defect.

## Blocking issues

**None** for the bounded scope. No fail-close hole (the old branch's hardcoded attempted synthesis still passed through the strict loader on the referenced record), no missing intended boundary, no fabricated success path, and no evidence-integrity failure was found within the selected scope.

## Non-blocking observations / limitations (for the record, not scope expansion)

1. **Antecedent weak oracle is acknowledged and fixed** — the 6d87edd tests used an invalid `alternate.tex` manifest, an array-authority "expected failure", and an invalid legacy fixture; e4c8269 replaces these with validator-valid constructions and route-boundary assertions. Runtime was identical throughout, so the earlier PASS did not cover the corrected oracles; the current PASS does.
2. **Inherited `--semantic-review` findings-array defect is out of scope and only observed.** `core.load_json` is object-only, so the advertised array transport fails (`expected JSON object`); the candidate does not fix or normatively encode this. Probe `logs/findings-transport-probe-20260927T1/` is explicitly labelled observational/deferred. No acceptance is implied.
3. **`run-candidate-tests.sh` claims `EXPECTED=e4c8269` but only warns** (`FIXTURE HEAD CHANGED`) instead of aborting if HEAD differs; it also overwrites its fixed log/exit. In the reviewed run HEAD matched, but a future re-run under a changed head could still emit exit 0 from the wrong tree. Nonblocking for this frozen artifact; worth tightening if the script is reused.
4. **Parent setup raw log loss acknowledged** — the first parent-witness setup control was overwritten and not recreated (disclosed in `inventory.md`); the first strict-loader positive control's initial absolute-path failure has no retained raw log. Later raw witnesses/controls are intact and sufficient for the conclusions drawn.
5. **Synthetic-only.** All manifests/reviews/authorities are labelled synthetic; this proves type/identity/route mechanics and the strict loader, never real visual judgment, Human Gate, publication, or adoption.
6. **Trailing JSON in the test log** is fixture stdout, not a second parse; noted only so it is not misread as an unexplained artifact.
7. **No claim** about whole-B, B3, step-4, application, Special/other profiles, build transfer, Weekly regeneration, Freeze/Release, or net savings. A changed head/merge/base would invalidate this PASS.

## Method and actions actually taken (deviation disclosed)

Not pristine read-only. Actions performed:

- Read-only throughout: fixed `git show`/`git diff`/`git rev-parse`, `git for-each-ref`, hash/blob comparison, packet/log reads, `git apply --check --stat` (display-only).
- **Deviation:** I ran `git checkout` twice in the fixture DB to place the worktree at `c04f32a` for the patch display check, then checked `codex/rephase-1-gate-cli` back. This **moved the worktree/HEAD** (detached at `c04f32a`, then re-attached). No ref was created, deleted, or repointed; no commit/object was created by me; no test was run. Exact commands, reflog, refs, and outputs are in `integrity-verification-log.md` §Deviations.
- The `git apply --check --stat` invocation **never applied the patch** (`--stat` "turns off apply"); it produced only a diffstat. It is therefore **not** an independent clean-baseline application proof; the scoped review relies on the exact blob/sha256 diff verification (which is sufficient for this unit).
- **No tests executed. No code changed. No commits created. No network, no production/current-main/Actions access, no agents spawned.** Only files written were this review and its integrity log in the reconstruct packet.
- No author approval or Worker PASS was assumed; conclusions rest on inspected bytes. The fixture DB currently reports HEAD/refs restored to the reviewed head with only untracked `__pycache__/` (root may independently inspect identity/status/reflog read-only).
