"""One source-join trace and corrective Card specimen; never production admission.

Only the inspected _build_card function is executed with a pre-resolved two-source
unit fixture. Full package/supplement validation, CLI, writers and Gates are not
executed. The fixture's exact input hashes are checked separately below.
"""
import ast
import copy
import hashlib
import json
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from types import SimpleNamespace
from typing import Any
import jsonschema
sys.dont_write_bytecode = True
from capture import LAB, ROOT, CACHE, HEAD, MAIN, save

FIXED = CACHE/HEAD
BASE = 'sources/2026-W34/evidence/v2/accepted/647cde464d92935c1ca633ade62bcbf7ebe88c458cc8b3848bae8d2fc4794831/'
RUN = 'sources/2026-W34/execution/luna/w34-screening-evidence-after-sol-discovery-r2/'
FILENAME = 'task-3ebd2dfa1c0a39c4f92a.json'
TID = 'evidence:2026-W34:589f97e8aee10bd1'
SID = 'supplement-src-6b3ce48a6c75d42b'


def read(rel):
    return json.loads((FIXED/rel).read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__(); self.skip = 0; self.parts = []
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'): self.skip += 1
    def handle_endtag(self, tag):
        if tag in ('script', 'style'): self.skip = max(0, self.skip - 1)
    def handle_data(self, value):
        if not self.skip and value.strip(): self.parts.append(value.strip())


def main():
    inputs = json.loads((LAB/'inputs.json').read_text(encoding='utf-8'))
    for row in inputs:
        path = CACHE/row['ref']/row['path']; raw = path.read_bytes()
        assert sha(path) == row['sha256']
        assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest() == row['git_blob_sha1']
    card = read(BASE+'results/'+FILENAME)
    task = read(BASE+'tasks/'+FILENAME)
    package = read(BASE+'package.json')
    acceptance = read(BASE+'evidence-accepted.json')
    meta = next(t for t in package['tasks'] if t['evidence_task_id'] == TID)
    accepted = next(t for t in acceptance['results'] if t['evidence_task_id'] == TID)
    bindings = []
    def bind(name, rel, expected):
        assert sha(FIXED/rel) == expected, name
        bindings.append(dict(name=name, path=rel, sha256=expected))
    bind('Card -> task', BASE+'tasks/'+FILENAME, card['basis']['task_sha256'])
    bind('Package -> task', BASE+meta['path'], meta['sha256'])
    bind('Acceptance -> Card', BASE+'results/'+accepted['filename'], accepted['sha256'])
    bind('Acceptance -> Package', BASE+'package.json', acceptance['package_sha256'])
    bind('Package -> supplement', package['authority_supplement']['path'], package['authority_supplement']['sha256'])
    for key,rel in [('prompt_sha256','config/prompts/evidence-verification-v2.md'),('result_contract_sha256','schemas/evidence-v2-card.schema.json')]:
        bind('Card -> '+key, rel, card['basis'][key])
    supplement = read(package['authority_supplement']['path'])
    source = next(s for s in supplement['sources'] if s['supplement_source_id'] == SID)
    assert source['evidence_task_id'] == TID and source['discovery_id'] == 'w34-event-c066'
    bind('Supplement -> primary HTML', source['raw_path'], source['raw_sha256'])
    assert (FIXED/source['raw_path']).stat().st_size == source['byte_count']
    original = task['source_records'][0]
    assert original['source_type'] == 'dailyx_x_observation'
    provenance = read('sources/2026-W34/external/x/dailyx/dailyx-source-provenance-v0.1.json')
    daily = next(r for r in provenance['files'] if r['source_filename'] == '2026-08-22_0700.md')
    raw_path = daily['repository_raw_path']
    assert raw_path in original['raw_paths'] and original['locator'] == daily['drive_url']
    bind('Task metadata -> DailyX bytes', raw_path, original['metadata']['sha256'])
    bind('Import provenance -> DailyX bytes', raw_path, daily['sha256'])
    assert daily['byte_count'] == original['metadata']['drive_byte_count'] == (FIXED/raw_path).stat().st_size
    assert daily['original_http_bytes_claimed'] is False
    daily_text = (FIXED/raw_path).read_text(encoding='utf-8')
    topic = daily_text.split('### 11. Grok Botのアクセス拡大', 1)[1].split('### 12.', 1)[0]
    x_url = 'https://x.com/elonmusk/status/2090853842552578523'
    assert x_url in topic and '2026-08-21 17:29:36 GMT' in topic
    html = VisibleText(); html.feed((FIXED/source['raw_path']).read_text(encoding='utf-8'))
    assert 'Aug 26, 2026' in html.parts
    relevant = [s for s in html.parts if any(w in s for w in ('August 11', 'SuperGrok', 'Cursor', 'Aug 26, 2026'))]

    authority = {
        'src-1': dict(url=original['locator'], source_class='SOCIAL', title=original['title'],
            published_at=original['published_at'], accessed_at=None,
            role='Discovery-bounded source used for factual verification', supplement=False),
        SID: dict(url=source['locator'], source_class=source['source_class'], title=source['title'],
            published_at=source['published_at'], accessed_at=source['accessed_at'],
            role='Post-Screening exact authority supplement: '+source['relation'], supplement=True),
    }
    # Test-unit seam supplies the two authority rows read above. It is not the
    # production task_authority_sources validator or full supplement closure.
    ns = dict(Path=Path, Any=Any, _nonempty=lambda x:isinstance(x,str) and bool(x.strip()),
        evidence=SimpleNamespace(task_authority_sources=lambda *args:copy.deepcopy(authority)))
    code = FIXED/'scripts/run_evidence_v2_interactive.py'
    node = next(n for n in ast.parse(code.read_text(encoding='utf-8')).body if isinstance(n,ast.FunctionDef) and n.name == '_build_card')
    exec(compile(ast.Module(body=[node],type_ignores=[]), str(code),'exec'), ns)
    compact = read(RUN+'interactive-evidence.json')
    record = next(r for r in compact['records'] if r['discovery_id'] == 'w34-event-c066')
    built = ns['_build_card'](FIXED, task, meta, package, record, compact['runner'])
    assert built == card
    both = copy.deepcopy(record); both['source_bindings'] = ['src-1',SID]
    built_both = ns['_build_card'](FIXED, task, meta, package, both, compact['runner'])
    shared = [r['source_ids'] for field in ('claims','limitations') for r in built_both[field]]
    shared += [r['source_ids'] for r in built_both['verification']['targets']]
    assert all(ids == ['src-1',SID] for ids in shared)

    # Reference-only specimen. Preserve the historical bounded chronology
    # judgment; a failed fresh X fetch is not a reason to overwrite that review.
    # A copied VERIFIED value is NOT a new approval of the corrected Card.
    lab = copy.deepcopy(card)
    social = {k:v for k,v in authority['src-1'].items() if k != 'supplement'}
    social.update(source_id='src-1', accessed_at=daily['imported_at'],
        role='Archived DailyX observation report, exact Drive-returned bytes imported at the stated access time; not original X HTTP content. Repository raw: '+raw_path)
    lab['sources'].append(social)
    lab['claims'][1]['source_ids'] = ['src-1']
    lab['limitations'][0]['source_ids'] = [SID,'src-1']
    lab['verification']['targets'][0]['source_ids'] = [SID,'src-1']
    schema = read('schemas/evidence-v2-card.schema.json')
    jsonschema.Draft202012Validator(schema,format_checker=jsonschema.FormatChecker()).validate(lab)
    assert lab['basis'] == card['basis'] and lab['temporal'] == card['temporal']
    restored = copy.deepcopy(lab)
    restored['sources'] = card['sources']
    restored['claims'][1]['source_ids'] = card['claims'][1]['source_ids']
    restored['limitations'][0]['source_ids'] = card['limitations'][0]['source_ids']
    restored['verification']['targets'][0]['source_ids'] = card['verification']['targets'][0]['source_ids']
    assert restored == card  # all other content and historical decisions unchanged
    def source_check(value):
        sources = {s['source_id']:s for s in value['sources']}
        for key,s in sources.items():
            assert key in authority and s['url'] == authority[key]['url'] and s['source_class'] == authority[key]['source_class']
        for row in value['claims'] + value['limitations'] + value['verification']['targets']:
            assert row['source_ids'] and set(row['source_ids']) <= sources.keys()
    source_check(lab)
    source_check(card)  # admissible sources alone do not establish correct support
    controls = {}
    for label,field,value in [('invented_direct_X_authority','url',x_url),('social_promoted_to_primary','source_class','PRIMARY_OFFICIAL')]:
        bad = copy.deepcopy(lab); bad['sources'][-1][field] = value
        try:source_check(bad)
        except AssertionError:controls[label] = 'REJECTED_BY_LOCAL_BOUND_SOURCE_CHECK'
        else:raise AssertionError(label)
    save(LAB/'card-corrective.lab.json', lab)
    (LAB/'source-excerpts.md').write_bytes(('# Phase 4-F — fixed-source excerpts\n\nHistorical report and captured HTML only; not independent X verification.\n\n## DailyX topic 11\n\n'+topic.strip()+'\n\n## Primary HTML visible text (selected)\n\n'+'\n\n'.join(relevant)+'\n').encode('utf-8'))
    ledger = [json.loads(x) for x in (FIXED/(RUN+'authority-consumption-ledger.jsonl')).read_text(encoding='utf-8').splitlines() if x.strip()]
    row = next(r for r in ledger if r['discovery_id'] == 'w34-event-c066')
    review_path = 'sources/2026-W34/execution/reviews/sol-evidence-authority-consumption-review-20260909-r1.md'
    review = (FIXED/review_path).read_text(encoding='utf-8').split('### Grok Bot chronology',1)[1].split('## Materiality review',1)[0].strip()
    assert review.startswith('PASS with bounded chronology note.')
    bind('Evidence Package -> Profile', package['basis']['profile_path'], package['basis']['profile_sha256'])
    save(LAB/'trace-result.json', dict(scope='ONE_HISTORICAL_SOURCE_JOIN_NOT_FULL_ADMISSION_OR_INDEPENDENT_REVIEW', main=MAIN, edition=HEAD,
        fixed_input_files=len(inputs), exact_bindings=bindings, source_record=original, import_provenance=daily,
        primary_supplement=source, consumption_record=row,
        historical_review=dict(path=review_path, grok_section=review),
        helper_unit=dict(body='_build_card unchanged; pre-resolved authority fixture, not full authority validator',
            actual_compact_reproduces_accepted_card=True, actual_source_bindings=record['source_bindings'],
            both_sources_selected_assigns_both_to_all_statements=True, affected_statement_rows=len(shared)),
        corrective_specimen=dict(path='card-corrective.lab.json', schema='PASS', local_bound_source_check='PASS',
            task_and_package_basis_unchanged=True, all_other_card_content_and_historical_status_preserved=True,
            chronology='Historical bounded PASS preserved, not independently re-established by this trace',
            status='VERIFIED_COPIED_FROM_HISTORICAL_CARD_NOT_NEW_ADMISSION',
            residual='Existing reference to secondary Aug 21 dating is preserved but that separate source was not established by this trace; no whole-Card quality verdict', negative_controls=controls),
        original_x_access=dict(url=x_url, method='web open once during this trace', result='403 Forbidden',
            implication='No original-post bytes obtained; not evidence of deletion or incorrectness'),
        conclusions=['DailyX archived bytes and exact import provenance exist and match the accepted task metadata',
            'The task already permits a SOCIAL Discovery source, but the override selects only the primary supplement',
            'The compact helper applies one source list to all statements; adding DailyX alone does not restore per-statement correspondence',
            'Existing Card fields can represent distinct source bindings without new task/supplement fields; renderer-only repair is insufficient',
            'A historical bounded chronology PASS exists; do not infer mandatory original-X refetch or automatic status downgrade from this probe'],
        limitations=['No independent original X or quoted-post verification', 'No exhaustive search for other production source evidence',
            'No production mutations, acceptance/State/Gate execution or new Human authority',
            'No net lifecycle savings, Special test, PDF or independent review']))
    print('PASS: exact archive/task/supplement bindings; accepted Card reproduced in helper unit; two-source fan-out reproduced; reference-only Card specimen schema/source checks pass')


if __name__ == '__main__':
    main()
