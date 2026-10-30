# Profile/Support contract intake — 4 pinned docs at c8d0ecc1 (20261030T124140Z)

Scope: Human-authorized ONLY 4 read-only GETs via `gh` at fixed production commit
`c8d0ecc1c9566a2303ad3b4c42635d4b672650e4`, repo `eariver/japanese-generative-ai-survey`.
No current/main/branch tracking, rebaseline, code adoption, Human commit readback,
runtime/tests/build/fixtures/Git mutation. Acquired `.py` NOT executed/imported.
Runtime final133 read-only untouched; baseline 774 untouched. See `manifest.json`
for API counts/sourceSHA/status/digest. Exactly 4 GETs; no extra fetch.

## 1. Availability (4/4 AVAILABLE_VERIFIED, no fallback)

1. `sources/SP-efficient-llm-2026/execution/defects/shared-core-evidence-source-map-gap-20260922.md`
   — AVAILABLE, HTTP 200 exit 0, size 6540, blob `d9f5847956c2e0c94a04749bf6aa76b4e34d7555`,
   sha256 `7a3c89dd248f43f665f5705620b50ff39de027ed303934d1b97f1c9e5c584729`.
   DATA: `DATA.shared-core-evidence-source-map-gap-20260922.md`.
2. `sources/SP-efficient-llm-2026/execution/sessions/ts001-reissue-evidence-20260922.md`
   — AVAILABLE, HTTP 200 exit 0, size 4815, blob `281df8a75a5b1775d6f7b6eb37f4c46c1614567e`,
   sha256 `28426d91089126c3a91dc6a068642130e023c77cd556a9c20533d0b5535f763b`.
   DATA: `DATA.ts001-reissue-evidence-20260922.md`.
3. `sources/SP-efficient-llm-2026/execution/compat/evidence-source-class-projection/run_frozen_evidence_chain.py`
   — AVAILABLE, HTTP 200 exit 0, size 14023, blob `792f7b6867e6ed74c0b2fc76896bd792dc51d31b`,
   sha256 `e338652b6a0d5f97c57d7d8084590f9f4dbced0e91c09cd362aa8b3ec55fd5dc`.
   DATA: `DATA.run_frozen_evidence_chain.py` (text-read only, never executed).
4. `sources/SP-efficient-llm-2026/execution/compat/evidence-source-class-projection/validation-report.md`
   — AVAILABLE, HTTP 200 exit 0, size 4548, blob `ca73fa6de6e5eab13b17b37a6d5922d17a997009`,
   sha256 `d8906e1d428b62846d3231f0cbe4e94eb7f21c7e040d2222679ffefdbd2cb78f`.
   DATA: `DATA.validation-report.md`.

Method: `gh api -i "<contents endpoint>?ref=<commit>"` per doc; raw stdout (headers+JSON),
headers split, command/exit/stderr saved (`get0N.command.txt/.exit.txt/.stderr.txt/.stdout.raw/.headers.txt/.body.json`).
Base64 decode verified `len==size` 4/4; `sha1("blob <len>\\0"+bytes)` == reported blob sha 4/4
(local hashlib, no git object creation). Response `path/url/html_url` match requested path+ref.

## 2. Explicit mapping original source_type → recommended/projected class (from these 4 docs ONLY)

Authoritative-in-these-4 source is defect doc §2 (RECORDED/BLOCKING/SHARED_CORE_UNCHANGED).
It lists 67/160 non-DROP tasks blocked on 10 source types absent from Core v2
`SOURCE_CLASS_MAP` (`scripts/survey_evidence_v2.py` lines 44–109), with
provenance-mirroring RECOMMENDED classes:

| Discovery source_type | Tasks | Recommended class (defect doc, NOT executed Core map) |
|---|---|---|
| PRIMARY_DOC | 13 | PRIMARY_OFFICIAL (first-party docs/recipes) |
| PRIMARY_REPO | 21 | PRIMARY_REPOSITORY |
| PRIMARY_ANNOUNCEMENT | 8 | PRIMARY_OFFICIAL |
| PRIMARY_MODEL_CARD | 6 | PRIMARY_OFFICIAL |
| PRIMARY_SPEC | 4 | PRIMARY_OFFICIAL |
| SECONDARY_REFERENCE | 8 | SECONDARY |
| SECONDARY_TECHNICAL | 4 | SECONDARY |
| RUNTIME_RECIPE | 1 | PRIMARY_OFFICIAL (maintainer recipe docs) |
| PACKAGING_DOCS | 1 | PRIMARY_OFFICIAL |
| RUNTIME_PR | 1 | PRIMARY_REPOSITORY |
| Total blocked | 67 | — |
| Runnable passthrough | 93 = PRIMARY_PAPER 92 + x-community-signal 1 | already mapped |

Validation-report §2 confirms compat execution preserved these counts:
Projected 67 / passthrough 93; per-type projected counts identical list
(PRIMARY_DOC 13, PRIMARY_REPO 21, PRIMARY_ANNOUNCEMENT 8, PRIMARY_MODEL_CARD 6,
PRIMARY_SPEC 4, SECONDARY_REFERENCE 8, SECONDARY_TECHNICAL 4, RUNTIME_RECIPE 1,
PACKAGING_DOCS 1, RUNTIME_PR 1). It asserts §7 invariant: only
`source_records[*].source_type` differs field-by-field, else `COMPATIBILITY_PROJECTION_INVALID`.

QUALIFICATION: These 4 docs do NOT contain the executed substitution strings
(e.g. which concrete mapped source_type value replaced each of the 10 in
`compat-package/package.json`, or the `build_compat_evidence_package.py` projection table/§7 definition).
Defect "Recommended class" is a class label (PRIMARY_OFFICIAL/PRIMARY_REPOSITORY/SECONDARY),
not proof of the projected source_type literal. Do NOT treat recommended class as
new canonical mapping authority. Actual compat-package bytes and builder logic are
out of this 4-doc scope — see §5 extra docs needed.

## 3. RUNTIME_RECIPE / PACKAGING_DOCS / RUNTIME_PR provenance + claim-vs-resource

What these 4 docs state:
- Each is 1 task (defect §2 + validation §2). Recommended: RUNTIME_RECIPE→PRIMARY_OFFICIAL
  (maintainer recipe docs), PACKAGING_DOCS→PRIMARY_OFFICIAL, RUNTIME_PR→PRIMARY_REPOSITORY.
- ts001 §5 lists 9 full-page fetches consumed for Evidence authorship without binding
  them to source_type in these docs: DSA launch/API-docs excerpts, ezyang V4.1 study,
  GenAI-Perf docs, vLLM V4.1 recipe, Unsloth GLM docs, llama.cpp PR 27742,
  Jev launch/concepts/models pages; plus arXiv bulk (95 records) and web-search gap-fill
  (SWE-bench-Pro 2509.16941+2609.08149, Terminal-Bench 2.0 2601.11868, DoReMi 2305.10429+CRFM).
- Candidate association (UNVERIFIED, do not adopt): vLLM V4.1 recipe plausibly the
  RUNTIME_RECIPE record; llama.cpp PR 27742 plausibly the RUNTIME_PR record; PACKAGING_DOCS
  counterpart not identified in these 4 docs. No Discovery IDs, URLs, or publisher
  excerpts for the 3 types are given in these 4 docs. Mechanical title cross-check
  (9 wrong-identity arXiv locators D005/D061/D062/D093/D094/D098/D112/D117/D139) is
  unrelated to these 3 types.

Claim-vs-resource: defect rationale classifies by provenance (maintainer recipe/docs as
official; PR as repository), but these 4 docs provide no direct raw/publisher bytes for
the 3 tasks to independently verify first-party vs third-party claim. Compat workaround
re-labels for Core passage; it does not create new publisher authority. Any Profile/support
applicability decision must not infer PRIMARY_OFFICIAL/REPOSITORY authority for these 3
from the recommended class alone.

## 4. Compat workaround vs canonical mapping authority

Recorded compat = edition-local WORKAROUND, explicitly NOT canonical/Core fix:
- Defect doc §§3–5: shared Core left unchanged (`git status` clean under scripts/schemas/config/workflows/docs);
  no silent patch/monkey-patch/fork; Discovery `source_records` always pass through `_source_class`
  (task_authority_sources line 423/923); supplement path cannot substitute Discovery authority;
  rewriting Discovery would falsify canonical bytes and is rejected. Resume requires reviewed Core
  repair on main + rebase + clean re-run; no PASS from failed/partial run carried forward.
- run_frozen header + body: driver replicates `run_evidence_v2_interactive.run()` step-for-step,
  substituting ONLY the Evidence package with edition-local derived compat package
  (built+validated+repro-tested by `build_compat_evidence_package.py`, NOT in these 4 docs);
  every judgment uses unmodified frozen Core functions; frozen `current_stage_basis_override`
  entered only at frozen-runner call sites for historical-basis tolerance; refuses to overwrite
  ledger/completeness; extra O13–O15 rows use frozen builder mechanical derivation + Luna
  provisional annotation.
- Validation-report status `WORKAROUND_VALIDATED (edition-local; CV2-DM-016 remains OPEN_CORE)`,
  explicitly `never CORE_FIXED`. Frozen-Core audit: no modification under scripts/schemas/config/workflows,
  no runtime monkey-patching, no Core source copied under execution tree, no canonical Discovery
  rewrite (SHA 7074cef2… unchanged), no Screening change (65330476… unchanged), main e69187f7/PR#518
  only docs entry. Chain PASS list (basis/package/input/cards/acceptance/views/ledger/completeness/stage/checkpoint)
  is workaround-chain evidence, not Core source-class authority.

Therefore: do NOT cite projected counts or WORKAROUND_VALIDATED as canonical SOURCE_CLASS_MAP
extension or Profile/support qualification. Canonical authority requires reviewed Core repair
(map extension + full regression) per defect §7 resume criteria, outside these 4 docs.

## 5. DM017 completeness row metadata (No New Access — only these 4 docs)

- ts001 §6 (r1 input): 160 records 155 PARTIAL/5 VERIFIED, 134 MATERIAL/24 CONTEXT/2 HOLD;
  Completeness block O01–O12: 3 SATISFIED/9 LIMITATION, LIMITED.
- run_frozen `EXTRA_OBLIGATIONS` (edition-authored, frozen-builder mechanical IDs + Luna provisional status/rationale):
  EFF-O13 dimension `attention_sequence_kv_cache` (Engram/sparsity axis, kNN-LM/RETRO boundaries, Qwen-PLE parallel);
  EFF-O14 `decoding_acceleration` (test-time scaling, budget forcing, ThinkPrune, overthinking/early-stopping, adaptive-TTC, effort-control);
  EFF-O15 `inference_kernels_serving` (FrugalGPT cascade, RouteLLM routing, 2026 survey unification, router-fragility).
  All 3 status LIMITATION with per-spec rationale; declaring Discovery IDs derived mechanically via
  `provenance.obligation_ids`; task IDs via ledger map; raises if names no records.
- Validation-report §1: `profile-completeness-v2.json` overall LIMITED; 15 obligations
  3 SATISFIED/12 LIMITATION incl. edition-authored O13/O14/O15 rows with Profile-declared dimensions;
  ledger 165 rows (MATERIAL 137/CONTEXT 23/EXCLUDED 5); evidence acceptance 160 (PARTIAL 148/VERIFIED 12).
- No new completeness bytes fetched. Declaring-ID lists, dimension membership proof, and Profile
  declaration source for O13–O15 are NOT in these 4 docs; do not assume DM017 SATISFACTION.

## 6. Findings + extra docs needed (STOP, await Human scope — no auto-fetch)

Findings:
- All 4 pinned docs retrieved and byte-verified.
- Only explicit source_type→class table in scope is the defect RECOMMENDED table; executed
  projection literals unverified in scope.
- RUNTIME_* 1-task each confirmed by count; raw/publisher binding absent in scope.
- DM017 O13–O15 metadata captured as above; closure/derivation proof absent in scope.
- Workaround validated as workaround; no canonical authority created.

If ROOT needs more, request new Human scope for (no fetch performed):
A. `execution/compat/evidence-source-class-projection/compat-package/package.json` + builder
   (`build_compat_evidence_package.py`) to verify actual projected source_type literals and §7 invariant;
B. canonical Discovery rows for the 3 RUNTIME_*/PACKAGING types (IDs, URLs, publisher) + supplement
   raw bytes reference;
C. `materiality-ledger-v2.json` / `profile-completeness-v2.json` accepted bytes for DM017 row closure;
D. Core `SOURCE_CLASS_MAP` post-repair diff if/when CV2-DM-016 lands (to confirm canonical authority).

Filepaths for ROOT: all under `notes/rephase-1-profile-support-contract/intake-20261030T124140Z/` —
`get0N.stdout.raw/.headers.txt/.body.json/.command.txt/.exit.txt/.stderr.txt`,
`DATA.*` (4 decoded), `manifest.json` (this intake), `intake-summary.md` (this file).
