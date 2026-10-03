# Independent final resolution — DM-001/019 joint Freeze implementation at 222a37e

2026-10-04. Final scoped author-independent resolution; did not author
design/code/tests/corrections. No agents, probes, execution, network, or
code/ref/config mutation. Read-only Git
(`GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file`,
no root overrides) plus `ls`/`tar -tzf`/pack-metadata reads. Read
`final-correction-task.md`, `final-closure-report.md`, and the full
`evidence-final-20261003T145621Z/` packet (10-runs, 20-packaging,
30-restore, 40-diff). Prior reviews
(`independent-implementation-review.md` F1–F5 CHANGES_REQUIRED on 490;
`independent-correction-review.md` runtime BOUNDED_PASS + packaging
CHANGES_REQUIRED G1 on ff) are preserved untouched. This resolves only
the final delta. No whole-candidate adoption; broader seven-point audit
not requested.

## 1. Final identity and paths (re-verified, not transcribed)

- Final candidate **`222a37e9ee2aa96724a491f2c04c2583a86b9650`**,
  tree **`dbabeed5e70d79b51abb09b64666ca9e1d0fd5dd`**,
  parent **`ff6c67f68e12b3093901248219f2de2872e54d73`**,
  live impl DB `/tmp/opencode/jgas-dm001019-impl-20261003T100801Z`
  (`log --format='%H %P' -5` chain, `rev-parse HEAD^{tree}`,
  clean `status --porcelain=v1 --untracked-files=no`).
- Final delta `ff..222` touches 2 paths only
  (`survey_publication_v2.py` +61/−7, test module +68;
  profiled blob `433c6096…` identical at ff and final).
  Public `build_freeze` signature unchanged; `diff --check` clean.
- Restored available-history DB:
  staging `/tmp/opencode/jgas-dm001019-chainrestore-20261003T150500Z/`,
  DB `…/candidate-partial-b40de60` (`.git` present), review ref
  `refs/heads/dm001019-final` → `222a37e`, tree `dbabeed5…`.
  Worktree HEAD stays b40 with the 3 changed paths materialized via
  `git checkout` (by restore design); the *ref* carries the final.

## 2. G2 — no double-close (verified in source + sentinel test)

- `scripts/survey_publication_v2.py:537-558`: after a failed
  `os.close(fd)` the handler performs **no second close**
  (`:541-543` comment + code: straight to `lstat`/`read_bytes`
  verification). The remaining `_close_quietly` calls (`:524`
  fstat-error, `:534` write-error) release a still-open fd — correct
  and distinct, preserved as required.
- Sentinel test
  (`test_close_failure_leaves_unrelated_descriptor_usable`,
  test `:1319-1353`): real-close → immediate sentinel open (may reuse
  the number) → raise; asserts the `close failed but complete
  verified bytes retained` outcome, sentinel still writable via its
  own fd, test closes only its sentinel, then identical retry
  byte-equal + manifest validates. Old code would have closed the
  sentinel. G2 resolved with no global resource framework.

## 3. G3 — Freeze recheck before Manifest (verified)

- `_install_manifest_target` (`:575-624`) rechecks the input snapshot
  (`:581`), then verifies the installed Freeze is still the planned
  regular non-symlink file at planned parents with planned
  bytes **and** hash (`:587-616`: `lstat`, symlink/regular,
  `_check_output_ancestors`, `read_bytes`, byte + `sha256_bytes`
  equality) **before any Manifest parent creation/write** (`:617`).
  Mutated/deleted/replaced Freeze refuses with "retained as found
  without Manifest write", no Manifest created.
- Pair-wrapper text (`:627-656`) distinguishes drift
  ("refused … retained as found", no retry promise — direct half
  proven) from genuine Manifest install failure
  ("retained for identical retry" kept). Drift-branch comment notes
  defensive-only single-threaded reachability — documented, no CAS.
- Proving tests: `test_freeze_output_drift_before_second_install_no_manifest`
  (drifted Freeze → `drift before second install`, no Manifest,
  follow-up pair retry refuses divergent Freeze, still no Manifest)
  plus extended input-drift tests. G3 resolved; error text no longer
  promises valid-Freeze retry for arbitrary drift.

## 4. Prior F1–F5 / root requirements — still pass (spot-reviewed at final)

Nesting refusal (`:351`), `..` rejection (`:114`), consistent
freeze-target threading, `FileExistsError` lstat revalidation,
close-always-raises, PDF in protected set (`:364`), wrapper State
guard/snapshot, single `_write_immutable`, snapshot rechecks, lstat
cleanup, real wrapper-mixed call, legacy-positive, reformat bytes,
Weekly equivalence, workflow env (+`GIT_OPTIONAL_LOCKS=0` G4 taken)
all present at `222a37e`. New delta narrows behavior only (G2/G3).

## 5. Exact-head results — 56, header-bound, no skips, no rerun needed

`10-runs/*.log` all `HEAD=222a37e… PARENT=ff6c67f… STATUS_CLEAN=True
EXIT=0`: new module **36/36**, publication **8/8**, profiled **4/4**,
freeze-stage **8/8** = **56 methods, 0 failures/skips**
(`Ran` + `... ok` counts re-verified). Two new tests vs the earlier
54 (sentinel + output-drift). Earlier 34/54 runs stay their own
evidence. No restored-DB suite rerun (identity/inventory only).

## 6. G1 — archive-chained portable history (fulfilled, supersession honest)

- Enumerated **from Git**: `rev-list --objects b40..222` = **20
  objects** (3 commits + 5 trees + 12 blobs; count from Git, never
  hardcoded). `object-list.txt` (20 lines) and
  `successor-manifest.json` (`chain` 222→ff→490, `chain_base` b40,
  20 `new_objects`, `tree_entry_count: 32153`, 3 file
  modes+blobs+worktree SHAs, patch 166,150 B) match. Pack
  `successor-pack.pack` (46,164 B, explicit IDs) carries all 20.
- Fresh restore (`restore_chain.py`, fail-closed/absent-destination):
  b40 archive hash/size/member/link gates pass, extraction untouched
  (HEAD b40 / tree `65703243…` / shallow `774dd39a…` / clean),
  20-object import, final ref, 3-path + index materialization via
  normal `checkout`. Verified **offline** in `restore-run.log`
  (`RESTORE_RESULT=OK`): real `git log` chain
  `222a37e→ff6c67f→490414c→b40de60→774dd39a9` with per-link parent
  lines, shallow-cutoff == `.git/shallow` == log terminus (cutoff
  **only** at real 774, no manufactured markers), `merge-base
  --is-ancestor`, exact HEAD/tree, 3-path mode/blob/object-worktree
  bytes + index entries, all 20 objects `cat-file -e`, **full
  `ls-tree -r`: 32,153 entries** (matches manifest; independently
  re-verified count here), inert `example.invalid` remotes only (no
  real remotes), no alternates, own object store. Parent missing
  historical blobs stay declared, never fetched.
- Failure honesty: `restore-run-attempt1-remote-gate.log`
  (`RESTORE_RESULT=FAIL` on the over-strict inert-remote gate)
  preserved, gate corrected to reject only real remotes, clean rerun
  OK. Prior 7-object pack/demo kept and clearly superseded, never
  deleted or relabelled. No patch-rebuilt commit identity anywhere
  in this chain.

## 7. Disposition (split as requested)

- **Joint Freeze implementation (runtime + tests) at `222a37e`:
  BOUNDED_PASS** — G2/G3 closed with actual sentinel/drift tests;
  F1–F5 and all correction-task runtime/test requirements hold.
- **Portable available history (G1): BOUNDED_PASS** — 20-object
  `b40..222` pack + fresh parent-archive-chained restore proves the
  exact offline chain `222→ff→490→b40→774(shallow)` with full tree
  and 3-file binding. No dangling-string stand-in, no extra
  shallow, no remotes/sharing.
- **Overall DM-001/019 unit: no open findings.** All review findings
  F1–F5, G1–G3 are resolved at the final candidate.

## 8. Exact limits / not-readiness (carried, unchanged)

Single-threaded reachability notes; read-only-dir test assumes
non-root; Manifest-without-Freeze conservative refusal retained;
Retrospective full flow, DM-003/004/016/017/018/020, build transfer,
findings transport, all-profile/application, Windows/Actions, and
whole-candidate/seven-point audit remain separate and unclaimed.
**Whole candidate NOT_READY** — this BOUNDED_PASS covers only the
DM-001/019 Freeze boundary and its portable available history at
`222a37e`; it is not adoption, Freeze/Release, or production
authority. Human Commit Point owns the next decision.
