import subprocess, os
DST = "/tmp/jgas-rephase-r1-assembly-20260929T143833Z"
seven = [
    "scripts/survey_agent_control_v2.py",
    "scripts/survey_reader_surface_gate_v2.py",
    "scripts/survey_weekly_derivation_v2.py",
    "tests/test_survey_publication_revalidation_v2.py",
    "scripts/survey_weekly_mechanical_refresh_v2.py",
    "tests/test_survey_weekly_mechanical_refresh_v2.py",
    "docs/weekly-mechanical-refresh.md",
]
print("=== git add ===")
r = subprocess.run(["git", "-C", DST, "add", "--"] + seven, capture_output=True, text=True)
print("CMD: git -C DST add -- seven")
print("STDOUT:", repr(r.stdout))
print("STDERR:", repr(r.stderr))
print("EXIT:", r.returncode)
print("=== status after add ===")
s = subprocess.run(["git", "-C", DST, "status", "--short", "--branch"], capture_output=True, text=True)
print(repr(s.stdout))
print("=== diff cached numstat ===")
c = subprocess.run(["git", "-C", DST, "diff", "--cached", "--numstat"], capture_output=True, text=True)
print(repr(c.stdout))
print("=== diff cached name-status ===")
c2 = subprocess.run(["git", "-C", DST, "diff", "--cached", "--name-status"], capture_output=True, text=True)
print(repr(c2.stdout))
print("DONE_ADD")
