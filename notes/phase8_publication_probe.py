"""Bounded local publication experiment, Linux only; no production mutation.
Uses phase6 fixed export and phase7 fixtures. No external trusted admission.
"""
from contextlib import ExitStack
import difflib
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
from unittest import mock
from phase7_byte_binding import bind_card_bytes
from phase8_staged_acceptance import staged_acceptance

NOTES = Path(__file__).resolve().parent
SNAPSHOT = NOTES.parent / '.phase6-lab-snapshot'
CASES = ['valid', 'package_after_check', 'task_after_check', 'result_write_failure',
         'manifest_write_failure', 'repeat', 'tampered_existing', 'historical_reentry']
STAGED_ONLY = ['publish_failure', 'empty_collision', 'complete_collision', 'raw_before_publish']

def worker(root, arm):
    os.chdir(root)
    sys.path.insert(0, str(root))
    from scripts import survey_evidence_v2 as ev
    from scripts import survey_production_v2 as core
    from scripts import survey_agent_tool_v2 as runtime
    from scripts import survey_screening_v2 as screening
    from phase7_fixture import fixture, IMPLEMENTATION_SHA
    rows = []
    for case in CASES + (STAGED_ONLY if arm == 'staged' else []):
        with fixture() as (repo, state, package, results, sources):
            initial_state = state.read_bytes()
            initial_package = package.read_bytes()
            tasks = sorted((package.parent / 'tasks').iterdir())
            task_bytes = {p.name: p.read_bytes() for p in tasks}
            destination = repo / 'accepted'
            accepted = None
            old = None
            old_files = None
            if case in {'repeat', 'tampered_existing', 'historical_reentry'}:
                old = ev.accept_evidence_results(repo, package, results, destination, IMPLEMENTATION_SHA)
                if case == 'historical_reentry':
                    state.write_bytes(initial_state + b'\n')
                    initial_state = state.read_bytes()
                    package = old.parent / 'package.json'
                    results = old.parent / 'results'
                if case == 'tampered_existing':
                    next((old.parent / 'results').iterdir()).write_bytes(b'{}')
                old_files = {p.relative_to(destination).as_posix(): p.read_bytes() for p in destination.rglob('*') if p.is_file()}
            call_count = 0
            supplement_calls = 0
            original_card = ev.validate_evidence_card
            original_supplement = ev._supplement_entries_for_package
            original_write = Path.write_bytes
            original_json = core.write_json
            publisher = getattr(ev, '_publish_evidence_directory', None)
            def checked(*args, **kwargs):
                nonlocal call_count
                value = original_card(*args, **kwargs)
                call_count += 1
                if call_count == 1:
                    if case == 'package_after_check': package.write_bytes(b'{"changed":true}')
                    if case == 'task_after_check': tasks[0].write_bytes(b'{}')
                return value
            def supplement(*args, **kwargs):
                nonlocal supplement_calls
                supplement_calls += 1
                return original_supplement(*args, **kwargs)
            def write(path, data):
                if case == 'result_write_failure' and path.parent.name == 'results':
                    raise OSError('injected result write failure')
                return original_write(path, data)
            def write_json(path, value):
                if case == 'manifest_write_failure' and path.name == 'evidence-accepted.json':
                    raise OSError('injected acceptance manifest write failure')
                return original_json(path, value)
            def publish(src, dst):
                if case == 'publish_failure': raise OSError('injected publish failure')
                if case == 'empty_collision': dst.mkdir()
                if case == 'complete_collision': shutil.copytree(src, dst)
                if case == 'raw_before_publish':
                    path = repo / sources[0]['raw_path']
                    data = path.read_bytes()
                    path.write_bytes(b'!' + data[1:])
                return publisher(src, dst)
            error = None
            with ExitStack() as stack:
                if case == 'historical_reentry':
                    stack.enter_context(mock.patch.object(ev, 'validate_evidence_package_basis',
                        runtime._historical_evidence_basis_wrapper(ev.validate_evidence_package_basis)))
                    stack.enter_context(mock.patch.object(screening, 'validate_package_basis',
                        runtime._historical_screening_basis_wrapper(screening.validate_package_basis)))
                stack.enter_context(mock.patch.object(ev, 'validate_evidence_card', side_effect=checked))
                stack.enter_context(mock.patch.object(ev, '_supplement_entries_for_package', side_effect=supplement))
                stack.enter_context(mock.patch.object(Path, 'write_bytes', write))
                stack.enter_context(mock.patch.object(core, 'write_json', side_effect=write_json))
                if publisher: stack.enter_context(mock.patch.object(ev, '_publish_evidence_directory', side_effect=publish))
                try:
                    accepted = ev.accept_evidence_results(repo, package, results, destination, IMPLEMENTATION_SHA)
                except (ValueError, OSError) as exc:
                    error = str(exc)
            revalidation = None
            captured_equal = None
            if accepted:
                captured_equal = (accepted.parent / 'package.json').read_bytes() == initial_package and all(
                    (accepted.parent / 'tasks' / name).read_bytes() == data for name, data in task_bytes.items())
                try:
                    with ExitStack() as scope:
                        if case == 'historical_reentry':
                            scope.enter_context(mock.patch.object(ev, 'validate_evidence_package_basis',
                                runtime._historical_evidence_basis_wrapper(ev.validate_evidence_package_basis)))
                            scope.enter_context(mock.patch.object(screening, 'validate_package_basis',
                                runtime._historical_screening_basis_wrapper(screening.validate_package_basis)))
                        ev.validate_evidence_acceptance(repo, accepted, IMPLEMENTATION_SHA)
                except (ValueError, OSError, KeyError) as exc:
                    revalidation = str(exc)
            assert state.read_bytes() == initial_state
            unchanged = None
            if old_files is not None:
                unchanged = old_files == {p.relative_to(destination).as_posix(): p.read_bytes() for p in destination.rglob('*') if p.is_file()}
                assert unchanged
            rows.append({'arm': arm, 'case': case, 'accept_returned': accepted is not None,
                'error': error, 'subsequent_revalidation_error': revalidation,
                'package_tasks_equal_initial_bytes': captured_equal,
                'acceptance_sha256': hashlib.sha256(accepted.read_bytes()).hexdigest() if accepted else None,
                'canonical_run_dirs': sorted(p.name for p in destination.iterdir()) if destination.exists() else [],
                'private_working_dirs': sorted(p.name for p in repo.glob('.evidence-working-*')),
                'existing_bytes_unchanged': unchanged, 'same_existing_path': accepted == old if old else None,
                'state_unchanged': True})
            rows[-1]['card_validation_calls_during_accept'] = call_count
            rows[-1]['supplement_validation_calls_during_accept'] = supplement_calls
    costs = []
    for n in [2, 16]:
        with fixture(n) as (repo, state, package, results, sources):
            start = time.perf_counter()
            accepted = ev.accept_evidence_results(repo, package, results, repo / 'accepted', IMPLEMENTATION_SHA)
            elapsed = time.perf_counter() - start
            costs.append({'cards': n, 'synthetic_accept_seconds': elapsed})
    print(json.dumps({'arm': arm, 'rows': rows, 'costs': costs}))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        worker(Path(sys.argv[2]), sys.argv[3])
    else:
        source = (SNAPSHOT / 'scripts/survey_evidence_v2.py').read_text()
        before = bind_card_bytes(source)
        after = staged_acceptance(source)
        (NOTES / 'phase8-staged-acceptance-proposal.patch').write_text(''.join(difflib.unified_diff(
            before.splitlines(True), after.splitlines(True), fromfile='a/scripts/survey_evidence_v2.py',
            tofile='b/scripts/survey_evidence_v2.py')))
        results = []
        inherited = None
        for arm, module in [('card_byte_bound', before), ('staged', after)]:
            with tempfile.TemporaryDirectory(prefix='astra-publication-') as td:
                root = Path(td)
                shutil.copytree(SNAPSHOT, root, dirs_exist_ok=True)
                (root / 'scripts/survey_evidence_v2.py').write_text(module)
                run = subprocess.run([sys.executable, '-B', str(Path(__file__).resolve()), '--worker', str(root), arm],
                    capture_output=True, text=True)
                assert run.returncode == 0, run.stdout + run.stderr
                result = json.loads(run.stdout)
                result['module_sha256'] = hashlib.sha256(module.encode()).hexdigest()
                results.append(result)
                if arm == 'staged':
                    run = subprocess.run([sys.executable, '-B', str(NOTES / 'phase7_ownership_probe.py'), '--worker', str(root), arm],
                        capture_output=True, text=True)
                    assert run.returncode == 0, run.stdout + run.stderr
                    inherited = json.loads(run.stdout)
                print(arm + ' completed', flush=True)
        by = {(r['arm'], r['case']): r for a in results for r in a['rows']}
        assert by['staged','valid']['acceptance_sha256'] == by['card_byte_bound','valid']['acceptance_sha256']
        for case in ['package_after_check','task_after_check']:
            assert by['card_byte_bound',case]['subsequent_revalidation_error']
            assert by['staged',case]['package_tasks_equal_initial_bytes'] and not by['staged',case]['subsequent_revalidation_error']
        for case in ['result_write_failure','manifest_write_failure']:
            assert by['card_byte_bound',case]['canonical_run_dirs']
            assert not by['staged',case]['canonical_run_dirs']
        assert not by['staged','publish_failure']['canonical_run_dirs']
        assert by['staged','empty_collision']['error'] and len(by['staged','empty_collision']['canonical_run_dirs']) == 1
        assert by['staged','complete_collision']['accept_returned']
        assert by['staged','repeat']['same_existing_path']
        assert by['card_byte_bound','historical_reentry']['same_existing_path']
        assert not by['card_byte_bound','historical_reentry']['subsequent_revalidation_error']
        assert by['staged','historical_reentry']['error'] == 'Evidence package basis drift: state_sha256'
        assert by['staged','tampered_existing']['error'] and by['staged','tampered_existing']['existing_bytes_unchanged']
        assert by['staged','raw_before_publish']['accept_returned'] and by['staged','raw_before_publish']['subsequent_revalidation_error']
        assert all(not r['private_working_dirs'] for a in results for r in a['rows'])
        assert all(not r['accept_returned'] for r in inherited['rows'] if r['case'] in ['missing_target','duplicate_target','missing_text','duplicate_key','raw_after_first','raw_after_last'])
        (NOTES / 'phase8-publication-results.json').write_text(json.dumps({
            'fixed_main': '005e59841272464307386abfc11f5b09228f0814', 'scope': 'LINUX_CONTROLLED_FUNCTION_INTERLEAVINGS',
            'arms': results, 'inherited_phase7_cases_and_unit_tests': inherited}, indent=2) + '\n')
