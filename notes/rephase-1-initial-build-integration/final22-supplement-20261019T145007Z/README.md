# Final22 supplement — BOTH stage Gate negatives + exclusive transfer + corrections — 20261019T145007Z

Answers the review return (`astra-integration-review-return.md` ALL6) and the
independent `§7` mandatory corrections. No source-code changes, no candidate/reconstruct
commits, no Production actions, no rebuilds (trio+recipe hash equality gates reuse of
real positive bytes), no full old-suite rerun. STOP at completion for fresh
author-independent resolution.

Tool disclosure: `apply_patch` absent. All code/doc edits via dedicated `Edit`/`Write`
except mechanical multi-line patches applied via `python3` heredocs in bash
(documented in `evidence-correction.md` §7, not repeated). New harness scripts were
saved BEFORE execution. No `git clean`/reset and no shell code-editing after the
final22 unit; failed-attempt fixtures/build dirs are preserved, never wiped
(`-supp…-supp5` lineage + `weekly-stage-orphan-unexplained` + attempt-suffixed evidence).

## 1. What this supplement adds (77 worker ops + 8 transfer controls)

On NEW source-only fixtures (`jgas-supplement-fixtures-…/{weekly,special}-supp5`,
SOURCE heads `51b0e42b…`/`9917a6ff…` = committed final22 heads; `git archive` tracked707
+ byte-copied `.git`, no generated authority, 22 pins verified, full `.git` dev:ino
independence, no alternates/hardlinks/persistent identity):
- Accepted chains → DRAFT_COMPLETE via actual producers (surfaces byte-identical to
  original21 pins `136c0dd8…` / `f40db7f6…957cd5`), synthetic type-only pretex reviews,
  actual pass2, trio hash-equal to recorded positive pins (no rebuild).
- REAL positive-run PDF/log/digest staged (hash-verified against recorded transfer pins)
  and transferred with the NEW exclusive helper (O_EXCL|O_NOFOLLOW, see §2).
  Weekly pdf `899f0f2a…` 61151 B / 5 pp; special `71a2c98a…` 79156 B / 5 pp.
  Log gates re-checked on staged bytes (workflow split preserved).
- Exact manuscript/Gate + receipt replays, deterministic QA bundle (3 weekly / 4 special,
  all genuine narrow predicates), synthetic postrender reviews, healthy DRAFT_COMPLETE
  advance (checkpoint saved) — then the two previously missing stage negatives:
  - NEG-S1 (DRAFT_COMPLETE advance with decoy manuscript + decoy reviews + exact gate):
    `StageValidationError: Reader-Surface Gate validation failed: … MANUSCRIPT_MANIFEST
    does not bind the exact expected Reader Manuscript: expected …-decoy-v2.json …
    got …reader-manuscript-v2.json …` (both routes). No-write verified (file-map + HEAD/status equal).
  - NEG-S2 (VALIDATED_DRAFT advance with decoy candidate):
    `StageValidationError: Publication Candidate does not bind exact reader_manuscript`
    (both routes). No-write verified.
  - Healthy VALIDATED_DRAFT advance → RELEASE_CANDIDATE + receipt/Gate (+surface for
    special) readbacks. STOP (no Preview/Freeze/Release here; positives covered them).
- Evidence packet: transferred PDF/log/digest hash-equal copies, extracted text,
  per-page PNGs (5+5), pins, checkpoints, raw CLI/stage outputs.

Decoy recipe mirrors the real ones: LF `test_gate_and_both_admission_backstops`
(negative DRAFT_COMPLETE advance 131 → healthy 130; decoy candidate 132 → healthy 133)
and Increment-A `test_validated_draft_rejects_valid_same_identity_alternate_manuscript`
(same-issue alternate manuscript, exact-manuscript refusal). Decoy detail strings differ
so digests differ; coverage pairs/locations stay coherent (preconditions healthy —
no validator/Git mocks, no state rewind, no faked `_resolve`).

## 2. Exclusive transfer helper + controls (same helper everywhere)

`transfer_exclusive.py` — evidence-only, not a shipping writer/framework. Exact delta vs
the old witness copy: destination creation uses
`os.open(dst, O_CREAT|O_EXCL|O_WRONLY|O_NOFOLLOW)` so pre-existing destinations refuse
with `FileExistsError` atomically at create time (no takeover; no TOCTOU between a
preflight `exists()` check and the write). The `absent-exclusive` wording for the old
`shutil.copyfile` helper is hereby retracted: old code only checked
`exists()`/`lexists()` first and then copied — never exclusive.
Helper also enforces: real-dir + no-symlink + prefix no-alias checks; survey dir inside
declared repo root (staging dir is a disposable build dir outside fixture Git by
design — noalias-checked, repo containment applies to the destination); 3-file order;
digest convention (`<sha>  main.pdf`); short-write/fsync/close checking; postread sha
equality; `on_error(exc, written, dir)` callback before re-raise; partials never cleaned.
Source opened before destination creation, so an unreadable source leaves no
destination trace. Fault seam is environmental I/O (chmod, missing input, pre-existing
destination), never a validator stub.

Same helper drives: supplement positive transfers (2), conflict C1 (`FileExistsError`,
shas unchanged), failed-build C2 (`no built main.pdf`, no writes), partial C3
(`PermissionError` after exactly 1 write; inventory 3trio+1pdf; State/QA/bundle/
candidate unchanged; `transfer-controls.json`), restore C4 in NEW targets (OK +
postread; partial preserved untouched). Raw per-control stdout/stderr/exit saved.

## 3. Corrections (see evidence-correction.md for the full append-only record)

- N5a JSON `matched` label withdrawn (raw `Reviewed surface bytes drifted` governs).
- Stale special base files marked SUPERSEDED (final = `*-attempt6.*` set only).
- N3c: 23/25 same-copy repairs (N3c ×2 refusal without same-copy repair, copies disposable).
- No-write scope bounded per recorded checks; orphan N2 rows noted; lost-raw scope
  (envelope-preemption raws, N3c rebound-ok raw, ignored-log resets) documented, nothing
  reconstructed; bash-edit deviations listed; QA scope restated as narrow DETERMINISTIC only.
- Orphan `weekly-stage-orphan-unexplained`: 3 packet-identical files (`899f0f2a…`),
  origin unexplained, sha-authenticated, preserved aside, never used as transfer source.

## 4. Terminal counts

- Supplement workers: 38 (weekly) + 39 (special) = 77 exact operations; final state
  RELEASE_CANDIDATE both routes.
- Transfer controls: 8/8 as expected (C1 FileExistsError ×2, C2 refuse ×2, C3
  PermissionError + unchanged State ×2, C4 restore OK ×2).
- Negatives total (final22 + supplement): 25 + 4 stage-gate (NEG-S1/S2 ×2 routes).
- Blockers: none remaining in this witness. No TeX rebuilds, no suite reruns.
- Visual contrast resolution (post-fix raster check) NOT done here — rasters above are
  the input for the independent visual inspector. Fresh code/evidence resolution
  (including this supplement) remains required before promotion/citation.
