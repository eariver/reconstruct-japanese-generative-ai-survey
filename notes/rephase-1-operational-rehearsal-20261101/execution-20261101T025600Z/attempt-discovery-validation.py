import sys
from pathlib import Path
WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
sys.path.insert(0, str(WORK))
from scripts import survey_discovery_v2 as disc
# Stage intake DATA copies as input-archive references (not active acceptance yet)
# Try validating historical accepted bytes if staged; here we only have discovery JSONL in active source,
# acceptance files live in input-archive (not copied to active source per no-old-State rule).
# Attempt 1: validate that active discovery JSONL normalizes (Raw-gated) — expect Raw-missing fail-close
for issue in ["2026-W34", "SP-efficient-llm-2026"]:
    dpath = WORK / f"sources/{issue}/discovery/discovery-v2.jsonl"
    print(f"== {issue} discovery JSONL normalize ==")
    try:
        recs = disc.read_jsonl(dpath)
        norm = [disc._normalize_record(WORK, r, issue) for r in recs]
        disc._validate_graph(norm)
        print(f"OK graph n={len(norm)}")
    except Exception as e:
        print(f"REFUSED: {e}")
# Attempt 2: historical acceptance files are in intake (not installed to active source); confirm they exist as DATA
import pathlib
for p in ["notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2b02.discovery-accepted-v2.json",
          "notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2b21.discovery-accepted-v2.json"]:
    pp = pathlib.Path(p)
    print(pp.name, "exists", pp.exists(), "bytes", pp.stat().st_size if pp.exists() else None)
