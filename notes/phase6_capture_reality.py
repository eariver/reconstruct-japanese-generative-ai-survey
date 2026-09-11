"""Capture bounded read-only upstream observation for PR #487 impact review."""
import base64
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from phase6_prepare_lab import api, REF

OLD = '6d748a962d57beff89da7c1b20cb5a9a86c8e261'
if __name__ == '__main__':
    pr = api('pulls/487')
    main = api('git/ref/heads/main')['object']['sha']
    branch = 'weekly/2026-W34-v2-work'
    edition = api('git/ref/heads/' + branch)['object']['sha']
    path = 'sources/2026-W34/production-state.json'
    data = api(f'contents/{path}?ref={edition}')
    raw = base64.b64decode(data['content'])
    state = json.loads(raw)
    compare = api(f'compare/{OLD}...{REF}')
    out = {'observed_at': datetime.now(timezone.utc).isoformat(),
        'main_observed': main, 'analysis_main': REF,
        'pr': {key: pr[key] for key in ['number','title','html_url','state','merged','merged_at','merge_commit_sha']},
        'comparison': {'base': OLD, 'head': REF, 'total_commits': compare['total_commits'],
            'files': [{key: row[key] for key in ['filename','status','additions','deletions']} for row in compare['files']]},
        'edition': {'branch': branch, 'ref': edition, 'path': path,
            'sha256': hashlib.sha256(raw).hexdigest(),
            'state_summary': {key: state[key] for key in ['lifecycle_state','human_gates','next_action','terminal_reason']}}}
    dest = Path(__file__).resolve().parent / 'phase6-production-reality.json'
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(dest)
