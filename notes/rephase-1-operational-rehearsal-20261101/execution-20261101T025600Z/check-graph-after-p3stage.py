import sys
from pathlib import Path
WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
sys.path.insert(0, str(WORK))
from scripts import survey_discovery_v2 as disc
for issue in ["2026-W34", "SP-efficient-llm-2026"]:
    dpath = WORK / f"sources/{issue}/discovery/discovery-v2.jsonl"
    print(f"== {issue} ==")
    try:
        recs = disc.read_jsonl(dpath)
        norm = [disc._normalize_record(WORK, r, issue) for r in recs]
        disc._validate_graph(norm)
        print(f"GRAPH OK n={len(norm)}")
    except Exception as e:
        print(f"GRAPH REFUSED: {e}")
