#!/usr/bin/env /usr/bin/python3
"""Final meaningful affected verification wrapper (fail-closed, NEW unique run).

Quiescent source: .rephase-1-editorial-runtime/profile-support-final-verify-20261031T200617Z/snapshot-fixed
Logs: notes/rephase-1-profile-support-implementation/final-verification-20261031T200617Z/logs/
- Exclusive open (xb) for all raw files, no overwrites.
- subprocess.Popen with actual PID/argv/cwd/env/time/returncode.
- Before/after full intended-file hash/size/mode snapshots (770 files, excl .git, excl pyc).
- Module __file__ loader binding outside test semantics (no authority mocks).
- Sequential batches; stop on first failure (no broad doomed runs).
- Saves numeric exit even on timeout/wrapper failure; logs missing raw, never reconstructs terminal.
"""
import hashlib
import os
import pathlib
import subprocess
import sys
import time
import datetime

SNAP = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/profile-support-final-verify-20261031T200617Z/snapshot-fixed")
LOGDIR = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-profile-support-implementation/final-verification-20261031T200617Z/logs")
PY = "/usr/bin/python3"

BATCHES = [
    ("ordinary-newmodule-28", ["tests.test_profile_support_upstream_repair_v2", "-v"], 600),
    ("ordinary-affected-26", ["tests.test_survey_evidence_v2", "tests.test_run_evidence_v2_interactive", "tests.test_run_evidence_v2_agent_first", "tests.test_survey_evidence_source_class_regression", "-v"], 600),
    ("dm022-c-6", ["tests.test_dm022_c_direct_operation_v2", "-v"], 600),
    ("dm022-a2-25", ["tests.test_dm022_prearchitecture_acceptance_v2", "-v"], 600),
    ("dm022-affected-37", ["tests.test_dm022_c1_family_closure_v2", "tests.test_dm022_c1_h_presence_controls_v2", "tests.test_dm022_c1_research_graph_v2", "tests.test_dm022_prearch_b_ordinary_consumers_v2", "-v"], 600),
    ("consumer-selection-1", ["tests.test_dm022_full_lifecycle_v2.Dm022FullLifecycleWitnessTests.test_weekly_dm022_to_selection_stage", "-v"], 300),
    ("consumer-sevenslot-1", ["tests.test_dm022_full_lifecycle_v2.Dm022FullLifecycleWitnessTests.test_weekly_present_old_seven_slots_retain_clear_regenerate", "-v"], 300),
    ("consumer-draft-1", ["tests.test_dm022_full_lifecycle_v2.Dm022FullLifecycleWitnessTests.test_weekly_draft_synthesis_reader", "-v"], 300),
]

LOADER_MODULES = [
    "scripts.survey_screening_v2",
    "scripts.survey_evidence_v2",
    "scripts.run_evidence_v2_interactive",
    "scripts.run_evidence_v2_agent_first",
    "scripts.survey_research_authority_v2",
    "scripts.survey_prearchitecture_acceptance_v2",
    "tests.test_profile_support_upstream_repair_v2",
    "tests.test_survey_evidence_v2",
    "tests.test_dm022_c_direct_operation_v2",
    "tests.test_dm022_prearchitecture_acceptance_v2",
]

def snapshot_files(root: pathlib.Path):
    rows = []
    for dirpath, dirnames, filenames in os.walk(root):
        # exclude .git entirely
        if ".git" in pathlib.Path(dirpath).parts:
            # prune: do not descend into .git
            if ".git" in dirnames:
                dirnames.remove(".git")
            # skip files directly under .git path
            continue
        # prune __pycache__ (should be none, but exclude from intended)
        if "__pycache__" in dirnames:
            dirnames.remove("__pycache__")
        for fn in sorted(filenames):
            if fn.endswith(".pyc"):
                continue
            full = pathlib.Path(dirpath) / fn
            rel = full.relative_to(root).as_posix()
            st = full.stat()
            h = hashlib.sha256(full.read_bytes()).hexdigest()
            rows.append((rel, h, st.st_size, oct(st.st_mode & 0o777)))
    rows.sort()
    return rows

def write_exclusive(path: pathlib.Path, data: bytes):
    # fail-closed: exclusive create, no overwrite
    with open(path, "xb") as f:
        f.write(data)

def run_one_batch(name, ut_args, timeout_s):
    stdout_p = LOGDIR / f"{name}-stdout.txt"
    stderr_p = LOGDIR / f"{name}-stderr.txt"
    meta_p = LOGDIR / f"{name}-meta.txt"
    cmd_p = LOGDIR / f"{name}-command.txt"
    env_p = LOGDIR / f"{name}-env.txt"
    pid_p = LOGDIR / f"{name}-pid.txt"
    exit_p = LOGDIR / f"{name}-exit.txt"
    before_p = LOGDIR / f"{name}-pins-before.txt"
    after_p = LOGDIR / f"{name}-pins-after.txt"
    loader_out_p = LOGDIR / f"{name}-loader-stdout.txt"
    loader_err_p = LOGDIR / f"{name}-loader-stderr.txt"
    loader_meta_p = LOGDIR / f"{name}-loader-meta.txt"
    loader_exit_p = LOGDIR / f"{name}-loader-exit.txt"

    # before snapshot (in-memory, then exclusive write)
    before_rows = snapshot_files(SNAP)
    before_text = "".join(f"{h}  {sz}  {mode}  {rel}\n" for rel, h, sz, mode in before_rows)
    write_exclusive(before_p, before_text.encode())

    argv = [PY, "-m", "unittest"] + ut_args
    # env: inherit + force PYTHONDONTWRITEBYTECODE=1
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    # record command/env without secrets (no secrets in this env)
    write_exclusive(cmd_p, (" ".join(argv) + f"\ncwd={SNAP}\n").encode())
    env_text = f"PYTHONDONTWRITEBYTECODE={env.get('PYTHONDONTWRITEBYTECODE')}\nPY={PY}\n"
    try:
        import platform
        env_text += f"python={platform.python_version()} {sys.version}\n"
    except Exception:
        pass
    # log full env keys (sorted) excluding potential secrets? No secrets here; log all non-GIT plus GIT check
    git_keys = [k for k in env if k.startswith("GIT_")]
    env_text += f"GIT_keys_present={git_keys if git_keys else 'none'}\n"
    env_text += f"PATH={env.get('PATH','')}\n"
    write_exclusive(env_p, env_text.encode())

    start_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    start_t = time.time()
    # exclusive open stdout/stderr for child
    out_f = open(stdout_p, "xb")
    err_f = open(stderr_p, "xb")
    try:
        proc = subprocess.Popen(argv, cwd=str(SNAP), env=env, stdout=out_f, stderr=err_f)
    except Exception as e:
        out_f.close()
        err_f.close()
        write_exclusive(meta_p, f"name={name}\nargv={' '.join(argv)}\ncwd={SNAP}\nstart={start_iso}\nwrapper_failure={e!r}\n".encode())
        write_exclusive(pid_p, b"no-pid-wrapper-failure\n")
        write_exclusive(exit_p, b"wrapper-failure-no-numeric\n")
        return False, f"wrapper failure {e!r}"
    pid = proc.pid
    write_exclusive(pid_p, f"{pid}\n".encode())
    # poll original live PID (wait on proc, not duplicate)
    try:
        rc = proc.wait(timeout=timeout_s)
        timed_out = False
    except subprocess.TimeoutExpired:
        # fail-closed: kill, preserve numeric marker
        try:
            proc.kill()
        except Exception:
            pass
        try:
            rc = proc.wait(timeout=30)
        except Exception:
            rc = 124
        timed_out = True
    end_t = time.time()
    end_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    out_f.close()
    err_f.close()
    # meta with actual PID/argv/cwd/env/time/returncode
    meta_text = (
        f"name={name}\nargv={' '.join(argv)}\n"
        f"pid={pid}\ncwd={SNAP}\n"
        f"start_utc={start_iso}\nend_utc={end_iso}\nduration_s={end_t-start_t:.3f}\n"
        f"timeout_s={timeout_s}\ntimed_out={timed_out}\nreturncode={rc}\n"
        f"python={PY}\nPYTHONDONTWRITEBYTECODE=1\n"
    )
    write_exclusive(meta_p, meta_text.encode())
    write_exclusive(exit_p, f"{rc}\n".encode())

    # loader binding outside test semantics (no mocks): import and log __file__/sha/size/mode
    loader_code = (
        "import importlib, hashlib, pathlib;"
        "mods=" + repr(LOADER_MODULES) + ";"
        "import sys;"
        "print('LOADER_CWD=' + __import__('os').getcwd());"
        "print('LOADER_SYS_VERSION=' + sys.version.replace(chr(10),' '));"
        "import jsonschema,pypdf;"
        "print('jsonschema-present');"
        "print('pypdf-present');"
        "outs=[];"
        "import traceback;"
        "for m in mods:"
        " try:"
        "  mod=importlib.import_module(m);"
        "  p=pathlib.Path(mod.__file__).resolve();"
        "  b=p.read_bytes();"
        "  h=hashlib.sha256(b).hexdigest();"
        "  st=p.stat();"
        "  print(f\"{m} __file__={p} sha256={h} bytes={len(b)} mode={oct(st.st_mode & 0o777)}\");"
        " except Exception as e:"
        "  print(f\"{m} LOAD_FAIL {e!r}\");"
        "  traceback.print_exc();"
    )
    loader_argv = [PY, "-c", loader_code]
    l_start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    l_start_t = time.time()
    try:
        with open(loader_out_p, "xb") as lo, open(loader_err_p, "xb") as le:
            lproc = subprocess.Popen(loader_argv, cwd=str(SNAP), env=env, stdout=lo, stderr=le)
            lpid = lproc.pid
            try:
                lrc = lproc.wait(timeout=120)
                l_timed_out = False
            except subprocess.TimeoutExpired:
                try:
                    lproc.kill()
                except Exception:
                    pass
                lrc = lproc.wait(timeout=30)
                l_timed_out = True
        l_end_t = time.time()
        l_end = datetime.datetime.now(datetime.timezone.utc).isoformat()
        write_exclusive(loader_meta_p, (
            f"name={name}-loader\nargv={PY} -c <loader_code>\npid={lpid}\ncwd={SNAP}\n"
            f"start_utc={l_start}\nend_utc={l_end}\nduration_s={l_end_t-l_start_t:.3f}\n"
            f"timed_out={l_timed_out}\nreturncode={lrc}\n"
        ).encode())
        write_exclusive(loader_exit_p, f"{lrc}\n".encode())
    except Exception as e:
        # log loader failure but do not mask test result; still record
        try:
            write_exclusive(loader_meta_p, f"loader_wrapper_failure={e!r}\n".encode())
        except Exception:
            pass
        try:
            write_exclusive(loader_exit_p, b"loader-wrapper-failure\n")
        except Exception:
            pass

    # after snapshot + diff
    after_rows = snapshot_files(SNAP)
    after_text = "".join(f"{h}  {sz}  {mode}  {rel}\n" for rel, h, sz, mode in after_rows)
    write_exclusive(after_p, after_text.encode())

    # compare
    before_dict = {r[0]: r[1:] for r in before_rows}
    after_dict = {r[0]: r[1:] for r in after_rows}
    if before_dict != after_dict:
        # do not invent PASS; report diff as failure signal (source must be quiescent)
        return False, f"pins changed before/after for {name}"
    if timed_out:
        return False, f"TIMEOUT {name} rc={rc}"
    if rc != 0:
        return False, f"non-zero exit {name} rc={rc}"
    return True, f"OK {name} rc=0"

def main():
    LOGDIR.mkdir(parents=True, exist_ok=True)
    # fail-fast if logdir not empty for our batch names (no overwrites already enforced via xb)
    results = []
    for name, args, to in BATCHES:
        ok, msg = run_one_batch(name, args, to)
        print(f"{name}: {msg}", flush=True)
        results.append((name, ok, msg))
        if not ok:
            # STOP dependent batches on common positive setup failure / any failure
            print(f"STOPPING further batches due to failure in {name}: {msg}", flush=True)
            break
    # summary file (wrapper's own summary, NOT test stdout; tests' raw are in per-batch stdout/stderr)
    summary_p = LOGDIR / "wrapper-summary.txt"
    lines = []
    for n, ok, m in results:
        lines.append(f"{n} {'PASS' if ok else 'FAIL'} {m}")
    # exclusive summary (new file)
    try:
        with open(summary_p, "xb") as f:
            f.write(("\n".join(lines) + "\n").encode())
    except FileExistsError:
        pass
    # exit non-zero if any fail
    sys.exit(0 if all(ok for _, ok, _ in results) else 1)

if __name__ == "__main__":
    main()
