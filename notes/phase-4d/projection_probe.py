"""Lab counterfactual only: no production edits, approvals, or quality verdict.

Tests what can be excluded from reader text without deleting canonical facts,
placement constraints or other bibliography fields. Not an unknown-source trial.
"""
import json
import re
import hashlib
from capture import CACHE,HEAD,DEST,save

if __name__=='__main__':
    root=CACHE/HEAD
    bib=(root/'surveys/weekly/2026-W34/references.bib').read_text(encoding='utf-8')
    lines=bib.splitlines(keepends=True)
    removed=[x for x in lines if re.fullmatch(r'  note = \{Core v2 Evidence: (?:VERIFIED|PARTIAL); materiality: MATERIAL\}\n',x)]
    assert len(removed)==41
    after=''.join(x for x in lines if x not in removed)
    def entries(text):
        result={}
        for part in text.split('@online{')[1:]:
            key,body=part.split(',',1)
            result[key]=[line for line in body.splitlines() if not line.startswith('  note = ')]
        return result
    assert entries(bib)==entries(after) and len(entries(after))==41
    draft=json.loads((root/'sources/2026-W34/draft/v2/packages/w34-collaborative-agent-workflows-retrieval/draft-result.json').read_text(encoding='utf-8'))
    package=json.loads((root/'sources/2026-W34/draft/v2/packages/w34-collaborative-agent-workflows-retrieval/draft-package.json').read_text(encoding='utf-8'))
    internal='regional processing is NOT part of this package after Selection r2; it belongs to Package 4'
    boundary=next(b for b in draft['blocks'] if b['block_type']=='CLAIM_BOUNDARY')
    assert package['package']['boundaries'].count(internal)==1
    assert boundary['text'].endswith(' / '+internal)
    projected=boundary['text'][:-len(' / '+internal)]
    assert projected=='この節の読解上の境界: '+' / '.join(x for x in package['package']['boundaries'] if x!=internal)
    before=next(r for r in draft['boundary_dispositions'] if r['boundary']==internal)
    after_disposition=dict(boundary=internal,handling='RESPECTED_BY_OMISSION',block_ids=[],rationale='Lab design only: preserve original Architecture placement constraint; do not publish internal correction history. Placement itself is unchanged.')
    # Use existing Draft Result schema fragment, not a new meaning contract.
    import jsonschema
    contract=json.loads((DEST.parent/'phase-4c/contracts/schemas/draft-v2-result.schema.json').read_text(encoding='utf-8'))
    jsonschema.Draft202012Validator(contract['properties']['boundary_dispositions']['items']).validate(after_disposition)
    save(DEST/'projection-probe.json',dict(scope='STATIC_COUNTERFACTUAL_NOT_ACCEPTED_DRAFT_NOT_PRODUCTION_REPAIR_NOT_SAVINGS_MEASUREMENT',head=HEAD,
        bibliography=dict(input_sha256=hashlib.sha256(bib.encode()).hexdigest(),removed_note_lines=41,remaining_entries=41,all_other_lines_and_fields_preserved=True,projected_sha256=hashlib.sha256(after.encode()).hexdigest()),
        boundary=dict(original_constraint=internal,original_disposition=before,proposed_disposition=after_disposition,other_22_boundary_strings_preserved=True,
            evidence_references_changed=False,architecture_or_placement_changed=False,fragment_schema='PASS'),
        limitations=['No PDF compile/render/visual review','No full canonical candidate emitted or validated','Remaining English boundary text still needs reader-facing authorship/review','Historical approved artifacts are immutable inputs','No comparative lifecycle cost or future quality guarantee']))
    # Keep only an explicitly named lab bibliography sample; original remains immutable.
    (DEST/'bibliography-projection.lab.bib').write_bytes(after.encode('utf-8'))
    print('PASS: 41 internal notes excluded, other bibliography lines preserved; one non-reader placement constraint represented by existing omission disposition; no accepted artifact emitted')
