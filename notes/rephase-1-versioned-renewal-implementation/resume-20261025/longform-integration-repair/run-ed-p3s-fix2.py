#!/usr/bin/env python3
"""P3S verify fix (correct key)."""
import subprocess, sys, pathlib
REPO = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-longform-repair-20261025T090000Z/renewal-longform"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-integration-repair/run-ed-20261025T090000Z"
ENV=dict(__import__("os").environ); ENV["PYTHONDONTWRITEBYTECODE"]="1"; ENV["LC_ALL"]="C"
def run_tag(tag, cmd):
    import subprocess as sp
    proc=sp.run(cmd, cwd=str(REPO), capture_output=True, text=True, timeout=1200, env=ENV)
    (EVID/f"{tag}-stdout.txt").write_text(proc.stdout or "",encoding="utf-8")
    (EVID/f"{tag}-stderr.txt").write_text(proc.stderr or "",encoding="utf-8")
    (EVID/f"{tag}-exit.txt").write_text(str(proc.returncode),encoding="utf-8")
    with open(EVID/"commands.log","a",encoding="utf-8") as fh:
        fh.write(f"$ ... tag={tag} -> exit={proc.returncode}\n")
    print(f"{tag}: exit={proc.returncode}",flush=True)
    return proc
code = r"""
import sys
sys.path.insert(0, sys.argv[1])
root_arg=sys.argv[1]; prop_new=sys.argv[2]
from pathlib import Path
root_p=Path(root_arg)
import importlib
for m in ["scripts.render_article_draft_tex","scripts.survey_agent_control_v2","scripts.survey_agent_tool_v2","scripts.survey_architecture_v2","scripts.survey_architecture_v2_base","scripts.survey_bibliography_access_provenance_v2","scripts.survey_completeness_v2","scripts.survey_discovery_v2","scripts.survey_drafting_citation_refs_v2","scripts.survey_drafting_v2","scripts.survey_drafting_v2_base","scripts.survey_x_intake_v2","scripts.survey_editorial_correction_proposal_v2","scripts.survey_editorial_current_authority_v2","scripts.survey_editorial_publication_v2","scripts.survey_editorial_retention_v2","scripts.survey_evidence_v2","scripts.survey_longform_derivation_v2","scripts.survey_longform_generated_v2","scripts.survey_production_v2","scripts.survey_publication_set_v2","scripts.survey_publication_v2","scripts.survey_quality_v2","scripts.survey_reader_fidelity_v2","scripts.survey_reader_publication_v2","scripts.survey_reader_surface_gate_v2","scripts.survey_review_attention_v2","scripts.survey_schema_v2","scripts.survey_screening_v2","scripts.survey_versioned_renewal_history_v2","scripts.survey_versioned_renewal_source_v2","scripts.survey_versioned_renewal_v2","scripts.survey_weekly_derivation_v2","scripts.validate_article_draft","scripts.weekly_pipeline"]:
    importlib.import_module(m)
from scripts import survey_editorial_staged_source_v2 as p3s
import os, json
print(f"P3S fix child PID={os.getpid()}", flush=True)
issue="SP001"
proposal=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/proposal.json"
import glob as _g
ret=list((root_p/f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/retained").rglob("*retention-manifest.json"))
manifest=str(ret[0].relative_to(root_p))
scope=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/scope-review-v2.json"
print(f"proposal={proposal} manifest={manifest} scope={scope}", flush=True)
res=p3s.materialize_staged_source(str(root_p), f"sources/{issue}/production-state.json", proposal, manifest, scope)
print(f"res keys={sorted(res.keys())}", flush=True)
staged_ref=res.get("staged_manifest_ref",{}).get("path")
print(f"staged={staged_ref}", flush=True)
v=p3s.verify_staged_source(str(root_p), proposal, staged_ref)
print(f"verify OK {v.get('result') if isinstance(v,dict) else 'ok'}", flush=True)
# 63 check
print(f"code_deps len={len(res.get('code_deps',[]))}", flush=True)
assert len(res.get('code_deps',[]))==63, f"expected 63, got {len(res.get('code_deps',[]))}"
print("P3S63 OK", flush=True)
"""
p = run_tag("ed-p3s-fix2", [sys.executable,"-c",code, str(FIX), "lf-ed-3"])
assert p.returncode==0, open(EVID/"ed-p3s-fix2-stderr.txt").read()[:12000]
print("P3S FIX DONE", flush=True)
