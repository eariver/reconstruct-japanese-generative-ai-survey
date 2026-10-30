# Author C2 — release publication-pointer decoder (Stage vs REVALIDATION)

2026-10-29 UTC. Owner C2. Scope ONLY C2 (no outside ownership):
`scripts/survey_release_checkpoint_v2.py` (publication pointer ONLY),
`scripts/survey_publication_v2.py` (Freeze retained pointer + preview wrong-role,
same REVALIDATION pattern), `scripts/survey_weekly_mechanical_refresh_v2.py`
(predecessor chain explicit PREARCH, no LOW), own
`tests/test_survey_dm022_c2_release_decoder_v2.py` (new, 4 tests).
No A/B/C1 edits (C1 retained helper NOT edited; durable fixture reused by COPY
NEW). No ordinary commit/Gitconfig/readback/network/Production/cleanup/old-runner.
`apply_patch` only. Tests ONLY NEW private frozen copy; no live-candidate tests.
No old log overwrites. No Commit Point; root unit ongoing near final witness.

Binding read FIRST: two independent actual witnesses fail final Release SAME C2
bug (G71→G76 genuine Weekly + G76 C→U→U FROZEN current pointer
`VERSIONED_RENEWAL_ACTIVATION_V1` valid, `build_release_checkpoint:93` LOW
Stage/PREARCH loader → unknown kind), precode ROOT §5.1 (NEVER publication
activation through LOW), contract a345 §11, H `a9de2c97…`/S `b139…`/stage
`a1b977…`, final93 proof-copy. P1/P2R/P2V + CURRENT70 + Freeze UPSTREAM green
preserved (no R1 fake); NOT reburned here. Fresh actual witnesses will regenerate
for changed Source Proof; don't hotpatch old Frozen fixture or ignore current
tool pin.

## 1. Bug (wrong decoder, same pattern in 3 C2 sites)

`survey_release_checkpoint_v2.py:93` loads
`state.publication_revalidation_provenance` (REVALIDATION_SCHEMA,
`VERSIONED_RENEWAL_ACTIVATION_V1` valid) via LOW
`load_typed_checkpoint_record` (Stage/PREARCH loader, CHECKPOINT_SCHEMA +
DM022 schema). LOW dispatches Stage (no kind) vs PREARCH (kind PREARCH...),
unknown kind → `unknown kind` error. Valid VERSIONED pointer can never reach
RELEASED. Same overbreadth class as closed Blockers 3/Freeze-trio, now in
publication-pointer decoder (not Stage trio).

Duplicates (same REVALIDATION-via-LOW pattern, all C2-owned, audited):
- `survey_publication_v2.py:785` retained `publication_revalidation_provenance`
  via LOW (Freeze, old COPY, not live) — same bug, fixed here (raw + S proof).
- `survey_publication_v2.py:774` `publication_preview` via LOW — preview approval
  is NOT Stage checkpoint (REVALIDATION-adjacent) → proper preview validator,
  never LOW (fixed here; `validation`/`freeze`/`release` Stage via LOW kept correct).
- `survey_weekly_mechanical_refresh_v2.py:597-608` predecessor REVALIDATION chain
  via `core.load_json` (no schema) + no explicit PREARCH — added explicit raw
  PREARCH refusal (proper separation, never LOW). `validation` via LOW kept
  correct (Stage).
- Other C2 pub ptr sites use correct decoders already (no LOW for REVALIDATION):
  `validate_candidate`/`validate_preview_approval`/`validate_release_record`
  via `REVALIDATION_SCHEMA` + `_refuse_prearch_as_publication` (raw kind+reason);
  `resolve_publication_selection`/`resolve_publication_artifact_path`/
  `resolve_active_publication_revalidation` via `REVALIDATION_SCHEMA` + prior/
  establishment/immutable rows; `editorial_*` State-pointer equality (no parse)
  + `validate_activation_record` (REVALIDATION_SCHEMA + explicit PREARCH).
  Schema Stage (`CHECKPOINT_SCHEMA` + LOW Stage/PREARCH dispatch) vs REVALIDATION
  (`REVALIDATION_SCHEMA` + reason_class/kind) separation now holds at ALL C2
  pub ptr sites; no generic dictionary token.

## 2. Fix (C2 release ONLY strict proper parser, no just-allow-known-string)

`survey_release_checkpoint_v2.py:89-122` (Stage validation/freeze/release via LOW
kept correct; publication pointer fixed):
- Explicit PREARCH wrong-family via raw `kind==PREARCH...` + `reason==REVIEWED...`
  (proper publication ref parser, never LOW Stage loader), preserved valid
  original reason root (`DM022_WRONG_FAMILY ... publication_revalidation_provenance`).
- SHA binding first (tampered hash refuses, `hashlib.sha256(live)!=ptr.sha` →
  `WRONG_FAMILY`, not just allow known string). Missing/unreadable/not-JSON/bad
  ref shape all fail-closed `WRONG_FAMILY`.
- Full REVALIDATION validation still happens via existing top
  `agent.verify_agent_state_basis` (entry line64: `validate_agent_state` →
  `resolve_active_publication_revalidation` with REVALIDATION schema, prior
  binding, establishment, immutable rows, SHA drift). Redundant LOW decoder
  removed; no skip of CURRENT proof (top unchanged) / current record role
  constraints (prior/establishment/immutable rows via top + explicit resolve
  below) / no generic dict token (exact `{path,sha256}`, hex64, lexical containment).
- Prove full pub validation in release (beyond top): explicit
  `agent.resolve_active_publication_revalidation(repo,cfg,state)` after PREARCH
  check; errors → `WRONG_FAMILY`, `None` → `WRONG_FAMILY` (missing, never CANONICAL
  fallback). Existing `verify_agent_state_basis` top + correct typed pub branch
  retained; redundant wrong decoder removed with proof (top + explicit resolve).

Freeze retained pointer (`survey_publication_v2.py:800-822`): same raw PREARCH +
SHA pattern (old COPY, not live; live resolver would compare retained prior to
live State and fail incorrectly). Full validation via S proof (retained COPY + H
OWN already bound in UPSTREAM branch + live `_add_live_fd` CURRENT rechecks);
no live resolver for retained, no LOW. `validation`/`freeze`/`release` Stage via
LOW kept; `publication_preview` via raw + `validate_preview_approval` already at
Freeze entry (no LOW).

Weekly refresh predecessor chain: `_expect_file` SHA binding kept (tampered
refuses) + explicit raw PREARCH refusal (REVALIDATION chain, never Stage/LOW).

No extra module/schema outside map (LOW/H/staged already mapped; no new schema).
If actual typed dependency schema branch requires changes beyond selected, return
root precise field (none needed; schemas unchanged).

## 3. Source pins (fixed for this correction)

- Candidate HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree `8ce36998…`,
  inert `example.invalid`, no alternates/commondir.
  H `a9de2c97eb40…`/315610B, S `b139f493f791…`/144597B,
  stage `a1b97759c36174bb86567952f86729e5d06d4727a9fa0d26afa452cc085a5573`.
- C2 overlay (candidate==exec, byte-identical):
  `scripts/survey_release_checkpoint_v2.py`
  `b9433b9efeca0275c3cd6f8cf77fce0942eaa3208e44df65187f6fcfbee18296`
  `scripts/survey_publication_v2.py`
  `705bcee32557a634c229acbbb58c42d8b34babd90d331f442c158ed59a67482d`
  `scripts/survey_weekly_mechanical_refresh_v2.py`
  `dd01fa01c974486690c9da9701b9ca7040371f6c4d10cb1aa9840126865b551e`
  `tests/test_survey_dm022_c2_release_decoder_v2.py` (new, 4 tests)
  `dbc97587be99bc9aa23493c69126247031d1b6722464f562384d5217dd0c1e09`
- Frozen exec: `…/c2-release-decoder-20261029T052336Z/exec/` 764 files,
  83 git, 0 `(dev,ino)` overlap (57/57), 0 `__pycache__` PRE/POST,
  no `GIT_*`, process-scoped identity, no global config, no clean/reset.
  Runtime `/usr/bin/python3` 3.14.4, `jsonschema 4.23.0`, `pypdf 6.16.2`,
  `python -m unittest` only, `PYTHONDONTWRITEBYTECODE=1`, per-run `unset GIT_*`.
- Old `c2-renewal-freeze-…` (UPSTREAM 70) + `c2-editorial-closure-…` +
  Attempt8 raws/durables preserved, never overwritten. New raws unique under
  `evidence/c2-release-decoder-…`.

## 4. Tests — NEW frozen copy ONLY, unique RAW

Evidence: `notes/…/evidence/c2-release-decoder-20261029T052336Z/`
(`run-01…run-05`, each `header.txt`+`stdout-stderr-raw.txt`+`exit-code.txt`).

| Run | Selection | Ran | OK | FAIL | ERR | Skip | Exit | Time | Raw SHA256 |
|-----|-----------|-----|----|------|-----|------|------|------|------------|
| 01 | `tests.test_survey_dm022_c2_release_decoder_v2` (healthy editorial + renewal positives same State path, malformed + pinned PREARCH refuses, not dummy dict) | 4 | 4 | 0 | 0 | 0 | 0 | 0.140s | `43a7b285…` |
| 02 | `tests.test_survey_dm022_c2_editorial_closure_v2` (CURRENT 70 regression) | 5 | 5 | 0 | 0 | 0 | 0 | 1.131s | `96ec7a75…` |
| 03 | `tests.test_survey_release_checkpoint_v2` (existing 9, narrow-gate) | 9 | 9 | 0 | 0 | 0 | 0 | 0.311s | `1840f501…` |
| 04 | `tests.test_survey_dm022_c2_consumers_v2` (C2 17) | 17 | 17 | 0 | 0 | 0 | 0 | 40.439s | `5a7aa58f…` |
| 05 | `tests.test_survey_dm022_c2_renewal_freeze_v2` (UPSTREAM trio regression) | 4 | 4 | 0 | 0 | 0 | 0 | 1.837s | `da507395…` |

0 skipped (no skip-as-PASS). POST 764 files, 0 pycache.

Targeted proves (real files, real SHA, real writer `build_release_checkpoint`
with same public full State path `production-state.json` via public pattern,
not dummy minimal-dict direct `_dm022_is_prearch_record` flag):
- Healthy EDITORIAL (`EDITORIAL_PUBLICATION_ACTIVATION_V1`/`REVIEWED_EDITORIAL_CORRECTION`,
  real file, real SHA) + healthy RENEWAL (`VERSIONED_RENEWAL_ACTIVATION_V1`/
  `REVIEWED_VERSIONED_CORE_RENEWAL`, real file, real SHA, the exact witness
  kind that LOW failed as unknown) both pass explicit PREARCH check (NOT PREARCH)
  + mocked full resolve says valid (for speed; production top + explicit resolve
  do full LIVE validation with prior/establishment/immutable rows). Must NOT fail
  at `publication_revalidation_provenance` (was LOW unknown kind).
- Malformed (tampered SHA `0*64`, missing file, bad ref) refuses (tampered hash,
  unreadable, not just allow known string).
- Pinned PREARCH (real `PREARCH...`/`REVIEWED...` file, correct SHA pinned, same
  State path) refuses `DM022_WRONG_FAMILY ... publication_revalidation_provenance`
  via real writer (not dummy dict).
- Existing 9 + C2 17 + closure 5 + freeze 4 re-green prove no regression in C2
  narrow gates + UPSTREAM trio (Stage vs REVALIDATION separation intact).

External-review scope: synthetic exact-new-PDF reviews later are nongenuine;
they cannot create genuine PASS runtime. No genuine approval, no Production.

## 5. Remaining (honest, whole long witness reruns actual AFTER fix)

- Fresh actual witnesses regenerate for changed Source Proof (new tool code
  `b9433b9e…`/`705bcee3…`/`dd01fa01…` requires new current proof/new fixture,
  not quiet stale proof, not hotpatched old Frozen fixture, not ignored current
  tool pin): G71→G76 genuine Weekly final Release + G76 C→U→U final Release
  (FROZEN `VERSIONED_RENEWAL_ACTIVATION_V1` valid, REAL TinyTeX, retained
  manifests, synthetic nongenuine gates) → THEMATIC, repeated U, G71→G76 control.
  Blocked only on this C2 decoder; unblocked now, awaits rerun (NOT claimed here).
- Independent implementation review, Profile/quality/audit/adoption/savings:
  OPEN. Whole `NOT_READY/step4B3OPEN/audit unstarted/DM021+022OPEN` preserved.
- If actual typed dependency schema branch requires changes beyond selected
  (none needed), return root precise field (not implemented).

Stop: no Commit Point taken. Ordinary Commit/Push Human-owned.
