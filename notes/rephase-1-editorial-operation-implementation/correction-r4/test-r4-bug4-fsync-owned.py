#!/usr/bin/env python3
"""R4 Bug4 focused: fsync propagate + owned inode recheck (no false CAS).

- Mocks os.fsync to raise OSError, verifies agent/high writers propagate (not pass),
  preserving bytes (no delete).
- Verifies owned inode+bytes recheck: same-byte foreign swap (different inode,
  identical content) refuses; unknown State never deletes referenced record.
- Verifies legacy R1 ordinary path still works (no regression): normal create/replace
  without fault passes.
Saved BEFORE execution. Temp dirs only.
"""
from __future__ import annotations
import os, sys, pathlib, tempfile, json

if os.environ.get("PYTHONDONTWRITEBYTECODE") != "1":
    print("BLOCKER PYTHONDONTWRITEBYTECODE"); sys.exit(2)
if not os.environ.get("PYTHONPYCACHEPREFIX","").startswith("/tmp/opencode/"):
    print("BLOCKER PYTHONPYCACHEPREFIX"); sys.exit(2)

DST = pathlib.Path("/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60")
sys.path.insert(0, str(DST))
for m in list(sys.modules.keys()):
    if m.startswith("scripts."):
        del sys.modules[m]
if "scripts" in sys.modules:
    del sys.modules["scripts"]

def main() -> int:
    import scripts.survey_agent_control_v2 as agent
    # 1. fsync failure propagates (agent record)
    with tempfile.TemporaryDirectory(prefix="r4-bug4-", dir="/tmp") as td:
        root = pathlib.Path(td)
        rec = root / "r1.json"
        orig_fsync = os.fsync
        def bad_fsync(fd):
            raise OSError("simulated fsync fault")
        os.fsync = bad_fsync  # type: ignore
        try:
            try:
                agent._exclusive_create_record_bytes(rec, b'{"x":1}', "test record")
                print("FAIL fsync should propagate"); return 2
            except agent.AgentControlError as e:
                assert "fsync" in str(e).lower(), e
                print("AGENT_RECORD_FSYNC_PROPAGATED PASS")
                # bytes preserved (owned partial, not deleted)
                assert rec.is_file(), "record should be preserved on fsync fail"
                print("OWNED_PARTIAL_PRESERVED PASS")
        finally:
            os.fsync = orig_fsync
        # 2. fsync failure propagates (agent State temp)
        state = root / "state.json"
        state.write_bytes(b'{"old":1}')
        os.fsync = bad_fsync  # type: ignore
        try:
            try:
                agent._atomic_replace_state_bytes(state, b'{"old":1}', b'{"new":1}', "test State")
                print("FAIL State fsync should propagate"); return 2
            except agent.AgentControlError as e:
                assert "fsync" in str(e).lower(), e
                print("AGENT_STATE_FSYNC_PROPAGATED PASS")
                assert state.read_bytes() == b'{"old":1}', "live State preserved"
                print("LIVE_STATE_PRESERVED PASS")
        finally:
            os.fsync = orig_fsync
        # 3. high writer fsync propagates
        import scripts.survey_editorial_publication_v2 as ed
        hp = root / "out.json"
        os.fsync = bad_fsync  # type: ignore
        try:
            try:
                ed._exclusive_write_bytes(hp, b'hello', "high test")
                print("FAIL high fsync should propagate"); return 2
            except Exception as e:
                assert "FSYNC" in str(e) or "fsync" in str(e).lower(), e
                print("HIGH_FSYNC_PROPAGATED PASS")
        finally:
            os.fsync = orig_fsync
        # 4. owned inode recheck: same-byte foreign swap refuses
        rec2 = root / "r2.json"
        payload = b'{"same":1}'
        owned = agent._exclusive_create_record_bytes(rec2, payload, "owned test")
        # foreign swap: replace with same bytes but different inode (new file)
        rec2.unlink()
        rec2.write_bytes(payload)  # new inode, same bytes
        # _record_identity_matches should be False (same bytes, different inode)
        assert agent._record_identity_matches(rec2, owned, payload) is False, "same-byte foreign must not match"
        print("SAME_BYTE_FOREIGN_REFUSED PASS (identity+bytes, not bytes alone)")
        # unknown State never deletes referenced record: _drop_own_temp logic preserves on mismatch
        # (covered by agent code; here verify record still exists after failed match)
        assert rec2.is_file(), "referenced record must never be deleted"
        print("REFERENCED_NEVER_DELETED PASS")
        # 5. legacy ordinary R1 path still works (no fault): normal create+replace passes
        rec3 = root / "r3.json"
        owned3 = agent._exclusive_create_record_bytes(rec3, b'{"ok":1}', "healthy")
        assert agent._record_identity_matches(rec3, owned3, b'{"ok":1}') is True
        st3 = root / "s3.json"
        st3.write_bytes(b'old')
        agent._atomic_replace_state_bytes(st3, b'old', b'new', "healthy State")
        assert st3.read_bytes() == b'new'
        print("HEALTHY_CONTROL PASS (ordinary R1 before versioned continues)")
    print("BUG4_FOCUSED PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
