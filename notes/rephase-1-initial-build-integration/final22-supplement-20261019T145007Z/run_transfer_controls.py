#!/usr/bin/env python3
"""Transfer controls with the SAME exclusive helper (evidence-only, not shipping).

Per route, on the supplement RELEASE_CANDIDATE fixtures (untouched by this script
except where the control explicitly writes into a NEW target dir):
 C1 conflict: same survey_root (3 files present) -> FileExistsError, no takeover, shas unchanged.
 C2 failed build: staging dir with trio only (no main.pdf) -> refuse before any write.
 C3 partial: NEW target with trio; staged set with unreadable main.log -> PermissionError
     after exactly 1 write; inventory 3trio+1pdf; fixture State/QA/bundle/candidate shas unchanged.
 C4 restore: another NEW target with trio -> full transfer OK + postread equal.
Uses actual existing build bytes throughout (survey_root trio + transferred outputs);
no TeX rebuild. Failure injection is environmental (chmod/missing/destination), never
a validator stub. Helper failures surface via on_error callback + re-raise.
"""
from __future__ import annotations
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

EVIDENCE = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-initial-build-integration/final22-supplement-20261019T145007Z")
FIXROOT = Path("/tmp/opencode/jgas-supplement-fixtures-20261019T145007Z")
BUILDROOT = Path("/tmp/opencode/jgas-supplement-builds-20261019T145007Z")
SANITIZE = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
            "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR")

ROUTES = {
    "weekly": {"issue": "2026-W37", "survey_rel": "surveys/weekly/2026-W37", "fixture": "weekly-supp5"},
    "special": {"issue": "SP001", "survey_rel": "surveys/special/SP001", "fixture": "special-supp5"},
}

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()

def snap(root: Path, rels) -> dict:
    out = {}
    for r in rels:
        p = root / r
        out[r] = sha256_file(p) if p.is_file() and not p.is_symlink() else ("SYMLINK" if os.path.lexists(p) else "ABSENT")
    return out

def main() -> int:
    for k in SANITIZE:
        if os.environ.get(k):
            print(f"FATAL inherited {k}", file=sys.stderr); return 2
    sys.path.insert(0, str(EVIDENCE))
    from transfer_exclusive import transfer_exact
    results: dict[str, dict] = {}
    for route, R in ROUTES.items():
        issue, srel = R["issue"], R["survey_rel"]
        fix = FIXROOT / R["fixture"]
        sr = fix / srel
        state_f = f"sources/{issue}/production-state.json"
        watch = [state_f, f"sources/{issue}/publication/v2/quality-regression-bundle-v2.json",
                 f"sources/{issue}/publication/v2/publication-candidate-v2.json"]
        before = snap(fix, watch)
        trio = {n: sha256_file(sr / n) for n in ("main.tex", "references.bib", "jgaisurvey.sty")}
        expected = {n: sha256_file(sr / n) for n in ("main.pdf", "main.log", "main.pdf.sha256")}
        # ---- C1 conflict: destinations exist ----
        c1stage = BUILDROOT / f"{route}-c1-stage"
        assert not c1stage.exists(), f"C1 stage exists {c1stage}"
        c1stage.mkdir(parents=True)
        for n in ("main.tex", "references.bib", "jgaisurvey.sty", "main.pdf", "main.log", "main.pdf.sha256"):
            shutil.copyfile(sr / n, c1stage / n)
        events: list = []
        try:
            transfer_exact(fix, c1stage, sr, expected,
                           on_error=lambda e, w, d: events.append({"exc": type(e).__name__, "written": w}))
            results[f"{route}-C1"] = {"verdict": "NO_REFUSAL (BAD)"}
            return 10
        except FileExistsError as e:
            results[f"{route}-C1"] = {"fault": "destinations pre-existing (positive transfer)",
                "oracle": {"exit": "FileExistsError", "message": str(e)[:200]},
                "no_takeover": snap(fix, [f"{srel}/main.pdf", f"{srel}/main.log", f"{srel}/main.pdf.sha256"]) == {f"{srel}/{n}": expected[n] for n in expected}}
        # ---- C2 failed build: staging without pdf ----
        stage_nb = BUILDROOT / f"{route}-nobuld"
        assert not stage_nb.exists(), f"stage exists {stage_nb}"
        stage_nb.mkdir(parents=True)
        for n in ("main.tex", "references.bib", "jgaisurvey.sty"):
            shutil.copyfile(sr / n, stage_nb / n)
        try:
            transfer_exact(fix, stage_nb, sr, expected)
            results[f"{route}-C2"] = {"verdict": "NO_REFUSAL (BAD)"}
            return 11
        except ValueError as e:
            assert "no built main.pdf" in str(e), str(e)[:300]
            results[f"{route}-C2"] = {"fault": "staging dir has trio only (failed-build stand-in)",
                "oracle": {"exit": "ValueError", "matched": "transfer refused: no built main.pdf in staging dir"}}
        # ---- C3 partial: after-first-file failure in NEW target ----
        tdir = BUILDROOT / f"{route}-partial-target"
        assert not tdir.exists(), f"target exists {tdir}"
        tdir.mkdir(parents=True)
        for n in ("main.tex", "references.bib", "jgaisurvey.sty"):
            shutil.copyfile(sr / n, tdir / n)
        stage = BUILDROOT / f"{route}-partial-stage"
        assert not stage.exists()
        stage.mkdir(parents=True)
        for n in ("main.tex", "references.bib", "jgaisurvey.sty", "main.pdf", "main.log", "main.pdf.sha256"):
            shutil.copyfile(sr / n, stage / n)
        pre = snap(stage, ["main.pdf", "main.log", "main.pdf.sha256"])
        os.chmod(stage / "main.log", 0o000)
        events = []
        # Control domain: NEW buildroot targets are outside fixture Git; the SAME
        # helper enforces containment within the declared root (BUILDROOT here,
        # fixture repo for in-fixture transfers). Strictness unchanged, domain declared.
        try:
            transfer_exact(BUILDROOT, stage, tdir, {n: pre[n] for n in ("main.pdf", "main.log", "main.pdf.sha256")},
                           on_error=lambda e, w, d: events.append({"exc": type(e).__name__, "written": list(w), "message": str(e)[:200]}))
            results[f"{route}-C3"] = {"verdict": "NO_REFUSAL (BAD)"}
            return 12
        except (PermissionError, OSError) as e:
            present = sorted(p.name for p in tdir.iterdir() if p.is_file())
            assert (tdir / "main.pdf").is_file() and not (tdir / "main.log").exists(), present
            results[f"{route}-C3"] = {"fault": "staged main.log unreadable (chmod 000)",
                "oracle": {"exit": type(e).__name__, "matched": "PermissionError"},
                "immediate_after_inventory": present,
                "state_qa_unchanged": snap(fix, watch) == before}
        finally:
            os.chmod(stage / "main.log", 0o644)
        assert results[f"{route}-C3"]["oracle"]["exit"] == "PermissionError"
        # ---- C4 restore control in NEW target; partial target preserved untouched ----
        rdir = BUILDROOT / f"{route}-restore-target"
        assert not rdir.exists()
        rdir.mkdir(parents=True)
        for n in ("main.tex", "references.bib", "jgaisurvey.sty"):
            shutil.copyfile(sr / n, rdir / n)
        got = transfer_exact(BUILDROOT, stage, rdir, {n: pre[n] for n in ("main.pdf", "main.log", "main.pdf.sha256")})
        assert got == {n: sha256_file(rdir / n) for n in ("main.pdf", "main.log", "main.pdf.sha256")}
        results[f"{route}-C4"] = {"restore": "NEW target full transfer OK; postread equal",
            "partial_preserved": sorted(p.name for p in tdir.iterdir() if p.is_file())}
        assert results[f"{route}-C4"]["partial_preserved"] == ["jgaisurvey.sty", "main.pdf", "main.tex", "references.bib"]
        print(f"{route} C1-C4 done", flush=True)
    (EVIDENCE / "transfer-controls.json").write_text(json.dumps(results, indent=2))
    print("TRANSFER-CONTROLS-OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
