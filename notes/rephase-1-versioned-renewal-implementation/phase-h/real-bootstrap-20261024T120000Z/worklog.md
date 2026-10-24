# Phase-H real-bootstrap worklog — HIST on genuine R3 + blocker fix (append-only)

2026-10-23. AUTHOR H correction using REAL old R3 fixtures (not synthetic stubs).
Preserves originals; NEW independent byte-copy DBs; no candidate commits; no Human Commit Point.

## 1. Real fixtures (preserved originals, not modified)

- Weekly: `.rephase-1-editorial-runtime/versioned-renewal-bootstrap-20261023T194449Z/bootstrap-weekly`
  HEAD `721a04d85532d7855f3e54cc411f5847c787726e`, tree `ac7cb0bd2e977b46e957450816eddd779799e144`, ls-files 721.
  Old E uncommitted (?? architecture-*, raw/, selection, sources/, surveys/, views-*).
  Record `sources/2026-W37/publication/v2/publication-surface-revalidation-r1.json`
  SHA `652462887f6a7ce5835f7db83e8d702110209c9ca7ed408d7133baf007145ea6`, supersedes None,
  anchor VALIDATION_CHECKPOINT, issue 2026-W37, wk-boot-1, real 5page PDF 61239B + log 92972B, Gate PASSED.
- Longform: `.../bootstrap-longform` same HEAD/tree/count, issue SP001, lf-boot-1,
  record SHA `2bd14fc72491efb30bd0b137960c9b72058f86eb3e1c1bd0b17e068736f38c7e`,
  real 5page PDF 79530B + log 94029B, old canonical candidate preserved byte-identical, Gate PASSED.
- Both: commit-before-authorities (HEAD unchanged, authorities uncommitted), ACTIVATED VALIDATED_DRAFT
  prePreview, VERSIONED_ACTIVE, strict State + history, no Preview/freeze/adoption. Synthetic reviews
  clearly synthetic, no genuine approval. Production semantic NO-GO retained.
- Exact refs in `notes/.../bootstrap-fixtures/evidence*.json` (weekly/longform + source-guard.md).

## 2. NEW independent DBs (fixture commits only, no candidate/reconstruct commits)

- Parent: `.rephase-1-editorial-runtime/versioned-renewal-realhist-20261024T120000Z/`
- Weekly-new: `bootstrap-weekly-new`, Longform-new: `bootstrap-longform-new`.
- Byte copy via `cp -a` (no `-l/--link`, no hardlinks): dev:ino disjoint (orig 21529023 vs new 21637927 weekly worktree;
  pack 21628534 vs 21637432), nlink==1 both, no `objects/info/alternates`, inert origins
  `https://example.invalid/versioned-renewal-realhist-weekly-new.git` (and longform-new),
  no `GIT_*` env, `git status` clean except ?? old E (same 10/12 untracked as originals), HEAD same 721a04d.
  Originals preserved (no edits to bootstrap-weekly/longform, candidate-work, M1, proof-copy).
- Overlay ONLY coherent current intended source (9 H/S + low files, byte-identical from candidate-work):
  `scripts/survey_publication_set_v2.py`, `scripts/survey_agent_control_v2.py`,
  `scripts/survey_versioned_renewal_history_v2.py`, `scripts/survey_versioned_renewal_source_v2.py`,
  `schemas/versioned-renewal-*.json` (4), `schemas/publication-surface-revalidation.schema.json`.
  S real module exists, high absent (no high stub; history only runs without closure current high,
  old50 historical epoch has required old high). No config/staged/consumer edits (high worker owns),
  no content/route edits (S worker owns). Snapshot manifest `source-manifest.json` (explicit path/SHA/bytes).
- Commit meaningful NEW tool source BEFORE history validation (no --allow-empty, code before authorities):
  weekly `81539cf` + `53389e6` (blocker fix), longform `0ed991c` + `8c5825a` (blocker fix), each 9 files
  (3 M + 6 A), old E remains ?? untracked. `ls-files` 727 (721+6 new), trees equal `e2a4d84...` (coherent).
  Full SHAs/trees in `source-manifest.json` + raw guard below. No `git clean/reset`, no network,
  no old runner exec. `PYTHONDONTWRITEBYTECODE=1`, fixture paths verified import origin
  (`sys.path.insert NEW DB first, assert __file__ starts with NEW DB`).

## 3. NEW ROOT BLOCKER fix (H-owned low + H module, preserve legacy/schema)

- Prior `_is_versioned_record` only matched RENEWAL pair; doc incorrectly called second pair seal.
  ROOT§2 means TWO ACTIVATION KIND/REASON PAIRS (old EDITORIAL + new RENEWAL), not activation+seal.
- Added `_is_renewal_record` (renewal-only: VERSIONED_RENEWAL_ACTIVATION_V1 + REVIEWED_VERSIONED_CORE_RENEWAL)
  and redefined `_is_versioned_record = _is_editorial_record or _is_renewal_record` (both pairs)
  in `survey_publication_set_v2.py`, `survey_agent_control_v2.py`, `survey_versioned_renewal_history_v2.py`.
  `_is_versioned_seal` unchanged (seal pair). Legacy/schema original shapes preserved.
- Callers updated carefully (not blind rename; renewal-only vs both distinguished):
  pubset: renewal validation/dispatch use `_is_renewal_record` (ONLY renewal); nullability, before-digest,
  selection (`VERSIONED_ACTIVE`), mode probe use `_is_versioned_record` (both).
  agent: checkpoint projection, chain head/link (renewal-only for renewal kind tracking, versioned-both
  for mixed-chain rule), kind checks (renewal-only for VERSIONED kind), linked proof + agreement use
  versioned-both; editorial/renewal branches in `_resolve_publication_revalidation` stay separate
  (editorial-only vs renewal-only) with versioned-both for shared chain/agreement.
  history: `_record_kind` VERSIONED uses renewal-only (editorial checked first); versioned-both available
  for predecessor checks. Old editorial `validate_activation_record` still calls old P2R KEEP tool LIVE
  (preserved for current publication checks); versioned predecessors use HIST structural (epoch blobs),
  normal current Candidate/Gate separate fully current (not weakened to history).
- Verified: `agent.validate_agent_state` on canonical LIVE old R3 after NEW tool commit PASS (0 errors,
  STATE structure, absolute root, no fake/pending/skip); old full current receipt REFUSE via public
  `edpub.validate_editorial_receipt` (TOOL_DRIFT on H-owned revalidation schema, proving Core change).
  Normal State after new renewal lifecycle will validate whole Proof later (high worker, not asserted here).

## 4. Public proofs on BOTH real fixtures (authority positive = real R3, not synthetic)

Script `verify_real_hist.py` (dedicated editor, `PYTHONDONTWRITEBYTECODE=1`, fixture import origin verified):
- HIST `verify_versioned_history` PASS both (chain 1, anchor VALIDATION_CHECKPOINT, refs 1,
  `observed_source_bindings==[]` correctly not claimed for editorial when skip).
- E absent old tool commit positive both (`git show 721a04d:E_path` exit 128, HIST still passes).
- beforeState COPY not live + old State mutated: live State SHA differs from before_ref
  (weekly live `ca7c0d2e...` vs before `ad2d207c...`; longform live `17c20a1e...` vs before `40107355...`),
  retained COPY matches before_ref, HIST passes despite live mutation.
- agent STATE-structure PASS both (0 errors, absolute root, no fake/pending/context/skip).
- old receipt REFUSE both via public API (TOOL_DRIFT on revalidation schema, Core change proof).
- Mutations each reach intended validator + repair pins (real graph/role arrays, not minimal synthetic):
  seal 15-name, staged code_deps 50 subset, receipt file SHA drift (authority), receipt closure TOOL_DRIFT
  direct (real OLD 50, no file mutation), scope SHA drift, raw duplicate/traversal/symlink (HIST raw),
  retained-COPY tamper, digest recompute mismatch. Each HIST preempts with exact HISTORY_* code,
  repair restores bytes + re-PASS. O17 pointer, supported==observed, byte-order, foreign lineage,
  depth/cycle/anchor renewal paths remain for high worker (no renewal yet; old H stub tests labelled
  unit-only, replaced authority positive with real R3 here). Synthetic shapes NOT used for authority.
- Raw output `run-raw.txt` (exit 0). Old H stub tests preserved as unit-only, not full proof.

## 5. Remaining / blockers (no Human Commit Point, root whole operation ongoing)

- S worker owns content/route modules; high worker coming owns other consumer files/config/staged —
  coordinated, not edited here. H owns low pubset/agent/H module/4 Schemas/revalid schema (this unit).
- Normal State after new renewal lifecycle validate whole Proof later (high worker).
- Old H tests with stub source/high isolated label accepted ONLY unit, not full proof (preserved).
- No source package cleanup/reset/commits. No genuine approval, no freeze/adoption, production NO-GO.
- Actual public failures observed: none unexpected (HIST/agent PASS, receipt REFUSE as required Core-change
  proof). Blocker fixed above; no new blockers found in H scope on real fixtures. Any renewal-path
  failures to be returned by high worker with precise issue before broadening.

Stop here. Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN. Ordinary Commit/Push Human-owned.
