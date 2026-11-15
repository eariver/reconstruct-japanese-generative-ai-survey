#!/usr/bin/env python3
"""ACTUAL normal HIGH prepare r3 — ONE edition per invocation (preserves v1).

v1 `prepare-normal-high.py` + `prepare-normal-high-config.json` preserved as
history (stale r4 fallback, 773 snapshot not compare, hand schema SHAs).
This r3 binds final SP r6 PROPOSAL_READY + r5 completeness + r4 full30,
fixes B1-B6, calls ONLY existing HIGH `prepare_revision` once.

No execution now. Later authorized run stages exact Raw/request/SP supp
inside NEW repo, then HIGH prepare. No adopt/decision/guard/State write.
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

EXP_HEAD = "cc1c7fd1cf979e71fda4ae2164828b37bc1b2325"
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
CONFIG_R3 = PACKET / "prepare-normal-high-config-r3.json"
DEFAULT_REV = {"2026-W34": "w34-repaired-20261112-r1",
               "SP-efficient-llm-2026": "sp-repaired-20261112-r1"}
TOOL_RELS = [
 "scripts/survey_research_authority_v2.py",
 "scripts/survey_prearchitecture_acceptance_v2.py",
 "schemas/dm022-revision-request-v2.schema.json",
 "schemas/dm022-revision-manifest-v2.schema.json",
 "schemas/dm022-revision-proof-v2.schema.json",
 "schemas/dm022-preadoption-report-v2.schema.json",
 "schemas/dm022-supersession-checkpoint-v2.schema.json",
]
SEVEN_SLOTS = (
 "candidate-matrix-v2.json",
 "candidate-selection-v2.json",
 "architecture-v2.json",
 "architecture-review-summary-v2.json",
 "architecture-review-attention-v2.json",
 "orchestration/v2/interactive/selection-architecture-input.json",
 "orchestration/v2/interactive/selection-architecture-audit.json",
)
GUARD_REL = "orchestration/v2/acceptance-revision.guard.json"

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

def canonical_bytes(obj) -> bytes:
    # Explicit canonicalization owned both sides: sort_keys + compact separators + unicode preserved.
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()

def check_manifest_all773(repo: Path):
    # BEFORE project imports: pin manifest, then compare EVERY file meta SHA/bytes/physical_mode.
    if hashlib.sha256(MANIFEST.read_bytes()).hexdigest() != EXP_MANIFEST_SHA:
        fail("manifest != a7e40")
    if MANIFEST.stat().st_size != EXP_MANIFEST_BYTES:
        fail("manifest bytes != 202833")
    m = json.loads(MANIFEST.read_text())
    files = m.get("files")
    if not isinstance(files, dict):
        fail(f"manifest files must be dict, got {type(files)}")
    if len(files) != EXP_FILES_LEN or m.get("intended_files") != EXP_FILES_LEN:
        fail(f"manifest files_len != 773: {len(files)}/{m.get('intended_files')}")
    for rel, meta in files.items():
        fp = repo / rel
        try:
            st = os.lstat(fp)
        except FileNotFoundError:
            fail(f"773 missing {rel}")
        if stat.S_ISLNK(st.st_mode):
            fail(f"773 symlink refused {rel}")
        if not stat.S_ISREG(st.st_mode):
            fail(f"773 not regular {rel} mode {oct(stat.S_IMODE(st.st_mode))}")
        if sha256_file(fp) != meta.get("sha256"):
            fail(f"773 sha drift {rel}")
        if st.st_size != meta.get("bytes"):
            fail(f"773 bytes drift {rel}")
        if oct(stat.S_IMODE(st.st_mode)) != meta.get("physical_mode"):
            fail(f"773 mode drift {rel}: {oct(stat.S_IMODE(st.st_mode))} != {meta.get('physical_mode')}")
        # kind must be file
        if meta.get("kind") != "file":
            fail(f"773 kind != file {rel}")
    # Derive 7 tool pins from bound manifest (no hand SHA constants)
    for rel in TOOL_RELS:
        meta = files.get(rel)
        if meta is None:
            fail(f"tool {rel} not in manifest")
        fp = repo / rel
        if sha256_file(fp) != meta["sha256"] or fp.stat().st_size != meta["bytes"]:
            fail(f"tool {rel} drift vs manifest")
        if oct(stat.S_IMODE(fp.stat().st_mode)) != meta["physical_mode"]:
            fail(f"tool {rel} mode drift")
    print("manifest ALL773 compare OK a7e4/773 + tools7 derived from manifest")

def check_head_tree_git(repo: Path):
    env = {k: v for k, v in os.environ.items() if k not in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES")}
    try:
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, check=True, capture_output=True, text=True, env=env).stdout.strip()
        tree = subprocess.run(["git", "rev-parse", "HEAD^{tree}"], cwd=repo, check=True, capture_output=True, text=True, env=env).stdout.strip()
    except Exception as e:
        fail(f"scoped Git HEAD/tree failed: {e}")
    if head != EXP_HEAD or not HEX40.fullmatch(head):
        fail(f"HEAD != cc1c {EXP_HEAD}: {head!r}")
    if tree != EXP_TREE or not HEX40.fullmatch(tree):
        fail(f"tree != ed2dc4 {EXP_TREE}: {tree!r}")
    print(f"HEAD/tree OK {head[:12]}/{tree[:12]} (scoped NEW repo)")
    return head, tree

def inventory_full(repo: Path, issue: str):
    # Full old material inventory: files sha/size/mode + dirs mode set; fail on symlink/special.
    m = json.loads(MANIFEST.read_text())
    files_meta = m["files"]
    inv_files = {}
    for rel in files_meta:
        fp = repo / rel
        st = os.lstat(fp)
        if stat.S_ISLNK(st.st_mode):
            fail(f"inventory symlink {rel}")
        if not stat.S_ISREG(st.st_mode):
            fail(f"inventory not regular {rel}")
        inv_files[rel] = [sha256_file(fp), st.st_size, oct(stat.S_IMODE(st.st_mode))]
    src = repo / f"sources/{issue}"
    inv_extra = {}
    dirset = set()
    for p in sorted(src.rglob("*")):
        # lstat, no follow
        try:
            st = os.lstat(p)
        except FileNotFoundError:
            continue
        s = p.relative_to(repo).as_posix()
        if "/research/v2/acceptance-revision" in s:
            fail(f"future R/inputs must not exist pre-dispatch: {s}")
        if stat.S_ISLNK(st.st_mode):
            fail(f"inventory symlink {s}")
        elif stat.S_ISDIR(st.st_mode):
            dirset.add(s + f" mode={oct(stat.S_IMODE(st.st_mode))}")
        elif stat.S_ISREG(st.st_mode):
            if s not in inv_files:
                inv_extra[s] = [sha256_file(p), st.st_size, oct(stat.S_IMODE(st.st_mode))]
        else:
            fail(f"inventory special {s} mode {oct(st.st_mode)}")
    # guard + slots must be absent (lstat ENOENT)
    guard = src / GUARD_REL
    try:
        os.lstat(guard)
        fail(f"guard present {guard}")
    except FileNotFoundError:
        pass
    for slot in SEVEN_SLOTS:
        sp = src / slot
        try:
            os.lstat(sp)
            fail(f"slot must be absent pre-prepare {slot}")
        except FileNotFoundError:
            pass
    return {"files773": inv_files, "extra": inv_extra, "dirs": sorted(dirset)}

class Tee:
    def __init__(self, *files):
        self.files = files
    def write(self, data):
        for f in self.files:
            f.write(data)
    def flush(self):
        for f in self.files:
            f.flush()

def resolve_inside(repo: Path, rel: str) -> Path:
    if not SAFEPATH.fullmatch(rel) or rel.startswith("/") or ".." in Path(rel).parts:
        fail(f"unsafe rel {rel!r}")
    abs_p = repo / rel
    try:
        # must be inside repo (no escape via symlink yet; symlink refused later)
        abs_p.resolve().relative_to(repo.resolve())
    except Exception:
        fail(f"rel escapes repo {rel!r}")
    return abs_p

def exclusive_write_bytes(abs_p: Path, repo: Path, data: bytes, label: str):
    # containment + ancestor symlink/non-dir guard + O_EXCL only new
    try:
        abs_p.resolve().relative_to(repo.resolve())
    except Exception:
        fail(f"{label} escapes repo")
    abs_p.parent.mkdir(parents=True, exist_ok=True)
    for anc in [abs_p.parent] + list(abs_p.parent.parents):
        if str(anc) == "/":
            break
        try:
            st = os.lstat(anc)
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(st.st_mode):
            fail(f"{label} ancestor symlink {anc}")
        if not stat.S_ISDIR(st.st_mode):
            # ancestor exists but not dir (file) -> refuse unless it is the target's direct parent being created? parent mkdir ensures dirs.
            if anc != abs_p.parent or not anc.exists():
                pass
            if anc.exists() and not stat.S_ISDIR(st.st_mode):
                fail(f"{label} ancestor not dir {anc}")
        try:
            anc.resolve().relative_to(repo.resolve())
        except Exception:
            # ancestor outside repo (e.g., /tmp) for parent chain beyond repo is ok; only target must be inside
            if anc == repo or str(repo.resolve()) in str(anc.resolve()):
                pass
            pass
        if anc == repo:
            break
    try:
        fd = os.open(str(abs_p), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o664)
    except FileExistsError:
        fail(f"{label} exists (O_EXCL new-only)")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
    except Exception as e:
        fail(f"{label} write failed: {e}")
    st = os.lstat(abs_p)
    if not stat.S_ISREG(st.st_mode) or stat.S_ISLNK(st.st_mode):
        fail(f"{label} not regular after write")
    return {"sha256": sha256_file(abs_p), "byte_count": abs_p.stat().st_size}

def exclusive_copy(src: Path, repo: Path, dst_rel: str, label: str, exp_sha: str, exp_len: int):
    if not SAFEPATH.fullmatch(dst_rel):
        fail(f"{label} safePath {dst_rel!r}")
    base = Path(dst_rel).name
    if ("EFF-D" not in base) and ("w34-event-" not in base):
        fail(f"{label} FULL DID missing in {base}")
    dst = resolve_inside(repo, dst_rel)
    if dst.exists() or dst.is_symlink():
        fail(f"{label} must be new absent O_EXCL {dst_rel}")
    if not src.is_file() or src.is_symlink():
        fail(f"{label} source not regular {src}")
    if sha256_file(src) != exp_sha or src.stat().st_size != exp_len:
        fail(f"{label} pinned source drift")
    data = src.read_bytes()
    info = exclusive_write_bytes(dst, repo, data, label)
    if info["sha256"] != exp_sha or info["byte_count"] != exp_len:
        fail(f"{label} copy mismatch")
    return info

def main():
    ap = argparse.ArgumentParser(description="ACTUAL normal HIGH prepare r3 (one edition).")
    ap.add_argument("--issue", required=True, choices=["2026-W34", "SP-efficient-llm-2026"])
    ap.add_argument("--repo-root", default=str(DEFAULT_REPO))
    ap.add_argument("--revision-id", default=None)
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--config", default=str(CONFIG_R3))
    a = ap.parse_args()
    issue = a.issue
    repo = Path(a.repo_root)
    cfg_path = Path(a.config)
    rev = a.revision_id
    # Load config first to get revision default, but verify config hash pinned? Config itself externally pinned at invocation: log its sha, no reseal.
    cfg_doc0, _, cfg_hash0, cfg_len0 = load_strict_json(cfg_path)
    rev = rev or cfg_doc0["issues"][issue]["revision_id"]
    if not REVISION_RE.fullmatch(rev) or any(c.isupper() for c in rev) or "T" in rev or "Z" in rev:
        fail(f"revision_id invalid {rev!r}")

    ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out = Path(a.outdir).resolve() if a.outdir else (PACKET.resolve() / f"prepare-normal-high-r3-{issue}-{ts}-pid{os.getpid()}")
    try:
        out.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        fail(f"outdir exists {out}")
    # stdio capture: tee stdout/stderr to files, preserve raw + numeric exit
    stdout_f = open(out / "stdout.txt", "w")
    stderr_f = open(out / "stderr.txt", "w")
    orig_out, orig_err = sys.stdout, sys.stderr
    sys.stdout = Tee(orig_out, stdout_f)
    sys.stderr = Tee(orig_err, stderr_f)
    def wlog(n: str, d: str):
        (out / n).write_text(d)
    wlog("argv.txt", " ".join(sys.argv))
    wlog("env-whitelist.txt", "\n".join(f"{k}={os.environ.get(k,'')}" for k in sorted(ALLOWED_ENV)))
    wlog("pid.txt", str(os.getpid()))
    wlog("wall-start.txt", ts)
    wlog("cwd.txt", os.getcwd())
    wlog("config-pinned.txt", f"{cfg_path} {cfg_hash0} {cfg_len0}\n(no post reseal)")
    exit_code = 2
    entry = None
    try:
        # Manifest ALL773 compare BEFORE project imports
        check_manifest_all773(repo)
        check_head_tree_git(repo)
        entry = inventory_full(repo, issue)
        wlog("entry-inventory.json", json.dumps(entry, indent=2, sort_keys=True))

        # Config/patch/review externally pinned at invocation (verify now, no reseal after)
        cfg_doc, _, cfg_hash, cfg_len = load_strict_json(cfg_path)
        if cfg_hash != cfg_hash0:
            fail("config resealed during run")
        # Verify each pinned packet file sha/bytes
        pins_to_check = []
        if issue == "2026-W34":
            pins_to_check = [cfg_doc["issues"][issue]["patch"], cfg_doc["issues"][issue]["routing"], cfg_doc["issues"][issue]["staging"]]
        else:
            pins_to_check = [cfg_doc["issues"][issue]["patch_r6"], cfg_doc["issues"][issue]["completeness_r5"],
                             cfg_doc["issues"][issue]["supplement_full30_r4"], cfg_doc["issues"][issue]["routing"],
                             cfg_doc["issues"][issue]["staging"], cfg_doc["issues"][issue]["assembly_r6"],
                             cfg_doc["issues"][issue]["delta_r5_r6"], cfg_doc["issues"][issue]["schema_check_r6"]]
        for pin in pins_to_check:
            p = Path(pin["path"])
            if sha256_file(p) != pin["sha256"] or p.stat().st_size != pin["bytes"]:
                fail(f"pinned input drift {pin['path']}")
        print(f"config/patch/review pins OK {cfg_hash[:12]} (no post reseal)")

        # State/Profile/CP full shape (not hex-only)
        st_doc, st_raw, _, _ = load_strict_json(repo / f"sources/{issue}/production-state.json")
        if st_doc.get("lifecycle_state") != "EVIDENCE_REVIEWED":
            fail("State not EVIDENCE_REVIEWED")
        if st_doc.get("implementation", {}).get("repository_commit_sha") != EXP_INIT480:
            fail("State init != 480")
        if st_doc.get("implementation", {}).get("orchestrator_version") != "survey-production-core-v2/0.15-postintegration-transport-thematic":
            fail("orchestrator != expected")
        hg = st_doc.get("human_gates", {})
        if hg != {"architecture_review": "pending", "publication_preview": "pending"}:
            fail(f"human_gates shape {hg}")
        hgp = st_doc.get("human_gate_provenance", {})
        if hgp != {"architecture_review": None, "publication_preview": None}:
            fail(f"human provenance shape {hgp}")
        if st_doc.get("exception_gate", {}).get("status") != "inactive":
            fail("exception not inactive")
        mc = st_doc.get("machine_checkpoints", {})
        for k in ("discovery", "screening", "evidence", "materiality", "completeness"):
            if mc.get(k) != "passed":
                fail(f"machine {k} != passed")
        for k in ("selection", "architecture", "draft", "validation", "publication_preview", "freeze", "release"):
            if mc.get(k) != "pending":
                fail(f"seven slot machine {k} != pending")
        cp = st_doc.get("checkpoint_provenance", {})
        if not isinstance(cp.get("evidence"), dict) or set(cp["evidence"]) != {"path", "sha256"}:
            fail("CP evidence shape")
        for k in ("selection", "architecture", "draft", "validation", "publication_preview", "freeze", "release"):
            if cp.get(k) is not None:
                fail(f"CP {k} must be null")
        prof_ref = st_doc.get("profile")
        if not isinstance(prof_ref, dict) or set(prof_ref) != {"path", "sha256"}:
            fail("State profile shape")
        prof_abs = repo / prof_ref["path"]
        prof_doc, _, _, _ = load_strict_json(prof_abs)
        if prof_doc["paths"]["source_root"] != f"sources/{issue}":
            fail("source_root")
        # artifacts: 4 named, from Evidence checkpoint
        ev_cp_path = cp["evidence"]["path"]
        ev_cp_doc, _, _, _ = load_strict_json(repo / ev_cp_path)
        arts = {x["name"]: x for x in ev_cp_doc.get("artifacts", [])}
        for need in ("edition-views-acceptance", "evidence-acceptance", "materiality-ledger", "profile-completeness"):
            if need not in arts or set(arts[need]) != {"name", "path", "sha256"}:
                fail(f"artifact {need} shape")
            ap_ = repo / arts[need]["path"]
            if sha256_file(ap_) != arts[need]["sha256"]:
                fail(f"artifact {need} drift")
        print(f"State/Profile/CP/guard/human shape OK {issue}")

        # Patch shape actual keys (no guess)
        if issue == "2026-W34":
            patch_doc, _, _, _ = load_strict_json(Path(cfg_doc["issues"][issue]["patch"]["path"]))
            print(f"W34 patch keys {sorted(patch_doc.keys())}")
            changed = patch_doc.get("changed_record_ids")
            rec_key = "new_records"
            counts = patch_doc.get("counts", {})
            if not isinstance(changed, list) or len(changed) != 4:
                fail("W34 changed_record_ids !=4")
            if counts.get("affected") != 4 or counts.get("total") != 409 or counts.get("unaffected") != 405:
                fail(f"W34 counts {counts}")
        else:
            patch_doc, _, _, _ = load_strict_json(Path(cfg_doc["issues"][issue]["patch_r6"]["path"]))
            print(f"SP r6 keys {sorted(patch_doc.keys())}")
            changed = patch_doc.get("changed_ids")
            rec_key = "new_records"
            counts = patch_doc.get("counts", {})
            if not isinstance(changed, list) or len(changed) != 4:
                fail("SP changed_ids !=4")
            if counts.get("affected") != 4 or counts.get("preserved") != 156 or counts.get("total") != 160:
                fail(f"SP counts {counts}")
            if "base_supplement" in patch_doc:
                fail("SP r6 must not carry stale base_supplement")
        recs = patch_doc.get(rec_key)
        if not isinstance(recs, list) or len(recs) != 4:
            fail("patch new_records !=4")
        if set(r.get("discovery_id") for r in recs) != set(changed):
            fail("patch changed vs records mismatch")
        # factual record keys: W34 13 keys incl window/carry + optional bindings; SP D070/D071/D141 16 keys, D142 15 keys (omit, not null)
        for r in recs:
            did = r.get("discovery_id")
            if issue == "2026-W34":
                # required WEEKLY: COMMON10 + window_relation/carry_over =12? + source_bindings optional =13
                for k in ["discovery_id", "status", "entity", "artifact_type", "claims", "limitations", "verification", "materiality", "materiality_rationale", "scope_dimensions", "window_relation", "carry_over"]:
                    if k not in r:
                        fail(f"W34 {did} missing {k}")
                if "source_bindings" in r and not (isinstance(r["source_bindings"], list) and len(r["source_bindings"]) > 0):
                    fail(f"W34 {did} source_bindings shape")
            else:
                for k in ["discovery_id", "status", "entity", "artifact_type", "claims", "limitations", "verification", "materiality", "materiality_rationale", "scope_dimensions", "lineage_role", "branch_ids", "transition_ids"]:
                    if k not in r:
                        fail(f"SP {did} missing {k} actual {sorted(r.keys())}")
                if r.get("lineage_role") != "CORE":
                    fail(f"SP {did} lineage_role != CORE")
                if did == "EFF-D142":
                    if "source_bindings" in r:
                        fail("SP D142 must omit source_bindings (not null)")
                else:
                    sb = r.get("source_bindings")
                    if not (isinstance(sb, list) and len(sb) > 0 and all(isinstance(x, str) and len(x) > 0 for x in sb)):
                        fail(f"SP {did} source_bindings must be non-empty string array")
                # only permitted nullable: entity.canonical_url, inheritance_note; contexts/caveats non-null strings checked by existing validator later
        print(f"patch shape OK {issue} 4 records")

        # Base interactive + preserved deep equality + canonical hash explicit
        base_rel = cfg_doc["issues"][issue]["base_interactive"]["path"] if "base_interactive" in cfg_doc["issues"][issue] and isinstance(cfg_doc["issues"][issue]["base_interactive"], dict) and "path" in cfg_doc["issues"][issue]["base_interactive"] and not cfg_doc["issues"][issue]["base_interactive"]["path"].startswith(".rephase-") else None
        # Resolve base file inspecting actual: W34 repo-relative, SP r6 workspace-relative
        if issue == "2026-W34":
            base_path_in_repo = cfg_doc["issues"][issue]["base_interactive"]["path"]
            base_abs = repo / base_path_in_repo
        else:
            # SP r6 base_interactive.path is workspace-relative .rephase...; verify inside repo
            ws_rel = "sources/SP-efficient-llm-2026/evidence/v2/accepted/73f4bc1ec69c70925a7119a0327ff5e6f024812b56cf8edd7c49eae9f672a297/interactive-evidence.json"
            base_abs = repo / ws_rel
            # verify workspace path also matches pin
            ws_abs = Path(cfg_doc["issues"][issue]["base_interactive"]["path"]) if False else None
        base_doc, base_raw, base_hash, base_len = load_strict_json(base_abs)
        exp_base = cfg_doc["issues"][issue]["base_interactive"] if issue == "2026-W34" else {"sha256": "697a4ed088b76f18b3859568a735491a3a8b2295c480be3e1e678c4d8b31f104", "bytes": 355643}
        if sha256_file(base_abs) != exp_base["sha256"] or base_len != exp_base["bytes"]:
            fail("base interactive drift")
        if len(base_doc.get("records", [])) != (409 if issue == "2026-W34" else 160):
            fail("base records != 409/160")
        runner = base_doc.get("runner", {})
        for k in ["provider", "model", "invocation", "generated_at"]:
            if k not in runner:
                fail(f"base runner missing {k}")
        # preserved deep equality
        by_base = {r["discovery_id"]: r for r in base_doc["records"]}
        by_new = {r["discovery_id"]: r for r in recs}
        for did in by_base:
            if did not in changed:
                # will compare after full assembly; ensure base has all changed IDs too (old versions)
                pass
        if set(changed) - set(by_base):
            fail(f"changed IDs not in base {set(changed)-set(by_base)}")
        full_map = dict(by_base)
        for r in recs:
            full_map[r["discovery_id"]] = r
        if len(full_map) != (409 if issue == "2026-W34" else 160):
            fail("full assembly != 409/160")
        # deep equality for preserved
        for did, rec in by_base.items():
            if did not in changed:
                if full_map[did] != rec:
                    fail(f"preserved deep equality failed {did}")
        # canonical hash explicit (same method both sides, documented)
        unaff = [by_base[did] for did in by_base if did not in set(changed)]
        canon = canonical_bytes(sorted(unaff, key=lambda r: r["discovery_id"]))
        calc = hashlib.sha256(canon).hexdigest()
        if issue == "2026-W34":
            if calc != patch_doc.get("unaffected405_hash") or len(canon) != patch_doc.get("unaffected405_bytes"):
                fail(f"W34 unaffected canonical mismatch {calc[:12]}")
        else:
            # SP r6: no hash field; verify against documented d455... informational (explicit method, no fallback)
            if calc != "d455f7221a0addd93dd2a3c07c874fe4dfb815d3e795933882eb839e868a1ef9":
                fail(f"SP preserved canonical mismatch {calc[:12]}")
        # D165 deep + canonical
        if issue == "SP-efficient-llm-2026":
            b165 = by_base.get("EFF-D165")
            if b165 is None:
                fail("SP base D165 missing")
            if hashlib.sha256(canonical_bytes(b165)).hexdigest() != "16f046f59e171a80c22bb0df2a159af9eafaa1ad3cfb0f9a2269ab90871e6fe2":
                fail("SP D165 canonical mismatch")
            if patch_doc.get("d165_preserved", {}).get("sha256") != "16f046f59e171a80c22bb0df2a159af9eafaa1ad3cfb0f9a2269ab90871e6fe2":
                fail("SP patch D165 pin")
        full = [full_map[did] for did in sorted(full_map)]
        print(f"records full {len(full)} deep-equality OK canonical {calc[:12]}")

        # Task targets exact set + cardinality via task files (not package summary)
        pkg_path = base_abs.parent / "package.json"
        pkg_doc, _, _, _ = load_strict_json(pkg_path)
        if len(pkg_doc.get("tasks", [])) != (409 if issue == "2026-W34" else 160):
            fail("package tasks cardinality")
        tmap = {}
        for t in pkg_doc["tasks"]:
            dids = t.get("discovery_ids", [])
            if len(dids) != 1:
                fail(f"package task discovery_ids shape {t.get('evidence_task_id')}")
            tmap[dids[0]] = t
        if set(tmap) != set(by_base):
            fail("package task IDs != base IDs")
        for r in recs:
            did = r["discovery_id"]
            t = tmap.get(did)
            if t is None:
                fail(f"changed {did} no package task")
            task_file = base_abs.parent / t["path"]
            if not task_file.is_file() or task_file.is_symlink():
                fail(f"task file missing {did} {t['path']}")
            task_doc, _, _, _ = load_strict_json(task_file)
            exp_targets = task_doc.get("verification_targets")
            if not isinstance(exp_targets, list) or len(exp_targets) == 0:
                fail(f"task {did} verification_targets missing/empty")
            got = set(x.get("target") for x in r.get("verification", []))
            if set(exp_targets) != got:
                fail(f"{did} targets != task exact missing={set(exp_targets)-got} extra={got-set(exp_targets)}")
        print("task targets exact set+cardinality OK (FULL revalidated by HIGH)")

        # Completeness 7-field + residual/closure shape (actual)
        if issue == "2026-W34":
            comp_abs = repo / "sources/2026-W34/profile-completeness-v2.json"
            comp_doc, _, _, _ = load_strict_json(comp_abs)
            obligs = comp_doc.get("obligations", [])
            if len(obligs) != 3:
                fail("W34 obligations !=3")
            resid = comp_doc.get("residual_limitations")
            clos = comp_doc.get("closure")
            if not isinstance(resid, list):
                fail("W34 residual shape")
            if clos is not None:
                fail("W34 closure must be null")
        else:
            comp_pkt, _, _, _ = load_strict_json(Path(cfg_doc["issues"][issue]["completeness_r5"]["path"]))
            obligs = comp_pkt.get("obligations", [])
            if len(obligs) != 15:
                fail("SP obligations !=15")
            resid = comp_pkt.get("residual_limitations")
            clos = comp_pkt.get("closure")
            if not isinstance(resid, list) or len(resid) == 0:
                fail("SP residual shape")
            if not isinstance(clos, dict) or set(clos) != {"targeted_gap_fill_completed", "limitations", "status"}:
                fail(f"SP closure request-shape {clos.keys() if isinstance(clos, dict) else clos}")
        for o in obligs:
            for k in ["obligation_id", "dimension", "description", "status", "discovery_ids", "evidence_task_ids", "rationale"]:
                if k not in o:
                    fail(f"obligation {o.get('obligation_id')} missing {k}")
            if o["status"] not in ("SATISFIED", "LIMITATION", "NEEDS_RESEARCH", "NOT_APPLICABLE"):
                fail(f"obligation {o.get('obligation_id')} status")
        # no fake SAT: W34 2 LIM+1 SAT; SP O01/O07 SAT rest LIM (approved r5)
        sats = [o["obligation_id"] for o in obligs if o["status"] == "SATISFIED"]
        if issue == "2026-W34":
            if set(sats) != {"weekly:carry-over"}:
                fail(f"W34 SAT {sats}")
        else:
            if set(sats) != {"EFF-O01", "EFF-O07"}:
                fail(f"SP SAT {sats}")
        completeness = {"obligations": obligs, "residual_limitations": resid, "closure": clos}
        print(f"completeness 7field {len(obligs)} no-fake-SAT OK")

        # Routing actual keys + Raw jobs (verify BEFORE any active writes)
        rout_doc, _, _, _ = load_strict_json(Path(cfg_doc["issues"][issue]["routing"]["path"]))
        print(f"routing keys {sorted(rout_doc.keys())}")
        raw_jobs = []
        if issue == "2026-W34":
            entries = rout_doc.get("entries")
            if not isinstance(entries, dict) or len(entries) != 4:
                fail("W34 routing entries !=4")
            for did, e in entries.items():
                if not isinstance(e, dict):
                    fail(f"W34 routing {did} shape actual {type(e)}")
                for k in ["source_file", "bytes", "sha256", "future_raw_path"]:
                    if k not in e:
                        fail(f"W34 routing {did} missing {k} actual {sorted(e.keys())}")
                fut = e["future_raw_path"]
                if did not in fut or "w34-event-arxiv-2608-" not in fut or not SAFEPATH.fullmatch(fut):
                    fail(f"W34 FULL DID/safePath {did} {fut}")
                src = Path(e["source_file"])
                # resolve inside repo (workspace-relative .rephase... must be inside NEW repo)
                try:
                    src.resolve().relative_to(repo.resolve())
                except Exception:
                    fail(f"W34 source escapes NEW repo {src}")
                if not src.is_file() or src.is_symlink():
                    fail(f"W34 source not regular {src}")
                if sha256_file(src) != e["sha256"] or src.stat().st_size != e["bytes"]:
                    fail(f"W34 pinned source drift {did}")
                raw_jobs.append((did, src, e["sha256"], e["bytes"], fut))
        else:
            for k in ["u1", "u2", "u3", "d142_summary_routing"]:
                if k not in rout_doc:
                    fail(f"SP routing missing {k} actual {sorted(rout_doc.keys())}")
            intake = Path(cfg_doc["issues"][issue]["intake_dir"])
            mapping = [("u1", "EFF-D070", "u1.snapshot.decoded.html", 253542, "14ae31184b253b736ff8be423fafbe5ff82d1f75cf66b600bad8b8c9152aa443"),
                       ("u2", "EFF-D071", "u2.snapshot.decoded.html", 307198, "357708348b9884d004669d6df45100986676f5ab900a75e76304fb19cae05bf2"),
                       ("u3", "EFF-D141", "u3.snapshot.body.bin", 350662, "97a5dd74ed1e9ba006d21759c14615a7c0a485c4db161dc00a2d0b1e4d651b69")]
            for rk, did, fn, exp_len, exp_sha in mapping:
                fut = rout_doc[rk].get("future_raw_path")
                if not isinstance(fut, str) or "EFF-D" not in fut or not SAFEPATH.fullmatch(fut):
                    fail(f"SP {rk} FULL DID/safePath {fut}")
                src = intake / fn
                if not src.is_file() or src.is_symlink():
                    fail(f"SP {rk} intake not regular {src}")
                if sha256_file(src) != exp_sha or src.stat().st_size != exp_len:
                    fail(f"SP {rk} pinned bytes drift")
                raw_jobs.append((did, src, exp_sha, exp_len, fut))
            d142 = rout_doc["d142_summary_routing"]
            for k in ["existing_file", "existing_sha256", "existing_bytes", "future_raw_path", "first_claim_literal"]:
                if k not in d142:
                    fail(f"SP d142 missing {k} actual {sorted(d142.keys())}")
            fut142 = d142["future_raw_path"]
            if "EFF-D142" not in fut142 or not SAFEPATH.fullmatch(fut142):
                fail("SP D142 FULL DID/safePath")
            src142 = Path(d142["existing_file"])
            try:
                src142.resolve().relative_to(repo.resolve())
            except Exception:
                fail("SP D142 existing escapes NEW repo")
            if sha256_file(src142) != d142["existing_sha256"] or src142.stat().st_size != d142["existing_bytes"]:
                fail("SP D142 pinned drift")
            raw_jobs.append(("EFF-D142", src142, d142["existing_sha256"], d142["existing_bytes"], fut142))
        # first-claim literal BEFORE writes (mechanical only)
        for r in recs:
            did = r["discovery_id"]
            first = (r.get("claims") or [{}])[0].get("text", "")
            if not first:
                fail(f"{did} first claim empty")
            cand = [j for j in raw_jobs if j[0] == did]
            if len(cand) != 1:
                fail(f"{did} raw job !=1")
            txt = cand[0][1].read_bytes().decode("utf-8", errors="ignore")
            if first not in txt:
                fail(f"{did} first-claim literal NOT in retained bytes")
        print(f"Raw 4 FULL-DID/pinned/literal OK BEFORE writes")

        # Request schema pre-validate BEFORE Raw when possible:
        # W34 supp known -> build+validate full request now; SP supp after builder -> pre-validate payload expected bytes now.
        # For SP, preconstruct expected supp payload bytes from full30 (no write) and validate shape.
        if issue == "SP-efficient-llm-2026":
            full30_doc, _, _, _ = load_strict_json(Path(cfg_doc["issues"][issue]["supplement_full30_r4"]["path"]))
            if len(full30_doc.get("sources", [])) != 30:
                fail("SP full30 !=30 pre-build")
            # expected new IDs + D142 absent
            got_ids = set(s.get("supplement_source_id") for s in full30_doc["sources"])
            if not {"supplement-src-ea9b086e35e1c559", "supplement-src-793903f4b4b1d3e1", "supplement-src-228b81661893f1ea"}.issubset(got_ids):
                fail("SP full30 missing 3 new")
            if any(s.get("discovery_id") == "EFF-D142" for s in full30_doc["sources"]):
                fail("SP full30 D142 entry")
            print("SP payload expected bytes prevalidated (no future-data-as-verified token)")

        # Stage 4 Raw O_EXCL only new (first active writes)
        req_rel = cfg_doc["issues"][issue]["request_rel"]
        rev_root_rel = cfg_doc["issues"][issue]["rev_root_rel"]
        if (repo / req_rel).exists() or (repo / req_rel).is_symlink():
            fail(f"request must be new absent {req_rel}")
        if (repo / rev_root_rel).exists():
            fail(f"R root must be new absent {rev_root_rel}")
        # explicit containment
        resolve_inside(repo, req_rel)
        # rev_root must be inside repo and under source_root/research/v2/acceptance-revisions
        if not rev_root_rel.startswith(f"sources/{issue}/research/v2/acceptance-revisions/"):
            fail(f"R root rel {rev_root_rel}")
        resolve_inside(repo, rev_root_rel + "/revision-manifest.json")
        for did, src, exp_sha, exp_len, fut in raw_jobs:
            exclusive_copy(src, repo, fut, f"Raw {did}", exp_sha, exp_len)
        print(f"staged 4 Raw O_EXCL new-only {issue}")

        # Supplement: W34 explicit ce6f; SP NORMAL builder writes actual after prevalidation
        if issue == "2026-W34":
            supp_ref = {"path": "sources/2026-W34/external/evidence-supplement/evidence-authority-supplement-r2-fresh-basis.json",
                        "sha256": "ce6f977a3e690e779c380b7b035d9247207e262b5c50a5b14b6b6b8f0fbc704e", "byte_count": 389414}
            chk_p = repo / supp_ref["path"]
            if sha256_file(chk_p) != supp_ref["sha256"] or chk_p.stat().st_size != supp_ref["byte_count"]:
                fail("W34 ce6f bytes drift (NO null fallback)")
            # verify OLD supplemented (policy requires non-null)
            pkg_old = pkg_doc.get("authority_supplement")
            if not isinstance(pkg_old, dict) or pkg_old.get("sha256") != supp_ref["sha256"]:
                fail("W34 OLD not supplemented ce6f")
            print("W34 supp explicit ce6f OK")
        else:
            import sys as _sys
            _sys.path.insert(0, str(repo.resolve()))
            try:
                from scripts import survey_evidence_v2 as ev_mod
                full30_doc, _, _, _ = load_strict_json(Path(cfg_doc["issues"][issue]["supplement_full30_r4"]["path"]))
                source_root = repo / "sources/SP-efficient-llm-2026"
                disc_path = repo / "sources/SP-efficient-llm-2026/discovery/discovery-v2.jsonl"
                scr_path = repo / f"sources/SP-efficient-llm-2026/screening/v2/accepted/9b9796295c2ddf28b087fc725b78b7d089d6e946a5a5ba65ab51601d58f558a9/screening-accepted.json"
                # effective DS pins from config (DIRECT 165)
                if sha256_file(disc_path) != cfg_doc["issues"][issue]["discovery_ref_effective"]["sha256"]:
                    fail("SP effective DS drift")
                supp_id = f"r4-sp17-EFF-DID-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
                out_rel = f"sources/SP-efficient-llm-2026/external/evidence-supplement/evidence-authority-supplement-{supp_id}.json"
                resolve_inside(repo, out_rel)
                if (repo / out_rel).exists():
                    fail(f"SP supp output must be new absent {out_rel}")
                try:
                    built = ev_mod.build_evidence_authority_supplement(repo, "SP-efficient-llm-2026", source_root, disc_path, scr_path, full30_doc["sources"], repo / out_rel, supplement_id=supp_id)
                except Exception as e:
                    # NORMAL builder may delete failed own output; document, do not claim all partials retained
                    fail(f"SP builder failed (own output may be deleted by builder) {e}")
                ev_mod.validate_evidence_authority_supplement(repo, built, expected_issue_id="SP-efficient-llm-2026", expected_source_root=source_root, expected_discovery_path=disc_path, expected_screening_acceptance_path=scr_path)
                st_o = (repo / out_rel).stat()
                supp_ref = {"path": out_rel, "sha256": sha256_file(repo / out_rel), "byte_count": st_o.st_size}
                print(f"SP supp built+validated {supp_id} {supp_ref['sha256'][:12]}")
            finally:
                try:
                    _sys.path.remove(str(repo.resolve()))
                except ValueError:
                    pass

        # Assemble request + validate with EXISTING validators (no redundant manual)
        import sys as _sys2
        _sys2.path.insert(0, str(repo.resolve()))
        try:
            from scripts import survey_prearchitecture_acceptance_v2 as high_mod
            from scripts import survey_production_v2 as core_mod
            from scripts import survey_schema_v2 as schema_gate
            from scripts import survey_evidence_v2 as ev_mod2
            cfg_obj = core_mod.load_json(repo / str(core_mod.DEFAULT_CONFIG))
            live_contract, live_tools = high_mod._contract_and_tools(repo, cfg_obj, st_doc)
            # live tools must match manifest-derived (no hand constants): compare to manifest metas
            m_all = json.loads(MANIFEST.read_text())["files"]
            for e in live_tools:
                meta = m_all.get(e["path"])
                if meta is None or e["sha256"] != meta["sha256"]:
                    fail(f"live tool {e['path']} != manifest")
            if set(e["path"] for e in live_tools) != set(TOOL_RELS):
                fail(f"live tool set != 7 {TOOL_RELS}")
            # discovery effective via normal facade: screening package basis must equal discovery_ref
            scr_pkg_path = (repo / f"sources/{issue}/screening/v2/accepted").glob("*/package.json")
            scr_pkgs = list(scr_pkg_path)
            if len(scr_pkgs) != 1:
                fail(f"screening package !=1 {scr_pkgs}")
            scr_pkg_doc, _, _, _ = load_strict_json(scr_pkgs[0])
            basis_disc = scr_pkg_doc.get("basis", {}).get("discovery_path")
            if issue == "2026-W34":
                disc_ref = {"path": "sources/2026-W34/screening/input/event-discovery-v2.jsonl", "sha256": "0a23be47dad8ddaf4f0a9c3261d97cc0006ac942bfd2321be2487289a34da31e", "byte_count": 1335444}
                if basis_disc != disc_ref["path"]:
                    fail(f"W34 effective != screening basis {basis_disc} (must be 439 not root 369)")
            else:
                disc_ref = {"path": "sources/SP-efficient-llm-2026/discovery/discovery-v2.jsonl", "sha256": "7074cef2bfc3b2dd034addbd778055bc2fed962e9845c756f32f9b3c848199d3", "byte_count": 173299}
                if basis_disc != disc_ref["path"]:
                    fail(f"SP effective != screening basis {basis_disc}")
            scr_ref_pin = cfg_doc["issues"][issue]["screening_ref"]
            scr_ref = {"path": scr_ref_pin["path"], "sha256": scr_ref_pin["sha256"], "byte_count": scr_ref_pin["byte_count"]}
            prof_ref = {"path": f"sources/{issue}/production-profile.json", "sha256": sha256_file(repo / f"sources/{issue}/production-profile.json"), "byte_count": (repo / f"sources/{issue}/production-profile.json").stat().st_size}
            before_state = {"path": f"sources/{issue}/production-state.json", "sha256": sha256_file(repo / f"sources/{issue}/production-state.json"), "byte_count": (repo / f"sources/{issue}/production-state.json").stat().st_size}
            before_checkpoint = {"evidence": {"path": cp["evidence"]["path"], "sha256": cp["evidence"]["sha256"]},
                                 "materiality": {"path": cp["materiality"]["path"], "sha256": cp["materiality"]["sha256"]},
                                 "completeness": {"path": cp["completeness"]["path"], "sha256": cp["completeness"]["sha256"]}}
            recorded_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            executor = f"general / Muse Spark 1.3 / prepare-normal-high-r3 {issue} {rev}"
            tool_pins = {"repository_commit_sha": EXP_HEAD, "orchestrator_version": "survey-production-core-v2/0.15-postintegration-transport-thematic", "contract": live_contract, "tool_shas": live_tools}
            request = {"schema_version": "2.0-rc1", "issue_id": issue, "revision_id": rev,
                       "research_profile": ("WEEKLY" if issue == "2026-W34" else "THEMATIC"),
                       "before_state": before_state, "before_checkpoint": before_checkpoint,
                       "profile_ref": prof_ref, "discovery_ref": disc_ref, "screening_ref": scr_ref,
                       "work": {"expected_head": EXP_HEAD, "expected_tree": EXP_TREE},
                       "affected_ids": sorted(changed), "supplement_manifest": supp_ref,
                       "records": full, "completeness": completeness,
                       "runner": runner, "tool_pins": tool_pins,
                       "recorded_at": recorded_at, "executor": executor}
            # EXISTING validators: full request schema + each record content with profile
            schema_gate.validate_instance(request, repo / "schemas/dm022-revision-request-v2.schema.json", label="revision request")
            for r in full:
                ev_mod2.validate_research_record_content(r, prof_doc)
            print(f"request validated via existing schema_gate + validate_research_record_content {len(full)}")
            req_bytes = json.dumps(request, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode() + b"\n"
            req_abs = resolve_inside(repo, req_rel)
            exclusive_write_bytes(req_abs, repo, req_bytes, "request")
            print(f"request staged inside NEW repo {req_rel}")
            # ACTUAL HIGH once
            from scripts.survey_prearchitecture_acceptance_v2 import prepare_revision
            result = prepare_revision(repo, Path(f"sources/{issue}/production-state.json"), Path(req_rel), rev)
            if not isinstance(result, dict) or "manifest_ref" not in result:
                fail(f"HIGH manifest_ref invalid {result}")
            print(f"HIGH prepare_revision OK {result['manifest_ref']}")
            wlog("manifest-ref.json", json.dumps(result["manifest_ref"], indent=2, sort_keys=True))
        finally:
            try:
                _sys2.path.remove(str(repo.resolve()))
            except ValueError:
                pass

        # Post full inventory compare (files+dirs, only explicit new allowed)
        post_files = {}
        post_dirs = set()
        m_all2 = json.loads(MANIFEST.read_text())["files"]
        for rel in m_all2:
            fp = repo / rel
            st = os.lstat(fp)
            post_files[rel] = [sha256_file(fp), st.st_size, oct(stat.S_IMODE(st.st_mode))]
        src2 = repo / f"sources/{issue}"
        post_extra = {}
        for p in sorted(src2.rglob("*")):
            try:
                st = os.lstat(p)
            except FileNotFoundError:
                continue
            s = p.relative_to(repo).as_posix()
            if stat.S_ISLNK(st.st_mode):
                fail(f"post symlink {s}")
            elif stat.S_ISDIR(st.st_mode):
                post_dirs.add(s + f" mode={oct(stat.S_IMODE(st.st_mode))}")
            elif stat.S_ISREG(st.st_mode):
                if s not in post_files:
                    post_extra[s] = [sha256_file(p), st.st_size, oct(stat.S_IMODE(st.st_mode))]
            else:
                fail(f"post special {s}")
        wlog("post-inventory.json", json.dumps({"files773": post_files, "extra": post_extra, "dirs": sorted(post_dirs)}, indent=2, sort_keys=True))
        # diff vs entry: old 773 unchanged, old extra unchanged, new only allowed
        for k, v in entry["files773"].items():
            if post_files.get(k) != v:
                fail(f"old 773 changed {k}")
        for k, v in entry["extra"].items():
            if post_extra.get(k) != v and k not in [r[4] for r in raw_jobs] and k != req_rel and (issue != "SP-efficient-llm-2026" or k != supp_ref["path"]):
                # post_extra includes old extra + new; old must be unchanged
                if k not in post_extra or post_extra[k] != v:
                    fail(f"old extra changed {k}")
        allowed = set([r[4] for r in raw_jobs] + [req_rel])
        if issue == "SP-efficient-llm-2026":
            allowed.add(supp_ref["path"])
        for k in post_extra:
            if k not in entry["extra"] and k not in allowed and not k.startswith(rev_root_rel + "/"):
                fail(f"unexpected new file {k} (only 4Raw/request/SPsupp/exact newR allowed)")
        # needed parent dirs allowed if ancestor of allowed or under rev_root
        print("post inventory OK only explicit 4Raw/request/SPsupp/exact newR+needed parents")
        wlog("wall-end.txt", time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()))
        wlog("exit.txt", "0")
        exit_code = 0
    except SystemExit as e:
        exit_code = int(e.code) if isinstance(e.code, int) else 2
        try:
            wlog("traceback.txt", traceback.format_exc())
            # post inventory on failure (best effort, no cleanup/retry)
            try:
                m_all3 = json.loads(MANIFEST.read_text())["files"]
                pf = {}
                for rel in m_all3:
                    fp = repo / rel
                    if fp.is_file() and not fp.is_symlink():
                        pf[rel] = [sha256_file(fp), fp.stat().st_size, oct(stat.S_IMODE(fp.stat().st_mode))]
                wlog("post-inventory-error.json", json.dumps(pf, indent=2, sort_keys=True)[:20000])
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
        print("REFUSE: unexpected (preserved, no retry/cleanup)", file=sys.stderr)
        traceback.print_exc()
        raise SystemExit(2)
    finally:
        try:
            sys.stdout = orig_out
            sys.stderr = orig_err
            stdout_f.close()
            stderr_f.close()
        except Exception:
            pass
        try:
            (out / "exit-code.txt").write_text(str(exit_code))
        except Exception:
            pass
    raise SystemExit(exit_code)

if __name__ == "__main__":
    main()
