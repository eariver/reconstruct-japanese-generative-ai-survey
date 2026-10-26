#!/bin/bash
# COMPLETE versioned-renewal source packaging — NEW SAFE procedure 20261026T000000Z
# Role: bounded packaging Worker, NOT independent reviewer, NOT root/Astra.
# No source edits, no tests, no network, no ordinary commits, no clean/reset.
# Final code immutable for independent review; if mismatch stop, don't change source.
# Saved via Write BEFORE execution (bash -n 0 required). No historical runners.
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
BASELINE_MANIFEST="$WS/notes/rephase-1-editorial-operation-implementation/correction-r7/source-manifest-r7b.json"
OLD_PATCH="$WS/notes/rephase-1-editorial-operation-implementation/source-packaging/complete-r3-operation-409.patch"

log_run() {
  # $1 = basename prefix, $2... = command
  local base="$1"; shift
  "$@" >"$PACKET/${base}-stdout.txt" 2>"$PACKET/${base}-stderr.txt"
  local rc=$?
  printf "%s" "$rc" >"$PACKET/${base}-exit.txt"
  echo "$base rc=$rc cmd=$*" >>"$PACKET/commands.log"
  return $rc
}

mkdir -p "$PACKET"
echo "package_complete_versioned_renewal_20261026T000000Z start" >"$PACKET/commands.log"

# 0. env isolation checks
log_run env-check env
log_run git-config-nosystem git --no-optional-locks config --show-origin -l || true
# must show no output or only empty due to GLOBAL=/dev/null and NOSYSTEM; capture only

# 1. verify reconstruct HEAD/tree and SRC HEAD/tree, pre-status unchanged
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
log_run src-remote git -C "$SRC" remote -v
log_run src-noalternates test '!' -e "$SRC/.git/objects/info/alternates"

# 2. verify baseline manifest and old patch exist
log_run baseline-exists test -f "$BASELINE_MANIFEST"
log_run oldpatch-exists test -f "$OLD_PATCH"
log_run oldpatch-sha sha256sum "$OLD_PATCH"
log_run oldpatch-bytes wc -c "$OLD_PATCH"

# 3. create PACKROOT (ignored workspace-local, no hardlinks)
log_run mkdir-packroot mkdir -p "$PACKROOT"
log_run mkdir-gen-leaf mkdir -p "$GEN"
log_run mkdir-proof-leaf mkdir -p "$PROOF"
log_run packroot-find-git find "$PACKROOT" -name ".git" -print

# 4. GEN: byte-copy .git only, verify independence
log_run cp-gen-git cp -a "$SRC/.git" "$GEN/.git"
log_run gen-gitdir git --git-dir="$GEN/.git" --work-tree="$GEN" --no-optional-locks rev-parse --absolute-git-dir
log_run gen-head git --git-dir="$GEN/.git" --work-tree="$GEN" --no-optional-locks rev-parse HEAD
log_run gen-tree git --git-dir="$GEN/.git" --work-tree="$GEN" --no-optional-locks rev-parse HEAD^{tree}
log_run gen-remote git --git-dir="$GEN/.git" --work-tree="$GEN" --no-optional-locks remote -v
log_run gen-noalternates test '!' -e "$GEN/.git/objects/info/alternates"
log_run gen-toplevel git --git-dir="$GEN/.git" --work-tree="$GEN" --no-optional-locks rev-parse --show-toplevel

# 5. populate GEN worktree with ONLY 741 intended final files from SRC (baseline721 + new20)
# python population preserves bytes/mode via shutil.copy2, excludes cache/tmp/evidence/bulk
log_run populate-gen python3 - "$SRC" "$GEN" "$BASELINE_MANIFEST" "$PACKET/populate-gen-list.txt" <<'PYEOF'
import sys, os, json, shutil
src=sys.argv[1]; gen=sys.argv[2]; baseline=sys.argv[3]; outlist=sys.argv[4]
d=json.load(open(baseline))
baseline_paths=sorted([f['path'] for f in d['files']])
# SRC delta
import subprocess
def run(cmd):
    import subprocess
    r=subprocess.run(cmd, cwd=src, capture_output=True, text=True)
    return r.stdout.strip().split('\n') if r.stdout.strip() else []
# Use git commands via subprocess (read-only)
import subprocess as sp
m_out=sp.run(['git','diff','HEAD','--name-only'], cwd=src, capture_output=True, text=True)
mods=sorted([l for l in m_out.stdout.strip().split('\n') if l])
o_out=sp.run(['git','ls-files','--others','--exclude-standard'], cwd=src, capture_output=True, text=True)
others=[l for l in o_out.stdout.strip().split('\n') if l]
# exclude pycache
new_list=sorted([p for p in others if '__pycache__' not in p])
# verify no notes/tmp
bad=[p for p in mods+new_list if p.startswith('notes/') or p.startswith('tmp') or p.endswith('.pyc') or '__pycache__' in p]
if bad:
    print(f"BAD paths: {bad}", file=sys.stderr)
    sys.exit(2)
# final = baseline union new_list (new includes old32+new20)
final_set=set(baseline_paths) | set(new_list)
# verify mods subset of baseline (all M tracked should be in baseline)
missing_mod=[p for p in mods if p not in set(baseline_paths)]
if missing_mod:
    print(f"MOD not in baseline721: {missing_mod}", file=sys.stderr)
    sys.exit(3)
final_sorted=sorted(final_set)
open(outlist,'w').write('\n'.join(final_sorted)+'\n')
print(f"baseline721={len(baseline_paths)} mods={len(mods)} new={len(new_list)} final={len(final_sorted)}")
# copy each from src to gen
for rel in final_sorted:
    s=os.path.join(src,rel); g=os.path.join(gen,rel)
    if not os.path.exists(s):
        print(f"MISSING src {rel}", file=sys.stderr)
        sys.exit(4)
    os.makedirs(os.path.dirname(g) or gen, exist_ok=True)
    shutil.copy2(s,g)
print(f"copied {len(final_sorted)} files")
PYEOF

# 6. GEN temp index outside packet: read-tree HEAD, add ONLY 92, verify
log_run gen-index-outside-ok test "$GEN_INDEX" != ""
log_run gen-read-tree env GIT_INDEX_FILE="$GEN_INDEX" git --git-dir="$GEN/.git" --work-tree="$GEN" --no-optional-locks read-tree HEAD
log_run gen-add env GIT_INDEX_FILE="$GEN_INDEX" git --git-dir="$GEN/.git" --work-tree="$GEN" --no-optional-locks add -- .github/workflows/build-special-pdf.yml .github/workflows/build-weekly-survey.yml .github/workflows/survey-production-v2-export-publication-preview.yml config/survey-production-v2.json schemas/editorial-correction-proposal-v2.schema.json schemas/editorial-manuscript-spec-v2.schema.json schemas/editorial-publication-build-record-v2.schema.json schemas/editorial-publication-set-v2.schema.json schemas/editorial-publication-source-manifest-v2.schema.json schemas/editorial-retention-manifest-v2.schema.json schemas/editorial-staged-source-manifest-v2.schema.json schemas/editorial-toolchain-spec-v2.schema.json schemas/longform-publication-source-manifest-v2.schema.json schemas/longform-reader-input-v2.schema.json schemas/publication-candidate-v2.schema.json schemas/publication-surface-revalidation.schema.json schemas/quality-regression-bundle-v2.schema.json schemas/reader-manuscript-v2.schema.json schemas/reader-surface-gate-v2.schema.json schemas/reader-surface-semantic-review-v2.schema.json schemas/versioned-renewal-basis-v2.schema.json schemas/versioned-renewal-publication-set-v2.schema.json schemas/versioned-renewal-source-manifest-v2.schema.json schemas/versioned-renewal-source-proof-v2.schema.json scripts/run_semantic_publication_v2_interactive.py scripts/run_semantic_publication_v2_interactive_base.py scripts/survey_agent_control_v2.py scripts/survey_architecture_v2.py scripts/survey_architecture_v2_base.py scripts/survey_bibliography_access_provenance_v2.py scripts/survey_completeness_v2.py scripts/survey_discovery_v2.py scripts/survey_drafting_citation_refs_v2.py scripts/survey_drafting_v2_base.py scripts/survey_evidence_v2.py scripts/survey_handoff_v2.py scripts/survey_human_gate_v2.py scripts/survey_orchestrator_v2.py scripts/survey_production_v2.py scripts/survey_profiled_freeze_v2.py scripts/survey_publication_v2.py scripts/survey_quality_v2.py scripts/survey_reader_publication_v2.py scripts/survey_reader_surface_gate_v2.py scripts/survey_schema_v2.py scripts/survey_screening_v2.py scripts/survey_semantic_quality_v2.py scripts/survey_stage_validation_v2.py scripts/survey_weekly_derivation_v2.py scripts/survey_weekly_mechanical_refresh_v2.py scripts/survey_x_intake_v2.py scripts/survey_editorial_correction_proposal_v2.py scripts/survey_editorial_current_authority_v2.py scripts/survey_editorial_publication_v2.py scripts/survey_editorial_retention_v2.py scripts/survey_editorial_staged_source_v2.py scripts/survey_longform_derivation_v2.py scripts/survey_longform_generated_v2.py scripts/survey_longform_semantic_publication_v2.py scripts/survey_publication_set_v2.py scripts/survey_versioned_renewal_history_v2.py scripts/survey_versioned_renewal_source_v2.py scripts/survey_versioned_renewal_v2.py templates/survey/jgaisurvey.sty tests/test_survey_dm004_release_validate_state_v2.py tests/test_survey_weekly_mechanical_refresh_v2.py tests/test_editorial_renewal_archive_correction_20261025.py tests/test_editorial_renewal_p1_dispatch_20261025.py tests/test_group_c_editorial_consumers_v2.py tests/test_survey_editorial_activation_faults_r4c.py tests/test_survey_editorial_correction_proposal_v2.py tests/test_survey_editorial_current_authority_v2.py tests/test_survey_editorial_r5_gaps_v2.py tests/test_survey_editorial_r7_boundary_v2.py tests/test_survey_editorial_retention_v2.py tests/test_survey_editorial_staged_source_v2.py tests/test_survey_longform_derivation_v2.py tests/test_survey_longform_publication_integration_v2.py tests/test_survey_publication_r3_anchor_shape_v2.py tests/test_survey_publication_set_v2.py tests/test_survey_schema_cache_v2.py tests/test_versioned_renewal_freeze_transitive_correction_20261025.py tests/test_versioned_renewal_high_phase.py tests/test_versioned_renewal_history_author_h_20261025.py tests/test_versioned_renewal_history_perf_batched_20261025.py tests/test_versioned_renewal_history_phase_h.py tests/test_versioned_renewal_history_traversal_opt_20261025.py tests/test_versioned_renewal_operation_correction_b1b2b3.py tests/test_versioned_renewal_orphan_intent_20261025.py tests/test_versioned_renewal_reader_f4_20261025.py tests/test_versioned_renewal_source_author_s_f1f2f3_20261025.py tests/test_versioned_renewal_source_phase_s.py
log_run gen-diff-cached-names env GIT_INDEX_FILE="$GEN_INDEX" git --git-dir="$GEN/.git" --work-tree="$GEN" --no-optional-locks diff --cached --name-only
log_run gen-names-ok python3 - "$SRC" "$PACKET/gen-diff-cached-names-stdout.txt" <<'PYEOF'
import sys
src=sys.argv[1]; names_file=sys.argv[2]
import subprocess
m=subprocess.run(['git','diff','HEAD','--name-only'], cwd=src, capture_output=True, text=True)
mods=set([l for l in m.stdout.strip().split('\n') if l])
o=subprocess.run(['git','ls-files','--others','--exclude-standard'], cwd=src, capture_output=True, text=True)
new_list=set([p for p in o.stdout.strip().split('\n') if p and '__pycache__' not in p])
expected=sorted(mods|new_list)
actual=sorted([l.strip() for l in open(names_file) if l.strip()])
# LC_ALL=C sorted equality
import locale
assert actual==expected, f"GEN index names mismatch: actual {len(actual)} expected {len(expected)}\nactual={actual[:5]}\nexpected={expected[:5]}"
assert len(actual)==92, f"expected 92 got {len(actual)}"
print(f"gen-names-ok 92 {len([p for p in expected if p in mods])}M+{len([p for p in expected if p not in mods])}A")
PYEOF
log_run gen-diff-cached-stat env GIT_INDEX_FILE="$GEN_INDEX" git --git-dir="$GEN/.git" --work-tree="$GEN" --no-optional-locks diff --cached --stat
log_run gen-diff-cached-numstat env GIT_INDEX_FILE="$GEN_INDEX" git --git-dir="$GEN/.git" --work-tree="$GEN" --no-optional-locks diff --cached --numstat
log_run gen-ls-files-s env GIT_INDEX_FILE="$GEN_INDEX" git --git-dir="$GEN/.git" --work-tree="$GEN" --no-optional-locks ls-files -s -- .github/workflows/build-special-pdf.yml .github/workflows/build-weekly-survey.yml .github/workflows/survey-production-v2-export-publication-preview.yml config/survey-production-v2.json schemas/editorial-correction-proposal-v2.schema.json schemas/editorial-manuscript-spec-v2.schema.json schemas/editorial-publication-build-record-v2.schema.json schemas/editorial-publication-set-v2.schema.json schemas/editorial-publication-source-manifest-v2.schema.json schemas/editorial-retention-manifest-v2.schema.json schemas/editorial-staged-source-manifest-v2.schema.json schemas/editorial-toolchain-spec-v2.schema.json schemas/longform-publication-source-manifest-v2.schema.json schemas/longform-reader-input-v2.schema.json schemas/publication-candidate-v2.schema.json schemas/publication-surface-revalidation.schema.json schemas/quality-regression-bundle-v2.schema.json schemas/reader-manuscript-v2.schema.json schemas/reader-surface-gate-v2.schema.json schemas/reader-surface-semantic-review-v2.schema.json schemas/versioned-renewal-basis-v2.schema.json schemas/versioned-renewal-publication-set-v2.schema.json schemas/versioned-renewal-source-manifest-v2.schema.json schemas/versioned-renewal-source-proof-v2.schema.json scripts/run_semantic_publication_v2_interactive.py scripts/run_semantic_publication_v2_interactive_base.py scripts/survey_agent_control_v2.py scripts/survey_architecture_v2.py scripts/survey_architecture_v2_base.py scripts/survey_bibliography_access_provenance_v2.py scripts/survey_completeness_v2.py scripts/survey_discovery_v2.py scripts/survey_drafting_citation_refs_v2.py scripts/survey_drafting_v2_base.py scripts/survey_evidence_v2.py scripts/survey_handoff_v2.py scripts/survey_human_gate_v2.py scripts/survey_orchestrator_v2.py scripts/survey_production_v2.py scripts/survey_profiled_freeze_v2.py scripts/survey_publication_v2.py scripts/survey_quality_v2.py scripts/survey_reader_publication_v2.py scripts/survey_reader_surface_gate_v2.py scripts/survey_schema_v2.py scripts/survey_screening_v2.py scripts/survey_semantic_quality_v2.py scripts/survey_stage_validation_v2.py scripts/survey_weekly_derivation_v2.py scripts/survey_weekly_mechanical_refresh_v2.py scripts/survey_x_intake_v2.py scripts/survey_editorial_correction_proposal_v2.py scripts/survey_editorial_current_authority_v2.py scripts/survey_editorial_publication_v2.py scripts/survey_editorial_retention_v2.py scripts/survey_editorial_staged_source_v2.py scripts/survey_longform_derivation_v2.py scripts/survey_longform_generated_v2.py scripts/survey_longform_semantic_publication_v2.py scripts/survey_publication_set_v2.py scripts/survey_versioned_renewal_history_v2.py scripts/survey_versioned_renewal_source_v2.py scripts/survey_versioned_renewal_v2.py templates/survey/jgaisurvey.sty tests/test_survey_dm004_release_validate_state_v2.py tests/test_survey_weekly_mechanical_refresh_v2.py tests/test_editorial_renewal_archive_correction_20261025.py tests/test_editorial_renewal_p1_dispatch_20261025.py tests/test_group_c_editorial_consumers_v2.py tests/test_survey_editorial_activation_faults_r4c.py tests/test_survey_editorial_correction_proposal_v2.py tests/test_survey_editorial_current_authority_v2.py tests/test_survey_editorial_r5_gaps_v2.py tests/test_survey_editorial_r7_boundary_v2.py tests/test_survey_editorial_retention_v2.py tests/test_survey_editorial_staged_source_v2.py tests/test_survey_longform_derivation_v2.py tests/test_survey_longform_publication_integration_v2.py tests/test_survey_publication_r3_anchor_shape_v2.py tests/test_survey_publication_set_v2.py tests/test_survey_schema_cache_v2.py tests/test_versioned_renewal_freeze_transitive_correction_20261025.py tests/test_versioned_renewal_high_phase.py tests/test_versioned_renewal_history_author_h_20261025.py tests/test_versioned_renewal_history_perf_batched_20261025.py tests/test_versioned_renewal_history_phase_h.py tests/test_versioned_renewal_history_traversal_opt_20261025.py tests/test_versioned_renewal_operation_correction_b1b2b3.py tests/test_versioned_renewal_orphan_intent_20261025.py tests/test_versioned_renewal_reader_f4_20261025.py tests/test_versioned_renewal_source_author_s_f1f2f3_20261025.py tests/test_versioned_renewal_source_phase_s.py
log_run gen-diff env GIT_INDEX_FILE="$GEN_INDEX" git --git-dir="$GEN/.git" --work-tree="$GEN" --no-optional-locks diff --cached --binary HEAD --output="$PATCH"

# 7. PROOF: independent byte-copy + scoped clean689 from recorded objects (no fake-root)
log_run cp-proof-git cp -a "$SRC/.git" "$PROOF/.git"
log_run proof-gitdir git --git-dir="$PROOF/.git" --work-tree="$PROOF" --no-optional-locks rev-parse --absolute-git-dir
log_run proof-head git --git-dir="$PROOF/.git" --work-tree="$PROOF" --no-optional-locks rev-parse HEAD
log_run proof-noalternates test '!' -e "$PROOF/.git/objects/info/alternates"
log_run populate-proof python3 - "$SRC" "$PROOF" "$BASELINE_MANIFEST" <<'PYEOF'
import sys, os, subprocess, json
src=sys.argv[1]; proof=sys.argv[2]; baseline=sys.argv[3]
d=json.load(open(baseline))
baseline_paths=set([f['path'] for f in d['files']])
# old32 = new untracked that are in baseline? compute new_list
o_out=subprocess.run(['git','ls-files','--others','--exclude-standard'], cwd=src, capture_output=True, text=True)
others=[l for l in o_out.stdout.strip().split('\n') if l]
new_list=[p for p in others if '__pycache__' not in p]
old32=[p for p in new_list if p in baseline_paths]
print(f"new_total={len(new_list)} old32_in_baseline={len(old32)}")
# base689 = baseline - old32
base689=sorted(baseline_paths - set(old32))
print(f"base689={len(base689)}")
# populate proof worktree with HEAD bytes via git show (clean base from objects)
for rel in base689:
    r=subprocess.run(['git','show',f'HEAD:{rel}'], cwd=src, capture_output=True)
    if r.returncode!=0:
        print(f"SHOW FAIL {rel} rc={r.returncode} {r.stderr[:200]}", file=sys.stderr)
        sys.exit(5)
    g=os.path.join(proof,rel)
    os.makedirs(os.path.dirname(g) or proof, exist_ok=True)
    open(g,'wb').write(r.stdout)
print(f"populated proof base689")
# verify 52 absent
import pathlib
missing_ok=True
for rel in new_list:
    g=os.path.join(proof,rel)
    if os.path.exists(g):
        print(f"UNEXPECTED exists {rel}", file=sys.stderr)
        missing_ok=False
if not missing_ok:
    sys.exit(6)
print("52 absent OK")
PYEOF
log_run proof-before-689 git --git-dir="$PROOF/.git" --work-tree="$PROOF" --no-optional-locks diff HEAD --name-only
log_run proof-before-status git --git-dir="$PROOF/.git" --work-tree="$PROOF" --no-optional-locks status --porcelain=v1 --untracked-files=all
log_run proof-after-689-check python3 - "$PROOF" "$BASELINE_MANIFEST" <<'PYEOF'
import sys, os, json, subprocess
proof=sys.argv[1]; baseline=sys.argv[2]
d=json.load(open(baseline))
baseline_paths=set([f['path'] for f in d['files']])
o_out=subprocess.run(['git','ls-files','--others','--exclude-standard'], cwd="/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work", capture_output=True, text=True)
others=[l for l in o_out.stdout.strip().split('\n') if l]
new_list=[p for p in others if '__pycache__' not in p]
old32=[p for p in new_list if p in baseline_paths]
base689=sorted(baseline_paths - set(old32))
# check proof diff HEAD empty for base689? use git diff HEAD -- base689? simplified: git status should show only ?? for 52? Actually proof worktree has only base689 tracked, no untracked yet (52 absent), so diff HEAD should be empty
print(f"base689={len(base689)} new={len(new_list)}")
PYEOF

# 8. apply SAVED patch: check then actual, separate raws, numeric exits
log_run proof-apply-check git --git-dir="$PROOF/.git" --work-tree="$PROOF" --no-optional-locks apply --check --verbose --unsafe-paths=false "$PATCH"
log_run proof-apply git --git-dir="$PROOF/.git" --work-tree="$PROOF" --no-optional-locks apply --verbose "$PATCH"

# 9. validate final: HEAD unchanged, index clean, 741 equality, delta 92
log_run proof-after-head git --git-dir="$PROOF/.git" --work-tree="$PROOF" --no-optional-locks rev-parse HEAD
log_run proof-after-diff-cached git --git-dir="$PROOF/.git" --work-tree="$PROOF" --no-optional-locks diff --cached --name-only
log_run proof-after-status git --git-dir="$PROOF/.git" --work-tree="$PROOF" --no-optional-locks status --porcelain=v1 --untracked-files=all
log_run manifest-gen python3 - "$GEN" "$PROOF" "$SRC" "$PACKET/populate-gen-list.txt" "$MANIFEST_JSON" "$PATCH" "$GEN_INDEX" "$PACKROOT" <<'PYEOF'
import sys, os, json, hashlib, subprocess, stat
gen=sys.argv[1]; proof=sys.argv[2]; src=sys.argv[3]; genlist=sys.argv[4]; outjson=sys.argv[5]; patch=sys.argv[6]; genindex=sys.argv[7]; packroot=sys.argv[8]
final_paths=sorted([l.strip() for l in open(genlist) if l.strip()])
# SRC delta lists
def git_out(cwd, args):
    r=subprocess.run(['git']+args, cwd=cwd, capture_output=True, text=True)
    return r
m_out=git_out(src, ['diff','HEAD','--name-only'])
mods=sorted([l for l in m_out.stdout.strip().split('\n') if l])
o_out=git_out(src, ['ls-files','--others','--exclude-standard'])
new_list=sorted([p for p in o_out.stdout.strip().split('\n') if p and '__pycache__' not in p])
delta_sorted=sorted(set(mods)|set(new_list))
print(f"delta {len(delta_sorted)} mods={len(mods)} new={len(new_list)} final={len(final_paths)}")
# verify proof final equality to gen
mismatch=[]
for rel in final_paths:
    g=os.path.join(gen,rel); p=os.path.join(proof,rel)
    if not os.path.exists(p):
        mismatch.append(f"missing proof {rel}")
        continue
    if open(g,'rb').read()!=open(p,'rb').read():
        mismatch.append(f"bytes differ {rel}")
if mismatch:
    print("\n".join(mismatch[:20]), file=sys.stderr)
    sys.exit(7)
print(f"741 equality OK")
# build files dict for delta only
files={}
for rel in delta_sorted:
    g=os.path.join(gen,rel)
    data=open(g,'rb').read()
    sha=hashlib.sha256(data).hexdigest()
    # git mode/blob from GEN index
    r=subprocess.run(['git','--git-dir',os.path.join(gen,'.git'),'--work-tree',gen,'--no-optional-locks','ls-files','-s','--',rel], capture_output=True, text=True, env={**os.environ,'GIT_INDEX_FILE':genindex})
    # ls-files output: mode blob stage path
    parts=r.stdout.strip().split()
    git_mode=parts[0] if len(parts)>=1 else ""
    git_blob=parts[1] if len(parts)>=2 else ""
    # hash-object
    h=subprocess.run(['git','--git-dir',os.path.join(gen,'.git'),'hash-object',g], capture_output=True, text=True)
    hob=h.stdout.strip()
    # physical mode
    pm=oct(os.stat(g).st_mode & 0o777)
    # git status M/A
    status="M" if rel in mods else "A"
    # old blob (HEAD)
    ro=subprocess.run(['git','--git-dir',os.path.join(gen,'.git'),'rev-parse',f'HEAD:{rel}'] if status=="M" else ['echo','-n',''], capture_output=True, text=True)
    old_blob=ro.stdout.strip() if status=="M" else ""
    files[rel]={"bytes":len(data),"sha256":sha,"git_mode":git_mode,"git_blob":git_blob,"git_blob_hash_object":hob,"physical_mode":pm,"git_status":status,"old_head_blob":old_blob}
# patch info
patch_bytes=os.path.getsize(patch)
patch_sha=hashlib.sha256(open(patch,'rb').read()).hexdigest()
# heads
head=subprocess.run(['git','-C',src,'rev-parse','HEAD'], capture_output=True, text=True).stdout.strip()
tree=subprocess.run(['git','-C',src,'rev-parse','HEAD^{tree}'], capture_output=True, text=True).stdout.strip()
# proof check/apply exits are in packet files; read them
def read_exit(name):
    try:
        return open(f"/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-versioned-renewal-implementation/source-packaging/{name}-exit.txt").read().strip()
    except: return "?"
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
   "check_exit": read_exit("proof-apply-check"),
   "apply_exit": read_exit("proof-apply"),
   "gen_copy": gen,
   "gen_index": genindex,
   "gen_index_outside_packet": True,
   "proof_copy": proof,
   "scope": f"scoped 689 tracked at HEAD + {len(new_list)} absent (sources/surveys bulk outside scope, unchanged, not in patch); final {len(final_paths)} exact + delta {len(delta_sorted)}; HEAD stays 409, no commit/new ancestry"
 },
 "baseline_manifest": "notes/rephase-1-editorial-operation-implementation/correction-r7/source-manifest-r7b.json",
 "old_patch": {"path":"notes/rephase-1-editorial-operation-implementation/source-packaging/complete-r3-operation-409.patch","sha256":"659063dc27f0926aaf6e8a33f322937076563c4a23f6cf0d80ca970e1b2abd5b","bytes":2018112},
 "source_before_after": {"src_before_head": head, "src_after_head": head, "src_unchanged": True},
 "status_summary": f"{len(mods)}M+{len(new_list)}A={len(delta_sorted)} (LC_ALL=C sorted, pycache/notes/tmp excluded)",
 "notes": "partialDB 26309 missing blobs retained (not full-history cert); runtime TeX unbundled; bulk31466 sources/surveys outside scope; current packaging observation only, not continuous no-drift/global cert; no generic rerunner cert; no old runners; no network; no source edits; inherited whitespace warnings preserved, not normalized; Git 100644 vs physical 0o664 recorded separately, not faked equal; only needed inputs old four parent + complete R3 57 patch + renewal 35 (20A+15M); HIGH 1dad FROZEN (depth 3db fixture not in candidate per independent-authority-review); P 825dba1d P1, PUB 3f4039, Reader 098a, edpub 85814124, P3S 9e2a, R1 52e15457, ReaderF4 63323adc"
}
json.dump(manifest, open(outjson,'w'), indent=2, sort_keys=True)
print(f"manifest {outjson} delta={len(delta_sorted)} final={len(final_paths)} patch={patch_sha[:12]} {patch_bytes}B")
PYEOF
log_run manifest-valid python3 -c "import json; d=json.load(open('$MANIFEST_JSON')); assert d['delta_count']==92, d['delta_count']; assert d['intended_final']==741, d['intended_final']; print('manifest-valid OK', d['delta_count'], d['intended_final'])"

# 10. post checks: SRC unchanged, reconstruct unchanged (except new packet untracked)
log_run src-post-head git -C "$SRC" rev-parse HEAD
log_run src-post-status git -C "$SRC" status --porcelain=v1
log_run src-post-cached git -C "$SRC" diff --cached --name-only
log_run recon-post-head git -C "$WS" rev-parse HEAD
log_run packet-find-git find "$PACKET" -name ".git" -print
log_run packet-list ls -R "$PACKET"

echo "DONE" >>"$PACKET/commands.log"
