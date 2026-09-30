import subprocess, os, hashlib, json

DST = "/tmp/jgas-rephase-r1-assembly-20260929T143833Z"
R1 = "/tmp/jgas-rephase-mechanical-r1-20260928T000710Z"
E4 = "/tmp/jgas-rephase-gate-cli"
RECON = "/mnt/d/Git/reconstruct-japanese-generative-ai-survey"

def git(repo, args):
    r = subprocess.run(["git", "-C", repo] + args, capture_output=True, text=True)
    return r

with open(RECON + "/notes/rephase-1-mechanical-refresh/correction/final-b74db679f03908048db91420a8f262d412b8f58c/manifest-final.json") as f:
    mf = json.load(f)

print("=== 7-path worktree SHA256 vs manifest + hash-object vs b74 blob ===")
all_ok = True
for e in mf["seven_paths"]:
    path = e["path"]
    exp_sha = e["worktree_sha256"]
    exp_blob = e["blob"]
    exp_mode = e["mode"]
    fp = os.path.join(DST, path)
    exists = os.path.exists(fp)
    print(path, "exists=", exists)
    if not exists:
        all_ok = False
        continue
    with open(fp, "rb") as fh:
        sha = hashlib.sha256(fh.read()).hexdigest()
    print("  worktree sha256:", sha, "expected:", exp_sha, "match:", sha == exp_sha)
    # hash-object
    ho = git(DST, ["hash-object", "--", path])
    # hash-object needs cwd? use -C, path relative to repo root? git -C DST hash-object -- path works with absolute? Use relative
    # retry with cwd=DST
    ho2 = subprocess.run(["git", "hash-object", "--", path], capture_output=True, text=True, cwd=DST)
    hobj = ho2.stdout.strip()
    print("  hash-object:", hobj, "expected blob:", exp_blob, "match:", hobj == exp_blob)
    # b74 blob
    b = git(R1, ["ls-tree", "b74db679f03908048db91420a8f262d412b8f58c", "--", path]).stdout.strip()
    print("  b74 ls-tree:", b, "contains blob:", exp_blob in b)
    # mode
    mode = oct(os.lstat(fp).st_mode & 0o777)
    print("  worktree mode:", mode, "expected:", exp_mode)
    # compare to final-b74 changed-files copy
    copy_path = RECON + "/notes/rephase-1-mechanical-refresh/correction/final-b74db679f03908048db91420a8f262d412b8f58c/changed-files/" + path
    with open(copy_path, "rb") as fh:
        csha = hashlib.sha256(fh.read()).hexdigest()
    print("  changed-files copy sha:", csha, "match worktree:", csha == sha)
    if not (sha == exp_sha and hobj == exp_blob and exp_blob in b):
        all_ok = False
print("ALL_7_MATCH:", all_ok)

print("=== no extra changed/untracked authored paths ===")
st = git(DST, ["status", "--porcelain"]).stdout.strip().splitlines()
print("porcelain lines:")
for l in st:
    print("  ", repr(l))
# filter pycache
authored = [l for l in st if "__pycache__" not in l]
print("authored (excl pycache):", authored)
print("authored count must be 7 (4 M + 3 ??):", len(authored))
# diff name-only for tracked
dn = git(DST, ["diff", "--name-only"]).stdout.strip().splitlines()
print("diff tracked:", dn)
# untracked excl pycache
ut = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"], capture_output=True, text=True, cwd=DST).stdout.strip().splitlines()
print("untracked excl standard:", ut)
ut_authored = [x for x in ut if "__pycache__" not in x]
print("untracked authored:", ut_authored)

print("=== unrelated tree entries remain e4 ===")
# Compare DST index/tracked vs e4 for all except seven
# Use ls-tree e4 vs DST worktree? Best: compare git ls-files -s in DST (staged? unstaged doesn't affect index) vs e4 ls-tree?
# For modified files, index still e4 until add; for new files, not in index. So check: DST HEAD ls-tree should still be e4 (no commit yet)
h = git(DST, ["rev-parse", "HEAD"]).stdout.strip()
print("DST HEAD still e4:", h == "e4c82692abee6acedbba07815b0d74ccefb80a7e")
# Check that only seven differ in worktree vs HEAD: use git diff --name-only (tracked) + untracked
# For committed tree comparison after commit, will verify again post-commit. For now, verify that e4 tree entries for unrelated paths are untouched:
# Sample: check 10 unrelated paths mode/blob equal e4
sample = ["survey_agent_control_v2.py", "config/survey_validated_gate_v2.json", "scripts/survey_core_execution_bridge_v2.py", "tests/test_survey_reader_surface_gate_v2.py"]
# Actually use ls-tree e4 vs ls-tree HEAD (same) - trivial. Instead verify worktree files for unrelated sample match e4 blob content?
# Check a few unrelated worktree hashes equal e4 blobs
for p in ["scripts/survey_core_execution_bridge_v2.py", "scripts/survey_weekly_derivation_v2.py"]:
    pass
# Better: full diff check - ensure diff only touches 4 tracked + 3 untracked
print("tracked diff files:", dn)
print("expected tracked 4:", sorted(dn) == sorted(["scripts/survey_agent_control_v2.py", "scripts/survey_reader_surface_gate_v2.py", "scripts/survey_weekly_derivation_v2.py", "tests/test_survey_publication_revalidation_v2.py"]))
print("untracked authored expected 3:", sorted(ut_authored) == sorted(["docs/weekly-mechanical-refresh.md", "scripts/survey_weekly_mechanical_refresh_v2.py", "tests/test_survey_weekly_mechanical_refresh_v2.py"]))

print("=== promisor/missing objects limitation probe (no hydration) ===")
# Try ls-tree for a known missing promisor path? From clarification: sources/2026-W32/freeze-v0.2.md is missing in R1 but may be promisor in e4?
# In e4, check ls-tree for that path (should exist as promisor ref, but object missing). Do NOT cat-file/fetch.
r = git(DST, ["ls-tree", "HEAD", "--", "sources/2026-W32/freeze-v0.2.md"])
print("promisor ls-tree:", repr(r.stdout.strip()), "exit", r.returncode)
# Check that unrelated tree metadata still references promisor (mode/blob present) without hydrating
r2 = git(E4, ["ls-tree", "HEAD", "--", "sources/2026-W32/freeze-v0.2.md"])
print("e4 promisor ls-tree:", repr(r2.stdout.strip()))
print("promisor metadata preserved:", r.stdout.strip() == r2.stdout.strip())

print("DONE")
