"""Populate DST worktree manifest-exact from SRC (all intended, not git ls-files-only).

Copies every intended file excluding .git/__pycache__/*.pyc via shutil.copy2,
verifies SHA/bytes post-copy and SRC==DST identical. Includes untracked
intended scripts/schemas plus .latexmkrc (tracked recipe, required tool input).
No network, no old runners, no cleanup, no candidate/reconstruct commit.
"""
import hashlib
import pathlib
import shutil
import sys

SRC = pathlib.Path(sys.argv[1])
DST = pathlib.Path(sys.argv[2])

def sha256(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

src_files = []
for p in SRC.rglob("*"):
    if p.is_dir():
        continue
    rel = p.relative_to(SRC)
    parts = rel.parts
    if parts[0] == ".git":
        continue
    if "__pycache__" in parts:
        continue
    if p.name.endswith(".pyc"):
        continue
    src_files.append(rel)

src_files.sort()
print(f"SRC_INTENDED_COUNT {len(src_files)}")
# Require 741 current full intended source (freeze 731 + 10 parallel additions).
if len(src_files) != 741:
    print(f"FAIL intended count {len(src_files)} != 741", file=sys.stderr)
    sys.exit(2)

for rel in src_files:
    s = SRC / rel
    d = DST / rel
    d.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(s, d)
    if sha256(s) != sha256(d):
        print(f"FAIL sha mismatch {rel}", file=sys.stderr)
        sys.exit(3)
    if s.stat().st_size != d.stat().st_size:
        print(f"FAIL size mismatch {rel}", file=sys.stderr)
        sys.exit(4)

# Verify .latexmkrc present and exact.
for name in [".latexmkrc", "tests/test_survey_weekly_mechanical_refresh_v2.py"]:
    s = SRC / name
    d = DST / name
    if not d.is_file():
        print(f"FAIL missing {name} in DST", file=sys.stderr)
        sys.exit(5)
    if sha256(s) != sha256(d):
        print(f"FAIL {name} drift SRC!=DST", file=sys.stderr)
        sys.exit(6)
    print(f"PIN {name} {sha256(d)} {d.stat().st_size}B")

print(f"DST_POPULATE_OK {len(src_files)}")
