#!/usr/bin/env python3
"""HIGH-phase chain driver — ONE interleaved renewal chain per fixture pair.

Fresh fixtures (high23) from the current workdir snapshot; stages advance the
tool epoch by overlay+commit of the CURRENT workdir (caller applies exactly one
genuine tidy between stages — E4/E5/F3-tidy respectively):

  g1 (G1 epoch): U1 + C1, both routes (C1: real build + postrender reviews).
  g2 (G2 epoch): U2, both routes (prior = C1 r3: the C->U link).
  g3 (G3 epoch): U3, weekly only (prior = U2 r4: completes C->U->U + U-repeat).

Chain (weekly): r1 editorial -> U1 r2 -> C1 r3 -> U2 r4 -> U3 r5.
H row counts: 11 -> 21 -> 22 -> 31/32 -> 41 (verified live each activation).
All HIGH invocations use the CLI (exit-code evidence); review/QA building uses
fresh subprocesses with fixture-first imports (actual builders). Old E +
renewal authorities stay uncommitted; tool commits are genuine (never
--allow-empty, never artifact-only). No genuine approval implied.
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

REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
WORK = REPO / ".rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work"
EVID_BASE = REPO / "notes/rephase-1-versioned-renewal-implementation/phase-high/20261024T130000Z"
NOTES = EVID_BASE
sys.path.insert(0, str(NOTES))
from run_c1 import REVIEW_QA_BUILDER as C_QA_BUILDER  # noqa: E402 (C reviews+QA)
from run_repeat import U_QA_BUILDER  # noqa: E402 (U QA)

TOOL_DIRS = ("scripts", "schemas", "config", "templates", "tests", "docs",
             "specials", ".github")
TOOL_TOP_FILES = ("AGENTS.md", "README.md", ".latexmkrc", ".gitignore")


def run(cmd: list[str], cwd: Path, tag: str, env: dict, evdir: Path) -> subprocess.CompletedProcess:
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True,
                          timeout=900, env=env)
    (evdir / f"{tag}-stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (evdir / f"{tag}-stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    (evdir / f"{tag}-exit.txt").write_text(str(proc.returncode), encoding="utf-8")
    with open(evdir / "commands.log", "a", encoding="utf-8") as fh:
        fh.write(f"$ {' '.join(cmd[:8])}...  # cwd={cwd} -> exit={proc.returncode}\n")
    return proc


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clone_fixtures(parent: Path, env: dict, evdir: Path) -> dict[str, dict[str, str]]:
    boot = REPO / ".rephase-1-editorial-runtime/versioned-renewal-bootstrap-20261023T194449Z"
    out: dict[str, dict[str, str]] = {}
    for kind, src, issue, prop in (
            ("weekly", boot / "bootstrap-weekly", "2026-W37", "wk-boot-1"),
            ("longform", boot / "bootstrap-longform", "SP001", "lf-boot-1")):
        dst = parent / f"renewal-{kind}"
        if run(["git", "clone", "--no-hardlinks", str(src), str(dst)],
               REPO, f"clone-{kind}", env, evdir).returncode != 0:
            raise RuntimeError(f"clone {kind}")
        run(["git", "remote", "set-url", "origin",
             f"https://example.invalid/versioned-renewal-chain-{kind}.git"],
            dst, f"remote-{kind}", env, evdir)
        for key, val in (("user.name", "rephase-fixture"),
                         ("user.email", "fixture@example.invalid"),
                         ("commit.gpgsign", "false")):
            run(["git", "config", key, val], dst, f"cfg-{kind}-{key}", env, evdir)
        head = run(["git", "rev-parse", "HEAD"], dst, f"head-{kind}", env, evdir).stdout.strip()
        if head != "721a04d85532d7855f3e54cc411f5847c787726e":
            raise RuntimeError(f"{kind} HEAD {head}")
        if (dst / ".git" / "objects" / "info" / "alternates").exists():
            raise RuntimeError(f"{kind} alternates")
        src_status = run(["git", "status", "--porcelain=v1", "--untracked-files=normal"],
                         src, f"src-status-{kind}", env, evdir).stdout
        for line in src_status.splitlines():
            code, path = line[:2], line[3:].strip().strip('"')
            if code.strip() == "??" and (src / path).exists() \
                    and ".git" not in Path(path).parts:
                s, d = src / path, dst / path
                if d.exists():
                    raise RuntimeError(f"E target exists {kind} {path}")
                if s.is_dir() and not s.is_symlink():
                    shutil.copytree(str(s), str(d), symlinks=True, copy_function=shutil.copy2)
                else:
                    d.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(str(s), str(d))
        out[kind] = {"root": str(dst), "issue": issue, "prop": prop}
    return out


def overlay_commit(dst: Path, kind: str, message: str, env: dict, evdir: Path,
                   tag: str) -> str:
    for path in sorted(WORK.rglob("*")):
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        if not path.is_file() or path.suffix == ".pyc":
            continue
        rel = path.relative_to(WORK)
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(path), str(target))
    bad = [str(r.relative_to(WORK)) for r in sorted(WORK.rglob("*"))
           if r.is_file() and ".git" not in r.parts and "__pycache__" not in r.parts
           and r.suffix != ".pyc"
           and sha_file(dst / r.relative_to(WORK)) != sha_file(r)]
    (evdir / f"overlay-{tag}-{kind}.txt").write_text(f"mismatches={bad}\n", encoding="utf-8")
    if bad:
        raise RuntimeError(f"overlay mismatch {bad[:3]}")
    st = run(["git", "status", "--porcelain=v1", "--untracked-files=normal"],
             dst, f"status-{tag}-{kind}", env, evdir).stdout.splitlines()
    add: list[str] = []
    for line in st:
        code, path = line[:2], line[3:].strip().strip('"')
        if code.strip() == "M":
            add.append(path)
        elif code.strip() == "??":
            first = path.split("/")[0]
            if first in TOOL_DIRS or path in TOOL_TOP_FILES or first.startswith("."):
                if "__pycache__" not in path and not path.endswith(".pyc"):
                    add.append(path)
    (evdir / f"addlist-{tag}-{kind}.txt").write_text("\n".join(sorted(add)) + "\n", encoding="utf-8")
    if not add:
        raise RuntimeError(f"nothing to commit {tag} {kind} (epoch must move)")
    if run(["git", "add", "--"] + sorted(add), dst, f"add-{tag}-{kind}", env, evdir).returncode != 0:
        raise RuntimeError("git add")
    before = run(["git", "rev-parse", "HEAD"], dst, f"head-{tag}-pre-{kind}", env, evdir).stdout.strip()
    if run(["git", "commit", "-m", message, "--no-verify"], dst,
           f"commit-{tag}-{kind}", env, evdir).returncode != 0:
        raise RuntimeError("commit")
    after = run(["git", "rev-parse", "HEAD"], dst, f"head-{tag}-post-{kind}", env, evdir).stdout.strip()
    if after == before:
        raise RuntimeError("HEAD did not move")
    if run(["git", "merge-base", "--is-ancestor", before, "HEAD"],
           dst, f"ancestor-{tag}-{kind}", env, evdir).returncode != 0:
        raise RuntimeError("not ancestor")
    return after


def cli(root: str, args: list[str], env: dict, evdir: Path, tag: str) -> subprocess.CompletedProcess:
    return run([sys.executable, "-c",
                "import sys; sys.path.insert(0, sys.argv[1]); "
                "from scripts.survey_versioned_renewal_v2 import main; "
                "sys.exit(main(sys.argv[2:]))",
                root] + args, REPO, tag, env, evdir)


def renewal_paths(issue: str, prop: str, rid: str) -> dict[str, str]:
    pdir = f"sources/{issue}/publication/v2/editorial-corrections/{prop}"
    r_dir = f"{pdir}/renewals/{rid}"
    return {"pdir": pdir, "r_dir": r_dir, "state": f"sources/{issue}/production-state.json",
            "mspec": f"{pdir}/manuscript-spec.json", "tspec": f"{pdir}/toolchain-spec.json",
            "basis": f"{r_dir}/renewal-basis.json"}


def do_prepare(env: dict, evdir: Path, root: str, issue: str, prop: str, rid: str,
               intent: str, now_iso: str, tag: str) -> bool:
    p = renewal_paths(issue, prop, rid)
    args = ["prepare", "--root", root, "--state", p["state"], "--renewal-id", rid,
            "--intent", intent, "--manuscript-spec", p["mspec"],
            "--executor", "high-phase-fixture", "--recorded-at", now_iso]
    if intent == "RENDER_TARGETS":
        args += ["--toolchain-spec", p["tspec"]]
    rc = cli(root, args, env, evdir, f"{tag}-prepare-{rid}").returncode
    print(f"{tag}-prepare-{rid}: exit={rc}", flush=True)
    return rc == 0


def do_targets(env: dict, evdir: Path, root: str, basis_rel: str, now_iso: str, tag: str) -> bool:
    rc = cli(root, ["prepare-targets", "--root", root, "--basis", basis_rel,
                    "--executor", "high-phase-fixture", "--recorded-at", now_iso],
             env, evdir, f"{tag}-targets").returncode
    print(f"{tag}-targets: exit={rc}", flush=True)
    return rc == 0


def do_reviews_qa(env: dict, evdir: Path, root: str, issue: str, prop: str, rid: str,
                  now_iso: str, tag: str, c_mode: bool) -> dict | None:
    p = renewal_paths(issue, prop, rid)
    if c_mode:
        proc = run([sys.executable, "-c", C_QA_BUILDER, root, issue, prop, rid, now_iso,
                    "high-phase-fixture fresh C deterministic re-assertion"],
                   REPO, f"{tag}-reviews-qa", env, evdir)
    else:
        proc = run([sys.executable, "-c", U_QA_BUILDER, root, p["basis"], p["r_dir"],
                    p["pdir"], now_iso,
                    "high-phase-fixture fresh deterministic re-assertion"],
                   REPO, f"{tag}-qa", env, evdir)
    print(f"{tag}-reviews-qa: exit={proc.returncode}", flush=True)
    if proc.returncode != 0:
        return None
    # U builder prints the checks path (plain string); C builder prints JSON
    # {SEMANTIC_EDITORIAL, VISUAL, checks}.
    if c_mode:
        return json.loads((evdir / f"{tag}-reviews-qa-stdout.txt").read_text())
    return (evdir / f"{tag}-qa-stdout.txt").read_text().strip()


def do_finalize(env: dict, evdir: Path, root: str, issue: str, prop: str, rid: str,
                now_iso: str, tag: str, c_outs: dict | None, checks_rel: str) -> dict | None:
    p = renewal_paths(issue, prop, rid)
    args = ["finalize", "--root", root, "--state", p["state"], "--basis", p["basis"],
            "--checks", checks_rel, "--executor", "high-phase-fixture",
            "--recorded-at", now_iso]
    if c_outs is not None:
        args += ["--semantic-review", c_outs["SEMANTIC_EDITORIAL"],
                 "--visual-review", c_outs["VISUAL"]]
    rc_proc = cli(root, args, env, evdir, f"{tag}-finalize-{rid}")
    print(f"{tag}-finalize-{rid}: exit={rc_proc.returncode}", flush=True)
    if rc_proc.returncode != 0:
        return None
    return json.loads((evdir / f"{tag}-finalize-{rid}-stdout.txt").read_text())


def do_activate(env: dict, evdir: Path, root: str, issue: str, set_path: str,
                reason: str, now_iso: str, tag: str) -> dict | None:
    p_state = f"sources/{issue}/production-state.json"
    rc_proc = cli(root, ["activate", "--root", root, "--state", p_state, "--set", set_path,
                         "--reason", reason, "--executor", "high-phase-fixture",
                         "--recorded-at", now_iso], env, evdir, f"{tag}-activate")
    print(f"{tag}-activate: exit={rc_proc.returncode}", flush=True)
    if rc_proc.returncode != 0:
        return None
    return json.loads((evdir / f"{tag}-activate-stdout.txt").read_text())


def do_history(env: dict, evdir: Path, root: str, record_path: str, tag: str,
               expect_bindings: int) -> bool:
    rc_proc = cli(root, ["history", "--root", root, "--record", record_path],
                  env, evdir, f"{tag}-history")
    print(f"{tag}-history: exit={rc_proc.returncode} (expect {expect_bindings} bindings)",
          flush=True)
    if rc_proc.returncode != 0:
        return False
    got = json.loads((evdir / f"{tag}-history-stdout.txt").read_text())
    n = got.get("n_bindings", len(got.get("observed_source_bindings", [])))
    if n != expect_bindings:
        print(f"{tag}-history: BINDING COUNT {n} != {expect_bindings}", flush=True)
        return False
    return True


def do_u(env: dict, evdir: Path, root: str, issue: str, prop: str, rid: str,
         now_iso: str, tag: str, expect_bindings: int, reason: str) -> bool:
    p = renewal_paths(issue, prop, rid)
    if not do_prepare(env, evdir, root, issue, prop, rid, "REUSE_TARGETS", now_iso, tag):
        return False
    outs = do_reviews_qa(env, evdir, root, issue, prop, rid, now_iso, tag, False)
    if outs is None:
        return False
    fin = do_finalize(env, evdir, root, issue, prop, rid, now_iso, tag, None, outs)
    if fin is None:
        return False
    act = do_activate(env, evdir, root, issue, fin["set_path"], reason, now_iso, tag)
    if act is None:
        return False
    return do_history(env, evdir, root, act["record_path"], tag, expect_bindings)


def do_c(env: dict, evdir: Path, root: str, issue: str, prop: str, rid: str,
         now_iso: str, tag: str, expect_bindings: int, reason: str) -> bool:
    p = renewal_paths(issue, prop, rid)
    if not do_prepare(env, evdir, root, issue, prop, rid, "RENDER_TARGETS", now_iso, tag):
        return False
    if not do_targets(env, evdir, root, p["basis"], now_iso, tag):
        return False
    outs = do_reviews_qa(env, evdir, root, issue, prop, rid, now_iso, tag, True)
    if outs is None:
        return False
    fin = do_finalize(env, evdir, root, issue, prop, rid, now_iso, tag, outs, outs["checks"])
    if fin is None:
        return False
    act = do_activate(env, evdir, root, issue, fin["set_path"], reason, now_iso, tag)
    if act is None:
        return False
    return do_history(env, evdir, root, act["record_path"], tag, expect_bindings)


def main() -> int:
    stage = sys.argv[1] if len(sys.argv) > 1 else "g1"
    evdir = EVID_BASE / f"run36-20261025T040000Z-{stage}"
    evdir.mkdir(parents=True, exist_ok=True)
    (evdir / "commands.log").write_text("", encoding="utf-8")
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        if os.environ.get(name):
            print(f"FATAL: inherited {name}", file=sys.stderr)
            return 1
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["LC_ALL"] = "C"
    now_iso = datetime.now(timezone.utc).isoformat()
    print(f"STAGE {stage} (chain driver via HIGH CLI)", flush=True)
    if stage == "g1":
        parent = REPO / ".rephase-1-editorial-runtime/versioned-renewal-high24-20261025T040000Z"
        if parent.exists():
            print(f"FATAL: parent exists {parent}", file=sys.stderr)
            return 1
        parent.mkdir(parents=True, exist_ok=False)
        fx = clone_fixtures(parent, env, evdir)
        ok = True
        for kind in ("weekly", "longform"):
            root, issue, prop = fx[kind]["root"], fx[kind]["issue"], fx[kind]["prop"]
            overlay_commit(Path(root), kind, "HIGH phase TEST-ONLY: G1 base implementation", env,
                           evdir, "g1")
            ok &= do_u(env, evdir, root, issue, prop, f"high-u1-{kind}", now_iso,
                       f"g1-u1-{kind}", 21,
                       "Core change: versioned renewal HIGH+consumer implementation")
            # C1 prior is U1 r2 (C-after-U): 11 editorial + 10 U-OWN + 11 C-OWN = 32.
            ok &= do_c(env, evdir, root, issue, prop, f"high-c1-{kind}", now_iso,
                       f"g1-c1-{kind}", 32,
                       "Core change: same-reader renewal with new rendered targets (real TL build)")
        print("G1 " + ("OK" if ok else "FAILED"), flush=True)
        return 0 if ok else 1
    if stage == "g2":
        # G2 epoch: overlay CURRENT workdir (E5 tidy) + commit, then U2 both
        # routes with prior=C1 r3 (the C->U link): 32 + 10 = 42 bindings.
        if len(sys.argv) < 3:
            print("g2 needs parent path argv[2]", file=sys.stderr)
            return 1
        parent = Path(sys.argv[2])
        ok = True
        for kind, issue, prop in (("weekly", "2026-W37", "wk-boot-1"),
                                  ("longform", "SP001", "lf-boot-1")):
            root = str(parent / f"renewal-{kind}")
            overlay_commit(Path(root), kind, "HIGH phase TEST-ONLY: G2 epoch (E5 loop-variable tidy)",
                           env, evdir, "g2")
            ok &= do_u(env, evdir, root, issue, prop, f"high-u2-{kind}", now_iso,
                       f"g2-u2-{kind}", 42,
                       "Core change: G2 epoch advancing the renewal tool chain")
        print("G2 " + ("OK" if ok else "FAILED"), flush=True)
        return 0 if ok else 1
    if stage == "g3":
        # G3 epoch: overlay CURRENT workdir (F3 tidy) + commit, then U3 weekly
        # with prior=U2 r4 (completes C->U->U and U-repeat depth): 42+10 = 52.
        if len(sys.argv) < 3:
            print("g3 needs parent path argv[2]", file=sys.stderr)
            return 1
        parent = Path(sys.argv[2])
        root = str(parent / "renewal-weekly")
        overlay_commit(Path(root), "weekly", "HIGH phase TEST-ONLY: G3 epoch (F3 tidy)",
                       env, evdir, "g3")
        ok = do_u(env, evdir, root, "2026-W37", "wk-boot-1", "high-u3-weekly", now_iso,
                  "g3-u3-weekly", 52,
                  "Core change: G3 epoch advancing the renewal tool chain")
        print("G3 " + ("OK" if ok else "FAILED"), flush=True)
        return 0 if ok else 1
    print(f"unknown stage {stage}", file=sys.stderr)
    return 1
    print("DONE CHAIN-" + stage.upper())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
