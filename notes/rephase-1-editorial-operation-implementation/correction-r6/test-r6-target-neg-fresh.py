#!/usr/bin/env python3
"""R6 target mismatch negative with fresh hashes (new SOURCE fresh authority).

Base: fresh Weekly active fixture r6-weekly-fresh (State r1 active, set wk-r6-1
with external reviews, new R6 code pins correct). Copy to r6-weekly-target-neg,
same-byte manuscript copy to new path, review internal manuscript to new path
(same SHA, fresh review_sha), candidate + seal fresh digests (fresh candidate_sha,
fresh seal roles + set_sha). Seal manuscript stays old path. H validate must
refuse path/binding (not digest), State unchanged/no-write. L must also refuse.
"""
from __future__ import annotations
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey").resolve()
NEW_SRC = REPO / ".rephase-1-editorial-runtime/jgas-editorial-r6-20261023T000000Z/candidate-partial-b40de60"
FRESH = REPO / ".rephase-1-editorial-runtime/r6-weekly-fresh/candidate-partial-b40de60"
NEG_BASE = REPO / ".rephase-1-editorial-runtime/r6-weekly-target-neg"
NOTES_R6 = REPO / "notes/rephase-1-editorial-operation-implementation/correction-r6"

ISSUE = "2026-W37"
PROP = "wk-r6-1"
PUBDIR = f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP}/publication"
STATE_REL = f"sources/{ISSUE}/production-state.json"
SET_REL = f"{PUBDIR}/publication-set.json"
MAN_REL = f"{PUBDIR}/reader-manuscript-v2.json"
SEM_REL = f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP}/external-reviews/semantic-review-v2.json"
CAND_REL = f"{PUBDIR}/publication-candidate-v2.json"

def log(m):
    print(m, flush=True)

def run_git(cwd, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file"})
    return subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True, timeout=60, env=env)

def sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for ch in iter(lambda: f.read(1<<20), b""):
            h.update(ch)
    return h.hexdigest()

def main() -> int:
    sys.path.insert(0, str(NEW_SRC))
    from scripts import survey_production_v2 as core_new
    NEG_BASE.mkdir(parents=True, exist_ok=True)
    NOTES_R6.mkdir(parents=True, exist_ok=True)
    dst = NEG_BASE / "candidate-partial-b40de60"
    if dst.exists():
        shutil.rmtree(dst)
    # cp -a fresh (with own .git)
    r = subprocess.run(["cp","-a",str(FRESH),str(dst)], capture_output=True, text=True, timeout=180)
    assert r.returncode == 0, f"cp failed {r.stderr[:500]}"
    # verify toplevel
    toplevel = run_git(dst, "rev-parse","--show-toplevel").stdout.strip()
    assert Path(toplevel).resolve() == dst.resolve(), f"toplevel {toplevel} != {dst}"
    log(f"copied fresh to {dst}")

    # same-byte manuscript copy to new path
    man_p = dst / MAN_REL
    man_new_rel = f"{PUBDIR}/reader-manuscript-forged.json"
    man_new_p = dst / man_new_rel
    man_new_p.write_bytes(man_p.read_bytes())
    assert sha_file(man_new_p) == sha_file(man_p)
    log(f"manuscript copy {MAN_REL} -> {man_new_rel} same SHA {sha_file(man_p)[:16]}")

    # update semantic review internal manuscript to new path (same SHA), fresh review_sha
    sem_p = dst / SEM_REL
    rev = json.loads(sem_p.read_bytes().decode())
    old_rm = rev["reader_manuscript"]
    rev["reader_manuscript"] = {"path": man_new_rel, "sha256": old_rm["sha256"]}
    base_r = {k: rev[k] for k in ("schema_version","issue_id","research_profile","publication_profile","review_kind","status","production_profile","reader_manuscript","source","pdf","page_count","checks","reviewed_by","recorded_at")}
    rev["review_sha256"] = core_new.sha256_object(base_r)
    sem_p.write_bytes(core_new.json_bytes(rev))
    log(f"review internal manuscript rebond fresh review_sha {rev['review_sha256'][:16]}")

    # update Candidate semantic_review SHA to fresh review file (path same, SHA fresh), fresh candidate_sha
    cand_p = dst / CAND_REL
    cand = json.loads(cand_p.read_bytes().decode())
    rev_bytes = sem_p.read_bytes()
    cand["semantic_review"] = {"path": SEM_REL, "sha256": core_new.sha256_bytes(rev_bytes), "byte_count": len(rev_bytes)}
    base_c = {k: cand[k] for k in ("schema_version","issue_id","publication_profile","status","reader_manuscript","source","pdf","quality_bundle","semantic_review","visual_review")}
    cand["candidate_sha256"] = core_new.sha256_object(base_c)
    cand_p.write_bytes(core_new.json_bytes(cand))
    log(f"candidate fresh {cand['candidate_sha256'][:16]}")

    # update Seal semantic-review + candidate roles to fresh, fresh set_sha; seal manuscript stays old
    seal_p = dst / SET_REL
    seal = json.loads(seal_p.read_bytes().decode())
    seal["roles"]["semantic-review"] = {"path": SEM_REL, "sha256": core_new.sha256_bytes(rev_bytes), "byte_count": len(rev_bytes)}
    cand_bytes = cand_p.read_bytes()
    seal["roles"]["publication-candidate"] = {"path": CAND_REL, "sha256": core_new.sha256_bytes(cand_bytes), "byte_count": len(cand_bytes)}
    base_s = {k: v for k, v in seal.items() if k != "set_sha256"}
    seal["set_sha256"] = core_new.sha256_object(base_s)
    seal_p.write_bytes(core_new.json_bytes(seal))
    log(f"seal fresh {seal['set_sha256'][:16]} (manuscript stays old)")

    # State SHA before
    state_p = dst / STATE_REL
    before_sha = sha_file(state_p)
    log(f"State before {before_sha[:16]}")

    # Run L + H with new code (subprocess, PYTHONPATH=NEW_SRC, cwd=dst)
    tmpdir = NEG_BASE / "tmp"
    tmpdir.mkdir(parents=True, exist_ok=True)
    (tmpdir / "pycache").mkdir(parents=True, exist_ok=True)
    def run_child(code: str):
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_") and k not in ("PYTHONPATH","PYTHONPYCACHEPREFIX","TMPDIR")}
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["PYTHONPYCACHEPREFIX"] = str(tmpdir / "pycache")
        env["TMPDIR"] = str(tmpdir)
        env["PYTHONPATH"] = str(NEW_SRC)
        env["GIT_NO_LAZY_FETCH"] = "1"
        p = subprocess.run([sys.executable,"-B","-c",code], cwd=str(dst), capture_output=True, text=True, timeout=120, env=env)
        return p

    code_L = f"""
import sys; sys.path.insert(0, r'{NEW_SRC}')
from pathlib import Path
from scripts import survey_publication_set_v2 as low
repo=Path(r'{dst}')
try:
    low.validate_seal(repo, r'{SET_REL}')
    print("L_UNEXPECTED_PASS")
except Exception as e:
    print(f"L_REFUSED {{type(e).__name__}}: {{str(e)[:1500]}}")
"""
    # Note: need to escape inner f-string braces for outer? Use simple (no outer f-string for inner)
    # Rebuild without nested f-string issue: use string concat
    code_L = "import sys; sys.path.insert(0, r'" + str(NEW_SRC) + "')\nfrom pathlib import Path\nfrom scripts import survey_publication_set_v2 as low\nrepo=Path(r'" + str(dst) + "')\ntry:\n    low.validate_seal(repo, r'" + SET_REL + "')\n    print('L_UNEXPECTED_PASS')\nexcept Exception as e:\n    print('L_REFUSED ' + type(e).__name__ + ': ' + str(e)[:1500])\n"
    code_H = "import sys; sys.path.insert(0, r'" + str(NEW_SRC) + "')\nfrom pathlib import Path\nfrom scripts import survey_editorial_publication_v2 as high\nrepo=Path(r'" + str(dst) + "')\ntry:\n    high.validate_prepared_set(repo, r'" + STATE_REL + "', r'" + SET_REL + "')\n    print('H_UNEXPECTED_PASS')\nexcept Exception as e:\n    print('H_REFUSED ' + type(e).__name__ + ': ' + str(e)[:2000])\n"

    pL = run_child(code_L)
    pH = run_child(code_H)
    log(f"L stdout: {pL.stdout[:1500]}")
    log(f"H stdout: {pH.stdout[:2000]}")
    (NOTES_R6 / "r6-target-neg-fresh-L-stdout.txt").write_text(pL.stdout)
    (NOTES_R6 / "r6-target-neg-fresh-L-stderr.txt").write_text(pL.stderr)
    (NOTES_R6 / "r6-target-neg-fresh-H-stdout.txt").write_text(pH.stdout)
    (NOTES_R6 / "r6-target-neg-fresh-H-stderr.txt").write_text(pH.stderr)
    after_sha = sha_file(state_p)
    (NOTES_R6 / "r6-target-neg-fresh-state.txt").write_text(f"before {before_sha}\nafter {after_sha}\n{'no-write OK' if before_sha==after_sha else 'WRITE DETECTED'}\n")
    assert before_sha == after_sha, "target-neg must be no-write"
    assert "REFUSED" in pL.stdout and "UNEXPECTED_PASS" not in pL.stdout, f"L must refuse {pL.stdout[:800]}"
    assert "REFUSED" in pH.stdout and "UNEXPECTED_PASS" not in pH.stdout, f"H must refuse {pH.stdout[:1000]}"
    assert any(k in (pL.stdout+pH.stdout).lower() for k in ["manuscript","path","bind"]), "refusal should mention manuscript/path"
    log("R6 target-neg fresh PASS (both L+H refuse, no-write)")
    print("EXIT:0")
    return 0

if __name__ == "__main__":
    try:
        import sys as _sys
        _sys.exit(main())
    except Exception:
        import traceback
        traceback.print_exc()
        print("EXIT:2")
        import sys as _sys2
        _sys2.exit(2)
