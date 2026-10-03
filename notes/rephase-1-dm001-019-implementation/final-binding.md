# DM-001/019 final binding — restored HEAD + worktree (supersedes ref-only scope)

2026-10-04. Root verification follow-up: the chained restore proved the
final REF (`restore-run.log: RESTORE_RESULT=OK`) while restored HEAD stayed
at b40 with FINAL 3-path bytes staged. Independent reviewer §33–34 noted
this yet called G1 fulfilled. This binding completes the actual worktree
proof with no candidate/test/network changes and no old-evidence edits.

## 1. New final binding

- Operational manifest:
  `notes/rephase-1-dm001-019-implementation/evidence-final-20261003T145621Z/50-head-binding/final-operational-manifest.json`
- Supplement raw:
  `…/50-head-binding/supplement-raw.log`
  (`SUPPLEMENT_RESULT=OK`, exit 0; runner
  `…/50-head-binding/supplement_check.py`, read-only)
- Switch raw:
  `…/50-head-binding/switch-raw.log`
  (pre-switch b40 + staged FINAL bytes, normal `git switch
  dm001019-final`, exit 0, no reset/clean/bypass)

Restored DB `/tmp/opencode/jgas-dm001019-chainrestore-20261003T150500Z/candidate-partial-b40de60`
now: HEAD **`222a37e9ee2aa96724a491f2c04c2583a86b9650`** on branch
`dm001019-final`, tree **`dbabeed5e70d79b51abb09b64666ca9e1d0fd5dd`**,
parent `ff6c67f`, chain `222a37e→ff6c67f→490414c→b40de60→774dd39a9`,
tracked-clean, worktree-clean (no untracked), `diff HEAD` and
`diff --cached` empty. Final commit hash unchanged from packaging.

## 2. Machine-counted object types (corrects final report §4)

`git cat-file --batch-check` over the 20 enumerated SHAs in the restored
DB: **3 commits + 9 trees + 8 blobs** (not the retyped 3+5+12 that slipped
into `final-closure-report.md §4`). Count and breakdown both from Git.

## 3. No-sharing proof (replaces inode!=0 heuristic)

68 files under restored `.git/objects` vs full donor inventory: zero
shared (dev,ino) pairs, zero multi-linked files, no alternates either
side. Donor pack-store vs restored loose-store are fully distinct.

## 4. Honest record: original ref-only scope

`30-restore/restore_chain.py` verified the final REF, 20 objects, 3-path
blobs/bytes/index, chain log and tree refs — but left HEAD at b40 with the
3 FINAL files staged, had no pack-hash gate, and its `own-store ino!=0`
check proved existence, not non-sharing. It stays preserved as the
historic incomplete procedure and is **not certified as a general safe
restore script**. Any future recovery must use a new verified procedure
including: archive hash/member gates, absent-destination gate, exact pack
hash gate, ref establishment, normal HEAD switch, full HEAD/tree/parent/
clean-status/chain/object/inode verification as performed here.

## 5. Operational manifest contents

Source + restored paths, current HEAD/tree/branch/parent chain, 3 actual
Git mode/blob + worktree SHA256 entries, parent archive SHA256
`faf6792f…`/5,152,199 B/760 members, pack SHA256 `2c2a8e6f…`/46,164 B/
20 objects with machine type counts. No failures: supplement exit 0,
all 14 checks PASS, no failure raw beyond the two preserved
attempt-logs in `30-restore/`.
