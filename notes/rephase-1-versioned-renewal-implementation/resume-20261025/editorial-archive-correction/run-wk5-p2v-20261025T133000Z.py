#!/usr/bin/env python3
"""WEEKLY wk-ed-renew-5 fresh P2V continuation (retained complete valid + same basis, no recapture)."""
import sys, pathlib, os
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-editorial-archive-weekly-20261025T100000Z/renewal-weekly"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/editorial-archive-correction/run-wk5-p2v-20261025T133000Z"
EVID.mkdir(parents=True, exist_ok=True)
for k in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
    assert not os.environ.get(k)
HEARTBEAT = EVID / "heartbeat.txt"
HEARTBEAT.write_text(f"start {__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat()} PID={os.getpid()}\n", encoding="utf-8")
def beat(msg):
    with open(HEARTBEAT, "a", encoding="utf-8") as fh:
        fh.write(f"{__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat()} {msg} PID={os.getpid()}\n")
print(f"P2V child PID={os.getpid()}", flush=True)
beat("init")
sys.path.insert(0, str(FIX))
from scripts import survey_editorial_current_authority_v2 as p2v
beat("imports done")
res=p2v.observe_current_authority(str(FIX), 'sources/2026-W37/production-state.json', 'sources/2026-W37/publication/v2/editorial-corrections/wk-ed-renew-5/proposal.json', 'sources/2026-W37/publication/v2/editorial-corrections/wk-ed-renew-5/retained/retention-manifest.json')
print(f"P2V OK {sorted(res.keys()) if isinstance(res,dict) else type(res)} result={res.get('result') if isinstance(res,dict) else 'no'}", flush=True)
beat(f"done {res.get('result') if isinstance(res,dict) else 'ok'}")
print("P2V DONE rc0", flush=True)
beat("done rc0")
