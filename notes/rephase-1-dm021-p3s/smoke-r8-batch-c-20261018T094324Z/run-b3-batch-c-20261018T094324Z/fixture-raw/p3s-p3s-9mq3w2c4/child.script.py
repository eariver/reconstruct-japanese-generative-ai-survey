
import json, sys
from pathlib import Path
root = Path(sys.argv[1])
state_path = Path(sys.argv[2]); proposal_path = Path(sys.argv[3])
manifest_path = Path(sys.argv[4]); scope_path = Path(sys.argv[5])
from scripts import survey_editorial_staged_source_v2 as staged
try:
    out = staged.materialize_staged_source(root, state_path, proposal_path, manifest_path, scope_path)
    print(json.dumps({"ok": True, "result": out["result"],
                      "staged": out["staged_manifest_ref"]["path"],
                      "digest": out["manifest_digest"], "head": out["observed_head"]}))
except Exception as exc:
    owned = getattr(exc, "owned", {})
    code = getattr(exc, "code", type(exc).__name__)
    phase = getattr(exc, "phase", "")
    disp = getattr(exc, "disposition", "")
    print(json.dumps({"ok": False, "error": f"{type(exc).__name__}: {exc}"[:2000],
                      "code": code, "phase": phase, "disposition": disp,
                      "owned_files": len(owned.get("owned_files", [])) if isinstance(owned, dict) else 0,
                      "owned": owned if isinstance(owned, dict) else {}}))
