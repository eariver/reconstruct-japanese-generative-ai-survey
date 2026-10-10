#!/usr/bin/env python3
"""LF-2I R3 correction strict asserting evidence runner (new tool, not old-script reuse).

Addresses root R2 E1-E3 on top of the prior correction runner:
- E1: forced no-network Git env (GIT_NO_LAZY_FETCH=1, GIT_OPTIONAL_LOCKS=0,
  GIT_ALLOW_PROTOCOL=file) for BOTH runner-owned git calls and children, plus
  PYTHONDONTWRITEBYTECODE=1 / GIT_TERMINAL_PROMPT=0; routing overrides
  (GIT_* / PYTHONPATH / PYTHONHOME / PYTHONSTARTUP / PYTHONOPTIMIZE) rejected
  before every candidate Git operation; optimized interpreter mode rejected;
  actual environment / interpreter / exact child argv recorded.
- E2: real guard proofs on NEW independent full disposable composites (9 files
  + own Git DB + own HEAD) invoking the same pre/post guard code: wrong source
  before child -> nonzero with no child sentinel; failing child -> nonzero
  with postguard recorded; child0 + source drift -> nonzero postguard. Direct
  numeric returncode capture, exclusive proof log, no candidate canary. The
  prior hash-inequality toy is preserved only as superseded logic probes in the
  old packet, not as runner proof here.
- E3: the exact SAVED complete-overlay.patch is applied as saved (git apply
  --check, then git apply) to a NEW isolated byte-copy (cp -a, no git archive,
  no clone) of the ORIGINAL clean 409 source DB
  /tmp/opencode/jgas-dm004-impl-20261004T234416Z; all-9 hashes + logical git
  modes + physical modes + status set + HEAD + object inode isolation compared.
  No candidate commits/refs; old 2-file-tmpdir+live-copy construction is
  superseded (preserved in the old packet).

Old 44-method result is historical, not transferred. Scope here: full focused
LF-2I integration module at fixed final hashes plus justified affected controls
(Gate module: publisher review validation + receipt replay depend on its review
loader/derivation dispatch; 3 LF-1 loader controls: derivation authority
boundary). Full-repo syntax/compile sweeps are unaffected (no schema/config
change) and not rerun.

Usage: python3 run_lf2i_correction3.py [--timeout SEC]
Writes run.log / manifest.json / apply.log / complete-overlay.patch /
hash-manifest.json / proofs.log exclusively; never overwrites.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


DESIGN = Path("/tmp/opencode/jgas-lf2-design-20261009T113013Z")
ORIG409 = Path("/tmp/opencode/jgas-dm004-impl-20261004T234416Z")
EVIDENCE = Path(__file__).resolve().parent
BASE_HEAD = "409b292756dd1277b9dfae87679934c0d2ce251c"
BASE_TREE = "8ce3699861505f32d1d60bdc185d4d4f635aedb2"
BASE_PARENT = "34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4"
# Final R2-corrected pins (2M+7A). Any subsequent path change must be declared.
EXPECTED = {
    "scripts/survey_reader_surface_gate_v2.py": {
        "sha256": "e73058841cfa1a841030b96d5cd2fb756c6ba99d1b99522ddbf0131d1f06bbe4",
        "mode": "664",
    },
    "schemas/reader-surface-gate-v2.schema.json": {
        "sha256": "fe4a96f4aa87f2a527096c4d3040f92e0217ef972ddae1d7140498184a13322c",
        "mode": "664",
    },
    "schemas/longform-publication-source-manifest-v2.schema.json": {
        "sha256": "4dadf873096f31cf564a7db4fee42a1fc8cdd8fc039dd14a7ee01cf26043e8ca",
        "mode": "664",
    },
    "schemas/longform-reader-input-v2.schema.json": {
        "sha256": "7bae9d2ac753c83521165c76c9e461ce40ac4e704d9b44d3518ae7b88fbd0643",
        "mode": "664",
    },
    "scripts/survey_longform_derivation_v2.py": {
        "sha256": "c09c5558f9668906b7d2ed34c55281d5f6d9ed279d3237a8ffc18ac84ea41149",
        "mode": "664",
    },
    "scripts/survey_longform_generated_v2.py": {
        "sha256": "d480e11d1c398f79f3e894e2e1e1f56ceec507dfde376a163a58b0ebed97d3c2",
        "mode": "664",
    },
    "scripts/survey_longform_semantic_publication_v2.py": {
        "sha256": "4d235a388955dcedd34d6a7dc5ac7761f9fc91de8bc723eb11f68cec6a229195",
        "mode": "664",
    },
    "tests/test_survey_longform_derivation_v2.py": {
        "sha256": "ce687447539a99eb92532bc34246a271fb489b259e63b31ed6699fcc12fbf913",
        "mode": "664",
    },
    "tests/test_survey_longform_publication_integration_v2.py": {
        "sha256": "4a03b564f8fa4dd39f2b48766ddb7612cf2d8d4dacdcc42ac39f637d2bca11a4",
        "mode": "664",
    },
}
M_FILES = (
    "scripts/survey_reader_surface_gate_v2.py",
    "schemas/reader-surface-gate-v2.schema.json",
)
A_FILES = (
    "scripts/survey_longform_derivation_v2.py",
    "schemas/longform-reader-input-v2.schema.json",
    "tests/test_survey_longform_derivation_v2.py",
    "scripts/survey_longform_generated_v2.py",
    "scripts/survey_longform_semantic_publication_v2.py",
    "schemas/longform-publication-source-manifest-v2.schema.json",
    "tests/test_survey_longform_publication_integration_v2.py",
)
GIT_OVERRIDE_VARS = (
    "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR",
)
PYTHON_OVERRIDE_VARS = ("PYTHONPATH", "PYTHONHOME", "PYTHONSTARTUP", "PYTHONOPTIMIZE")
# E1 forced no-network Git posture, applied to runner-owned git calls AND children.
FORCED_GIT_ENV = {
    "GIT_NO_LAZY_FETCH": "1",
    "GIT_OPTIONAL_LOCKS": "0",
    "GIT_ALLOW_PROTOCOL": "file",
}
DEFAULT_TESTS = (
    "tests.test_survey_longform_publication_integration_v2",
    "tests.test_survey_reader_surface_gate_v2",
    "tests.test_survey_longform_derivation_v2.LongformDerivationV2Tests"
    ".test_valid_single_did_projects_every_category",
    "tests.test_survey_longform_derivation_v2.LongformDerivationV2Tests"
    ".test_directive_file_presence_refuses",
    "tests.test_survey_longform_derivation_v2.LongformDerivationV2Tests"
    ".test_earlier_lifecycle_state_refuses",
)
PROOF_FILES = ("proofs.log",)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mode_of(path: Path) -> str:
    return oct(stat.S_IMODE(path.stat().st_mode))[2:]


def assert_clean_env(phase: str, record: dict) -> None:
    """Reject routing/optimization overrides before every candidate Git operation."""
    present_git = sorted(v for v in GIT_OVERRIDE_VARS if os.environ.get(v))
    present_py = sorted(v for v in PYTHON_OVERRIDE_VARS if os.environ.get(v))
    record.setdefault("env_checks", {})[phase] = {
        "git_present": present_git,
        "python_present": present_py,
        "optimize_flag": sys.flags.optimize,
    }
    assert not present_git, f"{phase}: refusing Git routing override: {present_git}"
    assert not present_py, f"{phase}: refusing Python routing/optimization override: {present_py}"
    assert sys.flags.optimize == 0, f"{phase}: refusing optimized interpreter mode"


def git_env() -> dict[str, str]:
    env = dict(os.environ)
    env.update(FORCED_GIT_ENV)
    return env


def git_checked(repo: Path, args: list[str], phase: str, record: dict, **kwargs) -> subprocess.CompletedProcess:
    assert_clean_env(phase, record)
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                          env=git_env(), **kwargs)


def child_env() -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if k not in (*GIT_OVERRIDE_VARS, *PYTHON_OVERRIDE_VARS)}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["GIT_TERMINAL_PROMPT"] = "0"
    env.update(FORCED_GIT_ENV)
    return env


def exclusive_write(path: Path, data: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(fd, "wb") as handle:
        handle.write(data)


def identity_for(root: Path, phase: str, record: dict) -> dict:
    head_p = git_checked(root, ["rev-parse", "HEAD"], phase, record)
    tree_p = git_checked(root, ["rev-parse", "HEAD^{tree}"], phase, record)
    parent_p = git_checked(root, ["rev-parse", "HEAD~1"], phase, record)
    status_p = git_checked(root, ["status", "--porcelain=v1", "--untracked-files=all"], phase, record)
    overlay: dict[str, dict[str, str]] = {}
    for rel in (*M_FILES, *A_FILES):
        p = root / rel
        overlay[rel] = {"sha256": sha256_file(p), "mode": mode_of(p)}
    return {
        "head": head_p.stdout.strip(), "head_exit": head_p.returncode,
        "tree": tree_p.stdout.strip(), "tree_exit": tree_p.returncode,
        "parent": parent_p.stdout.strip(), "parent_exit": parent_p.returncode,
        "status": status_p.stdout, "status_exit": status_p.returncode,
        "overlay": overlay,
    }


def guard_overlay(root: Path, expected: dict, base_head: str, base_tree: str, base_parent: str,
                  m_files: tuple[str, ...], a_files: tuple[str, ...],
                  tag: str, record: dict) -> tuple[int, dict]:
    """Same pre/post guard used by the runner and the E2 proofs (code-returning).

    Returns (0, ident) on pass, (1, ident-or-error) on refusal. Never raises.
    """
    try:
        ident = identity_for(root, f"guard-{tag}", record)
    except (AssertionError, OSError) as exc:
        return 1, {"error": f"{tag}: identity collection failed: {exc}"}
    for key, want, label in (("head_exit", 0, "rev-parse HEAD"), ("tree_exit", 0, "rev-parse tree"),
                             ("parent_exit", 0, "rev-parse parent"), ("status_exit", 0, "status")):
        if ident[key] != want:
            return 1, {"error": f"{tag}: git {label} exit {ident[key]}", "ident": ident}
    if ident["head"] != base_head:
        return 1, {"error": f"{tag}: HEAD drift {ident['head']}", "ident": ident}
    if ident["tree"] != base_tree:
        return 1, {"error": f"{tag}: tree drift {ident['tree']}", "ident": ident}
    if ident["parent"] != base_parent:
        return 1, {"error": f"{tag}: parent drift {ident['parent']}", "ident": ident}
    for rel, pin in expected.items():
        got = ident["overlay"][rel]
        if got["sha256"] != pin["sha256"]:
            return 1, {"error": f"{tag}: source hash drift {rel} {got['sha256']}", "ident": ident}
        if got["mode"] != pin["mode"]:
            return 1, {"error": f"{tag}: source mode drift {rel} {got['mode']}", "ident": ident}
    rows = [r for r in ident["status"].splitlines() if r.strip()]
    cache_rows = [r for r in rows if "__pycache__" in r or r.strip().endswith(".pyc")]
    src_rows = [r for r in rows if r not in cache_rows]
    allowed = {f"?? {rel}" for rel in a_files} | {f" M {rel}" for rel in m_files}
    unexpected = [r for r in src_rows if r not in allowed]
    if unexpected:
        return 1, {"error": f"{tag}: unexpected working-tree delta: {unexpected}", "ident": ident}
    if len(src_rows) != len(allowed):
        return 1, {"error": f"{tag}: overlay set changed: {src_rows}", "ident": ident}
    ident["cache_side_effects"] = cache_rows
    return 0, ident


def check_identity(tag: str, manifest: dict) -> None:
    rc, detail = guard_overlay(DESIGN, EXPECTED, BASE_HEAD, BASE_TREE, BASE_PARENT,
                               M_FILES, A_FILES, tag, manifest)
    manifest[f"identity_{tag}"] = detail.get("ident", detail)
    assert rc == 0, detail.get("error", f"{tag}: guard failed")


def run_child(argv: list[str], cwd: Path, timeout: int, log_path: Path,
              manifest: dict, key: str) -> int | None:
    """Launch a child with the forced env, exclusive log, direct returncode."""
    manifest[f"{key}_argv"] = argv
    log_fd = os.open(log_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    child = subprocess.Popen(argv, cwd=str(cwd), stdout=log_fd, stderr=subprocess.STDOUT,
                             env=child_env())
    os.close(log_fd)
    try:
        return child.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        child.kill()
        child.wait()
        return None


def new_disposable_composite(parent: Path, record: dict, label: str) -> Path:
    """NEW independent full disposable composite: 9 files + own Git DB + own HEAD."""
    dest = parent / label
    for rel in (*M_FILES, *A_FILES):
        src = DESIGN / rel
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(src.read_bytes())
        os.chmod(target, 0o664)
    assert_clean_env(f"proof-{label}-git", record)
    fx = dict(os.environ)
    fx.update(child_env())
    fx.update({"GIT_AUTHOR_NAME": "LF-2I Disposable Proof", "GIT_AUTHOR_EMAIL": "proof@example.invalid",
               "GIT_COMMITTER_NAME": "LF-2I Disposable Proof", "GIT_COMMITTER_EMAIL": "proof@example.invalid"})
    ident = ["-c", "user.name=LF-2I Disposable Proof", "-c", "user.email=proof@example.invalid"]
    # Mirror the real overlay state exactly: commit the 2 base (HEAD-blob)
    # files, then lay the 7 new files plus the 2 modified files uncommitted in
    # the worktree, so worktree status is exactly 2M+7A and the SAME guard
    # parameters (M_FILES/A_FILES/EXPECTED shape) apply.
    base_blobs: dict[str, bytes] = {}
    for rel in M_FILES:
        proc = subprocess.run(["git", "-C", str(DESIGN), "show", f"HEAD:{rel}"],
                              capture_output=True, env=git_env())
        assert proc.returncode == 0, f"{label}: HEAD blob missing for {rel}"
        base_blobs[rel] = proc.stdout
    steps = [(["git", "init", "-q"], None),
             (["git", "commit", "-q", "--allow-empty", "-m", "disposable proof root"], None)]
    for args, _ in steps:
        proc = subprocess.run(args, cwd=str(dest), capture_output=True, text=True, env=fx)
        assert proc.returncode == 0, f"{label}: disposable git setup failed: {args} {proc.stderr[:500]}"
    for rel, blob in base_blobs.items():
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(blob)
    proc = subprocess.run(["git", "add", "--", *M_FILES], cwd=str(dest),
                          capture_output=True, text=True, env=fx)
    assert proc.returncode == 0, f"{label}: disposable git add failed: {proc.stderr[:500]}"
    proc = subprocess.run(["git", *ident, "commit", "-q", "-m", "disposable proof base"],
                          cwd=str(dest), capture_output=True, text=True, env=fx)
    assert proc.returncode == 0, f"{label}: disposable git commit failed: {proc.stderr[:500]}"
    # Lay the overlay bytes uncommitted: worktree status is now exactly 2M+7A.
    for rel in M_FILES:
        target = dest / rel
        target.write_bytes((DESIGN / rel).read_bytes())
        os.chmod(target, 0o664)
    return dest


def disposable_base(root: Path, record: dict, label: str) -> tuple[str, str, str]:
    head = git_checked(root, ["rev-parse", "HEAD"], f"proof-{label}", record)
    tree = git_checked(root, ["rev-parse", "HEAD^{tree}"], f"proof-{label}", record)
    parent = git_checked(root, ["rev-parse", "HEAD~1"], f"proof-{label}", record)
    assert head.returncode == 0 and tree.returncode == 0 and parent.returncode == 0
    return head.stdout.strip(), tree.stdout.strip(), parent.stdout.strip()


def proof_suite(manifest: dict) -> int:
    """E2 real proofs on NEW independent full disposable composites.

    Returns 0 iff all three proofs behave exactly as required; each proof maps
    to a distinct nonzero driver code otherwise. Proof log is exclusive.
    """
    lines: list[str] = []
    proofs: dict[str, object] = {}

    def log(text: str) -> None:
        lines.append(text)

    with tempfile.TemporaryDirectory(prefix="jgas-lf2i-proof-") as tmp:
        parent = Path(tmp)
        # Proof A: wrong source before child -> pre-guard nonzero, child never launched.
        dest_a = new_disposable_composite(parent, manifest, "proofA")
        base_a = disposable_base(dest_a, manifest, "proofA")
        (dest_a / "scripts/survey_longform_generated_v2.py").write_bytes(b"# drifted\n")
        rc_a, detail_a = guard_overlay(dest_a, EXPECTED, *base_a, M_FILES, A_FILES, "proofA-pre", manifest)
        sentinel_a = dest_a / "child-sentinel.txt"
        child_launched_a = False
        if rc_a == 0:
            child_launched_a = True
            sentinel_a.write_text("launched\n", encoding="utf-8")
        ok_a = (rc_a != 0) and (not child_launched_a) and (not sentinel_a.exists())
        log(f"proofA pre-guard exit-mapping={rc_a} child_launched={child_launched_a} "
            f"sentinel_exists={sentinel_a.exists()} detail={detail_a.get('error', 'n/a')}")
        proofs["A"] = {"guard_rc": rc_a, "child_launched": child_launched_a,
                       "sentinel_exists": sentinel_a.exists(), "pass": ok_a}
        if not ok_a:
            exclusive_write(EVIDENCE / "proofs.log", ("\n".join(lines) + "\n").encode())
            manifest["disposable_proofs"] = proofs
            return 20
        # Proof B: correct source, failing child -> child exit 7 observed, driver nonzero.
        dest_b = new_disposable_composite(parent, manifest, "proofB")
        base_b = disposable_base(dest_b, manifest, "proofB")
        rc_b, detail_b = guard_overlay(dest_b, EXPECTED, *base_b, M_FILES, A_FILES, "proofB-pre", manifest)
        child_exit_b: int | None = -1
        if rc_b == 0:
            argv_b = [sys.executable, "-c", "import sys; sys.exit(7)"]
            proc_b = subprocess.run(argv_b, capture_output=True, text=True, env=child_env())
            child_exit_b = proc_b.returncode
        rc_bpost, detail_bpost = guard_overlay(dest_b, EXPECTED, *base_b, M_FILES, A_FILES,
                                               "proofB-post", manifest)
        log(f"proofB pre-guard={rc_b} child_argv={[sys.executable, '-c', 'import sys; sys.exit(7)']} "
            f"child_exit={child_exit_b} postguard={rc_bpost} "
            f"postdetail={detail_bpost.get('error', 'pass')}")
        ok_b = (rc_b == 0) and (child_exit_b == 7) and (rc_bpost == 0)
        proofs["B"] = {"pre_rc": rc_b, "child_exit": child_exit_b, "post_rc": rc_bpost, "pass": ok_b}
        if not ok_b:
            exclusive_write(EVIDENCE / "proofs.log", ("\n".join(lines) + "\n").encode())
            manifest["disposable_proofs"] = proofs
            return 21
        # Proof C: correct source, child0, then drift -> post-guard nonzero.
        dest_c = new_disposable_composite(parent, manifest, "proofC")
        base_c = disposable_base(dest_c, manifest, "proofC")
        rc_c, _ = guard_overlay(dest_c, EXPECTED, *base_c, M_FILES, A_FILES, "proofC-pre", manifest)
        child_exit_c: int | None = -1
        sentinel_c = dest_c / "child-sentinel.txt"
        if rc_c == 0:
            argv_c = [sys.executable, "-c",
                      f"open({str(sentinel_c)!r}, 'w').write('child-ok\\n')"]
            proc_c = subprocess.run(argv_c, capture_output=True, text=True, env=child_env())
            child_exit_c = proc_c.returncode
        (dest_c / "scripts/survey_longform_generated_v2.py").write_bytes(b"# post-child drift\n")
        rc_cpost, detail_cpost = guard_overlay(dest_c, EXPECTED, *base_c, M_FILES, A_FILES,
                                               "proofC-post", manifest)
        log(f"proofC pre-guard={rc_c} child_exit={child_exit_c} "
            f"sentinel_exists={sentinel_c.exists()} postguard={rc_cpost} "
            f"postdetail={detail_cpost.get('error', 'n/a')}")
        ok_c = (rc_c == 0) and (child_exit_c == 0) and sentinel_c.exists() and (rc_cpost != 0)
        proofs["C"] = {"pre_rc": rc_c, "child_exit": child_exit_c,
                       "sentinel_exists": sentinel_c.exists(), "post_rc": rc_cpost, "pass": ok_c}
        if not ok_c:
            exclusive_write(EVIDENCE / "proofs.log", ("\n".join(lines) + "\n").encode())
            manifest["disposable_proofs"] = proofs
            return 22
    exclusive_write(EVIDENCE / "proofs.log", ("\n".join(lines) + "\n").encode())
    manifest["disposable_proofs"] = proofs
    return 0


def object_inodes(repo: Path) -> set[int]:
    out: set[int] = set()
    for path in (repo / ".git" / "objects").rglob("*"):
        if path.is_file() and not path.is_symlink():
            out.add(path.stat().st_ino)
    return out


def apply_proof(manifest: dict) -> int:
    """E3: apply the exact SAVED complete patch to a NEW byte-copy of ORIG409."""
    apply_lines: list[str] = []
    patch_path = EVIDENCE / "complete-overlay.patch"
    if not patch_path.is_file():
        manifest["apply"] = "FAIL: saved complete-overlay.patch missing"
        return 5
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    bytecopy = Path(f"/tmp/opencode/jgas-lf2i-409bytecopy-{stamp}")
    try:
        assert_clean_env("apply-env", manifest)
        cp = subprocess.run(["cp", "-a", str(ORIG409), str(bytecopy)], capture_output=True, text=True)
        apply_lines.append(f"cp -a ORIG409 bytecopy exit: {cp.returncode} {cp.stderr[:500]}")
        assert cp.returncode == 0, "byte copy failed"
        head = git_checked(bytecopy, ["rev-parse", "HEAD"], "apply-head", manifest)
        apply_lines.append(f"bytecopy HEAD: {head.stdout.strip()} exit: {head.returncode}")
        assert head.returncode == 0 and head.stdout.strip() == BASE_HEAD, "bytecopy HEAD is not 409"
        st = git_checked(bytecopy, ["status", "--porcelain=v1", "--untracked-files=all"], "apply-status", manifest)
        apply_lines.append(f"bytecopy pre-status: {st.stdout!r} exit: {st.returncode}")
        assert st.returncode == 0 and not st.stdout.strip(), "bytecopy is not clean"
        rem = git_checked(bytecopy, ["remote", "-v"], "apply-remote", manifest)
        apply_lines.append(f"bytecopy remotes: {rem.stdout.strip()!r}")
        alt = bytecopy / ".git" / "objects" / "info" / "alternates"
        apply_lines.append(f"bytecopy alternates present: {alt.exists()}")
        assert not alt.exists(), "bytecopy has alternates"
        orig_inodes = object_inodes(ORIG409)
        copy_inodes = object_inodes(bytecopy)
        apply_lines.append(f"orig objects: {len(orig_inodes)} copy objects: {len(copy_inodes)} "
                           f"shared: {len(orig_inodes & copy_inodes)}")
        assert not (orig_inodes & copy_inodes), "bytecopy shares object inodes with original"
        manifest["bytecopy"] = str(bytecopy)
        chk = subprocess.run(["git", "apply", "--check", "-v", str(patch_path)],
                             cwd=str(bytecopy), capture_output=True, text=True, env=git_env())
        apply_lines.append(f"git apply --check saved-patch exit: {chk.returncode}")
        apply_lines.append(f"--check stdout: {chk.stdout[:2000]}")
        apply_lines.append(f"--check stderr: {chk.stderr[:2000]}")
        assert chk.returncode == 0, "saved complete patch does not apply onto clean 409"
        ap = subprocess.run(["git", "apply", "-v", str(patch_path)],
                            cwd=str(bytecopy), capture_output=True, text=True, env=git_env())
        apply_lines.append(f"git apply saved-patch exit: {ap.returncode}")
        apply_lines.append(f"apply stdout: {ap.stdout[:2000]}")
        apply_lines.append(f"apply stderr: {ap.stderr[:2000]}")
        assert ap.returncode == 0, "saved complete patch application failed"
        head2 = git_checked(bytecopy, ["rev-parse", "HEAD"], "apply-head2", manifest)
        assert head2.stdout.strip() == BASE_HEAD, "HEAD moved during apply"
        apply_lines.append(f"post-apply HEAD: {head2.stdout.strip()}")
        st2 = git_checked(bytecopy, ["status", "--porcelain=v1", "--untracked-files=all"], "apply-status2", manifest)
        rows = sorted(r for r in st2.stdout.splitlines() if r.strip())
        apply_lines.append(f"post-apply status rows: {rows}")
        expected_rows = sorted([f" M {rel}" for rel in M_FILES] + [f"?? {rel}" for rel in A_FILES])
        assert rows == expected_rows, f"post-apply status is not exactly 2M+7A: {rows}"
        mismatches = [rel for rel in (*M_FILES, *A_FILES)
                      if sha256_file(bytecopy / rel) != EXPECTED[rel]["sha256"]]
        apply_lines.append(f"byte-compare mismatches: {mismatches}")
        assert not mismatches, f"apply content mismatch: {mismatches}"
        mode_mismatch = [rel for rel in (*M_FILES, *A_FILES) if mode_of(bytecopy / rel) != EXPECTED[rel]["mode"]]
        apply_lines.append(f"physical-mode mismatches: {mode_mismatch}")
        assert not mode_mismatch, f"mode mismatch: {mode_mismatch}"
        ls = git_checked(bytecopy, ["ls-files", "-s", "--", *M_FILES], "apply-lsfiles", manifest)
        apply_lines.append(f"ls-files -s M: {ls.stdout.strip()!r}")
        manifest["apply"] = "PASS"
    except (AssertionError, subprocess.CalledProcessError, OSError) as exc:
        manifest["apply"] = f"FAIL: {exc}"
    exclusive_write(EVIDENCE / "apply.log", ("\n".join(apply_lines) + "\n").encode())
    return 0 if manifest.get("apply") == "PASS" else 5


def save_patch(manifest: dict) -> None:
    """Save the TRUE complete patch: M diff plus clean new-file diffs, no markers."""
    assert_clean_env("savepatch-env", manifest)
    m_diff = subprocess.run(["git", "-C", str(DESIGN), "diff", "HEAD", "--", *M_FILES],
                            capture_output=True, env=git_env())
    assert m_diff.returncode == 0, "M diff failed"
    parts: list[bytes] = [m_diff.stdout]
    newdiff_exits: dict[str, int] = {}
    for rel in A_FILES:
        nd = subprocess.run(["git", "diff", "--no-index", "--", "/dev/null", rel],
                            capture_output=True, cwd=str(DESIGN), env=git_env())
        # git diff --no-index exits 1 on differences: expected difference signal.
        newdiff_exits[rel] = nd.returncode
        assert nd.returncode in (0, 1), f"new-file diff failed for {rel}"
        assert b"new file mode" in nd.stdout, f"new-file diff has no mode header for {rel}"
        parts.append(nd.stdout)
    exclusive_write(EVIDENCE / "complete-overlay.patch", b"".join(parts))
    exclusive_write(EVIDENCE / "hash-manifest.json", (json.dumps(EXPECTED, indent=2) + "\n").encode())
    manifest["newfile_diff_exits"] = newdiff_exits


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=int, default=2400)
    parser.add_argument("--tests", default=" ".join(DEFAULT_TESTS))
    args = parser.parse_args()
    for name in ("run.log", "manifest.json", "apply.log", "complete-overlay.patch",
                 "hash-manifest.json", "proofs.log"):
        if (EVIDENCE / name).exists():
            print(f"refusing to overwrite prior evidence: {name}", file=sys.stderr)
            return 2
    git_version = subprocess.run(["git", "--version"], capture_output=True, text=True, env=git_env())
    manifest: dict = {
        "runner": Path(__file__).name,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "runtime": sys.version,
        "sys_flags_optimize": sys.flags.optimize,
        "git_version": git_version.stdout.strip(),
        "forced_git_env": FORCED_GIT_ENV,
        "argv": sys.argv,
        "tests": args.tests.split(),
        "timeout_sec": args.timeout,
        "cwd": os.getcwd(),
        "tmpdir": os.environ.get("TMPDIR", ""),
        "design": str(DESIGN),
        "orig409": str(ORIG409),
        "env": {k: os.environ.get(k, "") for k in ("PATH", "LANG", "LC_ALL", "TZ")},
        "base": {"head": BASE_HEAD, "tree": BASE_TREE, "parent": BASE_PARENT},
        "expected_overlay": EXPECTED,
    }
    save_patch(manifest)
    try:
        proof_rc = proof_suite(manifest)
    except Exception as exc:  # unexpected proof harness failure, not a guard verdict
        manifest["proofs"] = f"HARNESS-ERROR: {type(exc).__name__}: {exc}"
        exclusive_write(EVIDENCE / "manifest.json", (json.dumps(manifest, indent=2) + "\n").encode())
        print(f"DISPOSABLE-PROOF HARNESS ERROR: {exc}", file=sys.stderr)
        return 2
    if proof_rc != 0:
        manifest["proofs"] = f"FAIL driver={proof_rc}"
        exclusive_write(EVIDENCE / "manifest.json", (json.dumps(manifest, indent=2) + "\n").encode())
        print(f"DISPOSABLE-PROOF FAIL driver={proof_rc}; see proofs.log", file=sys.stderr)
        return 2
    manifest["proofs"] = "PASS"
    try:
        check_identity("pre", manifest)
    except AssertionError as exc:
        manifest["precheck"] = f"REFUSED: {exc}"
        exclusive_write(EVIDENCE / "manifest.json", (json.dumps(manifest, indent=2) + "\n").encode())
        print(f"PRE-CHECK REFUSED: {exc}", file=sys.stderr)
        return 2
    manifest["precheck"] = "PASS"
    child_argv = [sys.executable, "-m", "unittest", "-v", *args.tests.split()]
    exit_code = run_child(child_argv, DESIGN, args.timeout, EVIDENCE / "run.log", manifest, "child")
    if exit_code is None:
        manifest["child"] = {"exit": None, "timeout": True}
        try:
            check_identity("post", manifest)
            manifest["postcheck"] = "PASS"
        except AssertionError as exc:
            manifest["postcheck"] = f"FAIL: {exc}"
        exclusive_write(EVIDENCE / "manifest.json", (json.dumps(manifest, indent=2) + "\n").encode())
        print(f"CHILD TIMEOUT after {args.timeout}s; partial output preserved in run.log", file=sys.stderr)
        return 3
    manifest["child"] = {"exit": exit_code, "timeout": False}
    try:
        check_identity("post", manifest)
        manifest["postcheck"] = "PASS"
    except AssertionError as exc:
        manifest["postcheck"] = f"FAIL: {exc}"
        exclusive_write(EVIDENCE / "manifest.json", (json.dumps(manifest, indent=2) + "\n").encode())
        print(f"POST-CHECK FAIL (child exit {exit_code}): {exc}", file=sys.stderr)
        return 4
    apply_rc = apply_proof(manifest)
    exclusive_write(EVIDENCE / "manifest.json", (json.dumps(manifest, indent=2) + "\n").encode())
    if apply_rc != 0:
        print(f"APPLY {manifest.get('apply')}", file=sys.stderr)
        return 5
    if exit_code != 0:
        print(f"CHILD EXIT {exit_code}; see run.log", file=sys.stderr)
        return 6
    print("LF-2I R3 correction evidence run PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
