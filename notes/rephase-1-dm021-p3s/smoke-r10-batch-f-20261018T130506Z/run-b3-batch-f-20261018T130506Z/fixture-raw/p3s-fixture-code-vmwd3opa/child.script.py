
import sys
from pathlib import Path
from datetime import datetime, timezone
root = Path(sys.argv[1])
state_path = Path(sys.argv[2])
from scripts import survey_production_v2 as core
from scripts import survey_weekly_mechanical_refresh_v2 as r1
cfg = core.load_json(root / core.DEFAULT_CONFIG)
recorded = datetime(2026, 9, 19, 8, 0, 0, tzinfo=timezone.utc)
result = r1.refresh_mechanical_evidence(root, cfg, state_path, "fixture R1 non-emitted refresh", "synthetic P1 R1 fixture", recorded)
print(core.sha256_object(result)[:16])
