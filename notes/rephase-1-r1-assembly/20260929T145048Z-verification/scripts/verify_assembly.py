import os, hashlib, subprocess, sys

SRC = "/tmp/jgas-rephase-gate-cli"
DST = "/tmp/jgas-rephase-r1-assembly-20260929T143833Z"

def run(args, cwd=None):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    return r

print("=== HEAD/tree/branch ===")
for label, repo in [("SRC", SRC), ("DST", DST)]:
    h = run(["git", "-C", repo, "rev-parse", "HEAD"]).stdout.strip()
    t = run(["git", "-C", repo, "rev-parse", "HEAD^{tree}"]).stdout.strip()
    b = run(["git", "-C", repo, "branch", "--show-current"]).stdout.strip()
    gd = run(["git", "-C", repo, "rev-parse", "--git-dir"]).stdout.strip()
    cd = run(["git", "-C", repo, "rev-parse", "--git-common-dir"]).stdout.strip()
    agd = run(["git", "-C", repo, "rev-parse", "--absolute-git-dir"]).stdout.strip()
    print(f"{label} HEAD={h} tree={t} branch={b} gitdir={gd} commondir={cd} abs={agd}")

print("=== refs ===")
src_refs = run(["git", "-C", SRC, "for-each-ref"]).stdout.strip().splitlines()
dst_refs = run(["git", "-C", DST, "for-each-ref"]).stdout.strip().splitlines()
print(f"SRC refs lines: {len(src_refs)}")
for l in src_refs:
    print("SRC_REF:", l)
print(f"DST refs lines: {len(dst_refs)}")
for l in dst_refs:
    print("DST_REF:", l)
print("REFS_IDENTICAL:", src_refs == dst_refs)

print("=== .git symlink checks ===")
for p in [SRC + "/.git", DST + "/.git", DST + "/.git/objects", DST + "/.git/refs"]:
    st = os.lstat(p)
    import stat
    is_link = os.path.islink(p)
    print(f"{p} islink={is_link} mode={oct(st.st_mode)}")

# check for any symlinks under .git
def find_symlinks(root):
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        for n in dirnames + filenames:
            fp = os.path.join(dirpath, n)
            if os.path.islink(fp):
                out.append(fp)
    return out

print("SRC .git symlinks:", find_symlinks(SRC + "/.git")[:20])
print("DST .git symlinks:", find_symlinks(DST + "/.git")[:20])

print("=== alternates / commondir ===")
for f in ["/objects/info/alternates", "/commondir"]:
    for repo in [SRC, DST]:
        fp = repo + "/.git" + f
        print(fp, "exists=", os.path.exists(fp))

print("=== object files exhaustive ===")
def list_files(root):
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        for n in filenames:
            fp = os.path.join(dirpath, n)
            rel = os.path.relpath(fp, root)
            out.append(rel)
    out.sort()
    return out

src_objs = list_files(SRC + "/.git/objects")
dst_objs = list_files(DST + "/.git/objects")
print(f"SRC objects count={len(src_objs)} DST objects count={len(dst_objs)}")
print("OBJECT_LIST_IDENTICAL:", src_objs == dst_objs)
if src_objs != dst_objs:
    sset = set(src_objs)
    dset = set(dst_objs)
    print("ONLY_IN_SRC:", sorted(sset - dset)[:20])
    print("ONLY_IN_DST:", sorted(dset - sset)[:20])

# inode + nlink + hash check for ALL files
mismatch_inode_same = []
hardlink_non1 = []
hash_mismatch = []
size_mismatch = []
for rel in src_objs:
    sp = os.path.join(SRC + "/.git/objects", rel)
    dp = os.path.join(DST + "/.git/objects", rel)
    if not os.path.exists(dp):
        continue
    sst = os.lstat(sp)
    dst = os.lstat(dp)
    if sst.st_ino == dst.st_ino:
        mismatch_inode_same.append(rel)
    # check hardlinks: nlink should be 1 (no hardlink sharing); also check device+inode not shared
    if sst.st_nlink != 1 or dst.st_nlink != 1:
        hardlink_non1.append((rel, sst.st_nlink, dst.st_nlink))
    if sst.st_size != dst.st_size:
        size_mismatch.append(rel)
    # byte hash
    with open(sp, "rb") as f:
        sh = hashlib.sha256(f.read()).hexdigest()
    with open(dp, "rb") as f:
        dh = hashlib.sha256(f.read()).hexdigest()
    if sh != dh:
        hash_mismatch.append(rel)

print(f"INODE_SAME_COUNT (must be 0): {len(mismatch_inode_same)}")
if mismatch_inode_same:
    print(mismatch_inode_same[:20])
print(f"NLINK_NOT_1_COUNT: {len(hardlink_non1)}")
if hardlink_non1:
    print(hardlink_non1[:20])
print(f"SIZE_MISMATCH: {len(size_mismatch)} {size_mismatch[:10]}")
print(f"HASH_MISMATCH (must be 0): {len(hash_mismatch)}")
if hash_mismatch:
    print(hash_mismatch[:20])
print("ALL_INODES_DIFFERENT:", len(mismatch_inode_same) == 0)
print("NO_HARDLINKS (all nlink==1):", len(hardlink_non1) == 0)
print("ALL_BYTES_IDENTICAL:", len(hash_mismatch) == 0 and len(size_mismatch) == 0)

print("=== config/shallow/sparse byte compare ===")
import hashlib as hl
for rel in ["/.git/config", "/.git/shallow", "/.git/info/sparse-checkout", "/.git/HEAD"]:
    sp = SRC + rel
    dp = DST + rel
    if os.path.exists(sp) and os.path.exists(dp):
        with open(sp, "rb") as f:
            sh = hl.sha256(f.read()).hexdigest()
        with open(dp, "rb") as f:
            dh = hl.sha256(f.read()).hexdigest()
        print(rel, "identical=", sh == dh, sh[:12], dh[:12])
    else:
        print(rel, "missing src=", not os.path.exists(sp), "dst=", not os.path.exists(dp))

print("=== file modes for seven paths (source worktree) ===")
seven = [
    "scripts/survey_agent_control_v2.py",
    "scripts/survey_reader_surface_gate_v2.py",
    "scripts/survey_weekly_derivation_v2.py",
    "tests/test_survey_publication_revalidation_v2.py",
    "scripts/survey_weekly_mechanical_refresh_v2.py",
    "tests/test_survey_weekly_mechanical_refresh_v2.py",
    "docs/weekly-mechanical-refresh.md",
]
for p in seven:
    sp = os.path.join(SRC, p)
    dp = os.path.join(DST, p)
    se = os.path.exists(sp)
    de = os.path.exists(dp)
    print(p, "src_exists=", se, "dst_exists=", de)
    if se:
        print("  src_mode=", oct(os.lstat(sp).st_mode & 0o777))
    if de:
        print("  dst_mode=", oct(os.lstat(dp).st_mode & 0o777))

print("DONE")
