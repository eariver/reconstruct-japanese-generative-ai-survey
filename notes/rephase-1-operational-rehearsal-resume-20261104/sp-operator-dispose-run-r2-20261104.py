#!/usr/bin/env python3
"""SP dispose + normal-run one-use wrapper r2 — SOURCE REVIEW ONLY, DO NOT EXECUTE YET.

Single bounded operation: guarded removal of the two exact unaccepted CAND-owned
files (Ledger, then Completeness) + ONE ordinary normal Evidence retry via the
existing public run API. Supersedes rejected v1 (preserved untouched, never
executed): fixes ctx screening-path KeyError, audit archive-path semantics,
retention containment, return-gate rechecks, umask-recorded output modes,
pre-unlink backup re-verification, and removes dead/duplicate helpers.

Reuses pinned r6 helpers (r6 tool hash verified before import): stdlib pinning,
strict State + DM022 readiness, complete-tree compare, intended-source preflight.
No new auth framework, no duplicated validators, no new shipping API/module/
schema, no State advance. The retry is exactly one rn.run() call, which owns
the strict facade per phase itself (no outer facade, no checkpoint calls,
no run copy, no verified-dict bypass).

Phase table (STOP + preserve + no auto restore/retry on first failure):
 P0 invocation pinning: manifest/READY/r6-tool bytes == externally recorded
    hashes; umask recorded (round-trip, restored); manifest clean; READY is a
    prepare-only record binding the expected manifest. No active writes.
 P1 full pre-disposal verification (reads only): live HEAD == READY live impl;
    strict State + DM022; full SP tree == baseline 552 + READY exact 19 new
    (571 live); all771 intended with recorded per-file modes + triangulated
    test pin; all30 Raw + staged input/supplement pins; FULL supplement normal
    validation (existing API, Raw-present, facade); retained package basis
    validation (existing API, facade); gates/CP/checkpoints/accepted pins;
    r4 DATA pinned by manifest hash before use. Zero active writes on failure.
 P2 exclusive NEW retention (validated to sit DIRECTLY under the resume packet,
    never under active or elsewhere) + backups of both files (O_EXCL|O_NOFOLLOW,
    chmod 0o664, readback). retention-manifest binds old/new path, SHA, bytes,
    mode, live-verified 64-char State SHA, UTC. No rename onto backup names.
 P3 ledger gate: strict State + DM022 + full tree == 571 set + all771 + same
    manifest/READY hashes + BOTH retained backups re-verified (bytes/mode/sha)
    + ledger AND completeness present-pinned. Unlink ledger ONLY; verify absent
    + not-symlink; re-verify retained ledger copy. Single-operator snapshot
    checks, no CAS/atomicity claim.
 P4 completeness gate: strict State + DM022 + full tree == 570 set (ledger
    absent EXPECTED + verified absent, completeness present-pinned, rest exact)
    + all771 + same hashes + backups re-verified. Unlink completeness ONLY;
    verify both absent (569 set); re-verify retained completeness copy.
 P5 post-disposal verify: tree == 569 set; old accepted dirs byte-identical;
    gates absent; State bytes unchanged (still CAND).
 P6 ONE ordinary normal retry: rn.run(repo, state, input, supp) with the real
    staged paths. Captures result dict to stdout (launcher records exit/code).
    On failure after removal or partial run: preserve exact partial state,
    report, no retry.
 P7 post-run verify: State bytes unchanged (still CAND); exact active delta
    (only exact2 regenerated + 2 NEW accepted dirs, 5 + 322 files); produced
    input/output references exact (archived input == NEW accepted archive path
    with staged bytes; package authority == staged supplement); declared counts
    from actual files (160 results / 165 discovery rows / 15 obligations);
    overall_status == staged input closure status.
 P8 return gate: manifest + READY + staged input/supplement + new ledger/
    completeness pins re-verified (same captured values, not reseal); then
    DISPOSE_RUN record with full hashes. No semantic approval is produced.
"""
from __future__ import annotations
import argparse
import datetime
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path

if os.environ.get("PYTHONDONTWRITEBYTECODE") != "1":
    raise SystemExit("REFUSE: PYTHONDONTWRITEBYTECODE=1 required")

REPO_ROOT = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work")
WSROOT = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
RESUME = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-operational-rehearsal-resume-20261104")
SRC_REL = Path("sources/SP-efficient-llm-2026")
ISSUE = "SP-efficient-llm-2026"
HIST_IMPL = "480823560c0c26ed2e5baa18e0e79a22b2839a27"
R6_TOOL = RESUME / "sp-operator-prepare-r6-20261104.py"
R6_TOOL_SHA = "2c6f1aebfae91d95ed1f10e2cae6db6e8665e653d3ec5ecd881e988cab56d664"
GEN_MANIFEST = RESUME / "sp-prepare-expected-manifest-r6-20261104.json"
R4_INPUT = RESUME / "sp-corrected-input-r4-20261104.json"
R4_SUPP = RESUME / "sp-corrected-supplement-r4-20261104.json"
EXPECTED_ABSENT = (SRC_REL / "gates", Path("gates"),
                   SRC_REL / "candidate-matrix-v2.json", SRC_REL / "candidate-selection-v2.json",
                   SRC_REL / "orchestration/v2/interactive/selection-architecture-input.json",
                   SRC_REL / "CANDIDATES_NORMALIZED.json", SRC_REL / "EVIDENCE_REVIEWED.json")
LEDGER_REL = SRC_REL / "materiality-ledger-v2.json"
COMP_REL = SRC_REL / "profile-completeness-v2.json"
HEX64_RE = re.compile(r"[0-9a-f]{64}")
HEX40_RE = re.compile(r"[0-9a-f]{40}")


def _load_r6():
    """Reuse pinned r6 helpers: verify exact code hash first, then import.
    r6 top level is stdlib-only, so importing performs no project calls."""
    data = R6_TOOL.read_bytes()
    if hashlib.sha256(data).hexdigest() != R6_TOOL_SHA:
        raise ValueError("r6 helper code drift vs pinned hash (refuse)")
    import importlib.util
    spec = importlib.util.spec_from_file_location("r6prepare", R6_TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _check_retention_root(ret_dir: Path, base: Path = RESUME) -> Path:
    """Retention must sit DIRECTLY under the given base (production: the resume
    packet; never inside the active tree or elsewhere). Returns the absolutized
    lexical path."""
    abs_ret = ret_dir if ret_dir.is_absolute() else (Path.cwd() / ret_dir)
    abs_ret = Path(os.path.normpath(str(abs_ret)))
    if abs_ret.parent != base.resolve():
        raise ValueError(f"retention must sit directly under the base dir (refuse): {ret_dir}")
    return abs_ret


def _verify_ready_self(ready_path: Path, expected_sha: str) -> dict:
    if not HEX64_RE.fullmatch(expected_sha or ""):
        raise ValueError("expected READY SHA must be 64-hex (externally recorded)")
    raw = ready_path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected_sha:
        raise ValueError("READY bytes drift vs externally recorded hash (refuse)")
    val = json.loads(raw.decode("utf-8"))
    if not isinstance(val, dict) or val.get("ready") is not True or val.get("stage") != "prepare-only":
        raise ValueError("READY is not a prepare-only READY record (refuse)")
    if val.get("manifest", {}).get("sha256") is None:
        raise ValueError("READY lacks manifest binding (refuse)")
    return val


def _read_umask() -> tuple[int, int]:
    """Record process umask without permanent change (single-threaded tool;
    no file I/O happens between the set and the restore). Returns
    (umask, write_json_mode) where write_json_mode = 0o666 & ~umask."""
    prev = os.umask(0)
    os.umask(prev)
    return prev, (0o666 & ~prev)


def _backup_owned(R6, repo: Path, rel: Path, ret_dir: Path, state_sha_hex: str, expect_pin: dict, allowed_root: Path) -> dict:
    """Exclusive backup of one owned file: re-read + pin vs expected, O_EXCL +
    chmod + readback verify. state_sha must be the live-verified 64-char State
    file SHA, never a 40-char commit. Returns manifest linkage entry."""
    if not HEX64_RE.fullmatch(state_sha_hex or ""):
        raise ValueError(f"backup requires live-verified 64-char State SHA, got: {state_sha_hex!r}")
    live = R6._pin_live(repo, rel, expect_pin, mode="0o664")
    dest = ret_dir / rel.name
    got = R6._stage_bytes_exclusive_under(dest, allowed_root, (repo / rel).read_bytes())
    if got["sha256"] != live["sha256"]:
        raise ValueError(f"backup SHA mismatch (preserve, STOP): {rel}")
    return {"old": rel.as_posix(), "new": dest.name, "sha256": got["sha256"],
            "bytes": got["bytes"], "mode": "0o664", "state_sha": state_sha_hex,
            "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")}


def _verify_tree_phase(R6, repo: Path, exp_files: dict, exp_dirs: set, label: str) -> None:
    live_files, live_dirs, walk_errs = R6._walk_sp_tree_stdlib(repo, SRC_REL)
    if walk_errs:
        raise ValueError(f"{label}: SP walk FAILED:\n- " + "\n- ".join(walk_errs[:10]))
    errs = R6._compare_sp_tree(live_files, live_dirs, exp_files, exp_dirs)
    if errs:
        raise ValueError(f"{label}: tree mismatch (preserve, STOP):\n- " + "\n- ".join(errs[:10]))


def _gate_phase(R6, M, repo: Path, manifest: dict, manifest_path: Path, ready: dict, ready_path: Path,
                exp_manifest_sha: str, exp_ready_sha: str, exp_files: dict, exp_dirs: set, ret_dir: Path | None,
                label: str, expect_ledger: bool, expect_comp: bool) -> None:
    """Pre-removal gate: same-hash manifest/READY recheck, strict State + DM022,
    full tree set, all771, material pins, gates/refs, and (after backup) BOTH
    retained backups re-verified (bytes/mode/sha/nlink). Fail closed."""
    errs: list[str] = []
    try:
        if hashlib.sha256(manifest_path.read_bytes()).hexdigest() != exp_manifest_sha:
            errs.append(f"{label} manifest changed mid-run (refuse; same-hash recheck)")
        if hashlib.sha256(ready_path.read_bytes()).hexdigest() != exp_ready_sha:
            errs.append(f"{label} READY changed mid-run (refuse; same-hash recheck)")
    except OSError as e:
        errs.append(f"{label} pin re-read: {e}")
    try:
        R6._strict_state_and_ready(repo, M, manifest)
    except ValueError as e:
        errs.append(f"{label} state/readiness: {e}")
    try:
        live_files, live_dirs, walk_errs = R6._walk_sp_tree_stdlib(repo, SRC_REL)
        errs.extend(f"{label} walk: {e}" for e in walk_errs)
        if not walk_errs:
            errs.extend(f"{label} tree: {e}" for e in R6._compare_sp_tree(live_files, live_dirs, exp_files, exp_dirs))
    except ValueError as e:
        errs.append(f"{label} walk exception: {e}")
    try:
        errs.extend(f"{label} intended: {e}" for e in R6._check_intended_tree_stdlib(repo, manifest["delivery"]["intended"], manifest["delivery"]["test_pin"]))
    except ValueError as e:
        errs.append(f"{label} intended exception: {e}")
    try:
        if expect_ledger:
            R6._pin_live(repo, LEDGER_REL, manifest["original_authority"]["ledger"], mode="0o664")
        else:
            R6._require_absent(repo, LEDGER_REL)
        if expect_comp:
            R6._pin_live(repo, COMP_REL, manifest["original_authority"]["completeness"], mode="0o664")
        else:
            R6._require_absent(repo, COMP_REL)
    except ValueError as e:
        errs.append(f"{label} material pins: {e}")
    try:
        errs.extend(f"{label} gates: {e}" for e in R6._check_gates_absent(repo))
        errs.extend(f"{label} refs: {e}" for e in R6._scan_ledger_refs(repo, manifest["stage_ledger_ref_scan"]))
    except ValueError as e:
        errs.append(f"{label} gates/refs exception: {e}")
    if ret_dir is not None:
        try:
            for key in ("ledger", "completeness"):
                expect = manifest["original_authority"][key]
                back = ret_dir / Path(expect["rel"]).name
                if os.path.islink(back) or not back.is_file():
                    errs.append(f"{label} retained backup missing/unsafe: {key}")
                    continue
                st = os.lstat(back)
                if (hashlib.sha256(back.read_bytes()).hexdigest() != expect["sha256"] or back.stat().st_size != expect["bytes"]
                        or oct(st.st_mode & 0o777) != "0o664" or st.st_nlink != 1):
                    errs.append(f"{label} retained backup drift (preserve, STOP): {expect['rel']}")
        except OSError as e:
            errs.append(f"{label} backup re-read: {e}")
    if errs:
        raise ValueError(f"{label} FAILED (preserve partials, STOP, no restore, no retry):\n- " + "\n- ".join(errs[:15]))


def _check_post_run_layout(repo: Path, src_rel: Path, baseline_files: dict, baseline_dirs: set, staged_new: list,
                           old_ledger_rel: str, old_comp_rel: str, old_ev_dirs: list, old_view_dirs: list,
                           exp_results_n: int, staged_input_rel: str, staged_input_sha: str,
                           staged_supp_rel: str, staged_supp_sha: str,
                           exp_disc_n: int, exp_oblig_n: int, input_closure_status: str,
                           umask_file_mode: int) -> dict:
    """Stdlib post-run layout/binding check (no project imports). New normal outputs
    carry the recorded umask-derived mode (write_json) or 0o664 (O_EXCL copies of
    664 sources); staged files stay 0o664; old files byte-identical except the
    exact2 regenerated pair. Raises with exact partials."""
    um = oct(umask_file_mode)
    files: dict[str, dict] = {}
    dirs: set[str] = set()
    errs: list[str] = []
    for p in sorted((repo / src_rel).rglob("*")):
        rel = p.relative_to(repo).as_posix()
        if p.is_symlink():
            errs.append(f"symlink in SP tree: {rel}")
            continue
        if p.is_dir():
            dirs.add(rel)
        elif p.is_file():
            st = os.lstat(p)
            if not stat.S_ISREG(st.st_mode):
                errs.append(f"special entry: {rel}")
                continue
            data = p.read_bytes()
            files[rel] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                          "mode": oct(st.st_mode & 0o777), "nlink": st.st_nlink}
        else:
            errs.append(f"special entry: {rel}")
    if errs:
        raise ValueError("post-run walk FAILED:\n- " + "\n- ".join(errs[:10]))
    ev_root = f"{src_rel}/evidence/v2/accepted"
    view_root = f"{src_rel}/evidence/v2/views/accepted"
    old_ev = {f"{ev_root}/{d}" for d in old_ev_dirs}
    old_view = {f"{view_root}/{d}" for d in old_view_dirs}
    new_ev = sorted(d for d in dirs if d.startswith(ev_root + "/") and d.count("/") == len(ev_root.split("/")) and d not in old_ev and d != ev_root)
    new_view = sorted(d for d in dirs if d.startswith(view_root + "/") and d.count("/") == len(view_root.split("/")) and d not in old_view and d != view_root)
    if len(new_ev) != 1 or len(new_view) != 1:
        raise ValueError(f"expected exactly 1 NEW accepted dir per root, got ev={new_ev} views={new_view}")
    new_ev_rel, new_view_rel = new_ev[0], new_view[0]
    exp_new_files = {
        f"{new_ev_rel}/evidence-accepted.json", f"{new_ev_rel}/package.json",
        f"{new_ev_rel}/interactive-evidence.json", f"{new_ev_rel}/interactive-audit.json",
        f"{new_view_rel}/edition-views-accepted.json",
    }
    copy_files = sorted(r for r in files if r.startswith(new_ev_rel + "/tasks/") or r.startswith(new_ev_rel + "/results/"))
    view_files = sorted(r for r in files if r.startswith(new_view_rel + "/views/"))
    task_files = sorted(r for r in copy_files if "/tasks/" in r)
    result_files = sorted(r for r in copy_files if "/results/" in r)
    if len(task_files) != exp_results_n or len(result_files) != exp_results_n or len(view_files) != exp_results_n:
        errs.append(f"produced copy counts != {exp_results_n}: tasks={len(task_files)} results={len(result_files)} views={len(view_files)}")
    top_new = {r for r in files if r in exp_new_files}
    if top_new != exp_new_files:
        errs.append(f"new accepted top files mismatch: missing={sorted(exp_new_files-top_new)[:5]}")
    # staged files: unchanged, still O_EXCL 0o664
    for e in staged_new:
        got = files.get(e["rel"])
        if got is None or got["sha256"] != e["sha256"] or got["bytes"] != e["bytes"]:
            errs.append(f"staged file drift after run: {e['rel']}")
        elif got["mode"] != "0o664" or got.get("nlink", 1) != 1:
            errs.append(f"staged file identity drift after run: {e['rel']}")
    # old files: byte-identical except the exact2 regenerated pair
    for rel, exp in baseline_files.items():
        if rel in (old_ledger_rel, old_comp_rel):
            continue
        got = files.get(rel)
        if got is None:
            errs.append(f"old file missing after run: {rel}")
        elif got["sha256"] != exp["sha256"] or got["bytes"] != exp["bytes"] or got["mode"] != exp["mode"]:
            errs.append(f"old file changed by run (must be byte-identical): {rel}")
    # exact2 regenerated with recorded umask-derived modes (normal subprocess writes)
    for rel in (old_ledger_rel, old_comp_rel):
        got = files.get(rel)
        exp_old = baseline_files.get(rel)
        if got is None or exp_old is None:
            errs.append(f"exact2 path missing: {rel}")
        elif got["sha256"] == exp_old["sha256"]:
            errs.append(f"exact2 NOT regenerated (still old bytes): {rel}")
        elif got["mode"] != um or got.get("nlink", 1) != 1:
            errs.append(f"exact2 identity drift (expected recorded umask mode {um}/nlink 1): {rel} got {got['mode']}/nlink {got.get('nlink')}")
    # new outputs: umask-derived modes for normal-subprocess writes, 0o664 for the O_EXCL-copied archived input
    for r in sorted(exp_new_files):
        got = files.get(r)
        if got is None:
            continue
        want = "0o664" if r.endswith("/interactive-evidence.json") else um
        if got["mode"] != want or got.get("nlink", 1) != 1:
            errs.append(f"new output mode drift (expected {want} from recorded run mode): {r} got {got['mode']}")
    for r in task_files + result_files + view_files:
        got = files[r]
        if got["mode"] != um or got.get("nlink", 1) != 1:
            errs.append(f"new copy mode drift (expected recorded umask mode {um}): {r} got {got['mode']}")
    unexpected = set(files) - set(baseline_files) - {e["rel"] for e in staged_new} - exp_new_files - set(task_files) - set(result_files) - set(view_files)
    if unexpected:
        errs.append(f"unexpected active writes by run: {sorted(unexpected)[:8]}")
    exp_dirs = set(baseline_dirs) | {new_ev_rel, f"{new_ev_rel}/tasks", f"{new_ev_rel}/results", new_view_rel, f"{new_view_rel}/views"}
    if errs:
        raise ValueError("post-run layout FAILED (preserve, STOP):\n- " + "\n- ".join(errs[:12]))
    if dirs != exp_dirs:
        raise ValueError(f"post-run dir set drift: missing={sorted(exp_dirs-dirs)[:5]} extra={sorted(dirs-exp_dirs)[:5]}")
    # produced-record bindings (actual files, no transcription)
    ev_acc = json.loads((repo / f"{new_ev_rel}/evidence-accepted.json").read_bytes().decode("utf-8"))
    if ev_acc.get("result_count") != exp_results_n or len(ev_acc.get("results", [])) != exp_results_n:
        raise ValueError(f"evidence results != {exp_results_n}")
    if ev_acc.get("issue_id") != ISSUE:
        raise ValueError("evidence acceptance issue mismatch")
    if ev_acc.get("result_set_sha256") != new_ev_rel.rsplit("/", 1)[-1]:
        raise ValueError("evidence result set != new dir name")
    pkg = json.loads((repo / f"{new_ev_rel}/package.json").read_bytes().decode("utf-8"))
    auth = pkg.get("authority_supplement") or {}
    if auth.get("path") != staged_supp_rel or auth.get("sha256") != staged_supp_sha:
        raise ValueError("package supplement reference != staged supplement (refuse)")
    audit = json.loads((repo / f"{new_ev_rel}/interactive-audit.json").read_bytes().decode("utf-8"))
    inp = audit.get("interactive_input") or {}
    if inp.get("path") != f"{new_ev_rel}/interactive-evidence.json" or inp.get("sha256") != staged_input_sha:
        raise ValueError("audit input reference != NEW accepted archive path + staged bytes (refuse)")
    arch = (repo / f"{new_ev_rel}/interactive-evidence.json").read_bytes()
    if hashlib.sha256(arch).hexdigest() != staged_input_sha:
        raise ValueError("archived input bytes differ from staged input (refuse)")
    view_acc = json.loads((repo / f"{new_view_rel}/edition-views-accepted.json").read_bytes().decode("utf-8"))
    if len(view_acc.get("views", [])) != exp_results_n:
        raise ValueError(f"views != {exp_results_n}")
    if view_acc.get("view_set_sha256") != new_view_rel.rsplit("/", 1)[-1]:
        raise ValueError("views set != new dir name")
    res_by_task = {r["evidence_task_id"]: r for r in ev_acc["results"]}
    for v in view_acc["views"]:
        r = res_by_task.get(v.get("evidence_task_id"))
        if r is None or v.get("evidence_sha256") != r.get("sha256"):
            raise ValueError(f"view/card binding broken: {v.get('evidence_task_id')}")
    ledger_raw = (repo / old_ledger_rel).read_bytes()
    comp_raw = (repo / old_comp_rel).read_bytes()
    ledger = json.loads(ledger_raw.decode("utf-8"))
    if len(ledger.get("rows", [])) != exp_disc_n:
        raise ValueError(f"ledger rows {len(ledger.get('rows', []))} != discovery {exp_disc_n}")
    comp = json.loads(comp_raw.decode("utf-8"))
    if len(comp.get("obligations", [])) != exp_oblig_n:
        raise ValueError(f"completeness obligations {len(comp.get('obligations', []))} != {exp_oblig_n}")
    if comp.get("overall_status") != input_closure_status:
        raise ValueError(f"completeness status {comp.get('overall_status')!r} != input closure {input_closure_status!r}")
    return {"new_ev_dir": new_ev_rel, "new_view_dir": new_view_rel,
            "ev_acceptance": f"{new_ev_rel}/evidence-accepted.json",
            "views_acceptance": f"{new_view_rel}/edition-views-accepted.json",
            "ledger": old_ledger_rel, "completeness": old_comp_rel,
            "ledger_sha": hashlib.sha256(ledger_raw).hexdigest(),
            "ledger_bytes": len(ledger_raw),
            "completeness_sha": hashlib.sha256(comp_raw).hexdigest(),
            "completeness_bytes": len(comp_raw),
            "task_files": len(task_files), "result_files": len(result_files), "view_files": len(view_files),
            "ledger_rows": len(ledger.get("rows", [])), "ev_results": len(ev_acc["results"]), "ev_views": len(view_acc["views"]),
            "comp_obligations": len(comp.get("obligations", [])), "comp_status": comp.get("overall_status")}


def _best_effort_excl_write(abs_dest: Path, allowed_root: Path, data: bytes) -> None:
    """Best-effort O_EXCL packet-local write for FAILURE evidence only. Never
    masks the original refusal; carries no authority semantics."""
    root = allowed_root.resolve()
    norm = os.path.normpath(str(abs_dest if abs_dest.is_absolute() else (Path.cwd() / abs_dest)))
    if norm != str(root) and not norm.startswith(str(root) + os.sep):
        return
    if os.path.islink(Path(norm)) or Path(norm).exists():
        return
    try:
        fd = os.open(Path(norm), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o664)
        try:
            mv = memoryview(data)
            while mv:
                n = os.write(fd, mv)
                mv = mv[n:]
            os.fsync(fd)
        finally:
            try:
                os.close(fd)
            except OSError:
                pass
    except OSError:
        return
    try:
        os.chmod(Path(norm), 0o664)
    except OSError:
        pass


def stage_dispose_run(ret_dir: Path, ready_path: Path, manifest_path: Path, exp_ready_sha: str, exp_manifest_sha: str) -> dict:
    R6 = _load_r6()
    manifest = R6._verify_manifest_self(manifest_path, exp_manifest_sha)
    ready = _verify_ready_self(ready_path, exp_ready_sha)
    if ready.get("manifest", {}).get("sha256") != exp_manifest_sha:
        raise ValueError("READY does not bind the expected manifest (refuse)")
    repo = REPO_ROOT.resolve()
    errs: list[str] = []
    ctx: dict = {}

    # ---- P0: invocation pin + source bytes BEFORE imports (stdlib only) ----
    try:
        umask_val, umask_file_mode = _read_umask()
        ctx["umask"] = oct(umask_val)
        ctx["umask_file_mode"] = umask_file_mode
        pre = R6._phase0_source_precheck(repo, manifest)
    except ValueError as e:
        raise ValueError(f"phase0 source precheck: {e}") from e
    M = R6._bind_roots_after_import(repo, pre)
    core = M["core"]
    ctx["module_roots"] = M["roots"]

    # ---- P1: full pre-disposal verification (reads only, zero active writes) ----
    try:
        live_impl = core.repository_commit_sha(repo)  # single selected isolated call (mirrors run():599)
        if not HEX40_RE.fullmatch(live_impl or ""):
            errs.append(f"live implementation SHA not 40-hex: {live_impl!r}")
        ctx["live_implementation_sha"] = live_impl
        if live_impl != ready.get("live_implementation_sha"):
            errs.append(f"live HEAD drift vs READY live impl (refuse): {live_impl} != {ready.get('live_implementation_sha')}")
        if live_impl != manifest["active_instance"]["recorded_head"]:
            errs.append("live HEAD drift vs recorded e84 head (refuse blind proceed)")
        cfg, state, state_path, profile_path = R6._strict_state_and_ready(repo, M, manifest)
        ctx["state_path"] = state_path
        # full SP tree == baseline 552 + READY exact 19 (current 571)
        new_rels = [e["rel"] for e in ready["staged_raw"]] + [ready["new_input"]["rel"], ready["new_supplement"]["rel"]]
        if len(new_rels) != 19:
            errs.append(f"READY new set != 19: {len(new_rels)}")
        exp_files_571 = {e["rel"]: e for e in manifest["sp_tree_full"]["files"]}
        for e in ready["staged_raw"] + [ready["new_input"], ready["new_supplement"]]:
            exp_files_571[e["rel"]] = {"sha256": e["sha256"], "bytes": e["bytes"], "mode": e["mode"], "nlink": 1}
        exp_dirs = {e["rel"] for e in manifest["sp_tree_full"]["dirs"]}
        ctx["exp_files_571"], ctx["exp_dirs"] = exp_files_571, exp_dirs
        _verify_tree_phase(R6, repo, exp_files_571, exp_dirs, "pre-disposal")
        erv = R6._check_intended_tree_stdlib(repo, manifest["delivery"]["intended"], manifest["delivery"]["test_pin"])
        errs.extend(f"pre-disposal intended: {e}" for e in erv)
        # all30 Raw + staged input/supplement pins + r4 cross-check, no transcription
        r4supp_raw = R4_SUPP.read_bytes()
        r4input_raw = R4_INPUT.read_bytes()
        if hashlib.sha256(r4supp_raw).hexdigest() != manifest["corrected"]["supplement"]["sha256"]:
            errs.append("r4 supplement bytes drift vs manifest")
        if hashlib.sha256(r4input_raw).hexdigest() != manifest["corrected"]["input"]["sha256"]:
            errs.append("r4 input bytes drift vs manifest")
        r4supp = json.loads(r4supp_raw.decode("utf-8"))
        r4input = json.loads(r4input_raw.decode("utf-8"))
        if r4supp["supplement_id"] == ready.get("supplement_id"):
            errs.append("READY supplement_id must differ from r4 draft id")
        errs.extend(f"pre-disposal rows: {e}" for e in R6._check_supplement_rows_stdlib(repo, r4supp["sources"], manifest["supplement30"], WSROOT))
        ctx["r4supp"] = r4supp
        ctx["exp_oblig_n"] = len(r4input["completeness"]["obligations"])
        ctx["exp_closure"] = r4input["completeness"]["closure"]["status"]
        for s in r4supp["sources"]:
            if s["evidence_task_id"] != M["ev"].stable_task_id(ISSUE, s["discovery_id"]):
                errs.append(f"task_id mismatch (real function): {s['discovery_id']}")
            try:
                if s["source_class"] != M["ev"]._source_class(s["source_type"]):
                    errs.append(f"source_class mismatch (real function): {s['discovery_id']}")
            except ValueError as e:
                errs.append(f"source_type unsupported {s['discovery_id']}: {e}")
        if r4input.get("schema_version") != "2.0-rc1" or r4input.get("issue_id") != ISSUE:
            errs.append("corrected input identity mismatch")
        if len(r4input.get("records", [])) != 160 or len(r4input.get("completeness", {}).get("obligations", [])) != 15:
            errs.append("corrected input counts != 160/15")
        ctx["new_input_rel"] = ready["new_input"]["rel"]
        ctx["new_supplement_rel"] = ready["new_supplement"]["rel"]
        for rel in (Path(ctx["new_input_rel"]), Path(ctx["new_supplement_rel"])):
            try:
                R6._pin_live(repo, rel, next(e for e in [ready["new_input"], ready["new_supplement"]] if e["rel"] == rel.as_posix()), mode="0o664")
            except ValueError as e:
                errs.append(f"staged NEW drift: {e}")
        # resolver pair mirrors run():595-611 (read-only; inside facade like run())
        with M["at"].current_stage_basis_override():
            accepted_discovery = M["disc"].validate_acceptance(repo, (repo / SRC_REL) / "discovery/discovery-accepted-v2.json")
            root_discovery_path = core.repo_local_path(repo, accepted_discovery["discovery_path"], "accepted Discovery JSONL")
            active = M["sc"].resolve_active_screening_acceptance(repo, state_path, live_impl)
            _sp = Path(active["path"])
            screening_path = _sp if _sp.is_absolute() else (repo / _sp)
            effective = M["sc"].resolve_effective_discovery_basis(
                repo, screening_path.parent / "package.json", live_impl,
                accepted_root_path=root_discovery_path)
        if "root_records" not in effective or not effective["root_records"] or not effective.get("records"):
            errs.append("effective basis missing validated root/effective records")
        ctx["screening_acc_path"] = screening_path if screening_path.is_absolute() else (repo / screening_path)
        ctx["discovery_path_abs"] = Path(effective["path"]) if Path(effective["path"]).is_absolute() else (repo / effective["path"])
        # real full supplement normal validation BEFORE any destructive action (existing, facade)
        with M["at"].current_stage_basis_override():
            _real_acc, _, _real_disc = M["ev"].validate_screening_acceptance(
                repo, ctx["screening_acc_path"], ctx["discovery_path_abs"], ISSUE, live_impl)
            M["ev"].validate_evidence_authority_supplement(
                repo, repo / Path(ctx["new_supplement_rel"]), live_impl,
                expected_issue_id=ISSUE, expected_source_root=(repo / SRC_REL).resolve(),
                expected_discovery_path=ctx["discovery_path_abs"],
                expected_screening_acceptance_path=ctx["screening_acc_path"],
                screening_acceptance=_real_acc, discoveries=_real_disc)
            ctx["real_acc"], ctx["real_disc"] = _real_acc, _real_disc
        # retained package basis checks BEFORE removal (existing validator, facade)
        prep_ret = ready_path.parent
        pkg_path = prep_ret / ready["retained_pkg_dir"] / "package.json"
        if not pkg_path.is_file() or os.path.islink(pkg_path):
            errs.append(f"retained package missing/unsafe: {pkg_path}")
        else:
            if hashlib.sha256(pkg_path.read_bytes()).hexdigest() != ready["package_json_sha"]:
                errs.append("retained package.json drift vs READY (refuse)")
            else:
                ctx["pkg_path"] = pkg_path
                ctx["package"] = json.loads(pkg_path.read_bytes().decode("utf-8"))
                with M["at"].current_stage_basis_override():
                    M["ev"].validate_evidence_package_basis(repo, pkg_path, ctx["package"], live_impl)
        # gates/CP/checkpoints/accepted pins
        errs.extend(f"pre-disposal gates: {e}" for e in R6._check_gates_absent(repo))
        errs.extend(f"pre-disposal refs: {e}" for e in R6._scan_ledger_refs(repo, manifest["stage_ledger_ref_scan"]))
        for name in ("DISCOVERY_COLLECTED", "ISSUE_INITIALIZED"):
            try:
                R6._pin_live(repo, SRC_REL / "orchestration/v2/checkpoints" / f"{name}.json",
                             manifest["original_authority"][f"checkpoint_{name}"])
            except ValueError as e:
                errs.append(f"checkpoint {name}: {e}")
        for key, pin in manifest["original_authority"].items():
            if key.startswith("accepted_") and isinstance(pin, dict) and "rel" in pin:
                try:
                    R6._pin_live(repo, Path(pin["rel"]), pin)
                except ValueError as e:
                    errs.append(f"authority {key}: {e}")
        for key in ("state", "profile", "ledger", "completeness"):
            try:
                R6._pin_live(repo, Path(manifest["original_authority"][key]["rel"]), manifest["original_authority"][key])
            except ValueError as e:
                errs.append(f"preserved {key}: {e}")
    except ValueError as e:
        errs.append(f"phase1 exception: {e}")
    if errs:
        raise ValueError("pre-disposal verification FAILED (zero active writes performed):\n- " + "\n- ".join(errs[:25]))

    # ---- P2: exclusive NEW retention (exact resume-packet containment) + backups ----
    try:
        ret_dir = _check_retention_root(ret_dir, RESUME)
        R6._require_absent_under(RESUME.resolve(), ret_dir)
        ret_dir.parent.mkdir(parents=True, exist_ok=True)
    except (ValueError, OSError) as e:
        raise ValueError(f"retention path refused: {e}") from e
    try:
        ret_dir.mkdir(exist_ok=False)
    except FileExistsError:
        raise ValueError(f"single-use refuse: retention exists: {ret_dir}")
    try:
        state_sha_live = hashlib.sha256((repo / (SRC_REL / "production-state.json")).read_bytes()).hexdigest()
        if state_sha_live != manifest["original_authority"]["state"]["sha256"]:
            raise ValueError("State drift at backup time (STOP, preserve)")
    except OSError as e:
        raise ValueError(f"State re-read failed: {e}") from e
    journal: list[dict] = [{"step": "phase1", "result": "pass", "live_impl": ctx["live_implementation_sha"], "umask": ctx["umask"]}]
    man = {"ledger": _backup_owned(R6, repo, LEDGER_REL, ret_dir, state_sha_live, manifest["original_authority"]["ledger"], RESUME.resolve()),
           "completeness": _backup_owned(R6, repo, COMP_REL, ret_dir, state_sha_live, manifest["original_authority"]["completeness"], RESUME.resolve())}
    man["context"] = {"issue": ISSUE, "retained_from_ready": ready_path.name, "ready_sha256": exp_ready_sha,
                      "manifest_sha256": exp_manifest_sha, "state_sha256": state_sha_live,
                      "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
                      "note": "immutable linkage old->new; O_EXCL-created, chmod 0o664, readback-verified; no rename onto backup names; no automatic restore"}
    journal.append({"step": "backup-2", "ledger": man["ledger"]["sha256"], "completeness": man["completeness"]["sha256"]})
    R6._stage_bytes_exclusive_under(ret_dir / "retention-manifest.json", RESUME.resolve(),
                                    (json.dumps(man, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))

    # ---- P3: ledger gate -> unlink ledger ONLY ----
    _gate_phase(R6, M, repo, manifest, manifest_path, ready, ready_path, exp_manifest_sha, exp_ready_sha,
                exp_files_571, exp_dirs, ret_dir, "gate-ledger", expect_ledger=True, expect_comp=True)
    R6._pin_live(repo, LEDGER_REL, manifest["original_authority"]["ledger"], mode="0o664")
    R6._pin_live(repo, COMP_REL, manifest["original_authority"]["completeness"], mode="0o664")
    R6._strict_state_and_ready(repo, M, manifest)
    os.unlink(repo / LEDGER_REL)
    R6._require_absent(repo, LEDGER_REL)
    if hashlib.sha256((ret_dir / "materiality-ledger-v2.json").read_bytes()).hexdigest() != manifest["original_authority"]["ledger"]["sha256"]:
        raise ValueError("retention Ledger drift after unlink (preserve partials, STOP, no restore)")
    journal.append({"step": "unlink-ledger", "result": "absent-verified"})

    # ---- P4: completeness gate -> unlink completeness ONLY ----
    exp_files_570 = dict(exp_files_571)
    del exp_files_570[LEDGER_REL.as_posix()]
    _gate_phase(R6, M, repo, manifest, manifest_path, ready, ready_path, exp_manifest_sha, exp_ready_sha,
                exp_files_570, exp_dirs, ret_dir, "gate-completeness", expect_ledger=False, expect_comp=True)
    R6._pin_live(repo, COMP_REL, manifest["original_authority"]["completeness"], mode="0o664")
    R6._strict_state_and_ready(repo, M, manifest)
    os.unlink(repo / COMP_REL)
    R6._require_absent(repo, COMP_REL)
    R6._require_absent(repo, LEDGER_REL)
    if hashlib.sha256((ret_dir / "profile-completeness-v2.json").read_bytes()).hexdigest() != manifest["original_authority"]["completeness"]["sha256"]:
        raise ValueError("retention Completeness drift after unlink (preserve partials, STOP, no restore)")
    journal.append({"step": "unlink-completeness", "result": "both-absent-verified"})

    # ---- P5: post-disposal verify (569 set, accepted unchanged, gates, CAND State) ----
    exp_files_569 = dict(exp_files_570)
    del exp_files_569[COMP_REL.as_posix()]
    _verify_tree_phase(R6, repo, exp_files_569, exp_dirs, "post-disposal")
    for key, pin in manifest["original_authority"].items():
        if key.startswith("accepted_") and isinstance(pin, dict) and "rel" in pin:
            R6._pin_live(repo, Path(pin["rel"]), pin)
    for e in R6._check_gates_absent(repo):
        raise ValueError(f"post-disposal gates: {e}")
    for e in R6._scan_ledger_refs(repo, manifest["stage_ledger_ref_scan"]):
        raise ValueError(f"post-disposal refs: {e}")
    if hashlib.sha256((repo / (SRC_REL / "production-state.json")).read_bytes()).hexdigest() != manifest["original_authority"]["state"]["sha256"]:
        raise ValueError("State bytes changed during disposal (STOP, preserve)")
    R6._strict_state_and_ready(repo, M, manifest)
    journal.append({"step": "post-disposal-verify", "result": "pass"})

    # ---- P6: ONE ordinary normal retry (existing public API; owns its own facade) ----
    input_abs = repo / Path(ctx["new_input_rel"])
    supp_abs = repo / Path(ctx["new_supplement_rel"])
    result = M["rn"].run(repo, state_path, input_abs, supp_abs)
    journal.append({"step": "run", "result": result})
    if result.get("evidence_result_count") != 160:
        raise ValueError(f"run result count != 160 (preserve, STOP): {result.get('evidence_result_count')}")

    # ---- P7: post-run verify (State CAND+unchanged; layout; actual validators; refs; counts) ----
    st_after = json.loads((repo / (SRC_REL / "production-state.json")).read_bytes().decode("utf-8"))
    if st_after.get("lifecycle_state") != "CANDIDATES_NORMALIZED":
        raise ValueError("State advanced by run (refuse; expected still CAND)")
    if hashlib.sha256((repo / (SRC_REL / "production-state.json")).read_bytes()).hexdigest() != manifest["original_authority"]["state"]["sha256"]:
        raise ValueError("State bytes changed by run (STOP, preserve)")
    disc_lines = (repo / (SRC_REL / "discovery/discovery-v2.jsonl")).read_text().splitlines()
    exp_disc_n = len([ln for ln in disc_lines if ln.strip()])
    bindings = _check_post_run_layout(repo, SRC_REL, {e["rel"]: e for e in manifest["sp_tree_full"]["files"]},
                                      {e["rel"] for e in manifest["sp_tree_full"]["dirs"]},
                                      [{"rel": r, "sha256": e["sha256"], "bytes": e["bytes"]}
                                       for r, e in ((n, next(x for x in ([ready["new_input"], ready["new_supplement"]] + list(ready["staged_raw"])) if x["rel"] == n)) for n in new_rels)],
                                      LEDGER_REL.as_posix(), COMP_REL.as_posix(),
                                      [d for d in manifest["original_authority"].get("accepted_evidence_dirs", [])],
                                      [d for d in manifest["original_authority"].get("accepted_views_dirs", [])],
                                      160, ctx["new_input_rel"], ready["new_input"]["sha256"],
                                      ctx["new_supplement_rel"], ready["new_supplement"]["sha256"],
                                      exp_disc_n, ctx["exp_oblig_n"], ctx["exp_closure"], ctx["umask_file_mode"])
    with M["at"].current_stage_basis_override():
        ev_acc_path = repo / bindings["ev_acceptance"]
        view_acc_path = repo / bindings["views_acceptance"]
        M["ev"].validate_evidence_acceptance(repo, ev_acc_path, ctx["live_implementation_sha"])
        M["ev"].validate_edition_views_acceptance(
            repo, repo / (SRC_REL / "production-profile.json"),
            ev_acc_path, view_acc_path, ctx["live_implementation_sha"])
        ledger_doc = json.loads((repo / bindings["ledger"]).read_bytes().decode("utf-8"))
        M["ev"].validate_materiality_ledger(
            ledger_doc, repo, repo / (SRC_REL / "production-profile.json"),
            repo / (SRC_REL / "discovery/discovery-v2.jsonl"), ctx["screening_acc_path"],
            ev_acc_path, view_acc_path, ctx["live_implementation_sha"])
        comp_doc = json.loads((repo / bindings["completeness"]).read_bytes().decode("utf-8"))
        comp_errs = M["comp"].validate_profile_completeness(
            comp_doc, repo, repo / (SRC_REL / "production-profile.json"),
            repo / (SRC_REL / "discovery/discovery-v2.jsonl"), ctx["screening_acc_path"],
            ev_acc_path, view_acc_path, repo / bindings["ledger"], ctx["live_implementation_sha"])
        if comp_errs:
            raise ValueError("produced Completeness invalid: " + "; ".join(comp_errs))
    journal.append({"step": "post-run-verify", "result": "pass", "bindings": bindings})

    # ---- P8: return gate (same captured pins, not reseal) + record ----
    if hashlib.sha256(manifest_path.read_bytes()).hexdigest() != exp_manifest_sha:
        raise ValueError("manifest changed during run (refuse record)")
    if hashlib.sha256(ready_path.read_bytes()).hexdigest() != exp_ready_sha:
        raise ValueError("READY changed during run (refuse record)")
    ret_in = R6._pin_live(repo, Path(ctx["new_input_rel"]), {"sha256": ready["new_input"]["sha256"], "bytes": ready["new_input"]["bytes"]}, mode="0o664")
    ret_supp = R6._pin_live(repo, Path(ctx["new_supplement_rel"]), {"sha256": ready["new_supplement"]["sha256"], "bytes": ready["new_supplement"]["bytes"]}, mode="0o664")
    for _rel_key, _sha_key in (("ledger", "ledger_sha"), ("completeness", "completeness_sha")):
        _cur = (repo / bindings[_rel_key]).read_bytes()
        if hashlib.sha256(_cur).hexdigest() != bindings[_sha_key]:
            raise ValueError(f"{_rel_key} bytes changed since post-run validation (refuse record)")
    ret_errs = R6._check_intended_tree_stdlib(repo, manifest["delivery"]["intended"], manifest["delivery"]["test_pin"])
    if ret_errs:
        raise ValueError("return-gate intended FAILED:\n- " + "\n- ".join(ret_errs[:10]))
    ready_out = {"ready": False, "stage": "dispose-run-complete", "no_removal_beyond_exact2": True,
                 "manifest": {"path": manifest_path.name, "sha256": exp_manifest_sha},
                 "ready_in": {"path": ready_path.name, "sha256": exp_ready_sha},
                 "live_implementation_sha": ctx["live_implementation_sha"],
                 "historical_implementation_sha": HIST_IMPL,
                 "supplement_id": ready["supplement_id"],
                 "new_input": ready["new_input"], "new_supplement": ready["new_supplement"],
                 "staged_raw": ready["staged_raw"],
                 "task_count": result.get("evidence_result_count"),
                 "completeness_status": result.get("completeness_status"),
                 "bindings": bindings, "journal": journal}
    rp = ret_dir / "DISPOSE_RUN.json"
    R6._stage_bytes_exclusive_under(rp, RESUME.resolve(), (json.dumps(ready_out, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    R6._stage_bytes_exclusive_under(ret_dir / "journal.json", RESUME.resolve(),
                                    (json.dumps(journal, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    return {"result": str(rp), "tasks": result.get("evidence_result_count"), "completeness": result.get("completeness_status")}


def main() -> int:
    global REPO_ROOT
    ap = argparse.ArgumentParser(description="SP dispose + normal-run one-use wrapper r2 (review only, do not run yet)")
    ap.add_argument("--retention-dir", type=Path, required=True)
    ap.add_argument("--ready-path", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, default=GEN_MANIFEST)
    ap.add_argument("--expected-tool-sha", type=str, required=True)
    ap.add_argument("--expected-ready-sha", type=str, required=True)
    ap.add_argument("--expected-manifest-sha", type=str, required=True)
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    a = ap.parse_args()
    REPO_ROOT = a.repo_root
    try:
        if hashlib.sha256(Path(__file__).read_bytes()).hexdigest() != a.expected_tool_sha:
            raise ValueError("wrapper bytes drift vs externally recorded tool hash (refuse)")
        out = stage_dispose_run(a.retention_dir, a.ready_path, a.manifest, a.expected_ready_sha, a.expected_manifest_sha)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        try:
            rd = a.retention_dir
            if rd.is_dir() and not os.path.islink(rd):
                partials = sorted(p.relative_to(rd).as_posix() for p in rd.rglob("*") if p.is_file())
                _best_effort_excl_write(
                    rd / "FAILURE.json", RESUME,
                    (json.dumps({"stage": "dispose-run", "exit": 2, "error": str(exc)[:4000],
                                 "retained_partials": partials}, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        except OSError:
            pass
        print(f"DISPOSE_RUN_REFUSED: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"stage": "dispose-run", "exit": 0, **out}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
