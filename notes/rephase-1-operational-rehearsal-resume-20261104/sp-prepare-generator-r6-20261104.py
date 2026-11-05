#!/usr/bin/env python3
"""r6 prepare baseline generator — stdlib-only, data-only, no project imports, no git, no network.

Narrow successor of the r5 generator (preserved unchanged). Identical behavior
plus ONE structured addition: triangulated test-file pins
(delivered/intended vs live e84 vs r3-recorded prefixes), so the r6 tool can
enforce the exact known d486 pin instead of skipping it. Every pin is generated
programmatically from live bytes; NOTHING is hand-transcribed.

Writes --out (packet-local manifest path) + prints path/bytes/sha256 to stdout.
Exit 0 when all cross-checks clean, exit 2 when unresolved entries exist
(manifest is still written as evidence).
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path

HEX64 = re.compile(r"[0-9a-f]{64}")
HEX40 = re.compile(r"[0-9a-f]{40}")
HEX16 = re.compile(r"[0-9a-f]{16}")
HEXRUN = re.compile(r"[0-9a-f]{30,}")
TEST_REL = "tests/test_evidence_scaling_v2.py"


def _strict_json(path: Path):
    raw = path.read_bytes()

    def _hook(pairs):
        o = {}
        for k, v in pairs:
            if k in o:
                raise ValueError(f"duplicate JSON key in {path}: {k!r}")
            o[k] = v
        return o

    val = json.loads(raw.decode("utf-8"), object_pairs_hook=_hook)
    if not isinstance(val, dict):
        raise ValueError(f"expected JSON object: {path}")
    return val


def _pin_live(repo_root: Path, rel: str):
    """Pin a live file: regular, no symlinks anywhere; mode/nlink recorded (not enforced here)."""
    root = repo_root.resolve()
    cur = root
    for part in Path(rel).parts:
        cur = cur / part
        if os.path.islink(cur):
            raise ValueError(f"symlink component forbidden: {cur}")
    abs_p = root / rel
    try:
        abs_p.resolve().relative_to(root)
    except ValueError:
        raise ValueError(f"escapes repo_root: {rel}")
    if os.path.islink(abs_p) or not abs_p.is_file():
        raise ValueError(f"missing/unsafe live file: {rel}")
    st = os.lstat(abs_p)
    data = abs_p.read_bytes()
    return {
        "rel": rel,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "mode": oct(st.st_mode & 0o777),
        "islink": False,
        "nlink": st.st_nlink,
        "regular": stat.S_ISREG(st.st_mode),
    }


def _scan_hex_runs(raw: bytes):
    """Maximal [0-9a-f]{30,} runs with lengths; allowed: 64 (file), 40 (commit/tree), 16 (ids)."""
    text = raw.decode("utf-8", errors="replace")
    out = {}
    for m in HEXRUN.finditer(text):
        out.setdefault(len(m.group(0)), []).append(m.group(0)[:24])
    return {str(k): {"count": len(v), "sample": v[0]} for k, v in sorted(out.items())}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", type=Path, required=True)
    ap.add_argument("--resume", type=Path, required=True)
    ap.add_argument("--intake", type=Path, required=True)
    ap.add_argument("--supp-intake", type=Path, required=True)
    ap.add_argument("--delivery-manifest", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    repo = a.repo_root
    resume = a.resume
    errs: list[str] = []

    def _note(msg: str) -> None:
        errs.append(msg)

    src_rel = "sources/SP-efficient-llm-2026"
    src = repo / src_rel

    # ---- active instance cross-check (programmatic read of r3 machine) ----
    r3 = _strict_json(resume / "current-observation-r3-20261104.json")
    active = {
        "repo_root": ".rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work",
        "recorded_head": r3["active_instance"]["selected_head"],
        "recorded_parent": r3["active_instance"]["parent"],
        "recorded_tree": r3["active_instance"]["recorded_tree"],
        "historical_implementation_sha": r3["states"]["sp_state"]["implementation_repo_commit_sha256"]
        if "implementation_repo_commit_sha256" in r3["states"]["sp_state"]
        else r3["states"]["sp_state"].get("implementation_repo_commit_sha", "480823560c0c26ed2e5baa18e0e79a22b2839a27"),
    }
    sp_state_live = _strict_json(repo / f"{src_rel}/production-state.json")
    active["historical_implementation_sha_live"] = sp_state_live["implementation"]["repository_commit_sha"]
    if active["historical_implementation_sha_live"] != "480823560c0c26ed2e5baa18e0e79a22b2839a27":
        _note(f"State historical impl drift: {active['historical_implementation_sha_live']}")

    # ---- original authority (live re-read) + cross-check vs r3 machine ----
    watched = {
        "state": f"{src_rel}/production-state.json",
        "profile": f"{src_rel}/production-profile.json",
        "dcp_jsonl": f"{src_rel}/discovery/discovery-v2.jsonl",
        "dcp_accepted": f"{src_rel}/discovery/discovery-accepted-v2.json",
        "scp_accepted": r3["dcp_scp"]["sp_scp_accepted"]["path"],
        "ledger": f"{src_rel}/materiality-ledger-v2.json",
        "completeness": f"{src_rel}/profile-completeness-v2.json",
        "supplement_r1": r3["sp_old_products_held_changes_required"]["supplement_r1_fresh"]["path"],
        "proposed_input": r3["sp_old_products_held_changes_required"]["proposed_input"]["path"],
        "config": "config/survey-production-v2.json",
    }
    authority: dict = {}
    for key, rel in watched.items():
        authority[key] = _pin_live(repo, rel)
    ev_acc_root = src / "evidence/v2/accepted"
    ev_dirs = sorted(p.name for p in ev_acc_root.iterdir() if p.is_dir() and not p.is_symlink())
    views_root = src / "evidence/v2/views/accepted"
    view_dirs = sorted(p.name for p in views_root.iterdir() if p.is_dir() and not p.is_symlink())
    authority["accepted_evidence_dirs"] = ev_dirs
    authority["accepted_views_dirs"] = view_dirs
    for d in ev_dirs:
        for name in ("evidence-accepted.json", "package.json", "interactive-audit.json"):
            rel = f"{src_rel}/evidence/v2/accepted/{d}/{name}"
            if (repo / rel).exists():
                authority[f"accepted_evidence_{d}_{name}"] = _pin_live(repo, rel)
    for d in view_dirs:
        rel = f"{src_rel}/evidence/v2/views/accepted/{d}/edition-views-accepted.json"
        if (repo / rel).exists():
            authority[f"accepted_views_{d}_json"] = _pin_live(repo, rel)
    for mod in ("scripts/survey_evidence_v2.py", "scripts/run_evidence_v2_interactive.py",
                "scripts/survey_research_authority_v2.py", "scripts/survey_agent_tool_v2.py",
                "scripts/survey_agent_control_v2.py", "scripts/survey_production_v2.py",
                "scripts/survey_screening_v2.py", "scripts/survey_discovery_v2.py",
                "scripts/survey_completeness_v2.py", "scripts/survey_schema_v2.py"):
        authority[f"module_{Path(mod).name}"] = _pin_live(repo, mod)
    r3pins = {
        "state": r3["states"]["sp_state"]["sha256"],
        "profile": r3["profiles"]["sp_profile"]["sha256"],
        "dcp_jsonl": r3["dcp_scp"]["sp_dcp_raw_jsonl"]["sha256"],
        "dcp_accepted": r3["dcp_scp"]["sp_dcp_discovery_accepted"]["sha256"],
        "scp_accepted": r3["dcp_scp"]["sp_scp_accepted"]["sha256"],
        "ledger": r3["sp_old_products_held_changes_required"]["ledger"]["sha256"],
        "completeness": r3["sp_old_products_held_changes_required"]["completeness"]["sha256"],
        "supplement_r1": r3["sp_old_products_held_changes_required"]["supplement_r1_fresh"]["sha256"],
        "proposed_input": r3["sp_old_products_held_changes_required"]["proposed_input"]["sha256"],
        "config": r3["config_canonical_regeneration"]["sha256"],
    }
    for key, expect in r3pins.items():
        if authority[key]["sha256"] != expect:
            _note(f"authority drift vs r3 machine {key}: live {authority[key]['sha256']} != r3 {expect}")
    st = sp_state_live
    cand = {
        "lifecycle_state": st.get("lifecycle_state"),
        "machine_evidence": st.get("machine_checkpoints", {}).get("evidence"),
        "machine_materiality": st.get("machine_checkpoints", {}).get("materiality"),
        "machine_completeness": st.get("machine_checkpoints", {}).get("completeness"),
        "cp_evidence": st.get("checkpoint_provenance", {}).get("evidence"),
        "cp_materiality": st.get("checkpoint_provenance", {}).get("materiality"),
        "cp_completeness": st.get("checkpoint_provenance", {}).get("completeness"),
        "human_gates": st.get("human_gates"),
        "human_gate_provenance": st.get("human_gate_provenance"),
    }
    for k, v in (("lifecycle_state", "CANDIDATES_NORMALIZED"), ("machine_evidence", "pending"),
                 ("machine_materiality", "pending"), ("machine_completeness", "pending"),
                 ("cp_evidence", None), ("cp_materiality", None), ("cp_completeness", None)):
        if cand[k] != v:
            _note(f"State CAND gate {k}={cand[k]!r} expected {v!r}")
    if cand["human_gates"] != {"architecture_review": "pending", "publication_preview": "pending"}:
        _note(f"State human_gates drift: {cand['human_gates']}")
    if cand["human_gate_provenance"] != {"architecture_review": None, "publication_preview": None}:
        _note("State human_gate_provenance drift")
    for name in ("DISCOVERY_COLLECTED", "ISSUE_INITIALIZED"):
        rel = f"{src_rel}/orchestration/v2/checkpoints/{name}.json"
        pin = _pin_live(repo, rel)
        authority[f"checkpoint_{name}"] = pin
        if pin["sha256"] != r3["checkpoints"][f"sp_{name.lower()}"]["sha256"]:
            _note(f"checkpoint {name} drift vs r3")
    for absent_rel in (f"{src_rel}/gates", "gates",
                       f"{src_rel}/candidate-matrix-v2.json", f"{src_rel}/candidate-selection-v2.json",
                       f"{src_rel}/orchestration/v2/interactive/selection-architecture-input.json",
                       f"{src_rel}/CANDIDATES_NORMALIZED.json", f"{src_rel}/EVIDENCE_REVIEWED.json"):
        p = repo / absent_rel
        if os.path.islink(p) or p.exists():
            _note(f"must-be-absent present: {absent_rel}")

    # ---- FULL SP tree enumeration (files digest/mode/type/size + dirs; no skips) ----
    tree_files: list[dict] = []
    tree_dirs: list[dict] = []
    for p in sorted(src.rglob("*")):
        rel = p.relative_to(repo).as_posix()
        if p.is_symlink():
            _note(f"symlink in SP tree (refuse): {rel}")
            continue
        if p.is_dir():
            tree_dirs.append({"rel": rel, "mode": oct(os.lstat(p).st_mode & 0o777)})
        elif p.is_file():
            stt = os.lstat(p)
            data = p.read_bytes()
            tree_files.append({"rel": rel, "bytes": len(data),
                               "sha256": hashlib.sha256(data).hexdigest(),
                               "mode": oct(stt.st_mode & 0o777), "nlink": stt.st_nlink})
    ledger_refs = {}
    for e in tree_files:
        if e["rel"].startswith(f"{src_rel}/orchestration/") and e["rel"].endswith(".json"):
            txt = (repo / e["rel"]).read_text(encoding="utf-8", errors="replace")
            hit = ("materiality-ledger" in txt) or ("profile-completeness" in txt)
            ledger_refs[e["rel"]] = hit
            if hit:
                _note(f"stage file references ledger/completeness: {e['rel']}")

    # ---- delivery 771 preflight data ----
    delivery = _strict_json(a.delivery_manifest)
    intended: dict = delivery["files"]
    if len(intended) != 771:
        _note(f"delivery intended count={len(intended)} expected 771")

    # ---- triangulated test-file pins (r6 addition; no transcription) ----
    test_pin: dict = {"rel": TEST_REL}
    if TEST_REL not in intended:
        _note(f"test file missing from intended map: {TEST_REL}")
    else:
        test_pin["delivered"] = {k: intended[TEST_REL][k] for k in ("sha256", "bytes", "physical_mode", "git_mode")}
    live_test = _pin_live(repo, TEST_REL)
    test_pin["live_e84"] = live_test
    r3rows = [r for r in r3.get("intended_771_vs_e84", {}).get("mismatch_list", []) if r[0] == TEST_REL]
    if not r3rows:
        _note("r3 recorded test diff row missing")
    else:
        _, r3_del_prefix, r3_e84_prefix, r3_del_bytes, r3_e84_bytes = r3rows[0]
        test_pin["r3_recorded"] = {"delivered_prefix16": r3_del_prefix, "e84_prefix16": r3_e84_prefix,
                                   "delivered_bytes": r3_del_bytes, "e84_bytes": r3_e84_bytes}
        if not live_test["sha256"].startswith(r3_e84_prefix):
            _note("live test SHA does not match r3-recorded e84 prefix")
        if live_test["bytes"] != r3_e84_bytes:
            _note("live test bytes do not match r3-recorded e84 bytes")
        if TEST_REL in intended:
            if not intended[TEST_REL]["sha256"].startswith(r3_del_prefix):
                _note("intended test SHA does not match r3-recorded delivered prefix")
            if intended[TEST_REL]["bytes"] != r3_del_bytes:
                _note("intended test bytes do not match r3-recorded delivered bytes")
        if live_test["sha256"] == intended[TEST_REL]["sha256"]:
            _note("live test unexpectedly equals delivered bytes (known diff violated)")

    # ---- corrected DATA (r4) live reads, no transcription ----
    r4supp_path = resume / "sp-corrected-supplement-r4-20261104.json"
    r4input_path = resume / "sp-corrected-input-r4-20261104.json"
    r4supp_raw = r4supp_path.read_bytes()
    r4input_raw = r4input_path.read_bytes()
    r4supp = json.loads(r4supp_raw.decode("utf-8"))
    r4input = json.loads(r4input_raw.decode("utf-8"))
    corrected = {
        "supplement": {"path": r4supp_path.name, "bytes": len(r4supp_raw),
                       "sha256": hashlib.sha256(r4supp_raw).hexdigest()},
        "input": {"path": r4input_path.name, "bytes": len(r4input_raw),
                  "sha256": hashlib.sha256(r4input_raw).hexdigest()},
    }
    for label, raw in (("supplement", r4supp_raw), ("input", r4input_raw)):
        runs = _scan_hex_runs(raw)
        bad = {k: v for k, v in runs.items() if k not in ("64", "40", "16")}
        if bad:
            _note(f"malformed embedded hex in r4 {label}: {bad}")

    # ---- all30 rows: live pins + sidecar reverse-lookup + task-suffix check ----
    sidecar_by_sha: dict[str, list[str]] = {}
    for intake_dir in (a.intake, a.supp_intake):
        for p in intake_dir.iterdir():
            if p.name.endswith(".sha256.txt"):
                val = p.read_text(encoding="utf-8").strip().split()[0]
                sidecar_by_sha.setdefault(val, []).append(f"{intake_dir.name}/{p.name}")
    rows30: list[dict] = []
    for s in r4supp["sources"]:
        did, sid = s["discovery_id"], s["supplement_source_id"]
        tid = s["evidence_task_id"]
        expect_tid = "evidence:" + r4supp["issue_id"] + ":" + hashlib.sha256(did.encode()).hexdigest()[:16]
        suffix_ok = tid == expect_tid  # rebuilt from live fields, no transcription
        row = {"did": did, "supplement_source_id": sid, "evidence_task_id": tid,
               "raw_path": s["raw_path"], "bytes": s["byte_count"],
               "sha256": s["raw_sha256"], "hex64": bool(HEX64.fullmatch(s["raw_sha256"])),
               "task_suffix_ok": suffix_ok,
               "source_class_pair": [s["source_type"], s["source_class"]]}
        if s["raw_path"].startswith(f"{src_rel}/external/evidence-supplement/raw/supp-"):
            live = _pin_live(repo, s["raw_path"])
            row["live"] = live
            if live["sha256"] != s["raw_sha256"] or live["bytes"] != s["byte_count"]:
                _note(f"existing Raw drift {did}: live {live['sha256']}/{live['bytes']} vs supp {s['raw_sha256']}/{s['byte_count']}")
        else:
            row["live"] = None
        row["sidecars"] = sidecar_by_sha.get(s["raw_sha256"], [])
        rows30.append(row)
    r4map = _strict_json(resume / "sp-staging-expected-manifest-r4-20261104.json")
    locators = {r["supplement_source_id"]: r["src_packet_data"] for r in r4map["staging_rows"]}
    wsroot = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
    for row in rows30:
        if row["live"] is None:
            src_pkt = wsroot / locators[row["supplement_source_id"]]
            if os.path.islink(src_pkt) or not src_pkt.is_file():
                _note(f"unsafe packet source: {src_pkt}")
                continue
            data = src_pkt.read_bytes()
            h = hashlib.sha256(data).hexdigest()
            row["packet"] = {"path": locators[row["supplement_source_id"]],
                             "bytes": len(data), "sha256": h}
            if h != row["sha256"] or len(data) != row["bytes"]:
                _note(f"packet drift {row['did']}: file {h}/{len(data)} vs supp {row['sha256']}/{row['bytes']}")
    scp = _strict_json(repo / watched["scp_accepted"])
    non_drop = sorted(d["discovery_id"] for d in scp["decisions"] if d["decision"] != "DROP")
    input_ids = sorted(r["discovery_id"] for r in r4input["records"])
    if input_ids != non_drop:
        _note(f"input IDs != screening non-DROP ({len(input_ids)} vs {len(non_drop)})")
    if len(r4input["records"]) != 160 or len(r4input["completeness"]["obligations"]) != 15:
        _note("corrected input counts != 160/15")

    manifest = {
        "single_use": "r6 prepare-only expected-pin manifest (generated, no hand transcription). Reviewed before execution; tool re-verifies live and refuses on drift.",
        "generator": {"script": "notes/rephase-1-operational-rehearsal-resume-20261104/sp-prepare-generator-r6-20261104.py",
                      "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      "delivery_manifest": {"path": str(a.delivery_manifest),
                                            "bytes": a.delivery_manifest.stat().st_size,
                                            "sha256": hashlib.sha256(a.delivery_manifest.read_bytes()).hexdigest()}},
        "active_instance": active,
        "delivery": {"head": delivery.get("head"), "head_tree": delivery.get("head_tree"),
                     "intended_files": delivery.get("intended_files"), "intended": intended,
                     "test_pin": test_pin,
                     "known_test_exception": "tests/test_evidence_scaling_v2.py differs e84 vs delivery by exact triangulated pins above (recorded, not a failure)"},
        "original_authority": authority,
        "state_cand": cand,
        "gates_absent_ok": True,
        "sp_tree_full": {"files": tree_files, "dirs": tree_dirs,
                         "file_count": len(tree_files), "dir_count": len(tree_dirs)},
        "stage_ledger_ref_scan": ledger_refs,
        "supplement30": rows30,
        "corrected": corrected,
        "input_universe": {"non_drop_count": len(non_drop), "input_count": len(input_ids)},
        "unresolved": errs,
        "clean": not errs,
    }
    out = a.out
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps({"out": str(out), "bytes": out.stat().st_size,
                      "sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
                      "clean": not errs, "unresolved": errs}, indent=2))
    return 0 if not errs else 2


if __name__ == "__main__":
    raise SystemExit(main())
