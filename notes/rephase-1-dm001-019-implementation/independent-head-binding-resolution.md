# Independent head-binding resolution — restored HEAD 222a37e (bounded exact-HEAD portable closure)

2026-10-04. Scoped author-independent follow-up; did not author
design/code/tests/corrections/bindings. No agents, tests, probes,
execution, network, recovery, or edits of any kind (no code/root/worker
edits, no original-review edits). Read-only Git
(`GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file`,
no root overrides) plus hash/list reads. Read `final-binding.md` and
`evidence-final-20261003T145621Z/50-head-binding/`
(`final-operational-manifest.json`, `supplement_check.py`,
`supplement-raw.log`, `switch-raw.log`); supplement failure scopes
read from the checker source. Every identity below was re-verified with
live commands in this session, not taken on report trust.

## 1. Live restored identity (true final, verified now)

DB `/tmp/opencode/jgas-dm001019-chainrestore-20261003T150500Z/candidate-partial-b40de60`:

- `rev-parse HEAD` = **`222a37e9ee2aa96724a491f2c04c2583a86b9650`**
  (on `refs/heads/dm001019-final` via `symbolic-ref HEAD`).
- `rev-parse HEAD^{tree}` = **`dbabeed5e70d79b51abb09b64666ca9e1d0fd5dd`**.
- `log --format='%H %P'`: `222a37e→ff6c67f→490414c→b40de60→774dd39a9`
  (5 lines, per-link parents intact).
- `status --porcelain=v1 --untracked-files=no` empty;
  full `status --porcelain=v1` empty; `diff HEAD --stat` empty;
  `diff --cached --stat` empty — tracked-clean and worktree-clean.
- 3-path `ls-tree HEAD`: modes `100644`, blobs
  `433c6096… / 90cd3506… / be394ef6…`, matching the operational
  manifest and the source worktree SHA256s
  (`092f1a2d… / f3b73d85… / b84b7a76…` — restored bytes identical to
  source bytes for all three files, re-hashed here).
- Source DB `/tmp/opencode/jgas-dm001019-impl-20261003T100801Z`
  unchanged: HEAD `222a37e`, tree `dbabeed5…`.

## 2. Operational manifest + pack/archive hashes (re-hashed here)

- Pack `20-packaging/successor-pack.pack`: SHA256
  `2c2a8e6f2ab5fbd71b6cddfe5d875e4a821d09ef54ba9714eaab12e438e81a99`,
  46,164 B — matches `final-operational-manifest.json`.
- Parent archive `m3-20261003T0445Z/candidate-partial-b40de60.tar.gz`:
  SHA256 `faf6792faf37ad30af2dbd7203b8896ca00964a91d00623a4f01278f2ade9f3c`,
  5,152,199 B — matches.
- Object types **machine-counted here** via `cat-file --batch-check`
  over the 20 enumerated SHAs in the restored DB:
  **3 commits + 9 trees + 8 blobs** (20/20 present).
- Full tree `ls-tree -r HEAD`: **32,153 entries** (matches manifest
  `tree_entry_count`); `merge-base --is-ancestor b40de60 HEAD` exit 0;
  `.git/shallow` contains only `774dd39a…` (cutoff solely at real
  774, no manufactured markers).
- Object-store independence re-verified here (not report trust):
  68 files under restored `.git/objects`, 68 under donor, **zero
  shared (dev,ino) pairs, zero multi-linked files**, no `alternates`
  either side. Only remotes are the inert
  `origin → https://example.invalid/…` placeholder pair inherited
  from the parent archive (no real remotes).

## 3. Supplement/switch failure scopes (read from checker, results confirmed)

- `supplement_check.py` is read-only (no writes/checkouts/ref moves;
  only OUT logs + manifest): 13 checks, **any FAIL → exit 1 /
  `SUPPLEMENT_RESULT=FAIL`**. `supplement-raw.log` shows 13/13 PASS,
  no FAIL lines. No hidden failure raw exists in `50-head-binding/`.
- `switch-raw.log`: pre-switch HEAD b40 + staged FINAL bytes,
  normal `git switch dm001019-final`, `switch-exit=0` — no
  reset/clean/bypass. The only preserved failure raws in scope are
  the two historic `30-restore/` attempt logs (strict-linkage,
  remote-gate), both superseded by passing reruns, never relabelled.

## 4. Prior overclaims qualified (this review corrects, originals stand)

- **Ref-only / full-HEAD overclaim:** my `independent-final-resolution.md`
  §1 noted "Worktree HEAD stays b40" yet §6–7 accepted G1 as fulfilled.
  A ref pointing at 222 with HEAD checked out at b40 is **not** exact-HEAD
  portable closure. That acceptance was overbroad and is withdrawn here;
  closure holds only with this binding (actual HEAD 222, §1 above).
- **Wrong typed counts:** my review repeated the report's
  "3 commits + 5 trees + 12 blobs" (`final-closure-report.md §4`).
  Machine truth is **3 + 9 + 8**: 9 trees (root/scripts/tests × 3 commits,
  all distinct) and 8 unique blobs (3 + 3 + 2; profiled `433c6096…`
  shared ff→final). `final-binding.md §2` already corrects the report;
  this confirms it live.
- **Historic procedure scope:** `30-restore/restore_chain.py` proves the
  final REF, 20 objects, 3-path blobs/bytes/index, chain log and tree
  refs — but leaves HEAD at b40 with FINAL bytes staged, has **no pack
  hash gate**, and its `own-store ino!=0` check proves existence, not
  non-sharing. It is preserved as an incomplete historic procedure and
  is **not certified as a general safe restore script** (agreeing with
  `final-binding.md §4`). Future recovery needs a new verified procedure
  with archive/pack hash gates, absent-destination gate, normal HEAD
  switch, and the full verification set performed here.

## 5. Disposition (bounded)

- **Bounded exact-HEAD portable closure at `222a37e`: BOUNDED_PASS.**
  Actual restored HEAD/tree/branch/chain, tracked/worktree clean,
  3-file Git binding + worktree bytes identical to source, 20-object
  machine-typed availability, archive/pack hashes, full 32,153-entry
  tree, shallow-only-at-774 chain, physical no-sharing — all verified
  live in this session.
- Limits unchanged: single-threaded notes, non-root read-only-dir
  assumption, Manifest-without-Freeze conservative refusal,
  Retrospective/DM-003/004/016/017/018/020/build-transfer/findings/
  all-profile/application out of scope, parent missing historical blobs
  declared. **Whole candidate NOT_READY**; no adoption, Freeze/Release,
  or production authority inferred. Human Commit Point owns next.
