#!/usr/bin/env bash
set -u
# LONGFORM repair fixture setup — NEW independent clone of valid U3b r6 + 739 overlay preserve style variant
# OLD valid: .rephase-1-editorial-runtime/versioned-renewal-longform-20261025T060000Z/renewal-longform (HEAD 18587b6, State r6 pending, style b1cbb...)
# NEW repair INPUT: .rephase-1-editorial-runtime/versioned-renewal-repair-input-20261025T082826Z/snapshot-work (739, dst 20f1967f...)
# NEW owned: .rephase-1-editorial-runtime/versioned-renewal-longform-repair-20261025T090000Z/renewal-longform
# EVID: notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-integration-repair/setup-20261025T090000Z/
EVID="notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-integration-repair/setup-20261025T090000Z"
OLD=".rephase-1-editorial-runtime/versioned-renewal-longform-20261025T060000Z/renewal-longform"
SNAP=".rephase-1-editorial-runtime/versioned-renewal-repair-input-20261025T082826Z/snapshot-work"
PARENT=".rephase-1-editorial-runtime/versioned-renewal-longform-repair-20261025T090000Z"
FIXTURE=".rephase-1-editorial-runtime/versioned-renewal-longform-repair-20261025T090000Z/renewal-longform"
run_tag() {
  tag="$1"; shift
  out_std="$EVID/${tag}-stdout.txt"
  out_err="$EVID/${tag}-stderr.txt"
  out_exit="$EVID/${tag}-exit.txt"
  tmp_out=$(mktemp)
  tmp_err=$(mktemp)
  "$@" >"$tmp_out" 2>"$tmp_err"
  rc=$?
  cat "$tmp_out" >"$out_std"
  cat "$tmp_err" >"$out_err"
  echo "$rc" >"$out_exit"
  echo "\$ $*  # cwd=$(pwd) -> exit=$rc" >>"$EVID/commands.log"
  rm -f "$tmp_out" "$tmp_err"
  return $rc
}
echo "LONGFORM repair setup start $(date -u +%Y%m%dT%H%M%SZ) PID=$$" | tee "$EVID/commands.log"
if [ -n "${GIT_DIR:-}" ] || [ -n "${GIT_WORK_TREE:-}" ] || [ -n "${GIT_INDEX_FILE:-}" ]; then echo "FATAL inherited GIT env" >&2; exit 1; fi
run_tag env-check env
run_tag recon-head git rev-parse HEAD
run_tag recon-status git status --porcelain=v1 --untracked-files=all
# verify repair INPUT
run_tag snap-head git -C "$SNAP" rev-parse HEAD
run_tag snap-tree git -C "$SNAP" rev-parse "HEAD^{tree}"
run_tag snap-count bash -c "find \"$SNAP\" -path \"$SNAP/.git\" -prune -o -type f -print | wc -l"
run_tag snap-git-count bash -c "find \"$SNAP/.git\" -type f | wc -l"
run_tag snap-remote git -C "$SNAP" remote -v
# verify OLD valid fixture
run_tag old-head git -C "$OLD" rev-parse HEAD
run_tag old-tree git -C "$OLD" rev-parse "HEAD^{tree}"
run_tag old-log git -C "$OLD" log --oneline -7
run_tag old-status git -C "$OLD" status --porcelain=v1 --untracked-files=all
run_tag old-state python3 - "$OLD" <<'PY'
import sys, json, pathlib, hashlib
fix=pathlib.Path(sys.argv[1])
st=json.load(open(fix/"sources/SP001/production-state.json"))
print(f"lifecycle={st.get('lifecycle_state')} pointer={st.get('publication_revalidation_provenance')} gates={st.get('human_gates')}")
# check synthetic Preview exists but State pending (don't delete)
import pathlib as pl
previews=list((fix/"sources/SP001/publication/v2/editorial-corrections/lf-boot-1").rglob("*preview-approval.json"))
print(f"preview files={previews}")
assert (fix/"sources/SP001/publication/v2/editorial-corrections/lf-boot-1/lifecycle-high-u3b-longform-direct/preview-approval.json").exists()
assert st.get('human_gates',{}).get('publication_preview')=='pending'
print("PREVIEW_PENDING_DONT_DELETE_OK")
# style variant
print(f"style {hashlib.sha256((fix/'templates/survey/jgaisurvey.sty').read_bytes()).hexdigest()}")
PY
# create parent (fail if exists)
if [ -e "$PARENT" ]; then echo "FATAL parent exists $PARENT" >&2; exit 1; fi
run_tag mkdir-parent mkdir -p "$PARENT"
run_tag mkdir-evid mkdir -p "$EVID"
mkdir -p "$PARENT/tmp"
export TMPDIR="$PARENT/tmp"
ADDLIST="$PARENT/tmp/repair-addlist-090000Z.txt"
echo "TMPDIR=$TMPDIR" >>"$EVID/commands.log"
# byte-independent clone from OLD valid (retain 721+G1-G5 ancestry + U3b r6 State source)
run_tag clone-0 git clone --no-hardlinks "$OLD" "$FIXTURE"
run_tag remote-set git -C "$FIXTURE" remote set-url origin https://example.invalid/versioned-renewal-chain-longform-repair.git
run_tag remote-show git -C "$FIXTURE" remote -v
run_tag cfg-user-name git -C "$FIXTURE" config user.name rephase-fixture-longform-repair
run_tag cfg-user-email git -C "$FIXTURE" config user.email fixture-longform-repair@example.invalid
run_tag cfg-gpgsign git -C "$FIXTURE" config commit.gpgsign false
run_tag fixture-head git -C "$FIXTURE" rev-parse HEAD
run_tag fixture-tree git -C "$FIXTURE" rev-parse "HEAD^{tree}"
run_tag fixture-gitdir git -C "$FIXTURE" rev-parse --absolute-git-dir
run_tag noalternates bash -c "test ! -e \"$FIXTURE/.git/objects/info/alternates\" && echo NO_ALTERNATES || (echo HAS_ALTERNATES; exit 1)"
run_tag config-show git -C "$FIXTURE" config --list --show-origin
# copy captured valid U3b r6 + old E/source ancestry (explicit, SHA verify, exclude alias)
run_tag copy-valid python3 - "$OLD" "$FIXTURE" <<'PY'
import sys, hashlib, shutil, subprocess, pathlib
old=pathlib.Path(sys.argv[1]); dst=pathlib.Path(sys.argv[2])
def ls(args):
    r=subprocess.run(["git","-C",str(old)]+args, capture_output=True, text=True)
    assert r.returncode==0, r.stderr
    return [l for l in r.stdout.splitlines() if l.strip()]
others=ls(["ls-files","--others","--exclude-standard"])
ignored=ls(["ls-files","--others","--ignored","--exclude-standard"])
all_e=others+ignored
print(f"E files: others={len(others)} ignored={len(ignored)} total={len(all_e)}")
# exclusion: owned alias record (never tree-rm original; new fixture excludes, record explicit)
excluded=[]
copied=0
for rel in all_e:
    if rel.endswith(".alias.json"):
        print(f"EXCLUDED alias {rel} (owned neg test, fresh copy from before alias data, no hiding)")
        excluded.append(rel)
        continue
    s=old/rel; d=dst/rel
    assert s.exists(), f"missing SRC {rel}"
    if d.exists():
        raise SystemExit(f"E target exists {rel}")
    if s.is_dir() and not s.is_symlink():
        shutil.copytree(str(s), str(d), symlinks=True, copy_function=shutil.copy2)
    else:
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(s), str(d))
    if s.is_file() and not s.is_symlink():
        hs=hashlib.sha256(s.read_bytes()).hexdigest()
        hd=hashlib.sha256(d.read_bytes()).hexdigest()
        assert hs==hd, f"SHA mismatch {rel}"
    copied+=1
print(f"COPY_VALID_DONE copied={copied} excluded={excluded}")
# verify preview still pending, State r6
import json
st=json.load(open(dst/"sources/SP001/production-state.json"))
assert st["publication_revalidation_provenance"]["path"].endswith("r6.json")
assert st["human_gates"]["publication_preview"]=="pending"
assert (dst/"sources/SP001/publication/v2/editorial-corrections/lf-boot-1/lifecycle-high-u3b-longform-direct/preview-approval.json").exists()
print("PREVIEW_PENDING_PRESERVED")
PY
# overlay EXACT 739 except preserve style variant b1cbb... + G6 SOURCE-only commit
run_tag overlay-739-real python3 - "$SNAP" "$FIXTURE" "$EVID" <<'PY'
import hashlib, shutil, pathlib, sys
snap=pathlib.Path(sys.argv[1]); dst=pathlib.Path(sys.argv[2]); evid=pathlib.Path(sys.argv[3])
manifest=pathlib.Path("notes/rephase-1-versioned-renewal-implementation/resume-20261025/integration-repair-input-evidence-20261025T082826Z/dst-hash-intended-stdout.txt")
lines=[l.strip() for l in manifest.read_text().splitlines() if l.strip()]
assert len(lines)==739, len(lines)
style_rel="templates/survey/jgaisurvey.sty"
style_before=hashlib.sha256((dst/style_rel).read_bytes()).hexdigest()
print(f"style_before (fixture G2 variant) {style_before}")
assert style_before=="b1cbbdd93711aef17b37d3bbbedda25aa0bcb51f462bdc7ad172ce2aa103c8f4", style_before
mism=[]
copied=0
for line in lines:
    exp_sha, exp_bytes, rel=line.split()
    if rel==style_rel:
        print(f"PRESERVE style variant {rel} (keep {style_before[:12]}, not baseline 035645...)")
        continue
    s=snap/rel; d=dst/rel
    assert s.is_file(), rel
    d.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(s), str(d))
    got=hashlib.sha256(d.read_bytes()).hexdigest()
    if got!=exp_sha:
        mism.append((rel, exp_sha, got))
    if int(exp_bytes)!=d.stat().st_size:
        mism.append((rel+":bytes", exp_bytes, str(d.stat().st_size)))
    copied+=1
print(f"OVERLAY_DONE copied={copied} mismatches={mism[:3]}")
assert not mism
assert hashlib.sha256((dst/style_rel).read_bytes()).hexdigest()==style_before
print(f"style preserved {style_before[:12]}")
(evid/"source-variant-manifest.txt").write_text(f"style {style_rel} preserved {style_before} (baseline 035645caa06eb77e5416ae7a54bc1fb7b987e0b575a02bd4b512bccb5d683aec overlaid would force C new targets; U reuse C targets remains possible)\n", encoding="utf-8")
print("VARIANT_MANIFEST_WRITTEN")
PY
run_tag overlay-verify python3 - "$SNAP" "$FIXTURE" <<'PY'
import hashlib, pathlib, sys
snap=pathlib.Path(sys.argv[1]); dst=pathlib.Path(sys.argv[2])
manifest=pathlib.Path("notes/rephase-1-versioned-renewal-implementation/resume-20261025/integration-repair-input-evidence-20261025T082826Z/dst-hash-intended-stdout.txt")
bad=[]
for line in manifest.read_text().splitlines():
    if not line.strip(): continue
    exp_sha, exp_bytes, rel=line.split()
    if rel=="templates/survey/jgaisurvey.sty":
        continue
    a=snap/rel; b=dst/rel
    if hashlib.sha256(a.read_bytes()).hexdigest()!=hashlib.sha256(b.read_bytes()).hexdigest():
        bad.append(rel)
print(f"mismatches={bad}")
assert not bad
print("OVERLAY_VERIFY_OK (738/739, style preserved)")
PY
run_tag status-pre git -C "$FIXTURE" status --porcelain=v1 --untracked-files=all
run_tag add-G6 python3 - "$FIXTURE" <<'PY'
import subprocess, pathlib, sys
dst=pathlib.Path(sys.argv[1])
TOOL_DIRS=("scripts","schemas","config","templates","tests","docs","specials",".github")
TOOL_TOP=("AGENTS.md","README.md",".latexmkrc",".gitignore")
r=subprocess.run(["git","-C",str(dst),"status","--porcelain=v1","--untracked-files=all"], capture_output=True, text=True)
assert r.returncode==0
add=[]
for l in r.stdout.splitlines():
    code=l[:2]; path=l[3:].strip().strip('"')
    if code.strip()=="M":
        add.append(path)
    elif code.strip()=="??":
        first=path.split("/")[0]
        if first in TOOL_DIRS or path in TOOL_TOP or first.startswith("."):
            if "__pycache__" not in path and not path.endswith(".pyc"):
                add.append(path)
print(f"ADD_CANDIDATES {len(add)}")
manifest=set()
for line in open("notes/rephase-1-versioned-renewal-implementation/resume-20261025/integration-repair-input-evidence-20261025T082826Z/dst-hash-intended-stdout.txt"):
    if line.strip():
        manifest.add(line.split()[2])
# style preserved, so style should NOT be in add (no change); filter to manifest but exclude style (already preserved)
filtered=[p for p in add if p in manifest and p!="templates/survey/jgaisurvey.sty"]
print(f"FILTERED {len(filtered)} (style excluded, preserved)")
open(f"{dst.parent}/tmp/repair-addlist-090000Z.txt","w").write("\n".join(sorted(filtered))+"\n")
print("\n".join(sorted(filtered)[:30]))
PY
run_tag addlist-cat cat "$PARENT/tmp/repair-addlist-090000Z.txt"
run_tag git-add bash -c 'mapfile -t L < .rephase-1-editorial-runtime/versioned-renewal-longform-repair-20261025T090000Z/tmp/repair-addlist-090000Z.txt; git -C ".rephase-1-editorial-runtime/versioned-renewal-longform-repair-20261025T090000Z/renewal-longform" add -- "${L[@]}"'
run_tag diff-cached-names git -C "$FIXTURE" diff --cached --name-only
run_tag head-pre git -C "$FIXTURE" rev-parse HEAD
run_tag commit-G6 git -C "$FIXTURE" commit -m "LONGFORM TEST-ONLY: G6 repair 739 overlay (H/P1/PUB new, style b1cbb preserved for U reuse)" --no-verify
run_tag head-post git -C "$FIXTURE" rev-parse HEAD
run_tag ancestor-G6 git -C "$FIXTURE" merge-base --is-ancestor 721a04d85532d7855f3e54cc411f5847c787726e HEAD
run_tag log-G6 git -C "$FIXTURE" log --oneline -8
run_tag status-post git -C "$FIXTURE" status --porcelain=v1 --untracked-files=all
run_tag diff-cached-post git -C "$FIXTURE" diff --cached --name-only
echo "DONE OK LONGFORM repair setup G6" >>"$EVID/commands.log"
