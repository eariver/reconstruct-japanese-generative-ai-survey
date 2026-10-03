"""Milestone-3 five-method runner — literal argv, guards, allow-listed env.

Executed ONCE per Astra verification-decision. Each unittest method runs as its
own subprocess with a literal argv list; per-method stdout/stderr/exit saved to
unique raw paths. Guards abort when HEAD/tree/parent or tracked bytes change.

Runner source is itself evidence; it performs no source mutation and no
feature/test edits.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

# ---- literal pins (embedded, verified before/after) ----
FIXTURE = Path("/tmp/opencode/jgas-rephase-candidate-recovery-20261003T0435Z")
EXP_HEAD = "b40de600e9ed1f80cb278213ccf17aa5f3cd9de3"
EXP_TREE = "657032438c6ed8b1c055d5a120b67b4b261a5092"
EXP_PARENT = "774dd39a951c9ac3818e83dfffd4c7666efb0a20"
VENV_PY = Path("/tmp/opencode/candidate-recovery-tooling-20261003T0435Z/venv/bin/python")

METHODS = [
    ("t1-profiled-identity",
     ["tests.test_survey_profiled_freeze_v2.SurveyProfiledFreezeV2Tests"
      ".test_thematic_and_weekly_public_identity_remain_natural"]),
    ("t2-stage-positive",
     ["tests.test_survey_freeze_stage_boundary_v2.FreezeStageBoundaryV2Tests"
      ".test_weekly_approved_preview_advances_through_real_freeze_boundary"]),
    ("t3-stage-negatives",
     ["tests.test_survey_freeze_stage_boundary_v2.FreezeStageBoundaryV2Tests"
      ".test_freeze_artifact_set_rejects_missing_extra_and_wrong_visual"]),
    ("t4-gate-cli",
     ["tests.test_survey_gate_cli_persisted_review_v2.GateCliPersistedReviewV2Tests"
      ".test_direct_primary_cli_admission_absolute_relative_and_cwd"]),
    ("t5-publication-chain",
     ["tests.test_survey_publication_v2.SurveyPublicationV2Tests"
      ".test_exact_reviewed_pdf_chain_reaches_release_without_postapproval_quality_gate"]),
]

# Git-root/object overrides that must never be inherited by test processes.
SCRUB = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
         "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR", "GIT_NAMESPACE",
         "GIT_CEILING_DIRECTORIES", "GIT_DISCOVERY_ACROSS_FILESYSTEM")
ALLOW = ("GIT_NO_LAZY_FETCH", "GIT_ALLOW_PROTOCOL", "PYTHONDONTWRITEBYTECODE")


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(FIXTURE), *args],
                          capture_output=True, text=True, check=False)


def identity() -> dict[str, str]:
    head = git("rev-parse", "HEAD")
    tree = git("rev-parse", "HEAD^{tree}")
    parent = git("log", "--format=%P", "-1")
    status = git("status", "--porcelain")
    diff = git("diff", "--quiet", "HEAD")
    assert head.returncode == 0 and tree.returncode == 0 and parent.returncode == 0
    return {"head": head.stdout.strip(), "tree": tree.stdout.strip(),
            "parent": parent.stdout.strip(), "status": status.stdout,
            "tracked_diff_exit": str(diff.returncode)}


def check_identity(tag: str, raw: Path) -> dict[str, str]:
    ident = identity()
    (raw / f"guards-{tag}.txt").write_text(
        f"head={ident['head']}\ntree={ident['tree']}\nparent={ident['parent']}\n"
        f"tracked_diff_exit={ident['tracked_diff_exit']}\nstatus:\n{ident['status']}",
        encoding="utf-8")
    assert ident["head"] == EXP_HEAD, f"{tag}: HEAD moved {ident['head']}"
    assert ident["tree"] == EXP_TREE, f"{tag}: tree moved {ident['tree']}"
    assert ident["parent"] == EXP_PARENT, f"{tag}: parent moved {ident['parent']}"
    assert ident["tracked_diff_exit"] == "0", f"{tag}: tracked bytes changed"
    return ident


def child_env() -> tuple[dict[str, str], dict[str, str]]:
    env = dict(os.environ)
    for key in SCRUB:
        env.pop(key, None)
    env["GIT_NO_LAZY_FETCH"] = "1"
    env["GIT_ALLOW_PROTOCOL"] = "file"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.pop("PYTHONPATH", None)
    allow = {k: env[k] for k in ALLOW if k in env}
    allow["python"] = str(VENV_PY)
    allow["cwd"] = str(FIXTURE)
    return env, allow


def main() -> int:
    raw = Path(sys.argv[1])
    raw.mkdir(parents=True, exist_ok=True)
    (raw / "runner-argv.txt").write_text(
        f"argv={sys.argv}\ncwd={os.getcwd()}\n", encoding="utf-8")
    env, allow = child_env()
    (raw / "runner-env-allowlisted.txt").write_text(
        "".join(f"{k}={v}\n" for k, v in allow.items()), encoding="utf-8")
    before = check_identity("before", raw)
    (raw / "identity-before.txt").write_text(repr(before) + "\n", encoding="utf-8")
    failures: list[str] = []
    for name, dotted in METHODS:
        argv = [str(VENV_PY), "-m", "unittest", "-v", *dotted]
        (raw / f"{name}.argv.txt").write_text("argv=" + repr(argv) + "\n", encoding="utf-8")
        proc = subprocess.run(argv, cwd=str(FIXTURE), env=env,
                              capture_output=True, text=True, check=False)
        (raw / f"{name}.stdout.txt").write_text(proc.stdout, encoding="utf-8")
        (raw / f"{name}.stderr.txt").write_text(proc.stderr, encoding="utf-8")
        (raw / f"{name}.exit.txt").write_text(str(proc.returncode) + "\n", encoding="utf-8")
        if proc.returncode != 0:
            failures.append(name)
    after = check_identity("after", raw)
    (raw / "identity-after.txt").write_text(repr(after) + "\n", encoding="utf-8")
    (raw / "summary.txt").write_text(
        f"methods={len(METHODS)} failures={failures}\n", encoding="utf-8")
    print(f"methods={len(METHODS)} failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
