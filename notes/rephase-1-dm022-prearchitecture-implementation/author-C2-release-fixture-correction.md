# Author C2 — release narrow gate + P1/P2R/P2V fixture closure correction

2026-10-28 UTC. Owner C2 (replacement, prior resume `invalid_parameters` not deep-debugged).
Scope ONLY (per `astra-implementation-coordination.md`):
12 scripts `survey_publication_set_v2.py`, `run_semantic_publication_v2_interactive_base.py`,
`survey_editorial_correction_proposal_v2.py`, `survey_editorial_publication_v2.py`,
`survey_editorial_retention_v2.py`, `survey_editorial_current_authority_v2.py`,
`survey_publication_v2.py`, `survey_reader_surface_gate_v2.py`,
`survey_execution_record_v2.py`, `survey_reader_publication_v2.py`,
`survey_weekly_mechanical_refresh_v2.py`, `survey_release_checkpoint_v2.py`
+ P1/P2R/P2V fixture copy lists
(`test_survey_editorial_correction_proposal_v2.py`,
`test_survey_editorial_retention_v2.py`,
`test_survey_editorial_current_authority_v2.py`).
No other code edited. No ordinary commit/Gitconfig/readback/network/Production/cleanup/old-runner.
`apply_patch` (Edit tool) only. Tests ONLY on NEW private frozen copy.
Candidate otherwise A/B/C1 idle except C1 helper edits disjoint (different files, saved-BC base).
No Commit Point; root unit ongoing.

Binding read: coordination, precode assessment §5,
ROOT `astra-precode-gate-resolution.md` FULL `0425c530…`/13788B INCLUDING §5,
R6 role map (site 15 `release:121 validate_instance`),
whole-lifecycle Attempt 4 (`whole-lifecycle-witness-progress.md` §§Attempt4/Blocker3),
`integration-bc-diagnostics.md` (124 green + 88 systemic fixture errors),
`c2-a4-evidence-qualification.md` (8 bound greens = entry-guard scope only).

## 1. Root-confirmed blockers fixed (C2 scope)

### 1a. Release blanket ancestral ban — WRONG, removed

`scripts/survey_release_checkpoint_v2.py:68-82` (`build_release_checkpoint`) +
identical gate in CLI `main` (via same function) scanned EVERY
`checkpoint_provenance` entry via LOW typed loader and refused ANY `PREARCH`
family — including the valid adopted research trio
(`evidence`/`materiality`/`completeness` → same PREARCH record, permanent after adopt).

Wrong per R6 site 2 (ADMIT iff expected checkpoint in
`{evidence,materiality,completeness}`), contract §11.2 (normal forward
publication must continue to validate/consume adopted checkpoint), ROOT §3
(publication walkers use detached research-history validator at upstream nodes).
Payload here IS `FROZEN→RELEASED`; refusal fired on upstream lineage, so no
DM022-adopted issue could ever reach `RELEASED` through this CLI. Attempt 4
`test_weekly_candidate_to_released` ERROR reproduced exactly.

Fix (narrow, retains full strict Stage/State/gates):
- Delete blanket `for _rk,_ref in _prov.items()` loop.
- Check ONLY `validation`/`freeze`/`release` refs via REQUIRED LOW
  (`exact reason`, not `reason_class`); wrong-family refuses with
  `DM022_WRONG_FAMILY at <role>`.
- Check `publication_revalidation_provenance` pointer (R6 5/11/12) via LOW;
  PREARCH refuses as publication activation, never as research.
- Supplied Release Record PREARCH refused downstream by existing
  `publication.validate_release_record` R4-row31 explicit
  `_dm022_refuse_prearch_as_publication` (no new pre-check duplicated).
- Upstream trio + other upstream history explicitly ALLOWED through Release.
- Retain: `verify_agent_state_basis`, READY entry + re-assert after profile
  + prepublish re-check, `lifecycle_state==FROZEN`, `stage_plan FROZEN`
  `WORKFLOW_DISPATCH→RELEASED`, release-record path/SHA binding,
  `_validate_stage_artifacts`, CORE_STAGE_CONTRACT + reconciliation reviews,
  forward payload `FROZEN→RELEASED` gate (175-179) + schema gate,
  `canonical_checkpoint_path` + divergent-overwrite refusal.

Exact diff (`snapshot-bc worktree` → `candidate-work`, C2 overlay):

```diff
-    # R6 site 15 payload gate: FROZEN->RELEASED only; PREARCH never admitted.
-    # Classification via REQUIRED LOW typed loader (exact `reason`, not
-    # `reason_class`); wrong-family fails before any CANONICAL fallback.
-    # Content-invalid failures propagate (no swallow to legacy).
+    # R6 site 15 payload gate NARROW: FROZEN->RELEASED only; PREARCH refused
+    # ONLY where Release payload/validation/freeze/publication activation
+    # expected. Upstream research trio (evidence/materiality/completeness) and
+    # other upstream history MUST pass through Release (ROOT §3, R6 site 2,
+    # contract §11.2). A blanket scan over EVERY checkpoint_provenance entry
+    # is WRONG (would refuse valid adopted research). Classification via
+    # REQUIRED LOW typed loader (exact `reason`, not `reason_class`);
+    # wrong-family fails before any CANONICAL fallback. Content-invalid
+    # failures propagate (no swallow to legacy).
     from scripts import survey_research_authority_v2 as _low15  # type: ignore
     _prov = state.get("checkpoint_provenance") if isinstance(state, dict) else None
     if isinstance(_prov, dict):
-        for _rk, _ref in _prov.items():
+        for _rk in ("validation", "freeze", "release"):
+            _ref = _prov.get(_rk)
             if not isinstance(_ref, dict) or set(_ref) != {"path", "sha256"}:
                 continue
             _typed = _low15.load_typed_checkpoint_record(repo_root, Path(_ref["path"]))
@@ -80,6 +86,21 @@
                     f"DM022_WRONG_FAMILY for release checkpoint: PREARCH research "
                     f"node refused at {_rk} (expected FROZEN->RELEASED release)"
                 )
+    # Publication activation pointer NEVER carries PREARCH (R6 sites 5/11/12).
+    # Valid upstream research trio in checkpoint_provenance is allowed above.
+    _pub_ptr = state.get("publication_revalidation_provenance") if isinstance(state, dict) else None
+    if isinstance(_pub_ptr, dict) and set(_pub_ptr) == {"path", "sha256"}:
+        _pub_typed = _low15.load_typed_checkpoint_record(repo_root, Path(_pub_ptr["path"]))
+        if _pub_typed["family"] == "PREARCH":
+            raise ValueError(
+                "DM022_WRONG_FAMILY for release checkpoint: PREARCH research "
+                "node refused at publication_revalidation_provenance "
+                "(expected publication activation, not research)"
+            )
+    # NOTE: supplied Release Record PREARCH is refused downstream by
+    # publication.validate_release_record R4 row31 explicit
+    # _dm022_refuse_prearch_as_publication; valid upstream PREARCH trio does
+    # NOT refuse here (required for DM022-adopted issues to reach RELEASED).
```

C2 consumers `test_release_payload_prearch_refuses_whole_path` (helper
`_dm022_is_prearch_record` + manual raise) left UNCHANGED per ownership
(no other code). It proves helper classification only, NOT full Release
positive. Full both-route `FROZEN→RELEASED` positive with upstream PREARCH
trio + wrong-role payload/pointer refusal is longitudinal worker scope after
this fix (valid surrounding checkpoint full schema there). No helper bogus
prearch State flagged valid claimed here.

### 1b. Systemic retention/P1/P2V fixture closure — missing INHERITED, fixed

`integration-bc` runs 16-19: 82 errors, 0 pass (except 6 pass in renewal):
`ValueError: contract file does not exist: schemas/editorial-manuscript-spec-v2…`
/ `schemas/dm022-preadoption-report-v2…` / `ENOENT sources/…` via
`survey_production_v2:173 aggregate_file_hash` / history blob read.
Root cause: helpers copy `git ls-files` (tracked ONLY, 663 files in
candidate-work) + small explicit untracked lists (10+3+15+7), dropping ALL
untracked INCLUDING old inherited sources. `editorial-manuscript-spec` etc.
are untracked inherited (final-depth 53A), NOT DM022-new. Config
`contract_files.pipeline` closure pins actual bytes (incl. editorial +
versioned-renewal + dm022 schemas); missing file fails closed — NOT an
“unrelated DM022 skip”.

Fix (C2-owned P1/P2R/P2V ONLY; C1 P3S/Longform/renewal parallel, see §4):
- `test_survey_editorial_correction_proposal_v2.py`: add explicit
  `INHERITED53` (53 files from
  `source-packaging/final-depth-20261025T205432Z/complete-versioned-renewal-manifest.json`,
  `40M+53A`, listed verbatim in file) + `DM022_NEW7` (2+5, REQUIRED, no
  longer copy-if-present). `UNTRACKED_SOURCES = INHERITED53` kept for
  backward import compat (retention/P2V/C2-workspace import it).
  `_make_source_root` now copies `INHERITED53+DM022_NEW7` REQUIRED + pinned,
  then `.latexmkrc`, then commits before authority (process-scoped identity,
  inert origin, clean check, no `user.name` in local config). No blind empty
  root, no global Git config.
- `test_survey_editorial_retention_v2.py`: `P2R_EXTRA` kept explicit;
  `DM022_UNTRACKED_SOURCES = p1t.DM022_NEW7` (alias, REQUIRED);
  `_make_p2r_source_root` copies deduped
  `INHERITED53+DM022_NEW7+P2R_EXTRA` REQUIRED + pinned, same commit discipline.
- `test_survey_editorial_current_authority_v2.py`: add local
  `INHERITED53_P2V` (same 53 verbatim) + `DM022_NEW7_P2V` (same 7 REQUIRED);
  `_make_p2v_source_root` copies deduped full set REQUIRED + pinned, same
  commit discipline. No new import (avoids closure change).

Full 53 + 7 enumerated verbatim in the three files (finite explicit, no
wildcard/count-only). Tracked basis + `.latexmkrc` + commit-before-authority
unchanged. No fixture objects in reconstruct, no `GIT_*` inheritance
(asserted), no network, no old-runner reuse.

## 2. Audit — all C2 same-pattern PREARCH scans

Checked all 12 C2 scripts for `for … checkpoint_provenance` / `load_typed…` /
`WRONG_FAMILY`:

- `survey_release_checkpoint_v2.py`: ONLY blanket found, FIXED above.
- `survey_weekly_mechanical_refresh_v2.py:557` loop = snapshot pins
  (file+artifacts+results, no refusal); `:636-688`
  `validate_refresh_validation_checkpoint` = NARROW (only `validation` ref,
  lightweight + full LOW, correct per R6-17). Retained.
- `survey_editorial_correction_proposal_v2.py:1347` loop = checkpoint-wrapper
  graph pins (no refusal); wrong-family only at `validation:557`
  (original validation `DRAFT_COMPLETE→VALIDATED_DRAFT`, R6-14) + same-record
  triplet checks (R4-25). Correct, untouched.
- `survey_editorial_publication_v2.py`: only `validation` shape checks
  (`:978/:1809/:2031`), no blanket. Correct.
- `survey_publication_set_v2.py`: role-specific refuses only
  (`publication artifact` / `stage artifact` research names, mode probe
  PREARCH-before-versioned). Correct.
- `survey_publication_v2.py:60-65`, `survey_editorial_publication_v2.py:60`,
  `run_semantic…_base.py:153`, `survey_weekly…:676-688`: narrow payload/
  validation refuses only. Correct.
- `survey_reader_surface_gate_v2.py`, `survey_execution_record_v2.py`,
  `survey_reader_publication_v2.py`, `survey_editorial_retention_v2.py`,
  `survey_editorial_current_authority_v2.py`: recognize-or-refuse at correct
  narrow sites (retention/current-authority = research retention/observation,
  not publication activation). No blanket.

Conclusion: no other C2 blanket ancestral ban. Strict Stage/State/gates
retained everywhere (READY entry+prepublish, State basis, lifecycle,
stage_plan, artifact binding, schema).

## 3. Source pins (fixed for this correction)

- Base: `snapshot-bc-20261028T175932Z/worktree` 756 files (758 current minus
  2 longitudinal witness files), manifest
  `evidence/source-bc-20261028T175932Z/snapshot-bc-manifest.json`
  SHA256 `e7d9235ac958f7efd219ed589bad205f3ae6340d45bd49c85a1837d64eca0bae`
  /149939B/756 entries. Git 83 files, HEAD
  `409b292756dd1277b9dfae87679934c0d2ce251c`, tree
  `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, inert
  `example.invalid`, 0 inode overlap, no alternates/commondir.
- C2 overlay (ONLY 4 files, `candidate-work → exec` byte-identical):
  - `scripts/survey_release_checkpoint_v2.py`
    `a5e846682b5c7983f3adbaad11162d7dad1af0ab7b3376e7bb58c3a4b62692fb`
  - `tests/test_survey_editorial_correction_proposal_v2.py`
    `36ca8afec4d016f617706a733e2ac950b30e6274cdc0632d7cf5124dc991b399`
  - `tests/test_survey_editorial_retention_v2.py`
    `403beeed0986c45bb0e00f31ada0a930a5f425da55b03bad69a66d9d7161ca45`
  - `tests/test_survey_editorial_current_authority_v2.py`
    `cf7a5bd5288f461d94ee03ec604ea135bb718642f1e7f530cf7bf3995354c0f8`
- Private exec: `…/c2-release-fixture-20261028T184309Z/exec/` 756 files
  (same 756, 4 overlaid), 83 git, HEAD `409b292…`, inert origin, 0 overlap
  vs snapshot git (byte copy, no `--link`). Runtime
  `/usr/bin/python3` 3.14.4, `jsonschema 4.23.0`, `pypdf 6.16.2`,
  `python -m unittest` only, `PYTHONDONTWRITEBYTECODE=1`, per-run
  `unset GIT_*`, process-scoped fixture identity, no global config mutation,
  no `git clean/reset`, no fixture deletion, no old runners.
- POST: 799 files (756 +43 `__pycache__/*.pyc` from diagnostic
  `python3 -c` without env var + test imports). No `.py/.json/.schemas`
  drift (only pycache added). Honest contamination noted; does NOT affect
  fixture authority (fixtures in `/tmp`, snapshots exclude `__pycache__`
  where applicable; source manifest excludes `__pycache__`/`*.pyc`).
  Not cleaned per no-cleanup rule.

## 4. Tests — NEW private copy ONLY, unique dirs, no overwrite

Evidence base:
`notes/rephase-1-dm022-prearchitecture-implementation/evidence/c2-release-fixture-20261028T184309Z/`
(`run-01…run-06`, each `header.txt`+`stdout-stderr-raw.txt`+`exit-code.txt`).
Prior `integration-bc`/`integration-c2-a4fix`/Attempt dirs preserved, NOT overwritten.

| Run | Selection | Ran | OK | FAIL | ERR | Skip | Exit | Time | Raw SHA256 |
|-----|-----------|-----|----|------|-----|------|------|------|------------|
| 01 | retention `test_weekly_capture_verify_positive` (prior failing case FIRST) | 1 | 1 | 0 | 0 | 0 | 0 | 26.839s | `46a942da…` |
| 02 | `test_survey_editorial_correction_proposal_v2` (full P1) | 9 | 9 | 0 | 0 | 0 | 0 | 359.602s | `d0cd8582…` |
| 03 | `test_survey_editorial_retention_v2` (full P2R) | 25 | 25 | 0 | 0 | 0 | 0 | 842.183s | `4a8025ce…` |
| 04 | `test_survey_editorial_current_authority_v2` (full P2V) | 14 | 14 | 0 | 0 | 0 | 0 | 650.482s | `9e02d2db…` |
| 05 | `test_survey_release_checkpoint_v2` (narrow-gate regression) | 9 | 9 | 0 | 0 | 0 | 0 | 0.315s | `12d926a0…` |
| 06 | `test_survey_dm022_c2_consumers_v2` (C2 17) | 17 | 17 | 0 | 0 | 0 | 0 | 40.264s | `c822bc65…` |

All `exit 0`, 0 skipped everywhere (no skip-as-PASS). Run-01 proves the
prior systemic `editorial-manuscript-spec` closure fault is closed for C2
fixtures (was `ERROR`, now `ok`). Runs 02-04 prove full affected P1/P2R/P2V
with complete `inherited53+new7` committed before authority.
Runs 05-06 prove narrow release gate + C2 consumers still green (entry-guard
+ wrong-role refusal scope, NOT full Release positive).

Scope honesty (per `c2-a4-evidence-qualification.md` §5 + instruction):
C2 A4/fixture greens are ENTRY-guard + planted-guard refusal + healthy
positive for P1/P2R/P2V unit contexts ONLY. They do NOT prove full
publication positive, prepublish fault wiring beyond entry, or no-write
strings outside test oracles (raws show `ok` + counts, not error-text
proof). No prepublish-fault overclaim. Full both-route normal
`FROZEN→RELEASED` positive with upstream PREARCH trio + wrong-role
payload/pointer refusal (valid surrounding checkpoint full schema) is
longitudinal worker scope AFTER this fix (Attempt 4 Blocker 3 unblocked).
C2 `test_release_payload_prearch_refuses_whole_path` remains helper
classification scope, NOT a substitute for that witness.

## 5. Shared-helper needs → C1 (parallel, NOT edited here)

C2 did NOT edit (C1-owned per coordination):
- `tests/test_survey_editorial_staged_source_v2.py` (`UNTRACKED_P3S_SOURCES`
  27 incl. 7 DM022 but MISSING versioned scripts/schemas + many inherited
  tests; still fails via `test_survey_longform_derivation_v2` helper).
- `tests/test_survey_longform_derivation_v2.py:104-118` (`ls-files` + ONLY
  2 files; missing 53+7 → `dm022-preadoption-report` closure fail).
- `tests/test_survey_increment_b_weekly_derivation_v2.py:52-62`
  (`ls-files` ONLY, no untracked → `editorial-manuscript-spec` fail, hit via
  P1 `_build_weekly_validated` BEFORE C2 fix; now C2 P1 root supplies full
  closure so weekly path passes, but helper itself still incomplete for
  direct use).
- `tests/test_survey_evidence_v2.py`, `test_survey_longform_publication_integration_v2.py`,
  `test_survey_versioned_renewal_depth_prewrite_v2.py` chain (`sources/` tree
  + `schemas/` closure gaps → `HISTORY_BLOB_MISSING`/contract fail).
- `tests/dm022_c1_fixture_helpers_v2.py` counts (35/22/63/70/73/29/36/34/41/
  67/71/76) without explicit file lists; needs finite explicit lists matching
  pinned actual source if reused for fixtures.

C1 to fix finite explicit necessary sources + commit-before-authority in own
helpers, same discipline (no blind empty root, no global Git config).
No C2 edit to those files; no cross-owner patch applied here.

## 6. Unclosed / NOT claimed (honest)

- Both-route full normal `FROZEN→RELEASED` positive WITH upstream PREARCH
  trio (Weekly+Thematic) + wrong-role Release payload/pointer refusal with
  valid surrounding full-schema checkpoint: longitudinal worker AFTER fix,
  NOT proved here.
- THEMATIC Reader→REAL PDF→admission, later editorial + renewal
  Preview/Freeze/Release, G71→G76 unchanged-upstream compatibility control
  with genuine historical G71 epoch: blocked behind Blocker 3, now unblocked
  but NOT run here.
- P3S/Longform/renewal + `weekly_mechanical`/`dm001/dm003/dm004` affected
  regressions: C1 parallel + root disposition; NOT run here (stopped affected
  batch per BC §5 method; no broad burn).
- Full 7-slot audit no-overwrite + repeat + failure/resume/late seams beyond
  P1/P2R/P2V unit scope, representative quality/Profile/adoption/savings,
  fixed-candidate audit, independent implementation review: OPEN.
- Whole `NOT_READY/step4B3OPEN/audit unstarted/DM021+022OPEN` preserved
  except this bounded fix. No Production semantic claim, no genuine approval,
  no W40 reproduction, no upstream `CORE_FIXED`.
- POST pycache contamination (§3) disclosed; not cleaned, not counted as
  source drift.

Stop: no Commit Point taken; root whole unit ongoing. Human Commit Point
owns ordinary Commit/Push.
