"""Bind B3 design closeout without changing candidate or prior evidence."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
FIX=Path('/tmp/jgas-rephase-freeze-b1b2')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def git(*args):
    return subprocess.check_output(['git',*args],cwd=FIX).decode().strip()


def main():
    previous=load(HERE.parent/'rephase-1-freeze/closeout.json')
    for row in previous['evidence']:
        assert sha(ROOT/row['path'])==row['sha256'],row['path']
    manifest=load(HERE.parent/'rephase-1-freeze/candidate.json')
    assert git('rev-parse','HEAD')==manifest['candidate_head']
    assert git('rev-parse','HEAD^{tree}')==manifest['candidate_tree']
    assert not git('diff','--name-only') and not git('diff','--cached','--name-only')
    assert git('remote','get-url','origin')==manifest['origin']
    assert not (FIX/'.git/objects/info/alternates').exists()
    for row in manifest['files']:
        assert sha(FIX/row['path'])==row['sha256']
    probe=load(HERE/'probe-results.json')
    for row in probe['inputs']:
        assert sha(FIX/row['path'])==row['sha256']
    rows=probe['mutation_matrix']
    assert len(rows)==12 and sum(r['current_projection_unchanged'] for r in rows)==10
    assert all(r['tex_changed'] and r['prototype_envelope_changes'] for r in rows)
    initial=load(HERE/'auditor/input-hashes.json')
    initial_hashes={r['path']:r['sha256'] for r in initial['design_inputs']}
    assert sha(HERE/'probe-initial.py')==initial_hashes['probe.py']
    assert sha(HERE/'probe-results-initial.json')==initial_hashes['probe-results.json']
    assert sha(HERE/'worker-analysis.md')==initial_hashes['worker-analysis.md']
    # Reconstruct the initial decision text from the two recorded paragraph edits,
    # and authenticate it against the independently captured original hash.
    current=(HERE/'contract-decision.md').read_text()
    addition=' The stage must pass its exact selected Reader Manuscript path/hash into Gate validation (or an equivalent schema-bound authority): require one matching MANUSCRIPT_MANIFEST and matching primary-source path/hash. A valid Gate for a different same-issue/Profile manuscript is insufficient. Cover both DRAFT_COMPLETE and inherited VALIDATED_DRAFT callers.'
    regression=' a Gate for another same-issue/Profile manuscript fails at both stage callers; malformed structured JSON fails schema validation rather than being silently skipped;'
    assert addition in current and regression in current
    original=current.replace(addition,'').replace(regression,'')
    assert hashlib.sha256(original.encode()).hexdigest()==initial_hashes['contract-decision.md']
    (HERE/'contract-decision-initial.md').write_text(original)
    assert (HERE/'resolution-auditor/review.md').is_file()
    resolution=load(HERE/'resolution-auditor/input-hashes.json')
    audited={row['path']:row['sha256'] for row in resolution['reconstruct_inputs']}
    for name in ['probe.py','probe-results.json','contract-decision.md']:
        key=str((HERE/name).relative_to(ROOT))
        assert sha(HERE/name)==audited[key],key
    docs=[ROOT/'AGENTS.md',ROOT/'README.md',ROOT/'handoff/rephase-1-continuation.md',
          ROOT/'outputs/rephase-1-reader-boundary-assessment.md',HERE/'README.md',HERE/'contract-decision.md']
    links=0
    for doc in docs:
        for link in re.findall(r'\]\(([^)]+)\)',doc.read_text(encoding='utf-8-sig')):
            if '://' in link or link.startswith('#'): continue
            target=(doc.parent/link.split('#')[0]).resolve()
            assert target.exists() or target==(HERE/'closeout.json').resolve(),(doc,link)
            links+=1
    artifacts=[dict(path=str(p.relative_to(ROOT)),sha256=sha(p)) for p in sorted(HERE.rglob('*'))
               if p.is_file() and p.name!='closeout.json']
    final=dict(candidate_head=manifest['candidate_head'],candidate_unchanged=True,
        disposition='B3_OPEN_DESIGN_BOUNDARY_COMPLETE_NOT_READY',
        candidate_implementation=False,canonical_seven_point_audit=False,
        mutations=12,unprojected_output_mutations=10,covered_controls=2,
        prior_freeze_evidence_verified=len(previous['evidence']),candidate_files_verified=len(manifest['files']),
        initial_auditor_report_preserved=True,
        initial_decision_reconstructed_and_hash_verified=True,
        resolution_review='separate fresh-context independent check, not implementation acceptance',
        exact_corrected_design_and_probe_inputs_verified=True,
        local_links_checked=links,evidence=artifacts,
        production_mutation=False,production_adoption=False)
    (HERE/'closeout.json').write_text(json.dumps(final,indent=2)+'\n')
    print(json.dumps({k:v for k,v in final.items() if k!='evidence'},indent=2))


if __name__=='__main__':
    main()
