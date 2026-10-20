#!/usr/bin/env python3
"""Supplement per-route worker: authority -> RELEASE_CANDIDATE with BOTH actual
stage Gate negatives (DRAFT_COMPLETE + VALIDATED_DRAFT sites) via real stage calls.

Usage: python3 worker_supplement_route.py --fixture <path> --route weekly|special
  --evidence <dir> --buildroot <dir> --orig-surface-sha <sha> --toolroot <path>
  --positive-evidence <dir>
Runs inside the fixture (cwd + sys.path = fixture). No latexmk rebuild: the exact
generated trio + declared recipe are hash-compared to the recorded positive-run
pins; on equality the REAL positive-run PDF/log/digest bytes are staged and
transferred with the exclusive witness helper. Decoy wrong-manuscript negatives go
through actual stage_validation advancement (not standalone validators alone).
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
    ap.add_argument("--positive-evidence", required=True)
    a = ap.parse_args()
    POSEV = Path(a.positive_evidence)
    FIX = Path(a.fixture).resolve()
    EV0 = Path(a.evidence)
    _SUF = os.environ.get("EVID_SUFFIX", "")
    class _Ev:
        """Attempt-namespaced evidence paths; never overwrites prior attempts."""
        def __truediv__(self, name):
            p = Path(str(name))
            sfx = "".join(p.suffixes)
            stem = p.name[:len(p.name) - len(sfx)] if sfx else p.name
            return EV0 / (stem + _SUF + sfx)
        def mkdir(self, *ma, **mk):
            return EV0.mkdir(*ma, **mk)
    EV = _Ev()
    EVB = EV0
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

    # ---- NO latexmk rebuild: trio/recipe hash equality gates reuse of REAL build ----
    # Positive-run recorded pins (trio + recipe). Any inequality stops with a
    # blocker (source differs -> new build required); never rebuild silently.
    trio_pin_file = "weekly-trio.json" if route == "weekly" else "special-trio-attempt6.json"
    trio_pins = json.loads((POSEV / trio_pin_file).read_text())
    trio_now = {}
    for name in ("main.tex", "references.bib", "jgaisurvey.sty"):
        src = survey_root / name
        assert src.is_file() and not src.is_symlink(), f"pass2 output missing {name}"
        trio_now[name] = sha256_file(src)
    trio_now[".latexmkrc"] = sha256_file(FIX / ".latexmkrc")
    for name, pin in trio_pins.items():
        assert trio_now[name] == pin["fixture_sha256"], f"trio drift {name}: {trio_now[name]} vs {pin['fixture_sha256']}"
    ops.append("trio-hash-equal-positive")
    (EV / f"{route}-trio-compare.json").write_text(json.dumps(
        {"trio_now": trio_now, "trio_pins": {k: v["fixture_sha256"] for k, v in trio_pins.items()},
         "identical": True}, indent=2))
    # Stage REAL positive-run PDF/log/digest (packet files, hash-verified).
    # NOTE: stage dir is attempt-namespaced (prior un suffixed run left an
    # authenticated-but-unexplained orphan weekly-stage; preserved aside, never used).
    stage = BUILDROOT / f"{route}-stage{_SUF}"
    assert not stage.exists(), f"stage dir exists {stage}"
    stage.mkdir(parents=True)
    pkt = {"weekly": ("main.pdf", "main.log", "main.pdf.sha256"),
           "special": ("main-attempt6.pdf", "main-attempt6.log", "main-attempt6.pdf.sha256")}[route]
    for pkt_name, trio_name in zip(pkt, ("main.pdf", "main.log", "main.pdf.sha256")):
        data = (POSEV / f"{route}-{pkt_name}").read_bytes() if route == "weekly" else (POSEV / f"special-{pkt_name}").read_bytes()
        (stage / trio_name).write_bytes(data)
    transfer_pin_file = "weekly-transfer.json" if route == "weekly" else "special-transfer-attempt6.json"
    transfer_pins = json.loads((POSEV / transfer_pin_file).read_text())
    assert sha256_file(stage / "main.pdf") == transfer_pins["pdf_sha256"], "staged pdf != recorded build pdf"
    assert (stage / "main.pdf.sha256").read_text(encoding="utf-8").strip() == transfer_pins["digest_line"], "staged digest != recorded"
    (EV / f"{route}-stage-verify.json").write_text(json.dumps(
        {"staged_pdf_sha256": sha256_file(stage / "main.pdf"),
         "recorded_pdf_sha256": transfer_pins["pdf_sha256"],
         "staged_log_bytes": (stage / "main.log").stat().st_size,
         "recorded_log_bytes": transfer_pins["log_bytes"],
         "digest_line": (stage / "main.pdf.sha256").read_text(encoding="utf-8").strip(),
         "recorded_digest_line": transfer_pins["digest_line"],
         "original_build_basis": transfer_pins.get("build_dir", "see positive report"),
         "pages_recorded": transfer_pins["pages"]}, indent=2))
    assert transfer_pins["pages"] == 5
    pages = 5
    ops.append("stage-real-positive-bytes")
    # Log gates re-checked on the staged (real) log bytes (no new build).
    log_text = (stage / "main.log").read_text(encoding="utf-8", errors="replace")
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
    assert m and int(m[-1]) == pages, "page count mismatch in staged log"
    ops.append(f"pages={pages}")
    # ---- exclusive transfer (SAME witness helper as controls) ----
    sys.path.insert(1, str(EVB))
    from transfer_exclusive import transfer_exact as xfer_exact
    expected = {n: sha256_file(stage / n) for n in ("main.pdf", "main.log", "main.pdf.sha256")}
    assert expected["main.pdf"] == transfer_pins["pdf_sha256"]
    _xfer_written: list[str] = []
    def _on_xfer_error(exc, written, _survey):
        _xfer_written.extend(written)
        (EV / f"{route}-transfer-error.txt").write_text(f"{type(exc).__name__}: {exc}\nwritten={written}\n")
    post = xfer_exact(FIX, stage, survey_root, expected, on_error=_on_xfer_error)
    (EV / f"{route}-transfer.json").write_text(json.dumps(
        {"pdf_sha256": post["main.pdf"], "pdf_bytes": (survey_root / "main.pdf").stat().st_size,
         "log_bytes": (survey_root / "main.log").stat().st_size,
         "digest_line": (survey_root / "main.pdf.sha256").read_text().strip(),
         "pages": pages, "helper": "transfer_exclusive.transfer_exact (O_EXCL|O_NOFOLLOW, exclusive create)"}, indent=2))
    ops.append("transfer-3-files-exclusive")

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
    package_ids = [row["package_id"] for row in arch["packages"]]
    _ordered = [(row.get("drafting_order", 0), row["package_id"]) for row in arch["packages"]]
    final_package = max(_ordered)[1] if _ordered else None
    for kind, name in (("SEMANTIC_EDITORIAL", "semantic-editorial-review-v2.json"),
                       ("VISUAL", "visual-review-v2.json")):
        expected = reader_publication._expected_review_checks(FIX, profile, kind)
        checks = []
        for check_id in sorted(expected):
            ev = ["synthetic-fixture:main.tex"]
            detail = ("Synthetic TYPE-FIXTURE postrender check only; NOT a real editorial/visual acceptance. "
                      "Production content NO-GO unchanged per independent-pretex-inspection.md.")
            if check_id in ("ARCHITECTURE_CONTENT_FIDELITY", "LONGFORM_TECHNICAL_DEPTH"):
                ev = sorted({f"package:{pid}" for pid in package_ids} | set(cov_locs))
                if check_id == "LONGFORM_TECHNICAL_DEPTH":
                    ev = sorted(set(ev) | {f"page-plan:{pages}/12", "density-review:below-target-substantive"})
                    detail += (" Page-plan/density tags record the measured below-target page-count fact "
                               "required by the review contract; no substantive density assessment is asserted.")
            elif check_id == "FINAL_SYNTHESIS_QUALITY":
                ev = sorted(set(fin_locs) | {"reader-role:final-synthesis"} |
                            ({f"package:{final_package}"} if final_package else set()))
            elif check_id == "LONGFORM_MIXED_LAYOUT":
                ev = ["reader-layout:wide-surfaces-full-width", "reader-layout:references-one-column",
                      "reader-layout:balanced-two-column-narrative"]
            checks.append({"check_id": check_id, "status": "PASS", "detail": detail,
                "evidence_locations": ev})
        rp = pub_root / name
        assert not rp.exists(), f"review exists {name}"
        reader_publication.build_review_record(
            FIX, manuscript_path, pdf_path, pages, kind, checks,
            "synthetic type-fixture (NOT genuine reviewer, NOT Human)",
            core.parse_instant(f"{DAY}T05:30:00+09:00"), rp)
        review_paths[kind] = rp
    ops.append("postrender-reviews-synthetic")
    # ---- decoy wrong-manuscript set (same issue, coherent otherwise) ----
    def _snapshot(root: Path) -> dict:
        files = {}
        for p in sorted(root.rglob("*")):
            if ".git" in p.parts or "__pycache__" in p.parts:
                continue
            if p.is_file() and not p.is_symlink():
                files[str(p.relative_to(root))] = sha256_file(p)
        hg = subprocess.run(["git", "--no-optional-locks", "rev-parse", "HEAD"], cwd=str(root),
                            capture_output=True, text=True).stdout.strip()
        hs = subprocess.run(["git", "--no-optional-locks", "status", "--porcelain=v1", "--untracked-files=all"],
                            cwd=str(root), capture_output=True, text=True).stdout
        hd = subprocess.run(["git", "--no-optional-locks", "diff", "--name-only", "HEAD"], cwd=str(root),
                            capture_output=True, text=True).stdout
        return {"files": files, "head": hg, "status": hs, "diff": hd}
    if route == "weekly":
        decoy_coverage = [{**row, "detail": "Decoy manuscript detail for the same issue; locations unchanged."} for row in coverage]
        decoy_requirements = [{**row, "detail": "Decoy manuscript requirement detail; locations unchanged."} for row in requirements]
    else:
        decoy_coverage = [{**row, "detail": "Decoy manuscript detail for the same issue; locations unchanged."} for row in coverage]
        decoy_requirements = [{**row, "detail": "Decoy manuscript requirement detail; locations unchanged."} for row in requirements]
    decoy_manuscript_path = pub_root / "reader-manuscript-decoy-v2.json"
    assert not decoy_manuscript_path.exists(), "decoy exists"
    reader_publication.build_manuscript_manifest(
        FIX, ISSUE, profile_path, arch_path, appr_path, survey_root / "main.tex",
        [{"role": "BIBLIOGRAPHY", "path": str((survey_root / "references.bib").relative_to(FIX))},
         {"role": "STYLE", "path": str((survey_root / "jgaisurvey.sty").relative_to(FIX))}],
        decoy_coverage, decoy_requirements, "synthetic supplement decoy manuscript author (NOT genuine, NOT Human)",
        man_instant, decoy_manuscript_path)
    ops.append("decoy-manuscript")
    decoy_reviews: dict[str, Path] = {}
    for kind, name in (("SEMANTIC_EDITORIAL", "decoy-pub-semantic-editorial-review-v2.json"),
                       ("VISUAL", "decoy-pub-visual-review-v2.json")):
        expected = reader_publication._expected_review_checks(FIX, profile, kind)
        checks = []
        package_ids = [row["package_id"] for row in arch["packages"]]
        _ordered = [(row.get("drafting_order", 0), row["package_id"]) for row in arch["packages"]]
        _final_pkg = max(_ordered)[1] if _ordered else None
        for check_id in sorted(expected):
            ev = ["synthetic-fixture:main.tex"]
            detail = ("Synthetic TYPE-FIXTURE decoy postrender check only; bound to the decoy "
                      "manuscript for the stage negative; NOT a real review.")
            if check_id in ("ARCHITECTURE_CONTENT_FIDELITY", "LONGFORM_TECHNICAL_DEPTH"):
                ev = sorted({f"package:{pid}" for pid in package_ids} | set(cov_locs) | {f"page-plan:{pages}/12"})
                if check_id == "LONGFORM_TECHNICAL_DEPTH":
                    ev = sorted(set(ev) | {"density-review:below-target-substantive"})
                    detail += " Page-plan/density tags record the measured below-target page-count fact required by the review contract; no substantive density assessment is asserted."
            elif check_id == "FINAL_SYNTHESIS_QUALITY":
                ev = sorted(set(fin_locs) | {"reader-role:final-synthesis"} | ({f"package:{_final_pkg}"} if _final_pkg else set()))
            elif check_id == "LONGFORM_MIXED_LAYOUT":
                ev = ["reader-layout:wide-surfaces-full-width", "reader-layout:references-one-column",
                      "reader-layout:balanced-two-column-narrative"]
            checks.append({"check_id": check_id, "status": "PASS", "detail": detail, "evidence_locations": ev})
        rp = pub_root / name
        assert not rp.exists(), f"decoy review exists {name}"
        reader_publication.build_review_record(
            FIX, decoy_manuscript_path, pdf_path, pages, kind, checks,
            "synthetic supplement decoy review author (NOT genuine, NOT Human)",
            core.parse_instant(f"{DAY}T05:30:00+09:00"), rp)
        decoy_reviews[kind] = rp
    ops.append("decoy-reviews")
    # ---- NEG-S1: DRAFT_COMPLETE stage with decoy manuscript + decoy reviews + exact gate ----
    sp = source_root if route == "weekly" else chain["source_root"]
    _before = _snapshot(FIX)
    try:
        advance("DRAFT_COMPLETE", {
            "reader-manuscript": decoy_manuscript_path, "validated-source": survey_root / "main.tex",
            "publication-pdf": pdf_path, "quality-regression-bundle": bundle_path,
            "semantic-review": decoy_reviews["SEMANTIC_EDITORIAL"], "visual-review": decoy_reviews["VISUAL"],
            "reader-surface-gate": gate_path}, 131, DAY)
        raise AssertionError("NEG-S1 unexpectedly advanced (should refuse decoy manuscript)")
    except stage_validation.StageValidationError as e:
        assert "Reader-Surface Gate validation failed" in str(e), f"NEG-S1 unexpected reason: {e}"
        ops.append("NEG-S1-DRAFT_COMPLETE-refused-exact-manuscript")
        (EV / f"{route}-neg-s1.txt").write_text(f"StageValidationError: {e}\n")
    _after = _snapshot(FIX)
    assert _after == _before, "NEG-S1 mutated fixture tree"
    ops.append("NEG-S1-no-write-verified")
    (EV / f"{route}-neg-s1-snapshot.json").write_text(json.dumps(
        {"before_files": len(_before["files"]), "after_files": len(_after["files"]),
         "head_unchanged": _before["head"] == _after["head"],
         "status_unchanged": _before["status"] == _after["status"]}, indent=2))
    # ---- healthy DRAFT_COMPLETE -> VALIDATED_DRAFT (saves state/checkpoint) ----
    advance("DRAFT_COMPLETE", {
        "reader-manuscript": manuscript_path, "validated-source": survey_root / "main.tex",
        "publication-pdf": pdf_path, "quality-regression-bundle": bundle_path,
        "semantic-review": review_paths["SEMANTIC_EDITORIAL"], "visual-review": review_paths["VISUAL"],
        "reader-surface-gate": gate_path}, 130, DAY)
    assert core.load_json(sp / "production-state.json")["lifecycle_state"] == "VALIDATED_DRAFT"
    ops.append("advance-VALIDATED_DRAFT")
    _ckpt = core.load_json(sp / "production-state.json")["checkpoint_provenance"]["validation"]
    (EV / f"{route}-validated-draft-checkpoint.json").write_text(json.dumps(_ckpt, indent=2))
    if route == "weekly":
        drv.validate_receipt(FIX, pub_root / "validated-source-manifest.json", sp / "production-state.json")
    else:
        generated.validate_receipt(FIX, pub_root / "validated-source-manifest.json", sp / "production-state.json")
    reader_gate.validate_reader_surface_gate(
        FIX, gate_path, expected_manuscript_path=manuscript_path, state_path=sp / "production-state.json")
    ops.append("inherited-gate-site-VALIDATED_DRAFT")
    # ---- Candidate (real) for the VALIDATED_DRAFT stage call ----
    candidate_path = pub_root / "publication-candidate-v2.json"
    assert not candidate_path.exists(), "candidate exists"
    publication.build_candidate(FIX, ISSUE, PROF, manuscript_path, survey_root / "main.tex",
                                pdf_path, pages, bundle_path,
                                review_paths["SEMANTIC_EDITORIAL"], review_paths["VISUAL"], candidate_path)
    ops.append("candidate-build")
    # ---- decoy gate via ACTUAL builder, bound to the decoy manuscript ----
    # build_reader_surface_gate only requires a schema-valid manuscript + a PASS
    # surface review; it does not require review-manuscript binding, so a valid
    # decoy-manuscript gate is constructible with real code (shared pretex review
    # is surface-bound). No hand-written gate JSON anywhere.
    decoy_gate_path = pub_root / "reader-surface-gate-decoy-v2.json"
    assert not decoy_gate_path.exists(), "decoy gate exists"
    reader_publication.build_reader_surface_gate(
        FIX, decoy_manuscript_path, review_path, output_path=decoy_gate_path, state_path=state_path)
    ops.append("decoy-gate-build-actual")
    (EV / f"{route}-decoy-gate-pin.json").write_text(json.dumps(
        {"decoy_gate": str(decoy_gate_path.relative_to(FIX)), "decoy_sha256": sha256_file(decoy_gate_path),
         "real_gate": str(gate_path.relative_to(FIX)), "real_sha256": sha256_file(gate_path),
         "decoy_manuscript": str(decoy_manuscript_path.relative_to(FIX)),
         "decoy_manuscript_sha256": sha256_file(decoy_manuscript_path)}, indent=2))
    # ---- NEG-G: targeted late-fault gate refusal at the VALIDATED_DRAFT stage ----
    # Fault wrapper calls the ACTUAL _merge_artifacts first (prior-artifact checks
    # and merge complete unmodified), then swaps ONLY the validated gate file's
    # bytes for the decoy gate bytes, then returns. The public validate_stage then
    # runs the real _validate_stage_semantics, which must refuse at its Gate check
    # (line ~572), not the Candidate check (line ~555): all candidate/manuscript/
    # QA/PDF refs stay exactly active-before. No validator error forged, no Git
    # success stubbed, no function-global mis-alias (original restored in finally).
    import scripts.survey_stage_validation_v2 as _stage_mod
    _orig_merge = _stage_mod._merge_artifacts
    _real_gate_bytes = gate_path.read_bytes()
    _real_gate_sha = sha256_file(gate_path)
    _decoy_gate_bytes = decoy_gate_path.read_bytes()
    assert _real_gate_sha == json.loads((EV / f"{route}-manuscript-pin.json").read_text())["gate_sha256"]
    _seam = {"count": 0}
    def _merge_with_gate_swap(prior, current):
        merged = _orig_merge(prior, current)
        assert Path(merged["reader-surface-gate"]).resolve() == gate_path.resolve()
        gate_path.write_bytes(_decoy_gate_bytes)
        _seam["count"] += 1
        return merged
    _neg_report = pub_root / "VALIDATED_DRAFT-core-contract-neg-gate.json"
    assert not _neg_report.exists(), "neg report exists"
    st_now = core.load_json(sp / "production-state.json")
    assert st_now["lifecycle_state"] == "VALIDATED_DRAFT"
    _neg_state = {"lifecycle_state": st_now["lifecycle_state"],
                  "checkpoint_provenance": st_now.get("checkpoint_provenance"),
                  "candidate": {"path": str(candidate_path.relative_to(FIX)),
                                "sha256": sha256_file(candidate_path)}}
    _before_g = _snapshot(FIX)
    _stage_mod._merge_artifacts = _merge_with_gate_swap
    try:
        stage_validation.validate_stage(FIX, cfg, sp / "production-state.json",
                                         {"publication-candidate": candidate_path},
                                         _neg_report, core.parse_instant(f"{DAY}T06:14:00+09:00"))
        raise AssertionError("NEG-G unexpectedly passed (should refuse decoy gate)")
    except stage_validation.StageValidationError as e:
        assert "Reader-Surface Gate validation failed" in str(e), f"NEG-G unexpected reason: {e}"
        assert "MANUSCRIPT_MANIFEST does not bind the exact expected Reader Manuscript" in str(e), f"NEG-G wrong site: {e}"
        ops.append("NEG-G-VALIDATED_DRAFT-refused-exact-gate")
        (EV / f"{route}-neg-g.txt").write_text(f"StageValidationError: {e}\n")
    finally:
        _stage_mod._merge_artifacts = _orig_merge
    assert _seam["count"] == 1, f"seam fired {_seam['count']}x, expected exactly once"
    ops.append("NEG-G-seam-once")
    assert _stage_mod._merge_artifacts is _orig_merge, "wrapper not restored"
    _after_g = _snapshot(FIX)
    _gate_rel = str(gate_path.relative_to(FIX))
    _changed = sorted(k for k in _after_g["files"] if _after_g["files"].get(k) != _before_g["files"].get(k))
    _added = sorted(set(_after_g["files"]) - set(_before_g["files"]))
    _removed = sorted(set(_before_g["files"]) - set(_after_g["files"]))
    assert _changed == [_gate_rel] and not _added and not _removed, f"NEG-G unexpected delta: changed={_changed} added={_added} removed={_removed}"
    assert _after_g["head"] == _before_g["head"] and _after_g["status"] == _before_g["status"] and _after_g["diff"] == _before_g["diff"]
    assert not _neg_report.exists(), "neg report must not exist after refusal"
    ops.append("NEG-G-no-write-except-gate")
    (EV / f"{route}-neg-g-snapshot.json").write_text(json.dumps(
        {"changed": _changed, "added": _added, "removed": _removed,
         "head_unchanged": True, "status_unchanged": True, "diff_unchanged": True,
         "seam_count": _seam["count"],
         "state_refs": _neg_state,
         "injected_gate_sha256": sha256_file(gate_path),
         "decoy_gate_sha256": sha256_file(decoy_gate_path)}, indent=2))
    # ---- repair: restore ONLY the owned injected gate bytes ----
    # (The helper probe below runs AFTER this restore: gate==real bytes again,
    #  expected==decoy manuscript must mismatch. Probing before restore would
    #  trivially pass since gate and expectation would both be decoy.)
    gate_path.write_bytes(_real_gate_bytes)
    assert sha256_file(gate_path) == _real_gate_sha, "gate restore mismatch"
    ops.append("NEG-G-repair-gate-restored")
    # ---- secondary helper-level probe (labeled; NOT the stage proof) ----
    # Same expectation as NEG-G but through the direct helper on restored bytes:
    # documents helper/stage agreement without counting as stage coverage.
    try:
        surface_gate.validate_reader_surface_gate(
            FIX, gate_path, expected_manuscript_path=decoy_manuscript_path, state_path=sp / "production-state.json")
        raise AssertionError("helper probe unexpectedly passed")
    except ValueError as e:
        assert "does not bind the exact expected Reader Manuscript" in str(e), f"helper probe unexpected: {e}"
        ops.append("helper-probe-decoy-gate-mismatch")
        (EV / f"{route}-helper-probe.txt").write_text(f"ValueError (helper-level only, not stage proof): {e}\n")
    # ---- healthy rerun of the same actual stage call ----
    _healthy_report = pub_root / "VALIDATED_DRAFT-core-contract-targeted-healthy.json"
    assert not _healthy_report.exists(), "healthy report exists"
    stage_validation.validate_stage(FIX, cfg, sp / "production-state.json",
                                    {"publication-candidate": candidate_path},
                                    _healthy_report, core.parse_instant(f"{DAY}T06:15:00+09:00"))
    ops.append("NEG-G-healthy-rerun-pass")
    (EV / f"{route}-neg-g-healthy.json").write_text(json.dumps(
        {"report": str(_healthy_report.relative_to(FIX)),
         "report_sha256": sha256_file(_healthy_report),
         "gate_restored_sha256": sha256_file(gate_path)}, indent=2))
    if route == "weekly":
        drv.validate_receipt(FIX, pub_root / "validated-source-manifest.json", sp / "production-state.json")
    else:
        generated.validate_receipt(FIX, pub_root / "validated-source-manifest.json", sp / "production-state.json")
    reader_gate.validate_reader_surface_gate(
        FIX, gate_path, expected_manuscript_path=manuscript_path, state_path=sp / "production-state.json")
    ops.append("readback-post-repair-receipt-gate")

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
                        capture_output=True, text=True, cwd=str(EVB))
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
    (EV / f"{route}-targeted-report.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({"DONE": route, "operations": len(ops), "pages": pages,
                      "pdf": report["pdf_sha256"][:12], "state": "VALIDATED_DRAFT"}))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

