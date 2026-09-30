import subprocess, os, hashlib
SRC = "/tmp/jgas-rephase-gate-cli"
DST = "/tmp/jgas-rephase-r1-assembly-20260929T143833Z"
RAW = "/tmp/jgas-r1-verify-20260929T145048Z/raw"
for fn in ["new-observation.stdout", "new-observation.stderr", "new-observation.exit"]:
    fp = os.path.join(RAW, fn)
    assert not os.path.exists(fp), "refuse overwrite " + fp
def git(repo, args):
    return subprocess.run(["git", "-C", repo] + args, capture_output=True, text=True)
print("NEW_OBSERVATION read-only post-commit (labels current scope, not historic recreation)", flush=True)
print("DST_HEAD " + git(DST, ["rev-parse", "HEAD"]).stdout.strip(), flush=True)
print("DST_TREE " + git(DST, ["rev-parse", "HEAD^{tree}"]).stdout.strip(), flush=True)
print("DST_PARENT " + git(DST, ["log", "--format=%P", "-1"]).stdout.strip(), flush=True)
print("DST_BRANCH " + git(DST, ["branch", "--show-current"]).stdout.strip(), flush=True)
refs = git(DST, ["for-each-ref"]).stdout.strip().splitlines()
print("DST_REFS_N=" + str(len(refs)), flush=True)
for l in refs:
    print("DST_REF: " + l, flush=True)
# object counts
def list_files(root):
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        for n in filenames:
            out.append(os.path.relpath(os.path.join(dirpath, n), root))
    out.sort()
    return out
src_objs = list_files(SRC + "/.git/objects")
dst_objs = list_files(DST + "/.git/objects")
print("SRC_OBJECTS_N=" + str(len(src_objs)), flush=True)
print("DST_OBJECTS_N=" + str(len(dst_objs)), flush=True)
print("DST_LARGER_EXPECTED=" + str(len(dst_objs) > len(src_objs)), flush=True)
# all old source object paths still present in DST, bytes identical, inodes different
missing = [r for r in src_objs if r not in set(dst_objs)]
print("OLD_PATHS_MISSING_IN_DST=" + str(len(missing)), flush=True)
assert len(missing) == 0, "old paths missing " + repr(missing[:10])
same_inode = []
hash_mismatch = []
for rel in src_objs:
    sp = os.path.join(SRC + "/.git/objects", rel)
    dp = os.path.join(DST + "/.git/objects", rel)
    if os.lstat(sp).st_ino == os.lstat(dp).st_ino:
        same_inode.append(rel)
    with open(sp, "rb") as f:
        sh = hashlib.sha256(f.read()).hexdigest()
    with open(dp, "rb") as f:
        dh = hashlib.sha256(f.read()).hexdigest()
    if sh != dh:
        hash_mismatch.append(rel)
print("OLD_PATHS_SAME_INODE=" + str(len(same_inode)), flush=True)
print("OLD_PATHS_HASH_MISMATCH=" + str(len(hash_mismatch)), flush=True)
assert len(same_inode) == 0
assert len(hash_mismatch) == 0
print("OLD_PATHS_PHYSICALLY_INDEPENDENT=True", flush=True)
# current tree refs: seven in new HEAD match b74, unrelated match e4 (spot: count)
print("NEW_OBSERVATION_DONE", flush=True)
