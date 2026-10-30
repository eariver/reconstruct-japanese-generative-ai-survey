"""Independent small fault probe (read-only snapshot copy, no source patch)."""
import hashlib, json, os, sys, tempfile
from pathlib import Path
ROOT = Path("/tmp/dm022-independent-op-probe-20261029T060000Z/exec")
sys.path.insert(0, str(ROOT))
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
# Ensure no GIT_* overrides leak
for k in list(os.environ):
    if k.startswith("GIT_"):
        del os.environ[k]
from scripts import survey_research_authority_v2 as low
from scripts import survey_prearchitecture_acceptance_v2 as high

def check(name, fn):
    try:
        fn()
        print(f"PASS {name}")
        return True
    except AssertionError as e:
        print(f"FAIL {name}: {e}")
        return False
    except Exception as e:
        print(f"ERROR {name}: {type(e).__name__}: {e}")
        return False

results = []

# 1. _norm_path accepts Path/string, refuses None/empty/bytes with typed error (not AttributeError)
def t_norm():
    p = low._norm_path(Path("/tmp/x"), "lbl")
    assert isinstance(p, Path)
    p2 = low._norm_path("a/b", "lbl")
    assert isinstance(p2, Path)
    for bad in (None, "", b"bytes", 123):
        try:
            low._norm_path(bad, "lbl")
            raise AssertionError(f"should refuse {bad!r}")
        except low.ResearchAuthorityError:
            pass
        except AttributeError:
            raise AssertionError("bare AttributeError leak")
    # HIGH same
    try:
        high._norm_path(None, "lbl")
        raise AssertionError("HIGH should refuse None")
    except high.AcceptanceError:
        pass
results.append(check("norm_path_typed", t_norm))

# 2. require_no_active_guard: absent passes, present file refuses, nonregular refuses, unreadable refuses (as root, unreadable still regular -> refuses as present)
def t_guard():
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "src"
        src.mkdir()
        # absent passes
        low.require_no_active_guard(src)
        # present file refuses
        g = src / low.DM022_GUARD_REL
        g.parent.mkdir(parents=True)
        g.write_bytes(b'{"x":1}\n')
        try:
            low.require_no_active_guard(src)
            raise AssertionError("should refuse present guard")
        except low.ResearchAuthorityError as e:
            assert "DM022_TRANSITION_ACTIVE" in str(e), str(e)
        # nonregular (dir at guard path) refuses
        g.unlink()
        g.mkdir()
        try:
            low.require_no_active_guard(src)
            raise AssertionError("should refuse nonregular guard")
        except low.ResearchAuthorityError as e:
            assert "DM022_TRANSITION_ACTIVE" in str(e)
results.append(check("guard_absence", t_guard))

# 3. _exclusive_write_bytes: first succeeds, second refuses (no overwrite), temp preserved
def t_exclusive():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "a.json"
        data = b'{"a":1}\n'
        info = high._exclusive_write_bytes(p, data, "probe")
        assert p.read_bytes() == data
        assert "ino" in info and "dev" in info
        try:
            high._exclusive_write_bytes(p, b'{"a":2}\n', "probe2")
            raise AssertionError("should refuse overwrite")
        except high.AcceptanceError as e:
            assert "no overwrite" in str(e).lower() or "refused" in str(e).lower() or "atomic link" in str(e), str(e)
        assert p.read_bytes() == data, "original must be preserved"
        # temp preserved: check sibling .tmp.* exists
        tmps = list(Path(td).glob("a.json.tmp.*"))
        assert len(tmps) >= 1, f"temp should be preserved, found {tmps}"
results.append(check("exclusive_no_overwrite", t_exclusive))

# 4. load_typed_checkpoint_record: unknown kind refuses, PREARCH bad reason refuses, legacy passes minimal?
def t_decoder():
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        # unknown kind
        unk = td / "unk.json"
        unk.write_bytes(json.dumps({"kind": "VERSIONED_RENEWAL_ACTIVATION_V1", "reason_class": "X"}).encode())
        try:
            low.load_typed_checkpoint_record(ROOT, unk)
            raise AssertionError("should refuse unknown kind")
        except low.ResearchAuthorityError as e:
            assert "unknown checkpoint kind" in str(e), str(e)
        # PREARCH bad reason (uses reason_class instead of reason) refuses
        bad = td / "bad.json"
        bad.write_bytes(json.dumps({"kind": "PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1", "reason_class": "REVIEWED_ACCEPTED_UPSTREAM_CORRECTION"}).encode())
        try:
            low.load_typed_checkpoint_record(ROOT, bad)
            raise AssertionError("should refuse bad PREARCH")
        except low.ResearchAuthorityError:
            pass
        # string path same as Path (A4 normalization)
        try:
            low.load_typed_checkpoint_record(ROOT, str(unk))
            raise AssertionError("str path should also refuse unknown")
        except low.ResearchAuthorityError as e:
            assert "unknown checkpoint kind" in str(e)
results.append(check("decoder_separation", t_decoder))

# 5. lstat_slot: absent legitimate, regular present, nonregular (symlink/dir) classified, never coerced
def t_slot():
    with tempfile.TemporaryDirectory() as td:
        src = Path(td)
        # absent
        obs = low.lstat_slot(src, "candidate-matrix-v2.json")
        assert obs["present"] is False and obs["lstat_kind"] == "absent", obs
        # regular
        (src / "candidate-matrix-v2.json").write_bytes(b'{"x":1}\n')
        obs2 = low.lstat_slot(src, "candidate-matrix-v2.json")
        assert obs2["present"] is True and obs2["lstat_kind"] == "regular", obs2
        # symlink (nonregular)
        link_src = src / "candidate-selection-v2.json"
        link_src.symlink_to(src / "candidate-matrix-v2.json")
        obs3 = low.lstat_slot(src, "candidate-selection-v2.json")
        assert obs3["lstat_kind"] == "nonregular", obs3
        # dir at slot path -> nonregular
        d = src / "architecture-v2.json"
        d.mkdir()
        obs4 = low.lstat_slot(src, "architecture-v2.json")
        assert obs4["lstat_kind"] == "nonregular", obs4
results.append(check("slot_lstat", t_slot))

# 6. _safe_read_bytes: symlink refuses (O_NOFOLLOW), inode change detected? (basic)
def t_saferead():
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "real.json"
        src.write_bytes(b'{"a":1}\n')
        link = Path(td) / "link.json"
        link.symlink_to(src)
        try:
            low._safe_read_bytes(link, "probe link")
            raise AssertionError("symlink should refuse")
        except low.ResearchAuthorityError as e:
            assert "not a regular file" in str(e) or "O_NOFOLLOW" in str(e) or "regular" in str(e), str(e)
results.append(check("saferead_nofollow", t_saferead))

print(f"SUMMARY {sum(results)}/{len(results)} passed")
sys.exit(0 if all(results) else 1)
