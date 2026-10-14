# Anomalous v3b proof copy record (preserved evidence, cause undetermined)

2026-10-14. Executed `proof_apply16_v3b.py.READY` refused safely (exit 40)
at the first NEW-file unlink with `FileNotFoundError` for
`schemas/editorial-correction-proposal-v2.schema.json` in disposable copy
`/tmp/opencode/jgas-dm021p2r-verify-20261014T000002Z/candidate-partial-b40de60`.
The failed proof script, its stdout/stderr/exit, and the anomalous copy
itself are preserved byte-identical; nothing was repaired, deleted, or
rerun there. Active candidate was never written (status still `3M13A`,
all16 pins intact, verified after).

## Observed facts

- Proof log (`proof_apply16_v3b.stdout.txt`, 9 lines): patch sha matched
  the saved `complete-p2r-16path-v3.sha256`; active 16 matched static
  correction2c with HEAD/tree/index pinned (i.e. active HELD all 16 at
  proof runtime); copy `.git` walked 134 regular + 96 dirs, 0 problems;
  copy remote exact inert pair; 84 copy caches recorded; then the unlink
  refusal.
- Full `diff -rq` (excluding `__pycache__`) active-vs-copy: exactly 17
  non-cache lines — 13 files only-in-active (precisely the proof's NEW
  list: 4 schemas + 5 scripts + 4 tests), the 3 MODIFIED files differing
  (expected: the proof's `git checkout HEAD --` had already reverted them
  in the copy), and `.git/index` differing (expected: checkout updates
  index stat info). Nothing else differs.
- Copy `schemas/` dir mtime = proof runtime (freshly made by the proof's
  `cp -a --reflink=never`, rc 0); tracked files in the copy keep original
  mtimes (archive mode preserved).
- Active's 13 files carry old mtimes (Oct 12/13/14 edit times), distinct
  inodes from every other copy; never recreated.
- The v2 proof (11:02, same pattern, `...000000Z`) succeeded; the v3
  generator's disposable copy (`...000003Z`, same `cp` pattern, minutes
  before the proof) holds all 13 files.
- Step-by-step reproduction into `/tmp/opencode/bisect-probe` (freeze
  reads + remote/config + mkdir + the EXACT `cp` invocation + the EXACT
  `git checkout HEAD -- <3 paths>` invocation) keeps all files; a second
  plain manual `cp -a` into `/tmp/opencode/manual-copy-probe` also keeps
  them. No concurrent P2R process existed at proof time (narrow pgrep
  confirmed before and after); no sparse-checkout pruning (patterns
  include all affected dirs, and repro proves the checkout harmless).
- Disk healthy (tmpfs 22%); no symlinks in the involved paths; copy's
  git HEAD/history identical to active (detached 409b292).

## Status

Cause undetermined after direct investigation. v4
(`proof_apply16_v4.py.READY`, new copy `...000004Z`) adds a post-copy
completeness verification (all16 present + byte-equal active) that fails
fast and diagnosably. If v4 hits the same shape, stop — do not loop.
Probe dirs `manual-copy-probe/` + `bisect-probe/` are this turn's
diagnostic scratch (left in place, disclosed); they are not evidence.
