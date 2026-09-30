import subprocess, hashlib, json, os
DST = "/tmp/jgas-rephase-r1-assembly-20260929T143833Z"
R1 = "/tmp/jgas-rephase-mechanical-r1-20260928T000710Z"
E4 = "/tmp/jgas-rephase-gate-cli"
RECON = "/mnt/d/Git/reconstruct-japanese-generative-ai-survey"
def git(repo, args):
    return subprocess.run(["git", "-C", repo] + args, capture_output=True, text=True)

NEW = "481dec0c0233d7871df79a07a88aa5fe2291daa3"
print("=== new HEAD ls-tree seven ===")
with open(RECON + "/notes/rephase-1-mechanical-refresh/correction/final-b74db679f03908048db91420a8f262d412b8f58c/manifest-final.json") as f:
    mf = json.load(f)
ok = True
for e in mf["seven_paths"]:
    path = e["path"]
    exp_blob = e["blob"]
    r_new = git(DST, ["ls-tree", NEW, "--", path]).stdout.strip()
    r_b74 = git(R1, ["ls-tree", "b74db679f03908048db91420a8f262d412b8f58c", "--", path]).stdout.strip()
    match_new = exp_blob in r_new
    match_b74 = exp_blob in r_b74
    print(path, "NEW:", r_new, "match:", match_new, "B74:", r_b74)
    if not match_new:
        ok = False
print("SEVEN_IN_NEW_MATCH_B74:", ok)

print("=== new HEAD vs e4: diff name-status ===")
r = git(DST, ["diff", "e4c82692abee6acedbba07815b0d74ccefb80a7e", NEW, "--name-status"])
print(repr(r.stdout))
lines = sorted([l for l in r.stdout.strip().splitlines()])
print("sorted:", lines)
expected = sorted(["A\tdocs/weekly-mechanical-refresh.md","M\tscripts/survey_agent_control_v2.py","M\tscripts/survey_reader_surface_gate_v2.py","M\tscripts/survey_weekly_derivation_v2.py","A\tscripts/survey_weekly_mechanical_refresh_v2.py","M\ttests/test_survey_publication_revalidation_v2.py","A\ttests/test_survey_weekly_mechanical_refresh_v2.py"])
print("ONLY_SEVEN:", lines == expected)

print("=== unrelated entries: compare trees ===")
# List all files in e4 and new, compare mode/blob for non-seven
re = subprocess.run(["git", "-C", DST, "ls-tree", "-r", "e4c82692abee6acedbba07815b0d74ccefb80a7e"], capture_output=True, text=True).stdout.strip().splitlines()
rn = subprocess.run(["git", "-C", DST, "ls-tree", "-r", NEW], capture_output=True, text=True).stdout.strip().splitlines()
def parse(lines):
    d = {}
    for l in lines:
        # format: mode blob type path
        parts = l.split(None, 3)
        mode, btype, blob, path = parts[0], parts[1], parts[2], parts[3]
        d[path] = (mode, blob)
    return d
de = parse(re)
dn = parse(rn)
seven_set = set([e["path"] for e in mf["seven_paths"]])
print("e4 entries:", len(de), "new entries:", len(dn))
# new should be e4 + 3 added
print("new-e4 count diff:", len(dn) - len(de), "expected 3")
mismatch = []
for path, (mode_e, blob_e) in de.items():
    if path in seven_set:
        continue
    if path not in dn:
        mismatch.append((path, "missing in new"))
    elif dn[path] != (mode_e, blob_e):
        mismatch.append((path, de[path], dn[path]))
print("UNRELATED_MISMATCH_COUNT:", len(mismatch))
if mismatch:
    print(mismatch[:20])
else:
    print("UNRELATED_IDENTICAL: True")
# check added 3 are new
for p in ["scripts/survey_weekly_mechanical_refresh_v2.py","tests/test_survey_weekly_mechanical_refresh_v2.py","docs/weekly-mechanical-refresh.md"]:
    print(p, "in e4:", p in de, "in new:", dn.get(p))

print("=== log ===")
print(git(DST, ["log", "--oneline", "-5"]).stdout)
print(git(DST, ["log", "--format=%H %P %T", "-2"]).stdout)
print("=== status ===")
print(repr(git(DST, ["status", "--short", "--branch"]).stdout))
print("DONE_POST")
