# W34 guarded resume plan r3 — concise (NO EXECUTION YET)

Root decision required BEFORE any step: **CONTINUE ABSENT** — exact2 stay
absent (`materiality-ledger-v2.json`, `profile-completeness-v2.json` both
absent, verified), backups preserved (`retention-W34-dispose-20261105T003915Z/`
Ledger 186202B `76ac53...` + Completeness 71532B `93dbef...` + manifest),
**not auto_restore**. Any State drift, backup drift, or unexpected tree
change stops with partials preserved; no unconditional copy-back (could
overwrite newly accepted authority).

## Current pinned state (actual, not resealed)

- Active W34 tree **1780 files / 80 dirs** (baseline 1781 + staged r2 `1ea562...` −2 disposed). Staged r2 `interactive-evidence-w34-r2-20261104T235848Z.json` 1580317B present; exact2 absent (verified absent + not-symlink); old accepted `bf208.../f744...` + State `7e6a50c2...` CAND + profiles/checkpoints/supplement `ce6f...` 428/425 preserved. Source771 770+test diff preserved. SP `c7cd05a8...` + `cf26a23c...` preserved (no SP invoke).
- Backups pinned: retention manifest binds old/new path, SHA, bytes, mode 0664, live-verified 64-char State SHA, UTC. No rename onto backup names.

## Proposed RESUME-only execution wrapper (spec, NOT implemented here)

A NEW one-use wrapper (no destructive tool code in this packet) SHALL, after
separate Root + independent review auth:

1. Verify pins (wrapper/manifest/READY/r3 input `15e87eef...`/r6 helper) + strict CAND State + full tree == 1780 + all771 + staged r2 + backups + SP snapshots. Zero active writes on failure.
2. Stage ONLY NEW input: `interactive-evidence-w34-r3-<UTC>.json` (r3 bytes `15e87eef...`, O_EXCL 0664, readback). No restoration, no removal, no supplement/Raw change. Expected tree 1780 → 1781.
3. Full NONPUBLISHING preflight with SAME canonical card core (no accept):
   `prepare_evidence_package` to packet-retained scratch (409 tasks) +
   `validate_interactive_input` (r3 vs exact task source sets, 409/3) +
   `_build_card_core` for ALL 409 real tasks (same function run uses, `_validate_card_core` must pass, no writes) +
   FULL supplement Raw closure (`validate_evidence_authority_supplement`, facade, 428/425 present). Stop + preserve on first failure; no run yet.
4. Existing normal `rn.run` ONCE (owns facade) with staged r3 + existing supplement. Expected normal outputs 409/439/3 LIMITED + 2 NEW accepted dirs; State stays CAND.
5. Post-run verify (EFFECTIVE 439 validators, audit archived path+bytes, umask modes, old accepted immutable) + return-gate recheck (same pins, not reseal).

## Failure logger fix (for resume wrapper)

r2/r3 `main()` passes relative `rd/FAILURE.json` to `_stage_bytes_exclusive_under` (requires absolute) so the failure record itself fails. Resume wrapper MUST absolutize (`rd.resolve()`) before the best-effort FAILURE write (or reuse packet helper). Original error must be preserved verbatim (here: c001-class target mismatch, now fixed in r3 DATA).

## Next

Independent semantic review of r3 input + this plan; exact restoration decision (CONTINUE ABSENT) by Root; no State advance, no Selection, no SP mutation. No execution until authorized.
