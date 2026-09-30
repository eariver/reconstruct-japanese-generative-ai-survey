import subprocess, os, hashlib
DST = "/tmp/jgas-rephase-r1-assembly-20260929T143833Z"
EXP_HEAD = "481dec0c0233d7871df79a07a88aa5fe2291daa3"
EXP_TREE = "657032438c6ed8b1c055d5a120b67b4b261a5092"
EXP_PARENT = "e4c82692abee6acedbba07815b0d74ccefb80a7e"
def git(args):
    return subprocess.run(["git", "-C", DST] + args, capture_output=True, text=True)
print("PRECHECK fail-closed")
h = git(["rev-parse", "HEAD"]).stdout.strip()
t = git(["rev-parse", "HEAD^{tree}"]).stdout.strip()
p = git(["log", "--format=%P", "-1"]).stdout.strip()
print("HEAD", h, "match", h == EXP_HEAD)
print("TREE", t, "match", t == EXP_TREE)
print("PARENT", p, "match", p == EXP_PARENT)
st = git(["status", "--porcelain=v1", "-uall"]).stdout
print("STATUS_PORCELAIN:")
print(st)
# tracked clean means only ?? pycache lines, no M/A/D in index/worktree for tracked
lines = [l for l in st.strip().splitlines() if l.strip() != ""]
tracked_dirty = [l for l in lines if not l.startswith("??")]
print("TRACKED_DIRTY_COUNT", len(tracked_dirty), tracked_dirty)
# index cleanliness: diff --cached should be empty, diff unstaged empty
dc = git(["diff", "--cached", "--name-only"]).stdout.strip()
du = git(["diff", "--name-only"]).stdout.strip()
print("CACHED_DIFF_EMPTY", dc == "", repr(dc))
print("UNSTAGED_DIFF_EMPTY", du == "", repr(du))
# GIT overrides: check env for GIT_*
import os as _os
over = {k: v for k, v in _os.environ.items() if k.startswith("GIT_") or k in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE","GIT_OBJECT_DIRECTORY","GIT_ALTERNATE_OBJECT_DIRECTORIES","GIT_COMMON_DIR")}
print("GIT_OVERRIDES", over if over else "none")
print("PYTHONDONTWRITEBYTECODE", _os.environ.get("PYTHONDONTWRITEBYTECODE"))
# source paths/hashes for seven
seven = [
    "scripts/survey_agent_control_v2.py",
    "scripts/survey_reader_surface_gate_v2.py",
    "scripts/survey_weekly_derivation_v2.py",
    "scripts/survey_weekly_mechanical_refresh_v2.py",
    "tests/test_survey_weekly_mechanical_refresh_v2.py",
    "tests/test_survey_publication_revalidation_v2.py",
    "docs/weekly-mechanical-refresh.md",
]
for path in seven:
    fp = os.path.join(DST, path)
    with open(fp, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    print(path, sha)
print("PRECHECK_DONE")
