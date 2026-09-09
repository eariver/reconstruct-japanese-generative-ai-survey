# AGENTS.md

This repository is the writable workspace for an external architecture/design review of `eariver/japanese-generative-ai-survey`.

## Current primary task

The original Phase A architecture review and its refinement are complete. Do **not** restart `instructions/ASTRA_INITIAL_TASK.md` or replay Phase A as the default task.

For a new Astra session, read first:

1. `instructions/ASTRA_NEXT_PHASE_BOOTSTRAP.md`
2. `handoff/astra-phase-a-session-closeout.md`
3. `outputs/astra-phase-a-architecture-refinement.md` — begin with §1 and §10; load other sections only as needed

Use `context/2026-09-09_post-refinement-human-sol-discussion.md`, `notes/phase-a-evidence.md`, the original Phase A report, and upstream production artifacts selectively when they materially affect the current decision.

The first task is to let Astra determine the next phase under the bootstrap instruction, not to impose a predefined implementation path. After writing `outputs/astra-next-phase-decision.md`, stop until the Human explicitly authorizes the selected phase, preferably in the same Astra session.

Historical task files remain useful provenance and context but are not the active task unless explicitly reactivated.

## Repository boundary

- `eariver/japanese-generative-ai-survey`: **READ ONLY** for this exercise unless the Human later gives an explicit production-mutation instruction.
- `eariver/reconstruct-japanese-generative-ai-survey`: writable working area for notes, analysis, probes, diagrams, decisions, and proposals.

Do not mutate the upstream production repository, its branches, PRs, Issues, Human decisions, Freeze/Release state, or other production authority during the next-phase decision step.

## Investigation style

Choose your own cost-aware investigation strategy.

The durable context files are starting points, not a requirement to reload all prior work. Inspect upstream history, code, schemas, workflows, production artifacts, completed editions, issues, PRs, or public external sources only when they have meaningful information value for the current decision.

Prefer targeted reads over exhaustive crawling. Stop investigating a question when additional evidence is unlikely to change the decision.

Avoid wheel reinvention: public OSS, standards, workflow/provenance/publication/agent-orchestration patterns may be reused when they improve total-system cost and quality.

Small read-only analytical probes are allowed. The bootstrap task is a decision/design task, not authorization for production implementation, migration, or a large shadow execution.

## Role abstraction

Treat model names as current bindings only:

- Architecture / Policy Decision Role — currently Astra
- Supervisory / Independent Review Role — currently Sol
- Production Operations Role — currently Luna / Work
- Human Decision Authority — owner

Astra may revise the role decomposition if justified. Human authority over adoption, priority, migration, and Human Gates is not delegated.

## Current output boundary

For the bootstrap step, place the primary decision artifact at:

`outputs/astra-next-phase-decision.md`

Keep supporting artifacts to the minimum actually needed. Then stop before executing the selected phase until the Human gives the same-session follow-up authorization.
