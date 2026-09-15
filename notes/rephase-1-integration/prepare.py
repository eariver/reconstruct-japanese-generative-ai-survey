"""Materialize fixed-ref Core/test subset in an independent fixture Git root.

This is a synthetic snapshot commit, not the actual production commit/history.
No production checkout, main lookup, Git remote fetch, or push is used.
"""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import subprocess
from urllib.request import urlopen

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REF = '774dd39a951c9ac3818e83dfffd4c7666efb0a20'
CACHE = ROOT / '.rephase-1-inputs' / REF
TARGET = ROOT / '.rephase-1-inputs/integration-r2'


def git(*args):
    return subprocess.run(['git', *args], cwd=TARGET, check=True, capture_output=True, text=True).stdout.strip()


def main():
    assert not any(k in os.environ for k in ['GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE','GIT_OBJECT_DIRECTORY','GIT_ALTERNATE_OBJECT_DIRECTORIES']), 'Inherited Git overrides are not allowed'
    assert not TARGET.exists(), 'Preserve previous fixture runs; do not overwrite'
    tree = json.loads((CACHE / 'tree.json').read_text(encoding='utf-8'))
    assert tree['sha'] == REF and not tree['truncated']
    exact = {'AGENTS.md','README.md','.gitignore','.latexmkrc',
             'tests/test_survey_core_execution_bridge_v2.py',
             'tests/test_survey_core_execution_bridge_human_gate_v2.py',
             'tests/test_survey_human_gate_v2.py'}
    roots = {'config','docs','schemas','scripts','.github','templates','specials'}
    selected = [r for r in tree['tree'] if r['type']=='blob' and (r['path'].split('/')[0] in roots or r['path'] in exact)]
    old_roots = [CACHE, ROOT / '.phase-5-inputs' / REF, ROOT / '.phase-5-inputs/upstream-reconciliation', ROOT / '.phase-5-inputs/runtime-repair-candidate']

    def acquire(row):
        def matches(data):
            return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == row['sha']
        path = row['path']
        assert '..' not in Path(path).parts and not Path(path).is_absolute()
        raw, provenance = None, None
        for base in old_roots:
            p = base / path
            if p.is_file() and matches(p.read_bytes()):
                raw, provenance = p.read_bytes(), 'HASH_VERIFIED_LOCAL_CACHE'
                break
        url = f'https://raw.githubusercontent.com/eariver/japanese-generative-ai-survey/{REF}/{path}'
        if raw is None:
            with urlopen(url, timeout=45) as response:
                raw = response.read()
            provenance = 'FIXED_REF_RAW_GET'
        assert matches(raw), path
        cached = CACHE / path
        if not cached.exists():
            cached.parent.mkdir(parents=True, exist_ok=True)
            cached.write_bytes(raw)
        else:
            assert cached.read_bytes() == raw
        return dict(path=path, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(), git_blob_sha1=row['sha'], mode=row['mode'], url=url, acquisition=provenance)

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        manifest = list(pool.map(acquire, selected))
    HERE.mkdir(exist_ok=True)
    (HERE / 'inputs.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    TARGET.mkdir()
    assert TARGET.resolve().is_relative_to((ROOT / '.rephase-1-inputs').resolve())
    for row in manifest:
        dest = TARGET / row['path']
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes((CACHE / row['path']).read_bytes())
    git('init', '-b', 'fixture-baseline')
    assert Path(git('rev-parse','--show-toplevel')).resolve() == TARGET.resolve()
    assert Path(git('rev-parse','--absolute-git-dir')).resolve() == TARGET / '.git'
    git('config','user.name','Rephase Integration Fixture')
    git('config','user.email','rephase-fixture@example.invalid')
    git('config','core.autocrlf','false')
    git('config','commit.gpgsign','false')
    git('remote','add','origin','https://example.invalid/rephase-fixture.git')
    git('add','--all')
    git('commit','-m','Synthetic fixed-774dd39a Core subset; not production history')
    baseline = git('rev-parse','HEAD')
    git('switch','-c','codex/rephase-r2-fixture')
    candidates = json.loads((HERE.parent / 'rephase-1-connection/candidate-files.json').read_text(encoding='utf-8'))
    for row in candidates:
        raw = (ROOT / '.rephase-1-inputs/contract-candidate-r2' / row['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row['proposed_sha256']
        (TARGET / row['path']).write_bytes(raw)
    git('add','--all')
    git('commit','-m','Synthetic r2 candidate for integration verification only')
    candidate = git('rev-parse','HEAD')
    changed = git('diff','--name-only',baseline,candidate).splitlines()
    assert sorted(changed) == sorted(r['path'] for r in candidates)
    assert not git('status','--porcelain')
    report = dict(production_baseline=REF, fixture_root=str(TARGET),
                  snapshot_scope='CONTROL_DOCS_SCHEMAS_SCRIPTS_TEMPLATES_SPECIAL_SPECS_AND_THREE_TESTS_NO_PRODUCTION_SOURCES_SURVEYS',
                  synthetic_baseline_commit=baseline, synthetic_r2_commit=candidate,
                  candidate_files=candidates, captured_files=len(manifest),
                  network_files=sum(r['acquisition']=='FIXED_REF_RAW_GET' for r in manifest),
                  origin=git('remote','get-url','origin'), git_dir=git('rev-parse','--absolute-git-dir'))
    (HERE / 'setup.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
