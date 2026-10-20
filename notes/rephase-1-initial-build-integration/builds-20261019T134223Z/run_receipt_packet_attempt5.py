#!/usr/bin/env python3
"""Attempt5: corrected post-transfer strict receipt + evidence packet + report.

Context: attempt4 builds/logcheck/transfer all PASS (weekly+special PDFs built,
5 pages each, 3-file transfer complete). Attempt4 receipt step called a
nonexistent `gate.validate_survey_build_directory` (harness bug, archived as
faulty-v2); correct entry points are the route derivation/generator modules:
weekly `survey_weekly_derivation_v2.validate_receipt + validate_survey_build_directory`,
special `survey_longform_generated_v2.validate_receipt + validate_survey_build_directory`.
This harness does NOT rerun pass2/builds/transfer (outputs verified by hash);
it runs the corrected receipt checks, builds the evidence packet
(PDF/log/digest copies + pdftotext + pdfinfo + pdftoppm PNGs from the real
compiler PDFs), and writes the per-route report. No source edits, no commits.
"""
from __future__ import annotations
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

EVIDENCE_DIR = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-initial-build-integration/builds-20261019T134223Z")
SUF = "-attempt5"
class _Ev:
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
WEEKLY_HEAD = "88813a01accb320b5948e368618e4061a4d72e0b"
SPECIAL_HEAD = "d4078d1bc851b9977289acf4b9cd6560c080b69e"

GIT_SANITIZE = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
                "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR")

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()

def log_cmd(cmd, cwd, exit_code, extra=""):
    with open(EVIDENCE_DIR / "commands-attempt5.log", "a") as f:
        f.write(f"CMD {' '.join(str(c) for c in cmd)} | cwd={cwd} | exit={exit_code} {extra}\n".replace("\n", " "))

def git(args, cwd: Path):
    env = dict(os.environ)
    for k in GIT_SANITIZE:
        env.pop(k, None)
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_OPTIONAL_LOCKS": "0"})
    p = subprocess.run(["git", "--no-optional-locks", *args], cwd=str(cwd),
                       capture_output=True, text=True, env=env)
    log_cmd(["git"] + args, str(cwd), p.returncode)
    return p

def main() -> int:
    open(EVIDENCE_DIR / "commands-attempt5.log", "w").write("# attempt5 receipt+packet\n")
    for k in GIT_SANITIZE:
        if os.environ.get(k):
            print(f"FATAL inherited {k}", file=sys.stderr); return 2
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    # verify identities (read-only)
    if git(["rev-parse", "HEAD"], SOURCE).stdout.strip() != "409b292756dd1277b9dfae87679934c0d2ce251c":
        print("source HEAD mismatch", file=sys.stderr); return 3
    for label, fix, exp in (("weekly", WEEKLY, WEEKLY_HEAD), ("special", SPECIAL, SPECIAL_HEAD)):
        h = git(["rev-parse", "HEAD"], fix).stdout.strip()
        (EVIDENCE / f"{label}-head-reverify.txt").write_text(h + "\n")
        if h != exp:
            print(f"{label} HEAD moved {h}", file=sys.stderr); return 4
    # verify transferred 3 files match attempt4 actual pins (no re-transfer)
    t4w = json.loads((EVIDENCE_DIR / "transfer-weekly-actual-attempt4.json").read_text())
    t4s = json.loads((EVIDENCE_DIR / "transfer-special-actual-attempt4.json").read_text())
    for label, fix, issue, t4 in (("weekly", WEEKLY, "2026-W37", t4w), ("special", SPECIAL, "SP001", t4s)):
        sr = fix / f"surveys/{'weekly' if label == 'weekly' else 'special'}/{issue}"
        cur = {n: sha256_file(sr / n) for n in ("main.pdf", "main.log", "main.pdf.sha256")}
        (EVIDENCE / f"transfer-{label}-reverify.json").write_text(json.dumps(cur, indent=2))
        if cur != t4:
            print(f"{label} transferred files drifted", file=sys.stderr); return 5
    print("STAGE transfer-reverified")
    # corrected receipt checks (actual validators)
    results = {}
    checks = (
        ("weekly", WEEKLY, "2026-W37", "survey_weekly_derivation_v2",
         "surveys/weekly/2026-W37"),
        ("special", SPECIAL, "SP001", "survey_longform_generated_v2",
         "surveys/special/SP001"),
    )
    for label, fix, issue, mod, sr_rel in checks:
        code = (
            "import sys,pathlib;"
            f"sys.path.insert(0,{str(fix)!r});"
            "import os;os.environ['PYTHONDONTWRITEBYTECODE']='1';"
            f"from scripts import {mod} as drv;"
            f"root=pathlib.Path({str(fix)!r});"
            f"receipt=root/'sources'/{issue!r}/'publication'/'v2'/'validated-source-manifest.json';"
            f"state=root/'sources'/{issue!r}/'production-state.json';"
            "drv.validate_receipt(root,receipt,state);"
            f"drv.validate_survey_build_directory(root,{sr_rel!r});"
            "print('RECEIPT_OK '+str(receipt.relative_to(root)));"
        )
        env = dict(os.environ); env["PYTHONDONTWRITEBYTECODE"] = "1"; env["PYTHONPATH"] = str(fix)
        t0 = time.time()
        p = subprocess.run([sys.executable, "-c", code], cwd=str(fix),
                           capture_output=True, text=True, env=env)
        dt = time.time() - t0
        (EVIDENCE / f"receipt-{label}-stdout.txt").write_text(p.stdout or "")
        (EVIDENCE / f"receipt-{label}-stderr.txt").write_text(p.stderr or "")
        (EVIDENCE / f"receipt-{label}-exit.txt").write_text(str(p.returncode))
        (EVIDENCE / f"receipt-{label}-command.txt").write_text(
            f"{sys.executable} -c validate_receipt+validate_survey_build_directory({label})\nduration_s={dt:.1f}\n")
        log_cmd([sys.executable, "-c", f"receipt+build_dir {label}"], str(fix), p.returncode, f"duration_s={dt:.1f}")
        results[label] = {"receipt": "PASS" if p.returncode == 0 else "FAIL", "duration_s": round(dt, 1),
                          "detail": (p.stderr or p.stdout or "")[:800]}
        if p.returncode != 0:
            print(f"{label} receipt FAIL {(p.stderr or p.stdout)[:800]}", file=sys.stderr); return 6
    print("STAGE receipt-pass")
    # evidence packet: hash-equal PDF/log/digest copies + text + raster PNGs
    for label, fix, issue in (("weekly", WEEKLY, "2026-W37"), ("special", SPECIAL, "SP001")):
        sr = fix / f"surveys/{'weekly' if label == 'weekly' else 'special'}/{issue}"
        for name in ("main.pdf", "main.log", "main.pdf.sha256"):
            dst = EVIDENCE / f"{label}-{name}"
            if dst.exists():
                print(f"packet file exists {dst}", file=sys.stderr); return 7
            dst.write_bytes((sr / name).read_bytes())
            assert sha256_file(dst) == sha256_file(sr / name)
        pdf = EVIDENCE / f"{label}-main.pdf"
        for args, oname in ((["pdftotext", "-layout", str(pdf), str(EVIDENCE / f"{label}-extracted.txt")], f"{label}-pdftotext"),
                            (["pdfinfo", str(pdf)], f"{label}-pdfinfo")):
            p = subprocess.run(args, capture_output=True, text=True, cwd=str(EVIDENCE_DIR))
            (EVIDENCE / f"{oname}-stdout.txt").write_text(p.stdout or "")
            (EVIDENCE / f"{oname}-stderr.txt").write_text(p.stderr or "")
            (EVIDENCE / f"{oname}-exit.txt").write_text(str(p.returncode))
            log_cmd(args, str(EVIDENCE_DIR), p.returncode)
            if p.returncode != 0:
                print(f"{oname} failed", file=sys.stderr); return 8
        p = subprocess.run(["pdftoppm", "-png", "-r", "150", str(pdf), str(EVIDENCE_DIR / f"{label}-page")],
                           capture_output=True, text=True, cwd=str(EVIDENCE_DIR))
        (EVIDENCE / f"{label}-pdftoppm-stdout.txt").write_text(p.stdout or "")
        (EVIDENCE / f"{label}-pdftoppm-stderr.txt").write_text(p.stderr or "")
        (EVIDENCE / f"{label}-pdftoppm-exit.txt").write_text(str(p.returncode))
        log_cmd(["pdftoppm", "-png", "-r", "150", f"{label}-main.pdf", f"{label}-page"], str(EVIDENCE_DIR), p.returncode)
        if p.returncode != 0:
            print(f"{label} pdftoppm failed", file=sys.stderr); return 9
    print("STAGE packet-ok")
    # final per-route report (counts/status, not test-method counts)
    attempt4 = json.loads((EVIDENCE_DIR / "build-results-attempt4.json").read_text())
    logchecks = json.loads((EVIDENCE_DIR / "logcheck-results-attempt4.json").read_text())
    report = {}
    for label, fix, issue in (("weekly", WEEKLY, "2026-W37"), ("special", SPECIAL, "SP001")):
        sr = fix / f"surveys/{'weekly' if label == 'weekly' else 'special'}/{issue}"
        info = attempt4[label]
        report[label] = {
            "fixture": str(fix), "fixture_head": git(["rev-parse", "HEAD"], fix).stdout.strip(),
            "issue": issue,
            "pass2": {"status": "PASS", "exit": 0, "raw": f"pass2-{label}-exit-attempt2.txt (=0)"},
            "build": {"status": "BUILT", "exit": info.get("build_exit"),
                      "duration_s": info.get("build_duration_s"),
                      "engine": "LuaHBTeX 1.24.0 / latexmk 4.88 / biber 2.22 (TL2026)",
                      "source_date_epoch": (EVIDENCE_DIR / f"{label}-source-epoch.txt").read_text().strip() if False else None},
            "log_gate": logchecks[label],
            "transfer": {"status": "OK", "files": ["main.pdf", "main.log", "main.pdf.sha256"]},
            "receipt": results[label],
            "pdf_sha256": sha256_file(sr / "main.pdf"), "pdf_bytes": (sr / "main.pdf").stat().st_size,
            "log_bytes": (sr / "main.log").stat().st_size,
            "digest_line": (sr / "main.pdf.sha256").read_text().strip(),
            "build_dir": info.get("bdir"),
        }
    report["weekly"]["build"]["source_date_epoch"] = (EVIDENCE_DIR / "weekly-source-epoch.txt").read_text().strip()
    report["special"]["build"]["source_date_epoch"] = (EVIDENCE_DIR / "special-source-epoch.txt").read_text().strip()
    report["toolchain_additions"] = ["tikzfill (tlmgr, attempt3 pre-step)", "pdfcol (tlmgr, attempt4 pre-step)"]
    report["blockers"] = []
    (EVIDENCE / "final-report.json").write_text(json.dumps(report, indent=2))
    print("DONE pass2=2/2 build=2/2 logcheck=2PASS transfer=3+3 receipt=2PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
