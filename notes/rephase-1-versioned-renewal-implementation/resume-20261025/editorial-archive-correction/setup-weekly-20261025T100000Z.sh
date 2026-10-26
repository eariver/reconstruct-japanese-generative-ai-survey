#!/bin/bash
# WEEKLY archive-correction setup: NEW independent clone valid U4 + 739 base + patch SOURCE-only G6
set -u
REPO="/home/eariver/git/reconstruct-japanese-generative-ai-survey"
SRC_FIX="$REPO/.rephase-1-editorial-runtime/versioned-renewal-weekly-continuation-20261025T083000Z/renewal-weekly"
DST_PARENT="$REPO/.rephase-1-editorial-runtime/versioned-renewal-editorial-archive-weekly-20261025T100000Z"
DST="$DST_PARENT/renewal-weekly"
EVID="$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/editorial-archive-correction/setup-weekly-20261025T100000Z"
CAND="$REPO/.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work"
FIXED739="$REPO/.rephase-1-editorial-runtime/versioned-renewal-repair-input-20261025T082826Z/snapshot-work"
mkdir -p "$EVID" "$DST_PARENT"
exec >"$EVID/commands.log" 2>&1
echo "SETUP WEEKLY start $(date -u +%Y-%m-%dT%H:%M:%SZ) PID=$$"
for v in GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; do
  if [ -n "${!v:-}" ]; then echo "FATAL inherited $v"; exit 2; fi
done
git -C "$SRC_FIX" rev-parse HEAD >"$EVID/src-head-stdout.txt" 2>"$EVID/src-head-stderr.txt"; echo $? >"$EVID/src-head-exit.txt"
git -C "$SRC_FIX" log --oneline -6 >"$EVID/src-log-stdout.txt" 2>"$EVID/src-log-stderr.txt"; echo $? >"$EVID/src-log-exit.txt"
if [ -e "$DST" ]; then echo "FATAL DST exists"; exit 2; fi
git clone --no-hardlinks "$SRC_FIX" "$DST" >"$EVID/clone-stdout.txt" 2>"$EVID/clone-stderr.txt"; echo $? >"$EVID/clone-exit.txt"
git -C "$DST" remote set-url origin https://example.invalid/versioned-renewal-editorial-archive-weekly.git
git -C "$DST" remote -v >"$EVID/remote-stdout.txt" 2>"$EVID/remote-stderr.txt"; echo $? >"$EVID/remote-exit.txt"
git -C "$DST" rev-parse --absolute-git-dir >"$EVID/gitdir-stdout.txt" 2>"$EVID/gitdir-stderr.txt"; echo $? >"$EVID/gitdir-exit.txt"
if [ -e "$DST/.git/objects/info/alternates" ]; then echo "FATAL alternates"; exit 2; fi
echo "0" >"$EVID/noalternates-exit.txt"
python3 -c "import pathlib; dst=pathlib.Path('$DST'); src=pathlib.Path('$SRC_FIX'); assert (dst/'templates/survey/jgaisurvey.sty').stat().st_nlink==1; assert (dst/'templates/survey/jgaisurvey.sty').stat().st_ino != (src/'templates/survey/jgaisurvey.sty').stat().st_ino; print('inode OK')" >"$EVID/inode-stdout.txt" 2>"$EVID/inode-stderr.txt"; echo $? >"$EVID/inode-exit.txt"
sha256sum "$DST/templates/survey/jgaisurvey.sty" >"$EVID/style-pre-stdout.txt" 2>"$EVID/style-pre-stderr.txt"; echo $? >"$EVID/style-pre-exit.txt"
# Overlay FIXED739 except style (preserve a4bd variant)
python3 <<'PY'
import hashlib, pathlib, shutil
repo=pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
fixed=repo/".rephase-1-editorial-runtime/versioned-renewal-repair-input-20261025T082826Z/snapshot-work"
dst=repo/".rephase-1-editorial-runtime/versioned-renewal-editorial-archive-weekly-20261025T100000Z/renewal-weekly"
evid=repo/"notes/rephase-1-versioned-renewal-implementation/resume-20261025/editorial-archive-correction/setup-weekly-20261025T100000Z"
manifest=repo/"notes/rephase-1-versioned-renewal-implementation/resume-20261025/integration-repair-input-evidence-20261025T082826Z/dst-hash-intended-stdout.txt"
lines=[l.strip() for l in manifest.read_text().splitlines() if l.strip()]
mism=[]
for line in lines:
    parts=line.split()
    if len(parts)!=3: continue
    sha, size_s, rel = parts
    size=int(size_s)
    if rel=="templates/survey/jgaisurvey.sty":
        continue
    src=fixed/rel
    d=dst/rel
    assert src.is_file(), f"missing fixed {rel}"
    d.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, d)
    got=hashlib.sha256(d.read_bytes()).hexdigest()
    if got!=sha or d.stat().st_size!=size:
        mism.append((rel, got, sha))
(ev:=evid/"overlay-739-stdout.txt").write_text(f"overlay 738 (style preserved), mism={mism}\n")
assert mism==[], f"mism {mism}"
print("OVERLAY_739_OK")
PY
echo $? >"$EVID/overlay-739-exit.txt"
python3 <<'PY'
import hashlib, pathlib, shutil
repo=pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
cand=repo/".rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work"
dst=repo/".rephase-1-editorial-runtime/versioned-renewal-editorial-archive-weekly-20261025T100000Z/renewal-weekly"
for rel in ["scripts/survey_editorial_publication_v2.py", "tests/test_editorial_renewal_archive_correction_20261025.py"]:
    src=cand/rel
    d=dst/rel
    d.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, d)
    print(rel, hashlib.sha256(d.read_bytes()).hexdigest())
print("PATCH_OVERLAY_OK")
PY
echo $? >"$EVID/patch-overlay-exit.txt"
sha256sum "$DST/templates/survey/jgaisurvey.sty" >"$EVID/style-post-stdout.txt" 2>"$EVID/style-post-stderr.txt"; echo $? >"$EVID/style-post-exit.txt"
cat >"$EVID/variant-manifest.txt" <<'EOF'
739 BASE (20f1967f) + style a4bd135aa2876079923ba16cc2963c73647e49a3f1460806483d9c092827 variant (not baseline 035645) + patch edpub 85814124 + new test 5e5a0bdc
H6fe86/P1825dba/PUB3f4039 stable; S20f/HIGH9a/Reader098 stable; style preserved for U reuse
EOF
git -C "$DST" status --porcelain=v1 --untracked-files=all >"$EVID/status-pre-stdout.txt" 2>"$EVID/status-pre-stderr.txt"; echo $? >"$EVID/status-pre-exit.txt"
git -C "$DST" add scripts/survey_editorial_publication_v2.py tests/test_editorial_renewal_archive_correction_20261025.py >"$EVID/add-stdout.txt" 2>"$EVID/add-stderr.txt"; echo $? >"$EVID/add-exit.txt"
git -C "$DST" diff --cached --name-only >"$EVID/diff-cached-stdout.txt" 2>"$EVID/diff-cached-stderr.txt"; echo $? >"$EVID/diff-cached-exit.txt"
git -C "$DST" -c user.name="archive-correction" -c user.email="archive@example.invalid" commit -m "WEEKLY TEST-ONLY: G6 archive-correction edpub kind-aware renewal authoring_refs + new test (style a4bd preserved for U reuse)" >"$EVID/commit-stdout.txt" 2>"$EVID/commit-stderr.txt"; echo $? >"$EVID/commit-exit.txt"
git -C "$DST" rev-parse HEAD >"$EVID/head-post-stdout.txt" 2>"$EVID/head-post-stderr.txt"; echo $? >"$EVID/head-post-exit.txt"
git -C "$DST" log --oneline -8 >"$EVID/log-post-stdout.txt" 2>"$EVID/log-post-stderr.txt"; echo $? >"$EVID/log-post-exit.txt"
git -C "$DST" merge-base --is-ancestor 721a04d85532d7855f3e54cc411f5847f787726e HEAD; echo $? >"$EVID/ancestor-exit.txt"
echo "SETUP WEEKLY DONE"
