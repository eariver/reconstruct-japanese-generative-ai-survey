import json,subprocess,sys,importlib.metadata
from pathlib import Path
root=Path('/tmp/jgas-rephase-r2-502b3781')
assert root.is_dir() and (root/'.git').is_dir()
def git(*args):return subprocess.run(['git',*args],cwd=root,check=True,capture_output=True,text=True).stdout.strip()
assert Path(git('rev-parse','--show-toplevel')).resolve()==root
assert Path(git('rev-parse','--absolute-git-dir')).resolve()==root/'.git'
assert not (root/'.git/objects/info/alternates').exists()
git('remote','set-url','origin','https://example.invalid/rephase-fixture.git')
for ref in git('for-each-ref','--format=%(refname)','refs/remotes/').splitlines():git('update-ref','--no-deref','-d',ref)
git('config','core.autocrlf','false')
(root/'.fixture-scratch').mkdir(exist_ok=True)
report=dict(fixture_root=str(root),head=git('rev-parse','HEAD'),git_dir=git('rev-parse','--absolute-git-dir'),origin=git('remote','get-url','origin'),refs=git('for-each-ref','--format=%(refname)').splitlines(),python=sys.version,packages={x:importlib.metadata.version(x) for x in ['jsonschema','pypdf','attrs','referencing','rpds-py','jsonschema-specifications','typing-extensions']},git_version=git('--version'),no_alternates=True)
(Path(__file__).resolve().parent/'native-environment.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
