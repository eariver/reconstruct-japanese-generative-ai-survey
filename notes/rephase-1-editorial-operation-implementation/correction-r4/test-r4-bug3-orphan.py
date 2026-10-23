#!/usr/bin/env python3
"""R4 Bug3 focused: predecessor+1 seq + intent collision (no max+1 fork).

- Temp repo with source_root/publication/v2, profile, State.
- State predecessor r1, existing orphan r2 same intent: _next_record_seq must return r2
  (predecessor+1, not r3 max+1), and ordinary activate must refuse via collision +
  intent detection (explicit resume required, no auto adoption, no latest authority).
- Normal case (no orphan, predecessor is latest): next = predecessor+1 = max+1 passes.
Saved BEFORE execution. Temp dirs only.
"""
from __future__ import annotations
import os, sys, pathlib, tempfile, json, hashlib

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

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def make_repo(root: pathlib.Path, predecessor_seq: int | None, existing_seqs: list[int]):
    # profile
    prof_dir = root / "profiles"
    prof_dir.mkdir(parents=True, exist_ok=True)
    prof_path = prof_dir / "profile.json"
    prof = {"paths": {"source_root": "sources/ISSUE"}}
    prof_path.write_text(json.dumps(prof))
    prof_sha = sha(prof_path.read_bytes())
    # source root + pub dir
    pub = root / "sources/ISSUE/publication/v2"
    pub.mkdir(parents=True, exist_ok=True)
    for s in existing_seqs:
        (pub / f"publication-surface-revalidation-r{s}.json").write_text(json.dumps({"dummy": s}))
    # State
    if predecessor_seq is None:
        pointer = None
    else:
        # need sha for pointer; use dummy file sha if exists else fake
        p_path = f"sources/ISSUE/publication/v2/publication-surface-revalidation-r{predecessor_seq}.json"
        # if file exists, hash it, else fake 0
        pf = root / p_path
        psha = sha(pf.read_bytes()) if pf.is_file() else "0"*64
        pointer = {"path": p_path, "sha256": psha}
    state = {"profile": {"path": "profiles/profile.json", "sha256": prof_sha},
             "publication_revalidation_provenance": pointer}
    return state

def main() -> int:
    import scripts.survey_editorial_publication_v2 as ed
    # case 1: predecessor r1, orphan r2 exists -> next must be r2 (not r3)
    with tempfile.TemporaryDirectory(prefix="r4-bug3-", dir="/tmp") as td:
        root = pathlib.Path(td).resolve()
        state = make_repo(root, predecessor_seq=1, existing_seqs=[1, 2])
        # need existing r1 file for pointer sha to match? make_repo already hashed r1
        # _next_record_seq uses State pointer seq, not max
        try:
            rec_path, nxt = ed._next_record_seq(root, {}, state)
        except Exception as e:
            print(f"FAIL _next should return r2, got exc {e}"); return 2
        if nxt != 2:
            print(f"FAIL next should be 2 (predecessor+1), got {nxt} (max+1 fork bug)"); return 2
        print(f"PREDECESSOR_PLUS1 PASS next={nxt} path={rec_path.name}")
        # collision: r2 exists, so ordinary activate must refuse (lstat exists)
        import os as _os
        try:
            _os.lstat(rec_path)
            print("COLLISION_EXISTS PASS (ordinary activate must refuse, use resume)")
        except FileNotFoundError:
            print("FAIL r2 should exist for collision"); return 2
        # intent detection: same intent elsewhere (r5 same intent as r2) must also refuse
        # simulate record_base intent
        record_base = {"issue_id": "ISSUE", "supersedes": state["publication_revalidation_provenance"],
                       "before_state_ref": {"path": "sources/ISSUE/production-state.json", "sha256": "a"*64},
                       "set_ref": {"path": "sources/ISSUE/publication/v2/editorial-corrections/x/publication/publication-set.json", "sha256": "b"*64},
                       "prior_checkpoint": {"path": "c.json", "sha256": "c"*64}}
        # create r5 with same intent
        pub = root / "sources/ISSUE/publication/v2"
        r5 = {"kind": "EDITORIAL_PUBLICATION_ACTIVATION_V1", "reason_class": "REVIEWED_EDITORIAL_CORRECTION",
              "issue_id": "ISSUE", "supersedes": record_base["supersedes"],
              "before_state_ref": record_base["before_state_ref"], "set_ref": record_base["set_ref"],
              "prior_checkpoint": record_base["prior_checkpoint"]}
        (pub / "publication-surface-revalidation-r5.json").write_text(json.dumps(r5))
        try:
            ed._refuse_if_intent_exists(root, record_base, "sources/ISSUE/publication/v2/publication-surface-revalidation-r2.json")
            print("FAIL intent should refuse (r5 same intent)"); return 2
        except Exception as e:
            msg = str(e)
            assert "INTENT_COLLISION" in msg or "already exists" in msg or "resume" in msg.lower(), msg
            print(f"INTENT_COLLISION_REFUSED PASS ({msg[:120]})")
        # different intent must not refuse
        record_base2 = dict(record_base)
        record_base2["set_ref"] = {"path": "different.json", "sha256": "c"*64}
        try:
            ed._refuse_if_intent_exists(root, record_base2, "sources/ISSUE/publication/v2/publication-surface-revalidation-r2.json")
            print("DIFFERENT_INTENT_ALLOWED PASS")
        except Exception as e:
            print(f"FAIL different intent should allow: {e}"); return 2
    # case 2: normal, predecessor is latest (r2, max 2) -> next 3
    with tempfile.TemporaryDirectory(prefix="r4-bug3b-", dir="/tmp") as td:
        root = pathlib.Path(td).resolve()
        state = make_repo(root, predecessor_seq=2, existing_seqs=[1, 2])
        import scripts.survey_editorial_publication_v2 as ed2
        rec_path, nxt = ed2._next_record_seq(root, {}, state)
        if nxt != 3:
            print(f"FAIL normal next should be 3, got {nxt}"); return 2
        print("NORMAL_NEXT PASS")
        # unknown branch (unparseable predecessor) refuses
        state_bad = dict(state)
        state_bad["publication_revalidation_provenance"] = {"path": "weird.json", "sha256": "0"*64}
        try:
            ed2._next_record_seq(root, {}, state_bad)
            print("FAIL unknown branch should refuse"); return 2
        except Exception as e:
            assert "unknown" in str(e).lower() or "PREDECESSOR" in str(e), e
            print("UNKNOWN_BRANCH_REFUSED PASS")
    print("BUG3_FOCUSED PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
