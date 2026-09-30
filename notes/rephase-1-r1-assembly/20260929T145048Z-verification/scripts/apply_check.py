import subprocess
DST = "/tmp/jgas-rephase-r1-assembly-20260929T143833Z"
PATCH = "/mnt/d/Git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-mechanical-refresh/correction/final-b74db679f03908048db91420a8f262d412b8f58c/patch-final-a1-b74db67.patch"
r = subprocess.run(["git", "-C", DST, "apply", "--check", PATCH], capture_output=True, text=True)
print("CMD: git -C", DST, "apply", "--check", PATCH)
print("CWD: /tmp (via python cwd)")
print("STDOUT_LEN:", len(r.stdout))
print("STDOUT:", repr(r.stdout))
print("STDERR_LEN:", len(r.stderr))
print("STDERR:", repr(r.stderr))
print("EXIT:", r.returncode)
# also git version
v = subprocess.run(["git", "--version"], capture_output=True, text=True)
print("GIT_VERSION:", v.stdout.strip())
# head/tree/parent/branch
for args in [["rev-parse", "HEAD"], ["rev-parse", "HEAD^{tree}"], ["log", "--format=%P", "-1"], ["branch", "--show-current"], ["status", "--short", "--branch"]]:
    rr = subprocess.run(["git", "-C", DST] + args, capture_output=True, text=True)
    print(args, "->", repr(rr.stdout.strip()), "exit", rr.returncode, "stderr", repr(rr.stderr.strip()))
