#!/bin/bash
# FIXED TEST-ONLY complete SOURCE snapshot — latest 740 (candidate-work with P3S fix 9e2a0ad) + owned test patches, all intended fully tracked, no pycache.
# Saved via Write before execution. No old runners, no network. Fail-closed: set -u only, explicit rc.
set -u
REPO="/home/eariver/git/reconstruct-japanese-generative-ai-survey"
SRC="$REPO/.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work"
PATCHSRC="$REPO/.rephase-1-editorial-runtime/versioned-renewal-test-fixture-corrections-20261025T153000Z/test-source"
STAMP="20261025T170000Z"
PACKROOT="$REPO/.rephase-1-editorial-runtime/versioned-renewal-test-fixture-corrections-20261025T170000Z"
DST="$PACKROOT/test-source"
TMPLOCAL="$PACKROOT/tmp"
EVIDENCE="$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/test-fixture-corrections"
export PYTHONDONTWRITEBYTECODE=1
export LC_ALL=C

LOG="$EVIDENCE/commands-fixed-170000Z.log"
printf "stamp %s FIXED latest+P3Sfix+testpatches\n" "$STAMP" > "$LOG"

run() {
  tag="$1"; shift
  out="$EVIDENCE/${tag}-stdout.txt"
  err="$EVIDENCE/${tag}-stderr.txt"
  rcfile="$EVIDENCE/${tag}-exit.txt"
  env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_NO_LAZY_FETCH=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_OPTIONAL_LOCKS=0 PYTHONDONTWRITEBYTECODE=1 "$@" >"$out" 2>"$err"
  rc=$?
  printf "%s" "$rc" > "$rcfile"
  printf "run %s rc=%s cmd=%s\n" "$tag" "$rc" "$*" >> "$LOG"
  return $rc
}

fail() {
  printf "FAIL %s\n" "$1" >> "$LOG"
  echo "FAIL: $1" >&2
  exit 1
}

[ -d "$SRC/.git" ] || fail "SRC .git missing"
[ -d "$PATCHSRC/tests" ] || fail "PATCHSRC tests missing"
[ -e "$PACKROOT" ] && fail "PACKROOT already exists, need fresh unique id"
[ -e "$DST" ] && fail "DST already exists"
mkdir -p "$EVIDENCE" || fail "mkdir EVIDENCE"
mkdir -p "$TMPLOCAL" || fail "mkdir TMPLOCAL"
mkdir -p "$DST" || fail "mkdir DST"

run recon-head-fixed git -C "$REPO" --no-optional-locks rev-parse HEAD || fail "recon-head-fixed rc"
run recon-status-fixed git -C "$REPO" --no-optional-locks status --porcelain=v1 --untracked-files=all || fail "recon-status-fixed rc"
run recon-diff-cached-fixed git -C "$REPO" --no-optional-locks diff --cached --name-only || fail "recon-diff-cached-fixed rc"
[ -s "$EVIDENCE/recon-diff-cached-fixed-stdout.txt" ] && fail "recon index not clean"

run src-head-fixed git -C "$SRC" --no-optional-locks rev-parse HEAD || fail "src-head-fixed rc"
grep -q "^409b292756dd1277b9dfae87679934c0d2ce251c$" "$EVIDENCE/src-head-fixed-stdout.txt" || fail "SRC HEAD not 409"
run src-p3s-pin-fixed python3 - "$SRC/scripts/survey_editorial_staged_source_v2.py" <<'PYEOF'
import hashlib, sys
data = open(sys.argv[1], 'rb').read()
h = hashlib.sha256(data).hexdigest()
print(h)
assert h.startswith("9e2a0ad6"), f"P3S fix not present (latest 9e2a0ad...): {h}"
PYEOF
[ "$(cat "$EVIDENCE/src-p3s-pin-fixed-exit.txt")" = "0" ] || fail "src-p3s-pin-fixed failed (P3S fix 9e2a0ad not present)"

run cp-git-fixed cp -a "$SRC/.git" "$DST/.git" || fail "cp-git-fixed rc"
[ -d "$DST/.git" ] || fail "DST .git missing after cp"
run dst-git-count-fixed bash -c "find \"$DST/.git\" -type f | wc -l" || fail "dst-git-count-fixed rc"
run dst-noalternates-fixed bash -c "test ! -e \"$DST/.git/objects/info/alternates\" && test ! -e \"$DST/.git/objects/info\" && echo OK" || fail "DST alternates/info exists"
run dst-head-fixed git -C "$DST" --no-optional-locks rev-parse HEAD || fail "dst-head-fixed rc"
grep -q "^409b292756dd1277b9dfae87679934c0d2ce251c$" "$EVIDENCE/dst-head-fixed-stdout.txt" || fail "DST HEAD not 409 pre-populate"
run dst-remote-fixed git -C "$DST" --no-optional-locks remote -v || fail "dst-remote-fixed rc"
grep -q "example.invalid" "$EVIDENCE/dst-remote-fixed-stdout.txt" || fail "DST remote not inert"

run populate-fixed-worktree python3 - "$SRC" "$DST" <<'PYEOF'
import os, shutil, hashlib, sys
src, dst = sys.argv[1], sys.argv[2]
count = 0
for root, dirs, fnames in os.walk(src):
    if '.git' in dirs:
        dirs.remove('.git')
    dirs[:] = [d for d in dirs if d != '__pycache__']
    for f in fnames:
        if f.endswith('.pyc'):
            continue
        full = os.path.join(root, f)
        if '/.git/' in full:
            continue
        rel = os.path.relpath(full, src)
        # Skip empty sources/surveys dirs (no files under them in candidate-work)
        target = os.path.join(dst, rel)
        os.makedirs(os.path.dirname(target) or dst, exist_ok=True)
        shutil.copy2(full, target)
        a = open(full, 'rb').read()
        b = open(target, 'rb').read()
        assert a == b, f"copy mismatch {rel}"
        assert hashlib.sha256(a).hexdigest() == hashlib.sha256(b).hexdigest()
        count += 1
print(f"populate OK {count}")
assert count == 740, f"populated {count} != 740 (latest intended, no pycache)"
PYEOF
[ "$(cat "$EVIDENCE/populate-fixed-worktree-exit.txt")" = "0" ] || fail "populate-fixed-worktree failed"

run dst-count-fixed bash -c "find \"$DST\" -path \"$DST/.git\" -prune -o -type f -print | wc -l" || fail "dst-count-fixed rc"
grep -q "740" "$EVIDENCE/dst-count-fixed-stdout.txt" || fail "DST worktree not 740"

# Apply owned TEST-ONLY patches (test files only, no runtime): R1, H, S, P2R, P3S-O1 (Reader old as is, bare runner lives in notes).
run apply-owned-patches python3 - "$PATCHSRC" "$DST" <<'PYEOF'
import shutil, hashlib, sys
patchsrc, dst = sys.argv[1], sys.argv[2]
owned = [
    "tests/test_survey_weekly_mechanical_refresh_v2.py",
    "tests/test_versioned_renewal_history_phase_h.py",
    "tests/test_versioned_renewal_source_phase_s.py",
    "tests/test_versioned_renewal_reader_f4_20261025.py",
    "tests/test_survey_editorial_retention_v2.py",
    "tests/test_survey_editorial_staged_source_v2.py",
]
for rel in owned:
    a = open(f"{patchsrc}/{rel}", 'rb').read()
    b_path = f"{dst}/{rel}"
    # Reader old has no patches yet (same hash); copy anyway for exactness (no-op if same).
    open(b_path, 'wb').write(a)
    assert open(b_path, 'rb').read() == a, f"patch copy mismatch {rel}"
    print(f"{rel} {len(a)} {hashlib.sha256(a).hexdigest()}")
# Verify P3S runtime still latest fix (not touched by test patches).
p3s = open(f"{dst}/scripts/survey_editorial_staged_source_v2.py", 'rb').read()
h = hashlib.sha256(p3s).hexdigest()
print(f"scripts/survey_editorial_staged_source_v2.py {len(p3s)} {h}")
assert h.startswith("9e2a0ad6"), f"P3S fix lost after patches: {h}"
# Verify no pycache in DST worktree.
import os
for root, dirs, fnames in os.walk(dst):
    assert '__pycache__' not in dirs, f"pycache dir in DST {root}"
    for f in fnames:
        assert not f.endswith('.pyc'), f"pyc file in DST {root}/{f}"
print("owned patches applied, no pycache")
PYEOF
[ "$(cat "$EVIDENCE/apply-owned-patches-exit.txt")" = "0" ] || fail "apply-owned-patches failed"

run dst-pycache-check-fixed bash -c "find \"$DST\" -name \"*.pyc\" -o -name \"__pycache__\" | wc -l" || fail "dst-pycache-check-fixed rc"

run dst-add-fixed git -C "$DST" --no-optional-locks add -A || fail "dst-add-fixed rc"
run dst-status-fixed git -C "$DST" --no-optional-locks status --porcelain=v1 --untracked-files=all || fail "dst-status-fixed rc"
run dst-diff-cached-fixed git -C "$DST" --no-optional-locks diff --cached --name-only || fail "dst-diff-cached-fixed rc"
run dst-diff-cached-stat-fixed git -C "$DST" --no-optional-locks diff --cached --stat || fail "dst-diff-cached-stat-fixed rc"
# All intended fully tracked: no unstaged (worktree clean vs index), no untracked (all intended added, no pycache).
run dst-status-unstaged-fixed bash -c "git -C \"$DST\" --no-optional-locks status --porcelain=v1 --untracked-files=all | grep -v \"^[MA]\" | wc -l" || fail "dst-status-unstaged-fixed rc"

run dst-commit-fixed git -C "$DST" --no-optional-locks -c user.name="Synthetic Test Fixture" -c user.email="fixture@example.invalid" commit -q -m "TEST-ONLY: FIXED complete 740+P3S fix(9e2a0ad)+test patches SOURCE before authority" || fail "dst-commit-fixed rc"
run dst-head-post-fixed git -C "$DST" --no-optional-locks rev-parse HEAD || fail "dst-head-post-fixed rc"
run dst-status-post-fixed git -C "$DST" --no-optional-locks status --porcelain=v1 --untracked-files=all || fail "dst-status-post-fixed rc"
[ -s "$EVIDENCE/dst-status-post-fixed-stdout.txt" ] && fail "DST not clean after FIXED commit"
run dst-log-post-fixed git -C "$DST" --no-optional-locks log --oneline -3 || fail "dst-log-post-fixed rc"
run dst-pin-fixed python3 - "$DST" <<'PYEOF'
import hashlib, pathlib, sys
dst = pathlib.Path(sys.argv[1])
for rel in ["tests/test_survey_weekly_mechanical_refresh_v2.py","tests/test_versioned_renewal_history_phase_h.py","tests/test_versioned_renewal_source_phase_s.py","tests/test_versioned_renewal_reader_f4_20261025.py","tests/test_survey_editorial_retention_v2.py","tests/test_survey_editorial_staged_source_v2.py","scripts/survey_editorial_staged_source_v2.py","scripts/survey_versioned_renewal_history_v2.py","scripts/survey_versioned_renewal_source_v2.py","scripts/survey_versioned_renewal_v2.py","scripts/survey_reader_publication_v2.py","scripts/survey_editorial_correction_proposal_v2.py","scripts/survey_publication_v2.py","scripts/survey_editorial_publication_v2.py",".latexmkrc"]:
    data = (dst/rel).read_bytes()
    print(f"{rel} {len(data)} {hashlib.sha256(data).hexdigest()}")
PYEOF
[ "$(cat "$EVIDENCE/dst-pin-fixed-exit.txt")" = "0" ] || fail "dst-pin-fixed failed"

echo "FIXED READY DST=$DST"
