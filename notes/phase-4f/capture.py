"""Bounded read-only fixed-ref capture; reuse the prior blob/hash verifier."""
import importlib.util
import json
import sys
from pathlib import Path
sys.dont_write_bytecode = True
LAB = Path(__file__).resolve().parent
ROOT = LAB.parents[1]
spec = importlib.util.spec_from_file_location('capture4d', ROOT/'notes/phase-4d/capture.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.DEST = LAB
def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode('utf-8'))


module.save = save
get, api, CACHE = module.get, module.api, module.CACHE
HEAD = 'f50d229162b7402c504c0978f72dab4b33052f5e'
MAIN = '658ae823987431e1f1098243dc2f88cfc0d4864a'

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    print(get(HEAD, sys.argv[1]).decode('utf-8'))
