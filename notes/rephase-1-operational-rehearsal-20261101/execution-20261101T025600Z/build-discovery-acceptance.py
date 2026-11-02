"""Build + validate fresh Discovery acceptance via normal public API (no State advance).

Inputs: workdir discovery JSONL + NEW X manifests (COMPLETE) + staged Raw.
Old acceptance DATA stays archived in intake; new acceptance is fresh bytes.
No state transition here (review seam follows).
"""
import sys
from pathlib import Path

WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
sys.path.insert(0, str(WORK))
from scripts import survey_discovery_v2 as disc

for issue in ["2026-W34", "SP-efficient-llm-2026"]:
    print(f"===== {issue} =====")
    dpath = WORK / f"sources/{issue}/discovery/discovery-v2.jsonl"
    xmpath = WORK / f"sources/{issue}/external/x/x-source-intake-v2.json"
    outp = WORK / f"sources/{issue}/discovery/discovery-accepted-v2.json"
    print(f"exists discovery: {dpath.is_file()} X: {xmpath.is_file()} acceptance (must be missing): {outp.exists()}")
    assert dpath.is_file() and xmpath.is_file() and not outp.exists()
    built = disc.build_acceptance(WORK, dpath, xmpath, issue, outp)
    print(f"built: {built.relative_to(WORK)}")
    acc = disc.validate_acceptance(WORK, outp)
    print(f"validated: record_count={acc['record_count']} graph_sha={acc['graph_sha256'][:12]}... x={acc['x_source_intake']}")
print("DONE-ALL")
