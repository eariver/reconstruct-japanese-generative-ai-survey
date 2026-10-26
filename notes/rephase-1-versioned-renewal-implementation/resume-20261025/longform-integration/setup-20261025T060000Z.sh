#!/usr/bin/env bash
set -u
# LONGFORM-only fixture setup — NEW guarded runner (not old packet executables)
# Freeze: versioned-renewal-final-input-20261025T051343Z/snapshot-work (736, actual409+86)
# Baseline: versioned-renewal-bootstrap-20261023T194449Z/bootstrap-longform (721a04d + old E)
# Owned: .rephase-1-editorial-runtime/versioned-renewal-longform-20261025T060000Z/renewal-longform
# Evidence: notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-integration/setup-20261025T060000Z/
EVID="notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-integration/setup-20261025T060000Z"
PARENT=".rephase-1-editorial-runtime/versioned-renewal-longform-20261025T060000Z"
FIXTURE=".rephase-1-editorial-runtime/versioned-renewal-longform-20261025T060000Z/renewal-longform"
SNAP=".rephase-1-editorial-runtime/versioned-renewal-final-input-20261025T051343Z/snapshot-work"
BOOT=".rephase-1-editorial-runtime/versioned-renewal-bootstrap-20261023T194449Z/bootstrap-longform"
run_tag() {
  tag="$1"; shift
  out_std="$EVID/${tag}-stdout.txt"
  out_err="$EVID/${tag}-stderr.txt"
  out_exit="$EVID/${tag}-exit.txt"
  tmp_out=$(mktemp)
  tmp_err=$(mktemp)
  # shellcheck disable=SC2068
  "$@" >"$tmp_out" 2>"$tmp_err"
  rc=$?
  cat "$tmp_out" >"$out_std"
  cat "$tmp_err" >"$out_err"
  echo "$rc" >"$out_exit"
  echo "\$ $*  # cwd=$(pwd) -> exit=$rc" >>"$EVID/commands.log"
  rm -f "$tmp_out" "$tmp_err"
  return $rc
}
echo "LONGFORM setup start $(date -u +%Y%m%dT%H%M%SZ) PID=$$" | tee "$EVID/commands.log"
# 0. guards: no inherited GIT env
if [ -n "${GIT_DIR:-}" ] || [ -n "${GIT_WORK_TREE:-}" ] || [ -n "${GIT_INDEX_FILE:-}" ]; then echo "FATAL inherited GIT env" >&2; exit 1; fi
run_tag env-check env
run_tag recon-head git rev-parse HEAD
run_tag recon-status git status --porcelain=v1 --untracked-files=all
# 1. verify frozen input
run_tag snap-head git -C "$SNAP" rev-parse HEAD
run_tag snap-tree git -C "$SNAP" rev-parse "HEAD^{tree}"
run_tag snap-count bash -c "find \"$SNAP\" -path \"$SNAP/.git\" -prune -o -type f -print | wc -l"
run_tag snap-git-count bash -c "find \"$SNAP/.git\" -type f | wc -l"
run_tag snap-remote git -C "$SNAP" remote -v
run_tag snap-shallow cat "$SNAP/.git/shallow"
# 2. verify bootstrap longform
run_tag boot-head git -C "$BOOT" rev-parse HEAD
run_tag boot-tree git -C "$BOOT" rev-parse "HEAD^{tree}"
run_tag boot-status git -C "$BOOT" status --porcelain=v1 --untracked-files=all
run_tag boot-others git -C "$BOOT" ls-files --others --exclude-standard
run_tag boot-ignored git -C "$BOOT" ls-files --others --ignored --exclude-standard
run_tag boot-log git -C "$BOOT" log --oneline -3
# 3. create parent (fail if exists to avoid overwrite / parallel collision)
if [ -e "$PARENT" ]; then echo "FATAL parent exists $PARENT (parallel collision)" >&2; exit 1; fi
run_tag mkdir-parent mkdir -p "$PARENT"
run_tag mkdir-evid mkdir -p "$EVID"
# workspace-local TMPDIR
mkdir -p "$PARENT/tmp"
export TMPDIR="$PARENT/tmp"
ADDLIST="$PARENT/tmp/longform-addlist-060000Z.txt"
echo "TMPDIR=$TMPDIR" >>"$EVID/commands.log"
# 4. byte-independent clone (no hardlinks), retain 721 ancestry
run_tag clone-0 git clone --no-hardlinks "$BOOT" "$FIXTURE"
run_tag remote-set git -C "$FIXTURE" remote set-url origin https://example.invalid/versioned-renewal-chain-longform.git
run_tag remote-show git -C "$FIXTURE" remote -v
run_tag cfg-user-name git -C "$FIXTURE" config user.name rephase-fixture-longform
run_tag cfg-user-email git -C "$FIXTURE" config user.email fixture-longform@example.invalid
run_tag cfg-gpgsign git -C "$FIXTURE" config commit.gpgsign false
run_tag fixture-head git -C "$FIXTURE" rev-parse HEAD
run_tag fixture-tree git -C "$FIXTURE" rev-parse "HEAD^{tree}"
run_tag fixture-gitdir git -C "$FIXTURE" rev-parse --absolute-git-dir
run_tag noalternates bash -c "test ! -e \"$FIXTURE/.git/objects/info/alternates\" && echo NO_ALTERNATES || (echo HAS_ALTERNATES; exit 1)"
run_tag config-show git -C "$FIXTURE" config --list --show-origin
# 5. copy captured E (untracked + ignored logs) exact names/hashes, not blind source cache
# Uses explicit git ls-files lists from BOOT, per-file copy2 + SHA verify
run_tag copy-E python3 - "$BOOT" "$FIXTURE" <<'PY'
import sys, hashlib, shutil, subprocess, pathlib
boot=pathlib.Path(sys.argv[1]); dst=pathlib.Path(sys.argv[2])
def ls(args):
    r=subprocess.run(["git","-C",str(boot)]+args, capture_output=True, text=True)
    assert r.returncode==0, r.stderr
    return [l for l in r.stdout.splitlines() if l.strip()]
others=ls(["ls-files","--others","--exclude-standard"])
ignored=ls(["ls-files","--others","--ignored","--exclude-standard"])
all_e=others+ignored
print(f"E files: others={len(others)} ignored={len(ignored)} total={len(all_e)}")
for rel in all_e:
    s=boot/rel; d=dst/rel
    assert s.exists(), f"missing SRC E {rel}"
    if d.exists():
        raise SystemExit(f"E target exists {rel}")
    if s.is_dir() and not s.is_symlink():
        shutil.copytree(str(s), str(d), symlinks=True, copy_function=shutil.copy2)
    else:
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(s), str(d))
    # verify SHA for files
    if s.is_file() and not s.is_symlink():
        hs=hashlib.sha256(s.read_bytes()).hexdigest()
        hd=hashlib.sha256(d.read_bytes()).hexdigest()
        assert hs==hd, f"SHA mismatch {rel} {hs} vs {hd}"
        print(f"OK {hs[:12]} {rel}")
print(f"COPY_E_DONE total={len(all_e)}")
PY
# 6. overlay EXACT 736 intended files from snapshot-work (manifest list), verify SHA
run_tag overlay-736 python3 - "$SNAP" "$FIXTURE" <<'PY'
import hashlib, shutil, pathlib, sys
snap=pathlib.Path(sys.argv[1]); dst=pathlib.Path(sys.argv[2])
manifest=pathlib.Path("notes/rephase-1-versioned-renewal-implementation/resume-20261025/final-integration-input-evidence-20261025T051343Z/dst-hash-intended-stdout.txt")
lines=[l.strip() for l in manifest.read_text().splitlines() if l.strip()]
assert len(lines)==736, f"manifest lines {len(lines)} != 736"
mism=[]
for line in lines:
    parts=line.split()
    assert len(parts)==3, line
    exp_sha, exp_bytes, rel=parts
    s=snap/rel; d=dst/rel
    assert s.is_file(), f"missing SNAP {rel}"
    d.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(s), str(d))
    got=hashlib.sha256(d.read_bytes()).hexdigest()
    if got!=exp_sha:
        mism.append((rel, exp_sha, got))
    # bytes check
    if int(exp_bytes)!=d.stat().st_size:
        mism.append((rel+":bytes", exp_bytes, str(d.stat().st_size)))
print(f"OVERLAY_DONE copied={len(lines)} mismatches={mism[:5]}")
assert not mism, f"overlay mismatches {mism[:3]}"
PY
run_tag overlay-verify python3 - "$SNAP" "$FIXTURE" <<'PY'
import hashlib, pathlib, sys
snap=pathlib.Path(sys.argv[1]); dst=pathlib.Path(sys.argv[2])
manifest=pathlib.Path("notes/rephase-1-versioned-renewal-implementation/resume-20261025/final-integration-input-evidence-20261025T051343Z/dst-hash-intended-stdout.txt")
bad=[]
for line in manifest.read_text().splitlines():
    if not line.strip(): continue
    exp_sha, exp_bytes, rel=line.split()
    a=snap/rel; b=dst/rel
    if hashlib.sha256(a.read_bytes()).hexdigest()!=hashlib.sha256(b.read_bytes()).hexdigest():
        bad.append(rel)
print(f"mismatches={bad}")
assert not bad
PY
# 7. SOURCE-only add (tool sources only, no E): M + ?? filtered to TOOL_DIRS/top files, no pycache
run_tag status-pre git -C "$FIXTURE" status --porcelain=v1 --untracked-files=all
run_tag add-736 python3 - "$FIXTURE" <<'PY'
import subprocess, pathlib, sys
dst=pathlib.Path(sys.argv[1])
TOOL_DIRS=("scripts","schemas","config","templates","tests","docs","specials",".github")
TOOL_TOP=("AGENTS.md","README.md",".latexmkrc",".gitignore")
r=subprocess.run(["git","-C",str(dst),"status","--porcelain=v1","--untracked-files=all"], capture_output=True, text=True)
assert r.returncode==0
lines=r.stdout.splitlines()
print(f"status lines {len(lines)}")
add=[]
for l in lines:
    code=l[:2]; path=l[3:].strip().strip('"')
    if code.strip()=="M":
        add.append(path)
    elif code.strip()=="??":
        first=path.split("/")[0]
        if first in TOOL_DIRS or path in TOOL_TOP or first.startswith("."):
            if "__pycache__" not in path and not path.endswith(".pyc"):
                # only if path is in 736 manifest (intended) to avoid blind E add
                add.append(path)
print(f"ADD_CANDIDATES {len(add)}")
# verify each add path is in intended 736 list
manifest=set()
for line in open("notes/rephase-1-versioned-renewal-implementation/resume-20261025/final-integration-input-evidence-20261025T051343Z/dst-hash-intended-stdout.txt"):
    if line.strip():
        manifest.add(line.split()[2])
bad=[p for p in add if p not in manifest and not p.startswith(".git")]
# allow .git? no
print(f"manifest check bad={bad[:10]}")
# filter to only manifest members (SOURCE-only)
filtered=[p for p in add if p in manifest]
print(f"FILTERED {len(filtered)}")
open("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-longform-20261025T060000Z/tmp/longform-addlist-060000Z.txt","w").write("\n".join(sorted(filtered))+"\n")
print("\n".join(sorted(filtered)[:20]))
PY
run_tag addlist-cat cat "$PARENT/tmp/longform-addlist-060000Z.txt"
# git add exact filtered list
run_tag git-add bash -c 'mapfile -t L < .rephase-1-editorial-runtime/versioned-renewal-longform-20261025T060000Z/tmp/longform-addlist-060000Z.txt; git -C "'"$FIXTURE"'" add -- "${L[@]}"'
run_tag diff-cached-names git -C "$FIXTURE" diff --cached --name-only
run_tag head-pre git -C "$FIXTURE" rev-parse HEAD
run_tag commit-g1 git -C "$FIXTURE" commit -m "LONGFORM TEST-ONLY: G1 base 736 overlay (actual409+86 on old721 ancestry, SOURCE-only, no E rewrite)" --no-verify
run_tag head-post git -C "$FIXTURE" rev-parse HEAD
run_tag ancestor-g1 git -C "$FIXTURE" merge-base --is-ancestor 721a04d85532d7855f3e54cc411f5847c787726e HEAD
run_tag log-g1 git -C "$FIXTURE" log --oneline -3
run_tag status-post git -C "$FIXTURE" status --porcelain=v1 --untracked-files=all
run_tag diff-cached-post git -C "$FIXTURE" diff --cached --name-only
echo "DONE OK LONGFORM setup G1" >>"$EVID/commands.log"
