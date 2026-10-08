import hashlib
import json
import subprocess
import sys
from pathlib import Path

evid = Path(sys.argv[1])
repo = Path("/tmp/opencode/jgas-dm004-impl-20261004T234416Z")


def git(*a):
    r = subprocess.run(
        ["git", "-C", str(repo), *a], capture_output=True, text=True,
        env={"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0",
             "GIT_ALLOW_PROTOCOL": "file", "PATH": "/usr/bin:/bin"})
    assert r.returncode == 0, (a, r.stderr)
    return r.stdout.strip()


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()


head = git("rev-parse", "HEAD")
tree = git("rev-parse", "HEAD^{tree}")
parent = git("rev-parse", "HEAD^")
files = {}
for rel in ("scripts/survey_agent_control_v2.py",
            "tests/test_survey_dm004_release_validate_state_v2.py"):
    blob = git("rev-parse", "HEAD:" + rel)
    mode = git("ls-tree", "HEAD", rel).split()[0]
    p = repo / rel
    files[rel] = {"mode": mode, "blob": blob, "sha256": sha(p),
                  "bytes": p.stat().st_size}
pack = evid / "dm004-e1705b7-to-6ffed32.pack"
man = {
    "head": head, "tree": tree, "parent": parent,
    "branch": "codex/dm004-release-validate-state",
    "files": files,
    "pack": {"path": pack.name, "bytes": pack.stat().st_size,
             "sha256": sha(pack),
             "objects": {"total": 18, "commits": 4, "trees": 9,
                         "blobs": 5}},
    "parents": {
        "b40_archive_sha256":
            "faf6792faf37ad30af2dbd7203b8896ca00964a91d00623a4f01278f2ade9f3c",
        "successor20_sha256":
            "2c2a8e6f2ab5fbd71b6cddfe5d875e4a821d09ef54ba9714eaab12e438e81a99",
        "w1_7_sha256":
            "97d384fe8f7216f110cd401d1279129da83fab2000f28c24a73abe0b177b0fd9"},
    "tests": {
        "new_module": "tests.test_survey_dm004_release_validate_state_v2",
        "new_methods": 6, "new_subcases": 10,
        "affected_modules": ["tests.test_survey_agent_control_v2",
                             "tests.test_survey_release_checkpoint_v2"],
        "affected_methods": 14},
}
(evid / "implementation-manifest.json").write_text(
    json.dumps(man, indent=2), encoding="utf-8")
print("manifest written", man["head"][:7], man["tree"][:7])
