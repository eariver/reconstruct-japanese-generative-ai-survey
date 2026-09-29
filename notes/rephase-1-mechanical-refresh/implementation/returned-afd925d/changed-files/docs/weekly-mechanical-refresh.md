# Weekly mechanical refresh — operator runbook (informational)

This note describes how to run the bounded mechanical-only Weekly
receipt/Gate renewal. It is **not** publication authority: every guard is
enforced by `refresh-mechanical-evidence` itself and the existing
validators. Do not register this file as a contract file.

## When this applies

- Edition is pre-decision `VALIDATED_DRAFT` (Architecture approved, Preview
  pending without provenance, Freeze/Release pending, Exception Gate
  inactive) with strict State passing and, on repeat, a healthy LIVE active
  revalidation record.
- The only committed tool change since the bound receipt is a reviewed edit
  to `scripts/survey_weekly_derivation_v2.py`. Any other control, schema,
  style, config, contract, reviewer, helper or workflow change, any
  accepted/authored/render/review-criteria difference, or a dirty worktree
  stops the command before any write.
- The edition's receipts were first produced by a candidate that already
  installs this command. Pre-install/e4-era receipts are not migrated
  in place; give them a separate disposition.

## Command

```text
python scripts/survey_agent_control_v2.py --repo-root <edition> \
  refresh-mechanical-evidence \
  --state <canonical production-state.json> \
  --reason <non-empty reason> --executor <identity> \
  [--recorded-at <instant, default now>]
```

Fixed derived paths only: no alternate config, manuscript, retention or
implementation override. `reason_class` is always the existing
`REVIEWED_CORE_CHANGE`. A no-change edition is refused as
`MECHANICAL_REFRESH_NO_OP` before anything is written.

## What it writes

Live: `publication/v2/validated-source-manifest.json`,
`publication/v2/reader-surface-gate-v2.json` (same-directory atomic
replace), plus the existing revalidation API's new
`publication-surface-revalidation-rN.json` record and State pointer.
Inert evidence: `publication/v2/.mechanical-refresh-retention/<run-id>/`
(old receipt + old Gate + old State bytes with hashes) and one cooperative
guard `publication/v2/.mechanical-refresh.lock` held only during the run.

## Failed runs and stale guards

- A refused run (exit 2 with a precise message) before live replacement
  leaves live bytes, State and records untouched; a run that owned a guard
  releases only its own guard.
- If live bytes plus retention plus an occupied guard remain, a later run
  refuses. Reconciliation is explicit manual work under existing authority:
  compare `retention.json` hashes against live `sha256`, either complete
  the renewal with the same inputs after the drift is resolved, or copy
  the retained bytes back and re-validate. Never delete another
  operation's guard, temp files, retention or history, and never steal a
  stale lock automatically.
- After the revalidation call returns successfully, authority is committed;
  later reporting errors never roll it back.
