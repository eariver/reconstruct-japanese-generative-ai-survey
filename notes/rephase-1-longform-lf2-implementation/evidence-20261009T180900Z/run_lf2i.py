#!/usr/bin/env python3
"""LF-2I strict asserting evidence runner (new tool, not an old-script rerun).

Phases:
  A. pre-compare  — candidate identity (HEAD/tree/parent/status) + every
     intended overlay source hash; refuse on any unexpected delta.
  B. unittest run — focused integration + selected affected controls, direct
     child exit capture, timeout preserves partial output, exclusive log.
  C. post-compare — same identity/allowed-delta checks; drift fails even when
     the child passes. All changed-source hashes recorded.
  D. content-apply — exact HEAD bytes per overlay path via `git show` (the
     available database is partial, so no `git archive`) + M-diff
     apply --check/apply + A-file byte copy; proves the overlay applies onto
     clean 409 content.

Usage: python3 run_lf2i.py [--timeout SEC] [--tests "a b c"]
Writes run.log / manifest.json / apply.log exclusively; never overwrites.

Supersedes evidence-20261009T175100Z (one test assertion + approval path
fixed; that 5/6 run is preserved there) and evidence-20261009T173500Z
(pre-check refusal on runner status format; preserved there).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
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
LF1_HASHES = {
    "schemas/longform-reader-input-v2.schema.json":
        "7bae9d2ac753c83521165c76c9e461ce40ac4e704d9b44d3518ae7b88fbd0643",
    "tests/test_survey_longform_derivation_v2.py":
        "ce687447539a99eb92532bc34246a271fb489b259e63b31ed6699fcc12fbf913",
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
DEFAULT_TESTS = (
    "tests.test_survey_longform_publication_integration_v2",
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(args: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(DESIGN), *args], capture_output=True, text=True, **kwargs)


def identity() -> dict:
    head = git(["rev-parse", "HEAD"]).stdout.strip()
    tree = git(["rev-parse", "HEAD^{tree}"]).stdout.strip()
    parent = git(["rev-parse", "HEAD~1"]).stdout.strip()
    status = git(["status", "--porcelain=v1", "--untracked-files=all"]).stdout
    overlay = {}
    for rel in (*M_FILES, *A_FILES):
        overlay[rel] = sha256_file(DESIGN / rel)
    return {"head": head, "tree": tree, "parent": parent, "status": status, "overlay": overlay}


def check_identity(tag: str, manifest: dict) -> None:
    ident = identity()
    manifest[f"identity_{tag}"] = ident
    assert ident["head"] == BASE_HEAD, f"{tag}: HEAD drift {ident['head']}"
    assert ident["tree"] == BASE_TREE, f"{tag}: tree drift {ident['tree']}"
    assert ident["parent"] == BASE_PARENT, f"{tag}: parent drift {ident['parent']}"
    for rel, pinned in LF1_HASHES.items():
        assert ident["overlay"][rel] == pinned, f"{tag}: LF-1 overlay drift {rel}"
    status_rows = [row for row in ident["status"].splitlines() if row.strip()]
    # Bytecode caches are excluded exactly like the production tool guards
    # (they regenerate on every interpreter run and carry no source authority).
    status_rows = [row for row in status_rows
                   if "__pycache__" not in Path(row[3:]).parts and not row[3:].endswith(".pyc")]
    allowed = {f"?? {rel}" for rel in A_FILES} | {f" M {rel}" for rel in M_FILES}
    unexpected = [row for row in status_rows if row not in allowed]
    assert not unexpected, f"{tag}: unexpected working-tree delta: {unexpected}"
    assert len(status_rows) == len(allowed), f"{tag}: overlay set changed: {status_rows}"


def exclusive_write(path: Path, data: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(fd, "wb") as handle:
        handle.write(data)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=int, default=1500)
    parser.add_argument("--tests", default=" ".join(DEFAULT_TESTS))
    args = parser.parse_args()
    for name in ("run.log", "manifest.json", "apply.log"):
        if (EVIDENCE / name).exists():
            print(f"refusing to overwrite prior evidence: {name}", file=sys.stderr)
            return 2
    started = datetime.now(timezone.utc).isoformat()
    manifest: dict = {
        "runner": str(Path(__file__).name),
        "started_at": started,
        "runtime": sys.version,
        "argv": sys.argv,
        "cwd": os.getcwd(),
        "design": str(DESIGN),
        "env": {key: os.environ.get(key, "") for key in ("PATH", "LANG", "LC_ALL", "TZ")},
        "git_env_present": sorted(
            name for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE",
                              "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES",
                              "GIT_COMMON_DIR") if os.environ.get(name)),
    }
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
        cwd=str(DESIGN), stdout=log_fd, stderr=subprocess.STDOUT,
        env={key: value for key, value in os.environ.items()},
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
    apply_lines: list[str] = []
    try:
        # No `git archive`: the available database is partial (inherited
        # missing blobs for sparse-absent paths), so the check reconstructs
        # exact HEAD bytes per overlay path via `git show` (which requires the
        # blob to be present) and applies the M-diff onto them.
        with tempfile.TemporaryDirectory(prefix="jgas-lf2i-apply-") as tmp:
            base = Path(tmp) / "base"
            base.mkdir()
            for rel in M_FILES:
                proc = subprocess.run(["git", "-C", str(DESIGN), "show", f"HEAD:{rel}"],
                                      capture_output=True, check=True)
                target = base / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(proc.stdout)
            diff = subprocess.run(["git", "-C", str(DESIGN), "diff", "HEAD", "--", *M_FILES],
                                  capture_output=True, check=True).stdout
            (Path(tmp) / "overlay.patch").write_bytes(diff)
            chk = subprocess.run(["git", "apply", "--check", "-"], input=diff, cwd=str(base),
                                 capture_output=True)
            apply_lines.append(f"apply-check exit: {chk.returncode}")
            apply_lines.append(chk.stderr.decode()[:2000])
            assert chk.returncode == 0, "M-diff does not apply onto clean HEAD bytes"
            subprocess.run(["git", "apply", "-"], input=diff, cwd=str(base), check=True,
                           capture_output=True)
            for rel in A_FILES:
                data = (DESIGN / rel).read_bytes()
                target = base / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            mismatches = [rel for rel in (*M_FILES, *A_FILES)
                          if sha256_file(base / rel) != sha256_file(DESIGN / rel)]
            apply_lines.append(f"byte-compare mismatches: {mismatches}")
            assert not mismatches, f"apply content mismatch: {mismatches}"
            manifest["apply"] = "PASS"
    except (AssertionError, subprocess.CalledProcessError) as exc:
        manifest["apply"] = f"FAIL: {exc}"
    exclusive_write(EVIDENCE / "apply.log", ("\n".join(apply_lines) + "\n").encode())
    exclusive_write(EVIDENCE / "manifest.json", (json.dumps(manifest, indent=2) + "\n").encode())
    if manifest.get("apply") != "PASS":
        print(f"APPLY {manifest.get('apply')}", file=sys.stderr)
        return 5
    if manifest["child"]["exit"] != 0:
        print(f"CHILD EXIT {manifest['child']['exit']}; see run.log", file=sys.stderr)
        return 6
    print("LF-2I evidence run PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
