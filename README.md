# reconstruct-japanese-generative-ai-survey

This repository is a dedicated working area for an external architecture review and possible reconstruction of `eariver/japanese-generative-ai-survey`.

The production repository is **not** this repository. Treat the upstream survey repository as an authority/reference source and keep it read-only during this exercise.

## Purpose

The current Generative AI Survey production system has become increasingly expensive to operate in both wall-clock time and LLM usage. Recent failures also showed that more process and more validation do not automatically produce better reader-facing results. The goal of this workspace is to let an external architecture reasoner examine the system from first principles and propose a simpler, cheaper, higher-quality operating model.

The immediate external architect is **Astra**, running through the official Codex harness. Astra is not being asked to become the production operator. The current production roles remain filled by the existing supervisory and operations agents until a redesigned architecture is reviewed and deliberately adopted.

## Start here

**Phase 5 is active.** Current upstream reconciliation and bounded root review are complete. Production supersedes the old missing Release report repair; two Freeze mismatches and reader binding/coverage/scope gaps remain. Independent review, adoption and net lifecycle savings remain unproven. Conditional Phase 5-C remains unstarted, regardless of the corrected historical commit title. Phase 4 stays closed.

Fresh sessions need only:

1. [Current Phase 5 continuation](handoff/astra-phase-5-continuation.md).
2. [Current upstream assessment](outputs/astra-phase-5-upstream-reconciliation-assessment.md), sections 1–4 for disposition and next scope, section 5 for limits.
3. Necessary [Evidence](notes/phase-5-upstream-reconciliation/README.md). Earlier decisions and the old candidate/test results remain historical.

Next is current-Core residual Freeze repair, followed by a separate reader projection/binding/scope repair. Do not apply or review the old patch wholesale over the upstream fixes. No production change or new independent agent was executed. No reader trial or conditional 5-C ran. Function/schema witnesses and old local retry tests are not full workflow, publication-quality or lifecycle-cost proof.

## Last recorded upstream reference

Production repository: `eariver/japanese-generative-ai-survey`

Observed 2026-09-15 JST: main `774dd39a951c9ac3818e83dfffd4c7666efb0a20`. Current compare: 8 commits / 16 changed files from `3e3eebe0`.

W34 is **RELEASED / next null on main**. Its actual Release checkpoint matches the State pointer and passes the current schema. #495 implements Release dual-review authority, and #496 adds the reader gate. #492 remains the bibliography access-provenance baseline. These are upstream achievements, not reconstruct adoption or savings.

See the [current observation](notes/phase-5-upstream-reconciliation/observation.json) and [bounded witnesses](notes/phase-5-upstream-reconciliation/probe-results.json). Branch/public asset/PDF and full State/dependency validation were not refreshed. Earlier exact-byte checks and branch FROZEN status remain historical in the handoff. Do not assume the observed refs remain latest.

## Core principle

**Do not optimize one agent in isolation. Optimize total system work.**

The target system should reduce total Human + supervisory reasoning + production operations + CI/tooling work while preserving or improving publication quality, research sufficiency, provenance correctness, fail-close safety, and reproducibility.

## Working freedom

Astra may write analysis, notes, diagrams, and proposals in this repository. The upstream production repository must remain read-only during this architecture-review exercise.

Small read-only analytical probes are acceptable when they are cheaper than extended manual reasoning. Large replacement implementations, broad simulations, or production mutations are not the objective of the initial review and should not be undertaken unless Astra can justify that they are necessary to resolve a decisive architectural question.
