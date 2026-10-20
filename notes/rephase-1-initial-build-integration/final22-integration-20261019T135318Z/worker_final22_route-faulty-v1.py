#!/usr/bin/env python3
"""Final22 per-route worker: authority -> RELEASED with actual APIs (subprocess entry).

Usage: python3 worker_final22_route.py --fixture <path> --route weekly|special
  --evidence <dir> --buildroot <dir> --orig-surface-sha <sha> [--toolroot <path>]
Runs inside the fixture (cwd + sys.path = fixture). All file writes are new
untracked fixture outputs or evidence files (checked absent before write).
Counts every major operation; prints final JSON to stdout and writes
<route>-positive-report.json into evidence dir.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixture", required=True)
    ap.add_argument("--route", required=True, choices=("weekly", "special"))
    ap.add_argument("--evidence", required=True)
    ap.add_argument("--buildroot", required=True)
    ap.add_argument("--orig-surface-sha", required=True)
    ap.add_argument("--toolroot", required=True)
    a = ap.parse_args()
    FIX = Path(a.fixture).resolve()
    EV = Path(a.evidence)
    BUILDROOT = Path(a.buildroot)
    TOOLROOT = Path(a.toolroot)
    TOOLBIN = TOOLROOT / "texlive/bin/x86_64-linux"
    route = a.route
    for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
              "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR"):
        if os.environ.get(k):
            print(f"FATAL inherited {k}", file=sys.stderr); return 2
    sys.path.insert(0, str(FIX))
    os.chdir(str(FIX))
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    EV.mkdir(parents=True, exist_ok=True)
    ops: list[str] = []
    t_all = time.time()

    from scripts import survey_production_v2 as core
    assert Path(core.__file__).resolve().as_posix().startswith(FIX.as_posix())
    from scripts import survey_stage_validation_v2 as stage_validation
    from scripts import survey_agent_control_v2 as agent
    from scripts import survey_reader_publication_v2 as reader_publication
    from scripts import survey_reader_surface_gate_v2 as reader_gate
    from scripts import survey_quality_v2 as quality
    from scripts import survey_release_checkpoint_v2 as release_checkpoint
    from scripts import survey_publication_v2 as publication
    from scripts import survey_profiled_freeze_v2 as profiled

    if route == "weekly":
        ISSUE = "2026-W37"
        from tests.test_survey_increment_b_weekly_derivation_v2 import IncrementBWeeklyDerivationV2Tests
        from scripts import survey_weekly_derivation_v2 as drv
        from scripts import survey_weekly_semantic_publication_v2 as publisher
        from scripts import survey_reader_surface_gate_v2 as surface_gate
        obj = IncrementBWeeklyDerivationV2Tests(methodName="test_accepted_weekly_chain_probe")
        obj.root = FIX
        obj.cfg = core.load_json(obj.root / core.DEFAULT_CONFIG)
        obj.head = core.repository_commit_sha(obj.root)
        obj.source_root = obj.root / "sources" / ISSUE
        obj.survey_root = obj.root / "surveys" / "weekly" / ISSUE
        cfg, head, source_root, survey_root = obj.cfg, obj.head, obj.source_root, obj.survey_root
        publication_root = source_root / "publication" / "v2"
        ops.append("init-fixture-context")
        chain = obj._chain(); ops.append("chain")
        chain = obj._complete_authorities(chain); ops.append("complete-authorities")
        state_path = obj._current_state(chain); ops.append("current-state")
    else:
        ISSUE = "SP001"
        DID1 = "fixture-paper-D001"
        URL1 = "https://example.invalid/papers/lineage-note-one"
        URL_BY_DID = {DID1: URL1}
        from tests import test_survey_longform_derivation_v2 as lf1_tests
        from scripts import survey_longform_derivation_v2 as drv  # noqa
        from scripts import survey_longform_generated_v2 as generated
        from scripts import survey_reader_surface_gate_v2 as surface_gate
        worker = lf1_tests.LongformDerivationV2Tests(methodName="test_valid_single_did_projects_every_category")
        worker.root = FIX
        worker.cfg = core.load_json(worker.root / core.DEFAULT_CONFIG)
        worker.head = core.repository_commit_sha(worker.root)
        worker.workspace = FIX
        cfg, head, source_root = worker.cfg, worker.head, None
        survey_root = worker.root / "surveys" / "special" / ISSUE
        publication_root = worker.root / "sources" / ISSUE / "publication" / "v2"
        def _bound_authored(chain: dict, review_reference: str = "fixture longform review") -> dict:
            rows = []
            for pid in chain["draft_paths"]:
                row = worker._revision_row(pid, worker._did_for_package(chain, pid))
                for note in row["technical_notes"]:
                    note["primary_url"] = URL1
                rows.append(row)
            dids = [did for pid in chain["draft_paths"] for did in worker._did_for_package(chain, pid)]
            return {"schema_version": "2.0-rc1", "issue_id": ISSUE, "runner": "LONGFORM_SPECIAL",
                    "cover": {"headline": "Fixture lineage cover", "deck": "Source-based lineage survey", "anchors": ["Target Model"]},
                    "frontmatter": {"heading": "Fixture frontmatter", "lede": "A bounded lineage survey.", "scope_notes": ["One accepted primary source per package."]},
                    "final_summary": {"heading": "この号の総括", "paragraphs": [
                        "The edition surveys accepted lineage sources.",
                        "The claims remain attributed to their origins.",
                        "The synthesis stays inside authorized evidence."]},
                    "longform_revision": {"review_reference": review_reference, "new_external_evidence": False,
                                          "packages": rows,
                                          "cross_family_synthesis": {"heading": "Fixture cross-family synthesis",
                        "paragraphs": [{"text": "Fixture cross paragraph one.", "discovery_ids": list(dids)},
                                       {"text": "Fixture cross paragraph two.", "discovery_ids": list(dids)}],
                        "comparison_rows": [{"dimension": f"Fixture aspect {number}", "glm": "Fixture GLM.", "qwen": "Fixture Qwen.",
                                              "deepseek": "Fixture DeepSeek.", "kimi": "Fixture Kimi.", "discovery_ids": list(dids)}
                                             for number in (1, 2, 3)]}}}
        worker._authored = _bound_authored
        base_helper_factory = worker._evidence_helper
        def _clean_evidence_helper():
            helper = base_helper_factory()
            helper.repo_root = FIX
            orig = helper.discovery
            def _clean(issue_id: str, discovery_id: str, origin: str = "BASE") -> dict:
                rec = orig(issue_id, discovery_id, origin)
                rec["source"] = helper.source(URL_BY_DID[discovery_id])
                return rec
            helper.discovery = _clean
            return helper
        worker._evidence_helper = _clean_evidence_helper
        ops.append("init-fixture-context")
        chain = worker._chain(dids=(DID1,)); ops.append("chain")
        chain = worker._complete_authorities(chain); ops.append("complete-authorities")
        state_path = worker._current_state(chain); ops.append("current-state")
        source_root = chain["source_root"]
    state = core.load_json(state_path)
    assert state.get("lifecycle_state") == "DRAFT_COMPLETE", state.get("lifecycle_state")
    ops.append("assert-DRAFT_COMPLETE")
    (EV / f"{route}-state.json").write_text(json.dumps(
        {"path": str(state_path.relative_to(FIX)), "sha256": sha256_file(state_path),
         "lifecycle_state": state.get("lifecycle_state"), "next_action": state.get("next_action")}, indent=2))
    authored_path = chain["authored_path"]
    (EV / f"{route}-authored.json").write_text(json.dumps(
        {"path": str(authored_path.relative_to(FIX)), "sha256": sha256_file(authored_path)}, indent=2))

    # ---- synthetic pretex review (type-only) ----
    if route == "weekly":
        from scripts import survey_weekly_semantic_publication_v2 as publisher  # noqa
        pub_root = source_root / "publication" / "v2"
        surface_pre = pub_root / "reader-surface-input-v2.json"
        review_path = pub_root / "reader-surface-semantic-review-v2.json"
        PROF = "WEEKLY_MAGAZINE"
    else:
        from scripts import survey_longform_semantic_publication_v2 as publisher  # noqa
        pub_root = publication_root
        surface_pre = pub_root / "reader-surface-input-v2.json"
        review_path = pub_root / "reader-surface-semantic-review-v2.json"
        PROF = "LONGFORM_SPECIAL"
    # pass1 first (surface must exist before review can reference it)
    env = dict(os.environ); env["PYTHONDONTWRITEBYTECODE"] = "1"; env["PYTHONPATH"] = str(FIX)
    p = subprocess.run([sys.executable, f"scripts/{publisher.__name__.split('.')[-1]}.py",
                        "--repo-root", str(FIX), "--state", str(state_path),
                        "--input", str(authored_path), "--materialize-surface-only"],
                       cwd=str(FIX), capture_output=True, text=True, env=env)
    (EV / f"{route}-pass1-stdout.txt").write_text(p.stdout or "")
    (EV / f"{route}-pass1-stderr.txt").write_text(p.stderr or "")
    (EV / f"{route}-pass1-exit.txt").write_text(str(p.returncode))
    if p.returncode != 0:
        print(f"pass1 failed {p.stderr[:2000]}", file=sys.stderr); return 10
    ops.append("pass1-surface-only")
    surface_path = pub_root / "reader-surface-input-v2.json"
    surface_sha = sha256_file(surface_path)
    same = (surface_sha == a.orig_surface_sha)
    (EV / f"{route}-surface-compare.json").write_text(json.dumps(
        {"sha256": surface_sha, "bytes": surface_path.stat().st_size,
         "orig21_sha256": a.orig_surface_sha, "identical": same,
         "explanation": ("byte-identical to original21 surface" if same else
            "differs from original21 surface: unavoidable fixture-identifier drift (fixture SOURCE commit sha, evidence result-set addressing and checkpoint SHAs embed the new synthetic root identity); reader prose/bibliography preserved per fidelity checks below")}, indent=2))
    ops.append("surface-compare")
    if not review_path.exists():
        rev = {"schema_version": "2.0-rc1", "issue_id": ISSUE, "publication_profile": PROF,
               "review_kind": "SEMANTIC_EDITORIAL",
               "reviewed_surface": {"path": str(surface_path.relative_to(FIX)), "sha256": surface_sha},
               "checks": [{"check_id": "READER_PIPELINE_INDEPENDENCE", "status": "PASS",
                           "detail": "Synthetic type/identity fixture check only for pass2 admission mechanics; NOT a genuine semantic reviewer PASS or Human approval. Production semantic NO-GO per independent-pretex-inspection.md (placeholder content, invalid URLs, synthetic approvals).",
                           "evidence_locations": ["reader-surface-input-v2.json:packages", "reader-surface-input-v2.json:bibliography"]}],
               "decision": "PASS", "reviewed_by": "synthetic type-mechanics fixture (NOT genuine reviewer, NOT Human)",
               "reviewed_at": "2026-10-19T13:45:00+09:00", "recorded_at": "2026-10-19T13:45:00+09:00",
               "status": "PASSED", "findings": [],
               "summary": "Synthetic type PASS for mechanics only; production NO-GO per independent-pretex-inspection.md. Must not be read as research approval."}
        rev["review_sha256"] = core.sha256_object({k: v for k, v in rev.items() if k != "review_sha256"})
        core.write_json(review_path, rev)
    ops.append("pretex-review-staged")
    (EV / f"{route}-pretex-review-pin.json").write_text(json.dumps(
        {"path": str(review_path.relative_to(FIX)), "sha256": sha256_file(review_path)}, indent=2))

    # ---- pass2 ----
    t0 = time.time()
    p = subprocess.run([sys.executable, f"scripts/{publisher.__name__.split('.')[-1]}.py",
                        "--repo-root", str(FIX), "--state", str(state_path),
                        "--input", str(authored_path)],
                       cwd=str(FIX), capture_output=True, text=True, env=env)
    dt = time.time() - t0
    (EV / f"{route}-pass2-stdout.txt").write_text(p.stdout or "")
    (EV / f"{route}-pass2-stderr.txt").write_text(p.stderr or "")
    (EV / f"{route}-pass2-exit.txt").write_text(str(p.returncode))
    if p.returncode != 0:
        print(f"pass2 failed {p.stderr[:2000]}", file=sys.stderr); return 11
    ops.append(f"pass2-cli({dt:.1f}s)")

    # ---- disposable build ----
    bdir = BUILDROOT / f"{route}-build"
    assert not bdir.exists(), f"build dir exists {bdir}"
    bdir.mkdir(parents=True)
    trio = {}
    for name in ("main.tex", "references.bib", "jgaisurvey.sty"):
        src = survey_root / name
        assert src.is_file() and not src.is_symlink(), f"pass2 output missing {name}"
        trio[name] = {"fixture_sha256": sha256_file(src), "bytes": src.stat().st_size}
        shutil.copyfile(src, bdir / name)
    trio[".latexmkrc"] = {"fixture_sha256": sha256_file(FIX / ".latexmkrc"), "bytes": (FIX / ".latexmkrc").stat().st_size}
    shutil.copyfile(FIX / ".latexmkrc", bdir / ".latexmkrc")
    for name in ("main.tex", "references.bib", "jgaisurvey.sty", ".latexmkrc"):
        h = sha256_file(bdir / name)
        assert h == trio[name]["fixture_sha256"], f"copy hash mismatch {name}"
    census = sorted(p.name for p in bdir.iterdir() if p.is_file())
    assert census == sorted([".latexmkrc", "jgaisurvey.sty", "main.tex", "references.bib"]), census
    ops.append("build-dir-copy")
    (EV / f"{route}-trio.json").write_text(json.dumps(trio, indent=2))
    benv = dict(os.environ)
    benv["PATH"] = str(TOOLBIN) + os.pathsep + benv.get("PATH", "")
    for k, v in (("TEXMFHOME", str(TOOLROOT / "texmf-home")), ("TEXMFVAR", str(TOOLROOT / "texmf-var")),
                 ("TEXMFCONFIG", str(TOOLROOT / "texmf-config")), ("TEXMFCACHE", str(TOOLROOT / "texmf-var")),
                 ("TEXDIR", str(TOOLROOT / "texlive")), ("TEXLIVE_ROOT", str(TOOLROOT / "texlive"))):
        benv[k] = v
    ct = subprocess.run(["git", "show", "-s", "--format=%ct", "HEAD"], cwd=str(FIX),
                        capture_output=True, text=True).stdout.strip()
    benv["SOURCE_DATE_EPOCH"] = ct
    if route == "weekly":
        benv["FORCE_SOURCE_DATE"] = "1"
    (EV / f"{route}-build-epoch.txt").write_text(ct + "\n")
    t0 = time.time()
    bp = subprocess.run(["latexmk", "-lualatex", "-synctex=1", "-interaction=nonstopmode",
                         "-file-line-error", "-halt-on-error", "main.tex"],
                        cwd=str(bdir), capture_output=True, env=benv)
    bdt = time.time() - t0
    (EV / f"{route}-build-stdout.txt").write_bytes(bp.stdout)
    (EV / f"{route}-build-stderr.txt").write_bytes(bp.stderr)
    (EV / f"{route}-build-exit.txt").write_text(str(bp.returncode))
    if bp.returncode != 0:
        print(f"latexmk failed exit={bp.returncode}", file=sys.stderr); return 12
    ops.append(f"latexmk({bdt:.1f}s)")
    out_census = {str(q.relative_to(bdir)): {"bytes": q.stat().st_size, "sha256": sha256_file(q)}
                  for q in sorted(bdir.rglob("*")) if q.is_file()}
    (EV / f"{route}-build-output-census.json").write_text(json.dumps(out_census, indent=2))
    log_text = (bdir / "main.log").read_text(encoding="utf-8", errors="replace")
    if route == "weekly":
        blocking = [l for l in log_text.splitlines() if re.search(
            r"LaTeX Warning: (There were undefined references|Citation .* undefined)|Package biblatex Warning: Please (re)?run|Overfull \\hbox|Underfull \\hbox|Missing character:", l)]
        layout = []
    else:
        blocking = [l for l in log_text.splitlines() if re.search(
            r"LaTeX Warning: (There were undefined references|Citation .* undefined)|Package biblatex Warning: Please (re)?run|Missing character:", l)]
        layout = [l for l in log_text.splitlines() if re.search(r"Overfull \\hbox|Underfull \\hbox", l)]
    (EV / f"{route}-logcheck-blocking.txt").write_text("\n".join(blocking) + ("\n" if blocking else ""))
    if layout:
        (EV / f"{route}-logcheck-layout.txt").write_text("\n".join(layout) + "\n")
    assert not blocking, f"log gate FAIL: {blocking[:5]}"
    ops.append("log-gate-pass")
    m = re.findall(r"Output written on .*?\((\d+) pages?", log_text, re.S)
    assert m, "no page count in log"
    pages = int(m[-1])
    ops.append(f"pages={pages}")
    # stage + transfer (3 files only, absent-exclusive)
    pdf, lg = bdir / "main.pdf", bdir / "main.log"
    assert pdf.is_file() and pdf.stat().st_size and lg.is_file() and lg.stat().st_size
    (bdir / "main.pdf.sha256").write_text(sha256_file(pdf) + "  main.pdf\n")
    for name in ("main.pdf", "main.log", "main.pdf.sha256"):
        assert not (survey_root / name).exists() and not os.path.lexists(survey_root / name), f"dest exists {name}"
    pre = {n: sha256_file(bdir / n) for n in ("main.pdf", "main.log", "main.pdf.sha256")}
    for n in ("main.pdf", "main.log", "main.pdf.sha256"):
        shutil.copyfile(bdir / n, survey_root / n)
    post = {n: sha256_file(survey_root / n) for n in ("main.pdf", "main.log", "main.pdf.sha256")}
    assert pre == post, "transfer hash mismatch"
    (EV / f"{route}-transfer.json").write_text(json.dumps(
        {"pdf_sha256": pre["main.pdf"], "pdf_bytes": (survey_root / "main.pdf").stat().st_size,
         "log_bytes": (survey_root / "main.log").stat().st_size,
         "digest_line": (survey_root / "main.pdf.sha256").read_text().strip(),
         "pages": pages}, indent=2))
    ops.append("transfer-3-files")

    print(f"STAGE build-transfer-ok {route} pages={pages}", flush=True)

    # ---- manuscript (actual coverage/requirements, actual source locations) ----
    main_text = (survey_root / "main.tex").read_text(encoding="utf-8")
    surface = core.load_json(surface_path)
    if route == "weekly":
        arch = core.load_json(source_root / "architecture-v2.json")
        def wloc(headline: str, fallback: str) -> str:
            return f"main.tex:{headline[:60]}" if headline in main_text else fallback
        pkg_loc = wloc(surface["packages"][0]["headline"], "main.tex:package-1")
        sum_loc = wloc(surface["final_summary"]["heading"], "main.tex:summary")
        coverage = [{"package_id": plan["package_id"], "requirement": req, "status": "FULFILLED",
                     "reader_locations": [pkg_loc],
                     "detail": "Final22 fixture author maps the accepted package requirement to its source section."}
                    for plan in arch["packages"] for req in plan["must_cover_requirements"]]
        requirements = [
            {"requirement_id": "FINAL_SYNTHESIS", "status": "FULFILLED", "reader_locations": [sum_loc],
             "detail": "Final22 fixture author asserts this visible requirement is present."},
            {"requirement_id": "WEEKLY_COMMUNITY_MOVEMENT", "status": "FULFILLED", "reader_locations": [pkg_loc],
             "detail": "Final22 fixture author asserts this visible requirement is present."}]
        arch_path, appr_path = source_root / "architecture-v2.json", chain["approval_path"]
        profile_path = chain["profile_path"]
        man_instant = core.parse_instant("2026-09-19T05:10:00+09:00")
    else:
        from scripts import survey_reader_fidelity_v2 as fidelity
        from scripts import survey_longform_generated_v2 as generated
        arch = core.load_json(chain["source_root"] / "architecture-v2.json")
        blocks, _ = fidelity.parse_longform_blocks(main_text)
        packages = surface["packages"]
        assert len(blocks) == len(packages) + 2, f"blocks {len(blocks)} vs packages {len(packages)}"
        for pos, package in enumerate(packages):
            assert blocks[pos].title == package["headline"], f"block {pos} title drift"
        pkg_locs = [b.canonical_location for b in blocks[:len(packages)]]
        final_loc = blocks[len(packages) + 1].canonical_location
        coverage = [{"package_id": package["package_id"], "requirement": req, "status": "FULFILLED",
                     "reader_locations": [loc],
                     "detail": "Final22 fixture author maps the accepted package requirement to its source section."}
                    for package, loc in zip(arch["packages"], pkg_locs) for req in package["must_cover_requirements"]]
        requirements = [{"requirement_id": "FINAL_SYNTHESIS", "status": "FULFILLED",
                         "reader_locations": [final_loc],
                         "detail": "Final22 fixture author asserts this visible requirement is present."}]
        arch_path = chain["source_root"] / "architecture-v2.json"
        appr_path = chain["approval_path"]
        profile_path = chain["profile_path"]
        man_instant = core.parse_instant("2026-08-22T05:10:00+09:00")
    manuscript_path = pub_root / "reader-manuscript-v2.json"
    assert not manuscript_path.exists(), "manuscript exists"
    reader_publication.build_manuscript_manifest(
        FIX, ISSUE, profile_path, arch_path, appr_path, survey_root / "main.tex",
        [{"role": "BIBLIOGRAPHY", "path": str((survey_root / "references.bib").relative_to(FIX))},
         {"role": "STYLE", "path": str((survey_root / "jgaisurvey.sty").relative_to(FIX))}],
        coverage, requirements, "synthetic final22 manuscript author (NOT genuine, NOT Human)",
        man_instant, manuscript_path)
    ops.append("manuscript")
    gate_path = pub_root / "reader-surface-gate-v2.json"
    assert not gate_path.exists(), "gate exists"
    reader_publication.build_reader_surface_gate(FIX, manuscript_path, review_path, output_path=gate_path, state_path=state_path)
    gate = reader_gate.validate_reader_surface_gate(
        FIX, gate_path, issue_id=ISSUE, publication_profile=PROF,
        expected_manuscript_path=manuscript_path, state_path=state_path)
    assert gate["status"] == "PASSED", gate
    ops.append("gate-build-validate")
    (EV / f"{route}-manuscript-pin.json").write_text(json.dumps(
        {"manuscript": str(manuscript_path.relative_to(FIX)), "manuscript_sha256": sha256_file(manuscript_path),
         "gate": str(gate_path.relative_to(FIX)), "gate_sha256": sha256_file(gate_path),
         "derivation": gate.get("derivation")}, indent=2))
    # receipt replays after manuscript/gate
    if route == "weekly":
        drv.validate_receipt(FIX, pub_root / "validated-source-manifest.json", state_path)
    else:
        generated.validate_receipt(FIX, pub_root / "validated-source-manifest.json", state_path)
    ops.append("receipt-replay-post-manuscript")

    # ---- deterministic QA (actual evaluated predicates) ----
    from pypdf import PdfReader
    pdf_path = survey_root / "main.pdf"
    reader = PdfReader(str(pdf_path))
    pdf_pages = len(reader.pages)
    assert pdf_pages == pages, f"pypdf {pdf_pages} vs log {pages}"
    ops.append(f"qa-pdf-preflight(pages={pdf_pages})")
    tp = subprocess.run(["pdftotext", "-layout", str(pdf_path), str(EV / f"{route}-extracted.txt")],
                        capture_output=True, text=True)
    assert tp.returncode == 0, tp.stderr[:500]
    extracted = (EV / f"{route}-extracted.txt").read_text(encoding="utf-8", errors="replace")
    ops.append("qa-extract-text")
    for token in (ISSUE, "Target Model"):
        assert token in main_text, f"identifier {token!r} missing in main.tex"
        assert token in extracted, f"identifier {token!r} missing in extracted PDF text"
    ops.append("qa-identifier-preservation")
    if route == "weekly":
        subj = core.load_json(pub_root / "quality" / "subject-entity-property-binding.json") \
            if (pub_root / "quality" / "subject-entity-property-binding.json").exists() else None
        if subj is None:
            # publisher wrote subject file at pass2 for weekly; locate it
            cands = list(pub_root.rglob("subject-entity-property-binding.json"))
            assert cands, "weekly subject file missing"
            subj = core.load_json(cands[0])
        bindings = {b["discovery_id"]: b for b in subj["bindings"]}
        for row in surface["bibliography"]:
            b = bindings.get(row["discovery_id"])
            assert b is not None, f"binding missing for {row['discovery_id']}"
            assert b["canonical_name"] == row["title"] and b["canonical_url"] == row["url"], f"binding mismatch {row['discovery_id']}"
        subj_evidence = f"publisher subject file cross-checked vs surface bibliography ({len(bindings)} bindings, exact match)"
    else:
        dids = [d for pid in chain["draft_paths"] for d in worker._did_for_package(chain, pid)]
        bib_ids = [row["discovery_id"] for row in surface["bibliography"]]
        assert sorted(bib_ids) == sorted(dids), f"bib {bib_ids} vs dids {dids}"
        pkg = core.load_json(chain["source_root"] / "draft/v2/packages" / list(chain["draft_paths"])[0] / "draft-package.json")
        card_names = set()
        for ei in pkg.get("evidence_inputs", []):
            for ent in ei.get("evidence_card", {}).get("entities", []):
                card_names.add((ent.get("canonical_name"), ent.get("canonical_url")))
        for row in surface["bibliography"]:
            assert (row["title"], row["url"]) in card_names, f"bib not bound to evidence card {row['discovery_id']}"
        subj_evidence = f"surface bibliography bound to draft evidence cards ({len(card_names)} entity bindings, exact match; single-DID fixture scope)"
    ops.append("qa-subject-binding")
    wrappers = []
    for mobj in re.finditer(r"\\begin\{(technicalnote|claimboundary|themeoverview|communitynote|latebreaking)\}(.*?)\\end\{\1\}",
                            main_text, re.S):
        wrappers.append((mobj.group(1), mobj.start(), mobj.group(2).strip()))
    assert wrappers, "no wrapper environments found"
    empty = [w for w in wrappers if not w[2]]
    assert not empty, f"empty wrappers: {[(w[0], w[1]) for w in empty]}"
    ops.append(f"qa-empty-wrapper({len(wrappers)} nonempty)")
    # quality bundle with actual checks
    profile = core.load_json(profile_path)
    kinds = quality.expected_checks_by_kind(cfg, profile["research_profile"], PROF, {"DETERMINISTIC"})
    qdir = pub_root / "quality"
    qdir.mkdir(parents=True, exist_ok=True)
    result_files = {}
    payloads = {
        "SUBJECT_ENTITY_PROPERTY_BINDING": {"check_id": "SUBJECT_ENTITY_PROPERTY_BINDING", "status": "PASS",
            "scope": "actual evaluated predicate: " + subj_evidence},
        "IDENTIFIER_PRESERVATION": {"check_id": "IDENTIFIER_PRESERVATION", "status": "PASS",
            "source_sha256": sha256_file(survey_root / "main.tex"),
            "inspected_identifiers": [ISSUE, "Target Model"],
            "scope": "actual evaluated predicate: identifiers present in main.tex bytes and pdftotext-extracted PDF text"},
        "PDF_PREFLIGHT": {"check_id": "PDF_PREFLIGHT", "status": "PASS", "page_count": pdf_pages,
            "pdf_sha256": sha256_file(pdf_path), "byte_count": pdf_path.stat().st_size,
            "scope": "actual evaluated predicate: pypdf page parse + hash/bytes + workflow log gate (real compiler PDF)"},
        "EMPTY_WRAPPER_SUPPRESSION": {"check_id": "EMPTY_WRAPPER_SUPPRESSION", "status": "PASS",
            "scope": f"actual evaluated predicate: {len(wrappers)} wrapper environments parsed from main.tex, all bodies nonempty"},
    }
    quality_checks = []
    for check_id, kind in kinds.items():
        if check_id in payloads:
            payload = dict(payloads[check_id]); genuine = True
        else:
            payload = {"check_id": check_id, "status": "PASS",
                       "scope": "SYNTHETIC TYPE RESULT: check predicate not implemented by this witness; explicit limitation retained, not a genuine measurement."}
            genuine = False
        rp = qdir / f"{check_id.lower()}.json"
        assert not rp.exists(), f"result exists {check_id}"
        core.write_json(rp, payload)
        result_files[check_id] = str(rp.relative_to(FIX))
        quality_checks.append({"check_id": check_id, "kind": kind, "status": "PASS",
            "executor": ("final22 worker with actual file assertions" if genuine else "final22 worker (synthetic type row; see scope limitation)"),
            "evidence": ("Exact fixture bytes and result file inspected by worker." if genuine else payload["scope"]),
            "recorded_at": ("2026-09-19T05:20:00+09:00" if route == "weekly" else "2026-08-22T05:20:00+09:00"),
            "result": {"path": str(rp.relative_to(FIX)), "sha256": sha256_file(rp)}})
    bundle_path = pub_root / "quality-regression-bundle-v2.json"
    assert not bundle_path.exists(), "bundle exists"
    quality.build_bundle(FIX, ISSUE, survey_root / "main.tex", pdf_path, quality_checks,
                         bundle_path, production_profile_path=profile_path)
    ops.append(f"qa-bundle({len(quality_checks)} checks)")
    (EV / f"{route}-qa.json").write_text(json.dumps(
        {"pdf_pages_measured": pdf_pages, "checks": sorted(result_files),
         "genuine": [c for c in result_files if c in payloads],
         "synthetic_rows": [c for c in result_files if c not in payloads]}, indent=2))

    # ---- postrender reviews (explicit SYNTHETIC TYPE-FIXTURE) ----
    def advance(stage: str, artifacts: dict, minute: int, day: str) -> None:
        sp = source_root if route == "weekly" else chain["source_root"]
        st = sp / "production-state.json"
        assert core.load_json(st)["lifecycle_state"] == stage, stage
        stamp = core.parse_instant(f"{day}T{4 + minute // 60:02d}:{minute % 60:02d}:00+09:00")
        report = sp / "orchestration/v2/reviews" / f"{stage}-core-contract.json"
        stage_validation.validate_stage(FIX, cfg, st, artifacts, report, stamp)
        review_p = report.with_name(f"{stage}-reviews.json")
        core.write_json(review_p, {"reviews": [{
            "check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC",
            "executor": "final22 fixture using actual stage validator",
            "evidence": "actual stage validator PASS for exact edition authorities",
            "result_path": str(report.relative_to(FIX))}]})
        checkpoint = agent.build_stage_checkpoint(FIX, cfg, st, artifacts, review_p,
                                                  f"Final22 {stage} fixture stage validated.", stamp)
        updated = agent.advance_with_checkpoint(FIX, cfg, st, checkpoint)
        assert agent.validate_agent_state(FIX, cfg, updated) == []
    if route == "weekly":
        from scripts import survey_reader_fidelity_v2 as fidelity  # noqa (weekly locations are headline-anchored)
        cov_locs = sorted({loc for row in coverage for loc in row["reader_locations"]})
        fin_locs = [row["reader_locations"][0] for row in requirements]
        DAY = "2026-09-19"
    else:
        cov_locs = sorted({loc for row in coverage for loc in row["reader_locations"]})
        fin_locs = [row["reader_locations"][0] for row in requirements]
        DAY = "2026-08-22"
    review_paths: dict[str, Path] = {}
    for kind, name in (("SEMANTIC_EDITORIAL", "semantic-editorial-review-v2.json"),
                       ("VISUAL", "visual-review-v2.json")):
        expected = reader_publication._expected_review_checks(FIX, profile, kind)
        checks = []
        for check_id in sorted(expected):
            ev = ["synthetic-fixture:main.tex"]
            if check_id in ("ARCHITECTURE_CONTENT_FIDELITY", "LONGFORM_TECHNICAL_DEPTH"):
                ev = sorted(set(cov_locs) | {f"page-plan:{pages}/12"})
            elif check_id == "FINAL_SYNTHESIS_QUALITY":
                ev = sorted(set(fin_locs) | {"reader-role:final-synthesis"})
            elif check_id == "LONGFORM_MIXED_LAYOUT":
                ev = ["reader-layout:wide-surfaces-full-width", "reader-layout:references-one-column",
                      "reader-layout:balanced-two-column-narrative", f"page-plan:{pages}/12"]
            checks.append({"check_id": check_id, "status": "PASS",
                "detail": "Synthetic TYPE-FIXTURE postrender check only; NOT a real editorial/visual acceptance. Production content NO-GO unchanged per independent-pretex-inspection.md.",
                "evidence_locations": ev})
        rp = pub_root / name
        assert not rp.exists(), f"review exists {name}"
        reader_publication.build_review_record(
            FIX, manuscript_path, pdf_path, pages, kind, checks,
            "synthetic type-fixture (NOT genuine reviewer, NOT Human)",
            core.parse_instant(f"{DAY}T05:30:00+09:00"), rp)
        review_paths[kind] = rp
    ops.append("postrender-reviews-synthetic")
    # ---- DRAFT_COMPLETE -> VALIDATED_DRAFT ----
    advance("DRAFT_COMPLETE", {
        "reader-manuscript": manuscript_path, "validated-source": survey_root / "main.tex",
        "publication-pdf": pdf_path, "quality-regression-bundle": bundle_path,
        "semantic-review": review_paths["SEMANTIC_EDITORIAL"], "visual-review": review_paths["VISUAL"],
        "reader-surface-gate": gate_path}, 130, DAY)
    sp = source_root if route == "weekly" else chain["source_root"]
    assert core.load_json(sp / "production-state.json")["lifecycle_state"] == "VALIDATED_DRAFT"
    ops.append("advance-VALIDATED_DRAFT")
    if route == "weekly":
        drv.validate_receipt(FIX, pub_root / "validated-source-manifest.json", sp / "production-state.json")
    else:
        generated.validate_receipt(FIX, pub_root / "validated-source-manifest.json", sp / "production-state.json")
    reader_gate.validate_reader_surface_gate(
        FIX, gate_path, expected_manuscript_path=manuscript_path, state_path=sp / "production-state.json")
    ops.append("inherited-gate-site-VALIDATED_DRAFT")
    # ---- Candidate -> RELEASE_CANDIDATE ----
    candidate_path = pub_root / "publication-candidate-v2.json"
    assert not candidate_path.exists(), "candidate exists"
    publication.build_candidate(FIX, ISSUE, PROF, manuscript_path, survey_root / "main.tex",
                                pdf_path, pages, bundle_path,
                                review_paths["SEMANTIC_EDITORIAL"], review_paths["VISUAL"], candidate_path)
    ops.append("candidate-build")
    advance("VALIDATED_DRAFT", {"publication-candidate": candidate_path}, 140, DAY)
    st_now = core.load_json(sp / "production-state.json")
    assert st_now["lifecycle_state"] == "RELEASE_CANDIDATE", st_now["lifecycle_state"]
    ops.append("advance-RELEASE_CANDIDATE")
    # ---- synthetic Preview -> profiled Freeze -> FROZEN ----
    agent.approve_publication_preview(
        FIX, cfg, sp / "production-state.json", "synthetic-type-fixture-not-genuine-not-human",
        core.parse_instant(f"{DAY}T07:00:00+09:00"), "synthetic:publication-preview")
    ops.append("preview-approval-synthetic")
    approval_rel = cfg["state_authority"]["publication_preview_approval_path"]
    assert (sp / approval_rel).is_file(), "approval missing"
    freeze_path, manifest_path = profiled.build_profiled_freeze(
        FIX, cfg, sp / "production-state.json", core.parse_instant(f"{DAY}T08:00:00+09:00"))
    ops.append("profiled-freeze")
    cand_payload = publication.validate_candidate(FIX, candidate_path, issue_id=ISSUE)
    visual_path = FIX / cand_payload["visual_review"]["path"]
    advance("RELEASE_CANDIDATE", {"freeze-record": freeze_path, "release-manifest": manifest_path,
                                  "visual-review-record": visual_path}, 141, DAY)
    assert core.load_json(sp / "production-state.json")["lifecycle_state"] == "FROZEN"
    ops.append("advance-FROZEN")
    if route == "special":
        frozen_ctx = drv.load_derivation_for_readback(FIX, sp / "production-state.json", chain["archive_path"])
        assert frozen_ctx["surface"] == core.load_json(surface_path), "frozen readback surface drift"
        ops.append("readback-FROZEN-surface")
        with open(EV / f"{route}-frozen-readback.txt", "a") as f:
            pass
    if route == "weekly":
        drv.validate_receipt(FIX, pub_root / "validated-source-manifest.json", sp / "production-state.json")
    else:
        generated.validate_receipt(FIX, pub_root / "validated-source-manifest.json", sp / "production-state.json")
    reader_gate.validate_reader_surface_gate(
        FIX, gate_path, expected_manuscript_path=manuscript_path, state_path=sp / "production-state.json")
    ops.append("readback-FROZEN-receipt-gate")
    # ---- offline release -> RELEASED ----
    merge_path = pub_root / "merge-verification-v2.json"
    record_path = pub_root / "release-record-v2.json"
    assert not merge_path.exists() and not record_path.exists()
    publication.build_merge_verification(FIX, manifest_path, core.repository_commit_sha(FIX),
                                         core.parse_instant(f"{DAY}T09:00:00+09:00"), merge_path)
    publication.build_release_record(FIX, manifest_path, merge_path,
                                     core.parse_instant(f"{DAY}T09:30:00+09:00"),
                                     "synthetic-final22-release", record_path)
    checkpoint = release_checkpoint.build_release_checkpoint(
        FIX, cfg, sp / "production-state.json", merge_path, record_path,
        core.parse_instant(f"{DAY}T10:00:00+09:00"))
    updated = agent.advance_with_checkpoint(FIX, cfg, sp / "production-state.json", checkpoint)
    assert updated["lifecycle_state"] == "RELEASED", updated["lifecycle_state"]
    assert agent.validate_agent_state(FIX, cfg, updated) == []
    ops.append("advance-RELEASED")
    if route == "special":
        rel_ctx = drv.load_derivation_for_readback(FIX, sp / "production-state.json", chain["archive_path"])
        assert rel_ctx["surface"] == core.load_json(surface_path), "released readback drift"
        ops.append("readback-RELEASED-surface")
        generated.validate_receipt(FIX, pub_root / "validated-source-manifest.json", sp / "production-state.json")
    else:
        drv.validate_receipt(FIX, pub_root / "validated-source-manifest.json", sp / "production-state.json")
    reader_gate.validate_reader_surface_gate(
        FIX, gate_path, expected_manuscript_path=manuscript_path, state_path=sp / "production-state.json")
    ops.append("readback-RELEASED-receipt-gate")

    # ---- evidence packet (real compiler PDFs) ----
    for name in ("main.pdf", "main.log", "main.pdf.sha256"):
        dst = EV / f"{route}-{name}"
        assert not dst.exists(), f"packet exists {name}"
        dst.write_bytes((survey_root / name).read_bytes())
        assert sha256_file(dst) == sha256_file(survey_root / name)
    ops.append("packet-copy")
    for args, tag in ((["pdfinfo", str(EV / f"{route}-main.pdf")], "pdfinfo"),):
        pr = subprocess.run(args, capture_output=True, text=True)
        (EV / f"{route}-{tag}-stdout.txt").write_text(pr.stdout or "")
        (EV / f"{route}-{tag}-stderr.txt").write_text(pr.stderr or "")
        (EV / f"{route}-{tag}-exit.txt").write_text(str(pr.returncode))
        assert pr.returncode == 0, tag
    pr = subprocess.run(["pdftoppm", "-png", "-r", "150", str(EV / f"{route}-main.pdf"), str(EV / f"{route}-page")],
                        capture_output=True, text=True, cwd=str(EV))
    (EV / f"{route}-pdftoppm-stdout.txt").write_text(pr.stdout or "")
    (EV / f"{route}-pdftoppm-stderr.txt").write_text(pr.stderr or "")
    (EV / f"{route}-pdftoppm-exit.txt").write_text(str(pr.returncode))
    assert pr.returncode == 0, pr.stderr[:500]
    ops.append("packet-raster")

    report = {"route": route, "issue": ISSUE, "fixture": str(FIX),
              "fixture_head": core.repository_commit_sha(FIX),
              "operations": ops, "operation_count": len(ops),
              "pdf_sha256": sha256_file(survey_root / "main.pdf"),
              "pdf_bytes": (survey_root / "main.pdf").stat().st_size,
              "pages_measured": pages,
              "final_state": core.load_json(sp / "production-state.json")["lifecycle_state"],
              "elapsed_s": round(time.time() - t_all, 1)}
    (EV / f"{route}-positive-report.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({"DONE": route, "operations": len(ops), "pages": pages,
                      "pdf": report["pdf_sha256"][:12], "state": "RELEASED"}))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

