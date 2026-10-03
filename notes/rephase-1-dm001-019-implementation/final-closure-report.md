# DM-001/019 final closure — G2/G3 + archive-chained restoration

2026-10-04 (UTC 2026-10-03 late). Final bounded correction per
`final-correction-task.md`; independent correction review confirmed main
fixes at ff6c67f with packaging CHANGES_REQUIRED (G1) plus runtime notes
G2/G3. `b40/490414c/ff6c67f` and all prior evidence preserved. No agents,
Production, network, reconstruct Commit/Push, parent-witness rerun, or
new backlog.

## 1. Final candidate

- **`222a37e9ee2aa96724a491f2c04c2583a86b9650`**,
  tree **`dbabeed5e70d79b51abb09b64666ca9e1d0fd5dd`**,
  parent **`ff6c67f68e12b3093901248219f2de2872e54d73`**,
  chain `222a37e → ff6c67f → 490414c → b40de60 → 774dd39a`
  (shallow cutoff at 774 only; no manufactured markers).
- Same budget paths (profiled untouched this round):
  `scripts/survey_publication_v2.py` (+61/−7 region),
  `tests/test_survey_dm001_019_freeze_equivalence_v2.py` (+68).
  Public `build_freeze` signature unchanged; `git diff --check` clean.

## 2. G2/G3 matrix

- **G2:** removed the second `os.close` after a failed close (fd state
  unspecified; numeric reuse could close an unrelated descriptor). Kept
  the correct release attempts after fstat/write errors. Proven by the
  new sentinel test: real close, immediate sentinel open (may reuse the
  number), raise — sentinel stays writable, test closes only its own
  descriptor. Old code would have closed the sentinel.
- **G3:** `_install_manifest_target` now verifies the installed Freeze is
  still the planned regular file at planned parents with planned
  bytes/hash before any Manifest write. Mutated/deleted/replaced Freeze
  refuses with the Freeze retained as found and no Manifest. Pair-wrapper
  text distinguishes drift ("retained as found", no retry promise, direct
  half proven) from genuine install failure (retained-for-retry promise
  kept). Proven by output-drift injection (direct half + pair-divergent
  reinstall refusal) and the extended input-drift test.
- **G4 (advisory, taken):** workflow env adds `GIT_OPTIONAL_LOCKS=0`.

## 3. Final exact-head results

Header-bound logs (`evidence-final-20261003T145621Z/10-runs/`, all
`STATUS_CLEAN=True` at `222a37e`): new module **36/36 OK** (2 new tests),
publication 8/8, profiled 4/4, freeze-stage 8/8 — **56 methods, 0 skips**.
Earlier 54- связка stays its own evidence. No restored-DB suite rerun.

## 4. Packaging G1 — archive-chained restoration (supersedes 7-object demo)

- **Enumerated from Git:** `rev-list --objects b40..FINAL` = **20 objects**
  (3 commits + 5 trees + 12 blobs across 490/ff/FINAL; count from Git,
  never hardcoded). `successor-pack.pack` (46,164 B, explicit IDs,
  `--no-reuse-delta --no-reuse-object`, no lazy fetch) + machine
  `successor-manifest.json` (HEAD/tree/parent, chain, base,
  `tree_entry_count: 32153`, 3 file modes+blobs+worktree SHAs, patch
  166,150 B) + blob-verified `changed-files/` copies. Prior 7-object
  pack/demo kept, clearly superseded (not deleted, not rerun).
- **Fresh restore** (`30-restore/restore_chain.py`, fail-closed,
  absent-destination gate, archive hash/size/member/link gates):
  hash-validated b40 archive extracted untouched (HEAD b40/tree
  `65703243…`/shallow `774dd39a…`/clean), 20-object pack imported, final
  ref established, 3 paths + index materialized via `git checkout`.
- **Verified offline:** real `git log` chain
  `222a37e→ff6c67f→490414c→b40de60→774dd39a9`; per-link parent lines;
  shallow-cutoff check (base parents == shallow file == log terminus);
  `merge-base --is-ancestor`; exact HEAD/tree; 3-path mode/blob/object-
  worktree bytes + index entries; all 20 objects present; **full
  `ls-tree -r`: 32,153 entries** (matches generated count);
  inert-placeholder remotes only (no real remotes), no alternates, own
  object store. Parent missing historical blobs stay declared, never
  fetched. `index-pack --strict` unsuitability for the delta (dangling
  parent links) disclosed via the preserved strict-attempt failure, not
  relabelled.
- First attempt failed one over-strict gate (inert remote treated as
  real); preserved as `restore-run-attempt1-remote-gate.log`, gate
  corrected to reject real remotes, clean rerun to `RESTORE_RESULT=OK`.

## 5. Limits carried forward

Single-threaded reachability notes (pair-wrapper drift branch
defensive-only, documented in-test); read-only-dir test assumes
non-root; Manifest-without-Freeze conservative refusal retained;
Retrospective full flow, DM-003/004/016/017/018/020, build transfer,
findings transport, whole-candidate/seven-point audit remain separate.
Whole candidate NOT_READY. Root + same independent reviewer close this
unit; Human Commit Point owns the next decision.
