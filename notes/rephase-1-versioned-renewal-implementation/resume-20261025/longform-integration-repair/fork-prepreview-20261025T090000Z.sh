#!/usr/bin/env bash
set -u
# Fork independent prePreview copy of U4 pending fixture for NORMAL branch
SRC=".rephase-1-editorial-runtime/versioned-renewal-longform-repair-20261025T090000Z/renewal-longform"
DST=".rephase-1-editorial-runtime/versioned-renewal-longform-repair-20261025T090000Z/renewal-longform-prepreview"
EVID="notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-integration-repair/fork-prepreview-20261025T090000Z"
mkdir -p "$EVID"
echo "fork start $(date -u +%Y%m%dT%H%M%SZ) PID=$$" | tee "$EVID/commands.log"
if [ -n "${GIT_DIR:-}" ] || [ -n "${GIT_WORK_TREE:-}" ] || [ -n "${GIT_INDEX_FILE:-}" ]; then echo "FATAL GIT env" >&2; exit 1; fi
run_tag() {
  tag="$1"; shift
  tmp_out=$(mktemp); tmp_err=$(mktemp)
  "$@" >"$tmp_out" 2>"$tmp_err"; rc=$?
  cat "$tmp_out" >"$EVID/${tag}-stdout.txt"
  cat "$tmp_err" >"$EVID/${tag}-stderr.txt"
  echo "$rc" >"$EVID/${tag}-exit.txt"
  echo "\$ $* -> exit=$rc" >>"$EVID/commands.log"
  rm -f "$tmp_out" "$tmp_err"
  return $rc
}
run_tag src-head git -C "$SRC" rev-parse HEAD
run_tag src-state python3 -c "import json; print(json.load(open('$SRC/sources/SP001/production-state.json'))['publication_revalidation_provenance'])"
if [ -e "$DST" ]; then echo "FATAL DST exists" >&2; exit 1; fi
run_tag clone-pp git clone --no-hardlinks "$SRC" "$DST"
run_tag remote-pp git -C "$DST" remote set-url origin https://example.invalid/versioned-renewal-chain-longform-prepreview.git
run_tag cfg-name git -C "$DST" config user.name rephase-fixture-longform-prepreview
run_tag cfg-email git -C "$DST" config user.email fixture-prepreview@example.invalid
run_tag cfg-gpgsign git -C "$DST" config commit.gpgsign false
run_tag dst-head git -C "$DST" rev-parse HEAD
run_tag copy-pp python3 - "$SRC" "$DST" <<'PY'
import sys, hashlib, shutil, subprocess, pathlib
src=pathlib.Path(sys.argv[1]); dst=pathlib.Path(sys.argv[2])
def ls(args):
    r=subprocess.run(["git","-C",str(src)]+args, capture_output=True, text=True)
    assert r.returncode==0, r.stderr
    return [l for l in r.stdout.splitlines() if l.strip()]
others=ls(["ls-files","--others","--exclude-standard"])
ignored=ls(["ls-files","--others","--ignored","--exclude-standard"])
all_e=others+ignored
print(f"others={len(others)} ignored={len(ignored)}")
excluded=[p for p in all_e if p.endswith(".alias.json")]
print(f"excluded alias={excluded}")
copied=0
for rel in all_e:
    if rel.endswith(".alias.json"):
        continue
    s=src/rel; d=dst/rel
    if d.exists():
        raise SystemExit(f"exists {rel}")
    if s.is_dir() and not s.is_symlink():
        shutil.copytree(str(s), str(d), symlinks=True, copy_function=shutil.copy2)
    else:
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(s), str(d))
    if s.is_file() and not s.is_symlink():
        assert hashlib.sha256(s.read_bytes()).hexdigest()==hashlib.sha256(d.read_bytes()).hexdigest()
    copied+=1
print(f"COPY_PP_DONE {copied}")
import json
assert json.load(open(dst/"sources/SP001/production-state.json"))["publication_revalidation_provenance"]["path"].endswith("r7.json")
print("PREVIEW_PENDING_PRESERVED r7")
PY
run_tag verify-pp python3 - "$SRC" "$DST" <<'PY'
import sys, pathlib, hashlib, subprocess
src=pathlib.Path(sys.argv[1]); dst=pathlib.Path(sys.argv[2])
# HEAD same, tree same, gitdir distinct, inode disjoint
import subprocess as sp
h1=sp.run(["git","-C",str(src),"rev-parse","HEAD"],capture_output=True,text=True).stdout.strip()
h2=sp.run(["git","-C",str(dst),"rev-parse","HEAD"],capture_output=True,text=True).stdout.strip()
print(f"src HEAD {h1} dst HEAD {h2}")
assert h1==h2
# State SHA same
import json
s1=json.load(open(src/"sources/SP001/production-state.json"))
s2=json.load(open(dst/"sources/SP001/production-state.json"))
assert s1==s2
print("FORK_IDENTICAL_OK")
PY
echo "DONE OK fork prePreview" >>"$EVID/commands.log"
