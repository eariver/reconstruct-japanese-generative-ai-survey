"""Fixed-input function-unit probe, NOT Core/State admission or semantic review.

Only named, inspected functions/constants are extracted from pinned source ASTs.
Imports, CLIs, filesystem writers and authority/Gate execution are not loaded.
The tested Draft Result validator's body is unchanged; its pure IO/hash helpers
are likewise extracted from the fixed Core. This does not exercise its callers.
"""
import ast
import copy
import hashlib
import json
import re
import sys
from datetime import datetime
from types import SimpleNamespace
from typing import Any
from pathlib import Path
import jsonschema

sys.dont_write_bytecode = True
from author import LAB, ROOT, REF, FIXED, PID, PACKAGE, ORIGINAL, read, save

used = set()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extract(name, names, extra=None):
    path = FIXED/'scripts'/name
    used.add('scripts/' + name)
    tree = ast.parse(path.read_text(encoding='utf-8'))
    selected = []
    found = set()
    for node in tree.body:
        label = node.name if isinstance(node, ast.FunctionDef) else (
            node.targets[0].id if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) else None)
        if label in names:
            selected.append(node)
            found.add(label)
    assert found == set(names), (name, found, names)
    ns = dict(Any=Any, Path=Path, datetime=datetime, json=json, hashlib=hashlib, re=re)
    ns.update(extra or {})
    exec(compile(ast.Module(body=selected, type_ignores=[]), str(path), 'exec'), ns)
    return ns


def verify_inputs():
    rows = read(ROOT/'notes/phase-4d/inputs.json') + read(LAB/'inputs.json')
    for row in rows:
        path = ROOT/'.phase-4-inputs'/row['ref']/row['path']
        raw = path.read_bytes()
        assert sha(path) == row['sha256'], row['path']
        assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == row['git_blob_sha1']
    return rows


def main():
    rows = verify_inputs()
    core_names = ['load_json', 'sha256_bytes', 'sha256_file', 'sha256_object']
    core = SimpleNamespace(**extract('survey_production_v2.py', core_names))
    val = extract('survey_drafting_v2_base.py', ['DRAFT_RESULT_FIELDS', 'ATTRIBUTION_MODES', 'BLOCK_TYPES',
        'SUBJECT_ROLES', 'REF_KINDS', 'BOUNDARY_HANDLING', '_nonempty', '_aware', '_card_ref_index',
        '_validate_refs', '_validate_attribution', 'validate_draft_result'], dict(core=core))
    legacy = extract('render_article_draft_tex.py', ['tex_escape', 'cite_key', 'keys_for_refs', 'citation',
        'render_block', 'parse_bullets', 'parse_markdown_table', 'render_table', 'evidence_maps',
        'render_bibliography', 'date_field', 'bib_escape'])
    weekly = extract('survey_weekly_semantic_publication_v2.py', ['_render_tex', '_section_label', '_cite', '_bib_text'],
        dict(core=core, tex_escape=legacy['tex_escape']))
    package, original, draft = read(PACKAGE), read(ORIGINAL), read(LAB/'draft-result.lab.json')
    for path in [PACKAGE, ORIGINAL, FIXED/'schemas/draft-v2-result.schema.json', FIXED/'config/prompts/article-drafting-v2.md']:
        used.add(path.relative_to(FIXED).as_posix())
    validate = lambda d: val['validate_draft_result'](d, PACKAGE, FIXED/'config/prompts/article-drafting-v2.md')
    assert validate(original) == [], validate(original)
    assert validate(draft) == [], validate(draft)
    jsonschema.Draft202012Validator(read(FIXED/'schemas/draft-v2-result.schema.json'),
        format_checker=jsonschema.FormatChecker()).validate(draft)
    assert draft['basis'] == original['basis']
    assert draft['blocks'][:4] == original['blocks'][:4]
    assert draft['deck_evidence_refs'] == original['deck_evidence_refs']
    assert [x['boundary'] for x in draft['boundary_dispositions']] == package['package']['boundaries']
    oldrefs = {json.dumps(r, sort_keys=True) for r in original['blocks'][-1]['evidence_refs']}
    newrefs = {json.dumps(r, sort_keys=True) for b in draft['blocks'][4:] for r in b['evidence_refs']}
    assert newrefs == oldrefs
    controls = {}
    bad = copy.deepcopy(draft); bad['basis']['draft_package_sha256'] = '0'*64
    controls['stale_package_sha'] = validate(bad)
    bad = copy.deepcopy(draft); bad['blocks'][4]['evidence_refs'][0]['subject_id'] = 'wrong-subject'
    controls['wrong_subject'] = validate(bad)
    bad = copy.deepcopy(draft); bad['blocks'][4]['evidence_refs'][0]['evidence_id'] = 'absent-id'
    controls['unknown_evidence_id'] = validate(bad)
    bad = copy.deepcopy(draft); bad['boundary_dispositions'].pop()
    controls['missing_internal_disposition'] = validate(bad)
    bad = copy.deepcopy(draft); bad['boundary_dispositions'][-1]['block_ids'] = [draft['blocks'][0]['block_id']]
    controls['omission_claims_reader_block'] = validate(bad)
    assert all(controls.values())
    # Calibration of the *limit*: a structurally valid denial of the boundary
    # passes this mechanical validator. Never count this as semantic assurance.
    bad = copy.deepcopy(draft); bad['blocks'][4]['text'] = 'すべての数値は独立に再現され、料金と提供範囲にも制約はない。'
    assert validate(bad) == []

    used.update(['sources/2026-W34/architecture-v2.json',
        'sources/2026-W34/draft/v2/interactive-drafting-synthesis-input.json',
        'surveys/weekly/2026-W34/references.bib'])
    architecture = read(FIXED/'sources/2026-W34/architecture-v2.json')
    plan = next(p for p in architecture['packages'] if p['package_id'] == PID)
    archive = read(FIXED/'sources/2026-W34/draft/v2/interactive-drafting-synthesis-input.json')
    spec = next(p for p in archive['packages'] if p['package_id'] == PID)
    # Exercise the same compact-archive text comparison on this package only.
    block_index = {b['block_id']: b for b in draft['blocks'] if b['block_type'] != 'CLAIM_BOUNDARY'}
    assert draft['headline'] == spec['headline'] and draft['deck'] == spec['deck']
    assert all(block_index[b['block_id']]['text'] == b['text'] for b in spec['blocks'])
    dids = set(spec['deck_discovery_ids']) | {d for b in spec['blocks'] for d in b['discovery_ids']}
    keys = {d: 'w2026w34' + re.sub('[^a-zA-Z0-9]', '', d).lower() for d in dids}
    bib = (FIXED/'surveys/weekly/2026-W34/references.bib').read_text(encoding='utf-8')
    bib_entries = {m[0]: m[1] for m in re.findall(r'@online\{([^,]+),\n(.*?)\n\}', bib, re.S)}
    assert set(keys.values()) <= set(bib_entries)
    placeholder = dict(cover=dict(headline='LAB', deck='LAB', anchors=['LAB']),
        frontmatter=dict(heading='LAB', lede='LAB', scope_notes=['LAB']),
        final_summary=dict(heading='LAB', paragraphs=['LAB']))
    try:
        weekly['_render_tex']('2026-W34', 'LAB', 'LAB', placeholder, [(plan, spec, package, draft)], keys)
    except ValueError as exc:
        exact_plan_rejection = str(exc)
        assert 'missing publication section_label' in exact_plan_rejection
    else:
        raise AssertionError('historical plan unexpectedly acquired a section_label')
    # Explicit test fixture ONLY to reach the later block-rendering branch.
    # No modified Architecture file, approval or accepted input is emitted.
    unit_plan = copy.deepcopy(plan)
    unit_plan['publication_extensions']['section_label'] = 'LAB FUNCTION FIXTURE'
    render = lambda d: weekly['_render_tex']('2026-W34', 'LAB', 'LAB', placeholder, [(unit_plan, spec, package, d)], keys)
    tex = render(draft)
    boundary_tex = re.findall(r'\\begin\{claimboundary\}\[Claim boundary\]\n(.*?)\n\\end\{claimboundary\}', tex, re.S)
    assert len(boundary_tex) == 12 and not any('\\cite{' in s or '\\autocite{' in s for s in boundary_tex)
    assert all(legacy['tex_escape'](b['text']) in tex for b in draft['blocks'])
    section = tex[tex.index('% package:'):tex.index('\\clearpage\n\\onecolumn\n\\section{LAB}')]
    (LAB/'weekly-renderer.lab.tex').write_bytes(('% LAB ONLY: function-unit output; no admission or quality verdict\n'+section).encode('utf-8'))
    bad = copy.deepcopy(draft); bad['blocks'][4]['block_type'] = 'NOTE'
    assert validate(bad) == []
    try:
        render(bad)
    except ValueError as exc:
        missing_compact = str(exc)
    else:
        raise AssertionError('expected compact source requirement for the new NOTE block')

    # Existing Card -> row -> source_id resolution, no Discovery URL substitution.
    # This transient dict is a function input, not a new durable authority/store.
    mapping, by_ref = {}, {}
    for item in package['evidence_inputs']:
        card = item['evidence_card']; sources = {s['source_id']: s for s in card['sources']}
        for row in card['limitations']:
            refkey = (item['evidence_task_id'], 'LIMITATION', row['statement_id'])
            assert row['source_ids'] and len(row['source_ids']) == len(set(row['source_ids']))
            mapping[refkey] = [(legacy['cite_key'](sources[s]['url']), sources[s], card.get('artifact', {}).get('organization')) for s in row['source_ids']]
            by_ref[refkey] = row
    source_trace, reuse = [], []
    for b in draft['blocks'][4:]:
        urls, sids = set(), set()
        for r in b['evidence_refs']:
            k = (r['evidence_task_id'], r['kind'], r['evidence_id'])
            assert by_ref[k]['subject_id'] == r['subject_id'] and by_ref[k]['subject_role'] == r['subject_role']
            sids.update(by_ref[k]['source_ids']); urls.update(s['url'] for _, s, _ in mapping[k])
        rendered = legacy['render_block'](b, mapping)
        expected = legacy['keys_for_refs'](b['evidence_refs'], mapping)
        assert legacy['citation'](expected) in rendered and expected
        reuse.append(rendered)
        source_trace.append(dict(block_id=b['block_id'], refs=b['evidence_refs'], source_ids=sorted(sids), urls=sorted(urls), citation_keys=expected))
    (LAB/'existing-block-renderer.lab.tex').write_bytes(('% LAB ONLY: existing render_block with canonical-row mapping; not full legacy renderer or admission\n'+''.join(reuse)).encode('utf-8'))
    all_urls = {url for b in source_trace for url in b['urls']}
    bib_urls = set(re.findall(r'  url = \{([^\n]+)\}', bib))
    assert legacy['evidence_maps'](package) == ({}, {})
    legacy_sources = {key: dict(source=source, organization=org, url=source['url'])
        for values in mapping.values() for key, source, org in values}
    legacy_bib = legacy['render_bibliography'](legacy_sources)
    assert 'Post-Screening exact authority supplement' in legacy_bib
    grok = next(i for i in package['evidence_inputs'] if i['evidence_task_id'].endswith('589f97e8aee10bd1'))
    card = grok['evidence_card']
    timing = next(c for c in card['claims'] if c['statement_id'] == 'claim-2')
    grok_sources = {s['source_id']: s for s in card['sources']}
    timing_urls = [grok_sources[s]['url'] for s in timing['source_ids']]
    assert 'DailyX' in timing['text'] and timing_urls == ['https://x.ai/news/grok-bot-more-plans']
    assert card['temporal']['events'] == []
    grok_trace = dict(evidence_task_id=grok['evidence_task_id'], evidence_sha256=grok['evidence_sha256'],
        claim=timing, resolved_sources=[grok_sources[s] for s in timing['source_ids']],
        temporal=card['temporal'], limitations=card['limitations'],
        conclusion='Timing claim/context names DailyX raw authority, but its source_ids resolve only to edited news-page metadata. No X/DailyX source row or temporal event is in this embedded Card. This does not prove absence of upstream raw evidence.')
    bibcheck = []
    for key, body in bib_entries.items():
        fields = dict(re.findall(r'^  (\w+) = (.+?)(?:,)?$', body, re.M))
        def unwrap(field):
            v = fields[field].rstrip(',')
            return v[2:-2] if v.startswith('{{') else v[1:-1]
        record = dict(entity=dict(canonical_name=unwrap('title'), organization=unwrap('author'), canonical_url=unwrap('url')),
            status='PARTIAL' if 'PARTIAL' in fields['note'] else 'VERIFIED', materiality='MATERIAL')
        before = weekly['_bib_text'](key, record, unwrap('urldate'))
        # Constrained renderer change, not general deletion of arbitrary notes.
        line = f"  note = {{Core v2 Evidence: {record['status']}; materiality: MATERIAL}}\n"
        assert before.count(line) == 1
        after = before.replace(line, '')
        assert after.splitlines() == [s for s in before.splitlines() if s != line.rstrip('\n')]
        bibcheck.append(key)
    assert len(bibcheck) == 41
    selected = [r for r in rows if r['ref'] == REF and r['path'] in used]
    assert {r['path'] for r in selected} == used
    save(LAB/'used-inputs.json', selected)
    save(LAB/'probe-result.json', dict(scope='FUNCTION_UNIT_COMPATIBILITY_ONLY_NOT_CORE_ADMISSION_NOT_SEMANTIC_PASS', ref=REF,
        exact_input_files=len(selected), historical_draft_validator='PASS', lab_full_schema='PASS', lab_draft_validator='PASS',
        preservation=dict(basis=True, original_body_blocks=4, deck_refs=True, distinct_boundary_refs=len(newrefs),
            canonical_boundaries=23, explicit=22, omission=1), negative_controls=controls,
        semantic_negative_control='CONTRADICTORY_WORDING_PASSES_MECHANICAL_VALIDATOR',
        weekly_renderer=dict(compact_archive_text_comparison='PASS', exact_plan_rejection=exact_plan_rejection,
            downstream_branch_fixture='In-memory section_label=LAB FUNCTION FIXTURE; no Architecture/approval file emitted',
            japanese_boundary_blocks=12, boundary_citation_commands=0,
            canonical_note_validates_but_renderer_rejects=missing_compact),
        existing_render_block_reuse=dict(boundary_blocks=12, blocks_with_resolved_citations=12,
            distinct_source_urls=len(all_urls), direct_legacy_evidence_maps='EMPTY_ON_V2_PACKAGE',
            legacy_bibliography='EMITS_INTERNAL_SOURCE_ROLE_NOTE',
            full_legacy_renderer='NOT_COMPATIBLE_WITHOUT_ADAPTATION: primary_evidence/supporting_evidence and claim_id/limitation_id differ; role notes are also emitted'),
        source_trace=source_trace, evidence_urls_absent_from_existing_bibliography=sorted(all_urls-bib_urls),
        chronology_source_join=grok_trace,
        bibliography=dict(existing_entries=41, narrow_template_change_preserves_other_generated_fields=True,
            historical_clean_sample='../phase-4d/bibliography-projection.lab.bib'),
        limitations=['No full Core package/authority closure or CLI execution', 'Historical body carried forward, not source-re-reviewed',
            'Canonical reference resolution is not source sufficiency or correct reader attribution',
            'No PDF compile/visual review, independent review or Special execution', 'No production mutation or net lifecycle saving measurement']))
    print('PASS function-unit assertions; QUALITY PATH NOT ESTABLISHED: 12/12 Weekly boundary blocks lose citations; NOTE requires compact source')
    print('Card source URLs absent from existing bibliography:', sorted(all_urls-bib_urls))


if __name__ == '__main__':
    main()
