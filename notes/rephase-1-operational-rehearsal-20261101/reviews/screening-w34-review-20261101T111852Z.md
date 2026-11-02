# Independent W34 Screening supervisory review — 2026-W34 ONLY (isolated)

**Role:** General independent supervisory reviewer — NOT Luna/Work author, NOT Sol, NOT Astra/root, NOT Human. No false attribution.

**File:** `notes/rephase-1-operational-rehearsal-20261101/reviews/screening-w34-review-20261101T111852Z.md`
**Wall-clock:** 2026-11-01T11:18–11:25Z.
**Bounds:** workdir READ-ONLY. No network, no Production checkout, no Commit readback, no Git mutation, no source edit, no runtime/import/test/build/fixture, no State write/advance, no deterministic record creation. Data-only `python3` stdlib hash/parse; unique evidence this file. No subagents. **W34 ONLY** — SP already reviewed separately (`screening-efficient-llm-review-20261101T111203Z.md`), not re-judged here.

**Actual State (read-only):** W34 `DISCOVERY_COLLECTED` (`discovery passed, screening pending`), history last `ISSUE_INITIALIZED→DISCOVERY_COLLECTED 2026-11-01T11:00:03Z impl 48082356`. Checkpoint `orchestration/v2/checkpoints/ISSUE_INITIALIZED.json` (3101B `3c64e40b…`) exists (prior dispatch); NO screening checkpoint exists; NO advance attempted by this review.

**Workdir base:** `.rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work`, HEAD `480823560c0c26ed2e5baa18e0e79a22b2839a27`.

---

## 1. Exact read scope + input SHAs (actual operator paths, no guessing)

Fresh product (reviewed):

| artifact (workdir path) | bytes | SHA256 | notes |
|---|---|---|---|
| `sources/2026-W34/screening/v2/accepted/e193ad0507895568e369437833b87d2610d68ef50f0c6419b092f5711e26bbea/screening-accepted.json` | 543880 | `b9d963d83b712ba3fb7e93358f051c4e902f31d0e262c44eea6f76dcdf155841` | 439 rec, KEEP73/MAYBE136/INSPECT200/DROP30, `result_set e193ad05…`, 12 batches |
| `…/package.json` (accepted copy) | 4094 | `b992151ce2af271d76860a1837da9acf2aa022716d75d934b4da1d00c0fe8df7` | basis profile `2a8c3089…`/state `69942680…`/event `0a23be47…`, prompt `3e45900e…`, contract `a05b65b4…`, 439/12 |
| `…/results/batch-001.json` … `batch-012.json` (12 files) | 7239–21460 | per-file `80b971a0…/4058e449…/48a43f5…` etc. (full list in workdir; batch-001 input `6ff2bf50…` identical to archived partitioning) | decisions verbatim archived, basis real per-batch |
| `…/input/batches/batch-001.jsonl` … `batch-012.jsonl` | 17617–50834 | `6ff2bf50…/d406a8f9…/f95d4eb0…` etc., 43/44/41/37×8/38/14 = 439 | deterministic partitioning, no stale rebind |
| `sources/2026-W34/screening/proposed-input/reuse-provenance.json` | — | owned, NOT in results/ (accept enforces exact set) | reuse verbatim, no status/wording change, historical runner NOT claimed, old SHAs not reused |
| `sources/2026-W34/screening/proposed-input/expansion-package/package.json` + `input/batches/*` + `expansion-results/*` | — | same 439/12 basis as accepted (package draft only) | strict facade, `implementation_sha 48082356` actual HEAD (fault-then-fix logged) |

Basis (pinned, not re-audited):

- Root R369: `sources/2026-W34/discovery/discovery-v2.jsonl` 963155B `e176326f…` (369), `discovery-accepted-v2.json` 377589B `255fb12d…` (369, graph `a13afd9e…`, X `73db915a…`).
- E439: `sources/2026-W34/screening/input/event-discovery-v2.jsonl` 1335444B `0a23be47…`, git-blob `06eb26bbaafd08782a5158102e9a67885809b434` == tree@774 both canonical paths (computed; log `21` self-verified; log `20:1` blob field `0a822193…` is inconsistent line, superseded by `21` + recomputation — no data drift, E bytes exact).
- Fresh Profile `sources/2026-W34/production-profile.json` 2371B `2a8c3089…` (WEEKLY/WEEKLY_MAGAZINE, `ROLLING_WINDOW 2026-08-14T18:00–08-21T18:00-04:00`, UTC `[2026-08-14T22:00Z, 2026-08-21T22:00Z)`, 3 obligs, paths preserved); State `DISCOVERY_COLLECTED` (`c680…` SP analogue; W34 state `69942680…` per package basis, `078c3411…` was pre-advance).
- Current DCP `3c64e40b…` (3101B) binds `255fb12d…` + `CORE_STAGE_CONTRACT` + `SOURCE_INTAKE_SUPERVISORY_REVIEW/AGENT_RESEARCH` (prior dispatch, separate evidence).
- Previous SourceIntake review FULL+CORR `reviews/source-intake-review-20261101T104700Z.md` 38557B `1d46058e…` (BOUNDED PROCEED both, residuals §5 retained — carryover pending, 22Z per-item, vendor-vs-independent, 180-bucket concentration, abstract-scope). Human window metadata per Root: ordinary window above, cutoff `2026-08-21T18:00-04:00`, `Editorial cutoff` on reader p1.
- Archived decisions `DATA.p2b05.screening-accepted.json` 543880B `d18c8ce3…` (439, same counts); decisions array byte-identical to fresh (`d2726ed3…` both, 0 reason mismatches). Historical `SELECTED41/7 packages` (`DATA.p2b12/p2b13`) is baseline ONLY — current selection NOT done.
- Governing docs read (no execution): Sol/Luna §§4.1/4.4/5, X doc §§2–3/10, `screening-v2-batch-result/run-package` schemas; CORR prior (deterministic reports separate if still bound, no fake GAP/legacy transition).

Method: all 439 `decision/reason/scope_tags/duplicate_group/verification_targets/confidence` parsed; cross-checked against event `provenance.origin/parent_refs/reason/obligs`, `source.locator/source_type/summary_text/raw_paths/metadata.published_at/window_relation_observation/chronology_precision`, and root/raw union where meaningful. Counts not used as proof.

---

## 2. Substantive findings (grounded, not count-only)

**Provenance complete, no rewrite/promotion:** All 439 event records `origin REFERENCE_EXPANSION` (439/439) with explicit `parent_refs` (bare root IDs — correct Screening-expansion namespace, NOT Discovery-root `local:/external:` namespace; earlier `19-*` `_parse_parent` refusal was wrong-validator-for-E, preserved not a data defect). Expansion accounting `accounted_roots 369/369 mode DERIVED_EXPANSION`, universe U 3 obligs [`carry-over/current-relevance/technical-significance`], `DECLARATION_LOSS []` (log `20`). Event `reason` retains Sol identity + pre-screening qualifier + selected parent + `No Screening decision is made`; `source` retains identity/Raw/obligs without disposition; `source_type` (`arxiv_atom_snapshot/github_release_api_response/official_*_snapshot/dailyx_x_observation/grok_x_observation_corrected_r2/sol_discovery_*`) preserved, `technical_claims_accepted false`, `discovery_only true` where applicable. Screening adds `decision/reason/scope_tags/duplicate_group/verification_targets/confidence` only — no label rewrite, no status promotion, no autofill. Raw union 53 paths, 0 missing; obligs `current+technical 437, +carry-over 2` (C076/C077); all 369 roots referenced.

**Prior 369-wrapper limitation solved by existing transport (no new flag/bypass):** Package prepared via existing `screening.prepare_package` on canonical E path (`screening/input/event-discovery-v2.jsonl`, tree@774 path, bytes self-verified) under strict `current_stage_basis_override` (real HEAD `48082356`, prompt/contract/state/profile/discovery pins, 12 batches; `21-*` exit 0 after harness-argv fault fixed by passing actual HEAD — fault quoted, no silent stub). Results from unchanged archived 439 decisions via `validate_decision` 0/439 + per-batch real `expected_result_basis` + `reuse-provenance.json` owned (not in results/); accept via existing API (`22-*` exit 0). Batch-001 input `6ff2bf50…` identical (deterministic partitioning); result/package/digest differ (fresh basis) → new run dir `e193ad05…`, no old-run rebind. No new shipping code, no 369-root re-authorship losing granularity, no test-fixture DCP. E raw parentrefs correctly expansion-namespace.

**Question/window/semantics consistent:** KEEP73 are in-window deltas with `proceed to Evidence verification without treating discovery claims as established evidence` (e.g., arxiv 15127 agentic workloads, C031 Dogwood policy-authoring follow-up (not pre-window original C069), C029 JumpStart availability (not base C070), C001 GLM-5.3 flagship, C039 Qwen local wave, C040 DeepSeek pricing delta, C023/C025 Grok distribution/build, C065 Ox Alpha→GLM-5.3). MAYBE136 are plausible deltas with significance not yet strong (e.g., C024 Gemini Enterprise, C041 Gemini 3.7 usage, C066 Bot expansion). INSPECT200 flag insufficient identity/chronology/authority (e.g., arxiv triage with `score/matched/title_matches` + `requires Sol review`). DROP30 are legitimate duplicate/out-of-scope (see below). No `SELECTED` claimed; historical 41/7 stays baseline.

**Anti-compression held:** 73+136+200 = 409 incoming to Evidence (only 30 out). Abstract-only is NOT a rejection reason — 180 arxiv atom records stay KEEP/MAYBE/INSPECT with per-DID VT (`lane/matched/title_matches/score/provisional + abstract excerpt`), never DROP for being abstract. Counterevidence stays incoming via dailyx/X deltas (safety, outage, pricing, comparison) as MAYBE/INSPECT with quarantine VTs, not dropped as noise unless truly routine.

**DROP30 legitimate (all match event qualifiers, boilerplate reason is shorthand for shared template — no material loss):**

- 5 coverage passthroughs (`comfy/llama.cpp/TRT-LLM/sglang/vllm` with `window_match_count 0`, `Coverage passthrough only…not a new Weekly event`) — correctly DROP accounting placeholders.
- Pre/post-window originals with in-window follow-up retained: C076/C077 (Music-3.0 08-13/H3 08-03 pre-window, carryover unresolved — DROP original, ledger preserved via parent_refs + obligs); C069/C070 (Dogwood/Nemotron originals pre-window, C031/C029 deltas KEEP/MAYBE); C072 (Wan 3.0 post-cutoff 08-24/26).
- Business/context noise per Weekly technical question: C059/C060/C061/C062/C063/C064/C067/C068/C084/C086/C089/C090 (revenue/IPO/hire/preparedness/outage/pricing-discussion/release-density/Build-misc/Vector-Search/active-inference-paper/OpenRouter-tutorial/HF-summer-report/Amodei-amplification/C049 FlashInfer-nightly/C074/C075 Gemini-Omni/Transcribe/C078/C079 ScienceFlow/CoRun/C094 Palmyra). Each event summary itself states `park-leaning/context-only/pre-window/post-cutoff/duplicate` — screening preserves that qualifier. C042 Grok-generic-adoption DROP is duplicate of specific distribution records C023 KEEP/C024 MAYBE/C025 KEEP in `grok-4.6-distribution/build` groups (3+2 grouped) — delta preserved specifically.

**MAYBE/INSPECT targets are actual, not superficial:** MAYBE VTs name the missing significance/condition (`harness/prefix-hit/pricing/official/KDA/footnote` etc.); INSPECT VTs name exact gap (`dedicated URL/derivations/Pro-variant+body/product-identity/weight-vs-substitute`) + `Evidence-stage full-body verification`. All 409 non-DROP carry ≥1 VT; 30 DROPs correctly VT-empty. `duplicate_group` used truthfully for 8 groups (grok-distribution/build, lfm2.5, nemotron, dogwood, qwen-community, copilot, agentcore) — KEEP/MAYBE/DROP differentiated within groups, not blanket-deduped.

**X vs primary, carryover, window distinctions preserved:**

- X: dailyx 7 raws are `DISCOVERY_AND_COMMUNITY_SIGNAL_ONLY` with `exact_returned_bytes`; Grok result `43b0923…` + ledger/accounting bound via parent_refs (C001 etc. list `w34-grok-r2-corrected-47-url-ledger`) and 2 Grok-derived events C089/C090 (correctly DROP as summer-report/amplification outside ordinary scope). X reasons never assert spec truth; VTs require primary verification (X doc §10 boundary). No `PRIMARY_ONLY` gate invented.
- Carryover: `w34-carryover-minimax-unresolved` (`RECHECKED_UNRESOLVED, promotion false`) held via C076/C077 parent_refs + 2 carry-over obligs; DROP of pre-window originals does NOT delete ledger root. Explicit disposal remains Selection/Completeness (SourceIntake residual, not closed here).
- 22Z boundary: 08-22 dailyx `observed 2026-08-21T22:00Z` is exactly cutoff (JST slice `08-20T22Z–08-21T22Z`), not post-cutoff leakage; arxiv events carry `published_at` (e.g., 15127 `2026-08-15T09:02:16Z`), `window_utc`, `window_relation_observation IN_WINDOW_DATE_CANDIDATE`, `chronology_precision EXACT_PUBLISHED_IN_ATOM_SNAPSHOT`. Screening does not claim window verified — defers to Evidence per SourceIntake residual. Late/date-only/capture-time (Aug 26 re-date, Sep 8 capture, date-only unresolved) remain Evidence checks, correctly not decided at Screening.
- 180-bucket risk documented: 180 share `cs-ai.atom` (45 `cs-cv`, 40 `cs-cl`, …) as `arxiv_atom_snapshot`, each with per-DID `arxiv_id/lane/matched/score/abstract-excerpt/provisional + Sol review required`. Independence verified per DID (15127 KEEP vs 14967 MAYBE vs 14927 INSPECT with different lanes/scores) — not 1 paper counted 180×. Concentration called out, count ≠ sufficiency.

**Publisher truth not yet:** All Raws `SUMMARY/LOCATOR_CAPTURED` or API/index snapshots; screening explicitly `without treating discovery claims as established evidence`. `AUTHORITY_CONSUMED` judgment belongs to Evidence independent review (governance §4.2–4.3), still pending.

---

## 3. Mandatory vs permissible

**No mandatory proposed-input correction before `CANDIDATES_NORMALIZED`.** All 439 decisions are exact archived reuse (`d2726ed3…` identical, 0 reason mismatches, counts preserved) with valid shape (`validate_decision` 0/439, schema-valid batches). Limitations above are explicitly worded in `reason + verification_targets` and match event `qualifier/summary/metadata`. Rewriting archived reasons/scopes/VTs or re-authoring 369 root decisions would lose event granularity and exceed the Screening gate (which requires exact coverage + valid shape, not publisher proof). Generic W34 KEEP/MAYBE boilerplate (`materially relevant…/plausible delta…`) is permissible at Screening because per-DID specificity lives in `scope_tags + verification_targets + duplicate_group` + event metadata (lane/score/excerpt/window/parent_refs) — Evidence must consume those, not Screening prose.

If Evidence finds a window/identity gap (e.g., date-only vs 22Z, arXiv published_at outside window, locator unresolvable), the fix is an Evidence-stage `AUTHORITY_*` + gap-fill/supplement record with exact DID + evidence — NOT a silent accepted-rewrite. New content, if ever needed, is addressed in a new run with prior preserved.

---

## 4. Verdict + permission (existing typed path only)

**Verdict: `W34 BOUNDED PROCEED` to `CANDIDATES_NORMALIZED` via root-selected typed agent checkpoint/advance (reports revalidated at dispatch).**

Permit current correct bytes ONLY: `screening-accepted.json b9d963d8…` (439, 73/136/200/30, `e193ad05…`), `package.json b992151c…`, 12 inputs/results SHAs §1, event `0a23be47…`/`06eb26bb…`, root `e176326f…`/acceptance `255fb12d…`, profile `2a8c3089…`, state/DCP `3c64e40b…` lineage. No checkpoint write by this review; root dispatches after this decision; existing build/advance revalidates fresh State/contract/impl/artifact/report bindings (no rerun for chronology). Deterministic `CORE_STAGE_CONTRACT` reports before independent review remain separate evidence if still bound (CORR prior); no fake GAP schema/legacy transition demanded or created.

**Residual Evidence targets carried (not closed):** per-DID body consumption with `AUTHORITY_*` (180 atom abstracts → full bodies where load-bearing); 22Z per-item + late/date-only/capture-time verification; vendor-vs-independent gap-fill (pricing/comparison/outage/business context quarantined); carryover explicit disposal at Selection (Music-3.0/H3 ledger + C076/C077 DROP preserved); X/social as leads only; duplicate-group disambiguation where needed; no cross-condition ranking; historical 41/7 stays baseline until fresh Selection.

**Not allowed:** State advance by reviewer; Selection/Architecture/Draft/Candidate/Preview/Freeze/Release; Human Gate decisions; old approval rebinding; source edits; SP advance on this review.

---

## 5. Machine artifact — none (truthful)

No new schema/checkID invented. A truthful `AGENT_RESEARCH` row citing this actual review (executor `General independent supervisory reviewer`) is legitimate ONLY if the existing checkpoint flow requires an agent row; otherwise exact review path/hash in existing `evidence`/`summary` suffices with content review separate.

**Attribution:** General independent supervisory reviewer. No Sol/Astra/Human claim. No publication PASS/adoption/savings claim.

(End of independent W34 Screening review — 2026-11-01.)
