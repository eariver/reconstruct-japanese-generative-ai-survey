"""Run selected unchanged upstream classes in the independent r2 Git fixture."""
import collections
import hashlib
import io
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FIXTURE = Path(os.environ.get('REPHASE_FIXTURE_DIR', str(ROOT / '.rephase-1-inputs/integration-r2'))).resolve()


def main():
    assert sys.flags.isolated and sys.dont_write_bytecode
    setup = json.loads((HERE / 'setup.json').read_text(encoding='utf-8'))
    def git(*args):
        return subprocess.run(['git',*args],cwd=FIXTURE,check=True,capture_output=True,text=True).stdout.strip()
    assert Path(git('rev-parse','--show-toplevel')).resolve() == FIXTURE.resolve()
    assert Path(git('rev-parse','--absolute-git-dir')).resolve() == FIXTURE / '.git'
    assert git('rev-parse','HEAD') == setup['synthetic_r2_commit']
    assert git('remote','get-url','origin') == 'https://example.invalid/rephase-fixture.git'
    start_index = hashlib.sha256((FIXTURE / '.git/index').read_bytes()).hexdigest()
    scratch = FIXTURE / '.fixture-scratch'
    scratch.mkdir(exist_ok=True)
    tempfile.tempdir = str(scratch)
    os.environ['TMP'] = os.environ['TEMP'] = str(scratch)
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    os.chdir(FIXTURE)
    sys.path.insert(0,str(FIXTURE))
    commands, blocked = collections.Counter(), []
    allowed = {'rev-parse','show','diff','diff-tree','merge-base','for-each-ref','cat-file',
               'update-ref','hash-object','read-tree','update-index','write-tree','commit-tree',
               'config','remote','ls-files','ls-tree','show-ref','status','symbolic-ref','log','check-ref-format','rev-list'}

    def audit(event,args):
        if event == 'subprocess.Popen':
            executable, argv, cwd, env = args
            argv = [part.strip('"') for part in shlex.split(argv, posix=False)] if isinstance(argv, str) else list(argv)
            assert Path(executable or argv[0]).name.lower() in {'git','git.exe'}, 'Only local Git subprocesses are expected'
            assert Path(cwd or Path.cwd()).resolve().is_relative_to(FIXTURE.resolve()), 'Foreign subprocess cwd'
            i=1
            while i < len(argv) and argv[i] == '-c': i += 2
            verb=argv[i]
            if verb not in allowed:
                blocked.append(verb); raise RuntimeError('Unexpected Git operation: '+verb)
            for key in ('GIT_DIR','GIT_WORK_TREE','GIT_OBJECT_DIRECTORY','GIT_ALTERNATE_OBJECT_DIRECTORIES'):
                assert not (env or os.environ).get(key), key
            index=(env or os.environ).get('GIT_INDEX_FILE')
            if index: assert Path(index).resolve().is_relative_to(FIXTURE.resolve())
            commands[verb]+=1
        elif event in {'socket.connect','socket.bind','socket.getaddrinfo','os.system','os.startfile'}:
            blocked.append(event); raise RuntimeError('External operation not authorized: '+event)
    sys.addaudithook(audit)
    from tests.test_survey_core_execution_bridge_v2 import SurveyCoreExecutionBridgeV2Tests
    from tests.test_survey_core_execution_bridge_human_gate_v2 import SurveyCoreExecutionBridgeHumanGateV2Tests
    from tests.test_survey_human_gate_v2 import SurveyHumanGateV2Tests
    classes=[SurveyCoreExecutionBridgeV2Tests,SurveyCoreExecutionBridgeHumanGateV2Tests,SurveyHumanGateV2Tests]
    if '--failed-only' in sys.argv:
        previous=json.loads((HERE/'upstream-results.json').read_text())
        selected=previous['error_ids']+previous['failure_ids']
        assert selected
        suite=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromName(name) for name in selected)
    else:
        selected=None
        suite=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(cls) for cls in classes)
    output=io.StringIO()
    result=unittest.TextTestRunner(stream=output,verbosity=2).run(suite)
    (HERE / 'upstream-suite.txt').write_text(output.getvalue(),encoding='utf-8')
    assert git('rev-parse','HEAD') == setup['synthetic_r2_commit']
    assert hashlib.sha256((FIXTURE / '.git/index').read_bytes()).hexdigest() == start_index
    refs=git('for-each-ref','--format=%(refname)')
    assert 'refs/remotes/' not in refs, refs
    report=dict(scope='UNCHANGED_UPSTREAM_BRIDGE_AND_HUMAN_GATE_CLASSES_SYNTHETIC_GIT_FIXTURE',
                tests_run=result.testsRun, failures=len(result.failures), errors=len(result.errors),
                skipped=len(result.skipped), success=result.wasSuccessful(),
                failure_ids=[test.id() for test,_ in result.failures],error_ids=[test.id() for test,_ in result.errors],
                git_command_counts=dict(commands),blocked_operations=blocked,
                fixture_head_unchanged=True,normal_index_unchanged=True,test_remote_refs_cleaned=True,
                mocks_added=False,production_mutation=False,selected_test_ids=selected,setup_commit=setup['synthetic_r2_commit'])
    (HERE / 'upstream-results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))
    if not result.wasSuccessful():
        raise SystemExit(1)


if __name__ == '__main__':
    main()
