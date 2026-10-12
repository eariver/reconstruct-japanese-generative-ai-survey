#!/usr/bin/env bash
# DM021-P1 Phase A overlay — NEW script authored 2026-10-11T16:00:37Z.
# Applies the COMPLETE 9-file LF2I patch AS SAVED (not LF1 first) onto the
# restored actual409 worktree, then verifies 9 hashes/modes + 2M7A status.
# Fail-closed: any gate failure aborts; no index touch, no commit, no fetch.
set -euo pipefail

unset GIT_DIR GIT_WORK_TREE GIT_PREFIX GIT_INDEX_FILE GIT_OBJECT_DIRECTORY \
  GIT_ALTERNATE_OBJECT_DIRECTORIES 2>/dev/null || true
export GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file
export GIT_CEILING_DIRECTORIES=/tmp/opencode
export TZ=UTC

WS=/home/eariver/git/reconstruct-japanese-generative-ai-survey
EVID=$WS/notes/rephase-1-dm021-p1/evidence-20261011T160037Z-phaseA
PATCH=$WS/notes/rephase-1-longform-lf2-implementation/evidence-20261010T120000Z-correction3/complete-overlay.patch
MANIFEST=$WS/notes/rephase-1-longform-lf2-implementation/evidence-20261010T120000Z-correction3/hash-manifest.json
DEST=/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z
REPO=$DEST/candidate-partial-b40de60
RAW=$EVID/raw
FINAL=409b292756dd1277b9dfae87679934c0d2ce251c

echo "== P1B argv/preconditions =="
echo "argv: $0 $*"
test "$(git -C "$REPO" rev-parse HEAD)" = "$FINAL" || { echo "NOT_ON_409_ABORT"; exit 41; }
git -C "$REPO" status --porcelain | tee "$RAW/status-pre-overlay.txt"
test ! -s "$RAW/status-pre-overlay.txt" || { echo "PRE_OVERLAY_NOT_CLEAN"; exit 42; }
echo "PRECONDITIONS_OK"
echo "5c7e7503851f5cdbc30b6827560219f48ce75d4a6cf64ba13516ed97e0cea4f9  $PATCH" | sha256sum -c -
grep -c '^diff --git' "$PATCH" | tee "$RAW/patch-hunk-count.txt"
git -C "$REPO" apply --check "$PATCH" && echo "APPLY_CHECK_SILENT_OK"

echo "== P1B apply worktree-only =="
git -C "$REPO" apply "$PATCH"; echo "apply-exit:$?"
git -C "$REPO" status --porcelain | tee "$RAW/status-post-overlay.txt"

echo "== P1B 2M7A status gate =="
awk '$1=="M"{m++} $1=="??"{n++} END{print "M="m+0" NEW="n+0}' "$RAW/status-post-overlay.txt" | tee "$RAW/status-2m7a.txt"
grep -c '^ M' "$RAW/status-post-overlay.txt" | tee "$RAW/status-m-count.txt"
test "$(cat "$RAW/status-m-count.txt")" = "2" || { echo "M_COUNT_MISMATCH"; exit 43; }
grep -c '^??' "$RAW/status-post-overlay.txt" | tee "$RAW/status-new-count.txt"
test "$(cat "$RAW/status-new-count.txt")" = "7" || { echo "NEW_COUNT_MISMATCH"; exit 44; }
echo "STATUS_2M7A_OK"

echo "== P1B 9-hash/mode verification (stdlib only, no app imports) =="
python3 - "$MANIFEST" "$REPO" "$RAW/nine-verify.txt" <<'EOF'
import hashlib, json, os, sys
manifest_path, repo, out = sys.argv[1], sys.argv[2], sys.argv[3]
manifest = json.load(open(manifest_path))
lines = []
ok = True
for path in sorted(manifest):
    exp = manifest[path]
    full = os.path.join(repo, path)
    data = open(full, 'rb').read()
    got = hashlib.sha256(data).hexdigest()
    st = os.stat(full)
    mode = oct(st.st_mode & 0o777)
    match = (got == exp['sha256'])
    ok = ok and match
    lines.append(f"{path} sha256_match={match} got={got} exp={exp['sha256']} mode={mode} manifest_mode={exp['mode']} bytes={len(data)}")
open(out, 'w').write("\n".join(lines) + "\n")
print("\n".join(lines))
sys.exit(0 if ok else 1)
EOF
echo "nine-verify-exit:$?"
cat "$RAW/nine-verify.txt"

echo "P1B_OVERLAY_DONE"
