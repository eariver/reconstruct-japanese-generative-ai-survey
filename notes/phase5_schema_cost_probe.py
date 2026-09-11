"""Microbenchmark only: uncached schema gate vs exact-schema-byte compiled reuse.
No verdict/approval cache. No production change. Linux args: SNAPSHOT OUTPUT.
"""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import time
import jsonschema

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root))
from scripts import survey_schema_v2 as gate
card = json.loads((Path(__file__).parent / 'phase4-paper-candidate.json').read_text())
schema_path = root / 'schemas/evidence-v2-card.schema.json'
compiled = {}


def exact_schema_check(path):
    raw = path.read_bytes()
    key = hashlib.sha256(raw).hexdigest()
    if key not in compiled:
        schema = json.loads(raw)
        jsonschema.Draft202012Validator.check_schema(schema)
        compiled[key] = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    compiled[key].validate(card)


timings = []
for order in [('uncached', 'exact_schema_reuse'), ('exact_schema_reuse', 'uncached')]:
    for mode in order:
        start = time.perf_counter()
        for _ in range(200):
            if mode == 'uncached':
                gate.validate_instance(card, schema_path, label='microbenchmark')
            else:
                exact_schema_check(schema_path)
        timings.append({'mode': mode, 'validations': 200, 'seconds': time.perf_counter() - start})
with tempfile.TemporaryDirectory(prefix='astra-schema-cost-') as td:
    path = Path(td) / 'schema.json'
    path.write_bytes(schema_path.read_bytes())
    exact_schema_check(path)
    changed = json.loads(path.read_text())
    changed['properties']['status'] = {'const': 'REJECTED'}
    path.write_text(json.dumps(changed))
    rejected = False
    try:
        exact_schema_check(path)
    except jsonschema.ValidationError:
        rejected = True
    assert rejected
result = {'scope': 'SINGLE_CARD_SCHEMA_MICROBENCHMARK_NOT_STAGE_OR_LIFECYCLE_COST',
    'timings': timings, 'changed_schema_rejected_at_same_path': rejected,
    'cached_objects': 'compiled local-ref Card schema only; never PASS verdicts or Human approval',
    'limitations': 'No generic external-ref resolution, concurrency, memory bound or production integration tested'}
Path(sys.argv[2]).resolve().write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
