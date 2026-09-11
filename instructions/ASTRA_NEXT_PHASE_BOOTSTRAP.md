# Astra next-phase bootstrap

> **HISTORICAL — superseded as a resume entry after Phase 3-G.** Fresh sessions use [ASTRA_POST_PHASE_3_BOOTSTRAP.md](ASTRA_POST_PHASE_3_BOOTSTRAP.md) and [Phase 3 closeout](../handoff/astra-phase-3-session-closeout.md). The decision-only output and same-session authorization procedure below applied to the post-Phase-A step; do not replay them by default. This text is retained as historical instruction provenance.

Date: 2026-09-09 JST  
Status: **NEXT-PHASE DECISION BOOTSTRAP / NO PRODUCTION ADOPTION**

## 1. Purpose

This instruction starts a new Astra reasoning session after completion of Phase A, its refinement, and the prior-session closeout.

Astra remains the **Architecture / Policy Decision Role** for this experiment. The Human remains the final decision authority for adoption, priority, migration, and Human Gates. Sol remains the independent supervisory/review role.

The purpose of this first step is **not** to have Sol or the Human preselect the next implementation path. Astra should determine what the next phase ought to be from the durable decision state and current production reality.

Past Astra recommendations are inputs, not immutable architecture authority. Astra may retain, revise, reorder, combine, postpone, or reject them when newer evidence, current production reality, or better reasoning supports doing so.

## 2. Objective function

Choose the next phase in service of the existing system objective:

```text
Minimize total system work:
  Production Operations work
+ Supervisory review/reasoning work
+ repair iterations
+ regeneration and CI/runtime
+ LLM credits/usage
+ operational complexity
+ Human handoff/manual burden

Subject to:
  publication quality >= current intended quality
  provenance correctness >= current
  fail-close safety >= current
  Human authority preserved
  Weekly/Special generality preserved
  historical reproducibility preserved
```

Moving work from one role to another is not an improvement by itself.

## 3. Selective reload

Do not begin by rereading the whole repository or replaying Phase A.

Use this order unless the question you are investigating makes another narrow path more informative:

1. `handoff/astra-phase-a-session-closeout.md`
2. `outputs/astra-phase-a-architecture-refinement.md` — start with §1 and §10; read other sections only as needed
3. `context/2026-09-09_post-refinement-human-sol-discussion.md` — especially the remaining Sol guards and Human role intent when relevant
4. Only when needed for a concrete decision: `notes/phase-a-evidence.md`, the relevant part of the original Phase A report, and exact upstream production artifacts

Treat the closeout as a compact decision-state handoff, not as a command to preserve every prior conclusion.

## 4. Fresh production grounding

Before relying on implementation or schema details, obtain the **current** remote reality of:

- `eariver/reconstruct-japanese-generative-ai-survey`
- `eariver/japanese-generative-ai-survey`

Do not assume the Phase A production baseline is still current.

The production repository is read-only for this exercise. Inspect only the schemas, producers, consumers, history, artifacts, or contracts that are necessary to decide the next phase. Prefer targeted reads with high information gain over broad crawling.

## 5. Decision task

Determine the **single next phase** that is currently most valuable for reducing uncertainty and moving toward a lower-total-work production system without weakening the safety constraints above.

You may perform bounded read-only investigation needed to make that decision.

In particular, decide for yourself whether the next useful step is primarily architecture/design, current-schema/producer/consumer mapping, feasibility validation, shadow-evaluation preparation, a narrow independent maintenance issue, or something else. These are examples, not a required menu or priority order.

Do not assume that previously discussed candidates such as a Consumption Record, generated resume, blind critic, cross-family model, shadow Weekly/Special run, or a particular role topology must be selected or implemented.

When choosing the phase, explicitly distinguish:

- observed facts;
- working hypotheses;
- unresolved evidence dependencies;
- production safety constraints;
- choices that remain Human adoption decisions.

## 6. First-step output

Create one primary durable decision artifact:

`outputs/astra-next-phase-decision.md`

Keep supporting artifacts to the minimum actually needed.

The decision artifact should make the following clear, using whatever structure best fits your reasoning:

- the selected next phase and its purpose;
- why this phase has the highest information/value now;
- current evidence and production reality that materially affected the choice;
- important alternatives considered and why they are deferred or rejected;
- the uncertainty or bottleneck this phase is intended to resolve;
- the bounded execution scope and non-goals;
- the stop boundary;
- what evidence or result would cause the direction to change;
- what should be executed in the immediate same-session follow-up if the Human permits continuation.

Do not turn this artifact into a detailed implementation instruction unless the selected next phase itself requires that level of design to justify the choice.

## 7. Safety and authority boundary

For this decision step:

- do not mutate `eariver/japanese-generative-ai-survey`;
- do not create or alter production State, Human decisions, Gates, Freeze, Release, or publication authority;
- do not weaken exact-byte, provenance, fail-close, or Human-authority guarantees;
- do not treat reused semantic work as current-edition acceptance without new evidence sufficient to justify changing that rule;
- do not optimize only for Weekly at the expense of Special generality;
- do not start production adoption or migration;
- routine Git Pull/Push transport is Human-operated unless the Human explicitly directs otherwise.

`eariver/reconstruct-japanese-generative-ai-survey` remains the writable reasoning/design workspace.

## 8. Stop condition

After the next phase is selected and `outputs/astra-next-phase-decision.md` is complete, **stop before executing that selected phase**.

The intended operating pattern is that the Human may then give a short follow-up prompt in the **same Astra session** authorizing execution of the phase Astra just defined. This preserves the reasoning context without making the first prompt pre-authorize implementation, production migration, or a large experiment.
