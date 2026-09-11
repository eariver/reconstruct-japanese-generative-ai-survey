# reconstruct-japanese-generative-ai-survey

This repository is a dedicated working area for an external architecture review and possible reconstruction of `eariver/japanese-generative-ai-survey`.

The production repository is **not** this repository. Treat the upstream survey repository as an authority/reference source and keep it read-only during this exercise.

## Purpose

The current Generative AI Survey production system has become increasingly expensive to operate in both wall-clock time and LLM usage. Recent failures also showed that more process and more validation do not automatically produce better reader-facing results. The goal of this workspace is to let an external architecture reasoner examine the system from first principles and propose a simpler, cheaper, higher-quality operating model.

The immediate external architect is **Astra**, running through the official Codex harness. Astra is not being asked to become the production operator. The current production roles remain filled by the existing supervisory and operations agents until a redesigned architecture is reviewed and deliberately adopted.

## Start here

For the ongoing authorized architecture investigation, start with [the system direction reassessment](outputs/astra-system-direction-reassessment.md) (2026-09-12), especially sections 1, 5, and 7. It pauses further acceptance/staging implementation and prioritizes publication-quality and total-work comparison across research, editorial decisions, review, and repair. The initial-review reading list below is historical, not an instruction to restart Phase A.

Read these files before deep investigation:

1. `brief/00-mission-and-success-criteria.md`
2. `brief/01-human-and-supervisor-discussion-context.md`
3. `brief/02-current-system-reference.md`
4. `instructions/ASTRA_INITIAL_TASK.md`
5. `research/00-astra-usage-and-cost-context.md`

After that, investigate the upstream repository, its history, issues, pull requests, documentation, implementation, and relevant external sources as needed.

## Current upstream reference

Production repository: `eariver/japanese-generative-ai-survey`

Current `main` observed when this workspace was initialized:

`0a47a9b85108c5a2e9644037e7c0fb48b5bd96dc`

This commit merged PR #485 (`Core v2: enforce Sol/Luna review governance and full Architecture dossier`). It is a useful current baseline, not an architectural constraint.

## Core principle

**Do not optimize one agent in isolation. Optimize total system work.**

The target system should reduce total Human + supervisory reasoning + production operations + CI/tooling work while preserving or improving publication quality, research sufficiency, provenance correctness, fail-close safety, and reproducibility.

## Working freedom

Astra may write analysis, notes, diagrams, and proposals in this repository. The upstream production repository must remain read-only during this architecture-review exercise.

Small read-only analytical probes are acceptable when they are cheaper than extended manual reasoning. Large replacement implementations, broad simulations, or production mutations are not the objective of the initial review and should not be undertaken unless Astra can justify that they are necessary to resolve a decisive architectural question.
