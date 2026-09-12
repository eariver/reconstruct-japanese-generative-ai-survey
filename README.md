# reconstruct-japanese-generative-ai-survey

This repository is a dedicated working area for an external architecture review and possible reconstruction of `eariver/japanese-generative-ai-survey`.

The production repository is **not** this repository. Treat the upstream survey repository as an authority/reference source and keep it read-only during this exercise.

## Purpose

The current Generative AI Survey production system has become increasingly expensive to operate in both wall-clock time and LLM usage. Recent failures also showed that more process and more validation do not automatically produce better reader-facing results. The goal of this workspace is to let an external architecture reasoner examine the system from first principles and propose a simpler, cheaper, higher-quality operating model.

The immediate external architect is **Astra**, running through the official Codex harness. Astra is not being asked to become the production operator. The current production roles remain filled by the existing supervisory and operations agents until a redesigned architecture is reviewed and deliberately adopted.

## Start here

**Phase 4-E's bounded canonical Draft/rendering compatibility probe is complete, including the PR #488 production refresh.** Existing fields support boundary authorship, but renderer compatibility and one chronology source join remain unresolved. Bibliography internal-note generation is repaired in current production; do not duplicate that work. Net lifecycle savings and a quality-complete canonical baseline remain unproven. Phase 3 remains closed.

Fresh Astra sessions need only:

1. [Current Phase 4 handoff](handoff/astra-phase-4-continuation.md).
2. [Phase 4-E assessment](outputs/astra-phase-4e-canonical-rendering-assessment.md), sections 1, 3–4 and 6 (current reality refresh).
3. Only necessary Evidence from its index. [Phase 4-D assessment](outputs/astra-phase-4d-production-trace.md) and older Phase 4-A/B/C decisions remain historical context.

Further acceptance/staging/cache implementation is paused. Phase 4-E found that a structurally valid Japanese Draft does not by itself establish a compatible citation/publication path. Next consider tracing one Grok timing claim from accepted Card to its stated DailyX source authority, read-only, before expanding renderer or architecture work. Keep substantive limitations and account for all author/reviewer/repair work. Check relevant production fixes before duplicating work. See the assessment/handoff for boundaries; old chat logs and lab reruns are not mandatory resume inputs.

## Last recorded upstream reference

Production repository: `eariver/japanese-generative-ai-survey`

Last recorded production `main` (2026-09-13 JST):

`658ae823987431e1f1098243dc2f88cfc0d4864a`

This commit merged PR #488 (remove internal Evidence/materiality notes from Weekly bibliography). W34 is observed at `f50d229...` with regenerated bibliography, new PDF/review records and a `READY_FOR_PUBLICATION_PREVIEW` Candidate record. Human Preview approval/release is not established by that record. The upstream Draft/Architecture and section-20 internal note remain unchanged. See the [updated observation](notes/phase-4e/production-refresh.json) and current handoff. Earlier refs (`005e598...`, `c1703f7...`, `899d3d6...`, `601481a...`) remain fixed historical Evidence. Do not assume observed refs remain latest.

## Core principle

**Do not optimize one agent in isolation. Optimize total system work.**

The target system should reduce total Human + supervisory reasoning + production operations + CI/tooling work while preserving or improving publication quality, research sufficiency, provenance correctness, fail-close safety, and reproducibility.

## Working freedom

Astra may write analysis, notes, diagrams, and proposals in this repository. The upstream production repository must remain read-only during this architecture-review exercise.

Small read-only analytical probes are acceptable when they are cheaper than extended manual reasoning. Large replacement implementations, broad simulations, or production mutations are not the objective of the initial review and should not be undertaken unless Astra can justify that they are necessary to resolve a decisive architectural question.
