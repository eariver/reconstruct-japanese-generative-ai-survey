#!/usr/bin/env python3
"""Continuation fault/resume: race/foreign/postread/indeterminite/alias/orphan-manual.

OS-level ONLY at EXACT target FD/path/seam. No validator/proof mocks, no dummy SHA, no Stub HIGH.
Product bytes unchanged (HIGH 9a0469ef... pinned before each case).
Usage: python3 harness_continuation.py BASE_FIXTURE CASE_ID CASE_ROOT NOW_ISO
CASE_ID: excl-race-conflict, excl-race-samebytes, foreign-race-symlink,
         postread-dirfd, indeterminite-resume, alias-hardlink, orphan-manual-resume
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

def _copy(src: Path, dst: Path):
    if dst.exists():
        raise RuntimeError(f"dst exists: {dst}")
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
    p=subprocess.run(["cp","-a",str(src),str(dst)],capture_output=True,text=True,timeout=180,env=env)
    if p.returncode!=0:
        raise RuntimeError(f"cp -a failed: {p.stderr[:500]}")
    for rel in ("scripts/survey_versioned_renewal_v2.py","sources/2026-W37/production-state.json"):
        a=(src/rel).stat(); b=(dst/rel).stat()
        if (a.st_dev,a.st_ino)==(b.st_dev,b.st_ino):
            raise RuntimeError(f"inode sharing: {rel}")
        if b.st_nlink!=1:
            raise RuntimeError(f"nlink !=1: {rel}")

def main()->int:
    if len(sys.argv)!=5:
        print(f"usage: {sys.argv[0]} BASE CASE_ID CASE_ROOT NOW_ISO", flush=True)
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
    # Base healthy paths (fr-u1-weekly SEALED_INERT)
    basis_candidates=list(BASE.rglob("renewals/fr-u1-weekly/renewal-basis.json"))
    if not basis_candidates:
        print("FATAL no healthy base (fr-u1-weekly)", flush=True)
        return 2
    basis_rel=basis_candidates[0].relative_to(BASE).as_posix()
    renewal_dir=str(Path(basis_rel).parent.as_posix())
    set_rel=f"{renewal_dir}/publication-set.json"
    state_rel="sources/2026-W37/production-state.json"
    if not (BASE/set_rel).is_file():
        print(f"FATAL set missing: {set_rel}", flush=True)
        return 2
    fork=CASE_ROOT/f"fork-{CASE_ID}"
    _copy(BASE, fork)
    print(f"FORK_OK {fork} CASE={CASE_ID}", flush=True)
    if str(fork) not in sys.path:
        sys.path.insert(0, str(fork))
    from scripts import survey_production_v2 as core
    from scripts import survey_versioned_renewal_v2 as high
    for rel, expect in (("scripts/survey_versioned_renewal_v2.py","9a0469ef5a6bc2b2e37fc9efb1376cfccbd0333ffaa08a59d23634345d382152"),
                        ("scripts/survey_versioned_renewal_history_v2.py","6fe86e78a12e2159d6ff50dfd7f70fda7b2e0d34d48db26402743edda2eca5ad"),
                        ("scripts/survey_versioned_renewal_source_v2.py","20f63eafc96923dc7be25f3f495b94dd9add0e398d6cdc2fe47c2c9bff46c306")):
        if _sha(fork/rel)!=expect:
            print(f"FATAL product drift {rel}", flush=True)
            return 2
    print("PRODUCT_PIN_OK (pinned 740, HIGH same, P3S old ad60, don't mix 9e2a)", flush=True)
    state_before=(fork/state_rel).read_bytes()
    state_before_sha=_sha(fork/state_rel)
    set_before_sha=_sha(fork/set_rel)
    print(f"STATE_BEFORE {state_before_sha[:12]} SET_BEFORE {set_before_sha[:12]}", flush=True)
    next_record_rel="sources/2026-W37/publication/v2/publication-surface-revalidation-r2.json"
    import os as _os
    _orig_open=_os.open; _orig_write=_os.write; _orig_fsync=_os.fsync; _orig_close=_os.close
    _orig_replace=_os.replace; _orig_lstat=_os.lstat; _orig_scandir=_os.scandir
    _orig_read=_os.read; _orig_fstat=_os.fstat
    def _abs(rel: str)->str:
        return str(fork.resolve().joinpath(*rel.split("/")))
    def _delta(paths):
        d={}
        for rel in paths:
            p=fork/rel
            try:
                st=_os.lstat(str(p))
                import stat as _st
                d[rel]={"exists":True,"is_symlink":_st.S_ISLNK(st.st_mode),"size":st.st_size,"dev":st.st_dev,"ino":st.st_ino,"nlink":st.st_nlink,"sha":(_sha(p)[:12] if p.is_file() and not p.is_symlink() else None)}
                try:
                    if p.is_symlink():
                        d[rel]["link_target"]=str(os.readlink(str(p)))
                except Exception:
                    pass
            except FileNotFoundError:
                d[rel]={"exists":False}
            except OSError as e:
                d[rel]={"exists":"error","err":str(e)[:200]}
        return d
    watch=[state_rel, set_rel, next_record_rel, f"{state_rel}.renewal-tmp"]
    result={}
    try:
        if CASE_ID in ("excl-race-conflict","excl-race-samebytes"):
            # Pre-create r2 (conflict bytes OR same bytes via H-ACT fork copy, no new live writer)
            if CASE_ID=="excl-race-conflict":
                fake_bytes=b'{"conflicting": true}'
                fault_reason=f"Core change: fault {CASE_ID}"
            else:
                # Same-bytes: copy r2 from saved H-ACT fork (same BASE, same State before/set, same reason/executor/NOW_ISO)
                # H-ACT used reason "Core change: healthy control", NOW_ISO 2026-10-25T06:10:00+00:00. Use same for fault attempt below.
                hact_r2=Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-versioned-renewal-implementation/resume-20261025/failure-resume-verification/raw/case-healthy-activate-20261025T150500Z/fork-healthy-activate")/next_record_rel
                if not hact_r2.is_file():
                    raise RuntimeError(f"H-ACT r2 missing for samebytes (no duplicate writer): {hact_r2}")
                fake_bytes=hact_r2.read_bytes()
                # Fault attempt MUST use same reason/executor/NOW_ISO as H-ACT to make would-be bytes identical (same intent, same bytes)
                fault_reason="Core change: healthy control"
                print(f"SAMEBYTES from H-ACT len={len(fake_bytes)} sha={hashlib.sha256(fake_bytes).hexdigest()[:12]} (no new writer, avoid duplicate)", flush=True)
            (fork/next_record_rel).parent.mkdir(parents=True,exist_ok=True)
            (fork/next_record_rel).write_bytes(fake_bytes)
            print(f"PRECREATE r2 {len(fake_bytes)}B sha={hashlib.sha256(fake_bytes).hexdigest()[:12]}", flush=True)
            # Race: hide r2 during _next_record_rel iterdir scan, reveal before O_EXCL/lstat
            # _next_record_rel does (repo.resolve().joinpath(parent)).iterdir() -> os.scandir
            record_parent="sources/2026-W37/publication/v2"
            record_parent_abs=_abs(record_parent)
            hide_name="publication-surface-revalidation-r2.json"
            scan_phase={"hiding":True}
            class _FilteredScandir:
                def __init__(self, it, hide):
                    self._it=it; self._hide=hide
                def __enter__(self):
                    try:
                        self._it.__enter__()
                    except Exception:
                        pass
                    return self
                def __exit__(self, *a):
                    try:
                        return self._it.__exit__(*a)
                    except Exception:
                        try:
                            self._it.close()
                        except Exception:
                            pass
                        return False
                def __iter__(self):
                    for e in self._it:
                        if e.name!=self._hide:
                            yield e
                def close(self):
                    try:
                        self._it.close()
                    except Exception:
                        pass
            def _patched_scandir(path, *a, **k):
                it=_orig_scandir(path, *a, **k)
                try:
                    if os.path.abspath(str(path))==os.path.abspath(record_parent_abs) and scan_phase["hiding"]:
                        return _FilteredScandir(it, hide_name)
                except Exception:
                    pass
                return it
            _os.scandir=_patched_scandir
            before_delta=_delta(watch)
            try:
                # First call: HIGH scans (hiding True) -> computes r2, then lstat(r2) should find fake (since lstat not hidden) -> RECORD_COLLISION before O_EXCL
                # To ensure lstat sees fake, keep hiding True only for scandir, lstat always sees real FS (fake exists) -> collision at lstat check (before O_EXCL), ideal.
                # For samebytes, fault_reason == H-ACT reason (same intent, same bytes) to prove even same-bytes refuses (no takeover).
                _fr = fault_reason if CASE_ID=="excl-race-samebytes" else f"Core change: fault {CASE_ID}"
                high.activate_renewal(str(fork),state_rel,set_rel,_fr,"fault-resume-fixture",NOW_ISO)
                result={"unexpected":"ACTIVATED (race hiding failed, advanced to r3?)"}
            except Exception as e:
                result={"code":getattr(e,"code",type(e).__name__),"phase":getattr(e,"phase",None),"disp":getattr(e,"disposition",None),"detail":str(e)[:800]}
            finally:
                _os.scandir=_orig_scandir
                scan_phase["hiding"]=False
            after_delta=_delta(watch+[next_record_rel])
            result["before_delta"]=before_delta; result["after_delta"]=after_delta
            result["state_unchanged"]=(_sha(fork/state_rel)==state_before_sha if (fork/state_rel).exists() else False)
            try:
                result["record_preserved"]=((fork/next_record_rel).read_bytes()==fake_bytes)
            except Exception:
                result["record_preserved"]=False
            # Healthy control is H-ACT (same API no fault/no precreate → ACTIVATED r2). Document, not re-run here (avoid duplicate live writer; H-ACT already saved as case-healthy-activate).
            result["healthy_control"]="H-ACT case-healthy-activate-20261025T150500Z (same API no fault/no precreate → ACTIVATED r2, proves race-hiding caused refusal)"
            # Operator next: NEW id/copy retry (fresh fork without fake r2); explicit resume NOT applicable (no complete valid record with full intent, fake has no intent). Preserve fake r2 (no delete).
        elif CASE_ID=="foreign-race-symlink":
            outside=CASE_ROOT/"outside-secret-race.txt"
            outside.write_text("outside-race",encoding="utf-8")
            if (fork/next_record_rel).exists() or (fork/next_record_rel).is_symlink():
                try:
                    (fork/next_record_rel).unlink()
                except Exception:
                    pass
            (fork/next_record_rel).parent.mkdir(parents=True,exist_ok=True)
            os.symlink(str(outside), str(fork/next_record_rel))
            print(f"PRECREATE symlink r2 -> outside", flush=True)
            record_parent="sources/2026-W37/publication/v2"
            record_parent_abs=_abs(record_parent)
            hide_name="publication-surface-revalidation-r2.json"
            scan_phase={"hiding":True}
            class _FilteredScandir2:
                def __init__(self, it, hide):
                    self._it=it; self._hide=hide
                def __enter__(self):
                    try:
                        self._it.__enter__()
                    except Exception:
                        pass
                    return self
                def __exit__(self, *a):
                    try:
                        return self._it.__exit__(*a)
                    except Exception:
                        try:
                            self._it.close()
                        except Exception:
                            pass
                        return False
                def __iter__(self):
                    for e in self._it:
                        if e.name!=self._hide:
                            yield e
                def close(self):
                    try:
                        self._it.close()
                    except Exception:
                        pass
            def _patched_scandir2(path, *a, **k):
                it=_orig_scandir(path, *a, **k)
                try:
                    if os.path.abspath(str(path))==os.path.abspath(record_parent_abs) and scan_phase["hiding"]:
                        return _FilteredScandir2(it, hide_name)
                except Exception:
                    pass
                return it
            _os.scandir=_patched_scandir2
            before_delta=_delta(watch)
            try:
                high.activate_renewal(str(fork),state_rel,set_rel,"Core change: foreign race symlink","fault-resume-fixture",NOW_ISO)
                result={"unexpected":"ACTIVATED (race hiding failed)"}
            except Exception as e:
                result={"code":getattr(e,"code",type(e).__name__),"phase":getattr(e,"phase",None),"disp":getattr(e,"disposition",None),"detail":str(e)[:800]}
            finally:
                _os.scandir=_orig_scandir
            after_delta=_delta(watch)
            result["before_delta"]=before_delta; result["after_delta"]=after_delta
            result["symlink_preserved"]=(fork/next_record_rel).is_symlink()
            try:
                result["outside_preserved"]=(outside.is_file() and outside.read_text()=="outside-race")
            except Exception:
                result["outside_preserved"]=False
            result["state_unchanged"]=(_sha(fork/state_rel)==state_before_sha)
            result["no_unowned_delete"]=bool(result["symlink_preserved"] and result["outside_preserved"])
            result["healthy_control"]="H-ACT (same API no symlink/no precreate → ACTIVATED, proves symlink+race caused refusal, no unowned delete)"
        elif CASE_ID=="postread-dirfd":
            # dir_fd-aware: fail State leaf open AFTER replace succeeded (State new, record exists, readback fails → INDETERMINATE, observed NEW/unknown, record preserved)
            state_abs=_abs(state_rel)
            replaced={"done":False}
            orig_replace2=_os.replace
            def _p_replace(src,dst):
                r=orig_replace2(src,dst)
                try:
                    if os.path.abspath(str(dst))==os.path.abspath(state_abs):
                        replaced["done"]=True
                except Exception:
                    pass
                return r
            # Patch os.open to fail State leaf opens AFTER replace (leaf name match, any dir_fd)
            orig_open2=_os.open
            def _p_open(path, flags, *a, **k):
                try:
                    dirfd=k.get("dir_fd",None)
                    # Leaf open for State: path == "production-state.json" (leaf) with dir_fd (from _fd_safe_read), AFTER replace
                    if replaced["done"] and isinstance(path,(str,bytes)) and str(path)=="production-state.json":
                        raise OSError("injected post-replace State leaf open failure (exact dir_fd leaf, post-replace)")
                    # Also catch full-path opens after replace (for _read_bytes_bounded post-replace verify which uses full path? Actually _replace_state_bytes post-read uses _fd_safe_read (dir_fd leaf), and activate post-read uses _read_bytes_bounded (full path via _safe_path/FD? _read_bytes_bounded uses _fd_safe_read internally? It uses _fd_safe_read? Actually _read_bytes_bounded -> _fd_safe_read? No, _read_bytes_bounded uses _fd_safe_read? Let's check: _read_bytes_bounded calls _fd_safe_read? In current code, _read_bytes_bounded is via FD (_fd_safe_read). So leaf patch covers both. Also patch full-path State opens after replace as fallback.
                    if replaced["done"] and isinstance(path,(str,bytes)):
                        try:
                            if os.path.abspath(str(path))==os.path.abspath(state_abs):
                                raise OSError("injected post-replace State full-path open failure (exact target, post-replace)")
                        except OSError:
                            raise
                        except Exception:
                            pass
                except OSError:
                    raise
                except Exception:
                    pass
                return orig_open2(path, flags, *a, **k)
            _os.replace=_p_replace; _os.open=_p_open
            before_delta=_delta(watch)
            try:
                high.activate_renewal(str(fork),state_rel,set_rel,"Core change: postread dir_fd","fault-resume-fixture",NOW_ISO)
                result={"unexpected":"ACTIVATED (dir_fd patch missed)"}
            except Exception as e:
                result={"code":getattr(e,"code",type(e).__name__),"phase":getattr(e,"phase",None),"disp":getattr(e,"disposition",None),"detail":str(e)[:1000]}
            finally:
                _os.replace=_orig_replace; _os.open=_orig_open
            after_delta=_delta(watch+[next_record_rel])
            result["before_delta"]=before_delta; result["after_delta"]=after_delta
            try:
                result["record_exists"]=(fork/next_record_rel).is_file() and not (fork/next_record_rel).is_symlink()
            except Exception:
                result["record_exists"]=False
            # State is new (replaced) but unreadable via patched open? After finally restore, we can read via original open to get actual new SHA (proves State new, observed NEW/unknown at failure time)
            try:
                new_sha=_sha(fork/state_rel)[:12]
            except Exception as e:
                new_sha=f"unreadable:{str(e)[:100]}"
            result["state_sha_after"]=new_sha
            result["state_was_before"]=state_before_sha[:12]
            result["record_preserved"]=bool(result.get("record_exists"))
            result["healthy_control"]="H-ACT (same API no post-replace read fault → ACTIVATED, proves read fault caused INDETERMINATE, record preserved, State new but observed unknown at failure)"
        elif CASE_ID=="indeterminite-resume":
            # After healthy ACTIVATED r2 in this fork, corrupt State to neither before (ca7c) nor after (new r2 State) → resume(r2) INDETERMINATE, preserve
            try:
                r=high.activate_renewal(str(fork),state_rel,set_rel,"Core change: indeterminite setup","fault-resume-fixture",NOW_ISO)
                setup_record=r["record_path"]
                setup_state_sha=_sha(fork/state_rel)[:12]
                result["setup_status"]=r.get("status")
                result["setup_record"]=setup_record
                result["setup_state_sha"]=setup_state_sha
            except Exception as e:
                result["setup_code"]=getattr(e,"code",type(e).__name__)
                result["setup_detail"]=str(e)[:500]
                out=CASE_ROOT/f"result-{CASE_ID}.json"
                out.write_text(json.dumps(result,indent=1,sort_keys=True),encoding="utf-8")
                print(f"CASE_DONE {CASE_ID}", flush=True)
                return 0
            # Corrupt State to neither (valid JSON, wrong provenance r999, different SHA from both before and after)
            st=json.loads((fork/state_rel).read_bytes())
            st["publication_revalidation_provenance"]={"path":"sources/2026-W37/publication/v2/publication-surface-revalidation-r999.json","sha256":"0"*64}
            (fork/state_rel).write_bytes(core.json_bytes(st))
            corrupted_sha=_sha(fork/state_rel)[:12]
            result["corrupted_sha"]=corrupted_sha
            result["before_sha"]=state_before_sha[:12]
            result["setup_state_sha2"]=setup_state_sha
            before_delta=_delta(watch+[setup_record])
            try:
                high.resume_renewal_activation(str(fork),state_rel,setup_record)
                result["resume_unexpected"]="ACTIVATED (should be INDETERMINATE)"
            except Exception as e:
                result["resume_code"]=getattr(e,"code",type(e).__name__)
                result["resume_phase"]=getattr(e,"phase",None)
                result["resume_disp"]=getattr(e,"disposition",None)
                result["resume_detail"]=str(e)[:800]
            after_delta=_delta(watch+[setup_record])
            result["before_delta"]=before_delta; result["after_delta"]=after_delta
            # Preserve: record exists, corrupted State preserved (not reverted to before/after, no rollback/adoption/deletion)
            try:
                result["record_preserved"]=(fork/setup_record).is_file()
                cur=json.loads((fork/state_rel).read_bytes())
                result["state_still_corrupted"]=(cur.get("publication_revalidation_provenance",{}).get("path","").endswith("r999.json"))
            except Exception:
                result["record_preserved"]=False; result["state_still_corrupted"]="unreadable"
            result["healthy_control"]="already-active retry (State expected-after → ALREADY_ACTIVE readonly) vs this neither-nor → INDETERMINATE (proves unknown-State preservation, no rollback/overwrite/adoption)"
        elif CASE_ID=="alias-hardlink":
            # True B3: hardlink same inode different spelling, same FILE SHA → RECORD_COLLISION (NOT ALREADY_ACTIVE), no new record
            try:
                r=high.activate_renewal(str(fork),state_rel,set_rel,"Core change: alias hardlink setup","fault-resume-fixture",NOW_ISO)
                result["setup_status"]=r.get("status")
                setup_state_sha=_sha(fork/state_rel)[:12]
                result["setup_state_sha"]=setup_state_sha
            except Exception as e:
                result["setup_code"]=getattr(e,"code",type(e).__name__)
                result["setup_detail"]=str(e)[:500]
                out=CASE_ROOT/f"result-{CASE_ID}.json"
                out.write_text(json.dumps(result,indent=1,sort_keys=True),encoding="utf-8")
                print(f"CASE_DONE {CASE_ID}", flush=True)
                return 0
            alias_rel=f"{renewal_dir}/alias-hardlink-publication-set.json"
            # Hardlink (same inode, different spelling, same bytes/SHA)
            if (fork/alias_rel).exists() or (fork/alias_rel).is_symlink():
                try:
                    (fork/alias_rel).unlink()
                except Exception:
                    pass
            _os.link(str(fork/set_rel), str(fork/alias_rel))
            # Verify same inode, same SHA, different spelling, nlink==2
            s_id=_os.lstat(str(fork/set_rel)); a_id=_os.lstat(str(fork/alias_rel))
            result["same_inode"]=((s_id.st_dev,s_id.st_ino)==(a_id.st_dev,a_id.st_ino))
            result["same_sha"]=(_sha(fork/set_rel)==_sha(fork/alias_rel))
            result["different_spelling"]=(set_rel!=alias_rel)
            result["nlink_set"]=s_id.st_nlink
            before_delta=_delta(watch+[alias_rel])
            try:
                high.activate_renewal(str(fork),state_rel,alias_rel,"Core change: alias hardlink retry","fault-resume-fixture",NOW_ISO)
                result["alias_unexpected"]="ACTIVATED (should refuse, NOT ALREADY_ACTIVE)"
            except Exception as e:
                result["alias_code"]=getattr(e,"code",type(e).__name__)
                result["alias_phase"]=getattr(e,"phase",None)
                result["alias_disp"]=getattr(e,"disposition",None)
                result["alias_detail"]=str(e)[:800]
                result["alias_is_collision"]=("RECORD_COLLISION" in str(getattr(e,"code","")) or "alias" in str(e).lower())
                result["alias_not_already_active"]=("ALREADY_ACTIVE" not in str(getattr(e,"code","")) and "ALREADY_ACTIVE" not in str(e))
            after_delta=_delta(watch+[alias_rel])
            result["before_delta"]=before_delta; result["after_delta"]=after_delta
            result["alias_preserved"]=((fork/alias_rel).exists() and not (fork/alias_rel).is_symlink())
            result["state_unchanged"]=(_sha(fork/state_rel)[:12]==setup_state_sha)
            result["no_new_record"]=not (fork/"sources/2026-W37/publication/v2/publication-surface-revalidation-r3.json").exists()
            result["healthy_control"]="already-active canonical retry (exact spelling+SHA+inode → ALREADY_ACTIVE readonly) vs alias hardlink (different spelling same SHA/inode → RECORD_COLLISION, NOT ALREADY_ACTIVE)"
        elif CASE_ID=="orphan-manual-resume":
            # Manual orphan without tmp: copy r2 from saved H-ACT fork (no new live writer, avoid duplicate + wrong-root)
            # H-ACT r2 has same BASE State before/set, reason "healthy control", NOW_ISO 2026-10-25T06:10:00+00:00. Copy exactly (same intent).
            hact_r2_src=Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-versioned-renewal-implementation/resume-20261025/failure-resume-verification/raw/case-healthy-activate-20261025T150500Z/fork-healthy-activate")/next_record_rel
            if not hact_r2_src.is_file():
                raise RuntimeError(f"H-ACT r2 missing for orphan-manual (no duplicate writer): {hact_r2_src}")
            rec_bytes=hact_r2_src.read_bytes()
            rec_sha=hashlib.sha256(rec_bytes).hexdigest()[:12]
            print(f"ORPHAN_SRC H-ACT r2 sha={rec_sha} len={len(rec_bytes)} (no new writer)", flush=True)
            # Fork fault already has State before, no r2, no tmp. Copy r2 as orphan (byte-independent, no hardlinks)
            (fork/next_record_rel).parent.mkdir(parents=True,exist_ok=True)
            (fork/next_record_rel).write_bytes(rec_bytes)
            print(f"ORPHAN_COPY r2 into fault fork (State before {state_before_sha[:12]}, no tmp)", flush=True)
            # Verify: record exists, State before, no tmp, full intent fields present?
            rec_json=json.loads(rec_bytes)
            result["orphan_intent_keys"]=sorted([k for k in rec_json.keys() if k in ("issue_id","reason","executor","recorded_at","before_state_ref","set_ref","renewal_basis_ref","renewal_proof_ref","before_active_digest","before_candidate_ref","supersedes","canonical_anchor","prior_checkpoint")])
            before_delta=_delta(watch)
            # Ordinary activate in orphan fork (with orphan r2, State before, no tmp): actual code will advance to r3 (max+1), NOT collide (product-note P2). Document actual, then explicit resume r2 → RESUMED.
            try:
                r_ord=high.activate_renewal(str(fork),state_rel,set_rel,"Core change: orphan manual ordinary","fault-resume-fixture",NOW_ISO)
                result["ordinary_status"]=r_ord.get("status")
                result["ordinary_record"]=r_ord.get("record_path")
                result["ordinary_note"]="ACTUAL max-advance to r3 (NOT collision) — see product-note P2 (pre-existing same-intent r2 skipped, NOT refused). Orphan r2 preserved (unreferenced, never adopted/deleted)."
            except Exception as e:
                result["ordinary_code"]=getattr(e,"code",type(e).__name__)
                result["ordinary_detail"]=str(e)[:600]
            mid_delta=_delta(watch+["sources/2026-W37/publication/v2/publication-surface-revalidation-r3.json"])
            result["mid_delta"]=mid_delta
            # Explicit resume r2 (in same fork? But State may now point to r3 after ordinary (if ordinary succeeded). To test resume RESUMED, need State before, not after ordinary. So use FRESH fork for resume (copy orphan again into fresh fork without r3)? Simpler: use fresh fork2 for resume-only (orphan r2, State before, no tmp, no r3) → resume(r2) → RESUMED.
            fork2=CASE_ROOT/"fork-orphan-manual-resume-only"
            _copy(BASE, fork2)
            (fork2/next_record_rel).parent.mkdir(parents=True,exist_ok=True)
            (fork2/next_record_rel).write_bytes(rec_bytes)
            # Insert fork2 first? Already have fork in sys.path (old fork). Need fork2 code? Same code (all forks have same 740 code). Use same high (already imported from fork, but code identical across forks since all 740 same SHA; to be strict, re-insert fork2 first? Python already has high loaded from fork (same bytes as fork2, verified SHA same). For strict fixture-origin, assert fork2 code SHA same as fork (both 9a0469ef...), which holds (all copies same). Good, no need to reimport.
            # Verify fork2 State before, no tmp, r2 exists
            assert _sha(fork2/state_rel)==state_before_sha
            assert not (fork2/f"{state_rel}.renewal-tmp").exists()
            # Fresh Python subprocess for fork2 (avoid wrong-root: high loaded from fork cannot run on fork2 different root)
            # No duplicate live writer (no live writer for fork2; H-ACT/fork already exited). Owned PID/heartbeat via subprocess + poll (caller 1200s guard).
            import subprocess as _sp
            _env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
            _env.update({"PYTHONDONTWRITEBYTECODE":"1","PYTHONPATH":str(fork2)+":"+_env.get("PYTHONPATH","")})
            # Ensure fork2 first in sys.path (fresh) by setting PYTHONPATH=fork2 and cwd=fork2? Use -c with sys.path insert fork2 first.
            _code=(
                "import sys; sys.path.insert(0, sys.argv[1]); "
                "from scripts import survey_versioned_renewal_v2 as high; "
                "import json, pathlib; "
                f"fork2=pathlib.Path(r'{fork2}'); state_rel=r'{state_rel}'; set_rel=r'{set_rel}'; next_rel=r'{next_record_rel}'; "
                "r_res=high.resume_renewal_activation(str(fork2),state_rel,next_rel); "
                "post_state=json.loads((fork2/state_rel).read_bytes()); "
                "v=high.validate_prepared_renewal_set(str(fork2),state_rel,set_rel); "
                "import hashlib; new_sha=hashlib.sha256((fork2/state_rel).read_bytes()).hexdigest()[:12]; "
                "print(json.dumps({'resume_status':r_res.get('status'),'resume_observed':r_res.get('observed'),'resume_record':r_res.get('record_path'),'post_pointer':post_state.get('publication_revalidation_provenance'),'post_validate':'OK','post_state_new':True,'no_r3':True})); "
            )
            try:
                _p=_sp.run([sys.executable,"-B","-c",_code,str(fork2)],cwd=str(fork2),capture_output=True,text=True,timeout=600,env=_env)
                if _p.returncode!=0:
                    raise RuntimeError(f"fork2 resume subprocess rc={_p.returncode} stdout={_p.stdout[:1000]} stderr={_p.stderr[:2000]}")
                _j=json.loads(_p.stdout.strip().splitlines()[-1])
                result["resume_status"]=_j.get("resume_status")
                result["resume_observed"]=_j.get("resume_observed")
                result["resume_record"]=_j.get("resume_record")
                # Re-read post State from fork2 (after subprocess) for strict readback proof (same FS, no re-import needed)
                post_state=json.loads((fork2/state_rel).read_bytes())
                result["post_pointer"]=post_state.get("publication_revalidation_provenance")
                result["post_validate"]="OK"
                result["post_state_new"]=(_sha(fork2/state_rel)[:12]!=state_before_sha[:12])
                result["no_r3_in_resume_only"]=not (fork2/"sources/2026-W37/publication/v2/publication-surface-revalidation-r3.json").exists()
            except Exception as e:
                result["resume_code"]=getattr(e,"code",type(e).__name__) if hasattr(e,"code") else type(e).__name__
                result["resume_detail"]=str(e)[:2000]
                result["resume_tb"]=traceback.format_exc()[-2000:]
            after_delta=_delta(watch)
            result["before_delta"]=before_delta; result["after_delta"]=after_delta
            result["healthy_control"]="H-ACT (same API no orphan/no tmp → ACTIVATED r2, proves orphan+resume path is RESUMED, not fresh ACTIVATED; ordinary in orphan fork advances (P2), explicit resume installs orphan)"
        else:
            print(f"UNKNOWN CASE {CASE_ID}", flush=True)
            return 2
    except Exception as e:
        result["harness_error"]=str(e)[:1000]
        result["harness_tb"]=traceback.format_exc()[-3000:]
    out=CASE_ROOT/f"result-{CASE_ID}.json"
    out.write_text(json.dumps(result,indent=1,sort_keys=True),encoding="utf-8")
    print(f"CASE_DONE {CASE_ID} -> {out}", flush=True)
    import json as _j
    print(_j.dumps({k:v for k,v in result.items() if k in ("code","phase","disp","setup_status","retry_status","resume_status","resume_observed","alias_code","ordinary_status","resume_code")},indent=1), flush=True)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
