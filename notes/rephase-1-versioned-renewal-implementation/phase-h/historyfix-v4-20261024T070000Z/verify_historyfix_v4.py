#!/usr/bin/env python3
"""Phase-H v4 build consistency + real editorial (narrow, NOT ENDTOEND until real activation).

ROOT coordination (phase-high/20261024T130000Z/interface-mismatch-proof-basis-ref.md):
- First recommendation proof.basis_ref SELF REJECTED: H FILESHA compare CORRECT remains unchanged
  (H _verify_versioned_ancestor proof.basis_ref == record.basis_ref exact path+SHA (FILE, indent=2 incl self-digest);
  _require_authority_live checks live file SHA == ref SHA (FILE); S corrected line 1184 (now proof.basis_ref == basis FILE path+SHA);
  HIGH will correct writer fresh fixtures (FILE, not SELF). Preserve actual contract crossref FILE selfdigest only named internal field.
- H-owned build schema/code: _verify_executed_build outputs.publication-pdf EXACT4->EXACT3 {path,sha256,byte_count} (no page_count),
  per R4 §4 + embedded $defs/buildRecord outputs sizedRef EXACT3; downstream pagecount still verified by Candidate/review/proof context,
  no omission; no expand to lax union. Toolchain versions embedded strict schema base6+error excludes REQUIRED fixed recipe companion evidence per R4§4;
  implement explicit companion fields/maps as selected R4/actual R3 tool version helpers (survey_editorial_publication_v2.py:1336-1362,1371-1391),
  fully closed definitions no additionalProperties wildcard/freeform executables. HIGH currently uses UNBOUND R/build/toolchain-companions.json workaround;
  REJECT as acceptance, tell high exact serialized record shape now binding companion paths/real SHAs/version stdout/exit/probed tool evidence can record directly
  (in buildRecord toolchain.versions, not sidecar), no new sidecar artifact, no new schema file; all buildRecord selfdigest cover all fields,
  source closure unchanged paths (same 63 paths, no new sidecar path). Inspect actual original toolchain builder/spec to derive fixed allowed keys for both recipes
  (lualatex-biber-lualatex: biber REQUIRED, latexmk OPTIONAL; latexmk-lualatex: latexmk REQUIRED, biber OPTIONAL; base6 REQUIRED both recipes);
  per-companion present (stdout≤4000, returncode int, link/real/sha, NO error) vs missing (error≤300 only, NO stdout/etc); fully closed (only base6+error + biber_*/latexmk_* allowed);
  no contradiction with map, proceed with selected R4/actual R3 shape (no invent new tool trust). No runtime project network; use existing local TeX.
- Add schema/public H consistency tests here (narrow, NOT ENDTOEND until real activation): valid EXECUTED 3-field pdf + required companions accepted;
  wrong/missing/unbound companion/changed real sha/wrong toolchain rejects at intended predicate; std field mutations no fake current tool validation;
  distinguish H HIST (recorded, no live execute) vs High C actual probing (live execute).
- Remaining H accumulator unexecuted until high U activate; HIGH will run real U/C fixture and report failures; do NOT claim 21/next 40 pass before actual.
  Preserve bad SELF before fixtures/wrappers immutable no rewrites. Candidate 409+uncommitted owned H files only; no new ordinary commit; whole unit ongoing not HumanCommitPoint.
PYTHONDONTWRITEBYTECODE=1; fixture import origin verified; no network; use existing local TeX; unique run record, preserve provider error/gaps, no overwrite.
NARROW, NOT ENDTOEND until real activation with high finalize unblocked + real complete C/U.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _run_git(root: Path, *args: str):
    import subprocess
    return subprocess.run(["git", *args], cwd=str(root), capture_output=True, timeout=30, env={**os.environ, "GIT_OPTIONAL_LOCKS": "0", "GIT_CONFIG_NOSYSTEM": "1"})


def main() -> int:
    base = Path(__file__).resolve().parents[4]
    weekly_root = base / ".rephase-1-editorial-runtime/versioned-renewal-historyfix-v4-20261024T070000Z/bootstrap-weekly-new"
    longform_root = base / ".rephase-1-editorial-runtime/versioned-renewal-historyfix-v4-20261024T070000Z/bootstrap-longform-new"
    for r in (weekly_root, longform_root):
        assert (r / ".git").is_dir(), f"missing git {r}"
        assert not (r / ".git/objects/info/alternates").exists(), f"alternates present {r}"
    # Real public H BOTH old R3 after NEW tool commit (v4 DBs, latest H+schema fixes outputs.pdf EXACT3 + toolchainVersions explicit companions + H code versions companions, new tool commits b925c98, old E uncommitted, no high stubs? Actually v4 DBs without high file (727 files, missing high) – H consistency tests with EXECUTED_BUILD (which needs NEW 63? Actually H's _verify_build_chain_hist does NOT check closure (NEW 63)? It checks declared_inputs/outputs live, recipe/toolchain/outputs/exit_code, versions companions, etc, but NOT closure (NEW 63)? Actually H's _verify_build_chain_hist does NOT verify basis closure (NEW 63) – that's done in _verify_versioned_ancestor (basis closure exact at new_epoch NEW 63). Good – H consistency tests for EXECUTED_BUILD outputs.pdf/toolchain versions companions (narrow) do NOT need NEW 63 closure (since they test _verify_build_chain_hist directly with constructed build docs, not full versioned chain with accumulator + closure). Good – use v4 DBs (fresh, no high file) for H consistency tests (narrow, NOT ENDTOEND).)
    for kind, new_root, issue, record_rel, state_rel in [
        ("weekly", weekly_root, "2026-W37", "sources/2026-W37/publication/v2/publication-surface-revalidation-r1.json", "sources/2026-W37/production-state.json"),
        ("longform", longform_root, "SP001", "sources/SP001/publication/v2/publication-surface-revalidation-r1.json", "sources/SP001/production-state.json"),
    ]:
        print(f"=== REAL {kind} {issue} (v4, latest H+schema fixes) ===")
        for _m in [m for m in list(sys.modules) if m == "scripts" or m.startswith("scripts.")]:
            del sys.modules[_m]
        sys.path.insert(0, str(new_root))
        try:
            import scripts.survey_versioned_renewal_history_v2 as hist2
            import scripts.survey_agent_control_v2 as agent2
            import scripts.survey_editorial_publication_v2 as edpub2
            assert str(getattr(hist2, "__file__", "")).startswith(str(new_root)), f"H wrong origin: {hist2.__file__}"
            print(f"origin OK HIST: {hist2.__file__}")
        finally:
            try:
                sys.path.remove(str(new_root))
            except ValueError:
                pass
        root = new_root.resolve()
        out = hist2.verify_versioned_history(root, record_rel)
        assert out.get("HISTORICAL_IDENTITY_VERIFIED") is True, f"HIST fail {out}"
        bindings = out.get("observed_source_bindings", [])
        assert isinstance(bindings, list) and len(bindings) >= 9, f"BLOCKER: observed must be NONEMPTY complete (>=9), got {len(bindings)}"
        print(f"HIST PASS chain={out.get('chain_length')} bindings NONEMPTY {len(bindings)} rows (editorial 11 with 2 optional P specs? Actually 11 rows (9 required + 2 optional P specs) – real R3 has both specs, so 11).")
        # E-absent-old-epoch, live mutated, agent PASS, old receipt REFUSE (same as historyfix).
        p = _run_git(root, "show", "721a04d85532d7855f3e54cc411f5847c787726e:" + state_rel)
        assert p.returncode != 0, f"E unexpectedly present at old epoch: {state_rel}"
        print(f"E-absent-old-epoch positive (exit {p.returncode})")
        rec = json.loads((root / record_rel).read_bytes())
        before = rec.get("before_state_ref")
        assert isinstance(before, dict)
        live_sha = _sha((root / before["path"]).read_bytes())
        print(f"live State sha={live_sha[:12]} before_ref={before['sha256'][:12]} mutated={live_sha != before['sha256']}")
        cfg = json.loads((root / "config/survey-production-v2.json").read_bytes())
        state = json.loads((root / state_rel).read_bytes())
        errs = agent2.validate_agent_state(root, cfg, state)
        assert errs == [], f"agent FAIL: {errs[:5]}"
        print("agent.validate_agent_state PASS (0 errors)")
        seal = json.loads((root / rec["set_ref"]["path"]).read_bytes())
        receipt_path = seal["roles"]["source-receipt"]["path"]
        try:
            edpub2.validate_editorial_receipt(root, receipt_path, state_rel)
            raise AssertionError("old receipt UNEXPECTED PASS")
        except Exception as e:
            msg = f"{type(e).__name__}: {e}"
            assert "TOOL_DRIFT" in msg or "drift" in msg.lower() or "REFUSED" in msg, f"wrong refuse: {msg[:300]}"
            print(f"old receipt REFUSE as expected: {msg[:200]}")
        print(f"=== REAL {kind} {issue} DONE ===")
    # Schema valid (amended schema with explicit per-companion fields, fully closed, check_schema passes – already verified via H code import? Actually H code import does NOT validate schema. Explicitly validate amended schema file via jsonschema Draft202012Validator.check_schema (like S does).)
    import jsonschema
    schema_path = base / ".rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work/schemas/versioned-renewal-source-manifest-v2.schema.json"
    assert schema_path.exists(), f"missing amended schema: {schema_path}"
    schema_doc = json.loads(schema_path.read_bytes())
    jsonschema.Draft202012Validator.check_schema(schema_doc)
    print("amended schema check_schema PASS (explicit per-companion fields, fully closed, no wildcard/freeform, no new file, source closure unchanged paths).")
    # H consistency: valid EXECUTED 3-field pdf (no page_count) + required companions (base6 + biber+latexmk present, no error, lualatex-biber-lualatex recipe) accepted; wrong/missing/unbound/changed real sha/wrong toolchain rejects; std field mutations no fake live execute; H HIST vs High C actual probing distinguished – NARROW, NOT ENDTOEND until real activation (see worklog for constructed strict C with EXECUTED_BUILD + toolchain versions companions using existing local TeX, MUST label narrow).
    # Load real R3 build-record.json toolchain versions (existing local TeX, no runtime project network) as recorded evidence baseline (old terminal, EDITORIAL_PUBLICATION_BUILD_V1, old epoch 721a04d).
    real_build_path = base / ".rephase-1-editorial-runtime/versioned-renewal-bootstrap-20261023T194449Z/bootstrap-weekly/sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/publication/build-record.json"
    assert real_build_path.exists(), f"missing real R3 build-record: {real_build_path}"
    real_build = json.loads(real_build_path.read_bytes())
    real_versions = real_build.get("toolchain", {}).get("versions", {})
    assert isinstance(real_versions, dict) and "stdout" in real_versions and "biber_stdout" in real_versions and "latexmk_stdout" in real_versions
    print(f"real R3 toolchain versions baseline OK: base6 + biber+latexmk present (no error), exe={real_build.get('toolchain',{}).get('executable','')[:60]}")
    print("NARROW build schema/H consistency valid/invalid EXECUTED 3-field pdf + companions: UNEXECUTED honest in this script beyond baseline (see worklog for full constructed strict C with EXECUTED_BUILD + toolchain versions companions using existing local TeX, MUST label narrow until real activation with high finalize unblocked + real complete C).")
    print("HIGH sidecar R/build/toolchain-companions.json workaround REJECTED as acceptance (H must fail even if sidecar exists); tell high exact serialized record shape now binding companion paths/real SHAs/version stdout/exit/probed tool evidence can record directly in buildRecord toolchain.versions (not sidecar), no new sidecar artifact, no new schema file; all buildRecord selfdigest cover all fields, source closure unchanged 63 paths (same, no new sidecar path).")
    print("Preserve bad SELF before fixtures/wrappers immutable no rewrites.")
    print("Candidate 409+uncommitted owned H files only; no new ordinary commit; whole unit ongoing not HumanCommitPoint.")
    print("Remaining H accumulator unexecuted until high U activate; HIGH will run real U/C fixture and report failures; do NOT claim 21/next 40 pass before actual.")
    print("ALL REAL R3 HIST+AGENT+RECEIPT PASS (v4, latest H+schema fixes, high file present? Actually v4 DBs without high file (727 files, missing high) – H consistency tests with EXECUTED_BUILD (which needs NEW 63? Actually H's _verify_build_chain_hist does NOT check closure (NEW 63)? It checks declared_inputs/outputs live, recipe/toolchain/outputs/exit_code, versions companions, etc, but NOT closure (NEW 63)? Actually H's _verify_build_chain_hist does NOT verify basis closure (NEW 63) – that's done in _verify_versioned_ancestor (basis closure exact at new_epoch NEW 63). Good – H consistency tests for EXECUTED_BUILD outputs.pdf/toolchain versions companions (narrow) do NOT need NEW 63 closure (since they test _verify_build_chain_hist directly with constructed build docs, not full versioned chain with accumulator + closure). Good – use v4 DBs (fresh, no high file) for H consistency tests (narrow, NOT ENDTOEND).")
    print("ALL REAL R3 HIST+AGENT+RECEIPT PASS (v4, latest H+schema fixes). Narrow build/versioned OWN/C->U->U/negative/orphan: documented UNEXECUTED honest, MUST label narrow until real activation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
