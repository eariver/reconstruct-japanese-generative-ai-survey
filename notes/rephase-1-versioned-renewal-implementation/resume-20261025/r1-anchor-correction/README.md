# R1-anchor correction — AUTHOR runtime integration defect fix (no whole PASS, no CommitPoint)

2026-10-25. Root actual R1×2 public chain proven through old R3 editorial r3
(`../r1-anchor-verification/r1-anchor-chain-20261025T150000Z/r1-anchor-chain-summary.md`).
New renewal U prepare+finalize green but activate exit2 AFTER State write INDETERMINATE:
anchor mismatch + reader-surface-gate drift. New r4.supersedes r3 correct,
canonical_anchor.kind LEGACY_REVALIDATION but ref DRAFT_COMPLETE wrong; expected
REAL r2 sha27db45ce, r3 correct anchor ref. Product bug, not test shape.

Selected contract 478f0051 incl §11, ROOT 7d7d5a45 incl §6, astra-integration-corrections
binding. Current candidate actual409 + 741 (HIGH b124 orphan fix, H6fe, S20, P1825,
PUB3f, edpub858, P3S9e2, Reader098). OWN ONLY HIGH+H+S (low pubset/agent untouched,
P1/PUB/Reader/schema untouched unless root return).

## Defect (verified read-only, old fixture UNTOUCHED)

- OLD State -> r4 BAD (9b69, 5965B), r4 anchor DRAFT_COMPLETE ffbde (wrong), r3 anchor r2 27db (correct).
- OLD basis anchor DRAFT_COMPLETE (wrong, history.anchor_kind + original default).
- OLD retained COPY PRE-activation State 2797be (5965B, pointer -> r3 GOOD, hash+provenance verified).
- Live gate 71742cf (r2 cumulative), original gate 60c108, r2 row cumulative (prior original, new r2).
- Gate drift caused by SAME wrong anchor (via revalidation None -> original fallback, correct fail-closed),
  NOT independent old-row projection bug. Low `_anchored_canonical7` (old R1 cumulative) and
  `_verified_active7_from_seal` (new active versioned) predicates preserved, no fallback to originalPath
  when kind LEGACY (LEGACY with original ref refuses).

## Fix (3 files, no P1/PUB/Reader/schema, no low/agent edits needed)

- HIST `survey_versioned_renewal_history_v2.py` (6fe86e78 -> 74275d22):
  Derive full canonical_anchor from verified actual chain (latest legacy before FIRST versioned,
  no rolling, later legacy forbidden), compare EVERY editorial/versioned record anchor exact identity
  against derived (kind+path+sha), verify basis anchor vs derived, return full `canonical_anchor`
  (not just kind), no originalPath fallback when LEGACY, no current-State recursion.
- HIGH `survey_versioned_renewal_v2.py` (b12439d5 -> 1dad1ad1):
  Basis copies HIST chain-derived anchor verbatim via `_copy_hist_anchor` (not kind+validation default,
  LEGACY with original ref refuses). Activation validates new record/seal/basis/chain anchor BEFORE
  State mutation (HIST + low + hypothetical post-State strict agent/selection read-only, no write);
  known anchor contradiction refuses BEFORE write (PRESERVED_INCOMPLETE, not INDETERMINATE).
  Post-check still strict, no fallback.
- S `survey_versioned_renewal_source_v2.py` (20f63eaf -> 2290ddd0):
  Detached basis verifies against prior HIST full anchor (reload prior record chain via HIST leaf,
  no State validation/Reader/Gate/Candidate), exact equality, no rolling, no originalPath fallback
  when LEGACY. No current State in history/source leaf.

Low pubset (`306e5d10`) / agent (`a32072e7`) already correct (derive + selection anchor equality,
old cumulative vs new active projection), preserved, no edits. P1 (`825dba1d`), PUB (`3f4039fd`),
edpub (`85814124`), P3S (`9e2a0ad6`), Reader (`098a2c82`) unchanged, verified.

## New fixture (controlled construction, NOT recovery, original BAD untouched)

- New independent DB `.rephase-1-editorial-runtime/versioned-renewal-r1-anchor-correction-20261025T200000Z/anchor-fix-weekly`
  (`git clone --no-hardlinks`, inert `example.invalid`, no alternates, `nlink==1`, `dev:ino` disjoint, no `GIT_*`).
- E copied (226 files, SHA verified, no hardlinks), EXCLUDING POST State BAD, `__pycache__`, `raw/` residue;
  INCLUDE bad r4 as inert (9b69, stays inert, new allocator r5 gaps okay, chain 32 count not filenames).
  INCLUDE old renewal dir as inert (contains retained COPY).
- PRE-activation State reconstructed from recorded validated before-State COPY
  (`.../high-u1-anchor-weekly/retained/before/.../production-state.json` 2797be, 5965B, pointer -> r3 GOOD,
  hash+provenance verified: retained==before_state_ref, pointer==r3). Labelled controlled construction,
  original BAD State (POST r4 9c1e) preserved UNTOUCHED, no rollback/patch. Exclude/adopt NO orphans automatically.
- `raw/source.json` (547b8a37, discovery raw, E) copied (untracked, not SOURCE commit) after initial miss
  (finalize correctly refused without it; preserved as raw failure, no cleanup).
- SOURCE-only commit `05e32ec` (HIGH 1dad + H 7427 + S 2290, 3 paths ONLY, E stays `??`, no deletion)
  BEFORE new renewal, old E unchanged. Verified staged ONLY 3 files.

## New renewal (positive, public, strict)

- `high-u3-anchor-fix` REUSE_TARGETS (prior r3, mspec ed3, toolchain None): prepare/finalize/activate exit 0.
  (Prior `high-u1/u2-anchor-fix` incomplete preserved: u1 miss raw/source.json, u2 stale QA; no same-byte takeover/cleanup.)
- Basis anchor REAL r2 27db (NOT DRAFT_COMPLETE), S prior-HIST PASS, fresh QA 3/3 PASS (recorded after basis,
  live bytes reinspected, synthetic non-genuine), finalize keys `*_path` (matches source_phase_s shape).
- Activate ACTIVATED r5 (`.../publication-surface-revalidation-r5.json` 691fcb6b, supersedes r3 7dce79ac,
  anchor r2 27db, no rolling, gaps okay: r4 inert skipped, chain r1+r2+r3+r5 length 4).
- POST State -> r5 GOOD, strict `validate_agent_state` PASS (no anchor mismatch, no Gate drift),
  selection VERSIONED_ACTIVE anchor r2 (canonical gate 71742cf r2 cumulative, effective gate 692b9077 new active versioned),
  history HISTORICAL_IDENTITY_VERIFIED chain4 anchor r2 (R1 r2 anchor unchanged through new renewal).
- R1/canonical after refusal no writes (canonical operation refused in revised mode BEFORE writes, no r6, State unchanged,
  records r1+r2+r3+r4(inert)+r5).
- Ordinary activate SAME active set ALREADY_ACTIVE readonly (no new record, State unchanged, orphan b124 preserved, no regress).
  (SAME inert set with different State would INTENT_COLLISION; here SAME active set -> ALREADY_ACTIVE, both refuse new record.)

## Negatives (BEFORE any State write, no INDETERMINATE mutation, State stays -> r5)

- N1 forged anchor same-kind DRAFT (LEGACY kind, DRAFT_COMPLETE ref ffbde) after rehashing basis (basis_sha256 recomputed,
  no digest-only seam): S `validate_renewal_basis` refuses HISTORY_ANCESTOR anchor identity BEFORE State write,
  State unchanged (no mutation).
- N2 wrong latest legacy (r1 8974df vs expected r2 27db) with valid sequence r6, same supersedes r3: HIST refuses
  HISTORY_ANCESTOR anchor identity (not sequence/digest seam), State unchanged.
- N3 stale original (DRAFT_COMPLETE ffbde) with r7: HIST refuses anchor identity, State unchanged.
- N4 current VALIDATION_CHECKPOINT when legacy exists (r8): HIST refuses anchor identity, State unchanged.
  (Prior N2/N3/N4 with forged-record paths outside `rN.json` correctly hit sequence seam; fixed to r6/r7/r8 valid
  sequences to isolate anchor seam per task. Forged r6/r7/r8 + forged-basis-neg1 preserved inert, no cleanup, no adoption.)
- No NoneCandidate/predecessor-enum/metadata-fake patterns in fixed modules (grep verified).

## Pins

- FIX HIGH `1dad1ad1...` 221738B, H `74275d22...` 293643B, S `2290ddd0...` 130043B.
- Unchanged: pubset `306e5d10...`, agent `a32072e7...`, P1 `825dba1d...`, PUB `3f4039fd...`,
  edpub `85814124...`, P3S `9e2a0ad6...`, Reader `098a2c82...`.
- New fixture HEAD `05e32ec...` (parent `5950e0f...`), old fixture HEAD `5950e0f...` preserved UNTOUCHED
  (POST State still BAD r4 9c1e, no rollback).
- New r5 `691fcb6b...`, supersedes r3 `7dce79ac...`, anchor r2 `27db45ce...`, State -> r5.
- Old r4 `9b69edd8...` (anchor DRAFT `ffbde649...` wrong) preserved inert in BOTH old and new fixtures.

## Remaining (whole operation, NOT this fix unit)

Both routes (Longform U/C), genuine changed-tool epochs in isolated synthetic fixtures, repeat incl C->U->U,
renewal->editorial, normal direct Candidate/Preview/Freeze/Release, explicit failure/resume (IO/close/fsync/replace/postread/foreign-inode/32/33/cycle/anchor + ALREADY_ACTIVE/resume), affected regressions
(original routes/R1 slow incl R1x2 anchor/DM004 7/7 + publication/quality/gate/stage/pubset/revalidation/freeze/staged),
independent final implementation review. No whole PASS, no CommitPoint. Ordinary candidate/reconstruct Commit/Push Human-owned.
No network/old runners/cleanup failed roots (all raw preserved: diagnose, fixture clone/add/commit, u1/u2 incomplete, u3 positive, guards/negatives).
