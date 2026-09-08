# AGENTS.md

This repository is the writable workspace for an external architecture review of `eariver/japanese-generative-ai-survey`.

## Primary task

Read:

1. `README.md`
2. `brief/00-mission-and-success-criteria.md`
3. `brief/01-human-and-supervisor-discussion-context.md`
4. `brief/02-current-system-reference.md`
5. `instructions/ASTRA_INITIAL_TASK.md`
6. `research/00-astra-usage-and-cost-context.md`

Then perform the Phase A architecture review described in `instructions/ASTRA_INITIAL_TASK.md`.

## Repository boundary

- `eariver/japanese-generative-ai-survey`: **READ ONLY** for this exercise.
- `eariver/reconstruct-japanese-generative-ai-survey`: writable working area for notes, analysis, probes, diagrams, and final proposals.

Do not mutate the upstream production repository, its branches, PRs, Issues, Human decisions, Freeze/Release state, or other production authority.

## Investigation style

You are expected to choose your own cost-aware investigation strategy.

The context files are starting points, not a rigid read order after initial orientation. You may inspect upstream history, code, schemas, workflows, production artifacts, completed editions, issues, PRs, and public external sources as needed.

Prefer high information gain over exhaustive crawling. Stop investigating a question when additional evidence is unlikely to change the architecture decision.

Avoid wheel reinvention: public OSS, standards, workflow/provenance/publication/agent-orchestration patterns may be reused if they improve total-system cost and quality.

Small read-only analytical probes are allowed. The initial task is not primarily a replacement implementation or large simulation exercise.

## Role abstraction

Treat model names as current bindings only:

- Supervisory Reasoning Role — currently Sol
- Production Operations Role — currently Luna / Work
- Human Decision Authority — owner

The architecture must be model/vendor agnostic. You may recommend a different role decomposition if justified.

## Final output

Place the main Phase A report at:

`outputs/astra-phase-a-architecture-review.md`

Supporting files may be added under `outputs/`, `notes/`, or another sensible directory.

When the Phase A architecture report is complete, stop. Do not begin production implementation without a later explicit task.
