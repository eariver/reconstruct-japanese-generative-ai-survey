# Corrections to the milestone-3 recovery report (independent review CHANGES_REQUIRED)

Date: 2026-10-03T04:56:09Z. Worker: General Co-Worker. Authority:
`../independent-recovery-review.md` (fresh author-independent reviewer,
documentary verdict CHANGES_REQUIRED, correction-only, no retest).
**No tests, diagnostics, recovery, or candidate/archive changes were made for
this packet.** All originals (`report.md`, `manifest.json`, `raw/`, harnesses,
m2 packet) are preserved byte-intact. Commit-body bytes below come from a
read-only `git log` inspection recorded in `commit-body.txt` (same packet).

## R1. Test-method Git classification was wrong — corrected with call sites

`report.md` §1 claimed "methods 1/2/3/5 use no Git subprocesses and no real
Git repos". That sentence is retracted and replaced by:

- **t2/t3 DO invoke Git indirectly through the actual recovered root.**
  Both run with `ROOT = Path(".").resolve()` = the recovered fixture CWD
  (`tests/test_survey_freeze_stage_boundary_v2.py:22,39`) and call
  `stage_validation.validate_stage` →
  `survey_stage_validation_v2.py:624`
  `current_impl = core.repository_commit_sha(repo_root)` (which shells to
  `git rev-parse HEAD`), plus `survey_agent_control_v2.py` checkpoint/advance/
  approve paths calling the same helper at lines **761, 797, 1290, 1345, 2016**.
  The exercised validators therefore bind the real recovered Git DB, not only
  recovered code. This correction strengthens (not weakens) the Git-aware
  proof for the stage path.
- **Selected t4 does NOT bind the recovered index.** It runs the real recovered
  CLI (`_run_cli`, `PYTHONPATH=REPO`, one subcase with cwd=REPO) against
  synthetic manifests from `_direct_fixture()` (temp dirs), proving real CLI
  admission — but `survey_reader_surface_gate_v2.py` contains no
  `repository_commit_sha`/`subprocess`/`ls-files`, and the module's
  `git ls-files (cwd=REPO)` call lives only in
  `_make_env_identity_weekly_fixture()`, used by the *unselected*
  `test_generated_weekly_cli_admission_and_readback`. Git binding for the CLI
  path rests on the closure diagnostic (plus that unexecuted helper), not on t4.
- **t1 and t5 perform no Git invocation.** t1 calls pure dict helpers
  (`public_issue_slug`/`release_identity`; `survey_profiled_freeze_v2.py` has no
  git/subprocess usage). t5 roots its fixture in a temp dir
  (`test_survey_publication_v2.py:17-20`, schema/config files copied in) and
  neither the test module nor the exercised `survey_publication_v2.py` shells
  to git. "t1 simple identity and t5 canonical data fixture, no repo" stands.

## R2. Guards bracket the whole 5-suite, not each method

`run_five.py:101-115` calls `check_identity("before")` once before the method
loop and `check_identity("after")` once after; raw holds only
`raw/five/guards-before.txt` and `raw/five/guards-after.txt` (both
`head=b40de60 tree=6570324 parent=774dd39a tracked_diff_exit=0`, status
`?? scripts/__pycache__/` only). Report language about guarding "every run"
must be read as **suite-level before/after**, not per-method bracketing.
Likewise the per-method `tN.stdout/stderr/exit.txt` logs carry **no embedded
HEAD/hash headers**; method-to-identity binding rests on runner cwd
(= fixture) + suite guards + actual test sources + the before==after
no-change evidence — not on stronger per-test pinning than was recorded.

## R3. Saved `restore.sh` is evidence-only and unsafe for general rerun

The packet `restore.sh` (all versions) has `set -u` only: no `set -e`, no
`set -o pipefail`; `tar` exits are echoed, not asserted; the final
`} 2>&1 | tee script.log` masks inner-command failures as exit 0; there is no
archive-hash gate and no general tar member-type checks beyond the topdir/
traversal/FETCH_HEAD scans. **Explicit DO NOT RERUN** as a general restore
tool: a rerun without manual correction would still emit mismatch/fail text
masked by `tee`. The same evidence-only status applies to the saved
preparation harnesses (overwriting logs / warn-only risks noted in prior
packets). The restored copy's success is proven **not** by any script exit but
by the completed manual correction (empty-remnant `rmdir`, recorded) plus the
later independent checks: identity/tree/parent, `ls-tree` byte-identity,
object/worktree hash inventories, 0 shared inodes, no alternates, inert
origin, and the restored-copy positive diagnostic PASS.

## R4. True preservation gaps (disclosed, not healed)

"All failures fully preserved" overstates the record. Exact gaps:

- The **first tar attempt's stderr** (stale `\n`-suffixed member names) was
  written to `raw/archive-tar.stderr.txt` and then **overwritten by the
  successful retry** (now 0 bytes). The failure is described from observed
  output only; its raw stream was not preserved.
- The **first member-list and sources files** (`archive-members.txt`,
  `archive-sources0.bin` with blank/`\n` entries) were **regenerated in place**;
  the members list now matches the authoritative tar listing, but the original
  defective versions are not retained.
- `restore.sh` **v1 source** (assumed `git/`+`worktree/` subdirs) was
  **overwritten by v2** (corrected `.git`+flat layout); only v1's run outputs
  (`raw/restore-script.log`, `restore-listing.txt`, `restore-extract.*`)
  survive. v2's file-count assertion bug is preserved in `raw/restore2/`; the
  current file carries the corrected recursive-count assertion.
- The two `rmdir` completions (empty pre-restore dest; empty post-restore
  remnant) and the intermediate `stage.tar` removal (hash recorded first in
  `raw/archive-stage.tar.sha256`) were executed with **observed terminal
  output only, no raw files**.
- m2 meta abbreviations (`TGT`, `<message>`) are retained as-is; no transcript
  is reconstructed. Nothing above is invented raw; everything else claimed as
  preserved exists at its cited path.

## R5. Commit-body clarification (supplement C4 corrected)

Supplement C4's phrase "commit body in 17 stdout" is inaccurate:
`m2/raw/17-commit.stdout.txt` holds the commit **subject + diffstat only**.
The body lives in the commit object; read-only inspection
(`git -C <fixture> log --format=%B -1`, recorded in `commit-body.txt`):

> New honest identity directly on real 774dd39a951c9ac3818e83dfffd4c7666efb0a20. Not restored 481dec0/e4 ancestry. No Freeze code changes.

## R6. No operator delete authorization

Nothing in this packet authorizes operators to delete fixture, packet, or
worktree material. Deletions actually performed: empty pre-restore dest dir,
empty post-restore topdir remnant, and the superseded 15.8M intermediate
`stage.tar` (hash preserved) — each recorded above. The observed untracked
`scripts/__pycache__/` was **not** removed. No blanket delete permission is
granted for future runs.
