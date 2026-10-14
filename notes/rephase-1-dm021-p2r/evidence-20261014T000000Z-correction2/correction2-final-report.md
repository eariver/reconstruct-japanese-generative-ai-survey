# Correction2 final report — implementation/test return (no adoption)

2026-10-14. Executed exactly per
`notes/rephase-1-dm021-p2r/correction2-execution-selection.md`. This is an
implementation + test-execution return only. No independent or root PASS
is claimed; R2 status stays CHANGES_REQUIRED until root and
author-independent review of this evidence. No commits/branches/network,
no P1 modifications (all13 re-verified vs the P1 freeze pre AND post),
no adoption, no next-unit work, no active cleanup (84 preexisting
candidate caches remain).

## 1. Final source pins (candidate `/tmp/opencode/jgas-dm021p2r-impl-20261013T123807Z/candidate-partial-b40de60`)

- module `scripts/survey_editorial_retention_v2.py`
  `3833b14a281ab82999410d91361d5aace3c77015484e621c62077e480b73f5b2`,
  122231 bytes, `0o664`, 2080 lines.
- test `tests/test_survey_editorial_retention_v2.py`
  `4155baab733e8bddc0b7cbc34b83fe801def2927a716d43132321f8f083d614e`,
  93733 bytes, `0o664`, 1802 lines, 25 methods.
- schema `schemas/editorial-retention-manifest-v2.schema.json`
  `347e5499259ac878e28bc66b4e9ea62af1f5eb71a3f428558120a9f5d549855c`
  (unchanged since initial).
- Immutable metadata in reconstruct: `expected16-correction2c.json`
  (final 16), `inherited13-static-freeze.json` (P1-authoritative 13),
  `cache-inventory-static.json` (84 preknown residue), durable pre-edit
  v6 bytes `preedit-v6-module-77ee2a3e.py` / `preedit-v6-test-22f56041.py`
  / `preedit-v6-schema-347e5499.json` (byte-copied from the verified /tmp
  snapshot, hashes re-verified, not reconstructed).
- Final complete patch `complete-p2r-16path-v3.patch`, 830622 bytes,
  sha256 `5b79218e3c90fc8bcb11e39571e2ab1e8dfc52e04f5e98843937e4e876515208`,
  with saved hash manifest `complete-p2r-16path-v3.sha256` (compared, not
  merely printed, by the proof).

## 2. Active + apply copy (proof v7, exit 0)

- Active at proof: HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree
  `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, index empty, all16 match
  static correction2c; whole-`.git` separation (134 regular + 96 dirs
  each side, zero problems incl. nlink==1 enforced, zero shared
  (dev,ino) pairs); exact inert remote pair + exact inert config URLs
  with whole outputs persisted (active once, copy pre- and post-apply).
- Disposable copy `/tmp/opencode/jgas-dm021p2r-verify-20261014T000007Z/candidate-partial-b40de60`:
  post-copy completeness (all16 byte-equal), clean409 verified (13 NEW
  absent + 3 MODIFIED byte-equal `git show HEAD:` + empty status/index),
  declared cache removals only (84 inventoried), `apply --check` + `apply`
  rc 0, applied HEAD/tree/index pinned, applied 16 match static manifest,
  applied status exactly `3M13A`. `APPLY_PROOF_OK`, exit 0.
- Scripts executed (each once, never edited after execution, never
  re-executed): `run_p2r_correction_v8.py.READY` (hash `203ce5f6…`, ran
  23/25), `run_affected_c2c_v1.py` (2/2), `run_p2r_correction_v9.py.READY`
  (hash `e890cbab…`, ran 25/25), `run_opt_correction_v3.py` (1/1),
  `gen_16patch_v3.py` (patch+manifest), `proof_apply16_v7.py.READY`
  (proof exit 0). Superseded/failed versions preserved with raw:
  v3b/v4/v5/v6 proofs (exit 40; see §5), v7 runner DRAFT+READY (unexecuted).

## 3. Method/subcase coverage (final pins, 25 methods)

Positives: longform, weekly, r1-double (2 captures + cross-proposal
refusal). Existing-root refusal (empty/same-byte/alias + no-write).
Unsafe paths (5 lexical + leaf-alias + FIFO guard). Typed hops (7
coordinated subcases: missing/duplicate state-authority, disagreeing
state_ref, ambiguous KEEP, omitted/extra/duplicate rows). Bind matrix
(wrong COPY hash, missing dep, moved unplanted/provisional, moved planted
+ fd-chain no-read proof, dep-hash-tolerated success, bad size, extra
empty dir). Staged/canonical (reversed rows/roles, KEEP-extra-field, dup
inputs, noncanonical bytes; all with immediate no-write). X-vs-required
KEEP distinction with distinct-identity asserts. Persistence (live-State
swap verifies; retained/staged/cross-proposal drift refuse). Post-capture
P1 refusal + no-P1/Git verifier proof. Faults: short-write-loop success +
zero-progress + fsync; manifest write/zero/fsync/close all
`INDETERMINATE_INVOCATION` with distinct codes; combined write+close with
primary preserved. Replacements: root swap, ancestor swap, owned-file
mid-capture swap, post-verify same-inode same-size edit (NEW), verifier
file/inventory case. State labels (missing/disagreeing via coordinated
triple mutation, NEW). Late retained file/dir at the final boundary with
`"final retained"` proof (NEW). Control/edition injections inside the
standalone-readback window (NEW). Creation-identity failure with zero
tracked writes (NEW). Primary-read + intermediate-close preservation with
attached secondaries (NEW). Pre-final drift; control/edition/HEAD drift.

## 4. Exact runtimes / counts

- v8 (`run_p2r_correction_v8.py.READY`, child 2715472/own group, `-u`,
  forced 5 keys + 28 redacted): `Ran 25 tests in 7786.576s`: 23 ok,
  2 failures (below); child_rc=1, wrapper 1, post guards clean.
- Affected (`run_affected_c2c_v1.py`, child 2741839): `Ran 2 tests in
  440.248s OK`, exit 0, post guards clean.
- v9 (`run_p2r_correction_v9.py.READY`, child 2744108/own group, `-u`,
  forced 5 keys + 28 redacted): `Ran 25 tests in 7936.817s OK`
  (7938.5 s wall), child_rc=0, wrapper 0, post guards clean.
- `-O` smoke (`run_opt_correction_v3.py`, isolated, guarded): `Ran 1
  test in 250.016s OK`, exit 0. Full-suite `-O` unproved (unchanged
  bounded limit; new code uses explicit raises only).
- Proof v7: exit 0 (above). No duplicate processes at any launch or now;
  PIDs/logs: v8 child 2715472, affected 2741839, v9 child 2744108; child
  logs streamed to exclusive durable files during each run.

## 5. Failures (all preserved; oracles never loosened)

- v8 `test_fault_primary_read_close_secondary_preserved`: global
  close-failure mock killed the first read's normal close
  (`CLOSE_FAILED` at the Production State read; secondaries correctly
  attached by the new `_close_all`). Test-mechanics defect: close
  failures now arm only at the proposal-leaf open. Fixed, affected-proven,
  full-green in v9 (same expectation codes).
- v8 `test_verifier_late_retained_additions_refuse`: strict pre/post
  equality counted the test's own mid-call plant as verifier output.
  Test-mechanics defect: plant removed before the strict compare (which
  then proves the verifier wrote nothing else). Fixed, affected-proven,
  full-green in v9.
- Proof v3b/v4/v5 (exit 40, all preserved with raw + anomalous copies
  `...000002Z/000004Z/000005Z`): root-caused, NOT environmental. The E2
  rewrite's `freeze(COPYREPO)` read all 16 paths AFTER the unlink loop
  deleted the 13 NEW files; the `FileNotFoundError` came from the generic
  OSError handler, never from the unlink path's own message — the
  telltale misread that sent the ghost investigation (sparse/timers/
  stray-process/cp-loop/symlink audits, bisect + monitored repros, all
  clean) off course. The v6 `strace -f -e trace=%file` log
  (`proof_apply16_v6.strace.log`) is decisive: `cp` created the files,
  canary stats succeeded, the proof's own unlink loop deleted all 13
  (rc 0), and the later `openat` (freeze's read) hit ENOENT. v7 replaces
  the clean-state freeze with explicit revert observation; v7 green.
  The anomaly record file stands as history with this correction; probe
  scratch dirs (`mon-probe`, `bisect-probe`, `cp-loop-*`) disclosed.
- v5 interruption (prior unit) and v6 runner buffering/overclaim notes
  preserved as history; v8/v9 use `-u` direct redirect.

## 6. Strict attribution + limitations

- Roles: correction implementation + test execution by the General
  worker (this return); root reviewer; author-independent review PENDING.
  The prior independent blanket R1–R6 resolution was found overstated by
  root R2 (independent-correction-resolution.md is historical, not
  closure). Nothing here claims independent or root PASS.
- Accidentally deleted/restored UNEXECUTED `proof_apply16_v3.py.DRAFT`
  (ready-revision-notes.md): restored from transcript, parses, not
  byte-certified; READY files operative; DRAFT reference-only.
- Mechanical file versioning for v9/proof-READY2 used a python
  file-write instead of the specialized Write tool (functionally
  verified by AST + grep + execution; disclosed per tool-availability
  reporting).
- Bounded limits carried forward: snapshot equality is not continuous
  no-drift/global-CAS/crash-atomicity; synthetic accepted-chain fixtures
  are not genuine approvals or current-eligibility proof; capture_inputs
  are historical observations; same-byte identity continuity without a
  baseline is beyond a fresh standalone verifier (capture-time oracles
  prove it instead); full-suite `-O`, all-profile publication, Windows/
  Actions, net savings, canonical audit remain open per standing scope.
- Secrets audit: packet holds only the 5 forced Git/Python/runtime keys
  plus redaction counts in stage/meta records (`env_git: {}`); no full
  env dumps, no tokens (verified by grep). A process-listing this turn
  incidentally displayed an unrelated Minecraft token to the operator
  only; it was never written to any file (verified absent).
