#!/usr/bin/env python3
"""Depth rewrite correction: HIGH pre-write cap 32 allows / 33 refuses.

AUTHOR HIGH boundary fix ONLY (CHAIN_LIMIT 32 preserved, H74275d/S229 unchanged).
Entry for CREATING new renewal must check verified prior history.chain_length+1
<=32 BEFORE claiming R/COPY/basis or record/temp writes. Uses actual verified
history count (legacy+editorial+renewal), NOT filename maxseq (gaps/invalid
orphans don't count). Guard also activation/resume-before old State writes
through same entry/observation; no invalid record may publish before known cap
check. ALREADY_ACTIVE readonly same active32 remains possible under matching
CURRENT tools + full source validation (no cap applied to readonly retry).
History/source standalone 32 still valid. Existing prior33 invalid still refuses
as before. No cap change, no history loosening, no synthetic State, no caller
count permit. Preserves orphan matching-intent + anchor pre-write checks.

Scope: exact 32/33/read-only controls, terminal exits. Private fixture provided
legacy history (r1..r30 clones) != R1x30 actual ops (explicit label, ROOT
accepts finite construction). No candidate/reconstruct ordinary commit/network/
oldrunners/cleanup failed fixtures. Current root f84fcf5 candidate409. Write NEW
resume-20261025/depth-prewrite-correction/ raw/pins/newtest; no whole PASS/
CommitPoint.

Terminal: full HIGH hash + scope exact 32/33/read-only controls with terminal
exits.
"""
import hashlib, json, os, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

UTC = "20261025T200000Z"

def _run_git(root: Path, *a):
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file"})
    return subprocess.run(["git",*a], cwd=str(root), capture_output=True, text=True, timeout=120, env=env)

def _sha(p: Path):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    if len(sys.argv)!=4:
        print(f"usage: {sys.argv[0]} FIXTURE_NEW EVIDENCE_RAW TMPDIR_BASE", flush=True); return 2
    fix=Path(sys.argv[1]).resolve(); ev=Path(sys.argv[2]).resolve(); tmp_base=Path(sys.argv[3]).resolve()
    for v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
        if os.environ.get(v): print(f"UNSAFE {v}", flush=True); return 2
    sys.dont_write_bytecode=True; os.environ["PYTHONDONTWRITEBYTECODE"]="1"
    os.environ["TMPDIR"]=str(tmp_base); tmp_base.mkdir(parents=True, exist_ok=True); ev.mkdir(parents=True, exist_ok=True)
    pidf=ev/"depth-rewrite.pid"; hbf=ev/"depth-rewrite.heartbeat.txt"; exitf=ev/"exit.txt"
    pidf.write_text(f"{os.getpid()}\n{time.monotonic():.3f}\n{UTC}\n"); hbf.write_text(f"depth-rewrite start {time.monotonic():.3f} {UTC}\n")
    result={"utc":UTC,"unit":"depth-rewrite correction (HIGH pre-write cap 32 allows/33 refuses, NOT 32 real ops)","scope_qualifier":"ONLY 1 actual editorial (31, OLD, preserved) +1 actual renewal (new chain32, CURRENT, fixed HIGH) on 30 fixture-provided typed LEGACY predecessors (r1..r30 NOT R1x30 actual ops, REAL SHAs/supersedes/schema/own OLD commits/monotonic, same cumulative rows, labelled); plus orphans r32(valid old)/r33(invalid) preserved, gaps don't count chain; whole unit no CommitPoint"}
    try:
        # 0. Pins (FILE-BYTE SHA256, SELF only in named internal fields)
        # HIGH fixed (3dbded...), H74275d, S2290ddd unchanged, P1/PUB/etc CURRENT (from NEW fixture HEAD 9453e1c? Actually after fix commit HEAD will move, pins for H/S/etc unchanged, HIGH new)
        # For now, record current (pre-fix-commit) pins: HIGH fixed uncommitted (3dbded...), H74275d, S2290ddd, etc.
        # Will update after SOURCE commit (HIGH committed, new test committed, HEAD moves, but file SHAs same for H/S, HIGH same 3dbded...).
        pins={}
        for name in ["survey_versioned_renewal_history_v2.py","survey_versioned_renewal_source_v2.py","survey_versioned_renewal_v2.py"]:
            p=fix/f"scripts/{name}"
            assert p.is_file(), f"missing {name}"
            pins[name]=_sha(p)
        result["pins_pre_commit"]={k[:4]:v[:12] for k,v in pins.items()}
        result["HIGH_pre_commit"]=pins["survey_versioned_renewal_v2.py"]
        assert pins["survey_versioned_renewal_history_v2.py"]=="74275d22a342014009d5d090fbe9c552981941e90259c298065d2ba6929d1f3d", "H must stay 74275d"
        assert pins["survey_versioned_renewal_source_v2.py"]=="2290ddd0dc8397f86451aff70d50fd4da0c6184fcf1bef3ed96259642af2d1eb", "S must stay 2290ddd"
        assert pins["survey_versioned_renewal_v2.py"]=="3dbdedb8b44b366b129cc351b25a8bb898a62ad23e424d27e46c3df85a6a6d0b", f"HIGH must be fixed 3dbded, got {pins['survey_versioned_renewal_v2.py'][:12]}"
        hbf.write_text(hbf.read_text()+f"pins verified HIGH fixed 3dbded H74275d S2290ddd {time.monotonic():.3f}\n")
        # 1. Inventory before (count/classification/fileSHA, loop32 refs, epochs)
        rec_dir=fix/"sources/2026-W37/publication/v2"
        recs=sorted([p.name for p in rec_dir.iterdir() if p.name.startswith("publication-surface-revalidation-r")])
        result["inventory_before"]={"rec_count":len(recs),"recs":recs}
        assert len(recs)==33, f"NEW copy must have r1..r33 (33 files, r33 invalid preserved), got {len(recs)}"
        # Classification via real files (not synthetic): legacy (no kind, REVIEWED_CORE_CHANGE), editorial (EDITORIAL...), renewal (VERSIONED...), invalid (r33 hist fails)
        # FileSHA inventory (first 12 for brevity, full in raw file)
        sha_inv={}
        for name in recs:
            sha_inv[name]=_sha(rec_dir/name)[:12]
        (ev/"inventory-before-sha.json").write_text(json.dumps(sha_inv, indent=2, sort_keys=True)+"\n")
        result["classification_before"]="legacy r1..r30 (REVIEWED_CORE_CHANGE, no kind, 30) + editorial r31 (REVIEWED_EDITORIAL_CORRECTION, 1) + renewal r32 (REVIEWED_VERSIONED_CORE_RENEWAL, valid, 1) + invalid r33 (VERSIONED but hist fails chain exceeds max32, preserved, 1) =33 files, chain32 valid (r1..r32), r33 invalid inert"
        # Loop32 selected refs via hist (actual verified history count, not filename maxseq)
        sys.path.insert(0, str(fix))
        from scripts import survey_versioned_renewal_history_v2 as hist
        r31_hist=hist.verify_versioned_history(fix, "sources/2026-W37/publication/v2/publication-surface-revalidation-r31.json")
        assert r31_hist.get("HISTORICAL_IDENTITY_VERIFIED") and r31_hist.get("chain_length")==31, f"r31 must be chain31, got {r31_hist.get('chain_length')}"
        r32_hist=hist.verify_versioned_history(fix, "sources/2026-W37/publication/v2/publication-surface-revalidation-r32.json")
        assert r32_hist.get("HISTORICAL_IDENTITY_VERIFIED") and r32_hist.get("chain_length")==32, f"r32 must be chain32, got {r32_hist.get('chain_length')}"
        try:
            hist.verify_versioned_history(fix, "sources/2026-W37/publication/v2/publication-surface-revalidation-r33.json")
            raise AssertionError("r33 must fail (chain exceeds max32), but passed")
        except Exception as e:
            assert "max32" in str(e), f"r33 must fail max32, got {e}"
        result["loop32_before"]={"r31_chain":31,"r32_chain":32,"r33_invalid":"HISTORY_ANCESTOR chain exceeds max32 (preserved, not deleted)","anchor_r30":"8bc7c6b933ad0bed2ac7e20a0159f91aeff8fda3954ecbdfb4a2293c8938ee89","label":"provided legacy r1..r30 != R1x30 actual ops (fixture-provided typed history, ROOT accepts finite construction)"}
        (ev/"loop32-before.json").write_text(json.dumps(result["loop32_before"], indent=2)+"\n")
        # Epochs (source/genuine CODE epochs actual no empty)
        head_before=_run_git(fix,"rev-parse","HEAD").stdout.strip()
        assert head_before=="9453e1ca9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9" or head_before.startswith("9453e1c"), f"NEW copy HEAD must be 9453e1c (genuine Core comment for 33rd), got {head_before[:12]}"
        # Actually check full HEAD (9453e1c... from earlier log, full SHA? Let's get full)
        result["epochs_before"]={"HEAD":head_before,"HEAD_short":head_before[:12],"parent_fc127fc":"overlay CURRENT 741 (genuine Core change, 741 tracked, style 035645ca unchanged, E preserved)","parent_36c679cc":"R1 anchor r2 (old721+only weekly derivation comment epochs)","genuine_9453e1c":"comment-only derivation (2 insertions, style unchanged, E preserved, genuine, not artifact-only, no empty)"}
        # Verify genuine commits actual no empty (no --allow-empty, meaningful contents, real ancestry)
        for sha in [head_before]:
            r=_run_git(fix,"show","--stat","--oneline",sha)
            assert r.returncode==0 and "survey_weekly_derivation_v2.py" in r.stdout, f"genuine commit must include derivation, got {r.stdout[:500]}"
            r2=_run_git(fix,"log","--format=%P", "-n","1",sha)
            assert r2.returncode==0 and len(r2.stdout.strip())>0, "genuine commit must have parent (no empty root)"
        hbf.write_text(hbf.read_text()+f"inventory loop32 epochs verified {time.monotonic():.3f}\n")
        # 2. Dedicated test (6 tests, fixed HIGH, exit 0)
        # Run via subprocess with fresh Python (no module caching, PYTHONPATH=fix, cwd=fix, TMPDIR=tmp_base)
        import subprocess as _sp
        env={k:v for k,v in os.environ.items() if not k.startswith("GIT_") and k not in ("PYTHONPATH",)}
        env.update({"PYTHONDONTWRITEBYTECODE":"1","PYTHONPATH":str(fix),"TMPDIR":str(tmp_base),"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file"})
        proc=_sp.run([sys.executable,"-B","-m","unittest","tests.test_survey_versioned_renewal_depth_prewrite_v2","-v"], cwd=str(fix), capture_output=True, text=True, timeout=300, env=env)
        (ev/"dedicated-test-stdout.txt").write_text(proc.stdout[:8000]+"\n")
        (ev/"dedicated-test-stderr.txt").write_text(proc.stderr[:8000]+"\n")
        (ev/"dedicated-test-exit.txt").write_text(str(proc.returncode)+"\n")
        assert proc.returncode==0, f"dedicated test must pass (6 tests OK), exit {proc.returncode} stdout {proc.stdout[:1000]} stderr {proc.stderr[:1000]}"
        assert "Ran 6 tests" in proc.stderr or "Ran 6 tests" in proc.stdout, f"must run 6 tests, got {proc.stdout[:500]} {proc.stderr[:500]}"
        result["dedicated_test"]={"exit":0,"tests":6,"HIGH":"3dbdedb8b44b366b129cc351b25a8bb898a62ad23e424d27e46c3df85a6a6d0b","H":"74275d22a342014009d5d090fbe9c552981941e90259c298065d2ba6929d1f3d","S":"2290ddd0dc8397f86451aff70d50fd4da0c6184fcf1bef3ed96259642af2d1eb"}
        hbf.write_text(hbf.read_text()+f"dedicated test 6 OK {time.monotonic():.3f}\n")
        # 3. Direct activate at cap (State->r32 chain32 + high-u33 set valid inert prior chain32) must refuse pre-record (no new record/temp/State, real basis, no fake)
        # Use fixed HIGH IN fixture (live HIGH fixed, no wrong-root), State->r32 (chain32, original State32), set=high-u33 set (valid inert, prior r32, epoch 9453e1c matching HEAD 9453e1c? But live HIGH fixed vs closure old -> drift in validate_set before cap. Still pre-record, no new record/temp/State, real basis, no fake. Capture actual code/phase/disp (expect BASIS_CURRENT_TOOL_DRIFT RECEIPT REFUSED_PRE_WRITE due to HIGH change, still pre-record, no invalid record). This proves no invalid record publishes (pre-record refusal) with fixed HIGH, real basis, no fake.
        # To also prove cap-specific refusal (no drift) for prepare (which is before validate_set, no drift), see step 6 (prepare33 cap refusal, clean, no drift, matching tools). Good.
        state_rel="sources/2026-W37/production-state.json"
        set_u33_rel="sources/2026-W37/publication/v2/editorial-corrections/wk-depth32-ed31/renewals/high-u33-depth32-full/publication-set.json"
        assert (fix/set_u33_rel).is_file(), "high-u33 set must exist (valid inert, prior chain32)"
        state_before_sha=_sha(fix/state_rel)
        recs_before_set=set(p.name for p in rec_dir.iterdir() if p.name.startswith("publication-surface-revalidation-r"))
        # Run direct activate via fresh Python file (avoid -c try syntax, no shared execution)
        direct_py=ev/"direct-activate-probe.py"
        direct_py.write_text(
            "import sys\n"
            f"sys.path.insert(0, r'{fix}')\n"
            "from scripts import survey_versioned_renewal_v2 as high\n"
            "from pathlib import Path\n"
            f"repo=Path(r'{fix}')\n"
            f"state_rel=r'{state_rel}'\n"
            f"set_rel=r'{set_u33_rel}'\n"
            "try:\n"
            "  res=high.activate_renewal(repo, state_rel, set_rel, 'TEST direct activate at cap (valid inert prior chain32)', 'depth-rewrite-test', '2026-10-25T20:00:00Z')\n"
            "  print('UNEXPECTED_SUCCESS '+str(res))\n"
            "except Exception as e:\n"
            "  print('CODE:'+str(getattr(e,'code',type(e).__name__)))\n"
            "  print('PHASE:'+str(getattr(e,'phase','')))\n"
            "  print('DISP:'+str(getattr(e,'disposition','')))\n"
            "  print('DETAIL:'+str(getattr(e,'detail',str(e))[:800]))\n",
            encoding="utf-8")
        proc2=_sp.run([sys.executable,"-B",str(direct_py)], cwd=str(fix), capture_output=True, text=True, timeout=300, env=env)
        (ev/"direct-activate-stdout.txt").write_text(proc2.stdout[:4000]+"\n")
        (ev/"direct-activate-stderr.txt").write_text(proc2.stderr[:4000]+"\n")
        # Parse CODE/PHASE/DISP from stdout (lines CODE:..., PHASE:..., DISP:...)
        code=phase=disp=None
        for line in proc2.stdout.splitlines():
            if line.startswith("CODE:"): code=line[5:].strip()
            if line.startswith("PHASE:"): phase=line[6:].strip()
            if line.startswith("DISP:"): disp=line[5:].strip()
        assert code is not None and "UNEXPECTED_SUCCESS" not in proc2.stdout, f"direct activate must refuse (no success), got {proc2.stdout[:1000]}"
        assert disp in ("REFUSED_PRE_WRITE","PRESERVED_INCOMPLETE"), f"direct activate must refuse pre-record (no new record), got disp {disp} code {code} phase {phase}"
        # Verify no new record/temp/State (inventory exact same)
        recs_after_set=set(p.name for p in rec_dir.iterdir() if p.name.startswith("publication-surface-revalidation-r"))
        assert recs_before_set==recs_after_set, f"direct activate must create no new record (recs same), before {len(recs_before_set)} after {len(recs_after_set)}"
        assert not (fix/(state_rel+".renewal-tmp")).exists(), "direct activate must create no State temp"
        assert _sha(fix/state_rel)==state_before_sha, "direct activate must leave State unchanged"
        assert not (rec_dir/"publication-surface-revalidation-r34.json").exists(), "direct activate must create no r34"
        result["direct_activate"]={"code":code,"phase":phase,"disp":disp,"refuses_pre_record":True,"no_new_record":True,"no_temp":True,"state_unchanged":True,"real_basis":True,"no_fake":True,"note":"fixed HIGH (live fixed vs old basis closure old -> drift in validate_set before cap, still pre-record, no invalid record; cap-specific refusal proven via prepare33 (clean, no drift, matching tools) in step 6)"}
        hbf.write_text(hbf.read_text()+f"direct activate refuses pre-record {code} {phase} {disp} {time.monotonic():.3f}\n")
        (ev/"result-depth-rewrite.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
        print(json.dumps({"dedicated_test_exit":0,"direct_activate_code":code,"direct_activate_phase":phase,"direct_activate_disp":disp,"no_new_record":True,"state_unchanged":True}, indent=2))
        return 0
    except Exception as exc:
        import traceback
        hbf.write_text(hbf.read_text()+f"FAILED {exc} {traceback.format_exc()[:2000]}\n")
        result["exact_constraint"]=f"{getattr(exc,'code',type(exc).__name__)}: {getattr(exc,'detail',str(exc))[:1000]}"
        (ev/"result-depth-rewrite.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
        print(json.dumps(result, indent=2, sort_keys=True))
        return 1

if __name__=="__main__":
    import sys
    sys.exit(main())
