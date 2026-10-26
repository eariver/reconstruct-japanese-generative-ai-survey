#!/usr/bin/env python3
"""LONGFORM editorial prepare_publication for lf-ed-3 (real TL build)."""
import subprocess, sys, pathlib, json
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
# 1. create manuscript-spec + toolchain-spec for lf-ed-3
code_specs = r"""
import sys, json, pathlib, hashlib
sys.path.insert(0, sys.argv[1])
root_arg=sys.argv[1]
from pathlib import Path
root_p=Path(root_arg)
from scripts import survey_production_v2 as core
import os
print(f"spec child PID={os.getpid()}", flush=True)
issue="SP001"; prop_new="lf-ed-3"
pdir_new=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}"
# manuscript-spec: copy lf-boot-1, update proposal_ref
old_spec=json.loads((root_p/f"sources/{issue}/publication/v2/editorial-corrections/lf-boot-1/manuscript-spec.json").read_bytes())
new_proposal=root_p/pdir_new/"proposal.json"
new_sha=hashlib.sha256(new_proposal.read_bytes()).hexdigest()
new_spec=dict(old_spec)
new_spec["proposal_ref"]={"path":f"{pdir_new}/proposal.json","sha256":new_sha}
new_spec["authored_by"]="longform repair editorial author lf-ed-3"
# keep coverage/requirements FULFILLED (already)
import datetime
new_spec["recorded_at"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
# write
mspec_path=root_p/pdir_new/"manuscript-spec.json"
if not mspec_path.exists():
    mspec_path.write_bytes(core.json_bytes(new_spec))
    print(f"staged manuscript-spec {mspec_path.relative_to(root_p)}", flush=True)
else:
    print(f"manuscript-spec exists", flush=True)
# toolchain-spec: copy lf-boot-1
old_tool=json.loads((root_p/f"sources/{issue}/publication/v2/editorial-corrections/lf-boot-1/toolchain-spec.json").read_bytes())
new_tool=dict(old_tool)
new_tool["executor"]="longform-repair-lf-ed-3"
new_tool["recorded_at"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
tool_path=root_p/pdir_new/"toolchain-spec.json"
if not tool_path.exists():
    tool_path.write_bytes(core.json_bytes(new_tool))
    print(f"staged toolchain-spec {tool_path.relative_to(root_p)}", flush=True)
else:
    print(f"toolchain-spec exists", flush=True)
"""
p = run_tag("ed-specs", [sys.executable,"-c",code_specs, str(FIX)])
assert p.returncode==0, open(EVID/"ed-specs-stderr.txt").read()[:8000]
# 2. prepare_publication (real build, 1200s)
code_prep = r"""
import sys
sys.path.insert(0, sys.argv[1])
root_arg=sys.argv[1]
from pathlib import Path
root_p=Path(root_arg)
from scripts import survey_editorial_publication_v2 as edpub
import os
print(f"prepare child PID={os.getpid()}", flush=True)
issue="SP001"; prop_new="lf-ed-3"
proposal=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/proposal.json"
# find retention manifest and staged manifest and scope?
import glob as _g
# retention manifest
ret=list((root_p/f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/retained").rglob("*retention-manifest.json"))
ret_manifest=str(ret[0].relative_to(root_p))
# staged manifest
staged=list((root_p/f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/staged-source").rglob("*staged-source-manifest.json"))
staged_manifest=str(staged[0].relative_to(root_p)) if staged else None
# scope: we have scope-review-v2.json under proposal dir
scope=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/scope-review-v2.json"
# manuscript/toolchain specs we just created
mspec=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/manuscript-spec.json"
tspec=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/toolchain-spec.json"
print(f"proposal={proposal} staged={staged_manifest} scope={scope}", flush=True)
# prepare_publication needs staged_manifest_path, not scope? Check signature: prepare_publication(root, state_path, proposal_path, staged_manifest_path, manuscript_spec_path, toolchain_spec_path)
# It internally rechecks scope via _require_scope_bound (which loads scope via staged proof?). So we don't pass scope directly.
res=edpub.prepare_publication(str(root_p), f"sources/{issue}/production-state.json", proposal, staged_manifest, mspec, tspec)
import json as _j
print(f"prepare OK publication_dir={res.get('publication_dir') if isinstance(res,dict) else res}", flush=True)
# print keys
print(f"keys={sorted(res.keys()) if isinstance(res,dict) else type(res)}", flush=True)
"""
q = run_tag("ed-prepare-pub", [sys.executable,"-c",code_prep, str(FIX)])
assert q is not None and q.returncode==0, f"prepare pub failed {open(EVID/'ed-prepare-pub-stderr.txt').read()[:12000]}"
print("PREPARE PUB DONE", flush=True)
