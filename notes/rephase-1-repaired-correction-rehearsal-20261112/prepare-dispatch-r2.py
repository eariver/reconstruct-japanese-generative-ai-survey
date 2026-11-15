#!/usr/bin/env python3
"""Bounded ACTUAL prepare dispatch r2 — ONE edition per invocation (NOT EXECUTED).

Reads: NEW cc1c repo, packet DATA docs, final manifest.
Writes (only when executed later, not now): inside-repo request
  sources/<issue>/research/v2/acceptance-revision-inputs/<revision-id>.json,
  exact 4 Raw buffers (FULL DID, new only), SP new supp payload via existing
  builder, HIGH-owned R (manifest/retention/candidate). No Decision forged.
Calls ONLY existing HIGH prepare_revision(repo,state,request,id), prints manifest_ref.
Stdlib cheap checks first; HIGH performs full content guarantees.
Fail-closed: first error preserves partial, numeric exit, no retry/cleanup/adopt.
"""
import argparse
import hashlib
import json
import os
import re
import stat
import sys
import time
from pathlib import Path

# Pins (explicit, no guess)
EXP_HEAD = "cc1c7fd1cf979e71fda4ae2164828b37bc1b2325"
EXP_PARENT = "e84a82aca000c990597ea8cf60f548e2ff187bd1"
EXP_TREE = "ed2dc4ddd4a9486ccc9d0944bbd48653199b2485"
EXP_INIT480 = "480823560c0c26ed2e5baa18e0e79a22b2839a27"
EXP_MANIFEST_SHA = "a7e40c4711a66b4d1d2541e6af1a97fd0e531d217e233f45ce43b40e19cef40c"
REVISION_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
SAFEPATH = re.compile(r"^(?![/\\])(?!.*\.\.)[^\\]+$")
ALLOWED_ENV = {"PATH", "HOME", "LANG", "LC_ALL", "LC_MESSAGES", "TZ",
               "PYTHONDONTWRITEBYTECODE", "PYTHONPATH", "PWD", "TMPDIR",
               "USER", "LOGNAME", "SHELL"}

PACKET = Path("notes/rephase-1-repaired-correction-rehearsal-20261112")
DEFAULT_REPO = Path(".rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work")
MANIFEST = Path("notes/rephase-1-supplement-carry-repair-20261106/source-packaging/final-20261107T040903Z/complete-supplement-carry-manifest.json")
DEFAULT_REV = {"2026-W34": "w34-repaired-20261112-r1",
               "SP-efficient-llm-2026": "sp-repaired-20261112-r1"}

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()

def fail(msg: str):
    print(f"REFUSE: {msg}", file=sys.stderr)
    raise SystemExit(1)

def load_strict_json(p: Path):
    """Strict JSON with duplicate-key hook (no false strict)."""
    raw = p.read_bytes()
    def hook(pairs):
        d = {}
        for k, v in pairs:
            if k in d:
                raise ValueError(f"duplicate key {k!r} in {p}")
            d[k] = v
        return d
    try:
        doc = json.loads(raw.decode(), object_pairs_hook=hook)
    except Exception as e:
        fail(f"{p} strict JSON failed: {e}")
    return doc, raw, hashlib.sha256(raw).hexdigest(), len(raw)

def sized_ref(repo: Path, rel: str) -> dict:
    """Exact SizedRef helper, no fake verified_dict."""
    if not SAFEPATH.fullmatch(rel):
        fail(f"SizedRef safePath invalid: {rel!r}")
    if rel.startswith("/") or ".." in Path(rel).parts:
        fail(f"SizedRef traversal: {rel!r}")
    abs_p = repo / rel
    # refuse symlink for immutable inputs
    if abs_p.is_symlink():
        fail(f"SizedRef symlink refused: {rel}")
    st = abs_p.stat()
    if not stat.S_ISREG(st.st_mode):
        fail(f"SizedRef not regular: {rel}")
    return {"path": rel, "sha256": sha256_file(abs_p), "byte_count": st.st_size}

def check_head_tree(repo: Path):
    head_raw = (repo / ".git" / "HEAD").read_text().strip()
    if not HEX40.fullmatch(head_raw) or head_raw != EXP_HEAD:
        fail(f"HEAD != cc1c {EXP_HEAD}: got {head_raw!r}")
    import zlib
    obj = repo / ".git" / "objects" / head_raw[:2] / head_raw[2:]
    raw = zlib.decompress(obj.read_bytes())
    body = raw[raw.index(b"\x00") + 1:].decode()
    tree = parent = None
    for line in body.splitlines():
        if line.startswith("tree "):
            tree = line[5:].strip()
        if line.startswith("parent "):
            parent = line[7:].strip()
    if tree != EXP_TREE or parent != EXP_PARENT:
        fail(f"tree/parent != ed2dc4/e84: got {tree}/{parent}")
    print(f"HEAD/tree/parent OK {head_raw[:12]}/{tree[:12]}/{parent[:12]}")

def inventory_old(repo: Path, issue: str) -> dict:
    """Byte hash/mode inventory for entry/post guard (773 + issue materials)."""
    m = json.loads(MANIFEST.read_text())
    if hashlib.sha256(MANIFEST.read_bytes()).hexdigest() != EXP_MANIFEST_SHA:
        fail(f"final manifest != a7e40c…: {MANIFEST}")
    inv = {}
    for rel in m["files"]:
        fp = repo / rel
        if not fp.is_file():
            fail(f"773 missing {rel}")
        st = fp.stat()
        inv[rel] = [sha256_file(fp), st.st_size, oct(stat.S_IMODE(st.st_mode))]
    # materials under sources/<issue> (excluding future R/inputs not yet present)
    src = repo / f"sources/{issue}"
    for p in sorted(src.rglob("*")):
        if p.is_file() and not p.is_symlink():
            # skip future owned paths if somehow present (must not exist pre-dispatch)
            s = p.relative_to(repo).as_posix()
            if "/research/v2/acceptance-revision" in s:
                fail(f"future R/inputs must not exist pre-dispatch: {s}")
            if s not in inv:
                st = p.stat()
                inv[s] = [sha256_file(p), st.st_size, oct(stat.S_IMODE(st.st_mode))]
    return inv

def main():
    ap = argparse.ArgumentParser(description="Actual bounded HIGH prepare dispatch r2 (one edition).")
    ap.add_argument("--issue", required=True, choices=["2026-W34", "SP-efficient-llm-2026"])
    ap.add_argument("--repo-root", default=str(DEFAULT_REPO))
    ap.add_argument("--revision-id", default=None)
    ap.add_argument("--outdir", default=None)
    a = ap.parse_args()
    issue = a.issue
    repo = Path(a.repo_root)
    rev = a.revision_id or DEFAULT_REV[issue]
    if not REVISION_RE.fullmatch(rev) or any(c.isupper() for c in rev):
        fail(f"revision_id invalid (lowercase hyphen <=64, no T/Z): {rev!r}")

    ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out = Path(a.outdir).resolve() if a.outdir else (PACKET.resolve() / f"prepare-dispatch-r2-{issue}-{ts}-pid{os.getpid()}")
    out.mkdir(parents=True, exist_ok=False)
    abs_log = lambda n: str((out / n).resolve())
    argv_s = " ".join(sys.argv)
    (out / "argv.txt").write_text(argv_s)
    env_w = {k: os.environ.get(k, "") for k in sorted(ALLOWED_ENV)}
    (out / "env-whitelist.txt").write_text("\n".join(f"{k}={v}" for k, v in env_w.items()))
    (out / "pid.txt").write_text(str(os.getpid()))
    (out / "wall-start.txt").write_text(ts)
    print(f"DISPATCH r2 issue={issue} rev={rev} repo={repo.resolve()} out={out.resolve()}")

    # Entry guards (cheap, stdlib, no project import)
    check_head_tree(repo)
    entry_inv = inventory_old(repo, issue)
    (out / "entry-inventory.json").write_text(json.dumps(entry_inv, indent=2, sort_keys=True))
    st_doc, _, _, _ = load_strict_json(repo / f"sources/{issue}/production-state.json")
    if st_doc["lifecycle_state"] != "EVIDENCE_REVIEWED" or st_doc["implementation"]["repository_commit_sha"] != EXP_INIT480:
        fail(f"{issue} State not EVIDENCE_REVIEWED/init480")

    # Patch docs: check ACTUAL keys (no counts/new_records assumption)
    patch_name = "w34-repaired-patch4.json" if issue == "2026-W34" else "sp-repaired-records-4-r4.json"
    patch_doc, patch_raw, patch_hash, patch_len = load_strict_json(PACKET / patch_name)
    print(f"patch actual keys: {sorted(patch_doc.keys())}")
    if "changed_record_ids" not in patch_doc:
        fail(f"{patch_name} missing changed_record_ids, actual keys {sorted(patch_doc.keys())}")
    rec_key = "new_records" if "new_records" in patch_doc else ("records" if "records" in patch_doc else None)
    if rec_key is None:
        fail(f"{patch_name} missing new_records/records, actual keys {sorted(patch_doc.keys())}")
    changed = patch_doc["changed_record_ids"]
    recs = patch_doc[rec_key]
    if len(changed) != 4 or len(recs) != 4:
        fail(f"{patch_name} 4-record shape: changed {len(changed)} recs {len(recs)}")
    seen = set()
    for r in recs:
        did = r.get("discovery_id")
        if not did or did in seen:
            fail(f"{patch_name} duplicate/missing discovery_id {did!r}")
        seen.add(did)
        for k in ["discovery_id", "status", "entity", "artifact_type", "claims", "limitations", "verification", "materiality", "materiality_rationale", "scope_dimensions"]:
            if k not in r:
                fail(f"{patch_name} {did} missing {k}")
        if r["status"] not in ("PARTIAL", "VERIFIED"):
            fail(f"{patch_name} {did} status {r['status']}")
        for v in r["verification"]:
            if v.get("status") not in ("VERIFIED", "UNRESOLVED") or not v.get("target") or not v.get("finding"):
                fail(f"{patch_name} {did} verification shape")
    if set(seen) != set(changed):
        fail(f"{patch_name} changed vs records mismatch {set(changed)^seen}")
    # unaffected hash: log actual field, no hardcoded compare
    for k in patch_doc:
        if "unaffected" in k.lower() and "hash" in k.lower():
            v = patch_doc[k]
            if not (isinstance(v, str) and HEX64.fullmatch(v)):
                fail(f"{patch_name} {k} not 64hex")
            print(f"{patch_name} {k} actual {v[:12]} (logged, not guessed)")
    print(f"{patch_name} 4 unique/record-keys/verification OK {patch_hash[:12]}/{patch_len}")

    # Obligations actual (7-field x3 / x15, SP r5 pending noted)
    oblig_name = "sp-repaired-obligations-15-r4.json" if issue == "SP-efficient-llm-2026" else None
    if issue == "2026-W34":
        # W34 obligations live in profile-completeness (7-field x3) — cheap shape via State completeness file
        comp_ref = None
        # find completeness artifact from checkpoint record (actual, no guess)
        print("W34 obligations: 7-field x3 from profile-completeness (FULL validate by HIGH/full validator later; SP r5 pending separate)")
    else:
        o_doc, _, o_hash, o_len = load_strict_json(PACKET / oblig_name)
        if len(o_doc.get("obligations", [])) != 15:
            fail(f"{oblig_name} !=15")
        for o in o_doc["obligations"]:
            for k in ["obligation_id", "dimension", "description", "status", "discovery_ids", "evidence_task_ids", "rationale"]:
                if k not in o:
                    fail(f"{oblig_name} {o.get('obligation_id')} missing {k}")
            if o["status"] not in ("SATISFIED", "LIMITATION"):
                fail(f"{oblig_name} {o['obligation_id']} fake SAT shape {o['status']}")
        print(f"{oblig_name} 15x7-field OK {o_hash[:12]}/{o_len} (r5 rationale correction pending independent approval)")

    # Raw routing actual (FULL DID, safePath, pinned source bytes; no write yet)
    if issue == "2026-W34":
        rout, _, _, _ = load_strict_json(PACKET / "w34-repaired-raw-routing-map.json")
        if len(rout.get("entries", {})) != 4:
            fail("W34 routing not 4")
        for did, e in rout["entries"].items():
            if did not in e["future_raw_path"] or "w34-event-arxiv-2608-" not in e["future_raw_path"]:
                fail(f"W34 future_raw FULL DID {did}")
            if not SAFEPATH.fullmatch(e["future_raw_path"]):
                fail(f"W34 safePath {did}")
            src = Path(e["source_file"])
            if sha256_file(src) != e["sha256"] or src.stat().st_size != e["bytes"]:
                fail(f"W34 pinned source drift {did}")
        print("W34 4 Raw route FULL-DID/safePath/pinned-bytes OK (no write)")
    else:
        rout, _, _, _ = load_strict_json(PACKET / "sp-repaired-raw-routing-map-r4.json")
        for k in ["u1", "u2", "u3"]:
            fut = rout[k]["future_raw_path"]
            if "EFF-D" not in fut or not SAFEPATH.fullmatch(fut):
                fail(f"SP {k} FULL DID/safePath")
        if "EFF-D142" not in rout["d142_summary_routing"]["future_raw_path"]:
            fail("SP D142 FULL DID")
        print("SP 4 Raw route FULL-DID/safePath OK (no write)")

    # --- From here, actual writes would occur when EXECUTED (not now) ---
    # Planned write-set (declared, not created now):
    req_rel = f"sources/{issue}/research/v2/acceptance-revision-inputs/{rev}.json"
    rev_root_rel = f"sources/{issue}/research/v2/acceptance-revisions/{rev}"
    print(f"PLANNED request (inside repo): {req_rel}")
    print(f"PLANNED R (HIGH-owned): {rev_root_rel}/ (revision-manifest.json, retention/, candidate/)")
    if issue == "2026-W34":
        print("PLANNED Raw x4 (new only, byte-identical routing copies); W34 supplement_manifest=null (existing ce6f… carried)")
    else:
        print("PLANNED Raw x4 + new supp payload sources/SP-efficient-llm-2026/external/evidence-supplement/evidence-authority-supplement-r4-sp17-20261112.json via build_evidence_authority_supplement + FULL validate, then supplement_manifest SizedRef")

    print("CALL (when authorized, single edition): from scripts.survey_prearchitecture_acceptance_v2 import prepare_revision; prepare_revision(Path(repo), Path(state_path), Path(request_path), revision_id); print manifest_ref")
    print("Unresolved callsite Qs: (1) SP obligations r4 vs r5 rationale — use r4 until r5 independent approval; (2) request.runner=base preserved vs affected observed_at single-runner skew — HIGH guarantees full content, independent review judges; (3) request.recorded_at/generated_at actual UTC at execution, supplement_id actual, not guessed now; (4) independent source check next before any execution.")
    (out / "wall-end.txt").write_text(time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()))
    (out / "exit.txt").write_text("0 (plan only, no prepare executed)")

if __name__ == "__main__":
    main()
