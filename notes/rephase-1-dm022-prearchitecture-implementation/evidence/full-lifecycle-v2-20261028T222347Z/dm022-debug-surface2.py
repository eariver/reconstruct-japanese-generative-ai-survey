#!/usr/bin/env python3
"""Reproduce THEMATIC surface in a PERSISTENT dir, then grep for ln-D001."""
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

PRIVATE = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/dm022-full-lifecycle-fixed2-20261028T192129Z")
sys.path.insert(0, str(PRIVATE))
REPO_ROOT = PRIVATE

KEEP = Path("/tmp/dm022-surface-keep2")
import shutil
shutil.rmtree(KEEP, ignore_errors=True)
KEEP.mkdir(exist_ok=True)

_real_tmp = tempfile.TemporaryDirectory
class KeepTmp:
    def __init__(self, *a, **k):
        self._d = str(KEEP / "fixture")
        os.makedirs(self._d, exist_ok=True)
    @property
    def name(self):
        return self._d
    def cleanup(self):
        pass
tempfile.TemporaryDirectory = KeepTmp  # noqa

os.chdir(str(PRIVATE))

from tests.test_dm022_full_lifecycle_v2 import Dm022FullLifecycleWitnessTests, _sha_file, _write
from scripts import survey_production_v2 as core
from scripts import survey_agent_control_v2 as agent
from scripts import survey_research_authority_v2 as low
from scripts import survey_prearchitecture_acceptance_v2 as high

case = Dm022FullLifecycleWitnessTests(methodName="test_thematic_draft_synthesis_reader")
witness = case._full_route_witness("THEMATIC", "dbg", "ln-D001")
approved = case._approve_architecture_for(witness, "dbg", hour=3)
root = approved["root"]; cfg = approved["cfg"]; state_abs = approved["state_abs"]
chain = witness["chain"]
case._materialize_canonical_accepted_evidence_tree(root, chain, state_abs)
input_path = case._build_drafting_input(root, chain, "dbg")
proc = subprocess.run(
    [sys.executable, "-m", "scripts.run_drafting_synthesis_v2_interactive",
     "--repo-root", str(root), "--state", str(state_abs.relative_to(root)),
     "--input", str(input_path.relative_to(root))],
    cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=300)
assert proc.returncode == 0, proc.stderr[-2000:]
source_root = approved["source_root"]
draft_artifacts = {
    "synthesis-input": source_root / "draft/v2/profile-synthesis-input.json",
    "synthesis-result": source_root / "draft/v2/profile-synthesis-result.json",
}
for package_path in sorted((source_root / "draft/v2/packages").glob("*/draft-package.json")):
    pid = package_path.parent.name
    draft_artifacts[f"draft-package:{pid}"] = package_path
    draft_artifacts[f"draft-result:{pid}"] = package_path.parent / "draft-result.json"
reviews_path = case._stage_reviews_for(root, cfg, state_abs, draft_artifacts, "draft-dbg")
checkpoint = agent.build_stage_checkpoint(
    root, cfg, state_abs, draft_artifacts, reviews_path, "dbg",
    datetime(2026, 10, 28, 4, 0, 0, tzinfo=timezone.utc))
updated = agent.advance_with_checkpoint(root, cfg, state_abs, checkpoint)
assert updated["lifecycle_state"] == "DRAFT_COMPLETE"
case._write_interactive_evidence_for_longform(root, chain, state_abs, "dbg")
deriv_input = case._build_longform_derivation_input(root, chain, "dbg")
r1 = subprocess.run(
    [sys.executable, "-m", "scripts.survey_longform_semantic_publication_v2",
     "--repo-root", str(root), "--state", str(state_abs.relative_to(root)),
     "--input", str(deriv_input.relative_to(root)), "--materialize-surface-only"],
    cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=300)
print("r1 rc:", r1.returncode)
print("r1 stdout:", r1.stdout[-500:])
print("r1 stderr:", r1.stderr[-2000:])
surface_path = source_root / "publication/v2/reader-surface-input-v2.json"
if surface_path.is_file():
    text = surface_path.read_text()
    for m in re.finditer(r".{80}ln-D001.{80}", text):
        print("HIT:", m.group(0)[:200].replace("\n", " "))
print("KEEP root:", root)
