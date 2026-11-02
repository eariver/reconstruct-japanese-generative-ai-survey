import sys
from pathlib import Path
WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
sys.path.insert(0, str(WORK))
from scripts import survey_discovery_v2 as disc
recs = disc.read_jsonl(WORK/"sources/SP-efficient-llm-2026/discovery/discovery-v2.jsonl")
print("n", len(recs))
try:
  norm = [disc._normalize_record(WORK, r, "SP-efficient-llm-2026") for r in recs]
  disc._validate_graph(norm)
  print("SP discovery graph OK", len(norm))
except Exception as e:
  print("SP discovery graph FAIL:", e)
