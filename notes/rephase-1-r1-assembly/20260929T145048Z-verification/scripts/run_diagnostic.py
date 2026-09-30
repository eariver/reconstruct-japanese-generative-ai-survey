import subprocess, os, sys, hashlib
from pathlib import Path
DST = "/tmp/jgas-rephase-r1-assembly-20260929T143833Z"
RAW = "/tmp/jgas-r1-verify-20260929T145048Z/raw"
EXP_HEAD = "481dec0c0233d7871df79a07a88aa5fe2291daa3"
EXP_TREE = "657032438c6ed8b1c055d5a120b67b4b261a5092"
EXP_PARENT = "e4c82692abee6acedbba07815b0d74ccefb80a7e"
E4 = "e4c82692abee6acedbba07815b0d74ccefb80a7e"
def git(args):
    return subprocess.run(["git", "-C", DST] + args, capture_output=True, text=True)
# no-overwrite guard
for fn in ["diagnostic.stdout", "diagnostic.stderr", "diagnostic.exit", "diagnostic.before.txt", "diagnostic.after.txt"]:
    fp = os.path.join(RAW, fn)
    assert not os.path.exists(fp), "refuse overwrite " + fp
# fail-closed precheck
def precheck(label):
    h = git(["rev-parse", "HEAD"]).stdout.strip()
    t = git(["rev-parse", "HEAD^{tree}"]).stdout.strip()
    p = git(["log", "--format=%P", "-1"]).stdout.strip()
    st = git(["status", "--porcelain=v1", "-uall"]).stdout
    tracked = [l for l in st.strip().splitlines() if l.strip() != "" and not l.startswith("??")]
    assert h == EXP_HEAD, label + " HEAD " + h
    assert t == EXP_TREE, label + " TREE " + t
    assert p == EXP_PARENT, label + " PARENT " + p
    assert len(tracked) == 0, label + " tracked dirty " + repr(tracked)
    assert git(["diff", "--cached", "--name-only"]).stdout.strip() == ""
    assert git(["diff", "--name-only"]).stdout.strip() == ""
    over = {k: v for k, v in os.environ.items() if k.startswith("GIT_")}
    assert not over, label + " GIT overrides " + repr(over)
    assert os.environ.get("PYTHONDONTWRITEBYTECODE") == "1"
    return h, t, p, st
before_head, before_tree, before_parent, before_status = precheck("BEFORE")
print("DIAG_PRECHECK_PASS", flush=True)
print("HEAD " + before_head, flush=True)
print("TREE " + before_tree, flush=True)
print("PARENT " + before_parent, flush=True)
# source module path/hash (exact assembly source)
sys.path.insert(0, DST)
from scripts import survey_weekly_derivation_v2 as weekly
from scripts import survey_production_v2 as core
mod_path = Path(weekly.__file__)
print("MODULE_PATH " + str(mod_path), flush=True)
with open(mod_path, "rb") as f:
    mod_sha = hashlib.sha256(f.read()).hexdigest()
print("MODULE_SHA256 " + mod_sha, flush=True)
# also record seven hashes
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
        print("SEVEN " + path + " " + hashlib.sha256(f.read()).hexdigest(), flush=True)
root = Path(DST)
# ancestry: e4 parent of HEAD, e4 ancestor
anc = subprocess.run(["git", "-C", DST, "merge-base", "--is-ancestor", E4, before_head], capture_output=True, text=True)
print("E4_IS_ANCESTOR_OF_HEAD exit=" + str(anc.returncode), flush=True)
assert anc.returncode == 0, "e4 must be ancestor of assembly HEAD"
log2 = git(["log", "--format=%H %P", "-2"]).stdout.strip()
print("LOG2:\n" + log2, flush=True)
# 2. current closure passes at actual HEAD
cur = weekly.current_closure(root)
print("CURRENT_CLOSURE_N=" + str(len(cur)), flush=True)
for row in cur:
    print("CUR_ROW " + row["name"] + " " + row["sha256"], flush=True)
weekly._verify_head_bytes(root, before_head, cur)
print("CURRENT_VERIFY_PASS at HEAD " + before_head, flush=True)
# 3. historical eight-file closure at exact e4 from local blobs (not relabelled)
e4_closure = []
missing = []
for p in weekly.CURRENT_CLOSURE:
    name = p.as_posix()
    r = subprocess.run(["git", "-C", DST, "show", E4 + ":" + name], capture_output=True)
    if r.returncode != 0:
        missing.append(name)
        print("E4_SHOW_FAIL " + name + " exit=" + str(r.returncode) + " stderr=" + r.stderr[:500].decode(errors="replace") if isinstance(r.stderr, bytes) else str(r.stderr)[:500], flush=True)
    else:
        sha = hashlib.sha256(r.stdout).hexdigest()
        e4_closure.append({"name": name, "path": name, "sha256": sha})
        print("E4_ROW " + name + " " + sha, flush=True)
assert len(missing) == 0, "missing e4 blobs, stop without stale rejection: " + repr(missing)
assert len(e4_closure) == 8, "e4 closure must be 8"
weekly.verify_closure_at_commit(root, e4_closure, E4)
print("HISTORICAL_VERIFY_PASS at E4 " + E4, flush=True)
# 4. ordinary replay with e4 basis must reject with intended message (not missing/setup)
INTENDED = "Weekly receipt implementation or contract changed since renderer commit"
try:
    weekly._verify_head_bytes(root, E4, e4_closure)
    print("UNEXPECTED_PASS stale basis should have rejected", flush=True)
    raise SystemExit("stale basis unexpectedly passed")
except ValueError as exc:
    msg = str(exc)
    print("STALE_REJECT_TYPE ValueError", flush=True)
    print("STALE_REJECT_MSG " + msg, flush=True)
    assert msg == INTENDED, "wrong rejection message: " + repr(msg)
    print("STALE_REJECT_INTENDED_PASS", flush=True)
# success sentinel outside handler
print("DIAG_SENTINEL_OK", flush=True)
# 5. no-write after evidence
after_head, after_tree, after_parent, after_status = precheck("AFTER")
print("NO_WRITE_HEAD_SAME " + str(after_head == before_head), flush=True)
print("NO_WRITE_TREE_SAME " + str(after_tree == before_tree), flush=True)
print("DIAGNOSTIC_DONE", flush=True)
