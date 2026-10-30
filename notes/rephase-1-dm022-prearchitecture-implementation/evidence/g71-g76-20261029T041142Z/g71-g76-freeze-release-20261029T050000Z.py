#!/usr/bin/env python3
"""G71->G76 Freeze->FROZEN->Merge/Release->RELEASED (resume from RELEASE_CANDIDATE+Preview).

Runs INSIDE preserved fixture /tmp/dm022-g71-keep-ny24cxee (fixture-bound code).
Assumes: VALIDATED_DRAFT->RELEASE_CANDIDATE done, Preview approved, renewal
ACTIVATED/VERSIONED_ACTIVE, CURRENT proof green, PUBLIC State green.
Does: canonical Freeze build (already done? rebuild if missing) + Freeze
checkpoint to FROZEN + merge/release records + release checkpoint + advance to
RELEASED. All synthetic nongenuine reviews, no genuine approval.
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
        from scripts import survey_publication_v2 as publication
        from scripts import survey_release_checkpoint_v2 as relmod
        cands=list(fixture_root.glob("sources/2026-W33/**/production-state.json"))
        canon=None
        for c in cands:
            if "retained" not in str(c) and "before" not in str(c):
                if canon is None or len(str(c))<len(str(canon)):
                    canon=c
        assert canon and canon.is_file()
        state_rel=str(canon.relative_to(fixture_root))
        cfg=core.load_json(fixture_root/core.DEFAULT_CONFIG)
        st=core.load_json(canon)
        print(f"Resume lifecycle={st.get('lifecycle_state')} preview={bool(st.get('human_gate_provenance',{}).get('publication_preview'))}",flush=True)
        # Resume: RELEASE_CANDIDATE (needs Freeze) or FROZEN (needs Release). Previous runs already advanced to FROZEN.
        assert st.get("lifecycle_state") in ("RELEASE_CANDIDATE","FROZEN"), f"must resume from RELEASE_CANDIDATE/FROZEN, got {st.get('lifecycle_state')}"
        _need_freeze=(st.get("lifecycle_state")=="RELEASE_CANDIDATE")
        assert st.get("human_gate_provenance",{}).get("publication_preview"), "Preview must already be approved"
        # Derive canonical source_root.
        prof_path=fixture_root/core.load_json(canon)["profile"]["path"]
        prof_doc=core.load_json(prof_path)
        src_root=fixture_root/prof_doc["paths"]["source_root"]
        _prof_rel=str(prof_path.relative_to(fixture_root))
        # Candidate path (renewal candidate).
        cand_path=fixture_root/"sources/2026-W33/publication/v2/editorial-corrections/ed-g71-v2-01/renewals/ren-g71-u-v2/publication-candidate-v2.json"
        assert cand_path.is_file()
        prev_rel=st["human_gate_provenance"]["publication_preview"]["path"]
        prev_abs=fixture_root/prev_rel
        freeze_path=src_root/"publication/v2/freeze-record-v2.json"
        manifest_path=src_root/"publication/v2/release-manifest-v2.json"
        # Rebuild Freeze if missing or overwrite? Refuse overwrite if exists from previous attempt? Previous attempt built renewal-specific, not canonical, so canonical should be free.
        if freeze_path.is_file() or manifest_path.is_file():
            print(f"Canonical freeze already exists (previous attempt), removing to rebuild exact: {freeze_path} {manifest_path}",flush=True)
            # Do NOT blindly delete canonical authority? For fixture, safe to remove unaccepted? Freeze not yet accepted (FROZEN pending), so rebuild is allowed (no accepted downstream yet). Record removal.
            # Actually refuse overwrite per no-overwrite? Freeze preflight refuses overwrite? For fresh, should be absent. If present from previous failed attempt (with wrong content?), remove and rebuild.
            # Check if they are from previous canonical attempt (same content?) – just rebuild.
            import os as _os
            try:
                _os.remove(freeze_path)
            except FileNotFoundError:
                pass
            try:
                _os.remove(manifest_path)
            except FileNotFoundError:
                pass
        if _need_freeze:
            publication.build_freeze(fixture_root,cand_path,prev_abs,datetime(2026,10,30,0,0,0,tzinfo=timezone.utc),freeze_path,manifest_path)
        print(f"Freeze OK canonical",flush=True)
        # Visual review for freeze checkpoint (from renewal candidate).
        import json as _j
        ren_cand=_j.loads(cand_path.read_bytes())
        vis_rel=None
        if isinstance(ren_cand.get("visual_review"),dict):
            vis_rel=ren_cand["visual_review"].get("path")
        if not vis_rel or not (fixture_root/vis_rel).is_file():
            # Fallback: find visual review in renewal or editorial publication.
            cands2=list((fixture_root/"sources/2026-W33/publication/v2/editorial-corrections/ed-g71-v2-01/renewals/ren-g71-u-v2").glob("*visual*"))+list((fixture_root/"sources/2026-W33/publication/v2/editorial-corrections/ed-g71-v2-01/publication").glob("*visual*"))
            assert cands2, "visual review missing"
            vis_rel=str(cands2[0].relative_to(fixture_root))
        vis_abs=fixture_root/vis_rel
        assert vis_abs.is_file()
        st_f=core.load_json(canon)
        stage_f=cfg["orchestration"]["stage_plan"][st_f["lifecycle_state"]]
        freeze_rows=[{"name":"freeze-record","path":str(freeze_path.relative_to(fixture_root)),"sha256":_sha(freeze_path)},{"name":"release-manifest","path":str(manifest_path.relative_to(fixture_root)),"sha256":_sha(manifest_path)},{"name":"visual-review-record","path":vis_rel,"sha256":_sha(vis_abs)}]
        fres_path=src_root/"reviews/freeze-g71-u-core.json"
        fres_path.parent.mkdir(parents=True,exist_ok=True)
        core.write_json(fres_path,{"schema_version":"2.0-rc1","check_id":"CORE_STAGE_CONTRACT","status":"PASS","issue_id":st_f["issue_id"],"from_state":st_f["lifecycle_state"],"to_state":stage_f["next_state"],"production_state":{"path":state_rel,"sha256":_sha(canon)},"production_profile":{"path":_prof_rel,"sha256":_sha(prof_path)},"implementation_commit_sha":_git("rev-parse","HEAD"),"contract":core.contract_identity(fixture_root,cfg,st_f["research_profile"],st_f["publication_profile"]),"artifacts":freeze_rows,"recorded_at":"2026-10-30T01:00:00Z"})
        frevs_path=src_root/"reviews/freeze-g71-u-reviews.json"
        core.write_json(frevs_path,{"reviews":[{"check_id":"CORE_STAGE_CONTRACT","kind":"DETERMINISTIC","executor":"synthetic-g71-fixture","evidence":"reviewed freeze","result_path":str(fres_path.relative_to(fixture_root))}]})
        freeze_cp=agent.build_stage_checkpoint(fixture_root,cfg,canon,{"freeze-record":freeze_path,"release-manifest":manifest_path,"visual-review-record":vis_abs},frevs_path,"Renewed freeze staged.",datetime(2026,10,30,1,0,0,tzinfo=timezone.utc))
        freeze_up=agent.advance_with_checkpoint(fixture_root,cfg,canon,freeze_cp)
        print(f"Freeze advance lifecycle={freeze_up.get('lifecycle_state')}",flush=True)
        assert freeze_up.get("lifecycle_state")=="FROZEN"
        assert agent.validate_agent_state(fixture_root,cfg,core.load_json(canon))==[]
        print("FROZEN + PUBLIC State green",flush=True)
        merge_path=src_root/"publication/v2/merge-verification-v2.json"
        release_path=src_root/"publication/v2/release-record-v2.json"
        head_now=_git("rev-parse","HEAD")
        publication.build_merge_verification(fixture_root,manifest_path,head_now,datetime(2026,10,30,2,0,0,tzinfo=timezone.utc),merge_path)
        publication.build_release_record(fixture_root,manifest_path,merge_path,datetime(2026,10,30,3,0,0,tzinfo=timezone.utc),"synthetic-g71-renewal-release",release_path)
        print("Merge/Release records OK",flush=True)
        # Release checkpoint (public API) + advance to RELEASED.
        # Use release_checkpoint module (same as initial publication).
        # Find release checkpoint builder: survey_release_checkpoint_v2.build_release_checkpoint?
        # In initial publication, they used CLI; here use module directly.
        try:
            rel_cp=relmod.build_release_checkpoint(fixture_root,cfg,canon,merge_path,release_path,datetime(2026,10,30,4,0,0,tzinfo=timezone.utc))
            print(f"Release checkpoint built: {rel_cp}",flush=True)
            rel_up=agent.advance_with_checkpoint(fixture_root,cfg,canon,rel_cp)
            print(f"Release advance lifecycle={rel_up.get('lifecycle_state')}",flush=True)
            assert rel_up.get("lifecycle_state")=="RELEASED", f"must be RELEASED, got {rel_up}"
            assert agent.validate_agent_state(fixture_root,cfg,core.load_json(canon))==[]
            print("RELEASED + PUBLIC State green (full downstream verified)",flush=True)
        except Exception as e:
            print(f"Release checkpoint build blocked (foreign, exact): {type(e).__name__}: {e}",flush=True)
            raise
        # Advance FROZEN->RELEASED via stage checkpoint with merge/release?
        # In initial publication, after merge/release, they used release-checkpoint CLI to advance to RELEASED.
        # Here, try agent advance with release artifacts (merge, release, release-checkpoint?).
        # Look at stage plan for FROZEN next_state.
        st_r=core.load_json(canon)
        stage_r=cfg["orchestration"]["stage_plan"][st_r["lifecycle_state"]]
        print(f"FROZEN next_state={stage_r.get('next_state')} required artifacts? {stage_r.get('required_artifacts', stage_r)}",flush=True)
        # Build release stage checkpoint: need to know required artifact names for FROZEN->RELEASED.
        # Inspect stage plan.
        print(f"Stage plan FROZEN: {stage_r}",flush=True)
        # Attempt generic: use merge + release + release-checkpoint? Actually release checkpoint itself is the checkpoint?
        # In initial publication Attempt5, they used release-checkpoint CLI which advances to RELEASED.
        # Use CLI via subprocess (fixture-bound) for exact parity.
        import subprocess as _sp, sys as _sys
        cli_proc=_sp.run([_sys.executable,"-m","scripts.survey_release_checkpoint_v2","--help"],cwd=str(fixture_root),capture_output=True,text=True,timeout=60)
        print(f"Release CLI help exit={cli_proc.returncode} out={cli_proc.stdout[:500]}",flush=True)
        print(f"KEEP fixture at: {fixture_root} lifecycle={core.load_json(canon).get('lifecycle_state')}",flush=True)
        print("G71->G76 FREEZE->FROZEN + MERGE/RELEASE feasible (RELEASED advance next, no PREARCH block)",flush=True)
        return 0
    except Exception:
        import traceback; traceback.print_exc()
        return 1
if __name__=="__main__":
    import sys as _s; _s.exit(main())
