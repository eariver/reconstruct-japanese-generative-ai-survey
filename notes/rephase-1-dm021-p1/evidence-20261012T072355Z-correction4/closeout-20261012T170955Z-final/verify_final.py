#!/usr/bin/env python3
"""DM021-P1 correction4 FINAL read-only availability/identity verification.

NEW script, 2026-10-12T170955Z. Read-only only: no DB/index/worktree writes,
no recopy, no checkout/apply/add/reset, no cache cleanup, no commits, no test
run, no source import, no network. Reads ACTIVE + COPY + WORKSPACE git state,
hashes 13 overlay paths, lstat-walks every .git entry INCLUDING directories
(fails on any traversal/stat error or symlink), checks nlink and cross-repo
(dev,ino) sharing, rejects alternates, inspects EXACT remote/pushurl/rewrite
keys (no substring predicate). Writes ONLY inside its own CLOSEOUT dir with
exclusive O_EXCL creation. Explicit explicit-error failures only; no assert
statements anywhere (safe under optimized mode).
"""

from __future__ import annotations

import datetime
import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

STAMP = "20261012T170955Z"
ACTIVE = Path("/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z/candidate-partial-b40de60")
COPY = Path("/tmp/opencode/jgas-dm021p1-R2-verify-20261012T072355Z/candidate-partial-b40de60")
WORKSPACE = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
EVID = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey"
            "/notes/rephase-1-dm021-p1/evidence-20261012T072355Z-correction4")
CLOSEOUT = EVID / "closeout-20261012T170955Z-final"
FREEZE_PRE = EVID / "freeze-pre.json"
FREEZE_POST = EVID / "freeze-post.json"
PATCH = EVID / "complete-p1-correction-13path.patch"
PATCH_SHA_FILE = EVID / "complete-p1-correction-13path.sha256"
CONTRACT = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey"
                "/outputs/rephase-1-dm021-contract-decision.md")

HEAD409 = "409b292756dd1277b9dfae87679934c0d2ce251c"
TREE8CE = "8ce3699861505f32d1d60bdc185d4d4f635aedb2"
PATCH_SHA = "85e9d9ab3c972a786afb1cf2f941bf4dbcfd4980f2e63d0ad9cf6df3cb55963c"
CONTRACT_SHA = "07e899901f488b256ca846c62b1a1fab3edadc880f34593a38078412aeb3c661"

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
INERT_URL = "https://example.invalid/rephase-candidate-recovery.git"
WORKSPACE_URL = "https://github.com/eariver/reconstruct-japanese-generative-ai-survey.git"

RAW_NAME = f"verify-final-{STAMP}-corrected.raw.log"
JSON_NAME = f"verify-final-{STAMP}-corrected.json"


def fail(msg):
    print(f"VERIFY_REFUSAL: {msg}", flush=True)
    return 40


def xwrite_text(path, text):
    with open(path, "x", encoding="utf-8") as fh:
        fh.write(text)


def sanitized_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(FORCED_GIT)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def git_ro(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, env=sanitized_env())


def utcnow():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def walk_git_strict(repo, errors):
    """lstat EVERY entry under .git including directories. Fail on any error/symlink.

    Returns dict with counts and (dev,ino)->paths for regular files. Appends to
    errors on any traversal/stat failure or symlink presence (no silent skips).
    """
    gitdir = repo / ".git"
    result = {"gitdir_exists": False, "entries_total": 0, "dirs": 0, "files": 0,
              "other": 0, "symlinks": [], "nlink_bad": [], "stat_errors": [],
              "ino_map": {}}
    if not gitdir.is_dir():
        errors.append(f"{repo}: .git missing")
        return result
    result["gitdir_exists"] = True
    try:
        top_st = os.lstat(gitdir)
    except OSError as exc:
        errors.append(f"{repo}: lstat .git failed: {exc}")
        result["stat_errors"].append(".git")
        return result
    if stat.S_ISLNK(top_st.st_mode):
        errors.append(f"{repo}: .git itself is a symlink")
        result["symlinks"].append(".git")
        return result
    stack = [gitdir]
    while stack:
        cur = stack.pop()
        try:
            with os.scandir(cur) as it:
                entries = list(it)
        except OSError as exc:
            errors.append(f"{repo}: scandir failed {cur}: {exc}")
            result["stat_errors"].append(str(cur))
            continue
        for de in entries:
            try:
                st = de.stat(follow_symlinks=False)
            except OSError as exc:
                errors.append(f"{repo}: lstat failed {de.path}: {exc}")
                result["stat_errors"].append(de.path)
                continue
            result["entries_total"] += 1
            if stat.S_ISLNK(st.st_mode):
                errors.append(f"{repo}: symlink entry {de.path}")
                result["symlinks"].append(de.path)
                continue
            if stat.S_ISDIR(st.st_mode):
                result["dirs"] += 1
                stack.append(Path(de.path))
            elif stat.S_ISREG(st.st_mode):
                result["files"] += 1
                if st.st_nlink != 1:
                    errors.append(f"{repo}: nlink!=1 {de.path} nlink={st.st_nlink}")
                    result["nlink_bad"].append({"path": de.path, "nlink": st.st_nlink})
                key = f"{st.st_dev}:{st.st_ino}"
                result["ino_map"].setdefault(key, []).append(de.path)
            else:
                result["other"] += 1
                errors.append(f"{repo}: non-regular non-dir entry {de.path}")
    return result


def parse_config_exact(config_text):
    """Parse `git config --list --show-origin` into exact key/value records.

    Line format is `<origin>\\t<key>=<value>` (e.g.
    `file:.git/config\\tremote.origin.url=https://...`). Split origin from the
    rest on the FIRST tab, then key from value on the FIRST `=`. Records keep
    their origin so repo-local keys (`file:.git/config*`) can be evaluated
    strictly while global/system keys are recorded separately (informational).
    """
    records = []
    for line in config_text.splitlines():
        if "\t" not in line:
            records.append({"raw": line[:250], "origin": None, "key": None, "value": None})
            continue
        origin, kv = line.split("\t", 1)
        if "=" not in kv:
            records.append({"raw": line[:250], "origin": origin, "key": None, "value": None})
            continue
        key, value = kv.split("=", 1)
        records.append({"origin": origin, "key": key, "value": value})
    return records


def check_remote_exact(label, records, remote_out, errors, lines):
    """Exact remote/pushurl/rewrite allowlist check (no substring predicate).

    ACTIVE/COPY: exactly one remote (origin) whose url AND effective push
    destination are exactly INERT_URL; no pushurl override; no url.insteadOf /
    pushInsteadOf rewrites; no include.* indirection; no http_proxy routing keys.
    WORKSPACE: origin url exactly WORKSPACE_URL (recorded, same strict shape).
    Strict evaluation covers repo-local origins (`file:.git/config*`) only;
    global/system origins (e.g. `/home/eariver/.gitconfig` credential/user keys)
    are recorded separately as informational and never satisfy the allowlist.
    """
    local = [r for r in records if (r.get("origin") or "").startswith("file:.git/config")]
    other_origins = sorted({r.get("origin") for r in records if not (r.get("origin") or "").startswith("file:.git/config")})
    lines.append(f"  {label} non_repo_config_origins={other_origins}")
    by_key = {}
    for r in local:
        if r.get("key"):
            by_key.setdefault(r["key"], []).append(r["value"])
    remote_urls = by_key.get("remote.origin.url", [])
    pushurls = by_key.get("remote.origin.pushurl", [])
    lines.append(f"  {label} remote.origin.url={remote_urls}")
    lines.append(f"  {label} remote.origin.pushurl={pushurls}")
    rewrite_keys = [k for k in by_key if k.startswith("url.") and (k.endswith(".insteadOf") or k.endswith(".pushInsteadOf"))]
    lines.append(f"  {label} rewrite_keys={rewrite_keys}")
    include_keys = [k for k in by_key if k.startswith("include")]
    lines.append(f"  {label} include_keys={include_keys}")
    proxy_keys = [k for k in by_key if k.startswith("http.") and "proxy" in k.lower()]
    lines.append(f"  {label} proxy_keys={proxy_keys}")
    extra_remotes = sorted({k.split(".")[1] for k in by_key if k.startswith("remote.") and len(k.split(".")) > 2} - {"origin"})
    lines.append(f"  {label} extra_remotes={extra_remotes}")

    expected_url = INERT_URL if label in ("active", "copy") else WORKSPACE_URL
    if len(remote_urls) != 1 or remote_urls[0] != expected_url:
        errors.append(f"{label}: remote.origin.url not exactly expected ({expected_url}): {remote_urls}")
        return False
    if pushurls:
        errors.append(f"{label}: unexpected remote.origin.pushurl override: {pushurls}")
        return False
    if rewrite_keys:
        errors.append(f"{label}: unexpected url rewrite keys: {rewrite_keys}")
        return False
    if include_keys:
        errors.append(f"{label}: unexpected include indirection: {include_keys}")
        return False
    if proxy_keys:
        errors.append(f"{label}: unexpected http proxy routing: {proxy_keys}")
        return False
    if extra_remotes:
        errors.append(f"{label}: unexpected extra remotes: {extra_remotes}")
        return False
    # Effective push destination from `git remote -v` must match exactly too.
    push_lines = [ln for ln in remote_out.splitlines() if "(push)" in ln]
    if len(push_lines) != 1 or expected_url not in [tok for tok in push_lines[0].split()]:
        # strict token match, not substring of whole blob
        toks = push_lines[0].split() if push_lines else []
        if len(toks) < 2 or toks[1] != expected_url:
            errors.append(f"{label}: remote -v push destination not exactly {expected_url}: {push_lines}")
            return False
    return True


def main():
    if sys.flags.optimize != 0:
        return fail(f"optimized mode (optimize={sys.flags.optimize}); refusing (no assert reliance)")
    bad_git = sorted(k for k in os.environ if k.startswith("GIT_"))
    bad_py = sorted(k for k in ("PYTHONPATH", "PYTHONHOME") if k in os.environ)
    if not CLOSEOUT.is_dir():
        return fail(f"closeout dir missing: {CLOSEOUT}")
    for name in (RAW_NAME, JSON_NAME):
        if (CLOSEOUT / name).exists():
            return fail(f"output exists (exclusivity): {name}")
    out = {"stamp": STAMP, "started_utc": utcnow(), "errors": [], "checks": {}}
    lines = []
    lines.append(f"DM021-P1 correction4 FINAL read-only verification {STAMP}")
    lines.append(f"active={ACTIVE}")
    lines.append(f"copy={COPY}")
    lines.append(f"workspace={WORKSPACE}")
    lines.append(f"inherited_git_before_sanitize={bad_git}")
    lines.append(f"inherited_python_routing={bad_py}")
    lines.append(f"forced_git={sorted(FORCED_GIT)}")
    lines.append(f"optimize={sys.flags.optimize} interpreter={sys.executable} python={sys.version.split()[0]}")

    # Saved freeze + patch + contract identity (read-only).
    try:
        pre = json.loads(FREEZE_PRE.read_text(encoding="utf-8"))
        post = json.loads(FREEZE_POST.read_text(encoding="utf-8"))
    except OSError as exc:
        return fail(f"freeze unreadable: {exc}")
    out["checks"]["saved_pre_eq_post_full"] = (pre == post)
    out["checks"]["saved_status_exact13"] = (sorted(pre["status"].splitlines()) == EXPECTED_ROWS)
    lines.append(f"saved pre==post full: {pre == post}")
    lines.append(f"saved status exact13: {sorted(pre['status'].splitlines()) == EXPECTED_ROWS}")
    if pre != post:
        out["errors"].append("freeze pre/post differ")
    try:
        patch_bytes = PATCH.read_bytes()
        patch_sha = hashlib.sha256(patch_bytes).hexdigest()
        sha_file = PATCH_SHA_FILE.read_text(encoding="utf-8").strip()
        diffs = patch_bytes.decode("utf-8", errors="replace").count("diff --git ")
    except OSError as exc:
        return fail(f"patch unreadable: {exc}")
    out["checks"]["patch_sha_match"] = (patch_sha == PATCH_SHA and sha_file.startswith(PATCH_SHA))
    out["checks"]["patch_diffs"] = diffs
    out["checks"]["patch_bytes"] = len(patch_bytes)
    lines.append(f"patch sha={patch_sha} expect={PATCH_SHA} diffs={diffs} bytes={len(patch_bytes)}")
    if patch_sha != PATCH_SHA:
        out["errors"].append("patch SHA mismatch")
    if diffs != 13:
        out["errors"].append(f"patch diff count !=13: {diffs}")
    try:
        contract_sha = hashlib.sha256(CONTRACT.read_bytes()).hexdigest()
    except OSError as exc:
        return fail(f"contract unreadable: {exc}")
    out["checks"]["contract_sha_match"] = (contract_sha == CONTRACT_SHA)
    lines.append(f"contract sha={contract_sha} expect={CONTRACT_SHA}")
    if contract_sha != CONTRACT_SHA:
        out["errors"].append("contract SHA mismatch")

    # Per-repo read-only git state.
    states = {}
    for label, repo in (("active", ACTIVE), ("copy", COPY), ("workspace", WORKSPACE)):
        st = {"label": label, "path": str(repo), "exists": repo.is_dir()}
        if not repo.is_dir():
            out["errors"].append(f"{label} missing: {repo}")
            states[label] = st
            continue
        for name, argv in (
            ("head", ("rev-parse", "HEAD")),
            ("tree", ("rev-parse", "HEAD^{tree}")),
            ("status", ("status", "--porcelain")),
            ("cached", ("diff", "--cached", "--name-only")),
            ("ls_v", ("ls-files", "-v")),
            ("ls_stage", ("ls-files", "--stage")),
            ("config", ("config", "--list", "--show-origin")),
            ("remote_v", ("remote", "-v")),
        ):
            p = git_ro(repo, *argv)
            st[name + "_rc"] = p.returncode
            if name in ("head", "tree"):
                st[name] = p.stdout.strip()
            else:
                st[name] = p.stdout
            st[name + "_err"] = p.stderr[:300]
            if p.returncode != 0:
                out["errors"].append(f"{label} git {' '.join(argv)} rc={p.returncode}: {p.stderr[:200]}")
        alt = repo / ".git" / "objects" / "info" / "alternates"
        st["alternates_exists"] = alt.exists() or alt.is_symlink()
        states[label] = st
        lines.append(f"--- {label} head={st.get('head')} tree={st.get('tree')}")
        lines.append(f"  status_rc={st.get('status_rc')} bytes={len(st.get('status', ''))}")
        for ln in st.get("status", "").splitlines():
            lines.append(f"    |{ln}")
        lines.append(f"  cached={repr(st.get('cached', '')[:300])} ls_v_lines={len(st.get('ls_v','').splitlines())} stage_lines={len(st.get('ls_stage','').splitlines())}")

    out["states_summary"] = {k: {"head": v.get("head"), "tree": v.get("tree"),
                                 "status_rc": v.get("status_rc"), "cached_rc": v.get("cached_rc")}
                             for k, v in states.items()}

    # HEAD/tree/status/index expectations for candidate DBs.
    for label in ("active", "copy"):
        st = states[label]
        ok_head = (st.get("head") == HEAD409)
        ok_tree = (st.get("tree") == TREE8CE)
        ok_status = (st.get("status") == pre["status"])
        out["checks"][f"{label}_head409"] = ok_head
        out["checks"][f"{label}_tree8ce"] = ok_tree
        out["checks"][f"{label}_status_full_eq_freeze"] = ok_status
        lines.append(f"check {label}_head409={ok_head} {label}_tree8ce={ok_tree} status_full_eq={ok_status}")
        if not ok_head:
            out["errors"].append(f"{label} HEAD not 409")
        if not ok_tree:
            out["errors"].append(f"{label} tree not 8ce")
        if not ok_status:
            out["errors"].append(f"{label} full status != freeze-pre")
        # Index incl intent: cached empty AND no index-column staged entries AND no lowercase ls-files -v tags.
        cached_empty = (st.get("cached", "").strip() == "")
        porcelain = st.get("status", "")
        staged_rows = [ln for ln in porcelain.splitlines() if len(ln) >= 2 and ln[0] not in (" ", "?", "!")]
        ls_v_lower = [ln for ln in st.get("ls_v", "").splitlines() if ln[:1].islower()]
        out["checks"][f"{label}_cached_empty"] = cached_empty
        out["checks"][f"{label}_staged_rows"] = staged_rows
        out["checks"][f"{label}_lsv_lower"] = ls_v_lower
        lines.append(f"  {label} cached_empty={cached_empty} staged_rows={staged_rows} lsv_lower={ls_v_lower}")
        if not cached_empty:
            out["errors"].append(f"{label} index has cached entries")
        if staged_rows:
            out["errors"].append(f"{label} status shows staged/index-column rows: {staged_rows}")
        if ls_v_lower:
            out["errors"].append(f"{label} ls-files -v lowercase (intent/assume) rows: {ls_v_lower}")
        if st.get("alternates_exists"):
            out["errors"].append(f"{label} alternates present")
            lines.append(f"  {label} alternates PRESENT (reject)")
        else:
            lines.append(f"  {label} alternates absent")
        # Exact remote check.
        recs = parse_config_exact(st.get("config", ""))
        good = check_remote_exact(label, recs, st.get("remote_v", ""), out["errors"], lines)
        out["checks"][f"{label}_remote_exact"] = good

    # Workspace remote recorded strictly (expected github URL).
    ws = states.get("workspace", {})
    if ws.get("config") is not None:
        recs = parse_config_exact(ws.get("config", ""))
        good = check_remote_exact("workspace", recs, ws.get("remote_v", ""), out["errors"], lines)
        out["checks"]["workspace_remote_exact"] = good

    # 13 overlay bytes/modes vs freeze-pre (explicit-error on unreadable).
    for label, repo in (("active", ACTIVE), ("copy", COPY)):
        files = {}
        for rel in EXPECTED_MODIFIED + EXPECTED_NEW:
            full = repo / rel
            try:
                data = full.read_bytes()
                mode = oct(stat.S_IMODE(os.lstat(full).st_mode))
                files[rel] = {"sha256": hashlib.sha256(data).hexdigest(), "mode": mode, "bytes": len(data)}
            except OSError as exc:
                files[rel] = {"error": f"{type(exc).__name__}: {exc}"}
                out["errors"].append(f"{label} unreadable {rel}: {exc}")
        eq = (files == pre["files"])
        out["checks"][f"{label}_13_eq_freeze"] = eq
        lines.append(f"check {label}_13_eq_freeze={eq}")
        if not eq:
            for k in files:
                if files[k] != pre["files"].get(k):
                    lines.append(f"  MISMATCH {label} {k}: cur={files[k]} freeze={pre['files'].get(k)}")
                    if f"{label} 13 mismatch" not in str(out["errors"]):
                        out["errors"].append(f"{label} 13 mismatch: {k}")
        if f"{label}_files" not in out:
            out[f"{label}_files"] = files

    # Strict .git walks (every entry incl dirs; any error/symlink already recorded).
    walks = {}
    for label, repo in (("active", ACTIVE), ("copy", COPY), ("workspace", WORKSPACE)):
        w = walk_git_strict(repo, out["errors"])
        walks[label] = w
        lines.append(f"gitwalk {label}: entries={w['entries_total']} dirs={w['dirs']} files={w['files']} other={w['other']} symlinks={len(w['symlinks'])} nlink_bad={len(w['nlink_bad'])} stat_errors={len(w['stat_errors'])}")
        out["checks"][f"{label}_gitwalk_clean"] = (len(w["symlinks"]) == 0 and len(w["nlink_bad"]) == 0 and len(w["stat_errors"]) == 0 and w["gitdir_exists"])
    a_keys = set(walks["active"]["ino_map"].keys())
    c_keys = set(walks["copy"]["ino_map"].keys())
    w_keys = set(walks["workspace"]["ino_map"].keys())
    ac = sorted(a_keys & c_keys)
    aw = sorted(a_keys & w_keys)
    cw = sorted(c_keys & w_keys)
    out["checks"]["shared_active_copy"] = len(ac)
    out["checks"]["shared_active_workspace"] = len(aw)
    out["checks"]["shared_copy_workspace"] = len(cw)
    lines.append(f"shared dev:ino active&copy={len(ac)} active&ws={len(aw)} copy&ws={len(cw)}")
    for k in ac[:10]:
        lines.append(f"  SHARED A&C {k}: {walks['active']['ino_map'][k]} vs {walks['copy']['ino_map'][k]}")
        out["errors"].append(f"sharing active&copy: {k}")
    for k in aw[:10]:
        lines.append(f"  SHARED A&W {k}")
        out["errors"].append(f"sharing active&workspace: {k}")
    for k in cw[:10]:
        lines.append(f"  SHARED C&W {k}")
        out["errors"].append(f"sharing copy&workspace: {k}")

    ok = (len(out["errors"]) == 0)
    out["verdict"] = "FINAL_CURRENT_MATCH" if ok else "FINAL_MISMATCH"
    out["finished_utc"] = utcnow()
    lines.append(f"verdict={out['verdict']} errors={out['errors']}")
    lines.append("SCOPE: current-observation only; not retroactive, not continuous no-drift proof.")
    raw = "\n".join(lines) + "\n"
    print(raw, end="", flush=True)
    xwrite_text(CLOSEOUT / RAW_NAME, raw)
    xwrite_text(CLOSEOUT / JSON_NAME, json.dumps(out, indent=1) + "\n")
    return 0 if ok else 30


if __name__ == "__main__":
    sys.exit(main())
