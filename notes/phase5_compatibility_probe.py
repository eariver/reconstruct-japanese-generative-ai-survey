"""Additional-check compatibility, not full production historical replay.
Linux: python3 -B notes/phase5_compatibility_probe.py SNAPSHOT OUTPUT
Requires analysis-history-inputs.json from the four earlier fixed-ref samples.
"""
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
from phase5_stage_probe import harden

snapshot = Path(sys.argv[1]).resolve()
output = Path(sys.argv[2]).resolve()
with tempfile.TemporaryDirectory(prefix='astra-compatibility-') as td:
    root = Path(td)
    shutil.copytree(snapshot, root, dirs_exist_ok=True)
    source_path = root / 'scripts/survey_evidence_v2.py'
    source_path.write_text(harden(source_path.read_text()))
    os.chdir(root)
    sys.path.insert(0, str(root))
    from scripts import survey_evidence_v2 as evidence
    from scripts import survey_schema_v2 as schema
    from tests.test_survey_evidence_v2 import SurveyEvidenceV2Tests
    log = io.StringIO()
    result = unittest.TextTestRunner(stream=log, verbosity=1).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(SurveyEvidenceV2Tests))
    assert result.wasSuccessful(), log.getvalue()
    samples = json.loads((root / 'analysis-history-inputs.json').read_text())
    rows = []
    for index, sample in enumerate(samples):
        path = root / f'history-{index}.json'
        path.write_text(sample['card_text'])
        before = path.read_bytes()
        card = evidence._load_factual_card(path)
        schema.validate_instance(card, root / evidence.CARD_SCHEMA, label='historical sample')
        targets = [t['target'] for t in card['verification']['targets']]
        assert len(targets) == len(set(targets)) and set(targets) == set(sample['task']['verification_targets'])
        assert path.read_bytes() == before
        rows.append({'id': sample['id'], 'ref': sample['ref'], 'sha256': hashlib.sha256(before).hexdigest(),
            'additional_checks_pass': True, 'bytes_unchanged': True})
    output.write_text(json.dumps({'scope': 'PATCHED_UPSTREAM_UNIT_TESTS_AND_ADDITIONAL_HISTORICAL_CHECKS_ONLY',
        'patched_module_sha256': hashlib.sha256(source_path.read_bytes()).hexdigest(),
        'upstream_tests': {'run': result.testsRun, 'passed': result.wasSuccessful()},
        'historical_samples': rows, 'full_historical_authority_replay': False}, indent=2) + '\n')
    print(output)
