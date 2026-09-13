# reconstruct-japanese-generative-ai-survey

This repository is a dedicated working area for an external architecture review and possible reconstruction of `eariver/japanese-generative-ai-survey`.

The production repository is **not** this repository. Treat the upstream survey repository as an authority/reference source and keep it read-only during this exercise.

## Purpose

The current Generative AI Survey production system has become increasingly expensive to operate in both wall-clock time and LLM usage. Recent failures also showed that more process and more validation do not automatically produce better reader-facing results. The goal of this workspace is to let an external architecture reasoner examine the system from first principles and propose a simpler, cheaper, higher-quality operating model.

The immediate external architect is **Astra**, running through the official Codex harness. Astra is not being asked to become the production operator. The current production roles remain filled by the existing supervisory and operations agents until a redesigned architecture is reviewed and deliberately adopted.

## Start here

**Phase 4-F's bounded source-join trace is complete, including the PR #489 production refresh.** The archived timing report already exists; compact authoring and Card generation lose its statement-specific source binding. Existing canonical fields can express a reference repair. Full publication quality and net lifecycle savings remain unproven. Phase 3 remains closed.

Fresh Astra sessions need only:

1. [Current Phase 4 handoff](handoff/astra-phase-4-continuation.md).
2. [Phase 4-F assessment](outputs/astra-phase-4f-source-join-assessment.md), sections 1 and 3–6.
3. Only necessary Evidence from its index. Earlier Phase 4 decisions remain historical context.

Next compare the concrete authoring, transform, review and repair work of extending compact helpers versus authoring existing canonical artifacts directly and deriving presentation data. Use the known source-binding and Draft/renderer examples to identify removable duplication; do not count transferred work as savings. Further acceptance/staging/cache implementation remains paused. Old chat logs, repeated source searches and lab reruns are not mandatory resume inputs.

## Last recorded upstream reference

Production repository: `eariver/japanese-generative-ai-survey`

Last recorded production `main` (2026-09-13 JST):

`14781409f6fb8d79e3eb4ad6b4c457764a038fde`

PR #488 repaired bibliography internal-note generation. PR #489 adds a State-bound immutable publication-only revalidation path after reviewed Core changes, preserving upstream checkpoint-bound bytes. Include these repairs in the comparison baseline. They do not repair the source bindings or the upstream Draft boundary example.

W34 remains at `f50d229...`, with a `READY_FOR_PUBLICATION_PREVIEW` Candidate record and observed State `VALIDATED_DRAFT`. The PR's disposable-copy advance is not a real W34 advance or Human approval. See the [current observation](notes/phase-4f/production-refresh-489.json) and handoff. Earlier refs remain fixed historical Evidence; do not assume observed refs remain latest.

## Core principle

**Do not optimize one agent in isolation. Optimize total system work.**

The target system should reduce total Human + supervisory reasoning + production operations + CI/tooling work while preserving or improving publication quality, research sufficiency, provenance correctness, fail-close safety, and reproducibility.

## Working freedom

Astra may write analysis, notes, diagrams, and proposals in this repository. The upstream production repository must remain read-only during this architecture-review exercise.

Small read-only analytical probes are acceptable when they are cheaper than extended manual reasoning. Large replacement implementations, broad simulations, or production mutations are not the objective of the initial review and should not be undertaken unless Astra can justify that they are necessary to resolve a decisive architectural question.
