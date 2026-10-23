#!/usr/bin/env python3
"""R5b export workflow predicate probe (offline, no Actions/GitHub) on the FINAL
R5b source epoch (fixture roots bound to SOURCE HEAD 10e8662 via env pins).

Usage: export-predicate-r5b.py ACTIVE_ROOT INERT_ROOT ISSUE ACTIVE_ID SCENARIO
  SCENARIO in {manual-active, manual-old, manual-oldcanonical, manual-inert,
               manual-alias, pr-positive, pr-unrelated, pr-inert,
               pr-ambiguous, pr-retained-only}

Executes the ACTUAL current export workflow Python predicate end-to-end
(extracted verbatim from the fixture's own .github workflow file, fixed
_rel_expected version) with the fixture's own modules (binding-checked:
every scripts.* __file__ under the run root, single-root scripts.__path__).
The predicate's own git diff / State discovery / validation run for real;
stdout (the CI $GITHUB_OUTPUT payload) is captured and asserted.

- manual-active: REQUESTED_CANDIDATE=<active versioned candidate> -> PASS.
- manual-old: REQUESTED_CANDIDATE=<superseded r*-1 versioned candidate> -> refuse.
- manual-oldcanonical: REQUESTED_CANDIDATE=<old canonical candidate> -> refuse
  (stale canonical refused after activation; SKIP when route has no canonical
  candidate file, e.g. Weekly whose before_candidate_ref is honestly null).
- manual-inert: REQUESTED_CANDIDATE=<publication-set.json> -> refuse.
- manual-alias: symlink probe copy aliasing the active candidate -> refuse
  (alias/symlink laundering refused; probe copy lives under FINAL_R5B_ROOT).
- pr-positive: work repo = inert state + first-active commit, then overlay of
  the real active fixture + second commit ("second-correction activation
  delta", commit carries both old+new Candidate files vs SOURCE); BASE_SHA=
  SOURCE HEAD (env R5B_EXPECT_HEAD, ancestry asserted). Real git diff ->
  exactly one State-bound candidate -> PASS (also proves artifact-only
  commit ancestry + tool closure predicates on the artifact-only HEAD).
- pr-unrelated: temp repo + commit touching only an unrelated root file ->
  refuse (exactly-one-candidate rule).
- pr-inert: temp repo + commit touching only publication-set.json ->
  refuse (inert-set guard, no State activation change).
- pr-ambiguous: work repo combines the Weekly active tree and the Longform
  active tree (same SOURCE HEAD, env R5B_OTHER_ACTIVE_ROOT); two authoritative
  States select two distinct candidates -> refuse (genuinely ambiguous).
- pr-retained-only: work repo + commit adding only a retained-copy State
  decoy (non-canonical path, same bytes); BASE=pre-decoy commit -> refuse
  (no State activation change; retained decoy ignored, not adopted).
Work repos live under $R5B_TMPDIR (default FINAL_R5B_ROOT/tmp); preserved on
failure AND kept on success as evidence (no cleanup of owned evidence).
Fixtures never mutated (alias probe uses a cp -a copy). No mocks, no git
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
_fr = os.environ.get("FINAL_R5B_ROOT", "")
if not _fr or not pathlib.Path(_fr).is_dir():
    print(f"BLOCKER: FINAL_R5B_ROOT missing/not-a-dir: {_fr!r}", flush=True)
    sys.exit(2)
_pfx = os.environ.get("PYTHONPYCACHEPREFIX", "")
if not _pfx.startswith(_fr + "/"):
    print(f"BLOCKER: PYTHONPYCACHEPREFIX must be under FINAL_R5B_ROOT ({_fr}), got {_pfx!r}", flush=True)
    sys.exit(2)
_tdir = os.environ.get("TMPDIR", "")
if not _tdir.startswith(_fr + "/"):
    print(f"BLOCKER: TMPDIR must be under FINAL_R5B_ROOT ({_fr}), got {_tdir!r}", flush=True)
    sys.exit(2)
for _v in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
           "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR", "GIT_PREFIX"):
    if os.environ.get(_v):
        print(f"BLOCKER unsafe inherited {_v}", flush=True)
        sys.exit(2)

R5B_TMP = os.environ.get("R5B_TMPDIR", os.path.join(_fr, "tmp"))
SCENARIOS = ("manual-active", "manual-old", "manual-oldcanonical", "manual-inert",
             "manual-alias", "pr-positive", "pr-unrelated", "pr-inert",
             "pr-ambiguous", "pr-retained-only")


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
    exp_head = os.environ.get("R5B_EXPECT_HEAD", "").strip().lower()
    exp_count = int(os.environ.get("R5B_EXPECT_COUNT", "0") or 0)
    if len(exp_head) != 40 or exp_count <= 0:
        print(f"BLOCKER R5B_EXPECT_HEAD/COUNT pins required, got {exp_head!r}/{exp_count}", flush=True)
        return 2
    _check_binding_and_head(active, exp_head, exp_count)
    _check_binding_and_head(inert, exp_head, exp_count)
    print(f"BINDING_OK active+inert HEAD={exp_head} count={exp_count}", flush=True)
    active_rel = f"sources/{issue}/publication/v2/editorial-corrections/{active_id}/publication/publication-candidate-v2.json"
    old_id = active_id[:-1] + "1" if active_id[-1:].isdigit() else active_id + "-old"
    old_rel = f"sources/{issue}/publication/v2/editorial-corrections/{old_id}/publication/publication-candidate-v2.json"
    inert_rel = f"sources/{issue}/publication/v2/editorial-corrections/{active_id}/publication/publication-set.json"
    oldcanon_rel = f"sources/{issue}/publication/v2/publication-candidate-v2.json"

    if scenario.startswith("manual-"):
        if scenario == "manual-alias":
            probe = pathlib.Path(tempfile.mkdtemp(prefix=f"r5b-alias-{tag}-{issue}-", dir=R5B_TMP))
            print(f"ALIASPROBE={probe}", flush=True)
            cp = subprocess.run(["cp", "-a", str(active) + "/.", str(probe)], capture_output=True,
                                text=True, timeout=300)
            assert cp.returncode == 0, f"alias probe cp failed {cp.stderr[:200]}"
            alias_rel = f"sources/{issue}/publication/v2/editorial-corrections/{active_id}/publication/alias-candidate.json"
            try:
                (probe / alias_rel).symlink_to("publication-candidate-v2.json")
            except FileExistsError:
                pass
            exc, out = _run_full(probe, {"REQUESTED_CANDIDATE": alias_rel})
            got = _parse_outputs(out)
            if exc is None:
                print(f"MANUAL_ALIAS_UNEXPECTED_PASS {got} (probe kept at {probe})", flush=True)
                return 1
            print(f"MANUAL_ALIAS_REFUSED_OK {exc} (probe kept at {probe})", flush=True)
            return 0
        env = {"REQUESTED_CANDIDATE": {"manual-active": active_rel, "manual-old": old_rel,
                                       "manual-oldcanonical": oldcanon_rel,
                                       "manual-inert": inert_rel}[scenario]}
        if scenario in ("manual-old", "manual-oldcanonical") and not (active / env["REQUESTED_CANDIDATE"]).is_file():
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

    # PR scenarios: real work repo + real artifact commits (no mocks).
    # Work repos are kept under FINAL_R5B_ROOT as evidence (never deleted).
    work = pathlib.Path(tempfile.mkdtemp(prefix=f"r5b-export-{tag}-{issue}-", dir=R5B_TMP))
    print(f"PRWORK={work}", flush=True)
    try:
        if scenario == "pr-positive":
            cp = subprocess.run(["cp", "-a", str(inert) + "/.", str(work)], capture_output=True, text=True, timeout=300)
            assert cp.returncode == 0, f"inert cp failed {cp.stderr[:200]}"
            rdir = work / f"sources/{issue}/publication/v2/editorial-corrections/{active_id}"
            shutil.rmtree(rdir)
            c1 = _commit_all(work, "R5b test: first-active fixture state (artifact-only)")
            ov = subprocess.run(f"cd {active} && tar cf - --exclude=.git . | tar xf - -C {work}",
                                shell=True, capture_output=True, text=True, timeout=300)
            assert ov.returncode == 0, f"overlay failed {ov.stderr[:200]}"
            c2 = _commit_all(work, "R5b test: second-correction activation delta (artifact-only)")
            # BASE=SOURCE HEAD (task pin): the artifact-only delta vs SOURCE must
            # select exactly the one State-bound candidate; first-commit ancestry
            # must root at SOURCE HEAD.
            base = exp_head
            assert _git(work, "merge-base", "--is-ancestor", base, "HEAD").returncode == 0, \
                "BASE=SOURCE HEAD is not an ancestor of the artifact HEAD"
            assert _git(work, "merge-base", "--is-ancestor", c1, "HEAD").returncode == 0
            print(f"PR_COMMITS c1={c1[:12]} c2={c2[:12]} base=SOURCE_HEAD={base[:12]}", flush=True)
        elif scenario == "pr-ambiguous":
            other_active = pathlib.Path(os.environ.get("R5B_OTHER_ACTIVE_ROOT", "") or "")
            other_issue = os.environ.get("R5B_OTHER_ISSUE", "").strip()
            other_id = os.environ.get("R5B_OTHER_ACTIVE_ID", "").strip()
            if not str(other_active) or not other_issue or not other_id:
                print("BLOCKER pr-ambiguous requires R5B_OTHER_ACTIVE_ROOT/ISSUE/ACTIVE_ID", flush=True)
                return 2
            other_active = other_active.resolve()
            _check_binding_and_head(other_active, exp_head, exp_count)
            cp = subprocess.run(["cp", "-a", str(inert) + "/.", str(work)], capture_output=True, text=True, timeout=300)
            assert cp.returncode == 0, f"inert cp failed {cp.stderr[:200]}"
            rdir = work / f"sources/{issue}/publication/v2/editorial-corrections/{active_id}"
            shutil.rmtree(rdir)
            c1 = _commit_all(work, "R5b test: first-active fixture state (artifact-only)")
            for src in (active, other_active):
                ov = subprocess.run(f"cd {src} && tar cf - --exclude=.git . | tar xf - -C {work}",
                                    shell=True, capture_output=True, text=True, timeout=300)
                assert ov.returncode == 0, f"overlay failed for {src}: {ov.stderr[:200]}"
            c2 = _commit_all(work, "R5b test: two-edition activation delta (ambiguous, artifact-only)")
            base = exp_head
            assert _git(work, "merge-base", "--is-ancestor", base, "HEAD").returncode == 0
            other_rel = f"sources/{other_issue}/publication/v2/editorial-corrections/{other_id}/publication/publication-candidate-v2.json"
            assert (work / other_rel).is_file(), f"combined tree missing other candidate {other_rel}"
            print(f"PR_COMMITS c1={c1[:12]} c2={c2[:12]} base=SOURCE_HEAD (ambiguous {issue}+{other_issue})", flush=True)
        elif scenario == "pr-retained-only":
            cp = subprocess.run(["cp", "-a", str(active) + "/.", str(work)], capture_output=True, text=True, timeout=300)
            assert cp.returncode == 0, f"active cp failed {cp.stderr[:200]}"
            c1 = _commit_all(work, "R5b test: active fixture state (artifact-only)")
            decoy_dir = work / f"sources/{issue}/retained-copy"
            decoy_dir.mkdir(parents=True, exist_ok=False)
            shutil.copy2(work / f"sources/{issue}/production-state.json",
                          decoy_dir / "production-state.json")
            c2 = _commit_all(work, "R5b test: retained-copy State decoy only (negative)")
            base = c1
            print(f"PR_COMMITS c1={c1[:12]} decoy={c2[:12]} base=c1 (retained decoy only)", flush=True)
        elif scenario == "pr-unrelated":
            cp = subprocess.run(["cp", "-a", str(active) + "/.", str(work)], capture_output=True, text=True, timeout=300)
            assert cp.returncode == 0, f"active cp failed {cp.stderr[:200]}"
            (work / "notes-pr-probe-r5b.txt").write_text("synthetic unrelated artifact for PR negative\n")
            assert _git(work, "add", "notes-pr-probe-r5b.txt").returncode == 0
            assert _git(work, "-c", "user.name=R5b Export Probe", "-c", "user.email=export-probe-r5b@example.invalid",
                        "commit", "-q", "-m", "R5b test: unrelated artifact (PR negative)").returncode == 0
            base = _git(work, "rev-parse", "HEAD~1").stdout.strip()
        else:  # pr-inert
            cp = subprocess.run(["cp", "-a", str(active) + "/.", str(work)], capture_output=True, text=True, timeout=300)
            assert cp.returncode == 0, f"active cp failed {cp.stderr[:200]}"
            setf = work / inert_rel
            with open(setf, "ab") as fh:
                fh.write(b"\n")
            assert _git(work, "add", str(inert_rel)).returncode == 0
            assert _git(work, "-c", "user.name=R5b Export Probe", "-c", "user.email=export-probe-r5b@example.invalid",
                        "commit", "-q", "-m", "R5b test: inert-set-only change (PR negative)").returncode == 0
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
                print(f"{scenario.upper()}_UNEXPECTED_PASS {got} (work kept at {work})", flush=True)
                return 1
            if scenario == "pr-ambiguous" and "ambiguous" not in str(exc).lower():
                print(f"PR_AMBIGUOUS_WRONG_REFUSAL {exc} (work kept at {work})", flush=True)
                return 1
            if scenario == "pr-retained-only" and "without State activation" not in str(exc):
                print(f"PR_RETAINED_WRONG_REFUSAL {exc} (work kept at {work})", flush=True)
                return 1
            print(f"{scenario.upper()}_REFUSED_OK {exc} (work kept at {work})", flush=True)
        print(f"PRWORK_KEPT {scenario} {work}", flush=True)
        return 0
    except BaseException:
        print(f"PRWORK_PRESERVED_ON_FAILURE (no autoclean): inspect manually", flush=True)
        raise


if __name__ == "__main__":
    sys.exit(main())
