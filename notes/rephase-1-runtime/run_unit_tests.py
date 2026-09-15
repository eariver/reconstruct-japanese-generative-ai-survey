"""Run the unchanged execution-record unit suite against isolated r2 copies.

The upstream suite mocks Profile/State loaders. It is NOT full Core validation.
No new authority mocks; process/network/.git access is denied, never faked.
"""
import hashlib
import io
import json
import os
from pathlib import Path
import runpy
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REF = '774dd39a951c9ac3818e83dfffd4c7666efb0a20'
SOURCE = ROOT / '.rephase-1-inputs' / REF
CANDIDATE = ROOT / '.rephase-1-inputs/contract-candidate-r2'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    assert sys.flags.isolated and sys.dont_write_bytecode, 'Run with python -I -B'
    rows = json.loads((HERE / 'inputs.json').read_text(encoding='utf-8'))
    candidate_rows = json.loads((HERE.parent / 'rephase-1-connection/candidate-files.json').read_text(encoding='utf-8'))
    for row in rows:
        assert digest(SOURCE / row['path']) == row['sha256']
    for row in candidate_rows:
        assert digest(CANDIDATE / row['path']) == row['proposed_sha256']
    runtime_parent = ROOT / '.rephase-1-inputs/runtime-tests'
    runtime_parent.mkdir(exist_ok=True)
    assert runtime_parent.resolve().is_relative_to((ROOT / '.rephase-1-inputs').resolve())
    blocked, loaded = [], []
    result_data = dict(baseline=REF, candidate='r2', scope='EXISTING_MOCKED_LOADER_UNIT_TESTS_NOT_CORE_INTEGRATION',
        existing_mocks=['survey_execution_record_v2._load_profile', 'survey_execution_record_v2._load_state'],
        new_authority_mocks=False, git_operations=False, full_state_validation=False,
        cli_bridge_actions_executed=False, production_writes=False)

    def guard(event, args):
        denied = (event in {'subprocess.Popen', 'os.system', 'os.posix_spawn', 'os.spawn', 'os.exec', 'os.startfile',
                            'socket.connect', 'socket.connect_ex', 'socket.bind', 'socket.getaddrinfo'}
                  or event.startswith('os.spawn') or event.startswith('os.exec'))
        if event in {'open', 'os.listdir', 'os.scandir'} and args and isinstance(args[0], (str, bytes, os.PathLike)):
            path = os.fsdecode(args[0]).replace('\\', '/').lower()
            denied = denied or '.git' in path.split('/')
        if denied:
            blocked.append(event)
            raise RuntimeError('Prohibited operation denied before execution: ' + event)

    output = io.StringIO()
    with tempfile.TemporaryDirectory(prefix='r2-unit-', dir=runtime_parent) as directory:
        sandbox = Path(directory).resolve()
        assert sandbox.is_relative_to(runtime_parent.resolve())
        for row in rows:
            rel = row['path']
            src = CANDIDATE / rel if rel == 'scripts/survey_execution_record_v2.py' else SOURCE / rel
            dest = sandbox / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(src.read_bytes())
            loaded.append(dict(path=rel, sha256=digest(dest), source='r2' if src.is_relative_to(CANDIDATE) else REF))
        # Baseline has namespace packages; keep it that way and assert actual import origins below.
        (sandbox / 'fixtures').mkdir()
        previous_tempdir, previous_cwd = tempfile.tempdir, Path.cwd()
        tempfile.tempdir = str(sandbox / 'fixtures')
        os.chdir(sandbox)
        sys.path.insert(0, str(sandbox))
        sys.addaudithook(guard)
        try:
            module = runpy.run_path(str(sandbox / 'tests/test_survey_execution_record_v2.py'), run_name='isolated_unit_tests')
            execution = sys.modules['scripts.survey_execution_record_v2']
            assert Path(execution.__file__).resolve() == sandbox / 'scripts/survey_execution_record_v2.py'
            suite = unittest.defaultTestLoader.loadTestsFromTestCase(module['SurveyExecutionRecordV2Tests'])
            result = unittest.TextTestRunner(stream=output, verbosity=2).run(suite)
            result_data.update(tests_run=result.testsRun, failures=len(result.failures), errors=len(result.errors),
                               success=result.wasSuccessful(), skipped=len(result.skipped))
            assert result.testsRun == 5
            for name, imported in list(sys.modules.items()):
                if name.startswith('scripts.') and getattr(imported, '__file__', None):
                    assert Path(imported.__file__).resolve().is_relative_to(sandbox)
            result_data['imported_script_modules'] = sorted(name for name in sys.modules if name.startswith('scripts.'))
        except Exception as exc:
            result_data.update(success=False, setup_exception=repr(exc))
            raise
        finally:
            os.chdir(previous_cwd)
            tempfile.tempdir = previous_tempdir
            result_data.update(blocked_operations=blocked, copied_inputs=loaded,
                               python_version=sys.version, candidate_files=candidate_rows)
            (HERE / 'unit-tests.txt').write_text(output.getvalue(), encoding='utf-8')
            (HERE / 'unit-results.json').write_text(json.dumps(result_data, indent=2) + '\n', encoding='utf-8')
    for row in rows:
        assert digest(SOURCE / row['path']) == row['sha256']
    for row in candidate_rows:
        assert digest(CANDIDATE / row['path']) == row['proposed_sha256']
    assert not blocked, blocked
    assert result_data['success'], output.getvalue()
    print(json.dumps({key: result_data[key] for key in ('scope','tests_run','success','failures','errors','blocked_operations')}, indent=2))


if __name__ == '__main__':
    run()
