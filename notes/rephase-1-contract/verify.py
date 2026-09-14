"""Bounded offline checks; no Git, production imports, workflow or transitions."""
import ast
import copy
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

from build_candidate import build, CANDIDATE, SOURCE, HERE, REF, PREFIX
from state_view import inspect


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def anchor(root, path):
    return dict(path=path, sha256=digest((root / path).read_bytes()))


def write(root, path, value):
    dest = root / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return anchor(root, path)


def assignment(tree, function, name):
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == function)
    return next(n for n in ast.walk(fn) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in n.targets))


def section(text, number):
    import re
    return re.search(r'^## ' + str(number) + r'\..*?(?=^## |\Z)', text, re.M | re.S).group()


def run():
    results = []
    manifest = json.loads((HERE / 'inputs.json').read_text(encoding='utf-8'))
    for row in manifest:
        raw = (SOURCE / row['path']).read_bytes()
        assert digest(raw) == row['sha256']
        assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == row['git_blob_sha1']
    build()
    before_sources = {r['path']: digest((SOURCE / r['path']).read_bytes()) for r in manifest}
    examples = {}
    for edition in ('2026-W34', 'SP001'):
        state_path = f'sources/{edition}/production-state.json'
        index_path = f'sources/{edition}/gates/review-index.json'
        view = inspect(SOURCE, anchor(SOURCE, state_path), REF, SOURCE / 'schemas', anchor(SOURCE, index_path))
        assert view['stored_facts']['lifecycle_state'] == 'RELEASED', view
        assert view['stored_facts']['next_action'] is None
        assert view['profile_link']['check'] == 'DIRECT_BYTES_SCHEMA_IDENTITY_MATCH', view['profile_link']
        assert view['active_approval_links']['publication_preview']['check'] == 'DIRECT_BYTES_SCHEMA_IDENTITY_MATCH'
        assert view['selected_checkpoint_links']['publication_preview']['expected_type'] == 'PUBLICATION_PREVIEW'
        assert view['execution_admission'] == 'NOT_EVALUATED'
        expected_mode = 'ROLLING_WINDOW' if edition == '2026-W34' else 'OPEN_HISTORY_AS_OF'
        assert view['profile_context']['temporal_policy']['mode'] == expected_mode
        examples[edition] = view
        results.append(f'{edition}: saved facts and typed direct Preview approval; no execution admission')
    state_path = 'sources/2026-W34/production-state.json'
    index_path = 'sources/2026-W34/gates/review-index.json'
    actual = json.loads((SOURCE / state_path).read_text(encoding='utf-8'))
    schemas = SOURCE / 'schemas'
    with tempfile.TemporaryDirectory(prefix='rephase-contract-') as tmp:
        root = Path(tmp)
        # Only captured files, not a repository/working tree. No .git directory.
        for row in manifest:
            if row['path'].startswith('sources/'):
                target = root / row['path']
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(SOURCE / row['path'], target)
        state_ref = anchor(root, state_path)
        index_ref = anchor(root, index_path)
        view = lambda ref=state_ref, idx=index_ref: inspect(root, ref, 'SYNTHETIC_FIXTURE_NOT_PRODUCTION', schemas, idx)
        # Old index cannot select a stage, including when its content or presence changes.
        old = view()
        nav = root / 'sources/2026-W34/execution/index.md'
        nav.write_text('ARCHITECTURE_REVIEW_READY_FOR_HUMAN\n', encoding='utf-8')
        assert view() == old
        nav.unlink()
        assert view() == old
        results.append('stale/missing Markdown index does not alter State-derived facts')
        bad = dict(state_ref, sha256='0' * 64)
        assert view(bad)['stored_facts'] is None
        results.append('State anchor mismatch suppresses displayed facts')
        approval_path = actual['human_gate_provenance']['publication_preview']['path']
        approval_raw = (root / approval_path).read_bytes()
        (root / approval_path).write_bytes(approval_raw + b' ')
        assert view()['active_approval_links']['publication_preview']['check'] == 'HASH_MISMATCH'
        (root / approval_path).unlink()
        assert view()['active_approval_links']['publication_preview']['check'] == 'MISSING'
        (root / approval_path).write_bytes(approval_raw)
        results.append('drifted/missing active approval is explicit; no history fallback')
        wrong = copy.deepcopy(actual)
        wrong['human_gate_provenance']['publication_preview'] = actual['checkpoint_provenance']['release']
        assert view(write(root, state_path, wrong))['active_approval_links']['publication_preview']['check'] == 'TYPE_OR_SCHEMA_MISMATCH'
        results.append('Stage Checkpoint cannot impersonate a Preview approval')
        wrong = copy.deepcopy(actual)
        wrong['profile'] = anchor(root, 'sources/SP001/production-profile.json')
        assert view(write(root, state_path, wrong))['profile_link']['check'] == 'ISSUE_MISMATCH'
        results.append('cross-edition Profile binding rejected by display check')
        wrong = copy.deepcopy(actual)
        wrong['human_gate_provenance']['publication_preview']['path'] = '../escape.json'
        assert view(write(root, state_path, wrong))['active_approval_links']['publication_preview']['check'] == 'UNSAFE_PATH'
        results.append('path traversal rejected without reading outside fixture')
        # Display of a hypothetical post-r2 REQUEST_CHANGES state; no Core transition performed.
        fixture = copy.deepcopy(actual)
        fixture['lifecycle_state'] = 'DRAFT_COMPLETE'
        fixture['next_action'] = 'stage:reader-publication-validation'
        fixture['terminal_reason'] = None
        fixture['human_gates']['publication_preview'] = 'pending'
        fixture['human_gate_provenance']['publication_preview'] = None
        for key in ('validation', 'publication_preview', 'freeze', 'release'):
            fixture['checkpoint_provenance'][key] = None
            fixture['machine_checkpoints'][key] = 'pending'
        index = json.loads((root / index_path).read_text(encoding='utf-8'))
        index['reviews'] = [r for r in index['reviews'] if not (r['gate'] == 'PUBLICATION_PREVIEW' and r['revision'] == 3)]
        reopened = view(write(root, state_path, fixture), write(root, index_path, index))
        assert reopened['active_approval_links']['publication_preview']['check'] == 'NOT_ACTIVE'
        assert reopened['active_approval_links']['architecture_review']['check'] == 'DIRECT_BYTES_SCHEMA_IDENTITY_MATCH'
        assert reopened['latest_recorded_reviews_not_active_authority'][-1]['stored_review']['decision'] == 'REQUEST_CHANGES'
        examples['publication-local-request-changes-FIXTURE'] = reopened
        results.append('REQUEST_CHANGES fixture preserves Architecture; historical Preview approval is not revived')
        fixture['lifecycle_state'] = 'EVIDENCE_REVIEWED'
        fixture['next_action'] = 'stage:selection'
        fixture['human_gates']['architecture_review'] = 'pending'
        fixture['human_gate_provenance']['architecture_review'] = None
        for key in ('selection', 'architecture', 'draft'):
            fixture['checkpoint_provenance'][key] = None
            fixture['machine_checkpoints'][key] = 'pending'
        synthetic_review_path = 'sources/2026-W34/gates/reviews/publication-r2.json'
        synthetic_review = json.loads((root / synthetic_review_path).read_text(encoding='utf-8'))
        synthetic_review.update(regeneration_boundary='EVIDENCE_REVIEWED',
                                reviewed_by='SYNTHETIC_FIXTURE_NOT_HUMAN',
                                requested_changes='Synthetic cross-gate display example; not a production decision.')
        synthetic_ref = write(root, synthetic_review_path, synthetic_review)
        for row in index['reviews']:
            if row['gate'] == 'PUBLICATION_PREVIEW' and row['revision'] == 2:
                row['record'] = synthetic_ref
        reopened = view(write(root, state_path, fixture), write(root, index_path, index))
        assert reopened['active_approval_links']['architecture_review']['check'] == 'NOT_ACTIVE'
        assert reopened['latest_recorded_reviews_not_active_authority'][0]['stored_review']['decision'] == 'APPROVED'
        examples['cross-gate-pending-FIXTURE'] = reopened
        results.append('cross-gate fixture displays historical Architecture approval separately from pending active gate')
        index['reviews'].append(index['reviews'][0])
        assert view(anchor(root, state_path), write(root, index_path, index))['historical_review_index']['check'] == 'NONCONTIGUOUS_OR_DUPLICATE_REVISIONS'
        results.append('duplicate review revisions are not silently selected')

    script = 'scripts/survey_execution_record_v2.py'
    old_tree = ast.parse((SOURCE / script).read_text(encoding='utf-8'))
    new_tree = ast.parse((CANDIDATE / script).read_text(encoding='utf-8'))
    profile = json.loads((SOURCE / actual['profile']['path']).read_text(encoding='utf-8'))
    scope = dict(profile=profile, state=actual, state_rel=state_path,
                 profile_rel=actual['profile']['path'], state_sha=anchor(SOURCE, state_path)['sha256'],
                 main_sha=REF, branch_head='f' * 40, started_utc='2026-09-15T00:00:00Z',
                 requested_stop='COMPLETE', branch=profile['paths']['work_branch'],
                 x_policy='REQUIRED', session_id='EXAMPLE_ONLY', disposition='IN_PROGRESS',
                 lifecycle='RELEASED', terminal='COMPLETE', next_action='none', objective='EXAMPLE_ONLY',
                 _gate_status=lambda state, key: state['human_gates'][key])
    def render(tree, name):
        return eval(compile(ast.Expression(assignment(tree, 'initialize', name).value), '<isolated-template>', 'eval'), {'__builtins__': {}}, scope)
    before, after = render(old_tree, 'index'), render(new_tree, 'index')
    assert 'Current lifecycle: `RELEASED`' in before
    assert 'Current lifecycle:' not in after and 'Current State SHA-256:' not in after
    assert 'Current Human review target:' not in after
    headings = next(n.value for n in new_tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'INDEX_HEADINGS' for t in n.targets))
    assert all(h in after for h in ast.literal_eval(headings))
    assert all(f'`{x}`' in after for x in (profile['issue_id'], profile['research_profile'], profile['publication_profile'], profile['paths']['work_branch']))
    assert 'Initial execution disposition: `IN_PROGRESS`' in render(new_tree, 'session')
    for fn in ('validate', '_load_state', '_load_profile'):
        old_fn = next(n for n in old_tree.body if isinstance(n, ast.FunctionDef) and n.name == fn)
        new_fn = next(n for n in new_tree.body if isinstance(n, ast.FunctionDef) and n.name == fn)
        assert ast.dump(old_fn) == ast.dump(new_fn)
    (HERE / 'navigation-template-example.md').write_text('<!-- ISOLATED TEMPLATE EXAMPLE; NOT W34 EXECUTION OR AUTHORITY -->\n' + after, encoding='utf-8')
    results.append('isolated initializer template removes copied state values; required headings/identity and validator AST retained')
    preserved_sections = 0
    for doc, numbers in [('authority', [2,3,5,6,7,8,9,10,12]), ('redesign-authority', list(range(1,14))), ('session-bootstrap', [1,3,4,5,6,7,8,9,10,11,12,14]), ('execution-record-policy', [1,2,3,5,6,7,8,10])]:
        path = PREFIX + doc + '.md'
        before = (SOURCE / path).read_text(encoding='utf-8')
        after = (CANDIDATE / path).read_text(encoding='utf-8')
        for number in numbers:
            assert section(before, number) == section(after, number), (doc, number)
            preserved_sections += 1
    results.append(f'{preserved_sections} untouched rule sections preserved verbatim; edited sections require semantic review')
    for path, sha in before_sources.items():
        assert digest((SOURCE / path).read_bytes()) == sha
    (HERE / 'examples.json').write_text(json.dumps(examples,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    output = dict(baseline=REF, scope='OFFLINE_DISPLAY_AND_TEMPLATE_CHECKS_NOT_CORE_EXECUTION', checks=results,
                  count=len(results), captured_inputs=len(manifest), baseline_files_unchanged=True,
                  production_imports=False, git_operations=False, independent_review=False)
    (HERE / 'checks.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    run()
