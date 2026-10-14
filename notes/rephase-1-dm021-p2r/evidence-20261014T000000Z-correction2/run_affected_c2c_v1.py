#!/usr/bin/env python3
"""Affected-only scoped run v1 — 2 fixed methods on correction2c pins.

Runs ONLY test_fault_primary_read_close_secondary_preserved and
test_verifier_late_retained_additions_refuse (the two v8 failures, both
test-mechanics fixes; module unchanged). Same guard protocol as v8.READY
(static correction2c manifest, inherited13 freeze, exact 16+84 status,
exclusive outputs, direct redirect, cache isolation, forced-keys-only
env record), narrow scope, new exclusive outputs. A green here justifies
the final full v9 suite; it is not a suite result.
"""

import json
import os
import signal
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CANDIDATE = Path("/tmp/opencode/jgas-dm021p2r-impl-20261013T123807Z/candidate-partial-b40de60").resolve()
EV = Path(__file__).resolve().parent
EXPECTED = json.load(open(EV / "expected16-correction2c.json"))
STATIC_FREEZE = json.load(open(EV / "inherited13-static-freeze.json"))
CACHE_STATIC = json.load(open(EV / "cache-inventory-static.json"))
FIXED_HEAD = "409b292756dd1277b9dfae87679934c0d2ce251c"
FIXED_TREE = "8ce3699861505f32d1d60bdc185d4d4f635aedb2"
TIMEOUT_S = 2400
CACHE_PREFIX = Path("/tmp/opencode/jgas-p2r-nocache-20261014T000000Z")
METHODS = [
    "tests.test_survey_editorial_retention_v2.EditorialRetentionV2Tests.test_fault_primary_read_close_secondary_preserved",
    "tests.test_survey_editorial_retention_v2.EditorialRetentionV2Tests.test_verifier_late_retained_additions_refuse",
]
EXPECTED_16_SET = {
    "schemas/editorial-correction-proposal-v2.schema.json",
    "schemas/editorial-retention-manifest-v2.schema.json",
    "schemas/longform-publication-source-manifest-v2.schema.json",
    "schemas/longform-reader-input-v2.schema.json",
    "schemas/reader-surface-gate-v2.schema.json",
    "schemas/reader-surface-semantic-review-v2.schema.json",
    "scripts/survey_editorial_correction_proposal_v2.py",
    "scripts/survey_editorial_retention_v2.py",
    "scripts/survey_longform_derivation_v2.py",
    "scripts/survey_longform_generated_v2.py",
    "scripts/survey_longform_semantic_publication_v2.py",
    "scripts/survey_reader_surface_gate_v2.py",
    "tests/test_survey_editorial_correction_proposal_v2.py",
    "tests/test_survey_editorial_retention_v2.py",
    "tests/test_survey_longform_derivation_v2.py",
    "tests/test_survey_longform_publication_integration_v2.py",
}
INHERITED13 = sorted(set(EXPECTED_16_SET) - {
    "scripts/survey_editorial_retention_v2.py",
    "schemas/editorial-retention-manifest-v2.schema.json",
    "tests/test_survey_editorial_retention_v2.py",
})
EXPECTED_STATUS_ROWS = {
    " M schemas/reader-surface-gate-v2.schema.json",
    " M schemas/reader-surface-semantic-review-v2.schema.json",
    " M scripts/survey_reader_surface_gate_v2.py",
    "?? schemas/editorial-correction-proposal-v2.schema.json",
    "?? schemas/editorial-retention-manifest-v2.schema.json",
    "?? schemas/longform-publication-source-manifest-v2.schema.json",
    "?? schemas/longform-reader-input-v2.schema.json",
    "?? scripts/survey_editorial_correction_proposal_v2.py",
    "?? scripts/survey_editorial_retention_v2.py",
    "?? scripts/survey_longform_derivation_v2.py",
    "?? scripts/survey_longform_generated_v2.py",
    "?? scripts/survey_longform_semantic_publication_v2.py",
    "?? tests/test_survey_editorial_correction_proposal_v2.py",
    "?? tests/test_survey_editorial_retention_v2.py",
    "?? tests/test_survey_longform_derivation_v2.py",
    "?? tests/test_survey_longform_publication_integration_v2.py",
}
PREKNOWN_CACHE_ROWS = {f"?? {rel}" for rel in CACHE_STATIC.get("files", {})}
EXPECTED_FULL_STATUS = EXPECTED_STATUS_ROWS | PREKNOWN_CACHE_ROWS
FORCED_ENV_KEYS = ("GIT_NO_LAZY_FETCH", "GIT_OPTIONAL_LOCKS", "GIT_ALLOW_PROTOCOL",
                   "PYTHONDONTWRITEBYTECODE", "PYTHONPYCACHEPREFIX")

STDOUT_P = EV / "run_affected_c2c_v1.stdout.txt"
STDERR_P = EV / "run_affected_c2c_v1.stderr.txt"
EXIT_P = EV / "run_affected_c2c_v1.exit"
PRE_P = EV / "run_affected_c2c_v1.pre.json"
POST_P = EV / "run_affected_c2c_v1.post.json"
META_P = EV / "run_affected_c2c_v1.meta.json"
TERMINAL_P = EV / "run_affected_c2c_v1.terminal.json"


def _git(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file"})
    return subprocess.run(["git", "-c", f"safe.directory={str(cwd)}", *args],
                          cwd=cwd, capture_output=True, text=True, env=env, timeout=60)


def _observe(label: str) -> dict:
    procs = {
        "rev-parse HEAD": _git(["rev-parse", "HEAD"], CANDIDATE),
        "rev-parse tree": _git(["rev-parse", "HEAD^{tree}"], CANDIDATE),
        "status": _git(["status", "--porcelain=v1", "--untracked-files=all"], CANDIDATE),
        "index": _git(["diff", "--cached", "--name-only"], CANDIDATE),
    }
    for name, proc in procs.items():
        if proc.returncode != 0:
            raise RuntimeError(f"observe {label}: git {name} rc={proc.returncode}")
    import hashlib
    files = {}
    for rel in sorted(EXPECTED):
        f = CANDIDATE / rel
        try:
            data = f.read_bytes()
        except OSError as e:
            files[rel] = {"error": str(e)}
            continue
        files[rel] = {"sha256": hashlib.sha256(data).hexdigest(),
                      "bytes": len(data), "mode": oct(f.stat().st_mode & 0o777)}
    return {"label": label, "head": procs["rev-parse HEAD"].stdout.strip(),
            "tree": procs["rev-parse tree"].stdout.strip(), "status": procs["status"].stdout,
            "index": procs["index"].stdout, "files": files}


def _check(obs: dict, where: str) -> list[str]:
    errors = []
    if obs["head"] != FIXED_HEAD:
        errors.append(f"{where} HEAD mismatch")
    if obs["tree"] != FIXED_TREE:
        errors.append(f"{where} tree mismatch")
    if obs["index"].strip() != "":
        errors.append(f"{where} index non-empty")
    for rel, exp in EXPECTED.items():
        got = obs["files"].get(rel, {})
        if got.get("sha256") != exp["sha256"] or got.get("mode") != exp["mode"] \
                or got.get("bytes") != exp["bytes"]:
            errors.append(f"{where} expected16c mismatch: {rel}")
    rows = obs["status"].splitlines()
    if len(rows) != len(EXPECTED_FULL_STATUS) or set(rows) != EXPECTED_FULL_STATUS \
            or len(set(rows)) != len(rows):
        errors.append(f"{where} full status != expected16+preknown-cache")
    frozen = STATIC_FREEZE.get("files", {})
    for rel in INHERITED13:
        exp = frozen.get(rel, {})
        got = obs["files"].get(rel, {})
        if got.get("sha256") != exp.get("sha256") or got.get("mode") != exp.get("mode") \
                or got.get("bytes") != exp.get("bytes"):
            errors.append(f"{where} inherited13 drift: {rel}")
    return errors


def main() -> int:
    if set(EXPECTED) != EXPECTED_16_SET:
        print("RUNNER_REFUSAL: manifest path set wrong", file=sys.stderr)
        return 40
    if CACHE_PREFIX.exists():
        print(f"RUNNER_REFUSAL: prefix exists: {CACHE_PREFIX}", file=sys.stderr)
        return 40
    for p in (STDOUT_P, STDERR_P, EXIT_P, PRE_P, POST_P, META_P, TERMINAL_P):
        if p.exists():
            print(f"RUNNER_REFUSAL: output exists: {p.name}", file=sys.stderr)
            return 40
    terminal: dict = {"runner": "run_affected_c2c_v1.py", "pid": os.getpid(),
                      "methods": METHODS}
    out_fh = err_fh = None
    proc = None
    child_rc = None
    wrapper_rc = 40
    try:
        out_fh = open(STDOUT_P, "xb")
        err_fh = open(STDERR_P, "xb")
        terminal.update({"started_utc": datetime.now(timezone.utc).isoformat(),
                         "candidate": str(CANDIDATE), "argv": sys.argv, "cwd": os.getcwd(),
                         "python": sys.version})
        meta = dict(terminal)
        meta["env_git"] = {k: v for k, v in os.environ.items() if k.startswith("GIT")}
        with open(META_P, "x") as f:
            json.dump(meta, f, indent=1)
        pre = _observe("pre")
        with open(PRE_P, "x") as f:
            json.dump(pre, f, indent=1)
        pre_errors = _check(pre, "pre")
        if pre_errors:
            terminal["pre_errors"] = pre_errors
            msg = "PRE-GUARD FAILED:\n" + "\n".join(pre_errors) + "\n"
            out_fh.write(msg.encode())
            err_fh.write(msg.encode())
            print(msg, file=sys.stderr)
        else:
            cmd = [sys.executable, "-u", "-m", "unittest", "-v", *METHODS]
            env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
            env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0",
                        "GIT_ALLOW_PROTOCOL": "file", "PYTHONDONTWRITEBYTECODE": "1",
                        "PYTHONPYCACHEPREFIX": str(CACHE_PREFIX)})
            forced = {k: env.get(k) for k in FORCED_ENV_KEYS}
            t0 = datetime.now(timezone.utc)
            proc = subprocess.Popen(cmd, cwd=CANDIDATE, stdout=out_fh, stderr=err_fh,
                                    env=env, start_new_session=True)
            print(f"affected child pid={proc.pid} cmd={cmd} cwd={CANDIDATE} "
                  f"forced={forced} other=redacted", flush=True)
            try:
                child_rc = proc.wait(timeout=TIMEOUT_S)
            except subprocess.TimeoutExpired:
                terminal["timed_out"] = True
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except OSError as exc:
                    terminal["killpg"] = f"{type(exc).__name__}: {exc}"
                try:
                    proc.wait(timeout=120)
                except subprocess.SubprocessError:
                    pass
                child_rc = proc.returncode if proc.returncode is not None else 124
            terminal["child_rc"] = child_rc
    except KeyboardInterrupt as exc:
        terminal["interrupted"] = f"{type(exc).__name__}: {exc}"
        if proc is not None:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except OSError:
                pass
            child_rc = proc.returncode if proc.returncode is not None else 130
            terminal["child_rc"] = child_rc
    except Exception as exc:
        terminal["fatal"] = f"{type(exc).__name__}: {exc}"
        terminal["launch_rc"] = 1
        if proc is not None and child_rc is None:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except OSError:
                pass
    finally:
        try:
            post = _observe("finally-post")
            post_ok = True
        except Exception as exc:
            post = {"label": "finally-post", "observe_error": f"{type(exc).__name__}: {exc}"}
            post_ok = False
        try:
            with open(POST_P, "x") as f:
                json.dump(post, f, indent=1)
        except OSError as exc:
            terminal["post_write_error"] = f"{type(exc).__name__}: {exc}"
            post_ok = False
        post_errors = []
        if not post_ok:
            post_errors.append("post observation failed")
        else:
            post_errors = _check(post, "post")
        flush_errors = []
        if terminal.get("interrupted"):
            wrapper_rc = 130
        elif terminal.get("timed_out"):
            wrapper_rc = 124
        elif terminal.get("launch_rc") is not None:
            wrapper_rc = terminal["launch_rc"]
        elif terminal.get("pre_errors"):
            wrapper_rc = 2
        elif child_rc is not None and child_rc != 0:
            wrapper_rc = child_rc
        else:
            wrapper_rc = 0
        terminal["wrapper_rc"] = wrapper_rc
        terminal["post_errors"] = post_errors
        if post_errors and wrapper_rc == 0:
            wrapper_rc = 3
            terminal["wrapper_rc"] = wrapper_rc
        terminal["ended_utc"] = datetime.now(timezone.utc).isoformat()
        try:
            if out_fh is not None and not out_fh.closed:
                out_fh.write(f"\n[WRAPPER child_rc={child_rc} wrapper_rc={wrapper_rc}]\n".encode())
                if post_errors:
                    out_fh.write(("POST-GUARD: " + "; ".join(post_errors) + "\n").encode())
                out_fh.flush()
        except (OSError, ValueError) as exc:
            terminal["trailer_write_error"] = f"{type(exc).__name__}: {exc}"
            if wrapper_rc == 0:
                wrapper_rc = 5
        for fh, name in ((out_fh, "stdout"), (err_fh, "stderr")):
            if fh is not None and not fh.closed:
                try:
                    fh.flush()
                except (OSError, ValueError) as exc:
                    flush_errors.append(f"{name}: {exc}")
                try:
                    fh.close()
                except (OSError, ValueError) as exc:
                    flush_errors.append(f"{name}: {exc}")
        if flush_errors:
            terminal["flush_errors"] = flush_errors
            if wrapper_rc == 0:
                wrapper_rc = 5
        try:
            with open(EXIT_P, "x") as f:
                f.write(f"{wrapper_rc}\n")
        except OSError as exc:
            print(f"RUNNER_REFUSAL: cannot record exit: {exc}", file=sys.stderr)
        try:
            with open(TERMINAL_P, "x") as f:
                json.dump(terminal, f, indent=1)
        except OSError as exc:
            print(f"RUNNER_REFUSAL: cannot record terminal: {exc}", file=sys.stderr)
        print(f"child_rc={child_rc} wrapper_rc={wrapper_rc} post_errors={post_errors} "
              f"terminal={json.dumps(terminal)[:1500]}")
    return wrapper_rc


if __name__ == "__main__":
    sys.exit(main())
