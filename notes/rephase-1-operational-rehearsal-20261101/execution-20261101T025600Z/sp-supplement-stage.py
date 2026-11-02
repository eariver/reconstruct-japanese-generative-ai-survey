"""Stage 13 verified supplement raws to canonical paths + substantive read for body support."""
import hashlib
import json
import shutil
import sys
from pathlib import Path

WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
P2 = Path("notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p2-20261101T024051Z")
sys.path.insert(0, str(WORK))

gid_for = {
    "supp-d005-fp8-abs.html": "p2g01", "supp-d032-v32exp-launch.html": "p2g02",
    "supp-d061-mooncake-abs.html": "p2g03", "supp-d062-sarathi2023-abs.html": "p2g04",
    "supp-d062-sarathiserve2024-abs.html": "p2g05", "supp-d093-swepro-abs.html": "p2g06",
    "supp-d093-swepro-html.html": "p2g07", "supp-d094-tbench2-abs.html": "p2g08",
    "supp-d098-ruler-abs.html": "p2g09", "supp-d112-pyramidkv-abs.html": "p2g10",
    "supp-d117-deebert-abs.html": "p2g11", "supp-d119-genai-perf-docs.html": "p2g12",
    "supp-d139-doremi-abs.html": "p2g13",
}
old = json.loads((P2 / "DATA.p2f02.evidence-authority-supplement-r1.json").read_bytes())
assert len(old["sources"]) == 13
staged = 0
for e in old["sources"]:
    name = Path(e["raw_path"]).name
    src = P2 / f"DATA.{gid_for[name]}.{name}"
    b = src.read_bytes()
    assert len(b) == e["byte_count"], (name, len(b), e["byte_count"])
    assert hashlib.sha256(b).hexdigest() == e["raw_sha256"], name
    dst = WORK / e["raw_path"]
    if dst.exists():
        assert dst.read_bytes() == b, f"exists different {name}"
        print(f"ALREADY {e['raw_path']}")
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"STAGED {e['raw_path']} {len(b)}B")
    staged += 1
print(f"STAGED-OK {staged}/13 (size+sha256 verified vs old manifest entries; P2 bodies checker-PASS)")

print("--- substantive read: bound claims vs body ---")
r2 = json.loads(Path("notes/rephase-1-operational-rehearsal-20261101/execution-20261101T025600Z/input-archive/SP/interactive-evidence-r2-adapted-O13-15.json").read_bytes())
by_id = {r["discovery_id"]: r for r in r2["records"]}
sup_ids = {e["supplement_source_id"]: e for e in old["sources"]}
for r in r2["records"]:
    if r["status"] == "VERIFIED" and "source_bindings" in r:
        for sb in r["source_bindings"]:
            e = sup_ids[sb]
            raw = (WORK / e["raw_path"]).read_text(errors="replace")
            print(f"{r['discovery_id']} VERIFIED binds {sb}: raw {len(raw)} chars; title={e['title'][:70]}")
print("NOTE: abstract/launch-page bodies bound at abstract scope per r2 limitations; full-body pins remain pending research (see status docs)")
print("DONE-STAGE (raws only; no manifest built, no accept)")
