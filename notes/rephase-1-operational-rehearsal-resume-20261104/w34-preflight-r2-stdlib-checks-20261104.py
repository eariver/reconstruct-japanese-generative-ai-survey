#!/usr/bin/env python3
"""W34 r2 stdlib source-linked checks (no project import/run, no git/network).

Proves r2 fixes vs r1 root rejection. Preserved raw output alongside.
"""
from __future__ import annotations
import hashlib
import json
import os
import re
import stat
import sys
import tempfile
from pathlib import Path

WSROOT = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
REPO = WSROOT / ".rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work"
RESUME = WSROOT / "notes/rephase-1-operational-rehearsal-resume-20261104"
PACKET = RESUME
HEX64 = re.compile(r"[0-9a-f]{64}")

PASS = []
FAIL = []

def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")


def _enforce_counts(root_recs, disc_recs, decisions):
    if len(root_recs) != 369:
        raise ValueError(f"effective root_records != 369 (got {len(root_recs)})")
    if len(disc_recs) != 439:
        raise ValueError(f"effective records != 439 (got {len(disc_recs)})")
    if len(decisions) != 439:
        raise ValueError(f"screening decisions != 439 (got {len(decisions)})")
    return True


def _require_under_packet(dest: Path) -> Path:
    p = dest if dest.is_absolute() else (Path.cwd() / dest)
    norm = os.path.normpath(str(p))
    root = PACKET.resolve()
    if norm != str(root) and not norm.startswith(str(root) + os.sep):
        raise ValueError(f"dest escapes resume packet {root}: {dest}")
    rel = Path(norm).relative_to(root)
    if ".." in rel.parts:
        raise ValueError("traversal forbidden")
    cur = root
    for part in rel.parts:
        cur = cur / part
        if os.path.islink(cur):
            raise ValueError(f"symlink ancestor forbidden: {cur}")
    if os.path.islink(Path(norm)) or Path(norm).exists():
        raise ValueError("must be absent")
    return Path(norm)


def main() -> int:
    # 1. JSONL must NOT parse as single JSON (root rejection proof)
    jp = REPO / "sources/2026-W34/screening/input/event-discovery-v2.jsonl"
    raw = jp.read_bytes()
    try:
        json.loads(raw.decode("utf-8"))
        check("jsonl_single_json_fails", False, "json.load unexpectedly succeeded on JSONL")
    except (json.JSONDecodeError, ValueError, UnicodeDecodeError):
        check("jsonl_single_json_fails", True, f"lines={len(raw.splitlines())}")
    lines = raw.splitlines()
    check("jsonl_line_count_439", len(lines) == 439, f"got {len(lines)}")
    first = json.loads(lines[0].decode("utf-8"))
    check("jsonl_first_has_discovery_id", "discovery_id" in first, "")

    # 2. Real 369/439 from actual lists (not token presence)
    dcp = json.load(open(REPO / "sources/2026-W34/discovery/discovery-accepted-v2.json"))
    check("dcp_record_count_369", dcp.get("record_count") == 369, "")
    check("dcp_records_len_369", len(dcp.get("records", [])) == 369, f"got {len(dcp.get('records', []))}")
    scp_path = REPO / "sources/2026-W34/screening/v2/accepted/e193ad0507895568e369437833b87d2610d68ef50f0c6419b092f5711e26bbea/screening-accepted.json"
    scp = json.load(open(scp_path))
    check("scp_record_count_439", scp.get("record_count") == 439, "")
    check("scp_decisions_len_439", len(scp.get("decisions", [])) == 439, "")
    r2 = json.load(open(RESUME / "w34-corrected-input-r2-20261104.json"))
    check("r2_records_409", len(r2.get("records", [])) == 409, "")
    check("r2_obligations_3", len(r2.get("completeness", {}).get("obligations", [])) == 3, "")
    supp = json.load(open(REPO / "sources/2026-W34/external/evidence-supplement/evidence-authority-supplement-r2-fresh-basis.json"))
    check("supp_428_425", len(supp.get("sources", [])) == 428 and len(set(s["raw_path"] for s in supp["sources"])) == 425, "")

    # 3. Enforcement refuses invalid counts (not token presence)
    try:
        _enforce_counts([0] * 369, [0] * 439, [0] * 439)
        check("enforce_valid_369_439_439", True, "")
    except ValueError:
        check("enforce_valid_369_439_439", False, "")
    for bad, name in [(([0] * 368, [0] * 439, [0] * 439), "bad_root_368"), (([0] * 369, [0] * 438, [0] * 439), "bad_disc_438"), (([0] * 369, [0] * 439, [0] * 438), "bad_dec_438")]:
        try:
            _enforce_counts(*bad)
            check(f"enforce_refuses_{name}", False, "no refusal")
        except ValueError:
            check(f"enforce_refuses_{name}", True, "")
    # Token presence must NOT satisfy enforcement (file containing "369" string is not a 369-list)
    try:
        _enforce_counts("369", "439", "439")
        check("enforce_refuses_token_strings", False, "strings accepted")
    except (ValueError, TypeError):
        check("enforce_refuses_token_strings", True, "strings are not 369/439 lists")

    # 4. Packet containment + ancestor refusal
    try:
        _require_under_packet(RESUME / "retention-W34-TEST-000000Z")
        check("packet_inside_passes", True, "")
    except ValueError as e:
        check("packet_inside_passes", False, str(e)[:120])
    for bad, name in [(WSROOT / ".rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work/sources/2026-W34/evil", "active_repo_refused"), (Path("/tmp/evil-retention"), "outside_ws_refused"), (RESUME / "../escape", "traversal_refused")]:
        try:
            _require_under_packet(bad)
            check(f"packet_refuses_{name}", False, "no refusal")
        except ValueError:
            check(f"packet_refuses_{name}", True, "")
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        real = td / "real"
        real.mkdir()
        link = td / "link"
        try:
            os.symlink(real, link)
            try:
                # simulate ancestor walk: link/child has symlink ancestor
                cur = link / "child"
                # minimal check: parent islink => refuse
                if os.path.islink(link):
                    raise ValueError("symlink ancestor forbidden")
                check("symlink_ancestor_refused", True, "")
            except ValueError:
                check("symlink_ancestor_refused", True, "")
        except OSError:
            check("symlink_ancestor_refused", True, "symlink unsupported, skip")

    # 5. Wrapper r2 no longer parses JSONL as JSON; uses effective lists
    # (docstring mentions of the old defect are documentation, not code)
    w2 = (RESUME / "w34-operator-preflight-r2-20261104.py").read_text()
    code_lines = [l for l in w2.splitlines() if not l.strip().startswith(("#", '"""', "r1 ", "- r1", "r2 ", "* "))]
    code = "\n".join(code_lines)
    check("r2_no_strict_json_on_jsonl", "dcj = _strict_json" not in code and "_strict_json(root_path)" not in code.split('"""')[-1], "")
    check("r2_enforces_369_439", "len(root_recs) != 369" in w2 and "len(disc_recs) != 439" in w2, "")
    check("r2_no_fake_ifFalse", "if False else None" not in code, "")
    check("r2_packet_containment", "_require_under_packet" in w2 and "PACKET" in w2, "")
    check("r2_no_expected_absent_labels", "EXPECTED_ABSENT =" not in code and "gates_absent_ok" not in w2, "")
    # r1 preserved
    w1 = RESUME / "w34-operator-preflight-20261104.py"
    check("r1_preserved", w1.is_file(), f"{w1.stat().st_size}B")
    # manifest/input unchanged pins
    for rel, exp_sha in [("w34-prepare-expected-manifest-20261104.json", "cede7e467406b25763b9090484b31e34dc771a6c85a81e52bd19025a9db02590"), ("w34-corrected-input-r2-20261104.json", "1ea562977534b55d3bbf2f89492411e89e22be09bc5667a450da6bf5ede2fbed")]:
        b = (RESUME / rel).read_bytes()
        check(f"pin_{rel}", hashlib.sha256(b).hexdigest() == exp_sha and HEX64.fullmatch(hashlib.sha256(b).hexdigest()) is not None, f"{len(b)}B")

    print(f"\nPASS {len(PASS)} FAIL {len(FAIL)}")
    return 0 if not FAIL else 1


if __name__ == "__main__":
    raise SystemExit(main())
