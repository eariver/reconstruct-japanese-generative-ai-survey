#!/usr/bin/env python3
"""R4e export workflow predicate probe (offline, no Actions/GitHub).

Usage: export-predicate-r4e.py ACTIVE_ROOT INERT_ROOT ISSUE ACTIVE_ID SCENARIO
  SCENARIO in {manual-active, manual-old, manual-inert,
               pr-positive, pr-unrelated, pr-inert}

Executes the ACTUAL current export workflow Python predicate end-to-end
(extracted verbatim from the fixture's own .github workflow file, fixed
_rel_expected version) with the fixture's own modules (binding-checked:
every scripts.* __file__ under the run root, single-root scripts.__path__).
The predicate's own git diff / State discovery / validation run for real;
stdout (the CI $GITHUB_OUTPUT payload) is captured and asserted.

- manual-active: REQUESTED_CANDIDATE=<active versioned candidate> -> PASS.
- manual-old: REQUESTED_CANDIDATE=<superseded r*-1 versioned candidate> -> refuse.
- manual-inert: REQUESTED_CANDIDATE=<publication-set.json> -> refuse.
- pr-positive: temp repo = inert state + first-active commit, then overlay of
  the real active fixture + second commit ("second-correction activation
  delta"); BASE_SHA=<first commit>. Real git diff shows exactly the changed
  candidate + State -> PASS (also proves receipt commit ancestry + tool
  closure predicates on the artifact-only HEAD).
- pr-unrelated: temp repo + commit touching only an unrelated root file ->
  refuse (exactly-one-candidate rule).
- pr-inert: temp repo + commit touching only publication-set.json ->
  refuse (inert-set guard).
Temp repos live under $R4E_TMPDIR (default /dev/shm); removed on success,
preserved + reported on failure. Fixtures never mutated. No mocks, no git
diff mocking, no real Human/production approval, no candidate minting
(commits only record existing fixture artifacts).

Saved BEFORE execution.
"""
from __future__ import annotations
import contextlib
import io
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import textwrap

if os.environ.get("PYTHONDONTWRITEBYTECODE") != "1":
    print("BLOCKER: PYTHONDONTWRITEBYTECODE!=1 (set BEFORE python startup)", flush=True)
    sys.exit(2)
_pfx = os.environ.get("PYTHONPYCACHEPREFIX", "")
if not _pfx.startswith("/tmp/"):
    print(f"BLOCKER: PYTHONPYCACHEPREFIX must be /tmp/... external, got {_pfx!r}", flush=True)
    sys.exit(2)
for _v in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
           "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR", "GIT_PREFIX"):
    if os.environ.get(_v):
        print(f"BLOCKER unsafe inherited {_v}", flush=True)
        sys.exit(2)

R4E_TMP = os.environ.get("R4E_TMPDIR", "/dev/shm")
SCENARIOS = ("manual-active", "manual-old", "manual-inert",
             "pr-positive", "pr-unrelated", "pr-inert")


def _log(m: str):
    print(m, flush=True)


def _git(root: pathlib.Path, *args: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file"})
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, timeout=120, env=env)


def _extract_predicate(root: pathlib.Path) -> str:
    wf = (root / ".github/workflows/survey-production-v2-export-publication-preview.yml").read_text()
    if "def _rel_expected" not in wf or "def _selection_for_state" not in wf:
        raise SystemExit("BLOCKER workflow missing fixed selection code")
    start = wf.index("          python - <<'PY'")
    code_start = wf.index("\n", start) + 1
    end = wf.index("\n          PY\n", code_start)
    return textwrap.dedent(wf[code_start:end])


def _run_full(root: pathlib.Path, extra_env: dict) -> tuple:
    """Exec the full workflow predicate block with R as cwd+sys.path root.
    Returns (SystemExit|None, stdout_text)."""
    for m in [m for m in list(sys.modules) if m == "scripts" or m.startswith("scripts.")]:
        del sys.modules[m]
    sys.path.insert(0, str(root))
    try:
        import scripts as _pkg
        if list(getattr(_pkg, "__path__", [])) != [str(root / "scripts")]:
            return SystemExit(f"scripts namespace not single-root: {list(getattr(_pkg, '__path__', []))}"), ""
        block = _extract_predicate(root)
        old_env = dict(os.environ)
        old_cwd = os.getcwd()
        os.environ.update(extra_env)
        os.chdir(root)
        buf = io.StringIO()
        refusal = None
        try:
            with contextlib.redirect_stdout(buf):
                exec(block, {"__name__": "__workflow_predicate__"})  # noqa: S102 - actual predicate offline
        except SystemExit as exc:
            refusal = exc
        finally:
            os.chdir(old_cwd)
            os.environ.clear()
            os.environ.update(old_env)
        bad = [(n, getattr(m, "__file__", None)) for n, m in list(sys.modules.items())
               if (n == "scripts" or n.startswith("scripts.")) and getattr(m, "__file__", None) is not None
               and not str(pathlib.Path(getattr(m, "__file__")).resolve()).startswith(str(root))]
        if bad:
            return SystemExit(f"BLOCKER code binding outside run root: {bad}"), buf.getvalue()
        return refusal, buf.getvalue()
        for m in [m for m in list(sys.modules) if m == "scripts" or m.startswith("scripts.")]:
            del sys.modules[m]
        sys.path.remove(str(root))
        return None, buf.getvalue()
    finally:
        for m in [m for m in list(sys.modules) if m == "scripts" or m.startswith("scripts.")]:
            try:
                del sys.modules[m]
            except KeyError:
                pass
        if str(root) in sys.path:
            sys.path.remove(str(root))


def _parse_outputs(text: str) -> dict:
    out = {}
    for line in text.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def _check_binding_and_head(root: pathlib.Path, exp_head: str, exp_count: int) -> None:
    head = _git(root, "rev-parse", "HEAD").stdout.strip()
    if head != exp_head:
        raise SystemExit(f"BLOCKER unexpected HEAD {head}")
    n = len(_git(root, "ls-files").stdout.strip().splitlines())
    if n != exp_count:
        raise SystemExit(f"BLOCKER ls-files {n} != {exp_count}")


def main() -> int:
    if len(sys.argv) != 6:
        print(f"usage: {sys.argv[0]} ACTIVE_ROOT INERT_ROOT ISSUE ACTIVE_ID SCENARIO", flush=True)
        return 2
    active = pathlib.Path(sys.argv[1]).resolve()
    inert = pathlib.Path(sys.argv[2]).resolve()
    issue, active_id, scenario = sys.argv[3], sys.argv[4], sys.argv[5]
    tag = scenario.replace("-", "")
    print(f"ACTIVE={active} INERT={inert} ISSUE={issue} ACTIVE={active_id} SCENARIO={scenario}", flush=True)
    if scenario not in SCENARIOS:
        print(f"BLOCKER unknown scenario {scenario}", flush=True)
        return 2
    if [p for p in sys.path if "/tmp/opencode/jgas-" in p]:
        print("BLOCKER: fixture path pre-seeded on sys.path", flush=True)
        return 2
    active_rel = f"sources/{issue}/publication/v2/editorial-corrections/{active_id}/publication/publication-candidate-v2.json"
    old_id = active_id[:-1] + "1" if active_id[-1:].isdigit() else active_id + "-old"
    old_rel = f"sources/{issue}/publication/v2/editorial-corrections/{old_id}/publication/publication-candidate-v2.json"
    inert_rel = f"sources/{issue}/publication/v2/editorial-corrections/{active_id}/publication/publication-set.json"

    if scenario.startswith("manual-"):
        env = {"REQUESTED_CANDIDATE": {"manual-active": active_rel, "manual-old": old_rel,
                                      "manual-inert": inert_rel}[scenario]}
        if scenario == "manual-old" and not (active / old_rel).is_file():
            print(f"MANUAL_OLD_SKIP no stale file present ({old_rel})", flush=True)
            return 0
        exc, out = _run_full(active, env)
        got = _parse_outputs(out)
        if scenario == "manual-active":
            if exc is not None:
                print(f"MANUAL_ACTIVE_FAIL refused: {exc}", flush=True)
                return 1
            assert got.get("candidate_path") == active_rel, got
            print(f"MANUAL_ACTIVE_PASS issue={got.get('issue_id')} candidate={got.get('candidate_path')} "
                  f"pdf={got.get('pdf_path')} pages={got.get('page_count')}", flush=True)
            return 0
        if exc is None:
            print(f"{scenario.upper()}_UNEXPECTED_PASS {got}", flush=True)
            return 1
        print(f"{scenario.upper()}_REFUSED_OK {exc}", flush=True)
        return 0

    # PR scenarios: real temp repo + real artifact commits (no mocks).
    work = pathlib.Path(tempfile.mkdtemp(prefix=f"r4e-export-{tag}-", dir=R4E_TMP))
    print(f"PRWORK={work}", flush=True)
    try:
        if scenario == "pr-positive":
            cp = subprocess.run(["cp", "-a", str(inert) + "/.", str(work)], capture_output=True, text=True, timeout=300)
            assert cp.returncode == 0, f"inert cp failed {cp.stderr[:200]}"
            rdir = work / f"sources/{issue}/publication/v2/editorial-corrections/{active_id}"
            shutil.rmtree(rdir)
            assert _git(work, "add", "-A").returncode == 0
            assert _git(work, "-c", "user.name=R4e Export Probe", "-c", "user.email=export-probe-r4e@example.invalid",
                        "commit", "-q", "-m", "R4e test: first-active fixture state (artifact-only)").returncode == 0
            base = _git(work, "rev-parse", "HEAD").stdout.strip()
            ov = subprocess.run(f"cd {active} && tar cf - --exclude=.git . | tar xf - -C {work}",
                                shell=True, capture_output=True, text=True, timeout=300)
            assert ov.returncode == 0, f"overlay failed {ov.stderr[:200]}"
            assert _git(work, "add", "-A").returncode == 0
            assert _git(work, "-c", "user.name=R4e Export Probe", "-c", "user.email=export-probe-r4e@example.invalid",
                        "commit", "-q", "-m", "R4e test: second-correction activation delta (artifact-only)").returncode == 0
            assert _git(work, "status", "--porcelain").stdout.strip() == "", "work repo must be clean"
        elif scenario == "pr-unrelated":
            cp = subprocess.run(["cp", "-a", str(active) + "/.", str(work)], capture_output=True, text=True, timeout=300)
            assert cp.returncode == 0, f"active cp failed {cp.stderr[:200]}"
            (work / "notes-pr-probe-r4e.txt").write_text("synthetic unrelated artifact for PR negative\n")
            assert _git(work, "add", "notes-pr-probe-r4e.txt").returncode == 0
            assert _git(work, "-c", "user.name=R4e Export Probe", "-c", "user.email=export-probe-r4e@example.invalid",
                        "commit", "-q", "-m", "R4e test: unrelated artifact (PR negative)").returncode == 0
            base = _git(work, "rev-parse", "HEAD~1").stdout.strip()
        else:  # pr-inert
            cp = subprocess.run(["cp", "-a", str(active) + "/.", str(work)], capture_output=True, text=True, timeout=300)
            assert cp.returncode == 0, f"active cp failed {cp.stderr[:200]}"
            setf = work / inert_rel
            with open(setf, "ab") as fh:
                fh.write(b"\n")
            assert _git(work, "add", str(inert_rel)).returncode == 0
            assert _git(work, "-c", "user.name=R4e Export Probe", "-c", "user.email=export-probe-r4e@example.invalid",
                        "commit", "-q", "-m", "R4e test: inert-set-only change (PR negative)").returncode == 0
            base = _git(work, "rev-parse", "HEAD~1").stdout.strip()
        exc, out = _run_full(work, {"REQUESTED_CANDIDATE": "", "BASE_SHA": base})
        got = _parse_outputs(out)
        if scenario == "pr-positive":
            if exc is not None:
                print(f"PR_POSITIVE_FAIL refused: {exc} (work preserved at {work})", flush=True)
                return 1
            assert got.get("candidate_path") == active_rel, got
            print(f"PR_POSITIVE_PASS issue={got.get('issue_id')} candidate={got.get('candidate_path')} "
                  f"base={base[:12]} (real diff, real commit, no mocks)", flush=True)
        else:
            if exc is None:
                print(f"{scenario.upper()}_UNEXPECTED_PASS {got} (work preserved at {work})", flush=True)
                return 1
            print(f"{scenario.upper()}_REFUSED_OK {exc}", flush=True)
        shutil.rmtree(work, ignore_errors=False)
        print(f"PRWORK_CLEANED {scenario}", flush=True)
        return 0
    except BaseException:
        print(f"PRWORK_PRESERVED_ON_FAILURE (no autoclean): inspect manually", flush=True)
        raise


if __name__ == "__main__":
    sys.exit(main())
