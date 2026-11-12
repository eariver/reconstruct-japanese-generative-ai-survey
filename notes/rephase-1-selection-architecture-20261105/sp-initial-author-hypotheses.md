# SP initial author hypotheses — limits and unverified counts (superseded by source-joined map)

**Role:** SP AUTHOR. Date 2026-11-05 chat-only first draft. This file records what was hypothesis, not policy. Corrected by `sp-candidate-map.json` (source-joined, computed).

## First-draft unverified claims

- Claimed `SELECT-CORE 30 / SUPP 101 / APPENDIX-CURRENT 6 / HOLD 23 / EXCLUDED 5 =165`. Manual CORE 30 was not enumerated as 30 distinct DIDs with titles; count vs list not reconciled. Corrected map computes PRIMARY 13 / SUPPORTING 119 / HOLD 28 / non-Matrix EXCLUDED 5; Matrix 160 =13+119+28. Manual 30 is withdrawn.
- Grouped remaining 148 DIDs by obligation lane and ledger disposition with inferred topics; several titles inferred from DID ranges/old headlines, not joined Discovery `discovery-v2.jsonl` titles/locators. Corrected map joins `discovery-v2.jsonl` title/locator/published_at + screening decision/reason + interactive-evidence entity/claims/verification/limitations + evidence status + views materiality + ledger disposition + completeness obligations per DID. No `同上`.
- Existing 160 cards read only via first-file head / prior review excerpts, not full `interactive-evidence.json` records metadata (claims/verification/limitations/materiality/scope_dimensions/bindings). Corrected map reads all 160 records metadata.
- `D119 GenAI-Perf` treated as unusable because AIPerf missing. Wrong: GenAI-Perf docs VERIFIED (metrics/load/logging) is distinct claim from AIPerf successor UNRESOLVED. Corrected: D119 SELECTED SUPPORTING for docs, AIPerf open as limitation.
- `D162 SOCIAL` treated as factual appendix proof. Wrong: X reception ledger VERIFIED for acceptance counts only; limitations prohibit technical/economic/license facts. Corrected: D162 HOLD lead-only, NONE, not placed.
- Jev mandatory/as-of handled as silent current-appendix waiver with Q1 as Human question. Insufficient per Astra §2: Profile Jev mandatory remains, appendix alone does not close O10. Corrected: O10 stays LIMITATION, mapped to pkg08 (D142 SUPPORTING contract) + Appendix A current-context HOLDs with vendor quarantine + calibration/reproduction gaps; no temporal scope change claimed.
- DSpark OR handled as default Human block (Q2). Insufficient: existing bound V41 body §2.4.3 + HF README dba1be0 DSpark line already satisfy OR at body scope for architecture claim; vLLM recipe gap is deployment-config, not architecture block. Corrected: DSpark OR met, vLLM historical as deployment gap only.
- All unconsumed appendices declared optional because thin chapter writable. Insufficient per Astra §2: must decide REQUIRED depth per measured-effect claim from captured bodies. Corrected: per-body REQUIRED sections listed in map/gap (EAGLE §5.1+Fig1, Snell Intro+§7, s1 §§2-3, ThinkPrune Table1+§3.3, overthinking Table3+§3.3/§5, FrugalGPT Table3+§4, Kimi Abstract+arch+§§, Qwen Abstract+§2-3+Tab11, V41 §2+§5+Appx map, V32 §2.1); per-figure/appx pins REQUIRED only if chapter cites figure numbers, otherwise quarantine.
- 9 packages presented with arbitrary page budget and history-adjacent naming without explicit must_cover_requirements/boundaries/drafting_order. Corrected: 9 packages + Appendix A with explicit thesis/purpose/primary/supporting/must_cover/boundaries/order and page plan target 70/max 92 (prior 66pp actual + appendix, not copy).
- Q1-Q3 posed as Human questions. Per instruction they are not Human questions: research mechanics resolved locally; only real authority choice returned (none needed for DSpark; Jev 09-21 revision only if Human wants as-of VERIFIED, otherwise HOLD with LIMITATION is the honest ceiling).

## Counts to reconcile

- First draft: 30+101+6+23+5=165 (unverified).
- Corrected: PRIMARY 13 + SUPPORTING 119 + HOLD 28 + EXCLUDED 5 =165; Matrix 160 =13+119+28; non-Matrix 5 separate. Machine-computed in `sp-candidate-map.json` counts.
