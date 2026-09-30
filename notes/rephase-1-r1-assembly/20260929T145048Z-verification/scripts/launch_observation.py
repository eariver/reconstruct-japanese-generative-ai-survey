import subprocess, os
RAW = "/tmp/jgas-r1-verify-20260929T145048Z/raw"
SCRIPT = "/mnt/c/Users/shake/AppData/Local/Temp/opencode/new_observation.py"
for fn in ["new-observation.stdout", "new-observation.stderr", "new-observation.exit"]:
    assert not os.path.exists(os.path.join(RAW, fn)), "refuse overwrite " + fn
env = dict(os.environ)
r = subprocess.run(["/tmp/jgas-rephase-application-venv/bin/python3.12", SCRIPT], capture_output=True, text=True, env=env)
with open(os.path.join(RAW, "new-observation.stdout"), "w", encoding="utf-8", newline="\n") as f:
    f.write(r.stdout)
with open(os.path.join(RAW, "new-observation.stderr"), "w", encoding="utf-8", newline="\n") as f:
    f.write(r.stderr)
with open(os.path.join(RAW, "new-observation.exit"), "w", encoding="utf-8", newline="\n") as f:
    f.write(str(r.returncode) + "\n")
print("EXIT:", r.returncode)
print(r.stdout)
print("STDERR:", repr(r.stderr))
