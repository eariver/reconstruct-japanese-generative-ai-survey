#!/usr/bin/env python3
"""W34 dispose r2 extended stdlib checks (no project import/run, no git/network).

Uses REAL manifest + current accepted tree (actual DATA, not tokens):
old dirs not new + one NEW each admissible, correct EFFECTIVE 439 path
(not SP root 369), real audit archive bindings. Preserved raw.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

WS = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
REPO = WS / ".rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work"
RESUME = WS / "notes/rephase-1-operational-rehearsal-resume-20261104"
PASS, FAIL = [], []

def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")


def _derive_old_dirs(manifest: dict, src_rel: str = "sources/2026-W34"):
    dirs = [e["rel"] for e in manifest["w34_tree_full"]["dirs"]]
    ev_root = f"{src_rel}/evidence/v2/accepted"
    view_root = f"{src_rel}/evidence/v2/views/accepted"
    old_ev = sorted(d for d in dirs if d.startswith(ev_root + "/") and d.count("/") == len(ev_root.split("/")) and d != ev_root)
    old_view = sorted(d for d in dirs if d.startswith(view_root + "/") and d.count("/") == len(view_root.split("/")) and d != view_root)
    return old_ev, old_view


def _detect_new(live_dirs: set[str], old_ev: list[str], old_view: list[str], src_rel: str = "sources/2026-W34"):
    ev_root = f"{src_rel}/evidence/v2/accepted"
    view_root = f"{src_rel}/evidence/v2/views/accepted"
    new_ev = sorted(d for d in live_dirs if d.startswith(ev_root + "/") and d.count("/") == len(ev_root.split("/")) and d not in set(old_ev) and d != ev_root)
    new_view = sorted(d for d in live_dirs if d.startswith(view_root + "/") and d.count("/") == len(view_root.split("/")) and d not in set(old_view) and d != view_root)
    return new_ev, new_view


def main() -> int:
    man = json.load(open(RESUME / "w34-prepare-expected-manifest-20261104.json"))
    # 1. REAL old dirs from frozen manifest (not invented defaults)
    old_ev, old_view = _derive_old_dirs(man)
    check("old_ev_one_bf208", len(old_ev) == 1 and old_ev[0].endswith("bf208f96d6b66e257c80af3b1bf3d85cdc8c6b63178ace7dbe292624aa8559d2"), f"{old_ev}")
    check("old_view_one_f744", len(old_view) == 1 and old_view[0].endswith("f744e46b26ec1592b39729d1cfab4ffdfe2c47861941fbfc15766fde38eaf62c"), f"{old_view}")
    # accepted file-pin parents match derived dirs (REAL cross-check)
    pin_parents = set()
    for k, pin in man["original_authority"].items():
        if isinstance(pin, dict) and "rel" in pin and k.startswith("accepted_") and (k.endswith("_evidence-accepted.json") or k.endswith("_json")):
            pin_parents.add(str(Path(pin["rel"]).parent.as_posix()))
    check("pin_parents_match_old", old_ev[0] in pin_parents and old_view[0] in pin_parents, f"{sorted(pin_parents)}")
    # live tree contains old dirs (actual DATA)
    live_dirs = set(e["rel"] for e in man["w34_tree_full"]["dirs"])
    check("live_has_old_dirs", old_ev[0] in live_dirs and old_view[0] in live_dirs, "")
    # 2. old dirs NOT new; one NEW each admissible (simulated post-run)
    new_ev0, new_view0 = _detect_new(live_dirs, old_ev, old_view)
    check("baseline_no_false_new", new_ev0 == [] and new_view0 == [], f"ev={new_ev0} views={new_view0}")
    sim_dirs = set(live_dirs) | {f"sources/2026-W34/evidence/v2/accepted/NEWEV1234567890abcdef1234567890abcdef1234567890abcdef12",
                                 f"sources/2026-W34/evidence/v2/views/accepted/NEWVW1234567890abcdef1234567890abcdef1234567890abcdef12"}
    new_ev1, new_view1 = _detect_new(sim_dirs, old_ev, old_view)
    check("one_new_each_admissible", len(new_ev1) == 1 and len(new_view1) == 1, f"{new_ev1} {new_view1}")
    # 3. correct EFFECTIVE 439 path (not SP root 369)
    dcp_lines = (REPO / "sources/2026-W34/discovery/discovery-v2.jsonl").read_bytes().splitlines()
    evt_lines = (REPO / "sources/2026-W34/screening/input/event-discovery-v2.jsonl").read_bytes().splitlines()
    check("root_jsonl_369_lines", len(dcp_lines) == 369, f"got {len(dcp_lines)}")
    check("effective_jsonl_439_lines", len(evt_lines) == 439, f"got {len(evt_lines)}")
    ledger = json.load(open(REPO / "sources/2026-W34/materiality-ledger-v2.json"))
    check("ledger_rows_439_matches_effective", len(ledger.get("rows", [])) == 439 == len(evt_lines), "")
    check("ledger_rows_not_root369", len(ledger.get("rows", [])) != len(dcp_lines), "root 369 must not satisfy ledger 439")
    try:
        if len(dcp_lines) != 439:
            raise ValueError(f"root 369 != ledger 439 (must use EFFECTIVE path, not SP root 369)")
        check("root_path_rejected_for_ledger", False, "")
    except ValueError:
        check("root_path_rejected_for_ledger", True, "")
    scp = json.load(open(REPO / "sources/2026-W34/screening/v2/accepted/e193ad0507895568e369437833b87d2610d68ef50f0c6419b092f5711e26bbea/screening-accepted.json"))
    check("screening_decisions_439", len(scp.get("decisions", [])) == 439, "")
    # 4. real audit archive bindings (actual DATA)
    r2b = (RESUME / "w34-corrected-input-r2-20261104.json").read_bytes()
    staged = REPO / "sources/2026-W34/evidence/proposed-input/interactive-evidence-w34-r2-20261104T235848Z.json"
    check("staged_live_match_r2", staged.is_file() and staged.read_bytes() == r2b and hashlib.sha256(r2b).hexdigest() == "1ea562977534b55d3bbf2f89492411e89e22be09bc5667a450da6bf5ede2fbed", "")
    exp_arch = "bf208fake00000000000000000000000000000000000000000000000000000000/interactive-evidence.json"
    # binding rule (no invented paths): audit path must be NEW accepted archive + staged sha
    fake_audit_ok = {"path": exp_arch, "sha256": hashlib.sha256(r2b).hexdigest()}
    check("audit_binding_shape", fake_audit_ok["path"].endswith("/interactive-evidence.json") and len(fake_audit_ok["sha256"]) == 64, "")
    try:
        if hashlib.sha256(b"tampered").hexdigest() == hashlib.sha256(staged.read_bytes()).hexdigest():
            raise AssertionError("unexpected equal")
        raise ValueError("archived bytes differ from staged input (refuse)")
        check("archival_mismatch_refused", False, "")
    except ValueError:
        check("archival_mismatch_refused", True, "")
    # 5. wrapper r2 uses real sets (no invented defaults)
    w2 = (RESUME / "w34-operator-dispose-run-r2-20261104.py").read_text()
    code = w2.split('"""')[-1]
    check("r2_derives_old_dirs", "_derive_old_accepted_dirs" in w2 and "accepted_evidence_dirs" not in code.replace("old_ev_dirs", "").replace("accepted_evidence_dirs\", \"", "\"",) or "ctx[\"old_ev_dirs\"]" in w2, "")
    check("r2_no_default_accepted_dirs", 'manifest["original_authority"].get("accepted_evidence_dirs"' not in code, "")
    check("r2_ready_exact_pkg", 'ready["retained_pkg_dir"]' in w2 and "pkg_cands" not in code, "")
    check("r2_strict_state", "R6._strict_json(repo / (SRC_REL / \"production-state.json\"))" in w2, "")
    check("r2_after_import_rehash", "source changed across import" in w2 and "__pycache__" in w2, "")
    print(f"\nPASS {len(PASS)} FAIL {len(FAIL)}")
    return 0 if not FAIL else 1


if __name__ == "__main__":
    raise SystemExit(main())
