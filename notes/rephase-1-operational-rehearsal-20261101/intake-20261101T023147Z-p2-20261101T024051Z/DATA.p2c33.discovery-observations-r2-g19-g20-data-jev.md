# Discovery observations r2 — G19 Data/token efficiency sweep + G20 Jev authority check
# Edition: SP-efficient-llm-2026 | collector_run: efficient-llm-discovery-r2 | observed: 2026-09-21
# G19 outcome: PURSUE-as-context or PARK_WITH_REASON is Sol's call; this sweep only ensures no silent omission.
# G20 rule retained: vendor quarantine; secondary repetition never closes primary gaps.

## S138 — Deduplicating Training Data Makes Language Models Better (Lee et al.)
- locator: https://arxiv.org/abs/2107.06499
- class: PRIMARY_PAPER | published: 2021-07 | retrieval: SUMMARY_CAPTURED (full body pending Evidence)
- summary: Near-dup/duplicate removal improves quality AND reduces steps-to-target (token-efficiency via
  selection, not architecture). Candidate axis: training-token reduction without architecture change.

## S139 — DoReMi (Xie et al.; data-mixture optimization)
- locator: https://arxiv.org/abs/2308.01833
- class: PRIMARY_PAPER | published: 2023-08 | retrieval: SUMMARY_CAPTURED
- summary: Distributionally robust mixture weights from a small proxy run; 6.5x step-efficiency claim class.
  Data-mixture as compute lever; interacts with Chinchilla allocation (S02) — allocation is not only
  quantity but composition.

## S140 — Textbooks Are All You Need (Gunasekar et al.; phi data-quality line)
- locator: https://arxiv.org/abs/2306.11644
- class: PRIMARY_PAPER | published: 2023-06 | retrieval: SUMMARY_CAPTURED
- summary: Synthetic textbook-quality data enabling small-model reasoning; quality-over-quantity pole.
  Relevance to this issue is INDIRECT (capability-per-token, not serving cost) — park-leaning; Sol decides.
  Tokenizer/vocabulary efficiency: no materially distinct primary located this pass (subword vs byte-level
  is well-trodden; no 2026 capstone cites it as an efficiency lever) — PARK_WITH_REASON recommended.

## S141 — Jev 1.13 official Models page (versioned IDs, aliases, RLCD, serving facts)
- locator: https://docs.typesafe.ai/models
- class: PRIMARY_DOC (official model card equivalent) | published: null (living docs; captured 2026-09-21)
- retrieval: SUMMARY_CAPTURED
- summary: jev-1.13.0 current; jev-latest/jev-preview aliases (alias drift warning: answers can change
  without side change; log versioned ID); 64k ctx (32k state + longest question); 250k tok/s, 1200 req/min;
  input-only billing; NO per-account fine-tuning/LoRA (same RLCD weights for all; domain via state]). Upgrades
  S72 secondary facts to first-party; RLCD remains a NAME (no algorithm paper/pseudo-code located).
- r1 parents: external:SP-efficient-llm-2026:EFF-D072, external:SP-efficient-llm-2026:EFF-D070.

## S142 — TypeSafe API reference (request/answer contract, confidence derivation)
- locator: https://docs.typesafe.ai/api
- class: PRIMARY_DOC (official interface spec) | published: null (living docs) | retrieval: SUMMARY_CAPTURED
- summary: POST /v1/systemone; per-question Choice/Score/Noul answers with probabilities; confidence
  DERIVED from distribution (Choice/Score); usage.input/output tokens metered though output free.
  Closest available to an evaluation-protocol primary: answer schema + confidence semantics specified,
  but NO benchmark methodology, NO calibration measurement protocol, NO independent audit.
- independent-evidence verdict: INDEPENDENT_EVIDENCE_NOT_FOUND_AS_OF_2026-09-21 for peer-reviewed or
  vendor-independent benchmark/reproduction. Community-grade leads only: awesome-jev (S73), live playground
  (jevtypesafeai.com), Pydantic/Vercel integrations, community playbooks — deployment-interest signal,
  NOT technical validation. RLCD technical description: NOT FOUND beyond vendor name + primer prose.
- r1 parent: external:SP-efficient-llm-2026:EFF-D071.
