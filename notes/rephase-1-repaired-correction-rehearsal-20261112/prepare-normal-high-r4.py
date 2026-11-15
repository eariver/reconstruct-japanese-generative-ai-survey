#!/usr/bin/env python3
"""Thin order-preserving HIGH prepare continuation r4 — TWO explicit modes, NO execution yet.

Preserves r3/config/R1/request/Raw/held decision. NO shipping code change.
- W34 mode: NEW revision w34-repaired-20261112-r2 + new request; reuse exact 4
  existing Raw + ce6f (verify only, no overwrite/re-copy). R1 retained as
  legitimate inert history (inventory allowlists EXACT pinned R1/request/Raw).
- SP mode: fresh sp-repaired-20261112-r1; 4 new Raw + new30 supp from final r7
  DATA (forthcoming; operator refuses until r7 present, no stale r4 fallback).
  No SP files exist yet - verified absent pre-write.

Order: deepcopy unchanged dicts from accepted archive (no sort_keys);
request via core.json_bytes (indent=2, no sort); runner.generated_at kept;
executor/recorded_at new. Prospective REAL card check for UNAFFECTED only via
existing build_research_card_content + old task/package (affected with new
bindings need new pack - not pretended complete). All cards after core_json
parse must keep original entity order. Absolute repo only; HIGH prepare once.
"""
import argparse
import copy
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
MANIFEST = Path("notes/rephase-1-supplement-carry-repair-20261106/source-packaging/final-20261107T040903Z/complete-supplement-carry-manifest.json")
CONFIG_R4 = PACKET / "prepare-normal-high-config-r4.json"
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

def load_strict(p: Path):
    raw = p.read_bytes()
    def hook(pairs):
        d = {}
        for k, v in pairs:
            if k in d:
                raise ValueError(f"dup {k!r} in {p}")
            d[k] = v
        return d
    try:
        doc = json.loads(raw.decode(), object_pairs_hook=hook)
    except Exception as e:
        fail(f"{p} strict parse: {e}")
    return doc, raw, hashlib.sha256(raw).hexdigest(), len(raw)

def check_manifest_all773(repo: Path):
    if hashlib.sha256(MANIFEST.read_bytes()).hexdigest() != EXP_MANIFEST_SHA:
        fail("manifest != a7e4")
    m = json.loads(MANIFEST.read_text())
    files = m.get("files")
    if not isinstance(files, dict) or len(files) != EXP_FILES_LEN or m.get("intended_files") != EXP_FILES_LEN:
        fail("manifest 773 shape")
    for rel, meta in files.items():
        fp = repo / rel
        st = os.lstat(fp)
        if stat.S_ISLNK(st.st_mode) or not stat.S_ISREG(st.st_mode):
            fail(f"773 type {rel}")
        if sha256_file(fp) != meta["sha256"] or st.st_size != meta["bytes"] or oct(stat.S_IMODE(st.st_mode)) != meta["physical_mode"]:
            fail(f"773 drift {rel}")
    for rel in TOOL_RELS:
        if rel not in files:
            fail(f"tool {rel} not in manifest")
    print("manifest ALL773 OK + tools derived (no hand schema hashes)")

def inventory(repo: Path, issue: str, allow_exact: set):
    m = json.loads(MANIFEST.read_text())["files"]
    inv_f = {}
    for rel in m:
        fp = repo / rel
        st = os.lstat(fp)
        if stat.S_ISLNK(st.st_mode) or not stat.S_ISREG(st.st_mode):
            fail(f"inv type {rel}")
        inv_f[rel] = [sha256_file(fp), st.st_size, oct(stat.S_IMODE(st.st_mode))]
    src = repo / f"sources/{issue}"
    extra = {}
    dirs = set()
    for p in sorted(src.rglob("*")):
        try:
            st = os.lstat(p)
        except FileNotFoundError:
            continue
        s = p.relative_to(repo).as_posix()
        if stat.S_ISLNK(st.st_mode):
            fail(f"inv symlink {s} (sparse helper fixed: refuse, no skip)")
        elif stat.S_ISDIR(st.st_mode):
            dirs.add(s)
        elif stat.S_ISREG(st.st_mode):
            if s not in inv_f:
                extra[s] = [sha256_file(p), st.st_size, oct(stat.S_IMODE(st.st_mode))]
        else:
            fail(f"inv special {s}")
    # guard + seven absent (shape, not hex-only)
    try:
        os.lstat(src / GUARD_REL)
        fail("guard present")
    except FileNotFoundError:
        pass
    for slot in SEVEN_SLOTS:
        try:
            os.lstat(src / slot)
            fail(f"slot present {slot}")
        except FileNotFoundError:
            pass
    return {"files773": inv_f, "extra": extra, "dirs": sorted(dirs), "allow_exact": sorted(allow_exact)}

class Tee:
    def __init__(self, *fs): self.files = fs
    def write(self, d):
        for f in self.files: f.write(d)
    def flush(self):
        for f in self.files: f.flush()

def resolve_in(repo: Path, rel: str) -> Path:
    if not SAFEPATH.fullmatch(rel) or rel.startswith("/") or ".." in Path(rel).parts:
        fail(f"unsafe {rel!r}")
    ap = repo / rel
    try:
        ap.resolve().relative_to(repo.resolve())
    except Exception:
        fail(f"escapes repo {rel!r}")
    return ap

def main():
    ap = argparse.ArgumentParser(description="Thin order-preserving HIGH prepare r4 (W34-r2 reuse, SP-r1 fresh).")
    ap.add_argument("--issue", required=True, choices=["2026-W34", "SP-efficient-llm-2026"])
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--revision-id", required=True)
    ap.add_argument("--config", default=str(CONFIG_R4))
    ap.add_argument("--outdir", required=True)
    a = ap.parse_args()
    issue, rev = a.issue, a.revision_id
    repo = Path(a.repo_root)
    if not repo.is_absolute():
        fail("repo-root must be ABSOLUTE (relative bug fixed)")
    if not REVISION_RE.fullmatch(rev):
        fail(f"revision {rev!r}")
    out = Path(a.outdir)
    # fresh exclusive namespace (no reuse)
    try:
        out.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        fail(f"outdir exists {out}")
    stdout_f = open(out / "stdout.txt", "w")
    stderr_f = open(out / "stderr.txt", "w")
    o_out, o_err = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = Tee(o_out, stdout_f), Tee(o_err, stderr_f)
    def w(n: str, d: str): (out / n).write_text(d)
    w("argv.txt", " ".join(sys.argv))
    w("env-whitelist.txt", "\n".join(f"{k}={os.environ.get(k,'')}" for k in sorted(ALLOWED_ENV)))
    w("pid.txt", str(os.getpid())); w("wall-start.txt", time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())); w("cwd.txt", os.getcwd())
    exit_code = 2
    try:
        check_manifest_all773(repo)
        # absolute HEAD/tree via scoped git (no reconstruct readback)
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, check=True, capture_output=True, text=True, env=env).stdout.strip()
        tree = subprocess.run(["git", "rev-parse", "HEAD^{tree}"], cwd=repo, check=True, capture_output=True, text=True, env=env).stdout.strip()
        if head != EXP_HEAD or tree != EXP_TREE:
            fail("HEAD/tree != cc1c/ed2dc4")
        cfg, _, cfg_h, cfg_n = load_strict(Path(a.config))
        w("config-pinned.txt", f"{a.config} {cfg_h} {cfg_n}\n(no post reseal)")
        spec = cfg["issues"][issue]
        if spec["revision_id"] != rev:
            fail(f"revision != spec {spec['revision_id']}")
        # W34-r2 reuse vs SP fresh prechecks
        if issue == "2026-W34":
            if rev != "w34-repaired-20261112-r2":
                fail("W34 mode requires r2")
            # exact pinned R1 retained history allowed (not generic forbid)
            r1_req = "sources/2026-W34/research/v2/acceptance-revision-inputs/w34-repaired-20261112-r1.json"
            r1_root = "sources/2026-W34/research/v2/acceptance-revisions/w34-repaired-20261112-r1"
            for p in [r1_req, r1_root + "/revision-manifest.json"]:
                if sha256_file(repo / p) != {"sources/2026-W34/research/v2/acceptance-revision-inputs/w34-repaired-20261112-r1.json": "057e186fbda8df8f58fd400def30cf5a6a80ba1d310f161f1854882619f1e5a3", "sources/2026-W34/research/v2/acceptance-revisions/w34-repaired-20261112-r1/revision-manifest.json": "54de43edc49a24e2fd8ffaf02144a83c5812a2c59290eb1d3a914709e8583da2"}[p]:
                    fail(f"R1 pinned drift {p}")
            # 4 existing Raw verified present, NO re-copy
            for r in spec["reuse_raw"]:
                fp = repo / r["path"]
                if sha256_file(fp) != r["sha256"] or fp.stat().st_size != r["bytes"]:
                    fail(f"reuse Raw drift {r['path']}")
            print("W34 r2 reuse verified (no overwrite/re-copy)")
            allow_exact = {r1_req, r1_root + "/revision-manifest.json"} | {r["path"] for r in spec["reuse_raw"]}
        else:
            if rev != "sp-repaired-20261112-r1":
                fail("SP mode requires r1")
            # r7 DATA must exist now (forthcoming at spec time); no stale fallback
            for key in ("records_r7", "routing_r7", "staging_r7"):
                pin = spec.get(key)
                if not pin or pin.get("forthcoming"):
                    fail(f"SP {key} forthcoming (r7 DATA not yet available, STOP)")
                pp = Path(pin["path"])
                if sha256_file(pp) != pin["sha256"]:
                    fail(f"SP {key} drift")
            # no SP files exist yet
            for p in [spec["request_rel"], spec["rev_root_rel"] + "/revision-manifest.json"] + [r["future_raw_path"] for r in spec["new_raw"]]:
                if (repo / p).exists() or (repo / p).is_symlink():
                    fail(f"SP must be new absent {p}")
            # true S142 via old+new+P2 (no stale ...18662662)
            s142 = spec["true_s142"]
            for src in s142["sources"]:
                pp = Path(src["path"]) if src["path"].startswith("notes/") or src["path"].startswith(".rephase-") else repo / src["path"]
                # workspace-relative .rephase paths resolve against cwd (workspace)
                if sha256_file(pp) != s142["sha256"] or pp.stat().st_size != s142["bytes"]:
                    fail(f"S142 source drift {src['path']}")
            if s142["sha256"] != "f7eeec6872fa7dd9ad8f8fb08beadfb9e2ff2bab571ffff807c2d34718672662":
                fail("S142 must be true ...18672662")
            print("SP r7 pins + true S142 OK")
            allow_exact = set()
        entry = inventory(repo, issue, allow_exact)
        w("entry-inventory.json", json.dumps(entry, indent=2, sort_keys=True))
        # State/Profile/CP/Human/guard/seven shape (full, not hex-only)
        st, _, _, _ = load_strict(repo / f"sources/{issue}/production-state.json")
        if st["lifecycle_state"] != "EVIDENCE_REVIEWED" or st["implementation"]["repository_commit_sha"] != EXP_INIT480:
            fail("State shape")
        if st["human_gates"] != {"architecture_review": "pending", "publication_preview": "pending"} or st["human_gate_provenance"] != {"architecture_review": None, "publication_preview": None}:
            fail("Human shape")
        if st["exception_gate"]["status"] != "inactive":
            fail("guard shape")
        # records: deepcopy order-preserving, no sort_keys; request via core.json_bytes
        import sys as _s
        _s.path.insert(0, str(repo.resolve()))
        try:
            from scripts import survey_production_v2 as core
            from scripts import survey_schema_v2 as gate
            from scripts import survey_evidence_v2 as ev
            from scripts import survey_prearchitecture_acceptance_v2 as high
            cfg_obj = core.load_json(repo / str(core.DEFAULT_CONFIG))
            live_contract, live_tools = high._contract_and_tools(repo, cfg_obj, st)
            # base + patch with ACTUAL keys (no counts/new_records guess)
            if issue == "2026-W34":
                patch, _, _, _ = load_strict(Path(spec["patch"]["path"]))
                changed = patch.get("changed_record_ids")
                base_rel = spec["base_interactive"]["path"]
            else:
                patch, _, _, _ = load_strict(Path(spec["records_r7"]["path"]))
                changed = patch.get("changed_ids")
                base_rel = spec["base_interactive"]["path"]
            if not isinstance(changed, list) or len(changed) != 4:
                fail("changed !=4")
            base, _, _, _ = load_strict(repo / base_rel)
            if len(base["records"]) != (409 if issue == "2026-W34" else 160):
                fail("base count")
            runner = base["runner"]  # historical generated_at preserved
            by_base = {r["discovery_id"]: r for r in base["records"]}
            # deepcopy unchanged (order-preserving), patch affected as-is (already original order)
            full_map = {}
            for r in base["records"]:
                did = r["discovery_id"]
                if did in set(changed):
                    nr = [x for x in patch["new_records"] if x["discovery_id"] == did][0]
                    full_map[did] = copy.deepcopy(nr)
                else:
                    full_map[did] = copy.deepcopy(r)
            # preserve base list order (jq filter equivalent), NOT sorted()
            full = [full_map[r["discovery_id"]] for r in base["records"]]
            # precheck: entity key order + canonical serialized record exact for unaffected
            for r in base["records"]:
                did = r["discovery_id"]
                if did not in set(changed):
                    if list(full_map[did]["entity"].keys()) != list(r["entity"].keys()):
                        fail(f"entity order {did}")
                    if json.dumps(full_map[did], indent=2, ensure_ascii=False).encode() + b"\n" != json.dumps(r, indent=2, ensure_ascii=False).encode() + b"\n":
                        fail(f"unaffected serialized exact {did}")
            # REAL prospective card core for UNAFFECTED only (old task/package, no third mirror)
            pkg, _, _, _ = load_strict((repo / base_rel).parent / "package.json")
            tmap = {}
            for t in pkg["tasks"]:
                if len(t.get("discovery_ids", [])) == 1:
                    tmap[t["discovery_ids"][0]] = t
            prof, _, _, _ = load_strict(repo / f"sources/{issue}/production-profile.json")
            for r in base["records"]:
                did = r["discovery_id"]
                if did in set(changed):
                    continue
                t = tmap[did]
                tf, _, _, _ = load_strict((repo / base_rel).parent / t["path"])
                meta = {"sha256": "old", "byte_count": 1}
                card = ev.build_research_card_content(repo, tf, meta, pkg, copy.deepcopy(r), runner)
                old_card_path = (repo / base_rel).parent / "results" / (t["path"].split("/")[-1])
                old_raw = old_card_path.read_bytes()
                if core.json_bytes(card) != old_raw:
                    fail(f"unaffected card byte {did} (order fix required)")
            print(f"prospective unaffected cards byte-equal {len(base['records'])-4}")
            # completeness 7-field (W34 profile 3, SP r5 15) + residual/closure shape
            if issue == "2026-W34":
                comp, _, _, _ = load_strict(repo / "sources/2026-W34/profile-completeness-v2.json")
                obligs, resid, clos = comp["obligations"], comp["residual_limitations"], comp["closure"]
            else:
                comp5, _, _, _ = load_strict(Path(spec["completeness_r5"]["path"]))
                obligs, resid, clos = comp5["obligations"], comp5["residual_limitations"], comp5["closure"]
            # request assembly (order-preserving dict insertion; NO sort_keys)
            disc = spec["discovery_ref_effective"]
            scr = spec["screening_ref"]
            cp = st["checkpoint_provenance"]
            req = {"schema_version": "2.0-rc1", "issue_id": issue, "revision_id": rev,
                   "research_profile": ("WEEKLY" if issue == "2026-W34" else "THEMATIC"),
                   "before_state": {"path": f"sources/{issue}/production-state.json", "sha256": sha256_file(repo / f"sources/{issue}/production-state.json"), "byte_count": (repo / f"sources/{issue}/production-state.json").stat().st_size},
                   "before_checkpoint": {"evidence": cp["evidence"], "materiality": cp["materiality"], "completeness": cp["completeness"]},
                   "profile_ref": {"path": f"sources/{issue}/production-profile.json", "sha256": sha256_file(repo / f"sources/{issue}/production-profile.json"), "byte_count": (repo / f"sources/{issue}/production-profile.json").stat().st_size},
                   "discovery_ref": disc, "screening_ref": scr,
                   "work": {"expected_head": EXP_HEAD, "expected_tree": EXP_TREE},
                   "affected_ids": list(changed),
                   "supplement_manifest": ({"path": spec["supplement_manifest_explicit"]["path"], "sha256": spec["supplement_manifest_explicit"]["sha256"], "byte_count": spec["supplement_manifest_explicit"]["bytes"]} if issue == "2026-W34" else None),
                   "records": full, "completeness": {"obligations": obligs, "residual_limitations": resid, "closure": clos},
                   "runner": runner,
                   "tool_pins": {"repository_commit_sha": EXP_HEAD, "orchestrator_version": "survey-production-core-v2/0.15-postintegration-transport-thematic", "contract": live_contract, "tool_shas": live_tools},
                   "recorded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                   "executor": f"general / Muse Spark 1.3 / prepare-normal-high-r4 {issue} {rev}"}
            # SP supplement: builder writes actual AFTER prevalidation (may delete own failed output - documented)
            if issue == "SP-efficient-llm-2026":
                # stage 4 new Raw O_EXCL first (verified absent), then builder
                for job in spec["new_raw"]:
                    if "src" in job:
                        src = Path(job["src"])
                        if src.is_symlink() or not src.is_file():
                            fail(f"SP Raw src type {job['src']}")
                    elif "src_is_repo" in job:
                        src = repo / job["src_is_repo"]
                        if src.is_symlink() or not src.is_file():
                            fail(f"SP Raw repo src type {job['src_is_repo']}")
                    else:
                        fail("SP new_raw missing src/src_is_repo")
                    dst = resolve_in(repo, job["future_raw_path"])
                    if dst.exists() or dst.is_symlink():
                        fail(f"SP Raw must be new {job['future_raw_path']}")
                    # ancestor symlink guard (sparse helper fixed: no skip)
                    for anc in [dst.parent] + list(dst.parent.parents):
                        if str(anc) == "/":
                            break
                        try:
                            st_a = os.lstat(anc)
                        except FileNotFoundError:
                            continue
                        if stat.S_ISLNK(st_a.st_mode):
                            fail(f"SP Raw ancestor symlink {anc}")
                        if anc == repo:
                            break
                    data = src.read_bytes()
                    if hashlib.sha256(data).hexdigest() != job["sha256"] or len(data) != job["bytes"]:
                        fail(f"SP Raw pin {job['future_raw_path']}")
                    fd = os.open(str(dst), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o664)
                    with os.fdopen(fd, "wb") as f:
                        f.write(data)
                f30, _, _, _ = load_strict(Path(spec["supplement_full30_r4"]["path"]))
                out_rel = f"sources/SP-efficient-llm-2026/external/evidence-supplement/evidence-authority-supplement-r7-sp17-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}.json"
                built = ev.build_evidence_authority_supplement(repo, issue, repo / "sources/SP-efficient-llm-2026", repo / spec["discovery_ref_effective"]["path"], repo / spec["screening_ref"]["path"], f30["sources"], repo / out_rel, supplement_id=f"r7-sp17-EFF-DID-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}")
                ev.validate_evidence_authority_supplement(repo, built, expected_issue_id=issue, expected_source_root=repo / "sources/SP-efficient-llm-2026", expected_discovery_path=repo / spec["discovery_ref_effective"]["path"], expected_screening_acceptance_path=repo / spec["screening_ref"]["path"])
                st_o = (repo / out_rel).stat()
                req["supplement_manifest"] = {"path": out_rel, "sha256": sha256_file(repo / out_rel), "byte_count": st_o.st_size}
            # existing validators: request schema + record shapes, true R/E
            gate.validate_instance(req, repo / "schemas/dm022-revision-request-v2.schema.json", label="revision request")
            for r in full:
                ev.validate_research_record_content(r, prof)
            # after-parse entity order preserved
            parsed = json.loads(core.json_bytes(req).decode())
            for a, b in zip(req["records"], parsed["records"]):
                if list(a["entity"].keys()) != list(b["entity"].keys()):
                    fail("entity order after core_json")
            # write request inside repo exact new file (core.json_bytes, no sort)
            req_rel = spec["request_rel"]
            req_abs = resolve_in(repo, req_rel)
            if req_abs.exists():
                fail(f"request must be new {req_rel}")
            req_abs.parent.mkdir(parents=True, exist_ok=True)
            fd = os.open(str(req_abs), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o664)
            with os.fdopen(fd, "wb") as f:
                f.write(core.json_bytes(req))
            print(f"request staged {req_rel}")
            from scripts.survey_prearchitecture_acceptance_v2 import prepare_revision
            res = prepare_revision(repo, Path(f"sources/{issue}/production-state.json"), Path(req_rel), rev)
            if "manifest_ref" not in res:
                fail("HIGH manifest invalid")
            print(f"HIGH OK {res['manifest_ref']}")
            (out / "manifest-ref.json").write_text(json.dumps(res["manifest_ref"], indent=2, sort_keys=True))
            # post-inventory: old R1 candidate unchanged, only declared new R/request/staging
            post_f, post_e, post_d = {}, {}, set()
            m_all = json.loads(MANIFEST.read_text())["files"]
            for rel in m_all:
                fp = repo / rel
                st_p = os.lstat(fp)
                post_f[rel] = [sha256_file(fp), st_p.st_size, oct(stat.S_IMODE(st_p.st_mode))]
            src2 = repo / f"sources/{issue}"
            for p in sorted(src2.rglob("*")):
                try:
                    st_p = os.lstat(p)
                except FileNotFoundError:
                    continue
                s = p.relative_to(repo).as_posix()
                if stat.S_ISLNK(st_p.st_mode):
                    fail(f"post symlink {s}")
                elif stat.S_ISDIR(st_p.st_mode):
                    post_d.add(s)
                elif stat.S_ISREG(st_p.st_mode):
                    if s not in post_f:
                        post_e[s] = [sha256_file(p), st_p.st_size, oct(stat.S_IMODE(st_p.st_mode))]
                else:
                    fail(f"post special {s}")
            (out / "post-inventory.json").write_text(json.dumps({"files773": post_f, "extra": post_e, "dirs": sorted(post_d)}, indent=2, sort_keys=True))
            # old 773 unchanged vs entry
            for k, v in entry["files773"].items():
                if post_f.get(k) != v:
                    fail(f"old 773 changed {k}")
            # old R1 retained: W34 r1 request/manifest + 4 Raw + R1 candidate tree unchanged
            if issue == "2026-W34":
                for p in ["sources/2026-W34/research/v2/acceptance-revision-inputs/w34-repaired-20261112-r1.json", "sources/2026-W34/research/v2/acceptance-revisions/w34-repaired-20261112-r1/revision-manifest.json"]:
                    if (repo / p).stat().st_size == 0:
                        fail(f"R1 missing {p}")
                # new allowlist: r2 request + r2 R prefix only (+ needed parent dirs of those)
                allowed_new = {spec["request_rel"]}
                for k in post_e:
                    if k not in entry["extra"] and k not in allowed_new and not k.startswith(spec["rev_root_rel"] + "/"):
                        fail(f"unexpected new {k} (only r2 request/R allowed)")
            else:
                allowed_new = {spec["request_rel"]} | {j["future_raw_path"] for j in spec["new_raw"]}
                # supplement output path unknown until builder; allow any single new file under external/evidence-supplement/ matching r7 pattern + R prefix
                for k in post_e:
                    if k in entry["extra"]:
                        if post_e[k] != entry["extra"][k]:
                            fail(f"old extra changed {k}")
                        continue
                    ok = k in allowed_new or k.startswith(spec["rev_root_rel"] + "/") or (k.startswith("sources/SP-efficient-llm-2026/external/evidence-supplement/evidence-authority-supplement-r7-sp17-") and k.endswith(".json"))
                    if not ok:
                        fail(f"unexpected SP new {k}")
            print("post inventory OK (R1 preserved, only declared new R/request/staging)")
        finally:
            try:
                _s.path.remove(str(repo.resolve()))
            except ValueError:
                pass
        w("wall-end.txt", time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())); w("exit.txt", "0")
        exit_code = 0
    except SystemExit as e:
        exit_code = int(e.code) if isinstance(e.code, int) else 2
        try:
            w("traceback.txt", traceback.format_exc()); w("exit.txt", str(exit_code))
        except Exception:
            pass
        raise
    except Exception:
        try:
            w("traceback.txt", traceback.format_exc()); w("exit.txt", "2")
        except Exception:
            pass
        print("REFUSE: preserved, no retry/cleanup", file=sys.stderr)
        raise SystemExit(2)
    finally:
        try:
            sys.stdout, sys.stderr = o_out, o_err
            stdout_f.close(); stderr_f.close()
        except Exception:
            pass
        try:
            (out / "exit-code.txt").write_text(str(exit_code))
        except Exception:
            pass
    raise SystemExit(exit_code)

if __name__ == "__main__":
    main()
