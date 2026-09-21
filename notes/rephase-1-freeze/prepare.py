"""Preserve a1; copy it into a separate database for the B1/B2 repair only."""
import json
from pathlib import Path
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = Path('/tmp/jgas-rephase-application-r2')
TARGET = Path('/tmp/jgas-rephase-freeze-b1b2')
EDIT = ROOT / '.rephase-1-inputs/freeze-b1b2-edit'
BASE = 'd38f023ce200619f7f49ce17a348755f05e0e021'


def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root, text=True).strip()


def main():
    assert not TARGET.exists() and not EDIT.exists()
    assert git(SOURCE, 'rev-parse', 'HEAD') == BASE
    assert not git(SOURCE, 'diff', '--name-only') and not git(SOURCE, 'diff', '--cached', '--name-only')
    shutil.copytree(SOURCE, TARGET, copy_function=shutil.copy2, symlinks=True,
                    ignore=shutil.ignore_patterns('__pycache__', 'tmp_5bh1f_6'))
    assert git(TARGET, 'rev-parse', '--absolute-git-dir') == str(TARGET / '.git')
    assert not (TARGET / '.git/objects/info/alternates').exists()
    assert git(TARGET, 'remote', 'get-url', 'origin') == 'https://example.invalid/rephase-application.git'
    git(TARGET, 'switch', '-c', 'codex/rephase-freeze-b1b2')
    path = Path('scripts/survey_stage_validation_v2.py')
    (EDIT / path).parent.mkdir(parents=True)
    shutil.copy2(TARGET/path, EDIT/path)
    result = dict(base=BASE, production_baseline=git(TARGET,'rev-parse','HEAD^'),
                  fixture=str(TARGET), edit_root=str(EDIT), origin=git(TARGET,'remote','get-url','origin'))
    (HERE/'setup.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':
    main()
