# DM022 R2 integration diagnostics — NEW executor (no source edits)

Date: 2026-10-28 UTC. Role: NEW integration test executor. No source edits performed; root coordinates corrections.

## 1. Fixed source (ONLY tested source)

- Snapshot: `.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/snapshot-r2-20261028T124706Z/worktree`
- Manifest: `notes/rephase-1-dm022-prearchitecture-implementation/evidence/source-r2-20261028T124706Z/snapshot-r2-manifest.json`
- Manifest SHA256: `53fde56bea8b69adeb2cdfbbd716bbe9534bfb0bc49739619f909ae6ca1f3935` / 149982B / 756 entries (`{kind,sha256,bytes,mode}`)
- Snapshot git-independent: `snapshot-r2-.../git-independent/.git` — 83 files, HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, origin `https://example.invalid/rephase-candidate-recovery.git` (inert), no `alternates`, no `commondir`
- Verification before exec: snapshot worktree 756 files, snapshot git 83 files; manifest file SHA matches above.
- Policy: snapshot IMMUTABLE. No edits/clean/re-copy/delete. Live `candidate-work` (C2 editing) NOT mutated, NOT tested.

## 2. NEW independent execution copy (ignored parent, byte-copied .git)

- Parent (ignored via `/.rephase-1-editorial-runtime/`): `.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/`
- Exec: `.../exec-r2-integration-20261028T125129Z/` (NEW, unique stamp)
  - Worktree: `tar --exclude=.git --hard-dereference -cf - -C SNAP/worktree . | tar -xf - -C EXEC` → 756 files
  - Git: `cp -a SNAP/git-independent/.git EXEC/.git` (byte copy, no `--link`) → 83 files
  - HEAD: `409b292756dd1277b9dfae87679934c0d2ce251c` (matches snapshot)
  - Independence: SNAP_GIT 83 vs EXEC_GIT 83, `(dev,ino)` OVERLAP 0; 0 symlinks in exec worktree; no `alternates`/`commondir`; origin inert `example.invalid` preserved
  - Manifest check on exec: 756/756 paths, 0 only-either-side, 0 SHA/bytes/mode/kind mismatches, 0 symlinks (pre-run and FINAL post-suite recheck `mism=0 total=756`)
  - No `.git` in packet: exec `.git` stays under ignored parent; packet `notes/.../evidence/integration-r2-.../` contains only raw logs/headers, no Git DB
  - No ordinary commit/push; no `git clean/reset/fixture-deletion`; no network; no Production; no Gitconfig mutation (global `user.name/email` untouched); no root Human HEAD/status read (no git commands in workspace root; HEAD/config read as plain files only for binding)
  - Git overrides: `env | grep ^GIT_` → `NO_GIT_ENV_OVERRIDES` before each run; per-run `unset GIT_DIR GIT_WORK_TREE GIT_COMMON_DIR GIT_INDEX_FILE GIT_OBJECT_DIRECTORY GIT_ALTERNATE_OBJECT_DIRECTORIES` verified/logged in header
  - Fixture identity: test subprocesses use process-scoped `GIT_AUTHOR_NAME=dm022-test-fixture`, `GIT_AUTHOR_EMAIL=fixture@example.invalid`, `GIT_COMMITTER_*` (process env only); meaningful synthetic fixture commits belong to independent fixture DBs only (tests create isolated temp trees + independent Git DBs)
  - Cache: `PYTHONDONTWRITEBYTECODE=1` on all runs; PRE/POST `__pycache__/*.pyc` count 0 on every run; POST suite exec still 756 files, 0 pycache
  - Snapshot/candidate untouched proof (post-suite): SNAP worktree 756, SNAP git 83, EXEC 756/0 pycache, CAND 756, manifest SHA still `53fde56...`

## 3. Runtime pin (unittest, NOT pytest)

- `/usr/bin/python3` → `Python 3.14.4`
- `jsonschema 4.23.0` (via `importlib.metadata.version`), `pypdf 6.16.2` — matches coordination requirement `jsonschema==4.23.0`, `pypdf==6.16.2`
- `python3 -m unittest --help` OK; `python3 -m pytest` → `No module named pytest` (absence is not blocker per coordination)
- DeprecationWarning only: `scripts/survey_schema_v2.py:38: Accessing jsonschema.__version__ is deprecated` — does not fail tests; version is queried via `importlib.metadata` in header

## 4. Execution method (raw-first, unique dir per run)

- Base evidence: `notes/rephase-1-dm022-prearchitecture-implementation/evidence/integration-r2-20261028T125129Z/`
- Per run: `run-XX-<scope>/` with `header.txt` (command/environment/sourcepin + PRE/POST count/pycache), `stdout-stderr-raw.txt` (combined raw, full tracebacks), `exit-code.txt` (numeric exit)
- Command form (restricted explicit filenames, discovery): `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -m unittest discover -s tests -p "<exact-filename>" -v` with `cwd=EXEC`
- All 8 filenames verified actual in snapshot worktree before run (all FOUND)
- Timeout: 600s per `bash` call; no timeout occurred → no partial-raw timeout path exercised; explicit rule observed: timeout would NOT be claimed as PASS (no timeout→PASS forbidden)
- No old runners executed; no saved-runner reuse; no broad-suite burn after scoped failures (stopped at 5 NEW + 3 legacy as instructed; did NOT run full 236-file suite)
- Systemic import/setup failure did NOT occur (all 8 files collected: Ran 5/12/5/5/10/5/2/2) → proceeded through full scoped list per instruction

## 5. Actual results (ran/skipped/failures)

| Run | Test file | Ran | OK | FAIL | ERROR | Skipped | Exit | Raw SHA256 (stdout-stderr-raw.txt) |
|-----|-----------|-----|----|------|-------|---------|------|-------------------------------------|
| 01-A-acceptance | `test_dm022_prearchitecture_acceptance_v2.py` | 5 | 5 | 0 | 0 | 0 | 0 | `184a3f086b42414709d43c9c9cc6e854e5faaa7b6fc07c975a05d870fa685305` (10 lines) |
| 02-B-ordinary-consumers | `test_dm022_prearch_b_ordinary_consumers_v2.py` | 12 | 11 | 1 | 0 | 0 | 1 | `e17c8e66bc95a5602314eea366f44f0fca2a8f96c981c17c68689f740c462cea` (30 lines) |
| 03-C1-family-closure | `test_dm022_c1_family_closure_v2.py` | 5 | 3 | 0 | 2 | 0 | 1 | `23d121929112648182e44ebe22982d9e434d07cab14bb0059be0cc3d7b23f720` (37 lines) |
| 04-C1-research-graph | `test_dm022_c1_research_graph_v2.py` | 5 | 4 | 0 | 1 | 0 | 1 | `1f357fda869357d4ddb755b26f957a59f3172557e0a34e3a059063412ae47541` (23 lines) |
| 05-C2-consumers | `test_survey_dm022_c2_consumers_v2.py` | 10 | 9 | 0 | 1 | 0 | 1 | `e42303d74ab2e3eb1a400a450b84ca6373b4ba1b5458d2c96bb7c34ffaab0752` (36 lines) |
| 06-legacy-agent-control | `test_survey_agent_control_v2.py` | 5 | 5 | 0 | 0 | 0 | 0 | `60aa8597bef5c91d67ff9ff9c2dbc56a67bef89b5e8fa4f8eee4d2a76533a914` (10 lines) |
| 07-legacy-evidence-views | `test_survey_active_evidence_views_v2.py` | 2 | 2 | 0 | 0 | 0 | 0 | `77eb8059710a5e23d7a23b85992f1ff869478fc0d6554e022d0b6ca73581f8d5` (7 lines) |
| 08-legacy-selection-arch | `test_run_selection_architecture_v2_interactive.py` | 2 | 2 | 0 | 0 | 0 | 0 | `45bcbe7ff39b3a49c576535695ccdde5d98ecfa9f79aec1b5c982643f280e539` (7 lines) |

- NEW total: 37 ran, 32 pass, 1 FAIL + 4 ERROR = 5 blockers; 0 skipped
- Legacy total: 9 ran, 9 pass, 0 failures; 0 skipped
- Later seams NOT proved by earlier fails: each run is independent exec state (POST_COUNT 756 each); B/C1/C2 failures do not certify or invalidate downstream lifecycle seams; no whole-acceptance inference

## 6. First integration compatibility blockers (source-bound, NO fix applied)

### B-01 — `test_10_core_proof_branch_accepts_prearch_rejects_mixed` FAIL (run-02, exit 1)
- File: `tests/test_dm022_prearch_b_ordinary_consumers_v2.py:196`
- Expected: `assertRaisesRegex(agent.AgentControlError, "must not carry CORE_STAGE_CONTRACT")`
- Actual: `scripts.survey_agent_control_v2.AgentControlError: PREARCH record requires exactly one DM022_SUPERSESSION_PROOF review`
- Full traceback in raw `e17c8e66...` (30 lines). Other 11/12 B tests ok including discriminator, from/to-state, producer boundary, full-schema, wrong-family, forward-fields/lineage, triplet same/split, seven-slots, seven-preflight, legacy discriminators, drafting pure. Points to B/A contract mismatch on mixed CORE proof branch error identity; root to adjudicate expected error string vs producer behavior.

### C1-01 — `test_known_schema_owned_fingerprint` ERROR (run-03, exit 1)
- File: `tests/test_dm022_c1_family_closure_v2.py:133` → `scripts/survey_versioned_renewal_history_v2.py:491 _require_owned_schema_fingerprint` → `:501 _require_known_schema_sha`
- Error: `RenewalHistoryError: UNSUPPORTED_MIGRATION: c1-owned-fingerprint unknown foreign schema SHA for registered path schemas/dm022-revision-proof-v2.schema.json (not old/new known, no broad migration)`
- 3/5 pass in file (`literal_membership_plus_actual_files`, `own_epoch_fixture_public_verifier`, `staged_literal_plus_ast` ok). Points to owned-schema fingerprint allowlist missing live R2 schema SHA; no broad migration permitted by design.

### C1-02 — `test_weekly_longform_canon_literal_plus_files` ERROR (run-03, same run)
- File: `tests/test_dm022_c1_family_closure_v2.py:108` → `scripts/survey_weekly_derivation_v2.py:791 _verify_actual_import_closure`
- Error: `ValueError: Weekly actual import beyond R4/R5 literal requires expansion: ['scripts/survey_agent_control_v2.py', 'scripts/survey_agent_tool_v2.py', 'scripts/survey_drafting_v2.py', 'scripts/survey_evidence_v2.py', 'scripts/survey_production_v2.py', 'scripts/survey_schema_v2.py']`
- Points to R4/R5 literal membership narrower than actual Weekly imports; requires explicit expansion decision, not silent literal widening.

### C1-03 — `test_legacy_file_still_accepted` ERROR (run-04, exit 1)
- File: `tests/test_dm022_c1_research_graph_v2.py:88` → `scripts/survey_versioned_renewal_history_v2.py:1293 _record_kind`
- Error: `RenewalHistoryError: HISTORY_DIGEST_MISMATCH: record kind/reason pair unrecognized (no caller kind inference)`
- 4/5 pass in file (`g71_g76_control_literal`, `low_typed_loader_on_real_file`, `own_epoch_fixture_public_verifier`, `prearch_file_public_discriminators` ok). Points to legacy kind/reason pair not recognized without caller inference; root to decide legitimate legacy acceptance vs strict digest rule.

### C2-01 — `test_weekly_refresh_validation_prearch_refuses_whole_path` ERROR (run-05, exit 1)
- File: `tests/test_survey_dm022_c2_consumers_v2.py:165` → `wmod._dm022_refuse_prearch_refresh(prearch, "refresh validation checkpoint")`
- Error: `AttributeError: module 'scripts.survey_weekly_mechanical_refresh_v2' has no attribute '_dm022_refuse_prearch_refresh'`
- 9/10 pass in file (all other whole-path PREARCH refusal/healthy controls ok). Points to missing C2 helper on Weekly refresh module; test expects helper that source does not provide.

## 7. Source-bound results (no whole-acceptance claim)

- A end-to-end (LOW+HIGH, both routes, real chain fixtures, independent Git DBs, real validators/digests, real prepare/adopt/resume/readback, guard/State/slot/completion IO): 5/5 PASS in 3.391s — bounded A-scope only, NOT whole acceptance.
- B ordinary consumers: 11/12 PASS; single FAIL above blocks B integration sign-off.
- C1 family closure: 3/5 PASS; 2 ERRORs above block closure membership/fingerprint sign-off.
- C1 research graph: 4/5 PASS; 1 ERROR above blocks legacy/research-history compatibility sign-off.
- C2 consumers: 9/10 PASS; 1 ERROR above blocks Weekly-refresh checkpoint integration sign-off.
- Legacy controls: 9/9 PASS (agent-control 5, evidence-views 2, selection-arch 2) — affected regressions show no regression on those three files at R2 pins; NOT proof of full-suite health.
- No skipped tests; all 8 files actually collected (unittest `Ran N` present in each raw).
- Exec source invariant held throughout (PRE/POST 756, 0 pycache, FINAL manifest `mism=0`); failures are functional contract mismatches, NOT import/setup/systemic failures, NOT source drift.

## 8. Compliance and handoff

- No source edits to green; no code/test/fixture edits in snapshot, exec, or candidate.
- No old runners, no `git clean/reset`, no fixture deletion, no network, no Production/Gitconfig/ordinary commit-push, no root Human HEAD/status.
- Raw durably saved BEFORE this summary; each run dir has header + raw + exit code (SHAs in §5 table).
- Whole NOT_READY/DM021+022 OPEN preserved; R2 remains rejected pending review per `source-r2-preservation.md` §4 (HIGH O_EXCL/replace race, LOW broad closure, completion-checker weakness remain separate from these 5 test blockers).
- Return to root: coordinate corrections for B-01, C1-01, C1-02, C1-03, C2-01. Do NOT auto-start implementation. Stop at Human Commit Point.
