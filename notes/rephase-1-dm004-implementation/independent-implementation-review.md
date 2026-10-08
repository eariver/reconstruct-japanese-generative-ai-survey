# DM-004 independent implementation review — scope fixed 6ffed32 (read-only)

Status: **CHANGES_REQUIRED** (one blocking contract deviation; otherwise bounded evidence holds).
Scope is exactly final candidate **`6ffed32298fdaf87874a643b0f9f9b8f837c0256`**,
tree `c3d6ad6ffdadf2d5780a3cd5109555c87fe394cc`,
parent `22598f1c88f65c2ac08b94203f1e56670113d287`,
chain `6ffed32→22598f1→d80b5ee→3dc4288→e1705b7`
in `/tmp/opencode/jgas-dm004-impl-20261004T234416Z`,
branch `codex/dm004-release-validate-state`. No full audit / adoption / release.

## 1. Independence and method (no code/test/design authorship)

- Did not author code/tests/design; no agents/subagents launched.
- No runtime tests/probes, no network, no checkouts/ref/config/code writes,
  no worktree mutation. All Git reads used scrubbed env
  `GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file`
  with `env -i … git -C <repo> …` (no `GIT_DIR` overrides).
- Read-only sources: `AGENTS.md` Human boundaries (§Human boundaries,
  fixed baseline `774dd39`, read-only reconstruct, isolated-DB/inert-origin,
  Human Commit Point); `notes/rephase-1-dm004-implementation/contract-analysis.md`;
  `notes/rephase-1-dm004-implementation/implementation-task.md` (Astra-selected
  contract); `evidence-20261004T234535Z/` reports/qualification/runtime+test
  source copies (`implementation-report.md`, `evidence-qualification.md`,
  `implementation-manifest.json`, `run_dm004.py`, `gen_manifest_final.py`,
  `dm004-e1705b7-to-6ffed32.patch/.pack`, `restore_dm004.sh`,
  `restore.log`, `restore-verification.log`, `run-00…run-06/` guard-pre/post +
  stdout/stderr/exit); actual fixed candidate Git objects via `rev-parse`,
  `ls-tree`, `diff`, `rev-list`, `show HEAD:<path>`.
- Only write is this NEW review file. No Worker/root/source editing.

## 2. Read-only exact identity / diff verification (actual byte proof)

- `rev-parse HEAD` = `6ffed32…0256`, `HEAD^{tree}` = `c3d6ad6…fe394cc`,
  `HEAD^` = `22598f1…287d`, `status --porcelain` empty, branch
  `codex/dm004-release-validate-state`, origin
  `https://example.invalid/rephase-candidate-recovery.git` inert,
  no `objects/info/alternates`.
- `diff --stat e170..HEAD`: 2 files, `+394/-0`
  (`scripts/survey_agent_control_v2.py 19 +0`,
  `tests/test_survey_dm004_release_validate_state_v2.py 375 +0`).
  Worker “+394/-1” is off by one deletion; actual deletions 0.
  Runtime delta is exactly 19 added CLI lines (3 parser + 16 dispatch);
  no changed lines in runtime file.
- `ls-tree -r HEAD`: controller mode `100644` blob
  `7c6450c2bb39dd80ff0814bd175dd1cee433b63b`;
  new test mode `100644` blob `76e4fe5a27b1fc84416c254624a067d1c7f68801`;
  workflow `.github/workflows/survey-production-v2-release.yml`
  mode `100644` blob `de6531d70453dacf9745dae75564020da104420c` **unchanged**.
  Matches manifest SHA256/bytes
  (`06de5b47…`, 124484 B; `131eb7b0…`, 17876 B) and patch header.
- `rev-list --objects e170..HEAD` count 18, consistent with manifest
  18 objects (4 commits/9 trees/5 blobs). `rev-list --count` = 4.
- Patch equals live `diff e170..HEAD` for controller (verified byte-identical
  hunks); test file is pure addition. No schema/config/workflow/helper edits.

## 3. Contract compliance (source-grounded)

- **Generic API semantics, not RELEASED-only:** PASS. Dispatch calls shared
  public `validate_agent_state(root, cfg, state)` (source-copies
  `survey_agent_control_v2.py:2362-2377`), same validator as DM001/019 and
  W1. New test `test_generic_cli_accepts_valid_frozen_and_released` asserts
  real valid FROZEN exit 0 and real RELEASED/COMPLETE exit 0 with JSON
  `valid:true` + lifecycle/control fields, State bytes unchanged before/after
  (actual `read_bytes` comparison, not print-only). This correctly implements
  task §1.4 correction of proposal “not valid FROZEN” wording.
- **No schema/API weakening:** PASS. No schema, config, `validate_agent_state`,
  checkpoint builder, or existing-oracle edits. Existing 14 affected methods
  retain their mock scope and are labeled regression-only.
- **Exit-2 discriminative invalid/missing/parse:** PARTIAL. Five invalid-State
  subcases (drifted provenance SHA, removed record, pending release on
  RELEASED, malformed JSON, missing file) all exit 2, non-empty stderr,
  no `"valid": true` on stdout; three argparse refusals (typo command,
  missing `--state`, extra `--implementation-sha`) exit 2 with
  `invalid choice` / `--state` / `unrecognized arguments`. However the five
  semantic cases assert only generic non-empty stderr, not per-case
  discriminative substrings (e.g. SHA drift vs provenance-missing). Evidence
  supports fail-close, not full discriminability. Minor; fix by asserting
  distinctive validator phrases.
- **Read-only byte proof:** PASS (bounded). Positive paths compare on-disk
  bytes pre/post CLI; negative loop restores `valid_state`/`valid_checkpoint`/
  `valid_record` snapshot bytes per subcase and re-asserts final bytes +
  `validate_agent_state==[]`. Workflow-closure mutation window (record +
  checkpoint + State) is separately recorded; validation CLI itself claims no
  writes. This is actual-byte comparison, not log-only.
- **Real Frozen→Released acceptance, no mocks:** PASS. Test imports (not copies)
  DM001/019 `SpecialFixture`, builds Candidate→approval→Freeze→FROZEN with real
  validators, then real `build_merge_verification` + `build_release_record`
  (synthetic `RELEASE_REF=synthetic:dm004-offline-no-remote`, actual impl SHA)
  + real `survey_release_checkpoint_v2.py` CLI to RELEASED/COMPLETE with
  `machine_checkpoints.release=passed` + provenance binding + `validate_agent_state==[]`.
  No `mock` import in new file (grep-verifiable). Old 9 checkpoint tests keep
  mocks and are correctly NOT used as acceptance.
- **Workflow LOCAL closure, no live Release:** PASS. `extract_closure_step()`
  extracts exactly the `- name: Build immutable Release Record…` run block from
  saved workflow, asserts required tokens (`build_release_record`,
  checkpoint CLI, `validate-state`, `--state "$STATE"`, merge/record paths)
  and forbids `gh release`, `gh pr create`, `git push/switch/config`,
  `gh api`, `actions/checkout`, `setup-python`. Offline run uses pinned
  interpreter, `PYTHONPATH=.`, `PYTHONDONTWRITEBYTECODE=1`, allow-listed env,
  heredoc `python - <<'PY'` + two CLIs; final State RELEASED/COMPLETE with
  FROZEN-named checkpoint bound and validator clean. No `gh`/network/PR/push.
- **Fail-fast sentinel:** PASS (bounded). `set -euo pipefail` + invalid-JSON
  State + trailing `touch sentinel`; non-zero exit and sentinel absent.
  Uses parse-failure path; a semantic-drift sentinel would prove validator
  path distinctly (suggested hardening, not blocking).
- **Parent defect witness:** PASS. `run-00` at e170 with exact workflow argv
  `validate-state --state …` exits 2 with `invalid choice: 'validate-state'`
  (argparse list without it), not import/missing-file. Pre/post guards OK,
  clean, inert remote. No full-suite rerun, as tasked.
- **Guards in files + first failures:** PASS. `run_dm004.py` (saved, versioned)
  writes literal argv/cwd/runtime/env + expected HEAD/tree/source-hash/clean
  to `guard-pre.json` BEFORE and `guard-post.json` AFTER every run (00–06),
  raw `stdout.log`/`stderr.log`/`exit`, aborts on drift. Verified run-00/05/06
  pre/post `guard_ok:true`, exact HEAD/tree, empty porcelain, pinned 3.12.14.
  `run-01` (2 failures + 2 errors: fixture collision, RELEASED-vs-FROZEN name,
  `sentin` typo) and `run-02` (residual typo) preserved with full tracebacks;
  `run-05` new 6/6 (106 s) + `run-06` affected 14/14 are final oracles at 6ff.
  `run-04` at 22598f1 is runtime-identical superseded affected run (only test
  file changed after); disclosed, not transferred silently.
- **Portable pack + fresh restore:** PASS. Pack `dm004-e1705b7-to-6ffed32.pack`
  43,270 B SHA256 `7e147a60…59c95dd0b4e` (verified by `sha256sum`), 18 objects.
  `restore_dm004.sh` + `restore.log` + `restore-verification.log` saved (not
  manifest-only): 4 hash gates (b40 archive, successor-20, w17, dm004 pack),
  absent-destination, `unpack-objects` in order, actual `update-ref` +
  `symbolic-ref` + `reset --hard` to final, clean, full chain to shallow-774
  (`774dd39…`), both modes/blobs/bytes equal, `controller-equal`/`test-equal`,
  zero shared inodes (impl vs restore dev:ino differ), inert remotes, no
  alternates, no stale-parent acceptance. Missing-26309/runtime-not-bundled
  remain disclosed; no full-suite repeat in restore, as tasked.

## 4. Blocking finding F1 — `validate-state` path lacks required normalize/contain

**Contract:** task §1.1 requires: retain `_path` handling/style AND
“Normalize/contain the State path using existing helpers for consistent
repo-relative reporting; support ordinary absolute in-repo and repo-relative
arguments.” Existing helpers are `core.repo_local_path()` (rejects traversal,
resolves + contains; verified `survey_production_v2.py:222-231`) and controller
`_rel()` (resolve + `relative_to`, else `AgentControlError … must be
repository-local`; source-copies line 82-88).

**Actual code** (patch + source-copies `survey_agent_control_v2.py:2204-2208`,
`2362-2377`):

```python
def _path(root, value):
    path = Path(value)
    return path if path.is_absolute() else root / path
…
state_path = _path(root, args.state)          # no resolve/contain
state = core.load_json(state_path)            # outside bytes loadable
…
"state": str(state_path.relative_to(root))    # lexical only
```

`Path.relative_to()` is lexical, not resolved. Consequences (source-grounded,
no probe executed per instruction):

- Repo-relative `../external/state.json` with `root=/R` gives
  `_path=/R/../external/state.json`. `core.load_json` opens the outside file
  (OS resolves `..`). If those bytes happen to validate, CLI exits 0 and
  `str(_path.relative_to(root))` yields `"../external/state.json"` as if valid
  — containment bypass + inconsistent reporting, contrary to “normalize/contain.”
- Absolute outside `/tmp/external/x.json` does raise `ValueError` at the
  *print* step (caught → exit 2), but only AFTER `load_json` +
  `validate_agent_state` already ran on outside bytes. Fail-close is late and
  reporting is not canonical.
- Sibling commands share the `_path` idiom, but the new contract explicitly
  demanded helpers for this subcommand; following the old idiom alone does not
  satisfy §1.1.

**Required correction (minimal, no new framework):** normalize the CLI State
path through existing helpers before load and report the canonical rel, e.g.

```python
state_path = core.repo_local_path(
    root, _rel(root, _path(root, args.state), "Production State"),
    "Production State")
# then report _rel(root, state_path, "Production State")
```

preserving exit-2 via existing `AgentControlError`/`ValueError` catch and
supporting ordinary absolute-in-repo + repo-relative args while rejecting
`..`/absolute escapes before any State-byte load.

**Source-grounded failing test to add (proposal only, NOT executed):**

```python
def test_validate_state_rejects_repo_relative_escape(self):
    fix = build_to_frozen(self, "ESC")  # real valid FROZEN
    # copy valid State bytes to sibling outside repo (new absent path, cleanup)
    # argv: --repo-root . validate-state --state ../<sibling>/state.json
    # expect: exit 2, stderr matches "must be repository-local|escapes repository",
    #   no '"valid": true' on stdout; on-disk in-repo State unchanged.
```

Current code would exit 0 (lexical `../…` passes `relative_to`), so the test
fails pre-fix and passes post-fix. No actual outside file was created or
executed for this review.

## 5. Non-blocking observations

- **F2 — legacy non-equivalence test strength:** `test_legacy_core_validate_state_is_not_equivalent`
  runs both CLIs on a single dangling skeletal State (both invalid; legacy
  exit 1 vs new exit 2). Differing exit codes on one invalid input does not
  prove validation semantics. The report’s source contrast (legacy
  `verify_state_basis`/`validate_state_semantics` with init-pin/global-contract/
  legacy-attestation vs new `validate_agent_state`; exit 0/1 vs 0/2 style) is
  the stronger proof and should be cited as primary, test as auxiliary only.
- **F3 — reporting accuracy:** `+394/-1` should read `+394/-0`; discriminative
  stderr for the five semantic negatives and a semantic (not only parse)
  fail-fast sentinel would tighten oracles. No code impact.

## 6. Runtime-vs-evidence verdict

- Runtime evidence at fixed 6ff supports: new 6 methods / 10 subcases OK,
  affected 14/14 OK, parent exit-2 witness, offline closure to
  RELEASED/COMPLETE, sentinel suppression, all-4 hash-gated restore.
  Guards, env, argv, exits are in-files per run; first failures and runner/
  manifest script versions retained.
- Code contract fails F1 (explicit normalize/contain requirement). Therefore
  **CHANGES_REQUIRED**, not `BOUNDED_PASS`. No broader acceptance, no adoption,
  whole candidate remains `NOT_READY`; Human Commit Point still gates any
  correction unit (minimal path fix + escape test + rerun + repack/restore +
  fresh independent review).
