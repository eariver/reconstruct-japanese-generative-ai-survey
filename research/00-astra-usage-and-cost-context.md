# Astra Usage and Cost Context

This file is operational context for the architecture-review exercise. It is **not** evidence about the Survey architecture itself.

The Human asked Grok to survey recent X posts about Astra usage, especially allowance burn, harness overhead, Computer Use, unconstrained implementation/simulation, and ways to reduce waste. The underlying source set was intentionally biased toward direct-use reports rather than hype/showcase posts.

## Why this matters

The architecture-review exercise is being run under a limited-use plan. The goal is therefore not only to design a more efficient Survey pipeline, but also to avoid wasting Astra allowance while investigating it.

At the same time, the Human explicitly rejected the idea of over-constraining Astra with a rigid read order, tiny tool-call budget, or predetermined solution. Excessive constraints may force shallow analysis, repeated reads, or follow-up tasks and can therefore increase total cost.

The operating principle for this exercise is:

> **Strong safety boundary, high reasoning freedom, cost-aware investigation.**

## Field-report summary

The Grok survey found the following recurring signals in recent X usage reports:

- Plus users often reported the nominal five-hour usage window being consumed surprisingly quickly under medium/high agentic workloads, sometimes within roughly 8–30 minutes of active work.
- Computer Use / browser-heavy workflows were repeatedly described as high-burn compared with direct static/CLI/API-style work when those alternatives were available.
- Open-ended implementation, recursive verification loops, spontaneous helper scripts, simulations, and long autonomous coding sessions were repeatedly associated with high burn.
- Several independent users reported that lighter third-party harnesses such as OpenCode / OhMyPi felt more efficient than the full Codex harness for the same or similar models.
- However, the harness comparison evidence was mostly anecdotal; rigorous same-task quantitative Codex-vs-OpenCode-vs-OhMyPi benchmarks were scarce.
- Some Codex users reported acceptable efficiency when they stayed on lower effort settings, minimized skills/context overhead, used compaction, and explicitly stopped work when the task was complete.
- Multiple users advised minimizing unnecessary Skills / MCP / Plugin / tool definitions because of context/tool overhead.
- Well-scoped analysis/review work appeared capable of much lower burn than unconstrained implementation-heavy sessions in some counter-examples.

## Selected source examples from the Grok ledger

These are included only so the origin of the operational assumptions is visible. Do not spend Astra budget revalidating every post unless it affects a decision about how to execute this architecture review.

- https://x.com/AM09_21/status/2097096616138481807 — starting-point post; argues for lighter harnesses, fewer Skills/MCP/Plugins, classical tests over unnecessary Computer Use, and strong hooks/constraints.
- https://x.com/webtkdev/status/2096150167229772109 — Plus usage report with Medium/Light exhaustion observations.
- https://x.com/cedric_chee/status/2096154535542870308 — concrete Plus burn report with token/cost estimate on a non-trivial task.
- https://x.com/TrevBizz/status/2096451454533771753 — Plus coding task exhausting limit and requiring added credits.
- https://x.com/Sushilk91/status/2097340649439981639 — reports Computer Use/token hunger and spontaneous scripts/checkpoint behavior.
- https://x.com/EdwardDGregory/status/2097337522632147072 — heavy High/test workload exhausting a large weekly allowance.
- https://x.com/mjs022/status/2097326344782712941 — direct user comparison suggesting OpenCode felt lighter than Codex in a heavy Rust workflow.
- https://x.com/nuno_ferreira/status/2097337211196678414 — counter-example of relatively low reported burn on a well-scoped review/browsing task.

## Confidence and uncertainty

Treat these as **field signals**, not precise engineering measurements.

The survey explicitly found weak evidence for:

- exact accounting formulas behind the five-hour window / weekly limits;
- exact token multipliers for each tool category;
- controlled same-task harness comparisons;
- long-duration behavior under perfectly bounded prompts;
- whether lower reasoning effort always minimizes total cost on architecture tasks.

In particular, the conclusion "OpenCode is always more efficient than Codex" is **not** established. The signal is plausible and repeated, but only partially supported.

## How this should influence the present task

The Human chose to try the **official Codex harness** for this first Astra architecture review despite the lighter-harness field signal.

The current starting strategy is:

- Astra through official Codex;
- Medium reasoning as a starting point for a systems-architecture task;
- Fast mode off;
- upstream production repository read-only;
- static repository/history analysis preferred when sufficient;
- Computer Use not forbidden, but should be used only when it materially improves the investigation;
- large implementation/prototype/simulation work is not the objective of Phase A;
- small read-only analytical probes are allowed when they reduce total reasoning/tool effort.

These are **operational preferences**, not a rigid harness contract. If a different tactic is clearly more efficient for reaching a high-confidence architectural conclusion, Astra may use it within the safety boundary.

## The key meta-objective

Apply the same principle to your own investigation that you are being asked to apply to the Survey:

> Minimize work that is unlikely to change the result, but do not save cost by lowering the quality of the decision.
