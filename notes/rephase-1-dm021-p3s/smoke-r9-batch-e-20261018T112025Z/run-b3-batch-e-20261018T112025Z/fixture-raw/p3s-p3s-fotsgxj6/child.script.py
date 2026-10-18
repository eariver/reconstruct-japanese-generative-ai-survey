
import json, sys
from pathlib import Path
root = Path(sys.argv[1]); proposal_path = Path(sys.argv[2]); staged_path = Path(sys.argv[3])
from scripts import survey_editorial_staged_source_v2 as staged
try:
    out = staged.verify_staged_source(root, proposal_path, staged_path)
    print(json.dumps({"ok": True, "result": out["result"],
                      "reader": out["measured"]["proposed_reader_sha256"]}))
except Exception as exc:
    code = getattr(exc, "code", type(exc).__name__)
    phase = getattr(exc, "phase", "")
    disp = getattr(exc, "disposition", "")
    print(json.dumps({"ok": False, "error": f"{type(exc).__name__}: {exc}"[:2000],
                      "code": code, "phase": phase, "disposition": disp}))
