#!/usr/bin/env python3
"""Renewal U entry probe on fresh VALIDATED_DRAFT (fixed2 known snapshot).

Builds WEEKLY to VALIDATED_DRAFT via General witness helpers (no cleanup),
then calls public prepare_renewal U (REUSE_TARGETS). Preserves exact outcome:
exit 0 + ADOPTED-like result means renewal construction can proceed here;
a foreign-scope refusal is the precise C1-old blocker for root.
Exit codes: 0 = prepared (unexpected-healthy, report pins); 1 = probe setup
fault (not target); 2 = target refusal (expected if C1-old blocks; report).
"""
import os
import sys
import tempfile
import traceback
from datetime import datetime, timezone
from pathlib import Path

PRIVATE = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/dm022-full-lifecycle-fixed2-20261028T192129Z")
sys.path.insert(0, str(PRIVATE))
os.chdir(str(PRIVATE))

KEEP = Path("/tmp/dm022-renewal-probe-keep")
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

from tests.test_dm022_full_lifecycle_v2 import Dm022FullLifecycleWitnessTests  # noqa

case = Dm022FullLifecycleWitnessTests(methodName="test_weekly_publication_real_pdf_to_validated_draft")
try:
    validated = case._weekly_to_validated_draft("weekly-renewal-probe-v2")
except Exception as exc:
    print("PROBE SETUP FAILURE (fixture build):", type(exc).__name__, str(exc)[:800])
    traceback.print_exc()
    sys.exit(1)

root = validated["root"]
state_abs = validated["state_abs"]
print("fixture root:", root)
print("lifecycle:", __import__("json").loads(open(state_abs).read())["lifecycle_state"])
try:
    from scripts import survey_versioned_renewal_v2 as renewal
    out = renewal.prepare_renewal(
        root, state_abs, "ren-probe-v2", "REUSE_TARGETS",
        validated["manuscript_path"], None,
        "SYNTHETIC_FIXTURE_EXECUTOR_GENERAL_FULL_V2",
        datetime(2026, 10, 28, 16, 0, 0, tzinfo=timezone.utc))
    print("PREPARED keys:", sorted(out.keys()))
    print("PROBE OUTCOME: prepared (report pins to root)")
    sys.exit(0)
except Exception as exc:
    print("PROBE TARGET OUTCOME:", type(exc).__name__, str(exc)[:1500])
    traceback.print_exc()
    sys.exit(2)
