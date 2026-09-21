"""Read-only f1 source: bounded B3 coverage and derivation design experiment.

This is not a production validator, a candidate patch, or semantic approval.
The full render-input envelope deliberately exposes the cost of binding internal
metadata along with reader prose. Do not install this prototype wholesale.
"""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SOURCE = Path('/tmp/jgas-rephase-freeze-b1b2')
HEAD = 'bf32edf98ba8f605169d7188bbc764de74ee4f6e'
sys.path.insert(0, str(SOURCE))
from scripts import survey_production_v2 as core
from scripts import survey_reader_surface_gate_v2 as gate
from scripts import survey_weekly_semantic_publication_v2 as weekly


def sha(value):
    return hashlib.sha256(value).hexdigest()


def digest(value):
    return core.sha256_object(value)


def git(*args):
    return subprocess.check_output(['git',*args],cwd=SOURCE).decode().strip()


def args_fixture():
    return dict(issue_id='2026-W35', display_date='2026-09-14', boundary='Weekly window',
        publication={
            'cover':{'headline':'Systems','deck':'Weekly developments','anchors':['Tools']},
            'frontmatter':{'heading':'Overview','lede':'Reader introduction.',
                          'scope_notes':['Public evidence only.']},
            'final_summary':{'heading':'Summary','paragraphs':['Weekly conclusion.']}},
        ordered=[[{'package_id':'PKG-1','publication_extensions':{'section_label':'Research'}},
                  {'headline':'Inference','deck':'Serving performance.',
                   'deck_discovery_ids':['D1'],
                   'blocks':[{'block_id':'B1','text':'Measured latency improved.', 'discovery_ids':['D1']}]},
                  {},
                  {'package_id':'PKG-1','headline':'Inference','deck':'Serving performance.',
                   'blocks':[{'block_id':'B1','block_type':'PARAGRAPH','text':'Measured latency improved.',
                              'attribution_mode':'PRIMARY_SOURCE'},
                             {'block_id':'BOUNDARY','block_type':'CLAIM_BOUNDARY','text':'Limited to measured cases.',
                              'attribution_mode':'PRIMARY_SOURCE'}]}]],
        bib_key_by_did={'D1':'sourceone'})


def emitted_texts(a):
    """Explicit read-set projection for this fixed renderer, not a TeX parser."""
    p = a['publication']
    texts = dict(issue_id=a['issue_id'],display_date=a['display_date'],boundary=a['boundary'],
                 cover=p['cover'],frontmatter=p['frontmatter'],final_summary=p['final_summary'])
    texts['packages'] = [dict(headline=r['headline'],deck=r['deck'],
        section_label=weekly._section_label(plan),blocks=[b['text'] for b in r['blocks']])
        for plan,spec,package,r in a['ordered']]
    return copy.deepcopy(texts)


def old_projection(a, output):
    p = a['publication']
    packages = [dict(package_id=plan['package_id'],headline=spec['headline'],deck=spec['deck'],
                     blocks=[dict(block_id=b['block_id'],text=b['text']) for b in spec['blocks']])
                for plan,spec,package,result in a['ordered']]
    gate.build_weekly_reader_surface_input(SOURCE,a['issue_id'],'WEEKLY_MAGAZINE',
        'Weekly conclusion.',p['final_summary']['paragraphs'],packages,
        headline=p['cover']['headline'],deck=p['cover']['deck'],output_path=output)
    return sha(output.read_bytes())


RENDERER_SHA = sha((SOURCE/'scripts/survey_weekly_semantic_publication_v2.py').read_bytes())


def envelope(a):
    return dict(kind='PROTOTYPE_WEEKLY_COMPLETE_RENDER_INPUT',renderer_sha256=RENDERER_SHA,
                render_input=copy.deepcopy(a),reader_fields=emitted_texts(a))


def verify(reviewed_digest, payload, actual_primary):
    # Caller-supplied exact-source hashes do not authorize different output.
    if digest(payload) != reviewed_digest:
        raise ValueError('reviewed input bytes changed')
    if payload['renderer_sha256'] != RENDERER_SHA:
        raise ValueError('renderer identity changed')
    if payload['reader_fields'] != emitted_texts(payload['render_input']):
        raise ValueError('reader projection is incomplete or inconsistent')
    expected = weekly._render_tex(**payload['render_input']).encode('utf-8')
    if expected != actual_primary:
        raise ValueError('current primary source is not derived from reviewed input')


def rejection(fn):
    try:
        fn()
    except ValueError as exc:
        return str(exc)
    raise AssertionError('expected rejection')


def mutate(a, field):
    p=a['publication']
    if field=='cover.anchors': p['cover']['anchors'][0]='Hardware'
    elif field=='frontmatter.heading': p['frontmatter']['heading']='Introduction'
    elif field=='frontmatter.lede': p['frontmatter']['lede']='A changed introduction.'
    elif field=='frontmatter.scope_notes': p['frontmatter']['scope_notes'][0]='Different evidence scope.'
    elif field=='final_summary.heading': p['final_summary']['heading']='Conclusions'
    elif field=='package.section_label': a['ordered'][0][0]['publication_extensions']['section_label']='Tools'
    elif field=='result.claim_boundary': a['ordered'][0][3]['blocks'][1]['text']='New restrictions apply.'
    elif field=='display_date': a['display_date']='2026-09-15'
    elif field=='window_boundary': a['boundary']='A different research window'
    elif field=='citation_key': a['bib_key_by_did']['D1']='sourcetwo'
    elif field=='covered_control.cover.headline': p['cover']['headline']='Changed systems'
    elif field=='covered_control.summary.paragraph': p['final_summary']['paragraphs'][0]='A different conclusion.'
    else: raise AssertionError(field)


def main():
    assert git('rev-parse','HEAD') == HEAD
    assert not git('diff','--name-only') and not git('diff','--cached','--name-only')
    paths = ['scripts/survey_weekly_semantic_publication_v2.py',
             'scripts/survey_reader_surface_gate_v2.py',
             'schemas/reader-surface-input-v2.schema.json']
    inputs=[]
    for path in paths:
        data=(SOURCE/path).read_bytes()
        committed=subprocess.check_output(['git','show',f'{HEAD}:{path}'],cwd=SOURCE)
        assert data==committed
        inputs.append(dict(path=path,sha256=sha(data)))
    base=args_fixture()
    tex=weekly._render_tex(**base).encode('utf-8')
    bound=envelope(base)
    reviewed=digest(bound)  # synthetic review identity, no semantic judgment
    verify(reviewed,bound,tex)
    rows=[]
    with tempfile.TemporaryDirectory(prefix='jgas-b3-design-') as temp:
        out=Path(temp)/'surface.json'
        initial=old_projection(base,out)
        fields=['cover.anchors','frontmatter.heading','frontmatter.lede','frontmatter.scope_notes',
                'final_summary.heading','package.section_label','result.claim_boundary',
                'display_date','window_boundary','citation_key',
                'covered_control.cover.headline','covered_control.summary.paragraph']
        for field in fields:
            changed=copy.deepcopy(base)
            mutate(changed,field)
            altered=weekly._render_tex(**changed).encode('utf-8')
            same=old_projection(changed,out)==initial
            assert altered!=tex
            assert same == (not field.startswith('covered_control'))
            assert digest(envelope(changed))!=reviewed
            rows.append(dict(field=field,current_projection_unchanged=same,tex_changed=True,
                prototype_envelope_changes=True,
                stale_review_output_rejection=rejection(lambda:verify(reviewed,bound,altered))))
    incomplete=copy.deepcopy(bound)
    incomplete['reader_fields']['frontmatter'].pop('lede')
    # Even a fresh digest does not permit an incomplete claimed projection.
    incomplete_rejection=rejection(lambda:verify(digest(incomplete),incomplete,tex))
    forged=copy.deepcopy(bound)
    forged['render_input']['publication']['frontmatter']['lede']='Substituted input'
    changed_input_rejection=rejection(lambda:verify(reviewed,forged,tex))
    internal=copy.deepcopy(base)
    internal['ordered'][0][3]['internal_validation_note']='Changed internal annotation'
    internal_tex=weekly._render_tex(**internal).encode('utf-8')
    assert emitted_texts(internal)==emitted_texts(base)
    assert internal_tex!=tex and digest(envelope(internal))!=reviewed
    result=dict(candidate_read_only=HEAD,production_baseline='774dd39a951c9ac3818e83dfffd4c7666efb0a20',
        scope='FUNCTION_DESIGN_EXPERIMENT_NOT_CANDIDATE_REPAIR_OR_SEMANTIC_APPROVAL',
        inputs=inputs,mutation_matrix=rows,
        prototype_controls=dict(matching_render_accepted=True,incomplete_projection_rejection=incomplete_rejection,
                                changed_input_rejection=changed_input_rejection),
        known_cost=dict(internal_annotation_changes_review_digest=True,reader_prose_unchanged=True,
                       tex_comment_changes=True,note='Full render-input envelope overbinds internal result metadata; do not ship as the final reader IR.'),
        limits=['One synthetic package; not a validated edition or publisher CLI',
                'Primary TeX only; bibliography/style/support closure not demonstrated',
                'No Special/Retrospective renderer experiment',
                'No actual semantic/Human review, stage transition or publication',
                'The prototype does not modify or replace the current Gate'])
    assert git('rev-parse','HEAD')==HEAD and not git('diff','--name-only')
    (HERE/'probe-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
