"""Reconstruct r1 from its saved patch, then make bounded r2 edits. No Git."""
import difflib
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PRIOR = HERE.parent / 'rephase-1-contract'
REF = '774dd39a951c9ac3818e83dfffd4c7666efb0a20'
SOURCE = ROOT / '.rephase-1-inputs' / REF
TARGET = ROOT / '.rephase-1-inputs/contract-candidate-r2'


def apply_patch(originals, patch):
    result, path, old, out, cursor = {}, None, [], [], 0
    for line in patch.splitlines(True):
        if line.startswith('--- a/'):
            if path is not None:
                result[path] = ''.join(out + old[cursor:])
            path = line[6:].strip()
            old, out, cursor = originals[path].splitlines(True), [], 0
        elif line.startswith('+++ b/'):
            assert line[6:].strip() == path
        elif line.startswith('@@ '):
            start = int(re.match(r'@@ -(\d+)', line)[1]) - 1
            assert start >= cursor
            out.extend(old[cursor:start]); cursor = start
        elif line.startswith((' ', '-')):
            assert old[cursor] == line[1:], (path, cursor)
            cursor += 1
            if line[0] == ' ':
                out.append(line[1:])
        elif line.startswith('+'):
            out.append(line[1:])
        else:
            raise AssertionError(line)
    if path is not None:
        result[path] = ''.join(out + old[cursor:])
    return result


def change(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new)


def build():
    manifest = json.loads((PRIOR / 'candidate-files.json').read_text(encoding='utf-8'))
    originals = {}
    for row in manifest:
        raw = (SOURCE / row['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row['baseline_sha256']
        originals[row['path']] = raw.decode('utf-8').replace('\r\n', '\n')
    proposed = apply_patch(originals, (PRIOR / 'candidate.patch').read_text(encoding='utf-8'))
    for row in manifest:
        assert hashlib.sha256(proposed[row['path']].encode()).hexdigest() == row['proposed_sha256']
    r1 = proposed.copy()
    prefix = 'docs/survey-production-core-v2-'
    path = prefix + 'authority.md'
    proposed[path] = change(proposed[path], 'Frozen/released editions remain immutable.',
        'Released editions remain immutable. Frozen Candidate authority remains subject to the existing Freeze/Release rules; this index does not prohibit an authorized lifecycle advance.')
    path = prefix + 'session-bootstrap.md'
    proposed[path] = change(proposed[path], 'do not reconcile or update duplicated current values in Markdown.',
        'do not maintain duplicate live values in the authority index or execution navigation index. Continue required version-bound session/review records and Human review presentations; repair a misleading handoff before using it.')
    path = prefix + 'execution-record-policy.md'
    proposed[path] = change(proposed[path], '- start-of-run reviewed baseline, start/objective/requested stop, explicitly historical run context;',
        '- start-of-run reviewed baseline, start/requested stop and a pointer to the initial session objective, explicitly historical run context;')
    proposed[path] = change(proposed[path], '- pointers to Grok/X task/result disposition and execution-mode/transport records when applicable;',
        '- pointers to each session\'s execution mode/transport record, and Grok/X task/result disposition when applicable;')
    proposed[path] = change(proposed[path], 'A machine review index names historical rN records;',
        'Resolve the machine review index path from the reviewed Core configuration relative to the Profile source root. It may not exist before the first decision; absence is not approval. Pending Human review targets remain in the required version-bound session/review presentation and State-bound stage artifacts, and are not inferred from an old approval. A machine review index names historical rN records;')
    path = 'scripts/survey_execution_record_v2.py'
    proposed[path] = change(proposed[path], '- Run started: `{started_utc}`\n- Requested stop: `{requested_stop}`',
        '- Run started: `{started_utc}`\n- Initial requested stop (historical): `{requested_stop}`\n- Initial objective: see `sessions/{session_id}.md`, Starting authority.\n- Execution mode/transport: see each session\'s Deterministic execution transport section.')
    proposed[path] = change(proposed[path], "- Machine review history: `{profile['paths']['source_root']}/gates/review-index.json`",
        "- Machine review history path, relative to `{profile['paths']['source_root']}`: `{cfg.get('state_authority', {}).get('human_review_index_path', 'NOT_CONFIGURED')}`\n- Before the first decision, the history may be absent; absence or NOT_CONFIGURED is not approval.\n- Pending review target: follow the version-bound session/review presentation and State-bound stage artifacts; do not infer it from an old approval.")
    proposed[path] = change(proposed[path], '## Deviations / failures\n\n- None recorded yet.',
        '## Deterministic execution transport\n\n- Record this session\'s actual execution mode. For bridge execution, retain the distinct request, reviewed commit, executor and receipt references required by execution-record policy section 5.\n- Mode and transport evidence are not inferred from initialization.\n\n## Deviations / failures\n\n- None recorded yet.')
    diffs, delta, stats = [], [], []
    for path, after in proposed.items():
        target = TARGET / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(after, encoding='utf-8', newline='\n')
        diffs.extend(difflib.unified_diff(originals[path].splitlines(True), after.splitlines(True), fromfile='a/' + path, tofile='b/' + path))
        delta.extend(difflib.unified_diff(r1[path].splitlines(True), after.splitlines(True), fromfile='r1/' + path, tofile='r2/' + path))
        stats.append(dict(path=path, baseline_sha256=hashlib.sha256((SOURCE / path).read_bytes()).hexdigest(), r1_sha256=hashlib.sha256(r1[path].encode()).hexdigest(), proposed_sha256=hashlib.sha256(after.encode()).hexdigest()))
    (HERE / 'candidate.patch').write_text(''.join(diffs), encoding='utf-8', newline='\n')
    (HERE / 'r1-to-r2.patch').write_text(''.join(delta), encoding='utf-8', newline='\n')
    (HERE / 'candidate-files.json').write_text(json.dumps(stats, indent=2) + '\n', encoding='utf-8')
    assert apply_patch(originals, ''.join(diffs)) == proposed
    return stats


if __name__ == '__main__':
    print(json.dumps(build(), indent=2))
