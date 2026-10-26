#!/usr/bin/env python3
"""Read-only diagnosis of r4 anchor defect (no mutation of old fixture).

Old fixture: versioned-renewal-r1-anchor-20261025T150000Z/anchor-weekly
(PRESERVE UNTOUCHED, no rollback/patch). New code: candidate-work with fix
(HIGH 1dad, H 7427, S 2290). This script only READS old fixture + new source
pins, writes evidence to NEW r1-anchor-correction/ dir. No writes to old
fixture, no State patch, no cleanup. PYTHONDONTWRITEBYTECODE=1 required.
"""
import hashlib
import json
import os
import sys
from pathlib import Path

def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main() -> int:
    repo_root = Path(__file__).resolve().parents[4]
    old_root = repo_root / ".rephase-1-editorial-runtime/versioned-renewal-r1-anchor-20261025T150000Z/anchor-weekly"
    cand_root = repo_root / ".rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work"
    out_dir = repo_root / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/r1-anchor-correction/raw/diagnose-20261025T200000Z"
    out_dir.mkdir(parents=True, exist_ok=True)
    pid = os.getpid()
    (out_dir / "pid.txt").write_text(str(pid) + "\n")
    log = []
    def emit(s: str) -> None:
        print(s)
        log.append(s)
    emit(f"PID {pid}")
    emit(f"old_root {old_root} exists={old_root.exists()}")
    emit(f"cand_root {cand_root} exists={cand_root.exists()}")
    # Source pins (new fixed code)
    for rel in [
        "scripts/survey_versioned_renewal_v2.py",
        "scripts/survey_versioned_renewal_history_v2.py",
        "scripts/survey_versioned_renewal_source_v2.py",
        "scripts/survey_publication_set_v2.py",
        "scripts/survey_agent_control_v2.py",
    ]:
        p = cand_root / rel
        emit(f"CAND {rel} sha={sha_file(p)[:8]} size={p.stat().st_size}")
    # Old fixture State + records (read-only)
    state_rel = "sources/2026-W37/production-state.json"
    state_data = (old_root / state_rel).read_bytes()
    emit(f"OLD State sha={hashlib.sha256(state_data).hexdigest()} size={len(state_data)}")
    state = json.loads(state_data)
    emit(f"OLD State pointer={state.get('publication_revalidation_provenance')}")
    for n in ["r1", "r2", "r3", "r4"]:
        rel = f"sources/2026-W37/publication/v2/publication-surface-revalidation-{n}.json"
        p = old_root / rel
        if not p.exists():
            emit(f"OLD {n} MISSING")
            continue
        d = json.loads(p.read_bytes())
        emit(f"OLD {n} sha={sha_file(p)} supersedes={d.get('supersedes')} anchor={d.get('canonical_anchor')} kind={d.get('kind')} reason={d.get('reason_class')}")
    # Basis anchor (old bad)
    basis_rel = "sources/2026-W37/publication/v2/editorial-corrections/wk-anchor-ed3/renewals/high-u1-anchor-weekly/renewal-basis.json"
    basis = json.loads((old_root / basis_rel).read_bytes())
    emit(f"OLD basis anchor={basis.get('canonical_anchor')} prior_record={basis.get('prior_record_ref')} before_state={basis.get('before_state_ref')}")
    # Retained COPY (PRE-activation State, controlled construction source)
    retained_rel = str(basis.get("retained_copy_ref", {}).get("path", ""))
    retained_data = (old_root / retained_rel).read_bytes() if retained_rel else b""
    emit(f"OLD retained COPY {retained_rel} sha={hashlib.sha256(retained_data).hexdigest() if retained_data else 'MISSING'} size={len(retained_data) if retained_data else 0}")
    if retained_data:
        retained_state = json.loads(retained_data)
        emit(f"OLD retained State pointer={retained_state.get('publication_revalidation_provenance')}")
        # Verify retained COPY equals before_state_ref
        before_ref = basis.get("before_state_ref", {})
        emit(f"OLD retained vs before_state match={hashlib.sha256(retained_data).hexdigest() == before_ref.get('sha256')}")
    # Live gate vs original vs r2
    gate_data = (old_root / "sources/2026-W37/publication/v2/reader-surface-gate-v2.json").read_bytes()
    emit(f"OLD live gate sha={hashlib.sha256(gate_data).hexdigest()}")
    draft = json.loads((old_root / "sources/2026-W37/orchestration/v2/checkpoints/DRAFT_COMPLETE.json").read_bytes())
    for row in draft.get("artifacts", []):
        if row.get("name") == "reader-surface-gate":
            emit(f"OLD original gate {row}")
    r2 = json.loads((old_root / "sources/2026-W37/publication/v2/publication-surface-revalidation-r2.json").read_bytes())
    for row in r2.get("superseded_artifacts", []) + r2.get("preserved_artifacts", []):
        if row.get("name") == "reader-surface-gate":
            emit(f"OLD r2 gate row {row}")
    (out_dir / "diagnosis.txt").write_text("\n".join(log) + "\n")
    (out_dir / "exit.txt").write_text("0\n")
    return 0

if __name__ == "__main__":
    sys.exit(main())
