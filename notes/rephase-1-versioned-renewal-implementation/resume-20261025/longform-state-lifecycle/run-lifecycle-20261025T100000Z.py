#!/usr/bin/env python3
"""LONGFORM actualState lifecycle ONLY — parallel Weekly/editorial author.
No product candidate/INPUT/code edits. Input READONLY pinned preview U4 r7 pending.
Makes NEW byte-independent GitDB copy + exact E, then normal public lifecycle to RELEASED.
"""
import os, sys, json, subprocess, hashlib, time, shutil
from datetime import datetime, timezone
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
SRC = REPO / ".rephase-1-editorial-runtime/versioned-renewal-longform-repair-20261025T090000Z/renewal-longform-prepreview"
PARENT = REPO / ".rephase-1-editorial-runtime/versioned-renewal-longform-lifecycle-20261025T100000Z"
FIX = PARENT / "renewal-longform-lifecycle"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-state-lifecycle"
STAMP_SETUP = "setup-20261025T100000Z"
EVID_SETUP = EVID / STAMP_SETUP
EVID_SETUP.mkdir(parents=True, exist_ok=True)
TMP = PARENT / "tmp"
# ensure EVID exists already; PARENT new
import pathlib as _pl
LOG_SETUP = EVID_SETUP / "commands.log"
def _log_setup(msg):
    with open(LOG_SETUP, "a", encoding="utf-8") as fh:
        fh.write(msg + "\n")
if LOG_SETUP.exists():
    LOG_SETUP.unlink()
_log_setup(f"LONGFORM lifecycle setup start {datetime.now(timezone.utc).isoformat()} PID={os.getpid()}")
for k in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
    assert not os.environ.get(k), f"inherited {k}"
ENV=dict(os.environ); ENV["PYTHONDONTWRITEBYTECODE"]="1"; ENV["LC_ALL"]="C"
TIMEOUT=1200
def run_tag(eviddir, tag, cmd, timeout=TIMEOUT, cwd=None, env=None):
    if env is None:
        env=ENV
    if cwd is None:
        cwd=str(REPO)
    print(f"START {tag} PID={os.getpid()}", flush=True)
    t0=time.time()
    try:
        proc=subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, env=env)
    except subprocess.TimeoutExpired as e:
        dur=time.time()-t0
        (eviddir/f"{tag}-timeout.txt").write_text(f"timeout after {dur:.1f}s\n", encoding="utf-8")
        (eviddir/f"{tag}-exit.txt").write_text("TIMEOUT", encoding="utf-8")
        with open(eviddir/"commands.log","a",encoding="utf-8") as fh:
            fh.write(f"$ {' '.join(cmd[:6])}... tag={tag} TIMEOUT dur={dur:.1f}s\n")
        print(f"TIMEOUT {tag} after {dur:.1f}s", flush=True)
        raise
    dur=time.time()-t0
    (eviddir/f"{tag}-stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (eviddir/f"{tag}-stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    (eviddir/f"{tag}-exit.txt").write_text(str(proc.returncode), encoding="utf-8")
    (eviddir/f"{tag}-dur.txt").write_text(f"{dur:.2f}\n", encoding="utf-8")
    (eviddir/f"{tag}-pid.txt").write_text(f"pid={os.getpid()} wall={datetime.now(timezone.utc).isoformat()}\n", encoding="utf-8")
    with open(eviddir/"commands.log","a",encoding="utf-8") as fh:
        fh.write(f"$ {' '.join(cmd[:8])}... tag={tag} -> exit={proc.returncode} dur={dur:.2f}s\n")
    print(f"DONE {tag} exit={proc.returncode} dur={dur:.2f}s", flush=True)
    return proc
# setup env
ENV_SETUP=dict(ENV)
# TMPDIR workspace-local (create parent first)
PARENT.mkdir(parents=True, exist_ok=False)
TMP.mkdir(parents=True, exist_ok=True)
ENV_SETUP["TMPDIR"]=str(TMP); ENV_SETUP["TMP"]=str(TMP); ENV_SETUP["TEMP"]=str(TMP)
with open(EVID_SETUP/"commands.log","a",encoding="utf-8") as fh:
    fh.write(f"TMPDIR={TMP}\n")
def main_setup():
    # verify SRC
    p=run_tag(EVID_SETUP,"src-head",["git","-C",str(SRC),"rev-parse","HEAD"],cwd=str(REPO),env=ENV_SETUP)
    assert p.returncode==0 and p.stdout.strip()=="047f8adc0b7a7c005e03a8e2d374c1e5b6712b60", p.stdout
    p=run_tag(EVID_SETUP,"src-tree",["git","-C",str(SRC),"rev-parse","HEAD^{tree}"],cwd=str(REPO),env=ENV_SETUP)
    assert p.returncode==0
    p=run_tag(EVID_SETUP,"src-log",["git","-C",str(SRC),"log","--oneline","-8"],cwd=str(REPO),env=ENV_SETUP)
    assert p.returncode==0
    p=run_tag(EVID_SETUP,"src-status",["git","-C",str(SRC),"status","--porcelain=v1","--untracked-files=all"],cwd=str(REPO),env=ENV_SETUP)
    assert p.returncode==0
    p=run_tag(EVID_SETUP,"src-ancestor",["git","-C",str(SRC),"merge-base","--is-ancestor","721a04d85532d7855f3e54cc411f5847c787726e","HEAD"],cwd=str(REPO),env=ENV_SETUP)
    assert p.returncode==0, "ancestor 721 must be ancestor"
    p=run_tag(EVID_SETUP,"src-state",[sys.executable,"-c","import json,pathlib,hashlib; s=pathlib.Path('"+str(SRC)+"')/'sources/SP001/production-state.json'; d=json.load(open(s)); print(json.dumps({'lifecycle':d['lifecycle_state'],'pointer':d['publication_revalidation_provenance'],'gates':d['human_gates'],'machine':d['machine_checkpoints']},indent=1)); print('sha:'+hashlib.sha256(s.read_bytes()).hexdigest())"],cwd=str(REPO),env=ENV_SETUP)
    assert p.returncode==0 and "VALIDATED_DRAFT" in p.stdout and "r7.json" in p.stdout
    p=run_tag(EVID_SETUP,"src-pins",[sys.executable,"-c","import hashlib,pathlib; r=pathlib.Path('"+str(SRC)+"'); print('H '+hashlib.sha256((r/'scripts/survey_versioned_renewal_history_v2.py').read_bytes()).hexdigest()); print('P1 '+hashlib.sha256((r/'scripts/survey_editorial_correction_proposal_v2.py').read_bytes()).hexdigest()); print('PUB '+hashlib.sha256((r/'scripts/survey_publication_v2.py').read_bytes()).hexdigest()); print('S '+hashlib.sha256((r/'scripts/survey_versioned_renewal_source_v2.py').read_bytes()).hexdigest()); print('HIGH '+hashlib.sha256((r/'scripts/survey_versioned_renewal_v2.py').read_bytes()).hexdigest()); print('Reader '+hashlib.sha256((r/'scripts/survey_reader_publication_v2.py').read_bytes()).hexdigest()); print('style '+hashlib.sha256((r/'templates/survey/jgaisurvey.sty').read_bytes()).hexdigest())"],cwd=str(REPO),env=ENV_SETUP)
    assert p.returncode==0
    assert "6fe86e78a12e2159d6ff50dfd7f70fda7b2e0d34d48db26402743edda2eca5ad" in p.stdout
    assert "825dba1dedaed0850134b3a54a249a427b2e77709861818e8eb7cb63e1a33a2b" in p.stdout
    assert "3f4039fd7699baa212020dddfb02b3918bd63e02c475d638d99cbb2a1150d8d6" in p.stdout
    assert "b1cbbdd93711aef17b37d3bbbedda25aa0bcb51f462bdc7ad172ce2aa103c8f4" in p.stdout
    # clone NEW byte-independent
    p=run_tag(EVID_SETUP,"clone-0",["git","clone","--no-hardlinks",str(SRC),str(FIX)],cwd=str(REPO),env=ENV_SETUP)
    assert p.returncode==0, p.stderr
    p=run_tag(EVID_SETUP,"remote-set",["git","-C",str(FIX),"remote","set-url","origin","https://example.invalid/versioned-renewal-longform-lifecycle.git"],cwd=str(REPO),env=ENV_SETUP)
    assert p.returncode==0
    p=run_tag(EVID_SETUP,"remote-show",["git","-C",str(FIX),"remote","-v"],cwd=str(REPO),env=ENV_SETUP)
    assert p.returncode==0 and "example.invalid/versioned-renewal-longform-lifecycle.git" in p.stdout
    p=run_tag(EVID_SETUP,"cfg-name",["git","-C",str(FIX),"config","user.name","rephase-fixture-longform-lifecycle"],cwd=str(REPO),env=ENV_SETUP)
    assert p.returncode==0
    p=run_tag(EVID_SETUP,"cfg-email",["git","-C",str(FIX),"config","user.email","fixture-longform-lifecycle@example.invalid"],cwd=str(REPO),env=ENV_SETUP)
    assert p.returncode==0
    p=run_tag(EVID_SETUP,"cfg-gpgsign",["git","-C",str(FIX),"config","commit.gpgsign","false"],cwd=str(REPO),env=ENV_SETUP)
    assert p.returncode==0
    p=run_tag(EVID_SETUP,"fixture-head",["git","-C",str(FIX),"rev-parse","HEAD"],cwd=str(REPO),env=ENV_SETUP)
    assert p.returncode==0 and p.stdout.strip()=="047f8adc0b7a7c005e03a8e2d374c1e5b6712b60"
    p=run_tag(EVID_SETUP,"fixture-tree",["git","-C",str(FIX),"rev-parse","HEAD^{tree}"],cwd=str(REPO),env=ENV_SETUP)
    assert p.returncode==0
    p=run_tag(EVID_SETUP,"fixture-gitdir",["git","-C",str(FIX),"rev-parse","--absolute-git-dir"],cwd=str(REPO),env=ENV_SETUP)
    assert p.returncode==0
    p=run_tag(EVID_SETUP,"noalternates",["bash","-c",f"test ! -e \"{FIX}/.git/objects/info/alternates\" && echo NO_ALTERNATES || (echo HAS_ALTERNATES; exit 1)"],cwd=str(REPO),env=ENV_SETUP)
    assert p.returncode==0 and "NO_ALTERNATES" in p.stdout
    p=run_tag(EVID_SETUP,"config-show",["git","-C",str(FIX),"config","--list","--show-origin"],cwd=str(REPO),env=ENV_SETUP)
    assert p.returncode==0
    p=run_tag(EVID_SETUP,"isolation-inode",[sys.executable,"-c","import os,pathlib,subprocess; src=pathlib.Path('"+str(SRC)+"'); dst=pathlib.Path('"+str(FIX)+"'); print('src git inode '+str(os.stat(src/'.git').st_ino)); print('dst git inode '+str(os.stat(dst/'.git').st_ino)); assert os.stat(src/'.git').st_ino!=os.stat(dst/'.git').st_ino; import subprocess as sp; r=sp.run(['stat','-c','%h %i',str(dst/'.git/objects')],capture_output=True,text=True); print(r.stdout); print('nlink/inode disjoint OK')"],cwd=str(REPO),env=ENV_SETUP)
    assert p.returncode==0
    # copy exact E including ignored PDF/log/untracked typed graph files captured manifest
    p=run_tag(EVID_SETUP,"copy-E",[sys.executable,"-c","import sys,hashlib,shutil,subprocess,pathlib,json; src=pathlib.Path(sys.argv[1]); dst=pathlib.Path(sys.argv[2]); evid=pathlib.Path(sys.argv[3]);\n"
        "def ls(args):\n"
        " import subprocess as sp; r=sp.run(['git','-C',str(src)]+args,capture_output=True,text=True); assert r.returncode==0, r.stderr; return [l for l in r.stdout.splitlines() if l.strip()]\n"
        "others=ls(['ls-files','--others','--exclude-standard']); ignored=ls(['ls-files','--others','--ignored','--exclude-standard']); all_e=others+ignored\n"
        "print(f'others={len(others)} ignored={len(ignored)} total={len(all_e)}');\n"
        "manifest=[]; copied=0;\n"
        "import hashlib\n"
        "for rel in all_e:\n"
        " s=src/rel; d=dst/rel;\n"
        " assert s.exists(), f'missing SRC {rel}';\n"
        " if d.exists(): raise SystemExit(f'E target exists {rel}');\n"
        " d.parent.mkdir(parents=True,exist_ok=True);\n"
        " import shutil; \n"
        " shutil.copy2(str(s),str(d));\n"
        " hs=hashlib.sha256(s.read_bytes()).hexdigest() if s.is_file() and not s.is_symlink() else 'DIR';\n"
        " hd=hashlib.sha256(d.read_bytes()).hexdigest() if d.is_file() and not d.is_symlink() else 'DIR';\n"
        " assert hs==hd, f'SHA mismatch {rel}';\n"
        " manifest.append({'path':rel,'sha256':hs,'bytes':d.stat().st_size if d.is_file() else 0}); copied+=1;\n"
        "(evid/'e-manifest.json').write_text(json.dumps({'others':len(others),'ignored':len(ignored),'total':len(all_e),'files':manifest},indent=1));\n"
        "print(f'COPY_E_DONE copied={copied}');\n"
        "import json; st=json.load(open(dst/'sources/SP001/production-state.json')); assert st['publication_revalidation_provenance']['path'].endswith('r7.json'); assert st['human_gates']['publication_preview']=='pending'; print('E_PENDING_R7_OK')\n",str(SRC),str(FIX),str(EVID_SETUP)],cwd=str(REPO),env=ENV_SETUP)
    assert p.returncode==0, open(EVID_SETUP/"copy-E-stderr.txt").read()[:8000]
    # verify State SHA same, proof valid via agent API fresh child
    p=run_tag(EVID_SETUP,"verify-E",[sys.executable,"-c","import sys,json,hashlib,pathlib; sys.path.insert(0,sys.argv[1]); src=pathlib.Path(sys.argv[1]); dst=pathlib.Path(sys.argv[2]);\n"
        "from scripts import survey_production_v2 as core; from scripts import survey_agent_control_v2 as agent;\n"
        "import pathlib as pl; root=pl.Path(sys.argv[2]).resolve(); cfg=json.load(open(root/'config/survey-production-v2.json')); st=json.load(open(root/'sources/SP001/production-state.json'));\n"
        "errs=agent.validate_agent_state(root,cfg,st); print(f'validate_agent_state={errs}'); assert errs==[];\n"
        "print(f\"core {core.__file__}\"); assert str(pl.Path(core.__file__).resolve()).startswith(str(root.resolve())), 'fixture origin';\n"
        "print('SOURCE_GUARD_OK');\n"
        "print('state '+hashlib.sha256((root/'sources/SP001/production-state.json').read_bytes()).hexdigest());\n",str(FIX),str(FIX)],cwd=str(REPO),env=ENV_SETUP)
    assert p.returncode==0, open(EVID_SETUP/"verify-E-stderr.txt").read()[:8000]
    p=run_tag(EVID_SETUP,"status-post",["git","-C",str(FIX),"status","--porcelain=v1","--untracked-files=all"],cwd=str(REPO),env=ENV_SETUP)
    assert p.returncode==0
    # record before State hash/lifecycle etc.
    p=run_tag(EVID_SETUP,"state-before",[sys.executable,"-c","import json,hashlib,pathlib; r=pathlib.Path('"+str(FIX)+"'); s=r/'sources/SP001/production-state.json'; d=json.load(open(s)); print(json.dumps({'sha':hashlib.sha256(s.read_bytes()).hexdigest(),'lifecycle':d['lifecycle_state'],'machine':d['machine_checkpoints'],'human':d['human_gates'],'provenance':d['human_gate_provenance'],'active':d['publication_revalidation_provenance']},indent=1))"],cwd=str(REPO),env=ENV_SETUP)
    assert p.returncode==0
    print("SETUP DONE", flush=True)
    return 0
if __name__=="__main__":
    import sys
    raise SystemExit(main_setup())
