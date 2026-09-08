# Mission and Success Criteria

## Mission

Re-examine the architecture of `eariver/japanese-generative-ai-survey` from first principles and propose a production system that can create high-quality Weekly and Special editions with substantially less total work.

The optimization target is **the entire production system**, not one agent in isolation.

Minimize, where possible:

- supervisory reasoning wall-clock time;
- production-operations wall-clock time;
- LLM token / credit consumption;
- repeated source reads;
- handoffs between reasoning and operations roles;
- regeneration / repair loops;
- repeated exact-head audits;
- CI / tool runtime;
- artifact and checkpoint bookkeeping that exists only to support process machinery;
- Human effort needed to discover a bad editorial outcome.

Subject to these constraints:

- reader-facing publication quality must not decrease;
- research completeness and semantic fidelity must not decrease;
- provenance correctness must not decrease;
- fail-close behavior for crisp invariants must not become weaker without strong justification;
- Human decision authority must remain clear;
- reproducibility and historical traceability must remain defensible;
- Weekly and Special workflows must remain practically operable.

The preferred final state is a system where capable reasoning agents can usually follow a well-defined production pipeline to create Weekly and Special editions without repeated bespoke orchestration. Routine mechanics should be predictable and inexpensive; semantic judgment should remain autonomous where reasoning has real value.

## Current role abstraction

Do **not** design around current model names.

The current deployment happens to map roughly as follows:

- **Supervisory Reasoning Role** -> currently GPT-5.6 Sol
- **Production Operations Role** -> currently GPT-5.6 Luna / Work
- **Human Decision Authority** -> the owner

These are current bindings, not architectural invariants. Future GPT generations or non-OpenAI LLMs may fill either role. The current two-agent split is also reviewable: a better decomposition may be proposed if it lowers total cost while preserving quality and authority separation.

The roles are performed by capable reasoning agents, not deterministic programs. The architecture should automate routine mechanics without suppressing useful autonomous reasoning.

## Desired operating principle

A useful shorthand is:

> **Deterministic rails, bounded semantic autonomy.**

The pipeline should define, as appropriate:

- required inputs;
- required outputs;
- authority and provenance boundaries;
- crisp validation invariants;
- lifecycle / stop conditions;
- escalation conditions;
- Human decision surfaces.

It should avoid unnecessarily prescribing the internal reasoning path an LLM must take to satisfy those contracts.

The common path should be predictable. The reasoning itself should not be made rigid without a clear benefit.

## Important current symptom

The current system has accumulated both process complexity and operational cost.

A recent W34 production path produced an extreme editorial-compression outcome: a large research/evidence effort converged toward a Weekly issue that could effectively collapse to approximately two pages. The Human considered this an obvious quality failure. One identified contributing factor was excessive delegation of research/editorial judgment to the production operations agent.

PR #485 then introduced explicit governance requiring more independent supervisory review across Discovery, Evidence authority consumption, Materiality, Selection, Architecture, and the Human-facing Architecture dossier. This is a reasonable quality-recovery measure, but it also increases supervisory workload. The underlying architecture question remains open:

> Can the system prevent the same quality failure earlier and more reliably **without** shifting large amounts of repeated work from one reasoning agent to another?

## Avoid moving cost instead of removing it

A proposal is not an improvement if it merely:

- reduces production-agent work by moving the same semantic work to the supervisory agent;
- reduces supervisory work by blindly trusting production outputs;
- reduces Human work by lowering visibility into quality risk;
- reduces LLM work by adding excessive deterministic infrastructure and maintenance burden;
- reduces runtime while reducing editorial/research quality.

Prefer removal of duplicated work, earlier detection of failures, reusable authority/semantic products, clearer responsibility boundaries, and higher-leverage review points.

## Reuse before build

Avoid wheel reinvention where practical.

You may investigate and reuse ideas, standards, OSS, workflow systems, provenance/data-lineage approaches, content-addressed storage, state-machine patterns, research tooling, publication systems, agent orchestration approaches, CI/CD patterns, and relevant academic or industry work available on the public internet.

The current custom Core is not sacred. If a mature existing solution can replace custom machinery with less total complexity, evaluate it seriously.

However, introducing an external dependency is not automatically an improvement. Account for adapter cost, maintenance cost, context/tool overhead, operational complexity, lock-in, durability, and failure modes.

Do not conduct broad external research merely to maximize coverage. Research external solutions when doing so is likely to change an architectural decision or avoid unnecessary custom implementation.

## Success criteria for the architecture review

A strong result should explain:

1. what the current production system actually does;
2. why its complexity and work have grown;
3. where duplicate semantic/mechanical work occurs;
4. why the W34-style quality failure was detected late;
5. which current safeguards are essential and which are historical accumulation;
6. what should remain deterministic infrastructure;
7. what should remain reasoning-agent judgment;
8. what should remain Human authority;
9. what custom mechanisms could be simplified, merged, automated, removed, or replaced by existing technology;
10. what target architecture best reduces **total system work** while preserving or improving quality;
11. how the proposed system compares with the current system in expected wall-clock time, handoffs, repeated reads, regeneration loops, artifacts, review burden, and failure-detection latency;
12. how a migration could be staged without risking the production survey.

Quantitative estimates are welcome when supportable. Otherwise use explicit qualitative estimates such as LOW / MEDIUM / HIGH and state uncertainty.

## Non-goal

This initial exercise is **not** a request to rewrite the production system immediately.

The first deliverable is architectural understanding and a defensible proposal. Implementation decisions come only after independent review and Human discussion.
