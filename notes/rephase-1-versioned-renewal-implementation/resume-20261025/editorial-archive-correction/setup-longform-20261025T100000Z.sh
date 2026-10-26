#!/bin/bash
# LONGFORM archive-correction setup: NEW independent clone valid U4 + 739 base + patch SOURCE-only G7
# No candidate/INPUT/old-fixture edits, no network/old runners/cleanup/cache purge.
set -u
REPO="/home/eariver/git/reconstruct-japanese-generative-ai-survey"
SRC_FIX="$REPO/.rephase-1-editorial-runtime/versioned-renewal-longform-repair-20261025T090000Z/renewal-longform"
DST_PARENT="$REPO/.rephase-1-editorial-runtime/versioned-renewal-editorial-archive-longform-20261025T100000Z"
DST="$DST_PARENT/renewal-longform"
EVID="$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/editorial-archive-correction/setup-longform-20261025T100000Z"
CAND="$REPO/.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work"
FIXED739="$REPO/.rephase-1-editorial-runtime/versioned-renewal-repair-input-20261025T082826Z/snapshot-work"
mkdir -p "$EVID" "$DST_PARENT"
exec >"$EVID/commands.log" 2>&1
echo "SETUP LONGFORM start $(date -u +%Y-%m-%dT%H:%M:%SZ) PID=$$"
echo "SRC_FIX=$SRC_FIX"
echo "DST=$DST"
echo "CAND=$CAND"
echo "FIXED739=$FIXED739"
# Guards: no inherited GIT_*
for v in GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; do
  if [ -n "${!v:-}" ]; then echo "FATAL inherited $v"; exit 2; fi
done
# Verify SRC valid U4 r7
git -C "$SRC_FIX" rev-parse HEAD >"$EVID/src-head-stdout.txt" 2>"$EVID/src-head-stderr.txt"; echo $? >"$EVID/src-head-exit.txt"
cat "$EVID/src-head-stdout.txt"
git -C "$SRC_FIX" log --oneline -6 >"$EVID/src-log-stdout.txt" 2>"$EVID/src-log-stderr.txt"; echo $? >"$EVID/src-log-exit.txt"
# Verify FIXED739 manifest
ls "$FIXED739" >"$EVID/fixed-ls-stdout.txt" 2>"$EVID/fixed-ls-stderr.txt"; echo $? >"$EVID/fixed-ls-exit.txt"
# Clone --no-hardlinks, inert origin
if [ -e "$DST" ]; then echo "FATAL DST exists $DST"; exit 2; fi
git clone --no-hardlinks "$SRC_FIX" "$DST" >"$EVID/clone-stdout.txt" 2>"$EVID/clone-stderr.txt"; echo $? >"$EVID/clone-exit.txt"
cat "$EVID/clone-exit.txt"
git -C "$DST" remote set-url origin https://example.invalid/versioned-renewal-editorial-archive-longform.git
git -C "$DST" remote -v >"$EVID/remote-stdout.txt" 2>"$EVID/remote-stderr.txt"; echo $? >"$EVID/remote-exit.txt"
git -C "$DST" rev-parse --absolute-git-dir >"$EVID/gitdir-stdout.txt" 2>"$EVID/gitdir-stderr.txt"; echo $? >"$EVID/gitdir-exit.txt"
cat "$EVID/gitdir-stdout.txt"
# no alternates
if [ -e "$DST/.git/objects/info/alternates" ]; then echo "FATAL alternates"; exit 2; fi
echo "0" >"$EVID/noalternates-exit.txt"
# nlink==1, dev:ino disjoint (sample)
python3 -c "import os, pathlib; dst=pathlib.Path('$DST'); src=pathlib.Path('$SRC_FIX'); assert (dst/'templates/survey/jgaisurvey.sty').stat().st_nlink==1; assert (dst/'templates/survey/jgaisurvey.sty').stat().st_ino != (src/'templates/survey/jgaisurvey.sty').stat().st_ino; print('inode OK')" >"$EVID/inode-stdout.txt" 2>"$EVID/inode-stderr.txt"; echo $? >"$EVID/inode-exit.txt"
# Verify style variant preserved pre-overlay (b1cbb)
sha256sum "$DST/templates/survey/jgaisurvey.sty" >"$EVID/style-pre-stdout.txt" 2>"$EVID/style-pre-stderr.txt"; echo $? >"$EVID/style-pre-exit.txt"
cat "$EVID/style-pre-stdout.txt"
# Overlay FIXED739 739 files except style (preserve b1cbb variant, else U would become C)
python3 <<'PY'
import hashlib, pathlib, shutil
repo=pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
fixed=repo/".rephase-1-editorial-runtime/versioned-renewal-repair-input-20261025T082826Z/snapshot-work"
dst=repo/".rephase-1-editorial-runtime/versioned-renewal-editorial-archive-longform-20261025T100000Z/renewal-longform"
evid=repo/"notes/rephase-1-versioned-renewal-implementation/resume-20261025/editorial-archive-correction/setup-longform-20261025T100000Z"
# Load dst-hash-intended list (739 lines) from integration-repair evidence
manifest=repo/"notes/rephase-1-versioned-renewal-implementation/resume-20261025/integration-repair-input-evidence-20261025T082826Z/dst-hash-intended-stdout.txt"
lines=[l.strip() for l in manifest.read_text().splitlines() if l.strip()]
print(f"manifest lines {len(lines)}")
mism=[]
for line in lines:
    parts=line.split()
    if len(parts)!=3: continue
    sha, size_s, rel = parts
    size=int(size_s)
    if rel=="templates/survey/jgaisurvey.sty":
        continue  # preserve fixture variant b1cbb, not baseline 035645
    src=fixed/rel
    d=dst/rel
    assert src.is_file(), f"missing fixed {rel}"
    assert d.is_file() or not d.exists(), f"unexpected {rel}"
    # copy2 + SHA verify
    d.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, d)
    got=hashlib.sha256(d.read_bytes()).hexdigest()
    if got!=sha or d.stat().st_size!=size:
        mism.append((rel, got, sha))
(ev=evid/"overlay-739-stdout.txt").write_text(f"overlay 738 (style preserved), mism={mism}\n")
assert mism==[], f"mism {mism}"
print("OVERLAY_739_OK")
PY
echo $? >"$EVID/overlay-739-exit.txt"
cat "$EVID/overlay-739-stdout.txt"
# Overlay patch: edpub new + new test (from candidate-work)
python3 <<'PY'
import hashlib, pathlib, shutil
repo=pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
cand=repo/".rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work"
dst=repo/".rephase-1-editorial-runtime/versioned-renewal-editorial-archive-longform-20261025T100000Z/renewal-longform"
evid=repo/"notes/rephase-1-versioned-renewal-implementation/resume-20261025/editorial-archive-correction/setup-longform-20261025T100000Z"
for rel in ["scripts/survey_editorial_publication_v2.py", "tests/test_editorial_renewal_archive_correction_20261025.py"]:
    src=cand/rel
    d=dst/rel
    assert src.is_file(), f"missing cand {rel}"
    d.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, d)
    print(rel, hashlib.sha256(d.read_bytes()).hexdigest(), d.stat().st_size)
    (evid/f"patch-{pathlib.Path(rel).name}-sha.txt").write_text(f"{hashlib.sha256(d.read_bytes()).hexdigest()} {d.stat().st_size} {rel}\n")
print("PATCH_OVERLAY_OK")
PY
echo $? >"$EVID/patch-overlay-exit.txt"
# Verify style still b1cbb variant
sha256sum "$DST/templates/survey/jgaisurvey.sty" >"$EVID/style-post-stdout.txt" 2>"$EVID/style-post-stderr.txt"; echo $? >"$EVID/style-post-exit.txt"
cat "$EVID/style-post-stdout.txt"
# Variant manifest
cat >"$EVID/variant-manifest.txt" <<'EOF'
739 BASE (20f1967f, 739 files) + style b1cbbdd93711aef17b37d3bbbedda25aa0bcb51f462bdc7ad172ce2aa103c8f4 variant (not baseline 035645) + patch edpub 85814124 + new test 5e5a0bdc
H6fe86/P1825dba/PUB3f4039 stable; S20f/HIGH9a/Reader098 stable; style preserved for U reuse (baseline would force C new targets)
EOF
cat "$EVID/variant-manifest.txt"
# SOURCE-only git add 2 paths (edpub M + new test U), E overlap 0
git -C "$DST" status --porcelain=v1 --untracked-files=all >"$EVID/status-pre-stdout.txt" 2>"$EVID/status-pre-stderr.txt"; echo $? >"$EVID/status-pre-exit.txt"
cat "$EVID/status-pre-stdout.txt"
git -C "$DST" add scripts/survey_editorial_publication_v2.py tests/test_editorial_renewal_archive_correction_20261025.py >"$EVID/add-stdout.txt" 2>"$EVID/add-stderr.txt"; echo $? >"$EVID/add-exit.txt"
git -C "$DST" diff --cached --name-only >"$EVID/diff-cached-stdout.txt" 2>"$EVID/diff-cached-stderr.txt"; echo $? >"$EVID/diff-cached-exit.txt"
cat "$EVID/diff-cached-stdout.txt"
# Commit G7 SOURCE-only (no E rewrite, no git add -A)
git -C "$DST" -c user.name="archive-correction" -c user.email="archive@example.invalid" commit -m "LONGFORM TEST-ONLY: G7 archive-correction edpub kind-aware renewal authoring_refs + new test (style b1cbb preserved for U reuse)" >"$EVID/commit-stdout.txt" 2>"$EVID/commit-stderr.txt"; echo $? >"$EVID/commit-exit.txt"
cat "$EVID/commit-exit.txt"
git -C "$DST" rev-parse HEAD >"$EVID/head-post-stdout.txt" 2>"$EVID/head-post-stderr.txt"; echo $? >"$EVID/head-post-exit.txt"
cat "$EVID/head-post-stdout.txt"
git -C "$DST" log --oneline -8 >"$EVID/log-post-stdout.txt" 2>"$EVID/log-post-stderr.txt"; echo $? >"$EVID/log-post-exit.txt"
cat "$EVID/log-post-stdout.txt"
# Ancestor check
git -C "$DST" merge-base --is-ancestor 721a04d85532d7855f3e54cc411f5847f787726e HEAD; echo $? >"$EVID/ancestor-exit.txt"
echo "SETUP LONGFORM DONE"
