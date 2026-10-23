#!/usr/bin/env bash
# NEW inspect-only full isolation + closure/registry audit for R3 map resolution.
# No source copy recreation, no checkout/reset/clean, no network, no source imports/tests.
# Sanitized Git env; read-only verification only.
set -u
export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL=/dev/null
export GIT_OPTIONAL_LOCKS=0
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_OBJECT_DIRECTORY GIT_ALTERNATE_OBJECT_DIRECTORIES GIT_COMMON_DIR GIT_PREFIX || true
export PYTHONDONTWRITEBYTECODE=1

SRC="/tmp/opencode/jgas-style-correction-20261019T135318Z/candidate-partial-b40de60"
DST="/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60"
RECON="/home/eariver/git/reconstruct-japanese-generative-ai-survey"
MANIFEST="notes/rephase-1-initial-build-integration/source-packaging/complete22-manifest.json"
STATIC21="notes/rephase-1-dm021-p3s/draft-history-r11/static21.json"
PATCH="notes/rephase-1-initial-build-integration/source-packaging/complete22-409-clean.patch"

echo "=== R3 map-resolution full inspection (read-only) ==="
date -u; echo "exit_date=$?"
echo "src=${SRC}"
echo "dst=${DST}"
echo "recon=${RECON}"
echo "--- workspace head/contract (read-only) ---"
git rev-parse HEAD; echo "exit_ws_head=$?"
git log --oneline -2; echo "exit_ws_log=$?"
sha256sum outputs/rephase-1-editorial-operation-contract-decision.md; echo "exit_contract=$?"
git status --porcelain=v1 --untracked-files=all | sort; echo "exit_ws_status=$?"
echo "--- SRC identity pre ---"
git --no-optional-locks -C "$SRC" rev-parse HEAD; echo "exit_src_head=$?"
git --no-optional-locks -C "$SRC" rev-parse 'HEAD^{tree}'; echo "exit_src_tree=$?"
git --no-optional-locks -C "$SRC" symbolic-ref -q HEAD; echo "exit_src_sym=$? (1 detached expected)"
git --no-optional-locks -C "$SRC" status --porcelain=v1 --untracked-files=all | sort; echo "exit_src_status=$?"
git --no-optional-locks -C "$SRC" diff --cached --name-only; echo "exit_src_cached=$? (empty)"
git --no-optional-locks -C "$SRC" diff HEAD --name-only | sort; echo "exit_src_diff=$?"
echo "--- DST identity ---"
git --no-optional-locks -C "$DST" rev-parse HEAD; echo "exit_dst_head=$?"
git --no-optional-locks -C "$DST" rev-parse 'HEAD^{tree}'; echo "exit_dst_tree=$?"
git --no-optional-locks -C "$DST" symbolic-ref -q HEAD; echo "exit_dst_sym=$? (1 detached expected)"
git --no-optional-locks -C "$DST" status --porcelain=v1 --untracked-files=all | sort; echo "exit_dst_status=$?"
git --no-optional-locks -C "$DST" diff --cached --name-only; echo "exit_dst_cached=$? (empty)"
git --no-optional-locks -C "$DST" diff HEAD --name-only | sort; echo "exit_dst_diff=$?"
echo "--- RECON identity (read-only, no fetch) ---"
git rev-parse HEAD; echo "exit_recon_head=$?"
git rev-parse 'HEAD^{tree}'; echo "exit_recon_tree=$?"
git symbolic-ref -q HEAD; echo "exit_recon_sym=$? (0 attached expected main)"
git remote -v; echo "exit_recon_remote=$?"
echo "--- git safety SRC/DST/RECON (configs, alternates, hooks, shallow) ---"
for label in SRC DST RECON; do
  case $label in
    SRC) R="$SRC";; DST) R="$DST";; RECON) R="$RECON";;
  esac
  echo "== $label root=$R =="
  git --no-optional-locks -C "$R" config --list --show-origin | grep -v "^file:/home" ; echo "exit_${label}_cfg=$?"
  git --no-optional-locks -C "$R" remote -v; echo "exit_${label}_remote=$?"
  echo "-- $label .git/info --"; ls "$R/.git/info/"; echo "exit_${label}_info=$?"
  echo "-- $label .git/objects/info --"; ls "$R/.git/objects/info/" 2>&1; echo "exit_${label}_objinfo=$? (2 expected absent: no objects/info dir)"
  echo "-- $label alternates1 --"; cat "$R/.git/objects/info/alternates" 2>&1; echo "exit_${label}_alt1=$? (1 expected absent)"
  echo "-- $label alternates2 --"; cat "$R/.git/info/alternates" 2>&1; echo "exit_${label}_alt2=$? (1 expected absent)"
  echo "-- $label shallow --"; cat "$R/.git/shallow" 2>&1 | head -n 3; echo "exit_${label}_shallow=$?"
  echo "-- $label HEAD file --"; cat "$R/.git/HEAD" 2>&1; echo "exit_${label}_headfile=$?"
  echo "-- $label hooks --"; ls "$R/.git/hooks/" 2>&1; echo "exit_${label}_hooks=$?"
  ls "$R/.git/hooks/" 2>&1 | grep -v "\.sample$" || echo "$label no_active_hooks (expected)"; echo "exit_${label}_activehooks=$?"
done
echo "--- source22 pins pre (SRC) ---"
python3 -c "import json,hashlib,os,pathlib,stat as st; m=json.load(open('$MANIFEST')); root=pathlib.Path('$SRC'); ok=0; bad=[];
for rel,exp in sorted(m['files'].items()):
 p=root/rel
 if not p.is_file(): bad.append((rel,'missing')); continue
 d=p.read_bytes(); h=hashlib.sha256(d).hexdigest(); mode=oct(st.S_IMODE(os.stat(p).st_mode))
 if h==exp['sha256'] and len(d)==exp['bytes'] and mode==exp['mode']: ok+=1
 else: bad.append(rel)
print(f'src_pin_pre OK={ok} TOTAL={len(m[\"files\"])} MISMATCHES={len(bad)}')
print('BAD:',bad[:5]) if bad else print('BAD: []')
"; echo "exit_src_pins_pre=$?"
echo "--- cache scope SRC/DST (depth-limited, not whole-tree cert) ---"
ls "$SRC/__pycache__" 2>&1; echo "exit_src_rootcache=$? (2 expected absent)"
find "$SRC" -maxdepth 2 -name __pycache__ -o -maxdepth 2 -name '*.pyc' 2>&1 | head; echo "exit_src_cache2=$?"
ls "$DST/__pycache__" 2>&1; echo "exit_dst_rootcache=$? (2 expected absent)"
find "$DST" -maxdepth 2 -name __pycache__ -o -maxdepth 2 -name '*.pyc' 2>&1 | head; echo "exit_dst_cache2=$?"
echo "--- patch/static21/style ---"
sha256sum "$PATCH"; echo "exit_patch=$?"
stat -c '%s %n' "$PATCH"; echo "exit_patch_bytes=$?"
sha256sum "$STATIC21"; echo "exit_static21=$?"
sha256sum "$SRC/templates/survey/jgaisurvey.sty"; echo "exit_style=$?"
echo "--- FULL .git regular-entry inode comparison (all entries, type-aware) ---"
python3 <<'PY'
import os, pathlib, collections
src = pathlib.Path("/tmp/opencode/jgas-style-correction-20261019T135318Z/candidate-partial-b40de60/.git")
dst = pathlib.Path("/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60/.git")
recon = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.git")
def census(root):
    reg=[]; dirs=0; symlinks=0; other=0
    inode_map={}  # (dev,ino) -> [rel]
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        # count dirs (including root handled once)
        for d in dirnames:
            p=pathlib.Path(dirpath)/d
            try:
                st=os.lstat(p)
            except FileNotFoundError:
                continue
            import stat as stmod
            if stmod.S_ISLNK(st.st_mode): symlinks+=1
            elif stmod.S_ISDIR(st.st_mode): dirs+=1
            else: other+=1
            key=(st.st_dev, st.st_ino)
            inode_map.setdefault(key, []).append(str(p.relative_to(root)))
        for f in filenames:
            p=pathlib.Path(dirpath)/f
            try:
                st=os.lstat(p)
            except FileNotFoundError:
                continue
            import stat as stmod
            if stmod.S_ISLNK(st.st_mode):
                symlinks+=1
            elif stmod.S_ISREG(st.st_mode):
                reg.append((str(p.relative_to(root)), st.st_dev, st.st_ino, st.st_size))
            else:
                other+=1
            key=(st.st_dev, st.st_ino)
            inode_map.setdefault(key, []).append(str(p.relative_to(root)))
    return {"reg":reg, "dirs":dirs, "symlinks":symlinks, "other":other, "inode_map":inode_map}
for label, root in (("SRC",src),("DST",dst),("RECON",recon)):
    c=census(root)
    print(f"{label} .git census: regular={len(c['reg'])} dirs={c['dirs']} symlinks={c['symlinks']} other={c['other']}")
    # duplicate inodes within same repo (hardlinks) — report count
    dup=sum(1 for k,v in c["inode_map"].items() if len(v)>1)
    print(f"{label} .git intra-repo duplicate-inode keys={dup}")
    if label=="SRC": src_c=c
    if label=="DST": dst_c=c
    if label=="RECON": recon_c=c
def shared(a,b):
    sa=set((d,i) for _,d,i,_ in a["reg"])
    sb=set((d,i) for _,d,i,_ in b["reg"])
    return sa & sb
for x,y in (("DST","SRC"),("DST","RECON"),("SRC","RECON")):
    A={"DST":dst_c,"SRC":src_c,"RECON":recon_c}[x]
    B={"DST":dst_c,"SRC":src_c,"RECON":recon_c}[y]
    s=shared(A,B)
    print(f"shared regular inodes {x} vs {y}: {len(s)} (0 expected independent)")
    if s:
        print(list(s)[:5])
# full worktree regular-file inode sharing DST vs SRC (excluding .git)
import subprocess
def worktree_regs(root):
    out=[]
    for dirpath, dirnames, filenames in os.walk(pathlib.Path(root), followlinks=False):
        if ".git" in pathlib.Path(dirpath).parts:
            # skip .git subtree entirely
            if pathlib.Path(root, ".git").as_posix() in dirpath or dirpath==pathlib.Path(root, ".git").as_posix():
                continue
        # prune .git dir
        if ".git" in dirnames:
            dirnames.remove(".git")
        for f in filenames:
            p=pathlib.Path(dirpath)/f
            try:
                st=os.lstat(p)
            except FileNotFoundError:
                continue
            import stat as stmod
            if stmod.S_ISREG(st.st_mode):
                out.append((str(p.relative_to(root)), st.st_dev, st.st_ino))
    return out
src_w=worktree_regs("/tmp/opencode/jgas-style-correction-20261019T135318Z/candidate-partial-b40de60")
dst_w=worktree_regs("/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60")
sa=set((d,i) for _,d,i in src_w); sb=set((d,i) for _,d,i in dst_w)
print(f"worktree regular files: SRC={len(src_w)} DST={len(dst_w)} shared={len(sa & sb)} (0 expected)")
PY
echo "exit_full_inode=$?"
echo "--- exact registry counts (read-only, no imports) ---"
python3 -c "import json; c=json.load(open('$SRC/config/survey-production-v2.json')); print('contract_files.pipeline =',len(c['contract_files']['pipeline'])); print('contract_files.quality =',len(c['contract_files']['quality'])); print('implementation_control_roots =',c['implementation_control_roots'])"; echo "exit_registry_counts=$?"
echo "--- _SHARED_PY (27) exact ---"
python3 -c "import ast,pathlib; t=ast.parse(pathlib.Path('$SRC/scripts/survey_editorial_staged_source_v2.py').read_text()); vals=None
for n in ast.walk(t):
  if isinstance(n,ast.Assign) and any(getattr(x,'id','')=='_SHARED_PY' for x in n.targets):
    vals=ast.literal_eval(n.value); break
print('len=',len(vals)); [print(v) for v in vals]"; echo "exit_shared_py=$?"
echo "--- _SHARED_SCHEMAS (5) exact ---"
python3 -c "import ast,pathlib; t=ast.parse(pathlib.Path('$SRC/scripts/survey_editorial_staged_source_v2.py').read_text()); vals=None
for n in ast.walk(t):
  if isinstance(n,ast.Assign) and any(getattr(x,'id','')=='_SHARED_SCHEMAS' for x in n.targets):
    vals=ast.literal_eval(n.value); break
print('len=',len(vals)); [print(v) for v in vals]"; echo "exit_shared_sch=$?"
echo "--- CURRENT_CLOSURE weekly (8) exact ---"
python3 -c "import ast,pathlib; t=ast.parse(pathlib.Path('$SRC/scripts/survey_weekly_derivation_v2.py').read_text()); vals=None
for n in ast.walk(t):
  if isinstance(n,ast.Assign) and any(getattr(x,'id','')=='CURRENT_CLOSURE' for x in n.targets):
    import ast as a; vals=[a.unparse(x) if hasattr(a,'unparse') else str(x) for x in n.value.elts]; break
print('len=',len(vals)); [print(v) for v in vals]"; echo "exit_weekly_closure=$?"
echo "--- CURRENT_CLOSURE longform (14) exact ---"
python3 -c "import ast,pathlib; t=ast.parse(pathlib.Path('$SRC/scripts/survey_longform_generated_v2.py').read_text()); vals=None
for n in ast.walk(t):
  if isinstance(n,ast.Assign) and any(getattr(x,'id','')=='CURRENT_CLOSURE' for x in n.targets):
    import ast as a; vals=[a.unparse(x) if hasattr(a,'unparse') else str(x) for x in n.value.elts]; break
print('len=',len(vals)); [print(v) for v in vals]"; echo "exit_longform_closure=$?"
echo "--- top-level imports (AST, no source import) for closure justification ---"
python3 <<'PY'
import ast, pathlib
roots=["/tmp/opencode/jgas-style-correction-20261019T135318Z/candidate-partial-b40de60/scripts"]
files=["survey_weekly_derivation_v2.py","survey_longform_generated_v2.py","survey_longform_derivation_v2.py",
"survey_editorial_staged_source_v2.py","survey_editorial_retention_v2.py",
"survey_editorial_correction_proposal_v2.py","survey_editorial_current_authority_v2.py",
"survey_agent_control_v2.py","survey_production_v2.py","survey_stage_validation_v2.py",
"survey_reader_publication_v2.py","survey_reader_surface_gate_v2.py","survey_quality_v2.py",
"survey_publication_v2.py","survey_profiled_freeze_v2.py"]
for fn in files:
    p=pathlib.Path(roots[0])/fn
    try:
        t=ast.parse(p.read_text())
    except Exception as e:
        print(f"{fn}: PARSE_FAIL {e}"); continue
    tops=[]
    for n in t.body:
        if isinstance(n,ast.Import):
            tops.append("import "+" ,".join(a.name for a in n.names))
        elif isinstance(n,ast.ImportFrom) and (n.level==0 or n.level==1):
            mod="."*n.level+(n.module or "")
            tops.append(f"from {mod} import "+",".join(a.name for a in n.names))
    print(f"== {fn} top-level imports ({len(tops)}) ==")
    for x in tops: print("  "+x)
PY
echo "exit_ast=$?"
echo "--- source22 pins post (SRC, no mutation) ---"
python3 -c "import json,hashlib,os,pathlib,stat as st; m=json.load(open('$MANIFEST')); root=pathlib.Path('$SRC'); ok=0; bad=[];
for rel,exp in sorted(m['files'].items()):
 p=root/rel
 d=p.read_bytes() if p.is_file() else b''; h=hashlib.sha256(d).hexdigest() if p.is_file() else 'missing'; mode=oct(st.S_IMODE(os.stat(p).st_mode)) if p.is_file() else 'missing'
 if h==exp['sha256'] and len(d)==exp['bytes'] and mode==exp['mode']: ok+=1
 else: bad.append(rel)
print(f'src_pin_post OK={ok} TOTAL={len(m[\"files\"])} MISMATCHES={len(bad)}')"; echo "exit_src_pins_post=$?"
echo "=== DONE (inspect-only, no mutation) ==="
