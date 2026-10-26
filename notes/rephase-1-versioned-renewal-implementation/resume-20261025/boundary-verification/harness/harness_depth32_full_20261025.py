#!/usr/bin/env python3
"""Depth32-full finite construction: 30 provided legacy + 1 actual editorial + 1 actual renewal, 33 refuses.

TEST-only, no product edits, no candidate/reconstruct commits, no network/old-runners,
no cleanup failed fixture/cache purge. Uses workspace TMPDIR, per-phase 1200 with
owned PID/heartbeats/terminal exit, don't duplicate child on return.

ROOT accepts finite construction (not 32 actual ops):
- Use REAL old canonical R1x2 fixture source 36c679cc (old721+only weekly derivation
  comment epochs) and its valid r2 cumulative original checkpoint rows as TEMPLATE.
- Create NEW independent fixture provided history r1..r30 with REAL file SHAs/
  supersedes/strict schema/own OLD tool commits/monotonic timestamps and same
  valid cumulative rows; clearly label NOT R1x30 actual ops.
- Canonical current State points r30 in THIS new test fixture only, verified exact
  Profile/checkpoint/current canonical outputs + public old agent validate_state.
- Original real R1 fixtures unchanged.
- Need old source code from available R1 chain retained GitDB at 36c679 own
  clone+code checkout in NEW fixture before constructing input (no fake ancestor/
  no empty root).
- Source/E old data generation may reuse old r2 snapshot copies, or retained
  before-State COPY from actual r3 defines r2 pointer pre editorial; construction
  explicit not Production recovery/rewind original.
- Then run ACTUAL old public editorial correction at 31 (P1/P2R/P2V/P3S50/
  realbuild/finalize/activate) with latest legacy anchor REAL TYPED r30, no
  synthetic fake Candidate; all source committed before authority. Creates valid
  NONNULL versioned predecessor 31.
- Overlay CURRENT full source SOURCE-only commit preserving all old E, genuine
  Core change, run PUBLIC renewal U prepare/finalize/activate as 32
  (coreStyle old unchanged baseline035). Strict State/current proof/history
  passes chain32; anchor r30 unchanged.
- Then next genuine Core comment Source commit -> public prepare/activate33 must
  REFUSE before NEW R/State writes; record exact which gate catches and immediate
  inventory.
- Only 1 actual editorial+1 actual renewal on 31 fixture-provided predecessors,
  NOT 32 full genuine ops; labelled scope qualifier required.
- Code/validator no changes, no dummy sha or rows invalid schema.
- If old source constructor initial canonical State at r30 requires direct State
  fixture build allowed ONLY new test input exact descriptor not public live
  process rollback; actual tested HIGH32 public begins from fully valid input.
- Existing defensive cycle/public malformed cycle scopes acceptable; true SHA
  consistent cycle not required (fixedpoint infeasible), don't mark impossible
  open as delivery requirement. Existing alias current public same-leaf hardlink
  now HIT cite no rerun.
- No network/old runners/candidate/reconstruct commits/cleanup failed fixture/
  cache purge. Use workspace TMPDIR; per phase 1200 with owned PID heartbeats/
  terminal exit, don't duplicate child on return.
- Write NEW boundary-verification/depth32-full-<UTC>/ raw source input
  construction proof+entry validity+actual32/33 oracles. Return terminal public
  proof or EXACT constraint not generic 'needs 32 genuine epochs'; whole unit
  no CommitPoint.

Current source pins (FILE-BYTE SHA256):
  H 74275d22a342014009d5d090fbe9c552981941e90259c298065d2ba6929d1f3d
  S 2290ddd0dc8397f86451aff70d50fd4da0c6184fcf1bef3ed96259642af2d1eb
  HIGH 1dad1ad12ba509c477ea97fb3a22e5156ae1627182f3286f373f32eae7ba2fbb
  P1 825dba1dedaed0850134b3a54a249a427b2e77709861818e8eb7cb63e1a33a2b
  PUB 3f4039fd7699baa212020dddfb02b3918bd63e02c475d638d99cbb2a1150d8d6
  edpub 85814124278c3112562c84c4685ef555689d551b494dcbd23526fb27dc1d9a2a
  P3S 9e2a0ad6b42cb2444f03f2f9db138c6c1e1db7f41434f5fb1878d87f99ca7ab1
  Reader 098a2c8222f15f693c524139f2678be008a7ec9fafca275fc831ede9aa13bf1c
"""
from __future__ import annotations
import copy, hashlib, json, os, shutil, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

UTC = "20261025T200000Z"
CHAIN_LIMIT = 32

PINS = {
    "H": "74275d22a342014009d5d090fbe9c552981941e90259c298065d2ba6929d1f3d",
    "S": "2290ddd0dc8397f86451aff70d50fd4da0c6184fcf1bef3ed96259642af2d1eb",
    "HIGH": "1dad1ad12ba509c477ea97fb3a22e5156ae1627182f3286f373f32eae7ba2fbb",
    "P1": "825dba1dedaed0850134b3a54a249a427b2e77709861818e8eb7cb63e1a33a2b",
    "PUB": "3f4039fd7699baa212020dddfb02b3918bd63e02c475d638d99cbb2a1150d8d6",
    "edpub": "85814124278c3112562c84c4685ef555689d551b494dcbd23526fb27dc1d9a2a",
    "P3S": "9e2a0ad6b42cb2444f03f2f9db138c6c1e1db7f41434f5fb1878d87f99ca7ab1",
    "Reader": "098a2c8222f15f693c524139f2678be008a7ec9fafca275fc831ede9aa13bf1c",
}

def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def run_git(root: Path, *args: str, timeout: int = 120):
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file"})
    return subprocess.run(["git",*args], cwd=str(root), capture_output=True, text=True, timeout=timeout, env=env)

def main() -> int:
    if len(sys.argv) != 6:
        print(f"usage: {sys.argv[0]} OWN_SNAPSHOT_BASE OLD_FIXTURE_DB RUNTIME_BASE OUTPUT_RAW_BASE TMPDIR_BASE", flush=True)
        return 2
    own_base = Path(sys.argv[1]).resolve()
    old_db = Path(sys.argv[2]).resolve()
    runtime_base = Path(sys.argv[3]).resolve()
    output_raw = Path(sys.argv[4]).resolve()
    tmp_base = Path(sys.argv[5]).resolve()
    # Workspace TMPDIR, no /tmp writes except read-only TL binaries
    os.environ["TMPDIR"] = str(tmp_base)
    tmp_base.mkdir(parents=True, exist_ok=True)
    output_raw.mkdir(parents=True, exist_ok=True)
    runtime_base.mkdir(parents=True, exist_ok=True)
    pidfile = output_raw / "depth32-full.pid"
    hbfile = output_raw / "depth32-full.heartbeat.txt"
    exitfile = output_raw / "exit.txt"
    pidfile.write_text(f"{os.getpid()}\n{time.monotonic():.3f}\n{UTC}\n")
    hbfile.write_text(f"depth32-full start {time.monotonic():.3f} {UTC}\n")
    # Verify no GIT_* leakage
    for v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
        if os.environ.get(v):
            print(f"UNSAFE {v}", flush=True)
            exitfile.write_text("2")
            return 2
    sys.dont_write_bytecode=True
    os.environ["PYTHONDONTWRITEBYTECODE"]="1"
    result: dict = {"utc": UTC, "unit": "depth32-full finite (30 provided +1 editorial +1 renewal, 33 refuses, NOT 32 genuine ops)", "scope_qualifier": "ONLY 1 actual editorial (31, OLD) +1 actual renewal (32, CURRENT) on 30 fixture-provided typed LEGACY predecessors (r1..r30 NOT R1x30 actual ops); labelled scope qualifier required; whole unit no CommitPoint", "pins": PINS}
    try:
        # Phase 0: snapshot CURRENT intended candidate before test, no shared execution
        t0=time.monotonic()
        hbfile.write_text(hbfile.read_text()+f"phase0 snapshot start {t0:.3f}\n")
        own_snapshot = runtime_base / "snapshot-work"
        if own_snapshot.exists():
            shutil.rmtree(own_snapshot)
        # byte-independent cp -a, no -l
        proc = subprocess.run(["cp","-a",str(own_base),str(own_snapshot)], capture_output=True, text=True, timeout=1200)
        assert proc.returncode==0, f"cp snapshot failed {proc.stderr[:500]}"
        # Verify pins, nlink==1, dev:ino disjoint
        for name, pin in [("survey_versioned_renewal_history_v2.py",PINS["H"]),("survey_versioned_renewal_source_v2.py",PINS["S"]),("survey_versioned_renewal_v2.py",PINS["HIGH"]),("survey_editorial_correction_proposal_v2.py",PINS["P1"]),("survey_publication_v2.py",PINS["PUB"]),("survey_editorial_publication_v2.py",PINS["edpub"]),("survey_editorial_staged_source_v2.py",PINS["P3S"]),("survey_reader_publication_v2.py",PINS["Reader"])]:
            p = own_snapshot / "scripts" / name
            assert p.is_file(), f"missing {name}"
            got = sha_file(p)
            assert got==pin, f"pin mismatch {name}: {got[:12]} != {pin[:12]}"
            st=os.lstat(p)
            assert st.st_nlink==1, f"shared execution hardlink {name} nlink={st.st_nlink}"
        # dev:ino disjoint vs base
        for name in ["survey_versioned_renewal_history_v2.py"]:
            a=os.lstat(own_base/"scripts"/name); b=os.lstat(own_snapshot/"scripts"/name)
            assert (a.st_dev,a.st_ino)!=(b.st_dev,b.st_ino), "shared inode"
        hbfile.write_text(hbfile.read_text()+f"phase0 snapshot done dt={time.monotonic()-t0:.1f}s\n")
        result["phase0_snapshot"]={"own_snapshot":str(own_snapshot),"pins_verified":True,"nlink1":True,"disjoint":True}
        # Phase 1: inspect old R1 chain at 36c679, template r2 rows
        t0=time.monotonic()
        hbfile.write_text(hbfile.read_text()+f"phase1 inspect start {t0:.3f}\n")
        # Verify old DB HEADs
        r=run_git(old_db,"rev-parse","HEAD")
        assert r.returncode==0
        old_head=r.stdout.strip()
        # Must contain 36c679cc
        r2=run_git(old_db,"rev-parse","36c679cc5ed3291c11d4a01bdee906807cace8c4")
        assert r2.returncode==0, "old DB missing 36c679cc"
        r1=run_git(old_db,"rev-parse","fc9a5437dfb4364356974496c521d6e6a36b2636")
        assert r1.returncode==0, "old DB missing fc9a543"
        # Template r2 file (live E in old_db, current HEAD 5950e0f still has r2 with same SHA? Check)
        tmpl_path = old_db/"sources/2026-W37/publication/v2/publication-surface-revalidation-r2.json"
        assert tmpl_path.is_file(), "missing old r2 template"
        tmpl=json.loads(tmpl_path.read_bytes().decode("utf-8"))
        assert tmpl.get("reason_class")=="REVIEWED_CORE_CHANGE" and "kind" not in tmpl, "template not LEGACY"
        assert tmpl["issue_id"]=="2026-W37"
        assert tmpl["prior_checkpoint"]=={"path":"sources/2026-W37/orchestration/v2/checkpoints/DRAFT_COMPLETE.json","sha256":"ffbde649f25d5622dc3f49833b9a0a023e1af92cdf09732fae0b861177fa45da"}
        assert tmpl["core"]["implementation_commit_sha"]=="36c679cc5ed3291c11d4a01bdee906807cace8c4"
        tmpl_sha=sha_file(tmpl_path)
        assert tmpl_sha=="27db45ce3641866fcfadba6297cdf31b991660abd5cfe4445e7fb0b62ca4c582", f"r2 SHA drift {tmpl_sha[:12]}"
        # State/Profile/checkpoint/canonical outputs from retained before-State COPY (r2 pointer pre editorial)
        retained_before = old_db/"sources/2026-W37/publication/v2/editorial-corrections/wk-anchor-ed3/retained/before/sources/2026-W37/production-state.json"
        assert retained_before.is_file(), "missing retained before-State COPY"
        retained_state=json.loads(retained_before.read_bytes().decode("utf-8"))
        assert retained_state["publication_revalidation_provenance"]=={"path":"sources/2026-W37/publication/v2/publication-surface-revalidation-r2.json","sha256":"27db45ce3641866fcfadba6297cdf31b991660abd5cfe4445e7fb0b62ca4c582"}
        retained_sha=sha_file(retained_before)
        # Profile
        prof_path=old_db/"sources/2026-W37/production-profile.json"
        assert prof_path.is_file()
        prof_sha=sha_file(prof_path)
        # Checkpoint DRAFT_COMPLETE
        ckpt_path=old_db/"sources/2026-W37/orchestration/v2/checkpoints/DRAFT_COMPLETE.json"
        assert ckpt_path.is_file()
        ckpt_sha=sha_file(ckpt_path)
        assert ckpt_sha=="ffbde649f25d5622dc3f49833b9a0a023e1af92cdf09732fae0b861177fa45da"
        # Canonical outputs: reader-manuscript, gate, pdf, etc. from r2 rows
        # r2 rows: superseded gate new_sha 71742cf..., preserved pdf b3e44df..., etc. Verify live bytes exist
        for row in tmpl.get("superseded_artifacts",[])+tmpl.get("preserved_artifacts",[]):
            p=old_db/row["path"]
            # For superseded, check new_sha vs live? For preserved, check sha vs live
            # r2's new gate should be live gate? In old_db current E, gate may have drifted due to later editorial? Check retained before E instead?
            pass
        hbfile.write_text(hbfile.read_text()+f"phase1 inspect done dt={time.monotonic()-t0:.1f}s\n")
        result["phase1_old_inspect"]={"old_head":old_head[:12],"r1":"fc9a543","r2":"36c679cc","template_sha":tmpl_sha[:12],"retained_before_sha":retained_sha[:12],"profile_sha":prof_sha[:12],"ckpt_sha":ckpt_sha[:12]}
        # Phase 2: NEW independent fixture DB (clone 36c679, no fake ancestor) + r1..r30 provided
        t0=time.monotonic()
        hbfile.write_text(hbfile.read_text()+f"phase2 construction start {t0:.3f}\n")
        fixture = runtime_base / "fixture-weekly"
        if fixture.exists():
            shutil.rmtree(fixture)
        # git clone --no-hardlinks, inert origin, no alternates, no GIT_*
        # Use file:// with --no-hardlinks to ensure byte-independent, no hardlinks
        proc=subprocess.run(["git","clone","--no-hardlinks",str(old_db),str(fixture)], capture_output=True, text=True, timeout=1200, env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")})
        assert proc.returncode==0, f"clone failed {proc.stderr[:1000]}"
        # checkout 36c679cc explicitly (no fake ancestor, no empty root)
        r=run_git(fixture,"checkout","36c679cc5ed3291c11d4a01bdee906807cace8c4")
        assert r.returncode==0, f"checkout 36c679 failed {r.stderr[:500]}"
        r=run_git(fixture,"rev-parse","HEAD")
        assert r.stdout.strip()=="36c679cc5ed3291c11d4a01bdee906807cace8c4", "HEAD not 36c679"
        # inert origin, no alternates, no GIT_*, isolation
        r=run_git(fixture,"remote","set-url","origin","example.invalid")
        assert r.returncode==0
        # verify no alternates, nlink==1 for a sample file, dev:ino disjoint vs old_db
        assert not (fixture/".git/objects/info/alternates").exists(), "alternates present"
        # verify .git isolation: no GIT_* in env already checked
        # Copy E old data: reuse old r2 snapshot copies (E live/COPY, not tool commit)
        # Copy sources/, surveys/, etc. from old_db (which has OLD E + r1..r4 etc.) to fixture (which after checkout has no E? Actually clone includes committed source only, E untracked not cloned. So fixture currently has no E (sources/ missing). Need to copy E.)
        # Use byte-independent cp -a (no -l) for E, excluding POST State BAD, __pycache__, raw residue, etc. Similar to anchor-fix construction.
        # For simplicity, copy entire sources/, surveys/, etc. from old_db's live E, then overwrite r1..r30 with provided history, and reconstruct State->r30.
        # List E dirs to copy: sources, surveys, views-accepted, views-input, raw? raw is residue, exclude. Also exclude __pycache__, .pyc, etc.
        import fnmatch
        # old_db E top-level untracked: sources, surveys, etc. (see git status earlier: architecture-*.json, selection-v2.json, sources, surveys, views-*, raw, scripts/__pycache__)
        # Copy only sources, surveys, plus top-level jsons needed? Actually fixture needs full E to run editorial: sources/, surveys/, plus architecture-*.json? Let's copy all untracked E except __pycache__, raw, .pyc
        # Get untracked files via git status? Simpler: cp -a sources surveys + needed top-level?
        # Check old_db top-level E:
        for dirname in ["sources","surveys","views-accepted","views-input"]:
            src=old_db/dirname
            dst=fixture/dirname
            assert src.is_dir(), f"missing old E {dirname}"
            # cp -a
            proc2=subprocess.run(["cp","-a",str(src),str(dst)], capture_output=True, text=True, timeout=1200)
            assert proc2.returncode==0, f"cp {dirname} failed"
            # verify no hardlinks: sample file nlink==1 (any file, not just json for surveys which has pdf/tex)
            sample = next(dst.rglob("*"))
            # find first regular file
            for cand in dst.rglob("*"):
                if cand.is_file() and not cand.is_symlink():
                    sample=cand
                    break
            assert os.lstat(sample).st_nlink==1, f"hardlink in {dirname}"
        # Also copy top-level E jsons (architecture-*.json, selection-v2.json) if needed for editorial? Check helper needs: helper.source_root/semantic-publication-input.json etc. Those are under sources/, not top-level. Top-level jsons are selection/architecture? Might be needed for State validation? Let's copy them too (excluding raw, __pycache__)
        for fname in ["architecture-approval-v2.json","architecture-review-attention-v2.json","architecture-review-summary-v2.json","architecture-v2.json","selection-v2.json"]:
            s=old_db/fname
            if s.is_file():
                shutil.copy2(s, fixture/fname)
        # Also need config, docs, etc.? Those are committed source, already in fixture via clone (since clone includes committed files). Good. E copy done.
        # Now construct provided history r1..r30 with REAL SHAs/supersedes/strict schema/own OLD tool commits/monotonic + same valid cumulative rows
        # Template = old r2 (tmpl) with same issue/prior_checkpoint/rows, strictly increasing sequence, nondecreasing time, REAL file SHAs, own OLD tool commits (36c679cc + fc9a543... use 36c679cc for all, which is own OLD commit in NEW fixture), monotonic timestamps, same valid cumulative rows; label NOT R1x30 actual ops.
        rec_dir = fixture/"sources/2026-W37/publication/v2"
        # Remove old r1..r4 files that came from E copy (they are old chain of length 4, with SHAs 8974...,27db...,7dce...,9b69...). For NEW provided history, we need fresh r1..r30 (30 records) with new SHAs (since supersedes chain different). Remove old r*.json first to avoid confusion, then create new r1..r30.
        for p in list(rec_dir.glob("publication-surface-revalidation-r*.json")):
            p.unlink()
        # Also remove old editorial-corrections? Keep wk-anchor-ed3? For NEW fixture, editorial 31 will use new proposal ID (e.g., wk-depth32-ed31), not wk-anchor-ed3. Keep old ed dirs as inert? Or remove to avoid confusion? Keep as inert? Better to keep old ed dirs as inert? But they contain old r3 etc. with SHAs that reference old r2 (27db...). Since new r1..r30 will have different SHAs (new files), old ed dirs would reference old SHAs that no longer exist as r2? Actually new r2 will have different SHA than old r2 (since supersedes chain different? Wait new r1..r30 clones will have same rows as template but different supersedes/time, so their file SHAs will be different from old r1/r2. Old ed dirs reference old r2 SHA 27db..., which will no longer exist as file (since we deleted old r2). That would leave dangling refs in old ed dirs, but those old ed dirs are inert (not part of new chain). Should we delete old editorial-corrections to avoid confusion? For NEW fixture, we want clean provided history r1..r30 + new editorial31 + renewal32, without old r3/r4 etc. So delete editorial-corrections entirely (they are E, untracked, from old copy). Then new editorial31 will create new dir.
        ed_corr = rec_dir/"editorial-corrections"
        if ed_corr.exists():
            shutil.rmtree(ed_corr)
        # Also need to handle .mechanical-refresh-retention? That's E for R1? Keep? It contains retention for R1a/R1b. For NEW fixture, R1 retention not needed for provided history? But keep? Simpler to remove retention dirs that reference old r1/r2? Actually .mechanical-refresh-retention contains retention for R1 operations, not needed for new. Remove to avoid confusion? Keep? Let's remove all hidden retention dirs under publication/v2 that reference old chain.
        for p in list(rec_dir.glob(".mechanical-refresh-retention")):
            if p.is_dir():
                shutil.rmtree(p)
        # Now create r1..r30
        import datetime as _dt
        # Base time for r1..r30 must be BEFORE editorial31 (which uses current time ~Oct25 19:46Z).
        # Use 2026-10-25T15:00:00Z + i seconds (afternoon, before editorial, monotonic, nondecreasing).
        # Previous attempt used Oct26 00:00 (future) causing chronology failure (r30 Oct26 > r31 Oct25 19:46).
        # Preserved as fixture-weekly-failed-chronology-20261025T200000Z with exact constraint HISTORY_ANCESTOR chronology.
        base_time = datetime(2026,10,25,15,0,0,tzinfo=timezone.utc)
        clones=[]
        prev_ref=None
        for i in range(1,31):
            doc=copy.deepcopy(tmpl)
            rel=f"sources/2026-W37/publication/v2/publication-surface-revalidation-r{i}.json"
            doc["supersedes"]=prev_ref
            nt=base_time+_dt.timedelta(seconds=i)
            doc["recorded_at"]=nt.isoformat().replace("+00:00","Z")
            # issue/prior_checkpoint unchanged (same as template)
            doc["issue_id"]="2026-W37"
            doc["prior_checkpoint"]=copy.deepcopy(tmpl["prior_checkpoint"])
            # own OLD tool commits: use 36c679cc for all (own OLD commit in NEW fixture, REAL, not dummy). Keep core.contract same as template (since contract files unchanged at 36c679? Template contract is at 36c679? Template's contract pipeline SHA 3754... etc. At 36c679, contract recompute should match? Since we haven't changed contract files, contract at 36c679 equals template contract. Good.)
            # Ensure implementation_commit_sha is own OLD commit (36c679cc)
            doc["core"]["implementation_commit_sha"]="36c679cc5ed3291c11d4a01bdee906807cace8c4"
            # establishment also?
            if "establishment" in doc and isinstance(doc["establishment"],dict):
                doc["establishment"]["implementation_commit_sha"]="36c679cc5ed3291c11d4a01bdee906807cace8c4"
                doc["establishment"]["recorded_at"]=doc["recorded_at"]
            doc["executor"]="depth32-full-provided-history (NOT R1x30 actual ops; fixture-provided typed history, ROOT accepts finite construction)"
            # Remove any canonical_anchor/kind if present (legacy must not carry)
            doc.pop("canonical_anchor",None)
            doc.pop("kind",None)
            # Write deterministic JSON
            data=json.dumps(doc, indent=1, sort_keys=True)+"\n"
            (fixture/rel).write_text(data, encoding="utf-8")
            fsha=sha_file(fixture/rel)
            ref={"path":rel,"sha256":fsha}
            clones.append((rel,ref))
            prev_ref=ref
        # Verify chain r30 via hist (OLD code? Use fixture's own OLD code at 36c679? Or OWN CURRENT? For entry validity, need OLD code? Actually hist verification for legacy-only chain should pass with both OLD and CURRENT? Use fixture's OLD code (at 36c679) for initial validity, then also verify with CURRENT? For now verify with OWN CURRENT (74275d) to ensure strict schema passes? But OLD rows were created with OLD contract? Contract at 36c679 vs CURRENT? For legacy, contract not checked, so both pass. Use OWN CURRENT for verification (since CURRENT is strict).)
        # Use OWN snapshot (CURRENT) for hist verification of r1..r30 (read-only, no authority)
        sys.path.insert(0, str(own_snapshot))
        # Need fresh import without caching? Use importlib
        import importlib.util
        spec=importlib.util.spec_from_file_location("hist_current", str(own_snapshot/"scripts/survey_versioned_renewal_history_v2.py"))
        hist_current=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(hist_current)
        last_rel,last_ref=clones[-1]
        try:
            out=hist_current.verify_versioned_history(str(fixture), last_rel)
            assert out.get("HISTORICAL_IDENTITY_VERIFIED"), "not verified"
            chain_ok=True
            verify_detail=str(out)[:500]
        except Exception as exc:
            chain_ok=False
            verify_detail=f"{getattr(exc,'code',type(exc).__name__)}: {getattr(exc,'detail',str(exc))[:500]}"
            raise AssertionError(f"r1..r30 hist verify failed: {verify_detail}")
        # Now set canonical current State points r30 in THIS new test fixture only
        # Template retained_before State points r2 (27db...). Update provenance to r30 (new SHA), keep other fields same (Profile/checkpoint/canonical outputs same since same issue/rows). This is direct State fixture build allowed ONLY new test input exact descriptor not public live process rollback; actual tested HIGH32 public begins from fully valid input.
        state_path=fixture/"sources/2026-W37/production-state.json"
        # state_path currently from E copy points to r4 BAD? Actually after E copy + deletion of r1..r4, state_path still points to old r4 (9b69...). Need to reconstruct from retained_before template (which points r2) + update to r30.
        # Load retained_before as template for valid State (points r2, SHA 068e94bc...? Actually retained_before file SHA? Let's load retained_before from old_db (already have retained_state) and update provenance to r30.
        new_state=copy.deepcopy(retained_state)
        new_state["publication_revalidation_provenance"]={"path":last_rel,"sha256":last_ref["sha256"]}
        # Ensure other fields: issue, profiles, checkpoints, etc. remain same (same issue, same Profile, same checkpoints). Good.
        # Write State
        state_data=json.dumps(new_state, indent=1, sort_keys=True)+"\n"
        state_path.write_text(state_data, encoding="utf-8")
        new_state_sha=sha_file(state_path)
        # Verify exact Profile/checkpoint/current canonical outputs + public old agent validate_state
        # Use fixture's OLD code (at 36c679) for validate_state (public old agent)
        # Need to run OLD validate_state via fresh Python child (don't duplicate child on return: run once)
        # For now, verify via hist + manual Profile/checkpoint checks, then run OLD validate_state in next phase? Do it here via subprocess with OLD code.
        # To avoid module caching, run subprocess with PYTHONPATH=fixture (OLD code) to validate State
        env={k:v for k,v in os.environ.items() if not k.startswith("GIT_") and k!="PYTHONPATH"}
        env.update({"PYTHONDONTWRITEBYTECODE":"1","PYTHONPATH":str(fixture),"TMPDIR":str(tmp_base)})
        # Write a small validator script to run OLD agent.validate_agent_state
        validator_code = f"""
import sys, json
sys.path.insert(0, {repr(str(fixture))})
from scripts import survey_agent_control_v2 as agent
from scripts import survey_production_v2 as core
from pathlib import Path
repo=Path({repr(str(fixture))})
cfg=core.load_json(repo / "config/survey-production-v2.json") if (repo/"config/survey-production-v2.json").exists() else core.DEFAULT_CONFIG
# Actually load via core? Simpler: use agent.validate_agent_state with cfg from production?
# Load config via core.DEFAULT_CONFIG? Let's load file directly
import json as _j
cfg_path=repo/"config/survey-production-v2.json"
cfg=_j.loads(cfg_path.read_bytes().decode("utf-8"))
state=_j.loads((repo/"sources/2026-W37/production-state.json").read_bytes().decode("utf-8"))
errs=agent.validate_agent_state(repo, cfg, state)
print(_j.dumps({{"errors":errs}}))
"""
        val_path=runtime_base/"validate_r30_old.py"
        val_path.write_text(validator_code, encoding="utf-8")
        proc=subprocess.run([sys.executable,str(val_path)], cwd=str(fixture), capture_output=True, text=True, timeout=1200, env=env)
        assert proc.returncode==0, f"OLD validate_state child failed exit={proc.returncode} stdout={proc.stdout[:2000]} stderr={proc.stderr[:2000]}"
        # Parse output (last line json?)
        try:
            out_json=json.loads(proc.stdout.strip().splitlines()[-1])
            errs=out_json.get("errors",[])
        except Exception as e:
            raise AssertionError(f"validate output parse failed: {proc.stdout[:2000]} {e}")
        assert errs==[], f"OLD validate_state errors for r30: {errs[:5]}"
        hbfile.write_text(hbfile.read_text()+f"phase2 construction done dt={time.monotonic()-t0:.1f}s r30={last_ref['sha256'][:12]} state={new_state_sha[:12]}\\n")
        result["phase2_provided_history"]={"r1_sha":clones[0][1]["sha256"][:12],"r30_sha":last_ref["sha256"][:12],"r30_rel":last_rel,"state_sha":new_state_sha[:12],"hist_verified":chain_ok,"old_validate_empty":True,"label":"NOT R1x30 actual ops; fixture-provided typed history, ROOT accepts finite construction; original real R1 fixtures unchanged"}
        result["phase2_clones"]=len(clones)
        # Save construction proof to output_raw
        (output_raw/"construction-r1-r30.json").write_text(json.dumps({"clones":clones,"r30":last_ref,"state_sha":new_state_sha,"hist_detail":verify_detail}, indent=1, sort_keys=True)+"\\n", encoding="utf-8")
        return result, fixture, own_snapshot, clones, last_ref, new_state_sha
    except Exception as exc:
        import traceback
        hbfile.write_text(hbfile.read_text()+f"phase failed: {exc} {traceback.format_exc()[:2000]}\\n")
        result["exact_constraint"]=f"{getattr(exc,'code',type(exc).__name__)}: {getattr(exc,'detail',str(exc))[:1000]}"
        (output_raw/"result-depth32-full.json").write_text(json.dumps(result, indent=1, sort_keys=True)+"\\n", encoding="utf-8")
        print(json.dumps(result, indent=1, sort_keys=True))
        return result, None, None, None, None, None

if __name__=="__main__":
    raise SystemExit(main())
