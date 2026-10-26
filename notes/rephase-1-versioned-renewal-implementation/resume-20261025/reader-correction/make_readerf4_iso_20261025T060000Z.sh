#!/bin/bash
# Reader F4 isolated snapshot + test execution (author: Reader F4 only).
# No network, no old runners, no cleanup/reset, no ordinary candidate/reconstruct commit.
# Reads: frozen snapshot (READONLY) + writable candidate OWN files only.
# Writes: NEW isolated snapshot + notes/.../resume-20261025/reader-correction/ evidence only.
set -u
export LC_ALL=C
export PYTHONDONTWRITEBYTECODE=1
export GIT_NO_LAZY_FETCH=1
export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL=/dev/null
export GIT_OPTIONAL_LOCKS=0
# Fail if inherited GIT_DIR/WORK_TREE/INDEX_FILE (must be clean).
if [ -n "${GIT_DIR:-}" ] || [ -n "${GIT_WORK_TREE:-}" ] || [ -n "${GIT_INDEX_FILE:-}" ]; then
  echo "FAIL inherited GIT_*"
  exit 2
fi
RECON="/home/eariver/git/reconstruct-japanese-generative-ai-survey"
SNAP="$RECON/.rephase-1-editorial-runtime/versioned-renewal-freeze-20261024T174422Z/snapshot-work"
WORK="$RECON/.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work"
ISO_PARENT="$RECON/.rephase-1-editorial-runtime/versioned-renewal-readerf4-20261025T060000Z"
DST="$ISO_PARENT/snapshot-work"
EVID="$RECON/notes/rephase-1-versioned-renewal-implementation/resume-20261025/reader-correction"
WEEKLY="$RECON/.rephase-1-editorial-runtime/versioned-renewal-high24-20261025T040000Z/renewal-weekly"
echo "SNAP=$SNAP"
echo "WORK=$WORK"
echo "DST=$DST"
echo "EVID=$EVID"
echo "WEEKLY=$WEEKLY"
# Pre-checks (read-only).
git -C "$SNAP" rev-parse HEAD
git -C "$SNAP" status --porcelain=v1 --untracked-files=all | wc -l
git -C "$WORK" rev-parse HEAD
sha256sum "$SNAP/scripts/survey_reader_publication_v2.py"
sha256sum "$WORK/scripts/survey_reader_publication_v2.py"
sha256sum "$WORK/tests/test_versioned_renewal_reader_f4_20261025.py"
test -d "$WEEKLY"
test -f "$WEEKLY/sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/renewals/high-c1-weekly/reader-manuscript-v2.json"
test -f "$WEEKLY/sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/renewals/high-c1-weekly/renewal-source-proof.json"
# mkdir DST (fail-closed if exists).
mkdir -p "$ISO_PARENT"
if [ -e "$DST" ]; then
  echo "FAIL DST exists: $DST"
  exit 2
fi
mkdir "$DST"
# Byte-independent .git copy (no hardlinks).
cp -a "$SNAP/.git" "$DST/.git"
# Verify .git isolation.
git -C "$DST" rev-parse --absolute-git-dir
git -C "$DST" rev-parse HEAD
git -C "$DST" config --list --show-origin | head -n 20
test ! -f "$DST/.git/objects/info/alternates"
# Populate worktree: copy 731 intended files from SNAP (excluding .git/pycache/pyc).
python3 - "$SNAP" "$DST" <<'PY'
import pathlib, hashlib, shutil, sys
src = pathlib.Path(sys.argv[1])
dst = pathlib.Path(sys.argv[2])
files = [p for p in src.rglob('*') if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts and p.suffix != '.pyc']
print(f"SRC_COUNT={len(files)}")
assert len(files) == 731, f"expected 731, got {len(files)}"
for p in files:
    rel = p.relative_to(src)
    d = dst / rel
    d.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(p, d)
    # verify bytes
    assert hashlib.sha256(p.read_bytes()).hexdigest() == hashlib.sha256(d.read_bytes()).hexdigest(), f"mismatch {rel}"
print("POPULATE_731_OK")
PY
# Overwrite OWN files only: fixed reader + new dedicated test.
cp "$WORK/scripts/survey_reader_publication_v2.py" "$DST/scripts/survey_reader_publication_v2.py"
cp "$WORK/tests/test_versioned_renewal_reader_f4_20261025.py" "$DST/tests/test_versioned_renewal_reader_f4_20261025.py"
sha256sum "$DST/scripts/survey_reader_publication_v2.py"
sha256sum "$DST/tests/test_versioned_renewal_reader_f4_20261025.py"
# Verify counts: 731 + 1 new test = 732 files.
python3 - "$DST" <<'PY'
import pathlib, sys
dst = pathlib.Path(sys.argv[1])
files = [p for p in dst.rglob('*') if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts and p.suffix != '.pyc']
print(f"DST_COUNT={len(files)}")
assert len(files) == 732, f"expected 732, got {len(files)}"
print("DST_COUNT_OK")
PY
# Verify no hardlinks (nlink==1) and dev:ino disjoint vs SNAP (sample check).
python3 - "$SNAP" "$DST" <<'PY'
import pathlib, sys, os
snap = pathlib.Path(sys.argv[1]); dst = pathlib.Path(sys.argv[2])
# Check DST nlink==1 for all worktree files.
for p in dst.rglob('*'):
    if p.is_file() and '.git' not in p.parts:
        assert p.stat().st_nlink == 1, f"hardlink found {p}"
print("NOLINK_OK")
# Check .git dev:ino disjoint (sample: HEAD files).
snap_git = list((snap/'.git').rglob('*'))
dst_git = list((dst/'.git').rglob('*'))
snap_inos = {(f.stat().st_dev, f.stat().st_ino) for f in snap_git if f.is_file()}
dst_inos = {(f.stat().st_dev, f.stat().st_ino) for f in dst_git if f.is_file()}
assert snap_inos.isdisjoint(dst_inos), "git inode overlap"
print(f"GIT_DISJOINT_OK src_git={len(snap_inos)} dst_git={len(dst_inos)}")
PY
# AST + JSON checks (stdlib, no project import).
python3 - "$DST" <<'PY'
import ast, json, pathlib, sys
dst = pathlib.Path(sys.argv[1])
ast.parse((dst/'scripts/survey_reader_publication_v2.py').read_text())
print("AST_OK")
for rel in ['schemas/reader-manuscript-v2.schema.json']:
    json.loads((dst/rel).read_text())
    print(f"JSON_OK {rel}")
PY
# Git status in DST (expect 39M + 43U = 82 lines? 39 modified + 43 untracked).
git -C "$DST" status --porcelain=v1 --untracked-files=all | sort > "$EVID/dst-status-pre-commit-stdout.txt"
cat "$EVID/dst-status-pre-commit-stdout.txt"
git -C "$DST" diff HEAD --name-only | sort
echo "PRE_COMMIT_STATUS_DONE"
