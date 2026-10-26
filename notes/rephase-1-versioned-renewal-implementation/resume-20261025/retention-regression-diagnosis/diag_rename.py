#!/usr/bin/env python3
"""Retention regression diagnosis — instrumented replica of failed midcapture test.

READ-ONLY product, no validator bypass. Replicates
test_replacement_owned_file_midcapture_refuses with hook counting,
target path, dev/ino before/after, immediate snapshots.
Runs in NEW independent TESTSRC (current740 or baseline721) via PYTHONPATH.
Saves JSON observation to stdout + file.
"""
import json
import os
import sys
import hashlib
from pathlib import Path
from unittest import mock
import unittest

# workspace is TESTSRC via PYTHONPATH
from scripts import survey_production_v2 as core
from scripts import survey_editorial_retention_v2 as retention
from tests import test_survey_editorial_retention_v2 as r2t
from tests import test_survey_editorial_correction_proposal_v2 as p1t

RetentionError = retention.RetentionError

def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _run_diag(out_path=None):
    tc = r2t.EditorialRetentionV2Tests(methodName='test_replacement_root_ancestor_file_refuses')
    tc.setUp()
    scratch, root = tc._fresh_weekly("jgas-p2r-repl3-diag-")
    helper = p1t._new_weekly_helper(tc, root)
    # _build_weekly_validated in current test file is p1t._build_weekly_validated(self, helper)
    # Inspect signature dynamically
    import inspect
    sig = inspect.signature(p1t._build_weekly_validated)
    print(f"P1T_BUILD_SIG={sig}", flush=True)
    try:
        built = p1t._build_weekly_validated(tc, helper)
    except TypeError:
        built = p1t._build_weekly_validated(helper)
    chain, state_path = built["chain"], built["state_path"]

    def _mut():
        authored = core.load_json(chain["authored_path"])
        authored["cover"]["headline"] = "Weekly repl3 test, revised edition"
        return authored

    proposal_id = "fixture-wk-rp-own"
    pp, _ = r2t._prepare_proposal_for(tc, root, helper, chain, state_path, proposal_id, _mut)
    ppath = root / (pp.relative_to(root) if isinstance(pp, Path) and pp.is_absolute() else pp)
    proposal = core.load_json(ppath)
    copy_paths = [r["path"] for r in proposal["retention_plan"] if r["policy"] == "COPY_BEFORE_REPLACEMENT"]
    assert copy_paths, "no COPY paths"
    proposal_dir = f"sources/{r2t.W_ISSUE}/publication/v2/editorial-corrections/{proposal_id}"
    victim_rel = proposal_dir + "/retained/before/" + copy_paths[0]
    victim = root / victim_rel

    # Victim does not exist yet before capture (retained root not claimed) — log proposal plan + copy dest
    obs = {}
    obs["proposal_id"] = proposal_id
    obs["copy_paths"] = copy_paths
    obs["victim_rel"] = victim_rel
    obs["victim_exists_before"] = victim.exists()
    # Log retention_plan rows for victim
    for r in proposal["retention_plan"]:
        if r["path"] == copy_paths[0]:
            obs["victim_plan_row"] = r
            break
    # Snapshot before (like test)
    before = r2t._snapshot(root)
    obs["before_head"] = before.get("head")
    obs["before_files_count"] = len(before.get("files", {}))

    # Instrument os.open
    orig_open = os.open
    calls = []
    swapped = {"done": False, "count": 0}
    swap_info = {}

    # Record victim parent + expected manifest name
    def _open_swap_manifest(name, *a, **k):
        fd = orig_open(name, *a, **k)
        try:
            sname = name if isinstance(name, str) else os.fsdecode(name)
        except Exception:
            sname = ""
        flags = a[0] if a else k.get("flags", 0)
        try:
            is_create = bool(flags & os.O_CREAT)
        except Exception:
            is_create = False
        # Log every CREATE of retention-manifest + every retention-manifest open
        if "retention-manifest" in sname:
            calls.append({"sname": sname, "flags": int(flags) if isinstance(flags, int) else str(flags), "is_create": is_create, "dir_fd": str(k.get("dir_fd")), "swapped_before": swapped["done"]})
        if sname == "retention-manifest.json" and is_create and not swapped["done"]:
            swapped["done"] = True
            swapped["count"] += 1
            # Victim should exist now (COPY writes complete, before manifest publish)
            try:
                lst_before = os.lstat(victim)
                swap_info["victim_before_dev"] = lst_before.st_dev
                swap_info["victim_before_ino"] = lst_before.st_ino
                swap_info["victim_before_size"] = lst_before.st_size
                swap_info["victim_before_sha"] = hashlib.sha256(victim.read_bytes()).hexdigest()
            except Exception as e:
                swap_info["victim_before_error"] = f"{type(e).__name__}: {e}"
            # Perform rename-based swap (guarantees new inode on ext4, unlike unlink+write reuse)
            try:
                data = victim.read_bytes()
                backup = victim.with_suffix(".bak-diag")
                # Ensure no leftover backup
                try:
                    backup.unlink()
                except FileNotFoundError:
                    pass
                victim.rename(backup)
                victim.write_bytes(data)
                lst_after = os.lstat(victim)
                swap_info["victim_after_dev"] = lst_after.st_dev
                swap_info["victim_after_ino"] = lst_after.st_ino
                swap_info["victim_after_size"] = lst_after.st_size
                swap_info["victim_after_sha"] = hashlib.sha256(victim.read_bytes()).hexdigest()
                swap_info["swap_ok"] = True
                swap_info["ino_changed"] = swap_info.get("victim_before_ino") != swap_info.get("victim_after_ino")
                swap_info["sha_same"] = swap_info.get("victim_before_sha") == swap_info.get("victim_after_sha")
            except Exception as e:
                swap_info["swap_ok"] = False
                swap_info["swap_error"] = f"{type(e).__name__}: {e}"
        return fd

    obs_before_victim = {}
    # Note: victim not yet exists, so before stat will fail — log it
    result = {}
    with mock.patch("os.open", side_effect=_open_swap_manifest):
        try:
            out = retention.capture_retention(root, state_path, pp)
            result["raised"] = False
            result["out"] = {"result": out.get("result"), "manifest_path": out.get("manifest_path")}
            # Immediate after: victim stat
            try:
                lst = os.lstat(victim)
                result["victim_after_dev"] = lst.st_dev
                result["victim_after_ino"] = lst.st_ino
                result["victim_after_sha"] = hashlib.sha256(victim.read_bytes()).hexdigest()
            except Exception as e:
                result["victim_after_error"] = f"{type(e).__name__}: {e}"
        except Exception as exc:
            result["raised"] = True
            result["code"] = getattr(exc, "code", type(exc).__name__)
            result["phase"] = getattr(exc, "phase", "")
            result["disposition"] = getattr(exc, "disposition", "")
            result["detail"] = str(getattr(exc, "detail", str(exc)))[:2000]
            # Immediate after failure: victim stat
            try:
                lst = os.lstat(victim)
                result["victim_after_dev"] = lst.st_dev
                result["victim_after_ino"] = lst.st_ino
                result["victim_after_sha"] = hashlib.sha256(victim.read_bytes()).hexdigest()
            except Exception as e:
                result["victim_after_error"] = f"{type(e).__name__}: {e}"

    obs["swapped_done"] = swapped["done"]
    obs["swapped_count"] = swapped["count"]
    obs["manifest_open_calls"] = calls
    obs["manifest_open_count"] = len(calls)
    obs["swap_info"] = swap_info
    obs["result"] = result
    # After snapshot (like test) — but keep fixture (do not cleanup scratch yet)
    after = r2t._snapshot(root)
    obs["after_head"] = after.get("head")
    obs["after_files_count"] = len(after.get("files", {}))
    # Check live drift vs before (excluding owned retained prefix)
    proposal_retained = proposal_dir + "/retained"
    live_drift = []
    for rel, sha in before["files"].items():
        if rel not in after["files"]:
            live_drift.append(f"loss:{rel}")
        elif after["files"][rel] != sha:
            # Allow victim drift? No — live originals must be unchanged; victim is owned retained, not in before
            live_drift.append(f"drift:{rel}")
    # Victim is new (owned), not in before, so not drift
    obs["live_drift_vs_before"] = live_drift[:20]
    added = sorted(set(after["files"]) - set(before["files"]))
    obs["added_count"] = len(added)
    obs["added_sample"] = added[:20]
    obs["added_outside_owned"] = [r for r in added if not r.startswith(proposal_retained)][:20]
    obs["scratch"] = str(scratch.name)
    obs["root"] = str(root)
    # Do NOT cleanup scratch — keep failed fixture per task
    # Prevent unittest cleanup from deleting: cancel cleanup
    # tc.addCleanup registered scratch.cleanup; we want to keep it, so clear?
    # Instead, keep path and note that cleanup will delete on process exit — so we copy path?
    # For diagnosis we keep fixture by not calling cleanup: remove cleanup via _cleanups?
    try:
        # unittest TestCase stores cleanups in _cleanups (list of (func, args, kwargs))
        # Remove scratch.cleanup to keep fixture
        tc._cleanups = [c for c in getattr(tc, "_cleanups", []) if getattr(c[0], "__self__", None) is not getattr(scratch, "cleanup", None)]
    except Exception:
        pass
    # Also prevent scratch destructor? Keep dir by creating a keep marker
    print(json.dumps(obs, indent=2))
    if out_path:
        out_path.write_text(json.dumps(obs, indent=2))
    return obs

if __name__ == "__main__":
    import pathlib
    op = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else None
    _run_diag(op)
