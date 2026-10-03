"""Git-aware closure diagnostic on the actual recovered DB.

Phase A (positive): current_closure(root) + _verify_head_bytes(root,
EXACT_NEW_HEAD, closure) must return cleanly (None) — proves current-source
binding of the newly recovered candidate. No file mutations.

Phase B (negative): in-memory deepcopy of the rows with ONE recorded sha256
corrupted must raise ValueError with the EXACT message
"Weekly receipt current-tool closure drift: <name>". Any other outcome
(no exception, different message/type) is a FAILURE reported outside any
exception handler. No file mutations, no history construction, no receipt or
publication replay, no old-ancestry claims.

Usage: venv-python run_closure.py <rawdir> [--positive-only]
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

FIXTURE = Path("/tmp/opencode/jgas-rephase-candidate-recovery-20261003T0435Z")
EXACT_NEW_HEAD = "b40de600e9ed1f80cb278213ccf17aa5f3cd9de3"
EXP_TREE = "657032438c6ed8b1c055d5a120b67b4b261a5092"
EXP_PARENT = "774dd39a951c9ac3818e83dfffd4c7666efb0a20"
NEG_PREFIX = "Weekly receipt current-tool closure drift:"

SCRUB = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
         "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR", "GIT_NAMESPACE",
         "GIT_CEILING_DIRECTORIES", "GIT_DISCOVERY_ACROSS_FILESYSTEM")


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(FIXTURE), *args],
                          capture_output=True, text=True, check=False)


def identity() -> dict[str, str]:
    head = git("rev-parse", "HEAD")
    tree = git("rev-parse", "HEAD^{tree}")
    parent = git("log", "--format=%P", "-1")
    status = git("status", "--porcelain")
    diff = git("diff", "--quiet", "HEAD")
    return {"head": head.stdout.strip(), "tree": tree.stdout.strip(),
            "parent": parent.stdout.strip(), "status": status.stdout,
            "tracked_diff_exit": str(diff.returncode)}


def main() -> int:
    raw = Path(sys.argv[1])
    positive_only = "--positive-only" in sys.argv[1:]
    raw.mkdir(parents=True, exist_ok=True)
    for key in SCRUB:
        os.environ.pop(key, None)
    os.environ["GIT_NO_LAZY_FETCH"] = "1"
    os.environ["GIT_ALLOW_PROTOCOL"] = "file"
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    os.environ.pop("PYTHONPATH", None)
    (raw / "closure-argv.txt").write_text(
        f"argv={sys.argv}\ncwd={os.getcwd()}\nfixture={FIXTURE}\n"
        f"commit={EXACT_NEW_HEAD}\n"
        "env=GIT_NO_LAZY_FETCH=1 GIT_ALLOW_PROTOCOL=file PYTHONDONTWRITEBYTECODE=1\n",
        encoding="utf-8")
    before = identity()
    (raw / "closure-identity-before.txt").write_text(repr(before) + "\n", encoding="utf-8")
    assert before["head"] == EXACT_NEW_HEAD, f"HEAD moved: {before['head']}"
    assert before["tree"] == EXP_TREE, f"tree moved: {before['tree']}"
    assert before["parent"] == EXP_PARENT, f"parent moved: {before['parent']}"
    assert before["tracked_diff_exit"] == "0", "tracked bytes changed before probe"

    sys.path.insert(0, str(FIXTURE))
    import scripts.survey_weekly_derivation_v2 as deriv  # noqa: E402

    src = Path(deriv.__file__)
    blob = git("hash-object", str(src))
    (raw / "closure-source.txt").write_text(
        f"module={deriv.__name__}\nfile={src}\n"
        f"sha256={hashlib.sha256(src.read_bytes()).hexdigest()}\n"
        f"git_blob={blob.stdout.strip()}\n",
        encoding="utf-8")

    closure = deriv.current_closure(FIXTURE)
    (raw / "closure-rows.txt").write_text(
        json.dumps(closure, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # Phase A: positive binding on the actual recovered DB.
    deriv._verify_head_bytes(FIXTURE, EXACT_NEW_HEAD, closure)
    (raw / "closure-positive.txt").write_text(
        f"positive=PASS rows={len(closure)} commit={EXACT_NEW_HEAD}\n", encoding="utf-8")
    print(f"positive=PASS rows={len(closure)}")

    # Phase B: exact-drift negative on an in-memory corrupted copy.
    if not positive_only:
        bad = copy.deepcopy(closure)
        victim = bad[0]
        orig = victim["sha256"]
        victim["sha256"] = ("0" if orig[-1] != "0" else "1") + orig[1:]
        expected = f"{NEG_PREFIX} {victim['name']}"
        try:
            deriv._verify_head_bytes(FIXTURE, EXACT_NEW_HEAD, bad)
        except ValueError as exc:
            got = str(exc)
            (raw / "closure-negative.txt").write_text(
                f"negative_exception=ValueError\nmessage={got}\n"
                f"expected={expected}\ncorrupted_row={victim['name']}\n",
                encoding="utf-8")
            print(f"negative message={got}")
            if got != expected:
                print(f"negative=FAIL want exactly {expected!r}")
                return 2
        except Exception as exc:  # noqa: BLE001 - unexpected type is a failure
            (raw / "closure-negative.txt").write_text(
                f"negative_exception=UNEXPECTED {type(exc).__name__}: {exc}\n"
                f"expected=ValueError({expected})\n",
                encoding="utf-8")
            print(f"negative=FAIL unexpected {type(exc).__name__}: {exc}")
            return 2
        else:
            (raw / "closure-negative.txt").write_text(
                "negative_exception=NONE (FAIL: drift not detected)\n", encoding="utf-8")
            print("negative=FAIL no exception raised")
            return 2
        print("negative=PASS exact drift message")
    after = identity()
    (raw / "closure-identity-after.txt").write_text(repr(after) + "\n", encoding="utf-8")
    assert after["head"] == EXACT_NEW_HEAD and after["tree"] == EXP_TREE
    assert after["tracked_diff_exit"] == "0", "tracked bytes changed by probe"
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
