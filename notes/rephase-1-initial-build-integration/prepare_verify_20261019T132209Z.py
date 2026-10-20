#!/usr/bin/env python3
"""Initial-build-integration PREPARATION verifier (inspect-only, no source mutation).

Preparation-only for R2 initial Weekly+Longform real-build integration.
- Target source read-only: /tmp/opencode/jgas-roadmap-r1-20261018T163842Z/candidate-partial-b40de60
- No restoration/reapply, no historical runners/tests, no imports of source modules,
  no cache creation inside source, no candidate/reconstruct commits, no network/install.
- Git env sanitized: GIT_* overrides removed, GIT_NO_LAZY_FETCH=1,
  GIT_CONFIG_NOSYSTEM=1, GIT_CONFIG_GLOBAL=/dev/null, GIT_OPTIONAL_LOCKS=0,
  all git via --no-optional-locks.
- Static21 reference is hashed BEFORE trusting (expected 1c0e339c...).
- Checks: HEAD/tree/detached/status 3M18A/diff HEAD 3/diff cached 0/index count,
  all21 sha/bytes/mode 21/21, .git full entry-type census, alternates absent,
  config include/insteadOf inspection, remote inert (example.invalid),
  hooks active 0, __pycache__ 0, rev-list summary (NOT full 28k dump),
  toolchain inventory (which + --version, missing tolerated, no install),
  optional DEST copy identity + FULL .git inode non-sharing vs source+reconstruct.
- All output to stdout; stderr stays empty unless unexpected exception.
  Caller captures stdout/stderr/exit to unique durable files externally.
- This script writes nothing into SOURCE or DEST; it only reads.
Usage:
  python3 prepare_verify_20261019T132209Z.py [--dest /tmp/.../candidate-partial-b40de60]
  --dest absent  => source-before + toolchain only (pre-copy).
  --dest present => source re-guard + dest identity + full inode separation.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

SOURCE = Path("/tmp/opencode/jgas-roadmap-r1-20261018T163842Z/candidate-partial-b40de60")
WORKSPACE = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
STATIC21 = WORKSPACE / "notes/rephase-1-dm021-p3s/draft-history-r11/static21.json"
EXPECTED_STATIC21_SHA = "1c0e339ceb31ddb8d565580f4e0d0b2140085cc414bb766b46872fdc8a2ef1a5"
EXPECTED_HEAD = "409b292756dd1277b9dfae87679934c0d2ce251c"
EXPECTED_TREE = "8ce3699861505f32d1d60bdc185d4d4f635aedb2"

def git_env() -> dict[str, str]:
    env = dict(os.environ)
    for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_CEILING_DIRECTORIES",
              "GIT_COMMON_DIR", "GIT_PREFIX"):
        env.pop(k, None)
    env["GIT_NO_LAZY_FETCH"] = "1"
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_CONFIG_GLOBAL"] = "/dev/null"
    env["GIT_OPTIONAL_LOCKS"] = "0"
    return env

def run_git(args: list[str], cwd: Path) -> tuple[int, str, str]:
    p = subprocess.run(["git", "--no-optional-locks", *args], cwd=str(cwd),
                       env=git_env(), stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, text=True)
    return p.returncode, p.stdout, p.stderr

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for ch in iter(lambda: fh.read(65536), b""):
            h.update(ch)
    return h.hexdigest()

def census_git_dotgit(root: Path) -> tuple[int, int, int, int, list[str]]:
    dot = root / ".git"
    nf = nd = nl = no = 0
    links: list[str] = []
    for cur, dirs, files in os.walk(dot, followlinks=False):
        for d in dirs:
            q = Path(cur) / d
            try:
                if q.is_symlink():
                    nl += 1
                    links.append(str(q.relative_to(root)) + " -> " + os.readlink(q))
                elif q.is_dir() and not q.is_symlink():
                    nd += 1
                else:
                    no += 1
            except OSError:
                no += 1
        for f in files:
            q = Path(cur) / f
            try:
                if q.is_symlink():
                    nl += 1
                    links.append(str(q.relative_to(root)) + " -> " + os.readlink(q))
                elif q.is_file():
                    nf += 1
                else:
                    no += 1
            except OSError:
                no += 1
    return nf, nd, nl, no, links

def collect_git_file_inodes(root: Path) -> dict[str, str]:
    """Map relative path -> dev:ino for every regular file under root/.git (full, not pack-only)."""
    dot = root / ".git"
    out: dict[str, str] = {}
    for cur, _dirs, files in os.walk(dot, followlinks=False):
        for f in files:
            q = Path(cur) / f
            try:
                if q.is_symlink() or not q.is_file():
                    continue
                st = q.stat()
                out[str(q.relative_to(root))] = f"{st.st_dev}:{st.st_ino}"
            except OSError as e:
                out[str(q.relative_to(root))] = f"ERR:{e}"
    return out

def which_version(tool: str, ver_args: list[str]) -> tuple[str, int, str, str]:
    binp = shutil.which(tool)
    if binp is None:
        return "", 127, "", f"NOT_FOUND:{tool}"
    try:
        p = subprocess.run([binp, *ver_args], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, text=True, timeout=20)
        so = (p.stdout or "")[:2000]
        se = (p.stderr or "")[:2000]
        return binp, p.returncode, so.strip(), se.strip()
    except Exception as e:
        return binp, 126, "", f"EXEC_FAIL:{e}"

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dest", default="", help="optional dest copy root for after-phase")
    args = ap.parse_args()
    dest = Path(args.dest) if args.dest else None
    failures = 0
    def emit(s: str = "") -> None:
        print(s)
    emit("=== PREP 0. inherited env + enforced sanitization ===")
    gv = sorted((k, v) for k, v in os.environ.items() if k.startswith("GIT_"))
    if not gv:
        emit("NO_INHERITED_GIT_ENV")
    else:
        for k, v in gv:
            emit(f"INHERITED {k}={v}")
        failures += 1
        emit("INHERITED_GIT_ENV_PRESENT (recorded; enforced env still applied per-call)")
        failures -= 1  # informational only, not a source mismatch
    emit("enforced: GIT_NO_LAZY_FETCH=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_OPTIONAL_LOCKS=0 + git --no-optional-locks")
    emit(f"cwd={os.getcwd()}")
    emit(f"python={sys.version.replace(chr(10),' ')}")
    emit(f"source={SOURCE} exists={SOURCE.exists()} is_symlink={SOURCE.is_symlink() if SOURCE.exists() else False}")
    if not SOURCE.exists():
        emit("SOURCE_ABSENT_FAIL")
        emit("=== SUMMARY failures=1 ===")
        return 2
    if dest is not None:
        emit(f"dest={dest} exists={dest.exists()}")
    emit("")
    # --- 1. source identity ---
    emit("=== PREP 1. source HEAD/tree/detached ===")
    rc, so, se = run_git(["rev-parse", "HEAD"], SOURCE)
    emit(f"src rev-parse HEAD rc={rc} stdout={so.strip()!r} stderr={se.strip()!r}")
    ok = (rc == 0 and so.strip() == EXPECTED_HEAD)
    emit(f"src HEAD_EXPECTED {EXPECTED_HEAD} match={ok}")
    if not ok:
        failures += 1
    rc, so, se = run_git(["rev-parse", "HEAD^{tree}"], SOURCE)
    emit(f"src rev-parse HEAD^{{tree}} rc={rc} stdout={so.strip()!r} stderr={se.strip()!r}")
    ok = (rc == 0 and so.strip() == EXPECTED_TREE)
    emit(f"src TREE_EXPECTED {EXPECTED_TREE} match={ok}")
    if not ok:
        failures += 1
    rc, so, se = run_git(["symbolic-ref", "-q", "HEAD"], SOURCE)
    emit(f"src symbolic-ref rc={rc} (nonzero=detached)")
    if rc == 0:
        emit("src NOT_DETACHED_FAIL")
        failures += 1
    else:
        emit("src DETACHED=True")
    rc, so, se = run_git(["rev-parse", "--is-shallow-repository"], SOURCE)
    emit(f"src is-shallow rc={rc} stdout={so.strip()!r}")
    rc, so, se = run_git(["rev-parse", "--git-dir"], SOURCE)
    emit(f"src git-dir rc={rc} stdout={so.strip()!r}")
    rc, so, se = run_git(["rev-parse", "--git-common-dir"], SOURCE)
    emit(f"src git-common-dir rc={rc} stdout={so.strip()!r}")
    emit("")
    emit("=== PREP 2. source status 3M18A / diff / index ===")
    p = subprocess.run(["git", "--no-optional-locks", "status", "--porcelain=v1", "-z"],
                       cwd=str(SOURCE), env=git_env(),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    emit(f"src status -z rc={p.returncode} bytes={len(p.stdout)} stderr={p.stderr.decode()!r}")
    raw = p.stdout
    ents = raw.split(b"\x00")
    if ents and ents[-1] == b"":
        ents = ents[:-1]
    emit(f"src status_nul_entries={len(ents)}")
    mcnt = sum(1 for e in ents if e[:2] in (b"M ", b" M", b"MM"))
    un = sum(1 for e in ents if e[:2] == b"??")
    emit(f"src parsed M={mcnt} untracked={un} total={len(ents)} expected 3/18/21")
    if not (mcnt == 3 and un == 18 and len(ents) == 21):
        emit("src STATUS_PARSE_MISMATCH")
        failures += 1
    else:
        emit("src STATUS_PARSE_OK")
    for e in sorted(ents):
        emit(f"  src entry: {e!r}")
    rc, so, se = run_git(["diff", "--name-status", "HEAD"], SOURCE)
    dl = [l for l in so.splitlines() if l.strip()]
    emit(f"src diff HEAD rc={rc} lines={len(dl)} (expected 3)")
    for l in dl:
        emit(f"  src diff: {l}")
    if len(dl) != 3:
        failures += 1
    rc, so, se = run_git(["diff", "--cached", "--name-status"], SOURCE)
    cl = [l for l in so.splitlines() if l.strip()]
    emit(f"src diff --cached rc={rc} lines={len(cl)} (expected 0)")
    for l in cl:
        emit(f"  src cached: {l}")
    if len(cl) != 0:
        failures += 1
    rc, so, se = run_git(["ls-files", "--stage"], SOURCE)
    nic = len([l for l in so.splitlines() if l.strip()])
    emit(f"src ls-files --stage rc={rc} count={nic} (normal index holds HEAD bytes; NOT claimed empty)")
    emit("")
    emit("=== PREP 3. static21 hash-before-trust + all21 ===")
    try:
        sraw = STATIC21.read_bytes()
    except OSError as e:
        emit(f"STATIC_READ_FAIL {e}")
        emit(f"=== SUMMARY failures={failures+1} ===")
        return 2
    sh = hashlib.sha256(sraw).hexdigest()
    emit(f"static21 file sha256={sh} expected={EXPECTED_STATIC21_SHA} match={sh==EXPECTED_STATIC21_SHA}")
    if sh != EXPECTED_STATIC21_SHA:
        failures += 1
    try:
        pins = json.loads(sraw.decode("utf-8"))
    except ValueError as e:
        emit(f"STATIC_JSON_FAIL {e}")
        return 2
    emit(f"static21 entries={len(pins)} expected=21")
    if len(pins) != 21:
        failures += 1
    ok21 = 0
    for rel in sorted(pins):
        exp = pins[rel]
        fp = SOURCE / rel
        try:
            data = fp.read_bytes()
        except OSError as e:
            emit(f"MISSING {rel} {e}")
            failures += 1
            continue
        h = hashlib.sha256(data).hexdigest()
        ln = len(data)
        try:
            mode = oct(stat.S_IMODE(fp.stat().st_mode))
        except OSError as e:
            emit(f"STAT_FAIL {rel} {e}")
            failures += 1
            continue
        match = (h == exp.get("sha256", "") and ln == exp.get("bytes", -1) and mode == exp.get("mode", ""))
        emit(f"{'OK' if match else 'MISMATCH'} {rel} sha={h} bytes={ln} mode={mode}")
        if match:
            ok21 += 1
        else:
            failures += 1
    emit(f"VERIFY21 ok={ok21}/21")
    emit("")
    emit("=== PREP 4. source .git census / alternates / config / remote / hooks ===")
    nf, nd, nl, no, links = census_git_dotgit(SOURCE)
    emit(f"src .git files={nf} dirs={nd} symlinks={nl} other={no}")
    if links:
        for l in links:
            emit(f"  src symlink: {l}")
        failures += 1
    else:
        emit("src NO_SYMLINKS_OK")
    alt = SOURCE / ".git" / "objects" / "info" / "alternates"
    emit(f"src alternates exists={alt.exists()} (expected False)")
    if alt.exists():
        failures += 1
    else:
        emit("src NO_ALTERNATES_OK")
    rc, so, se = run_git(["config", "--show-origin", "--list"], SOURCE)
    emit(f"src config --show-origin rc={rc} stderr={se.strip()!r}")
    badinc = False
    for line in so.splitlines():
        emit(f"  src cfg: {line}")
        low = line.lower()
        if "include" in low and "includeif" not in low and "file:" in line:
            # config.worktree include is not expected here; flag for review
            pass
        if "insteadOf" in line:
            badinc = True
    # explicit include.path check
    rc2, so2, _se2 = run_git(["config", "--get-all", "include.path"], SOURCE)
    emit(f"src include.path rc={rc2} stdout={so2.strip()!r} (rc!=0 means none)")
    if badinc:
        emit("src CONFIG_INSTEADOF_NOTICE")
        failures += 1
    rc, so, se = run_git(["remote", "-v"], SOURCE)
    emit(f"src remote -v rc={rc} stdout={so.strip()!r}")
    if "example.invalid" not in so:
        emit("src REMOTE_NOT_INERT")
        failures += 1
    else:
        emit("src REMOTE_INERT_OK")
    hooks = SOURCE / ".git" / "hooks"
    try:
        hnames = sorted(q.name for q in hooks.iterdir())
    except OSError as e:
        emit(f"src HOOKS_READ_FAIL {e}")
        hnames = []
        failures += 1
    emit(f"src hooks entries={len(hnames)}")
    for n in hnames:
        emit(f"  src hook: {n}")
    act = [n for n in hnames if not n.endswith(".sample")]
    emit(f"src active_hooks={act} expected=[]")
    if act:
        failures += 1
    emit("")
    emit("=== PREP 5. source cache + rev-list summary (no full dump) ===")
    caches: list[str] = []
    for cur, dirs, _f in os.walk(SOURCE, followlinks=False):
        if "__pycache__" in dirs:
            caches.append(str((Path(cur) / "__pycache__").relative_to(SOURCE)))
    emit(f"src __pycache__ dirs={len(caches)} expected=0")
    for c in caches:
        emit(f"  src cache: {c}")
    if caches:
        failures += 1
    else:
        emit("src NO_CACHES_OK")
    q = subprocess.run(["git", "--no-optional-locks", "rev-list", "--count", EXPECTED_HEAD],
                       cwd=str(SOURCE), env=git_env(),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    emit(f"src rev-list --count rc={q.returncode} stdout={q.stdout.strip()!r} stderr={q.stderr.strip()!r} (expected 13)")
    if q.stdout.strip() != "13":
        failures += 1
    r = subprocess.run(["git", "--no-optional-locks", "rev-list", "--objects", "--missing=print", EXPECTED_HEAD],
                       cwd=str(SOURCE), env=git_env(),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    lines = [l for l in r.stdout.splitlines() if l.strip()]
    miss = [l for l in lines if l.startswith("?")]
    pres = len(lines) - len(miss)
    emit(f"src rev-list --missing=print rc={r.returncode} total={len(lines)} present={pres} missing={len(miss)} (expected total 28685/present 2376/missing 26309)")
    for l in miss[:5]:
        emit(f"  src missing-sample: {l}")
    if not (len(lines) == 28685 and pres == 2376 and len(miss) == 26309):
        emit("src REVLIST_CENSUS_MISMATCH (recorded; does not auto-pass)")
        failures += 1
    else:
        emit("src REVLIST_CENSUS_OK")
    emit("")
    emit("=== PREP 6. toolchain inventory (no install, no network) ===")
    probes: list[tuple[str, list[str]]] = [
        ("python3", ["--version"]),
        ("pip3", ["--version"]),
        ("lualatex", ["--version"]),
        ("latexmk", ["--version"]),
        ("biber", ["--version"]),
        ("bibtex", ["--version"]),
        ("kpsewhich", ["--version"]),
        ("fc-list", ["--version"]),
        ("fc-match", ["--version"]),
        ("pdfinfo", ["-v"]),
        ("pdftotext", ["-v"]),
        ("pdfimages", ["-v"]),
        ("pdftoppm", ["-v"]),
        ("gs", ["--version"]),
        ("convert", ["-version"]),
        ("magick", ["-version"]),
        ("qpdf", ["--version"]),
        ("docker", ["--version"]),
        ("git", ["--version"]),
    ]
    for tool, va in probes:
        binp, rcx, sox, sex = which_version(tool, va)
        if not binp:
            emit(f"TOOL {tool}: NOT_FOUND rc=127")
        else:
            first = (sox.splitlines()[0] if sox else (sex.splitlines()[0] if sex else ""))[:300]
            emit(f"TOOL {tool}: path={binp} rc={rcx} ver={first!r}")
    # font check (read-only, no install): list a known CJK-relevant query if fc-match exists
    if shutil.which("fc-match") is not None:
        try:
            p = subprocess.run(["fc-match", "-s", "sans"], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True, timeout=20)
            fl = [l for l in p.stdout.splitlines() if l.strip()][:5]
            emit(f"fc-match sans rc={p.returncode} top={len(fl)}")
            for l in fl:
                emit(f"  font: {l[:300]}")
        except Exception as e:
            emit(f"fc-match probe fail {e}")
    else:
        emit("fc-match unavailable; font coverage UNKNOWN")
    # docker daemon probe without network/pull: docker info would touch daemon; do version only above.
    # Deliberately no `docker pull`, no network egress test, no sudo install.
    emit("network/install: NO_NETWORK_TEST, NO_INSTALL_ATTEMPTED (per preparation scope)")
    emit("")
    if dest is not None and dest.exists():
        emit("=== PREP 7. dest identity (must mirror source expectations) ===")
        rc, so, se = run_git(["rev-parse", "HEAD"], dest)
        emit(f"dst rev-parse HEAD rc={rc} stdout={so.strip()!r}")
        if so.strip() != EXPECTED_HEAD:
            emit("dst HEAD_MISMATCH")
            failures += 1
        else:
            emit("dst HEAD_OK")
        rc, so, se = run_git(["rev-parse", "HEAD^{tree}"], dest)
        emit(f"dst tree rc={rc} stdout={so.strip()!r}")
        if so.strip() != EXPECTED_TREE:
            emit("dst TREE_MISMATCH")
            failures += 1
        else:
            emit("dst TREE_OK")
        rc, so, se = run_git(["symbolic-ref", "-q", "HEAD"], dest)
        emit(f"dst symbolic-ref rc={rc} (nonzero=detached)")
        if rc == 0:
            emit("dst NOT_DETACHED_FAIL")
            failures += 1
        else:
            emit("dst DETACHED=True")
        p2 = subprocess.run(["git", "--no-optional-locks", "status", "--porcelain=v1", "-z"],
                            cwd=str(dest), env=git_env(),
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        e2 = p2.stdout.split(b"\x00")
        if e2 and e2[-1] == b"":
            e2 = e2[:-1]
        m2 = sum(1 for e in e2 if e[:2] in (b"M ", b" M", b"MM"))
        u2 = sum(1 for e in e2 if e[:2] == b"??")
        emit(f"dst status entries={len(e2)} M={m2} untracked={u2} (expected 21/3/18)")
        if not (len(e2) == 21 and m2 == 3 and u2 == 18):
            emit("dst STATUS_MISMATCH")
            failures += 1
        else:
            emit("dst STATUS_OK")
        # dest all21 quick rehash (full 21)
        okd = 0
        for rel in sorted(pins):
            fp = dest / rel
            try:
                d = fp.read_bytes()
            except OSError as e:
                emit(f"dst MISSING {rel} {e}")
                failures += 1
                continue
            h = hashlib.sha256(d).hexdigest()
            if h == pins[rel].get("sha256", "") and len(d) == pins[rel].get("bytes", -1):
                okd += 1
            else:
                emit(f"dst MISMATCH {rel}")
                failures += 1
        emit(f"dst VERIFY21 sha+bytes ok={okd}/21")
        nf2, nd2, nl2, _no2, l2 = census_git_dotgit(dest)
        emit(f"dst .git files={nf2} dirs={nd2} symlinks={nl2}")
        if nl2 or l2:
            emit("dst SYMLINK_FAIL")
            failures += 1
        else:
            emit("dst NO_SYMLINKS_OK")
        if (dest / ".git" / "objects" / "info" / "alternates").exists():
            emit("dst ALTERNATES_PRESENT_FAIL")
            failures += 1
        else:
            emit("dst NO_ALTERNATES_OK")
        rc, so, se = run_git(["remote", "-v"], dest)
        emit(f"dst remote rc={rc} stdout={so.strip()!r}")
        if "example.invalid" not in so:
            emit("dst REMOTE_NOT_INERT")
            failures += 1
        else:
            emit("dst REMOTE_INERT_OK")
        dc: list[str] = []
        for cur, dirs, _f in os.walk(dest, followlinks=False):
            if "__pycache__" in dirs:
                dc.append(str((Path(cur) / "__pycache__").relative_to(dest)))
        emit(f"dst __pycache__ dirs={len(dc)} expected=0")
        if dc:
            failures += 1
        else:
            emit("dst NO_CACHES_OK")
        emit("")
        emit("=== PREP 8. FULL .git inode separation (all files, not pack-only) ===")
        src_map = collect_git_file_inodes(SOURCE)
        dst_map = collect_git_file_inodes(dest)
        recon_map = collect_git_file_inodes(WORKSPACE)
        emit(f"src .git files hashed={len(src_map)} dst .git files={len(dst_map)} recon .git files={len(recon_map)}")
        # invert dev:ino -> holders
        from collections import defaultdict
        holders: dict[str, list[str]] = defaultdict(list)
        for rel, di in src_map.items():
            if di.startswith("ERR:"):
                continue
            holders[di].append(f"src:{rel}")
        for rel, di in dst_map.items():
            if di.startswith("ERR:"):
                continue
            holders[di].append(f"dst:{rel}")
        for rel, di in recon_map.items():
            if di.startswith("ERR:"):
                continue
            holders[di].append(f"recon:{rel}")
        shared = {di: h for di, h in holders.items() if len(h) > 1}
        # Filter: same dev:ino shared across domains is failure; within same root duplicates
        # (hardlinked files inside one .git) would also appear but none expected.
        cross = {}
        for di, h in shared.items():
            domains = set(x.split(":")[0] for x in h)
            if len(domains) > 1 or len(h) > 1 and len(set(h)) > 1:
                # Report any sharing; cross-domain is the critical case
                if len(domains) > 1:
                    cross[di] = h
        emit(f"inode dev:ino collisions total={len(shared)} cross-domain={len(cross)} (expected 0/0)")
        for di in sorted(cross)[:20]:
            emit(f"  shared {di} holders={cross[di][:4]}")
        if cross:
            emit("INODE_SHARING_FOUND=True FAIL")
            failures += 1
        else:
            emit("INODE_SHARING_FOUND=False OK (full .git domain: src vs dst vs reconstruct)")
        # also check worktree 21 files not hardlinked src<->dst
        wshare = []
        for rel in sorted(pins):
            try:
                a = (SOURCE / rel).stat()
                b = (dest / rel).stat()
                if (a.st_dev, a.st_ino) == (b.st_dev, b.st_ino):
                    wshare.append(rel)
            except OSError:
                pass
        emit(f"worktree 21 hardlink-shared src<->dst count={len(wshare)} expected=0")
        if wshare:
            for r in wshare:
                emit(f"  worktree shared: {r}")
            failures += 1
        else:
            emit("WORKTREE_INODE_OK")
        emit("")
    elif dest is not None:
        emit("=== PREP 7/8 skipped: dest absent (pre-copy mode) ===")
        emit("")
    emit(f"=== SUMMARY failures={failures} (0=current observation matches stated expectations; nonzero preserved, not hidden; NOT a generic PASS) ===")
    return 1 if failures else 0

if __name__ == "__main__":
    sys.exit(main())
