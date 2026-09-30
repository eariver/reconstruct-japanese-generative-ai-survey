import subprocess, os
DST = "/tmp/jgas-rephase-r1-assembly-20260929T143833Z"
env = dict(os.environ)
env["GIT_AUTHOR_NAME"] = "R1 Assembly General Co-Worker"
env["GIT_AUTHOR_EMAIL"] = "r1-assembly@example.invalid"
env["GIT_COMMITTER_NAME"] = "R1 Assembly General Co-Worker"
env["GIT_COMMITTER_EMAIL"] = "r1-assembly@example.invalid"
msg = "R1 assembly: apply reviewed seven-path mechanical-refresh increment onto e4 lineage\n\nParent e4c82692abee6acedbba07815b0d74ccefb80a7e. Seven paths byte-identical to b74db67 final copies (no PASS transfer)."
print("=== pre-commit log ===")
r0 = subprocess.run(["git", "-C", DST, "log", "--oneline", "-10"], capture_output=True, text=True)
print(repr(r0.stdout))
print("=== commit ===")
r = subprocess.run(["git", "-C", DST, "commit", "-m", msg], capture_output=True, text=True, cwd=DST, env=env)
print("CMD: git commit -m (no --no-verify, no bypass, process-local identity, actual clock)")
print("STDOUT:", repr(r.stdout))
print("STDERR:", repr(r.stderr))
print("EXIT:", r.returncode)
print("=== after: rev-parse ===")
for a in [["rev-parse", "HEAD"], ["rev-parse", "HEAD^{tree}"], ["log", "--format=%H %P %T %s %ci", "-1"], ["branch", "--show-current"], ["status", "--short", "--branch"]]:
    rr = subprocess.run(["git", "-C", DST] + a, capture_output=True, text=True)
    print(a, repr(rr.stdout.strip()), "exit", rr.returncode, "stderr", repr(rr.stderr.strip()))
print("DONE_COMMIT")
