"""Corrected source-unchanged check: workdir bytes vs proof-copy bytes (no hand-typed pins)."""
import hashlib
import sys
from pathlib import Path

WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
PROOF = Path(".rephase-1-editorial-runtime/profile-support-packaging-20261031T202327Z/proof-copy/candidate-partial-b40de60").resolve()

files = [
    "scripts/survey_screening_v2.py",
    "scripts/survey_evidence_v2.py",
    "scripts/run_evidence_v2_interactive.py",
    "scripts/run_evidence_v2_agent_first.py",
    "scripts/survey_research_authority_v2.py",
    "scripts/survey_prearchitecture_acceptance_v2.py",
]
bad = 0
for rel in files:
    a = (WORK / rel).read_bytes()
    b = (PROOF / rel).read_bytes()
    same = a == b
    bad += not same
    print(f"{'SAME ' if same else 'DIFF '} {rel} {len(a)}B sha256={hashlib.sha256(a).hexdigest()}")
print(f"mismatch count: {bad} (expect 0; log 28 DRIFT flags were mistyped expected constants in that script, corrected here)")
print("DONE-SOURCE-PINS (read-only; proof-copy never written by this unit)")
