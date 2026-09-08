# Astra Initial Task — External Architecture Reconstruction (Phase A)

## Your role in this exercise

Act as an **external systems architect** for the Generative AI Survey production system.

You are not being asked to become its production operator, to defend its current architecture, or to immediately rewrite it. Your first job is to understand the current system well enough to propose a materially better production architecture.

This workspace is intentionally separate from the production repository so that you can reason freely without risking production state.

## Proposition

Reconstruct the Generative AI Survey production architecture so that **total system work is substantially reduced while reader-facing quality is preserved or improved**.

The target is not to optimize one agent in isolation.

Reduce, where possible, the combined cost of:

- Human attention;
- supervisory reasoning / semantic review;
- production research and execution;
- LLM token / credit usage;
- Sol-like / Luna-like handoffs;
- repeated source reads;
- repair and regeneration cycles;
- exact-head re-audits and repeated authority reconciliation;
- CI / deterministic-tool runtime;
- process-only artifacts and checkpoint bookkeeping;
- late discovery of editorial/research quality failures.

At the same time, do not reduce:

- publication quality;
- research sufficiency;
- semantic fidelity;
- provenance correctness;
- reproducibility;
- appropriate fail-close safety;
- meaningful Human decision authority.

## Important observed failure

The current process has become slower for both major LLM roles. At the same time, a recent W34 path showed that large research/evidence effort could still converge toward an obviously over-compressed Weekly outcome, effectively around two pages.

A subsequent governance repair (PR #485) corrected over-delegation of semantic/editorial judgment by adding stronger independent supervisory reviews. That is current production policy, but it also adds supervisory work.

Treat this as a central architecture problem:

> Can the system detect and prevent this kind of quality failure earlier and more reliably, while doing **less total repeated work**, rather than merely transferring work from one agent to another?

Do not assume PR #485 is either wrong or optimal. Study why it exists and what failure it prevents.

## Model-agnostic roles

Do not design around the current model/product names.

Current bindings happen to be approximately:

- **Supervisory Reasoning Role** -> GPT-5.6 Sol
- **Production Operations Role** -> GPT-5.6 Luna / Work
- **Human Decision Authority** -> owner

These are implementation bindings, not architecture invariants.

Either LLM role may later be filled by a newer GPT generation or a non-OpenAI model. You may also recommend a different role decomposition if the current two-role split is not optimal.

Remember that these roles are capable reasoning agents. Do not replace useful semantic autonomy with procedural detail merely because deterministic workflow is easier to specify.

A desirable system may have predictable **rails** for routine production while retaining autonomous reasoning at points where semantic judgment has real value. This is an intuition to evaluate, not a mandated solution.

## Reuse before build

Avoid wheel reinvention where practical.

You are explicitly allowed to use public external sources beyond the current project, including:

- public GitHub repositories;
- mature OSS;
- standards and established engineering patterns;
- workflow/state-machine systems;
- provenance and data-lineage systems;
- content-addressed storage approaches;
- research tooling;
- publishing/document-production systems;
- agent orchestration approaches;
- relevant papers and industry material.

The current custom Core is not sacred.

If existing technology can replace custom machinery with lower total cost and equal or better guarantees, consider it seriously. Also account for dependency, adapter, maintenance, context/tool overhead, lock-in, and operational risk. Reuse is a means, not a requirement.

## Investigation freedom

Choose your own investigation strategy.

The files in this repository provide context and starting points, not a mandatory sequence of reasoning. You may inspect whatever parts of the upstream repository, history, issues, PRs, external sources, and completed production cases are needed.

Optimize for **information gain per unit of work**, not maximum repository coverage.

Do not keep exploring a question once additional evidence is unlikely to change an architectural conclusion.

You do not need to ask the Human or supervisory assistant to approve each investigation step. They intend to remain mostly observers and factual advisors after giving you this proposition.

If you ask them questions, prefer questions that resolve missing facts or requirements. Do not expect them to choose your architecture for you.

## Safety boundary

### Upstream production repository

`eariver/japanese-generative-ai-survey`

Treat it as **READ ONLY** for this exercise.

Do not:

- commit or push to upstream;
- mutate upstream branches;
- open/update/merge upstream PRs as part of this task;
- mutate upstream Issues;
- create Human approval decisions;
- execute production release/freeze actions;
- perform destructive operations.

### This reconstruction repository

`eariver/reconstruct-japanese-generative-ai-survey`

This is your writable working area. You may create notes, analysis, diagrams, decision records, and final proposals here.

Small read-only analytical scripts/probes are acceptable when they are clearly more efficient than prolonged manual reasoning.

The initial phase is **not** primarily an implementation/prototyping task. Avoid spending substantial budget building a replacement Core, broad simulation environment, large synthetic fixture corpus, or production-grade implementation unless you believe it is necessary to settle a decisive architectural question. If so, explain the reason and keep the experiment bounded.

## Cost-awareness for your own work

This exercise is being run under a limited-use plan, so your own investigation should follow the same efficiency objective you are being asked to apply to the Survey.

Do not sacrifice architectural quality merely to minimize tool calls, but avoid redundant reading, unnecessary Computer Use, large implementation loops, or verification that cannot plausibly change the conclusion.

A strong compact investigation is preferable to a broad but low-information crawl.

## Current production references

Read the context in this workspace, then independently verify current upstream reality.

Useful starting points include:

- upstream `main` and recent PRs #483, #484, #485;
- current W34 work branch and its history;
- `AGENTS.md`;
- `config/survey-production-v2.json`;
- Core authority / final-audit / improvement-plan documents;
- current supervisory/operations governance;
- Human Gate implementation;
- Evidence / Screening / Selection / Architecture flow;
- operator bridge / CI workflows;
- completed W33 and SP001 production histories.

Do not assume these are exhaustive.

## Questions the final architecture should answer

At minimum, reach defensible conclusions about:

1. What does the current system actually do, end to end?
2. Why have wall-clock time and operational complexity grown?
3. Where does work amplification occur?
4. Where are sources or semantic judgments read/repeated by multiple roles or stages?
5. Which validations/checkpoints/authority layers prevent real historical failures, and which are redundant or over-specialized?
6. Why could a machine-valid large research run still collapse into a poor reader-facing Weekly architecture?
7. How should routine work, semantic judgment, anomaly detection, and Human authority be divided?
8. Should the current two-agent role split remain, change, or become conditional?
9. Which custom mechanisms can be KEEP / SIMPLIFY / MERGE / AUTOMATE / REMOVE / REPLACE-WITH-EXISTING-SOLUTION?
10. What should the common Weekly/Special production path look like when the system is mature?
11. How should exceptional or ambiguous cases escalate without making every normal edition expensive?
12. How much total work should the proposed design remove, and where?
13. How can the current system migrate toward the target without risking ongoing production?

## Expected final deliverable

Use whatever supporting files help you reason, but finish Phase A with a clear architecture report in this repository.

The report should include, in a form you consider effective:

- current-system model;
- root-cause / work-amplification diagnosis;
- quality-failure diagnosis, including the W34 compression case;
- architectural alternatives considered;
- recommended target architecture;
- model/vendor-independent role design;
- deterministic-vs-reasoning-vs-Human responsibility split;
- external solutions/patterns worth reusing, with trade-offs;
- current-vs-proposed workload comparison;
- migration strategy;
- major risks, uncertainties, and assumptions;
- what evidence would falsify or materially change your recommendation.

Do not stop at a prettier architecture diagram. The key question is whether the proposal can realistically produce better Weekly/Special editions with less total Human + agent + tooling work.

## Phase boundary

When the architectural report is complete, **stop**.

Do not begin production implementation automatically. The report will first be reviewed independently and discussed with the Human. A later task may request targeted follow-up or implementation design.
