# Independent correction review — DM-001/019 correction ff6c67f (parent 490414c)

2026-10-03. Fresh author-independent correction reviewer; did not author
design/code/tests/corrections. No agents spawned. No test/probe execution,
network, checkout, ref or config mutation. Read-only Git with
`GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file`
(no root overrides); source-read plus `ls`/`tar -tzf`/pack-metadata
listing only. Read `correction-task.md`, `correction-report.md`, and
`evidence-corr-20261003T110500Z/` (10-runs headers, 20-packaging,
30-restore, 40-correction). Original
`independent-implementation-review.md` (F1–F5, CHANGES_REQUIRED on
`490414c`) is preserved untouched; this file resolves only the
correction delta at `ff6c67f`. No whole-candidate adoption.

## 1. Candidate binding

- **`ff6c67f68e12b3093901248219f2de2872e54d73`**,
  tree **`664c796da983f322f1d244500d8b9b88198b772a`**,
  direct parent **`490414cef5be71d3b373171d8abeb0674b1f1c71`**
  (b40 ancestry intact; `log --format='%H %P'`, `rev-parse HEAD^{tree}`,
  clean `status --porcelain=v1 --untracked-files=no` re-verified in
  `/tmp/opencode/jgas-dm001019-impl-20261003T100801Z`).
- Same 3-path budget, `diff --stat 490..ff`: publication 238 lines,
  profiled 20, test module +439 (now 1731 lines, 34 methods).
  Blobs `30a42fee… / 433c6096… / 4f49114c…` match manifest worktree SHAs.
  Public `build_freeze` signature unchanged (candidate `:872-879`).
  `git diff --check` clean per report; single `_write_immutable`
  (`:65-71`) — F5 duplicate gone.

## 2. Original F1–F5 + root new requirements — resolved (runtime)

- **F1 nested/dotdot/consistent-target:** `parents` ancestry refusal
  (`survey_publication_v2.py:349-353`, both directions, pre-mkdir);
  lexical `..` rejected before `normpath` (`:113-114`); manifest
  builder receives `(freeze_sha, norm_freeze)` (`:412`, `:901-903`) so
  payload refs and install share one target. Proving test
  `test_l9_nested_and_dotdot_outputs_rejected_pre_write` (both
  nestings + dotdot, no target/parent created). PASS on the code.
- **F2 collision revalidation:** `FileExistsError` branch does
  `lstat`/symlink/regular/ancestor rechecks before `read_bytes`
  (`:503-511`); FIFO refused without blocking (mocked-collision
  unit, no `read_bytes` on special files); post-`mkdir` ancestor
  recheck (`:436-438`, cheap narrowing, no global claim). Proving
  tests `test_fileexists_symlink_identical_bytes_refused`,
  `test_fileexists_fifo_refused_without_blocking`. PASS.
- **F3 close propagation:** close failure always raises (freeze
  `:537-558`, manifest via retained wrapper); verified-complete
  bytes retained with explicit `close failed but complete verified
  bytes retained for identical retry` + safe retry byte-equal.
  Real-close-then-raise injection (real `os.close` first, then raise;
  no leaked fd in test path). Proving tests
  `test_close_failure_never_reports_success`,
  `test_manifest_close_failure_retains_freeze`. PASS, subject to G2
  below (retry-after-failed-close hardening).
- **F4 PDF alias + wrapper State:** `candidate["pdf"]` in protected
  set (`:359-369`, spelling + inode); wrapper guards fixed outputs
  against the State path and merges State bytes into the snapshot
  (`survey_profiled_freeze_v2.py:79-83,113`). Direct overlap
  untriggerable via fixed paths — documented honestly, acceptable.
  Alias refusal is pre-write, not incidental JSON refusal. PASS.
- **F5 duplicate + narrow API:** duplicate deleted; helpers
  privatized (`_prepare/_build/_preflight/_install_*`); slug
  authority stays the single public pair; no new unvalidated
  tag-write API (`release_identity(str,str)` retained legacy,
  builders never call it). Publication 8/8 + profiled 4/4 green.
  PASS.
- **Item 6 snapshot/recheck:** 9-file authority snapshot at prepare
  (`:213-229`), `_recheck_snapshot` before preflight return
  (`:429`), before first write (`:567`), before second install
  (`:581`); split `_install_freeze_target/_install_manifest_target`.
  Drift-before-first (no outputs) and drift-before-second (Freeze
  retained, no Manifest) proven. PASS, subject to G3 below.
- **Item 7 lstat cleanup:** `_remove_owned_partial` uses `lstat`
  (`:451`), explicit symlink (`:456-459`), identity-change and
  non-prefix preservation, foreign residual never deleted. Three
  owned-partial units green. PASS.
- **Wrapper mixed real call (`test_w4c`, test `:1550-1580`):**
  TRUE wrapper invocation confirmed —
  `profiled.build_profiled_freeze(ROOT, fix.cfg, state_file, …)`
  (`:1572`), with real valid State + approved C1 and independently
  valid C2 (same PDF) installed at the fixed wrapper path. Result is
  the honest earlier State-provenance refusal
  (`invalid before Freeze` — swapped Candidate breaks
  checkpoint-bound State validity), with State bytes
  before/after-equal, no outputs, recorded-C1/installed-C2/approval
  intact. Lower-level exact-Candidate refusal kept (L4/W4b prepare
  level). Acceptable under the task's "exact rejection (or
  demonstrably earlier real-State refusal … with concrete
  explanation)" clause. No finding; record that the wrapper
  exact-Candidate gate is proven at prepare level, not reached via
  the full wrapper path — inherent to valid-State construction,
  disclosed in-test (`:1573-1575`).
- **Legacy positive (`test_w1c`):** alt-path canonical VISUAL +
  valid legacy at hardcoded path; both builders succeed byte-equal,
  legacy untouched, frozen visual path is the alt path. Directly
  complements parent W1b. PASS.
- **Reformat bytes (L10/W7), Weekly equivalence (W2b), no-write
  snapshots (`_snap_state_targets`), workflow env
  (`GIT_NO_LAZY_FETCH/ALLOW_PROTOCOL` at test `:713-714`):** all
  present and header-bound. 34/34 new + 8/8 + 4/4 + 8/8 = **54
  methods, EXIT 0 in all four `10-runs/*.log` with
  HEAD/tree/parent/`STATUS_CLEAN`/source-hash/argv/env headers at
  `ff6c67f`** (34/8/4/8 `... ok` counts and `Ran` lines
  re-verified). PASS.

**Independent runtime disposition: BOUNDED_PASS** — every
CHANGES_REQUIRED runtime item from the original review plus every
`correction-task.md` runtime/test requirement is resolved at `ff6c67f`
within DM-001/019 scope. No new broad CAS/lock/atomicity claimed.

## 3. New minimal runtime findings (do not reopen F1–F5)

### G2 [LOW] Best-effort `close` retry after failed `os.close` is unsafe in principle
- **Where:** `survey_publication_v2.py:539-543`
  (`except OSError … _close_quietly(fd)` after `os.close(fd)` raised).
  The `_close_quietly` calls after *write* (`:534`) and *fstat*
  (`:524`) failures are correct (fd still open) — keep those.
- **Issue:** POSIX leaves fd state unspecified after a failed
  `close` — it may already be closed. A second `close` is `EBADF`
  (harmless, single-threaded test path) but in a threaded host the
  fd number may already be reused, and the retry would close an
  unrelated descriptor. Do not assume retry-safe.
- **Fix (one line, no CAS):** delete the `_close_quietly(fd)` in the
  close-exception handler only; treat the descriptor as closed and
  proceed to `lstat`/`read_bytes` verification. Tests (real-close
  then raise) still pass; production no longer risks closing a
  recycled fd.

### G3 [LOW-MEDIUM] Freeze bytes not rechecked before Manifest install
- **Where:** `_install_manifest_target` (`:575-589`): rechecks the
  *input* snapshot (`:581`) but never verifies the just-installed
  Freeze output still equals planned `_freeze_bytes` before writing
  the Manifest. Post-install Manifest check (`:584`) and final
  `validate_release_manifest` catch drift only *after* a stale
  Manifest is written.
- **Selected rule (`correction-task.md` item 6):** "Verify outputs
  against the planned bytes … later drift must fail explicitly under
  the declared partial-state rule." The Freeze output is part of the
  plan and should be verified pre-second-install.
- **Fix (cheap, no history machinery):** after `:581`, add
  `if norm_freeze.read_bytes() != _freeze_bytes: raise ValueError(
  "Freeze record changed before second install; completed Freeze
  retained …")` — no Manifest write on Freeze drift.
- **Proposed test:** install Freeze via `_install_freeze_target`,
  mutate Freeze bytes (fixture-owned), call
  `_install_manifest_target`, assert refusal with Manifest absent
  (current code installs a stale Manifest then fails validation).

(G4 nit, advisory only: workflow subprocess env adds
`GIT_NO_LAZY_FETCH`/`GIT_ALLOW_PROTOCOL` but not
`GIT_OPTIONAL_LOCKS` — runner env has all three. Harmless if the
predicate block performs no Git writes; align for consistency.)

## 4. Packaging — NOT fulfilled (root-spotted, independently confirmed)

- **Enumerated reality:** `rev-list --objects b40..ff` = **14 objects**;
  `20-packaging/object-list.txt` + `successor-manifest.json:26-54`
  enumerate only **`490..ff` = 7** (commit/tree/2 subtrees/3 blobs of
  the correction). The 7 objects of `490414c` (commit, `f5009749…`
  tree, scripts/tests subtrees, 3 blobs) are **not** in
  `successor-pack.pack` (42,089 B) and live only in the volatile
  impl DB. The b40 partial archive
  (`candidate-partial-b40de60.tar.gz`, 5.0 MiB, 760 entries) holds
  b40 content, not 490's objects.
- **Consequence:** "b40 archive + ff pack" cannot materialize the
  exact available chain `b40 → 490 → ff`. The restore demo
  (`30-restore/restore_successor.py` → empty DB, non-strict
  `unpack-objects`, `update-ref` to `ff`) passes its 7-object +
  3-blob + header-string gates (`restore-run.log: RESTORE_RESULT=OK`)
  but leaves dangling parent links: `490414c` commit/tree/blobs
  absent, full `ls-tree -r`/`git log`/`fsck` over the available
  chain impossible. Report §5 calls `cannot git log` "by design"
  (`correction-report.md:79-80`) and §6 labels the artifact
  "patch+object delta, not a full backup" — the label is honest,
  but `correction-task.md:29` explicitly required the **b40..final
  enumerated pack** (or ≤50 MiB partial-DB snapshot) **plus**
  verification of the exact available chain *against the existing
  partial parent archive*. That requirement is unmet.
- **Required:** pack `rev-list --objects b40..ff` (14 objects, still
  small, no history hydration beyond the enumerated set); restore
  procedure: extract the existing b40 partial archive to a new
  absent dir + unpack the 14-object pack (fail-closed, no old
  scripts) + verify `rev-parse` HEAD/tree, `cat-file commit` parent
  chain `ff→490→b40`, `cat-file -e` all 14, `ls-tree HEAD` 3-path
  blobs + `changed-files/` byte equality, no remotes/alternates,
  fresh inodes. Preserve the strict-attempt failure log; do not
  overwrite `restore-run-attempt1-strict-linkage.log`.

**Independent packaging disposition: CHANGES_REQUIRED (G1).**
G1 blocks any durable-restore claim; it does not reflect on runtime
correctness.

## 5. Verdict (split, actionable)

- **Runtime (F1–F5 + all correction-task runtime/test items):
  BOUNDED_PASS** at `ff6c67f`, contingent on nothing further except
  the two small hardening items G2/G3 (recommended in the next
  correction, not a reopen of F1–F5).
- **Packaging/restore (G1): CHANGES_REQUIRED** — new 14-object
  `b40..ff` pack + archive-chained restore verification required.
- **Overall correction unit: CHANGES_REQUIRED (packaging only).**
  Worker corrections belong in a new separate candidate; this review
  stays fixed to `ff6c67f` and must not be relabelled. Whole
  candidate remains NOT_READY; no next unit before the Human Commit
  Point. Root owns the follow-up correction task.
