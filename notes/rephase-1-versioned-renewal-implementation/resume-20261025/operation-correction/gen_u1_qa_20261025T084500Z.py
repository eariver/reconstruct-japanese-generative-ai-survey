#!/usr/bin/env python3
"""Generate fresh QA checks for new U1 (fixture type only, synthetic; genuine in production)."""
import sys, json, pathlib, datetime
root = pathlib.Path(sys.argv[1])
basis_rel = sys.argv[2]
out_rel = sys.argv[3]
sys.path.insert(0, str(root))
from scripts import survey_production_v2 as core
from scripts import survey_quality_v2 as quality
basis = json.loads((root / basis_rel).read_bytes())
cfg = json.loads((root / "config/survey-production-v2.json").read_bytes())
kinds = quality.expected_checks_by_kind(cfg, basis["research_profile"], basis["publication_profile"], {"DETERMINISTIC"})
prior_seal = json.loads((root / basis["prior_selected_ref"]["path"]).read_bytes())
roles = prior_seal["roles"]
trio_primary, pdf_role = roles["validated-source"], roles["publication-pdf"]
main_bytes = (root / trio_primary["path"]).read_bytes()
pdf_bytes = (root / pdf_role["path"]).read_bytes()
from pypdf import PdfReader
pages = len(PdfReader(str(root / pdf_role["path"])).pages)
now = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
evidence = "renewal high-u1-test fresh U (fixture type only, synthetic; genuine in production)"
# Agent-first contract (FIXED735, H closing config epoch): {check_id,kind,status,executor,evidence,recorded_at,result}
# DETERMINISTIC result is {path,sha256} file authority (must exist live, SHA must match).
payloads = {
    "SUBJECT_ENTITY_PROPERTY_BINDING": {"check_id": "SUBJECT_ENTITY_PROPERTY_BINDING", "kind": "DETERMINISTIC", "status": "PASS", "executor": "test", "evidence": evidence, "recorded_at": now, "result": {"path": trio_primary["path"], "sha256": core.sha256_bytes(main_bytes)}},
    "IDENTIFIER_PRESERVATION": {"check_id": "IDENTIFIER_PRESERVATION", "kind": "DETERMINISTIC", "status": "PASS", "executor": "test", "evidence": evidence, "recorded_at": now, "result": {"path": trio_primary["path"], "sha256": core.sha256_bytes(main_bytes)}},
    "PDF_PREFLIGHT": {"check_id": "PDF_PREFLIGHT", "kind": "DETERMINISTIC", "status": "PASS", "executor": "test", "evidence": evidence, "recorded_at": now, "result": {"path": pdf_role["path"], "sha256": core.sha256_bytes(pdf_bytes)}},
}
assert set(payloads) == set(kinds), f"{sorted(payloads)} != {sorted(kinds)}"
rows = [payloads[cid] for cid in sorted(payloads)]
out = root / out_rel
out.write_text(json.dumps({"checks": rows}, indent=1))
print(str(out.relative_to(root)))
