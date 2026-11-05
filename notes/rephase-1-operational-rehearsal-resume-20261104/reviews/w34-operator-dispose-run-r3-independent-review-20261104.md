# Independent source review — W34 dispose+run r3 (source-only, NO execution) + Root finding correction

**Role:** New independent reviewer. NOT author/operator, NOT Astra/root, NOT Sol/Luna/Human. Preserves v1 + r2 reviews untouched.

**Bounds:** Source/data-only, no active/project runtime imports/execution/tests/writes, no network/Production/reconstruct Git (`git -C .` never used)/readback, no subagents. `Read` + `sha256sum` + stdlib text/AST inspection only. Wrapper/launcher/checks NOT executed. Active source read only at e84 candidate-work. Creates only NEW r3 review files.

**Files (programmatic full SHAs):**
- NEW wrapper r3 `w34-operator-dispose-run-r3-20261104.py` `48be58796e7ee2ef31ce0873e3223d7c0f78fb6de08aed3012f06b593f2846b8` 52410B
- NEW launcher r3 `w34-dispose-run-launcher-r3-20261104.sh` `46f90f2116af45525b68e2924a2bb852158f5a8582780defe8b362a6c32f1d4f` 1099B (`TOOL=...r3...`, otherwise same guards/single-use as r2)
- NEW checks r3 `w34-dispose-run-r3-checks-20261104.py` `bda40b6b5d5664d95d810ff8b0e304609522c4d321fdc253f88219ce94cd55da` + raw `6d082ed6…` 6/6 PASS (controlled seam only — NOT broad proof, see §3)
- Unchanged: manifest `cede7e467406b25763b9090484b31e34dc771a6c85a81e52bd19025a9db02590`, input `1ea56297…`, READY `473bf85b…` 409/409, supp `ce6f977a…`, r6 `2c6f1aeb…`; r2 wrapper `a77dbb88…` + launcher `22c0fee3…` preserved
- Actual e84 defs (read, not imported): same as r2 review (`run`, `validate_supplement/package/acceptance/views/ledger/completeness`)

## 1. Root finding correction record (r2 defect → r3 fix)

Root final read: r2 phase0 `errs.extend(_check_intended_tree_stdlib…)` then proceeds to `sys.path.insert` + 9 project imports; `errs` only raised later after imports. Changed source could be imported before refusal. **Correction in r3 (tiny delta, 48-line unified diff):**
- `if errs: raise ValueError("phase0 source precheck FAILED (refuse BEFORE any project import)")` immediately after intended check, BEFORE `sys.path.insert` (lines 324-326). AST order verified in checks (`BEFORE any project import` index < `sys.path.insert` index).
- 10th schema: `rn.schema_gate` bound after 9-module re-hash (same pre pin `survey_schema_v2.py`, same e84 root, `__file__` present, hash == pre, `__pycache__` refuse). After-import now 10/10 vs pre pins. Unused `_bind_roots_after_import_strict` left untouched (dead, no call — avoids churn, harmless).

## 2. No regressions in destructive guards / normal-run paths

Unified diff r2→r3 = docstring (R3/B1-B3 preserved note) + 2 code hunks above only. Verified counts identical r2→r3: `os.unlink x2`, `rn.run x1`, `_check_post_run_layout x2`, `validate_ledger/completeness/acceptance/views/supplement/package x1 each`, `_derive_old_accepted_dirs x2`, `R6._strict_json(State) x2`, `_verify_tree_phase x3`, `_gate_phase x3`, `_backup_owned x3`. Full `1782->1781->1780` gates, O_EXCL backups + StateSHA64, EFFECTIVE 439 validators, archive `path+sha==staged`, `409/439/3 LIMITED`, umask/packet/failure, SP snapshot, strict State, READY exact pkg, frozen old dirs — all byte-identical outside the 2 hunks. No new network/Production/Git, no top-level `sys.path.insert`/`from scripts import` (only docstring mention + inside `stage_dispose_run` after fail-closed gate), no `subprocess/urllib/requests/socket`.

## 3. 6 checks scope (controlled seam, NOT broad proof)

R3 checks 6/6 prove narrow seam behavior on REAL files: `r2_defect_present` (source shape), `r3_fail_closed_before_import_ast` (AST order), `r3_binds_schema_gate`, `seam_drift_detected_by_hash` (tampered copy `/tmp/opencode/w34-r3-seam/tampered-manifest.json` first intended `8c779e60->0c779e60` detected by real `R6._check_intended_tree_stdlib`), `seam_refuses_before_import` (`stage_dispose_run` with tampered manifest + rebound READY raises `phase0 … BEFORE any project import`), `no_project_import_on_refusal` (`sys.modules` has no `survey_*/scripts` after refusal). Controlled single-file tamper + import-gate only — NOT full-tree/destruction/runner proof. Must not be cited beyond fail-closed + 10th binding.

## 4. Verdict

**DISPOSE_AND_RETRY_READY final (source-only, single bounded Root-authorized run).** Wrapper r3 `48be5879…`, launcher `46f90f21…` valid: R3 fail-closed + 10/10 schema with zero guard/runner regressions, B1-B3 preserved, same READY/manifest/input. Preserves v1/r2 reviews + preflight-actual `READY 473bf85b…` (no removal yet). No semantic/EVIDENCE_REVIEWED/Selection/adoption.

**Authorized-next (ONE bounded Root auth AFTER this review, NOT now):** Run `w34-dispose-run-launcher-r3-20261104.sh` with NEW packet-direct retention + READY `473bf85b…` + manifest `cede7e46…` + tool `48be5879…` externally recorded (tool self-checks `__file__` vs `--expected-tool-sha`). STOPS at `DISPOSE_RUN.json` or first `FAILURE.json`. No restore/retry. Human Commit Point — stop.

Attribution: Independent reviewer. No execution/network/Production/reconstructGit/project imports/subagents.
