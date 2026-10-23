#!/usr/bin/env bash
# NEW preparation for R3 editorial operation implementation (pre-code, no code edits).
# Creates NEW independent implementation copy under /tmp/opencode unique root.
# Preserves original source and R2 fixtures; no restore/reapply of old scripts,
# no git clean/reset/raw deletion, no candidate/reconstruct commits, no network.
# Sanitized Git env; read-only verification of source + write-once copy + verification.
set -u
export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL=/dev/null
export GIT_OPTIONAL_LOCKS=0
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_OBJECT_DIRECTORY GIT_ALTERNATE_OBJECT_DIRECTORIES GIT_COMMON_DIR GIT_PREFIX || true
export PYTHONDONTWRITEBYTECODE=1

SRC="/tmp/opencode/jgas-style-correction-20261019T135318Z/candidate-partial-b40de60"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
DST_ROOT="/tmp/opencode/jgas-editorial-op-impl-${STAMP}"
DST="${DST_ROOT}/candidate-partial-b40de60"
MANIFEST="notes/rephase-1-initial-build-integration/source-packaging/complete22-manifest.json"
STATIC21="notes/rephase-1-dm021-p3s/draft-history-r11/static21.json"
PATCH="notes/rephase-1-initial-build-integration/source-packaging/complete22-409-clean.patch"
REPRO_ROOT="$(pwd)"

echo "=== R3 editorial-op implementation copy preparation ==="
echo "stamp_utc=${STAMP}"
echo "src=${SRC}"
echo "dst_root=${DST_ROOT} (NEW unique root)"
echo "dst=${DST}"
echo "repro_root=${REPRO_ROOT}"
echo "--- inherited git env (must be empty for GIT_DIR etc) ---"
echo "GIT_DIR=${GIT_DIR-unset}"
echo "GIT_WORK_TREE=${GIT_WORK_TREE-unset}"
echo "GIT_INDEX_FILE=${GIT_INDEX_FILE-unset}"
echo "GIT_OBJECT_DIRECTORY=${GIT_OBJECT_DIRECTORY-unset}"
echo "GIT_ALTERNATE_OBJECT_DIRECTORIES=${GIT_ALTERNATE_OBJECT_DIRECTORIES-unset}"
echo "GIT_COMMON_DIR=${GIT_COMMON_DIR-unset}"
echo "GIT_PREFIX=${GIT_PREFIX-unset}"
echo "--- workspace head (reconstruct, read-only) ---"
git rev-parse HEAD; echo "exit_head=$?"
git log --oneline -3; echo "exit_log=$?"
git status --porcelain=v1 --untracked-files=all | head -n 20; echo "exit_ws_status=$?"

echo "--- source identity (sanitized, read-only) ---"
git --no-optional-locks -C "$SRC" rev-parse HEAD; echo "exit_src_head=$?"
git --no-optional-locks -C "$SRC" rev-parse 'HEAD^{tree}'; echo "exit_src_tree=$?"
git --no-optional-locks -C "$SRC" symbolic-ref -q HEAD; echo "exit_src_symbolic=$? (1 expected detached)"
git --no-optional-locks -C "$SRC" status --porcelain=v1 --untracked-files=all | sort; echo "exit_src_status=$?"
git --no-optional-locks -C "$SRC" status --porcelain=v1 --untracked-files=all | sort | wc -l; echo "exit_src_status_count=$?"
git --no-optional-locks -C "$SRC" diff --cached --name-only; echo "exit_src_cached=$? (empty expected)"
git --no-optional-locks -C "$SRC" diff HEAD --name-only | sort; echo "exit_src_diff=$?"
git --no-optional-locks -C "$SRC" diff HEAD --name-only | sort | wc -l; echo "exit_src_diff_count=$?"
git --no-optional-locks -C "$SRC" config --list --show-origin | grep -v "^file:/home"; echo "exit_src_config=$?"
git --no-optional-locks -C "$SRC" remote -v; echo "exit_src_remote=$?"
echo "--- source git safety ---"
ls "$SRC/.git/info/"; echo "exit_src_gitinfo=$?"
cat "$SRC/.git/info/exclude" 2>&1 | head -n 5; echo "exit_src_exclude=$?"
ls "$SRC/.git/objects/info/" 2>&1; echo "exit_src_objects_info=$? (non-zero expected: no objects/info dir)"
cat "$SRC/.git/objects/info/alternates" 2>&1; echo "exit_src_alternates1=$? (non-zero expected absent)"
cat "$SRC/.git/info/alternates" 2>&1; echo "exit_src_alternates2=$? (non-zero expected absent)"
ls "$SRC/.git/hooks/"; echo "exit_src_hooks=$? (only *.sample expected)"
ls "$SRC/.git/hooks/" | grep -v "\.sample$" || echo "no_active_hooks (expected)"; echo "exit_src_active_hooks=$?"
cat "$SRC/.git/shallow"; echo "exit_src_shallow=$?"
cat "$SRC/.git/HEAD"; echo "exit_src_HEADfile=$?"
ls -la "$SRC/.git/index" 2>&1; echo "exit_src_index=$?"
echo "--- source manifest / patch / static21 / style ---"
sha256sum "$PATCH"; echo "exit_patch_sha=$?"
stat -c '%s %n' "$PATCH"; echo "exit_patch_bytes=$?"
python3 -c "import json,hashlib,os,pathlib; m=json.load(open('$MANIFEST')); ok=0; tot=len(m['files']); bad=[]; root=pathlib.Path('$SRC'); import stat as st; 
for rel,exp in sorted(m['files'].items()):
 p=root/rel
 if not p.is_file(): bad.append((rel,'missing')); continue
 data=p.read_bytes()
 h=hashlib.sha256(data).hexdigest()
 mode=oct(st.S_IMODE(os.stat(p).st_mode))
 if h!=exp['sha256'] or len(data)!=exp['bytes'] or mode!=exp['mode']: bad.append((rel,h,len(data),mode,exp))
 else: ok+=1
print(f'pin_check OK={ok} TOTAL={tot} MISMATCHES={len(bad)}')
for b in bad[:10]: print(b)
"; echo "exit_pins=$?"
sha256sum "$STATIC21"; echo "exit_static21=$?"
sha256sum "$SRC/templates/survey/jgaisurvey.sty"; echo "exit_style=$?"
stat -c '%s %n' "$SRC/templates/survey/jgaisurvey.sty"; echo "exit_style_bytes=$?"
echo "--- TL2026 probe (availability only, no installer/test/build) ---"
ls /tmp/opencode/jgas-texlive-20261019T133205Z/texlive/bin/ 2>&1 | head -n 8; echo "exit_texbin=$?"
ls /tmp/opencode/jgas-final22-builds-20261019T135318Z/weekly-build/ 2>&1 | head -n 8; echo "exit_weeklybuild=$?"
ls /tmp/opencode/jgas-final22-builds-20261019T135318Z/special-build/ 2>&1 | head -n 8; echo "exit_specialbuild=$?"
ls /tmp/opencode/ 2>&1 | grep -c jgas-; echo "exit_tmpcount=$?"

echo "--- create NEW DST root (no overwrite of existing) ---"
if [ -e "$DST_ROOT" ]; then echo "REFUSE: DST_ROOT exists: $DST_ROOT"; echo "exit_dst_exists=1"; exit 1; fi
mkdir -p "$DST_ROOT"; echo "exit_mkdir=$?"
echo "--- filesystem copy (independent, no hardlinks, no git mutation) ---"
cp -a "$SRC" "$DST"; echo "exit_cp=$?"
echo "--- DST verification (same identity, independent inodes) ---"
git --no-optional-locks -C "$DST" rev-parse HEAD; echo "exit_dst_head=$?"
git --no-optional-locks -C "$DST" rev-parse 'HEAD^{tree}'; echo "exit_dst_tree=$?"
git --no-optional-locks -C "$DST" symbolic-ref -q HEAD; echo "exit_dst_symbolic=$? (1 expected detached)"
git --no-optional-locks -C "$DST" status --porcelain=v1 --untracked-files=all | sort; echo "exit_dst_status=$?"
git --no-optional-locks -C "$DST" diff --cached --name-only; echo "exit_dst_cached=$? (empty expected)"
git --no-optional-locks -C "$DST" diff HEAD --name-only | sort; echo "exit_dst_diff=$?"
git --no-optional-locks -C "$DST" config --list --show-origin | grep -v "^file:/home"; echo "exit_dst_config=$?"
git --no-optional-locks -C "$DST" remote -v; echo "exit_dst_remote=$?"
ls "$DST/.git/hooks/" | grep -v "\.sample$" || echo "dst_no_active_hooks (expected)"; echo "exit_dst_active_hooks=$?"
cat "$DST/.git/objects/info/alternates" 2>&1; echo "exit_dst_alternates1=$? (non-zero expected)"
cat "$DST/.git/info/alternates" 2>&1; echo "exit_dst_alternates2=$? (non-zero expected)"
cat "$DST/.git/HEAD"; echo "exit_dst_HEADfile=$?"
echo "--- inode independence (sample: index + 3 worktree files + 1 object) ---"
stat -c '%d:%i %n' "$SRC/.git/index" "$DST/.git/index"; echo "exit_inode_index=$?"
stat -c '%d:%i %n' "$SRC/scripts/survey_agent_control_v2.py" "$DST/scripts/survey_agent_control_v2.py"; echo "exit_inode_agent=$?"
stat -c '%d:%i %n' "$SRC/templates/survey/jgaisurvey.sty" "$DST/templates/survey/jgaisurvey.sty"; echo "exit_inode_style=$?"
stat -c '%d:%i %n' "$SRC/schemas/publication-surface-revalidation.schema.json" "$DST/schemas/publication-surface-revalidation.schema.json"; echo "exit_inode_schema=$?"
python3 -c "
import os
pairs=[('.git/index',),('scripts/survey_agent_control_v2.py',),('templates/survey/jgaisurvey.sty',),('schemas/publication-surface-revalidation.schema.json',)]
import pathlib
src=pathlib.Path('$SRC'); dst=pathlib.Path('$DST')
shared=[]
for (rel,) in pairs:
 a=os.stat(src/rel); b=os.stat(dst/rel)
 same=(a.st_dev==b.st_dev and a.st_ino==b.st_ino)
 print(f'{rel} src={a.st_dev}:{a.st_ino} dst={b.st_dev}:{b.st_ino} shared={same}')
 if same: shared.append(rel)
print('SHARED_COUNT=',len(shared))
"; echo "exit_inode_compare=$?"
echo "--- DST pin recheck (22/22, no source mutation) ---"
python3 -c "import json,hashlib,os,pathlib,stat as st; m=json.load(open('$MANIFEST')); root=pathlib.Path('$DST'); ok=0; bad=[]; 
for rel,exp in sorted(m['files'].items()):
 p=root/rel
 data=p.read_bytes() if p.is_file() else b''
 h=hashlib.sha256(data).hexdigest() if p.is_file() else 'missing'
 mode=oct(st.S_IMODE(os.stat(p).st_mode)) if p.is_file() else 'missing'
 if h==exp['sha256'] and len(data)==exp['bytes'] and mode==exp['mode']: ok+=1
 else: bad.append(rel)
print(f'dst_pin_check OK={ok} TOTAL={len(m[\"files\"])} MISMATCHES={len(bad)}')
"; echo "exit_dst_pins=$?"
echo "--- no source mutation recheck ---"
git --no-optional-locks -C "$SRC" status --porcelain=v1 --untracked-files=all | sort | wc -l; echo "exit_src_status_recheck=$?"
echo "DST_ROOT=${DST_ROOT}"
echo "DST=${DST}"
echo "=== DONE (no code edits, no commits, no network) ==="
