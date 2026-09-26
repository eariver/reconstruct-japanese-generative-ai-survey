#!/usr/bin/env python3
"""Generate reviewed Core v2 Draft Results and Profile Synthesis from a compact agent input.

The compact input addresses factual material by Discovery ID. This runner derives the
self-contained Draft Packages from the approved Architecture, resolves stable Evidence
references from those packages, validates every Draft Result, builds the canonical
Profile Synthesis Input, validates the Synthesis Result, and archives the exact semantic
input. It never advances Production State.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from scripts import survey_agent_control_v2 as agent
from scripts import survey_drafting_v2 as drafting
from scripts import survey_drafting_citation_refs_v2 as citation_refs
from scripts import survey_production_v2 as core


def _load(path: Path) -> dict[str, Any]:
    return core.load_json(path)


def _rel(root: Path, path: Path) -> str:
    return str(path.resolve().relative_to(root.resolve())).replace('\\', '/')


def _screening_path(root: Path, source_root: Path) -> Path:
    attention=_load(source_root/'architecture-review-attention-v2.json')
    raw=attention.get('basis',{}).get('screening_acceptance_path')
    if not isinstance(raw,str) or not raw:
        raise ValueError('Architecture Review Attention missing screening_acceptance_path')
    path=(root/raw).resolve()
    path.relative_to(root)
    if not path.is_file():
        raise ValueError('screening acceptance path missing')
    return path


def _upstream(root: Path, state_path: Path) -> dict[str, Path]:
    state=_load(state_path)
    if state.get('lifecycle_state') != 'ARCHITECTURE_ESTABLISHED':
        raise ValueError('interactive Drafting requires ARCHITECTURE_ESTABLISHED State')
    if state.get('human_gates',{}).get('architecture_review') != 'approved':
        raise ValueError('interactive Drafting requires approved Architecture Review')
    cfg = _load(root / core.DEFAULT_CONFIG)
    state_errors = agent.validate_agent_state(root, cfg, state)
    if state_errors:
        raise ValueError('Production State invalid before interactive Drafting: ' + '; '.join(state_errors))
    profile_path=root/state['profile']['path']
    profile=_load(profile_path)
    source_root=root/profile['paths']['source_root']
    discovery_acceptance=source_root/'discovery/discovery-accepted-v2.json'
    accepted=_load(discovery_acceptance)
    raw_discovery=accepted.get('discovery_path')
    if not isinstance(raw_discovery,str) or not raw_discovery:
        raise ValueError('Discovery Acceptance missing discovery_path')
    discovery_path=(root/raw_discovery).resolve()
    discovery_path.relative_to(root)
    if not discovery_path.is_file():
        raise ValueError('accepted Discovery JSONL missing')
    matrix_path=source_root/'candidate-matrix-v2.json'
    matrix=_load(matrix_path)
    active = agent.resolve_active_evidence_views(root, cfg, state)
    evidence_path = active['evidence_path']
    views_path = active['views_path']
    if matrix.get('basis', {}).get('evidence_acceptance_sha256') != core.sha256_file(evidence_path):
        raise ValueError('Candidate Matrix does not bind checkpoint-bound Evidence acceptance')
    if matrix.get('basis', {}).get('edition_views_acceptance_sha256') != core.sha256_file(views_path):
        raise ValueError('Candidate Matrix does not bind checkpoint-bound Edition Views acceptance')
    approval_ref=state.get('human_gate_provenance',{}).get('architecture_review')
    if not isinstance(approval_ref,dict) or not isinstance(approval_ref.get('path'),str):
        raise ValueError('Architecture approval provenance missing')
    approval_path=root/approval_ref['path']
    return {
        'state': state_path,
        'profile': profile_path,
        'source_root': source_root,
        'discovery': discovery_path,
        'screening': _screening_path(root, source_root),
        'evidence': evidence_path,
        'views': views_path,
        'ledger': source_root/'materiality-ledger-v2.json',
        'completeness': source_root/'profile-completeness-v2.json',
        'matrix': matrix_path,
        'selection': source_root/'candidate-selection-v2.json',
        'architecture': source_root/'architecture-v2.json',
        'review': source_root/'architecture-review-summary-v2.json',
        'approval': approval_path,
    }


def _ref_rows(card: dict[str,Any], task_id: str, mode: str) -> list[dict[str,Any]]:
    return citation_refs.ref_rows(card, task_id, mode)


def _refs(package: dict[str,Any], discovery_ids: list[str], mode: str) -> list[dict[str,Any]]:
    return citation_refs.refs(package, discovery_ids, mode)


def _classes(package: dict[str,Any], refs: list[dict[str,Any]]) -> set[str]:
    index=drafting._card_ref_index(package)
    values=set()
    for ref in refs:
        values.add(index[(ref['evidence_task_id'],ref['kind'],ref['evidence_id'])][2] or 'PRIMARY_FACT')
    return values


def _attribution(package: dict[str,Any], refs: list[dict[str,Any]]) -> str:
    if not refs: return 'NONE'
    classes=_classes(package, refs)
    if 'SOCIAL_OBSERVATION' in classes: return 'SOCIAL' if classes == {'SOCIAL_OBSERVATION'} else 'MIXED'
    if 'INFERENCE' in classes: return 'INFERENCE' if classes == {'INFERENCE'} else 'MIXED'
    claimed={'VENDOR_CLAIM','PROJECT_CLAIM','AUTHOR_CLAIM'}
    if classes & claimed: return 'ATTRIBUTED' if classes <= claimed else 'MIXED'
    return 'FACTUAL'


def _draft_result(root: Path, package_path: Path, package: dict[str,Any], spec: dict[str,Any], runner: dict[str,Any], draft_version: str) -> dict[str,Any]:
    deck_refs=_refs(package, spec['deck_discovery_ids'], spec.get('deck_ref_mode','CLAIMS'))
    blocks=[]
    for row in spec['blocks']:
        mode=row.get('ref_mode','CLAIMS')
        refs=_refs(package, row.get('discovery_ids',[]), mode) if mode != 'NONE' else []
        blocks.append({'block_id':row['block_id'],'block_type':row['block_type'],'text':row['text'],'attribution_mode':_attribution(package,refs),'evidence_refs':refs})
    boundary_id=f'{package["package_id"]}-boundaries'
    boundary_refs=[]
    for item in package['evidence_inputs']:
        boundary_refs.extend(_ref_rows(item['evidence_card'],item['evidence_task_id'],'LIMITATIONS'))
    if boundary_refs:
        blocks.append({'block_id':boundary_id,'block_type':'CLAIM_BOUNDARY','text':'この節の読解上の境界: ' + ' / '.join(package['package']['boundaries']),'attribution_mode':_attribution(package,boundary_refs),'evidence_refs':boundary_refs})
    else:
        blocks.append({'block_id':boundary_id,'block_type':'CLAIM_BOUNDARY','text':'この節の読解上の境界: ' + ' / '.join(package['package']['boundaries']),'attribution_mode':'NONE','evidence_refs':[]})
    content_ids=[row['block_id'] for row in blocks if row['block_type'] != 'HEADING']
    result={
        'schema_version':'2.0-rc1','issue_id':package['issue_id'],'research_profile':package['research_profile'],'publication_profile':package['publication_profile'],'package_id':package['package_id'],
        'draft_version':draft_version,'status':'ESTABLISHED',
        'basis':{'draft_package_sha256':core.sha256_file(package_path),'prompt_id':'article-drafting-v2','prompt_sha256':core.sha256_file(root/drafting.DRAFT_PROMPT)},
        'runner':runner,'headline':spec['headline'],'deck':spec['deck'],'deck_attribution_mode':_attribution(package,deck_refs),'deck_evidence_refs':deck_refs,'blocks':blocks,
        'must_cover_coverage':[{'requirement':req,'block_ids':content_ids} for req in package['package']['must_cover_requirements']],
        'boundary_dispositions':[{'boundary':boundary,'handling':'EXPLICITLY_STATED','block_ids':[boundary_id],'rationale':'Approved Architecture boundary is preserved explicitly in the Draft Result.'} for boundary in package['package']['boundaries']],
        'profile_extensions':package['profile_extensions'],'publication_extensions':package['publication_extensions'],
    }
    return result


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo-root',default='.')
    ap.add_argument('--state',required=True)
    ap.add_argument('--input',required=True)
    args=ap.parse_args()
    root=Path(args.repo_root).resolve(); state_path=(root/args.state).resolve(); input_path=(root/args.input).resolve()
    data=_load(input_path); up=_upstream(root,state_path); state=_load(state_path)
    if data.get('schema_version')!='2.0-rc1' or data.get('issue_id')!=state['issue_id']:
        raise SystemExit('interactive Drafting input identity mismatch')
    if set(data) != {'schema_version','issue_id','draft_version','runner','packages','synthesis'}:
        raise SystemExit('interactive Drafting input envelope invalid')
    plan=_load(up['architecture']); specs=data['packages']
    if {row['package_id'] for row in specs} != {row['package_id'] for row in plan['packages']}:
        raise SystemExit('interactive Drafting must cover every Architecture package exactly once')
    spec_by_id={row['package_id']:row for row in specs}
    draft_root=up['source_root']/'draft/v2'; pairs=[]; outputs=[]
    implementation_sha=core.repository_commit_sha(root)
    for plan_row in sorted(plan['packages'],key=lambda r:(r['drafting_order'],r['package_id'])):
        pid=plan_row['package_id']; spec=spec_by_id[pid]
        if set(spec) != {'package_id','headline','deck','deck_discovery_ids','blocks'}:
            raise SystemExit(f'interactive package fields invalid: {pid}')
        package=drafting.derive_draft_package(root,up['profile'],up['discovery'],up['screening'],up['evidence'],up['views'],up['ledger'],up['completeness'],up['matrix'],up['selection'],up['architecture'],up['review'],up['approval'],pid,implementation_sha)
        package_dir=draft_root/'packages'/pid; package_path=package_dir/'draft-package.json'; result_path=package_dir/'draft-result.json'
        if package_path.exists() or result_path.exists(): raise SystemExit(f'refusing existing Draft artifacts: {pid}')
        core.write_json(package_path,package)
        result=_draft_result(root,package_path,package,spec,data['runner'],data['draft_version'])
        errors=drafting.validate_draft_result(result,package_path,root/drafting.DRAFT_PROMPT)
        if errors: raise SystemExit(f'{pid} Draft Result invalid: ' + '; '.join(errors))
        core.write_json(result_path,result); pairs.append((package_path,result_path)); outputs.append({'package_id':pid,'package':_rel(root,package_path),'result':_rel(root,result_path)})
    synthesis_input=drafting.build_synthesis_input(root,up['profile'],up['architecture'],up['review'],up['approval'],pairs)
    synthesis_input_path=draft_root/'profile-synthesis-input.json'; synthesis_result_path=draft_root/'profile-synthesis-result.json'
    core.write_json(synthesis_input_path,synthesis_input)
    syn=data['synthesis']
    if set(syn) != {'profile_payload','publication_payload'}: raise SystemExit('interactive synthesis fields invalid')
    synthesis_result={
        'schema_version':'2.0-rc1','issue_id':state['issue_id'],'research_profile':state['research_profile'],'publication_profile':state['publication_profile'],'synthesis_version':'v1.0','status':'ESTABLISHED',
        'basis':{'synthesis_input_sha256':core.sha256_file(synthesis_input_path),'prompt_id':'profile-synthesis-v2','prompt_sha256':core.sha256_file(root/drafting.SYNTHESIS_PROMPT)},
        'runner':data['runner'],'profile_payload':syn['profile_payload'],'publication_payload':syn['publication_payload'],
    }
    errors=drafting.validate_synthesis_result(synthesis_result,synthesis_input_path,root/drafting.SYNTHESIS_PROMPT)
    if errors: raise SystemExit('Profile Synthesis Result invalid: ' + '; '.join(errors))
    core.write_json(synthesis_result_path,synthesis_result)
    archive=draft_root/'interactive-drafting-synthesis-input.json'
    if archive.exists(): raise SystemExit('refusing existing interactive Drafting archive')
    core.write_json(archive,data)
    print(json.dumps({'packages':outputs,'synthesis_input':_rel(root,synthesis_input_path),'synthesis_result':_rel(root,synthesis_result_path),'archive':_rel(root,archive)},ensure_ascii=False,indent=2))
    return 0


if __name__=='__main__':
    raise SystemExit(main())
