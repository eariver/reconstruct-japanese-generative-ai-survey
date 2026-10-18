# P3S preparation raw (direct command outputs, read-only + copy + implement)

All Git-aware reads use `GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file`.
No module imports, no test runs, no historical-script execution in this packet.
Cheap checks ran with `PYTHONDONTWRITEBYTECODE=1` (stdlib/third-party imports only).

## P0. Pre-copy source identity (P2V active copy)

Worktree: `/tmp/opencode/jgas-dm021p2v-impl-20261014T224000Z/candidate-partial-b40de60`

```
$ git rev-parse HEAD
409b292756dd1277b9dfae87679934c0d2ce251c
$ git rev-parse 'HEAD^{tree}'
8ce3699861505f32d1d60bdc185d4d4f635aedb2
$ git status --porcelain=v1 --untracked-files=all | sort | wc -l
102
$ git remote -v
origin  https://example.invalid/rephase-candidate-recovery.git (fetch)
origin  https://example.invalid/rephase-candidate-recovery.git (push)
$ ls .git/objects/info/alternates
(no such file)
$ git symbolic-ref -q HEAD; echo "rc=$? (nonzero=detached)"
rc=1 (nonzero=detached)
```

Static18 (sha256sum+stat, no imports): 18/18 MATCH vs
`notes/rephase-1-dm021-p2v/source-correction/expected18-source-correction-v5.json`
(bytes+sha256+mode 0o664 all equal).
Cache census (path only, bytes NOT proven, nothing executed/imported):
`find scripts/__pycache__ tests/__pycache__ -name '*.pyc' | wc -l` = 84
(68 scripts + 16 tests).

## P1. Copy command

```
$ date -u +%Y%m%dT%H%M%SZ
20261017T092635Z
$ mkdir -p /tmp/opencode/jgas-dm021p3s-impl-20261017T092635Z
$ cp -a /tmp/opencode/jgas-dm021p2v-impl-20261014T224000Z/candidate-partial-b40de60 \
      /tmp/opencode/jgas-dm021p3s-impl-20261017T092635Z/candidate-partial-b40de60
COPY_DONE
```

`cp -a` recreates all inodes in the destination (no `--link`), so no
cross-DB hardlink sharing is possible; verified by inode-set comparison below
instead of trusting flags.

## P2. Post-copy identity (NEW copy, before implementation)

```
$ git rev-parse HEAD
409b292756dd1277b9dfae87679934c0d2ce251c
$ git rev-parse 'HEAD^{tree}'
8ce3699861505f32d1d60bdc185d4d4f635aedb2
$ git status --porcelain=v1 --untracked-files=all | wc -l
102
$ git remote -v
origin  https://example.invalid/rephase-candidate-recovery.git (fetch/push)
$ ls .git/objects/info/alternates
(no such file)
$ git config --local --list | head
core.repositoryformatversion=1
core.filemode=true
core.bare=false
core.logallrefupdates=true
extensions.worktreeconfig=true
remote.origin.url=https://example.invalid/rephase-candidate-recovery.git
remote.origin.fetch=+refs/heads/*:refs/remotes/origin/*
```

Isolation (lstat walk, followlinks=False, both trees):

```
source entries: 1053   copy entries: 1053
shared inodes (dev,ino intersection): 0
all-entry census (copy): {'dir': 131, 'reg': 922}, odd (symlink/fifo/special): 0
```

No `.git` writes (no add/commit/branch/ref edit; detached HEAD untouched).

## P3. Implementation (NEW copy only)

3 files created (no edits to inherited 18; no other tree changes):

- `scripts/survey_editorial_staged_source_v2.py` (77172 B, 0o664, sha256 `49a5564371ae57c2…`)
- `schemas/editorial-staged-source-manifest-v2.schema.json` (5627 B, 0o664, sha256 `4fa6172338072258…`)
- `tests/test_survey_editorial_staged_source_v2.py` (40738 B, 0o664, sha256 `92fcc964838991e8…`)

Authoring notes (failures preserved): the initial whole-file `write` of the
module truncated mid-statement (harness payload limit); the remainder was
appended via sequential edits. Two `edit` payloads were likewise truncated
and completed by follow-up edits; the harness left literal
`...[truncated NNNN chars]` marker lines at two truncation points, both
removed (module tail + test mid-file). Final byte-verification below proves
no marker text remains in any of the 3 files (`b'...[truncated' not in bytes`).

## P4. Post-implementation static checks (NEW copy)

Cheap syntax only (no candidate imports; `PYTHONDONTWRITEBYTECODE=1`):

```
module AST-OK defs: 20 (materialize True, verify True); no harness marker
test AST-OK methods: 16 (o1..o14 incl. o6a/o6b + r1); no harness marker
schema JSON-OK; Draft202012Validator.check_schema OK; top-level required: 17
S2 sets from module text (no import): shared py 27 sorted True;
  shared schemas 5 sorted True; LONGFORM 37 unique True; WEEKLY 37 unique True
```

Static21 / inherited18 / caches:

```
inherited18 match: 18 / 18 (sha256+bytes+mode vs expected18 v5)
new3: 77172 / 5627 / 40738 B, all 0o664
status rows: 105  (3 M + 102 ??; i.e. 3M + 18 new source + 84 pyc)
tracked diff vs HEAD: exactly the inherited P2V 3M overlay
  schemas/reader-surface-gate-v2.schema.json          16 +++
  schemas/reader-surface-semantic-review-v2.schema.json  32 +++++
  scripts/survey_reader_surface_gate_v2.py           144 ++++--
  3 files changed, 182 insertions(+), 10 deletions(-)
```

Cache-effect evidence: `git status` showed 84 `__pycache__/*.pyc` rows before
implementation and 84 after; total rows 102 → 105 = exactly +3 new source
files. No `.pyc` created, executed, or cleaned by the cheap checks.

## P5. POST run (NEW copy, finally)

```
$ git rev-parse HEAD        -> 409b292756dd1277b9dfae87679934c0d2ce251c (rc=0)
$ git rev-parse 'HEAD^{tree}' -> 8ce3699861505f32d1d60bdc185d4d4f635aedb2 (rc=0)
$ git status --porcelain ... | wc -l  -> 105
$ git diff --quiet HEAD -- .  -> rc=1 (expected: inherited P2V 3M overlay)
```

Root selects smoke/affected/full checks after source + draft review. No
archive/fake-root/active `git add -N`/absent-NEW-file reads; GEN/PROOF
DBs/indexes (when authorized) stay under fresh `/tmp/opencode` locations,
never in notes.
