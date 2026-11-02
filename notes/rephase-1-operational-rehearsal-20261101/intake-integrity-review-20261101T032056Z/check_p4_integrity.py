"""P4 narrow DATA confirmation (10 files) + overlay + X FILE-ref + packages.

Scope: authorized local intake bytes only:
  P4 intake-20261101T023147Z-p4-20261101T031826Z (10 GETs)
  P3 bodies/DATA for p3a02-07 (fixed metadata + preserved zeros)
  P2 DATA.p2b02 / DATA.p2b21 (discovery accepted raw_refs + x_source_intake FILE refs)
  P2 architectures DATA.p2b13 / DATA.p2b29 (packages 7/9)
  P3 DATA.p3a51 / DATA.p3a59 (X result raws)
  P4 supersede-mapping.md / README.md (read as text, no edit)
No network, no git, no project runtime/import, no source edits.
Stdlib only: hashlib/json/base64/pathlib (+sys). No assert.
"""
import base64
import hashlib
import json
import sys
from pathlib import Path

R = Path("notes/rephase-1-operational-rehearsal-20261101")
P2 = R / "intake-20261101T023147Z-p2-20261101T024051Z"
P3 = R / "intake-20261101T023147Z-p3-20261101T025459Z"
P4 = R / "intake-20261101T023147Z-p4-20261101T031826Z"
W34 = "774dd39a951c9ac3818e83dfffd4c7666efb0a20"
SPR = "c8d0ecc1c9566a2303ad3b4c42635d4b672650e4"

errors = []
warnings = []
verified = []


def sh256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def blob1(b: bytes) -> str:
    h = hashlib.sha1()
    h.update(b"blob " + str(len(b)).encode("ascii") + b"\x00" + b)
    return h.hexdigest()


def b64strict(s: str) -> bytes:
    if not isinstance(s, str):
        raise ValueError("content not str")
    return base64.b64decode("".join(s.split()), validate=True)


def read(p: Path):
    return p.read_text()


def check_capture(gid: str):
    d = {}
    for suf in ["exit.txt", "headers.txt", "stderr.txt", "ref.txt", "url.txt"]:
        pp = P4 / (gid + "." + suf)
        d[suf] = pp.read_bytes() if pp.exists() else None
    if d["exit.txt"] is not None and d["exit.txt"].decode().strip() != "0":
        errors.append(f"{gid}: exit != 0")
    if d["headers.txt"] is not None and "200" not in d["headers.txt"].decode("utf-8", "replace"):
        errors.append(f"{gid}: headers missing 200")
    if d["stderr.txt"] is not None and len(d["stderr.txt"]) != 0:
        errors.append(f"{gid}: stderr non-empty")
    return d


def main():
    man = json.loads((P4 / "manifest.json").read_text())
    results = man.get("results", [])
    if len(results) != 10:
        errors.append(f"P4 manifest expected 10 results, got {len(results)}")
    # map gid -> manifest entry
    m = {r.get("gid"): r for r in results}
    # ---- 1. six blob payloads ----
    six = [
        ("p4a02", "p3a02", "sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/flashinfer-ai__flashinfer.json"),
        ("p4a03", "p3a03", "sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/ggml-org__llama.cpp.json"),
        ("p4a04", "p3a04", "sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/huggingface__transformers.json"),
        ("p4a05", "p3a05", "sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/nvidia__tensorrt-llm.json"),
        ("p4a06", "p3a06", "sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/sgl-project__sglang.json"),
        ("p4a07", "p3a07", "sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/vllm-project__vllm.json"),
    ]
    # load discovery accepted for content-sha cross-check
    disc = json.loads((P2 / "DATA.p2b02.discovery-accepted-v2.json").read_text())
    disc_refs = {}
    for rec in disc.get("records", []):
        for rr in rec.get("raw_refs", []):
            disc_refs[rr.get("path")] = (rr.get("sha256"), rr.get("byte_count"))
    for p4gid, p3gid, repo_path in six:
        cap = check_capture(p4gid)
        me = m.get(p4gid)
        if me is None:
            errors.append(f"{p4gid}: missing in manifest")
            continue
        try:
            body = json.loads((P4 / (p4gid + ".body.json")).read_text())
        except Exception as e:
            errors.append(f"{p4gid}: body json fail {e}")
            continue
        # blob API: sha/size/content/base64, no path
        bsha = body.get("sha")
        bsize = body.get("size")
        benc = body.get("encoding")
        bcon = body.get("content")
        if bsha != me.get("reported_blob_sha"):
            errors.append(f"{p4gid}: body sha != manifest")
        if bsize != me.get("reported_size"):
            errors.append(f"{p4gid}: body size != manifest")
        if benc != "base64":
            errors.append(f"{p4gid}: encoding {benc} != base64")
            continue
        try:
            raw = b64strict(bcon)
        except Exception as e:
            errors.append(f"{p4gid}: b64 fail {e}")
            continue
        if len(raw) != bsize:
            errors.append(f"{p4gid}: decoded len != size")
        if blob1(raw) != bsha:
            errors.append(f"{p4gid}: blob1 mismatch")
        dfs = me.get("data_files", [])
        if len(dfs) != 1:
            errors.append(f"{p4gid}: expected 1 data_file")
            continue
        df = dfs[0]
        dp = P4 / df.get("local")
        if not dp.exists():
            errors.append(f"{p4gid}: DATA missing")
            continue
        data = dp.read_bytes()
        if data != raw:
            errors.append(f"{p4gid}: DATA != decoded")
        if len(data) != df.get("bytes"):
            errors.append(f"{p4gid}: DATA len != manifest")
        if sh256(data) != df.get("sha256"):
            errors.append(f"{p4gid}: DATA sha256 != manifest")
        # vs P3 fixed metadata
        try:
            p3body = json.loads((P3 / (p3gid + ".body.json")).read_text())
        except Exception as e:
            errors.append(f"{p4gid}: P3 body load fail {e}")
            continue
        if p3body.get("sha") != bsha:
            errors.append(f"{p4gid}: P3 body sha {p3body.get('sha')} != P4 body sha {bsha}")
        if p3body.get("size") != bsize:
            errors.append(f"{p4gid}: P3 size != P4 size")
        if p3body.get("encoding") != "none" or p3body.get("content") != "":
            errors.append(f"{p4gid}: P3 body not metadata-only as expected")
        # P3 zero preserved unavailable
        p3df_local = None
        # find P3 manifest entry
        p3man = json.loads((P3 / "manifest.json").read_text())
        for r3 in p3man.get("results", []):
            if r3.get("gid") == p3gid:
                p3df_local = r3.get("data_files", [{}])[0].get("local")
                break
        if p3df_local is None:
            errors.append(f"{p4gid}: P3 manifest entry missing")
        else:
            zp = P3 / p3df_local
            if not zp.exists():
                errors.append(f"{p4gid}: P3 zero DATA missing (should be preserved)")
            else:
                zb = zp.read_bytes()
                if len(zb) != 0 or sh256(zb) != "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855":
                    errors.append(f"{p4gid}: P3 zero DATA altered (must stay 0B empty-sha)")
        # vs discovery accepted FILE ref (content sha256 + byte_count)
        want = disc_refs.get(repo_path)
        if want is None:
            errors.append(f"{p4gid}: no discovery raw_ref for {repo_path}")
        else:
            want_sha, want_bytes = want
            if want_sha != sh256(data):
                errors.append(f"{p4gid}: discovery want {want_sha} != P4 DATA {sh256(data)}")
            if want_bytes != len(data):
                errors.append(f"{p4gid}: discovery bytes {want_bytes} != {len(data)}")
            verified.append({"gid": p4gid, "repo_path": repo_path, "ref": W34, "blob_sha1": bsha, "size": len(data), "content_sha256": sh256(data), "discovery_sha256": want_sha, "overlay": "P3 zero UNAVAILABLE, P4 authoritative"})
    # ---- 2. X manifests + tasks ----
    # load P2 discovery x refs
    disc_w = json.loads((P2 / "DATA.p2b02.discovery-accepted-v2.json").read_text()).get("x_source_intake")
    disc_s = json.loads((P2 / "DATA.p2b21.discovery-accepted-v2.json").read_text()).get("x_source_intake")
    for gid, exp_ref, exp_path in [("p4x01", W34, "sources/2026-W34/external/x/x-source-intake-v2.json"), ("p4x02", SPR, "sources/SP-efficient-llm-2026/external/x/x-source-intake-v2.json")]:
        cap = check_capture(gid)
        me = m.get(gid)
        try:
            body = json.loads((P4 / (gid + ".body.json")).read_text())
        except Exception as e:
            errors.append(f"{gid}: body fail {e}")
            continue
        if body.get("path") != exp_path:
            errors.append(f"{gid}: body path mismatch")
        if body.get("path") != me.get("repo_path"):
            errors.append(f"{gid}: manifest repo_path mismatch body")
        if me.get("ref") != exp_ref:
            errors.append(f"{gid}: ref mismatch")
        if body.get("sha") != me.get("reported_blob_sha"):
            errors.append(f"{gid}: blob sha mismatch manifest")
        if body.get("size") != me.get("reported_size"):
            errors.append(f"{gid}: size mismatch manifest")
        if body.get("encoding") != "base64":
            errors.append(f"{gid}: encoding not base64")
            continue
        try:
            raw = b64strict(body.get("content", ""))
        except Exception as e:
            errors.append(f"{gid}: b64 fail {e}")
            continue
        if len(raw) != body.get("size"):
            errors.append(f"{gid}: decoded len != size")
        if blob1(raw) != body.get("sha"):
            errors.append(f"{gid}: blob1 mismatch")
        dfs = me.get("data_files", [])
        dp = P4 / dfs[0].get("local")
        data = dp.read_bytes()
        if data != raw:
            errors.append(f"{gid}: DATA != raw")
        if sh256(data) != dfs[0].get("sha256"):
            errors.append(f"{gid}: DATA sha256 mismatch")
        # vs discovery FILE ref (content sha256, NOT blob sha1, NOT semantic digest)
        exp_disc = disc_w if gid == "p4x01" else disc_s
        if exp_disc.get("path") != exp_path:
            errors.append(f"{gid}: discovery path mismatch")
        if exp_disc.get("sha256") != sh256(data):
            errors.append(f"{gid}: discovery content-sha {exp_disc.get('sha256')} != DATA {sh256(data)}")
        else:
            verified.append({"gid": gid, "repo_path": exp_path, "ref": exp_ref, "blob_sha1": body.get("sha"), "size": len(data), "content_sha256": sh256(data), "note": "blob-sha1 vs content-sha256 are different functions for same bytes; both valid; X manifest has no SELF digest field"})
        # url contains ref
        url = (P4 / (gid + ".url.txt")).read_text() if (P4 / (gid + ".url.txt")).exists() else ""
        if exp_ref not in url:
            errors.append(f"{gid}: url missing ref")
    # tasks
    for gid, exp_ref, exp_path in [("p4x03", W34, "sources/2026-W34/external/x/weekly-x-2026-W34-r2/grok-task.md"), ("p4x04", SPR, "sources/SP-efficient-llm-2026/external/x/efficient-llm-reception-pass-01/grok-task.md")]:
        cap = check_capture(gid)
        me = m.get(gid)
        try:
            body = json.loads((P4 / (gid + ".body.json")).read_text())
        except Exception as e:
            errors.append(f"{gid}: body fail {e}")
            continue
        if body.get("path") != exp_path or me.get("repo_path") != exp_path or me.get("ref") != exp_ref:
            errors.append(f"{gid}: path/ref mismatch")
        if body.get("sha") != me.get("reported_blob_sha") or body.get("size") != me.get("reported_size"):
            errors.append(f"{gid}: blob/size mismatch manifest")
        try:
            raw = b64strict(body.get("content", ""))
        except Exception as e:
            errors.append(f"{gid}: b64 fail {e}")
            continue
        if len(raw) != body.get("size") or blob1(raw) != body.get("sha"):
            errors.append(f"{gid}: decoded/blob mismatch")
            continue
        dp = P4 / me.get("data_files", [{}])[0].get("local")
        data = dp.read_bytes()
        if data != raw or sh256(data) != me.get("data_files", [{}])[0].get("sha256"):
            errors.append(f"{gid}: DATA mismatch")
        else:
            verified.append({"gid": gid, "repo_path": exp_path, "ref": exp_ref, "blob_sha1": body.get("sha"), "size": len(data), "content_sha256": sh256(data)})
    # X manifest internal task/result refs
    try:
        wx = json.loads((P4 / "DATA.p4x01.x-source-intake-v2.json").read_text())
        sx = json.loads((P4 / "DATA.p4x02.x-source-intake-v2.json").read_text())
    except Exception as e:
        errors.append(f"X DATA json fail {e}")
        wx = sx = None
    if wx is not None:
        t = wx["runs"][0]["task"]
        rraw = wx["runs"][0]["result"]["raw"]
        # task vs p4x03
        p4t = (P4 / "DATA.p4x03.grok-task.md").read_bytes()
        if t.get("path") != "sources/2026-W34/external/x/weekly-x-2026-W34-r2/grok-task.md" or t.get("sha256") != sh256(p4t):
            errors.append("W34 X task ref != p4x03 bytes")
        else:
            verified.append({"link": "W34 X task ref == p4x03", "path": t.get("path"), "content_sha256": t.get("sha256")})
        # result vs P3 p3a51
        p3r = (P3 / "DATA.p3a51.grok-x-result.corrected.md").read_bytes()
        if rraw.get("path") != "sources/2026-W34/external/x/weekly-x-2026-W34-r2/raw/grok-x-result.corrected.md" or rraw.get("sha256") != sh256(p3r) or rraw.get("byte_count") != len(p3r):
            errors.append("W34 X result ref != P3 p3a51 bytes")
        else:
            verified.append({"link": "W34 X result ref == P3 p3a51", "path": rraw.get("path"), "content_sha256": rraw.get("sha256"), "bytes": len(p3r)})
    if sx is not None:
        t = sx["runs"][0].get("task") or sx["runs"][0].get("task_file") or {}
        # SP task location: runs[0].task
        try:
            t2 = sx["runs"][0]["task"]
        except Exception:
            t2 = {}
        p4t = (P4 / "DATA.p4x04.grok-task.md").read_bytes()
        if t2.get("path") != "sources/SP-efficient-llm-2026/external/x/efficient-llm-reception-pass-01/grok-task.md" or t2.get("sha256") != sh256(p4t):
            errors.append("SP X task ref != p4x04 bytes")
        else:
            verified.append({"link": "SP X task ref == p4x04", "path": t2.get("path"), "content_sha256": t2.get("sha256")})
        rraw = sx["runs"][0]["result"]["raw"]
        p3r = (P3 / "DATA.p3a59.x-reception-result-r3.md").read_bytes()
        if rraw.get("path") != "sources/SP-efficient-llm-2026/external/x/efficient-llm-reception-pass-01/raw/x-reception-result-r3.md" or rraw.get("sha256") != sh256(p3r) or rraw.get("byte_count") != len(p3r):
            errors.append("SP X result ref != P3 p3a59 bytes")
        else:
            verified.append({"link": "SP X result ref == P3 p3a59", "path": rraw.get("path"), "content_sha256": rraw.get("sha256"), "bytes": len(p3r)})
    # ---- 3. search captured DATA for explicit replacement records / retained X bytes ----
    # Search all P1/P2/P3/P4 DATA.*.json text for old DRAFT hashes and X hashes (no new fetch).
    old_hashes = [
        "08c0e35848b93e8e27ae6937ea255278dbe760eec96dc32af6f295eed1f0f18d",
        "f99c3b9353e978aec009871875a0df77d30b7be387b2c90ede15ac44aacbd693",
        "417e49ac28b9e1c8babeac181fb541618a8f23935e61533ac79e5d21bce678a5",
        "c60513eb08a27d8339909dea75d48ea1ddcd6fde439106c26c8d29465d10c10f",
        "b09ab3516afaadb5e0f64e21515d2e71dd43cbb926c657e40d48b939dc54b44c",
        "c4ae1c38c09477dfd003336cf820f9e23267c864861b2f669e65257d6a222",
        "76191e9b5f24d6950ce3e80a4f3e19cf79dc4dfc2dee552948b8ce23956f787e",
    ]
    hits = []
    search_roots = [P2, P3, P4]
    for rt in search_roots:
        for dp in sorted(rt.glob("DATA.*.json")):
            try:
                txt = dp.read_text()
            except Exception:
                continue
            for h in old_hashes:
                if h in txt:
                    hits.append({"file": f"{rt.name}/{dp.name}", "hash": h})
                    break
    # retained X bytes: look for files containing W34/SP X content hashes
    x_hashes = ["702881aa75cc09ff3e65f52220e47076c8f67a8c97a36d4e4aea87e41f5a98b2", "3465dc4f4d9d3bce73c33cb16820aa771816fa64a8de850336ef56c46d8275b0"]
    x_hits = []
    for rt in [P2, P3, P4]:
        for dp in sorted(rt.glob("DATA.*.*")):
            if dp.suffix not in (".json", ".md"):
                continue
            try:
                txt = dp.read_text()
            except Exception:
                continue
            for h in x_hashes:
                if h in txt:
                    x_hits.append({"file": f"{rt.name}/{dp.name}", "hash": h})
                    break
    # ---- 4. packages 7/9 ----
    try:
        wa = json.loads((P2 / "DATA.p2b13.architecture-v2.json").read_text())
        sa = json.loads((P2 / "DATA.p2b29.architecture-v2.json").read_text())
        w_pkgs = [p.get("package_id") for p in wa.get("packages", [])]
        s_pkgs = [p.get("package_id") for p in sa.get("packages", [])]
    except Exception as e:
        errors.append(f"arch load fail {e}")
        w_pkgs = s_pkgs = []
    out = {
        "p4_count": len(results),
        "verified_links": verified,
        "replacement_record_hits": hits,
        "x_hash_hits": x_hits,
        "w34_packages": w_pkgs,
        "sp_packages": s_pkgs,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(out, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
