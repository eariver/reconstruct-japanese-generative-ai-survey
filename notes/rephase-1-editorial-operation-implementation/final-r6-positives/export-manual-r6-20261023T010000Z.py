#!/usr/bin/env python3
"""R6 exact-epoch export manual probe (offline, no Actions/GitHub) on the FINAL
R6 source epoch (fixture roots bound to SOURCE HEAD ce90246 via env pins).

Usage: export-manual-r6-20261023T010000Z.py ACTIVE_ROOT INERT_ROOT ISSUE ACTIVE_ID SCENARIO
  SCENARIO in {manual-active, manual-old, manual-inert}

The R6 export workflow source is unchanged from R5b, so no full Git-diff
matrix rerun: this probe covers the final exact-epoch manual matrix only.
Executes the ACTUAL current export workflow Python predicate end-to-end
(extracted verbatim from the fixture's own .github workflow file, fixed
_rel_expected version) with the fixture's own modules (binding-checked:
every scripts.* __file__ under the run root, single-root scripts.__path__).
The predicate's own State discovery / validation runs for real; stdout (the
CI $GITHUB_OUTPUT payload) is captured and asserted.

- manual-active: REQUESTED_CANDIDATE=<active versioned candidate> -> PASS.
- manual-old: REQUESTED_CANDIDATE=<superseded r*-1 versioned candidate> -> refuse.
- manual-inert: REQUESTED_CANDIDATE=<publication-set.json> -> refuse (inert
  valid set not adopted without activation).
Readonly selection (which State-bound SHA is active) is covered separately
by readonly-selection-r6 (both routes). No work repos, no commits, no mocks,
no real Human/production approval. Fixtures never mutated.

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
_fr = os.environ.get("FINAL_R6_ROOT", "")
if not _fr or not pathlib.Path(_fr).is_dir():
    print(f"BLOCKER: FINAL_R6_ROOT missing/not-a-dir: {_fr!r}", flush=True)
    sys.exit(2)
_pfx = os.environ.get("PYTHONPYCACHEPREFIX", "")
if not _pfx.startswith(_fr + "/"):
    print(f"BLOCKER: PYTHONPYCACHEPREFIX must be under FINAL_R5B_ROOT ({_fr}), got {_pfx!r}", flush=True)
    sys.exit(2)
_tdir = os.environ.get("TMPDIR", "")
if not _tdir.startswith(_fr + "/"):
    print(f"BLOCKER: TMPDIR must be under FINAL_R6_ROOT ({_fr}), got {_tdir!r}", flush=True)
    sys.exit(2)
for _v in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
           "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR", "GIT_PREFIX"):
    if os.environ.get(_v):
        print(f"BLOCKER unsafe inherited {_v}", flush=True)
        sys.exit(2)

SCENARIOS = ("manual-active", "manual-old", "manual-inert")


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
    top = _git(root, "rev-parse", "--show-toplevel").stdout.strip()
    gdir = _git(root, "rev-parse", "--absolute-git-dir").stdout.strip()
    if pathlib.Path(top) != root or pathlib.Path(gdir) != root / ".git":
        raise SystemExit(f"BLOCKER .git not owned: top={top} gitdir={gdir} root={root}")
    for _alt in (root / ".git/objects/info/alternates", root / ".git/info/alternates"):
        if _alt.exists():
            raise SystemExit(f"BLOCKER alternates present: {_alt}")


def _commit_all(work: pathlib.Path, message: str) -> str:
    assert _git(work, "add", "-A").returncode == 0
    assert _git(work, "-c", "user.name=R5b Export Probe", "-c",
               "user.email=export-probe-r5b@example.invalid",
               "commit", "-q", "-m", message).returncode == 0
    assert _git(work, "status", "--porcelain").stdout.strip() == "", "work repo must be clean"
    return _git(work, "rev-parse", "HEAD").stdout.strip()


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
    if [p for p in sys.path if "/jgas-" in p or "/dev/shm/" in p or "/tmp/opencode" in p]:
        print("BLOCKER: foreign fixture path pre-seeded on sys.path", flush=True)
        return 2
    exp_head = os.environ.get("R6_EXPECT_HEAD", "").strip().lower()
    exp_count = int(os.environ.get("R6_EXPECT_COUNT", "0") or 0)
    if len(exp_head) != 40 or exp_count <= 0:
        print(f"BLOCKER R6_EXPECT_HEAD/COUNT pins required, got {exp_head!r}/{exp_count}", flush=True)
        return 2
    _check_binding_and_head(active, exp_head, exp_count)
    _check_binding_and_head(inert, exp_head, exp_count)
    print(f"BINDING_OK active+inert HEAD={exp_head} count={exp_count}", flush=True)
    active_rel = f"sources/{issue}/publication/v2/editorial-corrections/{active_id}/publication/publication-candidate-v2.json"
    old_id = active_id[:-1] + "1" if active_id[-1:].isdigit() else active_id + "-old"
    old_rel = f"sources/{issue}/publication/v2/editorial-corrections/{old_id}/publication/publication-candidate-v2.json"
    inert_rel = f"sources/{issue}/publication/v2/editorial-corrections/{active_id}/publication/publication-set.json"

    if scenario.startswith("manual-"):
        env = {"REQUESTED_CANDIDATE": {"manual-active": active_rel, "manual-old": old_rel,
                                       "manual-inert": inert_rel}[scenario]}
        if scenario == "manual-old" and not (active / env["REQUESTED_CANDIDATE"]).is_file():
            print(f"{scenario.upper()}_SKIP no such file present ({env['REQUESTED_CANDIDATE']})", flush=True)
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
    print(f"BLOCKER unreachable scenario {scenario}", flush=True)
    return 2

if __name__ == "__main__":
    sys.exit(main())
