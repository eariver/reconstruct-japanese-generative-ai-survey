#!/usr/bin/env python3
"""HIGH-phase renewal->editorial probe — P1 prepare on a U3-activated prior.

Stages a genuinely changed authoring input (new proposal id, real text edits
to headline/deck/summary) and runs the READ-ONLY P1 prepare_proposal against
the U3-active State. P1 writes nothing; success means the renewed prior
(active U3 record + R receipt + renewed selection) is accepted as an editorial
predecessor with prior immutable versions KEEP (my P1 before-graph block) and
the identical-reader refusal correctly NOT triggering on changed bytes.
Failure returns the exact P1 code (cross-owned if in S-owned helpers).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
EVID_BASE = REPO / "notes/rephase-1-versioned-renewal-implementation/phase-high/20261024T130000Z"
EVID = EVID_BASE / "run61-20261025T110000Z"
PARENT = REPO / ".rephase-1-editorial-runtime/versioned-renewal-high24-20261025T040000Z"

PROBE = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
root, prop_new = sys.argv[1:3]
import faulthandler, os
os.environ.setdefault("ED_PROBE_DUMP", "/tmp/ed-probe-dump.txt")
try:
    _dump_path = os.environ.get("ED_PROBE_DUMP_PATH", "")
    if _dump_path:
        faulthandler.dump_traceback_later(180, repeat=True, file=open(_dump_path, "w"))
except Exception:
    pass
from pathlib import Path
root_p = Path(root)
from scripts import survey_production_v2 as core
from scripts import survey_editorial_correction_proposal_v2 as p1mod
assert str(Path(p1mod.__file__).resolve()).startswith(str(root_p.resolve())), "fixture origin"
issue = "2026-W37"
pdir_old = f"sources/{issue}/publication/v2/editorial-corrections/wk-boot-1"
pdir_new = f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}"
old_auth = json.loads((root_p / pdir_old / "authoring-input.json").read_bytes())
new_auth = json.loads(json.dumps(old_auth))
new_auth["cover"]["headline"] = ("Renewal-editorial probe headline: same-reader corpus gains a "
    "fixture-local editorial amendment after versioned renewal; no genuine approval implied.")
new_auth["cover"]["deck"] = ("Probe deck asserting changed-reader bytes for P1 repeated "
    "pre-Preview on a U3-activated prior.")
new_auth["final_summary"]["paragraphs"] = (["Probe paragraph: this changed authoring must NOT trip "
    "NO_EDITORIAL_CHANGE; prior immutable versions stay KEEP with fresh State COPY."])
assert json.dumps(new_auth, sort_keys=True) != json.dumps(old_auth, sort_keys=True), "change must differ"
dest = root_p / pdir_new / "authoring-input.json"
dest.parent.mkdir(parents=True, exist_ok=True)
if dest.exists():
    print(json.dumps({"probe": "REFUSED_TARGET_EXISTS", "path": str(dest.relative_to(root_p))}))
else:
    dest.write_bytes(core.json_bytes(new_auth))
    res = p1mod.prepare_proposal(root_p, root_p / f"sources/{issue}/production-state.json",
                                 dest, prop_new,
                                 "Renewal-to-editorial probe: changed reader on U3-active prior")
    print(json.dumps({"probe": "PREPARED", "proposal_id": prop_new,
                      "keys": sorted(res.keys()) if isinstance(res, dict) else type(res).__name__}))
"""


def main() -> int:
    EVID.mkdir(parents=True, exist_ok=True)
    (EVID / "commands.log").write_text("", encoding="utf-8")
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        if os.environ.get(name):
            print(f"FATAL: inherited {name}", file=sys.stderr)
            return 1
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["LC_ALL"] = "C"
    env["ED_PROBE_DUMP_PATH"] = str(EVID / "ed-probe-stacks.txt")
    root = str(PARENT / "renewal-weekly")
    prop_new = sys.argv[1] if len(sys.argv) > 1 else "ed-renew-1"
    proc = subprocess.run([sys.executable, "-c", PROBE, root, prop_new],
                          cwd=str(REPO), capture_output=True, text=True, timeout=3000, env=env)
    (EVID / "ed-probe-stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (EVID / "ed-probe-stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    (EVID / "ed-probe-exit.txt").write_text(str(proc.returncode), encoding="utf-8")
    with open(EVID / "commands.log", "a", encoding="utf-8") as fh:
        fh.write(f"$ probe {prop_new} -> exit={proc.returncode}\n")
    print(proc.stdout.strip()[-500:] if proc.stdout else f"exit={proc.returncode}", flush=True)
    print("DONE ED-PROBE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
