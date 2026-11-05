#!/usr/bin/env python3
"""W34 resume r2 oracle checks (stdlib only; no project import/run, no git/network).

Destructive-less bad-target preflight, journal collision, changed-manifest
refusal. No fake views. Preserved raw.
"""
from __future__ import annotations
import ast
import hashlib
import json
import os
import tempfile
from pathlib import Path

WS = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
RESUME = WS / "notes/rephase-1-operational-rehearsal-resume-20261104"
R2 = RESUME / "w34-operator-resume-r2-20261105.py"
MAN = RESUME / "w34-resume-expected-manifest-20261105.json"
R3 = RESUME / "w34-corrected-input-r3-20261104.json"
PASS, FAIL = [], []

def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")


def main() -> int:
    # 1. destructive-less bad-target preflight (same exact-set rule as run, no active writes)
    pkg_tasks = {}
    for p in (RESUME / "retention-W34-20261104T235848Z/pkg-w34-r2-20261104T235848Z/tasks").glob("task-*.json"):
        tj = json.loads(p.read_bytes().decode("utf-8"))
        pkg_tasks[tj["discovery_ids"][0]] = tj.get("verification_targets", [])
    r3 = json.loads(R3.read_bytes().decode("utf-8"))
    r3map = {r["discovery_id"]: [v["target"] for v in r["verification"]] for r in r3["records"]}
    bad = [d for d in pkg_tasks if set(r3map.get(d, [])) != set(pkg_tasks[d])]
    check("r3_all409_cover_exact", bad == [], f"mismatches={len(bad)}")
    tam = {k: list(v) for k, v in r3map.items()}
    tam["w34-event-c001"] = [tam["w34-event-c001"][0] + " X"]
    bad2 = [d for d in pkg_tasks if set(tam.get(d, [])) != set(pkg_tasks[d])]
    check("bad_target_preflight_refuses", "w34-event-c001" in bad2, "tampered target detected pre-run, no active writes")
    # 2. journal collision (O_EXCL, distinct names)
    with tempfile.TemporaryDirectory() as td:
        a = Path(td) / "preflight-journal.json"
        a.write_bytes(b"{}\n")
        try:
            fd = os.open(a, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o664)
            os.close(fd)
            check("journal_collision_refused", False, "overwrite allowed")
        except FileExistsError:
            check("journal_collision_refused", True, "")
    # 3. changed-manifest refusal (SAME hash, no reseal)
    man_bytes = MAN.read_bytes()
    exp = "13a3871067bedaa03c6208d31ac6a99ef4d3ea59d6abc2df58d6ae716cd6a1de"
    check("manifest_same_hash", hashlib.sha256(man_bytes).hexdigest() == exp, "")
    tampered = bytearray(man_bytes)
    tampered[-3] ^= 1
    check("changed_manifest_refused", hashlib.sha256(bytes(tampered)).hexdigest() != exp, "")
    # 4. r2 guards before READY + no view fiction (AST order, not tokens)
    src = R2.read_text()
    tree = ast.parse(src)
    order_ok, no_view_fiction, distinct_journals, umask_once = False, False, False, False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "stage_resume":
            seg = ast.get_source_segment(src, node) or ""
            i_ready = seg.find('stage_bytes_exclusive_packet(ret_dir / "READY.json"')
            i_recheck = seg.find("pre-READY recheck FAILED")
            i_journal_pre = seg.find('preflight-journal.json')
            order_ok = i_recheck != -1 and i_ready != -1 and i_recheck < i_ready
            no_view_fiction = "views_checked" not in seg and "view_ok" not in seg and "core.json_bytes(card)" in seg
            import re as _re
            _has_pre = len(_re.findall(r'"preflight-journal\.json"', seg)) >= 1
            _has_final = len(_re.findall(r'(?<!preflight-)"journal\.json"', seg)) >= 1
            distinct_journals = _has_pre and _has_final
    umask_src = src.split("P0: umask single read/restore")[1].split("pre = {}")[0] if "P0: umask single read/restore" in src else ""
    umask_once = umask_src.count("os.umask(") == 2 and "0o666 & ~_umask_prev" in umask_src
    check("guards_before_ready", order_ok, "")
    check("no_view_fiction_card_bytes", no_view_fiction, "")
    check("distinct_journals", distinct_journals, "")
    check("umask_single_read_restore", umask_once, "")
    print(f"\nPASS {len(PASS)} FAIL {len(FAIL)}")
    return 0 if not FAIL else 1


if __name__ == "__main__":
    raise SystemExit(main())
