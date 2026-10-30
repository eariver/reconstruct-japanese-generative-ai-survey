# Author C2 — renewal Freeze UPSTREAM research branch (Attempt8 blocker)

2026-10-29 UTC. Owner C2. Scope ONLY `scripts/survey_publication_v2.py`
(Freeze UPSTREAM trio) + own `tests/test_survey_dm022_c2_renewal_freeze_v2.py`
(new, 4 tests). No A/B/C1 edits (C1 retained helper NOT edited; durable fixture
reused by COPY NEW). No ordinary commit/Gitconfig/readback/network/Production/
cleanup/old-runner. `apply_patch` only. Tests ONLY NEW private frozen copy;
no live-candidate tests. Attempt8 raws/pointers preserved, never overwritten.
No Commit Point; root unit ongoing.

Binding read FIRST: `whole-lifecycle-witness-progress.md` Attempt8 §§BLOCKER/NOT
reached (exact `_prepare_freeze_inputs:791` verbatim + durable pins), Attempt8
raw `evidence/full-lifecycle-v2-20261029T012936Z/dm022-full-v2-test-raw-20261029T030000Z.txt`
+ retained `...-renew-release-...` + durable manifests, contract a345 §11,
ROOT 0425c530 §3/§5, R6 role map, C1 H `a9de2c97…`/S `b139…`/stage `a1b977…`,
final93 proof-copy. P1/P2R/P2V 9/25/14 + editorial CURRENT70 preserved (no R1
fake); NOT reburned here. Full post-Preview Freeze both routes → longitudinal
worker AFTER this fix.

## 1. Blocker (foreign, C2-owned, NOT patched by witness)

Post-renewal normal Preview→Freeze→Release refuses in
`survey_publication_v2.py:791 _prepare_freeze_inputs`:
`renewal checkpoint wrapper evidence+materiality+completeness from/to/checkpoints
mismatch: None->None ['evidence','materiality','completeness']`.

Cause (read, not patched by witness): renewal Freeze loads retained State
`checkpoint_provenance` trio (DM022-adopted PREARCH, same path+sha
`.../acceptance-revisions/.../checkpoint/record.json`, research record with NO
`from_state`/`to_state`) as stage-checkpoint wrapper expecting legacy
`CANDIDATES_NORMALIZED->EVIDENCE_REVIEWED`. Same overbreadth class as closed
Blocker 3 (research trio vs legacy shape), now in C2 Freeze (not release).
Blocks post-renewal Preview/Freeze/Release to RELEASED for DM022-adopted issues
(both U and C, same retained provenance). Initial Preview/Freeze/Release to
RELEASED remains green per Attempt5 (older qualified composite, NOT transferred);
editorial activation (no freeze) + renewal U activation (no freeze) green.

## 2. Fix (C2 publication only, actual API/frame, no unrelated contracts)

### 2a. Wrong-role refuses (no blanket provenance ban)

Before grouping, explicit typed refusal via LOW (exact `reason`, never
`reason_class`), no State/agent/guard/HEAD:
- `validation`/`publication_preview`/`freeze`/`release` refs in `prov_raw`
  resolving to PREARCH family → `DM022_WRONG_FAMILY` (expected legacy role).
- Retained `publication_revalidation_provenance` pointer resolving to PREARCH →
  `DM022_WRONG_FAMILY` (expected publication activation, R6 5/11/12).
Old wrappers strict legacy preserved (below); new trio never admitted as
validation/freeze/release/publication.

### 2b. UPSTREAM trio branch (all Freeze wrapper consumers 754–845 + downstream artifact lookups)

In `_done_wrappers` loop after `_load_typed_doc`, if
`_dm022_is_prearch_record(ckpt_data)`:
- Must be exactly `{"evidence","materiality","completeness"}` stages, else
  `DM022_WRONG_FAMILY` (wrong role, not trio).
- sameRecord G76: `prov_raw` evidence/materiality/completeness exactly same
  `{path,sha256}` dict == current `_ck` (grouping ensures same key, explicitly
  verified). Incoming Ref hash sizes correct (hex64 + path valid + source_root
  containment already checked 750-756 + file exists + SHA via `_load_typed_doc`).
- Full LOW proof (function-local, no State/agent/guard/HEAD, never H/S recursion):
  `load_typed_checkpoint_record` must be PREARCH + strict kind/reason/operation
  (`EVIDENCE_REVIEWED->EVIDENCE_REVIEWED` dict)/producer_boundary
  (`CANDIDATES_NORMALIZED->EVIDENCE_REVIEWED` dict)/checkpoints/artifacts/SELF
  (live bytes, never tool-epoch)/lineage/sole `DM022_SUPERSESSION_PROOF`/
  revision_root/SizedRefs 3-key (never 2-key) with live bytes + byte_count.
  Plus `check_supersession_record_from_paths` FULL graph (checkpoint/report/
  before_copy `revision_root/retention/state-before.json`, retention inventory
  bound to stored manifest, contract/implementation/profile/lineage, 4 artifacts
  via FULL content validators, recomputed not hash-only).
- Full H proof (OWN tools/schemas/Contract8 via `git show` at epoch, no
  State/agent/HEAD): `verify_prearch_accepted_graph(repo,ckpt,report,before,
  epoch)` with epoch from `record.implementation.repository_commit_sha`
  (tool commit predates CP, never HEAD equality). Covers 5 DM022 + stage
  `a1b977…` epoch blobs (pinned exact), Contract8 profile-derived, profile LIVE.
- Full S LIVE parity (same predicates as `survey_versioned_renewal_source_v2`
  Layer-A 709-807, no Git there): 4NamedRefs exact names/paths/SHA, live re-hash
  via `_add_live_fd` (LIVE/KEEP/COPY, never tool-epoch blobs), upstream producer
  check (trio only), issue match, SELF live, revision_root ownership, SizedRefs
  live bytes + byte_count.
- Freeze snapshot binds (via `_add_live_fd` live SHA, not merely skip/hash-only):
  CP (already via `_load_typed_doc`) + 4 artifacts + report/proof/request/decision
  (SizedRef SHA + `len==byte_count`) + retention_plan inventory (SizedRef SHA +
  byte_count) + `retention/state-before.json` (live pin for snapshot rechecks) +
  OWN 8 (`2` modules + `6` schemas: 5 DM022 + stage-checkpoint, live pin for
  CURRENT rechecks). Complete closure, no helper-only identity counted.
- No-quiet-stale: CURRENT disk family must still be G76 via
  `_derive_current_family_from_disk` (fail-closed; tool upgrade requires new
  current proof/new fixture, not quiet stale). G71/G67 editorial? Freeze renewal
  supports G76 CURRENT only for PREARCH trio (old G71 LEGACY trio without PREARCH
  stays legacy path, never UPSTREAM).
- `pinned_docs[ckpt_rel]=ckpt_data` + `continue` (skip legacy from/to + legacy
  required-set; PREARCH has no `from_state`/`to_state` top-level).
Old wrappers: strict legacy `from/to/checkpoints` (791) + required artifact sets
+ `issue_id`/schema/implementation/contract + producer map + draft dynamics
preserved unchanged.

Downstream `1094` (views), `1146` (completeness), `1175` (selection) + ledger/
matrix/arch/synthesis/draft lookups need NO changes (artifact-name based, not
from/to based; `pinned_docs` now contains PREARCH doc, so views/completeness
resolve in trio, selection resolves in legacy selection wrapper). Audited, not
edited.

No extra module/schema outside map (LOW/H/staged/C1 helpers already mapped).
If actual typed dependency schema branch requires changes beyond selected,
return root precise field (none needed here; schemas unchanged).

Existing normal CURRENT source proof verified each readback remains strict
(live `_add_live_fd` SHA + byte_count for every bound file, no C2 OWN bypass
forbidden prior review). Renewal strict branch `714–736` FULL matching CURRENT
source proof preserved unchanged.

## 3. Source pins (fixed for this correction)

- Candidate HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree `8ce36998…`,
  inert `example.invalid`, no alternates/commondir.
  H `a9de2c97eb40…`/315610B, S `b139f493f791…`/144597B,
  stage `a1b97759c36174bb86567952f86729e5d06d4727a9fa0d26afa452cc085a5573`.
- C2 overlay (candidate==exec, byte-identical):
  `scripts/survey_publication_v2.py`
  `f0486c54e8a6e1579d0c9a5edefcee3bd712f066341040b3c1aaa8bdeff86960`
  `tests/test_survey_dm022_c2_renewal_freeze_v2.py` (new, 4 tests)
  `354bddbb8ba6fd68b8f09d4ac5f6d6cbec837e5b5e6eb55c9db89f20af98d9bd`
- Frozen exec: `…/c2-renewal-freeze-20261029T024700Z/exec/` 761 files
  (760 + new test), 83 git, 0 `(dev,ino)` overlap (57/57),
  0 `__pycache__` PRE/POST, no `GIT_*`, process-scoped identity,
  no global config, no clean/reset. Runtime `/usr/bin/python3` 3.14.4,
  `jsonschema 4.23.0`, `pypdf 6.16.2`, `python -m unittest` only,
  `PYTHONDONTWRITEBYTECODE=1`, per-run `unset GIT_*`.
- Durable source reused by COPY NEW (no original mutation):
  `dm022-durable-versioned-active-prepreview-20261029T023302Z`
  (HEAD `f289de07…`, VALIDATED_DRAFT + VERSIONED_ACTIVE, REAL PDF 68035B,
  PREARCH trio same-record). Tool upgrade (new publication_v2) needs new
  current proof (fresh COPY NEW + live re-verify, done here), not quiet stale
  (old proof bytes never reused without live re-hash + H OWN + CURRENT G76).

## 4. Tests — NEW frozen copy ONLY, unique RAW

Evidence: `notes/…/evidence/c2-renewal-freeze-20261029T024700Z/`
(`run-01…run-04`, each `header.txt`+`stdout-stderr-raw.txt`+`exit-code.txt`).
Attempt8 raws/retained/durable preserved, never overwritten. No C1 helper edits
(used durable fixture directly; C1 retained helper request not needed).

| Run | Selection | Ran | OK | FAIL | ERR | Skip | Exit | Time | Raw SHA256 |
|-----|-----------|-----|----|------|-----|------|------|------|------------|
| 01 | `tests.test_survey_dm022_c2_renewal_freeze_v2` (Weekly sameRecord G76 FULL LOW/H + snapshot binds + wrong-role + malformed) | 4 | 4 | 0 | 0 | 0 | 0 | 1.664s | `3eee5ffc…` |
| 02 | `tests.test_survey_dm022_c2_editorial_closure_v2` (CURRENT 70 regression) | 5 | 5 | 0 | 0 | 0 | 0 | 1.178s | `165363a9…` |
| 03 | `tests.test_survey_release_checkpoint_v2` (narrow-gate regression) | 9 | 9 | 0 | 0 | 0 | 0 | 0.332s | `04978fa6…` |
| 04 | `tests.test_survey_dm022_c2_consumers_v2` (C2 17) | 17 | 17 | 0 | 0 | 0 | 0 | 41.919s | `bb205512…` |

0 skipped (no skip-as-PASS). POST 761 files, 0 pycache.

Targeted proves (real files, real LOW/H, real reads/SHA/byte_count/modes, not
helper-only identity):
- Weekly trio sameRecord G76 + FULL LOW (`load_typed` PREARCH + `check_supersession`
  empty) + FULL H (`PREARCH_VERIFIED`, family `G76`) + 4NamedRefs + SizedRefs
  live bytes == SHA + `len==byte_count` + SELF live + lineage + sole proof +
  revision_root ownership + incoming hex64 + source_root containment + modes.
- Freeze snapshot binds all (CP + 4 artifacts + report/proof/request/decision +
  retention inventory + state-before + OWN 8) via real `_add_live_fd` live SHA
  (not hash-only permit). CURRENT G76 via disk (no quiet stale).
- Wrong-role still refuses (PREARCH as validation/freeze/release/publication
  recognised as PREARCH family, never admitted as legacy; legacy from/to
  preserved for old wrappers).
- Malformed/missing/extra/drift refuse (nonexistent wrapper, extra stage set,
  tampered SHA, `path!=name`: all fail-closed).

External-review scope: synthetic exact-new-PDF reviews later are nongenuine;
they cannot create genuine PASS runtime. No genuine approval, no Production.

P1/P2R/P2V 9/25/14 + editorial CURRENT70 preserved (no R1 fake); NOT reburned
here (long burns). C2 consumers/release/closure re-green above prove no
regression in C2 narrow gates.

## 5. Remaining (honest, whole long witness reruns actual AFTER fix)

- Longitudinal Attempt8 continuation: C-route (RENDER_TARGETS new build + new
  postrender reviews + finalize/verify/activate) → G71→G76 CURRENT-proof control
  (genuine old/new epochs, SAME authority) → repeated U (new epoch, terminal
  EXECUTED) → post-renewal Preview→Freeze→Release to RELEASED both routes
  (REAL TinyTeX, retained manifests, synthetic nongenuine gates) → THEMATIC
  editorial/renewal. Blocked only on this C2 Freeze fix; unblocked now, awaits
  rerun (actual ~600s chains, NOT claimed here).
- Independent implementation review, Profile/quality/audit/adoption/savings:
  OPEN. Whole `NOT_READY/step4B3OPEN/audit unstarted/DM021+022OPEN` preserved.
- If actual typed dependency schema branch requires changes beyond selected
  (none needed here; schemas unchanged), return root precise field (not implemented).

Stop: no Commit Point taken. Ordinary Commit/Push Human-owned.
