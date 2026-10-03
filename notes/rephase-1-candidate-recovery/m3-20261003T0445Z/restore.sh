#!/bin/bash
# Offline restore of candidate-partial-b40de60.tar.gz into a second independent dir.
# Archive layout (authoritative: tar -tzf listing):
#   candidate-partial-b40de60/.git/...   (partial DB, no FETCH_HEAD)
#   candidate-partial-b40de60/<worktree paths>  (686 materialized tracked files)
# Usage: restore.sh <archive.tar.gz> <destdir> <rawdir>
# Result: <destdir>/.git + worktree files at <destdir>/. Strict: any unexpected
# layout aborts BEFORE destructive steps; the top dir is removed only when empty.
set -u
ARC="$1"; DEST="$2"; RAW="$3"
mkdir -p "$RAW"
{
echo "argv=$0 $*"
echo "cwd=$(pwd)"
test ! -e "$DEST" || { echo "DEST_EXISTS_ABORT"; exit 10; }
echo "DEST_ABSENT_OK"
tar -tzf "$ARC" > "$RAW/listing.txt" 2> "$RAW/listing.stderr.txt"
echo "list-exit:$?"
grep -vE "^candidate-partial-b40de60/" "$RAW/listing.txt" > "$RAW/nonconforming.txt" 2>&1
test ! -s "$RAW/nonconforming.txt" || { echo "NONCONFORMING_MEMBER"; exit 11; }
echo "ALL_MEMBERS_UNDER_TOPDIR"
grep -E '(^/|\\.\\.)' "$RAW/listing.txt" > "$RAW/traversal.txt" 2>&1
test ! -s "$RAW/traversal.txt" || { echo "TRAVERSAL_MEMBER"; exit 12; }
echo "NO_TRAVERSAL"
grep -E '(^|/)\\.git/FETCH_HEAD$' "$RAW/listing.txt" > "$RAW/fetchhead.txt" 2>&1
test ! -s "$RAW/fetchhead.txt" || { echo "FETCH_HEAD_PRESENT"; exit 13; }
echo "NO_FETCH_HEAD_IN_ARCHIVE"
mkdir -p "$DEST"
tar -xzf "$ARC" -C "$DEST" > "$RAW/extract.stdout.txt" 2> "$RAW/extract.stderr.txt"
echo "extract-exit:$?"
test -d "$DEST/candidate-partial-b40de60/.git" || { echo "NO_DOTGIT_AFTER_EXTRACT"; exit 14; }
echo "DOTGIT_EXTRACTED"
mv "$DEST/candidate-partial-b40de60/.git" "$DEST/.git"
echo "dotgit-moved:$?"
shopt -s dotglob nullglob
moved=0
for entry in "$DEST/candidate-partial-b40de60/"*; do
  mv "$entry" "$DEST/"
  moved=$((moved+1))
done
echo "worktree-entries-moved:$moved"
restored_files=$(find "$DEST" -path "$DEST/.git" -prune -o -type f -print | wc -l)
echo "restored-worktree-files:$restored_files"
test "$restored_files" -eq 686 || { echo "WORKTREE_COUNT_MISMATCH"; exit 15; }
rmdir "$DEST/candidate-partial-b40de60" 2>/dev/null || true
echo "topdir-removed:$?"
test ! -e "$DEST/.git/objects/info/alternates" && echo "NO_ALTERNATES"
git -C "$DEST" remote -v
} 2>&1 | tee "$RAW/script.log"
