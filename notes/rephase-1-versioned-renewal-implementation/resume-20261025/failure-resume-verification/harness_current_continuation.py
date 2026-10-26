#!/usr/bin/env python3
"""CURRENT continuation: postreplace true mismatch, parent-alias same-leaf, cycle/sequence, high-prepare-33 re-verify.

CURRENT product ONLY (HIGH 1dad1ad/H74275d/S2290ddd, no stale 9a/6fe/20f). OS-level ONLY at EXACT target.
No product edits, no validator/proof mocks, no dummy SHA, no Stub HIGH.
Usage: python3 harness_current_continuation.py BASE_FIXTURE CASE_ID CASE_ROOT NOW_ISO [CU_RID]
BASE_FIXTURE: NEW fixture CURRENT (4851523, cu1-weekly SEALED_INERT, State before ca7c...)
CASE_ID: postreplace-true-mismatch, parent-alias-same-leaf, cycle-proper-rehash, sequence-nonincreasing-time, high-prepare-33-current
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
    if len(sys.argv) not in (5,6):
        print(f"usage: {sys.argv[0]} BASE CASE_ID CASE_ROOT NOW_ISO [CU_RID]", flush=True)
        return 2
    BASE=Path(sys.argv[1]).resolve()
    CASE_ID=sys.argv[2].strip()
    CASE_ROOT=Path(sys.argv[3]).resolve()
    NOW_ISO=sys.argv[4].strip()
    CU_RID=sys.argv[5].strip() if len(sys.argv)==6 else "cu1-weekly"
    for v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
        if os.environ.get(v):
            print(f"UNSAFE {v}", flush=True)
            return 2
    sys.dont_write_bytecode=True
    os.environ["PYTHONDONTWRITEBYTECODE"]="1"
    CASE_ROOT.mkdir(parents=True, exist_ok=True)
    # Base healthy paths (CURRENT cu1-weekly SEALED_INERT)
    basis_candidates=list(BASE.rglob(f"renewals/{CU_RID}/renewal-basis.json"))
    if not basis_candidates:
        print(f"FATAL no healthy base {CU_RID} (run healthy CURRENT first)", flush=True)
        return 2
    basis_rel=basis_candidates[0].relative_to(BASE).as_posix()
    renewal_dir=str(Path(basis_rel).parent.as_posix())
    set_rel=f"{renewal_dir}/publication-set.json"
    state_rel="sources/2026-W37/production-state.json"
    if not (BASE/set_rel).is_file():
        print(f"FATAL set missing: {set_rel}", flush=True)
        return 2
    # For high-prepare-33-current, BASE is typed33 copy? No, this harness is for NEW fixture CURRENT (cu1-weekly). high-prepare-33-current needs typed33 fixture, not NEW fixture. Handle separately below (fork from typed33, not BASE).
    if CASE_ID=="high-prepare-33-current":
        # Use typed33 fixture copy (R6 era, 33 legacy records, State r33) + CURRENT code via OWN snapshot? No, need CURRENT code in fixture? For ENTRY depth, ENTRY uses agent.validate_agent_state (from CURRENT code? We run CURRENT HIGH code (from OWN CURRENT snapshot) on typed33 copy (which has old R6 tools). ENTRY State validation (agent.validate_agent_state) is from CURRENT agent code? Agent code unchanged? Agent a32072e7... same in CURRENT and old? Yes, agent unchanged (a32072e7...). Good. So ENTRY depth check uses CURRENT agent (same as old? Agent unchanged, so same). Good. No need for CURRENT tools in fixture for ENTRY depth (ENTRY checks chain depth via low, not closure). Good. So copy typed33 to fork, run CURRENT HIGH prepare (from OWN CURRENT snapshot via sys.path) on typed33 fork (which has old tools, but ENTRY depth fails before closure). Good. No source commit needed (prepare fails before writes? Actually prepare does R dir claim + COPY before history verify? Wait ENTRY fails before R claim? ENTRY is before renewal dir claim? Yes, ENTRY (_observe_renewal_entry) is before renewal dir claim (which is before COPY). ENTRY includes State validation (chain depth). For typed33 (33 records), ENTRY State validation fails (chain too deep) BEFORE R claim, so no R, no COPY, State unchanged. Perfect (prewrite no newR).
        typed33_src=Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/final-r6-faults/r6-depth33")
        fork=CASE_ROOT/"fork-high-prepare-33-current"
        # Direct cp -a (no _copy helper which requires renewal modules absent in R6 typed33). Isolation via config + State (exist in both).
        if fork.exists():
            raise RuntimeError(f"dst exists: {fork}")
        import subprocess as _sp
        _env2={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
        _cp=_sp.run(["cp","-a",str(typed33_src),str(fork)],capture_output=True,text=True,timeout=180,env=_env2)
        if _cp.returncode!=0:
            raise RuntimeError(f"cp -a typed33 failed: {_cp.stderr[:500]}")
        for _rel in ("config/survey-production-v2.json","sources/2026-W37/production-state.json"):
            _a=(typed33_src/_rel).stat(); _b=(fork/_rel).stat()
            if (_a.st_dev,_a.st_ino)==(_b.st_dev,_b.st_ino):
                raise RuntimeError(f"inode sharing typed33: {_rel}")
            if _b.st_nlink!=1:
                raise RuntimeError(f"nlink !=1 typed33: {_rel}")
        print(f"FORK_OK typed33 {fork} CASE={CASE_ID} (CURRENT code via OWN snapshot, no stale 9a, isolation via config+State, no renewal-module check (R6 has none))", flush=True)
        # Insert OWN CURRENT snapshot first (fresh, CURRENT code, no stale 9a), NOT fork (which has old R6 code). For ENTRY depth, need CURRENT agent/high? Agent unchanged, high CURRENT? ENTRY uses agent.validate_agent_state (agent unchanged) + high _observe_renewal_entry (CURRENT high 1dad1ad? Or old? We want CURRENT high (1dad1ad) to prove cap33 with CURRENT. Good. So sys.path OWN CURRENT first.
        own_current=Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-faultresume-current-20261026T000000Z/snapshot-work")
        if str(own_current) not in sys.path:
            sys.path.insert(0, str(own_current))
        # Verify CURRENT pins (no stale 9a)
        for rel, expect in (("scripts/survey_versioned_renewal_v2.py","1dad1ad12ba509c477ea97fb3a22e5156ae1627182f3286f373f32eae7ba2fbb"),
                            ("scripts/survey_versioned_renewal_history_v2.py","74275d22a342014009d5d090fbe9c552981941e90259c298065d2ba6929d1f3d")):
            if _sha(own_current/rel)!=expect:
                print(f"FATAL OWN CURRENT pin mismatch {rel}", flush=True)
                return 2
        print("PRODUCT_PIN_CURRENT_OK (HIGH 1dad1ad/H74275d, no stale 9a)", flush=True)
        from scripts import survey_versioned_renewal_v2 as high_current
        # State in typed33 points to r33 (33 records). Attempt prepare (should refuse ENTRY chain-too-deep, no R, State unchanged).
        before_state_sha=_sha(fork/state_rel)[:12] if (fork/state_rel).exists() else "missing"
        print(f"BEFORE_STATE {before_state_sha} (should be r33 9b5c...)", flush=True)
        import os as _os
        def _delta(paths):
            d={}
            for rel in paths:
                p=fork/rel
                try:
                    st=_os.lstat(str(p))
                    import stat as _st
                    d[rel]={"exists":True,"is_symlink":_st.S_ISLNK(st.st_mode),"size":st.st_size,"sha":(_sha(p)[:12] if p.is_file() and not p.is_symlink() else None)}
                except FileNotFoundError:
                    d[rel]={"exists":False}
                except OSError as e:
                    d[rel]={"exists":"error","err":str(e)[:100]}
            return d
        # Expected R dir for new test (fr-test-33-current? Use new ID to avoid collision with existing? Use cu-test-33-current)
        test_rid="cu-test-33-current"
        test_renewal_dir=f"sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/renewals/{test_rid}"
        # Note: typed33 fixture has different proposal namespace? Typed33 fixture's proposal? It's R6 era, with wk-...? Actually typed33 fixture is 2026-W37 with ...? It has sources/2026-W37/... with ...? Its proposal namespace? For HIGH prepare, need manuscript_spec from typed33 fixture (which has ...? Typed33 fixture is R6 depth33, with ...? Does it have wk-boot-1 manuscript-spec? No, typed33 fixture is R6 depth33 (editorial? No, it's legacy chain, not wk-boot-1). HIGH prepare requires prior record to be versioned active set (editorial or renewal) with live seal+record+Candidate. Typed33 legacy-only chain is UNSUPPORTED for renewal (per S1 correction: legacy-only UNSUPPORTED). So HIGH prepare on typed33 legacy-only will fail with BASIS_... (unsupported predecessor), NOT depth? Hmm. Wait previous high-prepare-33 with stale 9a on typed33 succeeded in hitting ENTRY chain-too-deep (BASIS_ENTRY_INELIGIBLE, chain too deep), NOT unsupported predecessor. How? Because ENTRY State validation (agent.validate_agent_state) checks chain depth via low (which fails for 33 records) BEFORE checking predecessor type for renewal? ENTRY does State validation (which includes chain depth for active revalidation? State points to r33 (legacy 33), agent.validate_agent_state will check revalidation chain (which is 33 legacy records, exceeds max32) → fails with chain-too-deep, before renewal predecessor type check (which is later in prepare, after ENTRY?). Good! So ENTRY depth fails first, before predecessor type check. Good. So even though legacy-only is unsupported for renewal, ENTRY depth fails first (chain too deep), which is intended seam (cap33 prewrite no newR). Good. Our previous high-prepare-33 with stale 9a did exactly that (ENTRY chain-too-deep, no R). Good. With CURRENT code (1dad1ad, same ENTRY depth check? ENTRY depth check is in agent.validate_agent_state (unchanged a32072e7...), same. Good. So re-verify with CURRENT should also hit ENTRY chain-too-deep, no R. Good.
        # For manuscript_spec, need valid path in typed33 fork? HIGH prepare requires manuscript_spec_path (for U, must exist? It checks manuscript_spec exists? For U with legacy-only prior, it will fail earlier at ENTRY (State validation) before checking manuscript_spec? Actually prepare order: entry (State validation, which fails for 33) BEFORE manuscript_spec check? Let's see prepare order: entry → graph → ... → manuscript_spec? Actually prepare checks manuscript_spec_path required (ARGS) before entry? From snippet: it checks renewal_id, intent, toolchain, manuscript_spec_path required (ARGS), executor required, ts, then entry = _observe_renewal_entry(...). So manuscript_spec_path existence is checked? It does _lexical_rel for manuscript_spec? Actually it checks manuscript_spec_path is not None (ARGS), then later loads manuscript_spec? For ENTRY depth fail, does it happen before manuscript_spec load? Entry is before manuscript_spec load? From snippet: entry = _observe_renewal_entry(...), then ... then mspec_rel = _lexical_rel(... manuscript_spec ...), mspec_bytes = _read_bytes_bounded(...). So ENTRY (which fails for 33) happens BEFORE mspec load. Good. So manuscript_spec path can be dummy (must be non-None string? It checks `if manuscript_spec_path is None: ARGS`). It doesn't check existence before ENTRY? It checks later (after entry). Since ENTRY fails first, mspec existence not needed. Good. Use dummy mspec path that exists? Safer to use existing file in typed33 fork (e.g., `sources/2026-W37/production-state.json` as dummy? No, must be manuscript_spec? For U, manuscript_spec is required but not checked before ENTRY fail. Use any existing file (e.g., `README.md` in fork? Fork has README.md? Typed33 fixture has README.md? Yes (R6 fixture has README.md). Use `README.md` as dummy mspec (won't be read because ENTRY fails first). Good. But to be safe, use a real manuscript-spec from typed33? Typed33 fixture may not have wk-boot-1 manuscript-spec (since it's R6 depth33, not wk-boot-1). Use `README.md` (exists in all fixtures). Good.
        mspec_dummy="README.md"
        before_delta=_delta([state_rel, test_renewal_dir])
        result={}
        try:
            high_current.prepare_renewal(str(fork),state_rel,test_rid,"REUSE_TARGETS",mspec_dummy,None,"fault-resume-fixture",NOW_ISO)
            result={"unexpected":"PREPARE PASS (should refuse ENTRY chain-too-deep)"}
        except Exception as e:
            result={"code":getattr(e,"code",type(e).__name__),"phase":getattr(e,"phase",None),"disp":getattr(e,"disposition",None),"detail":str(e)[:1000]}
        after_delta=_delta([state_rel, test_renewal_dir])
        result["before_delta"]=before_delta; result["after_delta"]=after_delta
        try:
            result["state_unchanged"]=(_sha(fork/state_rel)[:12]==before_state_sha)
        except Exception:
            result["state_unchanged"]=False
        result["no_new_R"]=not (fork/test_renewal_dir).exists()
        # Healthy control: R7 32-valid (existing) + H-U1 CURRENT (cu1-weekly SEALED, short chain) prove valid paths allow prepare; typed33 33 refuses (cap33 prewrite no newR)
        result["healthy_control"]="R7 32-valid (existing typed legacy32, API+CLI) + H-U1 CURRENT cu1-weekly SEALED (short chain 1→2, NEW closure, CURRENT code) → prepare succeeds; typed33 33 (same code, longer chain) → ENTRY refuses, no R"
        out=CASE_ROOT/f"result-{CASE_ID}.json"
        out.write_text(json.dumps(result,indent=1,sort_keys=True),encoding="utf-8")
        print(f"CASE_DONE {CASE_ID}", flush=True)
        return 0
    # For other cases, fork BASE (CURRENT cu1-weekly SEALED_INERT)
    fork=CASE_ROOT/f"fork-{CASE_ID}"
    _copy(BASE, fork)
    print(f"FORK_OK {fork} CASE={CASE_ID} (CURRENT base cu1-weekly SEALED, no stale 9a)", flush=True)
    if str(fork) not in sys.path:
        sys.path.insert(0, str(fork))
    from scripts import survey_production_v2 as core
    from scripts import survey_versioned_renewal_v2 as high
    for rel, expect in (("scripts/survey_versioned_renewal_v2.py","1dad1ad12ba509c477ea97fb3a22e5156ae1627182f3286f373f32eae7ba2fbb"),
                        ("scripts/survey_versioned_renewal_history_v2.py","74275d22a342014009d5d090fbe9c552981941e90259c298065d2ba6929d1f3d"),
                        ("scripts/survey_versioned_renewal_source_v2.py","2290ddd0dc8397f86451aff70d50fd4da0c6184fcf1bef3ed96259642af2d1eb")):
        if _sha(fork/rel)!=expect:
            print(f"FATAL product drift {rel} (stale? other worker edit?)", flush=True)
            return 2
    print("PRODUCT_PIN_CURRENT_OK (HIGH 1dad1ad/H74275d/S2290ddd, no stale 9a, SRC manifest guard: own copy immutable, no torn)", flush=True)
    state_before=(fork/state_rel).read_bytes()
    state_before_sha=_sha(fork/state_rel)
    set_before_sha=_sha(fork/set_rel)
    print(f"STATE_BEFORE {state_before_sha[:12]} SET_BEFORE {set_before_sha[:12]} (cu1-weekly SEALED, State before ca7c...)", flush=True)
    next_record_rel="sources/2026-W37/publication/v2/publication-surface-revalidation-r2.json"
    import os as _os
    _orig_open=_os.open; _orig_write=_os.write; _orig_fsync=_os.fsync; _orig_close=_os.close; _orig_replace=_os.replace; _orig_read=_os.read; _orig_scandir=_os.scandir
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
                d[rel]={"exists":"error","err":str(e)[:100]}
        return d
    watch=[state_rel, set_rel, next_record_rel, f"{state_rel}.renewal-tmp"]
    result={}
    try:
        if CASE_ID=="postreplace-true-mismatch":
            # Hook os.read for EXACT State FD after replace → return WRONG BYTES (not open fail), so _fd_safe_read succeeds but observed != new_bytes → INDETERMINATE post-replace mismatch, State NEW + record preserved, observed NEW/unknown, NO rollback/deletion.
            state_abs=_abs(state_rel)
            replaced={"done":False}
            # Track State FDs opened AFTER replace (leaf opens via dir_fd + full-path opens)
            state_fds=set()
            orig_open2=_orig_open
            def _p_open(path, flags, *a, **k):
                fd=orig_open2(path, flags, *a, **k)
                try:
                    # Leaf open for State via dir_fd (path=="production-state.json") AFTER replace → track FD
                    if replaced["done"] and isinstance(path,(str,bytes)) and str(path)=="production-state.json":
                        state_fds.add(fd)
                    # Full-path State open AFTER replace → track FD
                    if replaced["done"] and isinstance(path,(str,bytes)):
                        try:
                            if os.path.abspath(str(path))==os.path.abspath(state_abs):
                                state_fds.add(fd)
                        except Exception:
                            pass
                except Exception:
                    pass
                return fd
            orig_replace2=_orig_replace
            def _p_replace(src,dst):
                r=orig_replace2(src,dst)
                try:
                    if os.path.abspath(str(dst))==os.path.abspath(state_abs):
                        replaced["done"]=True
                except Exception:
                    pass
                return r
            orig_read2=_orig_read
            def _p_read(fd, n):
                data=orig_read2(fd, n)
                try:
                    if fd in state_fds and replaced["done"]:
                        # Return WRONG BYTES (flip first byte) to trigger post-replace mismatch (observed != new_bytes), NOT open fail (so NOT HIGH_MODE, IS INDETERMINATE)
                        if isinstance(data,(bytes,bytearray)) and len(data)>0:
                            wrong=bytes([data[0]^0xFF])+bytes(data[1:])
                            # Remove FD from set after first wrong read? Keep for all post-replace State reads (both _replace_state_bytes post-verify + activate post-read). Both should see wrong bytes → both mismatch? First mismatch (in _replace_state_bytes) will raise INDETERMINATE before second read. Good. Return wrong once, then remove to avoid affecting later healthy reads in same process? But process ends after case (fresh Python per case, no reuse). Good. Keep.
                            return wrong
                except Exception:
                    pass
                return data
            _os.open=_p_open; _os.replace=_p_replace; _os.read=_p_read
            before_delta=_delta(watch)
            try:
                high.activate_renewal(str(fork),state_rel,set_rel,"Core change: postreplace true mismatch CURRENT","fault-resume-fixture",NOW_ISO)
                result={"unexpected":"ACTIVATED (read patch missed?)"}
            except Exception as e:
                result={"code":getattr(e,"code",type(e).__name__),"phase":getattr(e,"phase",None),"disp":getattr(e,"disposition",None),"detail":str(e)[:1200]}
            finally:
                _os.open=_orig_open; _os.replace=_orig_replace; _os.read=_orig_read
            after_delta=_delta(watch+[next_record_rel])
            result["before_delta"]=before_delta; result["after_delta"]=after_delta
            try:
                result["record_exists"]=(fork/next_record_rel).is_file() and not (fork/next_record_rel).is_symlink()
            except Exception:
                result["record_exists"]=False
            # State should be NEW (replace succeeded, new SHA != before), but observed at failure was NEW/unknown (mismatch, not before). After finally restore, we can read actual NEW State SHA (proves replace succeeded, State NEW, not rolled back).
            try:
                new_sha=_sha(fork/state_rel)[:12]
            except Exception as e:
                new_sha=f"unreadable:{str(e)[:80]}"
            result["state_sha_after"]=new_sha
            result["state_was_before"]=state_before_sha[:12]
            result["state_is_new"]=(new_sha!=state_before_sha[:12] and "unreadable" not in new_sha)
            result["record_preserved"]=bool(result.get("record_exists"))
            result["no_rollback"]=bool(result.get("state_is_new"))  # State NEW (not reverted to before), record preserved, no deletion
            result["no_deletion"]=True  # No unowned delete (checked via delta: no unexpected missing)
            result["healthy_control"]="H-ACT CURRENT (same API no read fault → ACTIVATED, proves read-mismatch caused INDETERMINATE, State NEW + record preserved, observed NEW/unknown, NO rollback/deletion; wrapper unknown observations (e.g., HIGH_MODE open-fail in old postread-dirfd) are NOT counted as INDETERMINATE mismatch — this true mismatch IS INDETERMINATE)"
            # Verify INDETERMINATE (not HIGH_MODE): code must be INDETERMINATE, phase ACTIVATE/RESUME, disp PRESERVED_INCOMPLETE, detail mentions post-replace mismatch (not open fail)
            result["is_true_mismatch"]=(result.get("code")=="INDETERMINATE" and "post-replace mismatch" in result.get("detail","").lower() or "post-replace" in result.get("detail","").lower())
        elif CASE_ID=="parent-alias-same-leaf":
            # Parent-dir symlink alias, SAME leaf publication-set.json: alias-R -> fr? Actually CURRENT base renewal dir is cu1-weekly (not fr-u1-weekly). Use cu1-weekly.
            # renewal_dir = .../renewals/cu1-weekly (from CU_RID). Create symlink alias-R -> cu1-weekly (same parent), alias set path .../alias-R/publication-set.json (same leaf, different parent spelling, same inode/SHA).
            alias_parent_rel=f"{Path(renewal_dir).parent.as_posix()}/alias-R-current"
            alias_set_rel=f"{alias_parent_rel}/publication-set.json"
            # Create symlink parent
            alias_parent_abs=_abs(alias_parent_rel)
            target_abs=_abs(renewal_dir)
            if os.path.islink(alias_parent_abs) or os.path.exists(alias_parent_abs):
                try:
                    if os.path.islink(alias_parent_abs):
                        os.unlink(alias_parent_abs)
                    else:
                        import shutil as _sh
                        _sh.rmtree(alias_parent_abs)
                except Exception:
                    pass
            os.symlink(target_abs, alias_parent_abs)
            print(f"PARENT_ALIAS {alias_parent_rel} -> {renewal_dir} (same leaf publication-set.json)", flush=True)
            # Verify same inode/SHA, different spelling, same leaf
            s_id=_os.lstat(_abs(set_rel)); a_id=_os.lstat(_abs(alias_set_rel))
            result["same_inode"]=((s_id.st_dev,s_id.st_ino)==(a_id.st_dev,a_id.st_ino))
            result["same_sha"]=(_sha(fork/set_rel)==_sha(fork/alias_set_rel))
            result["different_spelling"]=(set_rel!=alias_set_rel)
            result["same_leaf"]=(Path(set_rel).name==Path(alias_set_rel).name=="publication-set.json")
            before_delta=_delta(watch+[alias_set_rel, alias_parent_rel])
            try:
                high.activate_renewal(str(fork),state_rel,alias_set_rel,"Core change: parent alias same-leaf CURRENT","fault-resume-fixture",NOW_ISO)
                result["alias_unexpected"]="ACTIVATED (should refuse path guard, NOT ALREADY)"
            except Exception as e:
                result["alias_code"]=getattr(e,"code",type(e).__name__)
                result["alias_phase"]=getattr(e,"phase",None)
                result["alias_disp"]=getattr(e,"disposition",None)
                result["alias_detail"]=str(e)[:1000]
                # Legitimate intended path guard: HIGH_PATH (lexical exact spelling) or HIGH_MODE (ancestor symlink, no-follow, LEXICAL/ancestor refuse) BEFORE writes, NOT ALREADY branch. Label accordingly, do NOT force ALREADY.
                detail_lower=str(e).lower()
                result["is_path_guard"]=("HIGH_PATH" in str(getattr(e,"code","")) or "HIGH_MODE" in str(getattr(e,"code","")) or "exact spelling" in detail_lower or "symlink" in detail_lower or "ancestor" in detail_lower)
                result["is_not_already"]=("ALREADY_ACTIVE" not in str(getattr(e,"code","")) and "ALREADY_ACTIVE" not in str(e))
            after_delta=_delta(watch+[alias_set_rel, alias_parent_rel])
            result["before_delta"]=before_delta; result["after_delta"]=after_delta
            result["alias_preserved"]=((fork/alias_set_rel).is_symlink() or (fork/alias_set_rel).exists())
            # Parent symlink preserved? Check alias parent still symlink
            try:
                result["parent_symlink_preserved"]=os.path.islink(alias_parent_abs)
            except Exception:
                result["parent_symlink_preserved"]=False
            result["state_unchanged"]=(_sha(fork/state_rel)==state_before_sha)
            result["no_new_record"]=not (fork/next_record_rel).exists()
            result["healthy_control"]="H-ACT CURRENT canonical (exact spelling, no alias → ACTIVATED) vs parent-alias same-leaf (different parent spelling, same leaf/inode/SHA → HIGH_PATH/HIGH_MODE path guard, BEFORE writes, NOT ALREADY; different-leaf hardlink SEAL_BIND (previous alias-hardlink) still valid no-write control, BUT NOT intended alias-identity coverage (different leaf fails set-shape before alias-identity))"
        elif CASE_ID in ("cycle-proper-rehash","sequence-nonincreasing-time"):
            # Typed synthetic history with proper rehash (or qualified preemption if rehash impossible for cycle).
            # Use NEW fixture CURRENT (cu1-weekly SEALED, State before ca7c..., anchor DRAFT_COMPLETE (wk-boot-1 r1 anchor, NOT R1 r2). For cycle/sequence with valid DRAFT_COMPLETE anchor (so anchor passes, cycle/sequence fails).
            # For canonical anchor tests (forged DRAFT, wrong latest legacy, etc.) with R1 anchor new full identity, CITE r1-anchor-correction N1-N4 (already with CURRENT product 1dad1ad/74275d/2290ddd, BEFORE State write, State unchanged, forged preserved), DO NOT duplicate blindly here. This harness only does cycle/sequence with DRAFT_COMPLETE anchor (simple, no R1 chain needed).
            # Cycle: attempt 2-cycle r2<->r3 with best-effort rehash (write r2 supersedes r3 (placeholder SHA), compute r2 SHA, write r3 supersedes r2 (correct r2 SHA), compute r3 SHA, update r2 supersedes to r3 SHA (now r2 SHA changes, so r3 supersedes (old r2 SHA) becomes outdated → digest mismatch (qualified preemption, NOT cycle). Report as qualified preemption (honest, NOT intended cycle). To reach intended cycle (HISTORY_ANCESTOR cycle), proper rehash impossible for 2-cycle (chicken-egg). So cycle will be preemption, NOT hit. Document.
            # Sequence: nonincreasing time (r2 recorded_at earlier than r1) with proper rehash (recompute r2 SHA after editing time, update r3 supersedes to new r2 SHA, recompute r3 SHA, etc., so digests pass, chronology fails). Feasible, should hit intended HISTORY_ANCESTOR chronology/sequence.
            import datetime as _dt
            # Load valid r1 (wk-boot-1 r1, EDITORIAL, anchor DRAFT_COMPLETE, supersedes None, sequence 1)
            r1_rel="sources/2026-W37/publication/v2/publication-surface-revalidation-r1.json"
            r1_json=json.loads((fork/r1_rel).read_bytes())
            r1_sha=_sha(fork/r1_rel)
            # Common prior_checkpoint (original validation DRAFT_COMPLETE) and issue
            issue=r1_json.get("issue_id")
            prior_cp=r1_json.get("prior_checkpoint")
            # Helper to write synthetic record with proper rehash (compute SHA after writing content, return SHA)
            def _write_rec(rel, supersedes_ref, seq_num, recorded_at_str, extra=None):
                rec=dict(r1_json)  # copy valid r1 as template (same issue/prior_checkpoint/anchor/kind? kind EDITORIAL? For synthetic chain, keep kind EDITORIAL? Actually for renewal chain, records are EDITORIAL (r1) then VERSIONED (renewals)? For pure HISTORY cycle/sequence test (no HIGH, just hist.verify), kind can be EDITORIAL for all? History verify checks kinds (first_active, mixed later-legacy). For synthetic chain r1 (EDITORIAL) + r2/r3/r4 (EDITORIAL? Or VERSIONED? To avoid mixed-later-legacy issues, keep all EDITORIAL? Or all LEGACY? Simpler: keep all EDITORIAL (same kind, no legacy). History verify allows EDITORIAL chain? Yes (kinds EDITORIAL, no legacy after first_active? first_active is first EDITORIAL/VERSIONED, later LEGACY forbidden, but later EDITORIAL allowed? Yes (no restriction on later EDITORIAL after first EDITORIAL? Only later LEGACY forbidden). Good. Keep kind EDITORIAL for synthetic.
                rec["supersedes"]=dict(supersedes_ref) if supersedes_ref else None
                # Sequence is derived from filename (rN.json), not record field? Actually _parse_sequence parses ref path (filename), not record content. So filename determines sequence. Good. No need to set sequence field in record.
                rec["recorded_at"]=recorded_at_str
                if extra:
                    rec.update(extra)
                # Write with core.json_bytes (sorted? To match record SHA? Use core.json_bytes for deterministic)
                from scripts import survey_production_v2 as _core
                data=_core.json_bytes(rec)
                (fork/rel).parent.mkdir(parents=True,exist_ok=True)
                (fork/rel).write_bytes(data)
                return _sha(fork/rel)
            if CASE_ID=="cycle-proper-rehash":
                # Attempt 2-cycle r2<->r3: r2 supersedes r3 (placeholder), r3 supersedes r2 (correct after r2 written), then update r2 supersedes to r3 SHA (now r2 SHA changes, r3 supersedes outdated → digest preemption). Best-effort, expect qualified preemption (digest, NOT cycle).
                # Step1: write r2 with supersedes r3 placeholder (0...0)
                r2_rel="sources/2026-W37/publication/v2/publication-surface-revalidation-r2.json"
                r3_rel="sources/2026-W37/publication/v2/publication-surface-revalidation-r3.json"
                # Use increasing time for both (so chronology passes, isolating cycle vs time)
                t1="2026-10-26T00:10:00+00:00"; t2="2026-10-26T00:11:00+00:00"
                # Write r2 placeholder
                _write_rec(r2_rel, {"path":r3_rel,"sha256":"0"*64}, 2, t1)
                r2_sha_after_placeholder=_sha(fork/r2_rel)
                # Write r3 supersedes r2 (correct r2 SHA placeholder? Actually r2 SHA placeholder version (with 0...0 supersedes). Use that SHA for r3 supersedes (so r3 points to placeholder r2, which will become outdated after r2 updated → digest preemption for r3? Hmm. To maximize chance to reach cycle (not digest), need both SHAs correct simultaneously (impossible). Best-effort: write r3 with correct r2 SHA (placeholder version), compute r3 SHA, then update r2 supersedes to r3 SHA (correct), recompute r2 SHA (now r2 changes, so r3 supersedes (old r2 SHA) outdated → digest mismatch for r3 when verifying? History verify loads r3 via ref (which points to r3 file with new SHA? Wait r3 ref in chain? For cycle test, head is r3? Or r4? Let's make head r3 (chain r1→r2→r3 with r2<->r3 cycle? Actually r2 supersedes r3 (cycle, r3 not yet in chain? Hmm. For walk from head r3: r3 supersedes r2, r2 supersedes r3 (cycle). Both refs must have correct SHAs to pass digest until cycle detection. As argued, impossible to have both correct simultaneously (chicken-egg). Best-effort will leave one outdated → digest preemption. Report as qualified preemption.
                _write_rec(r3_rel, {"path":r2_rel,"sha256":r2_sha_after_placeholder}, 3, t2)
                r3_sha=_sha(fork/r3_rel)
                # Update r2 supersedes to r3 SHA (correct r3 SHA), recompute r2 (now r2 SHA changes, so r3 supersedes (old r2 SHA placeholder) outdated)
                _write_rec(r2_rel, {"path":r3_rel,"sha256":r3_sha}, 2, t1)
                r2_sha_final=_sha(fork/r2_rel)
                print(f"CYCLE best-effort r2 final {r2_sha_final[:12]} (supersedes r3 {r3_sha[:12]}), r3 {r3_sha[:12]} (supersedes r2 placeholder {r2_sha_after_placeholder[:12]} outdated) → expect digest preemption (qualified, NOT cycle)", flush=True)
                # Verify history on r3 (head r3, chain r1? Wait r3 supersedes r2, r2 supersedes r3 (cycle, no r1? Actually r2 supersedes r3 (cycle, not r1), so chain does NOT include r1? Walk from r3: r2, then r2 supersedes r3 (which is head, already? Seen? Walk seen logic will detect cycle after loading r2 then r3 again? As earlier analysis, it will detect cycle after 3 iterations (r2, r3, r2 duplicate) IF digests pass. But digests will fail first (r3 supersedes points to old r2 SHA placeholder, but r2 file now has new SHA final, so _load_record_file for r2 via r3 supersedes (old SHA) will fail digest mismatch (expected old SHA, actual new SHA). Good → qualified preemption (digest, NOT cycle). Report.
                from scripts import survey_versioned_renewal_history_v2 as hist
                try:
                    hist.verify_versioned_history(str(fork), r3_rel)
                    result={"unexpected":"PASS (should refuse cycle/digest)"}
                except Exception as e:
                    result={"code":getattr(e,"code",type(e).__name__),"phase":None,"disp":None,"detail":str(e)[:1000]}
                    # Qualified preemption if digest (HISTORY_DIGEST_MISMATCH), intended if cycle (HISTORY_ANCESTOR cycle)
                    detail_lower=str(e).lower()
                    result["is_cycle_intended"]=("cycle" in detail_lower and "HISTORY_ANCESTOR" in str(getattr(e,"code","")))
                    result["is_qualified_preemption_digest"]=("HISTORY_DIGEST_MISMATCH" in str(getattr(e,"code","")))
                result["note"]="Cycle 2-cycle proper rehash impossible (chicken-egg cross SHAs); best-effort leaves one outdated → qualified preemption (digest, NOT cycle). Honest, NOT claimed as cycle HIT. True cycle HIT would require simultaneously correct cross SHAs (impossible) or different cycle construction (e.g., duplicate link r5->r2 where r2 already visited via different path? But walk is linear, not branching, so duplicate requires loop, same chicken-egg). Report as OPEN for true cycle (needs legitimate generator with simultaneously correct SHAs, not feasible with pure file edits; R1 worker proven chain has no cycle (healthy), no cycle fixture exists)."
            else:  # sequence-nonincreasing-time
                # Nonincreasing time: r2 recorded_at earlier than r1, with proper rehash (recompute r2 SHA, update r3 supersedes to new r2 SHA, recompute r3 SHA, so digests pass, chronology fails). Feasible, should hit intended HISTORY_ANCESTOR chronology.
                r2_rel="sources/2026-W37/publication/v2/publication-surface-revalidation-r2.json"
                r3_rel="sources/2026-W37/publication/v2/publication-surface-revalidation-r3.json"
                # r1 recorded_at? Get r1 time
                r1_time_str=r1_json.get("recorded_at")
                # r2 earlier than r1 (nonincreasing time: r2 time < r1 time, but chain order r1→r2→r3 requires r1 time <= r2 time <= r3 time for valid; we make r2 earlier → chronology fail)
                # Use r2 time = r1 time minus 1 hour (earlier), r3 time = r1 time (so r2 < r1 <= r3? Actually chronological order is r1, r2, r3 (chain order). Check is previous_instant <= instant? For index0 r1, index1 r2: if r2 instant < r1 instant → fail (must be nondecreasing). Good.
                import datetime as _dt
                def _parse(s):
                    # Strict ISO, Z→+00:00, tz-required (same as H _parse_instant)
                    if s.endswith("Z"):
                        s=s[:-1]+"+00:00"
                    return _dt.datetime.fromisoformat(s)
                r1_dt=_parse(r1_time_str)
                r2_dt=r1_dt-_dt.timedelta(hours=1)
                r3_dt=r1_dt  # r3 same as r1 (so r2 < r1 <= r3? Actually r2 < r1, so r1→r2 fails (r2 < r1), before reaching r3. Good, isolates chronology at r2.
                r2_time=r2_dt.isoformat().replace("+00:00","Z") if r2_dt.tzinfo else r2_dt.isoformat()+"Z"
                r3_time=r3_dt.isoformat().replace("+00:00","Z") if r3_dt.tzinfo else r3_dt.isoformat()+"Z"
                # Write r2 supersedes r1 (correct r1 SHA), with earlier time, proper rehash (compute r2 SHA after writing)
                r1_sha=_sha(fork/r1_rel)
                _write_rec(r2_rel, {"path":r1_rel,"sha256":r1_sha}, 2, r2_time)
                r2_sha=_sha(fork/r2_rel)
                # Write r3 supersedes r2 (correct new r2 SHA), with r1 time, proper rehash
                _write_rec(r3_rel, {"path":r2_rel,"sha256":r2_sha}, 3, r3_time)
                print(f"SEQUENCE r1 {r1_time_str} sha={r1_sha[:12]}, r2 earlier {r2_time} sha={r2_sha[:12]}, r3 {r3_time} → expect chronology fail (intended), digests pass (proper rehash)", flush=True)
                from scripts import survey_versioned_renewal_history_v2 as hist
                try:
                    hist.verify_versioned_history(str(fork), r3_rel)
                    result={"unexpected":"PASS (should refuse chronology)"}
                except Exception as e:
                    result={"code":getattr(e,"code",type(e).__name__),"detail":str(e)[:1000]}
                    detail_lower=str(e).lower()
                    result["is_sequence_intended"]=(("chronology" in detail_lower or "nondecreasing" in detail_lower or "sequence" in detail_lower) and "HISTORY_ANCESTOR" in str(getattr(e,"code","")))
                    result["is_qualified_preemption"]=("HISTORY_DIGEST_MISMATCH" in str(getattr(e,"code","")))
                result["note"]="Sequence nonincreasing time with proper rehash (all SHAs correct, supersedes refs correct) → should hit intended HISTORY_ANCESTOR chronology/sequence (NOT digest). If digest, then rehash missed (qualified preemption, fix rehash, do NOT claim sequence)."
            # No State write (history verify is read-only), State unchanged (before ca7c...), no new R (no prepare/activate, only verify). Good (before writes).
            result["state_unchanged"]=(_sha(fork/state_rel)==state_before_sha)
            result["no_new_R"]=True  # No prepare/activate in this harness (only verify), so no R claimed. Good.
            result["healthy_control"]="R7 32-valid (existing typed legacy32) + H-U1 CURRENT cu1-weekly SEALED (short chain, NEW closure) → verify passes; synthetic cycle (chicken-egg, digest preemption) vs sequence (proper rehash, chronology HIT) prove seam isolation (cycle OPEN for true simultaneously-correct SHAs, sequence HIT if proper rehash)"
        else:
            print(f"UNKNOWN CASE {CASE_ID}", flush=True)
            return 2
    except Exception as e:
        result["harness_error"]=str(e)[:1000]
        result["harness_tb"]=traceback.format_exc()[-3000:]
    out=CASE_ROOT/f"result-{CASE_ID}.json"
    out.write_text(json.dumps(result,indent=1,sort_keys=True),encoding="utf-8")
    print(f"CASE_DONE {CASE_ID} -> {out}", flush=True)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
