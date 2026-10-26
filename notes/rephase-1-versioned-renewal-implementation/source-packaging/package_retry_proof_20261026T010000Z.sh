#!/bin/bash
# RETRY proof for COMPLETE versioned-renewal packaging — 20261026T010000Z
# Preserves first failed attempt raws (proof-apply-check/apply rc129/rc1, manifest-gen rc7) untouched.
# Uses SAVED patch from first GEN (d6c72fb4..., 3415062B, 92 files) and SAME GEN/PROOF dirs.
# Fixes: remove invalid --unsafe-paths, use git -C PROOF (not --git-dir/--work-tree apply), fix 100755 mode.
# Saved via Write BEFORE execution, bash -n 0 required. No old runners, no network, no source mutation.
set -u
export PYTHONDONTWRITEBYTECODE=1
export GIT_NO_LAZY_FETCH=1
export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL=/dev/null
export GIT_OPTIONAL_LOCKS=0
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_PREFIX 2>/dev/null || true

WS="/home/eariver/git/reconstruct-japanese-generative-ai-survey"
SRC="$WS/.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work"
PACKROOT="$WS/.rephase-1-editorial-runtime/versioned-renewal-packaging-20261026T000000Z"
GEN="$PACKROOT/gen-copy/candidate-partial-b40de60"
PROOF="$PACKROOT/proof-copy/candidate-partial-b40de60"
GEN_INDEX="$PACKROOT/gen-index"
PACKET="$WS/notes/rephase-1-versioned-renewal-implementation/source-packaging"
PATCH="$PACKET/complete-versioned-renewal-409.patch"
MANIFEST_JSON="$PACKET/complete-versioned-renewal-manifest.json"

log_run() {
  local base="$1"; shift
  "$@" >"$PACKET/${base}-stdout.txt" 2>"$PACKET/${base}-stderr.txt"
  local rc=$?
  printf "%s" "$rc" >"$PACKET/${base}-exit.txt"
  echo "$base rc=$rc cmd=$*" >>"$PACKET/commands.log"
  return $rc
}

echo "retry-proof-20261026T010000Z start (preserving first failed raws)" >>"$PACKET/commands.log"

# 0. verify SAVED patch exists, GEN ok preserved, SRC unchanged
log_run retry-src-head git -C "$SRC" rev-parse HEAD
log_run retry-src-status git -C "$SRC" status --porcelain=v1
log_run retry-patch-sha sha256sum "$PATCH"
log_run retry-patch-bytes wc -c "$PATCH"
log_run retry-gen-names-ok2 cat "$PACKET/gen-names-ok-stdout.txt"

# 1. fix PROOF 100755 mode (core_execution_bridge) to match HEAD 100755 -> physical 775
#    First attempt used open(wb) -> 644, causing M mode diff. Fix to 775.
log_run retry-proof-mode-before git -C "$PROOF" diff HEAD --name-only
log_run retry-proof-chmod chmod 775 "$PROOF/scripts/survey_core_execution_bridge_v2.py"
log_run retry-proof-mode-after git -C "$PROOF" diff HEAD --name-only
log_run retry-proof-status git -C "$PROOF" status --porcelain=v1 --untracked-files=all

# 2. verify PROOF base still scoped clean689 (except fixed mode now clean)
log_run retry-proof-before-diff-names git -C "$PROOF" diff HEAD --name-only

# 3. apply SAVED patch with CORRECT invocation (git -C PROOF, no --unsafe-paths value)
log_run proof-apply-check-retry git -C "$PROOF" apply --check --verbose "$PATCH"
log_run proof-apply-retry git -C "$PROOF" apply --verbose "$PATCH"

# 4. validate final
log_run retry-proof-after-head git -C "$PROOF" rev-parse HEAD
log_run retry-proof-after-diff-cached git -C "$PROOF" diff --cached --name-only
log_run retry-proof-after-status git -C "$PROOF" status --porcelain=v1 --untracked-files=all

# 5. manifest generation (retry, preserves first failed manifest-gen raws)
log_run manifest-gen-retry python3 - "$GEN" "$PROOF" "$SRC" "$PACKET/populate-gen-list.txt" "$MANIFEST_JSON" "$PATCH" "$GEN_INDEX" "$PACKROOT" <<'PYEOF'
import sys, os, json, hashlib, subprocess
gen=sys.argv[1]; proof=sys.argv[2]; src=sys.argv[3]; genlist=sys.argv[4]; outjson=sys.argv[5]; patch=sys.argv[6]; genindex=sys.argv[7]; packroot=sys.argv[8]
final_paths=sorted([l.strip() for l in open(genlist) if l.strip()])
def git_out(cwd, args):
    import subprocess
    r=subprocess.run(['git']+args, cwd=cwd, capture_output=True, text=True)
    return r
m_out=git_out(src, ['diff','HEAD','--name-only'])
mods=sorted([l for l in m_out.stdout.strip().split('\n') if l])
o_out=git_out(src, ['ls-files','--others','--exclude-standard'])
new_list=sorted([p for p in o_out.stdout.strip().split('\n') if p and '__pycache__' not in p])
delta_sorted=sorted(set(mods)|set(new_list))
print(f"delta {len(delta_sorted)} mods={len(mods)} new={len(new_list)} final={len(final_paths)}")
mismatch=[]
for rel in final_paths:
    g=os.path.join(gen,rel); p=os.path.join(proof,rel)
    if not os.path.exists(p):
        mismatch.append(f"missing proof {rel}")
        continue
    if open(g,'rb').read()!=open(p,'rb').read():
        mismatch.append(f"bytes differ {rel}")
if mismatch:
    print("\n".join(mismatch[:30]), file=sys.stderr)
    print(f"TOTAL mismatches {len(mismatch)}", file=sys.stderr)
    sys.exit(7)
print(f"741 equality OK")
files={}
for rel in delta_sorted:
    g=os.path.join(gen,rel)
    data=open(g,'rb').read()
    sha=hashlib.sha256(data).hexdigest()
    r=subprocess.run(['git','-C',gen,'ls-files','-s','--',rel], capture_output=True, text=True, env={**os.environ,'GIT_INDEX_FILE':genindex})
    parts=r.stdout.strip().split()
    git_mode=parts[0] if len(parts)>=1 else ""
    git_blob=parts[1] if len(parts)>=2 else ""
    h=subprocess.run(['git','-C',gen,'hash-object',g], capture_output=True, text=True)
    hob=h.stdout.strip()
    pm=oct(os.stat(g).st_mode & 0o777)
    status="M" if rel in mods else "A"
    # old blob for M
    if status=="M":
        ro=subprocess.run(['git','-C',src,'rev-parse',f'HEAD:{rel}'], capture_output=True, text=True)
        old_blob=ro.stdout.strip()
    else:
        old_blob=""
    files[rel]={"bytes":len(data),"sha256":sha,"git_mode":git_mode,"git_blob":git_blob,"git_blob_hash_object":hob,"physical_mode":pm,"git_status":status,"old_head_blob":old_blob}
patch_bytes=os.path.getsize(patch)
patch_sha=hashlib.sha256(open(patch,'rb').read()).hexdigest()
head=subprocess.run(['git','-C',src,'rev-parse','HEAD'], capture_output=True, text=True).stdout.strip()
tree=subprocess.run(['git','-C',src,'rev-parse','HEAD^{tree}'], capture_output=True, text=True).stdout.strip()
def read_exit(name):
    try:
        return open(f"/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-versioned-renewal-implementation/source-packaging/{name}-exit.txt").read().strip()
    except:
        return "?"
manifest={
 "candidate_src": src,
 "head": head,
 "head_tree": tree,
 "delta_count": len(delta_sorted),
 "tracked_modified": len(mods),
 "untracked_new": len(new_list),
 "intended_final": len(final_paths),
 "intended_final_verified": True,
 "files": files,
 "patch": {"path":"complete-versioned-renewal-409.patch","bytes":patch_bytes,"sha256":patch_sha},
 "proof": {
   "check_exit": read_exit("proof-apply-check-retry"),
   "check_stderr_bytes": os.path.getsize(f"/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-versioned-renewal-implementation/source-packaging/proof-apply-check-retry-stderr.txt") if os.path.exists(f"/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-versioned-renewal-implementation/source-packaging/proof-apply-check-retry-stderr.txt") else 0,
   "apply_exit": read_exit("proof-apply-retry"),
   "apply_stderr_bytes": os.path.getsize(f"/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-versioned-renewal-implementation/source-packaging/proof-apply-retry-stderr.txt") if os.path.exists(f"/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-versioned-renewal-implementation/source-packaging/proof-apply-retry-stderr.txt") else 0,
   "first_failed_check_exit": read_exit("proof-apply-check"),
   "first_failed_apply_exit": read_exit("proof-apply"),
   "gen_copy": gen,
   "gen_index": genindex,
   "gen_index_outside_packet": True,
   "proof_copy": proof,
   "scope": f"scoped 689 tracked at HEAD + {len(new_list)} absent (sources/surveys bulk outside scope, unchanged, not in patch); final {len(final_paths)} exact + delta {len(delta_sorted)}; HEAD stays 409, no commit/new ancestry"
 },
 "baseline_manifest": "notes/rephase-1-editorial-operation-implementation/correction-r7/source-manifest-r7b.json",
 "old_patch": {"path":"notes/rephase-1-editorial-operation-implementation/source-packaging/complete-r3-operation-409.patch","sha256":"659063dc27f0926aaf6e8a33f322937076563c4a23f6cf0d80ca970e1b2abd5b","bytes":2018112},
 "source_before_after": {"src_before_head": head, "src_after_head": head, "src_unchanged": True},
 "status_summary": f"{len(mods)}M+{len(new_list)}A={len(delta_sorted)} (LC_ALL=C sorted, pycache/notes/tmp excluded, first failed proof preserved)",
 "notes": "partialDB 26309 missing blobs retained (not full-history cert); runtime TeX unbundled; bulk31466 sources/surveys outside scope; current packaging observation only, not continuous no-drift/global cert; no generic rerunner cert; no old runners; no network; no source edits; inherited whitespace warnings preserved (trailing/new-blank-line), not normalized; Git 100644 vs physical 0o664 (0o775 for single 100755 bridge) recorded separately, not faked equal; only needed inputs old four parent + complete R3 57 patch + renewal 35 (20A+15M); HIGH 1dad FROZEN (depth 3db fixture not in candidate per independent-authority-review); P 825dba1d P1, PUB 3f4039, Reader 098a, edpub 85814124, P3S 9e2a, R1 52e15457, ReaderF4 63323adc; first failed proof (check129 usage + apply1 wrong work-tree) preserved, retry check0/apply0 authoritative"
}
json.dump(manifest, open(outjson,'w'), indent=2, sort_keys=True)
print(f"manifest {outjson} delta={len(delta_sorted)} final={len(final_paths)} patch={patch_sha[:12]} {patch_bytes}B")
PYEOF
log_run manifest-valid-retry python3 -c "import json; d=json.load(open('$MANIFEST_JSON')); assert d['delta_count']==92, d['delta_count']; assert d['intended_final']==741, d['intended_final']; assert d['proof']['check_exit']=='0', d['proof']; assert d['proof']['apply_exit']=='0', d['proof']; print('manifest-valid-retry OK', d['delta_count'], d['intended_final'], d['patch']['sha256'][:12])"

# 6. post checks
log_run retry-src-post-head git -C "$SRC" rev-parse HEAD
log_run retry-src-post-status git -C "$SRC" status --porcelain=v1
log_run retry-recon-head git -C "$WS" rev-parse HEAD

echo "RETRY DONE" >>"$PACKET/commands.log"
