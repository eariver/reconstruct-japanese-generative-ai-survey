#!/usr/bin/env python3
"""Generate final complete 16-path patch v3 WITHOUT touching active index.

Byte-copies active P2R candidate to a NEW disposable dir, does transient
`git add -N` + `git diff HEAD` THERE (disposable index only), saves patch +
sha256 manifest to the correction2 packet, verifies active untouched
(HEAD/tree/status/index/pins recorded). No add-N/reset in active. V3 pins:
module 3833b14a / test 4155baab / schema 347e5499; inherited13 unchanged.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ACTIVE = Path("/tmp/opencode/jgas-dm021p2r-impl-20261013T123807Z/candidate-partial-b40de60")
EVID = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey"
            "/notes/rephase-1-dm021-p2r/evidence-20261014T000000Z-correction2")
GENROOT = Path("/tmp/opencode/jgas-dm021p2r-gen-20261014T000003Z")
GENREPO = GENROOT / "candidate-partial-b40de60"
OUT = EVID / "complete-p2r-16path-v3.patch"
OUTHASH = EVID / "complete-p2r-16path-v3.sha256"
OUT_STDOUT = EVID / "gen_16patch_v3.stdout.txt"
OUT_STDERR = EVID / "gen_16patch_v3.stderr.txt"
OUT_EXIT = EVID / "gen_16patch_v3.exit"
EXPECTED = json.load(open(EVID / "expected16-correction2c.json"))
FIXED_HEAD = "409b292756dd1277b9dfae87679934c0d2ce251c"
FIXED_TREE = "8ce3699861505f32d1d60bdc185d4d4f635aedb2"
MODIFIED = [
    "schemas/reader-surface-gate-v2.schema.json",
    "schemas/reader-surface-semantic-review-v2.schema.json",
    "scripts/survey_reader_surface_gate_v2.py",
]
NEW = [
    "schemas/editorial-correction-proposal-v2.schema.json",
    "schemas/editorial-retention-manifest-v2.schema.json",
    "schemas/longform-publication-source-manifest-v2.schema.json",
    "schemas/longform-reader-input-v2.schema.json",
    "scripts/survey_editorial_correction_proposal_v2.py",
    "scripts/survey_editorial_retention_v2.py",
    "scripts/survey_longform_derivation_v2.py",
    "scripts/survey_longform_generated_v2.py",
    "scripts/survey_longform_semantic_publication_v2.py",
    "tests/test_survey_editorial_correction_proposal_v2.py",
    "tests/test_survey_editorial_retention_v2.py",
    "tests/test_survey_longform_derivation_v2.py",
    "tests/test_survey_longform_publication_integration_v2.py",
]


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file"})
    return subprocess.run(["git", "-c", f"safe.directory={str(repo.resolve())}", *args],
                          cwd=repo, capture_output=True, text=True, env=env)


def main() -> int:
    for p in (OUT, OUTHASH, OUT_STDOUT, OUT_STDERR, OUT_EXIT):
        if p.exists():
            print(f"REFUSAL: output exists: {p.name}")
            return 40
    if GENROOT.exists():
        print(f"REFUSAL: gen destination exists: {GENROOT}")
        return 40
    log: list[str] = []

    def emit(code: int) -> int:
        with open(OUT_STDOUT, "xb") as f:
            f.write(("\n".join(log) + "\n").encode())
        with open(OUT_STDERR, "xb") as f:
            f.write(b"")
        with open(OUT_EXIT, "xb") as f:
            f.write(f"{code}\n".encode())
        return code

    head = git(ACTIVE, "rev-parse", "HEAD").stdout.strip()
    tree = git(ACTIVE, "rev-parse", "HEAD^{tree}").stdout.strip()
    if head != FIXED_HEAD or tree != FIXED_TREE:
        print(f"REFUSAL: active HEAD/tree moved: {head}/{tree}")
        return 40
    status = git(ACTIVE, "status", "--porcelain=v1", "-uall").stdout
    for m in MODIFIED:
        if f" M {m}" not in status:
            print(f"REFUSAL: modified missing in status: {m}")
            return 40
    for n in NEW:
        if f"?? {n}" not in status:
            print(f"REFUSAL: new missing in status: {n}")
            return 40
    for rel, exp in EXPECTED.items():
        data = (ACTIVE / rel).read_bytes()
        got = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
               "mode": oct((ACTIVE / rel).stat().st_mode & 0o777)}
        if got != exp:
            print(f"REFUSAL: active pin mismatch vs correction2c: {rel}: got={got} exp={exp}")
            return 40
    log.append(f"active pins match correction2c; HEAD={head} tree={tree}")
    GENROOT.mkdir(parents=True)
    proc = subprocess.run(["cp", "-a", "--reflink=never", str(ACTIVE), str(GENREPO)],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"REFUSAL: byte-copy failed: {proc.stderr[:1000]}")
        return 40
    r = git(GENREPO, "add", "-N", "--", *NEW)
    if r.returncode != 0:
        print(f"REFUSAL: disposable add-N failed: {r.stderr[:1000]}")
        return 40
    r = git(GENREPO, "diff", "HEAD", "--")
    if r.returncode != 0:
        print(f"REFUSAL: disposable diff failed: {r.stderr[:1000]}")
        return 40
    OUT.write_bytes(r.stdout.encode("utf-8"))
    sha = hashlib.sha256(r.stdout.encode("utf-8")).hexdigest()
    OUTHASH.write_text(sha + "\n")
    log.append(f"wrote {OUT.name} {OUT.stat().st_size}B sha256={sha}")
    log.append(f"generated_utc={datetime.now(timezone.utc).isoformat()}")
    r2 = git(ACTIVE, "diff", "--cached", "--name-only")
    if r2.stdout.strip() != "":
        print(f"REFUSAL: active index mutated: {r2.stdout[:500]}")
        return 40
    log.append("active index verified empty (no add-N in active)")
    return emit(0)


if __name__ == "__main__":
    sys.exit(main())
