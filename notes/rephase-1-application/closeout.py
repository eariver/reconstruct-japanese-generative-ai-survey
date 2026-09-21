"""Bind root closeout to unchanged candidate, sealed inputs and independent report."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    packet = json.loads((HERE/'review-input.json').read_text())
    for row in packet['evidence']:
        assert sha(ROOT/row['path']) == row['sha256'], row['path']
    independent = json.loads((HERE/'auditor/source-checks.json').read_text())
    assert independent['head'] == packet['candidate_head'] and independent['tree'] == packet['candidate_tree']
    hashes = {r['path']:r['sha256'] for r in independent['candidate_files']}
    for row in packet['candidate_files']:
        assert hashes[row['path']] == row['proposed_sha256']
    fixtures = []
    for value in [packet['fixture'], packet['auditor_fixture']]:
        folder = Path(value)
        def git(*args):
            return subprocess.check_output(['git', *args], cwd=folder, text=True).strip()
        assert git('rev-parse', 'HEAD') == packet['candidate_head']
        assert git('rev-parse', 'HEAD^{tree}') == packet['candidate_tree']
        assert git('rev-parse', 'HEAD^') == packet['baseline']
        assert git('remote','get-url','origin') == packet['origin']
        assert not (folder/'.git/objects/info/alternates').exists()
        assert not git('diff','--name-only') and not git('diff','--cached','--name-only')
        for row in packet['candidate_files']:
            assert sha(folder/row['path']) == row['proposed_sha256']
        fixtures.append(dict(path=value, head=packet['candidate_head'], tracked_and_staged_delta=False,
                             untracked=git('status','--porcelain').splitlines()))
    docs = [ROOT/'AGENTS.md', ROOT/'README.md', ROOT/'handoff/rephase-1-continuation.md',
            ROOT/'outputs/rephase-1-application-assessment.md', HERE/'README.md']
    checked_links = 0
    for doc in docs:
        for link in re.findall(r'\]\(([^)]+)\)', doc.read_text(encoding='utf-8-sig')):
            if '://' in link or link.startswith('#'):
                continue
            path = link.split('#')[0]
            assert (doc.parent/path).is_file(), (str(doc),path)
            checked_links += 1
    targeted = json.loads((HERE/'targeted-results.json').read_text())
    assert targeted['head'] == packet['candidate_head'] and targeted['returncode'] == 0
    log = (HERE/'targeted-unittest.txt').read_text()
    assert 'Ran 3 tests' in log and log.rstrip().endswith('OK')
    broad = (HERE/'full-unittest.txt').read_text()
    assert not (HERE/'full-results.json').exists() and not re.search(r'^Ran \d+ tests', broad, re.M)
    result = dict(closed_date_jst='2026-09-21', disposition='NOT_READY', final_seven_point_audit_started=False,
                  candidate_head=packet['candidate_head'], candidate_tree=packet['candidate_tree'],
                  evidence_inputs_verified=len(packet['evidence']), review_input_sha256=sha(HERE/'review-input.json'),
                  independent_report_sha256=sha(HERE/'auditor/review.md'), independent_source_checks_sha256=sha(HERE/'auditor/source-checks.json'),
                  independent_review_reperformed_after_root_tests=False, root_targeted_tests_passed=3,
                  broad_suite='INCOMPLETE; no completion record; termination cause unknown',
                  broad_log_sha256=sha(HERE/'full-unittest.txt'), local_links_checked=checked_links, fixtures=fixtures,
                  production_mutated=False, production_adopted=False)
    (HERE/'closeout.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__=='__main__':
    main()
