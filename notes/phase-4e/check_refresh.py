"""Verify the bounded post-PR488 reality delta without rerunning production."""
import ast
import hashlib
import re
import sys
sys.dont_write_bytecode = True
from author import LAB, ROOT, FIXED, read, save
from probe import verify_inputs


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bib_fields(path):
    entries = {}
    for key, body in re.findall(r'@online\{([^,]+),\n(.*?)\n\}', path.read_text(encoding='utf-8'), re.S):
        entries[key] = {k: v.rstrip(',') for k, v in re.findall(r'^  (\w+) = (.+)$', body, re.M)}
    return entries


def main():
    verify_inputs()
    obs = read(LAB/'production-refresh.json')
    main_root = ROOT/'.phase-4-inputs'/obs['main']
    weekly_root = ROOT/'.phase-4-inputs'/obs['weekly']
    code = 'scripts/survey_weekly_semantic_publication_v2.py'
    def functions(root):
        return {n.name: ast.dump(n, include_attributes=False)
                for n in ast.parse((root/code).read_text(encoding='utf-8')).body if isinstance(n, ast.FunctionDef)}
    old_funcs, new_funcs = functions(FIXED), functions(main_root)
    changed = [name for name in old_funcs if old_funcs[name] != new_funcs[name]]
    assert old_funcs.keys() == new_funcs.keys() and changed == ['_bib_text']
    path = 'surveys/weekly/2026-W34/references.bib'
    before, after = bib_fields(FIXED/path), bib_fields(weekly_root/path)
    assert list(before) == list(after) and len(after) == 41
    assert all({k:v for k,v in row.items() if k != 'note'} == after[key] for key,row in before.items())
    assert all(set(row) == {'title','author','url','urldate'} for row in after.values())
    paths = {r['filename'] for r in obs['weekly_compare']['files']}
    unchanged = ['sources/2026-W34/architecture-v2.json',
        'sources/2026-W34/draft/v2/packages/w34-collaborative-agent-workflows-retrieval/draft-package.json',
        'sources/2026-W34/draft/v2/packages/w34-collaborative-agent-workflows-retrieval/draft-result.json',
        'surveys/weekly/2026-W34/main.tex', 'surveys/weekly/2026-W34/sections/20-agent-workflows.tex',
        'sources/2026-W34/production-state.json']
    assert not (set(unchanged) & paths)
    candidate = read(weekly_root/'sources/2026-W34/publication/v2/publication-candidate-v2.json')
    bindings = []
    for field in ('reader_manuscript','quality_bundle','semantic_review','visual_review'):
        row = candidate[field]; target = weekly_root/row['path']
        assert sha(target) == row['sha256'] and target.stat().st_size == row['byte_count']
        bindings.append(field)
    assert candidate['source']['sha256'] == sha(FIXED/candidate['source']['path'])
    manuscript = read(weekly_root/candidate['reader_manuscript']['path'])
    bib = next(s for s in manuscript['supporting_files'] if s['role'] == 'BIBLIOGRAPHY')
    assert bib['sha256'] == sha(weekly_root/bib['path'])
    section = next(s for s in manuscript['supporting_files'] if s['path'].endswith('/20-agent-workflows.tex'))
    assert section['sha256'] == sha(FIXED/section['path'])
    internal = 'regional processing is NOT part of this package after Selection r2; it belongs to Package 4'
    assert internal in (FIXED/section['path']).read_text(encoding='utf-8')
    semantic = read(weekly_root/candidate['semantic_review']['path'])
    boundary = next(c for c in semantic['checks'] if c['check_id'] == 'PUBLICATION_BOUNDARY')
    assert boundary['status'] == 'PASS' and 'repair history' in boundary['detail']
    save(LAB/'refresh-check.json', dict(scope='SELECTIVE_READ_ONLY_DELTA_NOT_FULL_CANDIDATE_ADMISSION_OR_PDF_REVIEW',
        main=obs['main'], weekly=obs['weekly'], changed_renderer_functions=changed,
        bibliography=dict(entries=41, same_keys_and_order=True, other_field_values_equal=True, internal_notes_remaining=0,
            sha256=sha(weekly_root/path)), unchanged_paths_by_complete_compare=unchanged,
        candidate=dict(status=candidate['status'], candidate_sha256=candidate['candidate_sha256'],
            checked_file_bindings=bindings, pdf_metadata_only=candidate['pdf']),
        current_semantic_boundary=boundary, current_section_internal_note_still_present=True,
        limitations=['No download or visual inspection of PDF', 'No full State/Gate/candidate validation',
            'No inference of Human Preview approval or publication release', 'No independent source review or lifecycle savings measurement']))
    print('PASS refresh: only _bib_text changed; W34 41 keys/order/other fields preserved; candidate 4 file bindings match; internal section note and unchanged upstream inputs remain')


if __name__ == '__main__':
    main()
