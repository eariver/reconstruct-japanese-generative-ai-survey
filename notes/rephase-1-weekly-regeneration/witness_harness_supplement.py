#!/usr/bin/env python3
"""Supplement harness for the narrow mechanical-refresh witness (fixture-only, disposable).

NEW file. The original `witness_harness.py` is NOT modified by this supplement; this module
only *imports* it (top level of the original is stdlib-only, so importing is side-effect
free) to reuse proven helpers. It fixes the evidence/oracle defects identified in review:

- A: commit-only (stdlib, provably no runtime imports) and verify/refresh run in DISTINCT
  OS processes; verify processes log the real current helper import path + file hash + HEAD
  and execute the actual validators (not just a path print).
- B: a TRUE criteria-contract mutation negative (required check added to
  `config/publication-review-v2.json` with review/source bytes unchanged), with mutation
  baseline snapshots, harness-policy refusal AND real-validator refusal recorded
  separately, plus a labeled dirty-config observation.
- C: per-critical-operation BEFORE/AFTER tree deltas (excluding only `.git`,
  `.witness-evidence/` instrumentation, and `__pycache__`, all disclosed); negatives assert
  no-write between mutation baseline and pre-restore snapshot, and State/record-listing
  invariance.
- D: read-only independent-DB checks (no alternates/shared/hardlink/root-override);
  content-byte comparison of the copied subset against exact e4c blobs (the old
  `content_boundary_hash` covered pathnames only and is so labeled, not reused).
- E: corrected raw-byte hashes recorded alongside (never replacing) original fields;
  accepted/authored ref equality asserted old-vs-new receipt; per-run metadata stored.
- F: every phase refuses to overwrite its own outputs (fail-closed unique-log guard);
  saved scripts are NOT safe reruns against the same logs dir (see supplement report).

Each phase is invoked as a separate OS process:
    witness_harness_supplement.py <phase> --edition DIR --logs DIR --run-id ID \
        [--marker M] [--expect-head SHA] [--w0sidecar P] [--r1sidecar P] \
        [--h0 SHA] [--expect-origin URL] [--exit-file P]

Only documentary evidence under notes/rephase-1-weekly-regeneration/ plus the disposable
edition repo passed via --edition are written. No candidate/runtime/test changes, no
reconstruct commits, no production/network/Actions/main. No reset/checkout/clean or other
destructive git operations anywhere in this file.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

E4C_REPO = Path("/tmp/jgas-rephase-gate-cli")
E4C_HEAD = "e4c82692abee6acedbba07815b0d74ccefb80a7e"
E4C_TREE = "bc377b6b7eb1e47dacd719e0f76b5a86703f3f3e"
B_REPO = Path("/tmp/jgas-rephase-increment-b-sol-implementation")
B_HEAD = "c04f32ad46109403e8a63faaa8394a90ee6b869c"
COPY_TOPS = ["config", "docs", "schemas", "scripts", "templates", "tests"]
HELPER_REL = "scripts/survey_weekly_derivation_v2.py"
CONTRACT_REL = "config/publication-review-v2.json"
NEW_CHECK_ID = "WITNESS_SUPPLEMENT_REQUIRED_CHECK"
GIT_ENV_OVERRIDES = (
    "GIT_DIR",
    "GIT_WORK_TREE",
    "GIT_INDEX_FILE",
    "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_COMMON_DIR",
)
WITNESS_IDENTITY = {
    "GIT_AUTHOR_NAME": "Synthetic Witness Fixture",
    "GIT_AUTHOR_EMAIL": "synthetic-witness@example.invalid",
    "GIT_COMMITTER_NAME": "Synthetic Witness Fixture",
    "GIT_COMMITTER_EMAIL": "synthetic-witness@example.invalid",
}
EXCLUDE_PREFIXES = (".witness-evidence/",)


def _utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def _git_env() -> dict:
    env = {k: v for k, v in os.environ.items() if k not in GIT_ENV_OVERRIDES}
    env.update(WITNESS_IDENTITY)
    return env


def _git(args: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args], cwd=str(cwd), env=_git_env(),
        capture_output=True, text=True, encoding="utf-8", errors="replace", check=check,
    )


def _require_fresh(path: Path) -> None:
    assert not path.exists(), f"refusing to overwrite existing output (use a new run-id): {path}"


def _snapshot(edition: Path) -> dict[str, str]:
    snap: dict[str, str] = {}
    for path in sorted(edition.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(edition)
        if rel.parts and rel.parts[0] == ".git":
            continue
        snap[str(rel).replace("\\", "/")] = _sha(path)
    return snap


def _ignored(rel: str) -> bool:
    return rel.startswith(EXCLUDE_PREFIXES) or "__pycache__" in rel.split("/")


def _delta(before: dict[str, str], after: dict[str, str]) -> dict[str, list[str]]:
    return {
        "added": sorted(k for k in after if k not in before and not _ignored(k)),
        "removed": sorted(k for k in before if k not in after and not _ignored(k)),
        "changed": sorted(k for k in before if k in after and before[k] != after[k] and not _ignored(k)),
    }


def _assert_delta(actual: dict[str, list[str]], added, changed, removed=()) -> None:
    assert actual["added"] == sorted(added), f"added mismatch: {actual['added']}"
    assert actual["removed"] == sorted(removed), f"removed mismatch: {actual['removed']}"
    assert actual["changed"] == sorted(changed), f"changed mismatch: {actual['changed']}"


def _no_git_overrides() -> None:
    bad = [n for n in GIT_ENV_OVERRIDES if os.environ.get(n)]
    assert not bad, f"unsafe inherited Git overrides: {bad}"


def _check_sources_intact(log: list[str]) -> None:
    head = subprocess.run(
        ["git", "-C", str(E4C_REPO), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True).stdout.strip()
    assert head == E4C_HEAD, f"e4c8269 fixture moved: {head}"
    tree = subprocess.run(
        ["git", "-C", str(E4C_REPO), "show", "-s", "--format=%T", "HEAD"],
        capture_output=True, text=True, check=True).stdout.strip()
    assert tree == E4C_TREE, f"e4c8269 tree moved: {tree}"
    bhead = subprocess.run(
        ["git", "-C", str(B_REPO), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True).stdout.strip()
    assert bhead == B_HEAD, f"B fixture moved: {bhead}"
    log.append(f"preserved e4c8269 HEAD/tree {head}/{tree}; B HEAD {bhead}")


def _check_edition(edition: Path, expect_head: str | None = None) -> dict:
    assert edition.is_dir(), f"edition missing: {edition}"
    assert edition.resolve() != E4C_REPO.resolve(), "refusing to touch e4c8269 fixture"
    assert edition.resolve() != B_REPO.resolve(), "refusing to touch B fixture"
    marker = edition / ".witness-edition-marker.json"
    assert marker.is_file(), f"edition marker missing: {marker}"
    meta = json.loads(marker.read_text())
    assert meta.get("e4c_source") == E4C_HEAD, "edition marker source mismatch"
    if expect_head is not None:
        head = _git(["rev-parse", "HEAD"], edition).stdout.strip()
        assert head == expect_head, f"edition HEAD {head} != expected {expect_head}"
    return meta


def _run_metadata(log: list[str], tag: str, edition: Path) -> None:
    try:
        import importlib.metadata as md
        deps = {d: md.version(d) for d in ("pypdf", "jsonschema")}
    except Exception as exc:
        deps = {"error": str(exc)[:200]}
    log.append(
        f"{tag} cmd={sys.argv} cwd={os.getcwd()} python={sys.version.split()[0]} "
        f"deps={deps} edition={edition} "
        f"supplement_sha={_sha(Path(__file__).resolve())} "
        f"orig_harness_sha={_sha(Path(__file__).resolve().parent / 'witness_harness.py')}"
    )


def _runtime_source(log: list[str], tag: str, edition: Path):
    import scripts.survey_production_v2 as core
    import scripts.survey_weekly_derivation_v2 as weekly
    core_path = Path(core.__file__).resolve()
    helper_path = Path(weekly.__file__).resolve()
    assert str(core_path).startswith(str(edition.resolve())), f"stale core source: {core_path}"
    assert str(helper_path).startswith(str(edition.resolve())), f"stale helper source: {helper_path}"
    head = _git(["rev-parse", "HEAD"], edition).stdout.strip()
    log.append(f"{tag} runtime core={core_path} helper={helper_path} "
               f"helper_sha={_sha(helper_path)} HEAD={head}")
    return core, weekly, head


# ---------------------------------------------------------------- s-commit (stdlib only)

def s_commit(args) -> int:
    logs = Path(args.logs)
    logs.mkdir(parents=True, exist_ok=True)
    sidecar = logs / f"s-commit-{args.marker}.sidecar.json"
    plog = logs / f"s-commit-{args.marker}.log"
    _require_fresh(sidecar)
    _require_fresh(plog)
    log: list[str] = []
    _no_git_overrides()
    _check_sources_intact(log)
    edition = Path(args.edition).resolve()
    _check_edition(edition, args.expect_head)
    _run_metadata(log, f"S-commit-{args.marker}", edition)
    helper = edition / HELPER_REL
    st_tracked = _git(["status", "--porcelain=v1", "--untracked-files=no"], edition, check=False).stdout
    assert st_tracked.strip() == "", f"tracked dirty before {args.marker}: {st_tracked[:500]}"
    assert _git(["diff", "--", HELPER_REL], edition).stdout.strip() == "", "helper unexpectedly dirty"
    pre = _sha(helper)
    helper.write_bytes(
        helper.read_bytes()
        + f"\n# witness-{args.marker}: mechanical identity comment only; no semantic change.\n".encode())
    post = _sha(helper)
    assert pre != post
    diff = _git(["diff", "--", HELPER_REL], edition).stdout
    assert args.marker in diff, diff[:1000]
    _git(["add", "--", HELPER_REL], edition)
    _git(["commit", "-q", "-m", f"Synthetic witness {args.marker} comment-only control change"], edition)
    head = _git(["rev-parse", "HEAD"], edition).stdout.strip()
    parent = _git(["log", "--format=%P", "-n", "1", "HEAD"], edition).stdout.strip()
    tree = _git(["show", "-s", "--format=%T", "HEAD"], edition).stdout.strip()
    stat = _git(["show", "--stat", "--oneline", "HEAD"], edition).stdout.strip()
    mods = sorted(m for m in sys.modules if m.split(".")[0] in ("scripts", "tests"))
    assert mods == [], f"runtime imports leaked into commit-only process: {mods}"
    log.append(f"{args.marker} head={head} parent={parent} tree={tree} helper_sha={post}\n--- diff ---\n{diff}\n--- stat ---\n{stat}")
    log.append("commit-only process imported no scripts/tests modules (stdlib + git metadata only)")
    _write_json(sidecar, {"phase": f"s-commit-{args.marker}", "run_id": args.run_id,
                          "marker": args.marker, "head": head, "parent": parent, "tree": tree,
                          "helper_sha": post, "diff": diff, "stat": stat})
    plog.write_text("\n".join(log) + "\n")
    print(f"S-commit-{args.marker} OK head={head}")
    return 0


# ------------------------------------------------------- s-db-checks (read-only)

def _ls_tree(repo: Path, rev: str, tops: list[str]) -> dict[str, tuple[str, str]]:
    proc = _git(["ls-tree", "-r", rev, "--", *tops], repo)
    out: dict[str, tuple[str, str]] = {}
    for line in proc.stdout.splitlines():
        if not line.strip():
            continue
        meta, name = line.split("\t", 1)
        mode, _typ, blob = meta.split(" ")
        out[name] = (mode, blob)
    return out


def s_db_checks(args) -> int:
    logs = Path(args.logs)
    logs.mkdir(parents=True, exist_ok=True)
    suffix = f"-{args.tag}" if getattr(args, "tag", None) else ""
    sidecar = logs / f"s-db-checks{suffix}.sidecar.json"
    plog = logs / f"s-db-checks{suffix}.log"
    _require_fresh(sidecar)
    _require_fresh(plog)
    log: list[str] = []
    _no_git_overrides()
    _check_sources_intact(log)
    edition = Path(args.edition).resolve()
    _check_edition(edition, args.expect_head)
    _run_metadata(log, "S-db-checks", edition)
    gitdir = Path(_git(["rev-parse", "--git-dir"], edition).stdout.strip())
    if not gitdir.is_absolute():
        gitdir = (edition / gitdir).resolve()
    commondir = Path(_git(["rev-parse", "--git-common-dir"], edition).stdout.strip())
    if not commondir.is_absolute():
        commondir = (edition / commondir).resolve()
    assert gitdir == commondir, f"split git dirs: {gitdir} vs {commondir}"
    alternates = gitdir / "objects" / "info" / "alternates"
    assert not alternates.exists(), f"shared object store: {alternates}"
    remote = _git(["remote", "-v"], edition).stdout
    assert args.expect_origin in remote, f"unexpected origin: {remote[:300]}"
    config = _git(["config", "--list", "--show-origin"], edition).stdout
    assert "alternate" not in config.lower(), "alternates/worktree config present"
    log.append(f"independent DB: gitdir==commondir={gitdir}; no alternates file; origin inert; no alternate config")
    e4_entries = _ls_tree(E4C_REPO, E4C_HEAD, COPY_TOPS)
    ed_entries = _ls_tree(edition, args.h0, COPY_TOPS)
    marker_name = ".witness-edition-marker.json"
    # NOTE: the marker lives at the repo root, outside COPY_TOPS, so the pathspec-filtered
    # ls-tree listing cannot contain it; its presence is already asserted by _check_edition.
    ed_cmp = {k: v for k, v in ed_entries.items() if k != marker_name}
    byte_compare_ok = (ed_cmp == e4_entries)
    log.append(f"content-byte compare vs exact e4c blobs over {COPY_TOPS}: "
               f"{'MATCH' if byte_compare_ok else 'MISMATCH'} "
               f"(edition {len(ed_cmp)} entries incl. marker excluded; e4c {len(e4_entries)} entries)")
    mismatches = []
    for name in sorted(set(ed_cmp) | set(e4_entries)):
        if ed_cmp.get(name) != e4_entries.get(name):
            mismatches.append({"path": name, "edition": list(ed_cmp.get(name) or []),
                               "e4c": list(e4_entries.get(name) or [])})
    if not byte_compare_ok:
        only_e4 = sorted(set(e4_entries) - set(ed_cmp))[:20]
        only_ed = sorted(set(ed_cmp) - set(e4_entries))[:20]
        log.append(f"only-in-e4c={only_e4} only-in-edition={only_ed}")
        for m in mismatches[:10]:
            log.append(f"blob/mode mismatch: {m['path']} edition={m['edition']} e4c={m['e4c']}")
    names = sorted(ed_cmp)
    sample = [names[i * len(names) // 12] for i in range(12)] if names else []
    inodes = []
    for rel in sample:
        st_e, st_s = os.stat(edition / rel), os.stat(E4C_REPO / rel)
        assert (st_e.st_dev, st_e.st_ino) != (st_s.st_dev, st_s.st_ino), f"shared inode: {rel}"
        assert st_e.st_nlink == 1 and st_s.st_nlink == 1, f"hardlink count: {rel}"
        inodes.append({"path": rel, "edition_nlink": st_e.st_nlink})
    log.append(f"inode/hardlink sample: {len(inodes)} files, distinct inodes, nlink==1 (no sharing)")
    _write_json(sidecar, {"phase": "s-db-checks", "run_id": args.run_id,
                          "gitdir": str(gitdir), "origin_ok": True,
                          "byte_compare_ok": byte_compare_ok,
                          "edition_entries": len(ed_cmp), "e4c_entries": len(e4_entries),
                          "mismatches": mismatches[:50], "mismatch_count": len(mismatches),
                          "inode_sample": inodes, "config": config})
    plog.write_text("\n".join(log) + "\n")
    print(f"S-db-checks OK byte_compare={byte_compare_ok}")
    return 0


# ------------------------------------------------- s-refresh-first / repeat

def _refresh_common(args, log: list[str], H, w0: dict, h_new: str, tag: str):
    import scripts.survey_production_v2 as core
    import scripts.survey_agent_control_v2 as agent
    import scripts.survey_weekly_derivation_v2 as weekly
    import scripts.survey_reader_surface_gate_v2 as reader_gate
    edition = Path(args.edition).resolve()
    base, _ = H.setup_base(edition)
    assert base.head == h_new, f"{tag}: HEAD {base.head} != {h_new}"
    state_path = base.root / w0["state_rel"]
    assert agent.validate_agent_state(base.root, base.cfg, core.load_json(state_path)) == []
    log.append(f"{tag} strict State passes at {h_new[:12]} (HEAD not pinned)")
    ctx0 = weekly.load_derivation(base.root, state_path, base.root / w0["hashes"]["authored"]["rel"])
    assert ctx0["surface"] == core.load_json(base.root / w0["hashes"]["surface"]["rel"])
    log.append(f"{tag} strict load_derivation passes; recomputed surface identical")
    receipt_path = base.root / w0["hashes"]["receipt"]["rel"]
    try:
        weekly.validate_receipt(base.root, receipt_path, state_path)
        raise AssertionError(f"{tag} old receipt unexpectedly replayed")
    except ValueError as exc:
        (Path(args.logs) / f"{tag.lower()}-old-receipt.err.txt").write_text(str(exc))
        assert ("implementation or contract changed" in str(exc) or "current-tool" in str(exc)
                or "differ from exact committed basis" in str(exc)), str(exc)[:500]
        log.append(f"{tag} old receipt rejects: {str(exc)[:200]}")
    gate_path = base.root / w0["hashes"]["gate"]["rel"]
    try:
        reader_gate.validate_reader_surface_gate(
            base.root, gate_path, issue_id=w0["issue"], publication_profile="WEEKLY_MAGAZINE",
            expected_manuscript_path=base.root / w0["hashes"]["manuscript"]["rel"], state_path=state_path)
        raise AssertionError(f"{tag} old Gate unexpectedly validated")
    except ValueError as exc:
        (Path(args.logs) / f"{tag.lower()}-old-gate.err.txt").write_text(str(exc))
        log.append(f"{tag} old Gate rejects: {str(exc)[:200]}")
    return base, state_path, receipt_path, gate_path


def s_refresh_first(args) -> int:
    import witness_harness as H
    from scripts import survey_production_v2 as core
    from scripts import survey_agent_control_v2 as agent
    from scripts import survey_schema_v2 as schema_gate
    from scripts import survey_weekly_derivation_v2 as weekly
    from scripts import survey_reader_surface_gate_v2 as reader_gate
    logs = Path(args.logs)
    sidecar = logs / "s-refresh-first.sidecar.json"
    plog = logs / "s-refresh-first.log"
    _require_fresh(sidecar)
    _require_fresh(plog)
    log: list[str] = []
    tag = "S1"
    _no_git_overrides()
    _check_sources_intact(log)
    edition = Path(args.edition).resolve()
    _check_edition(edition, args.expect_head)
    _run_metadata(log, tag, edition)
    core0, weekly0, _ = _runtime_source(log, tag, edition)
    assert core0 is core and weekly0 is weekly
    w0 = json.loads(Path(args.w0sidecar).read_text())
    h1 = args.expect_head
    base, state_path, receipt_path, gate_path = _refresh_common(args, log, H, w0, h1, tag)
    H.harness_preconditions(base, w0, log, tag)
    snap_pre = _snapshot(edition)
    old_bytes = receipt_path.read_bytes()
    (edition / ".witness-evidence").mkdir(exist_ok=True)
    (edition / ".witness-evidence" / "receipt-superseded-supplement.json").write_bytes(old_bytes)
    old_receipt = json.loads(old_bytes.decode())
    old_raw_sha = _sha(receipt_path)
    context = weekly.load_derivation(base.root, state_path, base.root / w0["hashes"]["authored"]["rel"])
    archived = base.source_root / "publication/v2/interactive-semantic-publication-input.json"
    assert archived.is_file() and _sha(archived) == _sha(base.root / w0["hashes"]["authored"]["rel"])
    receipt_context = dict(context)
    receipt_context["authored_path"] = archived
    receipt = weekly.build_receipt(
        base.root, receipt_context, base.root / w0["hashes"]["surface"]["rel"],
        base.root / w0["hashes"]["pretex_review"]["rel"],
        base.root / w0["hashes"]["main_tex"]["rel"],
        base.root / w0["hashes"]["references_bib"]["rel"],
        base.root / w0["hashes"]["style"]["rel"])
    assert receipt["current_tools"]["repository_commit_sha"] == h1
    assert receipt["production_state_basis"]["lifecycle_state"] == "VALIDATED_DRAFT"
    assert receipt["production_state_basis"]["historical_sha256"] == core.sha256_file(state_path)
    schema_gate.validate_instance(receipt, base.root / weekly.RECEIPT_SCHEMA, label="Weekly source receipt")
    core.write_json(receipt_path, receipt)
    snap_post_r = _snapshot(edition)
    _assert_delta(_delta(snap_pre, snap_post_r), [], [w0["hashes"]["receipt"]["rel"]])
    log.append(f"{tag} receipt write delta == receipt only")
    validated = weekly.validate_receipt(base.root, receipt_path, state_path)
    assert validated["current_tools"]["repository_commit_sha"] == h1
    assert validated["accepted_refs"] == old_receipt["accepted_refs"], "accepted refs changed"
    assert validated["authored_refs"] == old_receipt["authored_refs"], "authored refs changed"
    log.append(f"{tag} new receipt replays; accepted/authored refs identical to superseded receipt")
    proc = H.run_gate_cli(edition, w0["hashes"]["manuscript"]["rel"], w0["hashes"]["pretex_review"]["rel"],
                          state_path, w0["hashes"]["gate"]["rel"])
    (logs / "s1-gate-cli.out.txt").write_text(proc.stdout)
    (logs / "s1-gate-cli.err.txt").write_text(proc.stderr)
    (logs / "s1-gate-cli.exit").write_text(str(proc.returncode))
    assert proc.returncode == 0, proc.stderr[-2000:]
    gate_doc = reader_gate.validate_reader_surface_gate(
        base.root, gate_path, issue_id=w0["issue"], publication_profile="WEEKLY_MAGAZINE",
        expected_manuscript_path=base.root / w0["hashes"]["manuscript"]["rel"], state_path=state_path)
    assert gate_doc["status"] == "PASSED"
    assert gate_doc["derivation"]["receipt"] == {
        "path": w0["hashes"]["receipt"]["rel"], "sha256": core.sha256_file(receipt_path)}
    snap_post_g = _snapshot(edition)
    _assert_delta(_delta(snap_post_r, snap_post_g), [], [w0["hashes"]["gate"]["rel"]])
    log.append(f"{tag} Gate renewed via fixed CLI; write delta == gate only; derivation binds new receipt")
    errors = agent.validate_agent_state(base.root, base.cfg, core.load_json(state_path))
    assert errors, "strict State unexpectedly passes after Gate renewal"
    joined = "; ".join(errors)
    (logs / "s1-strict-drift.err.txt").write_text(joined)
    assert "reader-surface-gate" in joined or "artifact drift" in joined, joined[:600]
    pending = agent.built_checked_pending_publication_basis(base.root, base.cfg, state_path)
    assert len(pending.replacements) == 1 and pending.replacements[0][0] == "reader-surface-gate"
    log.append(f"{tag} strict drift + gate-only pending basis confirmed")
    recorded_at = core.iso_utc(datetime.now(timezone.utc))
    proc2 = H.run_revalidate_cli(edition, state_path, H.SYNTHETIC_REASON_FIRST,
                                 "synthetic-witness-harness", recorded_at)
    (logs / "s1-revalidate-cli.out.txt").write_text(proc2.stdout)
    (logs / "s1-revalidate-cli.err.txt").write_text(proc2.stderr)
    (logs / "s1-revalidate-cli.exit").write_text(str(proc2.returncode))
    assert proc2.returncode == 0, proc2.stderr[-2000:]
    r1_rel = json.loads(proc2.stdout)["revalidation_record"]
    r1_path = base.root / r1_rel
    r1 = core.load_json(r1_path)
    assert r1["reason_class"] == "REVIEWED_CORE_CHANGE" and r1["supersedes"] is None
    assert [r["name"] for r in r1["superseded_artifacts"]] == ["reader-surface-gate"]
    state = core.load_json(state_path)
    assert state["publication_revalidation_provenance"] == {"path": r1_rel, "sha256": _sha(r1_path)}
    assert agent.validate_agent_state(base.root, base.cfg, state) == []
    active, act_errors = agent.resolve_active_publication_revalidation(base.root, base.cfg, state)
    assert not act_errors and active is not None
    weekly.validate_receipt(base.root, receipt_path, state_path)
    reader_gate.validate_reader_surface_gate(
        base.root, gate_path, issue_id=w0["issue"], publication_profile="WEEKLY_MAGAZINE",
        expected_manuscript_path=base.root / w0["hashes"]["manuscript"]["rel"], state_path=state_path)
    snap_post_r1 = _snapshot(edition)
    _assert_delta(_delta(snap_post_g, snap_post_r1), [r1_rel], [w0["hashes"]["state"]["rel"]])
    log.append(f"{tag} r1 established; revalidation write delta == new record + State pointer")
    proc3 = H.run_revalidate_cli(edition, state_path, "no-op repeat", "synthetic-witness-harness",
                                 core.iso_utc(datetime.now(timezone.utc)))
    (logs / "s1-noop-repeat.out.txt").write_text(proc3.stdout)
    (logs / "s1-noop-repeat.err.txt").write_text(proc3.stderr)
    (logs / "s1-noop-repeat.exit").write_text(str(proc3.returncode))
    assert proc3.returncode != 0 and "already validates current bytes" in proc3.stderr
    log.append(f"{tag} no-op repeat refused (raw CLI logs saved regardless of outcome)")
    _write_json(sidecar, {"phase": "s-refresh-first", "run_id": args.run_id, "h1": h1,
                          "recorded_at": recorded_at, "r1_rel": r1_rel,
                          "r1_sha256": _sha(r1_path),
                          "receipt_new_sha256": core.sha256_file(receipt_path),
                          "receipt_old_raw_sha256": old_raw_sha,
                          "gate_new_sha256": core.sha256_file(gate_path)})
    plog.write_text("\n".join(log) + "\n")
    print(f"S1 OK r1={r1_rel}")
    return 0


def s_refresh_repeat(args) -> int:
    import witness_harness as H
    from scripts import survey_production_v2 as core
    from scripts import survey_agent_control_v2 as agent
    from scripts import survey_schema_v2 as schema_gate
    from scripts import survey_weekly_derivation_v2 as weekly
    from scripts import survey_reader_surface_gate_v2 as reader_gate
    logs = Path(args.logs)
    sidecar = logs / "s-refresh-repeat.sidecar.json"
    plog = logs / "s-refresh-repeat.log"
    _require_fresh(sidecar)
    _require_fresh(plog)
    log: list[str] = []
    tag = "S2"
    _no_git_overrides()
    _check_sources_intact(log)
    edition = Path(args.edition).resolve()
    _check_edition(edition, args.expect_head)
    _run_metadata(log, tag, edition)
    _runtime_source(log, tag, edition)
    w0 = json.loads(Path(args.w0sidecar).read_text())
    r1s = json.loads(Path(args.r1sidecar).read_text())
    h2 = args.expect_head
    base, state_path, receipt_path, gate_path = _refresh_common(args, log, H, w0, h2, tag)
    r1_path = base.root / r1s["r1_rel"]
    assert r1_path.read_bytes() and _sha(r1_path) == r1s["r1_sha256"], "r1 changed before repeat"
    vref = core.load_json(state_path)["checkpoint_provenance"]["validation"]
    assert _sha(base.root / vref["path"]) == w0["validation_checkpoint_sha256"], "checkpoint changed"
    H.harness_preconditions(base, w0, log, tag)
    snap_pre = _snapshot(edition)
    old_bytes = receipt_path.read_bytes()
    (edition / ".witness-evidence").mkdir(exist_ok=True)
    (edition / ".witness-evidence" / "receipt-superseded-repeat.json").write_bytes(old_bytes)
    old_receipt = json.loads(old_bytes.decode())
    context = weekly.load_derivation(base.root, state_path, base.root / w0["hashes"]["authored"]["rel"])
    archived = base.source_root / "publication/v2/interactive-semantic-publication-input.json"
    rctx = dict(context)
    rctx["authored_path"] = archived
    receipt = weekly.build_receipt(
        base.root, rctx, base.root / w0["hashes"]["surface"]["rel"],
        base.root / w0["hashes"]["pretex_review"]["rel"],
        base.root / w0["hashes"]["main_tex"]["rel"],
        base.root / w0["hashes"]["references_bib"]["rel"],
        base.root / w0["hashes"]["style"]["rel"])
    assert receipt["current_tools"]["repository_commit_sha"] == h2
    schema_gate.validate_instance(receipt, base.root / weekly.RECEIPT_SCHEMA, label="Weekly source receipt")
    core.write_json(receipt_path, receipt)
    snap_post_r = _snapshot(edition)
    _assert_delta(_delta(snap_pre, snap_post_r), [], [w0["hashes"]["receipt"]["rel"]])
    validated = weekly.validate_receipt(base.root, receipt_path, state_path)
    assert validated["accepted_refs"] == old_receipt["accepted_refs"]
    assert validated["authored_refs"] == old_receipt["authored_refs"]
    log.append(f"{tag} new receipt at H2 replays; refs identical")
    (edition / ".witness-evidence" / "gate-superseded-repeat.json").write_bytes(gate_path.read_bytes())
    proc = H.run_gate_cli(edition, w0["hashes"]["manuscript"]["rel"], w0["hashes"]["pretex_review"]["rel"],
                          state_path, w0["hashes"]["gate"]["rel"])
    (logs / "s2-gate-cli.out.txt").write_text(proc.stdout)
    (logs / "s2-gate-cli.err.txt").write_text(proc.stderr)
    (logs / "s2-gate-cli.exit").write_text(str(proc.returncode))
    assert proc.returncode == 0, proc.stderr[-2000:]
    reader_gate.validate_reader_surface_gate(
        base.root, gate_path, issue_id=w0["issue"], publication_profile="WEEKLY_MAGAZINE",
        expected_manuscript_path=base.root / w0["hashes"]["manuscript"]["rel"], state_path=state_path)
    snap_post_g = _snapshot(edition)
    _assert_delta(_delta(snap_post_r, snap_post_g), [], [w0["hashes"]["gate"]["rel"]])
    pending = agent.built_checked_pending_publication_basis(base.root, base.cfg, state_path)
    assert len(pending.replacements) == 1 and pending.replacements[0][0] == "reader-surface-gate"
    recorded_at = core.iso_utc(datetime.now(timezone.utc))
    proc2 = H.run_revalidate_cli(edition, state_path, H.SYNTHETIC_REASON_SECOND,
                                 "synthetic-witness-harness", recorded_at)
    (logs / "s2-revalidate-cli.out.txt").write_text(proc2.stdout)
    (logs / "s2-revalidate-cli.err.txt").write_text(proc2.stderr)
    (logs / "s2-revalidate-cli.exit").write_text(str(proc2.returncode))
    assert proc2.returncode == 0, proc2.stderr[-2000:]
    r2_rel = json.loads(proc2.stdout)["revalidation_record"]
    r2_path = base.root / r2_rel
    r2 = core.load_json(r2_path)
    assert r2["supersedes"] == {"path": r1s["r1_rel"], "sha256": _sha(r1_path)}
    assert r1_path.read_bytes() and _sha(r1_path) == r1s["r1_sha256"], "r1 mutated by r2"
    assert agent.validate_agent_state(base.root, base.cfg, core.load_json(state_path)) == []
    weekly.validate_receipt(base.root, receipt_path, state_path)
    reader_gate.validate_reader_surface_gate(
        base.root, gate_path, issue_id=w0["issue"], publication_profile="WEEKLY_MAGAZINE",
        expected_manuscript_path=base.root / w0["hashes"]["manuscript"]["rel"], state_path=state_path)
    snap_post_r2 = _snapshot(edition)
    _assert_delta(_delta(snap_post_g, snap_post_r2), [r2_rel], [w0["hashes"]["state"]["rel"]])
    log.append(f"{tag} r2={r2_rel} supersedes intact r1; chain bound; deltas exact")
    _write_json(sidecar, {"phase": "s-refresh-repeat", "run_id": args.run_id, "h2": h2,
                          "recorded_at": recorded_at, "r2_rel": r2_rel,
                          "r2_sha256": _sha(r2_path), "r1_unchanged": True})
    plog.write_text("\n".join(log) + "\n")
    print(f"S2 OK r2={r2_rel}")
    return 0


# ------------------------------------------------------------- s-negatives

def _records_listing(base) -> list[list[str]]:
    import scripts.survey_production_v2 as core
    pub = base.source_root / "publication" / "v2"
    return sorted([p.name, core.sha256_file(p)] for p in sorted(pub.glob("publication-surface-revalidation-*.json")))


def s_negatives(args) -> int:
    import witness_harness as H
    from scripts import survey_production_v2 as core
    from scripts import survey_agent_control_v2 as agent
    from scripts import survey_weekly_derivation_v2 as weekly
    from scripts import survey_reader_surface_gate_v2 as reader_gate
    from scripts import survey_reader_publication_v2 as reader_publication
    logs = Path(args.logs)
    sidecar = logs / "s-negatives.sidecar.json"
    plog = logs / "s-negatives.log"
    _require_fresh(sidecar)
    _require_fresh(plog)
    log: list[str] = []
    tag = "SN"
    _no_git_overrides()
    _check_sources_intact(log)
    edition = Path(args.edition).resolve()
    _check_edition(edition, args.expect_head)
    _run_metadata(log, tag, edition)
    _runtime_source(log, tag, edition)
    w0 = json.loads(Path(args.w0sidecar).read_text())
    base, _ = H.setup_base(edition)
    state_path = base.root / w0["state_rel"]
    head_now = _git(["rev-parse", "HEAD"], edition).stdout.strip()
    results: dict[str, dict[str, str]] = {}

    def invariants() -> dict:
        return {"state_sha": _sha(state_path), "records": _records_listing(base)}

    def run_case(name: str, rel: str, mutate, policy_label: str, runtime_fn, runtime_label: str) -> None:
        path = base.root / rel
        before_raw = path.read_bytes()
        base_snap = _snapshot(edition)
        inv0 = invariants()
        mutate(path)
        m1 = _snapshot(edition)
        assert m1 != base_snap, f"{name}: mutation produced no byte change"
        try:
            H.harness_preconditions(base, w0, log, f"{tag}-{name}")
            raise AssertionError(f"{name} harness precondition unexpectedly passed")
        except AssertionError as exc:
            if "scope drift" not in str(exc) and "criteria drift" not in str(exc):
                raise
            (logs / f"sneg-{name}-policy.err.txt").write_text(str(exc))
            log.append(f"{tag}-{name} harness-policy ({policy_label}) refuses pre-write")
        m2 = _snapshot(edition)
        assert _delta(m1, m2) == {"added": [], "removed": [], "changed": []}, f"{name}: write during policy refusal"
        try:
            runtime_fn()
            raise AssertionError(f"{name} runtime unexpectedly admitted")
        except Exception as exc:
            (logs / f"sneg-{name}-runtime.err.txt").write_text(f"{type(exc).__name__}: {exc}")
            log.append(f"{tag}-{name} runtime ({runtime_label}) refuses: {type(exc).__name__}: {str(exc)[:200]}")
            if name == "n3-criteria":
                assert "check family differs" in str(exc), str(exc)[:400]
        m2b = _snapshot(edition)
        assert _delta(m1, m2b) == {"added": [], "removed": [], "changed": []}, f"{name}: write during runtime refusal"
        assert invariants() == inv0, f"{name}: State/record listing changed during refusal"
        path.write_bytes(before_raw)
        m3 = _snapshot(edition)
        assert _delta(base_snap, m3) == {"added": [], "removed": [], "changed": []}, f"{name}: restore inexact"
        results[name] = {"restored": "exact"}
        log.append(f"{tag}-{name} restored byte-exact; State/records unchanged throughout")

    surface_rel = w0["hashes"]["surface"]["rel"]
    arch_rel = w0["hashes"]["architecture"]["rel"]
    contract_rel = CONTRACT_REL

    def mut_surface(path: Path) -> None:
        doc = core.load_json(path)
        doc["cover"]["headline"] = "Unreviewed replacement headline"
        core.write_json(path, doc)

    def mut_arch(path: Path) -> None:
        path.write_bytes(path.read_bytes() + b" ")

    def mut_contract(path: Path) -> None:
        doc = json.loads(path.read_bytes().decode())
        lane = doc["publication_profiles"]["WEEKLY_MAGAZINE"]["semantic"]
        assert NEW_CHECK_ID not in lane
        lane.append(NEW_CHECK_ID)
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True) + "\n")

    try:
        run_case("n1-surface", surface_rel, mut_surface, "scope byte-identity",
                 lambda: weekly.validate_receipt(base.root, base.root / w0["hashes"]["receipt"]["rel"], state_path),
                 "validate_receipt")
        run_case("n2-upstream", arch_rel, mut_arch, "scope byte-identity",
                 lambda: agent.built_checked_pending_publication_basis(base.root, base.cfg, state_path),
                 "pending-basis construction")
        def n3_runtime() -> None:
            reader_publication.validate_review_record(
                base.root, base.root / w0["hashes"]["semantic_review"]["rel"],
                expected_kind="SEMANTIC_EDITORIAL")
        run_case("n3-criteria", contract_rel, mut_contract, "criteria hash identity", n3_runtime,
                 "validate_review_record (unchanged review bytes, changed criteria)")
        state_before = state_path.read_bytes()
        base_snap = _snapshot(edition)
        inv0 = invariants()
        corrupted = core.load_json(state_path)
        ptr = corrupted.get("publication_revalidation_provenance")
        assert isinstance(ptr, dict), "negatives need an established pointer; run after refresh"
        corrupted["publication_revalidation_provenance"]["sha256"] = "0" * 64
        core.write_json(state_path, corrupted)
        m1 = _snapshot(edition)
        assert m1 != base_snap, "n4: mutation produced no byte change"
        try:
            agent.built_checked_pending_publication_basis(base.root, base.cfg, state_path)
            raise AssertionError("n4 unexpectedly admitted")
        except agent.AgentControlError as exc:
            (logs / "sneg-n4-predecessor-runtime.err.txt").write_text(str(exc))
            assert "predecessor invalid" in str(exc), str(exc)[:400]
            log.append(f"{tag}-n4 runtime refuses malformed predecessor: {str(exc)[:200]}")
        m2b = _snapshot(edition)
        assert _delta(m1, m2b) == {"added": [], "removed": [], "changed": []}, "n4: write during refusal"
        assert invariants() == {"state_sha": _sha(state_path), "records": inv0["records"]}, \
            "n4: record listing changed during refusal"
        state_path.write_bytes(state_before)
        m3 = _snapshot(edition)
        assert _delta(base_snap, m3) == {"added": [], "removed": [], "changed": []}, "n4: restore inexact"
        results["n4-predecessor"] = {"restored": "exact"}
        log.append(f"{tag}-n4 restored byte-exact; pointer intact")
    finally:
        try:
            assert agent.validate_agent_state(base.root, base.cfg, core.load_json(state_path)) == []
            log.append(f"{tag} strict State passes after all restores")
        except Exception as exc:
            log.append(f"{tag} POST-RESTORE STRICT FAILURE: {exc}")
            raise
    assert _git(["rev-parse", "HEAD"], edition).stdout.strip() == head_now
    # Labeled dirty-config observation (read-only): what does strict validation report while
    # the criteria contract is dirty? Recorded separately; NOT claimed as a refresh-scope guard.
    contract_path = base.root / contract_rel
    contract_before = contract_path.read_bytes()
    doc = json.loads(contract_before.decode())
    doc["publication_profiles"]["WEEKLY_MAGAZINE"]["semantic"].append(NEW_CHECK_ID)
    contract_path.write_text(json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    try:
        dirty_errors = agent.validate_agent_state(base.root, base.cfg, core.load_json(state_path))
        (logs / "sneg-n3-dirty-config-observation.txt").write_text("; ".join(dirty_errors) or "[]")
        log.append(f"{tag}-n3 dirty-config strict-State observation (labeled separately): "
                   f"{('; '.join(dirty_errors))[:300] or '[]'}")
    finally:
        contract_path.write_bytes(contract_before)
    assert _sha(contract_path) == hashlib.sha256(contract_before).hexdigest()
    log.append(f"{tag} HEAD unchanged {head_now[:12]}; negatives created no State/record authority")
    _write_json(sidecar, {"phase": "s-negatives", "run_id": args.run_id, "head": head_now,
                          "cases": sorted(results), "new_check_id": NEW_CHECK_ID})
    plog.write_text("\n".join(log) + "\n")
    print("SN OK 4 instrumented negatives refused, all restored byte-exact")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["s-commit", "s-db-checks", "s-refresh-first",
                                          "s-refresh-repeat", "s-negatives"])
    parser.add_argument("--edition", required=True)
    parser.add_argument("--logs", required=True)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--exit-file", default=None)
    parser.add_argument("--marker", default=None)
    parser.add_argument("--expect-head", default=None)
    parser.add_argument("--w0sidecar", default=None)
    parser.add_argument("--r1sidecar", default=None)
    parser.add_argument("--h0", default=None)
    parser.add_argument("--tag", default=None)
    parser.add_argument("--expect-origin", default="https://example.invalid/witness-edition.git")
    args = parser.parse_args()
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    sys.path.insert(0, str(Path(args.edition).resolve()))
    table = {"s-commit": s_commit, "s-db-checks": s_db_checks,
             "s-refresh-first": s_refresh_first, "s-refresh-repeat": s_refresh_repeat,
             "s-negatives": s_negatives}
    try:
        code = table[args.phase](args)
    except Exception:
        code = 3
        raise
    finally:
        if args.exit_file:
            Path(args.exit_file).write_text(str(code if "code" in dir() else 3))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
