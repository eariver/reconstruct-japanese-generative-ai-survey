# Preparation qualification + current verification record (2026-10-09)

Supplements, never replaces, the copy-time packet. Old logs
(`commands.txt`, `source-identity.log`, `dst-identity.log`, `isolation.log`)
are preserved byte-identical; this record + `current-verify.sh` (exact script)
+ `current-verification.log` (raw stdout/stderr/exits) are new files.

## 1. `commands.txt` is an abbreviated reconstruction, not raw commands

- Line 22 `find <SRC|DST> | wc -l` is a placeholder (never executed literally).
- Line 23 aggregates six distinct git queries into one pseudo-command line.
- No per-command exit codes or env transcript were captured at copy time.
- The `CP_EXIT:0 / 0m0.042s` figure in `source-identity.log` is a transcribed
  note, not a captured `time` transcript. Do not replay `commands.txt` as exact history.

## 2. Current verification (2026-10-09, read-only, script exit 0)

- Proposal preserved: sha256 `4860669a…289`, 733 lines (log lines 1-4).
- DST/SRC identity hold NOW: HEAD `409b292…`, tree `8ce3699…`, parent `34f934e`,
  both `status` empty; origin inert; shallow `true`; no alternates (ls exit 2 =
  expected absence); no `GIT_*` overrides; no partialClone (log lines 6-33).
- Separation NOW: sample objects share device (dev=45, same filesystem) but
  distinct inodes, nlink=1; zero objects with nlink>1; zero shared object inodes
  (log lines 34-46). Same-device copy is disclosed; isolation rests on distinct
  inodes + no hardlinks/alternates, not separate media.
- Byte comparison: `diff -r -q` reports EXACTLY one difference — `.git/index`
  (log lines 47-49, exit 1). This is Git's stat cache, refreshed by the read-only
  `status` calls themselves; refs/objects/trees/worktree content otherwise identical.
  Refs identical (4 heads, no new writes, log lines 50-57). Reconstruct HEAD
  `1610777`, only untracked packet files added (log lines 58-71).

## 3. Limits (unchanged)

- Current checks verify CURRENT bytes only; they cannot retroactively certify that
  every copy-time guard (clean/order/no-fetch) held at copy time.
- Full-history availability remains limited: shallow at baseline, inherited
  unmaterialized blobs outside the available partial DB are unsearched.
- No source/test edits, fixture/test execution, commits, ref/branch writes, network,
  or edition-corpus expansion in this correction unit.
