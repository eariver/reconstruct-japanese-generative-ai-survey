#!/bin/bash
# G1 commit — SOURCE-only fixed736 + ONLY PUB patch (owned) before U authority
set -u
REPO=/home/eariver/git/reconstruct-japanese-generative-ai-survey
FIX=$REPO/.rephase-1-editorial-runtime/versioned-renewal-freeze-transitive-20261025T120000Z/renewal-weekly
EVID=$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/freeze-transitive-correction/g1-commit-20261025T120000Z
mkdir -p "$EVID"
exec > "$EVID/commands.log" 2>&1
echo "FIX $FIX"
run() { desc="$1"; shift; echo "\$ $* # $desc"; "$@" > "$EVID/$desc-stdout.txt" 2> "$EVID/$desc-stderr.txt"; ec=$?; echo $ec > "$EVID/$desc-exit.txt"; echo "-> exit=$ec"; return $ec; }
run head-pre git -C "$FIX" rev-parse HEAD
run diff-cached git -C "$FIX" diff --cached --name-only
run status-pre git -C "$FIX" status --porcelain=v1 --untracked-files=all
export GIT_AUTHOR_NAME=rephase-fixture
export GIT_AUTHOR_EMAIL=fixture@example.invalid
export GIT_COMMITTER_NAME=rephase-fixture
export GIT_COMMITTER_EMAIL=fixture@example.invalid
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
run commit-g1 git -C "$FIX" commit -m "G1 fixed736 + PUB freeze-transitive (shared wrapper union + M1-M6) before U authority"
run head-post git -C "$FIX" rev-parse HEAD
run log-post git -C "$FIX" log --oneline -3
run status-post git -C "$FIX" status --porcelain=v1 --untracked-files=all
run show-stat git -C "$FIX" show --stat HEAD
python3 -c "
import subprocess, pathlib
fix=pathlib.Path('$FIX')
p=subprocess.run(['git','--no-optional-locks','show','--name-only','--pretty=format:', 'HEAD'],cwd=str(fix),capture_output=True,text=True)
files=[l.strip() for l in p.stdout.splitlines() if l.strip()]
print(f'committed_files={len(files)}')
open('$EVID/committed-count.txt','w').write(str(len(files))+'\n')
"
echo "G1_DONE"
