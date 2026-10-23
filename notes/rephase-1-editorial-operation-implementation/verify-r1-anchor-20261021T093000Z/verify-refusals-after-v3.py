#!/usr/bin/env python3
"""Worker C v3: refusals AFTER versioned (State already VERSIONED_ACTIVE r3 despite POSTREPLACE_FAIL).

No source edits. Actual function calls via fixture-code subprocess (no ambient stale),
immediate full inventory comparison, exact refusal messages. Healthy controls reported
truthfully (current State invalid due to reported bug, so healthy post-activation checks
are INCOMPLETE, not PASS). No whole PASS.
"""
from __future__ import annotations
import json, os, shutil, stat as _stat, subprocess, sys, time, traceback
from pathlib import Path
from datetime import datetime, timezone
def _eprint(*a): print(*a, flush=True)
def main() -> int:
    FIX_ROOT = Path(sys.argv[1]).resolve()
    NOTES = Path(sys.argv[2]).resolve()
    NOTES.mkdir(parents=True, exist_ok=True)
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(FIX_ROOT))
    os.environ["PYTHONDONTWRITEBYTECODE"]="1"
    for _v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE","GIT_OBJECT_DIRECTORY","GIT_ALTERNATE_OBJECT_DIRECTORIES","GIT_COMMON_DIR","GIT_PREFIX"):
        if os.environ.get(_v):
            _eprint(f"UNSAFE {_v}"); return 2
    from scripts import survey_production_v2 as core
    def _run_git(*a):
        env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
        env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file","GIT_AUTHOR_NAME":"Synthetic WorkerC","GIT_AUTHOR_EMAIL":"w@example.invalid","GIT_COMMITTER_NAME":"Synthetic WorkerC","GIT_COMMITTER_EMAIL":"w@example.invalid"})
        return subprocess.run(["git",*a],cwd=FIX_ROOT,capture_output=True,text=True,env=env)
    # purge pycache
    try:
        for _p in FIX_ROOT.rglob("__pycache__"):
            if ".git" in _p.parts: continue
            shutil.rmtree(_p, ignore_errors=True)
        for _f in FIX_ROOT.rglob("*.pyc"):
            if ".git" in _f.parts: continue
            try: _f.unlink()
            except: pass
    except: pass
    head=_run_git("rev-parse","HEAD").stdout.strip()
    _eprint(f"FIX_HEAD={head}")
    assert head=="744b121cc0e561a6581e1ca6c9d01345b07fed42", head
    state_path=FIX_ROOT/"sources/2026-W37/production-state.json"
    state=core.load_json(state_path)
    _eprint(f"STATE_POINTER={state.get('publication_revalidation_provenance')}")
    assert state.get("publication_revalidation_provenance",{}).get("path")=="sources/2026-W37/publication/v2/publication-surface-revalidation-r3.json", "must be VERSIONED_ACTIVE r3"
    from scripts import survey_publication_set_v2 as setmod
    cfg=core.load_json(FIX_ROOT/core.DEFAULT_CONFIG)
    sel=setmod.resolve_publication_selection(FIX_ROOT,cfg,state)
    _eprint(f"SELECTION_MODE={sel.get('mode')}")
    assert sel.get("mode")=="VERSIONED_ACTIVE", sel
    # full snapshot
    def _snapshot(root: Path):
        files={}; special={}
        for p in sorted(root.rglob("*")):
            if ".git" in p.parts: continue
            try: rel=str(p.relative_to(root))
            except: continue
            try: st=p.lstat()
            except Exception as e: special[rel]=f"LSTAT:{e}"; continue
            if _stat.S_ISDIR(st.st_mode): special[rel]="DIR"; continue
            if not _stat.S_ISREG(st.st_mode): special[rel]="SPECIAL:"+oct(_stat.S_IMODE(st.st_mode)); continue
            try: files[rel]=core.sha256_file(p)
            except: special[rel]="UNREADABLE"
        return {"files":files,"special":special,"head":_run_git("rev-parse","HEAD").stdout.strip(),"status":_run_git("status","--porcelain").stdout}
    def _assert_no_write(b,a,label):
        assert a["files"]==b["files"], f"tree write {label}"
        assert a.get("special")==b.get("special"), f"special {label}"
        assert a["head"]==b["head"], f"HEAD {label}"
        assert a["status"]==b["status"], f"status {label}"
    def _run_fixture(script,args,timeout_s=600):
        env={k:v for k,v in os.environ.items() if not k.startswith("GIT_") and k!="PYTHONPATH"}
        env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file","PYTHONDONTWRITEBYTECODE":"1"})
        proc=subprocess.run([sys.executable,"-c",script,*args],cwd=FIX_ROOT,capture_output=True,text=True,timeout=timeout_s,env=env)
        return proc.returncode,proc.stdout,proc.stderr
    # R1 must refuse
    snap_before=_snapshot(FIX_ROOT)
    r1_script=("import sys\nfrom pathlib import Path\nroot=Path(sys.argv[1])\nstate_path=Path(sys.argv[2])\n"
               "from scripts import survey_production_v2 as core\nfrom scripts import survey_weekly_mechanical_refresh_v2 as r1\nfrom datetime import datetime,timezone\n"
               "recorded=datetime(2026,9,19,9,0,0,tzinfo=timezone.utc)\ntry:\n"
               "  r1.refresh_mechanical_evidence(root,core.load_json(root / core.DEFAULT_CONFIG),state_path,'post-versioned R1 must refuse','workerc',recorded)\n"
               "  print('UNEXPECTED_SUCCESS'); sys.exit(10)\n"
               "except Exception as e:\n  print(f'REFUSED:{type(e).__name__}:{e}'); sys.exit(3)\n")
    rc,out,err=_run_fixture(r1_script,[str(FIX_ROOT),str(state_path)])
    _eprint(f"R1_AFTER rc={rc} out={out[:2000]}")
    assert rc==3, f"R1 must exit 3 {rc} {out} {err[-2000:]}"
    assert "R1 mechanical refresh refused in VERSIONED_ACTIVE" in out, f"wrong R1 msg {out}"
    _assert_no_write(snap_before,_snapshot(FIX_ROOT),"R1 after no-write")
    _eprint("R1_AFTER_REFUSE_NOWRITE_OK")
    (NOTES/"refusal-r1-after.txt").write_text(f"rc={rc}\n{out}\n{err[-2000:]}")
    # Canonical must refuse
    snap2=_snapshot(FIX_ROOT)
    canon_script=("import sys\nfrom pathlib import Path\nroot=Path(sys.argv[1])\nstate_path=Path(sys.argv[2])\n"
                  "from scripts import survey_production_v2 as core\nfrom scripts import survey_agent_control_v2 as agent\nfrom datetime import datetime,timezone\n"
                  "cfg=core.load_json(root / core.DEFAULT_CONFIG)\nrecorded=datetime(2026,9,19,9,5,0,tzinfo=timezone.utc)\ntry:\n"
                  "  agent.revalidate_publication_surface(root,cfg,state_path,'REVIEWED_CORE_CHANGE','post-versioned canonical must refuse','workerc',recorded,None)\n"
                  "  print('UNEXPECTED_SUCCESS'); sys.exit(10)\n"
                  "except Exception as e:\n  print(f'REFUSED:{type(e).__name__}:{e}'); sys.exit(3)\n")
    rc2,out2,err2=_run_fixture(canon_script,[str(FIX_ROOT),str(state_path)])
    _eprint(f"CANON_AFTER rc={rc2} out={out2[:2000]}")
    assert rc2==3
    assert "canonical revalidation refused in revised mode" in out2.lower(), out2
    _assert_no_write(snap2,_snapshot(FIX_ROOT),"canon after no-write")
    _eprint("CANON_AFTER_REFUSE_NOWRITE_OK")
    (NOTES/"refusal-canon-after.txt").write_text(f"rc={rc2}\n{out2}\n{err2[-2000:]}")
    # Fake editorial
    snap3=_snapshot(FIX_ROOT)
    fake_script=("import sys\nfrom pathlib import Path\nroot=Path(sys.argv[1])\nstate_path=Path(sys.argv[2])\n"
                 "from scripts import survey_production_v2 as core\nfrom scripts import survey_agent_control_v2 as agent\nfrom datetime import datetime,timezone\n"
                 "cfg=core.load_json(root / core.DEFAULT_CONFIG)\nrecorded=datetime(2026,9,19,9,6,0,tzinfo=timezone.utc)\ntry:\n"
                 "  agent.revalidate_publication_surface(root,cfg,state_path,'REVIEWED_EDITORIAL_CORRECTION','fake','workerc',recorded,None)\n"
                 "  print('UNEXPECTED_SUCCESS'); sys.exit(10)\n"
                 "except Exception as e:\n  print(f'REFUSED:{type(e).__name__}:{e}'); sys.exit(3)\n")
    rc3,out3,err3=_run_fixture(fake_script,[str(FIX_ROOT),str(state_path)])
    _eprint(f"FAKE rc={rc3} out={out3[:2000]}")
    assert rc3==3
    assert "REVIEWED_EDITORIAL_CORRECTION" in out3 and "must use new versioned activation" in out3, out3
    _assert_no_write(snap3,_snapshot(FIX_ROOT),"fake no-write")
    _eprint("FAKE_REFUSE_NOWRITE_OK")
    (NOTES/"refusal-fake-after.txt").write_text(f"rc={rc3}\n{out3}\n{err3[-2000:]}")
    # Healthy controls truthfully INCOMPLETE due to bug
    from scripts import survey_agent_control_v2 as agent
    errs=agent.validate_agent_state(FIX_ROOT,cfg,state)
    _eprint(f"POST_STATE_VALIDATE_ERRORS={errs}")
    (NOTES/"post-state-validate.txt").write_text(json.dumps(errs,indent=2))
    # Receipt/Gate/Candidate checks will also fail due to same State invalid? Try but save as incomplete
    try:
        from scripts import survey_editorial_publication_v2 as edpub
        from scripts import survey_reader_surface_gate_v2 as rg
        from scripts import survey_publication_v2 as pubmod
        pubdir=FIX_ROOT/"sources/2026-W37/publication/v2/editorial-corrections/fixture-wk-corr-verify/publication"
        rv=edpub.validate_editorial_receipt(FIX_ROOT, str(pubdir/"validated-source-manifest.json".replace(".json",".json")) if False else str((pubdir/"validated-source-manifest.json").relative_to(FIX_ROOT)), str(state_path.relative_to(FIX_ROOT)))
        _eprint(f"RECEIPT_CHECK={rv.get('issue_id') if isinstance(rv,dict) else rv}")
    except Exception as e:
        _eprint(f"RECEIPT_INCOMPLETE {e}")
        (NOTES/"receipt-incomplete.txt").write_text(f"{e}\n{traceback.format_exc()}")
    _eprint("REFUSALS_AFTER_DONE no whole PASS")
    (NOTES/"refusals-v3-summary.json").write_text(json.dumps({"fix_head":head,"selection_mode":sel.get("mode"),"r1_refused":rc==3,"canon_refused":rc2==3,"fake_refused":rc3==3,"post_state_errors":errs},indent=2))
    return 0
if __name__=="__main__":
    try: sys.exit(main())
    except Exception: traceback.print_exc(); sys.exit(2)
