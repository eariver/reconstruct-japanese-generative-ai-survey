# reconstruct-japanese-generative-ai-survey

This repository is a dedicated working area for an external architecture review and possible reconstruction of `eariver/japanese-generative-ai-survey`.

The production repository is **not** this repository. Treat the upstream survey repository as an authority/reference source and keep it read-only during this exercise.

## Purpose

The current Generative AI Survey production system has become increasingly expensive to operate in both wall-clock time and LLM usage. Recent failures also showed that more process and more validation do not automatically produce better reader-facing results. The goal of this workspace is to let an external architecture reasoner examine the system from first principles and propose a simpler, cheaper, higher-quality operating model.

The immediate external architect is **Astra**, running through the official Codex harness. Astra is not being asked to become the production operator. The current production roles remain filled by the existing supervisory and operations agents until a redesigned architecture is reviewed and deliberately adopted.

## Start here

**Phase 5 is active; Phase 5-B and a follow-on investigation of one W34 publication repair are complete.** The repair case exposed a gap between correctly bound review declarations and effective assessment of the reader-facing output. It does not support the earlier comparison-condition reconstruction hypothesis: conditional Phase 5-C remains unstarted. Net savings and architecture adoption remain unproven. Phase 4 stays closed.

Fresh sessions need only:

1. [Current Phase 5 continuation](handoff/astra-phase-5-continuation.md).
2. [Publication review boundary decision](outputs/astra-phase-5-publication-review-boundary-decision.md), sections 1 and 4–6.
3. Only necessary [case Evidence](notes/phase-5-review-boundary/evidence.md). The 5-B assessment and older decisions remain historical evidence; the 5-A decision's section 2 restores Phase 4 conclusions.

The next candidate is applying existing editorial review to the complete reader-facing source before costly build/Candidate work, while retaining final exact PDF review and Human authority. Moving work is not saving: any avoided late repair cycles must exceed extra preparation, review and coordination costs. First concretize who already reviews what and when; do not duplicate that work or add a new role/store by default. No new trial/implementation is selected. The 5-B no-support/identification limits remain, and known-case rediscovery is not a fresh cost trial.

## Last recorded upstream reference

Production repository: `eariver/japanese-generative-ai-survey`

Observed 2026-09-14 JST: main `74708eb26a357ec11a839a59de62ab62cd246eef`; W34 `6be0f462d8f02284f8513d7165c778c3797dcaf4`.

W34 has **canonical Human Publication Preview APPROVE r3**, following r2 repair, Core #492 integration and fresh publication. It remains RELEASE_CANDIDATE; next is `stage:freeze`, with Freeze/Release pending. Core #492 repaired bibliography access provenance in Weekly/Special. This does not resolve every earlier source/citation finding. PR #488/#489/#490/#492 are existing baseline maintenance, not reconstruct achievements.

See the [current observation](notes/phase-5-review-boundary/observation.json) and [local binding checks](notes/phase-5-review-boundary/check.json). Candidate raw SHA begins `df376f47`, distinct from payload digest `52c8d0bc`; PDF SHA begins `e93db71a`. Approval/current Candidate/PDF bindings were checked, but full State validation, dependency closure and PDF/full-edition quality review were not repeated. Do not assume the observed refs remain latest.

## Core principle

**Do not optimize one agent in isolation. Optimize total system work.**

The target system should reduce total Human + supervisory reasoning + production operations + CI/tooling work while preserving or improving publication quality, research sufficiency, provenance correctness, fail-close safety, and reproducibility.

## Working freedom

Astra may write analysis, notes, diagrams, and proposals in this repository. The upstream production repository must remain read-only during this architecture-review exercise.

Small read-only analytical probes are acceptable when they are cheaper than extended manual reasoning. Large replacement implementations, broad simulations, or production mutations are not the objective of the initial review and should not be undertaken unless Astra can justify that they are necessary to resolve a decisive architectural question.
