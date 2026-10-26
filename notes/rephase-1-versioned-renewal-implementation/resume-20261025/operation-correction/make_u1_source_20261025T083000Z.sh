#!/bin/bash
# SOURCE commit ONLY code before NEW authority in u1-weekly-721 (preserve old tool ancestry 721a04d, oldE stays untracked live/COPY).
# Saved via Write before execution. No old runners, no network. Process-scoped Git identity.
set -u
U1=/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-operation-correction-20261025T060000Z/u1-weekly-721
EVID=/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-versioned-renewal-implementation/resume-20261025/operation-correction
export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0
export GIT_AUTHOR_NAME=renewal-test GIT_AUTHOR_EMAIL=renewal-test@example.invalid GIT_COMMITTER_NAME=renewal-test GIT_COMMITTER_EMAIL=renewal-test@example.invalid
# Isolation checks (read-only, no mutation): own .git, no alternates, inert origin, HEAD 721a04d.
git --no-optional-locks -C "$U1" rev-parse HEAD > "$EVID/u1-721-source-head-pre-stdout.txt" 2> "$EVID/u1-721-source-head-pre-stderr.txt"
echo $? > "$EVID/u1-721-source-head-pre-exit.txt"
git --no-optional-locks -C "$U1" remote -v > "$EVID/u1-721-source-remote-stdout.txt" 2> "$EVID/u1-721-source-remote-stderr.txt"
# Stage ONLY code (scripts/schemas/tests/config/.github/workflows) – NOT oldE (architecture-*/raw/sources/...).
git --no-optional-locks -C "$U1" add -- scripts schemas tests config .github/workflows 2> "$EVID/u1-721-source-add-stderr.txt"
echo $? > "$EVID/u1-721-source-add-exit.txt"
git --no-optional-locks -C "$U1" status --porcelain=v1 --untracked-files=all | head -n 50 > "$EVID/u1-721-source-status-staged-stdout.txt" 2> "$EVID/u1-721-source-status-staged-stderr.txt"
# Commit with meaningful message, real available ancestry (parent 721a04d), preserve old tool ancestry, no fake root.
git --no-optional-locks -C "$U1" commit -m "SOURCE: FIXED735 + PUB comprehensive B1 (isolated, not public; before NEW U1 authority; preserves 721a04d ancestry)" 2> "$EVID/u1-721-source-commit-stderr.txt" > "$EVID/u1-721-source-commit-stdout.txt"
echo $? > "$EVID/u1-721-source-commit-exit.txt"
git --no-optional-locks -C "$U1" rev-parse HEAD > "$EVID/u1-721-source-head-post-stdout.txt" 2> "$EVID/u1-721-source-head-post-stderr.txt"
git --no-optional-locks -C "$U1" log --oneline -3 > "$EVID/u1-721-source-log-stdout.txt" 2> "$EVID/u1-721-source-log-stderr.txt"
echo DONE
