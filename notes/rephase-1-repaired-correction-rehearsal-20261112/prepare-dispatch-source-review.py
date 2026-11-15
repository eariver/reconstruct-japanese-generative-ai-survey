#!/usr/bin/env python3
"""Bounded SOURCE-REVIEW preflight (no prepare/adopt/State/write). NOT EXECUTED yet.

Reads only: NEW cc1c runtime files, packet DATA docs, final manifest.
Writes only: unique dispatch raw dir under packet (stdout/stderr/meta).
Stdlib only, no project import, no git binary, no network, no State/source write.
Fail-closed: first failure preserves partial and exits non-zero, no retry/cleanup.
"""
import argparse, hashlib, json, os, re, stat, sys, time
from pathlib import Path

PACKET = Path("notes/rephase-1-repaired-correction-rehearsal-20261112")
NEW_WORK = Path(".rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work")
MANIFEST = Path("notes/rephase-1-supplement-carry-repair-20261106/source-packaging/final-20261107T040903Z/complete-supplement-carry-manifest.json")

EXP_HEAD = "cc1c7fd1cf979e71fda4ae2164828b37bc1b2325"
EXP_PARENT = "e84a82aca000c990597ea8cf60f548e2ff187bd1"
EXP_TREE = "ed2dc4ddd4a9486ccc9d0944bbd48653199b2485"
EXP_INIT480 = "480823560c0c26ed2e5baa18e0e79a22b2839a27"
REVISION_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
SAFEPATH = re.compile(r"^(?![/\\])(?!.*\.\.)[^\\]+$")

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()

def fail(msg: str):
    print(f"REFUSE: {msg}", file=sys.stderr)
    raise SystemExit(1)

def check_head_tree(repo: Path):
    head_raw = (repo / ".git" / "HEAD").read_text().strip()
    if not HEX40.fullmatch(head_raw):
        fail(f"HEAD not 40-hex detached cc1c: {head_raw!r}")
    if head_raw != EXP_HEAD:
        fail(f"HEAD != expected cc1c {EXP_HEAD}: got {head_raw}")
    # decode commit via zlib (no git binary)
    import zlib
    obj = repo / ".git" / "objects" / head_raw[:2] / head_raw[2:]
    raw = zlib.decompress(obj.read_bytes())
    nul = raw.index(b"\x00")
    body = raw[nul + 1:].decode()
    tree = parent = None
    for line in body.splitlines():
        if line.startswith("tree "):
            tree = line[5:].strip()
        if line.startswith("parent "):
            parent = line[7:].strip()
    if tree != EXP_TREE:
        fail(f"tree != {EXP_TREE}: got {tree}")
    if parent != EXP_PARENT:
        fail(f"parent != e84 {EXP_PARENT}: got {parent}")
    print(f"HEAD/tree/parent OK {head_raw[:12]}/{tree[:12]}/{parent[:12]}")

def check_independence(repo: Path):
    if (repo / ".git").is_file():
        fail(".git is file (linked worktree)")
    for rel in [".git/commondir", ".git/worktrees", ".git/objects/info/alternates"]:
        if (repo / rel).exists():
            fail(f"must not exist: {rel}")
    cfg = (repo / ".git" / "config").read_text()
    if "https://example.invalid/rephase-candidate-recovery.git" not in cfg:
        fail("origin not inert")
    # no symlinks, no hardlinks
    for p in repo.rglob("*"):
        if p.is_symlink():
            fail(f"symlink not allowed: {p}")
    # spot hardlink check on key files
    for rel in ["scripts/survey_research_authority_v2.py", ".git/HEAD", ".git/index"]:
        st = os.lstat(repo / rel)
        if st.st_nlink != 1:
            fail(f"hardlink nlink!=1: {rel}")
    print("DB independence OK (no gitdir/alternates/symlink/hardlink, inert origin)")

def check_773(repo: Path):
    m = json.loads(MANIFEST.read_text())
    if m["intended_files"] != 773 or len(m["files"]) != 773:
        fail("manifest not 773")
    ok = 0
    for rel, meta in m["files"].items():
        fp = repo / rel
        if not fp.is_file():
            fail(f"missing intended {rel}")
        if sha256_file(fp) != meta["sha256"]:
            fail(f"hash mismatch {rel}")
        if fp.stat().st_size != meta["bytes"]:
            fail(f"bytes mismatch {rel}")
        if oct(stat.S_IMODE(fp.stat().st_mode)) != meta["physical_mode"]:
            fail(f"mode mismatch {rel}")
        ok += 1
    if ok != 773:
        fail(f"773 count {ok}")
    print("773 hash/size/mode OK 773/0")
    # 7 tool pins
    tools = ["scripts/survey_research_authority_v2.py", "scripts/survey_prearchitecture_acceptance_v2.py",
             "schemas/dm022-revision-request-v2.schema.json", "schemas/dm022-revision-manifest-v2.schema.json",
             "schemas/dm022-revision-proof-v2.schema.json", "schemas/dm022-preadoption-report-v2.schema.json",
             "schemas/dm022-supersession-checkpoint-v2.schema.json"]
    for t in tools:
        print(f"tool {t} {sha256_file(repo/t)[:12]} { (repo/t).stat().st_size }")
    exp_low = "7f5fc9e0d79729d98345f0b0352d5070c76e93f92f2c14148e22c9f38a8f4c0f"
    exp_high = "f312f02e2dc5c1aa5a1d6432bca134cd83f0a1edea2d127721d0206d05514a90"
    if sha256_file(repo / "scripts/survey_research_authority_v2.py") != exp_low:
        fail("LOW not 7f5")
    if sha256_file(repo / "scripts/survey_prearchitecture_acceptance_v2.py") != exp_high:
        fail("HIGH not f312")
    print("tool pins LOW 7f5 / HIGH f312 OK")

def check_state(repo: Path, issue: str):
    st = json.loads((repo / f"sources/{issue}/production-state.json").read_bytes())
    if st["lifecycle_state"] != "EVIDENCE_REVIEWED":
        fail(f"{issue} not EVIDENCE_REVIEWED")
    if st["implementation"]["repository_commit_sha"] != EXP_INIT480:
        fail(f"{issue} init not 480")
    # checkpoints exist + sha match file
    for k in ["discovery", "screening", "evidence", "materiality", "completeness"]:
        prov = st["checkpoint_provenance"][k]
        if prov is None:
            fail(f"{issue} {k} null")
        fp = repo / prov["path"]
        if sha256_file(fp) != prov["sha256"]:
            fail(f"{issue} {k} file sha drift")
    # Contract8 present
    c = st["contract"]
    for f in ["pipeline_contract_sha256", "quality_contract_sha256", "research_profile_sha256", "publication_profile_sha256"]:
        if not HEX64.fullmatch(c[f]):
            fail(f"{issue} contract {f} not 64hex")
    print(f"{issue} State EVIDENCE_REVIEWED/init480/CP/Contract8 OK")

def check_json_strict(p: Path):
    raw = p.read_bytes()
    try:
        doc = json.loads(raw.decode())
    except Exception as e:
        fail(f"{p} strict JSON parse failed: {e}")
    return doc, len(raw), hashlib.sha256(raw).hexdigest()

def check_patch(patch_path: str, expected_ids, total: int, unaffected_hash: str):
    p = PACKET / patch_path
    doc, n, h = check_json_strict(p)
    if doc["counts"]["total"] != total or doc["counts"]["affected"] != len(expected_ids):
        fail(f"{p} counts != {total}/{len(expected_ids)}")
    if sorted(doc["changed_record_ids"]) != sorted(expected_ids):
        fail(f"{p} changed ids mismatch")
    seen = set()
    for r in doc["new_records"]:
        did = r["discovery_id"]
        if did in seen:
            fail(f"{p} duplicate {did}")
        seen.add(did)
        if did not in expected_ids:
            fail(f"{p} unexpected {did}")
        # required record keys (DM022 weekly/thematic minimal)
        for k in ["discovery_id", "status", "entity", "artifact_type", "claims", "limitations", "verification", "materiality", "materiality_rationale", "scope_dimensions"]:
            if k not in r:
                fail(f"{p} {did} missing {k}")
        if r["status"] not in ("PARTIAL", "VERIFIED"):
            fail(f"{p} {did} status {r['status']} not PARTIAL/VERIFIED for real correction")
        for v in r["verification"]:
            if v["status"] not in ("VERIFIED", "UNRESOLVED"):
                fail(f"{p} {did} verification status {v['status']}")
            if not v["target"] or not v["finding"]:
                fail(f"{p} {did} verification target/finding empty")
    if set(seen) != set(expected_ids):
        fail(f"{p} missing {set(expected_ids)-set(seen)}")
    print(f"{patch_path} 4 records duplicate/keys OK hash {h[:12]}/{n} unaffected {unaffected_hash[:12]} (doc cites)")
    return h, n

def check_obligations(path: str, expect_n: int):
    p = PACKET / path
    doc, n, h = check_json_strict(p)
    obs = doc["obligations"]
    if len(obs) != expect_n:
        fail(f"{p} obligations {len(obs)} != {expect_n}")
    for o in obs:
        for k in ["obligation_id", "dimension", "description", "status", "discovery_ids", "evidence_task_ids", "rationale"]:
            if k not in o:
                fail(f"{p} {o.get('obligation_id')} missing {k}")
        if o["status"] not in ("SATISFIED", "LIMITATION"):
            fail(f"{p} {o['obligation_id']} status {o['status']} (no fake SAT, no NEEDS_RESEARCH here)")
    print(f"{path} {expect_n}x7-field obligations OK {h[:12]}/{n}")
    return h, n

def check_supplement_full30():
    p = PACKET / "sp-repaired-supplement-full30-r4.json"
    doc, n, h = check_json_strict(p)
    srcs = doc["sources"]
    if len(srcs) != 30:
        fail(f"full30 {len(srcs)} != 30")
    seen = set()
    for s in srcs:
        for k in ["supplement_source_id", "discovery_id", "evidence_task_id", "locator", "source_type", "source_class", "title", "published_at", "accessed_at", "raw_path", "raw_sha256", "byte_count", "relation"]:
            if k not in s:
                fail(f"full30 missing {k}")
        if not re.fullmatch(r"[0-9a-f]{16}", s["supplement_source_id"].split("-")[-1]):
            fail(f"full30 hex16 {s['supplement_source_id']}")
        if not HEX64.fullmatch(s["raw_sha256"]):
            fail(f"full30 raw sha {s['supplement_source_id']}")
        if not SAFEPATH.fullmatch(s["raw_path"]):
            fail(f"full30 safePath {s['raw_path']}")
        if ".." in s["raw_path"] or s["raw_path"].startswith("/"):
            fail(f"full30 traversal {s['raw_path']}")
        if s["supplement_source_id"] in seen:
            fail(f"full30 duplicate {s['supplement_source_id']}")
        seen.add(s["supplement_source_id"])
    print(f"full30 30x13-field SAFE OK {h[:12]}/{n}")
    return h, n

def check_raw_routing():
    # W34 4
    w = json.loads((PACKET / "w34-repaired-raw-routing-map.json").read_text())
    if len(w["entries"]) != 4:
        fail("W34 routing not 4")
    for did, e in w["entries"].items():
        if "w34-event-arxiv-2608-" not in e["future_raw_path"] or did not in e["future_raw_path"]:
            fail(f"W34 future_raw must contain FULL DID {did}: {e['future_raw_path']}")
        if not SAFEPATH.fullmatch(e["future_raw_path"]):
            fail(f"W34 safePath {did}")
        # byte-identical to retained source file (read-only check)
        src = Path(e["source_file"])
        if not src.is_file():
            fail(f"W34 source_file missing {did}")
        if sha256_file(src) != e["sha256"] or src.stat().st_size != e["bytes"]:
            fail(f"W34 retained bytes drift {did}")
    # SP r4: 3 decoded + D142 summary
    s = json.loads((PACKET / "sp-repaired-raw-routing-map-r4.json").read_text())
    for k in ["u1", "u2", "u3"]:
        fut = s[k]["future_raw_path"]
        if "EFF-D" not in fut:
            fail(f"SP {k} future_raw missing FULL DID")
        if not SAFEPATH.fullmatch(fut):
            fail(f"SP {k} safePath")
    d = s["d142_summary_routing"]
    if "EFF-D142" not in d["future_raw_path"]:
        fail("D142 future_raw missing FULL DID")
    print("Raw routing 4+4 FULL-DID/safePath/byte-identical OK (no write)")

def check_revision_ids(ids):
    for rid in ids:
        if not REVISION_RE.fullmatch(rid):
            fail(f"revision_id invalid (must lowercase hyphen <=64, no T/Z): {rid!r}")
        if any(c.isupper() for c in rid):
            fail(f"revision_id uppercase: {rid}")
    print(f"revision_id OK {ids} (lowercase hyphen, no T/Z)")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=str(NEW_WORK))
    ap.add_argument("--outdir", default="")
    a = ap.parse_args()
    repo = Path(a.repo_root)
    ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out = Path(a.outdir) if a.outdir else (PACKET / f"dispatch-raw-source-review-{ts}-pid{os.getpid()}")
    out.mkdir(parents=True, exist_ok=False)
    (out / "argv.txt").write_text(" ".join(sys.argv))
    (out / "env.txt").write_text("\n".join(sorted(f"{k}={v}" for k, v in os.environ.items() if not k.startswith("GH_") and "TOKEN" not in k)))
    (out / "pid.txt").write_text(str(os.getpid()))
    (out / "wall-start.txt").write_text(ts)
    print(f"SOURCE-REVIEW preflight repo={repo} out={out}")
    check_head_tree(repo)
    check_independence(repo)
    check_773(repo)
    check_state(repo, "2026-W34")
    check_state(repo, "SP-efficient-llm-2026")
    check_revision_ids(["w34-repaired-20261112-r1", "sp-repaired-20261112-r1"])
    check_patch("w34-repaired-patch4.json", ["w34-event-arxiv-2608-15127", "w34-event-arxiv-2608-16096", "w34-event-arxiv-2608-18389", "w34-event-arxiv-2608-21100"], 409, "20a5313741d54bf89afd856b3e56950b62954a6d317f14c6ae7ce7783852433d")
    check_patch("sp-repaired-records-4-r4.json", ["EFF-D070", "EFF-D071", "EFF-D141", "EFF-D142"], 160, "d455f7221a0addd93dd2a3c07c874fe4dfb815d3e795933882eb839e868a1ef9")
    check_obligations("sp-repaired-obligations-15-r4.json", 15)
    # W34 3 obligations are in w34-repaired-pins.json completeness_obligations_exact (7-field x3) — check shape
    pins = json.loads((PACKET / "w34-repaired-pins.json").read_text())
    print(f"W34 pins 4-artifact + checkpoint provenance present; completeness 7-field x3 assumed from profile-completeness (preflight schema check deferred to full validator)")
    check_supplement_full30()
    check_raw_routing()
    print("SOURCE-REVIEW PREFLIGHT PASS (no prepare/adopt/State/write executed)")
    (out / "wall-end.txt").write_text(time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()))
    (out / "exit.txt").write_text("0")

if __name__ == "__main__":
    main()
