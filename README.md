# reconstruct-japanese-generative-ai-survey

This repository is a dedicated working area for an external architecture review and possible reconstruction of `eariver/japanese-generative-ai-survey`.

The production repository is **not** this repository. Treat the upstream survey repository as an authority/reference source and keep it read-only during this exercise.

## Purpose

The current Generative AI Survey production system has become increasingly expensive to operate in both wall-clock time and LLM usage. Recent failures also showed that more process and more validation do not automatically produce better reader-facing results. The goal of this workspace is to let an external architecture reasoner examine the system from first principles and propose a simpler, cheaper, higher-quality operating model.

The immediate external architect is **Astra**, running through the official Codex harness. Astra is not being asked to become the production operator. The current production roles remain filled by the existing supervisory and operations agents until a redesigned architecture is reviewed and deliberately adopted.

## Start here

**Phase 5 is active; Phase 5-A is complete.** The next step is to observe whether one reader question causes avoidable reconstruction of the same comparison conditions during research and later editing. A real work difference and net savings remain unproven; no new architecture B or A/B cost trial has been selected. Phase 4 remains closed, and its renderer probe is not the default route.

Fresh sessions need only:

1. [Current Phase 5 continuation](handoff/astra-phase-5-continuation.md).
2. [Phase 5-A work-unit decision](outputs/astra-phase-5a-work-unit-decision.md), sections 1 and 3–6; section 2 restores Phase 4 conclusions.
3. Only necessary Evidence from its index. Older decisions and lab probes remain historical evidence.

Phase 5-B is a bounded observation through research, reader prose, independent review and repair, with fresh sources and strong HOLD/exclusion possibilities. Candidate-level storage does not imply separate cognitive work, and current governance already supports cross-candidate grouping. Reject the hypothesis if only necessary verification/review remains; commonize benefits available to the same workflow. Full Core or renderer implementation is not a prerequisite. Do not invent a comparison arm or count relocated work as saving.

## Last recorded upstream reference

Production repository: `eariver/japanese-generative-ai-survey`

Observed 2026-09-13 JST: main `14781409f6fb8d79e3eb4ad6b4c457764a038fde`; W34 `5561e2328a09061a3e0c8e881d24ddcb03e1e975`.

Real W34 is now **RELEASE_CANDIDATE / Publication Preview pending**, following PR #489 revalidation. Human Preview approval and Release are not established. Existing Candidate and reader bytes are unchanged; upstream meaning/source findings remain. PR #488's bibliography repair and PR #489's publication-only revalidation are baseline repairs and should not be duplicated.

See the [5-A observation](notes/phase-5a/observation.json): the delta from 4-H is one worklog ancestry correction only. The [4-H limited binding checks](notes/phase-4h/refresh-result.json) remain historical checks, not a new 5-A full validation or quality review. Do not assume the observed refs remain latest.

## Core principle

**Do not optimize one agent in isolation. Optimize total system work.**

The target system should reduce total Human + supervisory reasoning + production operations + CI/tooling work while preserving or improving publication quality, research sufficiency, provenance correctness, fail-close safety, and reproducibility.

## Working freedom

Astra may write analysis, notes, diagrams, and proposals in this repository. The upstream production repository must remain read-only during this architecture-review exercise.

Small read-only analytical probes are acceptable when they are cheaper than extended manual reasoning. Large replacement implementations, broad simulations, or production mutations are not the objective of the initial review and should not be undertaken unless Astra can justify that they are necessary to resolve a decisive architectural question.
