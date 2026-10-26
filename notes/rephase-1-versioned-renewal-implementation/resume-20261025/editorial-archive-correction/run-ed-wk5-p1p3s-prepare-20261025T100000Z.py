#!/usr/bin/env python3
"""WEEKLY wk-ed-renew-5: NEW editorial on U5 r7 G6 — P1/P2R/P2V/P3S63 + specs + prepare (real build).
Tests OWN fix renewal authoring_refs vs editorial authored_refs for WEEKLY. 1200s per phase.
"""
import subprocess, sys, pathlib, os
from datetime import datetime, timezone
REPO = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-editorial-archive-weekly-20261025T100000Z/renewal-weekly"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/editorial-archive-correction/run-ed-wk5-p1p3s-prepare-20261025T100000Z"
EVID.mkdir(parents=True, exist_ok=True)
TMP = REPO / ".rephase-1-editorial-runtime/versioned-renewal-editorial-archive-weekly-20261025T100000Z/tmp"
TMP.mkdir(parents=True, exist_ok=True)
os.environ["TMPDIR"]=str(TMP)
for k in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
    assert not os.environ.get(k)
ENV=dict(os.environ); ENV["PYTHONDONTWRITEBYTECODE"]="1"; ENV["LC_ALL"]="C"
TIMEOUT=1200
def run_tag(tag, cmd, timeout=TIMEOUT):
    import subprocess as sp
    try:
        proc=sp.run(cmd, cwd=str(REPO), capture_output=True, text=True, timeout=timeout, env=ENV)
    except sp.TimeoutExpired:
        (EVID/f"{tag}-stdout.txt").write_text("", encoding="utf-8")
        (EVID/f"{tag}-stderr.txt").write_text(f"TIMEOUT {timeout}s", encoding="utf-8")
        (EVID/f"{tag}-exit.txt").write_text("TIMEOUT", encoding="utf-8")
        print(f"{tag}: TIMEOUT", flush=True)
        return None
    (EVID/f"{tag}-stdout.txt").write_text(proc.stdout or "",encoding="utf-8")
    (EVID/f"{tag}-stderr.txt").write_text(proc.stderr or "",encoding="utf-8")
    (EVID/f"{tag}-exit.txt").write_text(str(proc.returncode),encoding="utf-8")
    with open(EVID/"commands.log","a",encoding="utf-8") as fh:
        fh.write(f"$ ... tag={tag} -> exit={proc.returncode}\n")
    print(f"{tag}: exit={proc.returncode}",flush=True)
    return proc
def py_inline(code, argv, tag, timeout=TIMEOUT):
    return run_tag(tag, [sys.executable,"-c",code]+argv, timeout=timeout)
def main():
    (EVID/"commands.log").write_text(f"WK-ED-5 start {datetime.now(timezone.utc).isoformat()} PID={os.getpid()}\n",encoding="utf-8")
    run_tag("ed-pre-head", ["git","-C",str(FIX),"rev-parse","HEAD"])
    issue="2026-W37"; prop_old="wk-boot-1"; prop_new="wk-ed-renew-5"
    pdir_old=f"sources/{issue}/publication/v2/editorial-corrections/{prop_old}"
    pdir_new=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}"
    state_rel=f"sources/{issue}/production-state.json"
    # stage authoring (Weekly envelope, 3 paras + required synthesis)
    stage_code = r"""
import sys, json, pathlib
sys.path.insert(0, sys.argv[1])
root=pathlib.Path(sys.argv[1]); prop_new=sys.argv[2]
pdir_old=f"sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1"
pdir_new=f"sources/2026-W37/publication/v2/editorial-corrections/{prop_new}"
old_auth=json.loads((root/pdir_old/"authoring-input.json").read_bytes())
new_auth=json.loads(json.dumps(old_auth))
new_auth["cover"]["headline"]="Weekly tested method, revised edition G6 + renewal editorial (changed-reader)"
new_auth["cover"]["deck"]="Source-based survey with G6 renewal-editorial amendment; synthetic fixture, no genuine approval."
new_auth["final_summary"]["paragraphs"]=["The edition surveys one source with G6 renewal-editorial changed reader.",
 "The claims remain attributed; renewal proof fresh, tool epoch G6.",
 "The accepted source authors describe the tested method."]
assert json.dumps(new_auth,sort_keys=True)!=json.dumps(old_auth,sort_keys=True)
dest=root/pdir_new/"authoring-input.json"
dest.parent.mkdir(parents=True, exist_ok=True)
from scripts import survey_production_v2 as core
if dest.exists():
    assert dest.read_bytes()==core.json_bytes(new_auth), "different bytes need new ID"
    print(f"reuse {dest.relative_to(root)}")
else:
    dest.write_bytes(core.json_bytes(new_auth))
    print(f"staged {dest.relative_to(root)}")
"""
    sa=py_inline(stage_code, [str(FIX), prop_new], "ed-stage-auth")
    assert sa is not None and sa.returncode==0, open(EVID/"ed-stage-auth-stderr.txt").read()[:8000]
    p1_code = r"""
import sys, json, faulthandler, os
sys.path.insert(0, sys.argv[1])
root_arg=sys.argv[1]; prop_new=sys.argv[2]
faulthandler.dump_traceback_later(1100, exit=False)
from pathlib import Path
root_p=Path(root_arg)
from scripts import survey_editorial_correction_proposal_v2 as p1mod
print(f"P1 child PID={os.getpid()}", flush=True)
issue="2026-W37"
pdir_new=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}"
dest=root_p/pdir_new/"authoring-input.json"
res=p1mod.prepare_proposal(root_p, root_p/f"sources/{issue}/production-state.json", dest, prop_new, "Renewal-to-editorial G6: changed reader on U5-active prior (Weekly envelope, synthetic)")
print(f"P1 PREPARED keys={sorted(res.keys())}", flush=True)
"""
    p1=py_inline(p1_code, [str(FIX), prop_new], "ed-p1-prepare", timeout=1200)
    assert p1 is not None and p1.returncode==0, open(EVID/"ed-p1-prepare-stderr.txt").read()[:12000]
    stage2_code = r"""
import sys, json, pathlib
sys.path.insert(0, sys.argv[1])
root_arg=sys.argv[1]; prop_new=sys.argv[2]
from pathlib import Path
root_p=Path(root_arg)
from scripts import survey_production_v2 as core
from scripts import survey_editorial_correction_proposal_v2 as p1mod
import os
print(f"P1-stage child PID={os.getpid()}", flush=True)
issue="2026-W37"
pdir_new=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}"
dest=root_p/pdir_new/"authoring-input.json"
res=p1mod.prepare_proposal(root_p, root_p/f"sources/{issue}/production-state.json", dest, prop_new, "Renewal-to-editorial G6 stage")
proposal_dir=root_p/pdir_new
reader_file=proposal_dir/"reader-surface-input-v2.json"
proposal_file=proposal_dir/"proposal.json"
if not reader_file.exists():
    reader_file.write_bytes(res["proposed_canonical"])
    print(f"staged reader", flush=True)
else:
    assert reader_file.read_bytes()==res["proposed_canonical"]
if not proposal_file.exists():
    core.write_json(proposal_file, res["proposal"])
    print(f"staged proposal", flush=True)
else:
    print(f"proposal exists", flush=True)
"""
    st=py_inline(stage2_code, [str(FIX), prop_new], "ed-p1-stage", timeout=1200)
    assert st is not None and st.returncode==0, open(EVID/"ed-p1-stage-stderr.txt").read()[:8000]
    p2r_code = r"""
import sys
sys.path.insert(0, sys.argv[1])
root_arg=sys.argv[1]; prop_new=sys.argv[2]
from pathlib import Path
root_p=Path(root_arg)
from scripts import survey_editorial_retention_v2 as p2r
import os
print(f"P2R child PID={os.getpid()}", flush=True)
issue="2026-W37"
proposal=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/proposal.json"
res=p2r.capture_retention(str(root_p), f"sources/{issue}/production-state.json", proposal)
print(f"P2R {res.get('manifest_path')}", flush=True)
v=p2r.verify_retention(str(root_p), proposal, res.get('manifest_path'))
print(f"P2R verify OK", flush=True)
"""
    p2r=py_inline(p2r_code, [str(FIX), prop_new], "ed-p2r-full", timeout=1200)
    assert p2r is not None and p2r.returncode==0, open(EVID/"ed-p2r-full-stderr.txt").read()[:8000]
    p2v_code = r"""
import sys
sys.path.insert(0, sys.argv[1])
root_arg=sys.argv[1]; prop_new=sys.argv[2]
from pathlib import Path
root_p=Path(root_arg)
from scripts import survey_editorial_current_authority_v2 as p2v
import os
print(f"P2V child PID={os.getpid()}", flush=True)
issue="2026-W37"
proposal=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/proposal.json"
cands=list((root_p/f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/retained").rglob("*retention-manifest.json"))
ret=str(cands[0].relative_to(root_p))
res=p2v.observe_current_authority(str(root_p), f"sources/{issue}/production-state.json", proposal, ret)
print(f"P2V {sorted(res.keys())}", flush=True)
"""
    p2v=py_inline(p2v_code, [str(FIX), prop_new], "ed-p2v-full", timeout=1200)
    assert p2v is not None and p2v.returncode==0, open(EVID/"ed-p2v-full-stderr.txt").read()[:8000]
    scope_code = r"""
import sys, json, pathlib
sys.path.insert(0, sys.argv[1])
root_arg=sys.argv[1]; prop_new=sys.argv[2]
from pathlib import Path
root_p=Path(root_arg)
from scripts import survey_production_v2 as core
import os
print(f"scope child PID={os.getpid()}", flush=True)
issue="2026-W37"
pdir_new=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}"
proposal=json.loads((root_p/pdir_new/"proposal.json").read_bytes())
staged_reader_rel=proposal["proposed"]["proposed_reader_ref"]["path"]
after_sha=proposal["proposed"]["proposed_reader_canonical_sha256"]
block={"version":"EDITORIAL_CORRECTION_SCOPE_V1","decision":"WITHIN_APPROVED_AUTHORITY","before_reader_input":proposal["basis"]["active_reader_input_ref"],"preserved_upstream_sha256":proposal["basis"]["preserved_upstream_digest"],"change_summary":"Synthetic Weekly scope judgment inside approved authority (G6 archive-correction, no genuine approval).","evidence_locations":["synthetic-fixture:proposal"]}
review={"schema_version":"2.0-rc1","issue_id":proposal["issue_id"],"publication_profile":proposal["publication_profile"],"review_kind":"SEMANTIC_EDITORIAL","reviewed_surface":{"path":staged_reader_rel,"sha256":after_sha},"checks":[{"check_id":"READER_PIPELINE_INDEPENDENCE","status":"PASS","detail":"Synthetic scope reviewer judged proposed reader independently understandable.","evidence_locations":["synthetic-fixture:proposed-reader"]},{"check_id":"EDITORIAL_CORRECTION_SCOPE","status":"PASS","detail":"Synthetic scope reviewer judged delta inside approved Architecture authority.","evidence_locations":["synthetic-fixture:proposal"]}],"decision":"PASS","reviewed_by":"synthetic Weekly scope reviewer (G6)","reviewed_at":"2026-10-25T12:00:00+00:00","recorded_at":"2026-10-25T12:00:00+00:00","status":"PASSED","findings":[],"summary":"Synthetic scope PASS for G6 archive-correction.","editorial_correction_scope":block}
review["review_sha256"]=core.sha256_object(review)
scope_path=root_p/pdir_new/"scope-review-v2.json"
if not scope_path.exists():
    core.write_json(scope_path, review)
    print(f"scope {scope_path.relative_to(root_p)}", flush=True)
else:
    print(f"scope exists", flush=True)
"""
    sc=py_inline(scope_code, [str(FIX), prop_new], "ed-scope", timeout=1200)
    assert sc is not None and sc.returncode==0, open(EVID/"ed-scope-stderr.txt").read()[:8000]
    p3s_code = r"""
import sys
sys.path.insert(0, sys.argv[1])
root_arg=sys.argv[1]; prop_new=sys.argv[2]
from pathlib import Path
root_p=Path(root_arg)
import importlib
for m in ["scripts.render_article_draft_tex","scripts.survey_agent_control_v2","scripts.survey_agent_tool_v2","scripts.survey_architecture_v2","scripts.survey_architecture_v2_base","scripts.survey_bibliography_access_provenance_v2","scripts.survey_completeness_v2","scripts.survey_discovery_v2","scripts.survey_drafting_citation_refs_v2","scripts.survey_drafting_v2","scripts.survey_drafting_v2_base","scripts.survey_x_intake_v2","scripts.survey_editorial_correction_proposal_v2","scripts.survey_editorial_current_authority_v2","scripts.survey_editorial_publication_v2","scripts.survey_editorial_retention_v2","scripts.survey_evidence_v2","scripts.survey_longform_derivation_v2","scripts.survey_longform_generated_v2","scripts.survey_production_v2","scripts.survey_publication_set_v2","scripts.survey_publication_v2","scripts.survey_quality_v2","scripts.survey_reader_fidelity_v2","scripts.survey_reader_publication_v2","scripts.survey_reader_surface_gate_v2","scripts.survey_review_attention_v2","scripts.survey_schema_v2","scripts.survey_screening_v2","scripts.survey_versioned_renewal_history_v2","scripts.survey_versioned_renewal_source_v2","scripts.survey_versioned_renewal_v2","scripts.survey_weekly_derivation_v2","scripts.validate_article_draft","scripts.weekly_pipeline"]:
    importlib.import_module(m)
from scripts import survey_editorial_staged_source_v2 as p3s
import os
print(f"P3S child PID={os.getpid()}", flush=True)
issue="2026-W37"
proposal=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/proposal.json"
ret=list((root_p/f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/retained").rglob("*retention-manifest.json"))
manifest=str(ret[0].relative_to(root_p))
scope=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/scope-review-v2.json"
try:
    res=p3s.materialize_staged_source(str(root_p), f"sources/{issue}/production-state.json", proposal, manifest, scope)
    staged_ref=res.get('staged_manifest_ref',{}).get('path') if isinstance(res,dict) else None
    print(f"P3S staged={staged_ref}", flush=True)
    v=p3s.verify_staged_source(str(root_p), proposal, staged_ref)
    print(f"P3S verify OK", flush=True)
except Exception as e:
    import traceback
    msg=str(e)
    print(f"P3S materialize issue: {msg[:500]}", flush=True)
    if "STAGED_ROOT_EXISTS" in msg:
        staged=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/staged-source/staged-source-manifest.json"
        v=p3s.verify_staged_source(str(root_p), proposal, staged)
        print(f"P3S verify existing OK", flush=True)
    else:
        raise
"""
    p3s=py_inline(p3s_code, [str(FIX), prop_new], "ed-p3s", timeout=1200)
    assert p3s is not None and p3s.returncode==0, open(EVID/"ed-p3s-stderr.txt").read()[:12000]
    spec_code = r"""
import sys, json, pathlib, hashlib, datetime
sys.path.insert(0, sys.argv[1])
root_arg=sys.argv[1]; prop_new=sys.argv[2]
from pathlib import Path
root_p=Path(root_arg)
from scripts import survey_production_v2 as core
import os
print(f"spec child PID={os.getpid()}", flush=True)
issue="2026-W37"; prop_old="wk-boot-1"
pdir_new=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}"
old_spec=json.loads((root_p/f"sources/{issue}/publication/v2/editorial-corrections/{prop_old}/manuscript-spec.json").read_bytes())
new_sha=hashlib.sha256((root_p/pdir_new/"proposal.json").read_bytes()).hexdigest()
new_spec=dict(old_spec)
new_spec["proposal_ref"]={"path":f"{pdir_new}/proposal.json","sha256":new_sha}
new_spec["authored_by"]="weekly G6 editorial author wk-ed-renew-5"
new_spec["recorded_at"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
mspec_path=root_p/pdir_new/"manuscript-spec.json"
if not mspec_path.exists():
    mspec_path.write_bytes(core.json_bytes(new_spec))
    print(f"staged manuscript-spec", flush=True)
old_tool=json.loads((root_p/f"sources/{issue}/publication/v2/editorial-corrections/{prop_old}/toolchain-spec.json").read_bytes())
new_tool=dict(old_tool)
new_tool["executor"]="weekly-g6-wk-ed-renew-5"
new_tool["recorded_at"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
tool_path=root_p/pdir_new/"toolchain-spec.json"
if not tool_path.exists():
    tool_path.write_bytes(core.json_bytes(new_tool))
    print(f"staged toolchain-spec", flush=True)
"""
    sp=py_inline(spec_code, [str(FIX), prop_new], "ed-specs", timeout=1200)
    assert sp is not None and sp.returncode==0, open(EVID/"ed-specs-stderr.txt").read()[:8000]
    prep_code = r"""
import sys
sys.path.insert(0, sys.argv[1])
root_arg=sys.argv[1]; prop_new=sys.argv[2]
from pathlib import Path
root_p=Path(root_arg)
from scripts import survey_editorial_publication_v2 as edpub
import os
print(f"prepare child PID={os.getpid()}", flush=True)
issue="2026-W37"
proposal=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/proposal.json"
ret=list((root_p/f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/retained").rglob("*retention-manifest.json"))
ret_manifest=str(ret[0].relative_to(root_p))
staged=list((root_p/f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/staged-source").rglob("*staged-source-manifest.json"))
staged_manifest=str(staged[0].relative_to(root_p)) if staged else None
mspec=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/manuscript-spec.json"
tspec=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/toolchain-spec.json"
print(f"proposal={proposal} staged={staged_manifest}", flush=True)
res=edpub.prepare_publication(str(root_p), f"sources/{issue}/production-state.json", proposal, staged_manifest, mspec, tspec)
print(f"prepare OK {sorted(res.keys()) if isinstance(res,dict) else type(res)}", flush=True)
"""
    pr=py_inline(prep_code, [str(FIX), prop_new], "ed-prepare-pub", timeout=1200)
    assert pr is not None and pr.returncode==0, f"prepare_pub failed (OWN fix WEEKLY) {open(EVID/'ed-prepare-pub-stderr.txt').read()[:15000]}"
    print("PREPARE PUB DONE WEEKLY (OWN fix PASS)", flush=True)
    return 0
if __name__=="__main__":
    raise SystemExit(main())
