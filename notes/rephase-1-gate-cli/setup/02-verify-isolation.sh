#!/usr/bin/env bash
# Verify the new gate-cli DB is an independent, byte-identical copy of B and
# shares no objects/symlinks/inodes with the source fixture.
set -uo pipefail

SRC=/tmp/jgas-rephase-increment-b-sol-implementation
DST=/tmp/jgas-rephase-gate-cli

echo "== A. destination identity =="
git -C "$DST" rev-parse HEAD
git -C "$DST" rev-parse 'HEAD^{tree}'
git -C "$DST" rev-parse 'HEAD^'
echo "branch=$(git -C "$DST" branch --show-current)"
echo "== B. source identity (recheck) =="
git -C "$SRC" rev-parse HEAD
git -C "$SRC" rev-parse 'HEAD^{tree}'
git -C "$SRC" rev-parse 'HEAD^'
echo "== C. worktree status (tracked) =="
git -C "$DST" status --porcelain
echo "== D. origin =="
git -C "$DST" remote -v
echo "== E. alternates =="
if [ -e "$DST/.git/objects/info/alternates" ]; then echo "ALTERNATES_PRESENT"; cat "$DST/.git/objects/info/alternates"; else echo "NO_ALTERNATES"; fi
echo "alternate_env=${GIT_ALTERNATE_OBJECT_DIRECTORIES:-UNSET}"
echo "gitdir_env=${GIT_DIR:-UNSET}"
echo "worktree_env=${GIT_WORK_TREE:-UNSET}"
echo "index_env=${GIT_INDEX_FILE:-UNSET}"
echo "objectdir_env=${GIT_OBJECT_DIRECTORY:-UNSET}"
echo "common_dir=$(git -C "$DST" rev-parse --git-common-dir)"
echo "git_dir=$(git -C "$DST" rev-parse --absolute-git-dir)"
echo "== F. symlinks (must be empty) =="
find "$DST" -type l -print
echo "-- .git symlinks (must be empty) --"
find "$DST/.git" -type l -print
echo "== G. hardlink count >1 inside destination (must be empty) =="
find "$DST" -type f -links +1 -print
echo "== H. cross-DB inode intersection (must be empty) =="
find "$SRC" -type f -printf '%i\n' 2>/dev/null | sort -u > /tmp/gate-cli-src-inodes.txt
find "$DST" -type f -printf '%i\n' 2>/dev/null | sort -u > /tmp/gate-cli-dst-inodes.txt
comm -12 /tmp/gate-cli-src-inodes.txt /tmp/gate-cli-dst-inodes.txt
echo "src_file_count=$(find "$SRC" -type f | wc -l) dst_file_count=$(find "$DST" -type f | wc -l)"
echo "== I. object counts =="
git -C "$DST" count-objects -vH
echo "== J. refs =="
git -C "$DST" for-each-ref
echo "== K. fsck (promisor shallow expected) =="
git -C "$DST" fsck --no-dangling 2>&1 | head -40
echo "== L. shallow boundary =="
cat "$DST/.git/shallow"
echo "== M. size =="
du -sh "$DST" "$DST/.git"
