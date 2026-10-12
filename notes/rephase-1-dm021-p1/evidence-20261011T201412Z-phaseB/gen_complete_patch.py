#!/usr/bin/env python3
"""Generate + verify the complete 13-path P1 overlay patch (read-only to repo).

Base: restored actual409 worktree (HEAD409b292/tree8ce36998) + LF2I overlay.
Output: complete-p1-overlay-13path.patch with base-identity header, 3 modified
paths via `git diff HEAD`, 10 new paths via unified diffs vs /dev/null.
Verification: every new-file hunk reconstructs byte-identical content;
modified hunks match `git diff HEAD` output; diff count is exactly 13.
"""
from __future__ import annotations

import difflib
import hashlib
import subprocess
import sys
from pathlib import Path

REPO = Path("/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z/candidate-partial-b40de60")
EVID = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey"
            "/notes/rephase-1-dm021-p1/evidence-20261011T201412Z-phaseB")
MODIFIED = [
    "schemas/reader-surface-gate-v2.schema.json",
    "schemas/reader-surface-semantic-review-v2.schema.json",
    "scripts/survey_reader_surface_gate_v2.py",
]
NEW = [
    "schemas/editorial-correction-proposal-v2.schema.json",
    "schemas/longform-publication-source-manifest-v2.schema.json",
    "schemas/longform-reader-input-v2.schema.json",
    "scripts/survey_editorial_correction_proposal_v2.py",
    "scripts/survey_longform_derivation_v2.py",
    "scripts/survey_longform_generated_v2.py",
    "scripts/survey_longform_semantic_publication_v2.py",
    "tests/test_survey_editorial_correction_proposal_v2.py",
    "tests/test_survey_longform_derivation_v2.py",
    "tests/test_survey_longform_publication_integration_v2.py",
]
OUT = EVID / "complete-p1-overlay-13path.patch"


def main() -> int:
    for name in ("complete-p1-overlay-13path.patch", "complete-p1-overlay-13path.sha256"):
        if (EVID / name).exists():
            print(f"REFUSAL: output exists: {name}")
            return 40
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                          capture_output=True, text=True).stdout.strip()
    tree = subprocess.run(["git", "rev-parse", "HEAD^{tree}"], cwd=REPO,
                          capture_output=True, text=True).stdout.strip()
    status = subprocess.run(["git", "status", "--porcelain"], cwd=REPO,
                            capture_output=True, text=True).stdout
    assert head == "409b292756dd1277b9dfae87679934c0d2ce251c", head
    assert tree == "8ce3699861505f32d1d60bdc185d4d4f635aedb2", tree
    parts = [f"DM021-P1 complete overlay: 3M10A relative actual409",
             f"base HEAD {head}", f"base tree {tree}", ""]
    for rel in MODIFIED:
        proc = subprocess.run(["git", "diff", "HEAD", "--", rel], cwd=REPO,
                              capture_output=True, text=True)
        assert proc.returncode == 0 and proc.stdout, rel
        parts.append(proc.stdout.rstrip("\n"))
    reconstructed: dict[str, bytes] = {}
    for rel in NEW:
        data = (REPO / rel).read_bytes()
        text = data.decode("utf-8")
        diff = "".join(difflib.unified_diff(
            [], text.splitlines(keepends=True),
            fromfile="dev/null", tofile="b/" + rel))
        header = (f"diff --git a/{rel} b/{rel}\nnew file mode 100644\n"
                  f"index 0000000..{hashlib.sha256(data).hexdigest()[:7]} 100644\n")
        parts.append(header + "".join(
            ("--- a/dev/null\n+++ b/" + rel + "\n" + diff.split("+++ b/" + rel + "\n", 1)[1])
            if "+++ b/" + rel in diff else diff))
        reconstructed[rel] = data
    body = "\n".join(parts) + "\n"
    assert body.count("diff --git ") == 13, body.count("diff --git ")
    OUT.write_text(body, encoding="utf-8")
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
    (EVID / "complete-p1-overlay-13path.sha256").write_text(
        f"{digest}  complete-p1-overlay-13path.patch\n", encoding="utf-8")
    # Verify: reparse patch, rebuild each new file, compare bytes.
    current: str | None = None
    plus: list[str] = []
    rebuilt: dict[str, str] = {}
    for line in body.splitlines(keepends=True):
        if line.startswith("diff --git "):
            if current is not None and current in reconstructed:
                rebuilt[current] = "".join(plus)
            current = line.split(" b/", 1)[1].strip()
            plus = []
        elif current in reconstructed and line.startswith("+") and not line.startswith("+++"):
            plus.append(line[1:])
    if current is not None and current in reconstructed:
        rebuilt[current] = "".join(plus)
    assert set(rebuilt) == set(reconstructed), (set(rebuilt) ^ set(reconstructed))
    for rel, data in reconstructed.items():
        assert rebuilt[rel] == data.decode("utf-8"), f"reconstruction mismatch: {rel}"
    print(f"PATCH_OK paths=13 sha256={digest} bytes={len(body.encode())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
