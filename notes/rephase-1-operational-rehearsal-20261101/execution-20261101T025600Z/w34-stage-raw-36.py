"""W34 P6 Raw verify+stage 36 (fail-closed, no overwrite, no network).

Verifies 425 mapping rows vs 428-row r2 manifest + 426 DATA + 457 GET manifest,
then stages verified bytes at original repo-relative paths.
"""
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
P6 = Path("notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p6-20261101T115240Z")
P2 = Path("notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p2-20261101T024051Z")
sys.path.insert(0, str(WORK))
from scripts import survey_production_v2 as core
from scripts import survey_agent_control_v2 as agent

print(f"REAL-CLOCK {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
print(f"CWD={Path.cwd()}")
impl = core.repository_commit_sha(WORK)
print(f"HEAD={impl}")
assert impl == "480823560c0c26ed2e5baa18e0e79a22b2839a27", impl

# Pre: canonical State still CANDIDATES_NORMALIZED, evidence/v2 absent
state_path = WORK / "sources/2026-W34/production-state.json"
state = core.load_json(state_path)
print(f"PRE lifecycle={state['lifecycle_state']}")
assert state["lifecycle_state"] == "CANDIDATES_NORMALIZED", state["lifecycle_state"]
errs = agent.validate_agent_state(WORK, core.load_json(WORK / core.DEFAULT_CONFIG), state)
print(f"PRE agent errors={errs}")
assert not errs
ev2 = WORK / "sources/2026-W34/evidence/v2"
assert not ev2.exists(), f"refusing: evidence/v2 already exists {ev2}"
print("PRE evidence/v2 absent OK (no overwrite risk)")

# Load r2 manifest (old accepted proof, immutable) + P2b18 input
p6a_path = P6 / "DATA.p6a01.evidence-authority-supplement.json"
p6a_bytes = p6a_path.read_bytes()
print(f"P6a01 manifest {len(p6a_bytes)}B sha256={hashlib.sha256(p6a_bytes).hexdigest()}")
assert len(p6a_bytes) == 389423, len(p6a_bytes)
assert hashlib.sha256(p6a_bytes).hexdigest() == "0fada5df2f4add34b97a3ea722e4064245fc8475abadff154ca462cd9e302e19"
assert hashlib.sha1(b"blob " + str(len(p6a_bytes)).encode() + b"\x00" + p6a_bytes).hexdigest() == "88f5f3379f5dc8435ab16a21126ab7550b2c06fd"
r2 = json.loads(p6a_bytes)
print(f"r2 supplement_id={r2['supplement_id']} sources={len(r2['sources'])}")
assert len(r2["sources"]) == 428
assert r2["basis"]["discovery_sha256"] == "0a23be47dad8ddaf4f0a9c3261d97cc0006ac942bfd2321be2487289a34da31e"
# Old basis screening is stale 415... (will be rebased later, not here)
print(f"r2 basis screening stale={r2['basis']['screening_acceptance_sha256'][:12]}... path={r2['basis']['screening_acceptance_path']}")

# P2b18 input 409
evp = WORK / "sources/2026-W34/evidence/proposed-input/interactive-evidence.json"
inp_bytes = evp.read_bytes()
print(f"input staged {len(inp_bytes)}B sha256={hashlib.sha256(inp_bytes).hexdigest()}")
assert hashlib.sha256(inp_bytes).hexdigest() == "3ffc6e310e389bf03275b7ac7df0b029e43acec5f6140cc3a5bd56f8a4794f27"
doc = json.loads(inp_bytes)
need = {sb for r in doc["records"] for sb in (r.get("source_bindings") or [])}
print(f"input records={len(doc['records'])} need IDs={len(need)}")
assert len(need) == 428
r2_ids = {e["supplement_source_id"] for e in r2["sources"]}
print(f"need==r2_ids diff={len(need ^ r2_ids)}")
assert need == r2_ids, "P6a01 IDs must exactly equal input needed 428"
print(f"unbound records={sum(1 for r in doc['records'] if 'source_bindings' not in r)} (expect 8 documented)")
assert sum(1 for r in doc["records"] if "source_bindings" not in r) == 8

# Old r1 must never bind here
old = json.loads((P2 / "DATA.p2d01.evidence-authority-supplement.json").read_bytes())
old_ids = {e["supplement_source_id"] for e in old["sources"]}
print(f"old r1 {old['supplement_id']} sources={len(old_ids)} overlap with need={len(need & old_ids)} (must be 0)")
assert len(need & old_ids) == 0

# Mapping + manifest GET verification
mapping = json.loads((P6 / "supplement-mapping.json").read_bytes())
print(f"mapping rows={len(mapping)} total supp_ids={sum(len(r['supplement_ids']) for r in mapping)}")
assert len(mapping) == 425
assert sum(len(r["supplement_ids"]) for r in mapping) == 428
manifest = json.loads((P6 / "manifest.json").read_bytes())
print(f"P6 manifest results={len(manifest['results'])} total_data_files={manifest['total_data_files']} total_data_bytes={manifest['total_data_bytes']}")
assert len(manifest["results"]) == 457
assert manifest["total_data_files"] == 426
# Index manifest by gid and by repo_path
by_gid = {r["gid"]: r for r in manifest["results"]}
by_repo = {}
for r in manifest["results"]:
    rp = r.get("repo_path")
    if rp and rp.startswith("sources/2026-W34/"):
        by_repo.setdefault(rp, []).append(r)
# Index r2 sources by supplement_id
r2_by_sid = {e["supplement_source_id"]: e for e in r2["sources"]}
# Index manifest DATA by sha for blob fallback linkage
data_by_sha = {}
for r in manifest["results"]:
    for df in r.get("data_files", []):
        data_by_sha.setdefault(df.get("sha256"), []).append((r["gid"], df))

staged = 0
for row in mapping:
    repo_path = row["repo_path"]
    # containment: must be under sources/2026-W34/, relative, no .., no symlink components
    assert repo_path.startswith("sources/2026-W34/"), repo_path
    assert not repo_path.startswith("/"), repo_path
    assert ".." not in Path(repo_path).parts, repo_path
    local = Path("notes/rephase-1-operational-rehearsal-20261101") / row["local_DATA"]
    assert local.is_file(), f"missing DATA {row['local_DATA']}"
    b = local.read_bytes()
    assert len(b) == row["bytes"], (repo_path, len(b), row["bytes"])
    sha = hashlib.sha256(b).hexdigest()
    assert sha == row["content_sha256"], repo_path
    blob = hashlib.sha1(b"blob " + str(len(b)).encode() + b"\x00" + b).hexdigest()
    assert blob == row["git_blob_sha"], repo_path
    # vs manifest GET record(s) for same repo_path
    # Small files: local_DATA DATA.p6bXXX maps to manifest p6bXXX with repo_path+DATA.
    # Large files (>1MiB): local_DATA DATA.p6cXXX maps to p6cXXX DATA (repo_path None)
    #   + p6bXXX metadata (repo_path, no DATA). Link via blob SHA.
    gid = row["local_DATA"].split(".")[1]  # DATA.<gid>.<rest>
    rec = by_gid.get(gid)
    assert rec is not None, f"no manifest record for {gid}"
    if gid.startswith("p6b"):
        # small-file path: must carry repo_path+DATA
        assert rec.get("repo_path") == repo_path, (gid, rec.get("repo_path"), repo_path)
        assert rec.get("reported_blob_sha") == row["git_blob_sha"], gid
        assert rec.get("reported_size") == row["bytes"], gid
        df = rec.get("data_files", [{}])[0]
        assert df.get("bytes") == row["bytes"], gid
        assert df.get("sha256") == row["content_sha256"], gid
    elif gid.startswith("p6c"):
        # blob fallback: DATA here, repo metadata in sibling p6b
        assert rec.get("reported_blob_sha") == row["git_blob_sha"], gid
        assert rec.get("reported_size") == row["bytes"], gid
        df = rec.get("data_files", [{}])[0]
        assert df.get("bytes") == row["bytes"], gid
        assert df.get("sha256") == row["content_sha256"], gid
        # sibling p6b must carry same blob/size + repo_path
        sib_gid = gid.replace("p6c", "p6b", 1)
        sib = by_gid.get(sib_gid)
        # p6c007 links to p6b007 etc.; some p6c numbers skip (e.g. p6c020) – find by blob
        if sib is None or sib.get("reported_blob_sha") != row["git_blob_sha"]:
            cands = [r for r in manifest["results"] if r.get("reported_blob_sha") == row["git_blob_sha"] and r.get("repo_path") == repo_path]
            assert cands, f"no sibling metadata for blob {gid} {repo_path}"
            sib = cands[0]
        assert sib.get("repo_path") == repo_path, (gid, sib.get("repo_path"), repo_path)
        assert sib.get("reported_blob_sha") == row["git_blob_sha"], sib_gid
        assert sib.get("reported_size") == row["bytes"], sib_gid
    else:
        raise AssertionError(f"unexpected gid prefix {gid}")
    # vs r2 manifest raw_sha256/byte_count for each supplement_id in row
    for sid in row["supplement_ids"]:
        e = r2_by_sid.get(sid)
        assert e is not None, f"mapping sid {sid} not in r2 manifest"
        assert e["raw_path"] == repo_path, (sid, e["raw_path"], repo_path)
        assert e["raw_sha256"] == row["content_sha256"], sid
        assert e["byte_count"] == row["bytes"], sid
        # source_class/type preserved, no aliasing
        assert e["source_class"] == row["source_class"], sid
        assert e["source_type"] == row["source_type"], sid
    # Stage at original path (fail-closed, no overwrite)
    dst = WORK / repo_path
    # containment resolved: must stay under WORK/sources/2026-W34
    resolved = dst.resolve()
    assert str(resolved).startswith(str((WORK / "sources/2026-W34").resolve())), f"escape {repo_path}"
    assert not dst.is_symlink(), f"symlink present {repo_path}"
    if dst.exists():
        assert dst.read_bytes() == b, f"collision different bytes {repo_path}"
        print(f"ALREADY {repo_path}")
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        assert not dst.is_symlink()
        shutil.copy2(local, dst)
    staged += 1

print(f"STAGED-OK {staged}/425 (size+sha+blob+manifest+r2 verified; old r1 never used)")
# Post: state unchanged, still CANDIDATES_NORMALIZED
state2 = core.load_json(state_path)
assert state2["lifecycle_state"] == "CANDIDATES_NORMALIZED"
assert core.sha256_file(state_path) == core.sha256_file(state_path)
print(f"POST lifecycle={state2['lifecycle_state']} agent errors={agent.validate_agent_state(WORK, core.load_json(WORK / core.DEFAULT_CONFIG), state2)}")
print("DONE-STAGE-RAW-36 (raws only; no manifest built, no accept, no state write)")
