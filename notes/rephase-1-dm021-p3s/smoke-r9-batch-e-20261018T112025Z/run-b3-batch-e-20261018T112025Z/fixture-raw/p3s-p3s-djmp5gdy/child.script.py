
import json, os, sys
from pathlib import Path
root = Path(sys.argv[1])
state_path = Path(sys.argv[2]); proposal_path = Path(sys.argv[3])
manifest_path = Path(sys.argv[4]); scope_path = Path(sys.argv[5])
fault = sys.argv[6]
from scripts import survey_editorial_staged_source_v2 as staged
real_write, real_fsync, real_close = os.write, os.fsync, os.close
real_fstat, real_mkdir, real_open = os.fstat, os.mkdir, os.open
STAGED_LEAVES = ("main.tex", "references.bib", "jgaisurvey.sty", "staged-source-manifest.json")
active = {}
gen_counter = {"n": 0}
fired = {"n": 0}
partial_state = {"n": 0}
def _leaf_of(path):
    try:
        s = os.fspath(path)
    except Exception:
        return None
    if isinstance(s, bytes):
        try:
            s = s.decode()
        except Exception:
            return None
    return Path(s).name
def _track_open(path, flags, *a, **k):
    fd = real_open(path, flags, *a, **k)
    if flags & os.O_CREAT:
        leaf = _leaf_of(path)
        if leaf in STAGED_LEAVES:
            gen_counter["n"] += 1
            active[fd] = {"leaf": leaf, "gen": gen_counter["n"]}
    return fd
def _write_once(fd, data):
    info = active.get(fd)
    leaf = info["leaf"] if info else None
    if leaf == "main.tex" and fault in ("zero-write", "write-fail") and fired["n"] == 0:
        fired["n"] += 1
        if fault == "zero-write":
            return 0
        raise OSError(5, "injected write failure")
    if leaf == "main.tex" and fault == "short-once" and fired["n"] == 0:
        fired["n"] += 1
        half = max(1, len(bytes(data)) // 2)
        return real_write(fd, bytes(data)[:half])
    if leaf == "main.tex" and fault == "partial-then-fail":
        if partial_state["n"] == 0 and fired["n"] == 0:
            partial_state["n"] = 1
            fired["n"] += 1
            return real_write(fd, bytes(data)[:1])
        if partial_state["n"] == 1 and fired["n"] == 1:
            fired["n"] += 1
            raise OSError(5, "injected partial-then-fail second write")
    if leaf == "main.tex" and fault == "write-then-close-fail" and fired["n"] == 0:
        fired["n"] += 1
        raise OSError(5, "injected write failure (primary for close test)")
    if leaf == "staged-source-manifest.json" and fault == "manifest-write-fail" and fired["n"] == 0:
        fired["n"] += 1
        raise OSError(5, "injected manifest write failure")
    return real_write(fd, data)
def _fsync_once(fd):
    info = active.get(fd)
    leaf = info["leaf"] if info else None
    if leaf == "main.tex" and fault == "fsync-fail" and fired["n"] == 0:
        fired["n"] += 1
        raise OSError(5, "injected fsync failure")
    return real_fsync(fd)
def _close_once(fd):
    info = active.get(fd)
    leaf = info["leaf"] if info else None
    if leaf == "main.tex" and fault == "close-fail" and fired["n"] == 0:
        fired["n"] += 1
        active.pop(fd, None)
        raise OSError(5, "injected close failure")
    if leaf == "staged-source-manifest.json" and fault == "manifest-close-fail" and fired["n"] == 0:
        fired["n"] += 1
        active.pop(fd, None)
        raise OSError(5, "injected manifest close failure")
    if leaf == "main.tex" and fault == "write-then-close-fail" and fired["n"] == 1:
        fired["n"] += 1
        active.pop(fd, None)
        raise OSError(5, "injected secondary close failure")
    if fault == "close-leak-reuse" and info is not None and fired["n"] == 0:
        fired["n"] += 1
        active.pop(fd, None)
        raise OSError(5, "injected close failure")
    active.pop(fd, None)
    return real_close(fd)
def _fstat_once(fd):
    st = real_fstat(fd)
    info = active.get(fd)
    leaf = info["leaf"] if info else None
    if leaf == "main.tex" and fault == "fstat-fake" and fired["n"] == 0:
        fired["n"] += 1
        return os.stat_result((st.st_mode, st.st_ino + 7, st.st_dev, st.st_nlink, st.st_uid, st.st_gid, st.st_size, st.st_atime, st.st_mtime, st.st_ctime))
    if leaf == "main.tex" and fault == "fstat-fail" and fired["n"] == 0:
        fired["n"] += 1
        raise OSError(5, "injected fstat failure")
    return st
def _mkdir_once(path, *a, **k):
    leaf = _leaf_of(path)
    if leaf == "staged-source" and fault == "mkdir-fail" and fired["n"] == 0:
        fired["n"] += 1
        raise OSError(13, "injected mkdir failure")
    return real_mkdir(path, *a, **k)
_exact_reader_rel = None
try:
    _prop = json.loads(Path(proposal_path).read_bytes().decode("utf-8"))
    _exact_reader_rel = (_prop.get("proposed") or {}).get("proposed_reader_ref", {}).get("path")
except Exception:
    _exact_reader_rel = None
_real_read_bytes = Path.read_bytes
def _read_bytes_once(self):
    data = _real_read_bytes(self)
    try:
        is_exact = (_exact_reader_rel is not None and Path(self) == root / _exact_reader_rel)
    except Exception:
        is_exact = False
    if fault == "drift-reader" and is_exact and fired["n"] == 0:
        fired["n"] += 1
        with open(self, "ab") as handle:
            handle.write(b"\n% injected mid-call drift\n")
    return data
if fault == "drift-reader":
    Path.read_bytes = _read_bytes_once
# R2-4 late/drift/root wrappers: call the real helper first, then inject at the
# exact named boundary (never replace authority with fake success). Each pins
# the exact target path derived from the supplied proposal/manifest.
_real_compare = staged._compare_original_boundary
_real_emit = staged._emit_outputs
_real_verify_outputs = staged._verify_outputs_and_manifest
_real_verify = staged.verify_staged_source
_real_canonical = staged._canonical_json_bytes
_compare_calls = {"n": 0}
_emit_calls = {"n": 0}
def _late_control_path():
    return root / "scripts" / "late-control-probe-p3s.txt"
def _late_retained_dir():
    try:
        _pp = Path(proposal_path).parent.relative_to(root).as_posix()
    except Exception:
        _pp = None
    if _pp is None:
        return None
    return root / _pp / "retained" / "late-retained-probe-dir"
def _staged_rel_exact():
    try:
        _pp = Path(proposal_path).parent.relative_to(root).as_posix()
    except Exception:
        return None
    return _pp + "/staged-source"
def _compare_wrap(*a, **k):
    _compare_calls["n"] += 1
    out = _real_compare(*a, **k)
    if fault == "late-control-add" and _compare_calls["n"] == 1 and fired["n"] == 0:
        fired["n"] += 1
        _late_control_path().write_text("late control addition\n", encoding="utf-8")
    if fault == "late-retained-add" and _compare_calls["n"] == 1 and fired["n"] == 0:
        fired["n"] += 1
        d = _late_retained_dir()
        if d is not None:
            d.mkdir(parents=True, exist_ok=True)
    return out
def _canonical_wrap(*a, **k):
    out = _real_canonical(*a, **k)
    if fault == "drift-before-claim" and fired["n"] == 0:
        fired["n"] += 1
        if _exact_reader_rel is not None:
            with open(root / _exact_reader_rel, "ab") as h:
                h.write(b"\n% drift before claim\n")
    return out
def _emit_wrap(*a, **k):
    _emit_calls["n"] += 1
    if fault in ("root-replace", "ancestor-replace") and _emit_calls["n"] == 1 and fired["n"] == 0:
        fired["n"] += 1
        _srel = _staged_rel_exact()
        if _srel is not None:
            _sabs = root / _srel
            try:
                _backup = Path(str(_sabs) + ".orig-p3s")
                os.rename(_sabs, _backup)
            except Exception:
                _backup = None
            try:
                if fault == "root-replace":
                    _sabs.mkdir(parents=False, exist_ok=False)
                    (_sabs / "replacement.txt").write_text("replacement root\n", encoding="utf-8")
                else:
                    _sabs.symlink_to("/tmp")
            except Exception:
                pass
        return _real_emit(*a, **k)
    out = _real_emit(*a, **k)
    if fault == "drift-before-manifest" and _emit_calls["n"] == 1 and fired["n"] == 0:
        fired["n"] += 1
        try:
            _man = json.loads(Path(manifest_path).read_bytes().decode("utf-8"))
            _rows = _man.get("rows") or []
            _copy = next((r for r in _rows if r.get("policy") == "COPY_BEFORE_REPLACEMENT"), None)
            if _copy is not None:
                with open(root / _copy["retained_dest"], "ab") as h:
                    h.write(b"\n% drift before manifest\n")
            else:
                with open(root / _exact_reader_rel, "ab") as h:
                    h.write(b"\n% drift before manifest fallback\n")
        except Exception:
            pass
    return out
def _verify_outputs_wrap(*a, **k):
    out = _real_verify_outputs(*a, **k)
    if fault == "post-readback-edit" and fired["n"] == 0:
        fired["n"] += 1
        _srel = _staged_rel_exact()
        if _srel is not None:
            _main = root / _srel / "main.tex"
            try:
                _data = _main.read_bytes()
                _main.write_bytes(_data[:10] + b"% POST-READBACK EDIT\n" + _data[10:])
            except Exception:
                pass
    return out
def _verify_wrap(*a, **k):
    out = _real_verify(*a, **k)
    if fault == "post-replay-samebyte-replace" and fired["n"] == 0:
        fired["n"] += 1
        _srel = _staged_rel_exact()
        if _srel is not None:
            for _nm in ("main.tex", "references.bib", "jgaisurvey.sty", "staged-source-manifest.json"):
                _p = root / _srel / _nm
                try:
                    _d = _p.read_bytes()
                    _tmp = _p.parent / (_nm + ".swap-p3s")
                    _tmp.write_bytes(_d)
                    os.replace(_tmp, _p)
                except Exception:
                    pass
            _srel2 = _srel
            try:
                _m = root / _srel2 / "staged-source-manifest.json"
                _d2 = _m.read_bytes()
                _t2 = _m.parent / "staged-source-manifest.json.swap-p3s"
                _t2.write_bytes(_d2)
                os.replace(_t2, _m)
            except Exception:
                pass
    return out
if fault in ("late-control-add", "late-retained-add"):
    staged._compare_original_boundary = _compare_wrap
if fault == "drift-before-claim":
    staged._canonical_json_bytes = _canonical_wrap
if fault in ("drift-before-manifest", "root-replace", "ancestor-replace"):
    staged._emit_outputs = _emit_wrap
if fault == "post-readback-edit":
    staged._verify_outputs_and_manifest = _verify_outputs_wrap
if fault == "post-replay-samebyte-replace":
    staged.verify_staged_source = _verify_wrap
os.open, os.write, os.fsync, os.close, os.fstat, os.mkdir = (
    _track_open, _write_once, _fsync_once, _close_once, _fstat_once, _mkdir_once)
outcome = {"ok": True, "result": "PENDING", "fired": 0}
try:
    out = staged.materialize_staged_source(root, state_path, proposal_path, manifest_path, scope_path)
    outcome = {"ok": True, "result": out["result"], "fired": fired["n"],
               "head": out.get("observed_head")}
except Exception as exc:
    owned = getattr(exc, "owned", {})
    code = getattr(exc, "code", type(exc).__name__)
    phase = getattr(exc, "phase", "")
    disp = getattr(exc, "disposition", "")
    outcome = {"ok": False, "error": f"{type(exc).__name__}: {exc}"[:2000],
               "code": code, "phase": phase, "disposition": disp,
               "fired": fired["n"],
               "owned_files": len(owned.get("owned_files", [])) if isinstance(owned, dict) else 0,
               "owned": owned if isinstance(owned, dict) else {}}
finally:
    os.write, os.fsync, os.close, os.fstat, os.mkdir, os.open = (
        real_write, real_fsync, real_close, real_fstat, real_mkdir, real_open)
    if fault == "drift-reader":
        Path.read_bytes = _real_read_bytes
    staged._compare_original_boundary = _real_compare
    staged._emit_outputs = _real_emit
    staged._verify_outputs_and_manifest = _real_verify_outputs
    staged.verify_staged_source = _real_verify
    staged._canonical_json_bytes = _real_canonical
print(json.dumps(outcome))
