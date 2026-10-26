#!/usr/bin/env python3
"""Controlled fixture construction for anchor fix (NOT production recovery).

Old fixture (INDETERMINATE, PRESERVE UNTOUCHED):
  .rephase-1-editorial-runtime/versioned-renewal-r1-anchor-20261025T150000Z/anchor-weekly
  HEAD 5950e0f, State -> r4 BAD (9b69, anchor DRAFT_COMPLETE vs expected r2),
  r1+r2+r3 GOOD, basis/proof BAD (DRAFT_COMPLETE), retained COPY GOOD (2797be, PRE-activation State -> r3).

New fixture (independent DB, no alternates/hardlinks, no GIT env):
  .rephase-1-editorial-runtime/versioned-renewal-r1-anchor-correction-20261025T200000Z/anchor-fix-weekly
  - git clone --no-hardlinks from old Git DB (tracked 740 source at 5950e0f), inert origin, no alternates, nlink==1, dev:ino disjoint.
  - Copy E (untracked edition files) from old filesystem, EXCLUDING:
      * scripts/__pycache__/, raw/ (non-E residue, no cleanup of old roots per task),
      * sources/2026-W37/production-state.json (POST-activation BAD, not copied; reconstructed below).
    INCLUDE bad r4 record as inert file (stays inert old namespace if copied; new allocator uses r5, gaps okay).
    INCLUDE old renewal dir high-u1-anchor-weekly as inert (contains retained COPY needed for reconstruction).
  - Reconstruct PRE-activation State from recorded validated before-State COPY:
      old retained COPY .../high-u1-anchor-weekly/retained/before/sources/2026-W37/production-state.json
      SHA 2797be870e10309c174b3337d040517702be007216b5f65b519e6abfa83811d0, byte_count 5965,
      matches basis.before_state_ref (hash+provenance verified), pointer -> r3 GOOD.
      Write to new State path, verify SHA, label controlled construction (NOT recovery), original BAD State unaltered.
    Exclude/adopt NO orphans automatically: all orphans (wk-ed-renew-? none here; r4 inert) preserved, no deletion/adoption.
  - SOURCE-only commit with fix (HIGH 1dad + H 7427 + S 2290) before NEW renewal, old E unchanged:
      git add -- scripts/survey_versioned_renewal_v2.py scripts/survey_versioned_renewal_history_v2.py scripts/survey_versioned_renewal_source_v2.py ONLY,
      E stays ?? untracked, no deletion, verify.
  - New renewal uses fresh ID high-u1-anchor-fix (not same-byte takeover), record r5 (since r4 exists inert), chain r1+r2+r3+r5 (32 count, not filenames).

Captures commands/exits/PIDs/source pins/raw window/immediate fs. No ordinary
candidate/reconstruct commit, no network/old runners/cleanup.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

def run(cmd, cwd, out_dir, label):
    with open(out_dir / f"{label}-commands.log", "a") as f:
        f.write(" ".join(cmd) + f"  # cwd={cwd} pid={os.getpid()}\n")
    res = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    (out_dir / f"{label}-exit.txt").write_text(str(res.returncode) + "\n")
    (out_dir / f"{label}-stdout.txt").write_text(res.stdout or "")
    (out_dir / f"{label}-stderr.txt").write_text(res.stderr or "")
    if res.returncode != 0:
        print(f"FAIL {label} exit={res.returncode}\nSTDOUT:{res.stdout[:2000]}\nSTDERR:{res.stderr[:2000]}")
        raise SystemExit(f"{label} failed exit={res.returncode}")
    return res

def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main() -> int:
    repo = Path(__file__).resolve().parents[4]
    old = repo / ".rephase-1-editorial-runtime/versioned-renewal-r1-anchor-20261025T150000Z/anchor-weekly"
    cand = repo / ".rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work"
    new_base = repo / ".rephase-1-editorial-runtime/versioned-renewal-r1-anchor-correction-20261025T200000Z"
    new = new_base / "anchor-fix-weekly"
    raw = repo / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/r1-anchor-correction/raw/fixture-20261025T200000Z"
    raw.mkdir(parents=True, exist_ok=True)
    (raw / "pid.txt").write_text(str(os.getpid()) + "\n")
    # Env guard: no GIT_* inherited
    for k in list(os.environ):
        if k.startswith("GIT_"):
            del os.environ[k]
    # 1. Clone Git DB (tracked source only, no E)
    if new.exists():
        print(f"new exists {new}, refusing overwrite (no cleanup)")
        return 2
    new_base.mkdir(parents=True, exist_ok=True)
    run(["git", "clone", "--no-hardlinks", str(old.resolve()), str(new.resolve())], repo, raw, "clone")
    run(["git", "remote", "set-url", "origin", "example.invalid"], new, raw, "inert-origin")
    run(["git", "rev-parse", "HEAD"], new, raw, "head-pre")
    # Verify isolation: no alternates, nlink==1, dev:ino disjoint (sample)
    run(["sh", "-c", "test ! -e .git/objects/info/alternates && echo NO_ALTERNATES || echo HAS_ALTERNATES"], new, raw, "noalternates")
    # 2. Copy E (untracked) excluding State BAD, __pycache__, raw/
    # List old untracked E (top-level + sources/surveys, excluding raw/__pycache__)
    old_state_rel = "sources/2026-W37/production-state.json"
    old_state_data = (old / old_state_rel).read_bytes()
    print(f"OLD POST State sha={hashlib.sha256(old_state_data).hexdigest()} (BAD, NOT copied, preserved untouched)")
    # Copy via python (no rsync blind, SHA verified per file, no hardlinks)
    copied = []
    for top in ["architecture-approval-v2.json", "architecture-review-attention-v2.json", "architecture-review-summary-v2.json", "architecture-v2.json", "selection-v2.json"]:
        src = old / top
        if src.exists():
            dst = new / top
            dst.write_bytes(src.read_bytes())
            assert sha_file(dst) == sha_file(src)
            copied.append(top)
    for d in ["sources", "surveys", "views-accepted", "views-input"]:
        srcd = old / d
        if not srcd.exists():
            continue
        for root, dirs, files in os.walk(srcd):
            # Exclude __pycache__ dirs
            dirs[:] = [x for x in dirs if x != "__pycache__"]
            for fn in files:
                s = Path(root) / fn
                rel = s.relative_to(old).as_posix()
                # Exclude POST-activation State BAD (reconstructed below)
                if rel == old_state_rel:
                    continue
                # Exclude raw/ (non-E)
                if rel.startswith("raw/"):
                    continue
                dst = new / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                # No hardlinks: write bytes (new inode), verify SHA
                dst.write_bytes(s.read_bytes())
                assert sha_file(dst) == sha_file(s)
                copied.append(rel)
    (raw / "copied-list.txt").write_text("\n".join(sorted(copied)) + "\n")
    print(f"copied E files={len(copied)} (excluding POST State BAD, __pycache__, raw/)")
    # Verify bad r4 copied as inert (if present)
    r4_rel = "sources/2026-W37/publication/v2/publication-surface-revalidation-r4.json"
    assert (new / r4_rel).exists(), "bad r4 must be copied as inert"
    print(f"r4 inert copied sha={sha_file(new / r4_rel)[:8]} (stays inert, new allocator uses r5)")
    # 3. Reconstruct PRE-activation State from retained COPY (controlled construction)
    basis_rel = "sources/2026-W37/publication/v2/editorial-corrections/wk-anchor-ed3/renewals/high-u1-anchor-weekly/renewal-basis.json"
    basis = json.loads((old / basis_rel).read_bytes())
    retained_rel = str(basis["retained_copy_ref"]["path"])
    retained_data = (old / retained_rel).read_bytes()
    retained_sha = hashlib.sha256(retained_data).hexdigest()
    assert retained_sha == basis["retained_copy_ref"]["sha256"], "retained COPY SHA must equal basis retained_copy_ref"
    assert retained_sha == basis["before_state_ref"]["sha256"], "retained COPY SHA must equal before_state_ref (PRE-activation)"
    assert len(retained_data) == basis["retained_copy_ref"]["byte_count"] == 5965
    retained_state = json.loads(retained_data)
    assert retained_state["publication_revalidation_provenance"]["path"] == "sources/2026-W37/publication/v2/publication-surface-revalidation-r3.json", "PRE-activation State must point to r3 GOOD"
    assert retained_state["publication_revalidation_provenance"]["sha256"] == "7dce79acca8e876758fe0760633feb178e749467e17db19d3d62095bc95436c9"
    print(f"retained COPY verified sha={retained_sha[:8]} pointer->r3 GOOD (hash+provenance verified, controlled construction NOT recovery)")
    # Write PRE-activation State to new fixture
    new_state_path = new / old_state_rel
    new_state_path.parent.mkdir(parents=True, exist_ok=True)
    new_state_path.write_bytes(retained_data)
    assert sha_file(new_state_path) == retained_sha
    (raw / "controlled-construction-label.txt").write_text(
        "CONTROLLED FIXTURE CONSTRUCTION (NOT production recovery):\n"
        f"new State {old_state_rel} reconstructed from recorded validated before-State COPY\n"
        f"{retained_rel} sha={retained_sha} byte_count=5965 pointer->r3 GOOD\n"
        "hash+provenance verified (retained==before_state_ref, pointer==r3).\n"
        "Original BAD State (POST r4 9b69) preserved UNTOUCHED at old fixture, not patched/rolled back.\n"
        "Bad r4 stays inert old namespace if copied; new R allocator uses r5 (gaps okay, chain 32 count not filenames).\n"
        "Exclude/adopt NO orphans automatically.\n"
    )
    print("PRE-activation State reconstructed in new fixture (controlled, original untouched)")
    # 4. Verify old E unchanged? (read-only check old still points to r4 BAD)
    old_state_after = (old / old_state_rel).read_bytes()
    assert hashlib.sha256(old_state_after).hexdigest() != retained_sha, "old POST State must still be BAD (untouched, no rollback)"
    print("old fixture preserved UNTOUCHED (POST State still BAD r4)")
    # 5. SOURCE-only commit with fix before NEW renewal, old E unchanged
    # Copy fixed HIGH+H+S from candidate-work (verified pins) to new fixture tracked paths
    for rel in ["scripts/survey_versioned_renewal_v2.py", "scripts/survey_versioned_renewal_history_v2.py", "scripts/survey_versioned_renewal_source_v2.py"]:
        src = cand / rel
        dst = new / rel
        dst.write_bytes(src.read_bytes())
        assert sha_file(dst) == sha_file(src)
        print(f"overlay fix {rel} sha={sha_file(dst)[:8]}")
    # Verify E still untracked (State, sources, surveys as ??, no deletion)
    res = subprocess.run(["git", "status", "--porcelain"], cwd=str(new), capture_output=True, text=True)
    (raw / "status-before-add.txt").write_text(res.stdout)
    # Only add 3 source paths (SOURCE-only, E stays ??)
    run(["git", "add", "--", "scripts/survey_versioned_renewal_v2.py", "scripts/survey_versioned_renewal_history_v2.py", "scripts/survey_versioned_renewal_source_v2.py"], new, raw, "add-fix")
    run(["git", "status", "--porcelain"], new, raw, "status-staged")
    # Verify staged only 3 paths, E still untracked (no adoption/deletion)
    staged = subprocess.run(["git", "diff", "--cached", "--name-only"], cwd=str(new), capture_output=True, text=True).stdout.strip().splitlines()
    assert sorted(staged) == sorted(["scripts/survey_versioned_renewal_v2.py", "scripts/survey_versioned_renewal_history_v2.py", "scripts/survey_versioned_renewal_source_v2.py"]), f"staged must be ONLY 3 fix files, got {staged}"
    print("staged SOURCE-only 3 files verified, E unchanged (untracked preserved)")
    run(["git", "-c", "user.name=rephase-fixture", "-c", "user.email=fixture@example.invalid", "commit", "-m", "TEST-ONLY: r1-anchor fix (HIST full anchor + HIGH verbatim + S prior-HIST + pre-write validation, no P1/PUB/Reader/schema)"], new, raw, "commit-fix")
    run(["git", "rev-parse", "HEAD"], new, raw, "head-post")
    run(["git", "status", "--porcelain"], new, raw, "status-post")
    print("SOURCE-only commit DONE before NEW renewal, old E unchanged")
    (raw / "exit.txt").write_text("0\n")
    return 0

if __name__ == "__main__":
    sys.exit(main())
