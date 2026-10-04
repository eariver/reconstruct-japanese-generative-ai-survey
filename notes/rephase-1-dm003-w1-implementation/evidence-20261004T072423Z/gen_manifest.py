#!/usr/bin/env python3
"""Machine-generated DM003-W1 implementation/restore manifest (no manual transcription)."""
import hashlib
import json
import subprocess
from pathlib import Path

EVID = Path("/tmp/opencode/jgas-dm003w1-evidence-20261004T072423Z")
IMPL = Path("/tmp/opencode/jgas-dm003w1-impl-20261004T072423Z")
RESTORE = Path("/tmp/opencode/jgas-dm003w1-restore-20261004T073938Z/candidate-partial-b40de60")
RECON = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
ENV = {"GIT_NO_LAZY_FETCH": "1", "GIT_ALLOW_PROTOCOL": "file",
       "GIT_OPTIONAL_LOCKS": "0", "PYTHONDONTWRITEBYTECODE": "1"}


def git(args, cwd):
    import os
    env = dict(os.environ)
    env.update(ENV)
    return subprocess.run(["git"] + args, cwd=str(cwd), capture_output=True,
                          text=True, env=env, timeout=120)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def tail_summary(logpath):
    lines = Path(logpath).read_text().splitlines()
    ran = next((l for l in lines if l.startswith("Ran ")), "")
    status = "OK" if any(l.strip() == "OK" for l in lines) else (
        "FAILED" if any("FAILED" in l for l in lines) else "UNKNOWN")
    return {"log": Path(logpath).name, "sha256": sha256(logpath),
            "ran": ran, "status": status}


impl_head = git(["rev-parse", "HEAD"], IMPL).stdout.strip()
manifest = {
    "unit": "DM003-W1 narrow repair implementation",
    "parent": {"head": "222a37e9ee2aa96724a491f2c04c2583a86b9650",
               "tree": "dbabeed5e70d79b51abb09b64666ca9e1d0fd5dd",
               "parent": "ff6c67f68e12b3093901248219f2de2872e54d73"},
    "final": {
        "head": impl_head,
        "tree": git(["rev-parse", "HEAD^{tree}"], IMPL).stdout.strip(),
        "parent": git(["log", "--format=%P", "-1", "HEAD"], IMPL).stdout.strip(),
        "branch": "codex/dm003w1-preview-agreement",
        "clean": git(["status", "--porcelain=v1",
                      "--untracked-files=all"], IMPL).stdout.strip() == "",
    },
    "source_hashes": {
        "scripts/survey_agent_control_v2.py": sha256(IMPL / "scripts/survey_agent_control_v2.py"),
        "scripts/survey_profiled_freeze_v2.py": sha256(IMPL / "scripts/survey_profiled_freeze_v2.py"),
        "scripts/survey_stage_validation_v2.py": sha256(IMPL / "scripts/survey_stage_validation_v2.py"),
        "tests/test_survey_dm003_w1_preview_agreement_v2.py":
            sha256(IMPL / "tests/test_survey_dm003_w1_preview_agreement_v2.py"),
        "tests/test_survey_dm001_019_freeze_equivalence_v2.py":
            sha256(IMPL / "tests/test_survey_dm001_019_freeze_equivalence_v2.py"),
    },
    "diff_stat": git(["diff", "--stat", "222a37e9ee2aa96724a491f2c04c2583a86b9650",
                      impl_head], IMPL).stdout.strip(),
    "new_pack": {
        "path": "w1-222-to-e1705b7.pack",
        "sha256": sha256(EVID / "w1-222-to-e1705b7.pack"),
        "bytes": (EVID / "w1-222-to-e1705b7.pack").stat().st_size,
        "objects": git(["verify-pack", "-v", str(EVID / "w1-222-to-e1705b7.idx")],
                       IMPL).stdout.strip().splitlines(),
    },
    "old_inputs": {
        "b40_partial_tar_sha256": sha256(RECON / "notes/rephase-1-candidate-recovery/m3-20261003T0445Z/candidate-partial-b40de60.tar.gz"),
        "successor_20pack_sha256": sha256(RECON / "notes/rephase-1-dm001-019-implementation/evidence-final-20261003T145621Z/20-packaging/successor-pack.pack"),
    },
    "test_runs": [
        tail_summary(EVID / "run-02-newmod-full.log"),
        tail_summary(EVID / "run-03-affected-16.log"),
        tail_summary(EVID / "run-04-dm001-selected.log"),
        tail_summary(EVID / "run-05-w4-oracle-retry.log"),
        tail_summary(EVID / "run-06-final-newmod.log"),
        tail_summary(EVID / "run-07-final-affected-16.log"),
        tail_summary(EVID / "run-08-final-dm001-selected.log"),
    ],
    "restore": {
        "dir": str(RESTORE),
        "head": git(["rev-parse", "HEAD"], RESTORE).stdout.strip(),
        "tree": git(["rev-parse", "HEAD^{tree}"], RESTORE).stdout.strip(),
        "branch": "dm003w1-final",
        "clean": git(["status", "--porcelain=v1",
                      "--untracked-files=all"], RESTORE).stdout.strip() == "",
        "shallow": (RESTORE / ".git/shallow").read_text().strip(),
        "remotes": git(["remote", "-v"], RESTORE).stdout.strip(),
        "chain": git(["rev-list", "--format=%H %P", impl_head], RESTORE).stdout.strip().splitlines(),
    },
    "runtime": "/tmp/opencode/candidate-recovery-tooling-20261003T0435Z/venv/bin/python (3.12.14)",
    "limits": [
        "Single synthetic Special/Weekly scope per fixture; no all-profile/real-publication claim.",
        "Per-module HEAD/tree/source guards (not per-test); fixture no-write proofs are regular-file inventories under the two owned roots, not whole-filesystem attestation.",
        "26309 missing historical blobs inherited (partial DB); unbundled pinned runtime; no full-history claim.",
        "No full 56/R1/Weekly suite rerun; old PASS not transferred.",
    ],
}
(EVID / "implementation-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print("manifest bytes:", (EVID / "implementation-manifest.json").stat().st_size)
print("final head:", manifest["final"]["head"], "clean:", manifest["final"]["clean"])
print("restore head:", manifest["restore"]["head"], "clean:", manifest["restore"]["clean"])
