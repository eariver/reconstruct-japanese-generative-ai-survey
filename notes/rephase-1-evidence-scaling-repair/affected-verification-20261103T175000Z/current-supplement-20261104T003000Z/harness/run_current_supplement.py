#!/usr/bin/env python3
"""Capture wrapper for NEW CURRENT supplement (packet-only)."""
from __future__ import annotations
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

PACKET = Path(__file__).resolve().parent
SNAP = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/evidence-scaling-affected-verify-20261103T175000Z/snapshot-fixed")
SUPPLEMENT = PACKET / "current-supplement-20261104T003000Z"
SUPPLEMENT.mkdir(parents=True, exist_ok=False)
RUNS = SUPPLEMENT / "raw"
RUNS.mkdir(parents=True, exist_ok=False)

def _pins_771(root: Path):
    rows = []
    for p in sorted(root.rglob("*")):
        if ".git" in p.parts or "__pycache__" in p.parts or p.suffix == ".pyc" or p.is_dir():
            continue
        rows.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()} {p.stat().st_size} {oct(p.stat().st_mode & 0o777)} {p.relative_to(root).as_posix()}")
    return rows

before = _pins_771(SNAP)
(RUNS / "pins-snap-before-771.txt").write_text("\n".join(before) + "\n", encoding="utf-8")
assert len(before) == 771, f"SNAP 771 expected, got {len(before)}"
argv = [sys.executable, "-B", str(PACKET / "current_supplement_proof.py")]
(RUNS / "argv.txt").write_text(" ".join(argv) + "\n", encoding="utf-8")
(RUNS / "cwd.txt").write_text("/home/eariver/git/reconstruct-japanese-generative-ai-survey\n", encoding="utf-8")
env_show = {"PATH": os.environ.get("PATH", ""), "PYTHONDONTWRITEBYTECODE": "1", "PYTHONPATH": str(SNAP), "LANG": "C.UTF-8"}
(RUNS / "env.txt").write_text("\n".join(f"{k}={v}" for k, v in sorted(env_show.items())) + "\n", encoding="utf-8")
start = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
(RUNS / "wall-start.txt").write_text(start + "\n", encoding="utf-8")
proc = subprocess.Popen(argv, cwd="/home/eariver/git/reconstruct-japanese-generative-ai-survey",
                        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONPATH": str(SNAP)},
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
(RUNS / "pid.txt").write_text(str(proc.pid) + "\n", encoding="utf-8")
try:
    so, se = proc.communicate(timeout=900)
    rc = proc.returncode
    to = False
except subprocess.TimeoutExpired:
    proc.kill(); so, se = proc.communicate(); rc = 124; to = True
end = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
(RUNS / "wall-end.txt").write_text(end + "\n", encoding="utf-8")
(RUNS / "stdout.txt").write_text(so or "", encoding="utf-8")
(RUNS / "stderr.txt").write_text(se or "", encoding="utf-8")
(RUNS / "exit.txt").write_text(str(rc) + "\n", encoding="utf-8")
(RUNS / "meta.json").write_text(json.dumps({"argv": argv, "pid": proc.pid, "cwd": "/home/eariver/git/reconstruct-japanese-generative-ai-survey", "wall_start": start, "wall_end": end, "exit": rc, "timed_out": to}, indent=2) + "\n", encoding="utf-8")
after = _pins_771(SNAP)
(RUNS / "pins-snap-after-771.txt").write_text("\n".join(after) + "\n", encoding="utf-8")
(RUNS / "pins-same.txt").write_text("YES\n" if before == after else "NO\n", encoding="utf-8")
print(f"supplement exit={rc} timed_out={to} pins_same={before==after}", flush=True)
sys.exit(0 if rc == 0 else 1)
