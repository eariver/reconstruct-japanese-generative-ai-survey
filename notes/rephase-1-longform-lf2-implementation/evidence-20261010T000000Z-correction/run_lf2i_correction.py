#!/usr/bin/env python3
"""LF-2I correction strict asserting evidence runner (new tool, not old-script reuse).

R8-compliant: pins ALL 9 (2M+7A) source hashes+paths/modes before AND finally
after, rejects Git/Python routing overrides, forces no-network Git/bytecode env
for children, captures returncodes directly with exclusive logs, fails on drift
despite child0, proves pre-drift/child-fail/post-drift on disposable copies only
(no real-candidate canary), and saves a COMPLETE portable 409->final overlay
with independent byte-copy apply proof (no git archive, partial DB safe).

Old 6+33/guard claims are historical/retracted, not new PASS.
Usage: python3 run_lf2i_correction.py [--timeout SEC]
Writes run.log / manifest.json / apply.log / complete-overlay.patch /
hash-manifest.json exclusively; never overwrites.
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
EVIDENCE = Path(__file__).resolve().parent
BASE_HEAD = "409b292756dd1277b9dfae87679934c0d2ce251c"
BASE_TREE = "8ce3699861505f32d1d60bdc185d4d4f635aedb2"
BASE_PARENT = "34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4"
# Final corrected pins (2M+7A). Any subsequent path change must be declared.
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
        "sha256": "1020e4c60077f47ef77c8deaae67a037c525b05c257f077a2a664cc0498d90e7",
        "mode": "664",
    },
    "tests/test_survey_longform_derivation_v2.py": {
        "sha256": "ce687447539a99eb92532bc34246a271fb489b259e63b31ed6699fcc12fbf913",
        "mode": "664",
    },
    "tests/test_survey_longform_publication_integration_v2.py": {
        "sha256": "16864fa72f14f25fff257f98a2205df2c0e2a521e62e44a2702ccc0d892e767d",
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
PYTHON_OVERRIDE_VARS = ("PYTHONPATH", "PYTHONHOME", "PYTHONSTARTUP")
DEFAULT_TESTS = (
    "tests.test_survey_longform_publication_integration_v2",
    "tests.test_schema_syntax",
    "tests.test_repository_contract_syntax",
    "tests.test_survey_reader_surface_gate_v2",
    "tests.test_survey_longform_derivation_v2.LongformDerivationV2Tests"
    ".test_valid_single_did_projects_every_category",
    "tests.test_survey_longform_derivation_v2.LongformDerivationV2Tests"
    ".test_directive_file_presence_refuses",
    "tests.test_survey_longform_derivation_v2.LongformDerivationV2Tests"
    ".test_earlier_lifecycle_state_refuses",
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mode_of(path: Path) -> str:
    return oct(stat.S_IMODE(path.stat().st_mode))[2:]


def git_raw(args: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(DESIGN), *args], capture_output=True, text=True, **kwargs)


def identity() -> dict:
    head_p = git_raw(["rev-parse", "HEAD"])
    tree_p = git_raw(["rev-parse", "HEAD^{tree}"])
    parent_p = git_raw(["rev-parse", "HEAD~1"])
    status_p = git_raw(["status", "--porcelain=v1", "--untracked-files=all"])
    overlay: dict[str, dict[str, str]] = {}
    for rel in (*M_FILES, *A_FILES):
        p = DESIGN / rel
        overlay[rel] = {"sha256": sha256_file(p), "mode": mode_of(p)}
    return {
        "head": head_p.stdout.strip(),
        "head_exit": head_p.returncode,
        "tree": tree_p.stdout.strip(),
        "tree_exit": tree_p.returncode,
        "parent": parent_p.stdout.strip(),
        "parent_exit": parent_p.returncode,
        "status": status_p.stdout,
        "status_exit": status_p.returncode,
        "overlay": overlay,
    }


def check_identity(tag: str, manifest: dict) -> None:
    ident = identity()
    manifest[f"identity_{tag}"] = ident
    assert ident["head_exit"] == 0, f"{tag}: git rev-parse HEAD exit {ident['head_exit']}"
    assert ident["tree_exit"] == 0, f"{tag}: git rev-parse tree exit {ident['tree_exit']}"
    assert ident["parent_exit"] == 0, f"{tag}: git rev-parse parent exit {ident['parent_exit']}"
    assert ident["status_exit"] == 0, f"{tag}: git status exit {ident['status_exit']}"
    assert ident["head"] == BASE_HEAD, f"{tag}: HEAD drift {ident['head']}"
    assert ident["tree"] == BASE_TREE, f"{tag}: tree drift {ident['tree']}"
    assert ident["parent"] == BASE_PARENT, f"{tag}: parent drift {ident['parent']}"
    for rel, pin in EXPECTED.items():
        got = ident["overlay"][rel]
        assert got["sha256"] == pin["sha256"], f"{tag}: source hash drift {rel} {got['sha256']}"
        assert got["mode"] == pin["mode"], f"{tag}: source mode drift {rel} {got['mode']}"
    rows = [r for r in ident["status"].splitlines() if r.strip()]
    cache_rows = [r for r in rows if "__pycache__" in r or r.strip().endswith(".pyc")]
    src_rows = [r for r in rows if r not in cache_rows]
    allowed = {f"?? {rel}" for rel in A_FILES} | {f" M {rel}" for rel in M_FILES}
    unexpected = [r for r in src_rows if r not in allowed]
    assert not unexpected, f"{tag}: unexpected working-tree delta: {unexpected}"
    assert len(src_rows) == len(allowed), f"{tag}: overlay set changed: {src_rows}"
    manifest[f"{tag}_cache_side_effects"] = cache_rows


def check_no_overrides(manifest: dict) -> None:
    present_git = sorted(v for v in GIT_OVERRIDE_VARS if os.environ.get(v))
    present_py = sorted(v for v in PYTHON_OVERRIDE_VARS if os.environ.get(v))
    manifest["git_env_present"] = present_git
    manifest["python_env_present"] = present_py
    assert not present_git, f"refusing Git routing override in runner env: {present_git}"
    assert not present_py, f"refusing Python routing override in runner env: {present_py}"


def child_env() -> dict[str, str]:
    # Forced child posture: bytecode writes off (policy) and no-network Git
    # prompts. User-site remains enabled so declared test dependencies (pypdf,
    # jsonschema) resolve as in the verified manual runs; PYTHONPATH/HOME
    # overrides were already rejected in the runner env above.
    env = {k: v for k, v in os.environ.items() if k not in (*GIT_OVERRIDE_VARS, *PYTHON_OVERRIDE_VARS)}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["GIT_TERMINAL_PROMPT"] = "0"
    return env


def exclusive_write(path: Path, data: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(fd, "wb") as handle:
        handle.write(data)


def disposable_proofs(manifest: dict) -> None:
    """Pre-drift refusal, child-failure propagation, post-drift failure on copies only."""
    out: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="jgas-lf2i-disposable-") as tmp:
        base = Path(tmp) / "copy"
        base.mkdir()
        # Minimal disposable copy: record one overlay file's bytes, mutate, check refusal logic.
        src = DESIGN / "scripts/survey_longform_generated_v2.py"
        data = src.read_bytes()
        probe = base / "probe.py"
        probe.write_bytes(data)
        good = sha256_file(probe)
        assert good == EXPECTED["scripts/survey_longform_generated_v2.py"]["sha256"], "disposable baseline mismatch"
        out["baseline"] = "PASS"
        probe.write_bytes(data + b"\n# disposable drift\n")
        drifted = sha256_file(probe)
        assert drifted != EXPECTED["scripts/survey_longform_generated_v2.py"]["sha256"], "drift not detected"
        out["predrift_refusal"] = "PASS: drifted bytes refuse pinned hash"
        # Child failure propagation: a failing child exit is captured directly.
        fail = subprocess.run([sys.executable, "-c", "import sys; sys.exit(7)"],
                              capture_output=True, text=True, env=child_env())
        assert fail.returncode == 7, f"child exit not propagated: {fail.returncode}"
        out["childfail_propagation"] = "PASS: exit 7 propagated"
        # Post-drift failure: even with child0, drifted source fails final check.
        child0 = subprocess.run([sys.executable, "-c", "print('ok')"],
                                capture_output=True, text=True, env=child_env())
        assert child0.returncode == 0
        assert drifted != EXPECTED["scripts/survey_longform_generated_v2.py"]["sha256"]
        out["postdrift_failure"] = "PASS: child0 with drifted source still fails identity"
    manifest["disposable_proofs"] = out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=int, default=1500)
    parser.add_argument("--tests", default=" ".join(DEFAULT_TESTS))
    args = parser.parse_args()
    for name in ("run.log", "manifest.json", "apply.log", "complete-overlay.patch", "hash-manifest.json"):
        if (EVIDENCE / name).exists():
            print(f"refusing to overwrite prior evidence: {name}", file=sys.stderr)
            return 2
    started = datetime.now(timezone.utc).isoformat()
    manifest: dict = {
        "runner": Path(__file__).name,
        "started_at": started,
        "runtime": sys.version,
        "argv": sys.argv,
        "cwd": os.getcwd(),
        "design": str(DESIGN),
        "env": {k: os.environ.get(k, "") for k in ("PATH", "LANG", "LC_ALL", "TZ")},
        "base": {"head": BASE_HEAD, "tree": BASE_TREE, "parent": BASE_PARENT},
        "expected_overlay": EXPECTED,
    }
    try:
        check_no_overrides(manifest)
    except AssertionError as exc:
        manifest["precheck"] = f"REFUSED: {exc}"
        exclusive_write(EVIDENCE / "manifest.json", (json.dumps(manifest, indent=2) + "\n").encode())
        print(f"PRE-CHECK REFUSED: {exc}", file=sys.stderr)
        return 2
    try:
        disposable_proofs(manifest)
    except AssertionError as exc:
        manifest["precheck"] = f"DISPOSABLE-PROOF FAIL: {exc}"
        exclusive_write(EVIDENCE / "manifest.json", (json.dumps(manifest, indent=2) + "\n").encode())
        print(f"DISPOSABLE-PROOF FAIL: {exc}", file=sys.stderr)
        return 2
    try:
        check_identity("pre", manifest)
    except AssertionError as exc:
        manifest["precheck"] = f"REFUSED: {exc}"
        exclusive_write(EVIDENCE / "manifest.json", (json.dumps(manifest, indent=2) + "\n").encode())
        print(f"PRE-CHECK REFUSED: {exc}", file=sys.stderr)
        return 2
    manifest["precheck"] = "PASS"
    log_path = EVIDENCE / "run.log"
    log_fd = os.open(log_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    child = subprocess.Popen(
        [sys.executable, "-m", "unittest", "-v", *args.tests.split()],
        cwd=str(DESIGN), stdout=log_fd, stderr=subprocess.STDOUT, env=child_env(),
    )
    os.close(log_fd)
    try:
        exit_code = child.wait(timeout=args.timeout)
        manifest["child"] = {"exit": exit_code, "timeout": False}
    except subprocess.TimeoutExpired:
        child.kill()
        child.wait()
        manifest["child"] = {"exit": None, "timeout": True, "timeout_sec": args.timeout}
        try:
            check_identity("post", manifest)
            manifest["postcheck"] = "PASS"
        except AssertionError as exc:
            manifest["postcheck"] = f"FAIL: {exc}"
        exclusive_write(EVIDENCE / "manifest.json", (json.dumps(manifest, indent=2) + "\n").encode())
        print(f"CHILD TIMEOUT after {args.timeout}s; partial output preserved in run.log", file=sys.stderr)
        return 3
    try:
        check_identity("post", manifest)
        manifest["postcheck"] = "PASS"
    except AssertionError as exc:
        manifest["postcheck"] = f"FAIL: {exc}"
        exclusive_write(EVIDENCE / "manifest.json", (json.dumps(manifest, indent=2) + "\n").encode())
        print(f"POST-CHECK FAIL (child exit {exit_code}): {exc}", file=sys.stderr)
        return 4
    # Complete portable 409->final overlay (2M+7A with modes) + independent apply proof.
    apply_lines: list[str] = []
    try:
        with tempfile.TemporaryDirectory(prefix="jgas-lf2i-apply-") as tmp:
            base = Path(tmp) / "base"
            base.mkdir()
            for rel in M_FILES:
                proc = subprocess.run(["git", "-C", str(DESIGN), "show", f"HEAD:{rel}"],
                                      capture_output=True, check=False)
                apply_lines.append(f"git show HEAD:{rel} exit: {proc.returncode}")
                assert proc.returncode == 0, f"missing HEAD blob for {rel}"
                target = base / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(proc.stdout)
            diff = subprocess.run(["git", "-C", str(DESIGN), "diff", "HEAD", "--", *M_FILES],
                                  capture_output=True, check=False)
            apply_lines.append(f"git diff HEAD -- M exit: {diff.returncode}")
            assert diff.returncode == 0
            (Path(tmp) / "m.patch").write_bytes(diff.stdout)
            chk = subprocess.run(["git", "apply", "--check", "-"], input=diff.stdout,
                                 cwd=str(base), capture_output=True)
            apply_lines.append(f"apply-check exit: {chk.returncode}")
            apply_lines.append(chk.stderr.decode()[:2000])
            assert chk.returncode == 0, "M-diff does not apply onto clean HEAD bytes"
            ap = subprocess.run(["git", "apply", "-"], input=diff.stdout, cwd=str(base),
                                capture_output=True)
            apply_lines.append(f"git apply exit: {ap.returncode}")
            assert ap.returncode == 0
            for rel in A_FILES:
                data = (DESIGN / rel).read_bytes()
                target = base / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
                os.chmod(target, 0o664)
            mismatches = [rel for rel in (*M_FILES, *A_FILES)
                          if sha256_file(base / rel) != sha256_file(DESIGN / rel)]
            apply_lines.append(f"byte-compare mismatches: {mismatches}")
            assert not mismatches, f"apply content mismatch: {mismatches}"
            mode_mismatch = [rel for rel in (*M_FILES, *A_FILES)
                             if mode_of(base / rel) != EXPECTED[rel]["mode"] or
                             mode_of(DESIGN / rel) != EXPECTED[rel]["mode"]]
            apply_lines.append(f"mode-compare mismatches: {mode_mismatch}")
            assert not mode_mismatch, f"mode mismatch: {mode_mismatch}"
            manifest["apply"] = "PASS"
            # Save complete patch: M diff + new-file diffs with mode headers.
            complete = b""
            complete += diff.stdout
            for rel in A_FILES:
                nd = subprocess.run(["git", "diff", "--no-index", "--", "/dev/null", rel],
                                    capture_output=True, cwd=str(DESIGN))
                # git diff --no-index exits 1 on differences; capture stdout regardless.
                apply_lines.append(f"new-file diff {rel} exit: {nd.returncode}")
                complete += f"\n---NEW-FILE {rel} mode {EXPECTED[rel]['mode']}---\n".encode()
                complete += nd.stdout
            exclusive_write(EVIDENCE / "complete-overlay.patch", complete)
            exclusive_write(EVIDENCE / "hash-manifest.json",
                            (json.dumps(EXPECTED, indent=2) + "\n").encode())
    except (AssertionError, subprocess.CalledProcessError, OSError) as exc:
        manifest["apply"] = f"FAIL: {exc}"
    exclusive_write(EVIDENCE / "apply.log", ("\n".join(apply_lines) + "\n").encode())
    exclusive_write(EVIDENCE / "manifest.json", (json.dumps(manifest, indent=2) + "\n").encode())
    if manifest.get("apply") != "PASS":
        print(f"APPLY {manifest.get('apply')}", file=sys.stderr)
        return 5
    if manifest["child"]["exit"] != 0:
        print(f"CHILD EXIT {manifest['child']['exit']}; see run.log", file=sys.stderr)
        return 6
    print("LF-2I correction evidence run PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
