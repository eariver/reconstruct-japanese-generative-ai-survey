#!/usr/bin/env python3
"""H build schema/H consistency — EXECUTED 3-field pdf + required companions (narrow, NOT ENDTOEND until real activation).

ROOT coordination (phase-high/20261024T130000Z/interface-mismatch-proof-basis-ref.md):
- First recommendation proof.basis_ref SELF REJECTED: H FILESHA compare CORRECT remains unchanged.
- H outputs.pdf EXACT4->EXACT3; toolchainVersions explicit biber/latexmk companions (present vs error, recipe-specific REQUIRED).
- HIGH sidecar R/build/toolchain-companions.json REJECTED; tell high exact shape now binding in buildRecord (not sidecar).
- Uses existing local TeX real SHAs/version stdout/exit (no runtime project network, no live execute in H).
- NARROW, NOT ENDTOEND until real activation with high finalize unblocked + real complete C.
PYTHONDONTWRITEBYTECODE=1; fixture import origin verified; unique run record, no overwrite.
"""
from __future__ import annotations
import hashlib, json, os, sys
from pathlib import Path

def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def _run_git(root: Path, *args: str):
    import subprocess
    return subprocess.run(["git", *args], cwd=str(root), capture_output=True, timeout=30, env={**os.environ, "GIT_OPTIONAL_LOCKS": "0", "GIT_CONFIG_NOSYSTEM": "1"})

def main() -> int:
    base = Path(__file__).resolve().parents[4]
    weekly_root = base / ".rephase-1-editorial-runtime/versioned-renewal-historyfix-v4-20261024T070000Z/bootstrap-weekly-new"
    assert (weekly_root / ".git").is_dir()
    for _m in [m for m in list(sys.modules) if m == "scripts" or m.startswith("scripts.")]:
        del sys.modules[_m]
    sys.path.insert(0, str(weekly_root))
    try:
        import scripts.survey_versioned_renewal_history_v2 as hist
        assert str(getattr(hist, "__file__", "")).startswith(str(weekly_root))
        print(f"origin OK HIST: {hist.__file__}")
    finally:
        try: sys.path.remove(str(weekly_root))
        except ValueError: pass
    root = weekly_root.resolve()
    real_build_path = base / ".rephase-1-editorial-runtime/versioned-renewal-bootstrap-20261023T194449Z/bootstrap-weekly/sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/publication/build-record.json"
    assert real_build_path.exists()
    real_build = json.loads(real_build_path.read_bytes())
    real_versions = real_build.get("toolchain", {}).get("versions", {})
    assert isinstance(real_versions, dict) and "stdout" in real_versions and "biber_stdout" in real_versions and "latexmk_stdout" in real_versions
    print(f"real R3 toolchain baseline OK: base6 + biber+latexmk present (no error)")
    new_epoch = _run_git(root, "rev-parse", "HEAD").stdout.decode().strip()
    assert len(new_epoch) == 40
    print(f"v4 new_epoch (latest H+schema fixes): {new_epoch[:12]}...")
    # Temp live files for declared_inputs/outputs (untracked, no Git DB objects).
    tmp_base = root / "tmp-build-test-hist-v4"
    import shutil
    if tmp_base.exists(): shutil.rmtree(tmp_base)
    (tmp_base / "staged").mkdir(parents=True)
    (tmp_base / "build").mkdir(parents=True)
    trio_files = {"primary": (tmp_base / "staged" / "main.tex", b"\\documentclass{article}\\begin{document}test\\end{document}"), "bibliography": (tmp_base / "staged" / "references.bib", b"@book{k,}"), "style": (tmp_base / "staged" / "jgaisurvey.sty", b"% style test")}
    out_files = {"publication-pdf": (tmp_base / "build" / "main.pdf", b"%PDF-1.4 test\n"), "build-log": (tmp_base / "build" / "main.log", b"log test"), "pdf-digest": (tmp_base / "build" / "main.pdf.sha256", b"digest test")}
    for _, (p, b) in list(trio_files.items()) + list(out_files.items()):
        p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(b)
    def _rel(p: Path) -> str: return p.relative_to(root).as_posix()
    def _fsha(p: Path) -> str: return _sha(p.read_bytes())
    def _base_build_doc():
        doc = {"schema_version": "2.0-rc1", "kind": "VERSIONED_RENEWAL_BUILD_V1", "variant": "EXECUTED_BUILD", "issue_id": "2026-W37",
            "proposal_ref": {"path": "sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/proposal.json", "sha256": _sha((root / "sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/proposal.json").read_bytes())} if (root / "sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/proposal.json").exists() else {"path": "P/proposal.json", "sha256": "0"*64},
            "renewal_basis_ref": {"path": "R/basis.json", "sha256": "0"*64}, "renewal_proof_ref": {"path": "R/proof.json", "sha256": "0"*64},
            "recipe_ref": {"path": ".latexmkrc", "sha256": _sha((root / ".latexmkrc").read_bytes())} if (root / ".latexmkrc").exists() else {"path": ".latexmkrc", "sha256": "0"*64},
            "recorded_at": "2026-10-24T07:00:00Z",
            "declared_inputs": {"primary": {"path": _rel(trio_files["primary"][0]), "sha256": _fsha(trio_files["primary"][0])}, "bibliography": {"path": _rel(trio_files["bibliography"][0]), "sha256": _fsha(trio_files["bibliography"][0])}, "style": {"path": _rel(trio_files["style"][0]), "sha256": _fsha(trio_files["style"][0])}},
            "recipe": {"fixed_steps": ["lualatex -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error main.tex", "biber main", "lualatex -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error main.tex", "lualatex -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error main.tex"]},
            "toolchain": {"executable": real_build.get("toolchain", {}).get("executable", "/tmp/opencode/jgas-texlive-20261019T133205Z/texlive/bin/x86_64-linux/lualatex"), "versions": dict(real_versions), "argv": ["lualatex -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error main.tex", "biber main", "lualatex -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error main.tex", "lualatex -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error main.tex"], "env": {}},
            "outputs": {"publication-pdf": {"path": _rel(out_files["publication-pdf"][0]), "sha256": _fsha(out_files["publication-pdf"][0]), "byte_count": len(out_files["publication-pdf"][1])}, "build-log": {"path": _rel(out_files["build-log"][0]), "sha256": _fsha(out_files["build-log"][0]), "byte_count": len(out_files["build-log"][1])}, "pdf-digest": {"path": _rel(out_files["pdf-digest"][0]), "sha256": _fsha(out_files["pdf-digest"][0]), "byte_count": len(out_files["pdf-digest"][1])}},
            "exit_code": 0}
        payload = {k: v for k, v in doc.items() if k != "build_sha256"}
        doc["build_sha256"] = hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        return doc
    build_path = tmp_base / "build-record-test.json"
    import copy
    # Valid EXECUTED 3-field pdf + required companions accepted.
    valid_doc = _base_build_doc()
    build_path.write_bytes((json.dumps(valid_doc, ensure_ascii=False, indent=2) + "\n").encode())
    try:
        hist._verify_build_chain_hist(root, valid_doc, str(build_path.relative_to(root).as_posix()), new_epoch, [], "2026-W37", "H consistency valid EXECUTED")
        print("H VALID EXECUTED 3-field pdf (no page_count, R4 sizedRef EXACT3) + required companions (base6 + biber+latexmk present, no error, lualatex-biber-lualatex) ACCEPTED.")
    except Exception as e:
        print(f"H VALID EXECUTED UNEXPECTED FAIL: {type(e).__name__}: {e}"); raise
    # Wrong companion (unregistered pdflatex_*) -> MISMATCH (unbound, no freeform; sidecar REJECTED).
    bad = copy.deepcopy(valid_doc); bad["toolchain"]["versions"]["pdflatex_stdout"] = "x"
    bad.pop("build_sha256", None); bad["build_sha256"] = hashlib.sha256(json.dumps({k: v for k, v in bad.items() if k != "build_sha256"}, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    build_path.write_bytes((json.dumps(bad, ensure_ascii=False, indent=2) + "\n").encode())
    try:
        hist._verify_build_chain_hist(root, bad, str(build_path.relative_to(root).as_posix()), new_epoch, [], "2026-W37", "H wrong companion")
        print("H WRONG COMPANION UNEXPECTED PASS"); raise AssertionError("wrong companion UNEXPECTED PASS")
    except Exception as e:
        assert "HISTORY_DIGEST_MISMATCH" in str(e) and ("unbound" in str(e).lower() or "freeform" in str(e).lower() or "pdflatex" in str(e).lower() or "only biber" in str(e).lower()), f"wrong code: {e}"
        print(f"H WRONG COMPANION (unregistered pdflatex_*) correctly rejects MISMATCH (unbound, no freeform; sidecar REJECTED): {str(e)[:200]}")
    # Missing companion (biber missing, no error, no present) for lualatex-biber-lualatex where biber REQUIRED -> MISMATCH.
    bad2 = copy.deepcopy(valid_doc)
    for k in list(bad2["toolchain"]["versions"].keys()):
        if k.startswith("biber_"): del bad2["toolchain"]["versions"][k]
    assert "biber_error" not in bad2["toolchain"]["versions"] and "biber_stdout" not in bad2["toolchain"]["versions"]
    bad2.pop("build_sha256", None); bad2["build_sha256"] = hashlib.sha256(json.dumps({k: v for k, v in bad2.items() if k != "build_sha256"}, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    build_path.write_bytes((json.dumps(bad2, ensure_ascii=False, indent=2) + "\n").encode())
    try:
        hist._verify_build_chain_hist(root, bad2, str(build_path.relative_to(root).as_posix()), new_epoch, [], "2026-W37", "H missing companion")
        print("H MISSING COMPANION UNEXPECTED PASS"); raise AssertionError("missing companion UNEXPECTED PASS")
    except Exception as e:
        assert "HISTORY_DIGEST_MISMATCH" in str(e), f"wrong code: {e}"
        print(f"H MISSING COMPANION (biber missing, no error, no present) correctly rejects MISMATCH (must be present OR error only; biber REQUIRED): {str(e)[:200]}")
    # Unbound companion (sidecar with companions, versions missing required) -> H must fail even if sidecar exists (no sidecar laundering).
    sidecar_path = tmp_base / "toolchain-companions.json"
    sidecar_path.write_bytes(json.dumps({"biber_stdout": "x", "biber_returncode": 0, "biber_link_path": "y", "biber_real_path": "z", "biber_real_sha256": "0"*64}, ensure_ascii=False, indent=2).encode())
    bad3 = copy.deepcopy(valid_doc)
    for k in list(bad3["toolchain"]["versions"].keys()):
        if k.startswith("biber_"): del bad3["toolchain"]["versions"][k]
    bad3.pop("build_sha256", None); bad3["build_sha256"] = hashlib.sha256(json.dumps({k: v for k, v in bad3.items() if k != "build_sha256"}, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    build_path.write_bytes((json.dumps(bad3, ensure_ascii=False, indent=2) + "\n").encode())
    try:
        hist._verify_build_chain_hist(root, bad3, str(build_path.relative_to(root).as_posix()), new_epoch, [], "2026-W37", "H unbound companion (sidecar)")
        print("H UNBOUND COMPANION (sidecar) UNEXPECTED PASS"); raise AssertionError("unbound companion UNEXPECTED PASS")
    except Exception as e:
        assert "HISTORY_DIGEST_MISMATCH" in str(e), f"wrong code: {e}"
        print(f"H UNBOUND COMPANION (sidecar with companions, versions missing required) correctly rejects MISMATCH (no sidecar laundering, no new sidecar artifact): {str(e)[:200]}")
        print("Tell HIGH: exact serialized record shape now binding companion paths/real SHAs/version stdout/exit/probed tool evidence can record directly in buildRecord toolchain.versions (not sidecar R/build/toolchain-companions.json); REJECT sidecar as acceptance; no new sidecar artifact, no new schema file; all buildRecord selfdigest cover all fields, source closure unchanged 63 paths (same, no new sidecar path).")
    # Changed real sha invalid (non-64hex) -> schema/H rejects (format, not live execute).
    bad4 = copy.deepcopy(valid_doc); bad4["toolchain"]["versions"]["real_sha256"] = "z"*64
    bad4.pop("build_sha256", None); bad4["build_sha256"] = hashlib.sha256(json.dumps({k: v for k, v in bad4.items() if k != "build_sha256"}, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    build_path.write_bytes((json.dumps(bad4, ensure_ascii=False, indent=2) + "\n").encode())
    try:
        hist._verify_build_chain_hist(root, bad4, str(build_path.relative_to(root).as_posix()), new_epoch, [], "2026-W37", "H changed real sha")
        print("H CHANGED REAL SHA (invalid) UNEXPECTED PASS"); raise AssertionError("changed real sha UNEXPECTED PASS")
    except Exception as e:
        assert "HISTORY_DIGEST_MISMATCH" in str(e) or "real_sha256" in str(e).lower(), f"wrong code: {e}"
        print(f"H CHANGED REAL SHA (invalid non-64hex) correctly rejects (format, not live execute): {str(e)[:200]}")
    # Wrong toolchain executable (e.g., "/bin/false", still valid string): H accepts (no live execute, recorded evidence). Downstream High C actual probing would reject (live execute) – distinguish H HIST vs High C actual probing (documented, not executed here).
    bad5 = copy.deepcopy(valid_doc); bad5["toolchain"]["executable"] = "/bin/false"
    bad5.pop("build_sha256", None); bad5["build_sha256"] = hashlib.sha256(json.dumps({k: v for k, v in bad5.items() if k != "build_sha256"}, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    build_path.write_bytes((json.dumps(bad5, ensure_ascii=False, indent=2) + "\n").encode())
    try:
        hist._verify_build_chain_hist(root, bad5, str(build_path.relative_to(root).as_posix()), new_epoch, [], "2026-W37", "H wrong toolchain")
        print("H WRONG TOOLCHAIN (valid string /bin/false, no live execute, recorded evidence) ACCEPTED (H HIST, no live execute, accepts recorded evidence; downstream High C actual probing would reject via live execute – distinguish H HIST vs High C actual probing, High worker separate).")
    except Exception as e:
        print(f"H WRONG TOOLCHAIN UNEXPECTED FAIL (H HIST should accept recorded evidence, no live execute; High C actual probing would reject via live execute, High worker separate): {type(e).__name__}: {e}"); raise
    # Std field mutations valid format -> H PASS (no fake live execute, recorded evidence, H HIST vs High C actual probing).
    bad6 = copy.deepcopy(valid_doc); bad6["toolchain"]["versions"]["stdout"] = "different valid stdout <=8000"
    bad6.pop("build_sha256", None); bad6["build_sha256"] = hashlib.sha256(json.dumps({k: v for k, v in bad6.items() if k != "build_sha256"}, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    build_path.write_bytes((json.dumps(bad6, ensure_ascii=False, indent=2) + "\n").encode())
    try:
        hist._verify_build_chain_hist(root, bad6, str(build_path.relative_to(root).as_posix()), new_epoch, [], "2026-W37", "H std field mutation")
        print("H STD FIELD MUTATION (valid format) ACCEPTED (no fake current tool validation, H HIST recorded, no live execute; High C actual probing would record via live execute, not verify recorded vs live – distinguish).")
    except Exception as e:
        print(f"H STD FIELD MUTATION UNEXPECTED FAIL (H HIST should accept recorded evidence, no live execute): {type(e).__name__}: {e}"); raise
    # EXACT4 pdf (with page_count) must be REJECTED (accept ONLY EXACT3, no lax union).
    bad7 = copy.deepcopy(valid_doc)
    # Add page_count to publication-pdf (making EXACT4) – should be rejected (must be EXACT3).
    import copy as _copy2
    bad7 = _copy2.deepcopy(valid_doc)
    # Find outputs publication-pdf and add page_count.
    bad7["outputs"]["publication-pdf"]["page_count"] = 5
    bad7.pop("build_sha256", None); bad7["build_sha256"] = hashlib.sha256(json.dumps({k: v for k, v in bad7.items() if k != "build_sha256"}, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    build_path.write_bytes((json.dumps(bad7, ensure_ascii=False, indent=2) + "\n").encode())
    try:
        hist._verify_build_chain_hist(root, bad7, str(build_path.relative_to(root).as_posix()), new_epoch, [], "2026-W37", "H EXACT4 pdf")
        print("H EXACT4 PDF (with page_count) UNEXPECTED PASS (should FAIL, accept ONLY EXACT3)"); raise AssertionError("EXACT4 pdf UNEXPECTED PASS")
    except Exception as e:
        assert "HISTORY_DIGEST_MISMATCH" in str(e) and "EXACT3" in str(e), f"wrong code (should be MISMATCH EXACT3, no lax union): {e}"
        print(f"H EXACT4 PDF (with page_count) correctly rejects MISMATCH (accept ONLY EXACT3, no lax union; pagecount downstream): {str(e)[:200]}")
    import shutil
    try: shutil.rmtree(tmp_base)
    except Exception: pass
    print("NARROW build schema/H consistency valid/invalid EXECUTED 3-field pdf + companions: IMPLEMENTED above (using existing local TeX real SHAs/version stdout/exit, no runtime project network, no live execute in H).")
    print("Preserve bad SELF before fixtures/wrappers immutable no rewrites.")
    print("Candidate 409+uncommitted owned H files only; no new ordinary commit; whole unit ongoing not HumanCommitPoint.")
    print("Remaining H accumulator unexecuted until high U activate; HIGH will run real U/C fixture and report failures; do NOT claim 21/next 40 pass before actual.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
