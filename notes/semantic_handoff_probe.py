"""Read-only fixed-ref helpers for the semantic handoff feasibility investigation.

No production imports, validators, generation, Git fetch, or ref changes.
Cache is disposable and outside both repositories. stdout is caller-selected.
"""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

REPO = 'D:/Git/japanese-generative-ai-survey'
MAIN = '6d748a962d57beff89da7c1b20cb5a9a86c8e261'
W34 = '030eb723c12282f0cfd09aaada05d14f0c0906c7'
SPECIAL = '1b19a98511f9717d04b3b8f95207599fcdb7f48d'
CACHE = Path(tempfile.gettempdir()) / 'astra-semantic-handoff-fixed-ref-cache'

def read(path, ref=MAIN):
    assert len(ref) == 40 and all(c in '0123456789abcdef' for c in ref)
    key = hashlib.sha256((ref + ':' + path).encode()).hexdigest()
    cached = CACHE / key
    if cached.exists():
        return cached.read_bytes()
    result = subprocess.run(['git', '-C', REPO, 'show', f'{ref}:{path}'], capture_output=True)
    if result.returncode:
        data = subprocess.check_output(['gh', 'api',
            f'repos/eariver/japanese-generative-ai-survey/contents/{path}?ref={ref}',
            '-H', 'Accept: application/vnd.github.raw+json'])
    else:
        data = result.stdout
    CACHE.mkdir(exist_ok=True)
    cached.write_bytes(data)
    return data

def txt(path, ref=MAIN):
    return read(path, ref).decode('utf-8-sig')

def obj(path, ref=MAIN):
    return json.loads(txt(path, ref))

def rows(path, ref=MAIN):
    return [json.loads(line) for line in txt(path, ref).splitlines() if line.strip()]

def functions(path, names=(), ref=MAIN):
    source = txt(path, ref)
    lines = source.splitlines()
    for node in ast.parse(source).body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and (not names or node.name in names):
            if not names:
                print(f'{node.lineno}-{node.end_lineno}: {node.name}')
            else:
                print('\n'.join(f'{i+1}: {lines[i]}' for i in range(node.lineno-1, node.end_lineno)))

def emit(value):
    print(json.dumps(value, ensure_ascii=False, indent=2))

def audit_samples():
    """Check persisted bytes/joins only; not Core validation or acceptance."""
    import html
    import re
    report = {'scope': 'ANALYSIS_ONLY_NOT_CORE_VALIDATION', 'refs': {
        'main': MAIN, 'weekly': W34, 'special': SPECIAL}, 'samples': []}
    for issue, ref, dids in [
        ('2026-W34', W34, ['w34-event-c019', 'w34-event-arxiv-2608-14927', 'w34-event-c033']),
        ('SP001', SPECIAL, ['SP001-D008']),
    ]:
        ledger = obj(f'sources/{issue}/materiality-ledger-v2.json', ref)
        ep = f"sources/{issue}/evidence/v2/accepted/{ledger['basis']['evidence_set_sha256']}"
        vp = f"sources/{issue}/evidence/v2/views/accepted/{ledger['basis']['edition_view_set_sha256']}"
        package = obj(ep + '/package.json', ref)
        acceptance = obj(ep + '/evidence-accepted.json', ref)
        va = obj(vp + '/edition-views-accepted.json', ref)
        for did in dids:
            metas = [m for m in package['tasks'] if did in m['discovery_ids']]
            assert len(metas) == 1
            meta = metas[0]
            task_id = meta['evidence_task_id']
            filename = meta['path'].split('/')[-1]
            tp, cp = ep + '/tasks/' + filename, ep + '/results/' + filename
            vpath = vp + '/views/view-' + hashlib.sha256(task_id.encode()).hexdigest()[:20] + '.json'
            task, card, view = obj(tp, ref), obj(cp, ref), obj(vpath, ref)
            entry = next(r for r in acceptance['results'] if r['evidence_task_id'] == task_id)
            ve = next(r for r in va['views'] if r['evidence_task_id'] == task_id)
            digest = lambda path: hashlib.sha256(read(path, ref)).hexdigest()
            checks = {
                'package_hash_matches_acceptance': digest(ep+'/package.json') == acceptance['package_sha256'],
                'task_hash_matches_package_and_card': digest(tp) == meta['sha256'] == card['basis']['task_sha256'],
                'card_hash_matches_acceptance_and_view': digest(cp) == entry['sha256'] == view['evidence_sha256'],
                'view_hash_matches_view_acceptance': digest(vpath) == ve['view_sha256'],
                'same_edition_task': card['issue_id'] == view['issue_id'] == issue and card['evidence_task_id'] == view['evidence_task_id'] == task_id,
            }
            out = {'discovery_id': did, 'task_id': task_id, 'paths': {'task': tp, 'card': cp, 'view': vpath},
                   'card_sha256': digest(cp), 'status': card['status'], 'materiality': view['materiality'],
                   'checks': checks}
            if issue == '2026-W34':
                b = 'sources/2026-W34/execution/luna/w34-screening-evidence-after-sol-discovery-r2/'
                record = next(r for r in obj(ep+'/interactive-evidence.json',ref)['records'] if r['discovery_id']==did)
                details = next(r for r in rows(b+'evidence-consumption-details.jsonl',ref) if r['discovery_id']==did)
                consumption = next(r for r in rows(b+'authority-consumption-ledger.jsonl',ref) if r['discovery_id']==did)
                checks['claims_text_class_context_preserved_from_input'] = record['claims'] == [
                    {k:r[k] for k in ('text','evidence_class','context')} for r in card['claims']]
                checks['materiality_rationale_preserved_in_view'] = record['materiality_rationale'] == view['materiality']['rationale']
                supplement = obj(package['authority_supplement']['path'],ref)
                checks['supplement_hash_matches_package'] = digest(package['authority_supplement']['path']) == package['authority_supplement']['sha256']
                entries = [s for s in supplement['sources'] if s['discovery_id']==did]
                out['sources'] = [{'id':s['supplement_source_id'], 'path':s['raw_path'], 'sha256':s['raw_sha256'],
                    'exact_raw_hash_and_size_match': digest(s['raw_path']) == s['raw_sha256'] and len(read(s['raw_path'],ref))==s['byte_count']} for s in entries]
                out['consumption_state'] = consumption['consumption_state']
                out['detail_keys'] = list(details)
                out['target_characters'] = {'task':len(task['verification_targets'][0]),'ledger':len(consumption['verification_target'])}
                if did == 'w34-event-arxiv-2608-14927':
                    raw = read(entries[0]['raw_path'],ref).decode('utf-8', errors='replace')
                    # Independent reproduction of only the documented text-normalization step.
                    text = re.sub(r'(?is)<(script|style|noscript|svg|nav|footer|header)\b.*?</\1\s*>', ' ', raw)
                    text = re.sub(r'(?s)<[^>]+>', ' ', text)
                    text = re.sub(r'\s+', ' ', html.unescape(text)).strip()
                    out['paper_observations'] = {
                        'normalized_characters_before_cap':len(text), 'cap':60000,
                        'normalized_line_count':len(text[:60000].split('\n')),
                        'method_claim':card['claims'][0]['text'],
                        'ui_phrase_in_method_claim':'Content selection saved.' in card['claims'][0]['text'],
                        'ui_phrase_in_raw_hidden_modal':bool(re.search(r'<p[^>]*hidden[^>]*>Content selection saved\.',raw)),
                        'raw_has_section_7':bool(re.search(r'<section[^>]*id="S7"',raw)),
                        'detail_method_span_count':len(details['method_spans']),
                        'detail_method_span_3':details['method_spans'][2],
                        'verification_statuses':[r['status'] for r in card['verification']['targets']],
                    }
            else:
                matrix = obj('sources/SP001/candidate-matrix-v2.json',ref)
                mr = next(r for r in matrix['rows'] if r['evidence_task_id']==task_id)
                sel = obj('sources/SP001/candidate-selection-v2.json',ref)
                sr = next(r for r in sel['assignments'] if r['candidate_id']==mr['candidate_id'])
                checks['profile_annotations_preserved_through_selection'] = view['profile_annotations'] == mr['profile_extensions'] == sr['profile_extensions']
                checks['matrix_points_to_exact_card_and_view'] = mr['evidence_sha256']==digest(cp) and mr['edition_view_sha256']==digest(vpath)
                out['raw_refs'] = task['source_records'][0]['raw_paths']
                out['claim_equals_discovery_summary'] = card['claims'][0]['text']==task['source_records'][0]['summary_text']
                out['unresolved_questions'] = card['verification']['unresolved_questions']
                out['selection_rationale'] = sr['rationale']
                out['as_of'] = obj('sources/SP001/production-profile.json',ref)['research_scope']['temporal_policy']
            report['samples'].append(out)
    return report

if __name__ == '__main__':
    emit(audit_samples())
