#!/bin/bash
# Archive + verify + remove ONLY 6 known inactive early R3 scratch smoke copies.
# Storage worker: no code/test authoring, no git commit, no network, no source edits.
# Whitelist fixed; no glob delete; no git clean/reset; no packet raw deletion.
# Usage: bash <this-script>  (outputs go to caller-redirected stdout/stderr files)
set -u
PACKET="/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-editorial-operation-implementation"
ARCHDIR="$PACKET/preserved-scratch/archives"
TS="20261022T004100Z"

WL=(
"/tmp/opencode/jgas-editorial-smoke-20261021T120000Z"
"/tmp/opencode/jgas-editorial-smoke-20261021T121500Z"
"/tmp/opencode/jgas-editorial-smoke-20261021T123000Z"
"/tmp/opencode/jgas-editorial-smoke-20261021T130000Z"
"/tmp/opencode/jgas-editorial-smoke-20261021T133000Z"
"/tmp/opencode/jgas-editorial-smoke-20261021T134500Z"
)
# Expected SOURCE snapshot HEADs observed pre-archive (identity pin; stop path on mismatch)
declare -A EXPECT_HEAD=(
["/tmp/opencode/jgas-editorial-smoke-20261021T120000Z"]="d5a30a0f7b5988189f744b90294047c6d6be370d"
["/tmp/opencode/jgas-editorial-smoke-20261021T121500Z"]="ea54c1af2dc0019933164def85c224340dcc255b"
["/tmp/opencode/jgas-editorial-smoke-20261021T123000Z"]="99961578a54166e97e1722cbf2b0522f7001bbbe"
["/tmp/opencode/jgas-editorial-smoke-20261021T130000Z"]="e19de0859abe7c3f6f7164f9352777f73855c886"
["/tmp/opencode/jgas-editorial-smoke-20261021T133000Z"]="530592e3fceabdd45c4453d085737f3398be1612"
["/tmp/opencode/jgas-editorial-smoke-20261021T134500Z"]="3536af3d1cac80ceaf225c52b532ebd2af766e08"
)

echo "=== STORAGE-ARCHIVAL START $TS ==="
echo "PACKET=$PACKET"
echo "ARCHDIR=$ARCHDIR"

# 0. Workspace parent verify first; archive dir must exist, not symlink/hardlink
if [ ! -d "$PACKET" ]; then echo "FATAL: packet parent missing: $PACKET"; exit 10; fi
if [ -L "$ARCHDIR" ]; then echo "FATAL: archdir is symlink"; exit 11; fi
if [ ! -d "$ARCHDIR" ]; then echo "FATAL: archdir missing (must be pre-created with parent verify)"; exit 12; fi
echo "PARENT_OK packet exists; archdir exists not-symlink"

# 0b. Before disk/inode state
echo "--- BEFORE disk/bytes/inodes ---"
df -B1 /tmp; echo "DF_EXIT:$?"
df -i /tmp; echo "DFI_EXIT:$?"
du -sb "${WL[@]}"; echo "DU_EXIT:$?"
for p in "${WL[@]}"; do
  echo "--- whitelist entry: $p ---"
  if [ -L "$p" ]; then echo "STOP_PATH symlink root: $p"; exit 20; fi
  if [ ! -d "$p" ]; then echo "STOP_PATH missing/not-dir: $p"; exit 21; fi
  stat -c "owner:%U uid:%u mode:%a dev:%d ino:%i nlink:%h" "$p" || { echo "STOP_PATH stat failed: $p"; exit 22; }
  bn="$(basename "$p")"
  case "$bn" in
    jgas-editorial-smoke-20261021T120000Z|jgas-editorial-smoke-20261021T121500Z|jgas-editorial-smoke-20261021T123000Z|jgas-editorial-smoke-20261021T130000Z|jgas-editorial-smoke-20261021T133000Z|jgas-editorial-smoke-20261021T134500Z) echo "NAME_ALLOWLIST_OK $bn" ;;
    *) echo "STOP_PATH name not in fixed allowlist: $bn"; exit 23 ;;
  esac
  # Protected names must never match here (defense): 180000Z, 161500Z, diag, op-impl, source DST/R2/R2V/R3C, toolchain, workspace
  case "$p" in
    *180000Z*|*161500Z*|*diag*|*op-impl*|*toolchain*|*workspace*) echo "STOP_PATH protected pattern: $p"; exit 24 ;;
  esac
  # Owner must be eariver (uid 1000)
  ou="$(stat -c %U "$p")"
  if [ "$ou" != "eariver" ]; then echo "STOP_PATH owner mismatch ($ou): $p"; exit 25; fi
  # Git identity check (read-only)
  head="$(git -C "$p/candidate-partial-b40de60" rev-parse HEAD 2>&1)" || { echo "STOP_PATH git HEAD failed: $p $head"; exit 26; }
  echo "HEAD $head"
  exp="${EXPECT_HEAD[$p]}"
  if [ "$head" != "$exp" ]; then echo "STOP_PATH HEAD mismatch expected=$exp got=$head : $p"; exit 27; fi
  git -C "$p/candidate-partial-b40de60" log -1 --format="%H %ci %s" 2>&1 || { echo "STOP_PATH git log failed: $p"; exit 28; }
done

# 0c. No active process cwd/open work check (cwd + fd scan, never follow beyond readlink)
echo "--- activity check: cwd/fd scan for 6 paths ---"
python3 - <<'PY'
import os, sys
targets=[
"/tmp/opencode/jgas-editorial-smoke-20261021T120000Z",
"/tmp/opencode/jgas-editorial-smoke-20261021T121500Z",
"/tmp/opencode/jgas-editorial-smoke-20261021T123000Z",
"/tmp/opencode/jgas-editorial-smoke-20261021T130000Z",
"/tmp/opencode/jgas-editorial-smoke-20261021T133000Z",
"/tmp/opencode/jgas-editorial-smoke-20261021T134500Z",
]
hits=[]
for pid in os.listdir('/proc'):
    if not pid.isdigit(): continue
    try:
        cwd=os.readlink(f'/proc/{pid}/cwd')
    except Exception:
        cwd=None
    if cwd is not None:
        for t in targets:
            if cwd==t or cwd.startswith(t+'/'):
                try: cmd=open(f'/proc/{pid}/cmdline','rb').read().replace(b'\x00',b' ').decode(errors='replace')[:500]
                except Exception: cmd='?'
                hits.append(f'CWD-HIT pid={pid} cwd={cwd} cmd={cmd}')
    fd_dir=f'/proc/{pid}/fd'
    try: fds=os.listdir(fd_dir)
    except Exception: continue
    for fd in fds:
        try: link=os.readlink(os.path.join(fd_dir,fd))
        except Exception: continue
        for t in targets:
            if link==t or link.startswith(t+'/'):
                try: cmd=open(f'/proc/{pid}/cmdline','rb').read().replace(b'\x00',b' ').decode(errors='replace')[:500]
                except Exception: cmd='?'
                hits.append(f'FD-HIT pid={pid} fd={fd} link={link} cmd={cmd}')
                break
if hits:
    print("ACTIVE_HITS:")
    for h in hits: print(h)
    sys.exit(30)
else:
    print("ACTIVITY_OK no cwd/fd hits on 6 whitelist paths")
PY
pyrc=$?
echo "ACTIVITY_CHECK_EXIT:$pyrc"
if [ "$pyrc" -ne 0 ]; then echo "FATAL: active process holds whitelist path; stopping all"; exit 30; fi

# 0d. lsof probe (best-effort, non-fatal if missing, fatal if hits)
if command -v lsof >/dev/null 2>&1; then
  for p in "${WL[@]}"; do
    echo "--- lsof $p ---"
    lsof +D "$p" 2>&1 | head -n 20
    echo "LSOF_EXIT:$? for $p"
  done
else
  echo "lsof not available; /proc scan above is authoritative"
fi

# 1. Per-path inventory -> archive -> manifest -> verify -> unchanged check -> remove
OVERALL_RECLAIMED_BYTES=0
OVERALL_RECLAIMED_FILES=0
declare -a DONE_ARCHIVES=()
declare -a DONE_REMOVED=()

for SRC in "${WL[@]}"; do
  BN="$(basename "$SRC")"
  echo "===== PATH $SRC ($BN) ====="
  INV_JSON="$ARCHDIR/${BN}.inventory.json"
  ARCHIVE="$ARCHDIR/${BN}.tar.xz"
  MANIFEST="$ARCHDIR/${BN}.manifest.json"
  # Do not symlink/hardlink archive target; no raw truncation of existing different content
  if [ -L "$ARCHIVE" ]; then echo "STOP_PATH archive target is symlink: $ARCHIVE"; exit 40; fi
  if [ -e "$ARCHIVE" ]; then echo "STOP_PATH archive already exists, refusing overwrite: $ARCHIVE"; exit 41; fi
  if [ -L "$INV_JSON" ] || [ -L "$MANIFEST" ]; then echo "STOP_PATH manifest/inventory symlink"; exit 42; fi

  SRC_BYTES="$(du -sb "$SRC" | cut -f1)"
  echo "SRC_BYTES=$SRC_BYTES"

  # 1a. Full inventory: every dir/file/opaque symlink, lstat never follow, mode/size/SHA, prefix+traversal guard
  echo "--- inventory $SRC ---"
  python3 - "$SRC" "$INV_JSON" <<'PY'
import os, sys, json, hashlib
src=sys.argv[1]; out=sys.argv[2]
bn=os.path.basename(src.rstrip('/'))
entries=[]
for root, dirs, files in os.walk(src, topdown=True, followlinks=False):
    # record dirs (including root) + files; os.walk lists symlinked dirs in dirs (not followed)
    # To capture opaque symlinks correctly, lstat each name in dirs+files
    for name in dirs + files:
        full=os.path.join(root, name)
        try: st=os.lstat(full)
        except Exception as e:
            print(f"LSTAT_FAIL {full} {e}", file=sys.stderr); sys.exit(50)
        import stat as statm
        if statm.S_ISLNK(st.st_mode): typ="symlink"
        elif statm.S_ISDIR(st.st_mode): typ="dir"
        elif statm.S_ISREG(st.st_mode): typ="file"
        else: typ="other"
        rel=os.path.relpath(full, src)
        # prefix/traversal guard: rel must not be absolute, must not contain .., must stay inside
        if os.path.isabs(rel) or rel.startswith("..") or "/../" in rel or rel=="..":
            print(f"TRAVERSAL {full} rel={rel}", file=sys.stderr); sys.exit(51)
        mode=oct(statm.S_IMODE(st.st_mode))
        size=st.st_size
        sha=None; linktarget=None
        if typ=="file":
            h=hashlib.sha256()
            with open(full,'rb') as f:
                for chunk in iter(lambda: f.read(1048576), b''): h.update(chunk)
            sha=h.hexdigest()
        elif typ=="symlink":
            try: linktarget=os.readlink(full)
            except Exception as e: print(f"READLINK_FAIL {full} {e}", file=sys.stderr); sys.exit(52)
        entries.append({"rel":rel,"type":typ,"mode":mode,"size":size,"sha256":sha,"linktarget":linktarget})
    # also record root dir itself once
    if root==src:
        import stat as statm
        st=os.lstat(src)
        entries.append({"rel":".","type":"dir","mode":oct(statm.S_IMODE(st.st_mode)),"size":st.st_size,"sha256":None,"linktarget":None})
# deterministic order
entries.sort(key=lambda e: e["rel"])
# member path = bn + "/" + rel (root "." maps to bn)
for e in entries:
    e["member"]= bn if e["rel"]=="." else bn+"/"+e["rel"]
with open(out,'w') as f: json.dump({"source":src,"basename":bn,"count":len(entries),"entries":entries},f,indent=2,sort_keys=False)
print(f"INVENTORY_OK count={len(entries)} -> {out}")
PY
  pyr=$?; echo "INVENTORY_EXIT:$pyr for $BN"
  if [ "$pyr" -ne 0 ]; then echo "STOP_PATH inventory failed: $SRC"; exit 50; fi
  test -f "$INV_JSON" || { echo "STOP_PATH inventory file missing"; exit 53; }
  python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print('INV_COUNT',d['count'])" "$INV_JSON"

  # 1b. Create lossless streaming archive: tar -cJ, no follow (-h NOT used), numeric owner, preserve perms
  echo "--- archive $SRC -> $ARCHIVE ---"
  # Ensure parent of SRC is stable and SRC root is not symlink (re-check no-follow)
  if [ -L "$SRC" ]; then echo "STOP_PATH root became symlink before tar"; exit 60; fi
  tar -cJf "$ARCHIVE" --numeric-owner -p -C /tmp/opencode "$BN" 2>&1
  trc=$?; echo "TAR_EXIT:$trc for $BN"
  if [ "$trc" -ne 0 ]; then echo "STOP_PATH tar failed: $SRC"; rm -f "$ARCHIVE"; exit 61; fi
  test -f "$ARCHIVE" || { echo "STOP_PATH archive missing after tar"; exit 62; }
  if [ -L "$ARCHIVE" ]; then echo "STOP_PATH archive is symlink after tar"; exit 63; fi
  ARCH_SHA="$(sha256sum "$ARCHIVE" | cut -d' ' -f1)"
  ARCH_SIZE="$(stat -c %s "$ARCHIVE")"
  echo "ARCHIVE_SHA256=$ARCH_SHA SIZE=$ARCH_SIZE for $BN"
  if [ -z "$ARCH_SHA" ] || [ "$ARCH_SIZE" -eq 0 ]; then echo "STOP_PATH archive empty/hash fail"; exit 64; fi

  # 1c. Save manifest JSON: archive SHA + exact oldpath->archive/member map
  echo "--- manifest $MANIFEST ---"
  python3 - "$SRC" "$ARCHIVE" "$MANIFEST" "$INV_JSON" "$ARCH_SHA" <<'PY'
import os, sys, json
src, arch, manif, inv, asha = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
import stat as statm
d=json.load(open(inv))
bn=os.path.basename(src.rstrip('/'))
arch_size=os.lstat(arch).st_size
manifest={
 "old_path": src,
 "basename": bn,
 "archive_path": arch,
 "archive_sha256": asha,
 "archive_size": arch_size,
 "member_prefix": bn,
 "member_count": d["count"],
 "inventory_path": inv,
 "member_map": f"{src} -> {arch} :: members {bn}/...",
 "note": ".git preserved as archive binary; not imported as objects into reconstruct DB. Accessible via tar -tf / tarfile without unsafe filesystem extract. No restorer certification, no inode continuity claim."
}
with open(manif,'w') as f: json.dump(manifest,f,indent=2)
print(f"MANIFEST_OK {manif} members={d['count']} arch_size={arch_size}")
PY
  pyr=$?; echo "MANIFEST_EXIT:$pyr for $BN"
  if [ "$pyr" -ne 0 ]; then echo "STOP_PATH manifest failed"; exit 70; fi
  python3 -m json.tool "$MANIFEST" >/dev/null || { echo "STOP_PATH manifest invalid JSON"; exit 71; }

  # 1d. Verify archive file bytes/member metadata EXACT against source inventory (not only tar listing)
  echo "--- verify $ARCHIVE vs $INV_JSON ---"
  python3 - "$SRC" "$ARCHIVE" "$INV_JSON" <<'PY'
import os, sys, json, tarfile, hashlib
src, arch, inv = sys.argv[1], sys.argv[2], sys.argv[3]
d=json.load(open(inv))
inv_by={e["member"]: e for e in d["entries"]}
bn=os.path.basename(src.rstrip('/'))
tf=tarfile.open(arch, mode='r:xz')
members=tf.getmembers()
# guards: no absolute, no traversal, all inside prefix
for m in members:
    n=m.name
    if n.startswith('/') : print(f"FAIL absolute member {n}"); sys.exit(80)
    parts=n.split('/')
    if ".." in parts: print(f"FAIL traversal member {n}"); sys.exit(81)
    if not (n==bn or n.startswith(bn+'/')): print(f"FAIL outside prefix {n}"); sys.exit(82)
# root "." member maps to bn
# Compare sets
tar_names=set(m.name for m in members)
inv_names=set(inv_by.keys())
if tar_names!=inv_names:
    print(f"FAIL member set mismatch tar={len(tar_names)} inv={len(inv_names)}")
    print("ONLY_TAR", sorted(tar_names-inv_names)[:20])
    print("ONLY_INV", sorted(inv_names-tar_names)[:20])
    sys.exit(83)
# Per-member metadata + bytes
import stat as statm
for m in members:
    e=inv_by[m.name]
    # type
    if m.issym(): t="symlink"
    elif m.isdir(): t="dir"
    elif m.isreg(): t="file"
    else: t="other"
    if t!=e["type"]:
        # tar may report dirs with trailing slash; already handled via isdir
        print(f"FAIL type {m.name} tar={t} inv={e['type']}"); sys.exit(84)
    # mode (lower 12 bits incl suid/sgid/sticky? compare permission bits 0o7777)
    tar_mode=oct(m.mode & 0o7777); inv_mode=e["mode"]
    # normalize: inv mode from S_IMODE includes suid/sgid/sticky already (0o7777)
    if tar_mode!=inv_mode:
        print(f"FAIL mode {m.name} tar={tar_mode} inv={inv_mode}"); sys.exit(85)
    if t=="file":
        if m.size!=e["size"]: print(f"FAIL size {m.name} tar={m.size} inv={e['size']}"); sys.exit(86)
        f=tf.extractfile(m)
        if f is None: print(f"FAIL extractfile None {m.name}"); sys.exit(87)
        h=hashlib.sha256()
        for chunk in iter(lambda: f.read(1048576), b''): h.update(chunk)
        if h.hexdigest()!=e["sha256"]: print(f"FAIL sha {m.name}"); sys.exit(88)
    elif t=="symlink":
        if m.linkname!=e["linktarget"]: print(f"FAIL linktarget {m.name} tar={m.linkname!r} inv={e['linktarget']!r}"); sys.exit(89)
    elif t=="dir":
        pass
    else:
        print(f"FAIL other type unsupported {m.name}"); sys.exit(90)
print(f"VERIFY_OK members={len(members)} bytes+metadata exact")
PY
  pyr=$?; echo "VERIFY_EXIT:$pyr for $BN"
  if [ "$pyr" -ne 0 ]; then echo "STOP_PATH verification failed, preserving source: $SRC"; exit 80; fi

  # 1e. Final live inventory unchanged vs before (re-walk, compare count+hashes; no mtime assumption)
  echo "--- final live unchanged check $SRC ---"
  python3 - "$SRC" "$INV_JSON" <<'PY'
import json, sys, os, hashlib
src, inv = sys.argv[1], sys.argv[2]
d=json.load(open(inv))
old={e["member"]:(e["type"],e["mode"],e["size"],e["sha256"],e["linktarget"]) for e in d["entries"]}
# re-walk
import stat as statm
new={}
bn=os.path.basename(src.rstrip('/'))
for root, dirs, files in os.walk(src, topdown=True, followlinks=False):
    for name in dirs+files:
        full=os.path.join(root,name)
        st=os.lstat(full)
        if statm.S_ISLNK(st.st_mode): typ="symlink"
        elif statm.S_ISDIR(st.st_mode): typ="dir"
        elif statm.S_ISREG(st.st_mode): typ="file"
        else: typ="other"
        rel=os.path.relpath(full,src)
        member=bn if rel=="." else bn+"/"+rel
        mode=oct(statm.S_IMODE(st.st_mode)); size=st.st_size; sha=None; lt=None
        if typ=="file":
            h=hashlib.sha256()
            with open(full,'rb') as f:
                for chunk in iter(lambda: f.read(1048576), b''): h.update(chunk)
            sha=h.hexdigest()
        elif typ=="symlink":
            lt=os.readlink(full)
        new[member]=(typ,mode,size,sha,lt)
# root
st=os.lstat(src); new[bn if "." not in new else bn]=(new.get(bn, (None,None,None,None,None))[0] or "dir", oct(statm.S_IMODE(st.st_mode)), st.st_size, None, None) if bn not in new else new[bn]
# Actually ensure root entry exists:
if bn not in new:
    new[bn]=("dir",oct(statm.S_IMODE(st.st_mode)),st.st_size,None,None)
# Compare: old includes root "." mapped to bn; new includes bn
# old keys are members (bn + ...); new keys same
if set(old.keys())!=set(new.keys()):
    print(f"FAIL live set changed old={len(old)} new={len(new)}"); print(sorted(set(old.keys())-set(new.keys()))[:10]); print(sorted(set(new.keys())-set(old.keys()))[:10]); sys.exit(91)
for k in old:
    if old[k]!=new[k]:
        print(f"FAIL live entry changed {k} old={old[k]} new={new[k]}"); sys.exit(92)
print(f"LIVE_UNCHANGED_OK members={len(new)}")
PY
  pyr=$?; echo "LIVECHECK_EXIT:$pyr for $BN"
  if [ "$pyr" -ne 0 ]; then echo "STOP_PATH live tree changed after archive; preserving source: $SRC"; exit 91; fi

  # 1f. Only now remove EXPLICIT known owned inactive copy tree; fixed whitelist, no-follow root checks
  echo "--- remove $SRC (post-verify only) ---"
  if [ -L "$SRC" ]; then echo "STOP_PATH root symlink at remove time"; exit 100; fi
  # Re-confirm exact whitelist membership (no glob)
  case "$SRC" in
    "/tmp/opencode/jgas-editorial-smoke-20261021T120000Z"|"/tmp/opencode/jgas-editorial-smoke-20261021T121500Z"|"/tmp/opencode/jgas-editorial-smoke-20261021T123000Z"|"/tmp/opencode/jgas-editorial-smoke-20261021T130000Z"|"/tmp/opencode/jgas-editorial-smoke-20261021T133000Z"|"/tmp/opencode/jgas-editorial-smoke-20261021T134500Z") echo "REMOVE_ALLOWLIST_OK $SRC" ;;
    *) echo "STOP_PATH remove not in fixed whitelist"; exit 101 ;;
  esac
  # No-follow: ensure no symlink components at top (root already checked); use rm -rf -- on exact path
  rm -rf -- "$SRC" 2>&1
  rrc=$?; echo "RM_EXIT:$rrc for $SRC"
  if [ "$rrc" -ne 0 ]; then echo "STOP_PATH rm failed (preserving; manual check needed): $SRC"; exit 102; fi
  if [ -e "$SRC" ] || [ -L "$SRC" ]; then echo "STOP_PATH still exists after rm: $SRC"; exit 103; fi
  echo "REMOVED_OK $SRC bytes=$SRC_BYTES"
  OVERALL_RECLAIMED_BYTES=$((OVERALL_RECLAIMED_BYTES + SRC_BYTES))
  DONE_ARCHIVES+=("$ARCHIVE")
  DONE_REMOVED+=("$SRC")

done

echo "--- AFTER disk/bytes/inodes ---"
df -B1 /tmp; echo "DF_AFTER_EXIT:$?"
df -i /tmp; echo "DFI_AFTER_EXIT:$?"
echo "RECLAIMED_PATHS=${#DONE_REMOVED[@]} RECLAIMED_BYTES=$OVERALL_RECLAIMED_BYTES"
for a in "${DONE_ARCHIVES[@]}"; do sha256sum "$a"; stat -c "%s %n" "$a"; done
echo "REMOVED_LIST:"
printf "%s\n" "${DONE_REMOVED[@]}"
echo "ARCHIVE_LIST:"
printf "%s\n" "${DONE_ARCHIVES[@]}"
echo "=== STORAGE-ARCHIVAL DONE ==="
