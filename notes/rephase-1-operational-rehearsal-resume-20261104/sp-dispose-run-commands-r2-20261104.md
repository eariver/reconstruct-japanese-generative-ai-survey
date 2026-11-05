# SP dispose + normal-run one-use wrapper r2 — commands note (review only, NO EXECUTION)

Single bounded operation: guarded removal of the two exact unaccepted CAND-owned
files (Ledger, then Completeness) + ONE ordinary normal Evidence retry via the
existing public run API. Supersedes rejected v1 (preserved untouched, never
executed): fixes ctx screening-path KeyError, audit archive-path semantics,
retention containment, return-gate rechecks, umask-recorded output modes,
pre-unlink backup re-verification, and removes dead duplicate helpers.
No auth framework, no duplicated validators, no new shipping API/module/schema,
no State advance.

## Files (this packet only)

- `sp-operator-dispose-run-r2-20261104.py` — 46350 bytes
  SHA256 `2044257f18451beecf38589c0b1155a59f3506d9958b5adf5afc23c7f9bb0014`
- `sp-dispose-run-launcher-r2-20261104.sh` — 3020 bytes
  SHA256 `b60d2cad41bb3f3e3121a3dedf41df11e4aa2d1f0108fb49096c4ec200a7f9ac`
  (unique EXCLUSIVE bundle dir, `mkdir` without `-p`, no git; captures argv /
  cwd / env-subset / UTC timestamps / tool stdout / stderr / numeric exit)
- This note. Corrected DATA + expected manifest are the pinned r4/r6 files:
  input `0ee3187eb3850fd79060556bc03cfbe4634365efbf33f47cdacd119d0b7c2a89`
  (355386B), supplement `1221d293b121977d8fe4ce086e9fb09a2c4b296c1d50bcbcda3705ec997b5db7`
  (31278B), manifest `6507804dd4b16ff93f6513773a1adb6a47d7cc3db628b6f1a1c1f9efb97d6bb7`
  (395713B), READY `c7cd05a888106b2cdf0f4e984fb22412678a8ff792deda1ad7ff94e3b31e7643`
  (12270B), retained pkg `package.json` `4f6b9bdad089d88e12cbe96b1a80020d1dedb82da9afc33c752f6713c02789b5`
  (160 tasks + 160 task files, kept outside the active tree).

## Source-level phase table (`sp-operator-dispose-run-r2-20261104.py`)

| Phase | Code location | Gate (STOP + preserve, no auto restore/retry) |
|---|---|---|
| P0 invocation pinning | `main` + `_load_r6` (hash-verified r6 import) + `_verify_ready_self` + `R6._verify_manifest_self` + `_read_umask` (round-trip, restored) | tool/READY/manifest bytes == externally recorded 64-char hashes; manifest clean; READY is a prepare-only record binding the expected manifest; umask recorded for write_json-derived outputs. No active writes. |
| P1 full pre-disposal verification (reads only) | `stage_dispose_run` P1; `R6._phase0_source_precheck` (10 modules + all771 with recorded per-file modes incl. `0o775` executable + triangulated test pin) before imports; `R6._bind_roots_after_import`; live impl via `core.repository_commit_sha` (single isolated call) vs READY + recorded e84; `R6._strict_state_and_ready`; full SP tree == baseline 552 + READY exact 19 (571); all30 Raw (+ `stable_task_id`/`_source_class` per row); staged input/supplement pins vs READY; FULL supplement validation (existing, Raw-present, facade); retained package basis validation (existing, facade); gates/CP/checkpoints/accepted pins; 160/15 counts | any mismatch → refuse, zero active writes. |
| P2 exclusive NEW retention + backups | `_check_retention_root` (must sit DIRECTLY under the resume packet) + `_require_absent` + `mkdir(exist_ok=False)`; `_backup_owned` (re-read + pin vs manifest, O_EXCL\|O_NOFOLLOW, chmod 0o664, readback; 64-char live State SHA required, 40-char commit refused) + `retention-manifest.json` with context + immutable linkage | any drift → STOP, preserve; no rename onto backup names; no automatic restore. |
| P3 ledger gate | `_gate_phase(..., expect_ledger=True)` — same-hash manifest/READY recheck; strict State + DM022; full tree == 571 set; all771; ledger AND completeness present-pinned; BOTH retained backups re-verified (bytes/mode/sha/nlink) | then `os.unlink` ledger ONLY; verify absent + not-symlink; re-verify retained copy. Single-operator snapshot checks, no CAS claim. |
| P4 completeness gate | `_gate_phase(..., expect_ledger=False)` — 570 set (ledger absent EXPECTED + verified absent, completeness present-pinned, rest exact) + same rechecks | then `os.unlink` completeness ONLY; verify both absent (569 set); re-verify retained copy. |
| P5 post-disposal verify | `_verify_tree_phase` (569 set); old accepted dirs byte-identical; gates absent; State bytes unchanged (still CAND) | any drift → STOP, preserve. |
| P6 ONE ordinary normal retry | single `rn.run(repo, state, input_abs, supp_abs)` with the real staged paths; no outer facade (run owns it per phase), no checkpoint calls, no run copy | result `evidence_result_count` must be 160 or STOP (preserve, no retry). |
| P7 post-run verify | State bytes unchanged (still CAND); `_check_post_run_layout` (exact delta: only exact2 regenerated + 2 NEW accepted dirs; new outputs carry recorded umask modes, archived input is O_EXCL 0o664; old files byte-identical); actual validators `validate_evidence_acceptance`, `validate_edition_views_acceptance`, `validate_materiality_ledger`, `validate_profile_completeness` (all real, inside facade); input ref == NEW accepted archive path + staged bytes (no path rebinding); package supplement ref == staged supplement; counts 160 results / 165 discovery rows / 15 obligations from actual files; `overall_status` == staged input closure | any mismatch → STOP, preserve exact partials. |
| P8 return gate + record | manifest/READY same-hash recheck; staged input/supplement re-pin vs READY; new ledger/completeness vs P7-captured `ledger_sha`/`completeness_sha` (not reseal); all771 recheck; then `DISPOSE_RUN.json` + `journal.json` (exclusive writes) with full hashes | exit 0 with result JSON on stdout (captured by launcher); exit 2 + `FAILURE.json` + retained partials otherwise. |

Expected normal outputs (read from actual accepted dirs, never assumed):
`evidence-accepted.json` + `package.json` (copy) + archived
`interactive-evidence.json` + `interactive-audit.json` + `tasks/` (160) +
`results/` (160 cards) under `evidence/v2/accepted/<new_result_set_sha>/`;
`edition-views-accepted.json` + `views/` (160) under
`evidence/v2/views/accepted/<new_view_set_sha>/`; regenerated in-place
`materiality-ledger-v2.json` + `profile-completeness-v2.json`.
Old accepted dirs/State/Profile/checkpoints/Human/source/config/tests unchanged.

## Invocation (DO NOT RUN until root authorizes after independent review)

```sh
notes/rephase-1-operational-rehearsal-resume-20261104/sp-dispose-run-launcher-r2-20261104.sh \
  --retention-dir notes/rephase-1-operational-rehearsal-resume-20261104/retention-SP-dispose-YYYYMMDDTHHMMSSZ \
  --ready-path notes/rephase-1-operational-rehearsal-resume-20261104/retention-SP-20261104T162747Z/READY.json \
  --expected-tool-sha <64-hex of sp-operator-dispose-run-r2-20261104.py at authorize time> \
  --expected-ready-sha c7cd05a888106b2cdf0f4e984fb22412678a8ff792deda1ad7ff94e3b31e7643 \
  --expected-manifest-sha 6507804dd4b16ff93f6513773a1adb6a47d7cc3db628b6f1a1c1f9efb97d6bb7
# exit 0 → DISPOSE_RUN.json in NEW retention; exit 2 → FAILURE.json + partials preserved, no retry.
```

The tool refuses on any byte drift of itself, READY, or the manifest — at
invocation, before each removal, and before recording. The reported tool SHA
above was computed from bytes at authoring time; re-verify at authorize time
(do not copy a truncated prefix — full 64 hex only).

## Limits

Stop at first failure; preserve exact partial state; no automatic restore or
retry. No State/CP/Human/config/schema/source/test writes beyond the exact
regeneration set; no glob/force; no cleanup of orphans. No semantic approval
is produced; counts/bindings are mechanical checks only. If the run succeeds,
Selection/Architecture, audit, adoption, and savings remain OPEN.
WholeNOT_READY/step4B3OPEN/auditunstarted/DM021+022OPEN. Human Commit Point —
stop. This note authorizes nothing; only an explicit root continuation does.
