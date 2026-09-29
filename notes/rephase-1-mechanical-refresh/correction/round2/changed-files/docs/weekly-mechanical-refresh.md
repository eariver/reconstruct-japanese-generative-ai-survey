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

## Guarantees and limits (implemented)

- Canonical paths only, derived from Profile `source_root`/`survey_root`:
  State, publication `v2`, manuscript, reader input, receipt, Gate, retention
  and guard/temp/live targets. Any symlink ancestor, unsafe alias, traversal
  or non-canonical State/profile path stops before any write. The writer never
  follows a retention symlink out of root and never blesses changed bytes by
  re-hashing after drift.
- Complete bound snapshot (receipt accepted/authored/reviewed/semantic/outputs,
  old Gate/manuscript/reviews/PDF/bundle + deterministic results, validation
  checkpoint/prior chain, config/control/profile/HEAD) is captured before the
  guard and rechecked after guard acquisition, before each live write and
  before rollback/commit-sensitive operations. The live Gate/receipt destination
  is rechecked for its expected old hash immediately before atomic replace.
- Live receipt/Gate use same-directory temp + atomic replace from known
  expected bytes with readback verification. The revalidation owner creates its
  new record exclusively (`xb`, no exists-then-write race) from known serialized
  bytes and replaces State via bounded temp + replace from known bytes, with
  immediate pre-mutation basis/HEAD/State rechecks. Known-write hashes are of
  expected serializations, never read-after-write blessings.
- Cooperative guard `.mechanical-refresh.lock` serializes cooperating refresh
  commands only; other publication writers/editors must be externally
  serialized. No stale-lock stealing. The guard is released only when it still
  contains the operation's exact expected bytes after verified safe restore or
  after successful commit. A foreign/replaced/removed guard is never deleted.
- Commit point is the successful return of `revalidate_publication_surface`
  after its strict post-State validation. Post-commit reporting/readback errors
  never undo committed authority. Before commit, restoration rewrites only
  operation-owned files whose current bytes equal captured originals or this
  operation's known written bytes while HEAD/State/provenance and unchanged
  dependencies still match; unknown bytes are never called “our changed Gate”.
  If safe restoration cannot be established, live bytes + retention + guard are
  preserved and the command fails closed with precise paths/hashes.
- The wrapper inspects actual State/record disposition after an API failure and
  never assumes rollback completed. A leftover/changed record or changed State
  retains the guard for manual recovery and never deletes unknown record bytes.
- No full multi-file atomicity, no crash/kill/power-loss automation and no
  global compare-and-swap against noncooperating writers are claimed. Retained
  bytes plus an occupied guard identify an incomplete operation; a later normal
  invocation refuses.

## Failed runs and manual reconciliation (operator task, not automation)

- A refused run (exit 2 with a precise message) before live replacement
  leaves live bytes, State and records untouched; a run that owned a guard
  releases only its own unchanged guard. Pre-live aborts never touch foreign
  guards, temps, retention or history.
- If live bytes plus retention plus an occupied guard remain, a later run
  refuses. Reconciliation is an explicit operator task under existing
  authority, not automated adoption and not “copy old State back”:
  1. Compare `retention.json` recorded hashes/counts/paths against live
     `sha256` and `git rev-parse HEAD`; identify whether live equals retained
     originals, this operation's known new bytes, or unknown foreign bytes.
  2. Verify the validation checkpoint, prior chain, profile/config/control
     bytes and all receipt/Gate/manuscript/review/bundle references with the
     existing validators (`validate_receipt`, `validate_reader_surface_gate`,
     `validate_agent_state`, `resolve_active_publication_revalidation`).
  3. If live is unknown/foreign or a new/changed revalidation record remains
     without State provenance, do not overwrite it and do not delete the
     guard/retention/record. Resolve the drift under normal publication
     authority (fresh checkout, re-review, or a new bounded renewal once the
     tree is clean), then remove only the operation-owned guard after
     verification.
  4. Never delete another operation's guard, temp files, retention or history,
     never steal a stale lock automatically, and never complete missing
     authority by copying retained bytes over live unknown bytes.
- After the revalidation call returns successfully, authority is committed at
  the new `publication-surface-revalidation-rN.json` record and State pointer;
  later reporting errors never roll it back. Keep the retention and guard
  evidence for audit; a post-commit readback failure requires manual
  reconciliation of the committed record, not restoration of old bytes.
