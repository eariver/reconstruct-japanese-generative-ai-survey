"""Bounded Jev archive intake helper — single-run, no retries.
Authorized: 3 exact URLs, 1 CDX index each (20260901..20260921161000 UTC),
1 newest eligible exact-URL 200 text/html snapshot body each. Max 3+3.
All outputs under this packet intake dir. DATA only, no execution.
"""
import hashlib
import json
import os
import sys
import time
import urllib.parse
import urllib.request
import urllib.error
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
URLS = [
    "https://typesafe.ai/blog/introducing-system-one-models-and-jev",
    "https://docs.typesafe.ai/concepts/system-one",
    "https://docs.typesafe.ai/models",
]
FROM = "20260901"
TO = "20260921161000"  # 2026-09-21T16:10:00Z
CUTOFF = "20260921161000"
TIMEOUT = 30

class ChainRedirectHandler(urllib.request.HTTPRedirectHandler):
    def __init__(self):
        super().__init__()
        self.chain = []
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.chain.append({
            "code": code,
            "location": headers.get("Location"),
            "from": req.full_url,
            "to": newurl,
        })
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def one_get(url):
    """Single GET, no retry. Returns dict with status/headers/bytes/meta."""
    handler = ChainRedirectHandler()
    opener = urllib.request.build_opener(handler)
    opener.addheaders = [("User-Agent", "bounded-intake/1.0 (read-only archive lookup)")]
    utc = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
    t0 = time.time()
    try:
        req = urllib.request.Request(url, method="GET")
        with opener.open(req, timeout=TIMEOUT) as resp:
            body = resp.read()
            elapsed = time.time() - t0
            return {
                "request_url": url,
                "response_url": resp.geturl(),
                "status": resp.getcode(),
                "headers": dict(resp.getheaders()),
                "body": body,
                "utc": utc,
                "elapsed_s": elapsed,
                "redirect_chain": handler.chain,
                "error": None,
                "exit": 0,
            }
    except urllib.error.HTTPError as e:
        elapsed = time.time() - t0
        try:
            ebody = e.read()
        except Exception:
            ebody = b""
        hdrs = {}
        try:
            hdrs = dict(e.headers.items()) if e.headers else {}
        except Exception:
            hdrs = {}
        return {
            "request_url": url,
            "response_url": getattr(e, "url", url),
            "status": getattr(e, "code", None),
            "headers": hdrs,
            "body": ebody,
            "utc": utc,
            "elapsed_s": elapsed,
            "redirect_chain": handler.chain,
            "error": f"HTTPError {e}",
            "exit": 1,
        }
    except Exception as e:
        elapsed = time.time() - t0
        return {
            "request_url": url,
            "response_url": url,
            "status": None,
            "headers": {},
            "body": b"",
            "utc": utc,
            "elapsed_s": elapsed,
            "redirect_chain": handler.chain,
            "error": f"{type(e).__name__}: {e}",
            "exit": 2,
        }

def sha256_hex(b):
    return hashlib.sha256(b).hexdigest()

def build_cdx(u):
    q = {
        "url": u,
        "from": FROM,
        "to": TO,
        "output": "json",
        "fl": "timestamp,original,mimetype,statuscode,digest,length",
        "filter": ["statuscode:200", "mimetype:text/html"],
        "matchType": "exact",
    }
    # urlencode with doseq for repeated filter
    qs = urllib.parse.urlencode(q, doseq=True)
    return "https://web.archive.org/cdx/search/cdx?" + qs

def pick_newest(cdx_bytes, exact):
    """Parse CDX json bytes. Return (timestamp, rowdict) or (None, reason)."""
    if not cdx_bytes:
        return None, "empty index body"
    try:
        text = cdx_bytes.decode("utf-8", errors="strict")
    except Exception as e:
        return None, f"index not utf-8: {e}"
    try:
        data = json.loads(text)
    except Exception as e:
        return None, f"index malformed json: {e}"
    if not isinstance(data, list) or len(data) == 0:
        return None, "index empty list (no snapshots)"
    # First row may be header field names
    header = None
    rows = data
    if len(data) >= 1 and isinstance(data[0], list) and all(isinstance(x, str) for x in data[0]):
        # Heuristic: header row contains 'timestamp' and 'original'
        if "timestamp" in data[0] and "original" in data[0]:
            header = data[0]
            rows = data[1:]
    if not rows:
        return None, "index header only, no snapshot rows"
    # Map rows to dicts
    candidates = []
    for r in rows:
        if not isinstance(r, list):
            continue
        if header and len(r) == len(header):
            d = dict(zip(header, r))
        else:
            # Fallback positional: timestamp,original,mimetype,statuscode,digest,length
            keys = ["timestamp", "original", "mimetype", "statuscode", "digest", "length"]
            if len(r) != len(keys):
                continue
            d = dict(zip(keys, r))
        ts = str(d.get("timestamp", ""))
        orig = str(d.get("original", ""))
        mt = str(d.get("mimetype", ""))
        sc = str(d.get("statuscode", ""))
        # Eligibility: exact original match, ts <= cutoff, sc 200, html
        if orig != exact:
            continue
        if not ts or ts > CUTOFF:
            continue
        if sc != "200":
            continue
        if "text/html" not in mt:
            continue
        if len(ts) < 14 or not ts.isdigit():
            continue
        candidates.append((ts, d))
    if not candidates:
        return None, "no eligible exact-URL 200 text/html snapshot <= cutoff"
    candidates.sort(key=lambda x: x[0])
    return candidates[-1][0], candidates[-1][1]

def main():
    os.makedirs(BASE_DIR, exist_ok=True)
    index_count = 0
    body_count = 0
    exits = []
    per_url = []
    for i, exact in enumerate(URLS, start=1):
        tag = f"u{i}"
        cdx_url = build_cdx(exact)
        # --- index request (exactly one) ---
        r = one_get(cdx_url)
        index_count += 1
        exits.append(r["exit"])
        idx_body_path = os.path.join(BASE_DIR, f"{tag}.index.body.bin")
        idx_meta_path = os.path.join(BASE_DIR, f"{tag}.index.meta.json")
        with open(idx_body_path, "wb") as f:
            f.write(r["body"])
        idx_meta = {
            "tag": tag,
            "kind": "index",
            "original_url": exact,
            "request_url": r["request_url"],
            "response_url": r["response_url"],
            "utc": r["utc"],
            "elapsed_s": r["elapsed_s"],
            "status": r["status"],
            "headers": r["headers"],
            "redirect_chain": r["redirect_chain"],
            "error": r["error"],
            "exit": r["exit"],
            "body_path": os.path.basename(idx_body_path),
            "body_bytes": len(r["body"]),
            "body_sha256": sha256_hex(r["body"]),
            "cdx_from": FROM,
            "cdx_to": TO,
            "cdx_cutoff": "2026-09-21T16:10:00Z",
        }
        with open(idx_meta_path, "w", encoding="utf-8") as f:
            json.dump(idx_meta, f, indent=2, sort_keys=True)
            f.write("\n")
        # --- select newest eligible ---
        sel_ts, sel_info = pick_newest(r["body"], exact)
        entry = {
            "tag": tag,
            "original_url": exact,
            "cdx_request_url": cdx_url,
            "index_meta": os.path.basename(idx_meta_path),
            "index_body": os.path.basename(idx_body_path),
            "index_exit": r["exit"],
            "selected_timestamp": sel_ts,
            "selection_detail": sel_info,
            "body_meta": None,
            "body_file": None,
            "body_exit": None,
        }
        if sel_ts is None:
            entry["body_status"] = "UNKNOWN"
            entry["body_reason"] = sel_info
        else:
            snap_url = f"https://web.archive.org/web/{sel_ts}id_/{exact}"
            entry["snapshot_request_url"] = snap_url
            b = one_get(snap_url)
            body_count += 1
            exits.append(b["exit"])
            b_body_path = os.path.join(BASE_DIR, f"{tag}.snapshot.body.bin")
            b_meta_path = os.path.join(BASE_DIR, f"{tag}.snapshot.meta.json")
            with open(b_body_path, "wb") as f:
                f.write(b["body"])
            b_meta = {
                "tag": tag,
                "kind": "snapshot_body",
                "original_url": exact,
                "snapshot_timestamp": sel_ts,
                "selection_detail": sel_info,
                "request_url": b["request_url"],
                "response_url": b["response_url"],
                "utc": b["utc"],
                "elapsed_s": b["elapsed_s"],
                "status": b["status"],
                "headers": b["headers"],
                "redirect_chain": b["redirect_chain"],
                "error": b["error"],
                "exit": b["exit"],
                "body_path": os.path.basename(b_body_path),
                "body_bytes": len(b["body"]),
                "body_sha256": sha256_hex(b["body"]),
            }
            with open(b_meta_path, "w", encoding="utf-8") as f:
                json.dump(b_meta, f, indent=2, sort_keys=True)
                f.write("\n")
            entry["body_meta"] = os.path.basename(b_meta_path)
            entry["body_file"] = os.path.basename(b_body_path)
            entry["body_exit"] = b["exit"]
            # success vs body/version: body bytes present + status 200, no semantic PASS claimed
            if b["status"] == 200 and len(b["body"]) > 0 and b["exit"] == 0:
                entry["body_status"] = "RETRIEVED"
            else:
                entry["body_status"] = "UNKNOWN"
                entry["body_reason"] = f"snapshot fetch status={b['status']} bytes={len(b['body'])} error={b['error']}"
        per_url.append(entry)

    manifest = {
        "helper": os.path.basename(__file__),
        "utc_completed": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
        "authorized_original_urls": URLS,
        "cutoff": "2026-09-21T16:10:00Z",
        "cdx_from": FROM,
        "cdx_to": TO,
        "index_requests": index_count,
        "snapshot_requests": body_count,
        "total_requests": index_count + body_count,
        "max_allowed": "3 index + 3 body",
        "exits": exits,
        "per_url": per_url,
        "notes": [
            "CDX index response is metadata, not body proof.",
            "No retries/mirrors/new URLs/API/current-publisher refetch/interval broadening.",
            "Normal archive redirects only resolve selected archive resource; chain logged.",
            "HTML stored as DATA only, not executed.",
            "Lack of historical body remains a gap; no historical semantic PASS claimed.",
        ],
    }
    mpath = os.path.join(BASE_DIR, "manifest.json")
    with open(mpath, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
        f.write("\n")
    # stdout summary (counts only)
    print(json.dumps({"index_requests": index_count, "snapshot_requests": body_count, "exits": exits}, indent=2))
    for e in per_url:
        print(f"{e['tag']} index_exit={e['index_exit']} selected={e['selected_timestamp']} body={e.get('body_status')} body_exit={e.get('body_exit')}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
