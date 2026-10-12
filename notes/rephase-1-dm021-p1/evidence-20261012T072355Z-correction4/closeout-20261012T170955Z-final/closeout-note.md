# Final closeout note — correction4 strict verification (20261012T170955Z-final)

Read-only only. No source/test changes, no test runs, no historical-script runs,
no DB/index/worktree writes, no recopy/checkout/apply/cache-cleanup/commits,
no network. Scripts/logs live ONLY in this directory. Older evidence preserved
unmodified. No changes to global docs or other agent reports.

Tool note: the session offers no `apply_patch` tool, so the NEW script was
created with the file-creation tool (`Write`) under this exclusive directory —
same guarantee (writes only inside this new evidence dir, never into source DBs).

## 1. Prior predicate incompleteness (why this verification exists)

Root found the `closeout-20261012T121721Z/verify_current.py` checks insufficient
for fail-closed isolation claims:

- `walk_git_files` iterated `os.walk` FILES only — directory entries (including
  directory symlinks) were never `lstat`-checked; `lstat` `OSError` was silently
  skipped (`continue`); `os.walk` ran with default error handling (traversal
  errors ignored). A symlink smuggled as a directory, or an unreadable path,
  would pass silently.
- `inert` was a SUBSTRING test (`'example.invalid' in entire config text`).
  A config containing the string anywhere (comment, unrelated key, global file)
  would pass without the effective remote URL actually being inert; pushurl
  overrides and `url.insteadOf` rewrites were never inspected.

Those predicates are NOT repaired retroactively; that evidence keeps its original
narrow scope. This directory's `verify_final.py` replaces them with strict
current-observation checks (§2).

## 2. Strict checks in `verify_final.py` (all explicit-error, zero `assert` nodes)

- Sanitized env strips ALL `GIT_*` before forcing
  `GIT_NO_LAZY_FETCH=1/GIT_OPTIONAL_LOCKS=0/GIT_ALLOW_PROTOCOL=file`;
  inherited `GIT_*`/`PYTHONPATH`/`PYTHONHOME` recorded; `optimize!=0` refuses
  explicitly (no `assert` anywhere — verified 0 `ast.Assert` nodes, safe under `-O`).
- Read-only git verbs only (`rev-parse`, `status`, `diff --cached`, `ls-files`,
  `config --list --show-origin`, `remote -v`); every return code checked; no fetch.
- `.git` walked recursively with `os.scandir` + `lstat` on EVERY entry INCLUDING
  directories; ANY traversal/stat error, ANY symlink, ANY non-regular non-dir
  entry, or ANY regular file with `nlink!=1` is recorded as an error (fail-closed).
- Cross-repo `(dev,ino)` sharing across ALL `.git` regular files for
  active/copy/workspace must be 0/0/0 pairwise; alternates must be absent.
- Exact remote allowlist on REPO-LOCAL config (`file:.git/config*`) only:
  `remote.origin.url` must be exactly one entry equal to the expected URL
  (candidates: `https://example.invalid/rephase-candidate-recovery.git`;
  workspace: `https://github.com/eariver/reconstruct-japanese-generative-ai-survey.git`),
  no `pushurl`, no `url.*.insteadOf/pushInsteadOf`, no `include.*`, no http proxy
  keys, no extra remotes; effective `git remote -v (push)` token must equal the
  same URL. Global `/home/eariver/.gitconfig` (credential/user keys) is recorded
  as informational and can never satisfy the allowlist.
- Index incl intent: `diff --cached --name-only` empty AND no staged
  index-column rows in `status --porcelain` AND no lowercase `ls-files -v` tags.
- Identity: HEAD409/tree8ce, FULL raw status byte-equal to `freeze-pre` exact13,
  all 13 sha/mode/bytes equal to `freeze-pre`, patch SHA256 `85e9d9ab...`
  (604448B, 13 diffs), contract SHA256 `07e89990...`.

## 3. Self-correction record (transparent, preserved)

The first run in THIS directory (`verify-final-20261012T170955Z.raw.log/json`,
exit 30) failed ONLY on a script parser bug: `parse_config_exact` split the
`key=value` half on tab/whitespace instead of first `=`, yielding zero parsed
keys. Source state was never at fault (all identity/isolation lines passed).
The buggy pair is PRESERVED as defect evidence; the parser was fixed (split on
first `=`, strict scope to repo-local origins) and the corrected run wrote NEW
exclusive outputs (`*-corrected.raw.log/json`) without overwriting anything.

## 4. Result (current observation only)

Corrected run: `verdict=FINAL_CURRENT_MATCH`, `errors=[]`, exit 0.

- active/copy HEAD409/tree8ce, FULL status == freeze-pre (673B exact13),
  cached empty, no staged rows, no intent tags, alternates absent, exact inert
  remotes; workspace HEAD `ab17af4...` distinct with exact github remote.
- active/copy 13/13 bytes+modes match freeze-pre.
- Strict walks: active 229 entries (95 dirs + 134 files), copy identical,
  workspace 1341 (266 + 1075); 0 symlinks / 0 nlink_bad / 0 stat_errors
  everywhere; shared `(dev,ino)` 0/0/0.
- Patch + contract SHAs match.

## 5. Scope limits (binding)

This stronger result is CURRENT OBSERVATION ONLY (20261012T170955Z): it proves
byte/mode/status/identity/separation equality AT the recorded observations. It
is not retroactive copy-time proof, not continuous no-drift proof (an
intervening change-and-restore returning identical bytes cannot be excluded by
snapshots), not a closed future reject predicate, and not past enforcement
certification of the older restore/extract scripts (those remain exact-run
evidence only). No blockers observed; any claim beyond current-state equality
at these pins needs new evidence and is NOT made here.
