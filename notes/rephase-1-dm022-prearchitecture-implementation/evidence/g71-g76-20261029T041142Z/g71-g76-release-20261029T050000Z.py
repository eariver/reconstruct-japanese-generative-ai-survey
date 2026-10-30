#!/usr/bin/env python3
"""G71->G76 RELEASED (resume from FROZEN, canonical Freeze/Merge/Release exist).

Runs INSIDE preserved fixture /tmp/dm022-g71-keep-ny24cxee.
Does: release checkpoint (public API, C2 narrow gate, G71 no PREARCH so passes)
+ advance FROZEN->RELEASED via agent + PUBLIC State validation + CURRENT proof
repeat. All synthetic nongenuine, no genuine approval.
"""
import json, sys, subprocess
from pathlib import Path
from datetime import datetime, timezone
fixture_root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path("/tmp/dm022-g71-keep-ny24cxee")
import os
os.chdir(str(fixture_root))
sys.path.insert(0,str(fixture_root))
for _v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE","GIT_OBJECT_DIRECTORY","GIT_ALTERNATE_OBJECT_DIRECTORIES","GIT_COMMON_DIR"):
    os.environ.pop(_v,None)
os.environ["GIT_OPTIONAL_LOCKS"]="0"
os.environ["GIT_CONFIG_NOSYSTEM"]="1"
from scripts import survey_production_v2 as core
import inspect
assert str(Path(inspect.getfile(core)).resolve()).startswith(str(fixture_root))
def _sha(p:Path)->str:
    import hashlib as _h
    return _h.sha256(p.read_bytes()).hexdigest()
def _git(*a):
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_OPTIONAL_LOCKS":"0","GIT_CONFIG_NOSYSTEM":"1"})
    r=subprocess.run(["git",*a],cwd=str(fixture_root),capture_output=True,text=True,env=env,timeout=120)
    if r.returncode!=0:
        raise AssertionError(f"git {' '.join(a)} failed: {r.stderr[:800]}")
    return r.stdout.strip()
def main()->int:
    try:
        from scripts import survey_agent_control_v2 as agent
        from scripts import survey_release_checkpoint_v2 as relmod
        from scripts import survey_versioned_renewal_source_v2 as srcmod
        cands=list(fixture_root.glob("sources/2026-W33/**/production-state.json"))
        canon=None
        for c in cands:
            if "retained" not in str(c) and "before" not in str(c):
                if canon is None or len(str(c))<len(str(canon)):
                    canon=c
        assert canon
        state_rel=str(canon.relative_to(fixture_root))
        cfg=core.load_json(fixture_root/core.DEFAULT_CONFIG)
        st=core.load_json(canon)
        print(f"Resume lifecycle={st.get('lifecycle_state')}",flush=True)
        assert st.get("lifecycle_state")=="FROZEN"
        prof_path=fixture_root/core.load_json(canon)["profile"]["path"]
        prof_doc=core.load_json(prof_path)
        src_root=fixture_root/prof_doc["paths"]["source_root"]
        merge_path=src_root/"publication/v2/merge-verification-v2.json"
        release_path=src_root/"publication/v2/release-record-v2.json"
        for p in (merge_path,release_path):
            assert p.is_file(), f"missing {p}"
        # Release checkpoint (C2 narrow gate, G71 no PREARCH trio so passes).
        rel_cp=relmod.build_release_checkpoint(fixture_root,cfg,canon,merge_path,release_path,datetime(2026,10,30,4,0,0,tzinfo=timezone.utc))
        print(f"Release checkpoint built: {rel_cp.relative_to(fixture_root)}",flush=True)
        rel_up=agent.advance_with_checkpoint(fixture_root,cfg,canon,rel_cp)
        print(f"Release advance lifecycle={rel_up.get('lifecycle_state')}",flush=True)
        assert rel_up.get("lifecycle_state")=="RELEASED"
        assert agent.validate_agent_state(fixture_root,cfg,core.load_json(canon))==[]
        print("RELEASED + PUBLIC State green",flush=True)
        # CURRENT proof repeat (renewal basis/proof still valid after release? Renewal proof is detached, should still pass).
        new_basis=fixture_root/"sources/2026-W33/publication/v2/editorial-corrections/ed-g71-v2-01/renewals/ren-g71-u-v2/renewal-basis.json"
        new_proof=fixture_root/"sources/2026-W33/publication/v2/editorial-corrections/ed-g71-v2-01/renewals/ren-g71-u-v2/renewal-source-proof.json"
        vrfy=srcmod.verify_renewal_source_proof(fixture_root,str(new_basis.relative_to(fixture_root)),str(new_proof.relative_to(fixture_root)))
        assert vrfy.get("CURRENT_PROOF_VALID") is True
        print(f"CURRENT proof repeat after RELEASED: {vrfy.get('CURRENT_PROOF_VALID')}",flush=True)
        print(f"KEEP fixture at: {fixture_root} lifecycle=RELEASED",flush=True)
        print("G71->G76 U CONTROL FULLY VERIFIED (WEEKLY, genuine G71->G76, CURRENT70, PUBLIC State, Candidate/Preview/Freeze/Release to RELEASED)",flush=True)
        return 0
    except Exception:
        import traceback; traceback.print_exc()
        return 1
if __name__=="__main__":
    import sys as _s; _s.exit(main())
