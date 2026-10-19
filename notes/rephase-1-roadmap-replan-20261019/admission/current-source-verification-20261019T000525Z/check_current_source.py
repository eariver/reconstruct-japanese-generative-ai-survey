#!/usr/bin/env python3
"""Inspect-only current source verification (read-only, no Git writes).

Reads reference static pins from workspace static21.json; never computes
expected values from the observed tree (no baseline blessing).
All Git invocations use --no-optional-locks and
GIT_NO_LAZY_FETCH=1 / GIT_CONFIG_NOSYSTEM=1 / GIT_CONFIG_GLOBAL=/dev/null.
No restoration/reapply/Git writes/tests/imports. Writes nothing into the
restored DB; all output goes to stdout (captured externally to raw files).
"""
from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

RESTORED = Path("/tmp/opencode/jgas-roadmap-r1-20261018T163842Z/candidate-partial-b40de60")
WORKSPACE = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
STATIC21 = WORKSPACE / "notes/rephase-1-dm021-p3s/draft-history-r11/static21.json"
EXPECTED_STATIC21_SHA = "1c0e339ceb31ddb8d565580f4e0d0b2140085cc414bb766b46872fdc8a2ef1a5"
EXPECTED_HEAD = "409b292756dd1277b9dfae87679934c0d2ce251c"
EXPECTED_TREE = "8ce3699861505f32d1d60bdc185d4d4f635aedb2"
INPUTS = {
    "tar_b40": ("notes/rephase-1-candidate-recovery/m3-20261003T0445Z/candidate-partial-b40de60.tar.gz",
                "faf6792faf37ad30af2dbd7203b8896ca00964a91d00623a4f01278f2ade9f3c"),
    "successor_20": ("notes/rephase-1-dm001-019-implementation/evidence-final-20261003T145621Z/20-packaging/successor-pack.pack",
                     "2c2a8e6f2ab5fbd71b6cddfe5d875e4a821d09ef54ba9714eaab12e438e81a99"),
    "w1_7": ("notes/rephase-1-dm003-w1-implementation/evidence-20261004T072423Z/w1-222-to-e1705b7.pack",
             "97d384fe8f7216f110cd401d1279129da83fab2000f28c24a73abe0b177b0fd9"),
    "dm004_32": ("notes/rephase-1-dm004-implementation/evidence-20261007T131353Z/dm004final-e1705b7-to-409b292.pack",
                 "e3d941653eadf2459a13f1b85b9fbbffd819f0a0ad6bb77eb121b2cba02279bf"),
    "patch21": ("notes/rephase-1-dm021-p3s/evidence-20261018T154812Z-final-packaging/gen-complete21/complete-p3s-21path.patch",
                "e449d029c8775ee28ee610f224997a57b0cd68664194c6720a6038ce9a3012fa"),
}


def git_env() -> dict[str, str]:
    env = dict(os.environ)
    for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_CEILING_DIRECTORIES"):
        env.pop(k, None)
    env["GIT_NO_LAZY_FETCH"] = "1"
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_CONFIG_GLOBAL"] = "/dev/null"
    env["GIT_OPTIONAL_LOCKS"] = "0"
    return env


def run_git(args: list[str], cwd: Path) -> tuple[int, str, str]:
    p = subprocess.run(
        ["git", "--no-optional-locks", *args],
        cwd=str(cwd), env=git_env(),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return p.returncode, p.stdout, p.stderr


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    out: list[str] = []
    failures = 0

    def emit(s: str = "") -> None:
        out.append(s)
        print(s)

    emit("=== 0. inherited env (GIT_*) ===")
    git_vars = sorted((k, v) for k, v in os.environ.items() if k.startswith("GIT_"))
    if not git_vars:
        emit("NO_INHERITED_GIT_ENV")
    else:
        for k, v in git_vars:
            emit(f"INHERITED {k}={v}")
    emit(f"enforced: GIT_NO_LAZY_FETCH=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_OPTIONAL_LOCKS=0")
    emit("")

    emit("=== 1. HEAD/tree/detached ===")
    rc, so, se = run_git(["rev-parse", "HEAD"], RESTORED)
    emit(f"rev-parse HEAD rc={rc} stdout={so.strip()!r} stderr={se.strip()!r}")
    head_ok = (rc == 0 and so.strip() == EXPECTED_HEAD)
    emit(f"HEAD_EXPECTED {EXPECTED_HEAD} match={head_ok}")
    if not head_ok:
        failures += 1
    rc, so, se = run_git(["rev-parse", "HEAD^{tree}"], RESTORED)
    emit(f"rev-parse HEAD^{{tree}} rc={rc} stdout={so.strip()!r} stderr={se.strip()!r}")
    tree_ok = (rc == 0 and so.strip() == EXPECTED_TREE)
    emit(f"TREE_EXPECTED {EXPECTED_TREE} match={tree_ok}")
    if not tree_ok:
        failures += 1
    rc, so, se = run_git(["symbolic-ref", "-q", "HEAD"], RESTORED)
    emit(f"symbolic-ref HEAD rc={rc} stdout={so.strip()!r} stderr={se.strip()!r} (rc!=0 means detached)")
    detached_ok = (rc != 0)
    emit(f"DETACHED={detached_ok}")
    if not detached_ok:
        failures += 1
    rc, so, se = run_git(["rev-parse", "--is-shallow-repository"], RESTORED)
    emit(f"is-shallow rc={rc} stdout={so.strip()!r}")
    rc, so, se = run_git(["rev-parse", "--git-dir"], RESTORED)
    emit(f"git-dir rc={rc} stdout={so.strip()!r} stderr={se.strip()!r}")
    rc, so, se = run_git(["rev-parse", "--git-common-dir"], RESTORED)
    emit(f"git-common-dir rc={rc} stdout={so.strip()!r} stderr={se.strip()!r}")
    emit("")

    emit("=== 2. status -z (all untracked, parsed 3M18A, index diff) ===")
    p = subprocess.run(
        ["git", "--no-optional-locks", "status", "--porcelain=v1", "-z"],
        cwd=str(RESTORED), env=git_env(),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    emit(f"status -z rc={p.returncode} stdout_bytes={len(p.stdout)} stderr={p.stderr.decode()!r}")
    raw = p.stdout
    entries = raw.split(b"\x00")
    # trailing empty after final NUL
    if entries and entries[-1] == b"":
        entries = entries[:-1]
    emit(f"status_nul_entries={len(entries)}")
    # Parse XY + path (porcelain v1 -z: XY + space + path NUL; renames have extra NUL but none expected)
    mod = [e for e in entries if e.startswith(b" M ") or e.startswith(b"M ")]
    # Actually porcelain: first 2 chars XY, third char space. M can be in index or worktree.
    # Count precisely:
    m_count = sum(1 for e in entries if e[:2] in (b"M ", b" M", b"MM"))
    untracked = sum(1 for e in entries if e[:2] == b"??")
    emit(f"parsed M={m_count} untracked={untracked} total={len(entries)} expected_M=3 expected_untracked=18")
    if not (m_count == 3 and untracked == 18 and len(entries) == 21):
        failures += 1
        emit("STATUS_PARSE_MISMATCH")
    else:
        emit("STATUS_PARSE_OK")
    for e in sorted(entries):
        emit(f"  entry: {e!r}")
    rc, so, se = run_git(["diff", "--name-status", "HEAD"], RESTORED)
    emit(f"diff HEAD rc={rc} stdout_lines={len(so.splitlines())} stderr={se.strip()!r}")
    for line in so.splitlines():
        emit(f"  diff: {line}")
    rc, so, se = run_git(["diff", "--cached", "--name-status"], RESTORED)
    emit(f"diff --cached rc={rc} stdout_lines={len(so.splitlines())} stderr={se.strip()!r}")
    for line in so.splitlines():
        emit(f"  cached: {line}")
    rc, so, se = run_git(["ls-files", "--stage"], RESTORED)
    n_index = len([l for l in so.splitlines() if l.strip()])
    emit(f"ls-files --stage rc={rc} count={n_index} (normal index holds HEAD tracked bytes; NOT claimed empty)")
    emit("")

    emit("=== 3. all21 sha/len/mode vs static reference (reference-read, no blessing) ===")
    try:
        static_raw = STATIC21.read_bytes()
    except OSError as exc:
        emit(f"STATIC_READ_FAIL {exc}")
        return 2
    static_sha = hashlib.sha256(static_raw).hexdigest()
    emit(f"static21 file sha256={static_sha} expected={EXPECTED_STATIC21_SHA} match={static_sha == EXPECTED_STATIC21_SHA}")
    if static_sha != EXPECTED_STATIC21_SHA:
        failures += 1
    try:
        pins = json.loads(static_raw.decode("utf-8"))
    except ValueError as exc:
        emit(f"STATIC_JSON_FAIL {exc}")
        return 2
    emit(f"static21 entries={len(pins)} expected=21")
    if len(pins) != 21:
        failures += 1
    ok21 = 0
    for rel in sorted(pins):
        exp = pins[rel]
        fp = RESTORED / rel
        try:
            data = fp.read_bytes()
        except OSError as exc:
            emit(f"MISSING {rel} error={exc}")
            failures += 1
            continue
        h = hashlib.sha256(data).hexdigest()
        ln = len(data)
        try:
            mode = oct(stat.S_IMODE(fp.stat().st_mode))
        except OSError as exc:
            emit(f"STAT_FAIL {rel} {exc}")
            failures += 1
            continue
        exp_h = exp.get("sha256", "")
        exp_b = exp.get("bytes", -1)
        exp_m = exp.get("mode", "")
        match = (h == exp_h and ln == exp_b and mode == exp_m)
        emit(f"{'OK' if match else 'MISMATCH'} {rel} sha={h} bytes={ln} mode={mode} | exp sha={exp_h} bytes={exp_b} mode={exp_m}")
        if match:
            ok21 += 1
        else:
            failures += 1
    emit(f"VERIFY21 ok={ok21}/21")
    emit("")

    emit("=== 4. durable inputs + patch + static hashes ===")
    for key, (rel, exp_sha) in INPUTS.items():
        fp = WORKSPACE / rel
        try:
            sz = fp.stat().st_size
            h = sha256_file(fp)
        except OSError as exc:
            emit(f"INPUT_MISSING {key} {rel} error={exc}")
            failures += 1
            continue
        match = (h == exp_sha)
        emit(f"{'OK' if match else 'MISMATCH'} {key} bytes={sz} sha256={h} expected={exp_sha}")
        if not match:
            failures += 1
    emit("")

    emit("=== 5. .git entries/types/aliases/alternates/config-hints/hooks/remote ===")
    dotgit = RESTORED / ".git"
    n_file = n_dir = n_link = n_other = 0
    links: list[str] = []
    for root, dirs, files in os.walk(dotgit, followlinks=False):
        # dirs: check each dir entry for symlink before descending (walk already lists)
        for d in dirs:
            p = Path(root) / d
            try:
                if p.is_symlink():
                    n_link += 1
                    links.append(str(p.relative_to(RESTORED)) + " -> " + os.readlink(p))
                elif p.is_dir():
                    n_dir += 1
                else:
                    n_other += 1
            except OSError as exc:
                emit(f"WALK_DIR_ERR {p} {exc}")
        for f in files:
            p = Path(root) / f
            try:
                if p.is_symlink():
                    n_link += 1
                    links.append(str(p.relative_to(RESTORED)) + " -> " + os.readlink(p))
                elif p.is_file():
                    n_file += 1
                else:
                    n_other += 1
            except OSError as exc:
                emit(f"WALK_FILE_ERR {p} {exc}")
    emit(f".git census files={n_file} dirs={n_dir} symlinks={n_link} other={n_other}")
    if links:
        for l in links:
            emit(f"  symlink: {l}")
        failures += 1
    else:
        emit("NO_SYMLINKS_OK (no aliases)")
    alt = dotgit / "objects" / "info" / "alternates"
    emit(f"alternates exists={alt.exists()} (expected False; True would be sharing)")
    if alt.exists():
        try:
            emit(f"alternates content={alt.read_text()!r}")
        except OSError as exc:
            emit(f"alternates read err {exc}")
        failures += 1
    else:
        emit("NO_ALTERNATES_OK")
    rc, so, se = run_git(["config", "--show-origin", "--list"], RESTORED)
    emit(f"config --show-origin --list rc={rc} stderr={se.strip()!r}")
    for line in so.splitlines():
        emit(f"  cfg: {line}")
        if "insteadOf" in line or "include" in line.lower():
            emit("  CONFIG_INCLUDE_NOTICE (manual review)")
    rc, so, se = run_git(["remote", "-v"], RESTORED)
    emit(f"remote -v rc={rc} stdout={so.strip()!r} stderr={se.strip()!r}")
    if "example.invalid" not in so:
        emit("REMOTE_NOT_INERT")
        failures += 1
    else:
        emit("REMOTE_INERT_OK")
    # hooks: active (non-sample) executables
    hooks = dotgit / "hooks"
    try:
        hook_names = sorted(p.name for p in hooks.iterdir())
    except OSError as exc:
        emit(f"HOOKS_READ_FAIL {exc}")
        hook_names = []
        failures += 1
    emit(f"hooks entries={len(hook_names)}")
    for n in hook_names:
        emit(f"  hook: {n}")
    active_hooks = [n for n in hook_names if not n.endswith(".sample")]
    emit(f"active_hooks(non-sample)={active_hooks} expected=[]")
    if active_hooks:
        failures += 1
    emit("")

    emit("=== 6. inode sharing (exact comparison domain) ===")
    def devino(p: Path) -> str:
        try:
            st = p.stat()
            return f"{st.st_dev}:{st.st_ino}"
        except OSError as exc:
            return f"ERR:{exc}"
    # restored packs
    restored_packs = sorted((dotgit / "objects" / "pack").glob("*.pack"))
    emit(f"restored packs: {[p.name for p in restored_packs]}")
    restored_inodes = {p.name: devino(p) for p in restored_packs}
    for n, di in restored_inodes.items():
        emit(f"  restored {n} {di}")
    # durable inputs
    for key, (rel, _exp) in INPUTS.items():
        if key == "patch21":
            continue
        fp = WORKSPACE / rel
        emit(f"  durable {key} {devino(fp)} {rel}")
    # reconstruct .git objects sample (do not walk entire history; sample HEAD + pack dir listing)
    recon_git = WORKSPACE / ".git"
    emit(f"  reconstruct .git {devino(recon_git)}")
    # compare: any restored pack inode equals any durable input inode or reconstruct sample?
    seen: dict[str, str] = {}
    collision = False
    for n, di in restored_inodes.items():
        if di in seen:
            emit(f"  COLLISION restored {n} shares {di} with {seen[di]}")
            collision = True
        seen[di] = f"restored:{n}"
    for key, (rel, _exp) in INPUTS.items():
        fp = WORKSPACE / rel
        di = devino(fp)
        if di in seen:
            emit(f"  COLLISION durable {key} shares {di} with {seen[di]}")
            collision = True
        seen[di] = f"durable:{key}"
    # reconstruct HEAD object? compare .git/HEAD file inode (not object) as domain statement
    recon_head = recon_git / "HEAD"
    emit(f"  reconstruct .git/HEAD {devino(recon_head)}")
    if devino(recon_head) in seen:
        emit("  COLLISION reconstruct HEAD file shares inode (unexpected)")
        collision = True
    emit(f"INODE_SHARING_FOUND={collision} (expected False; domain: restored pack *.pack vs durable inputs vs reconstruct .git/HEAD file)")
    if collision:
        failures += 1
    else:
        emit("NO_INODE_SHARING_OK (within stated domain)")
    emit("")

    emit("=== 7. cache dirs (expected none) ===")
    cache_dirs = []
    for root, dirs, _files in os.walk(RESTORED, followlinks=False):
        if "__pycache__" in dirs:
            cache_dirs.append(str((Path(root) / "__pycache__").relative_to(RESTORED)))
    emit(f"__pycache__ dirs={len(cache_dirs)} expected=0")
    for d in cache_dirs:
        emit(f"  cache: {d}")
    if cache_dirs:
        failures += 1
    else:
        emit("NO_CACHES_OK (cache84 historical-absent, not reconstructed)")
    emit("")

    emit("=== 8. missing reachability (rev-list --missing=print; NOT fsck available13) ===")
    emit("NOTE: prior transcribed fsck missing26309 is NOT reused here; this section is the current census.")
    emit("NOTE: 13-commit chain length != all-object reachability; counts below are rev-list object lines, not commit count.")
    p = subprocess.run(
        ["git", "--no-optional-locks", "rev-list", "--objects", "--missing=print", EXPECTED_HEAD],
        cwd=str(RESTORED), env=git_env(),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    emit(f"rev-list rc={p.returncode} stderr={p.stderr.strip()!r}")
    lines = [l for l in p.stdout.splitlines() if l.strip()]
    emit(f"rev-list total_lines={len(lines)}")
    # --missing=print prefixes missing lines with '?'
    missing_lines = [l for l in lines if l.startswith("?")]
    present_lines = [l for l in lines if not l.startswith("?")]
    emit(f"rev-list present={len(present_lines)} missing_print={len(missing_lines)}")
    for l in missing_lines[:20]:
        emit(f"  missing: {l}")
    if len(missing_lines) > 20:
        emit(f"  ... and {len(missing_lines) - 20} more missing lines (full output is the raw stdout file)")
    # commit count within rev-list (lines whose object is a commit? cannot tell from --objects alone; do separate rev-list --count equivalent read-only)
    q = subprocess.run(
        ["git", "--no-optional-locks", "rev-list", "--count", "--missing=print", EXPECTED_HEAD],
        cwd=str(RESTORED), env=git_env(),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    emit(f"rev-list --count rc={q.returncode} stdout={q.stdout.strip()!r} stderr={q.stderr.strip()!r}")
    if p.returncode != 0:
        failures += 1
        emit("REVLIST_FAIL")
    emit("")

    emit(f"=== SUMMARY failures={failures} (0 means current observation matches stated expectations; nonzero is preserved, not hidden) ===")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
