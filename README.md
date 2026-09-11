# reconstruct-japanese-generative-ai-survey

This repository is a dedicated working area for an external architecture review and possible reconstruction of `eariver/japanese-generative-ai-survey`.

The production repository is **not** this repository. Treat the upstream survey repository as an authority/reference source and keep it read-only during this exercise.

## Purpose

The current Generative AI Survey production system has become increasingly expensive to operate in both wall-clock time and LLM usage. Recent failures also showed that more process and more validation do not automatically produce better reader-facing results. The goal of this workspace is to let an external architecture reasoner examine the system from first principles and propose a simpler, cheaper, higher-quality operating model.

The immediate external architect is **Astra**, running through the official Codex harness. Astra is not being asked to become the production operator. The current production roles remain filled by the existing supervisory and operations agents until a redesigned architecture is reviewed and deliberately adopted.

## Start here

**Phase 3 is closed after the Phase 3-G system-direction reassessment.** New main work has not started.

Fresh Astra sessions need only:

1. [Current bootstrap](instructions/ASTRA_POST_PHASE_3_BOOTSTRAP.md).
2. [Phase 3 durable handoff](handoff/astra-phase-3-session-closeout.md).
3. [System direction reassessment](outputs/astra-system-direction-reassessment.md), sections 1, 5, and 7.

Further acceptance/staging/cache implementation is paused. The next priority is publication-quality and total-work comparison across research questions, editorial decisions, reader-facing text, review, and repair. The handoff separates current decisions, unproven claims, and historical experiment references. Past Human-Sol logs, previous chat history, Phase A instructions, and lab reruns are not mandatory resume inputs. Other briefs and historical decisions remain available for selective provenance reads.

## Last recorded upstream reference

Production repository: `eariver/japanese-generative-ai-survey`

Last recorded production `main` (2026-09-12 JST):

`005e59841272464307386abfc11f5b09228f0814`

This commit merged PR #487 (`Core v2: resolve effective Screening Discovery basis during Drafting`). See the [fixed observation](notes/phase6-production-reality.json) and handoff for edition state and limitations. It was not re-observed during closeout and must not be assumed to remain latest. The initialization baseline `0a47a9b...` / PR #485 remains historical evidence.

## Core principle

**Do not optimize one agent in isolation. Optimize total system work.**

The target system should reduce total Human + supervisory reasoning + production operations + CI/tooling work while preserving or improving publication quality, research sufficiency, provenance correctness, fail-close safety, and reproducibility.

## Working freedom

Astra may write analysis, notes, diagrams, and proposals in this repository. The upstream production repository must remain read-only during this architecture-review exercise.

Small read-only analytical probes are acceptable when they are cheaper than extended manual reasoning. Large replacement implementations, broad simulations, or production mutations are not the objective of the initial review and should not be undertaken unless Astra can justify that they are necessary to resolve a decisive architectural question.
