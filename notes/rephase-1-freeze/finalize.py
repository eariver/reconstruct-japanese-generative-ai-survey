"""Root integration: preserve before witnesses, freeze candidate, bounded regression.

Run in Ubuntu with the task-local Python 3.12 runtime. Never touches production.
"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time

HERE = Path(__file__).resolve().parent
FIX = Path('/tmp/jgas-rephase-freeze-b1b2')
BEFORE = Path('/tmp/jgas-rephase-freeze-before')
PYTHON = '/tmp/jgas-rephase-application-venv/bin/python'
BASE = 'd38f023ce200619f7f49ce17a348755f05e0e021'
PRODUCTION = '774dd39a951c9ac3818e83dfffd4c7666efb0a20'
RUNTIME = 'scripts/survey_stage_validation_v2.py'
TEST = 'tests/test_survey_freeze_stage_boundary_v2.py'


def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root).decode().strip()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root, name, tests):
    command = [PYTHON, '-m', 'unittest', *tests, '-v']
    started = time.monotonic()
    with (HERE / (name + '.log')).open('w') as log:
        proc = subprocess.run(command, cwd=root, stdout=log, stderr=subprocess.STDOUT)
    result = dict(command=command, fixture=str(root), head=git(root, 'rev-parse', 'HEAD'),
                  exit_code=proc.returncode, elapsed_seconds=round(time.monotonic()-started, 3),
                  runtime_sha256=sha(root/RUNTIME), test_sha256=sha(root/TEST))
    (HERE/(name+'.json')).write_text(json.dumps(result, indent=2)+'\n')
    print(name, json.dumps(result), flush=True)
    return proc.returncode


def main():
    assert git(FIX, 'rev-parse', 'HEAD') == BASE
    assert not BEFORE.exists()
    # The Worker wrote seven connected tests before the session stopped. Root
    # owns this additional typed-loader witness and all execution/closeout.
    path = FIX/TEST
    content = path.read_text()
    marker = '    def test_weekly_approved_preview_advances_through_real_freeze_boundary(self) -> None:\n'
    extra = '''    def test_approved_preview_resolves_as_typed_authority(self) -> None:
        fix = self.make_fixture()
        candidate = self.build_candidate_and_advance(fix)
        self.approve_and_build_freeze(fix, candidate)
        state = core.load_json(fix.src / "production-state.json")
        artifacts = stage_validation._prior_artifacts(self.root, self.cfg, state)
        self.assertEqual(artifacts["publication-candidate"], candidate)

'''
    assert 'test_approved_preview_resolves_as_typed_authority' not in content
    path.write_text(content.replace(marker, extra+marker))
    shutil.copytree(FIX, BEFORE, copy_function=shutil.copy2,
                    ignore=shutil.ignore_patterns('__pycache__'))
    (BEFORE/RUNTIME).write_bytes(subprocess.check_output(['git','show',f'{BASE}:{RUNTIME}'],cwd=BEFORE))
    assert not (BEFORE/'.git/objects/info/alternates').exists()
    assert git(BEFORE,'remote','get-url','origin') == 'https://example.invalid/rephase-application.git'
    prefix = 'tests.test_survey_freeze_stage_boundary_v2.FreezeStageBoundaryV2Tests.'
    assert run(BEFORE,'before-b1',[prefix+'test_weekly_approved_preview_advances_through_real_freeze_boundary']) != 0
    assert 'unexpected current stage artifacts: visual-review-record' in (HERE/'before-b1.log').read_text()
    assert run(BEFORE,'before-b2',[prefix+'test_approved_preview_resolves_as_typed_authority']) != 0
    assert 'Stage Checkpoint' in (HERE/'before-b2.log').read_text()
    git(FIX,'diff','--check')
    git(FIX,'add','--',RUNTIME,TEST)
    git(FIX,'-c','user.name=Rephase isolated fixture','-c','user.email=fixture@example.invalid',
        '-c','core.hooksPath=/dev/null','commit','-m','Repair typed preview approval and Freeze artifact boundary')
    head = git(FIX,'rev-parse','HEAD')
    files = git(FIX,'diff','--name-only',PRODUCTION,head).splitlines()
    for label, base in [('repair',BASE),('application',PRODUCTION)]:
        (HERE/(label+'.patch')).write_bytes(subprocess.check_output(['git','diff','--binary',base,head],cwd=FIX))
    (HERE/'candidate-files').mkdir()
    for name in [RUNTIME,TEST]:
        dst = HERE/'candidate-files'/name
        dst.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(FIX/name,dst)
    manifest = dict(candidate_head=head,candidate_tree=git(FIX,'rev-parse','HEAD^{tree}'),
        parent=git(FIX,'rev-parse','HEAD^'),production_baseline=PRODUCTION,
        fixture=str(FIX),origin=git(FIX,'remote','get-url','origin'),
        git_dir=git(FIX,'rev-parse','--absolute-git-dir'),alternates=False,
        files=[dict(path=p,sha256=sha(FIX/p)) for p in files])
    (HERE/'candidate.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('FROZEN',head,flush=True)
    tests = ['tests.test_survey_freeze_stage_boundary_v2',
             'tests.test_survey_stage_validation_v2',
             'tests.test_survey_agent_control_v2',
             'tests.test_survey_publication_v2']
    assert run(FIX,'targeted-regression',tests) == 0
    assert not git(FIX,'diff','--name-only') and not git(FIX,'diff','--cached','--name-only')
    assert git(FIX,'rev-parse','HEAD') == head
    print('COMPLETED',head,flush=True)


if __name__ == '__main__':
    main()
