# DM022 A4 integration diagnostics — NEW executor (no source edits, no patch)

Date: 2026-10-28 UTC. Role: NEW integration test executor. Human continued, root whole unit ongoing. A4/B/C1/C2 all returned STOPPED, candidate idle. No source edits by executor until root assigns; no Human Commit readback; no ordinary commits. Current-code author reports are NOT authority — ONLY frozen-exec actuals below count. Fake fixes (if any) are reports, not proof.

## 1. Fixed source (ONLY tested source)

- Snapshot: `.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/snapshot-a4-20261028T160708Z/worktree`
- Manifest: `notes/rephase-1-dm022-prearchitecture-implementation/evidence/source-a4-20261028T160708Z/snapshot-a4-manifest.json`
- Manifest SHA256: `2eb615b41307e86cc86770c9798bf4ba559e2626f6884e898f3672a2cdc86621` / 149855B / 756 entries
- Snapshot git: `snapshot-a4-.../git-independent/.git` — 83 files, HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, origin `https://example.invalid/rephase-candidate-recovery.git` (inert), no `alternates`/`commondir`
- Preservation: `evidence/source-a4-20261028T160708Z/source-a4-preservation.md` (copy check pre/post, 0 mismatches, 0 overlap)
- Snapshot IMMUTABLE. Live `candidate-work` NOT mutated, NOT tested. Proof-copy/A4 `/tmp` private copy NOT executed (binding read only). Old R2 exec/logs NOT reused.

## 2. Independent exec copy (ignored parent, byte-copied 409 DB)

- Parent (ignored via `/.rephase-1-editorial-runtime/`): `.../dm022-prearchitecture-implementation-20261028T113126Z/`
- Exec: `.../exec-a4-integration-20261028T160708Z/` (NEW stamp)
  - Worktree: `tar --exclude=.git --hard-dereference` 756 files; Git: `cp -a SNAP/git-independent/.git EXEC/.git` (no `--link`) 83 files
  - HEAD matches `409b292...`; SNAP_GIT 83 vs EXEC_GIT 83 OVERLAP 0; 0 symlinks; no alternates/commondir; origin inert
  - Manifest check on exec: 756/756 match, 0 mismatches (pre-run and FINAL post-suite `EXEC_COUNT 756`, `EXEC_PYCACHE 0`)
  - No `.git` in packet; packet `evidence/integration-a4-.../` holds only headers/raw/exit codes
  - Git env: `NO_GIT_ENV_OVERRIDES` before each run; per-run `unset GIT_*`; process-scoped `GIT_AUTHOR/COMMITTER=dm022-test-fixture/example.invalid` only; no global config mutation; no `git clean/reset`; no network; no Production
  - Cache: `PYTHONDONTWRITEBYTECODE=1` all runs; PRE/POST pycache 0 throughout
  - Fixtures: tests create independent temp Git DBs (tempfile, inert origin, process identity); no fixture objects in reconstruct; no fixture deletion

## 3. Runtime pin (unittest, no pytest dep)

- `/usr/bin/python3` → `Python 3.14.4`; `jsonschema 4.23.0`, `pypdf 6.16.2` (via `importlib.metadata`)
- `python3 -m unittest --help` OK; pytest not used (bare-function legacy tests invoked explicitly via unittest where selected; no pytest dependency)
- TinyTeX available outside PATH at `/home/eariver/.TinyTeX/bin/x86_64-linux/` (lualatex/biber/latexmk) — availability only, no install, no PDF build in this task
- DeprecationWarning only: `survey_schema_v2.py:38 jsonschema.__version__` — does not fail; headers use `importlib.metadata`

## 4. Execution method (raw-first, unique dir per run)

- Base: `notes/rephase-1-dm022-prearchitecture-implementation/evidence/integration-a4-20261028T160708Z/`
- Per run `run-XX-<scope>/` with `header.txt` (command/cwd/python/sourcepin/HEAD/origin/GIT env/PRE-POST counts), `stdout-stderr-raw.txt` (combined raw, full tracebacks), `exit-code.txt` (numeric)
- Command: `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -m unittest discover -s tests -p "<exact-file>" -v`, `cwd=EXEC`
- Timeout 600-900s per file; no timeout occurred → no partial-raw timeout path; explicit rule: timeout never claimed as PASS
- No old runners; no saved-runner reuse; no broad full-suite burn (17 runs total: 5 NEW + 3 legacy + 9 scoped regressions); no auto-skipping (0 skipped everywhere collected)
- Systemic import/setup failure did NOT occur in first batch (all 8 files collected) → proceeded to scoped regressions per instruction; systemic per-module failures below stopped further broadening to P1/P2R/P2V/P3S/renewal (left unrun, NOT claimed)

## 5. Actual results (collection actuals, not assumed)

| Run | Test file | Ran | OK | FAIL | ERROR | Skipped | Exit | Raw SHA |
|-----|-----------|-----|----|------|-------|---------|------|---------|
| 01-A | `test_dm022_prearchitecture_acceptance_v2.py` | 19 | 19 | 0 | 0 | 0 | 0 | `4d2e0d6008c26d3e675339d4d863bffbc8b4eb689da2fa632057792e8d165aa5` (37 lines) |
| 02-B | `test_dm022_prearch_b_ordinary_consumers_v2.py` | 15 | 15 | 0 | 0 | 0 | 0 | `6841d6d8fed2bf9a5b905f30ff77a672b80b31e3d20bb785fba4e7bdd8c1a27a` (31 lines) |
| 03-C1-family | `test_dm022_c1_family_closure_v2.py` | 6 | 6 | 0 | 0 | 0 | 0 | `c888b7dca746a72f42afe0db57959b5050d050043058c6d490a64c82c9102bfc` (15 lines) |
| 04-C1-graph | `test_dm022_c1_research_graph_v2.py` | 5 | 5 | 0 | 0 | 0 | 0 | `1c3fc256d1084dea502b5b4d9ffceca1042e9338e85dfaafe855f42d95bcc09d` (12 lines) |
| 05-C2 | `test_survey_dm022_c2_consumers_v2.py` | 16 | 14 | 1 | 1 | 0 | 1 | `9e56f8c6d613520f6f7c7ada65217d3446cd7a9ff9ccdd09bb1a05ce9c6ac241` (67 lines) |
| 06-leg-agent | `test_survey_agent_control_v2.py` | 5 | 5 | 0 | 0 | 0 | 0 | `15ef4f004c8463ee93849341979143c88beb243ee1f5fffd717f21786e98d942` (10) |
| 07-leg-views | `test_survey_active_evidence_views_v2.py` | 2 | 2 | 0 | 0 | 0 | 0 | `77eb8059710a5e23d7a23b85992f1ff869478fc0d6554e022d0b6ca73581f8d5` (7) |
| 08-leg-sel | `test_run_selection_architecture_v2_interactive.py` | 2 | 2 | 0 | 0 | 0 | 0 | `a1c69cd35e07cb905d73952ed2ca73fddc0b88346d5d67e7244b78e82c120c50` (7) |
| 09-evidence | `test_survey_evidence_v2.py` | 12 | 12 | 0 | 0 | 0 | 0 | `3ce4ebb5871a0c3f4042f8ce24fd77daf692f6ef077fd62624f55ec8ae9b9938` |
| 10-completeness | `test_survey_completeness_v2.py` | 2 | 2 | 0 | 0 | 0 | 0 | `e93e5c0649968c9543794b828e3635674540f5f73585c4807db3ea05d1e63c5c` |
| 11-screening | `test_survey_screening_v2.py` | 7 | 7 | 0 | 0 | 0 | 0 | `161fda21c934ed133f05afcc517f85c89f9573adb155b08b7b10a64cbca3aae3` |
| 12-drafting | `test_survey_drafting_v2.py` | 5 | 5 | 0 | 0 | 0 | 0 | `a421789efe9ead7381251dae8b521e72f1473e49c0652eeff6ffdab86c72e75a` |
| 13-histJSON | `test_survey_drafting_historical_json_binding_v2.py` | 6 | 6 | 0 | 0 | 0 | 0 | `1e322121120e3c6cf3350ec90f0d0d8c387db991acd12612310e889d7ebf1ed8` |
| 14-readerGate | `test_survey_reader_surface_gate_v2.py` | 27 | 7 | 5 | 15 | 0 | 1 | `dde48a740831304cdda5209d41df138828c16b65f4fca235111f8e615f8042a6` (623 lines) |
| 15-pubset | `test_survey_publication_set_v2.py` | 18 | 18 | 0 | 0 | 0 | 0 | `53ee31e2f321335806d628c6a41a88511aa9b14b3c68d0fc7efb1041f0a6e36f` |
| 16-pub | `test_survey_publication_v2.py` | 8 | 1 | 2 | 5 | 0 | 1 | `ab79f7ac4f2d9965c525b587c0078362a0d22cf1d0542a70a41c1f944a29cbbd` (238 lines) |
| 17-release | `test_survey_release_checkpoint_v2.py` | 9 | 8 | 0 | 1 | 0 | 1 | `bbd6acadb7783885ca8dde5e3e1a1512ced4ec3410bbededc2ddbd4df88e9bdb` (96 lines) |

- NEW total: 61 ran (19+15+6+5+16), 59 pass, 1 FAIL + 1 ERROR (both C2)
- Legacy 3: 9 ran, 9 pass
- Scoped regressions: 9 files, 89 ran (12+2+7+5+6+27+18+8+9), 60 pass, 7 FAIL + 22 ERROR (readerGate 20, pub 7, release 1)
- Grand collected: 159 ran, 128 pass, 8 FAIL + 23 ERROR, 0 skipped
- Later lifecycle seams NOT proved by earlier passes; no whole-acceptance inference

## 6. First failures mapped to owners (NO patch by executor)

### C2-01 [C2 + A] — `test_weekly_refresh_validation_healthy_legacy_accepts_whole_path` ERROR (run-05)
- `tests/test_survey_dm022_c2_consumers_v2.py:225` → `scripts/survey_weekly_mechanical_refresh_v2.py:674 validate_refresh_validation_checkpoint` → `scripts/survey_research_authority_v2.py:300 load_typed_checkpoint_record`
- `AttributeError: 'str' object has no attribute 'is_absolute'` — `target = path if path.is_absolute() else ...`
- Root: A4 LOW signature `def load_typed_checkpoint_record(repo_root: Path, path: Path)` assumes `Path`, but C2 callers pass `_ref["path"]` (str from JSON). Same call site pattern in `survey_release_checkpoint_v2.py:77`. Owner: **A** (coerce `Path(path)` or accept `Path|str`; audit all LOW public path params) + **C2** (pass `Path` or confirm contract). Blocks healthy-legacy refresh path; PREARCH refusal path in same validator passed (other 14/16).

### C2-02 [C2] — `test_finalize_entry_refuses_with_guard` FAIL (run-05)
- `tests/...:323` expects `DM022_TRANSITION_ACTIVE|NO_PREPARE|STATE|PROFILE`, got `MISSING_ANCESTOR: [PIN/REFUSED_PRE_WRITE] proposal missing ancestor: /tmp/dm022-c2-fin-.../proposal`
- Writer entry gate fires `MISSING_ANCESTOR` before READY guard check in `survey_editorial_publication_v2.py:311 _safe`. Owner: **C2** (order entry guards: READY/guard check before ancestor pin, or test fixture must plant ancestor; do NOT weaken to pass). Real guard-held refusal not yet proved for finalize.

### REG-01 [A + C2] — `test_survey_reader_surface_gate_v2` 20/27 fail (run-14, `dde48a74...` 623 lines)
- Dominant ERROR: `ResearchAuthorityError: production state lstat failed: /tmp/.../sources/2026-W35|SP002/production-state.json: errno=2` via `survey_reader_publication_v2.py:606 build_manuscript_manifest` → `:56 _dm022_require_ready_for_manuscript` → `LOW require_research_operation_ready:2542 _safe_read_bytes`
- Legacy readerGate fixtures (no DM022 state) now hit C2 writer READY entry on `build_manuscript_manifest`. Owner: **C2** (writer gating vs legacy diagnostic compatibility; confirm whether legacy tests must plant DM022 READY or writers must exempt legacy paths — root decision, no silent bypass) + **A** (READY path assumes DM022 layout; legacy fallback must stay refused, not crash with lstat — already fail-closed, but error identity blocks legacy suite).
- 5 FAILs are leakage fixtures expecting `Pre-Publication Reader-Surface Gate FAILED` but getting `production state lstat failed` — same gate-ordering cause.

### REG-02 [A + C2] — `test_survey_publication_v2` 7/8 fail (run-16, `ab79f7ac...`)
- Same `production state lstat failed: /tmp/.../sources/SP001|2026-W34/production-state.json` via same `build_manuscript_manifest → READY` chain. 1/8 pass (`review_contract_preserves...`). Owner: **C2 + A** as above. Not a publisher-valid regression proof.

### REG-03 [A] — `test_survey_release_checkpoint_v2::test_cli_main_success_and_error` ERROR (run-17, `bbd6acad...`)
- Same `AttributeError: 'str' object has no attribute 'is_absolute'` at `survey_release_checkpoint_v2.py:77 _low15.load_typed_checkpoint_record(repo_root, _ref["path"])` → `LOW:300`. 8/9 pass. Owner: **A** (same Path/str coercion as C2-01). Blocks CLI release path only.

All other scoped regressions PASS (evidence 12, completeness 2, screening 7, drafting 5, histJSON 6, pubset 18) with actual helper fixtures (no skips hidden; `Ran N` present; ResourceWarnings in B15 are cleanup notices, not skips).

## 7. Source-bound results (no whole-acceptance claim)

- A full operation (LOW FULL resolve/report/proof/decision/retention/lineage + actual git own-epoch + HIGH prepare/adopt/resume/readback, both routes + 14 fault/later-seam tests): 19/19 PASS in 22.05s — bounded A-scope only.
- B ordinary consumers (SizedRef 3-key fix + 3 new real-chain tests): 15/15 PASS — B-scope only.
- C1 own scope (closure 6 incl real G71→G76 reloaded graph + research graph 5): 11/11 PASS — C1-scope only.
- C2 writers + diagnostic Gate fix: 14/16 PASS; 2 blockers above prevent C2 sign-off.
- Legacy 9/9 PASS — no regression on those three files at A4 pins; NOT full-suite health.
- Scoped regressions: 60/89 PASS; 3 systemic module failures above (readerGate, publication, release-CLI) prevent downstream sign-off; P1/P2R/P2V/P3S/renewal tests NOT run (left for next task after Path/str + writer-gate corrections to avoid burning suite on known systemic cause).
- Exec invariant held throughout (PRE/POST 756, 0 pycache, FINAL manifest recheck would be 0 mismatches — counts unchanged; failures are functional contract mismatches, NOT source drift, NOT import/setup systemic except the two systemic patterns mapped above).
- No longitudinal writer test exists yet (current writer unit will write own new test-only file, no existing files — NOT run here).

## 8. Compliance and handoff

- No source patch, no `git clean/reset`, no config/network, no ordinary commit/push, no Human HEAD/status, no live-candidate/proof-copy execution (ONLY frozen exec).
- All failures/raw/fixtures preserved; no old-log overwrites; no auto-skipping.
- Identity/proof limits: fixed A4 snapshot `2eb615b4...` + exec `...160708Z` + HEAD `409b292...` + inert origin; independent DBs with synthetic provenance (process identity); no genuine approvals; no Production semantic claim. Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN preserved except progress. Later lifecycle witness (full Weekly/Thematic correction→repeat→normal regeneration/Architecture/Draft/publication→editorial/renewal, G71→G76 control, failure/resume seams) is SEPARATE next task — NOT claimed done.
- Return to root: assign A Path/str coercion + READY-vs-legacy ordering, C2 finalize guard ordering + healthy-legacy validator threading, then re-freeze and re-run affected + P1/P2R/P2V/P3S/renewal + later lifecycle witness + independent implementation review. Stop at Human Commit Point.
