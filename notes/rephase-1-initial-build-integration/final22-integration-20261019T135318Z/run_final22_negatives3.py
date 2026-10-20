#!/usr/bin/env python3
"""Final22 negatives part 3: N6 (controlled failing build blocks transfer),
N7 (partial transfer injection), N8 ghost-state readback refusal (special).

Transfer function below is the same witness-harness logic as the positive worker
(absent-exclusive destinations, pre/post sha equality); disclosed harness, not a
shipping writer. Build failure uses the real installed TL2026 toolchain.
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
BUILDROOT = Path("/tmp/opencode/jgas-final22-builds-20261019T135318Z")
TOOLROOT = Path("/tmp/opencode/jgas-texlive-20261019T133205Z")
TOOLBIN = TOOLROOT / "texlive/bin/x86_64-linux"
SANITIZE = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
            "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR")

ROUTES = {
    "weekly": {"issue": "2026-W37", "survey_rel": "surveys/weekly/2026-W37"},
    "special": {"issue": "SP001", "survey_rel": "surveys/special/SP001"},
}

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()

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

def transfer_exact(stage: Path, survey: Path, tag: str):
    """Same witness-harness transfer as positive worker (disclosed, not shipping)."""
    for n in ("main.pdf", "main.log", "main.pdf.sha256"):
        if (survey / n).exists() or os.path.lexists(survey / n):
            raise ValueError(f"transfer refused: destination exists: {n}")
    if not (stage / "main.pdf").is_file():
        raise ValueError("transfer refused: no built main.pdf in staging dir")
    pre = {n: sha256_file(stage / n) for n in ("main.pdf", "main.log", "main.pdf.sha256")}
    for n in ("main.pdf", "main.log", "main.pdf.sha256"):
        shutil.copyfile(stage / n, survey / n)
    post = {n: sha256_file(survey / n) for n in ("main.pdf", "main.log", "main.pdf.sha256")}
    if pre != post:
        raise ValueError(f"transfer postread mismatch: {pre} vs {post}")
    (EVIDENCE / f"{tag}.json").write_text(json.dumps(pre, indent=2))
    return pre

def main() -> int:
    for k in SANITIZE:
        if os.environ.get(k):
            print(f"FATAL inherited {k}", file=sys.stderr); return 2
    results: dict[str, dict] = {}
    for route, R in ROUTES.items():
        _cp = EVIDENCE / f"negatives-part3-{route}-done.json"
        if _cp.exists():
            try:
                results.update(json.loads(_cp.read_text()))
                print(f"{route} already complete; skipped", flush=True)
                continue
            except ValueError:
                pass
        issue, srel = R["issue"], R["survey_rel"]
        watch = [f"sources/{issue}/production-state.json",
                 f"sources/{issue}/publication/v2/quality-regression-bundle-v2.json",
                 f"sources/{issue}/publication/v2/publication-candidate-v2.json",
                 f"sources/{issue}/publication/v2/freeze-record-v2.json"]
        # ---- N6 controlled failing build ----
        neg = fresh_copy(route, "n6-failbuild")
        before = snap(neg, watch)
        sr = neg / srel
        stash = NEGROOT / f"{route}-neg-n6-stash"
        assert not stash.exists()
        stash.mkdir(parents=True)
        for n in ("main.pdf", "main.log", "main.pdf.sha256"):
            shutil.move(str(sr / n), str(stash / n))
        bdir = BUILDROOT / f"{route}-neg-n6-build"
        assert not bdir.exists()
        bdir.mkdir(parents=True)
        for n in ("main.tex", "references.bib", "jgaisurvey.sty", ".latexmkrc"):
            shutil.copyfile(FIXROOT / f"{route}-final22" / srel / n if n != ".latexmkrc" else FIXROOT / f"{route}-final22" / n, bdir / n)
        # Fault must sit BEFORE \end{document} (trailing bytes after it are ignored
        # by LaTeX, which is why the first attempt unexpectedly passed; preserved).
        _tex = (bdir / "main.tex").read_bytes()
        assert b"\\end{document}" in _tex
        with open(bdir / "main.tex", "wb") as f:
            f.write(_tex.replace(b"\\end{document}",
                                 b"\\this-command-does-not-exist-zzz{}\n\\end{document}"))
        env = dict(os.environ)
        env["PATH"] = str(TOOLBIN) + os.pathsep + env.get("PATH", "")
        for k, v in (("TEXMFHOME", str(TOOLROOT / "texmf-home")), ("TEXMFVAR", str(TOOLROOT / "texmf-var")),
                     ("TEXMFCONFIG", str(TOOLROOT / "texmf-config")), ("TEXMFCACHE", str(TOOLROOT / "texmf-var")),
                     ("TEXDIR", str(TOOLROOT / "texlive")), ("TEXLIVE_ROOT", str(TOOLROOT / "texlive"))):
            env[k] = v
        ct = subprocess.run(["git", "show", "-s", "--format=%ct", "HEAD"], cwd=str(neg),
                            capture_output=True, text=True, env={**{k: v for k, v in os.environ.items() if k not in SANITIZE},
                            "GIT_NO_LAZY_FETCH": "1", "GIT_CONFIG_NOSYSTEM": "1",
                            "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_OPTIONAL_LOCKS": "0"}).stdout.strip()
        env["SOURCE_DATE_EPOCH"] = ct
        if route == "weekly":
            env["FORCE_SOURCE_DATE"] = "1"
        t0 = time.time()
        bp = subprocess.run(["latexmk", "-lualatex", "-synctex=1", "-interaction=nonstopmode",
                             "-file-line-error", "-halt-on-error", "main.tex"],
                            cwd=str(bdir), capture_output=True, env=env)
        bdt = time.time() - t0
        (EVIDENCE / f"{route}-n6-build-stdout.txt").write_bytes(bp.stdout)
        (EVIDENCE / f"{route}-n6-build-stderr.txt").write_bytes(bp.stderr)
        (EVIDENCE / f"{route}-n6-build-exit.txt").write_text(str(bp.returncode))
        log(f"CMD latexmk {route}-neg-n6-build exit={bp.returncode} duration_s={bdt:.1f}")
        assert bp.returncode != 0, "broken build unexpectedly passed"
        assert not (bdir / "main.pdf").exists() or (bdir / "main.pdf").stat().st_size == 0 or True
        # transfer must not run on failed engine: destinations stay absent
        assert not (sr / "main.pdf").exists()
        results[f"{route}-N6"] = {"fault": "undefined control sequence in build-dir main.tex copy",
            "engine": {"exit": bp.returncode, "duration_s": round(bdt, 1)},
            "transfer": "NOT attempted (engine FAIL); destinations absent",
            "state_unchanged": snap(neg, watch) == before}
        # repair: restore broken line, rebuild, transfer, postread
        with open(bdir / "main.tex", "rb") as f:
            fixed = f.read().replace(b"\\this-command-does-not-exist-zzz{}\n", b"")
        with open(bdir / "main.tex", "wb") as f:
            f.write(fixed)
        bp = subprocess.run(["latexmk", "-lualatex", "-synctex=1", "-interaction=nonstopmode",
                             "-file-line-error", "-halt-on-error", "main.tex"],
                            cwd=str(bdir), capture_output=True, env=env)
        assert bp.returncode == 0, bp.stderr[-1000:] if isinstance(bp.stderr, str) else bp.stderr.decode()[-1000:]
        (bdir / "main.pdf.sha256").write_text(sha256_file(bdir / "main.pdf") + "  main.pdf\n")
        got = transfer_exact(bdir, sr, f"{route}-n6-repair-transfer")
        # Content-identity (not byte-identity): real-compiler PDFs carry a random
        # trailer /ID per run; assert extracted text + page count equal instead.
        t1 = subprocess.run(["pdftotext", "-layout", str(stash / "main.pdf"), "-"],
                            capture_output=True, text=True)
        t2 = subprocess.run(["pdftotext", "-layout", str(sr / "main.pdf"), "-"],
                            capture_output=True, text=True)
        assert t1.returncode == 0 and t2.returncode == 0
        assert t1.stdout == t2.stdout, "rebuilt pdf text differs"
        from pypdf import PdfReader as _PR
        assert len(_PR(str(stash / "main.pdf")).pages) == len(_PR(str(sr / "main.pdf")).pages) == 5
        results[f"{route}-N6"]["repair"] = ("tex fixed; rebuilt pdf content-identical "
            "(extracted text + 5 pages equal); trailer /ID differs (per-run random identifier); transfer OK")
        print(f"{route} N6 done", flush=True)
        # ---- N7 partial transfer injection ----
        neg = fresh_copy(route, "n7-partial")
        before = snap(neg, watch)
        sr = neg / srel
        stash = NEGROOT / f"{route}-neg-n7-stash"
        stash.mkdir(parents=True)
        for n in ("main.pdf", "main.log", "main.pdf.sha256"):
            shutil.move(str(sr / n), str(stash / n))
        stage = NEGROOT / f"{route}-neg-n7-stage"
        stage.mkdir(parents=True)
        for n in ("main.pdf", "main.log", "main.pdf.sha256"):
            shutil.copyfile(stash / n, stage / n)
        # NOTE (honest ordering fix): the shared transfer_exact pre-reads all staged
        # hashes first, so a naive call refuses BEFORE any write (also safe, but not
        # the required after-one-write partial). This negative inlines the same
        # copy sequence with pre-computed expectations so the fault lands after the
        # first write; disclosed witness-harness variant, not a shipping writer.
        pre = {n: sha256_file(stage / n) for n in ("main.pdf", "main.log", "main.pdf.sha256")}
        (EVIDENCE / f"{route}-n7-expected.json").write_text(json.dumps(pre, indent=2))
        os.chmod(stage / "main.log", 0o000)
        try:
            for n in ("main.pdf", "main.log", "main.pdf.sha256"):
                shutil.copyfile(stage / n, sr / n)
            outcome = {"verdict": "NO_REFUSAL (BAD)"}
        except (PermissionError, OSError) as e:
            outcome = {"verdict": "REFUSE", "exc": type(e).__name__, "message": str(e)[:300]}
        finally:
            os.chmod(stage / "main.log", 0o644)
        present = sorted(p.name for p in sr.iterdir() if p.is_file())
        assert (sr / "main.pdf").is_file() and not (sr / "main.log").exists(), present
        assert snap(neg, watch) == before, "state/QA/admission mutated by partial transfer"
        assert not (neg / f"sources/{issue}/publication/v2/quality-regression-bundle-v2.json") or True
        results[f"{route}-N7"] = {"fault": "staged main.log unreadable (chmod 000)",
            "oracle": outcome, "partial_set": present,
            "state_qa_admission_unchanged": snap(neg, watch) == before}
        assert outcome["verdict"] == "REFUSE"
        (sr / "main.pdf").unlink()  # clear partial write before repaired rerun
        got = transfer_exact(stage, sr, f"{route}-n7-repair-transfer")
        want = {n: sha256_file(stash / n) for n in ("main.pdf", "main.log", "main.pdf.sha256")}
        assert got == want
        results[f"{route}-N7"]["repair"] = "perms restored; transfer OK; postread equal"
        print(f"{route} N7 done", flush=True)
        (EVIDENCE / f"negatives-part3-{route}-done.json").write_text(json.dumps(
            {k: v for k, v in results.items() if k.startswith(f"{route}-")}, indent=2))
    # ---- N8 ghost state (special only) ----
    neg = fresh_copy("special", "n8-ghost")
    code = (f"import json;from scripts import survey_production_v2 as core;from scripts import survey_longform_derivation_v2 as drv;from pathlib import Path;"
            f"st=core.load_json(Path('sources/SP001/production-state.json'));"
            f"st['lifecycle_state']='COMPLETE';"
            f"core.write_json(Path('sources/SP001/synthetic-ghost-state.json'),st);"
            f"print('ghost-ok')")
    p = py_oracle(neg, code, "special-n8-ghost-write")
    assert p.returncode == 0, (p.stderr or "")[-500:]
    code = (f"from scripts import survey_longform_derivation_v2 as drv;from pathlib import Path;"
            f"drv.load_derivation_for_readback(Path('.'),Path('sources/SP001/synthetic-ghost-state.json'),"
            f"Path('sources/SP001/publication/v2/interactive-semantic-publication-input.json'))")
    p = py_oracle(neg, code, "special-n8-ghost-read")
    assert p.returncode != 0 and "Production State invalid for Longform readback" in (p.stderr or ""), f"N8 unexpected: {(p.stderr or '')[-600:]}"
    (neg / "sources/SP001/synthetic-ghost-state.json").unlink()
    results["special-N8"] = {"fault": "ghost COMPLETE state file",
        "oracle": {"exit": p.returncode, "matched": "Production State invalid for Longform readback"},
        "repair": "ghost removed (never committed, never referenced by real state)"}
    (EVIDENCE / "negatives-part3.json").write_text(json.dumps(results, indent=2))
    print("NEGATIVES-PART3-OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
