#!/usr/bin/env python3
"""Batch-09 CURRENT proof capture (packet-only). Runs current_proof_harness.py with verbose raw capture."""
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
BATCH = PACKET / "test-runs/batch-09-current-proof"
BATCH.mkdir(parents=True, exist_ok=True)

def pins(root: Path):
    out = []
    for p in sorted(root.rglob("*")):
        if ".git" in p.parts or "__pycache__" in p.parts or p.suffix == ".pyc" or p.is_dir():
            continue
        rel = p.relative_to(root).as_posix()
        out.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()} {p.stat().st_size} {oct(p.stat().st_mode & 0o777)} {rel}")
    return out

before = pins(SNAP)
(BATCH / "pins-before.txt").write_text("\n".join(before) + "\n", encoding="utf-8")
argv = [sys.executable, str(PACKET / "current_proof_harness.py")]
(BATCH / "argv.txt").write_text(" ".join(argv) + "\n", encoding="utf-8")
(BATCH / "cwd.txt").write_text("/home/eariver/git/reconstruct-japanese-generative-ai-survey\n", encoding="utf-8")
env = {"PATH": os.environ.get("PATH", ""), "PYTHONDONTWRITEBYTECODE": "1", "PYTHONPATH": str(SNAP), "LANG": "C.UTF-8"}
(BATCH / "env.txt").write_text("\n".join(f"{k}={v}" for k, v in sorted(env.items())) + "\n", encoding="utf-8")
start = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
(BATCH / "wall-start.txt").write_text(start + "\n", encoding="utf-8")
proc = subprocess.Popen(argv, cwd="/home/eariver/git/reconstruct-japanese-generative-ai-survey",
                        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONPATH": str(SNAP)},
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
(BATCH / "pid.txt").write_text(str(proc.pid) + "\n", encoding="utf-8")
try:
    so, se = proc.communicate(timeout=900)
    rc = proc.returncode
    to = False
except subprocess.TimeoutExpired:
    proc.kill(); so, se = proc.communicate(); rc = 124; to = True
end = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
(BATCH / "wall-end.txt").write_text(end + "\n", encoding="utf-8")
(BATCH / "stdout.txt").write_text(so or "", encoding="utf-8")
(BATCH / "stderr.txt").write_text(se or "", encoding="utf-8")
(BATCH / "exit.txt").write_text(str(rc) + "\n", encoding="utf-8")
(BATCH / "meta.json").write_text(json.dumps({"batch": "batch-09-current-proof", "pid": proc.pid, "argv": argv, "cwd": "/home/eariver/git/reconstruct-japanese-generative-ai-survey", "wall_start": start, "wall_end": end, "exit": rc, "timed_out": to}, indent=2) + "\n", encoding="utf-8")
after = pins(SNAP)
(BATCH / "pins-after.txt").write_text("\n".join(after) + "\n", encoding="utf-8")
(BATCH / "pins-same.txt").write_text("YES\n" if before == after else "NO\n", encoding="utf-8")
print(f"batch-09 exit={rc} timed_out={to} pins_same={before==after} stdout_bytes={len(so or '')} stderr_bytes={len(se or '')}", flush=True)
sys.exit(0 if rc == 0 else 1)
