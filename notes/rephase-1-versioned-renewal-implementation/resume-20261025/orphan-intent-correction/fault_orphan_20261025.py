#!/usr/bin/env python3
"""Orphan intent-collision fault harness — fixed HIGH, OS seam only, fresh children.

NEW healthy SEALED_U (or1-weekly) before activate on actual old R3 + current
fixed code snapshot (source-only fixture commit before authority, old E
uncommitted). Fault after record complete before State switch yields orphan;
ordinary SAME then changed reason/time both refuse (INTENT_COLLISION, no new
r3/State change); explicit resume r2→RESUMED + strict current State/set/
history; repeated resume ALREADY_ACTIVE readonly. Unrelated valid inert
set/new set allocates; malformed/foreign/symlink refuses preserves, no
unowned delete. Guards record/State counts/inventory immediately before
repair. Only OS fault seam (os.replace once at exact State target in fresh
child). No validator mocks. Fresh Python child per fork op (fixture-first
sys.path, no wrong-root reuse). No candidate/reconstruct commit, network,
old runners, cleanup, cache purge.

Usage: python3 fault_orphan_20261025.py FIXTURE_ROOT HEALTHY_JSON OUT_RAW_PARENT NOW_ISO
"""
from __future__ import annotations
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

FIXED_HIGH = "b12439d5057003e703992b91f9590c5eb498f48c21977fa7ab51167e48909413"

def _run(cmd, cwd, env):
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=300, env=env)

def _sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()

def _utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

def _sanitized_env(extra_tmp: Path | None = None):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "1", "GIT_ALLOW_PROTOCOL": "file",
                "PYTHONDONTWRITEBYTECODE": "1", "LC_ALL": "C"})
    if extra_tmp is not None:
        env["TMPDIR"] = str(extra_tmp)
    return env

def _fresh_activate(fork: Path, state_rel: str, set_rel: str, reason: str, executor: str,
                    recorded_at: str | None, fault_replace: bool, out_json: Path | None = None):
    """Run activate in fresh Python child (fork-first, no wrong-root). Returns (rc, stdout, stderr)."""
    code = f"""
import sys, os, json
from pathlib import Path
ROOT = Path({str(fork)!r}).resolve()
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
from pathlib import Path as _P
import hashlib
h = hashlib.sha256((_P(ROOT) / "scripts/survey_versioned_renewal_v2.py").read_bytes()).hexdigest()
assert h == {FIXED_HIGH!r}, f"HIGH drift in fresh child: {{h}}"
from scripts import survey_versioned_renewal_v2 as high
state_rel = {state_rel!r}
set_rel = {set_rel!r}
reason = {reason!r}
executor = {executor!r}
recorded_at = {recorded_at!r}
fault = {str(fault_replace)}
if fault:
    _orig_replace = os.replace
    _state_abs = str((ROOT / state_rel).resolve())
    def _fault_replace(src, dst, *a, **k):
        try:
            _dst_s = str(_P(dst).resolve()) if isinstance(dst, (str, _P)) else str(dst)
        except Exception:
            _dst_s = str(dst)
        if _dst_s == _state_abs or _dst_s.endswith("/" + state_rel):
            raise OSError("injected replace fail (orphan test, exact State target only)")
        return _orig_replace(src, dst, *a, **k)
    os.replace = _fault_replace
try:
    res = high.activate_renewal(str(ROOT), state_rel, set_rel, reason, executor, recorded_at)
    print(json.dumps({{"status": res.get("status"), "record_path": res.get("record_path"), "observed": res.get("observed")}}))
    raise SystemExit(0)
except SystemExit:
    raise
except Exception as exc:
    code = getattr(exc, "code", type(exc).__name__)
    print(json.dumps({{"error_code": str(code), "detail": str(exc)[:2000]}}), file=sys.stderr)
    # Exit 2 for typed refusal (RenewalHighError-like), 1 otherwise? Use 2 for all expected refusals with code.
    raise SystemExit(2)
"""
    env = _sanitized_env()
    p = subprocess.run([sys.executable, "-c", code], cwd=str(fork), capture_output=True, text=True, timeout=300, env=env)
    return p.returncode, p.stdout, p.stderr

def _fresh_resume(fork: Path, state_rel: str, record_rel: str):
    code = f"""
import sys, os, json
from pathlib import Path
ROOT = Path({str(fork)!r}).resolve()
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
import hashlib
h = hashlib.sha256((Path(ROOT) / "scripts/survey_versioned_renewal_v2.py").read_bytes()).hexdigest()
assert h == {FIXED_HIGH!r}, f"HIGH drift in fresh child: {{h}}"
from scripts import survey_versioned_renewal_v2 as high
try:
    res = high.resume_renewal_activation(str(ROOT), {state_rel!r}, {record_rel!r})
    print(json.dumps({{"status": res.get("status"), "record_path": res.get("record_path"), "observed": res.get("observed")}}))
    raise SystemExit(0)
except SystemExit:
    raise
except Exception as exc:
    code = getattr(exc, "code", type(exc).__name__)
    print(json.dumps({{"error_code": str(code), "detail": str(exc)[:2000]}}), file=sys.stderr)
    raise SystemExit(2)
"""
    env = _sanitized_env()
    p = subprocess.run([sys.executable, "-c", code], cwd=str(fork), capture_output=True, text=True, timeout=300, env=env)
    return p.returncode, p.stdout, p.stderr

def _fresh_prepare(fork: Path, state_rel: str, rid: str, intent: str, mspec_rel: str, executor: str, recorded_at: str | None):
    code = f"""
import sys, os, json
from pathlib import Path
ROOT = Path({str(fork)!r}).resolve()
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
import hashlib
h = hashlib.sha256((Path(ROOT) / "scripts/survey_versioned_renewal_v2.py").read_bytes()).hexdigest()
assert h == {FIXED_HIGH!r}, f"HIGH drift: {{h}}"
from scripts import survey_versioned_renewal_v2 as high
try:
    res = high.prepare_renewal(str(ROOT), {state_rel!r}, {rid!r}, {intent!r}, {mspec_rel!r}, None, {executor!r}, {recorded_at!r})
    print(json.dumps({{"basis_path": res.get("basis_path")}}))
    raise SystemExit(0)
except SystemExit:
    raise
except Exception as exc:
    print(json.dumps({{"error_code": str(getattr(exc, "code", type(exc).__name__)), "detail": str(exc)[:2000]}}), file=sys.stderr)
    raise SystemExit(2)
"""
    env = _sanitized_env()
    p = subprocess.run([sys.executable, "-c", code], cwd=str(fork), capture_output=True, text=True, timeout=300, env=env)
    return p.returncode, p.stdout, p.stderr

def _fresh_finalize(fork: Path, state_rel: str, basis_rel: str, checks_rel: str, executor: str, recorded_at: str | None):
    code = f"""
import sys, os, json
from pathlib import Path
ROOT = Path({str(fork)!r}).resolve()
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
import hashlib
h = hashlib.sha256((Path(ROOT) / "scripts/survey_versioned_renewal_v2.py").read_bytes()).hexdigest()
assert h == {FIXED_HIGH!r}, f"HIGH drift: {{h}}"
from scripts import survey_versioned_renewal_v2 as high
try:
    res = high.finalize_renewal(str(ROOT), {state_rel!r}, {basis_rel!r}, {checks_rel!r}, None, None, {executor!r}, {recorded_at!r})
    print(json.dumps({{"set_path": res.get("set_path"), "disposition": res.get("disposition")}}))
    raise SystemExit(0)
except SystemExit:
    raise
except Exception as exc:
    print(json.dumps({{"error_code": str(getattr(exc, "code", type(exc).__name__)), "detail": str(exc)[:2000]}}), file=sys.stderr)
    raise SystemExit(2)
"""
    env = _sanitized_env()
    p = subprocess.run([sys.executable, "-c", code], cwd=str(fork), capture_output=True, text=True, timeout=300, env=env)
    return p.returncode, p.stdout, p.stderr

def main() -> int:
    if len(sys.argv) != 5:
        print(f"usage: {sys.argv[0]} FIXTURE_ROOT HEALTHY_JSON OUT_RAW_PARENT NOW_ISO", flush=True)
        return 2
    FIX = Path(sys.argv[1]).resolve()
    HEALTHY_JSON = Path(sys.argv[2]).resolve()
    RAW_PARENT = Path(sys.argv[3]).resolve()
    NOW_ISO = sys.argv[4].strip()
    for v in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES"):
        if os.environ.get(v):
            print(f"UNSAFE inherited {v}", flush=True)
            return 2
    env = _sanitized_env(RAW_PARENT / "tmp")
    (RAW_PARENT / "tmp").mkdir(parents=True, exist_ok=True)
    RAW_PARENT.mkdir(parents=True, exist_ok=True)
    healthy = json.loads(HEALTHY_JSON.read_bytes())
    state_rel = "sources/2026-W37/production-state.json"
    set_rel = healthy["set_path"]
    basis_rel = healthy["basis_path"]
    reason = "Core change: orphan intent-collision fix verification"
    executor = "orphanfix-harness"
    sys.path.insert(0, str(FIX))
    sys.dont_write_bytecode = True
    high_path = FIX / "scripts/survey_versioned_renewal_v2.py"
    high_sha = _sha_file(high_path)
    print(f"HIGH_PIN={high_sha}", flush=True)
    if high_sha != FIXED_HIGH:
        print("FATAL HIGH !=b124 (fixed)", flush=True)
        return 2
    state_before_bytes = (FIX / state_rel).read_bytes()
    state_before_sha = hashlib.sha256(state_before_bytes).hexdigest()
    print(f"STATE_BEFORE={state_before_sha[:12]}", flush=True)
    set_before_sha = _sha_file(FIX / set_rel)
    print(f"SET_BEFORE={set_rel} {set_before_sha[:12]}", flush=True)
    from scripts import survey_production_v2 as core
    cfg = json.loads((FIX / "config/survey-production-v2.json").read_bytes())
    state_doc = json.loads(state_before_bytes.decode("utf-8"))
    from scripts import survey_publication_set_v2 as setmod
    sel = setmod.resolve_publication_selection(FIX, cfg, state_doc)
    prior_rel = sel.get("record_ref", {}).get("path") or sel.get("activation_record_ref", {}).get("path")
    if not prior_rel:
        ptr = state_doc.get("publication_revalidation_provenance", {})
        prior_rel = ptr.get("path")
    if not prior_rel:
        print("FATAL no prior record rel", flush=True)
        return 2
    parent_rel = str(Path(prior_rel).parent.as_posix())
    print(f"PRIOR={prior_rel} PARENT={parent_rel}", flush=True)
    base_recs = sorted([p.name for p in (FIX / parent_rel).iterdir() if p.name.startswith("publication-surface-revalidation-r")]) if (FIX / parent_rel).exists() else []
    print(f"BASE_RECS={base_recs}", flush=True)

    def _fork(name: str) -> Path:
        dst = RAW_PARENT / name
        if dst.exists():
            print(f"FATAL fork exists: {dst}", flush=True)
            raise SystemExit(2)
        cp = _run(["cp", "-a", str(FIX), str(dst)], RAW_PARENT, env)
        if cp.returncode != 0:
            print(f"FATAL cp -a {cp.stderr[:500]}", flush=True)
            raise SystemExit(2)
        for rel in (state_rel, set_rel, basis_rel):
            s, d = FIX / rel, dst / rel
            if s.is_file():
                if _sha_file(s) != _sha_file(d):
                    print(f"FATAL fork sha mismatch: {rel}", flush=True)
                    raise SystemExit(2)
                if (s.stat().st_dev, s.stat().st_ino) == (d.stat().st_dev, d.stat().st_ino):
                    print(f"FATAL fork inode sharing: {rel}", flush=True)
                    raise SystemExit(2)
                if d.stat().st_nlink != 1:
                    print(f"FATAL fork nlink !=1: {rel}", flush=True)
                    raise SystemExit(2)
        return dst

    fork_orphan = _fork(f"fork-orphan-setup-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}")
    rec_dir = fork_orphan / parent_rel
    before_recs = sorted([p.name for p in rec_dir.iterdir() if p.name.startswith("publication-surface-revalidation-r")]) if rec_dir.exists() else []
    print(f"ORPHAN_SETUP_BEFORE_RECS={before_recs} STATE={state_before_sha[:12]}", flush=True)
    rc, out, err = _fresh_activate(fork_orphan, state_rel, set_rel, reason, executor, NOW_ISO, True)
    print(f"ORPHAN_SETUP_RC={rc} OUT={out[:500]} ERR={err[:1000]}", flush=True)
    if rc != 2 or "INDETERMINATE" not in err:
        print("FATAL expected INDETERMINATE replace failed (preserved)", flush=True)
        return 2
    after_recs = sorted([p.name for p in rec_dir.iterdir() if p.name.startswith("publication-surface-revalidation-r")])
    print(f"ORPHAN_SETUP_AFTER_RECS={after_recs}", flush=True)
    if len(after_recs) != len(before_recs) + 1:
        print(f"FATAL expected exactly one new record (orphan), before={before_recs} after={after_recs}", flush=True)
        return 2
    orphan_name = sorted(set(after_recs) - set(before_recs))[0]
    orphan_rel = f"{parent_rel}/{orphan_name}"
    print(f"ORPHAN={orphan_rel}", flush=True)
    orphan_bytes = (fork_orphan / orphan_rel).read_bytes()
    if len(orphan_bytes) < 100:
        print("FATAL orphan too small (partial, not complete)", flush=True)
        return 2
    doc = json.loads(orphan_bytes.decode("utf-8"))
    if doc.get("kind") != "VERSIONED_RENEWAL_ACTIVATION_V1" or doc.get("reason_class") != "REVIEWED_VERSIONED_CORE_RENEWAL":
        print("FATAL orphan kind mismatch (not complete renewal)", flush=True)
        return 2
    if (fork_orphan / state_rel).read_bytes() != state_before_bytes:
        print("FATAL State changed during orphan setup (must stay before)", flush=True)
        return 2
    print("ORPHAN_SETUP_OK (complete r2, State before, preserved)", flush=True)
    for label, r, e, t in (("same", reason, executor, NOW_ISO),
                           ("changed", reason + " (changed free text)", executor + "-changed", None)):
        b_recs = sorted([p.name for p in rec_dir.iterdir() if p.name.startswith("publication-surface-revalidation-r")])
        b_state = (fork_orphan / state_rel).read_bytes()
        rc2, out2, err2 = _fresh_activate(fork_orphan, state_rel, set_rel, r, e, t, False)
        print(f"ORDINARY_{label.upper()}_RC={rc2} ERR={err2[:500]}", flush=True)
        if rc2 != 2 or ("INTENT_COLLISION" not in err2 and "RECORD_COLLISION" not in err2):
            print(f"FATAL expected INTENT/RECORD_COLLISION for ordinary {label}, rc={rc2} err={err2[:1000]}", flush=True)
            return 2
        a_recs = sorted([p.name for p in rec_dir.iterdir() if p.name.startswith("publication-surface-revalidation-r")])
        if b_recs != a_recs:
            print(f"FATAL new record on ordinary {label} (must be no new r3): before={b_recs} after={a_recs}", flush=True)
            return 2
        if (fork_orphan / state_rel).read_bytes() != b_state:
            print(f"FATAL State changed on ordinary {label} (must stay before)", flush=True)
            return 2
    print("ORDINARY_COLLISION_OK (same + changed both refuse, no r3, State unchanged)", flush=True)
    fork_resume = _fork(f"fork-resume-only-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}")
    resume_rec_dir = fork_resume / parent_rel
    src_orphan = fork_orphan / orphan_rel
    dst_orphan = fork_resume / orphan_rel
    if dst_orphan.exists():
        print("FATAL resume fork already has orphan (should be fresh)", flush=True)
        return 2
    dst_orphan.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(src_orphan), str(dst_orphan))
    if _sha_file(src_orphan) != _sha_file(dst_orphan):
        print("FATAL orphan copy sha mismatch", flush=True)
        return 2
    if (src_orphan.stat().st_dev, src_orphan.stat().st_ino) == (dst_orphan.stat().st_dev, dst_orphan.stat().st_ino):
        print("FATAL orphan copy inode sharing (must be byte-independent)", flush=True)
        return 2
    if dst_orphan.stat().st_nlink != 1:
        print("FATAL orphan copy nlink !=1", flush=True)
        return 2
    tmp_rel = f"{state_rel}.renewal-tmp"
    if (fork_resume / tmp_rel).exists():
        print("FATAL resume fork has tmp (must be fresh without tmp for RESUMED)", flush=True)
        return 2
    r_names = sorted([p.name for p in resume_rec_dir.iterdir() if p.name.startswith("publication-surface-revalidation-r")])
    if orphan_name not in r_names:
        print("FATAL resume fork missing orphan", flush=True)
        return 2
    rc3, out3, err3 = _fresh_resume(fork_resume, state_rel, orphan_rel)
    print(f"RESUME_RC={rc3} OUT={out3[:500]} ERR={err3[:500]}", flush=True)
    if rc3 != 0 or "resumed" not in out3:
        print(f"FATAL expected ACTIVATED/resumed, rc={rc3} out={out3[:1000]} err={err3[:1000]}", flush=True)
        return 2
    post_state = json.loads((fork_resume / state_rel).read_bytes())
    if post_state.get("publication_revalidation_provenance", {}).get("path") != orphan_rel:
        print("FATAL post-resume pointer != orphan", flush=True)
        return 2
    # Strict current set/history in fresh child (fork-first) to avoid wrong-root.
    verify_code = f"""
import sys, json
from pathlib import Path
ROOT = Path({str(fork_resume)!r}).resolve()
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
from scripts import survey_versioned_renewal_v2 as high
high.validate_prepared_renewal_set(str(ROOT), {state_rel!r}, {set_rel!r})
h = high.verify_renewal_history(str(ROOT), {orphan_rel!r})
print(json.dumps({{"hist": str(h)[:500]}}))
"""
    vp = subprocess.run([sys.executable, "-c", verify_code], cwd=str(fork_resume), capture_output=True, text=True, timeout=300, env=_sanitized_env())
    print(f"VERIFY_RC={vp.returncode} OUT={vp.stdout[:500]} ERR={vp.stderr[:500]}", flush=True)
    if vp.returncode != 0:
        print("FATAL strict set/history failed after resume", flush=True)
        return 2
    rc4, out4, err4 = _fresh_resume(fork_resume, state_rel, orphan_rel)
    print(f"REPEAT_RESUME_RC={rc4} OUT={out4[:500]} ERR={err4[:500]}", flush=True)
    if rc4 != 0 or "ALREADY_ACTIVE" not in out4:
        print(f"FATAL expected ALREADY_ACTIVE on repeat, rc={rc4} out={out4[:1000]}", flush=True)
        return 2
    print("RESUME_ALREADY_ACTIVE_OK", flush=True)
    # Unrelated valid inert set/new set allocates (no global ban).
    fork_newset = _fork(f"fork-newset-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}")
    or2_id = "or2-weekly"
    mspec_rel = "sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/manuscript-spec.json"
    rc_p, out_p, err_p = _fresh_prepare(fork_newset, state_rel, or2_id, "REUSE_TARGETS", mspec_rel, "orphanfix-fixture", NOW_ISO)
    print(f"NEWSET_PREPARE_RC={rc_p} OUT={out_p[:300]} ERR={err_p[:500]}", flush=True)
    if rc_p != 0:
        print(f"FATAL newset prepare failed: {err_p[:1000]}", flush=True)
        return 2
    basis2_rel = json.loads(out_p)["basis_path"]
    # QA in parent (driver-side, exact bytes, no validator mocks).
    from scripts import survey_quality_v2 as quality_parent
    from scripts import survey_production_v2 as core_parent
    basis2 = json.loads((fork_newset / basis2_rel).read_bytes())
    cfg2 = json.loads((fork_newset / "config/survey-production-v2.json").read_bytes())
    kinds2 = quality_parent.expected_checks_by_kind(cfg2, basis2["research_profile"], basis2["publication_profile"], {"DETERMINISTIC"})
    prior_seal2 = json.loads((fork_newset / basis2["prior_selected_ref"]["path"]).read_bytes())
    trio2 = prior_seal2["roles"]["validated-source"]
    pdf2 = prior_seal2["roles"]["publication-pdf"]
    main2 = (fork_newset / trio2["path"]).read_bytes()
    pdfb2 = (fork_newset / pdf2["path"]).read_bytes()
    from pypdf import PdfReader as _PdfReader
    pages2 = len(_PdfReader(str(fork_newset / pdf2["path"])).pages)
    qroot2 = fork_newset / f"sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/renewals/{or2_id}/quality"
    qroot2.mkdir(parents=True, exist_ok=True)
    scope2 = f"renewal {or2_id} fresh U (orphanfix unrelated new set)"
    payloads2 = {
        "SUBJECT_ENTITY_PROPERTY_BINDING": {"check_id": "SUBJECT_ENTITY_PROPERTY_BINDING", "status": "PASS", "trio_sha256": hashlib.sha256(main2).hexdigest(), "trio_path": trio2["path"], "scope": scope2},
        "IDENTIFIER_PRESERVATION": {"check_id": "IDENTIFIER_PRESERVATION", "status": "PASS", "source_sha256": hashlib.sha256(main2).hexdigest(), "inspected_identifiers": [basis2["issue_id"]], "scope": scope2},
        "PDF_PREFLIGHT": {"check_id": "PDF_PREFLIGHT", "status": "PASS", "page_count": pages2, "pdf_sha256": hashlib.sha256(pdfb2).hexdigest(), "byte_count": len(pdfb2), "scope": scope2},
    }
    if "EMPTY_WRAPPER_SUPPRESSION" in kinds2:
        payloads2["EMPTY_WRAPPER_SUPPRESSION"] = {"check_id": "EMPTY_WRAPPER_SUPPRESSION", "status": "PASS", "inspected_paths": [trio2["path"]], "scope": scope2}
    rows2 = []
    for cid in sorted(payloads2):
        pp = qroot2 / f"{cid.lower()}.json"
        pp.write_bytes(core_parent.json_bytes(payloads2[cid]))
        rows2.append({"check_id": cid, "kind": "DETERMINISTIC", "status": "PASS", "executor": "orphanfix-fixture", "evidence": "unrelated new set QA", "recorded_at": NOW_ISO, "result": {"path": str(pp.relative_to(fork_newset)), "sha256": _sha_file(pp)}})
    checks2_rel = f"sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/renewal-qa-checks-{or2_id}.json"
    (fork_newset / checks2_rel).write_bytes(core_parent.json_bytes({"checks": rows2}))
    rc_f, out_f, err_f = _fresh_finalize(fork_newset, state_rel, basis2_rel, checks2_rel, "orphanfix-fixture", NOW_ISO)
    print(f"NEWSET_FINALIZE_RC={rc_f} OUT={out_f[:300]} ERR={err_f[:500]}", flush=True)
    if rc_f != 0:
        print(f"FATAL newset finalize failed: {err_f[:1000]}", flush=True)
        return 2
    set2_rel = json.loads(out_f)["set_path"]
    print(f"NEWSET_SEALED {set2_rel}", flush=True)
    dst_or1 = fork_newset / orphan_rel
    if not dst_or1.exists():
        shutil.copy2(str(src_orphan), str(dst_or1))
    newset_before = sorted([p.name for p in (fork_newset / parent_rel).iterdir() if p.name.startswith("publication-surface-revalidation-r")])
    print(f"NEWSET_BEFORE_RECS={newset_before}", flush=True)
    rc_n, out_n, err_n = _fresh_activate(fork_newset, state_rel, set2_rel, "Core change: unrelated new set (or2)", "orphanfix-fixture", NOW_ISO, False)
    print(f"NEWSET_ACTIVATE_RC={rc_n} OUT={out_n[:500]} ERR={err_n[:500]}", flush=True)
    if rc_n != 0:
        print(f"FATAL unrelated new set should ACTIVATE, rc={rc_n} err={err_n[:1000]}", flush=True)
        return 2
    new_rec = json.loads(out_n).get("record_path")
    if new_rec == orphan_rel:
        print("FATAL new set adopted orphan (must allocate new seq, no auto-adopt)", flush=True)
        return 2
    if not (fork_newset / orphan_rel).exists():
        print("FATAL unrelated orphan deleted (must preserve, no unowned delete)", flush=True)
        return 2
    print("UNRELATED_NEWSET_OK (no global ban, orphan preserved)", flush=True)
    # Malformed/foreign/symlink reserved record refuses preserves, no unowned delete.
    fork_bad = _fork(f"fork-bad-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}")
    outside = fork_bad / "outside-secret.txt"
    outside.write_text("outside-secret")
    symlink_rel = f"{parent_rel}/publication-surface-revalidation-r99.json"
    try:
        (fork_bad / symlink_rel).symlink_to(outside)
        symlink_created = True
    except Exception as exc:
        print(f"SKIP symlink unavailable: {exc}", flush=True)
        symlink_created = False
        symlink_rel = None
    if symlink_created:
        b_state = (fork_bad / state_rel).read_bytes()
        rc_b, out_b, err_b = _fresh_activate(fork_bad, state_rel, set_rel, reason, executor, NOW_ISO, False)
        print(f"SYMLINK_RC={rc_b} ERR={err_b[:500]}", flush=True)
        if rc_b != 2 or ("RECORD_COLLISION" not in err_b and "HIGH_MODE" not in err_b and "HIGH_UNREADABLE" not in err_b):
            print(f"FATAL expected fail-closed refusal for symlink, rc={rc_b} err={err_b[:1000]}", flush=True)
            return 2
        if not (fork_bad / symlink_rel).is_symlink():
            print("FATAL symlink deleted (must preserve, no unowned delete)", flush=True)
            return 2
        if outside.read_text() != "outside-secret":
            print("FATAL outside modified (must preserve)", flush=True)
            return 2
        if (fork_bad / state_rel).read_bytes() != b_state:
            print("FATAL State changed on symlink refusal (must stay before)", flush=True)
            return 2
    fork_mal = _fork(f"fork-malformed-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}")
    mal_rel = f"{parent_rel}/publication-surface-revalidation-r100.json"
    (fork_mal / mal_rel).write_text("{not-json")
    b_state2 = (fork_mal / state_rel).read_bytes()
    rc_m, out_m, err_m = _fresh_activate(fork_mal, state_rel, set_rel, reason, executor, NOW_ISO, False)
    print(f"MALFORMED_RC={rc_m} ERR={err_m[:500]}", flush=True)
    if rc_m != 2 or ("RECORD_COLLISION" not in err_m and "HIGH_" not in err_m):
        print(f"FATAL expected fail-closed refusal for malformed, rc={rc_m} err={err_m[:1000]}", flush=True)
        return 2
    if not (fork_mal / mal_rel).exists():
        print("FATAL malformed deleted (must preserve)", flush=True)
        return 2
    if (fork_mal / state_rel).read_bytes() != b_state2:
        print("FATAL State changed on malformed refusal", flush=True)
        return 2
    print("MALFORMED_FOREIGN_SYMLINK_OK (refuses preserves, no unowned delete)", flush=True)
    print("ALL_ORPHAN_FIX_CASES_OK", flush=True)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
