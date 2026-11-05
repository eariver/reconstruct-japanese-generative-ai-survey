# W34 dispose+run r3 — source review note (DO NOT EXECUTE)

r3 preserves r2 (`w34-operator-dispose-run-r2-20261104.py` 50975B `a77dbb88...`)
untouched. Minimal successor for Root final read; no broad features.
Independent review will confirm tiny delta, then Root authorizes.

## Root bug fixed

- r2 phase0 extends `errs` on intended drift then proceeds to
  `sys.path.insert` + project imports. r3 raises immediately if `errs`
  non-empty BEFORE any project import (`phase0 source precheck FAILED
  (refuse BEFORE any project import)`).
- r3 binds 10th schema imported transitively as `rn.schema_gate`
  (same pre pin, same e84 root). After-import was 9/10; now 10/10.
- Unused `_bind_roots_after_import_strict` left untouched to avoid churn.

## Files (packet only, no active writes)

- NEW wrapper `w34-operator-dispose-run-r3-20261104.py` 52410B
  `48be58796e7ee2ef31ce0873e3223d7c0f78fb6de08aed3012f06b593f2846b8`
- NEW launcher `w34-dispose-run-launcher-r3-20261104.sh` 1099B
  `46f90f2116af45525b68e2924a2bb852158f5a8582780defe8b362a6c32f1d4f`
- NEW checks `w34-dispose-run-r3-checks-20261104.py` 4555B
  `bda40b6b5d5664d95d810ff8b0e304609522c4d321fdc253f88219ce94cd55da`
  + raw `...raw.txt` 407B `6d082ed6...` — **6/6 PASS**
- Same manifest `cede7e46...` / input `1ea56297...` / READY `473bf85b...` /
  supp `ce6f...` / helper `2c6f...` unchanged.

## Focused behavioral proof (controlled seam, not tokens)

Tampered manifest copy in `/tmp/opencode/w34-r3-seam` (one intended SHA
`8c779e60->0c779e60`, real hash compare via `R6._check_intended_tree_stdlib`)
is detected (`seam_drift_detected_by_hash`). Calling r3 `stage_dispose_run`
with tampered manifest + rebound READY raises `phase0 ... BEFORE any project
import`; `sys.modules` has no `survey_*`/`scripts` after refusal
(`no_project_import_on_refusal`). AST confirms fail-closed order + 10th
`rn.schema_gate` binding.

## Limitations / no execution

Tiny delta only (fail-closed + schema 10th). All r2 guard/runtime semantics
otherwise exact (1782->1781->1780, EFFECTIVE 439, audit/umask/preservation).
No active execution/network/Git. Awaiting independent review + Root auth.
