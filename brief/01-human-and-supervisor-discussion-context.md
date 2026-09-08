# Human and Supervisory Discussion Context

This document summarizes the design conversation that led to this reconstruction exercise. It is intentionally a **problem/context document**, not a prescribed solution. Astra should use it as evidence of the Human's goals and observed pain points, while remaining free to disagree with proposed directions.

## 1. Why this exercise exists

The Human has become concerned that the Generative AI Survey production process is consuming more and more time for both major LLM roles:

- the current **Supervisory Reasoning Role** (today: GPT-5.6 Sol), and
- the current **Production Operations Role** (today: GPT-5.6 Luna / Work).

The concern is not simply that the system is complex. The more serious concern is that **operational effort has increased without a correspondingly reliable increase in reader-facing quality**.

A recent W34 path made the problem visible. A large research/evidence effort still converged toward an extremely compressed Weekly architecture, effectively capable of ending as an approximately two-page Weekly issue. The Human regarded this as an obvious bad outcome.

The diagnosis discussed in the production project was that the supervisory role had delegated too much research/editorial judgment to the operations role. Passing deterministic validation and having well-formed provenance did not prove that the research had been semantically consumed well enough to support a strong edition.

## 2. The immediate repair and its remaining problem

PR #485 (`Core v2: enforce Sol/Luna review governance and full Architecture dossier`) was created as a quality-governance correction.

It explicitly states two failures:

1. over-delegating research/editorial judgment to Luna/Work execution; and
2. requesting Architecture approval from an abbreviated machine-readiness summary before the Human could judge research sufficiency.

The governance introduced independent supervisory responsibility for areas including:

- Discovery completeness;
- Evidence authority consumption;
- iterative gap-fill judgment;
- Materiality and Selection;
- Architecture responsibility;
- omission and alternative analysis;
- the Human-facing Architecture Review dossier.

This repair is useful as a current production safeguard, but the Human's concern remains: **the supervisory role's own work time has not fallen much and may have increased further**.

The architecture-level question is therefore not "should Sol or Luna own this step?" but rather:

> Why does high-quality production currently require so much repeated work at all?

Astra should not treat PR #485 as the final answer. Treat it as a valuable record of a failure and the current emergency/production correction.

## 3. Do not optimize by transferring burden

The Human's desired outcome is deliberately demanding:

> Reduce total time and credit consumption for both major agent roles while improving, or at least preserving, publication quality.

Moving a review from Luna to Sol is not enough. Moving work from Sol back to Luna is also not enough.

The desired optimization target is the combined cost of:

- Human attention;
- supervisory semantic/review work;
- production execution/research work;
- deterministic tooling;
- CI and repeated validation;
- rework and regeneration;
- handoffs and context reconstruction.

## 4. Desired end-state intuition

The Human would like Weekly and Special editions to become much closer to **repeatable production pipelines**.

Ideally, once the system is mature, the two major reasoning roles should be able to follow a relatively stable path and produce an edition without needing a new bespoke orchestration plan each time.

However, the Human does **not** want this to become a rigid deterministic factory that suppresses LLM reasoning. Both major roles are capable reasoning agents.

The discussed intuition is:

- automate routine mechanics;
- make state/authority/quality/stop boundaries clear;
- let capable LLMs retain autonomy over semantic/research/editorial reasoning where that autonomy adds value;
- escalate expensive deeper review when risk/anomaly indicates it, rather than repeating full manual-style review everywhere by default.

This intuition is not a required architecture. Astra should test whether it is actually optimal.

## 5. Model names must not become architecture

The terms "Sol" and "Luna" are current implementation bindings only.

The Human expects model names and providers to change over time. Future roles may be filled by newer GPT models or by non-OpenAI LLMs. The Human is not planning to abandon GPT-based workflows, but does not want the architecture coupled to current product/model names.

Use abstract roles instead:

- **Supervisory Reasoning Role** — currently Sol;
- **Production Operations Role** — currently Luna / Work;
- **Human Decision Authority** — the owner.

Astra is free to propose a different role decomposition if the current two-role split is not optimal.

The important invariant is not necessarily "two different models". The important question is how to preserve appropriate separation between generation/execution and high-impact semantic/authority judgment without duplicating large amounts of work.

## 6. Avoid wheel reinvention

The Human explicitly does not want the project to keep inventing custom machinery when mature external solutions already exist.

Astra is allowed and encouraged to use public internet sources, GitHub repositories, OSS projects, standards, papers, workflow patterns, agent orchestration systems, provenance/data-lineage approaches, publishing systems, and other relevant external work.

The goal is not to preserve the current custom Core at all costs.

At the same time, external dependencies have real costs. A library/service/tool that saves 200 lines of custom code but adds a large adapter, plugin/context surface, or fragile operational dependency may be worse overall. Evaluate total-system cost.

## 7. Astra itself should not be over-constrained

Before creating this workspace, the Human and supervisory assistant discussed Astra usage cost. Community reports collected separately suggested that open-ended implementation, simulation, Computer Use, broad tool loops, and heavy harness behavior can consume Plus allowance quickly.

The first instinct was to impose many strict rules. The Human then raised an important counter-concern: **over-constraining Astra could itself increase cost** by making investigation inefficient, causing shallow results, repeated reads, or extra follow-up tasks.

The agreed direction is therefore:

- give Astra the proposition, context, safety boundary, and desired outcome;
- let Astra decide how to investigate and model the architecture;
- Human and supervisory assistant should mostly observe and provide factual clarification or advice if requested;
- do not pre-decide Astra's solution;
- do not prescribe a rigid file-read order or exact tool-call budget;
- allow small read-only analytical probes if they are genuinely efficient;
- avoid large implementation/simulation during the first architecture phase unless Astra believes it is necessary to settle a decisive question and can explain why.

In short:

> **Strong safety boundary, high reasoning freedom.**

## 8. Current execution experiment

For the first architecture review, the Human intends to use:

- official Codex harness;
- Astra;
- Medium reasoning as the current starting hypothesis;
- Fast mode off;
- upstream production repository read-only;
- this reconstruction repository as Astra's writable workspace.

These settings are not themselves architectural requirements. Astra may recommend a better investigation strategy if it believes one exists.

## 9. What would be an interesting result

A particularly valuable result would not simply list existing process defects. It would show how to reduce **work amplification**.

Examples of questions worth investigating include:

- Is the same source being semantically read multiple times by different agents/stages?
- Are some reviews happening too early or too often?
- Are quality failures being detected too late?
- Have governance/checkpoint/validator layers accumulated faster than obsolete layers are removed?
- Can one authoritative semantic extraction be safely reused downstream?
- Can anomaly detection trigger deeper review only when needed?
- Are repeated exact-head audits/checkpoint rebinding necessary at their current frequency?
- Can existing workflow/provenance/publication technology replace custom infrastructure?
- Which controls actually prevent historically observed failures, and which merely document them?

Again, these are investigation prompts, not expected conclusions.
