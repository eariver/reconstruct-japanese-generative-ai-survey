# Execution — SP-first Selection validation (report-only, bounded)

Authority: `astra-operation-resolution.md` §§3–4 (report-only, no advance). Source `.rephase-1-editorial-runtime/selection-scaling-real-20261116T021943Z/candidate-work` HEAD `3231a0c280287411513bba359f4d3d2b6703d591` (actual `d591`; R2 recorded `f591` typo superseded), parent `ae0dd1ee…`, tree `ff01b73e…`. Pre-PASS 774/774, R2 State/Profile/CP/completion/4refs/7outputs unchanged, guards absent, target absent, canonical `EVIDENCE_REVIEWED/SELECTION_COMPLETE.json` absent.

Invocation (stdlib launcher, owned process-group only, 1200s bound):

```
python3 -m scripts.survey_stage_validation_v2 \
  --repo-root <ABS-candidate> \
  --state sources/SP-efficient-llm-2026/production-state.json \
  --artifact candidate-matrix=sources/SP-efficient-llm-2026/candidate-matrix-v2.json \
  --artifact candidate-selection=sources/SP-efficient-llm-2026/candidate-selection-v2.json \
  --output sources/SP-efficient-llm-2026/orchestration/v2/stage-validation/selection-resume-20261117-r1.json
```

CWD `<ABS-candidate>`, `PYTHONPATH=<ABS-candidate>`, env `PYTHONDONTWRITEBYTECODE=1 GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null` + `PATH/HOME/LANG` only. No `--implementation-sha`, no private context, no fake report, no advance. `--recorded-at` omitted (default normal invocation time).

Outcome: **exit 2, timeout False, wall 35.004s**, PID 1329968 (reaped). `stdout 0B`, `stderr 253B`:

```
prior Stage Checkpoint fails …/schemas/stage-checkpoint-v2.schema.json: $: 'from_state' is a required property
```

Report `selection-resume-20261117-r1.json` absent (no manual JSON). No State/checkpoint/gate writes; post-inventory State/Profile/CP/7 outputs unchanged, guards absent, checkpoints still absent. `/proc` windows in `proc-snapshots.json` (same-child only, no totals claim).

Action: STOP this edition, preserve raw/partials, report to root. No local fix/retry, even pre-import. W34 single invocation proceeds separately only after reaped + unchanged check.

Raw: `argv.json`, `cwd.txt`, `env-whitelist.json`, `child-pid.txt`, `start-utc.txt`, `end-utc.txt`, `wall-s.txt`, `exit-or-timeout.txt`, `stdout.txt`, `stderr.txt`, `proc-snapshots.json`, `pre-inventory.json`, `post-inventory.json`, `report-absent.txt`, `machine.json`.

(End of file)
