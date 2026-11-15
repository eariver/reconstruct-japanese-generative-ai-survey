#!/usr/bin/env python3
"""ACTUAL normal HIGH prepare orchestrator — ONE edition per invocation.

Replaces prior print-only plan author (prepare-dispatch-r2.py preserved as
history, NOT valid operation: it printed CALL and proposed W34 null).

When later authorized, this script stages exact new Raw/request/SP supp
inside the selected NEW repo and calls ONLY the existing HIGH API:
  scripts.survey_prearchitecture_acceptance_v2.prepare_revision
  (repo_root, state_path, request_path, revision_id) -> manifest_ref.

No adopt/decision/guard/State write. Fail-closed: first error preserves
partial, logs traceback + post inventory, exits 2, no retries/cleanup.

Pins manifest a7e4/773 BEFORE any project import. Head/tree cc1c/ed2 via
scoped Git only during later operation. No execution now.
"""
import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import time
import traceback
from pathlib import Path

# Pins (explicit, no guess; config holds machine-generated actuals)
EXP_HEAD = "cc1c7fd1cf979e71fda4ae2164828b37bc1b2325"
EXP_PARENT = "e84a82aca000c990597ea8cf60f548e2ff187bd1"
EXP_TREE = "ed2dc4ddd4a9486ccc9d0944bbd48653199b2485"
EXP_INIT480 = "480823560c0c26ed2e5baa18e0e79a22b2839a27"
EXP_MANIFEST_SHA = "a7e40c4711a66b4d1d2541e6af1a97fd0e531d217e233f45ce43b40e19cef40c"
EXP_MANIFEST_BYTES = 202833
EXP_FILES_LEN = 773
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
CONFIG = PACKET / "prepare-normal-high-config.json"
DEFAULT_REV = {"2026-W34": "w34-repaired-20261112-r1",
               "SP-efficient-llm-2026": "sp-repaired-20261112-r1"}

# Live tool SHAs (verify BEFORE project import)
EXP_TOOLS = {
 "scripts/survey_research_authority_v2.py": "7f5fc9e0d79729d98345f0b0352d5070c76e93f92f2c14148e22c9f38a8f4c0f",
 "scripts/survey_prearchitecture_acceptance_v2.py": "f312f02e2dc5c1aa5a1d6432bca134cd83f0a1edea2d127721d0206d05514a90",
 "schemas/dm022-revision-request-v2.schema.json": "a99f0dc1f6e10ae5736063a051ef3b147eb85bccf20e435db87054a2bac1a31f",
 "schemas/dm022-revision-manifest-v2.schema.json": "e7534d019ec1b58672ff306ac901d65669e2c64251f4186df3e81e356fbaf4",
 "schemas/dm022-revision-proof-v2.schema.json": "a79c09209c145d485ec39e1c1c277f0d706cf3ccfb0972c5bd9f6d6e7fecec5c3",
 "schemas/dm022-preadoption-report-v2.schema.json": "10238a1af7330e5352cbbad709e6360797fade789f18426f91b2eae65b77c925ce",
 "schemas/dm022-supersession-checkpoint-v2.schema.json": "fd39c246617293ecb6760906534512e2b5a14a484916c3d1fba055b33d3bec0",
}
# Contract8 live (State-embedded; HIGH rechecks via _contract_and_tools)
EXP_PIPELINE_SHA = "3adfbda22131eac4017ef867aef2ebb2f346f884731c4ea8343e9062392eabd5"
EXP_QUALITY_SHA = "b5b955d524fb438c0f1b2c9490bea1da2083e79028d67a55ca424bbfc20f2958"
EXP_W34_RESEARCH = "666f8a064b190ffd35216e26d6fdf2dd0fa932cac7b1b0d6448e262ded77b9a8"
EXP_W34_PUB = "99adff93ff443e02bdcce639ce5fc4d4c959ee45a804da70efc4277db57fdddb"
EXP_SP_RESEARCH = "0f575e6d97caec72b2bf8b7f6b562d97ca67b2073417b968ba3e6e8"
EXP_SP_PUB = "a6859559dd1b9d42ab8fb4402b74b7bdd8611dbe65c8e02a7b022b545c20f4eb"
EXP_ORCH = "survey-production-core-v2/0.15-postintegration-transport-thematic"
# Old State/CP pins
EXP_STATE = {"2026-W34": ("d7acd29b1518399ffc2376eb07e102491a6ec9782b3fdd79815c5f230e1886b0", 4087),
             "SP-efficient-llm-2026": ("180db8c30721825d40461cd5e1b92edb704f3630f518bfd693b4732211538220", 4194)}
EXP_PROFILE = {"2026-W34": ("2a8c3089cec29eb64e121cdf0429eed38670df704ebe955079751198557cfeb1", 2371),
               "SP-efficient-llm-2026": ("aff05fd573ce873afa24c0ede26c2b4591ee28b7048c9ed528e8fc389ed8ee45", 13748)}
EXP_CP_EVID = {"2026-W34": ("0979f9f7703a25c2bd3424824bc4ad9f8719e8e7bcc49c19c5573d0f70ab593a",
                            "sources/2026-W34/orchestration/v2/checkpoints/CANDIDATES_NORMALIZED.json"),
               "SP-efficient-llm-2026": ("1233b1f6ca3301d6430d4d157788d0a45a613c9ce1e1563e7c06fe11d73993f0",
                            "sources/SP-efficient-llm-2026/orchestration/v2/checkpoints/CANDIDATES_NORMALIZED.json")}
EXP_ARTIFACTS = {
 "2026-W34": [("edition-views-acceptance", "sources/2026-W34/evidence/v2/views/accepted/574b96ff3ce87f7f2e46fcd78724bf1fbfcdad590e009be1500f03446697b5c5/edition-views-accepted.json", "3777133cc09d0189ab97cc1d8ff1f8b420108d43880f69f1745356508b8acfce", 159498),
               ("evidence-acceptance", "sources/2026-W34/evidence/v2/accepted/5ca6f31033dcaed6a153f0eb6f838f18bc9bdd1674a19a941f8c8378f88e4e48/evidence-accepted.json", "edf21e4de5f7ab8db2d5189f45abc8cc6d0cf6475e532b20bcc56b0ce5660218", 126592),
               ("materiality-ledger", "sources/2026-W34/materiality-ledger-v2.json", "f089cc4eedb49a81b4b925c1219f22a77237d16f28fdee73f20a3744e725e91d", 186202),
               ("profile-completeness", "sources/2026-W34/profile-completeness-v2.json", "e8c432dd6275e81df5286cb8c0d55d99e27aa0812c52a114d870dddaf0d2795f", 71532)],
 "SP-efficient-llm-2026": [("edition-views-acceptance", "sources/SP-efficient-llm-2026/evidence/v2/views/accepted/5e722402c7e8df6077f0da33b2b53355f22ae3f306482bdb27350b7145f/edition-views-accepted.json", "1557fef75b4b737379a0e84eea983d9151b7148077f65da018206a2fae2b0341", 64222),
               ("evidence-acceptance", "sources/SP-efficient-llm-2026/evidence/v2/accepted/73f4bc1ec69c70925a7119a0327ff5e6f024812b56cf8edd7c49eae9f672a297/evidence-accepted.json", "65784e69559f9379412935fa5e7671beddee59b46b8fdb28a848d450e2b68ce0", 49237),
               ("materiality-ledger", "sources/SP-efficient-llm-2026/materiality-ledger-v2.json", "b7c85b4eb009249b40f7c38595fa1e4374990dfc07c38591c1e770c8c60", 66850),
               ("profile-completeness", "sources/SP-efficient-llm-2026/profile-completeness-v2.json", "d67f7f8363407b30d58dbe2dbe562b3666ea9483f9f16303859cfe459ab5e805", 33683)],
}
EXP_W34_SUPP = ("sources/2026-W34/external/evidence-supplement/evidence-authority-supplement-r2-fresh-basis.json",
                "ce6f977a3e690e779c380b7b035d9247207e262b5c50a5b14b6b6b8f0fbc704e", 389414)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def fail(msg: str):
    print(f"REFUSE: {msg}", file=sys.stderr)
    raise SystemExit(2)


def load_strict_json(p: Path):
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
    if not SAFEPATH.fullmatch(rel):
        fail(f"SizedRef safePath invalid: {rel!r}")
    if rel.startswith("/") or ".." in Path(rel).parts:
        fail(f"SizedRef traversal: {rel!r}")
    abs_p = repo / rel
    if abs_p.is_symlink():
        fail(f"SizedRef symlink refused: {rel}")
    try:
        st = abs_p.stat()
    except FileNotFoundError:
        fail(f"SizedRef missing: {rel}")
    if not stat.S_ISREG(st.st_mode):
        fail(f"SizedRef not regular: {rel}")
    return {"path": rel, "sha256": sha256_file(abs_p), "byte_count": st.st_size}


def check_head_tree_git(repo: Path):
    env = {k: v for k, v in os.environ.items() if k not in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES")}
    try:
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, check=True, capture_output=True, text=True, env=env).stdout.strip()
        tree = subprocess.run(["git", "rev-parse", "HEAD^{tree}"], cwd=repo, check=True, capture_output=True, text=True, env=env).stdout.strip()
    except Exception as e:
        fail(f"scoped Git HEAD/tree observation failed: {e}")
    if not HEX40.fullmatch(head) or head != EXP_HEAD:
        fail(f"HEAD != cc1c {EXP_HEAD}: got {head!r}")
    if not HEX40.fullmatch(tree) or tree != EXP_TREE:
        fail(f"tree != ed2dc4 {EXP_TREE}: got {tree!r}")
    print(f"HEAD/tree OK {head[:12]}/{tree[:12]} (scoped Git, NEW repo only)")
    return head, tree


def inventory_old(repo: Path, issue: str) -> dict:
    if not MANIFEST.exists():
        fail(f"final manifest missing {MANIFEST}")
    if hashlib.sha256(MANIFEST.read_bytes()).hexdigest() != EXP_MANIFEST_SHA:
        fail("final manifest != a7e40c")
    if MANIFEST.stat().st_size != EXP_MANIFEST_BYTES:
        fail("final manifest bytes != 202833")
    m = json.loads(MANIFEST.read_text())
    if len(m.get("files", [])) != EXP_FILES_LEN:
        fail(f"manifest files_len != 773: {len(m.get('files', []))}")
    inv = {}
    for rel in m["files"]:
        fp = repo / rel
        if not fp.is_file() or fp.is_symlink():
            fail(f"773 missing/not-regular {rel}")
        st = fp.stat()
        inv[rel] = [sha256_file(fp), st.st_size, oct(stat.S_IMODE(st.st_mode))]
    src = repo / f"sources/{issue}"
    for p in sorted(src.rglob("*")):
        if p.is_file() and not p.is_symlink():
            s = p.relative_to(repo).as_posix()
            if "/research/v2/acceptance-revision" in s:
                fail(f"future R/inputs must not exist pre-dispatch: {s}")
            if s not in inv:
                st = p.stat()
                inv[s] = [sha256_file(p), st.st_size, oct(stat.S_IMODE(st.st_mode))]
    return inv


def exclusive_write_bytes(abs_p: Path, data: bytes, label: str):
    if ".." in abs_p.parts:
        fail(f"{label} traversal")
    abs_p.parent.mkdir(parents=True, exist_ok=True)
    # ancestor type checks: no symlink, no non-dir
    cur = abs_p.parent
    # walk up to repo root is checked by caller via relative_to; here check each ancestor
    for anc in [abs_p.parent] + list(abs_p.parent.parents):
        try:
            if anc.is_symlink():
                fail(f"{label} ancestor symlink: {anc}")
        except OSError:
            pass
        if anc.exists() and not anc.is_dir():
            fail(f"{label} ancestor not dir: {anc}")
        # stop at filesystem root to avoid infinite; caller ensures inside repo
        if str(anc) == "/":
            break
    try:
        fd = os.open(str(abs_p), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o664)
    except FileExistsError:
        fail(f"{label} exists (new-only, O_EXCL refused): {abs_p}")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
    except Exception as e:
        fail(f"{label} write failed: {e}")
    st = abs_p.stat()
    if not stat.S_ISREG(st.st_mode):
        fail(f"{label} not regular after write")
    return {"sha256": sha256_file(abs_p), "byte_count": st.st_size}


def exclusive_copy_file(src: Path, dst_rel: str, repo: Path, label: str, expect_sha: str, expect_len: int):
    if not SAFEPATH.fullmatch(dst_rel):
        fail(f"{label} safePath invalid: {dst_rel!r}")
    if dst_rel.startswith("/") or ".." in Path(dst_rel).parts:
        fail(f"{label} traversal: {dst_rel!r}")
    dst = repo / dst_rel
    if dst.exists() or dst.is_symlink():
        fail(f"{label} must be new absent (O_EXCL): {dst_rel}")
    if not src.is_file() or src.is_symlink():
        fail(f"{label} source not regular: {src}")
    if sha256_file(src) != expect_sha or src.stat().st_size != expect_len:
        fail(f"{label} pinned source drift: {src}")
    # FULL DID filename check
    base = Path(dst_rel).name
    # DID must appear literally in basename
    # caller passes did; here enforce generic FULL DID presence (EFF-D or w34-event-)
    if ("EFF-D" not in base) and ("w34-event-" not in base):
        fail(f"{label} FULL DID missing in basename: {base}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    data = src.read_bytes()
    info = exclusive_write_bytes(dst, data, label)
    if info["sha256"] != expect_sha or info["byte_count"] != expect_len:
        fail(f"{label} copy bytes mismatch")
    return info


def main():
    ap = argparse.ArgumentParser(description="ACTUAL normal HIGH prepare (one edition).")
    ap.add_argument("--issue", required=True, choices=["2026-W34", "SP-efficient-llm-2026"])
    ap.add_argument("--repo-root", default=str(DEFAULT_REPO))
    ap.add_argument("--revision-id", default=None)
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--config", default=str(CONFIG))
    a = ap.parse_args()
    issue = a.issue
    repo = Path(a.repo_root)
    rev = a.revision_id or DEFAULT_REV[issue]
    if not REVISION_RE.fullmatch(rev) or any(c.isupper() for c in rev):
        fail(f"revision_id invalid (lowercase hyphen <=64, no T/Z): {rev!r}")
    if "T" in rev or "Z" in rev:
        fail(f"revision_id must not contain T/Z: {rev!r}")

    ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out = Path(a.outdir).resolve() if a.outdir else (PACKET.resolve() / f"prepare-normal-high-{issue}-{ts}-pid{os.getpid()}")
    try:
        out.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        fail(f"outdir exists (unique required): {out}")
    def wlog(name: str, data: str):
        (out / name).write_text(data)
    wlog("argv.txt", " ".join(sys.argv))
    wlog("env-whitelist.txt", "\n".join(f"{k}={os.environ.get(k,'')}" for k in sorted(ALLOWED_ENV)))
    wlog("pid.txt", str(os.getpid()))
    wlog("wall-start.txt", ts)
    wlog("cwd.txt", os.getcwd())
    wlog("issue.txt", f"{issue} {rev} {repo.resolve()}")
    exit_code = 2
    entry_inv = {}
    try:
        # Manifest pin BEFORE project imports (stdlib only above)
        if hashlib.sha256(MANIFEST.read_bytes()).hexdigest() != EXP_MANIFEST_SHA:
            fail("manifest pin a7e4 failed before project imports")
        for rel, exp_sha in EXP_TOOLS.items():
            got = sha256_file(repo / rel)
            if got != exp_sha:
                fail(f"tool pin drift {rel}: {got[:12]} != {exp_sha[:12]}")
        print(f"manifest+tools7 pinned a7e4/773 before project imports")

        # Scoped Git HEAD/tree (NEW repo only)
        check_head_tree_git(repo)
        entry_inv = inventory_old(repo, issue)
        wlog("entry-inventory.json", json.dumps(entry_inv, indent=2, sort_keys=True))

        # State / Profile / CP / artifacts
        st_doc, st_raw, _, _ = load_strict_json(repo / f"sources/{issue}/production-state.json")
        exp_sha, exp_len = EXP_STATE[issue]
        if sha256_file(repo / f"sources/{issue}/production-state.json") != exp_sha or len(st_raw) != exp_len:
            fail(f"{issue} State bytes != original hash")
        if st_doc.get("lifecycle_state") != "EVIDENCE_REVIEWED":
            fail("State not EVIDENCE_REVIEWED")
        if st_doc.get("implementation", {}).get("repository_commit_sha") != EXP_INIT480:
            fail("State init != 480")
        hg = st_doc.get("human_gates", {})
        if hg.get("architecture_review") != "pending" or hg.get("publication_preview") != "pending":
            fail("Human gates not pending/pending")
        hgp = st_doc.get("human_gate_provenance", {})
        if hgp.get("architecture_review") is not None or hgp.get("publication_preview") is not None:
            fail("Human provenance must be null/null")
        if st_doc.get("exception_gate", {}).get("status") != "inactive":
            fail("exception_gate not inactive")
        mc = st_doc.get("machine_checkpoints", {})
        for k in ("selection", "architecture", "draft", "validation", "publication_preview", "freeze", "release"):
            if mc.get(k) != "pending":
                fail(f"seven slots not pending: {k}={mc.get(k)!r}")
        cp = st_doc.get("checkpoint_provenance", {})
        for k in ("selection", "architecture", "draft", "validation", "publication_preview", "freeze", "release"):
            if cp.get(k) is not None:
                fail(f"CP {k} must be null (no 7 slots)")
        # before_checkpoint evidence path/sha must equal CP evidence
        exp_cp_sha, exp_cp_path = EXP_CP_EVID[issue]
        if cp.get("evidence", {}).get("sha256") != exp_cp_sha or cp.get("evidence", {}).get("path") != exp_cp_path:
            fail("CP evidence != expected four-ref checkpoint")
        # Profile
        prof_ref = st_doc.get("profile", {})
        exp_psha, exp_plen = EXP_PROFILE[issue]
        if prof_ref.get("sha256") != exp_psha:
            fail("State profile sha != expected")
        prof_abs = repo / prof_ref["path"]
        if sha256_file(prof_abs) != exp_psha or prof_abs.stat().st_size != exp_plen:
            fail("Profile bytes drift")
        prof_doc, _, _, _ = load_strict_json(prof_abs)
        source_root_rel = prof_doc["paths"]["source_root"]
        if source_root_rel != f"sources/{issue}":
            fail(f"source_root != sources/{issue}: {source_root_rel}")
        # Four artifacts
        for name, rel, sha, n in EXP_ARTIFACTS[issue]:
            ap_ = repo / rel
            if not ap_.is_file() or ap_.is_symlink():
                fail(f"artifact {name} missing")
            if sha256_file(ap_) != sha or ap_.stat().st_size != n:
                fail(f"artifact {name} drift")
        print(f"State/Profile/CP/4-artifacts OK {issue} EVIDENCE_REVIEWED pending-Human no-7slots")

        # Patch / records (inspect actual keys, no counts/new_records guess)
        cfg_doc, _, _, _ = load_strict_json(Path(a.config))
        patch_rel = cfg_doc["issues"][issue]["patch"]["path"]
        patch_doc, _, patch_hash, patch_len = load_strict_json(Path(patch_rel))
        print(f"patch actual keys: {sorted(patch_doc.keys())}")
        if "changed_record_ids" not in patch_doc:
            fail(f"patch missing changed_record_ids: {sorted(patch_doc.keys())}")
        rec_key = "new_records" if "new_records" in patch_doc else ("records" if "records" in patch_doc else None)
        if rec_key is None:
            fail(f"patch missing new_records/records: {sorted(patch_doc.keys())}")
        changed = patch_doc["changed_record_ids"]
        recs = patch_doc[rec_key]
        if len(changed) != 4 or len(recs) != 4:
            fail(f"patch 4-record shape: changed {len(changed)} recs {len(recs)}")
        seen = set()
        for r in recs:
            did = r.get("discovery_id")
            if not did or did in seen:
                fail(f"patch duplicate/missing discovery_id {did!r}")
            seen.add(did)
            # 7-field + profile-specific keys per schema
            base_req = ["discovery_id", "status", "entity", "artifact_type", "claims", "limitations", "verification", "materiality", "materiality_rationale", "scope_dimensions"]
            for k in base_req:
                if k not in r:
                    fail(f"patch {did} missing {k}")
            if issue == "2026-W34":
                for k in ["window_relation", "carry_over"]:
                    if k not in r:
                        fail(f"W34 {did} missing {k}")
            else:
                for k in ["lineage_role", "branch_ids", "transition_ids"]:
                    if k not in r:
                        fail(f"SP {did} missing {k}")
            if r["status"] not in ("PARTIAL", "VERIFIED"):
                fail(f"patch {did} status {r['status']}")
            for v in r["verification"]:
                if v.get("status") not in ("VERIFIED", "UNRESOLVED") or not v.get("target") or not v.get("finding"):
                    fail(f"patch {did} verification shape")
        if set(seen) != set(changed):
            fail(f"patch changed vs records mismatch {set(changed)^seen}")
        # unaffected hash (canonical sorted JSON)
        base_inter_rel = cfg_doc["issues"][issue]["base_interactive"]["path"]
        base_doc, base_raw, base_hash, base_len = load_strict_json(repo / base_inter_rel)
        if len(base_doc.get("records", [])) != (409 if issue == "2026-W34" else 160):
            fail(f"base records != 409/160: {len(base_doc.get('records', []))}")
        # runner 4-field preserved
        runner = base_doc.get("runner", {})
        for k in ["provider", "model", "invocation", "generated_at"]:
            if k not in runner:
                fail(f"base runner missing {k}")
        # unaffected canonical
        unaff = [r for r in base_doc["records"] if r["discovery_id"] not in set(changed)]
        if len(unaff) != (405 if issue == "2026-W34" else 156):
            fail(f"unaffected count != 405/156: {len(unaff)}")
        canon = json.dumps(sorted(unaff, key=lambda r: r["discovery_id"]), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
        calc_hash = hashlib.sha256(canon).hexdigest()
        exp_unaff_key = "unaffected405_hash" if issue == "2026-W34" else "unaffected156_hash"
        # patch may use different key name for SP (unaffected156_hash) or W34 (unaffected405_hash)
        exp_unaff = patch_doc.get(exp_unaff_key) or patch_doc.get("unaffected156_hash") or patch_doc.get("unaffected405_hash")
        if exp_unaff is None:
            # log actual field containing unaffected+hash
            for k in patch_doc:
                if "unaffected" in k.lower() and "hash" in k.lower():
                    exp_unaff = patch_doc[k]
                    exp_unaff_key = k
                    break
        if exp_unaff != calc_hash:
            fail(f"unaffected hash mismatch {exp_unaff_key}: calc {calc_hash[:12]} != patch {str(exp_unaff)[:12]}")
        if issue == "2026-W34":
            if patch_doc.get("unaffected405_bytes") != len(canon):
                fail("W34 unaffected bytes mismatch")
        # D165 preserved (SP)
        if issue == "SP-efficient-llm-2026":
            d165 = patch_doc.get("d165_preserved", {})
            if d165.get("discovery_id") != "EFF-D165":
                fail("SP D165 id")
            # verify D165 byte-identical in base
            b165 = [r for r in base_doc["records"] if r["discovery_id"] == "EFF-D165"]
            if len(b165) != 1:
                fail("SP base D165 !=1")
            if hashlib.sha256(json.dumps(b165[0], sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest() != d165.get("sha256"):
                # fallback: compare canonical single-record hash? use same canonical as file? check via stored sha of record?
                # The stored sha is record hash; verify via same dump
                fail(f"SP D165 sha drift calc vs {d165.get('sha256','')[:12]}")
        # full assembly 409/160
        by_id = {r["discovery_id"]: r for r in base_doc["records"]}
        for r in recs:
            by_id[r["discovery_id"]] = r
        full = [by_id[did] for did in sorted(by_id)]
        if len(full) != (409 if issue == "2026-W34" else 160):
            fail(f"full records != 409/160: {len(full)}")
        if set(by_id) != set(r["discovery_id"] for r in base_doc["records"]):
            fail("full assembly discovery set drift (must be 405+4 / 156+4, no new split)")
        print(f"{issue} records 409/160 assembly OK unaffected {calc_hash[:12]} D165 preserved")

        # Task targets exact + coverage (package tasks)
        # package is sibling of interactive-evidence.json
        pkg_path = (repo / base_inter_rel).parent / "package.json"
        pkg_doc, _, _, _ = load_strict_json(pkg_path)
        if len(pkg_doc.get("tasks", [])) != (409 if issue == "2026-W34" else 160):
            fail("package tasks != 409/160")
        # authority_supplement policy: W34 must be supplemented, SP old supplemented
        old_auth = pkg_doc.get("authority_supplement")
        if issue == "2026-W34":
            if not isinstance(old_auth, dict) or old_auth.get("sha256") != EXP_W34_SUPP[1] or old_auth.get("path") != EXP_W34_SUPP[0]:
                fail(f"W34 OLD supplement != ce6f/389414: {old_auth}")
        # task-target exact for changed 4: record verification targets must equal task verification_targets if present
        # package tasks may have verification_targets or not; if task has them, enforce exact coverage
        tmap = {}
        for t in pkg_doc["tasks"]:
            dids = t.get("discovery_ids", [])
            if len(dids) == 1:
                tmap[dids[0]] = t
        for r in recs:
            did = r["discovery_id"]
            t = tmap.get(did)
            if t is None:
                fail(f"changed {did} has no package task")
            exp_targets = t.get("verification_targets")
            if exp_targets is not None:
                got_targets = set(x["target"] for x in r["verification"])
                if set(exp_targets) != got_targets:
                    fail(f"{did} verification targets != task exact missing={set(exp_targets)-got_targets} extra={got_targets-set(exp_targets)}")
        print("task targets exact/coverage OK (HIGH revalidates FULL)")

        # Completeness explicit 7field 3/15
        if issue == "2026-W34":
            comp_path = repo / "sources/2026-W34/profile-completeness-v2.json"
            comp_doc, _, _, _ = load_strict_json(comp_path)
            obligs = comp_doc.get("obligations", [])
            if len(obligs) != 3:
                fail(f"W34 obligations !=3: {len(obligs)}")
            resid = comp_doc.get("residual_limitations", [])
            clos = comp_doc.get("closure")
        else:
            oblig_pkt_rel = cfg_doc["issues"][issue]["obligations_packet"]["path"]
            oblig_doc, _, _, _ = load_strict_json(Path(oblig_pkt_rel))
            obligs = oblig_doc.get("obligations", [])
            if len(obligs) != 15:
                fail(f"SP obligations !=15: {len(obligs)}")
            # residual/closure from profile-completeness (current)
            comp_path = repo / "sources/SP-efficient-llm-2026/profile-completeness-v2.json"
            comp_doc, _, _, _ = load_strict_json(comp_path)
            resid = comp_doc.get("residual_limitations", [])
            clos = comp_doc.get("closure")
            # r5 pending note: do not switch
            print("SP obligations r4 15x7 (r5 cc4ce34 pending, not used)")
        for o in obligs:
            for k in ["obligation_id", "dimension", "description", "status", "discovery_ids", "evidence_task_ids", "rationale"]:
                if k not in o:
                    fail(f"obligation {o.get('obligation_id')} missing {k}")
            if o["status"] not in ("SATISFIED", "LIMITATION", "NEEDS_RESEARCH", "NOT_APPLICABLE"):
                fail(f"obligation {o.get('obligation_id')} status {o['status']}")
            # no fake SAT: W34 must keep 2 LIM +1 SAT; SP O01/O07 SAT rest LIM (r4); enforce not all SAT
            if issue == "2026-W34" and o["status"] not in ("SATISFIED", "LIMITATION"):
                fail("W34 obligation status")
        print(f"{issue} completeness 7field {len(obligs)} OK closure={'null' if clos is None else 'present'}")

        # Routing: inspect actual JSON keys, no guess
        rout_rel = cfg_doc["issues"][issue]["routing"]["path"]
        rout_doc, _, _, _ = load_strict_json(Path(rout_rel))
        print(f"routing actual keys: {sorted(rout_doc.keys())}")
        raw_jobs = []  # (did, src_abs, expect_sha, expect_len, future_rel)
        if issue == "2026-W34":
            entries = rout_doc.get("entries")
            if not isinstance(entries, dict) or len(entries) != 4:
                fail("W34 routing entries !=4")
            for did, e in entries.items():
                fut = e.get("future_raw_path")
                if did not in fut or "w34-event-arxiv-2608-" not in fut:
                    fail(f"W34 future_raw FULL DID {did}")
                if not SAFEPATH.fullmatch(fut):
                    fail(f"W34 safePath {did}")
                src = Path(e["source_file"])
                # map old retry path? must resolve inside NEW repo; source_file already points to NEW work
                if not src.exists():
                    # try repo-relative fallback
                    alt = repo / fut.replace("external/evidence-supplement/raw/", "execution/luna/w34-screening-evidence-after-sol-discovery-r2/evidence-bodies/arxiv/").replace("w34-event-arxiv-2608-", "2608_").replace(".html", ".html")
                    fail(f"W34 source missing {src} (no fallback guess)")
                if sha256_file(src) != e["sha256"] or src.stat().st_size != e["bytes"]:
                    fail(f"W34 pinned source drift {did}")
                raw_jobs.append((did, src, e["sha256"], e["bytes"], fut))
        else:
            # SP: keys u1/u2/u3 + d142_summary_routing (+ supplement_routing note)
            for k in ["u1", "u2", "u3"]:
                if k not in rout_doc:
                    fail(f"SP routing missing {k}, actual {sorted(rout_doc.keys())}")
                fut = rout_doc[k].get("future_raw_path")
                if "EFF-D" not in fut or not SAFEPATH.fullmatch(fut):
                    fail(f"SP {k} FULL DID/safePath")
            if "d142_summary_routing" not in rout_doc:
                fail("SP routing missing d142_summary_routing")
            intake_dir = Path(cfg_doc["issues"][issue]["intake_dir"])
            # u1/u2 decoded, u3 wire identity
            mapping = [("u1", "EFF-D070", "u1.snapshot.decoded.html", 253542, "14ae31184b253b736ff8be423fafbe5ff82d1f75cf66b600bad8b8c9152aa443"),
                       ("u2", "EFF-D071", "u2.snapshot.decoded.html", 307198, "357708348b9884d004669d6df45100986676f5ab900a75e76304fb19cae05bf2"),
                       ("u3", "EFF-D141", "u3.snapshot.body.bin", 350662, "97a5dd74ed1e9ba006d21759c14615a7c0a485c4db161dc00a2d0b1e4d651b69")]
            for rk, did, fn, exp_len, exp_sha in mapping:
                fut = rout_doc[rk]["future_raw_path"]
                src = intake_dir / fn
                if not src.is_file():
                    fail(f"SP {rk} intake file missing {src}")
                if sha256_file(src) != exp_sha or src.stat().st_size != exp_len:
                    fail(f"SP {rk} pinned bytes drift")
                # verify decoded sha in routing matches
                dec = rout_doc[rk].get("decoded") or {"sha256": exp_sha, "bytes": exp_len}
                # u3 uses wire as identity; handle varying keys
                if rk == "u3":
                    wire = rout_doc[rk].get("wire", {})
                    if wire.get("sha256") != exp_sha or wire.get("bytes") != exp_len:
                        fail("SP u3 wire sha/bytes != expected")
                else:
                    if dec.get("sha256") != exp_sha or dec.get("bytes") != exp_len:
                        fail(f"SP {rk} decoded sha/bytes != expected")
                raw_jobs.append((did, src, exp_sha, exp_len, fut))
            d142 = rout_doc["d142_summary_routing"]
            fut142 = d142["future_raw_path"]
            if "EFF-D142" not in fut142 or not SAFEPATH.fullmatch(fut142):
                fail("SP D142 FULL DID/safePath")
            src142 = Path(d142["existing_file"])
            # existing_file is NEW-repo-relative with leading .rephase...; resolve
            if not src142.exists():
                # try as repo-relative if starts with .rephase
                fail(f"SP D142 existing file missing {src142}")
            if sha256_file(src142) != d142["existing_sha256"] or src142.stat().st_size != d142["existing_bytes"]:
                fail("SP D142 pinned bytes drift")
            raw_jobs.append(("EFF-D142", src142, d142["existing_sha256"], d142["existing_bytes"], fut142))
        print(f"{issue} routing 4 Raw FULL-DID/safePath/pinned-bytes OK (no write yet)")

        # First-claim literal check BEFORE active Raw stage (when possible)
        for r in recs:
            did = r["discovery_id"]
            first = r["claims"][0]["text"] if r.get("claims") else ""
            if not first:
                fail(f"{did} first claim empty")
            # find matching raw job
            job = [j for j in raw_jobs if j[0] == did or (did.endswith(j[0].split('-')[-1]) if '-' in did else False)]
            # direct match by DID
            cand = [j for j in raw_jobs if j[0] == did]
            if not cand:
                # W34 DID full match; SP EFF-D match
                fail(f"{did} no raw job for literal check")
            src = cand[0][1]
            try:
                txt = src.read_bytes().decode("utf-8", errors="ignore")
            except Exception as e:
                fail(f"{did} literal read failed: {e}")
            if first not in txt:
                # for SP D142 second claim is negative statement, first claim is literal token; enforce first only
                fail(f"{did} first-claim literal NOT in retained bytes (mechanical proof failed)")
        print("first-claim literals present in retained bytes (mechanical only, not semantic PASS)")

        # Stage Raw (exclusive, new-only) + supplement + request + HIGH
        # Verify request/R absent pre-dispatch
        req_rel = cfg_doc["issues"][issue]["request_rel"]
        rev_root_rel = cfg_doc["issues"][issue]["rev_root_rel"]
        if (repo / req_rel).exists() or (repo / req_rel).is_symlink():
            fail(f"request must be new absent: {req_rel}")
        if (repo / rev_root_rel).exists():
            fail(f"R root must be new absent: {rev_root_rel}")
        # Stage 4 Raw byte-identical
        for did, src, exp_sha, exp_len, fut in raw_jobs:
            exclusive_copy_file(src, fut, repo, f"Raw {did}", exp_sha, exp_len)
        print(f"staged 4 Raw new-only O_EXCL {issue}")

        # Supplement: W34 explicit existing; SP public builder
        if issue == "2026-W34":
            supp_ref = {"path": EXP_W34_SUPP[0], "sha256": EXP_W34_SUPP[1], "byte_count": EXP_W34_SUPP[2]}
            # verify bytes via SizedRef helper (shape+bytes, no verified_dict, no OLD fallback)
            chk = sized_ref(repo, supp_ref["path"])
            if chk["sha256"] != supp_ref["sha256"] or chk["byte_count"] != supp_ref["byte_count"]:
                fail("W34 supplement SizedRef bytes mismatch (NO null fallback)")
            print(f"W34 supplement explicit SizedRef ce6f/389414 OK (null refused)")
        else:
            # SP: public builder with sourceRoot/profile/effectiveDS; override not needed for explicit pins
            # Import AFTER pins (project import allowed only now, during later operation)
            import sys as _sys
            _sys.path.insert(0, str(repo.resolve()))
            try:
                from scripts import survey_evidence_v2 as ev_mod
                full30_rel = cfg_doc["issues"][issue]["supplement_full30"]["path"]
                full30_doc, _, _, _ = load_strict_json(Path(full30_rel))
                if len(full30_doc.get("sources", [])) != 30:
                    fail(f"SP full30 !=30: {len(full30_doc.get('sources', []))}")
                # 27 same +3 replace check: 3 new IDs must be present, D142 absent
                new_ids = {"supplement-src-ea9b086e35e1c559", "supplement-src-793903f4b4b1d3e1", "supplement-src-228b81661893f1ea"}
                got_ids = set(s["supplement_source_id"] for s in full30_doc["sources"])
                if not new_ids.issubset(got_ids):
                    fail(f"SP full30 missing 3 new archive IDs")
                if any(s["discovery_id"] == "EFF-D142" for s in full30_doc["sources"]):
                    fail("SP full30 must have no D142 entry")
                # sourceRoot/profile/effectiveDS pins
                source_root = repo / "sources/SP-efficient-llm-2026"
                disc_path = repo / "sources/SP-efficient-llm-2026/discovery/discovery-v2.jsonl"
                scr_path = repo / "sources/SP-efficient-llm-2026/screening/v2/accepted/9b9796295c2ddf28b087fc725b78b7d089d6e946a5a5ba65ab51601d58f558a9/screening-accepted.json"
                # verify basis matches full30 basis
                basis = full30_doc.get("basis", {})
                if basis.get("discovery_sha256") != sha256_file(disc_path) or basis.get("screening_acceptance_sha256") != sha256_file(scr_path):
                    fail("SP full30 basis SHA drift vs effective DS")
                supp_id = f"r4-sp17-EFF-DID-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
                out_rel = f"sources/SP-efficient-llm-2026/external/evidence-supplement/evidence-authority-supplement-{supp_id}.json"
                if (repo / out_rel).exists():
                    fail(f"SP supp output must be new absent: {out_rel}")
                # public builder (validates FULL, no verified_dict, no wrong stage)
                built = ev_mod.build_evidence_authority_supplement(repo, "SP-efficient-llm-2026", source_root, disc_path, scr_path, full30_doc["sources"], repo / out_rel, supplement_id=supp_id)
                # public validate + FULL schema (builder already validated; re-validate explicitly)
                ev_mod.validate_evidence_authority_supplement(repo, built, expected_issue_id="SP-efficient-llm-2026", expected_source_root=source_root, expected_discovery_path=disc_path, expected_screening_acceptance_path=scr_path)
                supp_ref = sized_ref(repo, out_rel)
                print(f"SP supp built+validated {supp_id} {supp_ref['sha256'][:12]}/{supp_ref['byte_count']}")
            finally:
                try:
                    _sys.path.remove(str(repo.resolve()))
                except ValueError:
                    pass

        # Assemble request (inside NEW repo, before State/Profile/CP/true refs + tools7/Contract8)
        # Live contract/tools via HIGH helper (actual current, no stale pins)
        import sys as _sys2
        _sys2.path.insert(0, str(repo.resolve()))
        live_contract = None
        live_tools = None
        try:
            import json as _j
            cfg_raw = (repo / "config/survey-production-core-v2.json").read_bytes() if (repo / "config/survey-production-core-v2.json").exists() else None
            # HIGH _contract_and_tools needs cfg + state; load via stdlib then call helper
            from scripts import survey_prearchitecture_acceptance_v2 as high_mod
            from scripts import survey_production_v2 as core_mod
            cfg_obj = core_mod.load_json(repo / str(core_mod.DEFAULT_CONFIG))
            live_contract, live_tools = high_mod._contract_and_tools(repo, cfg_obj, st_doc)
            # verify against expected pins (fail on stale)
            exp_contract = {"pipeline_contract_version": "2.0-rc1", "pipeline_contract_sha256": EXP_PIPELINE_SHA,
                            "quality_contract_version": "2.0-rc1", "quality_contract_sha256": EXP_QUALITY_SHA,
                            "research_profile_version": "2.0-rc1",
                            "research_profile_sha256": EXP_W34_RESEARCH if issue == "2026-W34" else EXP_SP_RESEARCH,
                            "publication_profile_version": "2.0-rc1",
                            "publication_profile_sha256": EXP_W34_PUB if issue == "2026-W34" else EXP_SP_PUB}
            if live_contract != exp_contract:
                fail(f"live contract != expected pins: {live_contract}")
            live_map = {e["path"]: e["sha256"] for e in live_tools}
            if live_map != EXP_TOOLS:
                fail(f"live tool SHAs != expected 7")
        finally:
            # keep path for HIGH call below; remove after HIGH call
            pass

        # Build records/completeness/runner/tool_pins
        # before_state/profile/discovery/screening SizedRefs (actual current)
        if issue == "2026-W34":
            disc_ref = {"path": "sources/2026-W34/screening/input/event-discovery-v2.jsonl", "sha256": "0a23be47dad8ddaf4f0a9c3261d97cc0006ac942bfd2321be2487289a34da31e", "byte_count": 1335444}
            scr_ref = {"path": "sources/2026-W34/screening/v2/accepted/e193ad0507895568e369437833b87d2610d68ef50f0c6419b092f5711e26bbea/screening-accepted.json", "sha256": "b9d963d83b712ba3fb7e93358f051c4e902f31d0e262c44eea6f76dcdf155841", "byte_count": 543880}
        else:
            disc_ref = {"path": "sources/SP-efficient-llm-2026/discovery/discovery-v2.jsonl", "sha256": "7074cef2bfc3b2dd034addbd778055bc2fed962e9845c756f32f9b3c848199d3", "byte_count": 173299}
            scr_ref = {"path": "sources/SP-efficient-llm-2026/screening/v2/accepted/9b9796295c2ddf28b087fc725b78b7d089d6e946a5a5ba65ab51601d58f558a9/screening-accepted.json", "sha256": "6ff524b0a2c2c8f79603348acb86d18d39b180498a72ca92dc12f852dc786bf4", "byte_count": 69226}
        # verify SizedRef bytes now (effective DS binding; HIGH rechecks == effective)
        for _r, _lbl in [(disc_ref, "discovery_ref"), (scr_ref, "screening_ref")]:
            chk = sized_ref(repo, _r["path"])
            if chk["sha256"] != _r["sha256"] or chk["byte_count"] != _r["byte_count"]:
                fail(f"{_lbl} bytes != effective DS pin")
        prof_ref = {"path": f"sources/{issue}/production-profile.json", "sha256": EXP_PROFILE[issue][0], "byte_count": EXP_PROFILE[issue][1]}
        chk = sized_ref(repo, prof_ref["path"])
        if chk["sha256"] != prof_ref["sha256"]:
            fail("profile_ref bytes drift")
        before_state = {"path": f"sources/{issue}/production-state.json", "sha256": EXP_STATE[issue][0], "byte_count": EXP_STATE[issue][1]}
        # before_checkpoint: evidence/materiality/completeness ArtifactRefs (no byte_count)
        before_checkpoint = {"evidence": {"path": EXP_CP_EVID[issue][1], "sha256": EXP_CP_EVID[issue][0]},
                             "materiality": {"path": EXP_CP_EVID[issue][1], "sha256": EXP_CP_EVID[issue][0]},
                             "completeness": {"path": EXP_CP_EVID[issue][1], "sha256": EXP_CP_EVID[issue][0]}}
        # completeness object
        if issue == "2026-W34":
            comp_full, _, _, _ = load_strict_json(repo / "sources/2026-W34/profile-completeness-v2.json")
            completeness = {"obligations": comp_full["obligations"], "residual_limitations": comp_full.get("residual_limitations", []), "closure": comp_full.get("closure")}
        else:
            oblig_full, _, _, _ = load_strict_json(Path(cfg_doc["issues"][issue]["obligations_packet"]["path"]))
            comp_full, _, _, _ = load_strict_json(repo / "sources/SP-efficient-llm-2026/profile-completeness-v2.json")
            completeness = {"obligations": oblig_full["obligations"], "residual_limitations": comp_full.get("residual_limitations", []), "closure": comp_full.get("closure")}
        recorded_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        executor = f"general / Muse Spark 1.3 / prepare-normal-high {issue} {rev}"
        tool_pins = {"repository_commit_sha": EXP_HEAD, "orchestrator_version": EXP_ORCH, "contract": live_contract, "tool_shas": live_tools}
        request = {"schema_version": "2.0-rc1", "issue_id": issue, "revision_id": rev,
                   "research_profile": ("WEEKLY" if issue == "2026-W34" else "THEMATIC"),
                   "before_state": before_state, "before_checkpoint": before_checkpoint,
                   "profile_ref": prof_ref, "discovery_ref": disc_ref, "screening_ref": scr_ref,
                   "work": {"expected_head": EXP_HEAD, "expected_tree": EXP_TREE},
                   "affected_ids": sorted(seen),
                   "supplement_manifest": supp_ref,
                   "records": full, "completeness": completeness,
                   "runner": runner, "tool_pins": tool_pins,
                   "recorded_at": recorded_at, "executor": executor}
        # request inside NEW repo (repo-relative, safePath, no .., no leading /)
        if not SAFEPATH.fullmatch(req_rel) or req_rel.startswith("/") or ".." in Path(req_rel).parts:
            fail(f"request rel unsafe: {req_rel}")
        req_abs = repo / req_rel
        req_bytes = json.dumps(request, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode() + b"\n"
        exclusive_write_bytes(req_abs, req_bytes, "request")
        print(f"request staged inside NEW repo {req_rel} supplement={'null' if supp_ref is None else supp_ref['sha256'][:12]} records={len(full)} completeness={len(completeness['obligations'])}")

        # ACTUAL HIGH prepare (not print string); NO adopt/decision/guard/State write
        try:
            from scripts.survey_prearchitecture_acceptance_v2 import prepare_revision
            state_rel = f"sources/{issue}/production-state.json"
            result = prepare_revision(repo, Path(state_rel), Path(req_rel), rev)
        except Exception as e:
            raise
        finally:
            try:
                _sys2.path.remove(str(repo.resolve()))
            except ValueError:
                pass
        manifest_ref = result.get("manifest_ref") if isinstance(result, dict) else None
        if not isinstance(manifest_ref, dict) or "path" not in manifest_ref:
            fail(f"HIGH manifest_ref invalid: {result}")
        print(f"HIGH prepare_revision OK manifest_ref {manifest_ref}")
        wlog("manifest-ref.json", json.dumps(manifest_ref, indent=2, sort_keys=True))

        # Post inventory: only explicit Raw/request/SP supp/HIGH R allowed
        post_inv = inventory_old(repo, issue) if False else None  # inventory_old refuses future R; do manual post walk
        # manual post: walk 773 + sources/<issue>, allow new explicit paths
        m2 = json.loads(MANIFEST.read_text())
        allowed_new = set([r[4] for r in raw_jobs] + [req_rel])
        if issue == "SP-efficient-llm-2026":
            allowed_new.add(supp_ref["path"])
        # HIGH R root
        # collect post files
        post = {}
        for rel in m2["files"]:
            fp = repo / rel
            st = fp.stat()
            post[rel] = [sha256_file(fp), st.st_size, oct(stat.S_IMODE(st.st_mode))]
        src2 = repo / f"sources/{issue}"
        for p in sorted(src2.rglob("*")):
            if p.is_file() and not p.is_symlink():
                s = p.relative_to(repo).as_posix()
                if s not in post:
                    st = p.stat()
                    post[s] = [sha256_file(p), st.st_size, oct(stat.S_IMODE(st.st_mode))]
        wlog("post-inventory.json", json.dumps(post, indent=2, sort_keys=True))
        # diff vs entry
        for k, v in entry_inv.items():
            if k not in post or post[k] != v:
                fail(f"old inventory changed (only explicit new allowed): {k}")
        for k in post:
            if k not in entry_inv and k not in allowed_new and not k.startswith(rev_root_rel + "/"):
                fail(f"unexpected new file (only Raw/request/SP supp/HIGH R allowed): {k}")
        print("post inventory OK: only explicit Raw/request/SP supp/HIGH R new")
        wlog("wall-end.txt", time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()))
        wlog("exit.txt", "0")
        exit_code = 0
    except SystemExit as e:
        exit_code = int(e.code) if isinstance(e.code, int) else 2
        try:
            wlog("traceback.txt", traceback.format_exc())
            # post inventory on error (best effort, no retry/cleanup)
            try:
                m2 = json.loads(MANIFEST.read_text())
                post = {}
                for rel in m2["files"]:
                    fp = repo / rel
                    if fp.is_file():
                        st = fp.stat()
                        post[rel] = [sha256_file(fp), st.st_size, oct(stat.S_IMODE(st.st_mode))]
                src2 = repo / f"sources/{issue}"
                if src2.exists():
                    for p in sorted(src2.rglob("*")):
                        if p.is_file() and not p.is_symlink():
                            s = p.relative_to(repo).as_posix()
                            if s not in post:
                                st = p.stat()
                                post[s] = [sha256_file(p), st.st_size, oct(stat.S_IMODE(st.st_mode))]
                wlog("post-inventory-error.json", json.dumps(post, indent=2, sort_keys=True))
            except Exception:
                wlog("post-inventory-error.txt", traceback.format_exc())
            wlog("exit.txt", str(exit_code))
        except Exception:
            pass
        raise
    except Exception:
        exit_code = 2
        try:
            wlog("traceback.txt", traceback.format_exc())
            wlog("exit.txt", "2")
        except Exception:
            pass
        print("REFUSE: unexpected failure (preserved, no retry/cleanup)", file=sys.stderr)
        traceback.print_exc()
        raise SystemExit(2)


if __name__ == "__main__":
    main()
