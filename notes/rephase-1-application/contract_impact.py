"""Read-only contract-identity witness; not edition migration or validation."""
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = '774dd39a951c9ac3818e83dfffd4c7666efb0a20'
CACHE = ROOT / '.rephase-1-inputs' / BASE
CANDIDATE = Path('/tmp/jgas-rephase-application-r2')
sys.path.insert(0, str(CANDIDATE))
from scripts import survey_production_v2 as core


def main():
    cfg = core.load_json(CANDIDATE / core.DEFAULT_CONFIG)
    assert (CANDIDATE / core.DEFAULT_CONFIG).read_bytes() == (CACHE / core.DEFAULT_CONFIG).read_bytes()
    paths = set(cfg['contract_files']['pipeline'] + cfg['contract_files']['quality'])
    paths.update(map(str, [core.DEFAULT_CONFIG, core.PROFILE_SCHEMA, core.STATE_SCHEMA]))
    tree = json.loads((CACHE / 'tree.json').read_text())
    blobs = {r['path']: r for r in tree['tree'] if r['type'] == 'blob'}
    for path in paths:
        raw = (CACHE / path).read_bytes()
        assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == blobs[path]['sha']
    contracts = []
    for research in cfg['research_profiles']:
        for publication in cfg['publication_profiles']:
            before = core.contract_identity(CACHE, cfg, research, publication)
            after = core.contract_identity(CANDIDATE, cfg, research, publication)
            changed = [key for key in before if before[key] != after[key]]
            assert changed == ['pipeline_contract_sha256']
            contracts.append(dict(research=research, publication=publication, baseline=before, candidate=after, changed_fields=changed))
    historical = []
    for issue in ['2026-W33', '2026-W34', 'SP001']:
        path = CACHE / 'sources' / issue / 'production-state.json'
        raw = path.read_bytes()
        rel = path.relative_to(CACHE).as_posix()
        assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == blobs[rel]['sha']
        state = json.loads(raw)
        historical.append(dict(path=rel, sha256=hashlib.sha256(raw).hexdigest(), saved_lifecycle=state['lifecycle_state'],
                               saved_contract=state['contract'], saved_implementation=state['implementation'],
                               validation='NOT_RUN; retained historical authority, not migrated'))
    result = dict(scope='Exact contract function outputs and saved State field inspection only',
                  baseline=BASE, candidate=json.loads((HERE / 'candidate.json').read_text())['candidate_head'],
                  contract_inputs_verified=len(paths),
                  changed_pipeline_inputs=[p for p in cfg['contract_files']['pipeline'] if (CACHE/p).read_bytes() != (CANDIDATE/p).read_bytes()],
                  identity_pairs=contracts, historical_states=historical,
                  edition_migration=False, full_state_validation=False)
    (HERE / 'contract-impact.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['identity_pairs','historical_states']}, indent=2))


if __name__ == '__main__':
    main()
