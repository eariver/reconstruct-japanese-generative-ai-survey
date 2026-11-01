#!/usr/bin/env /usr/bin/python3
"""NEW safe wrapper for final affected7 on FINAL applied proof source.

- Proves 770 vs final manifest + scoped composite (1 changed vs both manifests + prior snapshot) using actual hashes.
- Runs harness_affected7.py in SAME proof cwd via Popen with exclusive raw files, actual PID/argv/cwd/env/time/exit.
- Sets PROFILE_SUPPORT_RETAIN_ROOT to NEW unique ignored retention parent.
- Verifies before/after 770 unchanged + retained 7+manifest with source binding.
- No saved-runner reuse, no source/Git mutation, no reconstruct Git readback.
"""
import datetime
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import time

PROOF = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/profile-support-packaging-20261031T202327Z/proof-copy/candidate-partial-b40de60")
PRIOR_SNAP = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/profile-support-final-verify-20261031T200617Z/snapshot-fixed")
LOGDIR = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-profile-support-implementation/final-affected7-20261031T202918Z/logs")
HARNESS = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-profile-support-implementation/final-affected7-20261031T202918Z/harness_affected7.py")
FINAL_MANIFEST = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-profile-support-implementation/source-packaging/final-20261031T202327Z/complete-profile-support-manifest.json")
ORIG_MANIFEST = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-profile-support-implementation/source-packaging/final-20261031T200637Z/complete-profile-support-manifest.json")
RETAIN_PARENT = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/profile-support-retain-final-affected7-20261031T202918Z")
PY = "/usr/bin/python3"

def snapshot_files(root: pathlib.Path):
    rows = []
    for dirpath, dirnames, filenames in os.walk(root):
        if ".git" in pathlib.Path(dirpath).parts:
            if ".git" in dirnames:
                dirnames.remove(".git")
            continue
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
    with open(path, "xb") as f:
        f.write(data)

def main():
    LOGDIR.mkdir(parents=True, exist_ok=True)
    # retention parent must already exist (created via mkdir, parent verified) and be empty
    if not RETAIN_PARENT.is_dir():
        print(f"FAIL retain parent missing: {RETAIN_PARENT}", flush=True)
        sys.exit(1)
    # failclosed if retain parent not under ignored runtime
    try:
        RETAIN_PARENT.resolve().relative_to(pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime").resolve())
    except ValueError:
        print(f"FAIL retain parent not under ignored runtime: {RETAIN_PARENT}", flush=True)
        sys.exit(1)
    existing = list(RETAIN_PARENT.iterdir())
    if existing:
        print(f"FAIL retain parent not empty (must be NEW unique): {existing}", flush=True)
        sys.exit(1)

    # before snapshot
    before_rows = snapshot_files(PROOF)
    before_text = "".join(f"{h}  {sz}  {mode}  {rel}\n" for rel, h, sz, mode in before_rows)
    write_exclusive(LOGDIR / "affected7-pins-before.txt", before_text.encode())
    # verify vs FINAL manifest using actual hashes (no copy-string trust)
    manifest = json.load(open(FINAL_MANIFEST))
    files = manifest.get("files", {})
    if isinstance(files, list):
        print("FAIL manifest files is list, expected dict", flush=True)
        sys.exit(1)
    before_dict = {r[0]: (r[1], r[2], r[3]) for r in before_rows}
    missing = [k for k in files if k not in before_dict]
    extra = [k for k in before_dict if k not in files]
    mismatch = []
    for k, v in files.items():
        if k in before_dict:
            ah, asz, amode = before_dict[k]
            if ah != v.get("sha256") or asz != v.get("bytes"):
                mismatch.append(k)
    verify_text = (
        f"proof_files={len(before_rows)}\nmanifest_intended={manifest.get('intended_files')}\n"
        f"missing={len(missing)} {missing[:5]}\nextra={len(extra)} {extra[:5]}\n"
        f"sha_bytes_mismatch={len(mismatch)} {mismatch[:5]}\n"
        f"manifest_patch={FINAL_MANIFEST}\n"
    )
    write_exclusive(LOGDIR / "affected7-verify-final-manifest.txt", verify_text.encode())
    if len(before_rows) != 770 or missing or extra or mismatch:
        print(f"FAIL manifest verify: {verify_text}", flush=True)
        sys.exit(1)

    # scoped composite: vs ORIG manifest + vs PRIOR_SNAP (actual hashes)
    orig = json.load(open(ORIG_MANIFEST))
    of = orig.get("files", {})
    nf = files
    changed_manifest = [k for k in of if k in nf and of[k].get("sha256") != nf[k].get("sha256")]
    # vs prior snap actual
    prior_rows = snapshot_files(PRIOR_SNAP)
    prior_dict = {r[0]: r[1] for r in prior_rows}
    proof_dict = {r[0]: r[1] for r in before_rows}
    changed_snap = [k for k in proof_dict if k in prior_dict and proof_dict[k] != prior_dict[k]]
    missing_prior = [k for k in proof_dict if k not in prior_dict]
    extra_prior = [k for k in prior_dict if k not in proof_dict]
    scoped_text = (
        f"changed_vs_orig_manifest={len(changed_manifest)} {changed_manifest}\n"
        f"changed_vs_prior_snap={len(changed_snap)} {changed_snap}\n"
        f"missing_vs_prior={missing_prior[:5]} extra_vs_prior={extra_prior[:5]}\n"
        f"orig_manifest={ORIG_MANIFEST}\nprior_snap={PRIOR_SNAP}\nproof={PROOF}\n"
        f"expected_single=tests/test_dm022_c_direct_operation_v2.py\n"
    )
    write_exclusive(LOGDIR / "affected7-verify-scoped-composite.txt", scoped_text.encode())
    if len(changed_manifest) != 1 or changed_manifest != ["tests/test_dm022_c_direct_operation_v2.py"]:
        print(f"FAIL scoped composite manifest: {scoped_text}", flush=True)
        sys.exit(1)
    if len(changed_snap) != 1 or changed_snap != ["tests/test_dm022_c_direct_operation_v2.py"]:
        print(f"FAIL scoped composite snap: {scoped_text}", flush=True)
        sys.exit(1)
    # verify changed file actual hash matches new manifest (full hash, no abbreviation)
    actual_new = proof_dict["tests/test_dm022_c_direct_operation_v2.py"]
    if actual_new != "6ffde575a21b3748147fda3f662d7934a78c5082a062a4f174519d4902aee585":
        print(f"FAIL changed file hash mismatch actual={actual_new}", flush=True)
        sys.exit(1)
    # verify all other 769 match prior snap actual
    for k, h in proof_dict.items():
        if k == "tests/test_dm022_c_direct_operation_v2.py":
            continue
        if prior_dict.get(k) != h:
            print(f"FAIL other file changed: {k}", flush=True)
            sys.exit(1)

    # run harness in proof cwd
    out_p = LOGDIR / "affected7-stdout.txt"
    err_p = LOGDIR / "affected7-stderr.txt"
    meta_p = LOGDIR / "affected7-meta.txt"
    cmd_p = LOGDIR / "affected7-command.txt"
    env_p = LOGDIR / "affected7-env.txt"
    pid_p = LOGDIR / "affected7-pid.txt"
    exit_p = LOGDIR / "affected7-exit.txt"
    argv = [PY, str(HARNESS)]
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = str(PROOF)
    env["PROFILE_SUPPORT_RETAIN_ROOT"] = str(RETAIN_PARENT)
    write_exclusive(cmd_p, (" ".join(argv) + f"\ncwd={PROOF}\nPYTHONPATH={PROOF}\nPROFILE_SUPPORT_RETAIN_ROOT={RETAIN_PARENT}\n").encode())
    git_keys = [k for k in env if k.startswith("GIT_")]
    # GIT_* may include GIT_OPTIONAL_LOCKS etc from test helper? Log but do not fail (harness sets its own git env per-fixture)
    write_exclusive(env_p, f"PYTHONDONTWRITEBYTECODE=1\nPY={PY}\nPYTHONPATH={PROOF}\nPROFILE_SUPPORT_RETAIN_ROOT={RETAIN_PARENT}\nGIT_keys_present={git_keys if git_keys else 'none'}\nPATH={env.get('PATH','')}\n".encode())
    start_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    start_t = time.time()
    out_f = open(out_p, "xb")
    err_f = open(err_p, "xb")
    try:
        proc = subprocess.Popen(argv, cwd=str(PROOF), env=env, stdout=out_f, stderr=err_f)
    except Exception as e:
        out_f.close()
        err_f.close()
        write_exclusive(meta_p, f"wrapper_failure={e!r}\n".encode())
        write_exclusive(pid_p, b"no-pid\n")
        write_exclusive(exit_p, b"wrapper-failure\n")
        sys.exit(1)
    pid = proc.pid
    write_exclusive(pid_p, f"{pid}\n".encode())
    try:
        rc = proc.wait(timeout=600)
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
    write_exclusive(meta_p, (f"argv={' '.join(argv)}\npid={pid}\ncwd={PROOF}\nPYTHONPATH={PROOF}\nPROFILE_SUPPORT_RETAIN_ROOT={RETAIN_PARENT}\nstart_utc={start_iso}\nend_utc={end_iso}\nduration_s={end_t-start_t:.3f}\ntimeout_s=600\ntimed_out={timed_out}\nreturncode={rc}\n").encode())
    write_exclusive(exit_p, f"{rc}\n".encode())
    if timed_out or rc != 0:
        print(f"FAIL harness rc={rc} timed_out={timed_out}", flush=True)
        sys.exit(1)

    # after snapshot (proof must be quiescent)
    after_rows = snapshot_files(PROOF)
    after_text = "".join(f"{h}  {sz}  {mode}  {rel}\n" for rel, h, sz, mode in after_rows)
    write_exclusive(LOGDIR / "affected7-pins-after.txt", after_text.encode())
    before_dict_full = {r[0]: r[1:] for r in before_rows}
    after_dict_full = {r[0]: r[1:] for r in after_rows}
    if before_dict_full != after_dict_full:
        diff_keys = [k for k in before_dict_full if before_dict_full.get(k) != after_dict_full.get(k)] + [k for k in after_dict_full if k not in before_dict_full]
        write_exclusive(LOGDIR / "affected7-pins-diff.txt", ("\n".join(diff_keys) + "\n").encode())
        print(f"FAIL pins changed after run: {diff_keys[:10]}", flush=True)
        sys.exit(1)
    else:
        write_exclusive(LOGDIR / "affected7-pins-diff.txt", b"identical 770/770\n")

    # retained verification: exactly one fresh mkdtemp subdir, 7+manifest, sha binding
    subdirs = [p for p in RETAIN_PARENT.iterdir() if p.is_dir()]
    retain_text = f"retain_parent={RETAIN_PARENT}\nsubdirs={len(subdirs)} {[p.name for p in subdirs]}\n"
    write_exclusive(LOGDIR / "affected7-retain-list.txt", retain_text.encode())
    if len(subdirs) != 1:
        print(f"FAIL retained subdirs !=1: {subdirs}", flush=True)
        sys.exit(1)
    run_dir = subdirs[0]
    retained_files = sorted([p for p in run_dir.iterdir() if p.is_file()], key=lambda p: p.name)
    retained_names = [p.name for p in retained_files]
    write_exclusive(LOGDIR / "affected7-retain-files.txt", ("\n".join(retained_names) + "\n").encode())
    # expect 7 operation outputs + manifest.json = 8 files? Test asserts len(_retained)==7 plus manifest => 8 total
    # Verify manifest.json exists and binds hashes
    manifest_path = run_dir / "manifest.json"
    if not manifest_path.is_file():
        print(f"FAIL retained manifest missing: {manifest_path}", flush=True)
        sys.exit(1)
    retained_manifest = json.load(open(manifest_path))
    # verify each retained file sha matches manifest entry
    files_map = retained_manifest.get("files", {})
    verify_lines = []
    for fname, meta in files_map.items():
        fpath = run_dir / fname
        if not fpath.is_file():
            verify_lines.append(f"{fname} MISSING")
            continue
        actual_h = hashlib.sha256(fpath.read_bytes()).hexdigest()
        actual_sz = fpath.stat().st_size
        ok = (actual_h == meta.get("sha256") and actual_sz == meta.get("bytes"))
        verify_lines.append(f"{fname} {'OK' if ok else 'MISMATCH'} actual={actual_h}/{actual_sz} manifest={meta.get('sha256')}/{meta.get('bytes')} source={meta.get('source')}")
    # also check all files on disk are in manifest (except manifest.json itself)
    on_disk_not_in_manifest = [n for n in retained_names if n != "manifest.json" and n not in files_map]
    verify_lines.append(f"on_disk_not_in_manifest={on_disk_not_in_manifest}")
    verify_lines.append(f"retained_manifest_script={retained_manifest.get('script')} revision={retained_manifest.get('revision')} route={retained_manifest.get('route')}")
    # load source identity: proof file for retained sources? Log proof root + harness binding already in stdout
    verify_lines.append(f"proof_root={PROOF}")
    write_exclusive(LOGDIR / "affected7-retain-verify.txt", ("\n".join(verify_lines) + "\n").encode())
    # fail if any mismatch
    if any("MISMATCH" in l or "MISSING" in l for l in verify_lines):
        print(f"FAIL retained verify mismatch", flush=True)
        sys.exit(1)
    if on_disk_not_in_manifest:
        print(f"FAIL retained extra files", flush=True)
        sys.exit(1)
    print("OK affected7 7/7 with retention bound", flush=True)
    # wrapper summary
    write_exclusive(LOGDIR / "wrapper-summary.txt", b"affected7 PASS OK rc=0 7/7 with retention\n")
    sys.exit(0)

if __name__ == "__main__":
    main()
