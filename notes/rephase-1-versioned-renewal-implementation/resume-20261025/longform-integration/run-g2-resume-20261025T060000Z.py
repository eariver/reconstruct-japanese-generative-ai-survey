#!/usr/bin/env python3
"""LONGFORM G2 C1 resume — finalize/activate/history after PID-line parse fix."""
import subprocess, sys, json, os, pathlib
from datetime import datetime, timezone
REPO = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-longform-20261025T060000Z/renewal-longform"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-integration/run-g2-20261025T060000Z"
ENV=dict(os.environ); ENV["PYTHONDONTWRITEBYTECODE"]="1"; ENV["LC_ALL"]="C"
TIMEOUT=1200
def run_tag(tag, cmd):
    proc=subprocess.run(cmd, cwd=str(REPO), capture_output=True, text=True, timeout=TIMEOUT, env=ENV)
    (EVID/f"{tag}-stdout.txt").write_text(proc.stdout or "",encoding="utf-8")
    (EVID/f"{tag}-stderr.txt").write_text(proc.stderr or "",encoding="utf-8")
    (EVID/f"{tag}-exit.txt").write_text(str(proc.returncode),encoding="utf-8")
    with open(EVID/"commands.log","a",encoding="utf-8") as fh:
        fh.write(f"$ {' '.join(cmd[:6])}... tag={tag} -> exit={proc.returncode}\n")
    print(f"{tag}: exit={proc.returncode}",flush=True)
    return proc
def cli(root, args, tag):
    return run_tag(tag, [sys.executable,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; sys.exit(main(sys.argv[2:]))", root]+args)
# parse outs handling PID line
raw=open(EVID/"c1-reviews-qa-stdout.txt").read()
print(f"raw reviews-qa stdout first 200: {raw[:200]}")
# find first { 
idx=raw.find("{")
outs=json.loads(raw[idx:])
print(f"outs={outs}")
# reuse now_c
now_c=open(EVID/"now-iso-c1.txt").read().strip()
print(f"now_c={now_c}")
issue="SP001"; prop="lf-boot-1"; rid="high-c1-longform"
state=f"sources/{issue}/production-state.json"
pdir=f"sources/{issue}/publication/v2/editorial-corrections/{prop}"
basis_rel=f"{pdir}/renewals/{rid}/renewal-basis.json"
fc = cli(str(FIX), ["finalize","--root",str(FIX),"--state",state,"--basis",basis_rel,"--checks",outs["checks"],"--semantic-review",outs["SEMANTIC_EDITORIAL"],"--visual-review",outs["VISUAL"],"--executor","longform-g2-c1","--recorded-at",now_c], "c1-finalize")
assert fc.returncode==0, f"c1 finalize failed {open(EVID/'c1-finalize-stderr.txt').read()[:5000]}"
fin=json.loads(open(EVID/"c1-finalize-stdout.txt").read())
print(f"c1 finalize set={fin['set_path']} disposition={fin['disposition']}")
assert fin["disposition"]=="NEW_TARGETS"
ac = cli(str(FIX), ["activate","--root",str(FIX),"--state",state,"--set",fin["set_path"],"--reason","Core change: LONGFORM G2 style+Core comment with new rendered targets (real TL build)","--executor","longform-g2-c1","--recorded-at",now_c], "c1-activate")
assert ac.returncode==0, f"c1 activate failed {open(EVID/'c1-activate-stderr.txt').read()[:4000]}"
act=json.loads(open(EVID/"c1-activate-stdout.txt").read())
print(f"c1 activate {act}")
hc = cli(str(FIX), ["history","--root",str(FIX),"--record",act["record_path"]], "c1-history")
assert hc.returncode==0
print(open(EVID/"c1-history-stdout.txt").read()[:5000])
print("G2 C1 RESUME DONE")
