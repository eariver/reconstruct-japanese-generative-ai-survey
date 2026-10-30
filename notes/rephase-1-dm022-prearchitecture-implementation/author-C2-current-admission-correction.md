# Author C2 — CURRENT-only editorial admission (ROOT rejection repair)

2026-10-28 UTC. Owner C2. Scope ONLY C2 paths+tests: `scripts/survey_editorial_publication_v2.py`
(closure CURRENT fix retained, LIVE validator CURRENT-only restored) + own
`tests/test_survey_dm022_c2_editorial_closure_v2.py` (rewritten for CURRENT-only
negatives). No A/B/C1 edits. No ordinary commit/Gitconfig/readback/network/
Production/cleanup/old-runner. `apply_patch` only. Tests ONLY NEW private frozen
copy; no live-candidate tests. Old `21ebf43d…` snapshot/code/failure evidence +
`author-C2-editorial-closure-correction.md` return PRESERVED, superseded by this
file (not edited, not deleted). No Commit Point; root unit ongoing.

Binding read FIRST: `independent-cross-family-boundary-review.md` §§1–7 (binding),
ROOT 0425c530 §3/§5.1-5.2, contract a345 §10/§11.2/§11.4, renewal ROOT 7d §2,
Attempt7 BLOCKER (prepare 63 vs 70), C1 H `a9de2c97…` presence-fixed / S `b139…` /
stage `a1b97759…`, final93 proof-copy. P1/P2R/P2V 9/25/14 green preserved (no R1
fake, before-graph intact); NOT reburned here. Full CURRENT70 prepare + normal
LIVE validation both routes → longitudinal worker AFTER this return.

## 1. What ROOT rejected (now removed)

Prior `21ebf43d…` `validate_editorial_receipt` derived `_own_fam` from receipt
commit + fallback `_cur=_own` on CURRENT-derive failure, then checked OWN set
vs OWN blobs, skipped CURRENT SHA/contract/head when `OWN!=CURRENT`. LIVE callers
`finalize 2361` / seal `2654` / `validate_seal 2952` / CLI `4194` / H `correction_proposal:240/:2394`
would admit G71 63-row receipt with G71 contract at G76 disk with NO CURRENT 70
proof — unselected stale admission (contract §10, renewal ROOT §2). Final93 at
same path proves always-CURRENT (no OWN branch). Correct home for OWN is H
detached existing APIs, never C2 LIVE.

Repair per review §5 (no new design, no waiver):
- Delete fallback `except EditorialError: _cur=_own` → fail-closed `CLOSURE_FAMILY`.
- Derive `expected` from CURRENT only (`_derive_current_editorial_family` disk,
  `_route_code_deps(route,_cur)`, `_want=63/70` family-specific).
- Every row: BOTH `git show commit:name==got` AND `_read_bytes_bounded CURRENT==got`
  unconditionally (final93 shape). Delete `if _own==_cur` gate.
- `tools[contract]==current_contract` unconditionally. Delete else-pass.
- `_verify_head_bytes` / `verify_tool_basis` on CURRENT-canonical filtered subset
  unconditionally. Filtered set via `_canonical_closure_names_for_family(route,_cur)`
  (CURRENT only in LIVE). Delete else-OWN-blob loop.
- Keep: strict State bytes/schema, `_require_canonical_current_state`, public
  `agent.validate_agent_state`, proposal/staged/scope/P3S proof/replay, renewal
  strict branch `714–736` FULL matching CURRENT source proof (untouched), no
  pending/verified-dict/quiet-OWN fallback, no `production.verify_state_basis`.
- Delete `_derive_own_editorial_family` (unused budget removed). No new public
  detached validator in C2 (historical belongs H existing APIs).
- `grep -n "_own_fam\|_cur_fam_for_val\|_derive_own" survey_editorial_publication_v2.py`
  empty in file (only `_cur_fam` CURRENT remains). Callgraph unchanged
  (2361/2654/2952/4194 + H 240/2394 all LIVE).
- Prepare unchanged except CURRENT-only: `receipt_closure=_editorial_closure_rows(repo,route)`
  (`family=None` → CURRENT). G76 producer 70 fix retained.

Forbidden alternatives NOT applied: pending/verified-dict, try-CURRENT-except-OWN,
skipping `validate_editorial_receipt` at finalize/seal, removing
`agent.validate_agent_state`/canonical-State, `production.verify_state_basis`,
renewal `authoring_refs` normalization.

G71 receipt at G76 LIVE MUST refuse; actual G71→G76 operation chronology root
separately resolving — never faked via validator waiver.

## 2. Source pins (fixed for this correction)

- Candidate HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree `8ce36998…`,
  inert `example.invalid`, no alternates/commondir.
  H `a9de2c97eb40…`/315610B, S `b139f493f791…`/144597B,
  stage `a1b97759c36174bb86567952f86729e5d06d4727a9fa0d26afa452cc085a5573`.
- C2 overlay (candidate==exec, byte-identical):
  `scripts/survey_editorial_publication_v2.py`
  `3a8721569d3cb1512501699ecf78d7c7e3679120cfb9b06504fa1471bfdee722`
  `tests/test_survey_dm022_c2_editorial_closure_v2.py` (rewritten, 5 tests)
  `f901e0a674537b4ef486941ebc0f49322cc04e633ece6a346ad225844c181f69`
- Frozen exec: `…/c2-current-admission-20261028T224624Z/exec/` 760 files,
  83 git, 0 `(dev,ino)` overlap (57/57), 0 `__pycache__` PRE/POST,
  no `GIT_*` env, process-scoped identity, no global config, no clean/reset.
  Runtime `/usr/bin/python3` 3.14.4, `jsonschema 4.23.0`, `pypdf 6.16.2`,
  `python -m unittest` only, `PYTHONDONTWRITEBYTECODE=1`, per-run `unset GIT_*`.
- Old `c2-editorial-closure-20261028T223346Z` (21ebf…/old test + raws) preserved,
  never overwritten. New raws unique under `evidence/c2-current-admission-…`.

## 3. Tests — NEW frozen copy ONLY, unique RAW

Evidence: `notes/…/evidence/c2-current-admission-20261028T224624Z/`
(`run-01…run-03`, each `header.txt`+`stdout-stderr-raw.txt`+`exit-code.txt`).

| Run | Selection | Ran | OK | FAIL | ERR | Skip | Exit | Time | Raw SHA256 |
|-----|-----------|-----|----|------|-----|------|------|------|------------|
| 01 | `tests.test_survey_dm022_c2_editorial_closure_v2` (CURRENT G76 70×2 + derive-fail + old63-refuse/H-may + mode/schema/control/drift) | 5 | 5 | 0 | 0 | 0 | 0 | 1.109s | `5c5763b6…` |
| 02 | `tests.test_survey_release_checkpoint_v2` (narrow-gate regression) | 9 | 9 | 0 | 0 | 0 | 0 | 0.314s | `65184884…` |
| 03 | `tests.test_survey_dm022_c2_consumers_v2` (C2 17) | 17 | 17 | 0 | 0 | 0 | 0 | 40.162s | `989e7429…` |

0 skipped (no skip-as-PASS). POST 760 files, 0 pycache.

Targeted unit proves (actual APIs, real G76 disk):
- CURRENT G76 weekly/longform full70: exact names == C1 `70`, no dups,
  `path==name`, regular non-exec modes, SHA==current bytes.
- CURRENT derive failure failclosed (empty repo → `CLOSURE_FAMILY`, never OWN fallback).
- Old63 at G76 ordinary refuses: `G71 63 < G76 70`, `G71 29/34 < G76 36/41`;
  ordinary set equality `63!=70` → LIVE `CLOSURE_SET` refuses. H detached may
  validate OWN via existing H `_derive_tool_generation`/`_expected_*` 50/63/70
  separation (not C2 LIVE; verified by H pins + literal distinction, no C2 waiver).
- Wrong mode/schema/control/live drift refuse: bogus route/family, `G67`,
  bad staged family, bad canonical route/family, exec-bit predicate,
  tampered SHA `!=` current (detection predicate). Full `prepare` + normal LIVE
  validation both routes NOT run here — longitudinal worker AFTER return
  (needs TinyTeX, real P1→P2R→P2V→P3S chain, PDFs, synthetic nongenuine reviews).

External-review scope: synthetic exact-new-PDF reviews later are nongenuine;
they cannot create genuine PASS runtime. No genuine approval, no Production.

## 4. Remaining (honest, root unit ongoing)

- Longitudinal Attempt7: CURRENT70 `prepare_publication` (real revised scope,
  P1→P2R→P2V→P3S green already) → reviews → finalize → activate →
  VERSIONED_ACTIVE → renewal U/C → normal release → G71→G76 control, both routes,
  REAL TinyTeX PDFs, retained manifests, synthetic nongenuine gates. Unblocked by
  CURRENT70 fix + CURRENT-only admission; awaits longitudinal rerun (not this unit).
- THEMATIC editorial/draft, renewal dual-epoch (genuine G71 old + G76 new commits +
  current proof), independent implementation review, Profile/quality/audit/adoption/
  savings: OPEN. Whole `NOT_READY/step4B3OPEN/audit unstarted/DM021+022OPEN` preserved.
- If General/Astra requires G71 63-row receipt admitted as LIVE at G76 without fresh
  G76 70 receipt → NOT_READY contract return (new typed migration per a345 §9/§11.4,
  options A/B/C per review §6). Not implemented here.

Stop: no Commit Point taken. Ordinary Commit/Push Human-owned.
