# reconstruct-japanese-generative-ai-survey

This repository is a dedicated working area for an external architecture review and possible reconstruction of `eariver/japanese-generative-ai-survey`.

The production repository is **not** this repository. Treat the upstream survey repository as an authority/reference source and keep it read-only during this exercise.

## Purpose

The current Generative AI Survey production system has become increasingly expensive to operate in both wall-clock time and LLM usage. Recent failures also showed that more process and more validation do not automatically produce better reader-facing results. The goal of this workspace is to let an external architecture reasoner examine the system from first principles and propose a simpler, cheaper, higher-quality operating model.

The immediate external architect is **Astra**, running through the official Codex harness. Astra is not being asked to become the production operator. The current production roles remain filled by the existing supervisory and operations agents until a redesigned architecture is reviewed and deliberately adopted.

## Start here

**Phase 5 is active; Phase 5-B is complete after independent review and repair.** No supported concrete case of removable reconstruction of comparison conditions was found; part of the observed work remains non-identifiable. Conditional Phase 5-C is not started. A real work difference and net savings remain unproven; no new architecture B or A/B cost trial has been selected. Phase 4 remains closed, and its renderer probe is not the default route.

Fresh sessions need only:

1. [Current Phase 5 continuation](handoff/astra-phase-5-continuation.md).
2. [Phase 5-B work observation assessment](outputs/astra-phase-5b-work-observation-assessment.md), sections 1 and 5–8.
3. Only necessary Evidence from the [5-B index](notes/phase-5b/README.md). Older decisions and lab probes remain historical evidence; the 5-A decision's section 2 restores Phase 4 conclusions.

Phase 5-B preserved fresh fixed sources, a strong post-cutoff HOLD, initial and repaired prose, independent source-first expectations/reviews and work observations. Its findings do not measure zero duplication or disprove the hypothesis across production. Do not repeat miniature articles to invent a comparison arm or count relocated work as saving. The next prioritization entry is one actual publication repair: which exact manuscript/public elements were reviewed, what reader-facing judgment was missed, and what checking costs. Existing editorial review must be considered before any new role or layer; no new trial/implementation is selected.

## Last recorded upstream reference

Production repository: `eariver/japanese-generative-ai-survey`

Observed 2026-09-13 JST: main `79a0ddea948af18ef02ec63184e67f99ad7f8e09`; W34 `c7faf207515e7429dd74abd5adaf2962725587ef`.

W34 had Human REQUEST_CHANGES, PR #490 integration, formal terminology repair and fresh publication generation. It is a **new RELEASE_CANDIDATE / Publication Preview pending**. Reader/Candidate bytes changed; old Human decisions do not approve the new bytes. Human Preview provenance is null and Freeze/Release remain pending. Terminology repair does not establish repair of earlier source/citation findings. PR #488/#489/#490 are existing baseline maintenance, not reconstruct achievements.

See the [5-B observation](notes/phase-5b/observation.json) and [limited change evidence](notes/phase-5b/production-change.json). The current Candidate raw SHA begins `6d18b496`, distinct from payload digest `d0af4c9c`. Full State validation, binding closure and PDF/full-edition quality review were not repeated. Do not assume the observed refs remain latest.

## Core principle

**Do not optimize one agent in isolation. Optimize total system work.**

The target system should reduce total Human + supervisory reasoning + production operations + CI/tooling work while preserving or improving publication quality, research sufficiency, provenance correctness, fail-close safety, and reproducibility.

## Working freedom

Astra may write analysis, notes, diagrams, and proposals in this repository. The upstream production repository must remain read-only during this architecture-review exercise.

Small read-only analytical probes are acceptable when they are cheaper than extended manual reasoning. Large replacement implementations, broad simulations, or production mutations are not the objective of the initial review and should not be undertaken unless Astra can justify that they are necessary to resolve a decisive architectural question.
