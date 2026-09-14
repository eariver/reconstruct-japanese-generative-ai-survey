"""Offline display experiment, not a Core validator or production command.

Only directly requested links are checked. No Git, network, directory search,
approval inference, state transition, reviewed-commit or transitive validation.
"""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from jsonschema import Draft202012Validator, FormatChecker

SCHEMAS = {
    'state': 'survey-production-state.schema.json',
    'profile': 'survey-production-profile.schema.json',
    'stage': 'stage-checkpoint-v2.schema.json',
    'ARCHITECTURE_REVIEW': 'architecture-approval-record-v2.schema.json',
    'PUBLICATION_PREVIEW': 'publication-preview-approval-v2.schema.json',
    'review_index': 'human-gate-review-index-v2.schema.json',
    'review': 'human-gate-review-record-v2.schema.json',
}


def read_link(root, ref, kind, schemas, issue=None, gate=None):
    result = {'reference': ref, 'expected_type': kind}
    try:
        value = ref['path']
        path = PurePosixPath(value)
        if (not isinstance(value, str) or not value or path.is_absolute()
                or any(part in ('.', '..') for part in value.split('/'))
                or '\\' in value or ':' in value):
            raise ValueError('UNSAFE_PATH')
        target = (root / value).resolve()
        if not target.is_relative_to(root.resolve()):
            raise ValueError('UNSAFE_PATH')
        if not re.fullmatch('[0-9a-f]{64}', ref['sha256']):
            raise ValueError('INVALID_DIGEST')
        raw = target.read_bytes()
        if hashlib.sha256(raw).hexdigest() != ref['sha256']:
            raise ValueError('HASH_MISMATCH')
        data = json.loads(raw)
        schema = json.loads((schemas / SCHEMAS[kind]).read_text(encoding='utf-8'))
        errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(data))
        if errors:
            raise ValueError('TYPE_OR_SCHEMA_MISMATCH')
        if issue is not None and data.get('issue_id') != issue:
            raise ValueError('ISSUE_MISMATCH')
        if gate is not None and data.get('gate') != gate:
            raise ValueError('GATE_MISMATCH')
        result['check'] = 'DIRECT_BYTES_SCHEMA_IDENTITY_MATCH'
        return result, data
    except FileNotFoundError:
        result['check'] = 'MISSING'
    except (OSError, ValueError, KeyError, TypeError) as exc:
        result['check'] = str(exc) if isinstance(exc, ValueError) else type(exc).__name__
    return result, None


def inspect(root, state_ref, snapshot_label, schemas, review_index_ref=None):
    result = {
        'snapshot': snapshot_label,
        'scope': 'STORED_FACTS_AND_SELECTED_DIRECT_LINKS_ONLY',
        'execution_admission': 'NOT_EVALUATED',
        'unverified': ['dependency closure', 'current contract compatibility',
                       'reviewed-commit existence/reachability/bytes',
                       'Candidate/PDF and public asset bytes', 'semantic/visual quality'],
    }
    state_check, state = read_link(root, state_ref, 'state', schemas)
    result['state_input'] = state_check
    if state is None:
        result['stored_facts'] = None
        return result
    issue = state['issue_id']
    result['stored_facts'] = {k: state.get(k) for k in (
        'issue_id', 'research_profile', 'publication_profile', 'lifecycle_state',
        'next_action', 'terminal_reason', 'target_gate', 'human_gates')}
    result['state_recorded_implementation'] = state.get('implementation')
    result['state_recorded_contract'] = state.get('contract')
    profile_check, profile = read_link(root, state['profile'], 'profile', schemas, issue)
    if profile is not None:
        if any(profile[k] != state[k] for k in ('research_profile', 'publication_profile')):
            profile_check['check'] = 'PROFILE_KIND_MISMATCH'
        elif not state_ref['path'].startswith(profile['paths']['source_root'].rstrip('/') + '/'):
            profile_check['check'] = 'PROFILE_SOURCE_ROOT_MISMATCH'
        else:
            result['profile_context'] = {
                'paths': profile['paths'],
                'question': profile['research_scope']['question'],
                'temporal_policy': profile['research_scope']['temporal_policy'],
                'remaining_scope': 'Read the exact Profile; inclusion/exclusion/obligations are not summarized here.',
            }
    result['profile_link'] = profile_check
    active = {}
    for key, gate in [('architecture_review', 'ARCHITECTURE_REVIEW'), ('publication_preview', 'PUBLICATION_PREVIEW')]:
        ref = (state.get('human_gate_provenance') or {}).get(key)
        status = state['human_gates'][key]
        if status != 'approved':
            active[key] = {'stored_gate_status': status, 'check': 'NOT_ACTIVE' if ref is None else 'INCONSISTENT_ACTIVE_POINTER'}
        elif ref is None:
            active[key] = {'stored_gate_status': status, 'check': 'MISSING_ACTIVE_POINTER'}
        else:
            check, approval = read_link(root, ref, gate, schemas, issue, gate)
            active[key] = check
            if approval is not None:
                active[key]['stored_approval'] = {k: approval.get(k) for k in ('decision', 'review_reference', 'publication_candidate_path', 'publication_candidate_sha256', 'pdf_path', 'pdf_sha256') if k in approval}
    result['active_approval_links'] = active
    result['selected_checkpoint_links'] = {}
    for key, kind in [('release', 'stage'), ('publication_preview', 'PUBLICATION_PREVIEW')]:
        ref = state.get('checkpoint_provenance', {}).get(key)
        if ref is not None:
            check, checkpoint = read_link(root, ref, kind, schemas, issue)
            if checkpoint is not None and key == 'release' and (checkpoint['from_state'], checkpoint['to_state']) != ('FROZEN', 'RELEASED'):
                check['check'] = 'STAGE_EDGE_MISMATCH'
            result['selected_checkpoint_links'][key] = check
    if review_index_ref is not None:
        index_check, index = read_link(root, review_index_ref, 'review_index', schemas, issue)
        result['historical_review_index'] = index_check
        result['latest_recorded_reviews_not_active_authority'] = []
        if index is not None:
            for gate in ('ARCHITECTURE_REVIEW', 'PUBLICATION_PREVIEW'):
                rows = [r for r in index['reviews'] if r['gate'] == gate]
                if not rows:
                    continue
                revisions = sorted(r['revision'] for r in rows)
                if revisions != list(range(1, len(rows) + 1)):
                    index_check['check'] = 'NONCONTIGUOUS_OR_DUPLICATE_REVISIONS'
                    continue
                row = max(rows, key=lambda r: r['revision'])
                check, review = read_link(root, row['record'], 'review', schemas, issue, gate)
                if review is not None and (review['revision'], review['decision']) != (row['revision'], row['decision']):
                    check['check'] = 'INDEX_RECORD_MISMATCH'
                    review = None
                item = {'gate': gate, 'link': check, 'role': 'HISTORICAL_RECORD_NOT_ACTIVE_APPROVAL'}
                if review is not None:
                    item['stored_review'] = {k: review[k] for k in ('revision', 'decision', 'regeneration_boundary', 'requested_changes', 'reviewed_repository_commit_sha', 'approval')}
                result['latest_recorded_reviews_not_active_authority'].append(item)
    return result
