# AGENTS.md

This repository is the writable workspace for an external architecture/design review of `eariver/japanese-generative-ai-survey`.

## Current primary task

Phase 3 is closed after the Phase 3-G system-direction reassessment. Do **not** restart Phase A, the former next-phase decision step, or the acceptance/staging experiments as the default task.

For a new Astra session, read first:

1. `instructions/ASTRA_POST_PHASE_3_BOOTSTRAP.md`
2. `handoff/astra-phase-3-session-closeout.md`
3. `outputs/astra-system-direction-reassessment.md` — §1, §5, §7; other sections only as needed

Past Human-Sol conversation logs and previous session history are not required inputs. Use the handoff's evidence index and selective production reality checks when they materially affect the decision.

The objective is to minimize total lifecycle work across production, supervisory reasoning/review, repair/regeneration, CI/runtime, LLM usage, operational complexity, and Human handoff, while preserving at least intended publication quality, provenance correctness, fail-close safety, Human authority, Weekly/Special generality, and historical reproducibility. Moving work between roles is not a saving; justified long-term investment is allowed.

The current priority is research-question-to-publication/review/repair comparison with all-role cost accounting. Additional acceptance/staging/cache implementation is paused, including the previously proposed internal-staging alternative. Canonical direct authoring plus mechanical assistance is a comparator, not a proven final architecture. On a new continuation instruction, choose the next bounded work from the current evidence; do not replay the former decision-only/same-session approval step. During a closeout-only request, update durable handoff and stop.

Historical task files remain useful provenance and context but are not the active task unless explicitly reactivated.

## Repository boundary

- `eariver/japanese-generative-ai-survey`: **READ ONLY** for this exercise unless the Human later gives an explicit production-mutation instruction.
- `eariver/reconstruct-japanese-generative-ai-survey`: writable working area for notes, analysis, probes, diagrams, decisions, and proposals.

Do not mutate the upstream production repository, its branches, PRs, Issues, production State, Human decisions, Gates, Freeze/Release state, adoption/migration, or other production authority without explicit Human authorization. Ordinary Git Pull/Push and final commit are handled by the Human.

## Investigation style

Choose your own cost-aware investigation strategy.

The durable context files are starting points, not a requirement to reload all prior work. Inspect upstream history, code, schemas, workflows, production artifacts, completed editions, issues, PRs, or public external sources only when they have meaningful information value for the current decision.

Prefer targeted reads over exhaustive crawling. Stop investigating a question when additional evidence is unlikely to change the decision.

Avoid wheel reinvention: public OSS, standards, workflow/provenance/publication/agent-orchestration patterns may be reused when they improve total-system cost and quality.

Reconstruct investigation and candidate work follow the current Human request. The bootstrap is not authorization for production implementation, migration, or a large shadow execution. Read current remote reality only when current implementation/edition details matter; fixed lab snapshots are historical evidence.

## Role abstraction

Treat model names as current bindings only:

- Architecture / Policy Decision Role — currently Astra
- Supervisory / Independent Review Role — currently Sol
- Production Operations Role — currently Luna / Work
- Human Decision Authority — owner

Astra may revise the role decomposition if justified. Human authority over adoption, priority, migration, and Human Gates is not delegated.

## Current output boundary

Current decision: `outputs/astra-system-direction-reassessment.md`.

Current handoff: `handoff/astra-phase-3-session-closeout.md`.

Do not overwrite historical decisions or recreate the old bootstrap output by default. Keep new durable artifacts minimal, preserve evidence scope and unresolved conditions, and stop at a supported decision surface or the Human's specified boundary.
