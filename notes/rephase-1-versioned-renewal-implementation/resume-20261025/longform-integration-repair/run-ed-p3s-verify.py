#!/usr/bin/env python3
"""Verify existing P3S63 staged for lf-ed-3."""
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
    print(f"{tag}: exit={proc.returncode}",flush=True)
    return proc
code=r"""
import sys
sys.path.insert(0, sys.argv[1])
from pathlib import Path
root_p=Path(sys.argv[1])
import importlib
for m in ["scripts.render_article_draft_tex","scripts.survey_agent_control_v2","scripts.survey_agent_tool_v2","scripts.survey_architecture_v2","scripts.survey_architecture_v2_base","scripts.survey_bibliography_access_provenance_v2","scripts.survey_completeness_v2","scripts.survey_discovery_v2","scripts.survey_drafting_citation_refs_v2","scripts.survey_drafting_v2","scripts.survey_drafting_v2_base","scripts.survey_x_intake_v2","scripts.survey_editorial_correction_proposal_v2","scripts.survey_editorial_current_authority_v2","scripts.survey_editorial_publication_v2","scripts.survey_editorial_retention_v2","scripts.survey_evidence_v2","scripts.survey_longform_derivation_v2","scripts.survey_longform_generated_v2","scripts.survey_production_v2","scripts.survey_publication_set_v2","scripts.survey_publication_v2","scripts.survey_quality_v2","scripts.survey_reader_fidelity_v2","scripts.survey_reader_publication_v2","scripts.survey_reader_surface_gate_v2","scripts.survey_review_attention_v2","scripts.survey_schema_v2","scripts.survey_screening_v2","scripts.survey_versioned_renewal_history_v2","scripts.survey_versioned_renewal_source_v2","scripts.survey_versioned_renewal_v2","scripts.survey_weekly_derivation_v2","scripts.validate_article_draft","scripts.weekly_pipeline"]:
    importlib.import_module(m)
from scripts import survey_editorial_staged_source_v2 as p3s
import os
print(f"verify child PID={os.getpid()}", flush=True)
issue="SP001"; prop_new="lf-ed-3"
proposal=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/proposal.json"
staged=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/staged-source/staged-source-manifest.json"
res=p3s.verify_staged_source(str(root_p), proposal, staged)
print(f"verify OK {res}", flush=True)
import json
staged_j=json.loads((root_p/staged).read_bytes())
print(f"staged keys={list(staged_j.keys())}", flush=True)
# code_deps 63?
print(f"code_deps in staged? {'code_deps' in staged_j}", flush=True)
"""
p=run_tag("ed-p3s-verify", [sys.executable,"-c",code, str(FIX)])
assert p.returncode==0, open(EVID/"ed-p3s-verify-stderr.txt").read()[:8000]
print("P3S VERIFY DONE", flush=True)
