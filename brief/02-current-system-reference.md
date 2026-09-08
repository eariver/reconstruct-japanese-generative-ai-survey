# Current Upstream System Reference

This file is a **navigation aid**, not a substitute for reading the upstream repository. Astra should re-read current repository reality at the start of its investigation because active branches may continue to move.

## Production repository

`eariver/japanese-generative-ai-survey`

Observed current `main` when this workspace was prepared:

`0a47a9b85108c5a2e9644037e7c0fb48b5bd96dc`

That commit is the merge of PR #485 (`Core v2: enforce Sol/Luna review governance and full Architecture dossier`).

Useful URL:

- https://github.com/eariver/japanese-generative-ai-survey

## Active W34 work branch

Observed when this workspace was prepared:

- branch: `weekly/2026-W34-v2-work`
- HEAD: `993583e871bcbfea7bfe700fe5c6f2648e8887c0`

The commit message records a fresh Screening basis after a later Discovery review, with:

- event-level basis: 439;
- KEEP 73;
- MAYBE 136;
- INSPECT 200;
- DROP 30;
- non-DROP 409;
- state advanced `DISCOVERY_COLLECTED -> CANDIDATES_NORMALIZED`;
- Selection / Architecture not authorized in that commit.

This branch is useful as a live case study of the production process, but it is dynamic. Do not assume the above SHA is still current when you begin.

## High-value recent PRs

### PR #483 — Screening authority candidate

https://github.com/eariver/japanese-generative-ai-survey/pull/483

Useful for understanding how exact-head authority, final audits, historical invalidation, rollout authority, and regression discipline accumulated.

### PR #484 — pre-Human Evidence regeneration repair

https://github.com/eariver/japanese-generative-ai-survey/pull/484

Useful for understanding:

- pending Human-Gate invalidation;
- regeneration after improved Evidence;
- Evidence Authority Supplement;
- checkpoint-bound active Evidence/View authority;
- exact historical authority binding;
- W34 read-only regression discipline.

### PR #485 — Sol/Luna review governance

https://github.com/eariver/japanese-generative-ai-survey/pull/485

Especially important for this reconstruction exercise. It records the Human-directed correction after over-delegation of semantic/editorial judgment to the production execution role.

Do not assume PR #485 is the optimal long-term architecture. It is current production governance and valuable evidence of both a failure mode and its immediate repair.

## Recommended starting documents in upstream `main`

These are starting points, not a mandatory exhaustive read order.

- `AGENTS.md`
- `config/survey-production-v2.json`
- `docs/survey-production-core-v2-authority.md`
- `docs/survey-production-core-v2-final-audit-rule.md`
- `docs/survey-production-core-v2-improvement-plan.md`
- `docs/survey-production-core-v2-sol-luna-review-governance.md`
- `docs/special-layout-policy.md`

## Recommended implementation surfaces

Inspect as needed:

- `scripts/survey_production_v2.py`
- `scripts/survey_agent_control_v2.py`
- `scripts/survey_human_gate_v2.py`
- `scripts/survey_evidence_v2.py`
- `scripts/survey_screening_v2.py`
- Selection / Architecture scripts and stage validators
- publication / drafting / release scripts
- operator execution bridge scripts
- `.github/workflows/**`
- `schemas/**`
- `config/prompts/**`

The repository has accumulated a large number of schemas, stage artifacts, review artifacts, and execution helpers. One purpose of the review is to determine which are essential, which duplicate responsibility, and which could be replaced by simpler standard mechanisms.

## Historical production examples

Useful completed or heavily exercised cases include:

- W33 Weekly production and release;
- SP001 longform Special production and release;
- W34 active production and repair history.

W33 and SP001 are valuable because they contain real revision, publication-preview, layout, freeze/release, and provenance incidents rather than only synthetic fixtures.

Useful PR examples include:

- PR #475 — LONGFORM mixed-layout visual-review correction;
- PR #481 / #482 — W33 freeze/release integration and release provenance;
- PR #477 / #478 — SP001 freeze/release integration and provenance;
- earlier W33 Publication Preview rebuild PRs (#398, #404, #406, #409, #412, #418, #424) as evidence of repeated regeneration/review work.

## Important current governance fact

The current canonical governance states that the supervisory reasoning role owns, among other things:

- research sufficiency;
- semantic authority consumption;
- materiality;
- Selection judgment;
- Architecture responsibility;
- Human-facing Architecture Review.

The production operations role owns bounded execution, bulk retrieval, exact-byte capture, provenance, normalization, task-level Evidence work, deterministic regeneration, and delegated gap fill.

The governance also adds mandatory supervisory reviews around Discovery completeness, Evidence authority consumption, gap-fill, Materiality/Selection, and Architecture.

This is precisely why the current system is an interesting reconstruction target: the governance repaired an under-review failure by adding more review work, while the Human's broader objective is to reduce **total** work without losing the quality protection.

## Human Gates

Current Core policy has two normal Human Gates:

1. `ARCHITECTURE_REVIEW`
2. `PUBLICATION_PREVIEW`

Astra may question surrounding mechanics, role decomposition, or internal review design. The existence of two current Human Gates is repository reality, not automatically an immutable design law. Any proposal to change Human decision surfaces must explain the safety and usability trade-off clearly.

## Authority and exact-byte discipline

The current system uses Git commit identity, repository-local paths, hashes, exact candidate/PDF bytes, checkpoint provenance, review records, and lifecycle state heavily.

Do not remove this machinery merely because it looks verbose. First determine which historical failures each mechanism prevents. Then evaluate whether the same invariant can be preserved more simply through standard version-control/content-addressing/provenance/workflow mechanisms.

## External reference freedom

You are explicitly allowed to consult public external sources beyond the upstream repository when useful. Existing OSS/standards/workflow/provenance/publishing/agent-orchestration solutions may be reused or adapted if they reduce total complexity and operational cost.
