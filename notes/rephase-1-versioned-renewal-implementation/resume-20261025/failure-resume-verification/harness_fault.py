#!/usr/bin/env python3
"""Fault/resume harness: OS-level injection at EXACT target FD/path/seam.

No validator/proof mocks, no dummy SHA, no Stub HIGH. Product bytes unchanged.
Usage: python3 harness_fault.py BASE_FIXTURE CASE_ID CASE_ROOT NOW_ISO
CASE_ID in: excl-conflict, excl-samebytes, rec-write, rec-short, rec-fsync, rec-close, rec-combined,
            orphan-resume, state-temp-write, state-temp-close, state-temp-fsync, state-replace-fail,
            postread-new, foreign-symlink, indeterminite, already-active, alias-refuse,
            drift-copy, drift-tool
Each creates byte-independent fork, injects, runs public activate/resume, captures FS delta.
"""
from __future__ import annotations
import hashlib
import json
import os
import shutil
import subprocess
import sys
import traceback
from pathlib import Path

def _sha(p: Path)->str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1<<20), b""):
            h.update(c)
    return h.hexdigest()

def _run_git(cwd: Path, *args):
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"1"})
    return subprocess.run(["git",*args],cwd=str(cwd),capture_output=True,text=True,timeout=60,env=env)

def _copy_independent(src: Path, dst: Path):
    if dst.exists():
        raise RuntimeError(f"dst exists: {dst}")
    # cp -a without -l
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
    p=subprocess.run(["cp","-a",str(src),str(dst)],capture_output=True,text=True,timeout=120,env=env)
    if p.returncode!=0:
        raise RuntimeError(f"cp -a failed: {p.stderr[:500]}")
    # verify no hardlink sharing for a sample + nlink==1
    for rel in ("scripts/survey_versioned_renewal_v2.py","sources/2026-W37/production-state.json"):
        a=(src/rel).stat(); b=(dst/rel).stat()
        if (a.st_dev,a.st_ino)==(b.st_dev,b.st_ino):
            raise RuntimeError(f"inode sharing: {rel}")
        if b.st_nlink!=1:
            raise RuntimeError(f"nlink !=1: {rel} {b.st_nlink}")

def main()->int:
    if len(sys.argv)!=5:
        print(f"usage: {sys.argv[0]} BASE_FIXTURE CASE_ID CASE_ROOT NOW_ISO", flush=True)
        return 2
    BASE=Path(sys.argv[1]).resolve()
    CASE_ID=sys.argv[2].strip()
    CASE_ROOT=Path(sys.argv[3]).resolve()
    NOW_ISO=sys.argv[4].strip()
    for v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
        if os.environ.get(v):
            print(f"UNSAFE {v}", flush=True)
            return 2
    sys.dont_write_bytecode=True
    os.environ["PYTHONDONTWRITEBYTECODE"]="1"
    CASE_ROOT.mkdir(parents=True, exist_ok=True)
    # Base healthy paths (from healthy U1)
    # Discover renewal dir: find fr-u1-weekly
    import glob
    basis_candidates=list((BASE).rglob("renewals/fr-u1-weekly/renewal-basis.json"))
    if not basis_candidates:
        print("FATAL no healthy base (run healthy U1 first)", flush=True)
        return 2
    basis_rel=basis_candidates[0].relative_to(BASE).as_posix()
    # Derive set/State
    basis=json.loads((BASE/basis_rel).read_bytes())
    # set path from finalize: publication-set.json in same dir
    renewal_dir=str(Path(basis_rel).parent.as_posix())
    set_rel=f"{renewal_dir}/publication-set.json"
    state_rel="sources/2026-W37/production-state.json"
    if not (BASE/set_rel).is_file():
        print(f"FATAL set missing: {set_rel}", flush=True)
        return 2
    # Fork
    fork=CASE_ROOT/f"fork-{CASE_ID}"
    _copy_independent(BASE, fork)
    print(f"FORK_OK {fork} CASE={CASE_ID}", flush=True)
    # Insert fork first for imports (fresh Python already, but ensure fixture origin)
    if str(fork) not in sys.path:
        sys.path.insert(0, str(fork))
    # Import AFTER fork (fresh)
    from scripts import survey_production_v2 as core
    from scripts import survey_versioned_renewal_v2 as high
    # Pin product bytes unchanged (HIGH/S/H/Reader/PUB/P1/edpub)
    for rel, expect in (("scripts/survey_versioned_renewal_v2.py","9a0469ef5a6bc2b2e37fc9efb1376cfccbd0333ffaa08a59d23634345d382152"),
                        ("scripts/survey_versioned_renewal_history_v2.py","6fe86e78a12e2159d6ff50dfd7f70fda7b2e0d34d48db26402743edda2eca5ad"),
                        ("scripts/survey_versioned_renewal_source_v2.py","20f63eafc96923dc7be25f3f495b94dd9add0e398d6cdc2fe47c2c9bff46c306")):
        got=_sha(fork/rel)
        if got!=expect:
            print(f"FATAL product drift {rel} {got[:12]} != {expect[:12]}", flush=True)
            return 2
    print("PRODUCT_PIN_OK", flush=True)
    state_before=(fork/state_rel).read_bytes()
    state_before_sha=_sha(fork/state_rel)
    set_before_sha=_sha(fork/set_rel)
    print(f"STATE_BEFORE sha={state_before_sha[:12]} SET_BEFORE sha={set_before_sha[:12]}", flush=True)
    # Determine next record path (for collision cases)
    # Use high._next_record_rel if available, else infer r2
    try:
        # Prior record is r1 (wk-boot-1)
        prior_record_rel="sources/2026-W37/publication/v2/publication-surface-revalidation-r1.json"
        # Next should be r2
        next_record_rel="sources/2026-W37/publication/v2/publication-surface-revalidation-r2.json"
    except Exception:
        next_record_rel="sources/2026-W37/publication/v2/publication-surface-revalidation-r2.json"
    result={}
    # --- OS patch helpers (exact target only) ---
    import os as _os
    _orig_open=_os.open; _orig_write=_os.write; _orig_fsync=_os.fsync; _orig_close=_os.close; _orig_replace=_os.replace
    _orig_lstat=_os.lstat
    def _abs(rel: str)->str:
        return str((fork.resolve().joinpath(*rel.split("/"))))

    # Helper to capture FS delta
    def _delta(paths):
        d={}
        for rel in paths:
            p=fork/rel
            try:
                st=_os.lstat(str(p))
                d[rel]={"exists":True,"is_symlink":False,"size":st.st_size,"dev":st.st_dev,"ino":st.st_ino,"nlink":st.st_nlink,"sha":(_sha(p)[:12] if p.is_file() and not p.is_symlink() else None)}
                try:
                    if p.is_symlink():
                        d[rel]["is_symlink"]=True
                        d[rel]["link_target"]=str(os.readlink(str(p)))
                except Exception:
                    pass
            except FileNotFoundError:
                d[rel]={"exists":False}
            except OSError as e:
                d[rel]={"exists":"error","err":str(e)[:200]}
        return d

    watch=[state_rel, set_rel, next_record_rel, f"{state_rel}.renewal-tmp"]
    try:
        if CASE_ID=="excl-conflict":
            # Pre-create conflicting record
            (fork/next_record_rel).parent.mkdir(parents=True,exist_ok=True)
            (fork/next_record_rel).write_bytes(b'{"conflicting": true}')
            before_delta=_delta(watch)
            try:
                high.activate_renewal(str(fork),state_rel,set_rel,"Core change: fault-resume excl-conflict","fault-resume-fixture",NOW_ISO)
                result={"unexpected":"ACTIVATED"}
            except Exception as e:
                result={"code":getattr(e,"code",type(e).__name__),"phase":getattr(e,"phase",None),"disp":getattr(e,"disposition",None),"detail":str(e)[:500]}
            after_delta=_delta(watch)
            # Verify preserved, no takeover, State unchanged
            result["before_delta"]=before_delta; result["after_delta"]=after_delta
            result["state_unchanged"]=(_sha(fork/state_rel)==state_before_sha)
            result["record_preserved"]=(fork/next_record_rel).read_bytes()==b'{"conflicting": true}'
            # Healthy control in same fork? No, need separate fork for healthy - do inline: remove conflict file in a copy? Instead report healthy as separate case (healthy-activate). Here just record fault.
            # Operator next step: fresh id retry (new renewal) - not executed here, documented.
        elif CASE_ID=="excl-samebytes":
            # Need same bytes as healthy would produce: run healthy activate in a temp copy to get bytes, then pre-create same bytes in fault fork
            tmp_copy=CASE_ROOT/"tmp-healthy-for-samebytes"
            if tmp_copy.exists():
                shutil.rmtree(str(tmp_copy))
            _copy_independent(BASE, tmp_copy)
            sys.path.insert(0, str(tmp_copy))
            # Run healthy activate in tmp_copy to get record bytes (fresh import? use same high but different root - high uses repo path, so okay)
            r=high.activate_renewal(str(tmp_copy),state_rel,set_rel,"Core change: healthy for samebytes","fault-resume-fixture",NOW_ISO)
            rec_rel=r["record_path"]
            rec_bytes=(tmp_copy/rec_rel).read_bytes()
            # Pre-create same bytes in fault fork
            (fork/next_record_rel).parent.mkdir(parents=True,exist_ok=True)
            (fork/next_record_rel).write_bytes(rec_bytes)
            before_delta=_delta(watch)
            try:
                high.activate_renewal(str(fork),state_rel,set_rel,"Core change: fault-resume excl-samebytes","fault-resume-fixture",NOW_ISO)
                result={"unexpected":"ACTIVATED"}
            except Exception as e:
                result={"code":getattr(e,"code",type(e).__name__),"phase":getattr(e,"phase",None),"disp":getattr(e,"disposition",None),"detail":str(e)[:500]}
            after_delta=_delta(watch)
            result["before_delta"]=before_delta; result["after_delta"]=after_delta
            result["state_unchanged"]=(_sha(fork/state_rel)==state_before_sha)
            result["record_preserved"]=((fork/next_record_rel).read_bytes()==rec_bytes)
            shutil.rmtree(str(tmp_copy))
        elif CASE_ID in ("rec-write","rec-short","rec-fsync","rec-close","rec-combined"):
            target_abs=_abs(next_record_rel)
            # Patch os.* only for target_abs
            fail_mode=CASE_ID
            def _patched_write(fd, data):
                # Need to map fd to path? Use /proc/self/fd? Simpler: check if fd corresponds to target via fstat dev/ino after open? Instead patch open to mark fd.
                return _orig_write(fd, data)
            # Better: patch open to return wrapped fd, and track target fds
            target_fds=set()
            def _patched_open(path, flags, *args, **kwargs):
                fd=_orig_open(path, flags, *args, **kwargs)
                try:
                    # Resolve path string
                    if isinstance(path,(str,bytes)):
                        ps=str(path)
                        # Compare resolved absolute
                        if os.path.abspath(ps)==os.path.abspath(target_abs) or ps==target_abs:
                            target_fds.add(fd)
                except Exception:
                    pass
                return fd
            def _patched_write2(fd, data):
                if fd in target_fds:
                    if fail_mode=="rec-write":
                        raise OSError("injected record write failure (exact target)")
                    if fail_mode=="rec-short":
                        # Write half
                        half=data[:len(data)//2] if len(data)>1 else b""
                        n=_orig_write(fd, half)
                        # Return full len to simulate short without error? Actually to trigger post-read mismatch, return full len but wrote half? Or write half and return half? HIGH doesn't check return, so either triggers post-read mismatch. Do half write, return len(data) to hide short.
                        return len(data)
                    if fail_mode=="rec-combined":
                        raise OSError("injected record write failure (combined primary)")
                return _orig_write(fd, data)
            def _patched_fsync2(fd):
                if fd in target_fds and fail_mode in ("rec-fsync",):
                    raise OSError("injected record fsync failure (exact target)")
                if fd in target_fds and fail_mode=="rec-combined":
                    # For combined, let write fail already; fsync not reached? But test combined primary+secondary: write fails + close fails. So fsync pass.
                    pass
                return _orig_fsync(fd)
            def _patched_close2(fd):
                if fd in target_fds and fail_mode=="rec-close":
                    raise OSError("injected record close failure (exact target)")
                if fd in target_fds and fail_mode=="rec-combined":
                    raise OSError("injected record close failure (combined secondary)")
                return _orig_close(fd)
            _os.open=_patched_open; _os.write=_patched_write2; _os.fsync=_patched_fsync2; _os.close=_patched_close2
            before_delta=_delta(watch)
            try:
                high.activate_renewal(str(fork),state_rel,set_rel,f"Core change: fault {fail_mode}","fault-resume-fixture",NOW_ISO)
                result={"unexpected":"ACTIVATED"}
            except Exception as e:
                result={"code":getattr(e,"code",type(e).__name__),"phase":getattr(e,"phase",None),"disp":getattr(e,"disposition",None),"detail":str(e)[:600]}
                result["tb"]=traceback.format_exc()[-2000:]
            finally:
                _os.open=_orig_open; _os.write=_orig_write; _os.fsync=_orig_fsync; _os.close=_orig_close
            after_delta=_delta(watch)
            result["before_delta"]=before_delta; result["after_delta"]=after_delta
            result["state_unchanged"]=(_sha(fork/state_rel)==state_before_sha)
            # Failed partial must exist? Or not? For write failures, _atomic_write_new leaves fd? Actually on failure it does not unlink? Let's check: _atomic_write_new on write failure raises without unlink? It leaves partial? For _replace_state_bytes it unlinks temp on failure. For _atomic_write_new, on primary failure it raises without unlink (leaves partial?). Our harness must NOT delete failed partial - verify it still exists (or not, but we must not delete).
            try:
                result["record_exists_after"]=(fork/next_record_rel).exists()
                if (fork/next_record_rel).exists() and not (fork/next_record_rel).is_symlink():
                    result["record_sha_after"]=_sha(fork/next_record_rel)[:12]
            except Exception as e:
                result["record_exists_after"]=f"error {e}"
        elif CASE_ID=="orphan-resume":
            # Inject replace failure to leave orphan, then ordinary collide + explicit resume
            target_state_abs=_abs(state_rel)
            orig_replace=_os.replace
            def _patched_replace(src,dst):
                # Only fail for State replace (dst == State)
                try:
                    if os.path.abspath(str(dst))==os.path.abspath(target_state_abs):
                        raise OSError("injected State replace failure (orphan test, exact target)")
                except OSError as e:
                    if "injected" in str(e):
                        raise
                return orig_replace(src,dst)
            _os.replace=_patched_replace
            before_delta=_delta(watch)
            try:
                high.activate_renewal(str(fork),state_rel,set_rel,"Core change: orphan setup","fault-resume-fixture",NOW_ISO)
                result={"unexpected":"ACTIVATED despite injected replace"}
            except Exception as e:
                result={"orphan_setup_code":getattr(e,"code",type(e).__name__),"orphan_setup_phase":getattr(e,"phase",None),"orphan_setup_disp":getattr(e,"disposition",None),"orphan_setup_detail":str(e)[:500]}
            finally:
                _os.replace=_orig_replace
            mid_delta=_delta(watch)
            result["mid_delta"]=mid_delta
            # Verify orphan: record exists, State still before
            try:
                rec_exists=(fork/next_record_rel).exists()
                state_still_before=(_sha(fork/state_rel)==state_before_sha)
            except Exception:
                rec_exists=False; state_still_before=False
            result["orphan_record_exists"]=rec_exists
            result["orphan_state_still_before"]=state_still_before
            # Ordinary retry should collide
            try:
                high.activate_renewal(str(fork),state_rel,set_rel,"Core change: orphan ordinary retry","fault-resume-fixture",NOW_ISO)
                result["ordinary_retry"]="UNEXPECTED_ACTIVATED"
            except Exception as e:
                result["ordinary_retry_code"]=getattr(e,"code",type(e).__name__)
                result["ordinary_retry_detail"]=str(e)[:500]
            # Explicit resume should RESUME (ACTIVATED resumed)
            try:
                r2=high.resume_renewal_activation(str(fork),state_rel,next_record_rel)
                result["resume_status"]=r2.get("status")
                result["resume_observed"]=r2.get("observed")
                # Strict readback: State now points to record, receipt/set valid?
                # Verify current State points to record and set valid
                post_state=json.loads((fork/state_rel).read_bytes())
                result["post_pointer"]=post_state.get("publication_revalidation_provenance")
                # Validate set still
                v=high.validate_prepared_renewal_set(str(fork),state_rel,set_rel)
                result["post_validate"]="OK"
            except Exception as e:
                result["resume_code"]=getattr(e,"code",type(e).__name__)
                result["resume_detail"]=str(e)[:800]
                result["resume_tb"]=traceback.format_exc()[-2000:]
            after_delta=_delta(watch+[next_record_rel])
            result["before_delta"]=before_delta; result["after_delta"]=after_delta
        elif CASE_ID in ("state-temp-write","state-temp-close","state-temp-fsync","state-replace-fail"):
            tmp_rel=f"{state_rel}.renewal-tmp"
            tmp_abs=_abs(tmp_rel)
            state_abs=_abs(state_rel)
            target_fds=set()
            def _p_open(path, flags, *a, **k):
                fd=_orig_open(path, flags, *a, **k)
                try:
                    if os.path.abspath(str(path)) in (os.path.abspath(tmp_abs), os.path.abspath(state_abs)):
                        # Only track tmp for temp faults, State for replace? For temp faults track tmp
                        if CASE_ID.startswith("state-temp") and os.path.abspath(str(path))==os.path.abspath(tmp_abs):
                            target_fds.add(fd)
                except Exception:
                    pass
                return fd
            def _p_write(fd, data):
                if fd in target_fds and CASE_ID=="state-temp-write":
                    raise OSError("injected STATE temp write failure (exact target)")
                return _orig_write(fd, data)
            def _p_fsync(fd):
                if fd in target_fds and CASE_ID=="state-temp-fsync":
                    raise OSError("injected STATE temp fsync failure (exact target)")
                return _orig_fsync(fd)
            def _p_close(fd):
                if fd in target_fds and CASE_ID=="state-temp-close":
                    raise OSError("injected STATE temp close failure (exact target)")
                return _orig_close(fd)
            def _p_replace(src,dst):
                try:
                    if CASE_ID=="state-replace-fail" and os.path.abspath(str(dst))==os.path.abspath(state_abs):
                        raise OSError("injected STATE replace failure (exact target)")
                except OSError as e:
                    if "injected" in str(e):
                        raise
                return _orig_replace(src,dst)
            _os.open=_p_open; _os.write=_p_write; _os.fsync=_p_fsync; _os.close=_p_close; _os.replace=_p_replace
            before_delta=_delta(watch)
            try:
                high.activate_renewal(str(fork),state_rel,set_rel,f"Core change: fault {CASE_ID}","fault-resume-fixture",NOW_ISO)
                result={"unexpected":"ACTIVATED"}
            except Exception as e:
                result={"code":getattr(e,"code",type(e).__name__),"phase":getattr(e,"phase",None),"disp":getattr(e,"disposition",None),"detail":str(e)[:600]}
            finally:
                _os.open=_orig_open; _os.write=_orig_write; _os.fsync=_orig_fsync; _os.close=_orig_close; _os.replace=_orig_replace
            after_delta=_delta(watch)
            result["before_delta"]=before_delta; result["after_delta"]=after_delta
            result["state_unchanged"]=(_sha(fork/state_rel)==state_before_sha if (fork/state_rel).exists() else False)
            # Old state must persist (State SHA == before)
        elif CASE_ID=="postread-new":
            # After replace, readback fails: patch _fd_safe_read for State post-replace? Simpler: patch os.open for State post-replace read to raise? But need replace to succeed, then readback to fail.
            # We patch high._fd_safe_read to fail only for State post-replace? That would be validator mock? No, _fd_safe_read is IO, not validator. But to keep OS-level only, patch os.read? HIGH uses os.open+read via _fd_safe_read (which uses os.open O_NOFOLLOW). We can patch os.open for State path after replace to fail once.
            # Approach: allow first replace to succeed, then fail subsequent open of State.
            state_abs=_abs(state_rel)
            call_count={"n":0}
            orig_open2=_os.open
            def _p_open2(path, flags, *a, **k):
                try:
                    if os.path.abspath(str(path))==os.path.abspath(state_abs):
                        # Count State opens: first few are pre-reads, later is post-replace read. Fail the post-replace read (after replace, there will be opens for post verification).
                        # We need to let replace happen first. So fail only after replace has been called.
                        if call_count.get("replaced",False):
                            raise OSError("injected post-replace read failure (exact target)")
                except OSError:
                    raise
                except Exception:
                    pass
                return orig_open2(path, flags, *a, **k)
            orig_replace2=_os.replace
            def _p_replace2(src,dst):
                r=orig_replace2(src,dst)
                try:
                    if os.path.abspath(str(dst))==os.path.abspath(state_abs):
                        call_count["replaced"]=True
                except Exception:
                    pass
                return r
            _os.open=_p_open2; _os.replace=_p_replace2
            before_delta=_delta(watch)
            try:
                high.activate_renewal(str(fork),state_rel,set_rel,"Core change: postread-new","fault-resume-fixture",NOW_ISO)
                result={"unexpected":"ACTIVATED"}
            except Exception as e:
                result={"code":getattr(e,"code",type(e).__name__),"phase":getattr(e,"phase",None),"disp":getattr(e,"disposition",None),"detail":str(e)[:800]}
            finally:
                _os.open=_orig_open; _os.replace=_orig_replace
            after_delta=_delta(watch+[next_record_rel])
            result["before_delta"]=before_delta; result["after_delta"]=after_delta
            # Record must be preserved even though State is new (replaced) but readback failed
            try:
                result["record_exists"]=(fork/next_record_rel).exists()
                # State file should be new (different SHA from before) if replace succeeded
                try:
                    new_sha=_sha(fork/state_rel)[:12]
                except Exception:
                    new_sha="unreadable (injected)"
                result["state_sha_after"]=new_sha
                result["state_was_before"]=state_before_sha[:12]
            except Exception as e:
                result["post_err"]=str(e)[:300]
        elif CASE_ID=="foreign-symlink":
            # Create symlink at expected record path pointing outside
            outside=CASE_ROOT/"outside-secret.txt"
            outside.write_text("outside",encoding="utf-8")
            if (fork/next_record_rel).exists():
                (fork/next_record_rel).unlink()
            (fork/next_record_rel).parent.mkdir(parents=True,exist_ok=True)
            os.symlink(str(outside), str(fork/next_record_rel))
            before_delta=_delta(watch)
            try:
                high.activate_renewal(str(fork),state_rel,set_rel,"Core change: foreign symlink","fault-resume-fixture",NOW_ISO)
                result={"unexpected":"ACTIVATED"}
            except Exception as e:
                result={"code":getattr(e,"code",type(e).__name__),"phase":getattr(e,"phase",None),"disp":getattr(e,"disposition",None),"detail":str(e)[:600]}
            after_delta=_delta(watch)
            result["before_delta"]=before_delta; result["after_delta"]=after_delta
            # Verify no unowned delete: symlink still exists, outside preserved
            result["symlink_preserved"]=(fork/next_record_rel).is_symlink()
            result["outside_preserved"]=outside.is_file() and outside.read_text()=="outside"
            result["state_unchanged"]=(_sha(fork/state_rel)==state_before_sha)
        elif CASE_ID=="indeterminite":
            # Corrupt State to neither before nor after (random valid JSON but wrong provenance)
            st=json.loads((fork/state_rel).read_bytes())
            st["publication_revalidation_provenance"]={"path":"sources/2026-W37/publication/v2/publication-surface-revalidation-r999.json","sha256":"0"*64}
            (fork/state_rel).write_bytes(json.dumps(st,indent=2,sort_keys=True).encode())
            before_delta=_delta(watch)
            try:
                high.activate_renewal(str(fork),state_rel,set_rel,"Core change: indeterminite","fault-resume-fixture",NOW_ISO)
                result={"unexpected":"ACTIVATED"}
            except Exception as e:
                result={"code":getattr(e,"code",type(e).__name__),"phase":getattr(e,"phase",None),"disp":getattr(e,"disposition",None),"detail":str(e)[:600]}
            after_delta=_delta(watch+[next_record_rel])
            result["before_delta"]=before_delta; result["after_delta"]=after_delta
            result["record_not_created"]=not (fork/next_record_rel).exists()
            # Preserve: no rollback (State stays corrupted, not reverted to before), no adoption
            try:
                cur=json.loads((fork/state_rel).read_bytes())
                result["state_still_corrupted"]=(cur.get("publication_revalidation_provenance",{}).get("path","").endswith("r999.json"))
            except Exception:
                result["state_still_corrupted"]="unreadable"
        elif CASE_ID=="already-active":
            # Healthy activate first, then retry canonical + alias
            try:
                r=high.activate_renewal(str(fork),state_rel,set_rel,"Core change: already-active setup","fault-resume-fixture",NOW_ISO)
                result["setup_status"]=r.get("status")
                result["setup_record"]=r.get("record_path")
                setup_sha=_sha(fork/state_rel)[:12]
                result["setup_state_sha"]=setup_sha
                # Retry canonical
                try:
                    r2=high.activate_renewal(str(fork),state_rel,set_rel,"Core change: already-active retry","fault-resume-fixture",NOW_ISO)
                    result["retry_status"]=r2.get("status")
                    result["retry_observed"]=r2.get("observed")
                    result["retry_state_unchanged"]=(_sha(fork/state_rel)[:12]==setup_sha)
                except Exception as e:
                    result["retry_code"]=getattr(e,"code",type(e).__name__)
                    result["retry_detail"]=str(e)[:500]
            except Exception as e:
                result["setup_code"]=getattr(e,"code",type(e).__name__)
                result["setup_detail"]=str(e)[:800]
            after_delta=_delta(watch+[next_record_rel])
            result["after_delta"]=after_delta
        elif CASE_ID=="alias-refuse":
            # Healthy activate first, then alias set path (symlink different spelling same bytes)
            try:
                r=high.activate_renewal(str(fork),state_rel,set_rel,"Core change: alias setup","fault-resume-fixture",NOW_ISO)
                result["setup_status"]=r.get("status")
                alias_rel=f"{renewal_dir}/alias-publication-set.json"
                # Create symlink alias (different spelling, same bytes via symlink)
                if (fork/alias_rel).exists() or (fork/alias_rel).is_symlink():
                    try:
                        (fork/alias_rel).unlink()
                    except Exception:
                        pass
                os.symlink(str(fork/set_rel), str(fork/alias_rel))
                try:
                    high.activate_renewal(str(fork),state_rel,alias_rel,"Core change: alias retry","fault-resume-fixture",NOW_ISO)
                    result["alias_retry"]="UNEXPECTED_ACTIVATED"
                except Exception as e:
                    result["alias_code"]=getattr(e,"code",type(e).__name__)
                    result["alias_detail"]=str(e)[:600]
                    result["alias_is_refusal"]=("alias" in str(e).lower() or "RECORD_COLLISION" in str(getattr(e,"code","")))
                # Verify no new record beyond setup, State unchanged after alias refuse
                result["alias_symlink_preserved"]=(fork/alias_rel).is_symlink()
            except Exception as e:
                result["setup_code"]=getattr(e,"code",type(e).__name__)
                result["setup_detail"]=str(e)[:800]
            after_delta=_delta(watch)
            result["after_delta"]=after_delta
        elif CASE_ID in ("drift-copy","drift-tool"):
            # Mutate retained COPY or tool after finalize, before activate
            if CASE_ID=="drift-copy":
                # Find retained COPY path from basis
                b=json.loads((fork/basis_rel).read_bytes())
                copy_rel=b.get("retained_copy_ref",{}).get("path") or b.get("retained_copy",{}).get("path")
                if not copy_rel:
                    # Fallback: retained/before/... from prep
                    copy_rel=f"{renewal_dir}/retained/before/{state_rel}"
                # Mutate one byte
                data=(fork/copy_rel).read_bytes()
                mutated=data[:-1]+(b"X" if data[-1:]!=b"X" else b"Y")
                (fork/copy_rel).write_bytes(mutated)
                result["drift_target"]=copy_rel
            else:
                # Tool drift: mutate a closure file (e.g., scripts/survey_production_v2.py) by appending comment? Must be exact? For drift test, change one byte in a tool file that is in closure.
                # Use templates/survey/jgaisurvey.sty (style) - change one byte? But that would affect U rederivation? Better to mutate a non-trio tool file that is in closure, e.g., scripts/survey_quality_v2.py append newline? That changes SHA, should be detected as TOOL_DRIFT.
                tool_rel="scripts/survey_quality_v2.py"
                data=(fork/tool_rel).read_bytes()
                (fork/tool_rel).write_bytes(data+b"\n# drift-test\n")
                result["drift_target"]=tool_rel
            before_delta=_delta(watch)
            try:
                high.activate_renewal(str(fork),state_rel,set_rel,f"Core change: fault {CASE_ID}","fault-resume-fixture",NOW_ISO)
                result={"unexpected":"ACTIVATED despite drift","drift_target":result.get("drift_target")}
            except Exception as e:
                # Preserve drift_target
                dt=result.get("drift_target")
                result={"code":getattr(e,"code",type(e).__name__),"phase":getattr(e,"phase",None),"disp":getattr(e,"disposition",None),"detail":str(e)[:800],"drift_target":dt}
            after_delta=_delta(watch+[next_record_rel])
            result["before_delta"]=before_delta; result["after_delta"]=after_delta
            result["state_unchanged"]=(_sha(fork/state_rel)==state_before_sha if (fork/state_rel).exists() else False)
            result["record_not_created"]=not (fork/next_record_rel).exists()
        else:
            print(f"UNKNOWN CASE {CASE_ID}", flush=True)
            return 2
    except Exception as e:
        result["harness_error"]=str(e)[:1000]
        result["harness_tb"]=traceback.format_exc()[-3000:]
    # Write result
    out_path=CASE_ROOT/f"result-{CASE_ID}.json"
    out_path.write_text(json.dumps(result,indent=1,sort_keys=True),encoding="utf-8")
    print(f"CASE_DONE {CASE_ID} -> {out_path}", flush=True)
    # Print summary for logs
    print(json.dumps({k:v for k,v in result.items() if k in ("code","phase","disp","setup_status","retry_status","resume_status","resume_observed","alias_code","ordinary_retry_code")},indent=1), flush=True)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
