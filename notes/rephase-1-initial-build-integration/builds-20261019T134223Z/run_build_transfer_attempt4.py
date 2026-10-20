#!/usr/bin/env python3
"""Pass2 + real builds + transfer + strict receipt (R2 mechanical witness) — FULL harness.

Saved BEFORE any execution. Single ordered run:
 0 verify source/fixtures/toolchain (read-only except evidence writes)
 1 stage synthetic type-only pre-TeX reviews (mechanics only, NO genuine PASS)
 2 actual publisher pass2 both routes (subprocess, raw capture)
 3 disposable build dirs + exact trio/.latexmkrc copy (hash all)
 4 latexmk real builds with fixture-epoch SOURCE_DATE_EPOCH (raw + census + versions)
 5 workflow log-gate checks (engine success vs log gate separated)
 6 stage PDF/log/digest + transfer ONLY 3 files to canonical survey_root (absent-only)
 7 post-transfer strict receipt + build-dir validation (actual validators)
 8 evidence packet PDFs/text/PNGs + per-route report; STOP before manuscript/QA/Candidate/State.

No fixture/reconstruct commits, no Production actions, no generated-TeX edits.
On renderer/style bug: record raw + minimal fix proposal, do NOT edit TeX.
"""
from __future__ import annotations
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

TS = "20261019T134223Z"
EVIDENCE_DIR = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-initial-build-integration/builds-20261019T134223Z")
SUF = "-attempt4"
class _Ev:
    """Attempt-namespaced evidence paths: every file gets -attempt2 suffix; never overwrites attempt1."""
    def __truediv__(self, name):
        p = Path(str(name))
        suffix = "".join(p.suffixes)
        stem = p.name[:len(p.name) - len(suffix)] if suffix else p.name
        return EVIDENCE_DIR / (stem + SUF + suffix)
    def mkdir(self, *a, **k):
        return EVIDENCE_DIR.mkdir(*a, **k)
EVIDENCE = _Ev()
SOURCE = Path("/tmp/opencode/jgas-initial-build-20261019T132209Z/candidate-partial-b40de60")
WEEKLY = Path("/tmp/opencode/jgas-initial-fixtures-20261019T133259Z/weekly-fixture")
SPECIAL = Path("/tmp/opencode/jgas-initial-fixtures-20261019T133259Z/special-fixture")
TOOLROOT = Path("/tmp/opencode/jgas-texlive-20261019T133205Z")
TOOLBIN = TOOLROOT / "texlive/bin/x86_64-linux"
BUILDROOT = Path("/tmp/opencode/jgas-initial-builds-20261019T134223Z")
STATIC21 = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-dm021-p3s/draft-history-r11/static21.json")
INSPECTION_REF = "notes/rephase-1-initial-build-integration/independent-pretex-inspection.md (production semantic NO-GO both)"

WEEKLY_HEAD = "88813a01accb320b5948e368618e4061a4d72e0b"
SPECIAL_HEAD = "d4078d1bc851b9977289acf4b9cd6560c080b69e"
WEEKLY_ISSUE = "2026-W37"
SPECIAL_ISSUE = "SP001"

GIT_SANITIZE = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
                "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR")

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()

def log_cmd(cmd, cwd, exit_code, extra=""):
    with open(EVIDENCE / "commands.log", "a") as f:
        f.write(f"CMD {' '.join(str(c) for c in cmd)} | cwd={cwd} | exit={exit_code} {extra}\n".replace("\n", " "))

def git(args, cwd: Path):
    env = dict(os.environ)
    for k in GIT_SANITIZE:
        env.pop(k, None)
    env["GIT_NO_LAZY_FETCH"] = "1"
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_CONFIG_GLOBAL"] = "/dev/null"
    env["GIT_OPTIONAL_LOCKS"] = "0"
    p = subprocess.run(["git", "--no-optional-locks", *args], cwd=str(cwd),
                       capture_output=True, text=True, env=env)
    log_cmd(["git"] + args, str(cwd), p.returncode)
    return p

def must_absent(p: Path, label: str):
    if p.exists() or os.path.lexists(p):
        print(f"FATAL {label} already exists (no overwrite): {p}", file=sys.stderr)
        raise SystemExit(20)

def run_capture(cmd, cwd: Path, env_extra: dict, out_name: str, err_name: str, exit_name: str):
    out_path, err_path, exit_path = EVIDENCE / out_name, EVIDENCE / err_name, EVIDENCE / exit_name
    for pp in (out_path, err_path, exit_path):
        must_absent(pp, "capture output")
    env = dict(os.environ)
    env.update(env_extra)
    t0 = time.time()
    p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, env=env)
    dt = time.time() - t0
    out_path.write_bytes(p.stdout)
    err_path.write_bytes(p.stderr)
    exit_path.write_text(str(p.returncode))
    log_cmd(cmd, str(cwd), p.returncode, f"duration_s={dt:.1f} stdout={out_name} stderr={err_name}")
    return p, dt

def main() -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    open(EVIDENCE / "commands.log", "w").write(f"# pass2/build/transfer {TS}\n")
    for k in GIT_SANITIZE:
        if os.environ.get(k):
            print(f"FATAL inherited {k}", file=sys.stderr)
            return 2
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    # ---------- 0. verify ----------
    src_head = git(["rev-parse", "HEAD"], SOURCE).stdout.strip()
    if src_head != "409b292756dd1277b9dfae87679934c0d2ce251c":
        print(f"source HEAD mismatch {src_head}", file=sys.stderr); return 3
    (EVIDENCE / "source-status-before.txt").write_text(git(["status", "--porcelain=v1", "--untracked-files=all"], SOURCE).stdout)
    static21 = json.loads(STATIC21.read_text())
    epochs = {}
    for label, fix, exp_head in (("weekly", WEEKLY, WEEKLY_HEAD), ("special", SPECIAL, SPECIAL_HEAD)):
        h = git(["rev-parse", "HEAD"], fix).stdout.strip()
        (EVIDENCE / f"{label}-head-verify.txt").write_text(h + "\n")
        if h != exp_head:
            print(f"{label} HEAD mismatch {h} expected {exp_head}", file=sys.stderr); return 5
        st = git(["status", "--porcelain=v1", "--untracked-files=all"], fix).stdout
        (EVIDENCE / f"{label}-status-before.txt").write_text(st)
        tracked_mods = [l for l in st.splitlines() if l.startswith(" M") or l.startswith("M ")]
        if tracked_mods:
            print(f"{label} tracked mods {tracked_mods}", file=sys.stderr); return 6
        dnames = git(["diff", "--name-only", "HEAD"], fix).stdout.strip()
        (EVIDENCE / f"{label}-diff-before.txt").write_text(dnames)
        if dnames.strip():
            print(f"{label} tracked diff non-empty", file=sys.stderr); return 7
        bad = [rel for rel, pin in static21.items() if not (fix / rel).is_file() or sha256_file(fix / rel) != pin["sha256"]]
        (EVIDENCE / f"{label}-control21-check.txt").write_text(json.dumps({"mismatches": bad}, indent=2))
        if bad:
            print(f"{label} control21 mismatch {bad}", file=sys.stderr); return 8
        cfg = git(["config", "--local", "--list"], fix).stdout
        (EVIDENCE / f"{label}-config-verify.txt").write_text(cfg)
        if "user.name=" in cfg or "user.email=" in cfg:
            print(f"{label} persistent user.*", file=sys.stderr); return 9
        if (fix / ".git/objects/info/alternates").exists():
            print(f"{label} alternates", file=sys.stderr); return 10
        ct = git(["show", "-s", "--format=%ct", "HEAD"], fix).stdout.strip()
        (EVIDENCE / f"{label}-source-epoch.txt").write_text(ct + "\n")
        epochs[label] = ct
    # toolchain versions (no download)
    tenv_base = {"PATH": str(TOOLBIN) + os.pathsep + os.environ.get("PATH", "")}
    for name, args in (("lualatex", ["lualatex", "--version"]), ("latexmk", ["latexmk", "--version"]),
                       ("biber", ["biber", "--version"]), ("kpsewhich-jlreq", ["kpsewhich", "jlreq.cls"]),
                       ("kpsewhich-luatexja", ["kpsewhich", "luatexja.sty"])):
        env = dict(os.environ); env.update(tenv_base)
        p = subprocess.run(args, capture_output=True, env=env, cwd=str(EVIDENCE_DIR))
        (EVIDENCE / f"tool-{name}-stdout.txt").write_bytes(p.stdout or b"")
        (EVIDENCE / f"tool-{name}-stderr.txt").write_bytes(p.stderr or b"")
        (EVIDENCE / f"tool-{name}-exit.txt").write_text(str(p.returncode))
        log_cmd(args, str(EVIDENCE_DIR), p.returncode)
        if p.returncode != 0:
            print(f"tool {name} failed", file=sys.stderr); return 11
    # ---------- 1. synthetic type-only reviews ----------
    sys.path.insert(0, str(WEEKLY))
    from scripts import survey_production_v2 as core_w
    assert Path(core_w.__file__).resolve().as_posix().startswith(WEEKLY.resolve().as_posix())
    w_root = WEEKLY.resolve()
    w_pub = w_root / "sources" / WEEKLY_ISSUE / "publication" / "v2"
    w_surface = w_pub / "reader-surface-input-v2.json"
    w_review = w_pub / "reader-surface-semantic-review-v2.json"
    # attempt1 already staged the identical synthetic review; reuse after pin verification (no overwrite)
    _w_pin = json.loads((EVIDENCE_DIR / "weekly-review-pin.json").read_text())
    if w_review.exists():
        if sha256_file(w_review) != _w_pin["sha256"]:
            print("weekly review exists with different bytes; refusing", file=sys.stderr); return 12
        (EVIDENCE / "weekly-review-pin.json").write_text(json.dumps(_w_pin, indent=2))
    else:
        print("weekly review missing on attempt2; refusing to recreate (attempt1 staged it)", file=sys.stderr); return 12
    _w_rev_surface = _w_pin["surface_sha256"]
    # (attempt1 staged the byte-identical review verified above; no rewrite)
    for m in [m for m in list(sys.modules) if m == "scripts" or m.startswith("scripts.")]:
        del sys.modules[m]
    sys.path.remove(str(WEEKLY))
    sys.path.insert(0, str(SPECIAL))
    from scripts import survey_production_v2 as core_s
    assert Path(core_s.__file__).resolve().as_posix().startswith(SPECIAL.resolve().as_posix())
    s_root = SPECIAL.resolve()
    s_pub = s_root / "sources" / SPECIAL_ISSUE / "publication" / "v2"
    s_surface = s_pub / "reader-surface-input-v2.json"
    s_review = s_pub / "reader-surface-semantic-review-v2.json"
    _s_pin = json.loads((EVIDENCE_DIR / "special-review-pin.json").read_text())
    if s_review.exists():
        if sha256_file(s_review) != _s_pin["sha256"]:
            print("special review exists with different bytes; refusing", file=sys.stderr); return 13
        (EVIDENCE / "special-review-pin.json").write_text(json.dumps(_s_pin, indent=2))
    else:
        print("special review missing on attempt2; refusing to recreate", file=sys.stderr); return 13
    # (attempt1 staged the byte-identical review verified above; no rewrite)
    for m in [m for m in list(sys.modules) if m == "scripts" or m.startswith("scripts.")]:
        del sys.modules[m]
    sys.path.remove(str(SPECIAL))
    print("STAGE reviews-staged")
    # ---------- 2. pass2 outputs VERIFIED (not rerun) ----------
    # attempt2 pass2 CLI succeeded for both routes (exit 0, outputs installed in
    # fixture survey_roots). Rerunning pass2 would refuse existing artifacts, so
    # attempt3 verifies the installed outputs + receipts instead of regenerating.
    _pass2_pins = json.loads((EVIDENCE_DIR / "build-inputs-attempt2.json").read_text())
    for _label, _fix in (("weekly", w_root), ("special", s_root)):
        _issue = WEEKLY_ISSUE if _label == "weekly" else SPECIAL_ISSUE
        _sr = _fix / f"surveys/{'weekly' if _label == 'weekly' else 'special'}/{_issue}"
        _pub = _fix / "sources" / _issue / "publication" / "v2"
        for _name in ("main.tex", "references.bib", "jgaisurvey.sty"):
            _fp = _sr / _name
            if not _fp.is_file() or _fp.is_symlink():
                print(f"{_label} pass2 output missing {_name}", file=sys.stderr); return 14
            _exp = _pass2_pins[_label]["trio"][_name]["fixture_sha256"]
            if sha256_file(_fp) != _exp:
                print(f"{_label} pass2 output drifted {_name}", file=sys.stderr); return 14
        _receipt = _pub / "validated-source-manifest.json"
        if not _receipt.is_file():
            print(f"{_label} receipt missing (pass2 incomplete)", file=sys.stderr); return 15
    (EVIDENCE / "pass2-reuse-verify.json").write_text(json.dumps(
        {"note": "attempt2 pass2 outputs reused after hash verification; no pass2 rerun",
         "weekly_receipt_sha256": sha256_file(w_root / "sources" / WEEKLY_ISSUE / "publication" / "v2" / "validated-source-manifest.json"),
         "special_receipt_sha256": sha256_file(s_root / "sources" / SPECIAL_ISSUE / "publication" / "v2" / "validated-source-manifest.json")}, indent=2))
    print("STAGE pass2-ok (reused verified attempt2 outputs)")
    # ---------- 3. disposable build dirs + exact trio copy ----------
    BUILDROOT.mkdir(parents=True, exist_ok=True)
    route_info = {}
    for label, fix, issue, survey_rel in (
            ("weekly", w_root, WEEKLY_ISSUE, f"surveys/weekly/{WEEKLY_ISSUE}"),
            ("special", s_root, SPECIAL_ISSUE, f"surveys/special/{SPECIAL_ISSUE}")):
        bdir = BUILDROOT / (f"{label}-build-attempt4")
        if bdir.exists():
            print(f"build dir exists {bdir}", file=sys.stderr); return 16
        bdir.mkdir(parents=True)
        sr = fix / survey_rel
        trio = {}
        for name in ("main.tex", "references.bib", "jgaisurvey.sty"):
            src = sr / name
            if not src.is_file() or src.is_symlink():
                print(f"{label} pass2 output missing {name}", file=sys.stderr); return 17
            trio[name] = {"fixture_sha256": sha256_file(src), "bytes": src.stat().st_size}
        latexmkrc = fix / ".latexmkrc"
        trio[".latexmkrc"] = {"fixture_sha256": sha256_file(latexmkrc), "bytes": latexmkrc.stat().st_size}
        # copy exact bytes
        for name in ("main.tex", "references.bib", "jgaisurvey.sty"):
            shutil.copyfile(sr / name, bdir / name)
        shutil.copyfile(latexmkrc, bdir / ".latexmkrc")
        # hash after copy
        for name in ("main.tex", "references.bib", "jgaisurvey.sty", ".latexmkrc"):
            h = sha256_file(bdir / name)
            trio[name]["build_sha256"] = h
            if h != trio[name]["fixture_sha256"] and name != ".latexmkrc":
                print(f"{label} copy hash mismatch {name}", file=sys.stderr); return 18
        # .latexmkrc equality is required too (declared recipe)
        if trio[".latexmkrc"]["build_sha256"] != trio[".latexmkrc"]["fixture_sha256"]:
            print(f"{label} latexmkrc copy mismatch", file=sys.stderr); return 18
        # census: build dir must contain exactly these 4 files (no legacy sections)
        census = sorted(p.name for p in bdir.iterdir() if p.is_file())
        (EVIDENCE / f"build-{label}-input-census.json").write_text(json.dumps(
            {"files": census, "trio": trio}, indent=2))
        if census != sorted([".latexmkrc", "jgaisurvey.sty", "main.tex", "references.bib"]):
            print(f"{label} build dir census unexpected {census}", file=sys.stderr); return 19
        route_info[label] = {"bdir": str(bdir), "survey_root": str(sr), "trio": trio,
                             "fixture": str(fix), "issue": issue}
    (EVIDENCE / "build-inputs.json").write_text(json.dumps(route_info, indent=2))
    print("STAGE build-dirs-ready")
    # ---------- 4. latexmk real builds ----------
    for label in ("weekly", "special"):
        info = route_info[label]
        bdir = Path(info["bdir"])
        epoch = epochs[label]
        env = dict(os.environ)
        env["PATH"] = str(TOOLBIN) + os.pathsep + env.get("PATH", "")
        env["TEXMFHOME"] = str(TOOLROOT / "texmf-home")
        env["TEXMFVAR"] = str(TOOLROOT / "texmf-var")
        env["TEXMFCONFIG"] = str(TOOLROOT / "texmf-config")
        env["TEXMFCACHE"] = str(TOOLROOT / "texmf-var")
        env["TEXDIR"] = str(TOOLROOT / "texlive")
        env["TEXLIVE_ROOT"] = str(TOOLROOT / "texlive")
        env["SOURCE_DATE_EPOCH"] = epoch
        if label == "weekly":
            env["FORCE_SOURCE_DATE"] = "1"
        (EVIDENCE / f"build-{label}-env.json").write_text(json.dumps(
            {k: env[k] for k in ("TEXMFHOME", "TEXMFVAR", "TEXMFCONFIG", "TEXMFCACHE", "TEXDIR",
                                 "TEXLIVE_ROOT", "SOURCE_DATE_EPOCH", "FORCE_SOURCE_DATE") if k in env},
            indent=2))
        cmd = ["latexmk", "-lualatex", "-synctex=1", "-interaction=nonstopmode",
               "-file-line-error", "-halt-on-error", "main.tex"]
        p, dt = run_capture(cmd, bdir, {k: env[k] for k in (
            "PATH", "TEXMFHOME", "TEXMFVAR", "TEXMFCONFIG", "TEXMFCACHE", "TEXDIR", "TEXLIVE_ROOT",
            "SOURCE_DATE_EPOCH", "FORCE_SOURCE_DATE") if k in env},
            f"build-{label}-stdout.txt", f"build-{label}-stderr.txt", f"build-{label}-exit.txt")
        (EVIDENCE / f"build-{label}-command.txt").write_text(" ".join(cmd) + f"\ncd {bdir}\nduration_s={dt:.1f}\n")
        info["build_exit"] = p.returncode
        info["build_duration_s"] = round(dt, 1)
        # census outputs (all files, incl aux/log/bbl/bcf/blg/run.xml/synctex)
        out_census = {}
        for q in sorted(bdir.rglob("*")):
            if q.is_file():
                out_census[str(q.relative_to(bdir))] = {"bytes": q.stat().st_size, "sha256": sha256_file(q)}
        (EVIDENCE / f"build-{label}-output-census.json").write_text(json.dumps(out_census, indent=2))
        info["output_files"] = sorted(out_census)
        if p.returncode != 0:
            print(f"{label} latexmk failed exit={p.returncode}; see build-{label}-stdout/stderr/log", file=sys.stderr)
            (EVIDENCE / f"build-{label}-failure-class.txt").write_text(
                f"engine FAIL exit={p.returncode}; no TeX edits made; minimal fix proposal requires log inspection by root\n")
            # do NOT proceed to transfer for failed route; continue other route then stop with error
            info["status"] = "BUILD_FAIL"
        else:
            info["status"] = "BUILT"
    (EVIDENCE / "build-results.json").write_text(json.dumps(route_info, indent=2))
    if any(route_info[l].get("status") != "BUILT" for l in ("weekly", "special")):
        print("one or both builds failed; stopping before transfer", file=sys.stderr); return 21
    print("STAGE builds-ok")
    # ---------- 5. workflow log gates ----------
    for label in ("weekly", "special"):
        info = route_info[label]
        log_text = (Path(info["bdir"]) / "main.log").read_text(encoding="utf-8", errors="replace")
        if label == "weekly":
            blocking = [l for l in log_text.splitlines() if re.search(
                r"LaTeX Warning: (There were undefined references|Citation .* undefined)|Package biblatex Warning: Please (re)?run|Overfull \\hbox|Underfull \\hbox|Missing character:", l)]
            (EVIDENCE / f"logcheck-{label}.txt").write_text("\n".join(blocking) + ("\n" if blocking else ""))
            info["log_blocking"] = blocking
            info["log_gate"] = "PASS" if not blocking else "FAIL"
        else:
            blocking = [l for l in log_text.splitlines() if re.search(
                r"LaTeX Warning: (There were undefined references|Citation .* undefined)|Package biblatex Warning: Please (re)?run|Missing character:", l)]
            layout = [l for l in log_text.splitlines() if re.search(r"Overfull \\hbox|Underfull \\hbox", l)]
            (EVIDENCE / f"logcheck-{label}-blocking.txt").write_text("\n".join(blocking) + ("\n" if blocking else ""))
            (EVIDENCE / f"logcheck-{label}-layout.txt").write_text("\n".join(layout) + ("\n" if layout else ""))
            info["log_blocking"] = blocking
            info["log_layout"] = layout
            info["log_gate"] = "PASS" if not blocking else "FAIL"
        m = re.findall(r"Output written on .*?\((\d+) pages?", log_text, re.S)
        info["page_count"] = int(m[-1]) if m else None
    (EVIDENCE / "logcheck-results.json").write_text(json.dumps(
        {l: {"log_gate": route_info[l]["log_gate"], "page_count": route_info[l].get("page_count"),
             "blocking_n": len(route_info[l].get("log_blocking", []))} for l in route_info}, indent=2))
    if any(route_info[l]["log_gate"] != "PASS" for l in route_info):
        print("log gate FAIL; stopping before transfer", file=sys.stderr); return 22
    print("STAGE logcheck-pass")
    # ---------- 6. stage digest + transfer ONLY 3 files ----------
    for label in ("weekly", "special"):
        info = route_info[label]
        bdir = Path(info["bdir"])
        pdf, lg = bdir / "main.pdf", bdir / "main.log"
        if not pdf.is_file() or pdf.stat().st_size == 0 or not lg.is_file() or lg.stat().st_size == 0:
            print(f"{label} missing pdf/log", file=sys.stderr); return 23
        digest = sha256_file(pdf) + "  main.pdf\n"
        dpath = bdir / "main.pdf.sha256"
        if dpath.exists():
            print(f"{label} staged digest exists", file=sys.stderr); return 24
        dpath.write_text(digest)
        info["staged"] = {"pdf_sha256": digest.split()[0], "pdf_bytes": pdf.stat().st_size,
                          "log_bytes": lg.stat().st_size}
        sr = Path(info["survey_root"])
        # preflight: all 3 destinations must be absent (fresh only, no overwrite)
        for name in ("main.pdf", "main.log", "main.pdf.sha256"):
            if (sr / name).exists() or os.path.lexists(sr / name):
                print(f"{label} destination {name} already exists; refusing overwrite", file=sys.stderr); return 25
        # expected hashes pre-recorded
        pre = {"main.pdf": sha256_file(pdf), "main.log": sha256_file(lg), "main.pdf.sha256": sha256_file(dpath)}
        (EVIDENCE / f"transfer-{label}-expected.json").write_text(json.dumps(pre, indent=2))
        shutil.copyfile(pdf, sr / "main.pdf")
        shutil.copyfile(lg, sr / "main.log")
        shutil.copyfile(dpath, sr / "main.pdf.sha256")
        post = {"main.pdf": sha256_file(sr / "main.pdf"), "main.log": sha256_file(sr / "main.log"),
                "main.pdf.sha256": sha256_file(sr / "main.pdf.sha256")}
        (EVIDENCE / f"transfer-{label}-actual.json").write_text(json.dumps(post, indent=2))
        if pre != post:
            print(f"{label} transfer hash mismatch", file=sys.stderr); return 26
        info["transfer"] = "OK"
    print("STAGE transfer-ok")
    # ---------- 7. post-transfer strict receipt + build-dir validation ----------
    for label, mod, route, issue in (("weekly", "survey_weekly_derivation_v2", "WEEKLY", WEEKLY_ISSUE),
                                     ("special", "survey_longform_derivation_v2", "LONGFORM", SPECIAL_ISSUE)):
        fix = Path(route_info[label]["fixture"])
        sr_rel = f"surveys/{'weekly' if label=='weekly' else 'special'}/{issue}"
        code = (
            "import sys,json,pathlib;"
            f"sys.path.insert(0,{str(fix)!r});"
            "import os;os.environ['PYTHONDONTWRITEBYTECODE']='1';"
            "from scripts import survey_production_v2 as core;"
            f"from scripts import {mod} as drv;"
            "from scripts import survey_reader_surface_gate_v2 as gate;"
            f"root=pathlib.Path({str(fix)!r});"
            f"receipt=root/'sources'/{issue!r}/'publication'/'v2'/'validated-source-manifest.json';"
            f"state=root/'sources'/{issue!r}/'production-state.json';"
            "drv.validate_receipt(root,receipt,state);"
            f"gate.validate_survey_build_directory(root,{sr_rel!r});"
            "print('RECEIPT_OK '+str(receipt.relative_to(root)));"
        )
        env = dict(os.environ); env["PYTHONDONTWRITEBYTECODE"] = "1"; env["PYTHONPATH"] = str(fix)
        p = subprocess.run([sys.executable, "-c", code], cwd=str(fix), capture_output=True, env=env, text=True)
        (EVIDENCE / f"receipt-{label}-stdout.txt").write_text(p.stdout or "")
        (EVIDENCE / f"receipt-{label}-stderr.txt").write_text(p.stderr or "")
        (EVIDENCE / f"receipt-{label}-exit.txt").write_text(str(p.returncode))
        log_cmd([sys.executable, "-c", f"validate_receipt+build_dir {label}"], str(fix), p.returncode)
        route_info[label]["receipt"] = "PASS" if p.returncode == 0 else f"FAIL: {(p.stderr or p.stdout)[:500]}"
        if p.returncode != 0:
            print(f"{label} receipt FAIL {(p.stderr or p.stdout)[:1000]}", file=sys.stderr); return 27
    (EVIDENCE / "build-results.json").write_text(json.dumps(route_info, indent=2))
    # source unchanged after build?
    for label, fix in (("weekly", w_root), ("special", s_root)):
        st = git(["status", "--porcelain=v1", "--untracked-files=all"], fix).stdout
        (EVIDENCE / f"{label}-status-after.txt").write_text(st)
    (EVIDENCE / "source-status-after.txt").write_text(git(["status", "--porcelain=v1", "--untracked-files=all"], SOURCE).stdout)
    print("STAGE receipt-ok")
    # ---------- 8. evidence packet PDFs/text/PNGs ----------
    for label in ("weekly", "special"):
        info = route_info[label]
        sr = Path(info["survey_root"])
        for name in ("main.pdf", "main.log", "main.pdf.sha256"):
            dst = EVIDENCE / f"{label}-{name}"
            must_absent(dst, "evidence packet copy")
            shutil.copyfile(sr / name, dst)
            assert sha256_file(dst) == sha256_file(sr / name)
        # text extraction + raster PNGs (real compiler PDF only)
        pdf = EVIDENCE / f"{label}-main.pdf"
        for args, oname in ((["pdftotext", "-layout", str(pdf), str(EVIDENCE / f"{label}-extracted.txt")], f"{label}-pdftotext"),
                            (["pdfinfo", str(pdf)], f"{label}-pdfinfo")):
            p = subprocess.run(args, capture_output=True, text=True)
            (EVIDENCE / f"{oname}-stdout.txt").write_text(p.stdout or "")
            (EVIDENCE / f"{oname}-stderr.txt").write_text(p.stderr or "")
            (EVIDENCE / f"{oname}-exit.txt").write_text(str(p.returncode))
            log_cmd(args, str(EVIDENCE_DIR), p.returncode)
        p = subprocess.run(["pdftoppm", "-png", "-r", "150", str(pdf), str(EVIDENCE / f"{label}-page")],
                           capture_output=True, text=True, cwd=str(EVIDENCE_DIR))
        (EVIDENCE / f"{label}-pdftoppm-stdout.txt").write_text(p.stdout or "")
        (EVIDENCE / f"{label}-pdftoppm-stderr.txt").write_text(p.stderr or "")
        (EVIDENCE / f"{label}-pdftoppm-exit.txt").write_text(str(p.returncode))
        log_cmd(["pdftoppm", "-png", "-r", "150", f"{label}-main.pdf", f"{label}-page"], str(EVIDENCE_DIR), p.returncode)
        if p.returncode != 0:
            print(f"{label} pdftoppm failed", file=sys.stderr); return 28
    (EVIDENCE / "final-report.json").write_text(json.dumps(route_info, indent=2))
    print("DONE pass2=2/2 build=2/2 logcheck=PASS transfer=3+3 receipt=PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
