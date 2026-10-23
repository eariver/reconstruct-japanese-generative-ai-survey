#!/usr/bin/env python3
"""R6 target-neg fresh inert (strict, no activation drift).
Base: fresh inert r6-weekly-fresh-strict inert (State None, set wk-r6-1 sealed external, new strict code pins correct).
Copy to r6-weekly-target-neg-strict, same-byte manuscript copy to new path, review internal to new path (fresh review_sha), candidate + seal fresh (fresh candidate_sha, seal roles + set_sha). Seal manuscript stays old. L+H must refuse path (not digest), State no-write.
"""
from __future__ import annotations
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey").resolve()
NEW_SRC = REPO / ".rephase-1-editorial-runtime/jgas-editorial-r6-20261023T000000Z/candidate-partial-b40de60"
INERT = REPO / ".rephase-1-editorial-runtime/r6-weekly-fresh-strict/candidate-partial-b40de60-inert"
NEG_BASE = REPO / ".rephase-1-editorial-runtime/r6-weekly-target-neg-strict"
NOTES_R6 = REPO / "notes/rephase-1-editorial-operation-implementation/correction-r6"
ISSUE="2026-W37";PROP="wk-r6-1"
PUBDIR=f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP}/publication"
EXTDIR=f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP}/external-reviews"
STATE_REL=f"sources/{ISSUE}/production-state.json"
SET_REL=f"{PUBDIR}/publication-set.json"
MAN_REL=f"{PUBDIR}/reader-manuscript-v2.json"
SEM_REL=f"{EXTDIR}/semantic-review-v2.json"
CAND_REL=f"{PUBDIR}/publication-candidate-v2.json"
def log(m):
    print(m,flush=True)
def run_git(cwd,*args):
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file"})
    return subprocess.run(["git",*args],cwd=str(cwd),capture_output=True,text=True,timeout=60,env=env)
def sha_file(p:Path)->str:
    import hashlib as _h
    h=_h.sha256()
    with p.open("rb") as f:
        for ch in iter(lambda:f.read(1<<20),b""):h.update(ch)
    return h.hexdigest()
def main()->int:
    sys.path.insert(0,str(NEW_SRC))
    from scripts import survey_production_v2 as core_new
    NEG_BASE.mkdir(parents=True,exist_ok=True)
    NOTES_R6.mkdir(parents=True,exist_ok=True)
    dst=NEG_BASE/"candidate-partial-b40de60"
    if dst.exists():
        shutil.rmtree(dst)
    r=subprocess.run(["cp","-a",str(INERT),str(dst)],capture_output=True,text=True,timeout=180)
    assert r.returncode==0
    toplevel=run_git(dst,"rev-parse","--show-toplevel").stdout.strip()
    assert Path(toplevel).resolve()==dst.resolve()
    log(f"copied inert to {dst}")
    man_p=dst/MAN_REL
    man_new_rel=f"{PUBDIR}/reader-manuscript-forged.json"
    man_new_p=dst/man_new_rel
    man_new_p.write_bytes(man_p.read_bytes())
    assert sha_file(man_new_p)==sha_file(man_p)
    sem_p=dst/SEM_REL
    rev=json.loads(sem_p.read_bytes().decode())
    rev["reader_manuscript"]={"path":man_new_rel,"sha256":core_new.sha256_bytes(man_p.read_bytes())}
    # Note: man_p.read_bytes() is old manuscript bytes (with trio), man_new_p same bytes (same SHA) - path different, SHA same. Good same-SHA rebind.
    base_r={k:rev[k] for k in ("schema_version","issue_id","research_profile","publication_profile","review_kind","status","production_profile","reader_manuscript","source","pdf","page_count","checks","reviewed_by","recorded_at") if k in rev}
    rev["review_sha256"]=core_new.sha256_object(base_r)
    sem_p.write_bytes(core_new.json_bytes(rev))
    cand_p=dst/CAND_REL
    cand=json.loads(cand_p.read_bytes().decode())
    rev_bytes=sem_p.read_bytes()
    cand["semantic_review"]={"path":SEM_REL,"sha256":core_new.sha256_bytes(rev_bytes),"byte_count":len(rev_bytes)}
    base_c={k:cand[k] for k in ("schema_version","issue_id","publication_profile","status","reader_manuscript","source","pdf","quality_bundle","semantic_review","visual_review")}
    cand["candidate_sha256"]=core_new.sha256_object(base_c)
    cand_p.write_bytes(core_new.json_bytes(cand))
    seal_p=dst/SET_REL
    seal=json.loads(seal_p.read_bytes().decode())
    seal["roles"]["semantic-review"]={"path":SEM_REL,"sha256":core_new.sha256_bytes(rev_bytes),"byte_count":len(rev_bytes)}
    cand_bytes=cand_p.read_bytes()
    seal["roles"]["publication-candidate"]={"path":CAND_REL,"sha256":core_new.sha256_bytes(cand_bytes),"byte_count":len(cand_bytes)}
    base_s={k:v for k,v in seal.items() if k!="set_sha256"}
    seal["set_sha256"]=core_new.sha256_object(base_s)
    seal_p.write_bytes(core_new.json_bytes(seal))
    state_p=dst/STATE_REL
    before=sha_file(state_p)
    tmpdir=NEG_BASE/"tmp"
    tmpdir.mkdir(parents=True,exist_ok=True)
    (tmpdir/"pycache").mkdir(parents=True,exist_ok=True)
    def run_child(code:str):
        env={k:v for k,v in os.environ.items() if not k.startswith("GIT_") and k not in ("PYTHONPATH","PYTHONPYCACHEPREFIX","TMPDIR")}
        env["PYTHONDONTWRITEBYTECODE"]="1";env["PYTHONPYCACHEPREFIX"]=str(tmpdir/"pycache");env["TMPDIR"]=str(tmpdir);env["PYTHONPATH"]=str(dst);env["GIT_NO_LAZY_FETCH"]="1"
        return subprocess.run([sys.executable,"-B","-c",code],cwd=str(dst),capture_output=True,text=True,timeout=120,env=env)
    code_L="import sys; sys.path.insert(0, r'"+str(dst)+"')\nfrom pathlib import Path\nfrom scripts import survey_publication_set_v2 as low\nrepo=Path(r'"+str(dst)+"')\ntry:\n    low.validate_seal(repo, r'"+SET_REL+"')\n    print('L_UNEXPECTED_PASS')\nexcept Exception as e:\n    print('L_REFUSED ' + type(e).__name__ + ': ' + str(e)[:2000])\n"
    code_H="import sys; sys.path.insert(0, r'"+str(dst)+"')\nfrom pathlib import Path\nfrom scripts import survey_editorial_publication_v2 as high\nrepo=Path(r'"+str(dst)+"')\ntry:\n    high.validate_prepared_set(repo, r'"+STATE_REL+"', r'"+SET_REL+"')\n    print('H_UNEXPECTED_PASS')\nexcept Exception as e:\n    print('H_REFUSED ' + type(e).__name__ + ': ' + str(e)[:2500])\n"
    pL=run_child(code_L)
    pH=run_child(code_H)
    log(f"L: {pL.stdout[:1500]}")
    log(f"H: {pH.stdout[:2500]}")
    (NOTES_R6/"r6-target-neg-strict-L-stdout.txt").write_text(pL.stdout)
    (NOTES_R6/"r6-target-neg-strict-L-stderr.txt").write_text(pL.stderr)
    (NOTES_R6/"r6-target-neg-strict-H-stdout.txt").write_text(pH.stdout)
    (NOTES_R6/"r6-target-neg-strict-H-stderr.txt").write_text(pH.stderr)
    after=sha_file(state_p)
    (NOTES_R6/"r6-target-neg-strict-state.txt").write_text(f"before {before}\nafter {after}\n{'no-write OK' if before==after else 'WRITE'}\n")
    assert before==after
    assert "REFUSED" in pL.stdout and "UNEXPECTED_PASS" not in pL.stdout
    assert "REFUSED" in pH.stdout and "UNEXPECTED_PASS" not in pH.stdout
    assert "manuscript" in (pL.stdout+pH.stdout).lower() or "path" in (pL.stdout+pH.stdout).lower()
    # Ensure H refusal is path/binding, not ToolDrift (no current_tools/tool/drift confusion? H may still have ToolDrift? Fresh inert pins new code, new code validation should not ToolDrift. Check H stdout does not contain ToolDrift-only (e.g., current_tools, code_deps, runtime) without path? It should contain path.
    assert "path" in pH.stdout.lower() or "bind" in pH.stdout.lower() or "manuscript" in pH.stdout.lower(), f"H must mention path/bind {pH.stdout[:800]}"
    log("R6 target-neg strict inert PASS")
    print("EXIT:0")
    return 0
if __name__=="__main__":
    try:
        import sys as _s
        _s.exit(main())
    except Exception:
        import traceback
        traceback.print_exc()
        print("EXIT:2")
        import sys as _s2
        _s2.exit(2)
