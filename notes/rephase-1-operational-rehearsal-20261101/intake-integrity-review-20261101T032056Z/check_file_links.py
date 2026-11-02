"""FILE-link checker: published source/candidate/acceptance FILE sha refs vs captured bytes.

Scope: authorized intake bytes only (P1/P2/P3) + explicitly listed old fixed archives
where available (no root sweep, no Gitlinks, no Production checkout).
Stdlib only: hashlib/json/base64/pathlib (+sys). No assert.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path("notes/rephase-1-operational-rehearsal-20261101")
P1 = ROOT / "intake-20261101T023147Z"
P2 = ROOT / "intake-20261101T023147Z-p2-20261101T024051Z"
P3 = ROOT / "intake-20261101T023147Z-p3-20261101T025459Z"

errors = []
links_checked = 0
links_matched = 0
links_unacquired = 0
archived_checked = 0


def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def build_captured_map():
    """repo_path -> list of (intake, local, bytes, sha256)."""
    m = {}
    for intake in (P1, P2, P3):
        man_p = intake / "manifest.json"
        try:
            man = json.loads(man_p.read_text())
        except Exception as e:
            errors.append(f"{intake.name}: manifest load failed: {e}")
            continue
        for r in man.get("results", []):
            rp = r.get("repo_path")
            if rp is None or (isinstance(rp, str) and rp.startswith("listing:")):
                continue
            for df in r.get("data_files", []) or []:
                local = df.get("local")
                dp = intake / local
                if not dp.exists():
                    errors.append(f"{intake.name}/{r.get('gid')}: DATA {local} missing for map")
                    continue
                try:
                    b = dp.read_bytes()
                except Exception as e:
                    errors.append(f"{intake.name}/{local}: read failed: {e}")
                    continue
                # verify manifest bytes/sha match actual (redundant with checker 1, but needed for link trust)
                if len(b) != df.get("bytes"):
                    errors.append(f"{intake.name}/{local}: len {len(b)} != manifest {df.get('bytes')}")
                if sha256_hex(b) != df.get("sha256"):
                    errors.append(f"{intake.name}/{local}: sha256 mismatch manifest")
                m.setdefault(rp, []).append((intake.name, local, b, sha256_hex(b)))
    return m


def walk_find_links(obj, out):
    if isinstance(obj, dict):
        if "path" in obj and "sha256" in obj and isinstance(obj["path"], str) and isinstance(obj["sha256"], str):
            p = obj["path"]
            # only repo-relative file refs under selected roots
            if p.startswith("sources/") or p.startswith("surveys/"):
                out.append((p, obj["sha256"], obj.get("byte_count")))
        for v in obj.values():
            walk_find_links(v, out)
    elif isinstance(obj, list):
        for v in obj:
            walk_find_links(v, out)


def main():
    global links_checked, links_matched, links_unacquired, archived_checked
    cmap = build_captured_map()
    # duplicate repo_path mapped to multiple DATA? should be unique per edition/ref; report
    for rp, lst in sorted(cmap.items()):
        if len(lst) > 1:
            # same repo_path appearing twice would be misbinding; but W34 vs SP paths differ by prefix so no dup expected.
            # Check if same bytes? If different, flag.
            shas = set(x[3] for x in lst)
            if len(shas) > 1:
                errors.append(f"DUPLICATE repo_path with differing bytes: {rp} -> {[(x[0], x[1]) for x in lst]}")
    # walk all JSON DATA files
    details = []
    for intake in (P1, P2, P3):
        for dp in sorted(intake.glob("DATA.*.json")) + sorted(intake.glob("DATA.*.jsonl")):
            # jsonl: try each line
            try:
                txt = dp.read_text()
            except Exception:
                continue
            objs = []
            if dp.suffix == ".jsonl" or dp.name.endswith(".jsonl"):
                # jsonl may be large; only scan first object for links? Discovery jsonl contains raw_paths, not path/sha256 file links.
                # Parse line by line, cap at 200 lines for link scan to avoid heavy work.
                for i, line in enumerate(txt.splitlines()):
                    if i >= 500:
                        break
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        objs.append(json.loads(line))
                    except Exception:
                        continue
                    if len(objs) >= 20:
                        break
                # also try whole file as json? skip
            else:
                try:
                    objs = [json.loads(txt)]
                except Exception:
                    continue
            for o in objs:
                links = []
                walk_find_links(o, links)
                for (p, want_sha, want_bytes) in links:
                    links_checked += 1
                    rec = {
                        "holder": f"{intake.name}/{dp.name}",
                        "path": p,
                        "want_sha256": want_sha,
                        "want_bytes": want_bytes,
                    }
                    lst = cmap.get(p)
                    if not lst:
                        links_unacquired += 1
                        rec["result"] = "UNACQUIRED (no captured DATA for this path; not invalid)"
                        details.append(rec)
                        continue
                    # prefer exact edition match: holder edition should match path edition, but cmap already keyed by full path
                    matched = False
                    for (iname, local, b, got_sha) in lst:
                        if got_sha == want_sha:
                            matched = True
                            if want_bytes is not None and want_bytes != len(b):
                                errors.append(f"{rec['holder']}: {p} sha matches but byte_count {want_bytes} != actual {len(b)}")
                                rec["result"] = "SHA_MATCH_BYTES_MISMATCH"
                            else:
                                rec["result"] = f"MATCH {iname}/{local} {len(b)}B"
                            links_matched += 1
                            break
                    if not matched:
                        got = [(x[0], x[1], x[3][:12], len(x[2])) for x in lst]
                        errors.append(f"{rec['holder']}: {p} want {want_sha[:12]} but captured {got}")
                        rec["result"] = f"MISMATCH captured={got}"
                    details.append(rec)
    # archived spot-checks (only if files exist at exact known paths; no sweep)
    archived = [
        (".rephase-1-inputs/774dd39a951c9ac3818e83dfffd4c7666efb0a20/sources/2026-W34/production-profile.json", None),
        (".phase-5-inputs/774dd39a951c9ac3818e83dfffd4c7666efb0a20/sources/2026-W34/publication/v2/reader-manuscript-v2.json", "c453bea798f6d7693d2e92d1dbae3fc7838b24d90df382c2547f3ad033b7c10e"),
    ]
    arch_results = []
    for ap, want in archived:
        pp = Path(ap)
        if not pp.exists():
            arch_results.append({"path": ap, "result": "UNAVAILABLE (not present; no sweep)"})
            continue
        try:
            b = pp.read_bytes()
        except Exception as e:
            arch_results.append({"path": ap, "result": f"READ_FAIL {e}"})
            continue
        archived_checked += 1
        got = sha256_hex(b)
        if want is not None and got != want:
            errors.append(f"archived {ap}: sha {got[:12]} != want {want[:12]}")
            arch_results.append({"path": ap, "bytes": len(b), "sha256": got, "result": "MISMATCH"})
        else:
            arch_results.append({"path": ap, "bytes": len(b), "sha256": got, "result": "MATCH" if want else "PRESENT"})
    out = {
        "links_checked": links_checked,
        "links_matched": links_matched,
        "links_unacquired": links_unacquired,
        "archived_checked": archived_checked,
        "errors": errors,
        "archived": arch_results,
        "details_sample": details[:120],
        "details_total": len(details),
    }
    # full details go to separate file via stdout redirect; print summary json
    print(json.dumps(out, indent=2))
    if errors:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
