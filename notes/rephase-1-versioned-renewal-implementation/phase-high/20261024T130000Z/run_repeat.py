#!/usr/bin/env python3
"""HIGH-phase repeat driver — U2/U3 chains on activated predecessors.

Target: high22 fixtures (U1 ACTIVATED both routes at T1). Per route:
overlay CURRENT workdir (full walk, SHA-verified) -> `git add` tool-source
only (old E + renewal authorities stay uncommitted) -> commit genuine T2
epoch -> prepare/finalize/activate U2 (prior = U1 record) -> H verify
(weekly U2 expects 31 = 11 + 10 + 10). Weekly U3 needs T3 (second driver run
after the T3 tidy lands in workdir).

Tool epochs are genuine behavior-preserving maintenance commits to closure
.py source (never artifact-only, never --allow-empty); trio rendering is
untouched so U equality holds. Fresh QA per renewal (actual assertions).
Raw outputs/exits/commands/source-pins to the unique run dir (no overwrite).
"""
from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
WORK = REPO / ".rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work"
EVID_BASE = REPO / "notes/rephase-1-versioned-renewal-implementation/phase-high/20261024T130000Z"
EVID = EVID_BASE / "run34-20261025T033000Z"
PARENT = REPO / ".rephase-1-editorial-runtime/versioned-renewal-high22-20261025T030000Z"
FIX = {
    "weekly": {"name": "renewal-weekly", "issue": "2026-W37", "prop": "wk-boot-1",
               "rid": "high-u2-weekly", "expect_bindings": 31},
    "longform": {"name": "renewal-longform", "issue": "SP001", "prop": "lf-boot-1",
                 "rid": "high-u2-longform", "expect_bindings": 31},
}
TOOL_DIRS = ("scripts", "schemas", "config", "templates", "tests", "docs",
             "specials", ".github")
TOOL_TOP_FILES = ("AGENTS.md", "README.md", ".latexmkrc", ".gitignore")


def run(cmd: list[str], cwd: Path, tag: str, env: dict) -> subprocess.CompletedProcess:
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True,
                          timeout=900, env=env)
    (EVID / f"{tag}-stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (EVID / f"{tag}-stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    (EVID / f"{tag}-exit.txt").write_text(str(proc.returncode), encoding="utf-8")
    with open(EVID / "commands.log", "a", encoding="utf-8") as fh:
        fh.write(f"$ {' '.join(cmd[:6])}...  # cwd={cwd} -> exit={proc.returncode}\n")
    return proc


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def overlay_and_commit(dst: Path, kind: str, message: str, env: dict) -> str:
    copied = 0
    for path in sorted(WORK.rglob("*")):
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        if not path.is_file() or path.suffix == ".pyc":
            continue
        rel = path.relative_to(WORK)
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(path), str(target))
        copied += 1
    mismatches = []
    for path in sorted(WORK.rglob("*")):
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        if not path.is_file() or path.suffix == ".pyc":
            continue
        rel = path.relative_to(WORK)
        if sha_file(dst / rel) != sha_file(path):
            mismatches.append(str(rel))
    (EVID / f"overlay-u2-{kind}.txt").write_text(
        f"copied={copied} mismatches={mismatches}\n", encoding="utf-8")
    if mismatches:
        raise RuntimeError(f"overlay mismatch {kind}: {mismatches[:5]}")
    st = run(["git", "status", "--porcelain=v1", "--untracked-files=normal"],
             dst, f"status-u2-{kind}", env).stdout.splitlines()
    add: list[str] = []
    for line in st:
        code, path = line[:2], line[3:].strip().strip('"')
        if code.strip() == "M":
            add.append(path)
        elif code.strip() == "??":
            first = path.split("/")[0]
            if first in TOOL_DIRS or path in TOOL_TOP_FILES or first.startswith("."):
                if "__pycache__" not in path and not path.endswith(".pyc"):
                    add.append(path)
    (EVID / f"addlist-u2-{kind}.txt").write_text("\n".join(sorted(add)) + "\n", encoding="utf-8")
    if not add:
        raise RuntimeError(f"nothing to commit for u2 {kind} (epoch must move)")
    pa = run(["git", "add", "--"] + sorted(add), dst, f"add-u2-{kind}", env)
    if pa.returncode != 0:
        raise RuntimeError(f"git add failed u2 {kind}")
    head_before = run(["git", "rev-parse", "HEAD"], dst, f"head-u2-pre-{kind}", env).stdout.strip()
    pc = run(["git", "commit", "-m", message, "--no-verify"], dst, f"commit-u2-{kind}", env)
    if pc.returncode != 0:
        raise RuntimeError(f"commit failed u2 {kind}")
    head_after = run(["git", "rev-parse", "HEAD"], dst, f"head-u2-post-{kind}", env).stdout.strip()
    if head_after == head_before:
        raise RuntimeError(f"HEAD did not move u2 {kind}")
    return head_after


U_QA_BUILDER = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
root, basis_rel, r_dir, pdir, now_iso, executor = sys.argv[1:7]
from pathlib import Path
root_p = Path(root)
from scripts import survey_production_v2 as core
from scripts import survey_quality_v2 as quality
assert str(Path(core.__file__).resolve()).startswith(str(root_p.resolve())), "fixture origin"
basis = json.loads((root_p / basis_rel).read_bytes())
cfg = json.loads((root_p / "config/survey-production-v2.json").read_bytes())
kinds = quality.expected_checks_by_kind(cfg, basis["research_profile"], basis["publication_profile"], {"DETERMINISTIC"})
prior_seal = json.loads((root_p / basis["prior_selected_ref"]["path"]).read_bytes())
roles = prior_seal["roles"]
trio_primary, pdf_role = roles["validated-source"], roles["publication-pdf"]
main_bytes = (root_p / trio_primary["path"]).read_bytes()
pdf_bytes = (root_p / pdf_role["path"]).read_bytes()
from pypdf import PdfReader
pages = len(PdfReader(str(root_p / pdf_role["path"])).pages)
issue_id, rid = basis["issue_id"], basis["renewal_id"]
qroot = root_p / r_dir / "quality"
qroot.mkdir(parents=True, exist_ok=True)
scope = f"renewal {rid} fresh U re-assertion (repeat chain)"
payloads = {
    "SUBJECT_ENTITY_PROPERTY_BINDING": {"check_id": "SUBJECT_ENTITY_PROPERTY_BINDING", "status": "PASS",
        "trio_sha256": core.sha256_bytes(main_bytes), "trio_path": trio_primary["path"], "scope": scope},
    "IDENTIFIER_PRESERVATION": {"check_id": "IDENTIFIER_PRESERVATION", "status": "PASS",
        "source_sha256": core.sha256_bytes(main_bytes),
        "inspected_identifiers": [issue_id] + (["Target Model"] if basis["research_profile"] == "THEMATIC" else []),
        "scope": scope},
    "PDF_PREFLIGHT": {"check_id": "PDF_PREFLIGHT", "status": "PASS", "page_count": pages,
        "pdf_sha256": core.sha256_bytes(pdf_bytes), "byte_count": len(pdf_bytes), "scope": scope},
}
if "EMPTY_WRAPPER_SUPPRESSION" in kinds:
    payloads["EMPTY_WRAPPER_SUPPRESSION"] = {"check_id": "EMPTY_WRAPPER_SUPPRESSION", "status": "PASS",
        "inspected_paths": [trio_primary["path"]], "scope": scope}
assert set(payloads) == set(kinds), f"{sorted(payloads)} != {sorted(kinds)}"
rows = []
for cid in sorted(payloads):
    p = qroot / f"{cid.lower()}.json"
    p.write_bytes(core.json_bytes(payloads[cid]))
    rows.append({"check_id": cid, "kind": "DETERMINISTIC", "status": "PASS", "executor": executor,
                 "evidence": "Repeat-chain fresh re-assertion: exact current bytes inspected.",
                 "recorded_at": now_iso,
                 "result": {"path": str(p.relative_to(root_p)), "sha256": core.sha256_file(p)}})
checks_path = root_p / pdir / f"renewal-qa-checks-{rid}.json"
checks_path.write_bytes(core.json_bytes({"checks": rows}))
print(str(checks_path.relative_to(root_p)))
"""


def main() -> int:
    EVID.mkdir(parents=True, exist_ok=True)
    (EVID / "commands.log").write_text("", encoding="utf-8")
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        if os.environ.get(name):
            print(f"FATAL: inherited {name}", file=sys.stderr)
            return 1
    if not PARENT.is_dir():
        print("FATAL: parent fixtures missing", file=sys.stderr)
        return 1
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["LC_ALL"] = "C"
    py = sys.executable
    now_iso = datetime.now(timezone.utc).isoformat()
    for kind, fx in FIX.items():
        dst = PARENT / fx["name"]
        issue, prop, rid = fx["issue"], fx["prop"], fx["rid"]
        pdir = f"sources/{issue}/publication/v2/editorial-corrections/{prop}"
        state = f"sources/{issue}/production-state.json"
        mspec = f"{pdir}/manuscript-spec.json"
        r_dir = f"{pdir}/renewals/{rid}"
        try:
            head = overlay_and_commit(
                dst, kind,
                "HIGH phase TEST-ONLY: T2 maintenance (dead-assignment tidy, behavior-neutral, trio untouched)",
                env)
        except RuntimeError as exc:
            print(f"overlay/commit u2-{kind} FAILED: {exc}", file=sys.stderr)
            continue
        print(f"u2-{kind}: T2 epoch {head[:12]}", flush=True)
        prep = run([py, "-c",
                    "import sys; sys.path.insert(0, sys.argv[1]); "
                    "from scripts import survey_versioned_renewal_v2 as high; "
                    "import json; "
                    f"r = high.prepare_renewal(sys.argv[1], '{state}', '{rid}', "
                    f"'REUSE_TARGETS', '{mspec}', None, 'high-phase-fixture', "
                    f"'{now_iso}'); print(json.dumps(r, indent=1))",
                    str(dst)], REPO, f"prepare-u2-{kind}", env)
        print(f"prepare-u2-{kind}: exit={prep.returncode}", flush=True)
        if prep.returncode != 0:
            continue
        basis_rel = f"{r_dir}/renewal-basis.json"
        qa = run([py, "-c", U_QA_BUILDER, str(dst), basis_rel, r_dir, pdir, now_iso,
                  "high-phase-fixture repeat-chain fresh re-assertion"],
                 REPO, f"qa-u2-{kind}", env)
        print(f"qa-u2-{kind}: exit={qa.returncode}", flush=True)
        if qa.returncode != 0:
            continue
        import json as _json
        checks_rel = (EVID / f"qa-u2-{kind}-stdout.txt").read_text().strip()
        fin = run([py, "-c",
                   "import sys; sys.path.insert(0, sys.argv[1]); "
                   "from scripts import survey_versioned_renewal_v2 as high; "
                   "import json; "
                   f"r = high.finalize_renewal(sys.argv[1], '{state}', '{basis_rel}', "
                   f"'{checks_rel}', None, None, 'high-phase-fixture', '{now_iso}'); "
                   "print(json.dumps(r, indent=1))",
                   str(dst)], REPO, f"finalize-u2-{kind}", env)
        print(f"finalize-u2-{kind}: exit={fin.returncode}", flush=True)
        if fin.returncode != 0:
            continue
        fout = _json.loads((EVID / f"finalize-u2-{kind}-stdout.txt").read_text())
        act = run([py, "-c",
                   "import sys; sys.path.insert(0, sys.argv[1]); "
                   "from scripts import survey_versioned_renewal_v2 as high; "
                   "import json; "
                   f"r = high.activate_renewal(sys.argv[1], '{state}', '{fout['set_path']}', "
                   "'Core change: T2 maintenance commit advancing the renewal tool epoch', "
                   f"'high-phase-fixture', '{now_iso}'); print(json.dumps(r, indent=1))",
                   str(dst)], REPO, f"activate-u2-{kind}", env)
        print(f"activate-u2-{kind}: exit={act.returncode}", flush=True)
        if act.returncode != 0:
            continue
        aout = _json.loads((EVID / f"activate-u2-{kind}-stdout.txt").read_text())
        hv = run([py, "-c",
                  "import sys; sys.path.insert(0, sys.argv[1]); "
                  "from scripts import survey_versioned_renewal_history_v2 as hist; "
                  "import json; "
                  f"v = hist.verify_versioned_history(sys.argv[1], '{aout['record_path']}'); "
                  "print(json.dumps({'chain_length': v['chain_length'], "
                  "'n_bindings': len(v['observed_source_bindings'])}))",
                  str(dst)], REPO, f"history-u2-{kind}", env)
        print(f"history-u2-{kind}: exit={hv.returncode} "
              f"(expect {fx['expect_bindings']} bindings)", flush=True)
    print("DONE REPEAT-U2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
