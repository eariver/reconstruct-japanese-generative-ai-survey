"""Fresh independent DATA-integrity checker (P1/P2/P3 only).

Scope: authorized local intake bytes only:
  notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z
  notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p2-20261101T024051Z
  notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p3-20261101T025459Z
No network, no git, no project runtime/import, no source/manifest edits.
Stdlib only: hashlib/json/base64/pathlib (+sys for exit). No assert (fail-closed explicit checks).
"""
import base64
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path("notes/rephase-1-operational-rehearsal-20261101")
P1 = ROOT / "intake-20261101T023147Z"
P2 = ROOT / "intake-20261101T023147Z-p2-20261101T024051Z"
P3 = ROOT / "intake-20261101T023147Z-p3-20261101T025459Z"
W34_REF = "774dd39a951c9ac3818e83dfffd4c7666efb0a20"
SP_REF = "c8d0ecc1c9566a2303ad3b4c42635d4b672650e4"
EMPTY_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
EMPTY_BLOB = "e69de29bb2d1d6434b8b29e777ad8c2e48b3f0ce"


def b64decode_strict(s: str) -> bytes:
    # GitHub contents/blob API inserts LF every 60 chars; strip all whitespace then validate.
    # Fail-closed: validate=True on cleaned string, no silent skip of non-base64 chars.
    if not isinstance(s, str):
        raise ValueError("content not str")
    cleaned = "".join(s.split())
    return base64.b64decode(cleaned, validate=True)

errors = []
needs_repair = []
warnings = []
checked_files = 0
checked_listings = 0
checked_blobs = 0


def fail(msg):
    errors.append(msg)


def git_blob_sha(data: bytes) -> str:
    h = hashlib.sha1()
    h.update(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data)
    return h.hexdigest()


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_text(p: Path):
    try:
        return p.read_text()
    except Exception as e:
        return None


def check_capture_indicators(intake: Path, gid: str):
    """Check exit/headers/stderr capture files where present."""
    out = {}
    for suffix in ["exit.txt", "headers.txt", "stderr.txt", "ref.txt", "url.txt"]:
        p = intake / (gid + "." + suffix)
        if p.exists():
            try:
                out[suffix] = p.read_bytes()
            except Exception as e:
                fail(f"{intake.name}/{gid}: cannot read {suffix}: {e}")
                out[suffix] = None
        else:
            out[suffix] = None
    # exit must be 0
    if out.get("exit.txt") is not None:
        txt = out["exit.txt"].decode("utf-8", "replace").strip()
        if txt != "0":
            fail(f"{intake.name}/{gid}: exit.txt={txt!r} != 0")
            out["exit_ok"] = False
        else:
            out["exit_ok"] = True
    # headers should contain 200
    if out.get("headers.txt") is not None:
        try:
            ht = out["headers.txt"].decode("utf-8", "replace")
        except Exception:
            ht = ""
        if "200" not in ht:
            fail(f"{intake.name}/{gid}: headers missing 200: {ht[:200]!r}")
            out["http_ok"] = False
        else:
            out["http_ok"] = True
    # stderr should be empty
    if out.get("stderr.txt") is not None:
        if len(out["stderr.txt"]) != 0:
            fail(f"{intake.name}/{gid}: stderr non-empty {len(out['stderr.txt'])}B: {out['stderr.txt'][:300]!r}")
    return out


def edition_for_path(repo_path):
    if repo_path is None:
        return None
    if repo_path.startswith("sources/2026-W34") or repo_path.startswith("surveys/weekly/2026-W34"):
        return "W34"
    if repo_path.startswith("sources/SP-efficient-llm-2026") or repo_path.startswith("surveys/special/efficient-llm-2026"):
        return "SP"
    return "OTHER"


def check_p1():
    global checked_files, checked_listings
    man = json.loads((P1 / "manifest.json").read_text())
    results = man.get("results", [])
    if len(results) != 6:
        fail(f"P1: expected 6 results, got {len(results)}")
    for r in results:
        api_path = r.get("api_path", "")
        data_file = r.get("data_file")
        # derive gid from api_path? P1 uses get01..get06 mapping via manifest order is fragile;
        # instead map data_file/label to getNN via label files: read getNN.label.txt
        # We enumerate getNN directly.
    # enumerate get01..get06
    for i in range(1, 7):
        gid = f"get{i:02d}"
        body_p = P1 / (gid + ".body.json")
        if not body_p.exists():
            fail(f"P1/{gid}: missing body.json")
            continue
        cap = check_capture_indicators(P1, gid)
        ref_txt = read_text(P1 / (gid + ".ref.txt"))
        if ref_txt is not None:
            ref_txt = ref_txt.strip()
        try:
            body = json.loads(body_p.read_text())
        except Exception as e:
            fail(f"P1/{gid}: body.json invalid JSON: {e}")
            continue
        if isinstance(body, list):
            checked_listings += 1
            # directory listing: no DATA expected; verify manifest has no data_file for this?
            # find manifest entry whose api_path contains listing path? get03/get06 are listings.
            if gid not in ("get03", "get06"):
                fail(f"P1/{gid}: unexpected listing body (expected file)")
            # record entries
            for e in body:
                if not isinstance(e, dict) or "path" not in e or "sha" not in e or "size" not in e:
                    fail(f"P1/{gid}: listing entry missing path/sha/size: {str(e)[:200]}")
            # verify ref is one of the two fixed refs
            if ref_txt not in (W34_REF, SP_REF):
                fail(f"P1/{gid}: listing ref {ref_txt!r} not fixed W34/SP")
            continue
        # file body
        checked_files += 1
        name = body.get("name")
        path = body.get("path")
        sha = body.get("sha")
        size = body.get("size")
        enc = body.get("encoding")
        content = body.get("content")
        if not isinstance(size, int):
            fail(f"P1/{gid}: size not int: {size!r}")
            continue
        if enc != "base64":
            # P1 should have no encoding none (all small files + listings)
            fail(f"P1/{gid}: unexpected encoding {enc!r} (expected base64 for files)")
            if enc == "none":
                needs_repair.append(f"P1/{gid} path={path} size={size} blob={sha} encoding=none empty-content -> NEEDS_REPAIR (no bytes)")
            continue
        if not isinstance(content, str) or len(content) == 0:
            fail(f"P1/{gid}: empty base64 content")
            continue
        try:
            raw = b64decode_strict(content)
        except Exception as e:
            fail(f"P1/{gid}: base64 decode failed: {e}")
            continue
        if len(raw) != size:
            fail(f"P1/{gid}: decoded len {len(raw)} != reported size {size}")
        gb = git_blob_sha(raw)
        if gb != sha:
            fail(f"P1/{gid}: git blob {gb} != reported sha {sha}")
        # find manifest entry matching this path
        matched = None
        for r in results:
            # api_path contains path
            if path in r.get("api_path", ""):
                matched = r
                break
        if matched is None:
            fail(f"P1/{gid}: no manifest result matches path {path}")
        else:
            if matched.get("blob_sha") != sha:
                fail(f"P1/{gid}: manifest blob_sha {matched.get('blob_sha')} != body sha {sha}")
            if str(matched.get("bytes")) != str(size) and matched.get("bytes") != size:
                fail(f"P1/{gid}: manifest bytes {matched.get('bytes')} != body size {size}")
            df = matched.get("data_file")
            if df:
                dp = P1 / df
                if not dp.exists():
                    fail(f"P1/{gid}: manifest data_file {df} missing on disk")
                else:
                    data = dp.read_bytes()
                    if len(data) != size:
                        fail(f"P1/{gid}: DATA {df} len {len(data)} != size {size}")
                    if git_blob_sha(data) != sha:
                        fail(f"P1/{gid}: DATA {df} blob mismatch")
                    if data != raw:
                        fail(f"P1/{gid}: DATA {df} bytes != decoded body bytes")
                    if sha256_hex(data) != matched.get("sha256"):
                        fail(f"P1/{gid}: DATA {df} sha256 mismatch manifest")
        # ref/edition check
        ed = edition_for_path(path)
        if ed == "W34" and ref_txt != W34_REF:
            fail(f"P1/{gid}: W34 path but ref {ref_txt!r} != W34_REF")
        if ed == "SP" and ref_txt != SP_REF:
            fail(f"P1/{gid}: SP path but ref {ref_txt!r} != SP_REF")
        # url check contains ref
        url_txt = read_text(P1 / (gid + ".url.txt"))
        if url_txt is not None and ref_txt is not None and ref_txt not in url_txt:
            # blob supplements have no ref; but P1 files should contain ref
            fail(f"P1/{gid}: url does not contain ref")


def check_intake_generic(intake: Path, tag: str):
    global checked_files, checked_listings, checked_blobs
    man = json.loads((intake / "manifest.json").read_text())
    results = man.get("results", [])
    # build blob supplement map: blob_sha -> decoded bytes (for P3 large, P2 large)
    blob_bytes = {}
    for r in results:
        gid = r.get("gid", "?")
        repo_path = r.get("repo_path")
        ref = r.get("ref", "")
        reported_size = r.get("reported_size")
        reported_blob = r.get("reported_blob_sha")
        data_files = r.get("data_files", [])
        body_p = intake / (gid + ".body.json")
        if not body_p.exists():
            fail(f"{tag}/{gid}: missing body.json")
            continue
        cap = check_capture_indicators(intake, gid)
        # ref file check
        ref_txt = read_text(intake / (gid + ".ref.txt"))
        if ref_txt is not None:
            ref_txt = ref_txt.strip()
            # manifest ref should match ref.txt unless blob-pinned
            if "blob-sha-pinned" in str(ref):
                pass
            else:
                if ref_txt != ref:
                    fail(f"{tag}/{gid}: ref.txt {ref_txt!r} != manifest ref {ref!r}")
        try:
            body = json.loads(body_p.read_text())
        except Exception as e:
            fail(f"{tag}/{gid}: body.json invalid JSON: {e}")
            continue
        # directory listing case: body is list
        if isinstance(body, list):
            checked_listings += 1
            if len(data_files) != 0:
                fail(f"{tag}/{gid}: listing body but manifest has {len(data_files)} data_files")
            if repo_path is not None and not str(repo_path).startswith("listing:"):
                fail(f"{tag}/{gid}: listing body but repo_path={repo_path!r} not listing:")
            # verify each entry has path/sha/size
            for e in body:
                if not isinstance(e, dict) or "path" not in e or "sha" not in e or "size" not in e:
                    fail(f"{tag}/{gid}: listing entry malformed: {str(e)[:200]}")
                    break
            # manifest reported_size/blob should be None for listings
            if reported_size is not None or reported_blob is not None:
                # P2 uses None for listings - enforce
                fail(f"{tag}/{gid}: listing should have null reported_size/blob, got {reported_size}/{reported_blob}")
            continue
        # body is dict
        if not isinstance(body, dict):
            fail(f"{tag}/{gid}: unexpected body type")
            continue
        # blob-API case: no path/name, has sha/size/content/encoding
        is_blob_api = ("path" not in body) and ("sha" in body) and ("content" in body)
        if is_blob_api:
            checked_blobs += 1
            sha = body.get("sha")
            size = body.get("size")
            enc = body.get("encoding")
            content = body.get("content")
            if sha != reported_blob:
                fail(f"{tag}/{gid}: blob body sha {sha} != manifest {reported_blob}")
            if size != reported_size:
                fail(f"{tag}/{gid}: blob body size {size} != manifest {reported_size}")
            if enc != "base64":
                fail(f"{tag}/{gid}: blob body encoding {enc!r} != base64")
                continue
            try:
                raw = b64decode_strict(content)
            except Exception as e:
                fail(f"{tag}/{gid}: blob base64 decode failed: {e}")
                continue
            if len(raw) != size:
                fail(f"{tag}/{gid}: blob decoded len {len(raw)} != size {size}")
            if git_blob_sha(raw) != sha:
                fail(f"{tag}/{gid}: blob git sha mismatch")
            blob_bytes[str(sha)] = raw
            # data_files: P2 blob supplements have 1 DATA, P3 have 0 (bytes folded into contents entry)
            for df in data_files:
                local = df.get("local")
                dp = intake / local
                if not dp.exists():
                    fail(f"{tag}/{gid}: blob DATA {local} missing")
                    continue
                checked_files += 1
                data = dp.read_bytes()
                if len(data) != df.get("bytes"):
                    fail(f"{tag}/{gid}: blob DATA {local} len {len(data)} != manifest {df.get('bytes')}")
                if len(data) != size:
                    fail(f"{tag}/{gid}: blob DATA {local} len != blob size")
                if sha256_hex(data) != df.get("sha256"):
                    fail(f"{tag}/{gid}: blob DATA {local} sha256 mismatch")
                if data != raw:
                    fail(f"{tag}/{gid}: blob DATA {local} != decoded blob bytes")
            continue
        # contents-API file case
        checked_files += 1
        name = body.get("name")
        path = body.get("path")
        sha = body.get("sha")
        size = body.get("size")
        enc = body.get("encoding")
        content = body.get("content")
        # manifest consistency
        if path != repo_path:
            fail(f"{tag}/{gid}: body path {path!r} != manifest repo_path {repo_path!r}")
        if sha != reported_blob:
            fail(f"{tag}/{gid}: body sha {sha} != manifest {reported_blob}")
        if size != reported_size:
            fail(f"{tag}/{gid}: body size {size} != manifest {reported_size}")
        # edition/ref check (skip blob-pinned)
        if "blob-sha-pinned" not in str(ref):
            ed = edition_for_path(path)
            if ed == "W34" and ref != W34_REF:
                fail(f"{tag}/{gid}: W34 path {path} but ref != W34_REF")
            if ed == "SP" and ref != SP_REF:
                fail(f"{tag}/{gid}: SP path {path} but ref != SP_REF")
            if ed == "OTHER":
                fail(f"{tag}/{gid}: path outside selected roots: {path!r}")
            # url should contain ref (for contents API)
            url_txt = read_text(intake / (gid + ".url.txt"))
            if url_txt is not None and ref not in url_txt:
                fail(f"{tag}/{gid}: url missing ref")
        if enc == "none":
            # metadata-only: content must be empty
            if content != "":
                fail(f"{tag}/{gid}: encoding none but content non-empty {len(str(content))}")
            # DATA handling: expect 0-byte DATA with empty sha256, unless supplemented
            if len(data_files) != 1:
                fail(f"{tag}/{gid}: encoding none expected 1 data_file entry, got {len(data_files)}")
                continue
            df = data_files[0]
            local = df.get("local")
            dp = intake / local
            if not dp.exists():
                fail(f"{tag}/{gid}: missing DATA {local}")
                continue
            data = dp.read_bytes()
            if len(data) == 0 and sha256_hex(data) == EMPTY_SHA256 and df.get("bytes") == 0 and df.get("sha256") == EMPTY_SHA256:
                # confirmed missing bytes, blob non-empty -> NEEDS_REPAIR
                if sha != EMPTY_BLOB and sha is not None and sha != "":
                    needs_repair.append(f"{tag}/{gid} path={path} ref={str(ref)[:12]} blob={sha} expected_size={size} actual_size=0 actual_sha={EMPTY_SHA256} indicator=encoding=none/empty-content (HTTP200 metadata-only, no blob supplement)")
                else:
                    warnings.append(f"{tag}/{gid}: empty file genuinely? blob empty too")
            else:
                # DATA has bytes despite encoding none -> must come from blob supplement; verify later
                # record for cross-check: store pending
                if len(data) != size:
                    fail(f"{tag}/{gid}: DATA len {len(data)} != reported size {size} (encoding none with bytes?)")
                if sha256_hex(data) != df.get("sha256"):
                    fail(f"{tag}/{gid}: DATA sha256 mismatch manifest")
                # stash for blob cross-check
                blob_bytes["PENDING:" + str(sha)] = data
        elif enc == "base64":
            if not isinstance(content, str) or len(content) == 0:
                fail(f"{tag}/{gid}: base64 empty content with size {size}")
                continue
            try:
                raw = b64decode_strict(content)
            except Exception as e:
                fail(f"{tag}/{gid}: base64 decode failed: {e}")
                continue
            if len(raw) != size:
                fail(f"{tag}/{gid}: decoded len {len(raw)} != size {size}")
            if git_blob_sha(raw) != sha:
                fail(f"{tag}/{gid}: git blob mismatch: computed {git_blob_sha(raw)[:12]} vs {str(sha)[:12]}")
            if len(data_files) != 1:
                fail(f"{tag}/{gid}: expected 1 data_file, got {len(data_files)}")
                continue
            df = data_files[0]
            local = df.get("local")
            dp = intake / local
            if not dp.exists():
                fail(f"{tag}/{gid}: missing DATA {local}")
                continue
            data = dp.read_bytes()
            if data != raw:
                fail(f"{tag}/{gid}: DATA {local} != decoded body bytes (len {len(data)} vs {len(raw)})")
            if len(data) != df.get("bytes"):
                fail(f"{tag}/{gid}: DATA len != manifest bytes")
            if sha256_hex(data) != df.get("sha256"):
                fail(f"{tag}/{gid}: DATA sha256 {sha256_hex(data)[:12]} != manifest {str(df.get('sha256'))[:12]}")
            # duplicate-basename proper lookup: local must start with DATA.<gid>.
            if not local.startswith("DATA." + gid + "."):
                fail(f"{tag}/{gid}: DATA local {local} does not start with DATA.{gid}. (basename collision risk)")
        else:
            fail(f"{tag}/{gid}: unknown encoding {enc!r}")
    return blob_bytes


def main():
    global checked_files, checked_listings, checked_blobs
    check_p1()
    p2_blobs = check_intake_generic(P2, "P2")
    p3_blobs = check_intake_generic(P3, "P3")
    # cross-check P3 large supplements: for each encoding-none with bytes, verify blob supplement exists with same sha
    # Re-scan P3 manifest for encoding-none entries that have bytes>0
    man3 = json.loads((P3 / "manifest.json").read_text())
    for r in man3.get("results", []):
        gid = r.get("gid", "")
        if not gid.startswith("p3a"):
            continue
        body_p = P3 / (gid + ".body.json")
        try:
            body = json.loads(body_p.read_text())
        except Exception:
            continue
        if isinstance(body, dict) and body.get("encoding") == "none":
            # already recorded as NEEDS_REPAIR if 0 bytes; if bytes>0, verify supplement
            dfs = r.get("data_files", [])
            if dfs and dfs[0].get("bytes", 0) > 0:
                sha = body.get("sha")
                # find blob supplement with same sha
                found = False
                for r2 in man3.get("results", []):
                    if r2.get("gid", "").startswith("p3b") and r2.get("reported_blob_sha") == sha:
                        found = True
                        # verify DATA equals blob decoded bytes
                        bbody_p = P3 / (r2.get("gid") + ".body.json")
                        try:
                            bbody = json.loads(bbody_p.read_text())
                            braw = b64decode_strict(bbody.get("content", ""))
                        except Exception as e:
                            fail(f"P3/{gid}: supplement {r2.get('gid')} decode failed: {e}")
                            continue
                        ddata = (P3 / dfs[0].get("local")).read_bytes()
                        if ddata != braw:
                            fail(f"P3/{gid}: DATA != supplement {r2.get('gid')} bytes")
                        if len(ddata) != bbody.get("size"):
                            fail(f"P3/{gid}: DATA len != supplement size")
                        break
                if not found:
                    fail(f"P3/{gid}: encoding none with bytes but no blob supplement found for sha {sha}")
    # summary
    summary = {
        "checked_files": checked_files,
        "checked_listings": checked_listings,
        "checked_blob_apis": checked_blobs,
        "errors": errors,
        "needs_repair": needs_repair,
        "warnings": warnings,
    }
    # write summary to stdout as JSON (captured separately) and return exit
    print(json.dumps(summary, indent=2))
    # fail-closed: non-zero if errors or needs_repair
    if errors or needs_repair:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
