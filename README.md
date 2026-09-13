# reconstruct-japanese-generative-ai-survey

This repository is a dedicated working area for an external architecture review and possible reconstruction of `eariver/japanese-generative-ai-survey`.

The production repository is **not** this repository. Treat the upstream survey repository as an authority/reference source and keep it read-only during this exercise.

## Purpose

The current Generative AI Survey production system has become increasingly expensive to operate in both wall-clock time and LLM usage. Recent failures also showed that more process and more validation do not automatically produce better reader-facing results. The goal of this workspace is to let an external architecture reasoner examine the system from first principles and propose a simpler, cheaper, higher-quality operating model.

The immediate external architect is **Astra**, running through the official Codex harness. Astra is not being asked to become the production operator. The current production roles remain filled by the existing supervisory and operations agents until a redesigned architecture is reviewed and deliberately adopted.

## Start here

**Phase 5 is active.** The reader-review execution plan is concrete, and current Freeze/Release runtime contract mismatches have limited local witnesses. The next candidate is an isolated repair of those producer/validator boundaries. Conditional Phase 5-C remains unstarted; the Human corrected the misleading `Astra work Phase 5-C` commit title. Net savings and architecture adoption remain unproven. Phase 4 stays closed.

Fresh sessions need only:

1. [Current Phase 5 continuation](handoff/astra-phase-5-continuation.md).
2. [Review plan and runtime priority](outputs/astra-phase-5-review-plan-and-runtime-priority.md), sections 1–2 and 4–6; section 3 contains the completed reader-review plan.
3. Only necessary [Evidence](notes/phase-5-review-plan/evidence.md). The publication review boundary investigation, 5-B assessment and older decisions remain historical; the 5-A decision's section 2 restores Phase 4 conclusions.

Human already carried a scoped pre-TeX reader-surface gate forward to W35+. The plan now aligns with that request, preserves final PDF/Human review, and does not reopen W34's accepted editorial debt. No new reader trial ran. Fresh production evidence also exposed deterministic freeze/release contract mismatches requiring runtime adjustment/recovery. A small isolated repair is now the next priority; no repair implementation or production mutation has occurred. Moving work to another role or merely writing PASS is not saving.

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
