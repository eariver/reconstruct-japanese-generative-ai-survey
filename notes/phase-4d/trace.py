"""Non-executing, bounded identity/content trace of fixed production artifacts."""
import hashlib
import json
from datetime import datetime, timezone
from capture import CACHE,DEST,HEAD,MAIN,save

P='sources/2026-W34/'
PID='w34-collaborative-agent-workflows-retrieval'
def raw(path,ref=HEAD): return (CACHE/ref/path).read_bytes()
def obj(path,ref=HEAD): return json.loads(raw(path,ref))
def sha(path,ref=HEAD): return hashlib.sha256(raw(path,ref)).hexdigest()
def excerpt(path,needle,ref=HEAD):
    lines=raw(path,ref).decode('utf-8').splitlines()
    return [dict(line=i+1,text=s) for i,s in enumerate(lines) if needle in s]

if __name__=='__main__':
    checks=[]
    for row in json.loads((DEST/'inputs.json').read_text(encoding='utf-8')):
        b=raw(row['path'],row['ref'])
        assert hashlib.sha256(b).hexdigest()==row['sha256']
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob_sha1']
    state=obj(P+'production-state.json')
    cp_path=state['checkpoint_provenance']['validation']['path']
    assert sha(cp_path)==state['checkpoint_provenance']['validation']['sha256']; checks.append('State -> validation checkpoint')
    cp=obj(cp_path)
    selected_names={'semantic-review','reader-manuscript','visual-review','validated-source'}
    for row in cp['artifacts']:
        if row['name'] in selected_names:
            assert sha(row['path'])==row['sha256']; checks.append('Checkpoint -> '+row['name'])
    manuscript=obj(P+'publication/v2/reader-manuscript-v2.json')
    for row in [manuscript['primary_source']]+manuscript['supporting_files']:
        if (CACHE/HEAD/row['path']).exists():
            assert sha(row['path'])==row['sha256']; checks.append('Reader manifest -> '+row['path'])
    package_path=P+'draft/v2/packages/'+PID+'/draft-package.json'
    result_path=P+'draft/v2/packages/'+PID+'/draft-result.json'
    package=obj(package_path); result=obj(result_path)
    assert result['basis']['draft_package_sha256']==sha(package_path);checks.append('Draft -> Package')
    for field,path in [('architecture_sha256',P+'architecture-v2.json'),('architecture_review_summary_sha256',P+'architecture-review-summary-v2.json')]:
        assert package['basis'][field]==sha(path);checks.append('Package -> '+path)
    architecture=obj(P+'architecture-v2.json')
    planned=next(r for r in architecture['packages'] if r['package_id']==PID)
    assert package['package']['boundaries']==planned['boundaries']; checks.append('Architecture -> exact package boundaries')
    archive=obj(P+'draft/v2/interactive-drafting-synthesis-input.json')
    spec=next(r for r in archive['packages'] if r['package_id']==PID)
    content=[b for b in result['blocks'] if b['block_type']!='CLAIM_BOUNDARY']
    assert [(r['block_id'],r['text']) for r in spec['blocks']]==[(r['block_id'],r['text']) for r in content]
    assert all(spec[k]==result[k] for k in ['headline','deck']);checks.append('Authored archive -> exact draft prose')
    boundaries=[r for r in result['blocks'] if r['block_type']=='CLAIM_BOUNDARY']
    assert len(boundaries)==1
    expected='この節の読解上の境界: '+' / '.join(planned['boundaries'])
    assert boundaries[0]['text']==expected;checks.append('Boundary = automatic full Architecture concatenation')
    section='surveys/weekly/2026-W34/sections/20-agent-workflows.tex'
    assert expected in raw(section).decode('utf-8');checks.append('Exact generated boundary -> publication TeX')
    leak=planned['boundaries'][-1]
    assert 'Selection r2' in leak and 'Package 4' in leak
    bib='surveys/weekly/2026-W34/references.bib'
    notes=excerpt(bib,'note = ')
    assert len(notes)==41 and all('Core v2 Evidence:' in r['text'] and 'materiality: MATERIAL' in r['text'] for r in notes)
    review=obj(P+'publication/v2/semantic-editorial-review-v2.json')
    boundary_check=next(r for r in review['checks'] if r['check_id']=='PUBLICATION_BOUNDARY')
    bib_check=next(r for r in review['checks'] if r['check_id']=='BIBLIOGRAPHY_METADATA')
    jobs=json.loads((DEST/'ci-run.json').read_text(encoding='utf-8'))
    runs=json.loads((DEST/'ci-related-runs.json').read_text(encoding='utf-8'))
    dt=lambda s:datetime.fromisoformat(s.replace('Z','+00:00'))
    spans=[dict(id=r['id'],head_sha=r['head_sha'],conclusion=r['conclusion'],wall_seconds=(dt(r['updated_at'])-dt(r['run_started_at'])).total_seconds()) for r in runs]
    save(DEST/'trace.json',dict(scope='STATIC_SELECTED_CHAIN_NOT_FULL_CORE_OR_PUBLICATION_REVIEW',head=HEAD,main=MAIN,
        named_binding_checks=checks,package_id=PID,source_question=package['package']['purpose'],
        archive=dict(package_count=len(archive['packages']),runner=archive['runner'],selected_content_blocks=len(content),exact_authored_content_copy=True),
        automatic_boundary=dict(count=len(planned['boundaries']),internal_placement_instruction=leak,exact_architecture_package_draft_tex_match=True,
            dispositions=result['boundary_dispositions'],prose_not_regenerated_by_entry_runner=True),
        bibliography=dict(entry_count=len(notes),note_patterns={s:sum(r['text']==s for r in notes) for s in sorted({r['text'] for r in notes})},first_line=notes[0]['line'],last_line=notes[-1]['line'],
            renderer=excerpt('scripts/survey_weekly_semantic_publication_v2.py','note = ',MAIN)),
        review=dict(recorded_by=review['reviewed_by'],recorded_at=review['recorded_at'],publication_boundary=boundary_check,bibliography=bib_check,
            bibliography_bound_by_reader_manifest=True,bibliography_explicitly_in_review_locations=False,
            independent_postdraft_review_not_established_by_these_records=True),
        runtime=dict(worklog_report='~4h sequential runner (unverified duration/allocation)',entry_call='agent wrapper -> interactive existing semantic input -> per-package derive/validate -> synthesis',
            measured_rerun=False,model_call_in_inspected_entry=False,ci_run_spans=spans,final_compile_step=next(s for j in jobs['jobs'] for s in j['steps'] if s['name']=='Compile weekly issue with LuaLaTeX'),
            authored_runner_timestamp_later_than_committed_output=True,active_time=None,tokens=None,total_lifecycle_cost=None),
        source_scope='No new primary-source factual audit, no PDF inspection, no sidecar re-execution, no production mutation',
        observed_at=datetime.now(timezone.utc).isoformat()))
    print(json.dumps({'named_binding_checks':len(checks),'input_archive_blocks':len(content),'auto_boundaries':len(planned['boundaries']),'bib_notes':len(notes),'ci_spans':spans},ensure_ascii=False))
