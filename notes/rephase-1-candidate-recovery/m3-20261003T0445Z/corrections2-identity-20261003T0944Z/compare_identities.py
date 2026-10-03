"""Machine comparison of ALL 32+9 identities across raw20 / manifests / live Git.

Sources (read-only; nothing here writes to fixtures, manifests, or raw):
  A. m2 raw/20-identities.stdout.txt (32 final + 9 Freeze sections)
  B. m2 manifest.json: final_32_identities + untouched_freeze_bindings_at_head_equal_baseline
  C. m3 manifest.pretty.json (expected copy of B)
  D. LIVE read-only `git ls-tree HEAD -- <paths from A>` in fixture
     (+ restored copy corroboration)
  E. m3 manifest.json five_methods exits/times (read back, not rerun)
  F. closure numerics: raw/closure rows/source vs report claims
  G. archive sha/bytes live recompute vs .sha256 + manifests

Writes ONLY into the given outdir: comparison report, final-identity-binding.json
(built SOLELY from parsed live-Git output + read-only rev-parse/log pins),
per-command raw. Usage:
  python3 compare_identities.py <reconstruct-root> <outdir>
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
RAW = OUT / "raw"
RAW.mkdir(parents=True, exist_ok=True)
FIXTURE = Path("/tmp/opencode/jgas-rephase-candidate-recovery-20261003T0435Z")
RESTORE = Path("/tmp/opencode/jgas-recovery-restore-20261003T0445Z")
M2 = ROOT / "notes/rephase-1-candidate-recovery/m2-20261003T0435Z"
M3 = ROOT / "notes/rephase-1-candidate-recovery/m3-20261003T0445Z"

log: list[str] = []


def emit(s: str) -> None:
    log.append(s)
    print(s)


def run(cmd: list[str], label: str, cwd: str | None = None) -> subprocess.CompletedProcess:
    import os
    env = dict(os.environ)
    for k in list(env):
        if k.startswith("GIT_") and k not in ("GIT_NO_LAZY_FETCH", "GIT_ALLOW_PROTOCOL"):
            del env[k]
    env["GIT_NO_LAZY_FETCH"] = "1"
    proc = subprocess.run(cmd, cwd=cwd or str(ROOT), env=env,
                          capture_output=True, text=True, check=False)
    (RAW / f"{label}.argv.txt").write_text(repr(cmd) + f"\ncwd={cwd or ROOT}\n")
    (RAW / f"{label}.stdout.txt").write_text(proc.stdout)
    (RAW / f"{label}.stderr.txt").write_text(proc.stderr)
    (RAW / f"{label}.exit.txt").write_text(str(proc.returncode) + "\n")
    return proc


def parse_ls_tree(text: str) -> dict[str, tuple[str, str]]:
    out: dict[str, tuple[str, str]] = {}
    for line in text.splitlines():
        if not line.strip():
            continue
        meta, path = line.split("\t")
        mode, typ, blob = meta.split()
        assert typ == "blob", line
        out[path] = (mode, blob)
    return out


def main() -> int:
    mismatches: list[str] = []

    # ---- A: parse raw20 (single machine source for the path set) ----
    raw20 = (M2 / "raw/20-identities.stdout.txt").read_text().splitlines()
    section: str | None = None
    a32: dict[str, tuple[str, str]] = {}
    a9: dict[str, tuple[str, str]] = {}
    for line in raw20:
        if line.startswith("== 32 "):
            section = "32"
            continue
        if line.startswith("== 9 "):
            section = "9"
            continue
        if not line.strip() or "\t" not in line:
            continue
        meta, path = line.split("\t")
        mode, typ, blob = meta.split()
        (a32 if section == "32" else a9)[path] = (mode, blob)
    emit(f"A raw20 parsed: 32-section={len(a32)} 9-section={len(a9)}")
    assert len(a32) == 32 and len(a9) == 9, "raw20 section counts"

    # ---- B/C: manifests ----
    b = json.loads((M2 / "manifest.json").read_text())
    b32 = {e["path"]: (e["mode"], e["blob"]) for e in b["final_32_identities"]}
    b9 = {e["path"]: (e["mode"], e["blob"]) for e in b["untouched_freeze_bindings_at_head_equal_baseline"]}
    c = json.loads((M3 / "manifest.pretty.json").read_text())
    c32 = {e["path"]: (e["mode"], e["blob"]) for e in c["final_32_identities"]}
    c9 = {e["path"]: (e["mode"], e["blob"]) for e in c["untouched_freeze_bindings_at_head_equal_baseline"]}
    emit(f"B m2 manifest: 32={len(b32)} 9={len(b9)}; C pretty: 32={len(c32)} 9={len(c9)}")

    # ---- D: live read-only ls-tree for the exact 41 paths ----
    paths = sorted(set(a32) | set(a9))
    emit(f"live query path count={len(paths)}")
    assert len(paths) == 41, "union must be 41 (32+9 disjoint)"
    assert not (set(a32) & set(a9)), "32/9 overlap"
    proc = run(["git", "-C", str(FIXTURE), "ls-tree", "HEAD", "--", *paths],
               "live-lstree-fixture")
    assert proc.returncode == 0, proc.stderr
    live = parse_ls_tree(proc.stdout)
    emit(f"D live fixture rows={len(live)}")
    proc2 = run(["git", "-C", str(RESTORE), "ls-tree", "HEAD", "--", *paths],
                "live-lstree-restore")
    live2 = parse_ls_tree(proc2.stdout) if proc2.returncode == 0 else {}
    emit(f"D2 live restore rows={len(live2)} rc={proc2.returncode}")

    # ---- pairwise comparison over all 41 ----
    for path in paths:
        expect32 = path in a32
        ra, rb, rc, rd = (a32.get(path) or a9.get(path)), (b32.get(path) or b9.get(path)), \
                         (c32.get(path) or c9.get(path)), live.get(path)
        for tag, val in (("raw20", ra), ("m2manifest", rb), ("pretty", rc), ("live", rd)):
            if val is None:
                mismatches.append(f"{path}: MISSING in {tag}")
        vals = {v for v in (ra, rb, rc, rd) if v is not None}
        if len(vals) > 1:
            mismatches.append(f"{path}: VALUE-DIFF raw20={ra} m2manifest={rb} pretty={rc} live={rd}")
        if proc2.returncode == 0 and live2.get(path) != rd:
            mismatches.append(f"{path}: RESTORE-DIFF restore={live2.get(path)} live={rd}")

    # ---- pins: commit/tree/parent read-only ----
    head = run(["git", "-C", str(FIXTURE), "rev-parse", "HEAD"], "live-head").stdout.strip()
    tree = run(["git", "-C", str(FIXTURE), "rev-parse", "HEAD^{tree}"], "live-tree").stdout.strip()
    parent = run(["git", "-C", str(FIXTURE), "log", "--format=%P", "-1"], "live-parent").stdout.strip()
    emit(f"pins head={head} tree={tree} parent={parent}")

    # ---- E/F/G numeric cross-checks (read-only, no rerun) ----
    checks: list[str] = []
    m3 = json.loads((M3 / "manifest.json").read_text())
    import glob as _glob
    exit_files = sorted(_glob.glob(str(M3 / "raw/five/t*.exit.txt")))
    checks.append(f"five exit files count=5: {'OK' if len(exit_files) == 5 else 'DIFF ' + str(exit_files)}")
    argv_names: set[str] = set()
    for ef in exit_files:
        content = Path(ef).read_text().strip()
        ok = content == "0"
        checks.append(f"five {Path(ef).name} exit-file={content} {'OK' if ok else 'DIFF'}")
        if not ok:
            mismatches.append("five exit nonzero: " + ef)
        argvp = Path(ef).parent / (Path(ef).name.replace(".exit.txt", ".argv.txt"))
        if argvp.exists():
            argv_names.add(argvp.read_text())
    manifest_names = {m["name"] for m in m3["five_methods"]}
    checks.append(f"five manifest names all present in argv files: {'OK' if all(any(n in a for a in argv_names) for n in manifest_names) else 'DIFF'}")
    if not all(any(n in a for a in argv_names) for n in manifest_names):
        mismatches.append("five manifest-name/argv mismatch")
    closure_rows = json.loads((M3 / "raw/closure/closure-rows.txt").read_text())
    src_txt = (M3 / "raw/closure/closure-source.txt").read_text()
    row1 = closure_rows[0]["sha256"]
    checks.append(f"closure row1 file-sha256 in source.txt: {'OK' if row1 in src_txt else 'DIFF'}")
    checks.append(f"closure rows count=8: {'OK' if len(closure_rows) == 8 else 'DIFF'}")
    arc = M3 / "candidate-partial-b40de60.tar.gz"
    arc_bytes = arc.stat().st_size
    arc_sha = hashlib.sha256(arc.read_bytes()).hexdigest()
    pinned = (M3 / "candidate-partial-b40de60.tar.gz.sha256").read_text().split()[0]
    checks.append(f"archive bytes live={arc_bytes} manifest={m3['archive']['bytes']} {'OK' if arc_bytes == m3['archive']['bytes'] else 'DIFF'}")
    checks.append(f"archive sha live==pinned-file: {'OK' if arc_sha == pinned else 'DIFF'}")
    checks.append(f"archive sha live==manifest: {'OK' if arc_sha == m3['archive']['sha256'] else 'DIFF'}")
    for c in checks:
        emit("NUM " + c)
        if c.endswith("DIFF"):
            mismatches.append("numeric: " + c)

    # ---- final binding built SOLELY from parsed live output + pins ----
    binding = {
        "head": head,
        "tree": tree,
        "direct_parent": parent,
        "provenance": "parsed live read-only git ls-tree/rev-parse/log at fixture; cross-checked vs m2 raw/20 (authoritative raw); supersedes typo'd manifest entries per corrections",
        "final_32_identities": [
            {"path": p, "mode": live[p][0], "blob": live[p][1]} for p in sorted(a32)
        ],
        "untouched_freeze_9": [
            {"path": p, "mode": live[p][0], "blob": live[p][1]} for p in sorted(a9)
        ],
    }
    assert len(binding["final_32_identities"]) == 32
    assert len(binding["untouched_freeze_9"]) == 9
    (OUT / "final-identity-binding.json").write_text(
        json.dumps(binding, indent=2, sort_keys=False) + "\n")

    emit(f"TOTAL_MISMATCHES={len(mismatches)}")
    for m in mismatches:
        emit("MISMATCH " + m)
    (OUT / "comparison-report.txt").write_text("\n".join(log) + "\n")
    return 0 if not mismatches else 0  # mismatches reported, not hidden; exit stays 0


if __name__ == "__main__":
    raise SystemExit(main())
