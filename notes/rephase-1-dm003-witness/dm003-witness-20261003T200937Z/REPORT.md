# DM-003 witness report — fixed 222, seven scenarios

Packet `notes/rephase-1-dm003-witness/dm003-witness-20261003T200937Z/`.
Harness `run_dm003_witness.py` (v1 frozen as `run_dm003_witness.v1.py`).
Canonical evidence per scenario is mapped in `evidence-rerun/summary-final.json`
(C1–C5 → `evidence-rerun/C1..C5`, C6 → `C6-R2`, C7 → `C7-R4`).
86 recorded operations total across 7 scenarios (operations, not test methods).

## Identity and isolation

- Source `222a37e9ee2aa96724a491f2c04c2583a86b9650` / tree
  `dbabeed5e70d79b51abb09b64666ca9e1d0fd5dd` / parent `ff6c67f`, branch
  `codex/dm001019-freeze-implementation`, asserted per scenario before/after plus
  five source-file hashes. Witness copy
  `/tmp/opencode/jgas-dm003-witness-20261003T200937Z` is an independent `cp -a`
  (no hardlinks, no alternates, inert origin untouched). Post-run: witness copy
  exact HEAD/tree, empty status; impl and restored DBs still HEAD 222 clean.
- One Special `LONGFORM_SPECIAL` scaffold (`SpecialFixture` + real
  advance/approve helpers); synthetic upstream/PDF/Human rows; real validators and
  builders throughout, no stubs, no Weekly/all-profile claim.

## Outcome table (all oracles held as selected)

- **C1 canonical omitted positive (= control, counted once):** producer creates
  `VALIDATED_DRAFT.json` with `checkpoints: []`; path absent from all 12 named
  refs; named `validation` = `DRAFT_COMPLETE.json` (distinct file/role); approval
  binds C1; wrapper Freeze + stage admission PASS; State/inputs byte-stable.
- **C2 sibling removed after advance, before approval:** State valid, approval +
  Freeze + stage PASS, sibling not recreated — consumed at transition, not
  re-discovered.
- **C3 corrupted unreferenced sibling after approval:** ignored; State valid, C1
  stable, Freeze + stage PASS (non-validation of corruption, recorded as such).
- **C4 approved-Candidate byte drift:** wrapper `ValueError: Production State
  invalid before Freeze: Publication Preview approved candidate bytes drifted`;
  direct approval check and State entry report the same drift; no
  outputs/State mutation.
- **C5 disagreeing human-vs-checkpoint typed refs (A1/A2 each standalone valid,
  distinct):** State entry returns `[]` (recorded observation); stage
  `StageValidationError: Human Preview and checkpoint approval authorities
  disagree`; no report, outputs/State stable.
- **C6 valid rival C2, same PDF:** C2 standalone `validate_candidate` PASS (same
  issue/Profile/PDF-sha; same bytes, distinct path — content-distinct rival is
  structurally infeasible, see below). Direct `Freeze(C2,A1)` →
  `ValueError: ... does not bind the exact Publication Candidate ...` before
  writes. Surplus stage key → `StageValidationError: unexpected current stage
  artifacts: publication-candidate` (extra-key guard, not merge). Correct
  admission then PASSes binding C1.
- **C7 rival orphan ignored:** altered orphan is schema-valid but row-divergent
  from the consumed CORE report; Freeze + stage bind C1; orphan C2 not promoted.

## Key invariant established

A byte-distinct same-PDF rival cannot be built at this lifecycle without drifting
recognized authority: manuscript requires canonical `survey_root/main.tex`
(`survey_reader_publication_v2.py:219`, raw v1 traceback preserved) and the named
`validation` checkpoint pins every upstream byte. The feasible conflicting
boundary is a distinct-path authority over identical bytes — and it is rejected
by exact path+hash binding while the orphan variant is ignored.

## Disposition recommendation

**No selected-path blocker.** The omitted `checkpoints: []` sibling does not
impede the Freeze path (typed Preview approval carries the exact Candidate;
`_prior_artifacts` never consults the sibling), and stale/conflicting
mapped/typed authorities reject precisely before any write or admission.
Residual observation (not a defect): `validate_agent_state` does not cross-check
the two Preview provenance slots — the stage entry does, before any effect. No
generic provenance repair and no DM-004 work is justified by this witness.
Limits: single-profile synthetic fixtures; no FROZEN advance here (prior unit);
per-scenario guards, not continuous attestation.

## Setup deviations (all preserved, none weakened to force pass)

V1 rival rebuild + C4 pin + C7 row-comparison bugs kept raw; one unintended full
v2 rerun kept as `evidence-rerun/C1–C5`; two pre-existing-path guard refusals
kept; one `__pycache__` write into the witness copy removed with final status
empty. Pre-existing reconstruct-tree `M .gitattributes` (DM-003 `-text` rule)
was not made by this unit and is left untouched.
