# DM021-P1 correction4 closeout evidence qualification (2026-10-12T121721Z)

Closeout-only verification. NO source/test edits, NO suite rerun, NO historical-script
rerun, NO DB writes/recopy/checkout/generation/index, NO network/subagents/commits/tests.
Historical `run_final.py` / `proof_apply.py` were READ only (not executed here).
New evidence is `closeout-20261012T121721Z/verify_current.py` (NEW read-only script)
+ exclusive `verify-current.raw.log` + `verify-current.json`, run once.

## 1. What was verified (current-state only)

- Saved `freeze-pre.json == freeze-post.json` full (HEAD/tree/status/files identical);
  saved full raw status is exact 13 rows (3M10A), `sorted(splitlines)==EXPECTED_ROWS`.
- Saved `proof-freeze-applied.json` files/status == `freeze-pre` files/status;
  `proof-freeze-clean.json` is clean409 HEAD/tree with empty status.
- CURRENT (2026-10-12T121721Z) ACTIVE
  `/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z/candidate-partial-b40de60`
  and COPY `/tmp/opencode/jgas-dm021p1-R2-verify-20261012T072355Z/candidate-partial-b40de60`:
  HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`,
  tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`,
  full raw `status --porcelain` == saved freeze-pre status (673 bytes, exact 13),
  `diff --cached --name-only` empty (no index intent), all 13 hashes/modes/bytes
  == freeze-pre, no alternates, inert remotes (`example.invalid`).
- Full `.git` separation CURRENT: ACTIVE 134 files / COPY 134 files / workspace 1075 files;
  0 symlinks in ACTIVE/COPY, 0 `nlink>1` in ACTIVE/COPY, shared `(dev,ino)` counts
  ACTIVE&COPY=0, ACTIVE&workspace=0, COPY&workspace=0 (entire `.git` walked, not just HEAD).
  Workspace HEAD `ab17af4211b04eaff4781ef104631bcd56a66085` distinct; workspace status
  is only `?? notes/rephase-1-dm021-p1/` (this closeout evidence itself).
- Patch `complete-p1-correction-13path.patch` 604448 bytes, SHA256
  `85e9d9ab3c972a786afb1cf2f941bf4dbcfd4980f2e63d0ad9cf6df3cb55963c`,
  13 `diff --git`, base HEAD409/tree8ce header. Verdict `CLOSEOUT_CURRENT_MATCH`.
- Restore+apply availability CURRENT: ACTIVE exists (readable, HEAD409) and COPY exists
  (readable, HEAD409, applied state == freeze-pre). No restoration was executed here;
  availability is current-read proof, not a new restore.

## 2. Residual claim issues (root) — qualified, not certified beyond current

- `run_final.named_status` (lines 100-108) FILTERS to expected 13; it does not reject
  unrelated status rows. Extra rows would be silently ignored. Actual saved raw status
  is currently exact 13, and this closeout compares FULL raw pre/post/CURRENT
  (pre==post full, CURRENT==freeze-pre full). Closed reject predicate is NOT certified;
  only full-raw equality at these pins is verified.
- Pins are capture-at-run pre vs post, not independent static preknown hashes.
  CURRENT 13 match proves no drift since the run; it is not retroactive per-run proof
  and not a static baseline certificate.
- `proof_apply.py` object-separation compared only `.git/HEAD` inode (lines 69-74).
  That narrow check is insufficient for full separation. This closeout verifies CURRENT
  all-object `(dev,ino)`/nlink/symlink/no-alternates/inert-remotes plus source13/copy13
  hash+mode and actual HEAD/tree/status/index-empty. It does not retroactively repair
  the prior narrow claim; prior evidence keeps its original narrow scope.

## 3. Known metadata / history qualifications

- Stale `R2` labels are cosmetic only: patch line 1
  `DM021-P1 R2 correction overlay`, `proof_apply.py` docstring `(R2)` and COPYROOT
  `...R2-verify...`, `gen_correction_patch.py` docstring `(R2)` and GENROOT `...R2-gen...`.
  Base HEAD/tree/content verified as correction4 pins above; label does not change bytes.
- Prior `add -N` + reset occurred ONLY in disposable gen/verify copies
  (`gen_correction_patch.py` THERE, `proof_apply.py` checkout/unlink THERE);
  ACTIVE `diff --cached --name-only` is currently empty and HEAD remains actual409.
  No candidate commit/branch was created; stop remains at Human Commit Point.
- D1 outside-raw seam (`d1-outside-raw-scope`, test 1608-1672 per independent resolution)
  is PRE-CALL staleness: clean snapshot, mutate outside-tree raw, assert injected-only
  delta, then call `validate_proposal(..., scope)` expecting refusal. It is not a
  late-in-call concurrent mutation after scope. Late-in-call stability remains covered
  by C3 seams + `reverify()` per resolution §2. Classification recorded, not a defect.
- Broad old PASS overclaims are withdrawn to the extent stated in
  `independent-final-resolution.md §0`: prior correction3 completeness PASS (missing
  `x_source_intake`/`raw_refs`/X-manifest locals) and prior `run_correction.py`
  fail-closed/exclusive/no-cleanup language. This closeout verifies only correction4
  D1/E1 at pins §1 with 36-method + apply-proof scope; old runs keep their own scope,
  no count transfer.
- Final 36 (`Ran 36 tests in 3308.284s OK`, 9 P1 + 27 Gate, `run.exit=exit=0`,
  `proof-apply.exit=exit=0`) is exact-run evidence at frozen pins only, not a generic
  certificate. No new runner and no 36 re-execution was needed here because CURRENT
  source/tests 13 match freeze-pre exactly (see §1); source component verdict is for
  root later. Whole NOT_READY, DM021 OPEN, Commit/Push Human-owned.
