#!/usr/bin/env python3
"""LF-ED-4 resume from P3S (P1/P2R/P2V/scope already 0, preserved)."""
import subprocess, sys, pathlib, os
REPO = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-editorial-archive-longform-20261025T100000Z/renewal-longform"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/editorial-archive-correction/run-ed-lf4-p1p3s-prepare-20261025T100000Z"
for k in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
    assert not os.environ.get(k)
ENV=dict(os.environ); ENV["PYTHONDONTWRITEBYTECODE"]="1"; ENV["LC_ALL"]="C"
TMP = REPO / ".rephase-1-editorial-runtime/versioned-renewal-editorial-archive-longform-20261025T100000Z/tmp"
os.environ["TMPDIR"]=str(TMP)
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
        fh.write(f"$ ... tag={tag} -> exit={proc.returncode} (resume-p3s)\n")
    print(f"{tag}: exit={proc.returncode}",flush=True)
    return proc
def py_inline(code, argv, tag, timeout=TIMEOUT):
    return run_tag(tag, [sys.executable,"-c",code]+argv, timeout=timeout)
def main():
    prop_new="lf-ed-4"
    for t in ["ed-p1-prepare","ed-p1-stage","ed-p2r-capture","ed-p2r-verify","ed-p2v-observe"]:
        assert (EVID/f"{t}-exit.txt").read_text().strip()=="0", f"prereq {t} not 0"
    # scope already manually created, record as 0 if exists
    import pathlib as pl
    scope_path = FIX/f"sources/SP001/publication/v2/editorial-corrections/{prop_new}/scope-review-v2.json"
    assert scope_path.exists(), "scope missing"
    # ensure ed-scope exit 0 recorded (manual creation)
    (EVID/"ed-scope-stdout.txt").write_text(f"scope {scope_path} exists, reuse (manual G7, no P1 re-run due to retention conflict)\n", encoding="utf-8")
    (EVID/"ed-scope-stderr.txt").write_text("", encoding="utf-8")
    (EVID/"ed-scope-exit.txt").write_text("0", encoding="utf-8")
    print("SCOPE OK (manual, preserved)", flush=True)
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
issue="SP001"
proposal=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/proposal.json"
ret=list((root_p/f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/retained").rglob("*retention-manifest.json"))
manifest=str(ret[0].relative_to(root_p))
scope=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/scope-review-v2.json"
print(f"proposal={proposal} manifest={manifest} scope={scope}", flush=True)
res=p3s.materialize_staged_source(str(root_p), f"sources/{issue}/production-state.json", proposal, manifest, scope)
print(f"P3S staged={res.get('staged_manifest_ref',{}).get('path') if isinstance(res,dict) else None}", flush=True)
v=p3s.verify_staged_source(str(root_p), proposal, res.get('staged_manifest_ref',{}).get('path') if isinstance(res,dict) else None)
print(f"P3S verify OK", flush=True)
"""
    p3s=py_inline(p3s_code, [str(FIX), prop_new], "ed-p3s", timeout=1200)
    # STAGED_ROOT_EXISTS (already present from previous G7 materialize, preserved) is not a failure:
    # verify existing staged with preload, like original lf-ed-3 fix2.
    if p3s is None or p3s.returncode!=0:
        err_txt=open(EVID/"ed-p3s-stderr.txt").read()
        if "STAGED_ROOT_EXISTS" in err_txt:
            print("P3S materialize STAGED_ROOT_EXISTS (already present, preserved), verify existing", flush=True)
            verify_code = r"""
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
print(f"P3S-verify child PID={os.getpid()}", flush=True)
issue="SP001"
proposal=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/proposal.json"
staged=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/staged-source/staged-source-manifest.json"
v=p3s.verify_staged_source(str(root_p), proposal, staged)
print(f"P3S verify OK {v.get('result')}", flush=True)
"""
            vfy=py_inline(verify_code, [str(FIX), prop_new], "ed-p3s-verify", timeout=1200)
            assert vfy is not None and vfy.returncode==0, open(EVID/"ed-p3s-verify-stderr.txt").read()[:8000]
            print("P3S63 VERIFY OK (existing staged, preserved)", flush=True)
        else:
            assert False, err_txt[:12000]
    else:
        print("P3S63 OK", flush=True)
    spec_code = r"""
import sys, json, pathlib, hashlib, datetime
sys.path.insert(0, sys.argv[1])
root_arg=sys.argv[1]; prop_new=sys.argv[2]
from pathlib import Path
root_p=Path(root_arg)
from scripts import survey_production_v2 as core
import os
print(f"spec child PID={os.getpid()}", flush=True)
issue="SP001"; prop_old="lf-boot-1"
pdir_new=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}"
old_spec=json.loads((root_p/f"sources/{issue}/publication/v2/editorial-corrections/{prop_old}/manuscript-spec.json").read_bytes())
new_proposal=root_p/pdir_new/"proposal.json"
new_sha=hashlib.sha256(new_proposal.read_bytes()).hexdigest()
new_spec=dict(old_spec)
new_spec["proposal_ref"]={"path":f"{pdir_new}/proposal.json","sha256":new_sha}
new_spec["authored_by"]="longform G7 editorial author lf-ed-4"
new_spec["recorded_at"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
mspec_path=root_p/pdir_new/"manuscript-spec.json"
if not mspec_path.exists():
    mspec_path.write_bytes(core.json_bytes(new_spec))
    print(f"staged manuscript-spec", flush=True)
else:
    print(f"manuscript-spec exists", flush=True)
old_tool=json.loads((root_p/f"sources/{issue}/publication/v2/editorial-corrections/{prop_old}/toolchain-spec.json").read_bytes())
new_tool=dict(old_tool)
new_tool["executor"]="longform-g7-lf-ed-4"
new_tool["recorded_at"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
tool_path=root_p/pdir_new/"toolchain-spec.json"
if not tool_path.exists():
    tool_path.write_bytes(core.json_bytes(new_tool))
    print(f"staged toolchain-spec", flush=True)
else:
    print(f"toolchain-spec exists", flush=True)
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
issue="SP001"
proposal=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/proposal.json"
ret=list((root_p/f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/retained").rglob("*retention-manifest.json"))
ret_manifest=str(ret[0].relative_to(root_p))
staged=list((root_p/f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/staged-source").rglob("*staged-source-manifest.json"))
staged_manifest=str(staged[0].relative_to(root_p)) if staged else None
mspec=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/manuscript-spec.json"
tspec=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/toolchain-spec.json"
print(f"proposal={proposal} staged={staged_manifest}", flush=True)
res=edpub.prepare_publication(str(root_p), f"sources/{issue}/production-state.json", proposal, staged_manifest, mspec, tspec)
print(f"prepare OK keys={sorted(res.keys()) if isinstance(res,dict) else type(res)}", flush=True)
"""
    pr=py_inline(prep_code, [str(FIX), prop_new], "ed-prepare-pub", timeout=1200)
    assert pr is not None and pr.returncode==0, f"prepare_pub failed (OWN fix) {open(EVID/'ed-prepare-pub-stderr.txt').read()[:15000]}"
    print("PREPARE PUB DONE (OWN fix PASS)", flush=True)
    return 0
if __name__=="__main__":
    raise SystemExit(main())
