#!/usr/bin/env python3
"""DM021-P1 correction4 CLOSEOUT read-only verification (NEW, 2026-10-12T121721Z).

Read-only only: no DB writes, no recopy/cp, no checkout/apply/add/reset,
no index mutation, no network, no test execution, no subagents.
Reads ACTIVE + COPY + WORKSPACE git state, hashes 13 overlay paths,
walks all .git files for (dev,ino)/nlink/symlink separation, checks
alternates/remotes/index-empty, compares CURRENT to saved freeze-pre/post
full raw (not just named_status filter). Writes ONLY to its own CLOSEOUT
dir with exclusive O_EXCL creation.

Active: /tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z/candidate-partial-b40de60
Copy:   /tmp/opencode/jgas-dm021p1-R2-verify-20261012T072355Z/candidate-partial-b40de60
Workspace: /home/eariver/git/reconstruct-japanese-generative-ai-survey (.git only read)
"""
from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

ACTIVE = Path("/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z/candidate-partial-b40de60")
COPY = Path("/tmp/opencode/jgas-dm021p1-R2-verify-20261012T072355Z/candidate-partial-b40de60")
WORKSPACE = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
EVID = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey"
            "/notes/rephase-1-dm021-p1/evidence-20261012T072355Z-correction4")
CLOSEOUT = EVID / "closeout-20261012T121721Z"
FREEZE_PRE = EVID / "freeze-pre.json"
FREEZE_POST = EVID / "freeze-post.json"
PATCH = EVID / "complete-p1-correction-13path.patch"
PATCH_SHA = EVID / "complete-p1-correction-13path.sha256"

EXPECTED_MODIFIED = [
    "schemas/reader-surface-gate-v2.schema.json",
    "schemas/reader-surface-semantic-review-v2.schema.json",
    "scripts/survey_reader_surface_gate_v2.py",
]
EXPECTED_NEW = [
    "schemas/editorial-correction-proposal-v2.schema.json",
    "schemas/longform-publication-source-manifest-v2.schema.json",
    "schemas/longform-reader-input-v2.schema.json",
    "scripts/survey_editorial_correction_proposal_v2.py",
    "scripts/survey_longform_derivation_v2.py",
    "scripts/survey_longform_generated_v2.py",
    "scripts/survey_longform_semantic_publication_v2.py",
    "tests/test_survey_editorial_correction_proposal_v2.py",
    "tests/test_survey_longform_derivation_v2.py",
    "tests/test_survey_longform_publication_integration_v2.py",
]
EXPECTED_ROWS = sorted([f" M {p}" for p in EXPECTED_MODIFIED] + [f"?? {p}" for p in EXPECTED_NEW])
FORCED_GIT = {"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file"}


def sanitized_env() -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(FORCED_GIT)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def git_readonly(repo: Path, *args: str) -> subprocess.CompletedProcess:
    # Read-only git verbs only; caller never passes write verbs.
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, env=sanitized_env())


def xwrite_text(path: Path, text: str) -> None:
    with open(path, "x", encoding="utf-8") as fh:
        fh.write(text)


def named_status_filter(status_text: str) -> list[str]:
    # Exact replica of run_final.py named_status (100-108): filters to expected13.
    rows: list[str] = []
    for line in status_text.splitlines():
        for exp in EXPECTED_ROWS:
            if line == exp:
                rows.append(line)
                break
    return sorted(rows)


def repo_state(repo: Path, label: str, out: dict) -> dict:
    d: dict = {"label": label, "path": str(repo), "exists": repo.is_dir()}
    if not repo.is_dir():
        out["errors"].append(f"{label} missing: {repo}")
        return d
    for name, argv in (
        ("head", ("rev-parse", "HEAD")),
        ("tree", ("rev-parse", "HEAD^{tree}")),
        ("status", ("status", "--porcelain")),
        ("cached", ("diff", "--cached", "--name-only")),
        ("config", ("config", "--list", "--show-origin")),
    ):
        p = git_readonly(repo, *argv)
        d[name + "_rc"] = p.returncode
        d[name] = p.stdout if name in ("status", "cached", "config") else p.stdout.strip()
        d[name + "_stderr"] = p.stderr[:500]
        if p.returncode != 0:
            out["errors"].append(f"{label} git {' '.join(argv)} rc={p.returncode}")
    # alternates (read-only existence check)
    alt = repo / ".git" / "objects" / "info" / "alternates"
    d["alternates_exists"] = alt.exists()
    try:
        d["alternates_target"] = os.readlink(alt) if alt.is_symlink() else None
    except OSError:
        d["alternates_target"] = "UNREADABLE"
    return d


def hash_13(repo: Path) -> dict:
    files: dict = {}
    for rel in EXPECTED_MODIFIED + EXPECTED_NEW:
        full = repo / rel
        try:
            data = full.read_bytes()
            files[rel] = {
                "sha256": hashlib.sha256(data).hexdigest(),
                "mode": oct(stat.S_IMODE(full.lstat().st_mode)),
                "bytes": len(data),
            }
        except OSError as exc:
            files[rel] = {"error": f"{type(exc).__name__}: {exc}"}
    return files


def walk_git_files(repo: Path) -> dict:
    """Walk ENTIRE .git (read-only lstat), collect (dev,ino)->paths, nlink>1, symlinks."""
    gitdir = repo / ".git"
    entries: list[dict] = []
    ino_map: dict[tuple[int, int], list[str]] = {}
    symlinks: list[str] = []
    nlink_gt1: list[dict] = []
    count = 0
    if not gitdir.is_dir():
        return {"gitdir_exists": False, "count": 0, "entries": [], "symlinks": [], "nlink_gt1": []}
    for root, _dirs, files in os.walk(gitdir, followlinks=False):
        for name in files:
            fp = Path(root) / name
            try:
                st = fp.lstat()
            except OSError:
                continue
            count += 1
            rel = str(fp.relative_to(repo))
            if fp.is_symlink():
                try:
                    tgt = os.readlink(fp)
                except OSError:
                    tgt = "UNREADABLE"
                symlinks.append(f"{rel} -> {tgt}")
                # also stat target dev/ino for info (read-only)
                try:
                    rst = fp.stat()
                    key = (rst.st_dev, rst.st_ino)
                except OSError:
                    key = None
            else:
                key = (st.st_dev, st.st_ino)
                if st.st_nlink > 1:
                    nlink_gt1.append({"path": rel, "dev": st.st_dev, "ino": st.st_ino, "nlink": st.st_nlink})
            if key is not None:
                ino_map.setdefault(key, []).append(rel)
    return {"gitdir_exists": True, "count": count, "ino_map_keys": len(ino_map),
            "ino_map": {f"{k[0]}:{k[1]}": v for k, v in ino_map.items()},
            "symlinks": sorted(symlinks), "nlink_gt1": nlink_gt1}


def main() -> int:
    # Exclusivity: refuse if outputs exist; never overwrite.
    for name in ("verify-current.raw.log", "verify-current.json"):
        if (CLOSEOUT / name).exists():
            print(f"REFUSAL: output exists: {name}", flush=True)
            return 40
    if not CLOSEOUT.is_dir():
        print(f"REFUSAL: closeout dir missing: {CLOSEOUT}", flush=True)
        return 40
    out: dict = {"errors": [], "checks": {}}
    lines: list[str] = []
    lines.append("DM021-P1 correction4 CLOSEOUT read-only verification 20261012T121721Z")
    lines.append(f"active={ACTIVE}")
    lines.append(f"copy={COPY}")
    lines.append(f"workspace={WORKSPACE}")

    # 0. Saved freeze/patch identity (read-only reads of evidence, no source mutation).
    try:
        pre = json.loads(FREEZE_PRE.read_text(encoding="utf-8"))
        post = json.loads(FREEZE_POST.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"REFUSAL: freeze unreadable: {exc}", flush=True)
        return 40
    out["checks"]["saved_pre_eq_post_full"] = (pre == post)
    out["checks"]["saved_pre_status_eq_post_status_full_raw"] = (pre["status"] == post["status"])
    out["checks"]["saved_pre_status_is_exact13_full_raw"] = (
        sorted(pre["status"].splitlines()) == EXPECTED_ROWS and len(pre["status"].splitlines()) == 13)
    lines.append(f"saved pre==post full: {pre == post}")
    lines.append(f"saved pre.status==post.status full raw: {pre['status'] == post['status']}")
    lines.append(f"saved pre.status exact13 lines: {sorted(pre['status'].splitlines()) == EXPECTED_ROWS}")
    # named_status limitation demonstration (code fact, no mutation).
    lines.append("NOTE run_final.named_status (lines 100-108) FILTERS to expected13:")
    lines.append("  for line in status: for exp in EXPECTED_ROWS: if line==exp: keep.")
    lines.append("  It does NOT reject unrelated rows; extra rows would be silently ignored.")
    lines.append(f"  Currently saved raw is exact13, so filtered==full ({len(named_status_filter(pre['status']))} rows).")
    lines.append("  This verification compares FULL raw, but does NOT certify a closed reject predicate.")
    out["checks"]["named_status_filtered_count_saved"] = len(named_status_filter(pre["status"]))
    # Patch identity (read-only).
    try:
        patch_bytes = PATCH.read_bytes()
        patch_sha_actual = hashlib.sha256(patch_bytes).hexdigest()
        patch_sha_file = PATCH_SHA.read_text(encoding="utf-8").strip()
        patch_text = patch_bytes.decode("utf-8", errors="replace")
        diff_count = patch_text.count("diff --git ")
    except OSError as exc:
        out["errors"].append(f"patch unreadable: {exc}")
        patch_sha_actual = patch_sha_file = ""
        diff_count = -1
    out["checks"]["patch_sha256_actual"] = patch_sha_actual
    out["checks"]["patch_sha256_file"] = patch_sha_file
    out["checks"]["patch_diff_count"] = diff_count
    out["checks"]["patch_bytes"] = len(patch_bytes) if "patch_bytes" in dir() else -1
    lines.append(f"patch sha256(actual)={patch_sha_actual}")
    lines.append(f"patch sha file={patch_sha_file}")
    lines.append(f"patch diff --git count={diff_count} bytes={len(patch_bytes)}")

    # 1. Repo states (read-only git).
    active_st = repo_state(ACTIVE, "active", out)
    copy_st = repo_state(COPY, "copy", out)
    ws_st = repo_state(WORKSPACE, "workspace", out)
    out["active"] = active_st
    out["copy"] = copy_st
    out["workspace"] = ws_st
    for st in (active_st, copy_st, ws_st):
        lines.append(f"--- {st['label']} ---")
        for k in ("head", "tree", "cached", "alternates_exists"):
            lines.append(f"  {k}={repr(st.get(k))[:300]}")
        lines.append(f"  status_rc={st.get('status_rc')} status_bytes={len(st.get('status',''))}")
        for ln in (st.get("status","").splitlines()):
            lines.append(f"    |{ln}")
        cfg = st.get("config","")
        lines.append(f"  config_rc={st.get('config_rc')} inert_example_invalid={'example.invalid' in cfg}")
        # show only remote/origin lines to keep log small but sufficient
        for ln in cfg.splitlines():
            if "remote" in ln.lower() or "url" in ln.lower() or "example.invalid" in ln:
                lines.append(f"    cfg:{ln[:250]}")

    # 2. HEAD/tree/status/index expectations (CURRENT vs saved freeze).
    out["checks"]["active_head_is_409"] = (active_st.get("head") == "409b292756dd1277b9dfae87679934c0d2ce251c")
    out["checks"]["active_tree_is_8ce"] = (active_st.get("tree") == "8ce3699861505f32d1d60bdc185d4d4f635aedb2")
    out["checks"]["copy_head_is_409"] = (copy_st.get("head") == "409b292756dd1277b9dfae87679934c0d2ce251c")
    out["checks"]["copy_tree_is_8ce"] = (copy_st.get("tree") == "8ce3699861505f32d1d60bdc185d4d4f635aedb2")
    out["checks"]["active_status_full_eq_freeze_pre"] = (active_st.get("status") == pre["status"])
    out["checks"]["copy_status_full_eq_freeze_pre"] = (copy_st.get("status") == pre["status"])
    out["checks"]["active_cached_empty"] = (active_st.get("cached","").strip() == "")
    out["checks"]["copy_cached_empty"] = (copy_st.get("cached","").strip() == "")
    out["checks"]["active_no_alternates"] = (active_st.get("alternates_exists") is False)
    out["checks"]["copy_no_alternates"] = (copy_st.get("alternates_exists") is False)
    out["checks"]["active_inert"] = ("example.invalid" in active_st.get("config",""))
    out["checks"]["copy_inert"] = ("example.invalid" in copy_st.get("config",""))
    for k, v in out["checks"].items():
        if k.startswith(("active_","copy_")):
            lines.append(f"check {k}={v}")

    # 3. 13-file hashes CURRENT vs freeze-pre (capture-at-run pins, not static preknown).
    active_files = hash_13(ACTIVE)
    copy_files = hash_13(COPY)
    out["active_files"] = active_files
    out["copy_files"] = copy_files
    out["checks"]["active_13_eq_freeze_pre"] = (active_files == pre["files"])
    out["checks"]["copy_13_eq_freeze_pre"] = (copy_files == pre["files"])
    lines.append(f"check active_13_eq_freeze_pre={active_files == pre['files']}")
    lines.append(f"check copy_13_eq_freeze_pre={copy_files == pre['files']}")
    if active_files != pre["files"]:
        for k in active_files:
            if active_files[k] != pre["files"].get(k):
                lines.append(f"  MISMATCH active {k}: current={active_files[k]} freeze={pre['files'].get(k)}")
                out["errors"].append(f"active 13 mismatch: {k}")
    if copy_files != pre["files"]:
        for k in copy_files:
            if copy_files[k] != pre["files"].get(k):
                lines.append(f"  MISMATCH copy {k}: current={copy_files[k]} freeze={pre['files'].get(k)}")
                out["errors"].append(f"copy 13 mismatch: {k}")
    lines.append("NOTE pins are capture-at-run pre vs post, not independent static preknown hashes;")
    lines.append("  CURRENT match proves no drift since run, not retroactive static proof.")
    # List all 13 current hashes for return.
    for rel in EXPECTED_MODIFIED + EXPECTED_NEW:
        lines.append(f"  file {rel} active={active_files.get(rel)} copy={copy_files.get(rel)}")

    # 4. Full-object separation: walk ENTIRE .git for all three DBs.
    active_walk = walk_git_files(ACTIVE)
    copy_walk = walk_git_files(COPY)
    ws_walk = walk_git_files(WORKSPACE)
    out["active_git_count"] = active_walk["count"]
    out["copy_git_count"] = copy_walk["count"]
    out["workspace_git_count"] = ws_walk["count"]
    out["active_symlinks"] = active_walk["symlinks"]
    out["copy_symlinks"] = copy_walk["symlinks"]
    out["workspace_symlinks_count"] = len(ws_walk["symlinks"])
    out["active_nlink_gt1"] = active_walk["nlink_gt1"]
    out["copy_nlink_gt1"] = copy_walk["nlink_gt1"]
    out["workspace_nlink_gt1_count"] = len(ws_walk["nlink_gt1"])
    lines.append(f"git file counts: active={active_walk['count']} copy={copy_walk['count']} workspace={ws_walk['count']}")
    lines.append(f"symlinks: active={len(active_walk['symlinks'])} copy={len(copy_walk['symlinks'])} workspace_sym={len(ws_walk['symlinks'])}")
    for s in active_walk["symlinks"][:20]:
        lines.append(f"  active symlink: {s}")
    for s in copy_walk["symlinks"][:20]:
        lines.append(f"  copy symlink: {s}")
    lines.append(f"nlink>1: active={len(active_walk['nlink_gt1'])} copy={len(copy_walk['nlink_gt1'])} workspace={len(ws_walk['nlink_gt1'])}")
    # Pairwise (dev,ino) intersection across ALL .git files.
    a_keys = set(active_walk["ino_map"].keys())
    c_keys = set(copy_walk["ino_map"].keys())
    w_keys = set(ws_walk["ino_map"].keys())
    ac_shared = sorted(a_keys & c_keys)
    aw_shared = sorted(a_keys & w_keys)
    cw_shared = sorted(c_keys & w_keys)
    out["checks"]["shared_active_copy_count"] = len(ac_shared)
    out["checks"]["shared_active_workspace_count"] = len(aw_shared)
    out["checks"]["shared_copy_workspace_count"] = len(cw_shared)
    out["shared_active_copy"] = [{"key": k, "active_paths": active_walk["ino_map"][k], "copy_paths": copy_walk["ino_map"][k]} for k in ac_shared[:20]]
    lines.append(f"shared (dev,ino) active&copy={len(ac_shared)} active&workspace={len(aw_shared)} copy&workspace={len(cw_shared)}")
    for k in ac_shared[:10]:
        lines.append(f"  SHARED A&C {k}: active={active_walk['ino_map'][k]} copy={copy_walk['ino_map'][k]}")
    for k in aw_shared[:10]:
        lines.append(f"  SHARED A&W {k}: active={active_walk['ino_map'][k]} ws={ws_walk['ino_map'][k]}")
    for k in cw_shared[:10]:
        lines.append(f"  SHARED C&W {k}: copy={copy_walk['ino_map'][k]} ws={ws_walk['ino_map'][k]}")
    if ac_shared or aw_shared or cw_shared:
        out["errors"].append("object sharing detected (see shared lists)")
    # Prior HEAD-only check insufficiency note + current HEAD inode detail.
    try:
        import os as _os
        a_head = _os.lstat(ACTIVE / ".git" / "HEAD")
        c_head = _os.lstat(COPY / ".git" / "HEAD")
        out["checks"]["head_inodes_differ"] = ((a_head.st_ino, a_head.st_dev) != (c_head.st_ino, c_head.st_dev))
        lines.append(f"HEAD inodes differ (prior narrow check): {(a_head.st_ino, a_head.st_dev) != (c_head.st_ino, c_head.st_dev)}")
        lines.append(f"  active HEAD dev={a_head.st_dev} ino={a_head.st_ino} nlink={a_head.st_nlink}")
        lines.append(f"  copy HEAD dev={c_head.st_dev} ino={c_head.st_ino} nlink={c_head.st_nlink}")
        lines.append("NOTE prior proof_apply.py compared ONLY .git/HEAD inode; this closeout compares ALL .git files.")
    except OSError as exc:
        out["errors"].append(f"HEAD lstat failed: {exc}")

    # 5. Overall.
    ok = (len(out["errors"]) == 0
          and out["checks"].get("active_13_eq_freeze_pre") is True
          and out["checks"].get("copy_13_eq_freeze_pre") is True
          and out["checks"].get("active_status_full_eq_freeze_pre") is True
          and out["checks"].get("copy_status_full_eq_freeze_pre") is True
          and out["checks"].get("shared_active_copy_count") == 0
          and out["checks"].get("shared_active_workspace_count") == 0
          and out["checks"].get("shared_copy_workspace_count") == 0)
    out["verdict"] = "CLOSEOUT_CURRENT_MATCH" if ok else "CLOSEOUT_MISMATCH_OR_SHARING"
    lines.append(f"verdict={out['verdict']} errors={out['errors']}")
    lines.append("SCOPE: current-state verification only; not retroactive per-run proof; no tests rerun; no source verdict.")

    raw = "\n".join(lines) + "\n"
    print(raw, end="", flush=True)
    # Exclusive writes only to CLOSEOUT.
    xwrite_text(CLOSEOUT / "verify-current.raw.log", raw)
    xwrite_text(CLOSEOUT / "verify-current.json", json.dumps(out, indent=1) + "\n")
    return 0 if ok else 30


if __name__ == "__main__":
    sys.exit(main())
