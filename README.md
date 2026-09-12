# reconstruct-japanese-generative-ai-survey

This repository is a dedicated working area for an external architecture review and possible reconstruction of `eariver/japanese-generative-ai-survey`.

The production repository is **not** this repository. Treat the upstream survey repository as an authority/reference source and keep it read-only during this exercise.

## Purpose

The current Generative AI Survey production system has become increasingly expensive to operate in both wall-clock time and LLM usage. Recent failures also showed that more process and more validation do not automatically produce better reader-facing results. The goal of this workspace is to let an external architecture reasoner examine the system from first principles and propose a simpler, cheaper, higher-quality operating model.

The immediate external architect is **Astra**, running through the official Codex harness. Astra is not being asked to become the production operator. The current production roles remain filled by the existing supervisory and operations agents until a redesigned architecture is reviewed and deliberately adopted.

## Start here

**Phase 4-C's bounded research/editorial slice is complete after independent review, repair and re-review.** Full canonical production execution and comparative lifecycle savings remain untested. Phase 3 remains closed after the Phase 3-G system-direction reassessment.

Fresh Astra sessions need only:

1. [Current Phase 4 handoff](handoff/astra-phase-4-continuation.md).
2. [Phase 4-C assessment](outputs/astra-phase-4c-trial-assessment.md), sections 1 and 3–5.
3. Only necessary Evidence from its index. [Phase 4-A comparison basis](outputs/astra-phase-4-comparison-basis.md) and [Phase 4-B preparation](outputs/astra-phase-4-next-window-readiness.md) remain historical decisions.

Further acceptance/staging/cache implementation is paused. The three-candidate Phase 4-C trial produced four semantic findings despite passing mechanical checks; all were repaired using existing canonical fields. Independent re-review found no remaining blocker within that slice. Selection/Package remained non-admitted lab envelopes, preserving the Human approval boundary. No work change with demonstrated net lifecycle savings has been established. The next candidate is a limited read-only trace of actual review/repair/runtime in one completed canonical case before defining an alternative. See the assessment and handoff for boundaries. Past Human-Sol logs, previous chat history, Phase A instructions, and lab reruns are not mandatory resume inputs.

## Last recorded upstream reference

Production repository: `eariver/japanese-generative-ai-survey`

Last recorded production `main` (2026-09-12 JST):

`005e59841272464307386abfc11f5b09228f0814`

This commit merged PR #487 (`Core v2: resolve effective Screening Discovery basis during Drafting`). Phase 4 initially re-observed the same refs, then detected W34 advancing to `899d3d6...` / `DRAFT_COMPLETE`. Its fixed four-candidate analysis remains at `601481a...`; Evidence/Selection/Architecture did not change in that advance. See the [fixed inputs](notes/phase-4/basis.json), [late observation](notes/phase-4/late-observation.json), and current handoff. Do not assume observed refs remain latest. The initialization baseline `0a47a9b...` / PR #485 remains historical evidence.

## Core principle

**Do not optimize one agent in isolation. Optimize total system work.**

The target system should reduce total Human + supervisory reasoning + production operations + CI/tooling work while preserving or improving publication quality, research sufficiency, provenance correctness, fail-close safety, and reproducibility.

## Working freedom

Astra may write analysis, notes, diagrams, and proposals in this repository. The upstream production repository must remain read-only during this architecture-review exercise.

Small read-only analytical probes are acceptable when they are cheaper than extended manual reasoning. Large replacement implementations, broad simulations, or production mutations are not the objective of the initial review and should not be undertaken unless Astra can justify that they are necessary to resolve a decisive architectural question.
