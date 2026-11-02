"""Final read-only verification: states, accepted products, source pins, no-op proofs."""
import hashlib
import json
import sys
from pathlib import Path

WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
sys.path.insert(0, str(WORK))
from scripts import survey_production_v2 as core
from scripts import survey_agent_control_v2 as agent

print(f"HEAD={core.repository_commit_sha(WORK)} (must equal 48082356...)")
for issue, exp in [("2026-W34", "DISCOVERY_COLLECTED"), ("SP-efficient-llm-2026", "CANDIDATES_NORMALIZED")]:
    cfg = core.load_json(WORK / core.DEFAULT_CONFIG)
    st = core.load_json(WORK / f"sources/{issue}/production-state.json")
    errs = agent.validate_agent_state(WORK, cfg, st)
    print(f"{issue}: lifecycle={st['lifecycle_state']} (expect {exp}) agent_errors={errs}")
    print(f"  state_sha={core.sha256_file(WORK / f'sources/{issue}/production-state.json')}")
    print(f"  checkpoints passed: {[k for k,v in st['machine_checkpoints'].items() if v=='passed']}")

# source138 runtime pins unchanged (independent review §0 pins)
pins = {
    "scripts/survey_screening_v2.py": "f0f289540302753b2e7cad5f4fded1df0387ca1403309a032a733199c42d5a1",
    "scripts/survey_evidence_v2.py": "36b7b5832845ea86ac69a3097f984697f980b0148fdf454736",
    "scripts/run_evidence_v2_interactive.py": "5a6280ac19986a05e363a673dd57294ed6d4357355fdb988d9cdd6f5db812",
    "scripts/run_evidence_v2_agent_first.py": "f73f2ab91fc88a5794d3f534d0958ed32a80eddfd6b48ec106d544714651a91eb",
    "scripts/survey_research_authority_v2.py": "546bbad1cfc84cd28e984b3652df08b52a07e5015dcf2836717fb64238212737",
    "scripts/survey_prearchitecture_acceptance_v2.py": "388c89941cef393868c9a2cef5ad7276889ffa01aeda294e756c9f76b6f9efd4",
}
bad = 0
for rel, want in pins.items():
    got = hashlib.sha256((WORK / rel).read_bytes()).hexdigest()
    ok = got == want
    bad += not ok
    print(f"runtime {'OK ' if ok else 'DRIFT '} {rel} {got[:12]}...")
print(f"runtime drift count: {bad} (expect 0; no source edits this unit)")

ev = WORK / "sources/SP-efficient-llm-2026/evidence/v2/accepted/09f487ab1ecb6dc7dd3851ba8791c02fba85d6ecb0d0aac834432a3b701b8e2f/evidence-accepted.json"
print(f"SP evidence accepted: {ev.exists()} sha={hashlib.sha256(ev.read_bytes()).hexdigest()[:16]}...")
sp = WORK / "sources/SP-efficient-llm-2026/screening/v2/accepted/9b9796295c2ddf28b087fc725b78b7d089d6e946a5a5ba65ab51601d58f558a9/screening-accepted.json"
print(f"SP screening accepted: {sp.exists()} sha={hashlib.sha256(sp.read_bytes()).hexdigest()[:16]}...")
w = WORK / "sources/2026-W34/screening/v2/accepted/e193ad0507895568e369437833b87d2610d68ef50f0c6419b092f5711e26bbea/screening-accepted.json"
print(f"W34 screening accepted: {w.exists()} sha={hashlib.sha256(w.read_bytes()).hexdigest()[:16]}...")
print("DONE-FINAL-VERIFY (read-only)")
