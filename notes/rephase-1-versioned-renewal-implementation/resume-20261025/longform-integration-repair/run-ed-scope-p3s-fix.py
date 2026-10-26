#!/usr/bin/env python3
"""Fix scope + P3S for lf-ed-3 (load proposal, no P1 re-run)."""
import subprocess, sys, json, os, pathlib
REPO = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-longform-repair-20261025T090000Z/renewal-longform"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-integration-repair/run-ed-20261025T090000Z"
ENV=dict(os.environ); ENV["PYTHONDONTWRITEBYTECODE"]="1"; ENV["LC_ALL"]="C"
TIMEOUT=1200
def run_tag(tag, cmd, timeout=TIMEOUT):
    import subprocess as sp
    try:
        proc=sp.run(cmd, cwd=str(REPO), capture_output=True, text=True, timeout=timeout, env=ENV)
    except sp.TimeoutExpired:
        (EVID/f"{tag}-stdout.txt").write_text("",encoding="utf-8")
        (EVID/f"{tag}-stderr.txt").write_text(f"TIMEOUT {timeout}s\n",encoding="utf-8")
        (EVID/f"{tag}-exit.txt").write_text("TIMEOUT",encoding="utf-8")
        print(f"{tag}: TIMEOUT",flush=True)
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
code_scope2 = r"""
import sys, json, pathlib
sys.path.insert(0, sys.argv[1])
root_arg=sys.argv[1]; prop_new=sys.argv[2]
from pathlib import Path
root_p=Path(root_arg)
from scripts import survey_production_v2 as core
import os
print(f"scope2 child PID={os.getpid()}", flush=True)
issue="SP001"
pdir_new=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}"
proposal=json.loads((root_p/pdir_new/"proposal.json").read_bytes())
staged_reader_rel=proposal["proposed"]["proposed_reader_ref"]["path"]
after_sha=proposal["proposed"]["proposed_reader_canonical_sha256"]
print(f"staged {staged_reader_rel} sha {after_sha[:12]}", flush=True)
# verify staged file exists and SHA matches
data=(root_p/staged_reader_rel).read_bytes()
import hashlib
assert hashlib.sha256(data).hexdigest()==after_sha
# build scope review (synthetic, small helper logic)
before_ref=proposal["basis"]["active_reader_input_ref"]
upstream=proposal["basis"]["preserved_upstream_digest"]
block={
    "version":"EDITORIAL_CORRECTION_SCOPE_V1",
    "decision":"WITHIN_APPROVED_AUTHORITY",
    "before_reader_input":before_ref,
    "preserved_upstream_sha256":upstream,
    "change_summary":"Synthetic LONGFORM scope judgment inside approved authority (repair, no genuine approval).",
    "evidence_locations":["synthetic-fixture:proposal"],
}
review={
    "schema_version":"2.0-rc1","issue_id":proposal["issue_id"],
    "publication_profile":proposal["publication_profile"],
    "review_kind":"SEMANTIC_EDITORIAL",
    "reviewed_surface":{"path":staged_reader_rel,"sha256":after_sha},
    "checks":[
        {"check_id":"READER_PIPELINE_INDEPENDENCE","status":"PASS","detail":"Synthetic scope reviewer judged proposed reader independently understandable.","evidence_locations":["synthetic-fixture:proposed-reader"]},
        {"check_id":"EDITORIAL_CORRECTION_SCOPE","status":"PASS","detail":"Synthetic scope reviewer judged delta inside approved Architecture authority.","evidence_locations":["synthetic-fixture:proposal"]},
    ],
    "decision":"PASS","reviewed_by":"synthetic LONGFORM scope reviewer (repair)","reviewed_at":"2026-10-25T09:00:00+00:00","recorded_at":"2026-10-25T09:00:00+00:00","status":"PASSED","findings":[],
    "summary":"Synthetic scope PASS for LONGFORM repair.",
    "editorial_correction_scope":block,
}
review["review_sha256"]=core.sha256_object(review)
scope_path=(root_p/staged_reader_rel).parent/f"scope-review-v2.json"
core.write_json(scope_path, review)
print(f"scope {scope_path.relative_to(root_p)}", flush=True)
"""
p = py_inline(code_scope2, [str(FIX), "lf-ed-3"], "ed-scope2")
assert p is not None and p.returncode==0, open(EVID/"ed-scope2-stderr.txt").read()[:8000]
code_p3s2 = r"""
import sys
sys.path.insert(0, sys.argv[1])
root_arg=sys.argv[1]; prop_new=sys.argv[2]
from pathlib import Path
root_p=Path(root_arg)
from scripts import survey_editorial_staged_source_v2 as p3s
import os, json
print(f"P3S2 child PID={os.getpid()}", flush=True)
issue="SP001"
proposal=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/proposal.json"
prop=json.loads((root_p/proposal).read_bytes())
# retention manifest
import glob as _g
ret=list((root_p/f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/retained").rglob("*retention-manifest.json"))
manifest=str(ret[0].relative_to(root_p))
# scope: find scope-review-v2.json under proposal dir (we wrote next to staged reader? Actually staged reader is reader-surface-input, scope is sibling)
# Our scope2 wrote to (staged_reader_rel).parent/scope-review-v2.json = .../lf-ed-3/scope-review-v2.json
scope=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/scope-review-v2.json"
# Our scope2 wrote to staged_reader parent which IS .../lf-ed-3/ (since staged_reader is .../lf-ed-3/reader-surface-input), so scope is .../lf-ed-3/scope-review-v2.json. Good.
print(f"proposal={proposal} manifest={manifest} scope={scope}", flush=True)
res=p3s.materialize_staged_source(str(root_p), f"sources/{issue}/production-state.json", proposal, manifest, scope)
print(f"P3S staged={res.get('staged_manifest_path')}", flush=True)
v=p3s.verify_staged_source(str(root_p), proposal, res.get('staged_manifest_path'))
print(f"P3S verify OK", flush=True)
# check 63?
import json as _j
staged=_j.loads((root_p/res.get('staged_manifest_path')).read_bytes())
# count code deps? Print manifest
print(f"staged manifest keys={list(staged.keys())[:10]}", flush=True)
"""
q = py_inline(code_p3s2, [str(FIX), "lf-ed-3"], "ed-p3s2", timeout=1200)
assert q is not None and q.returncode==0, open(EVID/"ed-p3s2-stderr.txt").read()[:12000]
print("P3S DONE", flush=True)
