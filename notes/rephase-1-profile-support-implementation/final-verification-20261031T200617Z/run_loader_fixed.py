#!/usr/bin/env /usr/bin/python3
"""Fixed loader binding runner: fail-closed Popen with exclusive raw files."""
import datetime
import os
import pathlib
import subprocess
import sys
import time

SNAP = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/profile-support-final-verify-20261031T200617Z/snapshot-fixed")
LOGDIR = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-profile-support-implementation/final-verification-20261031T200617Z/logs")
PROBE = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-profile-support-implementation/final-verification-20261031T200617Z/loader_probe.py")
PY = "/usr/bin/python3"

def main():
    out_p = LOGDIR / "loader-fixed-stdout.txt"
    err_p = LOGDIR / "loader-fixed-stderr.txt"
    meta_p = LOGDIR / "loader-fixed-meta.txt"
    cmd_p = LOGDIR / "loader-fixed-command.txt"
    env_p = LOGDIR / "loader-fixed-env.txt"
    pid_p = LOGDIR / "loader-fixed-pid.txt"
    exit_p = LOGDIR / "loader-fixed-exit.txt"
    argv = [PY, str(PROBE)]
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    with open(cmd_p, "xb") as f:
        f.write((" ".join(argv) + f"\ncwd={SNAP}\n").encode())
    with open(env_p, "xb") as f:
        git_keys = [k for k in env if k.startswith("GIT_")]
        f.write(f"PYTHONDONTWRITEBYTECODE=1\nPY={PY}\nGIT_keys_present={git_keys if git_keys else 'none'}\nPATH={env.get('PATH','')}\n".encode())
    start_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    start_t = time.time()
    out_f = open(out_p, "xb")
    err_f = open(err_p, "xb")
    try:
        proc = subprocess.Popen(argv, cwd=str(SNAP), env=env, stdout=out_f, stderr=err_f)
    except Exception as e:
        out_f.close()
        err_f.close()
        with open(meta_p, "xb") as f:
            f.write(f"wrapper_failure={e!r}\n".encode())
        with open(pid_p, "xb") as f:
            f.write(b"no-pid\n")
        with open(exit_p, "xb") as f:
            f.write(b"wrapper-failure\n")
        sys.exit(1)
    pid = proc.pid
    with open(pid_p, "xb") as f:
        f.write(f"{pid}\n".encode())
    try:
        rc = proc.wait(timeout=120)
        timed_out = False
    except subprocess.TimeoutExpired:
        try:
            proc.kill()
        except Exception:
            pass
        rc = proc.wait(timeout=30)
        timed_out = True
    end_t = time.time()
    end_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    out_f.close()
    err_f.close()
    with open(meta_p, "xb") as f:
        f.write((f"argv={' '.join(argv)}\npid={pid}\ncwd={SNAP}\nstart_utc={start_iso}\nend_utc={end_iso}\nduration_s={end_t-start_t:.3f}\ntimed_out={timed_out}\nreturncode={rc}\n").encode())
    with open(exit_p, "xb") as f:
        f.write(f"{rc}\n".encode())
    sys.exit(0 if rc == 0 else 1)

if __name__ == "__main__":
    main()
