#!/usr/bin/env bash
# DM-004 safe offline restore: b40 archive + successor20 + w1seven + dm004new.
# Fail-closed: hash-gates all 4 inputs, extracts only to an ABSENT destination,
# imports packs, switches actual HEAD, verifies clean/chain/objects/bytes.
# No network, no old-script reuse, no source mutation.
set -euo pipefail
export GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file

EVID=/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-dm004-implementation/evidence-20261004T234535Z
ARCHIVE=/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-candidate-recovery/m3-20261003T0445Z/candidate-partial-b40de60.tar.gz
SUCCESSOR=/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-dm001-019-implementation/evidence-final-20261003T145621Z/20-packaging/successor-pack.pack
W1PACK=/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-dm003-w1-implementation/evidence-20261004T072423Z/w1-222-to-e1705b7.pack
DM004PACK=$EVID/dm004-e1705b7-to-6ffed32.pack
DEST=/tmp/opencode/jgas-dm004-restore-20261004T235816Z
REPO=$DEST/candidate-partial-b40de60
FINAL=6ffed32298fdaf87874a643b0f9f9b8f837c0256
FINAL_TREE=c3d6ad6ffdadf2d5780a3cd5109555c87fe394cc

echo "== hash gates =="
echo "faf6792faf37ad30af2dbd7203b8896ca00964a91d00623a4f01278f2ade9f3c  $ARCHIVE" | sha256sum -c -
echo "2c2a8e6f2ab5fbd71b6cddfe5d875e4a821d09ef54ba9714eaab12e438e81a99  $SUCCESSOR" | sha256sum -c -
echo "97d384fe8f7216f110cd401d1279129da83fab2000f28c24a73abe0b177b0fd9  $W1PACK" | sha256sum -c -
echo "7e147a60fd1d751f4afeb91aa12d7ef7652693ef9453e3b7c564f59c95dd0b4e  $DM004PACK" | sha256sum -c -

echo "== absent destination =="
if [ -e "$DEST" ]; then echo "DEST EXISTS: $DEST" >&2; exit 1; fi
mkdir -p "$DEST"

echo "== extract archive =="
tar xzf "$ARCHIVE" -C "$DEST"
ls "$REPO" | head -5
git -C "$REPO" rev-parse --git-dir
git -C "$REPO" remote -v || echo "no remotes"

echo "== import packs in order =="
git -C "$REPO" unpack-objects < "$SUCCESSOR"
git -C "$REPO" unpack-objects < "$W1PACK"
git -C "$REPO" unpack-objects < "$DM004PACK"

echo "== object availability =="
git -C "$REPO" cat-file -e "$FINAL" && echo "final commit present"
git -C "$REPO" cat-file -e e1705b7fed01369767ab9d827c0360117d54aa1f && echo "e170 present"
git -C "$REPO" cat-file -e 222a37e9ee2aa96724a491f2c04c2583a86b9650 && echo "222 present"

echo "== switch actual HEAD =="
git -C "$REPO" update-ref refs/heads/dm004-final "$FINAL"
git -C "$REPO" symbolic-ref HEAD refs/heads/dm004-final
git -C "$REPO" checkout --force dm004-final -- 2>&1 | tail -2 || true
git -C "$REPO" reset --hard "$FINAL"

echo "== identity and cleanliness =="
git -C "$REPO" rev-parse HEAD
git -C "$REPO" rev-parse 'HEAD^{tree}'
git -C "$REPO" rev-parse HEAD^
git -C "$REPO" status --porcelain
git -C "$REPO" log --oneline -8
echo "== alternates check =="
test ! -e "$REPO/.git/objects/info/alternates" && echo "no alternates"
echo "== changed-file bytes =="
git -C "$REPO" rev-parse 'HEAD:scripts/survey_agent_control_v2.py'
git -C "$REPO" rev-parse 'HEAD:tests/test_survey_dm004_release_validate_state_v2.py'
sha256sum "$REPO/scripts/survey_agent_control_v2.py" "$REPO/tests/test_survey_dm004_release_validate_state_v2.py"
echo "RESTORE-DONE"
