#!/bin/bash
# Final R5b SOURCE freeze from actual DST (strict/close/canonical/export/pin + foreign-inode fix).
# Workspace-local runtime (authorized), no /tmp snapshot (EDQUOT proven), no new /home (preserve deviation).
# Intended paths from previous r5 manifest (720) + R5b modifications (no new paths, count stays 720 actual).
# Excludes DST caches/tmpvr/evidence/ignored outputs. Own new DB, inert origin, no sharing.
# Process identity only, no ordinary (reconstruct) commit. Meaningful fixture commit authorized.
set -euo pipefail
echo "=== R5b freeze start ==="
echo "DST=/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60"
echo "FROZEN_BASE=/tmp/opencode/jgas-editorial-r4d-20261021T170000Z/candidate-partial-b40de60 (4191503, 719 files, read-only)"
echo "NEWROOT(workpace-local, ignored)=/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/jgas-editorial-r5b-20261022T140000Z/candidate-partial-b40de60"
DST=/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60
FROZEN=/tmp/opencode/jgas-editorial-r4d-20261021T170000Z/candidate-partial-b40de60
NEWROOT=/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/jgas-editorial-r5b-20261022T140000Z/candidate-partial-b40de60
R5_MANIFEST=/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-editorial-operation-implementation/correction-r5/source-manifest-r5.json
echo "--- verify DST own .git/toplevel/absolute GitDir NOT parent reconstruct ---"
git -C "$DST" rev-parse --show-toplevel
git -C "$DST" rev-parse --absolute-git-dir
git -C /home/eariver/git/reconstruct-japanese-generative-ai-survey rev-parse --show-toplevel
echo "--- verify DST inert origin/no alternates ---"
git -C "$DST" remote -v
ls "$DST/.git/objects/info/alternates" 2>&1 || echo "no objects/info/alternates (good)"
ls "$DST/.git/info/alternates" 2>&1 || echo "no info/alternates (good)"
echo "--- check workspace-local quota (df + touch probe, return concrete error if blocked, no other root) ---"
df -h /home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime
touch /home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/.quota-probe-r5b && echo "touch probe OK" && rm /home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/.quota-probe-r5b && echo "rm probe OK"
echo "--- create NEWROOT (unique, ignored scratch) ---"
mkdir -p "$(dirname "$NEWROOT")"
echo "--- copy frozen base (719, read-only, approved /tmp) to NEWROOT (workspace-local, 355G avail, no EDQUOT) ---"
cp -a "$FROZEN" "$NEWROOT"
echo "copy base done"
echo "--- verify NEWROOT own .git/toplevel/absolute GitDir (must be NEWROOT, NOT parent reconstruct, NOT DST) ---"
git -C "$NEWROOT" rev-parse --show-toplevel
git -C "$NEWROOT" rev-parse --absolute-git-dir
echo "--- overlay intended 720 paths from DST (R5+R5b fixes, latest, no new paths) ---"
python3 - <<'PY'
import json, pathlib, shutil
r5_manifest = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-editorial-operation-implementation/correction-r5/source-manifest-r5.json")
data = json.loads(r5_manifest.read_text())
paths = [f["path"] for f in data["files"]]
print(f"intended paths from r5 manifest: {len(paths)} (actual, not assumed)")
dst = pathlib.Path("/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60")
newroot = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/jgas-editorial-r5b-20261022T140000Z/candidate-partial-b40de60")
missing = []
for rel in paths:
    src = dst / rel
    dst_p = newroot / rel
    if not src.is_file():
        # R5b has no new paths vs r5 manifest (720), but check anyway
        missing.append(rel)
        continue
    dst_p.parent.mkdir(parents=True, exist_ok=True)
    # copy content (not hardlink), preserve mode via shutil (copystat not needed, manifest records mode actual)
    # Use read_bytes/write_bytes to guarantee new inodes, no sharing, no hardlinks
    dst_p.write_bytes(src.read_bytes())
print(f"overlay done, missing (should be 0): {len(missing)}")
if missing:
    print("\n".join(missing[:20]))
    raise SystemExit(f"missing intended paths in DST: {len(missing)}")
PY
echo "--- verify NEWROOT file count actual (not assumed 720) ---"
find "$NEWROOT" -type f -not -path "*/.git/*" | wc -l
echo "--- git add + meaningful fixture commit (process identity only) ---"
export GIT_AUTHOR_NAME="worker-r5b"
export GIT_AUTHOR_EMAIL="worker-r5b@example.invalid"
export GIT_COMMITTER_NAME="worker-r5b"
export GIT_COMMITTER_EMAIL="worker-r5b@example.invalid"
export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL=/dev/null
export GIT_OPTIONAL_LOCKS=0
git -C "$NEWROOT" add -A
git -C "$NEWROOT" status --porcelain=v1 | head -n 20
git -C "$NEWROOT" -c user.name="worker-r5b" -c user.email="worker-r5b@example.invalid" commit -m "SOURCE snapshot: R5b strict/close/canonical/Profile-bound export/pin + foreign-inode replacement fix, 720 files (final R5b, supersedes outdated 0e092f9)"
echo "--- verify commit HEAD/tree 40char actual git ---"
git -C "$NEWROOT" rev-parse HEAD
git -C "$NEWROOT" rev-parse HEAD^{tree}
git -C "$NEWROOT" log --oneline -3
echo "--- verify clean/no alts/remotes/sharing, own GitDir ---"
git -C "$NEWROOT" status --porcelain=v1
git -C "$NEWROOT" remote -v
ls "$NEWROOT/.git/objects/info/alternates" 2>&1 || echo "no objects/info/alternates (good)"
ls "$NEWROOT/.git/info/alternates" 2>&1 || echo "no info/alternates (good)"
git -C "$NEWROOT" rev-parse --show-toplevel
git -C "$NEWROOT" rev-parse --absolute-git-dir
git -C "$NEWROOT" count-objects -v
echo "--- check no __pycache__/tmp residue, no hardlinks (4-sample nlink=1) ---"
find "$NEWROOT" -name "__pycache__" -o -name "*.pyc" | head -n 5 || echo "no caches (good)"
find "$NEWROOT" -maxdepth 2 -name "tmp*" | head -n 5 || echo "no tmp residue (good)"
find "$NEWROOT" -type f -not -path "*/.git/*" -links +1 | head -n 5 || echo "no hardlinks (good)"
python3 - <<'PY'
import os, pathlib
root = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/jgas-editorial-r5b-20261022T140000Z/candidate-partial-b40de60")
for rel in [".git/index", "scripts/survey_agent_control_v2.py", "templates/survey/jgaisurvey.sty", "schemas/publication-surface-revalidation.schema.json"]:
    p = root / rel
    st = os.stat(p)
    print(f"{rel} dev={st.st_dev} ino={st.st_ino} nlink={st.st_nlink}")
PY
echo "=== R5b freeze done (no tests in SOURCE) ==="
