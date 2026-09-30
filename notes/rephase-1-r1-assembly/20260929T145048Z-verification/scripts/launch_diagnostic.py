import subprocess, os
DST = "/tmp/jgas-rephase-r1-assembly-20260929T143833Z"
RAW = "/tmp/jgas-r1-verify-20260929T145048Z/raw"
SCRIPT = "/mnt/c/Users/shake/AppData/Local/Temp/opencode/run_diagnostic.py"
for fn in ["diagnostic.stdout", "diagnostic.stderr", "diagnostic.exit"]:
    fp = os.path.join(RAW, fn)
    assert not os.path.exists(fp), "refuse overwrite " + fp
env = dict(os.environ)
assert env.get("PYTHONDONTWRITEBYTECODE") == "1"
# ensure no GIT_* in env
for k in list(env.keys()):
    assert not k.startswith("GIT_"), "GIT override " + k
r = subprocess.run(["/tmp/jgas-rephase-application-venv/bin/python3.12", SCRIPT], cwd=DST, capture_output=True, text=True, env=env)
with open(os.path.join(RAW, "diagnostic.stdout"), "w", encoding="utf-8", newline="\n") as f:
    f.write(r.stdout)
with open(os.path.join(RAW, "diagnostic.stderr"), "w", encoding="utf-8", newline="\n") as f:
    f.write(r.stderr)
with open(os.path.join(RAW, "diagnostic.exit"), "w", encoding="utf-8", newline="\n") as f:
    f.write(str(r.returncode) + "\n")
print("DIAG_EXIT:", r.returncode)
print("STDOUT_LEN:", len(r.stdout))
print("STDERR_LEN:", len(r.stderr))
print(r.stdout[-2000:] if len(r.stdout) > 2000 else r.stdout)
print("STDERR_TAIL:", r.stderr[-1000:] if r.stderr else "(empty)")
