"""Local slice checks, deliberately not Core admission or semantic review."""
import copy
import hashlib
import json
import sys
from pathlib import Path
import jsonschema

LAB = Path(__file__).resolve().parent
ROOT = LAB.parents[1]

def read(path):
    def unique(pairs):
        obj = {}
        for key, value in pairs:
            assert key not in obj, f'duplicate key: {key}'
            obj[key] = value
        return obj
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def schema(value, name, field=None):
    contract = read(LAB/'contracts/schemas'/f'{name}.schema.json')
    if field:
        contract = dict(contract['properties'][field], **{'$defs':contract.get('$defs',{})})
    jsonschema.Draft202012Validator(contract, format_checker=jsonschema.FormatChecker()).validate(value)

def binding(actual, path):
    assert actual == sha(path), f'stale binding: {path.name}'

def resolve(ref, cards):
    card = cards[ref['evidence_task_id']]
    table, key = {'CLAIM':('claims','statement_id'),'METRIC':('metrics','metric_id'),
                  'LIMITATION':('limitations','statement_id'),'EVENT':('events','event_id')}[ref['kind']]
    rows = card['temporal']['events'] if table == 'events' else card[table]
    found = [r for r in rows if r[key] == ref['evidence_id']]
    assert len(found) == 1, f'unresolved evidence: {ref}'
    assert all(found[0][k] == ref[k] for k in ('subject_id','subject_role')), f'wrong subject: {ref}'

def calibrate():
    card = {'claims':[{'statement_id':'q','subject_id':'owner','subject_role':'PRIMARY_SUBJECT'}]}
    ref = {'evidence_task_id':'t','kind':'CLAIM','evidence_id':'q','subject_id':'owner','subject_role':'PRIMARY_SUBJECT'}
    resolve(ref, {'t':card})
    bad = dict(ref, subject_id='neighbor')
    try:
        resolve(bad, {'t':card})
    except AssertionError:
        pass
    else:
        raise AssertionError('calibration missed wrong subject')
    binding(sha(LAB/'protocol.md'), LAB/'protocol.md')
    try:
        binding('0'*64, LAB/'protocol.md')
    except AssertionError:
        pass
    else:
        raise AssertionError('calibration missed stale binding')
    return {'valid_reference':'PASS','wrong_subject':'REJECT','stale_binding':'REJECT'}

def check(version):
    d = LAB/version
    for r in read(LAB/'source-manifest.json')['sources']:
        binding(r['sha256'],ROOT/r['path'])
    for r in read(LAB/'contract-manifest.json')['contracts']:
        binding(r['sha256'],ROOT/r['path'])
    cards = {}
    for cid in ('c1','c2','c3'):
        task, card, view = (read(d/f'{cid}-{k}.json') for k in ('task','card','view'))
        schema(task,'evidence-v2-task')
        schema(card,'evidence-v2-card')
        schema(view,'edition-evidence-view')
        binding(task['screening_basis']['screening_acceptance_sha256'],d/'lab-screening.json')
        for key, path in [('task_sha256',d/f'{cid}-task.json'),('screening_acceptance_sha256',d/'lab-screening.json'),
                          ('prompt_sha256',LAB/'contracts/config/prompts/evidence-verification-v2.md'),
                          ('result_contract_sha256',LAB/'contracts/schemas/evidence-v2-card.schema.json')]:
            binding(card['basis'][key],path)
        binding(view['evidence_sha256'],d/f'{cid}-card.json')
        assert task['evidence_task_id'] == card['evidence_task_id'] == view['evidence_task_id']
        assert set(task['verification_targets']) == {r['target'] for r in card['verification']['targets']}
        entities = {e['entity_id'] for e in card['entities']}
        assert len(entities) == len(card['entities'])
        sources = {s['source_id'] for s in card['sources']}
        assert sources <= {r['source_id'] for r in read(LAB/'source-manifest.json')['sources']}
        ids = []
        for table,key in [('claims','statement_id'),('metrics','metric_id'),('limitations','statement_id'),('events','event_id')]:
            for row in (card['temporal']['events'] if table == 'events' else card[table]):
                ids.append(row[key])
                assert row['subject_id'] in entities
                assert (row['subject_id'] == card['artifact']['primary_subject_id']) == (row['subject_role'] == 'PRIMARY_SUBJECT')
                assert set(row['source_ids']) <= sources
                assert set(row.get('comparison_subject_ids',[])) <= entities
        assert len(ids) == len(set(ids))
        cards[card['evidence_task_id']] = card
    selection = read(d/'selection.lab.json')
    for field in ('assignments','summary'):
        schema(selection[field],'candidate-selection-v2',field)
    assignments = selection['assignments']
    assert {r['candidate_id'] for r in assignments} == {'c1','c2','c3'} and len(assignments) == 3
    counts = {x:sum(r['disposition']==x for r in assignments) for x in {r['disposition'] for r in assignments}}
    assert selection['summary'] == {'candidate_count':3,'disposition_counts':counts,'selected_count':counts.get('SELECTED',0)}
    package = read(d/'package.lab.json')
    for field in ('package','evidence_inputs','drafting_constraints'):
        schema(package[field],'draft-v2-package',field)
    for row in package['evidence_inputs']:
        binding(row['evidence_sha256'],d/(row['candidate_id']+'-card.json'))
        assert row['evidence_card'] == cards[row['evidence_task_id']]
    for usage, field in [('PRIMARY','primary_candidate_ids'),('SUPPORTING','supporting_candidate_ids')]:
        assert set(package['package'][field]) == {r['candidate_id'] for r in assignments if r['architecture_usage']==usage}
    draft = read(d/'draft.json')
    schema(draft,'draft-v2-result')
    binding(draft['basis']['draft_package_sha256'],d/'package.lab.json')
    binding(draft['basis']['prompt_sha256'],LAB/'contracts/config/prompts/article-drafting-v2.md')
    supplied = {r['evidence_task_id']:cards[r['evidence_task_id']] for r in package['evidence_inputs']}
    refs = draft['deck_evidence_refs'] + [r for b in draft['blocks'] for r in b['evidence_refs']]
    for ref in refs:
        resolve(ref,supplied)
    block_ids = {b['block_id'] for b in draft['blocks']}
    assert len(block_ids) == len(draft['blocks'])
    for rows in (draft['must_cover_coverage'],draft['boundary_dispositions']):
        for row in rows:
            assert set(row['block_ids']) <= block_ids
    assert {r['requirement'] for r in draft['must_cover_coverage']} == set(package['package']['must_cover_requirements'])
    assert {r['boundary'] for r in draft['boundary_dispositions']} == set(package['package']['boundaries'])
    manuscript = '# '+draft['headline']+'\n\n'+draft['deck']+'\n\n'+'\n\n'.join(b['text'] for b in draft['blocks'])+'\n'
    assert (d/'manuscript.md').read_text(encoding='utf-8') == manuscript
    return {'version':version,'schema_and_named_bindings':'PASS','canonical_full_package':'NOT_TESTED_LAB_ENVELOPE',
            'semantic_sufficiency':'NOT_A_MECHANICAL_VERDICT','evidence_references':len(refs)}

if __name__ == '__main__':
    print(json.dumps(calibrate() if sys.argv[1]=='--calibrate' else check(sys.argv[1]),ensure_ascii=False))
