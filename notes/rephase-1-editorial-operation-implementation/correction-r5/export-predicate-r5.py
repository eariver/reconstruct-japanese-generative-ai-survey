#!/usr/bin/env python3
"""R5 export workflow full predicate probe (offline, no Actions/GitHub).

Executes the ACTUAL current R5-fixed export workflow Python predicate end-to-end
(extracted verbatim from DST fixed workflow file) with available weekly R4e
fixtures (no rebuilds, artifact-only commits). Binds fixture's own modules
(single-root scripts.__path__), actual git diff (BASE...HEAD), no mocks.

Scenarios (same as R4e + R5 State-driven):
- manual-active: REQUESTED_CANDIDATE=<active versioned> -> PASS (scoped derivation, no global audit).
- manual-old: REQUESTED_CANDIDATE=<superseded r1> -> refuse (stale canonical).
- manual-inert: REQUESTED_CANDIDATE=<publication-set.json> -> refuse (inert without activation).
- pr-positive: temp repo = inert + first-active commit, overlay active + second commit.
  With R5 State-driven fix, exports exact State-bound active candidate even when
  diff has 0 versioned-candidate filenames (old pathspec bug) or 2 (old+new).
  Previously failed with "found 0" (raw exit 1 in correction-r4e).
- pr-unrelated: temp repo + unrelated file commit -> refuse.
- pr-inert: temp repo + inert-set-only change (State unchanged) -> refuse.
- Retained/symlink excluded: states_changed includes retained copy but filtered;
  symlinked State/Candidate refused via lstat.

Saved BEFORE execution. Temp repos under $R5_TMPDIR (default /dev/shm); removed
on success, preserved + reported on failure. Fixtures never mutated. No mocks,
no git diff mocking, no Human approval, no candidate minting (commits only
record existing fixture artifacts).

Usage: export-predicate-r5.py ACTIVE_ROOT INERT_ROOT ISSUE ACTIVE_ID SCENARIO
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
    print("BLOCKER PYTHONDONTWRITEBYTECODE!=1 (set BEFORE python startup)", flush=True)
    sys.exit(2)
_pfx = os.environ.get("PYTHONPYCACHEPREFIX", "")
if not _pfx.startswith("/tmp/"):
    print(f"BLOCKER PYTHONPYCACHEPREFIX must be /tmp/... external, got {_pfx!r}", flush=True)
    sys.exit(2)
for _v in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
           "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR", "GIT_PREFIX"):
    if os.environ.get(_v):
        print(f"BLOCKER unsafe inherited {_v}", flush=True)
        sys.exit(2)

R5_TMP = os.environ.get("R5_TMPDIR", "/dev/shm")
FIXED_WORKFLOW = os.environ.get(
    "R5_FIXED_WORKFLOW",
    "/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60/.github/workflows/survey-production-v2-export-publication-preview.yml",
)
SCENARIOS = ("manual-active", "manual-old", "manual-inert",
             "pr-positive", "pr-unrelated", "pr-inert")


def _log(m: str):
    print(m, flush=True)


def _git(root: pathlib.Path, *args: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file"})
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, timeout=120, env=env)


def _extract_predicate_fixed() -> str:
    wf = pathlib.Path(FIXED_WORKFLOW).read_text()
    if "def _derive_expected_state_for_candidate" not in wf or "active_from_states" not in wf:
        raise SystemExit("BLOCKER fixed workflow missing R5 scoped/State-driven code")
    start = wf.index("          python - <<'PY'")
    code_start = wf.index("\n", start) + 1
    end = wf.index("\n          PY\n", code_start)
    return textwrap.dedent(wf[code_start:end])


def _run_full(root: pathlib.Path, extra_env: dict) -> tuple:
    for m in [m for m in list(sys.modules) if m == "scripts" or m.startswith("scripts.")]:
        del sys.modules[m]
    sys.path.insert(0, str(root))
    try:
        import scripts as _pkg
        if list(getattr(_pkg, "__path__", [])) != [str(root / "scripts")]:
            return SystemExit(f"BLOCKER scripts namespace not single-root: {list(getattr(_pkg, '__path__', []))}"), ""
        block = _extract_predicate_fixed()
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


def main() -> int:
    if len(sys.argv) != 6:
        print(f"usage: {sys.argv[0]} ACTIVE_ROOT INERT_ROOT ISSUE ACTIVE_ID SCENARIO", flush=True)
        return 2
    active = pathlib.Path(sys.argv[1]).resolve()
    inert = pathlib.Path(sys.argv[2]).resolve()
    issue, active_id, scenario = sys.argv[3], sys.argv[4], sys.argv[5]
    tag = scenario.replace("-", "")
    print(f"ACTIVE={active} INERT={inert} ISSUE={issue} ACTIVE={active_id} SCENARIO={scenario} FIXED_WF={FIXED_WORKFLOW}", flush=True)
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

    work = pathlib.Path(tempfile.mkdtemp(prefix=f"r5-export-{tag}-", dir=R5_TMP))
    print(f"PRWORK={work}", flush=True)
    try:
        if scenario == "pr-positive":
            cp = subprocess.run(["cp", "-a", str(inert) + "/.", str(work)], capture_output=True, text=True, timeout=300)
            assert cp.returncode == 0, f"inert cp failed {cp.stderr[:200]}"
            rdir = work / f"sources/{issue}/publication/v2/editorial-corrections/{active_id}"
            shutil.rmtree(rdir)
            assert _git(work, "add", "-A").returncode == 0
            assert _git(work, "-c", "user.name=R5 Export Probe", "-c", "user.email=export-probe-r5@example.invalid",
                        "commit", "-q", "-m", "R5 test: first-active fixture state (artifact-only)").returncode == 0
            base = _git(work, "rev-parse", "HEAD").stdout.strip()
            ov = subprocess.run(f"cd {active} && tar cf - --exclude=.git . | tar xf - -C {work}",
                                shell=True, capture_output=True, text=True, timeout=300)
            assert ov.returncode == 0, f"overlay failed {ov.stderr[:200]}"
            assert _git(work, "add", "-A").returncode == 0
            assert _git(work, "-c", "user.name=R5 Export Probe", "-c", "user.email=export-probe-r5@example.invalid",
                        "commit", "-q", "-m", "R5 test: second-correction activation delta (artifact-only)").returncode == 0
            assert _git(work, "status", "--porcelain").stdout.strip() == "", "work repo must be clean"
        elif scenario == "pr-unrelated":
            cp = subprocess.run(["cp", "-a", str(active) + "/.", str(work)], capture_output=True, text=True, timeout=300)
            assert cp.returncode == 0, f"active cp failed {cp.stderr[:200]}"
            (work / "notes-pr-probe-r5.txt").write_text("synthetic unrelated artifact for PR negative\n")
            assert _git(work, "add", "notes-pr-probe-r5.txt").returncode == 0
            assert _git(work, "-c", "user.name=R5 Export Probe", "-c", "user.email=export-probe-r5@example.invalid",
                        "commit", "-q", "-m", "R5 test: unrelated artifact (PR negative)").returncode == 0
            base = _git(work, "rev-parse", "HEAD~1").stdout.strip()
        else:  # pr-inert
            cp = subprocess.run(["cp", "-a", str(active) + "/.", str(work)], capture_output=True, text=True, timeout=300)
            assert cp.returncode == 0, f"active cp failed {cp.stderr[:200]}"
            setf = work / inert_rel
            with open(setf, "ab") as fh:
                fh.write(b"\n")
            assert _git(work, "add", str(inert_rel)).returncode == 0
            assert _git(work, "-c", "user.name=R5 Export Probe", "-c", "user.email=export-probe-r5@example.invalid",
                        "commit", "-q", "-m", "R5 test: inert-set-only change (PR negative)").returncode == 0
            base = _git(work, "rev-parse", "HEAD~1").stdout.strip()
        exc, out = _run_full(work, {"REQUESTED_CANDIDATE": "", "BASE_SHA": base})
        got = _parse_outputs(out)
        if scenario == "pr-positive":
            if exc is not None:
                print(f"PR_POSITIVE_FAIL refused: {exc} (work preserved at {work})", flush=True)
                return 1
            assert got.get("candidate_path") == active_rel, got
            print(f"PR_POSITIVE_PASS issue={got.get('issue_id')} candidate={got.get('candidate_path')} "
                  f"base={base[:12]} (real diff, real commit, State-driven, no filename-count)", flush=True)
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
