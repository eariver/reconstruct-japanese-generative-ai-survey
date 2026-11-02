# Sol Evidence Review — SP-efficient-llm-2026 — PASS / PROCEED_TO_SELECTION_WITH_SCOPE_BOUNDARIES

Date: `2026-09-22`
Reviewer: `Sol / GPT-5.6`
Review kind: Sol-supplied semantic review (authority-consumption + materiality).
Materialized into the repository by Muse (Luna/Work execution role) without
claiming authorship. Semantic verdict and findings below are Sol's.

Status: `PASS / PROCEED_TO_SELECTION_WITH_SCOPE_BOUNDARIES`
Lifecycle at review: `EVIDENCE_REVIEWED` (machine lifecycle; Selection NOT entered)

## 1. Active authority reviewed

- Evidence acceptance:
  `sources/SP-efficient-llm-2026/evidence/v2/accepted/dba89409c1cdcfb6a8b319ef35e0e1ee1b5ffdc74cad4715dbe44e10345e5603/evidence-accepted.json`
  (SHA `72ba3407b63161c58d7f4c6a9c0c1db65f9fc26c498b781322e3f88b376a3047`,
  result_count 160)
- Edition Views acceptance:
  `sources/SP-efficient-llm-2026/evidence/v2/views/accepted/2bf475f518d80c8088dff7a67a0bc5cae5e2fa5c9a309d56695e66b1d54d7762/edition-views-accepted.json`
  (SHA `364d484a6466220d0fd3d98ed450fa8283098f3cbf61c10c83e8d193527227fb`,
  160 views)
- Materiality Ledger: `sources/SP-efficient-llm-2026/materiality-ledger-v2.json`
  (SHA `ad7509369252ee39b73aaf92798972bb61ac5dda6add3daaecf03ee6e087d913`;
  165 rows: MATERIAL 137 / CONTEXT 23 / EXCLUDED 5)
- Profile Completeness: `sources/SP-efficient-llm-2026/profile-completeness-v2.json`
  (SHA `aeeadd1981f3827ff4cc951b39f804f37346b096499a4600d6180df0f535e918`;
  overall `LIMITED`; 15 obligations: 3 SATISFIED / 12 LIMITATION)
- Authority-consumption ledger (Luna-side, reviewed not authored):
  `sources/SP-efficient-llm-2026/execution/reviews/evidence-authority-consumption-package-r2.md`
- Stage checkpoint: `sources/SP-efficient-llm-2026/orchestration/v2/checkpoints/CANDIDATES_NORMALIZED.json`
  (SHA `b69d2a0b4936c5122bd9a6f63b4186f46c5baee4f8f3156b8a01b2ac5a287038`)

A later regenerated Evidence run invalidates any semantic conclusion that
depended on the previous active pair. Selection/Architecture built from any
other Evidence/View bytes is not covered by this review.

## 2. Evidence execution (Sol finding)

- 160 accepted Evidence Cards: 12 VERIFIED / 148 PARTIAL / 0 NEEDS_MORE / 0 REJECTED.
- VERIFIED (12): EFF-D032, EFF-D036, EFF-D070, EFF-D071, EFF-D141, EFF-D148,
  EFF-D149, EFF-D150, EFF-D151, EFF-D154, EFF-D163, EFF-D165.
- Materiality: 137 MATERIAL / 23 CONTEXT / 5 EXCLUDED (the five accepted
  Screening DROPs D140 D158 D159 D160 D161).
- Completeness: `LIMITED` (expected for a Thematic Special at this stage; the
  12 LIMITATION obligations are source-backed limitations, not unprocessed gaps).
- Compatibility: 160 tasks, 67 projected / 93 passthrough,
  `COMPATIBILITY_REPRODUCIBILITY: PASS`, frozen Core validators PASS, shared
  Core unchanged. CV2-DM-016 remains `OPEN_CORE / EDITION_WORKAROUND`.

## 3. Evidence quality finding (Sol finding)

The high PARTIAL count is not itself blocking. The accepted corpus
distinguishes first-party fact, author/vendor claim, independent evidence,
X/community observation, inference, and unresolved limitation. Vendor and
community numbers are not promoted to general technical facts.

Major load-bearing bodies were materially consumed for DeepSeek V4.1, Qwen
3.8-Flash-Next, Kimi Linear, DeepSeek/V3.2 DSA, Jev launch/concepts/models,
EAGLE/MTP, TTC and reasoning-budget sources, routing sources, benchmark
methodology sources, and runtime follow-ups F1–F3. No further broad Evidence
gap-fill is required before Selection.

## 4. Mandatory D128 scope correction (Sol finding; binding on downstream work)

`EFF-D128` (GLM-5 technical report): the accepted Evidence Card correctly
states report-abstract scope — full-body DSA adoption details, RL
infrastructure, and benchmark tables were NOT consumed.

Downstream work MUST NOT repeat or imply that all four 2026 capstones were
consumed at section-level full-body depth for GLM. Correct interpretation:

- DeepSeek V4.1: section/body-level;
- Qwen3.8-Flash-Next: section/body-level;
- Kimi Linear: section/body-level;
- GLM-5 / GLM-5.3 lineage: mixed authority depth (D128 abstract-scope plus
  other first-party model/docs/runtime authorities).

The checkpoint-bound Completeness artifact is NOT mutated for this prose
correction. The correction is recorded here and MUST propagate into Selection
rationales, Architecture package boundaries, and the Human Architecture
dossier. D128 remains usable as bounded primary authority and MUST be
rationalized as `PRIMARY but abstract-scope for the material claims presently
consumed`, never as full-body verified.

## 5. Non-blocking limitations preserved (Sol finding)

The following are NOT closed and constrain claims; they do NOT require another
Evidence cycle before Selection:

- Jev independent reproduction remains thin; public calibration protocol
  unresolved; vendor claims stay bounded.
- AIPerf standalone product authority remains unresolved.
- Some capstone ablation and per-figure pins remain outstanding.
- GLM vendor ratios remain vendor-measured (quarantined, not generalized).
- Kimi independent reproduction remains limited.
- Routing fragility paper D157 remains summary-scope.
- SWE-bench-Pro full text is captured but section-level methodology consumption
  remains incomplete.
- Some repo/doc/spec bodies remain captured-but-unconsumed.
- 40 verification targets remain UNRESOLVED (enumerated in the r2
  authority-consumption package §17).

## 6. Selection authorization and boundaries (Sol directive)

Selection is AUTHORIZED under the following binding boundaries:

1. Comprehensive long-form posture: neither collapse 160 non-DROP candidates
   into an implausibly tiny set nor SELECT mechanically. Every candidate gets
   an explicit disposition with a non-generic rationale.
2. D162 (X ledger): SUPPORTING reception/deployment evidence only, never
   PRIMARY technical authority.
3. D164 (Unsloth GLM local quantization): GGUF availability, local-memory
   feasibility, and packaging/runtime paths only; vendor-measured
   speed/quality figures remain quarantined.
4. D128: as §4 above.
5. Jev: mandatory selected case with vendor claims bounded by missing
   independent reproduction/calibration evidence.
6. Benchmark numbers: no selection on headline numbers alone; methodology and
   conditions travel with every selected benchmark authority.
7. The five Screening DROPs (D140 D158 D159 D160 D161) normally remain REJECT;
   any resurrection is a recorded selected exception with architecture need.
8. Former MAYBE (20), former INSPECT (5), watches (MiniMax D086, gpt-oss D087),
   secondary surveys (D152 D156), and high-signal unselected MATERIAL sources
   each receive explicit negative-space rationale naming the superseding
   selected source or the unnecessary editorial role.

## 7. Recommendation

`PROCEED_TO_SELECTION_WITH_SCOPE_BOUNDARIES`. No further Evidence gap-fill
before Selection. Architecture preparation may proceed from Sol-reviewed
Selection semantics; the Sol Architecture review and the Human-facing dossier
remain due before any Human Gate presentation.
