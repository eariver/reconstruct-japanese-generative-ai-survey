#!/usr/bin/env python3
"""Public Freeze prep on actual U1 test2 Candidate + synthetic Preview (fixture type only)."""
import sys, pathlib, time
root = pathlib.Path(sys.argv[1])
cand_rel = sys.argv[2]
appr_rel = sys.argv[3]
sys.path.insert(0, str(root))
from scripts import survey_publication_v2 as pub
t0 = time.time()
prep = pub._prepare_freeze_inputs(root, root / cand_rel, root / appr_rel)
dt = time.time() - t0
print(f"PREP OK snapshot={len(prep['snapshot'])} authority={len(prep.get('renewal_authority', []))} time={dt:.2f}s")
import json
print(json.dumps({"snapshot_count": len(prep["snapshot"]), "authority_count": len(prep.get("renewal_authority", [])), "time_s": dt}))
