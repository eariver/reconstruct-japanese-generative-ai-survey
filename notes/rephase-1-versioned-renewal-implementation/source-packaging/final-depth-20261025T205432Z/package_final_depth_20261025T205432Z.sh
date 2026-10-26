#!/bin/bash
# FINAL-depth COMPLETE versioned-renewal source packaging — 20261025T205432Z UTC
# Delivery fix: HIGH 3dbdedb8 (tested 32/33, +27/0 guard only) + new depth test ea264638.
# ONLY 2 changed vs first 92/741: HIGH bytes 1dad->3db + new test file. All other H742/S229/etc same.
# First 92 d6c72fb...3415062B COMPLETED but OBSOLETE, preserved untouched (no overwrite).
# This FINAL expects 93 files 40M53A / 742 source (689+53), scoped 689+53.
# Role: bounded packaging Worker, NOT reviewer/root. No edits/tests/build/network/commit/clean.
# Saved via Write BEFORE execution (bash -n 0). No saved-runner reuse. No --unsafe-paths bypass (all paths closed manifest).
# Uses independent GEN/tempindex only, do NOT stage candidate/reconstruct.
set -u
export PYTHONDONTWRITEBYTECODE=1
export GIT_NO_LAZY_FETCH=1
export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL=/dev/null
export GIT_OPTIONAL_LOCKS=0
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_PREFIX 2>/dev/null || true

WS="/home/eariver/git/reconstruct-japanese-generative-ai-survey"
SRC="$WS/.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work"
STAMP="20261025T205432Z"
PACKROOT="$WS/.rephase-1-editorial-runtime/versioned-renewal-packaging-final-depth-${STAMP}"
GEN="$PACKROOT/gen-copy/candidate-partial-b40de60"
PROOF="$PACKROOT/proof-copy/candidate-partial-b40de60"
GEN_INDEX="$PACKROOT/gen-index"
PACKET="$WS/notes/rephase-1-versioned-renewal-implementation/source-packaging/final-depth-${STAMP}"
PATCH="$PACKET/complete-versioned-renewal-409.patch"
MANIFEST_JSON="$PACKET/complete-versioned-renewal-manifest.json"
BASELINE_MANIFEST="$WS/notes/rephase-1-editorial-operation-implementation/correction-r7/source-manifest-r7b.json"
OLD_PATCH="$WS/notes/rephase-1-editorial-operation-implementation/source-packaging/complete-r3-operation-409.patch"
FIRST_PATCH="$WS/notes/rephase-1-versioned-renewal-implementation/source-packaging/complete-versioned-renewal-409.patch"
DELIVERY_MD="$WS/notes/rephase-1-versioned-renewal-implementation/resume-20261025/depth-prewrite-correction/delivery-correction.md"

log_run() {
  local base="$1"; shift
  "$@" >"$PACKET/${base}-stdout.txt" 2>"$PACKET/${base}-stderr.txt"
  local rc=$?
  printf "%s" "$rc" >"$PACKET/${base}-exit.txt"
  echo "$base rc=$rc cmd=$*" >>"$PACKET/commands.log"
  return $rc
}

mkdir -p "$PACKET"
echo "package_final_depth_${STAMP} start (FINAL, first 92 preserved)" >"$PACKET/commands.log"

log_run env-check env
log_run recon-head git -C "$WS" rev-parse HEAD
log_run recon-status git -C "$WS" status --porcelain=v1
log_run recon-gitdir git -C "$WS" rev-parse --absolute-git-dir
log_run src-head git -C "$SRC" rev-parse HEAD
log_run src-tree git -C "$SRC" rev-parse HEAD^{tree}
log_run src-status git -C "$SRC" status --porcelain=v1
log_run src-status-all git -C "$SRC" status --porcelain=v1 --untracked-files=all
log_run src-diff-names git -C "$SRC" diff HEAD --name-only
log_run src-others git -C "$SRC" ls-files --others --exclude-standard
log_run src-cached-empty git -C "$SRC" diff --cached --name-only
log_run src-gitdir git -C "$SRC" rev-parse --absolute-git-dir
log_run src-noalternates test '!' -e "$SRC/.git/objects/info/alternates"
log_run delivery-md-exists test -f "$DELIVERY_MD"
log_run baseline-exists test -f "$BASELINE_MANIFEST"
log_run oldpatch-exists test -f "$OLD_PATCH"
log_run firstpatch-preserved test -f "$FIRST_PATCH"
log_run firstpatch-sha sha256sum "$FIRST_PATCH"

# verify final frozen pins: HIGH 3db, new test ea2646, H742 S229 unchanged, only 2 changed vs first
log_run final-pins python3 - "$SRC" "$FIRST_PATCH" <<'PYEOF'
import sys, hashlib, os, json
src=sys.argv[1]
def sha(rel):
    return hashlib.sha256(open(os.path.join(src,rel),'rb').read()).hexdigest()
assert sha('scripts/survey_versioned_renewal_v2.py')=='3dbdedb8b44b366b129cc351b25a8bb898a62ad23e424d27e46c3df85a6a6d0b', "HIGH not 3db"
assert sha('tests/test_survey_versioned_renewal_depth_prewrite_v2.py')=='ea2646381a41139a950deb1b6f60e6e27649beedee5ac3c4b5169c46fc63fdb8', "depth test not ea2646"
assert sha('scripts/survey_versioned_renewal_history_v2.py').startswith('74275d22'), "H changed"
assert sha('scripts/survey_versioned_renewal_source_v2.py').startswith('2290ddd0'), "S changed"
# only 2 changed vs first manifest
old=json.load(open('/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-versioned-renewal-implementation/source-packaging/complete-versioned-renewal-manifest.json'))
files=old['files']
diffs=[rel for rel,meta in files.items() if hashlib.sha256(open(os.path.join(src,rel),'rb').read()).hexdigest()!=meta['sha256']]
print(f"old92 diffs vs current: {diffs}")
assert diffs==['scripts/survey_versioned_renewal_v2.py'], f"expected only HIGH changed, got {diffs}"
print("final pins OK: HIGH 3db, depth ea2646, H742 S229 same, only HIGH changed +1 new")
PYEOF

log_run mkdir-packroot mkdir -p "$PACKROOT"
log_run mkdir-gen-leaf mkdir -p "$GEN"
log_run mkdir-proof-leaf mkdir -p "$PROOF"

log_run cp-gen-git cp -a "$SRC/.git" "$GEN/.git"
log_run gen-gitdir git --git-dir="$GEN/.git" --work-tree="$GEN" --no-optional-locks rev-parse --absolute-git-dir
log_run gen-head git --git-dir="$GEN/.git" --work-tree="$GEN" --no-optional-locks rev-parse HEAD
log_run gen-tree git --git-dir="$GEN/.git" --work-tree="$GEN" --no-optional-locks rev-parse HEAD^{tree}
log_run gen-noalternates test '!' -e "$GEN/.git/objects/info/alternates"

log_run populate-gen python3 - "$SRC" "$GEN" "$BASELINE_MANIFEST" "$PACKET/populate-gen-list.txt" <<'PYEOF'
import sys, os, json, shutil, subprocess
src=sys.argv[1]; gen=sys.argv[2]; baseline=sys.argv[3]; outlist=sys.argv[4]
d=json.load(open(baseline))
baseline_paths=sorted([f['path'] for f in d['files']])
m_out=subprocess.run(['git','diff','HEAD','--name-only'], cwd=src, capture_output=True, text=True)
mods=sorted([l for l in m_out.stdout.strip().split('\n') if l])
o_out=subprocess.run(['git','ls-files','--others','--exclude-standard'], cwd=src, capture_output=True, text=True)
others=[l for l in o_out.stdout.strip().split('\n') if l]
new_list=sorted([p for p in others if '__pycache__' not in p])
bad=[p for p in mods+new_list if p.startswith('notes/') or p.startswith('tmp') or p.endswith('.pyc') or '__pycache__' in p]
if bad:
    print(f"BAD {bad}", file=sys.stderr); sys.exit(2)
final_set=set(baseline_paths)|set(new_list)
missing_mod=[p for p in mods if p not in set(baseline_paths)]
if missing_mod:
    print(f"MOD not in baseline {missing_mod}", file=sys.stderr); sys.exit(3)
# expect 40M53A93/742
assert len(mods)==40, f"mods {len(mods)}"
assert len(new_list)==53, f"new {len(new_list)}"
assert len(final_set)==742, f"final {len(final_set)}"
final_sorted=sorted(final_set)
open(outlist,'w').write('\n'.join(final_sorted)+'\n')
print(f"baseline721={len(baseline_paths)} mods={len(mods)} new={len(new_list)} final={len(final_sorted)}")
for rel in final_sorted:
    s=os.path.join(src,rel); g=os.path.join(gen,rel)
    if not os.path.exists(s):
        print(f"MISSING {rel}", file=sys.stderr); sys.exit(4)
    os.makedirs(os.path.dirname(g) or gen, exist_ok=True)
    shutil.copy2(s,g)
print(f"copied {len(final_sorted)}")
PYEOF

log_run gen-index-outside-ok test "$GEN_INDEX" != ""
log_run gen-read-tree env GIT_INDEX_FILE="$GEN_INDEX" git --git-dir="$GEN/.git" --work-tree="$GEN" --no-optional-locks read-tree HEAD
log_run gen-add env GIT_INDEX_FILE="$GEN_INDEX" git --git-dir="$GEN/.git" --work-tree="$GEN" --no-optional-locks add -- .github/workflows/build-special-pdf.yml .github/workflows/build-weekly-survey.yml .github/workflows/survey-production-v2-export-publication-preview.yml config/survey-production-v2.json schemas/editorial-correction-proposal-v2.schema.json schemas/editorial-manuscript-spec-v2.schema.json schemas/editorial-publication-build-record-v2.schema.json schemas/editorial-publication-set-v2.schema.json schemas/editorial-publication-source-manifest-v2.schema.json schemas/editorial-retention-manifest-v2.schema.json schemas/editorial-staged-source-manifest-v2.schema.json schemas/editorial-toolchain-spec-v2.schema.json schemas/longform-publication-source-manifest-v2.schema.json schemas/longform-reader-input-v2.schema.json schemas/publication-candidate-v2.schema.json schemas/publication-surface-revalidation.schema.json schemas/quality-regression-bundle-v2.schema.json schemas/reader-manuscript-v2.schema.json schemas/reader-surface-gate-v2.schema.json schemas/reader-surface-semantic-review-v2.schema.json schemas/versioned-renewal-basis-v2.schema.json schemas/versioned-renewal-publication-set-v2.schema.json schemas/versioned-renewal-source-manifest-v2.schema.json schemas/versioned-renewal-source-proof-v2.schema.json scripts/run_semantic_publication_v2_interactive.py scripts/run_semantic_publication_v2_interactive_base.py scripts/survey_agent_control_v2.py scripts/survey_architecture_v2.py scripts/survey_architecture_v2_base.py scripts/survey_bibliography_access_provenance_v2.py scripts/survey_completeness_v2.py scripts/survey_discovery_v2.py scripts/survey_drafting_citation_refs_v2.py scripts/survey_drafting_v2_base.py scripts/survey_evidence_v2.py scripts/survey_handoff_v2.py scripts/survey_human_gate_v2.py scripts/survey_orchestrator_v2.py scripts/survey_production_v2.py scripts/survey_profiled_freeze_v2.py scripts/survey_publication_v2.py scripts/survey_quality_v2.py scripts/survey_reader_publication_v2.py scripts/survey_reader_surface_gate_v2.py scripts/survey_schema_v2.py scripts/survey_screening_v2.py scripts/survey_semantic_quality_v2.py scripts/survey_stage_validation_v2.py scripts/survey_weekly_derivation_v2.py scripts/survey_weekly_mechanical_refresh_v2.py scripts/survey_x_intake_v2.py scripts/survey_editorial_correction_proposal_v2.py scripts/survey_editorial_current_authority_v2.py scripts/survey_editorial_publication_v2.py scripts/survey_editorial_retention_v2.py scripts/survey_editorial_staged_source_v2.py scripts/survey_longform_derivation_v2.py scripts/survey_longform_generated_v2.py scripts/survey_longform_semantic_publication_v2.py scripts/survey_publication_set_v2.py scripts/survey_versioned_renewal_history_v2.py scripts/survey_versioned_renewal_source_v2.py scripts/survey_versioned_renewal_v2.py templates/survey/jgaisurvey.sty tests/test_survey_dm004_release_validate_state_v2.py tests/test_survey_weekly_mechanical_refresh_v2.py tests/test_editorial_renewal_archive_correction_20261025.py tests/test_editorial_renewal_p1_dispatch_20261025.py tests/test_group_c_editorial_consumers_v2.py tests/test_survey_editorial_activation_faults_r4c.py tests/test_survey_editorial_correction_proposal_v2.py tests/test_survey_editorial_current_authority_v2.py tests/test_survey_editorial_r5_gaps_v2.py tests/test_survey_editorial_r7_boundary_v2.py tests/test_survey_editorial_retention_v2.py tests/test_survey_editorial_staged_source_v2.py tests/test_survey_longform_derivation_v2.py tests/test_survey_longform_publication_integration_v2.py tests/test_survey_publication_r3_anchor_shape_v2.py tests/test_survey_publication_set_v2.py tests/test_survey_schema_cache_v2.py tests/test_survey_versioned_renewal_depth_prewrite_v2.py tests/test_versioned_renewal_freeze_transitive_correction_20261025.py tests/test_versioned_renewal_high_phase.py tests/test_versioned_renewal_history_author_h_20261025.py tests/test_versioned_renewal_history_perf_batched_20261025.py tests/test_versioned_renewal_history_phase_h.py tests/test_versioned_renewal_history_traversal_opt_20261025.py tests/test_versioned_renewal_operation_correction_b1b2b3.py tests/test_versioned_renewal_orphan_intent_20261025.py tests/test_versioned_renewal_reader_f4_20261025.py tests/test_versioned_renewal_source_author_s_f1f2f3_20261025.py tests/test_versioned_renewal_source_phase_s.py
log_run gen-diff-cached-names env GIT_INDEX_FILE="$GEN_INDEX" git --git-dir="$GEN/.git" --work-tree="$GEN" --no-optional-locks diff --cached --name-only
log_run gen-names-ok python3 - "$SRC" "$PACKET/gen-diff-cached-names-stdout.txt" <<'PYEOF'
import sys, subprocess
src=sys.argv[1]; f=sys.argv[2]
m=subprocess.run(['git','diff','HEAD','--name-only'], cwd=src, capture_output=True, text=True)
mods=set([l for l in m.stdout.strip().split('\n') if l])
o=subprocess.run(['git','ls-files','--others','--exclude-standard'], cwd=src, capture_output=True, text=True)
new_list=set([p for p in o.stdout.strip().split('\n') if p and '__pycache__' not in p])
expected=sorted(mods|new_list)
actual=sorted([l.strip() for l in open(f) if l.strip()])
assert actual==expected, f"mismatch actual {len(actual)} expected {len(expected)}"
assert len(actual)==93, f"expected 93 got {len(actual)}"
print(f"gen-names-ok 93 {len([p for p in expected if p in mods])}M+{len([p for p in expected if p not in mods])}A")
PYEOF
log_run gen-diff-cached-stat env GIT_INDEX_FILE="$GEN_INDEX" git --git-dir="$GEN/.git" --work-tree="$GEN" --no-optional-locks diff --cached --stat
log_run gen-diff-cached-numstat env GIT_INDEX_FILE="$GEN_INDEX" git --git-dir="$GEN/.git" --work-tree="$GEN" --no-optional-locks diff --cached --numstat
log_run gen-ls-files-s bash -c 'GIT_INDEX_FILE="$0" git --git-dir="$1/.git" --work-tree="$1" --no-optional-locks ls-files -s $(cat "$2")' "$GEN_INDEX" "$GEN" "$PACKET/gen-diff-cached-names-stdout.txt"
log_run gen-ls-files-s-full env GIT_INDEX_FILE="$GEN_INDEX" git --git-dir="$GEN/.git" --work-tree="$GEN" --no-optional-locks ls-files -s
log_run gen-diff env GIT_INDEX_FILE="$GEN_INDEX" git --git-dir="$GEN/.git" --work-tree="$GEN" --no-optional-locks diff --cached --binary HEAD --output="$PATCH"

log_run cp-proof-git cp -a "$SRC/.git" "$PROOF/.git"
log_run proof-gitdir git --git-dir="$PROOF/.git" --work-tree="$PROOF" --no-optional-locks rev-parse --absolute-git-dir
log_run proof-head git --git-dir="$PROOF/.git" --work-tree="$PROOF" --no-optional-locks rev-parse HEAD
log_run proof-noalternates test '!' -e "$PROOF/.git/objects/info/alternates"
log_run populate-proof python3 - "$SRC" "$PROOF" "$BASELINE_MANIFEST" <<'PYEOF'
import sys, os, subprocess, json
src=sys.argv[1]; proof=sys.argv[2]; baseline=sys.argv[3]
d=json.load(open(baseline))
baseline_paths=set([f['path'] for f in d['files']])
o_out=subprocess.run(['git','ls-files','--others','--exclude-standard'], cwd=src, capture_output=True, text=True)
others=[l for l in o_out.stdout.strip().split('\n') if l]
new_list=[p for p in others if '__pycache__' not in p]
old32=[p for p in new_list if p in baseline_paths]
print(f"new_total={len(new_list)} old32_in_baseline={len(old32)}")
base689=sorted(baseline_paths - set(old32))
print(f"base689={len(base689)}")
assert len(base689)==689, f"base689 {len(base689)}"
assert len(new_list)==53, f"new {len(new_list)}"
for rel in base689:
    r=subprocess.run(['git','show',f'HEAD:{rel}'], cwd=src, capture_output=True)
    if r.returncode!=0:
        print(f"SHOW FAIL {rel}", file=sys.stderr); sys.exit(5)
    g=os.path.join(proof,rel)
    os.makedirs(os.path.dirname(g) or proof, exist_ok=True)
    open(g,'wb').write(r.stdout)
    # preserve executable bit from HEAD mode
    mode=subprocess.run(['git','ls-tree','HEAD','--',rel], cwd=src, capture_output=True, text=True).stdout
    if mode.startswith('100755'):
        os.chmod(g, 0o775)
    else:
        os.chmod(g, 0o664)
print("populated proof base689")
for rel in new_list:
    g=os.path.join(proof,rel)
    if os.path.exists(g):
        print(f"UNEXPECTED exists {rel}", file=sys.stderr); sys.exit(6)
print("53 absent OK")
PYEOF
log_run proof-before-status git -C "$PROOF" status --porcelain=v1 --untracked-files=all
log_run proof-before-diff-names git -C "$PROOF" diff HEAD --name-only

# CORRECT apply: git -C PROOF (not --git-dir/--work-tree with relative paths), no --unsafe-paths flag
log_run proof-apply-check git -C "$PROOF" apply --check --verbose "$PATCH"
log_run proof-apply git -C "$PROOF" apply --verbose "$PATCH"

log_run proof-after-head git -C "$PROOF" rev-parse HEAD
log_run proof-after-diff-cached git -C "$PROOF" diff --cached --name-only
log_run proof-after-status git -C "$PROOF" status --porcelain=v1 --untracked-files=all

log_run manifest-gen python3 - "$GEN" "$PROOF" "$SRC" "$PACKET/populate-gen-list.txt" "$MANIFEST_JSON" "$PATCH" "$GEN_INDEX" "$PACKROOT" "$STAMP" <<'PYEOF'
import sys, os, json, hashlib, subprocess
gen=sys.argv[1]; proof=sys.argv[2]; src=sys.argv[3]; genlist=sys.argv[4]; outjson=sys.argv[5]; patch=sys.argv[6]; genindex=sys.argv[7]; packroot=sys.argv[8]; stamp=sys.argv[9]
final_paths=sorted([l.strip() for l in open(genlist) if l.strip()])
def git_out(cwd, args):
    import subprocess
    return subprocess.run(['git']+args, cwd=cwd, capture_output=True, text=True)
m_out=git_out(src, ['diff','HEAD','--name-only'])
mods=sorted([l for l in m_out.stdout.strip().split('\n') if l])
o_out=git_out(src, ['ls-files','--others','--exclude-standard'])
new_list=sorted([p for p in o_out.stdout.strip().split('\n') if p and '__pycache__' not in p])
delta_sorted=sorted(set(mods)|set(new_list))
print(f"delta {len(delta_sorted)} mods={len(mods)} new={len(new_list)} final={len(final_paths)}")
assert len(delta_sorted)==93 and len(mods)==40 and len(new_list)==53 and len(final_paths)==742
mismatch=[]
for rel in final_paths:
    g=os.path.join(gen,rel); p=os.path.join(proof,rel)
    if not os.path.exists(p):
        mismatch.append(f"missing proof {rel}"); continue
    if open(g,'rb').read()!=open(p,'rb').read():
        mismatch.append(f"bytes differ {rel}")
if mismatch:
    print("\n".join(mismatch[:30]), file=sys.stderr); sys.exit(7)
print("742 equality OK")
files={}
for rel in delta_sorted:
    g=os.path.join(gen,rel)
    data=open(g,'rb').read()
    sha=hashlib.sha256(data).hexdigest()
    r=subprocess.run(['git','-C',gen,'ls-files','-s','--',rel], capture_output=True, text=True, env={**os.environ,'GIT_INDEX_FILE':genindex})
    parts=r.stdout.strip().split()
    git_mode=parts[0] if len(parts)>=1 else ""
    git_blob=parts[1] if len(parts)>=2 else ""
    hob=subprocess.run(['git','-C',gen,'hash-object',g], capture_output=True, text=True).stdout.strip()
    pm=oct(os.stat(g).st_mode & 0o777)
    status="M" if rel in mods else "A"
    old_blob=subprocess.run(['git','-C',src,'rev-parse',f'HEAD:{rel}'], capture_output=True, text=True).stdout.strip() if status=="M" else ""
    files[rel]={"bytes":len(data),"sha256":sha,"git_mode":git_mode,"git_blob":git_blob,"git_blob_hash_object":hob,"physical_mode":pm,"git_status":status,"old_head_blob":old_blob}
patch_bytes=os.path.getsize(patch)
patch_sha=hashlib.sha256(open(patch,'rb').read()).hexdigest()
head=subprocess.run(['git','-C',src,'rev-parse','HEAD'], capture_output=True, text=True).stdout.strip()
tree=subprocess.run(['git','-C',src,'rev-parse','HEAD^{tree}'], capture_output=True, text=True).stdout.strip()
def read_exit(n):
    try: return open(f"/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-versioned-renewal-implementation/source-packaging/final-depth-{stamp}/"+n+"-exit.txt").read().strip()
    except: return "?"
manifest={
 "candidate_src": src,
 "stamp": stamp,
 "head": head,
 "head_tree": tree,
 "delta_count": len(delta_sorted),
 "tracked_modified": len(mods),
 "untracked_new": len(new_list),
 "intended_final": len(final_paths),
 "intended_final_verified": True,
 "files": files,
 "patch": {"path": f"final-depth-{stamp}/complete-versioned-renewal-409.patch","bytes": patch_bytes,"sha256": patch_sha},
 "proof": {
   "check_exit": read_exit("proof-apply-check"),
   "check_stderr_bytes": os.path.getsize(f"/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-versioned-renewal-implementation/source-packaging/final-depth-{stamp}/proof-apply-check-stderr.txt"),
   "apply_exit": read_exit("proof-apply"),
   "apply_stderr_bytes": os.path.getsize(f"/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-versioned-renewal-implementation/source-packaging/final-depth-{stamp}/proof-apply-stderr.txt"),
   "gen_copy": gen, "gen_index": genindex, "gen_index_outside_packet": True, "proof_copy": proof,
   "scope": f"scoped 689 tracked at HEAD + {len(new_list)} absent (bulk31466 outside, unchanged); final {len(final_paths)} exact + delta {len(delta_sorted)}; HEAD stays 409"
 },
 "baseline_manifest": "notes/rephase-1-editorial-operation-implementation/correction-r7/source-manifest-r7b.json",
 "old_patch": {"path":"notes/rephase-1-editorial-operation-implementation/source-packaging/complete-r3-operation-409.patch","sha256":"659063dc27f0926aaf6e8a33f322937076563c4a23f6cf0d80ca970e1b2abd5b","bytes":2018112},
 "first_obsolete_patch": {"path":"notes/rephase-1-versioned-renewal-implementation/source-packaging/complete-versioned-renewal-409.patch","sha256":"d6c72fb4557775691086e4b1cb804b1283b7e2864043281acd27110381771647","bytes":3415062,"delta":92,"final":741,"note":"OBSOLETE delivery (HIGH 1dad, missing depth test), preserved untouched"},
 "delivery_correction": "notes/rephase-1-versioned-renewal-implementation/resume-20261025/depth-prewrite-correction/delivery-correction.md (HIGH 1dad->3db +27/0, new test ea2646, only 2 changed)",
 "source_before_after": {"src_before_head": head, "src_after_head": head, "src_unchanged": True},
 "status_summary": f"{len(mods)}M+{len(new_list)}A={len(delta_sorted)} (LC_ALL=C, pycache/notes/tmp excluded)",
 "notes": "partialDB26309 retained; runtimeTeX unbundled; bulk31466 outside; current packaging only, no drift/global cert; no rerunner; no network; no edits; whitespace preserved, not normalized; Git100644 vs physical0o664 (0o775 single bridge outside delta) separate; HIGH 3dbdedb8 FINAL (tested32/33 byte-identical), H74275d22 S2290ddd0 same, P825dba1d PUB3f4039 Reader098a edpub85814124 P3S9e2a R152e15457 ReaderF4 63323adc depth ea2646"
}
json.dump(manifest, open(outjson,'w'), indent=2, sort_keys=True)
print(f"manifest {outjson} delta={len(delta_sorted)} final={len(final_paths)} patch={patch_sha[:12]} {patch_bytes}B")
PYEOF
log_run manifest-valid python3 -c "import json; d=json.load(open('$MANIFEST_JSON')); assert d['delta_count']==93; assert d['intended_final']==742; assert d['proof']['check_exit']=='0'; assert d['proof']['apply_exit']=='0'; print('manifest-valid OK', d['delta_count'], d['intended_final'], d['patch']['sha256'][:12])"

log_run src-post-head git -C "$SRC" rev-parse HEAD
log_run src-post-status git -C "$SRC" status --porcelain=v1
log_run recon-post-head git -C "$WS" rev-parse HEAD
log_run packet-find-git find "$PACKET" -name ".git" -print
log_run packet-list ls -R "$PACKET"

echo "DONE FINAL ${STAMP}" >>"$PACKET/commands.log"
