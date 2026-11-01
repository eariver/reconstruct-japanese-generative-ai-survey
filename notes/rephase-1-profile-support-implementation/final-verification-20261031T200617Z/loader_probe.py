"""Loader probe: binds actual imported paths/bytes outside test semantics. No mocks."""
import hashlib
import importlib
import os
import pathlib
import sys
import traceback

MODS = [
    "scripts.survey_screening_v2",
    "scripts.survey_evidence_v2",
    "scripts.run_evidence_v2_interactive",
    "scripts.run_evidence_v2_agent_first",
    "scripts.survey_research_authority_v2",
    "scripts.survey_prearchitecture_acceptance_v2",
    "tests.test_profile_support_upstream_repair_v2",
    "tests.test_survey_evidence_v2",
    "tests.test_dm022_c_direct_operation_v2",
    "tests.test_dm022_prearchitecture_acceptance_v2",
    "tests.test_run_evidence_v2_interactive",
    "tests.test_run_evidence_v2_agent_first",
    "tests.test_dm022_full_lifecycle_v2",
]

print("LOADER_CWD=" + os.getcwd())
print("LOADER_SYS_VERSION=" + sys.version.replace("\n", " "))
try:
    import jsonschema
    print("jsonschema-present")
except Exception as e:
    print(f"jsonschema-LOAD_FAIL {e!r}")
try:
    import pypdf
    print("pypdf-present")
except Exception as e:
    print(f"pypdf-LOAD_FAIL {e!r}")

for m in MODS:
    try:
        mod = importlib.import_module(m)
        p = pathlib.Path(mod.__file__).resolve()
        b = p.read_bytes()
        h = hashlib.sha256(b).hexdigest()
        st = p.stat()
        print(f"{m} __file__={p} sha256={h} bytes={len(b)} mode={oct(st.st_mode & 0o777)}")
    except Exception as e:
        print(f"{m} LOAD_FAIL {e!r}")
        traceback.print_exc()
