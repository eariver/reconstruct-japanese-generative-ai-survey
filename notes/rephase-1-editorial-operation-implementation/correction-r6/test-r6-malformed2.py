#!/usr/bin/env python3
"""R6 malformed missing-key negatives (strict, fresh digests).
M1 manuscript missing primary (with reviews/candidate/seal fresh to isolate missing-primary)
M2 review missing reader_manuscript (fresh review/candidate/seal)
M3 Gate missing derivation (fresh seal)
All must refuse even with fresh valid hash (no digest preemption).
"""
from __future__ import annotations
import json
import os
import subprocess
import sys
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey").resolve()
NEW_SRC = REPO / ".rephase-1-editorial-runtime/jgas-editorial-r6-20261023T000000Z/candidate-partial-b40de60"
INERT_W = REPO / ".rephase-1-editorial-runtime/final-r5b/weekly-inert"
R6_BASE = REPO / ".rephase-1-editorial-runtime/r6-tests"
NOTES_R6 = REPO / "notes/rephase-1-editorial-operation-implementation/correction-r6"
ISSUE = "2026-W37"
PROP = "wk-r5b-2"
PUBDIR = f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP}/publication"
SET_REL = f"{PUBDIR}/publication-set.json"
def log(m):
    print(m, flush=True)
def run_git(cwd, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file"})
    return subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True, timeout=60, env=env)
def sha_file(p: Path) -> str:
    import hashlib as _h
    h=_h.sha256()
    with p.open("rb") as f:
        for ch in iter(lambda: f.read(1<<20), b""): h.update(ch)
    return h.hexdigest()
def main() -> int:
    sys.path.insert(0, str(NEW_SRC))
    from scripts import survey_production_v2 as core_new
    R6_BASE.mkdir(parents=True, exist_ok=True)
    NOTES_R6.mkdir(parents=True, exist_ok=True)
    (R6_BASE / "tmp").mkdir(parents=True, exist_ok=True)
    results=[]
    def cp_fresh(name: str) -> Path:
        dst=R6_BASE/name
        if dst.exists():
            import shutil as _sh
            _sh.rmtree(dst)
        dst.parent.mkdir(parents=True, exist_ok=True)
        r=subprocess.run(["cp","-a",str(INERT_W),str(dst)], capture_output=True, text=True, timeout=180)
        assert r.returncode==0
        toplevel=run_git(dst,"rev-parse","--show-toplevel").stdout.strip()
        assert Path(toplevel).resolve()==dst.resolve()
        assert "r6-tests" in str(dst)
        return dst
    def run_L(dst: Path, label: str):
        tmpdir=R6_BASE/"tmp"/label
        tmpdir.mkdir(parents=True, exist_ok=True)
        (tmpdir/"pycache").mkdir(parents=True, exist_ok=True)
        code="import sys; sys.path.insert(0, r'"+str(NEW_SRC)+"')\nfrom pathlib import Path\nfrom scripts import survey_publication_set_v2 as low\nrepo=Path(r'"+str(dst)+"')\ntry:\n    low.validate_seal(repo, r'"+SET_REL+"')\n    print('L_UNEXPECTED_PASS')\nexcept Exception as e:\n    print('L_REFUSED ' + type(e).__name__ + ': ' + str(e)[:2000])\n"
        env={k:v for k,v in os.environ.items() if not k.startswith("GIT_") and k not in ("PYTHONPATH","PYTHONPYCACHEPREFIX","TMPDIR")}
        env["PYTHONDONTWRITEBYTECODE"]="1";env["PYTHONPYCACHEPREFIX"]=str(tmpdir/"pycache");env["TMPDIR"]=str(tmpdir);env["PYTHONPATH"]=str(NEW_SRC);env["GIT_NO_LAZY_FETCH"]="1"
        p=subprocess.run([sys.executable,"-B","-c",code],cwd=str(dst),capture_output=True,text=True,timeout=120,env=env)
        (NOTES_R6/f"r6-malformed-{label}-stdout.txt").write_text(p.stdout)
        (NOTES_R6/f"r6-malformed-{label}-stderr.txt").write_text(p.stderr)
        log(f"{label}: {p.stdout[:1200]}")
        return p.stdout
    # M1
    dst1=cp_fresh("r6-malformed-manuscript-missing-primary")
    man_rel=f"{PUBDIR}/reader-manuscript-v2.json"
    man_p=dst1/man_rel
    man=json.loads(man_p.read_bytes().decode())
    del man["primary_source"]
    man_p.write_bytes(core_new.json_bytes(man))
    for _rrel in [f"{PUBDIR}/semantic-review-v2.json",f"{PUBDIR}/visual-review-v2.json"]:
        _rp=dst1/_rrel
        _rv=json.loads(_rp.read_bytes().decode())
        _rv["reader_manuscript"]={"path":man_rel,"sha256":core_new.sha256_bytes(man_p.read_bytes())}
        _base={k:_rv[k] for k in ("schema_version","issue_id","research_profile","publication_profile","review_kind","status","production_profile","reader_manuscript","source","pdf","page_count","checks","reviewed_by","recorded_at") if k in _rv}
        _rv["review_sha256"]=core_new.sha256_object(_base)
        _rp.write_bytes(core_new.json_bytes(_rv))
    cand_rel=f"{PUBDIR}/publication-candidate-v2.json"
    cand_p=dst1/cand_rel
    cand=json.loads(cand_p.read_bytes().decode())
    man_bytes_for_cand=man_p.read_bytes()
    cand["reader_manuscript"]={"path":man_rel,"sha256":core_new.sha256_bytes(man_bytes_for_cand),"byte_count":len(man_bytes_for_cand)}
    for _rk,_rr in (("semantic_review",f"{PUBDIR}/semantic-review-v2.json"),("visual_review",f"{PUBDIR}/visual-review-v2.json")):
        _b=(dst1/_rr).read_bytes()
        cand[_rk]={"path":_rr,"sha256":core_new.sha256_bytes(_b),"byte_count":len(_b)}
    base_c={k:cand[k] for k in ("schema_version","issue_id","publication_profile","status","reader_manuscript","source","pdf","quality_bundle","semantic_review","visual_review")}
    cand["candidate_sha256"]=core_new.sha256_object(base_c)
    cand_p.write_bytes(core_new.json_bytes(cand))
    seal_p=dst1/SET_REL
    seal=json.loads(seal_p.read_bytes().decode())
    man_bytes=man_p.read_bytes()
    seal["roles"]["reader-manuscript"]={"path":man_rel,"sha256":core_new.sha256_bytes(man_bytes),"byte_count":len(man_bytes)}
    for _rk2,_rr2,_sr2 in (("semantic_review",f"{PUBDIR}/semantic-review-v2.json","semantic-review"),("visual_review",f"{PUBDIR}/visual-review-v2.json","visual-review")):
        _b2=(dst1/_rr2).read_bytes()
        seal["roles"][_sr2]={"path":_rr2,"sha256":core_new.sha256_bytes(_b2),"byte_count":len(_b2)}
    cand_bytes=cand_p.read_bytes()
    seal["roles"]["publication-candidate"]={"path":cand_rel,"sha256":core_new.sha256_bytes(cand_bytes),"byte_count":len(cand_bytes)}
    base_s={k:v for k,v in seal.items() if k!="set_sha256"}
    seal["set_sha256"]=core_new.sha256_object(base_s)
    seal_p.write_bytes(core_new.json_bytes(seal))
    out1=run_L(dst1,"manuscript-missing-primary")
    assert "REFUSED" in out1 and "UNEXPECTED_PASS" not in out1 and "primary_source" in out1.lower()
    results.append(("M1","PASS"))
    # M2
    dst2=cp_fresh("r6-malformed-review-missing-manuscript")
    sem_rel=f"{PUBDIR}/semantic-review-v2.json"
    sem_p=dst2/sem_rel
    rev=json.loads(sem_p.read_bytes().decode())
    del rev["reader_manuscript"]
    base_r={k:rev[k] for k in ("schema_version","issue_id","research_profile","publication_profile","review_kind","status","production_profile","source","pdf","page_count","checks","reviewed_by","recorded_at") if k in rev}
    rev["review_sha256"]=core_new.sha256_object(base_r)
    sem_p.write_bytes(core_new.json_bytes(rev))
    cand_p2=dst2/cand_rel
    cand2=json.loads(cand_p2.read_bytes().decode())
    rev_bytes=sem_p.read_bytes()
    cand2["semantic_review"]={"path":sem_rel,"sha256":core_new.sha256_bytes(rev_bytes),"byte_count":len(rev_bytes)}
    base_c2={k:cand2[k] for k in ("schema_version","issue_id","publication_profile","status","reader_manuscript","source","pdf","quality_bundle","semantic_review","visual_review")}
    cand2["candidate_sha256"]=core_new.sha256_object(base_c2)
    cand_p2.write_bytes(core_new.json_bytes(cand2))
    seal_p2=dst2/SET_REL
    seal2=json.loads(seal_p2.read_bytes().decode())
    seal2["roles"]["semantic-review"]={"path":sem_rel,"sha256":core_new.sha256_bytes(rev_bytes),"byte_count":len(rev_bytes)}
    cand_bytes2=cand_p2.read_bytes()
    seal2["roles"]["publication-candidate"]={"path":cand_rel,"sha256":core_new.sha256_bytes(cand_bytes2),"byte_count":len(cand_bytes2)}
    base_s2={k:v for k,v in seal2.items() if k!="set_sha256"}
    seal2["set_sha256"]=core_new.sha256_object(base_s2)
    seal_p2.write_bytes(core_new.json_bytes(seal2))
    out2=run_L(dst2,"review-missing-manuscript")
    assert "REFUSED" in out2 and "UNEXPECTED_PASS" not in out2
    results.append(("M2","PASS"))
    # M3
    dst3=cp_fresh("r6-malformed-gate-missing-derivation")
    gate_rel=f"{PUBDIR}/reader-surface-gate-v2.json"
    gate_p=dst3/gate_rel
    gate=json.loads(gate_p.read_bytes().decode())
    del gate["derivation"]
    gate_p.write_bytes(core_new.json_bytes(gate))
    seal_p3=dst3/SET_REL
    seal3=json.loads(seal_p3.read_bytes().decode())
    gate_bytes=gate_p.read_bytes()
    seal3["roles"]["reader-surface-gate"]={"path":gate_rel,"sha256":core_new.sha256_bytes(gate_bytes),"byte_count":len(gate_bytes)}
    base_s3={k:v for k,v in seal3.items() if k!="set_sha256"}
    seal3["set_sha256"]=core_new.sha256_object(base_s3)
    seal_p3.write_bytes(core_new.json_bytes(seal3))
    out3=run_L(dst3,"gate-missing-derivation")
    assert "REFUSED" in out3 and "UNEXPECTED_PASS" not in out3
    results.append(("M3","PASS"))
    log(f"TOTAL malformed {len(results)}")
    (NOTES_R6/"r6-malformed-summary.json").write_text(json.dumps([{"name":n,"status":s} for n,s in results],indent=2))
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
