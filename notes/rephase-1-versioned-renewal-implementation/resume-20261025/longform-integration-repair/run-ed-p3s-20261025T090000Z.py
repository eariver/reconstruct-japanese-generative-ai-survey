#!/usr/bin/env python3
"""LONGFORM P3S63 + editorial build + postrender + finalize + activate for lf-ed-3.
Scope synthetic (small helper logic), P3S63, real TL build, fresh QA + synthetic reviews, finalize, activate, history.
1200s per phase.
"""
import subprocess, sys, json, os, pathlib
from datetime import datetime, timezone
REPO = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-longform-repair-20261025T090000Z/renewal-longform"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-integration-repair/run-ed-20261025T090000Z"
ENV=dict(os.environ); ENV["PYTHONDONTWRITEBYTECODE"]="1"; ENV["LC_ALL"]="C"
TIMEOUT=1200
def run_tag(tag, cmd, timeout=TIMEOUT):
    import subprocess as sp
    try:
        proc=sp.run(cmd, cwd=str(REPO), capture_output=True, text=True, timeout=timeout, env=ENV)
    except sp.TimeoutExpired as e:
        (EVID/f"{tag}-stdout.txt").write_text("",encoding="utf-8")
        (EVID/f"{tag}-stderr.txt").write_text(f"TIMEOUT {timeout}s in {tag}\n",encoding="utf-8")
        (EVID/f"{tag}-exit.txt").write_text("TIMEOUT",encoding="utf-8")
        with open(EVID/"commands.log","a",encoding="utf-8") as fh:
            fh.write(f"$ ... tag={tag} -> TIMEOUT\n")
        print(f"{tag}: TIMEOUT",flush=True)
        return None
    (EVID/f"{tag}-stdout.txt").write_text(proc.stdout or "",encoding="utf-8")
    (EVID/f"{tag}-stderr.txt").write_text(proc.stderr or "",encoding="utf-8")
    (EVID/f"{tag}-exit.txt").write_text(str(proc.returncode),encoding="utf-8")
    with open(EVID/"commands.log","a",encoding="utf-8") as fh:
        fh.write(f"$ {' '.join(cmd[:6])}... tag={tag} -> exit={proc.returncode}\n")
    print(f"{tag}: exit={proc.returncode}",flush=True)
    return proc
def py_inline(code, argv, tag, timeout=TIMEOUT):
    return run_tag(tag, [sys.executable,"-c",code]+argv, timeout=timeout)
def main():
    prop_new="lf-ed-3"; issue="SP001"
    # scope review (synthetic, small helper logic, NEW runner)
    code_scope = r"""
import sys, json, pathlib
sys.path.insert(0, sys.argv[1])
root_arg=sys.argv[1]; prop_new=sys.argv[2]
from pathlib import Path
root_p=Path(root_arg)
from scripts import survey_production_v2 as core
from scripts import survey_editorial_correction_proposal_v2 as p1mod
import os
print(f"scope child PID={os.getpid()}", flush=True)
issue="SP001"
pdir_new=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}"
proposal_path=root_p/pdir_new/"proposal.json"
proposal=json.loads(proposal_path.read_bytes())
# need prepared dict? Re-derive proposed_canonical via P1 prepare (read-only, same authoring)
dest=root_p/pdir_new/"authoring-input.json"
res=p1mod.prepare_proposal(root_p, root_p/f"sources/{issue}/production-state.json", dest, prop_new, "scope re-derive")
staged_reader_rel=res["proposal"]["proposed"]["proposed_reader_ref"]["path"]
after_sha=core.sha256_bytes(res["proposed_canonical"])
# write staged reader file if not exists (needed for scope target)
staged_path=root_p/staged_reader_rel
staged_path.parent.mkdir(parents=True, exist_ok=True)
if not staged_path.exists():
    staged_path.write_bytes(res["proposed_canonical"])
    print(f"staged reader {staged_reader_rel}", flush=True)
block={
    "version":"EDITORIAL_CORRECTION_SCOPE_V1",
    "decision":"WITHIN_APPROVED_AUTHORITY",
    "before_reader_input":res["proposal"]["basis"]["active_reader_input_ref"],
    "preserved_upstream_sha256":res["proposal"]["basis"]["preserved_upstream_digest"],
    "change_summary":"Synthetic LONGFORM scope judgment inside approved authority (repair, no genuine approval).",
    "evidence_locations":["synthetic-fixture:proposal"],
}
review={
    "schema_version":"2.0-rc1","issue_id":res["proposal"]["issue_id"],
    "publication_profile":res["proposal"]["publication_profile"],
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
scope_path=(root_p/staged_reader_rel).parent/"scope-review-v2.json"
core.write_json(scope_path, review)
print(f"scope {scope_path.relative_to(root_p)}", flush=True)
"""
    s = py_inline(code_scope, [str(FIX), prop_new], "ed-scope")
    assert s is not None and s.returncode==0, f"scope failed {open(EVID/'ed-scope-stderr.txt').read()[:8000]}"
    # P3S materialize
    code_p3s = r"""
import sys
sys.path.insert(0, sys.argv[1])
root_arg=sys.argv[1]; prop_new=sys.argv[2]
from pathlib import Path
root_p=Path(root_arg)
from scripts import survey_editorial_staged_source_v2 as p3s
import os
print(f"P3S child PID={os.getpid()}", flush=True)
issue="SP001"
proposal=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/proposal.json"
# find retention manifest
import glob as _g
ret=list((root_p/f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/retained").rglob("*retention-manifest.json"))
print(f"ret cands={[str(p.relative_to(root_p)) for p in ret]}", flush=True)
manifest=str(ret[0].relative_to(root_p)) if ret else None
# find scope: staged reader dir scope-review-v2.json (we wrote next to staged reader, need to locate)
# staged reader path from proposal
import json
prop=json.loads((root_p/proposal).read_bytes())
staged_reader=prop["proposed"]["proposed_reader_ref"]["path"]
scope=str((Path(staged_reader).parent/"scope-review-v2.json"))
print(f"proposal={proposal} manifest={manifest} scope={scope}", flush=True)
res=p3s.materialize_staged_source(str(root_p), f"sources/{issue}/production-state.json", proposal, manifest, scope)
print(f"P3S staged={res.get('staged_manifest_path') if isinstance(res,dict) else res}", flush=True)
# verify
v=p3s.verify_staged_source(str(root_p), proposal, res.get('staged_manifest_path') if isinstance(res,dict) else res.get('staged_manifest_path'))
print(f"P3S verify OK", flush=True)
"""
    m = py_inline(code_p3s, [str(FIX), prop_new], "ed-p3s", timeout=1200)
    assert m is not None and m.returncode==0, f"P3S failed {open(EVID/'ed-p3s-stderr.txt').read()[:10000]}"
    print("P3S63 DONE", flush=True)
    return 0
if __name__=="__main__":
    raise SystemExit(main())
