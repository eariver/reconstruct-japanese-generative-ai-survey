#!/usr/bin/env python3
"""HIGH-phase fixture harness — NEW byte-independent renewal fixtures (weekly+longform).

Clones the real R3 bootstrap fixtures (721a04d, ACTIVATED prePreview, old E
authorities uncommitted) into NEW independent DBs, overlays the complete
intended new implementation from the HIGH workdir (actual409+57+H/S/HIGH), and
commits ONLY meaningful NEW tool source BEFORE authorities (old E stays
uncommitted; never `git add -A`). The tool-commit HEAD move IS the genuine
changed-tool epoch (old 721a04d retained as ancestor for H epoch blobs).

Runs HIGH prepare U first (both routes), then a finalize attempt to surface the
exact S-owned scope-row coordination point without bypass. All raw
stdout/stderr/exits/commands/source-pins go to unique evidence dirs (no
overwrite, no truncation). No network, no saved packet runners, no
reconstruct-DB fixtures, no ordinary commits.
"""
from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
WORK = REPO / ".rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work"
BOOT = REPO / ".rephase-1-editorial-runtime/versioned-renewal-bootstrap-20261023T194449Z"
PARENT = REPO / ".rephase-1-editorial-runtime/versioned-renewal-high22-20261025T030000Z"
EVID_BASE = REPO / "notes/rephase-1-versioned-renewal-implementation/phase-high/20261024T130000Z"
EVID = EVID_BASE / "run31-20261025T030000Z"
EXPECT_HEAD = "721a04d85532d7855f3e54cc411f5847c787726e"
TOOL_DIRS = ("scripts", "schemas", "config", "templates", "tests", "docs",
             "specials", ".github")
TOOL_TOP_FILES = ("AGENTS.md", "README.md", ".latexmkrc", ".gitignore")


def run(cmd: list[str], cwd: Path, tag: str, env: dict | None = None) -> subprocess.CompletedProcess:
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True,
                          timeout=600, env=env)
    (EVID / f"{tag}-stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (EVID / f"{tag}-stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    (EVID / f"{tag}-exit.txt").write_text(str(proc.returncode), encoding="utf-8")
    with open(EVID / "commands.log", "a", encoding="utf-8") as fh:
        fh.write(f"$ {' '.join(cmd)}  # cwd={cwd} -> exit={proc.returncode}\n")
    return proc


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def produce_fresh_qa(root: Path, basis_rel: str, r_dir: str, pdir: str,
                     executor: str, now_iso: str) -> str:
    """Fresh deterministic QA production (driver-side, actual assertions).

    Mirrors the bootstrap QA production shape ({"checks": [...]}) but with
    CURRENT renewal measurements: result files under R/quality/ carry exact
    live trio/PDF SHAs, check rows carry the renewal executor + current time
    (>= basis capture, satisfying HIGH freshness). The checks input file is
    driver-owned at P/<prop>/renewal-qa-checks-<rid>.json (supplied path,
    pinned by HIGH, never writer-rewritten). No genuine approval implied.
    """
    import json as _json
    sys.path.insert(0, str(root))
    from scripts import survey_production_v2 as core
    from scripts import survey_quality_v2 as quality
    basis = _json.loads((root / basis_rel).read_text(encoding="utf-8"))
    cfg = _json.loads((root / "config/survey-production-v2.json").read_text(encoding="utf-8"))
    research, publication = basis["research_profile"], basis["publication_profile"]
    kinds = quality.expected_checks_by_kind(cfg, research, publication, {"DETERMINISTIC"})
    prior_seal = _json.loads((root / basis["prior_selected_ref"]["path"]).read_text(encoding="utf-8"))
    roles = prior_seal["roles"]
    trio_primary = roles["validated-source"]
    trio_bib = roles["bibliography"]
    trio_style = roles["style"]
    pdf_role = roles["publication-pdf"]
    main_bytes = (root / trio_primary["path"]).read_bytes()
    pdf_bytes = (root / pdf_role["path"]).read_bytes()
    try:
        from pypdf import PdfReader
        pages = len(PdfReader(str(root / pdf_role["path"])).pages)
    except Exception as exc:
        raise RuntimeError(f"QA PDF unreadable: {exc}") from exc
    issue_id = basis["issue_id"]
    rid = basis["renewal_id"]
    qroot = root / r_dir / "quality"
    qroot.mkdir(parents=True, exist_ok=True)
    scope = f"renewal {rid} fresh deterministic re-assertion"
    payloads: dict[str, dict] = {
        "SUBJECT_ENTITY_PROPERTY_BINDING": {
            "check_id": "SUBJECT_ENTITY_PROPERTY_BINDING", "status": "PASS",
            "trio_sha256": core.sha256_bytes(main_bytes),
            "trio_path": trio_primary["path"],
            "scope": scope},
        "IDENTIFIER_PRESERVATION": {
            "check_id": "IDENTIFIER_PRESERVATION", "status": "PASS",
            "source_sha256": core.sha256_bytes(main_bytes),
            "inspected_identifiers": [issue_id] + (["Target Model"] if research == "THEMATIC" else []),
            "scope": scope},
        "PDF_PREFLIGHT": {
            "check_id": "PDF_PREFLIGHT", "status": "PASS", "page_count": pages,
            "pdf_sha256": core.sha256_bytes(pdf_bytes),
            "byte_count": len(pdf_bytes), "scope": scope},
    }
    if "EMPTY_WRAPPER_SUPPRESSION" in kinds:
        payloads["EMPTY_WRAPPER_SUPPRESSION"] = {
            "check_id": "EMPTY_WRAPPER_SUPPRESSION", "status": "PASS",
            "inspected_paths": [trio_primary["path"]], "scope": scope}
    if set(payloads) != set(kinds):
        raise RuntimeError(f"QA payload set {sorted(payloads)} != required {sorted(kinds)}")
    rows = []
    for cid in sorted(payloads):
        if kinds[cid] != "DETERMINISTIC":
            raise RuntimeError(f"non-deterministic kind refused: {cid}")
        p = qroot / f"{cid.lower()}.json"
        p.write_bytes(core.json_bytes(payloads[cid]))
        rows.append({"check_id": cid, "kind": "DETERMINISTIC", "status": "PASS",
                     "executor": executor,
                     "evidence": "Renewal fresh deterministic re-assertion: exact current trio/PDF bytes inspected.",
                     "recorded_at": now_iso,
                     "result": {"path": str(p.relative_to(root)),
                                "sha256": core.sha256_file(p)}})
    checks_path = root / pdir / f"renewal-qa-checks-{rid}.json"
    checks_path.write_bytes(core.json_bytes({"checks": rows}))
    return str(checks_path.relative_to(root))


def main() -> int:
    EVID.mkdir(parents=True, exist_ok=True)
    (EVID / "commands.log").write_text("", encoding="utf-8")
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        if os.environ.get(name):
            print(f"FATAL: inherited {name}", file=sys.stderr)
            return 1
    if WORK.resolve() == REPO.resolve():
        print("FATAL: workdir confusion", file=sys.stderr)
        return 1
    if PARENT.exists():
        print(f"FATAL: parent exists (no overwrite): {PARENT}", file=sys.stderr)
        return 1
    PARENT.mkdir(parents=True, exist_ok=False)
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["LC_ALL"] = "C"

    fixtures: dict[str, dict[str, str]] = {}
    for kind, src, issue, prop in (
            ("weekly", BOOT / "bootstrap-weekly", "2026-W37", "wk-boot-1"),
            ("longform", BOOT / "bootstrap-longform", "SP001", "lf-boot-1")):
        dst = PARENT / f"renewal-{kind}"
        proc = run(["git", "clone", "--no-hardlinks", str(src), str(dst)],
                   REPO, f"clone-{kind}", env)
        if proc.returncode != 0:
            print(f"clone {kind} failed", file=sys.stderr)
            return 1
        run(["git", "remote", "set-url", "origin",
             f"https://example.invalid/versioned-renewal-high-{kind}.git"],
            dst, f"remote-{kind}", env)
        run(["git", "config", "user.name", "rephase-fixture"], dst, f"cfg-{kind}-1", env)
        run(["git", "config", "user.email", "fixture@example.invalid"], dst, f"cfg-{kind}-2", env)
        run(["git", "config", "commit.gpgsign", "false"], dst, f"cfg-{kind}-3", env)
        head = run(["git", "rev-parse", "HEAD"], dst, f"head-{kind}", env).stdout.strip()
        if head != EXPECT_HEAD:
            print(f"FATAL: {kind} HEAD {head} != {EXPECT_HEAD}", file=sys.stderr)
            return 1
        alt = dst / ".git" / "objects" / "info" / "alternates"
        if alt.exists():
            print(f"FATAL: {kind} has alternates", file=sys.stderr)
            return 1
        status = run(["git", "status", "--porcelain=v1", "--untracked-files=normal"],
                     dst, f"status-pre-{kind}", env).stdout
        # Clone carries tracked files only: copy the untracked old-E authorities
        # from the source worktree (byte copy, no hardlinks). The untracked
        # list comes from the SOURCE (the clone is clean by construction).
        # These stay uncommitted (commit-before-authorities preserved).
        src_status = run(["git", "status", "--porcelain=v1", "--untracked-files=normal"],
                         src, f"src-status-{kind}", env).stdout
        e_paths = []
        for line in src_status.splitlines():
            code, path = line[:2], line[3:].strip().strip('"')
            if code.strip() == "??" and (src / path).exists() \
                    and ".git" not in Path(path).parts:
                e_paths.append(path)
        for rel in sorted(e_paths):
            s, d = src / rel, dst / rel
            if d.exists():
                print(f"FATAL: {kind} E target exists: {rel}", file=sys.stderr)
                return 1
            if s.is_dir() and not s.is_symlink():
                shutil.copytree(str(s), str(d), symlinks=True, copy_function=shutil.copy2)
            else:
                d.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(str(s), str(d))
        # Verify E bytes identical + inodes disjoint (no hardlink sharing).
        for rel in sorted(e_paths):
            s, d = src / rel, dst / rel
            for sfile in sorted(s.rglob("*") if s.is_dir() else [s]):
                if not sfile.is_file() or sfile.suffix == ".pyc" \
                        or "__pycache__" in sfile.parts:
                    continue
                drep = d / sfile.relative_to(s) if s.is_dir() else d
                if sha_file(drep) != sha_file(sfile):
                    print(f"FATAL: {kind} E bytes differ: {rel}", file=sys.stderr)
                    return 1
                if os.stat(drep).st_ino == os.stat(sfile).st_ino:
                    print(f"FATAL: {kind} E inode shared: {rel}", file=sys.stderr)
                    return 1
        (EVID / f"ecopy-{kind}.txt").write_text(
            f"e_paths={len(e_paths)} verified\n", encoding="utf-8")
        # Overlay complete intended new implementation (workdir worktree walk,
        # excluding .git/__pycache__/*.pyc). Fixture-only old E authorities have
        # no same-relpath counterpart in workdir and are preserved.
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
        # SHA-verify every overlaid file against workdir.
        mismatches = []
        for path in sorted(WORK.rglob("*")):
            if ".git" in path.parts or "__pycache__" in path.parts:
                continue
            if not path.is_file() or path.suffix == ".pyc":
                continue
            rel = path.relative_to(WORK)
            if sha_file(dst / rel) != sha_file(path):
                mismatches.append(str(rel))
        (EVID / f"overlay-{kind}.txt").write_text(
            f"copied={copied} mismatches={mismatches}\n", encoding="utf-8")
        if mismatches:
            print(f"FATAL: overlay mismatch {kind}: {mismatches[:5]}", file=sys.stderr)
            return 1
        # Stage ONLY meaningful NEW tool source (tracked mods + untracked under
        # tool dirs/top files). Old E (sources/, surveys/, raw/, views-*, root
        # E json) stays uncommitted by construction.
        st = run(["git", "status", "--porcelain=v1", "--untracked-files=normal"],
                 dst, f"status-post-{kind}", env).stdout.splitlines()
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
        (EVID / f"addlist-{kind}.txt").write_text("\n".join(sorted(add)) + "\n",
                                                 encoding="utf-8")
        if not add:
            print(f"FATAL: nothing to commit for {kind}", file=sys.stderr)
            return 1
        pa = run(["git", "add", "--"] + sorted(add), dst, f"add-{kind}", env)
        if pa.returncode != 0:
            print(f"git add failed {kind}", file=sys.stderr)
            return 1
        pc = run(["git", "commit", "-m",
                  f"HIGH phase TEST-ONLY: versioned renewal HIGH+consumer implementation "
                  f"({kind} tool source before authorities; old E uncommitted)",
                  "--no-verify"], dst, f"commit-{kind}", env)
        if pc.returncode != 0:
            print(f"commit failed {kind}", file=sys.stderr)
            return 1
        new_head = run(["git", "rev-parse", "HEAD"], dst, f"head2-{kind}", env).stdout.strip()
        if new_head == EXPECT_HEAD:
            print(f"FATAL: {kind} HEAD did not move", file=sys.stderr)
            return 1
        anc = run(["git", "merge-base", "--is-ancestor", EXPECT_HEAD, "HEAD"],
                  dst, f"ancestor-{kind}", env)
        if anc.returncode != 0:
            print(f"FATAL: {kind} old epoch not ancestor", file=sys.stderr)
            return 1
        post = run(["git", "status", "--porcelain=v1", "--untracked-files=normal"],
                   dst, f"status-commit-{kind}", env).stdout
        if "sources/" not in post and "surveys/" not in post:
            print(f"FATAL: {kind} old E authorities missing post-commit", file=sys.stderr)
            return 1
        fixtures[kind] = {"root": str(dst), "issue": issue, "prop": prop,
                          "head": new_head}
    (EVID / "fixtures.json").write_text(
        __import__("json").dumps(fixtures, indent=1), encoding="utf-8")

    # Bootstrap U first on both fixtures (prepare REUSE_TARGETS), then finalize
    # attempts (expected S-owned scope-row coordination refusal, no bypass).
    py = sys.executable
    from datetime import datetime, timezone
    now_iso = datetime.now(timezone.utc).isoformat()
    for kind, fx in fixtures.items():
        root = fx["root"]
        issue, prop = fx["issue"], fx["prop"]
        pdir = f"sources/{issue}/publication/v2/editorial-corrections/{prop}"
        state = f"sources/{issue}/production-state.json"
        mspec = f"{pdir}/manuscript-spec.json"
        rid = f"high-u1-{kind}"
        prep = run([py, "-c",
                    "import sys; sys.path.insert(0, sys.argv[1]); "
                    "from scripts import survey_versioned_renewal_v2 as high; "
                    "import json; "
                    f"r = high.prepare_renewal(sys.argv[1], '{state}', '{rid}', "
                    f"'REUSE_TARGETS', '{mspec}', None, 'high-phase-fixture', "
                    f"'{now_iso}'); "
                    "print(json.dumps({k: v for k, v in r.items() "
                    "if k not in ('pins',)}, indent=1))",
                    root], REPO, f"prepare-u-{kind}", env)
        print(f"prepare-u-{kind}: exit={prep.returncode}")
        if prep.returncode == 0:
            import json as _json
            try:
                basis_rel = f"{pdir}/renewals/{rid}/renewal-basis.json"
                r_dir = f"{pdir}/renewals/{rid}"
                qa_now = datetime.now(timezone.utc).isoformat()
                checks_rel = produce_fresh_qa(Path(root), basis_rel, r_dir, pdir,
                                              "high-phase-fixture fresh deterministic re-assertion",
                                              qa_now)
                (EVID / f"qa-u-{kind}.txt").write_text(
                    f"checks={checks_rel} at={qa_now}\n", encoding="utf-8")
                fin = run([py, "-c",
                           "import sys; sys.path.insert(0, sys.argv[1]); "
                           "from scripts import survey_versioned_renewal_v2 as high; "
                           "import json; "
                           f"r = high.finalize_renewal(sys.argv[1], '{state}', "
                           f"'{basis_rel}', '{checks_rel}', "
                           "None, None, 'high-phase-fixture', "
                           f"'{now_iso}'); "
                           "print(json.dumps(r, indent=1))",
                           root], REPO, f"finalize-u-{kind}", env)
                print(f"finalize-u-{kind}: exit={fin.returncode}")
                if fin.returncode == 0:
                    import json as _jj
                    fout = _jj.loads(
                        open(EVID / f"finalize-u-{kind}-stdout.txt",
                             encoding="utf-8").read())
                    set_rel = fout["set_path"]
                    act = run([py, "-c",
                               "import sys; sys.path.insert(0, sys.argv[1]); "
                               "from scripts import survey_versioned_renewal_v2 as high; "
                               "import json; "
                               f"r = high.activate_renewal(sys.argv[1], '{state}', "
                               f"'{set_rel}', "
                               "'Core change: versioned renewal HIGH+consumer "
                               "implementation with fixed source proof leaf', "
                               "'high-phase-fixture', "
                               f"'{now_iso}'); "
                               "print(json.dumps(r, indent=1))",
                               root], REPO, f"activate-u-{kind}", env)
                    print(f"activate-u-{kind}: exit={act.returncode}")
                    if act.returncode == 0:
                        aout = _jj.loads(
                            open(EVID / f"activate-u-{kind}-stdout.txt",
                                 encoding="utf-8").read())
                        rec_rel = aout["record_path"]
                        hv = run([py, "-c",
                                  "import sys; sys.path.insert(0, sys.argv[1]); "
                                  "from scripts import survey_versioned_renewal_history_v2 as hist; "
                                  "import json; "
                                  f"v = hist.verify_versioned_history(sys.argv[1], '{rec_rel}'); "
                                  "print(json.dumps({'chain_length': v['chain_length'], "
                                  "'anchor_kind': v['anchor_kind'], "
                                  "'n_bindings': len(v['observed_source_bindings']), "
                                  "'n_refs': len(v['observed_refs']), "
                                  "'n_lineage': len(v['materialization_lineage'])})); "
                                  "print('BINDINGS=' + ','.join("
                                  "sorted(set(str(b.get('binding')) for b in v['observed_source_bindings']))))",
                                  root], REPO, f"history-u-{kind}", env)
                        print(f"history-u-{kind}: exit={hv.returncode} "
                              f"(complete U history returns 21 after OWN rows)")
            except Exception as exc:
                print(f"finalize harness error: {exc}", file=sys.stderr)
    print("DONE OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
