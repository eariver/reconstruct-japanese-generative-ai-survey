"""Produce a five-file proposal with difflib; no Git or production writes."""
import difflib
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REF = '774dd39a951c9ac3818e83dfffd4c7666efb0a20'
SOURCE = ROOT / '.rephase-1-inputs' / REF
CANDIDATE = ROOT / '.rephase-1-inputs/contract-candidate'
PREFIX = 'docs/survey-production-core-v2-'
HISTORY = f'https://github.com/eariver/japanese-generative-ai-survey/blob/{REF}/'


def section(text, heading, replacement):
    start = text.index(heading)
    end = text.find('\n## ', start + len(heading))
    return text[:start] + replacement.rstrip() + '\n' + (text[end:] if end >= 0 else '')


def replace(text, old, new):
    assert text.count(old) == 1, old[:100]
    return text.replace(old, new)


def build():
    manifests = {r['path']: r for r in json.loads((HERE / 'inputs.json').read_text(encoding='utf-8'))}
    originals, proposed = {}, {}
    paths = [PREFIX + name + '.md' for name in ('authority', 'redesign-authority', 'session-bootstrap', 'execution-record-policy')]
    paths += ['scripts/survey_execution_record_v2.py']
    for path in paths:
        raw = (SOURCE / path).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == manifests[path]['sha256']
        originals[path] = raw.decode('utf-8').replace('\r\n', '\n')

    path = paths[0]
    t = originals[path]
    t = t[:t.index('Status:')] + '''Status: `CANONICAL CORE OPERATING RULE INDEX`
Established: 2026-08-22 JST
Final-audit rule: `docs/survey-production-core-v2-final-audit-rule.md`
Mandatory research/review governance: `docs/survey-production-core-v2-sol-luna-review-governance.md`

''' + t[t.index('## 1.'):]
    t = section(t, '## 1.', f'''## 1. Purpose and evidence boundary

This index states operating rules. It does not track the current main SHA, maintenance branch/PR status, edition lifecycle, or candidate acceptance status. Resolve those facts from the explicitly identified repository snapshot, canonical Profile/State and typed gate/checkpoint records, or the named maintenance PR/review record. Missing evidence remains unknown; do not infer approval from implementation or from a document's status label.

[The prior status and audit history]({HISTORY}{path}) is immutable historical context, not current operating status or reusable approval. Repository facts outrank stale summaries; they do not waive qualitative review or Human authority.

Any new Core candidate tree follows the fixed-head audit invalidation discipline. Exact final PASS evidence belongs in PR/Human-review metadata keyed to one unchanged candidate SHA; do not mutate the candidate merely to record that PASS.
''')
    # Keep every document-map destination and rule section; retire volatile labels only.
    t = t.replace('## 4. Current document map', '## 4. Document responsibility map')
    t = t.replace('| Document | Current status | Role |', '| Document | Document classification (not acceptance status) | Role |')
    t = t.replace('`CANONICAL PRE-AUDIT WORK STATUS`', '`MAINTENANCE WORK RECORD`')
    t = t.replace('`ACTIVE CONSOLIDATED PLAN / REPAIRS IMPLEMENTED`', '`DESIGN AND ROLLOUT PLAN`')
    t = t.replace('`ACTIVE MACHINE-READABLE AUDIT EVIDENCE`', '`FINDING AND REPAIR RECORDS`')
    t = section(t, '## 11.', f'''## 11. Finding disposition evidence

Finding status belongs to the named Finding/Repair Set and exact maintenance candidate review, not a copied current list here. [Historical dispositions and deferrals]({HISTORY}{path}#11-finding-disposition) remain evidence; moving their status out of this index neither reopens deferred work nor certifies any repair.

The machine Series engine and exhaustive synthetic future-edition matrix are not introduced by this change. Current scoped validation requirements and the generic Profile boundaries in sections 6 and 12 remain effective.
''')
    old = t[t.index('PR #310,'):t.index('Once Authority,')]
    t = replace(t, old, '''Frozen/released editions remain immutable. Active edition sessions do not edit shared Core in place. A Core candidate must name its production scope and keep edition mutation separately authorized; neither a branch name nor an implementation summary implies adoption or approval.

Edition status and candidate acceptance are read from their named machine/review authority. Previously recorded W33/W34/SP001/SP002/SP003 and maintenance-PR status is historical context available in the linked prior version, not a current work order.

''')
    proposed[path] = t

    path = paths[1]
    t = originals[path]
    start, end = t.index('Status:'), t.index('## 1.')
    t = t[:start] + 'Status: `CORE REDESIGN OPERATING CONSTRAINTS`\nEstablished: 2026-08-23 JST\n\n' + t[end:]
    start, end = t.index('Historical maintenance candidates'), t.index('Before PR #447')
    t = t[:start] + f'''Historical maintenance candidates and PASS results are not reusable after mutation. [The prior candidate/finding chronology]({HISTORY}{path}#14-acceptance-status) is retained as historical evidence. This document does not track a pending maintenance candidate or assert current acceptance.

''' + t[end:]
    t = t.replace('Before PR #447 may return to Human full-candidate review:', 'Before a new Core candidate may be presented for Human full-candidate review:')
    proposed[path] = t

    path = paths[2]
    t = originals[path]
    t = replace(t, '9. current Profile/State/review index/execution index if resuming.', '9. canonical Profile/State and typed checkpoint/active-approval pointers, the machine review index, and the execution navigation index if resuming.')
    t = replace(t, 'Repository state outranks chat history.', '''Repository state outranks chat history. Read lifecycle/next action, active approvals and Candidate pointers from the named snapshot's machine records; do not reconcile or update duplicated current values in Markdown. An execution index supplies run context and navigation, not current machine facts. Its historical session summaries remain tied to their recorded State/commit.

The authority index, redesign constraints, governance and applicable detailed policies above remain required. This change does not retire their substantive reading obligations or the independent reviews. A snapshot display is not a full State/contract/reviewed-commit validation or permission to execute.''')
    t = replace(t, 'Maintain `{source_root}/execution/index.md`, concise session records, review summaries, defect records, request/receipt pointers when bridge transport is used, and current Human-review rN authority.', '''Maintain `{source_root}/execution/index.md` as a run-context/navigation file under execution-record policy section 4. Do not copy live lifecycle, State hash, Gate status, Candidate/PDF hashes or next action into it. Maintain concise session records, review summaries, defect records, request/receipt pointers when bridge transport is used, and canonical Human-review rN authority. New navigation or a changed operational fact still requires a record; a State-only transition does not require rewriting the navigation index.''')
    proposed[path] = t

    path = paths[3]
    t = originals[path]
    t = replace(t, 'Status: `FOLLOW-UP REVIEW HARDENED MAINTENANCE CANDIDATE / REAUDIT PENDING`', 'Status: `EDITION EXECUTION RECORD POLICY`')
    t = section(t, '## 4.', '''## 4. `index.md`

`index.md` is the first human-readable navigation file after `production-state.json`. Maintain run context and navigation, not a second live State summary.

Record:

- issue/Profile identity and canonical work branch/source root, with Profile/State paths;
- start-of-run reviewed baseline, start/objective/requested stop, explicitly historical run context;
- stable paths to machine review index, active approval/checkpoint authority and publication records;
- pointers to Grok/X task/result disposition and execution-mode/transport records when applicable;
- known edition-local deviations/shared-Core defects and their evidence pointers;
- session/review/defect/receipt pointers, including the session that records final disposition.

Read live lifecycle, next action, stop reason, State hash, Gate status and Candidate/PDF identity directly from the named Profile/State and its typed pointers. A machine review index names historical rN records; its newest approval is not automatically active approval. A snapshot display must identify the inspected bytes and separate stored facts, checked direct links and unverified dependencies. It must not infer Human decisions, select a regeneration boundary, or authorize execution.

Update the index when run context or navigation changes, or new handoff/defect information must be discoverable. Do not rewrite it merely because Gate/revision/Candidate/final State changed. Record actions, end state and decisions once in their existing session and machine records. Preserve older edition indexes as historical navigation; do not regenerate frozen/released editions to conform to this layout.
''')
    t = replace(t, '4. latest machine Human-review record/index if applicable;', '4. machine Human-review index and its named records if applicable; active approval comes from State provenance, not latest-record selection;')
    t = replace(t, '4. record exact next action/stop reason;', '4. record exact end-state bytes/reference and next action/stop reason in the session log as historical provenance, without duplicating live values in the navigation index;')
    proposed[path] = t

    path = paths[4]
    t = originals[path]
    t = replace(t, 'This is the current human-readable navigation record for the edition. Machine lifecycle authority remains `{state_rel}`.', 'This file records run context and navigation. Read current machine facts from `{state_rel}` and its typed pointers; the sections below are not a live State summary.')
    start = t.index('- Current State SHA-256:')
    end = t.index('## Grok/X', start)
    t = t[:start] + '''
## Human Gates

- Machine review history: `{profile['paths']['source_root']}/gates/review-index.json`
- Active approvals: follow `human_gate_provenance` in Production State, not the newest historical approval.

## Publication Candidate

- Follow the exact named publication artifact in State-bound checkpoints or active Preview approval.
- Candidate/PDF bytes and review validity must be checked by existing Core before action.

''' + t[end:]
    t = replace(t, '`{disposition}`\n"""', 'See session records and Production State. Initial execution disposition is recorded in `sessions/{session_id}.md`.\n"""')
    # The initial disposition is meaningful operational provenance, so preserve it once.
    t = replace(t, '- Session objective: {objective}', '- Initial execution disposition: `{disposition}`\n- Session objective: {objective}')
    proposed[path] = t

    diffs, stats = [], []
    for path in paths:
        before, after = originals[path], proposed[path]
        target = CANDIDATE / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(after, encoding='utf-8', newline='\n')
        diffs.extend(difflib.unified_diff(before.splitlines(True), after.splitlines(True), fromfile='a/' + path, tofile='b/' + path))
        stats.append(dict(path=path, baseline_sha256=manifests[path]['sha256'], proposed_sha256=hashlib.sha256(after.encode()).hexdigest(), before_lines=len(before.splitlines()), after_lines=len(after.splitlines())))
    (HERE / 'candidate.patch').write_text(''.join(diffs), encoding='utf-8', newline='\n')
    (HERE / 'candidate-files.json').write_text(json.dumps(stats, indent=2) + '\n', encoding='utf-8')
    return stats


if __name__ == '__main__':
    print(json.dumps(build(), indent=2))
