# Correction2 notes (R2 S1–S3 + E1/E2) — DRAFT stage, NO long execution

2026-10-14. Second correction unit on DM021-P2R after root's R2 review.
v6 sources (`77ee2a3e`/`22f56041`/`347e5499`), patch `f42af778`, v6 raw and
both reviews are preserved unchanged as historical (pre-edit byte copies at
`/tmp/opencode/jgas-dm021p2r-v6hist-20261014T000000Z/`). All edits below are
in the 3A candidate only; P1 unchanged; no branches/commits/network/adoption.
Runner/proof here are DRAFTS for root inspection BEFORE any long run. No
full suite, no proof execution, no `-O` run in this unit.

## New source pins (candidate `/tmp/opencode/jgas-dm021p2r-impl-20261013T123807Z/candidate-partial-b40de60`)

- `scripts/survey_editorial_retention_v2.py`
  `ee7ebc48fb57535d42b6474f3f4dfb21f3a77607d70f6d1d1dbe16daab9b1171`,
  121092 bytes, mode `0o664`, 2066 lines.
- `tests/test_survey_editorial_retention_v2.py`
  `8c4c2ea1a43cc23c42f6fbaa07fea95e617527b5f8573c80e16935618513ee9b`,
  89080 bytes, mode `0o664`, 1736 lines, 24 methods (19 + 5 new).
- `schemas/editorial-retention-manifest-v2.schema.json` unchanged
  (`347e5499259a…`, 5618 bytes).

## Module diff summary (vs v6 `77ee2a3e`)

S1 — final inventory boundaries:
- New `_retained_expected_sets()` (exact COPY-dest + manifest file set and
  retained-root dir closure).
- `verify_retention`: full retained re-inventory compared against exact
  expected sets AFTER the canonical-bytes check, before `reverify`/close.
- `capture_retention` post-verify block replaced with the complete
  recheck: P1 inputs + HEAD (as before) PLUS this capture's P2R dep pins,
  full control inventory equality, edition owned-delta accounting with the
  manifest as an exact owned addition (no prefix exemption), retained
  inventory exact sets, and owned dev/ino identity recheck for every
  owned entry; then `reverify` + close-all before success.

S2 — failure/ownership accounting:
- COPY creation `fstat` failure now closes the new fd, records
  `owned["creation_attempts"] = [{path, identity-failed}]`, and refuses
  `WRITE_IDENTITY_FAILED`/`OWNED_PARTIAL` BEFORE any write (no swallowed
  error, no unbound/stale `owned_entry` reuse).
- Manifest creation likewise `fstat`-pinned (`manifest_attempt` carries
  dev/ino; `MANIFEST_IDENTITY_FAILED`/`INDETERMINATE_INVOCATION` on
  failure) and the closed manifest owned entry carries identity.
- `_close_all(prior=...)` now attaches every secondary close failure to
  the prior structured error (`owned.secondary_close_errors` + detail),
  instead of discarding them with `pass`.
- `safe_read`/`reverify` intermediate-close paths preserve a structured
  primary (secondaries attached) and only raise `CLOSE_FAILED` when no
  primary is in flight (unexpected non-structured primaries chain).

S3 — historical verifier precision:
- Provisional COPY-dest mapping for ALL COPY rows (against the supplied
  proposal directory) BEFORE the retained-State read; canonical
  re-validation against the State/Profile-derived `expected_dir` retained
  later. A moved dest now refuses `RETENTION_DEST_MISMATCH` before any
  read of the moved path (v4's `PATH_MISSING` is preserved history, not
  the current oracle).
- Retained-State `research_profile`/`publication_profile` labels are
  mandatory (`LABEL_MISMATCH` when absent or disagreeing; the `if k in
  rstate` silent accept is removed).
- `capture_inputs` P2R dep entries require presence + well-formed shape
  only (`MISSING_P2R_DEP` when absent); the blanket live-producer byte
  equality (`P2R_DEP_DRIFT`) is removed with a historical-observation
  scope comment. Exact hashes remain enforced where paths are
  independently required (plan/staged/proposal/KEEP/retained).

Also: module/test "Note on edits" tooling caveats removed while touched
(headers updated to correction2 scope); no other docstring changes.

## Test diff summary (vs v6 `22f56041`)

- New `test_verifier_state_labels_required` (S3): coordinated retained
  State + plan row + manifest row + `proposal_ref` rebind reaching the
  label check; missing/disagreeing labels refuse with immediate no-write
  and restore-to-VERIFIED.
- New `test_verifier_late_retained_additions_refuse` (S1): plants a
  retained file / empty dir mid-verify (hooked on the staged-reader read,
  after first inventory + all rehashes) and asserts the FINAL boundary
  refuses (`"final retained"` in the error), with immediate no-write.
- New `test_capture_readback_control_edition_injection_refuses` (S1):
  control-file / edition-dir injections exactly at manifest open (inside
  the standalone-readback window) refuse `FINALIZATION_REFUSED` at the
  post-verify recheck; partials/retry/deltas asserted.
- New `test_fault_create_identity_and_close_preservation` (S2a):
  scoped creation-`fstat` failure refuses before any write through the
  fd (tracked zero writes), attempt recorded, partial + retry asserted.
- New `test_fault_primary_read_close_secondary_preserved` (S2b):
  injected primary read error + intermediate-dir close failures preserve
  `PATH_UNREADABLE` with non-empty `owned.secondary_close_errors`.
- Bind matrix: unplanted moved-dest expectation tightened to
  `RETENTION_DEST_MISMATCH` (with v4-history comment); planted case now
  records fd-chain reads and asserts the moved path was never read;
  added dep-hash distinction sub-case (wrong P2R dep hash still
  VERIFIES; required-path wrong hashes still refuse).
- Typed-hop `_check_both` and staged `_corrupt`/noncanonical paths now
  compare immediate mutated-pre/post snapshots before restoration
  (`_assert_no_write`).

## Cheap checks executed (exact commands, no cache writes/cleanup)

- `python3 -c "import ast; ast.parse(open('<module>').read()); ..."` for
  the module, test, and both DRAFTs — all `AST_OK`.
- `PYTHONDONTWRITEBYTECODE=1 python3 -c "import unittest; ... loadTestsFromName('tests.test_survey_editorial_retention_v2') ..."`
  in the candidate — 24 methods collected, imports clean, zero cache writes.
- `git status`/`rev-parse` (sanitized env, read-only): candidate still
  `3M13A` at detached `409b292`; `expected16-correction2.json`
  re-verified byte-identical to current files (`STATIC_MANIFEST_MATCHES_CURRENT`).
- One collection probe was first run with the wrong cwd (reconstruct) and
  loaded 1 unrelated test; re-ran correctly in the candidate (24). No
  side effects from the misstep (read-only import with bytecode disabled).

## Packet contents (`evidence-20261014T000000Z-correction2/`)

- `expected16-correction2.json` — STATIC final 16 pins (prepared from
  post-edit files before any test; the v7 draft verifies against it).
- `run_p2r_correction_v7.py.DRAFT` — E1 runner draft (exclusive `xb`
  outputs + output-exists refusal, direct redirect to open exclusive
  binaries, exact-path `safe.directory`, immutable stage files, checked
  Git rc with full status/tree/index/all16 SHA+mode+size pre AND
  finally-post, finally-enclosed launch with timeout/interrupt
  disposition, no cleanup, no `-O`).
- `proof_apply16_v3.py.DRAFT` — E2 proof draft (all-entry lstat walk with
  nlink/dirs/symlink/error-failing, inode-set intersection, exact remote
  pair + exact inert config URLs, exact-16-row applied status, console-only
  output-exists refusal, reserved outputs, declared removals only).
- `correction2-notes.md` (this file).

NOT in packet (by instruction): no v3 patch (generate only after final
pins are approved — the v3 draft expects `complete-p2r-16path-v3.patch`
at execution time), no v7/proof outputs, no long-run evidence.

## Substitutions / deferrals disclosed

- Removed module/test "Note on edits" tooling caveats per instruction;
  full substitution detail lives here instead of in shipping docstrings.
- Fixture base-reuse optimization deferred: current per-method fresh
  fixtures are proven by v6; refactoring to shared-base + byte-copy
  without an execution to validate it risks the 24 oracles. Proposed as
  follow-up only if root judges the ~2.5 h suite cost unacceptable.
- v7 timeout proposed at 14400 s (≈24 methods × v6 pace + margin).

## Proposed final checks (for root selection; NOT started)

1. Root reviews this diff + both DRAFTs.
2. On approval: execute the v7 runner as-written (single launch,
   streaming exclusive files, ~2.5 h); then one cheap single-method
   `-O` smoke on final code (mirroring v1/v2 pattern, new names).
3. On green: generate `complete-p2r-16path-v3.patch` ( stalemate-free:
   reuse the v2 generator pattern with new names/paths), execute the v3
   proof draft once in a NEW disposable copy, and write the final
   correction2 report. Stop at the Human Commit Point.
