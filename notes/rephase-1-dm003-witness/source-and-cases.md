# DM-003 milestone-1: exact source / case proposal (fixed 222, no execution yet)

Source pins: HEAD `222a37e9ee2aa96724a491f2c04c2583a86b9650`, tree
`dbabeed5e70d79b51abb09b64666ca9e1d0fd5dd`, parent `ff6c67f68e12b3093901248219f2de2872e54d73`.
Verified read-only (`GIT_NO_LAZY_FETCH=1 GIT_ALLOW_PROTOCOL=file GIT_OPTIONAL_LOCKS=0`):
live impl DB `/tmp/opencode/jgas-dm001019-impl-20261003T100801Z` (branch
`codex/dm001019-freeze-implementation`) and restored
`/tmp/opencode/jgas-dm001019-chainrestore-20261003T150500Z/candidate-partial-b40de60`
(branch `dm001019-final`) both report exact HEAD/tree/parent, empty
`status --porcelain` and empty `diff --stat HEAD`. Saved Summary reused at
`notes/rephase-1-deferred-intake-20261003/deferred-maintenance-summary.md:126-149` only.

## 1. How the Candidate checkpoint is produced, and why the named map omits it

- `config/survey-production-v2.json:347-354`: `VALIDATED_DRAFT` stage has
  `checkpoints: []`, `next_state: RELEASE_CANDIDATE`, artifact `publication-candidate`.
- `scripts/survey_agent_control_v2.py:1186-1188` (`canonical_checkpoint_path`): checkpoint
  file path is derived from the *current* lifecycle, so advancing writes
  `<source>/orchestration/v2/checkpoints/VALIDATED_DRAFT.json`
  (`agent_checkpoint_dir`, config:395).
- `build_stage_checkpoint` (:1263-1325) writes that file with `checkpoints: []`
  (record literally carries an empty checkpoint set, :1307).
- `advance_with_checkpoint` (:1370-1372) registers provenance only
  `for checkpoint in stage.get("checkpoints", [])` — empty here, so **no
  `machine_checkpoints`/`checkpoint_provenance` entry is ever created**; lifecycle still
  moves to `RELEASE_CANDIDATE` (:1373-1385). Omission is structural, not a missed write.
- `_expected_completed_checkpoints` (:123-130) unions checkpoints of stages *before* the
  current lifecycle, so at `RELEASE_CANDIDATE` the VALIDATED_DRAFT file can never be
  expected/required. `_validate_agent_state` (:387-423) therefore never demands it.

## 2. Which pointer/typed approval is authoritative at each phase

- At `VALIDATED_DRAFT` (candidate construction): `validate_stage` VALIDATED_DRAFT branch
  (`scripts/survey_stage_validation_v2.py`, `_validate_stage_semantics` before :601) binds
  the Candidate to exact manuscript/source/PDF/quality/semantic/visual bytes; current
  artifact required set is `REQUIRED_CURRENT["VALIDATED_DRAFT"] = {"publication-candidate"}`
  (stage_validation:75).
- Transition `VALIDATED_DRAFT→RELEASE_CANDIDATE`: authority is the checkpoint *file*
  (canonical path + contract/implementation match, :1331-1359); State gains no named pointer.
- At `RELEASE_CANDIDATE` (Freeze admission): Candidate arrives **only** through the typed
  Preview approval — `_publication_approval_artifacts` (stage_validation:126-156):
  `human_gates.publication_preview == approved`, `human_gate_provenance ==
  checkpoint_provenance[publication_preview]`, `machine_checkpoints passed`, canonical
  approval path (`gates/publication-preview-approval.json`, config:398), approval's
  Candidate path+sha256 re-resolved (`_authority_ref_path`), Profile bindings checked.
  `_prior_artifacts` (:159-198) iterates *only* `state.checkpoint_provenance` (skips
  `publication_preview`, already validated) — an on-disk `VALIDATED_DRAFT.json` with no
  provenance entry is **invisible by construction**; there is no sibling-discovery scan
  anywhere in stage_validation or agent_control.
- Controller `approve_publication_preview` (agent_control:1461-1493) is the sole typed-approval
  producer: requires `RELEASE_CANDIDATE` + pending gate, canonical Candidate present and
  `validate_candidate`-valid, then writes both provenance slots.
- Builders: `_prepare_freeze_inputs` (`scripts/survey_publication_v2.py:171-189`) re-binds
  approval→Candidate exact path/hash plus Candidate-bound pre-preview VISUAL/PDF/bundle
  (`ValueError` on divergence); RELEASE_CANDIDATE stage semantics (stage_validation, branch
  after :575) re-checks Freeze/Manifest/visual approval binding. Same PDF never authorizes a
  different Candidate (DM-001/019 repair, unchanged here).

## 3. Existence/location-valid file vs active State authority; conflicting authorities

- A file can be location-valid (canonical path, schema-valid, matching bytes) yet carry
  **zero** authority: `_resolve_checkpoint_artifact` (agent_control:508-608) resolves
  exclusively via `state.checkpoint_provenance[checkpoint]` + `machine_checkpoints ==
  passed` (:537-542), with the docstring rule "historical storage, not active authority"
  (:516-522). Unreferenced sibling content is non-authority, not "rejected input".
- Two *mapped/typed* authorities in conflict fail closed with distinct errors:
  human vs checkpoint Preview refs disagree → `StageValidationError("Human Preview and
  checkpoint approval authorities disagree")` (stage_validation:138-139);
  prior checkpoints disagreeing on one artifact name → `"prior Stage Checkpoints disagree
  on artifact name"` (:195-196); current artifact replacing an accepted upstream name →
  `"current stage attempts to replace accepted upstream artifact"` (:227-228);
  Freeze record not binding exact Candidate/approval/visual → three `"does not bind
  exact ..."` errors (RELEASE_CANDIDATE branch).
- Same-PDF second Candidate is feasible with actual builders: clone the Candidate, keep
  `pdf.path/sha256/byte_count` identical, change any other bound byte (e.g. manuscript or
  semantic-review bytes + their Candidate-embedded hashes, keeping `validate_candidate`
  valid). `_prepare_freeze_inputs` still rejects cross-binding
  (`"approval does not bind the exact Publication Candidate"`, publication:189) and the
  stage RELEASE_CANDIDATE branch rejects record divergence — so conflict is demonstrated
  through the typed path, while the orphan file stays untouched/ignored.

## 4. Case matrix (5 cases; canonical control IS the omitted case — not double-counted)

Fixture base for all: reuse DM-001/019 `SpecialFixture`
(`tests/test_survey_dm001_019_freeze_equivalence_v2.py:95-569` — real `_cfg()` from
`core.DEFAULT_CONFIG`, `PRODUCERS` through `validation` (:103-113), canonical
advance→approve→freeze helpers at :585-625). Only NEW harness file outside candidate
control roots; real validators/builders, no stubs; synthetic research/PDF/Human rows labelled.
Per-case fresh asserted HEAD/tree/clean guards, `PYTHONDONTWRITEBYTECODE=1`, unique
no-overwrite evidence dirs, byte snapshots before/after.

- **C1 canonical omitted-map positive (= control, stated once):** canonical
  `advance_with_checkpoint(VALIDATED_DRAFT.json)` → `RELEASE_CANDIDATE` with
  `checkpoints: []`, no named pointer; `approve_publication_preview`; `validate_stage`
  RELEASE_CANDIDATE PASS + both `build_freeze`/`build_profiled_freeze` byte-equivalence.
  Oracle: exit 0, only declared report/Freeze/Manifest writes; orphan file present but no
  provenance entry (assert via `validate_agent_state == []`).
- **C2 unreferenced-sibling non-authority:** from C1 end-state, (a) tamper orphan
  `VALIDATED_DRAFT.json` artifact bytes in place, (b) separately delete it. Oracle: Freeze
  admission + rebuild still PASS identically in both variants (proves ignored content, not
  validated content); no `StageValidationError`; State/checkpoint bytes unchanged.
- **C3 stale typed authority:** mutate Candidate bytes after approval (hash drift), and
  separately revert Candidate but keep stale approval ref. Oracle: precise
  `StageValidationError("... authority drift")` / builder `ValueError("... does not bind
  the exact Publication Candidate...")`; no Freeze/Manifest/State writes beyond the
  declared failing output; pre/post snapshot diff empty except harness log.
- **C4 individually-valid conflicting Candidate, same PDF:** second valid Candidate (same
  `issue/Profile`, identical PDF bytes, divergent manuscript bytes), typed approval still
  bound to C1's Candidate; attempt Freeze with the rival Candidate + also attempt a rival
  orphan `VALIDATED_DRAFT.json` carrying it. Oracle: `ValueError`/stage `does not bind`
  rejection for the rival path; orphan variant still follows typed approval (PASS on C1
  bytes). Distinguishes conflicting *admitted* input (rejected) from orphan content (ignored).
- **C5 current-artifact merge conflict:** supply current `publication-candidate` differing
  from the prior approved one at `validate_stage`. Oracle:
  `StageValidationError("current stage attempts to replace accepted upstream artifact:
  publication-candidate")`; `output_path` not created (also assert pre-existing output
  refusal path untouched); no State mutation.

No filesystem scanning, map expansion, or new authority is proposed. Disposition returns
`no selected-path blocker` / `narrow defect` / `unresolved` after Astra oracle selection
and milestone-2 execution in this same unit.
