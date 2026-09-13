# reconstruct-japanese-generative-ai-survey

This repository is a dedicated working area for an external architecture review and possible reconstruction of `eariver/japanese-generative-ai-survey`.

The production repository is **not** this repository. Treat the upstream survey repository as an authority/reference source and keep it read-only during this exercise.

## Purpose

The current Generative AI Survey production system has become increasingly expensive to operate in both wall-clock time and LLM usage. Recent failures also showed that more process and more validation do not automatically produce better reader-facing results. The goal of this workspace is to let an external architecture reasoner examine the system from first principles and propose a simpler, cheaper, higher-quality operating model.

The immediate external architect is **Astra**, running through the official Codex harness. Astra is not being asked to become the production operator. The current production roles remain filled by the existing supervisory and operations agents until a redesigned architecture is reviewed and deliberately adopted.

## Start here

**Phase 5 is active.** An isolated Freeze/Release repair candidate is implemented and tested against synthetic publication authority chains. Independent review, adoption and net lifecycle savings remain unproven. Conditional Phase 5-C remains unstarted, regardless of the corrected historical commit title. Phase 4 stays closed.

Fresh sessions need only:

1. [Current Phase 5 continuation](handoff/astra-phase-5-continuation.md).
2. [Runtime repair assessment](outputs/astra-phase-5-runtime-repair-assessment.md), sections 1 and 3–5; section 2 describes the patch.
3. Necessary [Evidence](notes/phase-5-runtime-repair/README.md), including the distinction between the first regression run and isolated Git-aware follow-up. Earlier decisions remain historical.

The candidate resolves approved Candidate/visual authority and Freeze/Release producer–controller agreement. Next is bounded review and Shared Core maintenance disposition, checking for an existing upstream fix first. No production change or new independent agent was executed. The reader-review plan is complete; no reader trial or conditional 5-C ran. Local retry tests are not a complete Actions redispatch or lifecycle-cost proof.

## Last recorded upstream reference

Production repository: `eariver/japanese-generative-ai-survey`

Observed 2026-09-14 JST: main `3e3eebe0cda3a32ac88ae764d279b37768f6bfca`; W34 branch `3bad8a57cf2b246c7f71cb749ba3105fa318b073`.

W34 is **RELEASED / COMPLETE on main**, after PR #493 integrated frozen authority and release provenance was recovered. Its branch remains FROZEN / stage:release. Human-approved r3 bytes were preserved. Public Release metadata is non-draft/non-prerelease with the matching PDF digest. Core #492 remains the shared bibliography access-provenance baseline. These production results do not resolve every earlier source/citation finding or establish reconstruct savings.

See the [current observation](notes/phase-5-review-plan/observation.json) and [local checks](notes/phase-5-review-plan/check.json). Candidate raw SHA begins `df376f47`, distinct from payload digest `52c8d0bc`; PDF SHA begins `e93db71a`. Freeze/Release and selected authority bindings were checked. Full State/dependency validation, independent public-asset download and PDF/full-edition quality review were not repeated. Do not assume the observed refs remain latest.

## Core principle

**Do not optimize one agent in isolation. Optimize total system work.**

The target system should reduce total Human + supervisory reasoning + production operations + CI/tooling work while preserving or improving publication quality, research sufficiency, provenance correctness, fail-close safety, and reproducibility.

## Working freedom

Astra may write analysis, notes, diagrams, and proposals in this repository. The upstream production repository must remain read-only during this architecture-review exercise.

Small read-only analytical probes are acceptable when they are cheaper than extended manual reasoning. Large replacement implementations, broad simulations, or production mutations are not the objective of the initial review and should not be undertaken unless Astra can justify that they are necessary to resolve a decisive architectural question.
