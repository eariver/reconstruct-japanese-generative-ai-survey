"""Experimental read-only preflight; not an acceptance or production entrypoint.

Run only against an isolated fixed Core snapshot. Caller must provide exact
package bytes expected from prepare. Core remains the authority for acceptance.
"""
import json


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def check_candidate(root, package_path, candidate_path, expected_package_sha, implementation_sha):
    from scripts import survey_evidence_v2 as evidence
    from scripts import survey_production_v2 as core
    from scripts import survey_schema_v2 as schema

    if core.sha256_file(package_path) != expected_package_sha:
        raise ValueError('prepared package bytes changed')
    package = core.load_json(package_path)
    evidence.validate_evidence_package_basis(root, package_path, package, implementation_sha)
    if candidate_path.is_symlink() or not candidate_path.is_file():
        raise ValueError('candidate must be a regular file')
    card = json.loads(candidate_path.read_text(encoding='utf-8'), object_pairs_hook=reject_duplicate_keys)
    schema.validate_instance(card, root / evidence.CARD_SCHEMA, label='experimental candidate')
    matches = [m for m in package['tasks'] if m['evidence_task_id'] == card['evidence_task_id']]
    if len(matches) != 1:
        raise ValueError('candidate does not identify exactly one package task')
    meta = matches[0]
    task = core.load_json(package_path.parent / meta['path'])
    errors = evidence.validate_evidence_card(card, task, meta['sha256'], package, repo_root=root)
    if errors:
        raise ValueError('; '.join(errors))
    targets = [r['target'] for r in card['verification']['targets']]
    expected = task['verification_targets']
    if len(targets) != len(set(targets)) or set(targets) != set(expected):
        raise ValueError('targets must cover the exact task set once each')
    return card
