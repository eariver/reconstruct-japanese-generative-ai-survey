#!/usr/bin/env python3
"""Boundary verification — 32/33 attempt via mixed legacy+editorial (bounded).

TEST-only, no product edits. OWN CURRENT 741 (HIGH 1dad1ad, H 74275d, S 2290ddd).
Read-only verify (hist.verify_versioned_history), no new authority, no source
commit, no State write, no new R. Fork byte-independent (cp -a, no -l) from
CURRENT base; synthetic records as untracked E (NOT committed, read-only test).

Goal (ROOT allows): finite valid TYPED predecessor history from real R3/renewal
artifact templates + genuine isolated tool commits/private builders, then public
HIGH 32nd admission succeeds and 33rd refuses before writes (R_FILES=0). Label
fixture-provided prior history != 32 real operator runs. All refs/digests/
epochs/retainedCopies/current closure/source outputs/review target paths must
be REAL consistent, no dummy SHA/stub HIGH/NoneCandidate/loose validators.

This bounded attempt tries: prior 31 = 30 legacy clones (from wk-boot-1 valid
legacy template, same issue/prior_checkpoint, strictly increasing sequence,
nondecreasing time, cumulative rows) + 1 editorial (R3 template, sequence 31,
anchor = latest legacy r30). Then hist.verify on r31 (31 valid?) and synthetic
r32 versioned? Actually to keep read-only and bounded, this probe ONLY checks
whether 30 cloned legacy + 1 editorial can form a valid 31-length chain for
hist.verify (using CURRENT H 74275d new full anchor). It does NOT run 31 full
public activations (WITHOUT claiming 32 actual full publication operations).

If unconstructible, return EXACT predicate (which check fails first, with
code/phase/detail), NOT just 'needs 32 real renewals'. Use old/new legacy
allowed history branch combination if fully valid models but counts not R1x32.

Existing R7 typed legacy 32/33 retained (NOT rerun here): R7 proves STATE
32-valid/33-refuses (API+CLI, typed legacy33, NOT actual R1x33). High-prepare-33
CURRENT retained (case-high-prepare-33-current-000400Z, ENTRY chain-too-deep,
no R, State unchanged — NOT rerun). This probe is for HIGH 32-valid (prior 31
-> new 32nd) feasibility, NOT duplicate.
"""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    own_src = Path(sys.argv[1]).resolve()
    work_fork = Path(sys.argv[2]).resolve()
    out_json = Path(sys.argv[3]).resolve()
    sys.path.insert(0, str(own_src))
    from scripts import survey_versioned_renewal_history_v2 as hist

    repo = work_fork.resolve()
    # Find wk-boot-1 valid legacy template: use r1/r2 from r1-anchor-correction?
    # Simpler: use CURRENT base's wk-boot-1 r1 (editorial? Actually wk-boot-1 has
    # r1 legacy? Let's discover existing revalidation records in fork).
    cands = sorted(repo.glob("sources/**/publication-surface-revalidation-r*.json"))
    base_info = [{"path": str(p.relative_to(repo).as_posix()), "sha": sha_file(p)[:12]} for p in cands[:10]]
    # Load one legacy record as template (first LEGACY kind, else first record).
    template = None
    template_rel = None
    for p in cands:
        try:
            doc = json.loads(p.read_bytes().decode("utf-8"))
        except Exception:  # noqa: BLE001
            continue
        # LEGACY has no kind, reason REVIEWED_CORE_CHANGE.
        if doc.get("reason_class") == "REVIEWED_CORE_CHANGE" and "kind" not in doc:
            template = doc
            template_rel = str(p.relative_to(repo).as_posix())
            break
    if template is None and cands:
        # Fallback: use first record as structural template (will likely fail
        # with exact predicate, which is the desired output if unconstructible).
        p = cands[0]
        template = json.loads(p.read_bytes().decode("utf-8"))
        template_rel = str(p.relative_to(repo).as_posix())

    result: dict = {
        "unit": "depth32-attempt-mixed-legacy-editorial (bounded, read-only, NOT 32 real ops)",
        "source_pins": {
            "HIGH": "1dad1ad12ba509c477ea97fb3a22e5156ae1627182f3286f373f32eae7ba2fbb",
            "H": "74275d22a342014009d5d090fbe9c552981941e90259c298065d2ba6929d1f3d",
        },
        "base_records": base_info,
        "template_rel": template_rel,
        "template_kind": ("LEGACY" if template is not None and "kind" not in template and template.get("reason_class") == "REVIEWED_CORE_CHANGE" else str((template or {}).get("kind"))),
    }
    if template is None:
        result.update({"constructible": False, "exact_predicate": "no revalidation record template found in fork (no base chain)", "code": "NO_TEMPLATE"})
        out_json.write_text(json.dumps(result, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=1, sort_keys=True))
        return 2

    # Attempt: clone template into r1..r30 legacy (same issue/prior_checkpoint,
    # same rows, increasing time/sequence, chained supersedes, recomputed SHAs).
    # Then check hist.verify on r30 (30-length) to see if even 30 legacy clones
    # pass. This reveals the exact first failing predicate without building full 31.
    try:
        issue = template.get("issue_id")
        prior_ckpt = template.get("prior_checkpoint")
        # Use template's recorded_at as base, increment by 1s per clone.
        from datetime import datetime as dt

        base_time = hist._parse_instant(str(template.get("recorded_at", "")))
    except Exception as exc:  # noqa: BLE001
        result.update({"constructible": False, "exact_predicate": f"template time/issue parse fails: {exc}", "code": "TEMPLATE_PARSE"})
        out_json.write_text(json.dumps(result, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=1, sort_keys=True))
        return 2

    # Determine parent dir for synthetic chain (same as template's dir).
    parent_dir = str(Path(template_rel).parent.as_posix())
    # Clean any prior synthetic attempt files (only our synthetic rN clones in a
    # dedicated subdir? To avoid colliding with real rN, use dedicated dir
    # <parent>/synth-depth32/ with r1..r30? But _parse_sequence requires filename
    # publication-surface-revalidation-rN.json (any parent? Yes, _parse_sequence
    # checks basename only, not parent. But chain walk uses supersedes refs with
    # exact paths, so dedicated subdir is allowed as long as refs are exact.
    # However, prior_checkpoint/issue must match, and before_active_digest chain
    # recompute uses prior_doc artifacts (same). Good: dedicated subdir isolates
    # from real chain, no overwrite of real rN.
    synth_dir = parent_dir + "/synth-depth32-attempt"
    (repo / synth_dir).mkdir(parents=True, exist_ok=True)
    # Build 30 clones.
    clones: list[tuple[str, dict]] = []
    prev_ref = None
    for i in range(1, 31):
        doc = copy.deepcopy(template)
        # Sequence filename r<i>.json in synth dir.
        rel = f"{synth_dir}/publication-surface-revalidation-r{i}.json"
        doc["supersedes"] = prev_ref
        # Increment time by i seconds.
        import datetime as _dt

        nt = base_time + _dt.timedelta(seconds=i)
        # Format as ISO with +00:00 (match template style if possible).
        doc["recorded_at"] = nt.isoformat()
        # Ensure issue/prior_checkpoint unchanged (same as template).
        doc["issue_id"] = issue
        doc["prior_checkpoint"] = copy.deepcopy(prior_ckpt)
        # Write with canonical JSON? Use repo's core.sha256_object? For history
        # records, FILE SHA is full serialized bytes; loader checks SHA drift via
        # ref SHA vs file bytes. We write bytes then ref SHA = file SHA (REAL
        # consistent, no dummy). No self-digest inside record? Records have no
        # self-digest field? They are validated via schema + before_active_digest
        # chain recompute, not self-digest. Good: write deterministic JSON.
        data = json.dumps(doc, indent=1, sort_keys=True) + "\n"
        (repo / rel).write_text(data, encoding="utf-8")
        fsha = sha_file(repo / rel)
        ref = {"path": rel, "sha256": fsha}
        # Update previous clone's supersedes? No, clones are built forward:
        # r1 supersedes None, r2 supersedes r1, etc. Since we built r<i> with
        # prev_ref = r<i-1> ref, but r<i-1> file was already written BEFORE r<i>
        # existed, r<i-1> file bytes do NOT include r<i> (correct, supersedes
        # points backwards). However, r<i> file includes supersedes = r<i-1> ref
        # with correct SHA (since r<i-1> already written). Good. But r<i-1> file
        # itself is already final (no need to update after r<i>). Good.
        clones.append((rel, ref))
        prev_ref = ref

    # Verify the 30-length synthetic chain (r30) via hist.verify (read-only).
    last_rel, last_ref = clones[-1]
    verify_code = None
    verify_detail = ""
    try:
        out = hist.verify_versioned_history(str(repo), last_rel)
        verify_code = "HISTORICAL_IDENTITY_VERIFIED"
        verify_detail = str(out)[:800]
        chain_ok_30 = True
    except Exception as exc:  # noqa: BLE001
        verify_code = getattr(exc, "code", None) or type(exc).__name__
        verify_detail = (getattr(exc, "detail", None) or str(exc))[:800]
        chain_ok_30 = False

    result.update(
        {
            "synth_dir": synth_dir,
            "clones": len(clones),
            "last_ref": last_ref,
            "verify_30_code": verify_code,
            "verify_30_detail": verify_detail,
            "chain_30_valid": bool(chain_ok_30),
        }
    )
    if chain_ok_30:
        result.update(
            {
                "constructible_30": True,
                "note": "30 cloned legacy pass hist.verify (same issue/prior_checkpoint/rows, increasing sequence/time, REAL SHAs). Next would need 1 editorial (sequence 31, anchor = latest legacy) + HIGH 32nd public activate (genuine Core epoch + full basis/proof/etc.) + 33rd prepare refuse. NOT executed here (bounded probe only 30 legacy). This does NOT claim 32 real ops; prior 30 are fixture-provided typed history (labeled), 32nd would be 1 real public op.",
                "exact_predicate": "none for 30 legacy (passes); remaining for 31st editorial + 32nd versioned: editorial must carry canonical_anchor == derived (latest legacy r30) + staged source OLD50/NEW63 generation must match owned epoch + before_active_digest chain recompute must pass + HIGH 32nd requires genuine eligible Core change (old/new tool commits + changed paths, artifact-only never qualifies, per contract S2) + fresh basis/COPY + full proof/receipt/build/QA/Gate/Candidate/seal with REAL consistent refs (no dummy). If editorial template anchor != r30, exact code is HISTORY_ANCESTOR anchor identity (same as N1-N4).",
            }
        )
    else:
        result.update(
            {
                "constructible": False,
                "exact_predicate": f"{verify_code}: {verify_detail}",
                "note": "Even 30 cloned legacy (same rows/issue/prior_checkpoint, REAL SHAs, increasing sequence/time) fail hist.verify at first predicate above. This is the exact blocker for mixed legacy+editorial 31-predecessor construction without regenerating rows against the same prior_checkpoint/artifacts. NOT just 'needs 32 real renewals'.",
            }
        )
    out_json.write_text(json.dumps(result, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=1, sort_keys=True))
    return 0 if chain_ok_30 else 2


if __name__ == "__main__":
    raise SystemExit(main())
