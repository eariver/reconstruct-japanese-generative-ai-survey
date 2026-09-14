"""Git-free r2 checks: templates/AST, saved bytes, and upstream document-only tests.

Does not import production modules or execute initialize/validate/bridge/CLI.
"""
import ast
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import re
import runpy
import tempfile
import unittest

from build_r2 import HERE, PRIOR, SOURCE, TARGET, REF, apply_patch


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fn(tree, name):
    return next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)


def template(tree, name, scope):
    node = next(n for n in fn(tree, 'initialize').body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == name for t in n.targets))
    return eval(compile(ast.Expression(node.value), '<template-only>', 'eval'), {'__builtins__': {}}, scope)


def constants(tree, name):
    node = next(n for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == name for t in n.targets))
    return ast.literal_eval(node.value)


def section(text, number):
    match = re.search(rf'^## {number}\. .*$', text, re.M)
    end = text.find('\n## ', match.end())
    return text[match.start():end if end >= 0 else len(text)]


def run():
    checks = []
    inputs = {}
    for manifest in (PRIOR / 'inputs.json', HERE / 'inputs.json'):
        for row in json.loads(manifest.read_text(encoding='utf-8')):
            assert sha(SOURCE / row['path']) == row['sha256']
            inputs[row['path']] = row['sha256']
    rows = json.loads((HERE / 'candidate-files.json').read_text(encoding='utf-8'))
    originals = {r['path']: (SOURCE / r['path']).read_text(encoding='utf-8') for r in rows}
    applied = apply_patch(originals, (HERE / 'candidate.patch').read_text(encoding='utf-8'))
    for row in rows:
        assert sha(TARGET / row['path']) == row['proposed_sha256']
        assert applied[row['path']] == (TARGET / row['path']).read_text(encoding='utf-8')
    checks.append('All captured source bytes unchanged; five-file r2 patch roundtrip/hash match')

    path = 'scripts/survey_execution_record_v2.py'
    old, new = [ast.parse((root / path).read_text(encoding='utf-8')) for root in (SOURCE, TARGET)]
    # Prove all executable structure other than the two text templates unchanged.
    stripped = []
    for tree in (old, new):
        clone = copy.deepcopy(tree)
        init = fn(clone, 'initialize')
        init.body = [n for n in init.body if not (isinstance(n, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id in ('index', 'session') for t in n.targets))]
        stripped.append(ast.dump(clone))
    assert stripped[0] == stripped[1]
    checks.append('Entire helper AST unchanged outside index/session templates, including signatures, CLI and validation')

    cfg = json.loads((SOURCE / 'config/survey-production-v2.json').read_text(encoding='utf-8'))
    renderings = {}
    for edition in ('2026-W34', 'SP001'):
        profile_path = f'sources/{edition}/production-profile.json'
        state_path = f'sources/{edition}/production-state.json'
        profile = json.loads((SOURCE / profile_path).read_text(encoding='utf-8'))
        scope = dict(profile=profile, cfg=cfg, state_rel=state_path, profile_rel=profile_path,
            state_sha='a' * 64, lifecycle='SYNTHETIC_LIFECYCLE', terminal='SYNTHETIC_TERMINAL',
            next_action='SYNTHETIC_NEXT', branch=profile['paths']['work_branch'],
            branch_head='b' * 40, main_sha=REF, started_utc='2026-09-15T00:00:00Z',
            requested_stop='COMPLETE', session_id='EXAMPLE_ONLY', objective='SYNTHETIC_OBJECTIVE',
            disposition='BLOCKED_CORE_DEFECT', x_policy='REQUIRED_BY_PROFILE')
        index, session = [template(new, name, scope) for name in ('index', 'session')]
        assert all(h in index for h in constants(new, 'INDEX_HEADINGS'))
        assert all(h in session for h in constants(new, 'SESSION_HEADINGS'))
        assert '## Deterministic execution transport' in session
        # The existing execution-record test's six navigation expectations (with real Profiles).
        for value in (edition, profile['research_profile'], profile['publication_profile'],
                      profile['paths']['work_branch'], 'REQUIRED_BY_PROFILE', state_path):
            assert f'`{value}`' in index
        assert 'sessions/EXAMPLE_ONLY.md' in index and 'SYNTHETIC_OBJECTIVE' in session
        assert 'BLOCKED_CORE_DEFECT' in session and 'BLOCKED_CORE_DEFECT' not in index
        assert 'SYNTHETIC_LIFECYCLE' not in index and 'SYNTHETIC_NEXT' not in index
        assert cfg['state_authority']['human_review_index_path'] in index
        assert 'not the newest historical approval' in index
        # Candidate-specific negatives: configuration-driven path and absent configuration.
        custom_cfg = copy.deepcopy(cfg)
        custom_cfg['state_authority']['human_review_index_path'] = 'custom/history.json'
        custom = template(new, 'index', dict(scope, cfg=custom_cfg))
        assert 'custom/history.json' in custom and 'gates/review-index.json' not in custom
        missing = template(new, 'index', dict(scope, cfg={}))
        assert '`NOT_CONFIGURED`' in missing and 'not approval' in missing
        renderings[edition] = dict(index=index, session=session)
    checks.append('Two real Profile shapes with synthetic template values preserve navigation; custom/missing review-path config is explicit')
    (HERE / 'template-examples.json').write_text(json.dumps(dict(scope='TEMPLATE_ONLY_SYNTHETIC_SESSION_NOT_EXECUTION', examples=renderings), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    count = 0
    for name, numbers in [('authority', [2,3,5,6,7,8,9,10,12]), ('redesign-authority', list(range(1,14))), ('session-bootstrap', [1,3,4,5,6,7,8,9,10,11,12,14]), ('execution-record-policy', [1,2,3,5,6,7,8,10])]:
        p = 'docs/survey-production-core-v2-' + name + '.md'
        for number in numbers:
            assert section((SOURCE / p).read_text(encoding='utf-8'), number) == section((TARGET / p).read_text(encoding='utf-8'), number)
            count += 1
    assert count == 42
    checks.append('42 unedited normative sections still identical in r2; semantic edited-section review remains root-only')

    # This inspected test imports only stdlib unittest/Path and reads three documents.
    # Run the exact upstream class, with real document copies, no module mocks.
    test_path = SOURCE / 'tests/test_survey_final_audit_rule_v2.py'
    module = runpy.run_path(str(test_path), run_name='offline_document_test')
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(module['SurveyFinalAuditRuleV2Tests'])
    output = io.StringIO()
    cwd = Path.cwd()
    with tempfile.TemporaryDirectory(prefix='rephase-r2-docs-') as folder:
        root = Path(folder)
        for p, origin in [('AGENTS.md', SOURCE), ('docs/survey-production-core-v2-final-audit-rule.md', SOURCE), ('docs/survey-production-core-v2-session-bootstrap.md', TARGET)]:
            target = root / p
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((origin / p).read_bytes())
        try:
            os.chdir(root)
            result = unittest.TextTestRunner(stream=output, verbosity=2).run(suite)
        finally:
            os.chdir(cwd)
    assert result.wasSuccessful(), output.getvalue()
    assert result.testsRun == 4
    (HERE / 'upstream-document-tests.txt').write_text(output.getvalue(), encoding='utf-8')
    checks.append('Four unchanged upstream final-audit document tests passed on isolated r2 document set (no production imports/mocks)')
    for p, digest in inputs.items():
        assert sha(SOURCE / p) == digest
    report = dict(baseline=REF, scope='ROOT_STATIC_AND_TEMPLATE_REVIEW_PLUS_DOCUMENT_ONLY_TESTS',
        checks=checks, grouped_checks=len(checks), source_files=len(inputs),
        production_module_imports=False, initialize_validate_bridge_cli_executed=False,
        upstream_execution_record_tests='STATIC_REVIEW_ONLY', git_operations=False,
        independent_review=False, execution_admission='NOT_EVALUATED')
    (HERE / 'checks.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    run()
