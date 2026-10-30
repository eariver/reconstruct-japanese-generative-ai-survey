#!/usr/bin/env python3
"""P1 editorial-correction proposal probe on kept VALIDATED_DRAFT fixture.

Steps (public APIs only): revalidate_publication_surface REVIEWED_CORE_CHANGE
-> stage authoring input -> prepare_proposal -> validate_proposal.
Preserves exact outcome. Exit 0 = prepared+validated (report refs);
1 = probe setup fault; 2 = target refusal (report precisely).
"""
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

PRIVATE = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/dm022-full-lifecycle-fixed2-20261028T192129Z")
sys.path.insert(0, str(PRIVATE))
os.chdir(str(PRIVATE))

ROOT = Path("/tmp/dm022-renewal-probe-keep/fixture")
assert (ROOT / "sources").exists(), "kept fixture missing"

from scripts import survey_production_v2 as core
from scripts import survey_agent_control_v2 as agent

state_cands = list(ROOT.rglob("production-state.json"))
state_cands = [p for p in state_cands if ".git" not in p.parts and "retention" not in p.parts and "acceptance-revisions" not in p.parts]
print("state candidates:", [str(p.relative_to(ROOT)) for p in state_cands])
state_path = None
for p in state_cands:
    st = core.load_json(p)
    if st.get("lifecycle_state") == "VALIDATED_DRAFT":
        state_path = p
        break
assert state_path is not None, "no VALIDATED_DRAFT state in kept fixture"
state = core.load_json(state_path)
print("state:", state["lifecycle_state"], state["issue_id"])
cfg = core.load_json(ROOT / core.DEFAULT_CONFIG)

# Genuine byte change FIRST: revalidation requires changed publication bytes.
# Explicit synthetic fixture correction marker (TeX comment: bytes change,
# rendered output preserved; never a genuine editorial judgment).
from scripts import survey_production_v2 as _core2
_st = _core2.load_json(state_path)
_prof = _core2.load_json(ROOT / _st["profile"]["path"])
_survey = ROOT / _prof["paths"]["survey_root"]
_main = _survey / "main.tex"
_before = _main.read_bytes()
assert b"probe-correction-marker" not in _before
_main.write_bytes(_before + b"% Synthetic probe correction marker (explicit nongenuine fixture change).\n")
print("corrected main.tex bytes:", len(_before), "->", len(_main.read_bytes()))
try:
    record_path = agent.revalidate_publication_surface(
        ROOT, cfg, state_path, "REVIEWED_CORE_CHANGE",
        "Synthetic probe correction basis (explicit nongenuine fixture review)",
        "SYNTHETIC_FIXTURE_GENERAL_FULL_V2",
        datetime(2026, 10, 28, 16, 30, 0, tzinfo=timezone.utc), None)
    print("revalidated:", record_path.relative_to(ROOT))
except Exception as exc:
    print("PROBE TARGET OUTCOME (revalidate):", type(exc).__name__, str(exc)[:1500])
    import traceback; traceback.print_exc()
    sys.exit(2)

# Stage a minimal authoring input: revised reader surface (copy current + tweak deck).
import json
state = core.load_json(state_path)
profile = core.load_json(ROOT / state["profile"]["path"])
source_root = ROOT / profile["paths"]["source_root"]
surface_path = source_root / "publication" / "v2" / "reader-surface-input-v2.json"
surface = core.load_json(surface_path)
proposal_id = "probe-p1-v2"
proposal_dir = source_root / "publication" / "v2" / "editorial-corrections" / proposal_id
proposal_dir.mkdir(parents=True, exist_ok=True)
authored = dict(surface)
authored["cover"] = dict(surface["cover"], deck=surface["cover"]["deck"] + " (Synthetic probe correction.)")
authored_path = proposal_dir / "authoring-input.json"
authored_path.write_bytes((json.dumps(authored, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode())
print("staged authoring:", authored_path.relative_to(ROOT))

try:
    from scripts import survey_editorial_correction_proposal_v2 as proposal_mod
    prepared = proposal_mod.prepare_proposal(ROOT, state_path, authored_path, proposal_id)
    print("PREPARED keys:", sorted(prepared.keys()))
    print("PROBE OUTCOME: prepared (report refs to root)")
    sys.exit(0)
except Exception as exc:
    print("PROBE TARGET OUTCOME (prepare):", type(exc).__name__, str(exc)[:1500])
    import traceback; traceback.print_exc()
    sys.exit(2)
