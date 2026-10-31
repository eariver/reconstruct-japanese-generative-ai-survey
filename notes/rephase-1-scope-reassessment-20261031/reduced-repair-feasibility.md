# Reduced-repair feasibility — can P4 cut to DIRECT-only? (General, read-only)

General author. Source-read ONLY on final133 proof-candidate; no network/Git/readback/tests.
Astra qualifies; no edit to prior file. Reevaluates precode normative priority; SMALL≠cheaper not assumed.

## Code predicates (not normative claims)

- LOW `derive_before_context` (`survey_research_authority_v2.py:1172-1297`): verifies COPY==`before_state.sha256`,
  triplet==COPY provenance, records==exact non-DROP IDs (1271). Loads `discovery_ref`/`screening_ref`
  files and checks internal SHAs only; never compares them to COPY accepted chain; no R/E split.
- `_verify_adopted_graph_full:783-799`: explicitly binds `root_records/root_path` to request Discovery
  file as "DIRECT session basis". Caller-claimed DIRECT trusted; DERIVED request would misbind E as R.
- 4 LOW builders (`:1458,:1550,:1675,:1795`): signatures lack `before_copy_path`; validate package basis
  drift + internal digests (`build_revision_package:1336-1375`), never pinned-COPY D/S authority.
- HIGH `prepare_revision` (`survey_prearchitecture_acceptance_v2.py:456-538`): strict LIVE eligibility +
  canonical-State path + tool pins + state-before COPY (537-538), then calls LOW builders with
  `state_copy` (603,618) but without true-R/E. New-policy-before-COPY absent in source.
- True DIRECT proof exists elsewhere but unwired: `resolve_effective_discovery_basis`
  (`survey_screening_v2.py:353-439`) DIRECT vs DERIVED via `_canonical_root_acceptance:325-350` +
  `validate_discovery_expansion:243-322` + `validate_acceptance` D (`survey_discovery_v2.py:274-298`) /
  S (`survey_screening_v2.py:897-916`). DM022 LOW never calls it; it trusts request refs.
- Old runtime proved only synthetic DIRECT; no measured DERIVED frequency in scope. Absence of
  frequency ≠ permission to misbind when DERIVED mode remains readable/claimable.

## DIRECT-only cut: what remains vs what is saved

| | Whole P1-P4 (LAST repair) | P1-P3 + DERIVED-refusal |
|---|---|---|
| Retained | P1 canonical10, P2 U/loss/parity, P3 prepackage path-only, P4 true-R/E: HIGH-before-COPY, LOW pinned-COPY→DCP/SCP→acceptances/JSONL, 4 builders +required PATHs, adopted-full 3-arg, no E-as-R | Same P1-P3 + most of P4 above (DIRECT still needs COPY-bound DCP/SCP + root proof; otherwise DIRECT unproved) |
| Avoided | — | DERIVED-expansion threading + per-parent loss on DERIVED graphs only |
| New cost | None beyond precode map | Unsupported-branch contract delta + refusal-before-write oracles + review + permanent tests/maintenance |
| Compat | Old history under own predicates; manual DIRECT_PRIMARY limits kept, not canonical | Same + explicit refused entry; history kept; no alias-mapping/manual-as-canonical |

Rough relative work: whole ≈ M; cut ≈ M−S saved + S new branch/review/tests ≈ net ~M, with added fork.
Hence DIRECT-only does NOT remove the kernel; proving DIRECT *is* the kernel.

## Decision

Coherent smaller NOT ESTABLISHED as cheaper by read-only source: it retains most kernel cost
and adds a maintained refusal fork. Security/correctness not optional while DERIVED readable.

Preferred under uncertainty: keep whole P1-P4 as LAST bounded upstream repair, then R4 prep;
retract generic complete-reader-before-R4 prereq (that broader gate moves after R4 audit).
Root selects this one actionable last unit now; no new precode cycle, no Human schema pick.
Declared feature loss (DERIVED new-admission) + unproved history explicit; no quality/provenance
drop, no alias/manual-as-canonical claim.
