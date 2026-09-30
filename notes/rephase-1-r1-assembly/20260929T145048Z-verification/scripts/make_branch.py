import subprocess, os
DST = "/tmp/jgas-rephase-r1-assembly-20260929T143833Z"
def git(args, **kw):
    r = subprocess.run(["git", "-C", DST] + args, capture_output=True, text=True, **kw)
    return r

print("=== before branch: log ===")
r = git(["log", "--oneline", "-10"])
print("STDOUT:", repr(r.stdout))
print("EXIT:", r.returncode, "STDERR:", repr(r.stderr))

print("=== before branch: status ===")
r = git(["status", "--short", "--branch"])
print(repr(r.stdout))

print("=== create branch ===")
r = git(["checkout", "-b", "codex/rephase-1-r1-assembly"])
print("STDOUT:", repr(r.stdout))
print("STDERR:", repr(r.stderr))
print("EXIT:", r.returncode)

print("=== after branch: rev-parse ===")
for a in [["rev-parse", "HEAD"], ["rev-parse", "HEAD^{tree}"], ["branch", "--show-current"], ["log", "--format=%H %P %T", "-1"]]:
    rr = git(a)
    print(a, repr(rr.stdout.strip()), "exit", rr.returncode)

print("=== pre-commit inspect: status ===")
print(repr(git(["status", "--short", "--branch"]).stdout))
print("=== pre-commit inspect: diff --numstat ===")
print(repr(git(["diff", "--numstat"]).stdout))
print("=== pre-commit inspect: diff HEAD --name-status (incl untracked? no) ===")
print(repr(git(["diff", "HEAD", "--name-status"]).stdout))
print("=== untracked authored ===")
uu = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"], capture_output=True, text=True, cwd=DST)
lines = [x for x in uu.stdout.strip().splitlines() if "__pycache__" not in x]
print(repr(lines))
print("DONE_BRANCH")
