"""LAB section derivation attempt, stopped at metadata ambiguity. Never Core admission.

Uses the historical Package and Phase 4-E Draft; the planned separate repair is not run.
Only inspected pure TeX helpers are loaded from production; no CLI or writer.
"""
import ast
import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any
import jsonschema

ROOT = Path(__file__).resolve().parents[2]
LAB = Path(__file__).resolve().parent
CACHE = ROOT/'.phase-4-inputs'
MAIN = '14781409f6fb8d79e3eb4ad6b4c457764a038fde'
HEAD = '8480f4dfffb57b456d1147fcc5360f7864bb19df'
OLD = 'c1703f772837317b81735cd4cc851c715fff1a3b'
PREFIX = 'sources/2026-W34/'
PID = 'w34-collaborative-agent-workflows-retrieval'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode('utf-8'))


def helpers():
    names = {'tex_escape', 'bib_escape', 'cite_key', 'keys_for_refs', 'citation',
             'parse_bullets', 'parse_markdown_table', 'render_table', 'render_block', 'date_field'}
    path = CACHE/MAIN/'scripts/render_article_draft_tex.py'
    nodes = [n for n in ast.parse(path.read_text(encoding='utf-8')).body
             if isinstance(n, ast.FunctionDef) and n.name in names]
    assert len(nodes) == len(names)
    namespace = dict(Any=Any, re=re, hashlib=hashlib)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), namespace)
    return namespace


def index_cards(cards):
    index = {}
    for card in cards:
        sources = {}
        for source in card['sources']:
            if source['source_id'] in sources:
                raise ValueError('duplicate source identity')
            sources[source['source_id']] = source
        fields = [('claims', 'CLAIM', 'statement_id'), ('limitations', 'LIMITATION', 'statement_id'),
                  ('metrics', 'METRIC', 'metric_id')]
        groups = [(card.get(field, []), kind, identity) for field, kind, identity in fields]
        groups.append((card['temporal']['events'], 'EVENT', 'event_id'))
        for rows, kind, identity in groups:
            for row in rows:
                key = (card['evidence_task_id'], kind, row[identity])
                if key in index:
                    raise ValueError('duplicate statement identity')
                selected = row['source_ids']
                if not selected or len(selected) != len(set(selected)) or any(s not in sources for s in selected):
                    raise ValueError('invalid statement source binding')
                index[key] = (row, [sources[s] for s in selected])
    return index


def derive(draft, cards, fn):
    """Transient v2 map, exact refs only. Returned outputs have no authority."""
    index = index_cards(cards)
    mapping, cited, trace = {}, {}, []
    def bind(refs, location):
        for ref in refs:
            key = (ref['evidence_task_id'], ref['kind'], ref['evidence_id'])
            if key not in index:
                raise ValueError('unknown Evidence ref')
            row, sources = index[key]
            if any(ref[k] != row[k] for k in ('subject_id', 'subject_role')):
                raise ValueError('subject mismatch')
            values = []
            for source in sources:
                key_url = fn['cite_key'](source['url'])
                # Never select a winner silently for conflicting source metadata.
                public = {k: source.get(k) for k in ('title', 'url', 'published_at', 'accessed_at', 'source_class')}
                if key_url in cited and cited[key_url] != public:
                    failure = ValueError('conflicting citation metadata')
                    failure.detail = {'location': location, 'later_ref': ref, 'earlier_metadata': cited[key_url], 'later_metadata': public, 'earlier_refs': [entry['ref'] for entry in trace if any(item['url'] == source['url'] for item in entry['sources'])]}
                    raise failure
                cited[key_url] = public
                values.append((key_url, source, None))
            mapping[key] = values
            trace.append({'location': location, 'ref': ref, 'statement': row, 'sources': sources})
    bind(draft['deck_evidence_refs'], 'deck')
    for block in draft['blocks']:
        bind(block['evidence_refs'], block['block_id'])
    block_tex = {}
    for original in draft['blocks']:
        block = copy.deepcopy(original)
        # Explicit LAB style: canonical NOTE becomes a plain cited paragraph.
        # No claim of official profile layout compatibility.
        if block['block_type'] == 'NOTE':
            block['block_type'] = 'PARAGRAPH'
        if block['block_type'] == 'HEADING' and block['evidence_refs']:
            raise ValueError('heading citations unsupported by reused renderer')
        block_tex[block['block_id']] = fn['render_block'](block, mapping)
    tex = ('% LAB ONLY: no publication approval or full quality review\n'
           + '\\section{' + fn['tex_escape'](draft['headline']) + '}\n'
           + fn['tex_escape'](draft['deck'])
           + fn['citation'](fn['keys_for_refs'](draft['deck_evidence_refs'], mapping)) + '\n'
           + ''.join(block_tex.values()))
    # Bibliography is deliberately a limited LAB display projection. Full source
    # class/role/context remain in the trace, not blindly copied as internal notes.
    entries = []
    for key, source in sorted(cited.items()):
        fields = [f"  title = {{{fn['bib_escape'](source['title'])}}}", f"  url = {{{source['url']}}}"]
        for field, value in [('date', source['published_at']), ('urldate', source['accessed_at'])]:
            if fn['date_field'](value):
                fields.append(f"  {field} = {{{fn['date_field'](value)}}}")
        entries.append('@online{'+key+',\n'+',\n'.join(fields)+'\n}\n')
    return {'tex': tex, 'bib': '\n'.join(entries), 'blocks': block_tex, 'trace': trace, 'cited': cited}


def main():
    manifest = read(LAB/'inputs.json')
    reused = []
    required = {(OLD, PREFIX+f'draft/v2/packages/{PID}/draft-package.json'),
                (MAIN, 'schemas/draft-v2-result.schema.json')}
    for phase in ['phase-4d', 'phase-4g']:
        reused += [r for r in read(ROOT/'notes'/phase/'inputs.json') if (r['ref'], r['path']) in required]
    assert len(reused) == len(required)
    for row in manifest+reused:
        raw = (CACHE/row['ref']/row['path']).read_bytes()
        assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
        assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest() == row['git_blob_sha1']
    package_path = CACHE/OLD/PREFIX/f'draft/v2/packages/{PID}/draft-package.json'
    package = read(package_path)
    draft_path = ROOT/'notes/phase-4e/draft-result.lab.json'
    draft = read(draft_path)
    assert draft['basis']['draft_package_sha256'] == sha(package_path)
    schema = read(CACHE/MAIN/'schemas/draft-v2-result.schema.json')
    jsonschema.validate(draft, schema)
    cards = [i['evidence_card'] for i in package['evidence_inputs']]
    fn = helpers()
    original_hashes = {'package': sha(package_path), 'draft': sha(draft_path)}
    try:
        derive(draft, cards, fn)
    except ValueError as exc:
        assert str(exc) == 'conflicting citation metadata', str(exc)
        conflict = exc.detail
    else:
        raise AssertionError('Expected known URL metadata ambiguity was not detected')
    assert original_hashes == {'package': sha(package_path), 'draft': sha(draft_path)}
    assert conflict['earlier_metadata']['url'] == conflict['later_metadata']['url']
    differences = [k for k in conflict['earlier_metadata'] if conflict['earlier_metadata'][k] != conflict['later_metadata'][k]]
    assert set(differences) == {'title', 'published_at', 'accessed_at'}
    save(LAB/'probe-result.json', {
        'scope': 'BOUNDED_CONSUMER_ATTEMPT_STOPPED_AT_METADATA_AMBIGUITY',
        'status': 'EXPECTED_COUNTEREXAMPLE_REPRODUCED_NOT_PUBLICATION_PASS',
        'reused_inputs': reused,
        'lab_inputs': {'notes/phase-4e/draft-result.lab.json': sha(draft_path)},
        'phase4e_package_binding_pass': True,
        'draft_schema_pass': True,
        'conflict': conflict,
        'differing_fields': differences,
        'guard_origin': 'LAB conservative guard against first-wins URL deduplication, not a production Core rule',
        'production_defect_asserted': False,
        'repair_witness': 'NOT_RUN: bounded stop condition reached before initial section output',
        'not_run': ['Complete section/TeX/Bib output', 'Separate 4-F source repair fixture', 'Core or State admission',
                    'Independent review', 'PDF/visual QA', 'Special execution', 'All-role cost comparison'],
        'input_hashes_unchanged': True,
    })
    print('PASS as counterexample: same URL has different title/publication/access metadata. Section and repair not completed; no quality/admission PASS.')


if __name__ == '__main__':
    main()
