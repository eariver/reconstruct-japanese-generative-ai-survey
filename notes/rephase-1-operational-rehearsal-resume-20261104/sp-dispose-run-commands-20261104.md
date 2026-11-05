# SP dispose + normal-run one-use wrapper — commands note (review only, NO EXECUTION yet)

Small separate single-use tool for the guarded SP Ledger → Completeness
removal + ONE ordinary normal Evidence retry. Reuses pinned r6 helpers
(code hash verified before import); no new auth framework, no duplicated
validators, no new shipping API/module/schema, no State/code/config/test
changes. No network/Production/reconstruct Git. Project APIs run only on
explicit e84 when root authorizes; authoring used stdlib only, no active
project imports.

## Files (this packet only)

- `sp-operator-dispose-run-20261104.py` — one-use wrapper (source review only).
- `sp-dispose-run-launcher-20261104.sh` — unique EXCLUSIVE bundle dir (`mkdir`,
  no `-p`), no git. Captures argv/cwd/env-subset/timestamps + tool
  stdout/stderr/exit.
- This note (phase table + hashes + commands).

## Source-level phase table (`sp-operator-dispose-run-20261104.py`)

| Phase | Code | Gate (fail closed, preserve, no auto restore/retry) |
|---|---|---|
| P0 invocation pinning | `main` L620, `_load_r6` L78 (hash-verified r6 import), `_verify_ready_self`, `R6._verify_manifest_self` | tool/READY/manifest bytes == externally recorded hashes; manifest clean; READY ready+prepare-only and binds expected manifest; args present |
| P1 pre-disposal verification (reads only) | `stage_dispose_run` P1, `R6._phase0_source_precheck` (modules + all771, stdlib, before imports), `R6._bind_roots_after_import`, live impl vs READY+recorded head, `R6._strict_state_and_ready`, tree vs baseline+19 (571), intended 771 + test pin, all30 rows + stable_task_id/_source_class, staged input/supplement pins, FULL supplement validation (existing, facade), retained package basis validation (existing, facade), gates/CP/refscan/checkpoints/accepted pins | any drift → refuse, zero active writes |
| P2 retention + backups | `_backup_owned` (re-read + pin, O_EXCL 0o664 + chmod + readback), exclusive NEW retention + `retention-manifest.json` with context + immutable old→new linkage | single-use (refuse existing); no rename onto backup names |
| P3 ledger gate | `_gate_phase` (571 set): strict State + DM022, full tree, 771, READY/manifest same-hash, ledger+completeness present pinned | then `os.unlink` ledger ONLY; verify absent + not symlink; retention copy re-verified |
| P4 completeness gate | `_gate_phase` (570 set, ledger absent EXPECTED + verified, completeness present pinned, rest exact) | then `os.unlink` completeness ONLY; verify both absent (569) |
| P5 post-disposal verify | `_verify_tree_phase` (569), accepted dirs byte-identical, gates, State bytes unchanged (still CAND) | any drift → STOP, preserve |
| P6 run | ONE `rn.run(repo, state, input, supp)` — existing public API, owns its facade per phase; no outer facade, no checkpoint calls, no run copy | result count must be 160; failure after removal/partial run → preserve exact partials, report, no retry |
| P7 post-run verify | `_check_post_run_layout` (stdlib: old unchanged except exact2 + 2 exclusive NEW accepted dirs, counts, input/supplement refs, view/card binding) + actual `validate_evidence_acceptance`, `validate_edition_views_acceptance`, `validate_materiality_ledger`, `validate_profile_completeness` | overall_status == staged input closure; counts 160 results / 165 discovery / 15 obligations from actual files |

Expected outputs (read from actual acceptance paths/returns, not root JSON
alone): Evidence `results/` (160 cards) + `tasks/` (160 copies) + `package.json`
copy + archived `interactive-evidence.json` + `interactive-audit.json`;
Views `edition-views-accepted.json` + `views/` (160); regenerated
`materiality-ledger-v2.json` + `profile-completeness-v2.json` (same paths, new
bytes); State/Profile/checkpoints/Human/old accepted dirs/config/source/tests
byte-identical.

## Invocation (DO NOT RUN until root authorizes after independent review)

```sh
notes/rephase-1-operational-rehearsal-resume-20261104/sp-dispose-run-launcher-20261104.sh \
  --retention-dir notes/rephase-1-operational-rehearsal-resume-20261104/retention-SP-dispose-YYYYMMDDTHHMMSSZ \
  --ready-path notes/rephase-1-operational-rehearsal-resume-20261104/retention-SP-20261104T162747Z/READY.json \
  --expected-tool-sha <64-hex of sp-operator-dispose-run-20261104.py at authorize time> \
  --expected-ready-sha c7cd05a888106b2cdf0f4e984fb22412678a8ff792deda1ad7ff94e3b31e7643 \
  --expected-manifest-sha 6507804dd4b16ff93f6513773a1adb6a47d7cc3db628b6f1a1c1f9efb97d6bb7
# exit 0 → DISPOSE_RUN.json (full bindings) in NEW retention; exit 2 → FAILURE.json + partials preserved, no retry.
```

READY `c7cd05a8…` and manifest `6507804d…` are externally recorded here; the
tool refuses on any byte drift at invocation, before each removal, and before
reporting. Wrapper bytes must be hashed at authorize time and passed as
`--expected-tool-sha` (never copied from a truncated return).

## Limits

Stop at first failure; preserve exact partial state; no automatic restore or
retry. No State/CP/Human/config/schema/source/test writes beyond the exact
regeneration set; no glob/force; no cleanup of orphans. No semantic approval
is produced; counts/bindings are mechanical checks only. If the run succeeds,
Selection/Architecture, audit, adoption, and savings remain OPEN per standing
closeout. WholeNOT_READY/step4B3OPEN/auditunstarted/DM021+022OPEN.
Human Commit Point — stop.
