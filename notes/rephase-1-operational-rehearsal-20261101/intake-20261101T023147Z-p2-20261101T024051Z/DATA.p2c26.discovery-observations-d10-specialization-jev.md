# Discovery observations — D10 Specialization instead of generation (Jev mandatory case)
# Edition: SP-efficient-llm-2026 | collector_run: efficient-llm-discovery-r1 | observed: 2026-09-21
# Critical rule: TypeSafe's own benchmark is a VENDOR CLAIM until independently reproduced.
# Standing question: for classification/routing/ranking/structured probabilistic decisions,
# why generate natural-language tokens at all?

## S70 — Introducing System One Models & Jev (TypeSafe AI launch post)
- locator: https://typesafe.ai/blog/introducing-system-one-models-and-jev
- class: PRIMARY_ANNOUNCEMENT | published: 2026-09-15 | retrieval: SUMMARY_CAPTURED
- summary: New architecture + parallel sampler + RLCD (Reinforcement Learning for Calibrated Decisions);
  typed outputs (Choice/Score/Noul) with calibrated probabilities; end-to-end 70–500ms; input $0.042/MTok,
  output free; headline workflow race 0.114s vs 8.566s (193.6x faster, 444.6x cheaper) on System-One-shaped
  tasks; founder RLHF/InstructGPT lineage (Diogo Almeida); $40M/DCVC backing (per third-party page).
- vendor-claim quarantine: The 193.6x/444.6x race, "zero hallucinations", "no type errors", and benchmark
  deltas are VENDOR claims. Evidence must bind exact task/workflow, baseline models, harness, and date;
  no general faster/better-than-frontier-LLMs statement without task/evaluation qualification.

## S71 — TypeSafe documentation: System One concepts + Introduction (Choice/Score/Noul, parallel, calibration)
- locator: https://docs.typesafe.ai/concepts/system-one
- class: PRIMARY_DOC | published: 2026-09 (living docs; captured 2026-09-21) | retrieval: SUMMARY_CAPTURED
- cross: https://docs.typesafe.ai/introduction
- summary: State (string/JSON/text array; no image/audio/video yet) + typed question map in one POST;
  questions evaluated in parallel, isolation (no context-rot), ~100ms typical; calibration = group-level
  property, NOT per-answer correctness guarantee; atomic-question decomposition doctrine; RLCD primer.
- limitations (vendor-documented): text-only input; atomic narrow questions required (broad judgments must
  be decomposed in user code); calibration statistics do not certify individuals. Availability: early access,
  waitlist (S74).

## S72 — Jev wiki: Jev 1.13 model card facts (community-compiled from TypeSafe card)
- locator: https://jevai.wiki/
- class: SECONDARY_REFERENCE | published: 2026-09-19 | retrieval: SUMMARY_CAPTURED
- summary: Live build jev-1.13.0; 64k context; $0.042/M input, output free; 70–500ms (typical ~100ms);
  1200 req/min cap; English strongest; limits mutable without notice. Useful as a dated fact snapshot;
  NOT specification authority (pin to TypeSafe card/docs at Evidence).

## S73 — awesome-jev (community reproduction/independent-evaluation hub)
- locator: https://github.com/OmniJev/awesome-jev
- class: SECONDARY_REFERENCE (community repo) | published: 2026-09-17 | retrieval: SUMMARY_CAPTURED (contents pending Evidence)
- summary: Aggregates: HN launch thread (1850 pts/485 comments; CEO confirms zero-shot-classifier reading,
  encoder-with-heads shape); OpenJev (3090-scale baseline); Jevlike (from-scratch text+N-options shape,
  option-attention head); Qwen-2.5-1B-RLCD fine-tune + parallel constrained decoding (5.6–7x on Apple
  Silicon); DSPy adapter; TypeSafe System One Adapter (OpenAI/Anthropic-backed typed interface = the
  comparison baseline). Strongest current independent-reproduction lead set — but community-grade;
  NO peer-reviewed reproduction located in this pass.
- gap: Sol-directed gap-fill: verify each reproduction's actual measurements vs link-rot; seek peer-reviewed
  or vendor-independent benchmark of typed-decision vs generate-then-parse.

## S74 — Jev explainer with access/pricing facts (DataCamp, secondary)
- locator: https://www.datacamp.com/blog/system-one-models-jev
- class: SECONDARY_REFERENCE | published: 2026-09-19 | retrieval: SUMMARY_CAPTURED
- summary: Corroborates early-access waitlist, endpoint shape, $0.042/M input + free output, RLCD/parallel-sampler
  description, per-decision-case cost anecdote (~$0.0004). Secondary: use only as contextual signal;
  technical/economic facts rebind to TypeSafe primary at Evidence.
- precedent watch: earlier/parallel "no-generation decision" ideas (zero-shot classifiers, constrained
  decoding, semantic-router patterns) are candidate precedents WITHOUT forced ancestry — Sol to judge.
