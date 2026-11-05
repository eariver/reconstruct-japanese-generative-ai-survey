#!/usr/bin/env python3
"""W34 resume r3 oracle checks (stdlib only; no project import/run, no git/network).

Destructive-less behavioral proofs (not AST tokens, not fake views):
- r2-style unadapted D3 call on resume-shaped baseline MUST fail (documents
  the reported exp_old/old-dir bug class with real helper + real field names).
- Adapted path (baseline + observation-only old2, DIR NAMES) MUST pass.
- Pre-import fail-closed ordering + schema10 (structural, supplements T4).
- Real R369/E439 counts + staged r3 packet bytes (stdlib source-read).
Preserved raw.
"""
from __future__ import annotations
import ast
import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path

WS = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
RESUME = WS / "notes/rephase-1-operational-rehearsal-resume-20261104"
D3 = RESUME / "w34-operator-dispose-run-r3-20261104.py"
D3_SHA = "48be58796e7ee2ef31ce0873e3223d7c0f78fb6de08aed3012f06b593f2846b8"
R2 = RESUME / "w34-operator-resume-r2-20261105.py"
R3 = RESUME / "w34-operator-resume-r3-20261105.py"
PASS, FAIL = [], []

def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")


def _load_noproject(path: Path, name: str):
    for m in list(sys.modules):
        if m.startswith("survey_") or m == "scripts":
            del sys.modules[m]
    data = path.read_bytes()
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert not any(m.startswith("survey_") for m in sys.modules), "project import leaked"
    return mod, data


def _mkfixture(root: Path, n_task: int = 2, n_rows: int = 439):
    src = root / "sources/2026-W34"
    old_ev = "sources/2026-W34/evidence/v2/accepted/bf208fake000000000000000000000000000000000000000000000000000000000001"
    old_vw = "sources/2026-W34/evidence/v2/views/accepted/f744fake000000000000000000000000000000000000000000000000000000000001"
    new_ev = "sources/2026-W34/evidence/v2/accepted/new0000000000000000000000000000000000000000000000000000000000000001"
    new_vw = "sources/2026-W34/evidence/v2/views/accepted/new0000000000000000000000000000000000000000000000000000000000000002"
    base_files: dict = {}
    base_dirs: set = set()
    def _w_norecord(rel: str, data: bytes, mode: int = 0o664):
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, mode)
        try:
            mv = memoryview(data)
            while mv:
                n = os.write(fd, mv)
                mv = mv[n:]
            os.fsync(fd)
        finally:
            os.close(fd)
        os.chmod(p, mode)
    def _w(rel: str, data: bytes, mode: int = 0o664):
        _w_norecord(rel, data, mode)
        base_files[rel] = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data), "mode": oct(mode), "nlink": 1}
    for d in [str(src.relative_to(root)), old_ev, old_ev + "/tasks", old_ev + "/results", old_vw, old_vw + "/views",
              "sources/2026-W34/evidence/proposed-input", "sources/2026-W34/external/evidence-supplement"]:
        (root / d).mkdir(parents=True, exist_ok=True)
        base_dirs.add(d)
    _w("sources/2026-W34/materiality-old-keep.json", b'{"keep": true}\n')
    base_dirs.add("sources/2026-W34/evidence/v2/accepted")
    base_dirs.add("sources/2026-W34/evidence/v2/views/accepted")
    staged_rel = "sources/2026-W34/evidence/proposed-input/interactive-evidence-TEST.json"
    staged_bytes = b'{"staged": true}\n'
    _w(staged_rel, staged_bytes)
    # snapshot BASELINE (pre-run: old dirs present, exact2 absent, no new outputs)
    # via live walk with SAME semantics as helper ((src).rglob, rels vs repo root)
    baseline_files, baseline_dirs = {}, set()
    for p in sorted((root / "sources/2026-W34").rglob("*")):
        rel = p.relative_to(root).as_posix()
        if p.is_symlink():
            raise ValueError(f"fixture symlink: {rel}")
        if p.is_dir():
            baseline_dirs.add(rel)
        elif p.is_file():
            st = os.lstat(p)
            baseline_files[rel] = {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "bytes": p.stat().st_size, "mode": oct(st.st_mode & 0o777), "nlink": st.st_nlink}
    assert "sources/2026-W34/materiality-ledger-v2.json" not in baseline_files
    assert "sources/2026-W34/profile-completeness-v2.json" not in baseline_files
    staged = {"rel": staged_rel, "sha256": hashlib.sha256(staged_bytes).hexdigest(), "bytes": len(staged_bytes)}
    # post-run outputs WITHOUT recording (new dirs, task/result/view copies, regen exact2)
    for d in [new_ev, new_ev + "/tasks", new_ev + "/results", new_vw, new_vw + "/views"]:
        (root / d).mkdir(parents=True, exist_ok=True)
    for i in range(n_task):
        tid = f"task-{i:04d}"
        _w_norecord(f"{new_ev}/tasks/{tid}.json", json.dumps({"evidence_task_id": tid}).encode())
        _w_norecord(f"{new_ev}/results/{tid}.json", json.dumps({"evidence_task_id": tid, "sha256": "a" * 64}).encode())
        _w_norecord(f"{new_vw}/views/{tid}.json", json.dumps({"evidence_task_id": tid}).encode())
    ev_acc = {"result_count": n_task, "results": [{"evidence_task_id": f"task-{i:04d}", "sha256": "a" * 64} for i in range(n_task)]}
    _w_norecord(f"{new_ev}/evidence-accepted.json", json.dumps(ev_acc).encode())
    _w_norecord(f"{new_ev}/package.json", json.dumps({"authority_supplement": {"path": "supp/rel", "sha256": "b" * 64}}).encode())
    _w_norecord(f"{new_ev}/interactive-evidence.json", b'{"staged": true}\n')
    _w_norecord(f"{new_ev}/interactive-audit.json", json.dumps({"interactive_input": {"path": f"{new_ev}/interactive-evidence.json", "sha256": hashlib.sha256(b'{"staged": true}\n').hexdigest()}}).encode())
    _w_norecord(f"{new_vw}/edition-views-accepted.json", json.dumps({"views": [{"evidence_task_id": f"task-{i:04d}", "evidence_sha256": "a" * 64} for i in range(n_task)], "view_set_sha256": new_vw.rsplit("/", 1)[-1]}).encode())
    ledger_rel, comp_rel = "sources/2026-W34/materiality-ledger-v2.json", "sources/2026-W34/profile-completeness-v2.json"
    _w_norecord(ledger_rel, json.dumps({"rows": [{"id": i} for i in range(n_rows)]}).encode())
    _w_norecord(comp_rel, json.dumps({"obligations": [{}, {}, {}], "overall_status": "LIMITED"}).encode())
    return {
        "base_files": baseline_files, "base_dirs": baseline_dirs, "staged": staged,
        "old_ledger_rel": ledger_rel, "old_comp_rel": comp_rel,
        "old_ev_names": [old_ev.rsplit("/", 1)[-1]], "old_view_names": [old_vw.rsplit("/", 1)[-1]],
        "old_ev_full": [old_ev], "old_view_full": [old_vw],
        "new_ev": new_ev, "new_vw": new_vw, "n_task": n_task, "n_rows": n_rows,
    }


def main() -> int:
    d3, _ = _load_noproject(D3, "w34d3_oracle")
    check("d3_pinned_import", hashlib.sha256(D3.read_bytes()).hexdigest() == D3_SHA, "")
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        fx = _mkfixture(Path(td) / "repo")
        repo = Path(td) / "repo"
        # 1. unadapted D3 on resume-shaped baseline MUST fail (documents reported bug class)
        try:
            d3._check_post_run_layout(repo, Path("sources/2026-W34"), dict(fx["base_files"]),
                set(fx["base_dirs"]), [fx["staged"]], fx["old_ledger_rel"], fx["old_comp_rel"], fx["old_ev_full"], fx["old_view_full"],
                fx["n_task"], "staged/rel", fx["staged"]["sha256"], "supp/rel", "b" * 64, fx["n_rows"], 3, "LIMITED", 0o664)
            check("unadapted_fails_resume_shape", False, "no failure (unexpected)")
        except (ValueError, KeyError) as e:
            msg = str(e).lower()
            check("unadapted_fails_resume_shape", ("missing" in msg or "none" in msg or "exact2" in msg or "new accepted dir" in msg), str(e)[:110])
        # 2. adapted path (baseline + observation-only old2, DIR NAMES) MUST pass
        obs_old2 = {
            fx["old_ledger_rel"]: {"sha256": "c" * 64, "bytes": 10, "mode": "0o664", "nlink": 1},
            fx["old_comp_rel"]: {"sha256": "d" * 64, "bytes": 11, "mode": "0o664", "nlink": 1},
        }
        base_obs = dict(fx["base_files"])
        base_obs.update(obs_old2)
        try:
            out = d3._check_post_run_layout(repo, Path("sources/2026-W34"), base_obs,
                set(fx["base_dirs"]), [fx["staged"]], fx["old_ledger_rel"], fx["old_comp_rel"], fx["old_ev_names"], fx["old_view_names"],
                fx["n_task"], "staged/rel", fx["staged"]["sha256"], "supp/rel", "b" * 64, fx["n_rows"], 3, "LIMITED", 0o664)
            check("adapted_passes_with_obs_old2", out.get("ledger_rows") == fx["n_rows"] and out.get("ev_results") == fx["n_task"], f"{out.get('ledger_rows')}/{out.get('ev_results')}")
        except (ValueError, KeyError) as e:
            check("adapted_passes_with_obs_old2", False, str(e)[:150])
    # 3. r2 wrapper fail-closed ordering + 10th schema (structural, supplements behavioral T4)
    import ast
    src = (RESUME / "w34-operator-resume-r2-20261105.py").read_text()
    tree = ast.parse(src)
    ok = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "stage_resume":
            seg = ast.get_source_segment(src, node) or ""
            i_raise = seg.find("BEFORE any project import")
            i_insert = seg.find("sys.path.insert")
            ok = i_raise != -1 and i_insert != -1 and i_raise < i_insert and 'rn.schema_gate' in seg
    check("r2_failclosed_and_schema10", ok, "")
    # 4. real R369/E439 counts + staged r3 packet bytes (stdlib source-read, no tokens)
    dcp = json.loads((WS / ".rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work/sources/2026-W34/discovery/discovery-accepted-v2.json").read_bytes())
    evt = (WS / ".rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work/sources/2026-W34/screening/input/event-discovery-v2.jsonl").read_bytes().splitlines()
    scp = json.loads((WS / ".rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work/sources/2026-W34/screening/v2/accepted/e193ad0507895568e369437833b87d2610d68ef50f0c6419b092f5711e26bbea/screening-accepted.json").read_bytes())
    check("real_R369_E439", len(dcp.get("records", [])) == 369 and len(evt) == 439 and len(scp.get("decisions", [])) == 439, f"{len(dcp.get('records', []))}/{len(evt)}/{len(scp.get('decisions', []))}")
    r3b = (RESUME / "w34-corrected-input-r3-20261104.json").read_bytes()
    check("r3_packet_15e87eef", hashlib.sha256(r3b).hexdigest() == "15e87eef65753bd0eeff8c512651859d6cb3b8b57127d0243925628acbf1d112", f"{len(r3b)}B")
    print(f"\nPASS {len(PASS)} FAIL {len(FAIL)}")
    return 0 if not FAIL else 1


if __name__ == "__main__":
    raise SystemExit(main())
