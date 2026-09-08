"""Read-only Git object probe; writes results only to this workspace when redirected."""
import collections
import json
import subprocess

REPO = 'D:/Git/japanese-generative-ai-survey'
MAIN = '0a47a9b85108c5a2e9644037e7c0fb48b5bd96dc'
W34 = '993583e871bcbfea7bfe700fe5c6f2648e8887c0'

def git(*args):
    return subprocess.check_output(['git', '-C', REPO, *args]).decode('utf-8')

def read(path, ref=W34):
    return json.loads(git('show', f'{ref}:{path}'))

files = git('ls-tree', '-r', '--name-only', MAIN).splitlines()
cfg = read('config/survey-production-v2.json', MAIN)
result = {'main': MAIN, 'w34': W34,
          'inventory': {prefix: sum(p.startswith(prefix) for p in files)
                        for prefix in ['schemas/', 'scripts/', '.github/workflows/', 'docs/']},
          'contract_file_counts': {k: len(v) for k, v in cfg['contract_files'].items()}}
result['state'] = {k: v for k, v in read('sources/2026-W34/production-state.json').items()
                   if k in ['lifecycle_state', 'next_action', 'terminal_reason', 'human_gates']}
all_w34 = git('ls-tree', '-r', '--name-only', W34).splitlines()
prefix = 'sources/2026-W34/evidence/v2/accepted/377134b62c98bf0b65a7cf8cda1ef538eac0e2afcd7aa9aeeeda0f1d09493ada/results/'
cards = [(p, read(p)) for p in all_w34 if p.startswith(prefix) and p.endswith('.json')]
result['evidence_status_counts'] = dict(collections.Counter(c.get('status') for _, c in cards))
result['card_samples'] = [{'path': p, 'card': c} for p,c in cards[:2]]
result['claim_count_distribution'] = dict(collections.Counter(len(c.get('claims', [])) for _, c in cards))
result['verified_with_all_targets_unresolved'] = sum(c.get('status') == 'VERIFIED' and bool(c.get('verification', {}).get('targets')) and all(t.get('status') == 'UNRESOLVED' for t in c['verification']['targets']) for _, c in cards)
supp = read('sources/2026-W34/execution/luna/w34-core-repair-r1/evidence-authority-supplement.json')
result['c019_authority'] = [s for s in supp['sources'] if 'C019' in json.dumps(s)]
result['historical_architecture'] = read('sources/2026-W34/architecture-v2.json', 'bc0921724c96f70d3f1adda4ece5b80ab5d5dd1d')
result['findings_paths'] = [p for p in all_w34 if p.startswith('sources/2026-W34/execution/findings/')]
print(json.dumps(result, ensure_ascii=False, indent=2))
