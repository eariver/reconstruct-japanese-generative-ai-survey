import subprocess
DST = "/tmp/jgas-rephase-r1-assembly-20260929T143833Z"
def git(args):
    r = subprocess.run(["git", "-C", DST] + args, capture_output=True, text=True)
    return r
print("status raw:")
r = git(["status", "--porcelain=v1", "-uall"])
print(repr(r.stdout))
print("diff cached name-only:")
print(repr(git(["diff", "--cached", "--name-only"]).stdout))
print("diff unstaged name-only:")
print(repr(git(["diff", "--name-only"]).stdout))
print("ls-files -s seven:")
for p in ["scripts/survey_agent_control_v2.py","scripts/survey_reader_surface_gate_v2.py","scripts/survey_weekly_derivation_v2.py","tests/test_survey_publication_revalidation_v2.py"]:
    rr = git(["ls-files", "-s", "--", p])
    print(p, repr(rr.stdout.strip()))
print("diff HEAD stat:")
print(git(["diff", "HEAD", "--stat"]).stdout[:2000])
