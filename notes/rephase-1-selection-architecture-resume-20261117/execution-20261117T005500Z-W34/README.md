# Execution — W34 Selection validation (report-only, bounded, after SP reaped)

Authority: `astra-operation-resolution.md` §§3–4. SP child reaped (exit 2, 35.004s), source 774 still OK, W34 authority same as R2, so single W34 invocation allowed. Source HEAD `3231a0c…d591` actual, parent `ae0dd1ee…`, tree `ff01b73e…`. Pre-PASS 774/774, W34 State `a8586351…`/4162B, Profile `2a8c3089…`, CP `73ab28ea…`, completion `80c12d0c…`, 4 refs match, 7 outputs unchanged, guards absent, target absent, canonical checkpoints absent.

Invocation:

```
python3 -m scripts.survey_stage_validation_v2 \
  --repo-root <ABS-candidate> \
  --state sources/2026-W34/production-state.json \
  --artifact candidate-matrix=sources/2026-W34/candidate-matrix-v2.json \
  --artifact candidate-selection=sources/2026-W34/candidate-selection-v2.json \
  --output sources/2026-W34/orchestration/v2/stage-validation/selection-resume-20261117-r1.json
```

Same CWD/env/whitelist/no-override conditions as SP. No reviews/checkpoint/advance.

Outcome: **exit 2, timeout False, wall 180.013s**, PID 1331060 (reaped). `stdout 0B`, same `stderr`:

```
prior Stage Checkpoint fails …/schemas/stage-checkpoint-v2.schema.json: $: 'from_state' is a required property
```

Report absent, no State/checkpoint/gate writes; post-inventory unchanged. Cost reflects unfixed 45AG-scale public-validator multiplication; no timeout extension/retry/profile loop per dispatch. Do not fabricate PASS or call advance.

Raw: same set as SP (`argv/cwd/env/pid/start/end/wall/exit/stdout/stderr/proc-snapshots/pre/post/report-absent/machine`). Full stage advancement awaits later root dispatch on actual results.

(End of file)
