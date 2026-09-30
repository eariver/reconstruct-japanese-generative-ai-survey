import subprocess
DST = "/tmp/jgas-rephase-r1-assembly-20260929T143833Z"
PATCH = "/mnt/d/Git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-mechanical-refresh/correction/final-b74db679f03908048db91420a8f262d412b8f58c/patch-final-a1-b74db67.patch"
r = subprocess.run(["git", "-C", DST, "apply", PATCH], capture_output=True, text=True)
print("CMD: git -C DST apply PATCH")
print("STDOUT:", repr(r.stdout))
print("STDERR:", repr(r.stderr))
print("EXIT:", r.returncode)
# status after
s = subprocess.run(["git", "-C", DST, "status", "--short", "--branch"], capture_output=True, text=True)
print("STATUS:", repr(s.stdout))
d = subprocess.run(["git", "-C", DST, "diff", "--numstat"], capture_output=True, text=True)
print("DIFF_NUMSTAT:", repr(d.stdout))
ds = subprocess.run(["git", "-C", DST, "diff", "--name-status"], capture_output=True, text=True)
print("DIFF_NAME_STATUS:", repr(ds.stdout))
