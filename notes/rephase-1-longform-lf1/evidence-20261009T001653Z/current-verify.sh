#!/bin/bash
# LF-1 current verification (read-only supplement, 2026-10-09).
# Verifies CURRENT copy state only; not retroactive copy-time certification.
# No writes to source/dst DBs, no fixture/test execution, no network/fetch.
export GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file
SRC=/tmp/opencode/jgas-dm004-impl-20261004T234416Z
DST=/tmp/opencode/jgas-lf1-design-20261009T001653Z
echo "== 1. proposal preserved =="
sha256sum /home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-longform-lf1/evidence-20261009T001653Z/design-proposal.md; echo "exit:$?"
wc -l /home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-longform-lf1/evidence-20261009T001653Z/design-proposal.md; echo "exit:$?"
echo "== 2. DST identity =="
git -C "$DST" rev-parse HEAD; echo "exit:$?"
git -C "$DST" rev-parse 'HEAD^{tree}'; echo "exit:$?"
git -C "$DST" rev-parse 'HEAD^'; echo "exit:$?"
git -C "$DST" status --porcelain=v1 --untracked-files=all; echo "status_exit:$?"
echo "== 3. SRC identity (current) =="
git -C "$SRC" rev-parse HEAD; echo "exit:$?"
git -C "$SRC" rev-parse 'HEAD^{tree}'; echo "exit:$?"
git -C "$SRC" status --porcelain=v1 --untracked-files=all; echo "status_exit:$?"
echo "== 4. remotes/shallow/alternates/overrides =="
git -C "$DST" remote -v; echo "exit:$?"
git -C "$DST" rev-parse --is-shallow-repository; echo "exit:$?"
ls -l "$DST/.git/objects/info/alternates"; echo "exit:$?"
ls -l "$SRC/.git/objects/info/alternates"; echo "exit:$?"
env | grep -E '^GIT_(DIR|WORK_TREE|CEILING|COMMON)' || echo "(no GIT root overrides)"; echo "exit:$?"
git -C "$DST" config --get-all extensions.partialClone || echo "(no partialClone)"; echo "exit:$?"
echo "== 5. device+inode separation (sample objects) =="
for f in "$DST"/.git/objects/40/9b292756dd1277b9dfae87679934c0d2ce251c "$DST"/.git/objects/34/f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4; do
  rel=${f#$DST/}; echo "DST $rel $(stat -c 'dev=%d ino=%i nlink=%h' "$f")"; echo "exit:$?"
  echo "SRC $rel $(stat -c 'dev=%d ino=%i nlink=%h' "$SRC/$rel")"; echo "exit:$?"
done
echo -n "objects_nlink_gt1_dst:"; find "$DST/.git/objects" -type f -links +1 | wc -l; echo "exit:$?"
echo -n "shared_inodes:"; comm -12 <(find "$SRC/.git/objects" -type f -printf '%i\n' | sort -u) <(find "$DST/.git/objects" -type f -printf '%i\n' | sort -u) | wc -l; echo "exit:$?"
echo "== 6. byte comparison (worktrees incl .git) =="
diff -r -q "$SRC" "$DST"; echo "diff_exit:$?"
echo "== 7. refs (no new writes by this unit) =="
git -C "$DST" for-each-ref; echo "exit:$?"
diff <(git -C "$SRC" for-each-ref) <(git -C "$DST" for-each-ref) && echo "(refs identical)"; echo "exit:$?"
echo "== 8. reconstruct (read-only) =="
git -C /home/eariver/git/reconstruct-japanese-generative-ai-survey rev-parse HEAD; echo "exit:$?"
git -C /home/eariver/git/reconstruct-japanese-generative-ai-survey status --porcelain=v1 --untracked-files=all; echo "exit:$?"
echo "DONE"
