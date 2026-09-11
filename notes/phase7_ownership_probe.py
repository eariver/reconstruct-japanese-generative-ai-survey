"""Controlled interleavings on fixed-main Core. No real concurrency or workflow admission.
Linux: PYTHONPATH=.../.phase4-linux-deps python3 -B notes/phase7_ownership_probe.py
Memoization arm is an intentionally unsafe comparison, not an implementation proposal.
"""
from contextlib import ExitStack
import copy
import difflib
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from phase5_stage_probe import harden
from phase7_byte_binding import bind_card_bytes

NOTES = Path(__file__).resolve().parent
SNAPSHOT = NOTES.parent / '.phase6-lab-snapshot'
CASES = ['valid', 'raw_after_first', 'raw_after_last', 'card_after_check', 'card_before_copy',
         'missing_target', 'duplicate_target', 'missing_text', 'duplicate_key']

def worker(root, arm):
    os.chdir(root)
    sys.path.insert(0, str(root))
    from scripts import survey_evidence_v2 as ev
    from scripts import survey_production_v2 as core
    from phase7_fixture import fixture, IMPLEMENTATION_SHA
    rows = []
    for case in CASES:
        with fixture() as (repo, state, package, results, sources):
            state_bytes = state.read_bytes()
            paths = sorted(results.iterdir())
            original = {p.name: p.read_bytes() for p in paths}
            def corrupt_card():
                card = json.loads(paths[0].read_bytes())
                card['claims'][0].pop('text', None)
                core.write_json(paths[0], card)
            def corrupt_raw():
                path = repo / sources[0]['raw_path']
                raw = path.read_bytes()
                path.write_bytes(b'!' + raw[1:])
            if case in {'missing_target', 'duplicate_target', 'missing_text', 'duplicate_key'}:
                card = json.loads(paths[0].read_bytes())
                if case == 'missing_target': card['verification']['targets'] = []
                if case == 'duplicate_target': card['verification']['targets'] *= 2
                if case == 'missing_text': card['claims'][0].pop('text')
                core.write_json(paths[0], card)
                if case == 'duplicate_key':
                    text = paths[0].read_text()
                    paths[0].write_text(text.replace('"status": "VERIFIED"', '"status": "REJECTED", "status": "VERIFIED"', 1))
            calls = {'card': 0, 'supplement': 0}
            card_validator = ev.validate_evidence_card
            entries_loader = ev._supplement_entries_for_package
            digest = ev._evidence_result_set_digest
            cache = {}
            def checked(*args, **kwargs):
                errors = card_validator(*args, **kwargs)
                calls['card'] += 1
                if calls['card'] == 1:
                    if case == 'raw_after_first': corrupt_raw()
                    if case == 'card_after_check': corrupt_card()
                if calls['card'] == 2 and case == 'raw_after_last': corrupt_raw()
                return errors
            def entries(*args, **kwargs):
                # A private per-call cache still lacks immutable input ownership.
                key = (str(args[0]), json.dumps(args[1], sort_keys=True))
                if arm == 'unsafe_memoized' and key in cache:
                    return copy.deepcopy(cache[key])
                calls['supplement'] += 1
                value = entries_loader(*args, **kwargs)
                cache[key] = copy.deepcopy(value)
                return value
            def before_copy(*args, **kwargs):
                value = digest(*args, **kwargs)
                if case == 'card_before_copy': corrupt_card()
                return value
            accepted = None
            rejection = None
            with ExitStack() as stack:
                stack.enter_context(mock.patch.object(ev, 'validate_evidence_card', side_effect=checked))
                stack.enter_context(mock.patch.object(ev, '_supplement_entries_for_package', side_effect=entries))
                stack.enter_context(mock.patch.object(ev, '_evidence_result_set_digest', side_effect=before_copy))
                try:
                    accepted = ev.accept_evidence_results(repo, package, results, repo / 'accepted', IMPLEMENTATION_SHA)
                except ValueError as exc:
                    rejection = str(exc)
            immediate_error = None
            exact_original = None
            fingerprint = None
            if accepted:
                exact_original = all((accepted.parent / 'results' / name).read_bytes() == data for name, data in original.items())
                fingerprint = hashlib.sha256(accepted.read_bytes()).hexdigest()
                try:
                    ev.validate_evidence_acceptance(repo, accepted, IMPLEMENTATION_SHA)
                except ValueError as exc:
                    immediate_error = str(exc)
            assert state.read_bytes() == state_bytes
            row = {'arm': arm, 'case': case, 'accept_returned': accepted is not None,
                'rejection': rejection, 'accepted_root_exists': (repo / 'accepted').exists(),
                'accepted_cards_equal_initial_bytes': exact_original,
                'acceptance_sha256': fingerprint, 'subsequent_revalidation_error': immediate_error,
                'calls_during_accept': calls, 'state_unchanged': True}
            rows.append(row)
    log = io.StringIO()
    suite = unittest.defaultTestLoader.loadTestsFromName('tests.test_survey_evidence_v2')
    result = unittest.TextTestRunner(stream=log).run(suite)
    assert result.wasSuccessful(), log.getvalue()
    print(json.dumps({'arm': arm, 'rows': rows, 'unit_tests': result.testsRun,
        'module_sha256': hashlib.sha256((root / 'scripts/survey_evidence_v2.py').read_bytes()).hexdigest()}))

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--worker':
        worker(Path(sys.argv[2]), sys.argv[3])
    else:
        source = (SNAPSHOT / 'scripts/survey_evidence_v2.py').read_text()
        patched = bind_card_bytes(source)
        (NOTES / 'phase7-card-byte-binding-proposal.patch').write_text(''.join(difflib.unified_diff(
            harden(source).splitlines(True), patched.splitlines(True),
            fromfile='a/scripts/survey_evidence_v2.py', tofile='b/scripts/survey_evidence_v2.py')))
        arms = []
        for arm in ['baseline', 'hardened', 'unsafe_memoized', 'card_byte_bound']:
            with tempfile.TemporaryDirectory(prefix='astra-ownership-') as td:
                root = Path(td)
                shutil.copytree(SNAPSHOT, root, dirs_exist_ok=True)
                if arm != 'baseline':
                    (root / 'scripts/survey_evidence_v2.py').write_text(patched if arm == 'card_byte_bound' else harden(source))
                proc = subprocess.run([sys.executable, '-B', str(Path(__file__).resolve()), '--worker', str(root), arm],
                    capture_output=True, text=True)
                assert proc.returncode == 0, proc.stdout + proc.stderr
                arms.append(json.loads(proc.stdout))
                print(arm + ' complete', flush=True)
        by = {(r['arm'], r['case']): r for a in arms for r in a['rows']}
        assert len({by[a,'valid']['acceptance_sha256'] for a in ['baseline','hardened','unsafe_memoized','card_byte_bound']}) == 1
        for a in ['baseline','hardened','card_byte_bound']:
            assert not by[a,'raw_after_first']['accept_returned']
        assert by['unsafe_memoized','raw_after_first']['accept_returned']
        for a in ['hardened','unsafe_memoized','card_byte_bound']:
            for c in ['missing_target','duplicate_target','missing_text','duplicate_key']:
                assert not by[a,c]['accept_returned'] and not by[a,c]['accepted_root_exists']
        for c in ['card_after_check','card_before_copy']:
            assert by['hardened',c]['accept_returned'] and by['hardened',c]['subsequent_revalidation_error']
            assert by['card_byte_bound',c]['accepted_cards_equal_initial_bytes'] and not by['card_byte_bound',c]['subsequent_revalidation_error']
        (NOTES / 'phase7-ownership-results.json').write_text(json.dumps({
            'fixed_main': '005e59841272464307386abfc11f5b09228f0814',
            'scope': 'CONTROLLED_FUNCTION_INTERLEAVINGS_NOT_REAL_CONCURRENCY_OR_STAGE_ADMISSION',
            'patch_base': 'phase5 structural hardening applied to fixed main', 'arms': arms}, indent=2) + '\n')
