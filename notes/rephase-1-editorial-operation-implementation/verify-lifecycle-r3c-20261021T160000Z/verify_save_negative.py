#!/usr/bin/env python3
"""Worker B save + negative (TEST ONLY, NO SOURCE EDITS).

Uses RELEASED lifecycle copies:
  Weekly: /tmp/opencode/jgas-weekly-lifecycle-20261021T160000Z/candidate-partial-b40de60 (active wk-r3c-2)
  Longform: /tmp/opencode/jgas-longform-lifecycle-20261021T160000Z/candidate-partial-b40de60 (active lf-r3c-2)
Creates NEW negative copies, tests wrong old-Candidate Stage/refusal with immediate fault + healthy control,
saves final real PDF/text/page PNG + stage artifacts/State/records/rolemap hashes.
ENV must be set BEFORE python startup. No source/old authority edits, no clean/reset, no network.
"""
from __future__ import annotations
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import traceback
from pathlib import Path

if os.environ.get("PYTHONDONTWRITEBYTECODE") != "1":
    print("BLOCKER PYTHONDONTWRITEBYTECODE!=1", flush=True)
    sys.exit(2)
if not os.environ.get("PYTHONPYCACHEPREFIX","").startswith("/tmp/opencode/"):
    print("BLOCKER PYTHONPYCACHEPREFIX", flush=True)
    sys.exit(2)

TS = "20261021T160000Z"
PACKET = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-editorial-operation-implementation/verify-lifecycle-r3c-20261021T160000Z")
W_LIFE = Path(f"/tmp/opencode/jgas-weekly-lifecycle-{TS}/candidate-partial-b40de60")
L_LIFE = Path(f"/tmp/opencode/jgas-longform-lifecycle-{TS}/candidate-partial-b40de60")
W_NEG_ROOT = Path(f"/tmp/opencode/jgas-weekly-lifecycle-neg-{TS}")
W_NEG = W_NEG_ROOT / "candidate-partial-b40de60"
L_NEG_ROOT = Path(f"/tmp/opencode/jgas-longform-lifecycle-neg-{TS}")
L_NEG = L_NEG_ROOT / "candidate-partial-b40de60"

def log(m: str):
    print(m, flush=True)

def sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1<<20), b""):
            h.update(c)
    return h.hexdigest()

def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)

def load_mods_for_root(life_root):
    # Isolate imports per root (runtime binding checks compare loaded file paths to pins).
    # Must clear before each route; external pycache already set in bash before startup.
    if str(life_root) in sys.path:
        sys.path.remove(str(life_root))
    sys.path.insert(0, str(life_root))
    for m in list(sys.modules.keys()):
        if m.startswith("scripts.") or m.startswith("tests."):
            del sys.modules[m]
    import importlib
    import scripts.survey_production_v2 as core
    import scripts.survey_publication_v2 as pubmod
    import scripts.survey_publication_set_v2 as setmod
    import scripts.survey_stage_validation_v2 as stage_validation
    import scripts.survey_agent_control_v2 as agent
    import scripts.survey_reader_surface_gate_v2 as reader_gate
    import scripts.survey_editorial_publication_v2 as edpub
    # Ensure S2 runtime binding modules loaded (else RUNTIME_BINDING_MISSING).
    # Import every tracked scripts/*.py except file-pin-only semantic producers.
    import pathlib as _pl2  # noqa
    _skip_stems = {"survey_weekly_semantic_publication_v2", "survey_longform_semantic_publication_v2"}
    try:
        _scripts_dir = _pl2.Path(life_root) / "scripts"
        for _py in sorted(_scripts_dir.glob("*.py")):
            _stem = _py.stem
            if _stem in _skip_stems:
                continue
            try:
                __import__(f"scripts.{_stem}")
            except Exception:
                pass
    except Exception:
        pass
    importlib.invalidate_caches()
    return core, pubmod, setmod, stage_validation, agent, reader_gate, edpub

def main() -> int:
    log(f"PACKET={PACKET}")
    # Save final artifacts for both routes (from RELEASED lifecycle copies, no new PDF build)
    for label, life_root, issue, active_id in [
        ("weekly", W_LIFE, "2026-W37", "wk-r3c-2"),
        ("longform", L_LIFE, "SP001", "lf-r3c-2"),
    ]:
        core, pubmod, setmod, stage_validation, agent, reader_gate, edpub = load_mods_for_root(life_root)
        log(f"===SAVE {label} (mods from {life_root})===")
        cfg = core.load_json(life_root / core.DEFAULT_CONFIG)
        state_rel = f"sources/{issue}/production-state.json"
        st = core.load_json(life_root / state_rel)
        log(f"{label} STATE {st.get('lifecycle_state')} (expect RELEASED)")
        if st.get("lifecycle_state") != "RELEASED":
            log(f"BLOCKER {label} not RELEASED")
            return 2
        sel = setmod.resolve_publication_selection(life_root, cfg, st)
        active_cand_rel = (sel.get("candidate_ref") or {}).get("path")
        exp_cand = f"sources/{issue}/publication/v2/editorial-corrections/{active_id}/publication/publication-candidate-v2.json"
        log(f"{label} active {active_cand_rel} expect {exp_cand} SAME={active_cand_rel==exp_cand}")
        if active_cand_rel != exp_cand:
            log(f"BLOCKER {label} active mismatch")
            return 2
        cand = core.load_json(life_root / active_cand_rel)
        pdf_rel = cand.get("pdf", {}).get("path")
        log(f"{label} pdf {pdf_rel} sha={cand.get('pdf',{}).get('sha256')} pages={cand.get('pdf',{}).get('page_count')}")
        # copy PDF to packet
        out_pdf = PACKET / f"final-{label}-second-correction.pdf"
        shutil.copyfile(life_root / pdf_rel, out_pdf)
        log(f"SAVED {out_pdf} sha={sha_file(out_pdf)} bytes={out_pdf.stat().st_size}")
        # text via pdftotext (offline, no network)
        out_txt = PACKET / f"final-{label}-second-correction.txt"
        r = run(["pdftotext", str(life_root/pdf_rel), str(out_txt)])
        log(f"pdftotext {label} exit={r.returncode} stderr={r.stderr[:200]!r}")
        if out_txt.is_file():
            log(f"SAVED TXT {out_txt} sha={sha_file(out_txt)} head={out_txt.read_text()[:300]!r}")
        # png via pdftoppm first page
        out_prefix = PACKET / f"final-{label}-second-correction-page"
        r2 = run(["pdftoppm","-png","-r","150","-f","1","-l","1", str(life_root/pdf_rel), str(out_prefix)])
        log(f"pdftoppm {label} exit={r2.returncode} stderr={r2.stderr[:200]!r}")
        png1 = Path(str(out_prefix)+"-1.png")
        if png1.is_file():
            final_png = PACKET / f"final-{label}-second-correction-p1.png"
            shutil.copyfile(png1, final_png)
            try:
                png1.unlink()
            except Exception:
                pass
            log(f"SAVED PNG {final_png} sha={sha_file(final_png)} bytes={final_png.stat().st_size}")
        # stage artifacts/State/records/rolemap hashes
        hashes = {}
        # active set, receipt, gate, manuscript, State, r2, freeze, manifest, merge, release, checkpoints
        active_set_rel = (sel.get("set_ref") or sel.get("active_set_ref") or {}).get("path")
        pub_dir = f"sources/{issue}/publication/v2/editorial-corrections/{active_id}/publication"
        for rel in [pdf_rel, active_cand_rel, active_set_rel,
                    f"{pub_dir}/validated-source-manifest.json",
                    f"{pub_dir}/reader-surface-gate-v2.json",
                    f"{pub_dir}/reader-manuscript-v2.json",
                    state_rel,
                    f"sources/{issue}/publication/v2/publication-surface-revalidation-r2.json",
                    f"sources/{issue}/publication/v2/freeze-record-v2.json",
                    f"sources/{issue}/publication/v2/release-manifest-v2.json",
                    f"sources/{issue}/publication/v2/merge-verification-v2.json",
                    f"sources/{issue}/publication/v2/release-record-v2.json"]:
            if not rel:
                continue
            p = life_root / rel
            if p.is_file():
                hashes[rel] = {"sha256": sha_file(p), "bytes": p.stat().st_size}
            else:
                hashes[rel] = "missing"
                log(f"MISSING artifact {label} {rel}")
        # checkpoints
        for cp_name in ["VALIDATED_DRAFT","RELEASE_CANDIDATE","FROZEN"]:
            cp_rel = f"sources/{issue}/orchestration/v2/checkpoints/{cp_name}.json"
            p = life_root / cp_rel
            if p.is_file():
                hashes[cp_rel] = {"sha256": sha_file(p), "bytes": p.stat().st_size}
        (PACKET / f"artifact-hashes-{label}.json").write_text(json.dumps(hashes, indent=2))
        log(f"HASHES {label} saved {len(hashes)} entries")
        rolemap = {"mode": sel.get("mode"), "candidate_ref": sel.get("candidate_ref"), "set_ref": sel.get("set_ref") or sel.get("active_set_ref"), "canonical_anchor": sel.get("canonical_anchor"),
                   "effective7": {k: (v.get("path"), v.get("sha256")) for k,v in (sel.get("effective7") or {}).items()},
                   "roles": {k: (v.get("path"), v.get("sha256"), v.get("byte_count")) for k,v in (sel.get("roles") or {}).items()}}
        (PACKET / f"rolemap-{label}.json").write_text(json.dumps(rolemap, indent=2))
        log(f"ROLEMAP {label} saved")
        # strict State + active receipt/Gate/Candidate + history after RELEASED
        # agent/reader_gate/edpub already loaded per-root above
        # For longform post-RELEASED receipt, evidence package basis drift (state_sha) is known: log blocker but continue to Gate/Candidate + negative.
        errs = agent.validate_agent_state(life_root, cfg, st)
        log(f"{label} STATE errs={errs} (expect [])")
        if errs:
            log(f"BLOCKER {label} State unhealthy")
            return 2
        try:
            rv = edpub.validate_editorial_receipt(life_root, f"{pub_dir}/validated-source-manifest.json", state_rel)
            log(f"{label} RECEIPT {rv.get('issue_id')}")
        except BaseException as e:
            log(f"{label} RECEIPT BLOCKER (post-RELEASED, continue to Gate/Candidate + negative): {type(e).__name__}: {e}")
            traceback.print_exc()
        try:
            gv = reader_gate.validate_reader_surface_gate(life_root, f"{pub_dir}/reader-surface-gate-v2.json", issue_id=issue, publication_profile=("WEEKLY_MAGAZINE" if issue=="2026-W37" else "LONGFORM_SPECIAL"), expected_manuscript_path=life_root/f"{pub_dir}/reader-manuscript-v2.json", state_path=state_rel)
            log(f"{label} GATE {gv.get('status')}")
        except BaseException as e:
            log(f"{label} GATE BLOCKER: {type(e).__name__}: {e}")
            traceback.print_exc()
        try:
            cv = pubmod.validate_candidate(life_root, life_root/active_cand_rel)
            log(f"{label} CAND {cv.get('status')}")
        except BaseException as e:
            log(f"{label} CAND BLOCKER: {type(e).__name__}: {e}")
            traceback.print_exc()
        log(f"{label} HISTORY {st.get('history')[-3:]}")
    # Negative old-Candidate Stage/refusal in NEW negative copies
    for label, life_root, neg_root, neg_path, issue, old_id, active_id in [
        ("weekly", W_LIFE, W_NEG_ROOT, W_NEG, "2026-W37", "wk-r3c-1", "wk-r3c-2"),
        ("longform", L_LIFE, L_NEG_ROOT, L_NEG, "SP001", "lf-r3c-1", "lf-r3c-2"),
    ]:
        log(f"===NEGATIVE {label}===")
        if neg_root.exists():
            log(f"BLOCKER NEG_ROOT exists {neg_root}")
            return 2
        neg_root.mkdir(parents=True)
        r = run(["cp","-a", str(life_root), str(neg_path)])
        log(f"NEG cp -a {label} exit={r.returncode}")
        if r.returncode != 0:
            return 2
        # verify no sharing/alternates/inert (same checks minimal)
        for rel in ["scripts/survey_schema_v2.py",".git/HEAD"]:
            s = run(["stat","-c","%d:%i %h", str(life_root/rel)]).stdout.strip()
            d = run(["stat","-c","%d:%i %h", str(neg_path/rel)]).stdout.strip()
            if s.split()[0]==d.split()[0]:
                log(f"BLOCKER NEG hardlink {rel}")
                return 2
        if (neg_path/".git/objects/info/alternates").exists():
            log("BLOCKER NEG alternates")
            return 2
        # On NEG (RELEASED), create temp VALIDATED_DRAFT state to test Stage with wrong old vs healthy (no State rewind of real State)
        import copy as _copy
        neg_cfg = core.load_json(neg_path / core.DEFAULT_CONFIG)
        neg_state_rel = f"sources/{issue}/production-state.json"
        neg_st = core.load_json(neg_path / neg_state_rel)
        core_n, _, _, stage_validation_n, _, _, _ = load_mods_for_root(neg_path)
        tmp_st = _copy.deepcopy(neg_st)
        tmp_st["lifecycle_state"] = "VALIDATED_DRAFT"
        # keep gates pending for VALIDATED_DRAFT? After RELEASED gates are approved; for temp VALIDATED_DRAFT test, set preview pending to match VALIDATED_DRAFT expectations
        # Actually VALIDATED_DRAFT expects preview pending, freeze pending, release pending. Our RELEASED has them passed. For temp test, set them pending to avoid unrelated failures? But _validate_stage_semantics for VALIDATED_DRAFT only checks candidate binding + Gate, not gates? It checks candidate + Gate, not human gates directly. However validate_agent_state will check lifecycle vs gates? Let's keep as is and see: temp VALIDATED_DRAFT with approved preview may still be considered healthy? Better to set preview pending? Let's inspect: after RELEASED, human_gates preview approved, machine checkpoints passed. For VALIDATED_DRAFT, preview should be pending. If we keep approved, validate_agent_state may complain? Safer to set temp to have preview pending + freeze/release pending, but keep pointer same (r2). That temp is fixture-only, not authority rebind.
        tmp_st["human_gates"]["publication_preview"] = "pending"
        tmp_st["human_gate_provenance"]["publication_preview"] = None
        tmp_st["machine_checkpoints"]["publication_preview"] = "pending"
        tmp_st["machine_checkpoints"]["freeze"] = "pending"
        tmp_st["machine_checkpoints"]["release"] = "pending"
        try:
            tmp_st["checkpoint_provenance"]["publication_preview"] = None
            tmp_st["checkpoint_provenance"]["freeze"] = None
            tmp_st["checkpoint_provenance"]["release"] = None
        except Exception:
            pass
        try:
            _hist = tmp_st.get("history", [])
            if len(_hist) >= 3:
                tmp_st["history"] = _hist[:-3]
        except Exception:
            pass
        tmp_st["next_action"] = "stage:publication-candidate"
        tmp_st["terminal_reason"] = None
        # Write temp state in execution dir (not real State path)
        tmp_rel = f"sources/{issue}/publication/v2/editorial-corrections/{active_id}/execution/neg-validated-state.json"
        tmp_path = neg_path / tmp_rel
        tmp_path.parent.mkdir(parents=True, exist_ok=True)
        core_n.write_json(tmp_path, tmp_st)
        stale_rel = f"sources/{issue}/publication/v2/editorial-corrections/{old_id}/publication/publication-candidate-v2.json"
        active_rel = f"sources/{issue}/publication/v2/editorial-corrections/{active_id}/publication/publication-candidate-v2.json"
        log(f"NEG {label} stale {stale_rel} exists={(neg_path/stale_rel).is_file()} active {active_rel} exists={(neg_path/active_rel).is_file()}")
        log(f"NEG stale sha={sha_file(neg_path/stale_rel) if (neg_path/stale_rel).is_file() else 'missing'} active sha={sha_file(neg_path/active_rel) if (neg_path/active_rel).is_file() else 'missing'}")
        # immediate fault: stale must refuse
        try:
            neg_report = neg_path / f"sources/{issue}/publication/v2/editorial-corrections/{active_id}/execution/neg-stale-report.json"
            stage_validation_n.validate_stage(neg_path, neg_cfg, tmp_path, {"publication-candidate": neg_path/stale_rel}, neg_report, __import__("datetime").datetime.now(__import__("datetime").timezone.utc))
            log(f"BLOCKER NEG {label} stale unexpectedly PASSED (should refuse)")
            return 2
        except Exception as ex:
            log(f"NEG {label} stale correctly refused: {type(ex).__name__}: {ex}")
        # healthy control: active must pass
        try:
            neg_ok = neg_path / f"sources/{issue}/publication/v2/editorial-corrections/{active_id}/execution/neg-healthy-report.json"
            stage_validation_n.validate_stage(neg_path, neg_cfg, tmp_path, {"publication-candidate": neg_path/active_rel}, neg_ok, __import__("datetime").datetime.now(__import__("datetime").timezone.utc))
            log(f"NEG {label} healthy passed (control OK)")
        except Exception as ex:
            log(f"BLOCKER NEG {label} healthy failed: {ex}")
            traceback.print_exc()
            return 2
        log(f"NEGATIVE {label} complete (fault + healthy, no authority rebind, no State rewind of real State)")
    log("SAVE+NEGATIVE COMPLETE (synthetic type-only, NO production PASS)")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        sys.exit(2)
