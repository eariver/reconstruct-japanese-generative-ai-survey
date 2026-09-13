"""Run from an isolated fixed-ref Core snapshot, with dependencies available."""
import hashlib
import importlib.metadata
import json
import platform
from pathlib import Path
import sys
import time
import unittest

mode, destination = sys.argv[1:]
if mode == "baseline":
    names = ["tests.test_runtime_repair.RuntimeRepairTests.test_weekly_special_freeze_release_and_retry_after_local_failure"]
elif mode == "git-aware":
    names = ["tests.test_survey_human_gate_revalidation_revision_v2"]
else:
    names = ["tests.test_runtime_repair.RuntimeRepairTests", "tests.test_runtime_repair.RevalidatedFreezeTests",
             "tests.test_survey_publication_v2", "tests.test_survey_stage_validation_v2",
             "tests.test_survey_release_checkpoint_v2", "tests.test_survey_agent_control_v2",
             "tests.test_survey_publication_revalidation_v2", "tests.test_survey_human_gate_revalidation_revision_v2"]
sys.path.insert(0, str(Path.cwd()))
started = time.monotonic()
result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(names))
paths = ["scripts/survey_stage_validation_v2.py", "scripts/survey_release_checkpoint_v2.py", "tests/test_runtime_repair.py",
         "tests/test_survey_release_checkpoint_v2.py"]
report = {"mode":mode,"suite_names":names,"tests_run":result.testsRun,"successful":result.wasSuccessful(),
          "failures":[{"test":str(t),"traceback":err} for t,err in result.failures],
          "errors":[{"test":str(t),"traceback":err} for t,err in result.errors],
          "skipped":result.skipped,"elapsed_seconds":round(time.monotonic()-started,3),
          "python":platform.python_version(),"platform":platform.platform(),
          "dependencies":{k:importlib.metadata.version(k) for k in ("jsonschema","pypdf")},
          "input_sha256":{p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in paths},
          "limits":["Synthetic upstream research artifacts/reviewer decisions; no quality certification.",
                    "No production or external Release mutation; no live Actions replay.",
                    "Test elapsed time is not active-role work or lifecycle savings."]}
Path(destination).write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
raise SystemExit(0 if result.wasSuccessful() else 1)
