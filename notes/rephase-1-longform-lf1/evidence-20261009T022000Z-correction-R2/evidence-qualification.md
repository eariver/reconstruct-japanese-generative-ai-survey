# Closeout evidence qualification (no code/test/suite changes)

2026-10-09. Closeout-only unit: source/tests accepted by independent resolution
and left untouched (no overlay edits, no 31-method rerun). This file plus
`proof-postdrift-v2/` (saved script `prove_postdrift.py`, direct-capture
`capture.log`, `runner-postdrift-v2.log`) are the only additions. Original
proof logs unmodified. No source/candidate/refs writes, no commits, no network,
no subagents. Final bounded source/component acceptance unchanged.

## 1. Masked shell exit in `proof-postdrift-shell.log` (honest defect)

Line 26 of the preserved `proof-postdrift-shell.log` reads
`runner_shell_exit:0`. That `0` is **tee(1)'s exit status, not the runner's**:
the command was `python3 …/run_evidence.py … 2>&1 | tee -a shell.log; echo
"runner_shell_exit:$?"`, and in a shell pipeline `$?` is the LAST command's
status (tee), which is 0 whenever tee writes successfully. It evidences
nothing about the runner's exit and must not be cited as a numeric guard proof.

## 2. Exact provenance of the appended `RUNNER_EXIT:3` (observed vs reconstructed)

Line 43 reads `RUNNER_EXIT:3 (child_exit=0, postguard=FAILED → exit 3)`. The
digit `3` was **directly observed, not invented**: it came from a repeated
runner invocation issued as `python3 …/run_evidence.py … 2>/tmp/proof3-stderr.txt`
followed by `echo "RUNNER_EXIT:$?"` with NO pipe, so `$?` was the runner
process's own exit status, and the shell printed `RUNNER_EXIT:3`. However:

- it is a DIFFERENT process invocation from the one whose transcript fills
  lines 24–41 of the shell log (that first transcript's own exit was the
  masked `0` above);
- the second invocation also overwrote `proof-postdrift.log`, so the preserved
  `proof-postdrift.log` is the second run's transcript, not the first's;
- the shell log therefore contains NO single unbroken executable capture
  binding one exact argv to its exit code — the `3` is an observed digit
  inside a reconstructed narrative.

That gap is genuine and is closed by the v2 proof below, not by rewording.

## 3. v2 post-drift proof (direct returncode capture, saved script)

`proof-postdrift-v2/prove_postdrift.py` performs the whole proof with
`subprocess.run` and records `.returncode` directly — no shell pipe anywhere
in the capture path. In a NEW disposable independent copy
(`/tmp/opencode/jgas-lf1-proof-disposable-v2-20261009T025927Z`, byte-copy of
the candidate; the v1 disposable was already removed, never reused) it verifies
HEAD/tree/exact-status/inert origin/no alternates/no hardlinks/zero shared
object inodes, then runs the UNMODIFIED final `run_evidence.py` (pinned hashes)
with `--dst <disposable> --proof-postdrift-file drift-canary-proof-v2.json`
and exactly one fast pure-test child
(`…LongformDerivationV2Tests.test_pure_policy_boundaries_without_chain`; full
suite untouched). `capture.log` preserves the exact argv, the runner's
stdout/stderr, and `returncode=3`, plus `OUTCOME=POSTGUARD_FAILED` with
`unittest_exit:0` in `runner-postdrift-v2.log`. Candidate status verified
identical pre/post with no canary; disposable removed after. Script exit 0
(`SCRIPT_EXIT:0`) required runner exit exactly 3 AND candidate unchanged.

## 4. Claim-scope clarifications (accepted wording bounds)

- **Alias sentinel:** `test_results_dir_alias_refuses_before_read` writes
  `'{"malformed": true}'` outside the fixture tree. That is VALID JSON but NOT
  an Evidence card; the test's force is the pre-validator directory-alias
  refusal plus spies proving the real validator NEVER ran and the sentinel was
  NEVER read (byte-identical after). It is not a malformed-JSON parser trap —
  had the loader run, `core.load_json` would have parsed it without error.
- **Derived style mutation:** schema-only evidence — a mutated
  `edition_descriptor` is refused by `validate_longform_reader_input` const
  validation, not by any renderer/style engine.
- **Kicker:** `_kicker` ordinal/total/suffix assertions are helper-level unit
  checks, not an independent renderer probe; loader-level kicker order is
  covered by the two-package chain test.
- **Multi-DID unconstructible:** observed over the fixture-producer family used
  here (per-task single-DID cards), not a universal theorem about producers;
  DID-uniqueness loader evidence is the duplicate-card shape check plus the
  ambiguity/equal-timestamp resolver pair.

## 4b. Pure HOLD / NEEDS_MORE classification (unchanged, restated)

Pure mutated-HOLD (`test_held_back_cite_refuses_at_projection`) is
PROJECTOR-level pure-build evidence, not a loader negative; `NEEDS_MORE`
fixture BLOCKED is UPSTREAM-readiness evidence only. No loader negative is
claimed for either.

## 5. Preserved final identity (restated, unchanged)

Basis HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree
`8ce3699861505f32d1d60bdc185d4d4f635aedb2`; overlay runtime
`233e86557f1627203a4f1e4129c953bf34e1319bd8949b1d58b7d417b0744cf7`,
schema `7bae9d2ac753c83521165c76c9e461ce40ac4e704d9b44d3518ae7b88fbd0643`,
tests `ce687447539a99eb92532bc34246a271fb489b259e63b31ed6699fcc12fbf913`.
Candidate still exactly three `??`, zero tracked mods (verified pre/post v2
proof). Final bounded source/component acceptance unchanged.
