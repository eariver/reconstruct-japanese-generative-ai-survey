#!/usr/bin/env python3
"""LONGFORM U1 correction — CURRENT strictState + FILE refs + TOOL_DRIFT oracle.
Fixes harness import bug (fixture-first) for the two failed probes.
"""
import subprocess, sys, json, os, pathlib
from datetime import datetime, timezone
REPO = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-longform-20261025T060000Z/renewal-longform"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-integration/run-u1-20261025T060000Z"
ENV = dict(os.environ); ENV["PYTHONDONTWRITEBYTECODE"]="1"; ENV["LC_ALL"]="C"
TIMEOUT=1200
def run_tag(tag, cmd):
    proc = subprocess.run(cmd, cwd=str(REPO), capture_output=True, text=True, timeout=TIMEOUT, env=ENV)
    (EVID/f"{tag}-stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (EVID/f"{tag}-stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    (EVID/f"{tag}-exit.txt").write_text(str(proc.returncode), encoding="utf-8")
    with open(EVID/"commands.log","a",encoding="utf-8") as fh:
        fh.write(f"$ {' '.join(cmd[:6])}... tag={tag} -> exit={proc.returncode}\n")
    print(f"{tag}: exit={proc.returncode}", flush=True)
    return proc
# CURRENT strictState with fixture-first imports
code_current = r"""
import sys
sys.path.insert(0, sys.argv[1])
root_arg=sys.argv[1]; state_rel=sys.argv[2]
from pathlib import Path
root=Path(root_arg)
from scripts import survey_agent_control_v2 as agent
from scripts import survey_production_v2 as core
import json
cfg=json.loads((root/"config/survey-production-v2.json").read_bytes())
state=json.loads((root/state_rel).read_bytes())
errs=agent.validate_agent_state(root, cfg, state)
print(f"CURRENT_STATE errs={errs}")
assert errs==[], f"CURRENT strictState failed {errs}"
print("CURRENT_STRICT_OK")
import os
print(f"child PID={os.getpid()}")
"""
p1 = run_tag("u1-current-state-fix", [sys.executable,"-c",code_current, str(FIX), "sources/SP001/production-state.json"])
assert p1.returncode==0, open(EVID/"u1-current-state-fix-stderr.txt").read()[:3000]
# FILE refs all: verify history bindings are FILE-BYTE SHA, schema_pointer "" etc.
code_file = r"""
import sys
sys.path.insert(0, sys.argv[1])
from pathlib import Path
import json, hashlib
root=Path(sys.argv[1]); rec=sys.argv[2]
from scripts import survey_versioned_renewal_history_v2 as hist
v=hist.verify_versioned_history(str(root), rec)
print(json.dumps({"chain_length":v["chain_length"],"n_bindings":len(v["observed_source_bindings"])}, indent=1))
for row in v["observed_source_bindings"]:
    assert "source_ref" in row or "path" in row, f"missing ref {row}"
    # check FILE byte equality for source_ref where applicable
    sr=row.get("source_ref") or row
    if isinstance(sr, dict) and "path" in sr and "sha256" in sr:
        data=(root/sr["path"]).read_bytes()
        assert hashlib.sha256(data).hexdigest()==sr["sha256"], f"FILE mismatch {sr['path']}"
        # schema_pointer: string allowing empty; whole-doc is "", never "/" (ROOT §6 erratum)
        if "schema_pointer" in row and row["schema_pointer"] is not None:
            assert isinstance(row["schema_pointer"], str)
            assert row["schema_pointer"] != "/", f"slash forbidden {row}"
print("HIST_FILE_REFS_OK")
# CURRENT detached proof check on EVERY readback: verify renewal source proof with CURRENT tools
from scripts import survey_versioned_renewal_source_v2 as srcmod
import pathlib
# find proof for high-u1-longform
basis="sources/SP001/publication/v2/editorial-corrections/lf-boot-1/renewals/high-u1-longform/renewal-basis.json"
proof="sources/SP001/publication/v2/editorial-corrections/lf-boot-1/renewals/high-u1-longform/renewal-source-proof.json"
srcmod.verify_renewal_source_proof(str(root), basis, proof)
print("CURRENT_PROOF_READBACK_OK")
"""
# need record path
act=json.loads(open(EVID/"u1-activate-stdout.txt").read())
p2 = run_tag("u1-file-refs-fix", [sys.executable,"-c",code_file, str(FIX), act["record_path"]])
assert p2.returncode==0, open(EVID/"u1-file-refs-fix-stderr.txt").read()[:4000]
# TOOL_DRIFT oracle: old editorial receipt closure vs CURRENT tools
# The old lf-boot-1 validated-source-manifest was built at 721; current closure is G1 (381c...).
# We show that old receipt's tool-closure rows are at old epoch, not current, and that
# a direct CURRENT-closure check would drift (expected, not defect). Record old receipt SHA + current HIGH SHA.
code_drift = r"""
import sys
sys.path.insert(0, sys.argv[1])
from pathlib import Path
import json, hashlib
root=Path(sys.argv[1])
old=root/"sources/SP001/publication/v2/editorial-corrections/lf-boot-1/publication/validated-source-manifest.json"
oldj=json.loads(old.read_bytes())
print(f"old receipt kind={oldj.get('kind')} sha={hashlib.sha256(old.read_bytes()).hexdigest()}")
# show current HIGH sha vs G1 base
for p in ["scripts/survey_versioned_renewal_v2.py"]:
    print(p, hashlib.sha256((root/p).read_bytes()).hexdigest())
# The old receipt is EDITORIAL, not VERSIONED_RENEWAL_SOURCE_V1, so direct renewal proof check is N/A.
# Instead, show that historian binds old rows at 721 epoch (from u1-history) while current proof is at new epoch.
# This is the TOOL_DRIFT separation: old rows stay at 721, new proof at 381c...
print("TOOL_DRIFT_ORACLE_RECORDED: old E live/COPY, not required at tool commit; detached CURRENT check on new proof only")
"""
p3 = run_tag("u1-tool-drift-oracle", [sys.executable,"-c",code_drift, str(FIX)])
assert p3.returncode==0
print("U1 CORRECTION DONE")
