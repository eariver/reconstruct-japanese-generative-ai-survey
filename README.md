# reconstruct-japanese-generative-ai-survey

This repository is a dedicated working area for an external architecture review and possible reconstruction of `eariver/japanese-generative-ai-survey`.

The production repository is **not** this repository. Treat the upstream survey repository as an authority/reference source and keep it read-only during this exercise.

## Purpose

The current Generative AI Survey production system has become increasingly expensive to operate in both wall-clock time and LLM usage. Recent failures also showed that more process and more validation do not automatically produce better reader-facing results. The goal of this workspace is to let an external architecture reasoner examine the system from first principles and propose a simpler, cheaper, higher-quality operating model.

The immediate external architect is **Astra**, running through the official Codex harness. Astra is not being asked to become the production operator. The current production roles remain filled by the existing supervisory and operations agents until a redesigned architecture is reviewed and deliberately adopted.

## Start here

**Phase 4-D's bounded read-only production trace is complete.** It identified automatic internal-text output as a concrete source of downstream repair work. Net lifecycle savings and a quality-complete full canonical baseline remain unproven. Phase 3 remains closed after the Phase 3-G system-direction reassessment.

Fresh Astra sessions need only:

1. [Current Phase 4 handoff](handoff/astra-phase-4-continuation.md).
2. [Phase 4-D assessment](outputs/astra-phase-4d-production-trace.md), sections 1 and 3–5.
3. Only necessary Evidence from its index. [Phase 4-C assessment](outputs/astra-phase-4c-trial-assessment.md) and older Phase 4-A/B decisions remain historical context.

Further acceptance/staging/cache implementation is paused. Phase 4-D found internal Architecture notes copied into reader Draft/TeX and bibliography status metadata emitted by a template, despite recorded publication review PASS. A lab counterfactual preserved other bibliography fields and represented one internal constraint through existing canonical omission handling. Next consider a bounded compatibility/quality probe of reader-ready canonical Draft and rendering without added internal metadata; do not strip substantive limitations or claim cost superiority. Check relevant production fixes before duplicating work. See the current assessment/handoff for boundaries. Past chat logs, Phase A instructions and lab reruns are not mandatory resume inputs.

## Last recorded upstream reference

Production repository: `eariver/japanese-generative-ai-survey`

Last recorded production `main` (2026-09-12 JST):

`005e59841272464307386abfc11f5b09228f0814`

This commit merged PR #487 (`Core v2: resolve effective Screening Discovery basis during Drafting`). Phase 4-D observed W34 at `c1703f7...` / `VALIDATED_DRAFT`, followed by a sidecar FAIL and stop before Publication Candidate. See the [4-D observation](notes/phase-4d/observation.json) and current handoff. Phase 4-A's four-candidate analysis stays fixed at `601481a...`; its later `899d3d6...` observation remains historical. Do not assume observed refs remain latest. The initialization baseline `0a47a9b...` / PR #485 is also historical evidence.

## Core principle

**Do not optimize one agent in isolation. Optimize total system work.**

The target system should reduce total Human + supervisory reasoning + production operations + CI/tooling work while preserving or improving publication quality, research sufficiency, provenance correctness, fail-close safety, and reproducibility.

## Working freedom

Astra may write analysis, notes, diagrams, and proposals in this repository. The upstream production repository must remain read-only during this architecture-review exercise.

Small read-only analytical probes are acceptable when they are cheaper than extended manual reasoning. Large replacement implementations, broad simulations, or production mutations are not the objective of the initial review and should not be undertaken unless Astra can justify that they are necessary to resolve a decisive architectural question.
