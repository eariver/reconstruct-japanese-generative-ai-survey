# reconstruct-japanese-generative-ai-survey

This repository is a dedicated working area for an external architecture review and possible reconstruction of `eariver/japanese-generative-ai-survey`.

The production repository is **not** this repository. Treat the upstream survey repository as an authority/reference source and keep it read-only during this exercise.

## Purpose

The current Generative AI Survey production system has become increasingly expensive to operate in both wall-clock time and LLM usage. Recent failures also showed that more process and more validation do not automatically produce better reader-facing results. The goal of this workspace is to let an external architecture reasoner examine the system from first principles and propose a simpler, cheaper, higher-quality operating model.

The immediate external architect is **Astra**, running through the official Codex harness. Astra is not being asked to become the production operator. The current production roles remain filled by the existing supervisory and operations agents until a redesigned architecture is reviewed and deliberately adopted.

## Start here

**Phase 4 is closed.** Its canonical connection probe stopped at a source-metadata aggregation counterexample before section output or repair/regeneration. Further local renderer work is no longer the default route. Full canonical quality and total lifecycle savings remain unproven; the reconstruction objective continues.

Fresh sessions need only:

1. [Current continuation / Phase 4 closeout](handoff/astra-phase-4-continuation.md).
2. [Phase 4-H closure decision](outputs/astra-phase-4h-connection-and-closeout.md), sections 1 and 4–6; section 2 for production reality.
3. Only necessary Evidence from its index. Older decisions and lab probes remain historical evidence.

Next identify a concrete difference in research/editorial work units worth comparing through publication, independent review and repair. Full Core or renderer implementation is not a prerequisite. Continuous ownership is already present, and faithful compact input can converge with assisted canonical authorship. Do not invent a comparison arm or count relocated work as saving.

## Last recorded upstream reference

Production repository: `eariver/japanese-generative-ai-survey`

Observed 2026-09-13 JST: main `14781409f6fb8d79e3eb4ad6b4c457764a038fde`; W34 `8480f4dfffb57b456d1147fcc5360f7864bb19df`.

Real W34 is now **RELEASE_CANDIDATE / Publication Preview pending**, following PR #489 revalidation. Human Preview approval and Release are not established. Existing Candidate and reader bytes are unchanged; upstream meaning/source findings remain. PR #488's bibliography repair and PR #489's publication-only revalidation are baseline repairs and should not be duplicated.

See the [observation](notes/phase-4h/observation.json) and [limited binding checks](notes/phase-4h/refresh-result.json). Earlier refs remain historical; do not assume the observed refs remain latest.

## Core principle

**Do not optimize one agent in isolation. Optimize total system work.**

The target system should reduce total Human + supervisory reasoning + production operations + CI/tooling work while preserving or improving publication quality, research sufficiency, provenance correctness, fail-close safety, and reproducibility.

## Working freedom

Astra may write analysis, notes, diagrams, and proposals in this repository. The upstream production repository must remain read-only during this architecture-review exercise.

Small read-only analytical probes are acceptable when they are cheaper than extended manual reasoning. Large replacement implementations, broad simulations, or production mutations are not the objective of the initial review and should not be undertaken unless Astra can justify that they are necessary to resolve a decisive architectural question.
