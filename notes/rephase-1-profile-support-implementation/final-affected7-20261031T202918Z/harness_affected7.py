"""Harness for final affected7: loader binding in SAME process before unittest, no validator changes.

Runs from PROOF_ROOT cwd with PYTHONPATH=PROOF_ROOT. Imports all runtime/test
modules, verifies __file__ under PROOF_ROOT (failclosed on wrong root), prints
LOADER_BINDING lines to stdout, then runs 7 C tests with verbose unittest to
stderr. No mocks, no validator mutation.
"""
import hashlib
import pathlib
import sys

PROOF_ROOT = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/profile-support-packaging-20261031T202327Z/proof-copy/candidate-partial-b40de60").resolve()

MODS = [
    "scripts.survey_screening_v2",
    "scripts.survey_evidence_v2",
    "scripts.run_evidence_v2_interactive",
    "scripts.run_evidence_v2_agent_first",
    "scripts.survey_research_authority_v2",
    "scripts.survey_prearchitecture_acceptance_v2",
    "tests.test_dm022_c_direct_operation_v2",
    "tests.test_dm022_prearchitecture_acceptance_v2",
    "tests.test_profile_support_upstream_repair_v2",
    "tests.test_survey_evidence_v2",
]

def _sha_file(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    import os
    print(f"HARNESS_CWD={os.getcwd()}", flush=True)
    print(f"HARNESS_PROOF_ROOT={PROOF_ROOT}", flush=True)
    print(f"HARNESS_SYS_VERSION={sys.version.replace(chr(10), ' ')}", flush=True)
    print(f"HARNESS_PYTHONPATH={os.environ.get('PYTHONPATH','')}", flush=True)
    print(f"HARNESS_RETAIN_ROOT={os.environ.get('PROFILE_SUPPORT_RETAIN_ROOT','')}", flush=True)
    try:
        import jsonschema
        print("HARNESS_jsonschema-present", flush=True)
    except Exception as e:
        print(f"HARNESS_jsonschema-LOAD_FAIL {e!r}", flush=True)
        return 1
    try:
        import pypdf
        print("HARNESS_pypdf-present", flush=True)
    except Exception as e:
        print(f"HARNESS_pypdf-LOAD_FAIL {e!r}", flush=True)
        return 1
    import importlib
    for m in MODS:
        try:
            mod = importlib.import_module(m)
            p = pathlib.Path(mod.__file__).resolve()
            # failclosed on wrong root
            try:
                p.relative_to(PROOF_ROOT)
            except ValueError:
                print(f"LOADER_BINDING {m} WRONG_ROOT __file__={p} expected_under={PROOF_ROOT}", flush=True)
                print(f"HARNESS_FAIL wrong root for {m}: {p}", file=sys.stderr, flush=True)
                return 2
            b = p.read_bytes()
            h = hashlib.sha256(b).hexdigest()
            st = p.stat()
            print(f"LOADER_BINDING {m} __file__={p} sha256={h} bytes={len(b)} mode={oct(st.st_mode & 0o777)}", flush=True)
        except Exception as e:
            print(f"LOADER_BINDING {m} LOAD_FAIL {e!r}", flush=True)
            import traceback
            traceback.print_exc()
            return 3
    # run 7 C tests in SAME process (no validator changes)
    import unittest
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName("tests.test_dm022_c_direct_operation_v2")
    # count check: must be 7, failclosed otherwise (do not silently run wrong count)
    count = suite.countTestCases()
    print(f"HARNESS_SUITE_COUNT={count}", flush=True)
    if count != 7:
        print(f"HARNESS_FAIL expected 7 tests, got {count}", file=sys.stderr, flush=True)
        return 4
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stderr)
    result = runner.run(suite)
    print(f"HARNESS_RESULT testsRun={result.testsRun} failures={len(result.failures)} errors={len(result.errors)} skipped={len(result.skipped) if hasattr(result,'skipped') else 0} wasSuccessful={result.wasSuccessful()}", flush=True)
    return 0 if result.wasSuccessful() else 5

if __name__ == "__main__":
    sys.exit(main())
