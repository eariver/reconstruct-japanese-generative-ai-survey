#!/bin/bash
# G2 commit — ONLY PUB draft-fix (3f4039fd) before new U authority (preserves G1 + V1/V2/V3 evidence)
set -u
REPO=/home/eariver/git/reconstruct-japanese-generative-ai-survey
FIX=$REPO/.rephase-1-editorial-runtime/versioned-renewal-freeze-transitive-20261025T120000Z/renewal-weekly
CANDPUB=$REPO/.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work/scripts/survey_publication_v2.py
EVID=$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/freeze-transitive-correction/g2-commit-20261025T122000Z
mkdir -p "$EVID"
exec > "$EVID/commands.log" 2>&1
echo "FIX $FIX HEAD $(git -C $FIX rev-parse HEAD)"
run() { desc="$1"; shift; echo "\$ $* # $desc"; "$@" > "$EVID/$desc-stdout.txt" 2> "$EVID/$desc-stderr.txt"; ec=$?; echo $ec > "$EVID/$desc-exit.txt"; echo "-> exit=$ec"; return $ec; }
python3 -c "
import pathlib, shutil, hashlib
dst=pathlib.Path('$FIX')/'scripts/survey_publication_v2.py'
cand=pathlib.Path('$CANDPUB')
shutil.copy2(cand,dst)
print(f'G2 PUB SHA {hashlib.sha256(dst.read_bytes()).hexdigest()} bytes {dst.stat().st_size}')
"
run diff git -C "$FIX" diff --name-only
run status git -C "$FIX" status --porcelain=v1 --untracked-files=all
export GIT_AUTHOR_NAME=rephase-fixture
export GIT_AUTHOR_EMAIL=fixture@example.invalid
export GIT_COMMITTER_NAME=rephase-fixture
export GIT_COMMITTER_EMAIL=fixture@example.invalid
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
run add git -C "$FIX" add -- scripts/survey_publication_v2.py
run head-pre git -C "$FIX" rev-parse HEAD
run commit-g2 git -C "$FIX" commit -m "G2 PUB draft-fix (3f4039fd) before new U authority (freeze-transitive)"
run head-post git -C "$FIX" rev-parse HEAD
run log-post git -C "$FIX" log --oneline -4
run show-stat git -C "$FIX" show --stat HEAD
echo "G2_DONE"
