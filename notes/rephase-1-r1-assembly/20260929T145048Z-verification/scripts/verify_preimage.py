import subprocess, os, hashlib, json

E4 = "/tmp/jgas-rephase-gate-cli"
DST = "/tmp/jgas-rephase-r1-assembly-20260929T143833Z"
R1 = "/tmp/jgas-rephase-mechanical-r1-20260928T000710Z"
RECON = "/mnt/d/Git/reconstruct-japanese-generative-ai-survey"

def git(repo, args):
    r = subprocess.run(["git", "-C", repo] + args, capture_output=True, text=True)
    return r

# Expected e4 blobs from 03-return-evidence-clarification.md (4 existing)
expected_e4 = {
    "scripts/survey_agent_control_v2.py": "2940abe3cd4049769983d53ca0be269087b15977",
    "scripts/survey_reader_surface_gate_v2.py": "ea1eb652ab49eb479e17318712d84c318bfaf475",
    "scripts/survey_weekly_derivation_v2.py": "477de21e9565e7a15044bd0e5d1ae6e555394524",
    "tests/test_survey_publication_revalidation_v2.py": "01f9ce6b7561e59ac25fbb801dd27162667d30e7",
}
added = [
    "scripts/survey_weekly_mechanical_refresh_v2.py",
    "tests/test_survey_weekly_mechanical_refresh_v2.py",
    "docs/weekly-mechanical-refresh.md",
]

print("=== e4 ls-tree blobs ===")
for path, exp in expected_e4.items():
    r = git(E4, ["ls-tree", "e4c82692abee6acedbba07815b0d74ccefb80a7e", "--", path])
    print(path, "->", r.stdout.strip(), "stderr:", r.stderr.strip(), "exit:", r.returncode)
    print("  expected blob:", exp, "match:", exp in r.stdout)

print("=== e4 added absence ===")
for path in added:
    r = git(E4, ["ls-tree", "e4c82692abee6acedbba07815b0d74ccefb80a7e", "--", path])
    print(path, "stdout empty (absent):", r.stdout.strip() == "", "out:", repr(r.stdout.strip()))
    r2 = git(E4, ["ls-files", "-s", "--", path])
    print("  ls-files empty:", r2.stdout.strip() == "")

print("=== a1 blobs (via R1 db) ===")
for path, exp in expected_e4.items():
    r = git(R1, ["ls-tree", "a1a4242adaddc42427b68c18ae367c04d6cd63b4", "--", path])
    print(path, "->", r.stdout.strip(), "match e4:", exp in r.stdout)

print("=== DST pre-patch ls-files ===")
for path in list(expected_e4.keys()) + added:
    r = git(DST, ["ls-files", "-s", "--", path])
    print(path, "->", r.stdout.strip() or "(absent)")

print("=== DST worktree modes ===")
for path in list(expected_e4.keys()):
    fp = os.path.join(DST, path)
    print(path, oct(os.lstat(fp).st_mode & 0o777))

print("=== b74 final blobs ===")
with open(RECON + "/notes/rephase-1-mechanical-refresh/correction/final-b74db679f03908048db91420a8f262d412b8f58c/manifest-final.json") as f:
    mf = json.load(f)
for e in mf["seven_paths"]:
    path = e["path"]
    exp_blob = e["blob"]
    r = git(R1, ["ls-tree", "b74db679f03908048db91420a8f262d412b8f58c", "--", path])
    print(path, "manifest blob:", exp_blob, "ls-tree:", r.stdout.strip(), "match:", exp_blob in r.stdout)

print("=== patch hash ===")
with open(RECON + "/notes/rephase-1-mechanical-refresh/correction/final-b74db679f03908048db91420a8f262d412b8f58c/patch-final-a1-b74db67.patch", "rb") as f:
    h = hashlib.sha256(f.read()).hexdigest()
print("patch sha256:", h, "expected 7817fa4fc027ae0bac9bbd7e7bbd18c588ba3373b52e17730eafebe2b92aab01 match:", h == "7817fa4fc027ae0bac9bbd7e7bbd18c588ba3373b52e17730eafebe2b92aab01")

print("=== patch file list ===")
r = subprocess.run(["git", "apply", "--numstat", RECON + "/notes/rephase-1-mechanical-refresh/correction/final-b74db679f03908048db91420a8f262d412b8f58c/patch-final-a1-b74db67.patch"], capture_output=True, text=True, cwd="/tmp")
print("numstat stdout:", r.stdout[:2000])
print("numstat stderr:", r.stderr[:2000])
print("numstat exit:", r.returncode)
