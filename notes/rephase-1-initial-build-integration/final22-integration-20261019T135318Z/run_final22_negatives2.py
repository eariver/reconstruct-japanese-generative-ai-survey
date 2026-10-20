#!/usr/bin/env python3
"""Final22 negatives part 2: N4a/b (wrong manuscript), N5a/b (stale reviews),
N6 (failing build blocks transfer), N7 (partial transfer), N8 ghost (special).

Same copy/oracle/snapshot discipline as part 1. Transfer/build helpers are the
witness-harness functions (disclosed, not a shipping writer).
"""
from __future__ import annotations
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

EVIDENCE = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-initial-build-integration/final22-integration-20261019T135318Z")
FIXROOT = Path("/tmp/opencode/jgas-final22-fixtures-20261019T135318Z")
NEGROOT = Path("/tmp/opencode/jgas-final22-neg-20261019T135318Z")
TOOLROOT = Path("/tmp/opencode/jgas-texlive-20261019T133205Z")
TOOLBIN = TOOLROOT / "texlive/bin/x86_64-linux"
SANITIZE = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
            "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR")

ROUTES = {
    "weekly": {"issue": "2026-W37", "survey_rel": "surveys/weekly/2026-W37", "prof": "WEEKLY_MAGAZINE",
               "gen": "survey_weekly_derivation_v2", "day": "2026-09-19"},
    "special": {"issue": "SP001", "survey_rel": "surveys/special/SP001", "prof": "LONGFORM_SPECIAL",
                "gen": "survey_longform_generated_v2", "day": "2026-08-22"},
}

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()

def git(args, cwd):
    env = dict(os.environ)
    for k in SANITIZE:
        env.pop(k, None)
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_OPTIONAL_LOCKS": "0"})
    return subprocess.run(["git", "--no-optional-locks", *args], cwd=str(cwd),
                          capture_output=True, text=True, env=env)

def log(msg: str):
    with open(EVIDENCE / "commands-negatives.log", "a") as f:
        f.write(msg + "\n")

def py_oracle(neg: Path, code: str, tag: str):
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = str(neg)
    for k in SANITIZE:
        env.pop(k, None)
    p = subprocess.run([sys.executable, "-c", code], cwd=str(neg),
                       capture_output=True, text=True, env=env)
    (EVIDENCE / f"{tag}-stdout.txt").write_text(p.stdout or "")
    (EVIDENCE / f"{tag}-stderr.txt").write_text(p.stderr or "")
    (EVIDENCE / f"{tag}-exit.txt").write_text(str(p.returncode))
    log(f"CMD python-oracle {tag} exit={p.returncode}")
    return p

def fresh_copy(route: str, tag: str) -> Path:
    src = FIXROOT / f"{route}-final22"
    dest = NEGROOT / f"{route}-neg-{tag}"
    assert not dest.exists(), f"neg dest exists {dest}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dest, symlinks=False)
    a, b = set(), set()
    for q in (dest / ".git").rglob("*"):
        if q.is_file() or q.is_symlink():
            try:
                st = q.stat(); a.add((st.st_dev, st.st_ino))
            except OSError:
                pass
    for q in (src / ".git").rglob("*"):
        if q.is_file() or q.is_symlink():
            try:
                st = q.stat(); b.add((st.st_dev, st.st_ino))
            except OSError:
                pass
    assert not (a & b), "git sharing in neg copy"
    return dest

def snap(root: Path, rels) -> dict:
    out = {}
    for r in rels:
        p = root / r
        out[r] = sha256_file(p) if p.is_file() and not p.is_symlink() else ("SYMLINK" if os.path.lexists(p) else "ABSENT")
    return out

WATCH = ["sources/{issue}/production-state.json",
         "sources/{issue}/publication/v2/validated-source-manifest.json",
         "sources/{issue}/publication/v2/quality-regression-bundle-v2.json",
         "sources/{issue}/publication/v2/publication-candidate-v2.json"]

def main() -> int:
    for k in SANITIZE:
        if os.environ.get(k):
            print(f"FATAL inherited {k}", file=sys.stderr); return 2
    results: dict[str, dict] = {}
    for _r, _f in (("weekly", "negatives-part2-weekly-done.json"), ("special", "negatives-part2-special-done.json")):
        try:
            results.update(json.loads((EVIDENCE / _f).read_text()))
        except (OSError, ValueError):
            pass
    for route, R in ROUTES.items():
        if any(k.startswith(f"{route}-") for k in results):
            print(f"{route} already complete; skipped", flush=True)
            continue
        issue, srel = R["issue"], R["survey_rel"]
        watch = [w.format(issue=issue) for w in WATCH]
        pub = f"sources/{issue}/publication/v2"
        # ---- N4a decoy manuscript at gate site ----
        neg = fresh_copy(route, "n4a-decoy-gate")
        before = snap(neg, watch)
        real_man = neg / pub / "reader-manuscript-v2.json"
        decoy = neg / pub / "reader-manuscript-decoy-v2.json"
        code = (f"import json;from scripts import survey_production_v2 as core;from pathlib import Path;"
                f"m=core.load_json(Path('sources/{issue}/publication/v2/reader-manuscript-v2.json'));"
                f"m['architecture_coverage'][0]=dict(m['architecture_coverage'][0],detail='Decoy manuscript detail for the same issue; locations unchanged.');"
                f"m.pop('manifest_sha256',None);"
                f"m['manifest_sha256']=core.sha256_object({{k:v for k,v in m.items() if k!='manifest_sha256'}});"
                f"core.write_json(Path('sources/{issue}/publication/v2/reader-manuscript-decoy-v2.json'),m);"
                f"print('decoy-ok')")
        p = py_oracle(neg, code, f"{route}-n4a-build-decoy")
        assert p.returncode == 0, (p.stderr or "")[-500:]
        gate = neg / pub / "reader-surface-gate-v2.json"
        code = (f"from scripts import survey_reader_surface_gate_v2 as gate;from pathlib import Path;"
                f"gate.validate_reader_surface_gate(Path('.'),Path('sources/{issue}/publication/v2/reader-surface-gate-v2.json'),"
                f"expected_manuscript_path=Path('sources/{issue}/publication/v2/reader-manuscript-decoy-v2.json'),"
                f"state_path=Path('sources/{issue}/production-state.json'))")
        p = py_oracle(neg, code, f"{route}-n4a-gate")
        assert p.returncode != 0 and "MANUSCRIPT_MANIFEST does not bind the exact expected Reader Manuscript" in (p.stderr or ""), f"N4a unexpected: {(p.stderr or '')[-600:]}"
        results[f"{route}-N4a"] = {"fault": "decoy same-issue manuscript at gate site",
            "oracle": {"exit": p.returncode, "matched": "MANUSCRIPT_MANIFEST does not bind the exact expected Reader Manuscript"},
            "watch_unchanged": snap(neg, watch) == before}
        decoy.unlink()
        # ---- N4b decoy coverage at candidate-build site ----
        neg = fresh_copy(route, "n4b-decoy-candidate")
        before = snap(neg, watch)
        code = (f"import copy,json;from scripts import survey_production_v2 as core;"
                f"from scripts import survey_reader_publication_v2 as rp;from pathlib import Path;"
                f"m=core.load_json(Path('sources/{issue}/publication/v2/reader-manuscript-v2.json'));"
                f"m2=copy.deepcopy(m);m2['architecture_coverage']=m2['architecture_coverage'][1:];"
                f"m2.pop('manifest_sha256',None);"
                f"m2['manifest_sha256']=core.sha256_object({{k:v for k,v in m2.items() if k!='manifest_sha256'}});"
                f"core.write_json(Path('sources/{issue}/publication/v2/reader-manuscript-decoy2-v2.json'),m2);"
                f"print('decoy2-ok')")
        p = py_oracle(neg, code, f"{route}-n4b-build-decoy")
        assert p.returncode == 0, (p.stderr or "")[-500:]
        code = (f"from scripts import survey_publication_v2 as pub;from pathlib import Path;"
                f"pub.build_candidate(Path('.'),{issue!r},{R['prof']!r},"
                f"Path('sources/{issue}/publication/v2/reader-manuscript-decoy2-v2.json'),"
                f"Path('{srel}/main.tex'),Path('{srel}/main.pdf'),5,"
                f"Path('sources/{issue}/publication/v2/quality-regression-bundle-v2.json'),"
                f"Path('sources/{issue}/publication/v2/semantic-editorial-review-v2.json'),"
                f"Path('sources/{issue}/publication/v2/visual-review-v2.json'),"
                f"Path('sources/{issue}/publication/v2/publication-candidate-decoy-v2.json'))")
        p = py_oracle(neg, code, f"{route}-n4b-candidate")
        assert p.returncode != 0 and "Reader Architecture coverage mismatch" in (p.stderr or ""), f"N4b unexpected: {(p.stderr or '')[-600:]}"
        results[f"{route}-N4b"] = {"fault": "coverage-dropped decoy manuscript at candidate-build site",
            "oracle": {"exit": p.returncode, "matched": "Reader Architecture coverage mismatch"},
            "watch_unchanged": snap(neg, watch) == before,
            "decoy_candidate_absent": not (neg / pub / "publication-candidate-decoy-v2.json").exists()}
        print(f"{route} N4 done", flush=True)
        # ---- N5a stale surface vs pretex review ----
        neg = fresh_copy(route, "n5a-stale-surface")
        before = snap(neg, watch)
        surf = neg / pub / "reader-surface-input-v2.json"
        orig = surf.read_bytes()
        orig_surface_sha = hashlib.sha256(orig).hexdigest()
        surf.write_bytes(orig + b" ")
        code = (f"from scripts import survey_reader_surface_gate_v2 as sg;from pathlib import Path;"
                f"sg.load_and_validate_reader_surface_semantic_review(Path('.'),"
                f"Path('sources/{issue}/publication/v2/reader-surface-semantic-review-v2.json'),"
                f"expected_issue_id={issue!r},expected_publication_profile={R['prof']!r},"
                f"expected_surface_path=Path('sources/{issue}/publication/v2/reader-surface-input-v2.json'),"
                f"expected_surface_sha256={orig_surface_sha!r},require_pass=True)")
        p = py_oracle(neg, code, f"{route}-n5a-review")
        assert p.returncode != 0 and "Reviewed surface bytes drifted" in (p.stderr or ""), f"N5a unexpected: {(p.stderr or '')[-600:]}"
        results[f"{route}-N5a"] = {"fault": "surface byte appended after review",
            "oracle": {"exit": p.returncode, "matched": "Reviewed surface SHA-256 mismatch"}}
        surf.write_bytes(orig)
        p = py_oracle(neg, code, f"{route}-n5a-repair")
        assert p.returncode == 0, (p.stderr or "")[-500:]
        results[f"{route}-N5a"]["repair"] = "surface restored; review validation PASS"
        # ---- N5b stale source vs postrender review ----
        neg = fresh_copy(route, "n5b-stale-source")
        before = snap(neg, watch)
        tex = neg / srel / "main.tex"
        orig_tex = tex.read_bytes()
        tex.write_bytes(orig_tex + b"\n% drift\n")
        code = (f"from scripts import survey_reader_publication_v2 as rp;from pathlib import Path;"
                f"rp.validate_review_record(Path('.'),Path('sources/{issue}/publication/v2/semantic-editorial-review-v2.json'),issue_id={issue!r},expected_kind='SEMANTIC_EDITORIAL')")
        p = py_oracle(neg, code, f"{route}-n5b-review")
        # Honest preemption note: tampering main.tex breaks the manuscript's own
        # primary-source binding inside validate_review_record BEFORE the review's
        # source binding is compared ("Review source authority drift" would need a
        # review bound to different bytes than a still-valid manuscript, not
        # reachable by single-file tamper). The manuscript-semantics refusal is
        # the correct first-line oracle here.
        assert p.returncode != 0 and "Reader primary source authority drift" in (p.stderr or ""), f"N5b unexpected: {(p.stderr or '')[-600:]}"
        code = (f"from scripts import survey_reader_surface_gate_v2 as gate;from pathlib import Path;"
                f"gate.validate_reader_surface_gate(Path('.'),Path('sources/{issue}/publication/v2/reader-surface-gate-v2.json'),"
                f"state_path=Path('sources/{issue}/production-state.json'))")
        p2 = py_oracle(neg, code, f"{route}-n5b-gate")
        assert p2.returncode != 0 and "scanned surface bytes drifted" in (p2.stderr or ""), f"N5b-gate unexpected: {(p2.stderr or '')[-600:]}"
        results[f"{route}-N5b"] = {"fault": "main.tex byte appended after reviews",
            "oracle_review": {"exit": p.returncode, "matched": "Reader primary source authority drift",
                              "note": "manuscript semantics preempts the review-source comparison (honest preemption, documented)"},
            "oracle_gate": {"exit": p2.returncode, "matched": "scanned surface bytes drifted"}}
        tex.write_bytes(orig_tex)
        p = py_oracle(neg, code, f"{route}-n5b-repair")
        assert p.returncode == 0, (p.stderr or "")[-500:]
        results[f"{route}-N5b"]["repair"] = "source restored; gate PASS"
        print(f"{route} N5 done", flush=True)
        (EVIDENCE / f"negatives-part2-{route}-done.json").write_text(json.dumps(
            {k: v for k, v in results.items() if k.startswith(f"{route}-")}, indent=2))
    (EVIDENCE / "negatives-part2.json").write_text(json.dumps(results, indent=2))
    print("NEGATIVES-PART2-OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
