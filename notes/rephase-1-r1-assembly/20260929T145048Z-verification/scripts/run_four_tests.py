import subprocess, os, sys, hashlib
DST = "/tmp/jgas-rephase-r1-assembly-20260929T143833Z"
RAW = "/tmp/jgas-r1-verify-20260929T145048Z/raw"
EXP_HEAD = "481dec0c0233d7871df79a07a88aa5fe2291daa3"
EXP_TREE = "657032438c6ed8b1c055d5a120b67b4b261a5092"
# fail-closed precheck
def git(args):
    return subprocess.run(["git", "-C", DST] + args, capture_output=True, text=True)
h = git(["rev-parse", "HEAD"]).stdout.strip()
t = git(["rev-parse", "HEAD^{tree}"]).stdout.strip()
st = git(["status", "--porcelain=v1", "-uall"]).stdout
tracked = [l for l in st.strip().splitlines() if l.strip() != "" and not l.startswith("??")]
assert h == EXP_HEAD, "HEAD mismatch " + h
assert t == EXP_TREE, "TREE mismatch " + t
assert len(tracked) == 0, "tracked dirty " + repr(tracked)
assert git(["diff", "--cached", "--name-only"]).stdout.strip() == ""
assert git(["diff", "--name-only"]).stdout.strip() == ""
over = {k: v for k, v in os.environ.items() if k.startswith("GIT_")}
assert not over, "GIT overrides present " + repr(over)
assert os.environ.get("PYTHONDONTWRITEBYTECODE") == "1", "PYTHONDONTWRITEBYTECODE must be 1"
print("PRECHECK_PASS head/tree/clean/no-overrides/DONTWRITE=1", flush=True)
# exact single argv list per root task
argv = [
    "/tmp/jgas-rephase-application-venv/bin/python3.12",
    "-m", "unittest", "-v",
    "tests.test_survey_weekly_mechanical_refresh_v2.WeeklyMechanicalRefreshV2Tests.test_first_and_repeat_success",
    "tests.test_survey_weekly_mechanical_refresh_v2.WeeklyMechanicalRefreshV2Tests.test_metadata_revalidation_effective_rows_then_refresh",
    "tests.test_survey_weekly_mechanical_refresh_v2.WeeklyMechanicalRefreshV2Tests.test_active_predecessor_not_noop_and_artifact_only_noop",
    "tests.test_survey_weekly_mechanical_refresh_v2.WeeklyMechanicalRefreshV2Tests.test_pre_install_control_change_unsupported",
]
print("ARGV:", argv, flush=True)
print("CWD:", DST, flush=True)
# no-overwrite guard for outputs
for fn in ["four-tests.stdout", "four-tests.stderr", "four-tests.exit"]:
    fp = os.path.join(RAW, fn)
    assert not os.path.exists(fp), "refuse overwrite " + fp
# record python version + deps separately (best effort, not test failure)
ver = subprocess.run([argv[0], "--version"], capture_output=True, text=True)
print("PYTHON_VERSION:", ver.stdout.strip(), ver.stderr.strip(), flush=True)
# run once
r = subprocess.run(argv, cwd=DST, capture_output=True, text=True)
# write raw outputs via python (not shell redirection)
with open(os.path.join(RAW, "four-tests.stdout"), "w", encoding="utf-8", newline="\n") as f:
    f.write(r.stdout)
with open(os.path.join(RAW, "four-tests.stderr"), "w", encoding="utf-8", newline="\n") as f:
    f.write(r.stderr)
with open(os.path.join(RAW, "four-tests.exit"), "w", encoding="utf-8", newline="\n") as f:
    f.write(str(r.returncode) + "\n")
print("EXIT:", r.returncode, flush=True)
print("STDOUT_LEN:", len(r.stdout), flush=True)
print("STDERR_LEN:", len(r.stderr), flush=True)
# parse counts
import re
m = re.search(r"Ran (\d+) tests?", r.stderr + r.stdout)
print("RAN:", m.group(0) if m else "not-found", flush=True)
print("OK:", ("OK" in (r.stderr + r.stdout)), flush=True)
print("FAILED:", ("FAILED" in (r.stderr + r.stdout)), flush=True)
sk = re.search(r"skipped[^\n]*", r.stderr + r.stdout, re.IGNORECASE)
print("SKIP_LINE:", sk.group(0) if sk else "none", flush=True)
print("RUNNER_DONE", flush=True)
