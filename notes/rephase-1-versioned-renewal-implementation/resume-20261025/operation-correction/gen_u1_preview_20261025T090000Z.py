#!/usr/bin/env python3
"""Synthetic Preview approval for new U1 test2 (fixture type only, NOT genuine Human approval; production semantic NO-GO)."""
import sys, pathlib, datetime
root = pathlib.Path(sys.argv[1])
cand_rel = sys.argv[2]
out_rel = sys.argv[3]
sys.path.insert(0, str(root))
from scripts import survey_publication_v2 as pub
cand = root / cand_rel
out = root / out_rel
pub.build_preview_approval(
    root, cand, out,
    reviewed_by="fixture-synthetic (NOT genuine Human)",
    reviewed_at=datetime.datetime.now(datetime.timezone.utc),
    review_reference="fixture-type-only synthetic Preview for Freeze B1 test (U1 test2, current FIXED735, no genuine approval)",
)
print(str(out.relative_to(root)))
