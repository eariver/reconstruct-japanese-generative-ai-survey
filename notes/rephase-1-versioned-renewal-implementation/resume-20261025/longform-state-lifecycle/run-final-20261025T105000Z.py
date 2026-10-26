#!/usr/bin/env python3
"""PHASE5 final actualState lifecycle RELEASED + public validate-state API/CLI + proof/Candidate/history/release-readback + exact write window."""
import os, sys, json, subprocess, time, hashlib
from datetime import datetime, timezone
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
PARENT = REPO / ".rephase-1-editorial-runtime/versioned-renewal-longform-lifecycle-20261025T100000Z"
FIX = PARENT / "renewal-longform-lifecycle"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-state-lifecycle/phase-final-20261025T105000Z"
EVID.mkdir(parents=True, exist_ok=True)
if not (EVID/"commands.log").exists():
    (EVID/"commands.log").write_text("", encoding="utf-8")
for k in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
    assert not os.environ.get(k)
ENV=dict(os.environ); ENV["PYTHONDONTWRITEBYTECODE"]="1"; ENV["LC_ALL"]="C"
ENV["TMPDIR"]=str(PARENT/"tmp"); ENV["TMP"]=str(PARENT/"tmp"); ENV["TEMP"]=str(PARENT/"tmp")
TIMEOUT=1200
ISSUE="SP001"; STATE_REL=f"sources/{ISSUE}/production-state.json"
def run_tag(tag, cmd, timeout=TIMEOUT):
    print(f"START {tag} PID={os.getpid()}", flush=True)
    t0=time.time()
    try:
        proc=subprocess.run(cmd, cwd=str(REPO), capture_output=True, text=True, timeout=timeout, env=ENV)
    except subprocess.TimeoutExpired:
        dur=time.time()-t0
        (EVID/f"{tag}-timeout.txt").write_text(f"timeout after {dur:.1f}s\n", encoding="utf-8")
        (EVID/f"{tag}-exit.txt").write_text("TIMEOUT", encoding="utf-8")
        raise
    dur=time.time()-t0
    (EVID/f"{tag}-stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (EVID/f"{tag}-stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    (EVID/f"{tag}-exit.txt").write_text(str(proc.returncode), encoding="utf-8")
    (EVID/f"{tag}-dur.txt").write_text(f"{dur:.2f}\n", encoding="utf-8")
    (EVID/f"{tag}-pid.txt").write_text(f"pid={os.getpid()} wall={datetime.now(timezone.utc).isoformat()}\n", encoding="utf-8")
    with open(EVID/"commands.log","a",encoding="utf-8") as fh:
        fh.write(f"$ {' '.join(cmd[:6])}... tag={tag} -> exit={proc.returncode} dur={dur:.2f}s\n")
    print(f"DONE {tag} exit={proc.returncode} dur={dur:.2f}s", flush=True)
    return proc
with open(EVID/"commands.log","a",encoding="utf-8") as fh:
    fh.write(f"PHASE5 start {datetime.now(timezone.utc).isoformat()} PID={os.getpid()}\n")
run_tag("wall-before",["date","-u","+%Y-%m-%dT%H:%M:%SZ"])
p=run_tag("state-final",[sys.executable,"-c","import json,hashlib,pathlib; r=pathlib.Path('"+str(FIX)+"'); s=r/'"+STATE_REL+"'; d=json.load(open(s)); print(json.dumps({'sha':hashlib.sha256(s.read_bytes()).hexdigest(),'lifecycle':d['lifecycle_state'],'terminal':d['terminal_reason'],'next':d['next_action'],'machine':d['machine_checkpoints'],'human':d['human_gates'],'active':d['publication_revalidation_provenance'],'history_tail':d['history'][-3:]},indent=1))"])
assert p.returncode==0 and "RELEASED" in p.stdout
time.sleep(1)
now5=datetime.now(timezone.utc).isoformat()
(EVID/"now-iso-phase5.txt").write_text(now5+"\n", encoding="utf-8")
print(f"PHASE5 now {now5}", flush=True)
# final readback fresh child: API + current proof/Candidate/history/release + write window + PDF
CODE = r"""
import sys, json, hashlib, subprocess
sys.path.insert(0, sys.argv[1])
root, state_rel, now_iso = sys.argv[1:4]
from pathlib import Path
from datetime import datetime
import os
print(f"FINAL child PID={os.getpid()}", flush=True)
root_p = Path(root)
from scripts import survey_production_v2 as core
from scripts import survey_agent_control_v2 as agent
from scripts import survey_publication_v2 as pubmod
from scripts import survey_publication_set_v2 as setmod
from scripts import survey_versioned_renewal_history_v2 as hist
from scripts import survey_versioned_renewal_source_v2 as srcmod
assert str(Path(core.__file__).resolve()).startswith(str(root_p.resolve())), "fixture origin"
cfg = json.loads((root_p / "config/survey-production-v2.json").read_bytes())
state_path = root_p / state_rel
state = json.loads(state_path.read_bytes())
print(f"lifecycle={state['lifecycle_state']} terminal={state['terminal_reason']} next={state['next_action']}", flush=True)
assert state["lifecycle_state"]=="RELEASED"
assert state["terminal_reason"]=="COMPLETE"
# public validate-state API exit0
errs = agent.validate_agent_state(root_p, cfg, state)
print(f"validate_agent_state={errs}", flush=True)
assert errs==[]
# current proof/Candidate/history/release-readback
# 1. active pointer role-aware Candidate resolves original C targets reused U4
cand_path = Path(setmod.resolve_publication_artifact_path(root_p, cfg, state, "publication-candidate"))
print(f"active candidate={cand_path.relative_to(root_p)}", flush=True)
cand = pubmod.validate_candidate(root_p, cand_path, issue_id=state["issue_id"])
print(f"candidate pdf={cand['pdf']['path']} sha={cand['pdf']['sha256'][:12]} manuscript={cand['reader_manuscript']['path']}", flush=True)
# old producer proof history correctly: r7 still active, chain 6
rec = state["publication_revalidation_provenance"]["path"]
v = hist.verify_versioned_history(str(root_p), rec)
print(f"history chain={v['chain_length']} active={rec}", flush=True)
assert v["chain_length"]==6
assert rec.endswith("r7.json")
# current proof: U4 basis/proof CURRENT at HEAD 047f8ad (SOURCE epochs retained)
basis_rel = "sources/SP001/publication/v2/editorial-corrections/lf-boot-1/renewals/high-u4-longform/renewal-basis.json"
proof_rel = "sources/SP001/publication/v2/editorial-corrections/lf-boot-1/renewals/high-u4-longform/renewal-source-proof.json"
srcmod.verify_renewal_source_proof(str(root_p), basis_rel, proof_rel)
print("CURRENT proof SOURCE_READBACK_OK", flush=True)
# Candidate/history/release-readback: release manifest/record, preview approval, freeze, visual
manifest = pubmod.validate_release_manifest(root_p, root_p / "sources/SP001/publication/v2/release-manifest-v2.json")
print(f"manifest pdf={manifest['pdf_sha256'][:12]} identity={manifest['release_identity']}", flush=True)
release = pubmod.validate_release_record(root_p, root_p / "sources/SP001/publication/v2/release-record-v2.json")
print(f"release status={release['status']} ref={release['release_reference']}", flush=True)
assert release["status"]=="RELEASED"
appr = pubmod.validate_preview_approval(root_p, root_p / state["human_gate_provenance"]["publication_preview"]["path"], issue_id=state["issue_id"])
print(f"preview approval pdf={appr['pdf_sha256'][:12]} candidate={appr['publication_candidate_path']}", flush=True)
assert appr["pdf_sha256"]==cand["pdf"]["sha256"]
# exact write window: history recorded_at monotonic and >= r7, impl 047f8ad, orphan r5 unchanged
hist_list = state["history"]
# last three must be our lifecycle
assert hist_list[-3]["from"]=="VALIDATED_DRAFT" and hist_list[-3]["to"]=="RELEASE_CANDIDATE"
assert hist_list[-2]["from"]=="RELEASE_CANDIDATE" and hist_list[-2]["to"]=="FROZEN"
assert hist_list[-1]["from"]=="FROZEN" and hist_list[-1]["to"]=="RELEASED"
for row in hist_list[-3:]:
    assert row["repository_commit_sha"]=="047f8adc0b7a7c005e03a8e2d374c1e5b6712b60", row
    assert row["recorded_at"] >= "2026-10-25T08:41:57", row
    print(f"window {row['from']}->{row['to']} at {row['recorded_at']} impl {row['repository_commit_sha'][:8]}", flush=True)
# orphan r5 chronology keep unchanged ignore selection: r5 still 05:33:56, not altered
r5 = json.loads((root_p / "sources/SP001/publication/v2/publication-surface-revalidation-r5.json").read_bytes())
print(f"orphan r5 recorded_at={r5['recorded_at']}", flush=True)
assert r5["recorded_at"]=="2026-10-25T05:33:56.641796Z"
# PDF pages: U4 reused C PDF 5 pages, SHA matches freeze/manifest/approval
from pypdf import PdfReader
pdf_path = root_p / cand["pdf"]["path"]
pages = len(PdfReader(str(pdf_path)).pages)
print(f"pdf pages={pages} sha={hashlib.sha256(pdf_path.read_bytes()).hexdigest()[:12]}", flush=True)
assert pages==5
assert hashlib.sha256(pdf_path.read_bytes()).hexdigest()==cand["pdf"]["sha256"]==manifest["pdf_sha256"]==release["pdf_sha256"]==appr["pdf_sha256"]
# synthetic timestamps vs actual wallclock distinct: our now_iso synthetic vs wallclock
import datetime as _dt
wall = _dt.datetime.now(_dt.timezone.utc).isoformat()
print(f"synthetic now_iso={now_iso} wallclock={wall} distinct={now_iso!=wall}", flush=True)
assert now_iso!=wall
print("FINAL_READBACK_OK", flush=True)
"""
p=run_tag("final-readback",[sys.executable,"-c",CODE, str(FIX), STATE_REL, now5])
print(open(EVID/"final-readback-stdout.txt").read()[:8000] if (EVID/"final-readback-stdout.txt").exists() else "no stdout", flush=True)
print(open(EVID/"final-readback-stderr.txt").read()[:8000] if (EVID/"final-readback-stderr.txt").exists() else "no stderr", flush=True)
if p.returncode!=0:
    print("FATAL FINAL blocked exact source function/public input ref above", flush=True)
    sys.exit(1)
# CLI validate-state exit0
p=run_tag("cli-validate-state",[sys.executable,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_agent_control_v2 import main; import sys as _s; _s.argv=['survey_agent_control_v2.py','--repo-root',sys.argv[1],'--state',sys.argv[2],'validate-state','--state',sys.argv[2]]; raise SystemExit(main())", str(FIX), STATE_REL])
# Actually use CLI via module main with correct args: --repo-root FIX --state STATE validate-state --state STATE
# Simpler: call via subprocess with proper CLI
p=run_tag("cli-validate-state2",[sys.executable, str(FIX/"scripts/survey_agent_control_v2.py"), "--repo-root", str(FIX), "--state", STATE_REL, "validate-state", "--state", STATE_REL])
print(open(EVID/"cli-validate-state2-stdout.txt").read()[:3000] if (EVID/"cli-validate-state2-stdout.txt").exists() else "no", flush=True)
print(open(EVID/"cli-validate-state2-stderr.txt").read()[:3000] if (EVID/"cli-validate-state2-stderr.txt").exists() else "no", flush=True)
if p.returncode!=0:
    print("FATAL CLI validate-state blocked", flush=True)
    sys.exit(1)
# persist before/after hashes etc. + HEAD/tree/ancestor import/source guard
run_tag("head-final",["git","-C",str(FIX),"rev-parse","HEAD"])
run_tag("tree-final",["git","-C",str(FIX),"rev-parse","HEAD^{tree}"])
run_tag("ancestor-final",["git","-C",str(FIX),"merge-base","--is-ancestor","721a04d85532d7855f3e54cc411f5847c787726e","HEAD"])
run_tag("import-guard",[sys.executable,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts import survey_production_v2 as core; print(core.__file__); assert '"+str(FIX)+"' in core.__file__; print('IMPORT_GUARD_OK')", str(FIX)])
run_tag("wall-after",["date","-u","+%Y-%m-%dT%H:%M:%SZ"])
print("PHASE5 DONE", flush=True)
