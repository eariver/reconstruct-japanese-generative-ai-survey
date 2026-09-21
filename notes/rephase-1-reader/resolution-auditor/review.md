# Independent resolution check of two design-review findings

2026-09-21 JST. Disposition: **both prior findings are addressed at the evidence/design level reviewed here. B3 remains open and f1 is unchanged.**

This was a fresh, limited resolution check of the two actionable qualifications in `../auditor/review.md`. I did not author the root or Worker material. I read the preserved initial/current probe artifacts, current contract, and the relevant committed f1 source/schema bytes. I did not modify a candidate, access production or newer main, use the network, run the prior Auditor's script, or execute tests.

## Finding 1 — metadata mutation qualification

**Addressed.** The current probe moves the mutation from the forbidden top-level `result.internal_validation_note` to `result.publication_extensions.internal_validation_note`. In committed f1, `draft-v2-result.schema.json` defines `publication_extensions` as an object without a closed property set, so this nested field shape is schema-permitted. The probe now checks that schema shape and includes the schema among its hashed source inputs.

The correction does not overclaim validity. `probe-results.json` and `README.md` state that the complete synthetic fixture is still not a schema-valid publisher input and establishes no CLI/workflow execution. The original `probe-initial.py` and `probe-results-initial.json` remain intact as function-only history. Committed renderer source still hashes the complete Draft result into the TeX package comment, so the corrected control continues to support only the bounded cost point: a full-input semantic envelope can invalidate review for permitted internal metadata even when reader prose is unchanged.

## Finding 2 — binding to the stage-selected manuscript

**Addressed in the implementation contract and required regressions.** Current f1 still calls `validate_reader_surface_gate` at `survey_stage_validation_v2.py:510` and `:560` with issue/Profile identity only; the Gate API itself accepts no expected manuscript argument. `contract-decision.md` obligation 5 now requires the stage to pass its exact selected Reader Manuscript path/hash (or equivalent schema-bound authority), with one matching manuscript manifest and primary-source path/hash. It explicitly covers both DRAFT_COMPLETE and inherited VALIDATED_DRAFT callers. The required-regression paragraph further requires a Gate for a different same-issue/Profile manuscript to fail at both stage callers.

That language resolves the prior ambiguity and maps to the exact two source sites identified by the Auditor. It is a future implementation/test obligation, not evidence that f1 already enforces the binding.

## Boundary retained

This check does not close B3, accept an implementation, or assign a canonical seven-point PASS. The supporting bibliography/style/source closure, provenance split, direct-primary supporting scope, renderer-version behavior, Special/Retrospective and other Profile viability, actual semantic/Human review, and lifecycle saving remain future responsibilities exactly as qualified in the design packet. The current synthetic probe remains function-level evidence only.

Exact reviewed input hashes and f1 identities are in `input-hashes.json`.
