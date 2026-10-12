#!/usr/bin/env bash
# DM021-P1 Phase A restore — NEW script authored 2026-10-11T16:00:37Z.
# Fail-closed offline restore of actual409 into an exclusive destination.
# Reference only: old restore.sh / restore_dm004final.sh (NEVER executed here).
# Any gate failure aborts with nonzero exit; no repair, no retry-by-edit.
set -euo pipefail

# ---- R1: route isolation (no inherited Git routing, no Human config touch) --
unset GIT_DIR GIT_WORK_TREE GIT_PREFIX GIT_INDEX_FILE GIT_OBJECT_DIRECTORY \
  GIT_ALTERNATE_OBJECT_DIRECTORIES 2>/dev/null || true
export GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file
export GIT_CEILING_DIRECTORIES=/tmp/opencode
export TZ=UTC

WS=/home/eariver/git/reconstruct-japanese-generative-ai-survey
EVID=$WS/notes/rephase-1-dm021-p1/evidence-20261011T160037Z-phaseA
ARC=$WS/notes/rephase-1-candidate-recovery/m3-20261003T0445Z/candidate-partial-b40de60.tar.gz
P20=$WS/notes/rephase-1-dm001-019-implementation/evidence-final-20261003T145621Z/20-packaging/successor-pack.pack
PW1=$WS/notes/rephase-1-dm003-w1-implementation/evidence-20261004T072423Z/w1-222-to-e1705b7.pack
P32=$WS/notes/rephase-1-dm004-implementation/evidence-20261007T131353Z/dm004final-e1705b7-to-409b292.pack
DEST=/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z
REPO=$DEST/candidate-partial-b40de60
RAW=$EVID/raw
FINAL=409b292756dd1277b9dfae87679934c0d2ce251c
FTREE=8ce3699861505f32d1d60bdc185d4d4f635aedb2
FPARENT=34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4
C222=222a37e9ee2aa96724a491f2c04c2583a86b9650
CE170=e1705b7fed01369767ab9d827c0360117d54aa1f

echo "== P1A argv/cwd/machine =="
echo "argv: $0 $*"
echo "cwd: $(pwd)"
echo "host: $(hostname)"; uname -a
echo "git: $(git --version)"; echo "python: $(python3 --version 2>&1)"
echo "umask: $(umask)"; echo "date-utc: $(date -u +%Y%m%dT%H%M%SZ)"
echo "git-env: $(env | grep -E '^GIT' | sort | tr '\n' ';')"

echo "== P1A hash gates (4 archive/pack inputs) =="
echo "faf6792faf37ad30af2dbd7203b8896ca00964a91d00623a4f01278f2ade9f3c  $ARC" | sha256sum -c -
echo "2c2a8e6f2ab5fbd71b6cddfe5d875e4a821d09ef54ba9714eaab12e438e81a99  $P20" | sha256sum -c -
echo "97d384fe8f7216f110cd401d1279129da83fab2000f28c24a73abe0b177b0fd9  $PW1" | sha256sum -c -
echo "e3d941653eadf2459a13f1b85b9fbbffd819f0a0ad6bb77eb121b2cba02279bf  $P32" | sha256sum -c -

echo "== P1A archive pre-extraction verification (R2) =="
mkdir -p "$RAW"
tar -tzvf "$ARC" > "$RAW/archive-verbose-listing.txt"
tar -tzf "$ARC" > "$RAW/archive-members.txt"
wc -l "$RAW/archive-members.txt"
awk '{print $1}' "$RAW/archive-verbose-listing.txt" | cut -c1 | sort | uniq -c
# type flags: only '-' regular, 'd' dir, 'g' global header allowed
awk '{print substr($1,1,1)}' "$RAW/archive-verbose-listing.txt" | sort -u > "$RAW/archive-typeflags.txt"
cat "$RAW/archive-typeflags.txt"
grep -vE '^[dg-]$' "$RAW/archive-typeflags.txt" && { echo "FORBIDDEN_MEMBER_TYPE"; exit 21; }
echo "TYPES_OK"
grep -vE '^candidate-partial-b40de60(/|$)' "$RAW/archive-members.txt" > "$RAW/archive-nonconforming.txt" || true
test ! -s "$RAW/archive-nonconforming.txt" || { echo "NONCONFORMING_MEMBER"; exit 22; }
echo "ALL_MEMBERS_UNDER_TOPDIR"
grep -E '(^/|\\.\\.)' "$RAW/archive-members.txt" > "$RAW/archive-traversal.txt" || true
test ! -s "$RAW/archive-traversal.txt" || { echo "TRAVERSAL_MEMBER"; exit 23; }
echo "NO_TRAVERSAL"
grep -E '(^|/)\\.git/FETCH_HEAD$' "$RAW/archive-members.txt" > "$RAW/archive-fetchhead.txt" || true
test ! -s "$RAW/archive-fetchhead.txt" || { echo "FETCH_HEAD_PRESENT"; exit 24; }
echo "NO_FETCH_HEAD_IN_ARCHIVE"
sort "$RAW/archive-members.txt" | uniq -d > "$RAW/archive-duplicates.txt" || true
test ! -s "$RAW/archive-duplicates.txt" || { echo "DUPLICATE_MEMBER"; exit 25; }
echo "NO_DUPLICATES"

echo "== P1A exclusive extraction (R3) =="
test ! -e "$DEST" || { echo "DEST_EXISTS_ABORT"; exit 26; }
mkdir -p "$DEST"
tar -xzf "$ARC" -C "$DEST"
test -d "$REPO/.git" || { echo "NO_DOTGIT_AFTER_EXTRACT"; exit 27; }
echo "DOTGIT_EXTRACTED"

echo "== P1A imported config/hooks inspection (R4) =="
cat "$REPO/.git/config"
echo "--- hooks: ---"; ls -la "$REPO/.git/hooks"
echo "--- remotes: ---"; git -C "$REPO" remote -v || echo "NO_REMOTES"
git -C "$REPO" remote -v | grep -v 'example.invalid' > "$RAW/live-remote-check.txt" || true
test ! -s "$RAW/live-remote-check.txt" || { echo "LIVE_REMOTE_ABORT"; exit 28; }
echo "REMOTES_INERT_OK"
test ! -e "$REPO/.git/objects/info/alternates" || { echo "ALTERNATES_PRESENT_ABORT"; exit 29; }
echo "NO_ALTERNATES"
git -C "$REPO" rev-parse --is-shallow-repository
cat "$REPO/.git/shallow" 2>/dev/null | head -5 || true

echo "== P1A pack import 20+7+32 (R5) =="
git -C "$REPO" unpack-objects < "$P20"; echo "unpack20-exit:$?"
git -C "$REPO" unpack-objects < "$PW1"; echo "unpack7-exit:$?"
git -C "$REPO" unpack-objects < "$P32"; echo "unpack32-exit:$?"
git -C "$REPO" cat-file -e "$C222" && echo "C222_PRESENT"
git -C "$REPO" cat-file -e "$CE170" && echo "CE170_PRESENT"
git -C "$REPO" cat-file -e "$FINAL" && echo "FINAL_PRESENT"

echo "== P1A sparse state (no hydration) =="
git -C "$REPO" config --get core.sparseCheckout || echo "sparseCheckout-unset"
git -C "$REPO" sparse-checkout list 2>&1 || true

echo "== P1A select existing 409 detached, no new branch (R6) =="
git -C "$REPO" checkout --detach "$FINAL"
echo "checkout-exit:$?"
test "$(git -C "$REPO" rev-parse HEAD)" = "$FINAL" || { echo "HEAD_MISMATCH"; exit 31; }
test "$(git -C "$REPO" rev-parse 'HEAD^{tree}')" = "$FTREE" || { echo "TREE_MISMATCH"; exit 32; }
test "$(git -C "$REPO" rev-parse 'HEAD^')" = "$FPARENT" || { echo "PARENT_MISMATCH"; exit 33; }
echo "IDENTITY_409_OK"
git -C "$REPO" branch --show-current | tee "$RAW/branch-after-detach.txt"
test ! -s "$RAW/branch-after-detach.txt" || { echo "ON_BRANCH_ABORT"; exit 34; }
echo "DETACHED_NO_BRANCH_OK"
git -C "$REPO" log --oneline -14 | tee "$RAW/available-chain.txt"
git -C "$REPO" status --porcelain | tee "$RAW/status-409.txt"
test ! -s "$RAW/status-409.txt" || { echo "STATUS_NOT_CLEAN"; exit 35; }
echo "STATUS_CLEAN_409"

echo "== P1A no-sharing proof vs workspace DB (R4) =="
find "$REPO/.git/objects" -type f -printf '%d %i\n' 2>/dev/null | sort -u > "$RAW/restore-object-inodes.txt" || \
  find "$REPO/.git/objects" -type f -exec stat -c '%d %i' {} + | sort -u > "$RAW/restore-object-inodes.txt"
find "$WS/.git/objects" -type f -exec stat -c '%d %i' {} + | sort -u > "$RAW/workspace-object-inodes.txt"
wc -l "$RAW/restore-object-inodes.txt" "$RAW/workspace-object-inodes.txt"
comm -12 "$RAW/restore-object-inodes.txt" "$RAW/workspace-object-inodes.txt" > "$RAW/shared-inodes.txt" || true
test ! -s "$RAW/shared-inodes.txt" || { echo "SHARED_INODES_ABORT"; exit 36; }
echo "ZERO_SHARED_INODES_OK"

echo "P1A_RESTORE_DONE"
